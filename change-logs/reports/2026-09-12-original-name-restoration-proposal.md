# Original-name restoration proposal record — 2026-09-12

**Record type:** Proposal / review record only. **No Scripture text or canonical release artifact was changed by this record.**

## Baseline

- Canonical repository: this repository (`Wayback-Project/thewaytranslations`)
- Baseline canonical commit at proposal start: `0279d393d34d5e3d8341c2c50c14e1faec7bb2f4`
- Baseline canonical EPUB: `current-form-documents/the-way-current.epub`
- Baseline EPUB SHA-256: `8c41b165e7714730a4139ccee13c00b3c6e149af1e8ee5f00d4b8d5191bd5328`
- Baseline coverage: 66 books / 1,189 chapters

## Proposal

The detailed proposal is:

[`editor-notes/proposed-rules/original-name-restoration/README.md`](../../editor-notes/proposed-rules/original-name-restoration/README.md)

It proposes a canonical-first, reference-scoped process for reviewing and eventually correcting remaining conventional person/place names; generating pronunciation and familiar-name alias metadata from approved identities; auditing the mixed `Beth`/`Beit` place-name family; and preventing downstream generated readers from becoming independently edited Scripture sources.

Priority review examples include Michael → proposed `Mikha'el`; Ishmael → `Yishmael`; Jehoash → `Yoash`; Abijah → `Aviyah`; Amminadab → `Amminadav`; Nahshon → `Nachshon`; Sodom → proposed `Sedom`; Gomorrah → proposed `Amora`; Caesarea → proposed `Kaisareia`; Colossae → proposed `Kolosai`; and the remaining genuine `Beth ...` place names proposed for `Beit ...` normalization after exact occurrence classification.

## Release effect

- Scripture wording changed: **0 verses**
- Canonical EPUB replaced: **no**
- EPUB checksum changed: **no**
- Prior EPUB archive required: **no**
- Downstream reader synchronization required by this proposal record alone: **no**

## Required next steps before any implementation release

1. Editorially approve the restoration policy and exact spellings.
2. Generate an identity-aware occurrence ledger for the approved batch.
3. Review collision/context cases and record explicit exceptions.
4. Apply only approved reference-scoped changes.
5. Archive the then-current canonical EPUB under normal policy.
6. Rebuild and QA the canonical EPUB.
7. Create a release note under `editor-notes/consistency/` and an exact change ledger under `change-logs/reports/`.
8. Synchronize downstream readers only from the newly verified canonical artifact and approved metadata.

## Reviewer status

**Proposed; not yet accepted as a translation rule or released Scripture change.**
