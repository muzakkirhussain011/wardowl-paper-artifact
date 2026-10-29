# Draft upstream report: Redis Query Engine (RediSearch)

Status: draft, not filed. Confirm with the reproducer below on the version named before filing.
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

## Impact

Applications that filter on TAG values they do not control (identifiers, group names, hashes of
paths) silently miss documents, and a value equal to the first 4,096 bytes of another matches it. An
access-control filter built this way can admit a document granted to a different, longer name.

## Suggested resolution

Apply the same limit to query values (so both sides agree), or refuse a longer value at indexing with
an error, and document the limit on the tag fields page and in `FT.CREATE`.
