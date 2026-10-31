# Evidence: compute of the reported runs (paper/sections/appendix.tex, tab:app-compute)

Written 2026-10-30. GitHub rows are read from the public REST API:
`https://api.github.com/repos/muzakkirhussain011/wardowl/actions/runs/<id>` (`created_at`,
`updated_at`, `head_sha`, `conclusion`) and
`https://api.github.com/repos/muzakkirhussain011/wardowl/actions/runs/<id>/jobs?per_page=100&filter=all`
(each job's `name`, `conclusion`, `started_at`, `completed_at`). Every run is attempt 1. Sums with awk
over the API's JSON; nothing else was computed.

## The counting rule

**Jobs** counts every job the jobs API lists for the workflow run: experiment jobs and also data, plan,
report, summary and publish jobs, and jobs the workflow skipped. **Job hours** sums
`completed_at - started_at` over the jobs that started (a skipped job never gets a runner and adds
nothing). **Wall clock** is the run's `updated_at - created_at`, so it includes queueing.

## GitHub-hosted runs

| Experiment | Run id | Head commit | Conclusion | Jobs listed | Skipped | Job hours | Wall clock h |
|---|---|---|---|---|---|---|---|
| Conformance campaign, run 1 | 40313285885 | `5d0f414` | success | 7 | 0 | 6.64 | 2.93 |
| Conformance campaign, run 2 | 40905549149 | `182bcbc` | success | 10 | 0 | 8.19 | 2.11 |
| Engines (X4, X7) | 40919304635 | `e66dffc` | success | 15 | 0 | 15.29 | 2.01 |
| Revocation and faults, rerun (X7 amendment 2) | 40969846593 | `41292bd` | success | 8 | 1 | 1.47 | 1.53 |
| Filter size and side channels (X3, X6) | 40940385704 | `a191626` | success | 15 | 0 | 10.15 | 3.33 |
| Their follow-up (amendment 4) | 40982986417 | `9e22b89` | failure | 11 | 3 | 7.42 | 2.19 |
| Frontiers and repair (X2, X5) | 40921769714 | `884ce18` | cancelled | 72 | 0 | 98.72 | 10.56 |

The two runs that did not conclude `success`: the follow-up's `fu-cb-elasticsearch` job lost its runner
(`evidence/x3-x6-followup.md`), and in X2/X5 `x2-m-chroma-b2` ended at the runner's job timeout
(`evidence/x2-x5-run1.md`).

## What each count holds, and how it relates to the other evidence files

| Run | Jobs, as listed | Other evidence said | Difference |
|---|---|---|---|
| Conformance run 1 | 6 campaign (sql-and-kv, search-engines, vector-dbs, embedded, engines, cloud), `summary` | `conformance-campaign-run1.md` lists the same 7; the paper's table said 6 | The table counted campaign jobs only; corrected to 7 and its "n/a" job hours to 6.6 |
| Conformance run 2 | 9 campaign (the six above, engines-keto, engines-casbin-1, engines-casbin-2), `summary` | `conformance-campaign-run2.md` said 8 | The evidence miscounted; corrected there |
| X4, X7 | 14 experiment, `report` | `x4-x7-run1.md`: "14 jobs ... plus a report job" | None |
| X7 rerun | `plan`, 5 experiment (a2-x7a-cerbos, a2-x7a-spicedb, a2-x7b-pgvector, a2-x7b-qdrant, a2-x7b-spicedb), `report`, `matrix.job` (skipped) | `x7-amendment2.md` said five | The evidence counted experiment jobs; it now says so |
| X3, X6 | `data`, 12 experiment (5 x6, 7 x3), `summary`, `publish to results/x3-x6` | `x3-x6-run1.md` listed 14 (statistics and publishing as one job) | The publish job is separate; corrected there |
| Follow-up | 6 experiment (fu-x3-chroma, fu-chroma-bisect, fu-cb-faiss, fu-cb-pgvector, fu-cb-qdrant, fu-cb-elasticsearch), `follow-up readings`, `publish to results/x3-x6`, skipped `data`, `summary`, `matrix.group` | `x3-x6-followup.md` names the six | None; it did not state a total |
| X2, X5 | 14 embedding (6 for E, 8 for M), `plan`, `prepare-e`, `prepare-m`, 11 X2-E, 34 X2-M, 8 X5, `stats`, `publish` | `x2-x5-run1.md` counts 11, 34 and 8 experiment jobs | None; it did not state a total |

## Kaggle runs (not in GitHub's API)

| Experiment | Hours | Source |
|---|---|---|
| End-to-end, first run (seed 7) | 2.8 | The last `time` field of the kernel log in `evidence/raw/x0-seed7/`: 10,234 s |
| End-to-end, three repeats (X8) | 2.9 to 3.3 each, 9.2 | The last `time` field of each kernel log in `evidence/raw/x8-seed*/`: 11,773, 11,144 and 10,356 s |
| End-to-end, OpenFGA, four runs | 0.6 to 0.9 each, 3.3 | The last `time` field of each kernel log in `evidence/raw/x8fga-seed*/`: 3,418, 2,116, 3,269 and 3,219 s |
| End-to-end, exposure, four seeds (X8 amendment 2) | 0.5 | The last `time` field of each kernel log in `evidence/raw/x8b-seed*/`: 443, 429, 385 and 414 s. The pool kernel took 9 s and is not listed |
| End-to-end, mutation control (X8 amendment 2) | 2.2 | The last `time` field of `evidence/raw/x8b-control-seed7/wardowl-x8b-control-seed7.log`: 7,960 s |
| Not in the paper's table: the X8 amendment 2 smoke run | 0.3 | 1,181 s, `evidence/x8-controls.md`; the table's caption leaves smoke runs out |
| Not in the paper's table: the recount kernel `wardowl-x8b-verify` | 0.0 | 9 s, the last `time` field of `evidence/raw/x8b-verify/wardowl-x8b-verify.log` |
| Diagnosis grid, run 1 (X1) | 7.3 | `x1-underretrieval-run1.md` ("Successfully ran in 26312.7s") |
| Diagnosis grid, run 2 (X1) | 6.1 wall, 12.5 session hours | From the Kaggle kernel logs, read 2026-10-30 with `kernels output` and kept in `evidence/raw/x1run2-*/` since 2026-10-31 (the last `time` field of each log, in seconds): `x1run2-prep-gpu` 417, `x1run2-shard-a` 8,254, `-shard-b` 15,411, `-shard-c` 20,207, and `x1run2-stats` about 830 (`raw/x1run2-stats/x1run2-stats.log`): 45,118 s, 12.5 h. Wall clock: prep pushed 19:12 UTC, statistics ended about 01:18 UTC, 6.1 h. One GPU session and four CPU sessions. |
