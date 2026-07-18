# Reference audit — openMF/mifos-x-field-officer-app (fresh-build reference only)

> Ground truth from the repo's `dev` branch (default; `main`=release). Root Gradle project is literally `"AndroidClient"` — the KMP/CMP rewrite of legacy `openMF/android-client`. MPL-2.0. **We build fresh; this is reference for feature IDEAS + patterns, not code.** GitHub topics saying Retrofit/Hilt/MVVM are stale — the dev build is Ktor/Ktorfit/Koin.

## What it is (validates our stack)
KMP + **Compose Multiplatform 1.9.3**, Kotlin **2.2.21**; targets Android/iOS/Desktop/JS/WasmJS (Android is the production target). **Koin 4.1** (annotations/KSP), **Ktor 3.3 + Ktorfit 2.7** + the **Fineract Client KMP SDK 0.0.1** (generated), **Room 2.8 (KMP)** offline, JetBrains Navigation Compose (type-safe routes, adaptive BottomBar↔NavigationRail), MVVM/MVI per screen, `core-base` vs `core` split. **Same architecture family as openMF/kmp-project-template** → our template choice is well-aligned.

## Module inventory (21 feature modules — field-ops subset)
`auth · passcode (biometrics) · client (full lifecycle: list/details/profile/edit/addresses/identifiers/documents/signature/collateral/charges/closure/GPS) · center · groups · loan (20 screens) · savings (+v2 rewrite) · recurringDeposit (view-only) · collectionSheet · checker-inbox-task · data-table · document · note · activate · search · search-record · report · path-tracking (GPS) · offline (dashboard + per-aggregate sync) · settings (+UpdateServerConfig) · about`.
Nav shell: Splash → Login → passcode/biometrics → adaptive navbar. **Bottom tabs: Search / Clients / Centers / Groups.** Home destinations: Checker Inbox, Collection Sheet, Run Reports, Path Tracker, Settings, About, Offline Sync.

## Fineract coverage (a deliberate SUBSET)
**Consumes:** auth, clients, groups, centers, offices+staff (read), loans (deep lifecycle), savings, FD/share (network-only, no screens), recurring deposit (view), charges, collection sheets, checker-inbox, datatables, documents, notes, run-reports, search, surveys (network+DB, sync-dialog only).
**Does NOT consume (the whole generic-back-office delta we add):** accounting/GL · users/roles/permissions · product admin · tellers/cashiers · scheduler/jobs · global config · holidays/working-days · payment types/funds/currencies admin · campaigns/notifications · audit trails · standing instructions · tax/floating-rates/provisioning · batch API · bulk import.

## Field-officer-centric assumptions to AVOID (design anti-patterns for us)
1. **Hardcoded navigation** (4 static tabs + 7 static home destinations) → we need **permission/capability-registry-driven nav** (our F1 engine).
2. **Entity-first IA** (clients/centers/groups) → we need **task/permission-first IA** spanning products, accounting, admin consoles.
3. **Offline write-behind for EVERYTHING** → wrong default for admin ops. **Per-domain offline policy** (see below).
4. **Staff-scoped fetching** ("my clients / my sheet / my path") baked in → generic app needs **org-wide scoping + filters**, staffId is one filter.
5. **One-role auth — zero permission gating between login and screens** → THE gap our whole concept closes.
6. **Android-first residue** → we treat **Desktop/Web first-class** (back-office users sit at desks).

## Reusable ideas (concepts to carry forward)
1. `core-base`/`core` split (matches template).
2. Strict per-feature convention `feature/{d}` = Screen+ViewModel+Navigation+Koin module (mechanically generatable).
3. **DataTables as a generic dynamic-entity renderer** (list→rows→add-row) → directly our dynamic-forms engine (F3).
4. **Checker-inbox as a first-class nav destination** → even more central in a back-office; generalize to all 965 ops (our M15).
5. **Cross-entity shared modules** `document` / `note` / `activate` (attach to client/group/center/loan) → generic entity plumbing.
6. **`UpdateServerConfigScreen`** — runtime tenant/instance switch without rebuild → our M17 tenant/server switch.
7. **Payload-entity offline pattern** (`*PayloadEntity` + per-aggregate sync + OfflineDashboard) → keep as **opt-in per-domain**, not global.
8. **Adaptive scaffold** (BottomBar↔NavigationRail, Material3 Adaptive) — phone↔desktop continuity.
9. **Deep loan-lifecycle screen decomposition** (approve/disburse/repay/schedule/reschedule/charge-off/guarantor/assign-officer as separate screens) → correct granularity for **per-command permission-gating**.
10. **PDF receipts** (PDFBox) + **passcode+biometrics local lock**.
11. **Consume the Fineract Client KMP SDK** + `MifosInterceptor` tenant-header pattern — use the generated SDK, don't hand-roll 965 endpoints.

## Net for our plan
Our 17 permission-gated modules **superset** this app: M02–M06 + M14/M15 cover its field-ops scope; M07–M13 + M16 are the back-office domains it lacks. Its offline payload-entity + checker-inbox + datatable + adaptive-scaffold patterns are proven and carry forward; its 6 field-officer assumptions are the anti-patterns our permission-first, org-scoped, desktop-first, per-domain-offline design deliberately avoids.
