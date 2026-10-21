# MOCKUP — Pay Abroad (International Single Payment)

**Archetype:** form (five-step, single screen advancing through steps)
**Shell:** Top app bar ("Pay abroad") + back arrow. Bottom navigation bar: Home · Accounts · Pay (active) · More.
**Design system:** Open Banking — Trust Blue, Material 3, Roboto / Roboto Mono, seed `#266489`.

---

## Screen: loading

```
┌─────────────────────────────────────┐
│ ←  Pay abroad                       │  ← top_app_bar; onSurface title; arrow_back
├─────────────────────────────────────┤
│                                     │
│  [1]──[2]──[3]──[4]──[5]           │  ← step_indicator (skeletons — step labels dimmed)
│  Acct  Recip  Amt  Charges  Review  │    Roboto labelSmall, onSurfaceVariant
│                                     │
│  ┌───────────────────────────────┐  │  ← skeleton account card 1
│  │ ████████████████   ████████  │  │    outlineVariant fill, radius.md (12dp), 72dp height
│  │ █████████████████████        │  │    shimmer short (150ms)
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │  ← skeleton account card 2
│  │ ████████████████   ████████  │  │
│  │ █████████████████████        │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │  ← skeleton account card 3
│  │ ████████████████   ████████  │  │
│  │ █████████████████████        │  │
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  Home  Accounts  [Pay]  More        │  ← bottom_nav; Pay tab active (primary)
└─────────────────────────────────────┘
```

**Layout notes:** Step indicator visible but labels in onSurfaceVariant (disabled style). Three 72dp
skeleton cards shimmer against surfaceContainerHighest (`#E0E3E8`), radius.md (12dp). No buttons
active. Bottom nav present and navigable.

---

## Screen: content — Step 1 (Account)

```
┌─────────────────────────────────────┐
│ ←  Pay abroad                       │
├─────────────────────────────────────┤
│                                     │
│  [1]──[2]──[3]──[4]──[5]           │  ← step 1 filled-primary; steps 2-5 outline-onSurfaceVariant
│  Acct  Recip  Amt  Charges  Review  │
│                                     │
│  ┌───────────────────────────────┐  │  ← debtor_account_list card; surfaceContainer, radius.md
│  │ ○  Current Account            │  │    radio button (outline) + bodyLarge onSurface
│  │    80-20-01  10203349         │  │    bodyMedium onSurfaceVariant; Roboto Mono
│  │    £1,234.56 available        │  │    labelLarge primary; Roboto Mono
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │  ← second eligible account
│  │ ○  Savings Account            │  │
│  │    80-20-01  20304050         │  │
│  │    £8,750.00 available        │  │
│  └───────────────────────────────┘  │
│                                     │
│  ▸ 1 account not shown             │  ← ineligible_accounts_note; bodySmall, onSurfaceVariant
│    (Global Money — conversion only) │    (hidden if hiddenAccountCount == 0)
│                                     │
│  ┌───────────────────────────────┐  │  ← disabled Next button (no account selected)
│  │         Next →                │  │    opacity 0.38; primary fill; radius.full
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  Home  Accounts  [Pay]  More        │
└─────────────────────────────────────┘
```

**After selecting an account:**
- Selected card gets a filled-primary radio dot and a `check` trailing icon.
- Next button becomes active (full opacity).

---

## Screen: content — Step 2 (Recipient)

```
┌─────────────────────────────────────┐
│ ←  Pay abroad                       │
├─────────────────────────────────────┤
│                                     │
│  [1]─[2]──[3]──[4]──[5]            │  ← step 2 active (primary); step 1 completed (check)
│                                     │
│  Recipient's IBAN *                 │  ← iban_field; form.field token; 56dp min height; radius.sm
│  ┌───────────────────────────────┐  │    outline: form.field.outline_default (#72787E)
│  │ DE89 3704 0044 0532 0130 00   │  │    bodyLarge onSurface; Roboto
│  └───────────────────────────────┘  │
│  Enter the full IBAN including      │  ← helper_text; bodySmall onSurfaceVariant
│  country code (e.g. DE89…)          │
│                                     │
│  Payee name *                       │  ← payee_name_field
│  ┌───────────────────────────────┐  │
│  │ Klara Weiss                   │  │
│  └───────────────────────────────┘  │
│                                     │
│  Bank code (BIC) — optional         │  ← bic_field; helper text says "11 characters"
│  ┌───────────────────────────────┐  │    maxLength 11; bodyLarge Roboto Mono
│  │ COBADEFFXXX                   │  │
│  └───────────────────────────────┘  │
│  11 characters (e.g. COBADEFFXXX)   │  ← helper_text; bodySmall onSurfaceVariant
│                                     │
│  [If BIC is 8 chars — error shown:] │
│  ⚠ Bank code must be 11 characters │  ← bic_length_error; bodySmall error (#BA1A1A)
│                                     │
│  ┌───────────────────────────────┐  │  ← Next button; primary fill; radius.full
│  │         Next →                │  │
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  Home  Accounts  [Pay]  More        │
└─────────────────────────────────────┘
```

**BIC validation:** `bic_length_error` is shown only when the field is non-blank and the length
is not 11. An empty BIC field is valid — omitting CreditorAgent entirely is accepted. The field
validates length only; BIC-to-IBAN country correlation is deliberately absent (the refusal is
length-driven, not country-mismatch-driven — R2-07 matched country and was still refused).

---

## Screen: content — Step 3 (Amount)

```
┌─────────────────────────────────────┐
│ ←  Pay abroad                       │
├─────────────────────────────────────┤
│                                     │
│  [1]─[2]─[3]──[4]──[5]             │  ← step 3 active
│                                     │
│  Amount *                           │  ← amount_field; form.amount_field token
│  ┌───────────────────────────────┐  │    prefix "£" (onSurfaceVariant, not editable)
│  │ £  5.00                       │  │    headlineSmall; Roboto Mono; left-aligned
│  └───────────────────────────────┘  │
│                                     │
│  Charged in *                       │  ← instructed_currency_picker; dropdown
│  ┌───────────────────────────────┐  │    "The currency you pay in"
│  │ GBP — British Pound      ▾   │  │    bodyLarge onSurface
│  └───────────────────────────────┘  │
│  The currency you pay in            │  ← helper_text; bodySmall onSurfaceVariant
│                                     │
│  Arrives as *                       │  ← transfer_currency_picker; dropdown
│  ┌───────────────────────────────┐  │    "The currency the recipient receives"
│  │ EUR — Euro               ▾   │  │    bodyLarge onSurface
│  └───────────────────────────────┘  │
│  The currency the recipient         │  ← helper_text; bodySmall onSurfaceVariant
│  receives (required)                │
│                                     │
│  ┌───────────────────────────────┐  │  ← fx_disclosure banner; visible when currencies differ
│  │ ℹ  The converted amount is    │  │    info severity; secondaryContainer fill
│  │    set by HSBC at the time    │  │    bodyMedium onSecondaryContainer
│  │    of payment. No rate is     │  │
│  │    shown before authorisation.│  │
│  └───────────────────────────────┘  │
│                                     │
│  ▸ No payment reference            │  ← no_reference_note; bodySmall onSurfaceVariant
│    International payments on this   │
│    rail cannot include a reference. │
│                                     │
│  ┌───────────────────────────────┐  │
│  │         Next →                │  │
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  Home  Accounts  [Pay]  More        │
└─────────────────────────────────────┘
```

**Notes:**
- `fx_disclosure` is visible only when `instructedCurrency ≠ currencyOfTransfer`.
- `no_reference_note` is always visible on this step — named absence, not a silently missing field.
- Amount decimals follow the instructed currency (e.g. JPY renders no decimal places).

---

## Screen: content — Step 4 (Charges)

```
┌─────────────────────────────────────┐
│ ←  Pay abroad                       │
├─────────────────────────────────────┤
│                                     │
│  [1]─[2]─[3]─[4]──[5]              │  ← step 4 active
│                                     │
│  Who pays the bank charges? *       │  ← charge_bearer_picker; radio_group
│                                     │
│  ◉  I pay all charges               │  ← BorneByDebtor option
│                                     │
│  ○  We share the charges            │  ← Shared option
│                                     │
│  ○  The recipient pays the charges  │  ← BorneByCreditor option
│                                     │
│  ▸ HSBC quotes no fee for this      │  ← no_charge_note; bodySmall onSurfaceVariant
│    payment type. You are choosing   │
│    who covers any receiving-bank    │
│    charges, not HSBC charges.       │
│                                     │
│  ┌───────────────────────────────┐  │
│  │         Next →                │  │  ← disabled until a radio is selected
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  Home  Accounts  [Pay]  More        │
└─────────────────────────────────────┘
```

**ChargeBearer is mandatory.** Omitting it returns `U004 @ Data.Initiation.ChargeBearer`.
All three values stage 201 — the PSU makes a real choice, not a default selection.

---

## Screen: content — Step 5 (Review)

```
┌─────────────────────────────────────┐
│ ←  Pay abroad                       │
├─────────────────────────────────────┤
│                                     │
│  [1]─[2]─[3]─[4]─[5]               │  ← step 5 active (all prior steps completed)
│                                     │
│  ┌───────────────────────────────┐  │  ← review_card; surfaceContainer, radius.md (12dp)
│  │  Review your payment          │  │    titleMedium onSurface; 16dp padding
│  │                               │  │
│  │  From                         │  │  ← label bodySmall onSurfaceVariant
│  │  Current Account              │  │    value bodyLarge onSurface
│  │  80-20-01  10203349           │  │    Roboto Mono for account number
│  │                               │  │
│  │  To (IBAN)                    │  │
│  │  DE89370400440532013000       │  │    bodyLarge Roboto Mono
│  │                               │  │
│  │  Bank (BIC)                   │  │  ← hidden when bic is blank
│  │  COBADEFFXXX                  │  │    bodyLarge Roboto Mono
│  │                               │  │
│  │  Amount                       │  │
│  │  £5.00 GBP                    │  │    bodyLarge Roboto Mono; primary (#266489)
│  │                               │  │
│  │  Arrives as                   │  │
│  │  EUR                          │  │    bodyLarge onSurface
│  │                               │  │
│  │  Charges                      │  │
│  │  I pay all charges            │  │    bodyLarge onSurface
│  │                               │  │
│  │  ─────────────────────────── │  │  ← outlineVariant divider (decorative only)
│  │  ▸ No payment reference      │  │    bodySmall onSurfaceVariant
│  │  ▸ No fee quoted by HSBC     │  │    bodySmall onSurfaceVariant
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │  ← confirm_button; primary fill; radius.full
│  │     Send £5.00                │  │    labelLarge onPrimary; 48dp height
│  └───────────────────────────────┘  │    locks + shows spinner on tap (double-submit guard)
│                                     │
│  ┌───────────────────────────────┐  │  ← Cancel text button; no fill; onSurface
│  │          Cancel               │  │    same weight as confirm — not diminished
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  Home  Accounts  [Pay]  More        │
└─────────────────────────────────────┘
```

**Review surface invariants:**
- No fee row — this rail returns no Charges at any stage.
- No reference row — `RemittanceInformation` is refused with `U005`.
- CTA label is "Send £5.00" (amount in the label) — not a bare "Confirm".
- Cancel is same visual weight as confirm (both offered, neither diminished).
- Confirm button locks and shows a spinner on first tap; double-submission is impossible from the UI.

---

## Screen: submitting

```
┌─────────────────────────────────────┐
│ ←  Pay abroad                       │
├─────────────────────────────────────┤
│                                     │
│  [1]─[2]─[3]─[4]─[5]               │
│                                     │
│                                     │
│          ◌  (progress ring)         │  ← CircularProgressIndicator; primary stroke
│                                     │
│     Staging your payment…           │  ← StagingConsent label; bodyLarge; onSurface; centre
│                                     │
│  [Transitions through stages:]      │
│     Waiting for HSBC authorisation  │  ← AwaitingAuthorisation label
│     Checking funds…                 │  ← ConfirmingFunds label
│     Submitting payment…             │  ← SubmittingPayment label
│                                     │
│                                     │
├─────────────────────────────────────┤
│  Home  Accounts  [Pay]  More        │
└─────────────────────────────────────┘
```

**Notes:**
- Only `step_indicator` and `submitting_indicator` are visible. Form components are unmounted.
- The four stage labels correspond exactly to `SubmitStage` values in the ViewModel.
- No cancel affordance during submission — the consent has already been staged.

---

## Screen: error

```
┌─────────────────────────────────────┐
│ ←  Pay abroad                       │
├─────────────────────────────────────┤
│                                     │
│  [1]─[2]─[3]─[4]─[5]               │
│                                     │
│  ┌───────────────────────────────┐  │  ← error_panel; errorContainer (#FFDAD6) fill; radius.md
│  │                               │  │
│  │  ✕  Payment could not be      │  │  ← error icon + titleSmall onErrorContainer (#93000A)
│  │     processed                 │  │
│  │                               │  │
│  │  ─────────────────────────── │  │
│  │                               │  │  ← error rows — one per Errors[] entry, wire order
│  │  Unsupported scheme           │  │    row 1: ErrorCode U027 @ CreditorAccount.SchemeName
│  │  Data.Initiation.Creditor     │  │    bodyMedium onErrorContainer
│  │  Account.SchemeName           │  │    labelSmall onSurfaceVariant (path)
│  │                               │  │
│  │  ─────────────────────────── │  │
│  │                               │  │
│  │  Account cannot be same       │  │    row 2: ErrorCode U002 @ DebtorAccount.Identification
│  │  Data.Initiation.Debtor       │  │    (the actionable entry — shown because we render ALL)
│  │  Account.Identification       │  │
│  │                               │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │  ← Retry; outlined; primary border + text; radius.full
│  │          Try again            │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │  ← Back to payment; text button; onSurface
│  │      Back to payment          │  │
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  Home  Accounts  [Pay]  More        │
└─────────────────────────────────────┘
```

**Error panel invariants:**
- Every `Errors[]` entry is rendered in wire order — never only `Errors[0]`.
- Row content is keyed by `ErrorCode + Path`, not by `Message`.
- Two-entry fixture above (R13-10/R9-11): rendering only the first row would hide the actionable entry.
- Error is not framed as user fault — no "you entered", no "invalid", no correction instruction implying the PSU mis-typed. The bank rejected the request.

---

## Screen: content_no_eligible_accounts

```
┌─────────────────────────────────────┐
│ ←  Pay abroad                       │
├─────────────────────────────────────┤
│                                     │
│  [1]──[2]──[3]──[4]──[5]           │
│                                     │
│                                     │
│          [account_balance_wallet]   │  ← icon 48dp (icon.xl); onSurfaceVariant
│                                     │
│   No eligible accounts              │  ← titleMedium; onSurface; centre
│                                     │
│   International payments require    │  ← bodyMedium; onSurfaceVariant; centre
│   a current or savings account.     │
│   Global Money accounts cannot be   │
│   used as a payment source here.    │
│                                     │
│  ┌───────────────────────────────┐  │  ← outlined button; primary border; radius.full
│  │       Go to Accounts          │  │    navigates to accounts tab
│  └───────────────────────────────┘  │
│                                     │
├─────────────────────────────────────┤
│  Home  Accounts  [Pay]  More        │
└─────────────────────────────────────┘
```

---

## Component ↔ API binding table

| Component | API call triggered | Response fields consumed |
|-----------|-------------------|--------------------------|
| debtor_account_list | accounts-list (AISP, on mount) | `SchemeName`, `Identification`, `Balance` |
| confirm_button | POST /international-payment-consents | `Data.ConsentId` → navigate to payment-consent |
| submitting_indicator (ConfirmingFunds) | GET …/funds-confirmation | `Data.FundsAvailableResult.FundsAvailable` |
| submitting_indicator (SubmittingPayment) | POST /international-payments | `Data.InternationalPaymentId` |
| error_panel | all 400 responses | `Errors[*].ErrorCode`, `Errors[*].Path` |

---

## Partial-failure taxonomy

| Failure | HTTP | Surface | Recovery path |
|---------|------|---------|---------------|
| `ChargeBearer` omitted | 400 U004 | error_panel | Implementation fault — always sent |
| `CurrencyOfTransfer` omitted | 400 U004 | error_panel | Implementation fault — always sent |
| Sort-code creditor | 400 U027 | error_panel | Unreachable — form accepts IBAN only |
| 8-char BIC | 400 U002 | error_panel | Return to Recipient; bic_length_error shown client-side first |
| `RemittanceInformation` sent | 400 U005 | error_panel | Implementation fault — no reference field |
| Two-entry error (R13-10) | 400 | error_panel (two rows) | Both rows rendered; PSU reads the second |
| Funds not available | 200 FundsAvailable=NotAvailable | Error(InsufficientFunds) | Return to Amount step |
| Consent rejected by PSU | consent status RJCT | Error(ConsentRejected) | Fresh payment CTA; resubmit not offered |
| Network timeout | IOException | Error(NetworkError) | Retry — idempotency key reused |

---

<!-- Generated 2026-08-07 by /idea-feature-export from screens/pay-international-single/{ui,api,flow,docs,data-flow,demo-data}.yaml. -->
