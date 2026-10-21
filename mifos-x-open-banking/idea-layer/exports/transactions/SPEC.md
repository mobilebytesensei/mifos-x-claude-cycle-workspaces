# SPEC — Transactions

| Field         | Value                     |
|---------------|---------------------------|
| Feature       | transactions              |
| Flavor        | consumer                  |
| Status        | approved                  |
| Quality Score | 95                        |
| ViewModel     | TransactionsViewModel     |
| Archetype     | index_list                |

---

## Overview

The full transaction list for one account, with date grouping, search, money-in/out filters, a date
range picker, and cursor pagination.

**Pending transactions appear here.** This is the screen where they belong: rows carry a
`tx_pending_badge`, so a not-yet-settled amount is labelled rather than silently mixed into the
running total. `home`'s five-row preview deliberately excludes them; the difference is intentional
and the badge is what makes it safe to include them here.

Pagination follows the **OBIE `Links.Next` cursor**, not page numbers — the client stores the cursor
from each response and requests the next page with it. `hasNextPage` and `isPaginating` are separate
state fields so the Load More affordance and the in-flight indicator are independently controllable.

The error state is unusually rich: alongside Retry it carries a status chip and a **consent hint**,
because the most common failure here is a scope problem rather than a network one.

---

## Screens

| ID           | Name         | ViewModel             | Archetype  |
|--------------|--------------|-----------------------|------------|
| transactions | Transactions | TransactionsViewModel | index_list |

---

## Components

| ID                     | Type              | Description                                        |
|------------------------|-------------------|-----------------------------------------------------|
| loading_spinner        | progress_circular | Initial load                                       |
| period_summary         | stat_block        | Totals for the selected period                     |
| filter_chips           | chip_row          | Filter row                                         |
| └ filter_all           | chip              | `ALL`                                              |
| └ filter_money_in      | chip              | Credits only                                       |
| └ filter_money_out     | chip              | Debits only                                        |
| └ filter_date_range    | chip              | Opens the date range picker                        |
| search_field           | search_bar        | Query over the loaded rows                         |
| transactions_list      | list              | Date-grouped transactions                          |
| └ date_group_header    | section_header    | `{group.date}`                                     |
| └ transaction_row      | list_item         | One transaction — opens transaction-detail         |
| &nbsp;&nbsp;└ tx_merchant | text           | Merchant / description                             |
| &nbsp;&nbsp;└ tx_category_tag | chip       | Derived category                                   |
| &nbsp;&nbsp;└ tx_pending_badge | status_chip | Shown for Pending — **the reason pending is safe here** |
| load_more_button       | button            | Requests the next cursor page                      |
| pagination_loader      | progress_linear   | `isPaginating`                                     |
| empty_transactions     | empty_state       | No results                                         |
| └ clear_filters_button | button            | `ClearFilters` — recovers from an over-narrow filter |
| error_state            | error_state       | Load failure — `role: alert`                       |
| └ error_status_chip    | chip              | The failing status                                 |
| └ error_consent_hint   | text              | Points at a consent-scope cause                    |
| └ retry_button         | button            | `RetryLoad`                                        |

`empty_transactions` offers **Clear Filters** rather than only a message — the most likely cause of
an empty list is the customer's own filter, and the recovery should be one tap.

---

## States

Initial state: `loading`. Four states, matching `TransactionsUiState` one-for-one.

| State   | Rendering                                              |
|---------|---------------------------------------------------------|
| loading | `loading_spinner`                                      |
| content | Summary, filters, search, grouped rows, pagination     |
| empty   | `empty_transactions` + Clear Filters                   |
| error   | `error_state` + status chip + consent hint + Retry     |

Pagination is **not** a state — it is `isPaginating` within `content`, so appending a page never
blanks the list the customer is reading.

---

## State Model

**ViewModel:** `TransactionsViewModel`.

**State:** `TransactionsState`

| Field                 | Type                  | Purpose                                |
|-----------------------|-----------------------|-----------------------------------------|
| `accountId`           | `String`              | Scope                                   |
| `uiState`             | `TransactionsUiState` |                                         |
| `activeFilter`        | `TransactionFilter`   | All / money in / money out              |
| `query`               | `String`              | Search text                             |
| `dateFrom`            | `LocalDate?`          | Range start                             |
| `dateTo`              | `LocalDate?`          | Range end                               |
| `showDateRangePicker` | `Boolean`             | Picker visibility (ViewModel-held)      |
| `hasNextPage`         | `Boolean`             | Whether a `Links.Next` cursor exists    |
| `isPaginating`        | `Boolean`             | Append in flight                        |

**Actions:** `LoadTransactions`, `RetryLoad`, `LoadMore`, `FilterTransactions`,
`SearchTransactions`, `OpenDateRangePicker`, `SetDateRange`, `DismissDateRangePicker`,
`ClearFilters`.

Nine actions — four of them serve the date-range picker and filter clearing, which is proportionate
given that filters are the main cause of an empty result.

**DI:** `SavedStateHandle` (carries `accountId`), `TransactionsRepository`.

---

## Navigation

| From         | To                 | Trigger              | Type |
|--------------|--------------------|----------------------|------|
| transactions | transaction-detail | `transaction_row`    | push |

---

## API Endpoints

| ID           | Endpoint                                  | Permission               |
|--------------|-------------------------------------------|--------------------------|
| transactions | `GET /accounts/{AccountId}/transactions`  | `ReadTransactionsDetail` |

Returns booked **and pending** transactions within the optional date range, with OBIE-standard
`Links.Next` cursor pagination. Full detail: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto, with `Roboto Mono` for amounts so
figures align down each date group. Debit/credit colour comes from the `payment_disposition`
semantic pair; the pending badge uses `tertiaryContainer` rather than `error` — pending is a state,
not a fault. Components reference semantic roles, so both theme modes resolve from
`design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/transactions/{ui,api,flow,docs}.yaml. -->
