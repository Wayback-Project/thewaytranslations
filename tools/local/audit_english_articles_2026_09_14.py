#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / 'current-form-documents' / 'the-way-current.epub'

BOOKS = [
    'genesis','exodus','leviticus','numbers','deuteronomy','joshua','judges','ruth',
    '1-samuel','2-samuel','1-kings','2-kings','1-chronicles','2-chronicles','ezra',
    'nehemiah','esther','job','psalms','proverbs','ecclesiastes','song-of-solomon',
    'isaiah','jeremiah','lamentations','ezekiel','daniel','hosea','joel','amos',
    'obadiah','jonah','micah','nahum','habakkuk','zephaniah','haggai','zechariah',
    'malachi','matthew','mark','luke','john','acts','romans','1-corinthians',
    '2-corinthians','galatians','ephesians','philippians','colossians','1-thessalonians',
    '2-thessalonians','1-timothy','2-timothy','titus','philemon','hebrews','james',
    '1-peter','2-peter','1-john','2-john','3-john','jude','revelation'
]

# These are orthographic mismatches that can nevertheless be correct because
# English a/an follows the initial sound rather than the first written letter.
AN_CONSONANT_EXCEPTIONS = (
    'heir', 'herb', 'honest', 'honor', 'honour', 'hour',
)
A_VOWEL_EXCEPTIONS = (
    'ewe', 'eul', 'eun', 'eup', 'euro', 'euch',
    'one', 'once',
    'uni', 'use', 'user', 'usual', 'utility', 'utensil', 'ufo',
)

ARTICLE_RE = re.compile(r"\b(a|an)\s+([A-Za-z][A-Za-z'’\-]*)", re.I)
VERSE_RE = re.compile(r'^(\d+)\.\s*(.*)$', re.S)


def local_name(tag: str) -> str:
    return tag.split('}', 1)[-1] if '}' in tag else tag


def collapse(value: str) -> str:
    return re.sub(r'\s+', ' ', value or '').strip()


def visible_text(el: ET.Element) -> str:
    return collapse(html.unescape(' '.join(el.itertext())))


def classify(article: str, word: str) -> tuple[bool, str]:
    a = article.lower()
    w = word.lower().lstrip("'’-")
    if not w:
        return False, 'no-word'
    vowel = w[0] in 'aeiou'
    if a == 'an' and not vowel:
        if w.startswith(AN_CONSONANT_EXCEPTIONS):
            return False, 'sound-exception-an'
        return True, 'an-before-consonant-letter'
    if a == 'a' and vowel:
        if w.startswith(A_VOWEL_EXCEPTIONS):
            return False, 'sound-exception-a'
        return True, 'a-before-vowel-letter'
    return False, 'orthographically-aligned'


def main() -> None:
    findings = []
    exceptions = []
    with zipfile.ZipFile(EPUB, 'r') as z:
        for slug in BOOKS:
            member = f'OEBPS/Text/{slug}.xhtml'
            if member not in z.namelist():
                raise RuntimeError(f'missing expected EPUB member: {member}')
            root = ET.fromstring(z.read(member))
            chapter = None
            for el in root.iter():
                ident = el.attrib.get('id', '')
                m_ch = re.fullmatch(rf'ch-{re.escape(slug)}-(\d+)', ident, re.I)
                if m_ch:
                    chapter = int(m_ch.group(1))
                if local_name(el.tag).lower() != 'p':
                    continue
                text = visible_text(el)
                vm = VERSE_RE.match(text)
                verse = int(vm.group(1)) if vm else None
                body = vm.group(2) if vm else text
                for m in ARTICLE_RE.finditer(body):
                    bad, reason = classify(m.group(1), m.group(2))
                    if not bad and not reason.startswith('sound-exception'):
                        continue
                    start = max(0, m.start() - 70)
                    end = min(len(body), m.end() + 100)
                    context = body[start:end]
                    row = {
                        'book': slug,
                        'chapter': chapter,
                        'verse': verse,
                        'article': m.group(1),
                        'word': m.group(2),
                        'phrase': m.group(0),
                        'reason': reason,
                        'context': context,
                    }
                    (findings if bad else exceptions).append(row)

    print('=== ENGLISH ARTICLE AUDIT: ACTIONABLE CANDIDATES ===')
    print(json.dumps(findings, ensure_ascii=False, indent=2))
    print('=== ENGLISH ARTICLE AUDIT: SOUND-BASED EXCEPTIONS (NO AUTO-FIX) ===')
    print(json.dumps(exceptions, ensure_ascii=False, indent=2))
    print(json.dumps({'actionableCount': len(findings), 'exceptionCount': len(exceptions)}, indent=2))


if __name__ == '__main__':
    main()
