# Evidence: X1 under-retrieval experiment, Kaggle run 1 (and the X0 re-analysis)

Raw outputs, without the embeddings and query vectors: `evidence/raw/x1-run1/` (`x0/`, `x1-smoke/`, `x1/` with `stats/`,
`runs/`, `telemetry/`, `explain/`, `manifest.json` and `x1.log`, the kernel log
`wardowl-under-retrieval-diagnosis-run-1.log` and the gzipped `qdrant.log`), fetched with `kernels output` from kernel
`wardowl-under-retrieval-diagnosis-run-1` (`kaggle/x1-run1/`). The pre-registration is
`benchmarks/paper/PREREGISTRATION.md` on the wardowl branch `paper/x1-underretrieval`; the verdicts below are the ones
`x1_stats.py` printed, not re-derived.

**Two executions of run 1.** Run 1 was first executed on 2026-10-26 and again on 2026-11-07, with the same notebook
(pinned to commit `947fb8f`, whose `wardowl/` tree equals tag `v2.1.0`), the same scripts, seeds and session type. This
artifact holds the second execution, and every run-1 number below is from it unless it is marked as the first
execution's. The second execution read X0's second execution (kernel source `wardowl-end-to-end-scale-run-seed-7`); the
SHA-256 of `answers.jsonl` and `results.json` in `x0/manifest.json` equal those in `evidence/raw/x0-seed7/`. Run 2
(`x1-underretrieval-run2.md`) and amendment 2 were written after the first execution; the section "Against the first
execution" lists what changed. This file described the first execution until 2026-11-07.

## Setup

One Kaggle session (GPU T4 x2, 4 CPUs, 31.3 GiB RAM; the kernel log prints the commit `947fb8f11efa917ec86402d381c1983d143df7df`,
psycopg 3.3.8, psycopg-pool 3.3.3, qdrant-client 1.20.0, Qdrant server 1.19.2 commit `016542aa`, PostgreSQL 16 with pgvector
0.8.7) ran, in order: X0, an offline re-analysis of X0's `answers.jsonl` (11,050 lines, 1,105 per store); an X1 smoke run
(`--smoke`, 0.08 h, 0 failures) and its statistics; the full X1 on pgvector (`--stores pgvector --max-hours 5.5`, started
2026-11-07T03:41:26 UTC by `x1/manifest.json`), then on Qdrant; and `x1_stats.py` on `/kaggle/working/x1` (10,000 bootstrap
resamples, seed 20261026). X1 measures recall@5/10, the empty-result rate and related diagnostics against an exact
baseline for one question set (1,489 questions) under pre-registered settings: pgvector `hnsw-m16-efc64` with
`iterative_scan=relaxed_order` and variations of `max_scan_tuples`, `scan_mem_multiplier`, `work_mem` and `ef_search`;
Qdrant in five layouts (as-run, is-tenant, tenant-m0, separate-kb, one-segment), three builds each, with `hnsw_ef` 64 and
512, ACORN 0.4 and 1.0, and exact search.

## Status (kernel log and `x1/x1.log`)

- Every step returned exit code 0 (x0, x1 smoke, x1 smoke statistics, x1 pgvector, x1 qdrant, x1 statistics); the log ends
  with "every step finished cleanly". The last `time` field of the kernel log is 24,960 s (6.9 h).
- X0: 0 empty k=5 results in `answers.jsonl` ("the hit shortfall implies 7.5").
- X1 pgvector: "X1 finished in 5.11 h: 0 failures, 0 unsupported, 12 skipped". The deadline guard ("24 min left before the
  deadline, and a pgvector setting took up to 29 min") dropped the same 12 items as in the first execution: settings
  `pc-ef1000`, `pd-lim4`, `pd-lim10`, `pe-strict`, `pg-custom`, `pg-noprepare`, `ph-exact` of build `hnsw-m16-efc64-b0`,
  and whole builds `hnsw-m16-efc64-b1`, `-b2`, `hnsw-m32-efc200-b0`, `-b1`, `-b2`. One pgvector build ran, with 11 settings.
- X1 Qdrant: "X1 finished in 1.60 h: 0 failures, 0 unsupported, 0 skipped". Every Qdrant build, one-segment included,
  ended with two segments (`qdrant one-segment build N: ... segments {'wardowl_enterprise': 2}`).
- X1 statistics: "99,763 result rows of 33 settings; 67 setting records", done in 366 s; wrote summary_by_build.csv (67
  rows), summary_by_setting.csv (33), intervals.csv (3,696), paired.csv (352), explain_summary.csv (11), qdrant_paths.csv
  (242), acorn_engagement.csv (176), predictions.csv (8).

## X0 re-analysis (`x0/summary.md`)

Overlap@5 is the share of FAISS's top 5 (exact) among a store's top 5 for the same person and question; ties are not
credited. Questions whose person may read nothing are left out. The script's title and its "Predicted" column were written
for X0's first execution and are printed as they stand.

| Item | Predicted (section 6.0) | Observed |
|---|---|---|
| pgvector empty results | about 10 to 12, all judys, mostly forbidden questions | 0; judys 0; forbidden 0 |
| Qdrant overlap@5 for judys | near 1 | 1.000 |
| Qdrant overlap@5, KB readers, targeted and generic | low | 0.365 |
| pgvector overlap@5: targeted and generic / forbidden and red team | loss concentrated in targeted and generic | 0.885 / 0.561 |
| kb/ share of the top 5 on targeted questions: Qdrant / FAISS | Qdrant mostly kb/ where FAISS has tenant documents | 0.652 / 0.000 |

pgvector's overlap loss sits in forbidden and red-team questions (0.561), not targeted and generic (0.885), against the
section 6.0 expectation, as in the first execution (0.550 and 0.870). The run's own numbers are those of
`evidence/x0-scale-run.md` (89 checks passed; pgvector + OpenFGA did not start).

Overlap@5 by category:

| store | generic | targeted | forbidden | redteam |
|---|---|---|---|---|
| faiss | 1.000 | 1.000 | 1.000 | 1.000 |
| chroma | 0.823 | 0.972 | 0.847 | 0.817 |
| pgvector | 0.685 | 0.936 | 0.533 | 0.574 |
| pgvector + OPA | 0.685 | 0.936 | 0.533 | 0.574 |
| qdrant | 0.700 | 0.340 | 0.581 | 0.652 |
| elasticsearch | 0.940 | 0.989 | 0.948 | 0.936 |
| opensearch | 0.894 | 0.994 | 0.905 | 0.935 |
| weaviate | 0.787 | 0.991 | 0.866 | 0.833 |
| redis | 1.000 | 0.997 | 1.000 | 0.982 |
| lancedb | 0.894 | 1.000 | 0.810 | 0.724 |

Overlap@5 by person type (no-groups: n/a for every store):

| store | judy | kb-reader |
|---|---|---|
| faiss | 1.000 | 1.000 |
| chroma | 0.964 | 0.868 |
| pgvector | 0.704 | 0.702 |
| pgvector + OPA | 0.704 | 0.702 |
| qdrant | 1.000 | 0.494 |
| elasticsearch | 0.980 | 0.955 |
| opensearch | 1.000 | 0.942 |
| weaviate | 1.000 | 0.879 |
| redis | 1.000 | 0.991 |
| lancedb | 0.993 | 0.836 |

kb/ share of the top 5 on targeted questions (reference share 0.000 for every store): qdrant 0.652, pgvector and
pgvector + OPA 0.003, every other store 0.000.

## X1 verdicts (`x1/stats/report.md`; criteria as printed)

| ID | Hypothesis label (as printed) | Verdict | First execution |
|---|---|---|---|
| Q1 | islanded permitted subgraph in Qdrant | **confirmed** | confirmed |
| Q2 | ACORN's default gate engages unreliably | **falsified** | falsified |
| Q3 | recall varies by build and segment layout | **inconclusive** | inconclusive |
| Q4 | hnsw_ef 128 was not the cause | **inconclusive** | inconclusive |
| P1 | the iterative scan's budget runs out | **inconclusive** | confirmed |
| P2 | mis-retrieval from shallow, relaxed scans | **inconclusive** | inconclusive |
| P3 | the planner overestimates a judy filter | **inconclusive** | inconclusive |
| P4 | generic plans make no difference | **falsified** | falsified |

Q1, confirmed:
- confirm (i) judy recall@10 1.0000 [1.0000, 1.0000] >= 0.95: True
- confirm (ii) company-document recall@10 0.3135 [0.2756, 0.3498] <= 0.75, upper end below judy's lower end: True
- confirm (iii) kb/ share of non-counting top-5 hits 0.979 >= 0.5: True
- confirm (iv) best of ACORN 1.0 0.8139 [0.7913, 0.8352] and tenant-m0 0.9366 [0.9259, 0.9465] >= 0.90: True
- falsify: category miss-rate spread 0.627 < 0.10: False
- falsify: gains of ACORN 1.0 and tenant-m0 (0.173, 0.295) both < 0.02: False

Q2, falsified:
- confirm: share of people ACORN 0.4 engaged for 1.000 in (0.05, 0.95): False
- confirm: ACORN 1.0 minus 0.4 in recall@10 0.0000 [0.0000, 0.0000] above 0: False
- falsify: |ACORN 1.0 minus 0.4| < 0.01 with an interval containing 0: True

Q3, inconclusive:
- confirm: recall@10 range between as-run builds 0.021 >= 0.01: True
- confirm: one-segment minus as-run -0.0025 [-0.0142, 0.0096] excludes 0: False
- falsify: range < 0.002 and |one-segment minus as-run| < 0.002: False
- note: segments: as-run `{"wardowl_enterprise": 2}`, one-segment `{"wardowl_enterprise": 2}`; "both layouts ended with the
  same segments", so the one-segment manipulation did not take effect.

Q4, inconclusive:
- confirm: hnsw_ef 512 minus 128 0.0971 [0.0842, 0.1100] < 0.05: False
- falsify: gain > 0.15: False

P1, inconclusive:
- confirm: p-asrun reproduces empty results: False
- note: "no empty result under p-asrun". With no empty answer under the reference setting, the budget criteria (a) to (c)
  could not be evaluated. The first execution, which had empty answers under p-asrun (ERR 0.000681), printed "confirmed".

P2, inconclusive (criteria (a) to (c) and the falsifier have no data, because their settings were skipped):
- confirm (d) loss at rho_100 < 0.1 0.081 at least twice the rest 0.074: False
- confirm (e) mean similarity gap of missed questions 0.015 <= 0.02: True

P3, inconclusive:
- confirm: median planner estimate / R for judys 11.5 >= 5: True
- confirm: ph-exact ERR == 0: None (ph-exact was skipped)
- falsify: median ratio within [0.5, 2]: False

P4, falsified:
- every recall@10 and ERR criterion on pg-custom and pg-noprepare: None (both settings skipped)
- confirm: "generic plans run under p-asrun: 4308; fixed questions with another generic plan: 50 of 50: none run, or none
  differs": False
- falsify: the same count, "some run and some differ": True
- note: generic plans of the search statement under p-asrun: 4,308 (amendment 1)

## X1 settings table (`report.md`; means over builds; range between builds)

| store | layout | setting | builds | recall5 | recall10 | recall10_range | empty5 | short5 | gross_miss10 | sim_gap10 | latency_p50 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | hnsw-m16-efc64 | p-asrun | 1 | 0.907 | 0.920 | n/a | 0.000 | 0.000 | 0.082 | 0.003 | 352.2 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m1 | 1 | 0.999 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 385.7 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m16 | 1 | 0.999 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 377.3 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m8 | 1 | 0.999 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 385.9 |
| pgvector | hnsw-m16-efc64 | pa-t100k-m1 | 1 | 0.999 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 370.3 |
| pgvector | hnsw-m16-efc64 | pa-t100k-m8 | 1 | 0.999 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 378.6 |
| pgvector | hnsw-m16-efc64 | pa-t20k-m8 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 388.9 |
| pgvector | hnsw-m16-efc64 | pb-wm64 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 376.0 |
| pgvector | hnsw-m16-efc64 | pc-ef200 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 372.3 |
| pgvector | hnsw-m16-efc64 | pc-ef40 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 382.2 |
| pgvector | hnsw-m16-efc64 | pc-ef400 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 373.1 |
| qdrant | as-run | q-asrun | 3 | 0.648 | 0.641 | 0.021 | 0.000 | 0.001 | 0.383 | 0.045 | 4.232 |
| qdrant | as-run | qa-acorn040 | 3 | 0.817 | 0.814 | 0.060 | 0.000 | 0.001 | 0.215 | 0.016 | 4.366 |
| qdrant | as-run | qa-acorn100 | 3 | 0.817 | 0.814 | 0.060 | 0.000 | 0.001 | 0.215 | 0.016 | 4.404 |
| qdrant | as-run | qb-ef512 | 3 | 0.739 | 0.738 | 0.012 | 0.000 | 0.001 | 0.298 | 0.035 | 7.145 |
| qdrant | as-run | qb-ef64 | 3 | 0.597 | 0.591 | 0.032 | 0.000 | 0.001 | 0.423 | 0.050 | 3.626 |
| qdrant | as-run | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 34.1 |
| qdrant | is-tenant | q-asrun | 3 | 0.638 | 0.631 | 0.047 | 0.000 | 0.000 | 0.396 | 0.047 | 4.174 |
| qdrant | is-tenant | qa-acorn040 | 3 | 0.822 | 0.818 | 0.030 | 0.000 | 0.000 | 0.217 | 0.015 | 4.336 |
| qdrant | is-tenant | qa-acorn100 | 3 | 0.822 | 0.818 | 0.030 | 0.000 | 0.000 | 0.217 | 0.015 | 4.338 |
| qdrant | is-tenant | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 31.6 |
| qdrant | one-segment | q-asrun | 3 | 0.644 | 0.639 | 0.012 | 0.000 | 0.002 | 0.380 | 0.045 | 4.436 |
| qdrant | one-segment | qa-acorn040 | 3 | 0.815 | 0.814 | 0.030 | 0.000 | 0.000 | 0.211 | 0.016 | 4.677 |
| qdrant | one-segment | qa-acorn100 | 3 | 0.815 | 0.814 | 0.030 | 0.000 | 0.000 | 0.211 | 0.016 | 4.624 |
| qdrant | one-segment | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 35.4 |
| qdrant | separate-kb | q-asrun | 3 | 0.952 | 0.948 | 0.010 | 0.000 | 0.000 | 0.042 | 0.001 | 7.641 |
| qdrant | separate-kb | qa-acorn040 | 3 | 0.952 | 0.948 | 0.010 | 0.000 | 0.000 | 0.042 | 0.001 | 7.617 |
| qdrant | separate-kb | qa-acorn100 | 3 | 0.952 | 0.948 | 0.010 | 0.000 | 0.000 | 0.042 | 0.001 | 7.769 |
| qdrant | separate-kb | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 34.6 |
| qdrant | tenant-m0 | q-asrun | 3 | 0.937 | 0.937 | 0.005 | 0.000 | 0.000 | 0.087 | 0.004 | 4.244 |
| qdrant | tenant-m0 | qa-acorn040 | 3 | 0.937 | 0.937 | 0.005 | 0.000 | 0.000 | 0.087 | 0.004 | 4.246 |
| qdrant | tenant-m0 | qa-acorn100 | 3 | 0.937 | 0.937 | 0.005 | 0.000 | 0.000 | 0.087 | 0.004 | 4.242 |
| qdrant | tenant-m0 | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 30.5 |

Qdrant's short answers with k = 5 (`summary_by_setting.csv`, q-asrun): 0.14% as run and 0.18% one-segment, none in the other
layouts; no empty answer in any layout. Qdrant search paths were read from the telemetry path
`result/collections/collections/shards/local/segments/vector_index_searches`.

## Against the first execution (2026-10-26)

Same code, seeds, settings and skipped items; values from the first execution's `report.md` and `x0/summary.md`.

- **P1 changed from confirmed to inconclusive.** The first execution had empty answers under p-asrun (ERR 0.000681, median
  20,083 rows emitted on an empty answer) and printed "confirmed"; the second had none, so P1's first criterion fails and
  the budget criteria cannot be judged. The paper judges P1 on run 2 (`x1-underretrieval-run2.md`), where it is
  inconclusive, with 393 empty answers under the forced HNSW plan.
- **pgvector's reference setting ran a different mix of plans.** Of p-asrun's 5,946 search executions
  (`x1/meta/pgvector__hnsw-m16-efc64__hnsw-m16-efc64-b0__p-asrun.json`, `prepared_statements`), the first execution ran
  5,852 with a generic plan and 94 with a custom plan, at recall@5 0.998; the second 4,308 and 1,638, at recall@5 0.907,
  recall@10 0.920 and gross miss 0.082. A generic plan reads the GIN index and sorts, which is exact; custom plans use the
  HNSW index (P5, run 2). Every raised-limit setting stayed at recall@10 0.999.
- **Qdrant, same picture, magnitudes within 0.06:** as run 0.619 and 0.641; ACORN 0.761 and 0.814; per-tenant graphs (tenant-m0)
  0.943 and 0.937; separate KB 0.948 and 0.948; company-document recall 0.273 and 0.314; hnsw_ef 512 minus 128 0.090 and
  0.097; short answers as run 0.6% and 0.14%, one-segment 1.1% and 0.18%.
- **Q3's one-segment criterion changed** (0.0121 [0.0012, 0.0228] then, -0.0025 [-0.0142, 0.0096] now); the verdict is
  inconclusive in both, because the one-segment layout ended with two segments both times.
- **P3:** median planner estimate over R for judys 11.1 then, 11.5 now; inconclusive in both (ph-exact skipped).
- **X0 re-analysis:** it re-analysed each execution's own X0 (`evidence/x0-scale-run.md`): pgvector's empty answers 10 then
  0; Qdrant's overlap@5 for KB readers 0.523 then 0.494; Qdrant's kb/ share on targeted questions 0.596 then 0.652.

## What this means for the paper

- Qdrant's under-retrieval has the structural cause of Q1 in both executions and in run 2: under the as-run layout the
  permitted subgraph is islanded; least-privileged people get recall@10 1.000 while company documents get 0.314 here; layout
  fixes it (tenant-m0 0.937, separate KB 0.948, against 0.641 as run); ACORN alone reaches 0.814.
- ACORN 0.4 engaged for every person and gave exactly ACORN 1.0's recall (Q2 falsified), in both executions.
- pgvector: run 1 supports the plan-cache picture (generic plans for 98.4% and 72.5% of the reference setting's searches in
  the two executions) and not, on its own, the budget mechanism, which rests on run 2.
- P2, P3 and P4 rest on partial data because the same 12 pgvector items were skipped by the deadline; P4's "falsified"
  comes only from the plan-inspection criterion (amendment 1). Q3 stays inconclusive because the one-segment layout did not
  take effect.
