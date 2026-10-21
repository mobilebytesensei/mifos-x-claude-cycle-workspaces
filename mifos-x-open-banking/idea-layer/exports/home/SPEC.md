# SPEC — Home

| Field         | Value             |
|---------------|-------------------|
| Feature       | home              |
| Flavor        | consumer          |
| Status        | approved          |
| Quality Score | 95                |
| ViewModel     | HomeViewModel     |
| Archetype     | dashboard         |

---

## Overview

The landing dashboard: a hero balance card for the selected account, an account switcher, and the
five most recent transactions.

Three things define its behaviour.

**It is account-scoped with a switcher.** `selectedAccountId` drives the hero and the transaction
list; the bottom sheet swaps it. The accounts themselves come from the same `GET /accounts` the
Accounts screen uses, cached in memory rather than re-fetched.

**Balances and transactions load in parallel** (`coroutineScope` async/awaitAll) once an account is
selected — they are independent reads and serialising them would double the wait.

**Only five transactions, and only Booked ones.** The list is a client-side slice of the most recent
Booked transactions sorted descending by `BookingDateTime`. Pending transactions are excluded here —
a pending amount is not yet a movement, and showing it on a balance dashboard invites the customer to
reconcile two numbers that will not agree.

No top app bar — the hero card is the header.

---

## Screens

| ID   | Name | ViewModel     | Archetype |
|------|------|---------------|-----------|
| home | Home | HomeViewModel | dashboard |

**Shell:** no top app bar, bottom navigation visible, no FAB.

---

## Components

| ID                          | Type           | Description                                        |
|-----------------------------|----------------|-----------------------------------------------------|
| loading_skeleton            | stack          | Skeleton mirroring the loaded composition          |
| └ skeleton_hero             | shimmer        | Hero placeholder                                   |
| └ skeleton_tx_header        | shimmer        | Section header placeholder                         |
| └ skeleton_tx_1..3          | shimmer        | Three transaction row placeholders                 |
| account_selector_sheet      | bottom_sheet   | Account switcher — overlay, not a route            |
| └ account_selector_row      | list_item      | One selectable account                             |
| hero_balance_card           | card           | Selected account hero                              |
| └ hero_account_subtype      | text           | `{selectedAccount.AccountSubType}`                 |
| └ hero_account_icon         | icon           | Account type glyph                                 |
| └ hero_nickname             | text           | `{selectedAccount.Nickname}`                       |
| └ hero_balance              | text           | Primary balance amount                             |
| └ hero_available_label      | text           | "Available" label                                  |
| └ hero_available_amount     | text           | Second-best balance type                           |
| └ hero_identification       | text           | Account identification                             |
| recent_transactions_section | stack          | Recent transactions block                          |
| └ recent_tx_header          | section_header | Section heading                                    |
| └ view_all_transactions_link| text_button    | → transactions                                     |
| └ recent_transactions_list  | list           | The five most recent Booked transactions           |
| &nbsp;&nbsp;└ recent_tx_row | card           | One transaction — opens transaction-detail         |
| &nbsp;&nbsp;&nbsp;&nbsp;└ tx_category_icon | icon | Category glyph                            |
| &nbsp;&nbsp;&nbsp;&nbsp;└ tx_description | text | `{item.TransactionInformation}`             |
| &nbsp;&nbsp;&nbsp;&nbsp;└ tx_date | text  | `{item.BookingDateTime}` formatted                 |
| &nbsp;&nbsp;&nbsp;&nbsp;└ tx_amount | text | `{item.amountFormatted}`                          |
| empty_home                  | empty_state    | No accounts authorised                             |
| error_home                  | error_state    | Load failure — `role: alert`                       |
| └ retry_button              | button         | `{strings.home.error.retry}`                       |

The skeleton mirrors the real composition — hero, header, three rows — so there is no layout shift
when data arrives.

---

## States

Initial state: `loading`. The declared list is the canonical four; the sealed `ScreenState` carries
six, with `NoNetwork` and `Unauthenticated` rendering through the error surface.

| State   | Rendering                                              |
|---------|---------------------------------------------------------|
| loading | Skeleton hero + three row placeholders                 |
| content | Hero card, switcher, recent transactions               |
| empty   | `empty_home` — no accounts (`reason=no_accounts`)      |
| error   | `error_home` + retry                                   |

---

## State Model

**ViewModel:** `HomeViewModel`.

**State:** `HomeState` — `uiState: ScreenState<HomeData>`, `isAccountSelectorVisible: Boolean`,
`accountId: String`.

**Data model:** `HomeData`

| Field                  | Type                    |
|------------------------|-------------------------|
| `accounts`             | `List<AccountChipUi>`   |
| `selectedAccountId`    | `String`                |
| `accountTypeLabel`     | `String`                |
| `accountNickname`      | `String`                |
| `accountSubType`       | `String`                |
| `accountNumber`        | `String`                |
| `rawIdentification`    | `String`                |
| `balanceLabel`         | `String`                |
| `availableAmountLabel` | `String`                |
| `accountNumberLabel`   | `String`                |
| `recentTransactions`   | `List<TransactionRowUi>`|

Two balance labels, not one: the hero shows the preferred type and `availableAmountLabel` shows the
second-best, so the customer sees both booked and available where they differ.

**Screen state:** sealed `ScreenState` — `Loading`, `Content`, `Empty`, `Error`, `NoNetwork`,
`Unauthenticated`.

---

## Navigation

| From | To                 | Trigger                       | Type    |
|------|--------------------|-------------------------------|---------|
| home | transactions       | `view_all_transactions_link`  | push    |
| home | transaction-detail | `recent_tx_row` tap           | push    |
| home | (self)             | `account_selector_sheet`      | overlay |

The account switcher is a bottom sheet, not a route — home keeps its scroll position when it closes.

---

## API Endpoints

| ID                        | Endpoint                                  | Permission              |
|---------------------------|-------------------------------------------|-------------------------|
| accounts-list             | `GET /accounts`                           | `ReadAccountsDetail`    |
| selected-account-balances | `GET /accounts/{AccountId}/balances`      | `ReadBalances`          |
| recent-transactions       | `GET /accounts/{AccountId}/transactions`  | `ReadTransactionsDetail`|

Full detail including the parallel fetch, the balance preference order and the Booked-only rule:
`API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto, with `Roboto Mono` for the hero
balance and transaction amounts so figures align. Debit/credit colour comes from the
`payment_disposition` semantic pair rather than inline hex. Components reference semantic roles, so
both theme modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand
spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/home/{ui,api,flow,docs}.yaml. -->
