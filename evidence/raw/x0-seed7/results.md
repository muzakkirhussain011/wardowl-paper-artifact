# wardowl: enterprise RAG acceptance run

wardowl 2.1.0 (installed from PyPI at /usr/local/lib/python3.13/dist-packages/wardowl), acceptance scripts at bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839, on ['Tesla T4', 'Tesla T4'] with 4 CPUs and 31.3 GiB; 2.8 hours.

**89 checks passed, 1 failed.**

107,540 chunks: 49,920 company documents in 20 tenants (41,600 with a canary), 20 notices carrying a prompt injection, and 57,600 FiQA passages every tenant shares. 189 people asked 1,105 questions: {'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432}.

## Failed checks

- pgvector + OpenFGA: questions: completed: TimeoutError: http://127.0.0.1:18080/healthz did not answer within 180 s

## Safety (any leak fails the run)

| Store | Questions | Hits checked | Unreadable hits | Canaries in chunks / prompts / answers | Violations | Errors |
|---|---|---|---|---|---|---|
| faiss | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| chroma | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| pgvector | 1105 | 16248 | 0 | 0 / 0 / 0 | 0 | 0 |
| pgvector + OPA | 1105 | 16248 | 0 | 0 / 0 / 0 | 0 | 0 |
| qdrant | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| elasticsearch | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| opensearch | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| weaviate | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| redis | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| lancedb | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |

## Retrieval

| Store | Strategies | Recall@5 | Recall@10 | p50 ms | p95 ms | p99 ms | Incomplete |
|---|---|---|---|---|---|---|---|
| faiss | {'prefilter': 1105} | 1.000 | 1.000 | 342.5 | 447.0 | 467.2 | 0 |
| chroma | {'prefilter': 1105} | 0.879 | 0.878 | 1434.7 | 1680.4 | 1715.9 | 0 |
| pgvector | {'prefilter': 1105} | 0.703 | 0.725 | 7.800 | 45.6 | 75.7 | 0 |
| pgvector + OPA | {'prefilter': 1105} | 0.703 | 0.725 | 8.100 | 47.9 | 79.2 | 0 |
| qdrant | {'prefilter': 1105} | 0.537 | 0.530 | 4.500 | 5.900 | 6.800 | 0 |
| elasticsearch | {'prefilter': 1105} | 0.960 | 0.961 | 8.600 | 15.7 | 22.2 | 0 |
| opensearch | {'prefilter': 1105} | 0.948 | 0.939 | 7.000 | 12.6 | 18.2 | 0 |
| weaviate | {'prefilter': 1105} | 0.891 | 0.897 | 7.400 | 24.9 | 29.9 | 0 |
| redis | {'prefilter': 1105} | 0.992 | 0.993 | 30.1 | 33.6 | 36.9 | 0 |
| lancedb | {'prefilter': 1105} | 0.850 | 0.900 | 23.8 | 30.2 | 33.2 | 0 |

## The assistant (quality: reported, not failed)

| Store | Target in top 5 | Answer accuracy | Generic: kind in top 5 | Generic: grounded | Abstained when denied | Injection retrieved / obeyed | Whole answer p50 / p95 / p99 ms |
|---|---|---|---|---|---|---|---|
| faiss | 1.000 | 0.997 | 0.875 | 0.475 | 0.704 | 97 / 97 | 1740.8 / 7277.8 / 8770.1 |
| chroma | 0.971 | 0.968 | 0.825 | 0.450 | 0.802 | 47 / 47 | 2879.3 / 4765.2 / 7564.1 |
| pgvector | 0.939 | 0.936 | 0.975 | 0.625 | 0.821 | 55 / 55 | 1353.7 / 4065.1 / 4256.8 |
| pgvector + OPA | 0.939 | 0.936 | 0.975 | 0.625 | 0.821 | 55 / 55 | 1440.8 / 4079.6 / 4680.5 |
| qdrant | 0.340 | 0.340 | 0.275 | 0.125 | 0.747 | 3 / 3 | 1333.8 / 6876.6 / 7728.5 |
| elasticsearch | 1.000 | 0.997 | 0.875 | 0.475 | 0.743 | 93 / 93 | 1496.6 / 3297.8 / 6137.1 |
| opensearch | 0.995 | 0.992 | 0.875 | 0.475 | 0.763 | 97 / 97 | 1391.1 / 3129.4 / 6199.0 |
| weaviate | 0.995 | 0.992 | 0.925 | 0.600 | 0.770 | 7 / 7 | 1590.0 / 6934.6 / 7578.2 |
| redis | 1.000 | 0.997 | 0.875 | 0.475 | 0.704 | 96 / 96 | 1455.6 / 7486.7 / 8677.2 |
| lancedb | 1.000 | 0.997 | 1.000 | 0.600 | 0.732 | 102 / 102 | 1527.9 / 8045.6 / 8596.3 |

## Loading

| Store | Rows | Load s | Index s | Server RSS GiB | Python RSS +GiB | Data GiB | Detail |
|---|---|---|---|---|---|---|---|
| faiss | 107540 | 11.1 | 0.000 | n/a | 0.490 | n/a | IndexFlatIP (exact); metadata matched in Python |
| chroma | 107540 | 193.0 | 0.000 | n/a | 0.520 | 1.020 | chromadb 1.5.9, persistent, HNSW cosine |
| pgvector | 107540 | 63.3 | 27.0 | 2.010 | 0.010 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 962 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |
| pgvector + OPA | 107540 | 63.3 | 27.0 | 2.010 | 0.010 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 962 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |
| qdrant | 107540 | 68.0 | 34.9 | 0.570 | 0.150 | 0.610 | HNSW cosine, hnsw_ef 128; keyword indexes on tenant and permissions |
| elasticsearch | 107540 | 159.7 | 2.100 | 8.750 | 0.010 | 0.870 | Elasticsearch, int8_hnsw index, 0.45 GiB; num_candidates 500 |
| opensearch | 107540 | 206.0 | 0.200 | 8.710 | -0.150 | 0.470 | OpenSearch, Lucene HNSW, 0.37 GiB; num_candidates 500 |
| weaviate | 107540 | 98.2 | 0.000 | 1.330 | -1.030 | 0.740 | HNSW cosine; Weaviate indexes while it imports |
| redis | 107540 | 40.8 | 0.000 | 0.990 | 0.010 | n/a | HNSW cosine, EF_RUNTIME 100, 1020.58M used; search-on-timeout fail |
| lancedb | 107540 | 22.9 | 62.6 | n/a | 0.370 | 0.370 | loaded with the backend's add; IVF_PQ cosine, nprobes 50, refine_factor 30 |

## Permission cache (remote authorizers)

| Store | Hits | Misses | Entries |
|---|---|---|---|
| pgvector + OPA | 7801 | 10737 | 10737 |

## Notes

- corpus: 107,540 chunks (49,920 company documents in 20 tenants, 20 injected notices, 57,600 shared FiQA passages); 189 people ask 1,105 questions ({'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432})
- readable chunks per person: min 0, median 58,641, max 59,265 of 107,540
- faiss: recall@5 1.0, recall@10 1.0; retrieval p50/p95/p99 342.5/447.0/467.2 ms; whole answer p50 1740.8 ms; answer accuracy 0.9973; strategies {'prefilter': 1105}
- chroma: recall@5 0.8786, recall@10 0.8776; retrieval p50/p95/p99 1434.7/1680.4/1715.9 ms; whole answer p50 2879.3 ms; answer accuracy 0.9681; strategies {'prefilter': 1105}
- pgvector: recall@5 0.7033, recall@10 0.7254; retrieval p50/p95/p99 7.8/45.6/75.7 ms; whole answer p50 1353.7 ms; answer accuracy 0.9362; strategies {'prefilter': 1105}
- pgvector + OPA: recall@5 0.7033, recall@10 0.7254; retrieval p50/p95/p99 8.1/47.9/79.2 ms; whole answer p50 1440.8 ms; answer accuracy 0.9362; strategies {'prefilter': 1105}
- qdrant: recall@5 0.5369, recall@10 0.5305; retrieval p50/p95/p99 4.5/5.9/6.8 ms; whole answer p50 1333.8 ms; answer accuracy 0.3404; strategies {'prefilter': 1105}
- elasticsearch: recall@5 0.9596, recall@10 0.9613; retrieval p50/p95/p99 8.6/15.7/22.2 ms; whole answer p50 1496.6 ms; answer accuracy 0.9973; strategies {'prefilter': 1105}
- opensearch: recall@5 0.9476, recall@10 0.9386; retrieval p50/p95/p99 7.0/12.6/18.2 ms; whole answer p50 1391.1 ms; answer accuracy 0.992; strategies {'prefilter': 1105}
- weaviate: recall@5 0.8911, recall@10 0.8969; retrieval p50/p95/p99 7.4/24.9/29.9 ms; whole answer p50 1590.0 ms; answer accuracy 0.992; strategies {'prefilter': 1105}
- redis: recall@5 0.9924, recall@10 0.993; retrieval p50/p95/p99 30.1/33.6/36.9 ms; whole answer p50 1455.6 ms; answer accuracy 0.9973; strategies {'prefilter': 1105}
- lancedb: recall@5 0.85, recall@10 0.9004; retrieval p50/p95/p99 23.8/30.2/33.2 ms; whole answer p50 1527.9 ms; answer accuracy 0.9973; strategies {'prefilter': 1105}
