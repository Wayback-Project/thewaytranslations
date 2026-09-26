#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import os
import re
import shutil
import tempfile
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import audit_evil_brokenness_unripeness_2026_09_25 as audit
import release_2026_09_14_ecclesiastes_inclusive_language_isaiah_harm as prior

base = prior.base
grammar = prior.grammar
replace_one_verse = prior.prev.replace_one_verse
collect_verses = prior.prev.collect_verses

ROOT = prior.ROOT
EPUB = prior.EPUB
REGISTRY = prior.REGISTRY
ROOT_README = prior.ROOT_README
CURRENT_README = prior.CURRENT_README
HISTORY_LOG = prior.HISTORY_LOG
REFRESH = prior.REFRESH

BASELINE = 'edd3182ff57b54471505189628b82238c85d2d9c8b4edbba14339695eac827cd'
LEDGER = ROOT / 'tools' / 'local' / 'proposed_evil_brokenness_unripeness_2026_09_25.tsv'
REPORT = ROOT / 'change-logs' / 'reports' / '2026-09-26-evil-to-brokenness-direct-release.json'
NOTE = ROOT / 'editor-notes' / 'consistency' / '2026-09-26-evil-to-brokenness-direct-release.md'
RELEASE_NAME = 'Direct evil → brokenness / broken terminology release'

BOOK_TO_SLUG = {book: slug for slug, book, _testament in audit.BOOKS}
SLUG_TO_BOOK = {slug: book for book, slug in BOOK_TO_SLUG.items()}
ALL_SLUGS = tuple(slug for slug, _book, _testament in audit.BOOKS)
EVIL_RE = re.compile(r'\bevil\b', re.I)
EVIL_FAMILY_RE = re.compile(r'\bevil[A-Za-z]*\b', re.I)


def parse_reference(ref: str):
    m = re.match(r'^(.*)\s+(\d+):(\d+)$', ref)
    if not m:
        raise RuntimeError(f'cannot parse reference: {ref}')
    book, ch, vs = m.group(1), int(m.group(2)), int(m.group(3))
    if book not in BOOK_TO_SLUG:
        raise RuntimeError(f'unknown book in reference: {ref}')
    return BOOK_TO_SLUG[book], ch, vs


def load_changes():
    rows=[]
    with LEDGER.open(encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            if r['change_evil'] != 'YES':
                raise RuntimeError(f"{r['reference']}: release ledger contains non-YES row")
            if r['reviewed'] != '☑' or r['approved'] != '☑':
                raise RuntimeError(f"{r['reference']}: release ledger is not reviewed+approved")
            slug,ch,vs=parse_reference(r['reference'])
            rows.append((slug,ch,vs,r['reference'],r['current_verse'],r['proposed_verse'],r['proposed_form']))
    refs=[x[:3] for x in rows]
    if len(rows) != 124 or len(set(refs)) != 124:
        raise RuntimeError(f'approved ledger shape mismatch rows={len(rows)} unique={len(set(refs))}')
    occurrence_counts=Counter()
    for _slug,_ch,_vs,ref,before,after,forms in rows:
        before_n=len(EVIL_RE.findall(before))
        after_n=len(EVIL_RE.findall(after))
        if before_n < 1 or after_n != 0:
            raise RuntimeError(f'{ref}: lexical evil inventory mismatch before={before_n} after={after_n}')
        for form in [x.strip().lower() for x in forms.split('|')]:
            if form not in {'broken','brokenness'}:
                raise RuntimeError(f'{ref}: forbidden final form {form!r}')
            occurrence_counts[form]+=1
    if occurrence_counts != Counter({'brokenness':109,'broken':19}):
        raise RuntimeError(f'final-form count mismatch: {dict(occurrence_counts)}')
    return rows, occurrence_counts


CHANGES, OCCURRENCE_COUNTS = load_changes()
CHANGED_SLUGS = tuple(sorted({x[0] for x in CHANGES}))


def collect(path: Path, *, all_bible=False):
    return collect_verses(path, slugs=ALL_SLUGS if all_bible else CHANGED_SLUGS)


def validate_exact(path: Path, which: str):
    verse_map=collect(path)
    errors=[]
    for slug,ch,vs,ref,before,after,_forms in CHANGES:
        expected=before if which=='before' else after
        actual=verse_map.get((slug,ch,vs))
        if actual != expected:
            errors.append({'reference':ref,'expected':expected,'actual':actual})
    if errors:
        raise RuntimeError(f'{which} exact inventory mismatch ({len(errors)}): '+json.dumps(errors[:20],ensure_ascii=False,indent=2))


def rewrite_epub():
    by_slug=defaultdict(list)
    for row in CHANGES:
        by_slug[row[0]].append(row)
    with zipfile.ZipFile(EPUB,'r') as zin:
        infos=zin.infolist()
        original={i.filename:zin.read(i.filename) for i in infos}
    edited=dict(original)
    expected_members=[]
    with zipfile.ZipFile(EPUB,'r') as z:
        for slug,rows in by_slug.items():
            member=base.find_book_member(z,slug)
            expected_members.append(member)
            text=edited[member].decode('utf-8')
            for _slug,ch,vs,ref,before,after,_forms in rows:
                text=replace_one_verse(text,slug,ch,vs,before,after)
            edited[member]=text.encode('utf-8')
    fd,tmpname=tempfile.mkstemp(prefix='the-way-evil-direct-',suffix='.epub',dir=EPUB.parent)
    os.close(fd)
    tmp=Path(tmpname)
    try:
        with zipfile.ZipFile(tmp,'w') as zout:
            for info in infos:
                zout.writestr(info,edited[info.filename],compress_type=info.compress_type)
        base.validate_epub(tmp)
        shutil.move(tmp,EPUB)
    finally:
        if tmp.exists(): tmp.unlink()
    changed=sorted(name for name in original if original[name] != edited[name])
    if changed != sorted(expected_members):
        raise RuntimeError(f'changed EPUB members mismatch expected={sorted(expected_members)} actual={changed}')
    return changed


def language_qa(verse_map):
    errors=[]
    for (slug,ch,vs),text in verse_map.items():
        ref=f'{SLUG_TO_BOOK[slug]} {ch}:{vs}'
        checks=[
            ('standalone-evil', EVIL_RE.search(text)),
            ('brokenness-as-adjective', re.search(r'\bbrokenness\s+(?:plans?|ways?|actions?|doings?|abominations?|devices?)\b',text,re.I)),
            ('indefinite-pronoun-brokenness', re.search(r'\b(?:anything|something|nothing|everything)\s+brokenness\b',text,re.I)),
            ('copular-brokenness', re.search(r'\b(?:is|are|was|were|be|been|being)\s+brokenness\b',text,re.I)),
            ('bad-article', re.search(r'\b(?:an\s+broken|a\s+brokenness)\b',text,re.I)),
            ('sentence-start-lowercase', re.search(r'(^|[.!?][\"”\'’)]*\s+)(?:broken|brokenness)\b',text)),
            ('double-space', re.search(r' {2,}',text)),
            ('space-before-punctuation', re.search(r'\s+[,.!?;:]',text)),
            ('subject-verb-agreement', re.search(r'\bthey\s+(?:delights|is|was|has|does)\b',text,re.I)),
        ]
        for name,match in checks:
            if match: errors.append({'reference':ref,'issue':name,'text':text})
    if errors:
        raise RuntimeError('post-release language QA failed: '+json.dumps(errors[:30],ensure_ascii=False,indent=2))


def main():
    actual=base.sha256(EPUB)
    if actual != BASELINE:
        raise SystemExit(f'baseline SHA mismatch expected={BASELINE} got={actual}')

    pre_articles, pre_exceptions=grammar.audit_epub(EPUB)
    if pre_articles:
        raise RuntimeError('pre-release article audit not clean: '+json.dumps(pre_articles[:30],ensure_ascii=False,indent=2))
    validate_exact(EPUB,'before')

    before_all=collect(EPUB,all_bible=True)
    if len(before_all) != 31102:
        raise RuntimeError(f'whole-Bible verse inventory before release is {len(before_all)}, expected 31102')
    if sum(bool(EVIL_RE.search(t)) for t in before_all.values()) != 124:
        raise RuntimeError('baseline standalone evil verse count is not 124')

    now=datetime.now(timezone.utc)
    stamp=now.strftime('%Y-%m-%d_%H%MUTC')
    generated=now.replace(microsecond=0).isoformat().replace('+00:00','Z')
    archive_dir=ROOT/'rendered-documents-history'/stamp
    archive_dir.mkdir(parents=True,exist_ok=False)
    archive=archive_dir/EPUB.name
    shutil.copy2(EPUB,archive)
    if base.sha256(archive) != BASELINE:
        raise RuntimeError('archive SHA mismatch')

    changed_members=rewrite_epub()
    newsha=base.sha256(EPUB)
    if newsha == BASELINE:
        raise RuntimeError('EPUB SHA did not change')
    validate_exact(EPUB,'after')

    post_articles, post_exceptions=grammar.audit_epub(EPUB)
    if post_articles:
        raise RuntimeError('article inconsistencies introduced: '+json.dumps(post_articles[:30],ensure_ascii=False,indent=2))
    if len(post_exceptions) != len(pre_exceptions):
        raise RuntimeError(f'pronunciation article exception inventory changed before={len(pre_exceptions)} after={len(post_exceptions)}')

    after_all=collect(EPUB,all_bible=True)
    if len(after_all) != 31102:
        raise RuntimeError(f'whole-Bible verse inventory after release is {len(after_all)}, expected 31102')
    language_qa(after_all)

    evil_family=[]
    for (slug,ch,vs),text in after_all.items():
        forms=[m.group(0) for m in EVIL_FAMILY_RE.finditer(text)]
        if forms:
            evil_family.append((f'{SLUG_TO_BOOK[slug]} {ch}:{vs}',forms,text))
    if len(evil_family) != 2 or any([f.lower() for f in forms] != ['evilmerodach'] for _ref,forms,_text in evil_family):
        raise RuntimeError('post-release evil-family residuals are not exactly the two Evilmerodach proper-name verses: '+json.dumps(evil_family[:20],ensure_ascii=False,indent=2))

    registry=json.loads(REGISTRY.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256') != BASELINE:
        raise RuntimeError('registry baseline SHA mismatch')
    registry['canonicalEpubSha256']=newsha
    REGISTRY.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fallback=base.build_fallback(EPUB,registry,newsha,generated)
    for key,expected in [('bookCount',66),('chapterCount',1189),('verseSearchCount',31102)]:
        if key in fallback and fallback[key] != expected:
            raise RuntimeError(f'fallback {key} mismatch {fallback[key]} != {expected}')

    report_rows=[]
    for slug,ch,vs,ref,before,after,forms in CHANGES:
        report_rows.append({'reference':ref,'book':SLUG_TO_BOOK[slug],'chapter':ch,'verse':vs,'finalForms':[x.strip() for x in forms.split('|')],'before':before,'after':after})

    report={
      'release':RELEASE_NAME,
      'prior_epub_sha256':BASELINE,
      'released_epub_sha256':newsha,
      'archive_path':archive.relative_to(ROOT).as_posix(),
      'changed_verse_count':len(report_rows),
      'lexical_evil_occurrence_count':sum(OCCURRENCE_COUNTS.values()),
      'replacement_occurrence_counts':dict(OCCURRENCE_COUNTS),
      'proper_name_no_change_rows':['2 Kings 25:27','Jeremiah 52:31'],
      'changed_members':changed_members,
      'whole_bible_verse_count':len(after_all),
      'standalone_evil_residual_count':0,
      'evil_family_residuals':[{'reference':ref,'forms':forms} for ref,forms,_text in evil_family],
      'article_mismatch_count':len(post_articles),
      'mobileFallback':fallback,
      'changes':report_rows,
      'method':'Exact finite 124-verse release from the approved 2026-09-26 ledger. Only standalone lexical evil is replaced: brokenness in noun/abstract slots and broken in adjective/predicate/substantive-adjective slots. No contextual phrase rewrites. The only surrounding-token changes are Ezekiel 38:10 an→a, Malachi 2:17 they delights→they delight, and sentence-start capitalization in Psalms 5:4 and 34:21.',
    }
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    NOTE.parent.mkdir(parents=True,exist_ok=True)
    NOTE.write_text(f'''# {RELEASE_NAME}\n\n**Canonical release completed from the approved finite ledger.**\n\n## Scope\n\n- 124 exact verse-level Scripture edits.\n- 128 standalone lexical `evil` occurrences replaced: 109 → `brokenness`; 19 → `broken`.\n- 2 `Evilmerodach` proper-name rows remain unchanged.\n- No contextual phrase rewrites.\n- Grammar-only adjacent repairs: Ezekiel 38:10 `an` → `a`; Malachi 2:17 `they delights` → `they delight`; Psalm 5:4 and Psalm 34:21 sentence-start capitalization.\n\n## Canonical QA\n\n- Previous EPUB SHA-256: `{BASELINE}`\n- Released EPUB SHA-256: `{newsha}`\n- Previous EPUB archived at `{archive.relative_to(ROOT).as_posix()}`\n- Exact 124-row before/after inventory: pass\n- Whole Bible: 31,102 / 31,102 verses\n- Standalone lexical `evil` residuals: 0\n- Remaining `evil…` family matches: exactly 2 `Evilmerodach` proper-name verses\n- ZIP CRC, EPUB mimetype/XML/internal links: pass\n- English article audit: 0 actionable mismatches\n- Brokenness noun-vs-adjective guards: pass\n- Sentence capitalization and spacing guards: pass\n- Canonical mobile fallback regenerated from the finished EPUB\n\nThe website/e-reader and native mobile app must be regenerated from this exact finished canonical release; no downstream Scripture hand-editing.\n''',encoding='utf-8')

    base.append_once(HISTORY_LOG,newsha,f'- **{stamp}** — {RELEASE_NAME}: 124 exact verses / 128 lexical occurrences (109 brokenness, 19 broken). Prior EPUB archived at `{archive.relative_to(ROOT).as_posix()}`; new SHA-256 `{newsha}`.')
    base.append_once(REFRESH,'## 2026-09-26 Direct evil → brokenness / broken release',f'''## 2026-09-26 Direct evil → brokenness / broken release\n\nFinite 124-verse canonical release from the approved whole-Bible terminology review. Only the lexical word `evil` was changed: noun/abstract slots → `brokenness`; adjective/predicate/substantive-adjective slots → `broken`. No contextual phrase rewrites. Canonical SHA-256: `{newsha}`. See `../editor-notes/consistency/2026-09-26-evil-to-brokenness-direct-release.md` and `../change-logs/reports/2026-09-26-evil-to-brokenness-direct-release.json`.''')
    base.replace_sha_in_file(ROOT_README,BASELINE,newsha)
    base.replace_sha_in_file(CURRENT_README,BASELINE,newsha)

    print(json.dumps({'release':RELEASE_NAME,'releasedEpubSha256':newsha,'changedVerseCount':len(report_rows),'replacementOccurrenceCounts':dict(OCCURRENCE_COUNTS),'wholeBibleVerseCount':len(after_all),'standaloneEvilResidualCount':0,'evilFamilyResidualCount':len(evil_family),'articleMismatches':len(post_articles),'fallbackContentSha256':fallback.get('contentSha256'),'fallbackBytes':fallback.get('contentBytes'),'changedMembers':changed_members},indent=2))

if __name__=='__main__':
    main()
