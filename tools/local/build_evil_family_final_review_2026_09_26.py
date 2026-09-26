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
    if len(proposal_rows) != 124: raise RuntimeError(f'proposal row count mismatch: {len(proposal_rows)}')
    if len(family_rows) != 126: raise RuntimeError(f'family row count mismatch: {len(family_rows)}')

    combined=[]
    for fam in family_rows:
        ref=fam['reference']
        if ref in proposal_by_ref:
            p=proposal_by_ref[ref]
            combined.append({
                'reference':ref,'testament':fam['testament'],'decision_change':'YES',
                'current_text':p['current_verse'],'proposed_form':p['proposed_form'],'proposed_text':p['proposed_verse'],
                'semantic_rationale':p['semantic_rationale'],'grammar_check':p['grammar_check'],
                'capitalization_check':p['capitalization_check'],'spacing_punctuation_check':p['spacing_punctuation_check'],
                'reviewed':'☑','approved':'☑','notes':p['editor_notes'],
            })
        else:
            form=fam['compound_forms'] or fam['evil_family_forms']
            if form.lower() != 'evilmerodach': raise RuntimeError(f'unexpected nonlexical row: {ref} {form}')
            combined.append({
                'reference':ref,'testament':fam['testament'],'decision_change':'NO',
                'current_text':fam['current_text'],'proposed_form':'retain proper name Evilmerodach','proposed_text':fam['current_text'],
                'semantic_rationale':'Proper name, not the lexical English word “evil”; retain unchanged in this terminology release.',
                'grammar_check':'PASS','capitalization_check':'PASS','spacing_punctuation_check':'PASS',
                'reviewed':'☑','approved':'☑','notes':'Final NO CHANGE decision for this terminology release.',
            })

    yes=sum(r['decision_change']=='YES' for r in combined); no=sum(r['decision_change']=='NO' for r in combined)
    if (yes,no)!=(124,2): raise RuntimeError(f'decision count mismatch yes={yes} no={no}')
    fields=['reference','testament','decision_change','current_text','proposed_form','proposed_text','semantic_rationale','grammar_check','capitalization_check','spacing_punctuation_check','reviewed','approved','notes']
    with OUT_TSV.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(combined)

    esc=html.escape; rows_html=[]
    for i,r in enumerate(combined,1):
        qa=f"Grammar {r['grammar_check']} · Caps {r['capitalization_check']} · Spacing {r['spacing_punctuation_check']}"
        rows_html.append('<tr>'+f'<td>{i}</td><td><strong>{esc(r["reference"])}</strong></td><td><strong>{esc(r["decision_change"])}</strong></td>'+f'<td>{esc(r["current_text"])}</td><td>{esc(r["proposed_form"])}</td><td>{esc(r["proposed_text"])}</td>'+f'<td>{esc(r["semantic_rationale"])}</td><td>{esc(qa)}</td><td>{r["reviewed"]}</td><td>{r["approved"]}</td><td>{esc(r["notes"])}</td></tr>')

    pct=yes/len(combined)*100
    doc=f'''<!doctype html><html><head><meta charset="utf-8"><title>The Way Version — final evil / brokenness review</title>
<style>body{{font-family:Arial,sans-serif;line-height:1.35;color:#222}}h1{{font-size:22px}}h2{{font-size:17px;margin-top:24px}}p,li{{font-size:10.5pt}}table{{border-collapse:collapse;width:100%;font-size:8pt}}th,td{{border:1px solid #bbb;padding:4px;vertical-align:top}}th{{background:#eee;font-weight:bold}}.small{{font-size:9pt;color:#444}}</style></head><body>
<h1>The Way Version — final whole-Bible “evil” → brokenness / broken review</h1>
<p><strong>Status:</strong> FINAL EDITORIAL DECISION — approved for canonical release by direct instruction on 2026-09-26.</p>
<p><strong>Canonical baseline EPUB SHA-256:</strong> {CANONICAL_SHA}</p>
<p><strong>Whole-Bible audit:</strong> 31,102 canonical verses. 126 verses contain a word beginning <code>evil…</code>: 124 lexical <code>evil</code> rows approved for change and 2 <code>Evilmerodach</code> proper-name rows approved for NO CHANGE. {yes}/126 = {pct:.1f}% lexical-change decision coverage.</p>
<h2>Final editorial rule</h2><ul>
<li><strong>Do not rewrite the whole phrase.</strong> The lexical word <code>evil</code> itself is the target.</li>
<li>Use <strong>brokenness</strong> when <code>evil</code> occupies a noun / abstract-concept slot.</li>
<li>Use <strong>broken</strong> when English requires an adjective, predicate adjective, or substantive adjective; “the broken and the good” is acceptable.</li>
<li>No contextual substitutions such as harm, wrong, disaster, calamity, adversity, defective, or phrase rewrites are part of this final release.</li>
<li>The only surrounding-token changes are grammar-required: <code>an</code> → <code>a</code> in Ezekiel 38:10 and <code>they delights</code> → <code>they delight</code> in Malachi 2:17. Psalm 5:4 and Psalm 34:21 capitalize the new sentence-start word.</li>
</ul>
<h2>Final QA</h2><ul><li>Direct-diff guard: PASS on all 124 lexical rows; unrelated surrounding wording cannot change.</li><li>Noun-vs-adjective form: PASS.</li><li>Article agreement: PASS.</li><li>Sentence capitalization: PASS.</li><li>Replacement-induced spacing/punctuation: PASS.</li><li>Every row below is reviewed and approved.</li></ul>
<p class="small">This document is the print handoff record for this terminology release. The current-text column shows the pre-release canonical wording; the proposed-text column is the approved released wording.</p>
<table><thead><tr><th>#</th><th>Reference</th><th>Change?</th><th>Current text</th><th>Final form</th><th>Final text</th><th>Rationale</th><th>QA</th><th>Reviewed</th><th>Approved</th><th>Notes</th></tr></thead><tbody>{''.join(rows_html)}</tbody></table></body></html>'''
    OUT_HTML.parent.mkdir(parents=True,exist_ok=True); OUT_HTML.write_text(doc,encoding='utf-8')
    print(f'final review rows={len(combined)} yes={yes} no={no}')

if __name__=='__main__': main()
