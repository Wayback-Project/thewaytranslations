#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
AUD=ROOT/'audit-output'/'old-testament-gender-brokenness-2026-09-14'
CANDS=AUD/'candidates.tsv'
OUT=AUD/'proposed-cleanup.tsv'
SUMMARY=AUD/'proposed-cleanup-summary.json'

DIV_RE=re.compile(r'\b(?:YHWH|Elohim|God|Yah|El Shaddai|Elyon|Most High|Almighty|Creator)\b')
# Names/titles that make a global generic-pronoun rewrite unsafe in the verse.
PROPER_RE=re.compile(r"\b(?:Adam|Havvah|Qayin|Hevel|Lamech|Noach|Avram|Avraham|Sarai|Sarah|Hagar|Yishmael|Yitzhak|Yaakov|Yosef|Moshe|Aharon|Miriam|Yehoshua|Caleb|Pharaoh|Dawid|Shlomo|Shaul|Yonah|Yirmeyahu|Yehezkel|Daniel|Iyov|Eliyahu|Elisha|Mordekhai|Esther|Haman|Achav|Menashe|Chizkiyahu|Yehoshafat|Yerovam|Gid.?on)\b")
SEX_SPECIFIC_RE=re.compile(r'\b(?:father|mother|son|daughter|brother|sister|husband|wife|male|female|king|queen|prince|princess|virgin|eunuch)\b',re.I)
MASC_PRON_RE=re.compile(r'\b(?:he|him|his|himself)\b',re.I)

SPECIAL_LEXICAL={
'Genesis 8:21': [('the human heart is brokenness from youth','the human heart inclines toward evil from youth')],
'Genesis 19:19': [('lest brokenness overtake me','lest disaster overtake me')],
'Genesis 37:20': [('A brokenness animal','A wild animal')],
'Genesis 37:33': [('A brokenness animal','A wild animal')],
'Genesis 38:10': [('was brokenness in YHWH’s sight','was wrong in YHWH’s sight')],
'Genesis 44:5': [('done brokenness','done wrong')],
'Genesis 44:34': [('the brokenness that will come on my father','the harm that will come on my father')],
'Genesis 47:9': [('have been few and brokenness','have been few and difficult')],
'Genesis 48:16': [('redeemed me from all brokenness','redeemed me from all harm')],
'Genesis 50:15': [('all the brokenness which we did to him','all the wrong we did to him')],
'Genesis 50:17': [('they did brokenness to you','they did wrong to you')],
'Genesis 50:20': [('you meant brokenness against me','you intended harm against me')],
'Exodus 10:10': [('brokenness is clearly before your faces','trouble is clearly before you')],
'Exodus 23:2': [('to do brokenness','to do wrong')],
'Exodus 32:12': [('for brokenness, to kill them','for harm, to kill them'),('relent from this brokenness against your people','relent from this harm against your people')],
'Exodus 32:22': [('set on brokenness','bent on wrongdoing')],
'Exodus 33:4': [('brokenness news','bad news')],
'Leviticus 5:4': [('to do brokenness, or to do good','to do harm, or to do good')],
'Leviticus 26:6': [('brokenness animals','dangerous animals')],
'Numbers 14:27': [('brokenness congregation','rebellious congregation')],
'Numbers 14:35': [('brokenness congregation','rebellious congregation')],
'Numbers 20:5': [('this brokenness place','this barren place')],
'Numbers 32:13': [('done brokenness in the sight of YHWH','done wrong in the sight of YHWH')],
'Nehemiah 2:17': [('the brokenness case that we are in','the trouble that we are in')],
'Proverbs 9:7': [('broken person','wicked person')],
'Proverbs 11:7': [('broken person','wicked person')],
'Proverbs 11:21': [('brokenness man','wicked person')],
'Proverbs 12:12': [('brokenness men','wicked people')],
'Proverbs 12:13': [('A brokenness a person','A wicked person')],
'Proverbs 13:5': [('broken person','wicked person')],
'Proverbs 14:19': [('The brokenness bow down','Those who do wrong bow down')],
'Proverbs 17:4': [('An one who acts from brokenness','One who does wrong')],
'Proverbs 17:11': [('A brokenness man','A wicked person')],
'Proverbs 17:23': [('A broken person','A wicked person')],
'Proverbs 21:29': [('A broken person','A wicked person')],
'Proverbs 24:1': [('brokenness men','wicked people')],
'Proverbs 24:15': [('broken person','wicked person')],
'Proverbs 24:19': [('people who act from brokenness','people who do wrong')],
'Proverbs 24:20': [('brokenness man','wicked person')],
'Proverbs 26:24': [('harbors brokenness','harbors deceit')],
'Proverbs 28:5': [("Brokenness men don't understand justice","People who do wrong don't understand justice")],
'Proverbs 29:6': [('A brokenness a person is snared by their sin','A wicked person is snared by their sin')],
'Isaiah 1:4': [('a seed of people who act from brokenness','offspring of people who do wrong')],
'Isaiah 1:13': [("I can't bear with brokenness assemblies","I can't bear wrongdoing together with solemn assembly")],
'Isaiah 9:17': [('an one who acts from brokenness','one who does wrong')],
'Jeremiah 49:23': [('heard brokenness news','heard bad news')],
'Psalms 109:5': [('rewarded me brokenness for good','repaid me harm for good')],
'Psalms 109:6': [('Set a broken person over him','Set a wicked person over him')],
'Psalms 112:7': [('brokenness news','bad news')],
'Psalms 119:115': [('people who act from brokenness','people who do wrong')],
}

# Common malformed artifacts from the earlier broad AI lexical replacement.
PHRASE_RULES=[
(r'\bbrokenness men\b','wicked people'),
(r'\bbrokenness man\b','wicked person'),
(r'\bbroken person\b','wicked person'),
(r'\bbroken people\b','wicked people'),
(r'\bbroken deeds\b','wrong deeds'),
(r'\bpeople who act from brokenness\b','people who do wrong'),
(r'\bone who acts from brokenness\b','one who does wrong'),
(r'\bthe one who acts from brokenness\b','the one who does wrong'),
(r'\bbrokenness news\b','bad news'),
(r'\bbrokenness report\b','bad report'),
(r'\bbrokenness reports\b','bad reports'),
(r'\bbrokenness tidings\b','bad news'),
(r'\bbrokenness odor\b','foul odor'),
(r'\bbrokenness way\b','wrong way'),
(r'\bbroken ways\b','wrong ways'),
(r'\bbroken way\b','wrong way'),
(r'\bdo brokenness\b','do wrong'),
(r'\bdid brokenness\b','did wrong'),
(r'\bdone brokenness\b','done wrong'),
(r'\bdoing brokenness\b','doing wrong'),
(r'\bwork brokenness\b','do wrong'),
(r'\bworks brokenness\b','does wrong'),
(r'\bworked much brokenness\b','did much wrong'),
(r'\bplot brokenness\b','plot harm'),
(r'\bplots brokenness\b','plots harm'),
(r'\bplotted brokenness\b','plotted harm'),
(r'\bdevise brokenness\b','devise harm'),
(r'\bdevises brokenness\b','devises harm'),
(r'\bdevised brokenness\b','devised harm'),
(r'\bthought brokenness\b','planned harm'),
(r'\bset on brokenness\b','bent on wrongdoing'),
(r'\bbrokenness assemblies\b','wrongdoing and solemn assembly'),
]

# References where the moral good/evil contrast is itself the clearest lexical value.
GOOD_EVIL_REFS={
'Genesis 2:9','Genesis 2:17','Genesis 3:5','Genesis 3:22','Deuteronomy 1:39',
'Isaiah 5:20','Isaiah 7:15','Isaiah 7:16','Jeremiah 42:6','Ecclesiastes 12:14'
}

GENERIC_START=re.compile(r'(?i)\b(?:if|when|whenever)?\s*(?:anyone|someone|whoever|everyone|no one|a person|the person|one who|the one who)\b')
PRON_MAP={'he':'they','He':'They','HE':'THEY','him':'them','Him':'Them','HIM':'THEM','his':'their','His':'Their','HIS':'THEIR','himself':'themselves','Himself':'Themselves','HIMSELF':'THEMSELVES'}


def lexical_fix(ref,text):
    out=text
    for a,b in SPECIAL_LEXICAL.get(ref,[]): out=out.replace(a,b)
    for pat,repl in PHRASE_RULES: out=re.sub(pat,repl,out,flags=re.I)
    if ref in GOOD_EVIL_REFS:
        out=out.replace('brokenness','evil')
    # Contextual fallbacks before the final legacy-safe fallback.
    out=re.sub(r'\bthe brokenness of (?:your|their|his|her|our) doings\b',lambda m:'the wrongdoing in '+m.group(0).split(' of ',1)[1],out,flags=re.I)
    out=re.sub(r'\bbrokenness of (?:your|their|his|her|our) doings\b',lambda m:'wrongdoing in '+m.group(0).split(' of ',1)[1],out,flags=re.I)
    out=re.sub(r'\b(?:great )?brokenness that (?:I|YHWH|God|Elohim) (?:will|would|have) bring\b',lambda m:m.group(0).replace('brokenness','calamity'),out,flags=re.I)
    out=re.sub(r'\bbrokenness (?:shall|will|would|may) come on\b',lambda m:m.group(0).replace('brokenness','trouble'),out,flags=re.I)
    out=re.sub(r'\bbrokenness (?:has|had) come (?:on|upon|down)\b',lambda m:m.group(0).replace('brokenness','trouble'),out,flags=re.I)
    out=re.sub(r'\bbring(?:ing)? (?:all |such |this |great )?brokenness on\b',lambda m:m.group(0).replace('brokenness','calamity'),out,flags=re.I)
    out=re.sub(r'\bfrom all brokenness\b','from all harm',out,flags=re.I)
    out=re.sub(r'\bbrokenness against\b','harm against',out,flags=re.I)
    out=re.sub(r'\bbrokenness in (?:the )?(?:sight|eyes) of YHWH\b','wrong in the sight of YHWH',out,flags=re.I)
    out=re.sub(r'\bthat which is brokenness in (?:my|YHWH’s|YHWH\'s) sight\b','what is wrong in my sight',out,flags=re.I)
    # Any remaining occurrence came from the legacy evil->brokenness AI substitution.
    # Restore the attested pre-AI lexical value rather than inventing a new meaning.
    out=re.sub(r'\bbrokenness\b','evil',out,flags=re.I)
    return out


def neutralize_generic_pronouns(text):
    # Conservative verse-level transform: only formulaically generic verses with no
    # named person, no divine marker, and no sex-specific role whose gender matters.
    if not GENERIC_START.search(text): return text
    if DIV_RE.search(text) or PROPER_RE.search(text) or SEX_SPECIFIC_RE.search(text): return text
    out=text
    for src,dst in PRON_MAP.items(): out=re.sub(rf'\b{re.escape(src)}\b',dst,out)
    # agreement repairs created by singular-they conversion
    repairs=[
      (r'\bthey is\b','they are'),(r'\bThey is\b','They are'),
      (r'\bthey has\b','they have'),(r'\bThey has\b','They have'),
      (r'\bthey does\b','they do'),(r'\bThey does\b','They do'),
      (r'\bthey was\b','they were'),(r'\bThey was\b','They were'),
      (r'\bthey goes\b','they go'),(r'\bThey goes\b','They go'),
      (r'\bthey comes\b','they come'),(r'\bThey comes\b','They come'),
      (r'\bthey knows\b','they know'),(r'\bThey knows\b','They know'),
      (r'\bthey gives\b','they give'),(r'\bThey gives\b','They give'),
      (r'\bthey takes\b','they take'),(r'\bThey takes\b','They take'),
      (r'\bthey makes\b','they make'),(r'\bThey makes\b','They make'),
      (r'\bthey says\b','they say'),(r'\bThey says\b','They say'),
    ]
    for a,b in repairs: out=re.sub(a,b,out)
    return out


def generic_human_fix(text):
    rules=[
      (r'\bmankind\b','humanity'),(r'\bMankind\b','Humanity'),
      (r'\ball men\b','all people'),(r'\bAll men\b','All people'),
      (r'\bmen who\b','people who'),(r'\bMen who\b','People who'),
      (r'\ba man who\b','a person who'),(r'\bA man who\b','A person who'),
      (r'\bthe man who\b','the person who'),(r'\bThe man who\b','The person who'),
      (r'\bno man\b','no one'),(r'\bNo man\b','No one'),
      (r'\bevery man\b','everyone'),(r'\bEvery man\b','Everyone'),
      (r'\beach man\b','each person'),(r'\bEach man\b','Each person'),
      (r'\bany man\b','anyone'),(r'\bAny man\b','Anyone'),
    ]
    out=text
    for a,b in rules: out=re.sub(a,b,out)
    return out


def divine_fix(text,signals):
    # Very conservative: only devotion-object rows, or clear sentence-initial divine
    # subjects, and only when no named person/sex-specific human role competes.
    if PROPER_RE.search(text) or SEX_SPECIFIC_RE.search(text): return text
    out=text
    if 'devotion-object' in signals:
        # choose the closest established divine name before the devotion phrase
        pat=re.compile(r'(?P<d>YHWH|Elohim|God|Yah|Most High|Almighty|Creator)(?P<m>[^.!?]{0,180}?)(?P<v>serve|seek|follow|revere|fear|worship|trust|wait for|call on|pray to|praise|exalt|obey|return to) (?P<p>him|his|himself)\b',re.I)
        def repl(m):
            d=m.group('d'); p=m.group('p').lower()
            poss=(d+"'s") if p=='his' else d
            return d+m.group('m')+m.group('v')+' '+poss
        out=pat.sub(repl,out)
    if 'next-sentence-divine-subject' in signals:
        # Only when a sentence itself starts with a divine title/name and the next
        # sentence begins He/His; this avoids the serpent-style proximity false positive.
        pat=re.compile(r'(?P<s>\b(?:YHWH|Elohim|God|Yah|Most High|Almighty|Creator)\b[^.!?]{0,120}[.!?]\s*[“\"\']?)(?P<p>He|His)\b')
        def repl2(m):
            # repeat the first divine marker in the preceding sentence
            dm=DIV_RE.search(m.group('s')); d=dm.group(0) if dm else 'YHWH'
            return m.group('s') + (d+"'s" if m.group('p')=='His' else d)
        out=pat.sub(repl2,out)
    return out


def main():
    rows=[]
    with CANDS.open(encoding='utf-8',newline='') as f:
        cands=list(csv.DictReader(f,delimiter='\t'))
    byref=defaultdict(list)
    for r in cands: byref[r['reference']].append(r)
    for ref,rs in byref.items():
        before=rs[0]['text']; after=before; cats=[]
        if any(r['category']=='BROKENNESS LEXICAL REVIEW' for r in rs):
            n=lexical_fix(ref,after)
            if n!=after: cats.append('lexical'); after=n
        if any(r['category']=='GENERIC-HUMAN HIGH PRIORITY' for r in rs):
            n=generic_human_fix(after)
            if n!=after: cats.append('generic-human'); after=n
        if any(r['category']=='GENERIC PRONOUN HIGH PRIORITY' for r in rs):
            n=neutralize_generic_pronouns(after)
            if n!=after: cats.append('generic-pronoun'); after=n
        divrows=[r for r in rs if r['category']=='DIVINE-REFERENT REVIEW']
        if divrows:
            sig=';'.join(r['signals'] for r in divrows)
            n=divine_fix(after,sig)
            if n!=after: cats.append('divine'); after=n
        if after!=before:
            book=rs[0]['book']; ch=int(rs[0]['chapter']); vs=int(rs[0]['verse'])
            rows.append({'reference':ref,'book':book,'chapter':ch,'verse':vs,'categories':','.join(cats),'before':before,'after':after})
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('w',encoding='utf-8',newline='') as f:
        fields=['reference','book','chapter','verse','categories','before','after']
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)
    counts=Counter()
    books=Counter()
    for r in rows:
        for c in r['categories'].split(','): counts[c]+=1
        books[r['book']]+=1
    summary={'proposedVerseChanges':len(rows),'categoryCounts':dict(counts),'bookCounts':dict(books),'rules':'Conservative proposal only. Lexical rows use contextual rules plus legacy-safe evil fallback; generic pronouns require formulaic generic antecedent and exclude divine/named/sex-specific verses; divine changes are restricted to devotion-object or sentence-start divine patterns with human distractor exclusions.'}
    SUMMARY.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
