<!-- File at https://github.com/chroma-core/chroma/issues/new?template=bug_report.yaml
     Title:
     [Bug]: A where $or of about 16,500 or more clauses crashes the embedded client process (SIGSEGV)
     The form has three fields. Paste each section below into its field. -->

## What happened?

Thanks for Chroma. I found that a very large filter ends the embedded client process instead of returning an error, and I wanted to pass it on. Please correct me if I have misread anything.

A flat `$or` of about 16,500 or more `$eq` clauses on distinct boolean keys ends the client process with SIGSEGV on the first `query`, with no Python exception and no Rust panic message. Smaller filters get the expression-depth error instead, which I reported separately in #7969.

```python
import chromadb

c = chromadb.EphemeralClient().create_collection("repro", embedding_function=None)
c.add(ids=["a"], embeddings=[[1.0, 0.0, 0.0]], metadatas=[{"k0": True}])
where = {"$or": [{f"k{i}": {"$eq": True}} for i in range(40_000)]}
c.query(query_embeddings=[[1.0, 0.0, 0.0]], n_results=1, where=where)  # SIGSEGV
```

Each count ran once in a fresh child process, with a main-thread stack limit of 16 MiB (`ulimit -s 16384`):

| Clauses | Outcome | Exit status |
|---|---|---|
| 1,001 | `InternalError` "... Expression tree is too large (maximum depth 1000)" | 0 |
| 15,500; 16,000; 16,250; 16,375; 16,437 | the same error | 0 |
| 16,500 | SIGSEGV, no Python exception | -11 |
| 40,000 | SIGSEGV, no Python exception | -11 |

Under gdb, in an earlier run, the main thread received SIGSEGV in `chromadb_rust_bindings.abi3.so` with the stack about 16,500 frames deep, the innermost frames all returning to one address in that library, while the tokio and sqlx-sqlite worker threads were idle. The library has no symbols, so I could not name the function. I did not test other stack limits.

I met this with a filter built from a user's group memberships, one clause per group. I have not measured how many groups users have in practice, and I did not test server mode.

If it helps, one option would be to render n-ary `$and` and `$or` as a balanced tree, or with sea-query's `Cond::any()` and `Cond::all()`, and to validate the size of a `where` with a clear error. A documented size limit for local mode would also help. You know this code far better than I do, so please take that only as a suggestion.

I came across this while testing for a research paper on permission-aware retrieval. The paper mentions this behavior, and I wanted to let you know before it appears. If anything here is wrong, or if you would like the paper to describe it differently or to mention a fix, please tell me and I will update it.

The code and output here come from real runs, and I will follow this issue and answer any questions.

## Versions

chromadb 1.5.9 (the latest release on PyPI on 2026-10-30), `EphemeralClient` (local mode), Python 3.12.15, ubuntu-24.04 (GitHub-hosted runner)

## Relevant log output

Python's fault handler:

```
Fatal Python error: Segmentation fault
...
  File ".../chromadb/api/rust.py", line 582 in _query
  File ".../chromadb/api/models/Collection.py", line 265 in query
```
