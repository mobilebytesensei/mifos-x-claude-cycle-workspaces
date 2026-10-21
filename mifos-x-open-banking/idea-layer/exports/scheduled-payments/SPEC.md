# SPEC — Scheduled Payments

| Field         | Value                          |
|---------------|--------------------------------|
| Feature       | scheduled-payments             |
| Flavor        | consumer                       |
| Status        | approved                       |
| Quality Score | 96                             |
| ViewModel     | ScheduledPaymentsViewModel     |
| Archetype     | index_list                     |
| Route         | `accounts/{accountId}/scheduled-payments` |

---

## Overview

Future-dated payments for one account, reached from account-detail. Each row shows payee, amount,
due date, a type chip, the creditor identification and the reference.

The domain distinction that shapes the rows is `ScheduledType`: **Execution** means the money leaves
the account on that date; **Arrival** means it lands at the beneficiary on that date. Those are
different promises to the customer, which is why the type is a chip on every row rather than a
footnote.

The screen carries five states, not four — `unsupported` is a first-class state, and it is
deliberately distinct from `empty`:

- **empty** — the bank answered, and nothing is scheduled.
- **unsupported** — the bank refuses the capability for this account (OBIE `U000`).

Collapsing them would tell a customer "you have no scheduled payments" when the truth is "this bank
will not tell us."

---

## Screens

| ID                 | Name               | ViewModel                  | Entry point    |
|--------------------|--------------------|----------------------------|----------------|
| scheduled-payments | Scheduled Payments | ScheduledPaymentsViewModel | account-detail |

**Shell:** top app bar, title `{strings.sp_screen_title}`, `back` leading icon. Bottom navigation
visible. No FAB — this screen is read-only; it lists scheduled payments but does not create them.

---

## Components

| ID                             | Type        | Description                                          |
|--------------------------------|-------------|-------------------------------------------------------|
| back_button                    | icon_button | Returns to account-detail                             |
| scheduled_payments_list        | list        | Semantic list of scheduled payments                   |
| └ scheduled_payment_card       | card        | One scheduled payment                                 |
| &nbsp;&nbsp;└ sp_payee_name    | text        | `{item.CreditorAccount.Name}`                         |
| &nbsp;&nbsp;└ sp_amount        | text        | `{item.InstructedAmount.Currency} {…Amount}`          |
| &nbsp;&nbsp;└ sp_scheduled_date| text        | `{strings.sp_due_prefix} {item.scheduledDateLabel}`   |
| &nbsp;&nbsp;└ sp_type_chip     | chip        | `{item.scheduledTypeLabel}` — Execution vs Arrival    |
| &nbsp;&nbsp;└ sp_account_id    | text        | `{strings.sp_account_prefix} {item.creditorIdentification}` |
| &nbsp;&nbsp;└ sp_reference     | text        | `{strings.sp_ref_prefix} {item.Reference}`            |
| empty_scheduled_payments       | empty_state | Nothing scheduled                                     |
| unsupported_scheduled_payments | empty_state | Bank does not support the capability (`U000`)         |
| error_state                    | error_state | Load failure — `role: alert`                          |
| └ retry_button                 | button      | `{strings.action_retry}` → `RetryLoad`                |

---

## States

Initial state: `loading`. Five states, matching `ScheduledPaymentsUiState` one-for-one.

| State       | Meaning                                                       |
|-------------|----------------------------------------------------------------|
| loading     | Fetching                                                       |
| content     | One or more future-dated payments                              |
| empty       | Bank answered — none scheduled                                 |
| unsupported | Bank refuses the capability for this account (OBIE `U000`)     |
| error       | Load failed — retry offered                                    |

### `unsupported` is spec-ahead-of-source — deliberately

Declared 2026-08-02 by `/idea-sync`, owed by `/implement`, and kept rather than pruned to match
source. The reasoning is recorded in the YAML and worth carrying here: **source already records the
refusal** — `BankingStores.kt:377` (`scheduledPaymentsStore`) calls
`result.error.recordIfUnsupported(endpoint = AccountEndpoint.ScheduledPayments)` before rethrowing,
exactly as `directDebitsStore:234` and `standingOrdersStore:344` do. What source lacks is the UI
branch that lands it.

Its two sibling features (`direct-debits`, `standing-orders`) both declare `unsupported`; this one
did not, because the 2026-07-28 reverse sync back-filled the state into them from source and missed
this feature. Deleting the state to "match source" would have erased the specification of a live
defect rather than fixing it.

---

## State Model

**ViewModel:** `ScheduledPaymentsViewModel`.

**State:** `ScheduledPaymentsState` — `accountId: String`, `uiState: ScheduledPaymentsUiState`.

**Screen state:** sealed `ScheduledPaymentsUiState` — `Loading`, `Content`, `Empty`, `Unsupported`, `Error`.

**Row model:** `ScheduledPaymentUiModel`

| Field                    | Type                    |
|--------------------------|-------------------------|
| `scheduledPaymentId`     | `String`                |
| `payeeName`              | `String`                |
| `amountLabel`            | `String`                |
| `scheduledDateLabel`     | `String`                |
| `scheduledType`          | `ScheduledPaymentType`  |
| `creditorIdentification` | `String`                |
| `reference`              | `String`                |

**Error types:** `TokenExpired`, `ConsentRevoked`, `RateLimited`, `NetworkError`.

**Actions:** `RetryLoad`.

**Nav callbacks:** `onBack -> popBackStack()` returning to account-detail.

**DI:** `SavedStateHandle` (carries `accountId`), `ScheduledPaymentsRepository`.

---

## Navigation

| From               | To                 | Trigger | Type |
|--------------------|--------------------|---------|------|
| account-detail     | scheduled-payments | entry   | push |
| scheduled-payments | account-detail     | `onBack`| pop  |

A leaf screen — no forward navigation.

---

## API Endpoints

| ID                      | Endpoint                                          | Data path                |
|-------------------------|---------------------------------------------------|--------------------------|
| scheduled-payments-list | `GET /accounts/{AccountId}/scheduled-payments`    | `Data.ScheduledPayment`  |

Returns future-dated scheduled payments for the account. Full field list, the `ScheduledType`
semantics and error recovery: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto, with `Roboto Mono` for amounts so
figures align down the list. The type chip uses `secondaryContainer` rather than a status colour —
Execution and Arrival are categories, not severities. Components reference semantic roles, so both
theme modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/scheduled-payments/{ui,api,flow,docs}.yaml. -->
