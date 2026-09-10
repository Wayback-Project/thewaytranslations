import { Surreal } from 'surrealdb';

const mode = process.argv[2] || 'term';
const value = process.argv.slice(3).join(' ').trim();

if (!value) {
  console.log('Usage: npm --prefix tools/surreal-search run lookup -- <term|person|theme> <value>');
  process.exit(1);
}

const db = new Surreal();
await db.connect(process.env.SURREAL_URL || 'http://127.0.0.1:8000/rpc');
await db.signin({ username: process.env.SURREAL_USER || 'root', password: process.env.SURREAL_PASS || 'root' });
await db.use({ namespace: process.env.SURREAL_NS || 'way', database: process.env.SURREAL_DB || 'bible' });

const unwrap = (r) => (Array.isArray(r?.[0]) ? r[0] : (r?.[0]?.result || []));
let rows = [];

if (mode === 'person') {
  rows = unwrap(await db.query('SELECT ref,text FROM verse WHERE people CONTAINS $p LIMIT 50;', { p: value }));
} else if (mode === 'theme') {
  rows = unwrap(await db.query('SELECT ref,text FROM verse WHERE themes CONTAINS $t LIMIT 50;', { t: value }));
} else {
  const term = value.toLowerCase();
  const queryMap = {
    'elohim': 'SELECT ref,text FROM verse WHERE hasElohim = true LIMIT 50;',
    'yhwh': 'SELECT ref,text FROM verse WHERE hasYHWH = true LIMIT 50;',
    'cosmic-parent': 'SELECT ref,text FROM verse WHERE hasCosmicParent = true LIMIT 50;',
    'vibration': 'SELECT ref,text FROM verse WHERE hasLivingCreativeVibration = true LIMIT 50;',
    'spirit': 'SELECT ref,text FROM verse WHERE hasRuachOrSpirit = true LIMIT 50;',
    'wisdom': 'SELECT ref,text FROM verse WHERE hasWisdom = true LIMIT 50;'
  };
  if (queryMap[term]) {
    rows = unwrap(await db.query(queryMap[term]));
  } else {
    rows = unwrap(await db.query('SELECT ref,text FROM verse WHERE string::contains(string::lowercase(text), $q) LIMIT 50;', { q: term }));
  }
}

console.log(`Mode: ${mode} | Value: ${value} | Results: ${rows.length}`);
for (const r of rows.slice(0, 10)) {
  console.log(`- ${r.ref}: ${r.text}`);
}

await db.close();
