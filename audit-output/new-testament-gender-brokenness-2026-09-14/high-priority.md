# New Testament Inclusive Language, Divine-Referent & Lexical Residual Audit

- Canonical commit: `91b6e7b9eb3f5a9f46efe63a04cedda1e49d527b`
- Canonical EPUB SHA-256: `d48ec5b7da0db10c7c44c518793228dc5b2d69edc6e57de838486d2aefbcf62f`
- Scope: all 27 New Testament books / 260 chapters
- Canonical verse paragraphs scanned: 7,956
- Nominal NT verse count: 7,957
- Candidate rows: 743 across 710 unique verses
- Important: candidate rows are review prompts, not a count of translation errors.

## Critical structural finding

Romans is the only New Testament book whose canonical paragraph inventory does not match the nominal verse inventory. The present EPUB has 432 Romans verse paragraphs rather than 433. Inspection shows that Romans 14:23 contains embedded `(14:24)`, `(14:25)`, and `(14:26)` doxology text; Romans 16:25 is empty; and Romans 16:26 contains the literal artifact `016:027`. This should be corrected as a separate verse-mapping/data-integrity task before a future release. The audit does **not** alter it.

## Category counts

- **MASCULINE TERM REVIEW:** 234
- **GENERIC PRONOUN HIGH PRIORITY:** 203
- **UNRIPENESS LEXICAL REVIEW:** 109
- **DIVINE-REFERENT REVIEW:** 70
- **GENERIC PRONOUN REVIEW:** 51
- **BROTHERS / SIBLING LANGUAGE REVIEW:** 46
- **SONS / CHILDREN LANGUAGE REVIEW:** 17
- **GENERIC-HUMAN HIGH PRIORITY:** 6
- **STRUCTURAL VERSE MAPPING:** 3
- **MALFORMED LANGUAGE REVIEW:** 3
- **BROKENNESS LEXICAL REVIEW:** 1

## Priority counts

- **CRITICAL:** 3
- **HIGH:** 392
- **REVIEW:** 348

## Editorial guardrails

- Greek/Aramaic source and immediate literary context govern; English surface forms only identify review candidates.
- Preserve actual men, male kinship, male-specific social roles, and Yeshua/Mashiach references where the source/context is male-specific.
- Check plural `adelphoi`/brother-language for mixed-community address; do not assume every “brothers” occurrence means “brothers and sisters.”
- Check “sons” constructions individually; some may have broader family/community scope, while others are intentionally male or idiomatic.
- Masculine divine pronouns are changed under the project method only where the immediate referent is unmistakably divine; uncertain, Yeshua/Messianic, or ambiguous “Lord” references are not auto-resolved.
- `Brokenness` and `unripeness` are lexical review flags. Neither should be replaced by one global word without Greek/context review.

## Critical and high-priority queue

### Romans 14:23 — STRUCTURAL VERSE MAPPING

> But the one who doubts is condemned if they eat, because it isn't of faith; and whatever is not of faith is sin. (14:24) Now to the one who is able to establish you according to my good news and the preaching of Yeshua the Messiah, according to the revelation of the mystery which has been kept secret through long ages, (14:25) but now is revealed, and by the Scriptures of the prophets, according to the commandment of the age-enduring God, is made known for obedience of faith to all the nations; (14:26) to the only wise God, through Yeshua the Messiah, to whom be the glory forever! Amen.

Signals: `embedded (14:24); embedded (14:25); embedded (14:26)`

The Romans 14:23 paragraph improperly contains three additional parenthetical verse labels and the doxology text. This is a verse-mapping/data-structure defect, not an inclusive-language judgment.

### Romans 16:25 — STRUCTURAL VERSE MAPPING

> 

Signals: `empty verse paragraph`

The canonical Romans 16:25 verse paragraph is empty while related doxology text is embedded earlier in Romans 14:23.

### Romans 16:26 — STRUCTURAL VERSE MAPPING

> 016:027

Signals: `literal artifact 016:027`

The canonical Romans 16:26 verse paragraph contains the literal artifact “016:027” instead of normal verse text.

### Matthew 2:2 — GENERIC PRONOUN HIGH PRIORITY

> "Where is the one who is born King of the Judeans? For we saw his star in the east, and have come to worship him."

Signals: `the one who; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 3:3 — GENERIC PRONOUN HIGH PRIORITY

> For this is the one who was spoken of by Yeshayahu the prophet, saying, "The voice of one crying in the wilderness, make ready the way of YHWH. Make his paths straight."

Signals: `the one who; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 3:11 — GENERIC PRONOUN HIGH PRIORITY

> I indeed immerse you in water for turning back, but the one who comes after me is mightier than I, whose shoes I am not worthy to carry. He will immerse you in the Ruach of Elohim.

Signals: `the one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 4:4 — GENERIC PRONOUN HIGH PRIORITY

> But he answered, "It is written, 'A person shall not live by bread alone, but by every word that proceeds out of the mouth of Elohim.'"

Signals: `A person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 5:11 — UNRIPENESS LEXICAL REVIEW

> "Blessed are you when people reproach you, persecute you, and say all kinds of unripeness against you falsely, for my sake.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 5:31 — GENERIC PRONOUN HIGH PRIORITY

> "It was also said, 'Whoever shall put away his wife, let him give her a writing of divorce,'

Signals: `Whoever; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 5:32 — GENERIC PRONOUN HIGH PRIORITY

> but I tell you that whoever puts away his wife, except for the cause of sexual immorality, makes her an adulteress; and whoever marries her when she is put away commits adultery.

Signals: `whoever; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 5:37 — UNRIPENESS LEXICAL REVIEW

> But let your 'Yes' be 'Yes' and your 'No' be 'No.' Whatever is more than these is of the unripe one.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 5:39 — UNRIPENESS LEXICAL REVIEW

> But I tell you, don't resist one who acts from unripeness; but whoever strikes you on your right cheek, turn to them the other also.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 5:45 — UNRIPENESS LEXICAL REVIEW

> that you may be children of your Cosmic Parent who is in heaven. For he makes his sun to rise on the unripe and the good, and sends rain on the just and the unjust.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 6:23 — UNRIPENESS LEXICAL REVIEW

> But if your eye is unripe, your whole body will be full of darkness. If therefore the light that is in you is darkness, how great is the darkness!

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 6:34 — UNRIPENESS LEXICAL REVIEW

> Therefore don't be anxious for tomorrow, for tomorrow will be anxious for itself. Each day's own unripeness is sufficient.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 7:11 — UNRIPENESS LEXICAL REVIEW

> If you then, being unripe and still able to sour, know how to give good gifts to your children, how much more will your Cosmic Parent who is in heaven give good things to those who seek from him!

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 7:17 — UNRIPENESS LEXICAL REVIEW

> Even so, every good tree produces good fruit; but the corrupt tree produces unripe fruit.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 7:18 — UNRIPENESS LEXICAL REVIEW

> A good tree can't produce unripe fruit, neither can a corrupt tree produce good fruit.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 8:9 — GENERIC PRONOUN HIGH PRIORITY

> For I am also a person under authority, having under myself soldiers. I tell this one, 'Go,' and he goes; and tell another, 'Come,' and he comes; and tell my servant, 'Do this,' and he does it."

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 8:27 — GENERIC PRONOUN HIGH PRIORITY

> The men marveled, saying, "What kind of a person is this, that even the wind and the sea obey him?"

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 9:2 — GENERIC PRONOUN HIGH PRIORITY

> Behold, they brought to him a person who was paralyzed, lying on a bed. Yeshua, seeing their faith, said to the paralytic, "Son, cheer up! Your sins are forgiven you."

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 9:4 — UNRIPENESS LEXICAL REVIEW

> Yeshua, knowing their thoughts, said, "Why do you think unripeness in your hearts?

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 9:32 — GENERIC-HUMAN HIGH PRIORITY

> As they went out, behold, a mute man who was demon possessed was brought to him.

Signals: `man who`

Universal/generic human language is explicitly male-coded and should be checked against Greek/Aramaic context for inclusive rendering.

### Matthew 11:3 — GENERIC PRONOUN HIGH PRIORITY

> and said to him, "Are you the one who comes, or should we look for another?"

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 12:10 — GENERIC PRONOUN HIGH PRIORITY

> And behold there was a person with a withered hand. They asked him, "Is it lawful to heal on the Sabbath day?" that they might accuse him.

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 12:18 — DIVINE-REFERENT REVIEW

> "Behold, my servant whom I have chosen; my beloved in whom my soul is well pleased: I will put my Ruach on him. He will proclaim justice to the nations.

Signals: `next-sentence-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Matthew 12:19 — GENERIC PRONOUN HIGH PRIORITY

> He will not strive, nor shout; neither will anyone hear his voice in the streets.

Signals: `anyone; he; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 12:34 — UNRIPENESS LEXICAL REVIEW

> You offspring of vipers, how can you, being unripe, speak good things? For out of the abundance of the heart, the mouth speaks.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 12:35 — UNRIPENESS LEXICAL REVIEW

> The good person out of their good treasure brings out good things, and the unripe person out of their unripe treasure brings out unripe things.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 12:39 — UNRIPENESS LEXICAL REVIEW

> But he answered them, "An unripe and adulterous generation seeks after a sign, but no sign will be given it but the sign of Yonah the prophet.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 12:45 — UNRIPENESS LEXICAL REVIEW

> Then he goes, and takes with himself seven other spirits more unripe than he is, and they enter in and dwell there. The last state of that person becomes worse than the first. Even so will it be also to this unripe generation."

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 12:48 — GENERIC PRONOUN HIGH PRIORITY

> But he answered the one who spoke to him, "Who is my mother? Who are my brothers?"

Signals: `the one who; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 13:19 — UNRIPENESS LEXICAL REVIEW

> When anyone hears the word of the reign, and doesn't understand it, the unripe one comes, and snatches away that which has been sown in their heart. This is what was sown by the roadside.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 13:24 — GENERIC PRONOUN HIGH PRIORITY

> He set another parable before them, saying, "The reign of the heavens is like a person who sowed good seed in their field,

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 13:37 — GENERIC PRONOUN HIGH PRIORITY

> He answered them, "The one who sows the good seed is the Human One,

Signals: `The one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 13:38 — UNRIPENESS LEXICAL REVIEW

> the field is the world; and the good seed, these are the children of the reign; and the darnel weeds are the children of the unripe one.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 13:52 — GENERIC PRONOUN HIGH PRIORITY

> He said to them, "Therefore, every scribe who has been made a disciple in the reign of the heavens is like a person who is a householder, who brings out of their treasure new and old things."

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 15:19 — UNRIPENESS LEXICAL REVIEW

> For out of the heart come forth unripe thoughts, murders, adulteries, sexual sins, thefts, false testimony, and blasphemies.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 15:24 — GENERIC PRONOUN HIGH PRIORITY

> But he answered, "I wasn't sent to anyone but the lost sheep of the house of Israel."

Signals: `anyone; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 16:4 — UNRIPENESS LEXICAL REVIEW

> An unripe and adulterous generation seeks after a sign, and there will be no sign given to it, except the sign of the prophet Yonah." He left them, and departed.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 16:24 — GENERIC PRONOUN HIGH PRIORITY

> Then Yeshua said to his disciples, "If anyone desires to come after me, let them deny themselves, and take up their cross, and follow me.

Signals: `anyone; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 16:27 — GENERIC PRONOUN HIGH PRIORITY

> For the Human One will come in the glory of his Cosmic Parent with his angels, and then he will render to everyone according to their deeds.

Signals: `everyone; he; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 17:14 — GENERIC PRONOUN HIGH PRIORITY

> When they came to the multitude, a person came to him, kneeling down to him, saying,

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 18:24 — GENERIC PRONOUN HIGH PRIORITY

> When they had begun to reconcile, one was brought to the one who owed him ten thousand talents.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 19:4 — GENERIC PRONOUN HIGH PRIORITY

> He answered, "Haven't you read that the one who made them from the beginning made them male and female,

Signals: `the one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 19:9 — GENERIC PRONOUN HIGH PRIORITY

> I tell you that whoever divorces his wife, except for sexual immorality, and marries another, commits adultery; and the one who marries her when she is divorced commits adultery."

Signals: `whoever; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 20:15 — UNRIPENESS LEXICAL REVIEW

> Isn't it lawful for me to do what I want to with what I own? Or is your eye unripeness, because I am good?'

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 21:9 — GENERIC PRONOUN HIGH PRIORITY

> The multitudes who went before him, and who followed kept shouting, "Hosanna to the son of Dawid! Blessed is the one who comes in the name of YHWH! Hosanna in the highest!"

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 22:11 — GENERIC PRONOUN HIGH PRIORITY

> But when the king came in to see the guests, he saw there a person who didn't have on wedding clothing,

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 22:16 — GENERIC PRONOUN HIGH PRIORITY

> They sent their disciples to him, along with the Herodians, saying, "Teacher, we know that you are honest, and teach the way of Elohim in truth, no matter who you teach, for you aren't partial to anyone.

Signals: `anyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 22:24 — GENERIC PRONOUN HIGH PRIORITY

> saying, "Teacher, Moshe said, 'If someone dies, having no children, his brother shall marry his wife, and raise up seed for his brother.'

Signals: `someone; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 22:46 — GENERIC PRONOUN HIGH PRIORITY

> No one was able to answer him a word, neither did anyone dare ask him any more questions from that day forth.

Signals: `anyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 24:48 — UNRIPENESS LEXICAL REVIEW

> But if that unripe servant should say in his heart, 'My master is delaying his coming,'

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Matthew 25:28 — GENERIC PRONOUN HIGH PRIORITY

> Take away therefore the talent from him, and give it to the one who has the ten talents.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 26:48 — GENERIC PRONOUN HIGH PRIORITY

> Now the one who betrayed him gave them a sign, saying, "Whoever I kiss, they are the one. Seize him."

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 26:71 — GENERIC PRONOUN HIGH PRIORITY

> When they had gone out onto the porch, someone else saw him, and said to those who were there, "This man also was with Yeshua of Natzeret."

Signals: `someone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 27:32 — GENERIC PRONOUN HIGH PRIORITY

> As they came out, they found a person of Kyrene, Shimon by name, and they compelled him to go with them, that they might carry his cross.

Signals: `a person; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Matthew 27:43 — DIVINE-REFERENT REVIEW

> He trusts in Elohim. Let Elohim deliver him now, if Elohim wants him; for he said, 'I am the Son of Elohim.'"

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Mark 1:37 — GENERIC PRONOUN HIGH PRIORITY

> and they found him, and told him, "Everyone is looking for you."

Signals: `Everyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 5:2 — GENERIC PRONOUN HIGH PRIORITY

> When they had come out of the boat, immediately there met him out of the tombs a person with an unclean spirit,

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 5:18 — GENERIC PRONOUN HIGH PRIORITY

> As they were entering into the boat, the one who had been possessed by demons begged him that they might be with him.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 7:18 — GENERIC PRONOUN HIGH PRIORITY

> He said to them, "Are you thus without understanding also? Don't you perceive that whatever goes into a person from outside can't defile them,

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 7:21 — UNRIPENESS LEXICAL REVIEW

> For from within, out of the hearts of people, proceed unripe thoughts, adulteries, sexual sins, murders, thefts,

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Mark 7:22 — UNRIPENESS LEXICAL REVIEW

> covetings, wickedness, deceit, lustful desires, an unripe eye, blasphemy, pride, and foolishness.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Mark 7:23 — UNRIPENESS LEXICAL REVIEW

> All these unripe things come from within, and defile the person."

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Mark 7:24 — GENERIC PRONOUN HIGH PRIORITY

> From there he arose, and went away into the borders of Tzor and Tzidon. They entered into a house, and didn't want anyone to know it, but they couldn't escape notice.

Signals: `anyone; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 7:32 — GENERIC PRONOUN HIGH PRIORITY

> They brought to him one who was deaf and had an impediment in their speech. They begged him to lay his hand on him.

Signals: `one who; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 8:25 — GENERIC PRONOUN HIGH PRIORITY

> Then again he laid his hands on his eyes. They looked intently, and was restored, and saw everyone clearly.

Signals: `everyone; he; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 8:26 — GENERIC PRONOUN HIGH PRIORITY

> They sent him away to their house, saying, "Don't enter into the village, nor tell anyone in the village."

Signals: `anyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 9:23 — GENERIC PRONOUN HIGH PRIORITY

> Yeshua said to him, "If you can trust, all things are possible to the one who believes."

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 9:35 — GENERIC PRONOUN HIGH PRIORITY

> He sat down, and called the twelve; and they said to them, "If anyone wants to be first, they shall be last of all, and servant of all."

Signals: `anyone; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 9:38 — GENERIC PRONOUN HIGH PRIORITY

> Yochanan said to him, "Teacher, we saw someone who doesn't follow us casting out demons in your name; and we forbade them, because they don't follow us."

Signals: `someone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 9:39 — GENERIC PRONOUN HIGH PRIORITY

> But Yeshua said, "Don't forbid him, for there is no one who will do a mighty work in my name, and be able quickly to speak harmfully of me.

Signals: `one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 10:11 — GENERIC PRONOUN HIGH PRIORITY

> They said to them, "Whoever divorces his wife, and marries another, commits adultery against her.

Signals: `Whoever; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 11:3 — GENERIC PRONOUN HIGH PRIORITY

> If anyone asks you, 'Why are you doing this?' say, 'The Master needs him;' and immediately he will send him back here."

Signals: `anyone; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 12:1 — GENERIC PRONOUN HIGH PRIORITY

> He began to speak to them in parables. "A person planted a vineyard, put a hedge around it, dug a pit for the winepress, built a tower, rented it out to a farmer, and went into another country.

Signals: `A person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 12:14 — GENERIC PRONOUN HIGH PRIORITY

> When they had come, they asked him, "Teacher, we know that you are honest, and don't defer to anyone; for you aren't partial to anyone, but truly teach the way of Elohim. Is it lawful to pay taxes to Caesar, or not?

Signals: `anyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 12:19 — GENERIC PRONOUN HIGH PRIORITY

> "Teacher, Moshe wrote to us, 'If someone's brother dies, and leaves a wife behind him, and leaves no children, that their brother should take his wife, and raise up offspring for his brother.'

Signals: `someone; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 14:13 — GENERIC PRONOUN HIGH PRIORITY

> They sent two of their disciples, and said to them, "Go into the city, and there you will meet a person carrying a pitcher of water. Follow him,

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 14:44 — GENERIC PRONOUN HIGH PRIORITY

> Now the one who betrayed him had given them a sign, saying, "Whoever I will kiss, that is they. Seize him, and lead him away safely."

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Mark 15:43 — DIVINE-REFERENT REVIEW

> Yosef of Arimathaea, a prominent council member who also himself was looking for the reign of Elohim, came. He boldly went in to Pilatus, and asked for Yeshua' body.

Signals: `next-sentence-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Luke 1:15 — DIVINE-REFERENT REVIEW

> For he will be great in the sight of God, and he will drink no wine nor strong drink. He will be filled with the Ruach of Elohim, even from his mother's womb.

Signals: `explicit-divine-subject; next-sentence-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Luke 1:49 — GENERIC PRONOUN HIGH PRIORITY

> For the one who is mighty has done great things for me. Holy is his name.

Signals: `the one who; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 2:25 — GENERIC PRONOUN HIGH PRIORITY

> Behold, there was a person in Yerushalayim whose name was Shimon. This man was righteous and devout, looking for the consolation of Israel, and the Ruach of Elohim was on him.

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 2:26 — DIVINE-REFERENT REVIEW

> It had been revealed to him by the Ruach of Elohim that he should not see death before he had seen the Master's Messiah.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Luke 3:11 — GENERIC PRONOUN HIGH PRIORITY

> He answered them, "The one who has two coats, let them give to the one who has none. The one who has food, let them do likewise."

Signals: `The one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 3:14 — GENERIC PRONOUN HIGH PRIORITY

> Soldiers also asked him, saying, "What about us? What must we do?" He said to them, "Extort from no one by violence, neither accuse anyone wrongfully. Be content with your wages."

Signals: `anyone; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 3:19 — UNRIPENESS LEXICAL REVIEW

> but Herodes the tetrarch, being reproved by him for Herodias, his brother's wife, and for all the unripe things which Herodes had done,

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Luke 4:4 — GENERIC PRONOUN HIGH PRIORITY

> Yeshua answered him, saying, "It is written, 'A person shall not live by bread alone, but by every word of Elohim.'"

Signals: `A person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 4:18 — DIVINE-REFERENT REVIEW

> "The Ruach of YHWH is on me, because he has anointed me to proclaim good news to the poor. He has sent me to heal the brokenhearted, to proclaim release to the captives, recovery of sight to the blind, and to send the crushed away into freedom,

Signals: `explicit-divine-subject; next-sentence-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Luke 5:1 — DIVINE-REFERENT REVIEW

> Now it happened, while the multitude pressed on him and heard the word of Elohim, that he was standing by the lake of Gennesaret.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Luke 5:12 — GENERIC PRONOUN HIGH PRIORITY

> It happened, while they were in one of the cities, behold, there was a person full of leprosy. When he saw Yeshua, he fell on his face, and begged him, saying, "Master, if you want to, you can make me clean."

Signals: `a person; he; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 6:6 — GENERIC PRONOUN HIGH PRIORITY

> It also happened on another Sabbath that he entered into the synagogue and taught. There was a person there, and their right hand was withered.

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 6:8 — GENERIC PRONOUN HIGH PRIORITY

> But he knew their thoughts; and they said to the one who had the withered hand, "Rise up, and stand in the middle." He arose and stood.

Signals: `the one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 6:22 — UNRIPENESS LEXICAL REVIEW

> Blessed are you when people shall hate you, and when they shall exclude and mock you, and throw out your name as unripe, for the Human One's sake.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Luke 6:35 — DIVINE-REFERENT REVIEW

> But love your enemies, and do good, and lend, expecting nothing back; and your reward will be great, and you will be children of the Most High; for he is kind toward the unthankful and the unripe.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Luke 6:35 — UNRIPENESS LEXICAL REVIEW

> But love your enemies, and do good, and lend, expecting nothing back; and your reward will be great, and you will be children of the Most High; for he is kind toward the unthankful and the unripe.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Luke 6:45 — UNRIPENESS LEXICAL REVIEW

> The good person out of the good treasure of their heart brings out that which is good, and the unripe person out of the unripe treasure of their heart brings out what is unripe, for out of the abundance of the heart, their mouth speaks.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Luke 7:8 — GENERIC PRONOUN HIGH PRIORITY

> For I also am a person placed under authority, having under myself soldiers. I tell this one, 'Go!' and he goes; and to another, 'Come!' and he comes; and to my servant, 'Do this,' and he does it."

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 7:15 — GENERIC PRONOUN HIGH PRIORITY

> The one who was dead sat up, and began to speak. And he gave him to his mother.

Signals: `The one who; he; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 7:19 — GENERIC PRONOUN HIGH PRIORITY

> Yochanan, calling to himself two of his disciples, sent them to Yeshua, saying, "Are you the one who is coming, or should we look for another?"

Signals: `the one who; himself; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 7:20 — GENERIC PRONOUN HIGH PRIORITY

> When the men had come to him, they said, "Yochanan the Baptizer has sent us to you, saying, 'Are you the one who comes, or should we look for another?'"

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 7:21 — UNRIPENESS LEXICAL REVIEW

> In that hour he cured many of diseases and plagues and unripe spirits; and to many who were blind he gave sight.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Luke 8:2 — UNRIPENESS LEXICAL REVIEW

> and certain women who had been healed of unripe spirits and infirmities: Maryam who was called Magdalene, from whom seven demons had gone out;

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Luke 9:11 — DIVINE-REFERENT REVIEW

> But the multitudes, perceiving it, followed him. He welcomed them, and spoke to them of the reign of Elohim, and he cured those who needed healing.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Luke 9:38 — GENERIC PRONOUN HIGH PRIORITY

> Behold, a person from the crowd called out, saying, "Teacher, I beg you to look at my son, for he is my only child.

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 9:50 — GENERIC PRONOUN HIGH PRIORITY

> Yeshua said to him, "Don't forbid him, for the one who is not against us is for us."

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 10:2 — DIVINE-REFERENT REVIEW

> Then he said to them, "The harvest is indeed plentiful, but the laborers are few. Pray therefore to God of the harvest, that he may send out laborers into his harvest.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Luke 10:22 — GENERIC PRONOUN HIGH PRIORITY

> Turning to the disciples, he said, "All things have been delivered to me by my Cosmic Parent. No one knows who the Son is, except the Cosmic Parent, and who the Cosmic Parent is, except the Son, and anyone to whom the Son desires to reveal the Cosmic Parent."

Signals: `anyone; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 10:37 — GENERIC PRONOUN HIGH PRIORITY

> They said, "The one who showed mercy on him." Then Yeshua said to him, "Go and do likewise."

Signals: `The one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 11:13 — UNRIPENESS LEXICAL REVIEW

> If you then, being unripe and still able to sour, know how to give good gifts to your children, how much more will your heavenly Cosmic Parent give the Ruach of Elohim to those who seek from him?"

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Luke 11:22 — GENERIC PRONOUN HIGH PRIORITY

> But when someone stronger attacks him and overcomes him, they take from him his whole armor in which he trusted, and divide his spoils.

Signals: `someone; he; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 11:26 — UNRIPENESS LEXICAL REVIEW

> Then it goes, and takes seven other spirits more unripe than itself, and they enter in and dwell there. The last state of that person becomes worse than the first."

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Luke 11:29 — UNRIPENESS LEXICAL REVIEW

> When the multitudes were gathering together to him, he began to say, "This is an unripe generation. It seeks after a sign. No sign will be given to it but the sign of Yonah, the prophet.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Luke 11:34 — UNRIPENESS LEXICAL REVIEW

> The lamp of the body is the eye. Therefore when your eye is good, your whole body is also full of light; but when it is unripe, your body also is full of darkness.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Luke 12:15 — GENERIC PRONOUN HIGH PRIORITY

> He said to them, "Beware! Keep yourselves from covetousness, for a person's life doesn't consist of the abundance of the things which they possess."

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 14:2 — GENERIC-HUMAN HIGH PRIORITY

> Behold, a certain man who had dropsy was in front of him.

Signals: `man who`

Universal/generic human language is explicitly male-coded and should be checked against Greek/Aramaic context for inclusive rendering.

### Luke 14:8 — GENERIC PRONOUN HIGH PRIORITY

> "When you are invited by anyone to a marriage feast, don't sit in the best seat, since perhaps someone more honorable than you might be invited by him,

Signals: `anyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 14:12 — GENERIC PRONOUN HIGH PRIORITY

> They also said to the one who had invited him, "When you make a dinner or a supper, don't call your friends, nor your brothers, nor your kinsmen, nor rich neighbors, or perhaps they might also return the favor, and pay you back.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 14:15 — GENERIC PRONOUN HIGH PRIORITY

> When one of those who sat at the table with him heard these things, they said to him, "Blessed is the one who will feast in the reign of Elohim!"

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 14:31 — GENERIC PRONOUN HIGH PRIORITY

> Or what king, as he goes to encounter another king in war, will not sit down first and consider whether he is able with ten thousand to meet the one who comes against him with twenty thousand?

Signals: `the one who; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 16:1 — GENERIC-HUMAN HIGH PRIORITY

> He also said to his disciples, "There was a certain rich man who had a manager. An accusation was made to him that this man was wasting his possessions.

Signals: `man who`

Universal/generic human language is explicitly male-coded and should be checked against Greek/Aramaic context for inclusive rendering.

### Luke 16:18 — GENERIC PRONOUN HIGH PRIORITY

> Everyone who divorces his wife, and marries another, commits adultery. The one who marries one who is divorced from a husband commits adultery.

Signals: `Everyone; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 17:20 — DIVINE-REFERENT REVIEW

> Being asked by the Pharisees when the reign of Elohim would come, he answered them, "The reign of Elohim doesn't come with observation;

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Luke 18:14 — GENERIC PRONOUN HIGH PRIORITY

> I tell you, this man went down to his house justified rather than the other; for everyone who exalts themselves will be humbled, but the one who humbles themselves will be exalted."

Signals: `everyone; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 19:2 — GENERIC PRONOUN HIGH PRIORITY

> There was a person named Zakkai. He was a chief tax collector, and he was rich.

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 19:7 — GENERIC PRONOUN HIGH PRIORITY

> When they saw it, they all murmured, saying, "He has gone in to lodge with a person who is a sinner."

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 19:24 — GENERIC PRONOUN HIGH PRIORITY

> They said to those who stood by, 'Take the mina away from him, and give it to the one who has the ten minas.'

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 19:31 — GENERIC PRONOUN HIGH PRIORITY

> If anyone asks you, 'Why are you untying it?' say to him: 'The Master needs it.'"

Signals: `anyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 20:9 — GENERIC PRONOUN HIGH PRIORITY

> He began to tell the people this parable. "A person planted a vineyard, and rented it out to some farmers, and went into another country for a long time.

Signals: `A person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 20:21 — GENERIC PRONOUN HIGH PRIORITY

> They asked him, "Teacher, we know that you say and teach what is right, and aren't partial to anyone, but truly teach the way of Elohim.

Signals: `anyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 20:28 — GENERIC PRONOUN HIGH PRIORITY

> They asked him, "Teacher, Moshe wrote to us that if someone's brother dies having a wife, and they are childless, their brother should take the wife, and raise up children for their brother.

Signals: `someone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 22:47 — GENERIC PRONOUN HIGH PRIORITY

> While they were still speaking, behold, a multitude, and the one who was called Yehuda, one of the twelve, was leading them. He came near to Yeshua to kiss him.

Signals: `the one who; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 22:58 — GENERIC PRONOUN HIGH PRIORITY

> After a little while someone else saw him, and said, "You also are one of them!" But Shimon (called Kepha) answered, "Man, I am not!"

Signals: `someone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 22:64 — GENERIC PRONOUN HIGH PRIORITY

> Having blindfolded him, they struck him on the face and asked him, "Prophesy! Who is the one who struck you?"

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Luke 23:22 — UNRIPENESS LEXICAL REVIEW

> He said to them the third time, "Why? What unripeness has this man done? I have found no capital crime in him. I will therefore chastise him and release him."

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Luke 23:35 — DIVINE-REFERENT REVIEW

> The people stood watching. The rulers with them also scoffed at him, saying, "He saved others. Let him save himself, if this is the Messiah of Elohim, his chosen one!"

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 1:12 — DIVINE-REFERENT REVIEW

> But as many as received him, to them he gave the right to become Elohim's children, to those who trust in his name:

Signals: `divine-attribute`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 1:15 — GENERIC PRONOUN HIGH PRIORITY

> Yochanan testified about him. He cried out, saying, "This was he of whom I said, 'The one who comes after me has surpassed me, for he was before me.'"

Signals: `The one who; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 1:18 — DIVINE-REFERENT REVIEW

> No one has seen Elohim at any time. The one-of-a-kind Son, who is in the bosom of the Cosmic Parent, he has made the Cosmic Parent known.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 1:27 — GENERIC PRONOUN HIGH PRIORITY

> He is the one who comes after me, who is preferred before me, whose sandal strap I'm not worthy to loosen."

Signals: `the one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 1:30 — GENERIC PRONOUN HIGH PRIORITY

> This is he of whom I said, 'After me comes a person who is preferred before me, for he was before me.'

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 1:33 — GENERIC PRONOUN HIGH PRIORITY

> I didn't recognize him, but the one who sent me to immerse in water, they said to me, 'On whomever you will see the Ruach descending, and remaining on him, the same is the one who baptizes in the Ruach of Elohim.'

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 2:10 — GENERIC PRONOUN HIGH PRIORITY

> and said to him, "Everyone serves the good wine first, and when the guests have drunk freely, then that which is worse. You have kept the good wine until now!"

Signals: `Everyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 2:25 — GENERIC PRONOUN HIGH PRIORITY

> and because they didn't need for anyone to testify concerning humanity; for he himself knew what was in humanity.

Signals: `anyone; he; himself`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 3:4 — GENERIC PRONOUN HIGH PRIORITY

> Nikodemos said to him, "How can a person be born when they are old? Can they enter a second time into their mother’s womb, and be born?"

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 3:15 — GENERIC PRONOUN HIGH PRIORITY

> that whoever believes in him should not perish, but have life of the age.

Signals: `whoever; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 3:16 — GENERIC PRONOUN HIGH PRIORITY

> For Elohim so loved the world that Elohim gave the one and only Son, so that whoever trusts in him should not perish, but have life of the age to come.

Signals: `whoever; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 3:18 — GENERIC PRONOUN HIGH PRIORITY

> The one who believes in him is not judged. The one who doesn't trust has been judged already, because they have not believed in the name of the one and only Son of Elohim.

Signals: `The one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 3:19 — UNRIPENESS LEXICAL REVIEW

> This is the judgment, that the light has come into the world, and people loved the darkness rather than the light; for their works were unripe.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### John 3:20 — UNRIPENESS LEXICAL REVIEW

> For everyone who acts from unripeness hates the light, and doesn't come to the light, lest their works would be exposed.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### John 3:26 — GENERIC PRONOUN HIGH PRIORITY

> They came to Yochanan, and said to him, "Rabbi, the one who was with you beyond the Yarden, to whom you have testified, behold, the same baptizes, and everyone is coming to him."

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 3:29 — GENERIC PRONOUN HIGH PRIORITY

> The one who has the bride is the bridegroom; but the friend of the bridegroom, who stands and hears him, rejoices greatly because of the bridegroom's voice. This, my joy, therefore is made full.

Signals: `The one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 3:35 — DIVINE-REFERENT REVIEW

> The Cosmic Parent loves the Son, and has given all things into his hand.

Signals: `divine-attribute`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 4:10 — DIVINE-REFERENT REVIEW

> Yeshua answered her, "If you knew the gift of Elohim, and who it is who says to you, 'Give me a drink,' you would have asked him, and he would have given you living water."

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 4:25 — GENERIC PRONOUN HIGH PRIORITY

> The woman said to him, "I know that Messiah comes," (the one who is called Messiah). "When he has come, he will declare to us all things."

Signals: `the one who; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 4:33 — GENERIC PRONOUN HIGH PRIORITY

> The disciples therefore said one to another, "Has anyone brought him something to eat?"

Signals: `anyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 5:12 — GENERIC PRONOUN HIGH PRIORITY

> Then they asked him, "Who is the one who said to you, 'Take up your mat, and walk'?"

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 5:20 — DIVINE-REFERENT REVIEW

> For the Cosmic Parent has affection for the Son, and shows him all things that he himself does. He will show him greater works than these, that you may marvel.

Signals: `explicit-divine-subject; next-sentence-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 5:23 — GENERIC PRONOUN HIGH PRIORITY

> that all may honor the Son, even as they honor the Cosmic Parent. The one who doesn't honor the Son doesn't honor the Cosmic Parent who sent him.

Signals: `The one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 5:29 — UNRIPENESS LEXICAL REVIEW

> and will come out; those who have done good, to the resurrection of life; and those who have acted from unripeness, to the resurrection of judgment.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### John 6:7 — GENERIC PRONOUN HIGH PRIORITY

> Pilipos answered him, "Two hundred denarii worth of bread is not sufficient for them, that everyone of them may receive a little."

Signals: `everyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 6:40 — GENERIC PRONOUN HIGH PRIORITY

> This is the will of the one who sent me, that everyone who sees the Son, and believes in him, should have life of the age; and I will raise them up at the last day."

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 6:46 — GENERIC PRONOUN HIGH PRIORITY

> Not that anyone has seen the Cosmic Parent, except the one who is from Elohim. He has seen the Cosmic Parent.

Signals: `anyone; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 6:71 — GENERIC PRONOUN HIGH PRIORITY

> Now they spoke of Yehuda, the son of Shimon Iscariot, for it was the one who would betray him, being one of the twelve.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 7:7 — UNRIPENESS LEXICAL REVIEW

> The world can't hate you, but it hates me, because I testify about it, that its works are unripe.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### John 7:50 — GENERIC PRONOUN HIGH PRIORITY

> Nikodemos (the one who came to him by night, being one of them) said to them,

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 8:7 — GENERIC PRONOUN HIGH PRIORITY

> But when they continued asking him, they looked up and said to them, "The one who is without sin among you, let them throw the first stone at her."

Signals: `The one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 8:26 — GENERIC PRONOUN HIGH PRIORITY

> I have many things to speak and to judge concerning you. However the one who sent me is true; and the things which I heard from him, these I say to the world."

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 8:29 — GENERIC PRONOUN HIGH PRIORITY

> The one who sent me is with me. The Cosmic Parent hasn't left me alone, for I always do the things that are pleasing to him."

Signals: `The one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 8:33 — GENERIC PRONOUN HIGH PRIORITY

> They answered him, "We are Avraham's seed, and have never been in bondage to anyone. How do you say, 'You will be made free?'"

Signals: `anyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 8:52 — GENERIC PRONOUN HIGH PRIORITY

> Then the Judeans said to him, "Now we know that you have a demon. Avraham died, and the prophets; and you say, 'If someone keeps my word, they will never taste of death.'

Signals: `someone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 9:16 — DIVINE-REFERENT REVIEW

> Some therefore of the Pharisees said, "This man is not from Elohim, because he doesn't keep the Sabbath." Others said, "How can a person who is a sinner do such signs?" There was division among them.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 9:16 — GENERIC PRONOUN HIGH PRIORITY

> Some therefore of the Pharisees said, "This man is not from Elohim, because he doesn't keep the Sabbath." Others said, "How can a person who is a sinner do such signs?" There was division among them.

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 9:18 — GENERIC PRONOUN HIGH PRIORITY

> The Judeans therefore did not trust concerning him, that they had been blind, and had received their sight, until they called the parents of the one who had received their sight,

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 9:22 — GENERIC PRONOUN HIGH PRIORITY

> His parents said these things because they feared the Judeans; for the Judeans had already agreed that if anyone would confess him as Messiah, they would be put out of the synagogue.

Signals: `anyone; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 9:24 — GENERIC PRONOUN HIGH PRIORITY

> So they called the one who was blind a second time, and said to him, "Give glory to Elohim. We know that this a person is a sinner."

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 9:33 — DIVINE-REFERENT REVIEW

> If this man were not from Elohim, he could do nothing."

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 9:37 — GENERIC PRONOUN HIGH PRIORITY

> Yeshua said to him, "You have both seen him, and it is the one who speaks with you."

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 10:33 — GENERIC PRONOUN HIGH PRIORITY

> The Judeans answered him, "We don't stone you for a good work, but for blasphemy: because you, being a person, make yourself Elohim."

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 10:41 — GENERIC PRONOUN HIGH PRIORITY

> Many came to him. They said, "Yochanan indeed did no sign, but everything that Yochanan said about this a person is true."

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 11:27 — GENERIC PRONOUN HIGH PRIORITY

> She said to him, "Yes, Master. I have come to trust that you are the Messiah, Elohim's Son, the one who comes into the world."

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 11:39 — GENERIC PRONOUN HIGH PRIORITY

> Yeshua said, "Take away the stone." Marta, the sister of the one who was dead, said to him, "Master, by this time there is a stench, for he has been dead four days."

Signals: `the one who; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 11:44 — GENERIC PRONOUN HIGH PRIORITY

> The one who was dead came out, bound hand and foot with wrappings, and his face was wrapped around with a cloth. Yeshua said to them, "Free him, and let him go."

Signals: `The one who; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 11:48 — GENERIC PRONOUN HIGH PRIORITY

> If we leave him alone like this, everyone will trust in him, and the Romans will come and take away both our place and our nation."

Signals: `everyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 11:57 — GENERIC PRONOUN HIGH PRIORITY

> Now the chief priests and the Pharisees had commanded that if anyone knew where he was, they should report it, that they might seize him.

Signals: `anyone; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 12:13 — GENERIC PRONOUN HIGH PRIORITY

> they took the branches of the palm trees, and went out to meet him, and cried out, "Hosanna! Blessed is the one who comes in the name of YHWH, the King of Israel!"

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 13:1 — DIVINE-REFERENT REVIEW

> Now before the feast of the Passover, Yeshua, knowing that his time had come that he would depart from this world to the Cosmic Parent, having loved his own who were in the world, he loved them to the end.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 13:3 — DIVINE-REFERENT REVIEW

> Yeshua, knowing that the Cosmic Parent had given all things into his hands, and that he came forth from Elohim, and was going to Elohim,

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 13:10 — GENERIC PRONOUN HIGH PRIORITY

> Yeshua said to him, "Someone who has bathed only needs to have their feet washed, but is completely clean. You are clean, but not all of you."

Signals: `Someone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 13:11 — GENERIC PRONOUN HIGH PRIORITY

> For he knew the one who would betray him, therefore he said, "You are not all clean."

Signals: `the one who; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 14:9 — GENERIC PRONOUN HIGH PRIORITY

> Yeshua said to him, "Have I been with you such a long time, and do you not know me, Pilipos? The one who has seen me has seen the Cosmic Parent. How do you say, 'Show us the Cosmic Parent?'

Signals: `The one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 14:16 — DIVINE-REFERENT REVIEW

> I will pray to the Cosmic Parent, and he will give you another Counselor, that he may be with you forever,--

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 14:23 — GENERIC PRONOUN HIGH PRIORITY

> Yeshua answered him, "If someone loves me, they will keep my word. My Cosmic Parent will love them, and we will come to them, and make our home with them.

Signals: `someone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 15:10 — DIVINE-REFERENT REVIEW

> If you keep my commandments, you will remain in my love; even as I have kept my Cosmic Parent's commandments, and remain in his love.

Signals: `divine-attribute`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 15:16 — DIVINE-REFERENT REVIEW

> You didn't choose me, but I chose you, and appointed you, that you should go and bear fruit, and that your fruit should remain; that whatever you seek of the Cosmic Parent in the life of my name, he may give it to you.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 16:15 — DIVINE-REFERENT REVIEW

> All things whatever the Cosmic Parent has are mine; therefore I said that he takes of mine, and will declare it to you.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 16:23 — DIVINE-REFERENT REVIEW

> "In that day you will ask me no questions. Most certainly I tell you, whatever you may seek of the Cosmic Parent in the living authority and presence of my name, he will give it to you.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### John 17:15 — UNRIPENESS LEXICAL REVIEW

> I pray not that you would take them from the world, but that you would keep them from the unripe one.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### John 18:17 — GENERIC PRONOUN HIGH PRIORITY

> Then the maid who kept the door said to Shimon (called Kepha), "Are you also one of this a person's disciples?" He said, "I am not."

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 18:23 — UNRIPENESS LEXICAL REVIEW

> Yeshua answered him, "If I have spoken from unripeness, testify of the unripeness; but if I have spoken well, why do you beat me?"

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### John 18:30 — GENERIC PRONOUN HIGH PRIORITY

> They answered him, "If this man weren't a person who acts from unripeness, we wouldn't have delivered him up to you."

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 18:30 — UNRIPENESS LEXICAL REVIEW

> They answered him, "If this man weren't a person who acts from unripeness, we wouldn't have delivered him up to you."

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### John 18:31 — GENERIC PRONOUN HIGH PRIORITY

> Pilatus therefore said to them, "Take him yourselves, and judge him according to your law." Therefore the Judeans said to him, "It is not lawful for us to put anyone to death,"

Signals: `anyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 18:37 — GENERIC PRONOUN HIGH PRIORITY

> Pilatus therefore said to him, "Are you a king then?" Yeshua answered, "You say that I am a king. For this reason I have been born, and for this reason I have come into the world, that I should testify to the truth. Everyone who is of the truth listens to my voice."

Signals: `Everyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 19:12 — GENERIC PRONOUN HIGH PRIORITY

> At this, Pilatus was seeking to release him, but the Judeans cried out, saying, "If you release this man, you aren't Caesar's friend! Everyone who makes themselves a king speaks against Caesar!"

Signals: `Everyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 19:35 — GENERIC PRONOUN HIGH PRIORITY

> The one who has seen has testified, and his testimony is true. He knows that he tells the truth, that you may trust.

Signals: `The one who; he; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### John 20:31 — DIVINE-REFERENT REVIEW

> but these are written, that you may trust that Yeshua is the Messiah, the Son of Elohim, and that believing you may have life in his name.

Signals: `divine-attribute`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 2:22 — GENERIC PRONOUN HIGH PRIORITY

> "People of Israel, hear these words! Yeshua of Natzeret, a person approved by God to you by mighty works and wonders and signs which God did by him in the midst of you, even as you yourselves know,

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 2:24 — DIVINE-REFERENT REVIEW

> whom God raised up, having freed him from the agony of death, because it was not possible that he should be held by it.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 2:33 — DIVINE-REFERENT REVIEW

> Being therefore exalted by the right hand of God, and having received from the Cosmic Parent the promise of the Ruach of Elohim, he has poured out this, which you now see and hear.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 3:2 — GENERIC-HUMAN HIGH PRIORITY

> A certain man who was lame from his mother's womb was being carried, whom they laid daily at the door of the temple which is called Beautiful, to ask gifts for the needy of those who entered into the temple.

Signals: `man who`

Universal/generic human language is explicitly male-coded and should be checked against Greek/Aramaic context for inclusive rendering.

### Acts 3:10 — GENERIC PRONOUN HIGH PRIORITY

> They recognized him, that it was the one who used to sit begging for gifts for the needy at the Beautiful Gate of the temple. They were filled with wonder and amazement at what had happened to him.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 3:11 — GENERIC-HUMAN HIGH PRIORITY

> As the lame man who was healed held on to Shimon (called Kepha) and Yochanan, all the people ran together to them in the porch that is called Shlomo's, greatly wondering.

Signals: `man who`

Universal/generic human language is explicitly male-coded and should be checked against Greek/Aramaic context for inclusive rendering.

### Acts 3:26 — GENERIC PRONOUN HIGH PRIORITY

> God, having raised up God's servant, Yeshua, sent him to you first, to bless you, in turning away everyone of you from your wickedness."

Signals: `everyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 5:31 — DIVINE-REFERENT REVIEW

> God exalted him with God's right hand to be a Prince and a Savior, to give turning back to Israel, and remission of sins.

Signals: `devotion-object`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 7:6 — DIVINE-REFERENT REVIEW

> God spoke in this way: that his seed would live as aliens in a strange land, and that they would be enslaved and mistreated for four hundred years.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 7:24 — GENERIC PRONOUN HIGH PRIORITY

> Seeing one of them suffer wrong, he defended him, and avenged the one who was oppressed, striking the Egyptian.

Signals: `the one who; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 7:25 — DIVINE-REFERENT REVIEW

> He supposed that his brothers understood that God, by his hand, was giving them deliverance; but they didn't understand.

Signals: `divine-attribute`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 7:27 — GENERIC PRONOUN HIGH PRIORITY

> But the one who did their neighbor wrong pushed him away, saying, 'Who made you a ruler and a judge over us?

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 7:38 — GENERIC PRONOUN HIGH PRIORITY

> This is the one who was in the assembly in the wilderness with the angel that spoke to him on Mount Sinai, and with our fathers, who received living oracles to give to us,

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 7:44 — GENERIC PRONOUN HIGH PRIORITY

> "Our fathers had the tent of the testimony in the wilderness, even as the one who spoke to Moshe commanded him to make it according to the pattern that they had seen;

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 8:18 — DIVINE-REFERENT REVIEW

> Now when Shimon saw that the Ruach of Elohim was given through the laying on of the emissaries' hands, he offered them money,

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 8:27 — GENERIC PRONOUN HIGH PRIORITY

> He arose and went; and behold, there was a person of Ethiopia, a eunuch of great authority under Candace, queen of the Ethiopians, who was over all her treasure, who had come to Yerushalayim to worship.

Signals: `a person; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 8:31 — GENERIC PRONOUN HIGH PRIORITY

> They said, "How can I, unless someone explains it to me?" He begged Pilipos to come up and sit with him.

Signals: `someone; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 8:39 — DIVINE-REFERENT REVIEW

> When they came up out of the water, the Ruach of YHWH caught Pilipos away, and the eunuch didn't see him any more, for he went on his way rejoicing.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 9:11 — GENERIC PRONOUN HIGH PRIORITY

> The Master said to him, "Arise, and go to the street which is called Straight, and inquire in the house of Yehudah for one named Shaul, a person of Tarsos. For behold, he is praying,

Signals: `a person; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 9:21 — GENERIC PRONOUN HIGH PRIORITY

> All who heard him were amazed, and said, "Isn't this the one who in Yerushalayim made havoc of those who called on this name? And he had come here intending to bring them bound before the chief priests!"

Signals: `the one who; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 9:29 — DIVINE-REFERENT REVIEW

> preaching boldly in the name of YHWH. He spoke and disputed against the Hellenists, but they were seeking to kill him.

Signals: `next-sentence-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 10:2 — GENERIC PRONOUN HIGH PRIORITY

> a devout man, and one who revered God with all his house, who gave gifts for the needy generously to the people, and always prayed to God.

Signals: `one who; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 10:26 — GENERIC PRONOUN HIGH PRIORITY

> But Shimon (called Kepha) raised him up, saying, "Stand up! I myself am also a person."

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 10:43 — GENERIC PRONOUN HIGH PRIORITY

> All the prophets testify about him, that through their name everyone who believes in him will receive remission of sins."

Signals: `everyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 11:23 — DIVINE-REFERENT REVIEW

> who, when he had come, and had seen the grace of God, was glad. He exhorted them all, that with purpose of heart they should remain near to God.

Signals: `next-sentence-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 12:7 — DIVINE-REFERENT REVIEW

> And behold, a messenger of YHWH stood by him, and a light shone in the cell. He struck Shimon (called Kepha) on the side, and woke him up, saying, "Stand up quickly!" His chains fell off from his hands.

Signals: `next-sentence-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 12:23 — DIVINE-REFERENT REVIEW

> Immediately a messenger of YHWH struck him, because he didn't give God the glory, and he was eaten by worms and died.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 13:9 — DIVINE-REFERENT REVIEW

> But Shaul, who is also called Shaul, filled with the Ruach of Elohim, fastened his eyes on him,

Signals: `divine-attribute`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 13:11 — GENERIC PRONOUN HIGH PRIORITY

> Now, behold, the hand of God is on you, and you will be blind, not seeing the sun for a season!" Immediately a mist and darkness fell on him. They went around seeking someone to lead him by the hand.

Signals: `someone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 13:22 — GENERIC PRONOUN HIGH PRIORITY

> When God had removed him, God raised up Dawid to be their king, to whom God also testified, 'I have found Dawid the son of Yishai, a person after my heart, who will do all my will.'

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 13:39 — GENERIC PRONOUN HIGH PRIORITY

> and by him everyone who believes is justified from all things, from which you could not be justified by the law of Moshe.

Signals: `everyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 16:9 — GENERIC PRONOUN HIGH PRIORITY

> A vision appeared to Shaul in the night. There was a person of Makedonia standing, begging him, and saying, "Come over into Makedonia and help us."

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 18:2 — GENERIC PRONOUN HIGH PRIORITY

> They found a certain Judean named Akylas, a person of Pontus by race, who had recently come from Italy, with his wife Priskilla, because Claudius had commanded all the Judeans to depart from Roma. He came to them,

Signals: `a person; he; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 18:25 — DIVINE-REFERENT REVIEW

> This man had been instructed in the way of YHWH; and being fervent in spirit, he spoke and taught accurately the things concerning Yeshua, although he knew only the immersion of Yochanan.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 19:12 — UNRIPENESS LEXICAL REVIEW

> so that even handkerchiefs or aprons were carried away from his body to the sick, and the unripe spirits went out.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Acts 19:13 — UNRIPENESS LEXICAL REVIEW

> But some of the itinerant Judeans, exorcists, took on themselves to invoke over those who had the unripe spirits the name of Master Yeshua, saying, "We adjure you by Yeshua whom Shaul preaches."

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Acts 19:15 — UNRIPENESS LEXICAL REVIEW

> The unripe spirit answered, "Yeshua I know, and Shaul I know, but who are you?"

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Acts 19:16 — UNRIPENESS LEXICAL REVIEW

> The person in whom the unripe spirit was leaped on them, and overpowered them, and prevailed against them, so that they fled out of that house naked and wounded.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Acts 19:38 — GENERIC PRONOUN HIGH PRIORITY

> If therefore Demetrius and the craftsmen who are with him have a matter against anyone, the courts are open, and there are proconsuls. Let them press charges against one another.

Signals: `anyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 21:4 — DIVINE-REFERENT REVIEW

> Having found disciples, we stayed there seven days. These said to Shaul through the Ruach, that he should not go up to Yerushalayim.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Acts 21:11 — GENERIC PRONOUN HIGH PRIORITY

> Coming to us, and taking Shaul's belt, he bound his own feet and hands, and said, "Thus says the Ruach of Elohim: 'So will the Judeans at Yerushalayim bind the one who owns this belt, and will deliver him into the hands of the Gentiles.'"

Signals: `the one who; he; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 21:28 — GENERIC PRONOUN HIGH PRIORITY

> crying out, "People of Israel, help! This is the one who teaches all people everywhere against the people, and the law, and this place. Moreover, he also brought Greeks into the temple, and has defiled this holy place!"

Signals: `the one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 22:25 — GENERIC PRONOUN HIGH PRIORITY

> When they had tied him up with thongs, Shaul asked the centurion who stood by, "Is it lawful for you to scourge a person who is a Roman, and not found guilty?"

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 23:9 — UNRIPENESS LEXICAL REVIEW

> A great clamor arose, and some of the scribes of the Pharisees part stood up, and contended, saying, "We find no unripeness in this man. But if a spirit or angel has spoken to him, let's not fight against God!"

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Acts 25:16 — GENERIC PRONOUN HIGH PRIORITY

> To whom I answered that it is not the custom of the Romans to give up anyone to destruction, before the accused has met the accusers face to face, and has had opportunity to make their defense concerning the matter laid against him.

Signals: `anyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Acts 27:35 — DIVINE-REFERENT REVIEW

> When he had said this, and had taken bread, he gave thanks to God in the presence of all, and he broke it, and began to eat.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Romans 1:29 — UNRIPENESS LEXICAL REVIEW

> being filled with all unrighteousness, sexual immorality, wickedness, covetousness, maliciousness; full of envy, murder, strife, deceit, unripe habits, secret slanderers,

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Romans 1:30 — UNRIPENESS LEXICAL REVIEW

> backbiters, hateful to God, insolent, haughty, boastful, inventors of unripe things, disobedient to parents,

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Romans 2:9 — UNRIPENESS LEXICAL REVIEW

> oppression and anguish, on every person who acts from unripeness, to the Judean first, and also to the Greek.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Romans 3:8 — UNRIPENESS LEXICAL REVIEW

> Why not (as we are slanderously reported, and as some affirm that we say), "Let us act from unripeness, that good may come?" Those who say so are justly condemned.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Romans 4:20 — DIVINE-REFERENT REVIEW

> Yet, looking to the promise of God, he didn't waver through unbelief, but grew strong through faith, giving glory to God,

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Romans 5:19 — MALFORMED LANGUAGE REVIEW

> For as through the one a person's disobedience many were made sinners, even so through the obedience of the one, many will be made righteous.

Signals: `One a person`

Surface English is grammatically malformed or internally incoherent and warrants manual correction after checking the source/context.

### Romans 7:19 — UNRIPENESS LEXICAL REVIEW

> For the good which I desire, I don't do; but the unripeness which I don't desire, that I practice.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Romans 7:21 — UNRIPENESS LEXICAL REVIEW

> I find then the law, that, to me, while I desire to do good, unripeness is present.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Romans 8:3 — DIVINE-REFERENT REVIEW

> For what the law couldn't do, in that it was weak through the flesh, God did, sending God’s own Son in the likeness of sinful flesh and for sin, he condemned sin in the flesh;

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Romans 8:9 — MALFORMED LANGUAGE REVIEW

> But you are not in the flesh but in the Ruach, if it is so that the Ruach of God dwells in you. But if anyone doesn't have the Ruach of Messiah, they are not their.

Signals: `they are not their`

Surface English is grammatically malformed or internally incoherent and warrants manual correction after checking the source/context.

### Romans 8:29 — DIVINE-REFERENT REVIEW

> For whom he foreknew, he also predestined to be conformed to the image of God’s Son, that he might be the firstborn among many brothers and sisters.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Romans 8:32 — GENERIC PRONOUN HIGH PRIORITY

> The one who didn't spare their own Son, but delivered him up for us all, how would they not also with him freely give us all things?

Signals: `The one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Romans 9:33 — GENERIC PRONOUN HIGH PRIORITY

> even as it is written, "Behold, I lay in Tzion a stumbling stone and a rock of offense; and no one who believes in him will be disappointed."

Signals: `one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Romans 10:11 — GENERIC PRONOUN HIGH PRIORITY

> For the Scripture says, "Whoever believes in him will not be disappointed."

Signals: `Whoever; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Romans 11:32 — DIVINE-REFERENT REVIEW

> For God has shut up all to disobedience, that he might have mercy on all.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Romans 12:9 — UNRIPENESS LEXICAL REVIEW

> Let love be without hypocrisy. Abhor that which is unripeness. Cling to that which is good.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Romans 12:17 — UNRIPENESS LEXICAL REVIEW

> repay no one unripeness for unripeness. Respect what is honorable in the sight of all people.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Romans 12:21 — UNRIPENESS LEXICAL REVIEW

> Don't be overcome by unripeness, but overcome unripeness with good.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Romans 13:3 — UNRIPENESS LEXICAL REVIEW

> For rulers are not a terror to the good work, but to the unripeness. Do you desire to have no fear of the authority? Do that which is good, and you will have praise from the same,

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Romans 13:4 — GENERIC PRONOUN HIGH PRIORITY

> for he is a servant of God to you for good. But if you do that which is unripeness, be afraid, for he doesn't bear the sword in vain; for they are a servant of God, an avenger for wrath to the one who acts from unripeness.

Signals: `the one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Romans 13:4 — UNRIPENESS LEXICAL REVIEW

> for he is a servant of God to you for good. But if you do that which is unripeness, be afraid, for he doesn't bear the sword in vain; for they are a servant of God, an avenger for wrath to the one who acts from unripeness.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Romans 14:2 — MALFORMED LANGUAGE REVIEW

> One a person has faith to eat all things, but the one who is weak eats only vegetables.

Signals: `One a person`

Surface English is grammatically malformed or internally incoherent and warrants manual correction after checking the source/context.

### Romans 14:20 — UNRIPENESS LEXICAL REVIEW

> Don't overthrow God's work for food's sake. All things indeed are clean, however it is unripeness for that person who creates a stumbling block by eating.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Romans 15:8 — DIVINE-REFERENT REVIEW

> Now I say that Messiah has been made a servant of the circumcision for the truth of God, that he might confirm the promises given to the fathers,

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Romans 15:12 — GENERIC PRONOUN HIGH PRIORITY

> Again, Yeshayahu says, "There will be the root of Yishai, the one who arises to rule over the Gentiles; in him the Gentiles will hope."

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Romans 16:19 — UNRIPENESS LEXICAL REVIEW

> For your obedience has become known to all. I rejoice therefore over you. But I desire to have you wise in that which is good, but innocent in that which is unripeness.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Corinthians 5:13 — BROKENNESS LEXICAL REVIEW

> But those who are outside, God judges. "Put away the broken person from among yourselves."

Signals: `broken person`

The English brokenness/broken wording may flatten distinct Greek senses and should be checked against source/context.

### 1 Corinthians 6:16 — GENERIC PRONOUN HIGH PRIORITY

> Or don't you know that the one who is joined to a prostitute is one body? For, "The two," says he, "will become one flesh."

Signals: `the one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 Corinthians 7:18 — GENERIC PRONOUN HIGH PRIORITY

> Was anyone called having been circumcised? Let him not become uncircumcised. Has anyone been called in uncircumcision? Let him not be circumcised.

Signals: `anyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 Corinthians 7:36 — GENERIC-HUMAN HIGH PRIORITY

> But if any man thinks that he is behaving inappropriately toward his virgin, if she is past the flower of her age, and if need so requires, let him do what he desires. He doesn't sin. Let them marry.

Signals: `any man`

Universal/generic human language is explicitly male-coded and should be checked against Greek/Aramaic context for inclusive rendering.

### 1 Corinthians 10:6 — UNRIPENESS LEXICAL REVIEW

> Now these things were our examples, to the intent we should not lust after unripe things, as they also lusted.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Corinthians 11:14 — GENERIC PRONOUN HIGH PRIORITY

> Doesn't even nature itself teach you that if someone has long hair, it is a dishonor to him?

Signals: `someone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 Corinthians 13:5 — UNRIPENESS LEXICAL REVIEW

> doesn't behave itself inappropriately, doesn't seek its own way, is not provoked, takes no account of unripeness;

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Corinthians 15:28 — GENERIC PRONOUN HIGH PRIORITY

> When all things have been subjected to him, then the Son will also himself be subjected to the one who subjected all things to him, that God may be all in all.

Signals: `the one who; him; himself`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 Corinthians 15:33 — UNRIPENESS LEXICAL REVIEW

> Don't be deceived! "unripe companionships corrupt good morals."

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 2 Corinthians 5:21 — GENERIC PRONOUN HIGH PRIORITY

> For the one who knew no sin they made to be sin on our behalf; so that in him we might become the righteousness of God.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 2 Corinthians 9:15 — DIVINE-REFERENT REVIEW

> Now thanks be to God for his unspeakable gift!

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### 2 Corinthians 13:7 — UNRIPENESS LEXICAL REVIEW

> Now I pray to God that you act from no unripeness; not that we may appear approved, but that you may do that which is honorable, though we are as reprobate.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Galatians 1:4 — UNRIPENESS LEXICAL REVIEW

> who gave himself for our sins, that he might deliver us out of this present unripeness age, according to the will of our God and Cosmic Parent--

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Ephesians 5:16 — UNRIPENESS LEXICAL REVIEW

> redeeming the time, because the days are unripeness.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Ephesians 6:9 — GENERIC PRONOUN HIGH PRIORITY

> You masters, do the same things to them, and give up threatening, knowing that the one who is both their Master and yours is in heaven, and there is no partiality with him.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Ephesians 6:13 — UNRIPENESS LEXICAL REVIEW

> Therefore, put on the whole armor of God, that you may be able to withstand in the unripeness day, and, having done all, to stand.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Ephesians 6:16 — UNRIPENESS LEXICAL REVIEW

> above all, taking up the shield of faith, with which you will be able to quench all the fiery darts of the unripe one.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Philippians 2:9 — DIVINE-REFERENT REVIEW

> Therefore God also highly exalted him, and gave to him the name which is above every name;

Signals: `devotion-object`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Philippians 3:2 — UNRIPENESS LEXICAL REVIEW

> Beware of the dogs, beware of the workers of unripeness, beware of the false circumcision.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Colossians 1:21 — UNRIPENESS LEXICAL REVIEW

> You, being in past times alienated and enemies in your mind in your works of unripeness,

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Colossians 3:5 — UNRIPENESS LEXICAL REVIEW

> Put to death therefore your members which are on the earth: sexual immorality, uncleanness, depraved passion, unripe desire, and covetousness, which is idolatry;

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Thessalonians 5:15 — UNRIPENESS LEXICAL REVIEW

> See that no one returns unripeness for unripeness to anyone, but always follow after that which is good, for one another, and for all.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Thessalonians 5:22 — UNRIPENESS LEXICAL REVIEW

> Abstain from every form of unripeness.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 2 Thessalonians 2:4 — DIVINE-REFERENT REVIEW

> the one who opposes and exalts themselves against all that is called God or that is worshiped; so that he sits as God in the temple of God, setting himself up as God.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### 2 Thessalonians 2:4 — GENERIC PRONOUN HIGH PRIORITY

> the one who opposes and exalts themselves against all that is called God or that is worshiped; so that he sits as God in the temple of God, setting himself up as God.

Signals: `the one who; he; himself`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 2 Thessalonians 3:2 — UNRIPENESS LEXICAL REVIEW

> and that we may be delivered from unreasonable and people of unripeness; for not all have faith.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 2 Thessalonians 3:3 — UNRIPENESS LEXICAL REVIEW

> But the Master is faithful, who will establish you, and guard you from the unripe one.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Timothy 6:4 — UNRIPENESS LEXICAL REVIEW

> he is conceited, knowing nothing, but obsessed with arguments, disputes, and word battles, from which come envy, strife, reviling, unripe suspicions,

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Timothy 6:10 — UNRIPENESS LEXICAL REVIEW

> For the love of money is a root of all kinds of unripeness. Some have been led astray from the faith in their greed, and have pierced themselves through with many sorrows.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 2 Timothy 3:13 — UNRIPENESS LEXICAL REVIEW

> But people of unripeness and impostors will grow worse and worse, deceiving and being deceived.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 2 Timothy 4:14 — UNRIPENESS LEXICAL REVIEW

> Alexandros, the coppersmith, did much unripeness to me. The Master will repay him according to his works,

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 2 Timothy 4:18 — UNRIPENESS LEXICAL REVIEW

> And the Master will deliver me from every work of unripeness, and will preserve me for his heavenly Reign; to whom be the glory forever and ever. Amen.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Titus 1:12 — UNRIPENESS LEXICAL REVIEW

> One of them, a prophet of their own, said, "Cretans are always liars, unripe beasts, and idle gluttons."

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Titus 2:8 — UNRIPENESS LEXICAL REVIEW

> and soundness of speech that can't be condemned; that the one who opposes you may be ashamed, having no unripe thing to say about us.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Hebrews 1:3 — DIVINE-REFERENT REVIEW

> God’s Son is the radiance of his glory, the exact imprint of his being, upholding all things by the word of his power. When he had by himself made purification for our sins, he sat down on the right hand of the Majesty on high,

Signals: `divine-attribute`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Hebrews 1:5 — DIVINE-REFERENT REVIEW

> For to which of the angels did the Cosmic Parent say at any time, "You are my Son. Today I have brought you forth." and again, "I will be to him a Cosmic Parent, and he will be to me a Son."

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Hebrews 1:6 — DIVINE-REFERENT REVIEW

> Again, when he brings in the firstborn into the world he says, "Let all the angels of God worship him."

Signals: `devotion-object`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Hebrews 3:2 — GENERIC PRONOUN HIGH PRIORITY

> who was faithful to the one who appointed him, as also was Moshe in all their house.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Hebrews 3:12 — UNRIPENESS LEXICAL REVIEW

> Beware, brothers and sisters, lest perhaps there be in any one of you an unripe heart of unbelief, in falling away from the living God;

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Hebrews 5:1 — DIVINE-REFERENT REVIEW

> For every high priest, being taken from among people, is appointed for people in things pertaining to God, that he may offer both gifts and sacrifices for sins.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Hebrews 5:5 — GENERIC PRONOUN HIGH PRIORITY

> So also Messiah didn't glorify himself to be made a high priest, but it was the one who said to him, "You are my Son. Today I have brought you forth."

Signals: `the one who; him; himself`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Hebrews 5:7 — GENERIC PRONOUN HIGH PRIORITY

> He, in the days of his flesh, having offered up prayers and petitions with strong crying and tears to the one who was able to save him from death, and having been heard for his reverent awe,

Signals: `the one who; he; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Hebrews 5:14 — UNRIPENESS LEXICAL REVIEW

> But solid food is for those who are full grown, who by reason of use have their senses exercised to discern good and unripeness.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Hebrews 6:13 — DIVINE-REFERENT REVIEW

> For when God made a promise to Avraham, since he could swear by none greater, he swore by himself,

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Hebrews 7:25 — DIVINE-REFERENT REVIEW

> Therefore he is also able to save to the uttermost those who draw near to God through him, seeing that he lives forever to make intercession for them.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Hebrews 8:5 — DIVINE-REFERENT REVIEW

> who serve a copy and shadow of the heavenly things, even as Moshe was warned by God when he was about to make the tabernacle, for he said, "See, you shall make everything according to the pattern that was shown to you on the mountain."

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Hebrews 10:22 — UNRIPENESS LEXICAL REVIEW

> let's draw near with a true heart in fullness of faith, having our hearts sprinkled from an unripe conscience, and having our body washed with pure water,

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Hebrews 11:4 — DIVINE-REFERENT REVIEW

> By faith, Hevel offered to God a more excellent sacrifice than Qayin, through which he had testimony given to him that he was righteous, God testifying with respect to his gifts; and through it he, being dead, still speaks.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Hebrews 11:6 — GENERIC PRONOUN HIGH PRIORITY

> Without faith it is impossible to be well pleasing to him, for the one who comes to God must trust that God exists, and that God rewards those who seek God.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Hebrews 11:27 — GENERIC PRONOUN HIGH PRIORITY

> By faith, he left Mitzrayim, not fearing the wrath of the king; for they endured, as seeing the one who is invisible.

Signals: `the one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### James 1:12 — GENERIC PRONOUN HIGH PRIORITY

> Blessed is the one who endures temptation, for when they have been approved, they will receive the crown of life, which the Master promised to those who love him.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### James 1:13 — UNRIPENESS LEXICAL REVIEW

> Let no one say when they are tempted, "I am tempted by God," for God can't be tempted by unripeness, and God tempts no one.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### James 2:4 — UNRIPENESS LEXICAL REVIEW

> haven't you shown partiality among yourselves, and become judges with unripe thoughts?

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### James 2:23 — DIVINE-REFERENT REVIEW

> and the Scripture was fulfilled which says, "Avraham believed God, and it was accounted to him as righteousness;" and he was called the friend of God.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### James 3:8 — UNRIPENESS LEXICAL REVIEW

> But nobody can tame the tongue. It is a restless unripeness, full of deadly poison.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### James 3:16 — UNRIPENESS LEXICAL REVIEW

> For where jealousy and selfish ambition are, there is confusion and every unripeness deed.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### James 4:8 — DIVINE-REFERENT REVIEW

> Draw near to God, and he will draw near to you. Cleanse your hands, you sinners; and purify your hearts, you double-minded.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### James 4:10 — DIVINE-REFERENT REVIEW

> Humble yourselves in the sight of God, and he will exalt you.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### James 4:16 — UNRIPENESS LEXICAL REVIEW

> But now you glory in your boasting. All such boasting is unripeness.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Peter 1:17 — GENERIC PRONOUN HIGH PRIORITY

> If you call on him as Cosmic Parent, who without respect of persons judges according to each a person's work, pass the time of your living as foreigners here in reverence:

Signals: `a person; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 Peter 2:1 — UNRIPENESS LEXICAL REVIEW

> Putting away therefore all wickedness, all deceit, hypocrisies, envies, and all unripeness speaking,

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Peter 2:6 — GENERIC PRONOUN HIGH PRIORITY

> Because it is contained in Scripture, "Behold, I lay in Tzion a chief cornerstone, chosen, and precious: The one who believes in him will not be disappointed."

Signals: `The one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 Peter 2:12 — UNRIPENESS LEXICAL REVIEW

> having good behavior among the nations, so in that of which they speak against you as people who act from unripeness, they may by your good works, which they see, glorify God in the day of visitation.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Peter 2:14 — UNRIPENESS LEXICAL REVIEW

> or to governors, as sent by him for vengeance on people who act from unripeness and for praise to those who do well.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Peter 2:23 — GENERIC PRONOUN HIGH PRIORITY

> Who, when he was cursed, didn't curse back. When he suffered, didn't threaten, but committed himself to the one who judges righteously;

Signals: `the one who; he; himself`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 Peter 3:9 — UNRIPENESS LEXICAL REVIEW

> not rendering unripeness for unripeness, or reviling for reviling; but instead blessing; knowing that to this were you called, that you may inherit a blessing.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Peter 3:10 — UNRIPENESS LEXICAL REVIEW

> For, "The one who would love life, and see good days, let them keep their tongue from unripeness, and their lips from speaking deceit.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Peter 3:11 — UNRIPENESS LEXICAL REVIEW

> Let them turn away from unripeness, and do good. Let them seek peace, and pursue it.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Peter 3:12 — UNRIPENESS LEXICAL REVIEW

> For the eyes of the Master are on the righteous, and the Master’s ears open to their prayer; but the face of YHWH is against those who act from unripeness."

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Peter 3:16 — UNRIPENESS LEXICAL REVIEW

> having a good conscience; that, while you are spoken against as people who act from unripeness, they may be disappointed who curse your good manner of life in Messiah.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Peter 3:17 — UNRIPENESS LEXICAL REVIEW

> For it is better, if it is God's will, that you suffer for doing well than for doing unripeness.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 Peter 4:15 — UNRIPENESS LEXICAL REVIEW

> For let none of you suffer as a murderer, or a thief, or an unripeness doer, or a meddler in other people's matters.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 2 Peter 2:16 — GENERIC PRONOUN HIGH PRIORITY

> but he was rebuked for his own disobedience. A mute donkey spoke with a person's voice and stopped the madness of the prophet.

Signals: `a person; he; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 John 2:4 — GENERIC PRONOUN HIGH PRIORITY

> One who says, "I know him," and doesn't keep his commandments, is a liar, and the truth isn't in them.

Signals: `One who; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 John 2:5 — GENERIC PRONOUN HIGH PRIORITY

> But whoever keeps God's word, God's love has most certainly been perfected in them. This is how we know that we are in him:

Signals: `whoever; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 John 2:6 — GENERIC PRONOUN HIGH PRIORITY

> the one who says they remain in him ought also to walk just as he walked.

Signals: `the one who; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 John 2:13 — UNRIPENESS LEXICAL REVIEW

> I write to you, fathers, because you know the one who is from the beginning. I write to you, young people, because you have overcome the unripe one. I write to you, little children, because you know the Cosmic Parent.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 John 2:14 — UNRIPENESS LEXICAL REVIEW

> I have written to you, fathers, because you know the one who is from the beginning. I have written to you, young people, because you are strong, and the word of God remains in you, and you have overcome the unripe one.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 John 2:27 — GENERIC PRONOUN HIGH PRIORITY

> As for you, the anointing which you received from him remains in you, and you don't need for anyone to teach you. But as his anointing teaches you concerning all things, and is true, and is no lie, and even as it taught you, you will remain in him.

Signals: `anyone; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 John 2:29 — GENERIC PRONOUN HIGH PRIORITY

> If you know that they are righteous, you know that everyone who practices righteousness is born of him.

Signals: `everyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 John 3:3 — GENERIC PRONOUN HIGH PRIORITY

> Everyone who has this hope set on him purifies themselves, even as he is pure.

Signals: `Everyone; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 John 3:6 — GENERIC PRONOUN HIGH PRIORITY

> Whoever remains in him doesn't sin. Whoever sins hasn't seen him, neither knows him.

Signals: `Whoever; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 John 3:8 — DIVINE-REFERENT REVIEW

> The one who sins is of the Slanderer, for the Slanderer has been sinning from the beginning. To this end the Son of God was revealed, that he might destroy the works of the Slanderer.

Signals: `explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### 1 John 3:8 — GENERIC PRONOUN HIGH PRIORITY

> The one who sins is of the Slanderer, for the Slanderer has been sinning from the beginning. To this end the Son of God was revealed, that he might destroy the works of the Slanderer.

Signals: `The one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 John 3:12 — UNRIPENESS LEXICAL REVIEW

> unlike Qayin, who was of the unripe one, and killed his brother. Why did he kill him? Because his works were unripe, and his brother's righteous.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 John 3:24 — GENERIC PRONOUN HIGH PRIORITY

> The one who keeps their commandments remains in him, and they in him. By this we know that he remains in us, by the Ruach which he gave us.

Signals: `The one who; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 John 4:21 — GENERIC PRONOUN HIGH PRIORITY

> This commandment we have from him, that the one who loves God should also love their brother or sister.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 John 5:1 — GENERIC PRONOUN HIGH PRIORITY

> Whoever believes that Yeshua is the Messiah is born of God. Whoever loves the father also loves the child who is born of him.

Signals: `Whoever; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### 1 John 5:18 — UNRIPENESS LEXICAL REVIEW

> We know that whoever is born of God doesn't sin, but the one who was born of God keeps themselves, and the unripe one doesn't touch them.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 1 John 5:19 — UNRIPENESS LEXICAL REVIEW

> We know that we are of God, and the whole world lies in the power of the unripe one.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 2 John 1:11 — UNRIPENESS LEXICAL REVIEW

> for the one who welcomes them participates in their works of unripeness.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### 3 John 1:11 — UNRIPENESS LEXICAL REVIEW

> Beloved, don't imitate that which is unripeness, but that which is good. The one who does good is of God. The one who acts from unripeness hasn't seen God.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Revelation 1:1 — DIVINE-REFERENT REVIEW

> This is the Revelation of Yeshua the Messiah, which God gave him to show to his servants the things which must happen soon, which he sent and made known by his angel to his servant, Yochanan,

Signals: `divine-attribute`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Revelation 2:2 — UNRIPENESS LEXICAL REVIEW

> "I know your works, and your toil and perseverance, and that you can't tolerate people of unripeness, and have tested those who call themselves emissaries, and they are not, and found them false.

Signals: `unripeness`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Revelation 2:18 — DIVINE-REFERENT REVIEW

> "To the angel of the assembly in Thyatira write: "The Son of God, who has his eyes like a flame of fire, and his feet are like burnished brass, says these things:

Signals: `divine-attribute; explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Revelation 6:2 — GENERIC PRONOUN HIGH PRIORITY

> And behold, a white horse, and the one who sat on it had a bow. A crown was given to him, and he came forth conquering, and to conquer.

Signals: `the one who; he; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Revelation 6:4 — GENERIC PRONOUN HIGH PRIORITY

> Another came forth, a red horse. To the one who sat on it was given power to take peace from the earth, and that they should kill one another. There was given to him a great sword.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Revelation 6:5 — GENERIC PRONOUN HIGH PRIORITY

> When he opened the third seal, I heard the third living creature saying, "Come and see!" And behold, a black horse, and the one who sat on it had a balance in their hand.

Signals: `the one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Revelation 6:8 — GENERIC PRONOUN HIGH PRIORITY

> And behold, a pale horse, and the one who sat on it, their name was Death. Hades followed with him. Authority over one fourth of the earth, to kill with the sword, with famine, with death, and by the wild animals of the earth was given to him.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Revelation 6:13 — UNRIPENESS LEXICAL REVIEW

> The stars of the sky fell to the earth, like a fig tree dropping its unripe figs when it is shaken by a great wind.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Revelation 7:2 — DIVINE-REFERENT REVIEW

> I saw another angel ascend from the sunrise, having the seal of the living God. He cried with a loud voice to the four angels to whom it was given to harm the earth and the sea,

Signals: `next-sentence-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Revelation 7:15 — DIVINE-REFERENT REVIEW

> Therefore they are before the throne of God, they serve him day and night in his temple. The one who sits on the throne will spread their tent over them.

Signals: `devotion-object`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Revelation 7:15 — GENERIC PRONOUN HIGH PRIORITY

> Therefore they are before the throne of God, they serve him day and night in his temple. The one who sits on the throne will spread their tent over them.

Signals: `The one who; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Revelation 10:7 — DIVINE-REFERENT REVIEW

> but in the days of the voice of the seventh angel, when he is about to sound, then the mystery of God is finished, as he declared to his servants, the prophets.

Signals: `divine-attribute`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Revelation 12:9 — GENERIC PRONOUN HIGH PRIORITY

> The great dragon was thrown down, the old serpent, the one who is called the Slanderer and the Adversary, the deceiver of the whole world. He was thrown down to the earth, and his angels were thrown down with him.

Signals: `the one who; he; him; his`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Revelation 13:8 — GENERIC PRONOUN HIGH PRIORITY

> All who dwell on the earth will worship him, everyone whose name has not been written from the foundation of the world in the book of life of the Lamb who has been killed.

Signals: `everyone; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Revelation 14:7 — GENERIC PRONOUN HIGH PRIORITY

> He said with a loud voice, "Revere God, and give God glory; for the hour of God’s judgment has come. Worship the one who made the heaven, the earth, the sea, and the springs of waters!"

Signals: `the one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Revelation 14:10 — DIVINE-REFERENT REVIEW

> he also will drink of the wine of the wrath of God, which is prepared unmixed in the cup of God’s anger. He will be tormented with fire and sulfur in the presence of the holy angels, and in the presence of the Lamb.

Signals: `next-sentence-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Revelation 16:2 — UNRIPENESS LEXICAL REVIEW

> The first went, and poured out his bowl into the earth, and it became a harmful and harmful and unripe sore on the people who had the mark of the beast, and who worshiped his image.

Signals: `unripe`

“Unripe/unripeness” is unusual English in these moral/ethical contexts and may be a prior AI lexical artifact. Review the underlying Greek and immediate context; choose a contextual rendering rather than a global substitution.

### Revelation 16:19 — DIVINE-REFERENT REVIEW

> The great city was divided into three parts, and the cities of the nations fell. Bavel the great was remembered in the sight of God, to give to her the cup of the wine of the fierceness of his wrath.

Signals: `divine-attribute`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

### Revelation 19:11 — GENERIC PRONOUN HIGH PRIORITY

> I saw the heaven opened, and behold, a white horse, and the one who sat on it is called Faithful and True. In righteousness he judges and makes war.

Signals: `the one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Revelation 20:6 — GENERIC PRONOUN HIGH PRIORITY

> Blessed and holy is the one who has part in the first resurrection. Over these, the second death has no power, but they will be priests of God and of Messiah, and will reign with him one thousand years.

Signals: `the one who; him`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Revelation 21:5 — GENERIC PRONOUN HIGH PRIORITY

> The one who sits on the throne said, "Behold, I am making all things new." He said, "Write, for these words of God are faithful and true."

Signals: `The one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Revelation 21:6 — GENERIC PRONOUN HIGH PRIORITY

> He said to me, "It is done! I am the Alpha and the Omega, the Beginning and the End. I will give freely to the one who is thirsty from the spring of the water of life.

Signals: `the one who; he`

A strongly generic English antecedent is paired with masculine pronouns; likely inclusive-language inconsistency.

### Revelation 22:3 — DIVINE-REFERENT REVIEW

> There will be no curse any more. The throne of God and of the Lamb will be in it, and his servants serve him.

Signals: `devotion-object; divine-attribute; explicit-divine-subject`

Conservative heuristic indicates a masculine English pronoun may refer to an unmistakably divine antecedent. Verify coreference; if divine, project method prefers repeating the established divine name/title. Yeshua/Mashiach and ambiguous Lord references are intentionally not auto-classified here.

## Book-by-book queue

- **Matthew:** 104 candidate rows — BROTHERS / SIBLING LANGUAGE REVIEW: 14, DIVINE-REFERENT REVIEW: 2, GENERIC PRONOUN HIGH PRIORITY: 32, GENERIC PRONOUN REVIEW: 4, GENERIC-HUMAN HIGH PRIORITY: 1, MASCULINE TERM REVIEW: 26, SONS / CHILDREN LANGUAGE REVIEW: 5, UNRIPENESS LEXICAL REVIEW: 20
- **Mark:** 52 candidate rows — BROTHERS / SIBLING LANGUAGE REVIEW: 7, DIVINE-REFERENT REVIEW: 1, GENERIC PRONOUN HIGH PRIORITY: 19, GENERIC PRONOUN REVIEW: 5, MASCULINE TERM REVIEW: 15, SONS / CHILDREN LANGUAGE REVIEW: 2, UNRIPENESS LEXICAL REVIEW: 3
- **Luke:** 131 candidate rows — BROTHERS / SIBLING LANGUAGE REVIEW: 10, DIVINE-REFERENT REVIEW: 9, GENERIC PRONOUN HIGH PRIORITY: 34, GENERIC PRONOUN REVIEW: 13, GENERIC-HUMAN HIGH PRIORITY: 2, MASCULINE TERM REVIEW: 50, SONS / CHILDREN LANGUAGE REVIEW: 2, UNRIPENESS LEXICAL REVIEW: 11
- **John:** 118 candidate rows — BROTHERS / SIBLING LANGUAGE REVIEW: 6, DIVINE-REFERENT REVIEW: 15, GENERIC PRONOUN HIGH PRIORITY: 49, GENERIC PRONOUN REVIEW: 12, MASCULINE TERM REVIEW: 28, SONS / CHILDREN LANGUAGE REVIEW: 1, UNRIPENESS LEXICAL REVIEW: 7
- **Acts:** 148 candidate rows — BROTHERS / SIBLING LANGUAGE REVIEW: 8, DIVINE-REFERENT REVIEW: 15, GENERIC PRONOUN HIGH PRIORITY: 24, GENERIC PRONOUN REVIEW: 3, GENERIC-HUMAN HIGH PRIORITY: 2, MASCULINE TERM REVIEW: 88, SONS / CHILDREN LANGUAGE REVIEW: 3, UNRIPENESS LEXICAL REVIEW: 5
- **Romans:** 36 candidate rows — DIVINE-REFERENT REVIEW: 5, GENERIC PRONOUN HIGH PRIORITY: 5, GENERIC PRONOUN REVIEW: 1, MALFORMED LANGUAGE REVIEW: 3, MASCULINE TERM REVIEW: 6, STRUCTURAL VERSE MAPPING: 3, UNRIPENESS LEXICAL REVIEW: 13
- **1 Corinthians:** 16 candidate rows — BROKENNESS LEXICAL REVIEW: 1, GENERIC PRONOUN HIGH PRIORITY: 4, GENERIC-HUMAN HIGH PRIORITY: 1, MASCULINE TERM REVIEW: 7, UNRIPENESS LEXICAL REVIEW: 3
- **2 Corinthians:** 5 candidate rows — DIVINE-REFERENT REVIEW: 1, GENERIC PRONOUN HIGH PRIORITY: 1, GENERIC PRONOUN REVIEW: 1, SONS / CHILDREN LANGUAGE REVIEW: 1, UNRIPENESS LEXICAL REVIEW: 1
- **Galatians:** 3 candidate rows — GENERIC PRONOUN REVIEW: 1, SONS / CHILDREN LANGUAGE REVIEW: 1, UNRIPENESS LEXICAL REVIEW: 1
- **Ephesians:** 4 candidate rows — GENERIC PRONOUN HIGH PRIORITY: 1, UNRIPENESS LEXICAL REVIEW: 3
- **Philippians:** 4 candidate rows — DIVINE-REFERENT REVIEW: 1, GENERIC PRONOUN REVIEW: 2, UNRIPENESS LEXICAL REVIEW: 1
- **Colossians:** 3 candidate rows — GENERIC PRONOUN REVIEW: 1, UNRIPENESS LEXICAL REVIEW: 2
- **1 Thessalonians:** 2 candidate rows — UNRIPENESS LEXICAL REVIEW: 2
- **2 Thessalonians:** 4 candidate rows — DIVINE-REFERENT REVIEW: 1, GENERIC PRONOUN HIGH PRIORITY: 1, UNRIPENESS LEXICAL REVIEW: 2
- **1 Timothy:** 7 candidate rows — BROTHERS / SIBLING LANGUAGE REVIEW: 1, MASCULINE TERM REVIEW: 4, UNRIPENESS LEXICAL REVIEW: 2
- **2 Timothy:** 5 candidate rows — GENERIC PRONOUN REVIEW: 1, MASCULINE TERM REVIEW: 1, UNRIPENESS LEXICAL REVIEW: 3
- **Titus:** 4 candidate rows — MASCULINE TERM REVIEW: 2, UNRIPENESS LEXICAL REVIEW: 2
- **Philemon:** 0 candidate rows
- **Hebrews:** 23 candidate rows — DIVINE-REFERENT REVIEW: 8, GENERIC PRONOUN HIGH PRIORITY: 5, GENERIC PRONOUN REVIEW: 2, MASCULINE TERM REVIEW: 3, SONS / CHILDREN LANGUAGE REVIEW: 2, UNRIPENESS LEXICAL REVIEW: 3
- **James:** 10 candidate rows — DIVINE-REFERENT REVIEW: 3, GENERIC PRONOUN HIGH PRIORITY: 1, GENERIC PRONOUN REVIEW: 1, UNRIPENESS LEXICAL REVIEW: 5
- **1 Peter:** 14 candidate rows — GENERIC PRONOUN HIGH PRIORITY: 3, GENERIC PRONOUN REVIEW: 1, UNRIPENESS LEXICAL REVIEW: 10
- **2 Peter:** 1 candidate rows — GENERIC PRONOUN HIGH PRIORITY: 1
- **1 John:** 17 candidate rows — DIVINE-REFERENT REVIEW: 1, GENERIC PRONOUN HIGH PRIORITY: 11, UNRIPENESS LEXICAL REVIEW: 5
- **2 John:** 1 candidate rows — UNRIPENESS LEXICAL REVIEW: 1
- **3 John:** 1 candidate rows — UNRIPENESS LEXICAL REVIEW: 1
- **Jude:** 0 candidate rows
- **Revelation:** 30 candidate rows — DIVINE-REFERENT REVIEW: 8, GENERIC PRONOUN HIGH PRIORITY: 12, GENERIC PRONOUN REVIEW: 3, MASCULINE TERM REVIEW: 4, UNRIPENESS LEXICAL REVIEW: 3
