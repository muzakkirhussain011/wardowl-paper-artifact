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
