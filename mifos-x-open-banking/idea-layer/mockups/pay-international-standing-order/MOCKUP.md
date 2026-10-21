# Overseas Standing Order — Screen Mockup Specification

> Source: `screens/pay-international-standing-order/ui.yaml` schema 4.0
> Design system: Open Banking — Trust Blue (DESIGN.md 1.4.0, tokens v2.4.0)
> States: Content(step), Submitting(stage), Error(type)
> Steps: Recipient → Schedule → Amount → Charges → Review

> **COPY PROVENANCE** — quoted strings below are VERBATIM `_strings/strings.yaml`
> (`strings.payment.*`, `strings.pay_international_standing_order.title`). A few slots still
> have no catalogue key and are annotated UNSOURCED inline — treat those as intent, not as
> approved copy.

---

## App Shell

- **Top app bar**: title = "Overseas standing order", navigation_icon = back, no actions
- **Bottom nav**: present; tabs = Home / Accounts / Pay / More
- **Scrollable column**: screen_padding = `spacing.md` (16dp), gap between sections = `spacing.lg` (24dp)

---

## Step 1 — Recipient

Visible components: `step_indicator` (step 1 of 5 active), `no_debtor_note`, `iban_field`, `payee_name_field`, `bic_field`

### Component hierarchy

```
ScrollContent (Fill, Auto Layout Vertical, padding: spacing.md, gap: spacing.lg)
  ├─ stepper#step_indicator
  │     Steps: "Recipient · Schedule · Amount · Charges · Review"
  │     Active: step 1 (Recipient)
  │     Token: indicator dots — primary for active, outlineVariant for future
  │
  ├─ text#no_debtor_note
  │     Content: "You choose the account this comes from when you approve the standing order
  │       with HSBC, not here."   — payment.so_no_debtor_note VERBATIM
  │     Typography: bodySmall · Color: onSurfaceVariant
  │     Note: does NOT say the API has no debtor field — correction 2026-08-07
  │
  ├─ text_field#iban_field
  │     Label: "Recipient's IBAN"
  │     Keyboard: default (IBAN entry)
  │     Outline: outline (default) → primary (focus, 2dp) → error (validation fail, 2dp)
  │     Radius: radius.sm (8dp)
  │     Min height: 56dp
  │     Helper: "The international account number for the account you are paying. Your
  │       recipient will find it on their statement."   — payment.iban_helper VERBATIM
  │
  ├─ text_field#payee_name_field
  │     Label: "Recipient's name"
  │     Outline: outline → primary (focus)
  │     Radius: radius.sm
  │
  └─ text_field#bic_field
        Label: "Recipient's BIC (optional)"
        Helper: "Use the 11-character form. The shorter 8-character form is not accepted.
          Leave this blank if you are not sure."   — payment.bic_helper VERBATIM
        Error (bic non-blank, length ≠ 11): "A BIC must be exactly 11 characters"
        Outline: outline → primary (focus) → error (8-char BIC)
        Radius: radius.sm
```

**No reference field.** `RemittanceInformation` is refused by the API with U005. This is a designed absence, not a missing control. The note `no_reference_note` (inherited from pay-international-single) explains this on the Charges step.

---

## Step 2 — Schedule

Visible components: `step_indicator` (step 2 active), `frequency_picker`, `first_payment_date_picker`, `has_end_date_switch`, `final_payment_date_picker` (conditional)

### Component hierarchy

```
ScrollContent
  ├─ stepper#step_indicator — step 2 active
  │
  ├─ frequency_picker (inherited from pay-domestic-standing-order)
  │     Label: "How often"
  │     Exactly FIVE options — no more, no less (payment.frequency.* VERBATIM):
  │       • "Weekly" (WEEK)
  │       • "Every 2 weeks" (FRTN)
  │       • "Monthly" (MNTH)
  │       • "Every 3 months" (QURT)
  │       • "Yearly" (YEAR)
  │     Note: DAIL, ADHO, INDA, MIAN all return U002. Do not add them.
  │     Component type: radio_group or chip_group
  │     Color: primary for selected, outline for unselected
  │
  ├─ first_payment_date_picker (inherited)
  │     Label: "First payment date"
  │     Range: today + 1 day minimum, today + 12 months maximum
  │     Enforced by date picker bounds (not only client validation)
  │
  ├─ has_end_date_switch (inherited)
  │     Label: "Set an end date"
  │     Toggle: Boolean, default false
  │     When false → open-ended mandate
  │
  └─ final_payment_date_picker (inherited, visible: hasEndDate == true)
        Label: "Final payment date"
        Range: first_payment_date + 1 day minimum
        Note: omitting FinalPaymentDateTime stages 201 as open-ended — genuinely optional
```

---

## Step 3 — Amount

Visible components: `step_indicator` (step 3 active), `amount_field`, `fx_not_fixed_notice`, `no_varying_amounts_note`, `instructed_currency_picker`, `transfer_currency_picker`

### Component hierarchy

```
ScrollContent
  ├─ stepper#step_indicator — step 3 active
  │
  ├─ text_field#amount_field (amount_field type)
  │     Label: "Amount to send each time"   — payment.intl_so_amount_label VERBATIM
  │     Keyboard: number (decimal)
  │     Typography: headlineSmall · Font: typography.mono (Roboto Mono)
  │     Prefix: currency symbol (onSurfaceVariant, not part of editable value)
  │     Outline: outline → primary (focus) → error (invalid amount)
  │     Radius: radius.sm
  │     NOTE: Maps to InstructedAmount on the wire — NOT FirstPaymentAmount
  │     This is the field-level divergence from the domestic mandate rail.
  │     Each rail refuses the other's field with U005.
  │
  ├─ instructed_currency_picker (inherited from pay-international-single)
  │     Label: "Currency you are charged in"
  │     Helper: "The currency taken from your account."
  │     Value: ISO 4217 currency code, default GBP
  │     Note: independent of transfer_currency — do not couple them
  │
  ├─ transfer_currency_picker (inherited from pay-international-single)
  │     Label: "Currency the recipient gets"
  │     Helper: "This does not have to match the currency you are charged in."
  │     Value: ISO 4217 currency code, default USD
  │     Note: CurrencyOfTransfer on the wire — independent of InstructedAmount.Currency
  │
  ├─ banner#fx_not_fixed_notice
  │     Severity: warning
  │     Container: tertiaryContainer (#EADDFF light)
  │     Text color: onTertiaryContainer (#4C4162 light)
  │     Icon: schedule (tertiary)
  │     Visibility: step == Amount OR step == Review
  │     Text: "The exchange rate is not fixed for this standing order. Each payment is
  │       converted at the rate that applies on the day it is made, so the amount the
  │       recipient gets can differ each time. No rate can be shown here for a payment that
  │       has not happened yet."   — payment.intl_so_fx_not_fixed VERBATIM
  │     HARD RULE: never render a rate, a converted amount, a "you'll receive" figure or a
  │     projected total. Settled, not merely unavailable — ExchangeRateInformation is refused
  │     for all three RateType values, including the Agreed form carrying a real contracted
  │     rate. No rate can be agreed in advance.
  │
  └─ text#no_varying_amounts_note
        Text: "Every payment is for the same amount. This payment type does not let you set a
          different first or final amount."   — payment.intl_so_no_varying_amounts VERBATIM
        Typography: bodySmall · Color: onSurfaceVariant
        Visibility: step == Amount
        Note: explains the absence of the varying-amounts switch present
        on the domestic mandate screen
```

---

## Step 4 — Charges

Visible components: `step_indicator` (step 4 active), `charge_bearer_picker`, `no_reference_note`

### Component hierarchy

```
ScrollContent
  ├─ stepper#step_indicator — step 4 active
  │
  ├─ charge_bearer_picker (inherited from pay-international-single)
  │     Label: "Who pays the fees"   — payment.charge_bearer_label VERBATIM
  │     Options (radio group, ui.yaml order, payment.charge_bearer.* VERBATIM):
  │       • "You pay all the fees" (BorneByDebtor)
  │       • "You each pay your own bank's fees" (Shared)
  │       • "The recipient pays all the fees" (BorneByCreditor)
  │     Color: primary for selected
  │     Mandatory: omitting ChargeBearer returns U004
  │
  └─ text#no_reference_note (inherited from pay-international-single)
        Content: "You cannot send a payment reference abroad. This payment type has no way to
          add a message for the recipient."   — payment.intl_no_reference_note VERBATIM
        Typography: bodySmall · Color: onSurfaceVariant
        Note: RemittanceInformation is refused with U005 on all international
        shapes. This is a designed absence that must be named.
```

---

## Step 5 — Review

Visible components: `step_indicator` (step 5 active), `review_card`, `fx_not_fixed_notice`, `open_ended_mandate_note` (conditional), `deferred_charge_note`, `amend_notice`, `confirm_button`

### Component hierarchy

```
ScrollContent
  ├─ stepper#step_indicator — step 5 active
  │
  ├─ summary_card#review_card
  │     Container: surfaceContainer (#EBEEF3 light)
  │     Radius: radius.md (12dp)
  │     Elevation: level1
  │     Rows (all committed values — no truncation; labels payment.review.* VERBATIM):
  │       1. "To"           → IBAN (e.g. "FR29NWBK60161331926819")
  │       2. "Recipient's bank" → BIC (visible only when bic is not blank)
  │       3. "How often"    → e.g. "Monthly"
  │       4. "First payment" → first payment date
  │       5. "Final payment" → final date (visible only when hasEndDate)
  │       6. "Amount"       → instructedAmountLabel with instructedCurrency
  │       7. "Arrives in"   → transferCurrencyLabel
  │       8. "Who pays the fees" → chargeBearerLabel
  │       9. "HSBC's charge" → feeLabel, empty_value "Your bank has not quoted a fee yet"
  │            (payment.fee_unknown VERBATIM)
  │     Note: NO "Reference" row — RemittanceInformation refused
  │     Note: NO projected total, NO per-instalment received amount, NO rate
  │     The empty_value RULE: NEVER blank, NEVER "0.00", NEVER "Free". Charges is ABSENT
  │     from the consent response, not an empty array — a model that defaults it to []
  │     renders a 0.50 mandate as free at the moment of consent.
  │
  ├─ banner#fx_not_fixed_notice (same as Amount step)
  │     Visibility: step == Amount OR step == Review
  │
  ├─ text#open_ended_mandate_note
  │     Visibility: step == Review AND NOT hasEndDate
  │     Text: "This standing order has no end date, so it keeps going until it is stopped.
  │       You cannot stop it in this app — use the HSBC app or online banking."
  │       — payment.intl_so_open_ended_note VERBATIM. It names the channel concretely; do
  │       not soften it to "contact your bank".
  │     Typography: bodySmall · Color: onSurfaceVariant
  │
  ├─ banner#deferred_charge_note
  │     Severity: info
  │     Container: secondaryContainer (#D3E5F5 light)
  │     Text color: onSecondaryContainer (#384956 light)
  │     Visibility: step == Review
  │     Text: "A fee applies to this payment, but your bank does not quote it until the
  │       payment has been set up. You will see the amount then, and not before."
  │       — payment.deferred_charge_note VERBATIM
  │     CORRECTED: an earlier wording quoted "0.50" here. That is a DISCLOSURE VIOLATION —
  │     the charge first appears at RESOURCE CREATION, after the PSU authorises, never at
  │     AWAU and never at AUTH, and it is denominated in the INSTRUCTED currency, not
  │     necessarily sterling. The API also never states whether the 0.50 recurs per
  │     execution or applies once at setup, so quoting it would be doubly misleading on a
  │     recurring mandate. The catalogue string names no figure and no currency by design.
  │
  ├─ banner#amend_notice
  │     Severity: warning
  │     Container: tertiaryContainer (#EADDFF light)
  │     Text color: onTertiaryContainer (#4C4162 light)
  │     Icon: warning (tertiary)
  │     Body: "Once this standing order is set up, this app cannot change it or cancel it.
  │       To change the amount or the schedule, or to stop it altogether, use the HSBC app
  │       or online banking."
  │       — payment.amend_notice_standing_order VERBATIM (the key ui.yaml binds).
  │       ui.yaml declares `content` only; this banner has no title row. Do not swap it for
  │       the standing_order.amend_notice_* pair — that belongs to the standing-orders LIST
  │       screen and is not bound here.
  │     Visibility: step == Review OR uiState is Success
  │     MANDATORY under OBL Customer Experience Guidelines. CORRECTED: an earlier wording
  │     said only "contact your bank directly", which fails the obligation to direct the
  │     PSU to a specific channel. Do not re-soften it.
  │
  └─ button#confirm_button
        Label: "Set up this standing order"  — payment.confirm_standing_order VERBATIM.
        Names what is CREATED; must never read "Send" or name an amount.
        Variant: filled_pill
        Container: primary (#266489 light)
        Label color: onPrimary (#FFFFFF)
        Radius: radius.full (9999dp)
        Min touch target: 48dp
        Visibility: step == Review AND uiState is Content
        On click: ConfirmAndStageConsent
        Note: CTA names the action (instruction, not payment transfer)
        Note: locks and shows progress on tap — double-submission prevented
```

**No projected total, no FX rate, no estimated received amount** — all would require a rate the API does not provide, projected over a horizon nobody can forecast.

---

## Submitting State

Visible components: `step_indicator` (current step), `submitting_indicator`

```
ScrollContent
  ├─ stepper#step_indicator — step at time of submit
  │
  └─ progress#submitting_indicator
        Three stage labels shown as circular progress + text, all catalogue VERBATIM:
          StagingConsent:        "Setting up your payment with HSBC"   (payment.staging)
          AwaitingAuthorisation: "Waiting for your approval at HSBC"
                                 (payment.awaiting_authorisation)
          SubmittingPayment:     "Setting up your standing order"      (payment.creating_mandate)
        This rail ends on creating_mandate, NOT payment.submitting ("Sending your payment") —
        it returns INCO, the instruction is established and no money moves. No stage may read
        "sent", "paid" or "complete".
        Color: primary
        Note: confirm_button is hidden (Visibility: step == Review AND uiState is Content)
```

---

## Error State

Visible components: `step_indicator`, `error_panel`

```
ScrollContent
  ├─ stepper#step_indicator
  │
  └─ error_panel#error_panel
        Renders ONE ROW PER ENTRY in the Errors array, in wire order
        Row layout: errorCode label (labelMedium, error color) + message (bodyMedium, onSurface)
        Multi-error handling: SO-I04 can return TWO U002 entries simultaneously
        Copy keyed by ErrorCode + Path, never by Message (U004 has four distinct Messages)
        Background: errorContainer (#FFDAD6 light)
        Text: onErrorContainer (#93000A light)
        Tag: payInternationalStandingOrder:errorPanel
        Row tag: payInternationalStandingOrder:errorPanelRow
        Retry action available when NetworkError type — label "Try again" (payment.retry)
        UNSOURCED — ui.yaml binds no panel header key for this screen; render the rows alone.
        Per-row message text is the bank's own wire Message, not catalogue copy.
```

---

## Component ↔ API Binding Table

| Component | Action / API call | Field on the wire | Source of truth |
|---|---|---|---|
| amount_field | EnterInstructedAmount → ConfirmAndStageConsent | `Data.Initiation.InstructedAmount` | `instructedAmountMinorUnits` converted to major units |
| frequency_picker | SelectFrequency | `Data.Initiation.MandateRelatedInformation.Frequency.Type` | FrequencyType enum (5 values) |
| first_payment_date_picker | SelectFirstPaymentDate | `Data.Initiation.MandateRelatedInformation.FirstPaymentDateTime` | ISO 8601 |
| has_end_date_switch + final_payment_date_picker | ToggleEndDate + SelectFinalPaymentDate | `Data.Initiation.MandateRelatedInformation.FinalPaymentDateTime` | Absent when hasEndDate=false |
| iban_field | EnterIban | `Data.Initiation.CreditorAccount.Identification` (SchemeName: UK.OBIE.IBAN) | User input |
| payee_name_field | EnterPayeeName | `Data.Initiation.CreditorAccount.Name` | User input |
| bic_field | EnterBic | `Data.Initiation.CreditorAgent.Identification` (SchemeName: UK.OBIE.BICFI, 11 chars) | User input — whole object sent or omitted |
| instructed_currency_picker | SelectInstructedCurrency | `Data.Initiation.InstructedAmount.Currency` | ISO 4217 |
| transfer_currency_picker | SelectTransferCurrency | `Data.Initiation.CurrencyOfTransfer` | ISO 4217 — independent |
| charge_bearer_picker | SelectChargeBearer | `Data.Initiation.ChargeBearer` | ChargeBearer enum (mandatory) |
| review_card fee row | (read from resource after submit) | `Data.Charges[0].Amount` | Nullable — absent at consent |
| confirm_button | ConfirmAndStageConsent | POST /international-standing-order-consents | uiState → Submitting(StagingConsent) |

**Fields NOT sent**: `FirstPaymentAmount` (U005), `RemittanceInformation` (U005), `ExchangeRateInformation` (U005), `MandateRelatedInformation.Frequency.PointInTime` (U005), `DebtorAccount.Name` (schema constraint on this rail).

---

## Partial Failure Taxonomy

| Failure class | Origin | Example scenario | User-visible effect | Retry |
|---|---|---|---|---|
| Wrong amount field | Client sends FirstPaymentAmount on this rail | — | U005 @ Data.Initiation.FirstPaymentAmount — error_panel row | No (implementation fault) |
| Missing mandatory field | Client omits ChargeBearer, CurrencyOfTransfer, or Permission | — | U004 @ Data.Initiation.ChargeBearer — error_panel row | No (implementation fault) |
| Invalid frequency | Client sends DAIL or other non-5-value | — | U002 @ Data.Initiation.MandateRelatedInformation.Frequency.Type | No — return to Schedule |
| Invalid BIC length | Client sends 8-character BIC | — | U002 @ Data.Initiation.CreditorAgent.Identification | No — return to Recipient |
| Invalid mandate dates | Final before first, beyond 12 months, or today/tomorrow | SO-I09 | U003 | No — return to Schedule |
| Two U002 rules batched | Business rules fired together (SO-I04) | SO-I04/SO-I05 | Two error_panel rows; fix first, receive second alone on retry | No |
| Unresolvable creditor | Sort-code identifier that doesn't resolve internationally | SO-I07 | U027 @ Data.Initiation.CreditorAccount.SchemeName | No — unreachable (form takes IBAN) |
| Missing JWS signature | mTLS / signing misconfiguration | — | U019 — error_panel | No (not user-recoverable) |
| Consent not yet authorised | Submit called before AUTH | — | U009 | Yes — re-authorise |
| Network / timeout | IOException | — | NetworkError type — error_panel with Retry CTA | Yes — same idempotency key |
