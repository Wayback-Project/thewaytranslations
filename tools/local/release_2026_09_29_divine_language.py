#!/usr/bin/env python3
import base64,hashlib,json,os,re,shutil,tempfile,zlib,zipfile
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
import release_2026_09_26_evil_to_brokenness_direct as prev

base,grammar=prev.base,prev.grammar
replace_one_verse,collect_verses=prev.replace_one_verse,prev.collect_verses
ROOT,EPUB,REGISTRY=prev.ROOT,prev.EPUB,prev.REGISTRY
ROOT_README,CURRENT_README,HISTORY_LOG,REFRESH=prev.ROOT_README,prev.CURRENT_README,prev.HISTORY_LOG,prev.REFRESH
BASE_SHA="6a3a0dbc91949b082fdcf7c93d0832fe6762440933d8528009cf44b2271dfb92"
BASE_COMMIT="ada4a755463f6de6744e5e77070aa78fcc752a33"
DOC_ID="1hMhucZyhscYmW6alHBTsldrNg5P5Hl1lqmRx6oBn2Po"
DOC_REV="ANLCKQm2Ioa5QFnbPM_roDduqkXre-hKfAoHABp2S6-zAznyvcnik9jKuttMDtGaSXyS31RO8B_bhoEWnQQyHU2MxhSilJj7p4FMtoBKTqA"
PAYLOAD_SHA="616f64c6e8d1eab8dd87952c9027a24439e4c8f23af9a61ef7de405797d7df65"
AUTH=ROOT/"tools/local/2026-09-29-divine-language-authority.zlib.b64"
REPORT=ROOT/"change-logs/reports/2026-09-29-divine-language-release.json"
NOTE=ROOT/"editor-notes/consistency/2026-09-29-divine-language-release.md"
BOOK_TO_SLUG,SLUG_TO_BOOK,ALL_SLUGS=prev.BOOK_TO_SLUG,prev.SLUG_TO_BOOK,prev.ALL_SLUGS

def load_rows():
    raw=zlib.decompress(base64.b64decode(AUTH.read_text().strip()))
    if hashlib.sha256(raw).hexdigest()!=PAYLOAD_SHA: raise RuntimeError("authority payload SHA mismatch")
    rows=json.loads(raw)
    if len(rows)!=177: raise RuntimeError(f"authority rows={len(rows)}")
    counts=Counter(r["c"] for r in rows)
    exp=Counter({"divine pronoun":124,"divine royal title":40,"divine reign terminology":11,"source / collective pronoun correction":1,"audited — no change":1})
    if counts!=exp: raise RuntimeError(f"category counts={dict(counts)}")
    changed=[r for r in rows if r["b"]!=r["a"]]
    same=[r for r in rows if r["b"]==r["a"]]
    if len(changed)!=176 or [r["r"] for r in same]!=["Psalms 45:6"]: raise RuntimeError("change/no-change boundary mismatch")
    for r in rows:
        m=re.match(r"^(.*)\s+(\d+):(\d+)$",r["r"])
        if not m or m.group(1) not in BOOK_TO_SLUG: raise RuntimeError(f"bad reference {r['r']}")
        r["s"],r["ch"],r["v"]=BOOK_TO_SLUG[m.group(1)],int(m.group(2)),int(m.group(3))
    return rows,changed,counts
ROWS,CHANGES,CATEGORY_COUNTS=load_rows()
CHANGE_KEYS={(r["s"],r["ch"],r["v"]) for r in CHANGES}
CHANGED_SLUGS=tuple(sorted({r["s"] for r in CHANGES}))

def collect(path,all_bible=False):
    return collect_verses(path,slugs=ALL_SLUGS if all_bible else CHANGED_SLUGS)

def exact(path,after=False):
    vm=collect(path,True); errs=[]
    for r in ROWS:
        want=r["a"] if after else r["b"]; got=vm.get((r["s"],r["ch"],r["v"]))
        if got!=want: errs.append({"reference":r["r"],"expected":want,"actual":got})
    if errs: raise RuntimeError(("after" if after else "before")+" authority mismatch: "+json.dumps(errs[:20],ensure_ascii=False,indent=2))

def rewrite():
    by=defaultdict(list)
    for r in CHANGES: by[r["s"]].append(r)
    with zipfile.ZipFile(EPUB) as zin:
        infos=zin.infolist(); original={i.filename:zin.read(i.filename) for i in infos}
    edited=dict(original); expected=[]
    with zipfile.ZipFile(EPUB) as z:
        for slug,rs in by.items():
            member=base.find_book_member(z,slug); expected.append(member); text=edited[member].decode()
            for r in rs: text=replace_one_verse(text,slug,r["ch"],r["v"],r["b"],r["a"])
            edited[member]=text.encode()
    fd,name=tempfile.mkstemp(prefix="way-divine-",suffix=".epub",dir=EPUB.parent); os.close(fd); tmp=Path(name)
    try:
        with zipfile.ZipFile(tmp,"w") as out:
            for i in infos: out.writestr(i,edited[i.filename],compress_type=i.compress_type)
        base.validate_epub(tmp); shutil.move(tmp,EPUB)
    finally:
        if tmp.exists(): tmp.unlink()
    actual=sorted(n for n in original if original[n]!=edited[n])
    if actual!=sorted(expected): raise RuntimeError(f"changed EPUB members mismatch expected={sorted(expected)} actual={actual}")
    return actual

def main():
    if base.sha256(EPUB)!=BASE_SHA: raise SystemExit(f"baseline SHA mismatch expected={BASE_SHA} got={base.sha256(EPUB)}")
    pre_articles,pre_ex=grammar.audit_epub(EPUB)
    if pre_articles: raise RuntimeError("pre-release article audit not clean: "+json.dumps(pre_articles[:20],ensure_ascii=False))
    for r in CHANGES:
        if re.search(r" {2,}|\s+[,.!?;:]",r["a"]) or "\n" in r["a"] or "\r" in r["a"]: raise RuntimeError(f"approved-final whitespace issue: {r['r']}")
    exact(EPUB,False)
    before=collect(EPUB,True)
    if len(before)!=31102: raise RuntimeError(f"baseline verse count {len(before)} != 31102")
    now=datetime.now(timezone.utc); stamp=now.strftime("%Y-%m-%d_%H%M%SUTC"); generated=now.replace(microsecond=0).isoformat().replace("+00:00","Z")
    archive_dir=ROOT/"rendered-documents-history"/stamp; archive_dir.mkdir(parents=True,exist_ok=False); archive=archive_dir/EPUB.name; shutil.copy2(EPUB,archive)
    if base.sha256(archive)!=BASE_SHA: raise RuntimeError("archive SHA mismatch")
    changed_members=rewrite(); released=base.sha256(EPUB); exact(EPUB,True)
    post_articles,post_ex=grammar.audit_epub(EPUB)
    if post_articles: raise RuntimeError("post-release article audit not clean: "+json.dumps(post_articles[:20],ensure_ascii=False))
    if len(pre_ex)!=len(post_ex): raise RuntimeError("article exception inventory changed")
    after=collect(EPUB,True)
    if len(after)!=31102: raise RuntimeError(f"released verse count {len(after)} != 31102")
    diffs={k for k in before if before[k]!=after[k]}
    if diffs!=CHANGE_KEYS: raise RuntimeError(f"whole-Bible diff mismatch extra={sorted(diffs-CHANGE_KEYS)[:20]} missing={sorted(CHANGE_KEYS-diffs)[:20]}")
    reg=json.loads(REGISTRY.read_text())
    if reg.get("canonicalEpubSha256")!=BASE_SHA: raise RuntimeError("registry baseline SHA mismatch")
    reg["canonicalEpubSha256"]=released; REGISTRY.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+"\n")
    fallback=base.build_fallback(EPUB,reg,released,generated)
    for k,v in [("bookCount",66),("chapterCount",1189),("verseSearchCount",31102)]:
        if fallback.get(k)!=v: raise RuntimeError(f"fallback {k}={fallback.get(k)} != {v}")
    report={
      "release":"Divine language final release — Sovereign / reign / divine-pronoun consistency","releaseDate":"2026-09-29",
      "authority":{"googleDocumentId":DOC_ID,"googleRevisionId":DOC_REV,"authorityPayloadSha256":PAYLOAD_SHA,"auditRows":177,"releaseChanges":176,"auditedNoChange":["Psalms 45:6"]},
      "baseline":{"canonicalCommit":BASE_COMMIT,"canonicalEpubSha256":BASE_SHA},"releasedEpubSha256":released,
      "archivePath":archive.relative_to(ROOT).as_posix(),"categoryCounts":dict(CATEGORY_COUNTS),"changedBookCount":len(CHANGED_SLUGS),"changedVerseCount":176,
      "wholeBibleVerseCount":len(after),"changedEpubMembers":changed_members,"canonicalMobileFallback":fallback,
      "qa":{"exactBeforeAuthorityMatch":True,"exactAfterAuthorityMatch":True,"epubStructureXmlAndLinks":"pass","wholeBibleDiffExactlyApproved176":True,"articleMismatchCount":len(post_articles),"verseInventory":"31102/31102","bookInventory":66,"chapterInventory":1189,"psalm45_6Unchanged":True},
      "rows":[{"reference":r["r"],"category":r["c"],"disposition":"CHANGE" if r["b"]!=r["a"] else "NO CHANGE","before":r["b"],"after":r["a"]} for r in ROWS]
    }
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    NOTE.write_text(f"""# Divine-language final release — 2026-09-29

Canonical release completed from the frozen Google final-review authority.

- 177 rows revalidated; 176 exact verse changes across 37 books.
- 124 divine-pronoun edits; 40 divine `King` → `Sovereign`; 11 active divine-rule `kingdom` → `reign`; Daniel 7:27 source/collective correction.
- Psalm 45:6 remains unchanged.
- Scope-corrected rows applied exactly: 1 Samuel 6:5, Daniel 2:44, Zechariah 2:13, Romans 1:21.
- No unrelated Scripture modernization or cleanup.
- Baseline commit: `{BASE_COMMIT}`
- Baseline EPUB SHA-256: `{BASE_SHA}`
- Released EPUB SHA-256: `{released}`
- Prior EPUB archive: `{archive.relative_to(ROOT).as_posix()}`
- Exact before/after reconstruction: pass.
- Whole-Bible changed-verse boundary: exactly the approved 176.
- 31,102 / 31,102 verses; 66 books / 1,189 chapters.
- ZIP/XML/internal-link validation: pass.
- English article audit: 0 actionable mismatches.
- Canonical mobile fallback regenerated from the finished EPUB.
- Google authority document: `{DOC_ID}`, revision `{DOC_REV}`; embedded authority payload SHA-256 `{PAYLOAD_SHA}`.

Downstream web/mobile Scripture must be regenerated from this exact canonical release, never hand-edited.
""")
    base.append_once(HISTORY_LOG,released,f"- **{stamp}** — Divine-language final release: 176 exact changed verses across 37 books; prior EPUB archived at `{archive.relative_to(ROOT).as_posix()}`; new SHA-256 `{released}`.")
    base.append_once(REFRESH,"## 2026-09-29 Divine-language final release",f"""## 2026-09-29 Divine-language final release

Finite 176-verse release from the frozen final review: 124 divine-pronoun edits, 40 divine `King` → `Sovereign`, 11 active divine-rule `kingdom` → `reign`, and Daniel 7:27's source/collective correction. Psalm 45:6 remains unchanged. No unrelated Scripture cleanup. Canonical SHA-256: `{released}`. See `../editor-notes/consistency/2026-09-29-divine-language-release.md` and `../change-logs/reports/2026-09-29-divine-language-release.json`.""")
    base.replace_sha_in_file(ROOT_README,BASE_SHA,released); base.replace_sha_in_file(CURRENT_README,BASE_SHA,released)
    print(json.dumps({"releasedEpubSha256":released,"archivePath":archive.relative_to(ROOT).as_posix(),"changedVerseCount":176,"changedBookCount":len(CHANGED_SLUGS),"authorityPayloadSha256":PAYLOAD_SHA,"mobileFallback":fallback},ensure_ascii=False,indent=2))
if __name__=="__main__": main()
