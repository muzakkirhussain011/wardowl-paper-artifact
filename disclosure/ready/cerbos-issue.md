<!-- File at https://github.com/cerbos/cerbos/issues/new?template=feature.yaml
     Title:
     Docs: say that `in` on a string attribute makes the condition unsatisfied, while the query plan shows a plain `in`
     First tick "I have searched the existing issues". Paste each section below into its field.
     Checked 2026-10-30 against the current conditions page, the API page's query plan section, and the
     reproducer's output and server log in runs 41008151303. Scoped to `in` on a string because that is
     all the reproducer tests. The feature form is used because the bug form labels the issue kind/bug and
     this is not a bug. -->

## Feature description

Thanks for Cerbos. This is a documentation suggestion, not a bug: in the reproducer below, Cerbos does what its documentation says. The disagreement I met came from my own adapter's translator, and wardowl documents it.

The [conditions page](https://docs.cerbos.dev/cerbos/latest/policies/conditions) says a CEL runtime error "causes the condition to be treated as not satisfied", and that for `ALLOW` rules this "fails closed: the rule simply does not match". It describes `in` as "Membership in lists or maps" and does not say what happens on a value that is neither. The [query plan section](https://docs.cerbos.dev/cerbos/latest/api/index.html#resources-query-plan) lists `in` as "List membership (in)" and says nothing about types.

With a rule condition `request.principal.id in request.resource.attr.allowed_users`:

- CheckResources, for a principal `zoe` and a resource whose `allowed_users` is the string `"zoe"`, answers `EFFECT_DENY`, and the server logs `Error evaluating CEL expression` with `"error":"no such overload"`. When `allowed_users` is `["zoe"]` it answers `EFFECT_ALLOW`.
- PlanResources for the same principal answers `KIND_CONDITIONAL` with the operator `in` over `"zoe"` and `request.resource.attr.allowed_users`. Nothing in that answer says the attribute must be a list or map for the condition to hold.

My adapter mapped that `in` to an operator that matches a scalar as well as an array element, and in my tests that filter admitted documents that CheckResources denied.

## What would the ideal solution look like to you?

Perhaps one sentence on the conditions page that `in` on a string is a runtime error, so the condition is not satisfied, and one in the query plan section saying the same of the plan's `in`, so that an adapter does not translate it to an operator that also matches a scalar. You know your docs far better than I do, so please take this only as a suggestion.

## Anything else?

**Reproducer.** A PDP with this as its only policy:

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

**Tested on**, with the default configuration, and with the same answers on both:

- `ghcr.io/cerbos/cerbos:0.56.0`, `sha256:540643bc67ba628011a150ad1d3370f285daa38995be5cd7a4be181da902bec1`, commit `98604d71`
- `ghcr.io/cerbos/cerbos:0.57.0`, `sha256:e5e3b150b3cb0090975605254f255164567d67e233634199fb20972e3eaff300`, commit `43125124`

This reproducer covers `in` on a string only.

**Context.** Found by wardowl's conformance kit, as a disagreement between filter and check on chunks whose ACL fields hold a scalar instead of a list. wardowl documents this limit, and its re-check drops such a chunk and reports it as a violation. A research paper on permission-aware retrieval mentions this behavior, as a gap in my adapter and not as a fault of Cerbos. If anything here is wrong, or if you would like the paper to describe it differently, please tell me and I will update it.

AI disclosure: drafted with an AI coding agent; the output above comes from running the reproducer in CI on both versions.
