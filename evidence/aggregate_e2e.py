"""Aggregates of the end-to-end runs (X0 and the X8 repeats, and X8-FGA), computed from evidence/raw only.

    python evidence/aggregate_e2e.py > evidence/e2e-aggregates.md

Every number the paper gives for more than one end-to-end run comes from this script's output; it reads
each run's results.json, answers.jsonl and kernel log and writes nothing else.
"""

import collections
import json
import math
import sys
from pathlib import Path

RAW = Path(__file__).resolve().parent / "raw"
RUNS = [("X0, seed 7", "x0-seed7"), ("X8, seed 11", "x8-seed11"), ("X8, seed 13", "x8-seed13"),
        ("X8, seed 17", "x8-seed17")]
FGA_RUNS = [(f"X8-FGA, seed {s}", f"x8fga-seed{s}") for s in (7, 11, 13, 17)]
PG = ("pgvector", "pgvector + OPA", "pgvector + OpenFGA")
FAST_MS = 100.0  # a run is "fast" for a pgvector configuration when its median retrieval is below this


def results(run):
    return json.loads((RAW / run / "results.json").read_text(encoding="utf-8"))


def answers(run):
    with open(RAW / run / "answers.jsonl", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def kernel_seconds(run):
    """The last `time` field of the kernel log (the session's seconds since start)."""
    logs = [p for p in (RAW / run).glob("*.log") if p.read_text(encoding="utf-8", errors="replace").startswith("[{")]
    last = None
    for p in logs:
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if '"time":' in line:
                last = float(line.split('"time":', 1)[1].split(",", 1)[0])
    return last


def empties(rows):
    """Empty answers and people per pgvector configuration, counted as in evidence/x8-run.md: no hits where the
    exact baseline (FAISS, same person and question) has hits; without a FAISS pass, leaving out the people
    whose answers are empty in every store of the run (the one person who may read nothing)."""
    faiss = {(a["person"], a["question"]): bool(a["hits"]) for a in rows if a["store"] == "faiss"}
    always_empty = None
    if not faiss:
        by_person = collections.defaultdict(list)
        for a in rows:
            by_person[a["person"]].append(bool(a["hits"]))
        always_empty = {p for p, got in by_person.items() if not any(got)}
    out = {}
    for store in PG:
        mine = [a for a in rows if a["store"] == store]
        if not mine:
            continue
        if faiss:
            bad = [a for a in mine if not a["hits"] and faiss.get((a["person"], a["question"]))]
        else:
            bad = [a for a in mine if not a["hits"] and a["person"] not in always_empty]
        out[store] = (len(bad), len({a["person"] for a in bad}), sorted({a["person"] for a in bad}))
    return out, always_empty


def bound(n):
    return 1 - 0.05 ** (1 / n)


def fmt(x, d=3):
    return "n/a" if x is None else f"{x:.{d}f}"


def main():
    out = sys.stdout
    data = {label: (results(run), answers(run)) for label, run in RUNS + FGA_RUNS}
    four = [label for label, _ in RUNS]

    out.write("# End-to-end aggregates (computed by evidence/aggregate_e2e.py)\n\n")
    out.write("## Outcomes per run\n\n| Run | Checks passed / failed | Failed checks | Kernel seconds |\n|---|---|---|---|\n")
    for label, run in RUNS + FGA_RUNS:
        r = data[label][0]
        failed = "; ".join(f"{c['check']}: {c.get('detail', '')}".rstrip(": ") for c in r["failed"]) or "none"
        out.write(f"| {label} | {r['passed']} / {len(r['failed'])} | {failed} | {kernel_seconds(run)} |\n")

    out.write("\n## Empty answers / people, pgvector configurations\n\n| Run | " + " | ".join(PG) + " | People left out |\n")
    out.write("|---|---|---|---|---|\n")
    for label, _ in RUNS + FGA_RUNS:
        e, left = empties(data[label][1])
        cells = [f"{e[s][0]} / {e[s][1]} {e[s][2]}" if s in e else "" for s in PG]
        out.write(f"| {label} | " + " | ".join(cells) + f" | {sorted(left) if left else ''} |\n")

    out.write("\n## Safety\n\n| Run | Configurations | Questions | Hits checked | Unreadable | Leaks retrieved/prompts/answers"
              " | Violations | Errors |\n|---|---|---|---|---|---|---|---|\n")
    tot = collections.Counter()
    per_config = collections.defaultdict(list)
    for label in four + [l for l, _ in FGA_RUNS]:
        stores = data[label][0]["stores"]
        c = collections.Counter()
        for s in stores:
            c["questions"] += s["questions"]
            c["hits"] += s["hits_checked"]
            c["unreadable"] += s["unreadable_hits"]
            for k in ("retrieved", "prompts", "answers"):
                c["leak_" + k] += s["leaks"][k]
            c["violations"] += s["violations"]
            c["errors"] += s["errors"]
            per_config[(label in four, s["label"])].append(s["hits_checked"])
        out.write(f"| {label} | {len(stores)} | {c['questions']:,} | {c['hits']:,} | {c['unreadable']} | "
                  f"{c['leak_retrieved']}/{c['leak_prompts']}/{c['leak_answers']} | {c['violations']} | {c['errors']} |\n")
        if label in four:
            tot += c
    out.write(f"| **X0 and X8, four runs** | | **{tot['questions']:,}** | **{tot['hits']:,}** | **{tot['unreadable']}** | "
              f"**{tot['leak_retrieved']}/{tot['leak_prompts']}/{tot['leak_answers']}** | **{tot['violations']}** | "
              f"**{tot['errors']}** |\n\nHits checked per configuration, four runs: ")
    out.write("; ".join(f"{name} {sum(v):,} ({' + '.join(f'{x:,}' for x in v)})"
                        for (is_four, name), v in per_config.items() if is_four) + ".\n")
    fga_hits = [s["hits_checked"] for l, _ in FGA_RUNS for s in data[l][0]["stores"] if s["label"] == "pgvector + OpenFGA"]
    out.write(f"pgvector + OpenFGA over the four X8-FGA runs: {sum(fga_hits):,} hits checked.\n")

    pairs = collections.Counter()
    for label in four:
        seen = {(a["person"], a["question"]) for a in data[label][1] if a["store"] == "faiss"}
        pairs.update(seen)
    spread = collections.Counter(pairs.values())
    n_q = 4 * data[four[0]][0]["corpus"]["questions"]
    out.write(f"\nLeak bounds: {n_q:,} questions per configuration, one-sided 95% bound {bound(n_q):.2e}; "
              f"{len(pairs):,} distinct (person, question) pairs over the four runs "
              f"(in four runs: {spread.get(4, 0)}, three: {spread.get(3, 0)}, two: {spread.get(2, 0)}, one: {spread.get(1, 0)}), "
              f"bound {bound(len(pairs)):.2e}; X0 alone {bound(n_q // 4):.2e}; per person per run {bound(189):.2e}.\n")

    out.write("\n## Retrieval across the four runs (recall against exact search over the readable set)\n\n"
              "| Store | R@5 per run | mean | R@10 per run | mean | range R@10 | p50 ms per run | mode by p50 |\n"
              "|---|---|---|---|---|---|---|---|\n")
    labels = [s["label"] for s in data[four[0]][0]["stores"]]
    for name in labels:
        rows = [next(s for s in data[l][0]["stores"] if s["label"] == name) for l in four]
        r5 = [s["recall@5"] for s in rows]
        r10 = [s["recall@10"] for s in rows]
        p50 = [s["retrieval_ms"]["p50"] for s in rows]
        mode = " / ".join("fast" if p < FAST_MS else "exact" for p in p50) if name in PG else ""
        out.write(f"| {name} | {' / '.join(fmt(x) for x in r5)} | {fmt(sum(r5) / 4)} | {' / '.join(fmt(x) for x in r10)} | "
                  f"{fmt(sum(r10) / 4)} | {fmt(max(r10) - min(r10))} | {' / '.join(f'{p:g}' for p in p50)} | {mode} |\n")
    pg_modes = []
    for label in four + [l for l, _ in FGA_RUNS]:
        s = next(s for s in data[label][0]["stores"] if s["label"] == "pgvector")
        pg_modes.append((label, s["retrieval_ms"]["p50"], s["retrieval_ms"]["p95"], s["recall@10"]))
    out.write("\nIn-process pgvector over the eight runs (p50, p95 ms, recall@10): "
              + "; ".join(f"{l}: {a:g}, {b:g}, {fmt(c)} ({'fast' if a < FAST_MS else 'exact'})" for l, a, b, c in pg_modes) + ".\n")
    fast = [m for m in pg_modes if m[1] < FAST_MS]
    for group in ("fast", "exact"):
        g = fast if group == "fast" else [m for m in pg_modes if m[1] >= FAST_MS]
        if g:
            out.write(f"{group}: {len(g)} runs, recall@10 {fmt(min(m[3] for m in g))} to {fmt(max(m[3] for m in g))}, "
                      f"p50 {min(m[1] for m in g):g} to {max(m[1] for m in g):g} ms.\n")
    for name in ("pgvector", "pgvector + OPA"):
        g = [next(s for s in data[l][0]["stores"] if s["label"] == name) for l in four]
        f = [s for s in g if s["retrieval_ms"]["p50"] < FAST_MS]
        e = [s for s in g if s["retrieval_ms"]["p50"] >= FAST_MS]
        for tag, grp in (("fast", f), ("exact", e)):
            if grp:
                out.write(f"{name}, {tag} runs of the four: {len(grp)}; mean R@5 {fmt(sum(s['recall@5'] for s in grp) / len(grp))}, "
                          f"mean R@10 {fmt(sum(s['recall@10'] for s in grp) / len(grp))}, R@10 range "
                          f"{fmt(max(s['recall@10'] for s in grp) - min(s['recall@10'] for s in grp))}, p50 "
                          f"{min(s['retrieval_ms']['p50'] for s in grp):g} to {max(s['retrieval_ms']['p50'] for s in grp):g} ms.\n")
    loads = [(s["load"]["load_s"], s["load"]["index_s"]) for l in four for s in data[l][0]["stores"] if s["label"] == "pgvector"]
    out.write(f"pgvector load {min(a for a, _ in loads)} to {max(a for a, _ in loads)} s, index "
              f"{min(b for _, b in loads)} to {max(b for _, b in loads)} s over the four runs.\n")

    out.write("\n## The model\n\n| Run | Configurations | Injected notices retrieved | Obeyed | Per configuration |\n|---|---|---|---|---|\n")
    inj_four = [0, 0]
    inj_all = [0, 0]
    for label in four + [l for l, _ in FGA_RUNS]:
        q = [s["quality"] for s in data[label][0]["stores"]]
        got = [x["injected_notice_retrieved"] for x in q]
        obeyed = [x["injection_obeyed"] for x in q]
        out.write(f"| {label} | {len(q)} | {sum(got):,} | {sum(obeyed):,} | {min(got)} to {max(got)} |\n")
        inj_all[0] += sum(got)
        inj_all[1] += sum(obeyed)
        if label in four:
            inj_four[0] += sum(got)
            inj_four[1] += sum(obeyed)
    out.write(f"| **X0 and X8** | | **{inj_four[0]:,}** | **{inj_four[1]:,}** | |\n| **All eight runs** | | **{inj_all[0]:,}** | "
              f"**{inj_all[1]:,}** | |\n\n")
    qual = collections.defaultdict(list)
    for label in four:
        for s in data[label][0]["stores"]:
            q = s["quality"]
            qual[(s["label"], "target")].append(q["target_found@5"])
            qual[(s["label"], "accuracy")].append(q["answer_accuracy"])
            qual["abstained"].append(q["abstained_when_denied"])
    out.write(f"FAISS target in the top five {fmt(min(qual[('faiss', 'target')]))} to {fmt(max(qual[('faiss', 'target')]))}, "
              f"answer accuracy {fmt(min(qual[('faiss', 'accuracy')]))} to {fmt(max(qual[('faiss', 'accuracy')]))}; "
              f"Qdrant target in the top five {fmt(min(qual[('qdrant', 'target')]))} to {fmt(max(qual[('qdrant', 'target')]))}; "
              f"abstained when denied {fmt(min(qual['abstained']))} to {fmt(max(qual['abstained']))} over all stores of the four runs.\n")
    for label, _ in FGA_RUNS:
        s = next(s for s in data[label][0]["stores"] if s["label"] == "pgvector + OpenFGA")
        out.write(f"{label}, pgvector + OpenFGA: R@10 {fmt(s['recall@10'])}, p50 {s['retrieval_ms']['p50']:g} ms, "
                  f"injections {s['quality']['injected_notice_retrieved']}/{s['quality']['injection_obeyed']}.\n")


if __name__ == "__main__":
    main()
