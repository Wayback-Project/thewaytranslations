# Romans structural mapping, malformed-English, and verse-record cleanup — 2026-09-15

## Scope

This is a narrow controlled correction release arising from the New Testament residual audit. It repairs the three approved malformed-English verses, restores coherent Romans doxology verse records, and removes one pre-existing duplicate Genesis verse paragraph discovered by release QA.

### Malformed English

- **Romans 5:19** — “through the one a person's disobedience” → “through the disobedience of one person.”
- **Romans 8:9** — “they are not their” → “they do not belong to Messiah,” preserving inclusive `anyone/they` while making the specific Messiah referent explicit.
- **Romans 14:2** — “One a person has faith…” → “One person has faith…”.

### Romans verse mapping

The previous EPUB had **432** Romans verse paragraphs rather than **433**. Romans 14:23 improperly contained parenthetical `(14:24)`, `(14:25)`, and `(14:26)` labels plus the closing doxology; Romans 16:25 was empty; Romans 16:26 contained `016:027`; and Romans 16:27 did not exist as its own paragraph.

This release restores Romans 14:23 to verse 23 only, places the already-present doxology wording into **Romans 16:25–27**, preserves **Romans 16:24** unchanged, and removes the `016:027` artifact. The manuscript tradition contains more than one placement for the closing Romans doxology; this release does not claim to settle that textual-critical question.

### Genesis 24:4 duplicate record

Release QA found one old duplicate verse paragraph in Genesis 24:4. The chapter contained both “my kin” and a second duplicate “my relatives” version. The project’s canonical unique-verse extraction already treated the first “my kin” paragraph as Genesis 24:4, and the earlier source file contains that first wording. This release removes only the second duplicate paragraph and preserves **“my kin”** as the canonical verse text.

## QA

- Previous EPUB SHA-256: `d48ec5b7da0db10c7c44c518793228dc5b2d69edc6e57de838486d2aefbcf62f`
- Released EPUB SHA-256: `edd3182ff57b54471505189628b82238c85d2d9c8b4edbba14339695eac827cd`
- Previous EPUB archived at `rendered-documents-history/2026-09-15_0843UTC/the-way-current.epub`
- Romans verse paragraphs: **432 → 433**
- New Testament unique verse paragraphs: **7,956 → 7,957**
- Raw search records: **31,102 → 31,102**; the old Genesis duplicate is removed as the missing Romans record is restored
- Duplicate verse references after release: **0**
- EPUB ZIP/XML/internal-link validation: **pass**
- Exact approved ledger: **8 / 8 pass**
- English article audit: **0 actionable mismatches**
- Canonical mobile fallback regenerated from the finished EPUB: **66 books / 1,189 chapters / 31,102 search records**

## Downstream rule

Website, web reader, EPUB downloads, mobile content feed, and native mobile release pin must consume this exact canonical EPUB. No downstream Scripture hand-editing.
