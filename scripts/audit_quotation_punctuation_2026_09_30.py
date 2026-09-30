#!/usr/bin/env python3
"""Whole-Bible quotation/punctuation integrity audit for the 2026-09-30 review.

Read-only with respect to Scripture. Produces review reports only.
"""
from __future__ import annotations

import csv
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CANON_CONTENT = ROOT / "current-form-documents/mobile-reader/content.json"
EPUB = ROOT / "current-form-documents/the-way-current.epub"
OUT_MD = ROOT / "change-logs/reports/2026-09-30-quotation-punctuation-audit.md"
OUT_TSV = ROOT / "change-logs/reports/2026-09-30-quotation-punctuation-candidates.tsv"

QUOTE_CHARS = set('"\'“”‘’')


def load_search(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("search")
    if not isinstance(rows, list):
        raise SystemExit(f"Missing search array in {path}")
    return data, rows


def key(row):
    return (row.get("book"), int(row.get("chapter", 0)), int(row.get("verse", 0)))


def ref(row):
    return f"{row.get('book')} {row.get('chapter')}:{row.get('verse')}"


def quote_proximity(text: str):
    """Return merged spans containing 3+ quote-like glyphs inside 10 characters."""
    positions = [(i, ch) for i, ch in enumerate(text) if ch in QUOTE_CHARS]
    hits = []
    for n in range(len(positions)):
        i0 = positions[n][0]
        j = n
        while j + 1 < len(positions) and positions[j + 1][0] - i0 <= 10:
            j += 1
        if j - n + 1 >= 3:
            hits.append((i0, positions[j][0] + 1))
    merged = []
    for start, end in hits:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def suspicious(text: str):
    findings = []
    # Deterministic typography / encoding candidates.
    for m in re.finditer(r"([”’])\s+([”’])", text):
        findings.append(("CONFIRMED_SPACED_NESTED_CLOSERS", m.start(), m.end()))
    for m in re.finditer(r"\s+[,:;!?]", text):
        findings.append(("CONFIRMED_SPACE_BEFORE_PUNCTUATION", m.start(), m.end()))
    for m in re.finditer(r"\uFFFD", text):
        findings.append(("CONFIRMED_REPLACEMENT_CHARACTER", m.start(), m.end()))
    for m in re.finditer(r" {2,}", text):
        findings.append(("CONFIRMED_REPEATED_SPACES", m.start(), m.end()))

    # Review-only heuristics. These can be legitimate in dialogue or rhetoric.
    for start, end in quote_proximity(text):
        findings.append(("REVIEW_3PLUS_QUOTES_WITHIN_10_CHARS", start, end))
    for m in re.finditer(r"(?<!\.)\.\.(?!\.)|,,|;;|::|!!|\?\?", text):
        findings.append(("REVIEW_REPEATED_PUNCTUATION", m.start(), m.end()))
    for m in re.finditer(r'"', text):
        findings.append(("REVIEW_STRAIGHT_DOUBLE_QUOTE", m.start(), m.end()))
    for m in re.finditer(r"(?<![A-Za-z0-9])'(?![A-Za-z0-9])", text):
        findings.append(("REVIEW_STRAIGHT_SINGLE_QUOTE", m.start(), m.end()))
    return findings


def snippet(text: str, start: int, end: int, radius: int = 65):
    a = max(0, start - radius)
    b = min(len(text), end + radius)
    return ("…" if a else "") + text[a:b] + ("…" if b < len(text) else "")


def epub_verse_texts(path: Path):
    verses = {}
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            if not name.lower().endswith((".xhtml", ".html", ".htm")):
                continue
            raw = zf.read(name)
            try:
                root = ET.fromstring(raw)
            except ET.ParseError:
                continue
            for elem in root.iter():
                ident = elem.attrib.get("id", "")
                if not ident.startswith("v-"):
                    continue
                verses[ident] = "".join(elem.itertext()).strip()
    return verses


def source_occurrences():
    rows = []
    pattern = re.compile(r"[”’]\s+[”’]")
    for path in sorted((ROOT / "original-documents").glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                rows.append((str(path.relative_to(ROOT)), line_no, line.strip()))
    return rows


def main():
    canon_data, canon_rows = load_search(CANON_CONTENT)
    if len(canon_rows) != 31102:
        raise SystemExit(f"Expected 31,102 canonical search rows, found {len(canon_rows)}")

    epub_map = epub_verse_texts(EPUB)

    candidates = []
    by_category = Counter()
    refs_by_category = defaultdict(set)
    for row in canon_rows:
        text = row.get("text", "")
        for category, start, end in suspicious(text):
            by_category[category] += 1
            refs_by_category[category].add(ref(row))
            candidates.append({
                "reference": ref(row),
                "category": category,
                "start": start,
                "end": end,
                "snippet": snippet(text, start, end),
                "full_text": text,
            })

    genesis = next((r for r in canon_rows if key(r) == ("Genesis", 20, 13)), None)
    if not genesis:
        raise SystemExit("Genesis 20:13 missing from canonical content")
    genesis_text = genesis["text"]
    expected_current_tail = 'say of me, “He is my brother.” ’ ”'
    if expected_current_tail not in genesis_text:
        raise SystemExit(f"Genesis 20:13 no longer has expected audit trigger: {genesis_text}")
    proposed_genesis = genesis_text.replace('.” ’ ”', '.”’”')

    source_hits = source_occurrences()

    with zipfile.ZipFile(EPUB) as zf:
        epub_joined = b"\n".join(zf.read(n) for n in zf.namelist() if n.lower().endswith(".xhtml"))
    epub_has_trigger = '.” ’ ”'.encode("utf-8") in epub_joined

    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_TSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["reference", "category", "start", "end", "snippet", "full_text"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(candidates)

    lines = [
        "# 2026-09-30 quotation / punctuation integrity audit",
        "",
        "**Status: PROPOSAL / REVIEW ONLY — no Scripture wording or punctuation changed by this audit.**",
        "",
        "## Trigger diagnosis — Genesis 20:13",
        "",
        "The screenshot-visible ending is not three accidental quote marks. All three closing marks are structurally required by nested quotation levels: the inner double quotation closes Sarah's reported words; the single quotation closes Abraham's quotation to Sarah; and the final double quotation closes Abraham's longer speech. The defect is the inserted spaces between the nested closing marks.",
        "",
        f"- Current canonical verse: `{genesis_text}`",
        f"- Proposed typography-only normalization: `{proposed_genesis}`",
        "- Proposed change: remove the two inter-quote spaces only (`.” ’ ”` → `.”’”`). No wording and no quotation level is removed.",
        f"- Canonical EPUB contains the exact spaced trigger: **{epub_has_trigger}**",
        "",
        "## Canonical-layer checks",
        "",
        f"- Canonical mobile fallback inventory scanned: **{len(canon_rows):,}** verse-search records",
        f"- EPUB verse elements parsed: **{len(epub_map):,}**",
        f"- Canonical editable-source lines containing spaced curly closing-quote pairs: **{len(source_hits)}**",
        "",
        "## Whole-Bible candidate scan",
        "",
        "The scan deliberately separates deterministic formatting defects from review-only heuristics. Quote counts by themselves are not treated as errors because dialogue can span verses.",
        "",
    ]
    for category in sorted(by_category):
        lines.append(f"- `{category}`: **{by_category[category]} hit(s)** across **{len(refs_by_category[category])} verse(s)**")
    lines.extend(["", "### Editable-source spaced-closer hits", ""])
    for path, line_no, line in source_hits[:50]:
        clean = line.replace("`", "\\`")
        lines.append(f"- `{path}:{line_no}` — `{clean}`")
    if len(source_hits) > 50:
        lines.append(f"- … {len(source_hits)-50} additional source-line hit(s); see the machine candidate report.")
    lines.extend([
        "",
        "## Review policy and proposed next step",
        "",
        "1. Treat `CONFIRMED_*` categories as mechanical typography/encoding defects only after each reference is context-checked.",
        "2. Treat `REVIEW_*` categories as candidate queues, not release authority; nested dialogue, rhetorical punctuation, and multi-verse quotation spans can be legitimate.",
        "3. For any approved fixes, freeze exact Current → Final verse strings in the Google final-review ledger before release.",
        "4. Apply only the approved finite set to the canonical EPUB/source, then rebuild canonical mobile fallback, Netlify reader/search/mobile feed, and mobile content provenance from the new canonical artifact.",
        "5. Re-run this audit after the correction release and require zero unintended verse-text differences downstream.",
        "",
        "## Audit provenance",
        "",
        f"- Canonical release ID: `{canon_data.get('releaseId', '')}`",
        f"- Canonical EPUB SHA-256 in package: `{canon_data.get('canonicalEpubSha256', '')}`",
        "- Web-reader layer parity for the trigger verse is verified separately against the deployed/generated Netlify data and recorded in the Google final-review ledger.",
        "",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote {OUT_MD.relative_to(ROOT)}")
    print(f"wrote {OUT_TSV.relative_to(ROOT)}")
    print(f"candidates={len(candidates)} categories={dict(by_category)}")
    print(f"source_spaced_closer_hits={len(source_hits)}")
    print(f"epub_has_genesis_trigger={epub_has_trigger}")


if __name__ == "__main__":
    main()
