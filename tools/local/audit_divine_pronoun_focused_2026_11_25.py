#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
import release_2026_09_30_kingdom_residuals as rel

ROOT=rel.ROOT
EPUB=rel.EPUB
PRON=re.compile(r"\b(?:he|him|his|himself)\b",re.I)
START=re.compile(r"^[\s\"'“‘\[(]*(?:He|His|Him|Himself)\b")
DIV=re.compile(r"\b(?:YHWH|Elohim|God|Yah|Most High|Almighty|Creator|Cosmic Parent|Holy One)\b",re.I)
OUT=ROOT/"change-logs/reports/2026-11-25-divine-pronoun-focused-review.json"

def refs():
    v=rel.collect_verses(EPUB,slugs=rel.ALL_SLUGS)
    return v,{f"{rel.SLUG_TO_BOOK[s]} {c}:{n}":t for (s,c,n),t in v.items()}

def historical_rows():
    specs=[
      ("2026-09-10","change-logs/reports/2026-09-10-whole-bible-divine-pronoun-consistency.json","changes","original_phrase","replacement_phrase",None),
      ("2026-09-29","change-logs/reports/2026-09-29-divine-language-release.json","rows","before","after","divine pronoun"),
      ("2026-10-12","change-logs/reports/2026-10-12-nt-divine-referent-release.json","rows","before","after",None),
      ("2026-10-14-acts","change-logs/reports/2026-10-14-acts-revelation-divine-pronouns-release.json","approvedExactVerses","before","after",None),
      ("2026-10-14-romans","change-logs/reports/2026-10-14-romans-followup-4-divine-pronoun-release.json","changes","before","after",None),
      ("2026-10-12-1tim","change-logs/reports/2026-10-12-nt-divine-royal-followup-release.json","changes","before","after",None),
    ]
    out=[]
    for release,path,key,bk,ak,category in specs:
      p=ROOT/path
      if not p.exists(): continue
      d=json.loads(p.read_text(encoding="utf-8"))
      rows=d.get(key,[])
      for r in rows:
        if category and r.get("category")!=category: continue
        before=r.get(bk); after=r.get(ak)
        if not before or not after or before==after: continue
        out.append({"release":release,"reference":r["reference"],"before":before,"after":after})
    return out

def main():
    verses,by_ref=refs()
    hist=historical_rows()
    exact_reversions=[]
    pronoun_reappear=[]
    for r in hist:
      cur=by_ref.get(r["reference"])
      if cur is None: continue
      if cur==r["before"] and r["before"]!=r["after"]:
        exact_reversions.append({**r,"current":cur})
      if PRON.search(cur) and not PRON.search(r["after"]):
        pronoun_reappear.append({**r,"current":cur})
    carry=[]
    for (slug,ch,n),text in verses.items():
      if not START.search(text): continue
      prev=[]
      for dist in range(1,5):
        t=verses.get((slug,ch,n-dist))
        if t is not None: prev.append((dist,t))
      divine_prev=[(dist,t) for dist,t in prev if DIV.search(t)]
      if not divine_prev: continue
      carry.append({
        "reference":f"{rel.SLUG_TO_BOOK[slug]} {ch}:{n}",
        "text":text,
        "nearestDivineDistance":min(d for d,_ in divine_prev),
        "previous": [{"distance":d,"text":t} for d,t in prev],
      })
    # Explicit same-verse divine marker plus masculine pronoun, for a compact second review bucket.
    same=[]
    for (slug,ch,n),text in verses.items():
      if PRON.search(text) and DIV.search(text):
        same.append({"reference":f"{rel.SLUG_TO_BOOK[slug]} {ch}:{n}","text":text})
    result={
      "canonicalEpubSha256":rel.base.sha256(EPUB),
      "wholeBibleVerseCount":len(verses),
      "historicalApprovedRowsCompared":len(hist),
      "exactReversionsToPreviouslyRejectedBeforeText":exact_reversions,
      "exactReversionCount":len(exact_reversions),
      "historicalRowsWhereMasculinePronounExistsNowButApprovedAfterHadNone":pronoun_reappear,
      "pronounReappearanceCount":len(pronoun_reappear),
      "sentenceInitialCarryCandidatesWithinFourPriorVerses":carry,
      "carryCandidateCount":len(carry),
      "sameVerseDivineMarkerPronounCandidates":same,
      "sameVerseCandidateCount":len(same),
      "exodus35_34Carry":next((r for r in carry if r["reference"]=="Exodus 35:34"),None),
      "exodus35_35Carry":next((r for r in carry if r["reference"]=="Exodus 35:35"),None),
      "warning":"Candidate buckets require contextual review; only exact reversion to a previously approved before-text is intrinsically a regression."
    }
    OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
      "canonicalEpubSha256":result["canonicalEpubSha256"],
      "historicalApprovedRowsCompared":len(hist),
      "exactReversionCount":len(exact_reversions),
      "pronounReappearanceCount":len(pronoun_reappear),
      "carryCandidateCount":len(carry),
      "sameVerseCandidateCount":len(same),
      "exodus35_34Carry":bool(result["exodus35_34Carry"]),
      "exodus35_35Carry":bool(result["exodus35_35Carry"]),
      "exactReversionRefs":[r["reference"] for r in exact_reversions],
      "pronounReappearanceRefs":[r["reference"] for r in pronoun_reappear],
    },ensure_ascii=False,indent=2))
if __name__=="__main__":main()
