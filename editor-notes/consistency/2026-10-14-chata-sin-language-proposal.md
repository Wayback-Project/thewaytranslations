# Chata — moral failure, failure, and context-sensitive restoration of “sin” language

**Status:** PROPOSAL ONLY — translation review required; no Scripture changes authorized  
**Opened:** 2026-10-14 UTC  
**Updated:** 2026-10-15 — editor preference: **moral failure / failure first**  
**Scope:** Genesis–Revelation, The Way Version, all 66 books  
**Proposed term policy:** Treat **moral failure** as the first expression to evaluate for moral uses of “sin,” with **failure / failed** when a genuine falling-short or human limitation is in view. Use **wrongdoing / wronged** for concrete injuries, deliberate violations, or where grammar and literary imagery demand it. Keep ritual, guilt, rebellion, and proper-name usages distinct; never weaken accountability.

## Why this matters

English *sin*, *sinner*, and *sinful* can carry inherited institutional, shame-centered, or identity-fixing connotations that may distract readers, including those harmed by religious institutions. A restorative edition can often communicate the text more directly as **moral failure**, **failure**, **failed morally**, **wrongdoing**, **wronged**, **error**, **wandering**, or **turning back**, chosen by source meaning and natural English. This is an editorial accessibility rationale, **not** a claim that the biblical authors thought all wrongdoing was accidental, or that “missing the mark” is the full dictionary meaning in every instance. Nor does replacing language erase culpability, victim harm, or restorative justice.

Current project methodology: [README](../../README.md), [skill/SKILL.md](../../skill/SKILL.md), and the established proposal/release review paths. Source Greek is the textual starting point for New Testament lexical decisions; Semitic context may illuminate them but is not an attested original Hebrew autograph of a Greek letter.

## Editorial preference update — 2026-10-15

The editor's preferred **voice** is **moral failure**, and, where the meaning genuinely fits, **failure**. The previous draft used *wrongdoing* as its default. **This revision supersedes that default**; *wrongdoing* remains a purposeful contextual exception and is not removed from the vocabulary.

### Ordered selection, NOT a global substitution

1. **Moral failure / moral failures** — the normal **first candidate** for a moral noun where the passage speaks of human falling short, moral responsibility, confession, forgiveness, or restoration. This wording communicates an action or state without making “sinner” someone's permanent identity. *Example: “forgiveness of moral failures.”*
2. **Fail morally / failed morally / failing morally** — a first candidate for verbal uses, subject to natural English, tense, agency, and syntactic arguments. Sometimes “acted wrongly” reads better than a literal construction. *Example: “We have failed morally,”* not the ungrammatical “we have moral failed.”
3. **Failure / failed / failings** (without *moral*) — use **only** where the passage genuinely emphasizes falling short, weakness, an omission, or an inadvertent error, and the omission of “moral” does not disguise harm. This is **not** an automatic shortening of “moral failure”; check original-language meaning. *“Everyone has failed”* may be a readable alternative in Romans 3:23, but should be compared with *“everyone has failed morally”* because that verse separately says “fall short.”
4. **Wrongdoing / wrongdoings / wrong(s) / wronged** — choose when the text describes concrete mistreatment of another person, corruption, exploitation, intentional harm, legal-ethical offenses, wrongdoing as a ruling/predatory force, or when **moral failure** would distort or awkwardly soften what is described. This is not a less-preferred ethical verdict: it is sometimes simply the most faithful English.
5. **Error / mistake / wandering** — reserve for an *actual* involuntary, mistaken, or wayward context supported by the source, such as `planē` in James 5:20. A deliberate act does not become “a mistake” merely because we want non-shaming language.
6. **Guilt / rebellion / transgression / breach** — preserve specific source nuances, legal liability, and covenant relationship when those are the main point; don't collapse every Hebrew or Greek source term into `moral failure`.
7. **Purification offering** for ritual `ḥaṭṭāʾt` where source check supports it, and **Sin** unchanged for the place name. Neither should become “moral failure offering” or “wilderness of Failure.”

**Editing test:** For each proposed verse ask (a) Who did what? (b) Who was affected? (c) Was this intended, negligent, or inadvertent? (d) Is the passage naming a person, an action, guilt, a sacrifice, a force, or a direction of life? (e) Does “moral failure” sound like real contemporary English in that grammar? (f) Does it preserve the original metaphor and urgency? If not, choose a more concrete rendering and record why.

**Trauma-sensitive, not trivializing:** Avoid treating anyone as permanently defective, but **do not** describe abuse, violence, exploitation, or injustice as merely an unfortunate personal “failure.” Let the harm remain visible. Some readers may also find the word *failure* shaming; reader testing should therefore evaluate both accuracy and impact. No theological or ethical reality is removed by euphemism.

### Source-meaning constraint

Hebrew `ḥṭʾ` and Greek `hamartia / hamartanō` do **not** universally and literally mean “failure.” The root's physical *miss* sense does not turn all moral violations into inability or an accident. **Moral failure is an English editorial option**, not a rediscovered one-to-one ancient-language equivalent. Both **moral failure** and **wrongdoing** can be wrong for a particular verse. In all cases source syntax and literary context outrank a house vocabulary target.

## Data and audit boundary

A word-boundary, case-insensitive whole-Bible scan of the **existing English running text** in the reader's `app/data/books/*.json`, extracted from canonical EPUB **SHA-256 `58ccf8deb2f65ecaa0b35ce7b35137221c95998cee23d6461d98e250c297b4fc`**, found:

- **863 lexical occurrences** across **732 distinct verses**; **583 Old Testament / 280 New Testament**.
- Forms: `sin` 446, `sins` 204, `sinned` 124, `sinning` 7, `sinner` 22, `sinners` 50, `sinful` 9, `sinfulness` 1.
- **124** exact-token `sin offering` instances are triaged as *ritual terminology* for separate evaluation; **4** appearances are the proper place name **Sin** and must remain unchanged.
- 863 rows in [nine review CSVs](../research/chata-inventory/README.md), each with exact book/chapter/verse, matched form, tentative lexical direction, original English verse, and `UNREVIEWED` status. Multiple occurrences in one verse each receive their own row.
- This is **not** an audit of all source-language instances of Hebrew חטא or Greek ἁμαρτία: verses already rendered as “wrong,” “transgression,” “guilt,” etc. are outside this English-residual scan.

**Moving-release notice:** While this branch was being prepared, canonical `main` advanced to EPUB SHA-256 `094be0ae8786e2e407515b5485946fc8ce35162fc4d0e62815b7983cf3ec4ffa` (2026-10-14 Romans divine-pronoun follow-up). The branch's inventory remains explicitly pinned to the previous coherent snapshot, rather than silently mixing editions. The updated app's Romans file still contains 60 matches. **Re-run the full scan and compare every proposed verse against the final target EPUB immediately before approval/release.** Do not use the old snapshot as a substitute for final release QA.

## Source-language decision grid

| Language/context | Source forms to verify | Translational direction | Pitfall |
|---|---|---|---|
| Hebrew moral wrongdoing | חטא, חטאת (ḥṭʾ / ḥaṭṭāʾt) | moral failure / fail morally (first candidate); wrongdoing where concrete offense | “miss the mark” is an illustration of one root sense, not an automatic rendering |
| Hebrew ritual sacrifice | חטאת (ḥaṭṭāʾt) when naming the rite | purification offering / sin offering with glossary note | A different usage of the same form; not “wrongdoing offering” |
| Hebrew guilt/liability | עָוֹן (`ʿavon`) | guilt, iniquity, responsibility for wrong | Do not flatten guilt and wrongdoing into one English noun |
| Hebrew deliberate breach | פֶּשַׁע (`peshaʿ`) | rebellion, breach, transgression | Do not soften betrayal or intentional violation to “mistake” |
| Hebrew inadvertence | שגג / שגגה (`šggh` / `šegagah`) | done unknowingly, unintentional wrong, mistake | Must retain accountability and context where the law assigns it |
| Hebrew wandering / returning | תעה / שוב (`taʿah` / `shuv`) | wandered, went astray / turn back, return | Keep path image when present; don't import it to every ḥṭʾ |
| Greek moral action/noun | ἁμαρτάνω / ἁμαρτία (`hamartanō` / `hamartia`) | moral failure / fail morally (first candidate); wrongdoing where needed | In Romans and elsewhere “sin” can be personified as a ruling power |
| Greek person label | ἁμαρτωλός (`hamartōlos`) | person who has failed morally; person who does wrong, by context | Don't fix a whole person's identity as intrinsically bad if text allows an action-focused phrase |
| Greek deviation | πλάνη (`planē`) | error, wandering, going astray | Distinct lexeme; James 5:20 has both “sinner” and “error” |
| Greek distinct wrongs | παράπτωμα, ἀδικία, ἀνομία | offense / injustice / lawlessness | Do not retroactively replace these with a one-size-fits-all “sin” label |

For every disputed passage record: original lemma and inflection, source witness, syntax, action/agent/affected persons, rhetorical image, candidate readings, final chosen wording, reviewer, and decision. Context-sensitive fidelity outranks reduction of residual counts.

## Proposed rendering rules

1. **Noun:** Start by trying `sin` → **moral failure** and plural `sins` → **moral failures**. Prefer **wrongdoing / wrongs** when intentional harm or force-personification calls for them; prefer *guilt*, *offense*, or *rebellion* only where supported by the source. Do not assume English `sins` is always a noun: it can be a third-person singular verb.
2. **Verb:** Try `sin` → **fail morally**; `sinned` → **failed morally**; `sinning` → **failing morally**; `sins` as verb → **fails morally**. Where English requires an object, say **wronged [someone]**, **acted wrongly toward [someone]**, or **did wrong**. Preserve tense, aspect, idiom, and interpersonal responsibility.
3. **Human label:** Try `sinner(s)` → **someone / people who have failed morally**, or **those who fail morally** for a habitual or general statement. Where conduct concretely harms others, **people who do wrong / wrongdoers** may be clearer. Avoid turning a person's actions into an essentialized identity. Never soften serial or deliberate abuse.
4. **Adjective/abstract:** `sinful` → **marked by moral failure**, **morally compromised**, **wrongful** depending on grammar; `sinfulness` → **moral failure** or **pattern of wrongdoing** depending on whether a state or practice is meant. Preserve meaningful distinctions from weakness or sickness.
5. **Unqualified failure:** Choose **failure**, **failed**, or **failings** only when this conveys a shortfall, omission, limited ability, or genuinely inadvertent action; it is not the universal replacement for culpable wrong.
6. **Ritual and places:** `sin offering` requires source review and may become **purification offering** (not *moral failure offering*); **wilderness of Sin** stays *Sin*.
7. **Source-specific divergence:** Keep *error/wandering* (especially Greek `planē`), *guilt* (`ʿavon` as context warrants), *rebellion* (`peshaʿ`), and other distinct concepts, rather than importing a preferred label.
8. **Literary imagery:** retain *crouching at the door* (Genesis 4:7), *scarlet becoming white* (Isaiah 1:18), *enslavement / reigning* (John 8:34; Romans 6), *covering* (James 5:20), and the theological argument. In personification passages, **wrongdoing** may be more precise than **moral failure**.
9. **Search & notes:** preserve `sin / sins / sinner / sinners / sinned / sinning` as legacy **search metadata** only, while the reader displays approved canonical wording. Follow the reader's [alias-search display contract](https://github.com/drafthead/waywebsitenetlify/blob/netlify/app/ALIAS-SEARCH-UX.md).
10. **Release:** every occurrence remains an **unreviewed candidate** until source-context review. No bulk Scripture edits, generated JSON edits, EPUB publishing, or `main` merging under this draft PR.

## Passage-level draft comparisons (editorial candidates, not approved text)

This table applies the **new preferred voice** to specific passages. Where *wrongdoing* or a ritual expression reads better, that is a reasoned exception, not a failure to follow the editor's preference. These are **English revision candidates**, not certified fresh translations from the original witnesses.

| Reference | Existing focus | New proposed direction | Editorial reason / alternative |
|---|---|---|---|
| Genesis 4:7 | “sin crouches at the door” | **“wrongdoing crouches at the door”** | Retain force and personification; “moral failure crouches” is less idiomatic. |
| Genesis 20:9 | “How have I sinned against you … a great sin?” | **“How have I wronged you … such a serious wrong?”** | Direct harm toward someone, two distinct grammatical uses. |
| Genesis 39:9 | “sin against Elohim” | **“fail morally before Elohim”** / “do wrong against Elohim” | Compare whether this softens the serious act; retain context of betrayal. |
| Exodus 16:1 | “wilderness of Sin” | **Keep “Sin”** | Proper place name. |
| Leviticus 4:3 | “priest sins … his sin … sinned … sin offering” | **“priest fails morally … moral failure … failed morally … purification offering”** | First three are actions/liability; fourth is a distinct ritual noun. Review unintentional nature of priestly violation. |
| Numbers 15:27 | “sins unwittingly … sin offering” | **“does wrong unknowingly … purification offering”** | Inadvertence is explicitly present; “failure” without qualification might lose guilt/remedy. |
| Psalm 51:3 | “My sin is constantly before me” | **“My moral failure is always before me”** | Confession, not identity. |
| Psalm 51:5 | “In sin my mother conceived me” | **Defer: evaluate “moral failure” in full parallelism** | High-risk; avoid inventing blame of the mother or a doctrine of inherited guilt. |
| Isaiah 1:18 | “Though your sins be as scarlet” | **“Though your moral failures are as scarlet”** | Preserve the poetic contrast and responsibility. |
| Matthew 26:28 | “remission of sins” | **“forgiveness of moral failures”** | Readable and appropriate first candidate; validate covenant and forgiveness vocabulary. |
| Mark 2:17 | “call … sinners to turning back” | **“call … those who have failed morally to turn back”** | Invite change, not fixed identity; test naturalness in context. |
| Luke 15:7 | “one sinner who turns back” | **“one person who has failed morally and turns back”** | Keep the return/rejoicing image. |
| John 8:34 | “commits sin … bondservant of sin” | **“practices wrongdoing … enslaved to wrongdoing”** | Repeated harmful action / bondage image needs force; not a harmless shortfall. |
| Romans 3:23 | “all have sinned and fall short” | **“all have failed morally and fall short”** | Alternative: “all have failed,” but it may duplicate “fall short”; compare Greek clauses. |
| Romans 6:1 | “continue in sin” | **“continue in moral failure”** | Conveys ongoing practice and contrast with grace. |
| Romans 6:12 | “let sin reign” | **“let wrongdoing reign”** | Keep the governing-force metaphor; first-choice term would be less vivid here. |
| 1 Corinthians 15:3 | “died for our sins” | **“died for our moral failures”** | Keep received formula and theological claim open to source review. |
| Hebrews 10:18 | “no more offering for sin” | **“no further offering for moral failure”** | Sacrificial context: distinguish sacrifice *for* moral failure from named `ḥaṭṭāʾt` ritual. |
| James 5:20 | “turns a sinner from the error of their way … cover a multitude of sins” | **“turns a person who has failed morally back from the error of their way … cover many moral failures”** | `hamartōlos` (person label) and `planē` (error/going astray) are different, preserve both. |
| 1 John 1:8 | “we have no sin” | **“there is no moral failure in us”** | Review fuller syntax: “If we claim there is no moral failure in us…” |
| Revelation 18:5 | “her sins have reached to the sky” | **“her wrongdoings have reached to the sky”** | Corporate exploitation and judgment; “failures” might minimize harm. |
| Revelation 21:8 | “sinners” within a vice list | **“those who persist in wrongdoing”** (subject to source review) | Serious conduct, not a permanent metaphysical label; ensure habituality is supported. |

## Review queues and required judgments

**A — straightforward action/grammar:** individual past and participle forms, many plural nouns, personal wrongs; favor minimally invasive text diffs. **B — source-sensitive:** ambiguous `sin` / `sins`, moral state/identity, forgiveness, poems, covenant themes. **C — high-risk:** ritual offerings, inadvertent wrongdoing, Pauline personification, inherited-guilt constructions, contested manuscripts, and the proper noun *Sin*. A “moral failure” preference never overrides Queue C source-sensitive analysis.

A translator and second reviewer should evaluate Hebrew/Aramaic or Greek lemmas, context, manuscript issue if relevant, and alternatives. Keep reviewers' source notes and decisions alongside a row-level accepted wording rather than bulk-generating canonical text.

## Reader / publishing integration (proposal only)

- Translation source of truth: `current-form-documents/the-way-current.epub`; archived originals and `original-documents` do not automatically override it.
- Website repo `drafthead/waywebsitenetlify`: `app/tools/build_reader_data.py` regenerates `app/data/index.json`, all 66 `app/data/books/*.json`, `app/data/search.json`, and `app/version.json` from EPUB; do not hand-patch generated output or HTML.
- Existing alias-search UX should be extended to traditional theological vocabulary carefully (word forms and contextual mappings, not indiscriminate substring search). Literal matches should outrank aliases; snippets must remain canonical.
- At release: archive old EPUB; record source SHA, changed refs, justifications and approved reviewer; generate new EPUB and fallbacks; check 66 books/1,189 chapters/31,102 verse search entries; verify no accidental verse omission, source checksum consistency, notes/anchors/search deep links, unexpected residual lexical words, and the **intentional** preservation of the place name *Sin*.
- Accessibility review: ask readers affected by religious institution trauma whether wording is clearer and less stigmatizing **without** using their experiences to overrule Greek/Hebrew semantic evidence.

## Explicit non-goals

No global find-and-replace and no misleading claim that “moral failure” is the literal source word everywhere. No rewriting Hebrew/Greek evidence to fit the desired English. No claim that `sin` originally means *only* “missing the mark.” No doctrinal erasure, smoothing of violent injustice into “error,” live translation release, or app code changes within this proposal branch.

**Approval gate:** source-audited ledger + specific edits + diff inspection + canonical rebase + website search compatibility tests. All CSV candidates remain **UNREVIEWED** until that gate is met.
