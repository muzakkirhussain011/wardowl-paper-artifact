# Evidence: X2 and X5, full run 1

Written 2026-10-30. Pre-registration: `benchmarks/paper/PREREG_X2_X5.md` on wardowl branch
`paper/x2-x5`, committed alone at `828ea27` (2026-10-29) before any harness code. Harness at
`c1e20f8`; after the smoke run (GitHub Actions run 40915647544, published as
`results/x2-x5:40915647544-1/`) `884ce18` changed three things before the full run: PostgreSQL's
container got `--shm-size=4g` (the smoke run's pgvector MS MARCO jobs failed their parallel HNSW
build with "could not resize shared memory segment ... to 2144374208 bytes"), LanceDB's per-search
deprecation warnings were silenced (`LANCE_LOG=error`), and a verdict line printed the number of
seeds found instead of a fixed "5". No rule, setting or threshold changed.

Full run: GitHub Actions run **40921769714** (https://github.com/muzakkirhussain011/wardowl/actions/runs/40921769714),
commit `884ce18`, published by the workflow to branch `results/x2-x5`, commit `f4c175b`, folder
`40921769714-1/` (`RUN.md`; `stats/report.md`, `summary.md`, `verdicts.json`, `validity.csv` and
the `x2_*` / `x5_*` CSVs; `jobs/` with every job's record; `logs/` with the last 200 lines of every
job's log; `data/` with the corpora's `config.json` and `checksums.json`). Statistics: 10,000
cluster-bootstrap resamples, seed 20261029. Raw rows (one JSON line per setting and pair) are in the
run's artifacts `x2x5-res-*` (90 days); they still need archiving.

## What ran

Hosted runners (4 vCPUs, 16 GB); one store per job; throughput compared only within a job.

- **Data.** E: the enterprise scenario, 107,540 chunks, BAAI/bge-base-en-v1.5 (768 dimensions)
  embedded on CPU in float32 in 6 shards; 213 people (the scenario's 189 and X1's 24 probe people);
  1,489 questions (1,105 original); readable chunks per person min 0, median 58,433, max 59,265.
  M: the first 1,000,000 BEIR MS MARCO passages, BAAI/bge-small-en-v1.5 (384 dimensions) in 8
  shards; query pool 20,000; 5 seeds of U and C layouts; 1,050 subjects; 6,200 (question, subject)
  pairs; 684 pairs took a query-selection fallback (fewer than 4 pool queries met the P or N
  criterion); tenant `a` share 0.500341. U group sizes exact (division 10,000, department 1,000,
  team 100); C (k-means) division sizes median 9,499.5 to 9,889 (min 958 to 4,381, max 17,365 to
  21,335), team sizes median 88 to 92 with up to 23 empty teams per seed. Embedding environment:
  torch 2.15.0+cpu, sentence-transformers 6.2.0, transformers 5.22.0, datasets 5.1.0, numpy 2.5.4,
  Python 3.12.15. Every store job verified the data's SHA-256 (`checksums.json`) before loading.
- **Stores.** PostgreSQL 17.11 with pgvector 0.8.7; Qdrant 1.19.2; Elasticsearch 9.5.5; OpenSearch
  3.9.0; Weaviate 1.39.12; Redis 8.10.2; Milvus (`milvusdb/milvus:v3.0.2`; the job did not record
  a server version); MongoDB Atlas Local 8.0.30; LanceDB 0.40.0 and Chroma 1.5.9 (embedded); FAISS
  1.15.1 flat. M load time of build 0, seconds: LanceDB 116.5, Redis 267.2, pgvector 315.6,
  MongoDB 560.7, Milvus 662.6, Weaviate 677.7, Elasticsearch 721.0, OpenSearch 957.9, Qdrant
  1,041.3 (per-tenant layout 1,543.5), Chroma 1,303.7 (b1 1,626.9, b2 1,689.1), FAISS 65.8.
- **Jobs.** X2-E: 11 jobs (each store's three builds in one job; Qdrant and Elasticsearch two
  layouts each), all `done`. X2-M: 34 jobs, 33 `done`; `x2-m-chroma-b2` ended at the runner's
  job timeout with its record still `running` (so the run's `x2-m` status is `cancelled`). X5: 2 E
  jobs and 6 M jobs, all `done`. Stats and publish succeeded. No job had a failure; skipped settings
  are Chroma's below.
- **Budget cuts** (a setting's balanced prefix of the round-robin order, as pre-registered):
  pgvector's exact setting on M ran 998 of 6,200 pairs (p50 636.0 ms); Chroma on E ran 381 to 407 of
  1,468 scorable pairs per setting; every other setting ran all pairs (E 1,468 scorable, M 6,200;
  Qdrant's per-tenant layout on M 3,000 tenant-shape pairs by design).

### Chroma on MS MARCO: not measured (deviation)

All three builds loaded the million passages (1,302.5, 1,625.4 and 1,687.4 s), but no setting got
past its warm-up: every setting of every build reports `pairs_run` 0, `retrievals` 0,
`warmup_errors` 0 and `cut: budget`. The 20 untimed warm-up retrievals of a setting took
2,738.2 to 2,782.7 s on build 0, 4,414.7 to 4,421.4 s on build 1 and 3,826.0 to 3,851.7 s on
build 2, that is about 137 to 221 s per filtered retrieval. The harness starts pass 1 only while the
setting's budget lasts and checks the job's deadline only between settings; the warm-up is not
counted against either, so each warm-up overran its budget (about 49 min on build 0), build 1
skipped `ef500` and `ef1000`, build 2 skipped `ef1000` and ran past the runner's 355-minute limit.

**Rerun: not launched.** Re-running these jobs on the same data (`data_run_id` 40921769714) under
the pre-registered procedure cannot produce a measurement: at 137 to 221 s per retrieval, the six
settings' warm-ups alone (120 retrievals) take 4.6 to 7.4 h, more than a job's 6 h after a 22 to
28 min load, and one pass over the 6,200 pairs of one setting would take 9.8 to 15.8 days. Any
variant that could fit (fewer warm-ups, one setting per job) changes the procedure and would yield
about 40 to 100 pairs per setting and build, a few per cell. Chroma on MS MARCO is reported as
incomplete: it loaded, and a filtered retrieval took 137 to 221 s, but recall was not measured.
H2.1 to H2.4 are judged on the nine other stores (the rules count stores with data; none of them
reached a threshold through Chroma's absence, see below).

## Validity checks

- **V1 (exact settings reach recall@10 >= 0.999): holds.** Minimum recall@10 1.0 for every exact
  setting: E Elasticsearch (both index types), FAISS, LanceDB, MongoDB, OpenSearch, pgvector, Qdrant
  (as-run and per-tenant), Redis, Weaviate; M the same stores (pgvector on its 998 pairs). Milvus
  and Chroma have no per-query exact search.
- **V2 (as-run settings reproduce the audit within 0.03 for at least 7 of 9): holds, 8 of 9.**
  Recall@10 on the 1,105 original questions against X0:

  | Store (setting) | X2 | X0 | Within 0.03 |
  |---|---|---|---|
  | Redis (ef100) | 0.9879 | 0.980 | yes |
  | Elasticsearch (int8, nc500) | 0.9602 | 0.948 | yes |
  | OpenSearch (default) | 0.9402 | 0.938 | yes |
  | Weaviate (default) | 0.9056 | 0.892 | yes |
  | Chroma (default) | 0.9903 | 0.883 | **no** |
  | LanceDB (refine) | 0.8716 | 0.860 | yes |
  | pgvector (ef100) | 0.7297 | 0.732 | yes |
  | Qdrant (ef128) | 0.5763 | 0.561 | yes |
  | FAISS (exact) | 1.0 | 1.0 | yes |

  Chroma's miss: its budget allowed only 381 to 407 of the 1,468 scorable pairs per setting, the
  head of the round-robin order, which takes each person's first questions. For the 180 generated
  people these are targeted questions, and for the scenario's nine personas generic ones; X0
  measured Chroma's overlap@5 at 0.989 on targeted questions and 0.82 to 0.84 on the others
  [inference: the run did not print Chroma's recall by category for this prefix]. pgvector's match
  (0.7297 against 0.732) is the audit reproduced with every search planned with its own values.
- **V3 (no leak, unreadable hit, canary or violation): holds.** 0 jobs stopped by a leak; every hit
  of every pass was checked by the layer's re-check and by the independent oracle.
- **V4 (M subjects at s >= 0.5% within 25% of nominal, at least 90%): holds, 1.0.**
- **V5 (pgvector's plans).** Share of first-pass searches whose plan (EXPLAIN with the search's own
  values and settings) used the HNSW index, from `x2_pgvector_plans.csv`:

  | Setting | E | M |
  |---|---|---|
  | default (iterative scans off, ef_search 40) | 0.986 | 0.772 |
  | ef40, ef100, ef200, scan1m, strict | 0.986 | 0.770 to 0.772 |
  | ef400 | 0.889 | 0.739 |
  | ef1000 | 0.000 | 0.730 |
  | exact | 0.000 | 0.000 |

  On M the share depends on selectivity (default setting): 0.06 to 0.14 at 0.06%, 0.61 to 1.00
  at 0.5%, 1.00 from 2% up, in every regime; the planner picks the exact GIN plan for most of the
  smallest filters. On E, raising `hnsw.ef_search` to 1,000 moved every search to a non-HNSW plan (recall@10
  1.000 at p50 169.7 ms, against 0.670 at 17.9 ms with ef_search 200): pgvector's cost estimate
  grows with `ef_search`, and above some value the exact plan is cheaper to the planner. Relation to
  the plan-cache finding (`x1-underretrieval-run2.md`): X2 never prepared the search statement
  (psycopg `prepare_threshold=None`), so no generic plan could arise; with custom plans 98.6% of the
  enterprise searches used HNSW, matching X1 run 2's `pg-custom` (98.6% on the same 1,489
  questions, 98.1% on the original ones) and the replay right after loading (98.1%), and recall@10 at ef_search 100 (0.661 on all 1,468
  scorable pairs; 0.7297 on the originals) matches `pg-custom` (0.656) and the audit (0.732). The
  remaining switches to exact plans in X2 are the custom planner's own choices (tiny filters on M;
  ef_search 1,000 on E), not the plan cache.

## X2 verdicts (as printed)

| Hypothesis | Verdict |
|---|---|
| H2.1 negative correlation costs recall at defaults | inconclusive |
| H2.2 local axes predict recall better than global selectivity | falsified |
| H2.3 effort narrows the gap but does not close it | confirmed |
| H2.4 the hardest filters are the intermediate ones | confirmed |

### H2.1: inconclusive

M, setting `default`, s in {2%, 10%, 30%}, both shapes; G = recall@10(U) - recall@10(C, N); 1,200
pairs in each group per store.

- pgvector: G 0.4242 [0.4154, 0.4332], positive in 5 of 5 seeds: gap
- qdrant: G 0.0343 [0.0196, 0.0487], positive in 5 of 5 seeds: unclear
- elasticsearch: G 0.1371 [0.1242, 0.1500], positive in 5 of 5 seeds: gap
- opensearch: G -0.0014 [-0.0029, 0.0001], positive in 2 of 5 seeds: no gap
- weaviate: G 0.0549 [0.0478, 0.0618], positive in 5 of 5 seeds: gap
- redis: G -0.0794 [-0.0871, -0.0719], positive in 0 of 5 seeds: unclear
- milvus: G 0.0136 [0.0080, 0.0194], positive in 5 of 5 seeds: no gap
- mongodb: G -0.0037 [-0.0055, -0.0019], positive in 0 of 5 seeds: no gap
- lancedb: G 0.2535 [0.2423, 0.2649], positive in 5 of 5 seeds: gap
- stores with a gap: 4 (confirm at 6); with no gap: 3 (falsify at 5)

Why: the stores split. Four lose recall to negative correlation (pgvector, LanceDB, Elasticsearch,
Weaviate); three lose none at these selectivities (OpenSearch, MongoDB, Milvus), recall staying at
0.97 to 1.00; Qdrant's gap is real but below the threshold; and Redis is reversed. Chroma could not
change the verdict: with six gaps needed, it would have made at most five. Three readings from the
build-0 jobs (`x2_frontier.csv`, groups shape):

- **Redis pays in latency instead of recall.** At default (EF_RUNTIME 10) N questions at 10% and
  30% reached recall@10 1.000 and 1.000 at p50 56.8 and 147.1 ms (17.5 and 6.8 QPS), U questions
  0.908 and 0.858 at 2.2 and 2.7 ms (389 and 357 QPS). Consistent with Redis's documented switch
  from batches to ad hoc brute force when the batches yield few matches [inference]. OpenSearch
  and MongoDB show the same pattern more mildly: OpenSearch N at 10% p50 24.6 ms against U 15.3 ms;
  MongoDB N at 10% 68.0 ms against U 33.3 ms, recall 0.99 to 1.00 in both.
- **Qdrant: correlation interacts with selectivity.** Recall@10 at default, U / N / P: 2% 0.024 /
  0.312 / 0.808; 10% 0.433 / 0.439 / 0.954; 30% 0.818 / 0.565 / 0.985. At 2% a random 2% of the
  graph is the worst case (its permitted subgraph is fragmented), topical groups are better
  connected; at 30% the negative regime is the worst. The pooled G (0.034) averages opposite signs.
- **pgvector at its documented default** (iterative scans off) returns at most ef_search 40
  candidates before filtering: recall@10 on C, N, groups shape is 0.000 at 2% and 10% (H2.4 table
  below), and 32.4% of all M retrievals and 61.6% of E retrievals came back empty.

### H2.2: falsified

M, `default`, all cells; D = |Spearman(recall@10, rho_1000)| - |Spearman(recall@10, sigma_g)|.

- pgvector: D 0.3650 [0.3321, 0.3989], 3578 pairs below 1: local
- qdrant: D -0.2032 [-0.2194, -0.1876], 2760 pairs below 1: global
- elasticsearch: D 0.2439 [0.2116, 0.2754], 4600 pairs below 1: local
- opensearch: D -0.0601 [-0.0793, -0.0411], 94 pairs below 1: not assessable
- weaviate: D -0.3900 [-0.4159, -0.3644], 1294 pairs below 1: global
- redis: D -0.0757 [-0.0870, -0.0647], 899 pairs below 1: global
- milvus: D -0.5307 [-0.5469, -0.5140], 1545 pairs below 1: global
- mongodb: D -0.0804 [-0.1016, -0.0593], 318 pairs below 1: global
- lancedb: D 0.5382 [0.5080, 0.5674], 6198 pairs below 1: local
- assessable 8, local 3, global 5

Spearman correlations with recall@10 (point estimates, `x2_h22.csv`):

| Store | sigma_g | rho_1000 | rho_100 | ACORN corr. | GLS | alpha_hat | log r1 |
|---|---|---|---|---|---|---|---|
| pgvector | -0.201 | 0.566 | 0.623 | 0.665 | 0.571 | 0.089 | -0.525 |
| Qdrant | -0.417 | 0.214 | 0.252 | 0.391 | 0.293 | 0.366 | -0.173 |
| Elasticsearch | -0.185 | 0.429 | 0.478 | 0.562 | 0.493 | 0.113 | -0.429 |
| OpenSearch | -0.167 | -0.107 | -0.086 | 0.009 | 0.001 | 0.170 | 0.080 |
| Weaviate | -0.473 | 0.083 | 0.126 | 0.315 | 0.206 | 0.435 | -0.066 |
| Redis | -0.427 | -0.352 | -0.293 | -0.068 | -0.083 | 0.471 | 0.283 |
| Milvus | -0.577 | -0.046 | 0.011 | 0.263 | 0.156 | 0.551 | 0.040 |
| MongoDB | -0.261 | -0.180 | -0.153 | 0.000 | -0.024 | 0.278 | 0.144 |
| LanceDB | -0.026 | 0.564 | 0.555 | 0.672 | 0.628 | -0.068 | -0.611 |

Why: the stores split by mechanism. Where recall depends on what lies near the question (pgvector's
scan in distance order, LanceDB's probed partitions, Elasticsearch), local selectivity and ACORN's
correlation predict it; where the store switches its search path on the filter's estimated size
(Qdrant's cardinality threshold, Weaviate's flat-search cutoff, Redis's hybrid policy, Milvus,
MongoDB), the global selectivity does, because the small filters are searched exactly
[interpretation]. HCBGen's over-fetch estimate correlates positively with recall in most stores
(0.278 to 0.551), the wrong sign for a hardness measure: it grows as R shrinks, where these stores
search exactly. Recall by bin at default (`x2_axes.csv`): pgvector 0.933 / 0.503 / 0.394 / 0.639 by
sigma_g bin (<= 0.1%, <= 1%, <= 10%, > 10%) and 0.340 / 0.330 / 0.310 / 0.917 / 0.936 by rho_1000
bin (0, <= 0.01, <= 0.1, <= 0.5, > 0.5); Qdrant 1.000 / 1.000 / 0.574 / 0.840 by sigma_g and
0.737 / 0.899 / 0.471 / 0.914 / 0.970 by rho_1000.

### H2.3: confirmed

- pgvector (ef1000): G 0.4242 -> 0.1721 [0.1611, 0.1830], narrowing [0.2383, 0.2661]
- elasticsearch (nc10000): G 0.1371 -> 0.1617 [0.1506, 0.1727], narrowing [-0.0342, -0.0147]
- weaviate (ef1024): G 0.0549 -> 0.0041 [0.0014, 0.0068], narrowing [0.0448, 0.0567]
- lancedb (np500): G 0.2535 -> 0.2523 [0.2411, 0.2636], narrowing [0.0002, 0.0022]
- stores with a gap and a sweep: 4; narrowed and remaining: 2; closed: 1

Lowest sweep level reaching recall@10 >= 0.95 (s 2% to 30%), U / N: pgvector 4 (ef400) / none;
Weaviate 2 (ef128) / 3 (ef256); Elasticsearch none / none; LanceDB none / none. The two that narrowed
and remained (pgvector, LanceDB) make half; Elasticsearch's gap widened (more candidates helped U
more than N); Weaviate's closed. LanceDB's narrowing (0.0012) is negligible: its default index
loses to quantization, not to probing (recall@10 0.424 to 0.451 for nprobes 10 to 500, 0.908 with
refine_factor 30).

### H2.4: confirmed

M, `default`, C with N queries, groups shape; V = recall@10 at 0.06% minus the lowest among 0.5%,
2%, 10%.

- pgvector: V 0.9267 [0.8867, 0.9600], 5 seeds: U-shaped
- qdrant: V 0.5403 [0.5165, 0.5653], 5 seeds: U-shaped
- elasticsearch: V 0.2338 [0.2032, 0.2650], 5 seeds: U-shaped
- opensearch: V 0.0005 [0.0000, 0.0015], 1 seeds: neither
- weaviate: V 0.1780 [0.1578, 0.1980], 5 seeds: U-shaped
- redis: V 0.0000 [0.0000, 0.0000], 0 seeds: monotone
- milvus: V 0.1037 [0.0925, 0.1150], 5 seeds: U-shaped
- mongodb: V 0.0012 [0.0005, 0.0020], 4 seeds: neither
- lancedb: V -0.0098 [-0.0332, 0.0212], 3 seeds: monotone
- U-shaped 5 (confirm at 5), monotone 2 (falsify at 5)

Recall@10 by level (0.06% / 0.5% / 2% / 10%): pgvector 0.927 / 0.380 / 0.000 / 0.000; Qdrant 1.000 /
1.000 / 0.460 / 0.489; Elasticsearch 0.841 / 0.727 / 0.641 / 0.607; Weaviate 1.000 / 1.000 / 1.000
/ 0.822; Milvus 1.000 / 1.000 / 1.000 / 0.896; OpenSearch 1.000 / 1.000 / 1.000 / 0.9995; Redis
1.000 throughout; MongoDB 1.000 / 1.000 / 1.000 / 0.999; LanceDB 0.197 / 0.210 / 0.235 / 0.207.
Redis and MongoDB are flat at 1.0 (brute force at these sizes), OpenSearch nearly so; LanceDB is
flat at its quantization floor.

## X2 settings (from `stats/report.md`)

Recall@10 is the mean over three builds (exact settings one build) with the 95% interval; p50 is
the median per-pair latency over the builds' rows (latency is compared only within a job).

MS MARCO (6,200 pairs; Qdrant per-tenant 3,000):

| Store | default | sweep (level 1 ... 5) | store-specific | exact |
|---|---|---|---|---|
| pgvector | 0.575 [0.570, 0.581], empty 0.324, 5.6 ms | ef40 0.885, ef100 0.897, ef200 0.907, ef400 0.917, ef1000 0.927 | scan1m 0.949, strict 0.878 | 1.000 (998 pairs), 636.0 ms |
| Qdrant | 0.799 [0.796, 0.803], 5.1 ms | ef64 0.771, ef128 0.813, ef256 0.849, ef512 0.878, ef1024 0.898 | acorn 0.983 (13.6 ms), acorn-max 0.997 (32.3 ms); per-tenant ef128 0.854, ef512 0.919, acorn-max 0.919 | 1.000, 16.0 ms |
| Elasticsearch | 0.806 [0.803, 0.810], 4.5 ms | nc50 0.826, nc100 0.833, nc500 0.862, nc2000 0.873, nc10000 0.878 | | 1.000, 6.8 ms |
| OpenSearch | 0.998, 7.3 ms | ef32 0.995, ef64 0.997, ef128 0.998, ef256 0.999, ef512 0.999 | | 1.000, 16.0 ms |
| Weaviate | 0.968, 6.8 ms | ef64 0.955, ef128 0.973, ef256 0.985, ef512 0.991, ef1024 0.994 | sweeping 0.995 (7.3 ms), noflat 0.812 | 1.000, 12.6 ms |
| Redis | 0.971, 4.1 ms | ef50 0.982, ef100 0.988, ef200 0.993, ef500 0.997, ef1000 0.999 | batches 0.960 | 1.000, 17.8 ms |
| Milvus | 0.972, 12.7 ms | ef32 0.982, ef64 0.989, ef100 0.994, ef256 0.998, ef512 0.999 | | none |
| MongoDB | 0.996, 20.5 ms | nc20 0.979, nc50 0.992, nc200 0.998, nc1000 1.000, nc10000 1.000 | | 1.000, 31.3 ms |
| LanceDB | 0.437, 11.6 ms | np10 0.424, np50 0.447, np100 0.450, np200 0.450, np500 0.450 | refine 0.908 (23.7 ms), postfilter 0.175 (empty 0.534) | 1.000, 73.7 ms |
| FAISS | | | | 1.000, 993.2 ms |
| Chroma | not measured | | | none |

Enterprise (1,468 scorable pairs; Chroma 381 to 407):

| Store | default | sweep | store-specific | exact |
|---|---|---|---|---|
| pgvector | 0.112, empty 0.616 | ef40 0.641, ef100 0.661, ef200 0.670, ef400 0.754, ef1000 1.000 | scan1m 0.787, strict 0.504 | 1.000 |
| Qdrant | 0.641 | ef64 0.604, ef128 0.663, ef256 0.727, ef512 0.794, ef1024 0.864 | acorn 0.830, acorn-max 0.953; per-tenant ef128 0.941, ef512 0.983, acorn-max 0.983 | 1.000 |
| Elasticsearch (bbq_hnsw) | 0.815 | nc50 0.826, nc100 0.841, nc500 0.867, nc2000 0.873, nc10000 0.881 | | 1.000 |
| Elasticsearch (int8_hnsw) | 0.888 | nc50 0.919, nc100 0.940, nc500 0.966, nc2000 0.975, nc10000 0.988 | | 1.000 |
| OpenSearch | 0.948 | ef32 0.914, ef64 0.938, ef128 0.954, ef256 0.970, ef512 0.982 | | 1.000 |
| Weaviate | 0.923 | ef64 0.892, ef128 0.934, ef256 0.963, ef512 0.979, ef1024 0.991 | sweeping 0.923, noflat 0.837 | 1.000 |
| Redis | 0.987 | ef50 0.990, ef100 0.991, ef200 0.994, ef500 0.993, ef1000 0.995 | batches 0.865 | 1.000 |
| Milvus | 0.864 | ef32 0.905, ef64 0.928, ef100 0.920, ef256 0.968, ef512 0.983 | | none |
| MongoDB | 0.953 | nc20 0.873, nc50 0.927, nc200 0.972, nc1000 0.995, nc10000 1.000 | | 1.000 |
| LanceDB | 0.439 | np10 0.432, np50 to np500 0.439 | refine 0.896, postfilter 0.043 (empty 0.790) | 1.000 |
| Chroma | 0.983 | ef10 to ef1000 0.983 to 0.984, p50 996 to 1,000 ms | | none |
| FAISS | | | | 1.000 |

Build-to-build range of recall@10 at default: largest for Qdrant on M, 0.759 to 0.878 (range 0.119);
every other store's default within 0.037 (pgvector E 0.092 to 0.129).

## Frontier data (proposed figure `fig:qual-frontiers`)

One panel per store, MS MARCO, x = recall@10 (mean over three builds, table above), y = queries per
second of one client in the build-0 job (`x2_frontier.csv`, cell `all`, median of three passes),
marking default, sweep, store-specific and exact. QPS, build 0:

| Store | default | sweep (levels 1 to 5) | specific | exact |
|---|---|---|---|---|
| pgvector | 75.3 | 16.2, 16.1, 16.1, 15.7, 14.8 | scan1m 12.9, strict 16.2 | 0.26 |
| Qdrant | 205.3 | 215.2, 194.9, 166.7, 129.9, 96.7 | acorn 69.1, acorn-max 28.5; per-tenant ef128 151.8, ef512 97.3, acorn-max 99.6 | 22.6 (per-tenant 16.6) |
| Elasticsearch | 185.1 | 150.3, 161.7, 148.4, 131.9, 107.2 | | 52.1 |
| OpenSearch | 105.3 | 124.0, 113.5, 106.4, 96.5, 91.5 | | 15.8 |
| Weaviate | 136.1 | 145.0, 141.2, 117.4, 101.7, 77.1 | sweeping 104.3, noflat 138.7 | 24.8 |
| Redis | 54.1 | 54.6, 53.8, 54.3, 52.9, 49.9 | batches 40.8 | 17.0 |
| Milvus | 68.6 | 71.9, 145.1, 144.9, 122.4, 98.1 | | |
| MongoDB | 24.1 | 28.1, 25.9, 21.8, 17.2, 10.3 | | 18.7 |
| LanceDB | 67.9 | 80.9, 44.5, 27.9, 24.3, 24.1 | refine 37.9, postfilter 129.8 | 4.6 |
| FAISS | | | | 0.91 |

Build-0 recall@10 differs from the three-build mean mostly for Qdrant (default 0.760 in build 0).
Enterprise build-0 points (QPS): e.g. pgvector default 456.5 at 0.128 (empty answers are fast),
ef100 42.5 at 0.660, ef1000 7.8 at 1.000 (exact plan); Qdrant default 219.8 at 0.639, ef1024 103.5
at 0.854, acorn-max 122.4 at 0.956, per-tenant ef128 197.2 at 0.937; Elasticsearch int8 nc500 270.7
at 0.966; Weaviate ef1024 66.8 at 0.991; Chroma 1.0 QPS at 0.984 for every ef_search.

A second figure (`fig:qual-axes`) could plot recall@10 at default by rho_1000 bin and by sigma_g
bin per store (`x2_axes.csv`; values for pgvector and Qdrant above).

## X5 verdicts (as printed)

| Hypothesis | Verdict |
|---|---|
| H5.1 a count certifies short results without false alarms | confirmed |
| H5.2 exact repair removes empty and short results | confirmed |
| H5.3 the repairs cost nothing on untriggered queries | inconclusive |
| H5.4 repairs do not touch mis-retrieval | confirmed |
| H5.5 the recall monitor sees what complete cannot | confirmed |
| H5.6 widening is not a certificate | confirmed |
| H5.7 store-native layout fixes what library repairs cannot | confirmed |

- **H5.1:** e pgvector: false alarms 0, detection 1.0000 of 992, exhausted without min(k, R) hits
  0; e qdrant: 0 truly short first searches (< 10): not judged; m pgvector: false alarms 0,
  detection 1.0000 of 574, exhausted without min(k, R) hits 0; m qdrant: false alarms 0, detection
  1.0000 of 1091, exhausted without min(k, R) hits 0.
- **H5.2:** pgvector e: report short 992; exact-inf empty or short 0; recall@10 on 576 triggered
  1.0000. pgvector m: report short 574; exact-inf empty or short 0; recall@10 on 323 triggered
  1.0000. qdrant e: report has 0 short results (< 10): not judged. qdrant m: report short 1091;
  exact-inf empty or short 0; recall@10 on 644 triggered 1.0000.
- **H5.3:** 60 median latency ratios (repair arm over report, untriggered pairs, per build): 45 in
  [0.95, 1.05]; 14 below 0.95 (minimum 0.8662, Qdrant M build 0 widen); 1 above 1.05 (1.0542,
  Qdrant M build 2 exact-10k); none above 1.10. Full list in `report.md`. Why inconclusive: the
  ratios outside the band are mostly arms *faster* than report (12 of the 14 on Qdrant: E build 2
  exact-1k 0.9433, exact-10k 0.9443, exact-inf 0.9446, widen 0.9480; M build 0 exact-1k 0.8795,
  exact-10k 0.9238, widen 0.8662; M build 1 count 0.9438, exact-1k 0.9464, exact-10k 0.9324,
  exact-inf 0.9478, widen 0.8700; pgvector E build 2 exact-inf 0.9427 and M build 2 widen 0.9184).
  The arms run in a fixed order after report in each build, so this is consistent with the store's
  latency drifting during a build rather than with any cost or saving of the arms [interpretation;
  not established]. No arm slowed untriggered queries beyond the falsification bound.
- **H5.4:** report: false-completeness 0.5808 (confirm needs >= 0.20); count, exact-1k, exact-10k,
  exact-inf, widen: 0.5726 each, minus report -0.0082 [-0.0270, 0.0000]. The small decrease comes
  from short answers to people with fewer than k readable chunks, which the count marks exhausted
  and complete (they are maximal); Qdrant on E had no truly short first search, so no answer was
  repaired [consistent with trigger rate 0.014 and 0 truly short].
- **H5.5:** (a) sampled within the 99.9% binomial interval in all 12 builds: E pgvector 52, 56, 55
  of 5,956; E Qdrant 48, 65, 53 of 5,956; M pgvector 255, 239, 219 of 24,800; M Qdrant 210, 267,
  248 of 24,800. (b) agreement within 0.1 on 1767 sampled retrievals: 1.0000. (c) Qdrant e: mean
  sampled 0.6843 on 166, population 0.6541, difference 0.0302; Qdrant m: mean sampled 0.8116 on
  725, population 0.8074, difference 0.0042.
- **H5.6:** exact-inf minus widen on 421 triggered pairs: 0.0849 [0.0640, 0.1096], Wilcoxon p
  5.582e-30.
- **H5.7:** per-tenant layout recall@10 0.9386; best library arm 0.6535.

### X5 arms (`x5_arms.csv`; k = 10 unless marked; latency in ms, per-pair median of three passes)

Columns: recall@5, recall@10, empty, short, trigger (first search short), detection (truly short
first searches flagged `missed`), false completeness, p50, p99, and on triggered retrievals the
time spent on the short result (`shortfall_ms`: count plus repair) at p50 and p95. "--": the arm
does not count (report, monitor, native arms), so it flags nothing and spends nothing on a short
result.

| Corpus, store | Arm | R@5 | R@10 | Empty | Short | Trigger | Detect | FC | p50 | p99 | trig. p50 | trig. p95 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E, pgvector | report | 0.639 | 0.667 | 0.089 | 0.116 | 0.129 | -- | 0.551 | 17.3 | 92.5 | -- | -- |
| | count | 0.639 | 0.667 | 0.089 | 0.116 | 0.129 | 1.000 | 0.542 | 17.7 | 114.1 | 14.7 | 25.6 |
| | exact-1k | 0.747 | 0.782 | 0.000 | 0.000 | 0.129 | 1.000 | 0.480 | 17.6 | 122.7 | 25.3 | 30.6 |
| | exact-10k | 0.747 | 0.782 | 0.000 | 0.000 | 0.129 | 1.000 | 0.480 | 17.3 | 120.9 | 25.2 | 30.3 |
| | exact-inf | 0.747 | 0.782 | 0.000 | 0.000 | 0.129 | 1.000 | 0.480 | 17.2 | 127.2 | 30.1 | 40.2 |
| | widen | 0.739 | 0.775 | 0.000 | 0.000 | 0.129 | 1.000 | 0.498 | 17.9 | 410.7 | 34.5 | 360.9 |
| | monitor | 0.639 | 0.667 | 0.089 | 0.116 | 0.129 | -- | 0.551 | 17.6 | 96.1 | -- | -- |
| | max_scan_tuples 1M alone | 0.664 | 0.694 | 0.072 | 0.090 | 0.103 | -- | 0.543 | 17.6 | 128.9 | -- | -- |
| E, Qdrant | report | 0.658 | 0.654 | 0.000 | 0.000 | 0.014 | -- | 0.581 | 4.72 | 6.15 | -- | -- |
| | count, exact-*, widen | 0.658 | 0.654 | 0.000 | 0.000 | 0.014 | n/a | 0.573 | 4.59 to 4.60 | 5.86 to 5.91 | 1.57 to 1.58 | 1.69 to 1.84 |
| | monitor | 0.658 | 0.654 | 0.000 | 0.000 | 0.014 | -- | 0.581 | 4.71 | 6.00 | -- | -- |
| | ACORN 1.0 alone | 0.857 | 0.855 | 0.000 | 0.000 | 0.014 | -- | 0.388 | 4.84 | 6.35 | -- | -- |
| | per-tenant graphs | 0.938 | 0.939 | 0.000 | 0.000 | 0.014 | -- | 0.235 | 4.69 | 8.27 | -- | -- |
| M, pgvector | report | 0.896 | 0.900 | 0.003 | 0.017 | 0.017 | -- | 0.301 | 9.87 | 425.4 | -- | -- |
| | count | 0.896 | 0.900 | 0.003 | 0.017 | 0.017 | 1.000 | 0.301 | 9.83 | 427.7 | 21.7 | 87.7 |
| | exact-1k | 0.900 | 0.904 | 0.001 | 0.012 | 0.017 | 1.000 | 0.299 | 9.82 | 426.1 | 60.0 | 129.2 |
| | exact-10k | 0.909 | 0.915 | 0.000 | 0.001 | 0.017 | 1.000 | 0.296 | 10.0 | 486.9 | 115.8 | 365.8 |
| | exact-inf | 0.909 | 0.915 | 0.000 | 0.000 | 0.017 | 1.000 | 0.296 | 10.0 | 446.5 | 108.6 | 220.7 |
| | widen | 0.907 | 0.913 | 0.000 | 0.000 | 0.017 | 1.000 | 0.306 | 9.89 | 772.1 | 594.4 | 1,572.7 |
| | monitor | 0.896 | 0.900 | 0.003 | 0.017 | 0.017 | -- | 0.301 | 10.2 | 433.2 | -- | -- |
| | max_scan_tuples 1M alone | 0.899 | 0.903 | 0.003 | 0.016 | 0.016 | -- | 0.299 | 10.0 | 429.4 | -- | -- |
| M, Qdrant | report | 0.809 | 0.807 | 0.000 | 0.035 | 0.035 | -- | 0.356 | 6.07 | 10.7 | -- | -- |
| | count | 0.809 | 0.807 | 0.000 | 0.035 | 0.035 | 1.000 | 0.356 | 6.02 | 26.5 | 21.7 | 28.2 |
| | exact-1k | 0.809 | 0.807 | 0.000 | 0.035 | 0.035 | 1.000 | 0.356 | 5.80 | 25.8 | 21.1 | 28.3 |
| | exact-10k | 0.809 | 0.807 | 0.000 | 0.035 | 0.035 | 1.000 | 0.356 | 5.95 | 26.4 | 21.6 | 27.9 |
| | exact-inf | 0.833 | 0.842 | 0.000 | 0.000 | 0.035 | 1.000 | 0.343 | 6.10 | 44.4 | 37.9 | 50.4 |
| | widen | 0.833 | 0.841 | 0.000 | 0.000 | 0.035 | 1.000 | 0.349 | 5.56 | 117.8 | 97.4 | 148.5 |
| | monitor | 0.809 | 0.807 | 0.000 | 0.035 | 0.035 | -- | 0.356 | 5.15 | 10.6 | -- | -- |
| | ACORN 1.0 alone | 0.987 | 0.986 | 0.000 | 0.000 | 0.000 | n/a | 0.085 | 15.9 | 125.7 | -- | -- |

Repair rates (fallback `exact` or `widened`, k = 10): E pgvector 0.115 for exact-* and widen; M
pgvector exact-1k 0.005, exact-10k 0.017, exact-inf and widen 0.017; M Qdrant exact-1k and exact-10k
0.000, exact-inf and widen 0.035. Qdrant's short answers on M all had more than 10,000 readable
chunks, so the bounded exact repair held every one over the bound (`over_limit`, complete False).

## Observations beyond the rules

- Qdrant under-retrieves on MS MARCO: 3.5% of k = 10 retrievals at hnsw_ef 128 returned fewer
  than k hits while more were readable (never on the enterprise corpus, as in X0 and X1).
- Redis at default EF_RUNTIME 10 had a higher p50 on the enterprise corpus (19.0 ms) than at
  EF_RUNTIME 200 (2.7 ms); with negatively correlated questions on M it returned exact answers 25 to
  50 times slower than for uncorrelated ones.
- Weaviate: its default filter strategy (ACORN) reached 0.968 on M against 0.995 with `sweeping`
  (7.3 against 6.8 ms p50); equal on E (0.923). Turning off the flat-search cutoff cost 0.086 (E)
  and 0.156 (M).
- Elasticsearch's default `bbq_hnsw` index cost recall against `int8_hnsw` on E (0.815 against
  0.888 at defaults; 0.867 against 0.966 at num_candidates 500).
- pgvector's raised tuple limit alone (1,000,000) lowered E's empty rate only from 0.089 to 0.072,
  as X1 run 2 found (both scan limits bind).
- Chroma: changing `ef_search` from 10 to 1,000 through the collection configuration was read back
  as applied but changed neither recall (0.983 to 0.984) nor latency (996 to 1,000 ms p50) on E;
  not explained.

## Possible defects (library, harness, vendors)

- **Harness:** the warm-up is outside the setting's budget and the job deadline is checked only
  between settings; with Chroma at about 2 min per retrieval this consumed every budget and ran
  one job past the runner limit. No other store came near it.
- **Chroma 1.5.9 (vendor, performance):** 137 to 221 s per filtered retrieval over a million
  passages (about 1 s on 107,540 chunks); in X3 4.3 s with one group over 100,000. The layer's
  Chroma encoding (one boolean key per list value, here up to 31 per passage and about 111,000
  distinct keys) may contribute; not isolated. `ef_search` changes had no measurable effect.
- **Library (by design, worth stating):** with `max_exact_rows` 10,000, Qdrant's short answers on
  MS MARCO were never repaired (all over the bound); the result says so (`over_limit`,
  complete False). `complete` stays True on full answers that are wrong: 0.58 of Qdrant's complete
  answers on E and 0.30 to 0.36 on M were not maximal; only the monitor sees this.
- No leak and no wardowl defect were found.
