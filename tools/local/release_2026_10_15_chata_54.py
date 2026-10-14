#!/usr/bin/env python3
"""Release exactly 54 contextual Chata revisions on latest October 14 EPUB.
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
BASE_SHA="094be0ae8786e2e407515b5485946fc8ce35162fc4d0e62815b7983cf3ec4ffa"
LEDGER=ROOT/"tools/local/chata-2026-10-15-exact-verse-ledger.json"
REPORT=ROOT/"change-logs/reports/2026-10-15-chata-first-54-verse-release.json"
NOTE=ROOT/"editor-notes/consistency/2026-10-15-chata-first-54-verse-release.md"
SIN=re.compile(r"\b(?:sin(?:s|ned|ning|ful(?:ness|ly)?|less)?|sinner(?:s)?)\b",re.I)
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
 if ledger["canonicalBaselineEpubSha256"]!=BASE_SHA or len(rows)!=54 or ledger["count"]!=54:
  raise RuntimeError("The baseline or finite release count changed")
 keys={(r["slug"],r["chapter"],r["verse"]) for r in rows}
 if len(keys)!=54 or not all(r["slug"] in rel.ALL_SLUGS for r in rows):
  raise RuntimeError("Duplicate or invalid release verse")
 for r in rows:
  if not SIN.search(r["original"]) or r["original"]==r["final"]:
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
 preissues,exceptions=rel.grammar.audit_epub(EPUB)
 if preissues:raise RuntimeError("Baseline grammar issue; stop")
 if dry:
  print(json.dumps({"check":"pass","baselineSha":BASE_SHA,"exactVerseEdits":54,"wholeBibleVerses":31102}))
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
 if len(after)!=31102 or diff!=keys:
  raise RuntimeError("Whole-Bible diff is not exactly 54 approved verses")
 for r in rows:
  k=(r["slug"],r["chapter"],r["verse"])
  if after.get(k)!=r["final"]:raise RuntimeError("Changed verse does not match ledger "+r["reference"])
 for k,text in PROTECTED.items():
  if after[k]!=text:raise RuntimeError("October 14 pronoun regression")
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
  "date":"2026-10-15","release":"Chata finite moral-failure context review",
  "priorEpubSha256":BASE_SHA,"releasedEpubSha256":newsha,
  "changedVerseCount":54,"changes":rows,
  "archivedPriorEpub":archive.relative_to(ROOT).as_posix(),
  "changedEpubMembers":sorted(changed),"canonicalFallback":fallback,
  "qa":{"expectedVerses":31102,"afterVerses":len(after),
        "exactDiffVerses":54,"priorMasculinePronounReleasePreserved":True,
        "epubZipXmlLinks":"pass","articleGrammar":"pass"},
  "remainingSinFamily":"Unreviewed Chata inventory not released in this finite wave",
  "printStatus":"Actual Word master/typeset PDF require separate reconciliation"}
 REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 NOTE.write_text(
  "# Chata finite 54-verse release — 15 October 2026\n\n"
  "The original 863-token Chata audit is NOT a blanket replacement directive. "
  "This release implements 54 exact contextual before/after Scripture verses, with moral failure / failed morally first, "
  "and wrongdoing where direct harm or power imagery makes that clearer.\n\n"
  f"Previous canonical EPUB SHA: {BASE_SHA}\nNew canonical EPUB SHA: {newsha}\n"
  f"Archived prior EPUB: {archive.relative_to(ROOT).as_posix()}\n\n"
  "Validated exactly 54 whole-Bible verse diffs, 31,102 record inventory, EPUB ZIP/XML/links and article QA. "
  "October 14 masculine God pronouns are preserved.\n"
  "Original-name glossary, website reader and mobile feeds must be rebuilt from the exact new canonical EPUB.\n"
  "Remaining cases stay in the Chata context-review inventory.\n"
  "Physical print Word master/PDF require separate changes and proof.\n",
  encoding="utf-8")
 base.append_once(rel.HISTORY_LOG,newsha,
  f"- {stamp} — Chata 54 exact moral-failure / wrongdoing verses; previous EPUB archived: {archive.relative_to(ROOT).as_posix()}; new SHA-256 {newsha}.")
 base.append_once(rel.REFRESH,"## 2026-10-15 Chata 54-verse finite release",
  "## 2026-10-15 Chata 54-verse finite release\n\n"
  f"Exactly 54 context-sensitive edits from approved finite ledger. New canonical SHA-256: {newsha}. "
  "Remaining Chata instances pending contextual review. No earlier God-pronoun revisions changed.")
 base.replace_sha_in_file(rel.ROOT_README,BASE_SHA,newsha)
 base.replace_sha_in_file(rel.CURRENT_README,BASE_SHA,newsha)
 print(json.dumps({"status":"canonical-released","sha":newsha,
  "changedVerses":54,"canonicalFallback":fallback},ensure_ascii=False,indent=2))

if __name__=="__main__":main()
