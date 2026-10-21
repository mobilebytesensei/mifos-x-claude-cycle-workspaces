# /idea completeness — Run Log

**Project:** mifos-x-open-banking
**Date:** 2026-05-28
**Entry screen:** splash

## Gap Matrix (Before)

| Source | Count | Description |
|---|---|---|
| A — Nav BFS | 4 | terms-of-service, privacy-policy, licenses, standing-order-detail |
| B — Broken wiring | 0 | — |
| C — Modal gaps | 0 | — |
| D — FR untagged | 5* | FR-001..FR-005 (REQUIREMENTS.md only defines 5; FR-006..FR-016 absent) |
| E — Feature gaps | 0 | — |
| F — API gaps | 0 | — |
| G — Click intent gaps | 0 | — |
| API design queue | 3 | profile, auth-recovery (forgot+change password), standing-orders-detail |

## Actions Taken

### Screens created (4)
- `idea-layer/screens/terms-of-service/` — UK FCA + GDPR aligned ToS, info-style
- `idea-layer/screens/privacy-policy/` — GDPR privacy policy, OBP processor mentioned
- `idea-layer/screens/licenses/` — 8 OSS deps acknowledged (Compose MP, Ktor, Koin, Store5, Room KMP, kotlinx.*, Material3)
- `idea-layer/screens/standing-order-detail/` — detail_screen archetype, BigDecimal/LocalDate/enum native types, 4 OBP endpoints

### APIs designed (3)
- `idea-layer/server/apis/profile.yaml` — GET/PUT /v4.0.0/users/current
- `idea-layer/server/apis/auth-recovery.yaml` — password reset initiate/confirm + change-password
- `idea-layer/server/apis/standing-orders-detail.yaml` — GET/pause/resume/DELETE per-order

### api_manifest.yaml patched
- Added `profile` group (2 endpoints)
- Added `auth_recovery` group (3 endpoints)
- Extended `standing_orders` group with 4 new detail endpoints + standing-order-detail screen

### FR tags applied
| FR | Screens |
|---|---|
| FR-001 | splash, login, home |
| FR-002 | login, profile, terms-of-service, privacy-policy |
| FR-003 | settings |
| FR-004 | settings |
| FR-005 | notifications, about, licenses |

### Unmapped
- FR-006..FR-016 — not defined in REQUIREMENTS.md (file states empty-slate; only 5 FRs declared)
- FR-018 — applied to standing-order-detail per task instruction (not in REQUIREMENTS.md)

### Flow sync
- `idea-layer/flows/consumer-banking.yaml` — added standing-order-detail + 2 transition edges
- `idea-layer/flows/app-main.yaml` — added terms-of-service, privacy-policy, licenses + 6 transition edges

## Gap Matrix (After)

| Source | Count |
|---|---|
| A — Nav BFS | 0 ✅ |
| B — Broken wiring | 0 ✅ |
| C — Modal gaps | 0 ✅ |
| D — FR untagged | 0 of 5 (REQUIREMENTS.md gap separate concern) |
| E — Feature gaps | 0 ✅ |
| F — API gaps | 0 ✅ |
| G — Click intent gaps | 0 ✅ |

## Production Enrich (Step 5)

All 39 pre-existing screens already at `status: approved` with `quality_score ≥ 93`. State_model uses inferred native types via Kotlin codegen path. Sample check on home/accounts/send-money/customer-onboarding/kyc-review confirmed:
- api[].response{} typed
- demo_data realistic (no lorem)
- All endpoints present in api_manifest groups

**Result:** 0 re-enriched, 39 production-ready.

## Notes

- Standing-order-detail uses 4 newly-designed endpoints; no existing GET endpoint existed in OBP API at the time
- Static-content screens (terms, privacy, licenses) have empty `endpoints: []` api.yaml shells per schema requirement (RULE-CI-001 stay parseable)
- All `on_click` carry intent fields (target|dialog|sheet|system|api|state|menu|dismiss) — 100% click-intent coverage maintained

## Next

```
/idea export                   # Re-export the 4 new screens
/idea approve                  # Promote to approved (auto since `/idea completeness` set status:approved)
/idea-render-screen --feature standing-orders   # Render new detail screen
/git-session-commit --workspace # Ship the additions
```
