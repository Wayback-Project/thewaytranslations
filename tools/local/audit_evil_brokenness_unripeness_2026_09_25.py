#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

import release_2026_09_14_ecclesiastes_inclusive_language_isaiah_harm as prior

ROOT = prior.ROOT
EPUB = prior.EPUB
collect_verses = prior.prev.collect_verses
CANONICAL_SHA = 'edd3182ff57b54471505189628b82238c85d2d9c8b4edbba14339695eac827cd'
HISTORICAL_LEDGER = ROOT / 'tools' / 'local' / 'approved_lexicon_cleanup_2026_09_14.tsv'
OUT = ROOT / 'tools' / 'local' / 'generated_evil_inventory_2026_09_25.tsv'
CONCEPT_OUT = ROOT / 'tools' / 'local' / 'generated_concept_term_inventory_2026_09_25.tsv'
SUMMARY = ROOT / 'change-logs' / 'reports' / '2026-09-25-evil-brokenness-unripeness-inventory.json'

BOOKS = [
('genesis','Genesis','OT'),('exodus','Exodus','OT'),('leviticus','Leviticus','OT'),('numbers','Numbers','OT'),('deuteronomy','Deuteronomy','OT'),
('joshua','Joshua','OT'),('judges','Judges','OT'),('ruth','Ruth','OT'),('1-samuel','1 Samuel','OT'),('2-samuel','2 Samuel','OT'),('1-kings','1 Kings','OT'),('2-kings','2 Kings','OT'),
('1-chronicles','1 Chronicles','OT'),('2-chronicles','2 Chronicles','OT'),('ezra','Ezra','OT'),('nehemiah','Nehemiah','OT'),('esther','Esther','OT'),('job','Job','OT'),
('psalms','Psalms','OT'),('proverbs','Proverbs','OT'),('ecclesiastes','Ecclesiastes','OT'),('song-of-solomon','Song of Solomon','OT'),('isaiah','Isaiah','OT'),
('jeremiah','Jeremiah','OT'),('lamentations','Lamentations','OT'),('ezekiel','Ezekiel','OT'),('daniel','Daniel','OT'),('hosea','Hosea','OT'),('joel','Joel','OT'),('amos','Amos','OT'),
('obadiah','Obadiah','OT'),('jonah','Jonah','OT'),('micah','Micah','OT'),('nahum','Nahum','OT'),('habakkuk','Habakkuk','OT'),('zephaniah','Zephaniah','OT'),('haggai','Haggai','OT'),
('zechariah','Zechariah','OT'),('malachi','Malachi','OT'),
('matthew','Matthew','NT'),('mark','Mark','NT'),('luke','Luke','NT'),('john','John','NT'),('acts','Acts','NT'),('romans','Romans','NT'),
('1-corinthians','1 Corinthians','NT'),('2-corinthians','2 Corinthians','NT'),('galatians','Galatians','NT'),('ephesians','Ephesians','NT'),('philippians','Philippians','NT'),
('colossians','Colossians','NT'),('1-thessalonians','1 Thessalonians','NT'),('2-thessalonians','2 Thessalonians','NT'),('1-timothy','1 Timothy','NT'),('2-timothy','2 Timothy','NT'),
('titus','Titus','NT'),('philemon','Philemon','NT'),('hebrews','Hebrews','NT'),('james','James','NT'),('1-peter','1 Peter','NT'),('2-peter','2 Peter','NT'),
('1-john','1 John','NT'),('2-john','2 John','NT'),('3-john','3 John','NT'),('jude','Jude','NT'),('revelation','Revelation','NT')]
SLUG_TO_META = {slug:(book,testament) for slug,book,testament in BOOKS}

EVIL = re.compile(r'\bevil\b', re.I)
CONCEPT = re.compile(r'\b(?:evil|brokenness|broken|unripeness|unripe)\b', re.I)
LOWER_SENTENCE_EVIL = re.compile(r'(^|[.!?][\"”\'’)]*\s+)evil\b')
SPACE_BEFORE_PUNCT = re.compile(r'\s+[,.!?;:]')
DOUBLE_SPACE = re.compile(r' {2,}')
ARTICLE_BAD = re.compile(r'\b(?:a\s+(?:evil|unripe)|an\s+(?:broken|brokenness|unripeness))\b', re.I)


def sha256(path: Path):
    return prior.base.sha256(path)


def historical_map():
    out={}
    with HISTORICAL_LEDGER.open(encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            if 'lexical' not in row['categories'].split(','):
                continue
            key=(row['book'], int(row['chapter']), int(row['verse']))
            out[key]={'before':row['before'],'after':row['after']}
    return out


def grammar_flags(text: str):
    flags=[]
    if LOWER_SENTENCE_EVIL.search(text): flags.append('sentence-initial-lowercase-evil')
    if ARTICLE_BAD.search(text): flags.append('article-agreement')
    if DOUBLE_SPACE.search(text): flags.append('double-space')
    if SPACE_BEFORE_PUNCT.search(text): flags.append('space-before-punctuation')
    if text and text[-1] not in '.!?;:,””\"\'’—': flags.append('terminal-punctuation-review')
    return flags


def main():
    actual=sha256(EPUB)
    if actual != CANONICAL_SHA:
        raise SystemExit(f'canonical EPUB SHA mismatch expected={CANONICAL_SHA} got={actual}')
    verses=collect_verses(EPUB, slugs=tuple(slug for slug,_,_ in BOOKS))
    if len(verses) != 31102:
        raise RuntimeError(f'whole-Bible verse inventory mismatch: {len(verses)} != 31102')
    hist=historical_map()
    evil_rows=[]
    concept_rows=[]
    for (slug,ch,vs),text in verses.items():
        book,testament=SLUG_TO_META[slug]
        ref=f'{book} {ch}:{vs}'
        matches=sorted({m.group(0).lower() for m in CONCEPT.finditer(text)})
        if matches:
            concept_rows.append({'reference':ref,'testament':testament,'book':book,'chapter':ch,'verse':vs,'matched_terms':','.join(matches),'current_text':text})
        if EVIL.search(text):
            h=hist.get((book,ch,vs),{})
            evil_rows.append({
                'reference':ref,'testament':testament,'book':book,'chapter':ch,'verse':vs,
                'current_text':text,
                'historical_pre_cleanup_text':h.get('before',''),
                'historical_cleanup_text':h.get('after',''),
                'in_2026_09_14_lexical_ledger':'yes' if h else 'no',
                'current_grammar_flags':','.join(grammar_flags(text)),
            })
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('w',encoding='utf-8',newline='') as f:
        fields=['reference','testament','book','chapter','verse','current_text','historical_pre_cleanup_text','historical_cleanup_text','in_2026_09_14_lexical_ledger','current_grammar_flags']
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(evil_rows)
    with CONCEPT_OUT.open('w',encoding='utf-8',newline='') as f:
        fields=['reference','testament','book','chapter','verse','matched_terms','current_text']
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(concept_rows)
    by_testament=Counter(r['testament'] for r in evil_rows)
    by_book=Counter(r['book'] for r in evil_rows)
    flags=Counter(flag for r in evil_rows for flag in r['current_grammar_flags'].split(',') if flag)
    report={
        'status':'inventory-only; non-canonical; no Scripture changes',
        'canonicalEpubSha256':actual,
        'wholeBibleVerseCount':len(verses),
        'evilVerseCount':len(evil_rows),
        'evilVerseCountsByTestament':dict(by_testament),
        'evilVerseCountsByBook':dict(sorted(by_book.items())),
        'evilRowsFrom2026_09_14LexicalLedger':sum(r['in_2026_09_14_lexical_ledger']=='yes' for r in evil_rows),
        'conceptTermVerseCount':len(concept_rows),
        'currentGrammarFlags':dict(flags),
        'outputs':[str(OUT.relative_to(ROOT)),str(CONCEPT_OUT.relative_to(ROOT))],
        'method':'Exact whole-Bible extraction from the canonical EPUB using the repository release extractor; word-boundary inventory for evil and consistency inventory for evil/brokenness/broken/unripeness/unripe. No replacement is performed.'
    }
    SUMMARY.parent.mkdir(parents=True,exist_ok=True)
    SUMMARY.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
