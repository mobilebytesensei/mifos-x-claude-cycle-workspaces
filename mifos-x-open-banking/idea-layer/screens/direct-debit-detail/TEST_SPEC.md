# TEST SPEC — Direct Debit Detail

| Field      | Value                                                        |
|------------|--------------------------------------------------------------|
| Feature    | direct-debit-detail                                          |
| Source     | `screens/direct-debit-detail/tests.yaml`                     |
| Scenarios  | 19                                                           |
| Priorities | high 13 · medium 6                                           |
| States     | content 12 · cancel_confirm 3 · error 2 · loading 1 · empty 1 |
| Module     | _none yet — spec-only feature_                               |

> No source module exists. These are **forward specs** derived from the feature's idea-layer
> siblings. The sibling `direct-debits` list feature **does** ship (`feature/direct-debits`), and
> this screen's data comes from its repository — see TC-DDD-019.

---

## Coverage

| State          | Scenarios | Covered |
|----------------|-----------|---------|
| loading        | 1  | TC-DDD-001 |
| content        | 12 | TC-DDD-002 … -011, -015, -019 |
| cancel_confirm | 3  | TC-DDD-012, -013, -014 |
| error          | 2  | TC-DDD-016, -017 |
| empty          | 1  | TC-DDD-018 |

All five states covered.

---

## The screen has no endpoints of its own

TC-DDD-019 is the fact the rest of the spec hangs off: `GET` detail and `DELETE` cancel were
live-verified as 404 on OBP and dropped. Everything on this screen is **derived**:

| Surface | Derived from |
|---------|--------------|
| The mandate itself | `listMandates(bankId, accountId).firstOrNull { it.id == mandateId }` |
| Merchant name | transaction description (TC-DDD-003) |
| Mandate reference | `DD-{initials}-{first collection yyyyMMdd}` (TC-DDD-007) |
| Payment history | the `TXN_TYPE=DD` transaction set (TC-DDD-009) |
| Cancellation | a local `direct_debit_cancellations` record (TC-DDD-014) |

That is a legitimate way to ship a detail view over an API that has none. It also means the screen
can show a state the bank does not agree with — which is the unresolved conflict below.

---

## Unresolved — TC-DDD-014 contradicts TC-DDD-015

These two scenarios cannot both pass as written.

**TC-DDD-014** says confirming a cancel writes to `direct_debit_cancellations` in the local cache,
re-derives the mandate as Cancelled, and issues **no server DELETE** because OBP exposes no cancel
endpoint at any version.

**TC-DDD-015** says the UI must **not** present the mandate as cancelled when the servicer did not
honour it — and under a read-only AISP consent, the servicer never does.

TC-DDD-014's local-only cancellation *is* the case TC-DDD-015 forbids. Not settled here, because
this is a product decision rather than a rendering detail: either the local cancel is honest
enough to keep (in which case TC-DDD-015 needs narrowing to a specific failure the app can
detect), or the cancel affordance should not ship against a read-only consent (in which case
TC-DDD-002's `ddd_cancel_button`, TC-DDD-005, TC-DDD-012, -013 and -014 all change). Flagged for
`/idea-sync` rather than resolved by picking a record.

The customer-facing stake is plain: a mandate shown as Cancelled that still collects money next
month is worse than no cancel button at all.

---

## TC-DDD-001 — Loading state shows the detail skeleton

**Priority:** medium · **State:** loading

- **Given** `DirectDebitsRepository.listMandates()` is resolving (`initial_state: loading`)
- **When** Screen mounts
- **Then**
  - `ddd_loading_skeleton` visible with `role: progressbar` and label "Loading mandate details"
  - No hero, cards or cancel control rendered
  - Reduced-motion preference substitutes `static_placeholder`

---

## TC-DDD-002 — Content state renders hero, details, history and cancel

**Priority:** high · **State:** content

- **Given** An active mandate resolves from the derived `TXN_TYPE=DD` set
- **When** Screen renders
- **Then**
  - Top app bar shows "Direct Debit" with an `arrow_back` icon and **no** actions; no bottom nav
  - `ddd_merchant_hero` renders name, status chip, amount and frequency
  - `ddd_mandate_details_card` and `ddd_payment_history_card` visible
  - `ddd_cancel_button` visible because the mandate is active
  - The body scrolls vertically

---

## TC-DDD-003 — Merchant name comes from the transaction description, never the account holder

**Priority:** high · **State:** content

- **Given** A mandate derived from collection history
- **When** `ddd_merchant_name` renders
- **Then**
  - The name is the derived merchant from the transaction description
  - The signed-in user's login username is never rendered as the merchant

The negative assertion names a specific past failure, not a hypothetical. Deriving a payee from
transaction data has an obvious wrong answer close at hand — the other party on the record is the
customer themselves.

---

## TC-DDD-004 — Status chip is bound and resolves its tokens from the variant

**Priority:** high · **State:** content

- **Given** A mandate with `isActive` true
- **When** `ddd_mandate_status_badge` renders
- **Then**
  - `label` resolves from `mandate.statusLabel` and `variant` resolves to `active`
  - Container and icon come from `design-tokens.yaml`, not a hardcoded `primaryContainer`
  - Active renders in `primary` with `check_circle`; no green hue is used

---

## TC-DDD-005 — Cancelled mandate flips the chip and hides the cancel control

**Priority:** high · **State:** content

- **Given** A mandate with `isActive` false
- **When** Screen renders
- **Then**
  - `ddd_mandate_status_badge` variant resolves to `inactive` with the cancel icon
  - `ddd_cancel_button` is **NOT** rendered
  - `ddd_next_payment_value` renders an em dash

All three follow from one flag, and asserting them together is what catches a partial
implementation — a cancelled mandate still offering a cancel button, or still predicting a next
payment date, reads as if the cancellation did not take.

---

## TC-DDD-006 — Detail rows fall back to an em dash rather than blank

**Priority:** medium · **State:** content

- **Given** A mandate whose reference and start date cannot be derived
- **When** `ddd_mandate_details_card` renders
- **Then**
  - `ddd_mandate_ref_value` renders an em dash
  - `ddd_start_date_value` renders an em dash
  - No row renders as empty or "null"

Unavoidable on a derived screen: some fields simply have no source. An em dash says "not known";
a blank row says "nothing here", and `null` says the app is broken.

---

## TC-DDD-007 — Mandate reference follows the derived format

**Priority:** medium · **State:** content

- **Given** A mandate with a first observed collection
- **When** `ddd_mandate_ref_value` renders
- **Then**
  - The value follows `DD-{initials}-{first collection yyyyMMdd}`
  - It renders in a monospace face
  - The value is stable across reloads for the same mandate

Stability is the assertion that carries weight. This reference is synthesised by the app, and a
customer may quote it to their bank — a value that changes between reloads is worse than none.
Note it is also **not** the bank's reference, which no screen currently discloses.

---

## TC-DDD-008 — Linked-account resolution never blocks the screen

**Priority:** high · **State:** content

- **Given** `AccountsRepository.accountDetail()` fails or returns no label
- **When** `ddd_account_value_group` renders
- **Then**
  - `ddd_account_name` falls back to the account type, then to the literal "Account"
  - `ddd_account_number` still shows the last four alphanumerics prefixed with `••••`
  - The screen stays in Content — account resolution is best-effort only

A secondary lookup taking down a primary screen is a common failure; this scenario rules it out
explicitly. The masked number survives the fallback because it comes from the mandate, not from
the failed lookup.

---

## TC-DDD-009 — Recent payments render newest first with signed amounts

**Priority:** medium · **State:** content

- **Given** The mandate has observed collections
- **When** `ddd_history_list` renders
- **Then**
  - Rows appear newest first
  - Each row shows a date label and a signed amount in the form `-{symbol}{value}`
  - No per-payment status is rendered — every row is a booked collection

---

## TC-DDD-010 — Empty collection history states so plainly

**Priority:** medium · **State:** content

- **Given** The mandate has no observed collections
- **When** `ddd_history_list` renders
- **Then**
  - "No payments collected yet." is shown
  - The card still renders with its header and View all link

An empty history inside a content state, not an empty *screen* state — correct, since a mandate
set up but not yet collected is a real and unremarkable situation.

---

## TC-DDD-011 — View all opens the account's transaction history

**Priority:** medium · **State:** content

- **Given** Content state
- **When** User taps `ddd_history_view_all_link`
- **Then**
  - `onViewAllPayments` fires and the app navigates to `transactions`
  - The list is filtered to collections from this direct-debit originator

---

## TC-DDD-012 — Cancel opens a confirmation dialog without touching the mandate

**Priority:** high · **State:** cancel_confirm

- **Given** Content state with an active mandate
- **When** User taps `ddd_cancel_button` (`cancel_requested`)
- **Then**
  - `cancelDialogVisible` becomes true and `ddd_cancel_dialog` overlays the content at alpha 0.5
  - The dialog message names the merchant and reference and states it cannot be undone
  - The mandate is untouched until the confirm CTA is pressed

Naming the merchant in the dialog is what makes the confirmation meaningful — "cancel this direct
debit?" is not a decision a customer can make without knowing which one.

---

## TC-DDD-013 — Dismissing the dialog aborts with no side effects

**Priority:** high · **State:** cancel_confirm

- **Given** The cancel dialog is visible
- **When** User taps `ddd_cancel_dismiss_cta` (`cancel_dismissed`) or presses Escape
- **Then**
  - The dialog closes and `cancelDialogVisible` becomes false
  - The mandate remains active
  - No write of any kind occurs

Escape is asserted alongside the button. A dismissal path that skips the handler is exactly where
a partially-applied cancel would hide.

---

## TC-DDD-014 — Confirming records the cancellation locally and re-derives the mandate

**Priority:** high · **State:** cancel_confirm

- **Given** The cancel dialog is visible
- **When** User taps `ddd_cancel_confirm_cta` (`cancel_confirmed`)
- **Then**
  - The cancellation is written to `direct_debit_cancellations` in the local cache
  - The mandate is re-derived and flips to Cancelled
  - No server DELETE is issued — OBP exposes no cancel endpoint at any version
  - `ddd_cancel_button` disappears on the re-render

> **Conflicts with TC-DDD-015** — see "Unresolved" above.

---

## TC-DDD-015 — A cancellation that cannot be honoured must surface, not appear to succeed

**Priority:** high · **State:** content

- **Given** The AISP consent this screen reads under is read-only
- **When** A cancellation is attempted against a servicer that exposes no mandate cancellation
- **Then**
  - The failure is surfaced to the user
  - The UI does not present the mandate as cancelled when the servicer did not honour it

> **Conflicts with TC-DDD-014** — see "Unresolved" above.

---

## TC-DDD-016 — Error, no-network and unauthenticated share one recoverable shell

**Priority:** high · **State:** error

- **Given** `ScreenState` resolves to `Error`, `NoNetwork` or `Unauthenticated`
- **When** Screen renders
- **Then**
  - `ddd_error_state` renders with `cloud_off`, "Unable to load mandate" and "Check your connection and try again"
  - `ddd_retry_button` visible
  - All three states render the same shell

Same collapse as `atm-locator` TC-ATM-013, and the same caveat: "check your connection" is the
wrong instruction for an expired session.

---

## TC-DDD-017 — Retry re-derives the mandate

**Priority:** high · **State:** error

- **Given** Error state is displayed
- **When** User taps `ddd_retry_button` (`retry`)
- **Then**
  - `DirectDebitDetailViewModel.onRetry()` runs
  - The call reads from `direct-debits-list` and `transactions`
  - State transitions error → loading → content on success

---

## TC-DDD-018 — An unresolvable mandateId lands on the empty state with a way back

**Priority:** high · **State:** empty

- **Given** The `mandateId` no longer resolves in the derived set (already cancelled or expired)
- **When** Screen renders
- **Then**
  - `event_busy` icon, "Mandate not available" and the cancelled-or-expired message visible
  - `ddd_empty_back_button` visible; tapping it returns to `direct-debits`
  - This is distinct from the error state, which offers Retry instead

The right split. A mandate that no longer exists will not appear on the next attempt, so offering
Retry would invite the customer to keep asking a question with a settled answer.

---

## TC-DDD-019 — No direct-debit detail or cancel endpoint is called

**Priority:** high · **State:** content

- **Given** `GET` detail and `DELETE` cancel are live-verified 404 on OBP and dropped
- **When** The screen loads and the cancel flow is completed
- **Then**
  - The mandate is located via `listMandates(bankId, accountId).firstOrNull { it.id == mandateId }`
  - Cancellation is local-only
  - `DirectDebitsRepository` and `AccountsRepository` are the only injected dependencies

---

## Traceability

| Action | Scenario | Server call |
|--------|----------|:-----------:|
| `cancel_requested` | TC-DDD-012 | none |
| `cancel_dismissed` | TC-DDD-013 | none |
| `cancel_confirmed` | TC-DDD-014 | **none** (local write) |
| `ddd_history_view_all_link` | TC-DDD-011 | none — navigation |
| `retry` | TC-DDD-017 | re-reads list + transactions |

No action on this screen issues a write to the bank.

---

_Generated by /idea-feature-test-export | 2026-08-04_
