#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / "current-form-documents" / "the-way-current.epub"
REGISTRY = ROOT / "current-form-documents" / "original-name-registry.json"
OUT_JSON = ROOT / "change-logs" / "reports" / "2026-09-12-final-name-alignment-audit.json"
OUT_MD = ROOT / "editor-notes" / "consistency" / "2026-09-12-final-name-alignment-audit.md"

BOOKS = {
    'genesis':'Genesis','exodus':'Exodus','leviticus':'Leviticus','numbers':'Numbers','deuteronomy':'Deuteronomy',
    'joshua':'Joshua','judges':'Judges','ruth':'Ruth','1-samuel':'1 Samuel','2-samuel':'2 Samuel','1-kings':'1 Kings',
    '2-kings':'2 Kings','1-chronicles':'1 Chronicles','2-chronicles':'2 Chronicles','ezra':'Ezra','nehemiah':'Nehemiah',
    'esther':'Esther','job':'Job','psalms':'Psalms','proverbs':'Proverbs','ecclesiastes':'Ecclesiastes',
    'song-of-solomon':'Song of Solomon','isaiah':'Isaiah','jeremiah':'Jeremiah','lamentations':'Lamentations','ezekiel':'Ezekiel',
    'daniel':'Daniel','hosea':'Hosea','joel':'Joel','amos':'Amos','obadiah':'Obadiah','jonah':'Jonah','micah':'Micah','nahum':'Nahum',
    'habakkuk':'Habakkuk','zephaniah':'Zephaniah','haggai':'Haggai','zechariah':'Zechariah','malachi':'Malachi',
    'matthew':'Matthew','mark':'Mark','luke':'Luke','john':'John','acts':'Acts','romans':'Romans','1-corinthians':'1 Corinthians',
    '2-corinthians':'2 Corinthians','galatians':'Galatians','ephesians':'Ephesians','philippians':'Philippians','colossians':'Colossians',
    '1-thessalonians':'1 Thessalonians','2-thessalonians':'2 Thessalonians','1-timothy':'1 Timothy','2-timothy':'2 Timothy',
    'titus':'Titus','philemon':'Philemon','hebrews':'Hebrews','james':'James','1-peter':'1 Peter','2-peter':'2 Peter',
    '1-john':'1 John','2-john':'2 John','3-john':'3 John','jude':'Jude','revelation':'Revelation'
}

def visible(s: str) -> str:
    return html.unescape(re.sub(r'<[^>]+>', '', s)).replace('\u00a0', ' ').strip()

def boundary(value: str) -> re.Pattern[str]:
    return re.compile(r'(?<![A-Za-z0-9_])' + re.escape(value) + r'(?![A-Za-z0-9_])', re.I)

def verses():
    with zipfile.ZipFile(EPUB) as z:
        for member in z.namelist():
            m = re.fullmatch(r'OEBPS/Text/(.+)\.xhtml', member)
            if not m:
                continue
            slug = m.group(1)
            book = BOOKS.get(slug, slug)
            raw = z.read(member).decode('utf-8')
            chapter = None
            for pm in re.finditer(r'<p\b(?P<a>[^>]*)>(?P<i>.*?)</p>', raw, re.I | re.S):
                ch = re.search(rf'id=["\']ch-{re.escape(slug)}-(\d+)["\']', pm.group('a'), re.I)
                if ch:
                    chapter = int(ch.group(1))
                    continue
                text = visible(pm.group('i'))
                vm = re.match(r'^(\d+)\.\s*(.*)$', text, re.S)
                if vm and chapter:
                    yield {
                        'reference': f'{book} {chapter}:{int(vm.group(1))}',
                        'book': book,
                        'chapter': chapter,
                        'verse': int(vm.group(1)),
                        'member': member,
                        'text': vm.group(2).strip(),
                    }

def main():
    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    entries = []
    for item in registry.get('entries', []):
        term = item.get('term', '')
        for alias in item.get('traditionalAliases', []):
            if alias and alias.casefold() != term.casefold():
                entries.append((item.get('id'), alias, term, item.get('category'), item.get('scopeNotes', '')))

    rows = []
    inscription_rows = []
    for verse in verses():
        text = verse['text']
        for item_id, alias, term, category, scope in entries:
            matches = list(boundary(alias).finditer(text))
            for match in matches:
                rows.append({
                    **verse,
                    'id': item_id,
                    'alias': alias,
                    'matched': match.group(0),
                    'canonical': term,
                    'category': category,
                    'scopeNotes': scope,
                })
        if re.search(r'\bKING OF THE JEWS\b', text, re.I) or re.search(r'\bJESUS\b', text) or re.search(r'\bNAZARETH\b', text):
            inscription_rows.append(verse)

    report = {
        'epub': str(EPUB.relative_to(ROOT)),
        'caseInsensitiveTraditionalAliasHits': len(rows),
        'caseInsensitiveTraditionalAliasVerses': len({r['reference'] for r in rows}),
        'hits': rows,
        'inscriptionOrUppercaseLegacyCandidates': inscription_rows,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    lines = [
        '# Final original-name alignment audit — 2026-09-12',
        '',
        f"- Case-insensitive released traditional-name hits: **{len(rows)}** across **{len({r['reference'] for r in rows})}** verses.",
        f"- Inscription / uppercase legacy candidates: **{len(inscription_rows)}**.",
        '- Diagnostic only. Every hit must be reviewed for identity/scope before editing.',
        '',
        '## Traditional-name hits',
        '',
    ]
    for row in rows:
        lines.append(f"- **{row['reference']}** — `{row['matched']}` → `{row['canonical']}` ({row['id']}) — {row['text']}")
    lines += ['', '## Inscription / uppercase legacy candidates', '']
    for row in inscription_rows:
        lines.append(f"- **{row['reference']}** — {row['text']}")
    OUT_MD.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'aliasHits': len(rows), 'aliasVerses': len({r['reference'] for r in rows}), 'inscriptionCandidates': len(inscription_rows)}, indent=2))

if __name__ == '__main__':
    main()
