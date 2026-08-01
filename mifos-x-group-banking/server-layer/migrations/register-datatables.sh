#!/usr/bin/env bash
# register-datatables.sh — provision all 21 CommonPurse custom datatables on a Fineract instance.
#
# Reads migrations/datatables/datatables.manifest.json and POSTs each definition to
# Fineract `POST /datatables` (the COMP-DT-001 "register" operation). Idempotent: a table
# that already exists (Fineract 403/409 "already registered") is treated as OK and skipped.
#
# THIS IS THE RUNNABLE MIGRATION. It requires a reachable Fineract instance (the external
# gate — see ../COMPANION_API_BUILD_DEPLOY.md §3). Nothing here stands up that instance.
#
# Usage:
#   FINERACT_BASE_URL=https://your-fineract/fineract-provider/api/v1 \
#   FINERACT_USER=mifos FINERACT_PASSWORD=password FINERACT_TENANT=default \
#   bash register-datatables.sh [--dry-run] [--only dt_group_config]
#
# Env:
#   FINERACT_BASE_URL   (required) e.g. https://sandbox.mifos.community/fineract-provider/api/v1
#   FINERACT_USER       (default: mifos)
#   FINERACT_PASSWORD   (default: password)
#   FINERACT_TENANT     (default: default)   -> sent as Fineract-Platform-TenantId header
#   INSECURE=1          pass -k to curl (self-signed sandbox certs)
#
# Requires: bash, curl, jq.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="${SCRIPT_DIR}/datatables/datatables.manifest.json"

FINERACT_BASE_URL="${FINERACT_BASE_URL:-}"
FINERACT_USER="${FINERACT_USER:-mifos}"
FINERACT_PASSWORD="${FINERACT_PASSWORD:-password}"
FINERACT_TENANT="${FINERACT_TENANT:-default}"
DRY_RUN=0
ONLY=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    --only)    ONLY="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

command -v jq >/dev/null   || { echo "FATAL: jq is required" >&2; exit 3; }
command -v curl >/dev/null || { echo "FATAL: curl is required" >&2; exit 3; }
[[ -f "$MANIFEST" ]] || { echo "FATAL: manifest not found: $MANIFEST" >&2; exit 3; }
if [[ "$DRY_RUN" -eq 0 && -z "$FINERACT_BASE_URL" ]]; then
  echo "FATAL: FINERACT_BASE_URL is required (or use --dry-run). This is the external live-server gate." >&2
  exit 4
fi

CURL_OPTS=(-sS --max-time 60)
[[ "${INSECURE:-0}" == "1" ]] && CURL_OPTS+=(-k)

echo "== CommonPurse datatable migration =="
echo "   manifest : $MANIFEST"
echo "   base_url : ${FINERACT_BASE_URL:-<dry-run>}"
echo "   tenant   : $FINERACT_TENANT"
echo "   tables   : $(jq '.datatables | length' "$MANIFEST")"
[[ -n "$ONLY" ]] && echo "   only     : $ONLY"
echo

ok=0; skipped=0; failed=0
count="$(jq '.datatables | length' "$MANIFEST")"
for i in $(seq 0 $((count - 1))); do
  entry="$(jq -c ".datatables[$i]" "$MANIFEST")"
  name="$(echo "$entry" | jq -r '.datatableName')"
  [[ -n "$ONLY" && "$ONLY" != "$name" ]] && continue

  # Build the Fineract POST /datatables payload from the manifest entry.
  payload="$(echo "$entry" | jq '{
    datatableName: .datatableName,
    apptableName: .apptableName,
    entitySubType: .entitySubType,
    multiRow: .multiRow,
    columns: [ .columns[] | {
      name: .name,
      type: .type,
      mandatory: (.mandatory // false)
    } + (if .length then {length: .length} else {} end)
      + (if .code then {code: .code} else {} end) ]
  }')"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[dry-run] would POST /datatables  ->  $name (${entry:0:0}$(echo "$entry" | jq -r '.apptableName'), $(echo "$entry" | jq '.columns | length') cols)"
    ok=$((ok + 1))
    continue
  fi

  http_code="$(curl "${CURL_OPTS[@]}" -o /tmp/dt_resp.$$ -w '%{http_code}' \
    -u "${FINERACT_USER}:${FINERACT_PASSWORD}" \
    -H "Fineract-Platform-TenantId: ${FINERACT_TENANT}" \
    -H "Content-Type: application/json" \
    -X POST "${FINERACT_BASE_URL}/datatables" \
    -d "$payload" || echo "000")"

  body="$(cat /tmp/dt_resp.$$ 2>/dev/null || true)"; rm -f /tmp/dt_resp.$$
  if [[ "$http_code" == "200" ]]; then
    echo "  OK      $name"
    ok=$((ok + 1))
  elif echo "$body" | grep -qiE 'already (registered|exist)'; then
    echo "  SKIP    $name (already registered)"
    skipped=$((skipped + 1))
  else
    echo "  FAIL    $name  (HTTP $http_code): $(echo "$body" | head -c 300)"
    failed=$((failed + 1))
  fi
done

echo
echo "== done: ${ok} created, ${skipped} already-present, ${failed} failed =="
[[ "$failed" -eq 0 ]] || exit 1
