#!/usr/bin/env python3
from __future__ import annotations

import hashlib, html, json, os, posixpath, re, shutil, sys, tempfile, urllib.parse, zipfile
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / 'current-form-documents' / 'the-way-current.epub'
LEDGER = ROOT / 'change-logs' / 'reports' / '2026-09-11-original-name-consistency.json'
CURRENT_README = ROOT / 'current-form-documents' / 'README.md'
ROOT_README = ROOT / 'README.md'
HISTORY_LOG = ROOT / 'rendered-documents-history' / 'LOG.md'
NOTE = ROOT / 'editor-notes' / 'consistency' / '2026-09-11-original-name-consistency.md'
BASELINE = '71a0b125ed27706bd4318d075d53e249388ed5a36fdc5f0a2d754a8e0ea1ada5'


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def visible(inner: str) -> str:
    return html.unescape(re.sub(r'<[^>]+>', '', inner)).replace('\u00a0',' ').strip()

def replace_one(member_text: str, verse_no: str, before: str, after: str):
    # The canonical EPUB serializes XHTML with an html: namespace prefix.
    pat=re.compile(r'(<(?:[A-Za-z_][\w.-]*:)?p\b[^>]*>)(.*?)(</(?:[A-Za-z_][\w.-]*:)?p>)', re.I|re.S)
    matches=[]
    for m in pat.finditer(member_text):
        text=visible(m.group(2))
        if text in (f'{verse_no}. {before}', f'{verse_no}.{before}'):
            matches.append(m)
    if not matches: return member_text,0
    if len(matches)!=1: raise RuntimeError(f'multiple paragraph matches in one member for verse {verse_no}: {before[:50]}')
    m=matches[0]
    if re.search(r'<[^>]+>', m.group(2)):
        raise RuntimeError(f'inline markup in target paragraph; refusing rewrite: {before[:80]}')
    rendered=html.escape(f'{verse_no}. {after}', quote=False)
    return member_text[:m.start(2)] + rendered + member_text[m.end(2):], 1

def main():
    if sha256(EPUB)!=BASELINE:
        raise SystemExit(f'baseline SHA mismatch: expected {BASELINE}, got {sha256(EPUB)}')
    ledger=json.loads(LEDGER.read_text(encoding='utf-8'))
    changes=ledger['changes']
    if len(changes)!=39 or ledger.get('change_count')!=39:
        raise SystemExit(f'ledger count must be 39, got {len(changes)}')

    stamp=datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%MUTC')
    archive_dir=ROOT/'rendered-documents-history'/stamp
    archive_dir.mkdir(parents=True, exist_ok=False)
    archive=archive_dir/'the-way-current.epub'
    shutil.copy2(EPUB, archive)
    if sha256(archive)!=BASELINE: raise SystemExit('archive SHA mismatch')

    with zipfile.ZipFile(EPUB,'r') as zin:
        infos=zin.infolist()
        original={i.filename:zin.read(i.filename) for i in infos}
    edited=dict(original)
    applied=[]
    changed_members=set()
    for change in changes:
        ref=change['reference']; verse_no=ref.rsplit(':',1)[1]
        found=[]
        for name,data in list(edited.items()):
            if not name.lower().endswith(('.xhtml','.html','.htm')): continue
            try: text=data.decode('utf-8')
            except UnicodeDecodeError: continue
            new_text,count=replace_one(text,verse_no,change['before'],change['after'])
            if count:
                found.append(name); edited[name]=new_text.encode('utf-8'); changed_members.add(name)
        if len(found)!=1:
            raise RuntimeError(f'{ref}: expected exactly one EPUB paragraph match, got {found}')
        applied.append({'reference':ref,'member':found[0]})

    corpus='\n'.join(visible(d.decode('utf-8','ignore')) for n,d in edited.items() if n.lower().endswith(('.xhtml','.html','.htm')))
    for c in changes:
        if c['after'] not in corpus: raise RuntimeError(f"after text absent: {c['reference']}")
    preserved=[
        'Mahlah, and Noah, Hoglah, Milcah, and Tirzah',
        'Mahlah, Noah, and Hoglah, and Milcah, and Tirzah',
        'Abel Meholah','Abel Beth Maacah','Abel Shittim','Abel Mizraim','Tubal Cain','Seth'
    ]
    for token in preserved:
        if token not in corpus: raise RuntimeError(f'preserved collision missing: {token}')

    fd,tmpname=tempfile.mkstemp(suffix='.epub',dir=str(EPUB.parent)); os.close(fd); tmp=Path(tmpname)
    try:
        with zipfile.ZipFile(tmp,'w') as zout:
            for info in infos:
                data=edited[info.filename]
                zout.writestr(info,data,compress_type=info.compress_type)
        with zipfile.ZipFile(tmp,'r') as z:
            if z.testzip() is not None: raise RuntimeError('ZIP CRC failure')
            first=z.infolist()[0]
            if first.filename!='mimetype' or first.compress_type!=zipfile.ZIP_STORED: raise RuntimeError('EPUB mimetype rule failed')
            if z.read('mimetype')!=b'application/epub+zip': raise RuntimeError('EPUB mimetype content failed')
            names=set(z.namelist())
            ids={}
            book_members=[]; chapter_count=0
            for name in z.namelist():
                if name.lower().endswith(('.xhtml','.html','.htm','.opf','.ncx','.xml')):
                    raw=z.read(name)
                    ET.fromstring(raw)
                    text=raw.decode('utf-8','ignore')
                    ids[name]=set(re.findall(r'\bid=["\']([^"\']+)',text))
                    cc=len(re.findall(r'\bid=["\']ch-',text))
                    if cc: book_members.append(name); chapter_count += cc
                    if '<<' in text or '>>' in text: raise RuntimeError(f'angle-marker artifact in {name}')
            if len(book_members)!=66: raise RuntimeError(f'expected 66 book XHTML members, got {len(book_members)}')
            if chapter_count!=1189: raise RuntimeError(f'expected 1189 chapter anchors, got {chapter_count}')
            unresolved=[]
            for src in ids:
                text=z.read(src).decode('utf-8','ignore')
                for href in re.findall(r'\bhref=["\']([^"\']+)',text):
                    if not href or href.startswith(('http:','https:','mailto:','data:','javascript:')): continue
                    path,sep,frag=href.partition('#')
                    target=src if not path else posixpath.normpath(posixpath.join(posixpath.dirname(src),urllib.parse.unquote(path)))
                    if target not in names: unresolved.append((src,href,'missing member')); continue
                    if sep and frag and target in ids and urllib.parse.unquote(frag) not in ids[target]: unresolved.append((src,href,'missing fragment'))
            if unresolved: raise RuntimeError(f'unresolved internal links: {unresolved[:10]}')
        shutil.move(tmp,EPUB)
    finally:
        if tmp.exists(): tmp.unlink()

    newsha=sha256(EPUB)
    if newsha==BASELINE: raise RuntimeError('release SHA did not change')
    changed_content=[n for n in original if original[n]!=edited[n]]
    if set(changed_content)!=changed_members: raise RuntimeError('unexpected uncompressed member changes')
    if len(changed_members)!=6: raise RuntimeError(f'expected 6 affected book members, got {len(changed_members)}: {sorted(changed_members)}')

    archive_rel=archive.relative_to(ROOT).as_posix()
    ledger['released_epub_sha256']=newsha
    ledger['archive_path']=archive_rel
    ledger['qa']={
        'applied_changes':len(applied),'affected_book_members':len(changed_members),'book_count':66,'chapter_count':1189,
        'zip_crc':'pass','xml_parse':'pass','internal_links':'pass','angle_markers':'0','preserved_collisions':'pass'
    }
    ledger['applied']=applied
    LEDGER.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    NOTE.parent.mkdir(parents=True,exist_ok=True)
    NOTE.write_text(f'''# Original-name consistency and Genesis narrative wording — 2026-09-11

This release follows editor direction to complete obvious restored-name consistency and improve awkward early-Genesis references to the first man without flattening the Hebrew `adam` / `ha-adam` wordplay everywhere.

## Release

- Canonical source: `current-form-documents/the-way-current.epub`
- Prior SHA-256: `{BASELINE}`
- Current SHA-256: `{newsha}`
- Prior artifact archived at `{archive_rel}`
- Reviewed verse-level edits: **39**
- Affected canonical book files: **6**
- Coverage preserved: **66 books / 1,189 chapters**

## Name consistency

Established restored forms already present elsewhere in this edition were applied to their inconsistent references:

- **Qayin** for the Genesis person traditionally rendered Cain.
- **Hevel** for the Genesis person traditionally rendered Abel.
- **Noach** for the patriarch where four traditional `Noah` references remained.
- **Havvah** for Eve in 1 Timothy 2:13 and 2 Corinthians 11:3.
- **Chanokh** for Enoch where the traditional form remained in Genesis and 1 Chronicles.

This was reference-specific, not a global substitution. **Noah, daughter of Zelophehad, remains Noah.** `Abel` in place names such as Abel Meholah remains unchanged. `Tubal Cain` remains unchanged as a distinct compound name. `Seth` remains Seth because `Shet` is not an established form elsewhere in the current edition.

## Genesis wording

Genesis 2–4 was reviewed separately for `the human`, `the person`, `the man`, and `Adam`. Generic/formation contexts retain **the human** where it carries the Hebrew human/ground relationship; selected personal narrative contexts now use the more natural **the man**, and Genesis 4:1 uses **Adam** once the narrative has identified him personally. No blanket replacement was made.

## QA

The release builder required every ledger `before` value to match exactly once before writing. It then verified the 39 `after` values, preserved collision cases, EPUB ZIP/mimetype integrity, XML parsing, 66 canonical book XHTML members, 1,189 chapter anchors, internal links, and zero current `<<`/`>>` artifacts.

The exact before/after ledger is `change-logs/reports/2026-09-11-original-name-consistency.json`.
''',encoding='utf-8')

    cr=CURRENT_README.read_text(encoding='utf-8')
    cr=cr.replace(BASELINE,newsha)
    cr=re.sub(r'\| Previous release \| Archived under `rendered-documents-history/[^`]+/` \|',f'| Previous release | Archived under `{archive_dir.relative_to(ROOT).as_posix()}/` |',cr)
    cr=re.sub(r'This EPUB contains the completed whole-Bible divine-pronoun consistency update.*?It is suitable for Kindle, Apple Books, tablets, phones, and most EPUB-compatible e-readers\.',
              'This EPUB includes the completed whole-Bible divine-pronoun consistency update and the 2026-09-11 original-name / Genesis narrative consistency update (39 reviewed verse-level edits); see the [latest release notes](../editor-notes/consistency/2026-09-11-original-name-consistency.md). Website and application copies are verified separately when synchronized. It is suitable for Kindle, Apple Books, tablets, phones, and most EPUB-compatible e-readers.',cr,flags=re.S)
    CURRENT_README.write_text(cr,encoding='utf-8')

    rr=ROOT_README.read_text(encoding='utf-8').replace(BASELINE,newsha)
    rr=rr.replace('The latest [consistency notes](editor-notes/consistency/2026-09-10-whole-bible-divine-pronouns.md) document the completed whole-Bible divine-pronoun consistency update.',
                  'The latest [consistency notes](editor-notes/consistency/2026-09-11-original-name-consistency.md) document the original-name consistency and Genesis narrative wording update; the completed whole-Bible divine-pronoun update remains part of this same canonical artifact.')
    ROOT_README.write_text(rr,encoding='utf-8')

    log=HISTORY_LOG.read_text(encoding='utf-8').rstrip()+f'\n| {stamp} | {archive_rel.rsplit("/",1)[0]}/ | the-way-current.epub (SHA-256 `{BASELINE}`) | Archive the prior canonical EPUB before the original-name consistency / Genesis narrative wording release; 39 reviewed verse-level edits. |\n'
    HISTORY_LOG.write_text(log,encoding='utf-8')

    print(json.dumps({'new_sha256':newsha,'archive':archive_rel,'changes':len(applied),'changed_members':sorted(changed_members)},indent=2))

if __name__=='__main__':
    main()
