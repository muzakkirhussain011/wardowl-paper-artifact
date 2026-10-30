#!/bin/sh
# Reproducer of disclosure/redis.md: TAG values longer than 4,096 bytes are cut at indexing but not
# in queries. redis-cli and a POSIX shell only; nothing else, and no wardowl.
#
# Part 1 is the draft's reproducer, command for command. Part 2 (added 2026-10-30, not in the draft)
# checks the boundary: a 4,096-byte value and a 4,097-byte value, each searched by its whole value.
#
# Needs a Redis with the Query Engine and no index named idx and no keys under doc:. REDIS_CLI says
# how to call redis-cli (default: redis-cli; the workflow uses the server container's own,
# "docker exec redis redis-cli"). The script exits 0 when every command ran, whatever they answered;
# the RESULT lines at the end say what they answered.
set -u

cli() { ${REDIS_CLI:-redis-cli} "$@" 2>&1; }
oneline() { printf '%s' "$1" | tr '\n' ' ' | sed 's/ *$//'; }
bytes() { printf '%*s' "$1" '' | tr ' ' "$2"; }

# ---- part 1: the draft's reproducer
long=$(printf '%*s' 5000 '' | tr ' ' a)     # 5,000 bytes
prefix=$(printf '%*s' 4096 '' | tr ' ' a)   # its first 4,096 bytes
echo "value lengths: long ${#long} bytes, prefix ${#prefix} bytes"
if [ "${#long}" -ne 5000 ] || [ "${#prefix}" -ne 4096 ]; then echo "harness: the shell built wrong values"; exit 2; fi

echo '$ redis-cli FT.CREATE idx ON HASH PREFIX 1 doc: SCHEMA t TAG'
cli FT.CREATE idx ON HASH PREFIX 1 doc: SCHEMA t TAG
echo '$ redis-cli HSET doc:long t "$long"'
cli HSET doc:long t "$long"
echo '$ redis-cli HSET doc:prefix t "$prefix"'
cli HSET doc:prefix t "$prefix"
echo '$ redis-cli FT.SEARCH idx "@t:{$long}" NOCONTENT DIALECT 2'
search_long=$(cli FT.SEARCH idx "@t:{$long}" NOCONTENT DIALECT 2)
echo "$search_long"
echo '$ redis-cli FT.SEARCH idx "@t:{$prefix}" NOCONTENT DIALECT 2'
search_prefix=$(cli FT.SEARCH idx "@t:{$prefix}" NOCONTENT DIALECT 2)
echo "$search_prefix"

# ---- part 2: the boundary (other letters, so these values share no prefix with part 1's)
b4096=$(bytes 4096 b)
c4097=$(bytes 4097 c)
echo "value lengths: b4096 ${#b4096} bytes, c4097 ${#c4097} bytes"
echo '$ redis-cli HSET doc:b4096 t "$b4096"'
cli HSET doc:b4096 t "$b4096"
echo '$ redis-cli HSET doc:c4097 t "$c4097"'
cli HSET doc:c4097 t "$c4097"
echo '$ redis-cli FT.SEARCH idx "@t:{$b4096}" NOCONTENT DIALECT 2'
search_b4096=$(cli FT.SEARCH idx "@t:{$b4096}" NOCONTENT DIALECT 2)
echo "$search_b4096"
echo '$ redis-cli FT.SEARCH idx "@t:{$c4097}" NOCONTENT DIALECT 2'
search_c4097=$(cli FT.SEARCH idx "@t:{$c4097}" NOCONTENT DIALECT 2)
echo "$search_c4097"

# ---- what the searches answered (count, then keys), and what the draft predicts
echo "RESULT search for the 5,000-byte value: $(oneline "$search_long")"
echo "RESULT search for its first 4,096 bytes: $(oneline "$search_prefix")"
echo "RESULT search for a 4,096-byte value (part 2): $(oneline "$search_b4096")"
echo "RESULT search for a 4,097-byte value (part 2): $(oneline "$search_c4097")"
l=$(oneline "$search_long"); p=$(oneline "$search_prefix")
case "$p" in
  "2 doc:long doc:prefix" | "2 doc:prefix doc:long") p_both=yes ;;
  *) p_both=no ;;
esac
if [ "$l" = "0" ] && [ "$p_both" = yes ]; then
  echo "RESULT verdict: reproduced (the whole value finds nothing; its first 4,096 bytes find both keys)"
elif [ "$l" = "1 doc:long" ] && [ "$p" = "1 doc:prefix" ]; then
  echo "RESULT verdict: not reproduced (each search finds only its own key)"
else
  echo "RESULT verdict: neither the draft's prediction nor its expected behaviour; see the output above"
fi
