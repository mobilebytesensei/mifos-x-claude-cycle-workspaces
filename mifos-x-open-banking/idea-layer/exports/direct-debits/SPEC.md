# SPEC — Direct Debits

| Field         | Value                     |
|---------------|---------------------------|
| Feature       | direct-debits             |
| Flavor        | consumer                  |
| Status        | approved                  |
| Quality Score | 95                        |
| ViewModel     | DirectDebitsViewModel     |
| Archetype     | index_list                |

---

## Overview

The direct-debit mandates on one account, reached from account-detail. Summary chips count active
and inactive; each card shows originator, status, last collected amount and date, and the mandate id.

**Inactive mandates are included in the response and shown.** A cancelled direct debit is still
part of the customer's financial picture — they may need its reference or its last collection — so
the list does not filter them out. The summary chips exist precisely to make the split legible at a
glance.

Like its siblings `scheduled-payments` and `standing-orders`, it carries a distinct **`unsupported`**
state for the OBIE `U000` case where the bank refuses the capability for this account — different
from `empty`, which means the bank answered and there are no mandates.

---

## Screens

| ID            | Name          | ViewModel             | Archetype  | Entry point    |
|---------------|---------------|-----------------------|------------|----------------|
| direct-debits | Direct Debits | DirectDebitsViewModel | index_list | account-detail |

**Shell:** top app bar, title `{strings.direct_debits.title}`, `back` leading icon. Bottom
navigation visible.

---

## Components

| ID                        | Type        | Description                                        |
|---------------------------|-------------|-----------------------------------------------------|
| loading_skeleton          | skeleton    | Placeholder mirroring the card layout              |
| back_button               | icon_button | Returns to account-detail                          |
| mandate_summary_chips     | chip_group  | Active / inactive counts                           |
| └ active_count_chip       | chip        | `{strings.direct_debits.active_count}`             |
| └ inactive_count_chip     | chip        | `{strings.direct_debits.inactive_count}`           |
| direct_debits_list        | list        | Semantic list of mandates                          |
| └ direct_debit_card       | card        | One mandate — opens direct-debit-detail            |
| &nbsp;&nbsp;└ dd_originator_name | text | `{item.name}`                                     |
| &nbsp;&nbsp;└ dd_status_badge | status_chip | `{item.statusLabel}` — variant from `isActive` |
| &nbsp;&nbsp;└ dd_previous_amount | text | `{item.amountLabel}`                              |
| &nbsp;&nbsp;└ dd_previous_date | text | Last collected date                                 |
| &nbsp;&nbsp;└ dd_mandate_id | text   | Mandate reference                                    |
| empty_direct_debits       | empty_state | No mandates on this account                        |
| unsupported_direct_debits | empty_state | Bank refuses the capability (`U000`)               |
| error_state               | error_state | Load failure — `role: alert`                       |
| └ retry_button            | button      | `{strings.direct_debits.retry}` → `RetryLoad`      |

---

## States

Initial state: `loading`. Five states, matching `DirectDebitsUiState` one-for-one.

| State       | Meaning                                                  |
|-------------|-----------------------------------------------------------|
| loading     | Fetching                                                 |
| content     | One or more mandates (active and/or inactive)            |
| empty       | Bank answered — no mandates on this account              |
| unsupported | Bank refuses the capability for this account (`U000`)    |
| error       | Load failed — retry offered                              |

`unsupported` here ships in source: `directDebitsStore:234` calls `recordIfUnsupported` before
rethrowing. This is the pattern `scheduled-payments` specifies but has not yet landed in its UI.

---

## State Model

**ViewModel:** `DirectDebitsViewModel`.

**State:** `DirectDebitsState` — `accountId: String`, `uiState: DirectDebitsUiState`.

**Screen state:** sealed `DirectDebitsUiState` — `Loading`, `Content`, `Empty`, `Unsupported`, `Error`.

**Row model:** `DirectDebitRowUi`

| Field                | Type      |
|----------------------|-----------|
| `mandateId`          | `String`  |
| `name`               | `String`  |
| `statusLabel`        | `String`  |
| `isActive`           | `Boolean` |
| `amountLabel`        | `String`  |
| `lastCollectedLabel` | `String`  |

**Error kinds:** `TokenExpired`, `ConsentRevoked`, `RateLimited`, `ServerError`, `NetworkError`.

**Actions:** `RetryLoad`.

**DI:** `SavedStateHandle` (carries `accountId`), `DirectDebitsRepository`.

---

## Navigation

| From          | To                  | Trigger              | Type |
|---------------|---------------------|----------------------|------|
| direct-debits | direct-debit-detail | `direct_debit_card`  | push |
| direct-debits | account-detail      | `back_button`        | pop  |

---

## API Endpoints

| ID                 | Endpoint                                   | DTO                    | Permission          |
|--------------------|--------------------------------------------|------------------------|---------------------|
| direct-debits-list | `GET /accounts/{AccountId}/direct-debits`  | `DirectDebitsSummary`  | `ReadDirectDebits`  |

Full detail including the no-pagination note: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto, with `Roboto Mono` for amounts.
Status chips follow the design system's role mapping — `error` for a cancelled mandate where the
arrangement is actually gone. Components reference semantic roles, so both theme modes resolve from
`design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/direct-debits/{ui,api,flow,docs}.yaml. -->
