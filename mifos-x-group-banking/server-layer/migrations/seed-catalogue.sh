#!/usr/bin/env bash
# seed-catalogue.sh — seed the 9-archetype GROUP-TYPE CATALOGUE on Fineract (server-side SoT).
#
# The group-type picker needs a list of 9 archetypes to choose from BEFORE a group exists. This is a
# FIXED registry (ARCHITECTURE.md §4), not per-group config. Native Fineract has no global-catalogue
# concept, so we:
#   1. register a dedicated MULTI-ROW datatable `dt_group_type_catalogue` on m_group whose columns
#      EXACTLY match the app's GroupTypeConfigDto @SerialName keys (Fineract preserves camelCase),
#      so the app deserializes the raw datatable response with NO mapper;
#   2. create ONE anchor group (`_MifosSave Type Catalogue`) to hang the 9 catalogue rows on;
#   3. seed the 9 archetype rows (VSLA, ROSCA, ASCA, SILC, SHG, SACCO, CBO_VILLAGE_BANK,
#      BURIAL_WELFARE, JLG).
# The app reads GET /datatables/dt_group_type_catalogue/{anchorGroupId} → List<GroupTypeConfigDto>.
#
# Idempotent: re-register skips if present; anchor reused by name; rows re-posted (dupes tolerable for
# a catalogue read, but we clear first).
#
# Env: FINERACT_BASE_URL FINERACT_TENANT (FINERACT_USER=mifos FINERACT_PASSWORD=password)
set -uo pipefail
BASE="${FINERACT_BASE_URL:?}"; TEN="${FINERACT_TENANT:?}"
U="${FINERACT_USER:-mifos}"; P="${FINERACT_PASSWORD:-password}"
AUTH="$(printf '%s:%s' "$U" "$P" | base64)"
H=(-H "Fineract-Platform-TenantId: $TEN" -H "Authorization: Basic $AUTH" -H "Content-Type: application/json")
j() { curl -s --max-time 30 "${H[@]}" "$@"; }

TABLE="dt_group_type_catalogue"

echo "== 1. register $TABLE (multi-row, camelCase cols = GroupTypeConfigDto keys) =="
EXISTS="$(j "$BASE/datatables" | grep -o "\"$TABLE\"" | head -1)"
if [ -z "$EXISTS" ]; then
  j -X POST "$BASE/datatables" -d '{
    "datatableName":"'"$TABLE"'","apptableName":"m_group","entitySubType":"GROUP","multiRow":true,
    "columns":[
      {"name":"typeSlug","type":"string","length":40,"mandatory":true},
      {"name":"displayName","type":"string","length":80,"mandatory":true},
      {"name":"tagline","type":"string","length":160,"mandatory":false},
      {"name":"savingsMechanism","type":"string","length":30,"mandatory":false},
      {"name":"contributionMode","type":"string","length":30,"mandatory":false},
      {"name":"lendingEnabled","type":"boolean","mandatory":false},
      {"name":"hasSocialFund","type":"boolean","mandatory":false},
      {"name":"hasBankLinkage","type":"boolean","mandatory":false},
      {"name":"welfareOnlyMode","type":"boolean","mandatory":false},
      {"name":"formallyRegistered","type":"boolean","mandatory":false},
      {"name":"defaultLoanMultiplier","type":"decimal","mandatory":false},
      {"name":"defaultInterestRatePct","type":"decimal","mandatory":false},
      {"name":"defaultCycleLengthMonths","type":"number","mandatory":false},
      {"name":"maxMembers","type":"number","mandatory":false},
      {"name":"minMembers","type":"number","mandatory":false}
    ]}' -w " [%{http_code}]\n" | tail -c 80
else echo "   already registered"; fi

echo "== 2. anchor group (_MifosSave Type Catalogue) =="
ANCHOR="$(j "$BASE/groups?limit=200" | python3 -c "
import json,sys
d=json.load(sys.stdin); items=d.get('pageItems',d) if isinstance(d,dict) else d
print(next((g['id'] for g in items if g.get('name')=='_MifosSave Type Catalogue'), ''))" 2>/dev/null)"
if [ -z "$ANCHOR" ]; then
  ANCHOR="$(j -X POST "$BASE/groups" -d '{"name":"_MifosSave Type Catalogue","officeId":1,"active":true,"activationDate":"2026-08-01","locale":"en","dateFormat":"yyyy-MM-dd"}' | python3 -c "import json,sys;print(json.load(sys.stdin).get('groupId') or json.load(sys.stdin).get('resourceId',''))" 2>/dev/null)"
  # groupId key name varies; re-read if empty
  [ -z "$ANCHOR" ] && ANCHOR="$(j "$BASE/groups?limit=200" | python3 -c "
import json,sys
d=json.load(sys.stdin); items=d.get('pageItems',d) if isinstance(d,dict) else d
print(next((g['id'] for g in items if g.get('name')=='_MifosSave Type Catalogue'), ''))" 2>/dev/null)"
fi
echo "   anchor groupId = $ANCHOR"
[ -z "$ANCHOR" ] && { echo "FATAL: no anchor group id"; exit 1; }

echo "== 3. clear + seed 9 archetype rows onto anchor $ANCHOR =="
# clear existing catalogue rows (multi-row): delete all for this apptable id
j -X DELETE "$BASE/datatables/$TABLE/$ANCHOR" >/dev/null 2>&1 || true
seed_row() { # $1=json body
  j -X POST "$BASE/datatables/$TABLE/$ANCHOR" -d "$1" -w " [%{http_code}]" | tail -c 30; echo
}
# typeSlug|displayName|tagline|savingsMechanism|contributionMode|lending|social|bank|welfare|formal|loanMult|intPct|cycleMo|max|min
seed_row '{"typeSlug":"VSLA","displayName":"VSLA","tagline":"Village Savings & Loan — buy shares, borrow up to 3x, share out yearly","savingsMechanism":"ACCUMULATING","contributionMode":"SHARE_BASED_VARIABLE","lendingEnabled":true,"hasSocialFund":true,"hasBankLinkage":false,"welfareOnlyMode":false,"formallyRegistered":false,"defaultLoanMultiplier":3,"defaultInterestRatePct":2,"defaultCycleLengthMonths":12,"maxMembers":30,"minMembers":10,"locale":"en","dateFormat":"yyyy-MM-dd"}'
seed_row '{"typeSlug":"ROSCA","displayName":"ROSCA","tagline":"Rotating pot — everyone pays in, one member takes the pot each meeting","savingsMechanism":"ROTATING_PAYOUT","contributionMode":"FIXED","lendingEnabled":false,"hasSocialFund":false,"hasBankLinkage":false,"welfareOnlyMode":false,"formallyRegistered":false,"defaultLoanMultiplier":0,"defaultInterestRatePct":0,"defaultCycleLengthMonths":12,"maxMembers":20,"minMembers":5,"locale":"en","dateFormat":"yyyy-MM-dd"}'
seed_row '{"typeSlug":"ASCA","displayName":"ASCA","tagline":"Accumulating Savings & Credit — pool grows, lent at interest","savingsMechanism":"ACCUMULATING","contributionMode":"FIXED","lendingEnabled":true,"hasSocialFund":false,"hasBankLinkage":false,"welfareOnlyMode":false,"formallyRegistered":false,"defaultLoanMultiplier":3,"defaultInterestRatePct":2,"defaultCycleLengthMonths":12,"maxMembers":30,"minMembers":10,"locale":"en","dateFormat":"yyyy-MM-dd"}'
seed_row '{"typeSlug":"SILC","displayName":"SILC","tagline":"Savings & Internal Lending Communities (CRS) — shares + internal loans","savingsMechanism":"ACCUMULATING","contributionMode":"SHARE_BASED_VARIABLE","lendingEnabled":true,"hasSocialFund":true,"hasBankLinkage":false,"welfareOnlyMode":false,"formallyRegistered":false,"defaultLoanMultiplier":3,"defaultInterestRatePct":2,"defaultCycleLengthMonths":12,"maxMembers":30,"minMembers":10,"locale":"en","dateFormat":"yyyy-MM-dd"}'
seed_row '{"typeSlug":"SHG","displayName":"Self-Help Group","tagline":"Save, lend internally, and link to a bank for external credit","savingsMechanism":"ACCUMULATING","contributionMode":"FIXED","lendingEnabled":true,"hasSocialFund":true,"hasBankLinkage":true,"welfareOnlyMode":false,"formallyRegistered":false,"defaultLoanMultiplier":4,"defaultInterestRatePct":2,"defaultCycleLengthMonths":12,"maxMembers":20,"minMembers":10,"locale":"en","dateFormat":"yyyy-MM-dd"}'
seed_row '{"typeSlug":"SACCO","displayName":"SACCO / Credit Union","tagline":"Share capital, elected board, formally registered & regulated","savingsMechanism":"ACCUMULATING","contributionMode":"FIXED","lendingEnabled":true,"hasSocialFund":false,"hasBankLinkage":false,"welfareOnlyMode":false,"formallyRegistered":true,"defaultLoanMultiplier":3,"defaultInterestRatePct":1,"defaultCycleLengthMonths":12,"maxMembers":200,"minMembers":10,"locale":"en","dateFormat":"yyyy-MM-dd"}'
seed_row '{"typeSlug":"CBO_VILLAGE_BANK","displayName":"Village Bank / CBO","tagline":"An MFI on-lends alongside the internal group savings","savingsMechanism":"ACCUMULATING","contributionMode":"FIXED","lendingEnabled":true,"hasSocialFund":false,"hasBankLinkage":true,"welfareOnlyMode":false,"formallyRegistered":false,"defaultLoanMultiplier":3,"defaultInterestRatePct":2,"defaultCycleLengthMonths":12,"maxMembers":40,"minMembers":10,"locale":"en","dateFormat":"yyyy-MM-dd"}'
seed_row '{"typeSlug":"BURIAL_WELFARE","displayName":"Burial / Welfare Society","tagline":"A shared fund for emergencies & funerals — the fund IS the purpose","savingsMechanism":"ACCUMULATING","contributionMode":"FIXED","lendingEnabled":false,"hasSocialFund":true,"hasBankLinkage":false,"welfareOnlyMode":true,"formallyRegistered":false,"defaultLoanMultiplier":0,"defaultInterestRatePct":0,"defaultCycleLengthMonths":12,"maxMembers":100,"minMembers":10,"locale":"en","dateFormat":"yyyy-MM-dd"}'
seed_row '{"typeSlug":"JLG","displayName":"Joint Liability Group","tagline":"Mutual-guarantee group for an external MFI loan (Grameen-style)","savingsMechanism":"NONE","contributionMode":"MINIMAL","lendingEnabled":false,"hasSocialFund":false,"hasBankLinkage":true,"welfareOnlyMode":false,"formallyRegistered":false,"defaultLoanMultiplier":0,"defaultInterestRatePct":0,"defaultCycleLengthMonths":12,"maxMembers":10,"minMembers":4,"locale":"en","dateFormat":"yyyy-MM-dd"}'

echo "== 4. verify: read back the catalogue =="
CNT="$(j "$BASE/datatables/$TABLE/$ANCHOR" | python3 -c "import json,sys;print(len(json.load(sys.stdin)))" 2>/dev/null)"
echo "   catalogue rows on anchor $ANCHOR: $CNT"
echo "ANCHOR_GROUP_ID=$ANCHOR"
