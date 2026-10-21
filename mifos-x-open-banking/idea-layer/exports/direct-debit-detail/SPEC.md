# SPEC — Direct Debit Detail

| Field         | Value                          |
|---------------|--------------------------------|
| Feature       | direct-debit-detail            |
| Flavor        | consumer                       |
| Status        | approved                       |
| Quality Score | 95                             |
| ViewModel     | DirectDebitDetailViewModel     |
| Archetype     | detail_screen                  |

---

## Overview

One direct-debit mandate in full: the originator, its status, amount and frequency, the mandate
details, recent collections, and the cancel path.

The content type is **display-ready label strings, not typed domain values** — `amountLabel`,
`frequencyLabel`, `nextPaymentLabel` and the rest arrive already formatted, with no enums. Several
carry an explicit em-dash convention for the cases where a value cannot be derived: a cancelled
mandate has no next payment, a blank reference has nothing to show. That is a deliberate choice to
keep "unknown" visually distinct from "zero" rather than rendering a misleading `£0.00` or a blank.

Cancellation is behind a confirmation dialog with a deliberately asymmetric pair of CTAs — the
destructive one is explicit ("Yes, Cancel Mandate"), the safe one is affirmative ("Keep Mandate")
rather than a bare "Cancel", which would be ambiguous on a screen where *cancel* is also the
destructive verb.

---

## Screens

| ID                  | Name                | ViewModel                  | Archetype     |
|---------------------|---------------------|----------------------------|---------------|
| direct-debit-detail | Direct Debit Detail | DirectDebitDetailViewModel | detail_screen |

**Shell:** top app bar shown, title "Direct Debit", `arrow_back` → `navigate_back`, no actions.
No bottom navigation — a pushed detail screen.

---

## Components

| ID                        | Type        | Description                                             |
|---------------------------|-------------|----------------------------------------------------------|
| ddd_root                  | stack       | Vertical container                                      |
| ddd_merchant_hero         | stack       | Originator hero block                                   |
| └ ddd_merchant_name       | text        | `merchantName`                                          |
| └ ddd_mandate_status_badge| status_chip | `{mandate.statusLabel}` — variant from `isActive`       |
| └ ddd_mandate_amount_value| text        | `amountLabel`                                           |
| └ ddd_mandate_frequency_text | text     | `frequencyLabel`                                        |
| ddd_mandate_details_card  | card        | Mandate details panel                                   |
| └ ddd_details_header      | text        | "Mandate Details"                                       |
| └ ddd_next_payment_row    | stack       | Next payment row                                        |
| &nbsp;&nbsp;└ ddd_next_payment_label | text | "Next Payment"                                    |
| &nbsp;&nbsp;└ ddd_next_payment_value | text | `nextPaymentLabel` — em dash when cancelled       |
| └ ddd_divider_1           | divider     |                                                         |
| └ ddd_account_row         | stack       | Linked account row                                      |
| &nbsp;&nbsp;└ ddd_account_label | text  | "Account"                                              |
| &nbsp;&nbsp;└ ddd_account_value_group | stack | Name + masked number                            |
| &nbsp;&nbsp;&nbsp;&nbsp;└ ddd_account_name | text | `linkedAccountName` — "Account" fallback   |
| &nbsp;&nbsp;&nbsp;&nbsp;└ ddd_account_number | text | `linkedAccountMasked`                     |
| └ ddd_divider_2           | divider     |                                                         |
| └ ddd_mandate_ref_row     | stack       | Mandate reference row                                   |
| &nbsp;&nbsp;└ ddd_mandate_ref_label | text | "Mandate Ref"                                      |
| &nbsp;&nbsp;└ ddd_mandate_ref_value | text | `mandateReference` — em dash when blank            |
| └ ddd_divider_3           | divider     |                                                         |
| └ ddd_start_date_row      | stack       | Start date row                                          |
| &nbsp;&nbsp;└ ddd_start_date_label | text | "Start Date"                                        |
| &nbsp;&nbsp;└ ddd_start_date_value | text | `startDateLabel` — em dash when underivable         |
| ddd_payment_history_card  | card        | Recent collections panel                                |
| └ ddd_history_header_row  | stack       | Header row                                              |
| &nbsp;&nbsp;└ ddd_history_header | text | "Recent Payments"                                     |
| &nbsp;&nbsp;└ ddd_history_view_all_link | link | "View all" → transactions                      |
| └ ddd_history_list        | list        | `recentPayments`                                        |
| &nbsp;&nbsp;└ ddd_history_row | list_item | One collection — `one_line` density (date + amount)   |
| &nbsp;&nbsp;&nbsp;&nbsp;└ ddd_history_row_date | text | Collection date                        |
| &nbsp;&nbsp;&nbsp;&nbsp;└ ddd_history_row_amount | text | Signed amount                        |
| ddd_cancel_button         | button      | "Cancel Mandate" — opens the dialog                     |
| ddd_cancel_dialog         | dialog      | "Cancel Direct Debit?"                                  |
| └ ddd_cancel_confirm_cta  | button      | "Yes, Cancel Mandate" — destructive                     |
| └ ddd_cancel_dismiss_cta  | button      | "Keep Mandate" — affirmative, not a bare "Cancel"       |
| ddd_loading_skeleton      | skeleton    | Loading placeholder                                     |
| ddd_error_state           | stack       | Error container                                         |
| └ ddd_error_icon          | icon        | `cloud_off`                                             |
| └ ddd_error_title         | text        | "Unable to load mandate"                                |
| └ ddd_error_message       | text        | "Check your connection and try again."                  |
| └ ddd_retry_button        | button      | Retry                                                   |
| ddd_empty_state           | stack       | Mandate unavailable container                           |
| └ ddd_empty_icon          | icon        | `event_busy`                                            |
| └ ddd_empty_title         | text        | "Mandate not available"                                 |
| └ ddd_empty_message       | text        | "This direct debit could not be found."                 |
| └ ddd_empty_back_button   | button      | "Back to Direct Debits"                                 |

---

## States

Initial state: `loading`. Seven states — the canonical four plus a confirm overlay and two
connectivity states.

| State           | Rendering                                                    |
|-----------------|---------------------------------------------------------------|
| loading         | `ddd_loading_skeleton`                                       |
| content         | Hero, details card, payment history, Cancel Mandate          |
| cancel_confirm  | `ddd_cancel_dialog` over the content — **nothing sent yet**  |
| empty           | `event_busy` — mandate not found                             |
| error           | `cloud_off` + retry                                          |
| no_network      | Error treatment                                              |
| unauthenticated | Error treatment                                              |

---

## State Model

**ViewModel:** `DirectDebitDetailViewModel`.

**Constructor:** `bankId: String`, `accountId: String`, `mandateId: String` — all defaulting to
`""`. Three ids, because a mandate is addressed per bank *and* per account.

**Flows:** `uiState: StateFlow<ScreenState<DirectDebitDetailContent>>`, default `ScreenState.Loading`.

**Content — `DirectDebitDetailContent`** (display-ready labels; no typed enums)

| Field                 | Type                          | Note                                    |
|-----------------------|-------------------------------|------------------------------------------|
| `merchantName`        | `String`                      |                                          |
| `statusLabel`         | `String`                      |                                          |
| `isActive`            | `Boolean`                     | Drives the status chip variant           |
| `amountLabel`         | `String`                      |                                          |
| `frequencyLabel`      | `String`                      |                                          |
| `nextPaymentLabel`    | `String`                      | **em dash** when cancelled/underivable   |
| `linkedAccountName`   | `String`                      | Best-effort; "Account" fallback          |
| `linkedAccountMasked` | `String`                      |                                          |
| `mandateReference`    | `String`                      | **em dash** when blank                   |
| `startDateLabel`      | `String`                      | **em dash** when underivable             |
| `recentPayments`      | `List<DirectDebitPaymentRow>` |                                          |
| `cancelDialogVisible` | `Boolean`                     | Drives `cancel_confirm`                  |

---

## Navigation

| From                | To            | Trigger                        | Type |
|---------------------|---------------|--------------------------------|------|
| direct-debit-detail | transactions  | `ddd_history_view_all_link`    | push |
| direct-debit-detail | direct-debits | back, or `ddd_empty_back_button` | pop |

---

## API Endpoints

`api: []` — **this screen makes no network call of its own.**

OBP has no direct-debit detail endpoint and no cancel endpoint at any version; the originally
specified `GET`/`DELETE /direct-debit/{id}` were live-verified 404 and dropped on 2026-06-11.

Instead:

| Kind            | Source                                                              |
|-----------------|---------------------------------------------------------------------|
| derived read    | `DirectDebitsRepository.listMandates(...).firstOrNull { it.id == mandateId }` |
| derived read    | `AccountsRepository.accountDetail(...)` — best-effort, non-blocking  |
| local mutation  | `DirectDebitsRepository.cancel(...)` — **local only, never sent**    |

**Cancellation is local.** Confirming the dialog writes to the Room JSON cache and re-fetches; the
mandate flips to `CANCELLED` and the next-payment date clears. It persists across restarts and the
bank is never told. See `API.md` for the full contract and why no server cancel exists.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto, with `Roboto Mono` for amounts and
the masked account number so digits align. The status chip follows the design system's role mapping —
`error` only where the mandate is actually cancelled. Components reference semantic roles, so both
theme modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/direct-debit-detail/{ui,api,flow,docs}.yaml. -->
