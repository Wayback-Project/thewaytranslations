#!/usr/bin/env python3
from __future__ import annotations

import re
import propose_lexicon_inclusive_cleanup_2026_09_14 as v1

# Release proposal v2 deliberately disables heuristic divine-pronoun mutation.
# Divine rows require explicit hand approval because proximity/coreference produced
# real false positives in v1 (e.g. the serpent, Yishmael, Moshe).
def no_divine_autofix(text, signals):
    return text

# Formulaic generic-person fix only. We mutate from the generic antecedent forward,
# never pronouns before it, and only when that antecedent occurs near the beginning
# of the verse/quotation. Named people, divine markers, and sex-specific roles remain
# excluded by v1's guards.
STRICT_GENERIC = re.compile(
    r'(?i)(?:^[\s\"“\']{0,6})(?:if\s+|when\s+|whenever\s+)?'
    r'(?:anyone|someone|whoever|everyone|no one|a person|the person|one who|the one who)\b'
)


def strict_generic_fix(text):
    if v1.DIV_RE.search(text) or v1.PROPER_RE.search(text) or v1.SEX_SPECIFIC_RE.search(text):
        return text
    m=STRICT_GENERIC.search(text)
    if not m:
        return text
    # Any specific masculine pronoun before the generic marker means the verse is
    # already tracking another referent; do not touch it automatically.
    if v1.MASC_PRON_RE.search(text[:m.start()]):
        return text
    prefix=text[:m.start()]
    seg=text[m.start():]
    for src,dst in v1.PRON_MAP.items():
        seg=re.sub(rf'\b{re.escape(src)}\b',dst,seg)
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
      (r'\bthey walks\b','they walk'),(r'\bThey walks\b','They walk'),
      (r'\bthey seeks\b','they seek'),(r'\bThey seeks\b','They seek'),
      (r'\bthey hates\b','they hate'),(r'\bThey hates\b','They hate'),
    ]
    for a,b in repairs: seg=re.sub(a,b,seg)
    return prefix+seg

v1.neutralize_generic_pronouns = strict_generic_fix
v1.divine_fix = no_divine_autofix

if __name__ == '__main__':
    v1.main()
