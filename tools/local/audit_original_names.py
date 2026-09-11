#!/usr/bin/env python3
"""Audit early-Genesis/original-name forms in the canonical current-form EPUB.

Diagnostic only: this script never rewrites Scripture.
"""
from __future__ import annotations

import collections
import html
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / "current-form-documents" / "the-way-current.epub"
OUT = ROOT / "change-logs" / "reports" / "2026-09-11-original-name-audit.md"

PAIRS = [
    ("Adam", "Adam"),
    ("Eve", "Havvah"),
    ("Cain", "Qayin"),
    ("Abel", "Hevel"),
    ("Noah", "Noach"),
    ("Seth", "Shet"),
    ("Enoch", "Chanokh"),
    ("Enosh", "Enosh"),
]
TOKENS = sorted({x for pair in PAIRS for x in pair} | {"human", "person", "man", "woman"}, key=len, reverse=True)

def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).replace("\u00a0", " ").strip()

def extract_paragraphs(xhtml: str):
    return [strip_tags(x) for x in re.findall(r"<p\b[^>]*>(.*?)</p>", xhtml, flags=re.I|re.S)]

def main() -> None:
    if not EPUB.exists():
        raise SystemExit(f"Missing canonical EPUB: {EPUB}")
    counts = collections.Counter()
    hits = []
    genesis_2_5 = []
    with zipfile.ZipFile(EPUB) as zf:
        for member in zf.namelist():
            if not member.lower().endswith((".xhtml", ".html", ".htm")):
                continue
            try:
                raw = zf.read(member).decode("utf-8")
            except UnicodeDecodeError:
                continue
            paras = extract_paragraphs(raw)
            current_chapter = ""
            for p in paras:
                if re.fullmatch(r"[1-3]?\s*[A-Za-z][A-Za-z '\-]+\s+\d+", p):
                    current_chapter = p
                    continue
                if not re.match(r"^\d+\.\s", p):
                    continue
                for t in TOKENS:
                    counts[t] += len(re.findall(rf"(?<![A-Za-z]){re.escape(t)}(?![A-Za-z])", p, flags=re.I if t in {"human","person","man","woman"} else 0))
                if any(re.search(rf"(?<![A-Za-z]){re.escape(t)}(?![A-Za-z])", p) for t in ["Adam","Eve","Havvah","Cain","Qayin","Abel","Hevel","Noah","Noach","Seth","Shet","Enoch","Chanokh","Enosh"]):
                    hits.append((current_chapter or member, p))
                if current_chapter in {"Genesis 2","Genesis 3","Genesis 4","Genesis 5"}:
                    genesis_2_5.append((current_chapter, p))

    lines = [
        "# Original-name / early Genesis audit",
        "",
        f"Canonical input: `current-form-documents/the-way-current.epub`",
        "",
        "This is a diagnostic report only. It does not rewrite Scripture.",
        "",
        "## Whole-Bible form counts",
        "",
        "| Traditional/current form | Restored candidate | Traditional count | Restored count |",
        "|---|---|---:|---:|",
    ]
    for traditional, restored in PAIRS:
        lines.append(f"| {traditional} | {restored} | {counts[traditional]} | {counts[restored]} |")
    lines += [
        "",
        "## Genesis 2–5 context",
        "",
    ]
    last = None
    for chapter, verse in genesis_2_5:
        if chapter != last:
            lines += [f"### {chapter}", ""]
            last = chapter
        lines.append(f"- {verse}")
    lines += ["", "## Whole-Bible name hits", ""]
    for chapter, verse in hits:
        lines.append(f"- **{chapter}** — {verse}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    for traditional, restored in PAIRS:
        print(traditional, counts[traditional], restored, counts[restored])

if __name__ == "__main__":
    main()
