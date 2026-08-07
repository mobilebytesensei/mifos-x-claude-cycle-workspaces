#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
out="$(FINERACT_BASE_URL=https://127.0.0.1:1/fineract-provider/api/v1 FINERACT_TENANT=t \
       bash "$DIR/provision-instance.sh" --fineract-only --dry-run 2>&1 || true)"
# dry-run must acknowledge fineract-only mode and NOT plan the companion phase
echo "$out" | grep -qi "fineract-only" || { echo "FAIL: no fineract-only ack"; exit 1; }
echo "$out" | grep -qiE "Phase 3 — companion" && { echo "FAIL: companion phase not skipped"; exit 1; }
echo "PASS: fineract-only"
