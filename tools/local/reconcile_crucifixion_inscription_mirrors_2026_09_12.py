#!/usr/bin/env python3
from pathlib import Path
import hashlib

ROOT=Path(__file__).resolve().parents[2]
EPUB=ROOT/'current-form-documents'/'the-way-current.epub'
EXPECTED='fb14e9bdf84c1eef9a67c135ae7c42edf070e3f39ea4b8a265fa4a4a9dc1129a'
CHANGES={
  'original-documents/matthew_restorative_translation.txt':(
    'THIS IS JESUS, THE KING OF THE JEWS.',
    'THIS IS YESHUA, THE KING OF THE JUDEANS.'),
  'original-documents/mark_restorative_translation.txt':(
    'THE KING OF THE JEWS.',
    'THE KING OF THE JUDEANS.'),
  'original-documents/luke_restorative_translation.txt':(
    'THIS IS THE KING OF THE JEWS.',
    'THIS IS THE KING OF THE JUDEANS.'),
  'original-documents/john_restorative_translation.txt':(
    'JESUS OF NAZARETH, THE KING OF THE JEWS.',
    'YESHUA OF NATZERET, THE KING OF THE JUDEANS.'),
}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
  if sha(EPUB)!=EXPECTED: raise SystemExit(f'canonical EPUB SHA changed unexpectedly: {sha(EPUB)}')
  applied=[]
  for rel,(before,after) in CHANGES.items():
    p=ROOT/rel; text=p.read_text(encoding='utf-8')
    if after in text and before not in text:
      applied.append((rel,'already-aligned')); continue
    count=text.count(before)
    if count!=1: raise RuntimeError(f'{rel}: expected one exact legacy inscription, got {count}')
    p.write_text(text.replace(before,after,1),encoding='utf-8')
    applied.append((rel,'updated'))
  note=ROOT/'editor-notes'/'consistency'/'2026-09-12-crucifixion-inscription-name-alignment.md'
  note.write_text('''# Crucifixion inscription name/ethnonym alignment — 2026-09-12

## Decision
The current canonical EPUB is already aligned with the released original-name policy; this transaction reconciles the older editable text mirrors so they cannot reintroduce stale forms downstream.

The inscription is not reconstructed as a single Aramaic sentence inside the English Scripture text. John 19:20 explicitly describes the title as written in Hebrew, Latin, and Greek. The English edition therefore translates the inscription content while applying the edition’s established name and ethnonym conventions: `Yeshua`, `Natzeret`, and `Judeans` for the relevant Greek `Ioudaioi` wording.

## Mirror corrections
- Matthew 27:37 — `THIS IS JESUS, THE KING OF THE JEWS.` → `THIS IS YESHUA, THE KING OF THE JUDEANS.`
- Mark 15:26 — `THE KING OF THE JEWS.` → `THE KING OF THE JUDEANS.`
- Luke 23:38 — `THIS IS THE KING OF THE JEWS.` → `THIS IS THE KING OF THE JUDEANS.`
- John 19:19 — `JESUS OF NAZARETH, THE KING OF THE JEWS.` → `YESHUA OF NATZERET, THE KING OF THE JUDEANS.`

## Artifact boundary
- Canonical EPUB bytes are intentionally unchanged by this mirror reconciliation.
- Canonical EPUB SHA-256 remains `fb14e9bdf84c1eef9a67c135ae7c42edf070e3f39ea4b8a265fa4a4a9dc1129a`.
- Final released-name audit found no stale released-name forms and no `Jesus` / `Nazareth` / `King of the Jews` inscription residue in the canonical EPUB.
''',encoding='utf-8')
  print('\n'.join(f'{s}: {r}' for s,r in applied))
if __name__=='__main__': main()
