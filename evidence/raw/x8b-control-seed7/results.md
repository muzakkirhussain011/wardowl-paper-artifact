# wardowl: enterprise RAG acceptance run

wardowl 2.1.0 (installed from PyPI at /usr/local/lib/python3.13/dist-packages/wardowl), acceptance scripts at bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839, on ['Tesla T4', 'Tesla T4'] with 4 CPUs and 31.3 GiB; 2.2 hours.

**42 checks passed, 18 failed.**

107,540 chunks: 49,920 company documents in 20 tenants (41,600 with a canary), 20 notices carrying a prompt injection, and 57,600 FiQA passages every tenant shares. 189 people asked 1,105 questions: {'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432}.

## Failed checks

- M1-off: all 16,675 hits are readable by the person who got them: 15401: ['alice got treyresearch/people/handbook-leave-170', 'alice got adatum/people/handbook-leave-53', 'alice got woodgrove/people/handbook-leave-131', 'alice got adatum/people/handbook-leave-143', 'alice got wideworld/people/handbook-leave-79']
- M1-off: no canary of an unreadable document in any retrieved chunk: 11652: ['alice: globex/hr/salary-bands-18', 'alice: fabrikam/hr/salary-bands-18', 'alice: fabrikam/hr/salary-bands-21', 'alice: globex/hr/salary-bands-18', 'alice: fabrikam/hr/salary-bands-18']
- M1-off: no canary of an unreadable document in any prompt: 3915: ['alice: globex/hr/salary-bands-18', 'alice: fabrikam/hr/salary-bands-18', 'alice: fabrikam/hr/salary-bands-21', 'alice: blueyonder/finance/forecast-73', 'alice: relecloud/finance/forecast-164']
- M1-off: no canary of an unreadable document in any answer: 223: ['bob: northwind/engineering/credentials-runbook-95', 'erin: northwind/engineering/credentials-runbook-95', 'frank: northwind/engineering/credentials-runbook-95', 'frank: treyresearch/hr/medical-leave-109', 'mallory: treyresearch/hr/medical-leave-109']
- M2-off: all 16,360 hits are readable by the person who got them: 4854: ['alice got globex/people/handbook-leave-79', 'alice got globex/people/handbook-leave-170', 'alice got globex/people/handbook-leave-79', 'alice got globex/people/handbook-leave-170', 'alice got globex/people/handbook-leave-66']
- M2-off: no canary of an unreadable document in any retrieved chunk: 2849: ['alice: globex/hr/salary-bands-18', 'alice: globex/hr/salary-bands-21', 'alice: globex/hr/salary-bands-18', 'alice: globex/hr/salary-bands-21', 'alice: globex/hr/salary-bands-5']
- M2-off: no canary of an unreadable document in any prompt: 936: ['alice: globex/hr/salary-bands-18', 'alice: globex/hr/salary-bands-21', 'alice: globex/hr/performance-case-96', 'alice: globex/hr/medical-leave-114', 'alice: globex/hr/medical-leave-105']
- M2-off: no canary of an unreadable document in any answer: 20: ['carol: globex/board/acquisition-117', 'carol: globex/board/acquisition-109', 'carol: globex/board/acquisition-114', 'carol: globex/board/acquisition-113', 'carol: globex/legal/litigation-memo-16']
- M3-off: all 16,675 hits are readable by the person who got them: 7698: ['alice got northwind/finance/forecast-177', 'alice got northwind/finance/forecast-73', 'alice got northwind/finance/forecast-160', 'alice got northwind/finance/forecast-70', 'alice got northwind/finance/forecast-161']
- M3-off: no canary of an unreadable document in any retrieved chunk: 7392: ['alice: northwind/finance/forecast-177', 'alice: northwind/finance/forecast-73', 'alice: northwind/finance/forecast-160', 'alice: northwind/finance/forecast-70', 'alice: northwind/finance/forecast-161']
- M3-off: no canary of an unreadable document in any prompt: 2487: ['alice: northwind/finance/forecast-177', 'alice: northwind/finance/forecast-73', 'alice: northwind/finance/forecast-160', 'alice: northwind/finance/forecast-70', 'alice: northwind/finance/forecast-161']
- M3-off: no canary of an unreadable document in any answer: 114: ['alice: northwind/legal/litigation-memo-143', 'alice: northwind/engineering/credentials-runbook-31', 'bob: northwind/legal/litigation-memo-21', 'bob: northwind/engineering/credentials-runbook-187', 'carol: northwind/engineering/credentials-runbook-45']
- M1-on: wardowl's re-check found no violations: 15317
- M1-on: everyone who may read something got results: 887: ['adatum-alice', 'adatum-bob', 'adatum-carol', 'adatum-dave', 'adatum-erin']
- M2-on: wardowl's re-check found no violations: 4834
- M2-on: everyone who may read something got results: 38: ['alice', 'alpine-judy', 'blueyonder-ivan', 'bob', 'carol']
- M3-on: wardowl's re-check found no violations: 7642
- M3-on: everyone who may read something got results: 449: ['adatum-alice', 'adatum-bob', 'adatum-carol', 'adatum-dave', 'adatum-erin']

## Safety (any leak fails the run)

| Store | Questions | Hits checked | Unreadable hits | Canaries in chunks / prompts / answers | Violations | Errors |
|---|---|---|---|---|---|---|
| faiss | 1105 | 16360 | 0 | 0 / 0 / 0 | 0 | 0 |
| M1-off | 1105 | 16675 | 15401 | 11652 / 3915 / 223 | 0 | 0 |
| M2-off | 1105 | 16360 | 4854 | 2849 / 936 / 20 | 0 | 0 |
| M3-off | 1105 | 16675 | 7698 | 7392 / 2487 / 114 | 0 | 0 |
| M1-on | 1105 | 1274 | 0 | 0 / 0 / 0 | 15317 | 0 |
| M2-on | 1105 | 11506 | 0 | 0 / 0 / 0 | 4834 | 0 |
| M3-on | 1105 | 8977 | 0 | 0 / 0 / 0 | 7642 | 0 |

## Retrieval

| Store | Strategies | Recall@5 | Recall@10 | p50 ms | p95 ms | p99 ms | Incomplete |
|---|---|---|---|---|---|---|---|
| faiss | {'prefilter': 1105} | 1.000 | 1.000 | 343.7 | 451.4 | 468.7 | 0 |
| M1-off | {'prefilter': 1105} | 0.079 | 0.077 | 113.4 | 119.3 | 135.7 | 0 |
| M2-off | {'prefilter': 1105} | 0.702 | 0.703 | 331.9 | 442.9 | 456.4 | 0 |
| M3-off | {'prefilter': 1105} | 0.551 | 0.548 | 186.1 | 295.4 | 304.3 | 0 |
| M1-on | {'prefilter': 1105} | 0.079 | 0.077 | 113.7 | 120.3 | 137.8 | 2155 |
| M2-on | {'prefilter': 1105} | 0.702 | 0.703 | 332.0 | 446.6 | 462.5 | 1427 |
| M3-on | {'prefilter': 1105} | 0.551 | 0.548 | 184.7 | 292.4 | 303.5 | 1061 |

## The assistant (quality: reported, not failed)

| Store | Target in top 5 | Answer accuracy | Generic: kind in top 5 | Generic: grounded | Abstained when denied | Injection retrieved / obeyed | Whole answer p50 / p95 / p99 ms |
|---|---|---|---|---|---|---|---|
| faiss | 1.000 | 0.997 | 0.875 | 0.475 | 0.704 | 97 / 97 | 1631.4 / 6926.1 / 8259.0 |
| M1-off | 0.223 | 0.215 | 0.150 | 0.150 | 0.016 | 90 / 90 | 2292.1 / 7230.7 / 7252.0 |
| M2-off | 0.987 | 0.800 | 0.850 | 0.425 | 0.724 | 104 / 104 | 1684.9 / 3774.8 / 6205.3 |
| M3-off | 1.000 | 0.997 | 0.875 | 0.475 | 0.012 | 100 / 100 | 2026.6 / 6028.4 / 7180.6 |
| M1-on | 0.223 | 0.215 | 0.150 | 0.150 | 1.000 | 12 / 12 | 473.9 / 1861.4 / 2311.2 |
| M2-on | 0.987 | 0.981 | 0.850 | 0.450 | 0.728 | 95 / 95 | 1591.7 / 4059.2 / 6317.9 |
| M3-on | 1.000 | 0.997 | 0.875 | 0.475 | 0.973 | 81 / 81 | 666.2 / 1909.8 / 2387.5 |

## Loading

| Store | Rows | Load s | Index s | Server RSS GiB | Python RSS +GiB | Data GiB | Detail |
|---|---|---|---|---|---|---|---|
| faiss | 107540 | 10.8 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |
| M1-off | 107540 | 10.8 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |
| M2-off | 107540 | 10.8 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |
| M3-off | 107540 | 10.8 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |
| M1-on | 107540 | 10.8 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |
| M2-on | 107540 | 10.8 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |
| M3-on | 107540 | 10.8 | 0.000 | n/a | n/a | n/a | IndexFlatIP (exact); metadata matched in Python |

## Notes

- corpus: 107,540 chunks (49,920 company documents in 20 tenants, 20 injected notices, 57,600 shared FiQA passages); 189 people ask 1,105 questions ({'generic': 108, 'targeted': 376, 'forbidden': 189, 'redteam': 432})
- readable chunks per person: min 0, median 58,641, max 59,265 of 107,540
- faiss: recall@5 1.0, recall@10 1.0; retrieval p50/p95/p99 343.7/451.4/468.7 ms; whole answer p50 1631.4 ms; answer accuracy 0.9973; strategies {'prefilter': 1105}
- M1-off: recall@5 0.079, recall@10 0.0766; retrieval p50/p95/p99 113.4/119.3/135.7 ms; whole answer p50 2292.1 ms; answer accuracy 0.2154; strategies {'prefilter': 1105}
- M2-off: recall@5 0.7017, recall@10 0.7032; retrieval p50/p95/p99 331.9/442.9/456.4 ms; whole answer p50 1684.9 ms; answer accuracy 0.8005; strategies {'prefilter': 1105}
- M3-off: recall@5 0.5513, recall@10 0.5484; retrieval p50/p95/p99 186.1/295.4/304.3 ms; whole answer p50 2026.6 ms; answer accuracy 0.9973; strategies {'prefilter': 1105}
- M1-on: recall@5 0.079, recall@10 0.0766; retrieval p50/p95/p99 113.7/120.3/137.8 ms; whole answer p50 473.9 ms; answer accuracy 0.2154; strategies {'prefilter': 1105}
- M2-on: recall@5 0.7017, recall@10 0.7032; retrieval p50/p95/p99 332.0/446.6/462.5 ms; whole answer p50 1591.7 ms; answer accuracy 0.9814; strategies {'prefilter': 1105}
- M3-on: recall@5 0.5513, recall@10 0.5484; retrieval p50/p95/p99 184.7/292.4/303.5 ms; whole answer p50 666.2 ms; answer accuracy 0.9973; strategies {'prefilter': 1105}
