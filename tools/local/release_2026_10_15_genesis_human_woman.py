#!/usr/bin/env python3
"""Canonical-first Genesis 2–5 person-language release, finite ledger and fail-closed QA."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import release_2026_09_30_kingdom_residuals as rel

base = rel.base
ROOT, EPUB, REG = rel.ROOT, rel.EPUB, rel.REGISTRY
BASE = "4fbfbd979b9f6a37397ac21c17ad25bcae4d7743559fd8454abdfcd6d819df98"
LEDGER = ROOT / "tools/local/genesis-human-woman-consistency-2026-10-15.json"
REPORT = ROOT / "change-logs/reports/2026-10-15-genesis-human-woman-consistency-release.json"
NOTE = ROOT / "editor-notes/consistency/2026-10-15-genesis-human-woman-consistency-release.md"


def corpus(path: Path):
    return rel.collect_verses(path, slugs=rel.ALL_SLUGS)


def validated_rows(before):
    d = json.loads(LEDGER.read_text(encoding="utf-8"))
    rows = d["edits"]
    if d["canonicalBaselineEpubSha256"] != BASE or d["changedVerseCount"] != 10 or len(rows) != 10:
        raise RuntimeError("Unapproved ledger or baseline mismatch")
    keys = set()
    for r in rows:
        k = (r["slug"], r["chapter"], r["verse"])
        if r["slug"] != "genesis" or k in keys:
            raise RuntimeError("Duplicate/out-of-scope reference: " + str(k))
        keys.add(k)
        if before.get(k) != r["original"] or r["original"] == r["final"]:
            raise RuntimeError("Exact canonical verse mismatch: " + r["reference"])
        if "  " in r["final"] or re.search(r"\\s+[,.!?;:]", r["final"]):
            raise RuntimeError("Whitespace/grammar violation: " + r["reference"])
    if len(before) != 31102:
        raise RuntimeError("Expected 31,102 canonical verse records")
    return d, rows, keys


def write_trial(target: Path, rows):
    with zipfile.ZipFile(EPUB, "r") as zin:
        infos = zin.infolist()
        orig = {i.filename: zin.read(i.filename) for i in infos}
        member = base.find_book_member(zin, "genesis")
    changed = dict(orig)
    xml = changed[member].decode("utf-8")
    for r in rows:
        xml = rel.replace_one_verse(xml, "genesis", r["chapter"], r["verse"],
                                    r["original"], r["final"])
    ET.fromstring(xml.encode("utf-8"))
    changed[member] = xml.encode("utf-8")
    if {p for p in orig if orig[p] != changed[p]} != {member}:
        raise RuntimeError("Non-Genesis EPUB member unexpectedly changed")
    with zipfile.ZipFile(target, "w") as zout:
        for info in infos:
            zout.writestr(info, changed[info.filename], compress_type=info.compress_type)
    base.validate_epub(target)
    return member


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    check = parser.parse_args().check_only
    actual = base.sha256(EPUB)
    if actual != BASE:
        raise RuntimeError(f"Baseline changed: expected {BASE}, got {actual}. Re-review and regenerate ledger.")
    before = corpus(EPUB)
    ledger, rows, keys = validated_rows(before)
    oldissues, exceptions = rel.grammar.audit_epub(EPUB)
    if oldissues:
        raise RuntimeError("Baseline article-grammar audit failed")
    fd, path = tempfile.mkstemp(prefix="way-genesis-", suffix=".epub", dir=EPUB.parent)
    os.close(fd)
    trial = Path(path)
    try:
        member = write_trial(trial, rows)
        after = corpus(trial)
        diffs = {k for k in before if before[k] != after.get(k)}
        if len(after) != 31102 or diffs != keys:
            raise RuntimeError("Whole-Bible changes differ from the 10 authorized Genesis verses: " + repr(diffs ^ keys))
        for r in rows:
            if after[("genesis", r["chapter"], r["verse"])] != r["final"]:
                raise RuntimeError("Final whole-verse mismatch: " + r["reference"])
        protected = {
            "Genesis 1:27": ("genesis", 1, 27), "Genesis 2:7": ("genesis", 2, 7),
            "Genesis 2:18": ("genesis", 2, 18), "Genesis 2:23": ("genesis", 2, 23),
            "Genesis 3:6": ("genesis", 3, 6), "Genesis 3:16": ("genesis", 3, 16),
            "Genesis 3:17": ("genesis", 3, 17), "Genesis 4:17": ("genesis", 4, 17),
            "Genesis 6:5": ("genesis", 6, 5), "Genesis 8:21": ("genesis", 8, 21),
        }
        for ref, key in protected.items():
            if before.get(key) != after.get(key):
                raise RuntimeError("Protected contextual wording changed: " + ref)
        if any("the human" in after[("genesis", c, v)].lower()
               for c, v in [(2, 20), (2, 21), (2, 22), (2, 25), (3, 8)]):
            raise RuntimeError("Old man-only 'the human' reference survives after narrative transition")
        newissues, newexceptions = rel.grammar.audit_epub(trial)
        if newissues or len(newexceptions) != len(exceptions):
            raise RuntimeError("English-article grammar regression")
        newsha = base.sha256(trial)
        if check:
            print(json.dumps({"status": "check-pass", "priorEpubSha256": BASE,
                              "newEpubSha256": newsha, "changedVerses": 10,
                              "changedEpubMembers": [member],
                              "books": 66, "chapters": 1189, "verses": 31102,
                              "EPUB/ZIP/XML/internalLinks": "PASS"}))
            return
        now = datetime.now(timezone.utc)
        stamp = now.strftime("%Y-%m-%d_%H%M%SUTC")
        date = now.replace(microsecond=0).isoformat().replace("+00:00", "Z")
        archive_dir = ROOT / "rendered-documents-history" / stamp
        archive_dir.mkdir(parents=True, exist_ok=False)
        archive = archive_dir / EPUB.name
        shutil.copy2(EPUB, archive)
        if base.sha256(archive) != BASE:
            raise RuntimeError("Archive hash mismatch")
        reg = json.loads(REG.read_text(encoding="utf-8"))
        if reg.get("canonicalEpubSha256") != BASE:
            raise RuntimeError("Original name registry provenance mismatch")
        shutil.move(trial, EPUB)
        reg["canonicalEpubSha256"] = newsha
        REG.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        fallback = base.build_fallback(EPUB, reg, newsha, date)
        if tuple(fallback.get(k) for k in ("bookCount", "chapterCount", "verseSearchCount")) != (66, 1189, 31102):
            raise RuntimeError("Generated fallback inventory mismatch")
        report = {"date": date, "release": ledger["release"], "priorEpubSha256": BASE,
                  "releasedEpubSha256": newsha, "changedVerseCount": 10,
                  "changes": rows, "archivedPriorEpub": archive.relative_to(ROOT).as_posix(),
                  "changedEpubMembers": [member], "canonicalFallback": fallback,
                  "qa": {"exactDiffOnlyApproved": True, "verseCount": 31102,
                         "epubZipXmlLinks": "pass", "grammar": "pass",
                         "noUnrelatedScriptureChanges": True},
                  "printStatus": "Print master/PDF/proof not updated; separate handoff"}
        REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        NOTE.write_text(
            "# Genesis 2–5 human/man/woman/Havvah consistency — released\n\n"
            "Exact approved 10-verse changes with Hebrew reasoning are in "
            "editor-notes/proposals/2026-10-15-genesis-human-woman-consistency.md "
            "and tools/local/genesis-human-woman-consistency-2026-10-15.json.\n\n"
            f"Prior canonical EPUB SHA-256: {BASE}\nNew canonical EPUB SHA-256: {newsha}\n"
            f"Archived previous EPUB: {archive.relative_to(ROOT).as_posix()}\n\n"
            "QA: exact 10 whole-verse differences; all others protected across 31,102 Bible "
            "verses; valid EPUB ZIP/CRC/XML and links; 66 books/1,189 chapters; "
            "source-sensitive human/man/woman language and print independence.\n",
            encoding="utf-8")
        base.append_once(rel.HISTORY_LOG, newsha,
                         f"- {stamp} — Genesis 2–5 person-language 10-verse release; archive {archive.relative_to(ROOT).as_posix()}; new SHA-256 {newsha}.")
        base.append_once(rel.REFRESH, "## 2026-10-15 Genesis person-language release",
                         f"## 2026-10-15 Genesis person-language release\n\n"
                         f"10 context-sensitive Genesis 2–5 verse changes; canonical SHA-256: {newsha}. "
                         "See exact editorial ledger and original Hebrew rationale.")
        base.replace_sha_in_file(rel.ROOT_README, BASE, newsha)
        base.replace_sha_in_file(rel.CURRENT_README, BASE, newsha)
        print(json.dumps({"status": "canonical-released", "sha": newsha,
                          "changedVerses": 10, "fallback": fallback}, ensure_ascii=False))
    finally:
        trial.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
