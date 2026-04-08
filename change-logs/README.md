# Change Logs

This folder tracks what changed, when it changed, and why.

## Layout

- `new-testament/`
  - `INDEX.md` — master NT change-log index and completion status
  - `books/` — per-book change logs (or grouped source-file logs where books are grouped)
  - `reports/` — generated local QA summaries (markdown/json)

## Rules

- Every meaningful translation or policy change must be logged with UTC timestamp.
- Include rationale for each decision, especially where Aramaic-priority and Greek-priority tracks diverge.
- Do not require any database. Logs are plain markdown + optional JSON artifacts committed to git.

## Entry template

```md
## 2026-04-08 12:00 UTC — <short change title>
- Scope:
- Change:
- Rationale:
- Source track: Aramaic-priority | Greek-priority | Dual-witness
- Impacted files:
- Reviewer status:
```
