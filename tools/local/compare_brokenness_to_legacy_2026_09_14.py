#!/usr/bin/env python3
from __future__ import annotations

import csv
import difflib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANDIDATES = ROOT / 'audit-output' / 'old-testament-gender-brokenness-2026-09-14' / 'candidates.tsv'
HIST = ROOT / 'rendered-documents-history' / '2026-04-08_1216UTC' / 'books'
OUT = ROOT / 'audit-output' / 'old-testament-gender-brokenness-2026-09-14' / 'brokenness-legacy-comparison.tsv'

BOOK_TO_SLUG = {
'Genesis':'genesis','Exodus':'exodus','Leviticus':'leviticus','Numbers':'numbers','Deuteronomy':'deuteronomy',
'Joshua':'joshua','Judges':'judges','Ruth':'ruth','1 Samuel':'1-samuel','2 Samuel':'2-samuel','1 Kings':'1-kings','2 Kings':'2-kings',
'1 Chronicles':'1-chronicles','2 Chronicles':'2-chronicles','Ezra':'ezra','Nehemiah':'nehemiah','Esther':'esther','Job':'job',
'Psalms':'psalms','Proverbs':'proverbs','Ecclesiastes':'ecclesiastes','Song of Solomon':'song-of-solomon','Isaiah':'isaiah',
'Jeremiah':'jeremiah','Lamentations':'lamentations','Ezekiel':'ezekiel','Daniel':'daniel','Hosea':'hosea','Joel':'joel','Amos':'amos',
'Obadiah':'obadiah','Jonah':'jonah','Micah':'micah','Nahum':'nahum','Habakkuk':'habakkuk','Zephaniah':'zephaniah','Haggai':'haggai',
'Zechariah':'zechariah','Malachi':'malachi'}

VERSE_RE = re.compile(r'^(\d+)\.\s+(.*)$')
HEADING_RE = re.compile(r'^.+?\s+-\s+Chapter\s+(\d+)\s*$')
TOKEN_RE = re.compile(r"\w+(?:['’]\w+)?|[^\w\s]", re.UNICODE)


def parse_book(book: str) -> dict[tuple[int,int], str]:
    slug = BOOK_TO_SLUG[book]
    d = HIST / slug
    out: dict[tuple[int,int], str] = {}
    chapter_files = sorted(d.glob('chapter-*.txt'))
    if chapter_files:
        for p in chapter_files:
            m = re.search(r'chapter-(\d+)\.txt$', p.name)
            if not m: continue
            ch = int(m.group(1))
            for line in p.read_text(encoding='utf-8').splitlines():
                vm = VERSE_RE.match(line.strip())
                if vm:
                    out[(ch, int(vm.group(1)))] = vm.group(2).strip()
        return out
    p = d / 'book.txt'
    if not p.exists():
        raise RuntimeError(f'No historical text for {book}: {d}')
    ch = None
    for line in p.read_text(encoding='utf-8').splitlines():
        hm = HEADING_RE.match(line.strip())
        if hm:
            ch = int(hm.group(1)); continue
        vm = VERSE_RE.match(line.strip())
        if vm and ch is not None:
            out[(ch, int(vm.group(1)))] = vm.group(2).strip()
    return out


def diff_summary(old: str, new: str) -> str:
    a = TOKEN_RE.findall(old)
    b = TOKEN_RE.findall(new)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    parts=[]
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag == 'equal': continue
        old_span = ' '.join(a[i1:i2]) or '∅'
        new_span = ' '.join(b[j1:j2]) or '∅'
        parts.append(f'{tag}: [{old_span}] -> [{new_span}]')
    return ' || '.join(parts)


def main():
    rows=[]
    with CANDIDATES.open(encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            if r['category'] == 'BROKENNESS LEXICAL REVIEW':
                rows.append(r)
    books={b:parse_book(b) for b in sorted({r['book'] for r in rows})}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    missing=[]
    with OUT.open('w', encoding='utf-8', newline='') as f:
        fields=['reference','book','chapter','verse','historical','current','diff']
        w=csv.DictWriter(f, fieldnames=fields, delimiter='\t'); w.writeheader()
        for r in rows:
            ch=int(r['chapter']); vs=int(r['verse'])
            old=books[r['book']].get((ch,vs),'')
            if not old: missing.append(r['reference'])
            w.writerow({'reference':r['reference'],'book':r['book'],'chapter':ch,'verse':vs,'historical':old,'current':r['text'],'diff':diff_summary(old,r['text']) if old else 'MISSING'})
    if missing:
        raise SystemExit(f'Missing historical verses: {missing[:20]} total={len(missing)}')
    print(f'brokenness_rows={len(rows)} compared={len(rows)} missing=0 output={OUT}')

if __name__ == '__main__':
    main()
