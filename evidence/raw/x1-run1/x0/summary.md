# X0: the 2026-10-24 Kaggle run, re-analysed

Input: `/kaggle/input/notebooks/muzakkirhussain1/wardowl-end-to-end-scale-run-seed-7`. Overlap@5 is the share of FAISS's top 5 (exact) among a store's top 5 for the same person and question; ties are not credited, so it can sit slightly below the run's recall@5. Questions whose person may read nothing (FAISS returned nothing) are left out.

## Predictions of section 6.0, and what the data show

| Item | Predicted (section 6.0) | Observed |
|---|---|---|
| pgvector empty results | about 10 to 12, all judys, mostly forbidden questions | 0; judys 0; forbidden 0 |
| Qdrant overlap@5 for judys | near 1 | 1.000 |
| Qdrant overlap@5, KB readers, targeted and generic | low | 0.365 |
| pgvector overlap@5: targeted and generic / forbidden and red team | loss concentrated in targeted and generic | 0.885 / 0.561 |
| kb/ share of the top 5 on targeted questions: Qdrant / FAISS | Qdrant mostly kb/ where FAISS has tenant documents | 0.652 / 0.000 |

## The run's own numbers (results.json)

89 checks passed; failed: pgvector + OpenFGA: questions: completed (TimeoutError: http://127.0.0.1:18080/healthz did not answer within 180 s)

| Store | Recall@5 | Recall@10 | Hits checked | Hits short of the most | Short / 15 | Incomplete | p50 ms |
|---|---|---|---|---|---|---|---|
| faiss | 1.000 | 1.000 | 16360 | 0 | 0.000 | 0 | 342.5 |
| chroma | 0.879 | 0.878 | 16360 | 0 | 0.000 | 0 | 1434.7 |
| pgvector | 0.703 | 0.725 | 16248 | 112 | 7.500 | 0 | 7.800 |
| pgvector + OPA | 0.703 | 0.725 | 16248 | 112 | 7.500 | 0 | 8.100 |
| qdrant | 0.537 | 0.530 | 16360 | 0 | 0.000 | 0 | 4.500 |
| elasticsearch | 0.960 | 0.961 | 16360 | 0 | 0.000 | 0 | 8.600 |
| opensearch | 0.948 | 0.939 | 16360 | 0 | 0.000 | 0 | 7.000 |
| weaviate | 0.891 | 0.897 | 16360 | 0 | 0.000 | 0 | 7.400 |
| redis | 0.992 | 0.993 | 16360 | 0 | 0.000 | 0 | 30.1 |
| lancedb | 0.850 | 0.900 | 16360 | 0 | 0.000 | 0 | 23.8 |

## Empty results (k=5, FAISS non-empty)

| store | persona_type | category | questions |
|---|---|---|---|

### pgvector

| person | tenant | category | attack | target | question |
|---|---|---|---|---|---|

## Overlap@5 by category

| store | generic | targeted | forbidden | redteam |
|---|---|---|---|---|
| faiss | 1.000 | 1.000 | 1.000 | 1.000 |
| chroma | 0.823 | 0.972 | 0.847 | 0.817 |
| pgvector | 0.685 | 0.936 | 0.533 | 0.574 |
| pgvector + OPA | 0.685 | 0.936 | 0.533 | 0.574 |
| qdrant | 0.700 | 0.340 | 0.581 | 0.652 |
| elasticsearch | 0.940 | 0.989 | 0.948 | 0.936 |
| opensearch | 0.894 | 0.994 | 0.905 | 0.935 |
| weaviate | 0.787 | 0.991 | 0.866 | 0.833 |
| redis | 1.000 | 0.997 | 1.000 | 0.982 |
| lancedb | 0.894 | 1.000 | 0.810 | 0.724 |

## Overlap@5 by person type

| store | judy | kb-reader | no-groups |
|---|---|---|---|
| faiss | 1.000 | 1.000 | n/a |
| chroma | 0.964 | 0.868 | n/a |
| pgvector | 0.704 | 0.702 | n/a |
| pgvector + OPA | 0.704 | 0.702 | n/a |
| qdrant | 1.000 | 0.494 | n/a |
| elasticsearch | 0.980 | 0.955 | n/a |
| opensearch | 1.000 | 0.942 | n/a |
| weaviate | 1.000 | 0.879 | n/a |
| redis | 1.000 | 0.991 | n/a |
| lancedb | 0.993 | 0.836 | n/a |

## kb/ share of the top 5, targeted questions

| store | kb_share5 | reference_kb_share5 |
|---|---|---|
| faiss | 0.000 | 0.000 |
| chroma | 0.000 | 0.000 |
| pgvector | 0.003 | 0.000 |
| pgvector + OPA | 0.003 | 0.000 |
| qdrant | 0.652 | 0.000 |
| elasticsearch | 0.000 | 0.000 |
| opensearch | 0.000 | 0.000 |
| weaviate | 0.000 | 0.000 |
| redis | 0.000 | 0.000 |
| lancedb | 0.000 | 0.000 |
