#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import propose_lexicon_inclusive_cleanup_2026_09_14 as base

ROOT=base.ROOT
AUD=base.AUD
CANDS=base.CANDS
OUT=AUD/'proposed-cleanup-v3.tsv'
SUMMARY=AUD/'proposed-cleanup-v3-summary.json'

# This release intentionally does NOT automate divine-pronoun changes or broad
# man/men occupational cleanup. Those categories require verse-by-verse source
# and coreference review. The entries below are formulaically generic English
# contexts whose own wording already establishes an inclusive antecedent.
GENERIC_AFTER={
'Exodus 21:14': "If someone schemes and comes presumptuously on their neighbor to kill them, you shall take them from my altar, that they may die.",
'Exodus 21:16': '"Anyone who kidnaps someone and sells them, or if they are found in their hand, they shall surely be put to death.',
'Exodus 21:26': '"If someone strikes their servant\'s eye, or their maid\'s eye, and destroys it, they shall let that servant go free because of the eye.',
'Exodus 22:1': '"If someone steals an ox or a sheep, and kills it, or sells it; they shall pay five oxen for an ox, and four sheep for a sheep.',
'Exodus 22:7': '"If someone delivers to their neighbor money or stuff to keep, and it is stolen out of the person\'s house; if the thief is found, they shall pay double.',
'Leviticus 11:40': 'The one who eats of its carcass shall wash their clothes, and be unclean until the evening. The one who carries its carcass shall wash their clothes, and be unclean until the evening.',
'Leviticus 13:40': '"If someone\'s hair has fallen from their head, they are bald. They are clean.',
'Leviticus 14:8': '"The one who is to be cleansed shall wash their clothes, and shave off all their hair, and bathe themselves in water; and they shall be clean. After that they shall come into the camp, but shall dwell outside their tent seven days.',
'Leviticus 17:10': '"Anyone of the house of Israel, or of the strangers who live as foreigners among them, who eats any kind of blood, I will set my face against that soul who eats blood, and will cut them off from among their people.',
'Leviticus 24:19': 'If anyone injures their neighbor; as they have done, so shall it be done to them:',
'Leviticus 25:29': '"If someone sells a dwelling house in a walled city, then they may redeem it within a whole year after it has been sold. For a full year they shall have the right of redemption.',
'Numbers 6:9': '"If anyone dies very suddenly beside them and defiles the head of their separation, then they shall shave their head on the day of their cleansing. On the seventh day they shall shave it.',
'Deuteronomy 21:22': 'If someone has committed a sin worthy of death, and they are put to death, and you hang them on a tree;',
'Deuteronomy 24:7': 'If someone be found stealing any of their brothers of the children of Israel, and they deal with them as a slave, or sell them; then that thief shall die: so shall you put away the evil from the midst of you.',
'Joshua 1:18': '"Whoever rebels against your commandment, and doesn\'t listen to your words in all that you command them, they shall be put to death. Only be strong and of good courage.',
'1 Kings 8:31': 'If someone sins against their neighbor, and an oath is laid on them to cause them to swear, and they come and swear before your altar in this house;',
'2 Chronicles 6:22': 'If someone sins against their neighbor, and an oath is laid on them to cause them to swear, and they come and swear before your altar in this house;',
'Job 4:2': '"If someone ventures to talk with you, will you be grieved? But who can withhold themselves from speaking?',
'Isaiah 40:20': 'The one who is too impoverished for such an offering chooses a tree that will not rot. They seek a skilled artisan to set up an engraved image for them that will not be moved.',
'Jeremiah 10:14': 'Everyone is become brutish [and is] without knowledge; every goldsmith is disappointed by their engraved image; for their molten image is falsehood, and there is no breath in them.',
'Jeremiah 21:9': 'The one who remains in this city shall die by the sword, and by the famine, and by the pestilence; but the one who goes out, and passes over to the Chaldeans who besiege you, they shall live, and their life shall be to them for a prey.',
'Jeremiah 51:17': 'Everyone is become brutish [and is] without knowledge; every goldsmith is disappointed by their image; for their molten image is falsehood, and there is no breath in them.',
'Micah 2:11': '"If someone walking in a spirit of falsehood lies: "I will prophesy to you of wine and of strong drink;" they would be the prophet of this people.',
}

# Context repairs applied after the conservative pre-AI lexical restoration.
# These are intentionally narrow English repairs; where no rule applies, the
# attested pre-AI value "evil" is retained rather than inventing a new gloss.
POST_REPLACEMENTS={
'1 Chronicles 7:23': [('because it went evil with his house','because trouble had come upon his house')],
'2 Chronicles 7:22': [('YHWH brought all this evil on them','YHWH brought all this calamity on them')],
'2 Chronicles 20:9': [('If evil come on us, the sword, judgment, or pestilence, or famine','If calamity comes on us—sword, judgment, pestilence, or famine')],
'Deuteronomy 28:20': [('because of the wrongdoing in your doings, by which you have forsaken me','because of the wrongdoing by which you have forsaken me')],
'Deuteronomy 28:54': [('their eye shall be evil toward their brother','they will look with hostility on their brother')],
'Deuteronomy 28:56': [('her eye shall be evil toward the husband of her bosom','she will look with hostility on the husband of her bosom')],
'Deuteronomy 29:21': [('set him apart to evil','set him apart for calamity')],
'Deuteronomy 31:29': [('evil will happen to you in the latter days','disaster will happen to you in the latter days')],
'Joshua 24:15': [('If it seem evil to you to serve YHWH','If it seems wrong to you to serve YHWH')],
'Joshua 24:20': [('YHWH will turn and do you evil','YHWH will turn and bring calamity on you')],
'Judges 2:15': [('the hand of YHWH was against them for evil','the hand of YHWH was against them, bringing calamity')],
'Judges 20:34': [("they didn't know that evil was close on them","they didn't know that disaster was closing in on them")],
'1 Samuel 16:23': [('[evil] spirit from Elohim','[troubling] spirit from Elohim')],
'1 Samuel 20:7': [('evil is determined by him','harm is intended by him')],
'1 Samuel 20:9': [('evil were determined by my father to come on you','harm were intended by my father to come on you')],
'1 Samuel 20:13': [('please my father to do you evil','please my father to harm you')],
'1 Samuel 25:3': [('the person was churlish and evil in their doings','the person was harsh and wrong in their conduct')],
'1 Samuel 25:17': [('evil is determined against our master','harm is planned against our master')],
'1 Samuel 25:28': [('evil shall not be found in you','wrongdoing shall not be found in you')],
'1 Samuel 25:39': [('the evil-doing of Nabal','the wrongdoing of Nabal')],
'1 Samuel 26:18': [('what evil is in my hand','what wrong is in my hand')],
'1 Samuel 29:6': [('I have not found evil in you','I have not found wrongdoing in you')],
'2 Samuel 15:14': [('bring down evil on us','bring disaster on us')],
'2 Samuel 19:7': [('all the evil that has happened to you','all the trouble that has happened to you')],
'1 Kings 9:9': [('YHWH brought all this evil on them','YHWH brought all this calamity on them')],
'1 Kings 21:29': [('bring the evil in his days','bring the calamity in his days'),('bring the evil on his house','bring the calamity on his house')],
'2 Kings 22:20': [('all the evil which I will bring on this place','all the calamity which I will bring on this place')],
'Nehemiah 13:18': [('bring all this evil on us','bring all this calamity on us')],
'Esther 7:7': [('evil determined against him','harm determined against him')],
'Esther 8:6': [('the evil that would come to my people','the harm that would come to my people')],
'Job 2:10': [('receive evil?','receive adversity?')],
'Job 2:11': [('all this evil that had come on him','all this adversity that had come on him')],
'Job 5:19': [('no evil touch you','no harm touch you')],
'Job 21:30': [('that the evil a person is reserved to the day of calamity','that the wicked person is reserved for the day of calamity')],
'Isaiah 47:11': [('Therefore shall evil come on you','Therefore shall calamity come on you')],
'Isaiah 57:1': [('taken away from the evil [to come]','taken away from the calamity [to come]')],
'Jeremiah 6:1': [('for evil looks forth from the north','for disaster looms from the north')],
'Jeremiah 8:3': [('this evil family','this wicked family')],
'Jeremiah 9:3': [('they proceed from harm to evil','they proceed from one wrong to another')],
'Jeremiah 12:14': [('all my evil neighbors','all my hostile neighbors')],
'Jeremiah 13:10': [('This evil people','This wicked people')],
'Jeremiah 19:15': [('all the evil that I have pronounced against it','all the calamity that I have pronounced against it')],
'Jeremiah 21:10': [('set my face on this city for evil, and not for good','set my face on this city for calamity, and not for good')],
'Jeremiah 21:12': [('because of the wrongdoing in your doings','because of your wrongdoing')],
'Jeremiah 23:2': [('visit on you the wrongdoing in your doings','call you to account for your wrongdoing')],
'Jeremiah 23:10': [('Their course is evil','Their course is wrong')],
'Jeremiah 23:17': [('No evil shall come on you','No harm shall come on you')],
'Jeremiah 24:9': [('give them up to be tossed back and forth among all the kingdoms of the earth for evil','give them up to be tossed back and forth among all the kingdoms of the earth for disaster')],
'Jeremiah 25:29': [('I begin to work evil at the city','I begin to bring calamity on the city')],
'Jeremiah 25:32': [('evil shall go forth from nation to nation','disaster shall go forth from nation to nation')],
'Jeremiah 26:3': [('relent from the evil which I purpose to do to them','relent from the calamity which I purpose to bring on them')],
'Jeremiah 26:13': [('relent from the evil that YHWH has pronounced against you','relent from the calamity that YHWH has pronounced against you')],
'Jeremiah 26:19': [('Thus should we commit great evil against our own souls','Thus should we bring great harm on ourselves')],
'Jeremiah 28:8': [('of war, and of evil, and of pestilence','of war, calamity, and pestilence')],
'Jeremiah 29:11': [('thoughts of peace, and not of evil','thoughts of peace, and not of harm')],
'Jeremiah 32:23': [('caused all this evil to come on them','caused all this calamity to come on them')],
'Jeremiah 32:32': [('because of all the evil of the children of Israel','because of all the wrongdoing of the children of Israel')],
'Jeremiah 32:42': [('brought all this great evil on this people','brought all this great calamity on this people')],
'Jeremiah 35:17': [('all the evil that I have pronounced against them','all the calamity that I have pronounced against them')],
'Jeremiah 36:3': [('all the evil which I purpose to do to them','all the calamity which I purpose to bring on them')],
'Jeremiah 36:31': [('all the evil that I have pronounced against them','all the calamity that I have pronounced against them')],
'Jeremiah 39:16': [('for evil, and not for good','for calamity, and not for good')],
'Jeremiah 40:2': [('pronounced this evil on this place','pronounced this calamity on this place')],
'Jeremiah 41:11': [('heard of all the evil that Yishmael','heard of all the harm that Yishmael')],
'Jeremiah 42:17': [('escape from the evil that I will bring on them','escape from the calamity that I will bring on them')],
'Jeremiah 44:23': [('therefore this evil is happened to you','therefore this calamity has happened to you')],
'Jeremiah 44:27': [('watch over them for evil, and not for good','watch over them for harm, and not for good')],
'Jeremiah 44:29': [('stand against you for evil','stand against you for harm')],
'Jeremiah 51:60': [('all the evil that should come on Bavel','all the calamity that should come on Bavel')],
'Lamentations 3:38': [("Doesn't evil and good come out of the mouth of the Most High?","Don't adversity and good come out of the mouth of the Most High?")],
'Ezekiel 5:16': [('the evil arrows of famine','the deadly arrows of famine')],
'Ezekiel 5:17': [('evil animals','dangerous animals')],
'Ezekiel 7:5': [('A evil, an only evil; behold, it comes','A disaster, a singular disaster; behold, it comes')],
'Ezekiel 14:15': [('evil animals','dangerous animals')],
'Ezekiel 14:21': [('evil animals','dangerous animals')],
'Ezekiel 14:22': [('concerning the evil that I have brought on Yerushalayim','concerning the calamity that I have brought on Yerushalayim')],
'Ezekiel 34:25': [('evil animals','dangerous animals')],
'Ezekiel 38:10': [('devise a evil device','devise an evil plan')],
'Daniel 3:29': [('speak anything harm against','speak anything amiss against')],
'Daniel 9:12': [('bringing on us a great evil','bringing on us a great calamity')],
'Daniel 9:13': [('all this evil is come on us','all this calamity has come on us')],
'Daniel 9:14': [('watched over the evil, and brought it on us','watched over the calamity, and brought it on us')],
'Amos 3:6': [('Does evil happen to a city, and YHWH hasn\'t done it?','Does calamity come to a city, and YHWH hasn\'t done it?')],
'Amos 9:4': [('set my eyes on them for evil, and not for good','set my eyes on them for harm, and not for good')],
'Amos 9:10': [("'evil won't overtake nor meet us.'","'Disaster won't overtake nor meet us.'")],
'Jonah 1:7': [('for whose cause this evil is on us','for whose cause this trouble is on us')],
'Jonah 1:8': [('for whose cause this evil is on us','for whose cause this trouble is on us')],
'Micah 3:2': [('love the evil','love wrongdoing')],
'Micah 3:4': [('because they made their deeds evil','because their deeds were evil')],
}

# Additional phrase-level cleanup for lexical forms that are unambiguously malformed.
POST_REGEX=[
(r'\bevil animals\b','dangerous animals'),
(r'\bevil animal\b','dangerous animal'),
(r'\bevil diseases\b','terrible diseases'),
(r'\bevil congregation\b','rebellious congregation'),
(r'\bevil news\b','bad news'),
(r'\bevil device\b','evil plan'),
(r'\bevil arrows\b','deadly arrows'),
]


def lexical_v3(ref: str, text: str) -> str:
    out=base.lexical_fix(ref,text)
    for a,b in POST_REPLACEMENTS.get(ref,[]):
        out=out.replace(a,b)
    for pat,repl in POST_REGEX:
        out=re.sub(pat,repl,out,flags=re.I)
    return out


def main():
    with CANDS.open(encoding='utf-8',newline='') as f:
        candidates=list(csv.DictReader(f,delimiter='\t'))
    byref=defaultdict(list)
    for r in candidates: byref[r['reference']].append(r)
    rows=[]
    lexical_count=0; generic_count=0
    for ref,rs in byref.items():
        before=rs[0]['text']; after=before; cats=[]
        if any(r['category']=='BROKENNESS LEXICAL REVIEW' for r in rs):
            after=lexical_v3(ref,after)
            if after != before:
                cats.append('lexical'); lexical_count += 1
        if ref in GENERIC_AFTER:
            # If the verse also has lexical repair, GENERIC_AFTER is expected to include
            # that lexical result only when applicable. Most entries are generic-only.
            expected_before=after
            if any(r['category']=='BROKENNESS LEXICAL REVIEW' for r in rs):
                # Currently only Deuteronomy 24:7 is both; its final generic text also
                # includes the lexical restoration to evil.
                pass
            after=GENERIC_AFTER[ref]
            if after != expected_before:
                cats.append('generic-pronoun'); generic_count += 1
        if after != before:
            rows.append({'reference':ref,'book':rs[0]['book'],'chapter':int(rs[0]['chapter']),'verse':int(rs[0]['verse']),'categories':','.join(cats),'before':before,'after':after})
    # Every lexical candidate is intentionally resolved; generic set is exact and finite.
    lexical_refs={r['reference'] for r in candidates if r['category']=='BROKENNESS LEXICAL REVIEW'}
    proposed_lex={r['reference'] for r in rows if 'lexical' in r['categories']}
    if lexical_refs != proposed_lex:
        raise SystemExit(f'Lexical coverage mismatch missing={sorted(lexical_refs-proposed_lex)[:20]} extra={sorted(proposed_lex-lexical_refs)[:20]}')
    proposed_generic={r['reference'] for r in rows if 'generic-pronoun' in r['categories']}
    if proposed_generic != set(GENERIC_AFTER):
        raise SystemExit(f'Generic coverage mismatch missing={sorted(set(GENERIC_AFTER)-proposed_generic)} extra={sorted(proposed_generic-set(GENERIC_AFTER))}')
    fields=['reference','book','chapter','verse','categories','before','after']
    with OUT.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)
    bybook=Counter(r['book'] for r in rows)
    summary={
      'approvedVerseChanges':len(rows),
      'lexicalVerseChanges':len(proposed_lex),
      'genericPronounVerseChanges':len(proposed_generic),
      'divinePronounAutoChanges':0,
      'broadMasculineTermAutoChanges':0,
      'genericHumanAutoChanges':0,
      'bookCounts':dict(bybook),
      'policy':'Finite release proposal. All 347 audited brokenness artifacts are resolved using source/context rules plus the attested pre-AI lexical value when ambiguity remains. Only 23 hand-reviewed formulaically generic pronoun rows are included. Heuristic divine and broad masculine-term candidates are explicitly excluded.'
    }
    SUMMARY.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
