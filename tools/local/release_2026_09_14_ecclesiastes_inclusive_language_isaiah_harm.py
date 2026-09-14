#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import release_2026_09_14_psalms_proverbs_inclusive_pronouns as prev

base = prev.base
grammar = prev.grammar
ROOT = prev.ROOT
EPUB = prev.EPUB
REGISTRY = prev.REGISTRY
ROOT_README = prev.ROOT_README
CURRENT_README = prev.CURRENT_README
HISTORY_LOG = prev.HISTORY_LOG
FALLBACK_DIR = prev.FALLBACK_DIR
REFRESH = prev.REFRESH

BASELINE = 'feb0a7ad83de3c31df389a61db02dda4b5eecf2655caaad7cda4be911df3f55a'
REPORT = ROOT / 'change-logs' / 'reports' / '2026-09-14-ecclesiastes-inclusive-language-isaiah-harm.json'
NOTE = ROOT / 'editor-notes' / 'consistency' / '2026-09-14-ecclesiastes-inclusive-language-isaiah-harm.md'

# Finite reviewed ledger. The Ecclesiastes pass is source-sensitive:
# - generic proverbial/human references use inclusive English;
# - actual male figures, male kinship, kings, the male Preacher, and the explicit
#   man/woman contrast in Ecclesiastes 7:28 remain gendered;
# - unmistakable divine masculine pronouns repeat Elohim rather than introducing
#   divine they/she/it;
# - Hebrew ra/ra'ah is rendered by context (wrong, harm, misfortune, sorrow,
#   bad, etc.) instead of mechanically flattening every occurrence to
#   "brokenness".
# Isaiah 1:16 is included as a separately requested lexical correction:
# ra' / harea' describes harmful/evil deeds; this release uses "harm".
CHANGES = [
    ('ecclesiastes', 2, 19, 'generic',
     'Who knows whether they will be a wise person or a fool? Yet he will have rule over all of my labor in which I have labored, and in which I have shown myself wise under the sun. This also is vanity.',
     'Who knows whether they will be a wise person or a fool? Yet they will have rule over all of my labor in which I have labored, and in which I have shown myself wise under the sun. This also is vanity.'),
    ('ecclesiastes', 2, 21, 'lexical',
     'For there is a person whose labor is with wisdom, with knowledge, and with skillfulness; yet they shall leave it for their portion to a person who has not labored for it. This also is vanity and a great brokenness.',
     'For there is a person whose labor is with wisdom, with knowledge, and with skillfulness; yet they shall leave it for their portion to a person who has not labored for it. This also is vanity and a great misfortune.'),
    ('ecclesiastes', 2, 26, 'divine',
     'For to the one who pleases him, Elohim gives wisdom, knowledge, and joy; but to the sinner they give travail, to gather and to heap up, that they may give to the one who pleases Elohim. This also is vanity and a chasing after wind.',
     'For to the one who pleases Elohim, Elohim gives wisdom, knowledge, and joy; but to the sinner Elohim gives travail, to gather and to heap up, that they may give to the one who pleases Elohim. This also is vanity and a chasing after wind.'),
    ('ecclesiastes', 3, 11, 'grammar',
     "Elohim has made everything beautiful in its time. The Elohim has also set eternity in their hearts, yet so that a person can't find out the work that Elohim has done from the beginning even to the end.",
     "Elohim has made everything beautiful in its time. Elohim has also set eternity in their hearts, yet so that a person can't find out the work that Elohim has done from the beginning even to the end."),
    ('ecclesiastes', 4, 3, 'lexical',
     'Yes, better than them both is the one who has not yet been, who has not seen the work of brokenness that is done under the sun.',
     'Yes, better than them both is the one who has not yet been, who has not seen the harm that is done under the sun.'),
    ('ecclesiastes', 4, 8, 'generic',
     'There is one who is alone, and they have neither son nor brother. There is no end to all of his labor, neither are his eyes satisfied with wealth. For whom then, do I labor, and deprive my soul of enjoyment? This also is vanity, yes, it is a miserable business.',
     'There is one who is alone, and they have neither son nor brother. There is no end to all of their labor, neither are their eyes satisfied with wealth. For whom then, do I labor, and deprive my soul of enjoyment? This also is vanity, yes, it is a miserable business.'),
    ('ecclesiastes', 4, 10, 'generic',
     "For if they fall, the one will lift up his fellow; but woe to the one who is alone when they fall, and doesn't have another to lift them up.",
     "For if they fall, one will lift up the other; but woe to the one who is alone when they fall, and doesn't have another to lift them up."),
    ('ecclesiastes', 5, 1, 'lexical',
     "Guard your steps when you go to Elohim's house; for to draw near to listen is better than to give the sacrifice of fools, for they don't know that they do brokenness.",
     "Guard your steps when you go to Elohim's house; for to draw near to listen is better than to give the sacrifice of fools, for they don't know that they do wrong."),
    ('ecclesiastes', 5, 11, 'generic',
     'When goods increase, those who eat them are increased; and what advantage is there to its owner, except to feast on them with his eyes?',
     'When goods increase, those who eat them are increased; and what advantage is there to its owner, except to feast on them with their eyes?'),
    ('ecclesiastes', 5, 13, 'mixed',
     'There is a grievous brokenness which I have seen under the sun: wealth kept by its owner to his harm.',
     'There is a grievous misfortune which I have seen under the sun: wealth kept by its owner to their harm.'),
    ('ecclesiastes', 5, 16, 'lexical',
     'This also is a grievous brokenness, that in all points as they came, so shall they go. And what profit do they have who labor for the wind?',
     'This also is a grievous misfortune, that in all points as they came, so shall they go. And what profit do they have who labor for the wind?'),
    ('ecclesiastes', 6, 1, 'mixed',
     'There is a brokenness which I have seen under the sun, and it is heavy on men:',
     'There is a misfortune I have seen under the sun, and it weighs heavily on humanity:'),
    ('ecclesiastes', 6, 3, 'generic',
     'If someone fathers a hundred children, and lives many years, so that the days of their years are many, but their soul is not filled with good, and moreover they have no burial; I say, that an untimely birth is better than he:',
     'If someone has a hundred children, and lives many years, so that the days of their years are many, but their soul is not filled with good, and moreover they have no burial; I say that a stillbirth is better off than they are:'),
    ('ecclesiastes', 6, 6, 'generic',
     "Yes, though he live a thousand years twice told, and yet fails to enjoy good, don't all go to one place?",
     "Yes, though they live a thousand years twice told, and yet fail to enjoy good, don't all go to one place?"),
    ('ecclesiastes', 7, 15, 'lexical',
     'All this have I seen in my days of vanity: there is a righteous person who perishes in their righteousness, and there is a broken person who lives long in their brokenness-doing.',
     'All this have I seen in my days of vanity: there is a righteous person who perishes in their righteousness, and there is a wicked person who lives long in their wrongdoing.'),
    ('ecclesiastes', 8, 6, 'generic',
     'For there is a time and procedure for every purpose, although the misery of a person is heavy on him.',
     'For there is a time and procedure for every purpose, although the misery of a person is heavy on them.'),
    ('ecclesiastes', 8, 7, 'generic',
     "For he doesn't know that which will be; for who can tell him how it will be?",
     "For they don't know what will be; for who can tell them how it will be?"),
    ('ecclesiastes', 8, 9, 'mixed',
     'All this have I seen, and applied my mind to every work that is done under the sun. There is a time in which one a person has power over another to their hurt.',
     'All this have I seen, and applied my mind to every work that is done under the sun. There is a time in which one person has power over another to their harm.'),
    ('ecclesiastes', 8, 11, 'lexical',
     'Because sentence against a work of brokenness is not executed speedily, therefore the heart of the human beings is fully set in them to do brokenness.',
     'Because sentence against a harmful deed is not executed speedily, the hearts of human beings are fully set on doing harm.'),
    ('ecclesiastes', 8, 13, 'generic',
     "But it shall not be well with the wicked, neither shall he lengthen days like a shadow; because he doesn't revere Elohim.",
     "But it shall not be well with the wicked person, neither shall they lengthen their days like a shadow, because they don't revere Elohim."),
    ('ecclesiastes', 8, 14, 'generic',
     'There is a vanity which is done on the earth, that there are righteous men to whom it happens according to the work of the wicked. Again, there are wicked men to whom it happens according to the work of the righteous. I said that this also is vanity.',
     'There is a vanity which is done on the earth, that there are righteous people to whom it happens according to the work of the wicked. Again, there are wicked people to whom it happens according to the work of the righteous. I said that this also is vanity.'),
    ('ecclesiastes', 8, 16, 'generic',
     'When I applied my heart to know wisdom, and to see the business that is done on the earth (for also there is that neither day nor night sees sleep with his eyes),',
     'When I applied my heart to know wisdom, and to see the business that is done on the earth (for there are those whose eyes see no sleep by day or night),'),
    ('ecclesiastes', 9, 3, 'lexical',
     'This is a brokenness in all that is done under the sun, that there is one event to all: yes also, the heart of the human beings is full of brokenness, and madness is in their heart while they live, and after that they go to the dead.',
     'This is a grievous thing in all that is done under the sun: there is one event to all; yes, the hearts of human beings are full of wrongdoing, and madness is in their hearts while they live, and after that they go to the dead.'),
    ('ecclesiastes', 9, 9, 'divine',
     'Live joyfully with the wife whom you love all the days of your life of vanity, which he has given you under the sun, all your days of vanity: for that is your portion in life, and in your labor in which you labor under the sun.',
     'Live joyfully with the wife whom you love all the days of your life of vanity, which Elohim has given you under the sun, all your days of vanity: for that is your portion in life, and in your labor in which you labor under the sun.'),
    ('ecclesiastes', 9, 12, 'lexical',
     "For a person also doesn't know their time. As the fish that are taken in a brokenness net, and as the birds that are caught in the snare, even so are the human beings snared in a time of trouble, when it falls suddenly on them.",
     "For a person also doesn't know their time. As the fish that are taken in a deadly net, and as the birds that are caught in the snare, even so are the human beings snared in a time of trouble, when it falls suddenly on them."),
    ('ecclesiastes', 9, 14, 'generic',
     'There was a little city, and few men within it; and a great king came against it, besieged it, and built great bulwarks against it.',
     'There was a little city, and few people within it; and a great king came against it, besieged it, and built great bulwarks against it.'),
    ('ecclesiastes', 10, 1, 'lexical',
     'Dead flies cause the oil of the perfumer to send forth a brokenness odor; so does a little folly outweigh wisdom and honor.',
     'Dead flies cause the oil of the perfumer to send forth a foul odor; so does a little folly outweigh wisdom and honor.'),
    ('ecclesiastes', 10, 5, 'lexical',
     'There is a brokenness which I have seen under the sun, the sort of error which proceeds from the ruler.',
     'There is an error I have seen under the sun, the sort of mistake that proceeds from a ruler.'),
    ('ecclesiastes', 10, 10, 'generic',
     "If the axe is blunt, and one doesn't sharpen the edge, then he must use more strength; but skill brings success.",
     "If the axe is blunt, and one doesn't sharpen the edge, then they must use more strength; but skill brings success."),
    ('ecclesiastes', 10, 13, 'generic',
     'The beginning of the words of his mouth is foolishness; and the end of his talk is mischievous madness.',
     'The beginning of the words of their mouth is foolishness; and the end of their talk is mischievous madness.'),
    ('ecclesiastes', 10, 14, 'generic',
     "A fool also multiplies words. Man doesn't know what will be; and that which will be after him, who can tell him?",
     "A fool also multiplies words. A person doesn't know what will be; and that which will be after them, who can tell them?"),
    ('ecclesiastes', 10, 15, 'generic',
     "The labor of fools wearies every one of them; for he doesn't know how to go to the city.",
     "The labor of fools wearies every one of them; for they don't know how to go to the city."),
    ('ecclesiastes', 11, 2, 'lexical',
     "Give a portion to seven, yes, even to eight; for you don't know what brokenness will be on the earth.",
     "Give a portion to seven, yes, even to eight; for you don't know what misfortune may come upon the earth."),
    ('ecclesiastes', 11, 10, 'lexical',
     'Therefore remove sorrow from your heart, and put away brokenness from your flesh; for youth and the dawn of life are vanity.',
     'Therefore remove worry from your heart, and put away pain from your body; for youth and the dawn of life are vanity.'),
    ('ecclesiastes', 12, 1, 'lexical',
     'Remember also your Creator in the days of your youth, before the brokenness days come, and the years draw near, when you will say, "I have no pleasure in them;"',
     'Remember also your Creator in the days of your youth, before the days of sorrow come, and the years draw near, when you will say, "I have no pleasure in them;"'),
    ('ecclesiastes', 12, 14, 'lexical',
     'For Elohim will bring every work into judgment, with every hidden thing, whether it is good, or whether it is brokenness.',
     'For Elohim will bring every work into judgment, with every hidden thing, whether it is good, or whether it is bad.'),
    ('isaiah', 1, 16, 'lexical',
     'Wash yourselves, make yourself clean. Put away the brokenness of your doings from before my eyes. Cease to do brokenness.',
     'Wash yourselves, make yourselves clean. Put away the harm of your doings from before my eyes. Cease doing harm.'),
]

PRESERVED = [
    {'reference':'Ecclesiastes 4:14-16','reason':'The youth/king sequence is a specific royal male referent; masculine pronouns retained.'},
    {'reference':'Ecclesiastes 5:14-15','reason':'The immediate hypothetical explicitly describes someone who begets/fathers a son; retained rather than mechanically neutralized.'},
    {'reference':'Ecclesiastes 7:28','reason':'The verse explicitly contrasts a man and a woman; gender is semantically meaningful and retained.'},
    {'reference':'Ecclesiastes 8:3-4','reason':'Masculine pronouns refer to the king in the immediate royal context; retained.'},
    {'reference':'Ecclesiastes 12:9','reason':'Masculine pronouns refer to the male Preacher/narrator established in the book; retained.'},
    {'reference':'Ecclesiastes 12:12','reason':'Direct "my son" address retained as a source-marked kinship/student address rather than mechanically neutralized.'},
]

BOOK_NAME = {'ecclesiastes':'Ecclesiastes','isaiah':'Isaiah'}

def fmt_ref(slug: str, chapter: int, verse: int) -> str:
    return f'{BOOK_NAME[slug]} {chapter}:{verse}'


def collect(path: Path):
    return prev.collect_verses(path, slugs=('ecclesiastes','isaiah'))


def validate_inventory(path: Path, which: str):
    verse_map = collect(path)
    errors = []
    for slug, chapter, verse, category, before, after in CHANGES:
        expected = before if which == 'before' else after
        actual = verse_map.get((slug, chapter, verse))
        if actual != expected:
            errors.append({'reference':fmt_ref(slug, chapter, verse),'expected':expected,'actual':actual})
    if errors:
        raise RuntimeError(f'{which} inventory mismatch ({len(errors)} rows):\n' + json.dumps(errors[:30], ensure_ascii=False, indent=2))


def rewrite_epub():
    by_slug = defaultdict(list)
    for row in CHANGES:
        by_slug[row[0]].append(row)
    with zipfile.ZipFile(EPUB, 'r') as zin:
        infos = zin.infolist()
        original = {info.filename: zin.read(info.filename) for info in infos}
    edited = dict(original)
    expected_members = []
    with zipfile.ZipFile(EPUB, 'r') as z:
        for slug, rows in by_slug.items():
            member = base.find_book_member(z, slug)
            expected_members.append(member)
            text = edited[member].decode('utf-8')
            for _slug, chapter, verse, _category, before, after in rows:
                text = prev.replace_one_verse(text, slug, chapter, verse, before, after)
            edited[member] = text.encode('utf-8')
    fd, tmpname = tempfile.mkstemp(suffix='.epub', dir=str(EPUB.parent))
    os.close(fd)
    tmp = Path(tmpname)
    try:
        with zipfile.ZipFile(tmp, 'w') as zout:
            for info in infos:
                zout.writestr(info, edited[info.filename], compress_type=info.compress_type)
        base.validate_epub(tmp)
        shutil.move(tmp, EPUB)
    finally:
        if tmp.exists():
            tmp.unlink()
    changed_members = sorted(name for name in original if original[name] != edited[name])
    if changed_members != sorted(expected_members):
        raise RuntimeError(f'unexpected EPUB members changed: {changed_members}; expected {sorted(expected_members)}')
    return changed_members


def escape_md(value: str) -> str:
    return value.replace('|', '\\|').replace('\n', ' ')


def main():
    actual = base.sha256(EPUB)
    if actual != BASELINE:
        raise SystemExit(f'baseline SHA mismatch: expected {BASELINE}, got {actual}')

    pre_articles, pre_exceptions = grammar.audit_epub(EPUB)
    if pre_articles:
        raise RuntimeError('pre-release article audit is not clean: ' + json.dumps(pre_articles[:30], indent=2))

    refs = [(s,c,v) for s,c,v,*_ in CHANGES]
    if len(refs) != len(set(refs)):
        raise RuntimeError('duplicate verse references in reviewed ledger')
    if any(slug not in {'ecclesiastes','isaiah'} for slug,*_ in CHANGES):
        raise RuntimeError('release ledger escaped Ecclesiastes/Isaiah scope')
    isaiah_rows = [x for x in CHANGES if x[0] == 'isaiah']
    if [(x[1],x[2]) for x in isaiah_rows] != [(1,16)]:
        raise RuntimeError('Isaiah scope must be exactly 1:16')

    validate_inventory(EPUB, 'before')

    now = datetime.now(timezone.utc)
    stamp = now.strftime('%Y-%m-%d_%H%MUTC')
    generated = now.replace(microsecond=0).isoformat().replace('+00:00','Z')
    archive_dir = ROOT / 'rendered-documents-history' / stamp
    archive_dir.mkdir(parents=True, exist_ok=False)
    archive = archive_dir / EPUB.name
    shutil.copy2(EPUB, archive)
    if base.sha256(archive) != BASELINE:
        raise RuntimeError('archive SHA mismatch')

    changed_members = rewrite_epub()
    newsha = base.sha256(EPUB)
    if newsha == BASELINE:
        raise RuntimeError('EPUB SHA did not change')
    validate_inventory(EPUB, 'after')

    post_articles, post_exceptions = grammar.audit_epub(EPUB)
    if post_articles:
        raise RuntimeError('article inconsistencies introduced by release: ' + json.dumps(post_articles[:30], indent=2))
    if len(post_exceptions) != len(pre_exceptions):
        raise RuntimeError(f'pronunciation-based article exception inventory changed unexpectedly: before={len(pre_exceptions)} after={len(post_exceptions)}')

    verse_map = collect(EPUB)
    malformed = []
    for key, text in verse_map.items():
        if re.search(r'\ban\s+person\b|\ba\s+(?:individual|upright)\b', text, re.I):
            malformed.append((key,text))
    if malformed:
        raise RuntimeError('article regression in reviewed books: ' + json.dumps(malformed[:20], ensure_ascii=False, indent=2))

    registry = json.loads(REGISTRY.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256') != BASELINE:
        raise RuntimeError('registry baseline SHA mismatch')
    registry['canonicalEpubSha256'] = newsha
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    fallback = base.build_fallback(EPUB, registry, newsha, generated)

    counts = Counter(row[3] for row in CHANGES)
    rows = []
    for slug, chapter, verse, category, before, after in CHANGES:
        rows.append({'reference':fmt_ref(slug,chapter,verse),'book':slug,'chapter':chapter,'verse':verse,'category':category,'before':before,'after':after})

    report = {
        'release':'2026-09-14 Ecclesiastes inclusive language + Isaiah 1:16 harm wording',
        'scope':'Whole-book Ecclesiastes review for generic-human/divine-pronoun consistency and context-sensitive ra/raah renderings; Isaiah limited to 1:16.',
        'prior_epub_sha256':BASELINE,
        'released_epub_sha256':newsha,
        'archive_path':archive.relative_to(ROOT).as_posix(),
        'change_count':len(rows),
        'category_counts':dict(counts),
        'changes':rows,
        'preserved_decisions':PRESERVED,
        'mobileFallback':fallback,
        'qa':{
            'book_count':66,'chapter_count':1189,'verse_search_records':31102,
            'zip_crc':'pass','xml_parse':'pass','internal_links':'pass',
            'changed_book_members':changed_members,
            'post_release_actionable_article_mismatches':0,
            'article_sound_exceptions_preserved':len(post_exceptions),
            'exact_before_after_inventory':'pass',
            'scope_guard':'Ecclesiastes plus Isaiah 1:16 only',
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    detail = [f"| {r['reference']} | {r['category']} | {escape_md(r['before'])} | {escape_md(r['after'])} |" for r in rows]
    preserve = '\n'.join(f"- **{x['reference']}** — {x['reason']}" for x in PRESERVED)
    NOTE.parent.mkdir(parents=True, exist_ok=True)
    NOTE.write_text(f"""# Ecclesiastes inclusive language + Isaiah 1:16 harm wording — 2026-09-14

## Method

This release applies the Way Version's source-first inclusive-language method rather than a global word replacement.

- Generic human/proverbial referents use inclusive English when sex is not meaningful to the saying.
- Actual male kings, the male Preacher, source-marked kinship, and the explicit man/woman contrast are preserved.
- Unmistakably divine masculine English pronouns are replaced by the established divine name/title, not divine `they`, `she`, or `it`.
- Hebrew `ra` / `ra'ah` is translated by context: wrongdoing, harm, misfortune, sorrow, bad, and related senses are not mechanically flattened to `brokenness`.
- Isaiah 1:16 (`ra' ma'alaleikhem` / `harea'`) is rendered with **harm**: `Put away the harm of your doings ... Cease doing harm.`

## Totals

- Exact changed verses: **{len(rows)}**
- Ecclesiastes: **{sum(1 for r in rows if r['book']=='ecclesiastes')}**
- Isaiah: **1** (`Isaiah 1:16` only)
- Categories: `{dict(counts)}`

## Preserved male/source-marked cases

{preserve}

## Exact approved ledger

| Reference | Category | Before | After |
|---|---|---|---|
{chr(10).join(detail)}

## Canonical QA

- Previous EPUB SHA-256: `{BASELINE}`
- Released EPUB SHA-256: `{newsha}`
- Previous EPUB archived at `{archive.relative_to(ROOT).as_posix()}`
- 66 books / 1,189 chapters / 31,102 search records
- ZIP CRC, EPUB mimetype, XML parsing, and internal links: pass
- Exact before/after inventory: pass
- English article audit: **0 actionable mismatches**, including explicit `an person` regression guard
- Canonical mobile fallback regenerated from the finished EPUB

Downstream website and native readers must consume this exact finished EPUB/feed; no downstream Scripture hand-editing.
""", encoding='utf-8')

    base.append_once(HISTORY_LOG, newsha, f"- **{stamp}** — Ecclesiastes inclusive-language/contextual `ra/ra'ah` update plus Isaiah 1:16 harm wording released: {len(rows)} verse-level edits. Prior EPUB archived at `{archive.relative_to(ROOT).as_posix()}`; new SHA-256 `{newsha}`.")
    base.append_once(REFRESH, '## 2026-09-14 Ecclesiastes inclusive language + Isaiah 1:16', f"""## 2026-09-14 Ecclesiastes inclusive language + Isaiah 1:16

A whole-book Ecclesiastes review corrected generic-human pronoun chains, unmistakable divine-pronoun remnants, and contextually inappropriate `brokenness` renderings. Source-marked male referents were preserved. Isaiah 1:16 was separately corrected to `Put away the harm of your doings ... Cease doing harm.` Canonical SHA-256: `{newsha}`. See `../editor-notes/consistency/2026-09-14-ecclesiastes-inclusive-language-isaiah-harm.md` and `../change-logs/reports/2026-09-14-ecclesiastes-inclusive-language-isaiah-harm.json`.""")
    base.replace_sha_in_file(ROOT_README, BASELINE, newsha)
    base.replace_sha_in_file(CURRENT_README, BASELINE, newsha)

    print(json.dumps({'release':'Ecclesiastes inclusive language + Isaiah 1:16 harm wording','releasedEpubSha256':newsha,'changeCount':len(rows),'categoryCounts':dict(counts),'articleMismatches':len(post_articles),'fallbackContentSha256':fallback['contentSha256'],'fallbackBytes':fallback['contentBytes'],'changedMembers':changed_members}, indent=2))

if __name__ == '__main__':
    main()
