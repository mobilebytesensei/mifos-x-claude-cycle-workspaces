# Features — Mifos X Open Banking

All features and their HSBC UK Open Banking (OBIE v4.0) integration points.

**This is a consumer-only app.** There is a single consumer persona and no product
flavors. The field-officer / agent-banking persona was removed on 2026-08-02.

Updated 2026-08-02 — removed the field-officer persona (12 screens) plus pfm-dashboard,
pfm-settings and business-insights. `atm-locator` is retained as specified-but-unbuilt work.
Updated 2026-08-06 — **rewritten off Open Bank Project onto OBIE v4.0**, and payments rewritten
from one type to seven. Every endpoint in this file previously pointed at
`apisandbox.openbankproject.com`; none of them described what the app does.
Updated 2026-08-07 — `branch-locator` added (HSBC UK Branch Locator, Open Data) and `products`
restored to its catalogue meaning (HSBC UK Product Finder, Open Data, four families).
Also 2026-08-07 — **`cards` and `card-detail` deleted** (44 → 42 screens). See "Removed
2026-08-07" below.

Paths below are relative to `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking`, **except**
the Open Data features, which are absolute on `api.hsbc.com` and carry no auth at all.

---

## Core Banking

| Feature | Screen | OBIE Endpoint | Description |
|---|---|---|---|
| **splash** | Splash | — | App startup animation, branding |
| **consent-onboarding** | User Onboarding, Login, Consent Callback | `POST /v4.0/aisp/account-access-consents` → `GET /v1.1/oauth2/authorize` → `POST /v1.1/oauth2/token` | FAPI consent journey. **No credential fields** — the PSU authenticates at HSBC. |
| **home** | Home | accounts + balances + transactions | Selected-account overview, quick actions, spending snapshot |
| **accounts** | Accounts, Account Detail | `GET /v4.0/aisp/accounts`, `/{AccountId}` | List and view account details |
| **balances** | *(within accounts)* | `GET /v4.0/aisp/accounts/{AccountId}/balances` | Current and available balances |
| **account-holder** | Account Holder | `GET /v4.0/aisp/accounts/{AccountId}/party` | Account holder detail, gated by `ReadParty` |
| **transactions** | Transactions, Transaction Detail | `GET /v4.0/aisp/accounts/{AccountId}/transactions` | History with date and credit/debit filters |
| **statements** | Statements, Statement Detail | `GET /v4.0/aisp/accounts/{AccountId}/statements` | Periodic statements. **Credit card only** — 400 on every other account. |

## Payments — initiation (PISP)

Seven types, reached from a grid hub. Each has its own wire contract; see the per-type
`screens/*/api.yaml` for the measured field rules.

| Feature | Screen | OBIE Endpoint | Description |
|---|---|---|---|
| **payments** | Payments | — | Hub. Grid of seven square payment-type tiles. Navigation only. |
| **pay-domestic-single** | Pay someone | `POST /v4.0/pisp/domestic-payments` | Pay a person now. Funds-confirmation GET. Charge 0.05 GBP. |
| **pay-domestic-scheduled** | Pay on a date | `POST /v4.0/pisp/domestic-scheduled-payments` | One payment, T+1 to T+365. No funds check. |
| **pay-domestic-standing-order** | Standing order | `POST /v4.0/pisp/domestic-standing-orders` | Recurring mandate. `FirstPaymentAmount`. No debtor field. |
| **pay-international-single** | Pay abroad | `POST /v4.0/pisp/international-payments` | IBAN creditor. **No charge at any stage.** |
| **pay-international-scheduled** | Pay abroad on a date | `POST /v4.0/pisp/international-scheduled-payments` | Charge 0.50 at resource creation. Never emits `PDNG`. |
| **pay-international-standing-order** | Overseas standing order | `POST /v4.0/pisp/international-standing-orders` | `InstructedAmount` — the inverse of the domestic mandate. |
| **pay-vrp-mandate** | Variable payments | `POST /v4.0/pisp/domestic-vrps` + `DELETE …-consents/{id}` | Create once, pay many with no re-auth, revoke. The only DELETE. |
| **payment-consent** | Payment Consent | family consent-status GET | Authorise return leg, **shared by all seven** |
| **payment-status** | Payment Status | family resource-status GET | Settlement tracker, **shared by all seven** |
| **events** | *(headless)* | `POST /v4.0/event-subscriptions`, `POST /v4.0/events` | Surfaces out-of-band consent revocation |

## Payments — read surfaces (AIS, read-only)

| Feature | Screen | OBIE Endpoint | Description |
|---|---|---|---|
| **beneficiaries** | Beneficiaries | `GET /v4.0/aisp/accounts/{AccountId}/beneficiaries` | Saved payees. Read-only — OBIE has no write side. |
| **standing-orders** | Standing Orders, Detail | `GET /v4.0/aisp/accounts/{AccountId}/standing-orders` | Existing mandates. **Read-only by regulation** — a PISP may not amend or cancel. |
| **scheduled-payments** | Scheduled Payments | `GET /v4.0/aisp/accounts/{AccountId}/scheduled-payments` | Future-dated instructions. Read-only by regulation. |
| **direct-debits** | Direct Debits, Detail | `GET /v4.0/aisp/accounts/{AccountId}/direct-debits` | Mandates. Read-only — OBIE has no cancellation. |

## Consent

| Feature | Screen | OBIE Endpoint | Description |
|---|---|---|---|
| **consent-dashboard** | Consent List, Detail, Manager | `GET`/`DELETE /v4.0/aisp/account-access-consents/{ConsentId}` | Active consents, revoke, 90-day reconfirm |

## Utilities

Open Data features sit on a **third host, `api.hsbc.com`** — unauthenticated, no mTLS, no consent,
outside the OBIE base path above. Every feed is live-only and unpaged.

| Feature | Screen | Endpoint | Description |
|---|---|---|---|
| **atm-locator** | ATM Finder | `GET api.hsbc.com/open-banking/v2.2/atms` + geo-location / postcode / country lookups — unauthenticated | Map-based ATM finder — **specified, not yet built** |
| **branch-locator** | Branch Locator | `GET api.hsbc.com/open-banking/v2.2/branches`, `…/x-open-banking/v2.2/branches/geo-location/lat/{lat}/long/{long}`, `…/branches/sortcode/{sortcode}` — unauthenticated | HSBC UK Branch Locator. The sort-code lookup is the one Open Data path keyed on a banking identifier, so it can name the branch behind a beneficiary, standing order or transaction. **Added 2026-08-07; specified, not yet built** |
| **products** | Products | `GET api.hsbc.com/open-banking/v2.2/{personal-current-accounts, business-current-accounts, unsecured-sme-loans, commercial-credit-cards}` — unauthenticated | HSBC UK **Product Finder** catalogue, all four families. `unsecured-sme-loans` returns 200 with an empty array — HSBC publishes none — so that family's tab is hidden at runtime rather than hardcoded away. **Catalogue meaning restored 2026-08-07** |
| **product** | Product | `GET /v4.0/aisp/accounts/{AccountId}/product` | Per-account product terms. A **different resource on a different host** from the catalogue above — do not merge the two. 400 on Global Money. |
| **notifications** | Notifications | Firebase Cloud Messaging | Transaction alerts |

## App Shell & Legal

| Feature | Screen | OBIE Endpoint | Description |
|---|---|---|---|
| **profile** | Profile | — *(no data source)* | ⚠ **Orphaned, decision owed.** OBIE has no user resource, so this screen has no backing endpoint. The nearest concept is the account holder — read-only, `GET /v4.0/aisp/accounts/{AccountId}/party` — and it is already shipped as `account-holder`. `screens/profile/api.yaml` carries `status: orphaned-pending-decision`; resolve to a fold-into-`account-holder` or a delete before it is exported again. |
| **settings** | Settings, More | — | App theme, manage consents, about & legal |
| **legal** | About, Terms, Privacy, Licences | — | App identity, build provenance, legal links |

## Removed 2026-08-06

| Feature | Why |
|---|---|
| **sca-challenge** | HSBC performs SCA in its own browser. There is no in-app challenge step. |
| **auth-recovery** (forgot / change password) | There is no in-app password under FAPI. |
| **transaction-tags** | OBP v1.2.1 metadata API. No OBIE counterpart. |
| **standing-order-edit** | **A PISP may not amend or cancel a standing order.** OBL Customer Experience Guidelines make redirecting the PSU to their bank a mandatory obligation, not a courtesy. `standing-order-detail` carries the notice instead. |
| **send-money** (+ amount, confirm, result) | Superseded by the seven per-type payment screens. |
| **standing-order-create** | Superseded. Creating a standing order is a PISP action and lives in `pay-domestic-standing-order`. |
| **fx-rates** | **OBIE has no FX rate endpoint and no currency catalogue.** The screen had no data source at all — not a stale one, an absent one. No observed response on any international payment family carries a rate, which is why all three international screens state that the bank sets the final converted amount instead of showing one. |

## Removed 2026-08-07

| Feature | Why |
|---|---|
| **cards** (+ **card-detail**) | **OBIE has no card resource.** A card is an `Account` whose `Account[].SchemeName` is `UK.OBIE.PAN` — there is no card entity to model and no card endpoint to call. The `Card` and `CardAccountRef` DTOs were already deleted on 2026-08-06 for exactly this reason; the screens were spared then on the argument that filtering the accounts list to PAN entries is a legitimate surface. **That argument is overruled by the repository owner: the feature came from the OLD OBP PLANNING and goes with it.** The reprieve also never held up — `card-detail/ui.yaml` still shipped a freeze/unfreeze toggle and Spending Limits sections while carrying its own comment that "OBIE HAS NO CARD WRITE OF ANY KIND" twenty lines below the toggle. Its central interactions were impossible against this API by its own admission (the open `CARD-WRITE-UNBACKED` gap). |

> Not affected: `dtos/CccProduct.yaml` — **commercial credit cards from the Open Data Product
> Finder**, a different resource on a different host with no auth, part of the live `products`
> catalogue restored the same day. Nor the `UK.OBIE.PAN` debtor-eligibility rules under payments,
> which are about which account may fund a payment, not about these screens. `statements` remains
> credit-card-only (400 on every other account) — the account that happens to be a card is
> unaffected; only the card **screens** are gone.

---

## Complete Screen List (42 screens)

> Updated 2026-08-02 — 62 → 47 after the field-officer + PFM removal.
> Rewritten 2026-08-07 — the list still enumerated the eleven screens deleted on 2026-08-06
> (`transaction-tags`, `sca-challenge`, `forgot-password`, `change-password`,
> `standing-order-create`, `standing-order-edit`, the `send-money` set, `payment-result`,
> `fx-rates`) and none of the ten added, so it described an app that no longer exists. Four of
> those eleven were OBP-auth-model screens with no OBIE counterpart.
> Also 2026-08-07 — `branch-locator` added, and `cards` + `card-detail` deleted (44 → 42).
> The Cards section that stood between "Payments — read surfaces" and "Consent" is gone with them.
>
> The authoritative roster is `idea-layer/screens/_list.json`; this list mirrors it.

### Core banking (8)

1. **home**
2. **accounts**
3. **account-detail**
4. **account-holder**
5. **transactions**
6. **transaction-detail**
7. **statements**
8. **statement-detail**

### Payments — initiation (10)

1. **payments** — the grid hub
2. **pay-domestic-single**
3. **pay-domestic-scheduled**
4. **pay-domestic-standing-order**
5. **pay-international-single**
6. **pay-international-scheduled**
7. **pay-international-standing-order**
8. **pay-vrp-mandate**
9. **payment-consent** — shared by all seven
10. **payment-status** — shared by all seven

### Payments — read surfaces (6)

1. **beneficiaries**
2. **standing-orders**
3. **standing-order-detail**
4. **scheduled-payments**
5. **direct-debits**
6. **direct-debit-detail**

### Consent (4)

1. **consent-callback**
2. **consent-list**
3. **consent-detail**
4. **consent-manager**

### Utilities (5)

1. **atm-locator** — Open Data; specified, not yet built
2. **branch-locator** — Open Data; added 2026-08-07, specified, not yet built
3. **notifications**
4. **products** — Open Data Product Finder catalogue
5. **product** — per-account product terms (AIS)

### App shell & legal (9)

1. **splash**
2. **user-onboarding**
3. **login**
4. **profile** — orphaned, decision owed
5. **settings**
6. **about**
7. **terms-of-service**
8. **privacy-policy**
9. **licences**

> **Resolved 2026-08-03.** `licenses` and `licences` were the same screen under two spellings;
> they were merged into `licences`, the British slug that matches the shipped `LicencesRoute`
> in `feature/settings`. The deleted `licenses` was a legacy v3.1 monolith backed only by a
> `PlaceholderScreen`; `licences` is v4.0, source-mapped and carries the live i18n keys.
>
> `product` and `products` are **not** duplicates and both remain: `product` is the
> per-account product-terms screen (shipped — `ProductRoute(accountId)` in `feature/product`),
> `products` is the product catalogue (specified; `ProductsRoute` is still a placeholder).
>
> **Restored 2026-08-07.** `products` is the HSBC UK **Product Finder** — Open Data on
> `api.hsbc.com`, unauthenticated, four families. It answers "what could I open?"; `product`
> answers "what are the terms of the account I already hold?". Different question, different
> host, different auth model. They must not be merged.

---

## Feature Quality Baseline

All features start at quality score **50/100** (scaffold). Progression:

- **≥50:** Scaffolded (template-generated)
- **≥70:** Enriched (design tokens, state models, navigation edges)
- **≥85:** Fully specced (SPEC.md, API contract, mockups)
- **≥95:** Implemented (Kotlin code, tests passing)

---

## OBIE API Coverage

Rewritten 2026-08-06. The previous table counted Open Bank Project tags (89 Accounts endpoints,
39 Counterparties, 14 TransactionRequests) that this app never called.

### AIS — `/v4.0/aisp`

| Resource | In use | Availability caveat |
|---|---|---|
| `account-access-consents` (POST/GET/DELETE) | ✓ | Rejects `x-jws-signature` |
| `accounts`, `/{AccountId}` | ✓ | — |
| `balances` | ✓ | — |
| `transactions` | ✓ | ⚠ returns the card PAN **unmasked** |
| `beneficiaries` | ✓ | 400 on the credit card |
| `standing-orders` | ✓ | 400 on savings, Global Money, card. No `StandingOrderId`. |
| `scheduled-payments` | ✓ | 400 on Global Money and the card |
| `direct-debits` | ✓ | 400 on savings, Global Money, card |
| `statements` (+ detail, transactions, file) | ✓ | **400 on everything except the card** |
| `product` | ✓ | 400 on Global Money |
| `party` / `parties` | ✓ | `party` 400 on Global Money |

Five of these — `beneficiaries`, `standing-orders`, `scheduled-payments`, `direct-debits` and
`party` — return **403 with an empty body** when the token's SCA is stale, while `balances` and
`transactions` keep working. That is the PSD2 RTS Article 10 boundary, and there is no error
code to key on.

### PIS — `/v4.0/pisp` · 32 endpoints across 7 families

| Family | Consent POST | Consent GET | Funds conf. | Resource POST | Resource GET | DELETE |
|---|---|---|---|---|---|---|
| Domestic payment | ✓ | ✓ | GET | ✓ | ✓ | — |
| Domestic scheduled | ✓ | ✓ | — | ✓ | ✓ | — |
| Domestic standing order | ✓ | ✓ | — | ✓ | ✓ | — |
| International payment | ✓ | ✓ | GET | ✓ | ✓ | — |
| International scheduled | ✓ | ✓ | — | ✓ | ✓ | — |
| International standing order | ✓ | ✓ | — | ✓ | ✓ | — |
| Domestic VRP | ✓ | ✓ | **POST** | ✓ | ✓ | **✓** |

### Other

| Surface | In use |
|---|---|
| `/v1.1/oauth2/{token,authorize}` + `/register` | ✓ |
| `/v4.0/event-subscriptions`, `/v4.0/events` | ✓ (P5) |
| HSBC Open Data (`api.hsbc.com`) — ATMs, branches, Product Finder | planned |
| `/v4.0/cbpii/*` — Confirmation of Funds | ✗ out of scope |
| File payments, multi-bill payments | ✗ not offered for this brand |

---

## Notes

- **Single consumer persona** — no KMP product flavors, no flavor-aware navigation
- **FAPI 1.0 Advanced** is the sole authentication model: mTLS, `private_key_jwt`, signed request
  object, PKCE S256, app-to-app redirect. **The app has no password field.**
- **Every PISP write** carries a detached JWS (`PS256`, `b64:false`) and an idempotency key
- **Shared layers:** DTOs, domain models, API client, local storage schema — all KMP
- **State management:** Store5 repositories + ViewModels per feature
