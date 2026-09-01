# YHWH / Elohim / God Harmonization Matrix

Created: 2026-04-08 UTC
Updated: 2026-09-01 UTC
Status: Active policy matrix for transparent naming decisions

## Goal
Keep source-name fidelity while avoiding inconsistent drift across OT/NT tracks.

## Core rules
- Preserve source names where recoverable and contextually clear.
- Do not flatten `YHWH` and `Elohim` into one label by default.
- **Cosmic Parent is not a generic divine name.** Use it only for explicit divine Father/parent language or a documented Father relationship.
- Do not expand a pronoun referring to `YHWH`, `Elohim`, or `God` into Cosmic Parent unless the underlying wording itself identifies God as Father.

## Matrix

| Corpus zone | Source priority | Preferred rendering | Father/parent rule |
|---|---|---|---|
| Torah / Prophets / Writings (Hebrew-first OT) | Hebrew | `YHWH`, `Elohim`, `El`, etc. preserved | Use Cosmic Parent only where the Hebrew actually presents divine father/parent language. |
| Aramaic OT passages | Aramaic | Preserve the supported Aramaic divine title | Keep source distinction; do not substitute Cosmic Parent for a generic divine title. |
| Gospels / sayings-heavy NT | Aramaic-resonance posture + Greek check | `Elohim` generally preferred for ordinary divine God-language | Explicit `pater`/Father may be Cosmic Parent. Preserve `Abba` where attested. |
| Acts | Mixed | `Elohim` in Semitic-context lines; `God` allowed in Greek-formulaic speech | Explicit Father language may be Cosmic Parent; ordinary God-language is not. |
| Pauline-and-later NT | Greek-critical | `God` default for ordinary `theos` in Greek-grounded lines | Explicit divine `pater` may be Cosmic Parent; `theos` alone remains God. |

## Abba rule
- Preserve `Abba` only where attested: Mark 14:36, Romans 8:15, Galatians 4:6.
- Each NT occurrence is paired with Father language, so the English resonance may retain both: `Abba, Cosmic Parent` or equivalent punctuation.

## Style guardrails
1. Never replace explicit `YHWH` with `LORD` in this project.
2. When `Elohim` is chosen in NT, ensure it is intentional and track-based, not accidental carryover.
3. Where `God` is retained in Greek-grounded late NT, treat that as source-track fidelity, not doctrinal flattening.
4. Never use Cosmic Parent merely to avoid a masculine pronoun for God.
5. Human kinship father references remain `father` rather than Cosmic Parent.

## QA checks
- Report counts of `YHWH`, `Elohim`, `God`, `Cosmic Parent`, `Father`, and `Abba` by corpus file.
- Flag every `Cosmic Parent` occurrence for source-language Father/parent confirmation.
- Flag `Cosmic Parent` in a verse whose underlying divine noun is only `YHWH`, `Elohim`, or Greek `theos`.
- Flag human father references changed to Cosmic Parent.
- Confirm the three genuine NT `Abba` occurrences remain present and no additional ones are introduced.
