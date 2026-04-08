# OT Full Pass Results + Remaining Changes (2026-04-08)

## What was wrong

1. Legacy `repent*` vocabulary remained across OT in both divine and human contexts.
2. Divine-title `Father` remained in a small set of OT divine-address lines.
3. No single auditable matrix existed for YHWH/Elohim/God handling.
4. No local automated QA report existed for name/gender consistency.

## What was changed in this pass

- Cleared remaining OT `repent*` forms via context-sensitive replacements:
  - divine action -> `relent/relented`
  - human return -> `turn back/turned back`
- Normalized OT divine-title `Father` lines to `Cosmic Parent` (human kinship forms preserved).
- Added harmonization matrix doc:
  - `editor-notes/research/YHWH-ELOHIM-GOD-HARMONIZATION-MATRIX.md`
- Added local OT QA script + outputs:
  - `tools/local/ot_name_gender_audit.py`
  - `change-logs/old-testament/reports/OT-NAME-GENDER-AUDIT-LATEST.md`
  - `change-logs/old-testament/reports/OT-NAME-GENDER-AUDIT-LATEST.json`

## Current status snapshot

- `repent*` in OT source files: **0**
- `Father` (uppercase divine-title form) in OT source files: **0**
- `LORD` fallback token in OT source files: **0**
- Ruach feminine marker still preserved in Genesis 1:2 (`Ruach ... she`).

## What still needs to be changed (explicit)

1. Build a verse-level protected list for feminine-force lines (Ruach/Wisdom zones).
2. Expand wisdom-personification consistency checks beyond simple term counting.
3. Continue resonance-layer rollout in OT passages where approved (base line + labeled resonance line).
