#!/usr/bin/env python3
"""Release reviewed divine Father/God gender residuals across Acts–Revelation.

Finite approved ledger + complete 23-book, verse-by-verse masculine-pronoun
inventory. Fail closed for baseline drift, any unmatched replacement or any
Bible verse outside the ledger. A candidate is NOT automatically a God pronoun.
"""
from __future__ import annotations

import json,os,re,shutil,tempfile,zipfile
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
import release_2026_09_30_kingdom_residuals as rel

base=rel.base
ROOT,EPUB,REG=rel.ROOT,rel.EPUB,rel.REGISTRY
LEDGER=ROOT/'tools/local/2026-10-14-acts-revelation-divine-pronouns-approved-ledger.json'
NOTE=ROOT/'editor-notes/consistency/2026-10-14-acts-revelation-divine-pronouns-release.md'
REPORT=ROOT/'change-logs/reports/2026-10-14-acts-revelation-divine-pronouns-release.json'
AUDIT=ROOT/'change-logs/reports/2026-10-14-acts-revelation-masculine-pronoun-candidates.json'
SUMMARY=ROOT/'change-logs/reports/2026-10-14-acts-revelation-masculine-pronoun-candidates.md'
SOURCE=ROOT/'original-documents/rest_of_new_testament_restorative_translation.txt'
NT=['acts','romans','1-corinthians','2-corinthians','galatians','ephesians',
    'philippians','colossians','1-thessalonians','2-thessalonians','1-timothy',
    '2-timothy','titus','philemon','hebrews','james','1-peter','2-peter',
    '1-john','2-john','3-john','jude','revelation']
DIV=re.compile(r'\b(?:God|Elohim|YHWH|Cosmic Parent|Creator|Almighty|Master)\b',re.I)
MASC=re.compile(r'\b(?:he|him|his|himself)\b',re.I)

def bible():return rel.collect_verses(EPUB,slugs=rel.ALL_SLUGS)

def audit(verses):
    c={k:v for k,v in verses.items() if k[0] in NT}
    rows=[]
    nbooks=Counter()
    for book in NT:
        refs=sorted((k for k in c if k[0]==book),key=lambda k:(k[1],k[2]))
        nbooks[book]=len(refs)
        for i,key in enumerate(refs):
            s=c[key];words=[m.group() for m in MASC.finditer(s)]
            if not words:continue
            prior=(c[refs[i-1]] if i and refs[i-1][1]==key[1] else '')
            after=(c[refs[i+1]] if i+1<len(refs) and refs[i+1][1]==key[1] else '')
            rows.append({'reference':f'{rel.SLUG_TO_BOOK[book]} {key[1]}:{key[2]}',
               'book':book,'chapter':key[1],'verse':key[2],
               'text':s,'pronouns':words,'divineCueSameVerse':bool(DIV.search(s)),
               'divineCueNeighbor':bool(DIV.search(prior+' '+after)),
               'previousVerse':prior,'nextVerse':after,'status':'candidate, not automatic replacement'})
    return {'scope':'Acts through Revelation, all 23 canonical NT books after the four Gospels',
      'allVersesAudited':len(c),'bookVerseCounts':dict(nbooks),
      'masculinePronounCandidateVerses':len(rows),
      'withDivineCueSameVerse':sum(r['divineCueSameVerse'] for r in rows),
      'withDivineCueNeighbor':sum(r['divineCueNeighbor'] for r in rows),
      'limitation':'Candidate list contains Yeshua and human-male references; semantic referents require contextual editorial review.',
      'candidates':rows}

def main():
    ledger=json.loads(LEDGER.read_text(encoding='utf-8'))
    baseline=ledger['baselineCanonicalEpubSha256']
    rows=ledger['patches']
    if len(rows)!=66 or base.sha256(EPUB)!=baseline:
        raise RuntimeError('Ledger row count or canonical EPUB baseline changed; stop')
    before=bible()
    if len(before)!=31102:raise RuntimeError('Bible verse inventory changed unexpectedly')
    preissues,preexc=rel.grammar.audit_epub(EPUB)
    if preissues:raise RuntimeError('Pre-release EPUB grammar issues')
    audited=audit(before)
    if audited['allVersesAudited']<3500 or len(audited['bookVerseCounts'])!=23:
        raise RuntimeError('Not all Acts–Revelation verses audited')
    work=[];approved=set();grouped=defaultdict(list)
    for x in rows:
        ref=x['reference']
        name,chv=ref.rsplit(' ',1)
        ch,verse=map(int,chv.split(':'))
        slug=name.lower().replace(' ','-')
        key=(slug,ch,verse)
        if slug not in NT or key in approved or key not in before:
            raise RuntimeError('Duplicate, non-scope or nonexistent verse: '+ref)
        src=before[key];new=src
        for old,replacement in x['patches']:
            if old==replacement or new.count(old)!=1:
                raise RuntimeError(f'One-to-one match failed: {ref}; fragment: {old!r}; matches={new.count(old)}')
            new=new.replace(old,replacement,1)
        if new==src:raise RuntimeError('No verse-level change: '+ref)
        row={'reference':ref,'book':name,'chapter':ch,'verse':verse,
             'before':src,'after':new,'patches':x['patches']}
        work.append(row);approved.add(key);grouped[slug].append(row)
    now=datetime.now(timezone.utc)
    stamp=now.strftime('%Y-%m-%d_%H%M%SUTC')
    generated=now.replace(microsecond=0).isoformat().replace('+00:00','Z')
    archivedir=ROOT/'rendered-documents-history'/stamp
    archivedir.mkdir(parents=True,exist_ok=False)
    archive=archivedir/EPUB.name
    shutil.copy2(EPUB,archive)
    if base.sha256(archive)!=baseline:raise RuntimeError('Archive baseline checksum mismatch')
    with zipfile.ZipFile(EPUB) as zin:
        infos=zin.infolist()
        original={i.filename:zin.read(i.filename) for i in infos}
        members={slug:base.find_book_member(zin,slug) for slug in grouped}
    updated=dict(original)
    for slug,changes in grouped.items():
        member=members[slug]
        s=updated[member].decode('utf-8')
        for r in changes:
            s=rel.replace_one_verse(s,slug,r['chapter'],r['verse'],r['before'],r['after'])
        updated[member]=s.encode('utf-8')
    fd,name=tempfile.mkstemp(prefix='way-acts-rev-god-neut-',suffix='.epub',dir=EPUB.parent)
    os.close(fd);tmp=Path(name)
    try:
        with zipfile.ZipFile(tmp,'w') as zout:
            for i in infos:
                zout.writestr(i,updated[i.filename],compress_type=i.compress_type)
        base.validate_epub(tmp)
        shutil.move(tmp,EPUB)
    finally:tmp.unlink(missing_ok=True)
    changed_members={p for p in original if original[p]!=updated[p]}
    if changed_members!=set(members.values()):
        raise RuntimeError('EPUB member diff beyond exact changed NT books')
    after=bible()
    diffs={key for key in before if before[key]!=after[key]}
    if len(after)!=31102 or diffs!=approved:
        raise RuntimeError('Whole Bible diff != exactly approved 66 verses; differences: '+repr(list(diffs^approved)[:20]))
    for r in work:
        if after[(r['book'].lower().replace(' ','-'),r['chapter'],r['verse'])]!=r['after']:
            raise RuntimeError('Released verse text mismatch '+r['reference'])
    postissues,postexc=rel.grammar.audit_epub(EPUB)
    if postissues or len(postexc)!=len(preexc):
        raise RuntimeError('EPUB grammar regression after patch')
    digest=base.sha256(EPUB)
    names=json.loads(REG.read_text(encoding='utf-8'))
    if names.get('canonicalEpubSha256')!=baseline:
        raise RuntimeError('Canonical original-name registry SHA mismatch')
    names['canonicalEpubSha256']=digest
    REG.write_text(json.dumps(names,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fallback=base.build_fallback(EPUB,names,digest,generated)
    if (fallback.get('bookCount'),fallback.get('chapterCount'),fallback.get('verseSearchCount'))!=(66,1189,31102):
        raise RuntimeError('Updated GitHub mobile fallback inventory mismatch')
    source=SOURCE.read_text(encoding='utf-8')
    source_done=[];source_unmatched=[]
    for r in work:
        token=f'{r["verse"]}. {r["before"]}'
        if source.count(token)==1:
            source=source.replace(token,f'{r["verse"]}. {r["after"]}',1)
            source_done.append(r['reference'])
        else:source_unmatched.append(r['reference'])
    SOURCE.write_text(source,encoding='utf-8')
    audited['sourceCanonicalEpubSha256']=baseline
    audited['releasedCanonicalEpubSha256']=digest
    audited['approvedChangedVerses']=len(work)
    audited['reviewedLedgerReferences']=[r['reference'] for r in work]
    audited['protectedOrUnresolvedExamples']=ledger['protectedExamples']
    AUDIT.write_text(json.dumps(audited,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    summary=[
      '# Full Acts–Revelation gendered divine-reference candidate audit — 2026-10-14',
      '',
      f'Scanned **{audited["allVersesAudited"]}** verses across **23 NT books** in canonical EPUB.',
      f'Found **{audited["masculinePronounCandidateVerses"]}** verses containing masculine pronouns.',
      f'Same-verse divine-word candidates: **{audited["withDivineCueSameVerse"]}**; adjacent divine-word candidates: **{audited["withDivineCueNeighbor"]}**.',
      '',
      'These counts are lexical CANDIDATES, **not verified errors**. Yeshua/Jesus and genuine male persons remain masculine; Greek and local speaker/antecedent determine action.',
      f'Approved exact corrections: **{len(work)}** verses across **{len(grouped)}** of the 23 books.',
      'James 1:12 has important source variants: key early Greek witnesses lack an expressed subject; other witnesses supply “Lord” or “God”. Context and the Way editorial choice support “God”.',
      'James 1:18 clearly names the Cosmic Parent of lights in 1:17, so “his/he/his” refer to that divine actor.',
      '',
      '## Priority passages preserved for contextual review, not auto-replaced']
    for item in ledger['protectedExamples']:summary.append('- '+item)
    summary+=['','## Exact corrected references (full before/after appears in release JSON)']
    for row in work:summary.append('- '+row['reference'])
    summary+=['','## Coverage by canonical book']
    for b in NT:summary.append(f'- {rel.SLUG_TO_BOOK[b]}: {audited["bookVerseCounts"][b]} verses')
    summary+=['','## Historical source alignment',
      f'Legacy editable NT text exact-match updated: {len(source_done)} verses; mismatched older baselines need print/source reconciliation: {len(source_unmatched)}.',
      'The canonical EPUB is the authoritative released Scripture; a current physical Word master and typeset PDF are separate production artifacts.']
    SUMMARY.write_text('\n'.join(summary)+'\n',encoding='utf-8')
    report={
      'releaseDate':'2026-10-14','release':'Acts through Revelation reviewed God/Father masculine pronoun correction',
      'baselineEpubSha256':baseline,'releasedEpubSha256':digest,
      'archivePath':archive.relative_to(ROOT).as_posix(),
      'exactChangedVerseCount':len(work),'changedBookCount':len(grouped),
      'changedBooks':sorted(grouped),'changedEpubMembers':sorted(changed_members),
      'wholeBibleVerseCount':31102,'allActsThroughRevelationVersesAudited':audited['allVersesAudited'],
      'candidateMasculinePronounVerses':audited['masculinePronounCandidateVerses'],
      'sourceEditableNTAlignedReferences':source_done,'sourceEditableNTOlderUnmatchedReferences':source_unmatched,
      'qa':{'onlyApprovedVersesChanged':True,'epubZipXmlLinks':'pass','grammar':'pass',
            'bibleBooks':66,'chapters':1189,'verses':31102,'ntBooksReviewed':23},
      'approvedExactVerses':work,'textualNoteJames1_12':ledger['textualNote'],
      'protectedExamples':ledger['protectedExamples'],'canonicalMobileFallback':fallback,
      'printStatus':'Exact before/after ledger ready in Docs; owner-controlled Word print master and press-ready PDF require separate production/reconciliation and proof.'
    }
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    NOTE.write_text(
      '# Acts–Revelation divine-gender residual release — 2026-10-14\n\n'
      +'\n'.join(summary[:12])+'\n\n'
      +'Canonical previous SHA: '+baseline+'\nCanonical released SHA: '+digest+'\n'
      +'Archived previous: '+archive.relative_to(ROOT).as_posix()+'\n'
      +'Full before/after editorial ledger: '+str(REPORT.relative_to(ROOT))+'\n'
      +'Full remaining candidate audit: '+str(AUDIT.relative_to(ROOT))+'\n'
      +'For physical print production, update owner working Word master by exact verse and regenerate/proof typeset PDF; never patch only an old press PDF.\n',
      encoding='utf-8')
    base.append_once(rel.HISTORY_LOG,digest,
      f'- {stamp} — complete Acts–Revelation lexical audit, {len(work)} exact divine-referent verse corrections in {len(grouped)} books; archived {archive.relative_to(ROOT).as_posix()}; new SHA {digest}.')
    base.append_once(rel.REFRESH,'## 2026-10-14 Acts–Revelation divine-pronoun audit',
      '## 2026-10-14 Acts–Revelation divine-pronoun audit\n\n'
      f'23 books / {audited["allVersesAudited"]} verses scanned, {len(work)} reviewed '
      f'exact God/Cosmic Parent/Master reference corrections in {len(grouped)} books. '
      f'Canonical EPUB SHA-256 {digest}. Only ledger verses changed; all Yeshua and human male uses preserved where distinguished. '
      'Requires separate Word/PDF physical print proof.'
    )
    base.replace_sha_in_file(rel.ROOT_README,baseline,digest)
    base.replace_sha_in_file(rel.CURRENT_README,baseline,digest)
    print(json.dumps({
      'releasedEpubSha256':digest,'changedVerses':len(diffs),
      'changedBooks':len(grouped),'ActsThroughRevelationVersesAudited':audited['allVersesAudited'],
      'pronounCandidateVerses':audited['masculinePronounCandidateVerses'],
      'legacySourceUpdated':len(source_done),'legacySourceUnmatched':len(source_unmatched),
      'canonicalMobileFallback':fallback},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
