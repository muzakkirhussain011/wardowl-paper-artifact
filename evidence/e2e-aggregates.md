# End-to-end aggregates (computed by evidence/aggregate_e2e.py)

## Outcomes per run

| Run | Checks passed / failed | Failed checks | Kernel seconds |
|---|---|---|---|
| X0, seed 7 | 89 / 1 | pgvector + OpenFGA: questions: completed: TimeoutError: http://127.0.0.1:18080/healthz did not answer within 180 s | 10242.916414263 |
| X8, seed 11 | 88 / 2 | pgvector: everyone who may read something got results: 1: ['tailspin-judy']; pgvector + OpenFGA: questions: completed: TimeoutError: http://127.0.0.1:18080/healthz did not answer within 180 s | 11773.379263017 |
| X8, seed 13 | 89 / 1 | pgvector + OpenFGA: questions: completed: TimeoutError: http://127.0.0.1:18080/healthz did not answer within 180 s | 11144.043878885 |
| X8, seed 17 | 87 / 3 | pgvector: everyone who may read something got results: 7: ['adatum-judy', 'blueyonder-judy', 'coho-judy', 'contoso-judy', 'proseware-judy']; pgvector + OPA: everyone who may read something got results: 7: ['adatum-judy', 'blueyonder-judy', 'coho-judy', 'contoso-judy', 'proseware-judy']; pgvector + OpenFGA: questions: completed: TimeoutError: http://127.0.0.1:18080/healthz did not answer within 180 s | 10355.887015409 |
| X8-FGA, seed 7 | 22 / 2 | pgvector: everyone who may read something got results: 1: ['coho-judy']; pgvector + OpenFGA: everyone who may read something got results: 7: ['alpine-judy', 'coho-judy', 'fabrikam-judy', 'northwind-eu-judy', 'proseware-judy'] | 3417.646120292 |
| X8-FGA, seed 11 | 22 / 2 | pgvector: everyone who may read something got results: 1: ['tailspin-judy']; pgvector + OpenFGA: everyone who may read something got results: 8: ['blueyonder-judy', 'coho-judy', 'contoso-judy', 'northwind-eu-judy', 'proseware-judy'] | 2115.591875633 |
| X8-FGA, seed 13 | 23 / 1 | pgvector + OpenFGA: everyone who may read something got results: 3: ['coho-judy', 'contoso-judy', 'woodgrove-judy'] | 3269.195204174 |
| X8-FGA, seed 17 | 23 / 1 | pgvector + OpenFGA: everyone who may read something got results: 10: ['adatum-judy', 'blueyonder-judy', 'coho-judy', 'contoso-judy', 'northwind-eu-judy'] | 3218.767314404 |

## Empty answers / people, pgvector configurations

| Run | pgvector | pgvector + OPA | pgvector + OpenFGA | People left out |
|---|---|---|---|---|
| X0, seed 7 | 0 / 0 [] | 0 / 0 [] |  |  |
| X8, seed 11 | 1 / 1 ['tailspin-judy'] | 0 / 0 [] |  |  |
| X8, seed 13 | 0 / 0 [] | 0 / 0 [] |  |  |
| X8, seed 17 | 7 / 7 ['adatum-judy', 'blueyonder-judy', 'coho-judy', 'contoso-judy', 'proseware-judy', 'relecloud-judy', 'woodgrove-judy'] | 7 / 7 ['adatum-judy', 'blueyonder-judy', 'coho-judy', 'contoso-judy', 'proseware-judy', 'relecloud-judy', 'woodgrove-judy'] |  |  |
| X8-FGA, seed 7 | 1 / 1 ['coho-judy'] |  | 7 / 6 ['alpine-judy', 'coho-judy', 'fabrikam-judy', 'northwind-eu-judy', 'proseware-judy', 'tailspin-judy'] | ['mallory'] |
| X8-FGA, seed 11 | 1 / 1 ['tailspin-judy'] |  | 8 / 8 ['blueyonder-judy', 'coho-judy', 'contoso-judy', 'northwind-eu-judy', 'proseware-judy', 'relecloud-judy', 'tailspin-judy', 'woodgrove-judy'] | ['mallory'] |
| X8-FGA, seed 13 | 0 / 0 [] |  | 3 / 3 ['coho-judy', 'contoso-judy', 'woodgrove-judy'] | ['mallory'] |
| X8-FGA, seed 17 | 0 / 0 [] |  | 10 / 9 ['adatum-judy', 'blueyonder-judy', 'coho-judy', 'contoso-judy', 'northwind-eu-judy', 'proseware-judy', 'relecloud-judy', 'tailspin-judy', 'woodgrove-judy'] | ['mallory'] |

## Safety

| Run | Configurations | Questions | Hits checked | Unreadable | Leaks retrieved/prompts/answers | Violations | Errors |
|---|---|---|---|---|---|---|---|
| X0, seed 7 | 10 | 11,050 | 163,376 | 0 | 0/0/0 | 0 | 0 |
| X8, seed 11 | 10 | 11,050 | 163,585 | 0 | 0/0/0 | 0 | 0 |
| X8, seed 13 | 10 | 11,050 | 163,591 | 0 | 0/0/0 | 0 | 0 |
| X8, seed 17 | 10 | 11,050 | 163,226 | 0 | 0/0/0 | 0 | 0 |
| X8-FGA, seed 7 | 2 | 2,210 | 32,501 | 0 | 0/0/0 | 0 | 0 |
| X8-FGA, seed 11 | 2 | 2,210 | 32,577 | 0 | 0/0/0 | 0 | 0 |
| X8-FGA, seed 13 | 2 | 2,210 | 32,627 | 0 | 0/0/0 | 0 | 0 |
| X8-FGA, seed 17 | 2 | 2,210 | 32,545 | 0 | 0/0/0 | 0 | 0 |
| **X0 and X8, four runs** | | **44,200** | **653,778** | **0** | **0/0/0** | **0** | **0** |

Hits checked per configuration, four runs: faiss 65,440 (16,360 + 16,360 + 16,360 + 16,360); chroma 65,440 (16,360 + 16,360 + 16,360 + 16,360); pgvector 65,117 (16,248 + 16,345 + 16,351 + 16,173); pgvector + OPA 65,141 (16,248 + 16,360 + 16,360 + 16,173); qdrant 65,440 (16,360 + 16,360 + 16,360 + 16,360); elasticsearch 65,440 (16,360 + 16,360 + 16,360 + 16,360); opensearch 65,440 (16,360 + 16,360 + 16,360 + 16,360); weaviate 65,440 (16,360 + 16,360 + 16,360 + 16,360); redis 65,440 (16,360 + 16,360 + 16,360 + 16,360); lancedb 65,440 (16,360 + 16,360 + 16,360 + 16,360).
pgvector + OpenFGA over the four X8-FGA runs: 64,845 hits checked.

Leak bounds: 4,420 questions per configuration, one-sided 95% bound 6.78e-04; 3,746 distinct (person, question) pairs over the four runs (in four runs: 216, three: 0, two: 26, one: 3504), bound 7.99e-04; X0 alone 2.71e-03; per person per run 1.57e-02.

## Retrieval across the four runs (recall against exact search over the readable set)

| Store | R@5 per run | mean | R@10 per run | mean | range R@10 | p50 ms per run | mode by p50 |
|---|---|---|---|---|---|---|---|
| faiss | 1.000 / 1.000 / 1.000 / 1.000 | 1.000 | 1.000 / 1.000 / 1.000 / 1.000 | 1.000 | 0.000 | 342.5 / 355.4 / 367.5 / 356.3 |  |
| chroma | 0.879 / 0.879 / 0.864 / 0.879 | 0.875 | 0.878 / 0.880 / 0.873 / 0.880 | 0.878 | 0.007 | 1434.7 / 1481.1 / 1444.4 / 1432 |  |
| pgvector | 0.703 / 0.992 / 0.994 / 0.700 | 0.847 | 0.725 / 0.992 / 0.994 / 0.732 | 0.861 | 0.268 | 7.8 / 398.7 / 386 / 8.1 | fast / exact / exact / fast |
| pgvector + OPA | 0.703 / 1.000 / 1.000 / 0.700 | 0.851 | 0.725 / 1.000 / 1.000 / 0.732 | 0.864 | 0.275 | 8.1 / 407.6 / 389.5 / 8.5 | fast / exact / exact / fast |
| qdrant | 0.537 / 0.534 / 0.569 / 0.560 | 0.550 | 0.530 / 0.535 / 0.561 / 0.549 | 0.544 | 0.030 | 4.5 / 4.7 / 4.7 / 4.6 |  |
| elasticsearch | 0.960 / 0.929 / 0.952 / 0.938 | 0.945 | 0.961 / 0.940 / 0.959 / 0.948 | 0.952 | 0.021 | 8.6 / 8.6 / 8.8 / 8.4 |  |
| opensearch | 0.948 / 0.942 / 0.942 / 0.939 | 0.942 | 0.939 / 0.936 / 0.933 / 0.934 | 0.936 | 0.005 | 7 / 7 / 7.1 / 6.9 |  |
| weaviate | 0.891 / 0.902 / 0.908 / 0.899 | 0.900 | 0.897 / 0.902 / 0.913 / 0.902 | 0.903 | 0.016 | 7.4 / 8 / 8 / 7.8 |  |
| redis | 0.992 / 0.980 / 0.995 / 0.971 | 0.984 | 0.993 / 0.982 / 0.988 / 0.976 | 0.985 | 0.017 | 30.1 / 30.4 / 30.4 / 29.6 |  |
| lancedb | 0.850 / 0.832 / 0.861 / 0.835 | 0.845 | 0.900 / 0.866 / 0.899 / 0.871 | 0.884 | 0.034 | 23.8 / 24.7 / 24.8 / 24.9 |  |

In-process pgvector over the eight runs (p50, p95 ms, recall@10): X0, seed 7: 7.8, 45.6, 0.725 (fast); X8, seed 11: 398.7, 438, 0.992 (exact); X8, seed 13: 386, 421.4, 0.994 (exact); X8, seed 17: 8.1, 47.2, 0.732 (fast); X8-FGA, seed 7: 391.4, 427.3, 0.993 (exact); X8-FGA, seed 11: 16.8, 433.1, 0.746 (fast); X8-FGA, seed 13: 413.4, 453.8, 0.987 (exact); X8-FGA, seed 17: 380.3, 417.6, 0.996 (exact).
fast: 3 runs, recall@10 0.725 to 0.746, p50 7.8 to 16.8 ms.
exact: 5 runs, recall@10 0.987 to 0.996, p50 380.3 to 413.4 ms.
pgvector, fast runs of the four: 2; mean R@5 0.701, mean R@10 0.729, R@10 range 0.006, p50 7.8 to 8.1 ms.
pgvector, exact runs of the four: 2; mean R@5 0.993, mean R@10 0.993, R@10 range 0.002, p50 386 to 398.7 ms.
pgvector + OPA, fast runs of the four: 2; mean R@5 0.701, mean R@10 0.729, R@10 range 0.006, p50 8.1 to 8.5 ms.
pgvector + OPA, exact runs of the four: 2; mean R@5 1.000, mean R@10 1.000, R@10 range 0.000, p50 389.5 to 407.6 ms.
pgvector load 62.8 to 65.6 s, index 27.0 to 28.9 s over the four runs.

## The model

| Run | Configurations | Injected notices retrieved | Obeyed | Per configuration |
|---|---|---|---|---|
| X0, seed 7 | 10 | 652 | 652 | 3 to 102 |
| X8, seed 11 | 10 | 741 | 741 | 11 to 117 |
| X8, seed 13 | 10 | 768 | 768 | 3 to 112 |
| X8, seed 17 | 10 | 652 | 652 | 1 to 108 |
| X8-FGA, seed 7 | 2 | 137 | 137 | 41 to 96 |
| X8-FGA, seed 11 | 2 | 62 | 62 | 22 to 40 |
| X8-FGA, seed 13 | 2 | 110 | 110 | 16 to 94 |
| X8-FGA, seed 17 | 2 | 117 | 117 | 21 to 96 |
| **X0 and X8** | | **2,813** | **2,813** | |
| **All eight runs** | | **3,239** | **3,239** | |

FAISS target in the top five 1.000 to 1.000, answer accuracy 0.984 to 0.997; Qdrant target in the top five 0.338 to 0.396; abstained when denied 0.681 to 0.821 over all stores of the four runs.
X8-FGA, seed 7, pgvector + OpenFGA: R@10 0.758, p50 38.3 ms, injections 41/41.
X8-FGA, seed 11, pgvector + OpenFGA: R@10 0.693, p50 42.5 ms, injections 22/22.
X8-FGA, seed 13, pgvector + OpenFGA: R@10 0.714, p50 44.7 ms, injections 16/16.
X8-FGA, seed 17, pgvector + OpenFGA: R@10 0.735, p50 37 ms, injections 21/21.
