<!-- File at https://github.com/RediSearch/RediSearch/issues/new?template=bug_report.md
     Title:
     [BUG] TAG values longer than 4,096 bytes are cut at indexing but not in queries
     Paste everything below this comment as the body. -->

**Describe the bug**

Thanks for RediSearch. I noticed what looks like a mismatch in how long TAG values are handled, and I wanted to pass it on. Please correct me if I have misread the intended behavior.

A TAG value longer than 4,096 bytes is cut when it is indexed, while a query looks the value up as given. So for such a value:

1. `@field:{<whole value>}` does not find the document.
2. `@field:{<first 4,096 bytes of it>}` finds it, together with any document whose tag really is that shorter value.

`tokenizeTagString` copies each tag with `rm_strndup(tok, MIN(toklen, MAX_TAG_LEN))`, where `#define MAX_TAG_LEN 0x1000` ("Tags are limited to 4096 each"), in both the case-sensitive branch and the lowercase fallback (`src/tag_index.c`, lines 38-39 and 140-150 at commit `400ff19597dacab7676524130239bd0d9362ae88`). The [tag field documentation](https://redis.io/docs/latest/develop/ai/search-and-query/advanced-concepts/tags/) states no length limit.

**To Reproduce**

```sh
long=$(printf '%*s' 5000 '' | tr ' ' a)     # 5,000 bytes
prefix=$(printf '%*s' 4096 '' | tr ' ' a)   # its first 4,096 bytes
redis-cli FT.CREATE idx ON HASH PREFIX 1 doc: SCHEMA t TAG
redis-cli HSET doc:long t "$long"
redis-cli HSET doc:prefix t "$prefix"
redis-cli FT.SEARCH idx "@t:{$long}" NOCONTENT DIALECT 2
redis-cli FT.SEARCH idx "@t:{$prefix}" NOCONTENT DIALECT 2
```

Result, on both versions below, in every run: `FT.CREATE` answers `OK`, both `HSET` calls answer `1` (no error for the long value), the search for the 5,000-byte value answers `0`, and the search for its first 4,096 bytes answers `2`, `doc:long`, `doc:prefix`.

The boundary is exact: a 4,096-byte value is found by its whole value and a 4,097-byte value is not.

**Expected behavior**

The first search returns `doc:long` and the second returns `doc:prefix` only, or the index refuses the long value with an error.

**Environment**

- GitHub-hosted ubuntu-24.04 runners, commands sent with the image's own `redis-cli`
- `redis:8.10.2-alpine`, `sha256:9f8d2d789b9a1d1e3f283f979aa9cbf393373806472e1ccd460e2f9c869b833b` (`search` 81001)
- `redis:8.10.3-alpine`, `sha256:21090af93f8324db2f0f0f4f38a7c60369d47d917e000c3423d89d2ae2883537` (`search` 81001)

**Additional context**

Values this long are uncommon, so I don't expect this to affect most users. Where it does apply, in applications that filter on TAG values they do not control (identifiers, group names, hashes of paths), a document can be missed silently, and a value equal to the first 4,096 bytes of another matches it. An access-control filter built this way could admit a document granted to a different, longer name, which is why I thought it worth mentioning.

If it helps, one option would be to apply the same limit to query values, so that both sides agree, or to refuse a longer value at indexing with an error, and to document the limit on the tag fields page and in `FT.CREATE`. You know this code far better than I do, so please take that only as a suggestion.

I came across this while testing for a research paper on permission-aware retrieval. The paper mentions this behavior, and I wanted you to hear about it first. If anything here is wrong, or if you would like the paper to describe it differently or to mention a fix, please tell me and I will update it.

The commands and results above come from real runs, and I will follow this issue and answer any questions.
