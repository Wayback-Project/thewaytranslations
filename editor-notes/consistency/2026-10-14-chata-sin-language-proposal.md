# Chata — context-sensitive restoration of “sin” language

**Status:** PROPOSAL ONLY — translation review required; no Scripture changes authorized  
**Date:** 2026-10-14 UTC  
**Scope:** Genesis–Revelation, The Way Version, all 66 books  
**Proposed term policy:** Prefer clear, accountable English that expresses the specific wrongdoing, failed responsibility, error, guilt, rebellion, or path imagery in the source context. Do not silently modernize away ethical seriousness.

## Why this matters

English *sin*, *sinner*, and *sinful* can carry inherited institutional, shame-centered, or identity-fixing connotations that may distract readers, including those harmed by religious institutions. A restorative edition can often communicate the text more directly as **wrongdoing**, **doing wrong**, **wronged**, **moral failure**, **error**, **wandering**, or **turning back**. This is an editorial accessibility rationale, **not** a claim that the biblical authors thought all wrongdoing was accidental, or that “missing the mark” is the full dictionary meaning in every instance. Nor does replacing language erase culpability, victim harm, or restorative justice.

Current project methodology: [README](../../README.md), [skill/SKILL.md](../../skill/SKILL.md), and the established proposal/release review paths. Source Greek is the textual starting point for New Testament lexical decisions; Semitic context may illuminate them but is not an attested original Hebrew autograph of a Greek letter.

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
| Hebrew moral wrongdoing | חטא, חטאת (ḥṭʾ / ḥaṭṭāʾt) | wrongdoing, do wrong, offense, fail morally | “miss the mark” is an illustration of one root sense, not an automatic rendering |
| Hebrew ritual sacrifice | חטאת (ḥaṭṭāʾt) when naming the rite | purification offering / sin offering with glossary note | A different usage of the same form; not “wrongdoing offering” |
| Hebrew guilt/liability | עָוֹן (`ʿavon`) | guilt, iniquity, responsibility for wrong | Do not flatten guilt and wrongdoing into one English noun |
| Hebrew deliberate breach | פֶּשַׁע (`peshaʿ`) | rebellion, breach, transgression | Do not soften betrayal or intentional violation to “mistake” |
| Hebrew inadvertence | שגג / שגגה (`šggh` / `šegagah`) | done unknowingly, unintentional wrong, mistake | Must retain accountability and context where the law assigns it |
| Hebrew wandering / returning | תעה / שוב (`taʿah` / `shuv`) | wandered, went astray / turn back, return | Keep path image when present; don't import it to every ḥṭʾ |
| Greek moral action/noun | ἁμαρτάνω / ἁμαρτία (`hamartanō` / `hamartia`) | do wrong / wrongdoing, moral failure | In Romans and elsewhere “sin” can be personified as a ruling power |
| Greek person label | ἁμαρτωλός (`hamartōlos`) | person who does wrong; person known for wrongdoing, by context | Don't fix a whole person's identity as intrinsically bad if text allows an action-focused phrase |
| Greek deviation | πλάνη (`planē`) | error, wandering, going astray | Distinct lexeme; James 5:20 has both “sinner” and “error” |
| Greek distinct wrongs | παράπτωμα, ἀδικία, ἀνομία | offense / injustice / lawlessness | Do not retroactively replace these with a one-size-fits-all “sin” label |

For every disputed passage record: original lemma and inflection, source witness, syntax, action/agent/affected persons, rhetorical image, candidate readings, final chosen wording, reviewer, and decision. Context-sensitive fidelity outranks reduction of residual counts.

## Proposed rendering rules

1. **Noun**: normally `sin` → **wrongdoing**, sometimes *moral failure*, *offense*, *wrong*, *guilt*, or *rebellion* when source and context support it. `sins` → **wrongdoings** or **wrongs** in plural-noun uses.
2. **Verb**: `sin` → **do wrong / act wrongly / wrong someone**. `sinned` → **did wrong / acted wrongly / wronged**. `sinning` → **doing wrong**; make tense, aspect, negation, and object grammatical. `sins` may be a *third-person verb*, not a plural noun.
3. **Human label**: `sinner(s)` → **person/people who do wrong**, **wrongdoer(s)** where succinctness matters, or a more precise description grounded in the context. Avoid implying that harm was imaginary.
4. **Adjective**: `sinful` → **marked by wrongdoing**, **morally compromised**, or **wrongful** after syntactic review. Do not use “failure” to trivialize abuse, injustice, or cruelty.
5. **Accidental vs deliberate**: use **error**, **mistake**, **unintentional wrong**, or **failure** only when textual context supports inadvertence, omission, uncertainty, or inability. Reserve **rebellion**, **injustice**, or **betrayal** for contexts demanding them.
6. **Ritual `sin offering`**: review as **purification offering** where ḥaṭṭāʾt identifies the rite; preserve distinction between an offering and the wrong for which it is brought. Never globally replace the embedded word in the same verse.
7. **Named place**: **wilderness of Sin** (Exodus 16:1 and related mentions) remains *Sin*. It is a geographical name, not wrongdoing.
8. **Literary imagery**: retain *crouching at the door* (Genesis 4:7), *scarlet becoming white* (Isaiah 1:18), *enslavement / reigning* (John 8:34; Romans 6), *covering* (James 5:20), and the theological argument, changing only language that can be changed faithfully.
9. **Search & notes**: reader text uses approved rendering, but glossary and search metadata retain traditional `sin`, `sinned`, `sinners`, etc. as discoverable aliases. Search aliases must never rewrite Scripture snippets or reader content; follow the reader's [alias-search display contract](https://github.com/drafthead/waywebsitenetlify/blob/netlify/app/ALIAS-SEARCH-UX.md).
10. **Review-first release**: no live text edit, regenerated JSON, EPUB, mobile feed, or `main` merge without a signed-off verse ledger and standard QA.

## Passage-level draft comparisons (editorial candidates, not approved text)

Each *candidate* is deliberately a working phrase or sentence, not a claim to have retranslated the entire verse from original-language witnesses.

| Ref | Currently problematic wording / feature | Suggested contextual direction | Review reason |
|---|---|---|---|
| Genesis 4:7 | “sin crouches at the door” | “wrongdoing crouches at the door” | Keep powerful personification, not merely a mistake |
| Genesis 20:9 | “How have I sinned against you … a great sin?” | “How have I wronged you … such a grave wrong?” | Two different grammatical functions in one verse |
| Genesis 39:9 | “sin against Elohim” | “act wrongly against Elohim” / “do wrong before Elohim” | Personal and relational wrong |
| Exodus 16:1 | “wilderness of Sin” | **keep `Sin`** | Proper geographical name |
| Leviticus 4:3 | “priest sins … his sin … sinned … sin offering” | “priest does wrong … wrongdoing … did wrong … purification offering” | Four tokens in different grammatical/ritual roles |
| Numbers 15:27 | “sins unwittingly … sin offering” | “does wrong unintentionally … purification offering” | Explicit inadvertence and separate offering |
| Psalm 51:3 | “My sin is constantly before me” | “My wrongdoing is always before me” | Confession and responsibility |
| Psalm 51:5 | “In sin my mother conceived me” | Explore “amid wrongdoing” while retaining poetry; **DO NOT auto-replace** | Contested anthropology and parallelism, avoid implicating mother without textual support |
| Isaiah 1:18 | “Though your sins be as scarlet” | “Though your wrongdoings are scarlet” | Preserve the metaphor |
| Matthew 26:28 | “remission of sins” | “forgiveness of wrongdoings” | Testament/covenant and forgiveness |
| Mark 2:17 | “call … sinners to turning back” | “call … those who do wrong to turn back” | Person label and invitation |
| Luke 15:7 | “one sinner who turns back” | “one person who has done wrong and turns back” | Keep restored course of life |
| John 8:34 | “commits sin … bondservant of sin” | “continues doing wrong … enslaved to wrongdoing” | Greek verbal aspect and bondage metaphor need checking |
| Romans 6:1 | “continue in sin” | “continue in wrongdoing” | Preserve debate over grace, not mere slip |
| Romans 6:12 | “let sin reign” | “let wrongdoing reign” | Maintain personification |
| 1 Corinthians 15:3 | “died for our sins” | “died for our wrongdoings” | Check received creedal formula and doctrinal ambiguity |
| Hebrews 10:18 | “no more offering for sin” | “no further offering for wrongdoing” | Relationship of sacrifice and forgiveness |
| James 5:20 | “turns a sinner from the error of their way … cover a multitude of sins” | “turns someone who has done wrong back from the error of their way … cover many wrongdoings” | Greek `hamartōlos` and distinct `planē`; retain turning/path image |
| 1 John 1:8 | “we have no sin” | “we have no wrongdoing” / “we are free of wrongdoing” | Claim about moral state, not a one-off error |
| Revelation 18:5 | “sins have reached to the sky” | “wrongdoings have reached to the sky” | Collective wrongdoing and judgment |
| Revelation 21:8 | “sinners” in vice list | “people who do wrong” (review idiom in full list) | Avoid defining a person by a label without weakening moral import |

## Review queues and required judgments

**A — straightforward action/grammar:** individual past and participle forms, many plural nouns, personal wrongs; favor minimally invasive text diffs. **B — source-sensitive:** ambiguous `sin` / `sins`, moral state/identity, forgiveness, poems, covenant themes. **C — high-risk:** ritual offerings, inadvertent wrongdoing, Pauline personification, inherited-guilt constructions, contested manuscripts, and the proper noun *Sin*. A “wrongdoing” default is never grounds for silently passing Queue C.

A translator and second reviewer should evaluate Hebrew/Aramaic or Greek lemmas, context, manuscript issue if relevant, and alternatives. Keep reviewers' source notes and decisions alongside a row-level accepted wording rather than bulk-generating canonical text.

## Reader / publishing integration (proposal only)

- Translation source of truth: `current-form-documents/the-way-current.epub`; archived originals and `original-documents` do not automatically override it.
- Website repo `drafthead/waywebsitenetlify`: `app/tools/build_reader_data.py` regenerates `app/data/index.json`, all 66 `app/data/books/*.json`, `app/data/search.json`, and `app/version.json` from EPUB; do not hand-patch generated output or HTML.
- Existing alias-search UX should be extended to traditional theological vocabulary carefully (word forms and contextual mappings, not indiscriminate substring search). Literal matches should outrank aliases; snippets must remain canonical.
- At release: archive old EPUB; record source SHA, changed refs, justifications and approved reviewer; generate new EPUB and fallbacks; check 66 books/1,189 chapters/31,102 verse search entries; verify no accidental verse omission, source checksum consistency, notes/anchors/search deep links, unexpected residual lexical words, and the **intentional** preservation of the place name *Sin*.
- Accessibility review: ask readers affected by religious institution trauma whether wording is clearer and less stigmatizing **without** using their experiences to overrule Greek/Hebrew semantic evidence.

## Explicit non-goals

No global find-and-replace. No rewriting Hebrew/Greek evidence to fit the desired English. No claim that `sin` originally means *only* “missing the mark.” No doctrinal erasure, smoothing of violent injustice into “error,” live translation release, or app code changes within this proposal branch.

**Approval gate:** source-audited ledger + specific edits + diff inspection + canonical rebase + website search compatibility tests. All CSV candidates remain **UNREVIEWED** until that gate is met.
