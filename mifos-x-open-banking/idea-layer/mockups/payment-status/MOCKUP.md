# Payment Status — Mockup Specification

> Source: `screens/payment-status/*.yaml` + `design-system/DESIGN.md` + `design-tokens.yaml`
> Design System: Open Banking — Trust Blue (Material 3, seed `#266489`)
> Screen: single-column detail, bottom-nav visible, top-app-bar with back
> Copy: every quoted string is VERBATIM from `_strings/strings.yaml` unless marked UNSOURCED.

---

## Per-Ladder Visual Treatment

Payment status is not a single screen — it has four distinct rendering regimes determined by
the `paymentFamily` nav param. The chip, the notes, and the available actions all change.

### Ladder 1: single (domestic-payment, international-payment)

The PSU submitted a real-money transfer and is waiting for settlement.

| Phase     | Status | Disposition        | Chip treatment                         | Actions shown            |
|-----------|--------|--------------------|----------------------------------------|--------------------------|
| In flight | ACSP   | in_progress        | slate secondaryContainer, schedule icon| refresh_button           |
| Settled   | ACCC   | terminal_success   | trust-blue primaryContainer, check_circle | (none)              |
| Rejected  | RJCT   | terminal_failure   | error errorContainer, error icon       | new_payment_button       |

`in_progress_note` is visible while disposition is in_progress:
"Your bank has accepted this payment. The money has not left your account yet."

Settlement is BATCHED on five-minute boundaries — ACSP can legitimately persist for minutes on
a payment that will settle. The note must not imply a problem, and must not imply a settlement
deadline the API does not disclose. The polling cadence (3s → 30s) is sized for that window and
must not be shortened to feel responsive.

### Ladder 2: domestic_deferred (domestic-scheduled, domestic-standing-order)

The PSU set up an instruction that will execute at a future date. PDNG arrives first; INCO is
the terminal state. Both map to `instruction_established`.

| Status | Disposition            | Chip treatment                                          |
|--------|------------------------|---------------------------------------------------------|
| PDNG   | instruction_established | hue-less surfaceVariant, onSurfaceVariant, event_repeat |
| INCO   | instruction_established | same                                                    |

`instruction_established_note` is visible. The catalogue holds ONE value covering both rails:
"This instruction is set up with your bank. No payment has been made yet — the first one goes out on its due date."
A per-rail split of this note is UNSOURCED — there is no second key for it.

No refresh_button. No new_payment_button. Polling stops immediately on first read (INCO is stable).

The chip label must name the INSTRUCTION, never the payment. UNSOURCED — no catalogue key
exists for any chip label; the label is ViewModel-derived. FORBIDDEN label substrings: paid,
sent, complete, completed, successful, any past-tense amount.

### Ladder 3: international_deferred (international-scheduled, international-standing-order)

Same as domestic_deferred but the first read is already INCO — this ladder never emits PDNG.
Treatment is identical to ladder 2. The international deferred screen never enters a polling state.

### Ladder 4: vrp (domestic-vrp)

A recurring variable-payment mandate. The consent stays AUTH forever; the payment resource
cycles ACSP → ACCC on each execution.

| Phase      | Status | Disposition        | Chip treatment                          | Actions                          |
|------------|--------|--------------------|-----------------------------------------|----------------------------------|
| Settling   | ACSP   | in_progress        | slate secondaryContainer, schedule icon | refresh_button                   |
| Settled    | ACCC   | terminal_success   | trust-blue primaryContainer, check_circle | (none)                        |
| Revoked    | U011   | (MandateRevoked)   | hue-less surfaceVariant, block icon     | new-mandate button — UNSOURCED   |

VRP note: `ExpectedExecutionDateTime = CreationDateTime + 30s` on every corpus payment (all 8
observed). A 30-second settling indicator is legitimate here and ONLY here.

When 400 U011 arrives on the consent GET: this is NOT an error. The mandate was revoked. Render
from the local mandate record using the neutral (revoked) treatment. Do not show the error_state
layout. Offer a new-mandate path.

UNSOURCED: `payment-status` declares four error types and none is `MandateRevoked`. No chip
label, note or CTA copy for this ladder exists in `_strings/strings.yaml`. Do not render
finished-looking copy here — the keys must be added first.

---

## Disposition Colour Semantics (from DESIGN.md)

All four dispositions must carry their icon AND text label. Colour alone is never the signal
(WCAG 1.4.1). The three tonal contrast figures sit within 0.041 of each other — no disposition
shouts louder than the others.

| Disposition             | Container (light)     | On-container (light) | Icon          | Contrast | Token role           |
|-------------------------|-----------------------|----------------------|---------------|:--------:|----------------------|
| in_progress             | `#D3E5F5`             | `#384956`            | schedule      | 7.22:1   | secondaryContainer   |
| terminal_success        | `#C9E6FF`             | `#004B6F`            | check_circle  | 7.27:1   | primaryContainer     |
| terminal_failure        | `#FFDAD6`             | `#93000A`            | error         | 7.24:1   | errorContainer       |
| instruction_established | `#DDE3EA`             | `#41474D`            | event_repeat  | 7.28:1   | surfaceVariant       |

Dark mode counterparts:

| Disposition             | Container (dark) | On-container (dark) |
|-------------------------|------------------|---------------------|
| in_progress             | `#384956`        | `#D3E5F5`           |
| terminal_success        | `#004B6F`        | `#C9E6FF`           |
| terminal_failure        | `#93000A`        | `#FFDAD6`           |
| instruction_established | `#41474D`        | `#C1C7CE`           |

`instruction_established` is deliberately hue-less (surfaceVariant/onSurfaceVariant). The same
neutral the system uses for unsigned running balances. A hue-less chip makes no claim about
money — which is exactly the claim available here. `event_repeat` is the icon (not check_circle,
not schedule — neither is true of a dormant future instruction).

`terminal_failure` uses error-red to mark a terminal outcome, NOT to assign blame. A rejected
payment must not be worded as a user error — no "invalid", no "you", no correction affordance
implying the customer mis-typed. The bank declined; the customer's data was accepted.

A settled payment uses trust-blue (`primaryContainer`), NOT green. Green/red would be
colour-blind-unsafe and celebratory in tone. Calm, regulated finance.

---

## Component Hierarchy

### Loading state

```
PaymentStatusScreen (Fill, Auto Layout Vertical)
  TopAppBar (Fill × 64dp)
    ├─ back_button (icon_button, arrow_back, 48×48dp)
    └─ Title "Payment status" (titleLarge)
  Body (Fill, Auto Layout Vertical, padding=16dp, gap=16dp)
    └─ CircularProgressIndicator (48dp, primary colour, centred)
  BottomNavBar (Fill × 80dp)
```

### Content state

```
PaymentStatusScreen (Fill, Auto Layout Vertical)
  TopAppBar (Fill × 64dp)
    ├─ back_button (icon_button, arrow_back, 48×48dp)
    └─ Title "Payment status" (titleLarge)
  Body (Fill, Auto Layout Vertical, padding=16dp, gap=16dp, scrollable)
    ├─ status_chip (AssistChip, Fill × Hug)
    │     icon: {dispositionIcon}
    │     label: {statusLabel}
    │     container: {disposition container colour}
    │     labelColor: {disposition on-container colour}
    │     radius: full (pill)
    │
    ├─ payment_summary (Card, Fill, radius=12dp, container=surfaceContainerLow, elevation=1)
    │   Auto Layout Vertical, padding=16dp, gap=8dp
    │     ├─ Row: "Amount"   [row labels UNSOURCED — no keys] / amountLabel (titleMedium, mono, onSurface)
    │     ├─ Row: "To"       [UNSOURCED] / creditorName (bodyMedium, onSurface)
    │     ├─ Row: "From"     [UNSOURCED] / debtorAccountLabel (bodyMedium, onSurface)
    │     ├─ Row: "Reference"[UNSOURCED] / referenceLabel (bodyMedium, onSurface) [nullable — hidden if absent]
    │     └─ Row: "Submitted"[UNSOURCED] / submittedAtLabel (bodyMedium, onSurface)
    │
    ├─ in_progress_note (Text, Fill, bodyMedium, onSurfaceVariant)
    │     Visible only: disposition == in_progress
    │     Content: "Your bank has accepted this payment. The money has not left your account yet."
    │
    ├─ instruction_established_note (Text, Fill, bodyMedium, onSurfaceVariant)
    │     Visible only: disposition == instruction_established
    │     Content: "This instruction is set up with your bank. No payment has been made yet — the first one goes out on its due date."
    │
    ├─ refresh_button (Button tonal, Fill × 48dp, radius=full)
    │     Visible only: disposition == in_progress
    │     Label: "Refresh"
    │
    └─ new_payment_button (Button filled, Fill × 48dp, container=primary, radius=full)
          Visible only: disposition == terminal_failure
          Label: "Make a new payment"
  BottomNavBar (Fill × 80dp)
```

### Error state

```
PaymentStatusScreen (Fill, Auto Layout Vertical)
  TopAppBar (same as content)
  Body (Fill, Auto Layout Vertical, padding=16dp, centred)
    ErrorContent (Hug, Auto Layout Vertical, gap=16dp, centred)
      ├─ Icon: error_outline (48dp, error colour)
      ├─ Title: "Could not load payment" (headlineSmall, onSurface, centre-aligned)
      ├─ Message: {error.message} (bodyMedium, onSurfaceVariant, centre-aligned)
      └─ retry_button (Button filled, Hug, container=primary, radius=full)
             Visible only: error.type in {TokenExpired, NetworkError}
             Label: "Try again"
  BottomNavBar (same as content)
```

---

## Component ↔ API Binding

| Component                   | Data source                                  | Transform                                    |
|-----------------------------|----------------------------------------------|----------------------------------------------|
| status_chip.label           | Data.Status                                  | statusLabelFor(rawStatus, ladder)            |
| status_chip.icon            | disposition                                  | dispositionIcon enum map                     |
| status_chip.container       | disposition                                  | payment_disposition token                    |
| payment_summary.amountLabel | Data.Initiation.InstructedAmount OR FirstPaymentAmount | formatMoney + family selector     |
| payment_summary.creditorName | Data.Initiation.CreditorAccount.Name        | direct                                       |
| payment_summary.debtorAccountLabel | Data.Initiation.DebtorAccount OR consent.Data.Initiation.DebtorAccount | mask last 4 digits |
| payment_summary.referenceLabel | Data.Initiation.RemittanceInformation.Unstructured[0] | nullable; absent on international |
| payment_summary.submittedAtLabel | Data.CreationDateTime                   | formatDateTime                               |
| in_progress_note            | disposition                                  | visible when == IN_PROGRESS                  |
| instruction_established_note | disposition                                 | visible when == INSTRUCTION_ESTABLISHED      |
| refresh_button              | disposition                                  | visible when == IN_PROGRESS                  |
| new_payment_button          | disposition                                  | visible when == TERMINAL_FAILURE             |
| retry_button                | error.type                                   | visible when type.isRetryable                |

---

## Partial-Failure Taxonomy

| Failure class                             | Render                              | Retry | Notes                                           |
|-------------------------------------------|-------------------------------------|:-----:|-------------------------------------------------|
| 404 — unknown paymentId                   | error_state, no retry_button        | No    | Terminal; resource does not exist               |
| 400 U011 — VRP revoked                    | Revoked from local record           | No    | NOT error_state; offer new mandate              |
| 401 — token expired                       | error_state + retry_button          | Yes   | Retry triggers token refresh before re-read     |
| 403 — consent revoked                     | error_state, no retry_button        | No    | Settled payments are NOT reversed               |
| 429 — rate limited during poll            | Keep last known status; no banner   | Auto  | Double poll interval; no UI change visible      |
| Network / timeout                         | error_state + retry_button          | Yes   | Pure read; safe to retry                        |
| Unrecognised status code                  | in_progress chip + refresh_button   | Auto  | Fail-open; keep polling                         |
