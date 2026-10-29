# Evidence: X4 (engine filters against engine checks) and X7 (revocation and faults), GitHub Actions run 1

Source: repository `muzakkirhussain011/wardowl`, workflow `paper-x4-x7`
(`.github/workflows/paper-x4-x7.yml`), run #3 of the workflow, id 40919304635, attempt 1
(https://github.com/muzakkirhussain011/wardowl/actions/runs/40919304635), triggered by a push of
commit `e66dffc2a24b89b3ae60cd10db02e0363ff4387a` to branch `paper/x4-x7` (head commit message
"bench: run X4 and X7 in the full pre-registered configuration"), profile `full`. Read on
2026-10-29 with git only, from the branch `results/x4-x7` at commit `10641c0`, directory
`40919304635-1/`: `RUN.md`, the pooled reports `x4_report.md` and `x7_report.md` (the report job
ran `x4_stats.py` and `x7_stats.py` over every job's records), the 14 per-job reports in `jobs/`,
the log tails in `logs/` and the compressed raw records in `raw/` (read only for versions, image
digests, durations and two record samples; nothing was recomputed). The pre-registration is
`benchmarks/paper/PREREG_X4_X7.md` on `paper/x4-x7` (commit `eafafa9`, pushed before any harness
code; amendment 1 at `ba00ca6`). The verdicts below are the ones the statistics scripts printed,
not re-derived.

Two smoke runs preceded it and are not analysed: 40916767636 (commit `62a587a`, which found the
proxy fault and led to amendment 1) and 40918333147 (commit `3f2cff0`, which confirmed the fixes).

## Setup

wardowl 2.1.0 at `fix/engine-limits` `e7776f0` (the `wardowl/` package is unchanged on
`paper/x4-x7`), Python 3.12.15, `ubuntu-latest` runners (Linux 7.0.0-1017-azure, 4 CPUs), one job
per engine and part, 14 jobs in parallel plus a report job. Clients from `uv.lock`: numpy 2.5.4,
faiss-cpu 1.15.1, psycopg 3.3.6, psycopg-pool 3.3.3, qdrant-client 1.19.1, redis 8.1.0, httpx
0.28.1. OPA 1.21.2 (binary from `setup-opa`, build `3f7474e6`, run by the harness). Images (tag,
image id, registry digest):

| Server | Image | Image id | Registry digest |
|---|---|---|---|
| OpenFGA (Postgres datastore) | `openfga/openfga:v1.22.0` | `sha256:6da24ff1...b943` | `sha256:9cf9a20af32a40434cd3a788c429879439ee9ea9abf65c9c200ee17cd43f769e` |
| SpiceDB (Postgres datastore) | `authzed/spicedb:v1.56.2` | `sha256:3bad3b99...e811` | `sha256:aa96009a0477f8a759149823407d47ad16d1a74390bae3102b3b0b7143502764` |
| Cerbos | `ghcr.io/cerbos/cerbos:0.56.0` | `sha256:9769be85...e584` | `sha256:540643bc67ba628011a150ad1d3370f285daa38995be5cd7a4be181da902bec1` |
| Postgres (engine datastore; pgvector store) | `pgvector/pgvector:pg17` | `sha256:151aa1c2...d7e` | `sha256:ac08538c6f8b9904c33c8224c5e5706dbe760aca29db1d096972b4052c22a75d` |
| Qdrant | `qdrant/qdrant:v1.19.2` | `sha256:e37a0793...e8e7` | `sha256:b7b0444c4c351c970b98e90a6f89c2ee4287c65b44e52b4cb503fa5b2aa927ad` |
| Redis (shared cache) | `redis:8.10.2-alpine` | `sha256:6cfed4c6...c373` | `sha256:9f8d2d789b9a1d1e3f283f979aa9cbf393373806472e1ccd460e2f9c869b833b` |

Design (from the pre-registration): X4a measures filter against check at one revision for 13
profiles (7 well-formed, 4 stress, 2 controls) on seeded worlds of 3 tenants, 120 users, 60 nested
groups, 80 nested folders and 1,500 documents, 5 seeds, every user (600 subjects and 900,000
pairs per profile), against an oracle written without wardowl's filter code. X4b repeats it for
40 users per seed under a writer committing 20 toggles a second. X4c grows one subject's readable
set from 10 to 100,000 documents in a 100,000-document corpus (three structures: `simple-direct`,
`full-direct`, `full-folder`), 30 queries per level and seed, FAISS flat, k = 10. X4d times
`filter_for` and `check` with and without `CachingAuthorizer`. X7a revokes 40 grants per (path,
cache condition) for 10 paths and 5 conditions and polls retrieval every 50 ms. X7b injects 14
faults into each engine (and 5 or 8 into pgvector and Qdrant), 10 episodes per (target, fault,
condition), 3-s baseline, 12-s fault, recovery until 3 s of exact answers.

## Status

All 14 experiment jobs exited 0 (`jobs/*.status.json`), the report job published, the workflow's
`experiment` result is `success`. Durations of the driver parts, from the `part-end`, `path-end`
and `target-end` records (seconds):

| Job | Parts and durations |
|---|---|
| x4-openfga | a 4,579; b 2,333 |
| x4-spicedb | a 152; b 249 |
| x4-policy | controls 11; cerbos 211; opa a 338, b 16, c 6,613 |
| x4-openfga-scale | c 2,089 |
| x4-spicedb-scale | c 645 |
| x7a-openfga | openfga 1,468; openfga-cached-hc 1,468; openfga-cached-ml 1,467 |
| x7a-spicedb | spicedb-fc 1,499; spicedb-ml 4,013 |
| x7a-policy | opa-data 1,466; opa-policy 1,465; cerbos-policy 3,996 |
| x7a-acl | acl-pgvector 21; acl-qdrant 23 |
| x7b-openfga, -spicedb, -opa, -cerbos | 4,499; 4,502; 4,498; 4,497 |
| x7b-stores | pgvector 960; qdrant 1,450 |

Records: X4 23,849 in 5 files; X7 3,133 in 9 files. Harness errors: X4 only the expected OPA
Compile API timeouts (1,350 in retrievals and 45 in `filter_for`, all "OPA compile x4rel/allow
timed out after 2.0 s", see X4c); X7 none. G4: 1,090 fault episodes, 0 excluded for a baseline
below 99% exact answers. Every X7a trial was valid (the warm retrieval returned the target).

## Verdicts (as printed, pooled over all jobs)

Guards: **G1** controls CONFIRMED (control-oracle 600 subjects, none disagreeing; control-planted
600 subjects, reported counts exactly the planted 16,774 false admits and 1,233 false denials).
**G2** encoding CONFIRMED for all 7 well-formed profiles (check against oracle 0 of 900,000 pairs
each). **G3** leak detection CONFIRMED (allow-all control leaked 7,427, 17,484, 17,685 and 22,790
hits on OpenFGA, SpiceDB, OPA and Cerbos). **G4** baseline: no episode excluded.

| Hypothesis | Verdict | Numbers (95% intervals) |
|---|---|---|
| X4-H1 agreement at one revision | CONFIRMED for openfga, openfga-ctx, spicedb, opa-acl-doc, opa-rel-doc, opa-rel-pe, cerbos | each: 600 subjects with a filter, 0 false admits, 0 false denials in 900,000 pairs; subject-level bound 0.0050 |
| X4-H2 shape drift | CONFIRMED (cerbos-drift and opa-acl-doc-drift) | cerbos-drift: 569 false admits, all on documents with a scalar ACL field, all reproduce, 0 false denials; pair rate 0.000632 [0.000570, 0.000696]; subjects affected 0.525 [0.483, 0.563]. opa-acl-doc-drift: 0 of 900,000 |
| X4-H3 negation never dropped | CONFIRMED (no false admit in cerbos-excl, opa-rel-pe-excl) | no filter returned to any of 600 subjects in either profile, so 0 false admits |
| X4-H3 availability, cerbos-excl (predicted 0) | CONFIRMED | 0 of 600 subjects with a filter |
| X4-H3 availability, opa-rel-pe-excl (filter iff no ban in scope) | FALSIFIED | 527 of 600 subjects as predicted: the 73 users without a ban also got no filter (the residual kept a `not`) |
| X4-H4a SpiceDB pinned under the writer | CONFIRMED | 200 trials, 0 disagreeing pairs, 0 oracle mismatches |
| X4-H4b unpinned under the writer | CONFIRMED for all five conditions | trials disagreeing / pairs / skew-explained: OpenFGA writer-hc 1.000 [1.000, 1.000] / 9,433 / 9,433; writer-ml 1.000 [1.000, 1.000] / 9,972 / 9,972; SpiceDB writer-fc 0.815 [0.760, 0.865] / 2,190 / 2,190; writer-ml 0.040 [0.015, 0.070] / 228 / 226 (0.991); OPA writer 0.130 [0.085, 0.180] / 97 / 97 |
| X4-H4c quiet conditions | CONFIRMED (OpenFGA quiet-hc, SpiceDB quiet-ml, OPA quiet) | 200 trials each, 0 disagreeing pairs |
| X4-H4d SpiceDB writer-ml minus writer-pinned | CONFIRMED | 200 pairs, difference 0.040 [0.015, 0.070] |
| X4-H5a OpenFGA ListObjects count and signal | CONFIRMED | 135 calls (simple-direct), every count min(N, 1,000), only the key `objects` |
| X4-H5b SpiceDB LookupResources count | CONFIRMED | 135 calls, every count min(N, 1,000) |
| X4-H5c no silent truncation | CONFIRMED | 540 `filter_for` calls (OpenFGA and SpiceDB, 3 structures, 9 levels, 5 seeds, 2 timeouts), 0 short filters |
| X4-H5d filter below the limit, none at it | CONFIRMED | 0 calls with N <= 999 without an exact filter, 0 calls with N >= 1,000 with a filter |
| X4-H6 recall after the fallback (6 engine and structure combinations, parts a to d) | CONFIRMED, 24 of 24 | (a) recall 1 for every query with N <= 999; (b) N in {1,000, 1,001}: OpenFGA 0.877 [0.856, 0.897], 0.884 [0.865, 0.902], 0.885 [0.866, 0.904] and SpiceDB 0.869 [0.849, 0.889], 0.885 [0.865, 0.905], 0.877 [0.858, 0.896] (simple-direct, full-direct, full-folder); (c) 1.000 at 10,000, 30,000 and 100,000; (d) 0 false-complete results |
| X4-H7 caching | CONFIRMED for OpenFGA, SpiceDB, OPA; INCONCLUSIVE for Cerbos | lowest median uncached-to-cached ratio: OpenFGA 20.2, SpiceDB 17.5, OPA 114.3; Cerbos check per hit 8.6 [8.5, 8.7] (filter 94.4 [88.9, 99.5]) |
| X7-H1 the stated bound holds | FALSIFIED in 3 of 45 cells, all SpiceDB `minimizeLatency`; CONFIRMED in the other 42 | spicedb-ml nocache 1 of 40 beyond B + 1 = 6.5 s (maximum 8.742 s); spicedb-ml ttl30-inv 40 of 40 beyond 6.5 s; spicedb-ml ttl30-shared-inv 39 of 40 beyond 7.5 s; no trial failed to take effect |
| X7-H2 ttl is the realized delay | CONFIRMED, 12 of 12 cells | ttl5 medians 5.015 to 5.034 s; ttl30 medians 30.016 to 30.033 s (e.g. openfga 30.020 [30.014, 30.026]) |
| X7-H3 invalidation | FALSIFIED for spicedb-ml (2 cells); CONFIRMED in 16 cells | spicedb-ml ttl30-inv median 30.042 [30.031, 30.048] against 6.0; ttl30-shared-inv 31.048 [31.033, 31.061] against 7.0; elsewhere inv medians 0.6 ms to 9 ms, shared-inv 1.014 to 1.022 s |
| X7-H4 metadata paths ignore the ttl | CONFIRMED, 10 of 10 cells | medians 0.68 ms to 3 ms (acl-pgvector, acl-qdrant) |
| X7-H5 SpiceDB staleness real and bounded | FALSIFIED | median 3.251 [2.994, 3.371] s (meets >= 0.5), maximum 8.742 s (exceeds 6.5); 28 flaps in 40 trials |
| X7-H6 fail closed | CONFIRMED | 623,279 requests under faults (control excluded): 0 leaks (one-sided bound 4.8e-6 per request), 0 engine failures other than `AuthorizationError`, 0 messages naming a host |
| X7-H7a transport faults on engines | CONFIRMED, 24 of 24 cells | failing share 1.000 [1.000, 1.000] for down, refuse, blackhole, slow-3000, http500, http503 on each engine (40 to 5,833 requests per cell) |
| X7-H7b slow-200 and slow-1000 | CONFIRMED, 12 of 12 cells | failing 0.000; median rise per retrieval: engines 0.398 to 0.407 s (slow-200) and 1.999 to 2.013 s (slow-1000); Qdrant 0.201 and 1.001 s; pgvector 0.801 and 4.002 s |
| X7-H7c store faults | CONFIRMED for Qdrant (5 cells) and pgvector down and refuse; INCONCLUSIVE for pgvector blackhole | Qdrant 1.000 over 5,236 to 5,683 requests; pgvector down and refuse 1.000 over 10 requests each; pgvector blackhole 0 requests inside the fault window |
| X7-H8a recovery without the breaker | CONFIRMED, 20 of 20 cells | medians 0.020 to 0.178 s (refuse, blackhole, slow-3000, http500, http503) |
| X7-H8b breaker: recovery and fail-fast | CONFIRMED, 20 recovery cells and 4 fail-fast comparisons | recovery medians 3.12 to 3.55 s; failed-request latency under blackhole 0.05 to 0.1 ms with the breaker against 2.002 to 2.003 s without |
| X7-H9 a warm cache masks an outage | CONFIRMED, 20 of 20 cells | succeeding 1.000 [1.000, 1.000] for down, refuse, blackhole, slow-3000, http500 on each engine |

Exploratory (no prediction): `openfga-cached-ml` showed no staleness from OpenFGA's check-query
cache (nocache median 0.003 s, maximum 0.008 s; ttl30-inv 0.003 s). `cerbos-policy`: Cerbos
reloaded a rewritten policy file in median 2.549 [2.369, 3.219] s, maximum 4.035 s; with
`invalidate()` the revocation took 30.025 [30.019, 30.032] s (ttl30-inv) and 31.039 [31.026,
31.047] s (shared). Recovery after `down` (container or OPA process restarted): medians 0.081 s
(OPA), 0.201 s (Cerbos), 0.214 s (OpenFGA), 0.465 s (SpiceDB). Content faults on engines:
truncate, garbage-json and type-flip failed closed with `AuthorizationError` on every engine;
`empty` failed closed on OpenFGA, OPA and Cerbos and on SpiceDB returned no hits without an error
(4,746 deviating answers, 1 failure); `drop-last` failed closed on all four (a shortened
ListObjects list alone would only lose recall, but the batch check in the same retrieval then
failed). Store errors: 28,125 failures, none naming a host; their classes were the clients'
(`psycopg.OperationalError`, `psycopg_pool.PoolTimeout`,
`qdrant_client.http.exceptions.ResponseHandlingException` and `UnexpectedResponse`,
`json.decoder.JSONDecodeError`), unwrapped.

## Key numbers

- **X4a.** 13 profiles x 600 subjects x 1,500 documents = 11.7 million (subject, document) pairs.
  Every engine's check matched the oracle on every pair of every well-formed profile, and every
  filter matched its check: 0 of 6.3 million pairs over the 7 well-formed profiles. Cerbos with
  scalar ACL fields: 569 false admits, deterministic.
- **X4b.** Under a writer, OpenFGA's filter and check disagreed in every trial (median 59 writes
  in the window with `HIGHER_CONSISTENCY`, 208 with `MINIMIZE_LATENCY` and its 10-s allowance);
  SpiceDB `fullyConsistent` in 81.5% of trials, `minimizeLatency` in 4.0%, pinned in none.
  Every disagreement but 2 of 228 (SpiceDB `minimizeLatency`, 5.5-s allowance) was explained by
  a write in the window; none reproduced.
- **X4c.** Non-streaming ListObjects returned exactly 1,000 objects at every N >= 1,000 and nothing
  but `objects`; streamed ListObjects returned all N up to 100,000 within its deadline (median
  1.74 s simple-direct, 1.93 s full-direct, 2.03 s full-folder at 100,000). LookupResources with
  `optionalLimit` 1,000 returned exactly min(N, 1,000), every result carrying `afterResultCursor`
  whatever N (so the cursor does not signal truncation); without a limit it streamed 100,000 in
  2.64 to 3.67 s. wardowl gave an exact filter at N <= 999 and none at N >= 1,000 in all 540 calls,
  never a short one. Recall@10 through wardowl: 1.000 with the filter, 0.855 to 0.891 per level at
  N = 1,000 and 1,001 after the fallback to post-filtering (selectivity about 1%), 1.000 from
  3,000 up; 0 leaks and 0 false-complete results over 8,100 queries. OPA: the filter-document
  route was exact at every N (median `filter_for` 0.57 to 0.71 s over a 100,000-entry data
  document); OPA's Compile API took 4.25 to 5.67 s (median, 10-s timeout) and timed out at
  wardowl's default 2 s in all 45 calls and all 1,350 retrievals, which failed closed.
- **X4d.** Uncached `filter_for` medians: OpenFGA simple model 0.87 ms at N = 10 to 110 ms at
  100,000, full model 147 to 324 ms; SpiceDB 1.1 ms at N = 10 and 22 to 30 ms from 999 on (the
  1,000 limit caps it); on the X4a worlds OpenFGA 4.1 ms, SpiceDB 6.4 ms, Cerbos 1.2 ms, OPA
  filter document 1.7 ms (ACL) and 13.6 ms (relational), OPA Compile API 115.5 ms. Check per hit:
  OpenFGA 0.14 ms (simple) and 0.51 to 0.73 ms (full), SpiceDB 0.11 to 0.22 ms, Cerbos 0.13 ms,
  OPA 0.17 to 1.4 ms on the X4a worlds and 63 to 94 ms over the 100,000-entry data document.
  Cached answers were faster by a median factor of 8.6 (Cerbos check) to about 600,000 (OPA
  Compile API filter).
- **X7a.** Without a cache, revocation took effect in 0.6 ms to 10 ms everywhere except SpiceDB
  `minimizeLatency` (median 3.25 s, maximum 8.74 s, revoked chunks reappearing in 28 polls after
  having disappeared) and Cerbos's policy reload (median 2.55 s). A cache delayed it by its ttl
  (medians within 34 ms of 5 s and 30 s). `invalidate()` removed that delay everywhere except where the engine itself
  was stale: SpiceDB `minimizeLatency` and Cerbos before its reload, where the cache refilled
  from the stale answer and held it for the full 30 s.
- **X7b.** 1,090 episodes and 623,279 judged requests: no leak, every engine failure an
  `AuthorizationError` with a message naming no host, every transport fault fully unavailable,
  recovery within 0.18 s of the fault's removal (3.1 to 3.6 s with the breaker, which failed
  requests in under 0.1 ms instead of 2 s), and a warm 30-s cache answering 100% of retrievals
  through 12-s outages.

## Deviations from the pre-registration

- **Amendment 1** (committed alone at `ba00ca6`, after the first smoke run and before any full
  result): X7a polls until max(B, T + S') + 15 s instead of B + 15 s, so cells that miss their
  bound still yield a time; X7b counts a fault as begun when the injecting command returns. The
  verdict rules did not change. Without the amendment, the spicedb-ml ttl30-inv and shared-inv
  cells would have been recorded as never taking effect (same verdict, no time).
- **X4a OpenFGA "one revision"** is a quiescent store read with `HIGHER_CONSISTENCY`: OpenFGA's API
  has no snapshot token (stated in the pre-registration).
- **X4-H3 "no false admit" holds vacuously**: neither exclusion profile returned any filter.
- **X4-H6 (b)** pools the two levels with (seed, query, level) as the cluster.
- **X4-H7 Cerbos** has one level only (the X4a worlds); its verdict rests on 50 latency records.
- **X4c OPA Compile API route**: every retrieval failed closed on the default 2-s timeout, so
  recall through it was not measured; only its `filter_for` with a 10-s timeout was (exact at
  every N). This route carried no hypothesis.
- **X7-H7c pgvector**: the closed loop issues one retrieval at a time, and a blocked one holds the
  loop for the pool timeout (5 s) or the watchdog (10 s), so only 10 requests per fault fell inside
  the 12-s window for down and refuse, and none for blackhole (8 hangs and 5 pool timeouts fell
  across its boundaries). The blackhole cell is inconclusive, not failed.
- **X7-H7b slow-1000 on engines** rests on 41 to 43 requests per engine: each retrieval makes two
  authorizer calls, so it takes about 2 s.
- **X4b skew attribution** is generous for wide windows: with 59 to 208 writes in a window and half
  of the writes targeting the measured user, almost any disagreement on a touched document is
  explained. The pinned and quiet conditions are the controls that carry the claim.

## Library defects and gaps the run exposed

Code locations at `fix/engine-limits` `e7776f0` (the run's library).

1. **`invalidate()` does not survive a stale engine.** X7a spicedb-ml ttl30-inv: 40 of 40
   revocations took effect only after the full ttl (median 30.042 s, bound 5.5 s); cerbos-policy
   ttl30-inv likewise (30.025 s). After `invalidate()`, the next call asks the engine, which still
   answers from a stale snapshot, and `_put` caches that answer for the whole ttl
   (`wardowl/caching.py:315-325`; `invalidate` at `:457-491`; the module docstring's promise at
   `:7-11`). The real bound after `invalidate()` is ttl + staleness, not staleness. Minimal fix: a
   `source_staleness` (seconds) argument; `invalidate()` records `now + source_staleness` for the
   subject (or everyone), and `_put` and `_shared_put` refuse entries for that subject until then;
   document that SpiceDB `minimizeLatency` needs about 10 s and Cerbos with `watchForChanges` about
   5 s, or recommend `fullyConsistent` (or `atLeastAsFresh` with the write's token) where
   invalidation must be immediate.
2. **SpiceDB adapter documents a 5-s staleness bound; the run measured 8.7 s, non-monotonic.**
   `wardowl/authorizers/spicedb.py:37-40` says a revoked permission keeps granting access "for up
   to the datastore's revision quantization interval (5 seconds by default)"; X7-H5 measured a
   maximum of 8.742 s and 28 flaps (the revoked chunk reappearing after it had disappeared). The
   default consistency is `minimizeLatency` (`:138`). Minimal fix: correct the docstring (the
   quantization interval plus the max-staleness allowance plus the time a new revision takes to
   become the quantized one; observed up to 8.7 s, and successive reads may move backwards), and
   mention it in `docs/integrations/spicedb.md`.
3. **An empty LookupResources stream is taken as "no readable documents".** X7b spicedb `empty`:
   4,746 retrievals returned no hits and raised nothing. `_http.py:349-350` turns an empty body into
   no lines, and `spicedb.py:243-258` turns no lines into `In(doc_id, {})`, so the pre-filtered
   search returns nothing and the re-check never runs. It cannot leak, but a middlebox, a proxy or a
   server fault that ends the stream early is indistinguishable from an empty permission set, at
   any line boundary. Minimal fix: when LookupResources returns zero results, return no filter (the
   retriever post-filters, and CheckBulkPermissions then decides, or fails closed); the cost is a
   post-filter search for subjects who truly read nothing.
4. **Store errors are not wrapped.** X7b: 28,125 store-fault failures surfaced as the clients' own
   exceptions, with their own messages (Qdrant's include the raw response content), because
   `retriever.py:502` (and `:525` for `asearch`) call the backend outside the `try` that wraps
   authorizer failures (`:508-519`). The module's fixed-message guarantee (`:20-22`) covers the
   authorizer only, and an agent framework shows the message to the model. Minimal fix: wrap
   backend failures in a `SearchError` (a new exception, or `AuthorizationError` if callers rely on
   one class) with a fixed message such as "search failed", keeping the original as `__cause__`.
5. **No bound on a store call.** X7b pgvector: a blackholed or refused connection held retrievals
   for the pool timeout (5 s, `PoolTimeout`) or past the 10-s watchdog (8 hangs).
   `PgVectorBackend.search` (`wardowl/backends/pgvector.py:346-355`) sets no statement or client
   timeout, and the retriever has no deadline. Minimal fix: a `statement_timeout` (seconds)
   argument applied with `SET LOCAL statement_timeout` beside the existing `SET LOCAL` settings
   (`:328-339`), and documentation of libpq's `connect_timeout`, `tcp_user_timeout` and keepalives
   for network partitions.

Gaps that are not defects but belong in the documentation: OPA's Compile API over a
100,000-entry data document took 4.2 to 5.7 s, above wardowl's default 2-s timeout (fail closed,
availability lost); the 1,000-result fallback costs about 12% recall@10 at about 1% selectivity
because `max_candidates` is also 1,000, while streamed ListObjects and unlimited LookupResources
returned 100,000 objects in 2 to 4 s, so a paginated or streamed filter is a possible improvement.

## What this means for the paper

- **C3 is a clean negative result for translation faults.** At one revision, for OpenFGA (stored
  and contextual groups), SpiceDB, OPA (filter document over ACL metadata, filter document over
  relational data, and OPA's own partial evaluation) and Cerbos, filter and check never disagreed
  in 6.3 million pairs, and each engine's check matched an independent oracle. The only
  disagreements at one revision come from data shape (Cerbos with scalar ACL fields, 569 false
  admits, all caught by the re-check) and are the documented semantic gap the conformance
  campaign found.
- **Disagreement in practice is revision skew.** Under a concurrent writer, unpinned filter and
  check disagreed in up to 100% of trials, every disagreement but two attributable to a write
  between the calls, and pinning SpiceDB to one snapshot removed it. This backs the background
  section's "a violation is a translation fault only at a single revision" with numbers.
  `minimizeLatency` hides skew between the two calls (4% of trials) by reading one stale snapshot
  for both, which trades consistency between calls for freshness, as X7 then shows.
- **Truncation is detected, not silent, but costs recall.** Both list APIs truncate at 1,000 with
  no signal; wardowl's limit rule caught every case (0 short filters in 540 calls) and fell back
  honestly (0 false-complete results), at a measured cost of about 12% recall@10 at the limit.
- **Revocation bounds hold except where the engine is stale.** The ttl is the realized delay
  (medians within 34 ms of it), metadata paths are immediate, and `invalidate()` works, except
  with SpiceDB `minimizeLatency` and Cerbos's policy reload, where it is defeated by a stale
  refill. The paper's cache description in the system section ("an explicit invalidation ends it
  at once") must be qualified, and the "ttl plus engine staleness" bound restated for
  invalidation.
- **Fail closed holds without exception** across 623,279 requests and 13 kinds of fault, at the
  expected availability cost; the breaker and a warm cache each change that cost measurably. Two
  pre-registered predictions were falsified and should be reported as such: SpiceDB's staleness
  exceeded 6.5 s (8.7 s), and OPA's partial evaluation keeps `not (x in [])`, so its filter is
  unavailable to every subject once a ban rule exists.

## Follow-ups

- Library: the five items above, routed to a PR (none implemented here).
- Add the full residual of one OPA compile for a ban-free user to the evidence (the record keeps
  only its first 400 characters; the reason "compound 'not'" is recorded).
- X7-H7c pgvector blackhole needs an open-loop driver (several retrievals in flight) to put
  requests inside the window; report it as inconclusive until then.
- Archive the 14 artifacts (90-day retention) with the paper artifact; the compressed raw records
  are already on `results/x4-x7`.
