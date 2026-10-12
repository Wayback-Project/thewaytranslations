#!/usr/bin/env python3
"""Follow-up exact one verse: God and Sovereign title in 1 Timothy 6:15."""
from __future__ import annotations
import json,os,shutil,tempfile,zipfile
from datetime import datetime,timezone
from pathlib import Path
import release_2026_09_30_kingdom_residuals as rel

base=rel.base
ROOT,EPUB,REG=rel.ROOT,rel.EPUB,rel.REGISTRY
LEDGER=ROOT/'tools/local/2026-10-12-nt-divine-royal-followup-ledger.json'
REPORT=ROOT/'change-logs/reports/2026-10-12-nt-divine-royal-followup-release.json'
NOTE=ROOT/'editor-notes/consistency/2026-10-12-nt-divine-royal-followup-release.md'

def verses():return rel.collect_verses(EPUB,slugs=rel.ALL_SLUGS)

def main():
    led=json.loads(LEDGER.read_text(encoding='utf-8'))
    rows=led['rows']
    if len(rows)!=1 or rows[0]['reference']!='1 Timothy 6:15':
        raise RuntimeError('Follow-up ledger must contain 1 Timothy 6:15 only')
    row=rows[0]
    baseline=led['baselineCanonicalEpubSha256']
    if base.sha256(EPUB)!=baseline:raise RuntimeError('Canonical follow-up baseline mismatch')
    before=verses();key=('1-timothy',6,15)
    if len(before)!=31102 or before.get(key)!=row['before']:
        raise RuntimeError('Unexpected 1 Timothy baseline text or chapter verse inventory')
    issues,exceptions=rel.grammar.audit_epub(EPUB)
    if issues:raise RuntimeError('Grammar baseline issues')
    now=datetime.now(timezone.utc)
    stamp=now.strftime('%Y-%m-%d_%H%M%SUTC')
    generated=now.replace(microsecond=0).isoformat().replace('+00:00','Z')
    archive_dir=ROOT/'rendered-documents-history'/stamp
    archive_dir.mkdir(parents=True,exist_ok=False)
    archive=archive_dir/EPUB.name
    shutil.copy2(EPUB,archive)
    if base.sha256(archive)!=baseline:raise RuntimeError('Archive hash mismatch')
    with zipfile.ZipFile(EPUB) as zin:
        infos=zin.infolist()
        original={i.filename:zin.read(i.filename) for i in infos}
        member=base.find_book_member(zin,'1-timothy')
    modified=dict(original)
    old=original[member].decode('utf-8')
    new=rel.replace_one_verse(old,'1-timothy',6,15,row['before'],row['after'])
    if new==old:raise RuntimeError('Exact verse not changed')
    modified[member]=new.encode('utf-8')
    fd,tempname=tempfile.mkstemp(prefix='way-1tim-god-sovereign-',suffix='.epub',dir=EPUB.parent)
    os.close(fd);tmp=Path(tempname)
    try:
        with zipfile.ZipFile(tmp,'w') as zout:
            for info in infos:zout.writestr(info,modified[info.filename],compress_type=info.compress_type)
        base.validate_epub(tmp);shutil.move(tmp,EPUB)
    finally:tmp.unlink(missing_ok=True)
    assert [f for f in original if original[f]!=modified[f]]==[member]
    after=verses()
    changed={k for k in before if before[k]!=after[k]}
    if len(after)!=31102 or changed!={key} or after[key]!=row['after']:
        raise RuntimeError('Follow-up changed verses beyond approved 1 Timothy 6:15')
    issues2,exceptions2=rel.grammar.audit_epub(EPUB)
    if issues2 or len(exceptions2)!=len(exceptions):raise RuntimeError('Follow-up introduced grammar regressions')
    newsha=base.sha256(EPUB)
    registry=json.loads(REG.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256')!=baseline:
        raise RuntimeError('Canonical original-name registry baseline changed')
    registry['canonicalEpubSha256']=newsha
    REG.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fallback=base.build_fallback(EPUB,registry,newsha,generated)
    if (fallback.get('bookCount'),fallback.get('chapterCount'),fallback.get('verseSearchCount'))!=(66,1189,31102):
        raise RuntimeError('Mobile fallback coverage error')
    report={
      'release':'1 Timothy 6:15 God and Sovereign royal-title residual',
      'releaseDate':'2026-10-12','beforeEpubSha256':baseline,
      'releasedEpubSha256':newsha,'archivePath':archive.relative_to(ROOT).as_posix(),
      'changedVerseCount':1,'wholeBibleVerseCount':31102,'changedEpubMembers':[member],
      'changes':rows,'canonicalMobileFallback':fallback,
      'qa':{'only1Timothy6_15Changed':True,'epubZipXmlLinks':'pass',
            'books':66,'chapters':1189,'verses':31102,'grammar':'pass'},
      'context':'1 Timothy 6:13–16 distinguishes God who reveals the appearing from Messiah Yeshua, and applies the divine-only Ruler/King of kings title to God. Preserve historical kings and Yeshua title references elsewhere.',
      'batchTotal':'45 NT Father pronoun corrections + 1 related divine royal follow-up = 46 distinct verses in two sequential canonical releases.'
    }
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    NOTE.write_text(
      '# 1 Timothy 6:15 — God / Sovereign royal-title follow-up\n\n'
      'BEFORE: '+row['before']+'\n\nAFTER: '+row['after']+'\n\n'
      'Rationale: '+row['reason']+'\n\n'
      f'Prior canonical EPUB SHA-256: {baseline}\nReleased canonical EPUB SHA-256: {newsha}\n'
      f'Archived previous EPUB: {archive.relative_to(ROOT).as_posix()}\n'
      'Whole-Bible diff: exactly one verse / 31,102 records; structural QA passed.\n'
      'The previous 45-verse God/Father pronoun batch remains included. No changes to Yeshua pronouns or geopolitical kingdoms.\n',
      encoding='utf-8')
    base.append_once(rel.HISTORY_LOG,newsha,
      f'- {stamp} — God-referent 1 Timothy 6:15 “he/King” → “God/Sovereign”; prior EPUB archived at {archive.relative_to(ROOT).as_posix()}; new SHA-256 {newsha}.')
    base.append_once(rel.REFRESH,'## 2026-10-12 1 Timothy 6:15 God/Sovereign follow-up',
      '## 2026-10-12 1 Timothy 6:15 God/Sovereign follow-up\n\n'
      'After the 45-verse NT God/Father pronoun correction, exactly 1 Timothy 6:15 was reviewed and corrected: divine he → God and divine King of kings → Sovereign of sovereigns. '
      f'Canonical EPUB SHA-256 {newsha}. No other Scripture text changed.')
    base.replace_sha_in_file(rel.ROOT_README,baseline,newsha)
    base.replace_sha_in_file(rel.CURRENT_README,baseline,newsha)
    print(json.dumps({'release':'1 Timothy 6:15 God/Sovereign','newSha':newsha,
      'correctedVerses':1,'fallback':fallback},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
