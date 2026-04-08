---
name: openclaw-surreal-search
description: SurrealDB graph+vector+temporal search workflow for Wayback Project (adaptable to any large knowledgebase).
---

# OpenClaw Skill: Surreal Search Workflow

Use this skill when asked to:
- set up SurrealDB locally
- ingest corpus files for fast search
- run intent/semantic-like lookup with graph context
- answer "who did X, where?" questions quickly

This skill is built for `Wayback-Project/thewaytranslations` but is intentionally reusable for any large text corpus.

## What problem this solves

Without an index, assistants repeatedly scan large files.
With this workflow, assistants can:
1) run exact lexical queries fast
2) run hybrid intent queries quickly
3) return references with transparent provenance

## Repo paths this skill expects

- `tools/surreal-search/` (scripts + README)
- `original-documents/` (source corpus)
- `change-logs/` (results and audit notes)
- `editor-notes/` (reflection/proposed-rules/research records)

## Install + run

1. Start SurrealDB server locally
2. Run ingest script
3. Run demo/query scripts

(Commands are in `tools/surreal-search/README.md`.)

## OpenClaw usage pattern

When user asks a search question:
1. ensure SurrealDB is running
2. run query script with user question
3. return top matches with refs + snippets
4. if confidence low, run exact keyword fallback query and say so

## Discussion and issue format (for transparent collaboration)

For search architecture changes, open issues with:
- **Problem:** what query is currently hard/slow
- **Proposal:** schema/query/script update
- **Expected impact:** speed/quality/explainability
- **Test query set:** 3-5 real questions
- **Before/after results:** top references and runtime notes

Recommended labels:
- `search-index`
- `graph`
- `vector`
- `temporal`
- `openclaw-skill`

## What went wrong before (to help future bots)

1. Surreal JS SDK returns query results as nested arrays; scripts must unwrap correctly.
2. `NOT CONTAINS` syntax was wrong in SurrealQL; use `!string::contains(...)`.
3. Initial vector query operator usage was incorrect with parameters; fallback to explicit similarity function worked reliably.
4. Demo quality with cheap local embeddings is limited; hybrid lexical+vector rerank improves practical results.

## Adapt this to any knowledgebase

Replace parser in ingest script:
- parse your docs into chunks
- store `ref`, `text`, optional `source_path`, `time`, `entity` fields
- compute embeddings (local or API)
- add graph edges between entities and chunks

The rest of the querying approach remains the same.
