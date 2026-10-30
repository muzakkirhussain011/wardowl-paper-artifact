# Evidence: X1 run 2, under-retrieval under permission filters

Written 2026-10-30. Pre-registration: `benchmarks/paper/PREREGISTRATION.md` on branch
`paper/x1-underretrieval` (worktree `D:\Projects\wardowl-x1`), with amendment 1 (2026-10-26) and
amendment 2 (2026-10-29, after run 1 and before run 2; items 1 to 9 at commit eeb7d2b, items 10 to 12
"revised after the smoke run" at 80e3f56, before any full run). Harness at a956424.
Raw outputs: `evidence/raw/x1run2-stats/x1run2-stats/` (`report.md`, `summary_by_setting.csv`,
`summary_by_build.csv`, `intervals.csv`, `paired.csv`, `plans.csv`, `explain_summary.csv`,
`qdrant_paths.csv`, `acorn_engagement.csv`, `predictions.csv`, `manifest.json`, `x1_stats.log`).
Run 1 is `evidence/x1-underretrieval-run1.md`; the diagnosis that led to amendment 2 is
`investigations/x0-x1-pgvector-gap.md`.

## What ran

Kaggle, account muzakkirhussain1, CPU sessions: `x1run2-prep` (corpus, embeddings, exact baseline,
question table), shards `x1run2-shard-a` (hnsw-m16-efc64 build 0, with the two replays first),
`-shard-b` (hnsw-m16-efc64 builds 1 and 2) and `-shard-c` (hnsw-m32-efc200 builds 0 to 2, then the
Qdrant grid), and `x1run2-stats` (10,000 bootstrap resamples, seed 20261026; 798 s). 194,291 result
rows of 49 settings; 1,489 questions (the scenario's 1,105 and 384 probe questions of 24
single-group people), three timed passes, three builds per layout. PostgreSQL 16 with pgvector
0.8.7; Qdrant 1.19.2. Every pgvector invocation ran `VACUUM (ANALYZE)` once (after the replays in
shard A, before the first setting in B and C), per amendment 2 item 11.

Settings added by amendment 2: `pg-custom` (`plan_cache_mode = force_custom_plan`), `pg-hnsw` (that
plus `enable_seqscan` and `enable_bitmapscan` off, so the HNSW index scan is the only plan; the
reference of P1 and P2), and every P-a to P-e setting forced the same way; `p-asrun` keeps the server
and psycopg defaults; `p-x0` replays the original pass right after the load, `p-x0v` the same after
`VACUUM (ANALYZE)`.

## Verdicts as printed

| Hypothesis | Verdict | Key numbers |
|---|---|---|
| Q1 islanded permitted subgraph in Qdrant | confirmed | judy recall@10 1.000; company documents 0.369 [0.334, 0.402]; 97.5% of non-counting top-5 hits are shared passages; ACORN 1.0 0.808 [0.785, 0.830], tenant-m0 0.952 [0.944, 0.960] |
| Q2 ACORN's default gate engages unreliably | falsified | engaged for 100% of people; ACORN 1.0 minus 0.4: 0.0000 |
| Q3 recall varies by build and segment layout | inconclusive | range between as-run builds 0.086; one-segment minus as-run -0.030 [-0.042, -0.018], but both layouts ended with one data segment |
| Q4 hnsw_ef 128 was not the cause | inconclusive | hnsw_ef 512 minus 128: +0.1025 [0.0895, 0.1158] (confirm needs < 0.05, falsify > 0.15) |
| P1 the iterative scan's budget runs out | inconclusive | 393 empty results under pg-hnsw; (a) 0.799 of them had their first readable row beyond half the reach (needs 0.95): False; (b) lowest ERR of a raised limit 0.000: True; (c) median rows emitted on empties 20,181: True |
| P2 mis-retrieval from shallow, relaxed scans | inconclusive | ef_search 1000 minus 100 +0.0693 [0.0607, 0.0777]; inner LIMIT 10x minus 1x +0.0952 [0.0833, 0.1073]; m32/efc200 minus m16/efc64 +0.0663 [0.0550, 0.0778]; (d) loss at rho_100 < 0.1 is 0.368 against 0.188 elsewhere, not twice: False; similarity gap of missed questions 0.015 |
| P3 the planner overestimates a judy filter | confirmed | median planner estimate over R for judys 11.1; ph-exact ERR 0.000 |
| P4 generic plans make no difference | falsified | pg-custom minus p-asrun recall@10 -0.3428 [-0.3742, -0.3121], ERR +0.0890 [0.0552, 0.1253], McNemar p < 0.05; 17,556 generic executions under p-asrun; 150 of 150 fixed questions had another generic plan |
| P5 the plan cache decides whether pgvector searches the graph | confirmed | HNSW share 0.981 under pg-custom, 0.009 under p-asrun; pg-custom recall@5 0.680 [0.663, 0.697] (within 0.08 of X0's 0.691); p-asrun recall@5 0.996 [0.991, 1.000] at p50 361.6 ms against pg-custom's 22.4 ms |

## The replays (amendment 2 item 4; predictions of the revised amendment)

| Replay | GIN pending pages before | Generic plans | HNSW share | Recall@5 | Recall@10 | Empty@5 | p50 ms |
|---|---|---|---|---|---|---|---|
| p-x0 (right after the load) | 388 | 0 | 0.981 | 0.697 [0.677, 0.717] | 0.729 | 0.006 | 7.0 |
| p-x0v (after VACUUM (ANALYZE)) | 0 | 2,148 | 0.009 | 0.998 [0.996, 1.000] | 0.998 | 0.000 | 335.3 |

The predicted pattern held: `p-x0` kept custom HNSW plans and reproduced X0 (recall@5 0.691, p50
6.5 ms), and `p-x0v` switched to generic exact plans after its first executions. Mechanism, from
PostgreSQL 16's `gincostestimate` (`src/backend/utils/adt/selfuncs.c`, REL_16_STABLE, read
2026-10-30): the GIN cost estimate charges every pending-list page as an entry page fetched at the
start of the scan (`entryPagesFetched = numPendingPages`, costed at `random_page_cost`), so a GIN
index with a long pending list, as a bulk load leaves it until VACUUM (or autovacuum) merges the
list, looks expensive to the planner. The generic plan of the prepared search is the GIN bitmap scan
plus a sort (exact); while the pending list is long its estimated cost exceeds the average of the
first five custom plans, which use the HNSW index, and PostgreSQL keeps planning custom; once VACUUM
has emptied the list the generic plan is cheaper and PostgreSQL switches to it for good on that
statement and connection (`plancache.c`, `choose_custom_plan`). Whether a run of the scenario is
fast and lossy or exact and slow is therefore decided by whether autovacuum has processed the table
before the statements reach their sixth execution. This explains X0 and X8's three fast and five
exact runs (`evidence/x8-run.md`) without any difference in data or settings [the autovacuum timing
of those runs was not recorded; inference].

## pgvector under the HNSW scan (hnsw-m16-efc64, means over three builds, all 1,489 questions)

| Setting | Recall@5 | Recall@10 | Empty@5 | Short@5 | p50 ms |
|---|---|---|---|---|---|
| p-asrun (planner's choice, prepared; generic exact plans) | 0.997 | 0.999 | 0.000 | 0.000 | 403.2 |
| pg-custom (custom plans; 98.6% HNSW) | 0.621 | 0.656 | 0.089 | 0.109 | 22.8 |
| pg-hnsw (HNSW forced; reference) | 0.621 | 0.656 | 0.089 | 0.109 | 24.3 |
| pc-ef40 / ef200 / ef400 / ef1000 | 0.596 / 0.634 / 0.667 / 0.704 | 0.634 / 0.667 / 0.693 / 0.725 | 0.086 to 0.089 | | 24.5 to 31.7 |
| pa-t100k-m1, pa-t1000k-m1 (tuple limit raised alone) | 0.645 | 0.683 | 0.073 | 0.085 | 25 to 26 |
| pa-t20k-m8, pb-wm64 (memory raised alone) | 0.621 | 0.656 | 0.089 | 0.109 | 25 |
| pa-t100k-m8, pa-t1000k-m8, pa-t1000k-m16 (both raised) | 0.737 | 0.779 to 0.780 | 0.000 | 0.000 | 24 to 25 |
| pd-lim4 / pd-lim10 (inner LIMIT 4x / 10x) | 0.698 / 0.732 | 0.724 / 0.751 | 0.089 | | 27.0 / 30.2 |
| pe-strict (strict order) | 0.477 | 0.497 | 0.090 | | 25.2 |
| ph-exact (index scans off) | 1.000 | 1.000 | 0.000 | 0.000 | 329.9 |
| hnsw-m32-efc200: pg-hnsw / both limits raised / ef400 / lim10 | 0.698 / 0.833 / 0.720 / 0.768 | 0.722 / 0.866 / 0.744 / 0.786 | 0.097 / 0.000 / 0.094 / 0.097 | | 33 to 44 |

Readings:
- Both scan limits bind. Raising the tuple limit alone (to 100,000 or 1,000,000) lowered the
  empty-result rate only from 0.089 to 0.073, because the memory bound (`scan_mem_multiplier` x
  `work_mem`, 4 MB) then stops the scan; raising memory alone changed nothing; raising both removed
  every empty answer. This corrects run 1's reading ("every setting that raised the tuple limit to
  100,000 or more removed the empty answers"), which came from searches that mostly ran generic,
  exact plans.
- Removing the empties did not remove the loss: with both limits raised recall@10 stayed at 0.78
  (0.87 on the larger graph). The rest is mis-retrieval of relaxed-order scans that stop at the first
  k permitted rows: more candidates (inner LIMIT 10x: +0.095), a deeper search (ef_search 1000:
  +0.069) and a better graph (+0.066) each help; strict order is worse (0.497).
- P3: for the least-privileged people the planner's row estimate is a median 11.1 times their true
  readable count, so it prefers the HNSW scan where an exact plan would be both correct and cheap.

## Qdrant (means over three builds, all 1,489 questions)

| Layout | Setting | Recall@10 | Range over builds | p50 ms |
|---|---|---|---|---|
| as run | hnsw_ef 128 | 0.656 | 0.086 | 7.06 |
| as run | hnsw_ef 64 | 0.600 | 0.074 | 5.96 |
| as run | hnsw_ef 512 | 0.758 | 0.120 | 11.3 |
| as run | ACORN 0.4 or 1.0 | 0.808 | 0.127 | 7.26 |
| as run | exact | 1.000 | n/a | 43.1 |
| is_tenant | as run / ACORN | 0.651 / 0.802 | 0.025 / 0.076 | 6.91 / 7.09 |
| one segment | as run / ACORN | 0.625 / 0.777 | 0.029 / 0.027 | 7.04 / 7.18 |
| per-tenant graphs (is_tenant, m = 0) | as run | 0.952 | 0.001 | 6.58 |
| shared passages in a separate collection | as run | 0.949 | 0.003 | 12.9 |

Run 1 (`x1-underretrieval-run1.md`) agrees within the build-to-build range: as run 0.619, ACORN
0.761, per-tenant 0.943, separate 0.948, hnsw_ef 512 0.709. Q3's segment manipulation did not
differ in the end: both the as-run and the one-segment layouts ended with one segment holding
points (`data_segments`), so the -0.030 difference is a difference between builds, not layouts.

## Consequences for the paper

- `quality.tex`, sec:qual-pgvector: rewrite around the plan cache (P4 falsified, P5 confirmed, the
  replays and `gincostestimate`), then the HNSW scan's own loss (both limits bind; mis-retrieval
  remains), and P3. Correct run 1's tuple-limit sentence.
- `quality.tex`, sec:qual-qdrant and Table tab:qual-qdrant: run 2's numbers, Q3 and Q4 as printed;
  company-document recall 0.369 (run 1: 0.273).
- Introduction: "recall@10 of 0.27 on company documents, 0.94 with a tenant-aware layout" becomes
  run 2's 0.37 and 0.95; pgvector's empty answers are attributed to both scan limits and the mode to
  the plan cache.
