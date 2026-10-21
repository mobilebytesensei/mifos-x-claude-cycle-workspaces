# SPEC — Standing Orders

| Field         | Value                      |
|---------------|----------------------------|
| Feature       | standing-orders            |
| Flavor        | consumer                   |
| Status        | approved                   |
| Quality Score | 95                         |
| ViewModel     | StandingOrdersViewModel    |
| Archetype     | index_list                 |

---

## Overview

The standing orders on one account, reached from account-detail. Each card shows payee, status,
amount, frequency, next payment date, an optional final payment date, sort code and reference.

Two things distinguish it from the sibling recurring-payment screens.

**Frequency is an ISO 20022 code, not a word.** OBIE returns values like `IntrvlMnthDay:01:01`
(monthly on the 1st). The ViewModel maps these to a `frequency_label` — the raw code must never
reach the screen, and the mapping is the feature's real work.

**A final payment date is optional and meaningful.** `hasFinalPayment` gates `so_final_date`: a
standing order with an end date is a different commitment from an open-ended one, so the row appears
only when there is one.

The summary line ("3 Active · 1 Inactive") is computed from `StandingOrderStatusCode` counts rather
than from list length, so inactive orders are counted without being hidden.

Like `direct-debits` and `scheduled-payments`, it carries a distinct **`unsupported`** state for the
OBIE `U000` case.

---

## Screens

| ID              | Name            | ViewModel               | Archetype  | Entry point    |
|-----------------|-----------------|-------------------------|------------|----------------|
| standing-orders | Standing Orders | StandingOrdersViewModel | index_list | account-detail |

**Shell:** top app bar, title `{strings.standing_orders_screen_title}`, `back` leading icon. Bottom
navigation visible.

---

## Components

| ID                          | Type        | Description                                        |
|-----------------------------|-------------|-----------------------------------------------------|
| back_button                 | icon_button | Returns to account-detail                          |
| summary_row                 | text        | "3 Active · 1 Inactive" — from status-code counts  |
| standing_orders_list        | list        | Semantic list of standing orders                   |
| └ standing_order_card       | card        | One standing order                                 |
| &nbsp;&nbsp;└ so_payee_name | text        | `{item.payeeName}`                                 |
| &nbsp;&nbsp;└ so_status_badge | status_chip | `{item.statusLabel}` — from `status_variant`     |
| &nbsp;&nbsp;└ so_amount     | text        | `{item.amountLabel}` + currency                    |
| &nbsp;&nbsp;└ so_frequency  | text        | `{item.frequencyLabel}` — mapped from the ISO code |
| &nbsp;&nbsp;└ so_next_date  | text        | Next payment date                                  |
| &nbsp;&nbsp;└ so_final_date | text        | Final payment date — **only when `hasFinalPayment`** |
| &nbsp;&nbsp;└ so_sort_code  | text        | `{item.sortCodeLabel}`                             |
| &nbsp;&nbsp;└ so_payment_ref| text        | Payment reference                                  |
| empty_standing_orders       | empty_state | No standing orders on this account                 |
| └ empty_create_button       | button      | Create a standing order                            |
| unsupported_standing_orders | empty_state | Bank refuses the capability (`U000`)               |
| error_state                 | error_state | Load failure — `role: alert`                       |
| └ retry_button              | button      | `RetryLoad` — **always present** on error          |

The empty state carries a create CTA; the unsupported state does not — there is no point offering to
create something the bank will not serve.

---

## States

Initial state: `loading`. Five states, matching `StandingOrdersUiState` one-for-one.

| State       | Meaning                                                                    |
|-------------|-----------------------------------------------------------------------------|
| loading     | `OBReadStandingOrder6` fetch in flight; no data yet                        |
| content     | Non-empty response; all transforms applied by the ViewModel                |
| empty       | `Data.StandingOrder[]` returned empty — zero-result UI                     |
| unsupported | Bank refuses the capability for this account (`U000`)                      |
| error       | Typed error state; the Retry button is always available                    |

In `content`, `standingOrders` is the mapped OBIE list carrying `frequency_label`, `status_variant`
and `hasFinalPayment`; `summaryLabel` is the computed active/inactive string.

---

## State Model

**ViewModel:** `StandingOrdersViewModel`.

**State:** `StandingOrdersState` — `accountId: String`, `uiState: StandingOrdersUiState`.

**Screen state:** sealed `StandingOrdersUiState` — `Loading`, `Content`, `Empty`, `Unsupported`,
`Error`.

**DI:** `SavedStateHandle` (carries `accountId`), `StandingOrdersRepository`.

---

## Navigation

| From            | To             | Trigger              | Type |
|-----------------|----------------|----------------------|------|
| standing-orders | account-detail | `back_button`        | pop  |

---

## API Endpoints

| ID                   | Endpoint                                       | DTO                     | Permission                  |
|----------------------|------------------------------------------------|-------------------------|-----------------------------|
| standing-orders-list | `GET /accounts/{AccountId}/standing-orders`    | `StandingOrdersSummary` | `ReadStandingOrdersDetail`  |

The **detail** scope is required: `ReadStandingOrders` alone omits `NextPaymentAmount` and
`Reference`. Full error matrix and the ISO 20022 frequency note: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto, with `Roboto Mono` for amounts and
sort codes so figures align down the list. Status chips follow the design system's role mapping —
`error` only where the order is actually inactive. Components reference semantic roles, so both
theme modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/standing-orders/{ui,api,flow,docs}.yaml. -->
