# Original-language directory proposal record — 2026-09-12

**Record type:** Proposal / audit-preparation only. **No Scripture text or canonical release artifact was changed by this work.**

## Baseline canonical artifact

- Canonical Scripture: `current-form-documents/the-way-current.epub`
- Canonical Scripture release commit before proposal-only documentation work: `0279d393d34d5e3d8341c2c50c14e1faec7bb2f4`
- Canonical EPUB SHA-256: `8c41b165e7714730a4139ccee13c00b3c6e149af1e8ee5f00d4b8d5191bd5328`
- Coverage: 66 books / 1,189 chapters

The commits created for this proposal add only Markdown/JSON proposal metadata and a read-only audit tool. They do not replace the canonical EPUB.

## New proposal artifacts

- `editor-notes/proposed-rules/original-name-restoration/NATIVE-LANGUAGE-DIRECTORY-PROPOSAL.md`
- `editor-notes/proposed-rules/original-name-restoration/directory/README.md`
- `editor-notes/proposed-rules/original-name-restoration/directory/manifest.json`
- `editor-notes/proposed-rules/original-name-restoration/directory/priority-people.json`
- `editor-notes/proposed-rules/original-name-restoration/directory/priority-places.json`
- `editor-notes/proposed-rules/original-name-restoration/directory/beth-beit-a.json`
- `editor-notes/proposed-rules/original-name-restoration/directory/beth-beit-b.json`
- `editor-notes/proposed-rules/original-name-restoration/directory/reader-guide-only.json`
- `editor-notes/proposed-rules/original-name-restoration/directory/consistency-backlog-a.json`
- `editor-notes/proposed-rules/original-name-restoration/directory/consistency-backlog-b.json`
- `tools/local/audit_proposed_original_names.py`
- updated `editor-notes/proposed-rules/2026-09.md`

## Directory inventory

The manifest declares **69 proposal records**. The records cover priority people, priority places, `Beth`/`Beit` place compounds, reader-guide-only entries, conventional-form consistency remnants, and the `YAHWEH`/`YHWH` normalization review.

Each record is designed to carry:

- stable identity ID;
- current form(s) that a diagnostic finder may locate;
- proposed display form;
- pronunciation cue;
- source language and script;
- native-script spelling;
- textual-witness label and verification status;
- representative references;
- scope/collision instructions; and
- optional Yeshua-speech original-language preference.

## Yeshua-speech source-language proposal

The manifest proposes that original-language metadata attached to words, names, or places **inside direct speech attributed to Yeshua** prefer an attested Aramaic/Peshitta form in Syriac script when available, while preserving Greek and/or Hebrew witness fields.

This follows the repository's existing Aramaic-priority track for Gospels/core Yeshua sayings. It is a project editorial-source preference, not a claim that the surviving Syriac spelling proves the exact first-century spoken orthography or pronunciation.

Examples stored in the manifest include:

- Yeshua — `ܝܫܘܥ`
- Sedom/Sodom — `ܣܕܘܡ`
- Amora/Gomorrah — `ܥܡܘܪܐ`

## Reader-trial correction carried into the text-version handoff

The web-reader glossary trial surfaced one identity correction that must also be present in the human text-version update document:

- **Acts 1:23, 26 — `Mattityah` → familiar/traditional English alias `Matthias`.**
- Do **not** identify this Acts 1 person as `Mattithiah` or `Mattathias`; those names refer to different traditional identity/form conventions.
- The Way Version Scripture wording `Mattityah` is **not** being changed by this proposal. This is an alias/metadata and handoff correction so the text-version review and downstream reader directory stay aligned.

## Diagnostic tool behavior

`tools/local/audit_proposed_original_names.py` is diagnostic only. It:

1. loads the manifest and all listed JSON entry sets;
2. validates manifest entry count and duplicate IDs;
3. scans the canonical EPUB for literal current and proposed forms;
4. records references/text for candidate hits; and
5. writes Markdown and JSON audit reports.

It contains no Scripture write/replace operation.

## Required gate before any replacement

A future release must not consume the proposal directory as a direct replacement map. Editors must first:

1. run the diagnostic audit against the current canonical EPUB;
2. classify every hit by identity/context;
3. verify the proposed display form and native source form for the exact reference;
4. record false positives and intentional exceptions;
5. create an explicit human-approved before/after ledger; and
6. build any replacement/release tool to consume only that approved ledger.

The normal archive, checksum, EPUB integrity, coverage, link, verse, terminology, and collision QA then remains required before a canonical release.

## Release effect

- Scripture wording changed: **0 verses**
- Canonical EPUB replaced: **no**
- Canonical EPUB checksum changed: **no**
- Prior EPUB archive required: **no**
- Replacement script created: **no**
- Read-only diagnostic finder created: **yes**
- Proposal records created: **69**

## Reviewer status

**Proposed; not yet accepted as a translation rule and not yet authorized for canonical replacement.**
