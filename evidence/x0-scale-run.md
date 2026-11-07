# Evidence: X0, the Kaggle enterprise RAG acceptance run (wardowl 2.1.0, seed 7)

Raw outputs, without the embeddings: `evidence/raw/x0-seed7/` (`results.md`, `results.json`, `answers.jsonl` with the
k=5 hits and the answer per question, the model-answer cache, the kernel log `wardowl-end-to-end-scale-run-seed-7.log`
and the servers' logs), fetched with `kernels output` from kernel `wardowl-end-to-end-scale-run-seed-7`
(`kaggle/x0/`), whose run started 2026-11-07 00:39:30 UTC (`evidence/raw/KAGGLE_KERNELS.tsv`). Aggregates over X0 and
the X8 repeats: `evidence/e2e-aggregates.md`, written by `evidence/aggregate_e2e.py`.

**Two runs of X0.** X0 was first run on 2026-10-24 and run again on 2026-11-07 with the same notebook, seed (7),
acceptance scripts (`bf25bd0`), wardowl release (2.1.0 from PyPI) and session type (GPU T4 x2). This artifact holds the
second run, and every X0 number in the paper and in this file is from it. The plans written after the first run
(`plan/x8-prereg.md`, the X1 and X2 to X5 pre-registrations in the library's repository) quote the first run's
aggregates; those quotes stay as written, and the notes that judge a prediction against an X0 number say which run the
number comes from. This file was `evidence/kaggle-scale-run-2026-10-24.md`, which described the first run, until
2026-11-07.

## Setup

- wardowl 2.1.0 from PyPI; acceptance scripts at commit `bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839`.
- Hardware: 2 x Tesla T4, 4 CPUs, 31.3 GiB RAM; the harness's total 10,083 s (2.8 hours), the kernel log's last `time`
  field 10,243 s.
- Versions recorded in `results.json`: Python 3.13.15, torch 2.11.0+cu128, transformers 5.16.1, sentence-transformers
  5.7.0, psycopg 3.3.8, lancedb 0.41.0, weaviate-client 4.24.1; servers by their logs: PostgreSQL 16.15 with pgvector
  0.8.7, Qdrant 1.19.2, OpenSearch 3.9.0, Weaviate 1.39.12, Redis 8.10.3, OPA 1.21.2. Against the X8 repeats, which
  recorded psycopg 3.3.6, this is the only difference in `results.json`'s environment.
- Corpus: 107,540 chunks = 49,920 company documents in 20 tenants (41,600 carrying a unique canary),
  20 notices carrying a prompt injection (one per tenant), 57,600 BEIR FiQA passages shared by every tenant.
- Embeddings: BAAI/bge-base-en-v1.5; LLM: Qwen2.5-3B-Instruct answering from k=5.
- People and questions: 189 people, 1,105 questions (generic 108, targeted 376, forbidden 189, red-team 432). The
  question list, its order and the FAISS row are the same as in the first run (same seed).
- Readable chunks per person: min 0, median 58,641, max 59,265 of 107,540.
- Policy: `AllOf(TenantAuthorizer(), MetadataACLAuthorizer())`; pgvector additionally via OPA and via
  OpenFGA behind `CachingAuthorizer`.

## Outcome: 89 checks passed, 1 failed

1. pgvector + OpenFGA: did not run; OpenFGA's `/healthz` did not answer within 180 s. The cause is the harness:
   `openfga.log` holds `panic: configured request timeout (6s) cannot be lower than 'listObjectsDeadline' config (20s)`.
   The acceptance script sets the ListObjects deadline to 20 s and leaves OpenFGA 1.22.0's request timeout at its
   default, which OpenFGA rejects at start-up; the configuration was run with the timeout raised in X8-FGA
   (`plan/x8-prereg.md`, amendment 1; `evidence/x8-run.md`).

The check "everyone who may read something got results" passed for pgvector and pgvector + OPA: counted from
`answers.jsonl` as in `evidence/x8-run.md`, neither returned an empty answer to a person and question for which FAISS
returned hits. pgvector ran in its fast mode (median retrieval 7.8 ms, recall@10 0.725; `evidence/x8-run.md`).

## Safety (any leak fails the run)

| Store | Questions | Hits checked | Unreadable hits | Canaries chunks/prompts/answers | Violations | Errors |
|---|---|---|---|---|---|---|
| faiss | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| chroma | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| pgvector | 1105 | 16248 | 0 | 0/0/0 | 0 | 0 |
| pgvector + OPA | 1105 | 16248 | 0 | 0/0/0 | 0 | 0 |
| qdrant | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| elasticsearch | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| opensearch | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| weaviate | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| redis | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| lancedb | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |

Total: 11,050 retrievals, 163,376 hits checked, 0 unreadable hits, 0 canary leaks, 0 violations.

## Retrieval quality (recall against exact search over the readable set)

| Store | Strategy | Recall@5 | Recall@10 | p50 ms | p95 ms | p99 ms | Incomplete |
|---|---|---|---|---|---|---|---|
| faiss (exact) | prefilter 1105 | 1.000 | 1.000 | 342.5 | 447.0 | 467.2 | 0 |
| chroma | prefilter 1105 | 0.879 | 0.878 | 1434.7 | 1680.4 | 1715.9 | 0 |
| pgvector | prefilter 1105 | 0.703 | 0.725 | 7.8 | 45.6 | 75.7 | 0 |
| pgvector + OPA | prefilter 1105 | 0.703 | 0.725 | 8.1 | 47.9 | 79.2 | 0 |
| qdrant | prefilter 1105 | 0.537 | 0.530 | 4.5 | 5.9 | 6.8 | 0 |
| elasticsearch | prefilter 1105 | 0.960 | 0.961 | 8.6 | 15.7 | 22.2 | 0 |
| opensearch | prefilter 1105 | 0.948 | 0.939 | 7.0 | 12.6 | 18.2 | 0 |
| weaviate | prefilter 1105 | 0.891 | 0.897 | 7.4 | 24.9 | 29.9 | 0 |
| redis | prefilter 1105 | 0.992 | 0.993 | 30.1 | 33.6 | 36.9 | 0 |
| lancedb | prefilter 1105 | 0.850 | 0.900 | 23.8 | 30.2 | 33.2 | 0 |

Index settings: pgvector 0.8.7 HNSW ef_search 100, iterative scans relaxed_order; Qdrant HNSW cosine,
hnsw_ef 128, keyword payload indexes on tenant and permissions; Elasticsearch int8_hnsw,
num_candidates 500; OpenSearch Lucene HNSW, num_candidates 500; Weaviate HNSW; Redis HNSW EF_RUNTIME
100; LanceDB IVF_PQ nprobes 50 refine_factor 30; Chroma 1.5.9 HNSW; FAISS IndexFlatIP (exact).

pgvector's timings in the kernel log: its load started at 6,280.5 s, the questions began 91.7 s later, and the first
250 questions were retrieved in 8 s (1,105 in 35 s); pgvector + OPA, on the same table, 1,105 in 38 s.

## Assistant quality (reported, not failed)

| Store | Target in top 5 | Answer accuracy | Generic kind in top 5 | Generic grounded | Abstained when denied | Injection retrieved / obeyed |
|---|---|---|---|---|---|---|
| faiss | 1.000 | 0.997 | 0.875 | 0.475 | 0.704 | 97 / 97 |
| chroma | 0.971 | 0.968 | 0.825 | 0.450 | 0.802 | 47 / 47 |
| pgvector | 0.939 | 0.936 | 0.975 | 0.625 | 0.821 | 55 / 55 |
| pgvector + OPA | 0.939 | 0.936 | 0.975 | 0.625 | 0.821 | 55 / 55 |
| qdrant | 0.340 | 0.340 | 0.275 | 0.125 | 0.747 | 3 / 3 |
| elasticsearch | 1.000 | 0.997 | 0.875 | 0.475 | 0.743 | 93 / 93 |
| opensearch | 0.995 | 0.992 | 0.875 | 0.475 | 0.763 | 97 / 97 |
| weaviate | 0.995 | 0.992 | 0.925 | 0.600 | 0.770 | 7 / 7 |
| redis | 1.000 | 0.997 | 0.875 | 0.475 | 0.704 | 96 / 96 |
| lancedb | 1.000 | 0.997 | 1.000 | 0.600 | 0.732 | 102 / 102 |

Every retrieved injected notice was obeyed by the 3B model: 652 of 652. This is outside wardowl's threat model
(prompt injection in permitted content) and is reported as a limitation.

## Loading

| Store | Rows | Load s | Index s | Notes |
|---|---|---|---|---|
| faiss | 107540 | 11.1 | 0 | IndexFlatIP exact; metadata matched in Python |
| chroma | 107540 | 193.0 | 0 | chromadb 1.5.9, HNSW cosine |
| pgvector | 107540 | 63.3 | 27.0 | PostgreSQL 16.15, 962 MB with indexes |
| qdrant | 107540 | 68.0 | 34.9 | |
| elasticsearch | 107540 | 159.7 | 2.1 | int8_hnsw, 0.45 GiB |
| opensearch | 107540 | 206.0 | 0.2 | Lucene HNSW, 0.37 GiB |
| weaviate | 107540 | 98.2 | 0 | indexes while importing |
| redis | 107540 | 40.8 | 0 | 1020.58M used |
| lancedb | 107540 | 22.9 | 62.6 | IVF_PQ |

Permission cache (pgvector + OPA): 7,801 hits, 10,737 misses, 10,737 entries.
