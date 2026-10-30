# X8b recount (plan/x8-prereg.md, amendment 2): a check of what evidence/x8-controls.md and the paper's
# appendix state question by question, from the control kernel's per-question output, and of whether
# M3-off's unreadable hits stay inside the asker's tenant. Not a new measurement. No model and no GPU.
import json
from collections import Counter, defaultdict
from pathlib import Path

WORK = Path("/kaggle/working")
CATEGORIES = ("generic", "targeted", "forbidden", "redteam")
GLOBEX_NAMED = {"grace", "heidi"}
NORTHWIND_NAMED = {"alice", "bob", "carol", "dave", "erin", "frank", "mallory"}


def tenant_of(person: str) -> str:
    if person in GLOBEX_NAMED:
        return "globex"
    if person in NORTHWIND_NAMED:
        return "northwind"
    return person.rsplit("-", 1)[0]


path = sorted(Path("/kaggle/input").rglob("x8b-control-seed7-questions.json"))[0]
print(path, flush=True)
data = json.loads(path.read_text(encoding="utf-8"))
results = {"passes": {label: len(rows) for label, rows in data.items()}, "mutations": {}}
lines = ["# X8b recount of the control's per-question claims, seed 7", ""]
lines += [
    "| Mutation | Questions | Exposed off | Violations on | Incomplete on | Exposed, no violation | Violation, not exposed | "
    "Exposed, not incomplete | Incomplete, not exposed | Questions where counts differ | Unreadable off | Violations on | "
    "k=5 without k=10 | Answer canary | Answer canary not in prompt | Prompt canary | Prompt canary not in chunk |",
    "|" + "---|" * 17,
]
for mutation in ("M1", "M2", "M3"):
    off = {r["i"]: r for r in data[f"{mutation}-off"]}
    on = {r["i"]: r for r in data[f"{mutation}-on"]}
    if set(off) != set(on):
        raise SystemExit(f"{mutation}: the passes hold different questions")
    exposed = {i for i, r in off.items() if r["u5"] or r["u10"]}
    flagged = {i for i, r in on.items() if r["violations"] > 0}
    incomplete = {i for i, r in on.items() if not r["complete"]}
    row = {
        "questions": len(off),
        "exposed_off": len(exposed),
        "violations_on_questions": len(flagged),
        "incomplete_on_questions": len(incomplete),
        "exposed_no_violation": len(exposed - flagged),
        "violation_not_exposed": len(flagged - exposed),
        "exposed_not_incomplete": len(exposed - incomplete),
        "incomplete_not_exposed": len(incomplete - exposed),
        "questions_where_counts_differ": sum(len(off[i]["u5"]) + len(off[i]["u10"]) != on[i]["violations"] for i in off),
        "unreadable_off": sum(len(r["u5"]) + len(r["u10"]) for r in off.values()),
        "violations_on": sum(r["violations"] for r in on.values()),
        "k5_without_k10": sum(bool(r["u5"]) and not r["u10"] for r in off.values()),
        "answer_canary": sum(bool(r["answer"]) for r in off.values()),
        "answer_canary_not_in_prompt": sum(bool(set(r["answer"]) - set(r["prompt"])) for r in off.values()),
        "prompt_canary": sum(bool(r["prompt"]) for r in off.values()),
        "prompt_canary_not_in_chunk": sum(bool(set(r["prompt"]) - set(r["chunk"])) for r in off.values()),
    }
    results["mutations"][mutation] = row
    lines.append(f"| {mutation} | " + " | ".join(str(v) for v in row.values()) + " |")

# M3-off is exact search inside the asker's tenant: where do its unreadable hits lie?
where = Counter()
per_category = defaultdict(lambda: {"questions": 0, "u5": 0, "u10": 0})
per_type = defaultdict(lambda: {"questions": 0, "u5": 0, "u10": 0})
for r in data["M3-off"]:
    tenant = tenant_of(r["person"])
    for hit in set(r["u5"]) | set(r["u10"]):
        if hit.startswith("kb/"):
            where["shared passage"] += 1
        elif hit.startswith(f"{tenant}/"):
            where["own tenant"] += 1
        else:
            where["other tenant"] += 1
    for bucket in (per_category[r["category"]], per_type[r["type"]]):
        bucket["questions"] += 1
        bucket["u5"] += bool(r["u5"])
        bucket["u10"] += bool(r["u10"])
results["m3_off_where"] = dict(where)
results["m3_off_by_category"] = dict(per_category)
results["m3_off_by_type"] = dict(per_type)
lines += [
    "",
    "## M3-off: distinct (question, chunk) unreadable pairs by where the chunk lies",
    "",
    *(f"- {name}: {where[name]}" for name in ("own tenant", "shared passage", "other tenant")),
    "",
    "## M3-off: questions with an unreadable hit",
    "",
    "| Group | Questions | k=5 | k=10 |",
    "|---|---|---|---|",
]
for name in CATEGORIES:
    b = per_category[name]
    lines.append(f"| {name} | {b['questions']} | {b['u5']} | {b['u10']} |")
for name in sorted(per_type):
    b = per_type[name]
    lines.append(f"| {name} | {b['questions']} | {b['u5']} | {b['u10']} |")
lines.append("")
text = "\n".join(lines)
(WORK / "x8b-verify.json").write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
(WORK / "x8b-verify.md").write_text(text, encoding="utf-8")
print(text, flush=True)
