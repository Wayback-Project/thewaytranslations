#!/usr/bin/env python3
"""Audit editable Way Version Scripture for masculine-pronoun consistency candidates.

This script is diagnostic only. It never rewrites Scripture. It inventories masculine
pronouns with immediate verse context and flags legacy << >> header markers in both
editable sources and the current EPUB so editorial review can be exhaustive and
context-first.
"""

from __future__ import annotations

import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "original-documents"
EPUB = ROOT / "current-form-documents" / "the-way-current.epub"
OUT = ROOT / "audit-output"

PRONOUN_RE = re.compile(r"\b(?:He|Him|His|Himself|he|him|his|himself)\b")
CHAPTER_RE = re.compile(r"^(.+?)\s+(\d+)\s*$")
VERSE_RE = re.compile(r"^(\d+)\.\s*(.*)$")
DIVINE_TERMS = (
    "YHWH", "Elohim", "God", "Cosmic Parent", "Ruach", "the Master",
    "Master", "Creator", "Most High", "Almighty", "Holy One"
)


def parse_file(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    verses: list[dict] = []
    book = None
    chapter = None
    for line_no, line in enumerate(lines, 1):
        stripped = line.strip()
        ch = CHAPTER_RE.match(stripped)
        if ch and not VERSE_RE.match(stripped):
            book, chapter = ch.group(1), int(ch.group(2))
            continue
        vm = VERSE_RE.match(stripped)
        if vm and book and chapter:
            verses.append({
                "file": str(path.relative_to(ROOT)),
                "line": line_no,
                "book": book,
                "chapter": chapter,
                "verse": int(vm.group(1)),
                "text": stripped,
            })
    return verses


def divine_terms(text: str) -> list[str]:
    return [term for term in DIVINE_TERMS if term in text]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    all_verses: list[dict] = []
    angle_artifacts: list[dict] = []

    for path in sorted(SOURCE_DIR.glob("*_restorative_translation.txt")):
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            if "<<" in line or ">>" in line:
                angle_artifacts.append({
                    "location": str(path.relative_to(ROOT)),
                    "line": line_no,
                    "text": line.strip(),
                })
        all_verses.extend(parse_file(path))

    candidates: list[dict] = []
    for i, verse in enumerate(all_verses):
        matches = PRONOUN_RE.findall(verse["text"])
        if not matches:
            continue
        prev_text = all_verses[i - 1]["text"] if i and all_verses[i - 1]["book"] == verse["book"] else ""
        next_text = all_verses[i + 1]["text"] if i + 1 < len(all_verses) and all_verses[i + 1]["book"] == verse["book"] else ""
        same_terms = divine_terms(verse["text"])
        prev_terms = divine_terms(prev_text)
        next_terms = divine_terms(next_text)
        candidates.append({
            **verse,
            "reference": f'{verse["book"]} {verse["chapter"]}:{verse["verse"]}',
            "pronouns": matches,
            "same_divine_terms": same_terms,
            "prev_divine_terms": prev_terms,
            "next_divine_terms": next_terms,
            "prev": prev_text,
            "next": next_text,
            "triage_score": len(same_terms) * 3 + len(prev_terms) * 2 + len(next_terms),
        })

    if EPUB.exists():
        with zipfile.ZipFile(EPUB) as zf:
            for name in zf.namelist():
                if not name.lower().endswith((".xhtml", ".html", ".htm")):
                    continue
                try:
                    text = zf.read(name).decode("utf-8")
                except UnicodeDecodeError:
                    continue
                if "<<" in text or ">>" in text:
                    for line_no, line in enumerate(text.splitlines(), 1):
                        if "<<" in line or ">>" in line:
                            angle_artifacts.append({
                                "location": f"EPUB:{name}",
                                "line": line_no,
                                "text": line.strip()[:1000],
                            })

    per_book = Counter(c["book"] for c in candidates)
    per_file = Counter(c["file"] for c in candidates)
    high_context = [c for c in candidates if c["triage_score"] >= 3]

    payload = {
        "candidate_count": len(candidates),
        "high_context_count": len(high_context),
        "angle_artifact_count": len(angle_artifacts),
        "per_book": dict(sorted(per_book.items())),
        "per_file": dict(sorted(per_file.items())),
        "candidates": candidates,
        "angle_artifacts": angle_artifacts,
    }
    (OUT / "divine-pronoun-audit.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Whole-Bible divine-pronoun audit",
        "",
        f"Pronoun candidate verses: **{len(candidates)}**",
        f"Candidates with an explicit divine term in immediate context: **{len(high_context)}**",
        f"Legacy `<<` / `>>` artifacts in editable Scripture/current EPUB: **{len(angle_artifacts)}**",
        "",
        "## Candidate counts by book",
        "",
    ]
    for book, count in sorted(per_book.items()):
        lines.append(f"- {book}: {count}")
    lines.extend(["", "## Angle-marker artifacts", ""])
    if angle_artifacts:
        for item in angle_artifacts:
            lines.append(f'- `{item["location"]}:{item["line"]}` — {item["text"]}')
    else:
        lines.append("None found.")
    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "candidate_count": len(candidates),
        "high_context_count": len(high_context),
        "angle_artifact_count": len(angle_artifacts),
    }, indent=2))


if __name__ == "__main__":
    main()
