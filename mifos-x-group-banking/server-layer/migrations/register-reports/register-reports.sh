#!/usr/bin/env bash
# Register the Fineract "stretchy" reports the MifosSave app runs via GET /runreports/<name>.
#
# Today: FieldOfficerGroupReport — the field-officer dashboard's CSV/PDF EXPORT action
# (companion GET /companion/field-officer/report -> Fineract GET /runreports/FieldOfficerGroupReport
# ?R_staffId=&output-type=CSV). The dashboard itself is built from GET /groups and works without this;
# this closes the export gap (previously 5xx "Reporting meta-data entry not found").
#
# Idempotent: skips a report that already exists. Run once per Fineract instance.
#
# Usage:
#   FINERACT_BASE_URL=https://mifos-bank-2.mifos.community/fineract-provider/api/v1 \
#   FINERACT_USER=mifos FINERACT_PASSWORD=password FINERACT_TENANT=mifos-bank-2 \
#   bash register-reports.sh
#
# Env:
#   FINERACT_BASE_URL   (required)  Fineract API root
#   FINERACT_USER / FINERACT_PASSWORD / FINERACT_TENANT   (defaults mifos/password/mifos-bank-2)
#   INSECURE=1          pass -k to curl (self-signed certs)
#   --dry-run           print the plan, make no calls
set -euo pipefail

FINERACT_BASE_URL="${FINERACT_BASE_URL:-https://mifos-bank-2.mifos.community/fineract-provider/api/v1}"
FINERACT_USER="${FINERACT_USER:-mifos}"
FINERACT_PASSWORD="${FINERACT_PASSWORD:-password}"
FINERACT_TENANT="${FINERACT_TENANT:-mifos-bank-2}"
DRY_RUN=0; [[ "${1:-}" == "--dry-run" ]] && DRY_RUN=1

CURL_OPTS=(-sS --max-time 60)
[[ "${INSECURE:-0}" == "1" ]] && CURL_OPTS+=(-k)
command -v curl >/dev/null || { echo "FATAL: curl required" >&2; exit 3; }
command -v jq   >/dev/null || { echo "FATAL: jq required" >&2; exit 3; }

fin() { # fin METHOD PATH [json-body]
  local m="$1" p="$2" body="${3:-}"
  local args=(-u "${FINERACT_USER}:${FINERACT_PASSWORD}" -H "Fineract-Platform-TenantId: ${FINERACT_TENANT}" -H "Content-Type: application/json" -X "$m")
  [[ -n "$body" ]] && args+=(-d "$body")
  curl "${CURL_OPTS[@]}" "${args[@]}" "${FINERACT_BASE_URL}${p}"
}

# Field-officer group report SQL.
#  - mifos-bank-2 Fineract is PostgreSQL: double-quote column aliases, COALESCE (not IFNULL).
#  - The staff filter uses the stock `loanOfficerIdSelectAll` parameter (id 6): SQL var
#    ${loanOfficerId}, run-param R_loanOfficerId. Fineract only substitutes a ${var} that is a
#    DECLARED report parameter — so the parameter MUST be attached (see FO_PARAM_ID below), else the
#    literal ${loanOfficerId} reaches Postgres and errors. A group's staff IS its loan officer; the
#    companion translates the app's R_staffId -> R_loanOfficerId.
#  - status_enum / loan_status_id 300 = ACTIVE.
FO_PARAM_ID=6           # stock stretchy parameter: loanOfficerIdSelectAll
FO_PARAM_NAME=loanOfficerId
read -r -d '' FO_SQL <<'SQL' || true
SELECT
  g.id                                       AS "Group ID",
  g.display_name                             AS "Group Name",
  COALESCE(o.name, '')                       AS "Office",
  (SELECT COUNT(*) FROM m_group_client gc WHERE gc.group_id = g.id)                                                             AS "Members",
  COALESCE((SELECT SUM(sa.account_balance_derived) FROM m_savings_account sa WHERE sa.group_id = g.id AND sa.status_enum = 300), 0)  AS "Total Savings",
  COALESCE((SELECT SUM(l.total_outstanding_derived) FROM m_loan l WHERE l.group_id = g.id AND l.loan_status_id = 300), 0)           AS "Loans Outstanding"
FROM m_group g
LEFT JOIN m_office o ON o.id = g.office_id
WHERE g.staff_id = ${loanOfficerId}
ORDER BY g.display_name
SQL

register_report() {
  local name="$1" category="$2" desc="$3" sql="$4" paramId="$5" paramName="$6"
  # reportParameters attaches the declared param so Fineract substitutes ${paramName} at run time.
  local params='[]'
  [[ -n "$paramId" ]] && params="$(jq -nc --argjson pid "$paramId" --arg pn "$paramName" '[{parameterId:$pid, reportParameterName:$pn}]')"
  local body
  body="$(jq -nc --arg n "$name" --arg t "Table" --arg c "$category" --arg d "$desc" --arg s "$sql" --argjson p "$params" \
    '{reportName:$n, reportType:$t, reportCategory:$c, useReport:true, description:$d, reportSql:$s, reportParameters:$p}')"
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "   [dry-run] upsert report ($name)"; echo "$body" | jq -r '.reportSql' | sed 's/^/       /'
    return 0
  fi
  # Upsert: PUT to update an existing report (fixes SQL drift on re-run), else POST to create.
  local existing
  existing="$(fin GET "/reports" | jq -r --arg n "$name" '.[]? | select(.reportName==$n) | .id' 2>/dev/null | head -1)"
  if [[ -n "$existing" ]]; then
    # If the parameter is already attached, PUT only the SQL/description — re-sending reportParameters
    # would violate report_parameter_unique (report_id, parameter_id).
    local already="0"
    [[ -n "$paramId" ]] && already="$(fin GET "/reports/$existing" | jq -r --argjson pid "$paramId" '((.reportParameters//[])|any(.parameterId==$pid))' 2>/dev/null)"
    local ubody="$body"
    [[ "$already" == "true" ]] && ubody="$(jq -nc --arg d "$desc" --arg s "$sql" '{description:$d, reportSql:$s}')"
    local up; up="$(fin PUT "/reports/$existing" "$ubody")"
    echo "$up" | jq -e '.resourceId' >/dev/null 2>&1 && echo "   [ok] updated '$name' (id=$existing, param-attached=$already)" || { echo "   [FAIL] update '$name': $up" >&2; return 1; }
  else
    local resp; resp="$(fin POST "/reports" "$body")"
    local rid; rid="$(echo "$resp" | jq -r '.resourceId // empty' 2>/dev/null)"
    [[ -n "$rid" ]] && echo "   [ok] registered '$name' (id=$rid)" || { echo "   [FAIL] '$name': $resp" >&2; return 1; }
  fi
}

echo ">> Fineract: ${FINERACT_BASE_URL}  tenant: ${FINERACT_TENANT}  (dry-run=${DRY_RUN})"
register_report "FieldOfficerGroupReport" "Client" \
  "Groups managed by a field officer (staff) with member / savings / loan KPIs. Run: /runreports/FieldOfficerGroupReport?R_loanOfficerId={staffId}&output-type=CSV|PDF|JSON (the companion translates the app's R_staffId)." \
  "$FO_SQL" "$FO_PARAM_ID" "$FO_PARAM_NAME"
echo ">> done"
