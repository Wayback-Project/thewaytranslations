#!/usr/bin/env python3
"""READ-ONLY preapproval audit: names/glosses in current canonical The Way EPUB.

Never mutates Scripture or generates a new EPUB. Its purpose is to validate
the historical source snapshot and reviewed candidate ledger before approval.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import release_2026_09_30_kingdom_residuals as rel

ROOT = rel.ROOT
EPUB = rel.EPUB
LEDGER = ROOT / "tools/local/2026-10-19-name-alias-collision-candidates.json"


def main() -> None:
    proposal = json.loads(LEDGER.read_text(encoding="utf-8"))
    expected = proposal["canonicalBaselineEpubSha256"]
    current_sha = rel.base.sha256(EPUB)
    if current_sha != expected:
        raise RuntimeError(
            f"Canonical EPUB changed: expected {expected}, found {current_sha}. "
            "Reaudit the latest version; never apply stale approved verses."
        )
    if proposal["status"] != "UNAPPROVED_PROPOSAL_DO_NOT_RELEASE" or proposal["releaseAuthorization"]:
        raise RuntimeError("A review-only audit must not authorize publication")
    if proposal["candidateCount"] != len(proposal["candidates"]) or proposal["candidateCount"] != 3:
        raise RuntimeError("Unexpected candidate count")
    corpus = rel.collect_verses(EPUB, slugs=rel.ALL_SLUGS)
    if len(corpus) != 31102:
        raise RuntimeError("Expected 31,102 verse records")
    seen = set()
    for r in proposal["candidates"]:
        k = (r["slug"], int(r["chapter"]), int(r["verse"]))
        if k in seen or k[0] not in ("acts", "john"):
            raise RuntimeError("Duplicate or unexpected source-gloss candidate: " + str(k))
        seen.add(k)
        if corpus.get(k) != r["current"]:
            raise RuntimeError("Full-verse candidate baseline differs: " + r["reference"])
        if r["current"] == r["recommendation"]:
            raise RuntimeError("Candidate proposal is a no-op: " + r["reference"])
        if r["status"] != "proposed-awaiting-editor-choice":
            raise RuntimeError("Candidate was approved without source review")
    if seen != {("acts",13,9),("john",1,42),("john",4,25)}:
        raise RuntimeError("Unexpected candidate scopes")

    controls = {
        ("acts",13,7): "Sergius Paulus",
        ("acts",13,13): "Shaul",
        ("romans",1,1): "Shaul",
        ("acts",1,23): "Barsabbas",
        ("john",11,16): "Didymus",
        ("daniel",2,26): "Belteshazzar",
        ("luke",6,14): "Bar-Tolmai",
        ("genesis",35,10): "no longer be called Yaakov",
    }
    for k, needle in controls.items():
        if needle not in corpus.get(k, ""):
            raise RuntimeError("Protected reference changed unexpectedly: " + repr(k))
    duplicate_candidates = [
        "%s %s:%s" % key
        for key, value in corpus.items()
        if re.search(r"\b([A-Z][a-z]{2,})\b.{0,80}\bwho (?:is|was) also called\s+\1\b", value)
    ]
    if "acts 13:9" not in duplicate_candidates:
        raise RuntimeError("Alias-collision regex missed the known Shaul/Shaul case")
    print(json.dumps({
        "status": "READ_ONLY_PROPOSAL_BASELINE_VALIDATED",
        "canonicalEpubSha256": current_sha,
        "books": 66,
        "chapters": 1189,
        "verseRecords": len(corpus),
        "reviewOnlyCandidates": sorted("%s %s:%s" % k for k in seen),
        "protectedContexts": len(controls),
        "candidateRegexHits": duplicate_candidates[:60],
        "published": False,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
