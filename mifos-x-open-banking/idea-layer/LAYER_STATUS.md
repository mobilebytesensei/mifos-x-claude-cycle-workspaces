# mifos-x-open-banking — Layer Status

> Per-layer enablement + maturity across the 8 framework layers.
> Last updated: 2026-05-22 (empty-slate scaffold)

| Layer | Enabled | Maturity | Source signal |
|---|---|---|---|
| **plan** | ✅ | bootstrap | `idea-plan.yaml` exists (needs refresh post-empty-slate) |
| **idea** | ✅ | scaffold | foundation docs present; product feature scope undefined |
| **design-spec** | ✅ | bootstrap | `design-system/` directory present with tokens, DESIGN.md, COMPONENTS.md, app-shell.yaml |
| **server** | ✅ | observability-only | Firebase Crashlytics + Performance wired; no auth/persistence backend yet |
| **client** | ✅ | bootstrap | Ktorfit + Store5 set up in template; no real repository implementations yet |
| **feature** | ⚠️ | partial | 3 scaffolding modules (home/profile/settings); 3 template modules pending removal |
| **infrastructure** | ✅ | bootstrap | Gradle + KMP + Koin + cmp-navigation in place; CI workflows present |
| **platform** | ✅ | production | All 4 platforms build (cmp-android / cmp-ios / cmp-desktop / cmp-web Wasm+JS) |
| **testing** | ⚠️ | minimal | `kotlin-test` framework present; per-feature test coverage not enforced |
| CAPABILITY_STATE.yaml | ✅ | initialized via /idea init --force (2026-05-27) — 6 capabilities backfilled |

## Next-step matrix

| Layer | Next command | Why |
|---|---|---|
| plan | `/idea-plan` | Define product vision + feature roster (currently empty-slate) |
| idea | `/idea add` per feature | Once plan is set, declare each feature |
| feature | (manual) drop template modules | Remove `feature/{crypto,currency-rates,emi-calculator}` from `settings.gradle.kts` + delete dirs |
| client | `/client {feature}` | Wire repository per real feature |
| testing | `/idea-export-tests` then `/test` | Generate test spec from screen YAMLs |
| server | `/server init` | If product needs auth, DB, or backend |
