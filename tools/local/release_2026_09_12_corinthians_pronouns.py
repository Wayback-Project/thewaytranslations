#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import html
import json
import os
import posixpath
import re
import shutil
import tempfile
import urllib.parse
import zipfile
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / "current-form-documents" / "the-way-current.epub"
SOURCE = ROOT / "original-documents" / "rest_of_new_testament_restorative_translation.txt"
LEDGER = ROOT / "change-logs" / "reports" / "2026-09-12-1-corinthians-divine-pronoun-residuals.json"
NOTE = ROOT / "editor-notes" / "consistency" / "2026-09-12-1-corinthians-divine-pronoun-residuals.md"
BOOK_LOG = ROOT / "change-logs" / "new-testament" / "books" / "1-Corinthians.md"
CURRENT_README = ROOT / "current-form-documents" / "README.md"
ROOT_README = ROOT / "README.md"
HISTORY_LOG = ROOT / "rendered-documents-history" / "LOG.md"
BASELINE = "8c41b165e7714730a4139ccee13c00b3c6e149af1e8ee5f00d4b8d5191bd5328"

CHANGES = [
    {
        "reference": "1 Corinthians 1:30",
        "before": "But of him, you are in Messiah Yeshua, who was made to us wisdom from God, and righteousness and sanctification, and redemption:",
        "after": "It is from God that you are in Messiah Yeshua, who was made to us wisdom from God, and righteousness and sanctification, and redemption:",
        "reason": "The masculine pronoun refers to God; repeat the divine referent naturally rather than gendering God.",
    },
    {
        "reference": "1 Corinthians 2:9",
        "before": "But as it is written, \"Things which an eye didn't see, and an ear didn't hear, which didn't enter into the human heart, these God has prepared for those who love him.\"",
        "after": "But as it is written, \"Things which an eye didn't see, and an ear didn't hear, which didn't enter into the human heart, these God has prepared for those who love God.\"",
        "reason": "The final pronoun refers to God; repeat God explicitly.",
    },
    {
        "reference": "1 Corinthians 8:6",
        "before": "yet to us there is one God, the Cosmic Parent, of whom are all things, and we for him; and one Master, Yeshua the Messiah, through whom are all things, and we live through him.",
        "after": "yet to us there is one God, the Cosmic Parent, of whom are all things, and for whom we live; and one Master, Yeshua the Messiah, through whom are all things, and we live through him.",
        "reason": "Remove the masculine pronoun referring to the Cosmic Parent by natural rephrasing; retain the final him because it refers to Yeshua.",
    },
    {
        "reference": "1 Corinthians 9:10",
        "before": "or does he say it assuredly for our sake? Yes, it was written for our sake, because the one who plows ought to plow in hope, and the one who threshes in hope should partake of their hope.",
        "after": "or does God say it assuredly for our sake? Yes, it was written for our sake, because the one who plows ought to plow in hope, and the one who threshes in hope should partake of their hope.",
        "reason": "The immediate antecedent is God in verse 9; repeat God explicitly.",
    },
]

MANUAL_REVIEW = [
    "1 Corinthians 3:19",
    "1 Corinthians 6:16",
    "1 Corinthians 10:22",
    "1 Corinthians 15:27-28",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def visible(inner: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", inner)).replace("\u00a0", " ").strip()


def replace_one(member_text: str, verse_no: str, before: str, after: str):
    pat = re.compile(r"(<(?:[A-Za-z_][\w.-]*:)?p\b[^>]*>)(.*?)(</(?:[A-Za-z_][\w.-]*:)?p>)", re.I | re.S)
    matches = []
    for m in pat.finditer(member_text):
        text = visible(m.group(2))
        if text in (f"{verse_no}. {before}", f"{verse_no}.{before}"):
            matches.append(m)
    if not matches:
        return member_text, 0
    if len(matches) != 1:
        raise RuntimeError(f"multiple paragraph matches in one member for verse {verse_no}: {before[:80]}")
    m = matches[0]
    if re.search(r"<[^>]+>", m.group(2)):
        raise RuntimeError(f"inline markup in target paragraph; refusing rewrite: {before[:80]}")
    rendered = html.escape(f"{verse_no}. {after}", quote=False)
    return member_text[:m.start(2)] + rendered + member_text[m.end(2):], 1


def validate_epub(path: Path) -> tuple[int, int]:
    with zipfile.ZipFile(path, "r") as z:
        if z.testzip() is not None:
            raise RuntimeError("ZIP CRC failure")
        first = z.infolist()[0]
        if first.filename != "mimetype" or first.compress_type != zipfile.ZIP_STORED:
            raise RuntimeError("EPUB mimetype rule failed")
        if z.read("mimetype") != b"application/epub+zip":
            raise RuntimeError("EPUB mimetype content failed")
        names = set(z.namelist())
        ids = {}
        book_members = []
        chapter_count = 0
        for name in z.namelist():
            if name.lower().endswith((".xhtml", ".html", ".htm", ".opf", ".ncx", ".xml")):
                raw = z.read(name)
                ET.fromstring(raw)
                text = raw.decode("utf-8", "ignore")
                ids[name] = set(re.findall(r"\bid=[\"']([^\"']+)", text))
                cc = len(re.findall(r"\bid=[\"']ch-", text))
                if cc:
                    book_members.append(name)
                    chapter_count += cc
                if "<<" in text or ">>" in text:
                    raise RuntimeError(f"angle-marker artifact in {name}")
        if len(book_members) != 66:
            raise RuntimeError(f"expected 66 book XHTML members, got {len(book_members)}")
        if chapter_count != 1189:
            raise RuntimeError(f"expected 1189 chapter anchors, got {chapter_count}")
        unresolved = []
        for src in ids:
            text = z.read(src).decode("utf-8", "ignore")
            for href in re.findall(r"\bhref=[\"']([^\"']+)", text):
                if not href or href.startswith(("http:", "https:", "mailto:", "data:", "javascript:")):
                    continue
                path_part, sep, frag = href.partition("#")
                target = src if not path_part else posixpath.normpath(posixpath.join(posixpath.dirname(src), urllib.parse.unquote(path_part)))
                if target not in names:
                    unresolved.append((src, href, "missing member"))
                    continue
                if sep and frag and target in ids and urllib.parse.unquote(frag) not in ids[target]:
                    unresolved.append((src, href, "missing fragment"))
        if unresolved:
            raise RuntimeError(f"unresolved internal links: {unresolved[:10]}")
        return len(book_members), chapter_count


def main() -> None:
    actual = sha256(EPUB)
    if actual != BASELINE:
        # Idempotent no-op is allowed only when all requested after-values are already present.
        with zipfile.ZipFile(EPUB, "r") as z:
            corpus = "\n".join(visible(z.read(n).decode("utf-8", "ignore")) for n in z.namelist() if n.lower().endswith((".xhtml", ".html", ".htm")))
        if all(c["after"] in corpus for c in CHANGES):
            print(json.dumps({"status": "already-applied", "sha256": actual}, indent=2))
            return
        raise SystemExit(f"baseline SHA mismatch: expected {BASELINE}, got {actual}")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%MUTC")
    archive_dir = ROOT / "rendered-documents-history" / stamp
    archive_dir.mkdir(parents=True, exist_ok=False)
    archive = archive_dir / EPUB.name
    shutil.copy2(EPUB, archive)
    if sha256(archive) != BASELINE:
        raise RuntimeError("archive SHA mismatch")

    with zipfile.ZipFile(EPUB, "r") as zin:
        infos = zin.infolist()
        original = {i.filename: zin.read(i.filename) for i in infos}
    edited = dict(original)
    applied = []
    changed_members = set()

    for change in CHANGES:
        ref = change["reference"]
        verse_no = ref.rsplit(":", 1)[1]
        found = []
        for name, data in list(edited.items()):
            if not name.lower().endswith((".xhtml", ".html", ".htm")):
                continue
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                continue
            new_text, count = replace_one(text, verse_no, change["before"], change["after"])
            if count:
                found.append(name)
                edited[name] = new_text.encode("utf-8")
                changed_members.add(name)
        if len(found) != 1:
            raise RuntimeError(f"{ref}: expected exactly one EPUB paragraph match, got {found}")
        applied.append({"reference": ref, "member": found[0]})

    # Keep the text mirror synchronized for the exact affected verses.
    source_text = SOURCE.read_text(encoding="utf-8")
    for change in CHANGES:
        old = f'{change["reference"].split(":")[-1]}. {change["before"]}'
        new = f'{change["reference"].split(":")[-1]}. {change["after"]}'
        count = source_text.count(old)
        if count != 1:
            raise RuntimeError(f'{change["reference"]}: expected one source-text match, got {count}')
        source_text = source_text.replace(old, new, 1)
    SOURCE.write_text(source_text, encoding="utf-8")

    fd, tmpname = tempfile.mkstemp(suffix=".epub", dir=str(EPUB.parent))
    os.close(fd)
    tmp = Path(tmpname)
    try:
        with zipfile.ZipFile(tmp, "w") as zout:
            for info in infos:
                data = edited[info.filename]
                zout.writestr(info, data, compress_type=info.compress_type)
        validate_epub(tmp)
        shutil.move(tmp, EPUB)
    finally:
        if tmp.exists():
            tmp.unlink()

    newsha = sha256(EPUB)
    if newsha == BASELINE:
        raise RuntimeError("release SHA did not change")
    changed_content = [n for n in original if original[n] != edited[n]]
    if set(changed_content) != changed_members:
        raise RuntimeError("unexpected uncompressed member changes")
    if len(changed_members) != 1:
        raise RuntimeError(f"expected one affected book XHTML member, got {sorted(changed_members)}")

    report = {
        "release": "2026-09-12 1 Corinthians divine-pronoun residuals",
        "prior_epub_sha256": BASELINE,
        "released_epub_sha256": newsha,
        "archive_path": archive.relative_to(ROOT).as_posix(),
        "change_count": len(CHANGES),
        "changes": CHANGES,
        "applied": applied,
        "manual_review_retained": MANUAL_REVIEW,
        "qa": {
            "book_count": 66,
            "chapter_count": 1189,
            "zip_crc": "pass",
            "xml_parse": "pass",
            "internal_links": "pass",
            "changed_book_members": sorted(changed_members),
        },
    }
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    NOTE.parent.mkdir(parents=True, exist_ok=True)
    NOTE.write_text(f"""# 1 Corinthians divine-pronoun residual cleanup — 2026-09-12

This release applies four high-confidence residual fixes under the active divine-gender policy. Divine masculine pronouns are not mechanically converted to plural or feminine pronouns; where the antecedent is unmistakably God/Cosmic Parent, the divine referent is repeated or the clause is naturally rephrased. Masculine pronouns that refer to Yeshua remain.

## Released changes

- 1 Corinthians 1:30 — `But of him...` → `It is from God that...`
- 1 Corinthians 2:9 — `those who love him` → `those who love God`
- 1 Corinthians 8:6 — `and we for him` → `and for whom we live`; the final `through him` remains because it refers to Yeshua.
- 1 Corinthians 9:10 — `does he say` → `does God say`

The context-sensitive candidates at 1 Corinthians 3:19, 6:16, 10:22, and 15:27–28 remain for a separate clause-by-clause residual audit rather than being changed mechanically.

## Artifact

- Prior SHA-256: `{BASELINE}`
- Released SHA-256: `{newsha}`
- Prior EPUB archive: `{archive.relative_to(ROOT).as_posix()}`
- Coverage: 66 books / 1,189 chapters
- Exact ledger: `change-logs/reports/2026-09-12-1-corinthians-divine-pronoun-residuals.json`
""", encoding="utf-8")

    entry = f"""
## 2026-09-12 — Divine-pronoun residual cleanup
- Scope: 1 Corinthians 1:30; 2:9; 8:6; 9:10.
- Rule: when a masculine pronoun unmistakably refers to God/Cosmic Parent, repeat the divine referent or naturally rephrase; do not mechanically pluralize or feminize. Yeshua-referent masculine pronouns remain.
- Canonical EPUB SHA-256: `{newsha}`.
- Exact ledger: `change-logs/reports/2026-09-12-1-corinthians-divine-pronoun-residuals.json`.
"""
    current_log = BOOK_LOG.read_text(encoding="utf-8")
    if "## 2026-09-12 — Divine-pronoun residual cleanup" not in current_log:
        BOOK_LOG.write_text(current_log.rstrip() + "\n" + entry, encoding="utf-8")

    cr = CURRENT_README.read_text(encoding="utf-8").replace(BASELINE, newsha)
    cr = re.sub(r"\| Previous release \| Archived under `rendered-documents-history/[^`]+/` \|", f"| Previous release | Archived under `{archive_dir.relative_to(ROOT).as_posix()}/` |", cr)
    cr = cr.replace(
        "This EPUB includes the completed whole-Bible divine-pronoun consistency update and the 2026-09-11 original-name / Genesis narrative consistency update (39 reviewed verse-level edits);",
        "This EPUB includes the completed whole-Bible divine-pronoun consistency update, the 2026-09-11 original-name / Genesis narrative consistency update (39 reviewed verse-level edits), and the 2026-09-12 1 Corinthians divine-pronoun residual cleanup (4 reviewed verse-level edits);",
    )
    CURRENT_README.write_text(cr, encoding="utf-8")

    rr = ROOT_README.read_text(encoding="utf-8").replace(BASELINE, newsha)
    ROOT_README.write_text(rr, encoding="utf-8")

    history = HISTORY_LOG.read_text(encoding="utf-8").rstrip()
    row = f'| {stamp} | {archive_dir.relative_to(ROOT).as_posix()}/ | the-way-current.epub (SHA-256 `{BASELINE}`) | Archive prior canonical EPUB before 1 Corinthians divine-pronoun residual cleanup; 4 reviewed verse-level edits. |'
    if row not in history:
        history += "\n" + row
    HISTORY_LOG.write_text(history + "\n", encoding="utf-8")

    print(json.dumps({"status": "released", "new_sha256": newsha, "archive": archive.relative_to(ROOT).as_posix(), "changes": len(CHANGES), "changed_members": sorted(changed_members)}, indent=2))


if __name__ == "__main__":
    main()
