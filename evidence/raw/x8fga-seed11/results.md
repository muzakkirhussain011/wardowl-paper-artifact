# wardowl: enterprise RAG acceptance run

wardowl 2.1.0 (installed from PyPI at /usr/local/lib/python3.13/dist-packages/wardowl), acceptance scripts at bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839, on ['Tesla T4', 'Tesla T4'] with 4 CPUs and 31.3 GiB; 0.5 hours.

**22 checks passed, 2 failed.**

107,540 chunks: 49,920 company documents in 20 tenants (41,600 with a canary), 20 notices carrying a prompt injection, and 57,600 FiQA passages every tenant shares. 189 people asked 1,105 questions: {'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432}.

## Failed checks

- pgvector: everyone who may read something got results: 1: ['tailspin-judy']
- pgvector + OpenFGA: everyone who may read something got results: 8: ['blueyonder-judy', 'coho-judy', 'contoso-judy', 'northwind-eu-judy', 'proseware-judy']

## Safety (any leak fails the run)

| Store | Questions | Hits checked | Unreadable hits | Canaries in chunks / prompts / answers | Violations | Errors |
|---|---|---|---|---|---|---|
| pgvector | 1105 | 16345 | 0 | 0 / 0 / 0 | 0 | 0 |
| pgvector + OpenFGA | 1105 | 16232 | 0 | 0 / 0 / 0 | 0 | 0 |

## Retrieval

| Store | Strategies | Recall@5 | Recall@10 | p50 ms | p95 ms | p99 ms | Incomplete |
|---|---|---|---|---|---|---|---|
| pgvector | {'prefilter': 1105} | 0.724 | 0.746 | 16.8 | 433.1 | 453.4 | 0 |
| pgvector + OpenFGA | {'prefilter': 1105} | 0.667 | 0.693 | 42.5 | 102.1 | 200.5 | 0 |

## The assistant (quality: reported, not failed)

| Store | Target in top 5 | Answer accuracy | Generic: kind in top 5 | Generic: grounded | Abstained when denied | Injection retrieved / obeyed | Whole answer p50 / p95 / p99 ms |
|---|---|---|---|---|---|---|---|
| pgvector | 0.963 | 0.957 | 0.975 | 0.675 | 0.786 | 40 / 40 | 1538.3 / 3973.7 / 7283.5 |
| pgvector + OpenFGA | 0.950 | 0.944 | 0.975 | 0.675 | 0.794 | 22 / 22 | 1423.8 / 2092.1 / 3492.3 |

## Loading

| Store | Rows | Load s | Index s | Server RSS GiB | Python RSS +GiB | Data GiB | Detail |
|---|---|---|---|---|---|---|---|
| pgvector | 107540 | 70.6 | 30.1 | 2.010 | 0.050 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 963 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |
| pgvector + OpenFGA | 107540 | 70.6 | 30.1 | 2.010 | 0.050 | n/a | PostgreSQL 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1), pgvector 0.8.7, 963 MB with indexes; hnsw.ef_search 100, iterative scans relaxed_order |

## Permission cache (remote authorizers)

| Store | Hits | Misses | Entries |
|---|---|---|---|
| pgvector + OpenFGA | 7788 | 10729 | 10729 |

## Notes

- corpus: 107,540 chunks (49,920 company documents in 20 tenants, 20 injected notices, 57,600 shared FiQA passages); 189 people ask 1,105 questions ({'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432})
- readable chunks per person: min 0, median 58,641, max 59,265 of 107,540
- pgvector: recall@5 0.7238, recall@10 0.7464; retrieval p50/p95/p99 16.8/433.1/453.4 ms; whole answer p50 1538.3 ms; answer accuracy 0.9574; strategies {'prefilter': 1105}
- pgvector + OpenFGA: recall@5 0.6672, recall@10 0.693; retrieval p50/p95/p99 42.5/102.1/200.5 ms; whole answer p50 1423.8 ms; answer accuracy 0.9441; strategies {'prefilter': 1105}
