#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import html
import json
import os
import posixpath
import re
import shutil
import tempfile
import urllib.parse
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / 'current-form-documents' / 'the-way-current.epub'
REGISTRY = ROOT / 'current-form-documents' / 'original-name-registry.json'
SOURCE = ROOT / 'original-documents' / 'john_restorative_translation.txt'
ROOT_README = ROOT / 'README.md'
CURRENT_README = ROOT / 'current-form-documents' / 'README.md'
HISTORY_LOG = ROOT / 'rendered-documents-history' / 'LOG.md'
BOOK_LOG = ROOT / 'change-logs' / 'new-testament' / 'books' / 'John.md'
LEDGER = ROOT / 'change-logs' / 'reports' / '2026-09-13-john-14-6-living-way.json'
NOTE = ROOT / 'editor-notes' / 'consistency' / '2026-09-13-john-14-6-living-way.md'
FALLBACK_DIR = ROOT / 'current-form-documents' / 'mobile-reader'
BASELINE = '85666f0bbc81d21139fadbd9ae5defe42908f3e0e3754e2298980245c8db4833'
REFERENCE = 'John 14:6'
BEFORE = 'Yeshua said to him, "I am the way, the truth, and the life. No one comes to the Cosmic Parent, except through me.'
AFTER = 'Yeshua said to him, "I am the way, the truth, and the life: a path that opens as the human self comes into alignment with the Cosmic Parent. No one comes to the Cosmic Parent except through this living way that I embody.'

BOOKS = [
('old', [('genesis','Genesis'),('exodus','Exodus'),('leviticus','Leviticus'),('numbers','Numbers'),('deuteronomy','Deuteronomy'),('joshua','Joshua'),('judges','Judges'),('ruth','Ruth'),('1-samuel','1 Samuel'),('2-samuel','2 Samuel'),('1-kings','1 Kings'),('2-kings','2 Kings'),('1-chronicles','1 Chronicles'),('2-chronicles','2 Chronicles'),('ezra','Ezra'),('nehemiah','Nehemiah'),('esther','Esther'),('job','Job'),('psalms','Psalms'),('proverbs','Proverbs'),('ecclesiastes','Ecclesiastes'),('song-of-solomon','Song of Solomon'),('isaiah','Isaiah'),('jeremiah','Jeremiah'),('lamentations','Lamentations'),('ezekiel','Ezekiel'),('daniel','Daniel'),('hosea','Hosea'),('joel','Joel'),('amos','Amos'),('obadiah','Obadiah'),('jonah','Jonah'),('micah','Micah'),('nahum','Nahum'),('habakkuk','Habakkuk'),('zephaniah','Zephaniah'),('haggai','Haggai'),('zechariah','Zechariah'),('malachi','Malachi')]),
('new', [('matthew','Matthew'),('mark','Mark'),('luke','Luke'),('john','John'),('acts','Acts'),('romans','Romans'),('1-corinthians','1 Corinthians'),('2-corinthians','2 Corinthians'),('galatians','Galatians'),('ephesians','Ephesians'),('philippians','Philippians'),('colossians','Colossians'),('1-thessalonians','1 Thessalonians'),('2-thessalonians','2 Thessalonians'),('1-timothy','1 Timothy'),('2-timothy','2 Timothy'),('titus','Titus'),('philemon','Philemon'),('hebrews','Hebrews'),('james','James'),('1-peter','1 Peter'),('2-peter','2 Peter'),('1-john','1 John'),('2-john','2 John'),('3-john','3 John'),('jude','Jude'),('revelation','Revelation')])]
BOOK_NAME = {slug:name for _, group in BOOKS for slug,name in group}
TESTAMENT = {slug:testament for testament, group in BOOKS for slug,_ in group}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()


def collapse(value: str) -> str:
    return re.sub(r'\s+',' ',value or '').strip()


def visible(inner: str) -> str:
    return collapse(html.unescape(re.sub(r'<[^>]+>','',inner)).replace('\u00a0',' '))


def local_name(name: str) -> str:
    return name.split('}',1)[-1] if '}' in name else name


def normalized(value: str) -> str:
    return collapse(re.sub(r'[^a-z0-9]+',' ',value.lower()))


def strip_namespaces(root: ET.Element) -> ET.Element:
    root=copy.deepcopy(root)
    for el in root.iter():
        el.tag=local_name(el.tag)
        attrs={local_name(k):v for k,v in el.attrib.items()}
        el.attrib.clear(); el.attrib.update(attrs)
    return root


def element_text(el: ET.Element) -> str:
    return collapse(' '.join(el.itertext()))


def replace_epub_verse(member_text: str) -> tuple[str,int]:
    pat=re.compile(r'(<(?:[A-Za-z_][\w.-]*:)?p\b[^>]*>)(.*?)(</(?:[A-Za-z_][\w.-]*:)?p>)',re.I|re.S)
    found=[]
    for m in pat.finditer(member_text):
        text=visible(m.group(2))
        if text in (f'6. {BEFORE}', f'6.{BEFORE}'):
            found.append(m)
    if len(found)!=1:
        return member_text,len(found)
    m=found[0]
    if re.search(r'<[^>]+>',m.group(2)):
        raise RuntimeError('John 14:6 contains inline markup; refusing automatic release')
    replacement=html.escape(f'6. {AFTER}',quote=False)
    return member_text[:m.start(2)]+replacement+member_text[m.end(2):],1


def validate_epub(path: Path) -> tuple[int,int]:
    with zipfile.ZipFile(path,'r') as z:
        if z.testzip() is not None: raise RuntimeError('EPUB ZIP CRC failed')
        first=z.infolist()[0]
        if first.filename!='mimetype' or first.compress_type!=zipfile.ZIP_STORED: raise RuntimeError('EPUB mimetype placement/compression failed')
        if z.read('mimetype')!=b'application/epub+zip': raise RuntimeError('EPUB mimetype content failed')
        names=set(z.namelist()); ids={}; books=[]; chapters=0
        for name in z.namelist():
            if name.lower().endswith(('.xhtml','.html','.htm','.opf','.ncx','.xml')):
                raw=z.read(name); ET.fromstring(raw)
                text=raw.decode('utf-8','ignore')
                ids[name]=set(re.findall(r'\bid=["\']([^"\']+)',text))
                cc=len(re.findall(r'\bid=["\']ch-',text))
                if cc: books.append(name); chapters+=cc
                if '<<' in text or '>>' in text: raise RuntimeError(f'angle-marker artifact in {name}')
        if len(books)!=66 or chapters!=1189: raise RuntimeError(f'coverage failed: {len(books)} books/{chapters} chapters')
        bad=[]
        for src in ids:
            text=z.read(src).decode('utf-8','ignore')
            for href in re.findall(r'\bhref=["\']([^"\']+)',text):
                if not href or href.startswith(('http:','https:','mailto:','data:','javascript:')): continue
                path_part,sep,frag=href.partition('#')
                target=src if not path_part else posixpath.normpath(posixpath.join(posixpath.dirname(src),urllib.parse.unquote(path_part)))
                if target not in names: bad.append((src,href,'member')); continue
                if sep and frag and target in ids and urllib.parse.unquote(frag) not in ids[target]: bad.append((src,href,'fragment'))
        if bad: raise RuntimeError(f'broken internal links: {bad[:10]}')
        return len(books),chapters


def find_book_member(z: zipfile.ZipFile, slug: str) -> str:
    exact=f'OEBPS/Text/{slug}.xhtml'
    if exact in z.namelist(): return exact
    matches=[n for n in z.namelist() if n.lower().endswith(f'/{slug}.xhtml')]
    if len(matches)!=1: raise RuntimeError(f'cannot locate {slug} XHTML: {matches}')
    return matches[0]


def chapter_number(el: ET.Element, slug: str):
    ident=el.attrib.get('id','')
    m=re.fullmatch(rf'ch-{re.escape(slug)}-(\d+)',ident,re.I)
    return int(m.group(1)) if m else None


def extract_book(raw: bytes, slug: str, name: str):
    root=ET.fromstring(raw)
    parents={child:parent for parent in root.iter() for child in parent}
    anchors=[]
    for el in root.iter():
        n=chapter_number(el,slug)
        if n is not None: anchors.append((n,el))
    anchors.sort(key=lambda x:x[0])
    nums=[n for n,_ in anchors]
    if not nums or nums!=list(range(1,max(nums)+1)): raise RuntimeError(f'chapter anchors invalid for {name}')
    chapters=[]
    for number,el in anchors:
        frag=el
        text=element_text(el)
        if len(text)<80:
            parent=parents.get(el)
            if parent is None: raise RuntimeError(f'no wrapper for {name} {number}')
            siblings=list(parent); start=siblings.index(el); gathered=[]
            for sibling in siblings[start:]:
                if sibling is not el and chapter_number(sibling,slug) is not None: break
                gathered.append(copy.deepcopy(sibling))
            wrapper=ET.Element('section',{'id':f'reader-{slug}-{number}'})
            for sibling in gathered: wrapper.append(sibling)
            frag=wrapper; text=element_text(wrapper)
        clean=strip_namespaces(frag)
        verse_counts=defaultdict(int); verses=[]
        for node in clean.iter():
            if local_name(node.tag).lower()!='p': continue
            plain=element_text(node)
            m=re.match(r'^(\d+)\.\s*(.*)$',plain,re.S)
            if not m: continue
            verse=int(m.group(1)); verse_counts[verse]+=1
            anchor=f'v-{slug}-{number}-{verse}' + (f'-{verse_counts[verse]}' if verse_counts[verse]>1 else '')
            node.attrib['id']=anchor; node.attrib['data-verse']=str(verse)
            verses.append({'number':verse,'anchor':anchor,'text':collapse(m.group(2))})
        if not verses: raise RuntimeError(f'no verses for {name} {number}')
        for parent in list(clean.iter()):
            for child in list(parent):
                if local_name(child.tag).lower() in {'script','style','link'}: parent.remove(child)
        fragment=ET.tostring(clean,encoding='unicode',method='html')
        chapters.append({'number':number,'html':fragment,'text':text,'verses':verses})
    return {'slug':slug,'name':name,'testament':TESTAMENT[slug],'chapters':chapters}


def alias_catalog(registry: dict):
    out=[]
    for e in registry.get('entries',[]):
        term=collapse(str(e.get('term',''))); aliases=[collapse(str(a)) for a in e.get('traditionalAliases',[]) if collapse(str(a))]
        if term and aliases: out.append((term,normalized(term),aliases))
    return out


def verse_aliases(text: str, catalog):
    padded=f' {normalized(text)} '; aliases=set(); terms=set()
    for term,norm,traditional in catalog:
        if f' {norm} ' in padded:
            terms.add(term); aliases.update(traditional)
    return sorted(aliases,key=str.casefold),sorted(terms,key=str.casefold)


def build_fallback(epub: Path, registry: dict, release_sha: str, generated_at: str):
    books={}; search=[]; order=0; catalog=alias_catalog(registry); index_books=[]
    with zipfile.ZipFile(epub,'r') as z:
        for testament,group in BOOKS:
            for slug,name in group:
                member=find_book_member(z,slug)
                book=extract_book(z.read(member),slug,name)
                books[slug]=book
                index_books.append({'slug':slug,'name':name,'testament':testament,'chapterCount':len(book['chapters'])})
                for chapter in book['chapters']:
                    for verse in chapter['verses']:
                        aliases,canonical=verse_aliases(verse['text'],catalog)
                        search_text=normalized(f"{name} {chapter['number']} {verse['number']} {verse['text']}")
                        search.append({'order':order,'testament':testament,'book':name,'slug':slug,'chapter':chapter['number'],'verse':verse['number'],'anchor':verse['anchor'],'text':verse['text'],'searchText':search_text,'aliases':aliases,'aliasText':normalized(' '.join(aliases)),'canonicalTerms':canonical})
                        order+=1
    if len(index_books)!=66 or sum(x['chapterCount'] for x in index_books)!=1189: raise RuntimeError('fallback coverage mismatch')
    if len(search)!=31102: raise RuntimeError(f'fallback verse-search count mismatch: {len(search)}')
    index={'title':'The Way Version','sourceSha256':release_sha,'generatedAt':generated_at,'defaultBook':'genesis','defaultChapter':1,'bookCount':66,'chapterCount':1189,'verseSearchCount':len(search),'searchSchemaVersion':2,'books':index_books}
    bundle={'schemaVersion':1,'releaseId':f'canonical-{release_sha[:16]}','canonicalEpubSha256':release_sha,'generatedAt':generated_at,'index':index,'search':search,'books':books,'originalNameRegistry':registry}
    FALLBACK_DIR.mkdir(parents=True,exist_ok=True)
    content_path=FALLBACK_DIR/'content.json'
    encoded=(json.dumps(bundle,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf-8')
    content_path.write_bytes(encoded)
    content_sha=sha256_bytes(encoded)
    manifest={'schemaVersion':1,'releaseId':bundle['releaseId'],'canonicalEpubSha256':release_sha,'generatedAt':generated_at,'contentSha256':content_sha,'contentBytes':len(encoded),'contentUrl':'https://raw.githubusercontent.com/Wayback-Project/thewaytranslations/main/current-form-documents/mobile-reader/content.json','source':'canonical-github-fallback','bookCount':66,'chapterCount':1189,'verseSearchCount':len(search)}
    (FALLBACK_DIR/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return manifest


def replace_sha_in_file(path: Path, old: str, new: str):
    if not path.exists(): return
    text=path.read_text(encoding='utf-8')
    if old in text:
        path.write_text(text.replace(old,new),encoding='utf-8')


def append_once(path: Path, marker: str, content: str):
    text=path.read_text(encoding='utf-8') if path.exists() else ''
    if marker not in text:
        if text and not text.endswith('\n'): text+='\n'
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(text+'\n'+content.strip()+'\n',encoding='utf-8')


def main():
    actual=sha256(EPUB)
    if actual!=BASELINE: raise SystemExit(f'baseline SHA mismatch: expected {BASELINE}, got {actual}')
    source_text=SOURCE.read_text(encoding='utf-8')
    if source_text.count(BEFORE)!=1: raise RuntimeError(f'expected exactly one John source match, got {source_text.count(BEFORE)}')
    SOURCE.write_text(source_text.replace(BEFORE,AFTER,1),encoding='utf-8')

    stamp=datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%MUTC'); generated=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
    archive_dir=ROOT/'rendered-documents-history'/stamp; archive_dir.mkdir(parents=True,exist_ok=False)
    archive=archive_dir/EPUB.name; shutil.copy2(EPUB,archive)
    if sha256(archive)!=BASELINE: raise RuntimeError('archive SHA mismatch')

    with zipfile.ZipFile(EPUB,'r') as zin:
        infos=zin.infolist(); original={i.filename:zin.read(i.filename) for i in infos}
    edited=dict(original); target='OEBPS/Text/john.xhtml'
    if target not in edited: raise RuntimeError('John XHTML missing')
    text=edited[target].decode('utf-8'); new_text,count=replace_epub_verse(text)
    if count!=1: raise RuntimeError(f'expected one John 14:6 EPUB paragraph, got {count}')
    edited[target]=new_text.encode('utf-8')
    fd,tmpname=tempfile.mkstemp(suffix='.epub',dir=str(EPUB.parent)); os.close(fd); tmp=Path(tmpname)
    try:
        with zipfile.ZipFile(tmp,'w') as zout:
            for info in infos: zout.writestr(info,edited[info.filename],compress_type=info.compress_type)
        validate_epub(tmp); shutil.move(tmp,EPUB)
    finally:
        if tmp.exists(): tmp.unlink()
    changed=[name for name in original if original[name]!=edited[name]]
    if changed!=[target]: raise RuntimeError(f'unexpected EPUB members changed: {changed}')
    newsha=sha256(EPUB)
    if newsha==BASELINE: raise RuntimeError('EPUB SHA did not change')

    registry=json.loads(REGISTRY.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256')!=BASELINE: raise RuntimeError('registry baseline SHA mismatch')
    registry['canonicalEpubSha256']=newsha
    REGISTRY.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fallback=build_fallback(EPUB,registry,newsha,generated)

    report={'release':'2026-09-13 John 14:6 living-way rendering','prior_epub_sha256':BASELINE,'released_epub_sha256':newsha,'archive_path':archive.relative_to(ROOT).as_posix(),'change_count':1,'changes':[{'reference':REFERENCE,'before':BEFORE,'after':AFTER,'reason':'Editor-authorized Way Version rendering of Yeshua’s saying. It keeps the Way/truth/life language while expressing the Way as embodied alignment with the Cosmic Parent; it is an interpretive rendering and not a claim of word-for-word reconstruction.'}],'applied':[{'reference':REFERENCE,'member':target,'source':'original-documents/john_restorative_translation.txt'}],'mobileFallback':fallback,'qa':{'book_count':66,'chapter_count':1189,'zip_crc':'pass','xml_parse':'pass','internal_links':'pass','changed_book_members':[target],'verse_search_records':31102}}
    LEDGER.parent.mkdir(parents=True,exist_ok=True); LEDGER.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    NOTE.parent.mkdir(parents=True,exist_ok=True); NOTE.write_text(f'''# John 14:6 — living-way rendering — 2026-09-13\n\n## Released wording\n\n**Before:** `{BEFORE}`\n\n**Current:** `{AFTER}`\n\nThe quotation continues into John 14:7, so verse 6 intentionally does not acquire a new closing quotation mark.\n\n## Editorial posture\n\nThis is an editor-authorized Way Version interpretive rendering of Yeshua’s saying. It preserves “the way, the truth, and the life” while making the edition’s living-way/alignment reading explicit. Under the project’s Yeshua-sayings convention, Aramaic/Peshitta and Semitic context may inform interpretation, but this expanded English wording is not presented as a recoverable verbatim first-century Aramaic sentence.\n\n## Release\n\n- Previous EPUB SHA-256: `{BASELINE}`\n- Released EPUB SHA-256: `{newsha}`\n- Exact ledger: `change-logs/reports/2026-09-13-john-14-6-living-way.json`\n- Public mobile fallback feed: `current-form-documents/mobile-reader/manifest.json` and `content.json`\n- EPUB QA: 66 books / 1,189 chapters; ZIP, XML, and internal-link validation passed.\n''',encoding='utf-8')

    append_once(BOOK_LOG,'2026-09-13 — John 14:6 living-way rendering',f'''## 2026-09-13 — John 14:6 living-way rendering\n- Scope: John 14:6.\n- Change: `{BEFORE}` → `{AFTER}`\n- Status: editor-authorized canonical release.\n- Exact ledger: `change-logs/reports/2026-09-13-john-14-6-living-way.json`.''')
    append_once(HISTORY_LOG,newsha,f'''- **{stamp}** — John 14:6 living-way rendering released. Prior canonical EPUB archived at `{archive.relative_to(ROOT).as_posix()}`; new SHA-256 `{newsha}`.''')
    replace_sha_in_file(ROOT_README,BASELINE,newsha); replace_sha_in_file(CURRENT_README,BASELINE,newsha)
    append_once(ROOT_README,'### Mobile translation update fallback protocol','''### Mobile translation update fallback protocol\n\nThe canonical EPUB remains the text authority. Each approved canonical release also publishes a generated, read-only mobile fallback feed under `current-form-documents/mobile-reader/`. `manifest.json` identifies the exact canonical EPUB SHA and the SHA-256 of `content.json`; `content.json` contains generated chapter/search data plus the canonical original-name registry. These files are generated from the canonical EPUB and must never be hand-edited.\n\nThe website may publish the same canonical release in a richer primary mobile feed, but a mobile client must corroborate a new website release against this public canonical GitHub manifest before activating it. If the website is unavailable, an emergency website switch directs clients away from the website, or the website release cannot be corroborated, clients fall back to this GitHub feed. A previously verified downloaded release and the immutable Bible bundled with the app remain valid offline fallbacks.''')
    print(json.dumps({'releasedEpubSha256':newsha,'fallbackContentSha256':fallback['contentSha256'],'fallbackBytes':fallback['contentBytes']},indent=2))

if __name__=='__main__': main()
