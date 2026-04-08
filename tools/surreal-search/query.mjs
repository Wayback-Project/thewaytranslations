import { Surreal } from 'surrealdb';
const q = process.argv.slice(2).join(' ').trim();
if (!q) { console.log('Usage: npm --prefix tools/surreal-search run query -- "your question"'); process.exit(1); }

const DB_URL = process.env.SURREAL_URL || 'http://127.0.0.1:8000/rpc';
const DB_NS = process.env.SURREAL_NS || 'way';
const DB_DB = process.env.SURREAL_DB || 'bible';
const DB_USER = process.env.SURREAL_USER || 'root';
const DB_PASS = process.env.SURREAL_PASS || 'root';

function tokens(text){ return text.toLowerCase().replace(/[^a-z0-9\s]/g,' ').split(/\s+/).filter((t)=>t.length>2); }
function hashEmbedding(text, dim = 64){ const v=new Array(dim).fill(0); for(const t of tokens(text)){ let h=2166136261; for(let i=0;i<t.length;i++){ h ^= t.charCodeAt(i); h = Math.imul(h,16777619);} const j=Math.abs(h)%dim; v[j]+=1;} const norm=Math.sqrt(v.reduce((a,b)=>a+b*b,0))||1; return v.map(x=>x/norm); }
function cosine(a,b){ let dot=0,na=0,nb=0; for(let i=0;i<a.length;i++){ dot+=a[i]*b[i]; na+=a[i]*a[i]; nb+=b[i]*b[i]; } return dot/((Math.sqrt(na)*Math.sqrt(nb))||1); }

const db=new Surreal();
await db.connect(DB_URL);
await db.signin({username:DB_USER,password:DB_PASS});
await db.use({namespace:DB_NS,database:DB_DB});

const res=await db.query('SELECT ref, text, embedding, corpus FROM verse;');
const rows = Array.isArray(res?.[0]) ? res[0] : (res?.[0]?.result || []);
const qTokens = tokens(q);
const qSet = new Set(qTokens);
const qEmb = hashEmbedding(q);
const wantsDisciple = /disciple|apostle|emissary|peter|kefa|john|matthew|thomas/i.test(q);

const scored = rows.map((r)=>{
  const tSet = new Set(tokens(r.text));
  let overlap = 0;
  for (const t of qSet) if (tSet.has(t)) overlap++;
  const lex = overlap / Math.max(1, qSet.size);
  const sem = cosine(qEmb, r.embedding || hashEmbedding(r.text));

  let boost = 0;
  if (wantsDisciple && r.corpus === 'NT') boost += 0.08;
  if (wantsDisciple && /(Peter|Kefa|Yohanan|John|Matthew|Thomas|emissary|disciple)/i.test(r.text)) boost += 0.12;

  const score = lex * 0.65 + sem * 0.35 + boost;
  return { ref:r.ref, text:r.text, score, lex, sem, boost };
}).sort((a,b)=>b.score-a.score).slice(0,10);

console.log(`\nQuery: ${q}\n`);
for(const [i,r] of scored.entries()){
  console.log(`${i+1}. ${r.ref} (score ${r.score.toFixed(4)} | lex ${r.lex.toFixed(3)} | sem ${r.sem.toFixed(3)})`);
  console.log(`   ${r.text}`);
}
await db.close();
