import fs from 'node:fs';
import path from 'node:path';
import { Surreal } from 'surrealdb';

const DB_URL = process.env.SURREAL_URL || 'http://127.0.0.1:8000/rpc';
const DB_NS = process.env.SURREAL_NS || 'way';
const DB_DB = process.env.SURREAL_DB || 'bible';
const DB_USER = process.env.SURREAL_USER || 'root';
const DB_PASS = process.env.SURREAL_PASS || 'root';
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../..');

const FILES = [
  'original-documents/genesis_restorative_translation.txt',
  'original-documents/exodus_to_ecclesiastes_restorative_translation.txt',
  'original-documents/rest_of_old_testament_restorative_translation.txt',
  'original-documents/matthew_restorative_translation.txt',
  'original-documents/mark_restorative_translation.txt',
  'original-documents/luke_restorative_translation.txt',
  'original-documents/john_restorative_translation.txt',
  'original-documents/acts_restorative_translation.txt',
  'original-documents/rest_of_new_testament_restorative_translation.txt'
].map((p) => path.join(ROOT, p));

const MAIN_PEOPLE = [
  'Adam','Noah','Abraham','Moses','David','Solomon','Isaiah','Jeremiah','Ezekiel','Daniel',
  'Yeshua','Peter','Kefa','Yohanan','John','Matthew','Thomas','Paul','Shaul','Miryam','Mary'
];

const THEMES = {
  vibration: [/living creative vibration/i, /vibration/i],
  word_expression: [/\bword\b/i, /\blogos\b/i, /living creative vibration/i, /utterance/i, /expression/i],
  spirit_ruach: [/\bruach\b/i, /\bspirit\b/i, /\bbreath\b/i],
  wisdom_hokmah: [/\bwisdom\b/i, /\bhokmah\b/i, /\bsophia\b/i],
  feminine_markers: [/\bwoman\b/i, /\bwomen\b/i, /\bshe\b/i, /\bher\b/i, /\bdaughter\b/i, /\bmother\b/i, /\bwisdom\b/i, /\bruach\b/i],
  turn_back: [/turn back/i, /turning back/i, /\brelent/i],
  divine_names: [/\byhwh\b/i, /\belohim\b/i, /cosmic parent/i]
};

function hashEmbedding(text, dim = 64) {
  const v = new Array(dim).fill(0);
  const tokens = text.toLowerCase().replace(/[^a-z0-9\s]/g, ' ').split(/\s+/).filter(Boolean);
  for (const t of tokens) {
    let h = 2166136261;
    for (let i = 0; i < t.length; i++) {
      h ^= t.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    v[Math.abs(h) % dim] += 1;
  }
  const norm = Math.sqrt(v.reduce((a, b) => a + b * b, 0)) || 1;
  return v.map((x) => +(x / norm).toFixed(6));
}

function parseVerses(filePath) {
  const lines = fs.readFileSync(filePath, 'utf8').split('\n');
  const verses = [];
  let book = null;
  let chapter = null;
  for (const raw of lines) {
    const line = raw.trim();
    if (!line) continue;
    const head = line.match(/^([1-3]?\s?[A-Za-z]+)\s+(\d+)$/);
    if (head) {
      book = head[1];
      chapter = Number(head[2]);
      continue;
    }
    const verse = line.match(/^(\d+)\.\s+(.*)$/);
    if (verse && book && chapter) {
      verses.push({ book, chapter, verse: Number(verse[1]), text: verse[2] });
    }
  }
  return verses;
}

function inferPeople(text) {
  const found = [];
  for (const p of MAIN_PEOPLE) {
    if (new RegExp(`\\b${p}\\b`, 'i').test(text)) found.push(p);
  }
  return [...new Set(found)];
}

function inferThemes(text) {
  const out = [];
  for (const [theme, pats] of Object.entries(THEMES)) {
    if (pats.some((r) => r.test(text))) out.push(theme);
  }
  return out;
}

function inferTermFlags(text) {
  return {
    hasYHWH: /\bYHWH\b/.test(text),
    hasElohim: /\bElohim\b/.test(text),
    hasCosmicParent: /Cosmic Parent/.test(text),
    hasLivingCreativeVibration: /Living Creative Vibration/.test(text),
    hasRuachOrSpirit: /\bRuach\b|\bSpirit\b|\bbreath\b/i.test(text),
    hasWisdom: /\bWisdom\b/i.test(text)
  };
}

async function main() {
  const db = new Surreal();
  await db.connect(DB_URL);
  await db.signin({ username: DB_USER, password: DB_PASS });
  await db.use({ namespace: DB_NS, database: DB_DB });

  for (const stmt of [
    'REMOVE TABLE mentions;',
    'REMOVE TABLE person;',
    'REMOVE TABLE verse;'
  ]) {
    try { await db.query(stmt); } catch {}
  }

  await db.query(`
    DEFINE TABLE verse SCHEMAFULL;
    DEFINE FIELD ref ON TABLE verse TYPE string;
    DEFINE FIELD book ON TABLE verse TYPE string;
    DEFINE FIELD chapter ON TABLE verse TYPE int;
    DEFINE FIELD verse ON TABLE verse TYPE int;
    DEFINE FIELD text ON TABLE verse TYPE string;
    DEFINE FIELD corpus ON TABLE verse TYPE string;
    DEFINE FIELD t_order ON TABLE verse TYPE int;
    DEFINE FIELD embedding ON TABLE verse TYPE array<float>;
    DEFINE FIELD people ON TABLE verse TYPE array<string>;
    DEFINE FIELD themes ON TABLE verse TYPE array<string>;
    DEFINE FIELD hasYHWH ON TABLE verse TYPE bool;
    DEFINE FIELD hasElohim ON TABLE verse TYPE bool;
    DEFINE FIELD hasCosmicParent ON TABLE verse TYPE bool;
    DEFINE FIELD hasLivingCreativeVibration ON TABLE verse TYPE bool;
    DEFINE FIELD hasRuachOrSpirit ON TABLE verse TYPE bool;
    DEFINE FIELD hasWisdom ON TABLE verse TYPE bool;
    DEFINE INDEX verse_ref ON TABLE verse COLUMNS ref;
    DEFINE INDEX verse_vec ON TABLE verse FIELDS embedding HNSW DIMENSION 64 DIST COSINE TYPE F32;

    DEFINE TABLE person SCHEMAFULL;
    DEFINE FIELD name ON TABLE person TYPE string;
    DEFINE INDEX person_name_unique ON TABLE person COLUMNS name UNIQUE;

    DEFINE TABLE mentions TYPE RELATION IN person OUT verse;
  `);

  let total = 0;
  const themeCounts = {};

  for (const fp of FILES) {
    const corpus = fp.includes('new_testament') || /matthew|mark|luke|john|acts/.test(fp) ? 'NT' : 'OT';
    const verses = parseVerses(fp);
    for (const v of verses) {
      const ref = `${v.book} ${v.chapter}:${v.verse}`;
      const tOrder = (corpus === 'OT' ? 1 : 2) * 10_000_000 + v.chapter * 100 + v.verse;
      const embedding = hashEmbedding(v.text);
      const people = inferPeople(v.text);
      const themes = inferThemes(v.text);
      const flags = inferTermFlags(v.text);

      for (const t of themes) themeCounts[t] = (themeCounts[t] || 0) + 1;

      const vid = `${v.book.replace(/\s+/g, '_')}_${v.chapter}_${v.verse}_${total}`;
      await db.query('UPSERT verse:`'+vid+'` CONTENT $data;', {
        data: { ref, ...v, corpus, t_order: tOrder, embedding, people, themes, ...flags }
      });

      for (const person of people) {
        await db.query('UPSERT person:`'+person+'` CONTENT { name: $name };', { name: person });
        await db.query('RELATE person:`'+person+'`->mentions->verse:`'+vid+'`;');
      }

      total++;
      if (total % 2000 === 0) console.log('indexed', total);
    }
  }

  fs.mkdirSync(path.join(ROOT, 'change-logs/new-testament/reports'), { recursive: true });
  fs.writeFileSync(
    path.join(ROOT, 'change-logs/new-testament/reports/SURREAL-INDEX-SUMMARY-LATEST.json'),
    JSON.stringify({ totalVerses: total, themeCounts }, null, 2)
  );

  console.log('Indexed verses:', total);
  console.log('Themes:', themeCounts);
  await db.close();
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
