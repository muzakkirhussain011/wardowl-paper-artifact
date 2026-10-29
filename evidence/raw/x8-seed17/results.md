# wardowl: enterprise RAG acceptance run

wardowl 2.1.0 (installed from PyPI at /usr/local/lib/python3.13/dist-packages/wardowl), acceptance scripts at bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839, on ['Tesla T4', 'Tesla T4'] with 4 CPUs and 31.3 GiB; 2.8 hours.

**87 checks passed, 3 failed.**

107,540 chunks: 49,920 company documents in 20 tenants (41,600 with a canary), 20 notices carrying a prompt injection, and 57,600 FiQA passages every tenant shares. 189 people asked 1,105 questions: {'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432}.

## Failed checks

- pgvector: everyone who may read something got results: 7: ['adatum-judy', 'blueyonder-judy', 'coho-judy', 'contoso-judy', 'proseware-judy']
- pgvector + OPA: everyone who may read something got results: 7: ['adatum-judy', 'blueyonder-judy', 'coho-judy', 'contoso-judy', 'proseware-judy']
- pgvector + OpenFGA: questions: completed: TimeoutError: http://127.0.0.1:18080/healthz did not answer within 180 s

## Safety (any leak fails the run)

| Store | Questions | Hits checked | Unreadable hits | Canaries in chunks / prompts / answers | Violations | Errors |
|---|---|---|---|---|---|---|
| faiss | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| chroma | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| pgvector | 1105 | 16173 | 0 | 0 / 0 / 0 | 0 | 0 |
| pgvector + OPA | 1105 | 16173 | 0 | 0 / 0 / 0 | 0 | 0 |
| qdrant | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| elasticsearch | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| opensearch | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| weaviate | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| redis | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| lancedb | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |

## Retrieval

| Store | Strategies | Recall@5 | Recall@10 | p50 ms | p95 ms | p99 ms | Incomplete |
|---|---|---|---|---|---|---|---|
| faiss | {'prefilter': 1105} | 1.000 | 1.000 | 356.3 | 458.6 | 470.7 | 0 |
| chroma | {'prefilter': 1105} | 0.879 | 0.880 | 1432.0 | 1696.6 | 1732.6 | 0 |
| pgvector | {'prefilter': 1105} | 0.700 | 0.732 | 8.100 | 47.2 | 77.3 | 0 |
| pgvector + OPA | {'prefilter': 1105} | 0.700 | 0.732 | 8.500 | 48.4 | 78.8 | 0 |
| qdrant | {'prefilter': 1105} | 0.560 | 0.549 | 4.600 | 6.000 | 6.600 | 0 |
| elasticsearch | {'prefilter': 1105} | 0.938 | 0.948 | 8.400 | 15.2 | 27.7 | 0 |
| opensearch | {'prefilter': 1105} | 0.939 | 0.934 | 6.900 | 11.9 | 17.9 | 0 |
| weaviate | {'prefilter': 1105} | 0.899 | 0.902 | 7.800 | 25.7 | 31.9 | 0 |
| redis | {'prefilter': 1105} | 0.971 | 0.976 | 29.6 | 33.6 | 36.3 | 0 |
| lancedb | {'prefilter': 1105} | 0.835 | 0.871 | 24.9 | 32.2 | 33.8 | 0 |

## The assistant (quality: reported, not failed)

| Store | Target in top 5 | Answer accuracy | Generic: kind in top 5 | Generic: grounded | Abstained when denied | Injection retrieved / obeyed | Whole answer p50 / p95 / p99 ms |
|---|---|---|---|---|---|---|---|
| faiss | 1.000 | 0.984 | 0.825 | 0.525 | 0.728 | 97 / 97 | 1937.3 / 4108.6 / 5971.3 |
| chroma | 0.963 | 0.950 | 1.000 | 0.700 | 0.763 | 43 / 43 | 2985.9 / 5238.1 / 7518.3 |
| pgvector | 0.960 | 0.944 | 1.000 | 0.700 | 0.766 | 62 / 62 | 1588.3 / 2238.5 / 2441.4 |
| pgvector + OPA | 0.960 | 0.944 | 1.000 | 0.700 | 0.766 | 62 / 62 | 1605.2 / 2203.2 / 2477.8 |
| qdrant | 0.394 | 0.391 | 0.100 | 0.025 | 0.724 | 1 / 1 | 1554.6 / 2872.0 / 3040.9 |
| elasticsearch | 0.997 | 0.981 | 0.925 | 0.550 | 0.700 | 52 / 52 | 1624.6 / 2997.7 / 3500.2 |
| opensearch | 0.987 | 0.971 | 0.825 | 0.525 | 0.766 | 101 / 101 | 1629.9 / 2908.2 / 3069.7 |
| weaviate | 0.995 | 0.979 | 1.000 | 0.650 | 0.747 | 29 / 29 | 1638.6 / 2943.4 / 4131.2 |
| redis | 0.997 | 0.981 | 0.950 | 0.700 | 0.728 | 97 / 97 | 1639.0 / 3718.9 / 5674.1 |
| lancedb | 1.000 | 0.984 | 1.000 | 0.700 | 0.739 | 108 / 108 | 1567.6 / 2640.6 / 2844.0 |

## Loading

| Store | Rows | Load s | Index s | Server RSS GiB | Python RSS +GiB | Data GiB | Detail |
|---|---|---|---|---|---|---|---|
| faiss | 107540 | 11.0 | 0.000 | n/a | 0.500 | n/a | IndexFlatIP (exact); metadata matched in Python |
| chroma | 107540 | 192.5 | 0.000 | n/a | 0.460 | 1.020 | chromadb 1.5.9, persistent, HNSW cosine |
| pgvector | 107540 | 62.8 | 27.7 | 2.010 | 0.010 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 962 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |
| pgvector + OPA | 107540 | 62.8 | 27.7 | 2.010 | 0.010 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 962 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |
| qdrant | 107540 | 66.6 | 26.3 | 0.590 | 0.080 | 0.610 | HNSW cosine, hnsw_ef 128; keyword indexes on tenant and permissions |
| elasticsearch | 107540 | 158.3 | 2.100 | 8.750 | 0.010 | 0.860 | Elasticsearch, int8_hnsw index, 0.45 GiB; num_candidates 500 |
| opensearch | 107540 | 203.0 | 0.300 | 8.720 | -0.170 | 0.470 | OpenSearch, Lucene HNSW, 0.37 GiB; num_candidates 500 |
| weaviate | 107540 | 98.9 | 0.000 | 1.180 | -1.110 | 0.740 | HNSW cosine; Weaviate indexes while it imports |
| redis | 107540 | 40.9 | 0.000 | 0.980 | 0.010 | n/a | HNSW cosine, EF_RUNTIME 100, 1020.60M used; search-on-timeout fail |
| lancedb | 107540 | 21.6 | 64.0 | n/a | 0.390 | 0.370 | loaded with the backend's add; IVF_PQ cosine, nprobes 50, refine_factor 30 |

## Permission cache (remote authorizers)

| Store | Hits | Misses | Entries |
|---|---|---|---|
| pgvector + OPA | 7809 | 10654 | 10654 |

## Notes

- corpus: 107,540 chunks (49,920 company documents in 20 tenants, 20 injected notices, 57,600 shared FiQA passages); 189 people ask 1,105 questions ({'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432})
- readable chunks per person: min 0, median 58,641, max 59,265 of 107,540
- faiss: recall@5 1.0, recall@10 1.0; retrieval p50/p95/p99 356.3/458.6/470.7 ms; whole answer p50 1937.3 ms; answer accuracy 0.984; strategies {'prefilter': 1105}
- chroma: recall@5 0.879, recall@10 0.8804; retrieval p50/p95/p99 1432.0/1696.6/1732.6 ms; whole answer p50 2985.9 ms; answer accuracy 0.9495; strategies {'prefilter': 1105}
- pgvector: recall@5 0.6996, recall@10 0.7316; retrieval p50/p95/p99 8.1/47.2/77.3 ms; whole answer p50 1588.3 ms; answer accuracy 0.9441; strategies {'prefilter': 1105}
- pgvector + OPA: recall@5 0.6996, recall@10 0.7316; retrieval p50/p95/p99 8.5/48.4/78.8 ms; whole answer p50 1605.2 ms; answer accuracy 0.9441; strategies {'prefilter': 1105}
- qdrant: recall@5 0.5605, recall@10 0.5492; retrieval p50/p95/p99 4.6/6.0/6.6 ms; whole answer p50 1554.6 ms; answer accuracy 0.391; strategies {'prefilter': 1105}
- elasticsearch: recall@5 0.9384, recall@10 0.9478; retrieval p50/p95/p99 8.4/15.2/27.7 ms; whole answer p50 1624.6 ms; answer accuracy 0.9814; strategies {'prefilter': 1105}
- opensearch: recall@5 0.9389, recall@10 0.9343; retrieval p50/p95/p99 6.9/11.9/17.9 ms; whole answer p50 1629.9 ms; answer accuracy 0.9707; strategies {'prefilter': 1105}
- weaviate: recall@5 0.8991, recall@10 0.9022; retrieval p50/p95/p99 7.8/25.7/31.9 ms; whole answer p50 1638.6 ms; answer accuracy 0.9787; strategies {'prefilter': 1105}
- redis: recall@5 0.9708, recall@10 0.9755; retrieval p50/p95/p99 29.6/33.6/36.3 ms; whole answer p50 1639.0 ms; answer accuracy 0.9814; strategies {'prefilter': 1105}
- lancedb: recall@5 0.8354, recall@10 0.8711; retrieval p50/p95/p99 24.9/32.2/33.8 ms; whole answer p50 1567.6 ms; answer accuracy 0.984; strategies {'prefilter': 1105}
