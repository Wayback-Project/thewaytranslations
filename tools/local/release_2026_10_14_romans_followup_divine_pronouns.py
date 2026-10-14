#!/usr/bin/env python3
"""Final context-reviewed Romans God-pronoun follow-up after the 23-book audit.
Four additional verses, no generic replacements; one older Hosea source alias
reconciled without altering canonical Hoshea in Scripture.
"""
from __future__ import annotations
import json,os,shutil,tempfile,zipfile
from datetime import datetime,timezone
from pathlib import Path
import release_2026_09_30_kingdom_residuals as rel
base=rel.base
ROOT,EPUB,REG=rel.ROOT,rel.EPUB,rel.REGISTRY
SRC=ROOT/'original-documents/rest_of_new_testament_restorative_translation.txt'
BASE='58ccf8deb2f65ecaa0b35ce7b35137221c95998cee23d6461d98e250c297b4fc'
REPORT=ROOT/'change-logs/reports/2026-10-14-romans-followup-4-divine-pronoun-release.json'
NOTE=ROOT/'editor-notes/consistency/2026-10-14-romans-followup-4-divine-pronoun-release.md'
EDITS=[
 (4,21,
  'and being fully assured that what he had promised, he was able also to perform.',
  'and being fully assured that what God had promised, God was able also to perform.',
  'In Romans 4:20–21 the promise was made by God; Avraham is the one assured of it.'),
 (9,18,
  'So then, he has mercy on whom he desires, and he hardens whom he desires.',
  'So then, God has mercy on whom God desires, and God hardens whom God desires.',
  'Romans 9:15–19 repeatedly names God as the one who has mercy or hardens.'),
 (15,10,
  'Again he says, "Rejoice, you Gentiles, with his people."',
  'Again Scripture says, "Rejoice, you Gentiles, with God’s people."',
  'Romans 15:9–11 quotation sequence: the scriptural citation has the Gentiles rejoicing with the people of God. Speaker of “Again” is Scripture, not an implicit male God.'),
 (15,11,
  'Again, "Praise the Master, all you Gentiles! Let all the peoples praise him."',
  'Again, "Praise the Master, all you Gentiles! Let all the peoples praise the Master."',
  'The Master in this cited invitation to praise is God, not Yeshua, so use the established title twice.'),
]
def verses():return rel.collect_verses(EPUB,slugs=rel.ALL_SLUGS)
def main():
    if base.sha256(EPUB)!=BASE:raise RuntimeError('Baseline EPUB changed; stop')
    before=verses()
    if len(before)!=31102:raise RuntimeError('Bible verse count mismatch')
    keys={('romans',c,v) for c,v,_,_,_ in EDITS}
    if len(keys)!=4 or any(before.get(('romans',c,v))!=old for c,v,old,_,_ in EDITS):
        raise RuntimeError('Approved Romans base text no longer matches')
    preissues,preexcept=rel.grammar.audit_epub(EPUB)
    if preissues:raise RuntimeError('Baseline grammar QA issues')
    originalsrc=SRC.read_text(encoding='utf-8')
    for c,v,old,new,reason in EDITS:
        if originalsrc.count(f'{v}. {old}')!=1:
            raise RuntimeError(f'Older editable source verse {c}:{v} mismatch; fail closed')
    # Reconcile the one previously flagged spelling difference in legacy source:
    # canonical version is "Hoshea"; historical NT TXT spells this name "Hosea".
    legacy='25. As he says also in Hosea,'
    if originalsrc.count(legacy)!=1:
        raise RuntimeError('Historical Romans 9:25 source spelling drift')
    now=datetime.now(timezone.utc)
    tag=now.strftime('%Y-%m-%d_%H%M%SUTC')
    time=now.replace(microsecond=0).isoformat().replace('+00:00','Z')
    ar=ROOT/'rendered-documents-history'/tag
    ar.mkdir(parents=True,exist_ok=False)
    archive=ar/EPUB.name
    shutil.copy2(EPUB,archive)
    if base.sha256(archive)!=BASE:raise RuntimeError('Archived EPUB mismatch')
    with zipfile.ZipFile(EPUB) as zin:
        members=zin.infolist()
        orig={i.filename:zin.read(i.filename) for i in members}
        member=base.find_book_member(zin,'romans')
    xml=orig[member].decode('utf-8')
    for c,v,old,new,reason in EDITS:
        xml=rel.replace_one_verse(xml,'romans',c,v,old,new)
    updated=dict(orig);updated[member]=xml.encode('utf-8')
    fd,name=tempfile.mkstemp(prefix='way-romans-followup-',suffix='.epub',dir=EPUB.parent)
    os.close(fd);tmp=Path(name)
    try:
        with zipfile.ZipFile(tmp,'w') as out:
            for info in members:out.writestr(info,updated[info.filename],compress_type=info.compress_type)
        base.validate_epub(tmp);shutil.move(tmp,EPUB)
    finally:tmp.unlink(missing_ok=True)
    if [x for x in orig if orig[x]!=updated[x]]!=[member]:
        raise RuntimeError('Other EPUB members unexpectedly changed')
    after=verses()
    diffs={k for k in before if before[k]!=after[k]}
    if len(after)!=31102 or diffs!=keys:
        raise RuntimeError('Whole-Bible diff must equal exactly 4 approved Romans verses')
    issues,exceptions=rel.grammar.audit_epub(EPUB)
    if issues or len(exceptions)!=len(preexcept):raise RuntimeError('Grammar regression')
    source=originalsrc
    for c,v,old,new,reason in EDITS:
        source=source.replace(f'{v}. {old}',f'{v}. {new}',1)
    source=source.replace(legacy,'25. As God says also in Hosea,',1)
    SRC.write_text(source,encoding='utf-8')
    digest=base.sha256(EPUB)
    reg=json.loads(REG.read_text(encoding='utf-8'))
    if reg.get('canonicalEpubSha256')!=BASE:raise RuntimeError('Registry input SHA mismatch')
    reg['canonicalEpubSha256']=digest
    REG.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fb=base.build_fallback(EPUB,reg,digest,time)
    if (fb.get('bookCount'),fb.get('chapterCount'),fb.get('verseSearchCount'))!=(66,1189,31102):
        raise RuntimeError('Mobile canonical fallback inventory')
    rows=[{'reference':f'Romans {c}:{v}','book':'Romans','chapter':c,'verse':v,
       'before':old,'after':new,'reason':reason} for c,v,old,new,reason in EDITS]
    report={'releaseDate':'2026-10-14',
      'release':'Romans four additional God referent and divine quotation corrections after full Acts–Revelation release',
      'baselineCanonicalEpubSha256':BASE,'releasedCanonicalEpubSha256':digest,
      'changedVerseCount':4,'changes':rows,'archivedPriorEpub':archive.relative_to(ROOT).as_posix(),
      'sourceHistoricalHoseaAliasReconciledInLegacyTXT':True,
      'qa':{'onlyApprovedFourRomansVersesChanged':True,'books':66,'chapters':1189,'verses':31102,'epubZipXmlLinks':'pass','grammar':'pass'},
      'canonicalMobileFallback':fb,
      'printStatus':'must amend October 12–14 before/after print correction register, working full Word Bible print master, typeset PDF and printer proofs separately'}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    NOTE.write_text(
     '# Four extra Romans divine referent corrections — 14 October 2026\n\n'
     +'\n\n'.join(f'### {r["reference"]}\nBEFORE: {r["before"]}\nAFTER: {r["after"]}\nREASON: {r["reason"]}' for r in rows)
     +f'\n\nPrevious SHA: {BASE}\nNew canonical SHA: {digest}\n'
     +'Three kinds of referents: (1) God as promiser/actor, (2) God as divine mercy sovereign, (3) God as owner of the people and object of praise. “Again he says” is changed to “Again Scripture says” rather than assigning a gender to the quotation introducer.\n'
     +'One earlier legacy-text Romans 9:25 “Hosea” alias was brought into line on the gender correction while retaining its historical spelling in that archived editable source; canonical EPUB has “Hoshea”.\n'
     +'Preserves the prior 66 Acts–Revelation corrections plus 1 Corinthians adult, Romans 11:34–36, Luke 2:52 and divine God/Father release. Physical Bible requires separate Word master and proof.\n',
     encoding='utf-8')
    base.append_once(rel.HISTORY_LOG,digest,
      f'- {tag} — Four extra Romans God-referent 4:21, 9:18, 15:10–11 exact changes; prior {archive.relative_to(ROOT).as_posix()}, SHA {digest}.')
    base.append_once(rel.REFRESH,'## 2026-10-14 Romans God referent four-verse followup',
      '## 2026-10-14 Romans God referent four-verse followup\n\n'
      f'Additional 4 contextual God/pronoun verses after 66-verse Acts–Revelation release, only 4 verse whole Bible diff. New canonical EPUB SHA {digest}. '
      'Older Word/PDF print master not automatically updated.')
    base.replace_sha_in_file(rel.ROOT_README,BASE,digest)
    base.replace_sha_in_file(rel.CURRENT_README,BASE,digest)
    print(json.dumps({'newCanonicalSha256':digest,'newCorrectedVerses':4,
        'canonicalFallback':fb},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
