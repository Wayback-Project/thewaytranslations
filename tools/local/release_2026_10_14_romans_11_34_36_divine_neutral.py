#!/usr/bin/env python3
"""Editorially approved Romans 11:34–36 God referents, canonical-first.
Exactly three verses. For 11:35 the second historical English "him"
is a HUMAN possible giver, not another pronoun for God.
"""
from __future__ import annotations
import json,os,shutil,tempfile,zipfile
from datetime import datetime,timezone
from pathlib import Path
import release_2026_09_30_kingdom_residuals as rel

base=rel.base
ROOT,EPUB,REGISTRY=rel.ROOT,rel.EPUB,rel.REGISTRY
SOURCE=ROOT/'original-documents/rest_of_new_testament_restorative_translation.txt'
BASELINE='9a8793547680e7b8c1dc84ad5fb416ca2df484f1d0b5716a8c48ea09cfdaf87a'
REPORT=ROOT/'change-logs/reports/2026-10-14-romans-11-34-36-god-referents-release.json'
NOTE=ROOT/'editor-notes/consistency/2026-10-14-romans-11-34-36-god-referents-release.md'
EDITS=[
  (34,
   '"For who has known the mind of the Master? Or who has been his counselor?"',
   '"For who has known the mind of the Master? Or who has been the Master\'s counselor?"',
   'Romans 11:33–34 invokes God and echoes Isaiah 40:13. Here the Master is God; replacing the possessive his with the Master’s keeps the local established divine title and removes a male default.'),
  (35,
   '"Or who has first given to him, and it will be repaid to him again?"',
   '"Or who has given to God first, so that God must repay them?"',
   'This quotation/allusion to Job 41:11 rhetorically denies that God is indebted to any creature. The FIRST him denotes God; the SECOND him means the hypothetical human giver who could be repaid. God identifies the divine actor, and singular them refers to the human without defaulting to male. Both Greek pronouns are dative forms, but referents differ.'),
  (36,
   'For of him, and through him, and to him, are all things. To him be the glory for ever! Amen.',
   'For all things are from God, through God, and to God. To God be glory forever! Amen.',
   'In the doxology all the he/him references mean the one God of Romans 11:33–36. Direct divine naming preserves the from/through/to parallelism without assigning human maleness to God.')
]

def verses():
    return rel.collect_verses(EPUB,slugs=rel.ALL_SLUGS)

def main():
    if base.sha256(EPUB)!=BASELINE:
        raise RuntimeError('Canonical version advanced; abort until edits reviewed against latest')
    before=verses()
    keys={('romans',11,v) for v,_,_,_ in EDITS}
    if len(before)!=31102 or any(before.get(('romans',11,v))!=old for v,old,_,_ in EDITS):
        raise RuntimeError('Baseline Romans 11 or whole Bible inventory mismatch')
    preissues,preexceptions=rel.grammar.audit_epub(EPUB)
    if preissues:raise RuntimeError('Pre-release English grammar validation failed')
    source=SOURCE.read_text(encoding='utf-8')
    for v,old,new,_ in EDITS:
        if source.count(f'{v}. {old}')!=1:
            raise RuntimeError(f'Editable source Romans 11:{v} mismatch')
    stamp=datetime.now(timezone.utc)
    tag=stamp.strftime('%Y-%m-%d_%H%M%SUTC')
    at=stamp.replace(microsecond=0).isoformat().replace('+00:00','Z')
    archive_dir=ROOT/'rendered-documents-history'/tag
    archive_dir.mkdir(parents=True,exist_ok=False)
    archive=archive_dir/EPUB.name
    shutil.copy2(EPUB,archive)
    if base.sha256(archive)!=BASELINE:raise RuntimeError('Previous EPUB archive mismatch')
    with zipfile.ZipFile(EPUB) as zin:
        infos=zin.infolist()
        orig={i.filename:zin.read(i.filename) for i in infos}
        member=base.find_book_member(zin,'romans')
    xml=orig[member].decode('utf-8')
    for v,old,new,_ in EDITS:
        amended=rel.replace_one_verse(xml,'romans',11,v,old,new)
        if amended==xml:raise RuntimeError(f'No exact EPUB replacement for Romans 11:{v}')
        xml=amended
    modified=dict(orig)
    modified[member]=xml.encode('utf-8')
    fd,name=tempfile.mkstemp(prefix='way-romans-11-divine-',suffix='.epub',dir=EPUB.parent)
    os.close(fd);tmp=Path(name)
    try:
        with zipfile.ZipFile(tmp,'w') as out:
            for info in infos:
                out.writestr(info,modified[info.filename],compress_type=info.compress_type)
        base.validate_epub(tmp)
        shutil.move(tmp,EPUB)
    finally:tmp.unlink(missing_ok=True)
    if [name for name in orig if orig[name]!=modified[name]]!=[member]:
        raise RuntimeError('Unexpected other EPUB members changed')
    after=verses()
    changed={key for key in before if before[key]!=after[key]}
    if len(after)!=31102 or changed!=keys or any(after[('romans',11,v)]!=new for v,old,new,_ in EDITS):
        raise RuntimeError('Whole Bible diff not exactly Romans 11:34–36')
    postissues,postexceptions=rel.grammar.audit_epub(EPUB)
    if postissues or len(postexceptions)!=len(preexceptions):
        raise RuntimeError('Post-release grammar validation regression')
    for v,old,new,_ in EDITS:
        source=source.replace(f'{v}. {old}',f'{v}. {new}',1)
    SOURCE.write_text(source,encoding='utf-8')
    digest=base.sha256(EPUB)
    registry=json.loads(REGISTRY.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256')!=BASELINE:
        raise RuntimeError('Canonical registry checksum differs from input EPUB')
    registry['canonicalEpubSha256']=digest
    REGISTRY.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fallback=base.build_fallback(EPUB,registry,digest,at)
    if (fallback.get('bookCount'),fallback.get('chapterCount'),fallback.get('verseSearchCount'))!=(66,1189,31102):
        raise RuntimeError('Mobile fallback coverage mismatch')
    rows=[{'reference':f'Romans 11:{v}','chapter':11,'verse':v,'before':old,'after':new,'rationale':reason}
          for v,old,new,reason in EDITS]
    report={'releaseDate':'2026-10-14','release':'Romans 11:34–36 divine pronoun / generic human pronoun',
       'priorCanonicalEpubSha256':BASELINE,'releasedCanonicalEpubSha256':digest,
       'changedVerseCount':3,'wholeBibleVerseCount':31102,'changes':rows,
       'changedEpubMembers':[member],'archivePath':archive.relative_to(ROOT).as_posix(),
       'originalNTSourceAlsoAligned':True,'canonicalMobileFallback':fallback,
       'qa':{'onlyRomans11_34to36Changed':True,'epubZipXmlLinks':'pass','books':66,'chapters':1189,
              'verses':31102,'grammar':'pass'},
       'historicalPrintStatus':'handoff updated separately; print Word/PDF typesetting and proof not yet completed'}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    note=['# Romans 11:34–36 — divine pronouns / inclusive human reference (14 Oct 2026)',
          '', '### Source/translation decision',
          'Romans 11:33 explicitly names God. Verse 34 echoes Isaiah 40:13; verse 35 alludes to Job 41:11; verse 36 is a doxology to God.',
          'The LAST “him” in verse 35 describes the possible HUMAN recipient of repayment, NOT God: use generic “them”.',
          'Retain the established “Master” title in verse 34 and use the proper divine title God in verse 35–36,',
          'consistent with the passage. This is NOT a global policy to neutralize Yeshua.',
          '', '### Exact changes']
    for row in rows:
        note+=['',f"**{row['reference']}**",f"BEFORE: {row['before']}",f"AFTER: {row['after']}",
               f"REASON: {row['rationale']}"]
    note+=['',f'Previous canonical EPUB SHA-256: {BASELINE}',
           f'New canonical EPUB SHA-256: {digest}',
           f'Prior EPUB archived: {archive.relative_to(ROOT).as_posix()}',
           'Only 3 Bible verses changed; 66 books, 1,189 chapters, 31,102 verses; EPUB/grammar validated.',
           'PRINT TODO: Update current Word print master and regenerate/paginate/proof its interior PDF; do NOT claim already printed volumes updated.',
           'Previously corrected 1 Corinthians 13:11 adult, Luke 2:52 the people, 1 Peter 4:19 God and 46 NT divine cases retained.']
    NOTE.write_text('\n'.join(note)+'\n',encoding='utf-8')
    base.append_once(rel.HISTORY_LOG,digest,
      f'- {tag} — Romans 11:34–36 exact 3-verse God-referent release, old EPUB {archive.relative_to(ROOT).as_posix()}; new SHA-256 {digest}.')
    base.append_once(rel.REFRESH,'## 2026-10-14 Romans 11:34–36 God referents',
      '## 2026-10-14 Romans 11:34–36 God referents\n\n'
      'Correct exactly three verses. Romans 11:35 first him is God, second him is hypothetical human giver (render “them”); '
      f'new canonical EPUB SHA-256 {digest}. Physical print working Word master and PDF require separate reflow/proof.')
    base.replace_sha_in_file(rel.ROOT_README,BASELINE,digest)
    base.replace_sha_in_file(rel.CURRENT_README,BASELINE,digest)
    print(json.dumps({'releasedEpubSha256':digest,'changedVerses':len(changed),
       'canonicalFallback':fallback},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
