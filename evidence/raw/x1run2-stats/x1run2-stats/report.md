# X1: under-retrieval under permission filters, statistics

Input: `/kaggle/input/notebooks/muzakkirhussain1/x1run2-shard-a/x1run2`, `/kaggle/input/notebooks/muzakkirhussain1/x1run2-shard-b/x1run2`, `/kaggle/input/notebooks/muzakkirhussain1/x1run2-shard-c/x1run2` (grid run2); 194,291 result rows of 49 settings; 10,000 bootstrap resamples, seed 20261026. Verdicts follow PREREGISTRATION.md, with amendment 2: P1 and P2 read `pg-hnsw` where they say `p-asrun`.

## Verdicts

### Q1: confirmed (islanded permitted subgraph in Qdrant)

- confirm: (i) judy recall@10 1.0000 [1.0000, 1.0000] >= 0.95: **True**
- confirm: (ii) company-document recall@10 0.3689 [0.3343, 0.4020] <= 0.75, upper end below judy's lower end: **True**
- confirm: (iii) kb/ share of non-counting top-5 hits 0.975 >= 0.5: **True**
- confirm: (iv) best of ACORN 1.0 0.8080 [0.7853, 0.8297] and tenant-m0 0.9519 [0.9439, 0.9596] >= 0.90: **True**
- falsify: category miss-rate spread 0.580 < 0.10: **False**
- falsify: gains of ACORN 1.0 and tenant-m0 (0.152, 0.296) both < 0.02: **False**

### Q2: falsified (ACORN's default gate engages unreliably)

- confirm: share of people ACORN 0.4 engaged for 1.000 in (0.05, 0.95): **False**
- confirm: ACORN 1.0 minus 0.4 in recall@10 0.0000 [0.0000, 0.0000] above 0: **False**
- falsify: |ACORN 1.0 minus 0.4| < 0.01 with an interval containing 0: **True**
- notes: engagement: telemetry (filtered_acorn among people whose searches took a graph path)

### Q3: inconclusive (recall varies by build and segment layout)

- confirm: recall@10 range between as-run builds 0.086 >= 0.01: **True**
- confirm: one-segment minus as-run -0.0302 [-0.0423, -0.0184] excludes 0: **True**
- falsify: range < 0.002 and |one-segment minus as-run| < 0.002: **False**
- notes: segments: as-run {'{"wardowl_enterprise": 1}'}, one-segment {'{"wardowl_enterprise": 1}'}; both layouts ended with the same segments

### Q4: inconclusive (hnsw_ef 128 was not the cause)

- confirm: hnsw_ef 512 minus 128 0.1025 [0.0895, 0.1158] < 0.05: **False**
- falsify: gain > 0.15: **False**

### P1: inconclusive (the iterative scan's budget runs out)

- confirm: (a) share of empties with r1 > 10090 (half the reach 20181) 0.799 >= 0.95: **False**
- confirm: (b) lowest ERR of a raised limit 0.000 <= 10% of pg-hnsw's 0.0892: **True**
- confirm: (c) median rows emitted on empties 20181.0 in [10000, 25000]: **True**
- falsify: ERR at 1M tuples and 16x memory 0.000 >= half of pg-hnsw's: **False**
- notes: reference pgvector/hnsw-m16-efc64/pg-hnsw; empty results under it: 393; ERR by raised limit: {"pa-t100k-m1": 0.07288828337874659, "pa-t20k-m8": 0.08923705722070845, "pa-t100k-m8": 0.0, "pa-t1000k-m1": 0.07288828337874659, "pa-t1000k-m8": 0.0, "pa-t1000k-m16": 0.0, "pb-wm64": 0.08923705722070845}; binding: no single-limit raise removed 90% of the empties

### P2: inconclusive (mis-retrieval from shallow, relaxed scans)

- confirm: (a) ef_search 1000 minus 100 0.0693 [0.0607, 0.0777] >= 0.02, above 0: **True**
- confirm: (b) inner LIMIT 10x minus 1x 0.0952 [0.0833, 0.1073] above 0: **True**
- confirm: (c) m32/efc200 minus m16/efc64 0.0663 [0.0550, 0.0778] above 0: **True**
- confirm: (d) loss at rho_100 < 0.1 0.368 at least twice the rest 0.188: **False**
- confirm: (e) mean similarity gap of missed questions 0.015 <= 0.02: **True**
- falsify: |ef_search 1000 minus 100| < 0.01 with an interval containing 0: **False**
- notes: reference pgvector/hnsw-m16-efc64/pg-hnsw

### P3: confirmed (the planner overestimates a judy filter)

- confirm: median planner estimate / R for judys 11.1 >= 5: **True**
- confirm: ph-exact ERR 0.000 == 0: **True**
- falsify: median ratio within [0.5, 2]: **False**

### P4: falsified (generic plans make no difference)

- confirm: pg-custom: |recall@10 difference| -0.3428 [-0.3742, -0.3121] < 0.005: **False**
- confirm: pg-custom: |ERR difference| 0.0890 [0.0552, 0.1253] < 0.002: **False**
- confirm: pg-noprepare: |recall@10 difference| -0.3428 [-0.3748, -0.3120] < 0.005: **False**
- confirm: pg-noprepare: |ERR difference| 0.0890 [0.0538, 0.1252] < 0.002: **False**
- confirm: generic plans run under p-asrun: 17556; fixed questions with another generic plan: 150 of 150: none run, or none differs: **False**
- falsify: pg-custom: |recall@10 difference| >= 0.01, interval excluding 0: **True**
- falsify: pg-custom: McNemar p for ERR 0.000 < 0.05: **True**
- falsify: pg-noprepare: |recall@10 difference| >= 0.01, interval excluding 0: **True**
- falsify: pg-noprepare: McNemar p for ERR 0.000 < 0.05: **True**
- falsify: generic plans run under p-asrun: 17556; fixed questions with another generic plan: 150 of 150: some run and some differ: **True**
- notes: generic plans of the search statement, summed over builds, per setting: {'p-asrun': 17556, 'pg-custom': 0, 'pg-noprepare': 0} (amendment 1)

### P5: confirmed (the plan cache decides whether pgvector searches the graph)

- confirm: (a) HNSW share under pg-custom 0.981 >= 0.9 and under p-asrun 0.009 <= 0.1: **True**
- confirm: (b) pg-custom recall@5 on the original questions 0.6796 [0.6632, 0.6970] within 0.08 of 0.691: **True**
- confirm: (c) p-asrun recall@5 on the original questions 0.9964 [0.9912, 1.0000] >= 0.99, and its median latency 361.6 ms at least 10x pg-custom's 22.4 ms on builds ['hnsw-m16-efc64-b0', 'hnsw-m16-efc64-b1', 'hnsw-m16-efc64-b2']: **True**
- falsify: pg-custom HNSW share 0.981 >= 0.9 with recall@5 0.6796 [0.6632, 0.6970] >= 0.95: **False**
- falsify: p-asrun HNSW share 0.009 >= 0.5: **False**
- notes: p-x0: recall@5 0.6970 [0.6765, 0.7172], HNSW share 0.981, generic plans 0, GIN pending pages before [388]; p-x0v: recall@5 0.9978 [0.9955, 0.9996], HNSW share 0.009, generic plans 2148, GIN pending pages before [0]

## Settings (means over builds; range between builds)

| store | layout | setting | builds | recall5 | recall10 | recall10_range | empty5 | short5 | gross_miss10 | sim_gap10 | latency_p50 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | hnsw-m16-efc64 | p-asrun | 3 | 0.997 | 0.999 | 0.001 | 0.000 | 0.000 | 0.001 | 0.000 | 403.2 |
| pgvector | hnsw-m16-efc64 | p-x0 | 1 | 0.697 | 0.729 | n/a | 0.006 | 0.010 | 0.244 | 0.010 | 6.992 |
| pgvector | hnsw-m16-efc64 | p-x0v | 1 | 0.998 | 0.998 | n/a | 0.000 | 0.000 | 0.004 | 0.000 | 335.3 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m1 | 3 | 0.645 | 0.683 | 0.006 | 0.073 | 0.085 | 0.297 | 0.009 | 25.9 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m16 | 3 | 0.737 | 0.780 | 0.006 | 0.000 | 0.000 | 0.199 | 0.007 | 24.6 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m8 | 3 | 0.737 | 0.780 | 0.006 | 0.000 | 0.000 | 0.199 | 0.007 | 24.4 |
| pgvector | hnsw-m16-efc64 | pa-t100k-m1 | 3 | 0.645 | 0.683 | 0.006 | 0.073 | 0.085 | 0.297 | 0.009 | 25.2 |
| pgvector | hnsw-m16-efc64 | pa-t100k-m8 | 3 | 0.737 | 0.779 | 0.006 | 0.000 | 0.000 | 0.200 | 0.007 | 24.1 |
| pgvector | hnsw-m16-efc64 | pa-t20k-m8 | 3 | 0.621 | 0.656 | 0.011 | 0.089 | 0.109 | 0.326 | 0.010 | 25.7 |
| pgvector | hnsw-m16-efc64 | pb-wm64 | 3 | 0.621 | 0.656 | 0.011 | 0.089 | 0.109 | 0.326 | 0.010 | 24.9 |
| pgvector | hnsw-m16-efc64 | pc-ef1000 | 3 | 0.704 | 0.725 | 0.013 | 0.086 | 0.106 | 0.272 | 0.007 | 31.7 |
| pgvector | hnsw-m16-efc64 | pc-ef200 | 3 | 0.634 | 0.667 | 0.018 | 0.089 | 0.108 | 0.315 | 0.009 | 24.7 |
| pgvector | hnsw-m16-efc64 | pc-ef40 | 3 | 0.596 | 0.634 | 0.014 | 0.089 | 0.109 | 0.340 | 0.011 | 24.5 |
| pgvector | hnsw-m16-efc64 | pc-ef400 | 3 | 0.667 | 0.693 | 0.010 | 0.088 | 0.108 | 0.296 | 0.008 | 26.5 |
| pgvector | hnsw-m16-efc64 | pd-lim10 | 3 | 0.732 | 0.751 | 0.005 | 0.089 | 0.109 | 0.257 | 0.006 | 30.2 |
| pgvector | hnsw-m16-efc64 | pd-lim4 | 3 | 0.698 | 0.724 | 0.016 | 0.089 | 0.109 | 0.278 | 0.006 | 27.0 |
| pgvector | hnsw-m16-efc64 | pe-strict | 3 | 0.477 | 0.497 | 0.009 | 0.090 | 0.109 | 0.542 | 0.019 | 25.2 |
| pgvector | hnsw-m16-efc64 | pg-custom | 3 | 0.621 | 0.656 | 0.011 | 0.089 | 0.109 | 0.326 | 0.010 | 22.8 |
| pgvector | hnsw-m16-efc64 | pg-hnsw | 3 | 0.621 | 0.656 | 0.011 | 0.089 | 0.109 | 0.326 | 0.010 | 24.3 |
| pgvector | hnsw-m16-efc64 | pg-noprepare | 3 | 0.621 | 0.656 | 0.011 | 0.089 | 0.109 | 0.326 | 0.010 | 22.2 |
| pgvector | hnsw-m16-efc64 | ph-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 329.9 |
| pgvector | hnsw-m32-efc200 | p-asrun | 3 | 0.999 | 1.000 | 0.000 | 0.001 | 0.001 | 0.000 | 0.000 | 415.7 |
| pgvector | hnsw-m32-efc200 | pa-t1000k-m8 | 3 | 0.833 | 0.866 | 0.010 | 0.000 | 0.000 | 0.127 | 0.003 | 32.8 |
| pgvector | hnsw-m32-efc200 | pc-ef400 | 3 | 0.720 | 0.744 | 0.005 | 0.094 | 0.116 | 0.254 | 0.005 | 33.9 |
| pgvector | hnsw-m32-efc200 | pd-lim10 | 3 | 0.768 | 0.786 | 0.008 | 0.097 | 0.116 | 0.222 | 0.004 | 43.8 |
| pgvector | hnsw-m32-efc200 | pg-custom | 3 | 0.698 | 0.722 | 0.006 | 0.097 | 0.116 | 0.270 | 0.005 | 33.4 |
| pgvector | hnsw-m32-efc200 | pg-hnsw | 3 | 0.698 | 0.722 | 0.006 | 0.097 | 0.116 | 0.270 | 0.005 | 36.0 |
| qdrant | as-run | q-asrun | 3 | 0.661 | 0.656 | 0.086 | 0.000 | 0.000 | 0.363 | 0.042 | 7.064 |
| qdrant | as-run | qa-acorn040 | 3 | 0.811 | 0.808 | 0.127 | 0.000 | 0.000 | 0.213 | 0.017 | 7.259 |
| qdrant | as-run | qa-acorn100 | 3 | 0.811 | 0.808 | 0.127 | 0.000 | 0.000 | 0.213 | 0.017 | 7.238 |
| qdrant | as-run | qb-ef512 | 3 | 0.759 | 0.758 | 0.120 | 0.000 | 0.000 | 0.272 | 0.031 | 11.3 |
| qdrant | as-run | qb-ef64 | 3 | 0.606 | 0.600 | 0.074 | 0.000 | 0.000 | 0.407 | 0.048 | 5.963 |
| qdrant | as-run | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 43.1 |
| qdrant | is-tenant | q-asrun | 3 | 0.659 | 0.651 | 0.025 | 0.000 | 0.000 | 0.363 | 0.044 | 6.907 |
| qdrant | is-tenant | qa-acorn040 | 3 | 0.806 | 0.802 | 0.076 | 0.000 | 0.000 | 0.205 | 0.019 | 7.093 |
| qdrant | is-tenant | qa-acorn100 | 3 | 0.806 | 0.802 | 0.076 | 0.000 | 0.000 | 0.205 | 0.019 | 7.109 |
| qdrant | is-tenant | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 39.2 |
| qdrant | one-segment | q-asrun | 3 | 0.631 | 0.625 | 0.029 | 0.000 | 0.000 | 0.395 | 0.046 | 7.037 |
| qdrant | one-segment | qa-acorn040 | 3 | 0.780 | 0.777 | 0.027 | 0.000 | 0.000 | 0.250 | 0.020 | 7.178 |
| qdrant | one-segment | qa-acorn100 | 3 | 0.780 | 0.777 | 0.027 | 0.000 | 0.000 | 0.250 | 0.020 | 7.170 |
| qdrant | one-segment | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 41.5 |
| qdrant | separate-kb | q-asrun | 3 | 0.954 | 0.949 | 0.003 | 0.000 | 0.000 | 0.043 | 0.001 | 12.9 |
| qdrant | separate-kb | qa-acorn040 | 3 | 0.954 | 0.949 | 0.003 | 0.000 | 0.000 | 0.043 | 0.001 | 12.8 |
| qdrant | separate-kb | qa-acorn100 | 3 | 0.954 | 0.949 | 0.003 | 0.000 | 0.000 | 0.043 | 0.001 | 12.8 |
| qdrant | separate-kb | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 45.0 |
| qdrant | tenant-m0 | q-asrun | 3 | 0.950 | 0.952 | 0.001 | 0.000 | 0.000 | 0.077 | 0.002 | 6.580 |
| qdrant | tenant-m0 | qa-acorn040 | 3 | 0.950 | 0.952 | 0.001 | 0.000 | 0.000 | 0.077 | 0.002 | 6.612 |
| qdrant | tenant-m0 | qa-acorn100 | 3 | 0.950 | 0.952 | 0.001 | 0.000 | 0.000 | 0.077 | 0.002 | 6.587 |
| qdrant | tenant-m0 | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 38.3 |

## pgvector: the plans the searches executed (auto_explain, first pass; amendment 2)

A setting meant to search the HNSW graph with an HNSW share below 0.5 ran mostly exact and is left out of P1 and P2: ['pgvector/hnsw-m16-efc64/p-asrun', 'pgvector/hnsw-m16-efc64/p-x0v', 'pgvector/hnsw-m32-efc200/p-asrun'].

| layout | setting | captured | hnsw_share | gin_share | generic_share |
|---|---|---|---|---|---|
| hnsw-m16-efc64 | p-asrun | 8934 | 0.007 | 0.993 | 0.979 |
| hnsw-m16-efc64 | p-x0 | 1105 | 0.981 | 0.019 | 0.000 |
| hnsw-m16-efc64 | p-x0v | 2210 | 0.009 | 0.991 | 0.972 |
| hnsw-m16-efc64 | pa-t1000k-m1 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pa-t1000k-m16 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pa-t1000k-m8 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pa-t100k-m1 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pa-t100k-m8 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pa-t20k-m8 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pb-wm64 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pc-ef1000 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pc-ef200 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pc-ef40 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pc-ef400 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pd-lim10 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pd-lim4 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pe-strict | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pg-custom | 8934 | 0.986 | 0.014 | 0.000 |
| hnsw-m16-efc64 | pg-hnsw | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pg-noprepare | 8934 | 0.986 | 0.014 | 0.000 |
| hnsw-m16-efc64 | ph-exact | 2978 | 0.000 | 1.000 | 0.979 |
| hnsw-m32-efc200 | p-asrun | 8934 | 0.007 | 0.993 | 0.979 |
| hnsw-m32-efc200 | pa-t1000k-m8 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m32-efc200 | pc-ef400 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m32-efc200 | pd-lim10 | 8934 | 1.000 | 0.000 | 0.000 |
| hnsw-m32-efc200 | pg-custom | 8934 | 0.986 | 0.014 | 0.000 |
| hnsw-m32-efc200 | pg-hnsw | 8934 | 1.000 | 0.000 | 0.000 |

Qdrant search paths were read from the telemetry path `result/collections/collections/shards/local/segments/vector_index_searches`.
