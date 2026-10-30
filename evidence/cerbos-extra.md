# Cerbos: `hasIntersection` and `==` tested directly

Date: 2026-10-30. Workflow `.github/workflows/cerbos-extra.yml`, curl only, no wardowl, with the policies in
`disclosure/reproducers/cerbos-extra-policies/`. Raw answers, server logs and image digests are on the branch
`results/cerbos-extra`, and in the tag `evidence-v1` under `evidence/raw/results-cerbos-extra/`.

Why: the paper said Cerbos's check raises on a scalar for `in`, `==` and `hasIntersection`, but the reproducer in
`disclosure/reproducers/cerbos.sh` tests `in` only, and the other two rested on Cerbos's documentation and CEL.

The first run failed because the first policy file held two YAML documents and the server did not start (curl exit
status 7). That is an inference from the exit status, since that run's server log was not kept; with the two policies in
separate files the server started and the run below completed.

Principal `zoe` with `groups` `["eng"]` and `tenant` `"acme"`. Both versions gave the same answers.

| Condition | Attribute value | 0.56.0 | 0.57.0 | Server log |
|---|---|---|---|---|
| `hasIntersection(request.resource.attr.allowed_groups, request.principal.attr.groups)` | `"eng"` | EFFECT_DENY | EFFECT_DENY | `no such overload: hasIntersection(string, list)` |
| same | `["eng"]` | EFFECT_ALLOW | EFFECT_ALLOW | no error |
| `request.resource.attr.tenant == request.principal.attr.tenant` | `"acme"` | EFFECT_ALLOW | EFFECT_ALLOW | no error |
| same | `["acme"]` | EFFECT_DENY | EFFECT_DENY | no error |

PlanResources answered `KIND_CONDITIONAL` for both, with the operators `hasIntersection` and `eq`.

So `hasIntersection` on a string raises and denies, as `in` does, and `==` on a list denies without an error. The
paper's sentence that the check "raises on a scalar" was imprecise for `==` and was corrected in `conformance.tex`.
Cerbos issue #3456 stays scoped to `in`, as it was posted.
