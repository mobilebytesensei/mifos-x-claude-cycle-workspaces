# Companion API — Build & Deploy Spec (mcp-mifosx)

> The **actionable end-to-end plan** for realizing the companion API that CommonPurse consumes.
> `/mifos-bridge` produced the **contract** (`API_CONTRACT.yaml` companion section: 20 tools + 6 datatables);
> this doc is the **runtime**: what to build in `mcp-mifosx`, how to provision the datatables, and how to
> deploy — so `/device-test` can pass and matrix-green becomes reachable.
>
> Source of truth for behavior: `idea-layer/ARCHITECTURE.md` (topology + build-spec) + `API_CONTRACT.yaml`
> (companion tool contracts). Reuse vehicle: `/mifos-bridge` (contract) → this spec (implement + deploy).

---

## 0. Why this exists (the one thing /idea-agent can't do)

`/idea-agent` governs the app + idea-layer + implementation to source. It **cannot deploy infrastructure**.
Device-behavior verification (`/device-test`, RULE-IMPL-BEHAVIOR-EXECUTED-001) needs a **live** backend the
app can actually call. So `matrix-green` is gated on this spec being executed. Everything below is Fineract-only
+ mcp-mifosx — no Supabase, no standalone DDD service (per ARCHITECTURE.md non-goals).

---

## 1. Build in `mcp-mifosx` (canonical impl = Go; extension pattern per capability audit)

The Go impl (`source/mcp-mifosx/go/`) is the canonical, most-complete server. New tools are declarative
`BaseToolDef` structs (~10 lines each) in `go/tools/<domain>.go` + one line in `RegisterAllTools()`
(`go/tools/registry.go`). The generic handler substitutes path/query/body vars — no per-tool handler code.

### 1a. TIER-1 tools — thin wraps over existing Fineract endpoints (`go/tools/companion_*.go`)

| Contract | Endpoint (companion) → composes Fineract | Notes |
|---|---|---|
| **COMP-AUTH-001** self-register | `POST /companion/auth/self-register` → Fineract `POST /self/registration` + `/self/registration/user` | ⚠ needs auth-model change (§1c) + self-service-enabled Fineract (§3) |
| **COMP-AUTH-002** login | `POST /companion/auth/login` → `POST /authentication` (or `/self/authentication`) then reads group memberships | returns groups[] + per-group role for capability resolution |
| **COMP-AUTH-003** me | `GET /companion/auth/me` → session identity + memberships | bearer |
| **COMP-GRP-001** create/read group | `POST\|GET /companion/groups*` → `POST /groups` (+activate) / `GET /groups/{id}?associations=all` | organizer-scoped via service credential (self-scope can't do groups) |
| **COMP-GRP-002** activate | `POST /companion/groups/{id}/activate` → `POST /groups/{id}?command=activate` | |
| **COMP-GRP-003** associate-clients | `POST /companion/groups/{id}/associate-clients` → `POST /groups/{id}?command=associateClients` | invite-accept path |
| **COMP-GRP-004** assign-role | `POST /companion/groups/{id}/assign-role` → `POST /groups/{id}?command=assignRole` + writes `dt_member_role` | |
| **COMP-GRP-005** assign-staff | `POST /companion/groups/{id}/assign-staff` → `command=assignStaff` | organizer-as-loan-officer; P1 |
| **COMP-CAL-001..003** calendar + collection-sheet | `POST /companion/groups/{id}/calendar` · `GET\|POST .../collection-sheet` → `/{groups}/{id}/calendars` + `generateCollectionSheet`/`saveCollectionSheet` | meeting cadence + attendance; currently ABSENT in mcp — build |

### 1b. TIER-2 tools — datatable CRUD (`go/tools/datatables.go` — the P0 one-time build)

The mcp server today only has read-only `list_datatables`. Build the generic datatable-CRUD set (each a thin wrap):

| Contract | Endpoint → Fineract |
|---|---|
| **COMP-DT-001** register datatable | `POST /companion/datatables/register` → `POST /datatables` + `POST /datatables/register/{table}/{apptable}` |
| **COMP-DT-002** create row | `POST /companion/datatables/{table}/{entityId}` → `POST /datatables/{table}/{entityId}` |
| **COMP-DT-003** read row(s) | `GET /companion/datatables/{table}/{entityId}` → `GET /datatables/{table}/{entityId}` (entityId=0 ⇒ catalogue SELECT-all, per CK1) |
| **COMP-DT-004** update row | `PUT /companion/datatables/{table}/{entityId}` |
| **COMP-DT-005** delete row | `DELETE /companion/datatables/{table}/{entityId}` |
| **COMP-DIST-001/002** distribution execute | `POST /companion/groups/{id}/{shareout,rotation}/execute` → validates corpus, then drives GSIM withdrawal / account-transfer + journal | client computes payout; server re-validates + executes (CK4) |

### 1c. Auth-model change (the one structural lift — P0)

The mcp adapter today is **stateless single-env-credential**. Companion self-signup + per-user role resolution
requires **per-call user credentials**: the login/self-register tools accept `username`/`password`, mint a
session, and the group-orchestration tools execute back-office calls with a **service credential** while
enforcing organizer-vs-member authz in this tier (Fineract self-scope grants only one privilege class).
This is the backbone — the ONE genuinely-new build; everything else is thin wraps.

---

## 2. Datatable provisioning (run once at deploy, via COMP-DT-001)

Register these 6 companion datatables (full schemas in `API_CONTRACT.yaml#companion_datatables`):

| Datatable | Apptable | Purpose |
|---|---|---|
| `dt_group_type_config` | `m_group` | the `GroupTypeConfig` per group (2-axis + params) — 9 seeded types |
| `dt_companion_invitations` | `m_group` | invite tokens (create/list/validate/accept/revoke) |
| `dt_rosca_rotation` | `m_group` | ROSCA rotation order + received-flag |
| `dt_rosca_auction` | `m_group` | chit/hui bids + winning discount |
| `dt_vsla_cycle` | `m_group` | share value + cycle + computed share-out |
| `dt_welfare_fund` | `m_group` | social/welfare fund ledger |

CK3: `dt_group_type_config` (archetype registry) is distinct from the template's `dt_group_config` (per-group instance);
the create-group orchestrator reads the registry and writes the per-group table.

---

## 3. Deploy (the external gate for device-green)

1. **Fineract instance with self-service ENABLED** — the community sandbox (`sandbox.mifos.community`) does **not**
   have `/self/*` on. Stand up a Fineract deployment with the self-service module enabled; optionally add the
   **openMF `selfservice-plugin`** to harden self-registration (FINERACT-2392 double-persist bug).
2. **Tenant / office strategy** for global "anyone in the world" onboarding into Fineract's office-scoped model:
   single global office (v1) or office-per-region.
3. **Deploy the mcp-mifosx server** (Go, SSE transport via `PORT`) with the service credential + tenant header,
   reachable by the app.
4. **Provision the 6 datatables** (§2) against that Fineract, once.
5. **Wire the app** — point CommonPurse's companion base URL at the deployed mcp-mifosx.

---

## 4. End-to-end verification (device-green path)

Once §1–§3 land: the app calls `/companion/*` → mcp-mifosx → Fineract; `/device-test` (Maestro on the 2 devices)
can exercise real signup → create group → invite → savings/loan/meeting → share-out; RULE-IMPL-BEHAVIOR-EXECUTED-001
passes; `matrix-green` becomes reachable. Until then, implemented features compile + build-green but device-test
returns the declared `pending-device-verify` (not a failure — the honest external gate).

---

## 5. Bridge auto-migrate — runnable migrations closed loop (S10 / FR-029)

`/mifos-bridge` historically emitted only the **contract** (`API_CONTRACT.yaml` + `BRIDGE_AUDIT_LOG.yaml`).
As of 2026-08-01 the bridge also **emits runnable migrations** so "add a feature → migrate its
missing API" is a closed loop, not a prose to-do:

```
/mifos-bridge --auto                         (feature adds a datatable-backed API)
        │
        ├─ resolves the gap (TIER 1 / TIER 2)           → API_CONTRACT.yaml   (contract, as before)
        ├─ appends the register definition               → server-layer/migrations/datatables/datatables.manifest.json
        └─ logs the emit                                  → BRIDGE_AUDIT_LOG.yaml (_migration_emit)
```

- The **emit target** is `server-layer/migrations/datatables/datatables.manifest.json` — every
  TIER-2 datatable the bridge resolves has a corresponding register entry there, applied by
  `server-layer/migrations/register-datatables.sh`.
- The **demo seed** (`server-layer/migrations/seed-demo/`) is regenerated from the same
  `demo-fixture.json` SoT and stays consistent with `idea-layer/PROJECT_DEMO_DATA.yaml`.
- Re-running the bridge is **idempotent**: an already-present datatable keeps its existing
  register entry; a new one is appended.

### What is RUNNABLE now vs what remains GATED on the live-server deploy

| Deliverable | State | Where |
|---|---|---|
| 21 datatable register definitions | **runnable** (offline `--dry-run` clean) | `migrations/datatables/datatables.manifest.json` + `register-datatables.sh` |
| Demo-data seed (user, group, savings, meetings, corpus, cycle, invite `DEMO24`) | **runnable** (offline `--dry-run` clean) | `migrations/seed-demo/seed-demo.sh` + `demo-fixture.json` |
| Offline demo fixture (Demo Explore) | **done** | `idea-layer/PROJECT_DEMO_DATA.yaml` |
| 4 materialized api group files (clients-members/savings/share-out/field-officer) | **done** | `idea-layer/server/apis/*.yaml` |
| Meeting-calendar + collection-sheet contract (COMP-CAL) | **done** (contract) | `API_CONTRACT.yaml#companion_api` |
| `GET /loans` list + advanceCycle/disburse/list_meetings map fixes | **done** | `API_CONTRACT.yaml` + `idea-layer/server/apis/*.yaml` |
| **Applying** the migrations + seed against a real Fineract | **GATED** — needs live Fineract (self-service enabled) | §3 above (external gate) |
| Companion `mcp-mifosx` Go service (COMP-AUTH/GRP/CAL/DT/DIST tools) | **GATED** — deferred Go build, not deployed | §1 above (external gate) |
| Device-green (`/device-test` Maestro over live network) | **GATED** — depends on the two rows above | §4 above |

> Bottom line: everything the drive can author is authored and offline-verified. The single
> remaining blocker is the **live-server deploy** (§1–§3) — a human-gated infra step. Until it
> lands, implemented features build-green and device-test returns the honest
> `pending-device-verify`, never a false green (RULE-IMPL-BEHAVIOR-EXECUTED-001).

## Reference
- Migrations (runnable): `server-layer/migrations/` (`README.md` + `register-datatables.sh` + `seed-demo/`)
- Contract: `server-layer/API_CONTRACT.yaml` (companion section) · `BRIDGE_AUDIT_LOG.yaml` (per-tool resolution + CK1–CK4)
- Design SoT: `idea-layer/ARCHITECTURE.md` (§3 build-spec + deployment decisions)
- Vehicle: `/mifos-bridge` (contract generation) · mcp repo: `workspaces/mifos-x/mcp-mifosx`
- Capability audit basis: Go extension pattern (`go/tools/registry.go`); TIER-1/TIER-2 two-tier resolution (RULE-MIFOS-BRIDGE-001)
