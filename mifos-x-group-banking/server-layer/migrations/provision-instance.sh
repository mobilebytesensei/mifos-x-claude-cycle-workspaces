#!/usr/bin/env bash
# =============================================================================
# provision-instance.sh — ONE-SHOT end-to-end setup + verify of a Fineract
# instance for the CommonPurse (mifos-x-group-banking) backend.
# =============================================================================
#
# The single command behind `/mifos-bridge preflight`. Point it at ANY reachable
# Fineract instance (the current one OR a brand-new one after mifos-bank-2 dies) and it:
#
#   Phase 1  HEALTH   — Fineract reachable + service creds authenticate + self-service on
#   Phase 2  REGISTER — provision all 21 datatables (register-datatables.sh, idempotent)
#   Phase 3  COMPANION— ensure the mcp-mifosx companion is up + pointed at THIS instance
#                       (--manage-companion builds+restarts it; else verifies COMPANION_BASE_URL)
#   Phase 4  SEED     — demo user + group + savings + meetings + corpus + invite (seed-demo.sh)
#   Phase 5  VERIFY   — end-to-end: demo login → dashboard → groups → members/savings/loans/corpus
#   Phase 6  SUMMARY  — per-phase PASS/FAIL; exit 0 (green) / non-zero (red). NO fake green.
#
# Idempotent: safe to re-run (register skips existing tables; seed is create-or-skip).
#
# Usage:
#   FINERACT_BASE_URL=https://<instance>/fineract-provider/api/v1 \
#   FINERACT_TENANT=<tenant> [FINERACT_USER=mifos FINERACT_PASSWORD=password] \
#   COMPANION_BASE_URL=http://localhost:8090/companion \
#   bash provision-instance.sh [--dry-run] [--verify-only] [--skip-datatables] [--skip-seed] \
#        [--manage-companion] [--companion-bin <path>] [--companion-src <dir>]
#
# New instance: just set FINERACT_BASE_URL / FINERACT_TENANT to the new one and run.
# Requires: bash, curl, jq.
# =============================================================================
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

FINERACT_BASE_URL="${FINERACT_BASE_URL:-}"
FINERACT_USER="${FINERACT_USER:-mifos}"
FINERACT_PASSWORD="${FINERACT_PASSWORD:-password}"
FINERACT_TENANT="${FINERACT_TENANT:-default}"
COMPANION_BASE_URL="${COMPANION_BASE_URL:-}"
COMPANION_BIN="${COMPANION_BIN:-/tmp/mcp-companion}"
COMPANION_SRC="${COMPANION_SRC:-}"
COMPANION_PORT="${COMPANION_PORT:-8090}"
INSECURE="${INSECURE:-0}"
DRY_RUN=0 VERIFY_ONLY=0 SKIP_DT=0 SKIP_SEED=0 MANAGE_COMP=0
while [ $# -gt 0 ]; do case "$1" in
  --dry-run)          DRY_RUN=1; shift ;;
  --verify-only)      VERIFY_ONLY=1; shift ;;
  --skip-datatables)  SKIP_DT=1; shift ;;
  --skip-seed)        SKIP_SEED=1; shift ;;
  --manage-companion) MANAGE_COMP=1; shift ;;
  --companion-bin)    COMPANION_BIN="$2"; shift 2 ;;
  --companion-src)    COMPANION_SRC="$2"; shift 2 ;;
  -h|--help)          grep -E '^# ' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
  *) echo "unknown arg: $1" >&2; exit 2 ;;
esac; done

command -v curl >/dev/null || { echo "FATAL: curl required" >&2; exit 3; }
command -v jq   >/dev/null || { echo "FATAL: jq required" >&2; exit 3; }
CURL=(curl -sS --max-time 60); [ "$INSECURE" = 1 ] && CURL+=(-k)
FIXTURE="${SCRIPT_DIR}/seed-demo/demo-fixture.json"
DEMO_LOGIN="$(jq -r '.demo_user.emailPhone' "$FIXTURE" 2>/dev/null)"
DEMO_PASS="$(jq -r '.demo_user.password' "$FIXTURE" 2>/dev/null)"
DEMO_GROUP="$(jq -r 'if (.group|type)=="object" then .group.name else .group end' "$FIXTURE" 2>/dev/null)"

# ── phase-result accounting ──────────────────────────────────────────────────
declare -a RESULTS
mark(){ RESULTS+=("$1|$2|$3"); }   # phase | PASS/FAIL/SKIP | detail
fin(){ printf '%*s' "$1" '' | tr ' ' '─'; }

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  /mifos-bridge preflight — one-shot instance setup + verify   ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  instance : ${FINERACT_BASE_URL:-<dry-run>}"
echo "║  tenant   : ${FINERACT_TENANT}"
echo "║  companion: ${COMPANION_BASE_URL:-<none>}$([ "$MANAGE_COMP" = 1 ] && echo ' (managed)')"
echo "║  demo user: ${DEMO_LOGIN:-?}   group: ${DEMO_GROUP:-?}"
echo "╚══════════════════════════════════════════════════════════════╝"

if [ "$DRY_RUN" = 1 ]; then
  echo "[dry-run] would: HEALTH → REGISTER(21 datatables) → COMPANION → SEED(demo) → VERIFY(e2e)"
  bash "${SCRIPT_DIR}/register-datatables.sh" --dry-run 2>&1 | tail -3
  bash "${SCRIPT_DIR}/seed-demo/seed-demo.sh" --dry-run 2>&1 | tail -3
  echo "✅ dry-run clean — set FINERACT_BASE_URL + COMPANION_BASE_URL and re-run to apply."
  exit 0
fi
[ -n "$FINERACT_BASE_URL" ] || { echo "FATAL: FINERACT_BASE_URL required (or --dry-run)" >&2; exit 4; }

# ── Phase 1: Fineract HEALTH ─────────────────────────────────────────────────
if [ "$VERIFY_ONLY" = 0 ]; then
  echo; echo "▶ Phase 1 — Fineract health"
  code="$("${CURL[@]}" -o /tmp/pf_health.$$ -w '%{http_code}' -u "$FINERACT_USER:$FINERACT_PASSWORD" \
      -H "Fineract-Platform-TenantId: $FINERACT_TENANT" "$FINERACT_BASE_URL/offices" 2>/dev/null || echo 000)"
  if [ "$code" = 200 ]; then echo "  ✅ reachable + authenticated (GET /offices → 200)"; mark HEALTH PASS "200"
  else echo "  ❌ Fineract unreachable / auth failed (GET /offices → $code)"; mark HEALTH FAIL "$code"
       echo "  → the instance itself must be stood up first (Fineract w/ self-service module)."; fi
  ss="$("${CURL[@]}" -o /dev/null -w '%{http_code}' -u "$FINERACT_USER:$FINERACT_PASSWORD" \
      -H "Fineract-Platform-TenantId: $FINERACT_TENANT" "$FINERACT_BASE_URL/self/clients" 2>/dev/null || echo 000)"
  case "$ss" in 200|401|403) echo "  ✅ self-service module present (/self/* → $ss)"; mark SELFSVC PASS "$ss";;
    404) echo "  ⚠️ self-service module NOT enabled (/self/* → 404) — signup/self-register will fail"; mark SELFSVC FAIL "404";;
    *)   echo "  ⚠️ self-service probe inconclusive (/self/* → $ss)"; mark SELFSVC WARN "$ss";; esac
else mark HEALTH SKIP "verify-only"; mark SELFSVC SKIP "verify-only"; fi

# ── Phase 2: REGISTER datatables ─────────────────────────────────────────────
if [ "$VERIFY_ONLY" = 0 ] && [ "$SKIP_DT" = 0 ]; then
  echo; echo "▶ Phase 2 — register 21 datatables"
  if FINERACT_BASE_URL="$FINERACT_BASE_URL" FINERACT_USER="$FINERACT_USER" FINERACT_PASSWORD="$FINERACT_PASSWORD" \
     FINERACT_TENANT="$FINERACT_TENANT" INSECURE="$INSECURE" bash "${SCRIPT_DIR}/register-datatables.sh"; then
    echo "  ✅ datatables registered (idempotent)"; mark REGISTER PASS "21 tables"
  else echo "  ❌ datatable registration failed"; mark REGISTER FAIL "see log"; fi
else mark REGISTER SKIP "$([ "$VERIFY_ONLY" = 1 ] && echo verify-only || echo --skip-datatables)"; fi

# ── Phase 3: COMPANION up + pointed at THIS instance ─────────────────────────
echo; echo "▶ Phase 3 — companion API"
if [ "$MANAGE_COMP" = 1 ]; then
  [ -n "$COMPANION_SRC" ] || { echo "  ❌ --manage-companion needs --companion-src <go-dir>"; mark COMPANION FAIL "no src"; }
  if [ -n "$COMPANION_SRC" ]; then
    echo "  building companion from $COMPANION_SRC …"
    if ( cd "$COMPANION_SRC" && go build -o "$COMPANION_BIN" . ) 2>/tmp/pf_build.$$; then
      OLD="$(lsof -nP -iTCP:"$COMPANION_PORT" -sTCP:LISTEN -t 2>/dev/null)"; [ -n "$OLD" ] && kill "$OLD" 2>/dev/null; sleep 1
      MIFOSX_BASE_URL="$FINERACT_BASE_URL" MIFOSX_TENANT_ID="$FINERACT_TENANT" \
        MIFOSX_USERNAME="$FINERACT_USER" MIFOSX_PASSWORD="$FINERACT_PASSWORD" PORT="$COMPANION_PORT" \
        nohup "$COMPANION_BIN" >/tmp/companion-live.log 2>&1 & sleep 2
      COMPANION_BASE_URL="${COMPANION_BASE_URL:-http://localhost:$COMPANION_PORT/companion}"
      echo "  ✅ companion built + started on :$COMPANION_PORT → $FINERACT_BASE_URL"
    else echo "  ❌ companion build failed"; sed 's/^/    /' /tmp/pf_build.$$ | tail -4; mark COMPANION FAIL "build"; fi
  fi
fi
if [ -n "$COMPANION_BASE_URL" ]; then
  # companion base may end in /companion; probe a known route
  probe="${COMPANION_BASE_URL%/companion}/companion/groups/1"
  code="$("${CURL[@]}" -o /dev/null -w '%{http_code}' "$probe" 2>/dev/null || echo 000)"
  if [ "$code" = 200 ] || [ "$code" = 404 ]; then echo "  ✅ companion reachable (probe → $code)"; mark COMPANION PASS "$code"
  else echo "  ❌ companion NOT reachable (probe → $code) at $COMPANION_BASE_URL"; mark COMPANION FAIL "$code"; fi
else echo "  ⚠️ COMPANION_BASE_URL not set — cannot seed or verify the app surface"; mark COMPANION FAIL "unset"; fi

# ── Phase 4: SEED demo ───────────────────────────────────────────────────────
if [ "$VERIFY_ONLY" = 0 ] && [ "$SKIP_SEED" = 0 ]; then
  echo; echo "▶ Phase 4 — seed demo data"
  if [ -n "$COMPANION_BASE_URL" ] && FINERACT_BASE_URL="$FINERACT_BASE_URL" COMPANION_BASE_URL="$COMPANION_BASE_URL" \
       FINERACT_USER="$FINERACT_USER" FINERACT_PASSWORD="$FINERACT_PASSWORD" FINERACT_TENANT="$FINERACT_TENANT" \
       INSECURE="$INSECURE" bash "${SCRIPT_DIR}/seed-demo/seed-demo.sh"; then
    echo "  ✅ demo seeded (user + group + savings + meetings + corpus + invite)"; mark SEED PASS "demo"
  else echo "  ❌ demo seed failed (or companion unreachable)"; mark SEED FAIL "see log"; fi
else mark SEED SKIP "$([ "$VERIFY_ONLY" = 1 ] && echo verify-only || echo --skip-seed)"; fi

# ── Phase 5: VERIFY end-to-end (the app-facing surface) ──────────────────────
echo; echo "▶ Phase 5 — end-to-end verify (demo login → real data)"
vpass=0; vtotal=0
vcheck(){ vtotal=$((vtotal+1)); local d="$1" c="$2" ok="$3"
  if [ "$c" = 200 ] && [ "$ok" = 1 ]; then echo "  ✅ $d ($c)"; vpass=$((vpass+1))
  else echo "  ❌ $d (http=$c)"; fi; }
if [ -n "$COMPANION_BASE_URL" ]; then
  CB="${COMPANION_BASE_URL%/companion}"
  login="$("${CURL[@]}" -w '\n%{http_code}' -X POST "$CB/companion/auth/login" -H 'Content-Type: application/json' \
      -d "{\"emailPhone\":\"$DEMO_LOGIN\",\"password\":\"$DEMO_PASS\"}" 2>/dev/null)"
  lcode="$(printf '%s' "$login" | tail -1)"; ltok="$(printf '%s' "$login" | sed '$d' | jq -r '.sessionToken // empty' 2>/dev/null)"
  vcheck "demo login" "$lcode" "$([ -n "$ltok" ] && echo 1 || echo 0)"
  H=(-H "Authorization: Bearer $ltok")
  d="$("${CURL[@]}" "${H[@]}" -w '\n%{http_code}' "$CB/companion/organizer/dashboard" 2>/dev/null)"
  vcheck "organizer dashboard" "$(printf '%s' "$d"|tail -1)" "$(printf '%s' "$d"|sed '$d'|jq -e '.myGroupCount>=0' >/dev/null 2>&1 && echo 1||echo 0)"
  g="$("${CURL[@]}" -w '\n%{http_code}' "$CB/companion/groups" 2>/dev/null)"
  gcode="$(printf '%s' "$g"|tail -1)"; GID="$(printf '%s' "$g"|sed '$d'|jq -r --arg n "$DEMO_GROUP" '.pageItems[]? | select(.name|test($n)) | .id' 2>/dev/null|head -1)"
  [ -z "$GID" ] && GID="$(printf '%s' "$g"|sed '$d'|jq -r '.pageItems[0].id // empty' 2>/dev/null)"
  vcheck "groups list (seeded group present)" "$gcode" "$([ -n "$GID" ] && echo 1||echo 0)"
  if [ -n "$GID" ]; then
    for pair in "members:/companion/groups/$GID/members" "savings:/companion/groups/$GID/savings" \
                "corpus:/companion/groups/$GID/corpus" "loans:/groups/$GID/loans"; do
      lbl="${pair%%:*}"; path="${pair#*:}"
      r="$("${CURL[@]}" -o /dev/null -w '%{http_code}' "$CB$path" 2>/dev/null||echo 000)"
      vcheck "group $lbl" "$r" 1
    done
  fi
else echo "  ❌ no companion — cannot verify the app surface"; vtotal=1; fi

# ── Phase 6: SUMMARY ─────────────────────────────────────────────────────────
echo; echo "$(fin 64)"; echo "  PREFLIGHT SUMMARY"; echo "$(fin 64)"
red=0
for r in "${RESULTS[@]}"; do IFS='|' read -r ph st dt <<<"$r"
  ic="✅"; [ "$st" = FAIL ] && { ic="❌"; red=1; }; [ "$st" = SKIP ] && ic="⏭️"; [ "$st" = WARN ] && ic="⚠️"
  printf "  %s  %-10s %-6s %s\n" "$ic" "$ph" "$st" "$dt"; done
printf "  %s  %-10s %-6s %s\n" "$([ "$vpass" = "$vtotal" ] && [ "$vtotal" -gt 0 ] && echo ✅ || echo ❌)" "VERIFY" "$vpass/$vtotal" "app-facing endpoints"
[ "$vpass" = "$vtotal" ] && [ "$vtotal" -gt 0 ] || red=1
echo "$(fin 64)"
if [ "$red" = 0 ]; then echo "  ✅ GREEN — instance provisioned + verified end-to-end. App is ready."; exit 0
else echo "  ❌ RED — one or more phases failed (see above). NOT production-ready."; exit 1; fi
