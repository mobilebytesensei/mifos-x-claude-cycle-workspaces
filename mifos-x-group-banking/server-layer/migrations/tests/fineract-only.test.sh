#!/usr/bin/env bash
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
out="$(FINERACT_BASE_URL=https://127.0.0.1:1/fineract-provider/api/v1 FINERACT_TENANT=t \
       bash "$DIR/provision-instance.sh" --fineract-only --dry-run 2>&1)"; rc=$?
fail=0
# GREEN signal 1: flag is RECOGNIZED — no "unknown arg" error (that is the RED signature, exit 2)
echo "$out" | grep -qiE "unknown arg.*fineract-only" && { echo "FAIL: --fineract-only not recognized (RED)"; fail=1; }
# GREEN signal 2: exit 0 (dry-run of a recognized flag), not the arg-parse exit 2
[ "$rc" = 0 ] || { echo "FAIL: exit=$rc (want 0 for recognized-flag dry-run)"; fail=1; }
# GREEN signal 3: the fineract-only banner/mode line is present (only emitted when the flag gates)
echo "$out" | grep -qi "fineract-only" || { echo "FAIL: no fineract-only mode banner"; fail=1; }
# GREEN signal 4: dry-run plan does NOT advertise the companion phase under fineract-only
echo "$out" | grep -qiE "Phase 3 . companion" && { echo "FAIL: companion phase not skipped"; fail=1; }
[ "$fail" = 0 ] && echo "PASS: fineract-only"
exit "$fail"
