# SPEC — Transaction Detail

| Field         | Value                          |
|---------------|--------------------------------|
| Feature       | transaction-detail             |
| Flavor        | consumer                       |
| Status        | approved                       |
| Quality Score | 95                             |
| ViewModel     | TransactionDetailViewModel     |
| Archetype     | detail_screen                  |

---

## Overview

One transaction in full: a signed amount header, merchant, status, and a detail card of seven rows —
booking and value dates, category, MCC, balance after, reference and bank code.

The defining constraint is that **OBIE v4.0 AIS provides no single-transaction endpoint.** There is
no `GET /transactions/{id}` to call. The screen resolves its transaction by filtering the account's
transaction list by the `transactionId` passed as a route param — reusing the cached list where one
is already loaded, otherwise fetching it.

Two consequences follow. `TransactionNotFoundError` is a real and reachable state: an id that no
longer appears in the list has nothing to render. And the screen is only as fresh as the list it
reads from, which is why it is reached from `transactions` and `home` rather than deep-linked from
outside.

`CopyReference` exists as a first-class action because the payment reference is the one value a
customer routinely needs to quote elsewhere.

---

## Screens

| ID                 | Name               | ViewModel                  | Archetype     |
|--------------------|--------------------|----------------------------|---------------|
| transaction-detail | Transaction Detail | TransactionDetailViewModel | detail_screen |

---

## Components

| ID                        | Type        | Description                                          |
|---------------------------|-------------|-------------------------------------------------------|
| back_button               | icon_button | Returns to the referring list                        |
| amount_header             | text        | Signed amount — `CreditDebitIndicator` drives sign and colour |
| transaction_currency_meta | text        | Currency of the amount                               |
| merchant_name             | text        | Merchant display name                                |
| status_badge              | chip        | `{transaction.Status}` — Booked / Pending            |
| header_separator          | divider     |                                                      |
| detail_card               | card        | Detail panel                                         |
| └ detail_card_header      | text        | Section heading                                      |
| └ booking_date_row        | list_item   | `BookingDateTime`                                    |
| └ value_date_row          | list_item   | `ValueDateTime` — when funds actually moved          |
| └ category_row            | list_item   | Derived category                                     |
| └ mcc_row                 | list_item   | Merchant Category Code                               |
| └ balance_after_row       | list_item   | Running balance after this transaction               |
| └ reference_row           | list_item   | Payment reference — `CopyReference` target           |
| └ bank_code_row           | list_item   | Proprietary bank transaction code                    |
| error_state               | error_state | Load failure — `role: alert`                         |
| └ retry_button            | button      | `RetryLoad`                                          |
| └ go_back_button          | button      | Second CTA — return to the list                      |
| transaction_empty_state   | empty_state | Transaction not found in the list                    |
| └ transaction_empty_back_button | button| Return to the list                                   |

Booking date and value date are separate rows deliberately: they differ for card transactions, and
the value date is the one that determines when the money actually moved.

The error state carries a **second CTA** — Go Back. If the transaction cannot be resolved, retrying
the same id may never succeed, so returning to the list is a real alternative rather than a dead end.

---

## States

Initial state: `loading`. Four states, matching `TransactionDetailUiState` one-for-one.

| State   | Rendering                                             |
|---------|--------------------------------------------------------|
| loading | Resolving the transaction from the list               |
| content | Amount header + detail card                           |
| empty   | Transaction id not present — `transaction_empty_state`|
| error   | `error_state` + Retry + Go Back                       |

---

## State Model

**ViewModel:** `TransactionDetailViewModel`.

**State:** `TransactionDetailState` — `transactionId: String`, `accountId: String`,
`uiState: TransactionDetailUiState`.

Both ids are held: the account is what gets fetched, the transaction is what gets filtered out of it.

**Screen state:** sealed `TransactionDetailUiState` — `Loading`, `Content`, `Error`, `Empty`.

**Error types:** `TokenExpiredError`, `ConsentWithdrawnError`, `TransactionNotFoundError`,
`NetworkError`.

**Actions:** `RetryLoad`, `CopyReference`.

**Nav callbacks:** `onBack -> popBackStack()`.

**DI:** `SavedStateHandle` (carries both ids), `TransactionDetailRepository`.

---

## Navigation

| From               | To         | Trigger  | Type |
|--------------------|------------|----------|------|
| transaction-detail | (previous) | `onBack` | pop  |

A leaf screen. Inbound from `transactions`, `home` (recent list), `statement-detail`, and payment
notifications.

---

## API Endpoints

| ID           | Endpoint                                  | Permission               |
|--------------|-------------------------------------------|--------------------------|
| transactions | `GET /accounts/{AccountId}/transactions`  | `ReadTransactionsDetail` |

The **list** endpoint — there is no single-transaction endpoint in OBIE v4.0 AIS. Full detail:
`API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto, with `Roboto Mono` for the amount
and the balance-after figure. Debit/credit colour comes from the `payment_disposition` semantic pair
driven by `CreditDebitIndicator`, not inline hex. Components reference semantic roles, so both theme
modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/transaction-detail/{ui,api,flow,docs}.yaml. -->
