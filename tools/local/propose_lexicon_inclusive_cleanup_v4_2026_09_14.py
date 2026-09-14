#!/usr/bin/env python3
from __future__ import annotations

import propose_lexicon_inclusive_cleanup_v3_2026_09_14 as v3

_base=v3.lexical_v3

def lexical_v4(ref: str, text: str) -> str:
    out=_base(ref,text)
    if ref=='Psalms 140:11':
        out=out.replace("A evil speaker won't be established in the earth. evil will hunt the violent man to overthrow him.",
                        "A malicious speaker won't be established in the earth. Evil will hunt the violent person to overthrow them.")
    if ref=='Habakkuk 2:9':
        out=out.replace('gets a evil gain for their house','gets dishonest gain for their house')
    return out

v3.lexical_v3=lexical_v4

if __name__=='__main__':
    v3.main()
