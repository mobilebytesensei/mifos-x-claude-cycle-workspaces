# Pay International Scheduled — Mockup Specification

> Source: `idea-layer/screens/pay-international-scheduled/{ui,docs,api,data-flow}.yaml`
> Design system: Open Banking — Trust Blue (Material 3, seed #266489)
> Rail: international-scheduled-payment · Six steps · No funds confirmation

> **COPY PROVENANCE** — quoted strings below are VERBATIM `_strings/strings.yaml`
> (`strings.payment.*`, `strings.pay_international_scheduled.title`). A few slots still have no
> catalogue key and are annotated UNSOURCED inline — treat those as intent, not approved copy,
> and do not ship them to a renderer.

---

## 1. Form Architecture

The feature is a **six-step single-screen wizard**. Steps are internal state transitions; no new Activity or Fragment is mounted. The step_indicator persists at the top across all steps and all non-loading states.

| Step | Name | Components Active |
|------|------|-------------------|
| 1 | Account | step_indicator, debtor_account_list, ineligible_accounts_note |
| 2 | Recipient | step_indicator, iban_field, payee_name_field, bic_field, bic_length_error |
| 3 | Amount | step_indicator, amount_field, instructed_currency_picker, transfer_currency_picker, fx_disclosure, no_reference_note |
| 4 | Date | step_indicator, execution_date_picker, date_normalisation_note |
| 5 | Charges | step_indicator, charge_bearer_picker |
| 6 | Review | step_indicator, review_card, deferred_charge_note, no_funds_check_note, amend_notice, confirm_button |

---

## 2. Screen States

### 2.1 Loading State

**Purpose**: initial mount while eligible accounts are fetched.

```
TopAppBar (surface, onSurface)
  ← (back_icon)  "Pay abroad on a date" (titleLarge, onSurface)

ScrollContent (surface, padding: spacing.md, gap: spacing.md)
  Stepper [6 steps] — shimmer rectangle (surfaceContainerHighest, radius.sm)
  ShimmerBlock-1 (240 × 56dp, surfaceContainerHighest, radius.md)   — account card
  ShimmerBlock-2 (320 × 20dp, surfaceContainerHighest, radius.sm)   — row label
  ShimmerBlock-3 (240 × 56dp, surfaceContainerHighest, radius.md)   — account card
  ShimmerBlock-4 (320 × 20dp, surfaceContainerHighest, radius.sm)

BottomNav (surfaceContainerHigh)
  Home · Accounts · Pay (active, primary) · More
```

Tokens: `surfaceContainerHighest` for shimmer fill; `radius.md` for card shapes; no text.

---

### 2.2 Content State — Step 1: Account

**Purpose**: PSU selects their funding account.

```
TopAppBar (surface, onSurface)
  ← (back_icon)  "Pay abroad on a date" (titleLarge, onSurface)

ScrollContent (surface, padding: spacing.md, gap: spacing.md)

  [step_indicator]
  Stepper — 6 steps horizontal
    Steps 1–6, step 1 active dot (primary), steps 2–6 inactive (outlineVariant)
    Labels: "Account" "Recipient" "Amount" "Date" "Charges" "Review" (labelSmall, onSurfaceVariant)

  [ineligible_accounts_note]  — visible if hiddenAccountCount > 0
  Banner (severity: info, secondaryContainer / onSecondaryContainer)
    Icon: info (icon.md)
    "Some of your accounts are not shown. This payment can only be made from an account with a
     sort code and account number."   — payment.ineligible_accounts_note VERBATIM

  [debtor_account_list]
  SectionHeader "Choose the account to pay from" (titleSmall, onSurface)
  ListItem — Barclays Current Account (surfaceContainerLow, radius.md)
    Leading: bank_icon (icon.md, primary)
    "Barclays Current Account" (bodyLarge, onSurface)
    "•••• 4231" (bodyMedium, onSurfaceVariant)
    Trailing: "£2,450.00" (bodyLarge, Roboto Mono, onSurface)
  ListItem — HSBC Advance
    Leading: bank_icon (icon.md, primary)
    "HSBC Advance" (bodyLarge, onSurface)
    "•••• 7819" (bodyMedium, onSurfaceVariant)
    Trailing: "£800.50" (bodyLarge, Roboto Mono, onSurface)

  FilledButton "Next" (primary / onPrimary, radius.full, labelLarge)
    width: fill, min-height: 56dp
    UNSOURCED — ui.yaml declares no next_button and no catalogue key covers "Next".

BottomNav (surfaceContainerHigh)  Home · Accounts · Pay (primary active) · More
```

---

### 2.3 Content State — Step 2: Recipient

```
ScrollContent (surface, padding: spacing.md, gap: spacing.md)
  [step_indicator] — step 2 active

  SectionHeader "Recipient details" (titleSmall, onSurface)

  [iban_field]
  OutlinedTextField
    Label: "Recipient's IBAN" (bodySmall, onSurfaceVariant)
    Helper: "The international account number for the account you are paying. Your recipient
      will find it on their statement." (bodySmall, onSurfaceVariant)
    Input: "FR29NWBK60161331926819" (bodyLarge, onSurface)
    Radius: radius.sm · Min height: 56dp
    Outline default: outline (#72787E) · Focus: primary (#266489, 2dp)

  [payee_name_field]
  OutlinedTextField
    Label: "Recipient's name" (bodySmall, onSurfaceVariant)
    Input: "Mr Lee" (bodyLarge, onSurface)

  [bic_field]
  OutlinedTextField
    Label: "Recipient's BIC (optional)" (bodySmall, onSurfaceVariant)
    Helper: "Use the 11-character form. The shorter 8-character form is not accepted. Leave
      this blank if you are not sure." (bodySmall, onSurfaceVariant)

  [bic_length_error] — visible when BIC is non-blank and not 11 chars
  Text "A BIC must be exactly 11 characters" (bodySmall, error, #BA1A1A)

  FilledButton "Next" (primary, radius.full)   UNSOURCED — no key, see Step 1
```

---

### 2.4 Content State — Step 3: Amount

```
  [step_indicator] — step 3 active

  SectionHeader "Payment amount" (titleSmall, onSurface)

  [amount_field]
  OutlinedTextField (amount variant)
    Label: "Amount" (bodySmall, onSurfaceVariant)
    Prefix: "£" (onSurfaceVariant, non-editable)
    Input: "1.01" (headlineSmall, Roboto Mono, onSurface)
    Radius: radius.sm

  [instructed_currency_picker]
  ExposedDropdownMenu
    Label: "Currency you are charged in" (bodySmall, onSurfaceVariant)
    Helper: "The currency taken from your account." (bodySmall, onSurfaceVariant)
    Value: "GBP — British Pound" (bodyLarge, onSurface)

  [transfer_currency_picker]
  ExposedDropdownMenu
    Label: "Currency the recipient gets" (bodySmall, onSurfaceVariant)
    Helper: "This does not have to match the currency you are charged in." (bodySmall,
      onSurfaceVariant)
    Value: "EUR — Euro" (bodyLarge, onSurface)
    Note: two separate controls, no auto-sync

  [fx_disclosure]
  Banner (severity: info, secondaryContainer)
    "Your bank sets the exchange rate when it makes this payment. This app cannot show you the
     rate, or the amount the recipient will get."   — payment.fx_disclosure VERBATIM
    HARD RULE: never render a rate, a converted amount, a "you'll receive" figure, or a
    countdown. ExchangeRateInformation is refused for all three RateType values, so no rate can
    be shown or even asserted before authorisation.

  [no_reference_note]
  Banner (severity: info, secondaryContainer)
    "You cannot send a payment reference abroad. This payment type has no way to add a message
     for the recipient."   — payment.intl_no_reference_note VERBATIM
    (RemittanceInformation → U005 on this rail.)
```

---

### 2.5 Content State — Step 4: Date

```
  [step_indicator] — step 4 active

  SectionHeader "Execution date" (titleSmall, onSurface)

  [execution_date_picker]
  DatePicker (Material 3 modal calendar variant)
    Label: "Payment date" (bodySmall, onSurfaceVariant)
    Helper: "Choose any date from tomorrow up to a year ahead." (bodySmall, onSurfaceVariant)
    Min selectable: tomorrow (T+1)
    Max selectable: T+365 from today
    Disabled: today and all past dates (greyed, opacity.disabled)
    Disabled: T+366 and beyond (greyed, opacity.disabled)
    Allow weekends: yes
    Selected day chip: primary container / onPrimary

  [date_normalisation_note]
  Text "Your bank makes the payment on the date you choose. There is no set time of day."
    (bodySmall, onSurfaceVariant)   — payment.date_normalisation_note VERBATIM
```

---

### 2.6 Content State — Step 5: Charges

```
  [step_indicator] — step 5 active

  SectionHeader "Who pays the fees" (titleSmall, onSurface)   — payment.charge_bearer_label

  [charge_bearer_picker]
  RadioGroup (vertical, gap: spacing.sm) — ui.yaml order, no default selection: all three
  values stage 201, so none is a bank default and the PSU genuinely chooses.
    RadioItem "You pay all the fees" (bodyLarge, onSurface)               — BorneByDebtor
    RadioItem "You each pay your own bank's fees" (bodyLarge, onSurface)  — Shared
    RadioItem "The recipient pays all the fees" (bodyLarge, onSurface)    — BorneByCreditor
```

---

### 2.7 Content State — Step 6: Review

```
  [step_indicator] — step 6 active

  [review_card]
  Card (surfaceContainerLow, radius.md, elevation.level1)
    Row "From"     value: "Barclays Current Account •••• 4231" (bodyMedium, onSurface)
    Row "To"       value: "FR29NWBK60161331926819" (bodyMedium, onSurface)
    Row "Recipient's bank" [conditional: bic non-blank] value: "NWBKFRPPXXX" (bodyMedium)
    Row "Amount"   value: "£1.01 GBP" (bodyMedium, onSurface, Roboto Mono)
    Row "Arrives in" value: "EUR" (bodyMedium, onSurface)
    Row "Payment date" value: "13 August 2026" (bodyMedium, onSurface)
    Row "Who pays the fees" value: "The recipient pays all the fees" (bodyMedium, onSurface)
    Divider (outlineVariant — decorative only, never on controls)
    Row "HSBC's charge" value: "Your bank has not quoted a fee yet" (bodyMedium,
      onSurfaceVariant, italic)   — empty_value: payment.fee_unknown VERBATIM
      NOTE: NEVER show "Free", "£0.00", or blank. Charges is ABSENT on the consent.

  [deferred_charge_note]
  Banner (severity: info, secondaryContainer / onSecondaryContainer, icon: info)
    "A fee applies to this payment, but your bank does not quote it until the payment has been
     set up. You will see the amount then, and not before."
    — payment.deferred_charge_note VERBATIM
    CORRECTED: an earlier wording quoted "£0.50" here. That is a DISCLOSURE VIOLATION. The
    charge first appears at RESOURCE CREATION — after the PSU authorises — and it is
    denominated in the INSTRUCTED currency, which is not necessarily GBP. The catalogue string
    deliberately names no figure and no currency; do not add either.

  [no_funds_check_note]
  Banner (severity: info, secondaryContainer)
    "This app cannot check whether the money will be in your account on that date. Make sure
     there is enough to cover the payment."   — payment.no_funds_check_note VERBATIM

  [amend_notice]
  Banner (severity: info, secondaryContainer)
    "Once this payment is set up, this app cannot change it or cancel it. To do either, use the
     HSBC app or online banking."
    — payment.amend_notice_scheduled VERBATIM (the key ui.yaml binds; payments.amend_notice
    belongs to the hub screen). MANDATORY under OBL Customer Experience Guidelines.
    CORRECTED: an earlier wording said only "contact your bank directly", which fails the
    obligation to direct the PSU to a specific channel. Do not re-soften it.

  [confirm_button]
  FilledButton "Schedule this payment" (primary / onPrimary, radius.full, labelLarge)
    — payment.confirm_scheduled VERBATIM. Names what is CREATED; no money moves on tap.
    width: fill, min-height: 56dp
    Locks + shows LinearProgressIndicator on tap (prevents double-submission)
```

---

### 2.8 Content — No Eligible Accounts

```
  [step_indicator] — step 1, all steps inactive

  [no_eligible_accounts]
  EmptyState (center, gap: spacing.lg)
    Icon: account_balance_wallet (icon.xl, onSurfaceVariant)
    Title: "No account you can pay from" (headlineSmall, onSurface, center)
    Body: "This payment can only be made from an account with a sort code and account number.
           None of the accounts you have shared can be used for it."
          (bodyMedium, onSurfaceVariant, center)
    — payment.no_eligible_accounts_{title,body} VERBATIM
```

---

### 2.9 Submitting State

```
  [step_indicator] — step shows last active step (Review or beyond)

  [submitting_indicator]
  Column (center, gap: spacing.lg)
    CircularProgressIndicator (primary, 48dp)
    Text — stage label (bodyLarge, onSurface, center), all catalogue VERBATIM:
      StagingConsent:          "Setting up your payment with HSBC"
      AwaitingAuthorisation:   "Waiting for your approval at HSBC"
      SubmittingPayment:       "Sending your payment"
        KEY NOTE: payment.submitting is the shared caption across rails and reads "Sending",
        which is not literally true here — nothing is sent at submit time on a scheduled rail.
        Flagged for the catalogue owner; render verbatim, never paraphrased.

  NOTE: No "ConfirmingFunds" stage — this rail has no funds-confirmation endpoint.
```

---

### 2.10 Error State

```
  [step_indicator]

  [error_panel]
  Card (errorContainer / onErrorContainer, radius.md)
    Icon: error (icon.md, error)
    Title: "Payment could not be completed" (titleMedium, onErrorContainer)
      — payment.error_title VERBATIM

    FOR EACH entry in apiErrors (wire order):
      Divider (outlineVariant, decorative)
      ErrorRow
        Code badge: "U004" (labelSmall, onErrorContainer)
        Message: resolved from ErrorCode + Path key (bodyMedium, onErrorContainer)

  SP-I04 example — two entries:
    Entry 1 (U027) @ Data.Initiation.CreditorAccount.SchemeName
    Entry 2 (U002) @ Data.Initiation.CurrencyOfTransfer
    UNSOURCED — no catalogue key for either per-entry message, and the HSBC wire strings for
    SP-I04 are not recorded in the idea-layer. Render code + path only.
    Both entries MUST be shown. A panel bound to Errors[0] alone hides the second fault.

  RetryButton "Try again" (outlined, primary, radius.full) — payment.retry VERBATIM; if
    the error is retryable
  TextButton "Start a new payment" (primary) — always shown
    UNSOURCED — no key bound here. payment_status.new_payment ("Make a new payment") belongs
    to a different screen.
```

---

## 3. Component ↔ API Binding Table

| Component | API Trigger | Response Field | Notes |
|-----------|-------------|----------------|-------|
| debtor_account_list | Mount → GET /accounts | Data.Account[].Account[] | Filter SortCodeAccountNumber, exclude Global Money |
| confirm_button | POST /international-scheduled-payment-consents | Data.ConsentId | Body must include Permission, date, CurrencyOfTransfer, ChargeBearer; MUST NOT include RemittanceInformation |
| submitting_indicator (StagingConsent) | POST consent | — | Transition to AwaitingAuthorisation on 201 |
| submitting_indicator (AwaitingAuthorisation) | Poll GET /consents/{id} | Data.Status | Advance to SubmittingPayment on AUTH |
| submitting_indicator (SubmittingPayment) | POST /international-scheduled-payments | Data.InternationalScheduledPaymentId | Navigate to payment-status on 201 |
| review_card row "Fee" | POST /international-scheduled-payments | Data.Charges[0].Amount | Populated only AFTER resource creation; null at all prior stages |
| error_panel | Any 400 | Data.Errors[] | Render all entries, wire order, keyed ErrorCode+Path |
| execution_date_picker | — | — | Client-side constraint T+1..T+365; no API call until confirm |

---

## 4. Honest Treatment: Fee and FX Rate

### Fee Disclosure

| Stage | Charges key | UI rendering |
|-------|------------|--------------|
| Review (pre-confirm) | ABSENT from consent | Row shows strings.payment.fee_unknown + deferred_charge_note banner |
| Awaiting authorisation | ABSENT from consent | Not shown |
| After authorisation (AUTH) | ABSENT from consent | Still not shown |
| After resource creation (INCO) | 0.50 in instructed currency | fee_label updated on payment-status screen |

`strings.payment.fee_unknown` and `strings.payment.deferred_charge_note` are both present in
`_strings/strings.yaml` and are quoted verbatim on the Review step above.

The rule they encode: **no amount and no currency symbol may appear before the resource
exists.** Both strings deliberately name neither. The banner says only that a fee applies and
cannot be quoted until after authorisation. This is not an apology for a slow fetch — there is
no earlier call that could provide it, at AWAU or at AUTH. The charge first exists at resource
creation, i.e. after the PSU has already consented. Adding "£0.50" to either string would be a
disclosure violation, and the charge is in the INSTRUCTED currency, not necessarily sterling.

### FX Rate Disclosure

No FX rate is available at any stage. `ExchangeRateInformation` is refused (U005) for all three RateType values (Actual, Indicative, Agreed) on this rail and on both sibling international rails. The app must not show a rate, a converted amount, a "you'll receive" figure, or any placeholder implying a rate is forthcoming. The `fx_disclosure` banner states this plainly on the Amount step.

---

## 5. Partial-Failure Taxonomy

| Failure | HTTP / Trigger | Presentation | Recovery |
|---------|---------------|--------------|----------|
| U003 — date in the past | 400 | error_panel + BackStep to Date step | User corrects date |
| U002 — date out of range (>T+365) | 400 | error_panel + BackStep to Date step | User corrects date |
| U002 — BIC not 11 characters | 400 | error_panel + BackStep to Recipient step | User corrects BIC |
| U004 — mandatory field omitted | 400 | error_panel (implementation fault) | Not user-recoverable |
| U005 — RemittanceInformation sent | 400 | error_panel (implementation fault) | Not user-recoverable |
| U009 — consent not authorised | 400 | error_panel + re-authorise CTA | User re-authorises |
| U019 — signature missing | 400 | error_panel (implementation fault) | Not user-recoverable |
| SP-I04 — two Errors entries | 400 | error_panel shows BOTH in wire order | User fixes both |
| Network / timeout | IOException | error_panel + retry button | Retry, same idempotency key |
| Consent reaches RJCT | consent status | error_panel + "Start a new payment" CTA | Fresh payment, never resubmit |

---

## 6. Date Picker Constraints

| Rule | Value | API Error if violated |
|------|-------|-----------------------|
| Minimum selectable | T+1 (tomorrow) | U003 |
| Maximum selectable | T+365 from today | U002 |
| Weekends | Allowed | — |
| Past dates | Greyed out, not selectable | — |
| Today | Greyed out, not selectable | — |
| T+366 and beyond | Greyed out, not selectable | — |
| Normalisation | Server truncates to midnight UTC | date_normalisation_note informs user |

---

## 7. Disposition Token

After submit, the payment-status screen receives `paymentFamily = "international-scheduled-payment"` and `status = INCO`. Render using:

```
semantic.payment_disposition.instruction_established
  container:    surfaceVariant  (#DDE3EA light / #41474D dark)
  on_container: onSurfaceVariant (#41474D light / #C1C7CE dark)
  icon:         event_repeat
  contrast:     7.28:1  (W-30, WCAG AA pass)
```

Label: "Scheduled for \<date\>"  (UNSOURCED — no catalogue key for this chip label)  
FORBIDDEN substrings in this label: paid, sent, complete, completed, successful, any past-tense amount.  
FORBIDDEN dispositions for INCO: `terminal_success` (primary), `in_progress` (secondary).
