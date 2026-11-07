# Investigation: why X1 did not reproduce X0's pgvector numbers

> Note added 2026-11-07: the X0 numbers in this note are the printed aggregates of X0's first execution (2026-10-24), then
> described in `evidence/kaggle-scale-run-2026-10-24.md`. The artifact now holds X0's second execution
> (`evidence/x0-scale-run.md`), in which pgvector also ran in its fast mode (recall@5 0.703, recall@10 0.725, p50 7.8 ms) but
> returned no empty answer, and Qdrant reached recall@5 0.537 and recall@10 0.530. The reasoning below is unchanged.

Written 2026-10-29. Analysis of code and of published results. Inputs: `evidence/kaggle-scale-run-2026-10-24.md`
(X0), `evidence/x1-underretrieval-run1.md` (X1 run 1), `investigations/filtered-recall-gaps.md` (the
diagnosis written before X1), `evidence/raw/x8-seed13/` (X8 seed 13: X0's exact configuration rerun,
seed 13, Kaggle T4 x2), `evidence/raw/x8-seed11/` (the same with seed 11), and the run-2 smoke kernel's records (section 3, H2a).

Conventions:

- **Code references** are `file:line`. `enterprise_rag.py` means `acceptance/kaggle/enterprise_rag.py`
  and `pgvector.py` means `wardowl/backends/pgvector.py`; both are identical at X0's commit `bf25bd0`
  (tag v2.1.0) and at X1 run 1's commit `947fb8f` (`git diff --stat bf25bd0 947fb8f` lists no change
  to either). `x1@947fb8f` means `benchmarks/paper/x1_underretrieval.py` as run 1 ran it (the file has
  changed since, for run 2).
- **Store and library references** are to source at the versions the runs used: PostgreSQL 16
  (`REL_16_STABLE`; X0 reported 16.15), pgvector `v0.8.7`, psycopg 3.3.6 (X1's; X0's version is in its
  `results.json`, not in the evidence file).
- **[unverified]** marks an inference or estimate not confirmed from code, docs or data.
  **[derived]** marks a number computed from published results, not printed by a run.

---

## 1. Summary

X1 run 1 did not measure what X0 measured. In X1, almost every pgvector search ran a PostgreSQL
**generic plan**, and that plan does not use the HNSW index: it reads the rows the GIN index on
`metadata` returns and sorts them by distance, which is an exact search. X0's searches used the HNSW
index. That one difference explains both numbers at once: X1's recall@5 of 0.998 (exact, apart from
about ten searches per statement) and its p50 of 391 ms (an exact scan over tens of thousands of
rows), against X0's 0.691 and 6.5 ms.

- **The mechanism is in the code path both runs share.** wardowl binds every filter value and the
  LIMIT as parameters (`pgvector.py:41-94`, `:290-296`). psycopg prepares a statement on its sixth
  execution on a connection, and PostgreSQL then plans the first five executions of the prepared
  statement with their values (custom plans). After that it switches to a generic plan whenever the
  generic plan's estimated cost is below the custom plans' average, and it keeps that decision
  (`plancache.c`, `choose_custom_plan`). A generic plan cannot see the jsonb values or the LIMIT,
  so it assumes a very selective filter and a LIMIT of 10% of the rows, and prefers GIN plus a sort.
- **X1 measured this directly.** Under `p-asrun`, PostgreSQL ran the search statement with a generic
  plan 5,852 times, out of about 5,966 searches. For all 50 fixed questions, the generic plan had
  another shape than the custom plan EXPLAIN showed. Recall and latency did not move with
  `ef_search` (40 to 400), `max_scan_tuples` (20,000 to 1,000,000), scan memory or `work_mem`. Those
  settings only act on an HNSW scan.
- **X0 is the outlier, not X1.** X8 seed 13 reran X0's exact configuration: wardowl 2.1.0 from
  PyPI, acceptance scripts at `bf25bd0`, PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1),
  pgvector 0.8.7, psycopg 3.3.6, Python 3.13.15; only `Config.seed` 13 differed. Its pgvector
  numbers look like X1's, not X0's: recall@5 and @10 0.994, p50 386.0 ms (p95 421.4, p99 436.8),
  16,351 hits checked, and no failed empty-result check. Under OPA, on the same table and
  connection pool, recall was 1.000 at a p50 of 389.5 ms. Its log shows the slow pace from the
  first 250 questions on (162 s for 250, about 0.32 s per search) [derived]. X8 seed 11 (same
  configuration, seed 11, `evidence/raw/x8-seed11/`) did the same: recall@5 and @10 0.992, p50
  398.7 ms (p95 438.0, p99 454.3), 16,345 hits checked, 172 s for the first 250 questions, and
  pgvector + OPA at 1.000 and 407.6 ms. It also had one empty result (`tailspin-judy`; the check
  "everyone who may read something got results" failed for that one person). That fits one lossy
  custom-plan HNSW search among the first ten executions of a statement, like X1 run 1's single
  empty [inference]. So of three runs of X0's configuration, one (X0) ran HNSW custom plans and
  two (seeds 11 and 13) ran the exact generic plan, as X1 run 1 did.
- **Why X0 kept custom plans is not settled by the code.** The runs share the SQL, backend, session
  settings, index build and versions. The leading candidate is that the planner's cost of the GIN
  path depends on the state of the GIN index (its pending list and its statistics), which only
  VACUUM, including autovacuum, updates. The switch decision is taken once per statement and
  connection, seconds after the bulk load, and never revisited (section 3, H2a). The run-2 smoke
  run showed this switch flip with a VACUUM on a small corpus. Run 2 records that state and replays
  X0's pass to test it on the full corpus.
- **Consequences.** Run 1's P-a, P-b and P-c results describe the generic exact plan, not the HNSW
  scan that P1 and P2 are about. The mechanism behind P1 rests on a single custom-plan search. The
  Qdrant results are unaffected. For the paper, wardowl's default pgvector path through psycopg is
  bimodal: either fast and lossy (X0: recall@5 0.691 at 6.5 ms) or exact and about 60 times slower
  (X1, X8), decided by the plan cache in the first seconds of a connection. X0's pgvector numbers
  are not a stable property of the configuration and should not be reported as one. Run 2
  (amendment 2) records the plan every search executed, forces the HNSW scan where the hypotheses
  need it (`pg-hnsw`, P-a to P-e), leaves the planner its choice in `pg-custom`, and replays X0's
  pass.

---

## 2. What differs between X0's pgvector pass and X1's `p-asrun`

| Aspect | X0 (2026-10-24, `notebookd8377caca8`) | X1 run 1, `p-asrun` (2026-10-26, `notebook11401c38ff`) | Same? |
|---|---|---|---|
| PostgreSQL, pgvector | 16.15; pgvector v0.8.7 built by `benchmarks/kaggle_setup.sh:6,14-17`, `PG_TUNE=1` | same script and version; server version in run 1's manifest (`stages."pgvector: start and load".server`), not read here | yes [16.x for X1 unverified] |
| Server settings | `PG_TUNE=1`: `shared_buffers` 4 GB, `effective_cache_size` 16 GB, `max_parallel_workers_per_gather` 2 (`kaggle_setup.sh:20-26`); `maintenance_work_mem` 2 GB and 3 parallel maintenance workers for the build (`enterprise_rag.py:1195-1197`); `work_mem` 4 MB, `plan_cache_mode` auto, `enable_seqscan` on (defaults) | same calls (`enterprise_rag.PgVectorStore.start`/`load`, `x1@947fb8f:1125-1126`); recorded by `server_info` (`x1@947fb8f:1142-1172`) | yes |
| Table and indexes | `create_schema(hnsw=False)` (table and GIN `jsonb_path_ops` on `metadata`), bulk load, then `create_schema(hnsw=True)` (HNSW `vector_cosine_ops`, pgvector's defaults m 16, ef_construction 64), then `ANALYZE` (`enterprise_rag.py:1199-1205`, `pgvector.py:169-184`) | build b0 reuses that very index, unchanged (`x1@947fb8f:1233-1238`) | yes |
| Index at query time | exists and was used (p50 6.5 ms) | exists; custom-plan EXPLAINs show it in use (P1: 20,083 rows emitted); the searches' generic plans did not use it | **no**: the plan differs |
| Session settings | `SET LOCAL hnsw.iterative_scan = 'relaxed_order'`, `SET LOCAL hnsw.ef_search = 100` per search (`pgvector.py:325-336`, `enterprise_rag.py:1216-1219`); `max_scan_tuples` 20,000 and `scan_mem_multiplier` 1 (pgvector defaults) | the same two statements, nothing added for `p-asrun` (`x1@947fb8f:111`, `:177`, `:260-266`) | yes |
| SQL | `WITH candidates AS MATERIALIZED (SELECT ... WHERE <filter> ORDER BY distance LIMIT $k) SELECT ... ORDER BY distance, id`; filter values and k bound as parameters (`pgvector.py:41-94`, `:284-296`) | the backend's own SQL (`x1@947fb8f:268-270`, limit factor 1) | yes |
| Prepared statements | psycopg default `prepare_threshold` 5 on the load's pool (`ConnectionPool(url, min_size=1, max_size=4)`, `enterprise_rag.py:1198`) | psycopg default 5 on a fresh pool of one connection per setting (`x1@947fb8f:1270-1275`) | same rule; X0's pool in practice used one connection [psycopg_pool grows only when no connection is free; unverified for X0] |
| Plan PostgreSQL used | custom plans with the HNSW index, by the evidence (latency; recall; identical numbers under OPA) | generic plans for 5,852 of about 5,966 searches; first ~10 executions per statement custom | **no** |
| Retrieval strategy | prefilter for all 1,105 (`evidence`, "prefilter 1105") | prefilter (wardowl's `PermissionedRetriever`, `x1@947fb8f:879`) | yes |
| k | k=5, then k=10, two calls per question (`enterprise_rag.py:1952-1954`) | k=5 and k=10 in pass 1, k=5 again in passes 2 and 3 (`x1@947fb8f:898-906`); recall@5 from pass 1 | yes for recall; X1 executes each statement more often |
| Order | all questions shuffled with seed 7 (`enterprise_rag.py:1934-1935`) | people in a seeded order, each asking all their questions (`x1@947fb8f:808-812`, `:880`) | no (matters only for which searches fall in the first ten per statement) |
| Warm-up | 10 searches, k=5 (`enterprise_rag.py:1936-1938`) | 10 searches, k=5 (`x1@947fb8f:881-887`) | yes |
| Questions | 1,105 (generic 108, targeted 376, forbidden 189, red team 432); 1,084 scorable | the same 1,105 plus 384 probe questions (`x1@947fb8f:619-661`): 1,489; 1,468 scorable [derived] | no; the probes cannot lift 0.69 to 0.998 |
| People | 189 | 189 plus 24 single-group probes: 213 | no; the probes share SQL texts with people of the same filter shape |
| Embeddings | BAAI/bge-base-en-v1.5, fp16 on a T4, unit length (`enterprise_rag.py:1788-1827`, `:1603-1610`) | chunk vectors copied from X0's cache when attached (`x1@947fb8f:663-672`); query vectors encoded again the same way | chunks yes; queries nearly [difference size unverified, far too small to matter] |
| Ground truth | exact top 10 over each person's readable rows on the GPU (`enterprise_rag.py:1845-1877`) | the same function (`x1@947fb8f:595-597`) | yes |
| Recall | share of the exact top k among the first k hits, ties within 1e-4 credited (`enterprise_rag.py:2082-2096`) | the same function (`x1@947fb8f:1001`) | yes |

A correction to the brief: X0's 0.691 is the run's own tie-credited recall against the GPU exact
baseline, not an overlap with FAISS. The FAISS overlap@5 without tie credit (0.870 and 0.550 by
category group) is X0's re-analysis, `x0_reanalysis.py`, a different metric.

---

## 3. Ranked hypotheses

### H1 (established): X1's searches ran generic plans that do not use the HNSW index

**Evidence from X1's own records (run 1):**

- `pg_prepared_statements` after `p-asrun`: 5,852 generic executions of the search statement
  (`x1@947fb8f:1315-1334`, counted for statements containing `WITH candidates`). A setting runs
  10 + 1,489 x 4 = 5,966 searches [derived]. The difference, 114, matches about 11 distinct SQL texts
  (one per filter shape) times 10 custom executions each: five before psycopg prepares, then five
  custom plans before PostgreSQL considers a generic one [derived].
- For all 50 fixed questions, `EXPLAIN (GENERIC_PLAN)` (`x1@947fb8f:1373-1388`) gave another shape
  than EXPLAIN ANALYZE with the values (`x1@947fb8f:1390-1400`). The latter always shows a custom plan.
- Recall, ERR and latency were flat across `pc-ef40/200/400`, `pa-*`, `pb-wm64` (p50 378 to 394 ms;
  recall@10 0.9986 to 0.9994). These parameters change only an HNSW scan.
- The one empty result (ERR 0.000681 = 1 of 1,468 [derived]) fits a search among the first ten
  executions of its statement, which ran a custom HNSW plan. With the same person order, the
  same search was again among the first ten in the `pa-*` settings: the raised tuple limits removed
  it, and the memory-only raises (`pa-t20k-m8`, `pb-wm64`) did not.

**Mechanism, from source:**

- psycopg prepares a query after `prepare_threshold` (5) executions with the same text and parameter
  types (`psycopg/_preparing.py`, `PrepareManager.get`). wardowl runs the search with `conn.execute`
  inside a transaction (`pgvector.py:348-351`), so the same text recurs for every person with the
  same filter shape.
- PostgreSQL makes custom plans for the first five executions of a prepared statement, then uses the
  generic plan when `generic_cost < avg_custom_cost` (`plancache.c:1059-1075`, REL_16_STABLE). Once
  the generic plan wins, no more custom plans are made, so the average never moves again.
- In the generic plan, `metadata @> $n` gets `matchingsel`'s default selectivity of 0.010 per test,
  because the value is not a constant (`pg_operator.dat:3223-3225`; `selfuncs.c:1011`, `:3229-3250`).
  wardowl's filter is an AND of ORs of such tests, so the planner expects about 0.1% of the table
  [derived from the filter shape in `pgvector.py:55-94`].
- `LIMIT $k` cannot be estimated, so the planner costs it as 10% of the rows (`planner.c:2553`,
  `:2590-2591`).
- An HNSW index scan costs a fixed share of a whole-index scan before its first row: about 0.0128 for
  107,540 rows, m 16 and `ef_search` 100 (`hnsw.c:197-215`) [derived]. For 10% of a filter
  expected to pass ~100 rows, the planner prefers a bitmap scan on the GIN index plus a sort, which
  computes every candidate's distance: an exact search.
- Rough costs, consistent with the switch [derived estimates, unverified]: about 2,800 to 3,100 for a
  custom HNSW plan with `LIMIT 5`, about 10^3 for the generic GIN plan.
- **Still to read:** the generic plan's actual shape and costs. Run 1 saved them in
  `x1/explain/pgvector__hnsw-m16-efc64__hnsw-m16-efc64-b0__p-asrun.parquet` (column
  `generic_plan_shape`) and `x1/explain_raw/...p-asrun.jsonl.gz` (`generic_plan`). Run 2 records the
  executed plans directly.

**Fit with the latency.** For a typical person the filter passes about 58,000 rows. An exact plan
reads and detoasts that many 768-dimension vectors and computes their distances; 391 ms is
plausible for that [unverified], while judys' 624 rows are fast. X0's p95 of 47 ms and p99 of 75 ms
look like the deeper iterative HNSW scans of selective filters, not exact scans.

### H2: why X0 kept custom HNSW plans

That X0 used HNSW is well supported: its p50 of 6.5 ms, its recall of 0.691, and identical recall
(0.691 and 0.732) and the same ten empty people under the OPA pass. Both passes ran the same
deterministic custom plans. X8 seeds 11 and 13 show that the same configuration usually does not (see
the summary), so the question is what made X0's first decisions go to custom plans. Candidates,
ranked:

**H2a (most likely; mechanism shown on the smoke corpus, unverified for X0 itself). The decision is
sticky and depends on the GIN index's state when it is first taken.**

- The GIN index is created on the empty table before the bulk load (`enterprise_rag.py:1199`,
  `pgvector.py:175-177`), with `fastupdate` on by default. New entries go to a pending list, which
  is flushed when it passes `gin_pending_list_limit` (4 MB), and otherwise only by VACUUM,
  including autovacuum.
- A manual ANALYZE does not flush it. `ginvacuumcleanup` returns early for ANALYZE unless it runs in
  an autovacuum worker (`ginvacuum.c:740-748`). The load ends with a manual ANALYZE
  (`enterprise_rag.py:1204-1205`).
- The planner charges every pending page as a random page read, for every GIN index scan
  (`selfuncs.c:7710`, `:7800-7804`). The GIN statistics in the metapage are also only as current as
  the last VACUUM. Before any VACUUM, the planner invents them from the index size.
- With a few hundred pending pages, each GIN scan in the generic plan costs more than the whole
  custom HNSW plan [derived estimate]. The generic plan then loses at the first comparison.
- PostgreSQL keeps the generic plan's cost and the custom plans' average across invalidations: "we
  do not reset generic_cost or total_custom_cost" (`plancache.c:782-789`). Once custom plans win
  the first comparison, the generic plan is never rebuilt, so the decision stays for the life of
  the connection.
- In X0 that decision was taken seconds after the load. In X1 run 1 it was taken at about the same
  point for `p-asrun`, so H2a needs the GIN state to have differed by chance. That is possible
  [unverified]: autovacuum runs (and when one falls during the 63-second load) shift the 4 MB flush
  cycle, so the pending list left at the end of the load can be anywhere from empty to 4 MB.
- **First support (smoke run, 2026-10-29, small corpus only).** The run-2 smoke kernel
  (`x1run2-smoke`, version 1; about 3,000 chunks, so its numbers are not
  results) recorded the switch on both sides of a VACUUM:

  | Replay | GIN state before | Generic / custom executions | HNSW share of plans |
  |---|---|---|---|
  | `p-x0`, right after the load | 152 pending pages; statistics never set by VACUUM (`n_entries` 0, `n_total_pages` 2) | 12 / 83 | 0.66 |
  | `p-x0v`, after `VACUUM (ANALYZE)` | 0 pending pages; `n_entries` 1,150, `n_total_pages` 174 | 156 / 49 | 0.04 (GIN plus sort) |

  In that run, `p-asrun` on a build that saw no VACUUM (shard B) also kept custom HNSW plans, as
  X0 did. On the vacuumed build (shard A) it switched to generic GIN plans, as X1 run 1 did. This
  is the mechanism H2a proposes. On the full corpus it is untested until run 2.
- **Against or open:** neither X0 nor X1 run 1 recorded the pending list, the autovacuum history
  or the generic plan's cost at decision time, so whether this is what happened in those two runs
  cannot be shown. The full-corpus cost figures are estimates.
- **Test:** run 2's `p-x0` replays X0's pass on the load's own pool, right after the load, and
  records the GIN metapage (pending pages, statistics) and the autovacuum history before and
  after. `p-x0v` replays it after `VACUUM (ANALYZE)`. H2a predicts generic plans and recall near
  1.0 under `p-x0v`, and custom plans under `p-x0` whenever the pending list is large.

**H2b (ruled out for the versions X8 shares with X0). A version difference.** X8 seeds 11 and 13 used the
very versions X0 reported (PostgreSQL 16.15 from Ubuntu's package, pgvector 0.8.7, wardowl 2.1.0,
acceptance commit `bf25bd0`) and psycopg 3.3.6, and still ran exact plans. What X8 cannot exclude
is a difference in the Kaggle image between X0's session and later ones, beyond what the runs
record [unverified, unlikely].

**H2c (ruled out by X8). Order and question mix.** X8 ran X0's own harness, with X0's shuffled order
and no probe questions, and still switched to generic plans. X1's person-blocked order and probes are
therefore not needed for the switch.

**What X8 adds to H2a.** Under OPA, X8 reached recall 1.000, with no custom-plan misses at all. X0
under OPA reproduced its plain pass to three decimals (0.691). Both fit OPA's filter producing the
same SQL texts as the plain pass on the same connection, so that it inherits the plain pass's
plan-cache decisions, generic in X8 and custom in X0 [inference; OPA's SQL text not compared]. The
plain pass checked 16,351 hits, 9 short of 16,360 [derived], which fits a few lossy custom-plan
searches among the first ten executions of each statement.

**Ruled out by code.**

- X0 never preparing: psycopg's default threshold applies to `conn.execute` (`pgvector.py:351`).
  Its cache is cleared only by a first-seen DROP, ALTER, ROLLBACK, DISCARD ALL or DEALLOCATE ALL
  (`_preparing.py`, `_should_discard`), and none ran on the search connection during the pass.
- A different index, opclass or build parameters: X1's b0 is X0's index build (`x1@947fb8f:1233-1238`).
- Different session settings, SQL, strategy, ground truth or recall code: identical (table above).
- The probe questions: they add 384 questions to X1's average but cannot raise it from 0.69 to 0.998.
- Query-vector differences: fp16 re-encoding moves cosines by about 1e-3 at most [unverified], far
  below a 0.3 recall gap.

### H3 (minor, for the 0.998): the first ten executions per statement

Recall@5 under `p-asrun` was 0.998, not 1.0. The ~114 custom executions per setting cover about 50
first-pass k=5 searches [derived]; at their loss rate they cost about 0.002 recall@5 [derived;
which people they belong to was not read]. The same searches produce the single empty result.

---

## 4. What X1 run 1 can and cannot support

**Can support:**

- That wardowl's pgvector search, through psycopg's defaults, can run PostgreSQL's generic plan,
  which bypasses the HNSW index: exact, complete, and about 60 times slower than HNSW at these
  settings. This is a finding for the paper (whether a search uses the graph depends on the plan
  cache, not only on the index and `ef_search`). It also falsifies P4's plan criterion as amended:
  5,852 generic executions, 50 of 50 shapes differ.
- P3's planner-estimate ratio (median 11.1 for judys). `EXPLAIN SELECT 1 ... WHERE <filter>` with
  values does not depend on the search's plan.
- Every Qdrant verdict: Q1 confirmed, Q2 falsified, Q4 inconclusive. Qdrant has no plan cache. Q3
  stays inconclusive because both layouts ended with the same segment count.
- An illustration, not a test, of P1's mechanism: one custom-plan empty that stopped at 20,083 rows
  emitted, removed by raising `hnsw.max_scan_tuples` and not by raising scan memory. It is one event.

**Cannot support:**

- P1 (b) and (c) as quantitative tests, and P2 (a) to (c): `pa-*`, `pb-wm64` and `pc-*` measured the
  generic exact plan. P2 (a) to (c) were also skipped (`pc-ef1000`, `pd-lim*`, the m32 builds).
- The size of X0's pgvector loss, or any recall or latency number for pgvector's HNSW search.
- P4's recall and ERR parts: `pg-custom` and `pg-noprepare` were skipped.
- Any claim about why X0 kept custom plans (H2a is supported only on the smoke corpus). What X1 run
  1 and X8 together do support is that X0's pgvector behaviour is the less common of the two
  outcomes under its own configuration (one run of three: X0 and X8 seeds 11 and 13), not a property of that configuration.

---

## 5. The fix: run 2 (amendment 2)

Pre-registered as amendment 2 (`benchmarks/paper/PREREGISTRATION.md`, commits `eeb7d2b`,
`afadde4`, and `80e3f56` revised after the smoke run, all before any full run) and implemented in
commits `63e92f1` and `354e789` (harness), `7f35b91` and `8b08712` (statistics), `2646517`,
`be3ea06` and `a956424` (Kaggle driver, notebook, README) on branch `paper/x1-underretrieval`:

1. **Plan control.** `pg-custom` (`plan_cache_mode = force_custom_plan`) plans every search with
   its values and leaves the plan to the planner, as X0's searches were planned (P4, P5).
   `pg-hnsw` and every P-a to P-e setting also turn sequential and bitmap scans off, which leaves
   the HNSW scan as the only plan. The smoke run showed why this is needed: at higher `ef_search`
   the planner priced HNSW above an exact plan even with custom planning. `pg-hnsw` is the
   reference of P1 and P2. `p-asrun` keeps the defaults and is P4's reference. Every pgvector
   invocation vacuums the table once, after the replays, so every shard's settings see the same
   GIN state.
2. **Executed plans.** `auto_explain` (session-loaded, NOTICE level, JSON) records the plan of every
   first-pass search: whether it used the HNSW index, and whether it is generic. A setting meant to
   search the graph that did so in fewer than half of its searches is flagged and left out of P1
   and P2. The fixed questions are rerun once with ANALYZE on the plan actually in use.
3. **X0 replays.** `p-x0` (the load's own pool and backend, right after the load, X0's order, one
   pass) and `p-x0v` (the same after `VACUUM (ANALYZE)`). Both record the GIN metapage and the
   autovacuum history. This tests H2a.
4. **P5 (new):** the plan cache decides. It is confirmed if `pg-custom` runs at least 90% HNSW
   plans and reaches recall@5 within 0.08 of 0.691 on the original questions, and `p-asrun` runs at
   most 10% HNSW plans, reaches at least 0.99, and is at least ten times slower.
5. **Qdrant one segment.** Upload with indexing off (`indexing_threshold` 0, which Qdrant 1.19.2
   reads as disabled), then index the one segment at the default 10,000 KB. Q3 counts segments
   holding points: Qdrant always keeps an empty appendable segment, per its merge optimizer's own
   documentation. Every build records its per-segment points.
6. **The full design**, all questions, three passes, three builds, run as parallel Kaggle sessions
   (prep, then shards A, B, C, then statistics). Latency is compared only within a session.

**Run 2's sessions (Kaggle, code at `a956424`).**

- Smoke: `x1run2-smoke` version 1 (at `2646517`) passed; version 2 (at `a956424`, after the
  revision) passed, with exit codes 0, 0, 0, 0.
- Prep: `x1run2-prep-gpu`, on a T4. It embedded the 107,540 chunks in fp16 in 309 s and wrote 1,489
  questions of 213 people.
- Abandoned prep attempts, which no shard uses. The CPU attempt `x1run2-prep` could not have
  finished: the smoke corpus took 1,583 s to embed on four CPUs, so the full corpus would take
  about 15 h. The TPU-host attempt `x1run2-prep-tpu` made no visible progress in about 2 h. Both
  were superseded by trivial versions.
- Shards, launched 19:21 UTC: `x1run2-shard-a` (`hnsw-m16-efc64` b0, the replays first),
  `x1run2-shard-b` (b1, b2) and `x1run2-shard-c` (`hnsw-m32-efc200` b0 to b2, then the Qdrant
  grid). Then the statistics kernel `x1run2-stats`, which attaches the three shards.

What to look at first when run 2 is in: `plans.csv` (HNSW share per setting), P5's verdict and
notes, and `p-x0` against `p-x0v` with their `table_state_before`. If `pg-custom` lands near 0.69,
X0's loss is reproduced and attributed to HNSW custom plans. If `p-x0` also runs custom plans with
a large pending list while `p-x0v` runs generic ones, H2a explains why X0 differed from X1.

---

## Sources

- PostgreSQL 16 source: `src/backend/utils/cache/plancache.c` (choose_custom_plan, the comment on
  not resetting costs), `src/backend/optimizer/plan/planner.c` (preprocess_limit),
  `src/backend/utils/adt/selfuncs.c` (generic_restriction_selectivity, matchingsel,
  gincostestimate), `src/backend/access/gin/ginvacuum.c` (ginvacuumcleanup),
  `src/include/catalog/pg_operator.dat` (jsonb `@>`), all at
  https://github.com/postgres/postgres/tree/REL_16_STABLE
- PostgreSQL docs, PREPARE (custom and generic plans): https://www.postgresql.org/docs/16/sql-prepare.html
- pgvector v0.8.7 `src/hnsw.c` (hnswcostestimate): https://github.com/pgvector/pgvector/blob/v0.8.7/src/hnsw.c
- psycopg `psycopg/_preparing.py`: https://github.com/psycopg/psycopg/blob/3.3.6/psycopg/psycopg/_preparing.py
  and prepared statements: https://www.psycopg.org/psycopg3/docs/advanced/prepare.html
- Qdrant v1.19.2 `lib/shard/src/optimizers/merge_optimizer.rs`, `lib/shard/src/optimizers/config.rs`
  (`get_indexing_threshold_kb`: 0 disables indexing), `lib/collection/src/optimizers_builder.rs`,
  `lib/segment/src/types.rs` (`SegmentInfo`): https://github.com/qdrant/qdrant/tree/v1.19.2
- Qdrant docs, collections (grey status, empty optimizer update): https://qdrant.tech/documentation/manage-data/collections/
