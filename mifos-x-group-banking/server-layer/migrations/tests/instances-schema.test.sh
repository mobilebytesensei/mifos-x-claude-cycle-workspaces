#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INST="$DIR/instances.json"
fail=0
# active row (mifos-bank-2) carries render provider + service id
prov=$(jq -r '.instances[] | select(.name=="mifos-bank-2") | .companion_provider // "none"' "$INST")
[ "$prov" = "render" ] || { echo "FAIL: mifos-bank-2 companion_provider=$prov (want render)"; fail=1; }
sid=$(jq -r '.instances[] | select(.name=="mifos-bank-2") | .companion_service_id // ""' "$INST")
[ -n "$sid" ] || { echo "FAIL: mifos-bank-2 missing companion_service_id"; fail=1; }
# legacy row (sandbox, no new fields) defaults to none
sprov=$(jq -r '.instances[] | select(.name=="sandbox") | .companion_provider // "none"' "$INST")
[ "$sprov" = "none" ] || { echo "FAIL: sandbox default provider=$sprov (want none)"; fail=1; }
[ "$fail" = 0 ] && echo "PASS: instances schema"
exit "$fail"
