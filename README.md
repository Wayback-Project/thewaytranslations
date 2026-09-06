# The Way Version

> **Read now:** [Open the free web reader](https://thewayversion.com/app)  
> **Learn more:** [TheWayVersion.com](https://thewayversion.com)  
> **Download:** [Current whole-Bible EPUB](current-form-documents/the-way-current.epub)

The Way Version is the Bible with original names brought back into view. It keeps the Scripture people know while retaining names and source-language terms closer to the forms heard in their own time: **Yeshua, Yochanan, Ya’akov, Yosef, Maryam, Dawid, Avraham, YHWH, Elohim, Ruach**, and more.

This repository is the public editorial and release workspace behind the translation. It contains the current EPUB, editable source documents, historical renders, translation methodology, research notes, and change records.

## What readers will notice

- **Original names remain visible.** Familiar later English forms do not automatically replace the names carried by the text.
- **Divine names and titles stay distinct.** Terms such as **YHWH**, **Elohim**, and **Ruach** are not flattened into one generic label.
- **Ancient meanings guide English choices.** Terms including *torah*, *shalom*, *chesed*, *metanoeo*, *basileia*, *Sheol*, *Hades*, and *Gehenna* are rendered according to context instead of inherited one-word conventions.
- **The spoken world of Yeshua matters.** Gospel passages receive special attention to their Semitic setting, oral force, imagery, and patterns of thought.
- **Readability still matters.** The goal is clear contemporary English with ancient texture—not obscurity for its own sake.
- **Editorial decisions are traceable.** Meaningful changes are documented with rationale, source track, affected references, and review status.

### A few examples

| Reference | The Way Version direction |
|---|---|
| Matthew 1:1 | Yeshua the Messiah, son of Dawid, son of Avraham |
| Luke 1:26–31 | Gavriel, Elohim, Yosef, Dawid, Maryam, and Yeshua remain visible |
| Genesis 1:1–2 | Elohim creates; the Ruach of Elohim hovers over the waters |
| Psalm 23:1 | “YHWH is my shepherd: I shall lack nothing.” |
| Matthew 4:17 | “Turn back, for the reign of the heavens has drawn near.” |

See more comparisons and begin reading at [TheWayVersion.com](https://thewayversion.com).

## Current release

The canonical whole-Bible release is [current-form-documents/the-way-current.epub](current-form-documents/the-way-current.epub).

| Item | Current value |
|---|---|
| Coverage | 66 books / 1,189 chapters |
| EPUB SHA-256 | `dbd8cace51a0e726a2d910622af995d490ee4f24f76eb7efcd0e5a1756c1119e` |
| Browser reader | [thewayversion.com/app](https://thewayversion.com/app) |
| Website | [thewayversion.com](https://thewayversion.com) |
| Mobile | Native mobile applications are in development |

The browser reader is mobile-first and provides search, continuous reading, bookmarks, multi-verse highlights, notes, sharing, typography controls, and reading themes. The EPUB works with Kindle, Apple Books, tablets, phones, and most e-readers.

## Translation approach

The project follows a historical-restorative method:

1. Start with the earliest recoverable source-language evidence.
2. Give the Hebrew Bible priority in Hebrew, with Aramaic where the source is Aramaic.
3. Give the sayings of Yeshua special attention to their Aramaic/Semitic setting while checking the Greek textual witness.
4. Use Greek-critical evidence as primary where later New Testament writings have strong Greek grounding, while documenting relevant Semitic comparisons.
5. Preserve distinctions, grammatical force, ambiguity, social context, and ancient imagery when supported by the text.
6. Keep source-near translation separate from optional devotional or resonance language.
7. Record significant decisions instead of silently rewriting the corpus.

The complete working specification is in [skill/SKILL.md](skill/SKILL.md). This is an active translation project, and difficult or debated choices remain open to documented review.

## Repository map

| Location | Purpose |
|---|---|
| `current-form-documents/` | Current canonical EPUB and release information |
| `original-documents/` | Human-editable Scripture source files |
| `rendered-documents-history/` | Timestamped archives of earlier rendered editions |
| `change-logs/` | Dated book-level changes, reports, and QA records |
| `editor-notes/` | Research, reflections, inspirations, and proposed rules |
| `skill/` | Historical-restorative translation behavior and terminology policy |
| `tools/` | Import, export, audit, and search utilities |
| `activity/` | Saved query activity for transparent research workflows |

## Release workflow

1. Translation work is maintained in `original-documents/`.
2. Meaningful editorial changes are recorded in `editor-notes/` and `change-logs/`.
3. The prior current EPUB is archived under a UTC-stamped folder in `rendered-documents-history/`.
4. The new render becomes `current-form-documents/the-way-current.epub`.
5. The EPUB container, checksum, book count, chapter count, and terminology audits are validated.
6. `rendered-documents-history/LOG.md` records the release transaction.

## Collaboration

Thoughtful review is welcome. For substantial translation or structural changes, open an issue describing the proposed scope, evidence, and rationale. Keep pull requests focused, preserve verse ordering and source integrity, and update the corresponding methodology or change record.

The initial repository framework was created with AI assistance and is continually reviewed and corrected through an editor-directed workflow. AI output is not treated as authority; decisions are expected to remain text-based, reviewable, and documented.

## Copyright and quotation

The Way Version Scripture text and EPUB are copyright © 2026 **The Way Partners LLC**. All rights reserved.

Quotation of up to 500 verses is welcomed in books, ebooks, websites, social media, sermons, teaching materials, podcasts, video, and other print, digital, or audio works when the requirements in [COPYRIGHT.md](COPYRIGHT.md) are followed. Attribution is required. Uses beyond the standard quotation allowance require advance written permission from [hello@twpventures.com](mailto:hello@twpventures.com).

Public access to this repository does not place the translation in the public domain or automatically license the Scripture text, EPUB, branding, or software beyond the permissions expressly stated in [COPYRIGHT.md](COPYRIGHT.md).

---

Published by **The Way Partners LLC**  
[TheWayVersion.com](https://thewayversion.com) · [hello@twpventures.com](mailto:hello@twpventures.com)
