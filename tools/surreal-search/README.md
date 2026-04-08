# SurrealDB Search (Graph + Vector + Temporal)

This stack gives fast, explainable search over a large corpus without re-reading whole files each time.

## Problem it solves

- Find 50+ exact matches quickly (e.g., `Elohim`, `YHWH`)
- Support intent-style lookup (e.g., "who was the disciple who denied?")
- Keep results transparent with verse references and snippets

## How SurrealDB is used here

- **Graph:** person/entity-style links can be attached to verses
- **Vector:** each verse stores an embedding for similarity search
- **Temporal:** `t_order` provides ordering for chronology-aware queries

## Quick start (Ubuntu, local-first)

### 1) Install SurrealDB binary

```bash
mkdir -p ~/.local/bin
curl -fL https://github.com/surrealdb/surrealdb/releases/download/v2.3.10/surreal-v2.3.10.linux-amd64.tgz -o /tmp/surreal.tgz
tar -xzf /tmp/surreal.tgz -C /tmp
install -m 755 /tmp/surreal ~/.local/bin/surreal
~/.local/bin/surreal version
```

### 2) Start database

From repo root:

```bash
~/.local/bin/surreal start --user root --pass root --bind 127.0.0.1:8000 file:.surreal/way.db
```

### 3) Install scripts + ingest

```bash
npm --prefix tools/surreal-search install
npm --prefix tools/surreal-search run ingest
```

### 3.5) Connection/config keys (where they live)

- Example config file: `tools/surreal-search/.env.example`
- Variables used by scripts:
  - `SURREAL_URL`
  - `SURREAL_NS`
  - `SURREAL_DB`
  - `SURREAL_USER`
  - `SURREAL_PASS`

You can export these in your shell or load via your preferred env loader.

### 4) Run examples

```bash
npm --prefix tools/surreal-search run demo
npm --prefix tools/surreal-search run query -- "who was the disciple who denied and wept"
npm --prefix tools/surreal-search run lookup -- term elohim
npm --prefix tools/surreal-search run lookup -- person Noah
npm --prefix tools/surreal-search run lookup -- person Solomon
npm --prefix tools/surreal-search run lookup -- theme wisdom_hokmah
npm --prefix tools/surreal-search run lookup -- theme feminine_markers
npm --prefix tools/surreal-search run lookup -- term vibration
```

## OpenClaw instructions

Use these commands via OpenClaw `exec` in repo root:

1. Start DB server:
- `~/.local/bin/surreal start --user root --pass root --bind 127.0.0.1:8000 file:.surreal/way.db`

2. Ingest corpus:
- `npm --prefix tools/surreal-search run ingest`

3. Query:
- `npm --prefix tools/surreal-search run query -- "<question>"`

4. Demo pack:
- `npm --prefix tools/surreal-search run demo`

5. Fast exact lookup (term/person/theme):
- `npm --prefix tools/surreal-search run lookup -- term elohim`
- `npm --prefix tools/surreal-search run lookup -- person Adam`
- `npm --prefix tools/surreal-search run lookup -- theme spirit_ruach`

## Data model (current)

- `verse`: `ref`, `book`, `chapter`, `verse`, `text`, `corpus`, `t_order`, `embedding`
- extra fields on `verse`: `people`, `themes`, and boolean term flags (`hasYHWH`, `hasElohim`, `hasCosmicParent`, `hasLivingCreativeVibration`, `hasRuachOrSpirit`, `hasWisdom`)
- `person`: entity records (main biblical figures seeded during ingest)
- `mentions`: relation table for entity-to-verse links

## Test results (current run)

- Ingested verses: **30,980**
- Index summary file: `change-logs/new-testament/reports/SURREAL-INDEX-SUMMARY-LATEST.json`
- Includes theme counts for divine names, spirit/ruach, wisdom, vibration, turn-back, and feminine markers.
- Demo tests passed:
  - 50 Elohim verses returned quickly
  - 20 YHWH-only sample verses returned
  - Peter/Kefa sample references returned
- Query test:
  - Intent query returns top ranked references with lexical+semantic blended scoring

## What we got wrong and learned

1. **Result shape:** Surreal SDK query results may be nested arrays; scripts must unwrap correctly.
2. **SurrealQL syntax:** `NOT CONTAINS` failed; `!string::contains(...)` worked.
3. **Vector query syntax:** first knn operator use with parameterized vector was wrong; switched to stable similarity function + hybrid rerank.
4. **Search quality:** cheap local embeddings alone were weak; hybrid lexical+vector ranking gave better practical results.

## For other knowledgebases

This pattern is reusable:
1. Replace parser in `ingest.mjs` with your corpus parser.
2. Keep `ref`, `text`, `time/order`, `embedding`, and optional entity links.
3. Reuse `query.mjs`/`demo.mjs` as baseline.
