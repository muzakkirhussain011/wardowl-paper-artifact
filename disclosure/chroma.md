# Draft upstream report: Chroma

Status: draft, not filed. Confirm with the reproducer below before filing; run 1 saw the error
through wardowl, whose filter had the shape of the second query.
Where: https://github.com/chroma-core/chroma/issues

## Title

A `$or` with about 1,000 operands, nested two levels deep, fails with "Expression tree is too large
(maximum depth 1000)"

## Version

`chromadb==1.5.9`, `EphemeralClient` (local mode).

## What happens

A `where` whose top level is `$or` over 1,000 clauses, each a `$or` of two simple conditions, raises
`InternalError: Expression tree is too large (maximum depth 1000)`. The document is two levels deep;
the limit seems to count operands as depth [unverified: inferred from the message]. The filter docs
state no limit on the number of operands.

## Reproducer (Python, chromadb only)

```python
import chromadb

c = chromadb.EphemeralClient().create_collection("t", embedding_function=None)
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

## Impact

Permission filters for users in many groups (one clause per group) fail whole. They fail closed, so
this is an availability limit, not a wrong answer.

## Suggested resolution

Build n-ary `$and`/`$or` as one node rather than a chain, or document the limit in operands.

---

# Second draft report (2026-10-30): a large `where` kills the embedded client process

Status: draft, not filed; Syed decides whether and where to file (a public issue or a private
security report, since an end user who belongs to many groups could trigger it through an
application). Source: X3 run 40940385704 (`evidence/x3-x6-run1.md`, "X3: Chroma, refusal and
crash"); the follow-up run under faulthandler will add the stack and the crash threshold.

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
   processes. 10,000 clauses gave the error of item 1 instead. The cause is not established; a
   stack overflow in native code (recursive rendering or dropping of a 40,000-deep expression tree)
   is the likeliest [unverified].

## Reproducer (Python, chromadb only; item 2 ends the interpreter)

```python
import chromadb

c = chromadb.EphemeralClient().create_collection("t", embedding_function=None)
c.add(ids=["a"], embeddings=[[1.0, 0.0, 0.0]], metadatas=[{"k0": True}])
where = {"$or": [{f"k{i}": {"$eq": True}} for i in range(40_000)]}
c.query(query_embeddings=[[1.0, 0.0, 0.0]], n_results=1, where=where)  # SIGSEGV
```

## Impact

A client-supplied filter can take down the host process. An application that builds `where` from a
user's group memberships can be crashed by any user in enough groups. A single-node server probably
shares the code path [not tested].

## Suggested resolution

Render n-ary `$and` and `$or` as a balanced tree (or with sea-query's `Cond::any()` /
`Cond::all()`), and validate the size of a `where` with a clear error rather than letting native
code overflow. Documenting a size limit for local mode would help users. wardowl now nests its
disjunctions and refuses to send a `where` beyond conservative bounds (PR #187).
