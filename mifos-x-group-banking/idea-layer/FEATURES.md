# Features - MifosSave (mifos-x-group-banking)

> 24 app features | 18 must | 5 should | 1 could | + 1 external-gate (companion-api-backend)
> **One unified identity — self-signup**: anyone downloads → self-registers → creates or joins a group. Post-login capabilities auto-resolved **per group** (organizer vs member), never chosen up front.
> Global self-signup pivot (2026-07-17): `unified-auth`, `self-signup-organizer`, `group-type-config`, `pluggable-distribution`, `member-invitations` added; the old dual `authentication` feature + `client-type-selector`/`login`/`admin-dashboard` screens removed; `companion-api-backend` added as the external infrastructure gate.
> Production launch evolve (2026-08-01): `demo-explore` feature added (FR-027); requirement cross-maps fixed — group-type-config now satisfies FR-025, notifications now satisfies FR-031 (was FR-019), meeting-lifecycle references FR-019, unified-auth references FR-030 (first-class accept-invitation), offline-sync references FR-029 (server-ready). See `evolve-plans/20260801-production-signup-server-migration.md`.
> Source of truth: `idea-plan.yaml` (§features, §screens, §release_plan) + Community Research (CR-003) + VSLA best-practices + global self-signup pivot 2026-07-17.

## Feature Matrix

> **Surface** = which capability surface the feature belongs to. `all` = shared for every logged-in user; `organizer` = organizer/treasurer/chairperson (write) role surface within a group; `member` = self-service member surface. Roles are resolved per group after a single unified login — there is no app-wide admin vs end-user split.

| # | Feature | Priority | Surface | Version | Screens | Flow | Data Tables | Reqs |
|---|---------|----------|---------|---------|---------|------|-------------|------|
| 0 | **companion-api-backend** | **external-gate** | server-infra | pre-1.0.0 | — | — | group_type_config, invitations, rosca_rotation, rosca_auction, vsla_cycle, welfare_fund | FR-013, FR-021–025 |
| 1 | unified-auth | must | all | 1.0.0 | login-signup | unified-auth-flow | dt_member_role, invitations | FR-013, FR-014, FR-015, FR-030 |
| 2 | self-signup-organizer | must | organizer | 1.0.0 | login-signup, group-create, group-type-picker | self-signup-organizer-flow | group_type_config | FR-021, FR-013 |
| 3 | group-type-config | must | organizer | 1.0.0 | group-type-picker, group-create | — | group_type_config | FR-022, FR-025 |
| 4 | pluggable-distribution | must | organizer | 1.0.0 | share-out-preview, share-out-execute | share-out-flow | rosca_rotation, rosca_auction, vsla_cycle | FR-023, FR-007 |
| 5 | member-invitations | must | organizer | 1.0.0 | member-invite, join-with-code, member-list | member-invitation-flow | dt_member_invitation, invitations | FR-002, FR-024 |
| 6 | group-management | must | organizer | 1.0.0 | group-list, group-dashboard, group-create, group-type-picker | group-creation-flow | dt_group_config | FR-001, FR-022 |
| 7 | member-onboarding | must | organizer | 1.0.0 | member-list, member-profile, member-add | — | dt_member_role | FR-002 |
| 8 | meeting-lifecycle | must | organizer | 1.0.0 | meeting-calendar, meeting-conduct, meeting-summary, previous-meeting-review | meeting-flow | dt_meeting_record, dt_meeting_attendance | FR-003, FR-019 |
| 9 | savings-collection | must | organizer | 1.0.0 | savings-dashboard, meeting-conduct | meeting-flow | — | FR-004 |
| 10 | group-linked-savings | must | organizer | 1.0.0 | savings-dashboard, meeting-conduct, group-dashboard | — | — | FR-017, FR-020 |
| 11 | corpus-tracking | must | organizer | 1.0.0 | group-dashboard, meeting-conduct, meeting-summary | corpus-outflow-blocked-flow | dt_group_corpus | FR-018 |
| 12 | loan-management | must | organizer | 1.0.0 | loan-list, loan-apply, loan-detail, meeting-conduct | loan-lifecycle-flow | dt_loan_vote | FR-005, FR-006 |
| 13 | loan-ceilings | must | organizer | 1.0.0 | loan-ceiling-config, loan-apply | — | dt_group_loan_policy, dt_member_ceiling_override | FR-005 |
| 14 | share-out | must | organizer | 1.0.0 | share-out-preview, share-out-execute | share-out-flow | dt_share_out | FR-007, FR-023 |
| 15 | offline-sync | must | all | 1.0.0 | sync-status | offline-sync-flow | dt_sync_metadata | FR-008, FR-029 |
| 16 | notifications | must | all | 1.0.0 | notification-feed | — | dt_notification | FR-031 |
| 17 | end-user-dashboard | must | member | 1.0.0 | personal-dashboard, personal-savings, personal-loans, loan-request | end-user-loan-request-flow | dt_loan_request | FR-014, FR-016 |
| 24 | demo-explore | must | all | 1.0.0 | login-signup, personal-dashboard, group-dashboard | demo-explore-flow | — (offline-seeded) | FR-027, FR-028 |
| 18 | fines-tracking | should | organizer | 1.0.0 | meeting-conduct | — | dt_meeting_attendance | FR-012, FR-020 |
| 19 | multi-language | should | all | 1.0.0 | settings | — | — | FR-010 |
| 20 | loan-guarantees | should | organizer | 1.1.0 | loan-guarantee-select, loan-detail | loan-guarantee-flow | dt_loan_guarantor | FR-006 |
| 21 | loan-repayment-health | should | organizer | 1.1.0 | repayment-health-card, loan-detail, member-profile, meeting-conduct | — | — | FR-006 |
| 22 | field-officer-view | should | supervisory | 1.1.0 | field-officer-dashboard | — | dt_sync_metadata | FR-009 |
| 23 | social-fund | could | organizer | 1.1.0 | — | — | dt_social_fund, welfare_fund | FR-011 |

## companion-api-backend (External Infrastructure Gate)

> **Not an app feature** — this is the backend build + deploy prerequisite that unlocks `/device-test`.
> Until this gate is satisfied, app features **compile + build-green** but device-test returns `pending-device-verify`.
> The app talks ONLY to the companion API (extended `mcp-mifosx`, Go, Fineract-only — no Supabase, no standalone DDD service); the companion API executes Fineract calls with a service credential on behalf of the user.

| Build item | Contracts | Notes |
|---|---|---|
| P0 auth-model change | — | Per-call user credential intake; service-credential group orchestration; organizer-vs-member authz at companion tier |
| TIER-1: auth tools | COMP-AUTH-001 (self-register), COMP-AUTH-002 (login → groups+roles), COMP-AUTH-003 (me) | `go/tools/companion_auth.go` |
| TIER-1: group orchestration tools | COMP-GRP-001 (create), COMP-GRP-002 (activate), COMP-GRP-003 (associate-clients), COMP-GRP-004 (assign-role), COMP-GRP-005 (assign-staff) | `go/tools/companion_groups.go` |
| TIER-1: calendar + collection-sheet | COMP-CAL-001 (calendar), COMP-CAL-002 (get collection-sheet), COMP-CAL-003 (submit collection-sheet) | `go/tools/companion_calendar.go` |
| TIER-2: datatable CRUD | COMP-DT-001 (register), COMP-DT-002 (create row), COMP-DT-003 (read rows), COMP-DT-004 (update row), COMP-DT-005 (delete row) | `go/tools/datatables.go` |
| TIER-2: distribution execute | COMP-DIST-001 (share-out / rotation execute), COMP-DIST-002 (rosca-rotation next) | Client computes payout; server re-validates + executes |
| Fineract with self-service ENABLED | — | Community sandbox does NOT qualify; deploy a fresh instance |
| 6 datatables provisioned | group_type_config, invitations, rosca_rotation, rosca_auction, vsla_cycle, welfare_fund | Run once via COMP-DT-001 after deploy |

**Full spec**: `server-layer/COMPANION_API_BUILD_DEPLOY.md` | **Contract**: `server-layer/API_CONTRACT.yaml` (companion section)

## Milestone Roadmap

### companion-api-backend (External gate — must land before v1.0.0 device-verify)
See section above. Spec: `server-layer/COMPANION_API_BUILD_DEPLOY.md`

### v1.0.0 - Core Group Banking (17 features)
unified-auth, self-signup-organizer, group-type-config, pluggable-distribution, member-invitations, group-management, member-onboarding, meeting-lifecycle, savings-collection, group-linked-savings, corpus-tracking, loan-management, loan-ceilings, share-out, offline-sync, notifications, demo-explore
_(+ should/could riders shipping in 1.0.0: fines-tracking, multi-language, end-user-dashboard)_

### v1.1.0 - Supervision, Lending Maturity & Social
field-officer-view, social-fund, loan-guarantees, loan-repayment-health

### v2.0.0 - Scale & Integrate (future concepts — not yet defined in §features)
mobile-money-integration, web-admin-dashboard, sms-notifications, inter-group-lending, credit-scoring

## Epic Breakdown

| Epic | Features | Milestone |
|------|----------|-----------|
| Core Group Infrastructure | unified-auth, self-signup-organizer, end-user-dashboard, group-management, member-onboarding, member-invitations, demo-explore | v1.0.0 |
| Meeting & Savings Engine | meeting-lifecycle, savings-collection, group-linked-savings, corpus-tracking, fines-tracking | v1.0.0 |
| Lending & Distribution Lifecycle | loan-management, loan-ceilings, share-out, pluggable-distribution, group-type-config | v1.0.0 |
| Platform Foundation | offline-sync, multi-language, notifications | v1.0.0 |
| Supervision & Social | field-officer-view, social-fund | v1.1.0 |
| Lending Maturity | loan-guarantees, loan-repayment-health | v1.1.0 |

## Screen Inventory (33 screens)

> Single unified navigation graph. The entry screen is `login-signup` (one screen for sign-up and login). `organizer-dashboard` is the post-login home for an organizer-role session; `personal-dashboard` is the member-role home. Both live inside the one shared graph; the resolved per-group role decides which surfaces are shown.

| Screen | Archetype | Features | Surface |
|--------|-----------|----------|---------|
| login-signup | form | unified-auth, self-signup-organizer, demo-explore | all |
| organizer-dashboard | dashboard | self-signup-organizer, group-management | organizer |
| group-type-picker | form | group-type-config, group-management, self-signup-organizer | organizer |
| join-with-code | form | member-invitations, unified-auth | all |
| member-invite | form | member-invitations | organizer |
| personal-dashboard | dashboard | end-user-dashboard | member |
| personal-savings | detail_screen | end-user-dashboard | member |
| personal-loans | index_list | end-user-dashboard | member |
| loan-request | form | end-user-dashboard | member |
| group-list | index_list | group-management | organizer |
| group-dashboard | dashboard | group-management, corpus-tracking, group-linked-savings | organizer |
| group-create | form | group-management, self-signup-organizer | organizer |
| member-list | index_list | member-onboarding, member-invitations | organizer |
| member-profile | detail_screen | member-onboarding | organizer |
| member-add | form | member-onboarding | organizer |
| meeting-calendar | index_list | meeting-lifecycle | organizer |
| meeting-conduct | form | meeting-lifecycle, savings-collection, loan-management, corpus-tracking, group-linked-savings, fines-tracking | organizer |
| meeting-summary | detail_screen | meeting-lifecycle, corpus-tracking | organizer |
| previous-meeting-review | detail_screen | meeting-lifecycle | organizer |
| savings-dashboard | dashboard | savings-collection, group-linked-savings | organizer |
| loan-list | index_list | loan-management | organizer |
| loan-apply | form | loan-management, loan-ceilings | organizer |
| loan-detail | detail_screen | loan-management, loan-guarantees, loan-repayment-health | organizer |
| loan-ceiling-config | form | loan-ceilings | organizer |
| loan-guarantee-select | form | loan-guarantees | organizer |
| repayment-health-card | detail_screen | loan-repayment-health | organizer |
| share-out-preview | detail_screen | share-out, pluggable-distribution | organizer |
| share-out-execute | form | share-out, pluggable-distribution | organizer |
| sync-status | dashboard | offline-sync | all |
| notification-feed | index_list | notifications | all |
| field-officer-dashboard | dashboard | field-officer-view | supervisory |
| settings | settings | multi-language | all |

## Data Entities (8)

| Entity | Key Fields | Fineract Mapping |
|--------|------------|------------------|
| Group | name, cycle, rules, currency, corpus_balance, group_type_config | Center + group_type_config datatable |
| Member | name, phone, photo, role (per group) | Client + dt_member_role |
| Meeting | number, date, attendance, collected, opening_balance, closing_balance | dt_meeting_record |
| SavingsTransaction | member, amount, type (group-linked / individual) | Savings Transaction |
| Loan | member, amount, rate, status | Loan Product |
| LoanRepayment | loan, amount, date | Loan Transaction |
| AttendanceRecord | meeting, member, present, late, fine | dt_meeting_attendance |
| SyncQueue | entity, operation, payload, status | Batch API |

## API Coverage

- **Fineract endpoints**: 55+ (centers, groups, clients, savings, loans, charges, reports, batch, self-service)
- **Companion API contracts**: 16 (COMP-AUTH-001..003, COMP-GRP-001..005, COMP-CAL-001..003, COMP-DT-001..005, COMP-DIST-001/002) — abstract contract, backend built later
- **MCP tools**: 101 (full programmatic access via extended Mifos MCP Server / mcp-mifosx)
- **Custom Data Tables**: 11 Fineract-native domain extensions + 6 companion datatables provisioned via COMP-DT-001
- **Feature coverage**: 100% (19/19 API-bearing features fully resolvable; §api_gap_analysis)
- **Backend model**: Fineract-only. Companion API executes all Fineract money movements with a service credential; the app never calls Fineract directly.

### Data Tables — Custom API Design Pattern

**Fineract-native domain extension tables (11):**

| Data Table | Attached To | Feature | Purpose |
|-----------|-------------|---------|---------|
| dt_group_config | m_center | group-management | Cycle rules, contribution limits, loan multiplier, fine amounts, cycle dates |
| dt_meeting_record | m_center | meeting-lifecycle | Per-meeting summary: attendance, totals, decisions |
| dt_meeting_attendance | m_client | meeting-lifecycle, fines-tracking | Per-member attendance: present/late/fined |
| dt_member_role | m_client | unified-auth, member-onboarding | Per-(member, group) role — organizer/treasurer/chairperson/secretary/member; drives per-group RBAC |
| dt_share_out | m_center | share-out | Cycle share-out record: pool, distribution, status |
| dt_social_fund | m_center | social-fund | Emergency fund balance and disbursement tracking |
| dt_loan_vote | m_loan | loan-management | Loan approval voting: for/against/chairperson approval |
| dt_sync_metadata | m_center | offline-sync | Sync state: last sync, pending ops, conflicts |
| dt_loan_request | m_client | end-user-dashboard | Member loan requests submitted for organizer review at meetings |
| dt_group_corpus | m_center | corpus-tracking | Running fund balance: current, inflows, outflows, meeting open/close |
| dt_member_invitation | m_client | member-invitations | Invite token audit trail — code, role, expiry, accepted state |

**Companion datatables (6) — provisioned via COMP-DT-001 at deploy:**

| Datatable | Attached To | Feature | Purpose |
|-----------|-------------|---------|---------|
| group_type_config | m_group | group-type-config | 2-axis GroupTypeConfig per group (pool_model, contribution_model) + payout/lending/social-fund/cycle/governance params |
| rosca_rotation | m_group | pluggable-distribution | ROSCA rotation state — recipient order, current turn, payout per round |
| rosca_auction | m_group | pluggable-distribution | Chit/hui auction bids — per-round bids, winning bid, discount |
| vsla_cycle | m_group | pluggable-distribution, share-out | VSLA/SILC cycle state — cycle number, shares issued, share value, formula override |
| welfare_fund | m_group | social-fund | Welfare/burial fund balance + disbursement log |
| invitations | m_group | member-invitations, unified-auth | Invite tokens — token, group, inviter, role_to_assign, expires_at, accepted_at |

---

> Generated from idea-plan.yaml (§features, §screens, §release_plan) | Last updated: 2026-07-17 (global self-signup pivot regeneration)
