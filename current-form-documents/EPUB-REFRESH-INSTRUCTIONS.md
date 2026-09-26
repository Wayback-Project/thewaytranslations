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

## 2026-09-14 English article grammar consistency

A whole-Bible `a`/`an` audit corrected **38** genuine English article-agreement errors while retaining **29** pronunciation-based exceptions. No theological or lexical wording was changed. Canonical SHA-256: `bfd2e746afdb810d4b0b35abf66fe71da394abee77099f9c8f481102ab242f53`. See `../editor-notes/consistency/2026-09-14-english-article-grammar-consistency.md` and `../change-logs/reports/2026-09-14-english-article-grammar-consistency.json`.

## 2026-09-14 Psalms and Proverbs inclusive human/divine pronouns

A source-sensitive reviewed release corrected **254** verse-level pronoun/inclusive-language inconsistencies in Psalms and Proverbs only. Actual male persons and male kinship/royal referents were preserved; Psalm 110:5–7 remains explicitly unresolved. Unmistakably divine masculine pronouns were replaced by the established divine name/title. Canonical SHA-256: `feb0a7ad83de3c31df389a61db02dda4b5eecf2655caaad7cda4be911df3f55a`. See `../editor-notes/consistency/2026-09-14-psalms-proverbs-inclusive-pronouns.md` and `../change-logs/reports/2026-09-14-psalms-proverbs-inclusive-pronouns.json`.

## 2026-09-14 Ecclesiastes inclusive language + Isaiah 1:16

A whole-book Ecclesiastes review corrected generic-human pronoun chains, unmistakable divine-pronoun remnants, and contextually inappropriate `brokenness` renderings. Source-marked male referents were preserved. Isaiah 1:16 was separately corrected to `Put away the harm of your doings ... Cease doing harm.` Canonical SHA-256: `0e66242a07b5303337f90078ae8639a1fca264031b63962fb109f79033e48c30`. See `../editor-notes/consistency/2026-09-14-ecclesiastes-inclusive-language-isaiah-harm.md` and `../change-logs/reports/2026-09-14-ecclesiastes-inclusive-language-isaiah-harm.json`.

## 2026-09-14 Lexicon update — prior AI wording cleanup

Finite 369-verse release repairing prior AI lexical flattening and 23 hand-reviewed generic-person pronoun chains. No heuristic divine-pronoun or broad masculine-term rewrites were included. Canonical SHA-256: `d48ec5b7da0db10c7c44c518793228dc5b2d69edc6e57de838486d2aefbcf62f`. See `../editor-notes/consistency/2026-09-14-lexicon-update-ai-cleanup.md` and `../change-logs/reports/2026-09-14-lexicon-update-ai-cleanup.json`.

## 2026-09-15 Romans structural mapping and malformed-English correction

Controlled release: corrected malformed English at Romans 5:19, 8:9, and 14:2; restored Romans 14:23 and Romans 16:25–27 to a coherent verse structure while preserving Romans 16:24 and the existing doxology wording; removed one pre-existing duplicate Genesis 24:4 paragraph while preserving the canonical “my kin” wording. NT unique verse paragraphs are now 7,957 / 7,957 and the 31,102 search records contain no duplicate verse references. Canonical SHA-256: `edd3182ff57b54471505189628b82238c85d2d9c8b4edbba14339695eac827cd`. See `../editor-notes/consistency/2026-09-15-romans-structural-cleanup.md` and `../change-logs/reports/2026-09-15-romans-structural-cleanup.json`.

## 2026-09-26 Direct evil → brokenness / broken release

Finite 124-verse canonical release from the approved whole-Bible terminology review. Only the lexical word `evil` was changed: noun/abstract slots → `brokenness`; adjective/predicate/substantive-adjective slots → `broken`. No contextual phrase rewrites. Canonical SHA-256: `6a3a0dbc91949b082fdcf7c93d0832fe6762440933d8528009cf44b2271dfb92`. See `../editor-notes/consistency/2026-09-26-evil-to-brokenness-direct-release.md` and `../change-logs/reports/2026-09-26-evil-to-brokenness-direct-release.json`.
