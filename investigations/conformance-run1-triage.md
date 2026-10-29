# Triage: conformance campaign run 1

Written 2026-10-29. Input: `D:\CV_2\wardowl-paper\evidence\conformance-campaign-run1.md` (workflow
run 40313285885, campaign commit `5d0f414`, wardowl 2.1.0), plus the public check-run annotations of
its engines, sql-and-kv and vector-dbs jobs (GitHub API, unauthenticated; the job logs and artifacts
need a signed-in account and were not read). Nothing was run locally; all execution is in GitHub
Actions.

Conventions:

- **wardowl references** are `file:line` at main `438a176`, which is byte-identical to run 1's
  library (`950a5cc`) for every file cited except `wardowl/testing.py`, where #166 added 9 lines
  above `check_authorizer` (checked with `git diff --stat 950a5cc 438a176`). "After" references are
  at `fix/engine-limits` `e7776f0`.
- **Engine references** are official docs or source at the version run where I could pin it.
- **[derived]** marks a number I computed from the kit's generators and run 1's published counts.
  **[unverified]** marks an inference I could not confirm from code, docs or data.
- Effects use the paper's fault-table legend (`paper/sections/conformance.tex:108-116`).

## 0. Summary

| # | Finding (run 1) | Root cause | Fault | Fix | Effect | Expected in run 2 |
|---|---|---|---|---|---|---|
| 1a | OpenFGA, OpenFGA-tenant: 119 of 140 runs each, `AuthorizationError: OpenFGA batch-check returned HTTP 400` | Requests beyond OpenFGA's API limits: more than 100 contextual tuples (one subject in five holds 300 or 1,000 groups), users over 512 bytes and group objects over 256 characters (`long-ids`) | wardowl adapter (sent what the API refuses, unclear error); the limits are documented | `59203e3`: `UnsupportedSubject` up front | Avail. | 0 errors; the same runs become `refused-ValueError`; 21 of 140 pass as before |
| 1b | SpiceDB 124/140, SpiceDB-tenant 117/140, `CheckBulkPermissions returned HTTP 400` | Subject ids (and with `group_subjects=True`, group names) outside SpiceDB's object id syntax: `zoë`, `zoë` (decomposed), `7.0`, Arabic-Indic and fullwidth digits, Kelvin sign, `ß`, `é`, 4,096-character ids | wardowl adapter (documented as "fails closed", but only after a 400); harness data outside the id alphabet | `59203e3`: `UnsupportedSubject` up front | Avail. | 0 errors; the same runs refused; 16 and 23 pass as before |
| 2 | Cerbos 20/20, Cerbos-tenant 19/20 `scalar-fields` runs: filter and check disagree | Plan translation maps CEL `in`, `hasIntersection` and `==` to `In`, which also matches a scalar where CEL needs a list (and matches a list by element where CEL compares whole). For those chunks the filter admits, Cerbos's check denies | Documented translation limit plus data shape (policy-authoring pitfall); not a Cerbos bug; the filter is the side that agrees with wardowl's reference | None in the library (documented); harness now shows each hit and the side the reference takes | Leak (re-check drops it; with `recheck=False` a false admit) | Same 39 runs; every disagreeing hit marked "the filter gives the reference answer" |
| 3 | Redis 26 runs, MongoDB 19 runs: `missed` in exact mode with long and huge strings; sound-only retry passes | The index cuts a long term short and the query names the whole term. RediSearch keeps 4,096 bytes of a TAG value; wardowl hex-encodes terms, so any field and value over 2,048 bytes. Atlas Search keeps 8,181 characters. Also lets a value equal to the kept prefix match the longer one | wardowl adapter (encoding into an index with a cap); Redis: undocumented cap, asymmetric index/query handling; MongoDB: cap documented for the token type only | `e7776f0`: SHA-256 digest for terms over the cap | Recall; Leak (prefix match, caught by the re-check) | long-strings and huge-strings pass on both |
| 4 | Keto 72/140, Casbin 43/140 runs: time budget | The kit's `check_authorizer` asks about every chunk three ways; `group_subjects=True` multiplies each question by the subject's groups (300 or 1,000 for some); Keto answers 10 tuples per HTTP request; pycasbin scans every policy row per request. About 0.8 and 2.1 minutes per run | Harness (budget sized for a shared job) | `182bcbc`: Keto in its own job, Casbin in two (seeds split), each with the job's 320 minutes | (none: every run started passed) | 140 of 140 runs each |
| 5 | Elasticsearch, OpenSearch (huge-strings 20 each), Milvus (long and huge 40), Chroma (wide-or, odd-fields 40), Qdrant (odd-fields 20): errors | Engine limits: Lucene's 32,766-byte term; Milvus's 1,024-character array element of wardowl's default schema and 65,536-byte JSON; Chroma's expression depth for a 1,000-clause `$or` and its metadata key rules; Qdrant's JSON path grammar for odd keys | Engine limits; every one fails closed (checked below) | None now; recommendations in section 5 | Avail. | Unchanged |
| H | Findings cut at 600 characters, hiding the disagreeing hit's metadata | Harness (`_log` annotation, `conformance_campaign.py` at `5d0f414`) | Harness | `182bcbc`: `findings/<target>.txt` with whole messages, briefs that name the hits' metadata | | Every finding readable in the artifact |

Commits: `fix/engine-limits` (from main `438a176`): `59203e3`, `e7776f0`, pushed. Campaign branch
`paper/conformance-campaign`: merge `10c6e93`, harness `182bcbc`, pushed 2026-10-29 15:50:07 UTC;
run 2 is workflow run 40905549149 (run number 2), created 15:50:08 UTC.

## 1. OpenFGA and SpiceDB: HTTP 400 on batch checks

### 1a. OpenFGA

**Mechanism.** `OpenFGAAuthorizer` sends the subject's groups as contextual tuples with every check
and list (`wardowl/authorizers/openfga.py:159-167`). OpenFGA's API refuses the whole request when:

- an item carries more than 100 contextual tuples: `ContextualTupleKeys.tuple_keys`
  `(validate.rules).repeated.max_items = 100`
  ([openfga/api, openfga/v1/openfga.proto](https://github.com/openfga/api/blob/main/openfga/v1/openfga.proto));
  the docs state it too: "There is currently a limit of 100 contextual tuples per request"
  ([Contextual tuples](https://openfga.dev/docs/interacting/contextual-tuples));
- a tuple's user is over 512 bytes (`TupleKey.user` `max_bytes: 512`; `CheckRequestTupleKey.user`
  `^[^\s]{2,512}$`; `ListObjectsRequest.user` `max_bytes: 512`), or a tuple's object is over 256
  characters (`TupleKey.object` `^[^\s]{2,256}$`)
  ([openfga_service.proto](https://github.com/openfga/api/blob/main/openfga/v1/openfga_service.proto));
- an id holds a control character (`tuple.IsValidObject` rejects `unicode.IsControl`,
  [openfga/openfga pkg/tuple/tuple.go](https://github.com/openfga/openfga/blob/main/pkg/tuple/tuple.go)).

wardowl checked only `:`, `#`, `*` and whitespace in user ids and groups
(`openfga.py:54`, `60-64`) and the length of resource objects (`openfga.py:169-175`), not the group
count, the user's byte length or the group object's length.

**Which variants trigger it.** The kit's `_subject` adds 300 groups to one subject in five
(`wardowl/testing.py:162-166`, `_MANY` at `testing.py:71`). Predicted subject pass rates against
run 1's figures [derived]:

| Variant | Cause | Predicted | Run 1 subjects passing |
|---|---|---|---|
| default | 20% of subjects have 303 groups | 80% | 198/240 (82.5%) |
| unicode-case | same | 80% | 129/160 (80.6%) |
| numeric-strings | same | 80% | 125/160 (78.1%) |
| many-groups | every subject has 1,000+ groups | 0% | 0/60 |
| many-hits | 20% with 303 groups (batches of 50 are within `OPENFGA_MAX_CHECKS_PER_BATCH_CHECK`) | 80% | 68/80 (85%) |
| long-ids | the above, users of 1,024 and 4,096 characters (over 512 bytes), groups of 256 to 4,096 characters (`group:` makes them over 256) | 22.9% | 48/160 (30%) |
| scalar-fields | 20% with 303 groups | 80% | 134/160 (83.8%) |

`openfga-tenant` has the same figures, as it should: the same subjects and the same contextual
groups. The long-ids excess (48 against about 37 expected) is 2.1 standard deviations [derived];
if run 2 shows fewer than 48 long-ids subjects passing, the 256-character group rule is stricter than
the server applies. Default also fails, so this is not only odd ids.

**Fault.** wardowl's adapter: it sent requests the API documents it will refuse, and reported them
as an opaque `AuthorizationError("OpenFGA batch-check returned HTTP 400")`. Retrieval failed closed
throughout (Avail.); nothing leaked.

**Fix (`59203e3`).** `UnsupportedSubject(AuthorizationError, ValueError)` (`wardowl/authz.py:44`,
after). `OpenFGAAuthorizer` raises it before sending for more than 100 contextual groups
(`openfga.py:186-199` after), a user over 512 bytes (`openfga.py:168-175`), a group object over
256 characters (`openfga.py:177-184`), and ids with control characters (`openfga.py:59`). It stays
an `AuthorizationError`, so retrieval and code that catches it are unchanged
(`retriever.py:514-515` re-raises it as is); it is a `ValueError`, so the campaign classifies it
as `refused-ValueError` (`conformance_campaign.py` `classify`). Chunking contextual groups over
several requests was rejected: OR-ing the answers is wrong for models with exclusion
(`but not`) or intersection. Tests: `tests/test_openfga.py` (refusals without a request, the
exact boundaries 512 bytes and 256 characters, 100 groups sent and 101 refused,
`contextual_groups=False` unlimited, retrieval failing closed). Docs: `docs/integrations/openfga.md`.

### 1b. SpiceDB

**Mechanism.** SpiceDB object ids must match `^(([a-zA-Z0-9/_|\-=+]{1,})|\*)$` with
`max_bytes: 1024` (`ObjectReference.object_id`,
[authzed/api core.proto:106-115 at 20a9897](https://github.com/authzed/api/blob/20a9897fdbcad3bc4a7cd8746c45cef7b124c1e8/authzed/api/v1/core.proto#L106-L115)).
wardowl already denied resource ids outside it without sending them (`spicedb.py:156-160`), but sent
the subject id and, with `group_subjects=True`, every group name as they were
(`spicedb.py:139-146`), so one bad id made SpiceDB refuse the whole CheckBulkPermissions request.
Its docstring said so ("a subject id or group name that is not one makes requests fail, closed",
`spicedb.py:31`). Batch size is not a cause: 100 items per request (`spicedb.py:97`), and
many-hits fails at the same rate as the id rule predicts.

Predicted against run 1 [derived]. Non-tenant checks groups as subject sets; tenant does not:

| Variant | Ids outside the syntax | Predicted (non-tenant / tenant) | Run 1 (non-tenant / tenant) |
|---|---|---|---|
| default | users `zoë`, `zoë` decomposed (2 of 7) | 71% / 71% | 165/240 / 165/240 |
| unicode-case | 5 of 11 users; 4 of 11 groups | 30% / 55% | 41/160 / 84/160 |
| numeric-strings | `7.0`, Arabic-Indic 7; groups `1.0`, Arabic-Indic and fullwidth 1 | 32% / 60% | 52/160 / 93/160 |
| many-groups | users as default (decoy groups are valid) | 71% / 71% | 35/60 / 35/60 |
| many-hits | users as default | 71% / 71% | 56/80 / 56/80 |
| long-ids | user and group of 4,096 characters | 67% / 86% | 122/160 / 143/160 |
| scalar-fields | users as default | 71% / 71% | 118/160 / 118/160 |

**Fault.** wardowl's adapter for the opaque, late failure (behaviour was fail-closed and
documented); the harness, for feeding service-backed engines the kit's in-process pools, which the
kit's own docstring says not to do for a service ("pass subjects and hits from your test data",
`testing.py:538-539`). The campaign keeps doing so on purpose, as a stress variant.

**Fix (`59203e3`).** `SpiceDBAuthorizer._subjects` checks the subject id and, when sent, each group
with the same rule and raises `UnsupportedSubject` before any request (`spicedb.py:65-71`,
`150-163` after); `check` computes the subjects once, up front (`spicedb.py:183`). Tests:
`tests/test_spicedb.py` (the kit's ids, `*`, 1,025 characters, groups only when sent).

**Expected in run 2.** No engine errors for the four targets; runs that failed become
`refused-ValueError` and the pass counts stay 21, 21, 16 and 23. Any remaining error is a new
finding (for example a subject that passes these checks and still gets a 400).

## 2. Cerbos: filter and check disagree on scalar ACL fields

**What the data shows.** The one visible case (seed 2): subject `zoë`, groups `['legal']`; filter
`Or(In(allowed_users, [zoë]), In(allowed_groups, ["*"]), In(allowed_groups, [legal]))`; hit `doc-000`
`{"allowed_groups": 1, "allowed_users": "zoë"}`. The other annotations show the same filter shape and
documents whose ACL fields are strings, integers, `true`, `null`, objects and nested or mixed lists.

**Reference semantics.** `matches(In(F, values), metadata)` is true for a scalar string or integer
equal to a value, and for a list holding one (`wardowl/filters.py:82-88`); `MetadataACLAuthorizer`
uses exactly that (`authz.py:78-88`). For `doc-000`: `In(allowed_users, [zoë])` matches the scalar
`"zoë"`, so the reference allows. The filter, translated from Cerbos's plan, allows. Cerbos's check
denies.

**Why Cerbos denies.** The policies say `request.principal.id in request.resource.attr.allowed_users`,
`"*" in request.resource.attr.allowed_groups` and `hasIntersection(...)`
(`examples/cerbos/policies/document.yaml:22-24`; tenant policy
`acceptance/policies/cerbos/document.yaml:24-29`, with `tenant == ...`). CEL's `in` is defined for
lists and maps only, and Cerbos documents `in` as "Membership in lists or maps" and
`hasIntersection` as list intersection; on a string it is a runtime error, and "a CEL runtime error
during condition evaluation causes the condition to be treated as not satisfied"
([Cerbos conditions](https://docs.cerbos.dev/cerbos/latest/policies/conditions)), so the ALLOW rule
does not match (fails closed; strict evaluation, off by default in 0.55, denies outright,
[0.55 release post](https://cerbos.dev/blog/cerbos-pdp-v0-55-0-strict-evaluation-mode-multiple-jwts-faster-conditions)).
For the tenant policy, `tenant == "acme"` against `["acme"]` is false in CEL, while `In` matches the
list by element.

**Why the filter allows.** `plan_to_filter` maps `"v" in request.resource.attr.F` to `In(F, [v])`,
`F in [...]` and `F == v` to `In(F, ...)`, and `hasIntersection` to `In`
(`wardowl/authorizers/cerbos.py:91-98`). `In` cannot say "only if F is a list", so the translation
is exact only when each field has the shape the policy assumes. This is documented
(`cerbos.py:24-30`; `docs/integrations/cerbos.md:78-85`), with the consequence: the re-check drops
such chunks and counts them in `violations`; with `recheck=False` they are returned.

**Which side is wrong.** Relative to wardowl's reference semantics, the filter is right and Cerbos's
check is the one that differs. Relative to the policy as written (CEL), the check is right and the
filter over-approximates. Since the policy is the authority, the pushed-down filter is the inexact
side, and it errs towards admitting. Every disagreeing hit expected in run 2 is
filter-admits/check-denies, with the reference agreeing with the filter [derived from the generator:
string, integer, `true`, `null`, object, nested and mixed-list shapes, and tenant `[t]`; none makes
CEL admit what `In` refuses]. One shape could go the other way and is not generated: `"x" in {...}`
tests a map's keys in CEL, so a principal id equal to a key of an object-valued field would be
admitted by Cerbos and refused by the filter [unverified, not exercised: the variant's objects have
the key `id` only].

**Fault.** Policy-authoring pitfall with documented translation limit, caught by the kit. Not a
wardowl bug (behaviour and consequence documented), not a Cerbos bug (CEL and Cerbos behave as
documented). Security held: every such hit fails the default re-check.

**Fix.** None in the library. Two options for later, not done now so that run 2 stays comparable:
(a) a policy that agrees with `In` on every shape, for example
`request.principal.id in request.resource.attr.allowed_users || request.resource.attr.allowed_users == request.principal.id`
and `hasIntersection(F, groups) || F in groups` (CEL's `||` absorbs the error from the first operand
when the second is true; untested, and strict evaluation mode may deny instead [unverified]); or
(b) document the map-key case beside the existing note. The draft upstream note
(`disclosure/cerbos.md`) is a documentation suggestion only.

**Harness change (`182bcbc`).** For every subject with this disagreement, the record now lists each
disagreeing hit with its metadata, the filter's and check's answers, the reference answer
(`matches` on the target's rule: metadata ACL with `"*"`, or for tenant profiles tenant and sharing
without `"*"`), and which side gives it; the summary counts hits by side.

**Expected in run 2.** The same 20 and 19 runs (the data is deterministic per seed and nothing in
the path changed), with `reference_side` all `filter`.

## 3. Redis and MongoDB: matching documents missed with long values

**Redis mechanism.** wardowl writes every permission term into one TAG field as hex
(`wardowl/backends/redis.py:49-50`, `204`, `221`; `SEPARATOR ","`, case-insensitive, `redis.py:124`)
and queries `@wardowl_terms:{<hex> | ...}` with the whole hex term (`redis.py:74`). RediSearch's tag
tokenizer copies each token with `rm_strndup(tok, MIN(toklen, MAX_TAG_LEN))` where
`#define MAX_TAG_LEN 0x1000` ("Tags are limited to 4096 each")
([src/tag_index.c:38-39, 140-150 at RediSearch master 400ff19](https://github.com/RediSearch/RediSearch/blob/400ff19597dacab7676524130239bd0d9362ae88/src/tag_index.c#L38-L150));
the lookup side passes the query value through unchanged (`TagIndex_OpenReader`, same file). A term
is `field \x1f s: value` (`wardowl/backends/_engines.py:29-30`), so any field and value over 2,048
UTF-8 bytes is stored cut and never found by its full value. The Redis tag field docs state no
such limit ([Tag fields](https://redis.io/docs/latest/develop/ai/search-and-query/advanced-concepts/tags/)).

Triggering values in the campaign: the 3,001-letter `é` string (6,001 bytes), users and groups of
4,096 characters, values of 8,192 characters, and every huge string. Not triggering: 256 and 1,024
characters, 64- and 256-character ids. Run 1's annotations match: long-strings seeds 0, 3 and 7
missed documents through the `é` string, seed 1 through a 4,096-character user (prefilter returned
0 of 2), and huge-strings through 32,766-character values.

**MongoDB mechanism.** wardowl stores raw terms in an array indexed as a `filter` field of the
vector search index (`wardowl/backends/mongodb.py:152-158` at main) and as `token` in the text index
(`mongodb.py:185`), and filters with `$in` over whole terms (`mongodb.py:80`, `106`). Atlas Search:
"If a string being indexed as a `token` field type exceeds 8181 characters, MongoDB Search truncates
it to 8181 characters before indexing"
([token type](https://www.mongodb.com/docs/search/indexes/field-types/token-type/)). The vector
search `filter` type documents no limit
([vectorSearch type](https://www.mongodb.com/docs/vector-search/indexes/vector-search-type/)); run 1
is consistent with the same 8,181 limit [unverified directly]: MongoDB missed with 8,192-character
values (long-strings, 3 runs, all after `set_metadata`) and huge strings (16 runs), and never with the
3,001-character `é` string or 4,096-character ids that Redis missed (no retrieval misses at all).

**The prefix match.** Because only the stored side is cut, a filter value equal to the kept prefix
of a longer value (2,031 ASCII characters for `allowed_groups` in Redis; 8,164 in MongoDB) matches
the chunk holding the longer one. The retriever's re-check, which reads the chunk's exact metadata,
drops it (Leak in the legend). Not observed in run 1 (the generator has no such pairs) [derived].

**Fault.** wardowl's adapters: they promise exact filters and encode values into an index with a
cap. Upstream: Redis has an undocumented cap applied at index time only; MongoDB documents the cap
for `token` but not for the vector search `filter` type.

**Fix (`e7776f0`).** `digest(term)` in `wardowl/backends/_engines.py:28-39` (after): `\x1fsha256:`
plus the SHA-256 hex, which no term can equal (terms start with a non-empty field name). Redis
stores and queries `hex(digest)` when a term's hex would exceed 4,096 bytes
(`redis.py:46-58` after); MongoDB uses the digest for terms over 8,181 UTF-16 code units
(`mongodb.py:61-79` after, applied in both translators, `add`, `set_metadata` and
`permission_terms`). Terms within the caps are unchanged, so existing indexes keep working. Unit
tests and live tests at the exact boundaries (`tests/test_redis_vector.py`,
`tests/test_mongodb.py`); the live MongoDB test also checks that an 8,181-character term is
indexed whole, which will confirm or refute the 8,181 figure for the `filter` type in CI.

**Expected in run 2.** Redis and MongoDB pass long-strings and huge-strings (no `missed`, no
sound-only retries). Residual MongoDB misses would mean the filter type's cap is below 8,181
characters.

## 4. Keto and Casbin: time budget

**Why they are slow.** Per subject, `check_authorizer` checks all hits, then each hit alone, then all
reversed (`wardowl/testing.py:561-565`): about 3 × hits questions per subject. With
`group_subjects=True` each question is asked for the user and each group: Keto sends one tuple per
(chunk, subject) and 10 tuples per HTTP request (`wardowl/authorizers/keto.py:55`, `105-131`, Keto's
default `limit.max_batch_check_size`); Casbin makes one `enforce` per (chunk, subject)
(`wardowl/authorizers/casbin.py:80-94`, `96-115`), and pycasbin's `enforce` evaluates the matcher
against every policy row until one allows, so a denial scans them all, and `batch_enforce` is a loop
([pycasbin v1.43.0 casbin/core_enforcer.py:442-485, 526-532](https://github.com/casbin/pycasbin/blob/v1.43.0/casbin/core_enforcer.py#L442-L532)).
One subject in five has 303 groups and many-groups subjects 1,000 or more, so for example one
many-hits subject with 303 groups is about 300 × 304 × 3 ≈ 274,000 Casbin requests over about 400
policy rows [derived]. Casbin-tenant uses a custom request without group fan-out and finished all
140 runs.

**Timing [derived from the job's 174-minute step and the 320-minute fair-share rule in
`_deadline`].** Casbin ran to the 90-minute cap (a fair share below 90 would have pushed the step
past 230 minutes); Keto had about 60 minutes (a fifth of what was left when it started, about 19
minutes in). So about 0.8 minutes per Keto run and 2.1 per Casbin run: about 2 and 5 hours for 140.

**Fault.** Harness: budgets sized for a shared job. Not an adapter inefficiency worth changing for
the campaign; both adapters do what their documentation says. A small library improvement noted for
later: Keto and Casbin ask about a resource shared by several chunks once per chunk (OpenFGA and
SpiceDB deduplicate), which costs nothing in the campaign, where every chunk is its own document.

**Fix (`182bcbc`).** Keto runs in job `engines-keto`, Casbin in `engines-casbin-1` (seeds 0-9) and
`engines-casbin-2` (seeds 10-19), each target given the job's whole 320 minutes; the summary merges
a target's parts into one row (`_merge_start`, `_merge_end`). Per-call limits, data and everything
else are unchanged.

**Expected in run 2.** 140 of 140 runs each, all passing (every run started in run 1 passed).

## 5. Engine limits that surface as errors

All checked from code to return no partial result:

| Target, variant | Error in run 1 | Fails closed because | Recommendation |
|---|---|---|---|
| Elasticsearch, OpenSearch huge-strings | Bulk `document_parsing_exception` / `illegal_argument_exception` "immense term" over Lucene's 32,766 bytes; ES seed 2 a 400 on a query | `add` raises on any failed bulk item (`_engines.py:249-256`); a search error raises from the client; a 200 with failed shards or a timeout raises (`_engines.py:192`, `199-202`) | Apply the same digest to terms over 32,766 UTF-8 bytes in `EngineBackend` (small; would make huge values work). Not done now, to keep the change to the two silent cases |
| Milvus long and huge strings | Array element 8,199 over `max_length` 1,024; JSON 72,841 over 65,536 bytes | `upsert` raises (`milvus.py:233-239`); the collection's `max_term_length` defaults to 1,024 (`milvus.py:120`, `144`, documented at `127-129`) | Digest terms over the collection's element `max_length` (needs the schema read, or a constructor parameter); refuse metadata whose JSON exceeds 65,536 bytes with `ValueError` naming the limit |
| Chroma wide-or | `InternalError`, "Expression tree is too large (maximum depth 1000)" for an `Or` of 1,000 one-value clauses | The query raises; and every hit is re-matched against the filter locally (`chroma.py:238-242`) | Merge an `Or` of `In`s on one field into one `In` in `_where` (exact, and removes the width); report the behaviour (draft `disclosure/chroma.md`) |
| Chroma odd-fields | `InvalidArgumentError`, "Invalid metadata at index 3" on `add` | `add` deletes then adds per batch (`chroma.py:187-191`), so a refused batch is absent, never stored wrong | Refuse up front, in `_encode_metadata`, the keys Chroma rejects, once its rule is pinned from its source [unverified which key] |
| Qdrant odd-fields | `UnexpectedResponse` 400 | The search raises | Qdrant's path grammar takes unquoted keys of letters, digits, `_` and `-` only, and quoted keys without `"` or `\` ([lib/segment/src/json_path/parse.rs at v1.19.2](https://github.com/qdrant/qdrant/blob/v1.19.2/lib/segment/src/json_path/parse.rs)); `_key` refuses only `.`, `[`, `]`, `"` (`qdrant.py:65`, `126-129`). Quote other keys (`metadata."team name"`) or refuse them with `ValueError`; needs a test in local mode, whose parser is separate |

None of these is a wrong answer. Each fails loudly at write or search time; a failed search raises
out of the retriever, so nothing is returned. The paper can report them as limits that fail closed.

## 6. What the paper's fault table can credit to the kit

Found by "Kit (campaign)", run 1, fixed or explained, run 2 to confirm:

| Store or engine | Fault or gap | Effect | Upstream | Fixed |
|---|---|---|---|---|
| Redis 8.10 | TAG values cut at 4,096 bytes at index time only: long permission values never matched, prefixes matched | Recall; Leak | Bug and doc gap, draft `disclosure/redis.md`; None (adapter) for wardowl's encoding | `e7776f0` |
| MongoDB Atlas Local 8.0 | Strings cut at 8,181 characters: long values never matched, prefixes matched | Recall; Leak | Doc gap for the vector search `filter` type, draft `disclosure/mongodb.md` | `e7776f0` |
| OpenFGA 1.22 | More than 100 contextual tuples, users over 512 bytes, objects over 256 characters refused whole | Avail. | None (adapter); limits documented | `59203e3` |
| SpiceDB 1.56 | Subject and group ids outside the object id syntax refused whole | Avail. | None (adapter); syntax documented | `59203e3` (clearer, earlier refusal) |
| Cerbos 0.56 | Plan translation broader than CEL for scalar or wrongly shaped ACL fields | Leak | None (documented semantic gap); doc suggestion drafted | Documented; not changed |

Plus five engine limits that fail closed (section 5), and two harness faults (budgets, cut findings).
The kit found no leak through the re-check and no wrong answer from a store in run 1.

## 7. Not done, and open questions

- The coordinator's mid-task message asked for a `feat/under-retrieval` branch; it had no spec in
  this task and the task limits work to two branches, so it was not touched.
- Artifacts and job logs of run 1 were not read (they need a signed-in account); the per-run
  durations and the 400 response bodies would confirm sections 1 and 4 directly. Run 2's
  `findings/` will hold the whole messages.
- Run 2 checks: OpenFGA long-ids subjects passing (48 in run 1; fewer means the group rule is too
  strict); MongoDB long-string misses (any means the filter type's cap is below 8,181); Cerbos
  `reference_side` (anything but `filter` is a new finding).
