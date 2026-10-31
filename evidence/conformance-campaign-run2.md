# Evidence: conformance campaign, GitHub Actions run 2

Source: repository `muzakkirhussain011/wardowl`, workflow `paper-conformance`, run #2, id 40905549149
(https://github.com/muzakkirhussain011/wardowl/actions/runs/40905549149), triggered by the push of
commit `182bcbc` to branch `paper/conformance-campaign` at 2026-10-29 15:50:07 UTC. The branch merges
`fix/engine-limits` at `e7776f0` (PR #167: `UnsupportedSubject` for OpenFGA and SpiceDB; SHA-256
digests for Redis and MongoDB terms over their index limits) and main `438a176` (#166). The package
still reports version 2.1.0. Read on 2026-10-29 from the run page and the merged job summary of the
`summary` job (signed-in browser); artifacts were not downloaded. Status: **Success**, 2 h 6 min 27 s,
10 artifacts, 10 jobs from the jobs API (`evidence/compute.md`): nine campaign jobs, with Keto in its
own job and Casbin split over two, and `summary` (corrected 2026-10-30; this line said 8). Triage that predicted these results:
`investigations/conformance-run1-triage.md`.

## Merged summary (copied)

Controls: memory 180 of 180 runs pass; metadata-acl 140 of 140 runs pass.

Wrong answers (leaks, filter and check disagreeing, altered metadata):
- cerbos: filter-check-disagree in 20 runs (variants scalar-fields; seeds 0-19); 235 disagreeing hits:
  the filter gives the reference answer for 235, check for 0.
- cerbos-tenant: filter-check-disagree in 19 runs (variants scalar-fields; seeds 0-10, 12-19); 45
  disagreeing hits: the filter gives the reference answer for 45, check for 0.

Others: none.

| Target | Family | Version | Status | Seeds | Runs | Pass | Violations | Refused | Errors |
|---|---|---|---|---|---|---|---|---|---|
| memory | store | in process | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| pgvector | store | pgvector 0.8.7, PostgreSQL 17.11 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| redis | store | 8.10.2 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| cassandra | store | 5.0.9 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| elasticsearch | store | 9.5.5 (Lucene 10.5.1) | complete | 20 | 180 | 160 | 0 | 0 | 20 |
| opensearch | store | 3.9.0 | complete | 20 | 180 | 160 | 0 | 0 | 20 |
| vespa | store | 8.763.13 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| qdrant | store | 1.19.2 | complete | 20 | 180 | 160 | 0 | 0 | 20 |
| milvus | store | 3.0.2 | complete | 20 | 180 | 140 | 0 | 0 | 40 |
| weaviate | store | 1.39.12 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| mongodb | store | Atlas Local 8.0.30 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| chroma | store | 1.5.9 | complete | 20 | 180 | 140 | 0 | 0 | 40 |
| lancedb | store | 0.40.0 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| faiss | store | 1.15.1 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| pinecone | store | | skipped: no PINECONE_API_KEY | 0 | 0 | 0 | 0 | 0 | 0 |
| metadata-acl | engine | in process | complete | 20 | 140 | 140 | 0 | 0 | 0 |
| opa | engine | 1.21.2 | complete | 20 | 140 | 140 | 0 | 0 | 0 |
| opa-tenant | engine | 1.21.2 | complete | 20 | 140 | 140 | 0 | 0 | 0 |
| openfga | engine | 1.22.0 | complete | 20 | 140 | 21 | 0 | 119 | 0 |
| openfga-tenant | engine | 1.22.0 | complete | 20 | 140 | 21 | 0 | 119 | 0 |
| spicedb | engine | 1.56.2 | complete | 20 | 140 | 16 | 0 | 124 | 0 |
| spicedb-tenant | engine | 1.56.2 | complete | 20 | 140 | 23 | 0 | 117 | 0 |
| cerbos | engine | 0.56.0 | complete | 20 | 140 | 120 | 20 | 0 | 0 |
| cerbos-tenant | engine | 0.56.0 | complete | 20 | 140 | 121 | 19 | 0 | 0 |
| keto | engine | v26.2.0 | complete | 20 | 140 | 140 | 0 | 0 | 0 |
| cedar | engine | cedarpy 4.12.2 | complete | 20 | 140 | 140 | 0 | 0 | 0 |
| cedar-tenant | engine | cedarpy 4.12.2 | complete | 20 | 140 | 140 | 0 | 0 | 0 |
| casbin | engine | 1.43.0 | complete | 20 | 140 | 140 | 0 | 0 | 0 |
| casbin-tenant | engine | 1.43.0 | complete | 20 | 140 | 140 | 0 | 0 | 0 |

Totals summed by hand from the table: 4,480 runs = 3,822 pass + 39 violations + 479 refused + 140
errors. Stores: 2,520 runs, 2,380 pass, 140 errors. Engines: 1,960 runs, 1,442 pass, 39 violations,
479 refused. Image digests are in the summary (for example pgvector `sha256:151aa1c2...`).

## Run 1 against run 2

| Finding | Run 1 | Run 2 | Predicted in the triage |
|---|---|---|---|
| Redis long and huge strings | 26 violations (missed) | 0 | yes |
| MongoDB long and huge strings | 19 violations (missed) | 0 | yes |
| OpenFGA, OpenFGA-tenant | 119 + 119 errors (HTTP 400) | 119 + 119 refused, 0 errors | yes (same runs refused; 21 pass each as before) |
| SpiceDB, SpiceDB-tenant | 124 + 117 errors (HTTP 400) | 124 + 117 refused, 0 errors | yes (16 and 23 pass as before) |
| Keto, Casbin | 72 and 43 of 140 runs (time budget) | 140 and 140, all pass | yes |
| Cerbos, Cerbos-tenant | 20 + 19 disagreements | 20 + 19; 280 disagreeing hits, the filter on the reference's side for all 280 | yes |
| Engine limits (ES, OS, Qdrant, Milvus, Chroma) | 140 errors | 140 errors, unchanged | yes (no change made) |
| Controls | pass | pass | |
| Leaks or altered metadata | none | none | |

The OpenFGA long-ids variant passed the same number of runs as in run 1, so the 256-character group
limit wardowl now enforces is not stricter than OpenFGA's in the generated data (the triage's check).

## What this means for the paper

- Every fix behaved as the triage predicted: the Redis and MongoDB misses are gone, the OpenFGA and
  SpiceDB batches that the services refused whole are now refused by the library before any request
  with an error that names the limit, and the Keto and Casbin runs complete.
- The Cerbos disagreement is now attributed per hit: in all 280 disagreeing hits the pushed-down
  filter agrees with the reference semantics and Cerbos's check denies, so the filter over-approximates
  the policy as written (CEL), never the reverse; every such hit fails the re-check.
- Remaining errors are store limits that fail closed, some documented and some not.
