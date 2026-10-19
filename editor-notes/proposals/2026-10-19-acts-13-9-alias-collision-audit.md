# Proposed correction: collapsed dual names / source-language glosses — Acts 13:9 and related passages
**Created:** 2026-10-19. **STATUS: PROPOSAL FOR EDITORIAL REVIEW ONLY — NO SCRIPTURE, EPUB, NETLIFY, MOBILE OR PRINT RELEASE AUTHORIZED.**

## What prompted the investigation
A captured native e-reader extract says: **“But Shaul, who is also called Shaul, filled with the Ruach of Elohim, fastened his eyes on him,”** (Acts 13:9). The same string occurs in the **current production-derived Acts JSON**, in `original-documents/acts_restorative_translation.txt`, and in the **2026-04-08 historical Acts chapter snapshot**. It is a real inherited textual error, not a newly introduced Genesis-release change or proof of a missing `netlify` push. The user-provided capture was from an installed app's bundled local reader; an installed binary may also lag a remote content feed.

## What the source actually says
- **Acts 13:9**: Greek `Σαῦλος δέ, ὁ καὶ Παῦλος`, *Saulos de, ho kai Paulos*. This names **two distinct forms of the same person's name**: Jewish/Hebrew **Shaul** and Greek-transcribed Roman/Latin **Paulos/Paulus** (familiar English **Paul**). The point is that Shaul **was also called Paul**, not “Shaul was also called Shaul.” Acts 13:7 has the separate proconsul **Sergius Paulus**, which must not be modified or conflated with the emissary. The shift occurs in the Acts narrative in this context; **it is not a record of a conversion-time renaming by Yeshua**.
- **John 1:42**: Greek `Κηφᾶς (ὃ ἑρμηνεύεται Πέτρος)`: Aramaic **Kepha** is interpreted with the distinct Greek name **Petros** (Peter; rock/stone). The current parenthesis “Kepha (which is by interpretation, **Shimon (called Kepha)**)” obscures the *source-language explanation* and inserts another subject/name instead.
- **John 4:25**: Greek `Μεσσίας ... ὁ λεγόμενος Χριστός`: **Messias** (Messiah) is explicitly related to the Greek title **Christos** (“Anointed One”). The current “Messiah ... the one who is called **Messiah**” needlessly erases that relationship.
- The edition's current policy generally favors **Shaul** for the emissary's ongoing narrative mentions, even where the Greek uses *Paulos*. **That global naming policy should NOT be overturned automatically** merely to repair a dual-name explanation. Preserve both distinct names when the verse explicitly compares them.

Primary Greek references: https://www.greekbible.com/acts/13/9 ; https://biblehub.com/text/john/1-42.htm ; https://www.greekbible.com/john/4/25 . Academic context: https://academic.oup.com/book/9676/chapter-abstract/156811629 . Current edition policy: `skill/SKILL.md` and `editor-notes/proposed-rules/original-name-restoration/README.md`.

## Concrete verse-by-verse proposals (full verses; ALL require user/editor approval)
### A — Acts 13:9 — high-confidence identity/alias defect
**Current:** But Shaul, who is also called Shaul, filled with the Ruach of Elohim, fastened his eyes on him,

**Recommended:** But Shaul, who is also called Paulos, filled with the Ruach of Elohim, fastened his eyes on him,

**Editorial spelling alternative:** `Paul` (most familiar) or `Paulus` (Latin/Roman form, consistent with Sergius Paulus nearby) rather than `Paulos` (Greek transcription). The editor **must pick and approve** the distinct second form before the release ledger is considered final. Retain Shaul as first form and preserve the rest of the verse.

### B — John 1:42 — source-gloss collision
**Current:** He brought him to Yeshua. Yeshua looked at him, and said, "You are Shimon the son of Yonah. You shall be called Kepha" (which is by interpretation, Shimon (called Kepha)).

**Recommended:** He brought him to Yeshua. Yeshua looked at him, and said, "You are Shimon the son of Yonah. You shall be called Kepha" (which is rendered Petros in Greek, meaning Rock).

**Rationale:** Preserve distinct Greek `Petros` and Aramaic `Kepha` while using this edition's restored names. **Do not change Yonah/son-of-Jonah vs son-of-John at the same time**: that is a separate manuscript variation and needs its own textual-criticism decision. More conservative option: `(which is interpreted Petros in Greek)`.

### C — John 4:25 — Greek/Hebrew title conflation
**Current:** The woman said to him, "I know that Messiah comes," (the one who is called Messiah). "When he has come, he will declare to us all things."

**Recommended:** The woman said to him, "I know that Messiah comes" (the one called Christos in Greek, meaning the Anointed One). "When he has come, he will declare to us all things."

**Rationale:** Greek intentionally distinguishes the Semitic `Messias` and Greek `Christos`; preserving this explanatory bridge avoids a tautology. More concise option: `(the one called Christos)`. Do not treat every narrative occurrence of Messiah as a reason to reintroduce Christos.

## Corpus audit (production-derived Scripture, 2026-10-19)
We fetched **all 66 current `drafthead/waywebsitenetlify:netlify` per-book JSON files** (`app/data/books/*.json`) and examined **31,102 verse records**. All share the current canonical EPUB SHA-256 `785a21b93491ca5433f0bfaff849cfd7eb6f42957072cd5fe722a60dfb0d0a90`. The targeted “called / named / also-called / whose name / interpreted” pattern audit identifies the three above as **source-verified identity/explanatory collisions**. This is a **pattern-driven candidate audit**, not a claim that all possible translation mistakes have been eliminated; manual context/source comparisons remain necessary.

**Other verses reviewed / protect or evaluate individually**:
- **Acts 13:7** (Sergius Paulus) — a **different person**; retain the proconsul's name. **Acts 13:13, 13:16, 13:43** and **Romans 1:1** — currently **Shaul** under a general restoration policy. These are **not** included in the three-verse correction. A whole-corpus decision about whether Acts narratively switches to *Paulos* after 13:9 would require a separate translation-policy proposal, not a silent global replacement.
- **Acts 1:23** (Yosef / Barsabbas / Justus), **Acts 4:36** (Joses / Barnabas), **Acts 13:1** (Shimon / Niger), **Acts 15:37** (Yochanan / Markos), **John 11:16** (Ta'oma / Didymus), **Daniel 2:26** and **4:19** (Dani'el / Belteshazzar), **Genesis 35:18** (Benoni / Binyamin) — distinct forms remain distinct; **do not replace** without new textual findings.
- **Luke 6:14** (`Nethanel (called Bar-Tolmai)`) — **needs separate identity-critical review**: Luke's list actually supplies Bartholomaios/Bartholomew, and some traditions equate this person with John's Nathanael but this is not explicit in Luke. Do not silently convert Bartholomew to Nathanael or vice versa without an approved identity policy. **Not a confirmed duplicate-name defect**.
- **John 21:7, 21:15** and **Luke 22:61** use the edition's `Shimon (called Kepha)` identity-explainer to render narrative references to Peter; review the **translation-versus-added-reader-gloss** boundary, but do not batch change them under this three-verse proposal.
- **Genesis 35:10** repeats Yaakov in a **negated renaming** (“no longer ... Yaakov”) — not an alias-collapse error; preserve.

## How this likely happened — evidence versus inference
**Established:** The erroneous Acts 13:9 phrase already existed in `rendered-documents-history/2026-04-08_1216UTC/books/acts/chapter-013.txt`, and remains in older `original-documents/acts_restorative_translation.txt`. Therefore a present-day GitHub/Netlify sync faithfully **propagated inherited bad text** rather than creating the bad name. **Likely mechanism:** source-name restoration/normalization applied a single preferred label `Shaul` to both `Saulos` and `Paulos`, and similarly collapsed the explanatory secondary terms `Petros` and `Christos` in John. The current project skill explicitly recommends `Shaul` rather than Paul/Saul in normal prose; the original-name restoration rules also warn against global `Saul/Paul/Shaul` replacements. **Not proven:** the exact script, author, or original edit date that first introduced any collision. A targeted git-history/source-provenance search can refine that later. Do not describe a hypothesized script as a confirmed culprit.

## Approval and release gate — absolutely no automatic publishing
1. **User reviews these 3 proposed verses and chooses spelling/gloss options**. Include only explicitly approved rows in a finite, full-verse before/after release ledger. Source check Hebrew/Greek; keep distinctions between distinct identities, alternate names, and explanatory transliterations.
2. Before touching any Scripture, re-read **latest canonical** `current-form-documents/the-way-current.epub`; require exact baseline SHA and every old full-verse match. No stale EPUB overwrite.
3. Archive prior EPUB, write **only approved XHTML verses** in canonical EPUB, validate mimetype/CRC/XML/internal hyperlinks, 66 books, 1,189 chapters, **31,102** verse records, and assert zero unrelated verse diffs. Test **every** approved row and explicit preserved checkpoints including Acts 13:7, Acts 13:13, Romans 1:1, John 11:16 and other dual-name cases; do not run global replacements.
4. Regenerate canonical original-name registry and public mobile fallback with the **new canonical EPUB SHA**. Keep alias/search/pronunciation metadata **separate from Scripture**; make sure familiar searches `Saul`, `Paul`, `Paulos`, `Paulus`, `Shaul`, `Peter`, `Petros`, `Cephas`, `Christ`, `Christos` correctly map to the intended people/titles without rewriting original verses or confusing Sergius Paulus.
5. Sync exact EPUB onto `drafthead/waywebsitenetlify:main` if desired **AND MANDATORILY `drafthead/waywebsitenetlify:netlify`**. The **`netlify` branch** is the production branch. Generate both `media/The Way Version.epub` and `app/The Way Version.epub` plus `app/data/books/*.json`, `app/data/index.json`, `app/data/search.json`, `app/version.json` and `app/mobile-update/{manifest.json,content.json}` **from the exact canonical EPUB** (not hand edits).
6. Verify LIVE `https://thewayversion.com/app/` chapter JSON, search rows, version/manifest SHA, and both entire OTA JSON payload checksums; inspect all changed verses and the known unchanged alias exceptions. A branch merge or website `main` build alone is not proof of going live.
7. Update `drafthead/biblewithoriginalnamesMobileApp:main` `reader-release.json` with vetted **`netlify` content commit**, canonical commit/EPUB SHA, complete primary and GitHub fallback content SHA; run mobile CI. Native installed bundled reader is a separate binary source; distinguish a successful content-only OTA feed from an actual device refresh or native-binary update.
8. Append exact final approved before/after text and rationale to the **print Google Doc handoff**, but do not claim the editable 66-book print master, PDF, or publisher proof was changed.
9. **Fail closed:** if source/verse/alias/manifest hashes, coverage or protected passages disagree, halt before production and return for editorial review.

## Proposal artifacts
- Machine-readable source/current/recommended decisions: `tools/local/2026-10-19-name-alias-collision-candidates.json`.
- Audit/check-only tool: `tools/local/audit_2026_10_19_name_alias_collisions.py`.
- **This PR must remain DRAFT / UNMERGED until the user explicitly signs off on final wordings and scope.**
