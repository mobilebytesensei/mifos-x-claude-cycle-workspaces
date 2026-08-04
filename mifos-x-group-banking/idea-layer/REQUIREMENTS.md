# Requirements — MifosSave (mifos-x-group-banking)

> 31 functional requirements (FR-026 is a v1 non-goal/constraint) · 8 data entities · 2 third-party services
> **Global self-signup pivot (2026-07-17):** FR-013/014/015 revised, FR-021..FR-026 added, FR-009 demoted. See `ARCHITECTURE.md` for the backend contract + 9-type group registry.
> **Production sign-up + server-migration evolve (2026-08-01):** FR-027..FR-031 added (demo-explore, server demo-seed, idea→server auto-migrate, first-class accept-invitation, user-facing notifications); FR-026 re-tagged must → non-goal/constraint. See `evolve-plans/20260801-production-signup-server-migration.md`.
> Generated from `idea-plan.yaml` §requirements (quality 95%, approved 2026-05-03).
> Source of truth: `idea-layer/idea-plan.yaml` — do not hand-edit acceptance criteria here; edit the plan.

| Field | Value |
|-------|-------|
| Project | mifos-x-group-banking |
| Display name | MifosSave |
| Workspace | mifos-x |
| Type | kmp |
| Backend | Mifos Fineract (REST + MCP) |
| Generated | 2026-05-05 (bridge promote) |

---

## Functional Requirements

### Must (24)

| ID | Description |
|----|-------------|
| FR-001 | Create and configure a new savings group with name, cycle length, meeting schedule, contribution rules, and loan policies |
| FR-002 | Onboard members with name, photo, phone, and role assignment (chairperson, treasurer, secretary, member) |
| FR-003 | Conduct meetings with attendance tracking, savings collection, loan review, and decision recording |
| FR-004 | Collect regular savings contributions with amount validation against group rules |
| FR-005 | Process loan applications with eligibility check based on savings multiplier rule |
| FR-006 | Track loan repayments with schedule, overdue detection, and fine calculation |
| FR-007 | Calculate and execute share-out at end of cycle based on savings ratio + profit distribution |
| FR-008 | Work fully offline with local SQLDelight database and queue-based sync to Fineract |
| FR-013 | Self-signup + login via the companion API (Fineract self-service registration bridged to back-office) + local PIN/biometric for offline re-auth |
| FR-014 | **Single unified login/signup** with post-login capability auto-resolution (organizer vs member, per group) — replaces the prior dual client-type split |
| FR-015 | **Group-scoped roles** resolved per group: organizer (loan-officer powers), treasurer, chairperson, secretary, member |
| FR-021 | Self-signup registers the user as a group **organizer** by default — creates & runs a group end-to-end like a loan officer |
| FR-022 | **Config-driven group_type** (2-axis GroupTypeConfig); 9 seeded types (ROSCA/ASCA/VSLA/SILC/SHG/SACCO/CBO/Burial/JLG); new types = config rows |
| FR-023 | **Pluggable distribution** — pro-rata share-out · ROSCA rotation · auction/bid, selected by group_type |
| FR-024 | Members join a group via **invite link/code** (invitee self-registers, is associated to the group) |
| FR-025 | Group-type state as Fineract **datatables** via the companion API (group_type_config, rosca_rotation, rosca_auction, vsla_cycle, welfare_fund) — satisfied by the `group-type-config` feature |
| FR-017 | Dual savings: mandatory group savings (meeting-collected) and voluntary individual savings (anytime) — CR-003 |
| FR-018 | Real-time fund balance (corpus) for the group; blocks loan disbursement when insufficient — CR-003 |
| FR-019 | Enhanced meeting flow: review previous, separate cash inflows/outflows, fund balance throughout, opening/closing reconciliation — CR-003 |
| FR-027 | **Demo-explore mode** — 'Demo Explore' on login-signup → confirm dialog → guest offline-seeded demo session, explore without registering (works with NO live server) — evolve 2026-08-01 |
| FR-028 | **Server demo-data seed** — runnable migrations seed a demo user's data (clients + group activation, savings, meeting records, corpus, one live invite code) — externally gated on companion-api-backend — evolve 2026-08-01 |
| FR-029 | **Idea→server auto-migrate / server-ready** — re-run + extend `/mifos-bridge` to emit runnable datatable migrations so adding a feature migrates its missing API/table — evolve 2026-08-01 |
| FR-030 | **First-class accept-invitation auth path** — login / accept-invitation / sign-up as first-class pre-auth entries; cold-launched invitee resumes join via pendingInviteCode — evolve 2026-08-01 |
| FR-031 | **User-facing notifications & activity feed** — push + in-app notifications (loan approvals, reminders, meeting invites, share-out previews) with read/unread + per-type opt-in — satisfied by the `notifications` feature — evolve 2026-08-01 |

### Should (5)

| ID | Description |
|----|-------------|
| FR-009 | *(demoted → Could)* OPTIONAL supervisory tier: field officer / NGO program manager read-only cross-group monitoring — no longer the primary identity |
| FR-010 | Support multiple languages (English, Swahili, French, Hindi) with runtime switching |
| FR-012 | Fine collection for late attendance, missed meetings, or late loan repayment |
| FR-016 | End user can submit loan request from personal dashboard; appears as pending in next admin meeting |
| FR-020 | Penalty for member not meeting minimum group savings contribution at a meeting — CR-003 |

### Could (1)

| ID | Description |
|----|-------------|
| FR-011 | Social fund collection and emergency disbursement tracking |

### Constraints / Non-goals (1)

| ID | Description |
|----|-------------|
| FR-026 | **Non-goals (v1 constraint, re-tagged 2026-08-01 must → non-goal):** no standalone DDD service, no YAPE/PLIN, no group-level GL, no deployment-time group-type trapdoor. Records what v1 will NOT do — has no satisfying feature by design and must not read as an orphan MUST FR. |

> **Acceptance criteria** for each FR live in `idea-plan.yaml` §requirements.functional_requirements[].acceptance_criteria — read those before implementing the feature.

---

## Data Entities

| Entity | Key Fields | Relationships | Fineract Mapping |
|--------|-----------|--------------|------------------|
| Group | id, name, cycle_number, cycle_length_months, meeting_frequency, contribution_min/max, loan_multiplier, interest_rate, currency, fineract_center_id, status | has_many Members · has_many Meetings · has_one SavingsPool | m_center (+ dt_group_config datatable) |
| Member | id, name, phone, photo_uri, role, joined_date, fineract_client_id, status | belongs_to Group · has_many SavingsTransactions · has_many Loans | m_client (+ dt_member_role datatable) |
| Meeting | id, meeting_number, scheduled_date, actual_date, status, attendance_count, total_collected, notes | belongs_to Group · has_many AttendanceRecords · has_many SavingsTransactions | dt_meeting datatable on m_center |
| SavingsTransaction | id, member_id, meeting_id, amount, type (contribution/withdrawal/fine/social_fund), fineract_transaction_id, sync_status | belongs_to Member · belongs_to Meeting | m_savings_account_transaction |
| Loan | id, member_id, amount, interest_rate, duration_weeks, status (requested/approved/disbursed/repaying/closed/defaulted), approved_by, disbursed_date, fineract_loan_id, sync_status | belongs_to Member · has_many LoanRepayments | m_loan |
| LoanRepayment | id, loan_id, amount, meeting_id, paid_date, fineract_transaction_id, sync_status | belongs_to Loan | m_loan_transaction |
| AttendanceRecord | id, meeting_id, member_id, present, late, fine_amount | belongs_to Meeting · belongs_to Member | dt_attendance datatable on m_center |
| SyncQueue | id, entity_type, entity_id, operation (create/update/delete), payload_json, created_at, retry_count, last_error, status (pending/in_progress/synced/failed) | polymorphic to any entity | local-only (offline-first) |

---

## Third-Party Services

| Service | Purpose | Integration |
|---------|---------|-------------|
| Mifos Fineract | Core banking backend — groups (Centers), members (Clients), savings accounts, loan products, transactions | REST API + MCP server |
| SQLDelight | Local offline database for all entities | SDK (compile-time SQL → Kotlin) |

---

## Infrastructure Requirements (external gate)

> These are not functional requirements for the KMP app — they are **backend infrastructure prerequisites**
> that must be satisfied before `/device-test` can produce a non-`pending-device-verify` result and before
> `matrix-green` can be reached. See `server-layer/COMPANION_API_BUILD_DEPLOY.md` for the full spec.

| ID | Description |
|----|-------------|
| IR-001 | **Companion API — auth-model change (P0)**: mcp-mifosx Go server extended with per-call user credential intake; companion tools mint Fineract sessions and execute back-office group ops via service credential while enforcing organizer-vs-member authz at the companion tier |
| IR-002 | **Companion API — TIER-1 tools (9)**: COMP-AUTH-001..003 (self-register, login, me) + COMP-GRP-001..005 (create, activate, associate-clients, assign-role, assign-staff) + COMP-CAL-001..003 (calendar, collection-sheet get/save) — registered in `go/tools/companion_*.go` |
| IR-003 | **Companion API — TIER-2 datatable-CRUD tools (7)**: COMP-DT-001..005 (register, create-row, read-row, update-row, delete-row) + COMP-DIST-001/002 (share-out execute, rotation execute) — registered in `go/tools/datatables.go` |
| IR-004 | **Self-service-enabled Fineract instance**: a Fineract deployment with the self-service module enabled (the community sandbox does NOT qualify); tenant/office strategy configured for global "anyone in the world" onboarding |
| IR-005 | **6 companion datatables provisioned** against deployed Fineract (once, via COMP-DT-001): `dt_group_type_config`, `dt_companion_invitations`, `dt_rosca_rotation`, `dt_rosca_auction`, `dt_vsla_cycle`, `dt_welfare_fund` (all attached to `m_group`) |
| IR-006 | **App wired to companion backend**: MifosSave companion base URL points at deployed mcp-mifosx; end-to-end flow (signup → create group → invite → savings/loan → share-out) verified via Maestro on device |

## Cross-References

- **Features**: see `idea-layer/FEATURES.md` (21 features → these FRs)
- **API Contract**: see `server-layer/API_CONTRACT.yaml` (Fineract endpoints + 36 MCP tools generated by /mifos-bridge; companion section: 20 tools + 6 datatables)
- **Companion API Build Spec**: see `server-layer/COMPANION_API_BUILD_DEPLOY.md`
- **Bridge Audit**: see `server-layer/BRIDGE_AUDIT_LOG.yaml` (21-item Tier-1/Tier-2 resolution record)
- **Data Tables (custom)**: 15 datatable schemas in `server-layer/API_CONTRACT.yaml` under `custom_tables[]`
- **Plan**: `idea-layer/idea-plan.yaml` §requirements (line 541); §technical_decisions.companion_api; §release_plan.milestones[companion-api-backend]
