# X1: under-retrieval under permission filters, statistics

Input: `/kaggle/working/x1-smoke`; 7,436 result rows of 44 settings; 500 bootstrap resamples, seed 20261026. Verdicts follow PREREGISTRATION.md.

## Verdicts

### Q1: falsified (islanded permitted subgraph in Qdrant)

- confirm: (i) judy recall@10 1.0000 [1.0000, 1.0000] >= 0.95: **True**
- confirm: (ii) company-document recall@10 1.0000 [1.0000, 1.0000] <= 0.75, upper end below judy's lower end: **False**
- confirm: (iii) kb/ share of non-counting top-5 hits n/a >= 0.5: **None**
- confirm: (iv) best of ACORN 1.0 1.0000 [1.0000, 1.0000] and tenant-m0 1.0000 [1.0000, 1.0000] >= 0.90: **True**
- falsify: category miss-rate spread 0.000 < 0.10: **True**
- falsify: gains of ACORN 1.0 and tenant-m0 (0.000, 0.000) both < 0.02: **True**

### Q2: falsified (ACORN's default gate engages unreliably)

- confirm: share of people ACORN 0.4 engaged for 0.000 in (0.05, 0.95): **False**
- confirm: ACORN 1.0 minus 0.4 in recall@10 0.0000 [0.0000, 0.0000] above 0: **False**
- falsify: |ACORN 1.0 minus 0.4| < 0.01 with an interval containing 0: **True**
- notes: engagement: inferred (top 5 differs from q-asrun on the same build): the telemetry did not count ACORN

### Q3: inconclusive (recall varies by build and segment layout)

- confirm: recall@10 range between as-run builds n/a >= 0.01: **None**
- confirm: one-segment minus as-run 0.0000 [0.0000, 0.0000] excludes 0: **False**
- falsify: range < 0.002 and |one-segment minus as-run| < 0.002: **None**
- notes: segments: as-run {'{"wardowl_enterprise": 2}'}, one-segment {'{"wardowl_enterprise": 1}'}

### Q4: confirmed (hnsw_ef 128 was not the cause)

- confirm: hnsw_ef 512 minus 128 0.0000 [0.0000, 0.0000] < 0.05: **True**
- falsify: gain > 0.15: **False**

### P1: inconclusive (the iterative scan's budget runs out)

- confirm: p-asrun reproduces empty results: **False**
- notes: no empty result under p-asrun

### P2: confirmed (mis-retrieval from shallow, relaxed scans)

- confirm: (a) ef_search 1000 minus 100 0.0372 [0.0182, 0.0515] >= 0.02, above 0: **True**
- confirm: (b) inner LIMIT 10x minus 1x 0.0372 [0.0188, 0.0527] above 0: **True**
- confirm: (c) m32/efc200 minus m16/efc64 0.0372 [0.0203, 0.0536] above 0: **True**
- confirm: (d) loss at rho_100 < 0.1 0.045 at least twice the rest 0.009: **True**
- confirm: (e) mean similarity gap of missed questions 0.002 <= 0.02: **True**
- falsify: |ef_search 1000 minus 100| < 0.01 with an interval containing 0: **False**

### P3: confirmed (the planner overestimates a judy filter)

- confirm: median planner estimate / R for judys 13.4 >= 5: **True**
- confirm: ph-exact ERR 0.000 == 0: **True**
- falsify: median ratio within [0.5, 2]: **False**

### P4: falsified (generic plans make no difference)

- confirm: pg-custom: |recall@10 difference| 0.0000 [0.0000, 0.0000] < 0.005: **True**
- confirm: pg-custom: |ERR difference| 0.0000 [0.0000, 0.0000] < 0.002: **True**
- confirm: pg-noprepare: |recall@10 difference| 0.0000 [0.0000, 0.0000] < 0.005: **True**
- confirm: pg-noprepare: |ERR difference| 0.0000 [0.0000, 0.0000] < 0.002: **True**
- confirm: generic plans run under p-asrun: 53; fixed questions with another generic plan: 6 of 10: none run, or none differs: **False**
- falsify: pg-custom: |recall@10 difference| >= 0.01, interval excluding 0: **False**
- falsify: pg-custom: McNemar p for ERR 1.000 < 0.05: **False**
- falsify: pg-noprepare: |recall@10 difference| >= 0.01, interval excluding 0: **False**
- falsify: pg-noprepare: McNemar p for ERR 1.000 < 0.05: **False**
- falsify: generic plans run under p-asrun: 53; fixed questions with another generic plan: 6 of 10: some run and some differ: **True**
- notes: generic plans of the search statement, summed over builds, per setting: {'p-asrun': 53, 'pg-custom': 0, 'pg-noprepare': 0} (amendment 1)

## Settings (means over builds; range between builds)

| store | layout | setting | builds | recall5 | recall10 | recall10_range | empty5 | short5 | gross_miss10 | sim_gap10 | latency_p50 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | hnsw-m16-efc64 | p-asrun | 1 | 0.955 | 0.963 | n/a | 0.000 | 0.000 | 0.014 | 0.001 | 3.426 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m1 | 1 | 0.955 | 0.963 | n/a | 0.000 | 0.000 | 0.014 | 0.001 | 3.763 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m16 | 1 | 0.955 | 0.963 | n/a | 0.000 | 0.000 | 0.014 | 0.001 | 3.535 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m8 | 1 | 0.955 | 0.963 | n/a | 0.000 | 0.000 | 0.014 | 0.001 | 4.061 |
| pgvector | hnsw-m16-efc64 | pa-t100k-m1 | 1 | 0.955 | 0.963 | n/a | 0.000 | 0.000 | 0.014 | 0.001 | 3.863 |
| pgvector | hnsw-m16-efc64 | pa-t100k-m8 | 1 | 0.955 | 0.963 | n/a | 0.000 | 0.000 | 0.014 | 0.001 | 4.311 |
| pgvector | hnsw-m16-efc64 | pa-t20k-m8 | 1 | 0.955 | 0.963 | n/a | 0.000 | 0.000 | 0.014 | 0.001 | 4.043 |
| pgvector | hnsw-m16-efc64 | pb-wm64 | 1 | 0.999 | 0.999 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 13.0 |
| pgvector | hnsw-m16-efc64 | pc-ef1000 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 13.1 |
| pgvector | hnsw-m16-efc64 | pc-ef200 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 13.1 |
| pgvector | hnsw-m16-efc64 | pc-ef40 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 13.2 |
| pgvector | hnsw-m16-efc64 | pc-ef400 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 13.0 |
| pgvector | hnsw-m16-efc64 | pd-lim10 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 13.5 |
| pgvector | hnsw-m16-efc64 | pd-lim4 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 13.5 |
| pgvector | hnsw-m16-efc64 | pe-strict | 1 | 0.997 | 0.995 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 12.9 |
| pgvector | hnsw-m16-efc64 | pg-custom | 1 | 0.955 | 0.963 | n/a | 0.000 | 0.000 | 0.014 | 0.001 | 3.242 |
| pgvector | hnsw-m16-efc64 | pg-noprepare | 1 | 0.955 | 0.963 | n/a | 0.000 | 0.000 | 0.014 | 0.001 | 2.983 |
| pgvector | hnsw-m16-efc64 | ph-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 13.1 |
| pgvector | hnsw-m32-efc200 | p-asrun | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 13.2 |
| pgvector | hnsw-m32-efc200 | pa-t1000k-m8 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 13.7 |
| pgvector | hnsw-m32-efc200 | pc-ef400 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 13.2 |
| pgvector | hnsw-m32-efc200 | pd-lim10 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 13.4 |
| qdrant | as-run | q-asrun | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.064 |
| qdrant | as-run | qa-acorn040 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.084 |
| qdrant | as-run | qa-acorn100 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.130 |
| qdrant | as-run | qb-ef512 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 2.952 |
| qdrant | as-run | qb-ef64 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.194 |
| qdrant | as-run | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.096 |
| qdrant | is-tenant | q-asrun | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.095 |
| qdrant | is-tenant | qa-acorn040 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.056 |
| qdrant | is-tenant | qa-acorn100 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.121 |
| qdrant | is-tenant | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.166 |
| qdrant | one-segment | q-asrun | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.394 |
| qdrant | one-segment | qa-acorn040 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.260 |
| qdrant | one-segment | qa-acorn100 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.295 |
| qdrant | one-segment | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.198 |
| qdrant | separate-kb | q-asrun | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 5.591 |
| qdrant | separate-kb | qa-acorn040 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 5.427 |
| qdrant | separate-kb | qa-acorn100 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 5.512 |
| qdrant | separate-kb | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 5.615 |
| qdrant | tenant-m0 | q-asrun | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.145 |
| qdrant | tenant-m0 | qa-acorn040 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.018 |
| qdrant | tenant-m0 | qa-acorn100 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 3.048 |
| qdrant | tenant-m0 | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 2.968 |

Qdrant search paths were read from the telemetry path `result/collections/collections/shards/local/segments/vector_index_searches`.
