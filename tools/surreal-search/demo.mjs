import { Surreal } from 'surrealdb';
const db=new Surreal(); await db.connect(process.env.SURREAL_URL||'http://127.0.0.1:8000/rpc'); await db.signin({username:process.env.SURREAL_USER||'root',password:process.env.SURREAL_PASS||'root'}); await db.use({namespace:process.env.SURREAL_NS||'way',database:process.env.SURREAL_DB||'bible'});
const unwrap = (r) => (Array.isArray(r?.[0]) ? r[0] : (r?.[0]?.result || []));

const e=unwrap(await db.query('SELECT ref,text FROM verse WHERE string::contains(text, "Elohim") LIMIT 50;'));
console.log('Elohim verses:',e.length); console.log(e.slice(0,5).map(v=>`- ${v.ref}: ${v.text}`).join('\n'));

const y=unwrap(await db.query('SELECT ref,text FROM verse WHERE string::contains(text, "YHWH") AND !string::contains(text, "Elohim") LIMIT 20;'));
console.log('\nYHWH-only sample:',y.length); console.log(y.slice(0,5).map(v=>`- ${v.ref}: ${v.text}`).join('\n'));

const p=unwrap(await db.query('SELECT ref,text FROM verse WHERE string::contains(text, "Peter") OR string::contains(text, "Kefa") LIMIT 20;'));
console.log('\nPeter/Kefa mention sample:',p.length); console.log(p.slice(0,5).map(v=>`- ${v.ref}: ${v.text}`).join('\n'));

await db.close();
