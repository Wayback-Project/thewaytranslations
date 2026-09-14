#!/usr/bin/env python3
import csv, hashlib, html, io, json, re, sys, zipfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / "current-form-documents" / "the-way-current.epub"
OUT_DIR = ROOT / "audit-output" / "masculine-inventory-2026-09-14"
EXPECTED_SHA = "bfd2e746afdb810d4b0b35abf66fe71da394abee77099f9c8f481102ab242f53"
BOOKS = {"psalms": "Psalms", "proverbs": "Proverbs", "song-of-solomon": "Song of Solomon"}

# This is intentionally a BROAD extraction pass. It does not decide what should change.
# Editorial classification happens after source/context review.
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
TRIGGER_RE = re.compile("|".join(f"(?P<t{i}>{p})" for i,p in enumerate(TRIGGERS)), re.I)
VERSE_RE = re.compile(
    r'<p\b[^>]*\bid=["\']v-(psalms|proverbs|song-of-solomon)-(\d+)-(\d+)["\'][^>]*>(.*?)</p>',
    re.I | re.S,
)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")

def clean_text(raw: str) -> str:
    raw = re.sub(r"<br\s*/?>", " ", raw, flags=re.I)
    raw = TAG_RE.sub("", raw)
    raw = html.unescape(raw)
    return WS_RE.sub(" ", raw).strip()

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    actual_sha = sha256(EPUB)
    if actual_sha != EXPECTED_SHA:
        raise SystemExit(f"Canonical EPUB SHA mismatch: {actual_sha} != {EXPECTED_SHA}")

    verses = {}
    member_hits = 0
    with zipfile.ZipFile(EPUB) as zf:
        bad = zf.testzip()
        if bad:
            raise SystemExit(f"EPUB CRC failure: {bad}")
        for name in zf.namelist():
            if not name.lower().endswith((".xhtml", ".html", ".htm")):
                continue
            try:
                text = zf.read(name).decode("utf-8")
            except UnicodeDecodeError:
                continue
            for slug, ch, vs, raw in VERSE_RE.findall(text):
                member_hits += 1
                key = (slug.lower(), int(ch), int(vs))
                value = clean_text(raw)
                if key in verses and verses[key] != value:
                    raise SystemExit(f"Conflicting duplicate verse {key}")
                verses[key] = value

    expected_chapters = {"psalms": 150, "proverbs": 31, "song-of-solomon": 8}
    observed_chapters = {slug: set() for slug in BOOKS}
    for slug, ch, vs in verses:
        observed_chapters[slug].add(ch)
    for slug, count in expected_chapters.items():
        if len(observed_chapters[slug]) != count:
            raise SystemExit(f"{slug}: expected {count} chapters, found {len(observed_chapters[slug])}")

    rows = []
    for (slug, ch, vs), text in sorted(verses.items(), key=lambda x: (list(BOOKS).index(x[0][0]), x[0][1], x[0][2])):
        found = []
        for m in TRIGGER_RE.finditer(text):
            token = m.group(0).lower()
            if token not in found:
                found.append(token)
        if found:
            rows.append({
                "book": BOOKS[slug], "slug": slug, "chapter": ch, "verse": vs,
                "reference": f"{BOOKS[slug]} {ch}:{vs}",
                "triggers": ", ".join(found), "text": text,
            })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUT_DIR / "candidates.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["reference","triggers","text"], delimiter="\t")
        w.writeheader()
        for r in rows:
            w.writerow({k:r[k] for k in ["reference","triggers","text"]})

    with (OUT_DIR / "all-verses.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["reference","text"])
        for (slug, ch, vs), text in sorted(verses.items(), key=lambda x: (list(BOOKS).index(x[0][0]), x[0][1], x[0][2])):
            w.writerow([f"{BOOKS[slug]} {ch}:{vs}", text])

    by_book = {}
    for slug, name in BOOKS.items():
        total = sum(1 for k in verses if k[0] == slug)
        cand = sum(1 for r in rows if r["slug"] == slug)
        by_book[name] = {"verses": total, "candidateVerses": cand, "chapters": len(observed_chapters[slug])}
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
