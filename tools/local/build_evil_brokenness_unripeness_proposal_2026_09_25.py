#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / 'tools' / 'local' / 'generated_evil_inventory_2026_09_25.tsv'
OUT = ROOT / 'tools' / 'local' / 'proposed_evil_brokenness_unripeness_2026_09_25.tsv'
REPORT = ROOT / 'change-logs' / 'reports' / '2026-09-25-evil-brokenness-unripeness-proposal.json'
NOTE = ROOT / 'editor-notes' / 'consistency' / '2026-09-25-evil-brokenness-unripeness-audit.md'
CANONICAL_SHA = 'edd3182ff57b54471505189628b82238c85d2d9c8b4edbba14339695eac827cd'

# First-pass editorial recommendations only. These do not modify Scripture.
# Most rows restore the project's conceptual vocabulary; contextual alternatives
# are used where the Hebrew semantic range is adverse event/harm or where a
# direct abstract-noun restoration would be poor English.
GROUPS = {
'brokenness': [
'Genesis 2:9','Genesis 2:17','Genesis 3:5','Genesis 3:22','Genesis 6:5','Genesis 8:21',
'Deuteronomy 1:39','Deuteronomy 13:5','Deuteronomy 17:7','Deuteronomy 17:12','Deuteronomy 19:19','Deuteronomy 19:20','Deuteronomy 21:21','Deuteronomy 22:21','Deuteronomy 22:22','Deuteronomy 22:24','Deuteronomy 24:7','Deuteronomy 30:15','Deuteronomy 31:18',
'Judges 20:13','1 Samuel 12:19','1 Samuel 12:20','1 Kings 3:9','1 Kings 16:7','Nehemiah 13:27',
'Psalms 36:4','Psalms 37:8','Psalms 50:19','Psalms 52:3','Psalms 97:10','Psalms 101:4',
'Proverbs 2:12','Proverbs 2:14','Proverbs 8:13','Proverbs 11:19','Proverbs 11:27','Proverbs 12:21','Proverbs 14:16','Proverbs 15:28','Proverbs 16:30','Proverbs 20:30','Proverbs 21:10',
'Isaiah 7:15','Isaiah 7:16','Isaiah 13:11','Isaiah 33:15','Jeremiah 2:13','Jeremiah 11:17','Amos 5:14','Amos 5:15','Habakkuk 1:13'
],
'harm': [
'Genesis 44:4','1 Samuel 6:9','1 Samuel 24:17','1 Samuel 25:21','1 Samuel 25:26','2 Kings 8:12',
'Psalms 7:4','Psalms 15:3','Psalms 23:4','Psalms 35:12','Psalms 38:20','Psalms 54:5','Psalms 56:5','Psalms 74:3','Psalms 91:10',
'Proverbs 1:16','Proverbs 20:22','Isaiah 59:7','Jeremiah 18:20','Jeremiah 44:11','Jeremiah 51:24','Ezekiel 6:10','Habakkuk 2:9','Zephaniah 3:15'
],
'wrong': ['2 Samuel 12:9','2 Kings 21:9','Nehemiah 13:7','Psalms 51:4','Isaiah 56:2','Micah 7:3','Malachi 2:17'],
'wrongdoing': ['1 Samuel 24:11','Proverbs 20:8'],
'wrongly': ['Numbers 11:1'],
'defective': ['Deuteronomy 17:1'],
'adversity': ['Job 30:26','Psalms 37:19','Psalms 90:15'],
'trouble': ['Psalms 41:1','Psalms 49:5','Jeremiah 15:11','Jeremiah 17:17','Jeremiah 44:17'],
'calamity': ['Job 31:29','2 Chronicles 7:22','Psalms 140:11','Proverbs 16:4'],
'disaster': ['1 Kings 22:8','1 Kings 22:18','2 Chronicles 18:7','2 Chronicles 18:17','Jeremiah 1:14','Jeremiah 4:6','Jeremiah 4:15','Jeremiah 5:12','Jeremiah 17:18','Jeremiah 44:2'],
'harmful': ['Psalms 64:5','Psalms 140:8','Jeremiah 42:6'],
'destruction': ['Psalms 78:49'],
'broken': ['Proverbs 15:3','Isaiah 32:7','Micah 3:4'],
}

# Rows requiring more than a single one-word replacement, or multiple distinct
# replacements in the same verse.
SPECIAL = {
'Psalms 5:4': [('evil', 'Brokenness')],
'Psalms 34:21': [('evil', 'Brokenness')],
'Proverbs 17:13': [('evil', 'harm'), ('evil', 'harm')],
'Isaiah 5:20': [('evil', 'brokenness'), ('evil', 'brokenness')],
'Jeremiah 18:8': [('evil', 'brokenness'), ('evil', 'harm')],
'Ezekiel 6:11': [('evil abominations', 'broken acts')],
'Ezekiel 38:10': [('an evil plan', 'a harmful plan')],
'Zechariah 1:4': [('evil doings', 'broken actions')],
'Malachi 1:8': [('evil', 'wrong'), ('evil', 'wrong')],
}

EXTRA_GRAMMAR = {
'Malachi 2:17': [('they delights', 'they delight')],
}


def build_replacements():
    out={}
    for target, refs in GROUPS.items():
        for ref in refs:
            if ref in out or ref in SPECIAL:
                raise RuntimeError(f'duplicate proposal reference: {ref}')
            out[ref]=[('evil',target)]
    out.update(SPECIAL)
    return out

REPLACEMENTS=build_replacements()


def rationale_for(repls):
    targets=' '.join(new.lower() for _old,new in repls)
    if 'brokenness' in targets:
        return 'Conceptual/moral abstract noun: restore brokenness where it is grammatical and preserves the project’s intended contrast.'
    if 'broken' in targets:
        return 'Adjectival/predicate context: use broken rather than the ungrammatical noun modifier brokenness.'
    if any(x in targets for x in ['harm','harmful','calamity','disaster','adversity','trouble','destruction']):
        return 'Adverse-event or injury context: use a concrete harm/adversity term instead of the abstract label evil.'
    if any(x in targets for x in ['wrong','wrongdoing','wrongly']):
        return 'Action/predicate context: use grammatical, concrete wrong/wrongdoing wording rather than the abstract label evil.'
    if 'defective' in targets:
        return 'Physical sacrificial-defect context: defective is more precise than a moral abstraction.'
    return 'Context-specific replacement avoids the blanket word evil while preserving the verse’s sense.'


def apply_exact(text, repls, ref):
    out=text
    for old,new in repls:
        if old not in out:
            raise RuntimeError(f'{ref}: expected phrase not found: {old!r}')
        out=out.replace(old,new,1)
    return out


def qa(text):
    issues=[]
    if re.search(r'\bevil\b', text, re.I): issues.append('evil-residual')
    if re.search(r'\b(?:an\s+(?:broken|harmful|defective)|a\s+(?:adversity|evil|unripe)|anything\s+brokenness)\b', text, re.I): issues.append('article-or-form')
    if re.search(r'\bbrokenness\s+(?:plans?|ways?|actions?|doings?|abominations?|devices?)\b', text, re.I): issues.append('noun-used-as-adjective')
    if re.search(r'(^|[.!?][\"”\'’)]*\s+)(?:brokenness|harm|calamity|disaster|adversity|trouble|wrongdoing|destruction)\b', text): issues.append('sentence-initial-lowercase')
    if '  ' in text: issues.append('double-space')
    if re.search(r'\s+[,.!?;:]', text): issues.append('space-before-punctuation')
    if re.search(r'\bthey\s+(?:delights|is|was|has|does)\b', text, re.I): issues.append('subject-verb-agreement')
    return issues


def main():
    with INVENTORY.open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f,delimiter='\t'))
    refs=[r['reference'] for r in rows]
    if len(rows)!=124 or len(refs)!=len(set(refs)):
        raise RuntimeError(f'inventory shape mismatch rows={len(rows)} unique={len(set(refs))}')
    missing=sorted(set(refs)-set(REPLACEMENTS))
    extra=sorted(set(REPLACEMENTS)-set(refs))
    if missing or extra:
        raise RuntimeError(f'proposal coverage mismatch missing={missing} extra={extra}')

    proposed=[]
    target_counts=Counter()
    context_counts=Counter()
    for row in rows:
        ref=row['reference']
        repls=REPLACEMENTS[ref]
        text=apply_exact(row['current_text'],repls,ref)
        grammar_note=''
        for old,new in EXTRA_GRAMMAR.get(ref,[]):
            if old not in text: raise RuntimeError(f'{ref}: adjacent grammar phrase not found: {old!r}')
            text=text.replace(old,new,1)
            grammar_note=f'Also correct adjacent agreement: {old!r} → {new!r}.'
        issues=qa(text)
        if issues:
            raise RuntimeError(f'{ref}: proposal QA failed: {issues}: {text}')
        for _old,new in repls:
            normalized=new.lower()
            if 'brokenness' in normalized: target_counts['brokenness']+=1
            elif re.search(r'\bbroken\b',normalized): target_counts['broken']+=1
            elif 'wrong' in normalized: target_counts['wrong/wrongdoing']+=1
            elif 'harm' in normalized: target_counts['harm/harmful']+=1
            elif normalized in {'adversity','trouble','calamity','disaster','destruction'}: target_counts[normalized]+=1
            elif 'defective' in normalized: target_counts['defective']+=1
            else: target_counts[normalized]+=1
        rationale=rationale_for(repls)
        if 'Conceptual/moral' in rationale: context_counts['moral/conceptual']+=1
        elif 'Adjectival' in rationale: context_counts['adjectival broken']+=1
        elif 'Adverse-event' in rationale: context_counts['harm/adversity']+=1
        elif 'Action/predicate' in rationale: context_counts['wrong/action']+=1
        else: context_counts['other contextual']+=1
        proposed.append({
            'reference':ref,
            'testament':row['testament'],
            'current_verse':row['current_text'],
            'change_evil':'YES',
            'proposed_form':' | '.join(new for _old,new in repls),
            'proposed_verse':text,
            'semantic_rationale':rationale,
            'grammar_check':'PASS',
            'capitalization_check':'PASS',
            'spacing_punctuation_check':'PASS',
            'historical_pre_cleanup_text':row['historical_pre_cleanup_text'],
            'reviewed':'☐',
            'approved':'☐',
            'editor_notes':grammar_note,
        })

    fields=['reference','testament','current_verse','change_evil','proposed_form','proposed_verse','semantic_rationale','grammar_check','capitalization_check','spacing_punctuation_check','historical_pre_cleanup_text','reviewed','approved','editor_notes']
    with OUT.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(proposed)

    report={
        'status':'PROPOSAL ONLY — non-canonical until explicit editorial approval',
        'canonicalEpubSha256':CANONICAL_SHA,
        'inventoryVerseCount':124,
        'proposedChangeYes':124,
        'proposedChangeNo':0,
        'remainingEvilInProposedVerses':0,
        'proposalTargetCounts':dict(target_counts),
        'semanticClassCounts':dict(context_counts),
        'qa':{
            'grammar':'PASS for all 124 proposed verses',
            'capitalization':'PASS for all 124 proposed verses; Psalm 5:4 and Psalm 34:21 corrected',
            'spacingPunctuation':'PASS for replacement-induced spacing/punctuation regressions',
            'articleAgreement':'PASS, including a/an checks around replacement terms',
            'adjacentGrammarCorrections':['Malachi 2:17: they delights → they delight'],
        },
        'reviewState':{'reviewed':0,'approved':0,'checkboxMeaning':'Rows remain unchecked until human editorial review.'},
        'policy':'Finite exact-verse proposal derived from the current canonical EPUB and the 2026-09-14 historical cleanup ledger. No blanket search/replace is authorized. Brokenness is used as the project’s conceptual abstract noun where grammatical; broken is used where an adjective is required; concrete harm/adversity/wrong wording is preferred where the context is an event, injury, judgment, or action. Unripe/unripeness remains an allowed project concept but is not forced where it would make these 124 English verses less natural.',
        'proposalTsv':str(OUT.relative_to(ROOT)),
    }
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    NOTE.parent.mkdir(parents=True,exist_ok=True)
    NOTE.write_text(f'''# Whole-Bible `evil` → brokenness / contextual-language audit — proposal only\n\n**Status:** non-canonical proposal. Do not sync this file downstream and do not modify the canonical EPUB until the individual rows are explicitly reviewed and approved.\n\n**Canonical baseline EPUB SHA-256:** `{CANONICAL_SHA}`\n\n## Scope\n\n- Exact extraction of all 31,102 canonical verses found 124 verses containing the standalone English word `evil`.\n- All 124 are in the Old Testament.\n- All 124 were introduced or retained by the 2026-09-14 audited `brokenness` cleanup ledger.\n- The current New Testament contains zero standalone `evil` verses.\n- This proposal recommends changing all 124, but **not** by one global replacement.\n\n## Editorial rule\n\nUse `brokenness` where the verse needs the project’s abstract moral/conceptual noun. Use `broken` where English grammar needs an adjective or predicate adjective. Use concrete contextual language such as `harm`, `wrong`, `wrongdoing`, `adversity`, `trouble`, `calamity`, or `disaster` where the verse is describing injury, an adverse event, judgment, or an action rather than an abstract moral category. `Unripe` / `unripeness` remain available concepts for later row-level editorial review, but this first pass does not force them into contexts where the English becomes less natural.\n\n## QA gates for eventual approval\n\nEvery approved row must pass all of these before release:\n\n1. Exact before/after verse match against the canonical baseline.\n2. No unapproved global substitution.\n3. Sentence-initial capitalization after `.`, `?`, `!`, quotation marks, or parentheses.\n4. Article/form agreement (`a`/`an`, noun vs adjective), including guards against forms such as `brokenness plans`.\n5. No doubled spaces, spaces before punctuation, or replacement-induced punctuation damage.\n6. Whole-Bible 66-book / 1,189-chapter / 31,102-verse inventory unchanged.\n7. EPUB ZIP, XML, internal-link, and anchor validation unchanged from the normal release methodology.\n8. Regenerate the public mobile fallback and all downstream reader/search/name-linking content from the finished canonical EPUB only after approval.\n\n## Known grammar regressions addressed in the proposal\n\n- Psalm 5:4: sentence-initial lowercase `evil` → `Brokenness`.\n- Psalm 34:21: verse-initial lowercase `evil` → `Brokenness`.\n- Ezekiel 38:10: `an evil plan` → `a harmful plan` (article agreement).\n- Malachi 2:17: adjacent `they delights` → `they delight` so the proposed verse is grammatically clean.\n\nThe row-by-row ledger is `{OUT.relative_to(ROOT).as_posix()}`. `reviewed` and `approved` are intentionally unchecked for every row.\n''',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
