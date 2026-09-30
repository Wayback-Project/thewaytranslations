#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import release_2026_09_30_kingdom_residuals as prev

base = prev.base
grammar = prev.grammar
replace_one_verse = prev.replace_one_verse
collect_verses = prev.collect_verses
ROOT = prev.ROOT
EPUB = prev.EPUB
REGISTRY = prev.REGISTRY
ROOT_README = prev.ROOT_README
CURRENT_README = prev.CURRENT_README
HISTORY_LOG = prev.HISTORY_LOG
REFRESH = prev.REFRESH
ALL_SLUGS = prev.ALL_SLUGS
SLUG_TO_BOOK = prev.SLUG_TO_BOOK

BASELINE = '91b1daa6b2f796ebf4fd3c149cf4fabc8faabba796f0063bdb6ab8e0565492d7'
RELEASE_NAME = 'Quotation nesting spacing normalization'
GENESIS_SOURCE = ROOT / 'original-documents/genesis_restorative_translation.txt'
REPORT = ROOT / 'change-logs/reports/2026-09-30-quotation-spacing-release.json'
AUDIT = ROOT / 'change-logs/reports/2026-09-30-quotation-punctuation-audit.md'
NOTE = ROOT / 'editor-notes/consistency/2026-09-30-quotation-spacing-release.md'

# These are the exact verse references surfaced by the whole-Bible audit. The
# typography fix is intentionally narrow: remove whitespace only when it sits
# between nested curly quotation marks. Do not delete quotation levels and do
# not globally restyle straight/curly quotes.
SPACED_CLOSER_KEYS = {
    (3, 3), (20, 13), (22, 18), (26, 9), (31, 13), (32, 5), (32, 12),
    (32, 18), (32, 20), (37, 17), (38, 22), (42, 34), (43, 5), (44, 5),
    (45, 11), (48, 20), (50, 5), (50, 17),
}
SPACED_OPEN_KEYS = {(22, 16)}
CHANGE_KEYS = SPACED_CLOSER_KEYS | SPACED_OPEN_KEYS

# Review-only regex candidates that were initially overcalled as malformed.
# Context review confirmed that these endings close real nested speech levels;
# they are therefore explicit no-change checkpoints for this release.
REVIEWED_NO_CHANGE = [
    'Exodus 7:18', 'Exodus 8:23', 'Exodus 9:4', 'Exodus 9:19',
    'Isaiah 36:10', 'Isaiah 37:7', 'Isaiah 38:8', 'Ezekiel 29:16',
    'Zechariah 1:17', 'Zechariah 6:15', 'Matthew 13:30', 'Matthew 26:18',
]

CLOSE_SPACE_RE = re.compile(r'([”’])\s+(?=[”’])')
OPEN_SPACE_RE = re.compile(r'([“‘])\s+(?=[“‘])')


def collect(path: Path):
    return collect_verses(path, slugs=ALL_SLUGS)


def normalize_nested_spacing(text: str, key: tuple[int, int]) -> str:
    out = text
    if key in SPACED_CLOSER_KEYS:
        out = CLOSE_SPACE_RE.sub(r'\1', out)
    if key in SPACED_OPEN_KEYS:
        out = OPEN_SPACE_RE.sub(r'\1', out)
    return out


def quote_space_refs(verses: dict[tuple[str, int, int], str]):
    closers = set()
    openers = set()
    for (slug, chapter, verse), text in verses.items():
        if CLOSE_SPACE_RE.search(text):
            closers.add((slug, chapter, verse))
        if OPEN_SPACE_RE.search(text):
            openers.add((slug, chapter, verse))
    return closers, openers


def build_changes(before: dict[tuple[str, int, int], str]):
    changes = []
    for chapter, verse in sorted(CHANGE_KEYS):
        key = ('genesis', chapter, verse)
        current = before.get(key)
        if current is None:
            raise RuntimeError(f'missing Genesis {chapter}:{verse}')
        final = normalize_nested_spacing(current, (chapter, verse))
        if final == current:
            raise RuntimeError(f'approved spacing transform made no change at Genesis {chapter}:{verse}')
        # Safety contract: after normalizing both quote-boundary whitespace
        # forms, Current and Final must be identical. This prevents a lexical
        # change from entering a typography-only release.
        normalized_current = OPEN_SPACE_RE.sub(r'\1', CLOSE_SPACE_RE.sub(r'\1', current))
        normalized_final = OPEN_SPACE_RE.sub(r'\1', CLOSE_SPACE_RE.sub(r'\1', final))
        if normalized_current != normalized_final:
            raise RuntimeError(f'non-typographic change detected at Genesis {chapter}:{verse}')
        changes.append({
            'slug': 'genesis',
            'chapter': chapter,
            'verse': verse,
            'reference': f'Genesis {chapter}:{verse}',
            'before': current,
            'after': final,
        })
    return changes


def rewrite_genesis_source(changes):
    by_key = {(row['chapter'], row['verse']): row for row in changes}
    lines = GENESIS_SOURCE.read_text(encoding='utf-8').splitlines(keepends=True)
    chapter = None
    changed = []
    out = []
    for line in lines:
        stripped = line.rstrip('\r\n')
        ending = line[len(stripped):]
        heading = re.fullmatch(r'Genesis\s+(\d+)', stripped)
        if heading:
            chapter = int(heading.group(1))
            out.append(line)
            continue
        verse_match = re.match(r'^(\d+)\.\s(.*)$', stripped)
        if chapter is not None and verse_match:
            verse = int(verse_match.group(1))
            row = by_key.get((chapter, verse))
            if row:
                actual = verse_match.group(2)
                if actual != row['before']:
                    raise RuntimeError(
                        f'editable-source mismatch {row["reference"]}: expected={row["before"]!r} actual={actual!r}'
                    )
                out.append(f'{verse}. {row["after"]}{ending}')
                changed.append((chapter, verse))
                continue
        out.append(line)
    if set(changed) != set(by_key) or len(changed) != len(by_key):
        raise RuntimeError(f'editable-source change set mismatch: {changed}')
    GENESIS_SOURCE.write_text(''.join(out), encoding='utf-8')


def rewrite_epub(changes):
    with zipfile.ZipFile(EPUB, 'r') as zin:
        infos = zin.infolist()
        original = {info.filename: zin.read(info.filename) for info in infos}
        member = base.find_book_member(zin, 'genesis')
    edited = dict(original)
    text = edited[member].decode('utf-8')
    for row in changes:
        text = replace_one_verse(
            text,
            row['slug'], row['chapter'], row['verse'], row['before'], row['after']
        )
    edited[member] = text.encode('utf-8')
    fd, tmpname = tempfile.mkstemp(prefix='the-way-quotation-spacing-', suffix='.epub', dir=EPUB.parent)
    os.close(fd)
    tmp = Path(tmpname)
    try:
        with zipfile.ZipFile(tmp, 'w') as zout:
            for info in infos:
                zout.writestr(info, edited[info.filename], compress_type=info.compress_type)
        base.validate_epub(tmp)
        shutil.move(tmp, EPUB)
    finally:
        if tmp.exists():
            tmp.unlink()
    changed_members = [name for name in original if original[name] != edited[name]]
    if changed_members != [member]:
        raise RuntimeError(f'EPUB member diff is not Genesis-only: {changed_members}')
    return member


def write_audit(changes, newsha, generated):
    rows = '\n'.join(
        f"- **{row['reference']}** — `{row['before']}` → `{row['after']}`"
        for row in changes
    )
    retained = ', '.join(REVIEWED_NO_CHANGE)
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT.write_text(
        f'''# 2026-09-30 quotation / punctuation integrity audit\n\n'''
        f'''**Status: RELEASED — finite typography-only correction complete.**\n\n'''
        f'''## Decision\n\n'''
        f'''The screenshot-visible Genesis 20:13 ending contained three structurally required closing quotation marks. The defect was the whitespace between nested marks, not the number of quotation levels. The same rule was reviewed across the 31,102-verse corpus.\n\n'''
        f'''- Changed verses: **19**, all in Genesis.\n'''
        f'''- 18 verses: removed whitespace between nested curly closing quotation marks.\n'''
        f'''- Genesis 22:16: removed one whitespace boundary between nested curly opening quotation marks.\n'''
        f'''- Scripture wording changed: **0 words**.\n'''
        f'''- Quote levels deleted: **0**.\n'''
        f'''- Global straight/curly quote restyling: **not performed**.\n'''
        f'''- Canonical EPUB after release: `{newsha}`.\n'''
        f'''- Generated at: `{generated}`.\n\n'''
        f'''## Exact released rows\n\n{rows}\n\n'''
        f'''## Reviewed no-change dense-quote candidates\n\n'''
        f'''The earlier regex candidate bucket was deliberately reclassified after context review. These are valid nested speech closures/openings and remain unchanged: {retained}.\n\n'''
        f'''Examples include Exodus 7:16–18 / 8:20–23 (YHWH → Moses → Pharaoh), Isaiah 37:6–7 (Isaiah → Hezekiah's servants → YHWH), Zechariah 1:14–17, and Matthew 26:18 (Yeshua → disciples → householder → Teacher). Three adjacent marks can therefore be correct Bible typography when three quotation levels close at the same point.\n\n'''
        f'''## House-style boundary\n\n'''
        f'''The corpus contains both straight-quote and curly-quote book traditions. That variation is not treated as corruption in this release. A whole-Bible style conversion would be a separate editorial project because it can alter apostrophes and nested-dialogue semantics.\n\n'''
        f'''## QA gate\n\n'''
        f'''- Canonical inventory: 66 books / 1,189 chapters / 31,102 verse-search records.\n'''
        f'''- Whole-Bible text diff: exactly the 19 approved Genesis verses.\n'''
        f'''- Remaining curly nested-quote whitespace hits under the release rules: 0.\n'''
        f'''- EPUB ZIP/XML/internal-link validation: pass.\n'''
        f'''- Downstream website/mobile artifacts must be regenerated only from this finished canonical EPUB.\n''',
        encoding='utf-8'
    )


def main():
    actual_sha = base.sha256(EPUB)
    if actual_sha != BASELINE:
        raise SystemExit(f'baseline SHA mismatch expected={BASELINE} got={actual_sha}')

    pre_articles, pre_exceptions = grammar.audit_epub(EPUB)
    if pre_articles:
        raise RuntimeError('baseline article QA not clean')

    before = collect(EPUB)
    if len(before) != 31102:
        raise RuntimeError(f'baseline verse count {len(before)} != 31102')

    pre_closers, pre_openers = quote_space_refs(before)
    expected_closers = {('genesis', c, v) for c, v in SPACED_CLOSER_KEYS}
    expected_openers = {('genesis', c, v) for c, v in SPACED_OPEN_KEYS}
    if pre_closers != expected_closers:
        raise RuntimeError(f'unexpected spaced-closer inventory: {sorted(pre_closers)}')
    if pre_openers != expected_openers:
        raise RuntimeError(f'unexpected spaced-opener inventory: {sorted(pre_openers)}')

    changes = build_changes(before)

    now = datetime.now(timezone.utc)
    stamp = now.strftime('%Y-%m-%d_%H%MUTC')
    generated = now.replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    archive_dir = ROOT / 'rendered-documents-history' / stamp
    archive_dir.mkdir(parents=True, exist_ok=False)
    archive = archive_dir / EPUB.name
    shutil.copy2(EPUB, archive)
    if base.sha256(archive) != BASELINE:
        raise RuntimeError('archive SHA mismatch')

    rewrite_genesis_source(changes)
    changed_member = rewrite_epub(changes)
    newsha = base.sha256(EPUB)
    if newsha == BASELINE:
        raise RuntimeError('EPUB hash did not change')

    after = collect(EPUB)
    if len(after) != 31102:
        raise RuntimeError(f'post-release verse count {len(after)} != 31102')
    diffs = [(key, before[key], after[key]) for key in before if before[key] != after[key]]
    expected_keys = {('genesis', c, v) for c, v in CHANGE_KEYS}
    if {key for key, _, _ in diffs} != expected_keys or len(diffs) != len(expected_keys):
        raise RuntimeError(
            'whole-Bible diff is not exactly the approved 19 verses: ' +
            json.dumps([(SLUG_TO_BOOK[k[0]], k[1], k[2]) for k, _, _ in diffs], ensure_ascii=False)
        )
    for row in changes:
        key = ('genesis', row['chapter'], row['verse'])
        if after[key] != row['after']:
            raise RuntimeError(f'post-release exact mismatch at {row["reference"]}')

    post_closers, post_openers = quote_space_refs(after)
    if post_closers or post_openers:
        raise RuntimeError(
            f'quote-boundary whitespace remains closers={sorted(post_closers)} openers={sorted(post_openers)}'
        )

    post_articles, post_exceptions = grammar.audit_epub(EPUB)
    if post_articles:
        raise RuntimeError('article mismatches introduced: ' + json.dumps(post_articles[:20], ensure_ascii=False))
    if len(post_exceptions) != len(pre_exceptions):
        raise RuntimeError('article exception inventory changed')

    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256') != BASELINE:
        raise RuntimeError('registry baseline SHA mismatch')
    registry['canonicalEpubSha256'] = newsha
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    fallback = base.build_fallback(EPUB, registry, newsha, generated)
    for key, expected in [('bookCount', 66), ('chapterCount', 1189), ('verseSearchCount', 31102)]:
        if fallback.get(key) != expected:
            raise RuntimeError(f'fallback {key} mismatch: {fallback.get(key)}')

    report = {
        'release': RELEASE_NAME,
        'releaseDate': '2026-09-30',
        'priorEpubSha256': BASELINE,
        'releasedEpubSha256': newsha,
        'archivePath': archive.relative_to(ROOT).as_posix(),
        'changedVerseCount': len(changes),
        'wholeBibleVerseCount': 31102,
        'changedEpubMembers': [changed_member],
        'changes': changes,
        'reviewedNoChangeDenseQuoteCandidates': REVIEWED_NO_CHANGE,
        'policy': {
            'wordingChanges': 0,
            'quotationLevelsRemoved': 0,
            'globalQuoteStyleConversion': False,
            'rule': 'Remove only whitespace between nested curly quotation marks at the 19 audited Genesis references; preserve all required quotation levels and all wording.'
        },
        'qa': {
            'wholeBibleDiffExactlyApproved19': True,
            'remainingNestedCurlyQuoteWhitespaceHits': 0,
            'epubStructureXmlAndLinks': 'pass',
            'articleMismatchCount': 0,
            'verseInventory': '31102/31102'
        },
        'canonicalMobileFallback': fallback,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    write_audit(changes, newsha, generated)

    NOTE.parent.mkdir(parents=True, exist_ok=True)
    NOTE.write_text(
        f'''# {RELEASE_NAME}\n\n'''
        f'''User-authorized whole-Bible punctuation follow-up.\n\n'''
        f'''- Exact Scripture diff: 19 Genesis verses, typography-only.\n'''
        f'''- Removed only whitespace between nested curly quotation marks.\n'''
        f'''- Preserved every quotation level and every word.\n'''
        f'''- Twelve dense straight-quote regex candidates were context-reviewed and retained because their adjacent quote marks close legitimate nested speech.\n'''
        f'''- Prior EPUB SHA-256: `{BASELINE}`\n'''
        f'''- New EPUB SHA-256: `{newsha}`\n'''
        f'''- Previous EPUB archived at `{archive.relative_to(ROOT).as_posix()}`\n'''
        f'''- EPUB ZIP/XML/internal-link validation: pass\n'''
        f'''- Whole-Bible inventory: 31,102 / 31,102 verses\n'''
        f'''- Remaining audited nested-curly quote-spacing defects: 0\n\n'''
        f'''Website reader/download EPUB/search/mobile feed and native mobile content provenance must be regenerated from this exact finished canonical EPUB.\n''',
        encoding='utf-8'
    )

    base.append_once(
        HISTORY_LOG,
        newsha,
        f'- **{stamp}** — {RELEASE_NAME}: 19 Genesis typography-only quote-spacing corrections. Prior EPUB archived at `{archive.relative_to(ROOT).as_posix()}`; new SHA-256 `{newsha}`.'
    )
    base.append_once(
        REFRESH,
        '## 2026-09-30 quotation nesting spacing normalization',
        f'''## 2026-09-30 quotation nesting spacing normalization\n\nFinite 19-verse Genesis typography correction from the whole-Bible quotation audit. Only whitespace between nested curly quotation marks changed; no words or quotation levels changed. Dense straight-quote candidates with legitimate nested speech were retained. Canonical SHA-256: `{newsha}`. See `../editor-notes/consistency/2026-09-30-quotation-spacing-release.md` and `../change-logs/reports/2026-09-30-quotation-spacing-release.json`.'''
    )
    base.replace_sha_in_file(ROOT_README, BASELINE, newsha)
    base.replace_sha_in_file(CURRENT_README, BASELINE, newsha)

    print(json.dumps({
        'releasedEpubSha256': newsha,
        'changedVerseCount': len(changes),
        'remainingNestedCurlyQuoteWhitespaceHits': 0,
        'mobileFallback': fallback,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
