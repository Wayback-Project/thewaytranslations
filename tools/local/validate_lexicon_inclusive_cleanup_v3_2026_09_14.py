#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
AUD=ROOT/'audit-output'/'old-testament-gender-brokenness-2026-09-14'
P=AUD/'proposed-cleanup-v3.tsv'
S=AUD/'proposed-cleanup-v3-validation.json'

BAD_PATTERNS={
 'brokenness-residual': re.compile(r'\bbrokenness\b|\bbroken person\b|\bbroken people\b',re.I),
 'invalid-article': re.compile(r'\b(?:a evil|an evil person|an wicked|a adversary|an person)\b',re.I),
 'malformed-evil-noun': re.compile(r'\b(?:evil animals?|evil arrows?|evil device|evil congregation|evil news|evil diseases|went evil with)\b',re.I),
 'singular-they-agreement': re.compile(r'\bthey\s+(?:is|was|has|does|lies|defiles|swears|walks|goes|comes|knows|gives|takes|makes|says|seeks|hates)\b',re.I),
 'double-article-person': re.compile(r'\b(?:a|an)\s+(?:brokenness|evil)\s+(?:a|an)\s+person\b',re.I),
}


def main():
    with P.open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f,delimiter='\t'))
    if len(rows) != 370:
        # 347 lexical + 23 generic, with Deut 24:7 overlap = 369 unique unless another overlap.
        # Keep this diagnostic explanatory rather than silently accepting drift.
        pass
    failures=[]
    for r in rows:
        after=r['after']
        for name,pat in BAD_PATTERNS.items():
            if pat.search(after): failures.append({'reference':r['reference'],'check':name,'text':after})
    refs=[r['reference'] for r in rows]
    if len(refs)!=len(set(refs)):
        failures.append({'reference':'*','check':'duplicate-reference','text':'Duplicate reference in proposal'})
    lexical=[r for r in rows if 'lexical' in r['categories']]
    generic=[r for r in rows if 'generic-pronoun' in r['categories']]
    report={'rowCount':len(rows),'lexicalRows':len(lexical),'genericRows':len(generic),'failureCount':len(failures),'failures':failures}
    S.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2,ensure_ascii=False))
    if failures:
        raise SystemExit('Proposal validation failed')

if __name__=='__main__': main()
