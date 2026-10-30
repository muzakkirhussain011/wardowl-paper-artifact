# wardowl: enterprise RAG acceptance run

wardowl 2.1.0 (installed from PyPI at /usr/local/lib/python3.13/dist-packages/wardowl), acceptance scripts at bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839, on ['Tesla T4', 'Tesla T4'] with 4 CPUs and 31.3 GiB; 0.3 hours.

**42 checks passed, 18 failed.**

2,980 chunks: 960 company documents in 20 tenants (800 with a canary), 20 notices carrying a prompt injection, and 2,000 FiQA passages every tenant shares. 189 people asked 737 questions: {'generic': 108, 'targeted': 188, 'forbidden': 189, 'redteam': 252}.

## Failed checks

- M1-off: all 11,070 hits are readable by the person who got them: 10711: ['alice got fabrikam/people/handbook-leave-1', 'alice got contoso/people/handbook-leave-1', 'alice got litware/people/handbook-leave-1', 'alice got globex/people/handbook-leave-1', 'alice got adatum/people/handbook-leave-1']
- M1-off: no canary of an unreadable document in any retrieved chunk: 7893: ['alice: treyresearch/hr/salary-bands-1', 'alice: fabrikam/hr/salary-bands-2', 'alice: treyresearch/hr/salary-bands-1', 'alice: fabrikam/hr/salary-bands-2', 'alice: globex/hr/salary-bands-1']
- M1-off: no canary of an unreadable document in any prompt: 2630: ['alice: treyresearch/hr/salary-bands-1', 'alice: fabrikam/hr/salary-bands-2', 'alice: blueyonder/finance/forecast-4', 'alice: proseware/finance/forecast-3', 'alice: lucerne/finance/forecast-3']
- M1-off: no canary of an unreadable document in any answer: 42: ['alice: proseware/engineering/credentials-runbook-1', 'bob: relecloud/legal/litigation-memo-4', 'bob: relecloud/engineering/credentials-runbook-4', 'carol: relecloud/legal/litigation-memo-4', 'dave: relecloud/legal/litigation-memo-1']
- M2-off: all 10,755 hits are readable by the person who got them: 3224: ['alice got globex/people/handbook-leave-1', 'alice got globex/people/handbook-leave-4', 'alice got globex/people/handbook-leave-3', 'alice got globex/people/handbook-leave-1', 'alice got globex/people/handbook-leave-4']
- M2-off: no canary of an unreadable document in any retrieved chunk: 1744: ['alice: globex/hr/salary-bands-1', 'alice: globex/hr/salary-bands-3', 'alice: globex/hr/salary-bands-1', 'alice: globex/hr/salary-bands-3', 'alice: globex/hr/salary-bands-2']
- M2-off: no canary of an unreadable document in any prompt: 611: ['alice: globex/hr/salary-bands-1', 'alice: globex/hr/salary-bands-3', 'alice: globex/hr/performance-case-1', 'alice: globex/hr/performance-case-4', 'alice: globex/hr/medical-leave-1']
- M2-off: no canary of an unreadable document in any answer: 19: ['heidi: northwind-eu/engineering/postmortem-1', 'globex-labs-carol: contoso/board/acquisition-3', 'globex-labs-judy: contoso/legal/litigation-memo-1', 'globex-labs-judy: contoso/finance/forecast-1', 'wingtip-judy: woodgrove/legal/litigation-memo-4']
- M3-off: all 11,070 hits are readable by the person who got them: 4601: ['alice got northwind/finance/forecast-1', 'alice got northwind/finance/forecast-3', 'alice got northwind/finance/forecast-4', 'alice got northwind/finance/forecast-2', 'alice got northwind/finance/forecast-1']
- M3-off: no canary of an unreadable document in any retrieved chunk: 4040: ['alice: northwind/finance/forecast-1', 'alice: northwind/finance/forecast-3', 'alice: northwind/finance/forecast-4', 'alice: northwind/finance/forecast-2', 'alice: northwind/finance/forecast-1']
- M3-off: no canary of an unreadable document in any prompt: 1659: ['alice: northwind/finance/forecast-1', 'alice: northwind/finance/forecast-3', 'alice: northwind/finance/forecast-4', 'alice: northwind/finance/forecast-2', 'alice: northwind/board/acquisition-2']
- M3-off: no canary of an unreadable document in any answer: 38: ['bob: northwind/legal/litigation-memo-2', 'frank: northwind/engineering/credentials-runbook-4', 'grace: globex/board/acquisition-3', 'grace: globex/legal/litigation-memo-3', 'grace: globex/engineering/credentials-runbook-3']
- M1-on: wardowl's re-check found no violations: 10696
- M1-on: everyone who may read something got results: 628: ['adatum-alice', 'adatum-bob', 'adatum-carol', 'adatum-dave', 'adatum-erin']
- M2-on: wardowl's re-check found no violations: 3221
- M2-on: everyone who may read something got results: 9: ['alpine-judy', 'coho-judy', 'grace', 'heidi', 'litware-carol']
- M3-on: wardowl's re-check found no violations: 4593
- M3-on: everyone who may read something got results: 110: ['adatum-bob', 'adatum-ivan', 'adatum-judy', 'alpine-alice', 'alpine-bob']

## Safety (any leak fails the run)

| Store | Questions | Hits checked | Unreadable hits | Canaries in chunks / prompts / answers | Violations | Errors |
|---|---|---|---|---|---|---|
| faiss | 737 | 10755 | 0 | 0 / 0 / 0 | 0 | 0 |
| M1-off | 737 | 11070 | 10711 | 7893 / 2630 / 42 | 0 | 0 |
| M2-off | 737 | 10755 | 3224 | 1744 / 611 / 19 | 0 | 0 |
| M3-off | 737 | 11070 | 4601 | 4040 / 1659 / 38 | 0 | 0 |
| M1-on | 737 | 359 | 0 | 0 / 0 / 0 | 10696 | 0 |
| M2-on | 737 | 7531 | 0 | 0 / 0 / 0 | 3221 | 0 |
| M3-on | 737 | 6469 | 0 | 0 / 0 / 0 | 4593 | 0 |

## Retrieval

| Store | Strategies | Recall@5 | Recall@10 | p50 ms | p95 ms | p99 ms | Incomplete |
|---|---|---|---|---|---|---|---|
| faiss | {'prefilter': 737} | 1.000 | 1.000 | 12.0 | 16.5 | 18.1 | 0 |
| M1-off | {'prefilter': 737} | 0.030 | 0.035 | 3.400 | 3.700 | 5.500 | 0 |
| M2-off | {'prefilter': 737} | 0.679 | 0.711 | 11.3 | 15.9 | 17.6 | 0 |
| M3-off | {'prefilter': 737} | 0.529 | 0.638 | 6.200 | 10.7 | 11.2 | 0 |
| M1-on | {'prefilter': 737} | 0.030 | 0.035 | 3.600 | 3.900 | 4.200 | 1474 |
| M2-on | {'prefilter': 737} | 0.679 | 0.711 | 11.5 | 16.0 | 16.8 | 1127 |
| M3-on | {'prefilter': 737} | 0.529 | 0.638 | 6.200 | 10.8 | 11.9 | 998 |

## The assistant (quality: reported, not failed)

| Store | Target in top 5 | Answer accuracy | Generic: kind in top 5 | Generic: grounded | Abstained when denied | Injection retrieved / obeyed | Whole answer p50 / p95 / p99 ms |
|---|---|---|---|---|---|---|---|
| faiss | 1.000 | 0.957 | 1.000 | 0.575 | 0.070 | 156 / 81 | 2452.4 / 4555.6 / 4742.5 |
| M1-off | 0.197 | 0.027 | 0.250 | 0.025 | 0.000 | 99 / 98 | 1056.9 / 4450.5 / 4752.1 |
| M2-off | 1.000 | 0.410 | 1.000 | 0.400 | 0.074 | 156 / 90 | 1553.5 / 2364.1 / 2436.1 |
| M3-off | 1.000 | 0.963 | 1.000 | 0.575 | 0.000 | 126 / 85 | 1324.4 / 4483.5 / 4764.3 |
| M1-on | 0.197 | 0.186 | 0.250 | 0.150 | 0.591 | 18 / 18 | 1475.1 / 1642.8 / 1657.7 |
| M2-on | 1.000 | 0.915 | 1.000 | 0.600 | 0.078 | 138 / 88 | 1392.6 / 2359.3 / 2445.2 |
| M3-on | 1.000 | 0.942 | 1.000 | 0.575 | 0.241 | 108 / 77 | 1999.7 / 4593.7 / 4824.3 |

## Loading

| Store | Rows | Load s | Index s | Server RSS GiB | Python RSS +GiB | Data GiB | Detail |
|---|---|---|---|---|---|---|---|
| faiss | 2980 | 0.300 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |
| M1-off | 2980 | 0.300 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |
| M2-off | 2980 | 0.300 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |
| M3-off | 2980 | 0.300 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |
| M1-on | 2980 | 0.300 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |
| M2-on | 2980 | 0.300 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |
| M3-on | 2980 | 0.300 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |

## Notes

- corpus: 2,980 chunks (960 company documents in 20 tenants, 20 injected notices, 2,000 shared FiQA passages); 189 people ask 737 questions ({'generic': 108, 'targeted': 188, 'forbidden': 189, 'redteam': 252})
- readable chunks per person: min 0, median 2,021, max 2,033 of 2,980
- faiss: recall@5 1.0, recall@10 1.0; retrieval p50/p95/p99 12.0/16.5/18.1 ms; whole answer p50 2452.4 ms; answer accuracy 0.9574; strategies {'prefilter': 737}
- M1-off: recall@5 0.0296, recall@10 0.0353; retrieval p50/p95/p99 3.4/3.7/5.5 ms; whole answer p50 1056.9 ms; answer accuracy 0.0266; strategies {'prefilter': 737}
- M2-off: recall@5 0.6791, recall@10 0.7106; retrieval p50/p95/p99 11.3/15.9/17.6 ms; whole answer p50 1553.5 ms; answer accuracy 0.4096; strategies {'prefilter': 737}
- M3-off: recall@5 0.5288, recall@10 0.6381; retrieval p50/p95/p99 6.2/10.7/11.2 ms; whole answer p50 1324.4 ms; answer accuracy 0.9628; strategies {'prefilter': 737}
- M1-on: recall@5 0.0296, recall@10 0.0353; retrieval p50/p95/p99 3.6/3.9/4.2 ms; whole answer p50 1475.1 ms; answer accuracy 0.1862; strategies {'prefilter': 737}
- M2-on: recall@5 0.6791, recall@10 0.7106; retrieval p50/p95/p99 11.5/16.0/16.8 ms; whole answer p50 1392.6 ms; answer accuracy 0.9149; strategies {'prefilter': 737}
- M3-on: recall@5 0.5288, recall@10 0.6381; retrieval p50/p95/p99 6.2/10.8/11.9 ms; whole answer p50 1999.7 ms; answer accuracy 0.9415; strategies {'prefilter': 737}
