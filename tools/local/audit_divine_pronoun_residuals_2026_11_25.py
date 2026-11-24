#!/usr/bin/env python3
"""Read-only whole-Bible audit for residual masculine divine pronouns.

This audit never edits Scripture. It scans the current canonical EPUB and produces
candidate inventories for contextual review under The Way Version policy:
unmistakable YHWH/Elohim/God referents should not use English he/him/his/himself;
historically male Yeshua/Messiah referents, actual male humans, and ambiguous
referents remain masculine unless separately reviewed.
"""
from __future__ import annotations

import csv, hashlib, json, re
from collections import Counter
from pathlib import Path

import release_2026_09_30_kingdom_residuals as rel

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / "current-form-documents" / "the-way-current.epub"
EXPECTED_SHA = "5fd2cbd9544e95e69abbb6fc74d9fde16553fa42cc95b4b79d196098486757e9"
OUT_JSON = ROOT / "change-logs/reports/2026-11-25-divine-pronoun-residual-audit.json"
OUT_MD = ROOT / "change-logs/reports/2026-11-25-divine-pronoun-residual-audit.md"
OUT_TSV = ROOT / "change-logs/reports/2026-11-25-divine-pronoun-residual-candidates.tsv"

BOOKS = {
"genesis":"Genesis","exodus":"Exodus","leviticus":"Leviticus","numbers":"Numbers",
"deuteronomy":"Deuteronomy","joshua":"Joshua","judges":"Judges","ruth":"Ruth",
"1-samuel":"1 Samuel","2-samuel":"2 Samuel","1-kings":"1 Kings","2-kings":"2 Kings",
"1-chronicles":"1 Chronicles","2-chronicles":"2 Chronicles","ezra":"Ezra","nehemiah":"Nehemiah",
"esther":"Esther","job":"Job","psalms":"Psalms","proverbs":"Proverbs",
"ecclesiastes":"Ecclesiastes","song-of-solomon":"Song of Solomon","isaiah":"Isaiah",
"jeremiah":"Jeremiah","lamentations":"Lamentations","ezekiel":"Ezekiel","daniel":"Daniel",
"hosea":"Hosea","joel":"Joel","amos":"Amos","obadiah":"Obadiah","jonah":"Jonah",
"micah":"Micah","nahum":"Nahum","habakkuk":"Habakkuk","zephaniah":"Zephaniah",
"haggai":"Haggai","zechariah":"Zechariah","malachi":"Malachi","matthew":"Matthew",
"mark":"Mark","luke":"Luke","john":"John","acts":"Acts","romans":"Romans",
"1-corinthians":"1 Corinthians","2-corinthians":"2 Corinthians","galatians":"Galatians",
"ephesians":"Ephesians","philippians":"Philippians","colossians":"Colossians",
"1-thessalonians":"1 Thessalonians","2-thessalonians":"2 Thessalonians","1-timothy":"1 Timothy",
"2-timothy":"2 Timothy","titus":"Titus","philemon":"Philemon","hebrews":"Hebrews",
"james":"James","1-peter":"1 Peter","2-peter":"2 Peter","1-john":"1 John",
"2-john":"2 John","3-john":"3 John","jude":"Jude","revelation":"Revelation",
}
NT = {"matthew","mark","luke","john","acts","romans","1-corinthians","2-corinthians",
"galatians","ephesians","philippians","colossians","1-thessalonians","2-thessalonians",
"1-timothy","2-timothy","titus","philemon","hebrews","james","1-peter","2-peter",
"1-john","2-john","3-john","jude","revelation"}

PRON = re.compile(r"\b(?:he|him|his|himself)\b", re.I)
START = re.compile(r"^[\s\"'“‘\[(]*(?:He|His|Him|Himself)\b")
DIV_STRONG = re.compile(r"\b(?:YHWH|Elohim|God|Yah|Most High|Almighty|Creator|Cosmic Parent|Holy One)\b", re.I)
DIV_WIDE = re.compile(r"\b(?:YHWH|Elohim|God|Yah|Most High|Almighty|Creator|Cosmic Parent|Holy One|Ruach|Spirit|Master|Sovereign)\b", re.I)
YESHUA = re.compile(r"\b(?:Yeshua|Jesus|Messiah|Christ|Lamb|Son of God|Son of Man|the Son)\b", re.I)
HUMAN_CUE = re.compile(r"\b(?:Pharaoh|Moshe|Aharon|Dawid|Shlomo|Shaul|Kepha|Yosef|Yehoshua|king|priest|prophet|angel|messenger|man|woman|person|father|mother|brother|son|servant|ruler|governor|husband)\b", re.I)
DIV_ATTR = re.compile(r"\bhis\s+(?:name|glory|power|mercy|grace|wrath|anger|eyes|sight|hand|word|voice|commandments?|statutes?|covenant|works?|wonders?|holiness|temple|sanctuary|people|servants?|prophets?|will|purpose|righteousness|judgment|justice|throne|reign)\b", re.I)
DIV_ACTION = re.compile(r"\bHe\s+(?:has|had|will|would|is|was|gave|gives|made|makes|filled|put|sent|sends|raised|raises|created|creates|spoke|speaks|said|says|called|calls|delivered|delivers|saved|saves|blessed|blesses|judged|judges|commanded|commands|revealed|reveals|showed|shows|dwells|reigns|forgives|heals)\b")
DEVOTION = re.compile(r"\b(?:praise|worship|serve|seek|trust|obey|revere|fear|exalt|thank|call on|pray to|return to|wait for|hope in)\s+(?:him|his)\b", re.I)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def parse():
    extracted=rel.collect_verses(EPUB, slugs=rel.ALL_SLUGS)
    rows=[]
    for (slug, chapter, verse), text in extracted.items():
        rows.append({
            "slug": slug,
            "book": BOOKS.get(slug, slug),
            "testament": "NT" if slug in NT else "OT",
            "chapter": chapter,
            "verse": verse,
            "text": text,
        })
    rows.sort(key=lambda v:(list(BOOKS).index(v["slug"]) if v["slug"] in BOOKS else 999, v["chapter"], v["verse"]))
    return rows

def ref(v): return f"{v['book']} {v['chapter']}:{v['verse']}"

def main():
    actual=sha256(EPUB)
    if actual != EXPECTED_SHA:
        raise SystemExit(f"baseline SHA mismatch expected={EXPECTED_SHA} got={actual}")
    verses=parse()
    if len(verses)!=31102:
        raise RuntimeError(f"verse inventory mismatch {len(verses)}")
    by_key={(v["slug"],v["chapter"],v["verse"]):v for v in verses}
    pronoun_verses=[v for v in verses if PRON.search(v["text"])]
    candidates=[]
    for v in pronoun_verses:
        key=(v["slug"],v["chapter"],v["verse"])
        contexts=[]
        for delta in (-4,-3,-2,-1,1):
            q=by_key.get((v["slug"],v["chapter"],v["verse"]+delta))
            if q: contexts.append((delta,q))
        prevs=[q for d,q in contexts if d<0]
        strong_same=bool(DIV_STRONG.search(v["text"]))
        wide_same=bool(DIV_WIDE.search(v["text"]))
        recent_strong=[]
        recent_wide=[]
        for d,q in contexts:
            if d<0 and DIV_STRONG.search(q["text"]): recent_strong.append((d,q))
            if d<0 and DIV_WIDE.search(q["text"]): recent_wide.append((d,q))
        start=bool(START.search(v["text"]))
        score=0; signals=[]
        if strong_same: score+=5; signals.append("strong-divine-marker-same-verse")
        elif wide_same: score+=3; signals.append("wide-divine-marker-same-verse")
        if start and recent_strong:
            dist=min(abs(d) for d,_ in recent_strong); score+=max(2,6-dist); signals.append(f"sentence-initial-pronoun-after-strong-divine-within-{dist}")
        elif start and recent_wide:
            dist=min(abs(d) for d,_ in recent_wide); score+=max(1,4-dist); signals.append(f"sentence-initial-pronoun-after-wide-divine-within-{dist}")
        if DIV_ATTR.search(v["text"]) and (strong_same or recent_strong):
            score+=3; signals.append("divine-attribute-pattern")
        if DEVOTION.search(v["text"]) and (strong_same or recent_strong):
            score+=3; signals.append("devotion-object-pattern")
        if DIV_ACTION.search(v["text"]) and recent_strong:
            score+=3; signals.append("sentence-initial-divine-action")
        if YESHUA.search(v["text"]):
            score-=3; signals.append("Yeshua-male-referent-present")
        if HUMAN_CUE.search(v["text"]):
            score-=1; signals.append("human-cue-present")
        # Include all same-verse strong divine cases, and carry-over cases scoring >=4.
        if strong_same or score>=4:
            prev_text=" || ".join(f"{ref(q)} {q['text']}" for d,q in contexts if d<0)
            next_text=" || ".join(f"{ref(q)} {q['text']}" for d,q in contexts if d>0)
            candidates.append({**v,"reference":ref(v),"score":score,"signals":signals,
                               "previous_context":prev_text,"next_context":next_text})
    candidates.sort(key=lambda r:(-r["score"], r["testament"], r["book"], r["chapter"], r["verse"]))
    stats={
        "canonicalEpubSha256":actual,
        "wholeBibleVerseCount":len(verses),
        "versesWithMasculinePronoun":len(pronoun_verses),
        "candidateVerseCount":len(candidates),
        "candidateOT":sum(r["testament"]=="OT" for r in candidates),
        "candidateNT":sum(r["testament"]=="NT" for r in candidates),
        "highPriorityScore8Plus":sum(r["score"]>=8 for r in candidates),
        "mediumPriorityScore6to7":sum(6<=r["score"]<8 for r in candidates),
        "carryCandidatesScore4to5":sum(4<=r["score"]<6 for r in candidates),
        "exodus35_35Detected":any(r["reference"]=="Exodus 35:35" for r in candidates),
        "exodus35_34Detected":any(r["reference"]=="Exodus 35:34" for r in candidates),
        "candidateCountsByBook":dict(sorted(Counter(r["book"] for r in candidates).items())),
    }
    payload={
      "status":"CANDIDATE DISCOVERY ONLY. No Scripture changes. Every candidate requires contextual referent review.",
      "policy":"Remove masculine English pronouns only for unmistakable divine referents. Preserve Yeshua/Messiah historical male reference, actual male humans, quotations and ambiguous cases.",
      "summary":stats,"candidates":candidates
    }
    OUT_JSON.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    fields=["reference","testament","book","chapter","verse","score","signals","text","previous_context","next_context"]
    with OUT_TSV.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n"); w.writeheader()
        for r in candidates:
            row={k:r[k] for k in fields}; row["signals"]="; ".join(row["signals"]); w.writerow(row)
    lines=["# Whole-Bible residual masculine divine-pronoun audit — 2026-11-25","",
      "**Status: candidate discovery only. No Scripture changes were made.**","",
      "This reruns the divine-referent policy against the current canonical Oct. 28 EPUB. "
      "A candidate is not automatically an error: Yeshua/Messiah and real male humans remain masculine, "
      "and ambiguous antecedents require contextual review.","",
      f"- Canonical EPUB SHA-256: `{actual}`",
      f"- Whole Bible verses: **{len(verses)}**",
      f"- Verses containing he/him/his/himself: **{len(pronoun_verses)}**",
      f"- Contextual candidates requiring review: **{len(candidates)}** (OT {stats['candidateOT']}, NT {stats['candidateNT']})",
      f"- High priority (score 8+): **{stats['highPriorityScore8Plus']}**",
      f"- Medium priority (score 6–7): **{stats['mediumPriorityScore6to7']}**",
      f"- Carry/context candidates (score 4–5): **{stats['carryCandidatesScore4to5']}**",
      f"- Exodus 35:34 detected: **{stats['exodus35_34Detected']}**",
      f"- Exodus 35:35 detected: **{stats['exodus35_35Detected']}**","",
      "## Highest-priority review queue",""]
    for r in candidates:
        if r["score"]<8: break
        lines.append(f"- **{r['reference']}** (score {r['score']}): {r['text']}")
        lines.append(f"  - Signals: {', '.join(r['signals'])}")
        if r["previous_context"]: lines.append(f"  - Prior context: {r['previous_context']}")
    lines += ["","## Review rule","",
      "Read the verse with at least the preceding four verses and following verse. Classify each masculine pronoun as: "
      "(A) unmistakably YHWH/Elohim/God/divine title, propose recast; (B) Yeshua/Messiah, retain; "
      "(C) actual male human/angelic speaker, retain; (D) generic human, separately review under inclusive-human policy; "
      "(E) ambiguous/poetic/quoted, retain unless independently resolved.","",
      f"Full candidate inventory: `{OUT_TSV.relative_to(ROOT)}` and machine JSON: `{OUT_JSON.relative_to(ROOT)}`."
    ]
    OUT_MD.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(stats,indent=2))

if __name__=="__main__":
    main()
