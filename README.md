# Leak-Free but Not Loss-Free

Research artifact for the preprint "Leak-Free but Not Loss-Free: Verifying Permission-Aware Retrieval for
RAG across Vector Stores and Authorization Engines" by Syed Muzakkir Hussain.

The paper tests one enforcement layer, [wardowl](https://github.com/muzakkirhussain011/wardowl), across 13
vector stores and seven authorization engines. The author develops that library. Appendix A of the paper maps
every experiment to its versions and runs, and Appendix B lists every hypothesis with its registration and
verdict. The evaluation code lives in the wardowl repository, under `benchmarks/paper/`; this repository holds
what was registered, what came out and the text.

| Path | What it holds |
|---|---|
| `paper/` | The LaTeX source. GitHub Actions builds the PDF on every push, to the branch `results/pdf` |
| `plan/` | The paper plan, the pre-registration of the end-to-end repeats with its dated amendments, and the posting checklist |
| `evidence/` | One summary per run, with what each number was read from. `compute.md` gives the compute per experiment |
| `evidence/raw/` | Raw outputs of the Kaggle runs. In the tag `evidence-v1`, also the CI artifacts and results branches (see below) |
| `disclosure/` | The vendor reports with their minimal reproducers, which do not need wardowl. `reproducers.yml` runs them |
| `reviews/` | The numbers audit and the critical review the paper answers, with the decisions taken |
| `investigations/` | Diagnoses that turned into experiments |
| `literature/`, `bib/` | The literature review, the bibliography, its verification status and the reference checklist |
| `kaggle/` | The Kaggle runners and kernels |

## Raw outputs

The tag `evidence-v1`, which the DOI in the paper archives, adds to this tree:

- `evidence/raw/ci-artifacts/`: the GitHub Actions artifacts of the paper's runs, one folder per run, with
  `MANIFEST.tsv` (name, size, digest, dates and whether each artifact was copied) and `SHA256SUMS`.
- `evidence/raw/results-*/`: the published summaries of those runs, from the wardowl branches `results/*`.
- `evidence/raw/results-reproducers/`: the outputs of the vendor reproducers.

Prepared corpora and embeddings (the artifacts `x2x5-data`, `x2x5-emb` and `x3x6-data`) are left out. They can be
rebuilt from the seeds, and the corpora's own licenses limit redistribution. `MANIFEST.tsv` lists each one.

Model answers in the raw outputs may quote FiQA passages and synthetic company documents. The canaries, people,
ACLs and "credentials" in them are all synthetic, so a secret scanner's hits on those files are false alarms.

## Citing

See `CITATION.cff`. The arXiv identifier will be added when the preprint is posted.

## License

See `LICENSE.md`: MIT for code, CC BY 4.0 for text and data the author produced. Third-party material stays under
its own terms.
