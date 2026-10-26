# wardowl paper (private)

Working repository for the research paper on verifying permission-aware retrieval for RAG.

- `plan/`: the paper plan (`paper-plan-v1.md` is current).
- `paper/`: LaTeX source (`main.tex`). The PDF is built by GitHub Actions on every push (artifact
  `paper-pdf`); nothing is compiled locally.
- `bib/`: `references.bib` (papers and standards), `web.bib` (vendor and web pages), `STATUS.md`
  (verification status of every entry and works that must not be cited).
- `evidence/`: results of runs used by the paper.
- `investigations/`: diagnoses that turned into experiments.
- `literature/`: the literature review report.

Experiment code lives in the public wardowl repository under `benchmarks/paper/` so that Kaggle can
import it; results are archived here under `evidence/`.
