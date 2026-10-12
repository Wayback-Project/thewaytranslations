#!/usr/bin/env python3
"""Release exactly the reviewed NT Father/God residual ledger, canonical EPUB first.
Any drift, unexpected verse change or coverage violation aborts the transaction."""
from __future__ import annotations
import json,os,shutil,tempfile,zipfile
from datetime import datetime,timezone
from collections import defaultdict
from pathlib import Path
import release_2026_09_30_kingdom_residuals as rel

base=rel.base
ROOT,EPUB,REGISTRY=rel.ROOT,rel.EPUB,rel.REGISTRY
LEDGER=ROOT/'tools/local/2026-10-12-nt-divine-referent-approved-ledger.json'
REPORT=ROOT/'change-logs/reports/2026-10-12-nt-divine-referent-release.json'
NOTE=ROOT/'editor-notes/consistency/2026-10-12-nt-divine-referent-release.md'

def all_verses(path):return rel.collect_verses(path,slugs=rel.ALL_SLUGS)

def main():
    led=json.loads(LEDGER.read_text(encoding='utf-8'))
    rows=led['rows']; baseline=led['baselineCanonicalEpubSha256']
    if len(rows)!=45 or led['changedVerseCount']!=45:raise RuntimeError('Exact ledger 45-row authority mismatch')
    if base.sha256(EPUB)!=baseline:raise RuntimeError('Canonical baseline SHA drift. STOP')
    before=all_verses(EPUB)
    if len(before)!=31102:raise RuntimeError('Baseline verse inventory mismatch')
    seen=set()
    for r in rows:
        key=(r['book'],r['chapter'],r['verse'])
        if key in seen:raise RuntimeError('Duplicate approved verse '+r['reference'])
        seen.add(key)
        if before.get(key)!=r['before']:raise RuntimeError('Approved before text drift '+r['reference'])
        if r['before']==r['after']:raise RuntimeError('No-op ledger entry '+r['reference'])
    pre_issues,pre_ex=rel.grammar.audit_epub(EPUB)
    if pre_issues:raise RuntimeError('Baseline grammar validation failed')

    now=datetime.now(timezone.utc)
    stamp=now.strftime('%Y-%m-%d_%H%M%SUTC')
    generated=now.replace(microsecond=0).isoformat().replace('+00:00','Z')
    archive_dir=ROOT/'rendered-documents-history'/stamp
    archive_dir.mkdir(parents=True,exist_ok=False)
    archive=archive_dir/EPUB.name
    shutil.copy2(EPUB,archive)
    if base.sha256(archive)!=baseline:raise RuntimeError('Old canonical archive hash mismatch')

    grouped=defaultdict(list)
    for r in rows:grouped[r['book']].append(r)
    with zipfile.ZipFile(EPUB) as zin:
        infos=zin.infolist()
        original={i.filename:zin.read(i.filename) for i in infos}
        members={book:base.find_book_member(zin,book) for book in grouped}
    updated=dict(original)
    for book,rs in grouped.items():
        member=members[book]
        s=updated[member].decode('utf-8')
        for r in rs:
            s=rel.replace_one_verse(s,book,int(r['chapter']),int(r['verse']),r['before'],r['after'])
        updated[member]=s.encode('utf-8')
    fd,tempname=tempfile.mkstemp(prefix='way-nt-god-pronouns-',suffix='.epub',dir=EPUB.parent)
    os.close(fd)
    tmp=Path(tempname)
    try:
        with zipfile.ZipFile(tmp,'w') as out:
            for i in infos:out.writestr(i,updated[i.filename],compress_type=i.compress_type)
        base.validate_epub(tmp)
        shutil.move(tmp,EPUB)
    finally:tmp.unlink(missing_ok=True)
    changed_members={name for name in original if original[name]!=updated[name]}
    if changed_members!=set(members.values()):raise RuntimeError('Unexpected EPUB modified members')

    new_sha=base.sha256(EPUB)
    after=all_verses(EPUB)
    if len(after)!=31102:raise RuntimeError('Released verse inventory changed')
    actual_changes={k for k in before if before[k]!=after[k]}
    if actual_changes!=seen:raise RuntimeError('Unapproved verse diffs: '+repr(sorted(actual_changes^seen)[:20]))
    for r in rows:
        if after[(r['book'],r['chapter'],r['verse'])]!=r['after']:
            raise RuntimeError('Post-release text mismatch '+r['reference'])
    issues,ex=rel.grammar.audit_epub(EPUB)
    if issues or len(ex)!=len(pre_ex):raise RuntimeError('Post-release grammatical validation failed')

    registry=json.loads(REGISTRY.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256')!=baseline:raise RuntimeError('Registry baseline mismatch')
    registry['canonicalEpubSha256']=new_sha
    REGISTRY.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fallback=base.build_fallback(EPUB,registry,new_sha,generated)
    if (fallback.get('bookCount'),fallback.get('chapterCount'),fallback.get('verseSearchCount'))!=(66,1189,31102):
        raise RuntimeError('Canonical mobile fallback inventory mismatch')

    report={
      'releaseDate':'2026-10-12',
      'release':'NT divine Father/God masculine-residual correction',
      'approvedScope':'45 unambiguous divine antecedent verses; preserve Yeshua and concrete male referents.',
      'priorEpubSha256':baseline,'releasedEpubSha256':new_sha,
      'archivePath':archive.relative_to(ROOT).as_posix(),
      'changedVerseCount':len(rows),'changedBooks':sorted(grouped),
      'changedEpubMembers':sorted(changed_members),
      'wholeBibleVerseCount':31102,
      'qa':{'epubZipXmlLinks':'pass','only45ApprovedVersesChanged':True,
        'NTBooksScanned':27,'books':66,'chapters':1189,'verses':31102,
        'articleGrammarRegression':'pass'},
      'source':'reviewed exact ledger tools/local/2026-10-12-nt-divine-referent-approved-ledger.json',
      'rows':rows,'canonicalMobileFallback':fallback,
      'protectedRule':'References to Yeshua and real male human subjects are not mechanically neutralized. Divine kingdom/reign is context-dependent; no blanket kingdom substitution.'
    }
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    summary=(
      '# New Testament divine Father/God masculine-pronoun residual release\n\n'
      f'**Approved one-release scope:** {len(rows)} exact Scripture verses in {len(grouped)} NT books.\n\n'
      '1 Peter 4:19: “entrust their souls to him” → “entrust their souls to God” (faithful Creator).\n\n'
      'The 27-book NT candidate audit found many masculine forms that refer to Yeshua or other men. '
      'Only unambiguous references to God/YHWH/Elohim/the Cosmic Parent were changed. '
      'Textual witnesses and context outrank mechanical matching. '
      'Using God versus Elohim versus Cosmic Parent follows the immediately established '
      'verse-level divine form; no global rename was authorized.\n\n'
      f'- Baseline canonical EPUB SHA-256: {baseline}\n'
      f'- New EPUB SHA-256: {new_sha}\n'
      f'- Prior binary archived: {archive.relative_to(ROOT).as_posix()}\n'
      f'- Whole Bible exact diff: {len(rows)} approved verses / 31,102 verses.\n'
      f'- EPUB member diff: {len(changed_members)} NT book XHTML members.\n'
      '- ZIP/CRC/mimetype, XML/anchors, coverage and grammatical QA passed.\n'
      '- Mobile canonical fallback feed generated solely from final EPUB.\n'
      '- This is NOT an assertion that every possible contextual divine pronoun has been '
      'conclusively eliminated: the audit includes ambiguous Yeshua/human citations '
      'requiring interpretation. See full candidate audit JSON.\n\n'
      '## Exact reviewed before/after changes\n\n'
      + '\n'.join(f'- **{r["reference"]}** BEFORE: {r["before"]} AFTER: {r["after"]}' for r in rows)
      + '\n'
    )
    NOTE.write_text(summary,encoding='utf-8')
    base.append_once(rel.HISTORY_LOG,new_sha,
      f'- {stamp} — NT Father/God pronoun consistency: {len(rows)} exact changed verses in {len(grouped)} NT books; archive {archive.relative_to(ROOT).as_posix()}; EPUB SHA-256 {new_sha}.')
    base.append_once(rel.REFRESH,'## 2026-10-12 NT divine-referent residual release',
      f'## 2026-10-12 NT divine-referent residual release\n\n'
      f'45 exact God/Father/YHWH/Cosmic Parent pronoun corrections; 1 Peter 4:19 among them. '
      f'Yeshua and other real male pronouns retained. New canonical EPUB SHA-256: {new_sha}. '
      'See editor-notes/consistency/2026-10-12-nt-divine-referent-release.md')
    base.replace_sha_in_file(rel.ROOT_README,baseline,new_sha)
    base.replace_sha_in_file(rel.CURRENT_README,baseline,new_sha)
    print(json.dumps({'releasedEpubSha256':new_sha,'changedVerses':len(actual_changes),
      'changedBooks':len(grouped),'canonicalFallback':fallback},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
