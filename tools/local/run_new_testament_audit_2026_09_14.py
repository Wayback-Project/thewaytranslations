#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib.util
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().with_name('audit_new_testament_gender_brokenness_2026_09_14.py')
OUT = ROOT / 'audit-output' / 'new-testament-gender-brokenness-2026-09-14'

spec = importlib.util.spec_from_file_location('nt_audit', AUDIT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# The current canonical EPUB has 7,956 verse paragraphs in the NT, one fewer than the
# nominal 7,957 because Romans has a pre-existing verse-mapping corruption. We audit
# the text actually present, then record that structural failure explicitly below.
mod.EXPECTED_NT_VERSES = 7956
mod.main()

fields = ['reference','book','chapter','verse','category','priority','signals','reason','text']
with (OUT / 'candidates.tsv').open(encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
with (OUT / 'all-verses.tsv').open(encoding='utf-8', newline='') as f:
    allv = list(csv.DictReader(f, delimiter='\t'))

by_ref = {r['reference']: r['text'] for r in allv}
seen = {(r['reference'], r['category']) for r in rows}

def add(reference, book, chapter, verse, category, priority, signals, reason, text=None):
    key = (reference, category)
    if key in seen:
        return
    seen.add(key)
    rows.append({
        'reference': reference,
        'book': book,
        'chapter': str(chapter),
        'verse': str(verse),
        'category': category,
        'priority': priority,
        'signals': signals,
        'reason': reason,
        'text': by_ref.get(reference, '') if text is None else text,
    })

# Explicit structural QA findings discovered while validating the inventory.
add('Romans 14:23','Romans',14,23,'STRUCTURAL VERSE MAPPING','CRITICAL','embedded (14:24); embedded (14:25); embedded (14:26)',
    'The Romans 14:23 paragraph improperly contains three additional parenthetical verse labels and the doxology text. This is a verse-mapping/data-structure defect, not an inclusive-language judgment.')
add('Romans 16:25','Romans',16,25,'STRUCTURAL VERSE MAPPING','CRITICAL','empty verse paragraph',
    'The canonical Romans 16:25 verse paragraph is empty while related doxology text is embedded earlier in Romans 14:23.')
add('Romans 16:26','Romans',16,26,'STRUCTURAL VERSE MAPPING','CRITICAL','literal artifact 016:027',
    'The canonical Romans 16:26 verse paragraph contains the literal artifact “016:027” instead of normal verse text.')

# The prior AI/lexicon review suggests “unripeness/unripe” deserves the same kind of
# source-sensitive lexical scrutiny that “brokenness” received in the OT. This is a
# review flag, not a mandate for one replacement word.
unripe = re.compile(r'\bunripeness\b|\bunripe\b', re.I)
for item in allv:
    text = item['text']
    hits = sorted(set(m.group(0).lower() for m in unripe.finditer(text)))
    if not hits:
        continue
    ref = item['reference']
    m = re.match(r'^(.*) (\d+):(\d+)$', ref)
    if not m:
        continue
    add(ref, m.group(1), int(m.group(2)), int(m.group(3)), 'UNRIPENESS LEXICAL REVIEW','HIGH','; '.join(hits),
        '“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.', text)

# A tiny set of surface-English regressions can be identified safely without resolving
# source-language semantics.
malformed_patterns = [
    (re.compile(r'\bOne a person\b', re.I), 'One a person'),
    (re.compile(r'\bthey are not their\b', re.I), 'they are not their'),
]
for item in allv:
    hits = [label for rx, label in malformed_patterns if rx.search(item['text'])]
    if not hits:
        continue
    ref = item['reference']
    m = re.match(r'^(.*) (\d+):(\d+)$', ref)
    if not m:
        continue
    add(ref, m.group(1), int(m.group(2)), int(m.group(3)), 'MALFORMED LANGUAGE REVIEW','HIGH','; '.join(hits),
        'Surface English is grammatically malformed or internally incoherent and warrants manual correction after checking the source/context.', item['text'])

priority_order = {'CRITICAL': 0, 'HIGH': 1, 'REVIEW': 2}
book_order = {name: i for i, name in enumerate(mod.BOOKS.values())}
rows.sort(key=lambda r: (priority_order.get(r['priority'], 9), book_order.get(r['book'], 999), int(r['chapter']), int(r['verse']), r['category']))
with (OUT / 'candidates.tsv').open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields, delimiter='\t')
    w.writeheader(); w.writerows(rows)

summary_path = OUT / 'summary.json'
summary = json.loads(summary_path.read_text(encoding='utf-8'))
bycat = Counter(r['category'] for r in rows)
bypri = Counter(r['priority'] for r in rows)
bybook = defaultdict(Counter)
for r in rows:
    bybook[r['book']][r['category']] += 1
summary.update({
    'nominalStandardNewTestamentVerseCount': 7957,
    'canonicalExtractedVerseParagraphCount': 7956,
    'verseCountValidation': 'PASS WITH DOCUMENTED ROMANS STRUCTURAL EXCEPTION',
    'structuralVerseMappingStatus': 'CRITICAL REVIEW REQUIRED',
    'structuralFindings': [
        'Romans is the only NT book with a paragraph-count discrepancy: 432 extracted verse paragraphs versus a nominal 433.',
        'Romans 14:23 contains embedded labels (14:24), (14:25), and (14:26) followed by doxology text.',
        'Romans 16:25 is an empty verse paragraph.',
        'Romans 16:26 contains the literal artifact 016:027.',
        'No Scripture was modified by this audit.'
    ],
    'candidateRowCount': len(rows),
    'uniqueCandidateVerseCount': len({r['reference'] for r in rows}),
    'countsByCategory': dict(bycat),
    'countsByPriority': dict(bypri),
    'countsByBook': {b: dict(c) for b, c in bybook.items()},
})
summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

# Rebuild the review memo so the structural defect and added lexical checks appear first.
md = []
md.append('# New Testament Inclusive Language, Divine-Referent & Lexical Residual Audit')
md.append('')
md.append(f"- Canonical commit: `{summary['canonicalCommit']}`")
md.append(f"- Canonical EPUB SHA-256: `{summary['canonicalEpubSha256']}`")
md.append('- Scope: all 27 New Testament books / 260 chapters')
md.append('- Canonical verse paragraphs scanned: 7,956')
md.append('- Nominal NT verse count: 7,957')
md.append(f"- Candidate rows: {len(rows):,} across {summary['uniqueCandidateVerseCount']:,} unique verses")
md.append('- Important: candidate rows are review prompts, not a count of translation errors.')
md.append('')
md.append('## Critical structural finding')
md.append('')
md.append('Romans is the only New Testament book whose canonical paragraph inventory does not match the nominal verse inventory. The present EPUB has 432 Romans verse paragraphs rather than 433. Inspection shows that Romans 14:23 contains embedded `(14:24)`, `(14:25)`, and `(14:26)` doxology text; Romans 16:25 is empty; and Romans 16:26 contains the literal artifact `016:027`. This should be corrected as a separate verse-mapping/data-integrity task before a future release. The audit does **not** alter it.')
md.append('')
md.append('## Category counts')
md.append('')
for cat, n in bycat.most_common():
    md.append(f'- **{cat}:** {n:,}')
md.append('')
md.append('## Priority counts')
md.append('')
for pri in ['CRITICAL','HIGH','REVIEW']:
    md.append(f'- **{pri}:** {bypri.get(pri,0):,}')
md.append('')
md.append('## Editorial guardrails')
md.append('')
md.append('- Greek/Aramaic source and immediate literary context govern; English surface forms only identify review candidates.')
md.append('- Preserve actual men, male kinship, male-specific social roles, and Yeshua/Mashiach references where the source/context is male-specific.')
md.append('- Check plural `adelphoi`/brother-language for mixed-community address; do not assume every “brothers” occurrence means “brothers and sisters.”')
md.append('- Check “sons” constructions individually; some may have broader family/community scope, while others are intentionally male or idiomatic.')
md.append('- Masculine divine pronouns are changed under the project method only where the immediate referent is unmistakably divine; uncertain, Yeshua/Messianic, or ambiguous “Lord” references are not auto-resolved.')
md.append('- `Brokenness` and `unripeness` are lexical review flags. Neither should be replaced by one global word without Greek/context review.')
md.append('')
md.append('## Critical and high-priority queue')
md.append('')
for r in rows:
    if r['priority'] not in {'CRITICAL','HIGH'}:
        continue
    md.append(f"### {r['reference']} — {r['category']}")
    md.append('')
    md.append(f"> {r['text']}")
    md.append('')
    md.append(f"Signals: `{r['signals']}`")
    md.append('')
    md.append(r['reason'])
    md.append('')
md.append('## Book-by-book queue')
md.append('')
for book in mod.BOOKS.values():
    cats = bybook.get(book, {})
    total = sum(cats.values())
    details = ', '.join(f'{k}: {v}' for k, v in sorted(cats.items()))
    md.append(f'- **{book}:** {total:,} candidate rows' + (f' — {details}' if details else ''))
md.append('')
(OUT / 'high-priority.md').write_text('\n'.join(md), encoding='utf-8')

print(json.dumps(summary, indent=2, ensure_ascii=False))
