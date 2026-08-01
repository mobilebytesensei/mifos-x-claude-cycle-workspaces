# Idea Layer Roadmap — CommonPurse (mifos-x-group-banking)

> Source of truth: `idea-plan.yaml` (§features, §screens, §release_plan) | Feature detail: `FEATURES.md` | Design context: `DESIGN_CONTEXT.md`
> **One unified identity — self-signup.** Anyone downloads → self-registers → creates or joins a group. There is no "admin vs end-user" split. Capabilities are auto-resolved **per group** after a single login, based on the role the user holds in that specific group (organizer vs member). (Global self-signup pivot, 2026-07-17.)
> **Production launch evolve (2026-08-01):** added `demo-explore` (FR-027) to v1.0.0; added a Play-Store internal-testing track before closed alpha; server-ready requirements (server demo-seed FR-028, idea→server auto-migrate FR-029) + first-class accept-invitation (FR-030) + user-facing notifications (FR-031). See `evolve-plans/20260801-production-signup-server-migration.md`.

---

## Feature Status Matrix

> **Surface** = capability surface: `all` (shared for every logged-in user) · `organizer` (organizer/treasurer/chairperson write surface within a group) · `member` (self-service member surface) · `supervisory` (opt-in field-officer tier). Resolved per group after login — never a locally-stored client type.

| # | Feature | Priority | Surface | v1.0.0 | v1.1.0 | v2.0.0 | Status |
|---|---------|----------|---------|--------|--------|--------|--------|
| 0 | companion-api-backend | **external-gate** | server-infra | pre-req | | | pending-deploy |
| 1 | unified-auth | must | all | ✓ | | | designed |
| 2 | self-signup-organizer | must | organizer | ✓ | | | designed |
| 3 | group-type-config | must | organizer | ✓ | | | designed |
| 4 | pluggable-distribution | must | organizer | ✓ | | | designed |
| 5 | member-invitations | must | organizer | ✓ | | | designed |
| 6 | group-management | must | organizer | ✓ | | | designed |
| 7 | member-onboarding | must | organizer | ✓ | | | designed |
| 8 | meeting-lifecycle | must | organizer | ✓ | | | designed |
| 9 | savings-collection | must | organizer | ✓ | | | designed |
| 10 | group-linked-savings | must | organizer | ✓ | | | designed |
| 11 | corpus-tracking | must | organizer | ✓ | | | designed |
| 12 | loan-management | must | organizer | ✓ | | | designed |
| 13 | loan-ceilings | must | organizer | ✓ | | | designed |
| 14 | share-out | must | organizer | ✓ | | | designed |
| 15 | offline-sync | must | all | ✓ | | | designed |
| 16 | notifications | must | all | ✓ | | | designed |
| 17 | end-user-dashboard | must | member | ✓ | | | designed |
| 17+ | demo-explore | must | all | ✓ | | | designed (evolve 2026-08-01) |
| 18 | fines-tracking | should | organizer | ✓ | | | designed |
| 19 | multi-language | should | all | ✓ | | | designed |
| 20 | loan-guarantees | should | organizer | | ✓ | | designed |
| 21 | loan-repayment-health | should | organizer | | ✓ | | designed |
| 22 | field-officer-view | should | supervisory | | ✓ | | designed |
| 23 | social-fund | could | organizer | | ✓ | | designed |
| 24 | mobile-money-integration | future | all | | | ✓ | planned |
| 25 | web-admin-dashboard | future | supervisory | | | ✓ | planned |
| 26 | sms-notifications | future | all | | | ✓ | planned |
| 27 | inter-group-lending | future | organizer | | | ✓ | planned |
| 28 | credit-scoring | future | organizer | | | ✓ | planned |

---

## Companion API Build + Deploy (External Gate — pre-v1.0.0)

> **Status: external_gate** — This is not an app release milestone. It is the backend infrastructure
> prerequisite that must be satisfied before `/device-test` can pass and `matrix-green` can be reached.
> Until this gate is satisfied, app features compile + build-green but `/device-test` returns `pending-device-verify`.
> Backend = extended `mcp-mifosx` (Go), **Fineract-only** (no Supabase, no standalone DDD service). The app talks ONLY to the companion API; the companion API executes Fineract calls with a service credential on behalf of the user.

**What must land** (full spec: `server-layer/COMPANION_API_BUILD_DEPLOY.md`):

| # | Item | Priority | Contracts |
|---|------|----------|-----------|
| 1 | Auth-model change in mcp-mifosx: per-call user credential + service-credential group orchestration | P0 | — |
| 2 | TIER-1 tools: self-register, login (→ groups+roles), me | P0 | COMP-AUTH-001..003 |
| 3 | TIER-1 tools: group create/activate/associate/assign-role/assign-staff | P0/P1 | COMP-GRP-001..005 |
| 4 | TIER-1 tools: calendar + collection-sheet | P1 | COMP-CAL-001..003 |
| 5 | TIER-2 datatable CRUD tools | P0 | COMP-DT-001..005 |
| 6 | TIER-2 distribution execute tools | P1 | COMP-DIST-001/002 |
| 7 | Self-service-enabled Fineract deployed (tenant/office strategy decided) | P0 | — |
| 8 | 6 companion datatables provisioned via COMP-DT-001 | P0 | group_type_config, invitations, rosca_rotation, rosca_auction, vsla_cycle, welfare_fund |
| 9 | App companion base URL wired to deployed mcp-mifosx | P0 | — |

**Gate criteria**: End-to-end Maestro flow (self-signup → create group → invite → savings/loan → share-out) passes on device.

---

## Implementation Priority Order

Features must be implemented in dependency order. Tier-0 features unblock all others.

### Tier 0 — Foundation (must build first)
1. **unified-auth** — All other features require a valid unified session
   - Screens: login-signup (single sign-up + login screen — no client-type selector)
   - API: companion `COMP-AUTH-001` (self-register), `COMP-AUTH-002` (login → groups+roles), `COMP-AUTH-003` (me)
   - Post-login: resolve per-group role from `dt_member_role`; zero-group user → create/join empty state
   - DI: AuthRepository, PreferencesRepository (PIN/biometric cache for offline re-auth)

2. **self-signup-organizer** — Mints the organizer identity that unblocks group creation
   - Screens: login-signup, group-create, group-type-picker
   - API: `COMP-AUTH-001` + `COMP-GRP-001` (create) + `COMP-GRP-002` (activate)
   - Depends on: unified-auth

3. **group-type-config** — Group type must be pickable before a group can be fully configured
   - Screens: group-type-picker, group-create
   - API: `COMP-DT-001` (register group_type_config schema) + `COMP-DT-002..005` (CRUD)
   - Depends on: unified-auth

4. **group-management** — Group context required for all organizer features
   - Screens: group-list, group-dashboard, group-create, group-type-picker
   - API: `COMP-GRP-001/002`, Fineract Centers, `dt_group_config`
   - Depends on: self-signup-organizer, group-type-config

### Tier 1 — Core Group Operations
5. **member-invitations** — Remote-recruit path; associates invitees to a group
   - Screens: member-invite, join-with-code, member-list
   - API: `COMP-GRP-003` (associate-clients), invitations datatable, `dt_member_invitation`
   - Depends on: group-management, unified-auth

6. **member-onboarding** — In-meeting walk-up adds + role assignment
   - Screens: member-list, member-profile, member-add
   - API: Fineract Clients, `COMP-GRP-004` (assign-role), `dt_member_role`
   - Depends on: group-management

7. **meeting-lifecycle** — Requires members with savings accounts
   - Screens: meeting-calendar, meeting-conduct, meeting-summary, previous-meeting-review
   - API: `COMP-CAL-001..003`, `dt_meeting_record`, `dt_meeting_attendance`
   - Depends on: member-onboarding

### Tier 2 — Financial Operations
8. **savings-collection** — Runs during meeting-lifecycle
   - Screens: savings-dashboard, meeting-conduct (shared)
   - API: Fineract Savings deposit/withdrawal, `COMP-CAL-002/003` collection-sheet
   - Depends on: meeting-lifecycle

9. **group-linked-savings** — Dual savings (mandatory group-linked + voluntary individual)
   - Screens: savings-dashboard, meeting-conduct, group-dashboard
   - Depends on: savings-collection, group-management

10. **corpus-tracking** — Runs alongside savings-collection; blocks over-disbursement
    - Screens: group-dashboard (corpus card), meeting-conduct (close step), meeting-summary
    - API: `dt_group_corpus`
    - Depends on: savings-collection

11. **loan-management** — Requires corpus to be tracked
    - Screens: loan-list, loan-apply, loan-detail, meeting-conduct
    - API: Fineract Loans, `dt_loan_vote`
    - Depends on: corpus-tracking

12. **loan-ceilings** — Per-group ceiling rule enforced at loan-apply
    - Screens: loan-ceiling-config, loan-apply
    - API: `dt_group_loan_policy`, `dt_member_ceiling_override`
    - Depends on: loan-management

### Tier 3 — Distribution & Platform
13. **pluggable-distribution** — Strategy selected by group_type (share-out / ROSCA rotation / auction)
    - Screens: share-out-preview, share-out-execute
    - API: `COMP-DIST-001` (execute), `COMP-DIST-002` (rotation next), rosca_rotation / rosca_auction / vsla_cycle datatables
    - Depends on: group-type-config, share-out

14. **share-out** — End-of-cycle distribution (delegates strategy to pluggable-distribution)
    - Screens: share-out-preview, share-out-execute
    - API: Fineract withdrawal, `dt_share_out`, `COMP-DIST-001`
    - Depends on: loan-management, corpus-tracking, pluggable-distribution

15. **offline-sync** — Foundation for all offline-first features (core-base/store)
    - Screens: sync-status
    - API: Fineract Batch API, `dt_sync_metadata`
    - Depends on: (all data operations)

16. **notifications** — Push + in-app feed via user-scoped sync tier
    - Screens: notification-feed
    - API: `dt_notification`
    - Depends on: offline-sync

17. **fines-tracking** — Embedded in meeting-conduct
    - Depends on: meeting-lifecycle

18. **multi-language** — Applies to all screens
    - Screens: settings
    - Depends on: (none — can be implemented any time)

19. **end-user-dashboard** — Member self-service surface (resolved for member-role sessions)
    - Screens: personal-dashboard, personal-savings, personal-loans, loan-request
    - Depends on: unified-auth (member-role resolution)

20. **demo-explore** — Guest offline-seeded demo session for exploring the app without registering (evolve 2026-08-01)
    - Screens: login-signup (Demo Explore button + confirm dialog), personal-dashboard, group-dashboard
    - Data: LOCAL offline-seeded demo data — works with NO live server (server demo-seed FR-028 backs the live variant, externally gated)
    - Depends on: none for the offline path (self-contained); dashboards for exploration

---

## v1.0.0 — Core Group Banking (17 core features)

**Scope (§release_plan.milestones "1.0.0")**: unified-auth, self-signup-organizer, group-type-config,
pluggable-distribution, member-invitations, group-management, member-onboarding, meeting-lifecycle,
savings-collection, group-linked-savings, corpus-tracking, loan-management, loan-ceilings, share-out,
offline-sync, notifications, demo-explore
_(+ should/could riders shipping in 1.0.0: fines-tracking, multi-language, end-user-dashboard)_

**Rollout tracks (§release_plan.rollout_strategy)**: Play-Store **internal-testing** (first on-device distribution, ≤20 trusted testers) → **closed_alpha** (2 partner-NGO groups, KE) → **beta** (20 groups KE+UG) → **GA** (open Play Store + App Store). The internal-testing track was added 2026-08-01 for "first testing" before the NGO closed alpha.

**Screen count**: 33 (single unified navigation graph)
**Platforms**: Android + iOS + Desktop (KMP)
**Backend**: Fineract via the companion API (extended mcp-mifosx) — external gate above

**Definition of Done**:
- All 33 screens implemented in Compose Multiplatform, one unified nav graph, per-group role resolution
- Companion API contracts (COMP-AUTH/GRP/CAL/DT/DIST) integrated; app never calls Fineract directly
- All Fineract-native + companion datatables operational
- Offline mode with Store5 + SQLDelight + Bookkeeper outbox functional
- WCAG AA contrast compliance
- 4 languages supported (en/sw/fr/hi)
- End-to-end Maestro flow (self-signup → create group → invite → savings/loan → share-out) green on device

---

## v1.1.0 — Supervision, Lending Maturity & Social

**Scope (§release_plan.milestones "1.1.0")**: field-officer-view, social-fund, loan-guarantees, loan-repayment-health

**New screens**: field-officer-dashboard, loan-guarantee-select, repayment-health-card (all already designed)
**Supervisory tier**: opt-in field-officer cross-group read-only monitoring (NOT the default identity)
**Social fund**: emergency fund balance tracking via dt_social_fund / welfare_fund

---

## v2.0.0 — Scale & Integrate

> `_status: future_concept` — placeholders, not yet defined in §features. Define before implementation.

| Feature | Description |
|---------|-------------|
| mobile-money-integration | M-Pesa / MTN Mobile Money for deposits and loan disbursements |
| web-admin-dashboard | React-based portal for multi-group program management |
| sms-notifications | Meeting reminders, repayment alerts, share-out notifications via SMS |
| inter-group-lending | Groups can lend to each other using Fineract inter-office transfers |
| credit-scoring | Basic credit scoring from repayment history to set loan ceilings |

---

> Regenerated from idea-plan.yaml (§features, §screens, §release_plan) | 2026-07-17 (global self-signup pivot)
> Aligned with: FEATURES.md matrix + milestones, REQUIREMENTS.md, IDEA.md, DESIGN_CONTEXT.md principles
