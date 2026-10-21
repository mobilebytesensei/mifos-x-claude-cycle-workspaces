# Standing Order (Domestic) — Screen Mockup Specification

> Source: `screens/pay-domestic-standing-order/{ui,docs,api}.yaml`
> Design system: Open Banking — Trust Blue (DESIGN.md v1.4.0)
> Design tokens: `idea-layer/design-system/design-tokens.yaml` v2.4.0

> **COPY PROVENANCE** — quoted strings below are VERBATIM `_strings/strings.yaml`
> (`strings.payment.*`, `strings.pay_domestic_standing_order.title`). The handful of slots that
> still have no catalogue key are annotated UNSOURCED inline — treat those as intent, not as
> approved copy.

---

## Shell

- **Top app bar**: title = "Standing order"; back navigation icon
- **Bottom navigation**: Home · Accounts · Pay · More
- **Step indicator**: 4 steps — Payee / Schedule / Amount / Review

---

## Step 1: Payee

### Component Hierarchy

```
Screen (Fill, Auto Layout Vertical, surface)
  TopAppBar (Fill × 56dp)
    BackIcon (24dp, onSurface)
    Title: "Standing order" (titleLarge, onSurface)
  StepIndicator (Fill, 4 steps active=Payee)
  InformationBanner [no_debtor_note]
    Icon: info (icon.md, onSurfaceVariant)
    Text: "You choose the account this comes from when you approve the standing order with
      HSBC, not here." (bodyMedium, onSurfaceVariant) — payment.so_no_debtor_note VERBATIM
    Container: surfaceContainerLow, radius.md
  BeneficiaryList
    SectionLabel: "Choose who to pay" (labelLarge, onSurfaceVariant)
    BeneficiaryRow × N (Fill × 56dp, surface)
      LeadingIcon: account_balance (icon.md, primary)
      PrimaryText: payee name (bodyLarge, onSurface)
      SupportingText: sort code / account number (bodyMedium, onSurfaceVariant, Roboto Mono)
      TrailingChevron (icon.sm, onSurfaceVariant)
  EnterManuallyButton (text button, primary)
    Label: "Enter account details instead" (labelLarge, primary)
  BottomNav (Fill × 80dp, surfaceContainerHighest)
```

### Tokens

| Role | Token |
|------|-------|
| Screen background | `colors.surface` |
| Info banner container | `colors.surfaceContainerLow` |
| Banner icon, supporting text | `colors.onSurfaceVariant` |
| Payee name text | `colors.onSurface` |
| Sort code / account number | `colors.onSurfaceVariant`, `typography.font_family.mono` |
| Leading icon | `colors.primary` |
| Banner radius | `radius.md` |

### Design Notes

The `no_debtor_note` banner is mandatory on this step. This rail has no funding-account step
because `DebtorAccount` is not in the standing-order schema. Without this notice the PSU
wonders why they were never asked for a source account. The banner explains that the choice
happens at the bank when they approve.

---

## Step 2: Schedule

### Component Hierarchy

```
Screen (Fill, Auto Layout Vertical, surface)
  TopAppBar + StepIndicator (as Step 1)
  ScrollContent (Fill, padding: spacing.md, gap: spacing.md)
    FrequencyDropdown [frequency_picker]
      Label: "How often" (bodySmall, onSurfaceVariant)
      SelectField (Fill × 56dp, outline: colors.outline, radius: radius.sm)
        SelectedValue: "Monthly" (bodyLarge, onSurface)
        DropdownIcon: expand_more (icon.md, onSurfaceVariant)
      Menu (surfaceContainerHigh, radius.md, elevation.level2)
        MenuItem: "Weekly" — WEEK
        MenuItem: "Every 2 weeks" — FRTN
        MenuItem: "Monthly" — MNTH
        MenuItem: "Every 3 months" — QURT
        MenuItem: "Yearly" — YEAR
    FirstPaymentDatePicker [first_payment_date_picker]
      Label: "First payment date" (bodySmall, onSurfaceVariant)
      DateField (Fill × 56dp, outline: colors.outline, radius: radius.sm)
        Value: "13 Aug 2026" (bodyLarge, onSurface)
        CalendarIcon: calendar_today (icon.md, onSurfaceVariant)
      Note: min = today + 1 day; weekends allowed
    HasEndDateSwitch [has_end_date_switch]
      Label: "Set an end date" (bodyLarge, onSurface)
      Switch (trailing, default: off)
    [Conditional: visible when has_end_date_switch = ON]
    FinalPaymentDatePicker [final_payment_date_picker]
      Label: "Final payment date" (bodySmall, onSurfaceVariant)
      DateField (Fill × 56dp, radius: radius.sm)
      HelperText: "Must be within 12 months" (bodySmall, onSurfaceVariant)
        UNSOURCED — no catalogue key; ui.yaml declares no helper_text on this picker.
      Note: min = firstPaymentDate + 1 day; max = today + 12 months
  NextButton (filled_pill, primary, Fill)
    Label: "Next" (labelLarge, onPrimary)
  BottomNav
```

### Frequency Picker Constraint

The picker offers **exactly five** values. ADHO, INDA, MIAN, DAIL are never shown. The
server returns U002 for all four. MONT is also invalid (not an OBIE code; typo for MNTH).

### Final Payment Date Constraints

Three constraints enforced client-side, all from a single U003 error message:
1. Must be after `FirstPaymentDateTime`
2. Must be within 12 months from today
3. Must not be today or tomorrow

All three are enforced via picker bounds. If U003 is still returned, the screen cannot
identify which rule fired (undifferentiated error message). Do not attempt to parse the
message text.

---

## Step 3: Amount

### Component Hierarchy

```
Screen (Fill, Auto Layout Vertical, surface)
  TopAppBar + StepIndicator (active=Amount)
  ScrollContent (padding: spacing.md, gap: spacing.md)
    AmountField [amount_field]
      Label: "Amount of each payment" (bodySmall, onSurfaceVariant)
      Field (Fill × 56dp, outline: colors.outline, radius: radius.sm)
        Prefix: "£" (bodyLarge, onSurfaceVariant, non-editable)
        Input (headlineSmall, onSurface, Roboto Mono, keyboard: numeric)
      HelperText: "Amount for the first payment" (bodySmall, onSurfaceVariant)
        UNSOURCED — no catalogue key for an amount-field helper.
    VaryingAmountsSwitch [varying_amounts_switch]
      Label: "Use different amounts for later payments" (bodyLarge, onSurface)
      Switch (trailing, default: off)
      SubLabel: "Guide §20.2.1 recommends equal amounts" (bodySmall, onSurfaceVariant)
        UNSOURCED — no catalogue key for an equal-amounts sub-label.
    [Conditional: visible when varying_amounts_switch = ON]
    RecurringAmountField [recurring_amount_field]
      Label: "Amount of each later payment" (bodySmall, onSurfaceVariant)
      Field (Fill × 56dp, radius: radius.sm)
        Prefix: "£" (bodyLarge, onSurfaceVariant)
        Input (headlineSmall, onSurface, Roboto Mono)
    [Conditional: visible when varying_amounts_switch = ON AND has_end_date = ON]
    FinalAmountField [final_amount_field]
      Label: "Amount of the final payment" (bodySmall, onSurfaceVariant)
      Field (Fill × 56dp, radius: radius.sm)
        Prefix: "£"
        Input (headlineSmall, onSurface, Roboto Mono)
    ReferenceField [reference_field]
      Label: "Reference (optional)" (bodySmall, onSurfaceVariant)
      Field (Fill × 56dp, outline: colors.outline, radius: radius.sm)
        Input (bodyLarge, onSurface)
      HelperText: "Shown on the recipient's statement. Up to 35 characters." (bodySmall,
        onSurfaceVariant) — payment.reference_helper VERBATIM
      CharCount: "0/35" (labelSmall, onSurfaceVariant, trailing)
  NextButton (filled_pill, primary)
    Label: "Next" (labelLarge, onPrimary)
  BottomNav
```

### Token Notes

- `amount_field` uses `headlineSmall` from the type scale (no inline size), Roboto Mono
- Amounts are held as minor units (pence) and displayed as major-unit formatted strings
- Validation timing: `on_change_after_first_blur` per `form.validation.timing`
- Amount validation error renders below the field in `colors.error`, `bodySmall`

### Reference Field Note

The reference maps to `Data.Initiation.RemittanceInformation.Unstructured[0]`. Omitted
entirely when blank. `MandateRelatedInformation.Reference` is refused (U005) — this field
sends to the correct location, not the mandate-level one.

---

## Step 4: Review

### Component Hierarchy

```
Screen (Fill, Auto Layout Vertical, surface)
  TopAppBar + StepIndicator (active=Review)
  ScrollContent (padding: spacing.md, gap: spacing.md)
    ReviewCard [review_card]
      Container (Fill, surfaceContainerLow, radius.md, elevation.level1)
      CardTitle: "Your standing order" (titleMedium, onSurface)
        UNSOURCED — ui.yaml's summary_card declares no title and no key covers one.
      Divider (outlineVariant — decorative only, not bounding a control)
      ReviewRow: "To" | payee name + sort code + account (bodyLarge / bodyMedium, onSurface / onSurfaceVariant)
      ReviewRow: "How often" | "Monthly" (bodyLarge / bodyMedium, onSurface / onSurfaceVariant)
      ReviewRow: "First payment" | "13 Aug 2026" (bodyLarge / bodyMedium, onSurface)
      ReviewRow [conditional: hasEndDate]: "Final payment" | "4 Dec 2026"
      ReviewRow: "Amount" | "£25.00" (bodyLarge, Roboto Mono, onSurface)
      ReviewRow [conditional: reference non-blank]: "Reference" | "Monthly rent"
      ReviewRow: "HSBC's charge" | "£0.05" (bodyLarge, Roboto Mono, onSurfaceVariant)
        Note: amount + currency only; Type (UK.OBIE.CHAPSOut) never rendered
    AmendNotice [amend_notice]
      Container (semantic.status.warning_container: tertiaryContainer, radius.md)
      Icon: warning (icon.md, tertiary)
      Body: "Once this standing order is set up, this app cannot change it or cancel it. To
        change the amount or the schedule, or to stop it altogether, use the HSBC app or online
        banking." (bodyMedium, onTertiaryContainer)
        — payment.amend_notice_standing_order VERBATIM. ui.yaml binds `content` only; this
        banner has no title row.
      This disclosure is MANDATORY under OBL Customer Experience Guidelines. Do not re-soften,
        paraphrase, or swap it for the standing_order.amend_notice_* pair, which belongs to the
        standing-orders LIST screen and is not bound here.
    ConfirmButton [confirm_button]
      Style: filled_pill
      Container: colors.primary, radius.full
      Label: "Set up this standing order" (labelLarge, onPrimary)
        — payment.confirm_standing_order VERBATIM
      Note: NOT "Send £25.00" — this is a deferred instruction, not an immediate transfer
    EscapeButton
      Style: text / outlined
      Label: "Back" (labelLarge, primary)
        UNSOURCED — ui.yaml declares no escape button and no key covers this label.
  BottomNav
```

### Review Step Design Rules

1. Every committed value appears in full — nothing summarised, nothing truncated.
2. The fee row shows `Charges[].Amount` + `Currency` only (`0.05 GBP`). Never render `Type`.
3. `firstPaymentDateLabel` is always populated — this screen always sends `FirstPaymentDateTime`.
4. CTA label is "Set up this standing order", not "Send £25.00". A customer who taps
   "Send £25.00" and sees no money leave has been told something false.
5. `amend_notice` at severity warning is **mandatory under OBL CEG**.
6. A same-weight escape (Back) sits adjacent to the CTA. Never a lone destructive button.

---

## Success State

### Component Hierarchy

```
Screen (Fill, Auto Layout Vertical, surface)
  TopAppBar (no back — success is terminal)
    Title: "Standing order set up" (titleLarge, onSurface)   UNSOURCED — no catalogue key
  SuccessContent (Fill, Auto Layout Vertical, padding: spacing.md, gap: spacing.lg)
    StatusChip [instruction_established]
      Container: semantic.payment_disposition.instruction_established.container
                 (surfaceVariant, radius.full)
      Icon: event_repeat (icon.md, onSurfaceVariant)
      Label: "Standing order set up" (labelLarge, onSurfaceVariant)   UNSOURCED — no key
      Note: FORBIDDEN labels — paid, sent, complete, completed, successful, any past-tense amount
    SummaryCard (surfaceContainerLow, radius.md)
      Row: "To" | payee name
      Row: "First payment" | "13 Aug 2026"
      Row [conditional]: "Final payment" | "4 Dec 2026" or "Until further notice" (UNSOURCED)
      Row: "How often" | "Monthly"
      Row: "Amount" | "£25.00" (Roboto Mono)
      Row [conditional]: "Reference" | "Monthly rent"
    AmendNotice [amend_notice] — severity warning, MANDATORY
      Same as Review step — payment.amend_notice_standing_order VERBATIM
    DoneButton (filled_pill, primary)
      Label: "Done" (labelLarge, onPrimary)   UNSOURCED — no catalogue key
  BottomNav
```

### Success State Design Rules

- Status chip uses `instruction_established` from `semantic.payment_disposition`.
  NOT `terminal_success` — this mandate has not paid anything yet.
- `amend_notice` is shown again at severity warning. The PSU must not leave this screen
  without knowing they cannot change this instruction through this app.
- No "Edit" or "Cancel" button — the PISP has no amendment path.
- If `hasEndDate = false`, the "Final payment" row shows "Until further notice".

---

## Component↔API Binding Table

| Component | ViewModel Action | API Operation | Wire Field |
|-----------|-----------------|--------------|------------|
| `beneficiary_list` row tap | SelectCreditor | (local) | CreditorAccount.Identification, .Name |
| `frequency_picker` selection | SelectFrequency | — | MandateRelatedInformation.Frequency.Type |
| `first_payment_date_picker` confirm | SelectFirstPaymentDate | — | MandateRelatedInformation.FirstPaymentDateTime |
| `has_end_date_switch` toggle | ToggleEndDate | — | Controls FinalPaymentDateTime presence |
| `final_payment_date_picker` confirm | SelectFinalPaymentDate | — | MandateRelatedInformation.FinalPaymentDateTime |
| `amount_field` input | EnterFirstPaymentAmount | — | FirstPaymentAmount.Amount (quoted 2dp string) |
| `varying_amounts_switch` toggle | ToggleVaryingAmounts | — | Controls RecurringPaymentAmount, FinalPaymentAmount |
| `recurring_amount_field` input | EnterRecurringAmount | — | RecurringPaymentAmount.Amount |
| `final_amount_field` input | EnterFinalAmount | — | FinalPaymentAmount.Amount |
| `reference_field` input | EnterReference | — | RemittanceInformation.Unstructured[0] |
| `confirm_button` tap | ConfirmAndStageConsent | POST /domestic-standing-order-consents | Full Initiation body |
| (post-consent resume) | SubmitStandingOrder | POST /domestic-standing-orders | ConsentId + Initiation from AUTH consent |

---

## Partial-Failure Taxonomy

| Error Class | Trigger | User Visible? | Recovery Path | Notes |
|-------------|---------|:-------------:|--------------|-------|
| FieldNotExpected (U005) | InstructedAmount sent / PointInTime sent / MandateRelatedInformation.Reference sent | Yes — error_panel | None (implementation fault) | Should never be user-reachable |
| InvalidMandateDates (U003) | FinalPaymentDateTime outside the three constraints | Yes — error_panel | Return to Schedule step | All three constraints enforced client-side by picker bounds; reaching this error means picker failed |
| InvalidFrequency (U002) | Frequency.Type outside the five accepted values | Yes — error_panel | None (should be unreachable if picker offers exactly 5) | ADHO, INDA, MIAN, DAIL not offered |
| MissingMandatory (U004) | Permission or MandateRelatedInformation omitted | Yes — error_panel | None (implementation fault) | R17-B03: only the parent error returns; nested Frequency error never emitted |
| SignatureMissing (U019) | x-jws-signature absent or invalid | Yes — error_panel | Not user-recoverable | Errors[] array must be fully rendered |
| ConsentNotAuthorised (U009) | POST /domestic-standing-orders before AUTH | Yes — error_panel + retry | Re-authorise | User aborted or timed out at bank |
| NetworkError | IOException / timeout | Yes — error_panel + retry | Retry with same idempotency key | Idempotency key is stable per mandate; safe to reuse |
| Multiple errors in one 400 | Errors[] array with 2+ entries | Yes — render ALL entries | Depends on codes | R15-E01: U005 on InstructedAmount reports while MISSING FirstPaymentAmount is NOT reported; validate locally first |

---

## Prohibitions Carried Through All States

1. No instalment progress indicator. OBIE has no per-execution status on this rail.
2. No "Check your standing-orders list" CTA. PIS-created mandates do not appear in AIS.
3. No "Paid", "Sent", "Complete" on the INCO status chip.
4. No amendment or cancellation button in the app.
5. `Charges[].Type` (UK.OBIE.CHAPSOut) is never rendered.
6. No CTA labelled "Confirm" without specifying the action — "Set up this standing order".
7. No funding-account step, no account picker.
