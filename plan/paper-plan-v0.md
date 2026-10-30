# Paper plan v0 (draft, 2026-10-26)

Status: first draft written before the literature review returns. Everything here is a hypothesis to
check against the related work; novelty claims especially must be revised once the review is in.

## Working titles

- Permission-Aware Retrieval for RAG: Enforcing Existing Authorization Inside Vector Search
- Who May Read This Chunk? Fail-Closed Access Control for Retrieval-Augmented Generation
- Leak-Free but Not Loss-Free: An Empirical Study of Access Control in Vector Search for RAG

## The problem in one paragraph

RAG systems retrieve the chunks most similar to a question and place them in an LLM prompt. Similarity
ignores authorization, so in any index shared by readers with different permissions, retrieval can place
a chunk in the prompt that the requesting user may not read (OWASP LLM08:2025). The obvious fix, filter
the global top-k afterwards, collapses for users who may read a small or query-distant share of the
corpus. Enforcing permissions inside the approximate-nearest-neighbour (ANN) search fixes recall in
principle, but depends on each vector store's filtered-search implementation, on translating the
organisation's permission system into the store's filter language without semantic drift, and on what
happens when the permission system is slow, wrong-shaped or down.

## Candidate contributions (to be checked for novelty)

C1. Problem formalisation. Permission-aware top-k retrieval; metrics: leak rate, permission-recall@k
    (recall against exact search over the user's readable set), under-retrieval rate (users who can read
    something but get fewer than k or zero hits), completeness signalling. Key axes: selectivity
    (readable share) and alignment (correlation between the readable set and query similarity).
    Simple analysis of why post-filter recall collapses (expected permitted hits in top-m is about m*s
    when uncorrelated; worse when misaligned) and what geometric widening up to a cap can and cannot
    guarantee.

C2. Design with stated guarantees. Two independent enforcement layers (filter inside the ANN search,
    then an authorizer re-check of every hit, disagreements counted as violations); fail-closed
    semantics with strict answer validation; a three-operator filter algebra with one reference
    semantics; scopes (necessary conditions) to narrow post-filtering; AllOf/AnyOf composition with the
    scope asymmetry; identity bound to verified tokens for agents (MCP, HTTP); audit without content.
    State the safety property precisely (no denied chunk returned, given a correct authorizer and
    faithful stored metadata) and what completeness can and cannot claim under ANN.

C3. Differential conformance testing of filter semantics across 14 vector stores. A generator of
    adversarial metadata and filters (1 vs "1", Unicode normalisation, case, dotted fields), one
    reference oracle, applied to real stores; catalogue of bugs and semantic gaps found (type
    confusion in keyword fields, Chroma #7594 array-metadata resurrection, partial results on
    timeouts, eventual consistency in Pinecone, Cassandra lightweight-transaction timestamp ordering,
    quantization recall loss). Position against SQLancer-style differential testing of DBMSs.

C4. Empirical study. (a) Recall/latency of naive post-filter vs widening post-filter vs in-index
    pre-filter over selectivity 0.06% to 100% and three alignments, on BEIR FiQA (57.6k) and MS MARCO
    (1M), across up to seven stores; (b) enterprise end-to-end evaluation with canaries in chunks,
    prompts and answers: 107,540 chunks, 20 tenants, 189 people, 1,105 questions incl. 432 red-team,
    10 store configurations, 163k checked hits, 0 leaks; (c) the under-retrieval finding: at usual
    settings, store recall under permission filters ranges 0.56 to 1.00, and pgvector returned no hits
    at all for some least-privileged users while completeness could not detect it.

C5. (Optional, NeurIPS Datasets and Benchmarks angle) A reusable benchmark: permission-layout
    generator with tunable selectivity and alignment, the enterprise scenario with canaries, metrics,
    and a harness covering many stores and permission systems.

## Research questions

RQ1. How does retrieval quality under permission filters depend on selectivity and alignment, for
     post-filtering, widening post-filtering and in-index pre-filtering?
RQ2. How faithfully do production vector stores implement filter semantics, and what classes of
     disagreement exist? Does a two-layer design catch them in practice?
RQ3. What do production stores' filtered ANN implementations deliver under realistic permission
     filters, and when do they silently under-retrieve? Can under-retrieval be detected and mitigated
     cheaply?
RQ4. What does enforcing an external permission system cost (authorizer latency, caching, list
     truncation, fail-closed availability), and how fresh are revocations?
RQ5. Does the design prevent leaks end to end, including to the LLM's answer, under adversarial
     prompts? (Out of scope but measured: prompt injection inside permitted content.)

## Experiments needed beyond what exists

- E1 Repeats and confidence intervals: at least 5 seeds for layout generation and query sampling;
  bootstrap CIs for recall; report hardware and versions.
- E2 Recall-latency curves per store under permission filters (ef_search, num_candidates,
  max_scan_tuples, Qdrant search options), not single default points.
- E3 Continuous alignment sweep instead of three discrete layouts.
- E4 Filter-size scaling: 1 to 40,000 groups per subject; latency and failures per store.
- E5 Under-retrieval detection and mitigation (e.g. exact-search fallback when fewer than k hits
  return), with its latency cost.
- E6 Authorizer cost: OPA, OpenFGA, SpiceDB, Cerbos with and without caching; ListObjects truncation
  thresholds and their effect on strategy and recall; rerun OpenFGA (the 2026-10-24 run timed out on
  start-up).
- E7 Fault injection: authorizer outages and slowness; fail-closed availability cost.
- E8 Revocation latency end to end per store and permission system.
- E9 Baselines: naive top-k then filter; wardowl post-filter; PostgreSQL row-level security; one index
  per tenant; store-native ACL features where accessible; filtered-ANN algorithms (e.g. ACORN) where a
  store exposes them.
- E10 A real or realistic ACL dataset if the literature review finds one.

## Risks

- Prior art: enterprise search already studied early vs late binding of document-level security, and
  databases already enforce access control by query modification. The paper must credit this and claim
  only what is new: the ANN/RAG setting, the measured behaviour of today's stores, the two-layer design
  with stated guarantees, the cross-store differential testing, and the end-to-end canary evaluation.
- "Engineering, not research" criticism: answer with formalisation, guarantees, a principled study with
  CIs, and findings that generalise beyond the library (under-retrieval in production stores).
- Venue fit: NeurIPS/ICML main tracks are a weak fit for a systems/security study; the Datasets and
  Benchmarks track, security venues and database venues are stronger. To be settled by the venue review.
- Authorship and disclosure must follow the target venue's and arXiv's policies.
