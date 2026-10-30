# X1: under-retrieval under permission filters, statistics

Input: `/kaggle/working/x1`; 99,763 result rows of 33 settings; 10,000 bootstrap resamples, seed 20261026. Verdicts follow PREREGISTRATION.md.

## Verdicts

### Q1: confirmed (islanded permitted subgraph in Qdrant)

- confirm: (i) judy recall@10 1.0000 [1.0000, 1.0000] >= 0.95: **True**
- confirm: (ii) company-document recall@10 0.2734 [0.2417, 0.3051] <= 0.75, upper end below judy's lower end: **True**
- confirm: (iii) kb/ share of non-counting top-5 hits 0.986 >= 0.5: **True**
- confirm: (iv) best of ACORN 1.0 0.7607 [0.7327, 0.7873] and tenant-m0 0.9427 [0.9333, 0.9519] >= 0.90: **True**
- falsify: category miss-rate spread 0.669 < 0.10: **False**
- falsify: gains of ACORN 1.0 and tenant-m0 (0.142, 0.324) both < 0.02: **False**

### Q2: falsified (ACORN's default gate engages unreliably)

- confirm: share of people ACORN 0.4 engaged for 1.000 in (0.05, 0.95): **False**
- confirm: ACORN 1.0 minus 0.4 in recall@10 0.0000 [0.0000, 0.0000] above 0: **False**
- falsify: |ACORN 1.0 minus 0.4| < 0.01 with an interval containing 0: **True**
- notes: engagement: telemetry (filtered_acorn among people whose searches took a graph path)

### Q3: inconclusive (recall varies by build and segment layout)

- confirm: recall@10 range between as-run builds 0.062 >= 0.01: **True**
- confirm: one-segment minus as-run 0.0121 [0.0012, 0.0228] excludes 0: **True**
- falsify: range < 0.002 and |one-segment minus as-run| < 0.002: **False**
- notes: segments: as-run {'{"wardowl_enterprise": 2}'}, one-segment {'{"wardowl_enterprise": 2}'}; both layouts ended with the same segments

### Q4: inconclusive (hnsw_ef 128 was not the cause)

- confirm: hnsw_ef 512 minus 128 0.0901 [0.0784, 0.1023] < 0.05: **False**
- falsify: gain > 0.15: **False**

### P1: confirmed (the iterative scan's budget runs out)

- confirm: (a) share of empties with r1 > 10042 (half the reach 20083) 1.000 >= 0.95: **True**
- confirm: (b) lowest ERR of a raised limit 0.000 <= 10% of p-asrun's 0.0007: **True**
- confirm: (c) median rows emitted on empties 20083.0 in [10000, 25000]: **True**
- falsify: ERR at 1M tuples and 16x memory 0.000 >= half of p-asrun's: **False**
- notes: ERR by raised limit: {"pa-t100k-m1": 0.0, "pa-t20k-m8": 0.0006811989100817438, "pa-t100k-m8": 0.0, "pa-t1000k-m1": 0.0, "pa-t1000k-m8": 0.0, "pa-t1000k-m16": 0.0, "pb-wm64": 0.0006811989100817438}; binding: hnsw.max_scan_tuples

### P2: inconclusive (mis-retrieval from shallow, relaxed scans)

- confirm: (a) ef_search 1000 minus 100 missing >= 0.02, above 0: **None**
- confirm: (b) inner LIMIT 10x minus 1x missing above 0: **None**
- confirm: (c) m32/efc200 minus m16/efc64 missing above 0: **None**
- confirm: (d) loss at rho_100 < 0.1 0.001 at least twice the rest 0.001: **False**
- confirm: (e) mean similarity gap of missed questions 0.008 <= 0.02: **True**
- falsify: |ef_search 1000 minus 100| < 0.01 with an interval containing 0: **None**

### P3: inconclusive (the planner overestimates a judy filter)

- confirm: median planner estimate / R for judys 11.1 >= 5: **True**
- confirm: ph-exact ERR n/a == 0: **None**
- falsify: median ratio within [0.5, 2]: **False**

### P4: falsified (generic plans make no difference)

- confirm: pg-custom: |recall@10 difference| missing < 0.005: **None**
- confirm: pg-custom: |ERR difference| missing < 0.002: **None**
- confirm: pg-noprepare: |recall@10 difference| missing < 0.005: **None**
- confirm: pg-noprepare: |ERR difference| missing < 0.002: **None**
- confirm: generic plans run under p-asrun: 5852; fixed questions with another generic plan: 50 of 50: none run, or none differs: **False**
- falsify: pg-custom: |recall@10 difference| >= 0.01, interval excluding 0: **None**
- falsify: pg-custom: McNemar p for ERR n/a < 0.05: **None**
- falsify: pg-noprepare: |recall@10 difference| >= 0.01, interval excluding 0: **None**
- falsify: pg-noprepare: McNemar p for ERR n/a < 0.05: **None**
- falsify: generic plans run under p-asrun: 5852; fixed questions with another generic plan: 50 of 50: some run and some differ: **True**
- notes: generic plans of the search statement, summed over builds, per setting: {'p-asrun': 5852} (amendment 1)

## Settings (means over builds; range between builds)

| store | layout | setting | builds | recall5 | recall10 | recall10_range | empty5 | short5 | gross_miss10 | sim_gap10 | latency_p50 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pgvector | hnsw-m16-efc64 | p-asrun | 1 | 0.998 | 0.999 | n/a | 0.001 | 0.001 | 0.001 | 0.000 | 391.1 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m1 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.001 | 0.001 | 0.000 | 378.0 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m16 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 390.4 |
| pgvector | hnsw-m16-efc64 | pa-t1000k-m8 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 377.7 |
| pgvector | hnsw-m16-efc64 | pa-t100k-m1 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.001 | 0.001 | 0.000 | 390.7 |
| pgvector | hnsw-m16-efc64 | pa-t100k-m8 | 1 | 0.998 | 0.999 | n/a | 0.000 | 0.000 | 0.001 | 0.000 | 380.6 |
| pgvector | hnsw-m16-efc64 | pa-t20k-m8 | 1 | 0.998 | 0.999 | n/a | 0.001 | 0.001 | 0.001 | 0.000 | 391.0 |
| pgvector | hnsw-m16-efc64 | pb-wm64 | 1 | 0.998 | 0.999 | n/a | 0.001 | 0.001 | 0.001 | 0.000 | 388.3 |
| pgvector | hnsw-m16-efc64 | pc-ef200 | 1 | 0.998 | 0.999 | n/a | 0.001 | 0.001 | 0.000 | 0.000 | 390.2 |
| pgvector | hnsw-m16-efc64 | pc-ef40 | 1 | 0.998 | 0.999 | n/a | 0.001 | 0.001 | 0.001 | 0.000 | 392.8 |
| pgvector | hnsw-m16-efc64 | pc-ef400 | 1 | 0.999 | 0.999 | n/a | 0.001 | 0.001 | 0.000 | 0.000 | 393.8 |
| qdrant | as-run | q-asrun | 3 | 0.624 | 0.619 | 0.062 | 0.000 | 0.006 | 0.407 | 0.049 | 4.456 |
| qdrant | as-run | qa-acorn040 | 3 | 0.764 | 0.761 | 0.151 | 0.000 | 0.006 | 0.269 | 0.025 | 4.809 |
| qdrant | as-run | qa-acorn100 | 3 | 0.764 | 0.761 | 0.151 | 0.000 | 0.006 | 0.269 | 0.025 | 4.923 |
| qdrant | as-run | qb-ef512 | 3 | 0.711 | 0.709 | 0.101 | 0.000 | 0.006 | 0.324 | 0.039 | 7.732 |
| qdrant | as-run | qb-ef64 | 3 | 0.578 | 0.571 | 0.049 | 0.000 | 0.006 | 0.442 | 0.053 | 3.943 |
| qdrant | as-run | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 35.4 |
| qdrant | is-tenant | q-asrun | 3 | 0.662 | 0.656 | 0.031 | 0.000 | 0.000 | 0.362 | 0.042 | 4.295 |
| qdrant | is-tenant | qa-acorn040 | 3 | 0.832 | 0.830 | 0.038 | 0.000 | 0.000 | 0.194 | 0.014 | 4.473 |
| qdrant | is-tenant | qa-acorn100 | 3 | 0.832 | 0.830 | 0.038 | 0.000 | 0.000 | 0.194 | 0.014 | 4.544 |
| qdrant | is-tenant | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 32.2 |
| qdrant | one-segment | q-asrun | 3 | 0.638 | 0.631 | 0.116 | 0.000 | 0.011 | 0.389 | 0.046 | 4.348 |
| qdrant | one-segment | qa-acorn040 | 3 | 0.809 | 0.806 | 0.113 | 0.000 | 0.000 | 0.220 | 0.017 | 4.577 |
| qdrant | one-segment | qa-acorn100 | 3 | 0.809 | 0.806 | 0.113 | 0.000 | 0.000 | 0.220 | 0.017 | 4.623 |
| qdrant | one-segment | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 35.2 |
| qdrant | separate-kb | q-asrun | 3 | 0.951 | 0.948 | 0.004 | 0.000 | 0.000 | 0.037 | 0.001 | 8.172 |
| qdrant | separate-kb | qa-acorn040 | 3 | 0.951 | 0.948 | 0.004 | 0.000 | 0.000 | 0.037 | 0.001 | 8.095 |
| qdrant | separate-kb | qa-acorn100 | 3 | 0.951 | 0.948 | 0.004 | 0.000 | 0.000 | 0.037 | 0.001 | 8.207 |
| qdrant | separate-kb | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 37.6 |
| qdrant | tenant-m0 | q-asrun | 3 | 0.940 | 0.943 | 0.009 | 0.000 | 0.000 | 0.085 | 0.002 | 3.828 |
| qdrant | tenant-m0 | qa-acorn040 | 3 | 0.940 | 0.943 | 0.009 | 0.000 | 0.000 | 0.085 | 0.002 | 3.862 |
| qdrant | tenant-m0 | qa-acorn100 | 3 | 0.940 | 0.943 | 0.009 | 0.000 | 0.000 | 0.085 | 0.002 | 3.789 |
| qdrant | tenant-m0 | qc-exact | 1 | 1.000 | 1.000 | n/a | 0.000 | 0.000 | 0.000 | 0.000 | 31.6 |

Qdrant search paths were read from the telemetry path `result/collections/collections/shards/local/segments/vector_index_searches`.
