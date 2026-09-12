#!/usr/bin/env python3
"""Diagnostic scan for masculine pronouns near clearly divine Ruach expressions."""
from __future__ import annotations
import html, json, re, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
EPUB=ROOT/'current-form-documents'/'the-way-current.epub'
OUT=ROOT/'change-logs'/'reports'/'2026-09-12-divine-pronoun-ruach-audit.json'
MD=ROOT/'editor-notes'/'consistency'/'2026-09-12-divine-pronoun-ruach-audit.md'
BOOKS={'genesis':'Genesis','exodus':'Exodus','leviticus':'Leviticus','numbers':'Numbers','deuteronomy':'Deuteronomy','joshua':'Joshua','judges':'Judges','ruth':'Ruth','1-samuel':'1 Samuel','2-samuel':'2 Samuel','1-kings':'1 Kings','2-kings':'2 Kings','1-chronicles':'1 Chronicles','2-chronicles':'2 Chronicles','ezra':'Ezra','nehemiah':'Nehemiah','esther':'Esther','job':'Job','psalms':'Psalms','proverbs':'Proverbs','ecclesiastes':'Ecclesiastes','song-of-solomon':'Song of Solomon','isaiah':'Isaiah','jeremiah':'Jeremiah','lamentations':'Lamentations','ezekiel':'Ezekiel','daniel':'Daniel','hosea':'Hosea','joel':'Joel','amos':'Amos','obadiah':'Obadiah','jonah':'Jonah','micah':'Micah','nahum':'Nahum','habakkuk':'Habakkuk','zephaniah':'Zephaniah','haggai':'Haggai','zechariah':'Zechariah','malachi':'Malachi','matthew':'Matthew','mark':'Mark','luke':'Luke','john':'John','acts':'Acts','romans':'Romans','1-corinthians':'1 Corinthians','2-corinthians':'2 Corinthians','galatians':'Galatians','ephesians':'Ephesians','philippians':'Philippians','colossians':'Colossians','1-thessalonians':'1 Thessalonians','2-thessalonians':'2 Thessalonians','1-timothy':'1 Timothy','2-timothy':'2 Timothy','titus':'Titus','philemon':'Philemon','hebrews':'Hebrews','james':'James','1-peter':'1 Peter','2-peter':'2 Peter','1-john':'1 John','2-john':'2 John','3-john':'3 John','jude':'Jude','revelation':'Revelation'}
RUACH=re.compile(r'\b(?:Ruach of (?:YHWH|Elohim)|Holy Ruach|Ruach HaKodesh|the Ruach)\b',re.I)
PRON=re.compile(r'\b(?:he|him|his|himself)\b',re.I)

def visible(s): return html.unescape(re.sub(r'<[^>]+>','',s)).replace('\u00a0',' ').strip()

def main():
    rows=[]
    with zipfile.ZipFile(EPUB) as z:
        for member in z.namelist():
            mm=re.fullmatch(r'OEBPS/Text/(.+)\.xhtml',member)
            if not mm: continue
            slug=mm.group(1); book=BOOKS.get(slug,slug); chapter=None
            raw=z.read(member).decode('utf-8')
            for pm in re.finditer(r'<p\b(?P<a>[^>]*)>(?P<i>.*?)</p>',raw,re.I|re.S):
                ch=re.search(rf'id=["\']ch-{re.escape(slug)}-(\d+)["\']',pm.group('a'),re.I)
                if ch: chapter=int(ch.group(1)); continue
                txt=visible(pm.group('i')); vm=re.match(r'^(\d+)\.\s*(.*)$',txt,re.S)
                if not vm or chapter is None: continue
                body=vm.group(2).strip()
                if RUACH.search(body) and PRON.search(body):
                    rows.append({'reference':f'{book} {chapter}:{int(vm.group(1))}','text':body})
    OUT.parent.mkdir(parents=True,exist_ok=True); MD.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps({'count':len(rows),'candidates':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Divine Ruach masculine-pronoun audit — 2026-09-12','',f'Same-verse candidates: **{len(rows)}**. Diagnostic only; the pronoun may refer to a human, Yeshua, or another entity and must be reviewed in context.','']
    lines.extend(f"- **{r['reference']}** — {r['text']}" for r in rows)
    MD.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'ruachSameVerseCandidates':len(rows)},indent=2))
if __name__=='__main__': main()
