# Evidence: X3 (filter-size scaling) and X6 (side channels), GitHub Actions run 1

Source: repository `muzakkirhussain011/wardowl`, workflow `paper-x3-x6`
(`.github/workflows/paper-x3-x6.yml`), run id 40940385704, attempt 1
(https://github.com/muzakkirhussain011/wardowl/actions/runs/40940385704), commit
`a1916263f118f92a3446e6b98ec812549e82261a` on branch `paper/x3-x6` ("bench: run X3 and X6 at the
pre-registered full size"), mode `full`, 5 seeds. Read on 2026-10-30 with git only, from branch
`results/x3-x6` at commit `5da5a0c` ("results: paper-x3-x6 run 40940385704, attempt 1 (full)",
published 2026-10-29T22:48:18Z), directory `40940385704-1/`: `index.txt`, `jobs.json`,
`crashes.jsonl`, `reports/` (`x3_report.md`, `x6_report.md` and their CSVs) and `logs/` (the last
lines of every job's log, the data job's manifest, the two statistics logs). Nothing was recomputed;
every number below is as `x3_stats.py` and `x6_stats.py` printed it, or read from a log, except where
a line says "derived" (simple arithmetic on printed numbers, shown in full).

Pre-registration: `benchmarks/paper/PREREG_X3_X6.md` on `paper/x3-x6`, committed alone at `5da58ee`
(2026-10-29 18:50 +0300) before any harness code; amendment 1 at `f0acc15`, amendments 2 and the X3
part of 3 at `c369a80`, amendment 3 at `3b7ba31`, all before the full run. Several smoke runs
(among them 40918774649 and 40937668791) preceded the full run and are not analysed.

The raw records (`x3-*.jsonl`, `x6-*.jsonl`, 1.1 MB per X3 store, 61 to 134 MB per X6 store) are in
the run's artifacts `x3x6-results-*` only, which need an authenticated download; they were not read.
Several checks below are marked "needs the raw records" for that reason.

## Setup

wardowl 2.1.0 (the package as on `paper/x3-x6`), Python 3.12.15, numpy 2.5.4,
sentence-transformers 5.0.0, torch 2.8.0+cpu, transformers 4.57.6, `ubuntu24` runner image
20261026.354.1 (Linux 7.0.0-1017-azure, 4 CPUs, 15.6 GiB). Embedding model
`sentence-transformers/all-MiniLM-L6-v2` at revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`,
`max_seq_length` 256, from the cache (`from_cache: true`; the original embedding took 2,593.5 s).
FiQA 57,638 passages and 6,648 queries, SciDocs subset 12,000; FiQA tokens per passage mean 138.5,
median 95. Client and server versions as pre-registered (chromadb 1.5.9, lancedb 0.40.0, faiss-cpu
1.15.1, psycopg 3.3.6 seen in the setup logs).

Jobs: `data`, `run` (12 matrix jobs: 5 X6 jobs, one per store, and 7 X3 jobs), `summary` (statistics)
and `publish to results/x3-x6`, 15 jobs in the jobs API (`evidence/compute.md`; corrected 2026-10-30,
this line counted publishing inside `summary`). `jobs.json`: data, run and summary all `success`. The X6 jobs ran from
about 19:30 to 20:50 (runner time); X3 from 19:30 to 21:50; statistics 22:26 to 22:33.

## X6: what ran

Every pre-registered cell ran. Five seeds for every store, no store skipped, no retrieval error, no
seed stopped, **no leak** (health table: leaks 0 for every store).

| store | retrievals | build s (W1 / SEP / W0) |
|---|---|---|
| elasticsearch | 181,440 | 26.7 / 22.1 / 26.0 |
| faiss | 77,760 | 0.6 / 0.5 / 0.6 |
| memory | 1,920 | 0.4 / 0.3 / 0.4 |
| pgvector | 129,600 | 23.7 / 19.9 / 23.4 |
| qdrant | 129,600 | 57.6 / 48.3 / 57.8 |

Total 520,320 retrievals (derived: the sum of the column), 520,970 records. Per-seed durations: ES
11.0 to 11.4 min, FAISS 14.1 to 14.3, memory 10.6 to 12.0, pgvector 11.2 to 12.2, Qdrant 15.6 to
16.1. The in-memory control ran its pre-registered reduced design (first 3 probes of each level,
p = 10% only, `pre` and `post`, 3 timed repetitions): 60 clusters pooled, 15 per level.

Plans (data manifest), per seed 0 to 4:

| seed | probes (1000/100/10/1) | groups full | placements per group | secrets | extra group memberships | far eligible | far reused | boundary | rank of the m-th near passage, max (m = 1000 / 100 / 10 / 1) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 8/16/24/24 | 8 | 1,2,2,2,2,2,2,2 | 8,194 | 1,670 | 9,002 | no | 0.2015 | 1,149 / 123 / 10 / 2 |
| 1 | 8/16/24/24 | 8 | 1,1,1,1,1,2,1,1 | 8,510 | 1,354 | 4,491 | **yes** | 0.1416 | 1,085 / 159 / 12 / 1 |
| 2 | 8/16/24/24 | 8 | 1,1,1,1,1,1,2,2 | 8,417 | 1,447 | 2,331 | **yes** | 0.1135 | 1,145 / 152 / 16 / 2 |
| 3 | 8/16/24/24 | 8 | 1,1,1,2,1,1,1,1 | 6,999 | 2,865 | 7,754 | no | 0.1737 | 1,271 / 120 / 11 / 1 |
| 4 | 8/16/24/24 | 8 | 1,1,1,1,1,1,1,1 | 8,985 | 879 | 4,864 | **yes** | 0.1430 | 1,040 / 125 / 15 / 5 |

All 72 probes were placed in every seed (no shortfall). Secrets plus extra memberships equal 9,864 in
every seed (derived: 8,194 + 1,670, and so on), that is 8 groups of exactly 1,233 secrets
(1,000 + 2 x 100 + 3 x 10 + 3 x 1). Hubs: 576 passages; a hub is among the 2,000 nearest passages of
at least 901 queries (threshold), at most 2,052, median count 179, expected under uniformity 230.7.

## X6 guards

**G2 passed** for all four stores: `pre-exact` (pgvector, Qdrant, Elasticsearch) and FAISS `pre`
change rate 0.0000 (identical hit lists in W1 and W0 for every probe and p, 1,080 pairs each). A/A
change rate 0.000 everywhere.

**G1 passed for every configuration of the four vector stores** (360 clusters, 5 seeds each): ES
bm25-pre 0.491 [0.462, 0.521], hybrid-exact 0.463 [0.436, 0.492], hybrid-pre 0.513 [0.481, 0.544],
post 0.499 [0.467, 0.530], post-const 0.513 [0.483, 0.542], pre 0.500 [0.470, 0.530], pre-exact 0.507
[0.478, 0.536]; FAISS post 0.499 [0.468, 0.529], post-const 0.514 [0.483, 0.544], pre 0.504 [0.473,
0.535]; pgvector bm25-pre 0.536 [0.507, 0.563], post 0.493 [0.463, 0.523], post-const 0.484 [0.454,
0.515], pre 0.504 [0.472, 0.535], pre-exact 0.506 [0.478, 0.535]; Qdrant bm25-pre 0.492 [0.461,
0.522], post 0.495 [0.466, 0.525], post-const 0.517 [0.486, 0.545], pre 0.505 [0.474, 0.535],
pre-exact 0.499 [0.470, 0.529].

**G1 failed for the in-memory control**: post 0.533 [0.400, 0.650], pre 0.500 [0.367, 0.633]
(60 clusters, 5 seeds). What it means: the point estimates are at 0.5 and the intervals are wide, so
this is imprecision, not drift. With its reduced design (60 clusters, 3 repetitions) an interval
inside [0.40, 0.60] needs a half-width under 0.10, which 60 clusters do not give; the guard was out of
reach for this control by design (a flaw in the pre-registration, which did not adapt the guard to
the reduced design). Consequence under the rules: every latency part of the memory configurations is
inconclusive. They would have been inconclusive anyway: memory `pre` pooled latency 0.383 [0.267,
0.500], and every m = 1,000 part has 15 clusters, under the 20 required. H1 and H2 do not apply to
the in-memory control.

**What G1 cannot see.** SEPa and SEPb are one index measured twice. A latency difference between two
*builds* (W1 and W0^g are different index objects, and every W0^g is built later in the seed than
W1) is invisible to it. Such differences appear in this run (see H1(c) and H4 below).

## X6 verdicts as printed

| hypothesis | scope | outcome | parts (confirmed / falsified / inconclusive) |
|---|---|---|---|
| H1 | vector stores | **falsified** | 29 / 5 / 6 |
| H2 | vector stores | **falsified** | 2 / 4 / 10 |
| H3a | pgvector | confirmed | 3 / 0 / 0 |
| H3b | elasticsearch | inconclusive | 1 / 0 / 1 |
| H3c | qdrant | confirmed | 5 / 0 / 0 |
| H4 | pgvector pre-exact | inconclusive | 8 / 0 / 2 |
| H4 | qdrant pre-exact | inconclusive | 9 / 0 / 1 |
| H4 | elasticsearch pre-exact | inconclusive | 9 / 0 / 1 |
| H4 | faiss pre | inconclusive | 8 / 0 / 2 |
| H4 | memory pre | inconclusive | 3 / 0 / 5 |
| H5a | elasticsearch | inconclusive | 2 / 0 / 2 |
| H5a | qdrant | inconclusive | 2 / 0 / 2 |
| H5b | pgvector | confirmed | 2 / 0 / 0 |
| H5c | elasticsearch | confirmed | 1 / 0 / 0 |
| H6 | every cell with a raw latency channel | inconclusive | 0 / 0 / 7 (script defect, see below) |

### H1, widening (post)

| store | (a) m=1000 count p=1 | p=10 | p=50 | (b) m=100 latency p=10 | p=50 | (c) m=1 latency | (c) m=1 other observables |
|---|---|---|---|---|---|---|---|
| faiss | 1.000 [1.000, 1.000] C | 0.925 [0.863, 0.975] I | 0.688 [0.613, 0.762] **F** | 0.850 [0.762, 0.925] C | 0.975 [0.938, 1.000] C | 0.667 [0.617, 0.717] **F** | all 0.500 [0.500, 0.500] C |
| pgvector | 1.000 C | 0.912 [0.850, 0.963] I | 0.650 [0.588, 0.725] **F** | 0.662 [0.550, 0.762] I | 0.950 [0.900, 0.988] C | 0.369 [0.322, 0.417] I | count 0.499, complete 0.500, recall 0.496, score 0.496 C |
| qdrant | 1.000 C | 0.925 [0.863, 0.975] I | 0.688 [0.613, 0.762] **F** | 0.800 [0.713, 0.887] C | 0.950 [0.900, 0.988] C | 0.475 [0.419, 0.531] C | 0.506, 0.500, 0.501, 0.487 C |
| elasticsearch | 1.000 C | 0.912 [0.850, 0.963] I | 0.613 [0.550, 0.675] **F** | 0.825 [0.738, 0.900] C | 0.925 [0.863, 0.975] C | 0.481 [0.414, 0.544] C | 0.503, 0.499, 0.508, 0.507 C |

Clusters: 40 at m = 1,000, 80 at m = 100, 120 at m = 1. C confirmed, F falsified, I inconclusive.

One-shot (pooled) AUC beside the paired one: m = 100 latency FAISS 0.842 and 0.962 (p = 10, 50),
pgvector 0.808 and 0.945, Qdrant 0.811 and 0.916, ES 0.821 and 0.928; m = 1,000 count at p = 1:
1.000 (FAISS, pgvector, ES), 0.999 (Qdrant). Mean latency, FAISS post m = 100: p = 10 28.669 against
19.069 ms, p = 50 14.837 against 7.175 ms.

**Mechanism of H1(a) at p = 50% (falsified) and p = 10% (inconclusive): readable hubs among the
1,000 candidates.** The prediction's premise was that "the 1,000 nearest candidates are the secrets,
so the widening ends at the cap with nothing readable". Amendment 1 made hubs ineligible as secrets,
so hubs stay in the background, readable with probability p, interleaved with the secrets. Evidence:

- The largest rank of the 1,000th near passage per seed is 1,149, 1,085, 1,145, 1,271 and 1,040
  (plan manifest): up to 271 hubs lie before the last secret of an m = 1,000 probe.
- W1 mean count at m = 1,000 (post) rises with p: FAISS 0.375, 3.350, 7.600 at p = 1, 10, 50
  (W0: 7.675, 10.000, 10.000); pgvector 0.500, 3.825, 8.600; Qdrant 0.375, 3.275, 7.550; ES 0.525,
  4.225, 9.025.
- Derived: if h readable-eligible hubs lie among the candidates, E[count] = p x h until the cap of 10
  binds; 0.375 / 0.01 = 37.5 and 3.350 / 0.10 = 33.5 (FAISS), so about 35 hubs per m = 1,000 probe's
  candidate list on average, consistent with the ranks above.
- The count AUC equals 1 minus half the share of W1 answers that are full (W0 is always full at
  p = 10, 50): W1 `complete` share FAISS 0.000, 0.150, 0.625 at p = 1, 10, 50, and
  1 - 0.625 / 2 = 0.6875, printed 0.688; 1 - 0.150 / 2 = 0.925, printed 0.925 (derived). pgvector
  0.700 at p = 50 gives 0.650 (printed 0.650); ES 0.775 gives 0.6125 (printed 0.613).
- FAISS is exact and shows the same p = 50 AUC as Qdrant (0.688), so approximation is not the cause.

Needs the raw plan files (artifact `x3x6-data`): per-probe hub counts among the first 1,000 ranks,
to show the count per probe tracks Binomial(h, p). Not required for the conclusion.

**Mechanism of H1(b) pgvector p = 10% (inconclusive, 0.662 [0.550, 0.762]): partly explained.** The
widening effect is there in the means (W1 18.697 against W0 10.670 ms) and in the one-shot AUC
(0.808), but the paired AUC is diluted by probes that need no extra round in W1 (readable hubs
again) and on which pgvector's W1 index is slightly faster than W0^g whatever m is (pgvector post
latency AUC at m = 1 0.369 [0.322, 0.417], m = 10 0.383 [0.333, 0.433]). FAISS, without that offset,
gives 0.850 in the same cell. Needs the raw records (widening rounds per probe) to confirm.

**Mechanism of H1(c) FAISS m = 1 latency (falsified, 0.667 [0.617, 0.717]): not the secret; most
consistent with a difference between the two index objects; not proven.**

- Same answers: FAISS post returned identical hit lists in W1 and W0 in all 360 pairs at m = 1
  (`x6_listchange.csv`: rate 0.0 at p = 1, 10, 50), and count, complete, recall and score AUCs are
  0.500 [0.500, 0.500].
- Tiny, consistent difference: mean W1 against W0 45.515 / 45.374 ms (p = 1), 18.273 / 18.145
  (p = 10), 7.167 / 7.117 (p = 50); per-p paired AUC 0.608 [0.525, 0.692], 0.717 [0.633, 0.792],
  0.675 [0.592, 0.758]; pooled (one-shot) 0.520.
- Not dose-dependent: at m = 10, with ten times as many secrets among the 40 fetched candidates, the
  AUC is the same, 0.672 [0.617, 0.725]. The `post-const` path over the same index objects shows the
  same direction at m = 1, 0.628 [0.575, 0.681].
- The denial path is unlikely: at m = 1 the post-filter authorizes the same 40 candidates per round
  in both worlds (the secret replaces one background candidate); an extra round in W1 needs the
  tenth readable candidate of W0 to sit exactly at a round's last rank, which is rare (a negative
  binomial tail; not computed here), while W1 was slower for about two thirds of probes.
- Offsets of both signs that do not depend on m exist in other configurations whose answers are
  identical in both worlds: FAISS `pre` (W1 faster) 0.25 [0.20, 0.30], 0.30, 0.25, 0.35 at m = 1, 10,
  100, 1,000 (means 128.062 against 128.354 ms at m = 1); pgvector `pre-exact` (W0^g slower)
  0.17, 0.14, 0.13, 0.12, with W0^g 1.5 to 3.5 times slower at every m (p = 1: 2.604 against 9.072
  ms; p = 10: 19.695 against 42.766; p = 50: 84.880 against 131.512, pooled over m).
- G1 compares one index with itself and cannot detect a difference between builds.

Computation that would settle it: from artifact `x3x6-results-x6-faiss`, per (seed, probe, p) at
m = 1 and 10, the paired difference of `search_ms` and `authorize_ms` and the number of widening
rounds (`searches`) in W1 and W0. For future runs: an A/A comparison across two independent builds
of the same world (W0^g built twice), which would measure the build offset directly.

Whether it is a "real micro-channel": in the game W0 and W1 are separate builds, so any build offset
reads as a channel; a deployment that adds a document to the same index does not change the index
object, so the offset would not be there, while a deployment that rebuilds would show one unrelated
to the content. Either way it carries no information about the secret beyond what m = 10 shows.

**pgvector m = 1 latency (inconclusive, 0.369, W1 faster)**: same class of offset, opposite sign;
not explained beyond that.

### H2, constant-work widening (post-const)

| store | (a) pooled latency | (a) m=1000 latency | (b) m=1000 count p=10 | p=50 |
|---|---|---|---|---|
| faiss | 0.517 [0.484, 0.549] C | 0.133 [0.075, 0.200] I | 0.925 [0.863, 0.975] I | 0.688 [0.613, 0.762] **F** |
| pgvector | 0.188 [0.163, 0.214] I | 0.017 [0.000, 0.050] I | 0.912 [0.850, 0.963] I | 0.650 [0.588, 0.725] **F** |
| qdrant | 0.456 [0.422, 0.491] C | 0.350 [0.225, 0.483] I | 0.925 [0.863, 0.975] I | 0.688 [0.613, 0.762] **F** |
| elasticsearch | 0.573 [0.536, 0.610] I | 0.625 [0.517, 0.725] I | 0.912 [0.850, 0.963] I | 0.613 [0.550, 0.675] **F** |

- (b) is falsified and inconclusive by the same hub mechanism as H1(a); post-const fetches the same
  1,000 candidates, so the counts are those of post.
- (a) The widening channel is gone, but a channel in the **reverse** direction appears where
  candidates are secrets: pgvector latency AUC by m 0.289, 0.219, 0.075, 0.017 (pooled over p; at
  m = 1,000 W1 23.535 against W0 26.361 ms, and at p = 1 23.692 against 26.457); FAISS 0.628, 0.572,
  0.458, 0.133 (m = 1,000: 18.433 against 18.692 ms); Qdrant 0.475, 0.475, 0.454, 0.350. Because it
  grows with m, it depends on the secrets, unlike the m-independent offsets. Its mechanism is not
  established: FAISS's search cost does not depend on the data, so at least part lies in the layer
  (W1 returns fewer readable hits at m = 1,000, so less to re-check and return); for pgvector the
  gap at p = 1 (both worlds return few hits) points to the store's own traversal, where the 1,000
  nearest rows form a dense cluster of secrets in W1 and a sparser background region in W0. Needs
  `search_ms` and `authorize_ms` per pair from the raw records.
- ES: W1 slightly slower, 0.573 pooled, 0.625 at m = 1,000 (means 30.319 against 30.209 ms pooled,
  30.985 against 30.709 at m = 1,000). Not explained.
- **Interpretation difference, script against text.** The text of H2(a) and H4 asks at m = 1,000
  only that "the interval's upper end is at most 0.65". `x6_stats.py` applies `absent(c,
  upper=0.65)`, which also requires the lower end to be at least 0.40 (two-sided). Under the
  one-sided text, the m = 1,000 parts would be confirmed for FAISS, pgvector and Qdrant here (H2
  remains falsified through (b)) and for Qdrant and ES `pre-exact` in H4 (see below). The two-sided
  reading treats a reverse channel as a channel, which matches the intent of "no channel"; we report
  the printed verdicts and state the difference.

### H3, approximate pre-filter

- **H3a pgvector confirmed**: latency 1.000 [1.000, 1.000] at m = 1,000 p = 10 and p = 50 and at
  m = 100 p = 50 (40, 40, 80 clusters); means at m = 1,000 13.470 against 4.692 ms (p = 10) and
  13.707 against 3.285 (p = 50); one-shot 0.999 and 0.984. Exploratory, same cells: **recall moves
  the other way**: W1 recall@10 0.968 and 0.978 against W0 0.707 and 0.665 at m = 1,000, p = 10 and
  50 (recall paired AUC 0.100 [0.037, 0.163] and 0.150 [0.087, 0.225]); m = 100 p = 50 0.957 against
  0.780. Mechanism (consistent with the configured iterative scan): the scan passes the unreadable
  secrets, keeps going, and so ranks many more readable rows before it stops, approaching exact
  search; in W0 the first `ef_search` candidates already hold ten readable rows and the answer stays
  approximate. Pooled over m and p the recall AUC is 0.41 [0.40, 0.43].
- **H3b ES inconclusive**: m = 1,000 p = 10 0.800 [0.675, 0.925] confirmed; p = 50 0.613 [0.463,
  0.750] inconclusive. The differences are tiny: means 2.426 against 2.430 ms (p = 10, the W1 mean is
  lower although W1 is slower for most probes) and 2.498 against 2.520 (p = 50); one-shot 0.626 and
  0.530. At m = 1, 10, 100 there is no channel (0.487, 0.500, 0.477 pooled over p). Not explained;
  a fixed `num_candidates` of 100 bounds the extra work of passing secrets, which may be why the
  effect is small.
- **H3c Qdrant confirmed**: p in {1, 10}, pooled over m: latency 0.460 [0.424, 0.496], count,
  complete, recall, score 0.500 [0.500, 0.500]. Exploratory p = 50 at m = 1,000: recall paired AUC
  0.787 [0.688, 0.875], W1 recall 0.530 against W0 0.708, and W1 mean count 9.775 (some answers
  shorter than k; count AUC 0.512 [0.500, 0.537]). This is the islanding of the X1 diagnosis: a
  filter too broad for Qdrant's exact payload-index plan runs as filtered HNSW traversal, and a
  thousand unreadable points around the query cut the readable region off.

### H4, exact pre-filter (M2) and controls

- Every non-latency part is confirmed for pgvector, Qdrant and ES `pre-exact` and FAISS `pre`:
  count, complete, recall, score 0.500 [0.500, 0.500], pooled and at m = 1,000 (G2: identical hit
  lists). Exact pre-filtering returned the same answer in both worlds for every probe.
- Latency parts:
  - Qdrant `pre-exact`: pooled 0.461 [0.431, 0.490] confirmed; m = 1,000 0.417 [0.325, 0.508]
    inconclusive (40 clusters cannot place the interval inside [0.40, 0.65]; one-sided text:
    confirmed). Under the one-sided text, H4 for Qdrant would be confirmed.
  - ES `pre-exact`: pooled 0.486 [0.450, 0.521] confirmed; m = 1,000 0.467 [0.367, 0.575]
    inconclusive (same reason; one-sided text: confirmed).
  - pgvector `pre-exact`: pooled 0.147 [0.123, 0.172], m = 1,000 0.125 [0.067, 0.192], both
    inconclusive (reverse). The W0^g tables were slower at every m (see H1(c)); m-independent, so
    not about the secrets. **Not explained.** Leading candidate, untested: each W0^g was built and
    ANALYZEd shortly before its group was measured, while W1 was built at the start of the seed; if
    autovacuum had marked W1's pages all-visible but not yet those of W0^g, sequential and bitmap
    heap scans, which skip per-tuple visibility checks on all-visible pages, would be faster on W1.
    The run did not record vacuum state or plans for X6. Test: run `VACUUM (ANALYZE)` after each
    build, or record `EXPLAIN (ANALYZE, BUFFERS)` of one probe on W1 and on W0^g. The same direction
    shows in pgvector `pre` at p = 1 (W1 8.675 against W0 10.842 ms at m = 1) and `post-const`.
  - FAISS `pre`: pooled 0.276 [0.246, 0.306], m = 1,000 0.350 [0.250, 0.450], inconclusive; W1
    faster by about 0.3 ms on 115 to 147 ms at every m; not explained (the cost is dominated by
    evaluating the filter over the metadata in Python, not by the FAISS index).
  - memory `pre`: G1 failed; m = 1,000 parts have 15 clusters.

### H5, collection statistics

- **H5a inconclusive** for both stores: score paired AUC ES 0.794 [0.728, 0.858], 0.875 [0.819,
  0.928], 0.983 [0.954, 1.000], 0.992 [0.975, 1.000] at m = 1, 10, 100, 1,000; Qdrant 0.811 [0.744,
  0.872], 0.886 [0.833, 0.933], 0.979 [0.950, 1.000], 1.000 [1.000, 1.000]. m = 1 and 10 below 0.90
  (inconclusive), m = 100 and 1,000 confirmed; none near the falsification bound (0.70 at m = 1,000).
  Effect sizes are small: ES mean top-10 score 13.6344 against 13.6761 at m = 1, 13.2516 against
  13.6549 at m = 1,000. The one-shot attacker sees almost nothing: pooled AUC 0.503 [0.502, 0.505] to
  0.531 [0.526, 0.544]; KS 0.014 to 0.100. Every BM25 answer's scores changed between worlds (change
  rate 1.000 at every m, A/A 0.000); the ids changed for ES 0.461, 0.453, 0.483, 0.883 of probes at
  m = 1, 10, 100, 1,000, Qdrant 0.406, 0.425, 0.467, 0.842.
- **Confound (design).** W1 and W0^g differ in all 1,233 secrets of group g: the probe's own m and
  its eight group mates'. The zone rule keeps the mates' secrets beyond the depth dense search
  explores for this probe, but BM25's IDF and average length are collection-wide and see all 1,233.
  The m = 1 and m = 10 cells therefore measure the removal of a group of on-domain passages, not of
  one or ten documents. The single-document channel the hypothesis describes is not isolated by the
  grouped design (it was by the original per-probe W0, which Amendment 1 replaced). Not explained
  further.
- **H5b confirmed**: pgvector `ts_rank_cd` score 0.500 [0.500, 0.500] at every m; change rate
  0.002 [0.000, 0.005] (2 of 1,080 pairs). Exploratory latency: 0.45, 0.47, 0.50, then 0.70 [0.58,
  0.81] at m = 1,000 (W1 slower); consistent with the text index matching secrets that share the
  probe's words, which the permission filter then removes. Not verified (needs plans).
- **H5c confirmed**: ES `hybrid-exact` change rate at m = 1,000 0.567 [0.483, 0.650] (ids 0.55);
  at m = 1 0.269, m = 10 0.267, m = 100 0.300 (group confound as in H5a). Fusion score AUC stays near
  0.5 (0.50 pooled; 0.53 [0.51, 0.55] at m = 1,000), as RRF scores depend on ranks.

### H6, padding (M4): script defect

Seven cells had a raw latency AUC of at least 0.75 on seeds 1 to 4: ES post m = 1,000 (raw 0.844
[0.781, 0.896], 32 clusters), FAISS post m = 100 (0.833 [0.786, 0.880], 64) and m = 1,000 (0.781
[0.729, 0.833], 32), pgvector pre m = 100 (0.807 [0.766, 0.849], 64) and m = 1,000 (0.927 [0.875,
0.969], 32), Qdrant post m = 100 (0.755 [0.698, 0.812], 64) and m = 1,000 (0.781 [0.729, 0.833],
32). In every one the padded AUC is **0.500 [0.500, 0.500]** (4 seeds): every padded latency equals
the budget, so W1 and W0 tie.

The script printed **inconclusive** for all seven because of a defect in `x6_stats.py`, `h6()`:

```python
# T comes from seed 0 and the cells use seeds 1 to 4, so the rule needs all five seeds.
ready = len(seeds) >= MIN_SEEDS and self.usable(padded, seeds=MIN_SEEDS - 1)
outcome = self.absent(padded) if ready else INCONCLUSIVE
```

`absent()` calls `self.usable(c)` with the default `seeds=MIN_SEEDS` (5), and padded cells have 4
seeds by design, so `absent()` always returns inconclusive. Applied as written (G1 passed for all
four configurations; at least 20 clusters; the padded interval lies within [0.40, 0.60]), the rule
**confirms H6 in all seven cells**. This is a deviation to report (the rule was applicable; the
script did not apply it), not a change of rule. The fix is to pass `seeds=MIN_SEEDS - 1` through to
`absent` (or test usability once); the repository was not modified.

### Mitigation costs (latency, ratio of means [interval], median of per-probe ratios)

| store | M1 post-const / post | M2 pre-exact / pre | M3 separated / shared | M4 padded / raw |
|---|---|---|---|---|
| elasticsearch | 1.106 [1.08, 1.13] (3.012) | 2.014 [1.99, 2.03] (1.393) | 0.901 to 0.986 | post 5.224 (14.139), pre 6.265, pre-exact 3.083, post-const 3.675, bm25 4.588, hybrid-pre 3.248, hybrid-exact 2.246 |
| faiss | 0.740 [0.73, 0.75] (1.257) | n/a | 0.855 (post), 0.874 (pre), 0.965 (post-const) | post 6.651 (11.127), post-const 7.745, pre 1.332 |
| memory | n/a | n/a | 0.779 (post), 0.946 (pre) | post 1.422, pre 1.688 |
| pgvector | 1.226 [1.20, 1.25] (3.432) | 8.099 [7.73, 8.48] (6.475) | pre 0.452, pre-exact 0.592, post 0.862, post-const 0.947, bm25 1.073 [0.98, 1.18] | post 6.910 (18.390), post-const 5.566, pre 5.216 (9.501), pre-exact 4.448, bm25 15.727 [10.09, 26.74] (57.570) |
| qdrant | 1.052 [1.03, 1.07] (2.673) | 1.525 [1.52, 1.53] (1.006) | 0.904 to 0.989 | post 6.402 (15.949), post-const 4.234, pre 2.215, pre-exact 20.124, bm25 27.148 (31.666) |

M3's measured advantage is G1 (A/A 0.463 to 0.536 on the vector stores; list change 0.000).
M1 on FAISS is cheaper than widening (0.740): one 1,000-candidate round replaces up to four at
p = 1%; its median ratio 1.257 shows the typical request pays more. M4's cost is the budget (the
largest seed-0 latency) over the typical latency, hence medians up to 57.6.

### Exploratory: all paired AUCs (pooled over p) for the figure "paired advantage against m"

Data for a figure if one is wanted (advantage = 2 x AUC - 1; the report prints AUCs to 2 decimals
with intervals in `x6_report.md`, table "Paired AUC (W1 against W0), pooled over selectivity"):

| store, config, observable | m = 1 | 10 | 100 | 1,000 |
|---|---|---|---|---|
| FAISS post latency | 0.67 [0.62, 0.72] | 0.67 [0.62, 0.72] | 0.80 [0.76, 0.85] | 0.76 [0.72, 0.81] |
| pgvector post latency | 0.37 [0.32, 0.42] | 0.38 [0.33, 0.43] | 0.57 [0.53, 0.62] | 0.68 [0.67, 0.69] |
| Qdrant post latency | 0.47 [0.42, 0.53] | 0.46 [0.41, 0.51] | 0.75 [0.70, 0.80] | 0.78 [0.73, 0.83] |
| ES post latency | 0.48 [0.41, 0.54] | 0.58 [0.51, 0.65] | 0.76 [0.70, 0.82] | 0.86 [0.81, 0.91] |
| post count (FAISS / pgvector / Qdrant / ES) | 0.50 / 0.50 / 0.51 / 0.50 | 0.51 / 0.50 / 0.51 / 0.51 | 0.59 / 0.58 / 0.58 / 0.58 | 0.87 / 0.85 / 0.87 / 0.84 |
| post complete (same order) | 0.50 / 0.50 / 0.50 / 0.50 | 0.50 / 0.50 / 0.50 / 0.50 | 0.52 / 0.51 / 0.51 / 0.51 | 0.74 / 0.73 / 0.75 / 0.72 |
| FAISS post-const latency | 0.63 | 0.57 | 0.46 | 0.13 [0.07, 0.20] |
| pgvector post-const latency | 0.29 | 0.22 | 0.07 | 0.02 [0.00, 0.05] |
| Qdrant post-const latency | 0.47 | 0.47 | 0.45 | 0.35 [0.23, 0.48] |
| ES post-const latency | 0.57 | 0.57 | 0.55 | 0.62 [0.52, 0.72] |
| pgvector pre latency | 0.33 | 0.44 | 0.79 [0.75, 0.82] | 0.88 [0.82, 0.93] |
| pgvector pre recall | 0.49 | 0.47 | 0.31 [0.29, 0.34] | 0.22 [0.17, 0.27] |
| Qdrant pre latency | 0.47 | 0.43 | 0.47 | 0.57 [0.45, 0.68] |
| Qdrant pre recall | 0.50 | 0.53 | 0.53 | 0.60 [0.56, 0.62] |
| ES pre latency | 0.49 | 0.50 | 0.48 | 0.60 [0.50, 0.68] |
| FAISS pre latency | 0.25 | 0.30 | 0.25 | 0.35 |
| pgvector pre-exact latency | 0.17 | 0.14 | 0.13 | 0.12 |
| Qdrant pre-exact latency | 0.45 | 0.46 | 0.50 | 0.42 |
| ES pre-exact latency | 0.50 | 0.48 | 0.47 | 0.47 |
| ES bm25-pre score | 0.79 [0.73, 0.86] | 0.88 [0.82, 0.93] | 0.98 [0.95, 1.00] | 0.99 [0.97, 1.00] |
| Qdrant bm25-pre score | 0.81 [0.74, 0.87] | 0.89 [0.83, 0.93] | 0.98 [0.95, 1.00] | 1.00 [1.00, 1.00] |
| pgvector bm25-pre score | 0.50 | 0.50 | 0.50 | 0.50 |
| pgvector bm25-pre latency | 0.45 | 0.47 | 0.50 | 0.70 [0.58, 0.81] |
| ES bm25-pre latency | 0.41 | 0.45 | 0.43 | 0.40 |
| ES hybrid-pre score / latency | 0.48 / 0.49 | 0.48 / 0.49 | 0.52 / 0.45 | 0.53 / 0.49 |

A figure is not needed for the claims; the table `tab:side-auc` in `side.tex` carries the main rows.

### Deviations from the pre-registration (X6)

1. **Far chunks reused** in seeds 1, 2 and 4: eligible SciDocs passages (4,491; 2,331; 4,864) were
   fewer than secrets (8,510; 8,417; 8,985), and `x6_data.py` cycles through the eligible list
   (`eligible[i % len(eligible)]`), while amendment 1 says "far chunks are drawn without replacement
   across groups". Seeds 0 and 3 had no reuse. Every far chunk still lay below every probe's zone
   boundary (`far_closest_max` below `boundary` in every seed), so no reused far chunk entered any
   explored zone. Possible effects: duplicate vectors in W0's far region (approximate graphs) and
   repeated SciDocs terms (BM25 statistics of words FiQA probes rarely use). Not assessed; would
   need a rerun of seeds 1, 2, 4 with distinct far chunks (impossible at this boundary with 12,000
   SciDocs passages; a larger far pool would be needed).
2. **H6 script defect** (above): printed inconclusive, confirmed under the written rule.
3. **H2/H4 m = 1,000 one-sided text against two-sided script** (above).
4. **Group confound for collection statistics** (H5a, H5c at small m): a property of the amended
   design, not of the run; the amendment did not discuss it.
5. **G1 for the in-memory control** could not pass at 60 clusters by design.

## X3: what ran

| store | seeds done | retrievals | errors | build s | crashes |
|---|---|---|---|---|---|
| cassandra | 0-4 | 4,200 | 0 | 209 | none |
| chroma | 0-2 (each crashed at G = 40,000); 3, 4 skipped | 630 | 270 | 138 | -11, -11, -11 |
| elasticsearch | 0-4 | 4,200 | 0 | 55.9 | none |
| faiss | 0-4 | 4,200 | 0 | 1.3 | none |
| lancedb | 0-4 | 4,200 | 0 | 9.8 | none |
| memory | 0-4 | 4,200 | 0 | 1.1 | none |
| milvus | 0-4 | 4,200 | 0 | 43.2 | none |
| mongodb | 0-4 | 4,200 | 0 | 37.1 | none |
| opensearch | 0-4 | 4,200 | 0 | 70.5 | none |
| pgvector | 0-4 | 4,200 | 0 | 42.0 | none |
| qdrant | 0-4 | 4,200 | 0 | 78.2 | none |
| redis | 0-4 | 4,200 | 0 | 23.9 | none |
| vespa | 0-4 | 4,200 | 0 | 207 | none |
| weaviate | 0-4 | 4,200 | 0 | 47.3 | none |

56,992 records, 0 unreadable. No level timed out, no level was cut ("a smaller level timed out"
never occurred), every level of every store but Chroma ran 30 queries x 3 timed passes x 5 seeds
(450 timed retrievals). Chroma's accepted levels (G = 1, 10, 100) used the pre-registered slow-level
rule in all three seeds (first warm-up retrieval over 2 s): 10 queries, 90 timed retrievals per
level. Corpus: "57,638 FiQA passage embeddings and 6,648 FiQA query embeddings" (no synthetic-only
fallback). Build details from the logs: ES `bbq_hnsw` (m 16, ef_construction 100, rescore oversample
3.0), 4 to 9 segments; OpenSearch Lucene HNSW, 6 to 7 segments; Qdrant 2 segments, 100,000 indexed
vectors, green, settled wait 17 s; Milvus index Finished, 100,000 indexed rows; Redis 100,000 docs.

**Why Chroma ran three seeds.** Chroma was the first of four targets in the `x3-embedded` job
(`chroma,lancedb,faiss,memory`). The driver gives each target the smaller of its budget (330 min) and
a fair share of what is left of the job's 320 minutes, here 320 / 4 = 80 min, and skips a seed when
1.2 times the longest seed so far does not fit. Each Chroma seed took about 22 min (19:30:53 to
19:53:12, 19:53:12 to 20:15:14, and 20:15:14 to shortly after 20:37:23), so after three seeds (about
67 min) seed 3 did not fit: "seed 3 skipped: not enough time left", "seed 4 skipped: not enough time
left". The job then ran LanceDB, FAISS and memory and **finished at 21:50:05, about three hours
before its deadline**. The skip is a scheduling defect of the harness (the share ignores how long the
later targets need), not a pre-registered cut; it is a deviation. Completing Chroma needs only its
seeds 3 and 4 (`SEED_LIST=3-4`, about 45 min).

## X3: Chroma, refusal and crash

Log of the `x3-embedded` job, Chroma (complete; quoted as published):

```
[19:30:53] x3 chroma: seed 0
[19:30:55]   seed 0: building (100,000 chunks)
[19:33:13]   seed 0: built in 138 s {}
[19:36:14]   seed 0: G=1: ok, 0 errors, translation ok
[19:39:37]   seed 0: G=10: ok, 0 errors, translation ok
[19:46:43]   seed 0: G=100: ok, 0 errors, translation ok
[19:48:43]   seed 0: G=1,000: refused, 30 errors, translation ok
[19:50:48]   seed 0: G=4,000: refused, 30 errors, translation ok
[19:52:53]   seed 0: G=10,000: refused, 30 errors, translation ok
::warning title=x3 chroma::seed 0: the process ended with status -11
...
::warning title=x3 chroma::seed 2: the process ended with status -11
::warning title=x3 chroma::seed 3 skipped: not enough time left
::warning title=x3 chroma::seed 4 skipped: not enough time left
::warning title=x3 chroma::{"0": -11, "1": -11, "2": -11}
```

Seeds 1 and 2 repeat seed 0 line for line. `crashes.jsonl`: `{"schema": 1, "type": "crash",
"store": "chroma", "group": "x3-embedded", "exit_status": 6}` (the driver's status 6 means "a seed
process died"; the per-seed return code is -11, killed by signal 11, SIGSEGV).

`x3_errors.csv`: at G = 1,000, 4,000 and 10,000, 90 errors each (30 per seed, the whole warm-up
pass; the timed passes are then not run), all:

> InternalError: Error executing plan: Internal error: error returned from database: (code: 1)
> Expression tree is too large (maximum depth 1000)

**Where the crash happens.** For each level the seed process writes `level-start`, then calls the
translator 3 times and writes a `translate` record, then runs the warm-up retrievals, writing one
record per retrieval. At G = 40,000 the published level table shows the translation **succeeded**
(status ok, 100.9 ms median, 2,657,983 characters) and **no retrieval record** (timed 0, ok share
nan, first error "the process crashed, exit status -11"). So the process died inside the first
warm-up retrieval at G = 40,000, after wardowl's Python translation (`filter_to_where`, which built
and serialized the `where` document without error), that is inside `collection.query` of chromadb
1.5.9 (`EphemeralClient`, the Rust core). The next seed started 19 s after the G = 10,000 line, so
the first query died within seconds. No Python traceback, no Rust panic message and no
"overflowed its stack" line was printed (the child's output goes to the same log).

**What the filter looks like.** wardowl's Chroma translator turns `In(allowed_groups, groups + "*")`
into `{"$or": [{"allowed_groups": {"$in": [...]}}, {"allowed_groups::s:<g>": {"$eq": true}}, ...]}`,
one `$eq` clause per value (wardowl stores list values as boolean keys because of
chroma-core/chroma#7594), so the largest `$or` holds G + 2 clauses: 102 at G = 100 (accepted), 1,002
at G = 1,000 (refused). SQLite's default `SQLITE_MAX_EXPR_DEPTH` is 1,000. The refusal is consistent
with Chroma rendering an n-ary `$or` as a left-deep chain of binary ORs, whose depth is the number of
clauses; the threshold therefore lies between 100 and 1,000 groups in this run (about 998 by that
reading; not measured).

**Mechanism of the crash: not established.** The most consistent explanation is a stack overflow in
native code while chromadb converts or renders the 40,003-clause disjunction (depth about 40,000),
before SQLite could refuse it: at depth 10,000 the same path returned SQLite's error, at 40,000 the
process died without a message, as an overflow in a native library without Rust's stack-overflow
handler does. Not proven. To confirm: run that one query with `python -X faulthandler` (prints the
Python stack at the signal) or under `gdb` for the native stack, and bisect G between 10,000 and
40,000.

**Comparison with the smoke runs.** The smoke runs (40918774649, 40937668791) showed the same two
behaviours: refusal with the same SQLite message from G = 1,000, and the process ended with status
-11 at G = 40,000. With the full run's three seeds: 5 of 5 processes crashed at G = 40,000.

Other Chroma observations: retrievals were slow at every level (p50 4,416 ms at G = 1, 5,057 at 10,
10,689 at 100), and each refused retrieval also took about 4 s before failing (30 per level in about
120 to 125 s, from the log times). Recall@10 1.000 at G = 1, 10, 100.

**X3 Chroma verdicts**: X3-H1 Chroma parts inconclusive (3 seeds; all translations ok, median 0.0,
0.0, 0.1, 1.1, 4.5, 12.5, 100.9 ms); X3-H2 inconclusive ("observed refuses in 3 seeds"); X3-H4
inconclusive ("no accepted level pair").

## X3: verdicts as printed

| hypothesis | scope | outcome | parts |
|---|---|---|---|
| X3-H1 | every store | inconclusive | 77 confirmed, 0 falsified, 7 inconclusive (all Chroma: 3 seeds) |
| X3-H2 | cassandra, elasticsearch, faiss, lancedb, memory, opensearch, pgvector, qdrant | confirmed (each) | accepts at G = 40,000 in 5 seeds, ok share 1.000 |
| X3-H2 | chroma | inconclusive | refuses in 3 seeds (crash) |
| X3-H2 | milvus, mongodb, redis, vespa, weaviate | reported (no prediction) | accepts in 5 seeds, ok share 1.000 |
| X3-H3a | pgvector | confirmed | ratio 272.22 [264.42, 287.67], 150 queries, 5 seeds |
| X3-H3b | faiss, memory | confirmed | 1.19 [1.18, 1.19]; 1.17 [1.16, 1.18] |
| X3-H3c | cassandra | confirmed | p50 G = 100 / G = 1,000 1.85 [1.82, 1.87] |
| X3-H4 | qdrant, elasticsearch, opensearch, redis, weaviate, milvus, mongodb, vespa | confirmed (each) | see recall |
| X3-H4 | chroma | inconclusive | no accepted level pair |
| sanity | faiss, lancedb | passed | recall 1.0000 at every G |

Translation medians per store at G = 40,000 (X3-H1, all under 1 s): Cassandra 196.9 ms (fallback),
pgvector 120.1, Chroma 100.9, LanceDB 49.4, Redis 47.5, Vespa 46.1, MongoDB 37.7, Weaviate 36.7,
Qdrant 34.8, Milvus 33.8, OpenSearch 31.6, ES 31.2; FAISS and memory in process. Cassandra's
translator reports its documented fallback from G = 1,000 (status `fallback`).

Translation sizes (characters) at G = 40,000: Chroma 2,657,983; Vespa 2,537,926; LanceDB 2,457,950;
Redis 2,417,915; pgvector 1,658,057; ES and OpenSearch 1,509,067; Milvus 1,509,060; MongoDB
1,509,023; Qdrant 589,320. Weaviate (75 at every G) and Cassandra (19 to 39) report the length of
the client object's string form, not a payload size: a measurement limitation of `size_of`.

## X3: acceptance, latency, recall per store and G

Every store other than Chroma accepted every level in every seed with zero errors (ok share 1.000;
`x3_errors.csv` lists Chroma only). No documented limit bound: ES and OpenSearch got one `terms`
query of 40,001 values (under 65,536), pgvector two array parameters, MongoDB a command of about
1.5 million characters (under 16 MB), Qdrant about 0.59 million (under 32 MB).

p50 latency (ms), median of 3 passes, by G = 1 / 10 / 100 / 1,000 / 4,000 / 10,000 / 40,000:

| store | p50 | ratio 40,000 / 1 [interval] | recall@10 |
|---|---|---|---|
| pgvector | 2.860 / 3.590 / 4.509 / 22.195 / 81.323 / 201 / 797 | 272 [264.42, 287.67] | 0.967 every G |
| redis | 1.189 / 1.244 / 1.752 / 4.882 / 14.370 / 33.093 / 123 | 99.176 [93.71, 101.44] | 0.969 |
| vespa | 3.029 / 3.233 / 4.085 / 9.610 / 27.258 / 60.287 / 225 | 76.139 [72.24, 79.73] | 0.887 |
| weaviate | 4.788 / 4.831 / 5.739 / 14.336 / 38.438 / 82.710 / 306 | 64.057 [63.06, 65.57] | 1.000 |
| qdrant | 3.495 / 4.295 / 4.355 / 6.297 / 13.250 / 27.332 / 101 | 27.547 [26.41, 28.31] | 0.999 |
| milvus | 4.849 / 4.240 / 4.305 / 7.532 / 18.640 / 35.199 / 127 | 26.535 [25.72, 27.48] | 0.987 rising to 0.999 |
| elasticsearch | 3.358 / 2.728 / 2.782 / 3.954 / 8.734 / 19.345 / 78.798 | 24.987 [24.21, 27.05] | 0.939 |
| mongodb | 10.474 / 10.627 / 9.754 / 12.092 / 21.896 / 41.668 / 142 | 13.654 [13.57, 13.77] | 1.000 |
| opensearch | 6.062 / 6.377 / 6.269 / 7.627 / 10.862 / 20.171 / 71.605 | 11.526 [10.78, 12.22] | 1.000 |
| lancedb | 53.627 / 54.726 / 56.967 / 66.287 / 94.574 / 149 / 424 | 7.938 [7.91, 7.97] | 1.000 (exact) |
| cassandra | 109 / 42.199 / 166 / 90.707 / 100 / 124 / 308 | 2.782 [2.72, 2.86] | 0.996, then 1.000 |
| faiss | 385 / 391 / 390 / 403 / 416 / 424 / 454 | 1.191 [1.18, 1.19] | 1.000 (exact) |
| memory | 432 / 438 / 439 / 451 / 465 / 475 / 503 | 1.169 [1.16, 1.18] | n/a |
| chroma (3 seeds, 10 queries) | 4,416 / 5,057 / 10,689 / refused / refused / refused / crashed | n/a | 1.000 to G = 100 |

p95 and p99 are in `x3_report.md`; at G = 40,000 p99 is pgvector 1,013 ms, Weaviate 326, Cassandra
330, Vespa 294.

Recall differences G = 40,000 minus G = 1, paired by query (150 pairs): 0.000 [0.000, 0.000] for
Qdrant, ES, OpenSearch, Weaviate, MongoDB, Vespa and pgvector (exploratory); Redis 0.000 [-0.0007,
0.0007]; Milvus +0.012 [0.0060, 0.0187] (0.9873 to 0.9993: better with the larger filter; not
explained); Cassandra (exploratory) +0.004 [0.0007, 0.0093] (0.9960 to 1.0000).

Observations and mechanisms:

- **pgvector (X3-H3a confirmed)**: flat to G = 100 (2.86 to 4.51 ms), then roughly proportional to G
  (22.2 ms at 1,000, 201 at 10,000, 797 at 40,000), as predicted for a per-row array test once the
  layer switches to array parameters above 100 values. The plans are **not in the published
  outputs**: `x3_stats.py` does not summarise the `explain` records (35 of them, the extra lines in
  `x3-pgvector.jsonl`: 4,362 against 4,327). Indirect evidence: recall@10 is 0.9667 [0.955, 0.977]
  at every G and the paired difference is 0.000 [0.000, 0.000], so every query returned the same
  answer at every level; the scan order did not change (no switch to an exact plan, which would give
  1.0). Needs the raw records (artifact `x3x6-results-x3-pgvector-redis`) for node types and rows
  removed by the filter.
- **Cassandra (X3-H3c confirmed)**: 102 ANN queries at G = 100 (166 ms) against one fallback query
  at G = 1,000 (90.7 ms); the fallback then grows slowly to 308 ms at 40,000, of which the
  translation is 197 ms. Not explained: G = 1 (109 ms, recall 0.996) is slower than G = 10 (42.2 ms,
  recall 1.000), possibly because one group then covers the whole 10% pool, so each filtered ANN
  query is broad; needs the store's query traces.
- **Search engines and vector databases**: 11 to 99 times slower at 40,000 than at 1 group, most of
  the growth after 1,000 groups. The translator alone takes 31 to 49 ms at 40,000 (ES 31.2 of a
  78.8 ms p50; Redis 47.5 of 123), so a large part of the cost is building and shipping the filter.
- **Controls**: FAISS and memory grow 1.19 and 1.17 times (set lookups), as predicted.

## Library defects, vendor bugs and harness defects the run exposed

1. **Vendor (Chroma 1.5.9, embedded `EphemeralClient`)**: a `where` document holding a flat `$or` of
   about 40,000 clauses kills the client process with SIGSEGV, no exception and no message,
   reproducibly (5 of 5 processes: 2 smoke, 3 full). A client-supplied filter that crashes the host
   process is a denial-of-service bug worth disclosing to Chroma, with a minimal reproduction (one
   collection, a `$or` of 40,003 `$eq` clauses on distinct boolean keys). Related limitation: the
   refusal at about 1,000 clauses comes from SQLite's expression depth; rendering an n-ary `$or`
   as a balanced tree or an `IN` list would avoid it.
2. **Library (wardowl's Chroma translator)**: one `$eq` clause per group value in one flat `$or`
   means Chroma refuses every subject in about 1,000 or more groups and the application process dies
   at 40,000. The layer should refuse, before calling Chroma, any filter whose largest disjunction
   exceeds a safe clause count (failing closed with a clear error, or falling back to post-filtering
   as the Cassandra adapter does beyond 254 groups), and could nest the disjunction to stay under
   the depth limit (untested). The conformance campaign saw the depth error at 1,000 values; the
   crash at 40,000 is new.
3. **Analysis script (`x6_stats.py`, H6)**: the seeds mismatch above; every H6 part prints
   inconclusive whatever the data.
4. **Analysis script (`x6_stats.py`, H2(a) and H4 at m = 1,000)**: two-sided window where the text is
   one-sided; disclose, keep the printed verdicts.
5. **Harness (`x3_filter_scaling.py` driver)**: the fair share by target count skipped Chroma's seeds
   3 and 4 while the job ended three hours early.
6. **Harness (`x6_data.py`)**: far chunks reused when eligible passages ran out, against amendment 1.
7. **Harness (`size_of`)**: Weaviate's and Cassandra's translation sizes are string lengths of
   client objects.
8. **Pre-registration design**: G1 unreachable for the in-memory control at 60 clusters; G1 cannot
   detect build-to-build offsets; the grouped W0 confounds collection-statistics channels at small m.
9. **Store behaviour worth stating, not a bug**: pgvector's iterative scan returns better answers
   (recall 0.97 against 0.67 to 0.71) when unreadable rows crowd the query, and Qdrant's filtered
   traversal at 50% selectivity returned fewer than k hits for some probes when 1,000 unreadable
   points surrounded the query (W1 mean count 9.775). The paper's audit sentence "Qdrant never
   returned a short answer" is about the enterprise scenario and remains true there.

## Computations requested (not done here)

1. FAISS m = 1 and 10: paired `search_ms`, `authorize_ms` and `searches` per (seed, probe, p) from
   `x6-faiss.jsonl` (decides whether the H1(c) latency difference lies in the index search, in the
   layer, or in neither).
2. pgvector `pre-exact` on W1 and W0^g: plans and buffer counts for one probe, and whether VACUUM
   state differs (decides the build offset).
3. Per-probe hub counts within the first 1,000 ranks of each m = 1,000 probe (plan files of artifact
   `x3x6-data`), against the W1 counts (confirms the H1(a) mechanism probe by probe).
4. pgvector's 35 `explain` records from `x3-pgvector.jsonl` (X3 plans: node types, rows removed).
5. Chroma: one G = 40,000 query under `python -X faulthandler` or `gdb`, and a bisection between
   10,000 and 40,000; plus seeds 3 and 4 (`SEED_LIST=3-4`) to complete the pre-registered five.
6. A cross-build A/A (W0^g built twice) in any rerun of X6.

## What this means for the paper

- The three channels the design predicted exist and are large where predicted: widening latency at
  m = 100 (paired AUC 0.80 to 0.98 at p = 10% and 50%), the hit count at m = 1,000 when the attacker
  reads little (1.000 at p = 1%), pgvector's approximate pre-filter at m >= 100 (1.000), and BM25 or
  IDF scores at m >= 100 (0.98 to 1.00).
- They are weaker than predicted where readable content sits among the secrets (count at p = 50%:
  0.61 to 0.69, falsified), and BM25 at small m is not isolated by the grouped design.
- Exact pre-filtering returned identical answers in both worlds; its latency verdicts are
  inconclusive because of build offsets that do not depend on m.
- Constant-work widening removes the widening channel but leaves a reverse latency channel on
  pgvector (W1 faster in 98% of probes at m = 1,000).
- Padding to the slowest seed-0 answer removes every latency channel tested, at 1.3 to 27 times the
  mean latency; H6 must be reported with the script defect.
- X3: every store but Chroma accepts 40,000 groups with unchanged recall; latency grows up to 272
  times (pgvector); Chroma refuses from 1,000 groups and crashes the process at 40,000.

## Follow-up (2026-10-30): amendment 4, run 40982986417

The computations requested above were pre-registered as amendment 4 (written after these results
were seen) and run on GitHub Actions as run 40982986417; the full record is
`evidence/x3-x6-followup.md`. In short:

- Requests 1 to 5 ran in full; request 6 ran for FAISS, pgvector and Qdrant (see the last point).
  Chroma's seeds 3 and 4 complete X3: X3-H1 is now
  confirmed (84 of 84 parts), X3-H2 confirmed for Chroma (refuses in 5 seeds), X3-H4 for Chroma stays
  inconclusive by its rule; every other store's X3 tables reproduce this run's.
- The hub mechanism holds probe by probe: FAISS returned exactly min(10, readable hubs among the
  1,000 nearest) for all 40 m = 1,000 probes at every p (1 to 231 hubs, mean 45.7).
- FAISS's m = 1 difference lies wholly in FAISS's own search call, with equal widening rounds; two
  builds of the same content differ as much (cross-build A/A 0.361, age 0.600), but the reading fixed
  in advance prints inconclusive (matched content 0.447, interval 0.392 to 0.506).
- pgvector's `pre-exact` offset follows the vacuum state: the table built last before each group
  had no all-visible page at the group's start in 40 of 40 groups; vacuumed tables plan and run alike.
- Chroma crashes between 15,500 and 16,500 groups, inside `chromadb/api/rust.py` `_query`, with the
  main thread about 16,500 frames deep in one recursive function of its Rust bindings.
- Request 6 is partly missing: the Elasticsearch cross-build job was lost when its runner stopped
  responding, so Elasticsearch has no cross-build comparison.
