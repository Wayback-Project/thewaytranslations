#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import json
import os
import re
import shutil
import tempfile
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import release_2026_09_14_lexicon_update_ai_cleanup as prior

base = prior.base
grammar = prior.grammar
ROOT = prior.ROOT
EPUB = prior.EPUB
REGISTRY = prior.REGISTRY
ROOT_README = prior.ROOT_README
CURRENT_README = prior.CURRENT_README
HISTORY_LOG = prior.HISTORY_LOG
REFRESH = prior.REFRESH
replace_one_verse = prior.replace_one_verse

BASELINE = 'd48ec5b7da0db10c7c44c518793228dc5b2d69edc6e57de838486d2aefbcf62f'
LEDGER = ROOT / 'tools' / 'local' / 'approved_romans_structural_cleanup_2026_09_15.tsv'
REPORT = ROOT / 'change-logs' / 'reports' / '2026-09-15-romans-structural-cleanup.json'
NOTE = ROOT / 'editor-notes' / 'consistency' / '2026-09-15-romans-structural-cleanup.md'
RELEASE_NAME = 'Romans structural mapping, malformed-English, and verse-record cleanup'

NT_CHAPTERS = {
    'matthew':28,'mark':16,'luke':24,'john':21,'acts':28,'romans':16,'1-corinthians':16,'2-corinthians':13,
    'galatians':6,'ephesians':6,'philippians':4,'colossians':4,'1-thessalonians':5,'2-thessalonians':3,
    '1-timothy':6,'2-timothy':4,'titus':3,'philemon':1,'hebrews':13,'james':5,'1-peter':5,'2-peter':3,
    '1-john':5,'2-john':1,'3-john':1,'jude':1,'revelation':22,
}
ROMANS_COUNTS = {1:32,2:29,3:31,4:25,5:21,6:23,7:25,8:39,9:33,10:21,11:36,12:21,13:14,14:23,15:33,16:27}
P_RE = re.compile(r'(<(?:[A-Za-z_][\w.-]*:)?p\b[^>]*>)(.*?)(</(?:[A-Za-z_][\w.-]*:)?p>)', re.I | re.S)
VERSE_RE = re.compile(r'^(\d+)\.\s*(.*)$', re.S)

GENESIS_24_4_CANONICAL = 'But you shall go to my country, and to my kin, and take a wife for my son Yitzhak.”'
GENESIS_24_4_DUPLICATE = 'But you shall go to my country, and to my relatives, and take a wife for my son Yitzhak.”'

BEFORE = {
    (5,19): "For as through the one a person's disobedience many were made sinners, even so through the obedience of the one, many will be made righteous.",
    (8,9): "But you are not in the flesh but in the Ruach, if it is so that the Ruach of God dwells in you. But if anyone doesn't have the Ruach of Messiah, they are not their.",
    (14,2): "One a person has faith to eat all things, but the one who is weak eats only vegetables.",
    (14,23): "But the one who doubts is condemned if they eat, because it isn't of faith; and whatever is not of faith is sin. (14:24) Now to the one who is able to establish you according to my good news and the preaching of Yeshua the Messiah, according to the revelation of the mystery which has been kept secret through long ages, (14:25) but now is revealed, and by the Scriptures of the prophets, according to the commandment of the age-enduring God, is made known for obedience of faith to all the nations; (14:26) to the only wise God, through Yeshua the Messiah, to whom be the glory forever! Amen.",
    (16,25): "",
    (16,26): "016:027",
}
AFTER = {
    (5,19): "For as through the disobedience of one person many were made sinners, even so through the obedience of the one, many will be made righteous.",
    (8,9): "But you are not in the flesh but in the Ruach, if it is so that the Ruach of God dwells in you. But if anyone doesn't have the Ruach of Messiah, they do not belong to Messiah.",
    (14,2): "One person has faith to eat all things, but the one who is weak eats only vegetables.",
    (14,23): "But the one who doubts is condemned if they eat, because it isn't of faith; and whatever is not of faith is sin.",
    (16,25): "Now to the one who is able to establish you according to my good news and the preaching of Yeshua the Messiah, according to the revelation of the mystery which has been kept secret through long ages,",
    (16,26): "but now is revealed, and by the Scriptures of the prophets, according to the commandment of the age-enduring God, is made known for obedience of faith to all the nations;",
    (16,27): "to the only wise God, through Yeshua the Messiah, to whom be the glory forever! Amen.",
}


def chapter_span(text: str, slug: str, chapter: int):
    pat = re.compile(rf'\bid=["\']ch-{re.escape(slug)}-{chapter}["\']', re.I)
    m = pat.search(text)
    if not m:
        raise RuntimeError(f'cannot find chapter anchor {slug} {chapter}')
    start = m.start()
    nxt = re.compile(rf'\bid=["\']ch-{re.escape(slug)}-{chapter + 1}["\']', re.I).search(text, m.end())
    return start, (nxt.start() if nxt else len(text))


def numbered_paragraphs(text: str, slug: str, chapter: int):
    start, end = chapter_span(text, slug, chapter)
    rows = []
    for m in P_RE.finditer(text[start:end]):
        plain = base.visible(m.group(2))
        vm = VERSE_RE.match(plain)
        if vm:
            rows.append((int(vm.group(1)), vm.group(2), start + m.start(), start + m.end(), m))
    return rows


def get_romans_verse(text: str, chapter: int, verse: int) -> str | None:
    rows = [body for number, body, *_ in numbered_paragraphs(text, 'romans', chapter) if number == verse]
    if not rows:
        return None
    if len(rows) != 1:
        raise RuntimeError(f'Romans {chapter}:{verse} paragraph count={len(rows)}')
    return rows[0]


def collect_nt(path: Path):
    out = {}
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f'EPUB CRC failure: {bad}')
        for slug, expected_chapters in NT_CHAPTERS.items():
            member = base.find_book_member(z, slug)
            raw = z.read(member).decode('utf-8')
            anchors = [int(x) for x in re.findall(rf'\bid=["\']ch-{re.escape(slug)}-(\d+)["\']', raw, re.I)]
            if anchors != list(range(1, expected_chapters + 1)):
                raise RuntimeError(f'{slug} chapter anchors invalid: {anchors}')
            for chapter in range(1, expected_chapters + 1):
                seen = set()
                for verse, body, *_ in numbered_paragraphs(raw, slug, chapter):
                    if verse in seen:
                        raise RuntimeError(f'duplicate New Testament verse {slug} {chapter}:{verse}')
                    seen.add(verse)
                    out[(slug, chapter, verse)] = body
                if not seen:
                    raise RuntimeError(f'no verses found for {slug} {chapter}')
    return out


def raw_search_inventory(path: Path):
    raw_count = 0
    duplicate_refs = []
    with zipfile.ZipFile(path) as z:
        for testament, group in base.BOOKS:
            for slug, name in group:
                member = base.find_book_member(z, slug)
                book = base.extract_book(z.read(member), slug, name)
                for chapter in book['chapters']:
                    grouped = defaultdict(list)
                    for verse in chapter['verses']:
                        raw_count += 1
                        grouped[verse['number']].append(verse)
                    for number, rows in grouped.items():
                        if len(rows) > 1:
                            duplicate_refs.append({
                                'reference': f"{name} {chapter['number']}:{number}",
                                'count': len(rows),
                                'texts': [r['text'] for r in rows],
                            })
    return raw_count, duplicate_refs


def load_ledger():
    with LEDGER.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    if len(rows) != 8:
        raise RuntimeError(f'approved release ledger row count={len(rows)}, expected 8')
    expected = {
        'Romans 5:19','Romans 8:9','Romans 14:2','Romans 14:23','Romans 16:25','Romans 16:26','Romans 16:27','Genesis 24:4'
    }
    refs = {f"{r['book']} {r['chapter']}:{r['verse']}" for r in rows}
    if refs != expected:
        raise RuntimeError(f'approved release ledger refs mismatch: {sorted(refs)}')
    return rows


def validate_pre(path: Path):
    nt = collect_nt(path)
    if len(nt) != 7956:
        raise RuntimeError(f'pre-release NT unique verse count {len(nt)} != 7956')
    with zipfile.ZipFile(path) as z:
        romans = z.read(base.find_book_member(z, 'romans')).decode('utf-8')
        for ref, before in BEFORE.items():
            actual = get_romans_verse(romans, *ref)
            if actual != before:
                raise RuntimeError(f'pre-release Romans {ref[0]}:{ref[1]} mismatch expected={before!r} actual={actual!r}')
        if get_romans_verse(romans, 16, 27) is not None:
            raise RuntimeError('pre-release Romans 16:27 unexpectedly exists')
        genesis = z.read(base.find_book_member(z, 'genesis')).decode('utf-8')
        g24v4 = [body for number, body, *_ in numbered_paragraphs(genesis, 'genesis', 24) if number == 4]
        if g24v4 != [GENESIS_24_4_CANONICAL, GENESIS_24_4_DUPLICATE]:
            raise RuntimeError(f'pre-release Genesis 24:4 duplicate inventory mismatch: {g24v4!r}')
    raw_count, duplicates = raw_search_inventory(path)
    if raw_count != 31102:
        raise RuntimeError(f'pre-release raw search rows {raw_count} != 31102')
    if len(duplicates) != 1 or duplicates[0]['reference'] != 'Genesis 24:4':
        raise RuntimeError(f'pre-release duplicate inventory mismatch: {duplicates}')


def validate_post(path: Path):
    nt = collect_nt(path)
    if len(nt) != 7957:
        raise RuntimeError(f'post-release NT unique verse count {len(nt)} != 7957')
    with zipfile.ZipFile(path) as z:
        romans = z.read(base.find_book_member(z, 'romans')).decode('utf-8')
        for ref, after in AFTER.items():
            actual = get_romans_verse(romans, *ref)
            if actual != after:
                raise RuntimeError(f'post-release Romans {ref[0]}:{ref[1]} mismatch expected={after!r} actual={actual!r}')
        romans_rows = [(c, v) for c in range(1, 17) for v, *_ in numbered_paragraphs(romans, 'romans', c)]
        expected_rows = [(c, v) for c, count in ROMANS_COUNTS.items() for v in range(1, count + 1)]
        if romans_rows != expected_rows:
            raise RuntimeError('Romans canonical verse sequence is not 1–433 in chapter order')
        if len(romans_rows) != 433:
            raise RuntimeError(f'Romans verse paragraph count {len(romans_rows)} != 433')
        if any(x in (get_romans_verse(romans, 14, 23) or '') for x in ('(14:24)','(14:25)','(14:26)')):
            raise RuntimeError('embedded Romans 14 doxology labels remain')
        if '016:027' in romans:
            raise RuntimeError('literal Romans 016:027 artifact remains')
        if get_romans_verse(romans, 16, 24) != 'The grace of our Master Yeshua the Messiah be with you all! Amen.':
            raise RuntimeError('Romans 16:24 changed unexpectedly')
        genesis = z.read(base.find_book_member(z, 'genesis')).decode('utf-8')
        g24v4 = [body for number, body, *_ in numbered_paragraphs(genesis, 'genesis', 24) if number == 4]
        if g24v4 != [GENESIS_24_4_CANONICAL]:
            raise RuntimeError(f'post-release Genesis 24:4 inventory mismatch: {g24v4!r}')
    raw_count, duplicates = raw_search_inventory(path)
    if raw_count != 31102:
        raise RuntimeError(f'post-release raw search rows {raw_count} != 31102')
    if duplicates:
        raise RuntimeError(f'post-release duplicate verse records remain: {duplicates[:10]}')


def insert_romans_16_27(text: str) -> str:
    if get_romans_verse(text, 16, 27) is not None:
        raise RuntimeError('Romans 16:27 already exists before insertion')
    start, _ = chapter_span(text, 'romans', 16)
    segment = text[start:]
    expected = f"26. {AFTER[(16,26)]}"
    matches = [m for m in P_RE.finditer(segment) if base.visible(m.group(2)) == expected]
    if len(matches) != 1:
        raise RuntimeError(f'Romans 16:26 paragraph count before insertion={len(matches)}')
    m = matches[0]
    opening = m.group(1)
    closing = m.group(3)
    new_p = opening + html.escape(f"27. {AFTER[(16,27)]}", quote=False) + closing
    absolute_end = start + m.end()
    return text[:absolute_end] + '\n' + new_p + text[absolute_end:]


def remove_genesis_duplicate(text: str) -> str:
    start, end = chapter_span(text, 'genesis', 24)
    segment = text[start:end]
    matches = []
    for m in P_RE.finditer(segment):
        plain = base.visible(m.group(2))
        if plain == f'4. {GENESIS_24_4_DUPLICATE}':
            matches.append(m)
    if len(matches) != 1:
        raise RuntimeError(f'Genesis duplicate paragraph match count={len(matches)}')
    m = matches[0]
    abs_start = start + m.start()
    abs_end = start + m.end()
    return text[:abs_start] + text[abs_end:]


def rewrite_epub():
    with zipfile.ZipFile(EPUB, 'r') as zin:
        infos = zin.infolist()
        original = {i.filename: zin.read(i.filename) for i in infos}
        romans_member = base.find_book_member(zin, 'romans')
        genesis_member = base.find_book_member(zin, 'genesis')
    edited = dict(original)

    romans = edited[romans_member].decode('utf-8')
    for ref in [(5,19),(8,9),(14,2),(14,23),(16,25),(16,26)]:
        romans = replace_one_verse(romans, 'romans', ref[0], ref[1], BEFORE[ref], AFTER[ref])
    romans = insert_romans_16_27(romans)
    edited[romans_member] = romans.encode('utf-8')

    genesis = edited[genesis_member].decode('utf-8')
    genesis = remove_genesis_duplicate(genesis)
    edited[genesis_member] = genesis.encode('utf-8')

    fd, tmpname = tempfile.mkstemp(prefix='the-way-romans-', suffix='.epub', dir=EPUB.parent)
    os.close(fd)
    tmp = Path(tmpname)
    try:
        with zipfile.ZipFile(tmp, 'w') as zout:
            for info in infos:
                zout.writestr(info, edited[info.filename], compress_type=info.compress_type)
        base.validate_epub(tmp)
        changed = sorted(name for name in original if original[name] != edited[name])
        expected = sorted([romans_member, genesis_member])
        if changed != expected:
            raise RuntimeError(f'changed EPUB members mismatch expected={expected} actual={changed}')
        shutil.move(tmp, EPUB)
    finally:
        if tmp.exists():
            tmp.unlink()
    return changed


def main():
    ledger = load_ledger()
    actual = base.sha256(EPUB)
    if actual != BASELINE:
        raise SystemExit(f'baseline SHA mismatch expected={BASELINE} got={actual}')

    validate_pre(EPUB)
    pre_articles, pre_exceptions = grammar.audit_epub(EPUB)
    if pre_articles:
        raise RuntimeError('pre-release English article audit not clean: ' + json.dumps(pre_articles[:30], ensure_ascii=False, indent=2))

    now = datetime.now(timezone.utc)
    stamp = now.strftime('%Y-%m-%d_%H%MUTC')
    generated = now.replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    archive_dir = ROOT / 'rendered-documents-history' / stamp
    archive_dir.mkdir(parents=True, exist_ok=False)
    archive = archive_dir / EPUB.name
    shutil.copy2(EPUB, archive)
    if base.sha256(archive) != BASELINE:
        raise RuntimeError('archive SHA mismatch')

    changed_members = rewrite_epub()
    newsha = base.sha256(EPUB)
    if newsha == BASELINE:
        raise RuntimeError('EPUB SHA did not change')

    validate_post(EPUB)
    post_articles, post_exceptions = grammar.audit_epub(EPUB)
    if post_articles:
        raise RuntimeError('article inconsistencies introduced: ' + json.dumps(post_articles[:30], ensure_ascii=False, indent=2))
    if len(post_exceptions) != len(pre_exceptions):
        raise RuntimeError(f'pronunciation article exception inventory changed before={len(pre_exceptions)} after={len(post_exceptions)}')

    with zipfile.ZipFile(EPUB) as z:
        corpus = '\n'.join(z.read(i.filename).decode('utf-8','ignore') for i in z.infolist() if i.filename.lower().endswith(('.xhtml','.html','.htm')))
    forbidden = ["the one a person's disobedience", 'they are not their', 'One a person has faith', '016:027', '(14:24) Now to the one who is able']
    remains = [x for x in forbidden if x in corpus]
    if remains:
        raise RuntimeError(f'residual malformed/structural strings remain: {remains}')

    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256') != BASELINE:
        raise RuntimeError('registry baseline SHA mismatch')
    registry['canonicalEpubSha256'] = newsha
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    fallback = base.build_fallback(EPUB, registry, newsha, generated)
    for key, expected in [('bookCount',66),('chapterCount',1189),('verseSearchCount',31102)]:
        if fallback.get(key) != expected:
            raise RuntimeError(f'fallback {key} mismatch {fallback.get(key)} != {expected}')

    changes = [{
        'reference': f"{row['book']} {row['chapter']}:{row['verse']}",
        'category': row['category'],
        'before': row['before'],
        'after': row['after'],
    } for row in ledger]
    counts = Counter(x['category'] for x in changes)

    report = {
        'release': RELEASE_NAME,
        'prior_epub_sha256': BASELINE,
        'released_epub_sha256': newsha,
        'archive_path': archive.relative_to(ROOT).as_posix(),
        'approved_ledger_rows': len(changes),
        'category_counts': dict(counts),
        'malformed_english_corrections': 3,
        'romans_structural_mapping_records': 4,
        'duplicate_verse_record_removals': 1,
        'romans_verse_paragraphs_before': 432,
        'romans_verse_paragraphs_after': 433,
        'new_testament_unique_verse_paragraphs_before': 7956,
        'new_testament_unique_verse_paragraphs_after': 7957,
        'raw_search_records_before': 31102,
        'raw_search_records_after': 31102,
        'duplicate_references_before': ['Genesis 24:4'],
        'duplicate_references_after': [],
        'changed_epub_members': changed_members,
        'article_mismatch_count': len(post_articles),
        'mobileFallback': fallback,
        'changes': changes,
        'method': 'Finite approved ledger. Three Romans malformed-English repairs; structural relocation of the already-present doxology into Romans 16:25-27 while preserving Romans 16:24; removal of one pre-existing duplicate Genesis 24:4 paragraph while preserving the canonical first paragraph (“my kin”). No other unique Scripture wording changed.',
        'textual_note': 'The manuscript tradition varies on placement of the closing Romans doxology. This release does not adjudicate that textual-critical question; it restores the project canonical data structure to Romans 16:25-27 while preserving the project’s existing doxology wording and Romans 16:24.'
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    NOTE.parent.mkdir(parents=True, exist_ok=True)
    NOTE.write_text(f'''# {RELEASE_NAME} — 2026-09-15\n\n## Scope\n\nThis is a narrow controlled correction release arising from the New Testament residual audit. It repairs the three approved malformed-English verses, restores coherent Romans doxology verse records, and removes one pre-existing duplicate Genesis verse paragraph discovered by release QA.\n\n### Malformed English\n\n- **Romans 5:19** — “through the one a person's disobedience” → “through the disobedience of one person.”\n- **Romans 8:9** — “they are not their” → “they do not belong to Messiah,” preserving inclusive `anyone/they` while making the specific Messiah referent explicit.\n- **Romans 14:2** — “One a person has faith…” → “One person has faith…”.\n\n### Romans verse mapping\n\nThe previous EPUB had **432** Romans verse paragraphs rather than **433**. Romans 14:23 improperly contained parenthetical `(14:24)`, `(14:25)`, and `(14:26)` labels plus the closing doxology; Romans 16:25 was empty; Romans 16:26 contained `016:027`; and Romans 16:27 did not exist as its own paragraph.\n\nThis release restores Romans 14:23 to verse 23 only, places the already-present doxology wording into **Romans 16:25–27**, preserves **Romans 16:24** unchanged, and removes the `016:027` artifact. The manuscript tradition contains more than one placement for the closing Romans doxology; this release does not claim to settle that textual-critical question.\n\n### Genesis 24:4 duplicate record\n\nRelease QA found one old duplicate verse paragraph in Genesis 24:4. The chapter contained both “my kin” and a second duplicate “my relatives” version. The project’s canonical unique-verse extraction already treated the first “my kin” paragraph as Genesis 24:4, and the earlier source file contains that first wording. This release removes only the second duplicate paragraph and preserves **“my kin”** as the canonical verse text.\n\n## QA\n\n- Previous EPUB SHA-256: `{BASELINE}`\n- Released EPUB SHA-256: `{newsha}`\n- Previous EPUB archived at `{archive.relative_to(ROOT).as_posix()}`\n- Romans verse paragraphs: **432 → 433**\n- New Testament unique verse paragraphs: **7,956 → 7,957**\n- Raw search records: **31,102 → 31,102**; the old Genesis duplicate is removed as the missing Romans record is restored\n- Duplicate verse references after release: **0**\n- EPUB ZIP/XML/internal-link validation: **pass**\n- Exact approved ledger: **8 / 8 pass**\n- English article audit: **0 actionable mismatches**\n- Canonical mobile fallback regenerated from the finished EPUB: **66 books / 1,189 chapters / 31,102 search records**\n\n## Downstream rule\n\nWebsite, web reader, EPUB downloads, mobile content feed, and native mobile release pin must consume this exact canonical EPUB. No downstream Scripture hand-editing.\n''', encoding='utf-8')

    base.append_once(HISTORY_LOG, newsha, f'- **{stamp}** — {RELEASE_NAME}: 3 malformed-English repairs, Romans doxology/verse mapping normalization, and removal of the pre-existing duplicate Genesis 24:4 paragraph. NT unique verse paragraphs restored 7,956 → 7,957; search records remain 31,102 with zero duplicate references. Prior EPUB archived at `{archive.relative_to(ROOT).as_posix()}`; new SHA-256 `{newsha}`.')
    base.append_once(REFRESH, '## 2026-09-15 Romans structural mapping and malformed-English correction', f'''## 2026-09-15 Romans structural mapping and malformed-English correction\n\nControlled release: corrected malformed English at Romans 5:19, 8:9, and 14:2; restored Romans 14:23 and Romans 16:25–27 to a coherent verse structure while preserving Romans 16:24 and the existing doxology wording; removed one pre-existing duplicate Genesis 24:4 paragraph while preserving the canonical “my kin” wording. NT unique verse paragraphs are now 7,957 / 7,957 and the 31,102 search records contain no duplicate verse references. Canonical SHA-256: `{newsha}`. See `../editor-notes/consistency/2026-09-15-romans-structural-cleanup.md` and `../change-logs/reports/2026-09-15-romans-structural-cleanup.json`.''')
    base.replace_sha_in_file(ROOT_README, BASELINE, newsha)
    base.replace_sha_in_file(CURRENT_README, BASELINE, newsha)

    print(json.dumps({
        'release': RELEASE_NAME,
        'releasedEpubSha256': newsha,
        'approvedLedgerRows': len(changes),
        'romansVerseParagraphs': 433,
        'newTestamentUniqueVerseParagraphs': 7957,
        'searchRecords': 31102,
        'duplicateReferences': 0,
        'articleMismatches': len(post_articles),
        'fallbackContentSha256': fallback.get('contentSha256'),
        'fallbackBytes': fallback.get('contentBytes'),
        'changedMembers': changed_members,
    }, indent=2))


if __name__ == '__main__':
    main()
