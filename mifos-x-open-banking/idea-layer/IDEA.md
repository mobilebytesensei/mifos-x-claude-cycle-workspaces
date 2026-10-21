# Mifos-X Open Banking — Consumer KMP Application

**Vision:** Build a Kotlin Multiplatform (KMP) UK Open Banking reference client — an AISP and PISP built to the OBIE Read/Write API Specification v4.0 against the HSBC UK sandbox — running from a single codebase on Android, iOS, desktop and web.

> **Scope change 2026-08-02.** This was previously a dual-persona app (Consumer + Field
> Officer) built on KMP Product Flavors. The field-officer persona was removed in full, along
> with PFM. There is now **one persona and no product flavors**.

---

## Product Overview

### Persona

**Consumer (Alex)**
- Age: 28, Tech-savvy retail customer
- Needs: Self-service account management, fast payments, expense tracking, consent control
- Motivation: Convenience, security, control over finances
- Primary flows: View accounts → Check balance → Send money → Manage consents

### Brand Identity

| Attribute | Value |
|---|---|
| Primary Color | Sage Green `#4C662B` |
| Secondary Color | Muted Teal `#386663` |
| Error / Debit | Red `#BA1A1A` |
| Font Family | Outfit (all surfaces) |
| Tone | Professional, Trustworthy, Efficient |
| Key Message | "Banking for Everyone" |

---

## Architecture

### Tech Stack

| Layer | Tech | Notes |
|---|---|---|
| UI | Compose Multiplatform 1.8.2 | Single KMP UI codebase |
| Networking | Ktor 3.2.0 + Ktorfit 2.5.2 | OBIE v4.0 REST client over mTLS, with detached-JWS signing on PISP writes |
| State Management | Store5 + BaseViewModel + ScreenDataStream | Stream-First reactive architecture |
| Local Storage | Room KMP 2.7.2 | Cross-platform persistence |
| Serialization | Kotlinx Serialization | Type-safe JSON, `@Serializable` routes |
| Dependency Injection | Koin 4.1.0 | Lightweight, multiplatform |
| Navigation | Jetpack Navigation Compose | Type-safe `@Serializable` route objects |
| Build System | Gradle 8.0+ | Standard debug/release build types |

### Product Flavors — removed

The app previously used `io.github.mobilebytelabs.kmp-product-flavors` to gate a `consumer`
and a `fieldOfficer` variant, with `src/commonConsumer/` and `src/commonFieldOfficer/` source
sets wiring separate navigation graphs.

With the field-officer persona removed there is a single variant. Navigation is assembled once
in `cmp-navigation` from `src/commonMain/`; there is no flavor gating, no
`VARIANT_DEPENDENCY_EXCLUDES.yaml`, and no per-flavor source set.

Build: `./gradlew :cmp-android:assembleDebug` / `assembleRelease`.

### Module Structure

Based on **kmp-project-template** conventions (reusing its module layout):

```
cmp-android / cmp-ios / cmp-desktop / cmp-web   ← platform entry points
cmp-navigation                                   ← navigation hub
cmp-shared                                       ← SharedApp() + theme host

core:analytics · core:common · core:data         ← unchanged from template
core:database · core:datastore · core:designsystem
core:domain · core:model · core:network · core:ui

# App shell
feature:splash · feature:login
feature:profile · feature:settings

# Consumer feature modules
feature:home · feature:accounts · feature:account-detail · feature:account-holder
feature:transactions · feature:transaction-detail · feature:statements
feature:payments · feature:beneficiaries
feature:pay-domestic-single · feature:pay-domestic-scheduled
feature:pay-domestic-standing-order · feature:pay-international-single
feature:pay-international-scheduled · feature:pay-international-standing-order
feature:pay-vrp-mandate · feature:payment-consent · feature:payment-status
feature:standing-orders · feature:direct-debits · feature:scheduled-payments
feature:consent-list · feature:consent-detail · feature:consent-callback
feature:product
```

### Navigation Assembly

Navigation is assembled once, in `cmp-navigation/src/commonMain/`:

```kotlin
@Composable
fun App() {
    NavHost(startDestination = SplashRoute) {
        splashGraph()
        loginGraph()
        composable<AuthenticatedNavbarRoute> {
            AuthenticatedNavbarHost {
                homeGraph()
                accountsGraph()
                sendMoneyGraph()
                moreGraph() // profile, settings, standing-orders, ATM
            }
        }
    }
}
```

---

## Backend Integration

### HSBC UK Open Banking — OBIE Read/Write API v4.0

> **Rewritten 2026-08-06.** This section previously described the Open Bank Project sandbox
> (`apisandbox.openbankproject.com`, DirectLogin, `obp-oidc`, counterparties, 118 endpoints
> across 89 tags). The app was rebuilt against HSBC's OBIE surface and this document was never
> migrated with it.

**Resource host (mTLS):** `secure.sandbox.ob.hsbc.co.uk` — all AIS, PIS and events
**Authorize host:** `sandbox.ob.hsbc.co.uk` — **different host**, note the absent `secure.` prefix;
`oauth2/authorize` **only**
**Open Data host:** `api.hsbc.com` — unauthenticated, no mTLS, no consent (ATMs, branches, products)
**Base path:** `/obie/open-banking`
**Resource version:** v4.0 · **OAuth version:** v1.1 · **Brand:** HSBC UK Personal
**Standard:** OBIE Read/Write API Specification v4.0
**Roles:** AISP + PISP (one SSA; there is no separate VRP role)

> The resource and authorize hosts are not interchangeable. The resource host is mTLS-protected; the authorize host
> is where the PSU's browser is sent. Sourced from the shipped Postman environment
> (`bank_sandbox_ob_uk_personal_mtls_hostname` / `…_authorize_hostname`).

### Authentication — FAPI 1.0 Advanced, single method

**There is no in-app password.** The PSU authenticates on HSBC's own site via app-to-app
redirect, and this app receives only a scoped token. That single fact removes an entire class of
screens — there is no login form, no forgot-password and no change-password, and all three were
deleted from the idea-layer on 2026-08-06.

- **Transport:** mutual TLS (mTLS) with an HSBC-issued sandbox client certificate
- **Client auth:** `private_key_jwt` signed PS256 — not a client secret
- **Authorization:** `authorization_code` with a signed request object and PKCE S256
- **Endpoints:** `POST /v1.1/oauth2/token` · `GET /v1.1/oauth2/authorize`
- **Registration:** `POST /register` — DCR v3.2.1 with a signed SSA
- **Scopes:** `accounts`, `payments` (VRP rides `payments`; there is no VRP scope)
- **Redirect URI:** `https://thekalpeshpawar.github.io/obp-callback/callback/` — an HTTPS
  callback page, not a custom scheme. Corrected 2026-08-06 from the invented
  `org.mifosx.openbanking://oauth/callback`; the real value is in the Postman environment
  (`bank_sandbox_ob_authorize_callbackURL`) and must match what is registered at the bank.

**PISP writes carry two extra headers:**
- `x-jws-signature` — detached JWS, PS256, `b64:false`, `crit:[iat,iss,tan]`. Omitting it
  returns `400 U019`. **Sending it on an AIS consent is rejected** — PISP writes only.
- `x-idempotency-key` — max 40 chars, generated once per staged payment and reused across the
  consent stage, the submit, and every retry.

### API surface

**AIS (`/v4.0/aisp`)** — accounts, balances, transactions, beneficiaries, standing orders,
scheduled payments, direct debits, statements, product, party/parties, and the
account-access-consent lifecycle (create, status, revoke, 90-day reconfirmation).

**PIS (`/v4.0/pisp`)** — **32 endpoints across seven payment families**, each with a consent
POST, a consent-status GET, a resource POST and a resource-status GET:

| Family | Funds conf. | Delete | Resource id |
|---|---|---|---|
| Domestic payment | GET | — | `DomesticPaymentId` |
| Domestic scheduled payment | — | — | `DomesticScheduledPaymentId` |
| Domestic standing order | — | — | `DomesticStandingOrderId` |
| International payment | GET | — | `InternationalPaymentId` |
| International scheduled payment | — | — | `InternationalScheduledPaymentId` |
| International standing order | — | — | `InternationalStandingOrderId` |
| Domestic VRP | **POST** | **✓ 204** | `DomesticVRPId` |

**Events (`/v4.0`)** — `event-subscriptions` (POST/GET/DELETE) and `events` (POST poll), for
`UK.OBIE.Consent-Authorization-Revoked`. The only way to learn a consent was revoked
out-of-band.

**Open Data (`api.hsbc.com`)** — a **third host**, unauthenticated and outside the consent
surface entirely: no mTLS, no token, no PSU. Three feeds are in scope —
`/open-banking/v2.2/atms`, `/open-banking/v2.2/branches` (+ geo-location and sort-code lookups),
and the Product Finder's four family endpoints (`personal-current-accounts`,
`business-current-accounts`, `unsecured-sme-loans`, `commercial-credit-cards`). All are live-only
and unpaged.

**Credential Storage:**
- Signing and transport certificates: vault-managed, never in source or the binary
- Access and refresh tokens: encrypted on-device store, cleared on logout or revocation
- Payments-scope tokens are **never** written into the AIS `ConsentSession`

---

## Core Models

### Domain Objects (Shared)

```yaml
# idea-layer/dtos/Account.yaml
Account:
  id: String                              # AccountId
  label: String                           # display label / nickname
  account_type: String                    # CURRENT, SAVINGS
  balance: MoneyAmount                    # { amount, currency }
  account_routings: List<AccountRouting>  # UK.OBIE.SortCodeAccountNumber · UK.OBIE.IBAN · UK.OBIE.PAN
```

> **Rewritten 2026-08-07** to match `dtos/Account.yaml` — this block was missed by the
> 2026-08-06 OBP eviction that rewrote the Backend Integration section above. The previous shape
> was the Open Bank
> Project one: a flat `iban`/`swift` pair rather than the `Account[]` identification
> array OBIE actually returns, a `branchId` (there is one bank and no `bankId`/`branchId`
> concept under OBIE), and `owners: List<User>` — **OBIE has no user resource.** The nearest
> concept is the account holder, read from `/aisp/accounts/{AccountId}/party`, which is why
> `account-holder` exists as its own screen.
>
> `AccountType` and `AccountSubType` are absent from every account record in the sandbox despite
> the published profile table listing sub-types, so `account_type` is populated defensively.

```yaml
# idea-layer/dtos/Transaction.yaml
Transaction:
  TransactionId: String
  AccountId: String
  CreditDebitIndicator: Credit | Debit
  Amount: { Amount: String, Currency: String }
  BookingDateTime: Instant
  ValueDateTime: Instant
  TransactionInformation: String
  # OBIE names the other party by direction, not as a "counterparty" resource.
  CreditorAccount: { SchemeName, Identification, Name }
  DebtorAccount: { SchemeName, Identification, Name }
  Status: Booked | Pending
```

> ⚠ **Unmasked PAN.** The transactions resource returns the credit card number in full —
> `"SchemeName":"UK.OBIE.PAN","Identification":"1234567890123456"` — while the `account`
> resource masks it to `xxxx-xxxx-xxxx-3456`. Anything that logs, caches or exports transaction
> records is handling a full PAN.

> The `Customer` DTO was deleted on 2026-08-02 — its only consumers were `customer-search`
> and `fo-dashboard`, both removed with the field-officer persona.

---

## Feature Roadmap

> Rewritten 2026-08-06. The previous roadmap described DirectLogin auth, SEPA/ACH routing and
> counterparty management — none of which exists. Phases here mirror
> `idea-plan.yaml#release_phases`.

### P0–P2 — AISP (implemented)

1. **Consent journey** — staging, app-to-app authorisation, code exchange, 90-day reconfirm
2. **Home** — selected-account hero balance, quick actions, recent transactions
3. **Accounts** — list, detail, balances
4. **Transactions** — history with date and credit/debit filters, detail
5. **Payment-context reads** — beneficiaries, standing orders, scheduled payments, direct debits
6. **Statements, product, account holder, settings, licences**

### P3 — PISP: payments hub + the three domestic rails *(planned)*

1. **Payments hub** — a grid of seven square payment-type tiles, replacing the Pay tab placeholder
2. **Domestic single** — pay a person now; the reference rail
3. **Domestic scheduled** — one payment on a future date (T+1 to T+365)
4. **Domestic standing order** — a recurring mandate
5. **Shared surfaces** — `payment-consent` (authorise return leg) and `payment-status` (tracker)

Gated on cross-cutting prerequisites paid once for all seven types: a `Pisp.kt` Ktorfit client,
the detached-JWS signer, idempotency-key handling, a payments-scope token path, a scheme-based
debtor-eligibility filter, and a status mapper covering four ladders and two encodings.

### P4 — PISP: the three international rails *(planned)*

IBAN creditors, mandatory `CurrencyOfTransfer` and `ChargeBearer`, forbidden
`RemittanceInformation`, 11-character BICs. Separated from P3 because these add a distinct field
contract on top of plumbing that must already work.

### P5 — VRP mandates + event notification *(planned)*

Create a mandate once, pay under it many times with no re-authentication, revoke via DELETE.
Last because VRP inverts nearly every assumption the other six share.

### Unscheduled

- **ATM locator** — HSBC Open Data, unauthenticated *(specified, not built)*
- **Branch locator** — HSBC UK Branch Locator, Open Data *(added 2026-08-07; specified, not built)*
- **Products** — HSBC UK Product Finder catalogue, Open Data, four families
  (personal-current-accounts, business-current-accounts, unsecured-sme-loans,
  commercial-credit-cards) *(catalogue meaning restored 2026-08-07; specified, not built)*
- **Notifications** — present in the idea-layer, backed by Firebase rather than OBIE

---

## Screen Inventory (42 screens)

The authoritative roster is `idea-layer/screens/_list.json`. Headline surfaces:

| Screen | Purpose | OBIE resource |
|---|---|---|
| Splash | App startup | — |
| Login | Starts the FAPI consent journey — **no credential fields** | `oauth2/authorize` |
| Consent Callback | AIS authorise return leg | `oauth2/token` |
| Home | Selected-account overview | accounts, balances, transactions |
| Accounts / Account Detail | Account list and detail | `aisp/accounts` |
| Transactions / Detail | Transaction history | `aisp/…/transactions` |
| Beneficiaries | Read-only saved payees | `aisp/…/beneficiaries` |
| Standing Orders / Detail | Existing mandates, read-only | `aisp/…/standing-orders` |
| Scheduled Payments | Future-dated instructions, read-only | `aisp/…/scheduled-payments` |
| Direct Debits / Detail | Mandates, read-only | `aisp/…/direct-debits` |
| Statements / Detail | Statements *(credit card only)* | `aisp/…/statements` |
| Consent List / Detail / Manager | Consent lifecycle | `aisp/account-access-consents` |
| **Payments** | **Grid of seven payment-type tiles** | — *(navigation only)* |
| **Pay Domestic Single** | Pay a person now | `pisp/domestic-payments` |
| **Pay Domestic Scheduled** | One payment on a future date | `pisp/domestic-scheduled-payments` |
| **Pay Domestic Standing Order** | A recurring mandate | `pisp/domestic-standing-orders` |
| **Pay International Single** | Pay abroad now | `pisp/international-payments` |
| **Pay International Scheduled** | Pay abroad on a date | `pisp/international-scheduled-payments` |
| **Pay International Standing Order** | A recurring overseas mandate | `pisp/international-standing-orders` |
| **Pay VRP Mandate** | Create once, pay many, revoke | `pisp/domestic-vrps` |
| Payment Consent | PISP authorise return leg — **all seven families** | family consent-status GET |
| Payment Status | Settlement tracker — **all seven families** | family resource-status GET |
| ATM Finder | ATM map *(not yet built)* | Open Data — `/atms` |
| **Branch Locator** | Branch map + sort-code lookup *(new 2026-08-07)* | Open Data — `/branches` |
| **Products** | HSBC UK Product Finder catalogue, four families | Open Data — four family feeds |
| Product | Per-account product terms | `aisp/…/product` |
| Settings / Licences / About | Preferences, legal | — |

**Removed 2026-08-06** — screens that cannot exist under OBIE FAPI, or that a PISP is not
permitted to offer:

| Removed | Why |
|---|---|
| SCA Challenge | HSBC performs SCA in its own browser. There is no in-app challenge step. |
| Change Password | There is no in-app password. |
| Forgot Password | There is no in-app password. |
| Transaction Tags | OBP v1.2.1 metadata API. No OBIE counterpart. |
| Standing Order Edit | **A PISP may not amend or cancel a standing order** — OBL Customer Experience Guidelines make redirecting the PSU to their bank a mandatory obligation. |
| Send Money / Amount / Confirm / Result | Superseded by the seven per-type screens. |

**Removed 2026-08-07** — decided by the repository owner:

| Removed | Why |
|---|---|
| Cards / Card Detail | **OBIE has no card resource.** A card is an `Account` whose `SchemeName` is `UK.OBIE.PAN`, so there is nothing to model and no endpoint to call. The `Card` and `CardAccountRef` DTOs went on 2026-08-06 for this reason; the screens were spared then and are now removed with the rest of the OBP planning they came from. `card-detail` had shipped a freeze/unfreeze toggle and Spending Limits sections alongside its own note that "OBIE has no card write of any kind" — its central interactions were unbuildable. Unaffected: the Product Finder's **commercial credit cards** family (Open Data, different host, no auth), and `statements`, which remains credit-card-only. |

---

## Navigation Architecture

```
Splash → Login → [HSBC authorises in browser] → Consent Callback → Home (Bottom Nav)
  ├─ Home → Transaction Detail / Transactions
  ├─ Accounts → Account Detail → Transactions / Statements / Standing Orders /
  │                              Scheduled Payments / Direct Debits / ATM
  ├─ Pay → PAYMENTS HUB (7 square tiles)
  │        ├─ Domestic single ─────────────┐
  │        ├─ Domestic scheduled ──────────┤
  │        ├─ Domestic standing order ─────┤
  │        ├─ International single ────────┼→ Payment Consent → Payment Status
  │        ├─ International scheduled ─────┤   (shared by all seven)
  │        ├─ International standing order ┤
  │        └─ VRP mandate → mandate list ──┘
  │             ├─ create → Payment Consent (ONCE per mandate)
  │             ├─ pay under it → Payment Status  [no re-authentication]
  │             └─ revoke → DELETE
  └─ More → Settings / Consents / Licences / About / Logout
```

Two things this diagram encodes that the previous one got wrong:

- **There is no SCA Challenge step.** The PSU authenticates in HSBC's browser, both on the AIS
  journey and on every PISP authorisation.
- **The VRP pay path does not pass through Payment Consent.** One authorisation funds many
  payments — that is the defining property of the rail, and routing every payment through the
  authorise leg would defeat it.

---

## Design System

### Color Tokens

| Token | Value | Usage |
|---|---|---|
| primary | #4C662B | CTAs, active states, FAB |
| on_primary | #FFFFFF | Text on primary surfaces |
| primary_container | #CDEDA3 | Balance cards, highlights |
| secondary | #386663 | Secondary actions |
| error | #BA1A1A | Errors, debit amounts, destructive |
| warning | #E8A317 | Warnings, pending states |
| surface | #FFFFFF | Cards, containers |
| background | #F9FAEF | App background |
| on_background | #1A1C16 | Primary text |
| on_surface_variant | #44483D | Secondary text |

### Typography

| Level | Font | Size | Weight |
|---|---|---|---|
| display-lg | Outfit | 32px | 600 |
| headline-lg | Outfit | 24px | 600 |
| body-lg | Outfit | 16px | 400 |
| body-md | Outfit | 14px | 400 |
| body-sm | Outfit | 12px | 400 |

### Component Library

- Button (contained, outlined, text)
- Text Field (single, multi-line, search)
- Card, Dialog, Sheet
- TopAppBar, BottomNavigation, FAB
- Snackbar, ProgressIndicator, Badge
- List, Grid, Spacer
- Custom: AccountCard, TransactionRow, BeneficiaryItem

---

## Quality Standards

- **Type Safety:** 100% Kotlin, non-null by default
- **Null Safety:** Explicit optionals via `?`
- **Testability:** ViewModel + StateFlow + repository pattern
- **Accessibility:** Material 3 A11y semantics
- **Performance:** <500ms account load, <200ms transaction list
- **Security:** TLS 1.3, HTTPS only, no plaintext storage

---

## Success Metrics

1. **Adoption:** 1000+ active consumer users
2. **Transaction Volume:** 10K+ monthly transactions
3. **NPS:** >50
4. **Uptime:** 99.9% availability
5. **Load Time:** <2s home screen

---

## Timeline

- **M1 (Jan–Mar):** Consumer MVP (Auth, Accounts, Transactions)
- **M2 (Apr–Jun):** Consent journey + recurring payment surfaces
- **M3 (Jul–Sep):** Enhancement (ATM + Branch locators, Standing Orders, Product Finder)
  <!-- Cards dropped from M3 on 2026-08-07 with the cards / card-detail screens. -->

- **M4 (Oct–Dec):** Production hardening, scale testing

---

## Ideas Backlog

| # | Description | Feature | Status |
|---|---|---|---|
