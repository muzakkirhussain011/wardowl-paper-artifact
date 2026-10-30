#!/bin/sh
# Reproducer of disclosure/mongodb.md: string values in a vectorSearch index's `filter` fields over
# a length limit are not found by their whole value. mongosh only; nothing else, and no wardowl.
#
# Part 1 is the draft's reproducer. The draft leaves one step as a comment ("once
# db.c.getSearchIndexes("vi")[0].queryable is true"); here it is a loop that polls that field. The
# index creation is retried while mongot (the search process) is still starting; that changes
# nothing in what is created. Part 2 (added 2026-10-30, not in the draft) measures the limit: one
# document per length, each searched by its whole value, in a second collection with its own index.
#
# Needs a MongoDB Atlas Local deployment (mongod and mongot) whose test database has no collections
# c and d. MONGOSH says how to call mongosh (default: mongosh); MONGODB_URI where to connect. The
# script exits 0 when every step ran, whatever the searches answered; the RESULT lines say what
# they answered.
set -u

script="${TMPDIR:-/tmp}/mongodb-reproducer.$$.js"
cat > "$script" <<'EOF'
print(`mongosh ${version()}, server ${db.version()}, database ${db.getName()}`);

function retry(label, f) {
  const start = Date.now();
  for (;;) {
    try { return f(); }
    catch (e) {
      if (Date.now() - start > 180000) throw e;
      print(`${label}: ${e.message}; retrying in 2 s`);
      sleep(2000);
    }
  }
}
function waitQueryable(coll, name) {
  const start = Date.now();
  for (;;) {
    const ix = coll.getSearchIndexes(name);
    if (ix.length && ix[0].queryable === true) {
      print(`index ${name}: queryable after ${Math.round((Date.now() - start) / 1000)} s, status ${ix[0].status}`);
      return;
    }
    if (Date.now() - start > 600000) throw new Error(`index ${name} not queryable after 600 s: ${EJSON.stringify(ix)}`);
    sleep(2000);
  }
}
function ids(label, f) {
  try {
    const found = f().map((d) => d._id);
    print(`RESULT ${label}: ${JSON.stringify(found)}`);
    return found;
  } catch (e) {
    print(`RESULT ${label}: error ${e.codeName || e.name}: ${e.message}`);
    return null;
  }
}

// ---- part 1: the draft's reproducer
const long = "a".repeat(9000), prefix = "a".repeat(8181);
db.c.insertMany([
  { _id: "long", v: [0.1, 0.2], t: [long] },
  { _id: "prefix", v: [0.1, 0.2], t: [prefix] },
]);
retry("createSearchIndex vi", () => db.c.createSearchIndex("vi", "vectorSearch", {
  fields: [
    { type: "vector", path: "v", numDimensions: 2, similarity: "cosine" },
    { type: "filter", path: "t" },
  ],
}));
// once db.c.getSearchIndexes("vi")[0].queryable is true:
waitQueryable(db.c, "vi");
const find = (value) => db.c.aggregate([
  { $vectorSearch: { index: "vi", path: "v", queryVector: [0.1, 0.2], exact: true, limit: 10,
                     filter: { t: { $in: [value] } } } },
  { $project: { _id: 1 } },
]).toArray();
const l = ids("find(long), the 9,000-character value", () => find(long));       // expected [ { _id: "long" } ]
const p = ids("find(prefix), its first 8,181 characters", () => find(prefix));  // expected [ { _id: "prefix" } ]

const same = (a, b) => a !== null && JSON.stringify([...a].sort()) === JSON.stringify([...b].sort());
if (same(l, []) && same(p, ["long", "prefix"])) {
  print("RESULT verdict: reproduced (the whole value finds nothing; its first 8,181 characters find both documents)");
} else if (same(l, ["long"]) && same(p, ["prefix"])) {
  print("RESULT verdict: not reproduced (each search finds only its own document)");
} else {
  print("RESULT verdict: neither the draft's prediction nor its expected behaviour; see the lines above");
}

// ---- part 2: the limit. One letter per length, so no value is a prefix of another.
const lengths = [2048, 4096, 4097, 6000, 8000, 8181, 8182, 8192, 9000, 16384];
const docs = [];
for (let i = 0; i < lengths.length; i++) {
  docs.push({ _id: `len${lengths[i]}`, v: [0.1, 0.2], t: [String.fromCharCode(98 + i).repeat(lengths[i])] });
}
db.d.insertMany(docs);
retry("createSearchIndex vd", () => db.d.createSearchIndex("vd", "vectorSearch", {
  fields: [
    { type: "vector", path: "v", numDimensions: 2, similarity: "cosine" },
    { type: "filter", path: "t" },
  ],
}));
waitQueryable(db.d, "vd");
for (let i = 0; i < docs.length; i++) {
  const value = docs[i].t[0];
  ids(`part 2, a ${lengths[i]}-character value searched whole`, () => db.d.aggregate([
    { $vectorSearch: { index: "vd", path: "v", queryVector: [0.1, 0.2], exact: true, limit: 20,
                       filter: { t: { $in: [value] } } } },
    { $project: { _id: 1 } },
  ]).toArray());
}
print("done");
EOF

${MONGOSH:-mongosh} --quiet "${MONGODB_URI:-mongodb://127.0.0.1:27017/?directConnection=true}" --file "$script"
status=$?
rm -f "$script"
exit "$status"
