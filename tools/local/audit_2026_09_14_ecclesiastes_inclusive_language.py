#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import release_2026_09_14_psalms_proverbs_inclusive_pronouns as release

ROOT = release.ROOT
EPUB = release.EPUB
OUT = ROOT / 'audit-output' / 'ecclesiastes-inclusive-language-2026-09-14'

TRIGGERS = re.compile(r"\b(?:man|men|mankind|he|him|his|himself|someone|person|people|human|humans|humanity|father|son|brother|husband|king|prince|master|workman|watchmen)\b", re.I)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    verse_map = release.collect_verses(EPUB, slugs=('ecclesiastes', 'isaiah'))
    rows = []
    isaiah = {}
    for (slug, chapter, verse), text in sorted(verse_map.items(), key=lambda item: (item[0][0], item[0][1], item[0][2])):
        if slug == 'ecclesiastes':
            hits = sorted({x.group(0).lower() for x in TRIGGERS.finditer(text)})
            rows.append({'book':'Ecclesiastes','chapter':chapter,'verse':verse,'triggers':','.join(hits),'text':text})
        elif slug == 'isaiah' and chapter == 1 and verse == 16:
            isaiah = {'book':'Isaiah','chapter':1,'verse':16,'text':text}
    rows.sort(key=lambda r: (r['chapter'], r['verse']))
    if len(rows) != 222:
        raise SystemExit(f'Expected 222 Ecclesiastes verses, got {len(rows)}')
    if not isaiah:
        raise SystemExit('Isaiah 1:16 not found')
    candidates = [r for r in rows if r['triggers']]
    with (OUT / 'all-verses.tsv').open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['book','chapter','verse','triggers','text'], delimiter='\t')
        w.writeheader(); w.writerows(rows)
    with (OUT / 'candidates.tsv').open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['book','chapter','verse','triggers','text'], delimiter='\t')
        w.writeheader(); w.writerows(candidates)
    summary = {'ecclesiastesVerseCount':len(rows),'candidateVerseCount':len(candidates),'isaiah1_16':isaiah}
    (OUT / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
