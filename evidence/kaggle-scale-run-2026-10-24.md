# Evidence: Kaggle enterprise RAG acceptance run (wardowl 2.1.0)

Source: Kaggle notebook `muzakkirhussainsyed/notebookd8377caca8` (private), output `results.md` and
`results.json`, run on or about 2026-10-24, read on 2026-10-26. Raw outputs (`results.json`,
`answers.jsonl` 6.21 MB, per-store logs) remain in the notebook's output and should be downloaded
and archived with the paper's artifact.

## Setup

- wardowl 2.1.0 from PyPI; acceptance scripts at commit `bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839`.
- Hardware: 2 x Tesla T4, 4 CPUs, 31.3 GiB RAM; total run 2.8 hours.
- Corpus: 107,540 chunks = 49,920 company documents in 20 tenants (41,600 carrying a unique canary),
  20 notices carrying a prompt injection (one per tenant), 57,600 BEIR FiQA passages shared by every tenant.
- Embeddings: bge-base-en-v1.5 (per the scenario code); LLM: Qwen2.5-3B-Instruct answering from k=5.
- People and questions: 189 people, 1,105 questions (generic 108, targeted 376, forbidden 189, red-team 432).
- Readable chunks per person: min 0, median 58,641, max 59,265 of 107,540.
- Policy: `AllOf(TenantAuthorizer(), MetadataACLAuthorizer())`; pgvector additionally via OPA and via
  OpenFGA behind `CachingAuthorizer`.

## Outcome: 87 checks passed, 3 failed

1. pgvector: "everyone who may read something got results": 10 people failed
   (e.g. blueyonder-judy, coho-judy, contoso-judy, fabrikam-judy, northwind-eu-judy).
2. pgvector + OPA: the same 10 people.
3. pgvector + OpenFGA: did not run; OpenFGA's `/healthz` did not answer within 180 s (infrastructure).

Failures 1 and 2 mean pre-filtered pgvector search returned no hits for some highly selective users
who can read documents, while `complete` stayed True (0 incomplete reported). This is the documented
limit ("complete cannot see what an approximate index missed") observed in practice. Hypothesis to
test: pgvector's iterative scan stops at `hnsw.max_scan_tuples` (default 20,000) before finding any
permitted row for users whose readable set is small and far from the query.

## Safety (any leak fails the run)

| Store | Questions | Hits checked | Unreadable hits | Canaries chunks/prompts/answers | Violations | Errors |
|---|---|---|---|---|---|---|
| faiss | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| chroma | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| pgvector | 1105 | 16178 | 0 | 0/0/0 | 0 | 0 |
| pgvector + OPA | 1105 | 16178 | 0 | 0/0/0 | 0 | 0 |
| qdrant | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| elasticsearch | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| opensearch | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| weaviate | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| redis | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |
| lancedb | 1105 | 16360 | 0 | 0/0/0 | 0 | 0 |

Total: 11,050 retrievals, 163,236 hits checked, 0 unreadable hits, 0 canary leaks, 0 violations.

## Retrieval quality (recall against exact search over the readable set)

| Store | Strategy | Recall@5 | Recall@10 | p50 ms | p95 ms | p99 ms | Incomplete |
|---|---|---|---|---|---|---|---|
| faiss (exact) | prefilter 1105 | 1.000 | 1.000 | 345.6 | 450.4 | 464.0 | 0 |
| chroma | prefilter 1105 | 0.887 | 0.883 | 1441.6 | 1701.6 | 1739.9 | 0 |
| pgvector | prefilter 1105 | 0.691 | 0.732 | 6.5 | 46.7 | 74.5 | 0 |
| pgvector + OPA | prefilter 1105 | 0.691 | 0.732 | 7.3 | 47.1 | 75.9 | 0 |
| qdrant | prefilter 1105 | 0.564 | 0.561 | 4.3 | 5.6 | 6.5 | 0 |
| elasticsearch | prefilter 1105 | 0.948 | 0.948 | 8.1 | 14.8 | 22.1 | 0 |
| opensearch | prefilter 1105 | 0.947 | 0.938 | 6.8 | 11.9 | 17.3 | 0 |
| weaviate | prefilter 1105 | 0.888 | 0.892 | 7.1 | 23.5 | 28.4 | 0 |
| redis | prefilter 1105 | 0.985 | 0.980 | 28.3 | 31.9 | 36.1 | 0 |
| lancedb | prefilter 1105 | 0.833 | 0.860 | 22.4 | 29.3 | 31.0 | 0 |

Index settings: pgvector 0.8.7 HNSW ef_search 100, iterative scans relaxed_order; Qdrant HNSW cosine,
hnsw_ef 128, keyword payload indexes on tenant and permissions; Elasticsearch int8_hnsw,
num_candidates 500; OpenSearch Lucene HNSW, num_candidates 500; Weaviate HNSW; Redis HNSW EF_RUNTIME
100; LanceDB IVF_PQ nprobes 50 refine_factor 30; Chroma 1.5.9 HNSW; FAISS IndexFlatIP (exact).

## Assistant quality (reported, not failed)

| Store | Target in top 5 | Answer accuracy | Generic kind in top 5 | Generic grounded | Abstained when denied | Injection retrieved / obeyed |
|---|---|---|---|---|---|---|
| faiss | 1.000 | 0.997 | 0.875 | 0.475 | 0.704 | 97 / 97 |
| chroma | 0.987 | 0.984 | 0.825 | 0.450 | 0.802 | 45 / 45 |
| pgvector | 0.947 | 0.947 | 1.000 | 0.625 | 0.805 | 16 / 16 |
| qdrant | 0.399 | 0.399 | 0.600 | 0.425 | 0.704 | 14 / 14 |
| elasticsearch | 0.997 | 0.997 | 0.875 | 0.475 | 0.700 | 50 / 50 |
| opensearch | 0.995 | 0.992 | 0.875 | 0.475 | 0.759 | 96 / 96 |
| weaviate | 0.989 | 0.987 | 1.000 | 0.650 | 0.759 | 7 / 7 |
| redis | 0.995 | 0.992 | 0.875 | 0.475 | 0.704 | 51 / 51 |
| lancedb | 1.000 | 0.997 | 1.000 | 0.575 | 0.739 | 106 / 106 |

Every retrieved injected notice was obeyed by the 3B model. This is outside wardowl's threat model
(prompt injection in permitted content) but must be reported in the paper as a limitation and as
motivation for layered defences.

## Loading

| Store | Rows | Load s | Index s | Notes |
|---|---|---|---|---|
| faiss | 107540 | 11.1 | 0 | IndexFlatIP exact; metadata matched in Python |
| chroma | 107540 | 193.9 | 0 | chromadb 1.5.9, HNSW cosine |
| pgvector | 107540 | 63.1 | 26.9 | PostgreSQL 16.15, 962 MB with indexes |
| qdrant | 107540 | 67.7 | 41.2 | |
| elasticsearch | 107540 | 156.3 | 1.9 | int8_hnsw, 0.45 GiB |
| opensearch | 107540 | 198.1 | 0.2 | Lucene HNSW, 0.37 GiB |
| weaviate | 107540 | 93.3 | 0 | indexes while importing |
| redis | 107540 | 39.9 | 0 | 1023.86M used |
| lancedb | 107540 | 21.0 | 96.9 | IVF_PQ |

Permission cache (pgvector + OPA): 7,769 hits, 10,699 misses, 10,699 entries.

## What this means for the paper

1. Strong safety evidence at scale: 0 leaks over 163k checked hits, 10 configurations, with canaries
   in chunks, prompts and answers, and red-team prompts.
2. A genuine empirical finding: production vector stores' filtered ANN quality under realistic
   permission filters varies widely at their usual settings (recall@10 0.56 to 1.00), and some return
   empty results for the least-privileged users while the system cannot detect it. This motivates an
   "under-retrieval" metric and a mitigation study (e.g. exact-search fallback when fewer than k hits
   come back, store-specific parameters such as pgvector max_scan_tuples or Qdrant's filtered-search
   options).
3. Open questions to investigate before writing: the Qdrant 0.56 recall cause; the pgvector empty
   results cause; rerun OpenFGA with a longer start-up wait; repeat runs for variance.
