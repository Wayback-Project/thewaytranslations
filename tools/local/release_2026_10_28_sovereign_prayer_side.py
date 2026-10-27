#!/usr/bin/env python3
"""Fail-closed staged EPUB release. Last public canonical stage is Genesis side."""
import argparse, json, hashlib, os, re, shutil, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET
import release_2026_09_30_kingdom_residuals as rel
base=rel.base
ROOT, EPUB, REG=rel.ROOT,rel.EPUB,rel.REGISTRY
LEDGER=ROOT/'tools/local/2026-10-28-sovereign-prayer-side-ledger.json'
STAGES=['sovereign','prayer','rib']
PREFIX='2026-10-28-sovereign-prayer-side-'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def report(stage):return ROOT/'change-logs/reports'/(PREFIX+stage+'.json')
def execute(stage, preview):
    ledger=json.loads(LEDGER.read_text(encoding='utf-8'))
    rows=ledger['stages'][stage]
    i=STAGES.index(stage)
    expected=ledger['baselineSha256'] if i==0 else json.loads(report(STAGES[i-1]).read_text(encoding='utf-8'))['releasedEpubSha256']
    if sha(EPUB)!=expected:raise RuntimeError('STOP: canonical baseline changed: '+sha(EPUB))
    registry=json.loads(REG.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256')!=expected:raise RuntimeError('STOP: registry hash drift')
    before=rel.collect_verses(EPUB,slugs=rel.ALL_SLUGS)
    if len(before)!=31102:raise RuntimeError('STOP: 31,102 verse baseline mismatch')
    keys=set()
    for r in rows:
        k=(r['slug'],r['chapter'],r['verse'])
        if k in keys or before.get(k)!=r['original'] or r['original']==r['final']:
            raise RuntimeError('STOP: ledger mismatch '+str(k))
        if '  ' in r['final'] or re.search(r'\s+[,.!?;:]',r['final']):
            raise RuntimeError('STOP: punctuation whitespace '+str(k))
        keys.add(k)
    fd,name=tempfile.mkstemp(prefix='way-'+stage+'-',suffix='.epub',dir=EPUB.parent)
    os.close(fd);trial=Path(name)
    try:
        with zipfile.ZipFile(EPUB) as z:
            infos=z.infolist()
            orig={entry.filename:z.read(entry.filename) for entry in infos}
            members={slug:base.find_book_member(z,slug) for slug in {r['slug'] for r in rows}}
        amended=dict(orig)
        for slug,member in members.items():
            xml=amended[member].decode('utf-8')
            for r in rows:
                if r['slug']==slug:xml=rel.replace_one_verse(xml,slug,r['chapter'],r['verse'],r['original'],r['final'])
            ET.fromstring(xml.encode('utf-8'))
            amended[member]=xml.encode('utf-8')
        if {p for p in orig if orig[p]!=amended[p]}!=set(members.values()):
            raise RuntimeError('STOP: EPUB member changes out of scope')
        with zipfile.ZipFile(trial,'w') as z:
            for item in infos:z.writestr(item,amended[item.filename],compress_type=item.compress_type)
        base.validate_epub(trial)
        after=rel.collect_verses(trial,slugs=rel.ALL_SLUGS)
        diff={k for k in before if before[k]!=after.get(k)}
        if len(after)!=31102 or diff!=keys:raise RuntimeError('STOP: whole-Bible diff out of scope '+repr(diff^keys))
        for r in rows:
            k=(r['slug'],r['chapter'],r['verse'])
            if after[k]!=r['final']:raise RuntimeError('STOP: generated verse mismatch '+str(k))
        for k,value in {('acts',13,9):'who is also called Paul',('genesis',3,20):'Havvah',('daniel',7,5):'three ribs',('john',1,42):'Petros in Greek'}.items():
            if value not in after[k]:raise RuntimeError('STOP: protected older release '+str(k))
        if stage=='rib' and any('rib' in after[('genesis',2,v)].lower() for v in (21,22)):
            raise RuntimeError('STOP: Genesis rib not repaired')
        aftersha=sha(trial)
        print(json.dumps({'stage':stage,'status':'PASS_PREVIEW' if preview else 'VALIDATED','priorSha256':expected,
                          'newSha256':aftersha,'changedVerseCount':len(rows),'totalVerses':31102}),flush=True)
        if preview:return
        utc=datetime.now(timezone.utc)
        stamp=utc.strftime('%Y-%m-%d_%H%M%SUTC')
        date=utc.replace(microsecond=0).isoformat().replace('+00:00','Z')
        archive_dir=ROOT/'rendered-documents-history'/stamp
        archive_dir.mkdir(parents=True,exist_ok=False)
        archive=archive_dir/EPUB.name
        shutil.copy2(EPUB,archive)
        if sha(archive)!=expected:raise RuntimeError('STOP: archive failure')
        shutil.move(trial,EPUB)
        registry['canonicalEpubSha256']=aftersha
        REG.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        fallback=base.build_fallback(EPUB,registry,aftersha,date)
        if (fallback['bookCount'],fallback['chapterCount'],fallback['verseSearchCount'])!=(66,1189,31102):
            raise RuntimeError('STOP: fallback inventory mismatch')
        data={'release':ledger['title'],'stage':stage,'date':date,'priorEpubSha256':expected,
              'releasedEpubSha256':aftersha,'changedVerseCount':len(rows),'changes':rows,
              'archivedPriorEpub':archive.relative_to(ROOT).as_posix(),
              'canonicalFallback':fallback,
              'qa':{'exactApprovedDiff':True,'unchangedVerses':31102-len(rows),'epubZipXmlLinks':'pass'},
              'methodology':ledger['sourceNotes'],
              'printStatus':'Print Word/PDF not automatically updated',
              'downstreamStatus':'Netlify reader and native mobile release must be verified separately'}
        report(stage).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        note=ROOT/'editor-notes/consistency'/(PREFIX+stage+'.md')
        lines=['# '+ledger['title'],'','Stage: '+stage,'Date: '+date,
               'Prior canonical EPUB SHA-256: '+expected,'Released EPUB SHA-256: '+aftersha,'',
               'Methodology: Greek and Syriac/Peshitta corroboration; interpretive expansions are not literal Aramaic.','']
        for statement in ledger['sourceNotes']:lines.extend(['- '+statement])
        for r in rows:lines.extend(['', '## '+r['reference'],'','CURRENT: '+r['original'],'',
                                     'FINAL: '+r['final'],'','RATIONALE: '+r['rationale'],''])
        note.write_text('\n'.join(lines)+'\n',encoding='utf-8')
        base.append_once(rel.HISTORY_LOG,aftersha,'- '+stamp+' — '+stage+' staged Scripture release; '+str(len(rows))+
                         ' verses; previous EPUB archived '+archive.relative_to(ROOT).as_posix()+'; SHA-256 '+aftersha+'.')
        base.replace_sha_in_file(rel.ROOT_README,expected,aftersha)
        base.replace_sha_in_file(rel.CURRENT_README,expected,aftersha)
        base.append_once(rel.REFRESH,'## 2026-10-28 '+stage+' staged canonical release',
                         '## 2026-10-28 '+stage+' staged canonical release\n\n'+
                         str(len(rows))+' exact changed verses; canonical EPUB SHA-256 '+aftersha+'. '+\
                         'See change-logs/reports/'+PREFIX+stage+'.json.')
        print(json.dumps({'stage':stage,'status':'CANONICAL_RELEASED','sha256':aftersha}),flush=True)
    finally:trial.unlink(missing_ok=True)
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--stage',required=True,choices=STAGES)
    parser.add_argument('--check-only',action='store_true')
    args=parser.parse_args()
    execute(args.stage,args.check_only)
