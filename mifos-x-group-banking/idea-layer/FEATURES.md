# Features - CommonPurse (mifos-x-group-banking)

> 21 features | 12 must | 4 should | 1 could | 1 external-gate (companion-api-backend)
> Global self-signup pivot (2026-07-17): unified-auth, self-signup-organizer, group-type-config, pluggable-distribution, member-invitations added; companion-api-backend added as external infrastructure gate.

## Feature Matrix

> 21 features | 12 must | 4 should | 1 could | 1 external-gate
> **One unified identity — self-signup**: anyone downloads → self-registers → creates or joins a group. Post-login capabilities auto-resolved per group.
> Source: idea-plan.yaml + Community Research (CR-003: professionally curated) + global self-signup pivot 2026-07-17

| # | Feature | Priority | Client | Version | Screens | Flow | API | Data Tables | Reqs |
|---|---------|----------|--------|---------|---------|------|-----|-------------|------|
| 0 | **companion-api-backend** | **external-gate** | server-infra | pre-1.0.0 | — | — | COMP-AUTH-001..003, COMP-GRP-001..005, COMP-CAL-001..003, COMP-DT-001..005, COMP-DIST-001/002 | dt_group_type_config, dt_companion_invitations, dt_rosca_rotation, dt_rosca_auction, dt_vsla_cycle, dt_welfare_fund | IR-001..006 |
| 1 | authentication | must | both | 1.0.0 | client-type-selector, login, admin-dashboard | admin-auth, end-user-auth | 2 | dt_member_role | FR-013-15 |
| 2 | end-user-dashboard | must | end_user | 1.0.0 | personal-dashboard, personal-savings, personal-loans, loan-request | end-user-loan-request | 4 | dt_loan_request | FR-014, FR-016 |
| 3 | group-management | must | admin | 1.0.0 | group-list, group-dashboard, group-create | group-creation | 4 | dt_group_config | FR-001, FR-020 |
| 4 | member-onboarding | must | admin | 1.0.0 | member-list, member-profile, member-add, member-savings-detail | - | 3 | dt_member_role | FR-002 |
| 5 | meeting-lifecycle | must | admin | 1.0.0 | meeting-calendar, meeting-conduct, meeting-summary, previous-meeting-review | meeting | 2 | dt_meeting_record, dt_meeting_attendance | FR-003, FR-019 |
| 6 | savings-collection | must | admin | 1.0.0 | savings-dashboard, meeting-conduct | meeting | 2 | - | FR-004 |
| 7 | group-linked-savings | must | admin | 1.0.0 | savings-dashboard, meeting-conduct, group-dashboard | - | 2 | - | FR-017, FR-020 |
| 8 | corpus-tracking | must | admin | 1.0.0 | group-dashboard, meeting-conduct | corpus-outflow-blocked | 1 | dt_group_corpus | FR-018 |
| 9 | loan-management | must | admin | 1.0.0 | loan-list, loan-apply, loan-detail, meeting-conduct | loan-lifecycle | 3 | dt_loan_vote | FR-005-06 |
| 10 | share-out | must | admin | 1.0.0 | share-out-preview, share-out-execute | share-out | 2 | dt_share_out | FR-007 |
| 11 | offline-sync | must | both | 1.0.0 | sync-status | offline-sync | 1 | dt_sync_metadata | FR-008 |
| 12 | fines-tracking | should | admin | 1.0.0 | meeting-conduct | - | 3 | dt_meeting_attendance | FR-012, FR-020 |
| 13 | multi-language | should | both | 1.0.0 | settings | - | 0 | - | FR-010 |
| 14 | field-officer-view | should | admin | 1.1.0 | field-officer-dashboard | - | 3 | dt_sync_metadata | FR-009 |
| 15 | social-fund | could | admin | 1.1.0 | - | - | 1 | dt_social_fund | FR-011 |

## companion-api-backend (External Infrastructure Gate)

> **Not an app feature** — this is the backend build + deploy prerequisite that unlocks `/device-test`.
> Until this gate is satisfied, app features **compile + build-green** but device-test returns `pending-device-verify`.

| Build item | Contracts | Notes |
|---|---|---|
| P0 auth-model change | — | Per-call user credential intake; service-credential group orchestration; organizer-vs-member authz at companion tier |
| TIER-1: auth tools | COMP-AUTH-001 (self-register), COMP-AUTH-002 (login), COMP-AUTH-003 (me) | `go/tools/companion_auth.go` |
| TIER-1: group orchestration tools | COMP-GRP-001 (create/read), COMP-GRP-002 (activate), COMP-GRP-003 (associate-clients), COMP-GRP-004 (assign-role), COMP-GRP-005 (assign-staff) | `go/tools/companion_groups.go` |
| TIER-1: calendar + collection-sheet | COMP-CAL-001 (calendar), COMP-CAL-002 (get collection-sheet), COMP-CAL-003 (save collection-sheet) | `go/tools/companion_calendar.go` |
| TIER-2: datatable CRUD | COMP-DT-001 (register), COMP-DT-002 (create row), COMP-DT-003 (read rows), COMP-DT-004 (update row), COMP-DT-005 (delete row) | `go/tools/datatables.go` |
| TIER-2: distribution execute | COMP-DIST-001 (share-out execute), COMP-DIST-002 (rotation execute) | Client computes payout; server re-validates + executes (CK4) |
| Fineract with self-service ENABLED | — | Community sandbox does NOT qualify; deploy a fresh instance |
| 6 datatables provisioned | dt_group_type_config, dt_companion_invitations, dt_rosca_rotation, dt_rosca_auction, dt_vsla_cycle, dt_welfare_fund | Run once via COMP-DT-001 after deploy |

**Full spec**: `server-layer/COMPANION_API_BUILD_DEPLOY.md` | **Contract**: `server-layer/API_CONTRACT.yaml` (companion section)

## Milestone Roadmap

### companion-api-backend (External gate — must land before v1.0.0 device-verify)
See section above. Spec: `server-layer/COMPANION_API_BUILD_DEPLOY.md`

### v1.0.0 - Core Group Banking (13 features)
authentication, group-management, member-onboarding, meeting-lifecycle, savings-collection, group-linked-savings, corpus-tracking, loan-management, share-out, offline-sync, fines-tracking, multi-language, end-user-dashboard

### v1.1.0 - Supervision & Social
field-officer-view, social-fund

### v2.0.0 - Scale & Integrate
mobile-money-integration, web-admin-dashboard, sms-notifications, inter-group-lending, credit-scoring

## Epic Breakdown

| Epic | Features | Milestone |
|------|----------|-----------|
| Core Group Infrastructure | authentication, group-management, member-onboarding, end-user-dashboard | v1.0.0 |
| Meeting & Savings Engine | meeting-lifecycle, savings-collection, group-linked-savings, corpus-tracking, fines-tracking | v1.0.0 |
| Lending & Distribution | loan-management, share-out | v1.0.0 |
| Platform Foundation | offline-sync, multi-language | v1.0.0 |
| Supervision & Social | field-officer-view, social-fund | v1.1.0 |

## Screen Inventory (30 screens)

| Screen | Archetype | Features |
|--------|-----------|----------|
| client-type-selector | form | authentication |
| login | form | authentication |
| admin-dashboard | dashboard | authentication |
| personal-dashboard | dashboard | end-user-dashboard |
| personal-savings | detail_screen | end-user-dashboard |
| personal-loans | index_list | end-user-dashboard |
| loan-request | form | end-user-dashboard |
| group-list | index_list | group-management |
| group-dashboard | dashboard | group-management, corpus-tracking, group-linked-savings |
| group-create | form | group-management |
| member-list | index_list | member-onboarding |
| member-profile | detail_screen | member-onboarding |
| member-add | form | member-onboarding |
| member-savings-detail | detail_screen | member-onboarding |
| meeting-calendar | index_list | meeting-lifecycle |
| meeting-conduct | form | meeting-lifecycle, savings-collection, loan-management, corpus-tracking, group-linked-savings, fines-tracking |
| meeting-summary | detail_screen | meeting-lifecycle |
| previous-meeting-review | detail_screen | meeting-lifecycle |
| savings-dashboard | dashboard | savings-collection, group-linked-savings |
| loan-list | index_list | loan-management |
| loan-apply | form | loan-management |
| loan-detail | detail_screen | loan-management |
| loan-repayment-dialog | dialog | loan-management |
| loan-mark-defaulted-dialog | dialog | loan-management |
| share-out-preview | detail_screen | share-out |
| share-out-execute | form | share-out |
| sync-status | dashboard | offline-sync |
| field-officer-dashboard | dashboard | field-officer-view |
| settings | settings | multi-language |
| settings-logout-dialog | dialog | authentication |

## Data Entities (8)

| Entity | Key Fields | Fineract Mapping |
|--------|------------|------------------|
| Group | name, cycle, rules, currency, corpus_balance | Center |
| Member | name, phone, photo, role | Client |
| Meeting | number, date, attendance, collected, opening_balance, closing_balance | dt_meeting_record |
| SavingsTransaction | member, amount, type (group_linked / individual) | Savings Transaction |
| Loan | member, amount, rate, status | Loan Product |
| LoanRepayment | loan, amount, date | Loan Transaction |
| AttendanceRecord | meeting, member, present, late, fine | dt_meeting_attendance |
| SyncQueue | entity, operation, payload, status | Batch API |

## API Coverage

- **Fineract endpoints**: 55+ (centers, groups, clients, savings, loans, charges, reports, batch)
- **MCP tools**: 65 (full programmatic access via Mifos MCP Server)
- **Custom Data Tables**: 10 designed (9 original + 1 from community research)
- **Feature coverage**: 100% (15/15 features fully resolvable)
- **Zero gaps**: Data Tables API = custom endpoint designer

### Data Tables — Custom API Design Pattern (10 tables)

| Data Table | Attached To | Feature | Client | Purpose |
|-----------|-------------|---------|--------|---------|
| dt_group_config | m_center | group-management | admin | Cycle rules, contribution limits, loan multiplier, fine amounts, cycle dates |
| dt_meeting_record | m_center | meeting-lifecycle | admin | Per-meeting summary: attendance, totals, decisions |
| dt_meeting_attendance | m_client | meeting-lifecycle | admin | Per-member attendance: present/late/fined |
| dt_member_role | m_client | authentication | both | Role + client_type: admin(treasurer/chair/FO) or end_user(member) |
| dt_share_out | m_center | share-out | admin | Cycle share-out record: pool, distribution, status |
| dt_social_fund | m_center | social-fund | admin | Emergency fund balance and disbursement tracking |
| dt_loan_vote | m_loan | loan-management | admin | Loan approval voting: for/against/chairperson approval |
| dt_sync_metadata | m_center | offline-sync | both | Sync state: last sync, pending ops, conflicts |
| dt_loan_request | m_client | end-user-dashboard | end_user | End-user loan requests submitted for admin review at meetings |
| dt_group_corpus | m_center | corpus-tracking | admin | Running fund balance: current, inflows, outflows, meeting open/close |

---

> Generated from idea-plan.yaml | Last updated: 2026-05-03 (post professional curation)
