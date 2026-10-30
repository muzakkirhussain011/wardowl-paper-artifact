<!-- Send as documentation feedback on
     https://www.mongodb.com/docs/vector-search/indexes/vector-search-type/
     (the feedback control on the page), or as a support case if you have one. Feedback forms are
     short: if it will not take all of this, send the first two paragraphs and the reproducer.
     Note the date you sent it: this route gives no public link. -->

**A suggestion for this page: document the length limit of string values in `filter` fields of a vectorSearch index, and that a filter on the whole value does not match a truncated one.**

Thanks for these docs. I ran into a limit that I could not find on this page, and I wanted to pass it on. Please correct me if I have misread anything.

The `filter` field type cuts a string to its first 8,191 characters when it indexes it, and `$vectorSearch` looks the query value up whole. So a filter on a longer string does not find the document that holds it, and a filter on the string's first 8,191 characters does. For Atlas Search's `token` type the documentation says "If a string being indexed as a `token` field type exceeds 8181 characters, MongoDB Search truncates it to 8181 characters before indexing"; the vectorSearch index page lists the `filter` type's supported types but no length limit.

Reproducer (mongosh):

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
find(long);    // [] where [ { _id: "long" } ] is expected
find(prefix);  // both documents, where only [ { _id: "prefix" } ] is expected
```

Measured on `mongodb/mongodb-atlas-local:8.0.30` (`sha256:6d36b4421491ab115291361385c37484a3750ae46c9e35fdfe4123841979b044`) and `8.3.13` (`sha256:8c1cb7c4509d190aa1f1c007ba9debeef4ea1b8dcf1f8907ddd22399c3653929`), both with mongot `1.70.5-2-g607e7c6d48`. Whole-value search found every length tested up to 8,191 characters, and missed 8,192, 9,000 and 16,384. The 9,000-character document searched by its first k characters, for k from 8,182 to 8,192, was found only at k = 8,191. Strings of a two-byte character were found at 4,090 to 4,100 characters (8,180 to 8,200 bytes in UTF-8), so the limit does not count UTF-8 bytes; these runs do not tell characters from UTF-16 code units.

Strings this long are uncommon, so I don't expect this to affect most users. If it helps, one option would be to state the limit on the vectorSearch index page, and whether it counts characters or UTF-16 code units, and to either truncate filter values in queries the same way or reject longer strings, so that a filter never matches a document by a prefix of its value. You know this product far better than I do, so please take that only as a suggestion.

I came across this while testing for a research paper on permission-aware retrieval. The paper mentions this behavior, and I wanted you to hear about it first. If anything here is wrong, or if you would like the paper to describe it differently, please tell me and I will update it (Syed Muzakkir Hussain, github.com/muzakkirhussain011). I used an AI coding agent to help with the testing and this write-up; the results above come from real runs.
