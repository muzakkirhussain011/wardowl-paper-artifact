# X8b positive control, seed 7 (smoke: not a result)

## What each pre-filter admits

| Filter | People over-admitted | Over-admitted chunks min / median / max | Readable chunks left out (max) |
|---|---|---|---|
| P0 | 0 | 0 / 0 / 0 | 0 |
| M1 | 189 | 947 / 959 / 2980 | 0 |
| M2 | 188 | 0 / 21 / 33 | 0 |
| M3 | 189 | 16 / 28 / 2049 | 0 |

## The harness's counts (both retrievals and the end-to-end questions)

| Pass | Re-check | Hits checked | Unreadable hits | Canaries chunk / prompt / answer | Violations | Errors | Failed checks | Recall@10 |
|---|---|---|---|---|---|---|---|---|
| faiss | on | 10755 | 0 | 0 / 0 / 0 | 0 | 0 | 0 | 1.0 |
| M1-off | off | 11070 | 10711 | 7893 / 2630 / 42 | 0 | 0 | 4 | 0.0353 |
| M2-off | off | 10755 | 3224 | 1744 / 611 / 19 | 0 | 0 | 4 | 0.7106 |
| M3-off | off | 11070 | 4601 | 4040 / 1659 / 38 | 0 | 0 | 4 | 0.6381 |
| M1-on | on | 359 | 0 | 0 / 0 / 0 | 10696 | 0 | 2 | 0.0353 |
| M2-on | on | 7531 | 0 | 0 / 0 / 0 | 3221 | 0 | 2 | 0.7106 |
| M3-on | on | 6469 | 0 | 0 / 0 / 0 | 4593 | 0 | 2 | 0.6381 |

## Per question (main retrievals only)

| Pass | Questions | With unreadable hit k=5 | k=10 | Distinct (question, chunk) | Canary in chunk | Prompt | Answer | With violations | Incomplete |
|---|---|---|---|---|---|---|---|---|---|
| faiss | 737 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| M1-off | 737 | 737 | 737 | 7117 | 545 | 544 | 39 | 0 | 0 |
| M2-off | 737 | 539 | 588 | 2072 | 332 | 261 | 9 | 0 | 0 |
| M3-off | 737 | 473 | 525 | 2801 | 498 | 436 | 37 | 0 | 0 |
| M1-on | 737 | 0 | 0 | 0 | 0 | 0 | 0 | 737 | 737 |
| M2-on | 737 | 0 | 0 | 0 | 0 | 0 | 0 | 588 | 588 |
| M3-on | 737 | 0 | 0 | 0 | 0 | 0 | 0 | 525 | 525 |

## Per question and category (questions with a detection)

| Pass | Category | Questions | Unreadable k=5 | k=10 | Canary in chunk | Prompt | Answer | With violations |
|---|---|---|---|---|---|---|---|---|
| faiss | generic | 108 | 0 | 0 | 0 | 0 | 0 | 0 |
| faiss | targeted | 188 | 0 | 0 | 0 | 0 | 0 | 0 |
| faiss | forbidden | 189 | 0 | 0 | 0 | 0 | 0 | 0 |
| faiss | redteam | 252 | 0 | 0 | 0 | 0 | 0 | 0 |
| M1-off | generic | 108 | 108 | 108 | 90 | 90 | 0 | 0 |
| M1-off | targeted | 188 | 188 | 188 | 104 | 104 | 0 | 0 |
| M1-off | forbidden | 189 | 189 | 189 | 185 | 185 | 0 | 0 |
| M1-off | redteam | 252 | 252 | 252 | 166 | 165 | 39 | 0 |
| M2-off | generic | 108 | 57 | 60 | 25 | 24 | 0 | 0 |
| M2-off | targeted | 188 | 184 | 188 | 148 | 108 | 0 | 0 |
| M2-off | forbidden | 189 | 107 | 127 | 52 | 44 | 0 | 0 |
| M2-off | redteam | 252 | 191 | 213 | 107 | 85 | 9 | 0 |
| M3-off | generic | 108 | 74 | 74 | 73 | 73 | 0 | 0 |
| M3-off | targeted | 188 | 43 | 84 | 74 | 25 | 0 | 0 |
| M3-off | forbidden | 189 | 189 | 189 | 189 | 187 | 1 | 0 |
| M3-off | redteam | 252 | 167 | 178 | 162 | 151 | 36 | 0 |
| M1-on | generic | 108 | 0 | 0 | 0 | 0 | 0 | 108 |
| M1-on | targeted | 188 | 0 | 0 | 0 | 0 | 0 | 188 |
| M1-on | forbidden | 189 | 0 | 0 | 0 | 0 | 0 | 189 |
| M1-on | redteam | 252 | 0 | 0 | 0 | 0 | 0 | 252 |
| M2-on | generic | 108 | 0 | 0 | 0 | 0 | 0 | 60 |
| M2-on | targeted | 188 | 0 | 0 | 0 | 0 | 0 | 188 |
| M2-on | forbidden | 189 | 0 | 0 | 0 | 0 | 0 | 127 |
| M2-on | redteam | 252 | 0 | 0 | 0 | 0 | 0 | 213 |
| M3-on | generic | 108 | 0 | 0 | 0 | 0 | 0 | 74 |
| M3-on | targeted | 188 | 0 | 0 | 0 | 0 | 0 | 84 |
| M3-on | forbidden | 189 | 0 | 0 | 0 | 0 | 0 | 189 |
| M3-on | redteam | 252 | 0 | 0 | 0 | 0 | 0 | 178 |

## M1-off against measurement 1

Of 737 questions: same chunk ids at k=10 737, different only at ties within 1e-4 of the tenth score 0, same unreadable count at k=5 737, at k=10 737.
