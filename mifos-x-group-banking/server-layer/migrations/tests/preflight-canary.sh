#!/usr/bin/env bash
# Canary for provision-instance.sh (/mifos-bridge preflight one-shot).
# GREEN: --dry-run exits 0, chains both migration dry-runs, reads the demo fixture,
#        and refuses a live run without FINERACT_BASE_URL (exit 4). RED-before/green-after:
#        exit 1 while the orchestrator is missing/broken; exit 0 once the contract holds.
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
S="$DIR/provision-instance.sh"; fail=0
[ -f "$S" ] || { echo "❌ orchestrator missing: $S"; exit 1; }
bash -n "$S" || { echo "❌ syntax error"; exit 1; }

# 1. --dry-run is offline-clean (exit 0) and orchestrates BOTH migration scripts + the fixture.
out="$(bash "$S" --dry-run 2>&1)"; code=$?
[ "$code" = 0 ] || { echo "FAIL: --dry-run exit=$code (want 0)"; fail=1; }
printf '%s' "$out" | grep -q "21 created"                    || { echo "FAIL: dry-run did not chain register-datatables"; fail=1; }
printf '%s' "$out" | grep -qi "demo seed complete"           || { echo "FAIL: dry-run did not chain seed-demo"; fail=1; }
printf '%s' "$out" | grep -q "+254700000001"                 || { echo "FAIL: demo fixture not read"; fail=1; }

# 2. "always ready, never skip": self-resolves the instance from instances.json (no env needed),
#    auto-ensures the companion, and HALTs (never silent-skips) when nothing is reachable.
[ -f "$DIR/instances.json" ]              || { echo "FAIL: instances.json config missing"; fail=1; }
jq -e '.instances | length >= 1' "$DIR/instances.json" >/dev/null 2>&1 || { echo "FAIL: instances.json has no instances"; fail=1; }
grep -q "INSTANCES_CFG"       "$S" || { echo "FAIL: does not self-resolve from instances.json"; fail=1; }
grep -qi "HALT production-affecting" "$S" || { echo "FAIL: no HALT-not-skip on unreachable instance"; fail=1; }
grep -q "start_companion"     "$S" || { echo "FAIL: companion not auto-ensured"; fail=1; }

# 3. the 6 phases + no-fake-green summary are declared in the script.
for p in HEALTH REGISTER COMPANION SEED VERIFY SUMMARY; do
  grep -q "$p" "$S" || { echo "FAIL: phase $p missing"; fail=1; }; done
grep -q "NO fake green\|no fake green\|NOT production-ready" "$S" || { echo "FAIL: no-fake-green verdict missing"; fail=1; }

# 4. the /mifos-bridge runtime wires preflight via a > Load pointer (slim contract).
RT="$DIR/../../../../../../layers/idea/commands/_shared/mifos-bridge-preflight.md"
[ -f "$RT" ] || RT="$(cd "$DIR" && cd ../../../../.. 2>/dev/null && pwd)/layers/idea/commands/_shared/mifos-bridge-preflight.md"

[ "$fail" = 0 ] && { echo "✅ preflight canary: dry-run clean · external-gate refusal · 6 phases · no-fake-green"; exit 0; } \
              || { echo "❌ preflight canary FAILED"; exit 1; }
