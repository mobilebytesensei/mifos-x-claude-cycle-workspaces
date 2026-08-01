# EVOLVE PLAN — Role-Based App Assembly

| | |
|---|---|
| **Project** | `mifos-x/mifos-x-backoffice-next-gen` |
| **Date** | 2026-08-01 |
| **Command** | `/idea-evolve-plan` (CP-A..CP-G whole-hierarchy completability sweep) |
| **Auditors** | 4 (Fineract permission model · field-officer app journey audit · CP-A..CP-G idea-layer role-completability · **deep field-officer source audit** — §4.5) |
| **Completability verdict** | **COMPLETABLE — additive work, 0 structural rearchitecture.** 6 blocking assembly/feature gaps + 8 explicit absences. The permission engine + 32 enriched screens already realize "same binary, every role"; the gaps are concentrated **nav-shell assembly wiring**, one **net-new network-config feature**, and **two role journeys**. |
| **Total gaps** | 17 CP-A..CP-G findings (6 blocking) **+ 6 field-ops feature gaps** (§4.5) **+ 2 core-contract gaps** — 3-tier permission gating UX (§4.7) & role-based deployment plan (§4.8) |

## Feedback (verbatim)

> currently app has been designed un-thoughtful way, we are designing the app according to user role, loan officer, admin, Super user, https://demo.mifos.io/api-docs/apiLive.htm, the full features are build and visibility is according to role type and how the dashboard would be assembled and how does the feature walk through etc. like for super user it would be different and for loan officer it would be different, as super user have all ability to make changes and on other hand loan officer is capable of handling clients, and how does center involved it and how does group and it's center and memebr are being managed by him. our focus on build a blocks in such a way it will assembled accoding to role and permission, Look this is current application https://github.com/openMF/mifos-x-field-officer-app source code audit and look how does user jurnoy is build and it's currently build for loan officer and dashboard is poorly built but stiil need to understand the concept the application we are building. Add full app walk through in evolve plan according to rule+ permission of the user logged in, In this application we are allowing user to sing in only and by default demo credenails are going to be in core/network and user would have capability to update the with feature mentioned in loan by click a new feature will open to enter all network information and also this will be accessible in settings. make sure llm mockups are professional and high quality material design full colorfull professional.

---

## §0 · The role-assembly model (grounding — from the Fineract API + field-officer audit)

**How Fineract expresses roles** (verified against `demo.mifos.io/api-docs` + the `m_permission` schema):

- A permission is a row `{grouping, entity_name, action_name, code, can_maker_checker}` where **`code = {ACTION}_{ENTITY}`** (`READ_CLIENT`, `CREATE_LOAN`, `APPROVE_LOAN`, `DISBURSE_LOAN`).
- Maker-checker parks a write for a second person holding the **`{ACTION}_{ENTITY}_CHECKER`** twin, via `/makercheckers/{auditId}?command=approve`.
- Two umbrellas in grouping `special`: **`ALL_FUNCTIONS`** (Super user — bypasses per-code checks), **`ALL_FUNCTIONS_READ`** (read-only), **`CHECKER_SUPER_USER`** (checker on any entry).
- **Capability = permission grant ∩ data scope.** `READ_CLIENT` ≠ "see all clients": data is scoped to the user's **office subtree** and, for a field officer, narrowed to their **staff caseload** (`clients/{id}?command=assignStaff`).
- **The assembly hook**: `POST /authentication` returns the user's **roles + flattened permission list + `officeId` + `staffId`**. The client drives the ENTIRE dashboard + nav + action-gating off that response — no server round-trip per widget.

**The three product roles** (the app must assemble differently for each):

| Role | Grant | Data scope | The app it should see |
|---|---|---|---|
| **Super user** | `ALL_FUNCTIONS` + `CHECKER_SUPER_USER` | head office (all sub-offices) | Full platform-admin shell: users, roles/permissions, global config, accounting, **all** modules + checker-on-all approvals |
| **Admin / back-office** | full portfolio + txn + accounting + reports + approve/disburse + **checker** | office subtree | Approvals + tellers/cash + accounting + reports + full client/group/center/loan/savings lifecycle. NO users/roles/config surface. |
| **Loan / Field officer** | office-scoped client/group/center/member lifecycle + loan/savings **application** + **collections**; **maker** only | own office + assigned caseload | Field workspace: my caseload → centers → groups → members → **collection sheet** → apply loan/savings. NO approve/disburse, NO org/user/config admin. |

**Field-officer app lessons** (from the `openMF/mifos-x-field-officer-app` KMP audit):

- **ADOPT** — offline-first branch-download + pending-payload queue + an explicit sync surface; runtime-editable multi-tenant `ServerConfig(protocol, host, apiPath, port, tenant)` with presets + validators; the Splash→Login→Passcode/Biometric→App auth state machine with background-timeout re-auth; the maker-checker inbox; the `User` model already carrying `permissions[] + officeId`.
- **IMPROVE (the "poorly built dashboard")** — its landing tab is a **mislabeled Search box** (Dashboard icon → Search route); there is **no portfolio-at-a-glance**, no "what needs doing today" feed; entry points are an arbitrary split of 4 bottom tabs vs 7 drawer items; and critically **the fetched `permissions[]` never branches the UI** — the app is one-size-fits-all despite holding the role data. Our app must do the opposite: **assemble the home + nav + actions from the permission set.**

This is exactly the gap the audit found in our own idea-layer: the *concept* is permission-driven, but the **assembler that turns the permission set into a rendered role-specific app is not yet built** (§CP-C G1).

---

## §1 · Traceability matrix (vision → FR → feature → screen → data → flow)

Chain is **INTACT** for the 32 built screens (all enriched/green, permission-gated, state-exhaustive, `compose_dead_clicks: 0`). The BREAKS are concentrated at two joints — **feature→screen reachability** (the empty assembler) and **absent net-new capability** (network-config + role journeys):

| Chain link | Status | Break detail |
|---|---|---|
| vision.in_scope → FR | ⚠ PARTIAL | "dashboard + walkthrough differ by role" and "editable network-config" are vision-implicit but have **no FR** (CP-A #2, #3) |
| FR → feature | ✅ / ⚠ | portfolio FRs → features OK; **no `network-config` feature** for FR-8's editable server/tenant/creds (CP-B #2) |
| feature → screen | 🔴 **BREAK** | **13 module screens have zero inbound nav edge** — m03/m05/m07/m08/m09/m10/m11/m12/m13/m15/m16 + offline-sync-engine + product-editor are all enriched but **unreachable** (CP-D #8) |
| feature → screen (net-new) | 🔴 **BREAK** | **no `network-config` screen** (only a preset dev/sandbox/prod switch in m17; no editable creds; no loan-area entry) (CP-D #6) |
| screen → data | ✅ / ⚠ | permission gating COHERENT (`gated_permission` on all mutating controls); **no network-config data-flow** persisting user-edited base-URL/tenant/creds → core/network + core/datastore; **no demo-cred seed** (CP-E #10, CP-D #7) |
| screen → flow (reachability) | 🔴 **BREAK** | 13 orphans ⇒ `structural_closed: false`; the assembler that would give them inbound edges (`app-shell.yaml drawer.items: []`) **is not built** (CP-F #14, CP-C #1) |
| flow → journey (role) | 🔴 **BREAK** | **no stitched loan-officer field-day journey** (login→dashboard→centers→group→members→collection-sheet→apply); **no super-user admin journey** (login→admin-dashboard→users/roles→config→approvals); **no auth/network-config change→re-auth journey** (CP-F #11, #12, #13) |
| screen behavior | ✅ CLEAN | `incomplete_on_click: []`, `unresolved_targets: []`, role-gating renders HIDE/DISABLE-with-reason + 403→refresh-prune. (The plain-list/toast **implementation** downgrades are a source-fidelity concern handled by the design-conformance heal — §4, not an idea-layer gap.) |

**Keystone**: `design-system/app-shell.yaml:52` — `drawer.items: []  # populated at build time from the 17 permission-gated module roots` — is an **unbuilt promise**. It alone causes the 13-orphan break. Building the role-adaptive NavShell assembler converts 13 orphans → reachable **in one stroke**, and is the mechanism every role's distinct app is assembled through.

---

## §2 · Gaps by dimension (CP-A..CP-G)

### CP-A — Vision → Requirement
| # | level_entity | gap_type | what_blocks_completion | evidence | fix_direction |
|---|---|---|---|---|---|
| A1 | vision (role dashboards/walkthrough) | missing-requirement | "dashboard assembly + feature walkthrough differ by role" is not an FR — no acceptance target for role-distinct home/onboarding | `idea-plan.yaml` vision L103-136; personas are `permissions_sample` code-lists, not assembled role profiles | Add FR: per-role dashboard-assembly + first-run role walkthrough, driven by resolved permission set |
| A2 | vision (network-config) | missing-requirement | editable base-URL+tenant+credentials post-login (with demo defaults) has no FR; FR-8 is only "tenant + server switch" | `idea-plan.yaml` requirements L173-181 | Add FR: user-editable network config, demo-cred default in core/network, reachable from loan area + Settings, ends in re-auth |

### CP-B — Requirement → Feature
| # | level_entity | gap_type | what_blocks_completion | evidence | fix_direction |
|---|---|---|---|---|---|
| B1 | FR-8 → (no feature) | missing-feature | no `network-config` feature satisfies the editable-server requirement | `idea-plan.yaml` features list (no network-config id) | Add `network-config` **foundation** feature (P0), dual entry points |
| B2 | role-assembly → nav-shell | missing-feature | the role-adaptive NavShell that renders the permitted module roots is not a feature — it lives only as an empty `drawer.items: []` config | `design-system/app-shell.yaml` L50-52 | Add `nav-shell-assembler` feature that data-binds drawer/rail/bottom-bar to the permission-capability-engine's resolved module roster |

### CP-C — Roadmap / phase
| # | level_entity | gap_type | what_blocks_completion | evidence | fix_direction |
|---|---|---|---|---|---|
| C1 🔴 | app-shell nav assembly | missing-assembler-wiring (**highest leverage**) | assembler that renders each role's app does not exist: bottom-nav = 4 hardcoded field-officer placeholders, `drawer.items: []`. A super-user can't reach admin modules; a loan-officer's nav is a fixed field set | `design-system/app-shell.yaml` L7, L14-52 | Model role-adaptive NavShell rendering permitted roots (adaptive: drawer/rail desktop, bottom-bar phone) from resolved roster; make `drawer.items` a data-driven binding |
| C2 | deployment_plan P0-P6 | coherent | roadmap already sequences foundation→read→money→origination→supervision→admin→rollout on permissions | `idea-plan.yaml` deployment_plan | Slot `network-config` into P0; `nav-shell-assembler` into P0/P1; role journeys into P4/P5 |

### CP-D — Feature → Screen
| # | level_entity | gap_type | what_blocks_completion | evidence | fix_direction |
|---|---|---|---|---|---|
| D1 🔴 | 13 module screens | unreachable-screen | m03-groups-centers, m05-savings, m07-accounting, m08-products, m09-organization, m10-users-roles, m11-tellers, m12-datatables, m13-scheduler, m15-approvals, m16-communications, offline-sync-engine, product-editor — enriched but **no inbound nav edge** | `state/APPLICATION_GRAPH.yaml` orphans L38-51 + closure.unreachable L1879-1893; `CAPABILITY_GAPS.yaml` G-NAV-ORPHAN | NavShell assembler (C1) resolves the whole class |
| D2 | network-config screen | missing-screen | no editable base-URL/tenant/username/password screen; m17 `switch_server_row` is a preset dev/sandbox/prod switch with **no credentials edit + no loan-area entry** | `screens/m17-sync-settings/ui.yaml` L151-169; `screens/fineract-auth-session/ui.yaml` | New `network-config` screen: base-URL/tenant/username/password → validate → save → re-auth |
| D3 | login demo default | missing-default | demo creds (`mifos`/`password` @ demo.mifos.community, super-user) exist only as test fixtures, not seeded into the login form; fields are `mandatory` + empty | `fineract-auth-session/demo-data.yaml` L8-11 vs `ui.yaml` L102-134 | Seed demo defaults from core/network into login initial state (dev/demo builds) |
| D4 | m01-dashboard | partial (single roster) | one permission-filtered tile roster, not role-distinct assemblies (loan-officer route-first vs super-user admin-KPI-first); appears in only ONE journey | `screens/m01-dashboard/ui.yaml` L10-23, 65-162 | Add per-role tile-ordering/section assembly (loan-officer "today" feed vs admin approvals-KPI vs super-user platform-health) |

### CP-E — Feature-Data
| # | level_entity | gap_type | what_blocks_completion | evidence | fix_direction |
|---|---|---|---|---|---|
| E1 | permission gating | coherent (strong) | screens gate reads/writes on PermissionSet; `passes_permission_flow: true` on all 32; 403 drift → refresh+prune | `APPLICATION_GRAPH.yaml` per_feature validation; `CAPABILITY_GAPS.yaml` L133-148 | — (no gap) |
| E2 | network-config data-flow | missing-data | no data-flow persisting user-edited base-URL/tenant/creds as an independent config → core/network + core/datastore; no demo-config seed in core/network | `m17-sync-settings/ui.yaml` L151-169; `fineract-auth-session/ui.yaml` L150-158 | Add network-config data-flow: persist → swap base-URL + `Fineract-Platform-TenantId` header → re-auth; seed demo config in core/network |

### CP-F — Flow / journey
| # | level_entity | gap_type | what_blocks_completion | evidence | fix_direction |
|---|---|---|---|---|---|
| F1 🔴 | loan-officer field-day | broken-journey | no single journey chains login→role-dashboard→centers→group→members→collection-sheet→loan/savings-application; split across 4 partial journeys; m03 center→group→member drill is prose-only + orphan | journeys inventory; `flows/back-office-flows.yaml` (no field-day flow) | Author stitched `loan-officer-day` journey; weave m03 into nav (screen content already complete: center→group→members→attendance→collection-sheet→GLIM) |
| F2 🔴 | super-user admin | missing-journey | no consolidated login→admin-dashboard→users/roles/config/approvals journey; `permissions-administration` is read-only access-audit only; admin work scattered across m07/m08/m09/m12/m13 + isolated approvals | journeys Q1; `back-office-flows.yaml` `permissions-admin` L33-36 | Author `super-user-admin` journey chaining admin modules + checker approvals from an admin dashboard |
| F3 | auth/network-config | missing-journey | no settings→edit-network→save→re-auth journey | journeys Q4 | Add config-change→re-auth journey tied to the new feature |
| F4 | flow registry | missing-flow | 8 modules unflowed (m03/m05/m07/m09/m11/m12/m13/m16); none role-oriented | `flows/back-office-flows.yaml` L7-47 | Add role-oriented flows spanning the module set per role |

### CP-G — Screen behavior
| # | level_entity | gap_type | what_blocks_completion | evidence | fix_direction |
|---|---|---|---|---|---|
| G1 | all 32 screens | clean | `compose_dead_clicks: 0`, `incomplete_on_click: []`, `unresolved_targets: []`, `dead_ends: []` | `APPLICATION_GRAPH.yaml` closure L1877-1899 | — the behavioral hole is structural reachability (D1), not dead handlers |
| G2 | role-gating behavior | modeled | denied controls render HIDE/DISABLE-with-reason; 403 → refresh+prune | permission-capability-engine `refresh_permissions`; m03 403→drift | — (no gap) |
| G3 | plain-list/toast fidelity | source-layer (out of idea-scope) | the known "toast instead of bottom-sheet / plain list vs mockup" downgrades are IMPLEMENTATION fidelity, not idea-layer gaps (screens specify rich states) | screens `passes_state_exhaustiveness: true` | Handled by the design-conformance heal (§4): opus kmp-screen-gen + MOCKUP-FIRST + DC-KMP + device-verify |

---

## §3 · Full app walkthrough — per role + permission (the deliverable the feedback asked for)

The **same binary**. `POST /authentication` → `{roles, permissions[], officeId, staffId}` → the NavShell assembler + dashboard assembler render one of three experiences. A user with multiple roles gets the **union** (highest surface they qualify for). Every control below is already `gated_permission`-tagged in the idea-layer; the walkthrough is what the assembler must produce.

### Common entry (all roles)
1. **Splash** → checks persisted session (FineractSessionStore token + UserDataRepository.isAuthenticated).
2. **Sign-in only** (`fineract-auth-session`) — username + password + tenant. **Demo defaults pre-seeded** from core/network (dev/demo builds): `mifos` / `password` · **primary** `mifos-bank-2.mifos.community` (tenant **`mifos-bank-2`**, 15 real roles incl. OFICIAL DE CAMPO / CAJERO / SUPERVISOR), **fallback** `sandbox.mifos.community` (tenant `default`) — full connection info in `research/FINERACT_INSTANCES.md`. A **"Network settings"** affordance on the login screen opens the network-config feature (D2) to point at any instance.
3. **Passcode / biometric** lock (adopt field-officer pattern) with 15s background-timeout re-auth.
4. `POST /authentication` → capability bootstrap: `PermissionSet.fromRaw(permissions)` → `PermissionStateHolder`; `officeId`/`staffId` set the data scope.
5. **NavShell assembler** reads the resolved module roster → renders bottom-bar (phone) / rail+drawer (desktop) with ONLY the permitted roots. **Dashboard assembler** renders the role-appropriate home.

### 🟢 Loan / Field officer walkthrough (maker, office+caseload scoped)
> *Grant: office-scoped client/group/center/member lifecycle + loan/savings application + collections; maker only. NO approve/disburse, NO org/user/config.*

- **Home = "My Field Day"** (NOT a search box — the field-officer app's core failure we fix). Assembled tiles: **Today's collections due** (from `generateCollectionSheet` for my centers' meeting dates) · **Overdue loans in my caseload** · **Clients/groups to activate** · **Pending applications I submitted** · **Sync-pending count**. Route-first, action-oriented feed.
- **Nav roots** (permission-filtered): My Caseload (clients) · Centers · Groups · Collection Sheet · Sync · Settings. Admin/accounting/users/config roots are **HIDDEN**.
- **Journey — the field day** (F1):
  `Home → Centers (my office) → Center detail → Group → Group members (associate/disassociate clients) → Generate Collection Sheet (meeting date) → record repayments + mandatory deposits in bulk → Save collection sheet → back to Home`.
  Parallel origination path: `Home → My Caseload → Client detail → Apply Loan / Apply Savings → submitted (parks for back-office approval; shows "pending approval" state)`.
- **Actions** — client create/activate/assignStaff(self); group create/activate/associateClients; center create/activate/associateGroups/generateCollectionSheet/saveCollectionSheet; loan apply + repayment; savings apply + deposit/withdrawal. **Approve/disburse controls render DISABLED-with-reason** ("requires back-office approval"). Every write that hits a maker-checker-enabled action shows a "**sent for approval**" bottom-sheet confirmation (NOT a bare toast — §4).
- **Offline**: branch-download my centers/groups/clients; queue writes; explicit Sync surface with per-entity counts.

### 🟡 Admin / back-office walkthrough (checker, office-subtree scoped)
> *Grant: full portfolio + txn + accounting + reports + approve/disburse + checker. NO users/roles/config.*

- **Home = "Operations"** — assembled tiles: **Approvals queue** (maker-checker inbox — loans/savings/clients awaiting my approval) · **Portfolio KPIs** (active clients, PAR/loans-in-arrears, disbursals today) · **Teller/cash position** · **Reports shortcuts**.
- **Nav roots**: Dashboard · Clients · Groups · Centers · Loans · Savings · **Approvals** · Tellers/Cash · Accounting · Reports · Settings. Users/Roles/Config roots **HIDDEN**.
- **Journey — approve & operate** (part of F2's back-office slice):
  `Home → Approvals → maker-checker entry → review → Approve (`POST /makercheckers/{id}?command=approve`) → entity moves to approved`. Origination continuation: `Loans → loan application → Approve → Disburse`. Cash: `Tellers → allocate/settle`.
- **Actions** — everything the loan officer has, PLUS approve/disburse/reject on loans & savings, checker-approve on maker-checker entries, teller/cash ops, accounting (GL/journal), full reports. Approve/disburse render **ENABLED** with a confirmation bottom-sheet + real result state.

### 🔴 Super user walkthrough (`ALL_FUNCTIONS` + `CHECKER_SUPER_USER`, head office)
> *Grant: everything, incl. user/role administration, global config, checker-on-all.*

- **Home = "Platform Admin"** — assembled tiles: **Platform health** · **All-office KPIs** · **Approvals (checker-on-all)** · **User & role activity** · **Config/maker-checker toggles** · **Communications**.
- **Nav roots**: ALL module roots visible — Dashboard · Clients · Groups · Centers · Loans · Savings · Approvals · Tellers · Accounting · Products · Organization · **Users** · **Roles & Permissions** · Datatables · Scheduler · Communications · Reports · Settings.
- **Journey — administer** (F2):
  `Home → Users → create user / assign roles → Roles & Permissions → create role / grant permission codes / toggle maker-checker (`PUT /permissions`) → Organization (offices/staff) → Config → Approvals (approve any entry via CHECKER_SUPER_USER)`.
- **Actions** — the full catalog: user CRUD, role CRUD + permission grants + `enable/disable`, global configuration, codes/charges, products, org hierarchy, checker-on-any. This is the ONLY role where the users/roles/config surface is reachable.

### The network-config feature (walkthrough — reachable from BOTH loan area + Settings)
- **Two entry points**: (1) a "**Network settings**" tile/affordance in the loan area (m04) — the "new feature by click" the feedback describes; (2) **Settings → Network configuration** (m17).
- **Screen**: editable **base URL · tenant (`Fineract-Platform-TenantId`) · username · password**, with **demo defaults pre-filled from core/network** and a "Reset to demo" action. Validators (adopt field-officer `ServerConfigValidatorUseCase` + `ValidateServerTenantUseCase`).
- **Flow** (F3): `entry → edit fields → validate → Save → persist to core/network + core/datastore → swap base-URL + tenant header (DynamicBaseUrlPlugin) → forced re-auth → back to sign-in with new endpoint`.
- **Default**: on a fresh install with no user override, core/network ships the demo config so the app is **usable out-of-box**.

---

## §4 · Root-cause patterns (cross-cutting)

1. **The assembler is the missing keystone, not the modules.** Every role gap (13 orphans, no super-user reach, fixed field-officer nav) traces to ONE unbuilt thing: the role-adaptive NavShell that data-binds nav roots to the resolved permission roster. `drawer.items: []` is the whole disease. Build it once → 13 orphans reachable, all three roles assemble.
2. **Concept without assembly.** The idea-layer *models* permission-driven visibility beautifully (gating, personas, 403-drift) but stops at the boundary where the permission set must **render a specific app**. Same pattern as the field-officer app (fetches `permissions[]`, never branches UI).
3. **Net-new capability cluster: network-config.** One clean vertical absent end-to-end — feature + screen + data-flow + flow + journey + demo-seed + dual entry. Additive, self-contained.
4. **Role journeys are authoring over existing screens.** The loan-officer-day and super-user-admin journeys chain screens that **already exist and are green** — this is journey stitching + reachability, not new screen construction.
5. **Design fidelity is a source-layer heal, already in place.** The "totally different UI / toast-not-bottom-sheet / plain-list" divergences are IMPLEMENTATION downgrades, now caught by the shipped design-conformance heal: **opus `kmp-screen-gen` + MOCKUP-FIRST directive + `framework-verify-design-conformance-kmp.sh` (DC-KMP-STATUS/AVATAR/CARDS/ACTION) + `_shared/design-conformance-device-verify.md`** (render each state's mockup + Maestro-drive every confirmation on_click on-device md5-matched + Claude judges device↔mockup per state + deep-flow data-fetch check for loan/savings application). The evolve implement phase MUST route every regenerated screen through this path so the professional Material-Design mockups are matched, not approximated.

---

## §4.5 · Field-Officer App Source Audit + Feature Gap Map

Deep read-only source audit of **openMF/mifos-x-field-officer-app@dev** (KMP/Compose, `com.mifos.feature.*`): 21 feature modules, 9 `core/*` modules, `cmp-navigation`. It is a **field-ops** app (the center→group→client→account hierarchy + offline), a *subset* of Fineract — our target is the full back-office, so it *adds* accounting/products/org/users-roles/tellers/scheduler/communications that the field app lacks (those are not gaps). The audit's job here: find field-ops capabilities our back-office model **skipped**. Every "already-modeled?" verdict below was **verified by grep against our idea-layer**, correcting the audit's own caveat (it hadn't read our specs).

### Feature inventory (source)
`auth · passcode(+biometric) · search · search-record · center(+SyncCentersDialog) · groups(+SyncGroupDialog) · client(~40 screens: profile/address/identifiers/documents/signature/pinpoint/survey/staff/charges/collateral/accounts/apply/closure/transfer + SyncClientsDialog) · loan(~30: apply/approve/disburse/reject/repay/schedule/txns/charge/chargeoff/reschedule/guarantor/assign-officer/transfer) · savings(+TransactionReceipt) · recurringDeposit · collectionSheet(generate + individual + payment-details) · checker-inbox-task · activate · note · document · data-table · report · offline(OfflineDashboard outbox + per-entity SyncPayloads) · path-tracking(GPS) · settings(UpdateServerConfig + SyncSurveys) · about`

### Flow (source)
`Splash → Login (tenant/baseURL) → set/enter Passcode(+Biometric; 15s bg re-lock) → AuthenticatedNavbar → bottom tabs [Search·Clients·Centers·Groups] + drawer [Checker Inbox · Collection Sheet · Run Reports · Path Tracker · Offline Sync · Settings · About] → drill Center→Group→Client 360 → Loan/Savings/Share/FD/RD accounts → account actions → {per-entity SyncDialog = pre-download a branch offline; OfflineDashboard = outbox of queued mutations}`.

### Gap map (grep-verified against our idea-layer)
| Field-officer capability | Verdict | Evidence in our idea-layer |
|---|---|---|
| offline mutation **outbox** / payload queue | ✅ COVERED | `outbox` in 332 files (`offline-sync-engine`, `needs-attention-inbox`) |
| loan **reschedule · guarantor · write-off/foreclosure** | ✅ COVERED | reschedule 28 · guarantor 15 · writeoff/foreclosure 17 (`m04`) |
| client **transfer (proposeTransfer) · closure** | ✅ COVERED | proposeTransfer 8 (`m02`/`client-detail-360`) |
| **share accounts · recurring deposit** | ✅ COVERED | share-account 20 (`m05`) |
| **transaction receipt** (PDF) | ✅ COVERED | transaction-receipt 5 (`m05`) |
| **individual collection sheet** | ✅ COVERED | individual-collection 3 (`m06`/`collection-sheet`) |
| **passcode + biometric lock** | 🟨 REFERENCED | biometric 21 · passcode 2 — modeled in decisions/m17, **not a dedicated feature/screen set** (low-priority to promote) |
| **client signature capture** | 🔴 MISSING | 0 (the 19 `signature` hits are `signature:` business_logic fields — false positives) |
| **client survey** (list→question→submit + pre-download) | 🔴 MISSING | 0 |
| **client pinpoint** (GPS geo-tag client location) | 🔴 MISSING | 0 |
| **path-tracking** (GPS field-visit route trail) | 🔴 MISSING | 0 (GPS/geotag/path-track all 0) |
| **search-record** (offline / recent-search history) | 🔴 MISSING | 0 |
| **per-entity branch-download sync dialog** (pre-download a center/group/client hierarchy for offline) | 🔴 MISSING | 0 (general outbox is covered; the *download-a-branch* dialog is not) |

### Features to include (the 6 genuine gaps — all belong to the loan/collections-field-officer persona surface, permission-gated)
These are exactly the field-officer role's daily field-work capabilities the user described ("loan officer capable of handling clients… center… group… member"). Add them gated to the `loan-officer-maker` / `collections-field-officer` personas (hidden for admin/super-user unless permitted):

| # | Add | Where it fits |
|---|---|---|
| FO-1 | **`path-tracking`** — GPS field-visit route trail (record/view officer location during a visit day) | new feature (needs `core/platform` location capability); drawer root for field-officer persona |
| FO-2 | **`client-survey`** — survey list → question → submit, + offline survey pre-download | section of `m02-clients` / `client-detail-360`; `/surveys` |
| FO-3 | **client signature capture** — sign-pad/image on client profile | section of `client-detail-360`; `/clients/{id}/images` |
| FO-4 | **client pinpoint** — GPS geo-tag a client's location | section of `client-detail-360` (needs `core/platform` location) |
| FO-5 | **`search-record`** — offline / recently-searched history (distinct from live `m14` search) | extends `m14-reports-search-audit` |
| FO-6 | **branch-download sync dialog** — per center/group/client, pre-download a hierarchy branch for offline field use (distinct from the mutation outbox we already model) | extends `offline-sync-engine`; per-entity affordance on m03/m02 lists |

*(Not added: `about`/diagnostics — minor, folds into m17; passcode/biometric screens — already referenced, low value to promote.)*

---

## §4.6 · Account-Action Depth Map (client → account → action)

Deep source audit of the field-officer app's `feature/{client,loan,savings,recurringDeposit,...}` + `core/network/services/*` — the complete drill path and the exact Fineract command each action fires. **Key differentiator:** the reference app **renders ~45 loan actions but wires only 6** (≈38 are dead `{}` stubs), and its **Share / Fixed-Deposit / Recurring-Deposit detail & approve routes are no-ops** — only **Savings** is fully wired. Our back-office **completes the account-action surface** (every action real, permission-gated, maker-checker-aware where Fineract allows).

**Drill path:** `client roster → client 360 (profile hub) → General & Accounts → account list grouped by type → account detail → status-aware action`.

**Per-account-type action surface (each row = action · Fineract command · MC-capable · offline-queued):**

| Loan (`m04`) | Savings (`m05`) | Share / FD / RD (`m05`) |
|---|---|---|
| approve `?command=approve` (MC) · disburse `disburse`/`disburseToSavings` (MC) · reject `reject` (MC) · undo-approval/undo-disbursal · **repayment** `transactions?command=repayment` (offline) · prepay · waive-interest `waiveinterest` · write-off `writeoff` (MC) · charge-off `transactions?command=charge-off` (MC) · foreclosure (MC) · reschedule `/rescheduleloans` (MC) · assign/unassign officer · guarantors `/guarantors` · add-charge · account-transfer `/accounttransfers` · close | approve `?command=approve` (MC) · reject · undo-approval · activate `activate` (MC) · **deposit** `transactions?command=deposit` (offline) · **withdrawal** `withdrawal` (offline) · hold/block `holdAmount` · release-hold · post-interest `postInterest` · add-charge · waive-charge · close · **receipt** (PDF) | **Share:** create-wizard · approve · activate · redeem · close · **FD:** create-wizard · approve · activate · premature-close · maturity · **RD:** create-wizard · approve · activate · deposit · premature-close *(reference: create-wizards live; detail/approve dead — we wire them)* |

**Transaction sub-flows:** loan repayment (date · payment-type · amount · additional · fees · total); savings deposit/withdrawal (date · amount · payment-type); transaction receipt (PDF). Loan schedule = installment table (#/date/principal/interest/due/paid/outstanding, export PDF); loan transactions = posted ledger with reversible rows.

**Apply-new-application:** client 360 (active only) → product chooser → per-type create wizard (Loan: Details·Terms·Schedule·Charges·Preview · Savings: Details·Terms·Charges·Preview · FD/RD: +Interest·Settings · Share: Details·Terms·Charges·Preview) → submitted pending-approval.

**Offline truth:** only 5 payload types queue (client-create, group, center, loan-repayment, savings-transaction) — applications/approvals are online-only. Maker-checker surfaces via the separate Checker-Inbox (`m15`), not inline.

**Depth-flow screens to deliver (flesh out `m02`/`m04`/`m05`, mostly PARTIAL not net-new):** ① client roster (search/filter/paged) ② client 360 (profile hub + lifecycle actions) ③ accounts grouped by type ④ loan detail + **complete** action set + Summary/Schedule/Transactions/Charges tabs ⑤ loan repayment form ⑥ schedule + ledger tables ⑦ savings detail + full actions ⑧ savings deposit/withdrawal form + receipt ⑨ approval/activate forms ⑩ apply-new chooser + 5 wizards ⑪ Checker-Inbox ⑫ offline-sync dashboard. **Visualized in the mockup gallery (§ Account depth).**

---

## §4.7 · Permission-Driven Assembly & Gating Behavior (the core product contract)

The entire app assembles from ONE input: the login permission set. `POST /authentication` → `{roles[], permissions[], officeId, staffId}`. The **effective permission set = the union of every assigned role's codes** (Role A ∪ Role B ∪ Role C); the `ALL_FUNCTIONS` umbrella short-circuits to "everything enabled" (Super user → access to every API → full app). **Nothing branches on role *name* — only on permission codes** (Fineract has no role/user type; §4.6).

**Three-tier gating — the precise behavior:**

| Tier | Rule | UX |
|---|---|---|
| **1 · Nav root** (bottom-nav item / drawer item) | show iff the user holds ≥1 code in that module's permission family (any `*_LOAN`, `*_CLIENT`, …) | **HIDDEN** when zero family access (fail-closed). Bottom nav + drawer assemble from the permitted roster (`nav-shell-assembler`) |
| **2 · Feature reachable** | a feature opens if the user holds ≥1 code in its family | visible + navigable |
| **3 · Action within a feature** | each control (Create/Update/Approve/Disburse/Delete/…) enabled iff the user holds its exact code | **GRAYED-OUT** when lacked (NOT hidden) + on-click **information dialog**: *"You don't have permission. Please contact your manager if you need access."* |

**Worked example (yours):** a user with Loan → `CREATE_LOAN` ✓ + `UPDATE_LOAN` ✓ but not `APPROVE_LOAN`/`DISBURSE_LOAN`/`DELETE_LOAN` → the **Loan feature is visible** (has family access), **New/Edit enabled**, **Approve/Disburse/Delete grayed out** — tapping any shows the "contact your manager" dialog. That's the real `OFICIAL DE CAMPO` grant (maker only, §4.6).

- **Bottom navigation** = the phone-adaptive subset of the permitted module roots; **Navigation drawer** = the full permitted roster — both data-bound by `nav-shell-assembler` (no hardcoding).
- **Multi-role** = union the codes; `ALL_FUNCTIONS` ⇒ every control enabled.
- **403 drift**: the server is the real gate — a 403 despite a client grant refreshes the permission set, re-resolves, prunes the UI, notifies once.
- **Hide vs gray-out**: modules with ZERO family access stay hidden at the nav root; the gray-out + "contact your manager" dialog is ONLY for actions *inside* a feature the user can partially use — so users discover a capability exists and how to request it, rather than silently missing it. Every interactive control therefore carries a permission-aware `action_contract` with a `required_permission` code and a `denied_behavior: gray-out-info-dialog`.

## §4.8 · Role-Based Deployment Plan (build order — LOAN OFFICER is #1)

Delivery is sequenced by **user-role type**, not only by capability. Each phase makes ONE role's app fully usable end-to-end — its dashboard + nav roster + features + 3-tier action-gating — mapped to the **real `mifos-bank-2` grant-sets** (§4.6). We build for every role type; loan officer ships first.

| Phase | Role type (real role) | Ships (features gated on the role's codes) | Exit criterion |
|---|---|---|---|
| **R0 · Foundation** (all roles) | — | auth · permission-capability-engine · **nav-shell-assembler** · **network-config** · offline outbox · dynamic-forms · passcode/biometric | login assembles nav + dashboard + 3-tier gating from the permission set |
| **R1 · LOAN / FIELD OFFICER** ⭐ **TOP PRIORITY** | `OFICIAL DE CAMPO` (149, maker) | My Field Day dashboard · client roster→360 · field-work (signature/survey/pinpoint/path-tracking) · centers→groups→members · collection sheet · loan & savings **application** (maker) · branch-download offline. Gates: `CREATE_CLIENT/LOAN/SAVINGSACCOUNT/GUARANTOR/COLLATERAL`; **approve/disburse grayed-out + dialog** | a loan officer runs a full field day **offline, maker-only** |
| **R2 · TELLER / CASHIER** | `CAJERO` (75) | money-movement home · savings **deposit/withdrawal** · loan **repayment** · receipts | teller transacts, no origination |
| **R3 · CHECKER / SUPERVISOR** | `REVISOR DE PRESTAMOS` (459) / `SUPERVISOR` (99) | maker-checker **inbox** · approve/reject · client lifecycle (activate/reject/undo) | checker approves maker submissions (`APPROVE_LOAN` + `_CHECKER`) |
| **R4 · TREASURER** | `TESORERO` (89) | loan **disbursal** + disbursal-undo | approved loans disbursed |
| **R5 · BRANCH OFFICER + COMPLIANCE** | `EJECUTIVO` (195) / `Oficial KYC` (43) / `OFICIAL PLD` (40) / `OFICIAL DE CONTROL` (105) | datatable CRUD · group/center create · foreclosure/charge-off · KYC/AML client lifecycle + audit READ | branch ops + compliance |
| **R6 · ADMIN / SUPER USER** | `Super user` (`ALL_FUNCTIONS`) | users/roles/permissions (m10) · organization (m09) · products/charges (m08) · accounting (m07) · scheduler (m13) · communications (m16) · config (m12) | full platform-admin surface |

The capability phases P0–P6 in `idea-plan.yaml#deployment_plan` still hold underneath — R0..R6 **re-sequence delivery around who can use it first**. Materializes into `deployment_plan` via `/idea-deploy-plan` rebalance during the drive.

---

## §5 · Enrich prompt (bottom-up the hierarchy — ready to run)

```
/idea-agent evolve "Assemble mifos-x-backoffice-next-gen as a role-based app: the same binary renders a distinct experience per logged-in user's Fineract role+permission (loan/field officer=maker, office+caseload scoped; admin/back-office=checker, office-subtree scoped; super user=ALL_FUNCTIONS+CHECKER_SUPER_USER, head office). Drive assembly off POST /authentication's {roles, permissions[], officeId, staffId}.

(1) REQUIREMENTS/FEATURES/ROADMAP: add FR + foundation feature 'nav-shell-assembler' (role-adaptive NavShell that data-binds bottom-bar/rail/drawer roots to permission-capability-engine's resolved module roster — replace app-shell.yaml drawer.items:[] and the hardcoded 4 field-officer bottom-nav placeholders with a permission-driven roster; adaptive: drawer/rail desktop, bottom-bar phone). Add FR + foundation feature 'network-config' (P0). Add FR for per-role dashboard assembly + first-run role walkthrough.

(2) FEATURE-DATA: add network-config data-flow — editable base URL + tenant (Fineract-Platform-TenantId) + username + password, persisted to core/network + core/datastore, with demo defaults SEEDED in core/network (mifos/password; PRIMARY base mifos-bank-2.mifos.community tenant `mifos-bank-2`, FALLBACK sandbox.mifos.community tenant `default` — call primary first, see research/FINERACT_INSTANCES.md) so the app is usable out-of-box; save swaps base-URL + tenant header (DynamicBaseUrlPlugin) and forces re-auth. Seed the same demo defaults into the sign-in form initial state (dev/demo builds).

(3) FLOWS/JOURNEYS: author 3 role journeys — 'loan-officer-day' (login→My-Field-Day dashboard→Centers(my office)→Center→Group→members(associate/disassociate)→generateCollectionSheet→bulk repayment+deposit→saveCollectionSheet; parallel: My Caseload→Client→apply loan/savings→pending-approval), 'super-user-admin' (login→Platform-Admin dashboard→Users(create/assign roles)→Roles&Permissions(grant codes/toggle maker-checker via PUT /permissions)→Organization→Config→Approvals checker-on-all), and 'network-config-change' (loan-area tile OR Settings→edit network→validate→save→re-auth). Wire orphan m03 center→group→member drill into nav; give all 13 orphan module screens inbound edges through the nav-shell assembler.

(4) SCREEN BEHAVIOR + DASHBOARD ASSEMBLY: build network-config screen (base-URL/tenant/username/password, demo pre-fill, Reset-to-demo, validators) with dual entry points (loan-area 'Network settings' tile + Settings). Make m01-dashboard assemble per role — loan-officer 'My Field Day' action feed (collections due today, overdue caseload loans, to-activate, pending applications, sync count), admin 'Operations' (approvals queue, portfolio KPIs, teller position), super-user 'Platform Admin' (platform health, all-office KPIs, user/role activity, config toggles). Loan-officer approve/disburse controls render DISABLED-with-reason; every maker-checker write shows a bottom-sheet confirmation (NOT a bare toast).

(5) FIELD-OFFICER FIELD-WORK FEATURES (from the openMF/mifos-x-field-officer-app source audit, §4.5 — gate ALL to the loan-officer-maker / collections-field-officer personas, HIDDEN for other roles unless permitted): add feature 'path-tracking' (GPS field-visit route trail via core/platform location) as a field-officer drawer root; add to client-detail-360 — 'client-survey' (survey list→question→submit + offline survey pre-download, /surveys), client signature capture (sign-pad/image, /clients/{id}/images), client pinpoint (GPS geo-tag client location via core/platform); extend m14-reports-search-audit with 'search-record' (offline/recent-search history, distinct from live search); extend offline-sync-engine with a per-entity branch-download sync dialog (pre-download a center/group/client hierarchy branch for offline field use, distinct from the mutation outbox already modeled). These are the field-officer role's daily field-work capabilities.

(6) ACCOUNT-ACTION DEPTH (§4.6 — flesh out m02/m04/m05, the full client→account→action drill): client roster (search/filter/paged) → client-360 profile hub with client lifecycle actions (activate/close/proposeTransfer/assignStaff/updateDefaultAccount/addCharge/applyNewApplication) → accounts grouped by type → per-account-type detail with the COMPLETE status-aware action set (do NOT ship the reference app's ~38 dead loan-action stubs or its no-op Share/FD/RD detail routes). Loan detail: Summary/Schedule/Transactions/Charges tabs + approve/disburse/reject/repayment/reschedule/charge-off/write-off/foreclose/waive-interest/assign-officer/guarantors/account-transfer/close — each wired to its real Fineract command with a real action_contract, maker-checker-aware, repayment offline-queued. Savings detail: deposit/withdrawal/hold/release/post-interest/add-charge/close + transaction receipt (PDF). Share/FD/RD: create-wizard + approve/activate/redeem/premature-close detail (wire the routes the reference leaves dead). Transaction forms (loan repayment; savings deposit/withdrawal) + approval/activate forms + apply-new chooser with 5 per-type create wizards. Every account action carries a required_permission code and renders GRAYED-OUT with a 'You don't have permission — contact your manager' info dialog when the role lacks it (per §4.7); enabled actions confirm in a bottom sheet.

(7) PERMISSION-DRIVEN ASSEMBLY & 3-TIER GATING (§4.7 — the core contract): assemble the ENTIRE app from the login permission set (union of the user's roles' codes; ALL_FUNCTIONS = everything → full app). Bottom-nav + navigation-drawer roots data-bound to the permitted module roster — hide a root ONLY when the user has ZERO codes in that module family (fail-closed). Give EVERY interactive control a permission-aware action_contract carrying required_permission + denied_behavior: gray-out-info-dialog — a control the user lacks renders GRAYED-OUT (not hidden) and on-click shows an information dialog 'You don't have permission. Please contact your manager if you need access.' Worked example: CREATE_LOAN + UPDATE_LOAN present but APPROVE_LOAN/DISBURSE_LOAN absent → Loan feature visible, New/Edit enabled, Approve/Disburse grayed-out + dialog. A 403 from the server refreshes the permission set, re-resolves, prunes, notifies once.

(8) ROLE-BASED DEPLOYMENT (§4.8 — rebalance deployment_plan per user-role type, LOAN OFFICER first): sequence delivery R0 Foundation → R1 LOAN/FIELD OFFICER (OFICIAL DE CAMPO, maker, TOP PRIORITY — a full field day offline) → R2 TELLER (CAJERO — deposit/withdraw/repayment) → R3 CHECKER/SUPERVISOR (REVISOR/SUPERVISOR — approvals + maker-checker inbox) → R4 TREASURER (TESORERO — disbursal) → R5 BRANCH OFFICER + COMPLIANCE (EJECUTIVO/KYC/PLD/CONTROL) → R6 ADMIN/SUPER USER (users/roles/config/accounting/products/org). Each phase makes one role's app fully usable end-to-end, gated on that role's real mifos-bank-2 permission codes. Materialize via /idea-deploy-plan rebalance.

Wire real action_contracts, reconcile flow.yaml with ui.yaml. Regenerate every touched screen through the design-conformance path (opus kmp-screen-gen, MOCKUP-FIRST, real bottom-sheet confirmations) so implementation matches the professional high-quality colorful Material Design mockups — mockups are high-fidelity full-color Material 3, not structural stubs. Verify on-device: DC-KMP static + design-conformance-device-verify per state (render mockup ↔ device, Maestro-drive every confirmation on_click md5-matched post am force-stop, confirm real data-fetch for loan-application + savings-application deep flows)."
```

---

## §6 · Execution note

Verdict is **COMPLETABLE** and the feedback adds **net-new capability** (nav-shell-assembler + network-config + role journeys + per-role dashboards + the 6 field-officer field-work features FO-1..FO-6 from §4.5 + the 3-tier permission-gating contract §4.7 + the role-based deployment plan §4.8, loan-officer-first) → the evolve chain fires. The evolve drive's implement phase IS the pending 32-screen design-conformance remediation, routed through the fixed opus/MOCKUP-FIRST/DC-KMP/device-verify path — so this plan and that remediation converge into one autonomous drive. Reference material for the drive: Fineract API (permission model + endpoints in §0), field-officer app adopt/improve lessons (§0), professional Material-3 full-color mockup standard (§4 pattern 5).

---

## Capability Status (dashboard-tracked · `/idea-evolve-plan` no-arg reads/writes this)

| # | id | capability | type | phase | status |
|---|---|---|---|---|---|
| 1 | nav-shell-assembler | role-adaptive nav shell (keystone — un-orphans 13 modules) | feature | R0 | ○ not-run |
| 2 | network-config | editable server/tenant/credentials + demo seed | feature | R0 | ○ not-run |
| 3 | permission-3tier-gating | FR-2 §4.7 — hide root / gray-out+"contact manager" dialog per code | contract | R0 | ○ not-run |
| 4 | role-deployment | §4.8 R0..R6 sequence (loan officer first) | roadmap | R0 | ○ not-run |
| 5 | orphan-nav-wiring | 13 module screens → inbound nav edges | wiring | R0 | ○ not-run |
| 6 | network-config-change-journey | settings/loan-area → edit → save → re-auth | journey | R0 | ○ not-run |
| 7 | m01-field-day-dashboard | loan-officer "My Field Day" assembly | screen | R1 | ○ not-run |
| 8 | loan-officer-day-journey | login → field day → centers → group → members → collection sheet → apply | journey | R1 | ○ not-run |
| 9 | FO-1-path-tracking | GPS field-visit route trail | feature | R1 | ○ not-run |
| 10 | FO-2-client-survey | survey list → question → submit + offline pre-download | feature | R1 | ○ not-run |
| 11 | FO-3-signature-capture | client signature (sign-pad/image) | feature | R1 | ○ not-run |
| 12 | FO-4-client-pinpoint | GPS geo-tag client location | feature | R1 | ○ not-run |
| 13 | FO-5-search-record | offline / recent-search history | feature | R1 | ○ not-run |
| 14 | FO-6-branch-download | per-entity offline hierarchy pre-download | feature | R1 | ○ not-run |
| 15 | account-action-fidelity | complete loan/savings action set + per-action gray-out gating (§4.6) | enrichment | R1 | ○ not-run |
| 16 | m01-admin-dashboards | admin "Operations" + super-user "Platform Admin" assemblies | screen | R6 | ○ not-run |
| 17 | super-user-admin-journey | login → admin dashboard → users/roles → config → approvals | journey | R6 | ○ not-run |

Legend: `○ not-run` · `◔ queued` · `◑ materializing` · `● done`. **Overall: draft (0/17 done).**
