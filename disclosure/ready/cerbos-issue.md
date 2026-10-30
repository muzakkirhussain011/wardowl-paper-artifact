<!-- File at https://github.com/cerbos/cerbos/issues/new?template=bug.yaml
     Title:
     Docs: say that `in` and `hasIntersection` on a non-list attribute make the condition unsatisfied
     First tick "I have searched the existing issues", and do search them first: Cerbos does not
     engage with issues that skip its guidelines. Paste each section below into its field.
     The last line of "Anything else?" is the AI disclosure that Cerbos's guidelines ask of pull
     requests. Keep it, and change it if it does not describe what you did. -->

## Current Behavior

This is a documentation suggestion, not a bug: Cerbos behaves as CEL and its documentation say.

With a rule condition `request.principal.id in request.resource.attr.allowed_users`:

- CheckResources for a resource whose `allowed_users` is the string `"zoe"` and a principal `zoe` answers `EFFECT_DENY`: `in` on a string is a CEL runtime error, and the conditions page says a runtime error makes the condition "not satisfied".
- PlanResources for the same principal answers `KIND_CONDITIONAL` with the condition `"zoe" in request.resource.attr.allowed_users`. Nothing in the plan says that the attribute must be a list or map for it to hold. An adapter that maps it to a database operator matching a scalar as well as an array element (MongoDB's `{allowed_users: "zoe"}`, or Elasticsearch's `term` on a keyword field) admits rows that CheckResources denies. The same holds for `hasIntersection`, and for `==` on an attribute that holds a list in some rows.

The operators table describes `in` as "Membership in lists or maps" and `hasIntersection` as list intersection, and does not say what happens on other types.

## Expected Behavior

One sentence on the [conditions page](https://docs.cerbos.dev/cerbos/latest/policies/conditions) that `in`, `hasIntersection` and the list functions make the condition unsatisfied when the attribute is not a list (and that `in` on a map tests its keys), and one on the query plan page that plan operators keep CEL's types, so adapters must not translate `in` to an operator that also matches a scalar.

## Steps To Reproduce

A PDP with this as its only policy:

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
# "filter":{"kind":"KIND_CONDITIONAL","condition":{"expression":{"operator":"in",
#   "operands":[{"value":"zoe"},{"variable":"request.resource.attr.allowed_users"}]}}}
```

## Environment

- `ghcr.io/cerbos/cerbos:0.56.0`, `sha256:540643bc67ba628011a150ad1d3370f285daa38995be5cd7a4be181da902bec1`, commit `98604d71`
- `ghcr.io/cerbos/cerbos:0.57.0`, `sha256:e5e3b150b3cb0090975605254f255164567d67e233634199fb20972e3eaff300`, commit `43125124`
- Default configuration and default (non-strict) evaluation. Both versions gave the same answers.

## Anything else?

Found by wardowl's conformance kit, as a disagreement between filter and check on chunks whose ACL fields hold a string instead of a list. wardowl documents the same limit for its own plan translation; this note is about Cerbos's documentation only. A research paper on permission-aware retrieval will mention this behaviour and cite this issue.

AI disclosure: this report and its reproducer were drafted with an AI coding agent (Claude Code), and the reproducer's output above comes from running it in CI on both versions.
