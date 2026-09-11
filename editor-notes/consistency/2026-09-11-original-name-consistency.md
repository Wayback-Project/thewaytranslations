# Original-name consistency and Genesis narrative wording — 2026-09-11

This release follows editor direction to complete obvious restored-name consistency and improve awkward early-Genesis references to the first man without flattening the Hebrew `adam` / `ha-adam` wordplay everywhere.

## Release

- Canonical source: `current-form-documents/the-way-current.epub`
- Prior SHA-256: `71a0b125ed27706bd4318d075d53e249388ed5a36fdc5f0a2d754a8e0ea1ada5`
- Current SHA-256: `8c41b165e7714730a4139ccee13c00b3c6e149af1e8ee5f00d4b8d5191bd5328`
- Prior artifact archived at `rendered-documents-history/2026-09-11_0559UTC/the-way-current.epub`
- Reviewed verse-level edits: **39**
- Affected canonical book files: **6**
- Coverage preserved: **66 books / 1,189 chapters**

## Name consistency

Established restored forms already present elsewhere in this edition were applied to their inconsistent references:

- **Qayin** for the Genesis person traditionally rendered Cain.
- **Hevel** for the Genesis person traditionally rendered Abel.
- **Noach** for the patriarch where four traditional `Noah` references remained.
- **Havvah** for Eve in 1 Timothy 2:13 and 2 Corinthians 11:3.
- **Chanokh** for Enoch where the traditional form remained in Genesis and 1 Chronicles.

This was reference-specific, not a global substitution. **Noah, daughter of Zelophehad, remains Noah.** `Abel` in place names such as Abel Meholah remains unchanged. `Tubal Cain` remains unchanged as a distinct compound name. `Seth` remains Seth because `Shet` is not an established form elsewhere in the current edition.

## Genesis wording

Genesis 2–4 was reviewed separately for `the human`, `the person`, `the man`, and `Adam`. Generic/formation contexts retain **the human** where it carries the Hebrew human/ground relationship; selected personal narrative contexts now use the more natural **the man**, and Genesis 4:1 uses **Adam** once the narrative has identified him personally. No blanket replacement was made.

## QA

The release builder required every ledger `before` value to match exactly once before writing. It then verified the 39 `after` values, preserved collision cases, EPUB ZIP/mimetype integrity, XML parsing, 66 canonical book XHTML members, 1,189 chapter anchors, internal links, and zero current `<<`/`>>` artifacts.

The exact before/after ledger is `change-logs/reports/2026-09-11-original-name-consistency.json`.
