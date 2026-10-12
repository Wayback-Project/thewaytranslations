#!/usr/bin/env python3
"""Context triage of all New Testament masculine pronouns and royal-language residue.
This is candidate discovery only. A masculine pronoun next to 'God' is NOT
automatically a divine pronoun. The reviewer must read connected verses."""
from __future__ import annotations
import json,re
from collections import Counter
from pathlib import Path
import release_2026_09_30_kingdom_residuals as rel

ROOT=rel.ROOT
REPORT=ROOT/'change-logs/reports/2026-10-12-new-testament-divine-masculine-candidate-audit.json'
INDEX=ROOT/'change-logs/reports/2026-10-12-new-testament-divine-masculine-candidate-audit.md'
nt=['matthew','mark','luke','john','acts','romans','1-corinthians','2-corinthians',
'galatians','ephesians','philippians','colossians','1-thessalonians','2-thessalonians',
'1-timothy','2-timothy','titus','philemon','hebrews','james','1-peter','2-peter',
'1-john','2-john','3-john','jude','revelation']
books=rel.SLUG_TO_BOOK
PRON=re.compile(r'\b(?:he|him|his|himself)\b',re.I)
ROYAL=re.compile(r'\b(?:king|kings|kingdom|kingdoms|kingship|kingly)\b',re.I)
DIV=re.compile(r'\b(?:God|Elohim|YHWH|Father|Creator|Most High|Almighty|Cosmic Parent|Sovereign|Heavenly Father|Holy One|Abba|Lord of Hosts)\b',re.I)
YESHUA=re.compile(r'\b(?:Yeshua|Jesus|Christ|Messiah|Son of God|Son of Man|the Son|Lamb)\b',re.I)
VERSE_PREFIX=re.compile(r'\b(?:in him|to him|through him|for him|of him|with him|himself|his will|his grace|his name|his power|his glory|his righteousness|his mercy|his judgment|his sight|he himself|he gives|he gave|he has|he is|he was)\b',re.I)
GOD_CUE=re.compile(r'\b(?:will of God|God the Father|Father of|to God|God has|God who|God is|in God|God as|God gives|God gave|God will|God made|God raised|God\x27s|Elohim|Creator|Father)\b',re.I)

def main():
    sha=rel.base.sha256(rel.EPUB)
    verses=rel.collect_verses(rel.EPUB,slugs=tuple(nt))
    rows=[]
    for slug in nt:
        keys=sorted((key for key in verses if key[0]==slug),key=lambda k:(k[1],k[2]))
        for i,key in enumerate(keys):
            s=verses[key]
            pron=[m.group() for m in PRON.finditer(s)]
            royal=[m.group() for m in ROYAL.finditer(s)]
            if not pron and not royal: continue
            prev=verses[keys[i-1]] if i else ''
            nxt=verses[keys[i+1]] if i+1<len(keys) else ''
            current_div=bool(DIV.search(s))
            surrounding_div=bool(DIV.search(prev) or DIV.search(nxt))
            yes=bool(YESHUA.search(s))
            score=(4 if (pron and current_div) else 0)+(2 if (pron and surrounding_div) else 0)
            score+= (2 if pron and GOD_CUE.search(s) else 0)+(1 if pron and VERSE_PREFIX.search(s) else 0)
            score-= 1 if yes else 0
            if key==('1-peter',4,19): score+=10
            if royal and current_div: score+=2
            if royal and surrounding_div:score+=1
            rows.append({
              'ref':f'{books[slug]} {key[1]}:{key[2]}','book':books[slug],
              'chapter':key[1],'verse':key[2],
              'text':s,'previous':prev,'next':nxt,
              'masculinePronouns':pron,'royalTokens':royal,'divineInVerse':current_div,
              'divineAdjacent':surrounding_div,'yeshuaInVerse':yes,'triageScore':score
            })
    prioritized=sorted((r for r in rows if r['masculinePronouns']),key=lambda r:(-r['triageScore'],r['book'],r['chapter'],r['verse']))
    royals=[r for r in rows if r['royalTokens']]
    stats={
      'newTestamentVersesScanned':len(verses),'canonicalEpubSha256':sha,
      'versesWithMasculinePronouns':len(prioritized),
      'pronounVersesWithDivineNameInSameVerse':sum(r['divineInVerse'] for r in prioritized),
      'pronounVersesDivineNameWithinOneVerse':sum(r['divineAdjacent'] for r in prioritized),
      'pronounVersesHighTriageScore6Plus':sum(r['triageScore']>=6 for r in prioritized),
      'versesWithRoyalTokens':len(royals),
      'royalVersesWithDivineNameInSameVerse':sum(r['divineInVerse'] for r in royals),
      'totalRoyalTokens':sum(len(r['royalTokens']) for r in royals)
    }
    data={'scope':'Full New Testament 27 books, candidate discovery not replacement authority',
      'rules':'Retain Yeshua and concrete male referents; God/Father pronouns require contextual proof; kingdom->reign only when active divine rule.',
      'summary':stats,'allPronounCandidates':prioritized,'allRoyalCandidates':royals}
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    md=['# New Testament divine masculine and royal residue candidate audit — 2026-10-12',
      '', 'No blanket replacements. Every row is a CANDIDATE requiring referent determination.',
      '',json.dumps(stats,indent=2),'',
      '## Highest priority pronoun candidates (score 6+; still includes Yeshua and human false positives)','']
    for r in prioritized:
        if r['triageScore']<6:break
        md.append(f"- **{r['ref']}** (score {r['triageScore']}): {r['text']}")
    md+=['','## Royal-language candidates with explicit same-verse divine term','']
    for r in royals:
        if r['divineInVerse']: md.append(f"- {r['ref']}: {r['text']}")
    md+=['','## Review method','Treat the entire paragraph and preceding/following verses as context. Classify each masculine referent as God/Father, Yeshua (retain), other concrete male (retain), generic person, ambiguous, or quotation. Separately review every kingdom token: divine reign versus geopolitical kingdom. All candidates and neighbor contexts appear in the JSON report.']
    INDEX.write_text('\n'.join(md)+'\n',encoding='utf-8')
    print(json.dumps(stats,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
