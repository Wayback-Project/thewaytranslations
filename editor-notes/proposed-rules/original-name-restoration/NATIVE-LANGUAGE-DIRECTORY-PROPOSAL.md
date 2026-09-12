# Native-Language Original-Name Directory Proposal — 2026-09-12

**Status:** Proposed; editorial review required. **No Scripture wording or canonical EPUB bytes are changed by this proposal.**

## Proposal

Add and maintain a machine-readable original-name/place proposal directory in the canonical translation repository so every candidate restoration can carry its own source-language evidence before any replacement release is attempted.

The directory is:

[`editor-notes/proposed-rules/original-name-restoration/directory/`](directory/README.md)

It currently contains **69 scoped proposal records** covering:

- priority person names;
- priority place/city names;
- the systematic `Beth ...` → `Beit ...` place-name review family;
- reader-guide-only restored forms;
- known conventional-form consistency remnants; and
- the `YAHWEH` → `YHWH` normalization review item.

## Why add native-language data now

A future replacement script should not have to guess why a spelling was chosen. Recording native forms at the proposal stage gives the reviewer and later release tooling the evidence needed to distinguish:

- a Hebrew Bible identity from a later Greek textual form;
- an Aramaic/Peshitta witness from a Greek NT witness;
- a display transliteration from the native script itself;
- one person from another person sharing the same conventional English name;
- a person name from a book title or ordinary English word; and
- an intended restoration from an exception that should remain conventional.

This also future-proofs the canonical metadata for optional reader features such as native-script popovers, pronunciation research, familiar-name aliases, source-witness comparison, and Aramaic-priority metadata for Yeshua sayings.

## Source-language policy

The proposal follows the repository's existing source-priority framework:

- **Hebrew Bible:** Hebrew native-script form first where the biblical source is Hebrew; Aramaic where the biblical source passage itself is Aramaic.
- **New Testament generally:** retain Greek and Aramaic/Peshitta witness information where useful; later Greek-grounded writings may use Greek as the primary textual witness under the existing methodology.
- **Direct speech attributed to Yeshua:** for original-language metadata attached to a word, name, or place inside the saying, prefer an attested **Aramaic/Peshitta** form in **Syriac script** when available. Do not delete the Greek/Hebrew witness fields.

The Yeshua-speech preference implements the project's existing Aramaic-priority track for Gospels/core sayings. It does **not** claim that the surviving Syriac spelling is guaranteed verbatim first-century Galilean orthography or pronunciation. That caution is required by the existing `skill/SKILL.md` guardrail against presenting speculative reconstructions as certainty.

Examples encoded in the manifest:

- Yeshua: `ܝܫܘܥ`
- Sedom/Sodom in a Yeshua saying: `ܣܕܘܡ`
- Amora/Gomorrah in a Yeshua saying: `ܥܡܘܪܐ`

The Michael proposal also stores multiple witnesses together rather than flattening them:

- Hebrew: `מיכאל`
- Greek: `Μιχαήλ`
- Aramaic/Peshitta proposal witness: `ܡܝܟܐܝܠ` — marked to re-verify before release.

## Directory contract

Every record can include:

- stable `id`;
- current literal form(s);
- proposed Way Version display form;
- practical pronunciation cue;
- person/place/divine-name category;
- one or more native forms with language, script, transliteration, witness label, and verification status;
- default and Yeshua-speech language preference;
- representative references;
- explicit exclusions and collision notes.

Representative references are **guidance**, not an exhaustive replacement ledger.

## Diagnostic tooling

Add `tools/local/audit_proposed_original_names.py` as a read-only finder. It loads the directory manifest, scans the canonical EPUB, counts literal current/proposed forms, and emits Markdown/JSON occurrence reports.

The tool is intentionally incapable of rewriting the EPUB.

Its output is a candidate review set only. A literal hit is not an editorial decision.

## Required step before actual replacement

Before any name/place change is released:

1. run the finder against the then-current canonical EPUB;
2. classify every hit by identity and context;
3. re-verify the proposed display spelling and native-script witness for that exact reference;
4. record exceptions and false positives;
5. create an exact before/after ledger with reviewer status;
6. write a separate release tool that consumes only the approved ledger;
7. archive the prior EPUB and run the normal full canonical QA;
8. record the actual release in `editor-notes/consistency/`, `change-logs/`, and `rendered-documents-history/LOG.md`;
9. synchronize downstream readers only after canonical QA passes.

## Hard guardrails

- The proposal directory itself must never be treated as an auto-replacement map.
- `Beth` must never be globally replaced; only full reviewed place names may be changed.
- Book titles such as Luke, Jonah, Hosea, or Nehemiah are excluded unless a separate book-title decision is approved.
- `Abram` → `Avram` is scoped to the pre-Genesis-17:5 name; it must not undo `Avraham` after the renaming.
- `Syria` → `Aram` is context-sensitive and cannot be a blanket string replacement.
- Native-language metadata must retain alternate witnesses when relevant rather than pretending one surviving witness erases the others.
- Peshitta/Syriac metadata must be described as a textual witness, not certain verbatim historical speech.

## Release effect of this proposal

- Scripture verses changed: **0**
- Canonical EPUB replaced: **no**
- Canonical checksum changed: **no**
- Prior EPUB archive required: **no**
- Actual replacement authorization: **no**

This proposal is the structured preparation stage for the later editorial replacement release.
