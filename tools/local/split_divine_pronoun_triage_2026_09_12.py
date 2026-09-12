#!/usr/bin/env python3
from __future__ import annotations
import json, re, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'change-logs' / 'reports' / '2026-09-12-divine-pronoun-high-confidence-triage.json'
OUT = ROOT / 'editor-notes' / 'consistency' / 'divine-pronoun-triage-2026-09-12'


def slugify(value: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def main():
    data=json.loads(SRC.read_text(encoding='utf-8'))
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    groups={}
    for row in data.get('candidates',[]):
        book=row['reference'].rsplit(' ',1)[0]
        groups.setdefault(book,[]).append(row)
    index=['# Divine-pronoun triage by book — 2026-09-12','']
    for book in sorted(groups):
        rows=groups[book]
        fn=f'{slugify(book)}.md'
        lines=[f'# {book} — divine-pronoun residual triage', '', f'Heuristic candidates: **{len(rows)}**. Review-only; no Scripture changes.', '']
        for row in rows:
            sig=', '.join(f"{x['type']}:{x['pronoun']}→{x['divine']}" for x in row.get('signals',[]))
            lines.append(f"- **{row['reference']}** — [{sig}] — {row['text']}")
        (OUT/fn).write_text('\n'.join(lines)+'\n',encoding='utf-8')
        index.append(f'- {book}: {len(rows)} — `{fn}`')
    (OUT/'README.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
    print(json.dumps({'booksWithCandidates':len(groups),'candidateCount':sum(map(len,groups.values()))},indent=2))
if __name__=='__main__': main()
