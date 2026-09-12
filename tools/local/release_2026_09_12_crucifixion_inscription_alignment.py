#!/usr/bin/env python3
from __future__ import annotations

import bisect
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
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / 'current-form-documents' / 'the-way-current.epub'
REGISTRY = ROOT / 'current-form-documents' / 'original-name-registry.json'
CURRENT_README = ROOT / 'current-form-documents' / 'README.md'
ROOT_README = ROOT / 'README.md'
HISTORY_LOG = ROOT / 'rendered-documents-history' / 'LOG.md'
LEDGER = ROOT / 'change-logs' / 'reports' / '2026-09-12-crucifixion-inscription-name-alignment.json'
NOTE = ROOT / 'editor-notes' / 'consistency' / '2026-09-12-crucifixion-inscription-name-alignment.md'
BASELINE = 'fb14e9bdf84c1eef9a67c135ae7c42edf070e3f39ea4b8a265fa4a4a9dc1129a'

CHANGES = [
    {
        'reference': 'Matthew 27:37',
        'before': 'They set up over his head the accusation against him written, "THIS IS JESUS, THE KING OF THE JEWS."',
        'after': 'They set up over his head the accusation against him written, "THIS IS YESHUA, THE KING OF THE JUDEANS."',
        'reason': 'Restore the released Yeshua form and keep the Passion-context Ioudaioi rendering consistent as Judeans.',
        'source': 'original-documents/matthew_restorative_translation.txt',
    },
    {
        'reference': 'Mark 15:26',
        'before': 'The superscription of his accusation was written over him, "THE KING OF THE JEWS."',
        'after': 'The superscription of his accusation was written over him, "THE KING OF THE JUDEANS."',
        'reason': 'Keep the inscription ethnonym aligned with the edition’s established Judeans rendering for Ioudaioi in the Passion context.',
        'source': 'original-documents/mark_restorative_translation.txt',
    },
    {
        'reference': 'Luke 23:38',
        'before': 'An inscription was also written over him in letters of Greek, Latin, and Hebrew: "THIS IS THE KING OF THE JEWS."',
        'after': 'An inscription was also written over him in letters of Greek, Latin, and Hebrew: "THIS IS THE KING OF THE JUDEANS."',
        'reason': 'Keep the inscription ethnonym aligned with the edition’s established Judeans rendering for Ioudaioi in the Passion context.',
        'source': 'original-documents/luke_restorative_translation.txt',
    },
    {
        'reference': 'John 19:19',
        'before': 'Pilatus wrote a title also, and put it on the cross. There was written, "JESUS OF NAZARETH, THE KING OF THE JEWS."',
        'after': 'Pilatus wrote a title also, and put it on the cross. There was written, "YESHUA OF NATZERET, THE KING OF THE JUDEANS."',
        'reason': 'Restore released Yeshua and Natzeret forms and keep Ioudaioi aligned as Judeans. John 19:20 says the title was written in Hebrew, Latin, and Greek, so the English text does not invent one exclusive Aramaic reconstruction.',
        'source': 'original-documents/john_restorative_translation.txt',
    },
]

BOOKS = {
'genesis':'Genesis','exodus':'Exodus','leviticus':'Leviticus','numbers':'Numbers','deuteronomy':'Deuteronomy','joshua':'Joshua','judges':'Judges','ruth':'Ruth','1-samuel':'1 Samuel','2-samuel':'2 Samuel','1-kings':'1 Kings','2-kings':'2 Kings','1-chronicles':'1 Chronicles','2-chronicles':'2 Chronicles','ezra':'Ezra','nehemiah':'Nehemiah','esther':'Esther','job':'Job','psalms':'Psalms','proverbs':'Proverbs','ecclesiastes':'Ecclesiastes','song-of-solomon':'Song of Solomon','isaiah':'Isaiah','jeremiah':'Jeremiah','lamentations':'Lamentations','ezekiel':'Ezekiel','daniel':'Daniel','hosea':'Hosea','joel':'Joel','amos':'Amos','obadiah':'Obadiah','jonah':'Jonah','micah':'Micah','nahum':'Nahum','habakkuk':'Habakkuk','zephaniah':'Zephaniah','haggai':'Haggai','zechariah':'Zechariah','malachi':'Malachi','matthew':'Matthew','mark':'Mark','luke':'Luke','john':'John','acts':'Acts','romans':'Romans','1-corinthians':'1 Corinthians','2-corinthians':'2 Corinthians','galatians':'Galatians','ephesians':'Ephesians','philippians':'Philippians','colossians':'Colossians','1-thessalonians':'1 Thessalonians','2-thessalonians':'2 Thessalonians','1-timothy':'1 Timothy','2-timothy':'2 Timothy','titus':'Titus','philemon':'Philemon','hebrews':'Hebrews','james':'James','1-peter':'1 Peter','2-peter':'2 Peter','1-john':'1 John','2-john':'2 John','3-john':'3 John','jude':'Jude','revelation':'Revelation'}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def visible(inner: str) -> str:
    return html.unescape(re.sub(r'<[^>]+>', '', inner)).replace('\u00a0', ' ').strip()


def replace_one(member_text: str, verse_no: str, before: str, after: str):
    pat = re.compile(r'(<(?:[A-Za-z_][\w.-]*:)?p\b[^>]*>)(.*?)(</(?:[A-Za-z_][\w.-]*:)?p>)', re.I | re.S)
    matches = []
    for m in pat.finditer(member_text):
        text = visible(m.group(2))
        if text in (f'{verse_no}. {before}', f'{verse_no}.{before}'):
            matches.append(m)
    if not matches:
        return member_text, 0
    if len(matches) != 1:
        raise RuntimeError(f'multiple paragraph matches in one member for verse {verse_no}: {before[:80]}')
    m = matches[0]
    if re.search(r'<[^>]+>', m.group(2)):
        raise RuntimeError(f'inline markup in target paragraph; refusing rewrite: {before[:80]}')
    rendered = html.escape(f'{verse_no}. {after}', quote=False)
    return member_text[:m.start(2)] + rendered + member_text[m.end(2):], 1


def validate_epub(path: Path) -> tuple[int, int]:
    with zipfile.ZipFile(path, 'r') as z:
        if z.testzip() is not None:
            raise RuntimeError('ZIP CRC failure')
        first = z.infolist()[0]
        if first.filename != 'mimetype' or first.compress_type != zipfile.ZIP_STORED:
            raise RuntimeError('EPUB mimetype rule failed')
        if z.read('mimetype') != b'application/epub+zip':
            raise RuntimeError('EPUB mimetype content failed')
        names = set(z.namelist())
        ids = {}
        book_members = []
        chapter_count = 0
        for name in z.namelist():
            if name.lower().endswith(('.xhtml','.html','.htm','.opf','.ncx','.xml')):
                raw = z.read(name)
                ET.fromstring(raw)
                text = raw.decode('utf-8','ignore')
                ids[name] = set(re.findall(r'\bid=["\']([^"\']+)', text))
                cc = len(re.findall(r'\bid=["\']ch-', text))
                if cc:
                    book_members.append(name)
                    chapter_count += cc
                if '<<' in text or '>>' in text:
                    raise RuntimeError(f'angle-marker artifact in {name}')
        if len(book_members) != 66:
            raise RuntimeError(f'expected 66 book XHTML members, got {len(book_members)}')
        if chapter_count != 1189:
            raise RuntimeError(f'expected 1189 chapter anchors, got {chapter_count}')
        unresolved = []
        for src in ids:
            text = z.read(src).decode('utf-8','ignore')
            for href in re.findall(r'\bhref=["\']([^"\']+)', text):
                if not href or href.startswith(('http:','https:','mailto:','data:','javascript:')):
                    continue
                path_part, sep, frag = href.partition('#')
                target = src if not path_part else posixpath.normpath(posixpath.join(posixpath.dirname(src), urllib.parse.unquote(path_part)))
                if target not in names:
                    unresolved.append((src,href,'missing member')); continue
                if sep and frag and target in ids and urllib.parse.unquote(frag) not in ids[target]:
                    unresolved.append((src,href,'missing fragment'))
        if unresolved:
            raise RuntimeError(f'unresolved internal links: {unresolved[:10]}')
        return len(book_members), chapter_count


def verse_rows(path: Path):
    with zipfile.ZipFile(path, 'r') as z:
        for member in z.namelist():
            m = re.fullmatch(r'OEBPS/Text/(.+)\.xhtml', member)
            if not m: continue
            slug=m.group(1); book=BOOKS.get(slug,slug); chapter=None
            raw=z.read(member).decode('utf-8')
            for pm in re.finditer(r'<p\b(?P<a>[^>]*)>(?P<i>.*?)</p>', raw, re.I|re.S):
                ch=re.search(rf'id=["\']ch-{re.escape(slug)}-(\d+)["\']', pm.group('a'), re.I)
                if ch:
                    chapter=int(ch.group(1)); continue
                text=visible(pm.group('i')); vm=re.match(r'^(\d+)\.\s*(.*)$',text,re.S)
                if vm and chapter:
                    yield f'{book} {chapter}:{int(vm.group(1))}', vm.group(2).strip()


def final_name_audit(path: Path, registry: dict):
    rows=list(verse_rows(path))
    stale=[]
    released=[e for e in registry.get('entries',[]) if e.get('editorialStatus')=='released']
    checks=[]
    for e in released:
        term=e.get('term','')
        for alias in e.get('traditionalAliases',[]):
            if alias and alias.casefold()!=term.casefold(): checks.append((e.get('id'),alias,term))
    checks.extend([('yeshua','Jesus','Yeshua'),('babylon','Babylon','Bavel'),('nazareth','Nazareth','Natzeret')])
    for ref,text in rows:
        for ident,alias,term in checks:
            p=re.compile(r'(?<![A-Za-z0-9_])'+re.escape(alias)+r'(?![A-Za-z0-9_])',re.I)
            for m in p.finditer(text):
                if m.group(0).casefold()!=term.casefold():
                    stale.append({'reference':ref,'id':ident,'matched':m.group(0),'canonical':term,'text':text})
    inscription=[]
    for ref,text in rows:
        if re.search(r'\bJESUS\b|\bNAZARETH\b|KING OF THE JEWS', text, re.I):
            inscription.append({'reference':ref,'text':text})
    return {'releasedChecks':len(checks),'staleReleasedNameHits':stale,'legacyInscriptionHits':inscription}


def main():
    actual=sha256(EPUB)
    if actual != BASELINE:
        raise SystemExit(f'baseline SHA mismatch: expected {BASELINE}, got {actual}')

    # The editable mirrors were already reconciled in the preceding documentation transaction.
    for change in CHANGES:
        src=ROOT/change['source']
        text=src.read_text(encoding='utf-8')
        if change['after'] not in text:
            raise RuntimeError(f"source mirror is not aligned for {change['reference']}: {change['source']}")

    stamp=datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%MUTC')
    archive_dir=ROOT/'rendered-documents-history'/stamp
    archive_dir.mkdir(parents=True,exist_ok=False)
    archive=archive_dir/EPUB.name
    shutil.copy2(EPUB,archive)
    if sha256(archive)!=BASELINE:
        raise RuntimeError('archive SHA mismatch')

    with zipfile.ZipFile(EPUB,'r') as zin:
        infos=zin.infolist(); original={i.filename:zin.read(i.filename) for i in infos}
    edited=dict(original); applied=[]; changed_members=set()
    for change in CHANGES:
        verse_no=change['reference'].rsplit(':',1)[1]
        found=[]
        for name,data in list(edited.items()):
            if not name.lower().endswith(('.xhtml','.html','.htm')): continue
            try: text=data.decode('utf-8')
            except UnicodeDecodeError: continue
            new_text,count=replace_one(text,verse_no,change['before'],change['after'])
            if count:
                found.append(name); edited[name]=new_text.encode('utf-8'); changed_members.add(name)
        if len(found)!=1:
            raise RuntimeError(f"{change['reference']}: expected exactly one EPUB paragraph match, got {found}")
        applied.append({'reference':change['reference'],'member':found[0]})

    fd,tmpname=tempfile.mkstemp(suffix='.epub',dir=str(EPUB.parent)); os.close(fd); tmp=Path(tmpname)
    try:
        with zipfile.ZipFile(tmp,'w') as zout:
            for info in infos:
                zout.writestr(info,edited[info.filename],compress_type=info.compress_type)
        validate_epub(tmp)
        shutil.move(tmp,EPUB)
    finally:
        if tmp.exists(): tmp.unlink()

    newsha=sha256(EPUB)
    if newsha==BASELINE: raise RuntimeError('release SHA did not change')
    changed=[n for n in original if original[n]!=edited[n]]
    if set(changed)!=changed_members: raise RuntimeError('unexpected uncompressed member changes')
    expected_members={'OEBPS/Text/matthew.xhtml','OEBPS/Text/mark.xhtml','OEBPS/Text/luke.xhtml','OEBPS/Text/john.xhtml'}
    if changed_members!=expected_members:
        raise RuntimeError(f'unexpected changed book members: {sorted(changed_members)}')

    registry=json.loads(REGISTRY.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256')!=BASELINE:
        raise RuntimeError(f"registry baseline SHA mismatch: {registry.get('canonicalEpubSha256')}")
    registry['canonicalEpubSha256']=newsha
    REGISTRY.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    audit=final_name_audit(EPUB,registry)
    if audit['staleReleasedNameHits']:
        raise RuntimeError(f"stale released names remain: {audit['staleReleasedNameHits'][:10]}")
    if audit['legacyInscriptionHits']:
        raise RuntimeError(f"legacy inscription forms remain: {audit['legacyInscriptionHits']}")

    report={
        'release':'2026-09-12 crucifixion inscription original-name alignment',
        'prior_epub_sha256':BASELINE,
        'released_epub_sha256':newsha,
        'archive_path':archive.relative_to(ROOT).as_posix(),
        'change_count':len(CHANGES),
        'changes':CHANGES,
        'applied':applied,
        'finalNameAudit':{
            'releasedChecks':audit['releasedChecks'],
            'staleReleasedNameHitCount':0,
            'legacyInscriptionHitCount':0,
        },
        'qa':{
            'book_count':66,'chapter_count':1189,'zip_crc':'pass','xml_parse':'pass','internal_links':'pass',
            'changed_book_members':sorted(changed_members),
        },
    }
    LEDGER.parent.mkdir(parents=True,exist_ok=True)
    LEDGER.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    NOTE.write_text(f'''# Crucifixion inscription original-name alignment — 2026-09-12

## Released changes

- Matthew 27:37 — `THIS IS JESUS, THE KING OF THE JEWS.` → `THIS IS YESHUA, THE KING OF THE JUDEANS.`
- Mark 15:26 — `THE KING OF THE JEWS.` → `THE KING OF THE JUDEANS.`
- Luke 23:38 — `THIS IS THE KING OF THE JEWS.` → `THIS IS THE KING OF THE JUDEANS.`
- John 19:19 — `JESUS OF NAZARETH, THE KING OF THE JEWS.` → `YESHUA OF NATZERET, THE KING OF THE JUDEANS.`

## Historical/textual rationale

John 19:20 explicitly says the title was written in Hebrew, Latin, and Greek. The English Scripture therefore does not invent one exclusive Aramaic reconstruction of the sign. It translates the title content while applying this edition’s released name conventions (`Yeshua`, `Natzeret`) and the existing Passion-context rendering `Judeans` for Greek `Ioudaioi`.

## Final name audit

- Released/complete alias checks: **{audit['releasedChecks']}**
- Stale released-name hits: **0**
- Remaining `Jesus` / `Nazareth` / `King of the Jews` inscription hits: **0**
- Guide-only familiar-name entries (for example Yair/Jair) remain metadata-only unless separately approved for Scripture change.

## Artifact

- Prior SHA-256: `{BASELINE}`
- Released SHA-256: `{newsha}`
- Prior EPUB archive: `{archive.relative_to(ROOT).as_posix()}`
- Coverage: 66 books / 1,189 chapters
- Exact before/after ledger: `change-logs/reports/2026-09-12-crucifixion-inscription-name-alignment.json`
''',encoding='utf-8')

    cr=CURRENT_README.read_text(encoding='utf-8')
    if BASELINE not in cr: raise RuntimeError('current README baseline SHA missing')
    cr=cr.replace(BASELINE,newsha)
    cr=re.sub(r'\| Previous release \| Archived under `rendered-documents-history/[^`]+/` \|',f'| Previous release | Archived under `{archive_dir.relative_to(ROOT).as_posix()}/` |',cr)
    marker='plus the 2026-09-12 high-priority original-name restoration release;'
    if marker in cr:
        cr=cr.replace(marker,'plus the 2026-09-12 high-priority original-name restoration release and crucifixion-inscription alignment (4 reviewed verse-level edits);')
    CURRENT_README.write_text(cr,encoding='utf-8')

    rr=ROOT_README.read_text(encoding='utf-8')
    if BASELINE in rr:
        ROOT_README.write_text(rr.replace(BASELINE,newsha),encoding='utf-8')

    log=HISTORY_LOG.read_text(encoding='utf-8')
    line=f'| {stamp} | {archive_dir.relative_to(ROOT).as_posix()}/ | the-way-current.epub (SHA-256 `{BASELINE}`) | pre-crucifixion-inscription-name-alignment snapshot |'
    if line not in log:
        HISTORY_LOG.write_text(log.rstrip()+'\n'+line+'\n',encoding='utf-8')

    print(json.dumps({'releasedSha256':newsha,'changes':len(CHANGES),'finalNameChecks':audit['releasedChecks'],'staleReleasedNames':0,'legacyInscriptionHits':0},indent=2))

if __name__=='__main__': main()
