#!/usr/bin/env bash
# =============================================================================
# register-products.sh — idempotent provisioning of the CommonPurse VSLA
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
#   3. A KES loan product     — "VSLA Group Loan"    — what the loan-apply flow
#      applies against (3x savings, weekly repayment, flat interest).
#
# ONE loan + ONE savings product serve ALL group types (VSLA/ROSCA/ASCA/SILC/
# SHG): the group TYPE differences (pool model, share value, cycle) live in the
# companion's dt_group_type_config datatable + app logic, not in separate
# Fineract products — a member borrows/saves as an individual client under the
# group regardless of type, so one shared product per operation is correct and
# avoids product sprawl.
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
    \"description\":\"CommonPurse VSLA group-linked savings\",
    \"currencyCode\":\"$APP_CURRENCY\",\"digitsAfterDecimal\":2,\"inMultiplesOf\":0,
    \"nominalAnnualInterestRate\":0,\"interestCompoundingPeriodType\":1,
    \"interestPostingPeriodType\":4,\"interestCalculationType\":1,
    \"interestCalculationDaysInYearType\":365,\"accountingRule\":1,\"locale\":\"en\"}")"
  sid="$(printf '%s' "$resp" | jq -r '.resourceId // empty')"
  if [ -n "$sid" ]; then echo "  ✅ created (id $sid)"
  else echo "  ❌ create failed: $(printf '%s' "$resp" | jq -r '.errors[0].defaultUserMessage // .defaultUserMessage // .' 2>/dev/null | head -1)"; rc=1; fi
fi

# ── 3. VSLA loan product (create-or-skip) ────────────────────────────────────
LOAN_NAME="VSLA Group Loan"
echo "▶ loan product — '$LOAN_NAME'"
lid="$(api GET /loanproducts | jq -r --arg n "$LOAN_NAME" '.[]?|select(.name==$n)|.id' 2>/dev/null | head -1)"
if [ -n "$lid" ]; then echo "  ✅ exists (id $lid)"
else
  resp="$(api POST /loanproducts -d "{
    \"name\":\"$LOAN_NAME\",\"shortName\":\"VGL\",
    \"description\":\"CommonPurse VSLA group loan (3x savings, weekly repayment)\",
    \"currencyCode\":\"$APP_CURRENCY\",\"digitsAfterDecimal\":2,\"inMultiplesOf\":0,
    \"principal\":5000,\"minPrincipal\":500,\"maxPrincipal\":300000,
    \"numberOfRepayments\":12,\"minNumberOfRepayments\":1,\"maxNumberOfRepayments\":52,
    \"repaymentEvery\":1,\"repaymentFrequencyType\":2,
    \"interestRatePerPeriod\":10,\"minInterestRatePerPeriod\":0,\"maxInterestRatePerPeriod\":30,\"interestRateFrequencyType\":2,
    \"amortizationType\":1,\"interestType\":1,\"interestCalculationPeriodType\":1,
    \"transactionProcessingStrategyCode\":\"mifos-standard-strategy\",
    \"accountingRule\":1,\"daysInYearType\":1,\"daysInMonthType\":1,
    \"isInterestRecalculationEnabled\":false,
    \"locale\":\"en\",\"dateFormat\":\"dd MMMM yyyy\"}")"
  lid="$(printf '%s' "$resp" | jq -r '.resourceId // empty')"
  if [ -n "$lid" ]; then echo "  ✅ created (id $lid)"
  else echo "  ❌ create failed: $(printf '%s' "$resp" | jq -r '.errors[0].defaultUserMessage // .defaultUserMessage // .' 2>/dev/null | head -1)"; rc=1; fi
fi

echo
[ "$rc" = 0 ] && echo "✅ products ready: KES enabled · savings id ${sid:-?} · loan id ${lid:-?}" \
             || echo "❌ product provisioning had failures (see above)"
exit "$rc"
