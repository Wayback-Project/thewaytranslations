#!/usr/bin/env python3
"""Second-pass driver for the 2026-09-12 original-name release.

The proposal inventory was created against an earlier reader audit. The current
canonical EPUB already contains Yeshua/Bavel/Natzeret at the stale proposal
locations, and the Luke-person references are currently spelled Loukas. This
driver keeps the strict release checks while recording those already-complete
identities and normalizing Loukas/Luke person references to the approved Lukas.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import tempfile
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

HELPER_PATH = Path(__file__).with_name('release_2026_09_12_original_names.py')
spec = importlib.util.spec_from_file_location('name_release_helpers', HELPER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError('unable to load release helper module')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

CURRENT_FORM_OVERRIDES = {
    'luke-person': ['Luke', 'Loukas'],
}


def main() -> None:
    actual = m.sha256(m.EPUB)
    if actual != m.BASELINE:
        if m.REGISTRY.exists():
            existing = json.loads(m.REGISTRY.read_text(encoding='utf-8'))
            if existing.get('canonicalEpubSha256') == actual and existing.get('releaseDate') == '2026-09-12':
                print(json.dumps({'status': 'already-applied', 'sha256': actual}, indent=2))
                return
        raise SystemExit(f'baseline SHA mismatch: expected {m.BASELINE}, got {actual}')

    released, guides = m.load_entries()
    for item in released:
        if item['id'] in CURRENT_FORM_OVERRIDES:
            item['currentForms'] = list(CURRENT_FORM_OVERRIDES[item['id']])

    stamp = datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%MUTC')
    archive_dir = m.ROOT / 'rendered-documents-history' / stamp
    archive_dir.mkdir(parents=True, exist_ok=False)
    archive = archive_dir / m.EPUB.name
    shutil.copy2(m.EPUB, archive)
    if m.sha256(archive) != m.BASELINE:
        raise RuntimeError('archive SHA mismatch')

    with zipfile.ZipFile(m.EPUB, 'r') as zin:
        infos = zin.infolist()
        original = {i.filename: zin.read(i.filename) for i in infos}

    edited = dict(original)
    all_changes = []
    totals = Counter()
    changed_members = set()
    for name, raw in list(edited.items()):
        if not name.lower().endswith(('.xhtml', '.html', '.htm')):
            continue
        new_raw, changes, counts = m.edit_member(name, raw, released)
        if new_raw != raw:
            edited[name] = new_raw
            changed_members.add(name)
            all_changes.extend(changes)
            totals.update(counts)

    by_id = defaultdict(int)
    for (entry_id, old, target), count in totals.items():
        by_id[entry_id] += count

    corpus = m.verse_corpus(edited)
    already_complete = []
    missing_entries = []
    for item in released:
        if by_id[item['id']] > 0:
            continue
        target = item['proposedForm']
        old_remaining = [old for old in item['currentForms'] if old != target and m.token_pattern(old).search(corpus)]
        if not old_remaining and m.token_pattern(target).search(corpus):
            already_complete.append(item['id'])
        else:
            missing_entries.append({
                'id': item['id'],
                'target': target,
                'oldStillPresent': old_remaining,
                'targetPresent': bool(m.token_pattern(target).search(corpus)),
            })
    if missing_entries:
        raise RuntimeError(f'approved release entries unresolved after canonical comparison: {missing_entries}')

    stale = []
    for item in released:
        target = item['proposedForm']
        for old in item['currentForms']:
            if old == target:
                continue
            if m.token_pattern(old).search(corpus):
                stale.append({'id': item['id'], 'form': old})
    if stale:
        raise RuntimeError(f'stale approved traditional forms remain in verse text: {stale[:30]}')

    joined_all = '\n'.join(raw.decode('utf-8', 'ignore') for raw in edited.values() if isinstance(raw, bytes))
    for heading in ['Luke 1', 'Nehemiah 1', 'Jonah 1', 'Hosea 1', 'Ruth 1', 'Zechariah 1']:
        if heading not in joined_all:
            raise RuntimeError(f'book-title/chapter heading preservation check failed: {heading}')

    if by_id['luke-person'] < 3:
        raise RuntimeError(f'expected at least three Luke/Loukas-person → Lukas replacements, got {by_id["luke-person"]}')
    if 'Lukas, the beloved physician' not in corpus:
        raise RuntimeError('Colossians 4:14 Lukas verification failed')
    if 'Only Lukas is with me' not in corpus:
        raise RuntimeError('2 Timothy 4:11 Lukas verification failed')

    fd, tmpname = tempfile.mkstemp(suffix='.epub', dir=str(m.EPUB.parent))
    os.close(fd)
    tmp = Path(tmpname)
    try:
        with zipfile.ZipFile(tmp, 'w') as zout:
            for info in infos:
                zout.writestr(info, edited[info.filename], compress_type=info.compress_type)
        m.validate_epub(tmp)
        shutil.move(tmp, m.EPUB)
    finally:
        if tmp.exists():
            tmp.unlink()

    newsha = m.sha256(m.EPUB)
    if newsha == m.BASELINE:
        raise RuntimeError('release SHA did not change')

    records = [m.registry_record(item) for item in released]
    for item in guides:
        aliases = m.GUIDE_ALIASES.get(item['id'])
        if not aliases:
            raise RuntimeError(f'missing familiar alias for reader-guide-only entry {item["id"]}')
        records.append(m.registry_record(item, aliases=aliases, status='guide-only'))
    records.extend(m.EXTRA_GUIDES)
    records.sort(key=lambda r: r['id'])

    registry = {
        'schemaVersion': '1.0.0',
        'releaseDate': '2026-09-12',
        'canonicalEpubSha256': newsha,
        'priorCanonicalEpubSha256': m.BASELINE,
        'policy': {
            'bookTitlesChanged': False,
            'generatedReadersMayRewriteScripture': False,
            'aliasesAreReaderMetadata': True,
            'releasedEntries': len(released),
            'guideOnlyEntries': len(guides) + len(m.EXTRA_GUIDES),
            'alreadyCompleteAtRelease': already_complete,
        },
        'entries': records,
    }
    m.REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    mapping_summary = []
    for item in released:
        mapping_summary.append({
            'id': item['id'],
            'from': item['currentForms'],
            'to': item['proposedForm'],
            'replacementCount': by_id[item['id']],
            'alreadyCompleteBeforeThisBatch': item['id'] in already_complete,
            'proposalFile': item['_proposalFile'],
        })

    report = {
        'release': '2026-09-12 original-name restoration batch',
        'prior_epub_sha256': m.BASELINE,
        'released_epub_sha256': newsha,
        'archive_path': archive.relative_to(m.ROOT).as_posix(),
        'changedVerseCount': len(all_changes),
        'replacementCount': sum(totals.values()),
        'mappingCount': len(released),
        'alreadyCompleteAtRelease': already_complete,
        'changedBookMembers': sorted(changed_members),
        'mappings': mapping_summary,
        'changes': sorted(all_changes, key=lambda c: c['reference']),
        'preservedBookTitles': ['Luke', 'Nehemiah', 'Jonah', 'Hosea', 'Ruth', 'Zechariah'],
        'qa': {
            'bookCount': 66,
            'chapterCount': 1189,
            'zipCrc': 'pass',
            'xmlParse': 'pass',
            'internalLinks': 'pass',
            'staleReleasedFormsInVerseText': 0,
            'bookTitlePreservation': 'pass',
            'lukePersonReplacementCount': by_id['luke-person'],
        },
    }
    m.LEDGER.parent.mkdir(parents=True, exist_ok=True)
    m.LEDGER.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    m.NOTE.parent.mkdir(parents=True, exist_ok=True)
    m.NOTE.write_text(f'''# Original-name restoration release — 2026-09-12

This release promotes the reviewed high-priority original-name proposal directory into a canonical Scripture release under explicit editor authorization. It applies only the listed person/place/full-compound mappings to verse text. Biblical book titles remain unchanged unless separately approved.

## Release summary

- Prior canonical EPUB SHA-256: `{m.BASELINE}`
- Released canonical EPUB SHA-256: `{newsha}`
- Prior EPUB archived at `{archive.relative_to(m.ROOT).as_posix()}`
- Approved mapping identities: **{len(released)}**
- Individual replacements made in this batch: **{sum(totals.values())}**
- Changed verses: **{len(all_changes)}**
- Affected book XHTML members: **{len(changed_members)}**
- Identities already complete before this batch: **{', '.join(already_complete) if already_complete else 'none'}**
- Coverage preserved: **66 books / 1,189 chapters**

## Scope highlights

- `Michael` → `Mikha'el`
- `Ishmael` → `Yishmael`
- `Adonijah` → `Adoniyahu`; `Abishai` → `Avishai`; `Abiathar` → `Evyatar`
- `Phinehas` → `Pinchas`; `Jethro` → `Yitro`; `Laban` → `Lavan`
- `Aquila` → `Akylas`; `Priscilla` → `Priskilla`; `Silvanus` → `Silvanos`
- person `Luke` / current `Loukas` → `Lukas`, while the book title **Luke remains Luke**
- person `Nehemiah` → `Nechemyah`, while the book title **Nehemiah remains Nehemiah**
- `Sodom` → `Sedom`; `Gomorrah` → `Amora`; `Canaan` → `Kena'an`; `Caesarea` → `Kaisareia`; `Colossae` → `Kolosai`; `Ashkelon` → `Ashqelon`
- reviewed full `Beth ...` place compounds → approved `Beit ...` forms; no global bare `Beth` replacement
- consistency backlog forms including Oved, Yoram, Uzziyah, Yotam, Zerubavel, Zerach, Yonah, Peretz, Chetzron, Rut, Malki-Tzedek, She'altiel, Aram, Yekhonyahu, Hoshea, Avram, Yeshua, Bavel, Natzeret, and YHWH

The exact reference-level before/after ledger is `change-logs/reports/2026-09-12-original-name-restoration-release.json`.
The released identity/alias/pronunciation metadata is `current-form-documents/original-name-registry.json` and is intended to drive downstream reader glossary/search metadata without independently rewriting Scripture.

## Reader-guide-only aliases

The registry also records familiar aliases for already-restored Scripture forms: Rakhel/Rachel, Hananyah/Ananias, Yochana/Joanna, Shoshana/Susanna, Yair/Jair/Jairus, Shalem/Salem, and Mattityah/Matthias. These records do not alter Scripture text.
''', encoding='utf-8')

    cr = m.CURRENT_README.read_text(encoding='utf-8').replace(m.BASELINE, newsha)
    cr = re.sub(r'\| Previous release \| Archived under `rendered-documents-history/[^`]+/` \|', f'| Previous release | Archived under `{archive_dir.relative_to(m.ROOT).as_posix()}/` |', cr)
    marker = 'This EPUB includes the completed whole-Bible divine-pronoun consistency update, the 2026-09-11 original-name / Genesis narrative consistency update (39 reviewed verse-level edits), and the 2026-09-12 1 Corinthians divine-pronoun residual cleanup (4 reviewed verse-level edits);'
    replacement = marker[:-1] + ', plus the 2026-09-12 high-priority original-name restoration release;'
    if marker in cr:
        cr = cr.replace(marker, replacement)
    m.CURRENT_README.write_text(cr, encoding='utf-8')
    m.ROOT_README.write_text(m.ROOT_README.read_text(encoding='utf-8').replace(m.BASELINE, newsha), encoding='utf-8')

    history = m.HISTORY_LOG.read_text(encoding='utf-8').rstrip()
    history += f'\n| {stamp} | {archive_dir.relative_to(m.ROOT).as_posix()}/ | the-way-current.epub (SHA-256 `{m.BASELINE}`) | Archive prior canonical EPUB before the 2026-09-12 high-priority original-name restoration release; {len(released)} approved mapping identities / {sum(totals.values())} replacements. |\n'
    m.HISTORY_LOG.write_text(history, encoding='utf-8')

    print(json.dumps({
        'status': 'released',
        'new_sha256': newsha,
        'archive': archive.relative_to(m.ROOT).as_posix(),
        'mapping_count': len(released),
        'replacement_count': sum(totals.values()),
        'changed_verses': len(all_changes),
        'changed_books': len(changed_members),
        'already_complete': already_complete,
        'luke_person_replacements': by_id['luke-person'],
        'top_mappings': sorted(mapping_summary, key=lambda x: x['replacementCount'], reverse=True)[:20],
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
