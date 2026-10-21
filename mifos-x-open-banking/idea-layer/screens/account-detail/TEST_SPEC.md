# TEST SPEC — Account Detail

| Field      | Value                                |
|------------|--------------------------------------|
| Feature    | account-detail                       |
| Source     | `screens/account-detail/tests.yaml`  |
| Scenarios  | 20                                   |
| Priorities | critical 5 · high 6 · medium 8 · low 1 |
| States     | content 14 · error 4 · loading 1 · empty 1 |
| Module     | `feature/account-detail`             |

---

## Coverage

All four declared states covered. The weight sits on `content` (14 of 20) because this screen is
mostly a hub: 9 of those 14 are chip-navigation assertions, one per outbound destination. That is
the right shape for a screen whose job is to fan out — every chip that renders is a chip that must
land somewhere, and TC-ACCTDTL-005 asserts all 9 render while 006–010/016–020 assert where each
one goes.

The four `error` scenarios are not redundant. They separate **recoverable** from
**non-recoverable** failure, which is the only distinction the Retry button keys on:

| Scenario | HTTP | `error.recoverable` | Retry button |
|----------|------|---------------------|--------------|
| TC-ACCTDTL-012 | 401 token expired | true | visible |
| TC-ACCTDTL-013 | 403 consent withdrawn | false | hidden |
| TC-ACCTDTL-014 | 404 not in authorised set | false | hidden |
| TC-ACCTDTL-015 | network failure | true | visible |

Offering Retry on 403/404 would invite the customer to fail repeatedly at something that cannot
succeed — the same reasoning that gives consent-list its separate `error_auth` state.

---

## TC-ACCTDTL-001 — Loading state, spinner visible and content hidden

**Priority:** critical · **State:** loading · **Fixture:** `demo-data.yaml#account`

- **Given** Valid PSU access token; both API calls in flight (slow network simulation)
- **When** Screen mounts with `accountId=40051512345678` before either response arrives
- **Then**
  - Circular progress indicator visible (`loading_spinner`)
  - Account header card NOT rendered
  - Balances list NOT rendered
  - Action chips NOT rendered
  - Open Banking badge NOT rendered

Four separate negative assertions rather than one "content hidden" — a partially-composed loading
state is the failure this catches, and a single assertion would pass while three of the four
rendered.

---

## TC-ACCTDTL-002 — Content state, account metadata renders correctly

**Priority:** critical · **State:** content · **Fixture:** `demo-data.yaml#account`

- **Given** HSBC sandbox returns `OBReadAccount6` for account 40051512345678 (CurrentAccount, Everyday Current, GBP, sort-code 40-05-15 12345678)
- **When** Screen mounts with `accountId=40051512345678` and both API calls succeed
- **Then**
  - Account header card visible
  - `AccountSubType` label shows "CurrentAccount"
  - Nickname shows "Everyday Current" (headlineMedium)
  - Identification shows "40-05-15 12345678"
  - Currency shows "GBP"
  - Servicer shows "MIDLGB2105V"
  - `StatusUpdateDateTime` shown in last-updated row

---

## TC-ACCTDTL-003 — Content state, three balance types all rendered

**Priority:** critical · **State:** content · **Fixture:** `demo-data.yaml#balances`

- **Given** `GET /accounts/40051512345678/balances` returns InterimAvailable, InterimBooked, OpeningBooked
- **When** Both API calls succeed
- **Then**
  - Balances section header visible
  - Balances list has exactly 3 items
  - InterimAvailable row: Type = "InterimAvailable", Amount = "2847.63 GBP"
  - InterimBooked row: Type = "InterimBooked", Amount = "2810.04 GBP"
  - OpeningBooked row: Type = "OpeningBooked", Amount = "3150.00 GBP"
  - Each balance row shows an `accessibility_label` combining Type and Amount

"Exactly 3" is doing real work here — OBIE returns balance types the screen does not model, and an
unbounded list would silently render them.

---

## TC-ACCTDTL-004 — Content state, Open Banking trust badge visible

**Priority:** high · **State:** content · **Fixture:** `demo-data.yaml#account`

- **Given** Content state fully loaded
- **When** Screen renders after successful API responses
- **Then**
  - Open Banking badge card (`open_banking_badge`) visible
  - Badge text renders `{strings.account_detail_open_banking_badge}`
  - Badge is non-interactive (no `on_click`)

The non-interactivity assertion is deliberate: a regulated trust mark that looks tappable and
does nothing is worse than no mark.

---

## TC-ACCTDTL-005 — Content state, all 9 action chips present and labelled

**Priority:** high · **State:** content · **Fixture:** `demo-data.yaml#account`

- **Given** Content state fully loaded for account 40051512345678
- **When** Explore section renders
- **Then**
  - Chip row horizontally scrollable
  - `chip_transactions` renders with icon `receipt_long`, label from `{strings.nav_chip_transactions}`
  - `chip_statements` renders with icon `description`
  - `chip_standing_orders` renders with icon `autorenew`
  - `chip_direct_debits` renders with icon `subscriptions`
  - `chip_scheduled_payments` renders with icon `schedule`
  - `chip_beneficiaries` renders with icon `people`
  - `chip_atm_locator` renders with icon `atm`, label from `{strings.account_detail.nav_chip_atm_label}`
  - `chip_product` renders with icon `description`, label from `{strings.nav_chip_product}`
  - `chip_party` renders with icon `person`, label from `{strings.nav_chip_party}`

---

## TC-ACCTDTL-006 — Chip navigation, Transactions

**Priority:** high · **State:** content · **Fixture:** `demo-data.yaml#account`

- **Given** Content state loaded for account 40051512345678
- **When** User taps the Transactions chip
- **Then** Navigates to `transactions` with `accountId='40051512345678'`

---

## TC-ACCTDTL-007 — Chip navigation, Statements

**Priority:** high · **State:** content · **Fixture:** `demo-data.yaml#account`

- **Given** Content state loaded for account 40051512345678
- **When** User taps the Statements chip
- **Then** Navigates to `statements` with `accountId='40051512345678'`

---

## TC-ACCTDTL-008 — Chip navigation, Standing Orders

**Priority:** medium · **State:** content · **Fixture:** `demo-data.yaml#account`

- **Given** Content state loaded for account 40051512345678
- **When** User taps the Standing Orders chip
- **Then** Navigates to `standing-orders` with `accountId='40051512345678'`

---

## TC-ACCTDTL-009 — Chip navigation, Direct Debits

**Priority:** medium · **State:** content · **Fixture:** `demo-data.yaml#account`

- **Given** Content state loaded for account 40051512345678
- **When** User taps the Direct Debits chip
- **Then** Navigates to `direct-debits` with `accountId='40051512345678'`

---

## TC-ACCTDTL-010 — Back button navigates to accounts screen

**Priority:** high · **State:** content · **Fixture:** `demo-data.yaml#account`

- **Given** Account detail loaded
- **When** User taps the back button (`back_button`)
- **Then** Nav stack popped; accounts screen active

---

## TC-ACCTDTL-011 — Empty state, zero balances for a Global Wallet sub-account

**Priority:** medium · **State:** empty · **Fixture:** `demo-data.yaml#empty_scenario`

- **Given** `GET /accounts/40051599999999` succeeds (Euro Wallet); `GET /accounts/40051599999999/balances` returns an empty array
- **When** Screen mounts with `accountId=40051599999999`
- **Then**
  - Account header card visible with Nickname "Euro Wallet" and Currency "EUR"
  - Open Banking badge visible
  - `balances_empty_state` visible (icon `account_balance_wallet`)
  - Balances section header NOT rendered
  - Balances list NOT rendered

This is a *partial* empty — the account exists and its header renders; only the balances block is
empty. Asserting the header still shows is the point: an all-or-nothing empty state would hide an
account the PSU is authorised to see.

---

## TC-ACCTDTL-012 — Error state, 401 token expired (recoverable)

**Priority:** critical · **State:** error · **Fixture:** `demo-data.yaml#error_scenarios[0]`

- **Given** PSU access token is expired
- **When** `GET /accounts/{AccountId}` returns HTTP 401
- **Then**
  - Error state renders (`error_state`)
  - Error icon visible (`error_outline`)
  - Error title shows `{strings.account_detail_error_title}`
  - Error body shows "Session expired. Please log in again."
  - Retry button visible and tappable (`error.recoverable == true`)
  - Tapping Retry re-triggers `account_detail_load` (loading state re-entered)

---

## TC-ACCTDTL-013 — Error state, 403 consent withdrawn (non-recoverable)

**Priority:** critical · **State:** error · **Fixture:** `demo-data.yaml#error_scenarios[1]`

- **Given** PSU has revoked consent from the HSBC app since the access token was issued
- **When** `GET /accounts/{AccountId}` returns HTTP 403
- **Then**
  - Error state renders
  - Error body shows "Access to this account has been withdrawn."
  - Retry button hidden by the ViewModel (`error.recoverable == false`)
  - Back navigation still accessible

The last assertion matters — a non-recoverable error with no Retry and no way out is a dead end.

---

## TC-ACCTDTL-014 — Error state, 404 account not in authorised set (non-recoverable)

**Priority:** high · **State:** error · **Fixture:** `demo-data.yaml#error_scenarios[2]`

- **Given** `AccountId` is not in the PSU-authorised account set returned by the consent
- **When** `GET /accounts/{AccountId}` returns HTTP 404
- **Then**
  - Error state renders
  - Error body shows "Account not found in your authorised account set."
  - Retry button hidden (`error.recoverable == false`)

---

## TC-ACCTDTL-015 — Error state, network failure with retry loop

**Priority:** high · **State:** error · **Fixture:** `demo-data.yaml#error_scenarios[3]`

- **Given** Device has no network connection
- **When** Both API calls fail with `ConnectException` / `SocketTimeoutException`
- **Then**
  - Error state renders
  - Error body shows "No network connection. Please check your connection and retry."
  - Retry button visible (`error.recoverable == true`)
  - Tapping Retry re-enters loading state and retries **both** API calls

"Both" is the assertion — retrying only the account call would leave the balances permanently
stale behind a screen that looks recovered.

---

## TC-ACCTDTL-016 — Chip navigation, Scheduled Payments

**Priority:** medium · **State:** content · **Fixture:** `demo-data.yaml#account`

- **Given** Content state loaded for account 40051512345678
- **When** User taps the Scheduled Payments chip (`chip_scheduled_payments`)
- **Then** Navigates to `scheduled-payments` with `accountId='40051512345678'`

---

## TC-ACCTDTL-017 — Chip navigation, Beneficiaries

**Priority:** medium · **State:** content · **Fixture:** `demo-data.yaml#account`

- **Given** Content state loaded for account 40051512345678
- **When** User taps the Beneficiaries chip (`chip_beneficiaries`)
- **Then** Navigates to `beneficiaries` with `accountId='40051512345678'`

---

## TC-ACCTDTL-018 — Chip navigation, ATM Locator (placeholder destination)

**Priority:** low · **State:** content · **Fixture:** `demo-data.yaml#account`

- **Given** Content state loaded for account 40051512345678, `AtmLocator` in `availableChips`
- **When** User taps the ATM Locator chip
- **Then** `onNavigateToChip(AccountDetailChip.AtmLocator, accountId)` fires → `navigate(AtmLocatorRoute)`, which renders `PlaceholderScreen("ATM locator")`. No feature module exists; the arg-less route drops `accountId`.

The dropped `accountId` is transcribed as declared, not tidied away. `atm-locator` is a registered
deferral (`idea-plan.yaml#deferred_routes` → `AtmLocatorRoute`, `target_milestone: unscheduled`),
so this scenario documents a known placeholder rather than asserting a working destination — and
the dropped param is exactly what will need fixing when the module lands.

---

## TC-ACCTDTL-019 — Chip navigation, Product

**Priority:** medium · **State:** content · **Fixture:** `demo-data.yaml#account`

- **Given** Content state loaded for account 40051512345678
- **When** User taps the Product chip (`chip_product`)
- **Then** Navigates to `product` with `accountId='40051512345678'`

---

## TC-ACCTDTL-020 — Chip navigation, Party

**Priority:** medium · **State:** content · **Fixture:** `demo-data.yaml#account`

- **Given** Content state loaded for account 40051512345678
- **When** User taps the Party chip (`chip_party`)
- **Then** Navigates to `party` with `accountId='40051512345678'`

Note the route name is `party` while the destination feature is `account-holder`. The chip enum
case is `AccountDetailChip.Party` (source truth, recorded in `TRAINING_MASTER#test_tags.builder_keys`),
so the scenario is transcribed under the route name the nav layer actually uses.

---

_Generated by /idea-feature-test-export | 2026-08-03_
