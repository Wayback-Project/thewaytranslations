#!/usr/bin/env python3
from __future__ import annotations

import copy
import csv
import hashlib
import html
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / 'current-form-documents' / 'the-way-current.epub'
OUT = ROOT / 'audit-output' / 'old-testament-gender-brokenness-2026-09-14'
EXPECTED_SHA = '0e66242a07b5303337f90078ae8639a1fca264031b63962fb109f79033e48c30'
EXPECTED_OT_VERSES = 23145

BOOKS = {
'genesis':'Genesis','exodus':'Exodus','leviticus':'Leviticus','numbers':'Numbers','deuteronomy':'Deuteronomy','joshua':'Joshua','judges':'Judges','ruth':'Ruth','1-samuel':'1 Samuel','2-samuel':'2 Samuel','1-kings':'1 Kings','2-kings':'2 Kings','1-chronicles':'1 Chronicles','2-chronicles':'2 Chronicles','ezra':'Ezra','nehemiah':'Nehemiah','esther':'Esther','job':'Job','psalms':'Psalms','proverbs':'Proverbs','ecclesiastes':'Ecclesiastes','song-of-solomon':'Song of Solomon','isaiah':'Isaiah','jeremiah':'Jeremiah','lamentations':'Lamentations','ezekiel':'Ezekiel','daniel':'Daniel','hosea':'Hosea','joel':'Joel','amos':'Amos','obadiah':'Obadiah','jonah':'Jonah','micah':'Micah','nahum':'Nahum','habakkuk':'Habakkuk','zephaniah':'Zephaniah','haggai':'Haggai','zechariah':'Zechariah','malachi':'Malachi'}
EXPECTED_CHAPTERS = {
'genesis':50,'exodus':40,'leviticus':27,'numbers':36,'deuteronomy':34,'joshua':24,'judges':21,'ruth':4,'1-samuel':31,'2-samuel':24,'1-kings':22,'2-kings':25,'1-chronicles':29,'2-chronicles':36,'ezra':10,'nehemiah':13,'esther':10,'job':42,'psalms':150,'proverbs':31,'ecclesiastes':12,'song-of-solomon':8,'isaiah':66,'jeremiah':52,'lamentations':5,'ezekiel':48,'daniel':12,'hosea':14,'joel':3,'amos':9,'obadiah':1,'jonah':4,'micah':7,'nahum':3,'habakkuk':3,'zephaniah':3,'haggai':2,'zechariah':14,'malachi':4}
HANDLED = {'Psalms','Proverbs','Ecclesiastes','Isaiah'}

DIV = r'(?:YHWH|Elohim|God|El Shaddai|Elyon|Yah|Most High|Almighty|Creator)'
PRON = r'(?:he|him|his|himself)'
DIV_RE = re.compile(rf'\b{DIV}\b')
PRON_RE = re.compile(rf'\b{PRON}\b', re.I)
HUMAN_DISTRACTOR = re.compile(r'\b(?:angel|prophet|priest|king|Pharaoh|Moshe|Aharon|Dawid|Shlomo|Shaul|Yonah|Yehoshua|Gid.on|Job|man|woman|person|child|father|mother|brother|sister|servant|people|enemy|neighbor|ruler|one\s+who)\b', re.I)
DEVOTION = re.compile(r'\b(?:serve|serves|served|seek|seeks|sought|follow|follows|followed|revere|reveres|revered|fear|fears|feared|worship|worships|worshiped|trust|trusts|trusted|wait|waits|waited|call on|calls on|called on|pray to|prays to|prayed to|praise|praises|praised|exalt|exalts|exalted|obey|obeys|obeyed|return to|returns to|returned to|inquire of|inquired of)\s+(?:only\s+)?(?P<p>him|his|himself)\b', re.I)
ATTR = re.compile(r'\b(?P<p>his)\s+(?:anger|wrath|mercy|grace|name|glory|power|hand|eyes|commandments|commandment|statutes|ordinances|covenant|word|voice|spirit|Ruach|blessings|counsel|thoughts|temple|sanctuary|people|servants|prophets|army|flock|land|house|works|law|laws|gift|jealousy|place)\b', re.I)
SUBJECT_AFTER = re.compile(rf'\b(?P<d>{DIV})\b(?P<mid>[^.!?]{{0,110}}?)(?:;|,|\band\b|\bfor\b|\bbecause\b|\bwho\b|\bthat\b)\s*(?P<p>he|his|himself)\b', re.I)
SENTENCE_AFTER = re.compile(rf'\b(?P<d>{DIV})\b(?P<mid>[^.!?]{{0,140}}?)[.!?]\s*[\"“‘\']*(?P<p>He|His|Himself)\b')

BROKENNESS = re.compile(r'\bbrokenness\b|\bbroken deeds?\b|\bbroken person\b|\bbroken people\b|\bbrokenness news\b', re.I)
GENERIC_STRONG = re.compile(r'\b(?:a person|any person|each person|someone|anyone|everyone|whoever|one who|the one who)\b', re.I)
GENERIC_SECONDARY = re.compile(r'\b(?:a child|a servant|a stranger|a foreigner|your neighbor|your enemy|the poor|the rich|the righteous|the wicked|a fool|the fool|the wise|a sluggard|the sluggard|a sinner|the sinner|a buyer|the buyer|a messenger|the messenger|a worker|the worker)\b', re.I)
GENERIC_MAN = re.compile(r'\b(?:any man|every man|each man|no man|a man who|the man who|man who|men who|all men|mankind)\b', re.I)
MASC_TERM = re.compile(r'\b(?:man|men|mankind|watchman|watchmen|workman|workmen|craftsman|craftsmen)\b', re.I)
ARTICLE_BAD = re.compile(r'\ban\s+(?:person|people|man|woman|child|human|worker|servant|neighbor)\b', re.I)


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

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

def extract_book(raw: bytes, slug: str, book: str):
    root=ET.fromstring(raw)
    parents={child:parent for parent in root.iter() for child in parent}
    anchors=[]
    for el in root.iter():
        n=chapter_number(el,slug)
        if n is not None: anchors.append((n,el))
    anchors.sort(key=lambda x:x[0])
    nums=[n for n,_ in anchors]
    expected=list(range(1,EXPECTED_CHAPTERS[slug]+1))
    if nums != expected: raise RuntimeError(f'chapter anchors invalid for {book}: expected {len(expected)}, found {nums}')
    verses=[]
    for number,el in anchors:
        frag=el
        if len(element_text(el)) < 80:
            parent=parents.get(el)
            if parent is None: raise RuntimeError(f'no wrapper for {book} {number}')
            siblings=list(parent); start=siblings.index(el); gathered=[]
            for sibling in siblings[start:]:
                if sibling is not el and chapter_number(sibling,slug) is not None: break
                gathered.append(copy.deepcopy(sibling))
            wrapper=ET.Element('section')
            for sibling in gathered: wrapper.append(sibling)
            frag=wrapper
        clean=strip_namespaces(frag); seen_verses=set(); found=0
        for node in clean.iter():
            if local_name(node.tag).lower()!='p': continue
            plain=element_text(node); m=re.match(r'^(\d+)\.\s*(.*)$',plain,re.S)
            if not m: continue
            verse=int(m.group(1))
            if verse in seen_verses: continue
            seen_verses.add(verse); found+=1
            verses.append((book,number,verse,collapse(m.group(2))))
        if not found: raise RuntimeError(f'no verses for {book} {number}')
    return verses

def extract_all():
    verses=[]
    with zipfile.ZipFile(EPUB) as z:
        bad=z.testzip()
        if bad: raise RuntimeError(f'EPUB CRC failure: {bad}')
        for slug,book in BOOKS.items():
            verses.extend(extract_book(z.read(find_book_member(z,slug)),slug,book))
    if len(verses)!=EXPECTED_OT_VERSES:
        raise RuntimeError(f'Old Testament verse inventory mismatch: {len(verses)} != {EXPECTED_OT_VERSES}')
    return verses

def nearby_divine(text, pos, window=160):
    start=max(0,pos-window); before=text[start:pos]; ms=list(DIV_RE.finditer(before))
    if not ms: return None,''
    m=ms[-1]; return m.group(0), before[m.start():]

def divine_hits(text):
    if not DIV_RE.search(text) or not PRON_RE.search(text): return []
    hits=[]
    for m in DEVOTION.finditer(text):
        divine,segment=nearby_divine(text,m.start(),180)
        if divine and not HUMAN_DISTRACTOR.search(segment[segment.find(divine)+len(divine):]): hits.append('devotion-object')
    for m in ATTR.finditer(text):
        divine,segment=nearby_divine(text,m.start(),130)
        if divine:
            after=segment[segment.rfind(divine)+len(divine):]
            if not HUMAN_DISTRACTOR.search(after): hits.append('divine-attribute')
    for m in SUBJECT_AFTER.finditer(text):
        if not HUMAN_DISTRACTOR.search(m.group('mid') or ''): hits.append('explicit-divine-subject')
    for m in SENTENCE_AFTER.finditer(text):
        if not HUMAN_DISTRACTOR.search(m.group('mid') or ''): hits.append('next-sentence-divine-subject')
    return sorted(set(hits))

def add(rows, seen, book, ch, vs, text, category, priority, signals, reason):
    key=(book,ch,vs,category)
    if key in seen: return
    seen.add(key); rows.append({'reference':f'{book} {ch}:{vs}','book':book,'chapter':ch,'verse':vs,'handledBook':book in HANDLED,'category':category,'priority':priority,'signals':'; '.join(signals),'reason':reason,'text':text})

def main():
    actual=sha256(EPUB)
    if actual != EXPECTED_SHA: raise SystemExit(f'Canonical EPUB SHA mismatch: {actual} != {EXPECTED_SHA}')
    allv=extract_all(); rows=[]; seen=set()
    for book,ch,vs,text in allv:
        if ARTICLE_BAD.search(text):
            add(rows,seen,book,ch,vs,text,'ARTICLE REGRESSION','CRITICAL',[ARTICLE_BAD.search(text).group(0)],'Invalid English article before a consonant-sound human noun; release blocker.')
        b=BROKENNESS.findall(text)
        if b:
            add(rows,seen,book,ch,vs,text,'BROKENNESS LEXICAL REVIEW','HIGH',sorted(set(x.lower() for x in b)),'The English brokenness/broken wording may flatten distinct Hebrew senses such as harm, wrongdoing, calamity, trouble, wickedness, misfortune, or destruction. Requires source/context review.')
        gm=GENERIC_MAN.findall(text)
        if gm:
            add(rows,seen,book,ch,vs,text,'GENERIC-HUMAN HIGH PRIORITY','HIGH',sorted(set(x.lower() for x in gm)),'Universal/generic human language is explicitly male-coded and should be checked against Hebrew for inclusive rendering.')
        elif MASC_TERM.search(text):
            add(rows,seen,book,ch,vs,text,'MASCULINE TERM REVIEW','REVIEW',sorted(set(x.lower() for x in MASC_TERM.findall(text))),'Masculine English term present. Preserve if the referent is actually male; revise only if the Hebrew/context is generic.')
        if GENERIC_STRONG.search(text) and PRON_RE.search(text):
            add(rows,seen,book,ch,vs,text,'GENERIC PRONOUN HIGH PRIORITY','HIGH',[GENERIC_STRONG.search(text).group(0)] + sorted(set(x.lower() for x in PRON_RE.findall(text))),'A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.')
        elif GENERIC_SECONDARY.search(text) and PRON_RE.search(text):
            add(rows,seen,book,ch,vs,text,'GENERIC PRONOUN REVIEW','REVIEW',[GENERIC_SECONDARY.search(text).group(0)] + sorted(set(x.lower() for x in PRON_RE.findall(text))),'A potentially generic antecedent is paired with masculine pronouns, but the referent may be a specific person. Context/source review required.')
        dh=divine_hits(text)
        if dh:
            add(rows,seen,book,ch,vs,text,'DIVINE-REFERENT REVIEW','HIGH',dh,'Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title.')
    OUT.mkdir(parents=True,exist_ok=True)
    fields=['reference','book','chapter','verse','handledBook','category','priority','signals','reason','text']
    with (OUT/'candidates.tsv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t'); w.writeheader(); w.writerows(rows)
    with (OUT/'all-verses.tsv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f,delimiter='\t'); w.writerow(['reference','text'])
        for b,c,v,t in allv: w.writerow([f'{b} {c}:{v}',t])
    bycat=Counter(r['category'] for r in rows); bypri=Counter(r['priority'] for r in rows); bybook=defaultdict(Counter); verse_counts=Counter(b for b,_,_,_ in allv)
    for r in rows: bybook[r['book']][r['category']]+=1
    summary={'canonicalEpubSha256':actual,'scope':'All 39 Old Testament books, including a residual recheck of Psalms, Proverbs, Ecclesiastes, and Isaiah.','extractedVerseCount':len(allv),'expectedOldTestamentVerseCount':EXPECTED_OT_VERSES,'verseCountValidation':'PASS','versesByBook':dict(verse_counts),'candidateRowCount':len(rows),'countsByCategory':dict(bycat),'countsByPriority':dict(bypri),'handledBooks':sorted(HANDLED),'countsByBook':{b:dict(c) for b,c in bybook.items()},'rule':'Diagnostic only. HIGH means strong editorial priority, not authorization to edit. Actual male characters/kinship/royal figures remain masculine; divine edits require unmistakable divine antecedent; brokenness requires Hebrew/context review. Review-tier rows intentionally include possible false positives.'}
    (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    high=[r for r in rows if r['priority'] in {'CRITICAL','HIGH'}]
    lines=['# Old Testament gender / divine-pronoun / brokenness residual audit — 2026-09-14','',f'Canonical EPUB SHA: `{actual}`','',f'Extracted verses: **{len(allv)} / {EXPECTED_OT_VERSES}** · candidate rows: **{len(rows)}** · high/critical rows: **{len(high)}**.','', 'This is diagnostic only. It does not authorize global replacement. Preserve actual male characters, male kinship, kings/royal figures, and source-significant gender. Repeat the established divine name/title only when the referent is unmistakably divine. Review every brokenness rendering against Hebrew/context rather than replacing the word globally. Review-tier rows intentionally include possible false positives.','', '## High / critical candidates','']
    for r in high: lines.append(f"- **{r['reference']} — {r['category']}** — {r['text']}")
    (OUT/'high-priority.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
