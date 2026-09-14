#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import shutil
import tempfile
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import release_2026_09_14_ecclesiastes_inclusive_language_isaiah_harm as prior

base = prior.base
grammar = prior.grammar
replace_one_verse = prior.prev.replace_one_verse
collect_verses = prior.prev.collect_verses

ROOT = prior.ROOT
EPUB = prior.EPUB
REGISTRY = prior.REGISTRY
ROOT_README = prior.ROOT_README
CURRENT_README = prior.CURRENT_README
HISTORY_LOG = prior.HISTORY_LOG
REFRESH = prior.REFRESH

BASELINE = '0e66242a07b5303337f90078ae8639a1fca264031b63962fb109f79033e48c30'
LEDGER = ROOT / 'tools' / 'local' / 'approved_lexicon_cleanup_2026_09_14.tsv'
REPORT = ROOT / 'change-logs' / 'reports' / '2026-09-14-lexicon-update-ai-cleanup.json'
NOTE = ROOT / 'editor-notes' / 'consistency' / '2026-09-14-lexicon-update-ai-cleanup.md'
RELEASE_NAME = 'Lexicon update — translation cleanup of prior AI wording issues'

BOOK_TO_SLUG = {
'Genesis':'genesis','Exodus':'exodus','Leviticus':'leviticus','Numbers':'numbers','Deuteronomy':'deuteronomy',
'Joshua':'joshua','Judges':'judges','Ruth':'ruth','1 Samuel':'1-samuel','2 Samuel':'2-samuel','1 Kings':'1-kings','2 Kings':'2-kings',
'1 Chronicles':'1-chronicles','2 Chronicles':'2-chronicles','Ezra':'ezra','Nehemiah':'nehemiah','Esther':'esther','Job':'job',
'Psalms':'psalms','Proverbs':'proverbs','Ecclesiastes':'ecclesiastes','Song of Solomon':'song-of-solomon','Isaiah':'isaiah',
'Jeremiah':'jeremiah','Lamentations':'lamentations','Ezekiel':'ezekiel','Daniel':'daniel','Hosea':'hosea','Joel':'joel','Amos':'amos',
'Obadiah':'obadiah','Jonah':'jonah','Micah':'micah','Nahum':'nahum','Habakkuk':'habakkuk','Zephaniah':'zephaniah','Haggai':'haggai',
'Zechariah':'zechariah','Malachi':'malachi'}
SLUG_TO_BOOK = {v:k for k,v in BOOK_TO_SLUG.items()}
OT_SLUGS = tuple(BOOK_TO_SLUG.values())

BAD_CHANGED = [
    re.compile(r'\bbrokenness\b', re.I),
    re.compile(r'\b(?:a evil|an wicked|an person)\b', re.I),
    re.compile(r'\b(?:evil animals?|evil arrows?|evil device|evil congregation|evil news|evil diseases|went evil with)\b', re.I),
    re.compile(r'\bthey\s+(?:is|was|has|does|lies|defiles|swears|walks|goes|comes|knows|gives|takes|makes|says|seeks|hates)\b', re.I),
]


def load_changes():
    rows=[]
    with LEDGER.open(encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            slug=BOOK_TO_SLUG[r['book']]
            rows.append((slug, int(r['chapter']), int(r['verse']), r['categories'], r['before'], r['after']))
    refs=[x[:3] for x in rows]
    if len(rows) != 369 or len(refs) != len(set(refs)):
        raise RuntimeError(f'approved ledger shape mismatch rows={len(rows)} unique={len(set(refs))}')
    lexical=sum('lexical' in x[3].split(',') for x in rows)
    generic=sum('generic-pronoun' in x[3].split(',') for x in rows)
    if lexical != 347 or generic != 23:
        raise RuntimeError(f'approved category mismatch lexical={lexical} generic={generic}')
    bad=[]
    for slug,ch,vs,cats,before,after in rows:
        for pat in BAD_CHANGED:
            if pat.search(after): bad.append({'reference':f'{SLUG_TO_BOOK[slug]} {ch}:{vs}','pattern':pat.pattern,'after':after})
    if bad:
        raise RuntimeError('approved ledger malformed: '+json.dumps(bad[:30],ensure_ascii=False,indent=2))
    return rows

CHANGES = load_changes()
CHANGED_SLUGS = tuple(sorted({x[0] for x in CHANGES}))


def collect(path: Path, *, all_ot=False):
    return collect_verses(path, slugs=OT_SLUGS if all_ot else CHANGED_SLUGS)


def validate_exact(path: Path, which: str):
    verse_map=collect(path)
    errors=[]
    for slug,ch,vs,cats,before,after in CHANGES:
        expected=before if which=='before' else after
        actual=verse_map.get((slug,ch,vs))
        if actual != expected:
            errors.append({'reference':f'{SLUG_TO_BOOK[slug]} {ch}:{vs}','expected':expected,'actual':actual})
    if errors:
        raise RuntimeError(f'{which} exact inventory mismatch ({len(errors)}): '+json.dumps(errors[:30],ensure_ascii=False,indent=2))


def rewrite_epub():
    by_slug=defaultdict(list)
    for row in CHANGES: by_slug[row[0]].append(row)
    with zipfile.ZipFile(EPUB,'r') as zin:
        infos=zin.infolist()
        original={i.filename:zin.read(i.filename) for i in infos}
    edited=dict(original)
    expected_members=[]
    with zipfile.ZipFile(EPUB,'r') as z:
        for slug, rows in by_slug.items():
            member=base.find_book_member(z,slug)
            expected_members.append(member)
            text=edited[member].decode('utf-8')
            for _slug,ch,vs,_cats,before,after in rows:
                text=replace_one_verse(text,slug,ch,vs,before,after)
            edited[member]=text.encode('utf-8')
    fd,tmpname=tempfile.mkstemp(prefix='the-way-lexicon-',suffix='.epub',dir=EPUB.parent)
    import os; os.close(fd)
    tmp=Path(tmpname)
    try:
        with zipfile.ZipFile(tmp,'w') as zout:
            for info in infos:
                zout.writestr(info,edited[info.filename],compress_type=info.compress_type)
        base.validate_epub(tmp)
        shutil.move(tmp,EPUB)
    finally:
        if tmp.exists(): tmp.unlink()
    changed=sorted(name for name in original if original[name] != edited[name])
    if changed != sorted(expected_members):
        raise RuntimeError(f'changed EPUB members mismatch expected={sorted(expected_members)} actual={changed}')
    return changed


def category_counts():
    c=Counter()
    for row in CHANGES:
        for cat in row[3].split(','):
            if cat: c[cat]+=1
    return c


def main():
    actual=base.sha256(EPUB)
    if actual != BASELINE:
        raise SystemExit(f'baseline SHA mismatch expected={BASELINE} got={actual}')

    pre_articles, pre_exceptions=grammar.audit_epub(EPUB)
    if pre_articles:
        raise RuntimeError('pre-release article audit not clean: '+json.dumps(pre_articles[:30],ensure_ascii=False,indent=2))
    validate_exact(EPUB,'before')

    before_ot=collect(EPUB,all_ot=True)
    if len(before_ot) != 23145:
        raise RuntimeError(f'OT verse inventory before release is {len(before_ot)}, expected 23145')

    now=datetime.now(timezone.utc)
    stamp=now.strftime('%Y-%m-%d_%H%MUTC')
    generated=now.replace(microsecond=0).isoformat().replace('+00:00','Z')
    archive_dir=ROOT/'rendered-documents-history'/stamp
    archive_dir.mkdir(parents=True,exist_ok=False)
    archive=archive_dir/EPUB.name
    shutil.copy2(EPUB,archive)
    if base.sha256(archive) != BASELINE:
        raise RuntimeError('archive SHA mismatch')

    changed_members=rewrite_epub()
    newsha=base.sha256(EPUB)
    if newsha == BASELINE:
        raise RuntimeError('EPUB SHA did not change')
    validate_exact(EPUB,'after')

    post_articles, post_exceptions=grammar.audit_epub(EPUB)
    if post_articles:
        raise RuntimeError('article inconsistencies introduced: '+json.dumps(post_articles[:30],ensure_ascii=False,indent=2))
    if len(post_exceptions) != len(pre_exceptions):
        raise RuntimeError(f'pronunciation article exception inventory changed before={len(pre_exceptions)} after={len(post_exceptions)}')

    after_ot=collect(EPUB,all_ot=True)
    if len(after_ot) != 23145:
        raise RuntimeError(f'OT verse inventory after release is {len(after_ot)}, expected 23145')
    brokenness=[(f'{SLUG_TO_BOOK[s]} {c}:{v}',t) for (s,c,v),t in after_ot.items() if re.search(r'\bbrokenness\b',t,re.I)]
    if brokenness:
        raise RuntimeError('Old Testament brokenness residuals remain: '+json.dumps(brokenness[:30],ensure_ascii=False,indent=2))

    malformed=[]
    for (slug,ch,vs),text in after_ot.items():
        if re.search(r'\ban\s+person\b|\ba\s+evil\b|\ban\s+wicked\b|\bthey\s+(?:is|was|has|does)\b',text,re.I):
            malformed.append((f'{SLUG_TO_BOOK[slug]} {ch}:{vs}',text))
    if malformed:
        raise RuntimeError('OT malformed-language regression: '+json.dumps(malformed[:30],ensure_ascii=False,indent=2))

    registry=json.loads(REGISTRY.read_text(encoding='utf-8'))
    if registry.get('canonicalEpubSha256') != BASELINE:
        raise RuntimeError('registry baseline SHA mismatch')
    registry['canonicalEpubSha256']=newsha
    REGISTRY.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fallback=base.build_fallback(EPUB,registry,newsha,generated)
    for key,expected in [('bookCount',66),('chapterCount',1189),('verseSearchCount',31102)]:
        if key in fallback and fallback[key] != expected:
            raise RuntimeError(f'fallback {key} mismatch {fallback[key]} != {expected}')

    counts=category_counts()
    rows=[]
    for slug,ch,vs,cats,before,after in CHANGES:
        rows.append({'reference':f'{SLUG_TO_BOOK[slug]} {ch}:{vs}','book':SLUG_TO_BOOK[slug],'chapter':ch,'verse':vs,'categories':cats.split(','),'before':before,'after':after})

    report={
      'release':RELEASE_NAME,
      'prior_epub_sha256':BASELINE,
      'released_epub_sha256':newsha,
      'archive_path':archive.relative_to(ROOT).as_posix(),
      'change_count':len(rows),
      'lexical_verse_changes':347,
      'generic_pronoun_verse_changes':23,
      'automatic_divine_pronoun_changes':0,
      'automatic_broad_masculine_term_changes':0,
      'category_counts':dict(counts),
      'changed_members':changed_members,
      'old_testament_verse_count':len(after_ot),
      'old_testament_brokenness_residual_count':0,
      'article_mismatch_count':len(post_articles),
      'mobileFallback':fallback,
      'changes':rows,
      'method':'Exact finite ledger. Contextual/source-informed lexical repair of all 347 audited brokenness artifacts, with the attested pre-AI lexical value used as a conservative fallback where ambiguity remained; 23 separately hand-reviewed formulaically generic pronoun chains. No heuristic divine-pronoun or broad man/men changes.',
      'preserved':['Actual male characters and sex-specific roles','Male kinship and royal figures where source-specific','Ambiguous/divine-coreference candidates not explicitly approved','Psalm 110:5–7 unresolved']
    }
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    NOTE.parent.mkdir(parents=True,exist_ok=True)
    NOTE.write_text(f'''# {RELEASE_NAME}\n\nThis release repairs prior AI-generated lexical flattening in the Old Testament and a small, separately reviewed set of generic-person pronoun chains. It is a finite exact-verse release, not a global replacement.\n\n## Scope\n\n- 369 unique verse-level edits.\n- 347 lexical repairs from the audited `brokenness` inventory.\n- 23 hand-reviewed formulaically generic pronoun consistency repairs; one verse overlaps the lexical set.\n- 0 automatic divine-pronoun changes.\n- 0 automatic broad `man` / `men` / occupational changes.\n- All 23,145 Old Testament verses re-extracted after the release; literal `brokenness` residuals in the Old Testament: 0.\n\nThe April pre-AI rendered text was used only as lexical provenance/safety evidence. It did not overwrite later approved original-name, inclusive-language, divine-name, or other canonical work. Context-specific English such as `harm`, `wrong`, `wrongdoing`, `calamity`, `disaster`, `adversity`, `deceit`, `bad news`, `wicked person`, and `dangerous animal` was used where the context was clear; where it was not, the attested earlier lexical value was preferred over inventing a new sense.\n\n## Preservation rules\n\nActual men remain men. Male kinship, kings/royal figures, sex-specific ritual or narrative roles, and source-significant gender were not mechanically neutralized. Heuristic divine-coreference candidates were excluded from this release. Psalm 110:5–7 remains unresolved.\n\n## Canonical QA\n\n- Previous EPUB SHA-256: `{BASELINE}`\n- Released EPUB SHA-256: `{newsha}`\n- Previous EPUB archived at `{archive.relative_to(ROOT).as_posix()}`\n- 66 books / 1,189 chapters / 31,102 search records\n- 23,145 / 23,145 Old Testament verses\n- ZIP CRC, EPUB mimetype/XML/internal links: pass\n- Exact 369-row before/after inventory: pass\n- English article audit: 0 actionable mismatches, including `an person` guard\n- Canonical mobile fallback regenerated from the finished EPUB\n\nDownstream website/e-reader and native mobile must consume this exact canonical release; no downstream Scripture hand-editing.\n''',encoding='utf-8')

    base.append_once(HISTORY_LOG,newsha,f'- **{stamp}** — {RELEASE_NAME}: 369 exact verse-level edits (347 lexical, 23 generic-pronoun; one overlap). Prior EPUB archived at `{archive.relative_to(ROOT).as_posix()}`; new SHA-256 `{newsha}`.')
    base.append_once(REFRESH,'## 2026-09-14 Lexicon update — prior AI wording cleanup',f'''## 2026-09-14 Lexicon update — prior AI wording cleanup\n\nFinite 369-verse release repairing prior AI lexical flattening and 23 hand-reviewed generic-person pronoun chains. No heuristic divine-pronoun or broad masculine-term rewrites were included. Canonical SHA-256: `{newsha}`. See `../editor-notes/consistency/2026-09-14-lexicon-update-ai-cleanup.md` and `../change-logs/reports/2026-09-14-lexicon-update-ai-cleanup.json`.''')
    base.replace_sha_in_file(ROOT_README,BASELINE,newsha)
    base.replace_sha_in_file(CURRENT_README,BASELINE,newsha)

    print(json.dumps({'release':RELEASE_NAME,'releasedEpubSha256':newsha,'changeCount':len(rows),'categoryCounts':dict(counts),'articleMismatches':len(post_articles),'otVerseCount':len(after_ot),'otBrokennessResiduals':0,'fallbackContentSha256':fallback.get('contentSha256'),'fallbackBytes':fallback.get('contentBytes'),'changedMembers':changed_members},indent=2))

if __name__=='__main__':
    main()
