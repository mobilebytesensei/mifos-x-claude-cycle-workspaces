# pay-domestic-scheduled — Mockup Specification

> Source: `screens/pay-domestic-scheduled/{ui,docs,api,demo-data}.yaml`
> Design system: Open Banking — Trust Blue (DESIGN.md v1.4.0, design-tokens.yaml v2.4.0)
> Feature: Five-step domestic scheduled payment form

---

## Overview

Pay on a date is a five-step single-route form. Steps share a common chrome (top app bar with
back icon, bottom nav, 5-step stepper). Each step is one screenful; the user advances with a
single primary action and moves back with the navigation icon or the system Back gesture.

**Steps**: Account → Payee → Amount → Date → Review

The Date step is the only structural addition over the reference single-payment rail. The
funds-confirmation stage is deliberately absent — this rail has no such endpoint and displaying
one would be a false claim about a future balance.

---

## Component Hierarchy (all states)

```
PayDomesticScheduledScreen (Fill × Fill, Auto Layout Vertical)
  ├─ TopAppBar (Fill × 56dp)
  │   ├─ BackIcon — navigates back a step or to payments hub (48dp touch target)
  │   └─ Title "Pay on a date" (titleLarge, onSurface, Fill)
  │
  ├─ Stepper_step_indicator (Fill × 40dp, Auto Layout Horizontal, gap 4dp, padding 16dp)
  │   ├─ StepDot: Account   (labelSmall, active = primary, inactive = outline)
  │   ├─ StepDot: Payee
  │   ├─ StepDot: Amount
  │   ├─ StepDot: Date
  │   └─ StepDot: Review
  │
  ├─ ScrollContent (Fill, Auto Layout Vertical, padding 16dp, gap 16dp)
  │   └─ [Step-specific components — see per-step sections below]
  │
  └─ BottomNav (Fill × 80dp, surfaceContainerHigh)
      ├─ Home tab
      ├─ Accounts tab
      ├─ Pay tab (active, primary)
      └─ More tab
```

---

## Step 1: Account Selection

Visible when: `state == Content && step == Account`

```
ScrollContent
  ├─ SectionLabel "Pay from" (titleMedium, onSurface)
  ├─ List_debtor_account_list (Fill, Auto Layout Vertical, gap 0)
  │   └─ [FOR each eligible account]
  │       AccountListItem (Fill × 72dp, surface, radius.md)
  │         ├─ LeadingIcon: account_balance (icon.md, primary)
  │         ├─ PrimaryText: account name e.g. "Current Account" (bodyLarge, onSurface)
  │         ├─ SupportingText: sort-code + account formatted e.g. "40-20-01 / 10203351" (bodyMedium, onSurfaceVariant)
  │         └─ TrailingValue: balance e.g. "£2,450.00" (bodyLarge, mono, onSurface)
  └─ (if hiddenAccountCount > 0)
      IneligibleAccountsNote (bodySmall, onSurfaceVariant)
        "N other account(s) not shown — only accounts with a sort code and account number can make this payment."
```

**Interaction**: Tap any AccountListItem → `SelectDebtorAccount(accountId)` → advances to Step 2.
No explicit "Next" button on this step — selection is the advance.

**Demo content** (inherited from pay-domestic-single):
- Current Account · 40-20-01 / 10203351 · £2,450.00
- Savings Account · 40-20-01 / 10203352 · £500.00

---

## State: content_no_eligible_accounts

Visible when: `state == ContentNoEligibleAccounts`

```
ScrollContent (center-aligned, gap 24dp)
  └─ EmptyState_no_eligible_accounts (Hug, Auto Layout Vertical, center, gap 16dp)
      ├─ Icon: account_balance_wallet (48dp, onSurfaceVariant)
      ├─ Title "No accounts available" (headlineSmall, onSurface, center)
      └─ Body "Your account needs a UK sort code and account number to make this payment."
              (bodyMedium, onSurfaceVariant, center)
```

---

## Step 2: Payee Selection

Visible when: `state == Content && step == Payee`

```
ScrollContent
  ├─ SectionLabel "Pay to" (titleMedium, onSurface)
  ├─ List_beneficiary_list (Fill, Auto Layout Vertical, gap 0)
  │   └─ [FOR each beneficiary]
  │       BeneficiaryListItem (Fill × 64dp, surface, radius.md)
  │         ├─ LeadingIcon: person (icon.md, secondary)
  │         ├─ PrimaryText: payee name (bodyLarge, onSurface)
  │         └─ SupportingText: masked account e.g. "••••3351" (bodyMedium, onSurfaceVariant)
  └─ Button_enter_manually_button (outlined, Fill, radius.full)
      Label: "Enter sort code and account number" (labelLarge, primary)
```

**Manual entry sub-form** (visible when `manualEntryVisible == true`):

```
  ├─ TextField_sort_code_field (Fill, radius.sm, min 56dp)
  │   Label: "Sort code" · Placeholder: "00-00-00" · Helper: "6 digits"
  ├─ TextField_account_number_field (Fill, radius.sm, min 56dp)
  │   Label: "Account number" · Placeholder: "00000000" · Helper: "8 digits"
  └─ TextField_payee_name_field (Fill, radius.sm, min 56dp)
      Label: "Payee name" · Helper: "As registered with their bank"
```

**Interaction**: Tap beneficiary → `SelectCreditor(selection)` → advances to Step 3.
Tap "Enter sort code and account number" → shows manual sub-form; "Next" confirms and advances.

**Demo content** (inherited from pay-domestic-single):
- Ramu · ••••3351

---

## Step 3: Amount and Reference

Visible when: `state == Content && step == Amount`

```
ScrollContent
  ├─ AmountField_amount_field (Fill, radius.sm, min 56dp)
  │   Prefix: "£" (onSurfaceVariant, non-editable)
  │   InputText: major-unit decimal (headlineSmall, mono, onSurface)
  │   Label: "Amount"
  │   ErrorText: (if amountProblem) bodySmall, error
  ├─ (if amountProblem) Text_amount_error (bodySmall, error)
  └─ TextField_reference_field (Fill, radius.sm, min 56dp)
      Label: "Reference (optional)"
      Helper: "Appears on your payee's statement"
```

**Validation**: Runs on-change after first blur. Error locks the "Next" advance.
**Demo content**: Amount £1.01 · Reference "Rent"

---

## Step 4: Execution Date

Visible when: `state == Content && step == Date`

```
ScrollContent
  ├─ SectionLabel "Payment date" (titleMedium, onSurface)
  ├─ DatePicker_execution_date_picker (Fill, radius.sm)
  │   ─ Inline calendar widget, Material 3 DatePicker
  │   ─ minDate: tomorrow (today + 1)
  │   ─ maxDate: today + 365
  │   ─ allow_weekends: true (weekends ARE selectable — observed Saturday stages 201)
  │   ─ Disabled dates: today and earlier; today + 366 and later
  │   ─ Selected date chip: primary background, onPrimary text
  │   ─ Disabled date: outlineVariant text (decorative — do not use for control glyphs per WCAG)
  └─ Text_date_normalisation_note (bodySmall, onSurfaceVariant)
      "Your payment will be made on the date you choose. The bank does not guarantee a time of day."
```

**Date picker constraints** (derived from measured sandbox behaviour):

| Condition | Picker behaviour | API consequence |
|---|---|---|
| Today selected | Disabled (not selectable) | U003 if bypassed |
| Tomorrow selected | Enabled — minimum selectable date | Likely 201 (documented, not observed) |
| T+7 to T+365 selected | Enabled | 201 confirmed (measured) |
| T+366 or later | Disabled (not selectable) | U002 if bypassed |
| Saturday / Sunday | Enabled (selectable) | 201 confirmed (Saturday 2026-09-05 observed) |
| Bank holiday | No filter — bank does not enforce | Accept as-is |

**Time normalisation note** (mandatory copy): The bank discards the time component of
`RequestedExecutionDateTime`. `2026-08-13T10:28:58+00:00` becomes `2026-08-13T00:00:00+00:00`.
The copy in `date_normalisation_note` must not promise a time of day.

**Lower bound evidence gap**: The T+1 floor follows HSBC Guide §22.2.1 ("Today +1"). T+1 through
T+6 were never probed in the corpus. If the real floor is higher than tomorrow, the picker
offers dates that will return U003. This gap is declared, not resolved.

**Interaction**: Tap a date cell → `SelectExecutionDate(date)` → sets `requestedExecutionDate`;
enables the "Next" button (advance to Review). The "Next" button is disabled until a date is chosen.

---

## Step 5: Review

Visible when: `state == Content && step == Review`

```
ScrollContent
  ├─ SummaryCard_review_card (Fill, surfaceContainerLow, radius.md, elevation 1)
  │   ├─ Row: "From"        → debtorAccountLabel   e.g. "Current Account · 40-20-01"
  │   ├─ Row: "To"          → creditorLabel         e.g. "Ramu · ••••3351"
  │   ├─ Row: "Amount"      → amountLabel           e.g. "£1.01"
  │   ├─ Row: "Date"        → executionDateLabel    e.g. "13 August 2026"  ← date only, no time
  │   ├─ Row: "Reference"   → referenceLabel        e.g. "Rent"   (hidden if blank)
  │   └─ Row: "Fee"         → feeLabel              e.g. "£0.05 (UK.OBIE.CHAPSOut)"
  │
  ├─ Banner_no_funds_check_note (Fill, secondaryContainer, radius.md, severity: info)
  │   Icon: info (icon.md, onSecondaryContainer)
  │   Text: "We cannot check whether funds will be available on the payment date.
  │          The bank will attempt the payment on the chosen date."
  │          (bodyMedium, onSecondaryContainer)
  │
  ├─ Banner_amend_notice (Fill, surfaceVariant, radius.md, severity: info)
  │   Icon: info (icon.md, onSurfaceVariant)
  │   Text: "Once scheduled, this payment cannot be changed or cancelled through this app.
  │          To amend or cancel, use your bank's own app or online banking."
  │          (bodyMedium, onSurfaceVariant)
  │   — MANDATORY under OBL Customer Experience Guidelines —
  │
  └─ Button_confirm_button (filled_pill, primary, Fill, radius.full, min 56dp)
      Label: "Schedule payment"    ← NOT "Send £1.01" — this is a deferred instruction
```

**Review token mapping**:

| Row | Token | Notes |
|---|---|---|
| Row labels | `typography.titleSmall`, `onSurfaceVariant` | Left column |
| Row values | `typography.bodyLarge`, `onSurface` | Right column; amount uses `mono` |
| Date value | `typography.bodyLarge`, `onSurface` | Date only — no time of day displayed |
| Fee value | `typography.bodyLarge`, `onSurface`, `mono` | From Charges[0] |
| no_funds_check_note | `colors.secondaryContainer` / `onSecondaryContainer` | 7.22:1 contrast (W measured) |
| amend_notice | `colors.surfaceVariant` / `onSurfaceVariant` | 7.28:1 contrast (W-30) |
| confirm_button | `colors.primary` fill / `colors.onPrimary` label | Stays primary — never error-red |

**CTA label rule**: "Schedule payment" (not "Send £X.XX"). This CTA commits an instruction, not
a transfer. The payment does not move on tap — it is staged at the bank. A customer who reads
"Send £1.01" and sees no immediate debit has been told something false.

---

## State: Submitting

Visible when: `state == Submitting`

```
ScrollContent (center-aligned)
  ├─ Stepper (persists — same 5-step indicator, preserves orientation)
  └─ Progress_submitting_indicator (Hug, Auto Layout Vertical, center, gap 16dp)
      ├─ CircularProgressIndicator (48dp, primary)
      └─ ProgressLabel (bodyMedium, onSurfaceVariant, center)
          StagingConsent:        "Setting up your scheduled payment…"
          AwaitingAuthorisation: "Waiting for authorisation…"
          SubmittingPayment:     "Scheduling your payment…"
```

**No ConfirmingFunds stage.** This label does not exist on this rail. The single-payment rail's
"Confirming funds…" stage must not appear here.

**Locking**: The stepper steps are non-tappable. Back gesture is disabled while in-flight.

---

## State: Error

Visible when: `state == Error`

```
ScrollContent (center-aligned, gap 24dp)
  ├─ Stepper (persists)
  └─ ErrorContent (Hug, Auto Layout Vertical, center, gap 16dp)
      ├─ Icon: error_outline (48dp, error)
      ├─ Title: error title (headlineSmall, onSurface, center)
      ├─ Message: per-error body (bodyMedium, onSurfaceVariant, center)
      │   [Renders ALL Errors[] entries — not just the first]
      │   [Key on ErrorCode + Path case-insensitively, never on Message wording]
      └─ (if retryable) FilledButton "Try again" (primary, radius.full)
```

**Per-error rendering**:

| ErrorType | Title | Body | Retry |
|---|---|---|---|
| DateInPast | "Date in the past" | "The selected date has already passed. Please choose tomorrow or later." | No — return to Date step |
| DateOutOfRange | "Date too far ahead" | "The date must be within 365 days from today." | No — return to Date step |
| MissingRequiredField | "Something went wrong" | "A required field was missing. Please try again." | No |
| SignatureMissing | "Something went wrong" | "A security check failed. Please contact support." | No |
| ConsentNotAuthorised | "Authorisation required" | "The payment wasn't authorised. Please try again." | Yes — re-authorise |
| InitiationMismatch | "Something went wrong" | "The payment details don't match. Please try again." | No |
| NetworkError | "No connection" | "Check your internet connection and try again." | Yes |

---

## Component ↔ API Binding Table

| Component | Writes to | API call | When |
|---|---|---|---|
| `debtor_account_list` row tap | `content.debtorAccountId` | (none — local) | Step 1 selection |
| `beneficiary_list` row tap | `content.creditor` | (none — local) | Step 2 selection |
| Manual entry fields | `content.sortCodeInput`, `accountNumberInput`, `payeeNameInput` | (none — local) | Step 2 manual entry |
| `amount_field` keystroke | `content.amountMinorUnits` | (none — local) | Step 3 input |
| `reference_field` keystroke | `content.referenceInput` | (none — local) | Step 3 input |
| `execution_date_picker` day tap | `content.requestedExecutionDate` | (none — local) | Step 4 selection |
| `confirm_button` tap | `uiState → Submitting(StagingConsent)` | POST /domestic-scheduled-payment-consents | Step 5 confirm |
| (auto, after payment-consent AUTH) | `uiState → Submitting(SubmittingPayment)` | POST /domestic-scheduled-payments | Resume after auth |

---

## Partial Failure Taxonomy

| Scenario | Failure point | Safe? | Recovery |
|---|---|---|---|
| Network drops during POST /consents | Before 201; consent not staged | Yes (idempotency key not yet committed) | Retry from Review |
| Network drops during POST /payments | Before 201; payment may or may not exist | Yes (idempotency key reused — safe) | Retry |
| Consent staged but auth leg aborted | consent in AWAU forever | Yes | Re-enter flow; show error |
| U003 despite picker bounds | Client-side gap (T+1..T+6 unmeasured) | No | Return to Date step |
| INCO read back from status poll | Terminal — instruction is established | N/A — not a failure | Display instruction_established chip |
| Five stub timestamps received on 201 | Display bug if rendered | Prevented by invariant | Show only requestedExecutionDate |

---

## Accessibility Contract

- All interactive elements: 48dp minimum touch target.
- Stepper step labels: `labelSmall` on `surface` — 11sp/400 weight; decorative at this size.
  Active step uses `primary` container chip.
- Date picker disabled dates: `outlineVariant` on `surface` (W-32: 1.62:1) — decorative only,
  not used for control glyphs. Active/selected dates use `primary` (6.11:1 on surface).
- `no_funds_check_note` and `amend_notice` banners: 7.22:1 / 7.28:1 — both WCAG AA pass.
- Error state: `error` on `surface` = 6.14:1 — WCAG AA pass.
- `instruction_established` chip: `onSurfaceVariant` on `surfaceVariant` = 7.28:1 (W-30) — pass.
- `event_repeat` icon + text label BOTH present on `instruction_established` chip (WCAG 1.4.1).
- Colour is never the only signal on any disposition or status element.
