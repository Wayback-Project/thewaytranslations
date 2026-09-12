#!/usr/bin/env python3
"""Produce a conservative triage list of likely residual divine masculine pronouns.

This tool is diagnostic. It intentionally over-includes some candidates for human
review and never edits Scripture. It narrows the broad proximity inventory using
lexical/coreference signatures that commonly indicate an unmistakable divine
antecedent under The Way Version's current policy.
"""
from __future__ import annotations

import html
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / 'current-form-documents' / 'the-way-current.epub'
OUT = ROOT / 'editor-notes' / 'consistency' / '2026-09-12-divine-pronoun-high-confidence-triage.md'
OUT_JSON = ROOT / 'change-logs' / 'reports' / '2026-09-12-divine-pronoun-high-confidence-triage.json'

BOOKS = {
'genesis':'Genesis','exodus':'Exodus','leviticus':'Leviticus','numbers':'Numbers','deuteronomy':'Deuteronomy','joshua':'Joshua','judges':'Judges','ruth':'Ruth','1-samuel':'1 Samuel','2-samuel':'2 Samuel','1-kings':'1 Kings','2-kings':'2 Kings','1-chronicles':'1 Chronicles','2-chronicles':'2 Chronicles','ezra':'Ezra','nehemiah':'Nehemiah','esther':'Esther','job':'Job','psalms':'Psalms','proverbs':'Proverbs','ecclesiastes':'Ecclesiastes','song-of-solomon':'Song of Solomon','isaiah':'Isaiah','jeremiah':'Jeremiah','lamentations':'Lamentations','ezekiel':'Ezekiel','daniel':'Daniel','hosea':'Hosea','joel':'Joel','amos':'Amos','obadiah':'Obadiah','jonah':'Jonah','micah':'Micah','nahum':'Nahum','habakkuk':'Habakkuk','zephaniah':'Zephaniah','haggai':'Haggai','zechariah':'Zechariah','malachi':'Malachi','matthew':'Matthew','mark':'Mark','luke':'Luke','john':'John','acts':'Acts','romans':'Romans','1-corinthians':'1 Corinthians','2-corinthians':'2 Corinthians','galatians':'Galatians','ephesians':'Ephesians','philippians':'Philippians','colossians':'Colossians','1-thessalonians':'1 Thessalonians','2-thessalonians':'2 Thessalonians','1-timothy':'1 Timothy','2-timothy':'2 Timothy','titus':'Titus','philemon':'Philemon','hebrews':'Hebrews','james':'James','1-peter':'1 Peter','2-peter':'2 Peter','1-john':'1 John','2-john':'2 John','3-john':'3 John','jude':'Jude','revelation':'Revelation'}

DIV = r'(?:YHWH|Elohim|God|Cosmic Parent|El Shaddai|Elyon|Yah|Most High|Almighty|Creator)'
PRON = r'(?:he|him|his|himself)'
PRON_RE = re.compile(rf'\b{PRON}\b', re.I)
DIV_RE = re.compile(rf'\b{DIV}\b')

# Verbs where a nearby masculine object is often directly addressed to / acting toward God.
DEVOTION = re.compile(r'\b(?:serve|serves|served|seek|seeks|sought|follow|follows|followed|revere|reveres|revered|fear|fears|feared|worship|worships|worshiped|trust|trusts|trusted|wait|waits|waited|call on|calls on|called on|pray to|prays to|prayed to|praise|praises|praised|exalt|exalts|exalted|forsake|forsakes|forsook|obey|obeys|obeyed|return to|returns to|returned to|draw near to|draws near to|provoke|provokes|provoked|inquire after|inquired after|inquire of|inquired of)\s+(?:only\s+)?(?P<p>him|his|himself)\b', re.I)

ATTR = re.compile(r'\b(?P<p>his)\s+(?:anger|wrath|mercy|grace|name|glory|power|hand|eyes|commandments|commandment|statutes|ordinances|covenant|word|voice|soul|spirit|Ruach|blessings|counsel|thoughts|temple|sanctuary|holy\s+place|holy\s+temple|people|servants|prophets|army|flock|land|house|works|wondrous\s+works|law|laws|gift|jealousy|place)\b', re.I)

# Strong connective subject patterns: explicit divine subject followed by masculine continuation.
SUBJECT_AFTER = re.compile(rf'\b(?P<d>{DIV})\b(?P<mid>[^.!?]{{0,110}}?)(?:;|,|\band\b|\bfor\b|\bbecause\b|\bwho\b|\bthat\b)\s*(?P<p>he|his|himself)\b', re.I)
SENTENCE_AFTER = re.compile(rf'\b(?P<d>{DIV})\b(?P<mid>[^.!?]{{0,140}}?)[.!?]\s*[\"“‘\']*(?P<p>He|His|Himself)\b')

# A pronoun explicitly identified by a divine role after it.
ROLE_AFTER = re.compile(r'\b(?P<p>him)\b[^.!?]{0,45}\b(?:as\s+)?(?:Cosmic Parent|Creator|God|Elohim|YHWH)\b', re.I)

# Strongly human/Christic material after the divine marker usually means proximity alone is misleading.
HUMAN_DISTRACTOR = re.compile(r'\b(?:Yeshua|Messiah|Master|Son|angel|prophet|priest|king|Pharaoh|Moshe|Aharon|Dawid|Shlomo|Shaul|Kepha|Yonah|Yehoshua|Gid.on|Job|man|woman|person|child|father|mother|brother|sister|servant|people|enemy|neighbor|ruler|one\s+who)\b', re.I)


def visible(s):
    return html.unescape(re.sub(r'<[^>]+>','',s)).replace('\u00a0',' ').strip()


def verses():
    with zipfile.ZipFile(EPUB) as z:
        for member in z.namelist():
            m = re.fullmatch(r'OEBPS/Text/(.+)\.xhtml', member)
            if not m: continue
            slug=m.group(1); book=BOOKS.get(slug,slug); chapter=None
            raw=z.read(member).decode('utf-8')
            for pm in re.finditer(r'<p\b(?P<a>[^>]*)>(?P<i>.*?)</p>', raw, re.I|re.S):
                ch=re.search(rf'id=["\']ch-{re.escape(slug)}-(\d+)["\']', pm.group('a'), re.I)
                if ch: chapter=int(ch.group(1)); continue
                txt=visible(pm.group('i')); vm=re.match(r'^(\d+)\.\s*(.*)$',txt,re.S)
                if vm and chapter:
                    yield f'{book} {chapter}:{int(vm.group(1))}', vm.group(2).strip()


def nearby_divine(text, pos, window=150):
    start=max(0,pos-window); before=text[start:pos]
    matches=list(DIV_RE.finditer(before))
    if not matches: return None, before
    return matches[-1].group(0), before[matches[-1].start():]


def classify(ref,text):
    if not PRON_RE.search(text) or not DIV_RE.search(text): return []
    hits=[]
    for m in DEVOTION.finditer(text):
        divine, segment=nearby_divine(text,m.start(),180)
        if divine and not HUMAN_DISTRACTOR.search(segment[segment.find(divine)+len(divine):]):
            hits.append(('devotion-object',m.group('p'),divine,m.start()))
    for m in ATTR.finditer(text):
        divine, segment=nearby_divine(text,m.start(),130)
        if divine:
            after_div=segment[segment.rfind(divine)+len(divine):]
            # Attributes are high-confidence only if there is no competing human/Christic noun after the divine marker.
            if not HUMAN_DISTRACTOR.search(after_div):
                hits.append(('divine-attribute',m.group('p'),divine,m.start()))
    for m in SUBJECT_AFTER.finditer(text):
        mid=m.group('mid') or ''
        if not HUMAN_DISTRACTOR.search(mid):
            hits.append(('explicit-divine-subject',m.group('p'),m.group('d'),m.start('p')))
    for m in SENTENCE_AFTER.finditer(text):
        mid=m.group('mid') or ''
        if not HUMAN_DISTRACTOR.search(mid):
            hits.append(('next-sentence-divine-subject',m.group('p'),m.group('d'),m.start('p')))
    for m in ROLE_AFTER.finditer(text):
        hits.append(('explicit-divine-role',m.group('p'),'role-after-pronoun',m.start('p')))
    # Deduplicate same pronoun position while retaining the strongest first category.
    seen=set(); out=[]
    for hit in hits:
        key=hit[3]
        if key not in seen:
            seen.add(key); out.append(hit)
    return out


def main():
    rows=[]
    for ref,text in verses():
        hits=classify(ref,text)
        if hits: rows.append({'reference':ref,'text':text,'signals':[{'type':h[0],'pronoun':h[1],'divine':h[2]} for h in hits]})
    OUT_JSON.parent.mkdir(parents=True,exist_ok=True); OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT_JSON.write_text(json.dumps({'count':len(rows),'candidates':rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# High-confidence divine-pronoun residual triage — 2026-09-12','',f'Conservative heuristic candidates: **{len(rows)}**. This file is review-only and makes no Scripture changes.','']
    for row in rows:
        sig=', '.join(f"{x['type']}:{x['pronoun']}→{x['divine']}" for x in row['signals'])
        lines.append(f"- **{row['reference']}** — [{sig}] — {row['text']}")
    OUT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps({'highConfidenceTriageCount':len(rows)},indent=2))

if __name__=='__main__': main()
