# Critical review, 2026-10-30 (independent agent; report only) and the decisions taken

Verdict as written: weak reject (length; framing; missing controls). Strengths named: candid
reporting of falsified and inconclusive verdicts; the pgvector plan-cache finding (new, useful);
the Qdrant islanding diagnosis and layout fix; the side-channel game design; the engine study's
separation of translation faults from revision skew; careful bound units; bibliography hygiene.
Line numbers refer to the files as of commit 4dcd2e9.

## Decisions (Syed, 2026-10-30)

- Structure: one arXiv preprint now, restructured to a main text of about 15 to 20 pages plus
  appendices; a 9-page venue version is cut later from it. No split into two papers.
- Title: keep "Leak-Free but Not Loss-Free"; scope "leak" in the text (returned content at the
  checked revision, with freshness), and use "reveal" for side channels throughout.
- Disclosure: Syed files the vendor reports himself before the arXiv posting.
- Experiments: run the end-to-end positive control and exposure measurement only. Native
  enforcement baselines (PostgreSQL RLS, Elasticsearch/OpenSearch DLS), the near-duplicate
  sensitivity sweep and a release rerun are NOT run: state them as limitations.

## Major concerns and the fixes asked for

1. "Leak-free" is narrow and contradicted by the paper's own wording. Title/abstract
   (main.tex:46 "Security held everywhere"), intro.tex:46-48, conclusion.tex:5-6 ("secure whatever the
   other parts do") vs side.tex:181,243,310 ("leaked"); background.tex:56-58 defines security at the
   revision the hits are checked, so stale reads are secure by definition; engines.tex:172-178
   revoked chunks served up to 8.7 s and held a full ttl after invalidate(); Leak-dagger rows in the
   layer's adapters (conformance.tex:329-334, 362-367); system.tex:122-123 "With the re-check off ... a
   store that ignores the filter still cannot leak" contradicts the Cerbos finding (with the re-check
   off an over-approximating filter is returned). Fixes: define the claim as "no returned chunk
   outside R at the checked revision"; add freshness (delta-secure: H subset of R at every revision
   no older than t_request - delta) and report the measured delta per path; report the cache fault as
   a violation of the stated delta; abstract sentence like "No returned chunk was unreadable at the
   revision the re-check read, in any tested configuration; information about unreadable chunks still
   was revealed through latency, counts, recall and scores"; delete "whatever the other parts do";
   correct system.tex:122-123 (with the re-check off, security rests on the filter).
2. Formalization vs system. R defined from check makes A1 circular (background.tex:25-28, 80-81);
   Definition 1 requires honesty of every result (background.tex:59-66) while the evaluated flag is
   honest only about under-retrieval (system.tex:153-156; repair: 57-58% of Qdrant's complete results
   not maximal). "Sound" redefined as score fidelity departs from Wang et al. Fixes: define R from the
   policy oracle, A1 as check equals policy; sound = H subset of T*_eps (mis-retrieval violates it);
   complete = |H| = min(k, |R|) (under-retrieval violates it); count-honest = c = 1 implies
   |H| = min(k, |R intersect phi_s|), and say the implemented flag is count-honest relative to phi_s
   only; demote the proposition to an observation if it is definitional; add an explicit trusted
   computing base (subject-to-check mapping in adapters, identity extraction, the cache, staleness,
   metadata binding) and a cache-and-staleness variant (secure at a revision no older than
   t - (ttl + delta)).
3. End-to-end test power and units. The re-check evaluates the same metadata predicate as the filter
   (e2e.tex:114-116); no positive control at pipeline level; no exposure measure (how many questions
   had unreadable chunks in their unfiltered top-k); hits counted over k=5 and k=10 (about a third
   duplicates); per-request bounds in engines (4.8e-6, 2.9e-4) contradict the clustering argument:
   per fault episode about 2.7e-3 for 1,090 episodes; a binomial bound over sampled questions says
   nothing about an adaptive adversary. Fixes: exposure counterfactual and mutation positive control
   (being run, X8 amendment 2); count distinct (question, chunk) pairs where available; use
   per-question, per-episode and per-person bounds in abstract and conclusion, drop hit and request
   counts there; state that bounds are over the generator's question distribution.
4. Conformance attribution and coverage. Cerbos: triage shows the disagreement is the layer's
   translation of CEL in/== into In, which also accepts scalars (an adapter type gap), but intro blames
   Cerbos, engines says "no translation fault", conformance counts it as a class. Of "six classes",
   only Redis and MongoDB truncation are new store behaviours with a correctness effect; two are
   availability faults in the adapters; one is documented limits that fail closed; Cerbos was already
   found by review. Pinecone never ran (13 stores). In run 2, about 85% of OpenFGA and SpiceDB runs
   were refused before reaching the engine. The kit checks membership, count and ordering, and k is
   not stated: if k < |E(phi)|, false denials outside top-k are invisible. Fixes: Cerbos as a
   translator type gap in the adapter; recount honestly (store behaviours, adapter faults, documented
   limits); 13 stores; state k and the refusal share; separate "found by this paper's method" from
   project history.
5. Cross-store comparisons. No unfiltered baseline (cost of the filter vs baseline ANN error, e.g.
   LanceDB IVF-PQ floor); settings mix tuned and default; no matched-QPS comparison in the main text
   (frontier figure only proposed); the enterprise corpus with 19 near-identical copies per document is
   a worst case for graphs; no native-enforcement baselines; numbers partly properties of the layer's
   schema (jsonb @> with GIN, array test above 100 values, Chroma boolean keys); Lucene segment state
   unreported; PostgreSQL 16.15 vs 17.11 across experiments. Fixes: unfiltered or 100%-selectivity
   recall per store where data exist (X2 has 100% cells on MS MARCO); recall at matched QPS from the
   X2 sweeps; label rows "store under this layer's schema"; report 0.55-0.98 for approximate stores;
   state the rest as limitations (decision above).
6. Statements beyond the evidence. Autovacuum explanation is inference (write "consistent with");
   P2 inconclusive not mentioned; "two repeats fell outside" should say prediction 3 was falsified;
   X8-FGA seed 11 was a mixture; exact-mode runs still left one person without results (unexplained);
   the 8.7 s staleness was 1 of 40 trials and did not replicate (rerun max 5.2 s, within 5.5 s), and
   "6.5 s predicted" vs "5.5 s" is unreconciled (6.5 = 5.5 + 1 s polling); H2.4's "U-shaped" label is
   not supported as a U (V does not test recovery at high selectivity; pgvector's V is driven by
   exact plans at 0.06%): call it "intermediate filters harder than the smallest"; intro side-channel
   range cherry-picks; repair claim holds only for the unbounded arm; Qdrant comparison mixes subsets
   (use 0.656 vs 0.952 overall).
7. Side-channel null ignores build variation. Cross-build AUC ranges about 0.36-0.64, so channels in
   0.6-0.8 are near build noise; no multiplicity control; reverse channels (pgvector constant work
   0.017) excluded from H6 although a reverse channel serves an attacker equally; the new detection
   fields (missed, exhausted, over_limit) are caller-visible observables not measured. Fixes: report
   |AUC - 0.5|; state the cross-build noise level next to the channels; say padding was tested only
   where the forward AUC was at least 0.75; name the detection fields as an untested observable.
8. Related work omissions (already in references.bib, verified): Zerr et al. Zerber (EDBT 2008) and
   Zerber+R (EDBT 2009); Fagin et al. Searching the Workplace Web (WWW 2003); Pappachan et al. Sieve
   (PVLDB 2020); LeFevre et al. (VLDB 2004); Motro (ICDE 1989); Griffiths and Wade (TODS 1976); NHQ
   (NeurIPS 2023); HQANN (CIKM 2022); CAPS (2023); UNG (SIGMOD 2025); SeRF (SIGMOD 2024); iRangeGraph;
   Window filters (ICML 2024); SIEVE (Li et al.); AnalyticDB-V (PVLDB 2020); VBASE (OSDI 2023);
   Disselkoen et al. How We Built Cedar (FSE Companion 2024); Klees et al. (CCS 2018); Schloegel et al.
   SoK (S&P 2024); Smucker et al. (CIKM 2007); Urbano et al. (SIGIR 2019); PoisonedRAG (USENIX Security
   2025); FIDES (Costa et al., 2025); Wu et al. (2024). Not in the bib (verify before citing):
   Goguen and Meseguer noninterference (S&P 1982); Askarov, Zhang and Myers (CCS 2010); Zhang, Askarov
   and Myers (PLDI 2012); Gelernter and Herzberg cross-site search attacks (CCS 2015); Felten and
   Schneider timing attacks on web privacy (CCS 2000); McKeeman differential testing (Digital Technical
   Journal 1998); Margrave (Fisler et al., ICSE 2005); Zelkova (Backes et al., FMCAD 2018); Martin and
   Xie mutation testing of access-control policies (WWW 2007); Hanley and Lippman-Hand rule of three
   (JAMA 1983); Song, Wagner and Perrig (S&P 2000), Curtmola et al. (CCS 2006), Wong et al. secure kNN
   (SIGMOD 2009). related.tex:146 "NoREC-style oracle" is inaccurate (NoREC is metamorphic).
9. Version under test not single; artifacts may expire. Add a table mapping each experiment to the
   library commit and store/engine versions; archive raw outputs (Zenodo) before arXiv. (Release rerun
   not done, decision above: say so.)
10. Pre-registration ledger. Add an appendix ledger: every hypothesis with its file, commit,
    registration time, run id and start time, verdict, and class (confirmatory; exploratory, specified
    in writing after the main results and before running; implementation check). Replace "pre-
    registered after seeing these results" with "exploratory, specified in writing after the main
    results and before running". Tell readers how to verify ordering (pre-registration commit is an
    ancestor of the run's head SHA; Actions creation times).
11. Disclosure, AI statement, licenses, anonymity. Remove promises like "Every row will be confirmed
    with the maintainers before publication" (conformance.tex:395-396, 421-423). AI statement: say
    which artifacts the agent produced and what the author reviewed; the automated reference checks
    were done by the agent; common-mode risk (system, oracle and meta-tests from the same agent) as a
    threat to validity. Licenses: FiQA, SciDocs, MS MARCO (non-commercial research terms), Qwen2.5-3B-
    Instruct (check its license), bge models, all-MiniLM. Strip LaTeX comments before arXiv
    (arxiv_latex_cleaner or equivalent, run in CI).

## Minor (selected)
Experiment codes need a key (experiment map); terminology drift (subject/person/user/attacker;
chunk/document/passage/point/object; "organisation"); notation (R_tau(s), R(s), count R; k' unused);
error bars missing in several tables; H2.2 Spearman over a designed grid; precision varies (4 vs 3
decimals); answer accuracy scoring undefined; "without any signal" true only of the 2.1.0 flag; the new
Chroma post-filter fallback's 1,000-candidate recall cliff not evaluated; huge tables (fault table
about 30 rows; X5 13-column table*; e2e safety table of zeros); no figures (13 tables); unexplained
"21, 21, 16 and 23" and the missing 40th Cerbos run; embedding dimension differs across experiments
(affects Qdrant's full-scan threshold).

## Length plan (reviewer's option A, adapted to a 15-20 page arXiv main text)
Main text keeps: intro (3-4 contributions), problem and threat model (fixed definitions, TCB),
the layer (short), security results (conformance summary, engines, e2e with exposure and control),
retrieval quality (audit, Qdrant, pgvector plan cache, X2 essentials), repair, side channels (game and
verdicts), related work, limitations, conclusion. Appendices take: the full fault table, the
precedents table, composition/caching/identity details, engine latency and caching details, the e2e
model subsection, filter size (X3) with Chroma forensics, X2 detailed tests table, X5 full table, the
side-channel hypothesis table and build-offset forensics, related work on industry systems, the
experiment map, the pre-registration ledger, compute, settings.
