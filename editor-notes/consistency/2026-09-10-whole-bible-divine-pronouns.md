# Whole-Bible divine-pronoun consistency update — 2026-09-10

## Authority and scope

By editor direction, `current-form-documents/the-way-current.epub` is the authoritative electronic reading edition for this release. The older `original-documents/` files were **not** used to overwrite the current-form text. The supplied Edition 1.0 print PDF was used as a cross-check/reference only; it was not imported wholesale.

This is a **consistency update**, not a translation rewrite. Masculine pronouns were changed only when the immediate context made the referent unmistakably divine (YHWH, Elohim, God, Cosmic Parent, Ruach, or an already-established divine title). Human pronouns, pronouns referring to Yeshua or another named character, and uncertain/debated/poetic speaker transitions were retained. No `they`, `she`, or `it` substitutions were introduced for the divine referent, and no editorial comments were inserted into Scripture.

## Result

- Verse-level edits actually made: **1126**
- Affected canonical books: **51**
- Canonical EPUB SHA-256: `71a0b125ed27706bd4318d075d53e249388ed5a36fdc5f0a2d754a8e0ea1ada5`
- Previous canonical EPUB SHA-256: `04722fbaeb2b5394df83a4a4c9056a7edc6dfe4f00b0d4ccc8630880bb69eb15`
- Exact before/after ledger: `change-logs/reports/2026-09-10-whole-bible-divine-pronoun-consistency.json`
- QA report: `change-logs/reports/2026-09-10-whole-bible-divine-pronoun-qa.json`
- Prior EPUB archived at: `rendered-documents-history/2026-09-10_0352UTC/the-way-current.epub`

The Git diff plus the exact before/after ledger is the repository-equivalent change tracking for the binary EPUB release.

## Open editorial review — intentionally unchanged

- **Acts 5:32** — “His witnesses” has a referent/textual-basis question already carried from the Acts review.
- **Acts 13:35** — Citation speaker and psalm literary voice should not be silently collapsed.
- **Acts 20:28** — Assembly/Master/God/blood referents require separate textual review.
- **Exodus 34:28** — Speaker/reference transition makes the masculine pronoun insufficiently certain for this mechanical consistency pass.
- **Numbers 24:8** — The pronoun can reasonably refer to Israel rather than Elohim.
- **Psalm 110:5–7** — Royal/Messianic/divine referents are poetically and textually disputed; left unchanged.
- **Ezekiel 2:2** — Ruach and speaking-voice transition is not resolved silently.
- **Romans 15:10** — Quotation/speaker referent is not changed by this pass.
- **Hebrews 1:3** — God/Son language crosses referents; masculine pronouns referring to Yeshua are explicitly outside scope.

These are not failures of the consistency pass; they are cases where the supplied rule requires uncertainty to be preserved rather than silently resolved.

## Release QA

- EPUB ZIP integrity: pass; `mimetype` is first and uncompressed.
- Canonical coverage: **66 books / 1,189 chapters**.
- Verse inventory preserved: **31,102 occurrences / 31,101 unique references**. The pre-existing duplicate Genesis 24:4 remains untouched because it is outside this consistency task.
- XML parse errors: **0**.
- Broken internal links/anchors: **0**.
- Current `<<` / `>>` artifacts: **0**.
- Only the **51 affected canonical book XHTML members** changed inside the EPUB; all other EPUB members are byte-identical to the archived previous release.

## Reader synchronization

Website/e-reader synchronization is a separate downstream release transaction. The website must ingest this exact canonical EPUB and its `/app/version.json` SHA must match `71a0b125ed27706bd4318d075d53e249388ed5a36fdc5f0a2d754a8e0ea1ada5` before synchronization is considered verified.
