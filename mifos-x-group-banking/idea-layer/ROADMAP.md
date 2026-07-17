# Idea Layer Roadmap — CommonPurse (mifos-x-group-banking)

> Source of truth: `FEATURES.md` | Design context: `DESIGN_CONTEXT.md`
> Two client types: Admin (treasurer/chairperson/FO) | End User (self-service member)

---

## Feature Status Matrix

| # | Feature | Priority | Client | v1.0.0 | v1.1.0 | v2.0.0 | Admin | End User | Status |
|---|---------|----------|--------|--------|--------|--------|-------|----------|--------|
| 0 | companion-api-backend | **external-gate** | server-infra | pre-req | | | — | — | pending-deploy |
| 1 | authentication | must | both | ✓ | | | ✓ | ✓ | designed |
| 2 | end-user-dashboard | must | end_user | ✓ | | | | ✓ | designed |
| 3 | group-management | must | admin | ✓ | | | ✓ | | designed |
| 4 | member-onboarding | must | admin | ✓ | | | ✓ | | designed |
| 5 | meeting-lifecycle | must | admin | ✓ | | | ✓ | | designed |
| 6 | savings-collection | must | admin | ✓ | | | ✓ | | designed |
| 7 | group-linked-savings | must | admin | ✓ | | | ✓ | | designed |
| 8 | corpus-tracking | must | admin | ✓ | | | ✓ | | designed |
| 9 | loan-management | must | admin | ✓ | | | ✓ | | designed |
| 10 | share-out | must | admin | ✓ | | | ✓ | | designed |
| 11 | offline-sync | must | both | ✓ | | | ✓ | ✓ | designed |
| 12 | fines-tracking | should | admin | ✓ | | | ✓ | | designed |
| 13 | multi-language | should | both | ✓ | | | ✓ | ✓ | designed |
| 14 | field-officer-view | should | admin | | ✓ | | ✓ | | designed |
| 15 | social-fund | could | admin | | ✓ | | ✓ | | designed |
| 16 | mobile-money-integration | future | both | | | ✓ | ✓ | ✓ | planned |
| 17 | web-admin-dashboard | future | admin | | | ✓ | ✓ | | planned |
| 18 | sms-notifications | future | both | | | ✓ | ✓ | ✓ | planned |

---

## Companion API Build + Deploy (External Gate — pre-v1.0.0)

> **Status: external_gate** — This is not an app release milestone. It is the backend infrastructure
> prerequisite that must be satisfied before `/device-test` can pass and `matrix-green` can be reached.
> Until this gate is satisfied, app features compile + build-green but `/device-test` returns `pending-device-verify`.

**What must land** (full spec: `server-layer/COMPANION_API_BUILD_DEPLOY.md`):

| # | Item | Priority | Contracts |
|---|------|----------|-----------|
| 1 | Auth-model change in mcp-mifosx: per-call user credential + service-credential group orchestration | P0 | — |
| 2 | TIER-1 tools: self-register, login, me | P0 | COMP-AUTH-001..003 |
| 3 | TIER-1 tools: group create/activate/associate/assign-role/assign-staff | P1 | COMP-GRP-001..005 |
| 4 | TIER-1 tools: calendar + collection-sheet | P1 | COMP-CAL-001..003 |
| 5 | TIER-2 datatable CRUD tools | P0 | COMP-DT-001..005 |
| 6 | TIER-2 distribution execute tools | P1 | COMP-DIST-001/002 |
| 7 | Self-service-enabled Fineract deployed (tenant/office strategy decided) | P0 | — |
| 8 | 6 companion datatables provisioned via COMP-DT-001 | P0 | dt_group_type_config, dt_companion_invitations, dt_rosca_rotation, dt_rosca_auction, dt_vsla_cycle, dt_welfare_fund |
| 9 | App companion base URL wired to deployed mcp-mifosx | P0 | — |

**Gate criteria**: End-to-end Maestro flow (signup → create group → invite → savings/loan → share-out) passes on device.

---

## Implementation Priority Order

Features must be implemented in dependency order. Tier-0 features unblock all others.

### Tier 0 — Foundation (must build first)
1. **authentication** — All other features require a valid session
   - Screens: client-type-selector, login, admin-dashboard, settings-logout-dialog
   - API: `POST /authentication`, `POST /self/authentication`
   - DI: AuthRepository, PreferencesRepository

2. **group-management** — Group context required for all admin features
   - Screens: group-list, group-dashboard, group-create
   - API: `GET /centers`, `POST /centers`, `GET /datatables/dt_group_config`
   - Depends on: authentication

### Tier 1 — Core Group Operations
3. **member-onboarding** — Requires group to exist
   - Screens: member-list, member-profile, member-add, member-savings-detail
   - API: `GET /groups/{id}/clients`, `POST /clients`, `POST /savingsaccounts`
   - Depends on: group-management

4. **meeting-lifecycle** — Requires members with savings accounts
   - Screens: meeting-calendar, meeting-conduct, meeting-summary, previous-meeting-review
   - API: `POST /datatables/dt_meeting_record`, `POST /datatables/dt_meeting_attendance`
   - Depends on: member-onboarding

### Tier 2 — Financial Operations
5. **savings-collection** — Runs during meeting-lifecycle
   - Screens: savings-dashboard (standalone), meeting-conduct (shared)
   - API: `POST /savingsaccounts/{id}/transactions?command=deposit`
   - Depends on: meeting-lifecycle

6. **corpus-tracking** — Runs alongside savings-collection
   - Screens: group-dashboard (corpus card), meeting-conduct (close step)
   - API: `GET /datatables/dt_group_corpus`, `POST /datatables/dt_group_corpus`
   - Depends on: savings-collection

7. **loan-management** — Requires corpus to be tracked
   - Screens: loan-list, loan-apply, loan-detail, loan-repayment-dialog, loan-mark-defaulted-dialog
   - API: `POST /loans`, `POST /loans/{id}/transactions?command=approve`
   - Depends on: corpus-tracking

### Tier 3 — Distribution & Platform
8. **share-out** — Requires all loans tracked
   - Screens: share-out-preview, share-out-execute
   - Depends on: loan-management, corpus-tracking

9. **offline-sync** — Foundation for all offline-first features
   - Screens: sync-status
   - API: `GET/POST /datatables/dt_sync_metadata`, Fineract Batch API
   - Depends on: (all data operations)

10. **fines-tracking** — Embedded in meeting-conduct
    - Depends on: meeting-lifecycle

11. **group-linked-savings** — Extends savings-dashboard
    - Depends on: savings-collection, group-management

12. **multi-language** — Applies to all screens
    - Screens: settings
    - Depends on: (none — can be implemented any time)

13. **end-user-dashboard** — Self-service parallel track
    - Screens: personal-dashboard, personal-savings, personal-loans, loan-request
    - Depends on: authentication (self-service path)

---

## v1.0.0 — Core Group Banking (Target: 13 features)

**Scope**: authentication, group-management, member-onboarding, meeting-lifecycle,
savings-collection, group-linked-savings, corpus-tracking, loan-management, share-out,
offline-sync, fines-tracking, multi-language, end-user-dashboard

**Screen count**: 30 (all current screens)
**Platforms**: Android + iOS (KMP)
**Backend**: Fineract sandbox + production

**Definition of Done**:
- All 30 screens implemented in Compose Multiplatform
- All 55+ Fineract endpoints integrated
- All 10 custom datatables operational
- Offline mode with sync queue functional
- WCAG AA contrast compliance
- 4 languages supported (en/sw/fr/hi)

---

## v1.1.0 — Supervision & Social

**Scope**: field-officer-view, social-fund

**New screens**: field-officer-dashboard (already designed)
**Social fund**: emergency fund balance tracking via dt_social_fund

---

## v2.0.0 — Scale & Integrate

| Feature | Description |
|---------|-------------|
| mobile-money-integration | M-Pesa / MTN Mobile Money for deposits and loan disbursements |
| web-admin-dashboard | React-based admin portal for multi-group management |
| sms-notifications | Meeting reminders, repayment alerts, share-out notifications via SMS |
| inter-group-lending | Groups can lend to each other using Fineract inter-office transfers |
| credit-scoring | Basic credit scoring from repayment history to set loan ceilings |

---

> Generated by /idea-migration reference | 2026-05-08
> Aligned with: FEATURES.md milestones, DESIGN_CONTEXT.md principles
