# X8 pre-registration: repeated end-to-end runs (written 2026-10-29, before any X8 run)

## What runs

The 2026-10-24 enterprise run (X0, seed 7) repeated with seeds 11, 13 and 17, so that four runs
exist in all, everything else identical: wardowl 2.1.0 from PyPI, acceptance scripts at commit
`bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839` (unchanged in `acceptance/kaggle/` and the Kaggle setup
scripts up to main 438a176 apart from the notebook's version cell), the notebook's default
configuration (nine stores, OPA and OpenFGA on pgvector, 208 variants, the full FiQA corpus,
bge-base-en-v1.5, Qwen2.5-3B-Instruct, k = 5 and 10), Kaggle GPU T4 x2 sessions
(the session type X0 ran on), one seed per session. Each
session runs a script kernel that performs the notebook's cells in order and continues past a failed
store, as the notebook does. The seed changes the generated document text, the question
sample and the order in which people ask; the permission templates and personas are fixed by the
scenario, so the runs repeat the layout with fresh documents and questions, not fresh layouts.

## Predictions

1. Safety: every run reports 0 unreadable hits, 0 canaries in chunks, prompts and answers, and 0
   violations for every configuration. Any leak falsifies the end-to-end claim.
2. Qdrant recall@10 stays low in every run: between 0.45 and 0.70 (X0: 0.561).
3. pgvector returns empty results to some least-privileged people in every run: between 3 and 25 of
   them (X0: 10).
4. Stores that X0 put at or above 0.94 recall@10 (Redis, Elasticsearch, OpenSearch) stay at or above
   0.90 in every run.
5. The model obeys every injected notice it retrieves in every run (X0: 482 of 482).

## Analysis

Per store, the mean and range of recall@5 and recall@10 over the runs (X0 included), the per-run
empty-result count, and the leak bound over all runs pooled per question (independent questions
across seeds): with zero leaks in n questions per configuration, the one-sided 95% bound is
1 - 0.05^(1/n). The OpenFGA configuration is reported separately if its server starts.

## Amendment 1 (written 2026-10-30, after the three X8 runs, before any run below)

**Finding that prompts it.** The pgvector + OpenFGA configuration did not start in X0 or in any X8
run. The cause is the harness, not the infrastructure: `openfga.log` in all three X8 runs ends in
`panic: configured request timeout (6s) cannot be lower than 'listObjectsDeadline' config (20s)`.
The acceptance script sets `OPENFGA_LIST_OBJECTS_DEADLINE` to 20 s (`FGA_DEADLINE`) and leaves the
request timeout at OpenFGA's default of 3 s, which OpenFGA 1.22.0 extends by 3 s for the HTTP
gateway and then rejects as shorter than the deadline (`pkg/server/config/config.go`,
`verifyDeadline`). The server exits; the harness waits 180 s for `/healthz` and records a timeout.
The X0 evidence file's "(infrastructure)" was wrong and is corrected there.

**What runs (X8-FGA).** The same pinned scripts (`bf25bd0`), wardowl 2.1.0, versions and session type
as above, with one change made outside the scripts: the runner sets `OPENFGA_REQUEST_TIMEOUT=25s`
in the environment before the store cell, which the harness passes to the server (`env =
{**os.environ, ...}`); OpenFGA's effective timeout becomes 28 s, above the 20 s deadline. Only the
pgvector store runs, with `remote_authorizers=("openfga",)`, so each run has two configurations:
pgvector with the in-process policy (a fifth and later sixth repeat of that configuration) and
pgvector + OpenFGA behind the caching authorizer. Seeds 7 (X0's), 11, 13 and 17, one per GPU T4 x2
session. Nothing else changes; no result of these runs replaces a result of
X0 or X8.

**Predictions.**

F1. OpenFGA starts and the harness writes every tuple, in all four runs.
F2. Safety: 0 unreadable hits, 0 canaries in chunks, prompts or answers, 0 violations and 0 errors
    for pgvector + OpenFGA in every run. Any leak falsifies the end-to-end claim for this engine.
F3. Every retrieval with OpenFGA uses the pre-filter: the most a person may read is about 1,665
    company documents (59,265 chunks less the 57,600 shared passages) plus the one knowledge-base
    document, under the 10,000-object limit, so no
    ListObjects answer should reach the limit. A post-filter strategy on any question would mean
    an answer reached the 20 s deadline or the limit, and is reported with the person.
F4. The pgvector in-process configuration in these runs again shows one of the two modes seen so
    far (recall@10 near 0.73 with p50 under 20 ms, or near 0.99 with p50 over 300 ms).

Recall, latency and the model's behaviour for pgvector + OpenFGA are reported without a
prediction: the filter is an `In` over up to about 1,665 resource ids (a median person about 1,040), a shape no earlier run
measured on pgvector.

**Analysis.** As above, per configuration; the leak bound for pgvector + OpenFGA over its own
questions (n = 4 x 1,105 if all four runs complete).

## Amendment 2 (written 2026-10-30, after the X8 and X8-FGA results and the critical review, before any run below)

**Status.** This amendment is written after the results of X0, X8 and X8-FGA were known and after
the critical review of 2026-10-30 (`reviews/review-critical-2026-10-30.md`, concern 3), and before
any run it describes. Its measurements are exploratory in the review's sense: specified in writing
after the main results and before running. No result below replaces a result of X0, X8 or X8-FGA.

**Why.** The four runs report no leak, but they do not show two things a reader needs to weigh
that: (i) that the questions came near content the asking person may not read, so that a broken
filter would have had something to return; and (ii) that the pipeline's leak detection fires when
enforcement is broken on purpose. Measurement 1 answers (i), measurement 2 answers (ii).

**What runs.** The pinned scripts (`bf25bd0`), wardowl 2.1.0 from PyPI, the same corpus parameters
(208 variants, all of FiQA), bge-base-en-v1.5, Qwen2.5-3B-Instruct, k = 5 and 10, Kaggle GPU T4 x2
sessions. Only FAISS runs (the backend's `IndexFlatIP`, exact, in process), so
no store server is started and the PostgreSQL setup script is not run. Everything added is in the
runner `kaggle/x8/x8b_run.py`, which imports the harness and changes nothing in it: a subclass of
`PermissionedRetriever` sets `recheck` and records each retrieval's result, and a wrapper around
the policy `AllOf(TenantAuthorizer(), MetadataACLAuthorizer())` replaces its `filter_for` while its
`check` stays the unmutated policy's.

**Measurement 1: exposure (seeds 7, 11, 13 and 17).** One kernel per seed (`x8b-seedNN`), no
language model. The harness builds the corpus, people, questions, embeddings and its oracle masks as
in X8. For every question, the exact top 5 and top 10 chunks over the whole corpus are computed from
the harness's own chunk and query vectors (inner product on the GPU, the harness's `_baseline`
computation without the readable-set mask). For each k: U_k is the number of those chunks the asking
person may not read by the harness's oracle (`readable`); C_k is the number of them in whose text the
harness's `LeakDetector` finds a canary of a document that person may not read. Reported per seed
and pooled over the four seeds (a CPU kernel, `x8b-pool`, reads the four outputs), per question
category (generic, targeted, forbidden, red team) and per person type (the persona's conventional
name, which fixes its groups: alice, bob, carol, dave, erin, frank, grace, heidi, ivan, judy,
mallory, peggy, trent): the share of questions with U_k >= 1, the mean of U_k, and the share with
C_k >= 1, for k = 5 and k = 10.

**Measurement 2: mutation positive control (seed 7 only).** One kernel (`x8b-control-seed7`), with
the language model; seed 7 is X0's seed. FAISS is loaded once and the harness's own
`Run.evaluate` runs seven passes over the same 1,105 questions (retrieval at k = 5 and 10, prompts,
answers, the oracle and canary checks, and the 20 questions timed end to end):

| Pass | Pre-filter given to the store | Re-check |
|---|---|---|
| P0 | the policy's filter, unmutated | on (as in X0 and X8) |
| M1-off | admits everything: `In("tenant", all 20 tenants)` | off |
| M2-off | second tenant: the tenant clause also admits the next tenant in the harness's list (northwind admits globex, ..., treyresearch admits northwind); the ACL clause unchanged | off |
| M3-off | ACL clause dropped: the tenant clause alone | off |
| M1-on, M2-on, M3-on | as M1, M2, M3 | on |

M1 is a filter that admits everything, M2 a tenant-boundary fault that over-admits the neighbouring
tenant's documents the person's groups or user id are named on, M3 an ACL fault inside the tenant.
With the re-check off, wardowl 2.1.0 still matches each hit against the filter it gave the store, so
it cannot see what a wrong filter over-admits; with the re-check on, the unmutated `check` removes
those hits and counts them as violations. For each mutation the kernel also reports how many chunks
the mutated filter admits that each person may not read (minimum, median, maximum over people).

Reported per pass: the harness's own counts and checks (hits checked, unreadable hits, canaries in
chunks, prompts and answers, violations, errors), and from the recorded retrievals, per question:
the questions with at least one unreadable hit at k = 5 and at k = 10, the distinct (question, chunk)
pairs among those hits, the questions with a canary in a retrieved chunk, in the prompt and in the
answer, and the violations, overall and per question category. The harness's counts include the 20
end-to-end questions and count a chunk returned at both k = 5 and k = 10 twice; the per-question
figures use the main retrievals only.

**Predictions.**

X1. P0 reproduces X0's FAISS safety row: 16,360 hits checked, 0 unreadable hits, 0 canaries in
    chunks, prompts and answers, 0 violations, 0 errors, recall@5 and recall@10 1.000.
X2. In M1-off, M2-off and M3-off, unreadable hits > 0, canaries in retrieved chunks > 0 and canaries
    in prompts > 0, so the harness's own leak checks fail; and violations = 0 in all three.
X3. Canaries in answers > 0 in M1-off and in M3-off. M2-off is reported without a prediction.
X4. In M1-on, M2-on and M3-on, violations > 0, and 0 unreadable hits and 0 canaries in chunks,
    prompts and answers.
X5. M1-off is unfiltered exact retrieval through the store, so for at least 99% of questions its
    k = 10 retrieval returns the same chunk ids as measurement 1's unfiltered top 10 for seed 7, and
    the per-question U_5 and U_10 agree for at least 99% of questions.
X6. In every seed, at least 90% of forbidden questions have an unreadable chunk in the unfiltered
    top 5, and at least 75% have an unreadable canary-bearing chunk there.
X7. In every seed, at least 90% of targeted questions and at least 90% of red-team questions have an
    unreadable chunk in the unfiltered top 5 (each company document has a counterpart from the same
    template and pool entry in each of the other 19 tenants, and each tenant's injected notice in
    the other 19).

Generic questions, the canary shares of targeted and red-team questions, and the per-type figures
are reported without predictions. A prediction that fails is reported as falsified; a kernel that
fails is reported with its log, and is rerun only if the failure is in the runner, with the fix
recorded here first.
