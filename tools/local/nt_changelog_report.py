#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
OUT_MD = ROOT / 'change-logs/new-testament/reports/NT-QA-LATEST.md'
OUT_JSON = ROOT / 'change-logs/new-testament/reports/NT-QA-LATEST.json'

FILES = [
    ('Matthew', ROOT / 'original-documents/matthew_restorative_translation.txt'),
    ('Mark', ROOT / 'original-documents/mark_restorative_translation.txt'),
    ('Luke', ROOT / 'original-documents/luke_restorative_translation.txt'),
    ('John', ROOT / 'original-documents/john_restorative_translation.txt'),
    ('Acts', ROOT / 'original-documents/acts_restorative_translation.txt'),
    ('RestOfNT', ROOT / 'original-documents/rest_of_new_testament_restorative_translation.txt'),
]

TERMS = [
    'reign of the heavens',
    'turn back',
    'Yeshua',
    'Elohim',
    'Ruach',
    'rope',
    'camel',
    'Lord',
    'assembly',
    'church',
]

rows = []
for name, path in FILES:
    text = path.read_text(encoding='utf-8')
    lines = text.count('\n') + 1
    counts = {t: text.count(t) for t in TERMS}
    rows.append({
        'bookGroup': name,
        'path': str(path.relative_to(ROOT)),
        'lines': lines,
        'termCounts': counts,
    })

payload = {
    'generatedAtUtc': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
    'rows': rows,
    'terms': TERMS,
}

OUT_JSON.write_text(json.dumps(payload, indent=2), encoding='utf-8')

md = []
md.append('# NT QA Latest (Local, No-DB)')
md.append('')
md.append(f"Generated: {payload['generatedAtUtc']}")
md.append('')
md.append('| Group | Lines | ' + ' | '.join(TERMS) + ' |')
md.append('|---|---:|' + '|'.join(['---:' for _ in TERMS]) + '|')
for r in rows:
    md.append('| ' + r['bookGroup'] + ' | ' + str(r['lines']) + ' | ' + ' | '.join(str(r['termCounts'][t]) for t in TERMS) + ' |')
md.append('')
md.append('Command: `python3 tools/local/nt_changelog_report.py`')
OUT_MD.write_text('\n'.join(md) + '\n', encoding='utf-8')

print('Wrote', OUT_MD)
print('Wrote', OUT_JSON)
