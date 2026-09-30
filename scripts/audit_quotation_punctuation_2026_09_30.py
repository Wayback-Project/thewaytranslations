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

ROOT = Path(__file__).resolve().parents[1]
CANON_CONTENT = ROOT / "current-form-documents/mobile-reader/content.json"
EPUB = ROOT / "current-form-documents/the-way-current.epub"
OUT_MD = ROOT / "change-logs/reports/2026-09-30-quotation-punctuation-audit.md"
OUT_TSV = ROOT / "change-logs/reports/2026-09-30-quotation-punctuation-candidates.tsv"

QUOTE_CHARS = set('"\'“”‘’')
DETERMINISTIC_CATEGORIES = [
    "CONFIRMED_SPACED_NESTED_CLOSERS",
    "CONFIRMED_SPACE_BEFORE_CLOSING_QUOTE",
    "CONFIRMED_SPACE_AFTER_OPENING_QUOTE",
    "CONFIRMED_SPACE_BEFORE_PUNCTUATION",
    "CONFIRMED_REPLACEMENT_CHARACTER",
    "CONFIRMED_REPEATED_SPACES",
]
REVIEW_CATEGORIES = [
    "REVIEW_3PLUS_QUOTES_WITHIN_10_CHARS",
    "REVIEW_REPEATED_PUNCTUATION",
]


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
    """Merged spans containing 3+ quote-like glyphs inside a 10-character window."""
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
    for m in re.finditer(r"\S\s+[”’]", text):
        findings.append(("CONFIRMED_SPACE_BEFORE_CLOSING_QUOTE", m.start(), m.end()))
    for m in re.finditer(r"[“‘]\s+\S", text):
        findings.append(("CONFIRMED_SPACE_AFTER_OPENING_QUOTE", m.start(), m.end()))
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
    return findings


def snippet(text: str, start: int, end: int, radius: int = 65):
    a = max(0, start - radius)
    b = min(len(text), end + radius)
    return ("…" if a else "") + text[a:b] + ("…" if b < len(text) else "")


def source_spaced_closer_occurrences():
    rows = []
    pattern = re.compile(r"[”’]\s+[”’]")
    for path in sorted((ROOT / "original-documents").glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        for line_no, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                rows.append((str(path.relative_to(ROOT)), line_no, line.strip()))
    return rows


def epub_raw_audit(path: Path):
    xhtml_members = 0
    spaced_nested = 0
    space_before_close = 0
    space_after_open = 0
    trigger = False
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            if not name.lower().endswith((".xhtml", ".html", ".htm")):
                continue
            xhtml_members += 1
            text = zf.read(name).decode("utf-8", errors="replace")
            spaced_nested += len(re.findall(r"[”’]\s+[”’]", text))
            space_before_close += len(re.findall(r"\S\s+[”’]", text))
            space_after_open += len(re.findall(r"[“‘]\s+\S", text))
            trigger = trigger or ('.” ’ ”' in text)
    return {
        "xhtml_members": xhtml_members,
        "spaced_nested": spaced_nested,
        "space_before_close": space_before_close,
        "space_after_open": space_after_open,
        "trigger": trigger,
    }


def ordered_refs(candidates, category):
    seen = set()
    out = []
    for item in candidates:
        if item["category"] != category or item["reference"] in seen:
            continue
        seen.add(item["reference"])
        out.append(item["reference"])
    return out


def main():
    canon_data, canon_rows = load_search(CANON_CONTENT)
    if len(canon_rows) != 31102:
        raise SystemExit(f"Expected 31,102 canonical search rows, found {len(canon_rows)}")

    candidates = []
    by_category = Counter()
    refs_by_category = defaultdict(set)
    style = Counter()

    for row in canon_rows:
        text = row.get("text", "")
        # Style inventory only — presence is not classified as an error.
        if '"' in text:
            style["verses_with_straight_double_quote"] += 1
        if re.search(r"(?<![A-Za-z0-9])'(?![A-Za-z0-9])", text):
            style["verses_with_isolated_straight_single_quote"] += 1
        if "“" in text or "”" in text:
            style["verses_with_curly_double_quote"] += 1
        if "‘" in text or "’" in text:
            style["verses_with_curly_single_quote_or_apostrophe"] += 1
        if ('"' in text) and ("“" in text or "”" in text):
            style["verses_mixing_straight_and_curly_double_quotes"] += 1

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

    source_hits = source_spaced_closer_occurrences()
    epub = epub_raw_audit(EPUB)

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
        f"- Canonical EPUB contains the exact spaced trigger: **{epub['trigger']}**",
        "",
        "## Canonical-layer checks",
        "",
        f"- Canonical mobile fallback inventory scanned: **{len(canon_rows):,}** verse-search records",
        f"- EPUB XHTML/HTML members scanned as raw UTF-8: **{epub['xhtml_members']}**",
        f"- EPUB spaced nested-closer sequences: **{epub['spaced_nested']}**",
        f"- EPUB spaces immediately before curly closing quotes: **{epub['space_before_close']}**",
        f"- EPUB spaces immediately after curly opening quotes: **{epub['space_after_open']}**",
        f"- Canonical editable-source lines containing spaced curly closing-quote pairs: **{len(source_hits)}**",
        "",
        "## Whole-Bible candidate scan",
        "",
        "The scan deliberately separates deterministic formatting defects from review-only heuristics. Quote counts by themselves are not treated as errors because dialogue can span verses.",
        "",
    ]
    for category in DETERMINISTIC_CATEGORIES + REVIEW_CATEGORIES:
        lines.append(f"- `{category}`: **{by_category[category]} hit(s)** across **{len(refs_by_category[category])} verse(s)**")

    lines.extend(["", "### Confirmed spaced nested-closer references", ""])
    confirmed_refs = ordered_refs(candidates, "CONFIRMED_SPACED_NESTED_CLOSERS")
    lines.append(", ".join(confirmed_refs) if confirmed_refs else "None.")

    lines.extend(["", "### 3+ quote marks within 10 characters — review queue", ""])
    proximity_refs = ordered_refs(candidates, "REVIEW_3PLUS_QUOTES_WITHIN_10_CHARS")
    lines.append(", ".join(proximity_refs) if proximity_refs else "None.")

    lines.extend(["", "### Quote-style inventory (not presumed errors)", ""])
    for label in [
        "verses_with_straight_double_quote",
        "verses_with_isolated_straight_single_quote",
        "verses_with_curly_double_quote",
        "verses_with_curly_single_quote_or_apostrophe",
        "verses_mixing_straight_and_curly_double_quotes",
    ]:
        lines.append(f"- `{label}`: **{style[label]} verse(s)**")

    lines.extend(["", "### Editable-source spaced-closer hits", ""])
    for path, line_no, line in source_hits:
        clean = line.replace("`", "\\`")
        lines.append(f"- `{path}:{line_no}` — `{clean}`")

    lines.extend([
        "",
        "## Review policy and proposed next step",
        "",
        "1. Treat `CONFIRMED_*` categories as mechanical typography/encoding defects only after each reference is context-checked.",
        "2. Treat `REVIEW_*` categories as candidate queues, not release authority; nested dialogue, rhetorical punctuation, and multi-verse quotation spans can be legitimate.",
        "3. Treat the quote-style inventory as a possible future house-style project, not as permission for a mass replacement.",
        "4. For any approved fixes, freeze exact Current → Final verse strings in the Google final-review ledger before release.",
        "5. Apply only the approved finite set to the canonical EPUB/source, then rebuild canonical mobile fallback, Netlify reader/search/mobile feed, and mobile content provenance from the new canonical artifact.",
        "6. Re-run this audit after the correction release and require zero unintended verse-text differences downstream.",
        "",
        "## Audit provenance",
        "",
        f"- Canonical release ID: `{canon_data.get('releaseId', '')}`",
        f"- Canonical EPUB SHA-256 in package: `{canon_data.get('canonicalEpubSha256', '')}`",
        "- Web-reader layer parity for the trigger verse is verified separately against the generated Netlify data and recorded in the Google final-review ledger.",
        "",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote {OUT_MD.relative_to(ROOT)}")
    print(f"wrote {OUT_TSV.relative_to(ROOT)}")
    print(f"candidates={len(candidates)} categories={dict(by_category)}")
    print(f"style={dict(style)}")
    print(f"source_spaced_closer_hits={len(source_hits)}")
    print(f"epub={epub}")


if __name__ == "__main__":
    main()
