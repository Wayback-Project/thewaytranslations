#!/usr/bin/env python3
from __future__ import annotations

import bisect
import hashlib
import html
import json
import os
import posixpath
import re
import shutil
import tempfile
import urllib.parse
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / 'current-form-documents' / 'the-way-current.epub'
REGISTRY = ROOT / 'current-form-documents' / 'original-name-registry.json'
LEDGER = ROOT / 'change-logs' / 'reports' / '2026-09-12-original-name-restoration-release.json'
NOTE = ROOT / 'editor-notes' / 'consistency' / '2026-09-12-original-name-restoration-release.md'
CURRENT_README = ROOT / 'current-form-documents' / 'README.md'
ROOT_README = ROOT / 'README.md'
HISTORY_LOG = ROOT / 'rendered-documents-history' / 'LOG.md'
PROPOSAL_DIR = ROOT / 'editor-notes' / 'proposed-rules' / 'original-name-restoration' / 'directory'
BASELINE = '73c3bc73d2da91fed507ee7dd6e1db72f4640847c664cdc4666f4ad065faff50'

RELEASE_FILES = [
    'priority-people.json',
    'priority-places.json',
    'beth-beit-a.json',
    'beth-beit-b.json',
    'consistency-backlog-a.json',
    'consistency-backlog-b.json',
]

GUIDE_ALIASES = {
    'rakhel': ['Rachel'],
    'hananyah': ['Ananias'],
    'yochana': ['Joanna'],
    'shoshana': ['Susanna'],
    'yair': ['Jair', 'Jairus'],
    'shalem': ['Salem'],
}

EXTRA_GUIDES = [
    {
        'id': 'mattityah-matthias',
        'category': 'person',
        'term': 'Mattityah',
        'traditionalAliases': ['Matthias'],
        'pronunciationDisplay': 'maht-tee-YAH',
        'editorialStatus': 'guide-only',
        'notes': 'Acts 1:23 and Acts 1:26 identity; familiar alias is Matthias, not Mattithiah or Mattathias.',
        'exampleReferences': ['Acts 1:23', 'Acts 1:26'],
    }
]

# Explicit choices resolved by this release authorization.
DISPLAY_OVERRIDES = {
    'canaan': "Kena'an",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def visible(inner: str) -> str:
    return html.unescape(re.sub(r'<[^>]+>', '', inner)).replace('\u00a0', ' ').strip()


def slug_to_book(slug: str) -> str:
    special = {
        'psalms': 'Psalms', 'song-of-solomon': 'Song of Solomon',
        '1-samuel': '1 Samuel', '2-samuel': '2 Samuel',
        '1-kings': '1 Kings', '2-kings': '2 Kings',
        '1-chronicles': '1 Chronicles', '2-chronicles': '2 Chronicles',
        '1-corinthians': '1 Corinthians', '2-corinthians': '2 Corinthians',
        '1-thessalonians': '1 Thessalonians', '2-thessalonians': '2 Thessalonians',
        '1-timothy': '1 Timothy', '2-timothy': '2 Timothy',
        '1-peter': '1 Peter', '2-peter': '2 Peter',
        '1-john': '1 John', '2-john': '2 John', '3-john': '3 John',
    }
    return special.get(slug, slug.replace('-', ' ').title())


def load_entries() -> tuple[list[dict], list[dict]]:
    released = []
    for filename in RELEASE_FILES:
        data = json.loads((PROPOSAL_DIR / filename).read_text(encoding='utf-8'))
        for raw in data['entries']:
            item = dict(raw)
            item['proposedForm'] = DISPLAY_OVERRIDES.get(item['id'], item['proposedForm'])
            item['_proposalFile'] = filename
            released.append(item)

    guide_data = json.loads((PROPOSAL_DIR / 'reader-guide-only.json').read_text(encoding='utf-8'))
    guides = [dict(item) for item in guide_data['entries']]

    ids = [item['id'] for item in released]
    if len(ids) != len(set(ids)):
        raise RuntimeError('duplicate released proposal ids')
    return released, guides


def token_pattern(value: str) -> re.Pattern[str]:
    return re.compile(r'(?<![A-Za-z0-9_])' + re.escape(value) + r'(?![A-Za-z0-9_])')


def edit_member(name: str, raw: bytes, mappings: list[dict]) -> tuple[bytes, list[dict], Counter]:
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        return raw, [], Counter()

    slug = Path(name).stem
    book = slug_to_book(slug)
    chapter_re = re.compile(rf'id=["\']ch-{re.escape(slug)}-(\d+)["\']', re.I)
    chapter_hits = [(m.start(), int(m.group(1))) for m in chapter_re.finditer(text)]
    chapter_positions = [p for p, _ in chapter_hits]
    p_re = re.compile(r'(<(?:[A-Za-z_][\w.-]*:)?p\b([^>]*)>)(.*?)(</(?:[A-Za-z_][\w.-]*:)?p>)', re.I | re.S)

    changes = []
    counts = Counter()
    pieces = []
    cursor = 0

    for m in p_re.finditer(text):
        pieces.append(text[cursor:m.start()])
        open_tag, attrs, inner, close_tag = m.group(1), m.group(2), m.group(3), m.group(4)
        pieces.append(open_tag)

        plain = visible(inner)
        verse_match = re.match(r'^(\d+)\.\s*', plain)
        if not verse_match or re.search(r'\bid=["\']ch-', attrs, re.I):
            pieces.append(inner)
            pieces.append(close_tag)
            cursor = m.end()
            continue

        chapter_idx = bisect.bisect_right(chapter_positions, m.start()) - 1
        if chapter_idx < 0:
            raise RuntimeError(f'{name}: verse paragraph before chapter anchor: {plain[:80]}')
        chapter = chapter_hits[chapter_idx][1]
        verse = int(verse_match.group(1))
        before_plain = plain
        updated_inner = inner
        applied_ids = []
        applied_pairs = []

        for item in mappings:
            target = item['proposedForm']
            for old in sorted(item['currentForms'], key=len, reverse=True):
                if old == target:
                    continue
                pat = token_pattern(old)
                visible_now = visible(updated_inner)
                if not pat.search(visible_now):
                    continue
                if re.search(r'<[^>]+>', updated_inner):
                    raise RuntimeError(f'{book} {chapter}:{verse}: inline markup in a targeted verse; refusing generic rewrite')
                updated_inner, n = pat.subn(target, updated_inner)
                if n:
                    counts[(item['id'], old, target)] += n
                    applied_ids.append(item['id'])
                    applied_pairs.append({'from': old, 'to': target, 'count': n})

        if updated_inner != inner:
            after_plain = visible(updated_inner)
            changes.append({
                'reference': f'{book} {chapter}:{verse}',
                'member': name,
                'before': re.sub(r'^\d+\.\s*', '', before_plain),
                'after': re.sub(r'^\d+\.\s*', '', after_plain),
                'mappingIds': sorted(set(applied_ids)),
                'replacements': applied_pairs,
            })
        pieces.append(updated_inner)
        pieces.append(close_tag)
        cursor = m.end()

    pieces.append(text[cursor:])
    return ''.join(pieces).encode('utf-8'), changes, counts


def verse_corpus(members: dict[str, bytes]) -> str:
    out = []
    p_re = re.compile(r'<(?:[A-Za-z_][\w.-]*:)?p\b([^>]*)>(.*?)</(?:[A-Za-z_][\w.-]*:)?p>', re.I | re.S)
    for name, raw in members.items():
        if not name.lower().endswith(('.xhtml', '.html', '.htm')):
            continue
        text = raw.decode('utf-8', 'ignore')
        for attrs, inner in p_re.findall(text):
            plain = visible(inner)
            if re.match(r'^\d+\.\s*', plain) and not re.search(r'\bid=["\']ch-', attrs, re.I):
                out.append(plain)
    return '\n'.join(out)


def validate_epub(path: Path) -> tuple[int, int]:
    with zipfile.ZipFile(path, 'r') as z:
        if z.testzip() is not None:
            raise RuntimeError('ZIP CRC failure')
        first = z.infolist()[0]
        if first.filename != 'mimetype' or first.compress_type != zipfile.ZIP_STORED:
            raise RuntimeError('EPUB mimetype rule failed')
        if z.read('mimetype') != b'application/epub+zip':
            raise RuntimeError('EPUB mimetype content failed')
        names = set(z.namelist())
        ids = {}
        book_members = []
        chapter_count = 0
        for name in z.namelist():
            if name.lower().endswith(('.xhtml', '.html', '.htm', '.opf', '.ncx', '.xml')):
                raw = z.read(name)
                ET.fromstring(raw)
                text = raw.decode('utf-8', 'ignore')
                ids[name] = set(re.findall(r'\bid=["\']([^"\']+)', text))
                cc = len(re.findall(r'\bid=["\']ch-', text))
                if cc:
                    book_members.append(name)
                    chapter_count += cc
                if '<<' in text or '>>' in text:
                    raise RuntimeError(f'angle-marker artifact in {name}')
        if len(book_members) != 66:
            raise RuntimeError(f'expected 66 book XHTML members, got {len(book_members)}')
        if chapter_count != 1189:
            raise RuntimeError(f'expected 1189 chapter anchors, got {chapter_count}')
        unresolved = []
        for src in ids:
            text = z.read(src).decode('utf-8', 'ignore')
            for href in re.findall(r'\bhref=["\']([^"\']+)', text):
                if not href or href.startswith(('http:', 'https:', 'mailto:', 'data:', 'javascript:')):
                    continue
                path_part, sep, frag = href.partition('#')
                target = src if not path_part else posixpath.normpath(posixpath.join(posixpath.dirname(src), urllib.parse.unquote(path_part)))
                if target not in names:
                    unresolved.append((src, href, 'missing member'))
                    continue
                if sep and frag and target in ids and urllib.parse.unquote(frag) not in ids[target]:
                    unresolved.append((src, href, 'missing fragment'))
        if unresolved:
            raise RuntimeError(f'unresolved internal links: {unresolved[:10]}')
        return len(book_members), chapter_count


def registry_record(item: dict, aliases: list[str] | None = None, status: str = 'released') -> dict:
    return {
        'id': item['id'],
        'term': item['proposedForm'],
        'traditionalAliases': aliases if aliases is not None else list(item.get('currentForms', [])),
        'category': item['category'],
        'pronunciationDisplay': item.get('pronunciationDisplay'),
        'nativeForms': item.get('nativeForms', []),
        'originalLanguagePreference': item.get('originalLanguagePreference', {}),
        'exampleReferences': item.get('exampleReferences', []),
        'editorialStatus': status,
        'scopeNotes': item.get('matchGuidance', {}).get('notes', ''),
    }


def main() -> None:
    actual = sha256(EPUB)
    if actual != BASELINE:
        if REGISTRY.exists():
            existing = json.loads(REGISTRY.read_text(encoding='utf-8'))
            if existing.get('canonicalEpubSha256') == actual and existing.get('releaseDate') == '2026-09-12':
                print(json.dumps({'status': 'already-applied', 'sha256': actual}, indent=2))
                return
        raise SystemExit(f'baseline SHA mismatch: expected {BASELINE}, got {actual}')

    released, guides = load_entries()
    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%MUTC')
    archive_dir = ROOT / 'rendered-documents-history' / stamp
    archive_dir.mkdir(parents=True, exist_ok=False)
    archive = archive_dir / EPUB.name
    shutil.copy2(EPUB, archive)
    if sha256(archive) != BASELINE:
        raise RuntimeError('archive SHA mismatch')

    with zipfile.ZipFile(EPUB, 'r') as zin:
        infos = zin.infolist()
        original = {i.filename: zin.read(i.filename) for i in infos}

    edited = dict(original)
    all_changes = []
    totals = Counter()
    changed_members = set()

    for name, raw in list(edited.items()):
        if not name.lower().endswith(('.xhtml', '.html', '.htm')):
            continue
        new_raw, changes, counts = edit_member(name, raw, released)
        if new_raw != raw:
            edited[name] = new_raw
            changed_members.add(name)
            all_changes.extend(changes)
            totals.update(counts)

    by_id = defaultdict(int)
    for (entry_id, old, target), count in totals.items():
        by_id[entry_id] += count

    missing_entries = [item['id'] for item in released if by_id[item['id']] == 0]
    if missing_entries:
        raise RuntimeError(f'approved release entries had zero Scripture replacements: {missing_entries}')

    corpus = verse_corpus(edited)
    stale = []
    for item in released:
        target = item['proposedForm']
        for old in item['currentForms']:
            if old == target:
                continue
            if token_pattern(old).search(corpus):
                stale.append({'id': item['id'], 'form': old})
    if stale:
        raise RuntimeError(f'stale approved traditional forms remain in verse text: {stale[:30]}')

    # Book titles are deliberately not changed by this release.
    joined_all = '\n'.join(raw.decode('utf-8', 'ignore') for raw in edited.values() if isinstance(raw, bytes))
    for heading in ['Luke 1', 'Nehemiah 1', 'Jonah 1', 'Hosea 1', 'Ruth 1', 'Zechariah 1']:
        if heading not in joined_all:
            raise RuntimeError(f'book-title/chapter heading preservation check failed: {heading}')

    if by_id['luke-person'] < 3:
        raise RuntimeError(f'expected at least three Luke-person → Lukas replacements, got {by_id["luke-person"]}')
    if 'Lukas, the beloved physician' not in corpus:
        raise RuntimeError('Colossians 4:14 Lukas verification failed')
    if 'Only Lukas is with me' not in corpus:
        raise RuntimeError('2 Timothy 4:11 Lukas verification failed')

    fd, tmpname = tempfile.mkstemp(suffix='.epub', dir=str(EPUB.parent))
    os.close(fd)
    tmp = Path(tmpname)
    try:
        with zipfile.ZipFile(tmp, 'w') as zout:
            for info in infos:
                zout.writestr(info, edited[info.filename], compress_type=info.compress_type)
        validate_epub(tmp)
        shutil.move(tmp, EPUB)
    finally:
        if tmp.exists():
            tmp.unlink()

    newsha = sha256(EPUB)
    if newsha == BASELINE:
        raise RuntimeError('release SHA did not change')

    records = [registry_record(item) for item in released]
    for item in guides:
        aliases = GUIDE_ALIASES.get(item['id'])
        if not aliases:
            raise RuntimeError(f'missing familiar alias for reader-guide-only entry {item["id"]}')
        records.append(registry_record(item, aliases=aliases, status='guide-only'))
    records.extend(EXTRA_GUIDES)
    records.sort(key=lambda r: r['id'])

    registry = {
        'schemaVersion': '1.0.0',
        'releaseDate': '2026-09-12',
        'canonicalEpubSha256': newsha,
        'priorCanonicalEpubSha256': BASELINE,
        'policy': {
            'bookTitlesChanged': False,
            'generatedReadersMayRewriteScripture': False,
            'aliasesAreReaderMetadata': True,
            'releasedEntries': len(released),
            'guideOnlyEntries': len(guides) + len(EXTRA_GUIDES),
        },
        'entries': records,
    }
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    mapping_summary = []
    for item in released:
        mapping_summary.append({
            'id': item['id'],
            'from': item['currentForms'],
            'to': item['proposedForm'],
            'replacementCount': by_id[item['id']],
            'proposalFile': item['_proposalFile'],
        })

    report = {
        'release': '2026-09-12 original-name restoration batch',
        'prior_epub_sha256': BASELINE,
        'released_epub_sha256': newsha,
        'archive_path': archive.relative_to(ROOT).as_posix(),
        'changedVerseCount': len(all_changes),
        'replacementCount': sum(totals.values()),
        'mappingCount': len(released),
        'changedBookMembers': sorted(changed_members),
        'mappings': mapping_summary,
        'changes': sorted(all_changes, key=lambda c: c['reference']),
        'preservedBookTitles': ['Luke', 'Nehemiah', 'Jonah', 'Hosea', 'Ruth', 'Zechariah'],
        'guideOnlyAliases': records[len(released):],
        'qa': {
            'bookCount': 66,
            'chapterCount': 1189,
            'zipCrc': 'pass',
            'xmlParse': 'pass',
            'internalLinks': 'pass',
            'staleReleasedFormsInVerseText': 0,
            'bookTitlePreservation': 'pass',
            'lukePersonReplacementCount': by_id['luke-person'],
        },
    }
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    NOTE.parent.mkdir(parents=True, exist_ok=True)
    NOTE.write_text(f'''# Original-name restoration release — 2026-09-12

This release promotes the reviewed high-priority original-name proposal directory into a canonical Scripture release under explicit editor authorization. It applies only the listed person/place/full-compound mappings to verse text. Biblical book titles remain unchanged unless separately approved.

## Release summary

- Prior canonical EPUB SHA-256: `{BASELINE}`
- Released canonical EPUB SHA-256: `{newsha}`
- Prior EPUB archived at `{archive.relative_to(ROOT).as_posix()}`
- Approved mapping identities: **{len(released)}**
- Individual replacements: **{sum(totals.values())}**
- Changed verses: **{len(all_changes)}**
- Affected book XHTML members: **{len(changed_members)}**
- Coverage preserved: **66 books / 1,189 chapters**

## Scope highlights

- `Michael` → `Mikha'el`
- `Ishmael` → `Yishmael`
- `Adonijah` → `Adoniyahu`
- `Abishai` → `Avishai`
- `Abiathar` → `Evyatar`
- `Phinehas` → `Pinchas`
- `Jethro` → `Yitro`
- `Laban` → `Lavan`
- `Aquila` → `Akylas`; `Priscilla` → `Priskilla`; `Silvanus` → `Silvanos`
- person `Luke` → `Lukas` while the book title **Luke remains Luke**
- person `Nehemiah` → `Nechemyah` while the book title **Nehemiah remains Nehemiah**
- `Sodom` → `Sedom`; `Gomorrah` → `Amora`; `Canaan` → `Kena'an`; `Caesarea` → `Kaisareia`; `Colossae` → `Kolosai`; `Ashkelon` → `Ashqelon`
- reviewed full `Beth ...` place compounds → their approved `Beit ...` forms; no global bare `Beth` replacement was performed
- consistency backlog forms including Oved, Yoram, Uzziyah, Yotam, Zerubavel, Zerach, Yonah, Peretz, Chetzron, Rut, Malki-Tzedek, She'altiel, Aram, Yekhonyahu, Hoshea, Avram, Yeshua, Bavel, Natzeret, and YHWH

The exact reference-level before/after ledger is `change-logs/reports/2026-09-12-original-name-restoration-release.json`.
The released identity/alias/pronunciation metadata is `current-form-documents/original-name-registry.json` and is intended to drive downstream reader glossary/search metadata without changing Scripture independently.

## Reader-guide-only aliases

The registry also records familiar aliases for already-restored Scripture forms: Rakhel/Rachel, Hananyah/Ananias, Yochana/Joanna, Shoshana/Susanna, Yair/Jair/Jairus, Shalem/Salem, and Mattityah/Matthias. These records do not alter Scripture text.

## QA

The release script rewrites verse paragraphs only, rejects targeted paragraphs containing unexpected inline markup, verifies every approved mapping produced at least one Scripture replacement, verifies no released traditional form remains in verse text, preserves book-title/chapter headings, verifies `Lukas` in the known person references, then validates EPUB CRC/mimetype, XML, internal links, 66 books, and 1,189 chapter anchors.
''', encoding='utf-8')

    cr = CURRENT_README.read_text(encoding='utf-8').replace(BASELINE, newsha)
    cr = re.sub(r'\| Previous release \| Archived under `rendered-documents-history/[^`]+/` \|', f'| Previous release | Archived under `{archive_dir.relative_to(ROOT).as_posix()}/` |', cr)
    marker = 'This EPUB includes the completed whole-Bible divine-pronoun consistency update, the 2026-09-11 original-name / Genesis narrative consistency update (39 reviewed verse-level edits), and the 2026-09-12 1 Corinthians divine-pronoun residual cleanup (4 reviewed verse-level edits);'
    replacement = marker[:-1] + ', plus the 2026-09-12 high-priority original-name restoration release;'
    if marker in cr:
        cr = cr.replace(marker, replacement)
    CURRENT_README.write_text(cr, encoding='utf-8')
    ROOT_README.write_text(ROOT_README.read_text(encoding='utf-8').replace(BASELINE, newsha), encoding='utf-8')

    history = HISTORY_LOG.read_text(encoding='utf-8').rstrip()
    history += f'\n| {stamp} | {archive_dir.relative_to(ROOT).as_posix()}/ | the-way-current.epub (SHA-256 `{BASELINE}`) | Archive prior canonical EPUB before the 2026-09-12 high-priority original-name restoration release; {len(released)} approved mapping identities / {sum(totals.values())} replacements. |\n'
    HISTORY_LOG.write_text(history, encoding='utf-8')

    print(json.dumps({
        'status': 'released',
        'new_sha256': newsha,
        'archive': archive.relative_to(ROOT).as_posix(),
        'mapping_count': len(released),
        'replacement_count': sum(totals.values()),
        'changed_verses': len(all_changes),
        'changed_books': len(changed_members),
        'luke_person_replacements': by_id['luke-person'],
        'top_mappings': sorted(mapping_summary, key=lambda x: x['replacementCount'], reverse=True)[:15],
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
