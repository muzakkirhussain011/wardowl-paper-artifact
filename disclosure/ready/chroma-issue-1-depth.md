<!-- File at https://github.com/chroma-core/chroma/issues/new?template=bug_report.yaml
     Title:
     [Bug]: A $or with about 1,000 operands fails with "Expression tree is too large (maximum depth 1000)"
     The form has three fields. Paste each section below into its field. -->

## What happened?

A `where` whose top level is `$or` over 1,001 simple conditions, or over 1,000 clauses that are each a `$or` of two simple conditions, raises `InternalError` (see the log output). The flat document is one level deep and the nested one two, so the depth SQLite refuses grows with the number of operands, not with the nesting of the `where` document.

In `rust/segment/src/sqlite_metadata.rs` (tag 1.5.9), `CompositeExpression::eval` starts from a bound `false` (or `true` for `$and`) and folds in each child with `Expr::expr(expr).or(child.eval())`, so a flat `$or` of n clauses becomes a left-deep chain of binary ORs n levels deep. The filter docs state no limit on the number of operands.

Reproducer:

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

Expected: `[['a']]` for both, or a documented limit on the number of operands.

Impact: a permission filter for a user in many groups, with one clause per group, fails whole. It fails closed, so this is an availability limit, not a wrong answer.

Suggested resolution: build n-ary `$and` and `$or` as one node rather than a chain, or document the limit in operands.

This came up in differential testing for a research paper on permission-aware retrieval, which will describe the behaviour and cite this issue.

## Versions

chromadb 1.5.9 (the latest release on PyPI on 2026-10-30), `EphemeralClient` (local mode), Python 3.12.15, ubuntu-24.04 (GitHub-hosted runner)

## Relevant log output

```
InternalError Error executing plan: Internal error: error returned from database: (code: 1) Expression tree is too large (maximum depth 1000)
```

The same line is printed for `flat` and for `nested`.
