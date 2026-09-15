#!/usr/bin/env python3
from __future__ import annotations
from collections import defaultdict
import zipfile
import release_2026_09_14_lexicon_update_ai_cleanup as prior

base=prior.base
EPUB=prior.EPUB

with zipfile.ZipFile(EPUB) as z:
    total=0
    duplicates=[]
    for testament,group in base.BOOKS:
        for slug,name in group:
            member=base.find_book_member(z,slug)
            book=base.extract_book(z.read(member),slug,name)
            for chapter in book['chapters']:
                by=defaultdict(list)
                for verse in chapter['verses']:
                    total += 1
                    by[verse['number']].append(verse)
                for number,rows in by.items():
                    if len(rows)>1:
                        duplicates.append({
                            'reference':f"{name} {chapter['number']}:{number}",
                            'count':len(rows),
                            'rows':[{'anchor':r['anchor'],'text':r['text']} for r in rows],
                        })
    print({'rawSearchRows':total,'duplicateReferences':duplicates})
