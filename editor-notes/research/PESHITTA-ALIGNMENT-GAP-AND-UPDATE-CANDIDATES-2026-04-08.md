# Peshitta Alignment, Gaps, and Update Candidates

Created: 2026-04-08 UTC  
Purpose: map current Way One direction against major Peshitta-related research points, and identify update candidates for next pass.

## Source basis (research pass)

- Encyclopaedia Britannica summary on Peshitta antiquity and canon profile
- Peshitta overview references (including Syriac transmission profile and NT canon history)
- Lamsa-related modern reception context (support + criticism)

This is a working editorial research memo, not a final academic apparatus.

---

## Top 10 Peshitta differences: what aligns vs does not

### 1) NT source-priority claims (Aramaic primacy vs Greek critical)
- Peshitta-associated claim: Aramaic-origin emphasis.
- Current Way status: **Partially aligned** (Aramaic-primacy posture) but with explicit Greek-grounded exceptions in later NT zones.
- Gap: need clearer per-book source-track labels visible to readers.
- Update candidate: add a per-book `source-track` header in output metadata.

### 2) Early Syriac NT canon exclusions
- Early Syriac tradition omitted: 2 Peter, 2 John, 3 John, Jude, Revelation.
- Current Way status: **Intentionally non-aligned by design** (no-removal rule keeps full corpus).
- Gap: we should document this canon-layer distinction more visibly.
- Update candidate: add note block in README + book prefaces: "present in full corpus; early Syriac scope differed."

### 3) Semitic idiom preservation
- Peshitta strength: preserves Semitic idiom texture.
- Current Way status: **Aligned** (spoken-language orientation + anti-flattening).
- Gap: consistency uneven in some chapters.
- Update candidate: run chapter-level idiom audit for Matthew/Luke sayings clusters.

### 4) Repentance semantics (return/turn back)
- Peshitta-leaning effect: return/turn-back force.
- Current Way status: **Strongly aligned** (large-scale `repent*` normalization already done).
- Gap: keep regression checks.
- Update candidate: add automated grep guard in QA scripts for `repent*` residue.

### 5) Kingdom/reign language
- Peshitta-leaning interpretation: dynamic reign sense.
- Current Way status: **Partially aligned** (many places updated, not fully standardized).
- Gap: mixed `kingdom` vs `reign` wording still present.
- Update candidate: targeted pass in synoptics and Acts speeches.

### 6) Divine-name texture
- Peshitta tradition often preserves stronger Semitic naming signals than flattened English norms.
- Current Way status: **Aligned** in principle (YHWH/Elohim distinctions preserved).
- Gap: need clearer cross-corpus harmonization notes for readers.
- Update candidate: publish short public-facing name policy table from internal matrix.

### 7) John 1 expression language (Word/Logos/Memra trajectory)
- Peshitta-adjacent pressure: active expression rather than abstract doctrinal flattening.
- Current Way status: **Aligned with project decision** (`Living Creative Vibration` now in John 1 block).
- Gap: must clarify this is project-profile rendering choice, not uncontested lexical consensus.
- Update candidate: add short note in John preface: "profile translation term + rationale."

### 8) Assembly vs church institutionalization
- Peshitta/Aramaic-sensitive approach often resists later institutional over-translation.
- Current Way status: **Partially aligned**.
- Gap: still mixed in some NT sections.
- Update candidate: add lexicon check for `assembly/community/church` by context.

### 9) OT base relation (Hebrew-first with versional influence)
- Peshitta OT likely translated largely from Hebrew, with revisional/versional influence.
- Current Way status: **Aligned with caution** (Hebrew-first OT with comparative awareness).
- Gap: need sharper notes on where comparative witness influences wording.
- Update candidate: annotate high-impact OT divergences (Genesis, Isaiah, Psalms).

### 10) Devotional/interpretive expansion vs base translation
- Peshitta reception streams (and related modern interpreters) can move toward devotional expansion.
- Current Way status: **Controlled alignment** (base + resonance policy with transparency).
- Gap: ensure base line and resonance line are always clearly separated in output.
- Update candidate: enforce `Layer A / Layer B` labels in formatting templates.

---

## Potential word-level updates (candidate list)

These are candidate lanes to review in next pass (not auto-applied yet):

1. `kingdom` -> `reign` / `reigning presence` where Semitic dynamic sense is stronger.
2. `church` -> `assembly` / `community` where institutional back-projection is weak.
3. `word` in specific high-theology contexts -> project-approved active-expression wording (already applied in John 1 zone).
4. Ensure `turn back` / `relent` remains consistent where prior English used `repent*`.
5. Keep divine-name distinctions visible (`YHWH`, `Elohim`) unless a deliberate track-based exception is logged.

---

## Recommended next update pass (order)

1. NT sayings idiom consistency (Matthew/Luke first).
2. `kingdom/reign` consistency pass.
3. `assembly/church` consistency pass.
4. Public-facing canon-layer note for early Syriac NT scope differences.
5. Format-level enforcement of base/resonance separation.

---

## Editorial decision checkpoint for Mike

Please confirm priority order for next patch set:
- A) `kingdom -> reign` broad pass
- B) `church -> assembly` broad pass
- C) canon-layer explanatory notes only
- D) all of the above in staged sequence
