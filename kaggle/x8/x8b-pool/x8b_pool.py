# X8b (plan/x8-prereg.md, amendment 2): measurement 1 pooled over the four seeds, from the outputs of
# the exposure kernels. No model and no GPU.
import json
from collections import defaultdict
from pathlib import Path

CATEGORIES = ("generic", "targeted", "forbidden", "redteam")
SEEDS = [7, 11, 13, 17]
WORK = Path("/kaggle/working")

files = sorted(Path("/kaggle/input").rglob("x8b-exposure-seed*.json"))
print("\n".join(str(f) for f in files), flush=True)
runs = {}
for path in files:
    data = json.loads(path.read_text(encoding="utf-8"))
    runs[data["seed"]] = data
if sorted(runs) != SEEDS:
    raise SystemExit(f"expected seeds {SEEDS}, found {sorted(runs)}")
if any(d["smoke"] for d in runs.values()):
    raise SystemExit("a smoke output reached the pool")


def summary(records: list) -> dict:
    n = len(records)
    out = {"questions": n}
    for k in (5, 10):
        out[f"any_unreadable@{k}"] = round(sum(r[f"u{k}"] > 0 for r in records) / n, 4)
        out[f"mean_unreadable@{k}"] = round(sum(r[f"u{k}"] for r in records) / n, 3)
        out[f"any_canary@{k}"] = round(sum(r[f"c{k}"] > 0 for r in records) / n, 4)
    return out


def grouped(records: list, key) -> dict:
    groups = defaultdict(list)
    for r in records:
        groups[key(r)].append(r)
    return {name: summary(rows) for name, rows in groups.items()}


def pct(share: float) -> str:
    return f"{100 * share:.1f}%"


def table(title: str, rows: list) -> list:
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


records = [r for seed in SEEDS for r in runs[seed]["records"]]
pooled = {
    "seeds": SEEDS,
    "questions": len(records),
    "all": summary(records),
    "by_category": grouped(records, lambda r: r["category"]),
    "by_type": grouped(records, lambda r: r["type"]),
    "by_attack": grouped([r for r in records if r["attack"]], lambda r: r["attack"]),
    "by_category_type": grouped(records, lambda r: f"{r['category']}/{r['type']}"),
    "per_seed": {str(seed): {"all": runs[seed]["all"], "by_category": runs[seed]["by_category"]} for seed in SEEDS},
    "detector_disagreements": {str(seed): runs[seed]["detector_disagreements"] for seed in SEEDS},
    "corpus": {str(seed): runs[seed]["corpus"] for seed in SEEDS},
    "readable_by_type": {str(seed): runs[seed]["readable_by_type"] for seed in SEEDS},
}
by_category = pooled["by_category"]
lines = [
    "# X8b exposure, pooled over seeds 7, 11, 13 and 17",
    "",
    f"{len(records)} questions. For each group: the share of questions with at least one chunk the person may not "
    "read in the unfiltered exact top k, the mean count of such chunks, and the share with such a chunk that "
    "carries a canary.",
    "",
]
lines += table("By category", [*((c, by_category[c]) for c in CATEGORIES), ("all", pooled["all"])])
lines += table("By person type", sorted(pooled["by_type"].items()))
lines += table("Red team, by attack", sorted(pooled["by_attack"].items()))
lines += table("By category and person type", sorted(pooled["by_category_type"].items()))
lines += [
    "### Per seed, by category (top 5)",
    "",
    "| Category | Unreadable, seeds 7 / 11 / 13 / 17 | Lowest | Canary, seeds 7 / 11 / 13 / 17 | Lowest |",
    "|---|---|---|---|---|",
]
for category in CATEGORIES:
    unreadable = [runs[seed]["by_category"][category]["any_unreadable@5"] for seed in SEEDS]
    canary = [runs[seed]["by_category"][category]["any_canary@5"] for seed in SEEDS]
    lines.append(
        f"| {category} | {' / '.join(pct(u) for u in unreadable)} | {pct(min(unreadable))} | "
        f"{' / '.join(pct(c) for c in canary)} | {pct(min(canary))} |"
    )
lines += [
    "",
    "Detector and canary field disagree on "
    + ", ".join(f"{runs[seed]['detector_disagreements']} (seed {seed})" for seed in SEEDS)
    + " question-k cells.",
    "",
]
text = "\n".join(lines)
(WORK / "x8b-exposure-pooled.json").write_text(json.dumps(pooled, indent=1) + "\n", encoding="utf-8")
(WORK / "x8b-exposure-pooled.md").write_text(text, encoding="utf-8")
print(text, flush=True)
