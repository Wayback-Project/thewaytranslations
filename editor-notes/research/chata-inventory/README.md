# Chata — complete English “sin” family occurrence inventory

**Status:** automated candidate triage / **UNREVIEWED** (no Scripture changes)  
**Audit date:** 2026-10-14 UTC  
**Audited canonical source SHA-256:** `58ccf8deb2f65ecaa0b35ce7b35137221c95998cee23d6461d98e250c297b4fc`  
**Method:** scanned only `verses[].text` from the 66 EPUB-generated files in `drafthead/waywebsitenetlify/app/data/books/`; each file's `sourceSha256` was checked against the index during ingestion. Did not scan doubled copies in `chapters[].text`, HTML, search indexes, and notes.

## Coverage and interpretation

- 66/66 books; 1,189 chapter inventory; 31,102 indexed verses in this source release.
- **863 exact whole-word, case-insensitive English term occurrences**, spread over **732 distinct verse references**.
- **Old Testament:** 583; **New Testament:** 280.
- Source-language alignment **has not** been done for each row, and the `suggested_direction` is an automatic triage suggestion, *not* final translation wording.
- Terms inspected: `sin`, `sins`, `sinned`, `sinning`, `sinner`, `sinners`, `sinful`, `sinfulness`, `sinfully`, and `sinless` where present. Non-lexical embedded substrings (for example in `single` and `since`) were excluded.
- **Proper names:** 4 uses of the wilderness/place name **Sin** are `PROPER_NAME`; **do not replace**.
- **Ritual compounds:** 124 **specific matched `sin` tokens in `sin offering` / `sin-offering` compounds**, not merely words co-occurring elsewhere in a ritual verse, are `RITUAL_OFFERING`, proposed for Hebrew/source review.
- The remaining 735 lexical instances include nouns, verbal and person-label cases, figurative usage, and substantives requiring manual syntactic disambiguation.

## Files

- [01-genesis-ruth.csv](./01-genesis-ruth.csv) — 228 occurrences
- [02-1-samuel-nehemiah.csv](./02-1-samuel-nehemiah.csv) — 135 occurrences
- [03-esther-jeremiah.csv](./03-esther-jeremiah.csv) — 137 occurrences
- [04-lamentations-amos.csv](./04-lamentations-amos.csv) — 73 occurrences
- [05-micah-matthew.csv](./05-micah-matthew.csv) — 26 occurrences
- [06-mark-galatians.csv](./06-mark-galatians.csv) — 170 occurrences
- [07-ephesians-titus.csv](./07-ephesians-titus.csv) — 13 occurrences
- [08-philemon-3-john.csv](./08-philemon-3-john.csv) — 76 occurrences
- [09-jude-revelation.csv](./09-jude-revelation.csv) — 5 occurrences

Each CSV row has `testament, book, chapter, verse, reference, matched_term, triage, suggested_direction, status, original_verse`. Repeated occurrences in one verse appear in separate consecutive rows; every row preserves its source verse. No generated rendering has been spliced into Scripture.

## Observed English surface forms

| Form | Matches |
|---|---:|
| `sin` | 446 |
| `sins` | 204 |
| `sinned` | 124 |
| `sinners` | 50 |
| `sinner` | 22 |
| `sinful` | 9 |
| `sinning` | 7 |
| `sinfulness` | 1 |
| **Total** | **863** |

## Machine triage classes

| Class | Count | Meaning |
|---|---:|---|
| `NOUN_OR_VERB` | 497 | Human source review required; plural vs verb ambiguity included |
| `PAST_VERB` | 124 | Review past verbal tense |
| `RITUAL_OFFERING` | 124 | Examine as offering term |
| `PERSON_LABEL` | 72 | Try action-centered English |
| `VERB` | 25 | Review finite verb construction |
| `ADJECTIVE_OR_ABSTRACT` | 10 | Review adjective or abstract sense |
| `PARTICIPLE` | 7 | Review aspect/tense |
| `PROPER_NAME` | 4 | Keep unchanged |

## Full 66-book coverage

| Book | Testament | Occurrences |
|---|---|---:|
| Genesis | OT | 10 |
| Exodus | OT | 22 |
| Leviticus | OT | 112 |
| Numbers | OT | 60 |
| Deuteronomy | OT | 18 |
| Joshua | OT | 3 |
| Judges | OT | 3 |
| Ruth | OT | 0 |
| 1 Samuel | OT | 21 |
| 2 Samuel | OT | 5 |
| 1 Kings | OT | 41 |
| 2 Kings | OT | 35 |
| 1 Chronicles | OT | 2 |
| 2 Chronicles | OT | 18 |
| Ezra | OT | 2 |
| Nehemiah | OT | 11 |
| Esther | OT | 0 |
| Job | OT | 16 |
| Psalms | OT | 43 |
| Proverbs | OT | 20 |
| Ecclesiastes | OT | 7 |
| Song of Solomon | OT | 0 |
| Isaiah | OT | 25 |
| Jeremiah | OT | 26 |
| Lamentations | OT | 7 |
| Ezekiel | OT | 36 |
| Daniel | OT | 9 |
| Hosea | OT | 14 |
| Joel | OT | 0 |
| Amos | OT | 7 |
| Obadiah | OT | 0 |
| Jonah | OT | 0 |
| Micah | OT | 7 |
| Nahum | OT | 0 |
| Habakkuk | OT | 1 |
| Zephaniah | OT | 1 |
| Haggai | OT | 0 |
| Zechariah | OT | 1 |
| Malachi | OT | 0 |
| Matthew | NT | 16 |
| Mark | NT | 16 |
| Luke | NT | 33 |
| John | NT | 27 |
| Acts | NT | 9 |
| Romans | NT | 60 |
| 1 Corinthians | NT | 15 |
| 2 Corinthians | NT | 5 |
| Galatians | NT | 5 |
| Ephesians | NT | 2 |
| Philippians | NT | 0 |
| Colossians | NT | 2 |
| 1 Thessalonians | NT | 1 |
| 2 Thessalonians | NT | 1 |
| 1 Timothy | NT | 5 |
| 2 Timothy | NT | 1 |
| Titus | NT | 1 |
| Philemon | NT | 0 |
| Hebrews | NT | 30 |
| James | NT | 8 |
| 1 Peter | NT | 8 |
| 2 Peter | NT | 3 |
| 1 John | NT | 27 |
| 2 John | NT | 0 |
| 3 John | NT | 0 |
| Jude | NT | 1 |
| Revelation | NT | 4 |

## Version and release warning

The canonical repository's `main` advanced while the inventory was being compiled, to SHA-256 `094be0ae8786e2e407515b5485946fc8ce35162fc4d0e62815b7983cf3ec4ffa` with a four-pronoun Romans follow-up. This inventory is reproducibly pinned to `58ccf8de...`, and the later website Romans JSON was spot-checked to still have **60** sin-family matches. **This spot-check is not a whole-Bible recertification:** compare/rerun all rows against the final main EPUB before changing Scripture.

## Editorial workflow

1. Confirm edition/release hashes and rerun scan on final release. Never aggregate `html`, `chapters[].text`, and `verses[].text` into one inflated word count.
2. For every row, identify source-language lemma, grammatical function, passage context, and image. Resolve `NOUN_OR_VERB` cases especially.
3. Write an **approved complete verse** candidate and rationale in a separate decision ledger, rather than interpreting these machine suggestions as replacements.
4. Retain literal geographical **Sin**, distinguish **purification offering** from wrongdoing, and document source challenges. Do not erase personification of wrongdoing.
5. Run tests for full-book coverage, verse anchors, per-verse diffs, reader search aliases, original vocabulary lookup, and canonical release/fallback consistency.
6. Proceed to EPUB/web/mobile release only after explicit editorial approval. The current branch is **documentation only**.

See [the full Chata proposal](../../consistency/2026-10-14-chata-sin-language-proposal.md).
