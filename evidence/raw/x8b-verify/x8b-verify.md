# X8b recount of the control's per-question claims, seed 7

| Mutation | Questions | Exposed off | Violations on | Incomplete on | Exposed, no violation | Violation, not exposed | Exposed, not incomplete | Incomplete, not exposed | Questions where counts differ | Unreadable off | Violations on | k=5 without k=10 | Answer canary | Answer canary not in prompt | Prompt canary | Prompt canary not in chunk |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | 1105 | 1103 | 1103 | 1103 | 0 | 0 | 0 | 0 | 0 | 15317 | 15317 | 0 | 138 | 0 | 805 | 0 |
| M2 | 1105 | 751 | 751 | 751 | 0 | 0 | 0 | 0 | 0 | 4834 | 4834 | 0 | 13 | 0 | 360 | 0 |
| M3 | 1105 | 533 | 533 | 533 | 0 | 0 | 0 | 0 | 0 | 7642 | 7642 | 0 | 107 | 0 | 503 | 0 |

## M3-off: distinct (question, chunk) unreadable pairs by where the chunk lies

- own tenant: 4979
- shared passage: 126
- other tenant: 0

## M3-off: questions with an unreadable hit

| Group | Questions | k=5 | k=10 |
|---|---|---|---|
| generic | 108 | 67 | 68 |
| targeted | 376 | 2 | 3 |
| forbidden | 189 | 189 | 189 |
| redteam | 432 | 270 | 273 |
| alice | 113 | 57 | 57 |
| bob | 113 | 60 | 60 |
| carol | 113 | 33 | 33 |
| dave | 113 | 58 | 59 |
| erin | 113 | 49 | 49 |
| frank | 113 | 63 | 65 |
| grace | 23 | 11 | 11 |
| heidi | 23 | 15 | 15 |
| ivan | 90 | 36 | 36 |
| judy | 90 | 44 | 46 |
| mallory | 21 | 21 | 21 |
| peggy | 90 | 45 | 45 |
| trent | 90 | 36 | 36 |
