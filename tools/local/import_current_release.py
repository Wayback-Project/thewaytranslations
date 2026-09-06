#!/usr/bin/env python3
"""Import the verified public Way EPUB and synchronize repository source artifacts."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[2]
CURRENT = ROOT / "current-form-documents" / "the-way-current.epub"
HISTORY = ROOT / "rendered-documents-history"
LOG = HISTORY / "LOG.md"
EPUB_URL = "https://thewayversion.com/media/The%20Way%20Version.epub"
SEARCH_URL = "https://thewayversion.com/app/data/search.json"
EXPECTED_SHA256 = "dbd8cace51a0e726a2d910622af995d490ee4f24f76eb7efcd0e5a1756c1119e"

SOURCE_GROUPS = {
    "original-documents/genesis_restorative_translation.txt": ["genesis"],
    "original-documents/exodus_to_ecclesiastes_restorative_translation.txt": [
        "exodus", "leviticus", "numbers", "deuteronomy", "joshua", "judges", "ruth",
        "1-samuel", "2-samuel", "1-kings", "2-kings", "1-chronicles", "2-chronicles",
        "ezra", "nehemiah", "esther", "job", "psalms", "proverbs", "ecclesiastes",
    ],
    "original-documents/rest_of_old_testament_restorative_translation.txt": [
        "song-of-solomon", "isaiah", "jeremiah", "lamentations", "ezekiel", "daniel",
        "hosea", "joel", "amos", "obadiah", "jonah", "micah", "nahum", "habakkuk",
        "zephaniah", "haggai", "zechariah", "malachi",
    ],
    "original-documents/matthew_restorative_translation.txt": ["matthew"],
    "original-documents/mark_restorative_translation.txt": ["mark"],
    "original-documents/luke_restorative_translation.txt": ["luke"],
    "original-documents/john_restorative_translation.txt": ["john"],
    "original-documents/acts_restorative_translation.txt": ["acts"],
    "original-documents/rest_of_new_testament_restorative_translation.txt": [
        "romans", "1-corinthians", "2-corinthians", "galatians", "ephesians", "philippians",
        "colossians", "1-thessalonians", "2-thessalonians", "1-timothy", "2-timothy",
        "titus", "philemon", "hebrews", "james", "1-peter", "2-peter", "1-john",
        "2-john", "3-john", "jude", "revelation",
    ],
}


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "Way-Translation-Release-Importer/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response, destination.open("wb") as target:
        shutil.copyfileobj(response, target)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_epub(path: Path) -> None:
    with ZipFile(path) as archive:
        damaged = archive.testzip()
        if damaged:
            raise RuntimeError(f"Damaged EPUB member: {damaged}")
        names = set(archive.namelist())
        if "mimetype" not in names or not any(name.endswith("genesis.xhtml") for name in names):
            raise RuntimeError("Downloaded file is not the expected whole-Bible EPUB")


def split_verses(entry: dict) -> list[tuple[int, str]]:
    text = entry["text"].strip()
    heading = f'{entry["book"]} {entry["chapter"]}'
    if text.startswith(heading):
        text = text[len(heading):].lstrip()
    parts = re.split(r"(?<!\S)(?=\d+\.\s)", text)
    verses = []
    for part in parts:
        match = re.match(r"(\d+)\.\s*(.*)", part.strip(), flags=re.DOTALL)
        if match:
            verses.append((int(match.group(1)), match.group(2).strip()))
    if not verses:
        raise RuntimeError(f'Could not parse verses for {entry["book"]} {entry["chapter"]}')
    return verses


def load_corpus(path: Path) -> list[dict]:
    corpus = json.loads(path.read_text(encoding="utf-8"))
    if len(corpus) != 1189:
        raise RuntimeError(f"Expected 1,189 chapters, received {len(corpus)}")
    if len({entry["slug"] for entry in corpus}) != 66:
        raise RuntimeError("Expected 66 canonical books")
    return corpus


def synchronize_sources(corpus: list[dict]) -> None:
    by_slug: dict[str, list[dict]] = defaultdict(list)
    for entry in corpus:
        by_slug[entry["slug"]].append(entry)

    for relative_path, slugs in SOURCE_GROUPS.items():
        output = []
        for slug in slugs:
            chapters = sorted(by_slug[slug], key=lambda item: item["chapter"])
            if not chapters:
                raise RuntimeError(f"Missing source book: {slug}")
            for entry in chapters:
                output.append(f'{entry["book"]} {entry["chapter"]}')
                output.extend(f"{number}. {text}" for number, text in split_verses(entry))
                output.append("")
        (ROOT / relative_path).write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")


def write_terminology_audit(corpus: list[dict], timestamp: str) -> None:
    terms = {"Adversary": [], "Slanderer": []}
    occurrences = {"Adversary": 0, "Slanderer": 0}
    stale = []
    for entry in corpus:
        for number, text in split_verses(entry):
            reference = f'{entry["book"]} {entry["chapter"]}:{number}'
            for term in terms:
                count = len(re.findall(rf"\b{term}\b", text))
                if count:
                    terms[term].append(reference)
                    occurrences[term] += count
            if re.search(r"\bha-Satan\b|\bdevil\b", text, flags=re.IGNORECASE):
                stale.append(reference)
    if stale:
        raise RuntimeError("Legacy terminology remains at: " + ", ".join(stale))

    payload = {
        "generatedAt": timestamp,
        "epubSha256": EXPECTED_SHA256,
        "method": {
            "satanHaSatanSatanas": "the Adversary",
            "diabolos": "the Slanderer",
            "daimonion": "demon (unchanged)",
        },
        "counts": {
            "AdversaryOccurrences": occurrences["Adversary"],
            "AdversaryVerses": len(terms["Adversary"]),
            "SlandererOccurrences": occurrences["Slanderer"],
            "SlandererVerses": len(terms["Slanderer"]),
        },
        "references": terms,
        "legacyTermReferences": stale,
    }
    report = ROOT / "change-logs" / "reports" / "ADVERSARY-SLANDERER-AUDIT-LATEST.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_history_log(snapshot: str, old_digest: str) -> None:
    row = (
        f"| {snapshot} | rendered-documents-history/{snapshot}/ | the-way-current.epub "
        f"(SHA-256 `{old_digest}`) | pre-September-2026 canonical snapshot archived before "
        "importing the verified Adversary/Slanderer release |\n"
    )
    existing = LOG.read_text(encoding="utf-8")
    if row not in existing:
        LOG.write_text(existing.rstrip() + "\n" + row, encoding="utf-8")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="way-release-") as directory:
        temp = Path(directory)
        epub = temp / "the-way-current.epub"
        search = temp / "search.json"
        download(EPUB_URL, epub)
        download(SEARCH_URL, search)
        digest = sha256(epub)
        if digest != EXPECTED_SHA256:
            raise RuntimeError(f"EPUB checksum mismatch: expected {EXPECTED_SHA256}, received {digest}")
        validate_epub(epub)
        corpus = load_corpus(search)

        current_digest = sha256(CURRENT)
        if current_digest == digest:
            print("Current EPUB already matches the verified release; no import needed")
            return

        now = datetime.now(timezone.utc).replace(microsecond=0)
        snapshot = now.strftime("%Y-%m-%d_%H%MUTC")
        archive_dir = HISTORY / snapshot
        archive_dir.mkdir(parents=True, exist_ok=False)
        shutil.copyfile(CURRENT, archive_dir / CURRENT.name)
        shutil.copyfile(epub, CURRENT)
        synchronize_sources(corpus)
        write_terminology_audit(corpus, now.isoformat().replace("+00:00", "Z"))
        append_history_log(snapshot, current_digest)
        print(f"Imported verified release {digest}; archived prior EPUB in {archive_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
