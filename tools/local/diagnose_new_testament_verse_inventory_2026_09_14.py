#!/usr/bin/env python3
from collections import Counter
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT = HERE / 'audit_new_testament_gender_brokenness_2026_09_14.py'
spec = importlib.util.spec_from_file_location('ntaudit', AUDIT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.EXPECTED_NT_VERSES = 7956
verses = mod.extract_all()
actual = Counter(b for b,_,_,_ in verses)
expected = {
'Matthew':1071,'Mark':678,'Luke':1151,'John':879,'Acts':1007,'Romans':433,'1 Corinthians':437,'2 Corinthians':257,
'Galatians':149,'Ephesians':155,'Philippians':104,'Colossians':95,'1 Thessalonians':89,'2 Thessalonians':47,
'1 Timothy':113,'2 Timothy':83,'Titus':46,'Philemon':25,'Hebrews':303,'James':108,'1 Peter':105,'2 Peter':61,
'1 John':105,'2 John':13,'3 John':14,'Jude':25,'Revelation':404}
print('TOTAL', len(verses), 'expected-standard', sum(expected.values()))
for book in mod.BOOKS.values():
    a=actual[book]; e=expected[book]
    print(f'{book}\tactual={a}\texpected={e}\tdelta={a-e}')
