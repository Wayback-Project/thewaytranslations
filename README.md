# The Way Translation (Early Project)

> **This is a new project and several areas still need to be addressed.**
> What is here now is a starting point, and we welcome feedback, review, and collaboration as the project evolves.

## Current Version (Primary Link)

- Current EPUB: `current-form-documents/the-way-current.epub`

## Initial generation note

The initial repository draft was generated with AI (Codex GPT-5.3 profile) and is being iteratively reviewed and corrected through editor-guided workflow.

## Project Purpose

This repository is building a restorative Bible translation workflow that keeps source-language texture visible in English while producing practical export formats for publishing and distribution.

## Way One Direction (Current Editorial Policy)

The Way One currently follows an **Aramaic-primacy** restoration posture, with special attention to the spoken-language world behind the text.

Key commitments:
- prioritize language texture and oral force, not only later institutional renderings
- preserve and document major Aramaic-vs-Greek differences transparently
- **hard rule: do not remove text from the project corpus**
- for later writings with strong Greek textual grounding (for example, Pauline material), acknowledge that shift and use Greek-critical evidence as primary while still documenting Aramaic comparators

The repository currently includes:
- source text files in `original-documents/`
- current active outputs in `current-form-documents/`
- timestamped output history in `rendered-documents-history/`
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
   - Human-curated `.txt` source files are placed in `original-documents/`.
   - Files are organized in large canonical groupings (Torah/history/NT chunks, etc.) for manageable editing.

2. **Parsing & Normalization Transaction**
   - `tools/scripts/script.js` parses lines in `Book Chapter` + `Verse. text` format.
   - Book/chapter/verse content is normalized and merged into a consistent in-memory structure.

3. **Export Transaction(s)**
   - Publishing JSON export (`way-translation-publishing.json` shape).
   - Plain-text eBook export (`way-translation-ebook.txt` shape).
   - Book/chapter folder ZIP export for distribution pipelines.

4. **Render + Current Transaction**
   - The newest active render is written to `current-form-documents/` (current canonical output, EPUB-first).
   - Before replacing current output, the previous current output is copied into `rendered-documents-history/<UTC timestamp>/`.
   - Each history write is logged in `rendered-documents-history/LOG.md`.

This transaction model is intentionally lightweight right now and is expected to mature with validation, provenance tracking, and automated checks.

## Repository Structure (What’s in Each Folder and Why)

### `skill/`
- Contains `SKILL.md`, the translation behavior specification.
- Why: keeps the translation rules explicit, reusable, and reviewable.

### `original-documents/`
- Human-editable source translation text files.
- Why: this is the active drafting workspace before structured export.

### `tools/`
- Browser-based utility for loading source files and exporting transformed artifacts.
- `tools/scripts/index.html`: UI shell.
- `tools/scripts/script.js`: parsing, merge, normalization, and export logic.
- `tools/surreal-search/`: SurrealDB graph+vector+temporal search workflow.
- Why: gives a simple no-build workflow for exports and a fast local search stack for large-corpus retrieval.

### `current-form-documents/`
- Current active output set.
- Current policy: keep the latest whole-project EPUB here.
- Why: one stable location for the latest canonical render.

### `rendered-documents-history/`
- Timestamped history of prior renders.
- Each snapshot lives under UTC folder names like `YYYY-MM-DD_HHMMUTC/`.
- Includes `README.md` and `LOG.md` to track what changed and why.
- Why: preserves historical render traceability without requiring a database.

## Render Workflow (Required)

1. Edit source text in `original-documents/`.
2. Produce/update current render in `current-form-documents/`.
3. Before replacing current render, archive prior current render to `rendered-documents-history/<UTC timestamp>/`.
4. Append snapshot entry to `rendered-documents-history/LOG.md`.
5. Keep `current-form-documents/the-way-current.epub` as the primary user-facing artifact.

## Current Execution Framework

The project now uses a local, no-database documentation workflow for translation-change governance:

- `editor-notes/research/STRATEGY-LAMSA-PRIMACY-TOP-50.md` (top 50 focus strategy)
- `change-logs/new-testament/INDEX.md` (NT coverage and status)
- `change-logs/new-testament/books/*.md` (book-level log trail)
- `change-logs/new-testament/reports/NT-QA-LATEST.md` (generated QA table)
- `tools/local/nt_changelog_report.py` (local report generator)

Run locally:

```bash
python3 tools/local/nt_changelog_report.py
```

This writes:
- `change-logs/new-testament/reports/NT-QA-LATEST.md`
- `change-logs/new-testament/reports/NT-QA-LATEST.json`

## Surreal Search (Fast Local Retrieval)

For intent and exact search over the corpus, use the SurrealDB workflow:

- Guide: `tools/surreal-search/README.md`
- OpenClaw skill guide: `skills/openclaw-surreal-search/SKILL.md`
- Test results: `change-logs/new-testament/reports/SURREAL-SEARCH-TEST-RESULTS-2026-04-08.md`

This solves the practical problem of quickly answering questions like:
- "show 50 verses with Elohim"
- "where is YHWH used without Elohim"
- "who was the disciple who did X, and where"

Quick demo commands:

```bash
npm --prefix tools/surreal-search run ingest
npm --prefix tools/surreal-search run demo
npm --prefix tools/surreal-search run query -- "who was the disciple who denied and wept"
```

## Current Gaps / Areas to Address Next

Some high-value next steps:
- automated validation of verse ordering and completeness
- repeatable CLI build/export pipeline (in addition to browser tools)
- provenance metadata (source version, generator version, date, commit)
- QA checks for formatting drift across original documents
- contributor workflow hardening (templates, checks, review conventions)

## Collaboration Instructions (Standard)

We welcome constructive collaboration. To keep contributions clean and reviewable, please follow this baseline:

1. **Discuss first for major changes**
   - Open an issue describing goals, scope, and rationale before large structural updates.

2. **Keep PRs focused**
   - One logical change per pull request.
   - Include before/after examples when changing parsing or output format behavior.

3. **Preserve source integrity**
   - Do not silently rewrite large sections of `original-documents/` without documenting why.
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
