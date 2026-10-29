# X8 pre-registration: repeated end-to-end runs (written 2026-10-29, before any X8 run)

## What runs

The 2026-10-24 enterprise run (X0, seed 7) repeated with seeds 11, 13 and 17, so that four runs
exist in all, everything else identical: wardowl 2.1.0 from PyPI, acceptance scripts at commit
`bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839` (unchanged in `acceptance/kaggle/` and the Kaggle setup
scripts up to main 438a176 apart from the notebook's version cell), the notebook's default
configuration (nine stores, OPA and OpenFGA on pgvector, 208 variants, the full FiQA corpus,
bge-base-en-v1.5, Qwen2.5-3B-Instruct, k = 5 and 10), Kaggle GPU T4 x2 sessions on the account
muzakkirhussain1 (X0 ran on muzakkirhussainsyed; same session type), one seed per session. Each
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
session on muzakkirhussain1. Nothing else changes; no result of these runs replaces a result of
X0 or X8.

**Predictions.**

F1. OpenFGA starts and the harness writes every tuple, in all four runs.
F2. Safety: 0 unreadable hits, 0 canaries in chunks, prompts or answers, 0 violations and 0 errors
    for pgvector + OpenFGA in every run. Any leak falsifies the end-to-end claim for this engine.
F3. Every retrieval with OpenFGA uses the pre-filter: the most a person may read is about 1,040
    company documents plus the one knowledge-base document, under the 10,000-object limit, so no
    ListObjects answer should reach the limit. A post-filter strategy on any question would mean
    an answer reached the 20 s deadline or the limit, and is reported with the person.
F4. The pgvector in-process configuration in these runs again shows one of the two modes seen so
    far (recall@10 near 0.73 with p50 under 20 ms, or near 0.99 with p50 over 300 ms).

Recall, latency and the model's behaviour for pgvector + OpenFGA are reported without a
prediction: the filter is an `In` over up to about 1,040 resource ids, a shape no earlier run
measured on pgvector.

**Analysis.** As above, per configuration; the leak bound for pgvector + OpenFGA over its own
questions (n = 4 x 1,105 if all four runs complete).
