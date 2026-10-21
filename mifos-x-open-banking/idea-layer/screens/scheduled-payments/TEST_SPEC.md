# TEST SPEC — Scheduled Payments

| Field      | Value                                   |
|------------|-----------------------------------------|
| Feature    | scheduled-payments                      |
| Source     | `screens/scheduled-payments/tests.yaml` |
| Scenarios  | 9                                       |
| Priorities | p0 3 · p1 5 · p2 1                      |
| States     | content 4 · error 2 · loading 1 · empty 1 · unsupported 1 |
| Module     | `feature/scheduled-payments`            |

---

## Coverage

Contiguous ids; all five declared states covered. TC-SP-009 closed the `unsupported` gap on
2026-08-02 as part of ST-1 — one of the three `unsupported` states (with direct-debits and
standing-orders) that had no scenario before that pass.

---

## TC-SP-009 is spec-ahead-of-source, and says so

This is the only scenario in the file describing behaviour that **does not yet exist in source**,
and the `tests.yaml` comment is precise about the split:

- **Already built:** `BankingStores.kt:377` records the OBIE U000 refusal via
  `recordIfUnsupported(AccountEndpoint.ScheduledPayments)`.
- **Not yet built:** `ScheduledPaymentsViewModel` has no `isUnsupportedForProduct()` pre-check and
  no Unsupported UI branch.
- **Mirror to follow:** `DirectDebitsViewModel.kt:64` — direct-debits already ships the branch this
  screen owes (its TC-DD-010).

So the refusal is *recorded* today but not *rendered*. That is why this feature scores a source-drift
deduction in `/idea-verify-e2e`: the gap is real, declared, and has a named fix recipe
(`ui.yaml#spec_ahead_of_source`). It is an obligation `/implement` owes, not idea-layer drift to
reconcile away.

---

## TC-SP-001 — List loads and renders all pending payments

**Priority:** p0 · **State:** content

- **Given** Valid PSU access token; HSBC sandbox returns 4 scheduled payments for account 40051512345678
- **When** Screen mounts with `accountId=40051512345678`
- **Then**
  - Four cards render (HMRC Self Assessment, Westminster Council Tax, Direct Line Insurance, Amazon Payments UK)
  - Each card shows payee name, GBP amount, formatted scheduled date, `ScheduledType` chip, `CreditorAccount.Identification`, and reference
  - HMRC shows GBP 842.00, due Fri 31 Jul 2026, Execution date chip, sort code 08-32-00 12001039
  - Westminster shows GBP 198.00, due Sun 5 Jul 2026, Execution date chip, reference CTAX-JUL

Dates are asserted **with weekday** ("Fri 31 Jul 2026"). For a payment that will leave the account
on a specific day, the weekday is the part a customer actually plans around.

---

## TC-SP-002 — Loading state during the fetch

**Priority:** p0 · **State:** loading

- **Given** Slow network; API call in flight
- **When** Screen mounts
- **Then**
  - Circular progress indicator visible
  - Scheduled payments list not rendered
  - Empty and error states not visible

---

## TC-SP-003 — Empty state when no scheduled payments are pending

**Priority:** p1 · **State:** empty

- **Given** HSBC returns an empty `Data.ScheduledPayment[]` for the account
- **When** Screen mounts
- **Then**
  - Empty state renders with `schedule` icon
  - Title uses `{strings.sp_empty_title}`
  - Body uses `{strings.sp_empty_body}`
  - **Retry button not shown** in the empty state

The Retry exclusion is the same rule this screen applies three times (here, TC-SP-003; in
TC-SP-009 for `unsupported`) and inverts twice (TC-SP-004, TC-SP-006). An empty schedule is a fact
about the account, not a fetch that went wrong.

---

## TC-SP-004 — Error with Retry on 401 token expired

**Priority:** p0 · **State:** error

- **Given** Access token is expired; scheduled-payments endpoint returns 401
- **When** Screen mounts
- **Then**
  - Error state renders with `error_outline` icon
  - Title reads `{strings.sp_error_title}`
  - Retry button visible with `{strings.action_retry}` label
  - Tapping Retry re-triggers the `scheduled_payments_load` ViewModel action

---

## TC-SP-005 — Back button navigates to account-detail

**Priority:** p1 · **State:** content

- **Given** Scheduled payments rendered for account 40051512345678, reached from the account-detail Scheduled chip
- **When** User taps the back button
- **Then**
  - Navigates to account-detail
  - `accountId` parameter preserved in navigation

---

## TC-SP-006 — Error shows the consent-revoked message on 403

**Priority:** p1 · **State:** error

- **Given** Account access consent has been revoked; endpoint returns 403
- **When** Screen mounts
- **Then**
  - Error state renders
  - Error message reads "Account access consent has been revoked."
  - **Retry button visible**

⚠ **Corpus inconsistency, transcribed as declared.** This screen shows Retry on 403; its closest
sibling direct-debits explicitly hides it for the same status, with the reasoning written into the
scenario ("retry cannot help — consent must be re-authorised"). Both screens are reached from the
same account-detail chip row and fail the same way, so a customer with a revoked consent gets a
Retry button on one and not the other. product (TC-PROD-003) sits on this screen's side of the
split, home (TC-HOME-011) on direct-debits'. Worth one decision across all four rather than four
independent ones.

---

## TC-SP-007 — ScheduledType=Arrival renders an "Arrival date" chip

**Priority:** p1 · **State:** content

- **Given** HSBC returns a payment with `ScheduledType=Arrival` (SP-003: Direct Line Insurance)
- **When** Screen mounts
- **Then**
  - Direct Line Insurance card shows a chip labelled "Arrival date"
  - Chip icon is `arrow_downward`
  - Chip accessibility label references "funds arrive at" semantics
  - Execution-type cards show an "Execution date" chip with `calendar_today` icon

`Execution` and `Arrival` are genuinely different dates — when money *leaves* versus when it
*lands* — and OBIE lets the servicer choose which one it quotes. Rendering both as a generic
"date" would leave the customer unable to tell whether a bill is paid on time. The scenario
asserts all three signals (label, icon, accessibility text) so the distinction survives for a
screen-reader user too.

---

## TC-SP-008 — CreditorAccount.Identification displayed on each card

**Priority:** p2 · **State:** content

- **Given** HSBC returns scheduled payments with `CreditorAccount.Identification` populated
- **When** Screen renders payment cards
- **Then**
  - HMRC card shows "08-32-00 12001039" prefixed with `{strings.sp_account_prefix}`
  - Westminster card shows "60-23-05 20490017"
  - Field uses `labelSmall` style with `onSurfaceVariant` colour

---

## TC-SP-009 — Unsupported state on an OBIE U000 product-level refusal

**Priority:** p1 · **State:** unsupported · *spec-ahead-of-source — see above*

- **Given** OBIE returns a U000 product-level refusal for this account (e.g. a credit card); `BankingStores.kt:377` has already called `recordIfUnsupported(AccountEndpoint.ScheduledPayments)`
- **When** Screen mounts with an `accountId` whose product does not support the resource
- **Then**
  - `unsupported_scheduled_payments` renders; test tag `scheduledPayments:unsupportedState` present
  - Title reads `{strings.sp_unsupported_title}`
  - Body shows the data-driven `uiState.message` (the OBIE U000 message from `error.obieMessage()`) — **no i18n key wraps this value**
  - **No Retry button** — the refusal is a permanent product-capability decision, not a transient network failure
  - Accessibility label is `{strings.sp_unsupported_a11y}`

Same mixed-provenance rule as direct-debits TC-DD-010: static title and accessibility label from
i18n, dynamic body from the servicer. Wrapping the U000 message in a key would either discard the
bank's stated reason or invent a translation for text that arrives at runtime.

---

_Generated by /idea-feature-test-export | 2026-08-03_
