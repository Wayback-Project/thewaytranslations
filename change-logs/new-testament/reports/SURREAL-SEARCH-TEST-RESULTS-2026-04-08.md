# Surreal Search Test Results (2026-04-08)

## Environment
- Host: Ubuntu
- SurrealDB: 2.3.10
- Node: v22.x
- Repo: Wayback-Project/thewaytranslations

## Setup test

### Install
- SurrealDB binary installed locally at `~/.local/bin/surreal`.

### Start
- Local DB started with file-backed storage:
  - `file:.surreal/way.db`

### Ingest
- Command: `npm --prefix tools/surreal-search run ingest`
- Result: indexed **30,980 verses**

## Query tests

### Index summary snapshot
- Total verses indexed: 30,980
- Theme counts from ingest summary:
  - divine_names: 8,314
  - spirit_ruach: 590
  - word_expression: 702
  - wisdom_hokmah: 214
  - turn_back: 101
  - vibration: 5


### Test A — exact lexical sample: Elohim
- Command: `npm --prefix tools/surreal-search run demo`
- Result: returned 50 Elohim verses (sample output shown in terminal).

### Test B — exact lexical sample: YHWH but not Elohim
- Command: `npm --prefix tools/surreal-search run demo`
- Result: returned 20 sample verses.

### Test C — person/entity sample: Peter/Kefa
- Command: `npm --prefix tools/surreal-search run demo`
- Result: returned sample references where Peter/Kefa appears.

### Test D — intent-style query
- Command: `npm --prefix tools/surreal-search run query -- "who was the disciple who denied and wept"`
- Result: returned ranked verse list with score breakdown (`score`, `lex`, `sem`).

## Key learnings

1. Surreal SDK query response can be nested arrays; scripts must normalize output shape.
2. SurrealQL string negation works as `!string::contains(...)`, not `NOT CONTAINS`.
3. Pure cheap embeddings were weak for intent quality; hybrid lexical+semantic reranking performs better for this demo setup.
4. Keeping refs/snippets in output is essential for transparent verification.

## Additional tests after people/theme expansion

### Test E — feminine marker theme
- Command: `npm --prefix tools/surreal-search run lookup -- theme feminine_markers`
- Result: 50 rows returned immediately (sample includes women/feminine references and wisdom-adjacent lines).

### Test F — major people lookup (Solomon)
- Command: `npm --prefix tools/surreal-search run lookup -- person Solomon`
- Result: 50 rows returned (highly usable for rapid narrative location).

### Test G — vibration lookup
- Command: `npm --prefix tools/surreal-search run lookup -- term vibration`
- Result: 5 rows returned (John 1:1-4, 1:14), confirming term-specific indexing.

## Next improvements

1. Swap hash embeddings with model embeddings for better semantic relevance.
2. Expand entity extraction to full canonical person list + alias map.
3. Add benchmark script for latency + top-k relevance scoring against a fixed query set.
4. Add dedicated feminine-force curated index (manual verified subset) for higher precision audience demos.
