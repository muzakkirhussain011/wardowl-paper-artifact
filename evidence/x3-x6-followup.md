# Evidence: X3 and X6 follow-up (amendment 4), GitHub Actions run 40982986417

Written 2026-10-30. Source: repository `muzakkirhussain011/wardowl`, workflow `paper-x3-x6`,
configuration `followup`, run 40982986417, attempt 1
(https://github.com/muzakkirhussain011/wardowl/actions/runs/40982986417), commit
`9e22b895c6323e9d5198ce150c415757680994aa` on branch `paper/x3-x6`, mode full. It read the data and
raw records of the full run 40940385704 from that run's artifacts. Read with git only, from branch
`results/x3-x6` at commit `c43ec34` ("results: paper-x3-x6 run 40982986417, attempt 1 (followup,
full)", published 2026-10-30T03:09:28Z), directory `40982986417-1/`: `reports/` (`fu_report.md`,
the `fu_*.csv` tables, `fu_crash_stacks.md`, and `x3_*` recomputed with Chroma's five seeds),
`logs/`, `jobs.json`, `crashes.jsonl`, `index.txt`. Every number below is as the scripts printed it;
"derived" marks simple arithmetic on printed numbers. Nothing here changes a verdict of run
40940385704 except the X3 verdicts that part A completes, as the pre-registration says it would.

## What was registered, and the runs

- **Amendment 4** to `benchmarks/paper/PREREG_X3_X6.md`, committed alone at `ba67dd8`
  (2026-10-30 02:31 +0300), states plainly that it was written after the full run's results were
  seen. Part A: Chroma's X3 seeds 3 and 4, exactly as written, with the time-share deviation removed
  and Python's fault handler on. Part B: six exploratory analyses, with the readings fixed before
  they ran (items 1 to 6 below).
- Follow-up code at `c4a838f` (scripts `x6_crossbuild.py`, `x3_chroma_bisect.py`,
  `x3x6_followup.py`; the workflow's `configuration` input, push default `followup`); full size at
  `fe3f177`; `/dev/shm` of the follow-up's PostgreSQL raised to 4 GB at `9e22b89`.
- Runs: **40974904217** (smoke, commit `c4a838f`, never analysed); **40978589778** (full, commit
  `fe3f177`, cancelled by us after its pgvector part failed: "DiskFull: could not resize shared memory
  segment ... to 1070648864 bytes" during a parallel HNSW build with five tables live under the main
  run's 1 GB `/dev/shm`; its partial folder `40978589778-1` was published by the always-run publish
  job and is not used); **40982986417** (full, the run analysed here).
- One unintended run: the push of amendment 4 itself started the workflow's then-default full
  configuration (run **40973718886**, commit `ba67dd8`). We cancelled it while queued; no job ran.
  Its folder `40973718886-1` holds only `index.txt` and `jobs.json` (every job "cancelled").

## What ran in run 40982986417, and what is missing

`jobs.json`: `followup` **failure**, `followup-analysis` success (the full configuration's jobs
skipped). The failure is one matrix job:

| job | outcome | records |
|---|---|---|
| fu-x3-chroma (part A) | ran, seeds 3 and 4 (each ended with signal 11 at G = 40,000, as expected) | `x3-chroma.jsonl`, 470 lines |
| fu-chroma-bisect (item 6) | ran, 7 child processes | `x3bisect-chroma.jsonl`, 18 lines |
| fu-cb-faiss (item 2) | ran, 5 seeds | `x6cb-faiss.jsonl`, 52,103 lines |
| fu-cb-pgvector (items 2, 5) | ran, 5 seeds | `x6cb-pgvector.jsonl`, 26,744 lines |
| fu-cb-qdrant (item 2) | ran, 5 seeds | `x6cb-qdrant.jsonl`, 26,183 lines |
| **fu-cb-elasticsearch (item 2)** | **lost**: the job's run step has no conclusion, its log blob does not exist ("BlobNotFound"), and its only annotation reads "The hosted runner lost communication with the server. Anything in your workflow that terminates the runner process, starves it for CPU/Memory, or blocks its network access can cause this error." It ran from 01:01 to 02:12 UTC and uploaded nothing. | none |

**Missing because of it:** the cross-build A/A for Elasticsearch `pre-exact` (part of item 2's
scope). None of the three readings amendment 4 fixed (FAISS `post` at m = 1, FAISS `pre`, pgvector
`pre-exact`) needs Elasticsearch, so they are complete. Elasticsearch's part would need a rerun of
that one job. The cause is not in any published output; memory pressure is a candidate (five
Elasticsearch indexes with their keyword fields under a 2 GB heap, beside the harness holding five
sets of documents), which a rerun would need to rule out first. Not rerun here.

## Part A: Chroma's X3 seeds 3 and 4, and the X3 verdicts with five seeds

Log of `fu-x3-chroma` (published tail): seed 3 built in 129 s, G = 1, 10, 100 "ok, 0 errors", G =
1,000, 4,000, 10,000 "refused, 30 errors", then "Fatal Python error: Segmentation fault" and
"seed 3: the process ended with status -11"; seed 4 built in 136 s, the same sequence, status -11.
The fault handler printed, for both seeds, the innermost Python frame as
`chromadb/api/rust.py, line 582 in _query`, called from `chromadb/api/models/Collection.py, line 265
in query`, from `wardowl/backends/chroma.py, line 233 in search`. `crashes.jsonl`: driver status 6
for the job (a seed process died), per seed -11.

`x3_stats.py`, unchanged, over run 40940385704's X3 records and these two seeds (57,462 records):

- **X3-H1 confirmed**: 84 confirmed, 0 falsified, 0 inconclusive parts (it was inconclusive, 77/0/7,
  in run 40940385704 for want of Chroma's seeds). Chroma's translator, five seeds: median 0.0, 0.0,
  0.1, 1.1, 4.4, 12.0 and 100.9 ms at G = 1 to 40,000.
- **X3-H2 Chroma confirmed**: "observed refuses in 5 seeds, ok share nan, first error the process
  crashed, exit status -11".
- **X3-H4 Chroma inconclusive**: "no accepted level pair" (the rule needs an accepted level of at
  least 1,000 groups; Chroma accepts only up to 100).
- Chroma per level, five seeds: G = 1 accepts, p50 4,340 ms; G = 10 accepts, 5,005 ms; G = 100
  accepts, 10,627 ms; recall 1.000; G = 1,000, 4,000, 10,000 refuse with "InternalError: Error
  executing plan: Internal error: error returned from database: (code: 1) Expression tree is too
  large (maximum depth 1000)" (150 errors each); G = 40,000 refuses through the crash (crashed seeds
  5 of 5). Health row: retrievals 1,050, errors 450, crashes {0, 1, 2, 3, 4: -11}; it still lists
  "skipped [3, 4]" from run 40940385704's records, which is that run's history, not a gap.
- **Every other store reproduces run 40940385704**: `x3_levels.csv`, `x3_ratios.csv`,
  `x3_recall.csv`, `x3_errors.csv` and `x3_verdicts.csv` are identical without Chroma's rows, except
  one recall interval bound of pgvector at G = 100 (0.9553333333333334 against 0.9553333333333333,
  floating-point order) and the X3-H1 verdict line.

## Item 1: where FAISS's m = 1 latency difference lies (run 40940385704's records)

FAISS `post`, W1 against W0, medians per (seed, probe, p) over the timed repetitions, pooled over p
(360 pairs, 120 clusters; 10,000 resamples):

| m | component | mean W1 (ms) | mean W0 (ms) | difference [95% interval] | paired AUC [interval] | share equal |
|---|---|---|---|---|---|---|
| 1 | latency | 23.652 | 23.545 | 0.106 [0.067, 0.146] | 0.667 [0.614, 0.717] | 0.000 |
| 1 | search_ms (FAISS) | 21.768 | 21.653 | 0.115 [0.076, 0.154] | 0.681 [0.628, 0.733] | 0.000 |
| 1 | authorize_ms | 1.383 | 1.384 | -0.001 [-0.002, 0.001] | 0.465 [0.412, 0.519] | 0.092 |
| 1 | rest of the layer | 0.495 | 0.504 | -0.010 [-0.017, -0.003] | 0.444 [0.392, 0.497] | 0.008 |
| 1 | widening rounds | 2.433 | 2.433 | 0.000 [0.000, 0.000] | 0.500 | 1.000 |
| 10 | latency | 24.017 | 23.034 | 0.984 [0.661, 1.337] | 0.672 [0.617, 0.725] | 0.000 |
| 10 | search_ms | 22.104 | 21.202 | 0.902 [0.618, 1.215] | 0.700 [0.647, 0.750] | 0.000 |
| 10 | authorize_ms | 1.409 | 1.344 | 0.065 [0.039, 0.095] | 0.429 [0.378, 0.481] | 0.014 |
| 10 | rest | 0.504 | 0.485 | 0.020 [0.011, 0.029] | 0.542 [0.494, 0.589] | 0.006 |
| 10 | widening rounds | 2.486 | 2.406 | 0.081 [0.053, 0.111] | 0.540 [0.526, 0.556] | 0.919 |

Per selectivity at m = 1, the search difference was 0.166 [0.066, 0.267] ms at p = 1%, 0.129 [0.079,
0.179] at 10% and 0.050 [0.029, 0.070] at 50%, with rounds equal in every pair.

**Reading (fixed in advance):** at m = 1 the rounds are equal in all 360 pairs, the authorizer and
the rest of the layer show no difference in W1's direction, and the whole difference lies in FAISS's
own search call: the time FAISS took to scan the same number of vectors differed between the two
index objects. At m = 10, 8.1% of pairs had unequal rounds (derived: 1 - 0.919), W1 doing more:
there the denial path adds to the same offset.

## Item 2: cross-build A/A (this run)

Slots per group: W1 (built at the seed's start), W1r (W1 rebuilt), W0a and W0b (W0_g built twice),
the three late builds in a seeded random order; four slots per repetition in random order; five
seeds, eight groups, every probe and attacker, one warm-up and five repetitions. Paired latency
AUC, the first slot against the second, pooled over p (120 clusters at m = 1, 360 pooled):

| store, config | m | replication W1 vs W0a | age W1 vs W1r | matched content W1r vs W0a | cross-build A/A W0b vs W0a | reading (amendment 4) |
|---|---|---|---|---|---|---|
| FAISS post | 1 | 0.597 [0.539, 0.656] | 0.600 [0.547, 0.653] | 0.447 [0.392, 0.506] | 0.361 [0.308, 0.414] | inconclusive |
| FAISS pre | all | 0.293 [0.260, 0.326] | 0.426 [0.392, 0.460] | 0.384 [0.342, 0.428] | 0.257 [0.227, 0.288] | inconclusive |
| pgvector pre-exact | all | 0.202 [0.179, 0.225] | 0.186 [0.163, 0.209] | 0.567 [0.530, 0.602] | 0.789 [0.759, 0.818] | inconclusive |
| Qdrant pre-exact (no reading fixed) | all | 0.493 [0.465, 0.522] | 0.494 [0.465, 0.524] | 0.498 [0.469, 0.528] | 0.505 [0.476, 0.533] | n/a |
| Elasticsearch pre-exact | all | lost (runner) | lost | lost | lost | not measured |

The rule: "supported" when the matched-content interval lies within [0.40, 0.60] and the age or the
cross-build A/A interval lies wholly outside it; "refuted" when the matched-content interval lies
wholly outside [0.40, 0.60] on the main run's side while age and A/A both lie within it. All three
fixed readings print **inconclusive**: for FAISS `post` at m = 1 the matched-content interval reaches
0.392, below 0.40; for FAISS `pre` it is 0.342 to 0.428; for pgvector it reaches 0.602, above 0.60.

What the numbers show, beyond the formal reading:

- **FAISS `post`.** The replication reproduces the main run's direction, more weakly (0.597 against
  0.667). Two builds of identical content differ by as much: age 0.600 and cross-build A/A 0.361
  (the later build faster), and these same-content offsets are the same at every m (age 0.600,
  0.597, 0.608, 0.592 at m = 1, 10, 100, 1,000; A/A 0.361, 0.364, 0.362, 0.342). With builds matched
  in time, the content difference gives 0.447 at m = 1 and 0.494 at m = 10 (no offset in W1's
  direction), but 0.692 at m = 100 and 0.742 at m = 1,000, where the widening channel is real: the
  design detects content when there is content to detect. Mean latency at m = 1: W1 23.253, W1r
  23.204, W0a 23.239, W0b 23.129 ms. Answers identical in every m = 1 pair of every contrast
  (`ids_identical` 1.000).
- **FAISS `pre`.** The replication reproduces the main run (0.293 against 0.276). W0a, the first
  W0 build, is the slowest of the four: W1 vs W0a 0.293, W1r vs W0a 0.384, W0b vs W0a 0.257, while
  W1 vs W1r is 0.426. Not explained further.
- **pgvector `pre-exact`.** The replication reproduces the main run's direction (0.202 against
  0.147), and the same content rebuilt late is as slow relative to W1 (age 0.186). The second W0
  build is much slower than the first (A/A 0.789). Mean latency pooled over m and p: W1 59.888 ms,
  W0a 61.391, W1r 74.262, W0b 107. Item 5 explains this.
- **Qdrant `pre-exact`** shows no difference between builds in any contrast.

## Item 3: hubs, probe by probe (run 40940385704's data and records)

The hub set recomputed from the embeddings equals the data job's ("same": true: 576 hubs, count
threshold 901, maximum 2,052, median 179, expected 230.7). For the 40 m = 1,000 probes:

- hubs among the 1,000 nearest passages: 1 to 231, mean 45.70, median 24.5 (derived with awk from
  `fu_hubs.csv`); passages among them that are neither hubs nor secrets: 0 in every probe;
- **FAISS `post` returned exactly min(10, readable hubs among the 1,000 nearest) in W1 for 40 of 40
  probes at every p**, and exactly min(10, readable passages among W0_g's 1,000 nearest) in W0 (share
  equal 1.000 in all six cells; means 0.375, 3.350, 7.600 in W1 and 7.675, 10, 10 in W0);
- W1 answers full at p = 50%: 25 of 40 probes; at p = 10%: 6 of 40; no readable passage at all at
  p = 1%: 30 of 40 (derived counts from `fu_hubs.csv`);
- the approximate stores, whose 1,000 candidates are not exactly the nearest: share of probes equal
  to the count in W1 at p = 1, 10, 50%: Qdrant 1.000, 0.925, 0.950; pgvector 0.925, 0.700, 0.775;
  Elasticsearch 0.900, 0.650, 0.700 (pgvector and Elasticsearch returned more hits on average: 8.6
  and 9.025 against 7.6 predicted at p = 50%).

The prediction amendment 4 fixed holds without exception. Only the similarity columns of `fu_hubs.csv`
differ from the smoke run's copy, in the seventh decimal (floating-point order); every count is
identical.

## Item 4: pgvector's X3 plans (run 40940385704's 35 explain records)

Every level, every seed: `Incremental Sort / Limit / Index Scan (the table's embedding_hnsw index) /
CTE Scan`. The GIN index was never used, not even with one group. Rows removed by the filter for each
seed's first question: 142, 70, 85, 90, 55 (seeds 0 to 4), the same at every G; rows returned 10;
removed by recheck 0. Execution time of that first question (ms):

| G | seed 0 | seed 1 | seed 2 | seed 3 | seed 4 |
|---|---|---|---|---|---|
| 1 | 2.564 | 1.134 | 1.415 | 1.585 | 1.314 |
| 10 | 2.771 | 1.322 | 1.639 | 1.802 | 1.359 |
| 100 | 3.763 | 1.775 | 2.283 | 2.390 | 1.859 |
| 1,000 | 17.482 | 9.133 | 10.989 | 11.430 | 7.704 |
| 4,000 | 60.838 | 31.157 | 38.158 | 39.913 | 25.891 |
| 10,000 | 145.106 | 75.121 | 90.801 | 96.805 | 60.329 |
| 40,000 | 566.073 | 294.521 | 355.046 | 373.719 | 239.375 |

Derived: at 40,000 groups, execution time divided by the rows the scan tested (rows removed plus the
10 returned) is 3.72, 3.68, 3.74, 3.74 and 3.68 ms per row in seeds 0 to 4: the per-row filter test
costs the same in every seed and grows with G. The pre-registered rationale (above 100 values the
GIN index cannot serve the filter) did not decide the result, since the planner chose the HNSW scan
at every level; the 272-fold growth is the cost of testing each scanned row against a longer filter.

## Item 5: pgvector `pre-exact` on W1 and W0_g

**The main run's plans** (run 40940385704, first group of each seed, taken after that group was
measured): the same plan on W0_g and W1 for every level and attacker (`Incremental Sort / Limit /
Sort / Bitmap Heap Scan / BitmapOr / Bitmap Index Scan` on the metadata GIN index, with a `Gather
Merge` at p = 50% in some cases), and nearly equal execution times (for example seed 0, m = 1:
1.485 against 1.378 ms at p = 1%, 17.498 against 16.968 at 10%, 78.641 against 78.457 at 50%).

**This run's table states** (`fu_pg_state.csv`, 5 seeds x 8 groups x 4 tables, before and after
each group was measured; counts derived with awk):

| table, by build order | before the group: no all-visible page | after the group: none |
|---|---|---|
| W1 (built at the seed's start) | 0 of 40 | 0 of 40 |
| second-to-last late build | 13 of 40 | 0 of 40 |
| last build before the group | 40 of 40 | 5 of 40 |

By slot, before the group: W1 0 of 40, W0a 4, W1r 15, W0b 34. An unvacuumed table showed
`relallvisible` 0, `n_ins_since_vacuum` 57,638 and `autovacuum_count` 0; after autovacuum,
all-visible pages equal (or nearly equal) the page count (for example 9,206 of 9,224). In the main
run the table built just before each group was W0_g.

**This run's plans with buffers** (first group of each seed, after it was measured, when every table
had been vacuumed): identical plans, buffer counts and times on the four tables (for example seed 0,
m = 1, p = 10%: 64,689 to 64,699 shared hits, 3,864 to 3,866 exact heap blocks, 26.277 to 26.357
ms). No EXPLAIN was taken on an unvacuumed table in this run.

**Reading.** The prediction stated in amendment 4 holds for the pages: the tables built just before
a group start without all-visible pages and W1 never does. The latency follows the vacuum state: mean
exact-search latency 59.888 ms on W1 (never unvacuumed at a group's start), 61.391 and 74.262 ms on
W0a and W1r (unvacuumed in 4 and 15 groups), 107 ms on W0b (34 groups). Once vacuumed, the tables
plan and run alike. The main run's pgvector `pre-exact` offset (W0_g slower, 0.147) is therefore a
property of when the table was built and vacuumed, not of the secrets. A residual remains: W0a,
mostly vacuumed, was still slower than W1 in most pairs (replication 0.202) though by 1.5 ms on
average; not explained.

## Item 6: Chroma's crash threshold and location

Seed 0's X3 corpus (100,000 vectors), the subject holding the first G of the 40,000-level groups,
one retrieval per fresh process (build 93.5 to 96.0 s each):

| G | result | exit status | where-document size (characters) | translation ms |
|---|---|---|---|---|
| 40,000 | crash | -11 | 2,657,983 | 34.248 |
| 25,000 | crash | -11 | 1,652,983 | 19.844 |
| 17,500 | crash | -11 | 1,150,483 | 11.792 |
| 13,750 | error: "Expression tree is too large (maximum depth 1000)" | 0 | 899,233 | 9.239 |
| 15,500 | error, the same message | 0 | 1,016,483 | 10.237 |
| 16,500 | crash | -11 | 1,083,483 | 11.177 |
| 40,000, under gdb | crash (SIGSEGV) | 0 (gdb) | 2,657,983 | 34.248 |

**Threshold:** between 15,500 groups (refused with SQLite's error after 4,474.9 ms) and 16,500
(signal 11). The cancelled run 40978589778 bisected to the same bracket.

**Location.** The fault handler (every crashing level) put the crash in `chromadb/api/rust.py, line
582 in _query`, Chroma's call into its native core. Under gdb: "Thread 1 "python" received signal
SIGSEGV, Segmentation fault." in `chromadb_rust_bindings.abi3.so`; frames #1 to #39 all return to the
same address in that library (`0x00007fffbad9a46c`), and the stack runs to frame #16535 (`_start`),
the outermost frames being the Python interpreter's. The other threads (tokio workers, an
`sqlx-sqlite` worker) were waiting. So the main Python thread was about 16,500 frames deep in one
recursive function of Chroma's Rust bindings when it ran out of stack, before SQLite could see the
query. The frame count matches the clause count at the threshold (a disjunction of G + 2 clauses), as
one frame per clause would give; that correspondence is inferred, not shown by a symbol.

## What this changes in the paper

- side.tex, H1(a): the hub mechanism holds probe by probe (exact for FAISS), replacing "about 35
  hubs"; hub counts 1 to 231, mean 45.7.
- side.tex, H1(c): the m = 1 difference lies in FAISS's search call with equal rounds; the
  cross-build run shows same-content builds differing as much as W1 and W0_g; the fixed reading is
  inconclusive (matched content 0.447, 0.392 to 0.506).
- side.tex, H4: pgvector's offset follows the vacuum state; Qdrant shows no build differences;
  Elasticsearch's cross-build part was lost.
- quality.tex: X3-H1 confirmed (84/0/0) and X3-H2 confirmed for Chroma with five seeds; X3-H4 for
  Chroma inconclusive; the table's Chroma row over five seeds; pgvector's plans (HNSW scan at every
  level, the same rows removed); the crash location and the 15,500 to 16,500 bracket.

## Still open

1. **Elasticsearch cross-build A/A**: lost with its runner; needs that one job again (exploratory;
   no fixed reading depends on it).
2. **FAISS's build offset** has no mechanism beyond "the index object" (memory placement is a
   candidate; not measured), and the pre-stated reading is inconclusive.
3. **pgvector's residual** W0a-against-W1 difference after vacuum (1.5 ms on 60 ms): not explained.
