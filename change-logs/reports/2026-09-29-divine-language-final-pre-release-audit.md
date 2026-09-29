# Divine-language final pre-release audit — 2026-09-29

## Status

**GO FOR RELEASE — pending explicit release authorization.**

This report freezes the editorial proposal only. The canonical EPUB and downstream readers remain unchanged at this stage.

- Canonical baseline commit: `ada4a755463f6de6744e5e77070aa78fcc752a33`
- Canonical baseline EPUB SHA-256: `6a3a0dbc91949b082fdcf7c93d0832fe6762440933d8528009cf44b2271dfb92`
- Whole-Bible inventory audited: **31,102 verses**
- Audit rows reviewed: **177**
- Actual release changes: **176 verses across 37 books**
- Audited no-change: **Psalm 45:6**
- Public reference ledger: `change-logs/reports/2026-09-29-divine-language-final-ledger.tsv`
- Public reference-ledger SHA-256: `d0c8b8a4716d45c569a55b07af459cd841b53341a404a2607a352bf0f17c1882`
- Exact before/after release authority: Google final-review table (177 rows; 176 changes + Psalm 45:6 no-change)

## Final decision rule

The Way Version uses a source-faithful, function-preserving divine-language rule:

1. Human kings, human kingdoms, actual human gender, and source-significant male/messianic references remain gendered.
2. Unmistakably divine **King** is rendered **Sovereign** to preserve royal authority without adding an English male-gender assertion.
3. Divine **kingdom** is rendered **reign** only where the context denotes active divine rule/authority. Human geopolitical kingdoms remain **kingdom**; ambiguous royal/messianic contexts are not mechanically changed.
4. Unmistakable divine **he / him / his** is handled by repeating the established divine name/title or by a natural English recast. This pass does not introduce divine **they / she / it**.
5. `YHWH`, `Elohim`, `Cosmic Parent`, and `Abba` retain the project's existing source-controlled rules.
6. Unrelated lexical modernization and grammar cleanup do not ride along with this release unless required by the approved divine-language recast.

## Translation-method comparators

These sources inform method; they are **not** treated as templates that override The Way Version's own source-name rules.

- **Anglican Church of Canada, Inclusive Language Liturgical Psalter** — the official resource describes an inclusive/accessibility goal while retaining fidelity to the psalms, and its task-force report says alternative wording or sentence structure is used to eliminate masculine pronouns for God while retaining human masculine gender where context requires it.  
  https://www.anglican.ca/resources/inclusive-language-psalter/  
  https://www.anglican.ca/wp-content/uploads/009i-Appendix-8.pdf
- **NIV** — methodology comparator only, **not** a direct precedent for `King → Sovereign`. Its official philosophy emphasizes accurate source-language meaning in natural contemporary English and balancing transparency to the original with clarity.  
  https://www.thenivbible.com/about-the-niv/  
  https://thenivbible.com/wp-content/uploads/2023/11/The-Development-and-Use-of-Gender-Language-in-Contemporary-English-Collins-Report.pdf
- **NRSVue** — methodology comparator for rigorous review, readability/accessibility, inclusive language, and the stated principle “as literal as possible, as free as necessary.”  
  https://www.friendshippress.org/pages/about-the-nrsvue

## Audit revisions made before freeze

The audit did not simply approve the original 177-row draft. It changed the proposal where source, referent, or release scope required it.

- **1 Samuel 6:5:** removed the draft's unrelated `peradventure → perhaps` modernization; only the divine-pronoun problem is resolved.
- **Daniel 2:44:** retained the canonical **set up** wording; only `kingdom → reign` is proposed.
- **Romans 1:21:** retained **glorify**; only the divine object pronoun is changed.
- **Jeremiah 23:19:** retained the existing source-supply brackets while changing the divine possessive.
- **Zechariah 2:13:** source-checked the Hebrew/JPS sense and uses **YHWH is aroused from YHWH's holy habitation**, avoiding both the masculine reflexive and an unrelated `arisen/awakened` substitution.
- **Zechariah 9:14:** changes only the divine possessive; the existing `will go flash` grammar remains for a separate grammar/style pass.
- **2 Chronicles 14:13:** source check supports the army/host as YHWH's, so the divine possessive correction remains.
- **Psalm 45:6:** **NO CHANGE**. The royal/messianic wedding-psalm context is not securely divine enough for a mechanical `kingdom → reign` change in this pass.
- **Daniel 7:27:** reclassified from a divine-reign proposal to a source/collective-pronoun correction. The Aramaic/JPS context gives the kingdom to the people/saints of the Most High: **their kingdom ... obey them**, not a divine masculine singular. Source check: https://mechon-mamre.org/p/pt/pt3407.htm

## Release-change totals

| Category | Change rows |
| --- | ---: |
| Divine pronoun | 124 |
| Divine royal title (`King → Sovereign`) | 40 |
| Divine reign terminology (`kingdom → reign` in active-rule contexts) | 11 |
| Source / collective pronoun correction | 1 |
| **Total changes** | **176** |
| Audited no-change | **1** |

## Exact places that will change

### Divine royal titles — 40 rows

Psalms 10:16; Psalms 145:1; Psalms 149:2; Psalms 24:10; Psalms 24:7; Psalms 24:8; Psalms 24:9; Psalms 29:10; Psalms 44:4; Psalms 47:2; Psalms 47:6; Psalms 47:7; Psalms 48:2; Psalms 5:2; Psalms 68:24; Psalms 74:12; Psalms 84:3; Psalms 95:3; Psalms 98:6; Psalms 99:4; Isaiah 33:22; Isaiah 41:21; Isaiah 43:15; Isaiah 44:6; Isaiah 6:5; Jeremiah 10:10; Jeremiah 10:7; Jeremiah 46:18; Jeremiah 48:15; Jeremiah 51:57; Jeremiah 8:19; Daniel 4:37; Zephaniah 3:15; Zechariah 14:16; Zechariah 14:17; Zechariah 14:9; Malachi 1:14; Matthew 5:35; 1 Timothy 1:17; Revelation 15:3

### Divine reign terminology — 11 rows

1 Chronicles 29:11; Psalms 103:19; Psalms 145:11; Psalms 145:12; Psalms 145:13; Psalms 22:28; Daniel 2:44; Daniel 4:3; Daniel 4:34; Daniel 6:26; Obadiah 1:21

### Divine pronouns — 124 rows

Exodus 15:2; Exodus 15:26; Exodus 3:13; Numbers 12:9; Deuteronomy 31:29; Deuteronomy 4:25; Deuteronomy 4:7; Deuteronomy 9:18; Joshua 23:3; Joshua 24:18; Joshua 24:22; Joshua 24:7; Joshua 3:10; Joshua 9:9; Judges 10:16; Judges 10:6; Judges 10:7; Judges 2:14; Judges 2:20; Judges 3:8; 1 Samuel 5:7; 1 Samuel 6:5; 1 Samuel 7:3; 1 Kings 14:22; 1 Kings 16:7; 1 Kings 18:21; 2 Kings 17:17; 2 Kings 17:23; 2 Kings 21:6; 2 Chronicles 12:13; 2 Chronicles 14:13; 2 Chronicles 14:7; 2 Chronicles 15:2; 2 Chronicles 15:4; 2 Chronicles 20:20; 2 Chronicles 29:25; 2 Chronicles 33:6; Ezra 1:2; Ezra 8:22; Ezra 8:23; Ezra 9:8; Job 21:15; Job 4:9; Job 6:9; Isaiah 12:2; Isaiah 12:5; Isaiah 19:20; Isaiah 19:22; Isaiah 25:9; Isaiah 26:21; Isaiah 40:13; Isaiah 40:18; Isaiah 42:10; Isaiah 42:12; Isaiah 8:17; Isaiah 9:17; Jeremiah 13:16; Jeremiah 14:10; Jeremiah 20:13; Jeremiah 23:19; Jeremiah 23:20; Jeremiah 25:31; Jeremiah 4:2; Jeremiah 4:26; Jeremiah 52:3; Jeremiah 9:20; Lamentations 1:15; Lamentations 1:18; Lamentations 2:2; Lamentations 2:8; Lamentations 3:25; Lamentations 4:16; Ezekiel 36:20; Ezekiel 37:1; Ezekiel 3:12; Ezekiel 3:22; Ezekiel 40:1; Daniel 3:17; Daniel 5:23; Daniel 9:10; Hosea 11:10; Hosea 11:7; Hosea 3:5; Hosea 6:1; Hosea 7:10; Amos 7:1; Micah 1:2; Micah 1:3; Micah 4:12; Nahum 1:7; Habakkuk 2:20; Zephaniah 1:18; Zephaniah 1:6; Zephaniah 2:3; Zephaniah 3:9; Zechariah 10:3; Zechariah 2:13; Zechariah 7:12; Zechariah 9:14; Matthew 5:45; Matthew 6:8; Matthew 7:11; Matthew 9:38; Luke 2:38; Luke 3:4; Luke 6:35; John 8:29; John 8:42; Romans 11:21; Romans 11:22; Romans 11:32; Romans 1:21; Romans 3:29; Romans 5:8; 1 Corinthians 3:19; James 4:10; James 4:8; 1 John 5:9; Revelation 10:7; Revelation 16:19; Revelation 16:9; Revelation 7:15; Joel 2:13; Joel 2:23

### Source / collective pronoun correction — 1 row

Daniel 7:27

## Audited no-change

- **Psalm 45:6** — retain the current **kingdom** wording in this pass because the immediate source context is a royal/messianic wedding psalm and the referent is not secure enough for the divine `kingdom → reign` rule.

## Print authority

The public TSV is the complete reference/category/disposition index for all 177 audited places. The **exact before/after print and release authority is the corresponding Google final-review table**. For every one of the 176 release rows, print production must use the **Final text** field. Psalm 45:6 remains unchanged.

The table's before/after strings are the release boundary: no surrounding Scripture wording may change except what is explicitly present in an approved Final text cell.

## Release gate

Editorial audit: **PASS**.

The next release may proceed only after explicit authorization. The release step must:

1. apply exactly the 176 ledger rows to the current canonical EPUB;
2. archive the prior EPUB;
3. validate EPUB ZIP structure, XML, internal links/anchors, and the 31,102-verse inventory;
4. verify exact before/after reconstruction against this frozen ledger;
5. record the new EPUB SHA-256 and release commit;
6. regenerate the canonical mobile fallback from the finished EPUB;
7. only then regenerate the web reader and native mobile content from that finished canonical release;
8. preserve the final ledger, audit report, archived prior EPUB, hashes, and downstream provenance.

No canonical Scripture or downstream reader content is changed by this proposal report itself.
