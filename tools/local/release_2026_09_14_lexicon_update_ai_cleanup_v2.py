#!/usr/bin/env python3
from __future__ import annotations

import copy
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import release_2026_09_14_lexicon_update_ai_cleanup as release

EXPECTED_CHAPTERS={
'genesis':50,'exodus':40,'leviticus':27,'numbers':36,'deuteronomy':34,'joshua':24,'judges':21,'ruth':4,'1-samuel':31,'2-samuel':24,'1-kings':22,'2-kings':25,'1-chronicles':29,'2-chronicles':36,'ezra':10,'nehemiah':13,'esther':10,'job':42,'psalms':150,'proverbs':31,'ecclesiastes':12,'song-of-solomon':8,'isaiah':66,'jeremiah':52,'lamentations':5,'ezekiel':48,'daniel':12,'hosea':14,'joel':3,'amos':9,'obadiah':1,'jonah':4,'micah':7,'nahum':3,'habakkuk':3,'zephaniah':3,'haggai':2,'zechariah':14,'malachi':4}

def collapse(value: str) -> str:
    return re.sub(r'\s+',' ',value or '').strip()

def local_name(name: str) -> str:
    return name.split('}',1)[-1] if '}' in name else name

def element_text(el: ET.Element) -> str:
    return collapse(' '.join(el.itertext()))

def strip_namespaces(root: ET.Element) -> ET.Element:
    root=copy.deepcopy(root)
    for el in root.iter():
        el.tag=local_name(el.tag)
        attrs={local_name(k):v for k,v in el.attrib.items()}
        el.attrib.clear(); el.attrib.update(attrs)
    return root

def chapter_number(el: ET.Element, slug: str):
    m=re.fullmatch(rf'ch-{re.escape(slug)}-(\d+)',el.attrib.get('id',''),re.I)
    return int(m.group(1)) if m else None

def extract_book(raw: bytes, slug: str):
    root=ET.fromstring(raw)
    parents={child:parent for parent in root.iter() for child in parent}
    anchors=[]
    for el in root.iter():
        n=chapter_number(el,slug)
        if n is not None: anchors.append((n,el))
    anchors.sort(key=lambda x:x[0])
    nums=[n for n,_ in anchors]
    expected=list(range(1,EXPECTED_CHAPTERS[slug]+1))
    if nums != expected:
        raise RuntimeError(f'chapter anchors invalid for {slug}: expected {expected}, got {nums}')
    out={}
    for ch,el in anchors:
        frag=el
        if len(element_text(el)) < 80:
            parent=parents.get(el)
            if parent is None: raise RuntimeError(f'no wrapper for {slug} {ch}')
            siblings=list(parent); start=siblings.index(el); gathered=[]
            for sibling in siblings[start:]:
                if sibling is not el and chapter_number(sibling,slug) is not None: break
                gathered.append(copy.deepcopy(sibling))
            wrapper=ET.Element('section')
            for sibling in gathered: wrapper.append(sibling)
            frag=wrapper
        clean=strip_namespaces(frag); seen=set(); found=0
        for node in clean.iter():
            if local_name(node.tag).lower()!='p': continue
            plain=element_text(node); m=re.match(r'^(\d+)\.\s*(.*)$',plain,re.S)
            if not m: continue
            vs=int(m.group(1))
            if vs in seen: continue
            seen.add(vs); found+=1
            out[(slug,ch,vs)]=collapse(m.group(2))
        if not found: raise RuntimeError(f'no verses for {slug} {ch}')
    return out

def wrapper_aware_collect(path: Path, *, all_ot=False):
    slugs=release.OT_SLUGS if all_ot else release.CHANGED_SLUGS
    out={}
    with zipfile.ZipFile(path) as z:
        bad=z.testzip()
        if bad: raise RuntimeError(f'EPUB CRC failure: {bad}')
        for slug in slugs:
            member=release.base.find_book_member(z,slug)
            book_map=extract_book(z.read(member),slug)
            overlap=set(out).intersection(book_map)
            if overlap: raise RuntimeError(f'duplicate extracted references: {sorted(overlap)[:10]}')
            out.update(book_map)
    if all_ot and len(out)!=23145:
        raise RuntimeError(f'OT verse inventory mismatch: {len(out)} != 23145')
    return out

release.collect=wrapper_aware_collect

if __name__=='__main__':
    release.main()
