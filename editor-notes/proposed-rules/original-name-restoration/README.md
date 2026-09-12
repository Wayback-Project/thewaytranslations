# Whole-Bible Original-Name Restoration & Reader Metadata Proposal — 2026-09-12

**Status:** Proposed — editorial review required. **No Scripture wording is changed by this document.**

## Purpose

This proposal extends the existing original-name consistency work from a small set of obvious corrections into a repeatable whole-Bible process. It addresses three related needs:

1. restore conventional person and place names consistently where the project intends a source-near form;
2. keep pronunciation, familiar-name aliases, and reader-guide metadata synchronized with approved forms; and
3. prevent downstream readers from becoming a second, independently edited Bible text.

The canonical Scripture artifact remains `current-form-documents/the-way-current.epub`. Any future name restoration must be approved and released through the repository's normal editorial, change-log, archive, and QA workflow.

## Governing principles

- **Canonical first.** Scripture wording is changed only in the canonical translation/release workflow.
- **Reference-scoped edits, not blanket string replacement.** Identity, place-name compounds, book titles, demonyms, and ordinary-word collisions must be reviewed in context.
- **One approved identity record.** Each restored entity should have a stable metadata record from which familiar-name aliases, pronunciation cues, and reader metadata can be generated downstream.
- **Book titles are separate editorial decisions.** A person's name may be restored without automatically renaming a biblical book.
- **Exceptions are explicit.** If a familiar form is intentionally retained, record the reason instead of allowing accidental inconsistency.
- **Generated reader Scripture is not hand-edited.** Downstream products must be rebuilt from the canonical release artifact.

## Highest-priority person-name proposals

The following are proposed review targets from the second-pass audit. Pronunciations are practical reader cues, not claims that one exact ancient pronunciation can always be reconstructed.

| Current form | Proposed form | Practical pronunciation | Review note |
|---|---|---|---|
| Michael | **Mikha'el** | mee-khah-EL | 15 current occurrences; approve one form across Hebrew Bible and NT identities unless a documented exception applies. |
| Ishmael | **Yishmael** | yish-mah-EL | Existing edition already uses `Yishmael`; normalize remaining conventional occurrences by identity. |
| Adonijah | **Adoniyahu** | ah-do-nee-YAH-hoo | Review all identities before release. |
| Abishai | **Avishai** | ah-vee-SHY | Fits the project's existing `Av-` transliteration pattern. |
| Abiathar | **Evyatar** | ev-yah-TAR | Review possessives and all priestly references together. |
| Abijah | **Aviyah** | ah-vee-YAH | Existing edition already uses `Aviyah`; strong consistency candidate. |
| Amminadab | **Amminadav** | ah-mee-nah-DAHV | Existing edition already uses `Amminadav`. |
| Nahshon | **Nachshon** | nakh-SHONE | Existing edition already uses `Nachshon`. |
| Jehoash | **Yoash** | yoh-AHSH | Existing edition already uses `Yoash`; strong consistency candidate. |
| Phinehas | **Pinchas** | peen-KHAHS | Proposed Hebrew-near form; review all identities. |
| Jethro | **Yitro** | YIT-roh | Proposed Hebrew-near form. |
| Laban | **Lavan** | lah-VAHN | Proposed Hebrew-near form. |
| Zachariah | **Zekharyah** | zeh-khar-YAH | Scope to the person references; do not treat book headings as automatic targets. |
| Aquila | **Akylas** | ah-KOO-lahs | Greek-person-name proposal. |
| Priscilla | **Priskilla** | prees-KEEL-lah | Keep `Prisca` as a separate identity/form review rather than blindly expanding it. |
| Silvanus | **Silvanos** | seel-vah-NOS | Greek-person-name proposal. |
| Luke (person) | **Lukas** | LOO-kahs | Person references only unless a separate book-title policy is approved. |
| Nehemiah (person) | **Nechemyah** | neh-khem-YAH | Person references only unless a separate book-title policy is approved. |

## Highest-priority place-name proposals

| Current form | Proposed form | Practical pronunciation | Review note |
|---|---|---|---|
| Sodom | **Sedom** | seh-DOHM | High-priority Hebrew place-name normalization. |
| Gomorrah | **Amora** | ah-moh-RAH | High-priority Hebrew place-name normalization. |
| Canaan | **Kena'an / Kna'an** | keh-nah-AHN | Editorial spelling decision required before any change; also review Canaanite-family derivatives. |
| Caesarea | **Kaisareia** | kai-sar-AY-ah | Fits the edition's Greek-place pattern such as `Ephesos`, `Korinthos`, and `Antiocheia`. |
| Colossae | **Kolosai** | koh-loh-SAI | Greek-place proposal. |
| Ashkelon | **Ashqelon** | ash-keh-LONE | Review whether the source-near spelling adds enough value to justify visible change. |

## Systematic `Beth` → `Beit` place-name review

The edition already uses `Beit` in established forms such as `Beit El`, `Beit Lechem`, `Beit Anya`, and `Beit Tzaida`, while many other genuine place names still retain `Beth`. This should be handled as a **place-by-place audit**, never a global `Beth` string replacement.

Priority examples:

| Current place | Proposed form | Practical pronunciation |
|---|---|---|
| Beth Shemesh | **Beit Shemesh** | bayt SHEH-mesh |
| Beth Horon | **Beit Horon** | bayt kho-RONE |
| Beth Peor | **Beit Peor** | bayt peh-ORE |
| Beth Jeshimoth | **Beit HaYeshimot** | bayt hah-yeh-shee-MOTE |
| Beth Shean / Beth Shan | **Beit She'an** | bayt sheh-AHN |
| Beth Dagon | **Beit Dagon** | bayt dah-GONE |
| Beth Nimrah | **Beit Nimrah** | bayt neem-RAH |
| Beth Arabah | **Beit HaAravah** | bayt hah-ah-rah-VAH |
| Beth Tappuah | **Beit Tappuach** | bayt tah-POO-akh |
| Beth Gader | **Beit Gader** | bayt gah-DER |
| Beth Rapha | **Beit Rapha** | bayt rah-FAH |
| Beth Aven | **Beit Aven** | bayt AH-ven |
| Beth Kar | **Beit Kar** | bayt KAR |
| Beth Arbel | **Beit Arbel** | bayt ar-BEL |
| Beth Marcaboth | **Beit Markavot** | bayt mar-kah-VOTE |
| Beth Lebaoth | **Beit Lebaot** | bayt leh-bah-OTE |
| Beth Biri | **Beit Biri** | bayt bee-REE |
| Atroth Beth Yoav | **Atrot Beit Yoav** | ah-TROTE bayt yoh-AHV |

Before changing any of these, generate an exact occurrence inventory and classify every `Beth` token as a place-name target, personal-name/non-place token, or intentional exception.

## Already-restored forms that need reader-guide / alias coverage

These do **not** require Scripture wording changes merely to add reader guidance. They should receive familiar-name aliases and pronunciation metadata if not already present downstream.

| Way Version form | Familiar form | Practical pronunciation |
|---|---|---|
| Rakhel | Rachel | rah-KHEL |
| Hananyah | Ananias | hah-nahn-YAH |
| Yochana | Joanna | yoh-khah-NAH |
| Shoshana | Susanna | shoh-shah-NAH |
| Yair | Jair / Jairus | yah-EER |
| Shalem | Salem | shah-LEM |
| Mattityah | Matthias | maht-tee-YAH |

**Acts 1 alias correction for the text-version handoff:** Acts 1:23 and Acts 1:26 use `Mattityah` for the apostle chosen to replace Yehuda/Judas. The familiar/traditional English alias for this identity is **Matthias**. Do **not** map this Acts 1 identity to *Mattithiah* or *Mattathias*. This is an alias/metadata correction for the reader and text-version update sheet; the Scripture form `Mattityah` itself is not changed by this note.

## Additional high-priority consistency backlog

The existing glossary inversion and corpus audit also surfaced conventional forms where a restored mapping already exists or where consistency should be reviewed next. These include, among others:

- Obed → Oved
- Joram / Jehoram → Yoram
- Uzziah → Uzziyah
- Jotham → Yotam
- Zerubbabel → Zerubavel
- Zerah → Zerach
- Jonah → Yonah
- Perez → Peretz
- Hezron → Chetzron
- Ruth → Rut
- Melchizedek → Malki-Tzedek
- Shealtiel → She'altiel
- Syria → Aram where the contextual referent supports it
- Jeconiah → Yekhonyahu
- Hosea → Hoshea
- Abram → Avram
- Jesus → Yeshua
- Babylon → Bavel
- Nazareth → Natzeret

The corpus also contains four `YAHWEH` forms while the edition normally uses `YHWH`. Review those references individually and normalize them unless the spelling is deliberately preserved for a quotation, inscription, or other documented reason.

## Collision and scope rules

The audit must preserve identity rather than matching strings blindly. Examples:

- `Noah` can refer to the patriarch or a different biblical person; identity controls the target form.
- `Abel` can be the person Hevel or part of a place name such as Abel Meholah.
- `Israel/Yisrael` can refer to a person, people, nation, or geographic/political referent.
- `Mark` can be a personal name or an ordinary English word.
- `Luke` and `Nehemiah` can identify persons while also appearing as book titles.
- `James/Jacob`, `Judah/Judas/Jude/Judea`, and `Saul/Paul/Shaul` need scoped alias handling rather than one-string replacement rules.

## Proposed canonical metadata record

Approved naming metadata should live with the canonical editorial/release process. A logical record should support at least:

```json
{
  "id": "michael",
  "term": "Mikha'el",
  "traditionalAliases": ["Michael"],
  "category": "person",
  "original": {
    "hebrew": "מִיכָאֵל",
    "greek": "Μιχαήλ"
  },
  "pronunciationDisplay": "mee-khah-EL",
  "searchAliases": ["Michael", "Mikhael"],
  "scope": [],
  "editorialStatus": "proposed",
  "notes": "Approve exact project spelling before Scripture edits."
}
```

The exact file name/schema is an implementation choice, but the authoritative mapping should not be split across independent hand-maintained reader lists.

## Canonical implementation process

For each approved batch:

1. **Audit exact references.** Produce a before/after ledger with identity and collision checks.
2. **Editorially approve forms.** Record the source evidence, display form, pronunciation, aliases, scope, and any exceptions.
3. **Apply only approved reference-scoped Scripture edits.** Do not globally replace ambiguous strings.
4. **Archive the prior canonical EPUB** under the established UTC-stamped history folder.
5. **Rebuild** `current-form-documents/the-way-current.epub` from the reviewed source state.
6. **Record the release** in `editor-notes/consistency/`, the appropriate `change-logs/` report/ledger, and `rendered-documents-history/LOG.md`.
7. **Run full canonical QA:** EPUB container/XML integrity, checksum, 66-book/1,189-chapter coverage, links, verse inventory, exact post-change assertions, and explicit collision/exception assertions.
8. **Only after canonical QA passes**, synchronize the exact released artifact and approved metadata to downstream reader/mobile consumers. Downstream generated Scripture data must be rebuilt rather than hand-edited.

## Release gates for a future implementation

A release should not be called complete until:

- every changed name has an approved identity/form and source rationale;
- every exception is explicit;
- the exact before/after ledger passes;
- canonical EPUB checksum and coverage QA pass;
- the prior EPUB is archived according to existing policy;
- pronunciation and familiar-name aliases exist for every newly approved restored form that is exposed to reader guidance;
- downstream consumers can prove they were generated from the exact canonical release rather than an independently edited copy.

## Non-goals of this proposal

- It does not approve every item in the broader proper-name review queue.
- It does not make any Scripture change by itself.
- It does not authorize blanket replacements.
- It does not rename biblical book titles automatically.
- It does not move reader/search implementation code into the translation repository.
- It does not treat heuristic capitalized-word inventories as editorial authority.

## Related canonical records

- Existing released original-name consistency note: [`editor-notes/consistency/2026-09-11-original-name-consistency.md`](../../consistency/2026-09-11-original-name-consistency.md)
- Existing diagnostic original-name audit: [`change-logs/reports/2026-09-11-original-name-audit.md`](../../../change-logs/reports/2026-09-11-original-name-audit.md)
- Proposal log entry: [`editor-notes/proposed-rules/2026-09.md`](../2026-09.md)
- Proposal audit record: [`change-logs/reports/2026-09-12-original-name-restoration-proposal.md`](../../../change-logs/reports/2026-09-12-original-name-restoration-proposal.md)
