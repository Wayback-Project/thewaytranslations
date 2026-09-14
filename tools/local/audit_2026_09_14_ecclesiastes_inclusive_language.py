#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / 'current-form-documents' / 'the-way-current.epub'
OUT = ROOT / 'audit-output' / 'ecclesiastes-inclusive-language-2026-09-14'

TRIGGERS = re.compile(r"\b(?:man|men|mankind|he|him|his|himself|someone|person|people|human|humans|humanity|father|son|brother|husband|king|prince|master|workman|watchmen)\b", re.I)

def clean_fragment(value: str) -> str:
    value = re.sub(r'<[^>]+>', '', value)
    return html.unescape(value).replace('\xa0', ' ').strip()


def collect_verses() -> tuple[list[dict], dict]:
    rows: list[dict] = []
    isaiah = {}
    with zipfile.ZipFile(EPUB) as zf:
        for name in zf.namelist():
            if not name.lower().endswith(('.xhtml', '.html', '.htm')):
                continue
            raw = zf.read(name).decode('utf-8')
            if 'v-ecclesiastes-' in raw:
                for m in re.finditer(r'<p\s+id=["\']v-ecclesiastes-(\d+)-(\d+)["\'][^>]*>(.*?)</p>', raw, re.I | re.S):
                    chapter, verse = int(m.group(1)), int(m.group(2))
                    text = clean_fragment(m.group(3))
                    hits = sorted({x.group(0).lower() for x in TRIGGERS.finditer(text)})
                    rows.append({'book':'Ecclesiastes','chapter':chapter,'verse':verse,'text':text,'triggers':','.join(hits)})
            if 'v-isaiah-1-16' in raw:
                m = re.search(r'<p\s+id=["\']v-isaiah-1-16["\'][^>]*>(.*?)</p>', raw, re.I | re.S)
                if m:
                    isaiah = {'book':'Isaiah','chapter':1,'verse':16,'text':clean_fragment(m.group(1))}
    rows.sort(key=lambda r: (r['chapter'], r['verse']))
    return rows, isaiah


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows, isaiah = collect_verses()
    if len(rows) != 222:
        raise SystemExit(f'Expected 222 Ecclesiastes verses, got {len(rows)}')
    candidates = [r for r in rows if r['triggers']]
    with (OUT / 'all-verses.tsv').open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['book','chapter','verse','triggers','text'], delimiter='\t')
        w.writeheader(); w.writerows(rows)
    with (OUT / 'candidates.tsv').open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['book','chapter','verse','triggers','text'], delimiter='\t')
        w.writeheader(); w.writerows(candidates)
    summary = {
        'ecclesiastesVerseCount': len(rows),
        'candidateVerseCount': len(candidates),
        'isaiah1_16': isaiah,
    }
    (OUT / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
