# wardowl: enterprise RAG acceptance run

wardowl 2.1.0 (installed from PyPI at /usr/local/lib/python3.13/dist-packages/wardowl), acceptance scripts at bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839, on ['Tesla T4', 'Tesla T4'] with 4 CPUs and 31.3 GiB; 3.1 hours.

**89 checks passed, 1 failed.**

107,540 chunks: 49,920 company documents in 20 tenants (41,600 with a canary), 20 notices carrying a prompt injection, and 57,600 FiQA passages every tenant shares. 189 people asked 1,105 questions: {'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432}.

## Failed checks

- pgvector + OpenFGA: questions: completed: TimeoutError: http://127.0.0.1:18080/healthz did not answer within 180 s

## Safety (any leak fails the run)

| Store | Questions | Hits checked | Unreadable hits | Canaries in chunks / prompts / answers | Violations | Errors |
|---|---|---|---|---|---|---|
| faiss | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| chroma | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| pgvector | 1105 | 16351 | 0 | 0 / 0 / 0 | 0 | 0 |
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
| faiss | {'prefilter': 1105} | 1.000 | 1.000 | 367.5 | 488.2 | 518.1 | 0 |
| chroma | {'prefilter': 1105} | 0.864 | 0.873 | 1444.4 | 1681.8 | 1715.5 | 0 |
| pgvector | {'prefilter': 1105} | 0.994 | 0.994 | 386.0 | 421.4 | 436.8 | 0 |
| pgvector + OPA | {'prefilter': 1105} | 1.000 | 1.000 | 389.5 | 423.5 | 436.3 | 0 |
| qdrant | {'prefilter': 1105} | 0.569 | 0.561 | 4.700 | 5.900 | 6.700 | 0 |
| elasticsearch | {'prefilter': 1105} | 0.952 | 0.959 | 8.800 | 15.1 | 29.1 | 0 |
| opensearch | {'prefilter': 1105} | 0.942 | 0.933 | 7.100 | 12.5 | 20.5 | 0 |
| weaviate | {'prefilter': 1105} | 0.908 | 0.913 | 8.000 | 25.2 | 31.1 | 0 |
| redis | {'prefilter': 1105} | 0.995 | 0.988 | 30.4 | 34.3 | 37.4 | 0 |
| lancedb | {'prefilter': 1105} | 0.861 | 0.899 | 24.8 | 31.7 | 33.4 | 0 |

## The assistant (quality: reported, not failed)

| Store | Target in top 5 | Answer accuracy | Generic: kind in top 5 | Generic: grounded | Abstained when denied | Injection retrieved / obeyed | Whole answer p50 / p95 / p99 ms |
|---|---|---|---|---|---|---|---|
| faiss | 1.000 | 0.992 | 0.950 | 0.500 | 0.704 | 101 / 101 | 2010.5 / 3974.0 / 4527.2 |
| chroma | 0.992 | 0.984 | 1.000 | 0.675 | 0.763 | 43 / 43 | 3197.1 / 5295.8 / 5701.5 |
| pgvector | 1.000 | 0.992 | 0.950 | 0.500 | 0.712 | 98 / 98 | 1994.7 / 4073.0 / 4620.7 |
| pgvector + OPA | 1.000 | 0.992 | 0.950 | 0.500 | 0.704 | 101 / 101 | 1968.2 / 4122.6 / 4644.0 |
| qdrant | 0.396 | 0.388 | 0.375 | 0.200 | 0.712 | 3 / 3 | 1486.0 / 2536.1 / 3531.6 |
| elasticsearch | 0.995 | 0.989 | 0.950 | 0.525 | 0.700 | 94 / 94 | 1772.7 / 3769.5 / 4334.7 |
| opensearch | 0.987 | 0.979 | 0.950 | 0.500 | 0.728 | 102 / 102 | 1760.1 / 3904.1 / 4410.8 |
| weaviate | 0.987 | 0.979 | 1.000 | 0.550 | 0.766 | 13 / 13 | 1805.2 / 3897.1 / 4439.4 |
| redis | 0.989 | 0.984 | 0.950 | 0.500 | 0.704 | 101 / 101 | 1789.3 / 3865.3 / 4442.7 |
| lancedb | 1.000 | 0.992 | 0.975 | 0.650 | 0.720 | 112 / 112 | 1768.2 / 4284.3 / 6805.7 |

## Loading

| Store | Rows | Load s | Index s | Server RSS GiB | Python RSS +GiB | Data GiB | Detail |
|---|---|---|---|---|---|---|---|
| faiss | 107540 | 11.2 | 0.000 | n/a | 0.500 | n/a | IndexFlatIP (exact); metadata matched in Python |
| chroma | 107540 | 193.2 | 0.000 | n/a | 0.520 | 1.020 | chromadb 1.5.9, persistent, HNSW cosine |
| pgvector | 107540 | 64.5 | 28.3 | 2.020 | 0.010 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 963 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |
| pgvector + OPA | 107540 | 64.5 | 28.3 | 2.020 | 0.010 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 963 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |
| qdrant | 107540 | 71.0 | 39.1 | 1.280 | 0.100 | 1.160 | HNSW cosine, hnsw_ef 128; keyword indexes on tenant and permissions |
| elasticsearch | 107540 | 166.5 | 2.600 | 8.760 | 0.010 | 0.920 | Elasticsearch, int8_hnsw index, 0.45 GiB; num_candidates 500 |
| opensearch | 107540 | 211.0 | 0.300 | 8.730 | -0.160 | 0.470 | OpenSearch, Lucene HNSW, 0.35 GiB; num_candidates 500 |
| weaviate | 107540 | 101.1 | 0.000 | 1.170 | -1.070 | 0.750 | HNSW cosine; Weaviate indexes while it imports |
| redis | 107540 | 42.5 | 0.000 | 0.980 | 0.010 | n/a | HNSW cosine, EF_RUNTIME 100, 1020.59M used; search-on-timeout fail |
| lancedb | 107540 | 22.7 | 67.8 | n/a | 0.330 | 0.370 | loaded with the backend's add; IVF_PQ cosine, nprobes 50, refine_factor 30 |

## Permission cache (remote authorizers)

| Store | Hits | Misses | Entries |
|---|---|---|---|
| pgvector + OPA | 7703 | 10947 | 10850 |

## Notes

- corpus: 107,540 chunks (49,920 company documents in 20 tenants, 20 injected notices, 57,600 shared FiQA passages); 189 people ask 1,105 questions ({'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432})
- readable chunks per person: min 0, median 58,641, max 59,265 of 107,540
- faiss: recall@5 1.0, recall@10 1.0; retrieval p50/p95/p99 367.5/488.2/518.1 ms; whole answer p50 2010.5 ms; answer accuracy 0.992; strategies {'prefilter': 1105}
- chroma: recall@5 0.8635, recall@10 0.873; retrieval p50/p95/p99 1444.4/1681.8/1715.5 ms; whole answer p50 3197.1 ms; answer accuracy 0.984; strategies {'prefilter': 1105}
- pgvector: recall@5 0.9935, recall@10 0.9935; retrieval p50/p95/p99 386.0/421.4/436.8 ms; whole answer p50 1994.7 ms; answer accuracy 0.992; strategies {'prefilter': 1105}
- pgvector + OPA: recall@5 1.0, recall@10 1.0; retrieval p50/p95/p99 389.5/423.5/436.3 ms; whole answer p50 1968.2 ms; answer accuracy 0.992; strategies {'prefilter': 1105}
- qdrant: recall@5 0.5694, recall@10 0.5607; retrieval p50/p95/p99 4.7/5.9/6.7 ms; whole answer p50 1486.0 ms; answer accuracy 0.3883; strategies {'prefilter': 1105}
- elasticsearch: recall@5 0.9524, recall@10 0.9585; retrieval p50/p95/p99 8.8/15.1/29.1 ms; whole answer p50 1772.7 ms; answer accuracy 0.9894; strategies {'prefilter': 1105}
- opensearch: recall@5 0.9417, recall@10 0.9333; retrieval p50/p95/p99 7.1/12.5/20.5 ms; whole answer p50 1760.1 ms; answer accuracy 0.9787; strategies {'prefilter': 1105}
- weaviate: recall@5 0.9085, recall@10 0.913; retrieval p50/p95/p99 8.0/25.2/31.1 ms; whole answer p50 1805.2 ms; answer accuracy 0.9787; strategies {'prefilter': 1105}
- redis: recall@5 0.9946, recall@10 0.9878; retrieval p50/p95/p99 30.4/34.3/37.4 ms; whole answer p50 1789.3 ms; answer accuracy 0.984; strategies {'prefilter': 1105}
- lancedb: recall@5 0.8611, recall@10 0.8993; retrieval p50/p95/p99 24.8/31.7/33.4 ms; whole answer p50 1768.2 ms; answer accuracy 0.992; strategies {'prefilter': 1105}
