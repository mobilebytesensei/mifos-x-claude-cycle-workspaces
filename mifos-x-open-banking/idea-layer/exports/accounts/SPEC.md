# SPEC — Accounts

| Field         | Value               |
|---------------|---------------------|
| Feature       | accounts            |
| Flavor        | consumer            |
| Status        | approved            |
| Quality Score | 95                  |
| ViewModel     | AccountsViewModel   |
| Archetype     | index_list          |

---

## Overview

The authorised-accounts list — the first resource call after consent, and the entry point to the
whole account-browsing journey. Each card shows type, nickname, identifier and a balance; a chip
filter narrows by account type.

Two behaviours are worth knowing before implementing against this.

**Balances are a fan-out, not part of the list call.** `GET /accounts` returns the accounts;
balances then load per account in parallel (`coroutineScope` async/awaitAll). A card can therefore
render before its balance resolves, and a balance failure is per-account rather than fatal to the
list.

**A negative balance is a domain fact, not a formatting concern.** `isBalanceOwed` drives a
dedicated badge, because on a credit account the amount owed reads very differently from a positive
balance and must not be conveyed by a minus sign alone.

---

## Screens

| ID       | Name     | ViewModel         | Archetype  |
|----------|----------|-------------------|------------|
| accounts | Accounts | AccountsViewModel | index_list |

**Shell:** top app bar titled `{strings.accounts.screen.title}`, no leading icon — a bottom-nav
destination, not a pushed screen. Bottom navigation visible. No FAB.

---

## Components

| ID                    | Type        | Description                                                |
|-----------------------|-------------|-------------------------------------------------------------|
| loading_skeleton      | stack       | Skeleton container mirroring the card layout               |
| └ skeleton_card_1     | shimmer     | Placeholder card                                           |
| └ skeleton_card_2     | shimmer     | Placeholder card                                           |
| └ skeleton_card_3     | shimmer     | Placeholder card                                           |
| account_type_filter   | chip_group  | Type filter — operates on the loaded list, no refetch      |
| filter_all            | chip        | `ALL`                                                      |
| filter_current        | chip        | `CURRENT`                                                  |
| filter_savings        | chip        | `SAVINGS`                                                  |
| filter_credit         | chip        | `CREDIT`                                                   |
| accounts_list         | list        | Semantic list of authorised accounts                       |
| └ account_card        | card        | One account — opens account-detail                         |
| &nbsp;&nbsp;└ account_type_icon | icon | Glyph per `AccountUiType`                              |
| &nbsp;&nbsp;└ account_text_column | stack | Identity column                                      |
| &nbsp;&nbsp;&nbsp;&nbsp;└ account_subtype | text | `{item.accountSubType}`                    |
| &nbsp;&nbsp;&nbsp;&nbsp;└ account_nickname | text | `{item.nickname}`                         |
| &nbsp;&nbsp;&nbsp;&nbsp;└ account_number | text | `{item.identifier}`                         |
| &nbsp;&nbsp;└ balance_column | stack | Balance column                                          |
| &nbsp;&nbsp;&nbsp;&nbsp;└ balance_amount | text | `{item.balanceLabel}`                       |
| &nbsp;&nbsp;&nbsp;&nbsp;└ balance_owed_badge | badge | Shown when `isBalanceOwed`               |
| empty_accounts        | empty_state | Consent granted but no accounts authorised                 |
| error_accounts        | error_state | Load failure — `role: alert`                               |
| └ retry_button        | button      | `{strings.accounts.error.retry_button}` → `RetryLoad`      |

The skeleton mirrors the real card composition so there is no layout shift when data arrives.

---

## States

Initial state: `loading`. The declared state list is the canonical four, while the sealed
`ScreenState` carries six — `NoNetwork` and `Unauthenticated` are modelled in state and render
through the error surface.

| State   | Rendering                                        |
|---------|---------------------------------------------------|
| loading | Three shimmer cards                              |
| content | Filter chips + account cards                     |
| empty   | `empty_accounts` — authorised, but no accounts   |
| error   | `error_accounts` + retry                         |

---

## State Model

**ViewModel:** `AccountsViewModel`.

**State:** `AccountsState` — `uiState: ScreenState<AccountsData>`.

**Data model:** `AccountsData` — `rows: List<AccountRowUi>`, `activeFilter: AccountFilter`.

**Row model:** `AccountRowUi`

| Field               | Type            | Note                                        |
|---------------------|-----------------|---------------------------------------------|
| `id`                | `String`        |                                             |
| `type`              | `AccountUiType` | Drives `account_type_icon`                  |
| `nickname`          | `String`        |                                             |
| `identifier`        | `String`        | Display form                                |
| `balanceLabel`      | `String`        | Pre-formatted, currency-aware               |
| `isBalanceOwed`     | `Boolean`       | Drives `balance_owed_badge`                 |
| `accountSubType`    | `String`        |                                             |
| `accountNumber`     | `String`        |                                             |
| `rawIdentification` | `String`        | Unformatted — kept for downstream matching  |

**Screen state:** sealed `ScreenState` — `Loading`, `Content`, `Empty`, `Error`, `NoNetwork`,
`Unauthenticated`.

**Enums**
- `AccountUiType` — `CURRENT`, `SAVINGS`, `CREDIT`, `GLOBAL_MONEY`, `GLOBAL_WALLET`, `OTHER`
- `AccountFilter` — `ALL`, `CURRENT`, `SAVINGS`, `CREDIT`

The two enums are deliberately not the same set: `GLOBAL_MONEY`, `GLOBAL_WALLET` and `OTHER` are
renderable account types with no filter chip, so those accounts appear only under `ALL`.

**Actions:** `FilterAccounts`, `RetryLoad`.

**DI:** `AccountsOverviewRepository`.

---

## Navigation

| From     | To             | Trigger              | Type |
|----------|----------------|----------------------|------|
| accounts | account-detail | `account_card` tap   | push |

Filtering is a state transform over the loaded rows — it issues no request.

---

## API Endpoints

| ID            | Endpoint                             | DTO             | Permission           |
|---------------|--------------------------------------|-----------------|----------------------|
| accounts-list | `GET /accounts`                      | `BankAccount`   | `ReadAccountsDetail` |
| balances      | `GET /accounts/{AccountId}/balances` | `AccountBalance`| `ReadBalances`       |

Full error matrix, the balance preference order and the multi-currency rule: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto, with `Roboto Mono` for balances
and account numbers so figures align down the list. `balance_owed_badge` uses `errorContainer` —
money owed is the one list-level state that warrants the error role. Components reference semantic
roles, so both theme modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is the
canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/accounts/{ui,api,flow,docs}.yaml. -->
