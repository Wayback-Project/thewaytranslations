#!/usr/bin/env python3
from __future__ import annotations

import build_evil_brokenness_unripeness_proposal_2026_09_25 as builder


def apply_exact_preserving_case(text, repls, ref):
    """Apply the finite proposal ledger while preserving sentence-initial case.

    The proposal inventory stores the lexical target as lowercase ``evil`` in
    most rows. A canonical verse may contain sentence-initial ``Evil``. When
    that is the only case mismatch, capitalize the replacement rather than
    failing or producing a lowercase sentence start. All other mismatches stay
    fatal so this remains an exact, finite proposal rather than a broad search.
    """
    out = text
    for old, new in repls:
        if old in out:
            out = out.replace(old, new, 1)
            continue
        if old == 'evil' and 'Evil' in out:
            capped = new[:1].upper() + new[1:]
            out = out.replace('Evil', capped, 1)
            continue
        raise RuntimeError(f'{ref}: expected phrase not found: {old!r}')
    return out


builder.apply_exact = apply_exact_preserving_case
builder.main()
