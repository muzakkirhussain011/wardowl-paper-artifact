# X8 amendment 2: exposure and the mutation positive control

Pre-registration: `plan/x8-prereg.md`, amendment 2 (eff0b23, 2026-10-30 10:11, after X0, X8, X8-FGA
and the critical review, before any of these runs). Exploratory in the review's sense: specified in
writing after the main results and before running. Nothing here replaces a result of X0, X8 or X8-FGA.

Runner: `kaggle/x8/x8b_run.py`, wardowl 2.1.0 from PyPI, FAISS only (`IndexFlatIP`, exact, in process),
bge-base-en-v1.5, Qwen2.5-3B-Instruct, k = 5 and 10, Kaggle GPU T4 x2 on muzakkirhussain1.

Raw outputs: `evidence/raw/x8b-seed7/`, `-seed11/`, `-seed13/`, `-seed17/`, `x8b-pool/`, `x8b-smoke/`,
`x8b-control-seed7/`. The control kernel took 7,945 s.

## Verdicts

The labels below are that amendment's prediction numbers. They clash with the experiment codes (X1 to
X8) and mean nothing outside this file; the paper's ledger says so.

| Prediction | Verdict | Numbers |
|---|---|---|
| X1. P0 reproduces X0's FAISS row | holds | 16,360 hits, 0 unreadable, canaries 0 / 0 / 0, 0 violations, 0 errors, recall@5 and recall@10 1.000 |
| X2. Off passes: unreadable hits, canaries in chunks and prompts all > 0, violations 0 | holds | see the first table below; all four leak checks failed in every off pass |
| X3. Canaries in answers > 0 in M1-off and M3-off | holds | 223 and 114 canaries (138 and 107 questions). M2-off, without a prediction: 20 canaries, 13 questions |
| X4. On passes: violations > 0, and no unreadable hit or canary | holds | 15,317, 4,834, 7,642 violations, and 0 everywhere else |
| X5. M1-off equals unfiltered exact retrieval for at least 99% of questions | holds | 1,105 of 1,105 same ids at k = 10, same unreadable counts at k = 5 and k = 10 |
| X6. In every seed, forbidden questions: at least 90% unreadable in top 5, at least 75% canary | holds | 100.0% and 97.9% in each of the four seeds |
| X7. In every seed, targeted and red-team questions at least 90% unreadable in top 5 | partly falsified | targeted 100.0% in every seed: holds. Red team 87.7% in every seed: falsified |

Why X7 failed for red team: one of the eight attacks, `reference-codes`, has 1.8% of its questions
exposed in the top 5 (96.3% in the top 10), because its nearest chunks are almost all readable. The
other seven attacks are at 100.0%. The prediction reasoned from the counterpart documents and did not
consider a query whose neighbours are the shared passages.

## Exposure, pooled over seeds 7, 11, 13 and 17

| Category | Questions | Unreadable in top 5 | Mean | Canary in top 5 | Unreadable in top 10 | Mean | Canary in top 10 |
|---|---|---|---|---|---|---|---|
| generic | 432 | 100.0% | 4.77 | 83.3% | 100.0% | 9.57 | 83.3% |
| targeted | 1,504 | 100.0% | 4.78 | 54.8% | 100.0% | 9.54 | 54.8% |
| forbidden | 756 | 100.0% | 5.00 | 97.9% | 100.0% | 10.00 | 97.9% |
| red team | 1,728 | 87.7% | 4.26 | 75.0% | 99.5% | 8.62 | 75.0% |
| all | 4,420 | 95.2% | 4.61 | 72.9% | 99.8% | 9.26 | 72.9% |

The shares are the same to one decimal in every seed; the seed changes the document text and the
sample but not the templates or personas. Each company document has a counterpart from the same
template and pool entry in each of the other 19 tenants. "Exposure inside the tenant" below gives the
shares without them, for seed 7.
The per-person-type and per-attack tables are in `evidence/raw/x8b-pool/x8b-exposure-pooled.md`.

## Mutation control, seed 7

What each mutated pre-filter admits that the person may not read (chunks, over 189 people):

| Filter | People over-admitted | Min / median / max | Readable chunks left out (max) |
|---|---|---|---|
| P0, unmutated | 0 | 0 / 0 / 0 | 0 |
| M1, admits everything | 189 | 48,275 / 48,899 / 107,540 | 0 |
| M2, also the next tenant | 188 | 0 / 1,041 / 1,665 | 0 |
| M3, ACL clause dropped | 189 | 832 / 1,456 / 60,097 | 0 |

Per question, over the 1,105 main retrievals (k = 5 and k = 10):

| Pass | Re-check | Unreadable hit, k=5 | k=10 | Canary in chunk | Prompt | Answer | Violations (questions) | Violations (hits) | Incomplete | Recall@10 |
|---|---|---|---|---|---|---|---|---|---|---|
| P0 | on | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.000 |
| M1 | off | 1,052 | 1,103 | 805 | 805 | 138 | 0 | 0 | 0 | 0.077 |
| M2 | off | 676 | 751 | 400 | 360 | 13 | 0 | 0 | 0 | 0.703 |
| M3 | off | 528 | 533 | 509 | 503 | 107 | 0 | 0 | 0 | 0.548 |
| M1 | on | 0 | 0 | 0 | 0 | 0 | 1,103 | 15,317 | 1,103 | 0.077 |
| M2 | on | 0 | 0 | 0 | 0 | 0 | 751 | 4,834 | 751 | 0.703 |
| M3 | on | 0 | 0 | 0 | 0 | 0 | 533 | 7,642 | 533 | 0.548 |

Checked question by question on `x8b-control-seed7-questions.json` (not only as totals), first with an awk
script on a local copy of that file, then by the recount kernel described under "Audit and recount":

- For each mutation, the questions with an unreadable hit in the off pass are exactly the questions
  with a violation in the on pass, and exactly the questions marked incomplete in the on pass.
- For each question, the violations in the on pass equal the unreadable hits in the off pass (the
  k = 5 and k = 10 counts added). Totals: 15,317, 4,834, 7,642.
- No question has an unreadable hit at k = 5 without one at k = 10.
- Every canary in an answer is also in that question's prompt, as the design expects: a model cannot
  produce a 40-bit code it was not shown.

The harness's own hit counts are slightly higher in the off passes (15,401, 4,854, 7,698), because
they include the 20 end-to-end questions, whose hits do not enter its violation counter. The paper
uses the per-question figures of the main retrievals.

The harness's checks: P0 failed none. Each off pass failed exactly its four leak checks (hits readable,
no canary in chunk, in prompt, in answer). Each on pass failed exactly two: "the re-check found no
violations" and "everyone who may read something got results" (887, 38 and 449 retrievals came back
empty for people who may read something). 18 failed checks in all, as designed.

Reported without a prediction, not used in the paper: answer accuracy 0.9973 (P0), 0.2154 (M1 off and
on), 0.8005 and 0.9814 (M2 off and on), 0.9973 (M3 off and on).

## What this shows and what it does not

- The checks behind the bounds in the end-to-end section can fail: they fail when enforcement is broken.
- Questions came near unreadable content, so a broken filter had something to return.
- With a wrong pre-filter, the re-check alone contained the fault and reported it. It did not repair it:
  recall stayed where the broken filter left it.
- A test that reads only answers has much less power: of the questions with a canary in the prompt, the
  answer carried one in 138 of 805, 13 of 360 and 107 of 503.
- It is one seed and one configuration, on an exact store. It breaks only the filter: the check stays
  the unmutated policy's, so a wrong check is outside this control and stays in the trusted computing base.

## Audit and recount (added by the session that ran the kernels)

The sections above were written by another session from these outputs. This section was added after
checking them against the raw files.

**What was checked, and the result.** Every number in the tables and verdicts above, against
`x8b-control-seed7.md`, `x8b-control-seed7.json`, `results.json` and `x8b-exposure-pooled.md`: no
disagreement. The raw control outputs are byte-identical to a fresh download from Kaggle.

**Recount of the per-question claims.** CPU kernel `muzakkirhussain1/wardowl-x8b-verify`
(`kaggle/x8/x8b-verify/`, output in `evidence/raw/x8b-verify/`), run after the results and not part of
the amendment, reads `x8b-control-seed7-questions.json`. All four claims in the list above hold, with
no exception:

| Mutation | Exposed off / violation on / incomplete on (questions) | Set differences | Questions where violations differ from unreadable hits | Unreadable off / violations on (hits) | k=5 without k=10 | Answer canary not in prompt | Prompt canary not in chunk |
|---|---|---|---|---|---|---|---|
| M1 | 1,103 / 1,103 / 1,103 | 0 | 0 | 15,317 / 15,317 | 0 | 0 of 138 | 0 of 805 |
| M2 | 751 / 751 / 751 | 0 | 0 | 4,834 / 4,834 | 0 | 0 of 13 | 0 of 360 |
| M3 | 533 / 533 / 533 | 0 | 0 | 7,642 / 7,642 | 0 | 0 of 107 | 0 of 503 |

**Order of events.** Amendment eff0b23 (10:11 UTC). Runner and kernels 16cfb09 (10:17 UTC), unchanged
since, and the amendment unchanged since it was committed. Kernel start times from `kernels list`, all
at version 1, none rerun and none failed: smoke 10:17, seed 11 10:18, seed 13 10:27, seed 17 10:36,
control 10:39, seed 7 10:44, pool 10:53. `x8b-smoke` is not in the amendment. It ran this runner with
the harness's small configuration (4 variants per template, 2,000 FiQA passages, Qwen2.5-0.5B-Instruct,
737 questions, 1,181 s on GPU T4 x2) to catch faults in the runner before the control. Its numbers are
not results and are in no table here. Seed 11's output was read before the other kernels started, and
the smoke's before the control and seed 7 started; no code or prediction changed after either.

**X1 reproduced more than it predicted.** P0 also matches X0's quality columns for FAISS: target in the
top five 1.000, answer accuracy 0.997, generic kind 0.875, grounded 0.475, abstained when denied 0.704,
injected notices retrieved and obeyed 97 / 97. That is the same seed on another account and session.

**The `reference-codes` attack is one person.** Its prompt has no placeholder, so all 54 askers in a
seed share one query vector and one top 10 (1 distinct list of 54, in every seed), which starts with
FiQA passages. The 1.8% in the top 5 is one person of 54 in every seed: mallory, who may read nothing.
For everyone else who asked it, the five nearest chunks are readable. Red team's 87.7% is therefore
7 of 8 attacks plus mallory: (7 x 54 + 1) / 432 = 379 / 432. X7 stays falsified as registered.

**Exposure inside the tenant.**
M3-off is exact search over the asker's tenant and the shared passages, so other tenants' copies
cannot appear. The recount confirms it: of its 5,105 distinct unreadable (question, chunk) pairs, 4,979
are in the asker's own tenant, 126 are shared passages and 0 are in another tenant. Its per-category
counts were pre-registered output; reading them as exposure without the copies was noticed after the
run. One seed:

| Category | Questions | Whole corpus, top 5 (seed 7) | Inside the tenant, top 5 | Inside the tenant, top 10 |
|---|---|---|---|---|
| generic | 108 | 100.0% | 67 (62.0%) | 68 (63.0%) |
| targeted | 376 | 100.0% | 2 (0.5%) | 3 (0.8%) |
| forbidden | 189 | 100.0% | 189 (100.0%) | 189 (100.0%) |
| red team | 432 | 87.7% | 270 (62.5%) | 273 (63.2%) |
| all | 1,105 | 95.2% | 528 (47.8%) | 533 (48.2%) |

So targeted questions test the tenant boundary and hardly the ACL inside it. The ACL inside the tenant
is tested by the forbidden questions by construction, and by about 62% of the generic and red-team ones.

**Why person types differ.** Besides their permissions, the question generator picks a generated
person's targeted templates by `allowed[(i + j) % len(allowed)]`, where i is the person's position, so
a role with five allowed templates asks about the same two in every tenant. dave's generated personas
get handbook-it and handbook-leave, which are public, hence 2.6% canary on targeted questions (the one
northwind dave gets handbook-leave and postmortem); frank may read only public templates, hence 0.0%.
The per-type tables should not be read as a property of the role alone.

**Answers and the canary check (not checked question by question).** M2's answer accuracy on the 376
targeted questions is 0.8005 with the re-check off and 0.9814 with it on, about 68 more wrong answers,
while only 1 targeted answer held a canary. That is consistent with the model quoting the neighbouring
tenant's number, which a canary check on answers cannot see. The oracle's check of the retrieved chunks
and the canary check of the prompts are what catch it.

## Text for e2e.tex

`paper/sections/e2e.tex` already reports exposure and the control (ea904dc, eefa3df), and its numbers
agree with the outputs. This draft was applied on 2026-10-30, with the whole-corpus share of seed 7 added. It replaced only the passage from "Each company
document has a counterpart" to "was at 1.8\%." (lines 41 to 43 at eefa3df). The same correction applies
to `paper/sections/app-e2e.tex`, lines 163 to 168.

```latex
Each company document has a counterpart from the same template in each of the other 19 tenants, and these
shares depend on those copies. With the copies out of reach, as in the control's ACL mutation with the
re-check off, which searches only the person's tenant and the shared passages, 47.8\% of the 1,105 questions
of seed 7 had an unreadable chunk in the top 5: all 189 forbidden questions, 62.5\% of the red-team prompts,
62.0\% of the generic questions and 0.5\% of the targeted ones (a reading of that pass we made after the run).
Targeted questions therefore test the tenant boundary and hardly the ACL inside it. Over the whole corpus,
generic, targeted and forbidden questions were all exposed in the top 5, and red-team prompts at 87.7\%, which
falsifies our prediction of at least 90\% for them: the nearest chunks of one of the eight attacks, a request
for reference codes, are shared passages, and in the top 5 it reached only the one person who may read nothing.
```
