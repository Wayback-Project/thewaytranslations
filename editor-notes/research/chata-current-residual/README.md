# Chata — CURRENT post-release residual terminology audit (15 October 2026)

**Status: whole-Bible English residual scan COMPLETE; Scripture decisions UNREVIEWED and NOT part of an approved release.**

## Exact current-source provenance

- **Canonical translation EPUB SHA-256:** `b5500415431a339ba10c7021e9b091b7af38f0badb2a4d9e1e7cc0e15f46b943`
- **Canonical commit:** `98f12a2ba1cdbf7d90ff492de212b459451452a6`
- **Verified Netlify reader:** `drafthead/waywebsitenetlify` `netlify`; generated `app/data/books/*.json` at the same EPUB hash, after the published first Chata wave.
- **Release evidence:** [54-verse canonical ledger and QA](../../../change-logs/reports/2026-10-15-chata-first-54-verse-release.json), [live Netlify + both OTA feed verification](https://github.com/drafthead/waywebsitenetlify/actions/runs/38615051278).
- The **prior** initial English audit had 863 matched tokens in 732 verses, pinned to an older October 14 reader snapshot. The verified 54-verse release removed 60 of those English terms (61 tokens in the affected before-verses, one remains in Psalm 32:5). The **post-release, fresh 66-book scan finds 803 tokens in 679 verses**, confirming the arithmetic independently.

## Current exact findings

| Category | Tokens | Human-action implication |
|---|---:|---|
| `NOUN_OR_VERB` | 294 | Context/syntax must distinguish abstract noun, command, infinitive, personified power |
| `PLURAL_OR_FINITE_VERB` | 174 | `sins` may mean plural moral failures **or** third-person singular `fails morally` |
| `PAST_VERB` | 122 | Try `failed morally`, `wronged`, or other source-sensitive action phrase |
| `PERSON_LABEL` | 68 | Prefer a description of actions/turning, not a permanent identity |
| `ONGOING_VERB` | 7 | Preserve verb tense/aspect and repeated harms |
| `ADJECTIVE_ABSTRACT` | 10 | Rewrite grammar instead of inserting a noun mechanically |
| `PURIFICATION_OFFERING` | 124 | Source-specific ritual `ḥaṭṭāʾt`, do not replace with “moral failure offering” |
| `GEOGRAPHIC_NAME` | 4 | Wilderness/place name **Sin** stays as written |
| **TOTAL** | **803** | **All decisions in these CSVs are unreviewed** |

- **Old Testament:** 572 remaining tokens; **New Testament:** 231.
- Surface forms: `sin` 422, `sins` 174, `sinned` 122, `sinners` 48, `sinner` 20, `sinning` 7, `sinful` 9, `sinfulness` 1.
- **675** terms remain after excluding the 124 technical ritual tokens and four geographic proper names. This number is **not 675 automatically approved replacements**.
- One verse changed in the first wave still contains an unreviewed second token: **Psalms 32:5**, “you forgave the iniquity of my sin.” A later review must consider preserving Hebrew distinctions between *iniquity/guilt* (`ʿavon`) and the moral-failure term (`ḥaṭṭāʾt`) rather than a simple word substitution. Do not silently fold this into a previously released 54-verse change.

## Nine complete current-release CSV inventories

| Range | English term occurrences |
|---|---:|
| [Genesis–Ruth](./01-genesis-ruth.csv) | 224 |
| [1 Samuel–Nehemiah](./02-1-samuel-nehemiah.csv) | 135 |
| [Esther–Jeremiah](./03-esther-jeremiah.csv) | 130 |
| [Lamentations–Amos](./04-lamentations-amos.csv) | 73 |
| [Micah–Matthew](./05-micah-matthew.csv) | 20 |
| [Mark–Galatians](./06-mark-galatians.csv) | 148 |
| [Ephesians–Titus](./07-ephesians-titus.csv) | 13 |
| [Philemon–3 John](./08-philemon-3-john.csv) | 57 |
| [Jude–Revelation](./09-jude-revelation.csv) | 3 |
| **Total** | **803** |

Every CSV has these fields: `testament`, `book`, `chapter`, `verse`, `reference`, `occurrence_in_verse`, `term`, `machine_triage`, `first_candidate`, `status` and `released_verse_text`. Every row is backed by the **newly released current reader**; all 66 book JSON files were checked for the exact source SHA. The review CSVs passed a second lexical parse of every source verse: **803/803 original token matches, zero duplicate-ordinal errors, all UNREVIEWED**.

## Source-sensitive next editorial gate

The editorial preference remains **moral failure / failed morally** where faithful; **failure** for an actual shortfall; and **wrongdoing / wronged** for direct harm, deliberate action, or destructive powers. Distinguish Hebrew `ḥṭʾ`, `ʿavon`, `peshaʿ`, `šegagah` and Greek `hamartia`, `hamartanō`, `hamartōlos`, `planē`, plus ritual uses and the place name. Do not assert that all of these literally mean “failure” or that all wrongdoing is accidental.

For a later translation wave, select exact **full-verse Current→Final** readings from these 803 candidates, record original-language/context justifications, review and approve a finite ledger, and rerun the canonical-first release workflow (archive → EPUB diff/QA → Netlify → both OTA feeds → mobile metadata → print Doc + new Word handoff). Never publish unreviewed CSV suggestions directly to Scripture or downstream JSON.
