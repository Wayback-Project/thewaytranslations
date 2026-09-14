#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

import release_2026_09_13_john_14_6_living_way as base

ROOT = base.ROOT
EPUB = base.EPUB
REGISTRY = base.REGISTRY
ROOT_README = base.ROOT_README
CURRENT_README = base.CURRENT_README
HISTORY_LOG = base.HISTORY_LOG
FALLBACK_DIR = base.FALLBACK_DIR
BASELINE = '36e0d99030228644ac4c84129088e10323826dbe0652e7f0d9d2221575261144'
REPORT = ROOT / 'change-logs' / 'reports' / '2026-09-14-english-article-grammar-consistency.json'
NOTE = ROOT / 'editor-notes' / 'consistency' / '2026-09-14-english-article-grammar-consistency.md'
REFRESH = ROOT / 'current-form-documents' / 'EPUB-REFRESH-INSTRUCTIONS.md'

# Exact findings from the canonical-EPUB audit. These are grammar-only article
# corrections. No noun, verb, name, theological term, or sentence meaning changes.
CHANGES = [
    ('genesis', 37, 2, 'an harmful', 'a harmful'),
    ('genesis', 37, 20, 'An brokenness', 'A brokenness'),
    ('genesis', 37, 33, 'An brokenness', 'A brokenness'),
    ('numbers', 13, 32, 'an harmful', 'a harmful'),
    ('numbers', 14, 36, 'an harmful', 'a harmful'),
    ('numbers', 14, 37, 'an harmful', 'a harmful'),
    ('deuteronomy', 22, 14, 'an harmful', 'a harmful'),
    ('deuteronomy', 22, 19, 'an harmful', 'a harmful'),
    ('judges', 9, 23, 'an troubling', 'a troubling'),
    ('1-samuel', 16, 14, 'an troubling', 'a troubling'),
    ('1-samuel', 16, 15, 'an troubling', 'a troubling'),
    ('1-samuel', 18, 10, 'an troubling', 'a troubling'),
    ('1-samuel', 19, 9, 'An troubling', 'A troubling'),
    ('nehemiah', 6, 13, 'an harmful', 'a harmful'),
    ('psalms', 41, 8, 'An grievous', 'A grievous'),
    ('psalms', 140, 11, 'An brokenness', 'A brokenness'),
    ('proverbs', 12, 13, 'An brokenness', 'A brokenness'),
    ('proverbs', 17, 11, 'An brokenness', 'A brokenness'),
    ('proverbs', 26, 23, 'an broken', 'a broken'),
    ('proverbs', 28, 10, 'an broken', 'a broken'),
    ('proverbs', 29, 6, 'An brokenness', 'A brokenness'),
    ('ecclesiastes', 6, 1, 'an brokenness', 'a brokenness'),
    ('ecclesiastes', 6, 2, 'an grievous', 'a grievous'),
    ('ecclesiastes', 8, 3, 'an broken', 'a broken'),
    ('ecclesiastes', 8, 11, 'an work', 'a work'),
    ('ecclesiastes', 9, 3, 'an brokenness', 'a brokenness'),
    ('ecclesiastes', 9, 12, 'an time', 'a time'),
    ('ecclesiastes', 9, 12, 'an brokenness', 'a brokenness'),
    ('ecclesiastes', 10, 1, 'an brokenness', 'a brokenness'),
    ('ecclesiastes', 10, 5, 'An brokenness', 'A brokenness'),
    ('isaiah', 13, 14, 'a a hunted', 'a hunted'),
    ('jeremiah', 2, 19, 'an broken', 'a broken'),
    ('ezekiel', 7, 5, 'An brokenness', 'A brokenness'),
    ('ezekiel', 38, 10, 'an brokenness', 'a brokenness'),
    ('amos', 5, 13, 'an time', 'a time'),
    ('micah', 2, 3, 'an time', 'a time'),
    ('habakkuk', 2, 9, 'an brokenness', 'a brokenness'),
    ('luke', 12, 50, 'a immersion', 'an immersion'),
]

AN_CONSONANT_EXCEPTIONS = ('heir', 'herb', 'honest', 'honor', 'honour', 'hour')
A_VOWEL_EXCEPTIONS = ('ewe', 'eul', 'eun', 'eup', 'euro', 'euch', 'one', 'once', 'uni', 'use', 'user', 'usual', 'utility', 'utensil', 'ufo')
ARTICLE_RE = re.compile(r"(?<![A-Za-z'’])(a|an)\b\s+([A-Za-z][A-Za-z'’\-]*)", re.I)
VERSE_RE = re.compile(r'^(\d+)\.\s*(.*)$', re.S)

BOOK_NAME = {slug: name for _, group in base.BOOKS for slug, name in group}


def classify(article: str, word: str) -> tuple[bool, str]:
    a = article.lower()
    w = word.lower().lstrip("'’-")
    if not w:
        return False, 'no-word'
    if w in {'a', 'an'}:
        return True, 'duplicate-article'
    vowel = w[0] in 'aeiou'
    if a == 'an' and not vowel:
        if w.startswith(AN_CONSONANT_EXCEPTIONS):
            return False, 'sound-exception-an'
        return True, 'an-before-consonant-letter'
    if a == 'a' and vowel:
        if w.startswith(A_VOWEL_EXCEPTIONS):
            return False, 'sound-exception-a'
        return True, 'a-before-vowel-letter'
    return False, 'orthographically-aligned'


def audit_epub(path: Path):
    actionable = []
    exceptions = []
    with zipfile.ZipFile(path, 'r') as z:
        for _, group in base.BOOKS:
            for slug, _name in group:
                member = base.find_book_member(z, slug)
                root = ET.fromstring(z.read(member))
                chapter = None
                for el in root.iter():
                    number = base.chapter_number(el, slug)
                    if number is not None:
                        chapter = number
                    if base.local_name(el.tag).lower() != 'p':
                        continue
                    text = base.element_text(el)
                    vm = VERSE_RE.match(text)
                    verse = int(vm.group(1)) if vm else None
                    body = vm.group(2) if vm else text
                    for m in ARTICLE_RE.finditer(body):
                        bad, reason = classify(m.group(1), m.group(2))
                        if not bad and not reason.startswith('sound-exception'):
                            continue
                        row = (slug, chapter, verse, m.group(0), reason)
                        (actionable if bad else exceptions).append(row)
    return actionable, exceptions


def rewrite_epub(replacements_by_member: dict[str, Counter]):
    with zipfile.ZipFile(EPUB, 'r') as zin:
        infos = zin.infolist()
        original = {info.filename: zin.read(info.filename) for info in infos}
    edited = dict(original)
    for member, counter in replacements_by_member.items():
        if member not in edited:
            raise RuntimeError(f'missing EPUB member {member}')
        text = edited[member].decode('utf-8')
        for (before, after), expected_count in counter.items():
            found = text.count(before)
            if found != expected_count:
                raise RuntimeError(f'{member}: expected {expected_count} raw occurrence(s) of {before!r}, found {found}')
            text = text.replace(before, after)
        edited[member] = text.encode('utf-8')

    fd, tmpname = tempfile.mkstemp(suffix='.epub', dir=str(EPUB.parent))
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
    changed = sorted(name for name in original if original[name] != edited[name])
    expected_changed = sorted(replacements_by_member)
    if changed != expected_changed:
        raise RuntimeError(f'unexpected EPUB members changed: {changed}; expected {expected_changed}')
    return changed


def fmt_ref(slug: str, chapter: int, verse: int) -> str:
    return f'{BOOK_NAME[slug]} {chapter}:{verse}'


def expected_audit_key(slug: str, chapter: int, verse: int, before: str):
    # The scanner reports the duplicated article token pair itself; the release
    # replacement still removes the full malformed phrase `a a hunted` safely.
    phrase = 'a a' if before.startswith('a a ') else before
    return slug, chapter, verse, phrase


def main():
    actual = base.sha256(EPUB)
    if actual != BASELINE:
        raise SystemExit(f'baseline SHA mismatch: expected {BASELINE}, got {actual}')

    actionable, exceptions = audit_epub(EPUB)
    expected = Counter(expected_audit_key(slug, chapter, verse, before) for slug, chapter, verse, before, _after in CHANGES)
    found = Counter((slug, chapter, verse, phrase) for slug, chapter, verse, phrase, _reason in actionable)
    if found != expected:
        raise RuntimeError('canonical article audit differs from the reviewed 38-item ledger:\n' + json.dumps({'expected': list(expected.elements()), 'found': list(found.elements())}, indent=2))
    if len(exceptions) != 36:
        raise RuntimeError(f'expected 36 sound-based retained exceptions, found {len(exceptions)}')

    now = datetime.now(timezone.utc)
    stamp = now.strftime('%Y-%m-%d_%H%MUTC')
    generated = now.replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    archive_dir = ROOT / 'rendered-documents-history' / stamp
    archive_dir.mkdir(parents=True, exist_ok=False)
    archive = archive_dir / EPUB.name
    shutil.copy2(EPUB, archive)
    if base.sha256(archive) != BASELINE:
        raise RuntimeError('archive SHA mismatch')

    replacements_by_member: dict[str, Counter] = defaultdict(Counter)
    with zipfile.ZipFile(EPUB, 'r') as z:
        for slug, _chapter, _verse, before, after in CHANGES:
            member = base.find_book_member(z, slug)
            replacements_by_member[member][(before, after)] += 1
    changed_members = rewrite_epub(replacements_by_member)
    newsha = base.sha256(EPUB)
    if newsha == BASELINE:
        raise RuntimeError('EPUB SHA did not change')

    post_actionable, post_exceptions = audit_epub(EPUB)
    if post_actionable:
        raise RuntimeError('article inconsistencies remain after release: ' + json.dumps(post_actionable, indent=2))
    if len(post_exceptions) != 36:
        raise RuntimeError(f'sound-based exception inventory changed unexpectedly: {len(post_exceptions)}')

    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256') != BASELINE:
        raise RuntimeError('registry baseline SHA mismatch')
    registry['canonicalEpubSha256'] = newsha
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    fallback = base.build_fallback(EPUB, registry, newsha, generated)

    changes = [
        {
            'reference': fmt_ref(slug, chapter, verse),
            'book': slug,
            'chapter': chapter,
            'verse': verse,
            'before': before,
            'after': after,
            'reason': 'English indefinite-article grammar consistency; wording and meaning otherwise unchanged.'
        }
        for slug, chapter, verse, before, after in CHANGES
    ]
    report = {
        'release': '2026-09-14 English grammar consistency updates',
        'scope': 'Indefinite-article agreement (a/an) in the canonical current-form EPUB',
        'prior_epub_sha256': BASELINE,
        'released_epub_sha256': newsha,
        'archive_path': archive.relative_to(ROOT).as_posix(),
        'change_count': len(changes),
        'retained_sound_based_exception_count': len(post_exceptions),
        'changes': changes,
        'mobileFallback': fallback,
        'qa': {
            'book_count': 66,
            'chapter_count': 1189,
            'verse_search_records': 31102,
            'zip_crc': 'pass',
            'xml_parse': 'pass',
            'internal_links': 'pass',
            'post_release_actionable_article_mismatches': 0,
            'changed_book_members': changed_members,
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    by_book = defaultdict(list)
    for change in changes:
        by_book[change['book']].append(change)
    detail_lines = []
    for _, group in base.BOOKS:
        for slug, _name in group:
            for item in by_book.get(slug, []):
                detail_lines.append(f"- {item['reference']}: `{item['before']}` → `{item['after']}`")

    NOTE.parent.mkdir(parents=True, exist_ok=True)
    NOTE.write_text(f'''# English article grammar consistency — 2026-09-14

## Scope

A canonical whole-Bible audit checked indefinite-article forms that looked like **`an` before a consonant-starting word** or **`a` before a vowel-starting word**, plus duplicated articles. Because English `a`/`an` follows pronunciation rather than spelling alone, candidates were reviewed rather than changed mechanically.

This release corrects **{len(changes)}** genuine grammar errors. It deliberately retains **{len(post_exceptions)}** sound-based forms that are valid English, such as `an hour` and `a one-...` constructions. Restored names containing apostrophes (for example `Kena'an` / `She'an`) are excluded from article matching.

No theological term, proper name, noun, verb, or sentence meaning was changed. These are English grammar consistency corrections only.

## Exact corrections

{chr(10).join(detail_lines)}

## Release

- Previous EPUB SHA-256: `{BASELINE}`
- Released EPUB SHA-256: `{newsha}`
- Exact machine-readable ledger: `change-logs/reports/2026-09-14-english-article-grammar-consistency.json`
- Previous canonical EPUB archived at `{archive.relative_to(ROOT).as_posix()}`
- Public mobile fallback regenerated at `current-form-documents/mobile-reader/manifest.json` and `content.json`
- EPUB QA: 66 books / 1,189 chapters; ZIP, XML, internal links, and 31,102 verse-search records validated.
- Post-release grammar audit: **0 actionable article mismatches**; {len(post_exceptions)} pronunciation-based exceptions retained.
''', encoding='utf-8')

    base.append_once(HISTORY_LOG, newsha, f'''- **{stamp}** — English grammar consistency update released: {len(changes)} `a`/`an` corrections across {len(by_book)} books. Prior canonical EPUB archived at `{archive.relative_to(ROOT).as_posix()}`; new SHA-256 `{newsha}`.''')
    base.append_once(REFRESH, '## 2026-09-14 English article grammar consistency', f'''## 2026-09-14 English article grammar consistency

A whole-Bible `a`/`an` audit corrected **{len(changes)}** genuine English article-agreement errors while retaining **{len(post_exceptions)}** pronunciation-based exceptions. No theological or lexical wording was changed. Canonical SHA-256: `{newsha}`. See `../editor-notes/consistency/2026-09-14-english-article-grammar-consistency.md` and `../change-logs/reports/2026-09-14-english-article-grammar-consistency.json`.''')
    base.replace_sha_in_file(ROOT_README, BASELINE, newsha)
    base.replace_sha_in_file(CURRENT_README, BASELINE, newsha)

    print(json.dumps({
        'release': 'English grammar consistency updates',
        'releasedEpubSha256': newsha,
        'changeCount': len(changes),
        'changedBooks': len(by_book),
        'retainedSoundExceptions': len(post_exceptions),
        'postReleaseActionableMismatches': len(post_actionable),
        'fallbackContentSha256': fallback['contentSha256'],
        'fallbackBytes': fallback['contentBytes'],
    }, indent=2))


if __name__ == '__main__':
    main()
