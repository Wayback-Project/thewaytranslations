#!/usr/bin/env python3
"""Fail-closed, canonical-only nine-verse Greek / original-name release."""
from __future__ import annotations

import argparse, json, os, re, shutil, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET
import release_2026_09_30_kingdom_residuals as rel

base = rel.base
ROOT, EPUB, REG = rel.ROOT, rel.EPUB, rel.REGISTRY
BASE = '785a21b93491ca5433f0bfaff849cfd7eb6f42957072cd5fe722a60dfb0d0a90'
LEDGER = ROOT/'tools/local/2026-10-20-source-gloss-nine-verse-release.json'
REPORT = ROOT/'change-logs/reports/2026-10-20-original-names-nine-verse-release.json'
NOTE = ROOT/'editor-notes/consistency/2026-10-20-source-gloss-nine-verse-release.md'
SCOPE = {('acts',13,9),('acts',11,13),('john',1,42),('john',4,25),
         ('matthew',10,3),('mark',3,18),('luke',6,14),('acts',1,13),('matthew',16,18)}

def scan(path):
    return rel.collect_verses(path, slugs=rel.ALL_SLUGS)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check-only', action='store_true')
    args=parser.parse_args()
    sha=base.sha256(EPUB)
    if sha!=BASE: raise RuntimeError('Source EPUB SHA changed; stop stale release: '+sha)
    ledger=json.loads(LEDGER.read_text(encoding='utf-8'))
    rows=ledger['edits']
    if ledger['canonicalBaselineEpubSha256']!=BASE or ledger['changedVerseCount']!=9 or len(rows)!=9:
        raise RuntimeError('Ledger/provenance/count mismatch')
    prior=scan(EPUB)
    if len(prior)!=31102: raise RuntimeError('Canonical verse inventory not 31,102')
    keys={(r['slug'],r['chapter'],r['verse']) for r in rows}
    if keys != SCOPE: raise RuntimeError('Edited verse set is NOT the 9 user-authorized refs')
    for r in rows:
        k=(r['slug'],r['chapter'],r['verse'])
        if prior.get(k)!=r['original'] or r['original']==r['final']:
            raise RuntimeError('Original full verse mismatch at '+str(k))
        if '  ' in r['final'] or re.search(r'\s+[,.!?;:]',r['final']):
            raise RuntimeError('New grammar whitespace problem at '+str(k))
    article_before,exceptions_before=rel.grammar.audit_epub(EPUB)
    if article_before: raise RuntimeError('Baseline article grammar audit failed')
    fd,temp=tempfile.mkstemp(prefix='way-original-name-gloss-',suffix='.epub',dir=EPUB.parent)
    os.close(fd); trial=Path(temp)
    try:
        with zipfile.ZipFile(EPUB,'r') as zin:
            infos=zin.infolist()
            original={i.filename:zin.read(i.filename) for i in infos}
            affected={slug:base.find_book_member(zin,slug) for slug in sorted({r['slug'] for r in rows})}
        changed=dict(original)
        for slug,member in affected.items():
            xml=changed[member].decode('utf-8')
            for r in rows:
                if r['slug']==slug:
                    xml=rel.replace_one_verse(xml,slug,r['chapter'],r['verse'],r['original'],r['final'])
            ET.fromstring(xml.encode('utf-8'))
            changed[member]=xml.encode('utf-8')
        memberdiff={m for m in original if original[m]!=changed[m]}
        if memberdiff!=set(affected.values()): raise RuntimeError('EPUB member diff not exactly 5 reviewed NT books')
        with zipfile.ZipFile(trial,'w') as z:
            for info in infos:z.writestr(info,changed[info.filename],compress_type=info.compress_type)
        base.validate_epub(trial)
        after=scan(trial)
        diffkeys={k for k in prior if prior[k]!=after.get(k)}
        if len(after)!=31102 or diffkeys!=SCOPE:
            raise RuntimeError('Unexpected whole-Bible diff: '+repr(sorted(diffkeys ^ SCOPE)))
        for r in rows:
            if after[(r['slug'],r['chapter'],r['verse'])]!=r['final']:
                raise RuntimeError('Final full verse failed '+r['reference'])
        protections={
            ('acts',13,7):'Sergius Paulus',
            ('acts',13,13):'Shaul',
            ('romans',1,1):'Shaul',
            ('john',11,16):'Ta\'oma',
            ('john',21,7):'Shimon (called Kepha)',
            ('matthew',10,2):'Shimon (called Kepha)',
            ('genesis',35,10):'no longer be called Yaakov'
        }
        for k,word in protections.items():
            if prior[k]!=after[k] or word not in after[k]:
                raise RuntimeError('Protected context changed '+repr(k))
        if 'also called Shaul' in after[('acts',13,9)]:
            raise RuntimeError('Known Shaul/Shaul collision remains')
        if 'whose surname is Shimon (called Kepha)' in after[('acts',11,13)]:
            raise RuntimeError('Known Kepha alias nesting remains')
        for k in [('matthew',10,3),('mark',3,18),('luke',6,14),('acts',1,13)]:
            if 'Nethanel' in after[k] or 'Bar-Tolmai' not in after[k]:
                raise RuntimeError('Unproven Nathanael apostle-list identity remains')
        article_after,exceptions_after=rel.grammar.audit_epub(trial)
        if article_after or len(exceptions_after)!=len(exceptions_before):
            raise RuntimeError('English grammar regression')
        newsha=base.sha256(trial)
        if args.check_only:
            print(json.dumps({'status':'PASS_PREVIEW','baselineSha256':BASE,'newSha256':newsha,
              'changedVerses':9,'changedBooks':sorted(affected),'epubMembers':sorted(memberdiff),
              'fullBibleVerses':31102,'books':66,'chapters':1189,
              'zipCrcXmlInternalLinks':'PASS','unchangedVerses':31093,'published':False}))
            return
        now=datetime.now(timezone.utc)
        stamp=now.strftime('%Y-%m-%d_%H%M%SUTC')
        date=now.replace(microsecond=0).isoformat().replace('+00:00','Z')
        archive_dir=ROOT/'rendered-documents-history'/stamp
        archive_dir.mkdir(parents=True,exist_ok=False)
        archive=archive_dir/EPUB.name
        shutil.copy2(EPUB,archive)
        if base.sha256(archive)!=BASE: raise RuntimeError('Archive integrity failure')
        registry=json.loads(REG.read_text(encoding='utf-8'))
        if registry.get('canonicalEpubSha256')!=BASE:raise RuntimeError('Registry SHA provenance mismatch')
        shutil.move(trial,EPUB)
        registry['canonicalEpubSha256']=newsha
        REG.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        fallback=base.build_fallback(EPUB,registry,newsha,date)
        if tuple(fallback.get(x) for x in ('bookCount','chapterCount','verseSearchCount'))!=(66,1189,31102):
            raise RuntimeError('Fallback integrity violation')
        report={'release':ledger['release'],'date':date,'priorEpubSha256':BASE,
            'releasedEpubSha256':newsha,'changedVerseCount':9,'changes':rows,
            'changedEpubMembers':sorted(memberdiff),
            'archivedPriorEpub':archive.relative_to(ROOT).as_posix(),
            'canonicalFallback':fallback,
            'qa':{'exactDiffOnlyApproved':True,'verseCount':31102,'noUnrelatedScriptureChanges':True,
              'epubZipXmlLinks':'pass','grammar':'pass','sourceAliasControls':'pass'},
            'siteAndMobileStatus':'Website netlify, main and native must sync separately from this release',
            'printStatus':'Google Doc register handoff only; physical Word master/PDF/proof not updated'}
        REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        NOTE.write_text('# Source-name and Greek-language gloss repair — 2026-10-20\n\n'
            'User-approved exact nine-verse NT correction. Preserve the Greek distinction '
            'of Saulos/Paulos, Kepha/Petros and Messias/Christos; apostle lists identify '
            'Bar-Tolmai by the Greek text, not an unproven Nathanael identification. '
            'Contextual narrative uses Shimon (called Kepha) remain protected where they '
            'are not an incorrect alias definition.\n\n'
            f'Old canonical SHA-256: {BASE}\nNew canonical SHA-256: {newsha}\n'
            f'Archive: {archive.relative_to(ROOT).as_posix()}\n'
            'Nine authorized Scripture verses changed; 31,093 other verses unchanged. '
            '66 books / 1,189 chapters / 31,102 verse records. '
            'Validated ZIP/CRC/XML/link integrity and no grammar regression.\n',
            encoding='utf-8')
        base.append_once(rel.HISTORY_LOG,newsha,
            f'- {stamp} — Nine NT source-name/Greek gloss verse fixes; prior EPUB archive '
            f'{archive.relative_to(ROOT).as_posix()}; new SHA-256 {newsha}.')
        base.append_once(rel.REFRESH,'## 2026-10-20 Nine NT source-name / Greek gloss corrections',
            f'## 2026-10-20 Nine NT source-name / Greek gloss corrections\n\n'
            f'Exact 9 verses across Acts, John, Matthew, Mark and Luke; new canonical SHA-256 {newsha}. '
            'Greek alias / apostle-list fidelity and whole-Bible QA verified.')
        base.replace_sha_in_file(rel.ROOT_README,BASE,newsha)
        base.replace_sha_in_file(rel.CURRENT_README,BASE,newsha)
        print(json.dumps({'status':'CANONICAL_RELEASED','newSha256':newsha,
            'changedVerses':9,'canonicalFallback':fallback},ensure_ascii=False))
    finally:
        trial.unlink(missing_ok=True)

if __name__=='__main__':
    main()
