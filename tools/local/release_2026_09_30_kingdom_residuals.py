#!/usr/bin/env python3
from __future__ import annotations

import json, os, re, shutil, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path

import release_2026_09_26_evil_to_brokenness_direct as prev

base=prev.base
grammar=prev.grammar
replace_one_verse=prev.replace_one_verse
collect_verses=prev.collect_verses
ROOT=prev.ROOT
EPUB=prev.EPUB
REGISTRY=prev.REGISTRY
ROOT_README=prev.ROOT_README
CURRENT_README=prev.CURRENT_README
HISTORY_LOG=prev.HISTORY_LOG
REFRESH=prev.REFRESH
ALL_SLUGS=prev.ALL_SLUGS
SLUG_TO_BOOK=prev.SLUG_TO_BOOK

BASELINE='aec31f9c9248cd42913c561c4cd5155fb35c39dddc657b16e53c370edff7a615'
RELEASE_NAME='Daniel 7 kingdom residual → reign correction'
REPORT=ROOT/'change-logs/reports/2026-09-30-kingdom-residual-release.json'
NOTE=ROOT/'editor-notes/consistency/2026-09-30-kingdom-residual-release.md'
KINGDOM_RE=re.compile(r'\bkingdoms?\b',re.I)

CHANGES=[
 ('daniel',7,18,'Daniel 7:18',
  'But the saints of the Most High shall receive the kingdom, and possess the kingdom forever, even forever and ever.',
  'But the saints of the Most High shall receive the reign, and possess the reign forever, even forever and ever.'),
 ('daniel',7,22,'Daniel 7:22',
  'until the ancient of days came, and judgment was given to the saints of the Most High, and the time came that the saints possessed the kingdom.',
  'until the ancient of days came, and judgment was given to the saints of the Most High, and the time came that the saints possessed the reign.'),
 ('daniel',7,27,'Daniel 7:27',
  'The kingdom and the dominion, and the greatness of the kingdoms under the whole sky, shall be given to the people of the saints of the Most High: their kingdom is an everlasting kingdom, and all dominions shall serve and obey them.',
  'The reign and the dominion, and the greatness of the kingdoms under the whole sky, shall be given to the people of the saints of the Most High: their reign is an everlasting reign, and all dominions shall serve and obey them.'),
]

def collect(path:Path): return collect_verses(path,slugs=ALL_SLUGS)

def validate_exact(path:Path,which:str):
    verses=collect_verses(path,slugs=('daniel',))
    errors=[]
    for slug,ch,vs,ref,before,after in CHANGES:
        expected=before if which=='before' else after
        actual=verses.get((slug,ch,vs))
        if actual!=expected: errors.append({'reference':ref,'expected':expected,'actual':actual})
    if errors: raise RuntimeError(f'{which} exact mismatch: '+json.dumps(errors,ensure_ascii=False,indent=2))

def rewrite_epub():
    with zipfile.ZipFile(EPUB,'r') as zin:
        infos=zin.infolist(); original={i.filename:zin.read(i.filename) for i in infos}
        member=base.find_book_member(zin,'daniel')
    edited=dict(original)
    text=edited[member].decode('utf-8')
    for slug,ch,vs,ref,before,after in CHANGES:
        text=replace_one_verse(text,slug,ch,vs,before,after)
    edited[member]=text.encode('utf-8')
    fd,tmpname=tempfile.mkstemp(prefix='the-way-kingdom-residual-',suffix='.epub',dir=EPUB.parent); os.close(fd)
    tmp=Path(tmpname)
    try:
        with zipfile.ZipFile(tmp,'w') as zout:
            for info in infos: zout.writestr(info,edited[info.filename],compress_type=info.compress_type)
        base.validate_epub(tmp)
        shutil.move(tmp,EPUB)
    finally:
        if tmp.exists(): tmp.unlink()
    changed=[name for name in original if original[name]!=edited[name]]
    if changed!=[member]: raise RuntimeError(f'EPUB member diff not Daniel-only: {changed}')
    return member

def kingdom_inventory(verses):
    rows=[]; tokens=0
    for (slug,ch,vs),text in verses.items():
        forms=KINGDOM_RE.findall(text)
        if forms:
            rows.append((slug,ch,vs,text)); tokens+=len(forms)
    return rows,tokens

def main():
    if base.sha256(EPUB)!=BASELINE: raise SystemExit(f'baseline SHA mismatch expected={BASELINE} got={base.sha256(EPUB)}')
    pre_articles,pre_exceptions=grammar.audit_epub(EPUB)
    if pre_articles: raise RuntimeError('baseline article QA not clean')
    validate_exact(EPUB,'before')
    before=collect(EPUB)
    if len(before)!=31102: raise RuntimeError(f'baseline verse count {len(before)} != 31102')
    pre_rows,pre_tokens=kingdom_inventory(before)
    if (len(pre_rows),pre_tokens)!=(205,221): raise RuntimeError(f'baseline kingdom inventory mismatch verses={len(pre_rows)} tokens={pre_tokens}')

    now=datetime.now(timezone.utc); stamp=now.strftime('%Y-%m-%d_%H%MUTC'); generated=now.replace(microsecond=0).isoformat().replace('+00:00','Z')
    archive_dir=ROOT/'rendered-documents-history'/stamp; archive_dir.mkdir(parents=True,exist_ok=False)
    archive=archive_dir/EPUB.name; shutil.copy2(EPUB,archive)
    if base.sha256(archive)!=BASELINE: raise RuntimeError('archive SHA mismatch')

    changed_member=rewrite_epub(); newsha=base.sha256(EPUB)
    if newsha==BASELINE: raise RuntimeError('EPUB hash did not change')
    validate_exact(EPUB,'after')
    post_articles,post_exceptions=grammar.audit_epub(EPUB)
    if post_articles: raise RuntimeError('article mismatches introduced: '+json.dumps(post_articles[:20],ensure_ascii=False))
    if len(post_exceptions)!=len(pre_exceptions): raise RuntimeError('article exception inventory changed')
    after=collect(EPUB)
    if len(after)!=31102: raise RuntimeError(f'post-release verse count {len(after)} != 31102')
    diffs=[(k,before[k],after[k]) for k in before if before[k]!=after[k]]
    expected_keys={(slug,ch,vs) for slug,ch,vs,*_ in CHANGES}
    if {k for k,_,_ in diffs}!=expected_keys or len(diffs)!=3:
        raise RuntimeError('whole-Bible diff is not exactly the approved 3 verses: '+json.dumps([(SLUG_TO_BOOK[k[0]],k[1],k[2]) for k,_,_ in diffs],ensure_ascii=False))
    post_rows,post_tokens=kingdom_inventory(after)
    if (len(post_rows),post_tokens)!=(203,215): raise RuntimeError(f'post kingdom inventory mismatch verses={len(post_rows)} tokens={post_tokens}')

    retained={
      ('numbers',32,33):('kingdom','kingdom'),
      ('daniel',5,21):('kingdom',),
      ('daniel',7,23):('kingdom','kingdoms'),
      ('daniel',7,24):('kingdom',),
      ('daniel',7,27):('kingdoms',),
      ('psalms',45,6):('kingdom',),
    }
    for key,forms in retained.items():
        text=after[key]; found=tuple(x.lower() for x in KINGDOM_RE.findall(text))
        if found!=forms: raise RuntimeError(f'retained kingdom checkpoint failed {key}: {found} != {forms}')

    registry=json.loads(REGISTRY.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256')!=BASELINE: raise RuntimeError('registry baseline SHA mismatch')
    registry['canonicalEpubSha256']=newsha
    REGISTRY.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fallback=base.build_fallback(EPUB,registry,newsha,generated)
    for key,expected in [('bookCount',66),('chapterCount',1189),('verseSearchCount',31102)]:
        if fallback.get(key)!=expected: raise RuntimeError(f'fallback {key} mismatch: {fallback.get(key)}')

    report={
      'release':RELEASE_NAME,'releaseDate':'2026-09-30','priorEpubSha256':BASELINE,'releasedEpubSha256':newsha,
      'archivePath':archive.relative_to(ROOT).as_posix(),'changedVerseCount':3,'wholeBibleVerseCount':31102,
      'changedEpubMembers':[changed_member],'beforeKingdomVerseCount':205,'beforeKingdomTokenCount':221,
      'afterKingdomVerseCount':203,'afterKingdomTokenCount':215,
      'changes':[{'reference':ref,'before':b,'after':a} for _s,_c,_v,ref,b,a in CHANGES],
      'retainedKingdomCheckpoints':['Numbers 32:33','Daniel 5:21','Daniel 7:23','Daniel 7:24','Daniel 7:27 plural kingdoms under the whole sky','Psalms 45:6'],
      'qa':{'exactBeforeMatch':True,'exactAfterMatch':True,'wholeBibleDiffExactlyApproved3':True,'epubStructureXmlAndLinks':'pass','articleMismatchCount':0,'verseInventory':'31102/31102'},
      'canonicalMobileFallback':fallback,
      'method':'Context-first kingdom residual correction. Only Daniel 7:18, 7:22, and the three singular kingdom occurrences in Daniel 7:27 change to reign. Human/geopolitical kingdom language, including Daniel 7:23-24 and the plural kingdoms under the whole sky in Daniel 7:27, is retained.'
    }
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    NOTE.parent.mkdir(parents=True,exist_ok=True); NOTE.write_text(f'''# {RELEASE_NAME}\n\nUser-authorized follow-up to the 2026-09-29 divine-language release.\n\n- Changed exactly Daniel 7:18, Daniel 7:22, and Daniel 7:27.\n- Daniel 7:18: two `kingdom` → `reign`.\n- Daniel 7:22: one `kingdom` → `reign`.\n- Daniel 7:27: three singular `kingdom` → `reign`; plural `kingdoms under the whole sky` retained as geopolitical.\n- Whole-Bible residual audit: 205 verses / 221 kingdom tokens before; 203 verses / 215 tokens after.\n- Human/geopolitical residuals intentionally retained.\n- Prior EPUB SHA-256: `{BASELINE}`\n- New EPUB SHA-256: `{newsha}`\n- Previous EPUB archived at `{archive.relative_to(ROOT).as_posix()}`\n- EPUB ZIP/XML/internal-link validation: pass\n- Whole-Bible inventory: 31,102 / 31,102 verses\n- Exact whole-Bible diff: 3 / 3 approved verses\n\nWebsite, downloadable EPUB, search data, and mobile content must be regenerated from this exact finished canonical EPUB.\n''',encoding='utf-8')
    base.append_once(HISTORY_LOG,newsha,f'- **{stamp}** — {RELEASE_NAME}: exact Daniel 7:18, 7:22, 7:27 correction. Prior EPUB archived at `{archive.relative_to(ROOT).as_posix()}`; new SHA-256 `{newsha}`.')
    base.append_once(REFRESH,'## 2026-09-30 Daniel 7 kingdom residual → reign correction',f'''## 2026-09-30 Daniel 7 kingdom residual → reign correction\n\nExact three-verse follow-up after a fresh whole-Bible `kingdom/kingdoms` residual audit. Daniel 7:18, 7:22, and the singular rule/authority terms in 7:27 use `reign`; human/geopolitical kingdoms remain `kingdom`, including Daniel 7:23-24 and `kingdoms under the whole sky` in 7:27. Canonical SHA-256: `{newsha}`. See `../editor-notes/consistency/2026-09-30-kingdom-residual-release.md` and `../change-logs/reports/2026-09-30-kingdom-residual-release.json`.''')
    base.replace_sha_in_file(ROOT_README,BASELINE,newsha); base.replace_sha_in_file(CURRENT_README,BASELINE,newsha)
    print(json.dumps({'releasedEpubSha256':newsha,'changedVerseCount':3,'kingdomResidualVerses':len(post_rows),'kingdomResidualTokens':post_tokens,'mobileFallback':fallback},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
