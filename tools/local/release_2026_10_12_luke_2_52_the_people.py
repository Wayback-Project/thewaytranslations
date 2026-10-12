#!/usr/bin/env python3
"""Approved one-verse canonical release: Luke 2:52 -> the people."""
from __future__ import annotations
import json, os, shutil, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path
import release_2026_09_30_kingdom_residuals as rel

base = rel.base
ROOT, EPUB, REG = rel.ROOT, rel.EPUB, rel.REGISTRY
OLD_SHA = 'a1493bfd9f38181c5e552880f7156ef609a8e83550ee459d9ed01db4b3db1c897'
BEFORE = 'And Yeshua increased in wisdom and stature, and in favor with Elohim and people.'
AFTER = 'And Yeshua increased in wisdom and stature, and in favor with Elohim and the people.'
SOURCE = ROOT / 'original-documents/luke_restorative_translation.txt'
REPORT = ROOT / 'change-logs/reports/2026-10-12-luke-2-52-the-people-release.json'
NOTE = ROOT / 'editor-notes/consistency/2026-10-12-luke-2-52-the-people-release.md'

def verses():
    return rel.collect_verses(EPUB, slugs=rel.ALL_SLUGS)

def edit_binary():
    with zipfile.ZipFile(EPUB) as z:
        infos = z.infolist()
        orig = {info.filename:z.read(info.filename) for info in infos}
        member = base.find_book_member(z,'luke')
    before_xml=orig[member].decode('utf-8')
    after_xml=rel.replace_one_verse(before_xml, 'luke', 2, 52, BEFORE, AFTER)
    if after_xml == before_xml: raise RuntimeError('Luke 2:52 not replaced')
    edited=dict(orig); edited[member]=after_xml.encode('utf-8')
    fd,tmpname=tempfile.mkstemp(prefix='way-luke-2-52-',suffix='.epub',dir=EPUB.parent)
    os.close(fd); tmp=Path(tmpname)
    try:
        with zipfile.ZipFile(tmp,'w') as out:
            for info in infos: out.writestr(info,edited[info.filename],compress_type=info.compress_type)
        base.validate_epub(tmp)
        shutil.move(tmp,EPUB)
    finally: tmp.unlink(missing_ok=True)
    changed=[p for p in orig if orig[p]!=edited[p]]
    if changed!=[member]: raise RuntimeError('EPUB member changes outside Luke: '+repr(changed))
    return member

def main():
    if base.sha256(EPUB)!=OLD_SHA: raise RuntimeError('Canonical EPUB baseline changed; stop')
    before_all=verses()
    if len(before_all)!=31102 or before_all.get(('luke',2,52))!=BEFORE:
        raise RuntimeError('Original Bible count or Luke 2:52 mismatch')
    issues,exceptions=rel.grammar.audit_epub(EPUB)
    if issues: raise RuntimeError('Baseline grammar audit failed')
    now=datetime.now(timezone.utc)
    stamp=now.strftime('%Y-%m-%d_%H%M%SUTC')
    generated=now.replace(microsecond=0).isoformat().replace('+00:00','Z')
    archive_dir=ROOT/'rendered-documents-history'/stamp
    archive_dir.mkdir(parents=True,exist_ok=False)
    archive=archive_dir/EPUB.name
    shutil.copy2(EPUB,archive)
    if base.sha256(archive)!=OLD_SHA: raise RuntimeError('Archive corrupt')
    member=edit_binary()
    new_sha=base.sha256(EPUB)
    after_all=verses()
    if len(after_all)!=31102 or after_all.get(('luke',2,52))!=AFTER:
        raise RuntimeError('After release verse count/text mismatch')
    diffs={k for k in before_all if before_all[k]!=after_all[k]}
    if diffs!={('luke',2,52)}: raise RuntimeError('Unexpected changes outside Luke 2:52: '+repr(diffs))
    issues_after,exceptions_after=rel.grammar.audit_epub(EPUB)
    if issues_after or len(exceptions)!=len(exceptions_after):
        raise RuntimeError('Grammar QA regressed')
    source=SOURCE.read_text(encoding='utf-8')
    if source.count('52. '+BEFORE)!=1:
        raise RuntimeError('Editable Luke source not aligned with old verse')
    SOURCE.write_text(source.replace('52. '+BEFORE,'52. '+AFTER,1),encoding='utf-8')
    registry=json.loads(REG.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256')!=OLD_SHA:
        raise RuntimeError('Canonical name registry baseline drift')
    registry['canonicalEpubSha256']=new_sha
    REG.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fallback=base.build_fallback(EPUB,registry,new_sha,generated)
    if (fallback.get('bookCount'),fallback.get('chapterCount'),fallback.get('verseSearchCount'))!=(66,1189,31102):
        raise RuntimeError('Mobile fallback generated wrong inventory')
    rationale=(
      'Luke 2:52 uses Greek ἀνθρώποις (anthrōpois), the plural human noun, '
      'in contrast to θεῷ (God/Elohim). In the historical social setting it '
      'speaks of Yeshua gaining favor with people, not solely men. '
      'The Way Version editorial choice “the people” is natural English collective '
      'wording for those among whom Yeshua grew and was known. The English '
      'definite article is a style/context decision, not a claim that there '
      'is a separate Greek article before ἀνθρώποις. This is one exact verse '
      'edit, not a global replacement of the word people.'
    )
    report={'release':'Luke 2:52 the people','releaseDate':'2026-10-12',
      'status':'editor-authorized','oldEpubSha256':OLD_SHA,'releasedEpubSha256':new_sha,
      'archivePath':archive.relative_to(ROOT).as_posix(),
      'changes':[{'reference':'Luke 2:52','before':BEFORE,'after':AFTER,
                  'Greek':'ἀνθρώποις','rationale':rationale}],
      'changedVerseCount':1,'wholeBibleVerseCount':31102,
      'changedEpubMembers':[member],'qa':{'zipXmlLinks':'pass','onlyLuke2_52Changed':True,
         'books':66,'chapters':1189,'verses':31102,'grammar':'pass'},
      'canonicalMobileFallback':fallback}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    NOTE.write_text('# Luke 2:52 — “the people”\n\nBEFORE: '+BEFORE+
      '\n\nAFTER: '+AFTER+'\n\nRationale: '+rationale+
      '\n\nOnly Luke 2:52 changed in 31,102 canonical verse records. '+
      'The homepage example already has “the people.”\n\n'+
      'Previous canonical EPUB SHA-256: '+OLD_SHA+
      '\nNew canonical EPUB SHA-256: '+new_sha+
      '\nPrior EPUB archive: '+archive.relative_to(ROOT).as_posix()+
      '\nAll downstream website, app and mobile data must be regenerated from the new EPUB.\n',encoding='utf-8')
    base.append_once(rel.HISTORY_LOG,new_sha,
      f'- {stamp} — one-verse Luke 2:52 “the people”; previous EPUB archived at {archive.relative_to(ROOT).as_posix()}; SHA-256 {new_sha}.')
    base.append_once(rel.REFRESH,'## 2026-10-12 Luke 2:52 “the people”',
      '## 2026-10-12 Luke 2:52 “the people”\n\n'
      'One-verse release replacing “Elohim and people” with “Elohim and the people.” '
      'New EPUB SHA-256: '+new_sha+'. No other Scripture changes.')
    base.replace_sha_in_file(rel.ROOT_README,OLD_SHA,new_sha)
    base.replace_sha_in_file(rel.CURRENT_README,OLD_SHA,new_sha)
    print(json.dumps({'releasedEpubSha256':new_sha,'changedVerses':len(diffs),
      'canonicalMobileFallback':fallback},indent=2))

if __name__=='__main__': main()
