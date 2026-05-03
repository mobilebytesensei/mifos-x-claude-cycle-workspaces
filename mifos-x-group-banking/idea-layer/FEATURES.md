# Features - CommonPurse (mifos-x-group-banking)

> 15 features | 11 must | 3 should | 1 could

## Feature Matrix

> 15 features | 11 must | 3 should | 1 could
> Two client types: **Admin** (staff auth, group management) | **End User** (self-service, personal dashboard)
> Source: idea-plan.yaml + Community Research (CR-003: professionally curated)

| # | Feature | Priority | Client | Version | Screens | Flow | API | Data Tables | Reqs |
|---|---------|----------|--------|---------|---------|------|-----|-------------|------|
| 1 | authentication | must | both | 1.0.0 | client-type-selector, login | admin-auth, end-user-auth | 2 | dt_member_role | FR-013-15 |
| 2 | end-user-dashboard | must | end_user | 1.0.0 | personal-dashboard, personal-savings, personal-loans, loan-request | end-user-loan-request | 4 | dt_loan_request | FR-014, FR-016 |
| 3 | group-management | must | admin | 1.0.0 | group-list, group-dashboard, group-create | group-creation | 4 | dt_group_config | FR-001, FR-020 |
| 4 | member-onboarding | must | admin | 1.0.0 | member-list, member-profile, member-add | - | 3 | dt_member_role | FR-002 |
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

## Milestone Roadmap

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

## Screen Inventory (24 screens)

| Screen | Archetype | Features |
|--------|-----------|----------|
| client-type-selector | form | authentication |
| login | form | authentication |
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
| meeting-calendar | index_list | meeting-lifecycle |
| meeting-conduct | form | meeting-lifecycle, savings-collection, loan-management, corpus-tracking, group-linked-savings, fines-tracking |
| meeting-summary | detail_screen | meeting-lifecycle |
| previous-meeting-review | detail_screen | meeting-lifecycle |
| savings-dashboard | dashboard | savings-collection, group-linked-savings |
| loan-list | index_list | loan-management |
| loan-apply | form | loan-management |
| loan-detail | detail_screen | loan-management |
| share-out-preview | detail_screen | share-out |
| share-out-execute | form | share-out |
| sync-status | dashboard | offline-sync |
| field-officer-dashboard | dashboard | field-officer-view |
| settings | settings | multi-language |

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
