#!/usr/bin/env bash
# =============================================================================
# seed-demo.sh — materialize the ENRICHED MifosSave demo dataset on a LIVE
# Fineract + companion backend, fully DATA-DRIVEN from ./demo-fixture.json.
# =============================================================================
#
# WHAT IT SEEDS (one fully-populated group PER catalogue archetype — 9 groups —
# plus 6 self-registered demo LOGIN accounts, one per user type, distributed as members):
#
#   0. demo LOGIN accounts   companion /auth/self-register — one per user type:
#                            Amina (treasurer), Joseph (chairperson), Grace (member),
#                            Faith (organizer), Peter (secretary), David (field officer)
#   1. group + type-config   companion POST /companion/groups (captures fineractGroupId)
#   2. members + roles       regular -> companion POST /companion/members (client+associate+role);
#                            demo    -> resolve self-registered client + associate + dt_member_role
#   3. savings               group-linked (groupId) + individual (clientId): create->approve->
#                            activate->deposit  (Fineract /savingsaccounts) — MONEY-AFFECTING
#   4. meetings              COMPLETED -> dt_meeting_record + per-member dt_meeting_attendance;
#                            UPCOMING  -> dt_meeting_schedule
#   5. loans (lending types) create->approve->disburse->repayment (Fineract /loans) + dt_loan_vote
#   6. distribution          per archetype: dt_group_corpus + dt_vsla_cycle (ACCUMULATING),
#                            dt_rosca_rotation (ROTATING_PAYOUT), dt_social_fund / dt_welfare_fund
#   7. invitations           companion POST /companion/datatables/invitations/{groupId};
#                            ACCEPTED -> PUT mark-accepted by token
#
# ID-CAPTURE CONTRACT (the current seed's fatal weakness, now fixed): the script
# NEVER assumes Fineract client/group ids. It CAPTURES the real ids from each
# create response and builds a runtime local_id -> fineractId map (a tmp file, so
# it works on macOS bash 3.2 with no associative arrays).
#
# IDEMPOTENT + SAFE TO RE-RUN: a group whose NAME already exists is SKIPPED wholesale
# (no re-created members, no double deposits, no double loans). Demo self-register and
# every datatable write tolerate "already exists". `set -uo pipefail` (NOT -e) + a per-step
# `run` wrapper mean one failure never aborts the rest.
#
# DATE MODEL (why dates are computed, not taken from the fixture for financial rows):
#   Fineract enforces ordering on REAL financial entities (client activation <= savings/loan
#   dates <= business date), and mifos-bank-2's business date runs ~3 days behind the host
#   clock. So financial dates are computed relative to now (past-safe):
#     - FORMATION_DATE  (regular member client activation)     = today-90d  [SEED_FORMATION_DAYS]
#     - TXN_DATE        (group/individual savings + current loans) = today-3d [SEED_TXN_DAYS]
#     - OVERDUE loans disburse today-45d ; REPAID loans disburse today-60d (borrowers are
#       regular members activated today-90d, so the backdate is valid).
#   Demo-account clients are activated by companion self-register (~today-3d), so their
#   savings/current-loans use TXN_DATE (same-day, valid). DATATABLE narrative dates
#   (meeting_date, cycle/corpus/rotation dates) are taken verbatim from the fixture —
#   Fineract does NOT order datatable date columns against the business date.
#
# PREREQUISITE: ../register-datatables.sh (21 datatables) + ../register-products.sh
# (KES + 'VSLA Group Savings' + 'VSLA Group Loan') already run. EXTERNAL GATE: a
# reachable Fineract AND the deployed companion API (mcp-mifosx).
#
# Usage:
#   FINERACT_BASE_URL=https://<host>/fineract-provider/api/v1 \
#   COMPANION_BASE_URL=https://<host>/companion \
#   FINERACT_USER=mifos FINERACT_PASSWORD=password FINERACT_TENANT=mifos-bank-2 \
#   bash seed-demo.sh [--dry-run]
#
# Env:
#   FINERACT_BASE_URL    (required unless --dry-run)
#   COMPANION_BASE_URL   (required unless --dry-run) — NOTE: NO trailing "/companion" duplication;
#                        companion paths below are absolute (/companion/...), so set this to the
#                        API ROOT (e.g. https://host) — the script prefixes /companion itself.
#   FINERACT_USER / FINERACT_PASSWORD / FINERACT_TENANT   (defaults mifos/password/default)
#   INSECURE=1           pass -k to curl (self-signed sandbox certs)
#   SEED_FORMATION_DAYS  (default 90)   SEED_TXN_DAYS (default 3)
#   SEED_OVERDUE_DAYS    (default 45)   SEED_REPAID_DAYS (default 60)
#   SAVINGS_PRODUCT_NAME (default "VSLA Group Savings")  LOAN_PRODUCT_NAME (default "VSLA Group Loan")
#
# Requires: bash, curl, jq.
# =============================================================================
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIXTURE="${SCRIPT_DIR}/demo-fixture.json"

FINERACT_BASE_URL="${FINERACT_BASE_URL:-}"
COMPANION_BASE_URL="${COMPANION_BASE_URL:-}"
FINERACT_USER="${FINERACT_USER:-mifos}"
FINERACT_PASSWORD="${FINERACT_PASSWORD:-password}"
FINERACT_TENANT="${FINERACT_TENANT:-default}"
SAVINGS_PRODUCT_NAME="${SAVINGS_PRODUCT_NAME:-VSLA Group Savings}"
LOAN_PRODUCT_NAME="${LOAN_PRODUCT_NAME:-VSLA Group Loan}"

DRY_RUN=0
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

command -v jq   >/dev/null || { echo "FATAL: jq required"   >&2; exit 3; }
command -v curl >/dev/null || { echo "FATAL: curl required" >&2; exit 3; }
[[ -f "$FIXTURE" ]]        || { echo "FATAL: fixture not found: $FIXTURE" >&2; exit 3; }
if [[ "$DRY_RUN" -eq 0 ]]; then
  [[ -n "$FINERACT_BASE_URL" ]]  || { echo "FATAL: FINERACT_BASE_URL required (external gate)" >&2; exit 4; }
  [[ -n "$COMPANION_BASE_URL" ]] || { echo "FATAL: COMPANION_BASE_URL required (companion API must be deployed)" >&2; exit 4; }
fi

CURL_OPTS=(-sS --max-time 60)
[[ "${INSECURE:-0}" == "1" ]] && CURL_OPTS+=(-k)

# ── cross-platform "N days ago" -> yyyy-MM-dd (BSD/macOS `date -v` vs GNU `date -d`) ──
date_days_ago() {
  local n="$1"
  if date -v-1d +%Y-%m-%d >/dev/null 2>&1; then
    date -v-"${n}"d +%Y-%m-%d          # BSD / macOS
  else
    date -d "${n} days ago" +%Y-%m-%d  # GNU / Linux
  fi
}
FORMATION_DATE="$(date_days_ago "${SEED_FORMATION_DAYS:-90}")"
TXN_DATE="$(date_days_ago "${SEED_TXN_DAYS:-3}")"
OVERDUE_DISBURSE_DATE="$(date_days_ago "${SEED_OVERDUE_DAYS:-45}")"
OVERDUE_APPROVE_DATE="$(date_days_ago "$(( ${SEED_OVERDUE_DAYS:-45} + 2 ))")"
OVERDUE_REPAY_DATE="$(date_days_ago "$(( ${SEED_OVERDUE_DAYS:-45} - 7 ))")"
REPAID_DISBURSE_DATE="$(date_days_ago "${SEED_REPAID_DAYS:-60}")"
REPAID_REPAY1_DATE="$(date_days_ago "$(( ${SEED_REPAID_DAYS:-60} - 20 ))")"
REPAID_REPAY2_DATE="$(date_days_ago "$(( ${SEED_REPAID_DAYS:-60} - 40 ))")"

# ── HTTP helpers ──
fin() {  # fin METHOD PATH [json-body]   (Fineract REST, service credential)
  local m="$1" p="$2" b="${3:-}"
  local args=(-u "${FINERACT_USER}:${FINERACT_PASSWORD}" -H "Fineract-Platform-TenantId: ${FINERACT_TENANT}" -H "Content-Type: application/json" -X "$m")
  [[ -n "$b" ]] && args+=(-d "$b")
  curl "${CURL_OPTS[@]}" "${args[@]}" "${FINERACT_BASE_URL}${p}"
}
comp() { # comp METHOD PATH [json-body]  (companion API — absolute /companion/... paths)
  local m="$1" p="$2" b="${3:-}"
  # Paths are absolute (/companion/…), so the base must be the HOST. Tolerate a caller that passes
  # COMPANION_BASE_URL with a trailing /companion (the provision-instance / health convention) by
  # stripping it — otherwise the URL doubles to …/companion/companion/… → ServeMux 404.
  local base="${COMPANION_BASE_URL%/companion}"
  local args=(-H "Content-Type: application/json" -X "$m")
  [[ -n "$b" ]] && args+=(-d "$b")
  curl "${CURL_OPTS[@]}" "${args[@]}" "${base}${p}"
}
j() { jq -r "$1" "$FIXTURE"; }   # read from the fixture

# ── runtime local_id -> fineractId map (tmp file; bash-3.2 safe, no assoc arrays) ──
MAP_FILE="$(mktemp -t seed-demo-idmap.XXXXXX)"
trap 'rm -f "$MAP_FILE"' EXIT
map_put() { printf '%s\t%s\n' "$1" "$2" >> "$MAP_FILE"; }         # map_put key id
map_get() { grep -m1 -F "$(printf '%s\t' "$1")" "$MAP_FILE" 2>/dev/null | cut -f2; }  # map_get key -> id

STEP_OK=0; STEP_ERR=0
run() { # run "label" cmd...   — dry-run aware, non-fatal
  local label="$1"; shift
  if [[ "$DRY_RUN" -eq 1 ]]; then echo "   [plan] $label"; return 0; fi
  if "$@"; then STEP_OK=$((STEP_OK+1)); else STEP_ERR=$((STEP_ERR+1)); echo "      (non-fatal) '$label' returned error — continuing"; fi
}

# ── capture helper: run a producing curl, echo the response, extract a field ──
capture() { # capture JQ_FILTER -- CURL_FN ARGS...   → prints extracted id (or empty)
  local filter="$1"; shift; [[ "$1" == "--" ]] && shift
  local resp; resp="$("$@")"
  printf '%s' "$resp" | jq -r "$filter" 2>/dev/null | grep -E '^[0-9]+$' | head -1
}

first_word() { printf '%s' "$1" | awk '{print $1}'; }
rest_words() { printf '%s' "$1" | awk '{$1=""; sub(/^ /,""); print}'; }

echo "== MifosSave ENRICHED demo seed =="
echo "   fixture   : $FIXTURE"
echo "   fineract  : ${FINERACT_BASE_URL:-<dry-run>}   tenant: ${FINERACT_TENANT}"
echo "   companion : ${COMPANION_BASE_URL:-<dry-run>}"
echo "   groups    : $(j '.groups | length')   demo accounts: $(j '.demo_accounts | length')"
echo "   dates     : formation=${FORMATION_DATE}  txn=${TXN_DATE}  overdue-disburse=${OVERDUE_DISBURSE_DATE}  repaid-disburse=${REPAID_DISBURSE_DATE}"
echo

# =============================================================================
# PREFLIGHT — resolve savings + loan product ids by NAME (never hardcode)
# =============================================================================
SAVINGS_PRODUCT_ID=""; LOAN_PRODUCT_ID=""
if [[ "$DRY_RUN" -eq 0 ]]; then
  SAVINGS_PRODUCT_ID="$(fin GET /savingsproducts | jq -r --arg n "$SAVINGS_PRODUCT_NAME" '.[]?|select(.name==$n)|.id' 2>/dev/null | head -1)"
  LOAN_PRODUCT_ID="$(fin GET /loanproducts   | jq -r --arg n "$LOAN_PRODUCT_NAME"   '.[]?|select(.name==$n)|.id' 2>/dev/null | head -1)"
  echo ">> preflight: savings product '$SAVINGS_PRODUCT_NAME' = id ${SAVINGS_PRODUCT_ID:-<UNRESOLVED>}"
  echo ">> preflight: loan product    '$LOAN_PRODUCT_NAME'    = id ${LOAN_PRODUCT_ID:-<UNRESOLVED>}"
  [[ -n "$SAVINGS_PRODUCT_ID" ]] || echo "   (warn) savings product not found — savings steps will be skipped. Run ../register-products.sh first."
  [[ -n "$LOAN_PRODUCT_ID"   ]] || echo "   (warn) loan product not found — loan steps will be skipped. Run ../register-products.sh first."
else
  echo "   [plan] resolve savings product '$SAVINGS_PRODUCT_NAME' + loan product '$LOAN_PRODUCT_NAME' by name (GET /savingsproducts, /loanproducts)"
fi
echo

# =============================================================================
# STEP 0 — self-register the 4 demo LOGIN accounts (once), capture their clientIds
# =============================================================================
echo "== STEP 0: demo login accounts =="
DACC_N="$(jq '.demo_accounts | length' "$FIXTURE")"
for di in $(seq 0 $((DACC_N-1))); do
  d_name="$(jq -r ".demo_accounts[$di].name" "$FIXTURE")"
  d_ep="$(jq -r ".demo_accounts[$di].email_phone" "$FIXTURE")"
  d_pw="$(jq -r ".demo_accounts[$di].password" "$FIXTURE")"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "   [plan] self-register '$d_name' ($d_ep) then resolve clientId via GET /clients?externalId=$d_ep"
    continue
  fi
  echo ">> self-register $d_name ($d_ep)"
  body="$(jq -nc --arg n "$d_name" --arg e "$d_ep" --arg p "$d_pw" '{name:$n, emailPhone:$e, password:$p}')"
  comp POST /companion/auth/self-register "$body" >/dev/null 2>&1 || echo "   (non-fatal) self-register returned error (likely already exists) — continuing"
  # Resolve the self-registered client by externalId (== lowercased emailPhone). URL-encode '+'.
  enc="${d_ep//+/%2B}"
  cid="$(fin GET "/clients?externalId=${enc}" | jq -r '(.pageItems // .) | .[0].id // empty' 2>/dev/null)"
  if [[ -n "$cid" && "$cid" != "null" ]]; then
    map_put "email:${d_ep}" "$cid"
    echo "   resolved clientId=$cid for $d_name"
  else
    echo "   (warn) could NOT resolve clientId for $d_name ($d_ep) — its group memberships will be skipped"
  fi
done
echo

# =============================================================================
# Per-group workers
# =============================================================================
resolve_group_by_name() { # $1=name  -> prints existing fineract group id or empty
  fin GET "/groups?limit=1000" | jq -r --arg n "$1" '((.pageItems // .) | map(select(.name==$n)) | .[0].id) // empty' 2>/dev/null
}

seed_member() { # $1=group_index $2=member_index $3=gid
  local gi="$1" mi="$2" gid="$3"
  local base=".groups[$gi].members[$mi]"
  local lid name phone role join demo email
  lid="$(jq -r "$base.local_id" "$FIXTURE")"
  name="$(jq -r "$base.name" "$FIXTURE")"
  phone="$(jq -r "$base.phone" "$FIXTURE")"
  role="$(jq -r "$base.role" "$FIXTURE")"
  join="$(jq -r "$base.join_date" "$FIXTURE")"
  demo="$(jq -r "$base.is_demo_account" "$FIXTURE")"
  email="$(jq -r "$base.email_phone // empty" "$FIXTURE")"
  local fn ln; fn="$(first_word "$name")"; ln="$(rest_words "$name")"; [[ -z "$ln" ]] && ln="$fn"

  if [[ "$demo" == "true" ]]; then
    local cid; cid="$(map_get "email:${email}")"
    if [[ -z "$cid" ]]; then echo "   (warn) demo member $name unresolved — skipping"; return 0; fi
    # associate the already-existing self-registered client to this group + write role
    local abody rbody
    abody="$(jq -nc --argjson c "$cid" '{clientMembers:[$c]}')"
    fin POST "/groups/${gid}?command=associateClients" "$abody" >/dev/null 2>&1 || true
    rbody="$(jq -nc --arg r "$role" --argjson g "$gid" --arg d "$join" '{role:$r, client_type:"end_user", group_id:$g, joined_date:$d, is_active:true, locale:"en", dateFormat:"yyyy-MM-dd"}')"
    fin POST "/datatables/dt_member_role/${cid}" "$rbody" >/dev/null 2>&1 || true
    map_put "mem:${lid}" "$cid"
    echo "   demo    $name -> client $cid (role $role)"
  else
    # regular member: companion orchestrates client-create + group-associate + dt_member_role in one call
    local mbody cid
    mbody="$(jq -nc --arg fn "$fn" --arg ln "$ln" --arg mo "$phone" --arg ad "$FORMATION_DATE" \
                    --argjson gid "$gid" --arg role "$role" \
      '{firstname:$fn, lastname:$ln, mobileNo:$mo, active:true, activationDate:$ad, officeId:1, groupId:$gid, locale:"en", dateFormat:"yyyy-MM-dd", role:$role, assignedDate:$ad}')"
    cid="$(capture '.clientId // .resourceId' -- comp POST /companion/members "$mbody")"
    if [[ -n "$cid" ]]; then
      map_put "mem:${lid}" "$cid"
      echo "   member  $name -> client $cid (role $role)"
    else
      echo "   (warn) regular member $name create returned no clientId — downstream steps for this member skipped"
    fi
  fi
}

seed_group_savings() { # $1=group_index $2=gid
  local gi="$1" gid="$2"
  [[ -z "$SAVINGS_PRODUCT_ID" ]] && { echo "   (skip) no savings product resolved"; return 0; }
  local total; total="$(jq -r ".groups[$gi].group_savings_total" "$FIXTURE")"
  # 1 group-linked account on the GROUP (companion reads groups/{id}/accounts and splits pro-rata)
  local sbody sid
  sbody="$(jq -nc --argjson p "$SAVINGS_PRODUCT_ID" --argjson g "$gid" --arg d "$TXN_DATE" \
    '{productId:$p, groupId:$g, submittedOnDate:$d, locale:"en", dateFormat:"yyyy-MM-dd"}')"
  sid="$(capture '.savingsId // .resourceId' -- fin POST /savingsaccounts "$sbody")"
  if [[ -n "$sid" ]]; then
    fin POST "/savingsaccounts/${sid}?command=approve"  "$(jq -nc --arg d "$TXN_DATE" '{approvedOnDate:$d, locale:"en", dateFormat:"yyyy-MM-dd"}')"  >/dev/null 2>&1 || true
    fin POST "/savingsaccounts/${sid}?command=activate" "$(jq -nc --arg d "$TXN_DATE" '{activatedOnDate:$d, locale:"en", dateFormat:"yyyy-MM-dd"}')" >/dev/null 2>&1 || true
    fin POST "/savingsaccounts/${sid}/transactions?command=deposit" \
        "$(jq -nc --arg d "$TXN_DATE" --argjson a "$total" '{transactionDate:$d, transactionAmount:$a, paymentTypeId:1, locale:"en", dateFormat:"yyyy-MM-dd"}')" >/dev/null 2>&1 || true
    echo "   group savings acct $sid: deposited $total KES (group-linked corpus)"
  else
    echo "   (warn) group savings account create returned no id"
  fi
}

seed_individual_savings() { # $1=group_index
  local gi="$1"
  [[ -z "$SAVINGS_PRODUCT_ID" ]] && return 0
  local mn; mn="$(jq ".groups[$gi].members | length" "$FIXTURE")"
  for mi in $(seq 0 $((mn-1))); do
    local ind lid cid
    ind="$(jq -r ".groups[$gi].members[$mi].savings.individual // 0" "$FIXTURE")"
    [[ "$ind" -gt 0 ]] 2>/dev/null || continue
    lid="$(jq -r ".groups[$gi].members[$mi].local_id" "$FIXTURE")"
    cid="$(map_get "mem:${lid}")"; [[ -z "$cid" ]] && continue
    local sbody sid
    sbody="$(jq -nc --argjson p "$SAVINGS_PRODUCT_ID" --argjson c "$cid" --arg d "$TXN_DATE" \
      '{productId:$p, clientId:$c, submittedOnDate:$d, locale:"en", dateFormat:"yyyy-MM-dd"}')"
    sid="$(capture '.savingsId // .resourceId' -- fin POST /savingsaccounts "$sbody")"
    [[ -z "$sid" ]] && continue
    fin POST "/savingsaccounts/${sid}?command=approve"  "$(jq -nc --arg d "$TXN_DATE" '{approvedOnDate:$d, locale:"en", dateFormat:"yyyy-MM-dd"}')"  >/dev/null 2>&1 || true
    fin POST "/savingsaccounts/${sid}?command=activate" "$(jq -nc --arg d "$TXN_DATE" '{activatedOnDate:$d, locale:"en", dateFormat:"yyyy-MM-dd"}')" >/dev/null 2>&1 || true
    fin POST "/savingsaccounts/${sid}/transactions?command=deposit" \
        "$(jq -nc --arg d "$TXN_DATE" --argjson a "$ind" '{transactionDate:$d, transactionAmount:$a, paymentTypeId:1, locale:"en", dateFormat:"yyyy-MM-dd"}')" >/dev/null 2>&1 || true
    echo "   individual savings acct $sid (client $cid): deposited $ind KES"
  done
}

seed_meetings() { # $1=group_index $2=gid
  local gi="$1" gid="$2"
  local mn; mn="$(jq ".groups[$gi].meetings | length" "$FIXTURE")"
  for i in $(seq 0 $((mn-1))); do
    local base=".groups[$gi].meetings[$i]"
    local state num; state="$(jq -r "$base.state" "$FIXTURE")"; num="$(jq -r "$base.number" "$FIXTURE")"
    if [[ "$state" == "COMPLETED" ]]; then
      local rbody
      rbody="$(jq -c "$base | {meeting_number:.number, meeting_date:.date, opening_balance, closing_balance,
        total_inflows:(.total_savings_collected + .total_repayments_received),
        total_outflows:.total_loans_disbursed, total_savings_collected, total_repayments_received,
        total_loans_disbursed, total_fines_collected, attendance_count, notes,
        locale:\"en\", dateFormat:\"yyyy-MM-dd\"}" "$FIXTURE")"
      fin POST "/datatables/dt_meeting_record/${gid}" "$rbody" >/dev/null 2>&1 || true
      # per-member attendance rows (dt_meeting_attendance on m_client)
      local an; an="$(jq "$base.attendance | length" "$FIXTURE")"
      for ai in $(seq 0 $((an-1))); do
        local abase="$base.attendance[$ai]" alid acid abody
        alid="$(jq -r "$abase.member_local_id" "$FIXTURE")"
        acid="$(map_get "mem:${alid}")"; [[ -z "$acid" ]] && continue
        abody="$(jq -c "$abase | {meeting_number:$num, status, fine_amount, savings_collected, repayment_amount, locale:\"en\"}" "$FIXTURE")"
        fin POST "/datatables/dt_meeting_attendance/${acid}" "$abody" >/dev/null 2>&1 || true
      done
      echo "   meeting #$num COMPLETED (record + $an attendance rows)"
    else
      # UPCOMING -> forward schedule row
      local sbody
      sbody="$(jq -c "$base | {meeting_number:.number, scheduled_date:.date, cadence:\"weekly\", status:\"SCHEDULED\", locale:\"en\", dateFormat:\"yyyy-MM-dd\"}" "$FIXTURE")"
      fin POST "/datatables/dt_meeting_schedule/${gid}" "$sbody" >/dev/null 2>&1 || true
      echo "   meeting #$num UPCOMING (schedule row)"
    fi
  done
}

seed_loans() { # $1=group_index $2=gid
  local gi="$1" gid="$2"
  [[ -z "$LOAN_PRODUCT_ID" ]] && { local ln0; ln0="$(jq ".groups[$gi].loans | length" "$FIXTURE")"; [[ "$ln0" -gt 0 ]] && echo "   (skip) no loan product resolved"; return 0; }
  local ln; ln="$(jq ".groups[$gi].loans | length" "$FIXTURE")"
  local rate; rate="$(jq -r ".groups[$gi].type_config.defaultInterestRatePct // 2" "$FIXTURE")"
  for i in $(seq 0 $((ln-1))); do
    local base=".groups[$gi].loans[$i]"
    local blid bcid state P nrep sdate ddate
    blid="$(jq -r "$base.borrower_local_id" "$FIXTURE")"
    bcid="$(map_get "mem:${blid}")"; [[ -z "$bcid" ]] && { echo "   (warn) loan borrower $blid unresolved — skipping"; continue; }
    state="$(jq -r "$base.state" "$FIXTURE")"
    P="$(jq -r "$base.principal" "$FIXTURE")"
    nrep="$(jq -r "$base.number_of_repayments" "$FIXTURE")"
    case "$state" in
      OVERDUE) sdate="$OVERDUE_APPROVE_DATE"; ddate="$OVERDUE_DISBURSE_DATE" ;;
      REPAID)  sdate="$REPAID_DISBURSE_DATE"; ddate="$REPAID_DISBURSE_DATE" ;;
      *)       sdate="$TXN_DATE";             ddate="$TXN_DATE" ;;
    esac
    # 1. create (submitted) — mirror companion loan-apply flatten (loanType individual, weekly)
    local lbody lid
    lbody="$(jq -nc --argjson c "$bcid" --argjson p "$LOAN_PRODUCT_ID" --argjson P "$P" \
                    --argjson n "$nrep" --argjson r "$rate" --arg sd "$sdate" --arg dd "$ddate" \
      '{clientId:$c, productId:$p, loanType:"individual", principal:$P,
        loanTermFrequency:$n, loanTermFrequencyType:1, numberOfRepayments:$n, repaymentEvery:1,
        repaymentFrequencyType:1, interestRatePerPeriod:$r, amortizationType:1, interestType:1,
        interestCalculationPeriodType:1, transactionProcessingStrategyCode:"mifos-standard-strategy",
        expectedDisbursementDate:$dd, submittedOnDate:$sd, locale:"en", dateFormat:"yyyy-MM-dd"}')"
    lid="$(capture '.loanId // .resourceId' -- fin POST /loans "$lbody")"
    if [[ -z "$lid" ]]; then echo "   (warn) loan create ($state, $blid) returned no loanId — skipping rest"; continue; fi

    # dt_loan_vote tally (single-row on m_loan)
    local vbody
    vbody="$(jq -c "$base.votes | {meeting_number:1, votes_for:.for, votes_against:.against, votes_abstain:.abstain,
      chairperson_approved:(.for > .against),
      outcome:(if .for > .against then \"APPROVED\" else \"REJECTED\" end), locale:\"en\"}" "$FIXTURE")"
    fin POST "/datatables/dt_loan_vote/${lid}" "$vbody" >/dev/null 2>&1 || true

    if [[ "$state" == "PENDING" ]]; then echo "   loan $lid PENDING (client $bcid, $P KES) + vote"; continue; fi

    # 2. approve + 3. disburse (DISBURSED / OVERDUE / REPAID)
    fin POST "/loans/${lid}?command=approve" \
      "$(jq -nc --arg d "$sdate" --argjson a "$P" --arg dd "$ddate" '{approvedOnDate:$d, approvedLoanAmount:$a, expectedDisbursementDate:$dd, locale:"en", dateFormat:"yyyy-MM-dd"}')" >/dev/null 2>&1 || true
    fin POST "/loans/${lid}?command=disburse" \
      "$(jq -nc --arg d "$ddate" --argjson a "$P" '{actualDisbursementDate:$d, transactionAmount:$a, locale:"en", dateFormat:"yyyy-MM-dd"}')" >/dev/null 2>&1 || true

    # 4. repayments (dates depend on state)
    local rpn; rpn="$(jq "$base.repayments | length" "$FIXTURE")"
    for ri in $(seq 0 $((rpn-1))); do
      local amt rdate
      amt="$(jq -r "$base.repayments[$ri]" "$FIXTURE")"
      if [[ "$state" == "OVERDUE" ]]; then rdate="$OVERDUE_REPAY_DATE"
      elif [[ "$ri" -eq 0 ]]; then rdate="$REPAID_REPAY1_DATE"; else rdate="$REPAID_REPAY2_DATE"; fi
      fin POST "/loans/${lid}/transactions?command=repayment" \
        "$(jq -nc --arg d "$rdate" --argjson a "$amt" '{transactionDate:$d, transactionAmount:$a, locale:"en", dateFormat:"yyyy-MM-dd"}')" >/dev/null 2>&1 || true
    done
    echo "   loan $lid $state (client $bcid, $P KES, $rpn repayment(s)) + vote"
  done
}

seed_distribution() { # $1=group_index $2=gid
  local gi="$1" gid="$2"
  local base=".groups[$gi].distribution"
  # corpus (ACCUMULATING)
  if [[ "$(jq "$base | has(\"corpus\")" "$FIXTURE")" == "true" ]]; then
    fin POST "/datatables/dt_group_corpus/${gid}" \
      "$(jq -c "$base.corpus + {locale:\"en\", dateFormat:\"yyyy-MM-dd\"}" "$FIXTURE")" >/dev/null 2>&1 || true
    echo "   dt_group_corpus (closing $(jq -r "$base.corpus.closing_balance" "$FIXTURE") KES)"
  fi
  # vsla_cycle (ACCUMULATING)
  if [[ "$(jq "$base | has(\"cycle\")" "$FIXTURE")" == "true" ]]; then
    fin POST "/datatables/dt_vsla_cycle/${gid}" \
      "$(jq -c "$base.cycle + {locale:\"en\", dateFormat:\"yyyy-MM-dd\"}" "$FIXTURE")" >/dev/null 2>&1 || true
    echo "   dt_vsla_cycle (cycle $(jq -r "$base.cycle.cycle_number" "$FIXTURE"))"
  fi
  # social fund (hasSocialFund) — datetime column only → datetime dateFormat
  if [[ "$(jq "$base | has(\"social\")" "$FIXTURE")" == "true" ]]; then
    fin POST "/datatables/dt_social_fund/${gid}" \
      "$(jq -c "$base.social + {locale:\"en\", dateFormat:\"yyyy-MM-dd HH:mm\"}" "$FIXTURE")" >/dev/null 2>&1 || true
    echo "   dt_social_fund (balance $(jq -r "$base.social.current_balance" "$FIXTURE") KES)"
  fi
  # welfare fund (welfareOnlyMode)
  if [[ "$(jq "$base | has(\"welfare\")" "$FIXTURE")" == "true" ]]; then
    fin POST "/datatables/dt_welfare_fund/${gid}" \
      "$(jq -c "$base.welfare + {locale:\"en\", dateFormat:\"yyyy-MM-dd HH:mm\"}" "$FIXTURE")" >/dev/null 2>&1 || true
    echo "   dt_welfare_fund (balance $(jq -r "$base.welfare.current_balance" "$FIXTURE") KES)"
  fi
  # rosca rotation (ROTATING_PAYOUT) — omit paid_at (datetime) to avoid mixed date/datetime format
  if [[ "$(jq "$base | has(\"rotation\")" "$FIXTURE")" == "true" ]]; then
    local rn; rn="$(jq "$base.rotation | length" "$FIXTURE")"
    for ri in $(seq 0 $((rn-1))); do
      local rbase="$base.rotation[$ri]" rlid rcid rbody
      rlid="$(jq -r "$rbase.recipient_local_id" "$FIXTURE")"
      rcid="$(map_get "mem:${rlid}")"; [[ -z "$rcid" ]] && rcid=0
      rbody="$(jq -c "$rbase | {cycle_number, position, recipient_client_id:$rcid, recipient_name, amount, scheduled_date, payout_order_method, locale:\"en\", dateFormat:\"yyyy-MM-dd\"}" "$FIXTURE")"
      fin POST "/datatables/dt_rosca_rotation/${gid}" "$rbody" >/dev/null 2>&1 || true
    done
    echo "   dt_rosca_rotation ($rn positions)"
  fi
}

seed_invitations() { # $1=group_index $2=gid
  local gi="$1" gid="$2"
  local in; in="$(jq ".groups[$gi].invitations | length" "$FIXTURE")"
  for i in $(seq 0 $((in-1))); do
    local base=".groups[$gi].invitations[$i]"
    local ep role st exp
    ep="$(jq -r "$base.invited_email_phone" "$FIXTURE")"
    role="$(jq -r "$base.role_to_assign" "$FIXTURE")"
    st="$(jq -r "$base.state" "$FIXTURE")"
    exp="$(jq -r "$base.expires_at" "$FIXTURE")"
    local ibody token
    ibody="$(jq -nc --arg e "$ep" --arg r "$role" --arg x "$exp" '{invited_email_phone:$e, role_to_assign:$r, expires_at:$x}')"
    # companion GENERATES the token server-side; capture it from the response
    token="$(comp POST "/companion/datatables/invitations/${gid}" "$ibody" | jq -r '.token // empty' 2>/dev/null)"
    if [[ "$st" == "ACCEPTED" && -n "$token" ]]; then
      # mark-accepted resolves the row by token (rowId path segment is a sentinel)
      comp PUT "/companion/datatables/invitations/${token}/0" \
        "$(jq -nc --arg a "$TXN_DATE" '{accepted_at:$a}')" >/dev/null 2>&1 || true
      echo "   invite $ep -> token ${token} (ACCEPTED)"
    else
      echo "   invite $ep -> token ${token:-<none>} ($st)"
    fi
  done
}

# =============================================================================
# DRIVE — loop over every group
# =============================================================================
GN="$(jq '.groups | length' "$FIXTURE")"
for gi in $(seq 0 $((GN-1))); do
  gname="$(jq -r ".groups[$gi].name" "$FIXTURE")"
  garch="$(jq -r ".groups[$gi].archetype" "$FIXTURE")"
  mcount="$(jq ".groups[$gi].members | length" "$FIXTURE")"
  meetcount="$(jq ".groups[$gi].meetings | length" "$FIXTURE")"
  loancount="$(jq ".groups[$gi].loans | length" "$FIXTURE")"
  invcount="$(jq ".groups[$gi].invitations | length" "$FIXTURE")"
  savtotal="$(jq -r ".groups[$gi].group_savings_total" "$FIXTURE")"
  echo "============================================================"
  echo "GROUP $((gi+1))/$GN: $gname [$garch]"
  echo "  members=$mcount  savings=$savtotal KES  meetings=$meetcount  loans=$loancount  invites=$invcount"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "  [plan] create group (companion POST /companion/groups) + type-config"
    echo "  [plan] $mcount members (regular -> /companion/members ; demo -> associate+role)"
    echo "  [plan] group-linked savings deposit $savtotal KES + $(jq "[.groups[$gi].members[]|select(.savings.individual>0)]|length" "$FIXTURE") individual accounts"
    echo "  [plan] $meetcount meetings (records+attendance / schedule) ; $loancount loans ; distribution ; $invcount invitations"
    continue
  fi

  # idempotency: skip a group whose NAME already exists (no double money)
  existing="$(resolve_group_by_name "$gname")"
  if [[ -n "$existing" ]]; then
    echo "  SKIP — group '$gname' already exists (fineractGroupId=$existing). Re-run safe: not re-seeding."
    continue
  fi

  # 1. create group via companion (captures fineractGroupId + inviteCode)
  gbody="$(jq -c ".groups[$gi] as \$g | {
    name: \$g.name, officeId: \$g.office_id, currency: \$g.currency,
    meetingDay: \$g.meeting_day, meetingTime: \$g.meeting_time,
    typeConfig: {
      group_type: \$g.type_config.typeSlug,
      pool_model: \$g.type_config.savingsMechanism,
      contribution_model: \$g.type_config.contributionMode,
      shareout_formula: \$g.type_config.shareoutFormula,
      payout_order_method: \$g.type_config.payoutOrderMethod,
      share_value: \$g.type_config.shareValue,
      contribution_amount: \$g.type_config.contributionAmount,
      social_fund_enabled: \$g.type_config.hasSocialFund,
      social_fund_percent: \$g.type_config.socialFundPercent,
      cycle_length_months: \$g.type_config.defaultCycleLengthMonths,
      loan_multiplier: \$g.type_config.defaultLoanMultiplier,
      interest_rate: \$g.type_config.defaultInterestRatePct,
      fine_amount: \$g.type_config.fineAmount,
      max_members: \$g.type_config.maxMembers
    }
  }" "$FIXTURE")"
  gresp="$(comp POST /companion/groups "$gbody")"
  gid="$(printf '%s' "$gresp" | jq -r '.fineractGroupId // .groupId // empty' 2>/dev/null)"
  invite="$(printf '%s' "$gresp" | jq -r '.inviteCode // empty' 2>/dev/null)"
  if [[ -z "$gid" || "$gid" == "null" ]]; then
    # Create failed. A "data integrity"/duplicate-name 403 means the group DOES exist but the initial
    # resolve_group_by_name missed it (a transient /groups listing failure while the instance was busy).
    # Resolve once more and REUSE its id rather than hard-failing — so the enriched data still lands on
    # the existing group. Only a genuinely-uncreatable group falls through to FAIL.
    gid="$(resolve_group_by_name "$gname")"
    if [[ -z "$gid" || "$gid" == "null" ]]; then
      echo "  FAIL — group create returned no fineractGroupId: $(printf '%s' "$gresp" | head -c 200)"
      STEP_ERR=$((STEP_ERR+1)); continue
    fi
    echo "  REUSE — create hit a conflict; resolved existing fineractGroupId=$gid (seeding onto it)"
  else
    STEP_OK=$((STEP_OK+1))
    echo "  created group fineractGroupId=$gid  inviteCode=${invite:-<none>}"
  fi

  # 2. members
  for mi in $(seq 0 $((mcount-1))); do seed_member "$gi" "$mi" "$gid"; done
  # 3. savings
  run "group savings"      seed_group_savings "$gi" "$gid"
  run "individual savings" seed_individual_savings "$gi"
  # 4. meetings
  run "meetings"           seed_meetings "$gi" "$gid"
  # 5. loans
  run "loans"              seed_loans "$gi" "$gid"
  # 6. distribution
  run "distribution"       seed_distribution "$gi" "$gid"
  # 7. invitations
  run "invitations"        seed_invitations "$gi" "$gid"
done

echo "============================================================"
if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "== DRY RUN complete — no live writes performed. Plan printed above. =="
  exit 0
fi
echo "== ENRICHED demo seed complete: ${STEP_OK} steps ok, ${STEP_ERR} non-fatal errors =="
echo "   Demo Explore login: Amina Otieno / +254700000001 / DemoExplore@2026 (VSLA showcase)"
echo "   Other logins: David Ochieng (+254700000010), Grace Wanjiru (+254700000003), Joseph Mwangi (+254700000002)"
