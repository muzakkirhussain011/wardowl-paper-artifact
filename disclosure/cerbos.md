# Draft upstream note: Cerbos (documentation suggestion, not a bug)

Status: filed 2026-10-30 as https://github.com/cerbos/cerbos/issues/3456, scoped to `in` on a string, with the text in
`disclosure/ready/cerbos-issue.md`. This file is the working draft and its evidence; `evidence/cerbos-extra.md` tests
`hasIntersection` and `==`. Reproduced on 2026-10-30 with the reproducer below, unchanged, on Cerbos 0.56.0
and 0.57.0 (the latest release that day), in workflow runs 41007436602, 41007779363 and
41008151303; see "Reproduced (2026-10-30)".
Where: https://github.com/cerbos/cerbos/issues (documentation), for
https://docs.cerbos.dev/cerbos/latest/policies/conditions and the query plan pages.

## Title

Docs: say that `in` and `hasIntersection` on a non-list attribute make the condition unsatisfied,
and what that means for query plan adapters

## Version

`ghcr.io/cerbos/cerbos:0.56.0`, default (non-strict) evaluation.

## What happens

With a rule condition `request.principal.id in request.resource.attr.allowed_users`:

- CheckResources for a resource whose `allowed_users` is the string `"zoe"` and a principal `zoe`
  answers `EFFECT_DENY`: `in` on a string is a CEL runtime error, and the conditions page says a
  runtime error makes the condition "not satisfied".
- PlanResources for the same principal answers `KIND_CONDITIONAL` with the condition
  `"zoe" in request.resource.attr.allowed_users`. Nothing in the plan says the attribute must be a
  list or map for it to hold. An adapter that maps it to a database operator matching a scalar as
  well as an array element (MongoDB's `{allowed_users: "zoe"}`, or Elasticsearch's `term` on a
  keyword field) admits rows that CheckResources denies. The same holds for `hasIntersection`, and
  for `==` on an attribute that holds a list in some rows.

The operators table describes `in` as "Membership in lists or maps" and `hasIntersection` as list
intersection; it does not say what happens on other types.

## Reproducer (curl against a PDP with the policy below, no other client)

```yaml
apiVersion: api.cerbos.dev/v1
resourcePolicy:
  version: default
  resource: document
  rules:
    - actions: ["read"]
      effect: EFFECT_ALLOW
      roles: ["*"]
      condition:
        match:
          expr: request.principal.id in request.resource.attr.allowed_users
```

```sh
curl -s localhost:3592/api/check/resources -d '{"requestId":"r","principal":{"id":"zoe","roles":["user"]},
  "resources":[{"actions":["read"],"resource":{"kind":"document","id":"d1","attr":{"allowed_users":"zoe"}}},
               {"actions":["read"],"resource":{"kind":"document","id":"d2","attr":{"allowed_users":["zoe"]}}}]}'
# d1 EFFECT_DENY, d2 EFFECT_ALLOW
curl -s localhost:3592/api/plan/resources -d '{"requestId":"r","action":"read",
  "principal":{"id":"zoe","roles":["user"]},"resource":{"kind":"document"}}'
# KIND_CONDITIONAL: "zoe" in request.resource.attr.allowed_users
```

## Reproduced (2026-10-30)

Script `disclosure/reproducers/cerbos.sh`: the two curl requests above, byte for byte, against a
PDP started from the image with the policy above as its only policy
(`disclosure/reproducers/cerbos-policies/document.yaml`, mounted at `/policies`) and the image's
default configuration. Workflow `.github/workflows/reproducers.yml`, GitHub-hosted ubuntu-24.04
runners, runs 41007436602, 41007779363 and 41008151303; outputs on branch `results/reproducers`
under `runs/<run id>/cerbos-tested/` and `cerbos-latest/`.

| Image | Digest | `/api/server_info` |
|---|---|---|
| `ghcr.io/cerbos/cerbos:0.56.0` (the version tested) | `sha256:540643bc67ba628011a150ad1d3370f285daa38995be5cd7a4be181da902bec1` | 0.56.0, commit `98604d71`, built 2026-09-30 |
| `ghcr.io/cerbos/cerbos:0.57.0` (latest release, 2026-10-23) | `sha256:e5e3b150b3cb0090975605254f255164567d67e233634199fb20972e3eaff300` | 0.57.0, commit `43125124`, built 2026-10-23 |

Every run, both versions, the same answers:

- CheckResources: `d1` `EFFECT_DENY`, `d2` `EFFECT_ALLOW`.
- PlanResources: `"filter":{"kind":"KIND_CONDITIONAL","condition":{"expression":{"operator":"in",
  "operands":[{"value":"zoe"},{"variable":"request.resource.attr.allowed_users"}]}}}`.

Both as stated under "What happens"; the comment after the second request paraphrases this
`filter` object (the answers carried no `filterDebug` field). The plan request's singular `action`
field was accepted by both versions.

## Suggested resolution

One sentence on the conditions page that `in`, `hasIntersection` and the list functions make the
condition unsatisfied when the attribute is not a list (and that `in` on a map tests its keys), and
one on the query plan page that plan operators keep CEL's types, so adapters must not translate `in`
to an operator that also matches a scalar.

## Context

Found by wardowl's conformance kit (filter-and-check disagreement on chunks whose ACL fields hold a
string instead of a list). wardowl documents the same limit for its own plan translation; this note
is about Cerbos's documentation only.
