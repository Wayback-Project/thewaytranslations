#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import audit_divine_gender_titles_2026_09_28 as base

ROOT = base.ROOT
EPUB = base.EPUB
collect_verses = base.collect_verses
BOOKS = base.BOOKS
SLUG_TO_META = base.SLUG_TO_META
CANONICAL_SHA = base.CANONICAL_SHA

DIVINE = re.compile(r"\b(?:YHWH|Elohim|God|Most High|Almighty|Cosmic Parent)\b")
PRON = re.compile(r"\b(?:he|him|his|himself)\b", re.I)
START_PRON = re.compile(r"^[\s\"'“‘\[(]*(?:He|His|Him|Himself)\b")

OUT = ROOT / "tools/local/generated_fresh_divine_pronoun_candidates_2026_09_28.tsv"
REPORT = ROOT / "change-logs/reports/2026-09-28-fresh-divine-pronoun-candidates.json"


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    actual=sha256(EPUB)
    if actual != CANONICAL_SHA:
        raise SystemExit(f"canonical EPUB SHA mismatch expected={CANONICAL_SHA} got={actual}")
    verses=collect_verses(EPUB, slugs=tuple(slug for slug,_,_ in BOOKS))
    if len(verses)!=31102:
        raise RuntimeError(f"whole-Bible verse inventory mismatch: {len(verses)}")

    old_refs=set()
    old_path=ROOT/'tools/local/generated_divine_pronoun_residual_inventory_2026_09_28.tsv'
    if old_path.exists():
        with old_path.open(encoding='utf-8') as f:
            old_refs={r['reference'] for r in csv.DictReader(f,delimiter='\t')}

    rows=[]
    for (slug,ch,vs),text in verses.items():
        if not PRON.search(text):
            continue
        prev=verses.get((slug,ch,vs-1),'')
        same=bool(DIVINE.search(text))
        carry=bool(START_PRON.search(text) and DIVINE.search(prev))
        if not (same or carry):
            continue
        book,testament=SLUG_TO_META[slug]
        ref=f"{book} {ch}:{vs}"
        rows.append({
            'reference':ref,
            'testament':testament,
            'book':book,
            'same_verse_divine_marker':'yes' if same else 'no',
            'previous_verse_carry_candidate':'yes' if carry else 'no',
            'already_in_2026_09_12_triage':'yes' if ref in old_refs else 'no',
            'current_text':text,
            'previous_verse':prev,
        })

    OUT.parent.mkdir(parents=True,exist_ok=True)
    fields=['reference','testament','book','same_verse_divine_marker','previous_verse_carry_candidate','already_in_2026_09_12_triage','current_text','previous_verse']
    with OUT.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)

    new=[r for r in rows if r['already_in_2026_09_12_triage']=='no']
    report={
        'status':'heuristic QA only; not a change list',
        'canonicalEpubSha256':actual,
        'wholeBibleVerseCount':len(verses),
        'freshCandidateVerseCount':len(rows),
        'alreadyRepresentedInPriorTriage':sum(r['already_in_2026_09_12_triage']=='yes' for r in rows),
        'newCandidateVerseCount':len(new),
        'newCandidateCountsByBook':dict(sorted(Counter(r['book'] for r in new).items())),
        'warning':'A match does not prove a divine antecedent. Human, Yeshua, angelic, quoted, and generic pronouns must be rejected contextually before any proposal.',
        'output':str(OUT.relative_to(ROOT)),
    }
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(report,indent=2)+"\n",encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
