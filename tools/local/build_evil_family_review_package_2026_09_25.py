#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
from pathlib import Path

import audit_evil_brokenness_unripeness_2026_09_25 as base

ROOT = base.ROOT
PROPOSAL = ROOT / 'tools' / 'local' / 'proposed_evil_brokenness_unripeness_2026_09_25.tsv'
FAMILY = ROOT / 'tools' / 'local' / 'generated_evil_family_inventory_2026_09_25.tsv'
OUT_TSV = ROOT / 'tools' / 'local' / 'proposed_evil_family_review_2026_09_25.tsv'
OUT_HTML = ROOT / 'review' / '2026-09-25-evil-brokenness-unripeness-review.html'
CANONICAL_SHA = base.CANONICAL_SHA


def read_tsv(path: Path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def main():
    proposal_rows = read_tsv(PROPOSAL)
    family_rows = read_tsv(FAMILY)
    proposal_by_ref = {r['reference']: r for r in proposal_rows}

    if len(proposal_rows) != 124:
        raise RuntimeError(f'proposal row count mismatch: {len(proposal_rows)} != 124')
    if len(family_rows) != 126:
        raise RuntimeError(f'evil-family row count mismatch: {len(family_rows)} != 126')

    combined = []
    for fam in family_rows:
        ref = fam['reference']
        if ref in proposal_by_ref:
            p = proposal_by_ref[ref]
            combined.append({
                'reference': ref,
                'testament': fam['testament'],
                'decision_change': 'YES',
                'current_text': p['current_verse'],
                'proposed_form': p['proposed_form'],
                'proposed_text': p['proposed_verse'],
                'semantic_rationale': p['semantic_rationale'],
                'grammar_check': p['grammar_check'],
                'capitalization_check': p['capitalization_check'],
                'spacing_punctuation_check': p['spacing_punctuation_check'],
                'reviewed': '☐',
                'approved': '☐',
                'notes': p['editor_notes'],
            })
        else:
            form = fam['compound_forms'] or fam['evil_family_forms']
            if form.lower() != 'evilmerodach':
                raise RuntimeError(f'unexpected evil-family row outside lexical proposal: {ref} {form}')
            combined.append({
                'reference': ref,
                'testament': fam['testament'],
                'decision_change': 'NO',
                'current_text': fam['current_text'],
                'proposed_form': 'retain proper name Evilmerodach',
                'proposed_text': fam['current_text'],
                'semantic_rationale': 'Proper name, not the lexical word “evil.” Keep unchanged in this terminology audit; any original-name restoration belongs in the separate name workflow.',
                'grammar_check': 'PASS',
                'capitalization_check': 'PASS',
                'spacing_punctuation_check': 'PASS',
                'reviewed': '☐',
                'approved': '☐',
                'notes': 'False positive for evil-family substring matching.',
            })

    yes_count = sum(r['decision_change'] == 'YES' for r in combined)
    no_count = sum(r['decision_change'] == 'NO' for r in combined)
    if (yes_count, no_count) != (124, 2):
        raise RuntimeError(f'decision counts mismatch: yes={yes_count} no={no_count}')

    fields = ['reference','testament','decision_change','current_text','proposed_form','proposed_text','semantic_rationale','grammar_check','capitalization_check','spacing_punctuation_check','reviewed','approved','notes']
    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_TSV.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader(); w.writerows(combined)

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    esc = html.escape
    rows_html = []
    for i, r in enumerate(combined, 1):
        qa = f"Grammar {r['grammar_check']} · Caps {r['capitalization_check']} · Spacing {r['spacing_punctuation_check']}"
        rows_html.append(
            '<tr>'
            f'<td>{i}</td>'
            f'<td><strong>{esc(r["reference"])}</strong></td>'
            f'<td><strong>{esc(r["decision_change"])}</strong></td>'
            f'<td>{esc(r["current_text"])}</td>'
            f'<td>{esc(r["proposed_form"])}</td>'
            f'<td>{esc(r["proposed_text"])}</td>'
            f'<td>{esc(r["semantic_rationale"])}</td>'
            f'<td>{esc(qa)}</td>'
            f'<td>{r["reviewed"]}</td>'
            f'<td>{r["approved"]}</td>'
            f'<td>{esc(r["notes"])}</td>'
            '</tr>'
        )

    pct = yes_count / len(combined) * 100
    html_doc = f'''<!doctype html>
<html><head><meta charset="utf-8"><title>The Way Version — evil / brokenness / unripeness review</title>
<style>
body{{font-family:Arial,sans-serif;line-height:1.35;color:#222}}
h1{{font-size:22px}} h2{{font-size:17px;margin-top:24px}}
p,li{{font-size:10.5pt}}
table{{border-collapse:collapse;width:100%;font-size:8pt}}
th,td{{border:1px solid #bbb;padding:4px;vertical-align:top}}
th{{background:#eee;font-weight:bold}}
.small{{font-size:9pt;color:#444}}
</style></head><body>
<h1>The Way Version — whole-Bible “evil” / brokenness / unripeness review</h1>
<p><strong>Status:</strong> PROPOSAL ONLY — non-canonical until explicit editorial approval.</p>
<p><strong>Canonical baseline EPUB SHA-256:</strong> {CANONICAL_SHA}</p>
<p><strong>Whole-Bible audit:</strong> 31,102 canonical verses. 126 verses contain a word beginning <code>evil…</code>. Of these, 124 contain the lexical word <code>evil</code> and are proposed for change; 2 contain the proper name <code>Evilmerodach</code> and are proposed for NO CHANGE. That is {yes_count}/{len(combined)} = {pct:.1f}% proposed change.</p>
<h2>Editorial rule used for the first pass</h2>
<ul>
<li>Use <strong>brokenness</strong> for the project’s abstract moral/conceptual noun where that is grammatical.</li>
<li>Use <strong>broken</strong> where English requires an adjective/predicate adjective rather than the noun <em>brokenness</em>.</li>
<li>Use precise contextual terms such as <strong>harm, wrong, wrongdoing, adversity, trouble, calamity, disaster</strong> where the verse is about an event, injury, judgment, or action.</li>
<li><strong>Unripe / unripeness remain allowed review options</strong>, but this first pass does not force them into rows where the resulting English would be less natural. Human review may change any proposed form.</li>
<li>No blanket search/replace is authorized. Each row is a finite exact-verse proposal.</li>
</ul>
<h2>QA gates already applied</h2>
<ul>
<li>Grammar/form check, including noun-vs-adjective and a/an agreement.</li>
<li>Sentence-initial capitalization; specifically catches the Psalm 5:4 and Psalm 34:21 regressions.</li>
<li>Double-space and space-before-punctuation guards.</li>
<li>Residual <code>evil</code> check inside every YES proposal.</li>
<li>Adjacent grammar correction noted for Malachi 2:17: “they delights” → “they delight.”</li>
</ul>
<p class="small">The “Reviewed” and “Approved” boxes are intentionally unchecked. They are for the later human row-by-row process.</p>
<table>
<thead><tr><th>#</th><th>Reference</th><th>Change?</th><th>Current text</th><th>Proposed form</th><th>Proposed text</th><th>Rationale</th><th>QA</th><th>Reviewed</th><th>Approved</th><th>Notes</th></tr></thead>
<tbody>{''.join(rows_html)}</tbody>
</table>
</body></html>'''
    OUT_HTML.write_text(html_doc, encoding='utf-8')
    print(f'wrote {OUT_TSV.relative_to(ROOT)} and {OUT_HTML.relative_to(ROOT)} rows={len(combined)} yes={yes_count} no={no_count}')


if __name__ == '__main__':
    main()
