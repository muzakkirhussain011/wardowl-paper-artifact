# X1: under-retrieval under permission filters, statistics

Input: `/kaggle/working/smoke/a`, `/kaggle/working/smoke/b`, `/kaggle/working/smoke/c` (grid run2); 11,195 result rows of 49 settings; 200 bootstrap resamples, seed 20261026. Verdicts follow PREREGISTRATION.md, with amendment 2: P1 and P2 read `pg-hnsw` where they say `p-asrun`.

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

- confirm: pg-hnsw reproduces empty results: **False**
- notes: no empty result under pg-hnsw

### P2: confirmed (mis-retrieval from shallow, relaxed scans)

- confirm: (a) ef_search 1000 minus 100 0.0382 [0.0177, 0.0534] >= 0.02, above 0: **True**
- confirm: (b) inner LIMIT 10x minus 1x 0.0348 [0.0182, 0.0493] above 0: **True**
- confirm: (c) m32/efc200 minus m16/efc64 0.0236 [0.0111, 0.0343] above 0: **True**
- confirm: (d) loss at rho_100 < 0.1 0.046 at least twice the rest 0.014: **True**
- confirm: (e) mean similarity gap of missed questions 0.002 <= 0.02: **True**
- falsify: |ef_search 1000 minus 100| < 0.01 with an interval containing 0: **False**
- notes: reference pgvector/hnsw-m16-efc64/pg-hnsw

### P3: confirmed (the planner overestimates a judy filter)

- confirm: median planner estimate / R for judys 13.4 >= 5: **True**
- confirm: ph-exact ERR 0.000 == 0: **True**
- falsify: median ratio within [0.5, 2]: **False**

### P4: falsified (generic plans make no difference)

- confirm: pg-custom: |recall@10 difference| -0.0361 [-0.0511, -0.0163] < 0.005: **False**
- confirm: pg-custom: |ERR difference| 0.0000 [0.0000, 0.0000] < 0.002: **True**
- confirm: pg-noprepare: |recall@10 difference| -0.0361 [-0.0532, -0.0185] < 0.005: **False**
- confirm: pg-noprepare: |ERR difference| 0.0000 [0.0000, 0.0000] < 0.002: **True**
- confirm: generic plans run under p-asrun: 868; fixed questions with another generic plan: 12 of 20: none run, or none differs: **False**
- falsify: pg-custom: |recall@10 difference| >= 0.01, interval excluding 0: **True**
- falsify: pg-custom: McNemar p for ERR 1.000 < 0.05: **False**
- falsify: pg-noprepare: |recall@10 difference| >= 0.01, interval excluding 0: **True**
- falsify: pg-noprepare: McNemar p for ERR 1.000 < 0.05: **False**
- falsify: generic plans run under p-asrun: 868; fixed questions with another generic plan: 12 of 20: some run and some differ: **True**
- notes: generic plans of the search statement, summed over builds, per setting: {'p-asrun': 868, 'pg-custom': 0, 'pg-noprepare': 0} (amendment 1)

### P5: inconclusive (the plan cache decides whether pgvector searches the graph)

- confirm: (a) HNSW share under pg-custom 0.657 >= 0.9 and under p-asrun 0.048 <= 0.1: **False**
- confirm: (b) pg-custom recall@5 on the original questions 0.9512 [0.9294, 0.9896] within 0.08 of 0.691: **False**
- confirm: (c) p-asrun recall@5 on the original questions 0.9976 [0.9939, 1.0000] >= 0.99, and its median latency 19.7 ms at least 10x pg-custom's 6.641 ms on builds ['hnsw-m16-efc64-b0', 'hnsw-m16-efc64-b1']: **False**
- falsify: pg-custom HNSW share 0.657 >= 0.9 with recall@5 0.9512 [0.9294, 0.9896] >= 0.95: **False**
- falsify: p-asrun HNSW share 0.048 >= 0.5: **False**
- notes: p-x0: recall@5 0.9548 [0.9333, 1.0000], HNSW share 0.657, generic plans 12, GIN pending pages before [152]; p-x0v: recall@5 0.9976 [0.9939, 1.0000], HNSW share 0.038, generic plans 156, GIN pending pages before [0]

## Settings (means over builds; range between builds)

| store | layout | setting | builds | recall5 | recall10 | recall10_range | empty5 | short5 | gross_miss10 | sim_gap10 | latency_p50 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | hnsw-m16-efc64 | p-asrun | 2 | 0.999 | 0.998 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 21.0 |
| pgvector | hnsw-m16-efc64 | p-x0 | 1 | 0.955 | 0.960 | n/a | 0.000 | 0.000 | 0.012 | 0.001 | 5.727 |
| pgvector | hnsw-m16-efc64 | p-x0v | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 19.4 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m1 | 2 | 0.952 | 0.962 | 0.001 | 0.000 | 0.000 | 0.007 | 0.000 | 9.616 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m16 | 2 | 0.952 | 0.962 | 0.001 | 0.000 | 0.000 | 0.007 | 0.000 | 8.783 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m8 | 2 | 0.952 | 0.962 | 0.001 | 0.000 | 0.000 | 0.007 | 0.000 | 8.913 |
| pgvector | hnsw-m16-efc64 | pa-t100k-m1 | 2 | 0.952 | 0.962 | 0.001 | 0.000 | 0.000 | 0.007 | 0.000 | 9.775 |
| pgvector | hnsw-m16-efc64 | pa-t100k-m8 | 2 | 0.952 | 0.962 | 0.001 | 0.000 | 0.000 | 0.007 | 0.000 | 9.331 |
| pgvector | hnsw-m16-efc64 | pa-t20k-m8 | 2 | 0.952 | 0.962 | 0.001 | 0.000 | 0.000 | 0.007 | 0.000 | 9.355 |
| pgvector | hnsw-m16-efc64 | pb-wm64 | 2 | 0.952 | 0.962 | 0.001 | 0.000 | 0.000 | 0.007 | 0.000 | 8.341 |
| pgvector | hnsw-m16-efc64 | pc-ef1000 | 2 | 1.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | -0.000 | 14.2 |
| pgvector | hnsw-m16-efc64 | pc-ef200 | 2 | 0.973 | 0.970 | 0.000 | 0.000 | 0.000 | 0.007 | 0.000 | 9.427 |
| pgvector | hnsw-m16-efc64 | pc-ef40 | 2 | 0.919 | 0.936 | 0.004 | 0.000 | 0.000 | 0.010 | 0.001 | 7.380 |
| pgvector | hnsw-m16-efc64 | pc-ef400 | 2 | 0.995 | 0.989 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 9.875 |
| pgvector | hnsw-m16-efc64 | pd-lim10 | 2 | 0.993 | 0.997 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 12.0 |
| pgvector | hnsw-m16-efc64 | pd-lim4 | 2 | 0.984 | 0.989 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 9.349 |
| pgvector | hnsw-m16-efc64 | pe-strict | 2 | 0.870 | 0.860 | 0.007 | 0.000 | 0.000 | 0.135 | 0.003 | 8.443 |
| pgvector | hnsw-m16-efc64 | pg-custom | 2 | 0.953 | 0.962 | 0.001 | 0.000 | 0.000 | 0.007 | 0.000 | 6.816 |
| pgvector | hnsw-m16-efc64 | pg-hnsw | 2 | 0.952 | 0.962 | 0.001 | 0.000 | 0.000 | 0.007 | 0.000 | 8.358 |
| pgvector | hnsw-m16-efc64 | pg-noprepare | 2 | 0.953 | 0.962 | 0.001 | 0.000 | 0.000 | 0.007 | 0.000 | 6.467 |
| pgvector | hnsw-m16-efc64 | ph-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 24.0 |
| pgvector | hnsw-m32-efc200 | p-asrun | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 19.7 |
| pgvector | hnsw-m32-efc200 | pa-t1000k-m8 | 1 | 0.980 | 0.985 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 8.388 |
| pgvector | hnsw-m32-efc200 | pc-ef400 | 1 | 1.000 | 0.999 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 10.1 |
| pgvector | hnsw-m32-efc200 | pd-lim10 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 10.7 |
| pgvector | hnsw-m32-efc200 | pg-custom | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 19.6 |
| pgvector | hnsw-m32-efc200 | pg-hnsw | 1 | 0.980 | 0.985 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 7.865 |
| qdrant | as-run | q-asrun | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.384 |
| qdrant | as-run | qa-acorn040 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.564 |
| qdrant | as-run | qa-acorn100 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.448 |
| qdrant | as-run | qb-ef512 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.695 |
| qdrant | as-run | qb-ef64 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.810 |
| qdrant | as-run | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.707 |
| qdrant | is-tenant | q-asrun | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.589 |
| qdrant | is-tenant | qa-acorn040 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.704 |
| qdrant | is-tenant | qa-acorn100 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.959 |
| qdrant | is-tenant | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.706 |
| qdrant | one-segment | q-asrun | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.838 |
| qdrant | one-segment | qa-acorn040 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.983 |
| qdrant | one-segment | qa-acorn100 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.829 |
| qdrant | one-segment | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.756 |
| qdrant | separate-kb | q-asrun | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 10.0 |
| qdrant | separate-kb | qa-acorn040 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 9.869 |
| qdrant | separate-kb | qa-acorn100 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 9.822 |
| qdrant | separate-kb | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 9.906 |
| qdrant | tenant-m0 | q-asrun | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.396 |
| qdrant | tenant-m0 | qa-acorn040 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.361 |
| qdrant | tenant-m0 | qa-acorn100 | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.454 |
| qdrant | tenant-m0 | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | -0.000 | 5.739 |

## pgvector: the plans the searches executed (auto_explain, first pass; amendment 2)

A setting meant to search the HNSW graph with an HNSW share below 0.5 ran mostly exact and is left out of P1 and P2: ['pgvector/hnsw-m16-efc64/p-asrun', 'pgvector/hnsw-m16-efc64/p-x0v', 'pgvector/hnsw-m32-efc200/p-asrun', 'pgvector/hnsw-m32-efc200/pg-custom'].

| layout | setting | captured | hnsw_share | gin_share | generic_share |
|---|---|---|---|---|---|
| hnsw-m16-efc64 | p-asrun | 676 | 0.030 | 0.970 | 0.846 |
| hnsw-m16-efc64 | p-x0 | 105 | 0.657 | 0.000 | 0.114 |
| hnsw-m16-efc64 | p-x0v | 210 | 0.038 | 0.962 | 0.743 |
| hnsw-m16-efc64 | pa-t1000k-m1 | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pa-t1000k-m16 | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pa-t1000k-m8 | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pa-t100k-m1 | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pa-t100k-m8 | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pa-t20k-m8 | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pb-wm64 | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pc-ef1000 | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pc-ef200 | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pc-ef40 | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pc-ef400 | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pd-lim10 | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pd-lim4 | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pe-strict | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pg-custom | 676 | 0.598 | 0.402 | 0.000 |
| hnsw-m16-efc64 | pg-hnsw | 676 | 1.000 | 0.000 | 0.000 |
| hnsw-m16-efc64 | pg-noprepare | 676 | 0.598 | 0.402 | 0.000 |
| hnsw-m16-efc64 | ph-exact | 338 | 0.000 | 0.970 | 0.846 |
| hnsw-m32-efc200 | p-asrun | 338 | 0.000 | 0.970 | 0.846 |
| hnsw-m32-efc200 | pa-t1000k-m8 | 338 | 1.000 | 0.000 | 0.000 |
| hnsw-m32-efc200 | pc-ef400 | 338 | 1.000 | 0.000 | 0.000 |
| hnsw-m32-efc200 | pd-lim10 | 338 | 1.000 | 0.000 | 0.000 |
| hnsw-m32-efc200 | pg-custom | 338 | 0.000 | 0.402 | 0.000 |
| hnsw-m32-efc200 | pg-hnsw | 338 | 1.000 | 0.000 | 0.000 |

Qdrant search paths were read from the telemetry path `result/collections/collections/shards/local/segments/vector_index_searches`.
