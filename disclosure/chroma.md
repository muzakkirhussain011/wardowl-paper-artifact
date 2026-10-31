# Draft upstream report: Chroma

Status: filed 2026-10-30 as https://github.com/chroma-core/chroma/issues/7969, with the text in
`disclosure/ready/chroma-issue-1-depth.md`. This file is the working draft and its evidence. Reproduced on 2026-10-30
with the reproducer below (one fix: the collection name) on chromadb 1.5.9, still the latest release that day, in
workflow runs 41007779363 and 41008151303; see "Reproduced (2026-10-30)". Run 1 of the campaign saw the error
through wardowl, whose filter had the shape of the second query; the reproducer showed that the
first, flat query fails the same way, so the title and "What happens" no longer say the `$or` is
nested.
Where: https://github.com/chroma-core/chroma/issues

State on 2026-10-31: open, no comments (GitHub API). The last paragraph of `disclosure/ready/chroma-issue-1-depth.md` was
corrected that day, and the filed issue was edited to match on 2026-11-01, with a note saying so: it no longer says the maintainers hear of the behavior
first, because the library's public pull request #187 had described the filter fault earlier on 2026-10-30. The run ids
in this file belong to the paper's private development repository, so their pages are not public. Every job's output is
public: `runs/<run id>/` on branch `results/reproducers` of the artifact repository, and
`evidence/raw/results-reproducers/runs/<run id>/` in the tag `evidence-v1`. `REPRODUCE.md` says how to rerun them.

## Title

A `$or` with about 1,000 operands fails with "Expression tree is too large (maximum depth 1000)",
whether flat or nested

## Version

`chromadb==1.5.9`, `EphemeralClient` (local mode).

## What happens

A `where` whose top level is `$or` over 1,001 simple conditions, or over 1,000 clauses that are each
a `$or` of two simple conditions, raises `InternalError: Error executing plan: Internal error: error
returned from database: (code: 1) Expression tree is too large (maximum depth 1000)`. The flat
document is one level deep and the nested one two, so the depth SQLite refuses grows with the
number of operands, not with the nesting of the `where` document; item 1 of the second report below
gives the cause in the code. The filter docs state no limit on the number of operands.

(Corrected 2026-10-30. This paragraph first described only the nested query, with the error text
shortened, and called the operand count a guess from the message; the reproducer showed the flat
query failing too, with the full text above.)

## Reproducer (Python, chromadb only)

```python
import chromadb

c = chromadb.EphemeralClient().create_collection("repro", embedding_function=None)
c.add(ids=["a"], embeddings=[[0.1, 0.2]], metadatas=[{"g": 1, "g::i:1": True}])

flat = {"$or": [{"g": {"$eq": i}} for i in range(1001)]}
nested = {"$or": [{"$or": [{"g": {"$in": [i]}}, {f"g::i:{i}": {"$eq": True}}]} for i in range(1000)]}
for where in (flat, nested):
    try:
        print(c.query(query_embeddings=[[0.1, 0.2]], n_results=1, where=where)["ids"])
    except Exception as error:
        print(type(error).__name__, error)
```

Expected: `[['a']]` for both, or a documented limit on the number of operands. Seen in our run:
the error above for queries shaped like `nested`.

Changed on 2026-10-30: the collection was named `"t"`, which chromadb 1.5.9 refuses before any
query (`InvalidArgumentError: Validation error: name: Expected a name containing 3-512 characters
from [a-zA-Z0-9._-], starting and ending with a character in [a-zA-Z0-9]. Got: t`, run
41007436602); it is `"repro"` now. Nothing else changed.

## Reproduced (2026-10-30)

Script `disclosure/reproducers/chroma_depth.py`: the code above, with a label on each printed line.
Workflow `.github/workflows/reproducers.yml`, GitHub-hosted ubuntu-24.04 runners, Python 3.12.15,
chromadb 1.5.9 from PyPI (the newest release on PyPI and the GitHub release marked Latest on
2026-10-30, so the "tested" and "latest" jobs ran the same version). Runs 41007779363 and
41008151303; outputs on branch `results/reproducers` under `runs/<run id>/chroma-depth-tested/` and
`chroma-depth-latest/`. Every job printed, for `flat` and for `nested` alike:

    InternalError Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000)

So both queries fail; neither returns `[['a']]`.

## Impact

Permission filters for users in many groups (one clause per group) fail whole. They fail closed, so
this is an availability limit, not a wrong answer.

## Suggested resolution

Build n-ary `$and`/`$or` as one node rather than a chain, or document the limit in operands.

---

# Second draft report (2026-10-30): a large `where` kills the embedded client process

Status: filed 2026-10-30 as https://github.com/chroma-core/chroma/issues/7970, a public issue, with the text in
`disclosure/ready/chroma-issue-2-crash.md`. This file is the working draft and its evidence. Reproduced on 2026-10-30 with the reproducer below (one fix: the collection name) on
chromadb 1.5.9, still the latest release that day, in workflow runs 41007779363 and 41008151303; see
"Reproduced (2026-10-30)" at the end. Source: X3 run 40940385704 (`evidence/x3-x6-run1.md`,
"X3: Chroma, refusal and crash"); the follow-up run 40982986417 under faulthandler added the stack and the
crash threshold (`evidence/x3-x6-followup.md`).

State on 2026-10-31: open, no comments (GitHub API). The last paragraph of `disclosure/ready/chroma-issue-2-crash.md` was
corrected that day, and the filed issue was edited to match on 2026-11-01, with a note saying so: it no longer says the maintainers hear of the behavior
first, because the library's public pull request #187 had described it earlier on 2026-10-30.

## Title

A `where` `$or` of about 40,000 clauses crashes the embedded client process (SIGSEGV); about 1,000
clauses fail on SQLite's expression depth

## Version

chromadb 1.5.9, `EphemeralClient`, Linux (GitHub-hosted ubuntu-24.04 runner, Python 3.12).

## What happens

1. A flat `$or` of about 1,000 or more `$eq` clauses fails with `InternalError: ... Expression tree
   is too large (maximum depth 1000)`. In `rust/segment/src/sqlite_metadata.rs` (tag 1.5.9),
   `CompositeExpression::eval` starts from a bound `false` (or `true` for `$and`) and folds in each
   child with `Expr::expr(expr).or(child.eval())`, so a flat `$or` of n clauses becomes a left-deep
   chain of binary ORs n levels deep, which SQLite refuses beyond 1,000.
2. A flat `$or` of about 40,000 `$eq` clauses on distinct boolean keys kills the client process
   with SIGSEGV on the first `query`, with no Python exception and no Rust panic message, in 5 of 5
   processes. 10,000 clauses gave the error of item 1 instead. A bisection on one corpus put the
   threshold between 15,500 clauses (refused with the depth error) and 16,500 (crash), the same
   bracket in two runs. Python's fault handler places the crash in `chromadb/api/rust.py`, line 582,
   `_query`; under gdb the main thread received SIGSEGV in `chromadb_rust_bindings.abi3.so` with the
   stack about 16,500 frames deep, the innermost frames all returning to one address in that library,
   while the tokio and sqlx-sqlite worker threads were idle. So the main thread ran out of stack in one
   recursive function of the Rust bindings, about one frame per clause [the per-clause
   correspondence is inferred from the frame count; the library has no symbols], before SQLite saw
   the query. Evidence: `evidence/x3-x6-followup.md`, item 6 (run 40982986417).

## Reproducer (Python, chromadb only; item 2 ends the interpreter)

```python
import chromadb

c = chromadb.EphemeralClient().create_collection("repro", embedding_function=None)
c.add(ids=["a"], embeddings=[[1.0, 0.0, 0.0]], metadatas=[{"k0": True}])
where = {"$or": [{f"k{i}": {"$eq": True}} for i in range(40_000)]}
c.query(query_embeddings=[[1.0, 0.0, 0.0]], n_results=1, where=where)  # SIGSEGV
```

Changed on 2026-10-30: the collection was named `"t"`, which chromadb 1.5.9 refuses (names need 3
to 512 characters); it is `"repro"` now. Nothing else changed.

## Impact

A client-supplied filter can take down the host process. An application that builds `where` from a
user's group memberships can be crashed by any user in enough groups. A single-node server probably
shares the code path [not tested].

## Suggested resolution

Render n-ary `$and` and `$or` as a balanced tree (or with sea-query's `Cond::any()` /
`Cond::all()`), and validate the size of a `where` with a clear error rather than letting native
code overflow. Documenting a size limit for local mode would help users. wardowl now nests its
disjunctions and refuses to send a `where` beyond conservative bounds (PR #187).

## Reproduced (2026-10-30)

Script `disclosure/reproducers/chroma_crash.py`: the code above, with the clause count as a
parameter, run once per count in a fresh child process with Python's fault handler on (a crash ends
the process, so the parent reports how each child ended). Counts: 1,001 and 15,500, expected to be
refused, and 16,500 and 40,000, expected to crash; then a bisection between the largest count that
did not crash and the smallest that did, to 100 clauses. Workflow
`.github/workflows/reproducers.yml`, GitHub-hosted ubuntu-24.04 runners, Python 3.12.15, chromadb
1.5.9 from PyPI (the newest release that day, so the "tested" and "latest" jobs ran the same
version), main-thread stack limit 16 MiB (`ulimit -s` 16384). Runs 41007779363 and 41008151303;
outputs on branch `results/reproducers` under `runs/<run id>/chroma-crash-tested/` and
`chroma-crash-latest/`.

The same outcome in every job:

| Clauses | Outcome | Exit status |
|---|---|---|
| 1,001 | `InternalError` "... Expression tree is too large (maximum depth 1000)" | 0 |
| 15,500; 16,000; 16,250; 16,375; 16,437 | the same error | 0 |
| 16,500 | SIGSEGV, no Python exception | -11 |
| 40,000 | SIGSEGV, no Python exception | -11 |

The fault handler printed "Fatal Python error: Segmentation fault" with the innermost frame
`chromadb/api/rust.py, line 582 in _query`, called from `chromadb/api/models/Collection.py, line
265 in query`, the same location as in run 40982986417. On this one-record collection the
threshold lies between 16,437 clauses (refused) and 16,500 (crash), inside the 15,500 to 16,500
bracket of item 2. A stack overflow depends on the main thread's stack size (16 MiB here), so
another limit would move the threshold [not tested].
