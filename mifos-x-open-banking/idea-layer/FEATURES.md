# Feature Registry — Mifos X Open Banking

> **Total**: 26 (+9 deferred placeholder routes) | **Designed**: 0 | **Implemented**: 25 in source (2 unreachable from navigation) + 1 planned (consent-relay)
> **Last Updated**: 2026-10-21
> Managed by `/idea`. Read by `/design`, `/implement`, `/gap-planning-project`.
> Source-derived from openMF/mifos-x-open-banking @ d5c6782 — implementation exists ahead of the idea-layer.

---

## Features

| # | Feature | Description | Flow | Priority | Dependencies | FR IDs | SFR IDs | DR IDs | Screens | API Endpoints | Platform Targets | Version | Designed | Impl | Status |
|:-:|---------|-------------|------|:--------:|-------------|--------|---------|--------|:-------:|:------------:|-----------------|:-------:|:--------:|:----:|--------|
| 1 | home | Dashboard: greeting, quick actions, cards and accounts with balances | view-accounts | must | login, account-detail, send-money, payments-schedule-payment, payments-standing-order, vrp, settings | FR-001, FR-002, FR-039, FR-048 | — | — | 1 | 3 | all | 1.0.0 | — | ✅ | implemented |
| 2 | accounts | Filterable list of all connected accounts | — | should | login, account-detail | FR-003, FR-048 | — | — | 1 | 2 | all | 1.0.0 | — | ⚠️ | implemented_unreachable |
| 3 | account-detail | Account header, balances and Explore chips into each AIS resource | view-accounts | must | transactions, statements, standing-orders, direct-debits, scheduled-payments, beneficiaries, product, account-holder | FR-004, FR-005, FR-040 | — | — | 1 | 2 | all | 1.0.0 | — | ✅ | implemented |
| 4 | account-holder | Account holder (party) identity details | — | could | — | FR-006, FR-040 | — | — | 1 | 1 | all | 1.0.0 | — | ✅ | implemented |
| 5 | transactions | Paginated, filterable, searchable transaction history | browse-transactions | must | — | FR-007, FR-008, FR-009, FR-040 | — | — | 1 | 1 | all | 1.0.0 | — | ✅ | implemented |
| 6 | transaction-detail | Full detail of a single transaction | browse-transactions | must | — | FR-010, FR-040 | — | — | 1 | 1 | all | 1.0.0 | — | ✅ | implemented |
| 7 | scheduled-payments | Scheduled (future-dated) payments for an account | — | should | — | FR-011, FR-040 | — | — | 1 | 1 | all | 1.0.0 | — | ✅ | implemented |
| 8 | standing-orders | Read-only standing orders on an account | — | should | — | FR-012, FR-013, FR-040 | — | — | 1 | 1 | all | 1.0.0 | — | ✅ | implemented |
| 9 | direct-debits | Read-only direct-debit mandates on an account | — | should | — | FR-012, FR-013, FR-040 | — | — | 1 | 1 | all | 1.0.0 | — | ✅ | implemented |
| 10 | beneficiaries | Searchable saved payees for an account | — | should | — | FR-014, FR-040 | — | — | 1 | 1 | all | 1.0.0 | — | ✅ | implemented |
| 11 | product | Product terms (fees, interest tiers, overdraft) | — | could | — | FR-015, FR-040 | — | — | 1 | 1 | all | 1.0.0 | — | ✅ | implemented |
| 12 | statements | Statement list with file download | statements-download | should | — | FR-016, FR-017, FR-040 | — | — | 1 | 2 | all (download no-op on web) | 1.0.0 | — | ✅ | implemented |
| 13 | statement-detail | Statement breakdown with PDF download and drill-down | statements-download | should | — | FR-016, FR-018, FR-040 | — | — | 1 | 3 | all | 1.0.0 | — | ✅ | implemented |
| 14 | login | Onboarding intro and AIS consent request → HSBC authorisation redirect | connect-bank | must | — | FR-019, FR-020, FR-024 | — | — | 3 | 3 | all | 1.0.0 | — | ✅ | implemented |
| 15 | consent-callback | Handles the AIS redirect: completes sign-in or surfaces denial/security errors | connect-bank | must | — | FR-021, FR-022 | — | — | 1 | 2 | all | 1.0.0 | — | ✅ | implemented |
| 16 | consent-list | Connected-bank consents with expiry warnings and renew path | manage-consent | must | — | FR-023, FR-024 | — | — | 1 | 2 | all | 1.0.0 | — | ✅ | implemented |
| 17 | consent-detail | Consent permissions and expiry with re-confirm and revoke | manage-consent | must | — | FR-024, FR-025 | — | — | 1 | 3 | all | 1.0.0 | — | ✅ | implemented |
| 18 | payments-hub | Entry menu for payment products | — | should | — | FR-026, FR-048 | — | — | 1 | 0 | all | 1.0.0 | — | ⚠️ | implemented_unreachable |
| 19 | send-money | Immediate domestic/international payment initiation (PIS) | send-money | must | — | FR-027–FR-031, FR-047 | — | — | 2 | 6 | all | 1.0.0 | — | ✅ | implemented |
| 20 | payments-schedule-payment | Future-dated single payment initiation | schedule-payment | must | — | FR-027–FR-029, FR-031, FR-032, FR-047 | — | — | 2 | 6 | all | 1.0.0 | — | ✅ | implemented |
| 21 | payments-standing-order | Standing-order mandate creation via PIS consent | standing-order | must | — | FR-027–FR-029, FR-031, FR-033, FR-047 | — | — | 2 | 6 | all | 1.0.0 | — | ✅ | implemented |
| 22 | payment-consent | Completes a payment after bank authorisation and submits the staged draft | payment-failure-recovery | must | — | FR-034, FR-035 | — | — | 1 | 16 | all | 1.0.0 | — | ✅ | implemented |
| 23 | payment-status | Payment receipt and live status timeline | send-money | must | — | FR-036 | — | — | 1 | 7 | all | 1.0.0 | — | ✅ | implemented |
| 24 | settings | Theme, consents, privacy policy, open-source licences | settings-licences | should | — | FR-037, FR-038, FR-046 | — | — | 2 | 1 | all | 1.0.0 | — | ✅ | implemented |
| 25 | vrp | Variable Recurring Payments: setup, callback, consent list/detail/revoke, pay | vrp | should | — | FR-041–FR-045 | — | — | 5 | 10 | all | 1.0.0 | — | ✅ | implemented |
| 26 | consent-relay | Open-source OAuth consent relay on Cloudflare Pages — reads the bank's fragment, hands off to desktop loopback or the mobile app | connect-bank | must | consent-callback, payment-consent, vrp | FR-050–FR-052, NFR-011 | — | — | 1 | 0 | web-hosted (relay/) | 2026.11.0 | — | — | scaffold |

### Deferred (placeholder routes — registered, render PlaceholderScreen only)

| Feature | Reason | Target |
|---------|--------|:------:|
| cards | No OBIE card API in scope | — |
| atm-locator | Reached from AccountDetail ATM chip; needs OB ATM open-data API | 2027.1 |
| insights | PFM placeholder | — |
| fx-rates | Placeholder | — |
| change-password / forgot-password | PSU credentials live at the ASPSP — likely remove | — |
| about-legal | About / ToS / Privacy — needed for store listing | 2026.11.0 |
| standing-order-detail / direct-debit-detail | Placeholder detail/edit routes | — |

> FR-049 (401/403 → LoginRenew/Consents) applies to every AIS feature: account-detail, account-holder, transactions, transaction-detail, scheduled-payments, standing-orders, direct-debits, beneficiaries, product, statements, statement-detail, payment-status.

---

## Feature Dependencies

```
login ──► [bank] ──► consent-relay (Cloudflare Pages) ──► consent-callback ──► home
payment forms / vrp ──► [bank] ──► consent-relay ──► payment-consent / vrp-callback
home ──► account-detail ──► { transactions ──► transaction-detail,
                              statements ──► statement-detail ──► transaction-detail,
                              standing-orders, direct-debits, scheduled-payments,
                              beneficiaries, product, account-holder }
home ──► { send-money, payments-schedule-payment, payments-standing-order } ──► payment-consent ──► payment-status
home ──► vrp (consents → setup → callback → payment)
home ──► settings ──► consent-list ──► consent-detail ──► (revoke) login
accounts, payments-hub: registered graphs with no caller (unreachable)
```

---

## Feature-Flow Mapping

| Feature | User Flow | Screens | Entry Point |
|---------|-----------|:-------:|-------------|
| login, consent-callback | connect-bank, consent-callback-failures | 3 | App launch with no active consent |
| home, account-detail | view-accounts, expired-psu-token, offline | 2 | AuthenticatedGraph start |
| transactions, transaction-detail | browse-transactions | 2 | Account detail → Transactions chip |
| statements, statement-detail | statements-download | 2 | Account detail → Statements chip |
| send-money, payment-consent, payment-status | send-money, payment-failure-recovery | 4 | Home quick action |
| payments-schedule-payment | schedule-payment | 2 | Home quick action |
| payments-standing-order | standing-order | 2 | Home quick action |
| vrp | vrp | 5 | Home quick action |
| consent-list, consent-detail | manage-consent | 2 | Settings → Consents |
| settings | settings-licences | 2 | Home avatar |

---

## Feature Acceptance Criteria

> Per-feature acceptance criteria linked to FR entries (source-derived from tests). Used by `/implement` for TDD test generation.

### home
- [ ] AC-001: Card accounts appear only in Cards, never in Accounts (FR-001)
- [ ] AC-002: Greeting is Morning before 12:00, Afternoon 12:00–18:00, Evening after (FR-001)
- [ ] AC-003: RetryLoad refreshes the overview (FR-001)

### accounts
- [ ] AC-001: 4 type filters, none Global; CACC matches Current (FR-003)
- [ ] AC-002: Empty list shows the Empty state (FR-003)
- [ ] AC-003: Reachable from the app shell (gap — currently unreachable)

### account-detail
- [ ] AC-001: No balances shows Empty but keeps the header (FR-004)
- [ ] AC-002: 403 maps to ConsentWithdrawn, not retriable (FR-040)
- [ ] AC-003: Each chip passes accountId to its destination (FR-005)

### transactions
- [ ] AC-001: MONEY_IN shows only credits; MONEY_OUT only debits (FR-008)
- [ ] AC-002: Search is case-insensitive on description (FR-008)
- [ ] AC-003: LoadMore follows the next cursor (FR-009)

### login
- [ ] AC-001: StartOAuth persists state nonce and consentId before launching the browser (FR-020)
- [ ] AC-002: StartOAuth clears orphaned pending auth and is a no-op while Authorising or in Error (FR-020)
- [ ] AC-003: 400/401/500/network map to user-readable messages (FR-020)

### consent-callback
- [ ] AC-001: State mismatch → SecurityError; denial → AccessDenied; missing code → Error (FR-021)
- [ ] AC-002: An Awaiting poll still completes sign-in (FR-022)

### consent-detail
- [ ] AC-001: ExecuteRevoke unreachable without ConfirmRevoke; success emits LoggedOut (FR-025)

### send-money
- [ ] AC-001: Review unreachable until the payer question is answered (FR-027)
- [ ] AC-002: Switching rail clears the payee but keeps the amount (FR-028)
- [ ] AC-003: Domestic draft carries a reference and no international fields (FR-028)
- [ ] AC-004: Invalid IBAN refused; spaces and lower case accepted (FR-027)
- [ ] AC-005: Staging mints two distinct idempotency keys (FR-029)

### payments-schedule-payment
- [ ] AC-001: Today and day 366 not selectable; international weekdays only (FR-032)

### payments-standing-order
- [ ] AC-001: First date ≥ day after tomorrow; final after first (FR-033)

### payment-consent
- [ ] AC-001: Scheduled and standing-order payments never confirm funds (FR-034)
- [ ] AC-002: Consumed consent → AlreadySubmitted; Rejected → Declined (FR-034)

### payment-status
- [ ] AC-001: Refresh keeps current status and updates last-checked; Rejected is terminal (FR-036)

### settings
- [ ] AC-001: Exactly one write per theme selection (FR-037)
- [ ] AC-002: Sign-out row clears tokens + history (FR-046 — gap)

### consent-relay
- [ ] AC-001: Fragment read first, query fallback; empty → "Nothing to return" (FR-050)
- [ ] AC-002: Desktop loopback probed first; mobile hand-off only when no listener answers (FR-050)
- [ ] AC-003: Fragment scrubbed from history; no-store, no-referrer, frame-ancestors 'none', strict CSP, no inline script (FR-051, NFR-011)
- [ ] AC-004: App Links + Universal Links served from /.well-known on the relay domain (FR-052)
Test: Playwright + node --test (tests.yaml); Maestro not applicable (web page)

### vrp
- [ ] AC-001: Card and bank-refused accounts not offered as payers (FR-041)
- [ ] AC-002: Per-payment ceiling below periodic; end date ≥ today+2 UTC (FR-041)
- [ ] AC-003: Amount over per-payment ceiling or remaining allowance refused (FR-045)
- [ ] AC-004: Revoked, unapproved or card-payer consents cannot be paid under (FR-045)

---

*Managed by `/idea`. Bridge between requirements and implementation.*
*Each feature maps to: requirements (FR/SFR/DR) → flow (.mmd) → SPEC.md → source code → tests*
