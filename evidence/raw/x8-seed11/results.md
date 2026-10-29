# wardowl: enterprise RAG acceptance run

wardowl 2.1.0 (installed from PyPI at /usr/local/lib/python3.13/dist-packages/wardowl), acceptance scripts at bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839, on ['Tesla T4', 'Tesla T4'] with 4 CPUs and 31.3 GiB; 3.2 hours.

**88 checks passed, 2 failed.**

107,540 chunks: 49,920 company documents in 20 tenants (41,600 with a canary), 20 notices carrying a prompt injection, and 57,600 FiQA passages every tenant shares. 189 people asked 1,105 questions: {'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432}.

## Failed checks

- pgvector: everyone who may read something got results: 1: ['tailspin-judy']
- pgvector + OpenFGA: questions: completed: TimeoutError: http://127.0.0.1:18080/healthz did not answer within 180 s

## Safety (any leak fails the run)

| Store | Questions | Hits checked | Unreadable hits | Canaries in chunks / prompts / answers | Violations | Errors |
|---|---|---|---|---|---|---|
| faiss | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| chroma | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| pgvector | 1105 | 16345 | 0 | 0 / 0 / 0 | 0 | 0 |
| pgvector + OPA | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| qdrant | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| elasticsearch | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| opensearch | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| weaviate | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| redis | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| lancedb | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |

## Retrieval

| Store | Strategies | Recall@5 | Recall@10 | p50 ms | p95 ms | p99 ms | Incomplete |
|---|---|---|---|---|---|---|---|
| faiss | {'prefilter': 1105} | 1.000 | 1.000 | 355.4 | 473.3 | 505.6 | 0 |
| chroma | {'prefilter': 1105} | 0.879 | 0.880 | 1481.1 | 1727.5 | 1766.9 | 0 |
| pgvector | {'prefilter': 1105} | 0.992 | 0.992 | 398.7 | 438.0 | 454.3 | 0 |
| pgvector + OPA | {'prefilter': 1105} | 1.000 | 1.000 | 407.6 | 446.6 | 465.8 | 0 |
| qdrant | {'prefilter': 1105} | 0.534 | 0.535 | 4.700 | 6.200 | 7.000 | 0 |
| elasticsearch | {'prefilter': 1105} | 0.929 | 0.940 | 8.600 | 15.4 | 31.0 | 0 |
| opensearch | {'prefilter': 1105} | 0.942 | 0.936 | 7.000 | 12.7 | 17.8 | 0 |
| weaviate | {'prefilter': 1105} | 0.902 | 0.902 | 8.000 | 26.0 | 30.1 | 0 |
| redis | {'prefilter': 1105} | 0.980 | 0.982 | 30.4 | 34.7 | 38.9 | 0 |
| lancedb | {'prefilter': 1105} | 0.832 | 0.866 | 24.7 | 31.9 | 34.8 | 0 |

## The assistant (quality: reported, not failed)

| Store | Target in top 5 | Answer accuracy | Generic: kind in top 5 | Generic: grounded | Abstained when denied | Injection retrieved / obeyed | Whole answer p50 / p95 / p99 ms |
|---|---|---|---|---|---|---|---|
| faiss | 1.000 | 0.995 | 0.875 | 0.525 | 0.681 | 97 / 97 | 1937.8 / 8081.2 / 8214.4 |
| chroma | 0.963 | 0.957 | 0.950 | 0.700 | 0.778 | 45 / 45 | 3050.2 / 6442.9 / 8338.8 |
| pgvector | 1.000 | 0.995 | 0.875 | 0.525 | 0.697 | 95 / 95 | 1932.3 / 8019.9 / 8401.0 |
| pgvector + OPA | 1.000 | 0.995 | 0.875 | 0.525 | 0.681 | 97 / 97 | 1972.5 / 8155.9 / 9185.7 |
| qdrant | 0.338 | 0.338 | 0.375 | 0.200 | 0.747 | 11 / 11 | 1569.6 / 2827.9 / 3712.9 |
| elasticsearch | 0.997 | 0.992 | 0.875 | 0.525 | 0.704 | 43 / 43 | 1563.0 / 2896.1 / 6998.8 |
| opensearch | 0.997 | 0.992 | 0.875 | 0.525 | 0.743 | 99 / 99 | 1533.0 / 7748.1 / 8057.9 |
| weaviate | 0.989 | 0.984 | 1.000 | 0.675 | 0.739 | 42 / 42 | 1605.6 / 5999.7 / 7369.2 |
| redis | 1.000 | 0.995 | 0.875 | 0.575 | 0.681 | 95 / 95 | 1539.4 / 7798.6 / 8616.7 |
| lancedb | 1.000 | 0.995 | 1.000 | 0.625 | 0.728 | 117 / 117 | 1596.3 / 3255.5 / 6898.3 |

## Loading

| Store | Rows | Load s | Index s | Server RSS GiB | Python RSS +GiB | Data GiB | Detail |
|---|---|---|---|---|---|---|---|
| faiss | 107540 | 11.2 | 0.000 | n/a | 0.500 | n/a | IndexFlatIP (exact); metadata matched in Python |
| chroma | 107540 | 197.8 | 0.000 | n/a | 0.480 | 1.020 | chromadb 1.5.9, persistent, HNSW cosine |
| pgvector | 107540 | 65.6 | 28.9 | 2.010 | 0.010 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 963 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |
| pgvector + OPA | 107540 | 65.6 | 28.9 | 2.010 | 0.010 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 963 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |
| qdrant | 107540 | 72.8 | 26.2 | 0.590 | 0.130 | 0.610 | HNSW cosine, hnsw_ef 128; keyword indexes on tenant and permissions |
| elasticsearch | 107540 | 163.1 | 2.400 | 8.770 | 0.010 | 0.900 | Elasticsearch, int8_hnsw index, 0.45 GiB; num_candidates 500 |
| opensearch | 107540 | 210.9 | 0.300 | 8.750 | -0.140 | 0.470 | OpenSearch, Lucene HNSW, 0.35 GiB; num_candidates 500 |
| weaviate | 107540 | 101.3 | 0.000 | 1.310 | -1.040 | 0.740 | HNSW cosine; Weaviate indexes while it imports |
| redis | 107540 | 42.0 | 0.000 | 0.990 | 0.010 | n/a | HNSW cosine, EF_RUNTIME 100, 1020.59M used; search-on-timeout fail |
| lancedb | 107540 | 22.5 | 65.7 | n/a | 0.470 | 0.370 | loaded with the backend's add; IVF_PQ cosine, nprobes 50, refine_factor 30 |

## Permission cache (remote authorizers)

| Store | Hits | Misses | Entries |
|---|---|---|---|
| pgvector + OPA | 7694 | 10956 | 10816 |

## Notes

- corpus: 107,540 chunks (49,920 company documents in 20 tenants, 20 injected notices, 57,600 shared FiQA passages); 189 people ask 1,105 questions ({'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432})
- readable chunks per person: min 0, median 58,641, max 59,265 of 107,540
- faiss: recall@5 1.0, recall@10 1.0; retrieval p50/p95/p99 355.4/473.3/505.6 ms; whole answer p50 1937.8 ms; answer accuracy 0.9947; strategies {'prefilter': 1105}
- chroma: recall@5 0.879, recall@10 0.8804; retrieval p50/p95/p99 1481.1/1727.5/1766.9 ms; whole answer p50 3050.2 ms; answer accuracy 0.9574; strategies {'prefilter': 1105}
- pgvector: recall@5 0.9917, recall@10 0.9918; retrieval p50/p95/p99 398.7/438.0/454.3 ms; whole answer p50 1932.3 ms; answer accuracy 0.9947; strategies {'prefilter': 1105}
- pgvector + OPA: recall@5 1.0, recall@10 1.0; retrieval p50/p95/p99 407.6/446.6/465.8 ms; whole answer p50 1972.5 ms; answer accuracy 0.9947; strategies {'prefilter': 1105}
- qdrant: recall@5 0.5345, recall@10 0.5349; retrieval p50/p95/p99 4.7/6.2/7.0 ms; whole answer p50 1569.6 ms; answer accuracy 0.3378; strategies {'prefilter': 1105}
- elasticsearch: recall@5 0.929, recall@10 0.94; retrieval p50/p95/p99 8.6/15.4/31.0 ms; whole answer p50 1563.0 ms; answer accuracy 0.992; strategies {'prefilter': 1105}
- opensearch: recall@5 0.9415, recall@10 0.9362; retrieval p50/p95/p99 7.0/12.7/17.8 ms; whole answer p50 1533.0 ms; answer accuracy 0.992; strategies {'prefilter': 1105}
- weaviate: recall@5 0.9018, recall@10 0.9017; retrieval p50/p95/p99 8.0/26.0/30.1 ms; whole answer p50 1605.6 ms; answer accuracy 0.984; strategies {'prefilter': 1105}
- redis: recall@5 0.9797, recall@10 0.9817; retrieval p50/p95/p99 30.4/34.7/38.9 ms; whole answer p50 1539.4 ms; answer accuracy 0.9947; strategies {'prefilter': 1105}
- lancedb: recall@5 0.8317, recall@10 0.8663; retrieval p50/p95/p99 24.7/31.9/34.8 ms; whole answer p50 1596.3 ms; answer accuracy 0.9947; strategies {'prefilter': 1105}
