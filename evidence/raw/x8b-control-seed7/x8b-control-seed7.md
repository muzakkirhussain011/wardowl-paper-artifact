# X8b positive control, seed 7

## What each pre-filter admits

| Filter | People over-admitted | Over-admitted chunks min / median / max | Readable chunks left out (max) |
|---|---|---|---|
| P0 | 0 | 0 / 0 / 0 | 0 |
| M1 | 189 | 48275 / 48899 / 107540 | 0 |
| M2 | 188 | 0 / 1041 / 1665 | 0 |
| M3 | 189 | 832 / 1456 / 60097 | 0 |

## The harness's counts (both retrievals and the end-to-end questions)

| Pass | Re-check | Hits checked | Unreadable hits | Canaries chunk / prompt / answer | Violations | Errors | Failed checks | Recall@10 |
|---|---|---|---|---|---|---|---|---|
| faiss | on | 16360 | 0 | 0 / 0 / 0 | 0 | 0 | 0 | 1.0 |
| M1-off | off | 16675 | 15401 | 11652 / 3915 / 223 | 0 | 0 | 4 | 0.0766 |
| M2-off | off | 16360 | 4854 | 2849 / 936 / 20 | 0 | 0 | 4 | 0.7032 |
| M3-off | off | 16675 | 7698 | 7392 / 2487 / 114 | 0 | 0 | 4 | 0.5484 |
| M1-on | on | 1274 | 0 | 0 / 0 / 0 | 15317 | 0 | 2 | 0.0766 |
| M2-on | on | 11506 | 0 | 0 / 0 / 0 | 4834 | 0 | 2 | 0.7032 |
| M3-on | on | 8977 | 0 | 0 / 0 / 0 | 7642 | 0 | 2 | 0.5484 |

## Per question (main retrievals only)

| Pass | Questions | With unreadable hit k=5 | k=10 | Distinct (question, chunk) | Canary in chunk | Prompt | Answer | With violations | Incomplete |
|---|---|---|---|---|---|---|---|---|---|
| faiss | 1105 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| M1-off | 1105 | 1052 | 1103 | 10220 | 805 | 805 | 138 | 0 | 0 |
| M2-off | 1105 | 676 | 751 | 3217 | 400 | 360 | 13 | 0 | 0 |
| M3-off | 1105 | 528 | 533 | 5105 | 509 | 503 | 107 | 0 | 0 |
| M1-on | 1105 | 0 | 0 | 0 | 0 | 0 | 0 | 1103 | 1103 |
| M2-on | 1105 | 0 | 0 | 0 | 0 | 0 | 0 | 751 | 751 |
| M3-on | 1105 | 0 | 0 | 0 | 0 | 0 | 0 | 533 | 533 |

## Per question and category (questions with a detection)

| Pass | Category | Questions | Unreadable k=5 | k=10 | Canary in chunk | Prompt | Answer | With violations |
|---|---|---|---|---|---|---|---|---|
| faiss | generic | 108 | 0 | 0 | 0 | 0 | 0 | 0 |
| faiss | targeted | 376 | 0 | 0 | 0 | 0 | 0 | 0 |
| faiss | forbidden | 189 | 0 | 0 | 0 | 0 | 0 | 0 |
| faiss | redteam | 432 | 0 | 0 | 0 | 0 | 0 | 0 |
| M1-off | generic | 108 | 108 | 108 | 90 | 90 | 5 | 0 |
| M1-off | targeted | 376 | 376 | 376 | 206 | 206 | 0 | 0 |
| M1-off | forbidden | 189 | 189 | 189 | 185 | 185 | 3 | 0 |
| M1-off | redteam | 432 | 379 | 430 | 324 | 324 | 130 | 0 |
| M2-off | generic | 108 | 41 | 51 | 23 | 20 | 0 | 0 |
| M2-off | targeted | 376 | 359 | 361 | 193 | 189 | 1 | 0 |
| M2-off | forbidden | 189 | 84 | 108 | 62 | 48 | 0 | 0 |
| M2-off | redteam | 432 | 192 | 231 | 122 | 103 | 12 | 0 |
| M3-off | generic | 108 | 67 | 68 | 66 | 64 | 0 | 0 |
| M3-off | targeted | 376 | 2 | 3 | 3 | 2 | 0 | 0 |
| M3-off | forbidden | 189 | 189 | 189 | 185 | 185 | 0 | 0 |
| M3-off | redteam | 432 | 270 | 273 | 255 | 252 | 107 | 0 |
| M1-on | generic | 108 | 0 | 0 | 0 | 0 | 0 | 108 |
| M1-on | targeted | 376 | 0 | 0 | 0 | 0 | 0 | 376 |
| M1-on | forbidden | 189 | 0 | 0 | 0 | 0 | 0 | 189 |
| M1-on | redteam | 432 | 0 | 0 | 0 | 0 | 0 | 430 |
| M2-on | generic | 108 | 0 | 0 | 0 | 0 | 0 | 51 |
| M2-on | targeted | 376 | 0 | 0 | 0 | 0 | 0 | 361 |
| M2-on | forbidden | 189 | 0 | 0 | 0 | 0 | 0 | 108 |
| M2-on | redteam | 432 | 0 | 0 | 0 | 0 | 0 | 231 |
| M3-on | generic | 108 | 0 | 0 | 0 | 0 | 0 | 68 |
| M3-on | targeted | 376 | 0 | 0 | 0 | 0 | 0 | 3 |
| M3-on | forbidden | 189 | 0 | 0 | 0 | 0 | 0 | 189 |
| M3-on | redteam | 432 | 0 | 0 | 0 | 0 | 0 | 273 |

## M1-off against measurement 1

Of 1105 questions: same chunk ids at k=10 1105, different only at ties within 1e-4 of the tenth score 0, same unreadable count at k=5 1105, at k=10 1105.
