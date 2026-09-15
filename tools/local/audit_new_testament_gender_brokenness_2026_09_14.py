#!/usr/bin/env python3
from __future__ import annotations

import copy
import csv
import hashlib
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
EPUB = ROOT / 'current-form-documents' / 'the-way-current.epub'
OUT = ROOT / 'audit-output' / 'new-testament-gender-brokenness-2026-09-14'
EXPECTED_SHA = 'd48ec5b7da0db10c7c44c518793228dc5b2d69edc6e57de838486d2aefbcf62f'
EXPECTED_NT_VERSES = 7957

BOOKS = {
    'matthew':'Matthew','mark':'Mark','luke':'Luke','john':'John','acts':'Acts','romans':'Romans',
    '1-corinthians':'1 Corinthians','2-corinthians':'2 Corinthians','galatians':'Galatians','ephesians':'Ephesians',
    'philippians':'Philippians','colossians':'Colossians','1-thessalonians':'1 Thessalonians','2-thessalonians':'2 Thessalonians',
    '1-timothy':'1 Timothy','2-timothy':'2 Timothy','titus':'Titus','philemon':'Philemon','hebrews':'Hebrews','james':'James',
    '1-peter':'1 Peter','2-peter':'2 Peter','1-john':'1 John','2-john':'2 John','3-john':'3 John','jude':'Jude','revelation':'Revelation'
}
EXPECTED_CHAPTERS = {
    'matthew':28,'mark':16,'luke':24,'john':21,'acts':28,'romans':16,'1-corinthians':16,'2-corinthians':13,
    'galatians':6,'ephesians':6,'philippians':4,'colossians':4,'1-thessalonians':5,'2-thessalonians':3,
    '1-timothy':6,'2-timothy':4,'titus':3,'philemon':1,'hebrews':13,'james':5,'1-peter':5,'2-peter':3,
    '1-john':5,'2-john':1,'3-john':1,'jude':1,'revelation':22
}

# Deliberately conservative divine list. Yeshua/Mashiach and ambiguous "Lord" are excluded from automatic
# divine-coreference surfacing because the project retains genuinely human/Yeshua masculine reference and
# treats uncertain or Christological referents as manual review questions.
DIV = r'(?:YHWH|Elohim|God|Cosmic Parent|Creator|Almighty|Most High|Ruach(?: HaKodesh)?|Holy Spirit)'
PRON = r'(?:he|him|his|himself)'
DIV_RE = re.compile(rf'\b{DIV}\b', re.I)
PRON_RE = re.compile(rf'\b{PRON}\b', re.I)
HUMAN_DISTRACTOR = re.compile(
    r'\b(?:Yeshua|Jesus|Mashiach|Messiah|Lord|master|teacher|rabbi|apostle|disciple|prophet|priest|king|governor|'
    r'Caesar|Pilate|Herod|Shaul|Paul|Peter|Kefa|Yochanan|John|Yaakov|James|man|woman|person|child|father|mother|'
    r'brother|sister|servant|slave|people|enemy|neighbor|ruler|one\s+who)\b', re.I)
DEVOTION = re.compile(
    r'\b(?:serve|serves|served|seek|seeks|sought|follow|follows|followed|revere|reveres|revered|fear|fears|feared|'
    r'worship|worships|worshiped|trust|trusts|trusted|wait|waits|waited|call on|calls on|called on|pray to|prays to|'
    r'prayed to|praise|praises|praised|exalt|exalts|exalted|obey|obeys|obeyed|return to|returns to|returned to)\s+'
    r'(?:only\s+)?(?P<p>him|his|himself)\b', re.I)
ATTR = re.compile(
    r'\b(?P<p>his)\s+(?:anger|wrath|mercy|grace|name|glory|power|hand|eyes|commandments|commandment|will|kingdom|'
    r'word|voice|spirit|Ruach|people|servants|prophets|works|gift|love|righteousness|presence|throne|judgment|truth)\b', re.I)
SUBJECT_AFTER = re.compile(rf'\b(?P<d>{DIV})\b(?P<mid>[^.!?]{{0,110}}?)(?:;|,|\band\b|\bfor\b|\bbecause\b|\bwho\b|\bthat\b)\s*(?P<p>he|his|himself)\b', re.I)
SENTENCE_AFTER = re.compile(rf'\b(?P<d>{DIV})\b(?P<mid>[^.!?]{{0,140}}?)[.!?]\s*[\"“‘\']*(?P<p>He|His|Himself)\b')

BROKENNESS = re.compile(r'\bbrokenness\b|\bbroken deeds?\b|\bbroken person\b|\bbroken people\b|\bbrokenness news\b', re.I)
GENERIC_STRONG = re.compile(r'\b(?:a person|any person|each person|someone|anyone|everyone|whoever|one who|the one who|a believer|any believer|each believer)\b', re.I)
GENERIC_SECONDARY = re.compile(r'\b(?:a child|a servant|a slave|a stranger|a foreigner|your neighbor|your enemy|the poor|the rich|the righteous|the wicked|a sinner|the sinner|a disciple|the disciple|a worker|the worker|a teacher|the teacher)\b', re.I)
GENERIC_MAN = re.compile(r'\b(?:any man|every man|each man|no man|a man who|the man who|man who|men who|all men|mankind)\b', re.I)
MASC_TERM = re.compile(r'\b(?:man|men|mankind|watchman|watchmen|workman|workmen|craftsman|craftsmen)\b', re.I)
BROTHER_TERM = re.compile(r'\b(?:brothers|brethren)\b', re.I)
INCLUSIVE_BROTHERS = re.compile(r'\bbrothers\s+(?:and|&)\s+sisters\b', re.I)
SONS_TERM = re.compile(r'\bsons\b', re.I)
ARTICLE_BAD = re.compile(r'\ban\s+(?:person|people|man|woman|child|human|worker|servant|believer|disciple)\b', re.I)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def collapse(value: str) -> str:
    return re.sub(r'\s+', ' ', value or '').strip()


def local_name(name: str) -> str:
    return name.split('}', 1)[-1] if '}' in name else name


def element_text(el: ET.Element) -> str:
    return collapse(' '.join(el.itertext()))


def strip_namespaces(root: ET.Element) -> ET.Element:
    root = copy.deepcopy(root)
    for el in root.iter():
        el.tag = local_name(el.tag)
        attrs = {local_name(k): v for k, v in el.attrib.items()}
        el.attrib.clear()
        el.attrib.update(attrs)
    return root


def find_book_member(z: zipfile.ZipFile, slug: str) -> str:
    exact = f'OEBPS/Text/{slug}.xhtml'
    if exact in z.namelist():
        return exact
    matches = [n for n in z.namelist() if n.lower().endswith(f'/{slug}.xhtml')]
    if len(matches) != 1:
        raise RuntimeError(f'cannot locate {slug} XHTML: {matches}')
    return matches[0]


def chapter_number(el: ET.Element, slug: str):
    ident = el.attrib.get('id', '')
    m = re.fullmatch(rf'ch-{re.escape(slug)}-(\d+)', ident, re.I)
    return int(m.group(1)) if m else None


def extract_book(raw: bytes, slug: str, book: str):
    root = ET.fromstring(raw)
    parents = {child: parent for parent in root.iter() for child in parent}
    anchors = []
    for el in root.iter():
        n = chapter_number(el, slug)
        if n is not None:
            anchors.append((n, el))
    anchors.sort(key=lambda x: x[0])
    nums = [n for n, _ in anchors]
    expected = list(range(1, EXPECTED_CHAPTERS[slug] + 1))
    if nums != expected:
        raise RuntimeError(f'chapter anchors invalid for {book}: expected {len(expected)}, found {nums}')

    verses = []
    for number, el in anchors:
        frag = el
        if len(element_text(el)) < 80:
            parent = parents.get(el)
            if parent is None:
                raise RuntimeError(f'no wrapper for {book} {number}')
            siblings = list(parent)
            start = siblings.index(el)
            gathered = []
            for sibling in siblings[start:]:
                if sibling is not el and chapter_number(sibling, slug) is not None:
                    break
                gathered.append(copy.deepcopy(sibling))
            wrapper = ET.Element('section')
            for sibling in gathered:
                wrapper.append(sibling)
            frag = wrapper

        clean = strip_namespaces(frag)
        seen_verses = set()
        found = 0
        for node in clean.iter():
            if local_name(node.tag).lower() != 'p':
                continue
            plain = element_text(node)
            m = re.match(r'^(\d+)\.\s*(.*)$', plain, re.S)
            if not m:
                continue
            verse = int(m.group(1))
            if verse in seen_verses:
                continue
            seen_verses.add(verse)
            found += 1
            verses.append((book, number, verse, collapse(m.group(2))))
        if not found:
            raise RuntimeError(f'no verses for {book} {number}')
    return verses


def extract_all():
    verses = []
    with zipfile.ZipFile(EPUB) as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f'EPUB CRC failure: {bad}')
        for slug, book in BOOKS.items():
            verses.extend(extract_book(z.read(find_book_member(z, slug)), slug, book))
    if len(verses) != EXPECTED_NT_VERSES:
        raise RuntimeError(f'New Testament verse inventory mismatch: {len(verses)} != {EXPECTED_NT_VERSES}')
    return verses


def nearby_divine(text, pos, window=160):
    start = max(0, pos - window)
    before = text[start:pos]
    ms = list(DIV_RE.finditer(before))
    if not ms:
        return None, ''
    m = ms[-1]
    return m.group(0), before[m.start():]


def divine_hits(text):
    if not DIV_RE.search(text) or not PRON_RE.search(text):
        return []
    hits = []
    for m in DEVOTION.finditer(text):
        divine, segment = nearby_divine(text, m.start(), 180)
        if divine and not HUMAN_DISTRACTOR.search(segment[segment.find(divine) + len(divine):]):
            hits.append('devotion-object')
    for m in ATTR.finditer(text):
        divine, segment = nearby_divine(text, m.start(), 130)
        if divine:
            after = segment[segment.rfind(divine) + len(divine):]
            if not HUMAN_DISTRACTOR.search(after):
                hits.append('divine-attribute')
    for m in SUBJECT_AFTER.finditer(text):
        if not HUMAN_DISTRACTOR.search(m.group('mid') or ''):
            hits.append('explicit-divine-subject')
    for m in SENTENCE_AFTER.finditer(text):
        if not HUMAN_DISTRACTOR.search(m.group('mid') or ''):
            hits.append('next-sentence-divine-subject')
    return sorted(set(hits))


def add(rows, seen, book, ch, vs, text, category, priority, signals, reason):
    key = (book, ch, vs, category)
    if key in seen:
        return
    seen.add(key)
    rows.append({
        'reference': f'{book} {ch}:{vs}',
        'book': book,
        'chapter': ch,
        'verse': vs,
        'category': category,
        'priority': priority,
        'signals': '; '.join(signals),
        'reason': reason,
        'text': text,
    })


def main():
    actual = sha256(EPUB)
    if actual != EXPECTED_SHA:
        raise SystemExit(f'Canonical EPUB SHA mismatch: {actual} != {EXPECTED_SHA}')

    allv = extract_all()
    rows = []
    seen = set()

    for book, ch, vs, text in allv:
        m = ARTICLE_BAD.search(text)
        if m:
            add(rows, seen, book, ch, vs, text, 'ARTICLE REGRESSION', 'CRITICAL', [m.group(0)],
                'Invalid English article before a consonant-sound human noun; release blocker.')

        broken = BROKENNESS.findall(text)
        if broken:
            add(rows, seen, book, ch, vs, text, 'BROKENNESS LEXICAL REVIEW', 'HIGH', sorted(set(x.lower() for x in broken)),
                'The English brokenness/broken wording may flatten distinct Greek senses and should be checked against source/context.')

        gm = GENERIC_MAN.findall(text)
        if gm:
            add(rows, seen, book, ch, vs, text, 'GENERIC-HUMAN HIGH PRIORITY', 'HIGH', sorted(set(x.lower() for x in gm)),
                'Universal/generic human language is explicitly male-coded and should be checked against Greek/Aramaic context for inclusive rendering.')
        elif MASC_TERM.search(text):
            add(rows, seen, book, ch, vs, text, 'MASCULINE TERM REVIEW', 'REVIEW', sorted(set(x.lower() for x in MASC_TERM.findall(text))),
                'Masculine English term present. Preserve if the referent is actually male; revise only if source/context is generic.')

        if BROTHER_TERM.search(text) and not INCLUSIVE_BROTHERS.search(text):
            add(rows, seen, book, ch, vs, text, 'BROTHERS / SIBLING LANGUAGE REVIEW', 'REVIEW', sorted(set(x.lower() for x in BROTHER_TERM.findall(text))),
                'Plural brother-language can sometimes represent Greek adelphoi addressing a mixed community, but can also denote actual men or male kin. Requires source/context review.')

        if SONS_TERM.search(text):
            add(rows, seen, book, ch, vs, text, 'SONS / CHILDREN LANGUAGE REVIEW', 'REVIEW', ['sons'],
                'Plural son-language can be literal male offspring or a source-language idiom/category whose intended scope may be broader. Requires source/context review; do not neutralize mechanically.')

        if GENERIC_STRONG.search(text) and PRON_RE.search(text):
            add(rows, seen, book, ch, vs, text, 'GENERIC PRONOUN HIGH PRIORITY', 'HIGH',
                [GENERIC_STRONG.search(text).group(0)] + sorted(set(x.lower() for x in PRON_RE.findall(text))),
                'A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.')
        elif GENERIC_SECONDARY.search(text) and PRON_RE.search(text):
            add(rows, seen, book, ch, vs, text, 'GENERIC PRONOUN REVIEW', 'REVIEW',
                [GENERIC_SECONDARY.search(text).group(0)] + sorted(set(x.lower() for x in PRON_RE.findall(text))),
                'A potentially generic antecedent is paired with masculine pronouns, but the referent may be specific. Context/source review required.')

        dh = divine_hits(text)
        if dh:
            add(rows, seen, book, ch, vs, text, 'DIVINE-REFERENT REVIEW', 'HIGH', dh,
                'Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.')

    OUT.mkdir(parents=True, exist_ok=True)
    fields = ['reference','book','chapter','verse','category','priority','signals','reason','text']
    with (OUT / 'candidates.tsv').open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t')
        w.writeheader()
        w.writerows(rows)

    with (OUT / 'all-verses.tsv').open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['reference','text'])
        for b, c, v, t in allv:
            w.writerow([f'{b} {c}:{v}', t])

    bycat = Counter(r['category'] for r in rows)
    bypri = Counter(r['priority'] for r in rows)
    bybook = defaultdict(Counter)
    verse_counts = Counter(b for b, _, _, _ in allv)
    for r in rows:
        bybook[r['book']][r['category']] += 1

    unique_candidate_verses = len({(r['book'], r['chapter'], r['verse']) for r in rows})
    summary = {
        'canonicalCommit': '91b6e7b9eb3f5a9f46efe63a04cedda1e49d527b',
        'canonicalEpubSha256': actual,
        'scope': 'All 27 New Testament books. Candidate scan only; rows are not automatically translation errors.',
        'methodNotes': [
            'Greek/Aramaic source and immediate literary context govern; English surface forms only identify review candidates.',
            'Actual male referents, historical men, male kinship, and Yeshua/Mashiach references are preserved when source/context is male-specific.',
            'Plural brothers/brethren are surfaced because Greek adelphoi can address mixed communities in some contexts; every occurrence still requires source/context review.',
            'Plural sons are surfaced because some constructions may have broader family/community scope; literal sons and male-specific expressions must remain male.',
            'Divine-pronoun surfacing is conservative and excludes Yeshua/Mashiach and ambiguous Lord references from heuristic classification.',
            'No Scripture is modified by this audit.'
        ],
        'extractedVerseCount': len(allv),
        'expectedNewTestamentVerseCount': EXPECTED_NT_VERSES,
        'verseCountValidation': 'PASS',
        'bookCount': len(BOOKS),
        'chapterCount': sum(EXPECTED_CHAPTERS.values()),
        'versesByBook': dict(verse_counts),
        'candidateRowCount': len(rows),
        'uniqueCandidateVerseCount': unique_candidate_verses,
        'countsByCategory': dict(bycat),
        'countsByPriority': dict(bypri),
        'countsByBook': {b: dict(c) for b, c in bybook.items()},
    }
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

    priority_order = {'CRITICAL': 0, 'HIGH': 1, 'REVIEW': 2}
    rows_sorted = sorted(rows, key=lambda r: (priority_order.get(r['priority'], 9), r['book'], int(r['chapter']), int(r['verse']), r['category']))
    md = []
    md.append('# New Testament Inclusive Language, Divine-Referent & Lexical Residual Audit')
    md.append('')
    md.append(f'- Canonical commit: `91b6e7b9eb3f5a9f46efe63a04cedda1e49d527b`')
    md.append(f'- Canonical EPUB SHA-256: `{actual}`')
    md.append(f'- Scope: all 27 New Testament books / {sum(EXPECTED_CHAPTERS.values())} chapters / {len(allv):,} verses')
    md.append(f'- Candidate rows: {len(rows):,} across {unique_candidate_verses:,} unique verses')
    md.append('- Important: candidates are review prompts, not a count of translation errors.')
    md.append('')
    md.append('## Category counts')
    md.append('')
    for cat, n in bycat.most_common():
        md.append(f'- **{cat}:** {n:,}')
    md.append('')
    md.append('## Priority counts')
    md.append('')
    for pri in ['CRITICAL','HIGH','REVIEW']:
        md.append(f'- **{pri}:** {bypri.get(pri,0):,}')
    md.append('')
    md.append('## Editorial guardrails')
    md.append('')
    md.append('- Do not convert every masculine word to neutral English. Preserve actual men, male kinship, male-specific social roles, and source-specific imagery.')
    md.append('- Check `adelphoi`/brother-language for mixed-community address; do not assume every plural “brothers” means “brothers and sisters.”')
    md.append('- Check “sons” constructions individually; some may denote a broader group, while others are intentionally male or idiomatic in ways that should be preserved.')
    md.append('- A masculine pronoun is changed under the project method only when its immediate referent is unmistakably divine; uncertain/Yeshua/Messianic references are not auto-resolved.')
    md.append('- The lexical “brokenness” category is a source-review flag, not a mandate to choose one replacement word everywhere.')
    md.append('')
    md.append('## High-priority queue')
    md.append('')
    high = [r for r in rows_sorted if r['priority'] in {'CRITICAL','HIGH'}]
    if not high:
        md.append('_No critical/high-priority candidates._')
    else:
        for r in high:
            md.append(f"### {r['reference']} — {r['category']}")
            md.append('')
            md.append(f"> {r['text']}")
            md.append('')
            md.append(f"Signals: `{r['signals']}`")
            md.append('')
            md.append(r['reason'])
            md.append('')
    md.append('## Book-by-book queue')
    md.append('')
    for book in BOOKS.values():
        cats = bybook.get(book, {})
        total = sum(cats.values())
        md.append(f"- **{book}:** {total:,} candidate rows" + (f" — " + ', '.join(f"{k}: {v}" for k, v in sorted(cats.items())) if total else ''))
    md.append('')
    (OUT / 'high-priority.md').write_text('\n'.join(md), encoding='utf-8')

    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
