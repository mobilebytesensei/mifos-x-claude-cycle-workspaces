# EVOLVE PLAN — Role-Based App Assembly

| | |
|---|---|
| **Project** | `mifos-x/mifos-x-backoffice-next-gen` |
| **Date** | 2026-08-01 |
| **Command** | `/idea-evolve-plan` (CP-A..CP-G whole-hierarchy completability sweep) |
| **Auditors** | 3 parallel (Fineract permission model · field-officer app journey audit · CP-A..CP-G idea-layer role-completability) |
| **Completability verdict** | **COMPLETABLE — additive work, 0 structural rearchitecture.** 6 blocking assembly/feature gaps + 8 explicit absences. The permission engine + 32 enriched screens already realize "same binary, every role"; the gaps are concentrated **nav-shell assembly wiring**, one **net-new network-config feature**, and **two role journeys**. |
| **Total gaps** | 17 findings (6 blocking · 11 additive/quality) across CP-A..CP-G |

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
2. **Sign-in only** (`fineract-auth-session`) — username + password + tenant. **Demo defaults pre-seeded** from core/network (dev/demo builds): `mifos` / `password` / tenant `default` @ demo.mifos.community. A **"Network settings"** affordance on the login screen opens the network-config feature (D2) to point at any instance.
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

## §5 · Enrich prompt (bottom-up the hierarchy — ready to run)

```
/idea-agent evolve "Assemble mifos-x-backoffice-next-gen as a role-based app: the same binary renders a distinct experience per logged-in user's Fineract role+permission (loan/field officer=maker, office+caseload scoped; admin/back-office=checker, office-subtree scoped; super user=ALL_FUNCTIONS+CHECKER_SUPER_USER, head office). Drive assembly off POST /authentication's {roles, permissions[], officeId, staffId}.

(1) REQUIREMENTS/FEATURES/ROADMAP: add FR + foundation feature 'nav-shell-assembler' (role-adaptive NavShell that data-binds bottom-bar/rail/drawer roots to permission-capability-engine's resolved module roster — replace app-shell.yaml drawer.items:[] and the hardcoded 4 field-officer bottom-nav placeholders with a permission-driven roster; adaptive: drawer/rail desktop, bottom-bar phone). Add FR + foundation feature 'network-config' (P0). Add FR for per-role dashboard assembly + first-run role walkthrough.

(2) FEATURE-DATA: add network-config data-flow — editable base URL + tenant (Fineract-Platform-TenantId) + username + password, persisted to core/network + core/datastore, with demo defaults (mifos/password/tenant default @ demo.mifos.community) SEEDED in core/network so the app is usable out-of-box; save swaps base-URL + tenant header (DynamicBaseUrlPlugin) and forces re-auth. Seed the same demo defaults into the sign-in form initial state (dev/demo builds).

(3) FLOWS/JOURNEYS: author 3 role journeys — 'loan-officer-day' (login→My-Field-Day dashboard→Centers(my office)→Center→Group→members(associate/disassociate)→generateCollectionSheet→bulk repayment+deposit→saveCollectionSheet; parallel: My Caseload→Client→apply loan/savings→pending-approval), 'super-user-admin' (login→Platform-Admin dashboard→Users(create/assign roles)→Roles&Permissions(grant codes/toggle maker-checker via PUT /permissions)→Organization→Config→Approvals checker-on-all), and 'network-config-change' (loan-area tile OR Settings→edit network→validate→save→re-auth). Wire orphan m03 center→group→member drill into nav; give all 13 orphan module screens inbound edges through the nav-shell assembler.

(4) SCREEN BEHAVIOR + DASHBOARD ASSEMBLY: build network-config screen (base-URL/tenant/username/password, demo pre-fill, Reset-to-demo, validators) with dual entry points (loan-area 'Network settings' tile + Settings). Make m01-dashboard assemble per role — loan-officer 'My Field Day' action feed (collections due today, overdue caseload loans, to-activate, pending applications, sync count), admin 'Operations' (approvals queue, portfolio KPIs, teller position), super-user 'Platform Admin' (platform health, all-office KPIs, user/role activity, config toggles). Loan-officer approve/disburse controls render DISABLED-with-reason; every maker-checker write shows a bottom-sheet confirmation (NOT a bare toast).

Wire real action_contracts, reconcile flow.yaml with ui.yaml. Regenerate every touched screen through the design-conformance path (opus kmp-screen-gen, MOCKUP-FIRST, real bottom-sheet confirmations) so implementation matches the professional high-quality colorful Material Design mockups — mockups are high-fidelity full-color Material 3, not structural stubs. Verify on-device: DC-KMP static + design-conformance-device-verify per state (render mockup ↔ device, Maestro-drive every confirmation on_click md5-matched post am force-stop, confirm real data-fetch for loan-application + savings-application deep flows)."
```

---

## §6 · Execution note

Verdict is **COMPLETABLE** and the feedback adds **net-new capability** (nav-shell-assembler + network-config + role journeys + per-role dashboards) → the evolve chain fires. The evolve drive's implement phase IS the pending 32-screen design-conformance remediation, routed through the fixed opus/MOCKUP-FIRST/DC-KMP/device-verify path — so this plan and that remediation converge into one autonomous drive. Reference material for the drive: Fineract API (permission model + endpoints in §0), field-officer app adopt/improve lessons (§0), professional Material-3 full-color mockup standard (§4 pattern 5).
