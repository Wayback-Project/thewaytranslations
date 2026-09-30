# 2026-09-30 quotation / punctuation integrity audit

**Status: PROPOSAL / REVIEW ONLY — no Scripture wording or punctuation changed by this audit.**

## Trigger diagnosis — Genesis 20:13

The screenshot-visible ending is not three accidental quote marks. All three closing marks are structurally required by nested quotation levels: the inner double quotation closes Sarah's reported words; the single quotation closes Abraham's quotation to Sarah; and the final double quotation closes Abraham's longer speech. The defect is the inserted spaces between the nested closing marks.

- Current canonical verse: `When Elohim caused me to wander from my father’s house, I said to her, ‘This is your kindness which you shall show to me. Everywhere that we go, say of me, “He is my brother.” ’ ”`
- Proposed typography-only normalization: `When Elohim caused me to wander from my father’s house, I said to her, ‘This is your kindness which you shall show to me. Everywhere that we go, say of me, “He is my brother.”’”`
- Proposed change: remove the two inter-quote spaces only (`.” ’ ”` → `.”’”`). No wording and no quotation level is removed.
- Canonical EPUB contains the exact spaced trigger: **True**

## Canonical-layer checks

- Canonical mobile fallback inventory scanned: **31,102** verse-search records
- EPUB XHTML/HTML members scanned as raw UTF-8: **70**
- EPUB spaced nested-closer sequences: **18**
- EPUB spaces immediately before curly closing quotes: **18**
- EPUB spaces immediately after curly opening quotes: **1**
- EPUB dense contiguous ASCII quote runs (3+ glyphs): **12**
- Canonical editable-source lines containing spaced curly closing-quote pairs: **18**
- Canonical editable-source lines containing dense contiguous ASCII quote runs: **12**

## Whole-Bible candidate scan

The scan deliberately separates deterministic formatting defects from review-only heuristics. Quote counts by themselves are not treated as errors because dialogue can span verses.

- `CONFIRMED_SPACED_NESTED_CLOSERS`: **18 hit(s)** across **18 verse(s)**
- `CONFIRMED_SPACE_BEFORE_CLOSING_QUOTE`: **18 hit(s)** across **18 verse(s)**
- `CONFIRMED_SPACE_AFTER_OPENING_QUOTE`: **1 hit(s)** across **1 verse(s)**
- `CONFIRMED_DENSE_STRAIGHT_QUOTE_RUN`: **12 hit(s)** across **12 verse(s)**
- `CONFIRMED_SPACE_BEFORE_PUNCTUATION`: **0 hit(s)** across **0 verse(s)**
- `CONFIRMED_REPLACEMENT_CHARACTER`: **0 hit(s)** across **0 verse(s)**
- `CONFIRMED_REPEATED_SPACES`: **0 hit(s)** across **0 verse(s)**
- `REVIEW_3PLUS_QUOTES_WITHIN_10_CHARS`: **35 hit(s)** across **31 verse(s)**
- `REVIEW_REPEATED_PUNCTUATION`: **0 hit(s)** across **0 verse(s)**

### Confirmed spaced nested-closer references

Genesis 3:3, Genesis 20:13, Genesis 22:18, Genesis 26:9, Genesis 31:13, Genesis 32:5, Genesis 32:12, Genesis 32:18, Genesis 32:20, Genesis 37:17, Genesis 38:22, Genesis 42:34, Genesis 43:5, Genesis 44:5, Genesis 45:11, Genesis 48:20, Genesis 50:5, Genesis 50:17

### Confirmed dense straight-quote-run references

Exodus 7:18, Exodus 8:23, Exodus 9:4, Exodus 9:19, Isaiah 36:10, Isaiah 37:7, Isaiah 38:8, Ezekiel 29:16, Zechariah 1:17, Zechariah 6:15, Matthew 13:30, Matthew 26:18

These are confirmed malformed punctuation strings, but their intended final quotation nesting is **not** inferred mechanically. Each needs context reconstruction and an explicit Current → Final row before release.

### 3+ quote marks within 10 characters — review queue

Genesis 20:13, Exodus 7:18, Exodus 8:23, Exodus 9:4, Exodus 9:19, Leviticus 18:24, Leviticus 19:4, Leviticus 19:29, Leviticus 19:31, 2 Kings 2:18, Isaiah 29:22, Isaiah 36:10, Isaiah 37:7, Isaiah 37:35, Isaiah 38:8, Ezekiel 29:16, Hosea 2:23, Zechariah 1:17, Zechariah 6:15, Malachi 1:2, Matthew 5:37, Matthew 13:30, Matthew 22:21, Matthew 26:18, Mark 12:16, Luke 18:20, Luke 20:24, John 7:36, John 8:22, James 5:12, Revelation 14:13

### Quote-style inventory (not presumed errors)

- `verses_with_straight_double_quote`: **4245 verse(s)**
- `verses_with_isolated_straight_single_quote`: **656 verse(s)**
- `verses_with_curly_double_quote`: **608 verse(s)**
- `verses_with_curly_single_quote_or_apostrophe`: **1145 verse(s)**
- `verses_mixing_straight_and_curly_double_quotes`: **0 verse(s)**

### Editable-source spaced-closer hits

- `original-documents/genesis_restorative_translation.txt:64` — `3. but not the fruit of the tree which is in the middle of the garden. Elohim has said, ‘You shall not eat of it. You shall not touch it, lest you die.’ ”`
- `original-documents/genesis_restorative_translation.txt:548` — `13. When Elohim caused me to wander from my father’s house, I said to her, ‘This is your kindness which you shall show to me. Everywhere that we go, say of me, “He is my brother.” ’ ”`
- `original-documents/genesis_restorative_translation.txt:609` — `18. All the nations of the earth will be blessed by your offspring, because you have obeyed my voice.’ ”`
- `original-documents/genesis_restorative_translation.txt:754` — `9. Abimelech called Yitzhak, and said, “Look, surely she is your wife. Why did you say, ‘She is my sister’?” Yitzhak said to him, “Because I said, ‘Lest I die because of her.’ ”`
- `original-documents/genesis_restorative_translation.txt:949` — `13. I am the God of Beit El, where you anointed a pillar, where you vowed a vow to me. Now arise, get out from this land, and return to the land of your birth.’ ”`
- `original-documents/genesis_restorative_translation.txt:998` — `5. I have cattle, donkeys, flocks, male servants, and female servants. I have sent to tell my lord, that I may find favor in your sight.’ ”`
- `original-documents/genesis_restorative_translation.txt:1005` — `12. You said, ‘I will surely do you good, and make your offspring as the sand of the sea, which can’t be counted because there are so many.’ ”`
- `original-documents/genesis_restorative_translation.txt:1011` — `18. Then you shall say, ‘They are your servant, Yaakov’s. It is a present sent to my lord, Esav. Look, he also is behind us.’ ”`
- `original-documents/genesis_restorative_translation.txt:1013` — `20. You shall say, ‘Not only that, but look, your servant, Yaakov, is behind us.’ ” For, he said, “I will appease him with the present that goes before me, and afterward I will see his face. Perhaps he will accept me.”`
- `original-documents/genesis_restorative_translation.txt:1175` — `17. The person said, “They have left here, for I heard them say, ‘Let’s go to Dothan.’ ” Yosef went after his brothers, and found them in Dothan.`
- `original-documents/genesis_restorative_translation.txt:1218` — `22. He returned to Yehudah, and said, “I haven’t found her; and also the men of the place said, ‘There has been no prostitute here.’ ”`
- `original-documents/genesis_restorative_translation.txt:1371` — `34. Bring your youngest brother to me. Then I will know that you are not spies, but that you are honest men. So I will deliver your brother to you, and you shall trade in the land.’ ”`
- `original-documents/genesis_restorative_translation.txt:1382` — `5. but if you don’t send him, we won’t go down, for the person said to us, ‘You shall not see my face, unless your brother is with you.’ ”`
- `original-documents/genesis_restorative_translation.txt:1418` — `5. Isn’t this that from which my lord drinks, and by which he indeed divines? You have done brokenness in so doing.’ ”`
- `original-documents/genesis_restorative_translation.txt:1460` — `11. There I will provide for you; for there are yet five years of famine; lest you come to poverty, you, and your household, and all that you have.” ’`
- `original-documents/genesis_restorative_translation.txt:1568` — `20. He blessed them that day, saying, “Yisrael will bless in your name, saying, ‘Elohim make you as Efrayim and as Menashe’ ” He set Efrayim before Menashe.`
- `original-documents/genesis_restorative_translation.txt:1612` — `5. ‘My father made me swear, saying, “Look, I am dying. Bury me in my grave which I have dug for myself in the land of Canaan.” Now therefore, please let me go up and bury my father, and I will come again.’ ”`
- `original-documents/genesis_restorative_translation.txt:1624` — `17. ‘You shall tell Yosef, “Now please forgive the disobedience of your brothers, and their sin, because they did brokenness to you.” ’ Now, please forgive the disobedience of the servants of the God of your father.” Yosef wept when they spoke to him.`

### Editable-source dense straight-quote-run hits

- `original-documents/exodus_to_ecclesiastes_restorative_translation.txt:184` — `18. The fish that are in the river shall die, and the river shall become foul; and the Egyptians shall loathe to drink water from the river."'"`
- `original-documents/exodus_to_ecclesiastes_restorative_translation.txt:216` — `23. I will put a division between my people and your people: by tomorrow shall this sign be."'"`
- `original-documents/exodus_to_ecclesiastes_restorative_translation.txt:231` — `4. YHWH will make a distinction between the livestock of Israel and the livestock of Mitzrayim; and there shall nothing die of all that belongs to the children of Israel."'"`
- `original-documents/exodus_to_ecclesiastes_restorative_translation.txt:246` — `19. Now therefore command that all of your livestock and all that you have in the field be brought into shelter. Everyone and animal that is found in the field, and isn't brought home, the hail shall come down on them, and they shall die."'"`
- `original-documents/matthew_restorative_translation.txt:450` — `30. Let both grow together until the harvest, and in the harvest time I will tell the reapers, "First, gather up the darnel weeds, and bind them in bundles to burn them; but gather the wheat into my barn."'"`
- `original-documents/matthew_restorative_translation.txt:979` — `18. He said, "Go into the city to a certain person, and tell him, 'The Teacher says, "My time is at hand. I will keep the Passover at your house with my disciples."'"`
- `original-documents/rest_of_old_testament_restorative_translation.txt:890` — `10. Have I come up now without YHWH against this land to destroy it? YHWH said to me, "Go up against this land, and destroy it."'"`
- `original-documents/rest_of_old_testament_restorative_translation.txt:911` — `7. Behold, I will put a spirit in him and he will hear news, and will return to his own land. I will cause him to fall by the sword in his own land."'"`
- `original-documents/rest_of_old_testament_restorative_translation.txt:952` — `8. Behold, I will cause the shadow on the sundial, which has gone down on the sundial of Achaz with the sun, to return backward ten steps. So the sun returned ten steps on the sundial on which it had gone down."'"`
- `original-documents/rest_of_old_testament_restorative_translation.txt:3981` — `16. It shall be no more the confidence of the house of Israel, bringing iniquity to memory, when they turn to look after them: and they shall know that I am YHWH God."'"`
- `original-documents/rest_of_old_testament_restorative_translation.txt:5839` — `17. "Proclaim further, saying, 'Thus says YHWH of Armies: "My cities will again overflow with prosperity, and YHWH will again comfort Tzion, and will again choose Yerushalayim."'"`
- `original-documents/rest_of_old_testament_restorative_translation.txt:5916` — `15. Those who are far off shall come and build in the temple of YHWH; and you shall know that YHWH of Armies has sent me to you. This will happen, if you will diligently obey the voice of YHWH your God."'"`

## Review policy and proposed next step

1. Treat `CONFIRMED_SPACED_NESTED_CLOSERS` and the single confirmed opening-boundary space as typography-only candidates: preserve all quote glyphs and wording; remove only the inappropriate inter-quote/interior space after context confirmation.
2. Treat `CONFIRMED_DENSE_STRAIGHT_QUOTE_RUN` as definite corruption, but do not mass-normalize it. Reconstruct each intended quotation level from context and freeze an explicit Current → Final verse string.
3. Treat remaining `REVIEW_*` rows as candidate queues, not release authority; nested dialogue, rhetorical punctuation, and multi-verse quotation spans can be legitimate.
4. Treat the quote-style inventory as a possible future house-style project, not as permission for a mass replacement.
5. For any approved fixes, freeze exact Current → Final verse strings in the Google final-review ledger before release.
6. Apply only the approved finite set to the canonical EPUB/source, then rebuild canonical mobile fallback, Netlify reader/search/mobile feed, and mobile content provenance from the new canonical artifact.
7. Re-run this audit after the correction release and require zero unintended verse-text differences downstream.

## Audit provenance

- Canonical release ID: `canonical-91b1daa6b2f796eb`
- Canonical EPUB SHA-256 in package: `91b1daa6b2f796ebf4fd3c149cf4fabc8faabba796f0063bdb6ab8e0565492d7`
- Web-reader layer parity for the trigger verse is verified separately against the generated Netlify data and recorded in the Google final-review ledger.

