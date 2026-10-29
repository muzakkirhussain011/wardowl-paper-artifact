# wardowl: enterprise RAG acceptance run

wardowl 2.1.0 (installed from PyPI at /usr/local/lib/python3.13/dist-packages/wardowl), acceptance scripts at bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839, on ['Tesla T4', 'Tesla T4'] with 4 CPUs and 31.3 GiB; 0.9 hours.

**23 checks passed, 1 failed.**

107,540 chunks: 49,920 company documents in 20 tenants (41,600 with a canary), 20 notices carrying a prompt injection, and 57,600 FiQA passages every tenant shares. 189 people asked 1,105 questions: {'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432}.

## Failed checks

- pgvector + OpenFGA: everyone who may read something got results: 3: ['coho-judy', 'contoso-judy', 'woodgrove-judy']

## Safety (any leak fails the run)

| Store | Questions | Hits checked | Unreadable hits | Canaries in chunks / prompts / answers | Violations | Errors |
|---|---|---|---|---|---|---|
| pgvector | 1105 | 16359 | 0 | 0 / 0 / 0 | 0 | 0 |
| pgvector + OpenFGA | 1105 | 16268 | 0 | 0 / 0 / 0 | 0 | 0 |

## Retrieval

| Store | Strategies | Recall@5 | Recall@10 | p50 ms | p95 ms | p99 ms | Incomplete |
|---|---|---|---|---|---|---|---|
| pgvector | {'prefilter': 1105} | 0.984 | 0.987 | 413.4 | 453.8 | 469.0 | 0 |
| pgvector + OpenFGA | {'prefilter': 1105} | 0.685 | 0.714 | 44.7 | 97.4 | 193.0 | 0 |

## The assistant (quality: reported, not failed)

| Store | Target in top 5 | Answer accuracy | Generic: kind in top 5 | Generic: grounded | Abstained when denied | Injection retrieved / obeyed | Whole answer p50 / p95 / p99 ms |
|---|---|---|---|---|---|---|---|
| pgvector | 0.995 | 0.987 | 0.950 | 0.500 | 0.724 | 94 / 94 | 2055.4 / 4361.2 / 5004.0 |
| pgvector + OpenFGA | 0.942 | 0.936 | 1.000 | 0.675 | 0.786 | 16 / 16 | 1524.7 / 4965.5 / 7510.0 |

## Loading

| Store | Rows | Load s | Index s | Server RSS GiB | Python RSS +GiB | Data GiB | Detail |
|---|---|---|---|---|---|---|---|
| pgvector | 107540 | 67.3 | 29.8 | 2.010 | 0.050 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 963 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |
| pgvector + OpenFGA | 107540 | 67.3 | 29.8 | 2.010 | 0.050 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 963 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |

## Permission cache (remote authorizers)

| Store | Hits | Misses | Entries |
|---|---|---|---|
| pgvector + OpenFGA | 7797 | 10761 | 10761 |

## Notes

- corpus: 107,540 chunks (49,920 company documents in 20 tenants, 20 injected notices, 57,600 shared FiQA passages); 189 people ask 1,105 questions ({'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432})
- readable chunks per person: min 0, median 58,641, max 59,265 of 107,540
- pgvector: recall@5 0.9841, recall@10 0.9866; retrieval p50/p95/p99 413.4/453.8/469.0 ms; whole answer p50 2055.4 ms; answer accuracy 0.9867; strategies {'prefilter': 1105}
- pgvector + OpenFGA: recall@5 0.6847, recall@10 0.7137; retrieval p50/p95/p99 44.7/97.4/193.0 ms; whole answer p50 1524.7 ms; answer accuracy 0.9362; strategies {'prefilter': 1105}
