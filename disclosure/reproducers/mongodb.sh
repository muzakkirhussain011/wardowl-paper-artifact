#!/bin/sh
# Reproducer of disclosure/mongodb.md: string values in a vectorSearch index's `filter` fields over
# a length limit are not found by their whole value. mongosh only; nothing else, and no wardowl.
#
# Part 1 is the draft's reproducer. The draft leaves one step as a comment ("once
# db.c.getSearchIndexes("vi")[0].queryable is true"); here it is a loop that polls that field. The
# index creation is retried while mongot (the search process) is still starting; that changes
# nothing in what is created. Part 2 (added 2026-10-30, not in the draft) measures the limit: one
# document per length, each searched by its whole value, in a second collection with its own index.
# Part 3 (added after the first run) narrows the limit to the character, asks whether a prefix of a
# long value finds it, and tells bytes from characters, in a third collection.
#
# Needs a MongoDB Atlas Local deployment (mongod and mongot) whose test database has no collections
# c, d and e. MONGOSH says how to call mongosh (default: mongosh); MONGODB_URI where to connect. The
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

// ---- part 3 (added after run 41007436602, where 8,182 characters were found and 8,192 were not,
// and part 1's 9,000-character document was not found by its first 8,181 characters).
// 3a: whole-value search at every length from 8,182 to 8,192 (one letter each, from l).
// 3b: part 1's 9,000-character document searched by its first k characters, k = 8,182 to 8,192:
//     if the index keeps a prefix of a long value, one k finds it.
// 3c: two-byte characters (U+00E8 to U+00EB, one each): whole-value search at 4,090, 4,095, 4,096
//     and 4,100 characters, which are 8,180, 8,190, 8,192 and 8,200 bytes in UTF-8, to tell a limit
//     in bytes from one in characters.
const fine = [];
for (let k = 8182; k <= 8192; k++) fine.push(k);
const docs3 = fine.map((k, i) => ({ _id: `ascii${k}`, v: [0.1, 0.2], t: [String.fromCharCode(108 + i).repeat(k)] }));
const wide = [4090, 4095, 4096, 4100];
for (let i = 0; i < wide.length; i++) {
  docs3.push({ _id: `utf8x2_${wide[i]}`, v: [0.1, 0.2], t: [String.fromCharCode(0xe8 + i).repeat(wide[i])] });
}
db.e.insertMany(docs3);
retry("createSearchIndex ve", () => db.e.createSearchIndex("ve", "vectorSearch", {
  fields: [
    { type: "vector", path: "v", numDimensions: 2, similarity: "cosine" },
    { type: "filter", path: "t" },
  ],
}));
waitQueryable(db.e, "ve");
const inE = (value) => db.e.aggregate([
  { $vectorSearch: { index: "ve", path: "v", queryVector: [0.1, 0.2], exact: true, limit: 20,
                     filter: { t: { $in: [value] } } } },
  { $project: { _id: 1 } },
]).toArray();
for (let i = 0; i < docs3.length; i++) {
  const value = docs3[i].t[0];
  ids(`part 3, ${docs3[i]._id} (${value.length} characters, ${Buffer.byteLength(value, "utf8")} UTF-8 bytes) searched whole`,
      () => inE(value));
}
for (let i = 0; i < fine.length; i++) {
  ids(`part 3, part 1's collection searched with the first ${fine[i]} characters of the 9,000-character value`,
      () => find("a".repeat(fine[i])));
}
print("done");
EOF

${MONGOSH:-mongosh} --quiet "${MONGODB_URI:-mongodb://127.0.0.1:27017/?directConnection=true}" --file "$script"
status=$?
rm -f "$script"
exit "$status"
