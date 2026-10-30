# Bibliography status: wardowl permission-aware retrieval paper

Built 2026-10-26 from the six notes files in `D:\CV_2\research_notes\Permission aware retrieval literature review\` and the citations in `D:\CV_2\reports\Permission aware retrieval literature review.md`.

## Summary

| Item | Count |
|---|---|
| BibTeX entries found in the notes (4 of the 6 files carry BibTeX; `industry_systems.md` and `venues_and_policies.md` carry none) | 239 (43 + 70 + 80 + 46) |
| Duplicate records merged | 26 (into 15 works) |
| Unique works from the notes | 213 |
| New entries added for web pages the report cites that had no BibTeX | 37 (16 vendor/web, 21 venue/policy) |
| `references.bib` | 187 entries: 179 papers and preprints (113 published, 66 arXiv-only) + 8 standards and specifications |
| `web.bib` | 63 entries: 40 vendor docs, blogs, repositories and news + 23 venue/policy pages (planning only) |
| Status verified-now / verified-by-notes / partial | 242 / 3 / 5 |
| Entries dropped as unverifiable | 0 (fields were dropped instead, listed below) |
| Excluded works (do not cite) | listed in "Do not cite" |

## Verification codes

- **Status.** `verified-now` means title, authors, venue and year were re-checked on 2026-10-26 against a primary record. `verified-by-notes` means the notes verified it and it was not re-checked today. `partial` means at least one field could not be verified and was omitted, or the title could not be read. `unverified-excluded` means it is not in either file.
- **Checked.** `AX` = arXiv API (title, authors, dates, comment, journal-ref, primary class). `CR` = Crossref API (title, authors, container, volume, issue, pages, dates). `ACL` = ACL Anthology BibTeX. `UX` = USENIX presentation page. `PMLR`, `NIPS`, `MLSYS`, `JMLR` = proceedings page or proceedings BibTeX. `DC` = DataCite via doi.org. `RFC` = RFC Editor text. `GH` = GitHub page or API. `PG` = the page's own title, heading or metadata. `SR` = search-engine result (secondary). `N` = notes only.
- **Flags.** `C` = on the core-precedent list in the task. `R` = cited in the report.

## Key rule

`<first author's last name><year><first significant title word>`, lowercase ASCII, diacritics stripped (Büttcher becomes `buttcher`), spaces, hyphens and apostrophes removed. Leading stopwords are skipped: a, an, the, on, of, in, to, for, and, is, are. Corporate authors use a short organisation name (`oasis`, `nist`, `owasp`, `mitre`, `mcp`, `openfga`, `arxiv`, and so on). Collisions get `a`/`b`/`c` suffixes (`fong2011relationshipbaseda/b`, `neurips2026evaluationsa/b/c`, `icml2026icmla/b`, `arxiv2025attentiona/b`). Undated web pages carry the access year (2026) in the key and have no `year` field.

## Corrections made against the notes

1. **Zeng et al. 2024 author order.** Crossref's author order differs from the paper. The ACL Anthology record and arXiv agree, and that order is used. The evaluation notes' `and others` is replaced by the full list. Pages 4505–4524 confirmed.
2. **RFC 8693 authors.** Crossref omits B. Campbell (Ed.). The RFC Editor text lists Jones, Nadalin, Campbell (Ed.), Bradley and Mortimore, January 2020, Standards Track. All five are kept.
3. **Big-ANN NeurIPS'23.** arXiv v1 lists 23 authors. The NeurIPS 2025 proceedings (Datasets and Benchmarks Track) list 21 in a different order, without Frank Liu and Zihao Wan. The proceedings list is used. Pages 76394–76408.
4. **Big-ANN NeurIPS'21.** The full 12-author list (arXiv and PMLR 176:177–189) replaces `and others`. PMLR misspells "Krishnaswamny"; the correct spelling is used.
5. **Bouthillier et al. (MLSys 2021).** The MLSys proceedings list 16 authors, including Nazanin Mohammadi Sepahvand and without Dmitriy Serdyuk. arXiv lists 17. The MLSys list is used, with volume 3 and pages 747–769 added.
6. **Agarwal et al. (NeurIPS 2021).** Volume 34 and pages 29304–29320 added from the proceedings BibTeX.
7. **BEIR.** arXiv spells the title "Heterogenous". The proceedings title ("Heterogeneous") is used, with volume 1 of the NeurIPS Datasets and Benchmarks proceedings.
8. **PoisonedRAG.** Converted from an arXiv `@misc` ("to appear") to the published USENIX Security '25 paper, pages 3827–3844. Key changed to `zou2025poisonedrag`.
9. **PQS (OSDI 2020).** Pages 667–682 and ISBN added from the USENIX page.
10. **Cedar (PACMPL).** Volume 8 and issue OOPSLA1 added. The notes omitted them as unverified; Crossref now confirms them. **Guarnieri and Basin**: volume 7, issue 12 added. **Sieve (Pappachan et al.)**: volume 13, issue 12 added.
11. **HoneyBee.** The arXiv title carries "[Technical Report]". The published PACMMOD 4(1) title is used, and four records are merged.
12. **VecBench.** The fourth author is Guoliang Li. The notes had "G. Li", marked UNVERIFIED. Pages 1–27 added.
13. **GAAF.** The first author is Mengyang Ma (notes: "M. Ma", UNVERIFIED), and the venue is ICS '26, the 40th ACM International Conference on Supercomputing.
14. **LBGraph.** Its venue, unresolved in the notes, is SSDBM 2026 (Proceedings of the 38th International Conference on Scalable Scientific Data Management).
15. **Nova.** The first author is Dechuang Chen (notes: "D.").
16. **Vearch (Middleware '18).** The published record lists 7 authors and spells "Zhenyuan Ni". arXiv lists 6 and spells "Zhenyun". The published record is used.
17. **Iff et al.** The published record (SIGIR '26) spells "Brügger"; arXiv spells "Bruegger". The `@misc` arXiv record and the `@inproceedings` SIGIR record are merged into `iff2026benchmarking`.
18. **IsolateGPT** uses the NDSS title ("...for LLM-Based Systems"); the arXiv title adds "Agentic". **ALGEN** uses the ACL title ("via Cross-Model Alignment and Generation"); the arXiv title reads "using Alignment and Generation".
19. **Molloy et al. (SACMAT '09).** DOI 10.1145/1542207.1542224 and pages 95–104 added. The notes had no DOI.
20. **Pineau et al. (JMLR).** The full 8-author list and pages 1–20 replace `and others`. **Croissant**: the full 31-author list and pages 82133–82148. **Schloegel et al.**: the full 10-author list and pages 1974–1993.
21. **Pages added from Crossref** (the notes lacked them): Morris 12448–12460, Naseh 1245–1259, Greshake 79–90, Song and Raghunathan 377–390, MBA 2894–2907, AgentDojo 82895–82920, AgentPoison 130185–130213, InjecAgent 10471–10506, Zhong (EMNLP) 13764–13775, SAGE 24538–24569, GEIA 14022–14040, Huang 4193–4205, Chen 7808–7827, ALGEN 24330–24348, AirGapAgent 3868–3882, Conseca 8–17, Li et al. (PACMMOD) 1–26, Lu et al. 1–26, PACMMOD/PVLDB articles throughout.
22. **Song et al. (IEEE TSE).** Volume 52, issue 8, pages 2410–2426 added.
23. **FiQA subtitle and QuickCheck full title.** Both were flagged unverified in the notes. Crossref returns both as subtitle fields, so both are now verified.
24. **Lucene/Elastic blog.** The notes' title was paraphrased ("check exact title"). The real title is "Filtered HNSW & kNN search in Lucene and Elasticsearch", by Benjamin Trent, 27 February 2025.
25. **The Register (Asana).** The notes' headline was paraphrased. The real headline is "Asana's cutting-edge AI feature ran into a little data leakage problem", by Jessica Lyons, 18 June 2025.
26. **Weaviate and Qdrant pages.** The notes' titles were descriptive labels. Real: "How we speed up filtered vector search with ACORN" (Rodriguez, Trengrove, Hwang, 19 November 2024) and "Filtering in Vector Search: When to Use What" (Aquino, Myriel, 10 September 2024). Milvus is "Implement Multi-tenancy" (notes: "Multi-tenancy strategies"). The Cerbos API page is "The Cerbos API". OpenFGA's page is "Perform a list objects call".
27. **Invariant Labs blog.** Title confirmed; authors (Marco Milanta, Luca Beurer-Kellner) and date (2025-05-26) added.
28. **MITRE ATLAS title.** The notes' "Artificial-Intelligence Systems" is corrected to "AI Systems", as in the data file. The data file `dist/v6/ATLAS-2026.09.yaml` is version 2026.09, modified 2026-09-15.
29. **IETF drafts.** Authors added (the notes had none). draft-klrc-aiagent-auth-03 is by Kasselman, Lombardo, Rosomakho, Campbell, Steele and Parecki, and is dated **6 July 2026**, not September. draft-oauth-ai-agents-on-behalf-of-user-02 is by Senarath and Dissanayaka, dated **26 August 2025**; the notes' "Feb 2026" was its expiry date (27 February 2026). That draft has **expired**.
30. **NVD record.** The descriptive title from the notes is replaced by the record ID. The CVSS scores and CWE were re-confirmed through the NVD API.
31. **RAG-Thief.** The v1 title, flagged unverified in the notes, is confirmed: "RAG-Thief: Scalable Extraction of Private Data from Retrieval-Augmented Generation Applications with Agent-based Attacks" (21 November 2024, 5 authors). v2 adds Yang Chen.
32. **Pebblo.** The URL the report cites (`python.langchain.com/.../pebblo_retrieval_qa`) now redirects to a 404. The entry points to the live LangChain Reference page instead.
33. **Qdrant v1.16.0.** The release date is 17 November 2025 and v1.15.0 is 18 July 2025, both from the GitHub API. The notes had inferred the year.

## Fields dropped (entries kept)

- `wang2007correctness`: `pages` removed. The start page 555 came only from the VLDB file name, which may be a session number. The end page 566 was marked unverified, no DOI exists, DBLP sat behind a bot check, and DBScholar shows no pages.
- `fagin2003searching`: `pages` removed. Crossref and OpenAlex give only the start page (366). The end page (375) came from Bailey et al.'s reference list.
- `bailey2006secure`: pages 493–502 kept. Crossref confirms the start page, and the end page is corroborated by DBLP through a search result and by the notes' secondary bibliography, but DBLP itself could not be opened.
- Paraphrased or descriptive titles in the notes' web entries were replaced by the pages' real titles (see corrections 24–30).
- `pgvector`: the notes' parenthetical "(README: filtering and iterative index scans, v0.8.0+)" was moved from the title into `note`.

## Entries dropped

None was dropped for being unverifiable. The only removals are the 26 duplicate records merged into 15 works:
HoneyBee (4 records → `zhong2026honeybee`), Filtered-DiskANN (4 → `gollapudi2023filtereddiskann`), ACORN (4 → `patel2024acorn`), HNSW (3 → `malkov2020efficient`), Veda (3 → `han2026dont`), Policy-aware vector search (3 → `yalamarthi2026policyaware`), Curator (3 → `jin2024curator`), PermLLM (3 → `jayaraman2025permissioned`), Mu et al. (2 → `mu2026towards`), Wutschitz et al. (2 → `wutschitz2023rethinking`), Amanbayev et al. (2 → `amanbayev2026filtered`), Iff et al. (2 → `iff2026benchmarking`), Big-ANN'23 (2 → `simhadri2025results`), Big-ANN'21 (2 → `simhadri2022results`), Zeng et al. 2024 (2 → `zeng2024good`). In each merge the published version wins, and only verified fields were carried over.

## Do not cite (unverified-excluded)

| Work | Reason |
|---|---|
| Huang et al., "Give Them an Inch and They Will Take a Mile: Understanding and Measuring Caller Identity Confusion in MCP-Based AI Systems", arXiv:2603.07473 | **Withdrawn.** The arXiv v2 comment (checked 2026-10-26) reads "Withdrawal due to some flaws in experimental methodology and unresolved ethical issues in data collection." No entry was created. |
| Qi et al. cited as "ICLR 2025" | The venue could not be verified (OpenReview sits behind a bot check, and no proceedings record was found). Cite `qi2024follow` as an arXiv preprint only. |
| `wang2022navigable` (NHQ preprint, arXiv:2203.13601) used for results | Filtered-DiskANN's authors could not reproduce its results. Cite the NeurIPS 2023 version, `wang2023efficient`. The entry is kept only for completeness. |
| `senarath2025oauth` as a live draft | It expired on 27 February 2026 and has no IETF standing. Cite it, if at all, as an expired individual draft. |
| RAG-Thief cited under its v1 title as the current paper | It was retitled in v2 (CopyBreakRAG). Use `jiang2024feedbackguided`; the note records the v1 title. |
| Curator (SIGMOD 2026), arXiv:2601.01291, "Curator: Efficient Vector Search with Low-Selectivity Filters" | This is a different paper from `jin2024curator`; do not conflate them. It is not in either file because the notes gave no BibTeX (snippet-level). arXiv confirms 7 authors and "Accepted at SIGMOD 2026", so add it if the paper needs it. |
| Grey literature in `filtered_vector_search.md`: Tampere 2024 thesis, Research Square preprint 10.21203/rs.3.rs-7338381/v1, SNU 2026 dissertation, IJETCSIT 2026 "Silo, Pool, and Bridge" article | Not peer reviewed and not read; the notes say "cite with care or omit". No entries. |
| Concentric AI and ShareGate oversharing figures as primary data | Known only from secondary coverage (`pogorelec2025genai`; ShareGate through IT Brief). Not checked against the primary reports. |
| Items marked [U] in `evaluation_and_testing_methodology.md` without BibTeX: McKeeman 1998, Chen/Cheung/Yiu 1998 tech report, Slutz 1998 (RAGS), Ene et al. SACMAT 2008, the Secret Sharer exposure formula, Argus (arXiv 2510.06663), JoinEquiv (arXiv 2606.23294), VectorDBBench, OSS-Fuzz | Not verified in the notes and not in the report. No entries. |
| Hawking 2004 (ADC, "Challenges in Enterprise Search") | The notes did not verify its DOI or content. No entry. |
| Authors' own evidence files the report links (Kaggle run 2026-10-24, recall-gap investigation, paper plan v0) | Unpublished internal material, not bibliography entries. |
| Vendor pages in `industry_systems.md` and `venues_and_policies.md` that the report does not cite (Glean, Amazon Q Business, Vertex AI Search, Elastic and OpenSearch DLS, Supabase, Weaviate RBAC, Pinecone multitenancy, Zilliz, MongoDB Atlas, Permit.io, Pangea, Aserto, Descope, PAIG, Onyx, Slack AI, GeminiJack, ForcedLeak, CW1226324 and others) | Not added. Add them from the notes' URLs if the paper cites them, and re-read each title first. |

## Old key → new key

`(web)` marks entries that moved to `web.bib`. `=` means the key is unchanged.

**access_control_in_search_and_databases.md (43):** buettcher2005security→buttcher2005security; bailey2006secure =; mangtani2006dls→mangtani2006documentlevel (web); zerr2008zerber =; zerr2009zerberr =; fagin2003workplace→fagin2003searching; stonebraker1974access =; griffiths1976authorization =; motro1989access =; rizvi2004extending =; lefevre2004limiting =; kabra2006redundancy =; wang2007correctness =; guarnieri2014optimal =; pappachan2020sieve =; byun2004querymod→byun2004access (web); oracle19cvpd→oracle2026using (web); postgresql_rls→postgresql2026row (web); pang2019zanzibar =; fong2011rebac→fong2011relationshipbaseda; fong2011rebacpolicies→fong2011relationshipbasedb; openfga_search→openfga2026search (web); openfga_listobjects→openfga2026perform (web); authzed_listendpoint→authzed2026protecting (web); cutler2024cedar =; disselkoen2024howwebuiltcedar→disselkoen2024how; kastner2025cedarkeynote→kastner2025cedar; sandall2018opasql→sandall2018write (web); opa_filtering_pe→opa2026evaluating (web); cerbos_planresources→cerbos2026cerbos (web); oso_listfiltering→oso2026list (web); oasis2013xacml→oasis2013extensible; zhong2025honeybee→zhong2026honeybee; han2026stirpot→han2026dont; yalamarthi2026policyaware =; jin2024curator =; gollapudi2023filtereddiskann =; patel2024acorn =; malkov2020hnsw→malkov2020efficient; jayaraman2025permissioned =; lorenzo2025arbiter =; mu2026securerag→mu2026towards; ahmed2026beyond =.

**filtered_vector_search.md (70):** malkov2020hnsw→malkov2020efficient; subramanya2019diskann =; singh2021freshdiskann =; douze2024faiss =; gollapudi2023filtereddiskann =; patel2024acorn =; wang2023nhq→wang2023efficient; wang2022nhqpreprint→wang2022navigable; wu2022hqann =; gupta2023caps =; cai2024ung→cai2024navigating; xu2024irangegraph =; zuo2024serf =; engels2024window→engels2024approximate; li2025sieve =; aitaomar2025rwalks =; liang2024unify =; peng2025dsg→peng2025dynamic; jiang2025digra =; zhang2025rangepq→zhang2025efficient; wang2025wow =; mohoney2023hqi→mohoney2023highthroughput; sehgal2025navix =; ye2025compass =; yang2025elastic =; xia2026e2e =; kim2026racorn→kim2026racorn1; wang2026lssg→wang2026fast; zheng2026lbgraph→zheng2026labelbalanced; ma2026gaaf =; guo2026pipeannfilter =; chatzakis2026vader =; xiong2026routing→xiong2026queryaware; almamun2026ifvs =; uemura2026simple =; aslam2026adaptive =; wang2021milvus =; wei2020analyticdbv =; zhang2023vbase =; li2018vearch→li2018design; ma2025chase =; chen2026nova =; zhang2024pgvectorlimits→zhang2024there; sanca2024accesspaths→sanca2024efficient; lu2026filteragnosticpg→lu2026indepth; amanbayev2026fanns→amanbayev2026filtered; pan2024survey =; lin2025fannssurvey→lin2025survey; chronis2025fvstutorial→chronis2025filtered; simhadri2025bigann23→simhadri2025results; simhadri2022bigann21→simhadri2022results; li2025attrfiltering→li2025attribute; iff2026fannsbench→iff2026benchmarking; shi2025fannsbench→shi2025filtered; zhang2026vecbench =; zhong2026honeybee =; han2026veda→han2026dont; yalamarthi2026policyaware =; jin2024curator =; das2026staleness→das2026recallbounded; thuillier2026keyparam→thuillier2026keyparametrized; wutschitz2023ifc→wutschitz2023rethinking; pgvector→pgvector2026pgvector (web); qdrantfiltering→aquino2024filtering (web); weaviateacorn→rodriguez2024how (web); elasticfilteredknn→elastic2026filter (web); trent2025luceneacorn→trent2025filtered (web); opensearchfiltering→opensearch2026efficient (web); milvusmultitenancy→milvus2026implement (web); pineconefiltering→pinecone2026filter (web).

**rag_privacy_and_security.md (80):** zeng2024good =; qi2024spill→qi2024follow; jiang2024feedback→jiang2024feedbackguided; dimaio2025pirates =; anderson2025mydata→anderson2025my; li2025generating =; liu2025mba→liu2025maskbased; naseh2025riddle =; burnat2026collusion→burnat2026auditing; liu2026protection =; roychowdhury2024confusedpilot =; thornton2026pivot→thornton2026retrieval; bhatt2025participant→bhatt2025enterprise; sun2026spliceleak→sun2026agentassisted; balashov2025multistage =; greshake2023not =; evertz2024whispers =; reddy2025echoleak =; zou2024poisonedrag→zou2025poisonedrag; zhong2023poisoning =; chen2024agentpoison =; shafran2024machine =; zhong2026honeybee =; han2026stir→han2026dont; yalamarthi2026policy→yalamarthi2026policyaware; patel2024acorn =; gollapudi2023filtered→gollapudi2023filtereddiskann; arceo2026securing =; jayaraman2025permissioned =; almasoud2026sdrag =; zhou2025privacyaware =; zhang2026burn→zhang2026burnafteruse; byun2025secmulti→byun2025secure; addison2024cfedrag =; koga2024dprag→koga2024privacypreserving; zeng2025sage→zeng2025mitigating; siddiqui2024permissive =; costa2025fides→costa2025securing; wu2024fsecure→wu2024systemlevel; wutschitz2023rethinking =; sanyal2025orgaccess =; fei2026text2sqlrbac→fei2026benchmarking; mu2026securerag→mu2026towards; song2020information =; li2023geia→li2023sentence; morris2023text =; seputis2025rethinking =; huang2024transferable =; chen2024multilingual→chen2024text; chen2025algen =; zhang2025zsinvert→zhang2025universal; liu2024eguard =; hardy1988confused =; rfc8693→jones2020oauth; mcp2026authorization→mcp2026model; south2025authenticated =; shi2025sok =; hou2026mcp→hou2026model; song2026beyond =; zhou2026mcpauth→zhou2026first; kumar2026gateway =; radosevich2025mcpaudit→radosevich2025mcp; narajala2025enterprise→narajala2025enterprisegrade; debenedetti2024agentdojo =; zhan2024injecagent =; zhang2024asb→zhang2024agent; debenedetti2025camel→debenedetti2025defeating; shi2025progent =; wu2025isolategpt =; bagdasarian2024airgapagent =; tsai2025conseca→tsai2025contextual; nist2024ai6001→nist2024artificial; owasp2025llm08→owasp2025llm082025; mitre2026atlas =; draft-klrc-aiagent-auth-03→kasselman2026ai; draft-oauth-ai-agents-obo-02→senarath2025oauth; nvd2025cve32711→nvd2025cve202532711 (web); invariant2025githubmcp→milanta2025github (web); register2025asana→lyons2025asanas (web); microsoft2026copilotprivacy→microsoft2026data (web).

**evaluation_and_testing_methodology.md (46):** thakur2021beir =; maia2018fiqa→maia2018www18; bajaj2016msmarco→bajaj2016ms; aumuller2020annbenchmarks =; simhadri2022bigann21→simhadri2022results; simhadri2025bigann23→simhadri2025results; malkov2020hnsw→malkov2020efficient; patel2024acorn =; gollapudi2023filtereddiskann =; zhong2026honeybee =; jin2024curator =; iff2025fanns→iff2026benchmarking; amanbayev2026filtered =; lim2026hcbgen→lim2026revisiting; arora2023concurrentqa→arora2023reasoning; ryan2025enronqa =; jayaraman2025permllm→jayaraman2025permissioned; molloy2009evaluating =; smetters2009users→smetters2009how; nobi2022mlac→nobi2022machine; rigger2020pqs→rigger2020testing; rigger2020norec→rigger2020detecting; rigger2020tlp→rigger2020finding; ba2023qpg→ba2023testing; ba2024dqp→ba2024keep; kamm2023graphpartition→kamm2023testing; chen2018metamorphic =; segura2016survey =; xie2025vdbmsbugs→xie2025toward; wang2025vdbmsroadmap→wang2025towards; claessen2000quickcheck =; maciver2019hypothesis =; atheris→google2026atheris (web); klees2018evaluating =; schloegel2024sok =; carlini2019secretsharer→carlini2019secret; zeng2024goodbad→zeng2024good; dodge2019showyourwork→dodge2019show; bouthillier2021variance→bouthillier2021accounting; agarwal2021precipice→agarwal2021deep; pineau2021reproducibility→pineau2021improving; smucker2007comparison =; urbano2019significance→urbano2019statistical; akhtar2024croissant =; neurips2026checklist→neurips2026neurips (web); neurips2026ed→neurips2026call (web).

**industry_systems.md and venues_and_policies.md:** no BibTeX. The 37 new web entries come from the report's citations of pages in these notes and are marked "new" below.

## Per-entry status: references.bib (187)

### A. Enterprise search, database access control, authorization systems

| Key | Short title | Flags | Status | Checked | Warning |
|---|---|---|---|---|---|
| buttcher2005security | Security model for full-text file-system search (FAST '05) | C R | verified-now | UX (title, authors, venue, pp. 169–182) | |
| bailey2006secure | Secure search in enterprise webs (CIKM '06) | C R | verified-now | CR (start page 493), SR (DBLP 493–502) | End page corroborated only secondarily |
| zerr2008zerber | Zerber (EDBT '08) | | verified-now | CR | |
| zerr2009zerberr | Zerber+R (EDBT '09) | | verified-now | CR | Content snippet-level in notes |
| fagin2003searching | Searching the workplace web (WWW '03) | | partial | CR, OA | Pages omitted (end page unverified) |
| stonebraker1974access | Access control by query modification (ACM '74) | C R | verified-now | CR | Notes' content came from Byun's slides; full text not read |
| griffiths1976authorization | System R authorization mechanism (TODS) | | verified-now | CR | |
| motro1989access | Authorization via view definitions (ICDE 1989) | | verified-now | CR | Content not read in notes |
| rizvi2004extending | Query rewriting for FGAC; Truman/non-Truman (SIGMOD '04) | C R | verified-now | CR | Re-check Section 2 wording before quoting Truman definitions |
| lefevre2004limiting | Limiting disclosure in Hippocratic databases (VLDB '04) | | verified-now | CR | |
| kabra2006redundancy | Redundancy and information leakage in FGAC (SIGMOD '06) | C R | verified-now | CR | Content from abstract only |
| wang2007correctness | Correctness criteria of FGAC (VLDB '07) | C R | partial | SR (title, authors, venue), PG (author PDF host) | No DOI; pages omitted |
| guarnieri2014optimal | Optimal security-aware query processing (PVLDB 7(12)) | R | verified-now | CR | |
| pappachan2020sieve | Sieve middleware (PVLDB 13(12)) | | verified-now | CR | Content not read |
| pang2019zanzibar | Zanzibar (USENIX ATC '19) | C R | verified-now | UX (BibTeX) | |
| fong2011relationshipbaseda | ReBAC protection model (CODASPY '11) | | verified-now | CR | Content not read |
| fong2011relationshipbasedb | ReBAC policies and policy languages (SACMAT '11) | | verified-now | CR | |
| cutler2024cedar | Cedar language (PACMPL 8(OOPSLA1)) | C R | verified-now | CR, AX | arXiv extended version has "(Extended Version)" in its title |
| disselkoen2024how | How we built Cedar (FSE Companion '24) | | verified-now | CR | |
| kastner2025cedar | Cedar keynote abstract (SACMAT '25) | | verified-now | CR | One-page keynote abstract |

### B. Filtered ANN search, vector databases, permission-aware vector search

| Key | Short title | Flags | Status | Checked | Warning |
|---|---|---|---|---|---|
| malkov2020efficient | HNSW (TPAMI 42(4)) | C | verified-now | CR, AX | |
| subramanya2019diskann | DiskANN (NeurIPS 2019) | | verified-by-notes | N | Proceedings page misspells an author name (per notes) |
| singh2021freshdiskann | FreshDiskANN | | verified-now | AX | Preprint |
| douze2024faiss | The Faiss library | | verified-now | AX | Preprint |
| gollapudi2023filtereddiskann | Filtered-DiskANN (WWW '23) | C R | verified-now | CR | |
| patel2024acorn | ACORN (PACMMOD 2(3), SIGMOD 2024) | C R | verified-now | CR, AX | |
| wang2023efficient | NHQ (NeurIPS 2023) | | verified-now | CR | |
| wang2022navigable | NHQ preprint, different title | | verified-now | AX | Superseded; results not reproduced per Filtered-DiskANN (see Do not cite) |
| wu2022hqann | HQANN (CIKM '22) | | verified-now | CR, AX | |
| gupta2023caps | CAPS | | verified-now | AX | Preprint; no venue found |
| cai2024navigating | UNG (PACMMOD 2(6)) | | verified-now | CR | |
| xu2024irangegraph | iRangeGraph (PACMMOD 2(6)) | | verified-now | CR, AX | |
| zuo2024serf | SeRF (PACMMOD 2(1)) | | verified-now | CR | |
| engels2024approximate | Window filters (ICML 2024, PMLR 235) | R | verified-now | PMLR, AX | Author is "Ben Landrum" per PMLR |
| li2025sieve | SIEVE (PVLDB 18(11)) | | verified-now | CR, AX | |
| aitaomar2025rwalks | RWalks (PACMMOD 3(3)) | | verified-now | CR | |
| liang2024unify | UNIFY (PVLDB 18(4)) | | verified-now | CR | Issue dated Dec 2024; online 2025 |
| peng2025dynamic | DSG (PVLDB 18(10)) | | verified-now | CR | |
| jiang2025digra | DIGRA (PACMMOD 3(3)) | | verified-now | CR | |
| zhang2025efficient | RangePQ (PACMMOD 3(3)) | | verified-now | CR | |
| wang2025wow | WoW (PACMMOD 3(6)) | | verified-now | CR | |
| mohoney2023highthroughput | HQI (PACMMOD 1(2)) | | verified-now | CR | |
| sehgal2025navix | NaviX | | verified-now | AX | Preprint; venue unverified |
| ye2025compass | Compass | | verified-now | AX | Preprint; venue unverified |
| yang2025elastic | Elastic index selection | | verified-now | AX | Preprint (technical report) |
| xia2026e2e | E2E (KDD '26) | | verified-now | CR, AX | |
| kim2026racorn1 | RACORN-1 | R | verified-now | AX | Preprint, not peer reviewed |
| wang2026fast | LSSG | | verified-now | AX | SIGMOD 2027 per arXiv comment only |
| zheng2026labelbalanced | LBGraph (SSDBM 2026) | | verified-now | CR | |
| ma2026gaaf | GAAF (ICS '26) | | verified-now | CR | |
| guo2026pipeannfilter | PipeANN-Filter | | verified-now | AX | Preprint |
| chatzakis2026vader | VADER | | verified-now | AX | "Appeared in VLDB 2027" per arXiv comment only |
| xiong2026queryaware | Query-aware routing | | verified-now | AX | Preprint |
| almamun2026ifvs | iFVS | | verified-now | AX | 4-page preprint |
| uemura2026simple | Simple graph filtered ANN (full version) | | verified-now | AX | Short version at SISAP 2026 per arXiv comment |
| aslam2026adaptive | Adaptive query-aware hybrid search (EDBT 2026) | | verified-now | DC | |
| wang2021milvus | Milvus (SIGMOD '21) | | verified-now | CR | |
| wei2020analyticdbv | AnalyticDB-V (PVLDB 13(12)) | | verified-now | CR | |
| zhang2023vbase | VBASE (OSDI 23) | | verified-by-notes | N (USENIX page per notes) | |
| li2018design | Vearch / JD visual search (Middleware '18) | | verified-now | CR, AX | arXiv lists 6 authors, published record 7 |
| ma2025chase | CHASE | | verified-now | AX | Preprint |
| chen2026nova | Nova (PVLDB 19(12)) | | verified-now | CR | |
| zhang2024there | Vector data management limits in PostgreSQL (ICDE 2024) | | verified-now | CR | |
| sanca2024efficient | Access paths for vector-relational search (DaMoN '24) | | verified-now | CR | |
| lu2026indepth | Filter-agnostic vector search on PostgreSQL (PACMMOD 4(3)) | | verified-now | CR, AX | arXiv title says "[Experiments and Analysis]" |
| amanbayev2026filtered | Filtered ANN in vector DBs; MoReVec, GLS | R | verified-now | AX | Preprint |
| pan2024survey | Survey of VDBMSs (VLDB J. 33(5)) | | verified-now | CR, AX | |
| lin2025survey | Survey of filtered ANN | | verified-now | AX | Preprint, submitted to VLDB J. |
| chronis2025filtered | Filtered vector search tutorial (PVLDB 18(12)) | | verified-now | CR | |
| simhadri2025results | Big-ANN NeurIPS'23 results (NeurIPS 2025 D&B) | C R | verified-now | CR, NIPS, AX | Proceedings author list (21) differs from arXiv (23) |
| simhadri2022results | Big-ANN NeurIPS'21 results (PMLR 176) | C | verified-now | PMLR, AX | |
| li2025attribute | Attribute filtering experimental study (PACMMOD 3(6)) | R | verified-now | CR, AX | Corrigendum doi:10.1145/3803528 |
| iff2026benchmarking | Filtered ANN on transformer embeddings (SIGIR '26) | | verified-now | CR, AX | |
| shi2025filtered | Unified filtered-ANN benchmark | R | verified-now | AX | Preprint; PVLDB EA&B citation incomplete per notes |
| zhang2026vecbench | VecBench (PACMMOD 4(3)) | R | verified-now | CR | Read at abstract level only in notes |
| lim2026revisiting | HCBGen | R | verified-now | AX | PVLDB 19(10) per arXiv comment only |
| zhong2026honeybee | HoneyBee (PACMMOD 4(1), SIGMOD 2026) | C R | verified-now | CR, AX | arXiv title adds "[Technical Report]" |
| han2026dont | Veda / EffVeda ("Don't Stir the Pot!") | C R | verified-now | AX | Preprint, no venue |
| yalamarthi2026policyaware | Policy-aware vector search vision | C R | verified-now | AX | Workshop vision paper with preliminary results; venue per arXiv comment only |
| jin2024curator | Curator (multi-tenant indexing) | R | verified-now | AX | Preprint; not the SIGMOD 2026 Curator paper |
| das2026recallbounded | Recall-bounded staleness, multi-tenant ANN | R | verified-now | AX | October 2026 preprint |
| thuillier2026keyparametrized | Key-parametrized embeddings for RAG access control (COMPSAC 2026) | | verified-now | CR | Content not read |

### C. RAG privacy and security, LLM access control, embeddings, agents

| Key | Short title | Flags | Status | Checked | Warning |
|---|---|---|---|---|---|
| zeng2024good | Privacy issues in RAG (Findings ACL 2024) | C R | verified-now | ACL, CR, AX | Crossref author order wrong; ACL order used |
| qi2024follow | Spill the beans: RAG datastore extraction | R | verified-now | AX | ICLR 2025 venue unverified |
| jiang2024feedbackguided | CopyBreakRAG (formerly RAG-Thief) | R | verified-now | AX | Retitled; v1 title recorded in note |
| dimaio2025pirates | Pirates of the RAG (ECAI 2025, FAIA) | | verified-now | CR, AX | Volume and pages not in Crossref |
| anderson2025my | Membership inference against RAG (ICISSP 2025) | | verified-now | CR, AX | |
| li2025generating | S2MIA (ICASSP 2025) | | verified-now | CR, AX | |
| liu2025maskbased | MBA (WWW '25) | | verified-now | CR, AX | |
| naseh2025riddle | Riddle Me This (CCS '25) | R | verified-now | CR, AX | |
| burnat2026auditing | Multi-tenant RAG under account collusion | | verified-now | AX | Preprint |
| liu2026protection | Survey of RAG protection by endpoint | R | verified-now | AX | Preprint; ARR recommendation, not yet published |
| roychowdhury2024confusedpilot | ConfusedPilot | R | verified-now | AX | Preprint; Attack 5 details partly from press per industry notes |
| thornton2026retrieval | Retrieval pivot attacks | R | verified-now | AX | Preprint |
| bhatt2025enterprise | Participant-aware access control | R | verified-now | AX | Preprint |
| sun2026agentassisted | SpliceLeak (KV-cache side channel) | R | verified-now | AX | Preprint |
| balashov2025multistage | Multi-stage prompt inference | | verified-now | AX | Preprint |
| greshake2023not | Indirect prompt injection (AISec '23) | | verified-now | CR, AX | |
| evertz2024whispers | Whispers in the Machine | | verified-now | AX | Retitled; DIMVA 2026 per arXiv comment only |
| reddy2025echoleak | EchoLeak case study | | verified-now | AX | AAAI Fall Symposium per arXiv comment only |
| zou2025poisonedrag | PoisonedRAG (USENIX Security '25) | R | verified-now | UX, AX | Now the published version (was "to appear") |
| zhong2023poisoning | Poisoning retrieval corpora (EMNLP 2023) | | verified-now | CR, AX | |
| chen2024agentpoison | AgentPoison (NeurIPS 2024) | | verified-now | CR, AX | |
| shafran2024machine | Machine Against the RAG | | verified-now | AX | USENIX Security 2025 per arXiv comment only |
| arceo2026securing | Vendor-neutral multitenant retrieval (CAIS '26) | R | verified-now | CR, AX | |
| jayaraman2025permissioned | PermLLM (NeurIPS 2025) | R | verified-now | CR, AX | |
| lorenzo2025arbiter | ARBITER | | verified-now | AX | Preprint |
| ahmed2026beyond | LLM agents over structured enterprise data | | verified-now | AX | Preprint; content snippet-level in notes |
| almasoud2026sdrag | SD-RAG | | verified-now | AX | Preprint |
| zhou2025privacyaware | Privacy-Aware RAG (encryption) | | verified-now | AX | Preprint |
| zhang2026burnafteruse | Burn-After-Use / SMTA | | verified-now | AX | Preprint |
| byun2025secure | SecMulti-RAG | | verified-now | AX | Preprint; not per-user access control |
| addison2024cfedrag | C-FedRAG | | verified-now | AX | Preprint; abstract not reviewed in notes |
| koga2024privacypreserving | DP-RAG | | verified-now | AX | Preprint |
| zeng2025mitigating | SAGE synthetic data (EMNLP 2025) | | verified-now | CR, AX | |
| siddiqui2024permissive | Permissive information-flow analysis | | verified-now | AX | Preprint |
| costa2025securing | Fides (IFC for agents) | | verified-now | AX | Preprint |
| wu2024systemlevel | IFC defence against indirect injection | | verified-now | AX | Preprint |
| wutschitz2023rethinking | IFC view of ML-pipeline privacy | | verified-now | AX | Preprint; abstract not reviewed in notes |
| sanyal2025orgaccess | OrgAccess benchmark | R | verified-now | AX | Preprint |
| fei2026benchmarking | Text-to-SQL under RBAC | | verified-now | AX | SIGMOD 2027 per arXiv comment only |
| mu2026towards | Secure RAG survey | | verified-now | AX | Preprint; content snippet-level in notes |
| song2020information | Information leakage in embeddings (CCS '20) | | verified-now | CR, AX | |
| li2023sentence | GEIA (Findings ACL 2023) | | verified-now | CR, AX | |
| morris2023text | vec2text (EMNLP 2023) | C R | verified-now | ACL, CR, AX | Read `seputis2025rethinking` before quoting the 92% figure |
| seputis2025rethinking | vec2text reproducibility study (RecSys '25) | | verified-now | CR | Content not read; may qualify the 92% figure |
| huang2024transferable | Transferable embedding inversion (ACL 2024) | | verified-now | CR, AX | |
| chen2024text | Multilingual embedding inversion (ACL 2024) | | verified-now | CR, AX | |
| chen2025algen | ALGEN (ACL 2025) | | verified-now | CR, AX | arXiv title differs |
| zhang2025universal | ZSInvert | R | verified-now | AX | Preprint |
| liu2024eguard | Eguard | | verified-now | AX | Preprint |
| hardy1988confused | The Confused Deputy (OSR 22(4)) | R | verified-now | CR | |
| south2025authenticated | Authenticated delegation for AI agents | | verified-now | AX | Preprint |
| shi2025sok | SoK: trust-authorization mismatch | | verified-now | AX | Preprint |
| hou2026model | MCP landscape and threats (TOSEM 35(10)) | | verified-now | CR, AX | |
| song2026beyond | MCP attack vectors (IEEE TSE 52(8)) | | verified-now | CR, AX | |
| zhou2026first | Remote MCP server authentication study | R | verified-now | AX | Preprint |
| kumar2026gateway | Enterprise MCP gateway | | verified-now | AX | Preprint |
| radosevich2025mcp | MCP safety audit | | verified-now | AX | SPIE 2026 version has a different author list (not merged) |
| narajala2025enterprisegrade | Enterprise-grade MCP security | | verified-now | AX | Preprint |
| debenedetti2024agentdojo | AgentDojo (NeurIPS 2024 D&B) | R | verified-now | CR, AX | |
| zhan2024injecagent | InjecAgent (Findings ACL 2024) | | verified-now | CR, AX | |
| zhang2024agent | Agent Security Bench | | verified-now | AX | ICLR 2025 per arXiv comment only |
| debenedetti2025defeating | CaMeL | | verified-now | AX | Preprint |
| shi2025progent | Progent | | verified-now | AX | Preprint |
| wu2025isolategpt | IsolateGPT (NDSS 2025) | | verified-now | CR, AX | arXiv title adds "Agentic" |
| bagdasarian2024airgapagent | AirGapAgent (CCS '24) | | verified-now | CR, AX | |
| tsai2025contextual | Conseca (HotOS '25) | | verified-now | CR, AX | |

### D. Evaluation, datasets, testing methodology, reporting

| Key | Short title | Flags | Status | Checked | Warning |
|---|---|---|---|---|---|
| thakur2021beir | BEIR (NeurIPS 2021 D&B) | C R | verified-now | NIPS (BibTeX), AX | arXiv misspells "Heterogenous" |
| maia2018www18 | FiQA challenge (WWW '18 Companion) | | verified-now | CR | |
| bajaj2016ms | MS MARCO | C | verified-now | AX | arXiv only |
| aumuller2020annbenchmarks | ANN-Benchmarks (Information Systems 87) | R | verified-now | CR | The report links the GitHub README (see `erikbern2026annbenchmarks`) |
| arora2023reasoning | ConcurrentQA (TACL 11) | | verified-now | CR, AX | |
| ryan2025enronqa | EnronQA | R | verified-now | AX | Preprint |
| molloy2009evaluating | Evaluating role mining algorithms (SACMAT '09) | R | verified-now | CR | DOI and pages newly added |
| smetters2009how | How users use access control (SOUPS '09) | | verified-now | CR | |
| nobi2022machine | ML in access control survey | R | verified-now | AX | Preprint |
| rigger2020testing | PQS (OSDI 20) | C R | verified-now | UX (BibTeX) | |
| rigger2020detecting | NoREC (ESEC/FSE '20) | C R | verified-now | CR, AX | |
| rigger2020finding | TLP (PACMPL 4(OOPSLA)) | C R | verified-now | CR | |
| ba2023testing | QPG (ICSE 2023) | | verified-now | CR | |
| ba2024keep | DQP (PACMMOD 2(3)) | | verified-now | CR | |
| kamm2023testing | Graph DB query partitioning (ISSTA '23) | R | verified-now | CR | |
| chen2018metamorphic | Metamorphic testing review (CSUR 51(1)) | | verified-now | CR | Issue dated Jan 2019; online Jan 2018 |
| segura2016survey | Survey on metamorphic testing (TSE 42(9)) | | verified-now | CR | |
| xie2025toward | Bugs in vector DBMSs | R | verified-now | AX | Preprint; convenience sample per a third-party review |
| wang2025towards | VDBMS testing roadmap 2030 | R | verified-now | AX | Preprint |
| claessen2000quickcheck | QuickCheck (ICFP '00) | | verified-now | CR | |
| maciver2019hypothesis | Hypothesis (JOSS 4(43)) | | verified-now | CR | |
| klees2018evaluating | Evaluating fuzz testing (CCS '18) | | verified-now | CR | |
| schloegel2024sok | SoK: fuzzing evaluation (IEEE S&P 2024) | | verified-now | CR, AX | |
| carlini2019secret | The Secret Sharer (USENIX Security 19) | C R | verified-now | UX (BibTeX) | Exposure formula not checked in notes |
| dodge2019show | Show Your Work (EMNLP-IJCNLP 2019) | | verified-now | CR | |
| bouthillier2021accounting | Variance in ML benchmarks (MLSys 2021) | R | verified-now | MLSYS (BibTeX), AX | arXiv author list differs |
| agarwal2021deep | Statistical precipice (NeurIPS 2021) | R | verified-now | NIPS (BibTeX) | |
| pineau2021improving | NeurIPS 2019 reproducibility report (JMLR 22(164)) | | verified-now | JMLR (BibTeX) | |
| smucker2007comparison | IR significance tests (CIKM '07) | | verified-now | CR | |
| urbano2019statistical | IR significance testing errors (SIGIR '19) | | verified-now | CR | |
| akhtar2024croissant | Croissant (NeurIPS 2024 D&B) | | verified-now | CR, AX | |

### E. Standards, specifications and threat frameworks

| Key | Short title | Flags | Status | Checked | Warning |
|---|---|---|---|---|---|
| oasis2013extensible | XACML 3.0 (OASIS Standard, 22 Jan 2013) | R | verified-now | PG (cover page and citation format) | |
| jones2020oauth | RFC 8693 OAuth 2.0 Token Exchange | C R | verified-now | RFC, CR | Crossref omits Campbell (Ed.); RFC header used |
| nist2024artificial | NIST AI 600-1 GenAI profile | | verified-now | CR | |
| mcp2026model | MCP specification 2026-07-28: Authorization | C R | verified-now | PG (both authorization pages) | Living spec; the passthrough rule is on the Security Considerations page |
| owasp2025llm082025 | OWASP LLM08:2025 Vector and Embedding Weaknesses | C R | verified-now | PG | No date on page; first prevention item confirmed verbatim |
| mitre2026atlas | MITRE ATLAS data release 2026.09 | R | verified-now | GH (data file header, AML.M0027) | The repo README still advertises 2026.05 as latest; the 2026.09 file exists |
| kasselman2026ai | draft-klrc-aiagent-auth-03 | | verified-now | PG (draft text), datatracker API | Individual draft, work in progress |
| senarath2025oauth | draft-oauth-ai-agents-on-behalf-of-user-02 | | verified-now | PG (draft text), datatracker API | **Expired** 27 Feb 2026 |

## Per-entry status: web.bib (63)

All titles were read from the live page (`PG`) on 2026-10-26 unless stated otherwise. `new` = no BibTeX in the notes; created for a page the report cites.

| Key | Short title | Flags | Status | Checked | Warning |
|---|---|---|---|---|---|
| mangtani2006documentlevel | Google blog: document-level security (2006) | R | verified-now | PG (title, byline, date) | Industry source for the early/late-binding vocabulary |
| byun2004access | Byun slides: access control by query modification | R | verified-by-notes | N (PDF text not extractable today) | Secondary source; cite the primary papers |
| oracle2026using | Oracle VPD (19c Security Guide) | | verified-now | PG | |
| postgresql2026row | PostgreSQL Row Security Policies (v18) | R | verified-now | PG | "current" docs move with releases |
| openfga2026search | OpenFGA: Search With Permissions | R | verified-now | PG | |
| openfga2026perform | OpenFGA: Perform a list objects call | | verified-now | PG | |
| openfga2026openfga | OpenFGA Configuration Options (new) | R | verified-now | PG | |
| openfga2026rag | OpenFGA: RAG Authorization (new) | R | verified-now | PG | The report links the .md URL |
| authzed2026protecting | AuthZed: Protecting a List Endpoint | R | verified-now | PG | |
| authzed2026consistency | AuthZed: Consistency (new) | R | verified-now | PG | |
| sandall2018write | OPA blog: Write Policy in OPA, Enforce in SQL (2018) | R | verified-now | PG | |
| opa2026evaluating | OPA: Evaluating a Data Filter Policy | | verified-now | PG | |
| opa2026writing | OPA: Writing valid Data Filtering Policies (new) | R | verified-now | PG | Notes' content for this page is snippet-level |
| cerbos2026cerbos | The Cerbos API (PlanResources) | R | verified-now | PG | |
| oso2026list | Oso Cloud: List filtering | | verified-now | PG | Notes' content claims are snippet-level |
| pgvector2026pgvector | pgvector README | R | verified-now | PG | |
| aquino2024filtering | Qdrant: Filtering in Vector Search (2024) | R | verified-now | PG (title, authors, date) | Title corrected from the notes |
| qdrant2025release | Qdrant release v1.16.0 (new) | R | verified-now | GH API | |
| rodriguez2024how | Weaviate: speed up filtered search with ACORN (2024) | R | verified-now | PG (title, authors, date) | Title corrected from the notes |
| elastic2026filter | Elastic: Filter approximate kNN results | | verified-now | PG | |
| trent2025filtered | Elastic Labs: Filtered HNSW & kNN in Lucene (2025) | | verified-now | PG (title, author, date) | Title corrected (notes' was paraphrased) |
| opensearch2026efficient | OpenSearch: Efficient k-NN filtering | R | verified-now | PG | |
| milvus2026implement | Milvus: Implement Multi-tenancy | | verified-now | PG | Title corrected from the notes |
| pinecone2026filter | Pinecone: Filter by metadata | R | verified-now | PG | |
| microsoft2026querytime | Azure AI Search: Query-time ACL and RBAC enforcement (new) | R | verified-now | PG | Preview features; behaviour may change |
| aws2026access | Amazon Bedrock: ACL awareness enablement (new) | R | verified-now | PG | The report links the .md variant |
| auth02026authorization | Auth0: Authorization for RAG (new) | R | verified-now | PG | |
| authzed2026langchainspicedb | langchain-spicedb repository (new) | R | verified-now | GH | |
| cerbos2026implementing | Cerbos: Implementing authorization in RAG (new) | R | verified-now | PG | |
| coveo2026coveo | Coveo, Dynamics 365, and Security (new) | R | verified-now | PG | |
| langchain2026pebbloretrieval | LangChain Reference: pebblo_retrieval (new) | R | partial | PG (replacement page) | **The report's URL is dead (404)**; a different page is cited |
| gelevanog2026permissionaware | Clearance repository (permission-aware-rag) (new) | R | verified-now | GH | Unreviewed project; self-reported results |
| microsoft2026data | Microsoft Learn: Data, Privacy, and Security for Copilot | | verified-now | PG | |
| nvd2025cve202532711 | NVD: CVE-2025-32711 (EchoLeak) | R | verified-now | NVD API | Title is the CVE ID |
| milanta2025github | Invariant Labs: GitHub MCP exploited (2025) | | verified-now | PG (title, authors, date) | |
| lyons2025asanas | The Register: Asana MCP data leak (2025) | R | verified-now | PG (headline, byline, date) | News report; customer count unconfirmed |
| pogorelec2025genai | Help Net Security: GenAI exposing sensitive data (2025) (new) | R | verified-now | PG (title, author, date) | Secondary coverage of a vendor report |
| erikbern2026annbenchmarks | ann-benchmarks repository (new) | R | verified-now | GH | Cite the paper for the method |
| google2026atheris | Atheris repository | | verified-now | GH | |
| nist2026overview | TREC 2008 Enterprise overview page (new) | R | verified-now | PG | |
| neurips2026neurips | NeurIPS Paper Checklist Guidelines | R | verified-now | PG (heading) | Planning only |
| neurips2026call | NeurIPS 2026 Call for Evaluations & Datasets | R | verified-now | PG | Planning only |
| neurips2026main | NeurIPS 2026 Main Track Handbook (new) | R | verified-now | PG | Planning only |
| neurips2026evaluationsa | E&D Hosting 2026 (new) | R | verified-now | PG | Planning only |
| neurips2026evaluationsb | E&D FAQ 2026 (new) | R | verified-now | PG | Planning only |
| neurips2026evaluationsc | E&D 2026 Reviewing Guidelines (new) | R | verified-now | PG | Planning only |
| neurips2026choice | NeurIPS blog: contribution types (new) | R | partial | N (bot-check page) | **Title not verified**; planning only |
| icml2026icmla | ICML 2026 Call for Papers (new) | R | verified-now | PG | Planning only |
| icml2026icmlb | ICML 2026 Call for Position Papers (new) | R | verified-now | PG | Planning only |
| opencurious2026icml | OpenCurious: ICML 2027 deadline estimate (new) | R | verified-now | PG | Third-party estimate; planning only |
| vldb2026pvldb | PVLDB Vol. 20 submission guidelines (new) | R | partial | N (page timed out) | **Title is a descriptive label**; planning only |
| usenix2026usenix | USENIX Security '27 Call for Papers (new) | R | verified-now | PG | Planning only |
| ieee2026ieee | IEEE S&P 2027 Call for Papers (new) | R | verified-now | PG (title and heading) | Planning only |
| myhuiban2026sigir | myhuiban: SIGIR 2027 listing (new) | R | verified-now | PG | Third-party; planning only |
| iclr2026iclr | ICLR 2027 AI Policy for Authors (new) | R | verified-now | PG | Planning only |
| arxiv2026content | arXiv: Content Moderation (new) | R | verified-now | PG | Planning only |
| arxiv2026endorsement | arXiv: Endorsement (new) | R | verified-now | PG | Planning only |
| arxiv2026licenses | arXiv: Licenses (new) | R | verified-now | PG | Planning only |
| arxiv2025attentiona | arXiv blog: review and position papers in CS (2025-10-31) (new) | R | verified-now | PG | Planning only |
| arxiv2025attentionb | arXiv blog: endorsement policy update (2025-12-10) (new) | R | verified-now | PG | Planning only |
| arxiv2019arxiv | arXiv ML classification guide (2019) (new) | R | verified-now | PG | Planning only |
| arxiv2026fair | arXiv blog: updated rate-limit policy (2026-10-01) (new) | R | verified-now | PG | Planning only |
| singhchawla2026researchers | Nature: arXiv ban for hallucinated references (2026) (new) | R | verified-now | PG (title, author, date) | Press report, not an arXiv policy page; planning only |

## Core-precedent check (task item 3)

All 24 core items (27 entries, since the SQLancer item covers three papers and Big-ANN two) were re-checked online on 2026-10-26. Status: `verified-now`, except Wang et al. 2007, which is `partial` because no page range could be verified.

Stonebraker and Wong 1974 (CR); Büttcher and Clarke FAST 2005 (UX); Bailey, Hawking and Matson CIKM 2006 (CR, SR); Rizvi et al. SIGMOD 2004 (CR); Wang et al. VLDB 2007 (SR, partial); Kabra et al. SIGMOD 2006 (CR); Pang et al. Zanzibar ATC 2019 (UX); Cutler et al. Cedar OOPSLA 2024 (CR, AX); Malkov and Yashunin HNSW (CR, AX); Filtered-DiskANN (CR); ACORN (CR, AX); HoneyBee (CR, AX); Veda (AX); Yalamarthi and Pappachan (AX); Zeng et al. 2024 (ACL, CR, AX); Morris et al. vec2text (ACL, CR, AX); Rigger and Su PQS (UX), NoREC (CR, AX) and TLP (CR); Carlini et al. Secret Sharer (UX); Thakur et al. BEIR (NIPS, AX); MS MARCO (AX); Simhadri et al. Big-ANN 2023 (CR, NIPS, AX) and 2021 (PMLR, AX); OWASP LLM08:2025 (PG); RFC 8693 (RFC, CR); MCP specification 2026-07-28 (PG).

## Added 2026-10-26 (after the merge)

| Key | Short title | Status | Checked |
|---|---|---|---|
| lewis2020retrievalaugmented | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | verified-now | arXiv 2005.11401 abstract page: title, 12 authors in order, "Accepted at NeurIPS 2020"; pages not verified, left out |
| elastic2026controlling | Controlling access at the document and field level | verified-now | page title and the sentence "Document level security restricts the documents that users have read access to" |
| opensearch2026documentlevel | Document-level security | verified-now (title only) | page title; body text not read |
| xiao2024cpack | C-Pack: Packed Resources For General Chinese Embeddings | verified-now (2026-10-29) | arXiv 2309.07597 abstract page: title, 6 authors in order, comment "SIGIR 2024"; pages and DOI not verified, left out |
| yang2024qwen25 | Qwen2.5 Technical Report | verified-now (2026-10-29) | arXiv 2412.15115 abstract page: title, first six authors in order of 42, Qwen team, v1 19 Dec 2024 |
| qdrant2026search | Search (Qdrant documentation) | verified-now (2026-10-29) | page title; Query planning section and ACORN default 0.4 read |
| qdrant2026multitenancy | Multitenancy (Qdrant documentation) | verified-now (2026-10-29) | page title; is_tenant, payload_m, m 0 guidance read |
| couzon2026filtered | Filtered Vector Search: What ACORN Fixes, and What Fixes ACORN | verified-now (2026-10-29) | page title, two authors, 7 Aug 2026; quoted sentences read |
| reimers2019sentencebert | Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks | verified-now (2026-10-30) | ACL Anthology BibTeX D19-1410: title, two authors, EMNLP-IJCNLP 2019, pages 3982-3992, DOI |
| wang2020minilm | MiniLM: Deep Self-Attention Distillation for Task-Agnostic Compression of Pre-Trained Transformers | verified-now (2026-10-30) | NeurIPS proceedings page: title, six authors in order, NeurIPS 33 (2020); pages not shown, left out |
| ioannidis1997parametric | Parametric Query Optimization | verified-now (2026-10-30) | CR 10.1007/s007780050037: title, four authors in order, VLDB Journal 6(2) 132-151, 1997 |
| postgresql2026prepare | PREPARE (PostgreSQL 16 documentation) | verified-now (2026-10-30) | page title; Notes on custom and generic plans read |
| psycopg2026prepared | Prepared statements (Psycopg 3 documentation) | verified-now (2026-10-30) | page title; prepare_threshold behaviour read |
| elastic2026ignore | ignore_above (Elasticsearch Reference) | verified-now (2026-10-30) | page title; the 32766-byte Lucene term limit and the failure of indexed fields on longer values read |
| milvus2026json | JSON Field (Milvus Documentation) | verified-now (2026-10-30) | page title; FAQ sentence on the 65,536-byte limit read |
| postgresql2026selfuncs | selfuncs.c: gincostestimate (PostgreSQL source, REL_16_STABLE) | verified-now (2026-10-30) | source read: pending pages added to entry pages fetched and charged at random_page_cost in the startup cost |
| postgresql2026json | JSON Types (PostgreSQL 18 documentation, Section 8.14) | verified-now (2026-10-30) | page title, "current" = 18.6; numbers map to numeric, trailing zeroes insignificant for equality, E notation printed without it (1.230e-5 example) |
| elastic2026keyword | Keyword type family (Elasticsearch reference) | verified-now (2026-10-30) | page title; numeric identifiers as keyword suggested; checked that no sentence says a number is compared as a string |
| opensearch2026keyword | Keyword field type (OpenSearch Documentation) | verified-now (2026-10-30) | page title; both halves of the page read; numeric identifiers as keyword, range queries compare as strings, nothing on numeric terms |
| sjmurdoch2026bug | GitHub issue chroma-core/chroma#7594 | verified-now (2026-10-30) | GH API: title, author, opened 2026-08-16, state open, label bug, 2 comments; fix PR #7595 open, unmerged |
| redis2026tag | Tag fields (Redis documentation) | verified-now (2026-10-30) | page title; case-insensitive by default, CASESENSITIVE; no length limit stated |
| weaviate2026tokenizergo | tokenizer.go (weaviate/weaviate at v1.39.12) | verified-now (2026-10-30) | GH raw file at the tag and on main: tokenizeField trims whitespace (strings.TrimFunc, unicode.IsSpace) |
| weaviate2026inverted | Inverted indexes (Weaviate Documentation) | verified-now (2026-10-30) | page title; field tokenization described, no statement on trimming (also checked config-refs/collections) |
| qdrant2026filtering | Filtering (Qdrant documentation) | verified-now (2026-10-30) | page title; Nested key section: dot and [] path syntax; first 100,000 characters read |
| pinecone2026search | Search with a vector (Pinecone API reference, 2026-07) | verified-now (2026-10-30) | page title, API version; filter not among the required body fields |
| mongodb2026run | Run Vector Search ANN and ENN Queries (MongoDB Vector Search) | verified-now (2026-10-30) | page title; fields table (from the .md variant): filter Optional |
| elastic2026run | Run a search (Elasticsearch API documentation) | verified-now (2026-10-30) | page title; allow_partial_search_results default true, partial results on shard timeouts or failures |
| opensearch2026search | Search API (OpenSearch Documentation) | verified-now (2026-10-30) | page title; allow_partial_search_results default true |
| redis2026configuration | Configuration parameters (Redis Search) | verified-now (2026-10-30) | page title; search-on-timeout values RETURN (default), RETURN_STRICT, FAIL |
| vespa2026graceful | Graceful Query Coverage Degradation (Vespa documentation) | verified-now (2026-10-30) | page title; degraded results on timeout, coverage element and degraded flags |
| pinecone2026check | Check data freshness (Pinecone Docs) | verified-now (2026-10-30) | page title; "Pinecone is eventually consistent" sentence |
| mongodb2026configure | Configure mongot (Self-Managed MongoDB Search and Vector Search) | verified-now (2026-10-30) | page title; refresh interval default 1000 ms, delay between a write and being able to query it; mongot in Atlas confirmed on the Deployment Options page |
| datastax2026query | Query timestamps in Cassandra drivers (DataStax) | verified-now (2026-10-30) | page title; "don't mix LWTs and other mutation operations on a single table"; the Apache Cassandra DML page checked and silent |
| sungbin10152026fix | GitHub pull request milvus-io/pymilvus#3823 | verified-now (2026-10-30) | GH API: title, author, opened 2026-10-06, open, unmerged; body read; tracker search found no matching issue |
| authzed2026permissionserviceproto | permission_service.proto (authzed/api, main) | verified-now (2026-10-30) | GH raw file: optional_limit, after_result_cursor, LOOKUP_PERMISSIONSHIP_CONDITIONAL_PERMISSION comments |
| authzed2026coreproto | core.proto (authzed/api, main) | verified-now (2026-10-30) | GH raw file: ObjectReference.object_id pattern and 1,024-byte limit |
| openfga2026openfgaproto | openfga.proto (openfga/api, main) | verified-now (2026-10-30) | GH raw file: TupleKey user 512 bytes, object pattern 2 to 256 non-whitespace characters, 100 contextual tuples |
| authzed2026reference | Reference: spicedb (AuthZed documentation) | verified-now (2026-10-30) | page heading (the HTML title is generic); quantization interval default 5s, max staleness percent default 0.1 |
| pgvector2026pgvector, authzed2026consistency, opa2026evaluating, opa2026writing, postgresql2026prepare, psycopg2026prepared | (existing entries, re-read for the fault table) | re-read (2026-10-30) | pgvector README: max_scan_tuples 20,000, scan_mem_multiplier 1; consistency page: minimize_latency, configurable staleness window, no default stated; OPA pages: nothing on simplifying not over an empty collection; PREPARE notes and psycopg prepare_threshold re-read (the psycopg page does not state the default 5) |

## Build note (2026-10-26)

All `note` fields were renamed to `annote` so that plainnat does not print internal provenance remarks (several contained raw underscores and broke the build). Before submission, move genuine venue information (for example accepted-at statements once confirmed by the publisher) into proper fields.
