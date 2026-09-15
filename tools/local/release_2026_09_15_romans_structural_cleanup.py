#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import json
import os
import re
import shutil
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import release_2026_09_14_lexicon_update_ai_cleanup as prior

base = prior.base
grammar = prior.grammar
ROOT = prior.ROOT
EPUB = prior.EPUB
REGISTRY = prior.REGISTRY
ROOT_README = prior.ROOT_README
CURRENT_README = prior.CURRENT_README
HISTORY_LOG = prior.HISTORY_LOG
REFRESH = prior.REFRESH

BASELINE = 'd48ec5b7da0db10c7c44c518793228dc5b2d69edc6e57de838486d2aefbcf62f'
LEDGER = ROOT / 'tools' / 'local' / 'approved_romans_structural_cleanup_2026_09_15.tsv'
REPORT = ROOT / 'change-logs' / 'reports' / '2026-09-15-romans-structural-cleanup.json'
NOTE = ROOT / 'editor-notes' / 'consistency' / '2026-09-15-romans-structural-cleanup.md'
RELEASE_NAME = 'Romans structural mapping and malformed-English correction'

NT_SLUGS = {
    'matthew','mark','luke','john','acts','romans','1-corinthians','2-corinthians','galatians','ephesians',
    'philippians','colossians','1-thessalonians','2-thessalonians','1-timothy','2-timothy','titus','philemon',
    'hebrews','james','1-peter','2-peter','1-john','2-john','3-john','jude','revelation'
}
ROMANS_COUNTS = {1:32,2:29,3:31,4:25,5:21,6:23,7:25,8:39,9:33,10:21,11:36,12:21,13:14,14:23,15:33,16:27}

BEFORE = {
    (5,19): "For as through the one a person's disobedience many were made sinners, even so through the obedience of the one, many will be made righteous.",
    (8,9): "But you are not in the flesh but in the Ruach, if it is so that the Ruach of God dwells in you. But if anyone doesn't have the Ruach of Messiah, they are not their.",
    (14,2): "One a person has faith to eat all things, but the one who is weak eats only vegetables.",
    (14,23): "But the one who doubts is condemned if they eat, because it isn't of faith; and whatever is not of faith is sin. (14:24) Now to the one who is able to establish you according to my good news and the preaching of Yeshua the Messiah, according to the revelation of the mystery which has been kept secret through long ages, (14:25) but now is revealed, and by the Scriptures of the prophets, according to the commandment of the age-enduring God, is made known for obedience of faith to all the nations; (14:26) to the only wise God, through Yeshua the Messiah, to whom be the glory forever! Amen.",
    (16,25): "",
    (16,26): "016:027",
}
AFTER = {
    (5,19): "For as through the disobedience of one person many were made sinners, even so through the obedience of the one, many will be made righteous.",
    (8,9): "But you are not in the flesh but in the Ruach, if it is so that the Ruach of God dwells in you. But if anyone doesn't have the Ruach of Messiah, they do not belong to Messiah.",
    (14,2): "One person has faith to eat all things, but the one who is weak eats only vegetables.",
    (14,23): "But the one who doubts is condemned if they eat, because it isn't of faith; and whatever is not of faith is sin.",
    (16,25): "Now to the one who is able to establish you according to my good news and the preaching of Yeshua the Messiah, according to the revelation of the mystery which has been kept secret through long ages,",
    (16,26): "but now is revealed, and by the Scriptures of the prophets, according to the commandment of the age-enduring God, is made known for obedience of faith to all the nations;",
    (16,27): "to the only wise God, through Yeshua the Messiah, to whom be the glory forever! Amen.",
}


def collapse(value: str) -> str:
    return re.sub(r'\s+', ' ', value or '').strip()


def plain_inner(inner: str, verse: int) -> str:
    text = re.sub(r'<[^>]+>', ' ', inner)
    text = collapse(html.unescape(text))
    return re.sub(rf'^\s*{verse}\.\s*', '', text, count=1)


def verse_pattern(chapter: int, verse: int) -> re.Pattern[str]:
    return re.compile(
        rf'(<p\b(?=[^>]*\bid=["\']v-romans-{chapter}-{verse}["\'])[^>]*>)(.*?)(</p>)',
        re.I | re.S,
    )


def get_verse(text: str, chapter: int, verse: int) -> str | None:
    matches = list(verse_pattern(chapter, verse).finditer(text))
    if not matches:
        return None
    if len(matches) != 1:
        raise RuntimeError(f'Romans {chapter}:{verse} element count={len(matches)}')
    return plain_inner(matches[0].group(2), verse)


def replace_verse(text: str, chapter: int, verse: int, before: str, after: str) -> str:
    pat = verse_pattern(chapter, verse)
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f'Romans {chapter}:{verse} element count={len(matches)}')
    m = matches[0]
    actual = plain_inner(m.group(2), verse)
    if actual != before:
        raise RuntimeError(f'Romans {chapter}:{verse} before mismatch\nEXPECTED: {before}\nACTUAL:   {actual}')
    new_inner = f'{verse}. {html.escape(after, quote=False)}'
    return text[:m.start()] + m.group(1) + new_inner + m.group(3) + text[m.end():]


def insert_16_27(text: str) -> str:
    if get_verse(text, 16, 27) is not None:
        raise RuntimeError('Romans 16:27 already exists before insertion')
    pat = verse_pattern(16, 26)
    matches = list(pat.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f'Romans 16:26 element count before insertion={len(matches)}')
    m = matches[0]
    new_p = f'\n<p id="v-romans-16-27" data-verse="27">27. {html.escape(AFTER[(16,27)], quote=False)}</p>'
    return text[:m.end()] + new_p + text[m.end():]


def load_ledger() -> list[dict[str,str]]:
    with LEDGER.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    if len(rows) != 7:
        raise RuntimeError(f'approved Romans ledger row count={len(rows)}, expected 7')
    expected_refs = {'Romans 5:19','Romans 8:9','Romans 14:2','Romans 14:23','Romans 16:25','Romans 16:26','Romans 16:27'}
    refs = {f"{r['book']} {r['chapter']}:{r['verse']}" for r in rows}
    if refs != expected_refs:
        raise RuntimeError(f'approved Romans ledger refs mismatch: {sorted(refs)}')
    return rows


def collect_verse_ids(path: Path):
    all_ids=[]
    nt_ids=[]
    rx=re.compile(r'\bid=["\']v-([a-z0-9-]+)-(\d+)-(\d+)["\']', re.I)
    with zipfile.ZipFile(path) as z:
        bad=z.testzip()
        if bad:
            raise RuntimeError(f'EPUB CRC failure: {bad}')
        for info in z.infolist():
            if not info.filename.lower().endswith(('.xhtml','.html','.htm')):
                continue
            try:
                text=z.read(info.filename).decode('utf-8')
            except UnicodeDecodeError:
                continue
            for slug,ch,vs in rx.findall(text):
                ref=(slug.lower(),int(ch),int(vs))
                all_ids.append(ref)
                if slug.lower() in NT_SLUGS:
                    nt_ids.append(ref)
    return all_ids, nt_ids


def validate_inventory(path: Path, expected_nt: int):
    all_ids, nt_ids = collect_verse_ids(path)
    if len(all_ids) != len(set(all_ids)):
        raise RuntimeError('duplicate verse ids exist in EPUB')
    if len(nt_ids) != len(set(nt_ids)):
        raise RuntimeError('duplicate New Testament verse ids exist in EPUB')
    if len(nt_ids) != expected_nt:
        raise RuntimeError(f'New Testament verse paragraph count {len(nt_ids)} != {expected_nt}')
    if len(all_ids) != 23145 + expected_nt:
        raise RuntimeError(f'whole-Bible verse paragraph count {len(all_ids)} != {23145 + expected_nt}')


def validate_romans(path: Path, which: str):
    with zipfile.ZipFile(path) as z:
        member=base.find_book_member(z,'romans')
        text=z.read(member).decode('utf-8')
    if which == 'before':
        for ref,before in BEFORE.items():
            actual=get_verse(text,*ref)
            if actual != before:
                raise RuntimeError(f'pre-release Romans {ref[0]}:{ref[1]} mismatch expected={before!r} actual={actual!r}')
        if get_verse(text,16,27) is not None:
            raise RuntimeError('pre-release Romans 16:27 unexpectedly exists')
        return

    for ref,after in AFTER.items():
        actual=get_verse(text,*ref)
        if actual != after:
            raise RuntimeError(f'post-release Romans {ref[0]}:{ref[1]} mismatch expected={after!r} actual={actual!r}')
    expected_ids={(ch,vs) for ch,count in ROMANS_COUNTS.items() for vs in range(1,count+1)}
    actual_ids={(int(ch),int(vs)) for ch,vs in re.findall(r'\bid=["\']v-romans-(\d+)-(\d+)["\']',text,re.I)}
    if actual_ids != expected_ids:
        missing=sorted(expected_ids-actual_ids)
        extra=sorted(actual_ids-expected_ids)
        raise RuntimeError(f'Romans canonical verse IDs invalid missing={missing} extra={extra}')
    if len(actual_ids) != 433:
        raise RuntimeError(f'Romans verse paragraph count {len(actual_ids)} != 433')
    if any(x in get_verse(text,14,23) for x in ('(14:24)','(14:25)','(14:26)')):
        raise RuntimeError('embedded Romans 14 doxology labels remain')
    if '016:027' in text:
        raise RuntimeError('literal Romans 016:027 artifact remains')
    if get_verse(text,16,24) != 'The grace of our Master Yeshua the Messiah be with you all! Amen.':
        raise RuntimeError('Romans 16:24 changed unexpectedly')


def rewrite_epub() -> str:
    with zipfile.ZipFile(EPUB,'r') as zin:
        infos=zin.infolist()
        original={i.filename:zin.read(i.filename) for i in infos}
        romans_member=base.find_book_member(zin,'romans')
    edited=dict(original)
    text=edited[romans_member].decode('utf-8')
    for ref in [(5,19),(8,9),(14,2),(14,23),(16,25),(16,26)]:
        text=replace_verse(text,*ref,BEFORE[ref],AFTER[ref])
    text=insert_16_27(text)
    edited[romans_member]=text.encode('utf-8')

    fd,tmpname=tempfile.mkstemp(prefix='the-way-romans-',suffix='.epub',dir=EPUB.parent)
    os.close(fd)
    tmp=Path(tmpname)
    try:
        with zipfile.ZipFile(tmp,'w') as zout:
            for info in infos:
                zout.writestr(info,edited[info.filename],compress_type=info.compress_type)
        base.validate_epub(tmp)
        changed=sorted(name for name in original if original[name] != edited[name])
        if changed != [romans_member]:
            raise RuntimeError(f'changed EPUB members mismatch expected={[romans_member]} actual={changed}')
        shutil.move(tmp,EPUB)
    finally:
        if tmp.exists():
            tmp.unlink()
    return romans_member


def main():
    ledger=load_ledger()
    actual=base.sha256(EPUB)
    if actual != BASELINE:
        raise SystemExit(f'baseline SHA mismatch expected={BASELINE} got={actual}')

    validate_inventory(EPUB,7956)
    validate_romans(EPUB,'before')
    pre_articles, pre_exceptions=grammar.audit_epub(EPUB)
    if pre_articles:
        raise RuntimeError('pre-release English article audit not clean: '+json.dumps(pre_articles[:30],ensure_ascii=False,indent=2))

    now=datetime.now(timezone.utc)
    stamp=now.strftime('%Y-%m-%d_%H%MUTC')
    generated=now.replace(microsecond=0).isoformat().replace('+00:00','Z')
    archive_dir=ROOT/'rendered-documents-history'/stamp
    archive_dir.mkdir(parents=True,exist_ok=False)
    archive=archive_dir/EPUB.name
    shutil.copy2(EPUB,archive)
    if base.sha256(archive) != BASELINE:
        raise RuntimeError('archive SHA mismatch')

    changed_member=rewrite_epub()
    newsha=base.sha256(EPUB)
    if newsha == BASELINE:
        raise RuntimeError('EPUB SHA did not change')

    validate_inventory(EPUB,7957)
    validate_romans(EPUB,'after')
    post_articles, post_exceptions=grammar.audit_epub(EPUB)
    if post_articles:
        raise RuntimeError('article inconsistencies introduced: '+json.dumps(post_articles[:30],ensure_ascii=False,indent=2))
    if len(post_exceptions) != len(pre_exceptions):
        raise RuntimeError(f'pronunciation article exception inventory changed before={len(pre_exceptions)} after={len(post_exceptions)}')

    with zipfile.ZipFile(EPUB) as z:
        corpus='\n'.join(z.read(i.filename).decode('utf-8','ignore') for i in z.infolist() if i.filename.lower().endswith(('.xhtml','.html','.htm')))
    forbidden=["the one a person's disobedience",'they are not their','One a person has faith','016:027','(14:24) Now to the one who is able']
    remains=[x for x in forbidden if x in corpus]
    if remains:
        raise RuntimeError(f'residual malformed/structural strings remain: {remains}')

    registry=json.loads(REGISTRY.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256') != BASELINE:
        raise RuntimeError('registry baseline SHA mismatch')
    registry['canonicalEpubSha256']=newsha
    REGISTRY.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fallback=base.build_fallback(EPUB,registry,newsha,generated)
    for key,expected in [('bookCount',66),('chapterCount',1189),('verseSearchCount',31102)]:
        if key in fallback and fallback[key] != expected:
            raise RuntimeError(f'fallback {key} mismatch {fallback[key]} != {expected}')

    changes=[]
    for row in ledger:
        changes.append({
            'reference':f"{row['book']} {row['chapter']}:{row['verse']}",
            'category':row['category'],
            'before':row['before'],
            'after':row['after'],
        })

    report={
        'release':RELEASE_NAME,
        'prior_epub_sha256':BASELINE,
        'released_epub_sha256':newsha,
        'archive_path':archive.relative_to(ROOT).as_posix(),
        'affected_verse_records':7,
        'malformed_english_corrections':3,
        'structural_mapping_records':4,
        'romans_verse_paragraphs_before':432,
        'romans_verse_paragraphs_after':433,
        'new_testament_verse_paragraphs_before':7956,
        'new_testament_verse_paragraphs_after':7957,
        'whole_bible_verse_paragraphs_after':31102,
        'changed_epub_member':changed_member,
        'article_mismatch_count':len(post_articles),
        'mobileFallback':fallback,
        'changes':changes,
        'method':'Finite approved Romans ledger. Three malformed-English repairs plus a structural relocation of the already-present doxology from an embedded Romans 14:23 artifact into Romans 16:25-27. Romans 16:24 is preserved. No other Scripture text is changed.',
        'textual_note':'The manuscript tradition varies on placement of the closing doxology. This release does not adjudicate that textual-critical question; it restores the project canonical data structure to Romans 16:25-27 while preserving the project’s existing doxology wording and Romans 16:24.'
    }
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    NOTE.parent.mkdir(parents=True,exist_ok=True)
    NOTE.write_text(f'''# {RELEASE_NAME} — 2026-09-15\n\n## Scope\n\nThis is a narrow, controlled correction release arising from the New Testament residual audit. It changes only Romans and only the seven approved verse records in `tools/local/approved_romans_structural_cleanup_2026_09_15.tsv`.\n\n### Malformed English\n\n- **Romans 5:19** — repaired “through the one a person's disobedience” to “through the disobedience of one person.”\n- **Romans 8:9** — repaired “they are not their” to “they do not belong to Messiah,” preserving an inclusive `anyone/they` subject while keeping the specific Messiah referent explicit.\n- **Romans 14:2** — repaired “One a person has faith…” to “One person has faith…”.\n\n### Romans verse mapping\n\nThe previous EPUB had **432** Romans verse paragraphs rather than the expected **433**. Romans 14:23 improperly contained parenthetical `(14:24)`, `(14:25)`, and `(14:26)` labels plus the closing doxology; Romans 16:25 was empty; Romans 16:26 contained the literal artifact `016:027`; and Romans 16:27 did not exist as a verse paragraph.\n\nThis release:\n\n- restores Romans 14:23 to verse 23 only;\n- places the already-present doxology text into **Romans 16:25–27**;\n- preserves **Romans 16:24** unchanged;\n- removes the `016:027` artifact;\n- restores the New Testament to **7,957 / 7,957 canonical verse paragraphs** and the full Bible to **31,102** verse paragraphs.\n\nThe manuscript tradition contains more than one placement for the closing Romans doxology. This release does **not** claim to settle that textual-critical question. It normalizes the project’s canonical data structure to Romans 16:25–27 while preserving the doxology wording already present in The Way Version.\n\n## QA\n\n- Previous EPUB SHA-256: `{BASELINE}`\n- Released EPUB SHA-256: `{newsha}`\n- Previous EPUB archived at `{archive.relative_to(ROOT).as_posix()}`\n- Romans verse paragraphs: **432 → 433**\n- New Testament verse paragraphs: **7,956 → 7,957**\n- Whole-Bible verse paragraphs: **31,102**\n- EPUB ZIP/XML/internal-link validation: **pass**\n- Exact approved before/after ledger: **pass**\n- English article audit: **0 actionable mismatches**\n- Canonical mobile fallback regenerated from the finished EPUB\n\n## Downstream rule\n\nWebsite, web reader, EPUB downloads, mobile content feed, and native mobile release pin must consume this exact canonical EPUB. No downstream Scripture hand-editing.\n''',encoding='utf-8')

    base.append_once(HISTORY_LOG,newsha,f'- **{stamp}** — {RELEASE_NAME}: 3 malformed-English repairs plus Romans doxology/verse mapping normalization; NT canonical verse paragraphs restored 7,956 → 7,957. Prior EPUB archived at `{archive.relative_to(ROOT).as_posix()}`; new SHA-256 `{newsha}`.')
    base.append_once(REFRESH,'## 2026-09-15 Romans structural mapping and malformed-English correction',f'''## 2026-09-15 Romans structural mapping and malformed-English correction\n\nNarrow Romans-only release: corrected malformed English at Romans 5:19, 8:9, and 14:2; restored Romans 14:23 and Romans 16:25–27 to a coherent verse structure while preserving Romans 16:24 and the existing doxology wording. New Testament verse paragraphs are now 7,957 / 7,957. Canonical SHA-256: `{newsha}`. See `../editor-notes/consistency/2026-09-15-romans-structural-cleanup.md` and `../change-logs/reports/2026-09-15-romans-structural-cleanup.json`.''')
    base.replace_sha_in_file(ROOT_README,BASELINE,newsha)
    base.replace_sha_in_file(CURRENT_README,BASELINE,newsha)

    print(json.dumps({
        'release':RELEASE_NAME,
        'releasedEpubSha256':newsha,
        'affectedVerseRecords':7,
        'malformedEnglishCorrections':3,
        'romansVerseParagraphs':433,
        'newTestamentVerseParagraphs':7957,
        'wholeBibleVerseParagraphs':31102,
        'articleMismatches':len(post_articles),
        'fallbackContentSha256':fallback.get('contentSha256'),
        'fallbackBytes':fallback.get('contentBytes'),
        'changedMember':changed_member,
    },indent=2))


if __name__=='__main__':
    main()
