# Testing Permission-Aware Retrieval for RAG across Vector Stores and Authorization Engines

Research artifact for the preprint of that title by Syed Muzakkir Hussain.

The paper tests one enforcement layer, [wardowl](https://github.com/muzakkirhussain011/wardowl), across 13 vector stores
and seven authorization engines. **The author develops wardowl**, so this is not an independent evaluation of it.

## How to find things

- **From a table or figure to its data and code:** [`REPRODUCE.md`](REPRODUCE.md). It maps every table and figure to the
  run, the script and the data files, says how to rerun each class of experiment, and says plainly what has not been
  rerun.
- **What is missing, and why:** [`evidence/ARTIFACT_GAPS.md`](evidence/ARTIFACT_GAPS.md).
- **From a code like X1 or X8 to its versions and run ids:** the paper's Appendix A; `REPRODUCE.md` repeats the ids.
- **What was predicted, and when:** the paper's Appendix B, `plan/x8-prereg.md`, and the `PREREG*` files under
  `harness/*/benchmarks/paper/` in the tag.
- **Every Kaggle run's outputs and logs, browsable without git:** the public dataset
  [muzakkirhussain1/wardowl-paper-evidence](https://www.kaggle.com/datasets/muzakkirhussain1/wardowl-paper-evidence).

## Which version to read

The branch `main` holds what was registered, what came out, and the text. The tags `evidence-v1` (released 2026-11-02) and
`evidence-v2` are the archive versions: each adds the CI artifacts and results branches of the paper's runs and the library at the
commits those runs used, and `evidence-v2` holds X0 and X1 run 1 as executed again on 2026-11-07. Build them with
`.github/workflows/evidence-tag.yml` and `evidence-tag-v2.yml`; each refuses to replace its tag once a release, or its
`evidence/ARCHIVE_DOI` or `evidence/ARCHIVE_DOI_V2`, exists, and without an explicit answer. The archive is at
https://doi.org/10.5281/zenodo.23874613, which lists every version and resolves to the newest (v1:
https://doi.org/10.5281/zenodo.23874614; v2, released 2026-11-08: https://doi.org/10.5281/zenodo.24047105). The commit that adds a version's DOI, and any later commit of `main`, are not in that
version.

| Path | What it holds |
|---|---|
| `REPRODUCE.md` | The map from the paper to the data and code, and how to rerun |
| `paper/` | The LaTeX source. GitHub Actions builds the PDF on every push, to the branch `results/pdf` |
| `plan/` | The paper plan, and the pre-registration of the end-to-end repeats with its dated amendments |
| `evidence/` | One summary per run, with what each number was read from. `compute.md` gives the compute per experiment, and `ARTIFACT_GAPS.md` what is missing |
| `evidence/raw/` | Raw outputs and logs of the Kaggle runs: X0, X1 runs 1 and 2, X8, X8-FGA, X8 amendment 2 and the recount. `KAGGLE_KERNELS.tsv` lists each kernel and its server times |
| `disclosure/` | The vendor reports with their minimal reproducers, which do not need wardowl. `reproducers.yml` runs them |
| `reviews/` | The numbers audit and the critical review the paper answers, with the decisions taken |
| `investigations/` | Diagnoses that turned into experiments |
| `literature/`, `bib/` | The literature review, the bibliography and its verification status |
| `kaggle/` | The Kaggle runners and kernels. The kernels are private; their outputs and logs are in `evidence/raw/` and in the dataset above |

The tag `evidence-v1` adds to this tree:

- `harness/<experiment>-<commit>/`: the wardowl library at the exact commit of each run: the package, tests, harnesses,
  setup scripts, workflows and lock file. Only the site's media under `docs/_static/` stay out. `harness/COMMITS.tsv` names
  each folder's full commit hash and the runs that used it.
- `evidence/raw/ci-artifacts/`: the GitHub Actions artifacts of the paper's runs, one folder per run, with `MANIFEST.tsv`
  (name, size, digest, dates and whether each artifact was copied) and `SHA256SUMS`.
- `evidence/raw/results-*/`: the published summaries of those runs, from the wardowl branches `results/*`.
- `evidence/raw/results-reproducers/`: the outputs of the vendor reproducers.

## What is left out

Embedding matrices and query vectors, and the CI artifacts `x2x5-data-*`, `x2x5-emb-*` and `x3x6-data`, which hold prepared
corpora and embeddings. Each left-out CI artifact has a row in `MANIFEST.tsv` with its expiry date: `x3x6-data` on
2026-11-28 and the rest on 2027-01-27, after which they can only be rebuilt. Rebuilding has not been tested.
`REPRODUCE.md` gives the corpus and model identifiers and the digests a rebuild can be compared with.

Model answers in the raw outputs may quote FiQA passages and synthetic company documents. The canaries, people, ACLs and
"credentials" in them are all synthetic, so a secret scanner's hits on those files are false alarms.

## Citing

See `CITATION.cff`. The arXiv identifier will be added when the preprint is posted.

## License

Mixed; `LICENSE.md` is the full statement. Code is under MIT. Text and data the author produced are under CC BY 4.0. The
paper's text and figures under `paper/` are not licensed until the preprint is posted. FiQA text quoted in the outputs,
and answers generated by Qwen2.5-3B-Instruct, stay under their own terms and are for non-commercial research only.
