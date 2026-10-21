# SPEC — Standing Order Detail

| Field         | Value                            |
|---------------|----------------------------------|
| Feature       | standing-order-detail            |
| Flavor        | consumer                         |
| Status        | approved                         |
| Quality Score | 93                               |
| ViewModel     | StandingOrderDetailViewModel     |
| Archetype     | detail_screen                    |

---

## Overview

One standing order in full, in four cards: recipient, schedule, amount, and recent executions —
plus pause/resume and cancel.

Like its direct-debit counterpart, the content type is **display-ready label strings only** — no
typed enums, and explicitly no dialog or action-in-progress flags. The schedule card carries five
date rows (first, last, next, final) rather than one, because a standing order is defined by its
sequence: when it started, when it last ran, when it next runs, and whether it ever ends. "Ongoing"
is a rendered value for an open-ended order rather than a blank.

The recipient account is masked and falls back to `''` when unknown, which is why the row can render
empty rather than showing a placeholder.

---

## Screens

| ID                    | Name                  | ViewModel                    | Archetype     |
|-----------------------|-----------------------|------------------------------|---------------|
| standing-order-detail | Standing Order Detail | StandingOrderDetailViewModel | detail_screen |

---

## Components

| ID                          | Type      | Description                                  |
|-----------------------------|-----------|-----------------------------------------------|
| sod_root                    | stack     | Vertical container                           |
| sod_recipient_card          | card      | RECIPIENT                                    |
| └ sod_recipient_name_*      | stack/text| Name row                                     |
| └ sod_recipient_account_*   | stack/text| Masked account row — `''` when unknown       |
| sod_schedule_card           | card      | SCHEDULE                                     |
| └ sod_status_*              | stack/text| Status                                       |
| └ sod_frequency_*           | stack/text| Frequency label                              |
| └ sod_first_payment_*       | stack/text| First payment                                |
| └ sod_last_payment_*        | stack/text| Last payment                                 |
| └ sod_next_payment_*        | stack/text| Next payment                                 |
| └ sod_final_date_*          | stack/text| Final date — "Ongoing" when open-ended       |
| sod_amount_card             | card      | PAYMENT AMOUNT                               |
| └ sod_amount_value          | text      | Amount                                       |
| └ sod_currency_badge        | badge     | Currency code                                |
| sod_history_card            | card      | RECENT EXECUTIONS                            |
| └ sod_history_list          | list      | Past executions                              |
| &nbsp;&nbsp;└ sod_history_row | list_item | date · status · amount                     |
| sod_action_row              | stack     | Action row                                   |
| └ sod_pause_resume_button   | button    | Pause / Resume                               |
| └ sod_cancel_button         | button    | Cancel                                       |
| sod_bottom_spacer           | spacer    |                                              |
| sod_loading_skeleton        | skeleton  | Loading placeholder                          |
| sod_error_state             | stack     | Error container                              |
| └ sod_error_icon            | icon      | `cloud_off`                                  |
| └ sod_error_title           | text      | "Standing Order Not Found"                   |
| └ sod_error_message         | text      | "We could not load this standing order."     |
| └ sod_retry_button          | button    | Retry                                        |
| sod_empty_state             | stack     | Empty container                              |
| └ sod_empty_message         | text      | "No details are available."                  |
| └ sod_back_to_list_button   | button    | "Go Back"                                    |

---

## States

Initial state: `loading`. Six states — the canonical four plus two connectivity states.

| State           | Rendering                                        |
|-----------------|---------------------------------------------------|
| loading         | `sod_loading_skeleton`                           |
| content         | Four cards + action row                          |
| empty           | "No details are available." + Go Back            |
| error           | `cloud_off` + "Standing Order Not Found" + Retry |
| no_network      | Error treatment                                  |
| unauthenticated | Error treatment                                  |

---

## State Model

**ViewModel:** `StandingOrderDetailViewModel`.

**Constructor:** `bankId: String`, `accountId: String`, `standingOrderId: String` — three ids,
matching the address shape of the edit endpoint.

**Flows:** `uiState: StateFlow<ScreenState<StandingOrderDetailContent>>`, default `ScreenState.Loading`.

**Content — `StandingOrderDetailContent`** (display-ready labels only; no typed enums, no dialog or
action-in-progress flags)

| Field              | Type      | Note                          |
|--------------------|-----------|-------------------------------|
| `name`             | `String`  |                               |
| `statusLabel`      | `String`  |                               |
| `isActive`         | `Boolean` | Drives the status treatment   |
| `isCreated`        | `Boolean` |                               |
| `recipientName`    | `String`  |                               |
| `recipientAccount` | `String`  | Masked; `''` when unknown     |
| `amount`           | `String`  |                               |

---

## Navigation

| From                  | To                  | Trigger              | Type |
|-----------------------|---------------------|----------------------|------|
| standing-order-detail | transaction-detail  | `sod_history_row`    | push |
| standing-order-detail | standing-order-edit | edit affordance      | push |
| standing-order-detail | standing-orders     | back / Go Back       | pop  |

Execution rows open `transaction-detail`, so a past payment can be inspected like any other
transaction.

---

## API Endpoints

`api: []` — **this screen makes no network call of its own.** Its content is re-derived from the
standing-order list already fetched by `standing-orders`, in the same pattern as
`direct-debit-detail`.

That is also why `StandingOrderDetailContent` holds only display-ready strings: the transforms —
`frequency_label`, `status_variant`, `hasFinalPayment` — were applied upstream by
`StandingOrdersViewModel`.

The one write in this area, editing, lives on `standing-order-edit` and has its own contract.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto, with `Roboto Mono` for the amount,
masked account and execution figures so values align down each card. The currency badge uses
`secondaryContainer` — it labels the amount rather than qualifying it. Components reference semantic
roles, so both theme modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is the
canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/standing-order-detail/{ui,api,flow,docs}.yaml. -->
