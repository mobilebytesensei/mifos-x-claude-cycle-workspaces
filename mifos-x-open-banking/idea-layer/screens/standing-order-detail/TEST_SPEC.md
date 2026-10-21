# TEST SPEC — Standing Order Detail

| Field      | Value                                             |
|------------|---------------------------------------------------|
| Feature    | standing-order-detail                             |
| Source     | `screens/standing-order-detail/tests.yaml`        |
| Scenarios  | 18                                                |
| Priorities | high 11 · medium 7                                |
| States     | content 14 · error 2 · loading 1 · empty 1        |
| Module     | _none yet — spec-only feature_                    |

> No source module exists. These are **forward specs** derived from the feature's idea-layer
> siblings. The sibling `standing-orders` list feature **does** ship
> (`feature/standing-orders`).

---

## Coverage

| State   | Scenarios | Covered |
|---------|-----------|---------|
| loading | 1  | TC-SOD-001 |
| content | 14 | TC-SOD-002 … -014, -018 |
| error   | 2  | TC-SOD-015, -016 |
| empty   | 1  | TC-SOD-017 |

All four states covered.

---

## A detail screen with no detail endpoint and no controls that work

TC-SOD-018: `GET` detail, `POST` pause, `POST` resume and `DELETE` are **all live-verified 404 on
OBP and dropped**. So this screen derives everything and can change nothing:

| Surface | Source |
|---------|--------|
| The order | `StandingOrdersRepository.detail()` over the derived/created set |
| Executions | `deriveExecutions` over `TXN_TYPE=SO` transaction history |
| Pause / Resume | **snackbar only** — TC-SOD-013 |
| Cancel | **snackbar only** — TC-SOD-014 |

Both buttons in `sod_action_row` announce "coming soon". Together with
`standing-order-create` TC-SOC-017 — POST is the only verb the API offers — this completes the
picture: the app can create a recurring debit and can never pause, amend or cancel it.

That is honest engineering against a limited API, and the honesty needs to reach the customer at
the point of *creation*, not only here. A create screen whose end-date field says "leave empty to
pay until cancelled" (TC-SOC-012) sits directly upstream of two disabled cancel buttons.

---

## Four scenarios pin what cannot be known

The derived data model means some fields have no source at all, and the spec says so rather than
inventing values:

| Absence | Scenario |
|---------|----------|
| No IBAN row, no beneficiary bank row | TC-SOD-005 |
| Date rows omitted when no execution has been observed | TC-SOD-007 |
| Final date is always "Ongoing" | TC-SOD-008 |
| Every execution reads "Completed" — failures are not observable | TC-SOD-010 |

TC-SOD-010 is the one to watch. A history where every row says Completed is indistinguishable from
a history where a collection failed, because a failed standing order simply produces no
transaction to derive from. The customer sees an unbroken record of success that may be missing
entries.

---

## TC-SOD-001 — Loading state shows the detail skeleton

**Priority:** medium · **State:** loading

- **Given** `StandingOrdersRepository.detail()` is resolving (`initial_state: loading`)
- **When** Screen mounts
- **Then**
  - `sod_loading_skeleton` visible with `role: progressbar` and label "Loading standing order details"
  - No cards or action buttons rendered
  - Reduced-motion preference substitutes `static_placeholder`

---

## TC-SOD-002 — Content state renders all four cards plus the action row

**Priority:** high · **State:** content

- **Given** The order resolves from the derived/created set with observed executions
- **When** Screen renders
- **Then**
  - Top app bar shows "Standing Order" with an `arrow_back` icon and **no** actions; no bottom nav
  - `sod_recipient_card`, `sod_schedule_card`, `sod_amount_card`, `sod_history_card` and `sod_action_row` visible
  - The body scrolls vertically
  - No Edit action is present in the top bar

The absent Edit action is asserted because an edit affordance would have nothing behind it — same
reason as the two coming-soon buttons, handled the better way. An action that cannot exist is
better omitted than shipped as a snackbar.

---

## TC-SOD-003 — Recipient name never falls back to the login username

**Priority:** high · **State:** content

- **Given** The order has no counterparty name but does have an order name
- **When** `sod_recipient_name_value` renders
- **Then**
  - The fallback order is counterparty name, then order name, then the literal "Recipient"
  - The signed-in user's username is never rendered as the recipient

The same defect class `direct-debit-detail` TC-DDD-003 guards against, and the same fix. Both
screens derive a payee from records where the customer is the other party, so the wrong answer is
always within reach of a careless fallback.

---

## TC-SOD-004 — Recipient account row appears only when a masked account is available

**Priority:** medium · **State:** content

- **Given** `recipientAccount` is blank
- **When** `sod_recipient_card` renders
- **Then**
  - `sod_recipient_account_row` is not rendered
  - No empty Account label with a blank value is shown
  - When present, the value shows the last four alphanumerics in a monospace face

---

## TC-SOD-005 — IBAN and bank rows are absent because they are not observable

**Priority:** medium · **State:** content

- **Given** Content state
- **When** `sod_recipient_card` is inspected
- **Then**
  - No IBAN row renders
  - No beneficiary bank row renders
  - Only name and masked account are shown

---

## TC-SOD-006 — Schedule card renders status, frequency and the date rows

**Priority:** high · **State:** content

- **Given** An active monthly order with observed executions
- **When** `sod_schedule_card` renders
- **Then**
  - `sod_status_value` shows the status label and renders in `primary` when active
  - `sod_frequency_value` shows a human frequency (Daily / Weekly / Every 2 weeks / Monthly / Yearly)
  - `sod_next_payment_value` renders in `primary` when active
  - Status and next-payment colour come from the declared `primary` token, not a green hue

"Every 2 weeks" here where the create screen says "Fortnightly" (`standing-order-create`
TC-SOC-008). Both are unambiguous, and they are two labels for one cadence across two screens the
customer sees minutes apart.

---

## TC-SOD-007 — Date rows are conditional on observed data

**Priority:** medium · **State:** content

- **Given** An order with no observed executions and blank `lastPayment` and `nextPayment`
- **When** `sod_schedule_card` renders
- **Then**
  - `sod_first_payment_row` is not rendered (no oldest execution to derive from)
  - `sod_last_payment_row` is not rendered
  - `sod_next_payment_row` is not rendered

  - `sod_final_date_row` still renders

Note what this means for a freshly created order: the schedule card shows a frequency and a status
and **no dates at all** — not even the start date the customer chose on the create screen, which
the app knows and could show from its own local cache.

---

## TC-SOD-008 — Final date is always Ongoing

**Priority:** medium · **State:** content

- **Given** Any resolved order
- **When** `sod_final_date_value` renders
- **Then**
  - The value reads "Ongoing"
  - No end date is derived or invented — OBP data exposes none

"Always" is the problem. `standing-order-create` TC-SOC-012 lets the customer set an optional end
date and sends it as `date_expires`; this screen then tells them the order is Ongoing regardless.
For an order with an end date, that is a false statement about a commitment they deliberately
bounded — and the create screen's own local cache holds the value.

---

## TC-SOD-009 — Executions list is capped at five, newest first

**Priority:** high · **State:** content

- **Given** More than five booked `TXN_TYPE=SO` transactions exist for the order
- **When** `sod_history_list` renders
- **Then**
  - At most `MAX_EXECUTIONS` (5) rows render
  - Rows are ordered newest first
  - Each row shows a date label, the status "Completed" and an amount

Capped with no "view all" affordance specified. A monthly order older than five months has history
the customer cannot reach from here.

---

## TC-SOD-010 — Every observed execution reads Completed

**Priority:** medium · **State:** content

- **Given** Executions derived from booked `TXN_TYPE=SO` history
- **When** `sod_history_row_status` renders
- **Then**
  - Every row reads "Completed"
  - No failed or insufficient-funds status is rendered — those are not observable

> See the section above — an unbroken run of Completed rows may be hiding failures.

Given that, rendering a status column at all is questionable: a column with one possible value
conveys nothing and implies the others were checked for.

---

## TC-SOD-011 — Empty execution copy distinguishes a new order from an unobserved one

**Priority:** high · **State:** content

- **Given** An order with no executions
- **When** `sod_history_list` renders its empty copy
- **Then**
  - `isCreated` true renders "This order hasn't made a payment yet."
  - `isCreated` false renders "No payments observed yet."
  - The two cases are **not** collapsed into one message

The distinction is exactly right and it is the only place in this feature where the derived data
model is admitted in the customer's language. "Hasn't made a payment yet" is a fact about the
order; "no payments observed yet" is a fact about what the app can see.

---

## TC-SOD-012 — An execution row drills into its underlying transaction

**Priority:** high · **State:** content

- **Given** An execution row with a `transactionId`
- **When** User taps `sod_history_row`
- **Then**
  - App navigates to `transaction-detail`
  - `bankId`, `accountId` and the row's `transactionId` are passed through

---

## TC-SOD-013 — Pause/Resume states its unavailability rather than failing

**Priority:** high · **State:** content

- **Given** Content state
- **When** User taps `sod_pause_resume_button`
- **Then**
  - A one-shot snackbar "Pausing standing orders is coming soon" is emitted
  - No API call is issued — OBP has no pause or resume endpoint at any version
  - The button label toggles between Pause and Resume based on status

The label still toggles by status, so the button models a state machine it cannot drive.
Announcing beats silently failing, but a control that looks live on every render and never is
will be tapped repeatedly.

> The comparison here was to `cards` TC-CARDS-010, which made the same choice. **Removed
> 2026-08-07** — the `cards` and `card-detail` screens were deleted (OBIE has no card resource),
> so the citation no longer resolves. The reasoning stands on its own.

---

## TC-SOD-014 — Cancel states its unavailability and shows no confirmation dialog

**Priority:** high · **State:** content

- **Given** Content state
- **When** User taps `sod_cancel_button`
- **Then**
  - A one-shot snackbar "Cancelling standing orders is coming soon" is emitted
  - No confirmation dialog is shown — there is nothing to delete on OBP
  - No DELETE call is issued

Skipping the confirmation dialog is correct — a dialog for an action that cannot happen would be
theatre — and it leaves a customer who urgently wants to stop a recurring debit with a snackbar
and no next step. Neither this screen nor any other names the route that would work: contacting
the bank directly.

---

## TC-SOD-015 — Error, no-network and unauthenticated share one recoverable shell

**Priority:** high · **State:** error

- **Given** `ScreenState` resolves to `Error`, `NoNetwork` or `Unauthenticated`
- **When** Screen renders
- **Then**
  - `sod_error_state` renders with `cloud_off`, "Standing Order Not Found" and the connection-or-cancelled message
  - `sod_retry_button` visible
  - All three states render the same shell

The fourth occurrence of this three-state collapse (`atm-locator`, `direct-debit-detail`,
`send-money-amount`). Here the copy compounds it: "Standing Order Not Found" is a *found/not-found*
message shown for connectivity and session failures too.

---

## TC-SOD-016 — Retry re-derives the order and its executions

**Priority:** high · **State:** error

- **Given** Error state is displayed
- **When** User taps `sod_retry_button` (`retry`)
- **Then**
  - `StandingOrderDetailViewModel.onRetry()` runs
  - The call reads from `standing-orders-list` and `transactions`
  - State transitions error → loading → content on success

---

## TC-SOD-017 — Empty state offers a way back to the list

**Priority:** medium · **State:** empty

- **Given** `ScreenState.Empty` — no detail body
- **When** Screen renders
- **Then**
  - `sod_empty_icon`, "No details are available for this standing order." and `sod_back_to_list_button` visible
  - Tapping Go Back returns to `standing-orders` for the same account

Same split as `direct-debit-detail` TC-DDD-018: empty offers a way out, error offers a retry. The
right distinction — an order that cannot be resolved will not resolve on a second attempt.

---

## TC-SOD-018 — No standing-order detail endpoint is called

**Priority:** high · **State:** content

- **Given** `GET` detail, `POST` pause, `POST` resume and `DELETE` are all live-verified 404 on OBP and dropped
- **When** The screen loads and every control is exercised
- **Then**
  - Detail comes from `StandingOrdersRepository.detail()` over the derived/created set
  - Executions come from `deriveExecutions` over `TXN_TYPE=SO` history
  - `StandingOrdersRepository` is the only injected dependency

---

## Traceability

| Control | Scenario | Effect |
|---------|----------|--------|
| `sod_history_row` | TC-SOD-012 | navigates to `transaction-detail` |
| `sod_pause_resume_button` | TC-SOD-013 | **snackbar only** |
| `sod_cancel_button` | TC-SOD-014 | **snackbar only** |
| `sod_retry_button` | TC-SOD-016 | re-derives |
| `sod_back_to_list_button` | TC-SOD-017 | returns to list |

Two of the five controls do nothing but explain that they do nothing.

---

_Generated by /idea-feature-test-export | 2026-08-04_
