#!/usr/bin/env bash
# =============================================================================
# register-products.sh — idempotent provisioning of the MifosSave VSLA
# financial products (currency + savings product + loan product) on a Fineract
# instance. The product half of `/mifos-bridge preflight` (Phase 2.5 PRODUCTS).
# =============================================================================
#
# A VSLA group's app surface needs THREE things configured on Fineract that a
# fresh instance does NOT ship with:
#
#   1. KES currency ENABLED  — the app is KES-based; a fresh instance selects
#      only INR/MXN/USD, so KES products cannot be created until KES is added
#      to the selected-currency list.
#   2. A KES savings product — "VSLA Group Savings" — the apptable every group /
#      member savings account is opened against (meeting savings collection).
#   3. KES loan products      — ONE PER GROUP ARCHETYPE (VSLA/ROSCA/ASCA/SILC/
#      SHG/SACCO/Village-Bank/Welfare/JLG) — what the loan-apply "Loan Product"
#      dropdown lists, each tuned to how that archetype lends (term/cadence/rate).
#
# ONE savings product serves all group types (a member saves as an individual
# client under the group regardless of type). Loan products are PER-ARCHETYPE so
# the operator picks archetype-appropriate terms in loan-apply; Fineract has no
# "group type" on a loan product, so these are individual-client products and the
# archetype nuance still lives in the companion's dt_group_type_config + app logic.
#
# Idempotent: currency is a set-PUT; products are create-or-skip (matched by
# name). Safe to re-run — that IS the preflight contract ("verify + configure if
# missing").
#
# Usage (env-driven, same as register-datatables.sh):
#   FINERACT_BASE_URL=https://<instance>/fineract-provider/api/v1 \
#   FINERACT_TENANT=<tenant> [FINERACT_USER=mifos FINERACT_PASSWORD=password] \
#   bash register-products.sh
# Requires: bash, curl, jq (matches the sibling scripts).
# =============================================================================
set -uo pipefail

FINERACT_BASE_URL="${FINERACT_BASE_URL:-}"
FINERACT_TENANT="${FINERACT_TENANT:-default}"
FINERACT_USER="${FINERACT_USER:-mifos}"
FINERACT_PASSWORD="${FINERACT_PASSWORD:-password}"
INSECURE="${INSECURE:-0}"
APP_CURRENCY="${APP_CURRENCY:-KES}"

[ -n "$FINERACT_BASE_URL" ] || { echo "FATAL: FINERACT_BASE_URL required" >&2; exit 3; }
command -v curl >/dev/null || { echo "FATAL: curl required" >&2; exit 3; }
command -v jq   >/dev/null || { echo "FATAL: jq required"   >&2; exit 3; }

CURL=(curl -sS --max-time 60 -u "$FINERACT_USER:$FINERACT_PASSWORD"
      -H "Fineract-Platform-TenantId: $FINERACT_TENANT"
      -H "Accept: application/json" -H "Content-Type: application/json")
[ "$INSECURE" = 1 ] && CURL+=(-k)

api(){ local m="$1" p="$2"; shift 2; "${CURL[@]}" -X "$m" "$FINERACT_BASE_URL$p" "$@"; }

rc=0

# ── 1. Ensure the app currency (KES) is enabled ──────────────────────────────
echo "▶ currency — ensuring $APP_CURRENCY enabled"
sel="$(api GET /currencies | jq -r '.selectedCurrencyOptions[].code' 2>/dev/null | tr '\n' ' ')"
if printf ' %s ' "$sel" | grep -q " $APP_CURRENCY "; then
  echo "  ✅ $APP_CURRENCY already enabled ($sel)"
else
  merged="$(printf '%s\n%s\n' "$sel" "$APP_CURRENCY" | tr ' ' '\n' | sed '/^$/d' | sort -u | jq -R . | jq -sc .)"
  code="$(api PUT /currencies -d "{\"currencies\":$merged}" -o /dev/null -w '%{http_code}')"
  if [ "$code" = 200 ]; then echo "  ✅ enabled $APP_CURRENCY (now: $(api GET /currencies | jq -r '[.selectedCurrencyOptions[].code]|join(",")'))"
  else echo "  ❌ failed to enable $APP_CURRENCY (http $code)"; rc=1; fi
fi

# ── 2. VSLA savings product (create-or-skip) ─────────────────────────────────
SAVINGS_NAME="VSLA Group Savings"
echo "▶ savings product — '$SAVINGS_NAME'"
sid="$(api GET /savingsproducts | jq -r --arg n "$SAVINGS_NAME" '.[]?|select(.name==$n)|.id' 2>/dev/null | head -1)"
if [ -n "$sid" ]; then echo "  ✅ exists (id $sid)"
else
  resp="$(api POST /savingsproducts -d "{
    \"name\":\"$SAVINGS_NAME\",\"shortName\":\"VGS\",
    \"description\":\"MifosSave VSLA group-linked savings\",
    \"currencyCode\":\"$APP_CURRENCY\",\"digitsAfterDecimal\":2,\"inMultiplesOf\":0,
    \"nominalAnnualInterestRate\":0,\"interestCompoundingPeriodType\":1,
    \"interestPostingPeriodType\":4,\"interestCalculationType\":1,
    \"interestCalculationDaysInYearType\":365,\"accountingRule\":1,\"locale\":\"en\"}")"
  sid="$(printf '%s' "$resp" | jq -r '.resourceId // empty')"
  if [ -n "$sid" ]; then echo "  ✅ created (id $sid)"
  else echo "  ❌ create failed: $(printf '%s' "$resp" | jq -r '.errors[0].defaultUserMessage // .defaultUserMessage // .' 2>/dev/null | head -1)"; rc=1; fi
fi

# ── 3. Loan products — ONE PER GROUP ARCHETYPE (create-or-skip) ──────────────
# The loan-apply "Loan Product" dropdown lists every registered KES loan product, so each group
# archetype gets a product tuned to how it lends (term, cadence, rate, ceiling). All are individual-
# client products under the group (Fineract has no "group type" on a loan product); the archetype
# nuance lives in dt_group_type_config + app logic, and these give the operator archetype-appropriate
# starting terms. Spec = shortName|name|principal|minP|maxP|numRepay|minRepay|maxRepay|every|freq|rate|maxRate|description
#   freq: 1=months, 2=weeks (repaymentFrequencyType). rate is per-period (interestRateFrequencyType matches).
LOAN_PRODUCTS=(
  "VGL|VSLA Group Loan|5000|500|300000|12|1|52|1|2|10|30|VSLA group loan (3x savings, weekly flat)"
  "RRA|ROSCA Rotation Advance|5000|1000|100000|4|1|12|1|2|0|10|ROSCA interest-free rotation-pot advance"
  "AAL|ASCA Accumulating Loan|8000|1000|300000|16|1|52|1|2|8|30|ASCA accumulating-fund loan"
  "SCL|SILC Community Loan|5000|500|200000|12|1|52|1|2|10|30|SILC internal-lending community loan"
  "SDL|SHG Development Loan|10000|1000|500000|12|1|36|1|1|2|10|SHG monthly development loan"
  "SAC|SACCO Development Loan|50000|5000|2000000|24|1|60|1|1|2|10|SACCO long-term development loan"
  "VBL|Village Bank Loan|15000|2000|500000|12|1|36|1|1|3|10|Village-bank (CBO) group loan"
  "WEL|Welfare Emergency Loan|2000|200|50000|6|1|24|1|2|5|20|Welfare / burial emergency loan"
  "JLL|JLG Joint Liability Loan|10000|1000|300000|12|1|52|1|2|8|30|Joint-liability group loan"
)
echo "▶ loan products — ${#LOAN_PRODUCTS[@]} archetypes"
existing_lp="$(api GET /loanproducts | jq -c '[.[]?|{name,id}]' 2>/dev/null)"
lid=""; created=0; skipped=0
for spec in "${LOAN_PRODUCTS[@]}"; do
  IFS='|' read -r sn name pr minp maxp nr minr maxr every freq rate maxrate desc <<< "$spec"
  eid="$(printf '%s' "$existing_lp" | jq -r --arg n "$name" '.[]?|select(.name==$n)|.id' 2>/dev/null | head -1)"
  if [ -n "$eid" ]; then echo "  ✅ '$name' exists (id $eid)"; [ -z "$lid" ] && lid="$eid"; skipped=$((skipped+1)); continue; fi
  resp="$(api POST /loanproducts -d "{
    \"name\":\"$name\",\"shortName\":\"$sn\",
    \"description\":\"MifosSave $desc\",
    \"currencyCode\":\"$APP_CURRENCY\",\"digitsAfterDecimal\":2,\"inMultiplesOf\":0,
    \"principal\":$pr,\"minPrincipal\":$minp,\"maxPrincipal\":$maxp,
    \"numberOfRepayments\":$nr,\"minNumberOfRepayments\":$minr,\"maxNumberOfRepayments\":$maxr,
    \"repaymentEvery\":$every,\"repaymentFrequencyType\":$freq,
    \"interestRatePerPeriod\":$rate,\"minInterestRatePerPeriod\":0,\"maxInterestRatePerPeriod\":$maxrate,\"interestRateFrequencyType\":$freq,
    \"amortizationType\":1,\"interestType\":1,\"interestCalculationPeriodType\":1,
    \"transactionProcessingStrategyCode\":\"mifos-standard-strategy\",
    \"accountingRule\":1,\"daysInYearType\":1,\"daysInMonthType\":1,
    \"isInterestRecalculationEnabled\":false,
    \"locale\":\"en\",\"dateFormat\":\"dd MMMM yyyy\"}")"
  nid="$(printf '%s' "$resp" | jq -r '.resourceId // empty')"
  if [ -n "$nid" ]; then echo "  ✅ created '$name' (id $nid)"; [ -z "$lid" ] && lid="$nid"; created=$((created+1))
  else echo "  ❌ '$name' failed: $(printf '%s' "$resp" | jq -r '.errors[0].defaultUserMessage // .defaultUserMessage // .' 2>/dev/null | head -1)"; rc=1; fi
done
echo "  → loan products: created=$created skipped=$skipped"

echo
[ "$rc" = 0 ] && echo "✅ products ready: KES enabled · savings id ${sid:-?} · loan id ${lid:-?}" \
             || echo "❌ product provisioning had failures (see above)"
exit "$rc"
