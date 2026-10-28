# Evidence: conformance campaign, GitHub Actions run 1

Source: repository `muzakkirhussain011/wardowl`, workflow `paper-conformance`
(`.github/workflows/paper-conformance.yml`), run #1, id 40313285885
(https://github.com/muzakkirhussain011/wardowl/actions/runs/40313285885), triggered by a push of
commit `5d0f414a346511ad48a6c1c8b411259e6d908b84` to branch `paper/conformance-campaign`
(head commit message "paper-conformance: also run on a push to its branch"). Read on
2026-10-28 from the run page, the job summaries rendered on it (the merged summary of the
`summary` job and the six per-job summaries), the run's annotations, the public jobs API
listing, and the `campaign (engines)` job log. Artifacts were not downloaded.

## Setup

The campaign runs wardowl's conformance kit (`benchmarks/paper/conformance_campaign.py`, see
`benchmarks/paper/CONFORMANCE.md`) against real backends and authorization engines, wardowl
2.1.0 at commit 5d0f414, Python 3.12.15, as a six-way job matrix (sql-and-kv, search-engines,
vector-dbs, embedded, engines, cloud) plus a `summary` job that merges the results. Each store
target gets seeds 0-19 and nine data variants (default, large-corpus, deep-filters, wide-or,
long-strings, huge-strings, unicode-case, numeric-strings, odd-fields), 10 corpora per seed
for the default variant and 3 for the others, large corpora up to 150 documents; each engine
target gets seeds 0-19 and seven variants (default, unicode-case, numeric-strings,
many-groups, many-hits, long-ids, scalar-fields) in consistency mode. A run is one (seed,
variant) and takes its worst subject's outcome. Outcomes: pass (the kit found nothing),
conformance-violation (the kit's first disagreement with the reference), refused-ValueError
(wardowl refused the data or a filter), error (anything else). Controls: the in-memory store
(`memory`, the reference semantics) and the in-process `metadata-acl` engine.

## Status

Run status: **Success**, total duration 2h 55m 37s, 7 artifacts. Every job completed with
conclusion `success` (from the jobs API):

| Job | Conclusion | Started (UTC) | Completed (UTC) | Targets, runs (from its summary) |
|---|---|---|---|---|
| campaign (sql-and-kv) | success | 2026-10-26 11:12:13 | 11:57:55 | 3 targets, 540 runs |
| campaign (search-engines) | success | 11:12:13 | 12:21:56 | 3 targets, 540 runs |
| campaign (vector-dbs) | success | 11:12:18 | 12:55:41 | 4 targets, 720 runs |
| campaign (embedded) | success | 11:12:13 | 11:15:46 | 4 targets, 720 runs |
| campaign (engines) | success | 11:12:13 | 14:07:34 | 14 targets, 1795 runs |
| campaign (cloud) | success | 11:12:13 | 11:12:30 | 1 target, 0 runs (Pinecone skipped) |
| summary | success | 14:07:36 | 14:07:47 | 29 targets, 4315 runs (merged) |

The engines job's step "Run the campaign, one process per target" took 2h 54m 1s; Keto and
Casbin stopped on the time budget (below). Annotations: 30 warnings and 7 notices (the notices
are GitHub's ubuntu-latest migration message on each job).

Artifacts (name, size, digest): conformance-cloud 1.67 KB
`sha256:d3c732445e1b40708430c4cd221aca5dbf49dd2aaba0da33bd4b71e0228f68d8`;
conformance-embedded 11.8 KB `sha256:7b069528de60385f56049f2786a1de3f2f8c664f1112667ecd3fedc5354f1f62`;
conformance-engines 138 KB `sha256:5ca9ab17bfacbc3ca62ab4be3e88f998c681e480e40d35543e5e44a85a58406a`;
conformance-search-engines 35 KB `sha256:270c7220579a7f81b73d00ec147ab982d25a7ffefed29e8f9701e72051248c7d`;
conformance-sql-and-kv 37.1 KB `sha256:c37f9893b388b1347be1cf67bad5cb3830b2af02672371cdaa0d10b841765998`;
conformance-summary 142 KB `sha256:e0237635e2631e7b63adf5649b53b88d29d494b4b44e4212373876187d312304`;
conformance-vector-dbs 43.5 KB `sha256:a78e66d497db6823420c20bfca671a11f073bc721e6a38e36c552ff2a6b2907c`.

## Merged summary (summary job, copied)

Controls: memory 180 of 180 runs pass; metadata-acl 140 of 140 runs pass.

Violations, as the summary groups them:

- Wrong answers (leaks, filter and check disagreeing, altered metadata):
  - cerbos: filter-check-disagree in 20 runs (variants scalar-fields; seeds 0-19)
  - cerbos-tenant: filter-check-disagree in 19 runs (variants scalar-fields; seeds 0-10, 12-19)
- Others:
  - redis: after-set-metadata:missed in 10 runs (variants long-strings, huge-strings; seeds 0, 2, 9, 13, 15, 17-19)
  - redis: missed in 16 runs (variants long-strings, huge-strings; seeds 0-1, 3-5, 7-8, 10-14, 19)
  - mongodb: after-set-metadata:missed in 9 runs (variants long-strings, huge-strings; seeds 0, 2, 9, 13, 15, 17-19)
  - mongodb: missed in 10 runs (variants huge-strings; seeds 1, 3-5, 8, 10-14)

No leak is reported for any target.

### Per-target counts

Runs count one (seed, variant) each; sound-only retries of short exact answers are not counted.
Version strings shortened where the page itself truncates them.

| Target | Family | Version | Status | Seeds | Runs | Pass | Violations | Refused | Errors |
|---|---|---|---|---|---|---|---|---|---|
| memory | store | (in process) | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| pgvector | store | pgvector/pgvector:pg17; pgvector 0.8.7, PostgreSQL 17.11 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| redis | store | redis:8.10.2-alpine | complete | 20 | 180 | 154 | 26 | 0 | 0 |
| cassandra | store | cassandra:5.0.9 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| elasticsearch | store | elasticsearch 9.5.5 (Lucene 10.5.1) | complete | 20 | 180 | 160 | 0 | 0 | 20 |
| opensearch | store | opensearch 3.9.0 (Lucene 10.5.1) | complete | 20 | 180 | 160 | 0 | 0 | 20 |
| vespa | store | vespaengine/vespa:8.763.13 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| qdrant | store | qdrant/qdrant:v1.19.2 | complete | 20 | 180 | 160 | 0 | 0 | 20 |
| milvus | store | milvusdb/milvus:v3.0.2 | complete | 20 | 180 | 140 | 0 | 0 | 40 |
| weaviate | store | weaviate 1.39.12 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| mongodb | store | mongodb-atlas-local 8.0.30 | complete | 20 | 180 | 161 | 19 | 0 | 0 |
| chroma | store | chromadb 1.5.9 | complete | 20 | 180 | 140 | 0 | 0 | 40 |
| lancedb | store | lancedb 0.40.0, pyarrow 26.0.0 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| faiss | store | faiss-cpu 1.15.1, numpy 2.5.4 | complete | 20 | 180 | 180 | 0 | 0 | 0 |
| pinecone | store | httpx 0.28.1 | skipped: the PINECONE_API_KEY secret is not set | 0 | 0 | 0 | 0 | 0 | 0 |
| metadata-acl | engine | (in process) | complete | 20 | 140 | 140 | 0 | 0 | 0 |
| opa | engine | OPA 1.21.2 | complete | 20 | 140 | 140 | 0 | 0 | 0 |
| opa-tenant | engine | OPA 1.21.2 | complete | 20 | 140 | 140 | 0 | 0 | 0 |
| openfga | engine | openfga/openfga:v1.22.0 | complete | 20 | 140 | 21 | 0 | 0 | 119 |
| openfga-tenant | engine | openfga/openfga:v1.22.0 | complete | 20 | 140 | 21 | 0 | 0 | 119 |
| spicedb | engine | authzed/spicedb:v1.56.2 | complete | 20 | 140 | 16 | 0 | 0 | 124 |
| spicedb-tenant | engine | authzed/spicedb:v1.56.2 | complete | 20 | 140 | 23 | 0 | 0 | 117 |
| cerbos | engine | ghcr.io/cerbos/cerbos:0.56.0 | complete | 20 | 140 | 120 | 20 | 0 | 0 |
| cerbos-tenant | engine | ghcr.io/cerbos/cerbos:0.56.0 | complete | 20 | 140 | 121 | 19 | 0 | 0 |
| keto | engine | oryd/keto:v26.2.0 | time budget: 68 of 140 runs not started | 11 | 72 | 72 | 0 | 0 | 0 |
| cedar | engine | cedarpy 4.12.2 | complete | 20 | 140 | 140 | 0 | 0 | 0 |
| cedar-tenant | engine | cedarpy 4.12.2 | complete | 20 | 140 | 140 | 0 | 0 | 0 |
| casbin | engine | casbin 1.43.0 | time budget: 97 of 140 runs not started | 7 | 43 | 43 | 0 | 0 | 0 |
| casbin-tenant | engine | casbin 1.43.0 | complete | 20 | 140 | 140 | 0 | 0 | 0 |

Totals summed by hand from this table (not printed by the page): 4,315 runs = 3,612 pass +
84 violations + 0 refused + 619 errors. Stores: 2,520 runs, 2,335 pass, 45 violations, 140
errors. Engines: 1,795 runs, 1,277 pass, 39 violations, 479 errors.

Image digests and exact reported versions for every container target are printed in the
summary (for example pgvector `sha256:151aa1c2...`, reported "PostgreSQL 17.11 (Debian
17.11-1.pgdg12+2)") and are kept in the `conformance-summary` artifact.

### Per-variant breakdown where anything failed

Variants not listed passed 20 of 20 seeds (Keto and Casbin: every started run passed).

| Target | Variant | Mode | Pass/Seeds | Violations | Errors | Notes |
|---|---|---|---|---|---|---|
| redis | long-strings | exact | 10/20 | 10 (missed 6, after-set-metadata:missed 4) | 0 | sound-retry 10/10 pass |
| redis | huge-strings | exact | 4/20 | 16 (missed 10, after-set-metadata:missed 6) | 0 | sound-retry 16/16 pass |
| mongodb | long-strings | exact | 17/20 | 3 (after-set-metadata:missed 3) | 0 | sound-retry 3/3 pass |
| mongodb | huge-strings | exact | 4/20 | 16 (missed 10, after-set-metadata:missed 6) | 0 | sound-retry 16/16 pass |
| elasticsearch | huge-strings | exact | 0/20 | 0 | 20 (RuntimeError 16, BadRequestError 4) | |
| opensearch | huge-strings | exact | 0/20 | 0 | 20 (RuntimeError 20) | |
| qdrant | odd-fields | exact | 0/20 | 0 | 20 (UnexpectedResponse 20) | filters refused per variant: 440, 197, 340, 59, 122, 133, 111, 125, 47 |
| milvus | long-strings | exact | 0/20 | 0 | 20 (MilvusException 20) | |
| milvus | huge-strings | exact | 0/20 | 0 | 20 (MilvusException 20) | |
| chroma | wide-or | exact | 0/20 | 0 | 20 (InternalError 20) | |
| chroma | odd-fields | exact | 0/20 | 0 | 20 (InvalidArgumentError 20) | |
| cerbos | scalar-fields | consistency | 0/20 | 20 (filter-check-disagree) | 0 | subjects passing 33/160 |
| cerbos-tenant | scalar-fields | consistency | 1/20 | 19 (filter-check-disagree) | 0 | subjects passing 119/160 |
| openfga | all 7 variants | consistency | 21/140 | 0 | 119 (AuthorizationError) | per variant pass 2, 4, 3, 0, 8, 0, 4; subjects passing 198/240, 129/160, 125/160, 0/60, 68/80, 48/160, 134/160 |
| openfga-tenant | all 7 variants | consistency | 21/140 | 0 | 119 (AuthorizationError) | same per-variant figures as openfga |
| spicedb | all 7 variants | consistency | 16/140 | 0 | 124 (AuthorizationError) | per variant pass 1, 0, 0, 5, 5, 3, 2; subjects passing 165/240, 41/160, 52/160, 35/60, 56/80, 122/160, 118/160 |
| spicedb-tenant | all 7 variants | consistency | 23/140 | 0 | 117 (AuthorizationError) | per variant pass 1, 0, 0, 5, 5, 10, 2; subjects passing 165/240, 84/160, 93/160, 35/60, 56/80, 143/160, 118/160 |

(Variant order for engines: default, unicode-case, numeric-strings, many-groups, many-hits,
long-ids, scalar-fields.) Qdrant reports "filters refused" counts for every variant even where
all runs passed; the other targets report 0.

## Concrete violations and their reproducers (as printed)

### Cerbos: filter_for and check disagree on scalar ACL fields

Policy `examples/cerbos/policies/document.yaml` (cerbos) and
`acceptance/policies/cerbos/document.yaml` (cerbos-tenant), Cerbos 0.56.0. The kit prints
only the first 600 characters of each finding, so the metadata of the disagreeing hit is
visible in one case only (seed 2). Examples from the engines job log:

- seed 0, example 0: subject carol, groups ['1', 'Eng', 'hr']; filter
  `{"or": [{"in": {"field": "allowed_users", "values": ["carol"]}}, {"in": {"field": "allowed_groups", "values": ["*"]}}, {"in": {"field": "allowed_groups", "values": ["1", "Eng", "hr"]}}]}`;
  hits `['doc-024']`; the hit's metadata is not visible in the page.
- seed 2, example 0: subject zoë, groups ['legal']; filter on allowed_users ["zoë"],
  allowed_groups ["*"], allowed_groups ["legal"]; hits `['doc-000']`, and
  `doc-000: {"allowed_groups": 1, "allowed_users": "zoë", "doc_id": "doc-000"}`, a scalar
  (not a list) in both ACL fields.
- seed 4: subject zoë, groups ['1']; hits `['doc-004', 'doc-021']`. Seed 6: subject Bob, groups
  ['Eng']; hits `['doc-018', 'doc-023']`.

Which side (the pushed-down filter or Cerbos's check) gives the reference answer is not stated
in the visible text; the kit reports only that they gave different answers for some hits.

Reproducers:

    python benchmarks/paper/conformance_campaign.py run --targets cerbos --seed-list 0 --variants scalar-fields --examples 10 --stress-examples 3 --large-documents 150
    python benchmarks/paper/conformance_campaign.py run --targets cerbos-tenant --seed-list 0 --variants scalar-fields --examples 10 --stress-examples 3 --large-documents 150

### Redis and MongoDB: matching documents missed with long and huge string values

Exact-mode search with a filter (and after `set_metadata`) missed documents that match the
filter when values are long or huge strings; every such run passed its sound-only retry, so
these are completeness failures (under-retrieval), not leaks. Examples from the annotations:

- redis long-strings seed 0, example 2: "missed documents that match: ['doc-002']", filter an
  `and` over `allowed_groups` in ["b", a long "é..." string].
- redis long-strings seed 1, example 2: `retrieve with strategy='prefilter'` "returned 0 of the
  2 readable documents asked for" (subject id a long run of "u").
- redis huge-strings seed 0, example 1 (after set_metadata): missed `['doc-000']`.
- mongodb huge-strings seed 1, example 0: missed `['doc-000']`, filter
  `{"or": [{"in": {"field": "team", "values": ["b", "xxx..."]}} ...`.
- mongodb huge-strings seed 11, example 0: missed `['doc-009']`, filter with `allowed_groups`
  in [] or `team` in [1000, 1001, ...].

Reproducers (first run of each kind):

    python benchmarks/paper/conformance_campaign.py run --targets redis --seed-list 0 --variants long-strings --examples 10 --stress-examples 3 --large-documents 150
    python benchmarks/paper/conformance_campaign.py run --targets redis --seed-list 9 --variants long-strings --examples 10 --stress-examples 3 --large-documents 150
    python benchmarks/paper/conformance_campaign.py run --targets redis --seed-list 0 --variants huge-strings --examples 10 --stress-examples 3 --large-documents 150
    python benchmarks/paper/conformance_campaign.py run --targets redis --seed-list 1 --variants huge-strings --examples 10 --stress-examples 3 --large-documents 150
    python benchmarks/paper/conformance_campaign.py run --targets mongodb --seed-list 13 --variants long-strings --examples 10 --stress-examples 3 --large-documents 150
    python benchmarks/paper/conformance_campaign.py run --targets mongodb --seed-list 0 --variants huge-strings --examples 10 --stress-examples 3 --large-documents 150
    python benchmarks/paper/conformance_campaign.py run --targets mongodb --seed-list 1 --variants huge-strings --examples 10 --stress-examples 3 --large-documents 150

### Errors (not violations), first of each kind as printed

- elasticsearch huge-strings seed 0: RuntimeError, bulk request failed for 'doc-000':
  `document_parsing_exception`, failed to parse field [wardowl_terms] of type [keyword]. Seed 2:
  BadRequestError(400, 'x_content_parse_exception', '[1:498] [bool] failed to parse field [should]').
- opensearch huge-strings seed 0: RuntimeError, `illegal_argument_exception`, "Document contains
  at least one immense term in field="wardowl_terms" (whose UTF8 encoding is longer than the
  max length 32766)".
- qdrant odd-fields seed 0: UnexpectedResponse, 400 (Bad Request).
- milvus long-strings seed 0: MilvusException code 1100, array field "wardowl_terms" element
  length 8199 exceeds max length 1024. huge-strings seed 0: JSON field (metadata) length 72841
  exceeds max length 65536.
- chroma wide-or seed 0: InternalError, "Expression tree is too large (maximum depth 1000)".
  odd-fields seed 0: InvalidArgumentError, "Invalid metadata at index 3".
- openfga and openfga-tenant, every variant: AuthorizationError, "OpenFGA batch-check returned
  HTTP 400".
- spicedb and spicedb-tenant, every variant: AuthorizationError, "SpiceDB CheckBulkPermissions
  returned HTTP 400".

Each has a printed replay command of the same form, e.g.
`python benchmarks/paper/conformance_campaign.py run --targets openfga --seed-list 0 --variants default --examples 10 --stress-examples 3 --large-documents 150`.

## What this means for the paper

- No target leaked: across 29 targets and 4,315 runs the kit reports no leak and no altered
  metadata, and both controls pass every run (memory 180/180, metadata-acl 140/140).
- The kit found one class of wrong answer: Cerbos's filter and check disagree when ACL fields
  hold scalars instead of lists (39 of 40 scalar-fields runs across the two Cerbos policies).
  This is the paper's concrete example of the enforcement layer catching a filter/check
  mismatch; before writing it up, establish which side is wrong and whether wardowl's adapter
  or the example policy causes it.
- Redis and MongoDB under-retrieve with long and huge string values (45 runs), always passing
  the sound-only retry: a second, independent example that a correct filter can still return
  fewer permitted documents than exist, which ties the conformance results to X1's
  under-retrieval theme.
- Engine size limits (Elasticsearch/OpenSearch 32,766-byte terms, Milvus 1,024 array element
  and 65,536 JSON limits, Chroma expression depth 1,000) surface as errors rather than as wrong
  answers; the paper can report them as limits that fail loudly, after checking that no partial
  result is returned in those cases.
- OpenFGA and SpiceDB results are not usable yet (84% to 89% of runs errored with HTTP 400 on
  batch checks), Keto and Casbin ran only 72 and 43 of 140 runs, and Pinecone did not run, so
  conformance claims for those five targets must wait for a rerun.

## Follow-ups

- Reproduce the Cerbos scalar-fields disagreement locally in CI with the printed replay
  command, print the full finding (the 600-character limit hides the hit's metadata) and decide
  whether wardowl, the example policy or Cerbos is at fault.
- Investigate the OpenFGA batch-check and SpiceDB CheckBulkPermissions HTTP 400s (the server
  logs are in the conformance-engines artifact); a request-size or batch-limit cause is a
  hypothesis only.
- Rerun Keto and Casbin with a larger time budget, and Pinecone once the PINECONE_API_KEY
  secret is set.
- Decide whether wardowl should refuse (ValueError) values that exceed known engine limits
  instead of surfacing engine errors, and document the limits.
- Investigate the Redis and MongoDB exact-mode misses with long strings (index tokenization or
  field length limits are candidates) and document whether exact mode should be claimed for
  them with such values.
- Download and archive the `conformance-summary` artifact (142 KB) with the paper artifact;
  not done here (read-only, no downloads).
