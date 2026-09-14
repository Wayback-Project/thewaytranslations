#!/usr/bin/env python3
from __future__ import annotations

import copy
import csv
import hashlib
import html
import json
import re
import zipfile
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / "current-form-documents" / "the-way-current.epub"
OUT_DIR = ROOT / "audit-output" / "masculine-inventory-2026-09-14"
EXPECTED_SHA = "bfd2e746afdb810d4b0b35abf66fe71da394abee77099f9c8f481102ab242f53"
BOOKS = {"psalms": "Psalms", "proverbs": "Proverbs", "song-of-solomon": "Song of Solomon"}
EXPECTED_CHAPTERS = {"psalms": 150, "proverbs": 31, "song-of-solomon": 8}

# Broad candidate extraction only. Editorial/source review decides what changes.
TRIGGERS = [
    r"\bman\b", r"\bmen\b", r"\bmankind\b",
    r"\bson\b", r"\bsons\b", r"\bfather\b", r"\bfathers\b",
    r"\bbrother\b", r"\bbrothers\b", r"\bhusband\b", r"\bhusbands\b",
    r"\bboy\b", r"\bboys\b", r"\bmale\b", r"\bmales\b",
    r"\bhe\b", r"\bhim\b", r"\bhis\b", r"\bhimself\b",
    r"\bking\b", r"\bkings\b", r"\bprince\b", r"\bprinces\b",
    r"\bmaster\b", r"\bmasters\b", r"\blord\b", r"\blords\b",
    r"\bbridegroom\b",
]
TRIGGER_RE = re.compile("|".join(f"(?P<t{i}>{p})" for i, p in enumerate(TRIGGERS)), re.I)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collapse(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def local_name(name: str) -> str:
    return name.split("}", 1)[-1] if "}" in name else name


def element_text(el: ET.Element) -> str:
    return collapse(" ".join(el.itertext()))


def strip_namespaces(root: ET.Element) -> ET.Element:
    root = copy.deepcopy(root)
    for el in root.iter():
        el.tag = local_name(el.tag)
        attrs = {local_name(k): v for k, v in el.attrib.items()}
        el.attrib.clear(); el.attrib.update(attrs)
    return root


def find_book_member(z: zipfile.ZipFile, slug: str) -> str:
    exact = f"OEBPS/Text/{slug}.xhtml"
    if exact in z.namelist():
        return exact
    matches = [n for n in z.namelist() if n.lower().endswith(f"/{slug}.xhtml")]
    if len(matches) != 1:
        raise RuntimeError(f"cannot locate {slug} XHTML: {matches}")
    return matches[0]


def chapter_number(el: ET.Element, slug: str):
    ident = el.attrib.get("id", "")
    m = re.fullmatch(rf"ch-{re.escape(slug)}-(\d+)", ident, re.I)
    return int(m.group(1)) if m else None


def extract_book(raw: bytes, slug: str, name: str):
    root = ET.fromstring(raw)
    parents = {child: parent for parent in root.iter() for child in parent}
    anchors = []
    for el in root.iter():
        n = chapter_number(el, slug)
        if n is not None:
            anchors.append((n, el))
    anchors.sort(key=lambda x: x[0])
    nums = [n for n, _ in anchors]
    if nums != list(range(1, EXPECTED_CHAPTERS[slug] + 1)):
        raise RuntimeError(f"chapter anchors invalid for {name}: {nums[:10]} ... count={len(nums)}")

    verses = []
    for number, el in anchors:
        frag = el
        if len(element_text(el)) < 80:
            parent = parents.get(el)
            if parent is None:
                raise RuntimeError(f"no wrapper for {name} {number}")
            siblings = list(parent); start = siblings.index(el); gathered = []
            for sibling in siblings[start:]:
                if sibling is not el and chapter_number(sibling, slug) is not None:
                    break
                gathered.append(copy.deepcopy(sibling))
            wrapper = ET.Element("section")
            for sibling in gathered:
                wrapper.append(sibling)
            frag = wrapper
        clean = strip_namespaces(frag)
        verse_counts = defaultdict(int)
        found = 0
        for node in clean.iter():
            if local_name(node.tag).lower() != "p":
                continue
            plain = element_text(node)
            m = re.match(r"^(\d+)\.\s*(.*)$", plain, re.S)
            if not m:
                continue
            verse = int(m.group(1)); verse_counts[verse] += 1; found += 1
            verses.append((slug, number, verse, collapse(m.group(2))))
        if not found:
            raise RuntimeError(f"no verses for {name} {number}")
    return verses


def main():
    actual_sha = sha256(EPUB)
    if actual_sha != EXPECTED_SHA:
        raise SystemExit(f"Canonical EPUB SHA mismatch: {actual_sha} != {EXPECTED_SHA}")

    verses = []
    with zipfile.ZipFile(EPUB) as zf:
        bad = zf.testzip()
        if bad:
            raise SystemExit(f"EPUB CRC failure: {bad}")
        for slug, name in BOOKS.items():
            member = find_book_member(zf, slug)
            verses.extend(extract_book(zf.read(member), slug, name))

    rows = []
    for slug, ch, vs, text in verses:
        found = []
        for m in TRIGGER_RE.finditer(text):
            token = m.group(0).lower()
            if token not in found:
                found.append(token)
        if found:
            rows.append({
                "slug": slug,
                "reference": f"{BOOKS[slug]} {ch}:{vs}",
                "triggers": ", ".join(found),
                "text": text,
            })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUT_DIR / "candidates.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["reference", "triggers", "text"], delimiter="\t")
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in ["reference", "triggers", "text"]})

    with (OUT_DIR / "all-verses.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["reference", "text"])
        for slug, ch, vs, text in verses:
            w.writerow([f"{BOOKS[slug]} {ch}:{vs}", text])

    by_book = {}
    for slug, name in BOOKS.items():
        total = sum(1 for v in verses if v[0] == slug)
        cand = sum(1 for r in rows if r["slug"] == slug)
        by_book[name] = {"chapters": EXPECTED_CHAPTERS[slug], "verses": total, "candidateVerses": cand}
    summary = {
        "canonicalEpubSha256": actual_sha,
        "scope": list(BOOKS.values()),
        "candidateRule": "Broad mechanical extraction only; every row requires contextual/source-language editorial classification.",
        "counts": by_book,
        "candidateVerseCount": len(rows),
        "extractedVerseCount": len(verses),
    }
    (OUT_DIR / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
