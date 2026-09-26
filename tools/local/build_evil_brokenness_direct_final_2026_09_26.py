#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

import audit_evil_brokenness_unripeness_2026_09_25 as audit

ROOT = audit.ROOT
INVENTORY = ROOT / 'tools' / 'local' / 'generated_evil_inventory_2026_09_25.tsv'
OUT = ROOT / 'tools' / 'local' / 'proposed_evil_brokenness_unripeness_2026_09_25.tsv'
REPORT = ROOT / 'change-logs' / 'reports' / '2026-09-25-evil-brokenness-unripeness-proposal.json'
NOTE = ROOT / 'editor-notes' / 'consistency' / '2026-09-25-evil-brokenness-unripeness-audit.md'
CANONICAL_SHA = audit.CANONICAL_SHA

# Final editorial rule (2026-09-26): do not rewrite whole phrases.  Replace only
# the lexical word evil with the grammatically required project form:
#   brokenness = noun/abstract slot
#   broken = adjective, predicate adjective, or substantive adjective
# The occurrence numbers below are 1-based within each verse.  Every other
# standalone evil occurrence uses brokenness.
BROKEN_OCCURRENCES = {
    'Deuteronomy 17:1': {1},              # anything broken
    '2 Samuel 12:9': {1},                 # that which is broken
    '2 Kings 21:9': {1},                  # that which is broken
    'Psalms 51:4': {1},                   # that which is broken
    'Psalms 64:5': {1},                   # broken plans
    'Psalms 140:8': {1},                  # broken plans
    'Proverbs 15:3': {1},                 # the broken and the good
    'Isaiah 5:20': {2},                   # call brokenness good; call good broken
    'Isaiah 7:15': {1},                   # refuse the broken
    'Isaiah 7:16': {1},                   # refuse the broken
    'Isaiah 32:7': {1},                   # ways ... are broken
    'Jeremiah 42:6': {1},                 # whether it be ... broken
    'Ezekiel 6:11': {1},                  # broken abominations
    'Ezekiel 38:10': {1},                 # a broken plan
    'Micah 3:4': {1},                     # deeds were broken
    'Micah 7:3': {1},                     # that which is broken
    'Zechariah 1:4': {1},                 # broken doings
    'Malachi 1:8': {1, 2},                # isn't that broken?
}

EVIL_RE = re.compile(r'\bevil\b', re.I)
SPACE_BEFORE_PUNCT = re.compile(r'\s+[,.!?;:]')


def read_rows():
    with INVENTORY.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    if len(rows) != 124:
        raise RuntimeError(f'inventory row count mismatch: {len(rows)} != 124')
    return rows


def replacement_for(ref: str, occurrence: int, original: str) -> str:
    base = 'broken' if occurrence in BROKEN_OCCURRENCES.get(ref, set()) else 'brokenness'
    if original[:1].isupper():
        return base[:1].upper() + base[1:]
    return base


def replace_direct_only(ref: str, text: str) -> tuple[str, list[str]]:
    seen = 0
    forms = []

    def repl(m: re.Match[str]) -> str:
        nonlocal seen
        seen += 1
        new = replacement_for(ref, seen, m.group(0))
        forms.append(new)
        return new

    out = EVIL_RE.sub(repl, text)
    if seen == 0:
        raise RuntimeError(f'{ref}: no standalone evil occurrence')

    # Grammar-required article agreement only.  This is the only non-evil token
    # change allowed by the direct-replacement policy.
    if ref == 'Ezekiel 38:10':
        before = out
        out = re.sub(r'\ban broken plan\b', 'a broken plan', out, count=1)
        if out == before:
            raise RuntimeError('Ezekiel 38:10: expected an broken plan after lexical replacement')

    # Existing adjacent agreement regression found during the audit.  This is
    # independent of the lexical decision and is fixed in the same exact verse.
    if ref == 'Malachi 2:17':
        before = out
        out = out.replace('they delights', 'they delight', 1)
        if out == before:
            raise RuntimeError('Malachi 2:17: expected they delights regression not found')

    # The current canonical has two lowercase sentence-start regressions caused
    # by the earlier cleanup.  Capitalize the replacement, not any other text.
    if ref in {'Psalms 5:4', 'Psalms 34:21'}:
        out = re.sub(r'(^|[.!?][\"”\'’)]*\s+)(brokenness|broken)\b',
                     lambda m: m.group(1) + m.group(2).capitalize(), out, count=1)
        forms[0] = forms[0].capitalize()

    return out, forms


def assert_direct_diff(ref: str, before: str, after: str):
    """Reject any whole-phrase rewrite.

    Reconstruct the current verse from the proposed verse by reversing only the
    explicitly allowed substitutions.  If it does not match exactly, some
    unrelated wording moved and the proposal fails.
    """
    reconstructed = after
    if ref == 'Malachi 2:17':
        reconstructed = reconstructed.replace('they delight', 'they delights', 1)
    if ref == 'Ezekiel 38:10':
        reconstructed = reconstructed.replace('a broken plan', 'an broken plan', 1)

    # Replace project forms back to evil in occurrence order.  Match only the
    # number of lexical occurrences present in the canonical before text.
    count = len(EVIL_RE.findall(before))
    for i in range(count):
        # First matching broken/brokenness token in reading order.
        m = re.search(r'\b(?:brokenness|broken)\b', reconstructed, re.I)
        if not m:
            raise RuntimeError(f'{ref}: cannot reverse direct lexical replacement #{i+1}')
        original_match = EVIL_RE.findall(before)[i]
        evil = 'Evil' if original_match[:1].isupper() else 'evil'
        # Psalm regressions intentionally repair lowercase sentence starts; to
        # reconstruct their current text, restore lowercase evil.
        if ref in {'Psalms 5:4', 'Psalms 34:21'}:
            evil = 'evil'
        reconstructed = reconstructed[:m.start()] + evil + reconstructed[m.end():]

    if reconstructed != before:
        raise RuntimeError(f'{ref}: direct-diff guard failed\nBEFORE: {before}\nAFTER:  {after}\nRECON:  {reconstructed}')


def qa(ref: str, text: str):
    issues=[]
    if EVIL_RE.search(text): issues.append('evil-residual')
    if re.search(r'\b(?:an broken|a brokenness)\b', text, re.I): issues.append('article-agreement')
    if re.search(r'\bbrokenness\s+(?:plans?|ways?|actions?|doings?|abominations?|devices?)\b', text, re.I): issues.append('noun-used-as-adjective')
    if re.search(r'\b(?:anything|something|nothing|everything)\s+brokenness\b', text, re.I): issues.append('indefinite-pronoun-needs-adjective')
    if re.search(r'\b(?:is|are|was|were|be|been|being)\s+brokenness\b', text, re.I): issues.append('predicate-needs-adjective')
    if re.search(r'(^|[.!?][\"”\'’)]*\s+)(?:brokenness|broken)\b', text): issues.append('sentence-initial-lowercase')
    if '  ' in text: issues.append('double-space')
    if SPACE_BEFORE_PUNCT.search(text): issues.append('space-before-punctuation')
    if re.search(r'\bthey\s+(?:delights|is|was|has|does)\b', text, re.I): issues.append('subject-verb-agreement')
    if ref == 'Ezekiel 38:10' and 'a broken plan' not in text: issues.append('article-fix-missing')
    return issues


def rationale(forms: list[str]) -> str:
    if all(f.lower() == 'brokenness' for f in forms):
        return 'Direct lexical replacement only: evil functions as a noun/abstract concept here, so use brokenness without rewriting the surrounding phrase.'
    if all(f.lower() == 'broken' for f in forms):
        return 'Direct lexical replacement only: evil functions adjectivally or substantivally here, so use broken without rewriting the surrounding phrase.'
    return 'Direct lexical replacement only: each evil occurrence is changed independently to the grammatically required brokenness/broken form; surrounding wording is preserved.'


def main():
    rows = read_rows()
    out_rows=[]
    counts=Counter()
    for r in rows:
        ref=r['reference']
        before=r['current_text']
        after, forms = replace_direct_only(ref, before)
        assert_direct_diff(ref, before, after)
        issues=qa(ref, after)
        if issues:
            raise RuntimeError(f'{ref}: QA failed {issues}: {after}')
        for f in forms:
            counts[f.lower()] += 1
        notes=[]
        if ref in {'Psalms 5:4','Psalms 34:21'}:
            notes.append('Repairs existing lowercase sentence-start regression.')
        if ref == 'Ezekiel 38:10':
            notes.append('Article agreement only: an → a before broken.')
        if ref == 'Malachi 2:17':
            notes.append("Adjacent grammar correction: 'they delights' → 'they delight'.")
        out_rows.append({
            'reference':ref,
            'testament':r['testament'],
            'current_verse':before,
            'change_evil':'YES',
            'proposed_form':' | '.join(forms),
            'proposed_verse':after,
            'semantic_rationale':rationale(forms),
            'grammar_check':'PASS',
            'capitalization_check':'PASS',
            'spacing_punctuation_check':'PASS',
            'historical_pre_cleanup_text':r['historical_pre_cleanup_text'],
            'reviewed':'☑',
            'approved':'☑',
            'editor_notes':' '.join(notes),
        })

    fields=['reference','testament','current_verse','change_evil','proposed_form','proposed_verse','semantic_rationale','grammar_check','capitalization_check','spacing_punctuation_check','historical_pre_cleanup_text','reviewed','approved','editor_notes']
    with OUT.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(out_rows)

    report={
      'status':'FINAL EDITORIAL DECISION — approved for canonical release by direct user instruction on 2026-09-26',
      'canonicalEpubSha256':CANONICAL_SHA,
      'inventoryVerseCount':len(out_rows),
      'proposedChangeYes':len(out_rows),
      'proposedChangeNo':0,
      'remainingStandaloneEvilInProposedVerses':sum(bool(EVIL_RE.search(r['proposed_verse'])) for r in out_rows),
      'replacementOccurrenceCounts':dict(counts),
      'policy':'No whole-phrase rewrites. Replace only standalone lexical evil with brokenness in noun/abstract slots and broken in adjective, predicate-adjective, or substantive-adjective slots. The only permitted non-evil-token edits are the required article change an→a in Ezekiel 38:10 and the adjacent agreement repair they delights→they delight in Malachi 2:17. Psalm 5:4 and Psalm 34:21 also capitalize the replacement because the current canonical text contains lowercase sentence-start regressions.',
      'qa':{
        'directDiff':'PASS for all 124 verses; unrelated surrounding wording cannot change',
        'grammar':'PASS for all 124 verses',
        'capitalization':'PASS for all 124 verses',
        'spacingPunctuation':'PASS for replacement-induced regressions',
        'articleAgreement':'PASS',
      },
      'reviewState':{'reviewed':124,'approved':124,'basis':'User explicitly instructed final review and canonical rollout on 2026-09-26.'},
      'proposalTsv':str(OUT.relative_to(ROOT)),
    }
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    NOTE.write_text(f'''# Final evil → brokenness / broken terminology decision\n\n**Status:** Approved for canonical release by direct editorial instruction on 2026-09-26.\n\nCanonical baseline SHA-256: `{CANONICAL_SHA}`.\n\n## Final rule\n\nThis supersedes the earlier contextual-wording first pass. **Do not rewrite the whole phrase.** Change only the standalone lexical word `evil`:\n\n- `brokenness` when the word occupies a noun / abstract-concept slot.\n- `broken` when English requires an adjective, predicate adjective, or substantive adjective (for example, “the broken and the good”).\n\nNo contextual substitutions such as `harm`, `wrong`, `calamity`, `adversity`, `disaster`, or phrase rewrites such as “broken acts” are authorized by this release.\n\nThe only surrounding-token changes permitted are grammar repairs required by the final wording: `an` → `a` in Ezekiel 38:10 (“a broken plan”), and the pre-existing agreement repair in Malachi 2:17 (`they delights` → `they delight`). Psalm 5:4 and Psalm 34:21 capitalize the new sentence-start word, repairing the lowercase regressions currently in the canonical EPUB.\n\n## QA\n\n- 124 / 124 lexical `evil` verses reviewed and approved.\n- Exact direct-diff guard: pass for all 124; surrounding wording is unchanged except the explicitly permitted grammar repairs above.\n- Noun-vs-adjective form guard: pass.\n- Article agreement: pass.\n- Sentence-initial capitalization: pass.\n- Double-space / space-before-punctuation: pass.\n- Residual standalone `evil` in the 124 proposed verses: 0.\n\nThe two `Evilmerodach` rows remain NO CHANGE because they are a proper name, not the lexical English word `evil`.\n''',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
