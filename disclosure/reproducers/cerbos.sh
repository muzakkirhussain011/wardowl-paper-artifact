#!/bin/sh
# Reproducer of disclosure/cerbos.md: `in` on a non-list attribute makes the condition unsatisfied
# in CheckResources, while PlanResources answers with a plain `in` condition. curl only (jq, when
# present, only summarizes the answers); no wardowl.
#
# The two requests are the draft's, byte for byte. Needs a Cerbos PDP on localhost:3592 that loaded
# only cerbos-policies/document.yaml (the draft's policy). The script exits 0 when both requests
# were answered, whatever they answered; the RESULT lines say what they answered.
set -u

echo '$ curl -s localhost:3592/api/check/resources -d '\''{"requestId":"r", ... d1 "zoe", d2 ["zoe"] ...}'\'''
check=$(curl -s localhost:3592/api/check/resources -d '{"requestId":"r","principal":{"id":"zoe","roles":["user"]},
  "resources":[{"actions":["read"],"resource":{"kind":"document","id":"d1","attr":{"allowed_users":"zoe"}}},
               {"actions":["read"],"resource":{"kind":"document","id":"d2","attr":{"allowed_users":["zoe"]}}}]}')
check_status=$?
echo "$check"
echo '$ curl -s localhost:3592/api/plan/resources -d '\''{"requestId":"r","action":"read", ...}'\'''
plan=$(curl -s localhost:3592/api/plan/resources -d '{"requestId":"r","action":"read",
  "principal":{"id":"zoe","roles":["user"]},"resource":{"kind":"document"}}')
plan_status=$?
echo "$plan"

if [ "$check_status" -ne 0 ] || [ "$plan_status" -ne 0 ]; then
  echo "harness: curl exit status $check_status (check) and $plan_status (plan)"
  exit 2
fi

if command -v jq > /dev/null 2>&1; then
  d1=$(printf '%s' "$check" | jq -r '.results[]? | select(.resource.id == "d1") | .actions.read')
  d2=$(printf '%s' "$check" | jq -r '.results[]? | select(.resource.id == "d2") | .actions.read')
  kind=$(printf '%s' "$plan" | jq -r '.filter.kind // empty')
  debug=$(printf '%s' "$plan" | jq -r '.filterDebug // empty')
  op=$(printf '%s' "$plan" | jq -r '.filter.condition.expression.operator // empty')
  echo "RESULT check d1 (allowed_users \"zoe\"): $d1"
  echo "RESULT check d2 (allowed_users [\"zoe\"]): $d2"
  echo "RESULT plan kind: $kind"
  echo "RESULT plan condition: $(printf '%s' "$plan" | jq -c '.filter.condition // empty')"
  echo "RESULT plan filterDebug: $debug"
  if [ "$d1" = EFFECT_DENY ] && [ "$d2" = EFFECT_ALLOW ] && [ "$kind" = KIND_CONDITIONAL ] && [ "$op" = in ]; then
    echo "RESULT verdict: reproduced (check denies d1, allows d2; the plan is a conditional 'in')"
  else
    echo "RESULT verdict: differs from the draft; see the answers above"
  fi
fi
