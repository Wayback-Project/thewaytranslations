#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter

import audit_evil_brokenness_unripeness_2026_09_25 as base

ROOT = base.ROOT
EPUB = base.EPUB
OUT = ROOT / 'tools' / 'local' / 'generated_evil_family_inventory_2026_09_25.tsv'
SUMMARY = ROOT / 'change-logs' / 'reports' / '2026-09-25-evil-family-inventory.json'
EVIL_FAMILY = re.compile(r'\bevil[\w-]*\b', re.I)
STANDALONE = re.compile(r'\bevil\b', re.I)


def main():
    actual = base.sha256(EPUB)
    if actual != base.CANONICAL_SHA:
        raise SystemExit(f'canonical EPUB SHA mismatch expected={base.CANONICAL_SHA} got={actual}')

    verses = base.collect_verses(EPUB, slugs=tuple(slug for slug, _, _ in base.BOOKS))
    if len(verses) != 31102:
        raise RuntimeError(f'whole-Bible verse inventory mismatch: {len(verses)} != 31102')

    rows = []
    for (slug, ch, vs), text in verses.items():
        matches = [m.group(0) for m in EVIL_FAMILY.finditer(text)]
        if not matches:
            continue
        book, testament = base.SLUG_TO_META[slug]
        standalone_count = len(STANDALONE.findall(text))
        family_count = len(matches)
        compound_forms = sorted({m.lower() for m in matches if m.lower() != 'evil'})
        rows.append({
            'reference': f'{book} {ch}:{vs}',
            'testament': testament,
            'book': book,
            'chapter': ch,
            'verse': vs,
            'evil_family_forms': ','.join(sorted({m.lower() for m in matches})),
            'standalone_evil_count': standalone_count,
            'compound_evil_count': family_count - standalone_count,
            'compound_forms': ','.join(compound_forms),
            'current_text': text,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = ['reference','testament','book','chapter','verse','evil_family_forms','standalone_evil_count','compound_evil_count','compound_forms','current_text']
    with OUT.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader(); w.writerows(rows)

    compound_only = [r for r in rows if int(r['compound_evil_count']) > 0]
    compound_occurrences = sum(int(r['compound_evil_count']) for r in compound_only)
    form_counts = Counter()
    for r in compound_only:
        for form in r['compound_forms'].split(','):
            if form:
                form_counts[form] += 1

    report = {
        'status': 'inventory-only; non-canonical; no Scripture changes',
        'canonicalEpubSha256': actual,
        'wholeBibleVerseCount': len(verses),
        'evilFamilyVerseCount': len(rows),
        'standaloneEvilVerseCount': sum(1 for r in rows if int(r['standalone_evil_count']) > 0),
        'compoundEvilVerseCount': len(compound_only),
        'compoundEvilOccurrenceCount': compound_occurrences,
        'compoundVerseCountsByTestament': dict(Counter(r['testament'] for r in compound_only)),
        'compoundFormsByVerseCount': dict(sorted(form_counts.items())),
        'output': str(OUT.relative_to(ROOT)),
        'method': 'Exact 31,102-verse canonical EPUB extraction. Finds word-initial evil-family forms including standalone evil and compounds such as evildoer/evildoing; no replacement is performed.'
    }
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
