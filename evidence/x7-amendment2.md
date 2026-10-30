# Evidence: X7 amendment 2, the targeted rerun of the library fixes

Written 2026-10-30. GitHub Actions run 40969846593 (attempt 1), branch `paper/x4-x7` at
`41292bd2aa21814b025fbac31a1be94cf8744855`, configuration `amendment2`, wardowl from
`fix/revocation-faults` at `3c6559f3ecfd850bcd59416f14237d85887ba498` (PR #186). Pre-registration:
amendment 2 in `benchmarks/paper/PREREG_X4_X7.md` (commit `618b108`, before the harness `32af4b7`, the
smoke run 40952219346 and this run). Results: branch `results/x4-x7`, directory `40969846593-1/`
(`x7_report.md`, `x7a_revocation.csv`, `x7b_faults.csv`, raw JSON lines per job). Five experiment jobs:
x7a-cerbos, x7a-spicedb, x7b-pgvector, x7b-qdrant, x7b-spicedb (the run lists eight with `plan`,
`report` and a skipped `matrix.job`; `evidence/compute.md`); 480 records; 140 fault episodes,
none excluded by guard G4.

## Verdicts as printed (every one CONFIRMED)

| Hypothesis | Numbers |
|---|---|
| A2-H1 revocation within D + 1 s (D + 2 s shared) after invalidate() | SpiceDB minimizeLatency (D = 11): 40/40 and 40/40 within; Cerbos (D = 10): 40/40 and 40/40 within |
| A2-H2 medians | SpiceDB ttl30-inv 4.774 s [4.708, 4.839] (limit 6.0; run 1: 30.042, max 38.419); shared 4.767 [4.684, 4.827] (limit 7.0; run 1: 31.048). Cerbos ttl30-inv 3.884 [3.879, 3.891] (limit 4.0; run 1: 30.025); shared 3.887 [3.876, 3.900] (limit 5.0; run 1: 31.039) |
| A2-H3 without cache, ttl5, ttl30 within their bounds | SpiceDB nocache 40/40 (median 4.732, max 5.212); ttl5 40/40 (median 5.040); ttl30 40/40 (median 30.017); Cerbos nocache 40/40 (median 3.881) |
| X7-H2, X7-H5 replication | SpiceDB staleness median 4.732 [4.627, 4.799], max 5.212; ttl5 median 5.040 in [4.0, 11.5]; ttl30 30.017 in [29.0, 36.5] |
| A2-H4 pgvector blackhole | plain and stmt-timeout: failing or hanging 1.000 over 340 requests each; median 5.000 s |
| A2-H5 pgvector table lock | stmt-timeout: failing 1.000 over 540 requests, 0 hangs, median 1.003 s; plain: 80 hangs, median 5.000 s |
| A2-H6 SpiceDB empty | `empty`: failing 1.000, deviating 0.000 over 3,520 requests (run 1: 4,746 deviating answers); `empty-lookup`: exact 1.000 over 3,180 |
| A2-H7 store errors | 6,066 failures, all `SearchError` with the fixed message, 0 naming a host, 0 leaks |
| A2-H8 fail closed | 10,303 requests, 0 leaks (one-sided 95% bound 2.91e-4), 0 failures other than the layer's errors, 0 naming a host |

## Notes

- SpiceDB still flapped (a revoked chunk reappearing after it had gone): 19 polls without cache, 28
  with ttl30 and invalidation, 16 on the shared replica. This is the engine serving different
  quantized revisions; the cache no longer extends it.
- SpiceDB's staleness stayed within its documented 5.5 s in this run (max 5.212 s); run 1 measured
  up to 8.742 s, which motivated the 11 s declaration.
- Cerbos's policy reload took a median 3.88 s here against 2.55 s in run 1, within the declared 10 s.
- The blackhole case is not bounded by any per-statement setting; the library has no deadline for
  a whole retrieval (follow-up listed in PR #186).
