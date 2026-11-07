# X1: under-retrieval under permission filters, statistics

Input: `/kaggle/working/x1`; 99,763 result rows of 33 settings; 10,000 bootstrap resamples, seed 20261026. Verdicts follow PREREGISTRATION.md.

## Verdicts

### Q1: confirmed (islanded permitted subgraph in Qdrant)

- confirm: (i) judy recall@10 1.0000 [1.0000, 1.0000] >= 0.95: **True**
- confirm: (ii) company-document recall@10 0.3135 [0.2756, 0.3498] <= 0.75, upper end below judy's lower end: **True**
- confirm: (iii) kb/ share of non-counting top-5 hits 0.979 >= 0.5: **True**
- confirm: (iv) best of ACORN 1.0 0.8139 [0.7913, 0.8352] and tenant-m0 0.9366 [0.9259, 0.9465] >= 0.90: **True**
- falsify: category miss-rate spread 0.627 < 0.10: **False**
- falsify: gains of ACORN 1.0 and tenant-m0 (0.173, 0.295) both < 0.02: **False**

### Q2: falsified (ACORN's default gate engages unreliably)

- confirm: share of people ACORN 0.4 engaged for 1.000 in (0.05, 0.95): **False**
- confirm: ACORN 1.0 minus 0.4 in recall@10 0.0000 [0.0000, 0.0000] above 0: **False**
- falsify: |ACORN 1.0 minus 0.4| < 0.01 with an interval containing 0: **True**
- notes: engagement: telemetry (filtered_acorn among people whose searches took a graph path)

### Q3: inconclusive (recall varies by build and segment layout)

- confirm: recall@10 range between as-run builds 0.021 >= 0.01: **True**
- confirm: one-segment minus as-run -0.0025 [-0.0142, 0.0096] excludes 0: **False**
- falsify: range < 0.002 and |one-segment minus as-run| < 0.002: **False**
- notes: segments: as-run {'{"wardowl_enterprise": 2}'}, one-segment {'{"wardowl_enterprise": 2}'}; both layouts ended with the same segments

### Q4: inconclusive (hnsw_ef 128 was not the cause)

- confirm: hnsw_ef 512 minus 128 0.0971 [0.0842, 0.1100] < 0.05: **False**
- falsify: gain > 0.15: **False**

### P1: inconclusive (the iterative scan's budget runs out)

- confirm: p-asrun reproduces empty results: **False**
- notes: no empty result under p-asrun

### P2: inconclusive (mis-retrieval from shallow, relaxed scans)

- confirm: (a) ef_search 1000 minus 100 missing >= 0.02, above 0: **None**
- confirm: (b) inner LIMIT 10x minus 1x missing above 0: **None**
- confirm: (c) m32/efc200 minus m16/efc64 missing above 0: **None**
- confirm: (d) loss at rho_100 < 0.1 0.081 at least twice the rest 0.074: **False**
- confirm: (e) mean similarity gap of missed questions 0.015 <= 0.02: **True**
- falsify: |ef_search 1000 minus 100| < 0.01 with an interval containing 0: **None**

### P3: inconclusive (the planner overestimates a judy filter)

- confirm: median planner estimate / R for judys 11.5 >= 5: **True**
- confirm: ph-exact ERR n/a == 0: **None**
- falsify: median ratio within [0.5, 2]: **False**

### P4: falsified (generic plans make no difference)

- confirm: pg-custom: |recall@10 difference| missing < 0.005: **None**
- confirm: pg-custom: |ERR difference| missing < 0.002: **None**
- confirm: pg-noprepare: |recall@10 difference| missing < 0.005: **None**
- confirm: pg-noprepare: |ERR difference| missing < 0.002: **None**
- confirm: generic plans run under p-asrun: 4308; fixed questions with another generic plan: 50 of 50: none run, or none differs: **False**
- falsify: pg-custom: |recall@10 difference| >= 0.01, interval excluding 0: **None**
- falsify: pg-custom: McNemar p for ERR n/a < 0.05: **None**
- falsify: pg-noprepare: |recall@10 difference| >= 0.01, interval excluding 0: **None**
- falsify: pg-noprepare: McNemar p for ERR n/a < 0.05: **None**
- falsify: generic plans run under p-asrun: 4308; fixed questions with another generic plan: 50 of 50: some run and some differ: **True**
- notes: generic plans of the search statement, summed over builds, per setting: {'p-asrun': 4308} (amendment 1)

## Settings (means over builds; range between builds)

| store | layout | setting | builds | recall5 | recall10 | recall10_range | empty5 | short5 | gross_miss10 | sim_gap10 | latency_p50 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | hnsw-m16-efc64 | p-asrun | 1 | 0.907 | 0.920 | n/a | 0.000 | 0.000 | 0.082 | 0.003 | 352.2 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m1 | 1 | 0.999 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 385.7 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m16 | 1 | 0.999 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 377.3 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m8 | 1 | 0.999 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 385.9 |
| pgvector | hnsw-m16-efc64 | pa-t100k-m1 | 1 | 0.999 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 370.3 |
| pgvector | hnsw-m16-efc64 | pa-t100k-m8 | 1 | 0.999 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 378.6 |
| pgvector | hnsw-m16-efc64 | pa-t20k-m8 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 388.9 |
| pgvector | hnsw-m16-efc64 | pb-wm64 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 376.0 |
| pgvector | hnsw-m16-efc64 | pc-ef200 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 372.3 |
| pgvector | hnsw-m16-efc64 | pc-ef40 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 382.2 |
| pgvector | hnsw-m16-efc64 | pc-ef400 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 373.1 |
| qdrant | as-run | q-asrun | 3 | 0.648 | 0.641 | 0.021 | 0.000 | 0.001 | 0.383 | 0.045 | 4.232 |
| qdrant | as-run | qa-acorn040 | 3 | 0.817 | 0.814 | 0.060 | 0.000 | 0.001 | 0.215 | 0.016 | 4.366 |
| qdrant | as-run | qa-acorn100 | 3 | 0.817 | 0.814 | 0.060 | 0.000 | 0.001 | 0.215 | 0.016 | 4.404 |
| qdrant | as-run | qb-ef512 | 3 | 0.739 | 0.738 | 0.012 | 0.000 | 0.001 | 0.298 | 0.035 | 7.145 |
| qdrant | as-run | qb-ef64 | 3 | 0.597 | 0.591 | 0.032 | 0.000 | 0.001 | 0.423 | 0.050 | 3.626 |
| qdrant | as-run | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 34.1 |
| qdrant | is-tenant | q-asrun | 3 | 0.638 | 0.631 | 0.047 | 0.000 | 0.000 | 0.396 | 0.047 | 4.174 |
| qdrant | is-tenant | qa-acorn040 | 3 | 0.822 | 0.818 | 0.030 | 0.000 | 0.000 | 0.217 | 0.015 | 4.336 |
| qdrant | is-tenant | qa-acorn100 | 3 | 0.822 | 0.818 | 0.030 | 0.000 | 0.000 | 0.217 | 0.015 | 4.338 |
| qdrant | is-tenant | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 31.6 |
| qdrant | one-segment | q-asrun | 3 | 0.644 | 0.639 | 0.012 | 0.000 | 0.002 | 0.380 | 0.045 | 4.436 |
| qdrant | one-segment | qa-acorn040 | 3 | 0.815 | 0.814 | 0.030 | 0.000 | 0.000 | 0.211 | 0.016 | 4.677 |
| qdrant | one-segment | qa-acorn100 | 3 | 0.815 | 0.814 | 0.030 | 0.000 | 0.000 | 0.211 | 0.016 | 4.624 |
| qdrant | one-segment | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 35.4 |
| qdrant | separate-kb | q-asrun | 3 | 0.952 | 0.948 | 0.010 | 0.000 | 0.000 | 0.042 | 0.001 | 7.641 |
| qdrant | separate-kb | qa-acorn040 | 3 | 0.952 | 0.948 | 0.010 | 0.000 | 0.000 | 0.042 | 0.001 | 7.617 |
| qdrant | separate-kb | qa-acorn100 | 3 | 0.952 | 0.948 | 0.010 | 0.000 | 0.000 | 0.042 | 0.001 | 7.769 |
| qdrant | separate-kb | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 34.6 |
| qdrant | tenant-m0 | q-asrun | 3 | 0.937 | 0.937 | 0.005 | 0.000 | 0.000 | 0.087 | 0.004 | 4.244 |
| qdrant | tenant-m0 | qa-acorn040 | 3 | 0.937 | 0.937 | 0.005 | 0.000 | 0.000 | 0.087 | 0.004 | 4.246 |
| qdrant | tenant-m0 | qa-acorn100 | 3 | 0.937 | 0.937 | 0.005 | 0.000 | 0.000 | 0.087 | 0.004 | 4.242 |
| qdrant | tenant-m0 | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 30.5 |

Qdrant search paths were read from the telemetry path `result/collections/collections/shards/local/segments/vector_index_searches`.
