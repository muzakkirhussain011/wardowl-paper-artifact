<!-- File at https://github.com/chroma-core/chroma/issues/new?template=bug_report.yaml
     Title:
     [Bug]: A where $or of about 16,500 or more clauses crashes the embedded client process (SIGSEGV)
     The form has three fields. Paste each section below into its field. -->

## What happened?

A flat `$or` of about 16,500 or more `$eq` clauses on distinct boolean keys kills the client process with SIGSEGV on the first `query`, with no Python exception and no Rust panic message. Smaller filters get the expression-depth error instead, which is a separate report.

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

Under gdb, in an earlier run, the main thread received SIGSEGV in `chromadb_rust_bindings.abi3.so` with the stack about 16,500 frames deep, the innermost frames all returning to one address in that library, while the tokio and sqlx-sqlite worker threads were idle. So the main thread appears to run out of stack in one recursive function of the Rust bindings, before SQLite sees the query. The per-clause correspondence is inferred from the frame count, since the library has no symbols. A stack overflow depends on the stack size, so another limit would probably move the threshold; I did not test that.

Impact: a client-supplied filter can take down the host process. An application that builds `where` from a user's group memberships can be crashed by a user in enough groups. A single-node server may share the code path; I did not test that.

Suggested resolution: render n-ary `$and` and `$or` as a balanced tree, or with sea-query's `Cond::any()` and `Cond::all()`, and validate the size of a `where` with a clear error rather than letting native code overflow. A documented size limit for local mode would also help.

This came up in differential testing for a research paper on permission-aware retrieval, which will describe the behaviour and cite this issue.

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
