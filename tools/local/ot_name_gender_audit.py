#!/usr/bin/env python3
from pathlib import Path
import re, json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
OT_FILES = [
    ROOT / 'original-documents/genesis_restorative_translation.txt',
    ROOT / 'original-documents/exodus_to_ecclesiastes_restorative_translation.txt',
    ROOT / 'original-documents/rest_of_old_testament_restorative_translation.txt',
]

patterns = {
    'YHWH': r'\bYHWH\b',
    'Elohim': r'\bElohim\b',
    'God': r'\bGod\b',
    'LORD': r'\bLORD\b',
    'Cosmic Parent': r'\bCosmic Parent\b',
    'Father': r'\bFather\b',
    'repent*': r'\brepent\w*\b',
    'relent*': r'\brelent\w*\b',
    'turn back*': r'\bturn back\w*\b',
    'Wisdom': r'\bWisdom\b',
    'Ruach': r'\bRuach\b',
    'Ruach she': r'Ruach[^\n]{0,50}\bshe\b',
}

rows=[]
for path in OT_FILES:
    txt = path.read_text(encoding='utf-8')
    row={'path':str(path.relative_to(ROOT)), 'lines':txt.count('\n')+1}
    for k,p in patterns.items():
        row[k]=len(re.findall(p,txt))
    rows.append(row)

out={
    'generatedAtUtc': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
    'rows': rows,
    'patterns': list(patterns.keys())
}

out_json = ROOT / 'change-logs/old-testament/reports/OT-NAME-GENDER-AUDIT-LATEST.json'
out_md = ROOT / 'change-logs/old-testament/reports/OT-NAME-GENDER-AUDIT-LATEST.md'
out_json.write_text(json.dumps(out, indent=2), encoding='utf-8')

headers=['path','lines']+list(patterns.keys())
md=['# OT Name + Gender Audit (Local)','',f"Generated: {out['generatedAtUtc']}",'']
md.append('| ' + ' | '.join(headers) + ' |')
md.append('|' + '|'.join(['---']*len(headers)) + '|')
for r in rows:
    md.append('| ' + ' | '.join(str(r[h]) for h in headers) + ' |')
md.append('')
md.append('Command: `python3 tools/local/ot_name_gender_audit.py`')
out_md.write_text('\n'.join(md)+'\n', encoding='utf-8')
print(out_md)
print(out_json)
