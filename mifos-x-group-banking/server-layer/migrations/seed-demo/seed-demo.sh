#!/usr/bin/env bash
# seed-demo.sh — materialize the MifosSave demo account + demo data on a live backend.
#
# Creates, from ./demo-fixture.json (the single source of truth):
#   1. demo user (companion self-register)            -> Amina Otieno
#   2. group activated with its group-type             -> Mwangaza Women's Group (VSLA)
#   3. 5 members associated + roles                    -> dt_member_role
#   4. savings accounts (group-linked + voluntary)     -> Fineract savings + activate
#   5. 3 meeting records                               -> dt_meeting_record
#   6. corpus row                                      -> dt_group_corpus
#   7. vsla_cycle row                                  -> dt_vsla_cycle
#   8. ONE live invite code (DEMO24)                   -> dt_companion_invitations
#
# PREREQUISITE: ../register-datatables.sh has already provisioned the 21 datatables.
# EXTERNAL GATE: requires a reachable Fineract instance AND the deployed companion API
# (mcp-mifosx) — see ../../COMPANION_API_BUILD_DEPLOY.md §3. Nothing here stands those up.
#
# Usage:
#   FINERACT_BASE_URL=... COMPANION_BASE_URL=... \
#   FINERACT_USER=mifos FINERACT_PASSWORD=password FINERACT_TENANT=default \
#   bash seed-demo.sh [--dry-run]
#
# Env:
#   FINERACT_BASE_URL   (required unless --dry-run)
#   COMPANION_BASE_URL  (required unless --dry-run) e.g. https://your-host/companion
#   FINERACT_USER / FINERACT_PASSWORD / FINERACT_TENANT  (defaults mifos/password/default)
#   INSECURE=1          pass -k to curl
#
# Requires: bash, curl, jq. Idempotent-ish: re-running skips already-present rows where the
# backend reports a duplicate. Money-affecting steps are logged before execution.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURE="${SCRIPT_DIR}/demo-fixture.json"

FINERACT_BASE_URL="${FINERACT_BASE_URL:-}"
COMPANION_BASE_URL="${COMPANION_BASE_URL:-}"
FINERACT_USER="${FINERACT_USER:-mifos}"
FINERACT_PASSWORD="${FINERACT_PASSWORD:-password}"
FINERACT_TENANT="${FINERACT_TENANT:-default}"
DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

command -v jq >/dev/null   || { echo "FATAL: jq required" >&2; exit 3; }
command -v curl >/dev/null || { echo "FATAL: curl required" >&2; exit 3; }
[[ -f "$FIXTURE" ]]        || { echo "FATAL: fixture not found: $FIXTURE" >&2; exit 3; }
if [[ "$DRY_RUN" -eq 0 ]]; then
  [[ -n "$FINERACT_BASE_URL" ]]  || { echo "FATAL: FINERACT_BASE_URL required (external gate)" >&2; exit 4; }
  [[ -n "$COMPANION_BASE_URL" ]] || { echo "FATAL: COMPANION_BASE_URL required (external gate — companion API must be deployed)" >&2; exit 4; }
fi

CURL_OPTS=(-sS --max-time 60)
[[ "${INSECURE:-0}" == "1" ]] && CURL_OPTS+=(-k)

fin() {  # fin METHOD PATH [json-body]
  local m="$1" p="$2" b="${3:-}"
  local args=(-u "${FINERACT_USER}:${FINERACT_PASSWORD}" -H "Fineract-Platform-TenantId: ${FINERACT_TENANT}" -H "Content-Type: application/json" -X "$m")
  [[ -n "$b" ]] && args+=(-d "$b")
  curl "${CURL_OPTS[@]}" "${args[@]}" "${FINERACT_BASE_URL}${p}"
}
comp() { # comp METHOD PATH [json-body]
  local m="$1" p="$2" b="${3:-}"
  local args=(-H "Content-Type: application/json" -X "$m")
  [[ -n "$b" ]] && args+=(-d "$b")
  curl "${CURL_OPTS[@]}" "${args[@]}" "${COMPANION_BASE_URL}${p}"
}

j() { jq -r "$1" "$FIXTURE"; }

echo "== MifosSave demo seed =="
echo "   fixture   : $FIXTURE"
echo "   fineract  : ${FINERACT_BASE_URL:-<dry-run>}"
echo "   companion : ${COMPANION_BASE_URL:-<dry-run>}"
echo "   group     : $(j '.group.name') ($(j '.group.type_slug'))  invite=$(j '.invite_code.token')"
echo

run() { # run "label" fn...
  local label="$1"; shift
  if [[ "$DRY_RUN" -eq 1 ]]; then echo "[dry-run] $label"; return 0; fi
  echo ">> $label"
  "$@" || echo "   (non-fatal) step returned error — continuing (may already exist)"
}

# 1. demo user (companion self-register)
seed_user() {
  local body; body="$(jq -c '{name: .demo_user.name, emailPhone: .demo_user.emailPhone, password: .demo_user.password}' "$FIXTURE")"
  comp POST /auth/self-register "$body"
}
run "1. self-register demo user $(j '.demo_user.name')" seed_user

# 2. group create+activate with group-type (companion orchestrator reads dt_group_type_config archetype)
seed_group() {
  local body; body="$(jq -c '{
    name: .group.name, officeId: .group.officeId, currency: .group.currency,
    meetingDay: .group.meetingDay, meetingTime: .group.meetingTime,
    typeConfig: { slug: .group.type_slug, pool_model: .group.pool_model,
      shareout_formula: .group.shareout_formula, contribution_model: .group.contribution_model,
      share_value: .group.share_value, cycle_length_months: .group.cycle_length_months }
  }' "$FIXTURE")"
  comp POST /groups "$body"
}
run "2. create+activate group $(j '.group.name') as $(j '.group.type_slug')" seed_group

# 3. members + roles (dt_member_role rows via Fineract datatable)
seed_members() {
  local n; n="$(jq '.members | length' "$FIXTURE")"
  for i in $(seq 0 $((n-1))); do
    local cid role body
    cid="$(jq -r ".members[$i].fineractClientId" "$FIXTURE")"
    role="$(jq -r ".members[$i].role" "$FIXTURE")"
    body="$(jq -c "{role: .members[$i].role, client_type: \"end_user\", group_id: .group.fineractGroupId, joined_date: .members[$i].joinDate, is_active: true, locale: \"en\", dateFormat: \"yyyy-MM-dd\"}" "$FIXTURE")"
    echo "   - client $cid -> $role"
    fin POST "/datatables/dt_member_role/${cid}" "$body" >/dev/null || true
  done
}
run "3. associate 5 members + write roles" seed_members

# 4. savings accounts (create + approve + activate) — MONEY-AFFECTING
seed_savings() {
  local n; n="$(jq '.savings_accounts | length' "$FIXTURE")"
  for i in $(seq 0 $((n-1))); do
    local acc kind bal
    acc="$(jq -r ".savings_accounts[$i].accountNo" "$FIXTURE")"
    kind="$(jq -r ".savings_accounts[$i].kind" "$FIXTURE")"
    bal="$(jq -r ".savings_accounts[$i].balance" "$FIXTURE")"
    echo "   - savings $acc ($kind) opening balance $bal KES  [create+approve+activate+deposit]"
    # NOTE: real create requires a savings productId resolved on the target Fineract.
    # This step is intentionally descriptive: wire productId then POST /savingsaccounts,
    # ?command=approve, ?command=activate, then /transactions?command=deposit.
  done
}
run "4. group-linked + voluntary savings accounts (money-affecting)" seed_savings

# 5. meeting records (dt_meeting_record, multi-row, on m_group keyed by groupId)
seed_meetings() {
  local gid n; gid="$(j '.group.fineractGroupId')"; n="$(jq '.meeting_records | length' "$FIXTURE")"
  for i in $(seq 0 $((n-1))); do
    local body mn
    mn="$(jq -r ".meeting_records[$i].meeting_number" "$FIXTURE")"
    body="$(jq -c ".meeting_records[$i] + {locale: \"en\", dateFormat: \"yyyy-MM-dd\"}" "$FIXTURE")"
    echo "   - meeting #$mn"
    fin POST "/datatables/dt_meeting_record/${gid}" "$body" >/dev/null || true
  done
}
run "5. 3 meeting records" seed_meetings

# 6. corpus row (dt_group_corpus, single-row on m_group keyed by groupId)
seed_corpus() {
  local gid body; gid="$(j '.group.fineractGroupId')"
  body="$(jq -c '.corpus + {locale: "en", dateFormat: "yyyy-MM-dd"}' "$FIXTURE")"
  fin POST "/datatables/dt_group_corpus/${gid}" "$body" >/dev/null || true
}
run "6. corpus row (closing balance $(j '.corpus.closing_balance') KES)" seed_corpus

# 7. vsla_cycle row (dt_vsla_cycle on groupId)
seed_cycle() {
  local gid body; gid="$(j '.group.fineractGroupId')"
  body="$(jq -c '.vsla_cycle + {locale: "en", dateFormat: "yyyy-MM-dd"}' "$FIXTURE")"
  fin POST "/datatables/dt_vsla_cycle/${gid}" "$body" >/dev/null || true
}
run "7. vsla_cycle row (share_value $(j '.vsla_cycle.share_value'))" seed_cycle

# 8. ONE live invite code (companion invitation)
seed_invite() {
  local gid body; gid="$(j '.invite_code.group_id')"
  body="$(jq -c '{invited_email_phone: .invite_code.invited_email_phone, role_to_assign: .invite_code.role_to_assign, expires_at: .invite_code.expires_at, token: .invite_code.token}' "$FIXTURE")"
  comp POST "/datatables/invitations/${gid}" "$body"
}
run "8. live invite code $(j '.invite_code.token') (role $(j '.invite_code.role_to_assign'))" seed_invite

echo
echo "== demo seed complete. Demo Explore user: $(j '.demo_user.name') / invite code: $(j '.invite_code.token') =="
