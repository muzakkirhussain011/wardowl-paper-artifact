"""Reproducer of the second report in disclosure/chroma.md: a large `where` `$or` kills the embedded
client process (SIGSEGV), and about 1,000 clauses fail on SQLite's expression depth. chromadb and the
standard library only; no wardowl.

Each size runs the draft's code (a one-record collection, a flat `$or` of n `$eq` clauses on distinct
boolean keys) in a fresh child process with Python's fault handler on, because a crash ends the
process; the parent reports how the child ended. The draft's sizes come first: 1,001 and 15,500,
which the draft expects to be refused with the depth error, and 16,500 and 40,000, which it expects
to crash. Then, if some size crashed and a smaller one did not, the parent bisects between the
largest size that did not crash and the smallest that did, to 100 clauses.

    python chroma_crash.py            # the parent: every size, then the bisection
    python chroma_crash.py child N    # one child: the draft's code with N clauses

The parent exits 0 when every child ran to an outcome (answered, raised or died on a signal); the
RESULT lines say which.
"""

import json
import platform
import resource
import signal
import subprocess
import sys
import time

SIZES = (1_001, 15_500, 16_500, 40_000)
RESOLUTION = 100


def child(n: int) -> None:
    import chromadb

    c = chromadb.EphemeralClient().create_collection("t", embedding_function=None)
    c.add(ids=["a"], embeddings=[[1.0, 0.0, 0.0]], metadatas=[{"k0": True}])
    where = {"$or": [{f"k{i}": {"$eq": True}} for i in range(n)]}
    print(f"CHILD querying with {n} clauses, where-document {len(json.dumps(where))} characters", flush=True)
    try:
        result = c.query(query_embeddings=[[1.0, 0.0, 0.0]], n_results=1, where=where)
    except Exception as error:  # the depth refusal is an exception; a crash never gets here
        print("CHILD raised", type(error).__name__, str(error)[:400], flush=True)
        return
    print("CHILD answered", json.dumps(result["ids"]), flush=True)


def run(n: int) -> dict:
    start = time.monotonic()
    proc = subprocess.run(
        [sys.executable, "-X", "faulthandler", __file__, "child", str(n)],
        capture_output=True, text=True, timeout=900,
    )
    seconds = round(time.monotonic() - start, 1)
    out = proc.stdout.splitlines()
    err = proc.stderr.splitlines()
    if proc.returncode < 0:
        outcome = f"crashed, signal {signal.Signals(-proc.returncode).name}"
    elif any(line.startswith("CHILD answered") for line in out):
        outcome = "answered"
    elif any(line.startswith("CHILD raised") for line in out):
        outcome = "raised"
    else:
        outcome = "ended without an outcome"
    detail = next((line for line in out if line.startswith(("CHILD answered", "CHILD raised"))), "")
    fault = [line.strip() for line in err if "Fatal Python error" in line or line.strip().startswith("File ")][:8]
    record = {"clauses": n, "exit_status": proc.returncode, "outcome": outcome, "seconds": seconds,
              "detail": detail.removeprefix("CHILD ").strip(), "fault_handler": fault}
    print(json.dumps(record), flush=True)
    if outcome == "ended without an outcome":
        print("stderr tail:", *err[-15:], sep="\n  ", flush=True)
    return record


def parent() -> int:
    soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
    import importlib.metadata

    print(f"chromadb {importlib.metadata.version('chromadb')}, Python {platform.python_version()}, "
          f"{platform.platform()}, main-thread stack limit {soft} bytes (hard {hard})", flush=True)
    records = {n: run(n) for n in SIZES}
    crashed = lambda n: records[n]["exit_status"] < 0  # noqa: E731
    bracket = None
    crashes = sorted(n for n in records if crashed(n))
    if crashes:
        hi = crashes[0]
        below = [n for n in records if n < hi and not crashed(n)]
        if below:
            lo = max(below)
            while hi - lo > RESOLUTION:
                mid = (lo + hi) // 2
                records[mid] = run(mid)
                if crashed(mid):
                    hi = mid
                else:
                    lo = mid
            bracket = (lo, hi)
    for n in sorted(records):
        r = records[n]
        print(f"RESULT {n} clauses: {r['outcome']}, exit status {r['exit_status']}, {r['seconds']} s"
              + (f"; {r['detail']}" if r["detail"] else ""))
    if bracket:
        print(f"RESULT threshold: between {bracket[0]} clauses ({records[bracket[0]]['outcome']}) "
              f"and {bracket[1]} clauses ({records[bracket[1]]['outcome']})")
    fault = next((records[n]["fault_handler"] for n in sorted(records) if records[n]["fault_handler"]), [])
    if fault:
        print("RESULT fault handler (first crash):", " | ".join(fault))
    expected = {1_001: "raised", 15_500: "raised", 16_500: "crashed", 40_000: "crashed"}
    met = all(records[n]["outcome"].startswith(expected[n]) for n in SIZES)
    print("RESULT verdict:", "as the draft expects (1,001 and 15,500 raised; 16,500 and 40,000 crashed)"
          if met else "differs from the draft's expectation; see the sizes above")
    return 0 if all(r["outcome"] != "ended without an outcome" for r in records.values()) else 2


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "child":
        child(int(sys.argv[2]))
    else:
        sys.exit(parent())
