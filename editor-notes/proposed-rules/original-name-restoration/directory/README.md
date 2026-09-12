# Proposed Original-Name / Place Directory — 2026-09-12

**Status: proposal metadata only. Nothing in this directory changes Scripture.**

This directory is the machine-readable lead-up to a future original-name consistency release. It gives the audit/replacement tooling a stable list of candidate identities, current literal forms, proposed Way Version forms, source-language/native-script evidence, pronunciation cues, examples, and collision rules without turning those proposals into automatic edits.

The canonical Scripture artifact remains `current-form-documents/the-way-current.epub`.

## Why this directory exists

The earlier original-name pass proved that reference-specific edits can be released safely, but it also showed that a small remembered list is not enough. Names such as Michael and a wider set of people/places remain conventional or mixed, while reader metadata needs the same approved identity information for pronunciation and familiar-name search.

The goal is therefore to maintain one reviewable proposal directory that can later produce an exact occurrence inventory and, only after editorial approval, a before/after ledger for a canonical release.

## Files

- `manifest.json` — policy, source-language rules, audit contract, entry count, and file inventory.
- `priority-people.json` — highest-priority person-name proposals.
- `priority-places.json` — highest-priority place-name proposals.
- `beth-beit-a.json` / `beth-beit-b.json` — systematic full-place-name review for genuine `Beth ...` compounds; never a global `Beth` replacement.
- `reader-guide-only.json` — already-restored forms needing alias/pronunciation/native-language metadata but no Scripture wording change from this proposal.
- `consistency-backlog-a.json` / `consistency-backlog-b.json` — existing traditional-form remnants and related consistency items, including `Jesus` → `Yeshua`, `Babylon` → `Bavel`, `Nazareth` → `Natzeret`, and `YAHWEH` → `YHWH` review.

The manifest currently declares **69 entries**.

## Record model

Each entry includes:

- `id` — stable proposal identity.
- `category` — person, place, divine-name, etc.
- `currentForms` — literal forms the diagnostic finder may look for.
- `proposedForm` — proposed Way Version display spelling; still unapproved unless separately accepted.
- `pronunciationDisplay` — practical reader cue.
- `proposalGroup` / `editorialStatus` — workflow classification.
- `nativeForms[]` — one or more source/witness forms with:
  - `language`
  - `script`
  - `native`
  - `transliteration`
  - `witness`
  - `verificationStatus`
- `originalLanguagePreference` — default witness plus the special Yeshua-speech rule where applicable.
- `exampleReferences` — representative places to help an audit script/editor recognize the identity. These are examples, not necessarily the complete replacement list.
- `matchGuidance` — exact matching notes, exclusions, collision warnings, and scope rules.

## Native-language policy

### Hebrew Bible

Use the Hebrew native-script form by default when the source passage is Hebrew. Where the biblical source passage itself is Aramaic, use the Aramaic form appropriate to that source passage.

### New Testament generally

Preserve both Greek and Aramaic/Peshitta witness information when it helps the editorial decision. Under the existing project methodology, later writings with strong Greek textual grounding may use Greek as their primary source witness while still documenting an Aramaic witness when relevant.

### Direct speech attributed to Yeshua

For **original-language metadata attached to a word, name, or place inside direct speech attributed to Yeshua**, the proposal preference is:

1. use an attested **Aramaic/Peshitta** form as the preferred original-language metadata;
2. store it in **Syriac script**;
3. keep Greek and/or Hebrew witness forms alongside it when relevant rather than deleting them.

Examples already encoded in `manifest.json` include:

- Yeshua — `ܝܫܘܥ`
- Sedom/Sodom in a Yeshua saying — `ܣܕܘܡ`
- Amora/Gomorrah in a Yeshua saying — `ܥܡܘܪܐ`

This is a **project source-priority rule**, not a claim that the surviving Syriac spelling is certain verbatim first-century Galilean orthography or pronunciation. The repository's existing methodology already warns against presenting speculative reconstruction as certainty. See `skill/SKILL.md` and `editor-notes/research/STRATEGY-LAMSA-PRIMACY-TOP-50.md`.

## Examples

A Michael record preserves multiple relevant witnesses instead of flattening them:

```json
{
  "id": "michael",
  "currentForms": ["Michael"],
  "proposedForm": "Mikha'el",
  "nativeForms": [
    {"language": "Hebrew", "native": "מיכאל"},
    {"language": "Greek", "native": "Μιχαήλ"},
    {"language": "Aramaic", "script": "Syriac", "native": "ܡܝܟܐܝܠ"}
  ],
  "exampleReferences": ["Daniel 10:13", "Jude 1:9", "Revelation 12:7"]
}
```

A context-sensitive record can carry guards. `Abram` → `Avram`, for example, is limited to the identity before the Genesis 17:5 renaming; it must never cause `Avraham` after that point to be rewritten back to `Avram`.

Book-title collisions are also explicit: person references to Luke/Lukas, Jonah/Yonah, Hosea/Hoshea, or Nehemiah/Nechemyah do **not** authorize automatic renaming of the biblical book title.

## Diagnostic finder

`tools/local/audit_proposed_original_names.py` reads `manifest.json`, loads every listed JSON set, scans the canonical EPUB, and writes:

- `change-logs/reports/PROPOSED-ORIGINAL-NAME-DIRECTORY-AUDIT.md`
- `change-logs/reports/PROPOSED-ORIGINAL-NAME-DIRECTORY-AUDIT.json`

Run from repository root:

```bash
python3 tools/local/audit_proposed_original_names.py
```

The tool is intentionally read-only with respect to Scripture. It reports literal current/proposed hits so editors can classify them.

## Required path to an actual replacement release

1. Run the diagnostic finder against the then-current canonical EPUB.
2. Review every hit by identity and context.
3. Re-verify every proposed display spelling and every native-script source form against the relevant witness.
4. Mark false positives and intentional exceptions explicitly.
5. Convert only accepted hits into an exact before/after ledger containing reference, before text, after text, identity ID, native-source evidence, scope decision, and reviewer status.
6. Build a separate release tool that consumes only that approved ledger—not this proposal directory directly.
7. Archive the prior canonical EPUB and run the repository's normal full EPUB QA.
8. Record the release in `editor-notes/consistency/`, `change-logs/`, and `rendered-documents-history/LOG.md`.
9. Only after canonical QA passes should downstream readers regenerate from the exact released artifact and approved metadata.

## Hard guards

- No global search/replace from this directory.
- No automatic change merely because a literal token matches.
- No hand-editing generated downstream Scripture.
- No book-title rename without a separate approved policy.
- No loss of alternate textual-witness metadata just because one witness is preferred for display/source guidance.
- No claim that a Peshitta/Syriac form proves exact historical pronunciation.

## Proposal rationale

Adding the native spelling now makes the eventual release easier to audit and future-proofs the data for reader features such as source-language popovers, pronunciation work, source-witness comparison, and Aramaic-priority metadata for Yeshua sayings. Keeping the data in a proposed canonical editorial directory also prevents the web/mobile readers from becoming independent authorities for translation identity.
