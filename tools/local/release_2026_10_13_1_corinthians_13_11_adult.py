#!/usr/bin/env python3
"""Release only 1 Corinthians 13:11: 'become a person' -> 'become an adult'.

New Testament Greek ὅτε γέγονα ἀνήρ contrasts childhood with adulthood.
Inclusive 'adult' preserves the point without implying the speaker was not
previously human. Retain every other word of the approved canonical verse.
"""
from __future__ import annotations

import hashlib, json, os, shutil, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path
import release_2026_09_30_kingdom_residuals as rel

base=rel.base
ROOT,EPUB,REGISTRY=rel.ROOT,rel.EPUB,rel.REGISTRY
SOURCE=ROOT/'original-documents/rest_of_new_testament_restorative_translation.txt'
OLD_SHA='5afdb333aa06d83d4f98211251d563c6ba2077ca054a08cf7a000a4f399c29a0'
BEFORE='When I was a child, I spoke as a child, I felt as a child, I thought as a child. Now that I have become a person, I have put away childish things.'
AFTER='When I was a child, I spoke as a child, I felt as a child, I thought as a child. Now that I have become an adult, I have put away childish things.'
KEY=('1-corinthians',13,11)
REPORT=ROOT/'change-logs/reports/2026-10-13-1-corinthians-13-11-adult-release.json'
NOTE=ROOT/'editor-notes/consistency/2026-10-13-1-corinthians-13-11-adult-release.md'

def verses():
    return rel.collect_verses(EPUB,slugs=rel.ALL_SLUGS)

def main():
    if base.sha256(EPUB)!=OLD_SHA:
        raise RuntimeError('Canonical EPUB baseline changed; no release. Verify against latest EPUB.')
    before=verses()
    if len(before)!=31102 or before.get(KEY)!=BEFORE:
        raise RuntimeError('Baseline 31,102 verse inventory / 1 Corinthians 13:11 before mismatch')
    issues,exceptions=rel.grammar.audit_epub(EPUB)
    if issues:
        raise RuntimeError('Canonical English-article audit baseline not clean')
    original_source=SOURCE.read_text(encoding='utf-8')
    oldsource='11. '+BEFORE
    if original_source.count(oldsource)!=1:
        raise RuntimeError('Historical editable source 1 Corinthians 13:11 not uniquely aligned')
    now=datetime.now(timezone.utc)
    stamp=now.strftime('%Y-%m-%d_%H%M%SUTC')
    created=now.replace(microsecond=0).isoformat().replace('+00:00','Z')
    archive_dir=ROOT/'rendered-documents-history'/stamp
    archive_dir.mkdir(parents=True,exist_ok=False)
    archive=archive_dir/EPUB.name
    shutil.copy2(EPUB,archive)
    if base.sha256(archive)!=OLD_SHA:
        raise RuntimeError('Previous EPUB archive checksum mismatch')
    with zipfile.ZipFile(EPUB,'r') as zin:
        infos=zin.infolist()
        original={i.filename:zin.read(i.filename) for i in infos}
        member=base.find_book_member(zin,'1-corinthians')
    old_xml=original[member].decode('utf-8')
    new_xml=rel.replace_one_verse(old_xml,'1-corinthians',13,11,BEFORE,AFTER)
    if new_xml==old_xml:
        raise RuntimeError('Specific 1 Corinthians 13:11 change was not applied')
    updated=dict(original)
    updated[member]=new_xml.encode('utf-8')
    fd,tmpname=tempfile.mkstemp(prefix='way-1cor13-adult-',suffix='.epub',dir=EPUB.parent)
    os.close(fd);tmp=Path(tmpname)
    try:
        with zipfile.ZipFile(tmp,'w') as zout:
            for info in infos:
                zout.writestr(info,updated[info.filename],compress_type=info.compress_type)
        base.validate_epub(tmp)
        shutil.move(tmp,EPUB)
    finally:
        tmp.unlink(missing_ok=True)
    changed_members=[name for name in original if original[name]!=updated[name]]
    if changed_members!=[member]:
        raise RuntimeError('EPUB changed members outside 1 Corinthians: '+repr(changed_members))
    after=verses()
    if len(after)!=31102 or after.get(KEY)!=AFTER:
        raise RuntimeError('Final inventory/text mismatch for 1 Corinthians 13:11')
    diffs={key for key in before if before[key]!=after[key]}
    if diffs!={KEY}:
        raise RuntimeError('Unexpected other Scripture changes: '+repr(diffs^({KEY})))
    postissues,postexceptions=rel.grammar.audit_epub(EPUB)
    if postissues or len(postexceptions)!=len(exceptions):
        raise RuntimeError('Released EPUB English article grammar regression')
    SOURCE.write_text(original_source.replace(oldsource,'11. '+AFTER,1),encoding='utf-8')
    released_sha=base.sha256(EPUB)
    registry=json.loads(REGISTRY.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256')!=OLD_SHA:
        raise RuntimeError('Original-name registry baseline mismatch')
    registry['canonicalEpubSha256']=released_sha
    REGISTRY.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fallback=base.build_fallback(EPUB,registry,released_sha,created)
    if (fallback.get('bookCount'),fallback.get('chapterCount'),fallback.get('verseSearchCount'))!=(66,1189,31102):
        raise RuntimeError('Regenerated mobile fallback coverage mismatch')
    reason=(
      'The Greek ὅτε γέγονα ἀνήρ (hote gegona anēr) contrasts the state '
      'of being a child with reaching adulthood. The speaker did not turn '
      'from nonhuman to human. In this rhetorical contrast, adult expresses '
      'the relevant maturity without assigning male gender to a generic '
      'translation or flattening the intended child/adult contrast. '
      'The 1st-person I remains unchanged; gender references to concrete '
      'male figures in other Bible verses are unaffected.'
    )
    report={
      'release':'1 Corinthians 13:11 adulthood wording',
      'releaseDate':'2026-10-13',
      'sourceGreek':'ὅτε γέγονα ἀνήρ',
      'changedVerseCount':1,'wholeBibleVerseCount':31102,
      'originalCanonicalEpubSha256':OLD_SHA,
      'releasedCanonicalEpubSha256':released_sha,
      'archivePath':archive.relative_to(ROOT).as_posix(),
      'changedEpubMembers':[member],
      'changes':[{'reference':'1 Corinthians 13:11','before':BEFORE,'after':AFTER,'rationale':reason}],
      'qa':{'only1Corinthians13_11Changed':True,'66Books':True,'1189Chapters':True,'31102Verses':True,
            'epubZipXmlLinks':'pass','grammar':'pass','sourceAlsoAligned':True},
      'canonicalMobileFallback':fallback,
      'printHandoff':{
        'action':'Include exact approved verse in next FULL physical print master typesetting and press-ready PDF',
        'status':'PENDING physical Word/PDF regeneration, proofreading, pagination and print proof signoff',
        'source':'Newest verified canonical EPUB (never historical PDF, EPUB older copy, or web JSON)',
        'reference':'1 Corinthians 13:11','before':BEFORE,'after':AFTER,
        'scope':'Exactly one verse for THIS release; physical working master must also reconcile all canonical changes since the last print edition.'
      }
    }
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    NOTE.write_text(
      '# 1 Corinthians 13:11 — become an adult (canonical + physical print handoff)\n\n'
      f'BEFORE: {BEFORE}\n\nAFTER: {AFTER}\n\n'
      f'RATIONALE: {reason}\n\n'
      f'Prior EPUB SHA-256: {OLD_SHA}\n'
      f'New EPUB SHA-256: {released_sha}\n'
      f'Prior archived EPUB: {archive.relative_to(ROOT).as_posix()}\n'
      'Whole-Bible diff: EXACTLY 1 approved verse / 31,102 records.\n'
      'EPUB ZIP/XML/links, 66 book/1,189 chapters, English article grammar: PASS.\n\n'
      'PRINT PRODUCTION TODO: Use this exact final verse in the next print working master, '
      'then regenerate/typeset and proofread full press-ready interior PDF. '
      'Do not claim any existing physical book or print master file changed simply '
      'because the canonical EPUB and Google print handoff were updated.\n',
      encoding='utf-8')
    base.append_once(rel.HISTORY_LOG,released_sha,
      f'- {stamp} — 1 Corinthians 13:11 person→adult (one verse), previous EPUB archive {archive.relative_to(ROOT).as_posix()}, new EPUB SHA-256 {released_sha}.')
    base.append_once(rel.REFRESH,'## 2026-10-13 1 Corinthians 13:11 adult',
      '## 2026-10-13 1 Corinthians 13:11 adult\n\n'
      'Single-verse source-faithful maturity contrast: "Now that I have become a person" '
      '→ "Now that I have become an adult". Exact whole-Bible diff: one verse; '
      f'new canonical EPUB SHA-256: {released_sha}. '
      'Physical print working master/PDF must be updated and proofed separately.')
    base.replace_sha_in_file(rel.ROOT_README,OLD_SHA,released_sha)
    base.replace_sha_in_file(rel.CURRENT_README,OLD_SHA,released_sha)
    print(json.dumps({'canonicalEpubSha256':released_sha,'changedVerseCount':len(diffs),
       'printStatus':'pending typeset/proof, Google handoff follows',
       'canonicalMobileFallback':fallback},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
