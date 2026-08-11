#!/usr/bin/env bash
# verify-demo-creds.test.sh — provision-instance.sh Phase-5 verify must resolve the demo login
# credentials from the REAL fixture shape (`.demo_accounts[]`), not the non-existent `.demo_user`
# key (fixture-key-mismatch bug: `demo user: null` → guaranteed 401 on every --verify-only run,
# regardless of instance health). Guards the heal.
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PI="$DIR/provision-instance.sh"
FIX="$DIR/seed-demo/demo-fixture.json"
fail=0

# 1) the script must READ creds from .demo_accounts (the real key), not only .demo_user
grep -qE 'demo_accounts\[0\]\.email_phone' "$PI" || { echo "FAIL: provision-instance.sh does not read .demo_accounts[0].email_phone"; fail=1; }
grep -qE 'demo_accounts\[0\]\.password'    "$PI" || { echo "FAIL: provision-instance.sh does not read .demo_accounts[0].password"; fail=1; }

# 2) the resolution the script uses must actually produce non-empty creds against the shipped fixture
DL="$(jq -r '.demo_accounts[0].email_phone // .demo_user.emailPhone // empty' "$FIX" 2>/dev/null)"
DP="$(jq -r '.demo_accounts[0].password  // .demo_user.password  // empty' "$FIX" 2>/dev/null)"
[ -n "$DL" ] || { echo "FAIL: DEMO_LOGIN resolves empty from fixture"; fail=1; }
[ -n "$DP" ] || { echo "FAIL: DEMO_PASS resolves empty from fixture"; fail=1; }

# 2b) the authenticated app-surface calls (groups list) must carry the login token header — the
#     groups-list + members/savings/corpus/loans probes were called WITHOUT "${H[@]}" → 401.
grep -qE 'CB/companion/groups" 2>/dev/null.*|.*"\$\{H\[@\]\}".*CB/companion/groups' "$PI" 2>/dev/null \
  || grep -qE '"\$\{H\[@\]\}" -w .\\n%\{http_code\}. "\$CB/companion/groups"' "$PI" \
  || { echo "FAIL: groups-list verify call missing auth header \${H[@]}"; fail=1; }

# 3) the primary showcase group name must resolve (was reading missing `.group`, fixture has `.groups`)
DG="$(jq -r '(.demo_accounts[0].primary_group_local_id) as $g | (.groups[]? | select(.local_id==$g) | .name) // .groups[0].name // empty' "$FIX" 2>/dev/null)"
[ -n "$DG" ] || { echo "FAIL: DEMO_GROUP resolves empty from fixture"; fail=1; }

[ "$fail" = 0 ] && echo "PASS: verify demo creds resolve from fixture ($DL / group '$DG')"
exit "$fail"
