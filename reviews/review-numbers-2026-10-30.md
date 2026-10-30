# Numbers audit, 2026-10-30 (independent agent; report only)

Checked against evidence/, investigations/, disclosure/, evidence/raw (X1, X8) and the results branches
results/x2-x5, x3-x6, x4-x7. Everything not listed matched and rounded correctly (every table except
the compute table; the conformance counts; related-work figures; leak-bound arithmetic; 3,069
injection total; 2,657 = 992 + 574 + 1,091; 783,888 = 653,638 + 64,845 + 65,405). Line numbers refer
to the files as of commit 4dcd2e9.

## (A) Wrong number or verdict
1. quality.tex:194-195 "20.1% of the empty answers came from questions whose first readable row lay
   within the first half of the scan's reach, short of the 95% we had predicted". P1(a) predicts at
   least 95% beyond half the reach; observed 0.799. Fix: "79.9% ... lay beyond half the scan's
   reach, short of the 95% we had predicted".
2. limits.tex:41 "(Qdrant's by up to 0.086)": 0.086 is X1 as-run only; tab:qual-qdrant has 0.120
   and 0.127; X2 MS MARCO spanned 0.119. Fix: "by up to 0.13".
3. quality.tex:124-125 per-tenant graphs "the fastest configuration": hnsw_ef 64 is faster (5.963 vs
   6.580 ms). Fix: "faster than the as-run layout".
4. quality.tex:82-83 cap "of a few percent of the segment": the cap is about 4/avg_links, 12.5% to
   17% (investigations/filtered-recall-gaps.md:272-273, 428). Fix: "roughly an eighth".
5. conclusion.tex:18-19 "an exact search within a bound repaired them": bounded arms repaired none
   of Qdrant's 1,091 short answers on MS MARCO; B = 1,000 repaired 0.5% of pgvector's 1.7%. Fix:
   unbounded repaired all; bounded caveat.
6. intro.tex:80-81, conclusion.tex:16 "lost a third of its recall": e2e fast mode 0.732-0.746 vs
   0.987-0.996, about a quarter; a third (0.343) is X1 P4 only. Fix: "about a quarter".
7. main.tex:38 "across 14 vector stores": Pinecone skipped in both campaign runs; 13 tested.

## (B) Inconsistent across sections
8. background.tex:191-194 "4.6e-6 that 653,638 checked hits" vs 783,888 elsewhere (3.8e-6).
9. conformance.tex:265-266 Chroma row "about 40,000": threshold 15,500-16,500 (16,437-16,500 in the
   reproducer). Fix: "about 16,500 or more".
10. quality.tex:168 "against the audit's 0.691": table shows fast-mode 0.695; 0.691 is the first run.
11. quality.tex:253-255 X2 V2 check cites tab:qual-x0 (four-run means) but the check used the first
    run's values. Cite the first run.
12. main.tex:40-41 vs intro.tex:75-76 vs quality.tex:55-56: "ranged from 0.55 to 1.00" without
    "mean" in the abstract; 1.00 is the FAISS exact control; worst single run 0.535; "ten store
    configurations" are nine stores with pgvector split by mode. Harmonise.
13. appendix.tex:104,106,107 job counts vs evidence: conformance run 2 10 vs 8; X7 rerun 8 vs 5;
    X3/X6 15 vs 14. Settle the counting rule (with orchestration jobs or not).
14. appendix.tex:102 X1 run 2 "1 GPU session, 4 CPU sessions" vs evidence/x1-underretrieval-run2.md:15
    listing x1run2-prep as CPU. Correct the evidence (prep ran in x1run2-prep-gpu).

## (C) Not supported by evidence files
15. appendix.tex:98-109 job hours and several wall clocks are in no evidence file. Add a compute
    evidence file (jobs API).
16. limits.tex:63-66 "For each fault in a third-party component that our experiments found, we
    prepared a report": only Redis, MongoDB, Chroma, Cerbos have drafts; SpiceDB staleness, OPA's
    residual, pgvector plan switching have none. Narrow the claim or draft notes.
17. conformance.tex:97 "plants 18 faulty backends and six faulty authorizers": unsupported; main now
    has 22 backend subclasses incl. PR #168's. Recount at the evaluated commit.
18. quality.tex:536-538 CI claim for the Chroma fix: only a commit message. Add an evidence entry
    (PR #187 CI green, merged 2026-10-30).
19. conformance.tex:143-144, 252-253 MongoDB 8,181 stated as fact (now corrected to 8,191 by the
    reproducer run; keep consistent everywhere).
20. quality.tex:178-180, intro.tex:79-81 autovacuum stated as the reason: evidence marks it an
    inference. Fix: "consistent with".

## (D) Precision or wording
21. intro.tex:97-98 widening "paired AUC 0.80 to 0.98" omits pgvector 0.662 at m=100, p=10%.
22. main.tex:39, intro.tex:60-61 "found six classes": the campaign added five entries and confirmed a
    sixth (Cerbos); conformance.tex:132 says violations fall into two classes. Fix: "found five and
    confirmed a sixth".
23. intro.tex:70-73 "revocation measurements falsified three predictions ... OPA": OPA's is X4-H3
    (filter agreement); four verdict rows were falsified (X4-H3, X7-H1, X7-H3, X7-H5).
24. intro.tex:89-91 "exact repair left none empty or short": unbounded arm only.
25. intro.tex:84-85, conclusion.tex:14-15 "0.5% to 10% harder in five of nine stores": H2.4 is for
    clustered layouts, negatively correlated questions, one disjunction. Add the qualifier.
26. conformance.tex:153-155 Chroma "refused 20 writes ... 20 queries": 20 runs each.
27. conformance.tex:151-152 all Elasticsearch errors attributed to the 32,766-byte term: 4 of 20
    were a query-side x_content_parse_exception.
28. engines.tex:132 "22 to 30 ms": x4d_latency.csv 21.9 to 29.4. Fix "22 to 29".
29. quality.tex:134-136 "varied by up to 0.086 between three builds": as-run setting only.
30. e2e.tex:126-127 "3 to 25 empty answers": the prediction counted people with no results.
31. e2e.tex:127-129, quality.tex:179 "fast in three and exact in five": X8-FGA seed 11 was a
    mixture. Fix: "fast by its median in three, one of them a mixture".
32. intro.tex:77-78 "0.37 on company documents, 0.95 with per-tenant graphs": unlike subsets; as-run
    overall 0.656 vs 0.952.
33. quality.tex:113-114 caption "Run 1 agreed within the range over builds (per-tenant 0.943)": differs
    by 0.009, nine times the range 0.001. Fix: "within 0.05" (also in evidence).
34. limits.tex:38 "three builds per store and corpus over ten permission layouts": ten MS MARCO layouts
    plus the enterprise layout.

## (E) Stale
35. background.tex:130-132 "in the run of Section e2e, where pgvector returned no hits to ten".
36. background.tex:211-212 "in the run of Section e2e it ... caused most of the recall loss".
37. system.tex:145-147 "In the run of Section e2e, wardowl thus reported empty answers as complete".
38. limits.tex:22-24 tbd results of reproducers (now filled; MongoDB reproduced in run 41008151303).
    Drafts carry a placeholder run id "RUN3" in disclosure/redis.md:4, chroma.md:5, cerbos.md:5.
39. Comments: conformance.tex:7 "run 2 pending"; conformance.tex:17 PRs "were open" (all five merged
    2026-10-30, none released); main.tex:2-3 and appendix.tex:4-5 mention \tbd markers.

## Remaining \tbd (limits.tex)
- filing dates, links and vendor responses (Syed files before arXiv);
- final human check of every reference (Syed);
- archive DOI (Zenodo; must include X2/X5 and X4/X7 artifacts with 90-day retention, the
  conformance artifacts never downloaded, the X0 Kaggle outputs).
