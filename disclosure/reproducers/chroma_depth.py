"""Reproducer of the first report in disclosure/chroma.md: a `$or` of about 1,000 operands fails with
"Expression tree is too large (maximum depth 1000)". chromadb only; no wardowl.

The draft's code, with a label on each printed line and the versions printed first. Exits 0 when
both queries ran (whether they answered or raised); the RESULT lines say which.
"""

import platform

import chromadb

print(f"chromadb {chromadb.__version__}, Python {platform.python_version()}, {platform.platform()}")

c = chromadb.EphemeralClient().create_collection("t", embedding_function=None)
c.add(ids=["a"], embeddings=[[0.1, 0.2]], metadatas=[{"g": 1, "g::i:1": True}])

flat = {"$or": [{"g": {"$eq": i}} for i in range(1001)]}
nested = {"$or": [{"$or": [{"g": {"$in": [i]}}, {f"g::i:{i}": {"$eq": True}}]} for i in range(1000)]}
for name, where in (("flat, 1,001 operands", flat), ("nested, 1,000 operands of 2", nested)):
    try:
        print(f"RESULT {name}: ids", c.query(query_embeddings=[[0.1, 0.2]], n_results=1, where=where)["ids"])
    except Exception as error:
        print(f"RESULT {name}: raised", type(error).__name__, error)
