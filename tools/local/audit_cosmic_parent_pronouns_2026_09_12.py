#!/usr/bin/env python3
from __future__ import annotations
import html, json, re, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / 'current-form-documents' / 'the-way-current.epub'
REPORT = ROOT / 'change-logs' / 'reports' / '2026-09-12-cosmic-parent-pronoun-audit.json'
NOTE = ROOT / 'editor-notes' / 'consistency' / '2026-09-12-cosmic-parent-pronoun-audit.md'
PRONOUN = re.compile(r'\b(he|him|his|himself)\b', re.I)
PARA = re.compile(r'<(?:[A-Za-z_][\w.-]*:)?p\b[^>]*>(.*?)</(?:[A-Za-z_][\w.-]*:)?p>', re.I | re.S)

def visible(s: str) -> str:
    return html.unescape(re.sub(r'<[^>]+>', '', s)).replace('\u00a0', ' ').strip()

rows=[]
with zipfile.ZipFile(EPUB,'r') as z:
    for name in z.namelist():
        if not name.lower().endswith(('.xhtml','.html','.htm')): continue
        raw=z.read(name).decode('utf-8','ignore')
        for m in PARA.finditer(raw):
            text=visible(m.group(1))
            if 'Cosmic Parent' not in text: continue
            pronouns=[x.group(0) for x in PRONOUN.finditer(text)]
            if pronouns:
                rows.append({'member':name,'text':text,'pronouns':pronouns})

REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text(json.dumps({'candidate_count':len(rows),'candidates':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
NOTE.parent.mkdir(parents=True,exist_ok=True)
lines=['# Cosmic Parent + masculine-pronoun focused audit — 2026-09-12','',f'Candidate paragraphs: **{len(rows)}**.','', 'This is a focused review list. A paragraph is included when it contains both `Cosmic Parent` and one of `he/him/his/himself`; the pronoun may still refer to Yeshua or another human character, so every item requires antecedent review.','']
for r in rows:
    lines.append(f"- `{r['member']}` — {r['text']}")
NOTE.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'candidate_count':len(rows)},indent=2))
