#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "audit-output" / "masculine-inventory-2026-09-14"
CANDIDATES = AUDIT / "candidates.tsv"
SUMMARY = AUDIT / "summary.json"
OUT = AUDIT / "Masculine-update-Bible-with-Original-Names.html"

TITLE = "Masculine update Bible with Original Names"
CANONICAL_SHA = "bfd2e746afdb810d4b0b35abf66fe71da394abee77099f9c8f481102ab242f53"

DIVINE_MARKERS = re.compile(r"\b(YHWH|Elohim|God|Yah|Most High|Holy One)\b", re.I)
MASC_PRONOUN = re.compile(r"\b(he|him|his|himself)\b", re.I)
GENERIC_NEUTRAL_CUES = re.compile(r"\b(person|people|humanity|human beings?|mortals?|someone|anyone|everyone|whoever|the one|one who|child|children|they|them|their|theirs)\b", re.I)
GENERIC_MASC = re.compile(r"\b(man|men|mankind|[a-z]+man|[a-z]+men)\b", re.I)
MALE_SPECIFIC = re.compile(r"\b(husband|father|son|brother|king|prince|bridegroom|male|Shlomo|Dawid|Lemuel|Yosef|Aharon|Pharaoh)\b", re.I)

# Already-established source/methodology decisions or internally undeniable consistency defects.
# These are examples, not the only rows that may be approved in the release ledger.
CONFIRMED = {
    "Proverbs 8:4": ("Generic-human source wording", "Replace the male-coded audience with broad humanity. Suggested direction: ‘To you, people, I call; my voice is to all humanity / all mortals.’ Hebrew אִישִׁים + בְּנֵי אָדָם is not a men-only audience here."),
    "Psalm 8:4": ("Generic-human source wording", "Keep the already-restored ‘child of humanity’ idea and make the whole human-reference chain inclusive; do not switch back to singular male pronouns in vv. 5–6."),
    "Psalm 8:5": ("Pronoun-chain consistency", "Continue the plural/inclusive human referent from v. 4: use them/their rather than him/his."),
    "Psalm 8:6": ("Pronoun-chain consistency", "Continue the plural/inclusive human referent from v. 4: use them/their rather than him/his."),
    "Psalm 119:9": ("Pronoun-chain consistency", "Current ‘young person’ must agree with the following pronoun. If ‘young person’ is retained, use ‘their way,’ not ‘his way.’"),
    "Psalm 144:3": ("Generic-human source wording", "The verse already uses ‘child of humanity’ and ‘them’; align ‘man’ with that inclusive human sense."),
    "Psalm 144:4": ("Pronoun-chain consistency", "Current ‘A person … His days’ is internally inconsistent. Use a consistent person/they chain."),
    "Proverbs 9:8": ("Pronoun-chain consistency", "Current verse mixes a generic scoffer with ‘he’ and a ‘wise person’ with ‘they.’ Use one consistent generic-human strategy."),
    "Proverbs 11:17": ("Pronoun-chain consistency", "Current ‘merciful man … their own soul’ is internally mixed. Prefer a fully generic person/one construction."),
    "Proverbs 12:2": ("Pronoun-chain consistency", "Current ‘A good man … they … a person’ is internally mixed. Make the first subject generic as well."),
    "Proverbs 17:28": ("Pronoun-chain consistency", "Current ‘a fool, when they … When he …’ needs one consistent generic pronoun chain."),
    "Proverbs 18:20": ("Pronoun-chain consistency", "Current ‘A person … their mouth … his lips … he’ is a direct consistency defect. Keep the whole proverb gender-inclusive."),
    "Proverbs 19:11": ("Pronoun-chain consistency", "Current ‘a person … them … his glory’ is internally inconsistent. Keep the generic referent consistent."),
    "Proverbs 21:29": ("Pronoun-chain consistency", "Current verse mixes ‘person/their’ and ‘upright/he/his.’ Use a consistent generic-human construction."),
    "Proverbs 22:29": ("Pronoun-chain consistency", "Current ‘a person skilled in their work? He … He … obscure men’ is internally inconsistent. Use a consistent generic-human chain; ‘people of no standing’/similar can replace ‘obscure men’ if source review supports it."),
    "Proverbs 24:5": ("Pronoun-chain consistency", "Current ‘A wise person … a knowledgeable man’ should use the same inclusive strategy for both parallel subjects."),
    "Proverbs 28:11": ("Pronoun-chain consistency", "Current ‘The rich a person … their own eyes … sees through him’ contains both a grammar artifact and a mixed generic pronoun chain; repair before release."),
    "Proverbs 28:24": ("Pronoun-chain consistency", "Current ‘Whoever … their father … He is’ should remain generic throughout."),
    "Proverbs 29:23": ("Pronoun-chain consistency", "Current ‘A person’s pride brings him low’ should agree with the generic noun phrase."),
    "Proverbs 29:24": ("Pronoun-chain consistency", "Current ‘Whoever … their own soul. He takes an oath …’ should remain generic throughout."),
    "Proverbs 30:2": ("Pronoun-chain consistency", "Current ‘ignorant man’ paired with ‘a person’s understanding’ is internally inconsistent; choose one source-appropriate generic strategy."),
    "Song of Solomon 3:3": ("Occupational language review", "Review ‘watchmen’ against שֹׁמְרִים. If sex is not narratively important, ‘guards’/‘watchers’ avoids unnecessary male-only English while preserving the city-watch role."),
    "Song of Solomon 5:7": ("Occupational language review", "Same city-watch issue as 3:3; consider ‘guards’/‘watchers’ if the source does not require male identity."),
    "Song of Solomon 7:1": ("Occupational language update", "‘Skillful workman’ is unnecessary male-coded occupational English. Suggested direction: ‘a skilled artisan/craftsperson,’ subject to final lexical check."),
}

# Existing repository policy says Psalm 110:5–7 is disputed and must not be mechanically resolved.
LOCKED_REVIEW = {"Psalm 110:5", "Psalm 110:6", "Psalm 110:7"}


def h(s):
    return html.escape(str(s), quote=True)


def classify(row):
    ref = row["reference"]
    text = row["text"]
    triggers = row["triggers"].lower()
    book = ref.split()[0]

    if ref in LOCKED_REVIEW:
        return "EDITORIAL REVIEW", "Known disputed royal/Messianic/divine referent. Preserve current wording until a dedicated source/textual decision; do not change mechanically."
    if ref in CONFIRMED:
        kind, action = CONFIRMED[ref]
        return "CONFIRMED UPDATE", f"{kind}. {action}"
    if ref.startswith("Song of Solomon"):
        if "watchmen" in triggers or "workman" in triggers or " men" in f" {triggers}":
            return "SOURCE REVIEW", "Potentially unnecessary male-coded occupational/group English. Check the Hebrew lexeme and narrative role; prefer role-based wording if sex is not semantically important."
        return "KEEP MASCULINE", "Male lover, named male, kinship, royal, or other sex-specific imagery appears intentional in Song of Songs. Preserve unless source review shows the English added maleness not present in the Hebrew."

    has_divine = bool(DIVINE_MARKERS.search(text))
    has_pron = bool(MASC_PRONOUN.search(text))
    has_neutral = bool(GENERIC_NEUTRAL_CUES.search(text))
    has_generic_masc = bool(GENERIC_MASC.search(text))
    has_male_specific = bool(MALE_SPECIFIC.search(text))

    if has_neutral and has_pron:
        return "HIGH-PRIORITY UPDATE", "Generic/inclusive wording and masculine singular pronouns occur in the same verse. Resolve the entire antecedent chain consistently after checking that the pronoun is not a different, specifically male referent."
    if has_divine and has_pron:
        return "DIVINE-REFERENT REVIEW", "Apply the established divine-pronoun policy: where the antecedent is unmistakably YHWH/Elohim/God, repeat the established divine name/title instead of he/him/his. If the pronoun is human or the poetic referent is uncertain, retain it."
    if has_generic_masc and not has_male_specific:
        return "GENERIC-HUMAN REVIEW", "The current English uses man/men or a masculine compound without an obvious sex-specific marker. Check אדם/אנוש/איש/גבר and context; change to person/people/humanity/mortals or a role noun when the source is generic."
    if has_male_specific and not has_generic_masc:
        return "LIKELY KEEP", "Male-specific kinship/title/role is present. Preserve unless source review shows that the English is more male-specific than the Hebrew."
    if has_generic_masc and has_male_specific:
        return "SOURCE REVIEW", "The verse contains both generic-looking and male-specific language. Review each referent separately; do not neutralize the whole verse mechanically."
    if has_pron:
        return "PRONOUN REVIEW", "Trace the antecedent across the sentence/parallel line. Use singular they/recasing for generic humans; repeat YHWH/Elohim for unmistakably divine referents; preserve specifically male referents."
    return "SOURCE REVIEW", "Review the Hebrew lexeme and immediate poetic context."


def example_rewrite(ref, text):
    examples = {
        "Proverbs 8:4": "Suggested: “To you, people, I call! I send my voice to all humanity.” (Final wording should follow the chosen lexical register.)",
        "Psalm 8:4": "Suggested direction: “what are human beings, that you think of them? What are the children of humanity, that you care for them?”",
        "Psalm 8:5": "Suggested direction: “For you have made them a little lower than Elohim, and crowned them with glory and honor.”",
        "Psalm 8:6": "Suggested direction: “You make them rulers over the works of your hands. You have put all things under their feet.”",
        "Psalm 119:9": "Suggested: “How can a young person keep their way pure? By living according to your word.”",
        "Psalm 144:4": "Suggested: “A person is like a breath. Their days are like a shadow that passes away.”",
        "Proverbs 9:8": "Suggested direction: “Don’t reprove a scoffer, lest they hate you. Reprove a wise person, and they will love you.”",
        "Proverbs 18:20": "Suggested direction: “A person’s stomach is filled with the fruit of their mouth. With the harvest of their lips they are satisfied.”",
        "Proverbs 29:24": "Suggested direction: “Whoever is an accomplice of a thief is an enemy of their own soul. They take an oath, but dare not testify.”",
        "Song of Solomon 7:1": "Suggested direction: “…the work of the hands of a skilled artisan.”",
    }
    return examples.get(ref, "")


def main():
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    if summary["canonicalEpubSha256"] != CANONICAL_SHA:
        raise SystemExit("Unexpected canonical SHA")
    with CANDIDATES.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    for r in rows:
        r["classification"], r["recommendation"] = classify(r)

    counts = Counter(r["classification"] for r in rows)
    by_book = defaultdict(list)
    for r in rows:
        if r["reference"].startswith("Song of Solomon"):
            by_book["Song of Songs (Song of Solomon in current data)"].append(r)
        else:
            by_book[r["reference"].split()[0]].append(r)

    css = """
    body{font-family:Arial,sans-serif;line-height:1.38;color:#202124;max-width:980px;margin:0 auto;padding:28px}
    h1{font-size:28px;margin-bottom:4px} h2{font-size:21px;margin-top:30px;border-bottom:1px solid #dadce0;padding-bottom:5px}
    h3{font-size:17px;margin-top:24px}.muted{color:#5f6368}.callout{background:#f8f9fa;border-left:4px solid #5f6368;padding:10px 14px;margin:14px 0}
    table{border-collapse:collapse;width:100%;font-size:10.5pt;margin:10px 0 22px}th,td{border:1px solid #dadce0;padding:6px;vertical-align:top}th{background:#f1f3f4;text-align:left}
    .confirmed{font-weight:700}.small{font-size:9.5pt}.ref{white-space:nowrap;font-weight:700}.pagebreak{page-break-before:always}
    ul{margin-top:5px}.status{font-weight:700}.quote{font-style:italic}.mono{font-family:monospace;font-size:9pt}
    """

    out = []
    out.append(f"<!doctype html><html><head><meta charset='utf-8'><title>{h(TITLE)}</title><style>{css}</style></head><body>")
    out.append(f"<h1>{h(TITLE)}</h1>")
    out.append("<p class='muted'><strong>Editorial inventory — Psalms, Proverbs, and Song of Songs</strong><br>Prepared from the current canonical EPUB for print/text and synchronized digital release planning.</p>")
    out.append("<div class='callout'><strong>Status:</strong> Diagnostic/editorial inventory only. This document does not itself authorize or apply Scripture changes. The exact approved before/after ledger must be finalized before the canonical EPUB is edited.</div>")

    out.append("<h2>1. Canonical baseline and scope</h2>")
    out.append(f"<p>Canonical EPUB SHA-256: <span class='mono'>{CANONICAL_SHA}</span>. The audit parsed all <strong>{summary['extractedVerseCount']:,}</strong> verses in the three-book scope and mechanically flagged <strong>{summary['candidateVerseCount']:,}</strong> verses for editorial review.</p>")
    out.append("<table><tr><th>Book</th><th>Chapters</th><th>Verses parsed</th><th>Candidate verses</th></tr>")
    for book, c in summary["counts"].items():
        out.append(f"<tr><td>{h(book)}</td><td>{c['chapters']}</td><td>{c['verses']}</td><td>{c['candidateVerses']}</td></tr>")
    out.append("</table>")
    out.append("<p>A candidate is not automatically a change. The broad scan intentionally catches actual male persons, kings, husbands, fathers, sons, brothers, the male beloved in Song of Songs, and ambiguous poetic references so they can be explicitly preserved rather than accidentally neutralized.</p>")

    out.append("<h2>2. Governing Way Version methodology</h2>")
    out.append("<ul>"
               "<li>Begin with the Hebrew/Aramaic source and literary context; do not inherit male-only English merely because a traditional English translation used it.</li>"
               "<li>Preserve meaningful grammatical gender and actual sex-specific identity. Inclusive language is not a license to erase real sons, husbands, fathers, kings, male lovers, or deliberately gendered imagery.</li>"
               "<li>Human references that are not gender-specific in the source should not be narrowed to men in English.</li>"
               "<li>Preserve ambiguity where the Hebrew preserves ambiguity; disputed poetic/Messianic speaker transitions are not mechanically resolved.</li>"
               "<li>For an unmistakably divine antecedent, the established project rule is to repeat the divine name/title (YHWH, Elohim, God, etc.) rather than use he/him/his. Do not replace a divine referent with singular they, she, or it under this consistency rule.</li>"
               "<li>Downstream web/mobile reader Scripture is generated from the approved canonical EPUB and must not be hand-edited independently.</li>"
               "</ul>")

    out.append("<h2>3. Hebrew decision guide for this pass</h2>")
    out.append("<table><tr><th>Source form</th><th>Editorial handling</th></tr>"
               "<tr><td><strong>אָדָם (adam)</strong></td><td>Often human/humankind/person. Do not default to modern male-only ‘man’ when the referent is humanity generally.</td></tr>"
               "<tr><td><strong>אֱנוֹשׁ (enosh)</strong></td><td>Human/mortal. Often well served by ‘mortal,’ ‘human being,’ or a context-appropriate generic expression.</td></tr>"
               "<tr><td><strong>בְּנֵי אָדָם (bene adam)</strong></td><td>Literally ‘children/sons of humanity’; in generic address, ‘human beings,’ ‘people,’ ‘mortals,’ or ‘children of humanity’ can preserve the sense without a men-only implication.</td></tr>"
               "<tr><td><strong>אִישׁ (ish)</strong></td><td>Can mean man, person, individual, husband, or each/one depending context. Do not neutralize automatically; do not masculinize automatically.</td></tr>"
               "<tr><td><strong>גֶּבֶר (gever)</strong></td><td>More strongly male-marked. Usually preserve male force unless the literary construction clearly functions generically.</td></tr>"
               "<tr><td><strong>בֵּן (ben)</strong></td><td>Son/descendant. Preserve actual kinship and male identity; generic wisdom-address uses require contextual review rather than blind substitution.</td></tr>"
               "<tr><td><strong>חָכְמָה (hokhmah, Wisdom)</strong></td><td>Feminine personification in Proverbs. Preserve Wisdom’s feminine presentation; do not confuse her ‘I/she’ voice with YHWH’s referent in adjacent creation language.</td></tr>"
               "</table>")

    out.append("<h2>4. Decision classes used in this inventory</h2>")
    out.append("<table><tr><th>Class</th><th>Meaning</th></tr>")
    desc = {
        "CONFIRMED UPDATE":"High-confidence source/methodology decision or undeniable internal consistency defect; expected to enter the approved change ledger.",
        "HIGH-PRIORITY UPDATE":"The current verse already uses inclusive/generic wording but falls back to he/him/his; very likely a consistency repair after antecedent check.",
        "GENERIC-HUMAN REVIEW":"Man/men or a masculine compound appears generic; source lexeme/context must confirm final inclusive wording.",
        "DIVINE-REFERENT REVIEW":"A divine marker and masculine pronoun co-occur; trace the antecedent and apply the established divine-name repetition rule only where unmistakably divine.",
        "PRONOUN REVIEW":"Masculine pronoun needs antecedent tracing; may be generic human, divine, or truly male.",
        "LIKELY KEEP":"Male-specific kinship/title/role is likely intentional and should be preserved.",
        "KEEP MASCULINE":"Song-of-Songs male lover/named male/sex-specific imagery; preserve unless source evidence says otherwise.",
        "EDITORIAL REVIEW":"Known disputed or poetically ambiguous referent; no mechanical change.",
        "SOURCE REVIEW":"Mixed or uncertain case requiring lexical/context review.",
    }
    for k in ["CONFIRMED UPDATE","HIGH-PRIORITY UPDATE","GENERIC-HUMAN REVIEW","DIVINE-REFERENT REVIEW","PRONOUN REVIEW","LIKELY KEEP","KEEP MASCULINE","EDITORIAL REVIEW","SOURCE REVIEW"]:
        out.append(f"<tr><td><strong>{h(k)}</strong></td><td>{h(desc[k])}</td></tr>")
    out.append("</table>")

    out.append("<h2>5. Current audit classification summary</h2><table><tr><th>Class</th><th>Rows</th></tr>")
    for k,n in sorted(counts.items(), key=lambda x:(-x[1],x[0])):
        out.append(f"<tr><td>{h(k)}</td><td>{n}</td></tr>")
    out.append("</table>")

    out.append("<h2>6. High-confidence examples for the upcoming update</h2>")
    out.append("<p>These examples show the kinds of repairs that should drive the final approved ledger. Suggested wording is directional until the source-language review is signed off.</p>")
    for ref in ["Proverbs 8:4","Psalm 8:4","Psalm 8:5","Psalm 8:6","Psalm 119:9","Psalm 144:4","Proverbs 9:8","Proverbs 18:20","Proverbs 29:24","Song of Solomon 7:1"]:
        row = next((r for r in rows if r["reference"] == ref), None)
        if not row: continue
        out.append(f"<h3>{h(ref)}</h3><p><strong>Current:</strong> {h(row['text'])}</p><p><strong>Recommended direction:</strong> {h(example_rewrite(ref,row['text']))}</p>")

    out.append("<h2>7. Proverbs 8: speaker/referent handling</h2>")
    out.append("<p>Proverbs 8 must distinguish two simultaneous features: <strong>Wisdom is personified as feminine</strong>, while <strong>YHWH is the divine referent</strong> in the creation sequence. The audience in v. 4 is broad humanity, not males only. Therefore:</p>"
               "<ul><li>v. 4: remove the men-only address.</li><li>Wisdom’s she/I voice remains feminine.</li><li>vv. 22–31: when a masculine English pronoun unmistakably points back to YHWH, use the established divine name/title instead of leaving ‘he/his/him’ ambiguous.</li><li>Do not convert Wisdom to a masculine divine speaker and do not merge Wisdom and YHWH into one referent by accident.</li></ul>")

    out.append("<h2>8. Psalms: special cautions</h2>")
    out.append("<ul><li>Generic humanity formulas such as adam/enosh/bene adam often need people/humanity/mortals or a plural they-chain rather than man + he/him/his.</li>"
               "<li>Royal psalms, named male speakers, and Messianic/royal poetry are not automatically neutralized.</li>"
               "<li>Psalm 110:5–7 remains a documented disputed referent and is explicitly held for editorial review.</li>"
               "<li>When a psalm directly names YHWH/Elohim and the next he/him/his clearly refers to YHWH/Elohim, follow the existing divine-pronoun rule to prevent reader confusion.</li></ul>")

    out.append("<h2>9. Song of Songs: special cautions</h2>")
    out.append("<p>The Song is not a target for gender-neutralizing the lovers. The male beloved, Shlomo, and genuine male kinship/royal references should remain male. The meaningful review cases are mainly <strong>occupational/group labels</strong> that modern English unnecessarily encodes as male: ‘watchmen’ (3:3; 5:7) and ‘workman’ (7:1), plus any role noun whose Hebrew does not make sex material to the image. ‘Mighty men’ in 4:4 should be checked for whether ‘warriors’ better preserves the source role without adding modern male-only force.</p>")

    out.append("<h2>10. Action plan for print/text + canonical digital update</h2>")
    out.append("<ol><li>Review every row in the appendix and approve a finite before/after ledger. No global search-and-replace.</li>"
               "<li>For each proposed human-language change, record the source lexeme (adam/enosh/ish/gever/ben or other), whether the referent is generic or sex-specific, and the chosen English strategy.</li>"
               "<li>For every he/him/his near YHWH/Elohim/Wisdom, identify the antecedent explicitly. Apply the existing divine-name repetition rule only when the divine referent is unmistakable.</li>"
               "<li>Keep a separate ‘preserve male’ list so true male identity is protected from accidental neutralization.</li>"
               "<li>Apply the approved ledger to the authoritative current EPUB only after archiving the prior EPUB. Do not edit downstream reader Scripture by hand.</li>"
               "<li>Run canonical QA: ZIP/CRC and mimetype, XML parsing, internal links, 66 books, 1,189 chapters, 31,102 search-record inventory, and an exact before/after ledger check.</li>"
               "<li>Regenerate canonical mobile fallback data and SHA metadata from the finished EPUB.</li>"
               "<li>Regenerate the website/e-reader from that exact EPUB; verify website and Netlify release SHA match canonical.</li>"
               "<li>Update the native mobile release pins/feed from the verified website/canonical release; keep native Scripture updates content-only under the existing verification gates.</li>"
               "<li>Apply the same approved ledger to the print/text manuscript. The print and digital editions should be reconciled to the same verse-level decisions, not edited independently.</li>"
               "<li>Run a final editorial spot audit of Proverbs 8, Psalm 8, Psalm 110, generic wisdom proverbs, and Song-of-Songs occupational terms before release.</li></ol>")

    out.append("<h2 class='pagebreak'>Appendix A — Complete current-form candidate inventory</h2>")
    out.append("<p>This appendix is deliberately exhaustive. Rows marked KEEP/LIKELY KEEP are included because the purpose of the audit is both to find unnecessary masculinity and to protect meaningful male identity. Rows marked REVIEW must not be changed automatically.</p>")
    for book, bookrows in by_book.items():
        out.append(f"<h3>{h(book)} — {len(bookrows)} candidates</h3>")
        out.append("<table><tr><th>Reference</th><th>Current text</th><th>Class</th><th>Editorial action</th></tr>")
        for r in bookrows:
            out.append(f"<tr><td class='ref'>{h(r['reference'])}</td><td>{h(r['text'])}</td><td class='status'>{h(r['classification'])}</td><td>{h(r['recommendation'])}</td></tr>")
        out.append("</table>")

    out.append("<h2>Appendix B — Release rule to carry forward</h2>")
    out.append("<div class='callout'><strong>Do not equate grammatical masculine with male-only meaning, and do not equate inclusive English with removing real gender.</strong> The controlling question is what the Hebrew referent actually is in context. Generic humanity should sound like humanity in English; actual men should remain men; Wisdom’s feminine personification should remain visible; and unmistakable divine referents should follow the project’s established divine-name/title repetition rule.</div>")
    out.append("</body></html>")
    OUT.write_text("".join(out), encoding="utf-8")
    print(json.dumps({"output":str(OUT),"rows":len(rows),"classes":dict(counts)},indent=2))

if __name__ == "__main__":
    main()
