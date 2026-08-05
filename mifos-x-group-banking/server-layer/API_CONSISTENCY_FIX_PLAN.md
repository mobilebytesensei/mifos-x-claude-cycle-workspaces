# API Consistency + Access-Level — Fix Plan (Group-centric, production-stable)

**Project:** mifos-x-group-banking (MifosSave)
**Created:** 2026-08-05 · **Revised:** 2026-08-05 (decision flipped to Group-centric)
**Owner:** Rajan Maurya
**Trigger:** User-flagged recurring inconsistency (RULE-USER-FLAGGED-DEFECT-HEAL-001) — one logical
"group" split across two Fineract entities; datatable name/parent/column/count drift; unresolvable
mcp_tool bindings. Full audit → §1.

---

## DECISION (locked, revised)

**Group-centric.** The savings group **is** a Fineract **Group** (`m_group`, keyed by `groupId`).
Members (`m_client`) associate to the Group; the Group holds its state, meetings, savings (GSIM), and
loans (GLIM). **Center is dropped from the per-group unit** — reserved only for an OPTIONAL future
federation layer (a cluster of multiple groups that meet/collect jointly), which is not a MifosSave
feature today.

Why the flip (from the earlier "Center+Group pair"): Fineract's hierarchy is
`m_center ⊃ m_group ⊃ m_client`. **Members live on the Group, so the group's identity + state belong on
the Group** — putting them on the Center placed state one level *above* the members and forced a
two-id `{centerId, groupId}` smear (the source of the real bug). A MifosSave savings group is always a
single group of members → the Center was empty overhead. Removing it collapses the group to one id and
matches the hierarchy exactly.

### ACCESS-LEVEL POLICY (new, user-directed)

**AL-RULE:** Any capability whose native Fineract API is **not available at the required access level**
(a self-signed-up organizer or member = a Fineract **self-service** client) is modeled as a
**datatable on the owning entity, read/written by the companion with a service credential** — never
left unreachable, and never by forcing a self-service client to call a staff-only endpoint directly.

Three mechanisms, in priority order:
1. **native self-service** — the `/self/*` surface a self-service client can call directly (own
   profile, own savings, own loans). Use when it exists.
2. **companion service-exec** — a staff-only native endpoint the companion runs on the user's behalf
   with a service credential after authz (create group, associateClients, post transactions, group
   reads). Use when a native staff API exists but the user can't reach it.
3. **datatable via companion** — when Fineract has **no** native API at the right level (VSLA/ROSCA
   state, corpus, share-out ledger, group-type config, meeting schedule/record if the group calendar
   isn't self-service-reachable). This is the AL-RULE fallback.

---

## §0. Canonical model (target SoT)

```
m_group  = THE savings group   → owns: state (13 datatables), meetings, GSIM savings, GLIM loans
   └─ m_client = member          → owns: 6 per-member datatables
        └─ m_loan = a loan        → owns: 2 per-loan datatables
[ m_center = OUT OF SCOPE for v1 — optional federation of multiple groups only ]
```

**Invariants (gated in Phase 2):**
- INV-1 `groupId` is the single group identity. No `centerId` anywhere in the per-group unit.
- INV-2 Each datatable keyed by its TRUE parent id: `m_group`→groupId, `m_client`→clientId,
  `m_loan`→loanId.
- INV-3 One canonical name per datatable (single `dt_` prefix), one parent, one column set — defined
  once in `DATATABLE_REGISTRY.yaml`, derived everywhere else.
- INV-4 Every endpoint's `mcp_tool` resolves to a defined tool in the contract catalog.
- INV-5 (access) Every capability maps to native-self-service | companion-service-exec |
  datatable-via-companion per the §0.1 matrix. No self-service client calls a staff-only endpoint
  directly; no capability is left unreachable.

**Datatable → parent map (21, re-parented to Group-centric):**
- `m_group` (13): dt_group_config · dt_group_corpus · dt_meeting_record · dt_share_out · dt_social_fund
  · dt_sync_metadata · dt_group_loan_policy *(these 7 MOVE from m_center → m_group)* + dt_group_type_config
  · dt_companion_invitations · dt_rosca_rotation · dt_rosca_auction · dt_vsla_cycle · dt_welfare_fund
  *(already m_group)*. **+ NEW dt_meeting_schedule** if the group calendar isn't self-service-reachable
  (AL-RULE) → 13 or 14.
- `m_client` (6): dt_member_role *(add `group_id` col)* · dt_meeting_attendance · dt_loan_request ·
  dt_member_ceiling_override · dt_notification · dt_member_invitation
- `m_loan` (2): dt_loan_vote · dt_loan_guarantor

Note: `dt_group_type_config` (global archetype registry, entityId=0) and `dt_group_config` (per-group
instance) are BOTH on m_group but DISTINCT — documented, not merged.

### §0.1 Access-level → mechanism matrix (starter — finalized in Phase 1.5)

| Capability | Native Fineract API | Self-service reachable? | Mechanism (chosen) |
|---|---|---|---|
| Sign in (organizer/member) | `POST /self/authentication` | ✅ | native self-service |
| Own profile / savings / loans | `/self/clients/{id}`, `/self/savingsaccounts`, `/self/loans` | ✅ | native self-service |
| Create group | `POST /groups` (+activate) | ❌ staff | companion service-exec |
| Associate members | `POST /groups/{id}?command=associateClients` | ❌ | companion service-exec |
| Assign role | group `assignRole` | ⚠️ partial | companion + `dt_member_role` |
| Create client (member) | `POST /clients` | ❌ | companion service-exec |
| Open savings (GSIM) | `POST /savingsaccounts` | ❌ | companion service-exec |
| Post deposit / repayment | `POST /savingsaccounts/{id}/transactions`, `/loans/{id}/transactions` | ❌ | companion service-exec |
| Loan apply / approve / disburse | `POST /loans`, `/loans/{id}?command=…` | ❌ | companion service-exec |
| **Schedule meeting** | `POST /groups/{id}/calendars` | ❌ not self-service | **`dt_meeting_schedule` on m_group via companion (AL-RULE)** |
| Meeting record / attendance / corpus | none native | — | datatables (m_group / m_client) via companion |
| Group savings summary | none at self-service | ❌ | companion BFF `/companion/groups/{id}/savings` |
| VSLA/ROSCA state, share-out, welfare | none native | — | datatables on m_group via companion |
| Group members list | `GET /groups/{id}/clients` | ❌ | companion service-exec |
| Batch offline replay | `POST /batches` | ❌ | companion service-exec |

**Rule applied:** every ❌/— row resolves to companion or datatable — never a raw staff call from the
app, never an unreachable capability.

---

## §1. The inconsistencies (audit result — what we are fixing)

Severity: 8 HIGH · ~10 MED · ~8 LOW across 5 classes.

- **Class 1 — Entity split (8, 4 HIGH):** group modeled as Center AND Group. Now RESOLVED by the
  Group-centric decision (Center removed). HIGH BUG: 6 companion `m_group` tables addressed by
  `centerId` — fixed by INV-2 (all groupId).
- **Class 2 — Datatable name drift (3, 2 HIGH):** `group_type_config` vs `dt_group_type_config`;
  `invitations` vs `dt_companion_invitations`; invitation concept duplicated on m_client + m_group.
  Fixed by DATATABLE_REGISTRY (INV-3).
- **Class 3 — Column/count drift (6):** api_manifest lists 11 of 15 tier-2 tables; `dt_member_role`
  missing `group_id`; truncated columns (dt_group_config 5/11, dt_meeting_record 7/12,
  dt_group_corpus 5/9, dt_loan_vote 5/6). Fixed by registry-derived manifest.
- **Class 4 — mcp_tool binding drift (6):** `list_accounts` + `list_group_loans` UNDEFINED;
  approve+disburse share one `?command=approve` tool (404 class); reused tools; 4 conflicting role
  enums. Fixed in Phase 4 under MB-8.
- **Class 5 — Rollup/doc drift (~7):** MCP tool count 65 vs 116 vs 101; stale post-pivot screens;
  phantom `/meetings` resource. Fixed by generating docs from the contract.

**Root cause:** `/mifos-bridge` derives bottom-up from per-screen `api.yaml` and never reconciles
against `ARCHITECTURE.md`, an entity-model SoT, or a datatable registry; its 4 gates are per-item.
Three artifacts re-author the same facts independently → drift is structural. The Center choice
originated in `screens/{meeting-conduct,group-create,group-dashboard}/api.yaml`.

---

## §2. Execution order (WHY)

Durable fix (Phases 1–2) BEFORE cleanup (3–7): the SoT + gate must exist first so every regeneration
is checked, and the per-screen origin (Phase 3) must be fixed before regenerating (Phase 4) or the
bridge re-derives the drift. The Group-centric flip makes Phase 3 + Phase 6 larger (real Center→Group
migration + client-layer rework) — done incrementally, each phase device-verified, never a big-bang.

| Phase | Scope | Gate to advance |
|---|---|---|
| 1 SoT | project idea-layer | ENTITY_MODEL + DATATABLE_REGISTRY + ACCESS_MATRIX + ARCHITECTURE agree (Group-centric) |
| 1.5 Access audit | project | every capability classified per §0.1; datatable-fallbacks identified |
| 2 Root-cause heal | framework | MB-5..MB-9 gate + RED→GREEN canary; bridge reads SoT top-down |
| 3 Fix origin | project idea-layer (screens) | screen api.yaml Center→Group; no centerId; conform to SoT |
| 4 Regenerate | project (dispatched bridge) | `/mifos-bridge --auto` passes MB-5..MB-9; tools + enum fixed |
| 5 Rollup docs | project server-layer | API.md/API_INDEX counts generated from contract |
| 6 App + device | project source | client layer Center→Group; Maestro + on-device on mifos-bank-2 |
| 7 Site | project idea-layer/site | `/idea-site update` → api.html + ERD refreshed → deploy |
| 8 Commit | all 3 repos | `/git-session-commit` bottom-up |

---

## §3. Phase detail

### Phase 1 — Establish SoT (idea-layer; Claude Intelligence only, RULE-CI-001)
- [ ] 1.1 Rewrite `idea-layer/ARCHITECTURE.md` entity section → Group-centric: the savings group is a
  Fineract Group; members associate to it; meetings + state on m_group; Center = optional federation
  only (explicit non-goal for v1). Dated + authoritative.
- [ ] 1.2 Create `idea-layer/server/ENTITY_MODEL.yaml` — `group_entity: m_group`, `key: groupId`,
  member/loan/savings relations, INV-1..INV-2, Center marked out-of-scope.
- [ ] 1.3 Create `idea-layer/server/DATATABLE_REGISTRY.yaml` — 21 rows (`name → parent, entitySubType,
  multi_row, dt_prefix_canonical, columns[]`), re-parented per §0 (the 7 state tables → m_group). Seed
  from `datatables.manifest.json` (most complete), apply re-parenting + `dt_member_role.group_id`.
- [ ] 1.4 Create `idea-layer/server/ACCESS_MODEL.yaml` — the §0.1 matrix as data: per capability
  `{native_api, self_service_reachable, mechanism, datatable_ref?}` + the AL-RULE statement.
- **Accept:** 4 SoT artifacts agree; REGISTRY has 21 rows on {m_group:13, m_client:6, m_loan:2}; no
  centerId; ACCESS_MODEL classifies every capability.

### Phase 1.5 — Access-level audit (project; Claude Intelligence + FINERACT_API_CATALOG)
- [ ] 1.5.1 For each capability in `apis/*.yaml`, classify against the self-service surface (read
  `workspaces/mifos-x/mcp-mifosx/server-layer/FINERACT_API_CATALOG.yaml` + Fineract self-service docs).
- [ ] 1.5.2 Where a native API is NOT self-service-reachable AND no companion staff-exec path fits →
  define a datatable (AL-RULE). Confirm/introduce `dt_meeting_schedule` on m_group if
  `/groups/{id}/calendars` is not reachable at the organizer access level.
- **Accept:** ACCESS_MODEL complete; every ❌ row has a companion or datatable mechanism; new
  datatables added to DATATABLE_REGISTRY.

### Phase 2 — Root-cause heal (framework; RULE-USER-FLAGGED-DEFECT-HEAL-001; TDD RED→GREEN)
- [ ] 2.1 RED canary — `capsules/idea/mifos-bridge/tests/api-consistency-canary/red/` reproducing:
  centerId-keyed m_group table, `group_type_config` vs `dt_group_type_config`, duplicate invitation
  table, undefined `list_accounts`, a self-service client calling a staff-only endpoint. Gate FAILS.
- [ ] 2.2 Add gate `MB-5..MB-9` to `capsules/idea/mifos-bridge/verify/verify.sh`:
  - MB-5 entity conformance (group-level uses ENTITY_MODEL key `groupId`; matches ARCHITECTURE; no centerId).
  - MB-6 datatable name/parent conformance (API_CONTRACT + api_manifest + manifest.json == REGISTRY).
  - MB-7 single-parent uniqueness (no concept under two parents).
  - MB-8 count agreement + mcp_tool-catalog resolvability (every mcp_tool defined; counts == registry).
  - MB-9 (NEW) access-level conformance — every capability's mechanism matches ACCESS_MODEL; no app
    endpoint requires a self-service client to hit a staff-only path directly; unreachable-native →
    must have a datatable/companion fallback.
  - RULE-CI-001: idea-layer reconciliation = Claude-intelligence; verify.sh may diff project-layer
    `datatables.manifest.json` (server-layer, shell OK) against the registry.
- [ ] 2.3 GREEN — wire the gate; register in `core/registries/COHERENCE_CATALOG.yaml`; green fixture passes.
- [ ] 2.4 Bridge reads SoT top-down: add `ENTITY_MODEL.yaml` + `DATATABLE_REGISTRY.yaml` +
  `ACCESS_MODEL.yaml` + `ARCHITECTURE.md` to `layers/idea/commands/mifos-bridge.md` STEP 0; assert
  conformance in STEP 3/6 (reconcile-then-emit) in `_shared/mifos-bridge-analyze-resolve.md` +
  `_shared/mifos-bridge-contract-status.md`.
- **Accept:** RED fails, GREEN passes, gate registered; bridge STEP 0 lists the 4 SoT reads.

### Phase 3 — Fix the origin: per-screen api.yaml (idea-layer; Claude Intelligence)
- [ ] 3.1 Rewrite `screens/{group-create,group-dashboard,meeting-conduct,share-out,group-list,
  member-add,field-officer-dashboard}/api.yaml` + DTOs: `POST /centers`→`POST /groups`;
  `/centers/{centerId}`→`/groups/{groupId}`; all `/datatables/{t}/{centerId}`→`/{groupId}`; DTO
  `fineractCenterId`→`fineractGroupId`; meetings via group calendar (companion) or `dt_meeting_schedule`
  per Phase 1.5.
- **Accept:** no screen references a center or keys a datatable by centerId; screens pass MB-5..MB-9 preflight.

### Phase 4 — Regenerate the contract (dispatched, gated)
- [ ] 4.1 `/mifos-bridge --auto` → regenerates API_CONTRACT.yaml + api_manifest.yaml +
  datatables.manifest.json from SoT; MB-5..MB-9 block residual divergence.
- [ ] 4.2 Fix tool bindings: define/rebind `list_accounts` + `list_group_loans`; split
  `approve_disburse_loan` → `approve_loan` + `disburse_loan`; unify `dt_member_role.role` enum; ensure
  `group_id` column present. Re-provision datatables under new parents (register migrations regenerated).
- **Accept:** bridge green; api_manifest lists all datatables with full columns on m_group/m_client/m_loan;
  every mcp_tool resolves; every capability access-classified.

### Phase 5 — Regenerate rollup docs
- [ ] 5.1 `server-layer/API.md` + `API_INDEX.md` counts generated/reconciled from API_CONTRACT (one
  MCP-tool number); drop phantom `/meetings`; remove stale screen names.
- **Accept:** no count contradiction; no dropped-screen references.

### Phase 6 — Propagate to app + device-verify (source; device-truth)
- [ ] 6.1 Client layer/services/repos + DTOs: replace all center endpoints/ids with group; re-key
  datatable calls to groupId; wire the meeting-schedule datatable if introduced; route each capability
  through its ACCESS_MODEL mechanism (self / companion / datatable).
- [ ] 6.2 Re-provision the 21 (+meeting-schedule) datatables on the target instance under the new
  parents (`server-layer/migrations/` regenerated); re-seed demo data on m_group.
- [ ] 6.3 `/kmp-implement` touched features; Maestro + on-device verify on `mifos-bank-2` (fresh
  capture AFTER `am force-stop`, device-APK md5 == built md5). No "fixed" without a capture.
- **Accept:** create-group → meeting-conduct → share-out flows pass on-device against a Group entity;
  companion reads/writes hit `groupId`; self-service reads use `/self/*`.
- **Note:** this is the largest phase (Center→Group is a real migration) — sequence feature-by-feature,
  each device-verified, never all-at-once.

### Phase 7 — Refresh the site
- [ ] 7.1 `/idea-site update` → re-author api.html + ERD from consistent sources → deploy to Netlify
  (site 8939b862-…). Verify live (RULE-WEB-DEBUG-001). ERD now shows a single `m_group` root
  (+ m_client, m_loan); Center gone from the per-group view.
- **Accept:** ERD + tables show the Group-centric model; counts match the regenerated manifest.

### Phase 8 — Commit
- [ ] 8.1 `/git-session-commit --all` — bottom-up source → workspace → framework.

---

## §4. Safety / stability guardrails
- Phases 1–2 make recurrence machine-impossible (gate MB-5..MB-9 + canary) before any regeneration.
- Incremental, not big-bang: Phase 6 migrates feature-by-feature, each device-verified.
- Every source/app change device-verified before "done" (RULE-VERIFY-COMPLETION-001, device-truth).
- Bridge becomes reconcile-then-emit → future features can't reintroduce entity/datatable/access drift.
- The Center→Group migration is the deliberate cost of correctness (members + state on one entity, one
  id); the AL-RULE guarantees no capability becomes unreachable in the process.
- Rollback: SoT files + gate are additive; the working contract is not destroyed until Phase 4
  regenerates under the gate; the old center-based datatables can coexist until re-provisioned.

## §5. Files touched (inventory)
- **New (project idea-layer):** `server/ENTITY_MODEL.yaml`, `server/DATATABLE_REGISTRY.yaml`,
  `server/ACCESS_MODEL.yaml`
- **Edit (project idea-layer):** `ARCHITECTURE.md`, `server/apis/*.yaml` (regenerated),
  `server/api_manifest.yaml` (regenerated), `screens/{group-create,group-dashboard,meeting-conduct,
  share-out,group-list,member-add,field-officer-dashboard}/api.yaml` + DTOs, `site/api.html` (via /idea-site update)
- **Edit (project server-layer):** `API_CONTRACT.yaml`, `datatables/datatables.manifest.json`,
  `register-datatables.sh`, `seed-demo/*`, `API.md`, `API_INDEX.md` (regenerated)
- **New/Edit (framework):** `capsules/idea/mifos-bridge/verify/verify.sh` (MB-5..MB-9),
  `capsules/idea/mifos-bridge/tests/api-consistency-canary/{red,green}/`,
  `layers/idea/commands/mifos-bridge.md`, `_shared/mifos-bridge-analyze-resolve.md`,
  `_shared/mifos-bridge-contract-status.md`, `core/registries/COHERENCE_CATALOG.yaml`
- **Edit (project source):** client layer/services/repos/DTOs (Phase 6 — Center→Group migration)

## §6. Status log
- 2026-08-05 — plan created; decision Center+Group pair.
- 2026-08-05 — **decision flipped to Group-centric** (members live on the Group → group state belongs
  on the Group; Center dropped, federation-only). Added ACCESS-LEVEL POLICY (AL-RULE): native API not
  reachable at self-service level → datatable via companion. Added Phase 1.5 + gate MB-9 + ACCESS_MODEL.yaml.
- 2026-08-05 — **Phase 1 DONE** (SoT keystone): authored `idea-layer/server/ENTITY_MODEL.yaml`,
  `DATATABLE_REGISTRY.yaml` (21 tables re-parented: m_group 14 / m_client 5 / m_loan 2; +dt_meeting_schedule
  provisional; dt_member_invitation deprecated→dt_companion_invitations), `ACCESS_MODEL.yaml`; pinned the
  Group-centric entity model in `ARCHITECTURE.md` §1.1.
- 2026-08-05 — **Phase 2 DONE** (root-cause heal, framework, RED→GREEN verified): `datatable-conformance.sh`
  mechanical checker + RED/GREEN canary (catches m_center parent · un-prefixed name · duplicate-parent);
  `verify.sh` MB-5..MB-9 (RED confirmed → GREEN after wiring); `mifos-bridge.md` STEP 0 reads the 3 SoT files
  + STEP 3.5 reconcile-then-emit; `_shared/mifos-bridge-sot-conformance.md`; COHERENCE_CATALOG E60-E62.
- 2026-08-05 — **Phase 3-4 DONE + verified**: server-layer datatables.manifest.json (gate PASS, 21 tables,
  m_group 14/m_client 5/m_loan 2, no m_center) · idea-layer apis/*.yaml + screens/*/api.yaml +
  api_manifest.yaml (0 residual centerId/centers; approve/disburse split; role enum unified). Fixed the
  field-officer duplicate → 51 endpoints (counts reconciled).
- 2026-08-05 — **Phase 5 DONE + verified**: API.md + API_INDEX.md reconciled — Center→Group, 0 residual
  m_center/centers, single MCP-tool total 101 (= API_CONTRACT SoT), phantom /meetings removed.
- 2026-08-05 — **Phase 7 DONE + verified live**: site/api.html re-authored Group-centric (51 endpoints,
  ERD 4→3 lanes m_office→m_group→m_client→m_loan, datatables re-parented + dt_meeting_schedule);
  deployed to https://mifossave.netlify.app (HTTP 200); ERD rendered on-device (3 lanes, no Center).
- **REMAINING — Phase 6 (app client-layer + on-device verify) + Phase 1.5 live mifos-bank-2 spike**:
  HALT `pending-device-verify` — external dependency (live Fineract/companion + device/build env). All
  contract/site/framework work authored + verified; the on-device proof + client-layer migration await
  the live instance. Phase 8 commit follows this entry.
