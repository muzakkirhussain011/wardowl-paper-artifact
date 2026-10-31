# What the artifact does not hold, and why

Written 2026-10-31, after an independent artifact review of the tag `evidence-v1` as it stood on 2026-10-30. This file
records what is still missing or weak, so that nobody has to find it out. `REPRODUCE.md` is the map of what is here.

## Per-question outputs

| Run | Per-question rows with k=5 hits | k=10 hit lists | Note |
|---|---|---|---|
| X0, seed 7 | `evidence/raw/x0-seed7/answers.jsonl` | Not written | |
| X8, seeds 11, 13, 17 | `evidence/raw/x8-seed*/answers.jsonl` | Not written | Fetched on 2026-10-31 |
| X8-FGA, seeds 7, 11, 13, 17 | `evidence/raw/x8fga-seed*/answers.jsonl` | Not written | Fetched on 2026-10-31 |
| X8 amendment 2, exposure, four seeds | `evidence/raw/x8b-seed*/x8b-exposure-seed*.json`, counts per question, no hit identifiers and no answers | Counts only | No model ran, so these kernels have no `answers.jsonl` |
| X8 amendment 2, control, seed 7 | `evidence/raw/x8b-control-seed7/answers.jsonl`, `x8b-control-seed7-questions.json` | Unreadable hits per question only (`u10`) | |
| X1 runs 1 and 2 | `evidence/raw/x1-run1/x1/runs/`, `evidence/raw/x1run2-shard-*/x1run2/runs/`, parquet | Present (`hits10`) | Fetched for run 2 on 2026-10-31 |
| X2, X5 | `rows/*.jsonl.gz` in the zips `x2x5-res-*` of run 40921769714 | Present (`hits10`) | |
| X3, X6 | One record per retrieval, in `x3-<store>.jsonl` and `x6-<store>.jsonl` in the zips `x3x6-results-*` of run 40940385704: latency, count, and for X3 the recall | No hit identifiers | |
| X4, X7 | One record per subject, trial or episode, in `raw/*.jsonl.gz` of each results folder | Not applicable | |
| Conformance runs | Findings per target in `findings/` in the zips `conformance-*` of runs 40313285885 and 40905549149 | Not applicable | |

**The k=10 hit lists of X0, X8 and X8-FGA do not exist.** `_write_answers` in `enterprise_rag.py` writes the k=5 hits and
the answer; the k=10 retrieval is scored and dropped. So recall@10 of those eight runs, which Figure `fig:qual-audit` and
the abstract's recall range rest on, is a printed number that can't be recomputed from stored outputs. Recall@5 can be
approximated from `answers.jsonl` as overlap with FAISS's hits, without the tie credit. Also, 5,420 of the 16,360 hits checked
per configuration are the stored k=5 hits; the safety counters over the rest are printed. The check of each hit against the
oracle ran inside the kernel and was not recorded hit by hit. A later rerun would need a harness change to store them.

## Pre-registration and ordering

- **The Kaggle pre-registrations have no independent timestamp.** The public repository was created on 2026-10-30, after every
  X8, X8-FGA and X8 amendment 2 run, and git dates are set by the author. `plan/x8-prereg.md` and its amendments (875d98e,
  ba64c23, 1a25086, eff0b23) therefore prove order only as far as one trusts the author. `evidence/raw/KAGGLE_KERNELS.tsv`
  gives Kaggle's server times for each kernel, read through the API on 2026-10-31. They agree with the author dates: for example
  the first X8 kernel started at 15:45:18 UTC on 2026-10-29, 22 seconds after 875d98e's date, and the first X8-FGA kernel at 21:58:58
  UTC, 41 seconds after ba64c23's. But the kernels are private, so a stranger can't check these times. The stored logs date the
  runs only in part: the server logs of X8 and `openfga.log` of X8-FGA hold dates, `x1run2-*/x1run2/manifest.json` holds start
  times, and the kernel logs of X8 amendment 2 hold only seconds since the start.
- **The same weakness applies to X1 run 2.** Its pre-registration commits are on a public branch of the library, but no
  Actions run bounds them.
- **The GitHub experiments do not have this weakness:** their run times and head commits are in GitHub's own records, and
  the review confirmed the ancestry the paper claims.

## Kaggle kernels

- The kernels of X1 run 2, X8, X8-FGA and X8 amendment 2 are private on `muzakkirhussain1`. Their code is in `kaggle/`, and their
  outputs and logs are in `evidence/raw/` and in the public dataset `muzakkirhussain1/wardowl-paper-evidence`, but their
  version history is not public. Any sentence in the paper that rests on that history can't be checked by a stranger until they
  are public or the sentence changes.
- The first two runs, X0 and X1 run 1, ran under another account of the author, `muzakkirhussainsyed`, as public notebooks. Two
  accounts for one person are named here because that is what happened.
- The kernels `x1run2-prep`, an abandoned CPU attempt, and `x1run2-prep-tpu` hold no output files. Their last version is a stub
  that prints "superseded" (`kaggle/x1run2/prep-stop/`, `kaggle/x1run2/tpu-stop/`), pushed to stop them, so nothing from those
  attempts survives. No number in the paper comes from them: `x1run2-prep-gpu` did the preparation.

## Pinning and rebuilding

- **The Kaggle runs do not pin their Python dependencies.** They install `sentence-transformers>=3`, `datasets>=2.19` and so on,
  and record the versions afterwards in `results.json`. X0 and the later runs differ in weaviate-client and lancedb, and in Redis's
  server version.
- **Corpora and models carry no revision in the code** (`load_dataset("BeIR/fiqa", ...)`, `load_dataset("BeIR/msmarco", ...)`, and
  the model names). `REPRODUCE.md` gives the revisions read on 2026-10-31 and the digests a rebuild can be compared with.
- **Rebuilding has not been tested.** The left-out CI artifacts expire on 2026-11-28 (`x3x6-data`) and on 2027-01-27 (the rest),
  by `expires_at` in `MANIFEST.tsv`. After those dates a rerun of X3 and X6 from the same prepared data, or a follow-up against it,
  is not possible.

## Provenance of the vendor reproducers

The run ids 41007436602, 41007779363 and 41008151303 are of the paper's private development repository, so a stranger can't open
them; only the outputs on branch `results/reproducers` are public, and those are self-reported copies. Later runs on that branch
name head commits of the same repository, and `38f4ae7` (run 41114474172) is not on any public branch. A run of
`.github/workflows/reproducers.yml` on the public repository would give public run ids, at a later date.

## Archive and licenses

- **No DOI exists yet,** and the paper's release sentence depends on it. Minting one needs the author's Zenodo account.
  `.github/workflows/evidence-tag.yml` then refuses to move the tag.
- **GitHub reports this repository's license as "other" (NOASSERTION).** That stands: the repository holds material under several
  terms by design (`LICENSE.md`).
- **MS MARCO text.** We state that the archive holds none, from a sample of the result files and from what the harness writes. We
  did not open all 348 archived CI artifacts.

## Review items left as they are, with the reason

- `reviews/` opens with hard criticism of an earlier draft, including "weak reject". It stays: the paper answers it, and the record
  is more useful with it than without it.
- `plan/paper-plan-v1.md` keeps its plan sections, including venue choices. They are what was planned at the time. Its progress
  log was removed on 2026-10-31 because it was an operational diary and pointed to a file that no longer exists; `evidence/` and
  the git log hold the same events.
- `plan/x8-prereg.md` still counts "people" in its prediction X8-3, because a pre-registration is not rewritten. The unit is
  corrected in `evidence/x8-run.md`.
- The Redis over-admission was filed as a public issue, although the behavior can match a different value and RediSearch's
  `SECURITY.md` routes serious issues privately. It was a judgement call: the behavior needs a value longer than 4,096 bytes, and
  the author took a public bug report to be the proportionate route. The library's public pull request #167 had already described
  it. It stands.
