# New Testament Change Log Index

Status: **Pass 1 initialized and completed for all NT books** (policy and tracking layer).

## Source files currently used for NT content

- `working-documents/matthew_restorative_translation.txt`
- `working-documents/mark_restorative_translation.txt`
- `working-documents/luke_restorative_translation.txt`
- `working-documents/john_restorative_translation.txt`
- `working-documents/acts_restorative_translation.txt`
- `working-documents/rest_of_new_testament_restorative_translation.txt`

## Book coverage map

| Book | Log file | Track default | Pass 1 status |
|---|---|---|---|
| Matthew | `books/Matthew.md` | Aramaic-priority | done |
| Mark | `books/Mark.md` | Aramaic-priority | done |
| Luke | `books/Luke.md` | Aramaic-priority | done |
| John | `books/John.md` | Aramaic-priority | done |
| Acts | `books/Acts.md` | Dual-witness | done |
| Romans | `books/Romans.md` | Greek-priority acknowledged | done |
| 1 Corinthians | `books/1-Corinthians.md` | Greek-priority acknowledged | done |
| 2 Corinthians | `books/2-Corinthians.md` | Greek-priority acknowledged | done |
| Galatians | `books/Galatians.md` | Greek-priority acknowledged | done |
| Ephesians | `books/Ephesians.md` | Greek-priority acknowledged | done |
| Philippians | `books/Philippians.md` | Greek-priority acknowledged | done |
| Colossians | `books/Colossians.md` | Greek-priority acknowledged | done |
| 1 Thessalonians | `books/1-Thessalonians.md` | Greek-priority acknowledged | done |
| 2 Thessalonians | `books/2-Thessalonians.md` | Greek-priority acknowledged | done |
| 1 Timothy | `books/1-Timothy.md` | Greek-priority acknowledged | done |
| 2 Timothy | `books/2-Timothy.md` | Greek-priority acknowledged | done |
| Titus | `books/Titus.md` | Greek-priority acknowledged | done |
| Philemon | `books/Philemon.md` | Greek-priority acknowledged | done |
| Hebrews | `books/Hebrews.md` | Greek-priority acknowledged | done |
| James | `books/James.md` | Greek-priority acknowledged | done |
| 1 Peter | `books/1-Peter.md` | Greek-priority acknowledged | done |
| 2 Peter | `books/2-Peter.md` | Greek-priority acknowledged | done |
| 1 John | `books/1-John.md` | Aramaic-priority with Greek check | done |
| 2 John | `books/2-John.md` | Greek-priority acknowledged | done |
| 3 John | `books/3-John.md` | Greek-priority acknowledged | done |
| Jude | `books/Jude.md` | Greek-priority acknowledged | done |
| Revelation | `books/Revelation.md` | Greek-priority acknowledged | done |

## Pass 1 baseline decision package (applied)

1. Aramaic primacy posture documented.
2. No-removal rule documented.
3. Greek-priority acknowledgement documented for later NT segments.
4. Rope-oriented policy documented for Matthew 19:24 profile.
5. Local-only logging and QA workflow in place (no DB).

## Regeneration commands

```bash
python3 tools/local/nt_changelog_report.py
```

Outputs:
- `change-logs/new-testament/reports/NT-QA-LATEST.md`
- `change-logs/new-testament/reports/NT-QA-LATEST.json`
