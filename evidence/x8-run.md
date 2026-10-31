# Evidence: X8, repeated end-to-end runs (seeds 11, 13, 17)

Written 2026-10-30. Pre-registration: `plan/x8-prereg.md` (2026-10-29, before any X8 run).
Raw outputs: `evidence/raw/x8-seed11/`, `evidence/raw/x8-seed13/`, `evidence/raw/x8-seed17/`
(`results.md`, `results.json`, `answers.jsonl` with the k=5 hits and the answer per question, the model-answer
cache, the kernel log and the servers' logs, fetched with `kernels output`; `answers.jsonl` and the cache were added on
2026-10-31). The k=10 hit lists were not written by the harness, so recall@10 is a printed number
(`evidence/ARTIFACT_GAPS.md`). X0, the run being repeated, is `evidence/kaggle-scale-run-2026-10-24.md` (seed 7).

**Corrected 2026-10-31: the "people with no results" are empty answers.** The check "everyone who may read something got
results" (`enterprise_rag.py:2011-2016` at `bf25bd0`) counts one entry per question, not per person, and the wording in
this file and in the pre-registration took it for people. Counted from each run's `answers.jsonl`, as answers with no hits
where the exact baseline has hits (FAISS's row of the same person and question, or for X8-FGA, which has no FAISS pass,
leaving out mallory, the one person who may read nothing, whose 21 questions are empty in every store):

| Run | pgvector: empty answers / people | pgvector + OPA | pgvector + OpenFGA |
|---|---|---|---|
| X0, seed 7 | 10 / 9 | 10 / 9 | did not start |
| X8, seed 11 | 1 / 1 | 0 / 0 | did not start |
| X8, seed 13 | 0 / 0 | 0 / 0 | did not start |
| X8, seed 17 | 7 / 7 | 7 / 7 | did not start |
| X8-FGA, seed 7 | 1 / 1 | | 7 / 6 |
| X8-FGA, seed 11 | 1 / 1 | | 8 / 8 |
| X8-FGA, seed 13 | 0 / 0 | | 3 / 3 |
| X8-FGA, seed 17 | 0 / 0 | | 10 / 9 |

Nobody who may read something got an empty answer on every question: each of these people asked 5 questions and got hits
on 3 or 4 of them. So wherever this file says "people with no results" below, read "empty answers"; the table above gives
the people. The verdict on prediction 3 does not change: seeds 11 and 13 fall outside 3 to 25 in either unit.

## What ran

Script kernels `muzakkirhussain1/wardowl-x8-seed11`, `-seed13` and `-seed17`, one seed per Kaggle
GPU T4 x2 session (4 CPUs, 31.3 GiB), 2.9 to 3.3 hours each (the last `time` field of each kernel log: 11,773, 11,144 and
10,356 s). wardowl 2.1.0 from PyPI, acceptance scripts at
`bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839`, PostgreSQL 16.15 with pgvector 0.8.7, the notebook's
default configuration. Every run: 107,540 chunks (49,920 company documents in 20 tenants, 41,600 with
a canary; 20 injected notices; 57,600 FiQA passages), 189 people, 1,105 questions (108 generic,
376 targeted, 189 forbidden, 432 red team), readable chunks per person min 0, median 58,641, max
59,265. The seed changes the document text, the question sample and the asking order; the
permission templates and personas are fixed by the scenario.

## Outcomes per run

| Run | Checks passed / failed | Failed checks |
|---|---|---|
| X0, seed 7 | 87 / 3 | pgvector empty results (10 answers, 9 people); pgvector + OPA the same 10; OpenFGA did not start |
| seed 11 | 88 / 2 | pgvector empty results (1 answer: tailspin-judy); OpenFGA did not start |
| seed 13 | 89 / 1 | OpenFGA did not start |
| seed 17 | 87 / 3 | pgvector empty results (7 answers, 7 people, all "judy" personas); pgvector + OPA the same 7; OpenFGA did not start |

"OpenFGA did not start": `http://127.0.0.1:18080/healthz did not answer within 180 s`, in all four
runs. The cause is the harness: each X8 run's `openfga.log` ends in `panic: configured request
timeout (6s) cannot be lower than 'listObjectsDeadline' config (20s)`. The acceptance script sets
the ListObjects deadline to 20 s and leaves OpenFGA's request timeout at its default, which OpenFGA
1.22.0 rejects at start-up. The configuration is excluded from these runs and rerun with the timeout
raised (X8-FGA, `plan/x8-prereg.md`, amendment 1, pre-registered 2026-10-30 before the runs).

## Safety

| Run | Configurations | Questions | Hits checked | Unreadable hits | Canaries (chunk/prompt/answer) | Violations | Errors |
|---|---|---|---|---|---|---|---|
| X0, seed 7 | 10 | 11,050 | 163,236 | 0 | 0/0/0 | 0 | 0 |
| seed 11 | 10 | 11,050 | 163,585 | 0 | 0/0/0 | 0 | 0 |
| seed 13 | 10 | 11,050 | 163,591 | 0 | 0/0/0 | 0 | 0 |
| seed 17 | 10 | 11,050 | 163,226 | 0 | 0/0/0 | 0 | 0 |
| **All four** | 10 | **44,200** | **653,638** | **0** | **0/0/0** | **0** | **0** |

Hits checked per configuration over the four runs: FAISS, Chroma, Qdrant, Elasticsearch, OpenSearch,
Weaviate, Redis and LanceDB 65,440 each (16,360 per run); pgvector 65,047 (16,178 + 16,345 + 16,351
+ 16,173); pgvector + OPA 65,071 (16,178 + 16,360 + 16,360 + 16,173).

**Leak bound (pre-registered analysis).** Zero leaks in n = 4 x 1,105 = 4,420 questions per
configuration; the pre-registered analysis treats them as independent. One-sided 95% bound:
1 - 0.05^(1/4420) = 6.8 x 10^-4 leaks per question, for each configuration (X0 alone: 2.7 x 10^-3).

**Corrected 2026-10-31: the questions are not all sampled afresh.** Recounted from the four `answers.jsonl`
(X0 and X8), for every configuration: 3,746 distinct (person, question) pairs, of which 216 are in all four
seeds, 26 in two and 3,504 in one. Taken as independent they give 1 - 0.05^(1/3746) = 8.0 x 10^-4 per question,
the figure the paper reports; it gives 6.8 x 10^-4 once, as the pre-registered figure.

Per person the bound stays per run,
1 - 0.05^(1/189) = 1.6 x 10^-2: the 189 personas repeat across seeds with the same permissions, so a
fault tied to a permission shape would recur, and pooling person-runs would overstate independence.

**The canary matcher.** `LeakDetector` (`enterprise_rag.py:668-690` at `bf25bd0`) matches each canary
`WO-` plus ten hex digits (`canary_for`, a SHA-256 prefix of the document id, 40 bits) in any case,
with the ASCII hyphen, any Unicode hyphen or dash, spaces or nothing between the parts. A positive
control (`:1726-1731`) builds one text holding every canary and checks, for every person, that the
detector finds exactly the canaries of the documents that person may not read.

## Retrieval quality across the four runs

Recall against exact search over each person's readable set, ties within 1e-4 credited.

| Store | R@5 X0 / 11 / 13 / 17 | mean | R@10 X0 / 11 / 13 / 17 | mean | p50 ms X0 / 11 / 13 / 17 |
|---|---|---|---|---|---|
| FAISS (exact) | 1.000 / 1.000 / 1.000 / 1.000 | 1.000 | 1.000 / 1.000 / 1.000 / 1.000 | 1.000 | 346 / 355 / 368 / 356 |
| Chroma | 0.887 / 0.879 / 0.864 / 0.879 | 0.877 | 0.883 / 0.880 / 0.873 / 0.880 | 0.879 | 1442 / 1481 / 1444 / 1432 |
| pgvector | 0.691 / 0.992 / 0.994 / 0.700 | bimodal | 0.732 / 0.992 / 0.994 / 0.732 | bimodal | 6.5 / 398.7 / 386.0 / 8.1 |
| pgvector + OPA | 0.691 / 1.000 / 1.000 / 0.700 | bimodal | 0.732 / 1.000 / 1.000 / 0.732 | bimodal | 7.3 / 407.6 / 389.5 / 8.5 |
| Qdrant | 0.564 / 0.534 / 0.569 / 0.560 | 0.557 | 0.561 / 0.535 / 0.561 / 0.549 | 0.552 | 4.3 / 4.7 / 4.7 / 4.6 |
| Elasticsearch | 0.948 / 0.929 / 0.952 / 0.938 | 0.942 | 0.948 / 0.940 / 0.959 / 0.948 | 0.949 | 8.1 / 8.6 / 8.8 / 8.4 |
| OpenSearch | 0.947 / 0.942 / 0.942 / 0.939 | 0.942 | 0.938 / 0.936 / 0.933 / 0.934 | 0.935 | 6.8 / 7.0 / 7.1 / 6.9 |
| Weaviate | 0.888 / 0.902 / 0.908 / 0.899 | 0.899 | 0.892 / 0.902 / 0.913 / 0.902 | 0.902 | 7.1 / 8.0 / 8.0 / 7.8 |
| Redis | 0.985 / 0.980 / 0.995 / 0.971 | 0.983 | 0.980 / 0.982 / 0.988 / 0.976 | 0.981 | 28.3 / 30.4 / 30.4 / 29.6 |
| LanceDB | 0.833 / 0.832 / 0.861 / 0.835 | 0.840 | 0.860 / 0.866 / 0.899 / 0.871 | 0.874 | 22.4 / 24.7 / 24.8 / 24.9 |

Every store except pgvector repeats within a narrow band: the largest range of recall@10 is
LanceDB's 0.039 (0.860 to 0.899), Qdrant's is 0.026.

**pgvector is bimodal across runs, with the same configuration.** Two runs (X0 and seed 17) ran
fast and lossy: recall@10 0.732, p50 6.5 and 8.1 ms, 10 and 7 least-privileged people with no
results. Two runs (seeds 11 and 13) ran exact and slow: recall@10 0.992 and 0.994, p50 399 and
386 ms, 1 and 0 people with no results. The mode was fixed from the first questions: seed 17
retrieved 250 questions in 8 s, seeds 11 and 13 in 172 s and 162 s (kernel logs). The load and
index times were alike in all four runs (62.8 to 65.6 s and 26.9 to 28.9 s), and in the three X8
runs the questions began between 92 and 96 s after the pgvector load started (X0's log timings were
not kept). This matches the plan-cache mechanism of
`investigations/x0-x1-pgvector-gap.md`: through psycopg's prepared statements PostgreSQL either keeps
custom plans, which use the HNSW index with the iterative-scan budget, or switches to a generic plan
that reads the GIN index and sorts, which is exact. Within a run, pgvector + OPA ran on the same
table and pool after the plain pass and stayed in the same mode; in the exact runs it reached 1.000,
since its statements were already generic from the first question. X1 run 2 records the executed
plans and the index state to settle what decides the switch.

## The model

| Run | Configurations reporting | Injected notices retrieved | Obeyed | Per configuration |
|---|---|---|---|---|
| X0, seed 7 | 10 | 498 | 498 | 7 to 106 |
| seed 11 | 10 | 741 | 741 | 11 to 117 |
| seed 13 | 10 | 768 | 768 | 3 to 112 |
| seed 17 | 10 | 652 | 652 | 1 to 108 |
| **All four** | | **2,659** | **2,659** | 1 to 117 |

(Corrected 2026-10-31: the X0 row left out pgvector + OPA, 16 of 16, and read 9 configurations, 482; X0's `results.md`
has 10 rows and 498. With the 426 of X8-FGA, whose four runs give 137, 62, 110 and 117 over both configurations, the eight
runs sum to 3,085 of 3,085.)

FAISS: target document in the top five for every targeted question in all four runs; answer
accuracy 0.984 to 0.997. Qdrant: target in the top five for 0.338 to 0.399 of targeted questions.
Abstained when a person asked about a document they may not read: 0.681 to 0.805 over all stores and
runs.

## Verdicts on the pre-registered predictions

1. **Safety, holds.** 0 unreadable hits, 0 canaries in chunks, prompts or answers, 0 violations and
   0 errors in every configuration of every run.
2. **Qdrant recall@10 between 0.45 and 0.70 in every run, holds.** 0.535, 0.561 and 0.549.
3. **pgvector returns no results to between 3 and 25 people in every run, falsified.** Seed 17: 7
   (inside). Seed 11: 1 and seed 13: 0 (outside). The prediction assumed X0's mode was a property of
   the configuration; the runs show two modes, and the count falls inside the range only in the fast
   mode.
4. **Redis, Elasticsearch and OpenSearch at or above 0.90 recall@10 in every run, holds.** Lowest:
   OpenSearch 0.933 (seed 13).
5. **The model obeys every retrieved injected notice, holds.** 2,161 of 2,161 in the three X8 runs
   (2,659 of 2,659 with X0).

## X8-FGA (amendment 1)

Kernels `muzakkirhussain1/wardowl-x8fga-seed7`, `-seed11`, `-seed13`, `-seed17` (2026-10-29 and 30,
GPU T4 x2, 0.6 to 0.9 hours each by the last `time` field of each kernel log: 3,418, 2,116, 3,269 and 3,219 s), pushed after the amendment's commits (ba64c23, 1a25086). Raw outputs:
`evidence/raw/x8fga-seedNN/` (`results.md`, `results.json`, `answers.jsonl`, the model-answer cache, kernel log,
`openfga.log`).

OpenFGA started in every run (its log holds only the three start-up warnings about disabled
authentication and TLS) and the harness wrote 74,960 tuples in 109 to 119 s each time.

| Seed | Configuration | Hits checked | Unreadable / canaries / violations / errors | Recall@5 | Recall@10 | p50 / p95 ms | No results for |
|---|---|---|---|---|---|---|---|
| 7 | pgvector | 16,341 | 0 / 0 / 0 / 0 | 0.994 | 0.993 | 391.4 / 427.3 | 1 (coho-judy) |
| 7 | pgvector + OpenFGA | 16,160 | 0 / 0 / 0 / 0 | 0.732 | 0.758 | 38.3 / 94.0 | 7 judys |
| 11 | pgvector | 16,345 | 0 / 0 / 0 / 0 | 0.724 | 0.746 | 16.8 / 433.1 | 1 (tailspin-judy) |
| 11 | pgvector + OpenFGA | 16,232 | 0 / 0 / 0 / 0 | 0.667 | 0.693 | 42.5 / 102.1 | 8 judys |
| 13 | pgvector | 16,359 | 0 / 0 / 0 / 0 | 0.984 | 0.987 | 413.4 / 453.8 | 0 |
| 13 | pgvector + OpenFGA | 16,268 | 0 / 0 / 0 / 0 | 0.685 | 0.714 | 44.7 / 97.4 | 3 judys |
| 17 | pgvector | 16,360 | 0 / 0 / 0 / 0 | 0.995 | 0.996 | 380.3 / 417.6 | 0 |
| 17 | pgvector + OpenFGA | 16,185 | 0 / 0 / 0 / 0 | 0.701 | 0.735 | 37.0 / 90.9 | 10 judys |

Every retrieval used the pre-filter (1,105 of 1,105 per configuration and run). Model, pgvector +
OpenFGA: injected notices retrieved and obeyed 41/41, 22/22, 16/16 and 21/21 (100 of 100); target in
the top five 0.942 to 0.979; answer accuracy 0.936 to 0.976; abstained when denied 0.732 to 0.833.
Permission cache: 7,603 to 7,797 hits and 10,729 to 10,847 misses per run.

**Verdicts.**

- F1, OpenFGA starts and every tuple is written: **holds** in all four runs.
- F2, safety for pgvector + OpenFGA: **holds**. 0 unreadable hits, canaries, violations and errors in
  64,845 checked hits over 4,420 questions; one-sided 95% bound 1 - 0.05^(1/4420) = 6.8 x 10^-4 per
  question as pre-registered, 8.0 x 10^-4 on the 3,746 distinct pairs (see the correction above).
- F3, every OpenFGA retrieval pre-filtered: **holds** (no ListObjects answer reached the limit or
  the deadline).
- F4, pgvector shows one of the two known modes: **holds as worded**, with a caveat. Seeds 7, 13 and
  17 ran exact (recall@10 0.987 to 0.996, p50 380 to 413 ms). Seed 11 ran fast by its median (p50
  16.8 ms, recall@10 0.746) but its p95 of 433 ms shows that part of its searches ran exact: a
  mixture within one run, which the plan-cache mechanism allows (the decision is per statement and
  connection).

**What the repeats add about pgvector's modes.** The same seed does not give the same mode: seed 7
ran fast in X0 and exact here; seed 11 exact in X8 and mostly fast here; seed 17 fast in X8 and exact
here. Over the eight runs of the in-process pgvector configuration, three ran fast by their median
(X0, X8 seed 17, X8-FGA seed 11) and five exact. The mode is decided at run time, not by the data.

**pgvector + OpenFGA is stable and lossy.** Unlike the in-process configuration, the OpenFGA
configuration gave the same picture in all four runs, whatever mode the in-process pass had just
run in: recall@10 0.693 to 0.758, p50 37 to 45 ms, and 3 to 10 least-privileged people with no
results. Its filter is the tenant clause and an `In` over the resource ids OpenFGA lists (up to about
1,665); above 100 values wardowl sends the list as array
parameters that the GIN index cannot serve (`pgvector.py`, `MANY_VALUES`), so no plan can use the
index for that clause and the search runs through the HNSW iterative scan with its tuple budget
[inference from the code and X3's pgvector result; the plans were not recorded in these runs].
Answer quality held up better than recall (target in the top five 0.94 to 0.98).

## Consequences for the paper

- Section 9 (`e2e.tex`): four runs, 653,638 checked hits, no leak; bound 8.0 x 10^-4 per question
  per configuration (corrected from 6.8 x 10^-4, see above); the run-to-run table; the matcher description replaces the paraphrase
  placeholder; injection totals.
- Section 6 (`quality.tex`): X0's single-run pgvector number must not be reported as a property of
  the configuration; report both modes with their frequency (2 of 4) and the mechanism.
- Abstract and introduction: recall@10 over the four runs ranges from 0.535 (Qdrant, seed 11) to
  1.000, and the pgvector line changes to the bimodal statement.
