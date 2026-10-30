# X8b (plan/x8-prereg.md, amendment 2). Measurement 1, exposure: for every question, how much of the
# unfiltered exact top 5 and top 10 the asking person may not read. Measurement 2, when CONTROL is set:
# a mutation positive control, the harness's own evaluation on FAISS with enforcement broken on purpose.
# The pinned harness (acceptance/kaggle/enterprise_rag.py at bf25bd0) is imported and not changed;
# everything added is in this file. Kaggle settings: GPU T4 x2, internet on.
import json
import statistics
import subprocess
import sys
import time
import traceback
from collections import defaultdict
from functools import partial
from pathlib import Path

SEED = 7
CONTROL = False  # also run the seven passes of the positive control
SMOKE = False  # a check of this runner on the harness's small configuration: its numbers are not results
WARDOWL_VERSION = "2.1.0"
REF = "bf25bd0f4c3f7b757ab02b7cda830d0e05c1f839"  # the scripts X0 and X8 ran
SRC = "/tmp/wardowl-src"
EXTRAS = "pgvector,chroma,elasticsearch,opensearch,qdrant,weaviate,redis,lancedb,faiss"  # as X8 installed them
WORK = Path("/kaggle/working")
CATEGORIES = ("generic", "targeted", "forbidden", "redteam")


def sh(command: str) -> None:
    print(f"+ {command}", flush=True)
    subprocess.run(command, shell=True, check=True)


def save(name: str, data: dict, text: str) -> None:
    (WORK / f"{name}.json").write_text(json.dumps(data, indent=1, default=str) + "\n", encoding="utf-8")
    (WORK / f"{name}.md").write_text(text, encoding="utf-8")
    print(f"wrote {name}.json and {name}.md", flush=True)


started = time.time()
sh(f"rm -rf {SRC} && git clone -q https://github.com/muzakkirhussain011/wardowl.git {SRC}")
sh(f"git -C {SRC} checkout -q {REF} && git -C {SRC} log -1 --format='%H %cs %s'")
sh(f'pip install -q "wardowl[{EXTRAS}]=={WARDOWL_VERSION}" "sentence-transformers>=3" "datasets>=2.19" psutil')
# No PostgreSQL and no store server: FAISS runs in this process.

sys.path.insert(0, f"{SRC}/acceptance/kaggle")
import enterprise_rag as er  # noqa: E402
import numpy as np  # noqa: E402
import torch  # noqa: E402
from wardowl import MetadataACLAuthorizer, TenantAuthorizer  # noqa: E402
from wardowl.filters import And, In, matches  # noqa: E402

if SMOKE:
    config = er.Config.smoke()
    config.stores, config.remote_authorizers, config.seed = ("faiss",), (), SEED
else:
    config = er.Config(
        stores=("faiss",),
        remote_authorizers=(),
        variants=208,
        kb_limit=0,
        embed_model="BAAI/bge-base-en-v1.5",
        llm_model="Qwen/Qwen2.5-3B-Instruct",
        seed=SEED,
    )
config.wardowl_version, config.repo = WARDOWL_VERSION, SRC
print(f"X8b seed {SEED}, control {CONTROL}, smoke {SMOKE}", flush=True)
run = er.Run(config)

# ---- person types and tables -------------------------------------------------------------------

NAMED = {p.id for p in er.PERSONAS}


def person_type(persona) -> str:
    """The conventional name, which fixes the groups: enterprise.py's personas keep their ids, and
    the generated ones are <tenant>-<name>."""
    return persona.id if persona.id in NAMED else persona.id.rsplit("-", 1)[1]


def pct(share) -> str:
    return "n/a" if share is None else f"{100 * share:.1f}%"


# ---- measurement 1: exposure -------------------------------------------------------------------


def exposure_summary(records: list) -> dict:
    n = len(records)
    out = {"questions": n}
    for k in (5, 10):
        out[f"any_unreadable@{k}"] = round(sum(r[f"u{k}"] > 0 for r in records) / n, 4) if n else None
        out[f"mean_unreadable@{k}"] = round(sum(r[f"u{k}"] for r in records) / n, 3) if n else None
        out[f"any_canary@{k}"] = round(sum(r[f"c{k}"] > 0 for r in records) / n, 4) if n else None
    return out


def grouped(records: list, key) -> dict:
    groups = defaultdict(list)
    for r in records:
        groups[key(r)].append(r)
    return {name: exposure_summary(rows) for name, rows in groups.items()}


def exposure_table(title: str, rows: list) -> list:
    out = [
        f"### {title}",
        "",
        "| Group | Questions | Unreadable in top 5 | Mean | Canary in top 5 | Unreadable in top 10 | Mean | Canary in top 10 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for name, s in rows:
        out.append(
            f"| {name} | {s['questions']} | {pct(s['any_unreadable@5'])} | {s['mean_unreadable@5']:.2f} | "
            f"{pct(s['any_canary@5'])} | {pct(s['any_unreadable@10'])} | {s['mean_unreadable@10']:.2f} | "
            f"{pct(s['any_canary@10'])} |"
        )
    return [*out, ""]


def exposure_markdown(data: dict) -> str:
    by_category = data["by_category"]
    lines = [
        f"# X8b exposure, seed {SEED}" + (" (smoke: not a result)" if SMOKE else ""),
        "",
        f"{data['questions']} questions. For each group: the share of questions with at least one chunk the "
        "person may not read in the unfiltered exact top k, the mean count of such chunks, and the share with "
        "such a chunk that carries a canary.",
        "",
    ]
    lines += exposure_table(
        "By category", [*((c, by_category[c]) for c in CATEGORIES if c in by_category), ("all", data["all"])]
    )
    lines += exposure_table("By person type", sorted(data["by_type"].items()))
    lines += exposure_table("Red team, by attack", sorted(data["by_attack"].items()))
    lines += exposure_table("By category and person type", sorted(data["by_category_type"].items()))
    lines += ["### Readable chunks per person type", "", "| Type | People | Min | Median | Max |", "|---|---|---|---|---|"]
    for name, r in sorted(data["readable_by_type"].items()):
        lines.append(f"| {name} | {r['people']} | {r['min']} | {r['median']} | {r['max']} |")
    lines += ["", f"Detector and canary field disagree on {data['detector_disagreements']} question-k cells.", ""]
    return "\n".join(lines)


def exposure() -> list:
    """The exact top 10 of every question over the whole corpus, ignoring permissions: the harness's
    _baseline computation without the readable-set mask, on the harness's own vectors."""
    device = run.embed_device
    corpus = torch.from_numpy(run.vectors).to(device)
    queries = torch.from_numpy(np.ascontiguousarray(run.qvecs)).to(device)
    rows, scores = [], []
    for start in range(0, queries.shape[0], 128):
        values, found = torch.topk(queries[start : start + 128] @ corpus.T, 10, dim=1)
        rows += found.tolist()
        scores += values.tolist()
    del corpus, queries
    torch.cuda.empty_cache()

    records, disagreements = [], 0
    for i, pair in enumerate(run.pairs):
        person, mask = pair.persona, run.masks[pair.persona.id]
        record = {
            "i": i,
            "person": person.id,
            "type": person_type(person),
            "category": pair.category,
            "attack": pair.attack or None,
            "top10": [run.docs[r].id for r in rows[i]],
            "scores10": [round(s, 6) for s in scores[i]],
        }
        for k in (5, 10):
            unreadable = [r for r in rows[i][:k] if not mask[r]]
            flagged = [r for r in unreadable if run.detector.leaks(person, run.docs[r].text)]
            disagreements += len(flagged) != sum(run.docs[r].canary is not None for r in unreadable)
            record[f"u{k}"], record[f"c{k}"] = len(unreadable), len(flagged)
        records.append(record)

    readable = defaultdict(list)
    for p in run.people:
        readable[person_type(p)].append(int(run.masks[p.id].sum()))
    data = {
        "seed": SEED,
        "smoke": SMOKE,
        "questions": len(records),
        "corpus": run.corpus,
        "all": exposure_summary(records),
        "by_category": grouped(records, lambda r: r["category"]),
        "by_type": grouped(records, lambda r: r["type"]),
        "by_attack": grouped([r for r in records if r["attack"]], lambda r: r["attack"]),
        "by_category_type": grouped(records, lambda r: f"{r['category']}/{r['type']}"),
        "readable_by_type": {
            t: {"people": len(v), "min": min(v), "median": statistics.median(v), "max": max(v)}
            for t, v in readable.items()
        },
        "detector_disagreements": disagreements,
        "records": records,
    }
    save(f"x8b-exposure-seed{SEED}", data, exposure_markdown(data))
    print(exposure_markdown(data), flush=True)
    return records


# ---- measurement 2: the mutation positive control ------------------------------------------------

CALLS: list = []


class Recording(er.PermissionedRetriever):
    """The harness's retriever with `recheck` set for the pass, keeping every result it returns."""

    recheck_setting = True

    def __init__(self, backend, authorizer, **options):
        options.setdefault("recheck", Recording.recheck_setting)
        super().__init__(backend, authorizer, **options)

    def retrieve(self, query, subject, k=5):
        result = super().retrieve(query, subject, k=k)
        CALLS.append((id(query), k, result))
        return result


class MutatedFilter:
    """The policy with its pre-filter replaced on purpose; `check` stays the unmutated policy's."""

    def __init__(self, mutate) -> None:
        self.policy = er.tenant_acl()
        self.mutate = mutate

    def filter_for(self, subject, action="read"):
        return self.mutate(subject, action)

    def check(self, subject, hits, action="read"):
        return self.policy.check(subject, hits, action)


NEXT_TENANT = {t: er.TENANT_IDS[(j + 1) % len(er.TENANT_IDS)] for j, t in enumerate(er.TENANT_IDS)}


def admit_all(subject, action):
    """Every chunk's tenant field names one of these, or all of them."""
    return In("tenant", er.TENANT_IDS)


def second_tenant(subject, action):
    """A tenant-boundary fault: the next tenant's chunks pass the tenant clause; the ACL clause stands."""
    tenant = subject.attributes["tenant"]
    return And(In("tenant", [tenant, NEXT_TENANT[tenant]]), MetadataACLAuthorizer().filter_for(subject, action))


def acl_dropped(subject, action):
    """An ACL fault inside the tenant: the tenant clause alone."""
    return TenantAuthorizer().filter_for(subject, action)


MUTATIONS = {"M1": admit_all, "M2": second_tenant, "M3": acl_dropped}
PASSES = (
    ("faiss", None, True),  # P0, the unmutated policy; the label keeps the harness's exact-search check
    ("M1-off", "M1", False),
    ("M2-off", "M2", False),
    ("M3-off", "M3", False),
    ("M1-on", "M1", True),
    ("M2-on", "M2", True),
    ("M3-on", "M3", True),
)
HARNESS_FIELDS = (
    "questions",
    "retrieved",
    "hits_checked",
    "strategies",
    "incomplete",
    "violations",
    "errors",
    "error_examples",
    "unreadable_hits",
    "leaks",
    "leak_examples",
    "recall@5",
    "recall@10",
    "retrieval_ms",
    "end_to_end_ms",
    "generation",
    "quality",
    "seconds",
)


def admission() -> dict:
    """Per pre-filter and person, the chunks it admits that the person may not read, and the readable
    chunks it leaves out: `matches` on one chunk per distinct (tenants, readers), the only metadata
    these filters read."""
    keys, examples = {}, []
    of_row = np.empty(len(run.docs), dtype=np.int64)
    for row, d in enumerate(run.docs):
        key = (d.tenants, d.readers)
        if key not in keys:
            keys[key] = len(examples)
            examples.append(d)
        of_row[row] = keys[key]
    size = np.bincount(of_row, minlength=len(examples))
    metadata = [d.metadata() for d in examples]
    filters = {"P0": lambda s, a: er.tenant_acl().filter_for(s, a), **MUTATIONS}
    out = {}
    for name, make in filters.items():
        extra, missing = [], []
        for p in run.people:
            f = make(er.person_subject(p), "read")
            admitted = np.array([matches(f, m) for m in metadata], dtype=bool)
            readable = np.array([er.readable(p, d) for d in examples], dtype=bool)
            extra.append(int(size[admitted & ~readable].sum()))
            missing.append(int(size[readable & ~admitted].sum()))
        out[name] = {
            "people_over_admitted": sum(e > 0 for e in extra),
            "over_admitted_min": min(extra),
            "over_admitted_median": statistics.median(extra),
            "over_admitted_max": max(extra),
            "readable_left_out_max": max(missing),
        }
    return out


def main_retrievals() -> tuple:
    """Each question's two main retrievals (k, then recall_k) from the recorded calls. The warm-up
    and the end-to-end questions retrieve only at k, so a call at recall_k and the call before it
    are the main pair."""
    position = {id(q): i for i, q in enumerate(run.queries)}
    top, wide, unpaired, previous = {}, {}, 0, None
    for call in CALLS:
        query, k, result = call
        if k == run.cfg.recall_k:
            if previous is not None and previous[0] == query and previous[1] == run.cfg.k:
                top[position[query]], wide[position[query]] = previous[2], result
            else:
                unpaired += 1
        previous = call
    return top, wide, unpaired


def unreadable_ids(person, hits) -> list:
    """As the harness's _check_hits decides it."""
    out = []
    for hit in hits:
        row = run.row_of.get(hit.id)
        if row is None or not er.readable(person, run.docs[row]):
            out.append(hit.id)
    return out


def per_question() -> tuple:
    top, wide, unpaired = main_retrievals()
    rows = []
    for i, pair in enumerate(run.pairs):
        if i not in top:
            continue
        person = pair.persona
        hits5, hits10 = top[i].hits, wide[i].hits
        chat = er.messages(pair, hits5)
        answer_text = None
        if run.assistant is not None:
            answer_text = run.assistant.answers.get(run.assistant._key(run.assistant.render(chat)))
        rows.append(
            {
                "i": i,
                "person": person.id,
                "type": person_type(person),
                "category": pair.category,
                "attack": pair.attack or None,
                "n5": len(hits5),
                "n10": len(hits10),
                "u5": unreadable_ids(person, hits5),
                "u10": unreadable_ids(person, hits10),
                "chunk": sorted({d for h in [*hits5, *hits10] for d in run.detector.leaks(person, h.text)}),
                "prompt": sorted(set(run.detector.leaks(person, "\n".join(m["content"] for m in chat)))),
                "answer": sorted(set(run.detector.leaks(person, answer_text))) if answer_text else [],
                "answered": answer_text is not None,
                "violations": top[i].violations + wide[i].violations,
                "complete": top[i].complete and wide[i].complete,
                "ids10": [h.id for h in hits10],
                "scores10": [round(h.score, 6) for h in hits10],
            }
        )
    return rows, unpaired


def question_counts(rows: list) -> dict:
    return {
        "questions": len(rows),
        "with_unreadable@5": sum(bool(r["u5"]) for r in rows),
        "with_unreadable@10": sum(bool(r["u10"]) for r in rows),
        "unreadable_5_plus_10": sum(len(r["u5"]) + len(r["u10"]) for r in rows),
        "distinct_question_chunk": sum(len(set(r["u5"]) | set(r["u10"])) for r in rows),
        "with_canary_chunk": sum(bool(r["chunk"]) for r in rows),
        "with_canary_prompt": sum(bool(r["prompt"]) for r in rows),
        "with_canary_answer": sum(bool(r["answer"]) for r in rows),
        "distinct_question_canary_chunk": sum(len(r["chunk"]) for r in rows),
        "distinct_question_canary_prompt": sum(len(r["prompt"]) for r in rows),
        "distinct_question_canary_answer": sum(len(r["answer"]) for r in rows),
        "with_violations": sum(r["violations"] > 0 for r in rows),
        "violations": sum(r["violations"] for r in rows),
        "incomplete": sum(not r["complete"] for r in rows),
        "answered": sum(r["answered"] for r in rows),
    }


def question_summary(rows: list) -> dict:
    out = {"all": question_counts(rows)}
    for category in CATEGORIES:
        selected = [r for r in rows if r["category"] == category]
        if selected:
            out[category] = question_counts(selected)
    return out


def agreement(rows: list, records: list) -> dict:
    """M1-off against measurement 1: both are unfiltered exact search, one through the store."""
    same_set = same_u5 = same_u10 = ties = 0
    different = []
    for r in rows:
        e = records[r["i"]]
        if set(r["ids10"]) == set(e["top10"]):
            same_set += 1
        else:
            scores = {**dict(zip(e["top10"], e["scores10"])), **dict(zip(r["ids10"], r["scores10"]))}
            changed = set(r["ids10"]) ^ set(e["top10"])
            ties += all(abs(scores[d] - e["scores10"][-1]) <= 1e-4 for d in changed)
            if len(different) < 5:
                different.append({"i": r["i"], "changed": sorted(changed)})
        same_u5 += len(r["u5"]) == e["u5"]
        same_u10 += len(r["u10"]) == e["u10"]
    return {
        "questions": len(rows),
        "same_ids@10": same_set,
        "different_only_at_ties": ties,
        "same_u5": same_u5,
        "same_u10": same_u10,
        "examples": different,
    }


def examples(rows: list, field: str, n: int = 5) -> list:
    picked = [r for r in rows if r[field]]
    return [{"person": r["person"], "category": r["category"], "attack": r["attack"], field: r[field][:3]} for r in picked[:n]]


def control_markdown(results: dict) -> str:
    lines = [f"# X8b positive control, seed {SEED}" + (" (smoke: not a result)" if SMOKE else ""), ""]
    lines += [
        "## What each pre-filter admits",
        "",
        "| Filter | People over-admitted | Over-admitted chunks min / median / max | Readable chunks left out (max) |",
        "|---|---|---|---|",
    ]
    for name, a in (results.get("admission") or {}).items():
        lines.append(
            f"| {name} | {a['people_over_admitted']} | {a['over_admitted_min']} / {a['over_admitted_median']} / "
            f"{a['over_admitted_max']} | {a['readable_left_out_max']} |"
        )
    lines += [
        "",
        "## The harness's counts (both retrievals and the end-to-end questions)",
        "",
        "| Pass | Re-check | Hits checked | Unreadable hits | Canaries chunk / prompt / answer | Violations | Errors | "
        "Failed checks | Recall@10 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for label, p in results["passes"].items():
        h, state = p.get("harness"), "on" if p["recheck"] else "off"
        if h is None:
            lines.append(f"| {label} | {state} | pass failed | | | | | | |")
            continue
        leaks = h["leaks"]
        failed = sum(not c["ok"] for c in p["checks"])
        lines.append(
            f"| {label} | {state} | {h['hits_checked']} | {h['unreadable_hits']} | {leaks['retrieved']} / "
            f"{leaks['prompts']} / {leaks['answers']} | {h['violations']} | {h['errors']} | {failed} | {h['recall@10']} |"
        )
    lines += [
        "",
        "## Per question (main retrievals only)",
        "",
        "| Pass | Questions | With unreadable hit k=5 | k=10 | Distinct (question, chunk) | Canary in chunk | Prompt | "
        "Answer | With violations | Incomplete |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for label, p in results["passes"].items():
        q = p.get("per_question")
        if q is None:
            continue
        a = q["all"]
        lines.append(
            f"| {label} | {a['questions']} | {a['with_unreadable@5']} | {a['with_unreadable@10']} | "
            f"{a['distinct_question_chunk']} | {a['with_canary_chunk']} | {a['with_canary_prompt']} | "
            f"{a['with_canary_answer']} | {a['with_violations']} | {a['incomplete']} |"
        )
    lines += [
        "",
        "## Per question and category (questions with a detection)",
        "",
        "| Pass | Category | Questions | Unreadable k=5 | k=10 | Canary in chunk | Prompt | Answer | With violations |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for label, p in results["passes"].items():
        q = p.get("per_question")
        if q is None:
            continue
        for category in CATEGORIES:
            if category in q:
                c = q[category]
                lines.append(
                    f"| {label} | {category} | {c['questions']} | {c['with_unreadable@5']} | {c['with_unreadable@10']} | "
                    f"{c['with_canary_chunk']} | {c['with_canary_prompt']} | {c['with_canary_answer']} | "
                    f"{c['with_violations']} |"
                )
    if results.get("m1_against_exposure"):
        m = results["m1_against_exposure"]
        lines += [
            "",
            "## M1-off against measurement 1",
            "",
            f"Of {m['questions']} questions: same chunk ids at k=10 {m['same_ids@10']}, different only at ties within "
            f"1e-4 of the tenth score {m['different_only_at_ties']}, same unreadable count at k=5 {m['same_u5']}, "
            f"at k=10 {m['same_u10']}.",
        ]
    lines.append("")
    return "\n".join(lines)


def evaluate_pass(label: str, backend, authorizer, load: dict) -> dict:
    row = run.evaluate(label, backend, authorizer, er.person_subject)
    run.rows.append({"store": "faiss", **row, "load": load})
    return row


def control(records) -> None:
    er.PermissionedRetriever = Recording
    store = er.FaissStore(run)
    load = store.load()
    load["rows"] = store.count()
    run.report.check(f"faiss: holds all {len(run.docs):,} chunks", load["rows"] == len(run.docs), str(load["rows"]))
    backend = store.backend()
    results = {"seed": SEED, "smoke": SMOKE, "load": load, "admission": admission(), "passes": {}}
    questions = {}
    print(json.dumps(results["admission"], indent=1), flush=True)
    for label, mutation, recheck in PASSES:
        CALLS.clear()
        Recording.recheck_setting = recheck
        authorizer = er.tenant_acl() if mutation is None else MutatedFilter(MUTATIONS[mutation])
        before = len(run.report.checks)
        row = run.report.run(f"{label}: questions", partial(evaluate_pass, label, backend, authorizer, load))
        entry = {
            "mutation": mutation,
            "recheck": recheck,
            "checks": [{"check": n, "ok": ok, "detail": d[:300]} for n, ok, d in run.report.checks[before:]],
        }
        if row is not None:
            entry["harness"] = {name: row[name] for name in HARNESS_FIELDS}
            try:
                rows, unpaired = per_question()
                entry["unpaired_calls"] = unpaired
                entry["per_question"] = question_summary(rows)
                entry["examples"] = {f: examples(rows, f) for f in ("u5", "chunk", "prompt", "answer")}
                if label == "M1-off" and records:
                    results["m1_against_exposure"] = agreement(rows, records)
                questions[label] = [{k: v for k, v in r.items() if k not in ("ids10", "scores10")} for r in rows]
                (WORK / f"x8b-control-seed{SEED}-questions.json").write_text(json.dumps(questions), encoding="utf-8")
            except Exception as error:  # the harness's own counts above still stand
                traceback.print_exc()
                entry["per_question_error"] = f"{type(error).__name__}: {error}"
        results["passes"][label] = entry
        if run.assistant is not None:
            run.assistant.save()
        save(f"x8b-control-seed{SEED}", results, control_markdown(results))
    print(control_markdown(results), flush=True)
    store.stop()


# ---- the run -------------------------------------------------------------------------------------

run.environment_check()
run.build_corpus()
run.embed()
run.baseline()
exposure_records = run.report.run("exposure (amendment 2, measurement 1)", exposure)
if CONTROL:
    run.load_llm()
    run.report.run("positive control (amendment 2, measurement 2)", partial(control, exposure_records))
failed = run.finish()
for path in (WORK / "cache").glob("chunks-*.npy"):  # 330 MB that nothing reads after this point
    path.unlink()
note = " (the mutated passes are meant to fail theirs)" if CONTROL else ""
print(f"X8b seed {SEED}: {failed} failed checks{note}, {time.time() - started:.0f} s", flush=True)
