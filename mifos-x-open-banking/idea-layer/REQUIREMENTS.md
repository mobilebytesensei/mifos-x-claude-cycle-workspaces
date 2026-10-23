# Requirements Registry — Mifos X Open Banking

> **Last Updated**: 2026-10-21
> **Single source of truth** for ALL product requirements (mirrors `idea-plan.yaml#requirements`).
> Managed by `/idea`. Read by `/design`, `/server`, `/implement`, `/test`.

---

## Technical Context

| Attribute | Value |
|-----------|-------|
| Architecture | KMP multi-module (cmp-* / feature/* / core/* / core-base/*), MVI, Store5 + Room offline-first |
| Backend Type | None first-party — HSBC UK Open Banking sandbox (OBIE Read/Write v4.0) |
| Base URL | `https://{HSBC_BANK_HOST}/obie/open-banking/` |
| Auth Method | mTLS + `private_key_jwt` (PS256) + OIDC hybrid consent (`code id_token`) |
| Database | Room 3 (local cache) + secure Settings (tokens, PendingAuth) |
| API Docs | HSBC Open Banking DevHub — OBIE Read/Write v4.0 |
| Hosted pieces | Consent relay on Cloudflare Pages (feature `consent-relay`); Worker BFF planned (task `cloudflare-worker-bff`) |

### Key Entities / Data Model

| Entity | Description | Key Fields | Relationships | Storage | CRUD | Feature |
|--------|-------------|-----------|---------------|---------|:----:|---------|
| Account | Connected bank account | accountId, type, nickname, identification, currency | has Balance, Transaction, Statement, Product, Party | OBIE + Room `accounts` | R | home, accounts, account-detail |
| Balance | Account balance | amount, currency, creditDebit, dateTime | belongs to Account | OBIE | R | home, account-detail |
| Transaction | Booked or pending transaction | transactionId, amount, status, bookingDateTime, reference | belongs to Account | OBIE + Room `transactions` | R | transactions, transaction-detail |
| Statement | Monthly statement | statementId, startDate, endDate, closingBalance | has Transaction | OBIE | R | statements, statement-detail |
| StandingOrder | Existing standing order | payee, amount, frequency, nextPaymentDate | belongs to Account | OBIE | R | standing-orders |
| DirectDebit | Direct-debit mandate | name, mandateRef, lastAmount, status | belongs to Account | OBIE | R | direct-debits |
| ScheduledPayment | Future-dated payment | payee, amount, executionDate | belongs to Account | OBIE | R | scheduled-payments |
| Beneficiary | Saved payee | name, scheme, identification | used as payee | OBIE | R | beneficiaries, payment forms |
| Product | Product terms | monthlyFee, overdraftTiers, features | belongs to Account | OBIE | R | product |
| Party | Account holder | name, email, phone, address | belongs to Account | OBIE | R | account-holder |
| AccountAccessConsent | AIS consent | consentId, status, permissions, expiry | authorises AIS reads | OBIE + secure Settings | CRD | login, consent-* |
| PaymentConsent | PIS consent (single / scheduled / SO) | consentId, kind, status, initiation | consumed by Payment | OBIE | CR | payment forms, payment-consent |
| Payment | Submitted payment | paymentId, status, amount, charges | from PaymentConsent | OBIE | CR | payment-consent, payment-status |
| PaymentHistoryEntry | Local history row | product, payee, amount, paymentId, status | references Payment | Room `payment_history` (cap 200) | CRD | payment forms |
| VrpConsent | Sweeping mandate | consentId, maxIndividualAmount, periodicLimits, status | has VrpPayment | OBIE + Room `vrp_consent` | CRD | vrp |
| VrpPayment | Payment under a VRP consent | vrpId, amount, status | belongs to VrpConsent | OBIE + Room `vrp_payment` | CR | vrp |
| PendingAuth | Single-use authorisation context | state, nonce, consentId, leg | one per in-flight authorisation | secure Settings | CRD | login, payment forms, vrp |
| PsuTokens | PSU access/refresh/id tokens | accessToken, refreshToken, expiresAt | per authorised consent | secure Settings | CRUD | consent-callback, vrp |

### Third-Party Services

| Service | Purpose | SDK/Library | Config Keys | Feature | Required |
|---------|---------|-------------|-------------|---------|:--------:|
| HSBC UK Open Banking sandbox | AIS, PIS, VRP | Ktor + Ktorfit, mTLS | HSBC_* (local.properties, vault) | all | ✅ |
| Cloudflare Pages | Consent relay hosting (redirect URI) | static site, `_headers` | Cloudflare account (org) | consent-relay | ✅ |
| Cloudflare Workers | BFF — keys off device (planned) | Worker + mTLS certificate binding | Workers secrets | — (task) | for public release |
| Firebase Analytics + Crashlytics | Telemetry | GitLive 2.4.0 | firebase config | all | ✅ |

---

## Functional Requirements (FR)

> User-facing features — what the user can DO.

| ID | Priority | Requirement | Feature(s) |
|----|:--------:|-------------|-----------|
| FR-001 | must | Home dashboard of accounts and cards with balances | home |
| FR-002 | must | Quick actions from home to send, schedule, standing order, VRP, settings | home |
| FR-003 | should | List all accounts with type filtering | accounts |
| FR-004 | must | Account header and balances for a routed accountId | account-detail |
| FR-005 | must | Explore chips into each AIS resource, hiding unsupported ones | account-detail |
| FR-006 | could | Account-holder identity details | account-holder |
| FR-007 | must | Transactions grouped by date with period totals | transactions |
| FR-008 | must | Filter transactions by direction, search and date range, with clear-all | transactions |
| FR-009 | must | Cursor pagination (Load more) | transactions |
| FR-010 | must | Transaction detail with copy-reference | transaction-detail |
| FR-011 | should | Scheduled payments list with formatted dates | scheduled-payments |
| FR-012 | should | Standing orders and direct-debit mandates, active first | standing-orders, direct-debits |
| FR-013 | should | Unsupported state when the bank returns U000 | scheduled-payments, standing-orders, direct-debits |
| FR-014 | should | Beneficiaries with local search and IBAN grouping | beneficiaries |
| FR-015 | could | Product terms: fees, tiers, features | product |
| FR-016 | should | Statements newest first with closing balance | statements, statement-detail |
| FR-017 | should | Download statement file via the platform save dialog | statements |
| FR-018 | should | Statement detail with PDF download | statement-detail |
| FR-019 | must | Onboarding intro, then the AIS permission list | login |
| FR-020 | must | Start HSBC consent in the system browser, persisting nonce + consentId first | login |
| FR-021 | must | Validate the AIS redirect and exchange for PSU tokens | consent-callback |
| FR-022 | must | Persist consent id + expiry, poll status, navigate home on success | consent-callback |
| FR-023 | must | Current consent card with status, permission count, expiry banner | consent-list |
| FR-024 | must | Renew / reconfirm consent via LoginRenew | login, consent-list, consent-detail |
| FR-025 | must | Revoke consent behind a confirmation gate, then log out | consent-detail |
| FR-026 | should | Payments hub listing payment products | payments-hub |
| FR-027 | must | Payer account or bank-chosen; saved or manual payee | send-money, schedule, standing order |
| FR-028 | must | Domestic (GBP) and International rails with currency + charge bearer | send-money, schedule, standing order |
| FR-029 | must | Validate, review, stage consent, launch bank authorisation | send-money, schedule, standing order |
| FR-030 | must | Classify staging failures into actionable kinds with a support reference | send-money |
| FR-031 | should | Local payment history per product (cap 200, cleared at logout) | send-money, schedule, standing order |
| FR-032 | must | Schedule within 365 days (international weekdays only) | payments-schedule-payment |
| FR-033 | must | Standing order with frequency and first/recurring/final amounts and dates | payments-standing-order |
| FR-034 | must | PIS redirect: exchange, check consent, confirm funds (immediate only), submit | payment-consent |
| FR-035 | must | CheckAgain / RetryAuthorisation / AbandonPayment on payment-consent errors | payment-consent |
| FR-036 | must | Payment receipt and status timeline with manual refresh | payment-status |
| FR-037 | should | Theme choice (system/light/dark), persisted | settings |
| FR-038 | should | Open-source licences + links to consents and privacy policy | settings |
| FR-039 | should | Offline snackbar in the authenticated shell | home |
| FR-040 | must | Uniform AIS error classification (401 / 403 / 429 / network) | all AIS features |
| FR-041 | should | VRP consent setup with per-payment + periodic ceilings | vrp |
| FR-042 | should | Stage VRP consent and launch bank authorisation | vrp |
| FR-043 | should | VRP redirect: validate, exchange, read consent back | vrp |
| FR-044 | should | List/view VRP consents with limits, usage, history, revoke | vrp |
| FR-045 | should | Pay under a VRP consent within the remaining allowance | vrp |
| FR-046 | should | Sign out from Settings | settings |
| FR-047 | should | "Manage consents" from payment flows opens ConsentList | send-money, schedule, standing order |
| FR-048 | should | Accounts and Payments Hub reachable from the shell | home, accounts, payments-hub |
| FR-049 | must | 401 / 403 on AIS screens route to LoginRenew / Consents, never a dead-end Retry | all AIS features, payment-status |
| FR-050 | must | Consent relay reads the bank response and delivers it to desktop loopback or the mobile app | consent-relay |
| FR-051 | must | Consent relay leaves no authorisation code behind (history scrub, no-store, no-frame, no-referrer) | consent-relay |
| FR-052 | should | Redirect opens only the verified app (App Links / Universal Links) | consent-relay |
| FR-053 | must | The TPP identity (signing key, mTLS cert + key, client id, kid, software statement, signing issuer) is held only by the Cloudflare Worker BFF — no app build carries it | all (core/network, BFF) |
| FR-054 | must | The BFF verifies the id_token (PS256 signature vs HSBC JWKS, iss, aud, exp, nonce, c_hash, s_hash) before exchanging the authorisation code | consent-callback, payment-consent, vrp |
| FR-055 | must | Android (Play Integrity) and iOS (App Attest) attest consent creation and /v1/auth/complete; desktop and web use sessions + rate limits | login, consent-callback, payments, vrp |

Acceptance criteria per FR: `idea-plan.yaml#requirements.functional_requirements[]`.

---

## Non-Functional Requirements (NFR)

| ID | Category | Requirement |
|----|----------|-------------|
| NFR-001 | security | mTLS on every bank call; certs + keys never committed; secrets via vault → local.properties |
| NFR-002 | security | Single-use PendingAuth (state/nonce); redirect dedupe |
| NFR-003 | reliability | Idempotent payment writes (x-idempotency-key ≤ 40) |
| NFR-004 | offline | Cached Room data shown offline via Store5 |
| NFR-005 | quality | Kover coverage floor enforced in CI |
| NFR-006 | security | FAPI 1.0 Advanced: revocation confirmed at the ASPSP before local logout; PS256 everywhere |
| NFR-007 | security | No secrets, keystore passwords or certificates in the repository |
| NFR-008 | i18n | All strings in strings.xml; 20 tier-1 locales |
| NFR-009 | accessibility | WCAG 2.1 AA |
| NFR-010 | security | TPP private keys never ship inside an app build for a production / public release — they live in the Cloudflare Worker BFF |
| NFR-011 | security | Consent relay open source under openMF, org-controlled Cloudflare account, strict security headers, zero third-party script |
| NFR-012 | performance | Every BFF route's p99 cpuTime stays under 10 ms on Workers Free (measured on the deployed Worker; Paid is the documented fallback) |
| NFR-013 | security | No HSBC credential or key material in any built APK, IPA, desktop package or web bundle — enforced by the no-tpp-identity CI job |

---

## Source Defects (from source analysis)

DEF-001 … DEF-014 — see `idea-plan.yaml#requirements.source_defects` (each linked to the FR it violates).
