# Reproducing the paper

This file goes from a claim in the paper to the data and code behind it. Written 2026-10-31. Every path below was opened
in a build of the tag `evidence-v1` made with `.github/workflows/evidence-tag.yml`, or on the public library at the stated
commit; paths under `harness/`, `evidence/raw/ci-artifacts/` and `evidence/raw/results-*/` exist only in the tag, not on
`main`. What is missing is in `evidence/ARTIFACT_GAPS.md`.

**The author develops wardowl, and nobody independent has rerun any of this.** The author did not rerun the experiments
for this file either. Section 3 says what it would take. What was rechecked is listed in section 4.

## 1. From a table or figure to its data

The main text names experiments by what they do; the codes are defined in the paper's Appendix A. One row per table or
figure, in the order of the paper. The labels are the LaTeX labels in `paper/sections/`. Numbers come from the data file as
printed by the script unless a row says otherwise.

Short names used in the table:

- `E2E` = `harness/x0-x8-bf25bd0/acceptance/kaggle/enterprise_rag.py`, the end-to-end scenario.
- `X25` = `evidence/raw/results-x2-x5/40921769714-1/stats/`, the statistics of X2 and X5.
- `X36` = `evidence/raw/results-x3-x6/40940385704-1/reports/`, the statistics of X3 and X6.
- `FU` = `evidence/raw/results-x3-x6/40982986417-1/reports/`, the follow-up to X3 and X6.
- `X47` = `evidence/raw/results-x4-x7/40919304635-1/`, the statistics of X4 and X7.
- `X7A` = `evidence/raw/results-x4-x7/40969846593-1/`, the rerun of X7 (amendment 2).
- `S1` = `evidence/raw/x1run2-stats/x1run2-stats/`, the statistics of X1 run 2.

### Main text

| Paper item | Run | Script | Data | Summary |
|---|---|---|---|---|
| `tab:conf-findings`, this paper's findings on stores and engines | Conformance runs 40313285885, 40905549149; vendor reproducers | `harness/conformance-run2-182bcbc/benchmarks/paper/conformance_campaign.py`, kit `harness/conformance-run2-182bcbc/wardowl/testing.py`; `disclosure/reproducers/` | `evidence/raw/ci-artifacts/40905549149/conformance-summary.zip`, `evidence/raw/ci-artifacts/40313285885/conformance-summary.zip`; `evidence/raw/results-reproducers/runs/41008151303/` | `evidence/conformance-campaign-run1.md`, `evidence/conformance-campaign-run2.md`, `disclosure/redis.md`, `disclosure/mongodb.md`, `disclosure/chroma.md`, `disclosure/cerbos.md` |
| `tab:eng-revoke`, revocation delay | X7, 40919304635 | `harness/x4-x7-e66dffc/benchmarks/paper/x7_revocation_faults.py`, `harness/x4-x7-e66dffc/benchmarks/paper/x7_stats.py` | `X47` `x7a_revocation.csv`; raw `evidence/raw/ci-artifacts/40919304635/x4x7-x7a-acl.zip` and its siblings `x4x7-x7a-*.zip` | `evidence/x4-x7-run1.md`; the fixes tested, `evidence/x7-amendment2.md` with `X7A` `x7a_revocation.csv` |
| `fig:qual-audit`, recall@10 per store, four runs | X0, X8 | `E2E`; `kaggle/x8/x8_run.py` | `evidence/raw/x0-seed7/results.json`, `evidence/raw/x8-seed11/results.json`, `evidence/raw/x8-seed13/results.json`, `evidence/raw/x8-seed17/results.json`, field `recall@10`. Printed only: no run stored its k=10 hits | `evidence/x8-run.md`, "Retrieval quality across the four runs" |
| `fig:qual-frontiers`, recall against throughput on MS MARCO | X2, 40921769714 | `harness/x2-x5-884ce18/benchmarks/paper/x2_frontiers.py`, `harness/x2-x5-884ce18/benchmarks/paper/x2x5_stats.py` | `X25` `x2_frontier.csv` (cell `all`; QPS from build 0, recall the mean of three builds); rows `evidence/raw/ci-artifacts/40921769714/x2x5-res-x2-m-pgvector-b0.zip` and its siblings | `evidence/x2-x5-run1.md`, "Frontier data" |
| `tab:rep-summary`, repair | X5, 40921769714 | `harness/x2-x5-884ce18/benchmarks/paper/x5_mitigation.py`, `harness/x2-x5-884ce18/benchmarks/paper/x2x5_stats.py` | `X25` `x5_arms.csv`; rows `evidence/raw/ci-artifacts/40921769714/x2x5-res-x5-m-pgvector-b0.zip` and its siblings, members `rows/*.jsonl.gz` | `evidence/x2-x5-run1.md`, "X5 arms" |
| `fig:side-auc`, paired AUC against the number of documents | X6, 40940385704 | `harness/x3-x6-a191626/benchmarks/paper/x6_side_channels.py`, `harness/x3-x6-a191626/benchmarks/paper/x6_stats.py` | `X36` `x6_cells.csv`, `x6_report.md`; same-content ranges `FU` `fu_crossbuild_cells.csv`; records `evidence/raw/ci-artifacts/40940385704/x3x6-results-x6-faiss.zip` and its siblings, member `x6-<store>.jsonl`. The paper's $W_0^g$ is the slot `W0` in the data | `evidence/x3-x6-run1.md`, "Exploratory: all paired AUCs"; `evidence/x3-x6-followup.md` |

### Appendices

| Paper item | Run | Script | Data | Summary |
|---|---|---|---|---|
| `tab:app-map`, the experiments | All | | GitHub API for run times and head commits; `harness/COMMITS.tsv`; `evidence/raw/KAGGLE_KERNELS.tsv` | `evidence/compute.md`, section 2 below |
| `tab:app-ledger`, every hypothesis | All | | `plan/x8-prereg.md`; `harness/x1-run2-a956424/benchmarks/paper/PREREGISTRATION.md`, `harness/x2-x5-884ce18/benchmarks/paper/PREREG_X2_X5.md`, `harness/x3-x6-followup-9e22b89/benchmarks/paper/PREREG_X3_X6.md`, `harness/x4-x7-e66dffc/benchmarks/paper/PREREG_X4_X7.md`, with amendment 2 in `harness/x7-amendment2-harness-41292bd/benchmarks/paper/PREREG_X4_X7.md`; verdicts in the summaries of each run | The `evidence/*.md` files; the weakness of the Kaggle ordering is in `evidence/ARTIFACT_GAPS.md` |
| `tab:sys-precedents`, components and precedents | None | | `bib/references.bib`, `bib/web.bib`; the library at `harness/x0-x8-bf25bd0/wardowl/` | `literature/Permission aware retrieval literature review.md` |
| `tab:conf-faults`, faults and semantic gaps | Conformance runs; other rows as cited | `harness/conformance-run2-182bcbc/tests/test_testing_kit.py` for planted faults | `harness/conformance-run2-182bcbc/CHANGELOG.md`, `harness/conformance-run2-182bcbc/docs/review.md`; `evidence/raw/results-reproducers/runs/41008151303/` | `investigations/conformance-run1-triage.md`, `evidence/x3-x6-run1.md`, `evidence/x4-x7-run1.md`, `evidence/x7-amendment2.md` |
| `tab:eng-agree`, filter against check | X4, 40919304635 | `harness/x4-x7-e66dffc/benchmarks/paper/x4_engines.py`, `harness/x4-x7-e66dffc/benchmarks/paper/x4_stats.py` | `X47` `x4a_profiles.csv`; raw `X47` `raw/`, `evidence/raw/ci-artifacts/40919304635/x4x7-x4-policy.zip` and its siblings | `evidence/x4-x7-run1.md` |
| `tab:qual-x0`, retrieval quality in the scenario | X0, X8; re-analysis in X1 run 1 | `E2E`; `harness/x1-run1-947fb8f/benchmarks/paper/x0_reanalysis.py` | `results.json` of `evidence/raw/x0-seed7/` and `evidence/raw/x8-seed*/`; overlap@5 `evidence/raw/x1-run1/x0/recall5_by_person_type.csv` | `evidence/x8-run.md`, `evidence/x1-underretrieval-run1.md` |
| `tab:qual-qdrant`, Qdrant under permission filters | X1 run 2; run 1 for the comparison | `harness/x1-run2-a956424/benchmarks/paper/x1_underretrieval.py`, `harness/x1-run2-a956424/benchmarks/paper/x1_stats.py`, `harness/x1-run2-a956424/benchmarks/paper/x1_run2_kaggle.py`; kernels `kaggle/x1run2/` | `S1` `summary_by_setting.csv`, `summary_by_build.csv`; per-question rows with hits at k=5 and k=10, `evidence/raw/x1run2-shard-c/x1run2/runs/qdrant__*.parquet`; run 1, `evidence/raw/x1-run1/x1/stats/` | `evidence/x1-underretrieval-run2.md` |
| Text of `sec:qual-pgvector` and the appendix grid `app:x1grid` | X1 run 2 | As above | `S1` `summary_by_setting.csv`, `plans.csv`, `explain_summary.csv`, `predictions.csv`, `intervals.csv`, `paired.csv`, `report.md`; rows `evidence/raw/x1run2-shard-a/x1run2/runs/`, `evidence/raw/x1run2-shard-b/x1run2/runs/`, `evidence/raw/x1run2-shard-c/x1run2/runs/`; plans `evidence/raw/x1run2-shard-a/x1run2/explain/`, `evidence/raw/x1run2-shard-a/x1run2/explain_raw/` | `evidence/x1-underretrieval-run2.md`, `investigations/x0-x1-pgvector-gap.md` |
| `tab:qual-frontiers`, X2 on MS MARCO | X2, 40921769714 | As `fig:qual-frontiers` | `X25` `x2_settings.csv`, `x2_frontier.csv`, `x2_builds.csv` | `evidence/x2-x5-run1.md` |
| `tab:qual-x2tests`, X2's statistics | X2, 40921769714 | `harness/x2-x5-884ce18/benchmarks/paper/x2x5_stats.py` | `X25` `x2_h21.csv`, `x2_h22.csv`, `x2_h23.csv`, `x2_h24.csv`, `x2_axes.csv` | `evidence/x2-x5-run1.md` |
| `tab:qual-size`, filter size | X3, 40940385704; Chroma's seeds 3 and 4 from the follow-up, 40982986417 | `harness/x3-x6-a191626/benchmarks/paper/x3_filter_scaling.py`, `harness/x3-x6-a191626/benchmarks/paper/x3_stats.py`, `harness/x3-x6-followup-9e22b89/benchmarks/paper/x3x6_followup.py` | `X36` `x3_levels.csv`, `x3_ratios.csv`, `x3_recall.csv`, `x3_verdicts.csv`; records `evidence/raw/ci-artifacts/40940385704/x3x6-results-x3-search.zip` and its siblings; `evidence/raw/ci-artifacts/40982986417/x3x6-results-fu-x3-chroma.zip` | `evidence/x3-x6-run1.md`, `evidence/x3-x6-followup.md` |
| `tab:rep-results`, X5, all arms | X5, 40921769714 | As `tab:rep-summary` | `X25` `x5_arms.csv`, `x5_confusion.csv`, `x5_paired_tests.csv` | `evidence/x2-x5-run1.md` |
| `tab:side-hyp`, side-channel hypotheses | X6, 40940385704 | `harness/x3-x6-a191626/benchmarks/paper/PREREG_X3_X6.md`, `harness/x3-x6-a191626/benchmarks/paper/x6_stats.py` | `X36` `x6_verdicts.csv`, `x6_report.md`. Where the script departs from the written rules, the paper's text says so | `evidence/x3-x6-run1.md` |
| `tab:side-auc`, paired AUC | X6, 40940385704 | `harness/x3-x6-a191626/benchmarks/paper/x6_stats.py` | `X36` `x6_report.md`, `x6_cells.csv`; records as `fig:side-auc` | `evidence/x3-x6-run1.md` |
| `tab:e2e-safety`, safety over four runs | X0, X8, X8-FGA | `E2E`; `kaggle/x8/x8_run.py`, `kaggle/x8/x8fga_run.py` | `results.md` and `results.json` of `evidence/raw/x0-seed7/`, `evidence/raw/x8-seed*/`, `evidence/raw/x8fga-seed*/`; per question, `answers.jsonl` in the same folders, with k=5 hits only | `evidence/x8-run.md` |
| `tab:e2e-exposure`, exposure | X8 amendment 2 | `kaggle/x8/x8b_run.py`; kernels `kaggle/x8/x8b-seed7/` and its siblings, `kaggle/x8/x8b-pool/` | `evidence/raw/x8b-pool/x8b-exposure-pooled.md`, `evidence/raw/x8b-pool/x8b-exposure-pooled.json`; per seed and question, `evidence/raw/x8b-seed7/x8b-exposure-seed7.json` and its siblings | `evidence/x8-controls.md` |
| `tab:e2e-control`, the mutation control | X8 amendment 2, seed 7 | `kaggle/x8/x8b_run.py`, `kaggle/x8/x8b-control-seed7/`; recount `kaggle/x8/x8b-verify/` | `evidence/raw/x8b-control-seed7/x8b-control-seed7.md`, per question `evidence/raw/x8b-control-seed7/x8b-control-seed7-questions.json`; recount `evidence/raw/x8b-verify/x8b-verify.md` | `evidence/x8-controls.md` |
| `tab:limits-rls`, row-level security against the pre-filter | The library's own benchmark of 2026-10-22, before this paper's experiments and not pre-registered | `harness/rls-side-run-42fcca6/benchmarks/kaggle_benchmark.ipynb`, `harness/rls-side-run-42fcca6/benchmarks/permissions_bench.py` | `harness/x0-x8-bf25bd0/benchmarks/results/fiqa-row-level-security.md`, `harness/x0-x8-bf25bd0/benchmarks/results/fiqa-qwen3-embedding-0.6b.md`. Summaries only; the run's raw output is not in the archive | The results files above |
| `tab:app-x0-settings`, store settings | X0, X8 | `harness/x0-x8-bf25bd0/benchmarks/kaggle_setup.sh`, `harness/x0-x8-bf25bd0/benchmarks/kaggle_stores.sh`, `E2E` | `results.md`, section on stores, in `evidence/raw/x0-seed7/` and `evidence/raw/x8-seed*/` | `investigations/filtered-recall-gaps.md` |
| `tab:app-compute`, compute | All | | GitHub jobs API; last `time` field of each kernel log in `evidence/raw/` | `evidence/compute.md` |

## 2. Runs, versions and where each came from

`harness/COMMITS.tsv` gives the full commit hash of every folder under `harness/`. The GitHub runs are in the public
library's Actions, `https://github.com/muzakkirhussain011/wardowl/actions/runs/<id>`; the API's `head_sha` and `created_at`
are the trustworthy times.

| Code | Where it ran | Commit folder | Run ids | How it ended |
|---|---|---|---|---|
| X0 | Kaggle, public notebook `muzakkirhussainsyed/wardowl-end-to-end-scale-run-seed-7` (code in `kaggle/x0/`) | `harness/x0-x8-bf25bd0/` | Kaggle script version 361900948 | 87 checks passed, 3 failed: the failures are findings |
| X1 run 1 | Kaggle, public notebook `muzakkirhussainsyed/wardowl-under-retrieval-diagnosis-run-1` (code in `kaggle/x1-run1/`) | `harness/x1-run1-947fb8f/` | Kaggle script version 362442153 | Completed; 12 pgvector items skipped at the deadline |
| X1 run 2 | Kaggle, private kernels `muzakkirhussain1/x1run2-prep-gpu`, `-shard-a`, `-shard-b`, `-shard-c`, `-stats` (code in `kaggle/x1run2/`) | `harness/x1-run2-a956424/` | See `evidence/raw/KAGGLE_KERNELS.tsv` | Completed |
| X2, X5 | GitHub-hosted | `harness/x2-x5-884ce18/` | 40921769714 | `cancelled`: job `x2-m-chroma-b2` ended at the runner's job timeout, and the workflow published the rest (`evidence/compute.md`, `evidence/x2-x5-run1.md`) |
| X3, X6 | GitHub-hosted | `harness/x3-x6-a191626/` | 40940385704 | `success`; Chroma's X3 job crashed on seeds 0 to 2 at 40,000 groups and skipped seeds 3 and 4, a finding; the follow-up ran those seeds |
| Follow-up to X3, X6 | GitHub-hosted | `harness/x3-x6-followup-9e22b89/` | 40982986417 | `failure`: job `fu-cb-elasticsearch` lost its runner, so Elasticsearch's part is missing (`evidence/compute.md`) |
| X4, X7 | GitHub-hosted | `harness/x4-x7-e66dffc/` (its `wardowl/` is identical to `fix/engine-limits` at e7776f0) | 40919304635 | `success` |
| X7 amendment 2 | GitHub-hosted | Harness `harness/x7-amendment2-harness-41292bd/`, library `harness/x7-amendment2-library-3c6559f/` | 40969846593 | `success` |
| X8 | Kaggle, private kernels `muzakkirhussain1/wardowl-x8-seed11`, `-seed13`, `-seed17` (code in `kaggle/x8/`) | `harness/x0-x8-bf25bd0/` | See `evidence/raw/KAGGLE_KERNELS.tsv` | Completed; the OpenFGA configuration did not start |
| X8-FGA | Kaggle, private kernels `muzakkirhussain1/wardowl-x8fga-seed7`, `-seed11`, `-seed13`, `-seed17` | `harness/x0-x8-bf25bd0/` | See `evidence/raw/KAGGLE_KERNELS.tsv` | Completed |
| X8 amendment 2 | Kaggle, private kernels `muzakkirhussain1/wardowl-x8b-seed7`, `-seed11`, `-seed13`, `-seed17`, `-control-seed7`, `-pool`; smoke `-smoke`; recount `-verify` | `harness/x0-x8-bf25bd0/` | See `evidence/raw/KAGGLE_KERNELS.tsv` | Completed |
| Conformance run 1 | GitHub-hosted | `harness/conformance-run1-5d0f414/` | 40313285885 | `success` |
| Conformance run 2 | GitHub-hosted | `harness/conformance-run2-182bcbc/` | 40905549149 | `success` |
| Vendor reproducers | GitHub-hosted, in the paper's private development repository | None: `disclosure/reproducers/` uses the vendors' clients only | 41007436602, 41007779363, 41008151303. These pages are not public; the outputs are in `evidence/raw/results-reproducers/runs/` | `success` |

The Kaggle runs' outputs and logs, without embedding matrices, are also in the public dataset
[muzakkirhussain1/wardowl-paper-evidence](https://www.kaggle.com/datasets/muzakkirhussain1/wardowl-paper-evidence). Its
description says which account ran what.

## 3. How to rerun

Nothing below has been rerun for this file. Each class is described as far as the evidence supports it.

### Corpora and models

The harnesses download these from Hugging Face without pinning a revision. The table gives each source's current revision,
read from the Hub API on 2026-10-31. Each was last modified before the runs of October 2026, so it is what the runs would
have read, but only all-MiniLM-L6-v2's revision is recorded in a run's output. To pin a rerun, pass `revision=` to
`load_dataset` or to the model loader.

| Source | Used by | Revision on 2026-10-31 | Last modified |
|---|---|---|---|
| Dataset `BeIR/fiqa`, configs `corpus` and `queries` | E2E, X1, X2-E, X5-E, X3, X6 | `979c07a7cb5ccc6ca009792241fa1250b98055dd` | 2026-04-09 |
| Dataset `BeIR/msmarco`, configs `corpus` (streamed, first 1,000,000) and `queries` | X2-M, X5-M | `a918e0d11a77ed33f42f29d98340b655593b96ad` | 2026-04-09 |
| Dataset `BeIR/scidocs` | X3, X6 | `acebceec772628c6679d76d6cff30ad517d17f4e` | 2026-04-09 |
| Model `BAAI/bge-base-en-v1.5` | E2E, X1, X2-E, X5-E | `a5beb1e3e68b9ab74eb54cfd186867f64f240e1a` | 2024-02-21 |
| Model `BAAI/bge-small-en-v1.5` | X2-M, X5-M | `5c38ec7c405ec4b44b94cc5a9bb96e735b38267a` | 2024-02-22 |
| Model `sentence-transformers/all-MiniLM-L6-v2` | X3, X6 | `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, recorded in `x6-faiss.jsonl` | 2026-06-01 |
| Model `Qwen/Qwen2.5-3B-Instruct` | E2E | `aa8e72537993ba99e69dfaafa59ed015b17504d1` | 2024-09-25 |

The terms of FiQA and MS MARCO limit redistribution and allow non-commercial research (`LICENSE.md`), so the prepared
corpora are not here. A rebuild can be compared with the digests of the originals: `data/e-checksums.json` and
`data/m-checksums.json` in `evidence/raw/results-x2-x5/40921769714-1/`, and `logs/data-manifest.json` in
`evidence/raw/results-x3-x6/40940385704-1/`. The X1 query vectors have a digest in
`evidence/raw/x1run2-prep-gpu/x1run2/query_vectors.json`.

### End-to-end runs (X0, X8, X8-FGA, X8 amendment 2): Kaggle, GPU

- Compute: Kaggle GPU T4 x2 session with internet on. 2.8 hours per seed for X8, 0.9 for X8-FGA, about 0.1 per seed for the
  exposure and 2.2 for the control (`evidence/compute.md`).
- Each kernel in `kaggle/x8/` is a script that clones the library at bf25bd0, installs wardowl 2.1.0 from PyPI, runs
  `benchmarks/kaggle_setup.sh` and calls `acceptance/kaggle/enterprise_rag.py`. To run one, change `id` in its
  `kernel-metadata.json` to your account and run `kaggle kernels push -p kaggle/x8/seed11`. X0 and X1 run 1 are public
  notebooks that can be copied on Kaggle; their code is also in `kaggle/x0/` and `kaggle/x1-run1/`.
- Pinned by the code: wardowl 2.1.0 and the acceptance scripts; pgvector v0.8.7, Qdrant 1.19.2, Elasticsearch 9.5.5,
  OpenSearch 3.9.0, Weaviate 1.39.12 (`benchmarks/kaggle_setup.sh`, `benchmarks/kaggle_stores.sh`), OPA v1.21.2, OpenFGA
  1.22.0 (`enterprise_rag.py`).
- Not pinned, and read back from `results.json`: X0, X8 and X8-FGA ran Python 3.13.15, torch 2.11.0+cu128, transformers
  5.16.1, sentence-transformers 5.7.0, datasets 4.8.5, psycopg 3.3.6, chromadb 1.5.9, elasticsearch 9.5.1, opensearch-py
  3.2.0, qdrant-client 1.20.0, redis 8.1.0 and faiss-cpu 1.15.1. X0 had weaviate-client 4.24.0 and lancedb 0.40.0; the
  later runs had 4.24.1 and 0.41.0, so the runs were not on one set of versions. To pin a rerun, replace the `pip install`
  line with these versions. Redis comes from its package repository, unpinned: 8.10.2 in X0 and 8.10.3 in X8, by each
  run's `redis.log`. The Kaggle image digest of each kernel is in `evidence/raw/KAGGLE_KERNELS.tsv`; an image can be
  retired.

### Diagnosis grid (X1): Kaggle, CPU and one GPU

- X1 run 2: push, in order, `kaggle/x1run2/x1run2-prep-gpu/`, then `kaggle/x1run2/x1run2-shard-a/`,
  `kaggle/x1run2/x1run2-shard-b/` and `kaggle/x1run2/x1run2-shard-c/` side by side, then `kaggle/x1run2/x1run2-stats/`. Their
  `kernel_sources` name the private account, so change them, and `id`, to your own account (`kaggle/x1run2/make.sh` writes
  these folders). Wall clock 6.1 hours; 12.5 session hours.
- `harness/x1-run2-a956424/benchmarks/paper/x1_run2_kaggle.py` installs wardowl from that commit with
  `qdrant-client>=1.16`, `sentence-transformers>=3`, `datasets>=2.19`, `psutil`, `pyarrow` and `scipy`, not pinned. Each
  folder's `manifest.json` records what ran. Statistics: 10,000 bootstrap resamples, seed 20261026.
- X1 run 1 ran 7.3 hours in one session with the notebook in `kaggle/x1-run1/`.

### GitHub-hosted experiments (X2 to X7, conformance)

Fork `muzakkirhussain011/wardowl`, push the commit named in section 2 to a branch, and dispatch its workflow. The jobs install
from `uv.lock` by hash (`uv export --frozen`, `pip install --require-hashes`), and each records its image digests in a
`versions` record, so these are pinned much better than the Kaggle runs. They publish to the fork's `results/*` branches.

| Experiment | Workflow at that commit | Inputs | Job hours |
|---|---|---|---|
| X2, X5 | `harness/x2-x5-884ce18/.github/workflows/paper-x2-x5.yml` | `mode=full`; `data_run_id` empty, to prepare and embed again | 98.7 |
| X3, X6 | `harness/x3-x6-a191626/.github/workflows/paper-x3-x6.yml` | `mode=full`, `seeds=5` | 10.2 |
| Follow-up | `harness/x3-x6-followup-9e22b89/.github/workflows/paper-x3-x6.yml` | `configuration=followup`, `mode=full`, `seeds=5`. It reads the data and records of a full run's artifacts, so it needs a full run first | 7.4 |
| X4, X7 | `harness/x4-x7-e66dffc/.github/workflows/paper-x4-x7.yml` | `profile=full` | 15.3 |
| X7 amendment 2 | `harness/x7-amendment2-harness-41292bd/.github/workflows/paper-x4-x7.yml` | `profile=full`, `configuration=amendment2`; installs the library at 3c6559f | 1.5 |
| Conformance | `harness/conformance-run2-182bcbc/.github/workflows/paper-conformance.yml` | `seeds=20`, `examples=10`, `variants=all`; the Pinecone target needs its own key and was skipped without one | 8.2 |

Run 1 of the conformance campaign is the same workflow at `harness/conformance-run1-5d0f414/`.

### Vendor reproducers

These need neither wardowl nor the paper's data. Fork this repository and dispatch `.github/workflows/reproducers.yml`, or run
`disclosure/reproducers/redis.sh`, `disclosure/reproducers/mongodb.sh`, `disclosure/reproducers/cerbos.sh`,
`disclosure/reproducers/chroma_depth.py` and `disclosure/reproducers/chroma_crash.py` by hand with the versions in the
workflow's matrix. `chroma_crash.py` ends its own interpreter by design. `.github/workflows/cerbos-extra.yml` runs the extra
Cerbos tests of `evidence/cerbos-extra.md`.

## 4. What has and has not been checked

Not done:

- No independent rerun exists, and the author did not rerun any experiment to write this file. Rebuilding the prepared
  corpora from the seeds has not been tried.
- Nobody has confirmed that the Kaggle kernels still run on today's images, or that a fork can run the GitHub workflows.
- The recomputation in the artifact review covers a few numbers only, listed there. Most numbers were read from what the
  scripts printed.

Done on 2026-10-31, by re-reading stored outputs only:

- Outputs downloaded again from the X1 run 2, X8, X8-FGA and X8 amendment 2 kernels match the files archived earlier byte for
  byte where both exist. The outputs on the public notebooks of X0 and X1 run 1 match `evidence/raw/x0-seed7/` and
  `evidence/raw/x1-run1/`, apart from the kernel log's name and the gzipped `qdrant.log`.
- Empty answers counted from `answers.jsonl` for all eight end-to-end runs (`evidence/x8-run.md`).
- Notices retrieved and obeyed summed from `results.md` over the eight runs: 3,085 of 3,085.

## 5. What is left out, and why

- **Embedding matrices and query vectors** (`*.npy`): large, reproducible only with the models above, and derived from
  corpora whose terms limit redistribution. On Kaggle they remain in the kernels' own output.
- **CI artifacts `x2x5-data-*`, `x2x5-emb-*`, `x3x6-data`** (27 rows of `evidence/raw/ci-artifacts/MANIFEST.tsv`, the largest
  1.6 GB): prepared corpora and embeddings, for the same reasons. **They expire on GitHub:** the `x3x6-data` artifacts on
  2026-11-28, all the others on 2027-01-27, by the `expires_at` column of `MANIFEST.tsv`. After that, rebuilding is the only
  route, and it is untested.
- **The k=10 hit lists of the end-to-end runs:** never written, so recall@10 of X0, X8 and X8-FGA can't be recomputed from
  stored outputs (`evidence/ARTIFACT_GAPS.md`). X1, X2 and X5 do store them.
