#!/usr/bin/env python3
"""Release exactly 17 contextual copyedits after Chata's 666 verse release.
Fail closed if baseline, source words, verse count, grammar or EPUB checks drift.
No bulk sin-family substitution and no rewriting later masculine pronoun edits.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import tempfile
import zipfile
from collections import defaultdict
from datetime import datetime,timezone
from pathlib import Path
import release_2026_09_30_kingdom_residuals as rel

base=rel.base
ROOT,EPUB,REG=rel.ROOT,rel.EPUB,rel.REGISTRY
BASE_SHA="b1775a6ba98b7fbbef2a733890b5087e0835bcb4d647e520610704c6afdfb73e"
LEDGER=ROOT/"tools/local/chata-wave2-post-qa-copyedits.json"
REPORT=ROOT/"change-logs/reports/2026-10-15-chata-post-wave2-17-copyedits-release.json"
NOTE=ROOT/"editor-notes/consistency/2026-10-15-chata-post-wave2-17-copyedits-release.md"
SIN=re.compile(r"\b(?:sin(?:s|ned|ning|ful(?:ness|ly)?|less)?|sinner(?:s)?)\b",re.I)
EXPECTED_HELD={
 ("exodus",16,1),("exodus",17,1),("numbers",33,11),("numbers",33,12),
 ("ezekiel",30,15),("ezekiel",30,16),
 ("psalms",51,5),("1-samuel",15,18),("amos",8,14),
 ("2-corinthians",5,21),("2-thessalonians",2,3),
 ("hebrews",9,28),("revelation",21,8),
}
PREVIOUS=ROOT/"change-logs/reports/2026-10-15-chata-wave2-666-verse-release.json"
PROTECTED={
 ("romans",4,21):"and being fully assured that what God had promised, God was able also to perform.",
 ("romans",9,18):"So then, God has mercy on whom God desires, and God hardens whom God desires.",
 ("romans",15,10):'Again Scripture says, "Rejoice, you Gentiles, with God’s people."',
 ("romans",15,11):'Again, "Praise the Master, all you Gentiles! Let all the peoples praise the Master."',
}

def collect():
 return rel.collect_verses(EPUB,slugs=rel.ALL_SLUGS)

def main():
 args=argparse.ArgumentParser()
 args.add_argument("--check-only",action="store_true")
 dry=args.parse_args().check_only
 ledger=json.loads(LEDGER.read_text(encoding="utf-8"))
 rows=ledger["edits"]
 if ledger["canonicalBaselineEpubSha256"]!=BASE_SHA or len(rows)!=17 or ledger["count"]!=17:
  raise RuntimeError("The baseline or finite release count changed")
 keys={(r["slug"],r["chapter"],r["verse"]) for r in rows}
 if len(keys)!=17 or not all(r["slug"] in rel.ALL_SLUGS for r in rows):
  raise RuntimeError("Duplicate or invalid release verse")
 for r in rows:
  if r["original"]==r["final"]:
   raise RuntimeError("Invalid lexical candidate: "+r["reference"])
  if "  " in r["final"] or re.search(r"\s+[,.!?;:]",r["final"]):
   raise RuntimeError("Punctuation or spacing issue: "+r["reference"])
 if base.sha256(EPUB)!=BASE_SHA:
  raise RuntimeError("CANONICAL BASELINE CHANGED. Rereview the newest EPUB; no older release may overwrite it")
 before=collect()
 if len(before)!=31102: raise RuntimeError("Expected 31,102 existing Scripture verse records")
 for r in rows:
  k=(r["slug"],r["chapter"],r["verse"])
  if before.get(k)!=r["original"]:
   raise RuntimeError("Full-verse baseline mismatch: "+r["reference"])
 for k,text in PROTECTED.items():
  if before.get(k)!=text: raise RuntimeError("October 14 pronoun guard mismatch: "+repr(k))
 old_report=json.loads(PREVIOUS.read_text(encoding="utf-8"))
 if old_report["releasedEpubSha256"]!=BASE_SHA or old_report["changedVerseCount"]!=666:
  raise RuntimeError("Earlier 666-verse Chata canonical release drift")
 for old in old_report["changes"]:
  key=(old["slug"],old["chapter"],old["verse"])
  if before.get(key)!=old["final"]:
   raise RuntimeError("Earlier 666-verse Chata regression before release: "+old["reference"])
 preissues,exceptions=rel.grammar.audit_epub(EPUB)
 if preissues:raise RuntimeError("Baseline grammar issue; stop")
 if dry:
  trial=defaultdict(list)
  for r in rows:trial[r["slug"]].append(r)
  with zipfile.ZipFile(EPUB) as zin:
   for slug,items in trial.items():
    member=base.find_book_member(zin,slug)
    xml=zin.read(member).decode("utf-8")
    for r in items:
     xml=rel.replace_one_verse(xml,slug,r["chapter"],r["verse"],r["original"],r["final"])
  print(json.dumps({"check":"pass","baselineSha":BASE_SHA,"exactVerseEdits":17,
                    "wholeBibleVerses":31102,"allExactXhtmlReplacements":"pass"}))
  return
 now=datetime.now(timezone.utc)
 stamp=now.strftime("%Y-%m-%d_%H%M%SUTC")
 time=now.replace(microsecond=0).isoformat().replace("+00:00","Z")
 archive_dir=ROOT/"rendered-documents-history"/stamp
 archive_dir.mkdir(parents=True,exist_ok=False)
 archive=archive_dir/EPUB.name
 shutil.copy2(EPUB,archive)
 if base.sha256(archive)!=BASE_SHA:raise RuntimeError("Archive checksum mismatch")
 grouped=defaultdict(list)
 for r in rows:grouped[r["slug"]].append(r)
 with zipfile.ZipFile(EPUB,"r") as zin:
  infos=zin.infolist()
  original={x.filename:zin.read(x.filename) for x in infos}
  members={slug:base.find_book_member(zin,slug) for slug in grouped}
 updated=dict(original)
 for slug,items in grouped.items():
  member=members[slug]
  xml=updated[member].decode("utf-8")
  for r in items:
   xml=rel.replace_one_verse(xml,slug,r["chapter"],r["verse"],r["original"],r["final"])
  updated[member]=xml.encode("utf-8")
 changed={p for p in updated if updated[p]!=original[p]}
 if changed!=set(members.values()):
  raise RuntimeError("EPUB member scope not exactly the approved changed books")
 fd,tmpname=tempfile.mkstemp(prefix="chata-",suffix=".epub",dir=EPUB.parent)
 os.close(fd);tmp=Path(tmpname)
 try:
  with zipfile.ZipFile(tmp,"w") as zout:
   for info in infos:zout.writestr(info,updated[info.filename],compress_type=info.compress_type)
  base.validate_epub(tmp)
  shutil.move(tmp,EPUB)
 finally:tmp.unlink(missing_ok=True)
 after=collect()
 diff={k for k in before if after.get(k)!=before[k]}
 remaining=sum(len(SIN.findall(t)) for t in after.values())
 retained={key for key,value in after.items() if SIN.search(value)}
 if remaining!=15 or retained!=EXPECTED_HELD:
  raise RuntimeError("Unexpected sin-family residuals: tokens "+str(remaining)+" references "+str(retained ^ EXPECTED_HELD))
 if len(after)!=31102 or diff!=keys:
  raise RuntimeError("Whole-Bible diff is not exactly 17 approved verses")
 for r in rows:
  k=(r["slug"],r["chapter"],r["verse"])
  if after.get(k)!=r["final"]:raise RuntimeError("Changed verse does not match ledger "+r["reference"])
 for k,text in PROTECTED.items():
  if after[k]!=text:raise RuntimeError("October 14 pronoun regression")
 for old in old_report["changes"]:
  key=(old["slug"],old["chapter"],old["verse"])
  if key not in keys and after.get(key)!=old["final"]:
   raise RuntimeError("Earlier 666-verse Chata revision unexpectedly changed: "+old["reference"])
 postissues,postexceptions=rel.grammar.audit_epub(EPUB)
 if postissues or len(postexceptions)!=len(exceptions):
  raise RuntimeError("English article grammar regression")
 newsha=base.sha256(EPUB)
 reg=json.loads(REG.read_text(encoding="utf-8"))
 if reg["canonicalEpubSha256"]!=BASE_SHA:raise RuntimeError("Source registry mismatch")
 reg["canonicalEpubSha256"]=newsha
 REG.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 fallback=base.build_fallback(EPUB,reg,newsha,time)
 if (fallback.get("bookCount"),fallback.get("chapterCount"),fallback.get("verseSearchCount"))!=(66,1189,31102):
  raise RuntimeError("Generated public mobile fallback inventory mismatch")
 report={
  "date":"2026-10-15","release":"Chata 17 post-wave2 copyedits, natural grammar and faithful referents",
  "priorEpubSha256":BASE_SHA,"releasedEpubSha256":newsha,
  "changedVerseCount":17,"changes":rows,
  "archivedPriorEpub":archive.relative_to(ROOT).as_posix(),
  "changedEpubMembers":sorted(changed),"canonicalFallback":fallback,
  "qa":{"expectedVerses":31102,"afterVerses":len(after),
        "exactDiffVerses":17,"priorMasculinePronounReleasePreserved":True,
        "epubZipXmlLinks":"pass","articleGrammar":"pass"},
  "remainingSinFamily":"Six proper Sin place names and seven held source cases remain unchanged; full audit documents residuals",
  "printStatus":"Google Doc print ledger and Word handoff need update; printed PDF/full print master separate"}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 NOTE.write_text(
  "# Chata 17-verse post-wave-two copyediting release — 15 October 2026\n\n"
  "The existing 666 Chata changes and earlier divine pronoun edits remain protected. "
  "This finite release corrects 17 awkward grammar or referent constructions; "
  "the exact full-verse before/after decisions and rationale are in "
  "tools/local/chata-wave2-post-qa-copyedits.json.\n\n"
  f"Prior EPUB SHA-256: {BASE_SHA}\nNew EPUB SHA-256: {newsha}\n"
  f"Archived EPUB: {archive.relative_to(ROOT).as_posix()}\n\n"
  "Checks: exact 17 whole-verse diffs, 31,102 total Scripture verses, "
  "15 deliberate source-sensitive sin-family residual tokens, 666 protected prior revisions "
  "(except expressly corrected verses), prior God pronouns, EPUB ZIP/XML and grammar validation.\n"
  "Append these 17 current-to-final copyedits to the print document after the 666-verse change register.\n",
  encoding="utf-8")
 base.append_once(rel.HISTORY_LOG,newsha,
  f"- {stamp} — Chata 17 post-wave2 careful grammar/referent corrections; previous EPUB archived: {archive.relative_to(ROOT).as_posix()}; new SHA-256 {newsha}.")
 base.append_once(rel.REFRESH,"## 2026-10-15 Chata 17 post-wave2 copyedits",
  "## 2026-10-15 Chata 17 post-wave2 copyedits\n\n"
  f"Exactly 17 idiomatic grammar and semantic copyedits, preserving previous 666 verse corrections. New canonical SHA-256: {newsha}. "
  "Remaining Chata instances pending contextual review. No earlier God-pronoun revisions changed.")
 base.replace_sha_in_file(rel.ROOT_README,BASE_SHA,newsha)
 base.replace_sha_in_file(rel.CURRENT_README,BASE_SHA,newsha)
 print(json.dumps({"status":"canonical-released","sha":newsha,
  "changedVerses":17,"canonicalFallback":fallback},ensure_ascii=False,indent=2))

if __name__=="__main__":main()
