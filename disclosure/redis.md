# Draft upstream report: Redis Query Engine (RediSearch)

Status: draft, not filed. Reproduced on 2026-10-30 with the reproducer below, unchanged, on Redis
8.10.2 and 8.10.3 (the latest release that day), in workflow runs 41007436602, 41007779363 and
41008151303; see "Reproduced (2026-10-30)".
Where: https://github.com/RediSearch/RediSearch/issues (bug), with a docs note for
https://redis.io/docs/latest/develop/ai/search-and-query/advanced-concepts/tags/.

## Title

TAG values longer than 4,096 bytes are cut at indexing but not in queries: the document is not
found by its value, and is found by the value's first 4,096 bytes

## Version

`redis:8.10.2-alpine` (Query Engine built in). The constant is on RediSearch master at
`400ff19597dacab7676524130239bd0d9362ae88`.

## What happens

`tokenizeTagString` copies each tag with `rm_strndup(tok, MIN(toklen, MAX_TAG_LEN))`, where
`#define MAX_TAG_LEN 0x1000` ("Tags are limited to 4096 each"), in both the case-sensitive branch and
the lowercase fallback (`src/tag_index.c`, lines 38-39 and 140-150 at the commit above). The query
side looks the value up as given. So for a value over 4,096 bytes:

1. `@field:{<whole value>}` does not find the document;
2. `@field:{<first 4,096 bytes of it>}` finds it, together with any document whose tag really is
   that shorter value.

The tag field documentation states no length limit.

## Reproducer (redis-cli and a POSIX shell, no client library)

```sh
long=$(printf '%*s' 5000 '' | tr ' ' a)     # 5,000 bytes
prefix=$(printf '%*s' 4096 '' | tr ' ' a)   # its first 4,096 bytes
redis-cli FT.CREATE idx ON HASH PREFIX 1 doc: SCHEMA t TAG
redis-cli HSET doc:long t "$long"
redis-cli HSET doc:prefix t "$prefix"
redis-cli FT.SEARCH idx "@t:{$long}" NOCONTENT DIALECT 2
redis-cli FT.SEARCH idx "@t:{$prefix}" NOCONTENT DIALECT 2
```

Expected: the first search returns `doc:long`, the second `doc:prefix` only (or the index refuses the
long value with an error). Seen in our conformance runs (through a client that hex-encodes values):
documents holding values over the limit were never returned by a search for their value; the
reproducer above also predicts the second search returns both keys.

## Reproduced (2026-10-30)

Script `disclosure/reproducers/redis.sh`: the commands above, unchanged, sent with the server
image's own redis-cli (`docker exec redis redis-cli ...`), by `.github/workflows/reproducers.yml` on
GitHub-hosted ubuntu-24.04 runners. Runs 41007436602, 41007779363 and 41008151303; each job's
output is on branch `results/reproducers` under `runs/<run id>/redis-tested/` and
`redis-latest/`.

| Image | Digest | `redis_version`, search module |
|---|---|---|
| `redis:8.10.2-alpine` (the version tested) | `sha256:9f8d2d789b9a1d1e3f283f979aa9cbf393373806472e1ccd460e2f9c869b833b` | 8.10.2, `search` 81001 |
| `redis:8.10.3-alpine` (latest release, GitHub release marked Latest) | `sha256:21090af93f8324db2f0f0f4f38a7c60369d47d917e000c3423d89d2ae2883537` | 8.10.3, `search` 81001 |

Every run, both versions: `FT.CREATE` answered `OK`; both `HSET` calls answered `1` (no error
for the long value); the search for the 5,000-byte value answered `0`; the search for its first
4,096 bytes answered `2`, `doc:long`, `doc:prefix`. So the second search returns both keys, as
predicted above.

The script also checks the boundary, which the reproducer above does not: a 4,096-byte value is
found by its whole value (`1`, `doc:b4096`) and a 4,097-byte value is not (`0`), so values are cut
when they are longer than 4,096 bytes. The source lines cited under "What happens" were not re-read
for these runs; the behaviour agrees with them.

## Impact

Applications that filter on TAG values they do not control (identifiers, group names, hashes of
paths) silently miss documents, and a value equal to the first 4,096 bytes of another matches it. An
access-control filter built this way can admit a document granted to a different, longer name.

## Suggested resolution

Apply the same limit to query values (so both sides agree), or refuse a longer value at indexing with
an error, and document the limit on the tag fields page and in `FT.CREATE`.
