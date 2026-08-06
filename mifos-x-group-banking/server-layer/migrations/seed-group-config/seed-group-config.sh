#!/usr/bin/env bash
# Seed the dt_group_config datatable (the loan-config the loan-apply screen reads) for every active
# group. This table was never populated by the create-group flow — create-group writes
# dt_group_type_config (the archetype config), while loan-apply reads dt_group_config (loan rules:
# contribution / multiplier / interest / fine / meeting cadence). Without a row, dt_group_config
# returns [] and the loan-apply form loads DEGRADED (zero max-loan). This copies each group's real
# values from dt_group_type_config into dt_group_config. dt_group_corpus is already seeded by
# seed-demo, so it is left alone.
#
# Idempotent: a group that already has a dt_group_config row is skipped.
#
# Usage:
#   FINERACT_BASE_URL=https://mifos-bank-2.mifos.community/fineract-provider/api/v1 \
#   FINERACT_USER=mifos FINERACT_PASSWORD=password FINERACT_TENANT=mifos-bank-2 \
#   bash seed-group-config.sh
#   bash seed-group-config.sh --dry-run
set -u
FINERACT_BASE_URL="${FINERACT_BASE_URL:-https://mifos-bank-2.mifos.community/fineract-provider/api/v1}"
FINERACT_USER="${FINERACT_USER:-mifos}"
FINERACT_PASSWORD="${FINERACT_PASSWORD:-password}"
FINERACT_TENANT="${FINERACT_TENANT:-mifos-bank-2}"
DRY_RUN=0; [[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

command -v curl >/dev/null || { echo "curl required" >&2; exit 3; }
command -v jq   >/dev/null || { echo "jq required" >&2; exit 3; }

fin() { # fin METHOD PATH [json-body]  — with a bounded retry to ride out mifos-bank-2 502 flaps
  local m="$1" p="$2" body="${3:-}" a out code
  for a in 1 2 3 4; do
    if [[ -n "$body" ]]; then
      out="$(curl -sS --max-time 45 -u "${FINERACT_USER}:${FINERACT_PASSWORD}" \
        -H "Fineract-Platform-TenantId: ${FINERACT_TENANT}" -H "Content-Type: application/json" \
        -X "$m" -d "$body" -w $'\n%{http_code}' "${FINERACT_BASE_URL}${p}" 2>/dev/null)"
    else
      out="$(curl -sS --max-time 45 -u "${FINERACT_USER}:${FINERACT_PASSWORD}" \
        -H "Fineract-Platform-TenantId: ${FINERACT_TENANT}" \
        -X "$m" -w $'\n%{http_code}' "${FINERACT_BASE_URL}${p}" 2>/dev/null)"
    fi
    code="${out##*$'\n'}"; body_out="${out%$'\n'*}"
    [[ "$code" == "50"* || "$code" == "000" ]] || { printf '%s' "$body_out"; return 0; }
    sleep 6
  done
  printf '%s' "$body_out"; return 0
}

# cycle window: 1 Jan → 31 Dec of the group's activation year, defaulting to a wide fixed window so we
# never depend on the wall clock (kept simple + deterministic for a seed).
CYCLE_START="2026-01-01"; CYCLE_END="2026-12-31"

echo ">> Fineract: ${FINERACT_BASE_URL}  tenant: ${FINERACT_TENANT}  (dry-run=${DRY_RUN})"
GROUPS_JSON="$(fin GET "/groups?limit=500")"
mapfile -t GIDS < <(printf '%s' "$GROUPS_JSON" | jq -r '.[]? | select(.active) | .id' 2>/dev/null)
echo ">> ${#GIDS[@]} active groups"

seeded=0; skipped=0; nocfg=0; failed=0
for gid in "${GIDS[@]}"; do
  existing="$(fin GET "/datatables/dt_group_config/${gid}" | jq 'length' 2>/dev/null)"
  if [[ "${existing:-0}" -gt 0 ]]; then
    skipped=$((skipped+1)); continue
  fi
  # source the real loan values from the group's dt_group_type_config
  tc="$(fin GET "/datatables/dt_group_type_config/${gid}" | jq -c 'if type=="array" then .[0] else . end' 2>/dev/null)"
  if [[ -z "$tc" || "$tc" == "null" ]]; then
    echo "  group ${gid}: no dt_group_type_config → skip (can't derive)"; nocfg=$((nocfg+1)); continue
  fi
  # Floor each value at a sensible VSLA default: type_config carries 0 for some older/test groups,
  # and a 0 contribution/multiplier yields a useless max-loan of 0. `// x` only covers null, so
  # explicitly bump non-positive values.
  body="$(printf '%s' "$tc" | jq -c \
    --arg cs "$CYCLE_START" --arg ce "$CYCLE_END" '
    def pos($v; $d): if (($v // 0) > 0) then $v else $d end;
    (pos(.contribution_amount; 100)) as $c |
    {
      cycle_number: 1,
      cycle_length_weeks: (pos(.cycle_length_months; 12) * 4),
      contribution_amount: $c,
      contribution_min: $c,
      contribution_max: ($c * 10),
      loan_multiplier: (pos(.loan_multiplier; 3)),
      interest_rate: (pos(.interest_rate; 2)),
      fine_amount: (pos(.fine_amount; 50)),
      meeting_frequency: "WEEKLY",
      cycle_start_date: $cs,
      cycle_end_date: $ce,
      locale: "en",
      dateFormat: "yyyy-MM-dd"
    }')"
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "  [dry-run] group ${gid}: POST dt_group_config $(printf '%s' "$body" | jq -c '{contribution_amount,loan_multiplier,interest_rate,fine_amount}')"
    continue
  fi
  resp="$(fin POST "/datatables/dt_group_config/${gid}" "$body")"
  if printf '%s' "$resp" | jq -e '.resourceId // .groupId' >/dev/null 2>&1; then
    echo "  group ${gid}: ✓ dt_group_config seeded ($(printf '%s' "$body" | jq -r '"mult="+(.loan_multiplier|tostring)+" rate="+(.interest_rate|tostring)'))"
    seeded=$((seeded+1))
  else
    echo "  group ${gid}: ✗ $(printf '%s' "$resp" | head -c 120)"; failed=$((failed+1))
  fi
done
echo ""
echo ">> done — seeded=$seeded skipped(existing)=$skipped no-type-config=$nocfg failed=$failed"
[[ "$failed" -eq 0 ]] && echo "✅ dt_group_config populated for all derivable active groups" || echo "⚠️ $failed group(s) failed — re-run (backend flap) or inspect"
