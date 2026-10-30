# wardowl: enterprise RAG acceptance run

wardowl 2.1.0 (installed from PyPI at /usr/local/lib/python3.13/dist-packages/wardowl), acceptance scripts at bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839, on ['Tesla T4', 'Tesla T4'] with 4 CPUs and 31.3 GiB; 2.8 hours.

**87 checks passed, 3 failed.**

107,540 chunks: 49,920 company documents in 20 tenants (41,600 with a canary), 20 notices carrying a prompt injection, and 57,600 FiQA passages every tenant shares. 189 people asked 1,105 questions: {'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432}.

## Failed checks

- pgvector: everyone who may read something got results: 10: ['blueyonder-judy', 'coho-judy', 'contoso-judy', 'fabrikam-judy', 'northwind-eu-judy']
- pgvector + OPA: everyone who may read something got results: 10: ['blueyonder-judy', 'coho-judy', 'contoso-judy', 'fabrikam-judy', 'northwind-eu-judy']
- pgvector + OpenFGA: questions: completed: TimeoutError: http://127.0.0.1:18080/healthz did not answer within 180 s

## Safety (any leak fails the run)

| Store | Questions | Hits checked | Unreadable hits | Canaries in chunks / prompts / answers | Violations | Errors |
|---|---|---|---|---|---|---|
| faiss | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| chroma | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| pgvector | 1105 | 16178 | 0 | 0 / 0 / 0 | 0 | 0 |
| pgvector + OPA | 1105 | 16178 | 0 | 0 / 0 / 0 | 0 | 0 |
| qdrant | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| elasticsearch | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| opensearch | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| weaviate | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| redis | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| lancedb | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |

## Retrieval

| Store | Strategies | Recall@5 | Recall@10 | p50 ms | p95 ms | p99 ms | Incomplete |
|---|---|---|---|---|---|---|---|
| faiss | {'prefilter': 1105} | 1.000 | 1.000 | 345.6 | 450.4 | 464.0 | 0 |
| chroma | {'prefilter': 1105} | 0.887 | 0.883 | 1441.6 | 1701.6 | 1739.9 | 0 |
| pgvector | {'prefilter': 1105} | 0.691 | 0.732 | 6.500 | 46.7 | 74.5 | 0 |
| pgvector + OPA | {'prefilter': 1105} | 0.691 | 0.732 | 7.300 | 47.1 | 75.9 | 0 |
| qdrant | {'prefilter': 1105} | 0.564 | 0.561 | 4.300 | 5.600 | 6.500 | 0 |
| elasticsearch | {'prefilter': 1105} | 0.948 | 0.948 | 8.100 | 14.8 | 22.1 | 0 |
| opensearch | {'prefilter': 1105} | 0.947 | 0.938 | 6.800 | 11.9 | 17.3 | 0 |
| weaviate | {'prefilter': 1105} | 0.888 | 0.892 | 7.100 | 23.5 | 28.4 | 0 |
| redis | {'prefilter': 1105} | 0.985 | 0.980 | 28.3 | 31.9 | 36.1 | 0 |
| lancedb | {'prefilter': 1105} | 0.833 | 0.860 | 22.4 | 29.3 | 31.0 | 0 |

## The assistant (quality: reported, not failed)

| Store | Target in top 5 | Answer accuracy | Generic: kind in top 5 | Generic: grounded | Abstained when denied | Injection retrieved / obeyed | Whole answer p50 / p95 / p99 ms |
|---|---|---|---|---|---|---|---|
| faiss | 1.000 | 0.997 | 0.875 | 0.475 | 0.704 | 97 / 97 | 1735.9 / 7310.3 / 8852.1 |
| chroma | 0.987 | 0.984 | 0.825 | 0.450 | 0.802 | 45 / 45 | 2957.1 / 4970.0 / 7594.2 |
| pgvector | 0.947 | 0.947 | 1.000 | 0.625 | 0.805 | 16 / 16 | 1500.3 / 3454.1 / 4090.3 |
| pgvector + OPA | 0.947 | 0.947 | 1.000 | 0.625 | 0.805 | 16 / 16 | 1499.5 / 3552.7 / 4532.7 |
| qdrant | 0.399 | 0.399 | 0.600 | 0.425 | 0.704 | 14 / 14 | 1350.7 / 4067.5 / 6258.7 |
| elasticsearch | 0.997 | 0.997 | 0.875 | 0.475 | 0.700 | 50 / 50 | 1365.0 / 6911.9 / 8332.4 |
| opensearch | 0.995 | 0.992 | 0.875 | 0.475 | 0.759 | 96 / 96 | 1333.8 / 3064.8 / 6059.6 |
| weaviate | 0.989 | 0.987 | 1.000 | 0.650 | 0.759 | 7 / 7 | 1328.7 / 3367.0 / 6124.4 |
| redis | 0.995 | 0.992 | 0.875 | 0.475 | 0.704 | 51 / 51 | 1454.7 / 7505.9 / 8521.9 |
| lancedb | 1.000 | 0.997 | 1.000 | 0.575 | 0.739 | 106 / 106 | 1325.1 / 3182.5 / 3376.5 |

## Loading

| Store | Rows | Load s | Index s | Server RSS GiB | Python RSS +GiB | Data GiB | Detail |
|---|---|---|---|---|---|---|---|
| faiss | 107540 | 11.1 | 0.000 | n/a | 0.490 | n/a | IndexFlatIP (exact); metadata matched in Python |
| chroma | 107540 | 193.9 | 0.000 | n/a | 0.530 | 1.020 | chromadb 1.5.9, persistent, HNSW cosine |
| pgvector | 107540 | 63.1 | 26.9 | 2.010 | 0.010 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 962 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |
| pgvector + OPA | 107540 | 63.1 | 26.9 | 2.010 | 0.010 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 962 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |
| qdrant | 107540 | 67.7 | 41.2 | 1.310 | 0.140 | 1.100 | HNSW cosine, hnsw_ef 128; keyword indexes on tenant and permissions |
| elasticsearch | 107540 | 156.3 | 1.900 | 8.730 | 0.010 | 0.840 | Elasticsearch, int8_hnsw index, 0.45 GiB; num_candidates 500 |
| opensearch | 107540 | 198.1 | 0.200 | 8.740 | -0.150 | 0.470 | OpenSearch, Lucene HNSW, 0.37 GiB; num_candidates 500 |
| weaviate | 107540 | 93.3 | 0.000 | 1.210 | -1.150 | 0.800 | HNSW cosine; Weaviate indexes while it imports |
| redis | 107540 | 39.9 | 0.000 | 0.990 | 0.010 | n/a | HNSW cosine, EF_RUNTIME 100, 1023.86M used; search-on-timeout fail |
| lancedb | 107540 | 21.0 | 96.9 | n/a | 0.380 | 0.370 | loaded with the backend's add; IVF_PQ cosine, nprobes 50, refine_factor 30 |

## Permission cache (remote authorizers)

| Store | Hits | Misses | Entries |
|---|---|---|---|
| pgvector + OPA | 7769 | 10699 | 10699 |

## Notes

- corpus: 107,540 chunks (49,920 company documents in 20 tenants, 20 injected notices, 57,600 shared FiQA passages); 189 people ask 1,105 questions ({'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432})
- readable chunks per person: min 0, median 58,641, max 59,265 of 107,540
- faiss: recall@5 1.0, recall@10 1.0; retrieval p50/p95/p99 345.6/450.4/464.0 ms; whole answer p50 1735.9 ms; answer accuracy 0.9973; strategies {'prefilter': 1105}
- chroma: recall@5 0.8869, recall@10 0.8833; retrieval p50/p95/p99 1441.6/1701.6/1739.9 ms; whole answer p50 2957.1 ms; answer accuracy 0.984; strategies {'prefilter': 1105}
- pgvector: recall@5 0.6906, recall@10 0.7321; retrieval p50/p95/p99 6.5/46.7/74.5 ms; whole answer p50 1500.3 ms; answer accuracy 0.9468; strategies {'prefilter': 1105}
- pgvector + OPA: recall@5 0.6906, recall@10 0.7321; retrieval p50/p95/p99 7.3/47.1/75.9 ms; whole answer p50 1499.5 ms; answer accuracy 0.9468; strategies {'prefilter': 1105}
- qdrant: recall@5 0.5638, recall@10 0.5613; retrieval p50/p95/p99 4.3/5.6/6.5 ms; whole answer p50 1350.7 ms; answer accuracy 0.3989; strategies {'prefilter': 1105}
- elasticsearch: recall@5 0.9476, recall@10 0.9481; retrieval p50/p95/p99 8.1/14.8/22.1 ms; whole answer p50 1365.0 ms; answer accuracy 0.9973; strategies {'prefilter': 1105}
- opensearch: recall@5 0.9467, recall@10 0.9376; retrieval p50/p95/p99 6.8/11.9/17.3 ms; whole answer p50 1333.8 ms; answer accuracy 0.992; strategies {'prefilter': 1105}
- weaviate: recall@5 0.8884, recall@10 0.8921; retrieval p50/p95/p99 7.1/23.5/28.4 ms; whole answer p50 1328.7 ms; answer accuracy 0.9867; strategies {'prefilter': 1105}
- redis: recall@5 0.9847, recall@10 0.9803; retrieval p50/p95/p99 28.3/31.9/36.1 ms; whole answer p50 1454.7 ms; answer accuracy 0.992; strategies {'prefilter': 1105}
- lancedb: recall@5 0.8327, recall@10 0.8603; retrieval p50/p95/p99 22.4/29.3/31.0 ms; whole answer p50 1325.1 ms; answer accuracy 0.9973; strategies {'prefilter': 1105}
