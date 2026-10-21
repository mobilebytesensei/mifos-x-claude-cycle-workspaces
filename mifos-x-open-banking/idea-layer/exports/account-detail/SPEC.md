# SPEC — Account Detail

| Field         | Value                     |
|---------------|---------------------------|
| Feature       | account-detail            |
| Flavor        | consumer                  |
| Status        | approved                  |
| Quality Score | 95                        |
| ViewModel     | AccountDetailViewModel    |
| Archetype     | detail_screen             |

---

## Overview

One account's metadata and balances, plus the chip row that fans out to everything else scoped to
that account. It is the hub of the account-browsing journey: nine of the app's screens are reached
from here and almost nowhere else.

The chip row is **capability-gated, not static**. `availableChips: Set<AccountDetailChip>` is
resolved per account through `AccountCapabilityRegistry`, so a chip is present only where the bank
supports that capability for that account. This is what stops the screen offering, say, Scheduled
Payments on an account whose bank refuses it — the sibling screens each have their own
`unsupported` state for the case where the customer gets there anyway.

Balances are a list, not a single figure: OBIE returns several balance types per account
(InterimAvailable, InterimBooked, OpeningBooked and others), and this screen shows all of them
rather than picking one.

---

## Screens

| ID             | Name           | ViewModel              | Archetype     |
|----------------|----------------|------------------------|---------------|
| account-detail | Account Detail | AccountDetailViewModel | detail_screen |

**Shell:** top app bar titled `{account.Nickname}` — the account's own name, not a static string —
with a `back` leading icon. Bottom navigation visible. No FAB.

---

## Components

| ID                        | Type              | Description                                            |
|---------------------------|-------------------|---------------------------------------------------------|
| loading_spinner           | progress_circular | Loading state                                          |
| back_button               | icon_button       | Returns to accounts                                    |
| account_header_card       | card              | Identity block                                         |
| └ account_subtype_label   | text              | `{account.AccountSubType}`                             |
| └ account_nickname        | text              | `{account.Nickname}`                                   |
| └ account_identification  | text              | `{account.Account.Identification}`                     |
| └ account_currency        | text              | `{account.Currency}`                                   |
| └ account_servicer        | text              | `{account.Servicer.Identification}`                    |
| └ account_last_updated    | text              | Data freshness stamp                                   |
| open_banking_badge        | card              | Regulated-connection badge                             |
| └ open_banking_badge_text | text              | Badge copy                                             |
| account_description_card  | card              | Bank-supplied account description                      |
| └ account_description_label | text            | Section label                                          |
| └ account_description_value | text            | `{account.Description}`                                |
| balances_header           | section_header    | Balances section                                       |
| balances_list             | list              | All balance types returned for the account             |
| └ balance_row             | list_item         | One balance type + amount                              |
| balances_empty_state      | empty_state       | Account resolved but no balances returned              |
| actions_header            | section_header    | Actions section                                        |
| action_chips              | chip_row          | Capability-gated navigation chips                      |
| └ chip_transactions       | chip              | → transactions                                         |
| └ chip_statements         | chip              | → statements                                           |
| └ chip_standing_orders    | chip              | → standing-orders                                      |
| └ chip_direct_debits      | chip              | → direct-debits                                        |
| └ chip_scheduled_payments | chip              | → scheduled-payments                                   |
| └ chip_beneficiaries      | chip              | → beneficiaries                                        |
| └ chip_atm_locator        | chip              | → atm-locator                                          |
| └ chip_product            | chip              | → product                                              |
| └ chip_party              | chip              | → account-holder                                       |
| error_state               | error_state       | Load failure — `role: alert`                           |
| └ retry_button            | button            | `{strings.account_detail_retry}` → `RetryLoad`         |

Note `balances_empty_state` sits **inside** a loaded screen — an account with no balances is not an
empty screen, so the emptiness is scoped to the balances section rather than replacing the view.

---

## States

Initial state: `loading`. Four states, matching `AccountDetailUiState` one-for-one.

| State   | Rendering                                                     |
|---------|----------------------------------------------------------------|
| loading | `loading_spinner`                                             |
| content | Header, badge, description, balances list, capability chips   |
| empty   | Account resolved with no renderable content                   |
| error   | `error_state` + retry                                         |

---

## State Model

**ViewModel:** `AccountDetailViewModel`.

**State:** `AccountDetailState` — `accountId: String`, `uiState: AccountDetailUiState`,
plus `availableChips: Set<AccountDetailChip>`.

**Screen state:** sealed `AccountDetailUiState` — `Loading`, `Content`, `Empty`, `Error`.

**`AccountDetailChip` enum** — `Transactions`, `Statements`, `StandingOrders`, `DirectDebits`,
`ScheduledPayments`, `Beneficiaries`, `AtmLocator`, `Product`, `Party`.

The enum case, not a slug, is what the per-chip test tag is built from — a detail that matters when
writing assertions against this screen.

**Actions:** `RetryLoad`.

**Nav callbacks:** `onNavigateToChip(chip: AccountDetailChip, accountId: String)` ·
`onBack -> popBackStack()` returning to accounts.

Every forward navigation goes through the single `onNavigateToChip` callback carrying the enum and
the account id — there are not nine separate callbacks.

**DI:** `SavedStateHandle` (carries `accountId`), `AccountDetailRepository`,
`AccountCapabilityRegistry`.

---

## Navigation

| From           | To                 | Trigger                     | Type |
|----------------|--------------------|-----------------------------|------|
| account-detail | transactions       | `chip_transactions`         | push |
| account-detail | statements         | `chip_statements`           | push |
| account-detail | standing-orders    | `chip_standing_orders`      | push |
| account-detail | direct-debits      | `chip_direct_debits`        | push |
| account-detail | scheduled-payments | `chip_scheduled_payments`   | push |
| account-detail | beneficiaries      | `chip_beneficiaries`        | push |
| account-detail | atm-locator        | `chip_atm_locator`          | push |
| account-detail | product            | `chip_product`              | push |
| account-detail | account-holder     | `chip_party`                | push |
| account-detail | accounts           | `onBack`                    | pop  |

Each chip renders only when its capability is in `availableChips`.

**Known deferral:** `AtmLocatorRoute` resolves to `PlaceholderScreen("ATM locator")` in
cmp-navigation — the chip renders and navigates, but no feature module implements the destination.
It is recorded in `idea-plan.yaml#deferred_routes` with `target_milestone: unscheduled`; the
atm-locator idea-layer screen itself does exist.

---

## API Endpoints

| ID             | Endpoint                            | Purpose                                                    |
|----------------|-------------------------------------|------------------------------------------------------------|
| account-detail | `GET /accounts/{AccountId}`         | Account metadata — subtype, identification, currency, servicer |
| balances       | `GET /accounts/{AccountId}/balances`| All balance types for the account                          |

Full detail: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto, with `Roboto Mono` for balance
figures and the account identification so digits align. Chips use `secondaryContainer`; the Open
Banking badge uses `primary` with a `verified_user` glyph to read as a trust marker rather than a
status. Components reference semantic roles, so both theme modes resolve from
`design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/account-detail/{ui,api,flow,docs}.yaml. -->
