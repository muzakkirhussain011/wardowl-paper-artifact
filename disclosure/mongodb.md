# Draft upstream report: MongoDB Atlas Vector Search

Status: draft, not filed. Reproduced on 2026-10-30 on Atlas Local 8.0.30 and 8.3.13 (the latest
release that day) in workflow runs 41007436602, 41007779363 and 41008151303, with one correction:
the `filter` type keeps 8,191 characters, not the 8,181 first inferred from the documented `token`
limit, so the reproducer's prefix is now 8,191 characters. See "Reproduced (2026-10-30)".
Where: MongoDB documentation feedback for the vector search index page
(https://www.mongodb.com/docs/vector-search/indexes/vector-search-type/), or a support case.

## Title

Document the length limit of string values in `filter` fields of a vectorSearch index, and that a
filter on the whole value does not match a truncated one

## Version

`mongodb/mongodb-atlas-local:8.0.30`; also `mongodb/mongodb-atlas-local:8.3.13`. Both images carry
mongot `1.70.5-2-g607e7c6d48`.

## What is documented

For Atlas Search's `token` type: "If a string being indexed as a `token` field type exceeds 8181
characters, MongoDB Search truncates it to 8181 characters before indexing"
(https://www.mongodb.com/docs/search/indexes/field-types/token-type/). The vectorSearch index page
lists the `filter` type's supported types (strings and arrays of them) but no length limit.

## What we saw

`$vectorSearch` with `filter: {terms: {$in: [<string of more than 8,181 characters>]}}` did not
return documents holding that exact string in an indexed `filter` field; strings of up to about
4,100 characters were found. Run with `exact: true` and with `numCandidates` above the collection
size, so not an approximate-search miss. (The reproducer later put the limit at 8,191 characters:
strings of 8,182 to 8,191 characters are found by their whole value.)

## Reproducer (mongosh, no other client)

```js
const long = "a".repeat(9000), prefix = "a".repeat(8191);
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

The `filter` type cuts a string to its first 8,191 characters when it indexes it and looks the
query value up whole, so the first call returns nothing and the second returns both documents
(see below).

Changed on 2026-10-30: `prefix` was `"a".repeat(8181)`, the `token` type's documented limit, and
the prediction read "If the `filter` type truncates as `token` does, the first call returns nothing
and the second returns both documents". Run as first written (runs 41007436602 and 41007779363), the
first call returned nothing but the second returned only `prefix`, because the `filter` type keeps
8,191 characters, not 8,181. Nothing else changed. In `disclosure/reproducers/mongodb.sh` the
"once ... queryable" comment is a loop that polls that field.

## Reproduced (2026-10-30)

Script `disclosure/reproducers/mongodb.sh`, mongosh 2.14.1 (npm) against the image's deployment on
port 27017, by `.github/workflows/reproducers.yml` on GitHub-hosted ubuntu-24.04 runners. Outputs
on branch `results/reproducers` under `runs/<run id>/mongodb-tested/` and `mongodb-latest/`.

| Image | Digest | Server | mongot |
|---|---|---|---|
| `mongodb/mongodb-atlas-local:8.0.30` (the version tested) | `sha256:6d36b4421491ab115291361385c37484a3750ae46c9e35fdfe4123841979b044` | 8.0.30 | 1.70.5-2-g607e7c6d48 |
| `mongodb/mongodb-atlas-local:8.3.13` (the registry's `latest` tag on 2026-10-30) | `sha256:8c1cb7c4509d190aa1f1c007ba9debeef4ea1b8dcf1f8907ddd22399c3653929` | 8.3.13 | 1.70.5-2-g607e7c6d48 |

The `8.0.30` tag was rebuilt on 2026-10-29 (image created 2026-10-29T05:53:50Z), so these runs used
a later build of 8.0.30 than the conformance campaign's run 1; that run's digest is in its job
summary, not in this repository.

Both versions answered the same in every run:

- The reproducer above (run 41008151303): `find(long)` `[]`; `find(prefix)` with the first 8,191
  characters `["long", "prefix"]`; the first 8,181 characters `[]`.
- As first written (runs 41007436602, 41007779363): `find(long)` `[]`; `find(prefix)` with 8,181
  characters `["prefix"]`.
- Whole-value search, one document per length (added to the script, not part of the reproducer):
  found at 2,048, 4,096, 4,097, 6,000, 8,000 and every length from 8,181 to 8,191 characters; not
  found at 8,192, 9,000 and 16,384.
- The 9,000-character document searched by its first k characters, k = 8,182 to 8,192: found only
  at k = 8,191.
- Strings of a two-byte character (U+00E8 to U+00EB) were found by their whole value at 4,090,
  4,095, 4,096 and 4,100 characters (8,180 to 8,200 bytes in UTF-8), so the limit does not count
  UTF-8 bytes. These characters are one UTF-16 code unit each, so the runs do not tell characters
  from UTF-16 code units.

## Suggested resolution

State the limit on the vectorSearch index page (8,191 characters for `filter` fields in these
runs, against 8,181 documented for the `token` type, and whether it counts characters or UTF-16
code units), and either truncate filter values in queries the same way or reject longer strings, so
that a filter never matches a document by a prefix of its value.
