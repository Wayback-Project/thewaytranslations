#!/usr/bin/env python3
from __future__ import annotations

import re

import release_2026_09_30_quotation_spacing as release


def rewrite_genesis_source_preserving_source_wording(changes):
    """Normalize only approved quote-boundary whitespace in editable Genesis.

    The editable source has pre-existing lexical drift from the already-released
    EPUB at some references (for example Genesis 44:5 brokenness/wrong). That
    drift is outside this typography release. Therefore source and EPUB are each
    normalized in place without copying lexical wording from one layer to the
    other.
    """
    approved = {(row['chapter'], row['verse']) for row in changes}
    lines = release.GENESIS_SOURCE.read_text(encoding='utf-8').splitlines(keepends=True)
    chapter = None
    changed = set()
    out = []

    for line in lines:
        stripped = line.rstrip('\r\n')
        ending = line[len(stripped):]
        heading = re.fullmatch(r'Genesis\s+(\d+)', stripped)
        if heading:
            chapter = int(heading.group(1))
            out.append(line)
            continue

        verse_match = re.match(r'^(\d+)\.\s(.*)$', stripped)
        if chapter is not None and verse_match:
            verse = int(verse_match.group(1))
            key = (chapter, verse)
            if key in approved:
                current = verse_match.group(2)
                final = release.normalize_nested_spacing(current, key)
                if final == current:
                    raise RuntimeError(f'editable-source approved spacing transform made no change at Genesis {chapter}:{verse}')
                # This function is permitted to remove only quote-boundary
                # whitespace; normalize both sides to prove no other source text
                # changed.
                normalize_all = lambda value: release.OPEN_SPACE_RE.sub(
                    r'\1', release.CLOSE_SPACE_RE.sub(r'\1', value)
                )
                if normalize_all(current) != normalize_all(final):
                    raise RuntimeError(f'non-typographic editable-source change at Genesis {chapter}:{verse}')
                out.append(f'{verse}. {final}{ending}')
                changed.add(key)
                continue

        out.append(line)

    if changed != approved:
        missing = sorted(approved - changed)
        extra = sorted(changed - approved)
        raise RuntimeError(f'editable-source change set mismatch missing={missing} extra={extra}')

    release.GENESIS_SOURCE.write_text(''.join(out), encoding='utf-8')


release.rewrite_genesis_source = rewrite_genesis_source_preserving_source_wording
release.main()
