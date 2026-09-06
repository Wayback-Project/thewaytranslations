# The Way Version

> **Read now:** [Open the free web reader](https://thewayversion.com/app)  
> **Learn more:** [TheWayVersion.com](https://thewayversion.com)  
> **Download:** [Current whole-Bible EPUB](current-form-documents/the-way-current.epub)

The Way Version is a contemporary English Bible translation that retains selected Hebrew and Aramaic forms of biblical names and terms in the running text. Readers will encounter forms such as **Yeshua, Yochanan, Ya’akov, Yosef, Maryam, Dawid, Avraham, YHWH, Elohim**, and **Ruach**.

The project is intended for readers interested in the Bible, the history of biblical names, and the languages and settings in which the texts developed. Familiar English forms such as Jesus, John, James, Mary, and David reflect their normal transmission through several languages and remain useful in English. The Way Version uses selected earlier-language forms to make that history more visible.

This repository is the public editorial and release workspace for the translation. It contains the current EPUB, editable source documents, historical renders, methodology, research notes, and change records.

## At a glance

- **Names appear in the text.** Selected Hebrew and Aramaic forms are retained where they help readers notice the linguistic and historical setting.
- **Divine names and terms are identified carefully.** **YHWH**, **Elohim**, and **Ruach** represent different source-language forms and are used according to the editorial decisions of the current edition.
- **Translation choices consider context.** Terms including *torah*, *shalom*, *chesed*, *metanoeo*, *basileia*, *Sheol*, *Hades*, and *Gehenna* are evaluated in their literary, linguistic, and historical settings.
- **New Testament language is handled with appropriate limits.** Greek textual witnesses provide the primary textual basis. Aramaic and other Semitic evidence is considered when it helps explain the historical setting, speech patterns, or possible background of a passage.
- **The English remains readable.** Source-language details are retained selectively so that the translation can still be read continuously.
- **Significant decisions are documented.** Change records describe the rationale, sources, affected references, and review status of substantial revisions.

## Names and terminology

Transliteration is an editorial practice, not a claim that one exact ancient pronunciation can always be recovered. Biblical names passed through Hebrew, Aramaic, Greek, Latin, and later languages, and more than one responsible spelling may be possible.

| Familiar English form | Form used in the current edition | Context |
|---|---|---|
| Jesus | Yeshua | A Hebrew and Aramaic form associated with the name |
| John | Yochanan | A Hebrew form of the name |
| James / Jacob | Ya’akov | A Hebrew form underlying both conventional English renderings |
| Mary | Maryam | A Semitic form associated with the name |
| David | Dawid | A transliteration of the Hebrew name |
| LORD | YHWH | The four Hebrew consonants of the divine name; its exact ancient pronunciation is uncertain |
| God | Elohim | Retained where the Hebrew term itself is relevant to the edition |
| Spirit / breath / wind | Ruach | Rendered according to context, with the source term retained in selected passages |

### Examples from the current edition

| Reference | Example rendering | What it illustrates |
|---|---|---|
| Matthew 1:1 | Yeshua the Messiah, son of Dawid, son of Avraham | Personal names retained in Semitic forms |
| Luke 1:26–31 | Gavriel, Elohim, Yosef, Dawid, Maryam, and Yeshua | Several names and a divine title within one passage |
| Genesis 1:1–2 | Elohim creates; the Ruach of Elohim hovers over the waters | Distinct Hebrew terms in context |
| Psalm 23:1 | “YHWH is my shepherd: I shall lack nothing.” | The consonantal Hebrew divine name in the text |
| Matthew 4:17 | “Turn back, for the reign of the heavens has drawn near.” | A contextual translation choice documented by the project |

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

## Editorial approach

The project uses a historical and text-based method:

1. Begin with the relevant textual witnesses and source languages for each passage.
2. Use Hebrew and Aramaic evidence for the Hebrew Bible according to the language of the source text.
3. Use Greek textual witnesses as the primary basis for the New Testament while consulting Semitic context and comparators where historically relevant.
4. Distinguish what the surviving text says from proposals about historical speech, later interpretation, or reconstructed wording.
5. Preserve meaningful ambiguity, grammatical force, social context, and imagery when the evidence supports doing so.
6. Present debated decisions with appropriate qualification and record plausible alternatives when they materially affect the translation.
7. Keep source-near translation separate from optional devotional or resonance language.
8. Record significant decisions so that revisions can be reviewed rather than silently introduced.

The complete working specification is in [skill/SKILL.md](skill/SKILL.md). This is an active translation project, and difficult or debated choices remain open to documented review.

## Repository map

| Location | Purpose |
|---|---|
| `current-form-documents/` | Current canonical EPUB and release information |
| `original-documents/` | Human-editable Scripture source files |
| `rendered-documents-history/` | Timestamped archives of earlier rendered editions |
| `change-logs/` | Dated book-level changes, reports, and QA records |
| `editor-notes/` | Research, reflections, inspirations, and proposed rules |
| `skill/` | Translation methodology and terminology policy |
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

The initial repository framework was created with AI assistance and is continually reviewed and corrected through an editor-directed workflow. AI output is not treated as authority; decisions are expected to remain evidence-based, reviewable, and documented.

## Copyright and quotation

The Way Version Scripture text and EPUB are copyright © 2026 **The Way Partners LLC**. All rights reserved.

Quotation of up to 500 verses is welcomed in books, ebooks, websites, social media, sermons, teaching materials, podcasts, video, and other print, digital, or audio works when the requirements in [COPYRIGHT.md](COPYRIGHT.md) are followed. Attribution is required. Uses beyond the standard quotation allowance require advance written permission from [hello@twpventures.com](mailto:hello@twpventures.com).

Public access to this repository does not place the translation in the public domain or automatically license the Scripture text, EPUB, branding, or software beyond the permissions expressly stated in [COPYRIGHT.md](COPYRIGHT.md).

---

Published by **The Way Partners LLC**  
[TheWayVersion.com](https://thewayversion.com) · [hello@twpventures.com](mailto:hello@twpventures.com)
