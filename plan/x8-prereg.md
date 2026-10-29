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
