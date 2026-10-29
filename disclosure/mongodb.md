# Draft upstream report: MongoDB Atlas Vector Search

Status: draft, not filed. Confirm with the reproducer below before filing; the 8,181 figure for the
`filter` type is inferred from our runs and from the documented `token` limit.
Where: MongoDB documentation feedback for the vector search index page
(https://www.mongodb.com/docs/vector-search/indexes/vector-search-type/), or a support case.

## Title

Document the length limit of string values in `filter` fields of a vectorSearch index, and that a
filter on the whole value does not match a truncated one

## Version

`mongodb/mongodb-atlas-local:8.0.30`.

## What is documented

For Atlas Search's `token` type: "If a string being indexed as a `token` field type exceeds 8181
characters, MongoDB Search truncates it to 8181 characters before indexing"
(https://www.mongodb.com/docs/search/indexes/field-types/token-type/). The vectorSearch index page
lists the `filter` type's supported types (strings and arrays of them) but no length limit.

## What we saw

`$vectorSearch` with `filter: {terms: {$in: [<string of more than 8,181 characters>]}}` did not
return documents holding that exact string in an indexed `filter` field; strings of up to about
4,100 characters were found. Run with `exact: true` and with `numCandidates` above the collection
size, so not an approximate-search miss.

## Reproducer (mongosh, no other client)

```js
const long = "a".repeat(9000), prefix = "a".repeat(8181);
db.c.insertMany([
  { _id: "long", v: [0.1, 0.2], t: [long] },
  { _id: "prefix", v: [0.1, 0.2], t: [prefix] },
]);
db.c.createSearchIndex("vi", "vectorSearch", {
  fields: [
    { type: "vector", path: "v", numDimensions: 2, similarity: "cosine" },
    { type: "filter", path: "t" },
  ],
});
// once db.c.getSearchIndexes("vi")[0].queryable is true:
const find = (value) => db.c.aggregate([
  { $vectorSearch: { index: "vi", path: "v", queryVector: [0.1, 0.2], exact: true, limit: 10,
                     filter: { t: { $in: [value] } } } },
  { $project: { _id: 1 } },
]).toArray();
find(long);    // expected [ { _id: "long" } ]
find(prefix);  // expected [ { _id: "prefix" } ]
```

If the `filter` type truncates as `token` does, the first call returns nothing and the second returns
both documents.

## Suggested resolution

State the limit on the vectorSearch index page (and whether it counts characters or UTF-16 code
units), and either truncate filter values in queries the same way or reject longer strings, so that a
filter never matches a document by a prefix of its value.
