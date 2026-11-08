# Reproducers, run 41007436602 (commit 8babaf354d91430bce3d4cb96419dc3b13517f95)

## cerbos (latest): ghcr.io/cerbos/cerbos:0.57.0

exit status 0, 1 s

    reproducer: cerbos
    version label: latest
    target: ghcr.io/cerbos/cerbos:0.57.0
    commit: 8babaf354d91430bce3d4cb96419dc3b13517f95
    run: 41007436602 attempt 1
    runner: ubuntu24 20261026.354.1, Linux 7.0.0-1017-azure x86_64
    started: 2026-10-30T05:15:56Z
    image digest: ghcr.io/cerbos/cerbos@sha256:e5e3b150b3cb0090975605254f255164567d67e233634199fb20972e3eaff300
    image id: sha256:4b39c844352d8b887e1d7406078a27b7fab075d80263f0ca1761995ecb0c13bc
    image labels: {"org.opencontainers.image.created":"2026-10-23T07:10:11Z","org.opencontainers.image.name":"cerbos","org.opencontainers.image.revision":"43125124efe4b50b83d894635fb2f691e980dc62","org.opencontainers.image.source":"https://github.com/cerbos/cerbos","org.opencontainers.image.version":"0.57.0"}
    server_info: {"version":"0.57.0","commit":"43125124efe4b50b83d894635fb2f691e980dc62","buildDate":"2026-10-23T07:10:11Z"}
    curl: curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.10

- check d1 (allowed_users "zoe"): EFFECT_DENY
- check d2 (allowed_users ["zoe"]): EFFECT_ALLOW
- plan kind: KIND_CONDITIONAL
- plan condition: {"expression":{"operator":"in","operands":[{"value":"zoe"},{"variable":"request.resource.attr.allowed_users"}]}}
- plan filterDebug: 
- verdict: reproduced (check denies d1, allows d2; the plan is a conditional 'in')

## cerbos (tested): ghcr.io/cerbos/cerbos:0.56.0

exit status 0, 0 s

    reproducer: cerbos
    version label: tested
    target: ghcr.io/cerbos/cerbos:0.56.0
    commit: 8babaf354d91430bce3d4cb96419dc3b13517f95
    run: 41007436602 attempt 1
    runner: ubuntu24 20261026.354.1, Linux 7.0.0-1017-azure x86_64
    started: 2026-10-30T05:15:54Z
    image digest: ghcr.io/cerbos/cerbos@sha256:540643bc67ba628011a150ad1d3370f285daa38995be5cd7a4be181da902bec1
    image id: sha256:9769be8555e0d7a5bf8da1d9b5bb6b64dfa7a8350a6a42d752e7dae7cbc6e584
    image labels: {"org.opencontainers.image.created":"2026-09-30T06:22:34Z","org.opencontainers.image.name":"cerbos","org.opencontainers.image.revision":"98604d71b79dafdc16ac57e4712fc435227e7c0f","org.opencontainers.image.source":"https://github.com/cerbos/cerbos","org.opencontainers.image.version":"0.56.0"}
    server_info: {"version":"0.56.0", "commit":"98604d71b79dafdc16ac57e4712fc435227e7c0f", "buildDate":"2026-09-30T06:22:34Z"}
    curl: curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.10

- check d1 (allowed_users "zoe"): EFFECT_DENY
- check d2 (allowed_users ["zoe"]): EFFECT_ALLOW
- plan kind: KIND_CONDITIONAL
- plan condition: {"expression":{"operator":"in","operands":[{"value":"zoe"},{"variable":"request.resource.attr.allowed_users"}]}}
- plan filterDebug: 
- verdict: reproduced (check denies d1, allows d2; the plan is a conditional 'in')

## chroma-crash (latest): chromadb==1.5.9

exit status 2, 4 s

    reproducer: chroma-crash
    version label: latest
    target: chromadb==1.5.9
    commit: 8babaf354d91430bce3d4cb96419dc3b13517f95
    run: 41007436602 attempt 1
    runner: ubuntu24 20261026.354.1, Linux 7.0.0-1017-azure x86_64
    started: 2026-10-30T05:16:18Z
    python: Python 3.12.15
    chromadb: Version: 1.5.9
    stack limit (ulimit -s): 16384

- 1001 clauses: ended without an outcome, exit status 1, 1.3 s
- 15500 clauses: ended without an outcome, exit status 1, 1.0 s
- 16500 clauses: ended without an outcome, exit status 1, 0.9 s
- 40000 clauses: ended without an outcome, exit status 1, 0.9 s
- fault handler (first crash): File "/home/runner/work/wardowl-paper/wardowl-paper/disclosure/reproducers/chroma_crash.py", line 115, in <module> | File "/home/runner/work/wardowl-paper/wardowl-paper/disclosure/reproducers/chroma_crash.py", line 34, in child | File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb/api/client.py", line 222, in create_collection | File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb/api/rust.py", line 244, in create_collection
- verdict: differs from the draft's expectation; see the sizes above

## chroma-crash (tested): chromadb==1.5.9

exit status 2, 4 s

    reproducer: chroma-crash
    version label: tested
    target: chromadb==1.5.9
    commit: 8babaf354d91430bce3d4cb96419dc3b13517f95
    run: 41007436602 attempt 1
    runner: ubuntu24 20261026.354.1, Linux 7.0.0-1017-azure x86_64
    started: 2026-10-30T05:16:16Z
    python: Python 3.12.15
    chromadb: Version: 1.5.9
    stack limit (ulimit -s): 16384

- 1001 clauses: ended without an outcome, exit status 1, 1.3 s
- 15500 clauses: ended without an outcome, exit status 1, 0.9 s
- 16500 clauses: ended without an outcome, exit status 1, 0.9 s
- 40000 clauses: ended without an outcome, exit status 1, 0.9 s
- fault handler (first crash): File "/home/runner/work/wardowl-paper/wardowl-paper/disclosure/reproducers/chroma_crash.py", line 115, in <module> | File "/home/runner/work/wardowl-paper/wardowl-paper/disclosure/reproducers/chroma_crash.py", line 34, in child | File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb/api/client.py", line 222, in create_collection | File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/site-packages/chromadb/api/rust.py", line 244, in create_collection
- verdict: differs from the draft's expectation; see the sizes above

## chroma-depth (latest): chromadb==1.5.9

exit status 1, 1 s

    reproducer: chroma-depth
    version label: latest
    target: chromadb==1.5.9
    commit: 8babaf354d91430bce3d4cb96419dc3b13517f95
    run: 41007436602 attempt 1
    runner: ubuntu24 20261026.354.1, Linux 7.0.0-1017-azure x86_64
    started: 2026-10-30T05:16:23Z
    python: Python 3.12.15
    chromadb: Version: 1.5.9
    stack limit (ulimit -s): 16384



## chroma-depth (tested): chromadb==1.5.9

exit status 1, 1 s

    reproducer: chroma-depth
    version label: tested
    target: chromadb==1.5.9
    commit: 8babaf354d91430bce3d4cb96419dc3b13517f95
    run: 41007436602 attempt 1
    runner: ubuntu24 20261026.354.1, Linux 7.0.0-1017-azure x86_64
    started: 2026-10-30T05:16:12Z
    python: Python 3.12.15
    chromadb: Version: 1.5.9
    stack limit (ulimit -s): 16384



## mongodb (latest): mongodb/mongodb-atlas-local:8.3.13

exit status 0, 6 s

    reproducer: mongodb
    version label: latest
    target: mongodb/mongodb-atlas-local:8.3.13
    commit: 8babaf354d91430bce3d4cb96419dc3b13517f95
    run: 41007436602 attempt 1
    runner: ubuntu24 20261026.354.1, Linux 7.0.0-1017-azure x86_64
    started: 2026-10-30T05:16:54Z
    image digest: mongodb/mongodb-atlas-local@sha256:8c1cb7c4509d190aa1f1c007ba9debeef4ea1b8dcf1f8907ddd22399c3653929
    image id: sha256:9d666c3fffd7581bb89719e90f5558a0ad8a531cd5101a8dd148f69bec457e1a
    image labels: {"architecture":"x86_64","build-date":"2026-10-29T05:53:50Z","com.redhat.component":"ubi9-minimal-container","com.redhat.license_terms":"https://www.redhat.com/en/about/red-hat-end-user-license-agreements#UBI","cpe":"cpe:/a:redhat:enterprise_linux:9::appstream","description":"Container configured with a single node replicaset instance of MongoDB and Atlas Search","distribution-scope":"public","io.buildah.version":"1.45.0","io.k8s.description":"The Universal Base Image Minimal is a stripped down image that uses microdnf as a package manager. This base image is freely redistributable, but Red Hat only supports Red Hat technologies through subscriptions for Red Hat products. This image is maintained by Red Hat and updated regularly.","io.k8s.display-name":"Red Hat Universal Base Image 9 Minimal","io.openshift.expose-services":"","io.openshift.tags":"minimal rhel9","maintainer":"support@mongodb.com","mongodb-atlas-local":"container","mongodb-type":"community","mongot-edition":"localDev","mongot-version":"1.70.5-2-g607e7c6d48","name":"MongoDB Atlas Local","org.opencontainers.image.created":"2026-10-29T05:53:50Z","org.opencontainers.image.revision":"9eac53daf60c61895dd274c7017f0605f411e146","release":"1793253163","summary":"MongoDB Atlas Local Container","url":"https://catalog.redhat.com/en/search?searchType=containers","vcs-ref":"9eac53daf60c61895dd274c7017f0605f411e146","vcs-type":"git","vendor":"MongoDB","version":"8.3.13"}
    mongosh: 2.14.1
    server: 8.3.13
    image env: ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/mongot","container=oci","TOOL=CONTAINER"]

- find(long), the 9,000-character value: []
- find(prefix), its first 8,181 characters: ["prefix"]
- verdict: neither the draft's prediction nor its expected behaviour; see the lines above
- part 2, a 2048-character value searched whole: ["len2048"]
- part 2, a 4096-character value searched whole: ["len4096"]
- part 2, a 4097-character value searched whole: ["len4097"]
- part 2, a 6000-character value searched whole: ["len6000"]
- part 2, a 8000-character value searched whole: ["len8000"]
- part 2, a 8181-character value searched whole: ["len8181"]
- part 2, a 8182-character value searched whole: ["len8182"]
- part 2, a 8192-character value searched whole: []
- part 2, a 9000-character value searched whole: []
- part 2, a 16384-character value searched whole: []

## mongodb (tested): mongodb/mongodb-atlas-local:8.0.30

exit status 0, 6 s

    reproducer: mongodb
    version label: tested
    target: mongodb/mongodb-atlas-local:8.0.30
    commit: 8babaf354d91430bce3d4cb96419dc3b13517f95
    run: 41007436602 attempt 1
    runner: ubuntu24 20261026.354.1, Linux 7.0.0-1017-azure x86_64
    started: 2026-10-30T05:16:55Z
    image digest: mongodb/mongodb-atlas-local@sha256:6d36b4421491ab115291361385c37484a3750ae46c9e35fdfe4123841979b044
    image id: sha256:f2432378f9951befd3e0e3bffe51384204ecdd1ce614d53a249662a23fdd959a
    image labels: {"architecture":"x86_64","build-date":"2026-10-29T05:53:50Z","com.redhat.component":"ubi9-minimal-container","com.redhat.license_terms":"https://www.redhat.com/en/about/red-hat-end-user-license-agreements#UBI","cpe":"cpe:/a:redhat:enterprise_linux:9::appstream","description":"Container configured with a single node replicaset instance of MongoDB and Atlas Search","distribution-scope":"public","io.buildah.version":"1.45.0","io.k8s.description":"The Universal Base Image Minimal is a stripped down image that uses microdnf as a package manager. This base image is freely redistributable, but Red Hat only supports Red Hat technologies through subscriptions for Red Hat products. This image is maintained by Red Hat and updated regularly.","io.k8s.display-name":"Red Hat Universal Base Image 9 Minimal","io.openshift.expose-services":"","io.openshift.tags":"minimal rhel9","maintainer":"support@mongodb.com","mongodb-atlas-local":"container","mongodb-type":"community","mongot-edition":"localDev","mongot-version":"1.70.5-2-g607e7c6d48","name":"MongoDB Atlas Local","org.opencontainers.image.created":"2026-10-29T05:53:50Z","org.opencontainers.image.revision":"9eac53daf60c61895dd274c7017f0605f411e146","release":"1793253163","summary":"MongoDB Atlas Local Container","url":"https://catalog.redhat.com/en/search?searchType=containers","vcs-ref":"9eac53daf60c61895dd274c7017f0605f411e146","vcs-type":"git","vendor":"MongoDB","version":"8.0.30"}
    mongosh: 2.14.1
    server: 8.0.30
    image env: ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/mongot","container=oci","TOOL=CONTAINER"]

- find(long), the 9,000-character value: []
- find(prefix), its first 8,181 characters: ["prefix"]
- verdict: neither the draft's prediction nor its expected behaviour; see the lines above
- part 2, a 2048-character value searched whole: ["len2048"]
- part 2, a 4096-character value searched whole: ["len4096"]
- part 2, a 4097-character value searched whole: ["len4097"]
- part 2, a 6000-character value searched whole: ["len6000"]
- part 2, a 8000-character value searched whole: ["len8000"]
- part 2, a 8181-character value searched whole: ["len8181"]
- part 2, a 8182-character value searched whole: ["len8182"]
- part 2, a 8192-character value searched whole: []
- part 2, a 9000-character value searched whole: []
- part 2, a 16384-character value searched whole: []

## redis (latest): redis:8.10.3-alpine

exit status 0, 1 s

    reproducer: redis
    version label: latest
    target: redis:8.10.3-alpine
    commit: 8babaf354d91430bce3d4cb96419dc3b13517f95
    run: 41007436602 attempt 1
    runner: ubuntu24 20261026.354.1, Linux 7.0.0-1017-azure x86_64
    started: 2026-10-30T05:15:53Z
    image digest: redis@sha256:21090af93f8324db2f0f0f4f38a7c60369d47d917e000c3423d89d2ae2883537
    image id: sha256:9722accf3e8eeaeb7cd74a86256d6a41b83deb44d508c2988c8e5776bfdb7694
    image labels: null
    redis-cli: redis-cli 8.10.3
    redis_version:8.10.3
    redis_git_sha1:00000000
    redis_build_id:defa938dbe2c41f
    modules:
    name timeseries ver 81001 path /usr/local/lib/redis/modules//redistimeseries.so args  name vectorset ver 1 path  args  name search ver 81001 path /usr/local/lib/redis/modules//redisearch.so args  name bf ver 81001 path /usr/local/lib/redis/modules//redisbloom.so args  name ReJSON ver 81000 path /usr/local/lib/redis/modules//rejson.so args  

- search for the 5,000-byte value: 0
- search for its first 4,096 bytes: 2 doc:long doc:prefix
- search for a 4,096-byte value (part 2): 1 doc:b4096
- search for a 4,097-byte value (part 2): 0
- verdict: reproduced (the whole value finds nothing; its first 4,096 bytes find both keys)

## redis (tested): redis:8.10.2-alpine

exit status 0, 0 s

    reproducer: redis
    version label: tested
    target: redis:8.10.2-alpine
    commit: 8babaf354d91430bce3d4cb96419dc3b13517f95
    run: 41007436602 attempt 1
    runner: ubuntu24 20261026.354.1, Linux 7.0.0-1017-azure x86_64
    started: 2026-10-30T05:15:55Z
    image digest: redis@sha256:9f8d2d789b9a1d1e3f283f979aa9cbf393373806472e1ccd460e2f9c869b833b
    image id: sha256:6cfed4c686145bcd5807ef3ac1d2bf3384503cb3da30b0d308b4f25eb50dc373
    image labels: null
    redis-cli: redis-cli 8.10.2
    redis_version:8.10.2
    redis_git_sha1:00000000
    redis_build_id:8d909ac7aa12fd40
    modules:
    name bf ver 81001 path /usr/local/lib/redis/modules//redisbloom.so args  name timeseries ver 81001 path /usr/local/lib/redis/modules//redistimeseries.so args  name search ver 81001 path /usr/local/lib/redis/modules//redisearch.so args  name vectorset ver 1 path  args  name ReJSON ver 81000 path /usr/local/lib/redis/modules//rejson.so args  

- search for the 5,000-byte value: 0
- search for its first 4,096 bytes: 2 doc:long doc:prefix
- search for a 4,096-byte value (part 2): 1 doc:b4096
- search for a 4,097-byte value (part 2): 0
- verdict: reproduced (the whole value finds nothing; its first 4,096 bytes find both keys)

## Jobs

- mongodb (tested): success
- chroma-depth (latest): failure (failed: The script ran to its end)
- redis (latest): success
- redis (tested): success
- chroma-crash (latest): failure (failed: The script ran to its end)
- chroma-crash (tested): failure (failed: The script ran to its end)
- chroma-depth (tested): failure (failed: The script ran to its end)
- mongodb (latest): success
- cerbos (latest): success
- cerbos (tested): success
- commit the results: running
