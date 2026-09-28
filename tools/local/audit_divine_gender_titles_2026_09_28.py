#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import release_2026_09_14_ecclesiastes_inclusive_language_isaiah_harm as prior

ROOT = prior.ROOT
EPUB = prior.EPUB
collect_verses = prior.prev.collect_verses
CANONICAL_SHA = "6a3a0dbc91949b082fdcf7c93d0832fe6762440933d8528009cf44b2271dfb92"

BOOKS = [
("genesis","Genesis","OT"),("exodus","Exodus","OT"),("leviticus","Leviticus","OT"),("numbers","Numbers","OT"),("deuteronomy","Deuteronomy","OT"),
("joshua","Joshua","OT"),("judges","Judges","OT"),("ruth","Ruth","OT"),("1-samuel","1 Samuel","OT"),("2-samuel","2 Samuel","OT"),("1-kings","1 Kings","OT"),("2-kings","2 Kings","OT"),
("1-chronicles","1 Chronicles","OT"),("2-chronicles","2 Chronicles","OT"),("ezra","Ezra","OT"),("nehemiah","Nehemiah","OT"),("esther","Esther","OT"),("job","Job","OT"),
("psalms","Psalms","OT"),("proverbs","Proverbs","OT"),("ecclesiastes","Ecclesiastes","OT"),("song-of-solomon","Song of Solomon","OT"),("isaiah","Isaiah","OT"),
("jeremiah","Jeremiah","OT"),("lamentations","Lamentations","OT"),("ezekiel","Ezekiel","OT"),("daniel","Daniel","OT"),("hosea","Hosea","OT"),("joel","Joel","OT"),("amos","Amos","OT"),
("obadiah","Obadiah","OT"),("jonah","Jonah","OT"),("micah","Micah","OT"),("nahum","Nahum","OT"),("habakkuk","Habakkuk","OT"),("zephaniah","Zephaniah","OT"),("haggai","Haggai","OT"),
("zechariah","Zechariah","OT"),("malachi","Malachi","OT"),
("matthew","Matthew","NT"),("mark","Mark","NT"),("luke","Luke","NT"),("john","John","NT"),("acts","Acts","NT"),("romans","Romans","NT"),
("1-corinthians","1 Corinthians","NT"),("2-corinthians","2 Corinthians","NT"),("galatians","Galatians","NT"),("ephesians","Ephesians","NT"),("philippians","Philippians","NT"),
("colossians","Colossians","NT"),("1-thessalonians","1 Thessalonians","NT"),("2-thessalonians","2 Thessalonians","NT"),("1-timothy","1 Timothy","NT"),("2-timothy","2 Timothy","NT"),
("titus","Titus","NT"),("philemon","Philemon","NT"),("hebrews","Hebrews","NT"),("james","James","NT"),("1-peter","1 Peter","NT"),("2-peter","2 Peter","NT"),
("1-john","1 John","NT"),("2-john","2 John","NT"),("3-john","3 John","NT"),("jude","Jude","NT"),("revelation","Revelation","NT")
]
SLUG_TO_META = {slug:(book,testament) for slug,book,testament in BOOKS}
BOOK_TO_SLUG = {book:slug for slug,book,_ in BOOKS}

TITLE_PATTERNS = {
    "king": re.compile(r"\bking\b", re.I),
    "kings": re.compile(r"\bkings\b", re.I),
    "kingdom": re.compile(r"\bkingdom\b", re.I),
    "kingdoms": re.compile(r"\bkingdoms\b", re.I),
    "kingship": re.compile(r"\bkingship\b", re.I),
    "lord": re.compile(r"\blord\b", re.I),
    "lords": re.compile(r"\blords\b", re.I),
    "master": re.compile(r"\bmaster\b", re.I),
    "masters": re.compile(r"\bmasters\b", re.I),
    "father_cap": re.compile(r"\bFather\b"),
    "sovereign": re.compile(r"\bsovereign\b", re.I),
    "reign": re.compile(r"\breign(?:s|ed|ing)?\b", re.I),
    "realm": re.compile(r"\brealm(?:s)?\b", re.I),
    "domain": re.compile(r"\bdomain(?:s)?\b", re.I),
    "adonai": re.compile(r"\bAdonai\b"),
    "abba": re.compile(r"\bAbba\b"),
    "cosmic_parent": re.compile(r"\bCosmic Parent\b"),
}

DIVINE_MARKERS = re.compile(r"\b(?:YHWH|Elohim|God|Adonai|Cosmic Parent|Most High|Ruach|Messiah|Yeshua)\b")
GOD_ONLY_MARKERS = re.compile(r"\b(?:YHWH|Elohim|God|Adonai|Cosmic Parent|Most High)\b")
MASC_PRONOUN = re.compile(r"\b(?:he|him|his|himself)\b", re.I)
TRIAGE_LINE = re.compile(r"^- \*\*(?P<reference>.+?\d+:\d+)\*\* — \[(?P<tag>[^\]]+)\] — (?P<text>.*)$")
ARROW = re.compile(r"(?P<from>He|he|Him|him|His|his|Himself|himself)→(?P<to>[^,\]]+)")

INVENTORY_OUT = ROOT / "tools/local/generated_divine_gender_title_inventory_2026_09_28.tsv"
TRIAGE_OUT = ROOT / "tools/local/generated_divine_pronoun_residual_inventory_2026_09_28.tsv"
REPORT_OUT = ROOT / "change-logs/reports/2026-09-28-divine-gender-title-inventory.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_ref(ref: str):
    m = re.match(r"^(.*) (\d+):(\d+)$", ref)
    if not m:
        raise ValueError(ref)
    return m.group(1), int(m.group(2)), int(m.group(3))


def load_triage():
    triage_dir = ROOT / "editor-notes/consistency/divine-pronoun-triage-2026-09-12"
    rows = []
    for path in sorted(triage_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            m = TRIAGE_LINE.match(raw)
            if not m:
                continue
            ref = m.group("reference")
            tags = m.group("tag")
            prior_text = m.group("text")
            arrows = [{"from": a.group("from"), "to": a.group("to").strip()} for a in ARROW.finditer(tags)]
            rows.append({
                "reference": ref,
                "triage_tags": tags,
                "triage_text_2026_09_12": prior_text,
                "arrow_hints": arrows,
                "triage_file": str(path.relative_to(ROOT)),
            })
    return rows


def main():
    actual = sha256(EPUB)
    if actual != CANONICAL_SHA:
        raise SystemExit(f"canonical EPUB SHA mismatch expected={CANONICAL_SHA} got={actual}")

    verses = collect_verses(EPUB, slugs=tuple(slug for slug,_,_ in BOOKS))
    if len(verses) != 31102:
        raise RuntimeError(f"whole-Bible verse inventory mismatch: {len(verses)} != 31102")

    title_rows = []
    for (slug,ch,vs), text in verses.items():
        matches = [name for name,pat in TITLE_PATTERNS.items() if pat.search(text)]
        if not matches:
            continue
        book,testament = SLUG_TO_META[slug]
        title_rows.append({
            "reference": f"{book} {ch}:{vs}",
            "testament": testament,
            "book": book,
            "chapter": ch,
            "verse": vs,
            "matched_categories": ",".join(matches),
            "has_divine_marker": "yes" if DIVINE_MARKERS.search(text) else "no",
            "has_god_only_marker": "yes" if GOD_ONLY_MARKERS.search(text) else "no",
            "has_masculine_pronoun": "yes" if MASC_PRONOUN.search(text) else "no",
            "current_text": text,
            "previous_verse": verses.get((slug,ch,vs-1),""),
            "next_verse": verses.get((slug,ch,vs+1),""),
        })

    INVENTORY_OUT.parent.mkdir(parents=True, exist_ok=True)
    title_fields = ["reference","testament","book","chapter","verse","matched_categories","has_divine_marker","has_god_only_marker","has_masculine_pronoun","current_text","previous_verse","next_verse"]
    with INVENTORY_OUT.open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f,fieldnames=title_fields,delimiter="\t",lineterminator="\n")
        w.writeheader(); w.writerows(title_rows)

    triage_rows = []
    triage_missing_refs = []
    for row in load_triage():
        try:
            book,ch,vs = parse_ref(row["reference"])
            slug = BOOK_TO_SLUG[book]
        except Exception:
            triage_missing_refs.append(row["reference"])
            continue
        current = verses.get((slug,ch,vs))
        if current is None:
            triage_missing_refs.append(row["reference"])
            continue
        pronouns = sorted({m.group(0) for m in MASC_PRONOUN.finditer(current)}, key=str.lower)
        arrow_hints = "; ".join(f"{a['from']}→{a['to']}" for a in row["arrow_hints"])
        triage_rows.append({
            "reference": row["reference"],
            "testament": SLUG_TO_META[slug][1],
            "book": book,
            "chapter": ch,
            "verse": vs,
            "triage_tags": row["triage_tags"],
            "arrow_hints": arrow_hints,
            "still_has_masculine_pronoun": "yes" if pronouns else "no",
            "current_masculine_pronouns": ",".join(pronouns),
            "current_text": current,
            "triage_text_2026_09_12": row["triage_text_2026_09_12"],
            "triage_file": row["triage_file"],
        })

    TRIAGE_OUT.parent.mkdir(parents=True, exist_ok=True)
    triage_fields = ["reference","testament","book","chapter","verse","triage_tags","arrow_hints","still_has_masculine_pronoun","current_masculine_pronouns","current_text","triage_text_2026_09_12","triage_file"]
    with TRIAGE_OUT.open("w", encoding="utf-8", newline="") as f:
        w=csv.DictWriter(f,fieldnames=triage_fields,delimiter="\t",lineterminator="\n")
        w.writeheader(); w.writerows(triage_rows)

    title_counts = Counter()
    for r in title_rows:
        title_counts.update(r["matched_categories"].split(","))
    title_books = Counter(r["book"] for r in title_rows)
    triage_books = Counter(r["book"] for r in triage_rows)
    residual = [r for r in triage_rows if r["still_has_masculine_pronoun"]=="yes"]

    report = {
        "status":"inventory-only; proposal input; no Scripture changes",
        "canonicalCommit":"ada4a755463f6de6744e5e77070aa78fcc752a33",
        "canonicalEpubSha256":actual,
        "wholeBibleVerseCount":len(verses),
        "titleMetaphorInventoryVerseCount":len(title_rows),
        "titleMetaphorMatchCounts":dict(sorted(title_counts.items())),
        "titleMetaphorVerseCountsByBook":dict(sorted(title_books.items())),
        "priorDivinePronounTriageRows":len(triage_rows),
        "priorDivinePronounTriageRowsStillContainingMasculinePronoun":len(residual),
        "divinePronounTriageCountsByBook":dict(sorted(triage_books.items())),
        "triageReferenceErrors":triage_missing_refs,
        "outputs":[str(INVENTORY_OUT.relative_to(ROOT)),str(TRIAGE_OUT.relative_to(ROOT))],
        "method":[
            "Exact 31,102-verse extraction from the canonical EPUB.",
            "Broad title/metaphor inventory for king/kingdom/lord/master/Father plus existing neutral forms Sovereign/reign/realm/domain/Adonai/Abba/Cosmic Parent.",
            "Reconciliation of the 2026-09-12 review-only divine-pronoun triage against the current canonical EPUB, retaining current verse text and marking rows that still contain he/him/his/himself.",
            "This inventory intentionally does not decide whether a title/pronoun refers to God, Yeshua, or a human. Proposal classification must remain context-first."
        ]
    }
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
