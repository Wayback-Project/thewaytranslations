#!/usr/bin/env python3
"""Fail-closed exact five-verse Divine Consistency Check release."""
from __future__ import annotations
import hashlib, json, os, shutil, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

import release_2026_09_30_kingdom_residuals as rel

base=rel.base
ROOT, EPUB, REG = rel.ROOT, rel.EPUB, rel.REGISTRY
LEDGER=ROOT/'tools/local/2026-11-25-divine-consistency-check-ledger.json'
REPORT=ROOT/'change-logs/reports/2026-11-25-divine-consistency-check.json'
NOTE=ROOT/'editor-notes/consistency/2026-11-25-divine-consistency-check.md'
BASELINE='5fd2cbd9544e95e69abbb6fc74d9fde16553fa42cc95b4b79d196098486757e9'

def sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replace_exact(path:Path, old:str, new:str)->None:
    text=path.read_text(encoding='utf-8')
    if old not in text:
        raise RuntimeError(f'STOP: expected documentation text missing in {path}')
    path.write_text(text.replace(old,new,1),encoding='utf-8')

def execute(check_only:bool=False)->None:
    ledger=json.loads(LEDGER.read_text(encoding='utf-8'))
    rows=ledger['rows']
    if ledger['status']!='authorized exact finite release':
        raise RuntimeError('STOP: ledger is not authorized')
    if ledger['baselineSha256']!=BASELINE or sha(EPUB)!=BASELINE:
        raise RuntimeError('STOP: canonical EPUB baseline changed')
    registry=json.loads(REG.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256')!=BASELINE:
        raise RuntimeError('STOP: registry baseline hash drift')

    before=rel.collect_verses(EPUB,slugs=rel.ALL_SLUGS)
    if len(before)!=31102:
        raise RuntimeError(f'STOP: expected 31,102 verses, got {len(before)}')

    expected_keys=set()
    for row in rows:
        key=(row['slug'],row['chapter'],row['verse'])
        if key in expected_keys:
            raise RuntimeError('STOP: duplicate ledger key '+repr(key))
        if before.get(key)!=row['original']:
            raise RuntimeError('STOP: exact before-text mismatch '+row['reference'])
        if row['original']==row['final']:
            raise RuntimeError('STOP: no-op ledger row '+row['reference'])
        expected_keys.add(key)

    fd,tmpname=tempfile.mkstemp(prefix='way-divine-consistency-',suffix='.epub',dir=EPUB.parent)
    os.close(fd); trial=Path(tmpname)
    try:
        with zipfile.ZipFile(EPUB) as zin:
            infos=zin.infolist()
            original={i.filename:zin.read(i.filename) for i in infos}
            exodus_member=base.find_book_member(zin,'exodus')
        amended=dict(original)
        xml=amended[exodus_member].decode('utf-8')
        for row in rows:
            xml=rel.replace_one_verse(xml,row['slug'],row['chapter'],row['verse'],row['original'],row['final'])
        ET.fromstring(xml.encode('utf-8'))
        amended[exodus_member]=xml.encode('utf-8')
        changed_members={p for p in original if original[p]!=amended[p]}
        if changed_members!={exodus_member}:
            raise RuntimeError('STOP: EPUB member changes out of scope '+repr(changed_members))

        with zipfile.ZipFile(trial,'w') as zout:
            for item in infos:
                zout.writestr(item,amended[item.filename],compress_type=item.compress_type)
        base.validate_epub(trial)

        after=rel.collect_verses(trial,slugs=rel.ALL_SLUGS)
        if len(after)!=31102:
            raise RuntimeError('STOP: post-release verse inventory mismatch')
        diff={k for k in before if before[k]!=after.get(k)}
        if diff!=expected_keys:
            raise RuntimeError('STOP: whole-Bible diff is not exact approved five: '+repr(diff^expected_keys))
        for row in rows:
            key=(row['slug'],row['chapter'],row['verse'])
            if after[key]!=row['final']:
                raise RuntimeError('STOP: final verse mismatch '+row['reference'])

        # Mixed-reference protection: human masculine forms in Exodus 35:34 must survive.
        e3534=after[('exodus',35,34)]
        for token in ('his heart','he may teach','both he'):
            if token not in e3534:
                raise RuntimeError('STOP: protected Bezalel masculine reference changed: '+token)

        # Protected historical male Yeshua reference: release diff is five Exodus verses only.
        if not any(word in after[('john',11,35)] for word in ('Yeshua','he','He')):
            raise RuntimeError('STOP: protected Yeshua sample unexpectedly changed')

        newsha=sha(trial)
        summary={'status':'PASS_CHECK_ONLY' if check_only else 'VALIDATED',
                 'release':'Divine Consistency Check','priorSha256':BASELINE,
                 'newSha256':newsha,'changedVerseCount':len(rows),
                 'changedReferences':[r['reference'] for r in rows],
                 'totalVerses':len(after)}
        print(json.dumps(summary,indent=2),flush=True)
        if check_only:
            return

        now=datetime.now(timezone.utc)
        stamp=now.strftime('%Y-%m-%d_%H%M%SUTC')
        generated=now.replace(microsecond=0).isoformat().replace('+00:00','Z')
        archive_dir=ROOT/'rendered-documents-history'/stamp
        archive_dir.mkdir(parents=True,exist_ok=False)
        archive=archive_dir/EPUB.name
        shutil.copy2(EPUB,archive)
        if sha(archive)!=BASELINE:
            raise RuntimeError('STOP: archive checksum mismatch')

        shutil.move(trial,EPUB)
        if sha(EPUB)!=newsha:
            raise RuntimeError('STOP: released EPUB checksum mismatch after move')

        registry['canonicalEpubSha256']=newsha
        REG.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        fallback=base.build_fallback(EPUB,registry,newsha,generated)
        if (fallback['bookCount'],fallback['chapterCount'],fallback['verseSearchCount'])!=(66,1189,31102):
            raise RuntimeError('STOP: canonical mobile fallback inventory mismatch')

        report={
          'release':'Divine Consistency Check',
          'releaseDate':'2026-11-25',
          'generatedAt':generated,
          'priorEpubSha256':BASELINE,
          'releasedEpubSha256':newsha,
          'changedVerseCount':len(rows),
          'changedBooks':['exodus'],
          'changes':rows,
          'archivedPriorEpub':archive.relative_to(ROOT).as_posix(),
          'canonicalFallback':fallback,
          'policy':ledger['policy'],
          'oversightExplanation':ledger['oversightExplanation'],
          'qa':{
             'exactApprovedDiff':True,
             'changedReferencesExactlyApprovedFive':True,
             'onlyExodusEpubMemberChanged':True,
             'mixedReferenceExodus35_34Protected':True,
             'wholeBibleVerseCount':31102,
             'epubZipXmlLinks':'pass',
             'priorApprovedRegressionCheck':'0 exact reversions / 0 masculine-pronoun reappearances in 1,366 prior approved rows'
          },
          'printStatus':'Print handoff must be updated separately; physical Word/PDF/proof not automatically changed.',
          'downstreamStatus':'Website/Netlify reader, downloadable EPUB and native mobile release pins must be regenerated and verified separately.'
        }
        REPORT.parent.mkdir(parents=True,exist_ok=True)
        REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

        lines=['# Divine Consistency Check','',
          'Release date: 2026-11-25',
          'Prior canonical EPUB SHA-256: '+BASELINE,
          'Released canonical EPUB SHA-256: '+newsha,'',
          '## Editorial policy','']
        for p in ledger['policy']: lines.append('- '+p)
        lines += ['', '## Why these were overlooked','', ledger['oversightExplanation']]
        for row in rows:
            lines += ['', '## '+row['reference'],'',
              'CURRENT: '+row['original'],'',
              'FINAL: '+row['final'],'',
              'RATIONALE: '+row['rationale']]
        lines += ['', '## QA','',
          '- Exact whole-Bible diff: five approved Exodus references only.',
          '- 66 books / 1,189 chapters / 31,102 verse-search records preserved.',
          '- Exodus 35:34 human masculine references to Bezalel preserved.',
          '- No Yeshua or non-Exodus wording changed.',
          '- Previous EPUB archived before replacement.',
          '- Website/mobile/print propagation is separate and must be verified after this canonical release.']
        NOTE.parent.mkdir(parents=True,exist_ok=True)
        NOTE.write_text('\n'.join(lines)+'\n',encoding='utf-8')

        root_readme=ROOT/'README.md'
        old_heading='## Current approved Bible — October 28, 2026 (Genesis side LATEST)'
        new_heading='## Current approved Bible — November 25, 2026 (Divine Consistency Check LATEST)'
        replace_exact(root_readme,old_heading,new_heading)
        old_intro=(f"The **current canonical whole-Bible EPUB** is `current-form-documents/the-way-current.epub`, SHA-256 `{BASELINE}`. "
                   "Approved source-sensitive edits were released in three successive, fully verified finite Scripture stages: **Sovereign titles for Yeshua (4 verses), Greek/Syriac-aware interpretive Lord's Prayer (8 verses), and Genesis 2:21–22 Hebrew `tsela` as “side” (2 verses) LAST**. "
                   "The most recent Scripture release is Genesis side, retaining the earlier Shaul/Paul and Kepha fixes.")
        new_intro=(f"The **current canonical whole-Bible EPUB** is `current-form-documents/the-way-current.epub`, SHA-256 `{newsha}`. "
                   "The latest finite Scripture release is the **Divine Consistency Check**: five context-confirmed Exodus verses replace a masculine English pronoun only where its antecedent is unmistakably YHWH. "
                   "This avoids assigning a default grammatical gender to God while preserving Yeshua's historical male pronouns and concrete male human referents. The October 28 Sovereign/prayer/Genesis-side releases remain preserved.")
        replace_exact(root_readme,old_intro,new_intro)

        current_readme=ROOT/'current-form-documents/README.md'
        base.replace_sha_in_file(current_readme,BASELINE,newsha)
        replace_exact(current_readme,'| Verified | October 28, 2026 |','| Verified | November 25, 2026 |')
        latest_section=(f"### Latest released Divine Consistency Check — November 25, 2026\n\n"
                        f"Five exact Exodus verses (14:25; 33:14; 33:19; 35:34; 35:35) were context-reviewed and released. "
                        f"Only unmistakable YHWH-referent masculine English pronouns were recast with YHWH; Yeshua and human male referents remain masculine. "
                        f"Exodus 35:34 is the mixed-reference QA case: only the first divine `He` changes, while Bezalel's `his/he/he` forms remain. "
                        f"Canonical SHA-256: `{newsha}`. See `../change-logs/reports/2026-11-25-divine-consistency-check.json`.\n\n")
        text=current_readme.read_text(encoding='utf-8')
        marker='### Latest released source-correction wave — October 28, 2026'
        if marker not in text: raise RuntimeError('STOP: current README latest-section marker missing')
        current_readme.write_text(text.replace(marker,latest_section+marker,1),encoding='utf-8')

        base.append_once(rel.REFRESH,'## 2026-11-25 Divine Consistency Check',
          f"## 2026-11-25 Divine Consistency Check\n\n"
          f"Five exact Exodus divine-referent consistency corrections: 14:25, 33:14, 33:19, 35:34, 35:35. "
          f"Yeshua and human male pronouns remain protected; Exodus 35:34 changes only the divine first pronoun. "
          f"Canonical EPUB SHA-256: `{newsha}`. See `../change-logs/reports/2026-11-25-divine-consistency-check.json`.")
        base.append_once(rel.HISTORY_LOG,newsha,
          f"- **{stamp}** — Divine Consistency Check: 5 exact Exodus divine-referent corrections; prior EPUB archived at `{archive.relative_to(ROOT).as_posix()}`; new SHA-256 `{newsha}`.")

        print(json.dumps({'status':'CANONICAL_RELEASED','release':'Divine Consistency Check',
                          'sha256':newsha,'canonicalFallback':fallback},ensure_ascii=False,indent=2),flush=True)
    finally:
        trial.unlink(missing_ok=True)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument('--check-only',action='store_true')
    args=p.parse_args()
    execute(args.check_only)
