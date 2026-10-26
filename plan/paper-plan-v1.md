# Paper plan v1 (2026-10-26, after the literature review)

Supersedes paper-plan-v0.md. Sources: reports/Permission aware retrieval literature review.md, the six
notes in research_notes/Permission aware retrieval literature review/, evidence/kaggle-scale-run-2026-10-24.md
and investigations/filtered-recall-gaps.md.

## Positioning (decided)

A verification and evaluation paper, not a new-mechanism paper. The enforcement design (pre-filter,
widening post-filter, re-check, fail closed) has clear precedent: query modification (Stonebraker &
Wong 1974), Büttcher & Clarke 2005, Bailey, Hawking & Matson 2006, Zanzibar-style per-candidate
checks, Amazon Bedrock managed knowledge bases, and 2026 access-aware vector indexes (HoneyBee, Veda,
the SeQureDB '26 vision paper). We credit all of it and claim what nobody has: how faithfully today's
vector stores and authorization engines implement permission filters, how well they retrieve under
permission-shaped filters, and how to detect when they silently fail.

Working title: **Leak-Free but Not Loss-Free: Verifying Permission-Aware Retrieval for RAG across
Vector Stores and Authorization Engines**

Formal frame: adapt Wang et al. (VLDB 2007) sound / secure / maximal to top-k vector retrieval
(the SeQureDB '26 paper explicitly calls for this). Because every hit passes the authorizer's check API,
security depends on the check API alone; filter translation errors can only cost maximality (recall).
State the blind side: the re-check sees false admits, never false denials.

## Contributions (revised)

C1. Formalisation: secure and maximal top-k retrieval under an external authorizer; metrics: leak rate
    (with a per-question upper bound, not per-hit), permission-recall@k against exact search over the
    readable set, under-retrieval rate, false-completeness rate. Position the aligned/misaligned layouts
    on the field's existing correlation axis (ACORN; GLS; HCBGen) by measuring it.
C2. Differential conformance testing of filter semantics across 14 vector stores with an independent
    reference oracle; a bug and semantic-gap table, each item confirmed or reported upstream before the
    preprint.
C3. Filter-versus-check disagreement measurement for authorization engines that compile policies into
    filters (OPA partial evaluation or filter documents, Cerbos query plans, OpenFGA ListObjects,
    SpiceDB LookupResources), at a single revision token so ACL churn is not miscounted.
C4. Audit of production stores under permission-shaped filters (OR over many groups, multi-tenant,
    directory-scale group counts, misaligned readable sets): recall-throughput frontiers at documented
    defaults, tuned settings and exact search; the under-retrieval finding (empty results with
    complete=True) and its causes (pgvector scan limits; Qdrant filtered-graph traversal without ACORN).
C5. Detection and mitigation of under-retrieval in the enforcement layer (count-based detection,
    bounded exact fallback, honest completeness), evaluated for recall and latency. Credit OpenSearch 3.5,
    which already falls back to exact search when fewer than k approximate results return.
C6. End-to-end canary evaluation: 107,540 chunks, 20 tenants, 189 people, 1,105 questions incl. 432
    red-team, 10 store configurations, 163,236 checked hits, 0 leaks; plus the out-of-scope observation
    that the model obeyed every retrieved injection (marks the boundary of the claim).
C7. (New, high value) Side channels of permission-aware retrieval: does the widening loop's round count,
    latency or the complete flag reveal unauthorized documents near the query; same for filtered graph
    traversal and hybrid BM25 statistics. Measure, then state mitigations (constant-work widening).

## Venue plan

- Primary: NeurIPS 2027 Evaluations & Datasets track (the renamed Datasets & Benchmarks track; 2027 call
  not yet out; 2026 pattern suggests abstract ~early May 2027, 9 pages, double-blind, code required at
  submission for tool contributions, Croissant metadata if a dataset is released, 16-item checklist incl.
  error bars and compute).
- Backup routes (pick one stream; NeurIPS forbids concurrent archival submission): PVLDB Experiment,
  Analysis & Benchmark (rolling monthly to 1 March 2027, 12 pages, reproducibility package at
  submission) or USENIX Security '27 Cycle 2 (26 January 2027, 13 pages, open-science appendix).
- Not targeted: IEEE S&P 17 Nov 2026 (too soon; one-year resubmission block), ICML/ICLR main, position tracks.
- arXiv preprint: primary cs.CR, cross-list cs.IR, cs.DB, cs.LG. Post it after the vendor notifications
  and before or alongside submission, consistent with the chosen venue's anonymity rules.

## Process risks and actions

1. arXiv endorsement: first-time submitter needs a personal endorser in cs.CR (since Jan 2026). Action:
   Syed to identify an endorser early (a co-author or a researcher who has published in cs.CR).
2. Anonymity: wardowl is public under Syed's name. Action: anonymised mirror and renamed package for
   review; avoid self-identifying citations in the submission.
3. AI-assistance disclosure: the implementation was written largely with an AI coding agent. Disclose
   per the venue (NeurIPS: non-standard LLM/agent use in the methods; arXiv: significant use must be
   reported; AI is never an author). Every reference must be verified by a human; arXiv announced a
   one-year ban for hallucinated references.
4. Vendor disclosure: report store bugs and documentation gaps to maintainers before the preprint.
5. Prior-art overlap: the related-work section must credit the precedents above explicitly.

## Experiment programme (all on Kaggle; nothing on the laptop)

Statistics for every experiment: at least 5 permission-layout seeds and 3 index builds per configuration;
95% confidence intervals by cluster bootstrap over persons/questions; paired tests between strategies;
hardware, versions and settings disclosed; predictions written down before running.

- X1 Under-retrieval diagnosis grid (from investigations/filtered-recall-gaps.md): pgvector
  max_scan_tuples, work_mem, scan_mem_multiplier, ef_search, inner LIMIT; Qdrant ACORN (max_selectivity),
  is_tenant / payload_m layouts, segment count; probe set of single-group people. Retrieval only, no LLM;
  fits one 12-hour session. Step 0 needs no new run: analyse answers.jsonl from the existing run inside a
  Kaggle notebook that attaches that notebook's output.
- X2 Recall-throughput frontiers per store under permission filters: documented defaults, tuned, exact;
  selectivity 0.06%-100%; measured correlation axis; FiQA and MS MARCO 1M.
- X3 Filter-size scaling: groups per subject 1 to 40,000; OR-filter latency and failures per store.
- X4 Authorization engines: filter-versus-check disagreement (C3); ListObjects/LookupResources truncation
  thresholds; authorizer latency with and without caching; rerun OpenFGA with a longer start-up wait.
- X5 Under-retrieval mitigation (C5): detection rate, false-completeness rate, recall and latency of the
  bounded exact fallback.
- X6 Side channels (C7): round count, latency and complete as functions of unauthorized density near the
  query; attacker success at inferring existence; effect of constant-work widening.
- X7 Revocation latency end to end per store and engine; faults (authorizer down, slow, malformed) and
  the availability cost of failing closed.
- X8 End-to-end canary run repeated (3 runs) with paraphrase-aware canary detection.

## Engineering prerequisites in wardowl (core library)

- Honest completeness: a short result from an approximate pre-filtered search must not be reported as
  complete (currently retriever.py:407-408).
- Under-retrieval detection and a bounded exact-search fallback using the same filter and re-check.
- Expose pgvector scan settings (max_scan_tuples, scan_mem_multiplier, work_mem) and Qdrant's ACORN
  search option.
- Fix docs/concepts.md (iterative scans do not guarantee full results for selective filters).
- Optional: revision-token pinning for SpiceDB and OpenFGA so filter and re-check see one snapshot.
All changes go through PRs with CI in GitHub Actions; nothing runs locally.

## Writing artefacts

- Private repository for the paper (LaTeX, figures, bibliography); PDF built in GitHub Actions.
- Bibliography: merge and de-duplicate the BibTeX from the six notes; every entry verified; unverified
  fields left out rather than guessed.
- Experiment code: public, in the wardowl repository (benchmarks/paper/), so Kaggle can import it from a
  public GitHub URL; an anonymised mirror is made at submission time.
