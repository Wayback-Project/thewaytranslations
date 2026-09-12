#!/usr/bin/env python3
"""Audit the current canonical EPUB for residual masculine divine pronouns.

This is a diagnostic only. It does not edit Scripture. The project policy replaces
masculine pronouns only where the referent is unmistakably divine; ambiguous,
poetic, Yeshua-referent, and human-referent cases remain outside a mechanical pass.
"""
from __future__ import annotations

import html
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / "current-form-documents" / "the-way-current.epub"
OUT_JSON = ROOT / "change-logs" / "reports" / "2026-09-12-divine-pronoun-residual-audit.json"
OUT_MD = ROOT / "editor-notes" / "consistency" / "2026-09-12-divine-pronoun-residual-audit.md"

BOOK_NAMES = {
    "genesis": "Genesis", "exodus": "Exodus", "leviticus": "Leviticus", "numbers": "Numbers",
    "deuteronomy": "Deuteronomy", "joshua": "Joshua", "judges": "Judges", "ruth": "Ruth",
    "1-samuel": "1 Samuel", "2-samuel": "2 Samuel", "1-kings": "1 Kings", "2-kings": "2 Kings",
    "1-chronicles": "1 Chronicles", "2-chronicles": "2 Chronicles", "ezra": "Ezra", "nehemiah": "Nehemiah",
    "esther": "Esther", "job": "Job", "psalms": "Psalms", "proverbs": "Proverbs",
    "ecclesiastes": "Ecclesiastes", "song-of-solomon": "Song of Solomon", "isaiah": "Isaiah",
    "jeremiah": "Jeremiah", "lamentations": "Lamentations", "ezekiel": "Ezekiel", "daniel": "Daniel",
    "hosea": "Hosea", "joel": "Joel", "amos": "Amos", "obadiah": "Obadiah", "jonah": "Jonah",
    "micah": "Micah", "nahum": "Nahum", "habakkuk": "Habakkuk", "zephaniah": "Zephaniah",
    "haggai": "Haggai", "zechariah": "Zechariah", "malachi": "Malachi", "matthew": "Matthew",
    "mark": "Mark", "luke": "Luke", "john": "John", "acts": "Acts", "romans": "Romans",
    "1-corinthians": "1 Corinthians", "2-corinthians": "2 Corinthians", "galatians": "Galatians",
    "ephesians": "Ephesians", "philippians": "Philippians", "colossians": "Colossians",
    "1-thessalonians": "1 Thessalonians", "2-thessalonians": "2 Thessalonians", "1-timothy": "1 Timothy",
    "2-timothy": "2 Timothy", "titus": "Titus", "philemon": "Philemon", "hebrews": "Hebrews",
    "james": "James", "1-peter": "1 Peter", "2-peter": "2 Peter", "1-john": "1 John",
    "2-john": "2 John", "3-john": "3 John", "jude": "Jude", "revelation": "Revelation",
}

# These are the explicitly documented unresolved cases from the 2026-09-10 release note.
DOCUMENTED_REVIEW = {
    "Exodus 34:28", "Numbers 24:8", "Psalms 110:5", "Psalms 110:6", "Psalms 110:7",
    "Ezekiel 2:2", "Acts 5:32", "Acts 13:35", "Acts 20:28", "Romans 15:10", "Hebrews 1:3",
}

DIVINE = r"(?:YHWH|Elohim|God|Cosmic Parent|El Shaddai|Elyon)"
PRONOUN = r"(?:he|him|his|himself)"
PRONOUN_RE = re.compile(rf"\b{PRONOUN}\b", re.I)
DIVINE_RE = re.compile(rf"\b{DIVINE}\b")
AFTER_RE = re.compile(rf"\b(?P<divine>{DIVINE})\b(?P<between>[^.!?]{{0,120}}?)\b(?P<pronoun>{PRONOUN})\b", re.I)
BEFORE_RE = re.compile(rf"\b(?P<pronoun>{PRONOUN})\b(?P<between>[^.!?]{{0,80}}?)\b(?P<divine>{DIVINE})\b", re.I)


def visible(fragment: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).replace("\u00a0", " ").strip()


def audit() -> dict:
    candidates = []
    all_divine_pronoun_verses = []
    with zipfile.ZipFile(EPUB, "r") as z:
        for member in z.namelist():
            m = re.fullmatch(r"OEBPS/Text/(.+)\.xhtml", member)
            if not m:
                continue
            slug = m.group(1)
            book = BOOK_NAMES.get(slug, slug)
            raw = z.read(member).decode("utf-8")
            chapter = None
            token_re = re.compile(r"<p\b(?P<attrs>[^>]*)>(?P<inner>.*?)</p>", re.I | re.S)
            for pm in token_re.finditer(raw):
                attrs = pm.group("attrs")
                inner = pm.group("inner")
                ch = re.search(rf"\bid=[\"']ch-{re.escape(slug)}-(\d+)[\"']", attrs, re.I)
                if ch:
                    chapter = int(ch.group(1))
                    continue
                text = visible(inner)
                vm = re.match(r"^(\d+)\.\s*(.*)$", text, re.S)
                if not vm or chapter is None:
                    continue
                verse = int(vm.group(1))
                verse_text = vm.group(2).strip()
                if not PRONOUN_RE.search(verse_text) or not DIVINE_RE.search(verse_text):
                    continue
                ref = f"{book} {chapter}:{verse}"
                record = {"reference": ref, "text": verse_text, "documentedReview": ref in DOCUMENTED_REVIEW}
                all_divine_pronoun_verses.append(record)

                hits = []
                for match in AFTER_RE.finditer(verse_text):
                    hits.append({
                        "direction": "divine-before-pronoun",
                        "divine": match.group("divine"),
                        "pronoun": match.group("pronoun"),
                        "between": match.group("between"),
                    })
                for match in BEFORE_RE.finditer(verse_text):
                    hits.append({
                        "direction": "pronoun-before-divine",
                        "divine": match.group("divine"),
                        "pronoun": match.group("pronoun"),
                        "between": match.group("between"),
                    })
                if hits:
                    candidates.append({**record, "hits": hits})

    undocumented = [item for item in candidates if not item["documentedReview"]]
    return {
        "canonicalEpub": str(EPUB.relative_to(ROOT)),
        "policy": "Do not use masculine pronouns for an unmistakably divine referent; repeat the established divine name/title instead. Do not mechanically change human, Yeshua, ambiguous, or poetic referents.",
        "divineMarkers": ["YHWH", "Elohim", "God", "Cosmic Parent", "El Shaddai", "Elyon"],
        "pronouns": ["he", "him", "his", "himself"],
        "sameVerseDivineAndPronounCount": len(all_divine_pronoun_verses),
        "proximityCandidateCount": len(candidates),
        "undocumentedProximityCandidateCount": len(undocumented),
        "documentedReviewReferences": sorted(DOCUMENTED_REVIEW),
        "proximityCandidates": candidates,
        "allSameVerseCandidates": all_divine_pronoun_verses,
    }


def main() -> None:
    data = audit()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    undocumented = [item for item in data["proximityCandidates"] if not item["documentedReview"]]
    lines = [
        "# Divine-pronoun residual audit — 2026-09-12",
        "",
        "This is a **diagnostic audit only**. It does not change Scripture.",
        "",
        "Policy under audit: when the referent is unmistakably divine, The Way Version avoids masculine `he / him / his / himself` and repeats the established divine name/title instead. Human referents, Yeshua references, uncertain speaker transitions, and poetic/textually disputed referents are not mechanically rewritten.",
        "",
        f"- Same-verse divine-marker + masculine-pronoun verses: **{data['sameVerseDivineAndPronounCount']}**",
        f"- Close-proximity candidates: **{data['proximityCandidateCount']}**",
        f"- Close-proximity candidates outside the documented review list: **{data['undocumentedProximityCandidateCount']}**",
        "",
        "## Undocumented close-proximity candidates",
        "",
    ]
    if undocumented:
        for item in undocumented:
            lines.append(f"- **{item['reference']}** — {item['text']}")
    else:
        lines.append("None.")
    lines += [
        "",
        "## Documented review references preserved from the prior release",
        "",
    ]
    for ref in sorted(DOCUMENTED_REVIEW):
        lines.append(f"- {ref}")
    lines += [
        "",
        "The full machine-readable candidate inventory is in `change-logs/reports/2026-09-12-divine-pronoun-residual-audit.json`.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({
        "sameVerse": data["sameVerseDivineAndPronounCount"],
        "proximity": data["proximityCandidateCount"],
        "undocumentedProximity": data["undocumentedProximityCandidateCount"],
    }, indent=2))


if __name__ == "__main__":
    main()
