# Investigation: Qdrant's 0.56 recall and pgvector's empty results in the 2026-10-24 Kaggle run

> Note added 2026-11-07: the X0 numbers in this note are the printed aggregates of X0's first execution (2026-10-24), then
> described in `evidence/kaggle-scale-run-2026-10-24.md`. The artifact now holds X0's second execution
> (`evidence/x0-scale-run.md`), in which pgvector also ran in its fast mode (recall@5 0.703, recall@10 0.725, p50 7.8 ms) but
> returned no empty answer, and Qdrant reached recall@5 0.537 and recall@10 0.530. The reasoning below is unchanged.

Written 2026-10-26. Read-only investigation: no code in the wardowl repository was changed and nothing
was run against a store. Input: `evidence/kaggle-scale-run-2026-10-24.md`.

Conventions:

- **Code references** are `file:line` in the wardowl repository at commit `5c1d04a`. Every file cited
  is byte-identical to tag `v2.1.0` = commit `bf25bd0f`, the commit the run used (checked with
  `git diff v2.1.0 -- <files>`; only `enterprise_rag.ipynb` changed since then, in its first cell).
- **Store references** are to official docs, or to source at the exact versions the run used:
  pgvector `v0.8.7` (`benchmarks/kaggle_setup.sh:6`) and Qdrant `v1.19.2` (`benchmarks/kaggle_stores.sh:62`).
- **[unverified]** marks an inference or estimate that I did not confirm from code, docs or data.
- **[derived]** marks a number I computed from the scenario code or the published results, not one
  the run printed.

---

## 0. Summary

Both gaps come from the same property of the scenario. Near a query, the permission filter is
**anti-correlated with similarity**: it is misaligned with the vector geometry. Each store fails
in its own way under that misalignment.

- The shared FiQA knowledge base (57,600 of 107,540 chunks) carries **every** tenant in its
  `tenant` field and is readable by `employees` and `contractors`. A typical person therefore reads
  about 54% of the corpus overall (median 58,641). Near a question about a company document,
  though, they read only 2 to 5%: the 19 other tenants' near-duplicate copies are all denied.
  `judy` (only `board`, no `employees`) reads 624 chunks (0.58%), all in three templates of her own
  tenant, and none of the knowledge base.
- **Qdrant (recall@10 0.561, answer accuracy 0.399).** Qdrant's filtered HNSW traversal **drops
  neighbours that fail the filter**: they are neither scored nor expanded. Its extra
  "filterable HNSW" edges are built only for payload values that hold more than
  `full_scan_threshold` points (about 3,333 here) and no more than about `4/avg_links` of a segment.
  The values that matter fall outside that window: every `tenant` value covers 56% of the points,
  `employees` 65% and `contractors` 61%, so they get **no** extra edges. A typical person's search
  is therefore confined to the permitted subgraph. That subgraph is dense in the knowledge-base
  region and broken into islands in the company-document region, so the search returns FiQA
  passages instead of the person's own documents. `judy`'s filter is small enough that Qdrant's
  planner switches to **exact** search over the payload index. That is why Qdrant gave her results
  and pgvector did not. ACORN, the remedy Qdrant ships, was not enabled. With its default gate
  (`max_selectivity` 0.4) it might not engage for these filters anyway (Section 2.2).
- **pgvector (empty results for 10 judys, recall@10 0.732).** pgvector applies the filter *after*
  the index. Iterative scans keep going only until **20,000 visited graph elements**
  (`hnsw.max_scan_tuples`) or until **`work_mem` × `hnsw.scan_mem_multiplier` = 4 MB** of scan
  memory, whichever comes first. `PG_TUNE=1` does not raise `work_mem`, so it stays at
  PostgreSQL's 4 MB default. For a `judy` question whose neighbourhood holds none of her 624 chunks
  (her forbidden question in most cases), the scan returns 0 rows. wardowl then reports
  `complete=True`, because an empty pre-filtered result is unconditionally marked complete
  (`wardowl/retriever.py:407-408`). Empty results explain at most about 1.1 points of the
  26.8-point recall@10 gap (Section 3.1). The rest is mis-retrieval: k rows come back but not the
  true top k. The causes are `ef_search=100` against a filter that passes about 5% of each
  neighbourhood, relaxed ordering cut off by `LIMIT k` inside the CTE, and a default index
  (`m=16`, `ef_construction=64`).
- **Fixes.**
  - Benchmark: give both stores settings matched to the permission filter (Qdrant ACORN with
    `max_selectivity=1.0`, or per-tenant graphs; pgvector higher `max_scan_tuples`, `work_mem` and
    `ef_search`, and a deeper `LIMIT`). Report exact-search reference numbers per store, and log
    store diagnostics.
  - wardowl:
    - Stop calling a short approximate result complete.
    - Detect under-retrieval (fewer than k hits while a count shows at least k readable chunks)
      and fall back to exact search, bounded by a row budget.
    - Expose the pgvector scan limits.
    - Add a sampled exact-recall monitor for the mis-retrieval that `complete` can never see.
- **Before spending Kaggle time,** the existing `answers.jsonl` from the run can confirm most of
  this offline (Section 6.0).

---

## 1. What the run configured (code facts)

### 1.1 Corpus, people and permissions

| Item | Value | Source |
|---|---|---|
| Company documents | 20 tenants x 12 templates x 208 variants = 49,920; 2,496 per tenant; 4,160 per template across tenants | `acceptance/kaggle/enterprise_rag.py:560-611`, `:96` |
| Injected notices | 20, one per tenant, readers `employees`, `contractors` | `enterprise_rag.py:614-621`, `:517` |
| Shared KB (FiQA) | 57,600 passages, `tenant` = list of all 20 tenants, readers `employees`, `contractors` | `enterprise_rag.py:624-639`, `:544` |
| Near-duplicates | Every tenant writes every template with the same 208 entity names, so each document has 19 near-identical copies in other tenants that only the tenant rule tells apart | `enterprise_rag.py:224-226`, `:571` |
| Template readers | handbook-leave and handbook-it: employees, contractors; handbook-expenses: employees; salary-bands: hr, user:carol; performance-case: user:alice; medical-leave: hr; forecast: finance, board; acquisition: board; postmortem: engineering; credentials-runbook: sre; msa-renewal: legal, user:carol; litigation-memo: legal, board | `acceptance/enterprise.py:64-173` |
| `judy` | `("board",)`, a non-executive board member, in each of the 18 generated tenants | `enterprise_rag.py:188-199` |
| `mallory` | no groups: reads 0 chunks (the run's "min 0"), so excluded from recall and from the empty-results check | `enterprise.py:55`, `enterprise_rag.py:2011`, `:2087-2088` |
| Policy | `AllOf(TenantAuthorizer(), MetadataACLAuthorizer())` | `enterprise_rag.py:798-799` |

Readable sets [derived]:

| Person | Readable chunks | Share | Where they lie |
|---|---|---|---|
| `judy` (generated tenant) | forecast + acquisition + litigation-memo of her tenant = 3 x 208 = **624** | 0.58% | three templates of one tenant; no KB, no notice |
| typical employee (for example `dave`: employees, engineering, sre) | 57,600 KB + 1 notice + 5 templates x 208 = **58,641** (the run's median) | 54.5% | 98% of it is the KB. In the company region (49,920 docs) they read 1,040, i.e. 2.1%; inside one readable template's 4,160 cross-tenant copies they read 5% |
| `carol` (employees, finance, board) | 59,265 (the run's max) | 55.1% | |

Payload/metadata value cardinalities over the whole collection [derived]:

| Field = value | Points | Share |
|---|---|---|
| `tenant` = any one tenant | 2,496 + 1 + 57,600 = 60,097 | 55.9% |
| `allowed_groups` = employees | 57,600 + 20 + 3 x 4,160 = 70,100 | 65.2% |
| `allowed_groups` = contractors | 57,600 + 20 + 2 x 4,160 = 65,940 | 61.3% |
| `allowed_groups` = board | 3 x 4,160 = 12,480 | 11.6% |
| `allowed_groups` = hr / legal | 8,320 each | 7.7% |
| `allowed_groups` = finance / engineering / sre | 4,160 each | 3.9% |
| `allowed_users` = one person | at most 416 (two templates name `<tenant>-carol`; 832 for Northwind's and Globex's `carol`) | under 1% |

The filter for `judy` in tenant T is
`And(In(tenant, [T]), Or(In(allowed_users, {T-judy}), In(allowed_groups, {board, *})))`
(`wardowl/authz.py:78-84`, `:172-175`, `:266-270`).

### 1.2 Ground truth and the metrics

- **Exact baseline.** One GPU matrix product of all question vectors against all chunk vectors.
  Unreadable rows (per the oracle `readable`, which never calls wardowl) are masked to -inf, then
  `topk(10)` is taken (`enterprise_rag.py:1845-1877`, mask at `:1829-1843`, oracle at `:660-665`).
  FAISS `IndexFlatIP` reproduces it at recall 1.000, which validates the pipeline (check at
  `:2038-2043`).
- **Recall@k.** The share of the exact top k among the first k hits. A hit counts if it is readable
  and its similarity, recomputed from the run's own vectors, is at least the k-th exact score minus
  1e-4, so ties do not penalise (`enterprise_rag.py:2082-2096`). Questions with no readable chunk
  are excluded.
- **Two calls per question.** Recall@5 is computed on the k=5 retrieval and recall@10 on a separate
  k=10 retrieval (`enterprise_rag.py:1952-1954`, `:2030-2037`). For pgvector these are different
  SQL `LIMIT`s, so they are different scans.
- **"Everyone who may read something got results"** fails when a k=5 retrieval returns `[]` while
  the exact baseline is non-empty. The failure detail prints `sorted(set(empty))[:5]`
  (`enterprise_rag.py:2010-2016`).

### 1.3 pgvector as run

- PostgreSQL 16.15 with pgvector 0.8.7. `PG_TUNE=1` sets only `shared_buffers=4GB`,
  `effective_cache_size=16GB` and `max_parallel_workers_per_gather=2`; **`work_mem` stays at the
  4 MB default** (`benchmarks/kaggle_setup.sh:20-26`, `enterprise_rag.py:1181-1183`).
- The schema is `metadata jsonb` with a GIN `jsonb_path_ops` index. The HNSW index was built
  **after** the bulk load, with **default parameters (m=16, ef_construction=64)**, then the table
  was `ANALYZE`d (`wardowl/backends/pgvector.py:169-184`, `enterprise_rag.py:1199-1205`).
- The backend is `PgVectorBackend(pool, None, table=NAME, ef_search=100)`, with the default
  `iterative_scan="relaxed_order"` (`enterprise_rag.py:1216-1219`, `pgvector.py:220`).
- Per search, `SET LOCAL hnsw.iterative_scan = 'relaxed_order'` and `SET LOCAL hnsw.ef_search = 100`
  run in the search's transaction (`pgvector.py:325-336`, `:348-351`). **`hnsw.max_scan_tuples`
  and `hnsw.scan_mem_multiplier` cannot be set through the backend; they stayed at 20,000 and 1.**
- The SQL is
  `WITH candidates AS MATERIALIZED (SELECT ... embedding <=> $q AS distance FROM t WHERE <filter> ORDER BY distance LIMIT $k) SELECT ... ORDER BY distance, id`
  (`pgvector.py:284-296`). The filter is an OR/AND tree of `metadata @> '{"field": v}'` and
  `metadata @> '{"field": [v]}'` tests (`pgvector.py:41-94`).
- Statements run through psycopg 3 with the default `prepare_threshold=5`, so a statement is
  server-prepared after 5 executions on a connection and the server may then switch to a generic
  plan ([psycopg API](https://www.psycopg.org/psycopg3/docs/api/connections.html),
  [PostgreSQL PREPARE, Notes](https://www.postgresql.org/docs/current/sql-prepare.html)).
  Whether that happened here is [unverified].

### 1.4 Qdrant as run

- Qdrant v1.19.2, one node, default collection config:
  `VectorParams(size=768, distance=COSINE)` with no `hnsw_config` and no `optimizers_config`, hence
  m=16, ef_construct=100 and full_scan_threshold=10,000 KB
  (`wardowl/backends/qdrant.py:197-202`; defaults in
  [Qdrant indexing docs](https://qdrant.tech/documentation/concepts/indexing/)).
- Keyword payload indexes on `metadata.allowed_users`, `metadata.allowed_groups`, `metadata.tenant`
  and `wardowl_id`. They are created **before** any point is uploaded, so the HNSW build could use
  them. None is `is_tenant` (`enterprise_rag.py:1314-1315`, `qdrant.py:203-205`).
- After loading, the run waits until the collection status is green (`enterprise_rag.py:1317`).
- Search is `query_points(query=<vector>, query_filter=<filter>, search_params=SearchParams(hnsw_ef=128), limit=k, with_payload=True)`,
  with **no `exact` and no `acorn`** (`enterprise_rag.py:1324-1330`, `qdrant.py:323-348`, `:369-375`).
  The filter is `must[ tenant MatchAny[T], Filter(should=[allowed_users MatchAny, allowed_groups MatchAny]) ]`
  (`qdrant.py:143-172`).

### 1.5 What `complete` does today

- `_prefilter` returns `complete=True` whenever the backend returned **no hits at all**
  (`wardowl/retriever.py:404-408`). Otherwise `complete` is `violations == 0`
  (`retriever.py:418-420`).
- The docstring states the limit: `complete` "trusts the backend's ranking, so it cannot see results
  an approximate index failed to return" (`retriever.py:101-104`).
- The user docs go further and are contradicted by this run. `docs/concepts.md:151-157` says that
  for pgvector iterative scans are "what keeps a selective filter from cutting results short".
  `docs/integrations/pgvector.md:73-79` says they "keep scanning until enough rows pass", which
  leaves out the stop conditions.

---

## 2. How the two stores behave (docs and source, October 2026)

### 2.1 pgvector 0.8.7

- **The filter is applied after the index.** "With approximate indexes, filtering is applied
  *after* the index is scanned." Iterative scans continue "until enough results are found (or it
  reaches `hnsw.max_scan_tuples` ...)". Relaxed ordering returns slightly out-of-order results and
  should be wrapped in a materialized CTE, which wardowl does.
  ([README: Filtering](https://github.com/pgvector/pgvector#filtering),
  [README: Iterative index scans](https://github.com/pgvector/pgvector#iterative-index-scans))
- **Scan options.**
  - `hnsw.max_scan_tuples`: "max number of tuples to visit (20,000 by default)". It "is approximate
    and does not affect the initial scan".
  - `hnsw.scan_mem_multiplier`: "max amount of memory to use, as a multiple of `work_mem`
    (1 by default)". The README advises raising it "if increasing `hnsw.max_scan_tuples` does not
    improve recall" ([README](https://github.com/pgvector/pgvector#iterative-index-scans)).
  - Registered in [hnsw.c#L102-L109](https://github.com/pgvector/pgvector/blob/v0.8.7/src/hnsw.c#L102-L109).
- **What the limits count, from source.**
  - The stop test is `so->tuples >= hnsw_max_scan_tuples || MemoryContextMemAllocated(so->tmpCtx) > so->maxMemory`,
    where `maxMemory = work_mem * hnsw_scan_mem_multiplier * 1024 + 256` bytes
    ([hnswscan.c#L160-L161](https://github.com/pgvector/pgvector/blob/v0.8.7/src/hnswscan.c#L160-L161),
    [#L264](https://github.com/pgvector/pgvector/blob/v0.8.7/src/hnswscan.c#L264)).
  - `tuples` counts **visited graph elements** (each newly seen neighbour), not rows returned or
    rows that passed the filter: "OK to count elements instead of tuples"
    ([hnswutils.c#L874-L909](https://github.com/pgvector/pgvector/blob/v0.8.7/src/hnswutils.c#L874-L909)).
  - When a limit is hit, the scan stops exploring the graph, emits the candidates it had already
    discarded (in distance order), then ends
    ([hnswscan.c#L263-L271](https://github.com/pgvector/pgvector/blob/v0.8.7/src/hnswscan.c#L263-L271)).
  - Each resumed iteration processes `ef_search` discarded candidates
    ([hnswscan.c#L64-L91](https://github.com/pgvector/pgvector/blob/v0.8.7/src/hnswscan.c#L64-L91)).
  - So a scan examines roughly the 20,000 elements nearest the query along the graph, and returns
    nothing when none of them passes the `WHERE` clause.
  - pgvector emits no NOTICE when a limit is hit; the only diagnostic needs a compile-time
    `HNSW_MEMORY` flag. The cut-off is invisible to the caller.
- **`strict_order` can drop rows**: elements closer than the previous one are skipped
  (`continue`), not reordered
  ([hnswscan.c#L318-L323](https://github.com/pgvector/pgvector/blob/v0.8.7/src/hnswscan.c#L318-L323)).
  It is no fix for recall.
- **Which limit binds first is [unverified].** Scan memory holds, per visited element, a TID-hash
  entry, a search candidate and an element struct with up to 10 heap TIDs; it does not hold the
  vector ([hnswutils.c](https://github.com/pgvector/pgvector/blob/v0.8.7/src/hnswutils.c)). At an
  estimated 200 to 250 bytes per element, 4 MB allows about 16,000 to 20,000 elements. The memory
  limit may therefore stop the scan before `max_scan_tuples` does. That is exactly the case where
  the README's hint applies.
- **Remedies the README itself offers:** a partial index per filter value, for "only a few distinct
  values", and partitioning, for "many different values"
  ([README: Filtering](https://github.com/pgvector/pgvector#filtering)).
- **Changelog.** 0.8.0 (2024-10-30) added iterative scans and "Improved cost estimation for better
  index selection when filtering". 0.8.1 to 0.8.7 (to 2026-10-01) contain no change to scan stop
  behaviour ([CHANGELOG](https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md)).

### 2.2 Qdrant 1.19.2

- **Query planning is per segment.**
  - The planner estimates the filter's cardinality from the payload indexes
    ([search docs, Query planning](https://qdrant.tech/documentation/search/search/)).
  - In source: if `exact`, plain search. If `cardinality.max < full_scan_threshold`, plain search
    over the payload index, which is **exact over the filtered points**. If
    `cardinality.min > full_scan_threshold`, filtered HNSW. Otherwise a sampled cardinality check
    decides
    ([dispatch.rs#L95-L200](https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/hnsw_index/hnsw/read_view/dispatch.rs#L95-L200)).
  - `full_scan_threshold` is in KB of vectors, converted to points by dividing by the average vector
    size ([hnsw.rs#L192-L210](https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/hnsw_index/hnsw.rs#L192-L210)).
    For 768-d float32 that is 10,000 x 1024 / 3,072 = **3,333 points** [derived].
  - `must` estimates multiply the clauses' fractions (an independence assumption), take
    `min = max(0, sum of mins - (n-1) x total)` and `max = min of maxes`. `should` takes
    `max = sum of maxes` (capped at the total) and `min = max of mins`
    ([query_estimator.rs#L135-L217](https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/query_estimator.rs#L135-L217)).
- **Filtered traversal discards non-matching neighbours.**
  - At level 0 and in the upper-level greedy descent, `score_points` keeps only neighbours that pass
    the filter (`check_batched(..., Select::Matches, Rest::Discard)`). Failing nodes are never
    scored or expanded
    ([point_scorer.rs#L266-L281](https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/hnsw_index/point_scorer.rs#L266-L281),
    [graph_layers.rs#L116-L152](https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/hnsw_index/graph_layers.rs#L116-L152),
    [#L301-L337](https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/hnsw_index/graph_layers.rs#L301-L337)).
  - The search therefore walks only the subgraph induced by permitted points, plus the extra
    payload edges below.
- **Extra "filterable HNSW" edges are built only for some payload values.**
  - Docs: Qdrant "extend[s] the HNSW graph with additional edges based on indexed payload values",
    built only for indexes that exist at build time
    ([indexing docs](https://qdrant.tech/documentation/concepts/indexing/)).
  - Qdrant's own article: edges are built "per payload field, never per combination", and "a value
    shared by more points than a size cap gets no extra edges"
    ([ACORN article](https://qdrant.tech/articles/filtered-vector-search-acorn/)).
  - Source, per segment and per keyword value:
    1. the value must hold **more than `full_scan_threshold` points**
       ([str.rs#L327-L347](https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/field_index/map_index/payload_index_impl/str.rs#L327-L347));
    2. it must hold **at most `total / avg_level0_links x 4` points**
       ([additional_links.rs#L147-L165](https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/hnsw_index/hnsw/build/additional_links.rs#L147-L165));
    3. for non-tenant fields after the first, the extra graph is skipped if the main graph is
       already well connected on those points (lines 186-201 of the same file).
  - Level 0 has at most 2m = 32 links, so the cap is at most about 4/avg_links of the segment:
    12.5% at 32 links, 17% at 24 [unverified average].
  - **Consequences here [derived]:**
    - Every `tenant` value (56%), `employees` (65%) and `contractors` (61%) exceeds the cap at any
      plausible link count, so they **never** get extra edges.
    - `board`, `hr` and `legal` get them only if a segment holds more than 3,333 points with that
      value, which depends on the number of segments.
    - User values are far below 3,333 and never get extra edges.
  - `is_tenant` lifts only condition 3 ("Always build for tenants"), not the cap in condition 2, so
    **`is_tenant` alone would not help** this layout [derived from the cited lines].
- **ACORN.**
  - ACORN (Qdrant 1.16, November 2025) explores neighbours of neighbours when direct neighbours are
    filtered out. It is enabled per query, needs no index change, and costs about 2 to 10 times the
    latency
    ([1.16 release](https://qdrant.tech/blog/qdrant-1.16.x/),
    [search docs](https://qdrant.tech/documentation/search/search/)).
  - It engages only when the **estimated** selectivity `cardinality.exp / available_vectors` is at
    most `max_selectivity`, default **0.4**
    ([dispatch.rs#L222-L254](https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/hnsw_index/hnsw/read_view/dispatch.rs#L222-L254),
    [types.rs#L624](https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/types.rs#L624);
    Python `models.AcornSearchParams(enable=True, max_selectivity=...)`,
    [qdrant-client models](https://github.com/qdrant/qdrant-client/blob/master/qdrant_client/http/models/models.py)).
  - Qdrant's benchmark (v1.18.2) shows the failure mode and the fix. With two filters whose
    intersection is 4%, recall goes from 39.7% at default settings to 100% with ACORN. Raising `ef`
    did not rescue a plain graph "trapped on a disconnected island"
    ([ACORN article](https://qdrant.tech/articles/filtered-vector-search-acorn/)).
  - **For this run [derived, unverified numerically]:** the independence estimate for a typical
    employee is about 0.56 x 0.65 to 0.69, i.e. 0.36 to 0.39, just under 0.4, while the true
    selectivity is about 0.54. The default gate would engage for some people and not others,
    depending on group mix and segment. `max_selectivity=1.0` makes it deterministic.
- **Multitenancy layout.** A keyword index with `is_tenant=true`, plus `hnsw_config` with
  `payload_m=16` and `m=0`, builds per-tenant graphs and no global graph
  ([multitenancy docs](https://qdrant.tech/documentation/manage-data/multitenancy/)). With `m=0` the
  size cap does not apply (`max_block_size = usize::MAX`, additional_links.rs#L152-L156).
- **Segments and indexing.** The default segment count follows the CPU count, and segments below
  the indexing threshold (10,000 KB in the config example) stay plain, i.e. brute force
  ([optimizer docs](https://qdrant.tech/documentation/ops-optimization/optimizer/)). New points go
  to a random or the smallest appendable segment
  ([segment_holder/mod.rs#L694-L740](https://github.com/qdrant/qdrant/blob/v1.19.2/lib/shard/src/segment_holder/mod.rs#L694-L740)),
  so the final segment composition (how KB and company points mix per segment) is
  [unverified].

### 2.3 Contrast: Lucene (Elasticsearch, OpenSearch)

Lucene's earlier filtered HNSW search **scored filtered-out nodes and used them for navigation**.
Lucene 10.2 added an ACORN-1-style search with bounded neighbour-of-neighbour exploration
([Elastic Search Labs](https://www.elastic.co/search-labs/blog/filtered-hnsw-knn-search)). Both
avoid Qdrant's trapping, which fits ES and OpenSearch reaching 0.94 to 0.95 recall at
`num_candidates=500`. Which algorithm ES 9.5.5 and OpenSearch 3.9.0 actually ran is [unverified].

---

## 3. Evidence already in the published results [derived]

### 3.1 Under-retrieval is about 1% of pgvector's questions; the recall gap is mostly mis-retrieval

- **Expected hit total.** A question yields k=5 plus k=10 hits, so 15 when nothing is short.
  `mallory`'s 21 questions yield 0, and the 20 end-to-end questions add 5 each:
  1,105 x 15 - 21 x 15 + 20 x 5 = **16,360**. That is exactly what every store except pgvector
  checked.
- **pgvector's shortfall.** pgvector checked 16,178, so it is **182 hits short**. An empty question
  costs 15, because both `LIMIT 5` and `LIMIT 10` stop at the same scan budget, so **at most 12
  questions were empty**. At least 10 were (10 people). That is 10 to 12 of 1,084 scorable
  questions.
- **How much recall that explains.** Empty questions cost at most 12/1,084, about 0.011, of
  recall@10; the observed gap is 0.268. **About 96% of pgvector's recall loss is mis-retrieval**:
  k hits came back, but not the true top k.
- **Qdrant** checked all 16,360 hits, so **all** of its loss is mis-retrieval; it never returned
  short.
- **pgvector's recall@5 (0.691) is below its recall@10 (0.732),** the largest such gap among the
  stores; ES and OpenSearch are flat. This fits relaxed ordering cut off early. With `LIMIT 5` the
  CTE takes the first 5 permitted rows *in emission order*; with `LIMIT 10` the scan goes deeper and
  the outer `ORDER BY` repairs more of the order.

### 3.2 The failing `judy` questions

Each `judy` asks 2 targeted questions (on her readable kinds), 1 forbidden question and 2 red-team
prompts. Her index in `people()` is `i = 16 + 10g` for generated tenant number g
(`enterprise_rag.py:202-207`). The forbidden kind is `denied[i % 9]`, over the 9 kinds she may not
read in sorted order, and the red-team prompts are `REDTEAM[(2i) % 8]` and `REDTEAM[(2i+1) % 8]`
(`enterprise_rag.py:759-773`). So:

| g | Tenant | Forbidden question about | Red-team prompts | Empty in pgvector? |
|---|---|---|---|---|
| 0 | northwind-eu | postmortem | ignore-instructions, claimed-identity | **yes** |
| 1 | globex-labs | salary-bands | other-tenant-facts, admin-override | no |
| 2 | contoso | credentials-runbook | ignore-instructions, claimed-identity | **yes** |
| 3 | fabrikam | handbook-expenses | other-tenant-facts, admin-override | **yes** |
| 4 | tailspin | handbook-it | ignore-instructions, claimed-identity | ? |
| 5 | wingtip | handbook-leave | other-tenant-facts, admin-override | ? |
| 6 | woodgrove | medical-leave | ignore-instructions, claimed-identity | ? |
| 7 | litware | msa-renewal | other-tenant-facts, admin-override | no |
| 8 | proseware | performance-case | ignore-instructions, claimed-identity | ? |
| 9 | lucerne | postmortem | other-tenant-facts, admin-override | no |
| 10 | adatum | salary-bands | ignore-instructions, claimed-identity | no |
| 11 | fourthcoffee | credentials-runbook | other-tenant-facts, admin-override | no |
| 12 | coho | handbook-expenses | ignore-instructions, claimed-identity | **yes** |
| 13 | alpine | handbook-it | other-tenant-facts, admin-override | no |
| 14 | blueyonder | handbook-leave | ignore-instructions, claimed-identity | **yes** |
| 15 | wideworld | medical-leave | other-tenant-facts, admin-override | ? |
| 16 | relecloud | msa-renewal | ignore-instructions, claimed-identity | ? |
| 17 | treyresearch | performance-case | other-tenant-facts, admin-override | ? |

How the "yes" and "no" were read. The failure detail lists the alphabetically first five failing
ids. So every id that sorts before `northwind-eu-judy` and is not listed did **not** fail. That
includes adatum, alpine, fourthcoffee, globex-labs, litware and lucerne. If all 10 failures are
judys, 5 of the 7 "?" failed. This reading assumes the evidence file quotes the check's detail
verbatim.

What the pattern suggests [inference]:

- Empties track the **forbidden question**. handbook-expenses failed 2 of 2; salary-bands 0 of 2.
  Salary text ("earns between ... a year ... staff engineer") plausibly lies nearer `judy`'s
  forecast documents ("revenue ... gross margin ... hiring stays frozen outside engineering") than
  travel and meal allowances do. Those sit among 12,480 site-handbook documents and FiQA passages
  on expenses.
- Postmortem and credentials fail for one of two tenants each. The result therefore sits near the
  scan budget, and depends on the random entity drawn and on the HNSW graph.
- The empties are thus mostly on questions **where nothing relevant is readable**. The assistant
  should abstain there anyway, so the practical harm in this run is small. The contract "top k of
  what the subject may read" is still broken, and the same mechanism would hide a *relevant* but
  distant readable document. Section 6.0 settles this from `answers.jsonl`.

### 3.3 Qdrant's pattern

- Target found in top 5 is **0.399** for Qdrant, against 0.947 for pgvector and 0.99 to 1.0 for the
  rest. "Generic kind in top 5" is 0.600, against 0.825 to 1.0.
- These questions are about the person's **own company documents**, which sit in the region where
  only 2 to 5% of points are permitted. This is what a search confined to the permitted subgraph
  and stuck in the KB region predicts.
- Latency is very low and tight (p50 4.3 ms, p99 6.5 ms), which fits short, trapped graph searches
  rather than long ones.
- No Qdrant empties for `judy` also fits. Per segment, her filter's `max` estimate is at most the
  `board` count (12,480/S for S segments) and her true count is 624/S. The planner takes plain,
  exact search directly when 12,480/S < 3,333 (S ≥ 4), or after the sampled check otherwise.
- **Prediction:** Qdrant's recall for `judy` is about 1.0, and the loss sits in typical users'
  company-document questions.

---

## 4. Ranked hypotheses

### 4(a) Qdrant: recall@10 0.561

**Q1 (most likely, primary cause). Traversal is confined to an islanded permitted subgraph, with
no compensating payload edges.**

For typical people the filter passes about 54% of points, so the planner takes filtered HNSW. The
traversal discards non-matching neighbours. Near company-document queries only the person's own
tenant's copies pass, 1 in 20 of each near-duplicate group, and the tenant and employee values are
too common to get extra edges. The search descends into and stays in the FiQA region, which is
entirely permitted, and returns KB passages.

- For:
  - the source behaviour (Section 2.2: point_scorer.rs, graph_layers.rs, the additional_links.rs
    cap);
  - value cardinalities of 56 to 65% against a cap of about 12 to 17%;
  - target found 0.399;
  - no short results (an islanded search still fills k from the KB);
  - flat low latency;
  - Qdrant's own benchmark of the same failure (4% intersection: 39.7% recall by default).
- Against or open:
  - per-question data not examined yet;
  - segment composition unknown: a segment holding only company points would give tenant values
    about 5% per segment, below the cap, and extra edges would be built there;
  - whether the HNSW entry point lands in the KB region is not measured.
- Decisive test: on the existing outputs, the share of `kb/` hits in Qdrant's top 5 against
  FAISS's, by category (6.0). Then ACORN on and off, and per-tenant graphs (6.3).

**Q2 (contributing, configuration). ACORN was not enabled, and its default gate would engage
unreliably.**

Neither `acorn` nor `exact` was sent (`enterprise_rag.py:1329`). The estimated selectivity for
typical people sits near the 0.4 gate.

- For: the docs, dispatch.rs.
- Against: none; it is a configuration fact. What is unknown is how much ACORN recovers when local
  permitted density is about 2%: two hops reach about 32 x 32 neighbours, roughly 20 permitted
  [estimate].

**Q3 (contributing). Per-segment planning and segment composition.**

Extra edges and the plan are decided per segment. The segment count (CPU count, 4) and mix are
unknown, so recall may vary between builds of the same data.

- For: the docs and source.
- Against: cannot by itself explain 0.56.
- Test: force one segment against the default, and record `segments_count`.

**Q4 (unlikely). `hnsw_ef=128` too low.**

- Against: the ACORN article found that raising `ef` does not escape islands in a plain graph.
- Test: `hnsw_ef` 512. Prediction: under +0.05.

**Q5 (ruled out by code and logic). Collection not indexed, or payload indexes created after the
graph.**

- The indexes are created before upload and the run waits for green (`enterprise_rag.py:1314-1317`).
- An unindexed segment is searched plain, which is exact, and would *raise* recall.
- Still record `indexed_vectors_count == points_count` in the experiment.

**Q6 (unlikely). An artefact of the metric or the harness.**

- The same recall code gives FAISS 1.000 and ES 0.948.
- Qdrant cosine normalises vectors, and the run's vectors are unit length (`enterprise_rag.py:1822-1826`).
- wardowl's `_hits` re-sorts by score and id (`qdrant.py:350-367`), which does not change the set.

### 4(b) pgvector: empty results for 10 people, recall@10 0.732

**P1 (most likely, for the empties). The iterative scan budget runs out before any readable row.**

`judy`'s 624 rows are clustered in three templates. For questions in other regions (the forbidden
question) the scan explores about 20,000 graph elements, about 19% of the index, whichever limit
binds first, and none passes the filter. Zero rows come back, and wardowl marks the result
complete.

- For:
  - the source (Section 2.1);
  - failures only for the one persona without the KB;
  - 10 to 12 empty questions, about one per affected judy, matching one forbidden question each;
  - the pattern by forbidden kind (Section 3.2);
  - the identical failures under OPA, which produces the same filter semantics, so the store is the
    cause, not the authorizer;
  - `complete` stayed True, as `retriever.py:407-408` dictates.
- Open: which limit binds (tuples or memory; the 4 MB `work_mem` is suspect), and whether a
  relevant readable document was ever hidden.
- Decisive test: EXPLAIN (ANALYZE, BUFFERS) on the empty queries ("Rows Removed by Filter" equals
  the rows the scan emitted). Then vary `max_scan_tuples` and `scan_mem_multiplier` separately
  (6.2).

**P2 (most likely, for the recall gap). Mis-retrieval from shallow, relaxed scans in a sparse
neighbourhood.**

To return a typical person's top 10 in a company region, the scan must deliver roughly the 200
nearest elements correctly: about 10 variants times about 20 tenant copies [estimate]. `ef_search`
is 100 and later batches are resumed approximately. Relaxed order with `LIMIT k` inside the CTE
takes the first k permitted rows in emission order. The default index (`m=16`,
`ef_construction=64`) is built on data full of near-duplicates.

- For:
  - 96% of the loss is mis-retrieval (3.1);
  - recall@5 < recall@10 (3.1);
  - target found stays high at 0.947, because the single nearest own-tenant copy is easy and the
    rest of the near-tied top k is not.
- Against or open: no per-category data yet. Some loss may be near-ties just above the 1e-4
  tolerance, which a similarity-gap metric would show (6.5).

**P3 (possible, contributing to P1). The planner misjudges how selective the filter is.**

jsonb containment selectivity is estimated per clause and combined under independence. For `judy`
that is about 0.56 x 0.12, roughly 7,000 rows, against 624 true [estimate]. A correct estimate
might make the planner choose the GIN bitmap scan plus sort, which is exact and cheap for 624 rows.
The anti-correlation of tenant and groups (the KB is in every tenant but only for employees and
contractors) is what misleads it.

- Test: EXPLAIN estimated against actual rows; the same query with `enable_indexscan=off` (6.2).

**P4 (low prior). Generic plans after psycopg prepares the statement.**

After 5 executions with the same SQL text on a connection, PostgreSQL may switch to a generic plan
whose cost uses no parameter values.

- Test: `plan_cache_mode=force_custom_plan`, or `prepare_threshold=None`, against the default, and
  `EXPLAIN EXECUTE` on a prepared statement.
- Prediction: no difference.

**P5 (ruled out). Iterative scan not active, or dead tuples.**

- `SET LOCAL` runs in the same transaction as the query (`pgvector.py:348-351`).
- The table was created fresh and never updated (`enterprise_rag.py:1193-1205`).

---

## 5. Fixes

### 5.1 Configuration the scenario and benchmark should use

Report three numbers per store, not one:

- **as documented**: today's settings;
- **tuned for permission filters**: the settings below;
- **exact reference**: the store's own exact search, which must reach recall 1.0 and checks each
  harness end to end.

Readers then see the cost of the defaults and what a fix buys.

**pgvector:**

| Setting | Value to try | Why | Cost |
|---|---|---|---|
| `work_mem` (role or database, or `SET LOCAL`) | 64 MB | lifts the 4 MB scan-memory cap that may bind before `max_scan_tuples` | memory per concurrent scan |
| `hnsw.scan_mem_multiplier` | 4 to 16 | the same, without raising `work_mem` for sorts | as above |
| `hnsw.max_scan_tuples` | 100,000 to 1,000,000 | lets the scan reach misaligned readable rows | latency only on the queries that need it |
| `hnsw.ef_search` | 200, 400, 1000 | deeper first batch and larger resumed batches | latency on every query |
| Inner `LIMIT` | 4k to 10k, outer re-sort, keep k | repairs relaxed-order truncation (the @5 < @10 gap) | small |
| Index build | `m=24` or `32`, `ef_construction=128` to `200` | better graph on near-duplicate data | build time (27 s today) and size |
| Layout (optional) | KB in its own table; company rows partitioned by tenant, or a partial HNSW index per tenant | removes the misalignment at the source | schema change; queries two indexes and merges |
| Exact reference | `SET LOCAL enable_indexscan = off` (GIN bitmap plus sort, or a sequential scan) | ground truth inside the store | latency [unverified] |

These GUCs can be set today without any library change: `ALTER DATABASE bench SET hnsw.max_scan_tuples = ...`
and `ALTER ROLE ... SET work_mem = ...`.

**Qdrant:**

| Setting | Value to try | Why | Cost |
|---|---|---|---|
| `SearchParams(acorn=AcornSearchParams(enable=True, max_selectivity=1.0))` | on, gate 1.0 (and 0.4 for comparison) | second-hop exploration through denied nodes | 2 to 10x latency (from 4 ms) |
| `SearchParams(exact=True)` | reference, and a candidate production setting at this scale | exact over the filtered points | latency [unverified], about 58,000 x 768 dot products per typical query |
| Tenant index `is_tenant=True` plus `HnswConfigDiff(m=0, payload_m=16)` | per-tenant graphs | the cap does not apply with m=0, so each tenant, KB included, gets a connected graph | about 20 graphs of about 60,000 nodes [estimate]; global unfiltered search becomes slow |
| `is_tenant=True` alone | control | predicted **no** gain (cap unchanged) | none |
| Separate KB collection; company points with a single-valued tenant | layout | the company collection's tenant filter is about 5%, so the planner uses exact plain search; KB search barely filters | two searches merged by score |
| `optimizers_config.default_segment_number=1` | control | removes the per-segment variance | build time |
| `hnsw_ef` | 128, 512 | control for Q4 | latency |

**Both stores: log diagnostics with each result.**

- pgvector: EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) for a fixed sample and for every short result.
- Qdrant: collection info (`segments_count`, `indexed_vectors_count`) and `/telemetry` search
  counters, which show the path taken per segment: `small_cardinality` (plain), `large_cardinality`
  (graph), `acorn`, `exact_filtered` (the counter names come from dispatch.rs).

### 5.2 Library-level mitigations in wardowl

**(1) `complete` must not certify a short approximate result.**

Today `retriever.py:407-408` returns `complete=True` for an empty pre-filtered result, and a result
of 0 < n < k hits is also complete when there are no violations.

Proposal: a backend declares whether its search is exact, for example `exact_search: bool` (True
for `FaissBackend` with a flat index, or for Qdrant with `exact=True`). For an approximate backend,
a result with fewer than k hits is `complete=False` unless it was certified as in (2).

- Trade-off: people who really can read fewer than k chunks (`mallory`, or a new tenant) would be
  marked incomplete on every query unless (2) is on. That is noisy, but honest.
- Compatibility: this tightens a documented field (`retriever.py:101-104`). Ship it in a minor
  release with a changelog entry, as a correction of the field's documented meaning. The safety
  guarantees are untouched.

**(2) Certify or repair short results** (`short_results="exact" | "widen" | "report"`, per
retriever).

- Certify cheaply. A filter-only existence count (`count(filter, limit=k)`):
  - **If the count is at least k while fewer than k hits came back, under-retrieval is
    certain.** A detector with no false positives.
  - If the count equals the number of hits, the readable set is exhausted, and `complete=True` is
    honest.
  - Per store: pgvector `SELECT count(*) FROM (SELECT 1 FROM t WHERE <filter> LIMIT k) s`; Qdrant
    `count(filter, exact=True)`; Elasticsearch and OpenSearch `_count`.
- Repair, `"exact"`. Re-run the search exactly under the **same filter**: pgvector with
  `SET LOCAL enable_indexscan = off`, Qdrant with `exact=True`, ES/OpenSearch with `script_score`
  under the filter. Guard it with `max_exact_rows` (skip and report `complete=False` above it).
  - Under-retrieval mostly happens when the readable set is small, which is exactly when an exact
    scan is cheap: 624 rows for `judy`.
- Repair, `"widen"`. Repeat with larger store parameters (pgvector `max_scan_tuples` and
  `ef_search`, Qdrant `hnsw_ef` and ACORN, ES `num_candidates`) up to a cap. This can never certify
  completeness; it only reduces the empty-result rate.
- Interaction with the guarantees:
  - **Never leak.** The fallback is one more `_Search` with the filter already obtained, and its
    hits go through the same `_Check` re-check (`retriever.py:404-420`). Implement it inside the
    generator plan so that `retrieve` and `aretrieve` share it (`retriever.py:262-298`). No new data
    path is created.
  - **Fail closed.** Authorizer failures still raise `AuthorizationError` before any search. A
    failing *fallback search* should propagate like any backend error does today, by default. An
    opt-in `fallback_errors="degrade"` could return the first, already re-checked hits with
    `complete=False`.
  - **`complete` stays honest.** True only when the backend is exact, the fallback ran exactly, or
    the count proved exhaustion. Report `short`, `fallback` and `fallback_ms` in `RetrievalEvent`
    and in OpenTelemetry.
  - **Cost and abuse.** The fallback adds latency only on short results, bounded by
    `max_exact_rows`. Its timing tells the caller only what the short result already tells them,
    and nothing about other subjects.

**(3) Expose store scan parameters.**

- `PgVectorBackend(max_scan_tuples=..., scan_mem_multiplier=..., work_mem=...)`, set with
  `SET LOCAL` like the existing two (`pgvector.py:214-241`, `:325-336`).
- A `candidates=` (inner `LIMIT`) factor for the CTE (`pgvector.py:284-296`), the analogue of
  ES `num_candidates`.
- Qdrant already passes `search_params` through (`qdrant.py:238`, `:345`). Add per-call overrides
  so the fallback can switch to `exact` or ACORN.
- `create_collection(..., tenant_field=..., hnsw_config=...)` to build the `is_tenant` plus
  `m=0`/`payload_m` layout (`qdrant.py:175-205`).

**(4) Monitor what `complete` can never see.**

Mis-retrieval was 96% of pgvector's loss and 100% of Qdrant's, and it returns k hits that look
normal. An opt-in `recall_sample_rate` in the retriever would re-run a sampled share of queries
exactly, off the request path, and emit only recall@k and a similarity gap as metrics. It never
logs content, and the sampler uses the subject's own filter, so it sees only permitted chunks.

- Trade-off: extra load proportional to the rate.
- It needs the query and filter in hand, so it belongs in the retriever, not in an observer:
  observers receive only an HMAC of the query (`retriever.py:335-358`).

**(5) A score-merging union backend.**

For the "shared corpus separate from tenant data" layout: search two backends under the same
filter and merge by score when both use the same embedding model and metric. `RankFusion`
(`wardowl/fusion.py:1-17`) uses reciprocal rank fusion, which suits mixed scorers but discards
comparable cosine scores.

### 5.3 Documentation to correct (in the repository, for a later session)

- `docs/concepts.md:151-157`: iterative scans do not stop a selective filter from cutting results
  short. They stop at `hnsw.max_scan_tuples` or `work_mem` x `hnsw.scan_mem_multiplier`. Cite this
  run.
- `docs/integrations/pgvector.md:73-79`: name both stop conditions and the two GUCs. State that
  `work_mem` defaults to 4 MB.
- `docs/integrations/qdrant.md:86-92`: add ACORN and `max_selectivity`. Explain the payload-edge
  window and why a shared corpus in every tenant defeats it. Recommend the `is_tenant` plus
  `m=0`/`payload_m` layout or a separate shared collection.

---

## 6. Experiment plan (to run later on Kaggle; nothing was run now)

### 6.0 Offline re-analysis of the existing outputs (no store needed)

Download `results.json` and `answers.jsonl` (6.21 MB) from the notebook's output and archive them
(the evidence file asks for this too). `answers.jsonl` has, per store and question, the person,
the category, the target and the top-5 hit ids (`enterprise_rag.py:2136-2153`). This is light
parsing, fine on a laptop or a CPU-only Kaggle session.

1. **pgvector empties.** List the empty (store=pgvector, person, category, question) rows.
   Predicted: about 10 to 12 rows, all judys, mostly `forbidden`.
2. **Approximate recall@5 by category, person and store.** Use overlap with the FAISS row for the
   same question; FAISS is exact, and ties are ignored here. Predicted:
   - Qdrant near 1 for judys;
   - Qdrant low for targeted and generic questions of KB-reading people;
   - pgvector's loss concentrated in targeted and generic questions.
3. **KB share in Qdrant's top 5 against FAISS's top 5,** for targeted questions. Predicted: Qdrant
   mostly `kb/fiqa-*` where FAISS has tenant documents. This would confirm Q1 without rerunning.

### 6.1 Common setup

- Reuse `enterprise_rag.Run` for `build_corpus`, `embed` and `baseline`. The embedding `.npy` is
  cached under `/kaggle/working/cache` (`enterprise_rag.py:1798-1812`).
- **Skip the LLM**: retrieval only, which removes most of the 2.8 hours.
- One store at a time, as now.
- **Add a probe set for selectivity and alignment.** Single-group people in 3 tenants for each of
  the 8 groups (`hr`, `finance`, `board`, `engineering`, `sre`, `legal`, `contractors`,
  `employees`), and people with KB-only access, each asking all 12 template questions and 4 FiQA
  queries.
- From the exact GPU ranking (unfiltered and filtered), record per (question, person):
  - **R**, the readable count;
  - **r1**, the unfiltered rank of the first readable chunk;
  - **rk**, the unfiltered rank of the k-th readable chunk;
  - **local selectivity ρ_m**, the share of readable chunks in the unfiltered top m, for m = 100
    and 1,000.

  These are the alignment variables. Every result is reported against them.

### 6.2 pgvector experiments (query-time grid on one build; build-time variants rebuilt three times)

| ID | Variable | Levels | Tests |
|---|---|---|---|
| P-a | `hnsw.max_scan_tuples` x `hnsw.scan_mem_multiplier` (`work_mem` 4 MB) | {20k, 100k, 1M} x {1, 8} | P1, and which limit binds |
| P-b | `work_mem` | 4 MB, 64 MB (multiplier 1) | P1 |
| P-c | `hnsw.ef_search` | 40, 100, 200, 400, 1000 | P2 |
| P-d | inner `LIMIT` factor | 1x, 4x, 10x k (outer keeps k) | P2 (relaxed truncation) |
| P-e | `iterative_scan` | relaxed, strict | P2 (strict should not help; may drop rows) |
| P-f | index build | (16, 64), (32, 200) | P2 |
| P-g | plan control | default; `plan_cache_mode=force_custom_plan`; `prepare_threshold=None` | P4 |
| P-h | exact | `SET LOCAL enable_indexscan = off` | reference; P3 (also EXPLAIN estimated against actual rows) |

Instrumentation:

- EXPLAIN (ANALYZE, BUFFERS) on every short result and on 50 fixed queries: plan node, estimated
  against actual rows, "Rows Removed by Filter".
- Optionally a custom build with `-DHNSW_MEMORY` on one run to print memory and tuples per scan.
- **P1 is confirmed if:**
  - empties occur only where r1 exceeds the scan's reach;
  - raising the binding limit, and only that one, removes them;
  - "Rows Removed by Filter" equals the rows emitted, about 15,000 to 20,000 at the defaults.
- **P1 is falsified** if empties persist at 1M tuples and 16x memory.

### 6.3 Qdrant experiments (each layout rebuilt three times; query-time variants on each build)

| ID | Variable | Levels | Tests |
|---|---|---|---|
| Q-a | ACORN | off; on with `max_selectivity` 0.4; on with 1.0 | Q1, Q2 |
| Q-b | `hnsw_ef` | 64, 128, 512 | Q4 |
| Q-c | `exact` | True | reference |
| Q-d | layout | as run; `is_tenant` only; `is_tenant` + `m=0`, `payload_m=16`; separate KB collection | Q1 (predicted: no change, large gain, large gain) |
| Q-e | segments | default; `default_segment_number=1` | Q3 |

Instrumentation:

- Telemetry path counters per segment, before and after each pass.
- `segments_count` and `indexed_vectors_count`.
- For each query, the share of `kb/` hits.
- **Q1 is confirmed if:**
  - typical people take the `large_cardinality` path and judys `small_cardinality`;
  - Qdrant's misses are KB passages where the exact top k are tenant documents;
  - ACORN at 1.0 or per-tenant graphs recover recall above 0.9.

### 6.4 Library mitigation experiments (on a wardowl branch, after 5.2 is implemented)

Arms:

- pgvector and Qdrant as run;
- plus `short_results="report"`;
- plus `"exact"` with `max_exact_rows` at 1,000, 10,000 and infinite;
- plus `"widen"`;
- plus `recall_sample_rate` 1%.

Measure:

- the empty-result rate (ERR) and the short-result rate;
- recall;
- fallback trigger rate;
- latency overall and on triggered queries;
- the `complete` confusion matrix against the ground truth.

Every safety check of the acceptance run must still pass, with 0 leaks.

### 6.5 Metrics, repeats and statistics

Metrics, per (question, person) and aggregated by category, persona type and ρ bin:

- recall@5 and recall@10 (the existing definition);
- **ERR**: P(no hits | R ≥ 1), per question and per person;
- **short-result rate**: P(hits < min(k, R));
- **gross-miss rate**: the exact top 1 is absent;
- **similarity gap**: mean exact top-k similarity minus mean returned similarity. This separates
  near-tie misses (pgvector, predicted) from wrong-region misses (Qdrant, predicted);
- target found@5;
- latency p50, p95 and p99;
- **`complete` confusion**:
  - false-complete: `complete=True` but the hits are not the tie-aware exact top min(k, R);
  - false-incomplete: the reverse;
- fallback trigger rate and fallback latency.

Repeats:

- Query-time settings are deterministic on a fixed build, so variance comes from index builds and
  segment layout. Rebuild three times per build-time configuration.
- Run each query-time configuration on every build.
- For latency, take the median of 3 passes per query after the warm-up already in the harness
  (`enterprise_rag.py:1936-1938`).

Statistics:

- Paired comparisons on the same questions.
- 95% CIs by cluster bootstrap over persons (189 plus the probe set, 10,000 resamples).
- McNemar for ERR; Wilcoxon signed-rank on per-question recall.
- Report the effect with its CI, not just p-values.

Budget [estimate]:

- pgvector query-time grid of about 30 configurations x 2,210 retrievals at 5 to 50 ms each: under
  1 hour.
- Qdrant: 4 layouts x 3 builds x about 2 minutes to load and index, plus about 10 query
  configurations: about 1 to 1.5 hours.
- Exact baselines and the probe set: minutes on the T4.
- Fits one 12-hour Kaggle session with room for OpenFGA's rerun (180 s healthz timeout).

### 6.6 Pre-registered predictions

| Hypothesis | Prediction that would confirm | Result that would falsify |
|---|---|---|
| Q1 | Qdrant recall about 1 for judys and low for KB readers on company-document questions; misses are KB passages; ACORN at 1.0 or per-tenant graphs give recall at least 0.9 | Misses spread evenly over categories, or ACORN and m=0 give no gain |
| Q2 | ACORN at 0.4 engages for only part of the people (telemetry) and recovers less than 1.0 does | ACORN at 0.4 and at 1.0 give the same recall |
| Q3 | Recall varies between builds and with the segment count | Identical across builds and segment counts |
| Q4 | `hnsw_ef` 512 gains less than 0.05 | Gains of more than 0.15 |
| P1 | Empties only when r1 exceeds the scan's reach; removed by raising the binding limit | Empties persist at 1M tuples and 16x memory |
| P2 | Recall rises with `ef_search`, inner `LIMIT` and index quality; losses concentrated at ρ_100 below 0.1; small similarity gap | No change with `ef_search` 1000 |
| P3 | EXPLAIN shows an estimate of about 10 times the actual rows for judys; exact plans fix the empties | Estimates within 2x |
| P4 | No difference between plan modes | Recall or plan changes with plan mode |

---

## 7. Unverified points, collected

- Which pgvector limit stopped the scans (tuples against the 4 MB memory). The 200 to 250 bytes per
  element is an estimate.
- Qdrant segment count and composition in the run; the average level-0 link count (hence the exact
  edge cap).
- Whether Qdrant's default ACORN gate would engage for these filters. The estimates of 0.36 to 0.39
  assume the independence product in query_estimator.rs; the `should` combination formula was not
  read in full.
- Whether the PostgreSQL planner's row estimate for `judy` is about 7,000, and whether a correct
  estimate would pick an exact plan.
- Whether generic plans were used (psycopg `prepare_threshold=5`).
- Which filtered-kNN algorithm ES 9.5.5 and OpenSearch 3.9.0 used.
- Latency of exact search in Qdrant and pgvector at about 58,000 filtered rows.
- The judy table's "no" entries rest on the evidence file quoting the check detail (the first five
  ids in sorted order) verbatim.

## Sources

- pgvector README (Filtering; Iterative index scans; HNSW options): https://github.com/pgvector/pgvector#filtering and https://github.com/pgvector/pgvector#iterative-index-scans
- pgvector v0.8.7 source: https://github.com/pgvector/pgvector/blob/v0.8.7/src/hnswscan.c, https://github.com/pgvector/pgvector/blob/v0.8.7/src/hnswutils.c, https://github.com/pgvector/pgvector/blob/v0.8.7/src/hnsw.c
- pgvector changelog: https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md
- PostgreSQL PREPARE (custom and generic plans): https://www.postgresql.org/docs/current/sql-prepare.html
- psycopg 3 prepared statements and `prepare_threshold` (default 5): https://www.psycopg.org/psycopg3/docs/advanced/prepare.html and https://www.psycopg.org/psycopg3/docs/api/connections.html
- Qdrant indexing (filterable HNSW, full_scan_threshold, is_tenant): https://qdrant.tech/documentation/concepts/indexing/
- Qdrant search (search params, ACORN, query planning): https://qdrant.tech/documentation/search/search/
- Qdrant optimizer (indexing threshold, segments): https://qdrant.tech/documentation/ops-optimization/optimizer/
- Qdrant multitenancy (is_tenant, payload_m, m=0): https://qdrant.tech/documentation/manage-data/multitenancy/
- Qdrant 1.16 release (ACORN): https://qdrant.tech/blog/qdrant-1.16.x/
- Qdrant ACORN article and benchmark (v1.18.2): https://qdrant.tech/articles/filtered-vector-search-acorn/
- Qdrant v1.19.2 source:
  - https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/hnsw_index/hnsw/read_view/dispatch.rs
  - https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/hnsw_index/hnsw/build/additional_links.rs
  - https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/hnsw_index/point_scorer.rs
  - https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/hnsw_index/graph_layers.rs
  - https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/query_estimator.rs
  - https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/field_index/map_index/payload_index_impl/str.rs
  - https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/index/hnsw_index/hnsw.rs
  - https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/types.rs
  - https://github.com/qdrant/qdrant/blob/v1.19.2/lib/shard/src/segment_holder/mod.rs
- qdrant-client `AcornSearchParams`: https://github.com/qdrant/qdrant-client/blob/master/qdrant_client/http/models/models.py
- Lucene filtered HNSW (Elastic Search Labs): https://www.elastic.co/search-labs/blog/filtered-hnsw-knn-search
