# Architecture — MifosSave (mifos-x-group-banking)

> Global self-signup community-banking app. **Backend strategy: Fineract-only** (the ledger) + a **companion API** (extended `mcp-mifosx`) for the missing behavior, with VSLA/ROSCA/SFG state as Fineract **datatables**. No Supabase, no standalone DDD service.
>
> The backend is an **abstract contract the app consumes**; the concrete backend is designed later, fully compatible with the spec below. Materialized by the 2026-07-17 global self-signup evolve.

---

## 1. Topology (3 tiers)

```
┌─────────────────────────────────────────────┐
│  MifosSave KMP app                          │  single login/signup · offline-first (Store5/SQLDelight)
│  organizer + member surfaces resolved per-group │  client-side share-out / rotation compute (preview)
└───────────────────────┬─────────────────────┘
                        │  REST — app never talks to Fineract directly
┌───────────────────────▼─────────────────────┐
│  COMPANION API  (extended mcp-mifosx, Go — built later)
│  · per-user auth + self-registration bridge   │  ← the one real "new build"
│  · self-user → back-office group orchestration │     (executes group ops with a service credential)
│  · datatable-CRUD (provisions group-type state)│
│  · executes client-computed money moves        │  (idempotent, server re-validates money moves)
└───────────────────────┬─────────────────────┘
                        │  Fineract REST (service credential)
┌───────────────────────▼─────────────────────┐
│  APACHE FINERACT CORE  (system of record for MONEY)
│  clients · groups · GLIM · GSIM · collection-sheet · calendar
│  savings · loans · interest · charges · GL · transactions
│  + custom datatables: group_type_config · rosca_rotation · rosca_auction · vsla_cycle · welfare_fund · invitations
└─────────────────────────────────────────────┘
```

**Division of record:** Fineract owns *money* (client registry, savings balances, loan accounts, interest, GL). The companion API owns *coordination* (identity bridge, group orchestration, group-type state). The **app** owns *offline UX + distribution compute (preview)*.

### 1.1 Entity model — Group-centric (SoT: `server/ENTITY_MODEL.yaml`)

The savings group **is** a Fineract **Group** (`m_group`, keyed by `groupId`) — members associate to it,
and it natively owns group roles, GSIM (group savings) and GLIM (group loans). Hierarchy `m_group ⊃ m_client ⊃ m_loan`.
A MifosSave savings group is always ONE group of members.

- **All group state is a datatable on `m_group`** (13) — see `server/DATATABLE_REGISTRY.yaml` (the single
  datatable SoT: name · parent · columns for all 21). Per-member datatables (5) on `m_client`, per-loan (2) on `m_loan`.
- **Access-level rule (AL-RULE, SoT `server/ACCESS_MODEL.yaml`):** organizers + members are Fineract
  self-service clients. Any capability whose native API is not reachable at that level is served by the
  companion (staff service-exec) or, where Fineract has no native API at all, by a **datatable via the companion**
  — e.g. the meeting schedule (`dt_meeting_schedule`, since `/groups/{id}/calendars` is not self-service-reachable).

These three files (`ENTITY_MODEL.yaml` · `DATATABLE_REGISTRY.yaml` · `ACCESS_MODEL.yaml`) are read top-down by
`/mifos-bridge` and enforced by gates MB-5..MB-9 (reconcile-then-emit), so the contract can never drift from
this model. Fix plan: `server-layer/API_CONSISTENCY_FIX_PLAN.md`.

---

## 2. Feature → backend map (end-to-end feasibility)

Legend: ✅ Fineract native · 🔧 build in companion API (thin) · 🗃️ datatable (config/state) · 📱 client-side.

| Capability | Vehicle |
|---|---|
| Anyone downloads + self-signs-up | 🔧 self-registration bridge over Fineract `POST /self/registration(/user)` |
| Single login/signup, auto-resolve organizer vs member | 📱 app + 🔧 per-user auth returns held groups/roles + 🗃️ role datatable |
| Sign-up-as-organizer (loan-officer powers) | 🔧 bridge grants organizer capability + executes group ops via service credential |
| Create a group | ✅ `POST /groups` + activate, via 🔧 bridge |
| Pick group type (any of 9+) | 🗃️ `group_type_config` on `m_group` |
| Invite members (link/code) | 🗃️ `invitations` datatable + 🔧 bridge → on accept: self-register + `associateClients` |
| Assign roles (organizer/treasurer/secretary) | ✅ Fineract group roles (`assignRole`) + 🗃️ authz datatable |
| Schedule meetings | ✅ `POST /groups/{id}/calendars` via 🔧 calendar tool |
| Attendance + conduct meeting | ✅ collection-sheet `clientsAttendance` via 🔧 tool + 📱 app |
| Collect savings (mandatory/voluntary) | ✅ GSIM/savings + collection sheet via 🔧 bridge |
| Share-based (VSLA) vs fixed (ROSCA/SHG) | ✅ savings product (recurring-deposit for fixed) + 🗃️ `share_value` |
| Corpus tracking | 📱 client compute; truth = ✅ Fineract savings balances |
| Loans: apply / vote-approve / disburse / repay | ✅ loans + GLIM via 🔧 bridge; 📱 voting + 🗃️ votes |
| Fines / penalties | ✅ Fineract charges + 🗃️ ledger |
| VSLA/SILC/ASCA share-out | 📱 compute + 🔧 bridge executes GSIM withdrawal/journal + 🗃️ ledger |
| ROSCA rotation payout | 🗃️ `rosca_rotation` + 📱 compute + 🔧 bridge executes transfer |
| Auction/bid (chit/hui) | 🗃️ `rosca_auction` + 📱 compute |
| Social/welfare fund | ✅ dedicated GSIM savings account (cleaner) or 🗃️ ledger |
| SHG bank-linkage / CBO on-lending | ✅ Fineract loan account (group as borrower) + 🗃️ linkage config |
| Offline-first | 📱 Store5/SQLDelight + 🔧 Fineract batch drain |
| Multi-language / multi-currency | 📱 app + ✅ Fineract currencies |

**Every row resolves. Nothing is a dead-end. Nothing needs Supabase.**

---

## 3. Companion API — deferred build spec (extended `mcp-mifosx`, Go)

The whole "missing API" is a bounded build on the trivial Go tool-def pattern (~10 lines/tool):

| # | Build | Type | Priority |
|---|---|---|---|
| 1 | Generic **datatable-CRUD** tools (register + row create/get/update/delete) | thin, one-time | P0 |
| 2 | **Per-user auth + self-registration** bridge (auth-model change — mcp is single-cred today) | the main lift | P0 |
| 3 | **Self-user → back-office group orchestration** (create/activate group, associateClients, assignRole, assignStaff) | thin (some exist) | P0 |
| 4 | **Calendar + collection-sheet** tools (currently absent) | thin | P1 |
| 5 | **Execute** endpoints for client-computed share-out/rotation money moves (idempotent, re-validated) | thin | P1 |

**Compute (share-out, rotation) stays client-side** in the offline-first app; the companion API only executes the resulting Fineract money moves.

### Active backend instance (SoT: `idea-plan.yaml#fineract_instance`)
The app connects to **`https://mifos-bank-2.mifos.community`** (tenant **`mifos-bank-2`**, dev creds `mifos`/`password`) via the companion server — set `MIFOSX_BASE_URL`/`MIFOSX_TENANT_ID` there. Sandbox (`default`) is the fallback. (User directive 2026-08-01.)

### Deployment decisions (made when the backend is built — not blockers now)
1. A **self-service-enabled Fineract** instance (the community sandbox does not have `/self/*` on; `mifos-bank-2` is the chosen instance — optionally harden signup with the openMF `selfservice-plugin`).
2. A **tenant/office strategy** for global "anyone in the world" onboarding into Fineract's office-scoped model (single global office, or office-per-region).

---

## 4. Group-type registry (`#group-type-registry`)

Every self-funded group is a point in a **2-axis** space, not a bespoke type — so ~1 config object supports them all. Adding a new type is a **`group_type_config` row, not code**.

- **Axis A — pool disposition:** `ROTATING_PAYOUT` (pot rotates to one member each period) vs `ACCUMULATING` (pool grows, lent internally, shared out at cycle end).
- **Axis B — contribution:** `FIXED` vs `SHARE_BASED_VARIABLE`.

### Seeded types (9)

| Type | pool_model | contribution | lending | social fund | formality | distinguishing config |
|---|---|---|---|---|---|---|
| **ROSCA** | ROTATING_PAYOUT | FIXED | no | optional | informal | `payout_order_method` (FIXED_ORDER/LOTTERY/AUCTION/NEED_BASED); pot = contribution × members. Variants: chit/bhishi (IN), tontine (W.Africa), susu (Ghana), tanda (MX), hui (CN), committee (PK) |
| **ASCA** | ACCUMULATING | FIXED/VARIABLE | yes (interest) | optional | informal | end-of-cycle or perpetual; needs bookkeeping |
| **VSLA** | ACCUMULATING | SHARE_BASED_VARIABLE | yes (≤3× savings) | yes | semi-formal (CARE) | `share_value`, min/max shares/meeting, annual cycle, share-out pro-rata to shares |
| **SILC** | ACCUMULATING | SHARE_BASED_VARIABLE | yes | yes | semi-formal (CRS) | VSLA-equivalent; `promoter = CRS` |
| **SHG** | ACCUMULATING | FIXED | yes + **bank linkage** | often | semi-formal→formal (IN) | `external_linkage = BANK_LINKAGE`, `savings_to_loan_ratio` (1:1..1:4), grading |
| **SACCO / Credit Union** | ACCUMULATING | FIXED (+ **share capital**) | yes | optional | **formal, registered** | `share_capital`, elected board, legal status, regulated |
| **CBO / Village Banking** | ACCUMULATING | FIXED | yes (**MFI on-lending**) | optional | semi-formal (FINCA) | `external_linkage = MFI_ONLENDING` — external loan on-lent to members alongside internal savings |
| **Burial / Welfare society** | ACCUMULATING (welfare) | FIXED | no | **fund IS the purpose** | informal | `welfare_only_mode = true`, `benefit_waiting_period_days`; can nest inside a VSLA as its social fund |
| **JLG / Solidarity group** | NONE (borrow) | minimal | **external MFI loan**, mutual guarantee | no | semi-formal (Grameen) | `joint_liability = true`, `purpose = EXTERNAL_BORROWING`; 4–10 members |

> New types (equb [Ethiopia], hagbad [Somalia], stokvel [S.Africa], chama [Kenya], kye [Korea]…) = additional `group_type_config` rows.

### `GroupTypeConfig` schema (stored in the `group_type_config` datatable on `m_group`)

```yaml
GroupTypeConfig:
  slug: string                 # "vsla" | "rosca-tanda" | "shg" | "sacco" | ...
  display_name: string
  # AXIS A — pool disposition
  pool_model: enum             # ROTATING_PAYOUT | ACCUMULATING | NONE
  payout_order_method: enum    # FIXED_ORDER | LOTTERY | AUCTION | NEED_BASED | NA
  shareout_formula: enum       # NONE | PRORATA_SHARES | PRORATA_SAVINGS | EQUAL | INVESTMENT_PROPORTIONAL
  residual_returns: enum       # NONE | INTEREST_ONLY | INVESTMENT_RETURNS
  # AXIS B — contribution
  contribution_model: enum     # FIXED_AMOUNT | SHARE_BASED_VARIABLE | FIXED_NEGOTIATED
  share_value: money|null
  min_shares_per_meeting: int|null
  max_shares_per_meeting: int|null
  contribution_amount: money|null
  # lending
  internal_lending_enabled: bool
  loan_interest_model: enum    # NONE | FLAT | DECLINING | GROUP_SET | AUCTION_IMPLICIT
  loan_multiplier_cap: decimal|null
  loan_max_term_periods: int|null
  external_linkage: enum       # NONE | BANK_LINKAGE | MFI_ONLENDING
  savings_to_loan_ratio: string|null
  joint_liability: bool        # JLG
  share_capital: bool          # SACCO / Credit Union
  # social / welfare fund
  social_fund_enabled: bool
  social_fund_contribution: money|null
  welfare_only_mode: bool      # burial society
  benefit_waiting_period_days: int|null
  # cycle & cadence
  cycle_model: enum            # FIXED_DURATION | N_MEMBERS_ROTATION | PERPETUAL_OPEN
  cycle_length_months: int|null
  meeting_cadence: enum        # DAILY | WEEKLY | BIWEEKLY | MONTHLY
  meeting_schedule_rule: string
  # governance & discipline
  group_size_min: int
  group_size_max: int
  management_committee: bool
  formality: enum              # INFORMAL | SEMI_FORMAL | FORMAL_REGISTERED
  promoter_role: enum          # NONE | NGO_CARE | NGO_CRS | NGO_SHPI | MFI | COLLECTOR | FOREMAN
  penalty_rules: [ {reason: enum(ABSENCE|LATE|MIN_SHARE), amount: money} ]
```

### Fineract mapping (clean reuse vs custom datatable)
- **~60% rides Fineract native:** the **group** (`m_group`), recurring-deposit or variable savings products, loan products, group calendar/meeting, charges/fees. Adding a type = pick product templates + fill a `dt_group_type_config` row.
- **~40% custom datatables + client compute:** rotation order (`rosca_rotation`), auction/bid (`rosca_auction`), VSLA share-out (`vsla_cycle`), welfare fund (`welfare_fund`), and the `group_type_config` switchboard.

---

## 5. Harvested invariants (from the technical DDD doc — vocabulary only, not architecture)

Kept as domain rules: **corpus** = Σ member savings + borrowings + earnings − investments − loans-outstanding · **votes-per-share** & **voting quorum** for internal-loan approval · **cash-in accepted tentatively / cash-out rejected on offline conflict** · **idempotency keys** on every money move (Fineract `externalId`) · **eventual consistency** between the companion API and Fineract.

## 6. Non-goals (v1)

- ❌ Standalone heavy DDD backend service (Spring `vsla-service`) — the companion API is a thin extension of `mcp-mifosx`, not a new DDD app.
- ❌ Region-specific payment webhooks (YAPE/PLIN, Peru) — out of scope for a global v1.
- ❌ Group-level GL/COA accounting in a separate DB — Fineract holds the ledger.
- ❌ Deployment-time group-type **trapdoor** — group type is **runtime per-group config**, never immutable-per-deployment.

---

> Generated by the 2026-07-17 global self-signup evolve · SoT: `idea-plan.yaml` §requirements (FR-013/014/015 revised, FR-021..FR-026 added) + §domain.
