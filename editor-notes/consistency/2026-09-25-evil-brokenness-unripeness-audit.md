# Whole-Bible `evil` → brokenness / contextual-language audit — proposal only

**Status:** non-canonical proposal. Do not sync this file downstream and do not modify the canonical EPUB until the individual rows are explicitly reviewed and approved.

**Canonical baseline EPUB SHA-256:** `edd3182ff57b54471505189628b82238c85d2d9c8b4edbba14339695eac827cd`

## Scope

- Exact extraction of all 31,102 canonical verses found 124 verses containing the standalone English word `evil`.
- All 124 are in the Old Testament.
- All 124 were introduced or retained by the 2026-09-14 audited `brokenness` cleanup ledger.
- The current New Testament contains zero standalone `evil` verses.
- This proposal recommends changing all 124, but **not** by one global replacement.

## Editorial rule

Use `brokenness` where the verse needs the project’s abstract moral/conceptual noun. Use `broken` where English grammar needs an adjective or predicate adjective. Use concrete contextual language such as `harm`, `wrong`, `wrongdoing`, `adversity`, `trouble`, `calamity`, or `disaster` where the verse is describing injury, an adverse event, judgment, or an action rather than an abstract moral category. `Unripe` / `unripeness` remain available concepts for later row-level editorial review, but this first pass does not force them into contexts where the English becomes less natural.

## QA gates for eventual approval

Every approved row must pass all of these before release:

1. Exact before/after verse match against the canonical baseline.
2. No unapproved global substitution.
3. Sentence-initial capitalization after `.`, `?`, `!`, quotation marks, or parentheses.
4. Article/form agreement (`a`/`an`, noun vs adjective), including guards against forms such as `brokenness plans`.
5. No doubled spaces, spaces before punctuation, or replacement-induced punctuation damage.
6. Whole-Bible 66-book / 1,189-chapter / 31,102-verse inventory unchanged.
7. EPUB ZIP, XML, internal-link, and anchor validation unchanged from the normal release methodology.
8. Regenerate the public mobile fallback and all downstream reader/search/name-linking content from the finished canonical EPUB only after approval.

## Known grammar regressions addressed in the proposal

- Psalm 5:4: sentence-initial lowercase `evil` → `Brokenness`.
- Psalm 34:21: verse-initial lowercase `evil` → `Brokenness`.
- Ezekiel 38:10: `an evil plan` → `a harmful plan` (article agreement).
- Malachi 2:17: adjacent `they delights` → `they delight` so the proposed verse is grammatically clean.

The row-by-row ledger is `tools/local/proposed_evil_brokenness_unripeness_2026_09_25.tsv`. `reviewed` and `approved` are intentionally unchecked for every row.
