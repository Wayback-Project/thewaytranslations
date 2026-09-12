# Crucifixion inscription name/ethnonym alignment — 2026-09-12

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
