#!/usr/bin/env python3
from __future__ import annotations
import json, re, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'change-logs'/'reports'/'2026-09-12-divine-pronoun-high-confidence-triage.json'
OUT=ROOT/'editor-notes'/'consistency'/'divine-pronoun-triage-chunks-2026-09-12'
CHUNK=12

def slugify(v): return re.sub(r'[^a-z0-9]+','-',v.lower()).strip('-')

def main():
    data=json.loads(SRC.read_text(encoding='utf-8'))
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    groups={}
    for row in data.get('candidates',[]): groups.setdefault(row['reference'].rsplit(' ',1)[0],[]).append(row)
    readme=['# Divine-pronoun triage chunks — 2026-09-12','']
    total=0
    for book in sorted(groups):
        rows=groups[book]; total+=len(rows)
        for idx in range(0,len(rows),CHUNK):
            chunk=rows[idx:idx+CHUNK]; part=idx//CHUNK+1; fn=f'{slugify(book)}-{part:02d}.md'
            lines=[f'# {book} — divine-pronoun triage part {part}','',f'Candidates {idx+1}–{idx+len(chunk)} of {len(rows)}. Review-only; no Scripture changes.','']
            for row in chunk:
                sig=', '.join(f"{x['type']}:{x['pronoun']}→{x['divine']}" for x in row.get('signals',[]))
                lines.append(f"- **{row['reference']}** — [{sig}] — {row['text']}")
            (OUT/fn).write_text('\n'.join(lines)+'\n',encoding='utf-8')
            readme.append(f'- {book} part {part}: `{fn}`')
    (OUT/'README.md').write_text('\n'.join(readme)+'\n',encoding='utf-8')
    print(json.dumps({'candidateCount':total,'chunkFiles':sum((len(v)+CHUNK-1)//CHUNK for v in groups.values())},indent=2))
if __name__=='__main__': main()
