#!/usr/bin/env python3
"""Audit proposed original-name/place candidates against the canonical EPUB.

Diagnostic only: this script never rewrites Scripture or the EPUB. It reads
editor-notes/proposed-rules/original-name-restoration/directory/manifest.json
plus the listed JSON sets and emits occurrence reports for editorial review.
"""
from __future__ import annotations

import collections
import html
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / "current-form-documents" / "the-way-current.epub"
DIRECTORY_DIR = ROOT / "editor-notes" / "proposed-rules" / "original-name-restoration" / "directory"
MANIFEST = DIRECTORY_DIR / "manifest.json"
OUT_MD = ROOT / "change-logs" / "reports" / "PROPOSED-ORIGINAL-NAME-DIRECTORY-AUDIT.md"
OUT_JSON = ROOT / "change-logs" / "reports" / "PROPOSED-ORIGINAL-NAME-DIRECTORY-AUDIT.json"


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    return html.unescape(value).replace("\u00a0", " ").strip()


def extract_paragraphs(xhtml: str) -> list[str]:
    return [strip_tags(value) for value in re.findall(r"<p\b[^>]*>(.*?)</p>", xhtml, flags=re.I | re.S)]


def token_pattern(term: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])")


def load_directory() -> dict:
    if not MANIFEST.exists():
        raise SystemExit(f"Missing proposal directory manifest: {MANIFEST}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = []
    for file_name in manifest.get("files", []):
        path = DIRECTORY_DIR / file_name
        if not path.exists():
            raise SystemExit(f"Manifest references missing directory file: {path}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        entries.extend(payload.get("entries", []))
    expected = manifest.get("entryCount")
    if expected is not None and expected != len(entries):
        raise SystemExit(f"Directory entry count mismatch: manifest={expected}, loaded={len(entries)}")
    ids = [entry.get("id") for entry in entries]
    duplicates = [item for item, count in collections.Counter(ids).items() if count > 1]
    if duplicates:
        raise SystemExit(f"Duplicate directory ids: {duplicates}")
    return {"manifest": manifest, "entries": entries}


def iter_verses():
    if not EPUB.exists():
        raise SystemExit(f"Missing canonical EPUB: {EPUB}")
    with zipfile.ZipFile(EPUB) as zf:
        for member in zf.namelist():
            if not member.lower().endswith((".xhtml", ".html", ".htm")):
                continue
            try:
                raw = zf.read(member).decode("utf-8")
            except UnicodeDecodeError:
                continue
            current_chapter = ""
            for paragraph in extract_paragraphs(raw):
                if re.fullmatch(r"[1-3]?\s*[A-Za-z][A-Za-z '\-]+\s+\d+", paragraph):
                    current_chapter = paragraph
                    continue
                match = re.match(r"^(\d+)\.\s*(.*)$", paragraph, flags=re.S)
                if not match:
                    continue
                verse_no = int(match.group(1))
                text = match.group(2).strip()
                reference = f"{current_chapter}:{verse_no}" if current_chapter else f"{member}#{verse_no}"
                yield reference, text


def main() -> None:
    directory = load_directory()
    entries = directory["entries"]
    current_patterns = {
        entry["id"]: [(form, token_pattern(form)) for form in entry.get("currentForms", [])]
        for entry in entries
    }
    proposed_patterns = {
        entry["id"]: token_pattern(entry["proposedForm"])
        for entry in entries if entry.get("proposedForm")
    }
    result_by_id = {
        entry["id"]: {
            "id": entry["id"],
            "category": entry.get("category"),
            "proposalGroup": entry.get("proposalGroup"),
            "editorialStatus": entry.get("editorialStatus"),
            "currentForms": entry.get("currentForms", []),
            "proposedForm": entry.get("proposedForm"),
            "currentHitCount": 0,
            "proposedHitCount": 0,
            "currentHits": [],
            "proposedHits": [],
            "exampleReferences": entry.get("exampleReferences", []),
            "notes": entry.get("matchGuidance", {}).get("notes", ""),
        }
        for entry in entries
    }

    verse_count = 0
    for reference, text in iter_verses():
        verse_count += 1
        for entry in entries:
            row = result_by_id[entry["id"]]
            for form, pattern in current_patterns[entry["id"]]:
                matches = list(pattern.finditer(text))
                if matches:
                    row["currentHitCount"] += len(matches)
                    row["currentHits"].append({"reference": reference, "matchedForm": form, "text": text})
            proposed_pattern = proposed_patterns.get(entry["id"])
            if proposed_pattern is not None:
                matches = list(proposed_pattern.finditer(text))
                if matches:
                    row["proposedHitCount"] += len(matches)
                    row["proposedHits"].append({"reference": reference, "text": text})

    ordered = [result_by_id[entry["id"]] for entry in entries]
    machine = {
        "status": "diagnostic-only-no-scripture-changes",
        "inputEpub": str(EPUB.relative_to(ROOT)),
        "inputDirectory": str(DIRECTORY_DIR.relative_to(ROOT)),
        "verseRowsScanned": verse_count,
        "entries": ordered,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(machine, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Proposed original-name directory audit",
        "",
        "**Diagnostic only. This report does not authorize or perform Scripture replacement.**",
        "",
        f"- Canonical input: `{EPUB.relative_to(ROOT)}`",
        f"- Proposal directory: `{DIRECTORY_DIR.relative_to(ROOT)}`",
        f"- Verse rows scanned: **{verse_count:,}**",
        "",
        "## Summary",
        "",
        "| ID | Group | Current form(s) | Proposed form | Current hits | Proposed hits |",
        "|---|---|---|---|---:|---:|",
    ]
    for row in ordered:
        current = ", ".join(row["currentForms"])
        lines.append(f"| `{row['id']}` | {row['proposalGroup']} | {current} | {row['proposedForm']} | {row['currentHitCount']} | {row['proposedHitCount']} |")

    lines += ["", "## Candidate current-form hits", "", "Every hit below still requires identity/context review. A hit is not an approved replacement.", ""]
    for row in ordered:
        if not row["currentHits"]:
            continue
        lines += [f"### {row['id']} — {', '.join(row['currentForms'])} → {row['proposedForm']}", ""]
        if row["notes"]:
            lines += [f"Scope note: {row['notes']}", ""]
        for hit in row["currentHits"]:
            lines.append(f"- **{hit['reference']}** — `{hit['matchedForm']}` — {hit['text']}")
        lines.append("")

    lines += [
        "## Release rule",
        "",
        "Do not feed this report directly into a replacement script. First convert reviewed hits into an explicit before/after ledger with identity, reference, approved form, native-source evidence, collision decision, and reviewer status. Only that approved ledger may drive a later canonical release tool.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
