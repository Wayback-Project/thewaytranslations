# EPUB Refresh Instructions

## Canonical electronic authority

By editor direction for the September 2026 release line, `current-form-documents/the-way-current.epub` is the authoritative electronic reading edition. The files under `original-documents/` are older working sources and must not be used to overwrite the current-form EPUB unless a later explicit reconciliation decision says otherwise.

There is one current whole-Bible artifact in this directory: `the-way-current.epub`. Older instructions referring to a separate `newtestament.epub` are obsolete.

## Release procedure

1. Begin from the current canonical EPUB.
2. Make only editor-approved changes and maintain an exact before/after ledger.
3. Archive the prior EPUB under `rendered-documents-history/<YYYY-MM-DD_HHMMUTC>/` before replacement.
4. Validate ZIP integrity, `mimetype` placement/compression, 66 canonical books, 1,189 chapters, verse inventory, XML, internal links/anchors, and terminology/formatting checks.
5. Record the actual SHA-256 of the finished binary in this directory's README and the repository README.
6. Append the archive transaction to `rendered-documents-history/LOG.md`.
7. Synchronize downstream readers from the exact finished EPUB; do not maintain a separate hand-edited Bible text in the reader.

## 2026-09-10 consistency release

The completed whole-Bible divine-pronoun consistency release contains **1126** reviewed verse-level edits. Canonical SHA-256: `71a0b125ed27706bd4318d075d53e249388ed5a36fdc5f0a2d754a8e0ea1ada5`. See `../editor-notes/consistency/2026-09-10-whole-bible-divine-pronouns.md` and `../change-logs/reports/2026-09-10-whole-bible-divine-pronoun-consistency.json`.

The prior canonical artifact (SHA-256 `04722fbaeb2b5394df83a4a4c9056a7edc6dfe4f00b0d4ccc8630880bb69eb15`) is archived at `../rendered-documents-history/2026-09-10_0352UTC/the-way-current.epub`.

Current `<<` / `>>` formatting artifact count in the canonical EPUB is **0**.

## Existing terminology carried forward

The September 2026 release line also carries forward the accepted source-sensitive terminology rule: `satan` / `ha-satan` / `Satanas` → **the Adversary**; `diabolos` → **the Slanderer**; `daimonion` remains **demon**. Earlier Yeshua-sayings work already present in the current-form EPUB is preserved unchanged except where a verse is listed in the exact consistency ledger.
