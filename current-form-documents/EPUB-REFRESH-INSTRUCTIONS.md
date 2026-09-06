# EPUB Refresh Instructions

Binary EPUB files are intentionally not updated in normal pull requests, because the repository review flow cannot display binary EPUB diffs reliably.

When a binary-capable editor or release process is ready to refresh the current outputs after source-text changes:

1. Start from the text sources in `original-documents/`.
2. Rebuild both current EPUB artifacts:
   - `current-form-documents/the-way-current.epub`
   - `current-form-documents/newtestament.epub`
3. Before replacing the current EPUBs, archive the existing files under `rendered-documents-history/<YYYY-MM-DD_HHMMUTC>/`.
4. Append a row to `rendered-documents-history/LOG.md` describing the archive snapshot and refresh reason.
5. Validate the EPUB zip containers, for example:

```bash
python3 - <<'PY'
import zipfile
for path in [
    'current-form-documents/the-way-current.epub',
    'current-form-documents/newtestament.epub',
]:
    with zipfile.ZipFile(path) as epub:
        assert epub.testzip() is None, path
        print(f'{path}: OK')
PY
```

## September 2026 refresh status

The verified whole-Bible EPUB was refreshed from the application release and synchronized back into the editable source documents. The current artifact must have SHA-256 `dbd8cace51a0e726a2d910622af995d490ee4f24f76eb7efcd0e5a1756c1119e`.

The refresh includes the July 2026 Yeshua-sayings work listed below and the accepted source-sensitive terminology rule: `satan` / `ha-satan` / `Satanas` → **the Adversary**; `diabolos` → **the Slanderer**; `daimonion` remains **demon**.

## Changes included in the refreshed EPUB

The July 2026 Yeshua-sayings pass changed the source text and documentation only. The next EPUB refresh should include these source changes, especially:

- Matthew 6:13 and Luke 11:4: trial too great / sour and corrupt rescue language.
- Luke 14:26: `sana` as placing family and life behind the Way rather than literal hatred.
- John 16:24: “set your trap” in the vibration Yeshua carries, preserving the video-script receiving-space metaphor.
- John 14–16, Matthew 7, and Mark 11: intentional seeking / living-name language.
