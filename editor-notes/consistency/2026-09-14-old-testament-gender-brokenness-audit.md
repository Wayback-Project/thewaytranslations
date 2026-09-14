# Old Testament inclusive-language / divine-pronoun / “brokenness” residual audit — 2026-09-14

Status: **diagnostic editorial handoff only — no Scripture changes authorized by this file.**

Canonical EPUB audited: `current-form-documents/the-way-current.epub`

Canonical EPUB SHA-256: `0e66242a07b5303337f90078ae8639a1fca264031b63962fb109f79033e48c30`

## Completeness

The final wrapper-aware audit extracted **23,145 / 23,145 Old Testament verses across all 39 books**. This matters because an earlier draft of the scanner skipped eight differently structured EPUB book files; that draft was rejected and is not the basis of this report.

Final mechanical inventory:

- 2,493 candidate rows total.
- 1,157 high-priority review rows.
- 1,336 lower-confidence/context-review rows.
- 347 `BROKENNESS LEXICAL REVIEW` rows.
- 437 `DIVINE-REFERENT REVIEW` rows.
- 360 `GENERIC PRONOUN HIGH PRIORITY` rows.
- 13 `GENERIC-HUMAN HIGH PRIORITY` rows.
- 143 secondary `GENERIC PRONOUN REVIEW` rows.
- 1,193 `MASCULINE TERM REVIEW` rows.

These are **candidate counts, not approved change counts**. Narrative male characters, explicitly male kinship, kings, husbands, sons, fathers, male warriors, and other genuinely male referents must remain male. Divine rows must be checked for coreference before any change. The broad masculine-term inventory intentionally over-includes specific men.

Full machine inventory:

- `audit-output/old-testament-gender-brokenness-2026-09-14/summary.json`
- `audit-output/old-testament-gender-brokenness-2026-09-14/candidates.tsv`
- `audit-output/old-testament-gender-brokenness-2026-09-14/high-priority.md`
- `audit-output/old-testament-gender-brokenness-2026-09-14/all-verses.tsv`

## Editorial rules for the next release

1. **Generic humanity:** legal, wisdom, proverbial, and universal statements should not become male-only English when the Hebrew/context addresses people generally. Use person/people/humanity or singular they when that preserves the source.
2. **Actual men stay men:** do not neutralize named male characters, actual husbands/fathers/sons, male royal figures, or source-significant male references.
3. **Divine masculine pronouns:** when `he / him / his / himself` unmistakably refers to YHWH, Elohim, God, or an established divine title, repeat the established divine name/title. Do not introduce divine `they`, `she`, or `it`. Preserve genuinely disputed poetic/royal referents.
4. **“Brokenness” is not a universal replacement for Hebrew evil/harm language.** Hebrew words in these rows carry different senses: wrong, harm, evil, calamity, misfortune, trouble, wickedness, deceit, iniquity, bad news, and other meanings. Choose the English word demanded by the local Hebrew and context.
5. **No global replacement.** Every change must be an exact verse-level editorial decision and then pass the existing article/grammar scanner.

## Recheck of books already updated

### Psalms

The earlier 254-verse Psalms/Proverbs pronoun release remains valuable; the present audit found a **separate lexical queue**, especially around `brokenness`. The audit shows 48 brokenness lexical rows, 4 divine-referent review rows, 1 strong generic-pronoun row, 3 generic-human rows, 10 secondary generic-pronoun rows, and 63 broad masculine-term rows.

Important items:

- **Psalm 112:7** — current: `They will not be afraid of brokenness news.` Hebrew `שְׁמוּעָה רָעָה` is bad/evil tidings. Recommended direction: **“They will not be afraid of bad news”** (or “troubling news”), while keeping the inclusive `they/their` already fixed.
- **Psalm 109:5** — current: `They have rewarded me brokenness for good`. This should be reviewed as harm/wrong/evil rather than the abstract noun “brokenness.”
- **Psalm 109:6** — current: `Set a broken person over him.` The Hebrew/context calls for a wicked/hostile person, not a “broken person.”
- **Psalm 119:115** — current: `people who act from brokenness`. Likely direction: people who do wrong / do harm / evildoers, depending final source-style decision.
- **Psalm 110:5–7** — still **preserve for explicit editorial review**. The scanner flags masculine/divine proximity, but this passage is intentionally not to be resolved mechanically because the royal/Messianic/divine referent is disputed.
- Broad `man/men` rows such as Psalms 118:6, 118:8, 119:113, and 119:134 should receive Hebrew/context review, but are not automatically changes.

### Proverbs

The pronoun release corrected many generic-person chains, but a distinct lexical cleanup remains. Current audit: 44 brokenness rows, 1 divine-referent review, 2 strong generic-pronoun rows, 1 generic-human row, 7 secondary generic-pronoun rows, and 48 broad masculine-term rows.

Highest-priority examples:

- **Proverbs 26:24** — current: `he harbors brokenness in his heart.` Hebrew `מִרְמָה` means **deceit**. Recommended direction: **“they harbor deceit within”** after the gender/coreference decision for the generic hater.
- **Proverbs 28:5** — current: `Brokenness men don't understand justice`. Hebrew `אַנְשֵׁי־רָע` is people/men of evil/wrong. Recommended inclusive direction: **“People who do wrong do not understand justice”** or equivalent.
- **Proverbs 29:6** — current: `A brokenness a person is snared by their sin`. This is both unnatural English and a lexical problem. Hebrew `אִישׁ רָע` is an evil/wicked person. Recommended inclusive direction: **“A person who does wrong is trapped by their transgression”** (final wording requires source-style review).
- **Proverbs 30:32** — current: `if you have thought brokenness`. Review toward **planned evil / planned harm / schemed wrongdoing** according to the Hebrew.
- The remaining generic `man/men` wisdom sayings should be source-checked one by one; do not change sex-specific family or narrative roles.

### Ecclesiastes

The whole-book pass is holding well. The only masculine-term row from this mechanical inventory is **Ecclesiastes 7:28**, where the verse explicitly contrasts `one man among a thousand` with `a woman`. That sex-specific contrast should **remain**, absent a separate source-critical decision. No new brokenness, divine-pronoun, or strong generic-pronoun residual was identified by this audit.

### Isaiah

Isaiah 1:16 was correctly improved to `Put away the harm of your doings ... Cease doing harm`, but the rest of Isaiah still needs a broader pass. Current inventory: 18 brokenness lexical rows, 32 divine-referent review rows, 26 strong generic-pronoun rows, 2 generic-human rows, 13 secondary generic-pronoun rows, and 54 broad masculine-term rows.

Immediate examples:

- **Isaiah 1:4** — current: `a seed of people who act from brokenness`. Hebrew `זֶרַע מְרֵעִים` is a brood/offspring of evildoers or people doing evil. Recommended direction: **“offspring of people who do harm/wrong”** or another source-faithful equivalent—not “act from brokenness.”
- **Isaiah 1:13** — current: `I can't bear with brokenness assemblies.` Hebrew has `אָוֶן וַעֲצָרָה`, iniquity/wrongdoing **and** assembly. Recommended direction: **“I cannot bear wrongdoing and solemn assembly”** or equivalent.
- **Isaiah 2:11, 2:17** — `man` is paired with broader human language and should be checked for a consistent humanity/people rendering.
- The 32 divine-referent rows need coreference review; many will be real divine-pronoun residuals, but proximity alone cannot authorize changes.

## Clear lexical pattern: “brokenness” has been overextended

The audit found **347** Old Testament verses containing suspicious `brokenness / broken ...` language. Not all 347 should change. Some theological uses may be intentional and meaningful—for example, the project may decide to retain a relational/moral “brokenness” rendering in selected `good and ...` passages. The problem is using the same English word for unrelated Hebrew senses.

Source-checked examples demonstrating the range:

- **Exodus 23:2** — `לְרָעֹת`: “to do wrong.” Current `do brokenness` should be revised toward **do wrong / do harm**.
- **Exodus 33:4** — `הַדָּבָר הָרָע`: bad/evil tidings. Current `brokenness news` should be **bad news / troubling news**.
- **Psalm 112:7** — `שְׁמוּעָה רָעָה`: bad/evil tidings. Current `brokenness news` should be **bad news** or equivalent.
- **Isaiah 1:13** — `אָוֶן וַעֲצָרָה`: iniquity/wrongdoing and assembly. `brokenness assemblies` collapses the grammar and should be revised.
- **Proverbs 26:24** — `מִרְמָה`: deceit. `harbors brokenness` is the wrong lexical value.
- **Proverbs 29:6** — `אִישׁ רָע`: an evil/wicked person. `A brokenness a person` is not viable English or a sound lexical rendering.

High concentrations of brokenness-review rows are in Jeremiah (70), Psalms (48), Proverbs (44), Deuteronomy (24), Genesis (18), Isaiah (18), 1 Samuel (17), Ezekiel (15), and Job (11). These books should be prioritized for the lexical phase.

## Generic-human / pronoun pattern across the rest of the Old Testament

The strongest remaining pattern is legal or instructional language that starts with `anyone / someone / whoever / everyone / a person / one who` and then falls back to `he / him / his`.

Representative examples:

- **Exodus 21:14** — `If someone ... kill him ... take him ... that they may die.` The generic actor/object chain is internally inconsistent and needs a context-aware inclusive rewrite.
- **Exodus 21:16** — `Anyone who kidnaps someone and sells him...` Generic `someone` should not automatically become male.
- **Exodus 22:1** — `If someone steals ... he shall pay...` Generic legal instruction.
- **Exodus 25:2** — `everyone whose heart makes him willing` — generic community instruction.
- **Leviticus 2:1** — `When anyone offers ... he shall pour...` — clear generic ritual/legal instruction.
- Similar patterns recur through Leviticus, Numbers, Deuteronomy, prophetic teaching, and wisdom material.

There are **360 strong generic-pronoun rows** plus **143 secondary rows**. These are not all automatic changes because a pronoun elsewhere in the same verse can refer to a specific named person; however, the legal/wisdom formulas are a high-yield editorial queue.

## Divine-referent pattern across the rest of the Old Testament

There are **437 divine-referent review rows**. The scanner intentionally errs on the side of review. Examples that are strong on their face include:

- **Exodus 15:2** — `Yah is my strength and song. He has become my salvation ... I will praise him ... exalt him.` Under the current project method, the divine masculine pronouns should be reviewed toward repeated `Yah / God / Elohim` language.
- **Exodus 15:26** — `YHWH your God ... right in his eyes` — `his` appears to be divine and should be reviewed accordingly.
- **Exodus 16:7** — `the glory of YHWH; because he hears your murmurings` — likely divine antecedent.
- Similar residuals remain especially in 2 Chronicles (41), 2 Kings (39), 1 Samuel (34), Isaiah (32), Judges (28), 1 Kings (28), Numbers (27), and Jeremiah (22).

But false positives are expected: e.g. a verse can name YHWH and then use `he/his` for Moshe, a priest, a king, an offerer, or another human. **Every divine row needs coreference review before editing.**

## Broad masculine-term review

The inventory contains **1,193** rows with `man / men / watchman / workman / craftsman` etc. This is deliberately the lowest-confidence category. Most historical/narrative male references should remain untouched.

Useful review targets are places where the English clearly means humanity generally or an occupation whose sex is not part of the source meaning, for example:

- plague/judgment formulas that contrast `man and animal` where the Hebrew may mean human/humankind;
- generic wisdom statements such as `a ... man` when the teaching addresses everyone;
- `workman/craftsman/watchman` where the Hebrew describes a role and the sex is not contextually significant.

Do **not** use this list for mechanical neutralization.

## Priority order for the next editorial release

1. **Lexical correctness first:** source-check the 347 brokenness rows, beginning with obvious malformed/incorrect English (`brokenness news`, `brokenness assemblies`, `brokenness men`, `A brokenness a person`, `harbors brokenness` where Hebrew is `deceit`).
2. **Strong generic legal/wisdom chains:** review the 360 high-priority generic-pronoun rows, prioritizing `anyone/someone/whoever/everyone/a person` constructions.
3. **Divine pronouns:** review the 437 divine-referent rows using the existing unmistakable-divine-only rule.
4. **Broad masculine terms last:** review the 1,193 term rows only where context indicates generic humanity or a non-sex-specific role.
5. Re-run the entire 23,145-verse audit plus the existing article/grammar scanner after any release. No global replacement.

## Suggested production instruction

Review the current canonical Old Testament only. For each listed candidate, consult the Hebrew and immediate literary context. Replace male-coded generic English only when the source is genuinely generic; preserve named/specific male people and source-significant gender. Replace masculine divine pronouns only when the referent is unmistakably divine, using the established divine name/title rather than introducing divine they/she/it. Treat `brokenness` as a contextual English choice, not a fixed gloss: distinguish wrong, harm, evil, calamity, trouble, misfortune, wickedness, deceit, iniquity, bad news, and other source senses. Apply only exact approved verse-level edits; never global-replace `man`, `he`, or `brokenness`. Re-run structural, verse-count, article, pronoun-agreement, and downstream feed validation before release.
