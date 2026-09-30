#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, json, re
from collections import Counter
from pathlib import Path
import release_2026_09_26_evil_to_brokenness_direct as prev

ROOT=prev.ROOT
EPUB=prev.EPUB
ALL_SLUGS=prev.ALL_SLUGS
SLUG_TO_BOOK=prev.SLUG_TO_BOOK
collect_verses=prev.collect_verses
EXPECTED_SHA='aec31f9c9248cd42913c561c4cd5155fb35c39dddc657b16e53c370edff7a615'
OUT=ROOT/'change-logs/reports/2026-09-30-kingdom-residual-audit.tsv'
SUMMARY=ROOT/'change-logs/reports/2026-09-30-kingdom-residual-audit.json'
PAT=re.compile(r'\bkingdoms?\b',re.I)
DIVINE=re.compile(r'\b(?:YHWH|Elohim|God|Most High|Cosmic Parent|Almighty|Adonai)\b',re.I)
RULE=re.compile(r'\b(?:reign|dominion|throne|everlasting|forever|saints? of the Most High)\b',re.I)

def sha256(path:Path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def main():
    actual=sha256(EPUB)
    if actual!=EXPECTED_SHA: raise SystemExit(f'canonical EPUB SHA mismatch expected={EXPECTED_SHA} got={actual}')
    verses=collect_verses(EPUB,slugs=ALL_SLUGS)
    if len(verses)!=31102: raise RuntimeError(f'verse count {len(verses)} != 31102')
    rows=[]
    for (slug,ch,v),text in verses.items():
        if not PAT.search(text): continue
        book=SLUG_TO_BOOK[slug]
        prev_text=verses.get((slug,ch,v-1),'')
        next_text=verses.get((slug,ch,v+1),'')
        context=' '.join([prev_text,text,next_text])
        forms=[m.group(0) for m in PAT.finditer(text)]
        rows.append({
            'reference':f'{book} {ch}:{v}',
            'book':book,'chapter':ch,'verse':v,
            'kingdom_occurrences':len(forms),'forms':'|'.join(forms),
            'same_verse_divine_marker':'yes' if DIVINE.search(text) else 'no',
            'context_divine_marker':'yes' if DIVINE.search(context) else 'no',
            'rule_authority_signal':'yes' if RULE.search(context) else 'no',
            'previous_verse':prev_text,'current_text':text,'next_verse':next_text,
        })
    OUT.parent.mkdir(parents=True,exist_ok=True)
    fields=list(rows[0].keys())
    with OUT.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows)
    candidates=[r for r in rows if r['context_divine_marker']=='yes' and r['rule_authority_signal']=='yes']
    report={
        'status':'review-only; no Scripture changes',
        'canonicalEpubSha256':actual,
        'wholeBibleVerseCount':len(verses),
        'versesContainingKingdomOrKingdoms':len(rows),
        'totalKingdomTokenOccurrences':sum(r['kingdom_occurrences'] for r in rows),
        'candidateVerseCount':len(candidates),
        'candidateReferences':[r['reference'] for r in candidates],
        'candidateRows':candidates,
        'method':[
            'Exact whole-word kingdom/kingdoms inventory from the current canonical EPUB.',
            'Previous and next verse captured for every match.',
            'Candidate flag is deliberately broad: nearby divine marker plus rule/authority signal. Every candidate requires context-first human review; it is not an automatic replacement list.',
            'Human/geopolitical kingdom language must remain kingdom; active divine or saintly rule/authority may be reviewed for reign.'
        ]
    }
    SUMMARY.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='candidateRows'},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
