# TEST SPEC — Standing Orders

| Field      | Value                                |
|------------|--------------------------------------|
| Feature    | standing-orders                      |
| Source     | `screens/standing-orders/tests.yaml` |
| Scenarios  | 14                                   |
| Priorities | p0 2 · p1 8 · p2 4                   |
| States     | content 7 · error 4 · loading 1 · empty 1 · unsupported 1 |
| Module     | `feature/standing-orders`            |

---

## Coverage

Contiguous ids; all five declared states covered. TC-SO-014 closed the `unsupported` gap on
2026-08-02 (ST-1) — the third of the three `unsupported` states, with direct-debits and
scheduled-payments.

This is the most thoroughly specified list screen in the corpus: four distinct error codes, a
dedicated accessibility scenario, and three scenarios on frequency decoding alone.

---

## Frequency decoding is the domain problem this screen exists to solve

OBIE encodes recurrence as an opaque string — `IntrvlMnthDay:01:01`, `IntrvlWkDay:01:5`. Showing
that to a customer is not showing them anything. Three scenarios cover the decode from both ends:

| Scenario | Input | Expected |
|---|---|---|
| TC-SO-001 | `IntrvlMnthDay:01:01` | "Monthly on the 1st" |
| TC-SO-009 | `IntrvlWkDay:01:5` | "Weekly every Friday" |
| TC-SO-013 | `IntrvlMnthDay:02:10` (unmapped) | **the raw code, verbatim** |

TC-SO-013 is the one worth defending. OBIE's frequency vocabulary is larger than any decoder
covers, and the graceful-degradation choice — render the raw string rather than blank, "Unknown",
or a guess — keeps a real recurrence visible even when the app cannot phrase it. A blank frequency
row on a recurring payment is strictly worse than an ugly one.

---

## TC-SO-001 — List loads and renders all standing orders

**Priority:** p0 · **State:** content

- **Given** Valid PSU access token; HSBC sandbox returns 5 standing orders (4 Active, 1 Inactive) for account 40051512345678
- **When** Screen mounts with `accountId=40051512345678`
- **Then**
  - Five cards render (Jameson Lettings, ISA Saver, PureGym, Oxfam GB, Marcus Savings)
  - Each card shows payee name, status badge, GBP amount, human-readable frequency, next payment date, sort-code/account, and payment reference
  - Summary row reads "4 Active · 1 Inactive"
  - Frequency codes mapped to human labels (`IntrvlMnthDay:01:01` → "Monthly on the 1st", `IntrvlWkDay:01:5` → "Weekly every Friday")

---

## TC-SO-002 — Loading state during the fetch

**Priority:** p0 · **State:** loading

- **Given** Slow network; API call in flight
- **When** Screen mounts
- **Then**
  - Circular progress indicator visible
  - Standing orders list and summary row not rendered
  - Progress indicator `accessibility_label` reads "Loading standing orders"

---

## TC-SO-003 — Empty state when no standing orders are set up

**Priority:** p1 · **State:** empty

- **Given** HSBC returns an empty `Data.StandingOrder[]` for the account
- **When** Screen mounts
- **Then**
  - Empty state renders with `autorenew` icon
  - Title "No standing orders"
  - Body "No standing orders are set up for this account."

---

## TC-SO-004 — Error with Retry on 401 token expired

**Priority:** p1 · **State:** error

- **Given** Access token is expired; standing-orders endpoint returns 401
- **When** Screen mounts
- **Then**
  - Error state renders with `error_outline` icon
  - Title "Could not load standing orders"
  - Message "Session expired. Please log in again."
  - Retry button visible with label "Retry"
  - Tapping Retry re-triggers `LoadStandingOrders` (`RetryLoad` ViewModel action)

---

## TC-SO-005 — Back button navigates to account-detail

**Priority:** p1 · **State:** content

- **Given** Standing orders rendered for account 40051512345678, reached from the account-detail StandingOrders chip
- **When** User taps the back button
- **Then**
  - `NavigationEvent.Back` emitted to the NavController
  - Navigates to account-detail

---

## TC-SO-006 — Inactive order renders a secondary badge and its final payment date

**Priority:** p1 · **State:** content

- **Given** HSBC returns SO-004 (Oxfam GB, Inactive, `FinalPaymentDateTime=2025-12-28`)
- **When** Screen mounts
- **Then**
  - SO-004 card renders with badge `variant='secondary'` and text "Inactive"
  - `FinalPaymentDateTime` row visible: "Final: 28 Dec 2025"
  - `NextPaymentDateTime` row **not shown** (null value)

An inactive order swaps *which date it shows*, not just its badge colour. "Next payment" on a
finished arrangement would be a claim about future money movement that will not happen — so the row
is removed rather than rendered empty or zeroed.

Note this screen uses `secondary` for inactive where direct-debits (TC-DD-001) explicitly chose
`outline` over `secondary` for the same concept. Two adjacent list screens, two treatments of an
inactive row. Recorded as an observation; both are transcribed as declared.

---

## TC-SO-007 — 403 consent revoked shows a distinct message from 401

**Priority:** p1 · **State:** error

- **Given** AISP consent has been revoked; endpoint returns 403
- **When** Screen mounts
- **Then**
  - Message "Account access consent has been revoked."
  - Title "Could not load standing orders"
  - Retry button visible (user can attempt to re-consent and retry)

⚠ Third instance of the corpus-wide 403 split. This screen and scheduled-payments (TC-SP-006) and
product (TC-PROD-003) show Retry on 403; direct-debits (TC-DD-006) and home (TC-HOME-011) hide it.
Standing-orders states its reasoning explicitly — the customer may re-consent, then retry — which
is the strongest version of the case, but it is still the opposite decision to the screen sitting
next to it in the same chip row.

---

## TC-SO-008 — 429 rate limited shows a rate-limit specific message

**Priority:** p2 · **State:** error

- **Given** HSBC sandbox rate limit exceeded; endpoint returns 429
- **When** Screen mounts
- **Then**
  - Message "Too many requests. Please wait a moment and try again."
  - Retry button visible

---

## TC-SO-009 — Weekly frequency code decodes to "Weekly every Friday"

**Priority:** p1 · **State:** content

- **Given** HSBC returns SO-005 with `Frequency=IntrvlWkDay:01:5`
- **When** Screen mounts
- **Then**
  - SO-005 frequency row reads "Weekly every Friday"
  - Frequency accessibility label reads "Frequency: Weekly every Friday"

---

## TC-SO-010 — Pull-to-refresh re-triggers the load

**Priority:** p2 · **State:** content

- **Given** Screen already showing content with standing orders
- **When** User pulls down on the list
- **Then**
  - Loading indicator appears
  - `LoadStandingOrders` re-triggered
  - Updated list renders on completion

---

## TC-SO-011 — All interactive elements and key data fields carry accessibility labels

**Priority:** p2 · **State:** content

- **Given** Screen in content state with 3 standing orders
- **When** TalkBack/VoiceOver traverses the screen
- **Then**
  - Back button announces "Navigate back to Account Detail"
  - Each payee name announces "Payee: {name}"
  - Each amount announces "Next payment: {amount} {currency}"
  - Each status badge announces "Status: Active" or "Status: Inactive"
  - Each sort-code announces "Sort code / Account: {identification}"
  - Each next-date row announces "Next payment date: {date}"
  - Each payment reference row announces "Payment reference: {reference}"
  - Card container announces "Standing order for {payee name}" for TalkBack grouping
  - Retry button (error state) announces "Retry loading standing orders"

The only dedicated accessibility scenario in the corpus, and the card-grouping assertion is why it
earns its place: without it, a screen reader reads seven unlabelled fragments per card and a
customer with five orders hears thirty-five values with no indication of which payee each belongs
to. Every label here is a *prefix* ("Payee:", "Next payment date:") rather than a bare value, which
is what makes the sequence parseable by ear.

This screen scores against project findings N-1 and N-3 (164 interactive components with no
keyboard-focusability signal, 28 with no accessible name). Those are separate concerns from
announced text — this scenario covers what is *said*, not what is *reachable*.

---

## TC-SO-012 — Network error shows the correct message and Retry

**Priority:** p1 · **State:** error

- **Given** Device has no network connectivity; Ktorfit throws `IOException`
- **When** Screen mounts
- **Then**
  - Error state renders with `error_outline` icon
  - Title "Could not load standing orders"
  - Message "No network connection. Check your connection and retry."
  - Retry button visible with label "Retry"
  - Tapping Retry re-triggers `LoadStandingOrders`

---

## TC-SO-013 — Unknown OBIE frequency code falls back to the raw string

**Priority:** p2 · **State:** content

- **Given** HSBC returns a standing order with `Frequency='IntrvlMnthDay:02:10'` (not in the decoder mapping)
- **When** Screen mounts
- **Then**
  - Frequency row displays the raw OBIE code "IntrvlMnthDay:02:10" (`fallback={Frequency}`)
  - No crash or empty label; the decoder falls back gracefully
  - Frequency accessibility label reads "Frequency: IntrvlMnthDay:02:10"

---

## TC-SO-014 — Unsupported state when the capability registry refuses the call

**Priority:** p1 · **State:** unsupported

- **Given** The servicer does not expose standing orders for this account type; the ViewModel receives `StandingOrdersUiState.Unsupported` with a capability-refused message
- **When** Screen mounts with an `accountId` for an account that does not support standing orders
- **Then**
  - Unsupported empty-state (`standingOrders:unsupportedState`) renders with `info_outline` icon and the **info** variant
  - Title "Standing orders unavailable" (`{strings.standing_orders_unsupported_title}`)
  - Body renders the runtime message from `StandingOrdersUiState.Unsupported(message)` — not a static i18n key
  - **No Retry button** — the capability registry refused outright; this is not a transient network or auth failure

The `info_outline` icon and info variant match product's empty state (TC-PROD-005) rather than any
error state — the correct read, since an account type without standing orders is a fact about the
product, not a fault.

---

_Generated by /idea-feature-test-export | 2026-08-03_
