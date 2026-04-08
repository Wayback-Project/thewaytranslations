# The Way Translation (Early Project)

> **This is a new project and several areas still need to be addressed.**
> What is here now is a starting point, and we welcome feedback, review, and collaboration as the project evolves.

## Project Purpose

This repository is building a restorative Bible translation workflow that keeps source-language texture visible in English while producing practical export formats for publishing and distribution.

The repository currently includes:
- source working text files
- generated publication artifacts
- a browser-based export/conversion tool
- a translation skill prompt (`skill/SKILL.md`) that defines translation behavior

## What the Prompt (`skill/SKILL.md`) Does

The `skill/SKILL.md` file defines a **Historical-Restorative Bible Translator** behavior.

In short, it tells the translator to:
- prioritize earliest recoverable source-language meaning
- preserve names and distinctions (for example, divine names)
- avoid flattening ancient terms into later doctrinal/legalized defaults
- preserve meaningful gender and social context when textually supported
- output clear but ancient-feeling English
- keep speculative interpretation separate from secure translation evidence

It is effectively the project’s translation policy and style guide for how passages should be rendered.

## Translation Workflow Transactions

This project currently uses a simple transaction flow from source text to generated outputs:

1. **Source Input Transaction**
   - Human-curated `.txt` source files are placed in `working-documents/`.
   - Files are organized in large canonical groupings (Torah/history/NT chunks, etc.) for manageable editing.

2. **Parsing & Normalization Transaction**
   - `tools/scripts/script.js` parses lines in `Book Chapter` + `Verse. text` format.
   - Book/chapter/verse content is normalized and merged into a consistent in-memory structure.

3. **Export Transaction(s)**
   - Publishing JSON export (`way-translation-publishing.json` shape).
   - Plain-text eBook export (`way-translation-ebook.txt` shape).
   - Book/chapter folder ZIP export for distribution pipelines.

4. **Generated Artifact Transaction**
   - Outputs are written into `generated-documents/` (single-file exports and per-book/chapter files).

This transaction model is intentionally lightweight right now and is expected to mature with validation, provenance tracking, and automated checks.

## Repository Structure (What’s in Each Folder and Why)

### `skill/`
- Contains `SKILL.md`, the translation behavior specification.
- Why: keeps the translation rules explicit, reusable, and reviewable.

### `working-documents/`
- Human-editable source translation text files.
- Why: this is the active drafting workspace before structured export.

### `tools/`
- Browser-based utility for loading source files and exporting transformed artifacts.
- `tools/scripts/index.html`: UI shell.
- `tools/scripts/script.js`: parsing, merge, normalization, and export logic.
- Why: gives a simple no-build, local workflow for contributors.

### `generated-documents/`
- Generated outputs for downstream use.
- Includes:
  - consolidated publishing JSON
  - consolidated eBook plain text
  - per-book/per-chapter text layout under `generated-documents/books/`
- Why: separates generated artifacts from editable source drafts.

## Current Gaps / Areas to Address Next

Some high-value next steps:
- automated validation of verse ordering and completeness
- repeatable CLI build/export pipeline (in addition to browser tools)
- provenance metadata (source version, generator version, date, commit)
- QA checks for formatting drift across working documents
- contributor workflow hardening (templates, checks, review conventions)

## Collaboration Instructions (Standard)

We welcome constructive collaboration. To keep contributions clean and reviewable, please follow this baseline:

1. **Discuss first for major changes**
   - Open an issue describing goals, scope, and rationale before large structural updates.

2. **Keep PRs focused**
   - One logical change per pull request.
   - Include before/after examples when changing parsing or output format behavior.

3. **Preserve source integrity**
   - Do not silently rewrite large sections of `working-documents/` without documenting why.
   - Keep naming/format conventions consistent (`Book Chapter`, `Verse. text`).

4. **Document behavior changes**
   - If you change translation-policy behavior, update `skill/SKILL.md` and describe the reason in the PR.
   - If you change export shapes, document the new schema and migration impact.

5. **Review expectations**
   - Be respectful and evidence-based in feedback.
   - Prioritize textual accuracy, reproducibility, and clarity over personal preference.

6. **Commit hygiene**
   - Use clear commit messages.
   - Avoid committing temporary files or unrelated formatting churn.

## Feedback

If you want to collaborate, suggest improvements, or challenge assumptions, please open an issue or PR. Early feedback is especially valuable while the project architecture and standards are still forming.
