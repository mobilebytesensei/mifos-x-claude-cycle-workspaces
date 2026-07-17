# API — CommonPurse (mifos-x-group-banking)

> Mifos Fineract REST + Companion API (Go, deferred build) + 116 total MCP tools + 21 custom datatables.
> Single source of truth: `server-layer/API_CONTRACT.yaml` (bridge runs `bridge-260504-001` + `bridge-260717-002`).
> Bridge audit: `server-layer/BRIDGE_AUDIT_LOG.yaml` (41 items; 21 approved-deployed + 20 design-approved-pending-deployment).

| Field | Value |
|-------|-------|
| Backend | Mifos Fineract (sandbox.mifos.community) + Companion API (deferred Go build) |
| Base URLs | `/fineract-provider/api/v1` (Fineract) · `/companion/*` (Companion API) |
| MCP Server | `mifos` |
| Consumer | mifos-x-group-banking (KMP) |
| Bridge run 1 | `bridge-260504-001` (2026-05-04T14:08:00Z) — 15 features, 36 tools |
| Bridge run 2 | `bridge-260717-002` (2026-07-17) — 8 new screens, 20 companion tools |
| Coverage | All endpoints covered · 23/23 screens · 0 gaps |

---

## Coverage Summary

| Tier | Count | What |
|------|------:|------|
| Native (existing MCP) | 54 | Fineract endpoints with ready MCP tools — no work |
| Tier 1 — generated tools | 6 | Fineract endpoint wrappers generated (bridge-260504-001) |
| Tier 2 — datatables + tools | 15 | Custom datatables + 30 wrapper tools (bridge-260504-001) |
| Companion Tier 1 | 12 | `/companion/*` façades over Fineract orchestration (bridge-260717-002) |
| Companion Tier 2 | 8 | Companion datatable-CRUD tools: invitations + group_type_config + corpus/rotation aggregators (bridge-260717-002) |
| **Total endpoints** | **96** | — |
| Features / screens covered | 23/23 | 100% (no uncovered features) |
| Companion datatables | 6 | dt_group_type_config · dt_companion_invitations · dt_rosca_rotation · dt_rosca_auction · dt_vsla_cycle · dt_welfare_fund |

---

## Endpoint Categories

### Clients & Identification (Member onboarding — FR-002, FR-013, FR-014)
- `GET /search`, `GET /clients/{id}`, `GET /clients/{id}/accounts`
- `POST /clients`, `POST /clients/{id}?command=activate`, `POST /clients/{id}?command=close`
- `PUT /clients/{id}` (mobile/email update)
- Identifiers: `GET/POST /clients/{id}/identifiers`
- Documents: `GET /clients/{id}/documents`
- Addresses: `GET /client/{id}/addresses`
- Charges/Fees: `GET/POST /clients/{id}/charges`
- Transactions: `GET /clients/{id}/transactions`
- Self-service auth: `mcp__mifos__self_authenticate` (FR-014 end-user)

### Groups & Centers (Group management — FR-001, FR-019)
- Centers (group container): `GET /centers`, `GET /centers/{id}`, `POST /centers`
- Groups (lending units within centers): `GET /groups`, `GET /groups/{id}`, `POST /groups`, `POST /groups/{id}?command=activate`
- Group config: `mcp__mifos__get_group_config`, `mcp__mifos__upsert_group_config`
- Group members: `mcp__mifos__add_member_to_group`, `mcp__mifos__assign_member_role`
- Meetings (Tier 2 datatable): `mcp__mifos__list_meetings`, `mcp__mifos__record_meeting`
- Attendance: `mcp__mifos__list_attendance`, `mcp__mifos__record_attendance`

### Savings (Group + voluntary — FR-004, FR-017)
- Products: `GET /savingsproducts`, `GET /savingsproducts/{id}` → `mcp__mifos__get_savings_product_details`
- Accounts: `GET/POST /savingsaccounts`, `POST /savingsaccounts/{id}?command=approve|activate`
- Transactions: `mcp__mifos__deposit`, `mcp__mifos__withdraw`, `mcp__mifos__get_savings_txns`
- Interest: `mcp__mifos__calc_post_interest`
- Fees: `mcp__mifos__apply_savings_fee`

### Loans (Application → disbursal → repayment — FR-005, FR-006)
- Products: `mcp__mifos__list_available_loan_products`, `mcp__mifos__get_loan_product_details`
- Application: `mcp__mifos__submit_loan_request`, `mcp__mifos__create_group_loan_app`, `mcp__mifos__get_loan_app_template`
- Approval flow: `mcp__mifos__approve_disburse_loan`, `mcp__mifos__reject_loan`, `mcp__mifos__undo_approval`, `mcp__mifos__undo_disbursal`
- Repayment: `mcp__mifos__make_repayment`, `mcp__mifos__get_repayment_sched`, `mcp__mifos__waive_loan_interest`
- Voting (Tier 2): `mcp__mifos__record_loan_vote`, `mcp__mifos__get_loan_vote`
- Guarantors: `mcp__mifos__list_loan_guarantors`, `mcp__mifos__add_loan_guarantor`
- Overdue: `mcp__mifos__get_overdue_loans_for_client`
- History: `mcp__mifos__get_loan_hist`
- Policy: `mcp__mifos__get_loan_policy`, `mcp__mifos__set_loan_policy`
- Member ceilings: `mcp__mifos__get_member_ceiling`, `mcp__mifos__set_member_ceiling`
- Reschedule: `mcp__mifos__reschedule_loan_app`

### Share-Out (FR-007 — end-of-cycle distribution)
- `mcp__mifos__list_share_outs`, `mcp__mifos__record_share_out`
- Computed via Tier 2 wrapper from m_savings_account aggregations

### Group Corpus / Fund Balance (FR-018 — real-time corpus)
- `mcp__mifos__get_group_corpus`, `mcp__mifos__update_group_corpus`
- Backed by dt_group_corpus datatable on m_center

### Social Fund (FR-011)
- `mcp__mifos__get_social_fund`, `mcp__mifos__update_social_fund`

### Charges, Penalties, Fines (FR-012, FR-020)
- Catalog: `GET/POST /charges`, `mcp__mifos__list_all_charges`, `mcp__mifos__create_new_charge`, `mcp__mifos__update_existing_charge`
- Apply: `mcp__mifos__apply_loan_fee`, `mcp__mifos__apply_savings_fee`, `mcp__mifos__apply_client_fee`
- List: `mcp__mifos__list_client_charges`

### Reports & Analytics
- Definitions: `mcp__mifos__list_all_reports`, `mcp__mifos__create_report_definition`, `mcp__mifos__update_report_definition`, `mcp__mifos__get_report_definition`
- Run: `mcp__mifos__run_fineract_report`

### Journal Entries / Accounting
- `mcp__mifos__list_journal_entries`, `mcp__mifos__record_journal_entry`

### Notifications
- `mcp__mifos__list_notifications`, `mcp__mifos__push_notification`

### System / Org
- Offices: `mcp__mifos__list_all_offices`, `mcp__mifos__get_office`
- Staff: `mcp__mifos__list_all_staff`, `mcp__mifos__get_staff`
- Codes: `mcp__mifos__list_system_codes`, `mcp__mifos__get_code_values`

### Auth
- `mcp__mifos__authenticate` (admin), `mcp__mifos__self_authenticate` (end user)
- Sync state: `mcp__mifos__get_sync_state`, `mcp__mifos__update_sync_state` (FR-008 offline-first)
- Batch: `mcp__mifos__send_batch`

### Datatables (CRUD on custom schemas — Tier 2 base)
- `mcp__mifos__create_datatable`, `mcp__mifos__list_all_datatables`
- Per entry: `mcp__mifos__create_datatable_entry`, `mcp__mifos__get_datatable_entries`, `mcp__mifos__update_datatable_entry`, `mcp__mifos__delete_datatable_entry`

### Invitations (FR-016 end-user invites)
- Pre-pivot (m_client): `mcp__mifos__list_invitations`, `mcp__mifos__create_invitation`
- Companion (m_group, bridge-260717-002): `mcp__mifos__companion_create_invitation`, `mcp__mifos__companion_list_pending_invites`, `mcp__mifos__companion_validate_invite_token`, `mcp__mifos__companion_mark_invitation_accepted`, `mcp__mifos__companion_revoke_invite`

---

---

## Companion API — `/companion/*` (bridge-260717-002, design-approved-pending-deployment)

The **global self-signup pivot** introduced a thin Go microservice (extended mcp-mifosx) that sits
between the KMP app and Fineract. All `/companion/*` paths go through this layer — never raw Fineract.

**Architecture**: KMP app → Companion API → Apache Fineract Core.
- Companion owns: identity bridge, group orchestration, datatable-CRUD, distribution execution.
- Fineract owns: all money (savings, loans, transactions).
- App owns: offline UX + distribution compute (preview). Compute stays client-side; companion only
  executes Fineract money moves.

### COMP-AUTH — Authentication Bridge

| Tool | Method | Path | Description |
|------|--------|------|-------------|
| `mcp__mifos__companion_self_register` | POST | `/companion/auth/self-register` | Self-register — creates Fineract client atomically (COMP-AUTH-001) |
| `mcp__mifos__companion_login` | POST | `/companion/auth/login` | Login — returns sessionToken + group memberships (COMP-AUTH-002) |
| `mcp__mifos__companion_me` | GET | `/companion/auth/me` | Fetch authenticated profile post-biometric unlock (COMP-AUTH-003) |

### COMP-GRP — Group Orchestration

| Tool | Method | Path | Description |
|------|--------|------|-------------|
| `mcp__mifos__companion_create_group` | POST | `/companion/groups` | Orchestrate create+activate+associate+role+provision in one call |
| `mcp__mifos__companion_get_group` | GET | `/companion/groups/{groupId}` | Group details + merged group_type_config |
| `mcp__mifos__companion_list_my_groups` | GET | `/companion/groups/mine` | Paginated list with groupType + viewerRole |
| `mcp__mifos__companion_get_viewer_role` | GET | `/companion/groups/{groupId}/my-role` | Authenticated user's role in a group |
| `mcp__mifos__companion_get_group_corpus` | GET | `/companion/groups/{groupId}/corpus` | Corpus/rotation state, resolves groupId→centerId |
| `mcp__mifos__companion_get_group_accounts` | GET | `/companion/groups/{groupId}/accounts` | Savings + loan summary |
| `mcp__mifos__companion_associate_clients` | POST | `/companion/groups/{groupId}/associate-clients` | Associate invitee with role (post token validation) |

### COMP-DT — Datatable CRUD (Invitations + GroupTypeConfig)

| Tool | Method | Path | Description |
|------|--------|------|-------------|
| `mcp__mifos__companion_get_group_type_configs` | GET | `/companion/datatables/group_type_config/0` | Global seed catalogue — 9+ GroupTypeConfig archetype rows |
| `mcp__mifos__companion_create_invitation` | POST | `/companion/datatables/invitations/{groupId}` | Create invite — companion generates 6-char token (COMP-DT-002) |
| `mcp__mifos__companion_list_pending_invites` | GET | `/companion/datatables/invitations/{groupId}` | Pending invites for organizer view (COMP-DT-003) |
| `mcp__mifos__companion_validate_invite_token` | GET | `/companion/datatables/invitations/{token}` | Token validation for join-with-code (COMP-DT-001) |
| `mcp__mifos__companion_mark_invitation_accepted` | PUT | `/companion/datatables/invitations/{token}/{rowId}` | Mark invite consumed (COMP-DT-004) |
| `mcp__mifos__companion_revoke_invite` | DELETE | `/companion/datatables/invitations/{groupId}/{rowId}` | Organizer revokes pending invite (COMP-DT-005) |

### COMP-DIST — Distribution Execution

| Tool | Method | Path | Description |
|------|--------|------|-------------|
| `mcp__mifos__companion_get_shareout_preview` | GET | `/companion/groups/{groupId}/shareout/preview` | Strategy-aware preview — memberPayouts[] or rotationPosition (COMP-DIST-001) |
| `mcp__mifos__companion_execute_shareout` | POST | `/companion/groups/{groupId}/shareout/execute` | ACCUMULATING share-out — records dt_share_out + per-member withdrawals (COMP-DIST-001) |
| `mcp__mifos__companion_execute_rotation_payout` | POST | `/companion/groups/{groupId}/rotation/execute` | ROTATING_PAYOUT — advance rotation + single-recipient withdrawal (COMP-DIST-002) |

### Companion Aggregated Dashboard Endpoints

| Tool | Method | Path | Screen |
|------|--------|------|--------|
| `mcp__mifos__companion_get_member_dashboard` | GET | `/companion/member/dashboard` | personal-dashboard |
| `mcp__mifos__companion_get_organizer_dashboard` | GET | `/companion/organizer/dashboard` | admin-dashboard |
| `mcp__mifos__companion_get_group_savings_summary` | GET | `/companion/groups/{groupId}/savings` | savings-dashboard (Group tab) |
| `mcp__mifos__companion_get_individual_savings_summary` | GET | `/companion/groups/{groupId}/savings/individual` | savings-dashboard (Individual tab) |
| `mcp__mifos__companion_get_member_savings_detail` | GET | `/companion/groups/{groupId}/members/{memberId}/savings` | member-savings-detail |

### Companion Datatable Read Endpoints

| Tool | Datatable | Schema anchor |
|------|-----------|---------------|
| `mcp__mifos__companion_dt_rosca_rotation` | dt_rosca_rotation on m_group | rotation queue, position, paid_at, FIXED_ORDER/LOTTERY/AUCTION |
| `mcp__mifos__companion_dt_rosca_auction` | dt_rosca_auction on m_group | chit/hui bid records per meeting |
| `mcp__mifos__companion_dt_vsla_cycle` | dt_vsla_cycle on m_group | share_value + VSLA/SILC/ASCA cycle state |
| `mcp__mifos__companion_dt_welfare_fund` | dt_welfare_fund on m_group | social/welfare fund balance (social_fund_enabled=true groups) |

> All companion tools are **design-approved, pending deployment** (companion Go service not yet on sandbox).
> Gates 3+4 of RULE-MIFOS-BRIDGE-001 fire when the service reaches the sandbox milestone.

---

## Custom Data Tables

21 total custom datatables (15 from bridge-260504-001 + 6 new from bridge-260717-002). Full schemas in `API_CONTRACT.yaml`.

### Original Datatables (bridge-260504-001 — m_center + m_client + m_loan)

- `dt_group_config` on m_center — group rules: cycle length, contribution min/max, loan multiplier, interest rate, meeting frequency
- `dt_member_role` on m_client — chairperson / treasurer / secretary / member / field_officer / program_manager
- `dt_meeting_record` on m_center — meeting_number, scheduled_date, status, attendance_count
- `dt_meeting_attendance` on m_client — per-meeting member presence + late + auto-fine
- `dt_group_corpus` on m_center — running fund balance for FR-018
- `dt_loan_vote` on m_loan — chairperson + member majority votes
- `dt_group_loan_policy` on m_center — group-level policy overrides
- `dt_member_ceiling_override` on m_client — per-member loan cap
- `dt_share_out` on m_center — end-of-cycle distribution records
- `dt_social_fund` on m_center — emergency fund balance + disbursements
- `dt_member_invitation` on m_client — pending end-user invites with token
- `dt_loan_request` on m_client — loan application queue
- `dt_loan_guarantor` on m_loan — guarantor list per loan
- `dt_notification` on m_client — push notification records
- `dt_sync_metadata` on m_center — offline sync state tracker

### Companion Datatables (bridge-260717-002 — all on m_group)

| Datatable | Anchor | Purpose |
|-----------|--------|---------|
| `dt_group_type_config` | m_group | Global archetype registry — 9 seeded rows: ROSCA/ASCA/VSLA/SILC/SHG/SACCO/CBO/BURIAL/JLG. 27-column schema across 9 axis fields. entityId=0 = catalogue mode. |
| `dt_companion_invitations` | m_group | Group-scoped invite tokens. 6-char alphanumeric token key. Dual access: token-lookup (join-with-code) + list-pending (organizer). accepted_at=null → pending. |
| `dt_rosca_rotation` | m_group | Rotation queue: position, recipient_client_id, paid_at, payout_order_method (FIXED_ORDER / LOTTERY / AUCTION). Written by companion_execute_rotation_payout. |
| `dt_rosca_auction` | m_group | Chit/hui bid records: bidder_client_id, bid_amount, bid_status (PENDING / WON / LOST / WITHDRAWN) per meeting. |
| `dt_vsla_cycle` | m_group | VSLA/SILC/ASCA cycle state: share_value (KES), total_shares_outstanding, cycle status (ACTIVE / CLOSED / SHARED_OUT). |
| `dt_welfare_fund` | m_group | Social/welfare fund: current_balance, total_contributions, total_disbursements. Active when group_type_config.social_fund_enabled=true. |

---

## Sync Strategy (FR-008 offline-first)

- All write operations enqueue to `SyncQueue` (local SQLDelight)
- Background sync via `mcp__mifos__send_batch` for bulk replay
- Conflict resolution: server-wins for create/update, except member-attributable transactions (timestamp-precedence)
- Sync state per entity tracked via `dt_sync_state` (Tier 2)

---

## Cross-References

- Full contract: `server-layer/API_CONTRACT.yaml` (bridge-260504-001 + bridge-260717-002)
- Bridge audit: `server-layer/BRIDGE_AUDIT_LOG.yaml` (41 items total)
- Architecture / companion API design: `idea-layer/ARCHITECTURE.md` §companion_api + §companion_datatables
- Plan: `idea-layer/idea-plan.yaml` §api_surface
- MCP capabilities (shared): `../../mcp-mifosx/server-layer/MCP_CAPABILITIES.yaml`
- Companion API implementation spec: deferred Go build — pending milestone
