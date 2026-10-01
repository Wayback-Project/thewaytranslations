# Genesis 44:5 editable-source alignment

**Status:** resolved 2026-10-01.

The released canonical Scripture already reads:

> Isn’t this that from which my lord drinks, and by which he indeed divines? You have done wrong in so doing.’”

The editable Genesis source had retained the older wording `You have done brokenness in so doing.` This was source drift only. The September 14 contextual lexical cleanup had already established `wrong` here, and the later September 26 direct `evil → brokenness / broken` release explicitly did not authorize replacing already-contextualized wording such as `wrong`.

The Hebrew clause uses the finite verb הֲרֵעֹתֶם ("you have done evil/wrong"), so `You have done wrong` is the natural English verbal rendering and is consistent with the project’s contextual methodology.

## Resolution

- `original-documents/genesis_restorative_translation.txt` is aligned to `wrong`.
- Canonical EPUB wording is unchanged.
- Canonical EPUB SHA-256 remains `a1493bfd9f38181c5e552880f7156ef609a8e83550ee459d9ed01db4b3db1c89`.
- No downstream Scripture regeneration is required because the EPUB, web reader, downloadable EPUB, and mobile content feed already contain the correct `wrong` wording.
