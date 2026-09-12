#!/usr/bin/env python3
from __future__ import annotations
import html, json, re, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
EPUB=ROOT/'current-form-documents'/'the-way-current.epub'
REGISTRY=ROOT/'current-form-documents'/'original-name-registry.json'
OUTJ=ROOT/'change-logs'/'reports'/'2026-09-12-final-release-alignment-v2.json'
OUTM=ROOT/'editor-notes'/'consistency'/'2026-09-12-final-release-alignment-v2.md'
BOOKS={'genesis':'Genesis','exodus':'Exodus','leviticus':'Leviticus','numbers':'Numbers','deuteronomy':'Deuteronomy','joshua':'Joshua','judges':'Judges','ruth':'Ruth','1-samuel':'1 Samuel','2-samuel':'2 Samuel','1-kings':'1 Kings','2-kings':'2 Kings','1-chronicles':'1 Chronicles','2-chronicles':'2 Chronicles','ezra':'Ezra','nehemiah':'Nehemiah','esther':'Esther','job':'Job','psalms':'Psalms','proverbs':'Proverbs','ecclesiastes':'Ecclesiastes','song-of-solomon':'Song of Solomon','isaiah':'Isaiah','jeremiah':'Jeremiah','lamentations':'Lamentations','ezekiel':'Ezekiel','daniel':'Daniel','hosea':'Hosea','joel':'Joel','amos':'Amos','obadiah':'Obadiah','jonah':'Jonah','micah':'Micah','nahum':'Nahum','habakkuk':'Habakkuk','zephaniah':'Zephaniah','haggai':'Haggai','zechariah':'Zechariah','malachi':'Malachi','matthew':'Matthew','mark':'Mark','luke':'Luke','john':'John','acts':'Acts','romans':'Romans','1-corinthians':'1 Corinthians','2-corinthians':'2 Corinthians','galatians':'Galatians','ephesians':'Ephesians','philippians':'Philippians','colossians':'Colossians','1-thessalonians':'1 Thessalonians','2-thessalonians':'2 Thessalonians','1-timothy':'1 Timothy','2-timothy':'2 Timothy','titus':'Titus','philemon':'Philemon','hebrews':'Hebrews','james':'James','1-peter':'1 Peter','2-peter':'2 Peter','1-john':'1 John','2-john':'2 John','3-john':'3 John','jude':'Jude','revelation':'Revelation'}
TARGET_REFS={'Matthew 27:37','Mark 15:26','Luke 23:38','John 19:19','John 19:20'}
ALREADY_COMPLETE=[('yeshua','Jesus','Yeshua'),('babylon','Babylon','Bavel'),('nazareth','Nazareth','Natzeret')]

def vis(s): return html.unescape(re.sub(r'<[^>]+>','',s)).replace('\u00a0',' ').strip()
def pat(s): return re.compile(r'(?<![A-Za-z0-9_])'+re.escape(s)+r'(?![A-Za-z0-9_])',re.I)
def verses():
  with zipfile.ZipFile(EPUB) as z:
    for member in z.namelist():
      m=re.fullmatch(r'OEBPS/Text/(.+)\.xhtml',member)
      if not m: continue
      slug=m.group(1); book=BOOKS.get(slug,slug); ch=None; raw=z.read(member).decode('utf-8')
      for pm in re.finditer(r'<p\b(?P<a>[^>]*)>(?P<i>.*?)</p>',raw,re.I|re.S):
        cm=re.search(rf'id=["\']ch-{re.escape(slug)}-(\d+)["\']',pm.group('a'),re.I)
        if cm: ch=int(cm.group(1)); continue
        t=vis(pm.group('i')); vm=re.match(r'^(\d+)\.\s*(.*)$',t,re.S)
        if vm and ch: yield {'reference':f'{book} {ch}:{int(vm.group(1))}','member':member,'text':vm.group(2).strip()}

def main():
  reg=json.loads(REGISTRY.read_text(encoding='utf-8'))
  checks=[]
  for item in reg.get('entries',[]):
    if item.get('editorialStatus')!='released': continue
    term=item.get('term','')
    for alias in item.get('traditionalAliases',[]):
      if alias and alias.casefold()!=term.casefold(): checks.append((item.get('id'),alias,term))
  checks.extend(ALREADY_COMPLETE)
  allv=list(verses()); stale=[]
  for v in allv:
    for ident,alias,term in checks:
      for m in pat(alias).finditer(v['text']):
        # do not count a case-insensitive alias if it is exactly the canonical form
        if m.group(0).casefold()==term.casefold(): continue
        stale.append({**v,'id':ident,'alias':alias,'matched':m.group(0),'canonical':term})
  exact={v['reference']:v['text'] for v in allv if v['reference'] in TARGET_REFS}
  inscription_legacy=[v for v in allv if re.search(r'\bJESUS\b|\bNAZARETH\b|\bKING OF THE JEWS\b',v['text'],re.I)]
  report={'epub':str(EPUB.relative_to(ROOT)),'releasedChecks':len(checks),'staleReleasedNameHits':len(stale),'staleReleasedNameVerses':len({x['reference'] for x in stale}),'staleHits':stale,'targetVerses':exact,'legacyInscriptionCandidates':inscription_legacy}
  OUTJ.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  lines=['# Final released-name + crucifixion-inscription audit — 2026-09-12','',f"- Released/complete alias checks: **{len(checks)}**",f"- Stale released-name hits: **{len(stale)}** across **{len({x['reference'] for x in stale})}** verses",f"- Legacy inscription candidates (`Jesus`, `Nazareth`, `King of the Jews`): **{len(inscription_legacy)}**",'', '## Current canonical target verses','']
  for ref in sorted(exact): lines.append(f'- **{ref}** — {exact[ref]}')
  lines+=['','## Stale released-name hits','']
  for x in stale: lines.append(f"- **{x['reference']}** — `{x['matched']}` → `{x['canonical']}` ({x['id']}) — {x['text']}")
  lines+=['','## Legacy inscription candidates','']
  for x in inscription_legacy: lines.append(f"- **{x['reference']}** — {x['text']}")
  OUTM.write_text('\n'.join(lines)+'\n',encoding='utf-8')
  print(json.dumps({'staleReleasedNameHits':len(stale),'legacyInscriptionCandidates':len(inscription_legacy),'targets':exact},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
