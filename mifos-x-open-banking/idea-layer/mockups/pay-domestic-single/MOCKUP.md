# pay-domestic-single — Mockup Guide

> Source: `screens/pay-domestic-single/{ui,docs,demo-data}.yaml`
> Design system: Open Banking — Trust Blue (Material 3, seed #266489)
> Feature contract: 2.1.0

---

## 1. Screen Overview

One route, four internal steps. The screen never navigates away mid-form (except to the
bank's own authorisation browser via `payment-consent`). Steps share a single ViewModel and a
persistent `step_indicator` at the top.

| Step | Visible components |
|---|---|
| 1 — Account | step_indicator, debtor_account_list, [ineligible_accounts_note] |
| 2 — Payee | step_indicator, beneficiary_list, enter_manually_button, [sort_code_field, account_number_field, payee_name_field] |
| 3 — Amount | step_indicator, amount_field, [amount_error], reference_field |
| 4 — Review | step_indicator, review_card, confirm_button |

Bracketed components are conditionally visible within that step.

---

## 2. State-by-State Descriptions

### 2.1 `loading` state

Top app bar shows "Pay someone" with a back/close navigation icon. Below it, the
`step_indicator` is visible but the four step labels (Account · Payee · Amount · Review) render
as narrow shimmer rectangles — no text visible. The rest of the content area is a skeleton: a
shimmer rectangle spanning full width at roughly list-item height (56dp) repeated 3× for the
account slots below. No text, no real account names, no interactive elements beyond the top bar.
Background: `surface` (`#F7F9FF`). Shimmer fill: `surfaceContainerLow` (`#F1F4F9`) with a
left-to-right sweep at opacity transitions. Bottom nav visible with Pay tab active
(`primary` colour, `#266489`).

### 2.2 `content` state — Step 1: Account

Top bar: "Pay someone", back icon.

**4-step horizontal stepper** at top, currently on step 1 ("Account" label active in `primary`,
steps 2–4 in `onSurfaceVariant`).

**Debtor account list** (label: "Pay from"):
- Row 1: "Current account" · "80200110203349" · "£1,250.00 available" — trailing chevron right
- Row 2: "Current account 2" · "80200110203348" · "£480.00 available" — trailing chevron right
- Row 3: "BMM ACCOUNT" · "80122590953695" · "£8,000.00 available" — trailing chevron right

Each row: 48dp min height, leading bank glyph (placeholder account icon in `primary`), primary
text in `onSurface` `bodyLarge`, supporting text (identification) in `onSurfaceVariant`
`bodyMedium`, trailing mono balance in `primary` (positive, `semantic.money.credit`).

**ineligible_accounts_note** (visible — hiddenAccountCount = 2):
Inline text below the list: "2 accounts can't be used for this payment type. Only UK sort-code
accounts are supported." Typography: `bodySmall`, colour: `onSurfaceVariant`.

No next/continue button — tapping an account row advances automatically (SelectDebtorAccount
action).

### 2.3 `content` state — Step 2: Payee

Stepper advances to step 2 ("Payee" label active).

**Beneficiary list** (label: "Pay to"):
- Row 1: "Mr Mark" · sort-code icon · "80200110203349" — trailing chevron
- Row 2: "Ramu" · sort-code icon · "40200110203351" — trailing chevron

**enter_manually_button** below the list: text variant, label "Enter details manually",
`primary` colour, no background — inline secondary action.

When enter_manually_button is tapped (manualEntryVisible = true), three fields appear below:
- **Sort code** field: label "Sort code", placeholder "00-00-00", numeric keyboard, max 8 chars,
  `text_field` with `radius.sm` corners, outline in `outline` (`#72787E`), focus outline in
  `primary` (`#266489`) at 2dp.
- **Account number** field: label "Account number", numeric keyboard, max 8 digits.
- **Payee name** field: label "Payee name" — MANDATORY. When blank and the user tries to
  advance, inline error below field in `error` (`#BA1A1A`) `bodySmall`.

### 2.4 `content` state — Step 3: Amount

Stepper on step 3.

**Amount field**: large mono display — `headlineSmall` Roboto Mono — with a non-editable "£"
prefix in `onSurfaceVariant`. Field outline as per text_field tokens. Numeric keyboard.

When validation fires after first blur:
- `amount_error` text appears below the field.
  - NotANumber → "Please enter a valid amount"
  - NotPositive → "Amount must be greater than zero"
  - ExceedsAvailableBalance → "Amount exceeds your available balance"
  Error text colour: `error` (`#BA1A1A`), `bodySmall`.

**Reference field** below amount: label "Reference (optional)", helper "Up to 35 characters.
Visible to the payee.", max_length 35, standard keyboard.

Note: This field is ABSENT on international rails. Its presence here is by design and per the
rail spec.

Continue button (or stepper advance) moves to Review.

### 2.5 `content` state — Step 4: Review

Stepper on step 4.

**review_card** (M3 Card, `surfaceContainer` fill `#EBEEF3`, `radius.md` 12dp corners,
elevation 1):

| Row | Label | Value |
|---|---|---|
| From | "Pay from" | "Current account · 802001 10203349" |
| To | "Pay to" | "Mr Mark · 802001 10203348" |
| Amount | "Amount" | "£15.55" (Roboto Mono, `onSurface`) |
| Reference | "Reference" | "Rent August" (hidden when blank) |
| Fee | "Fee" | "£0.05" (populated from Charges[] after staging; shows "Calculating…" before consent exists) |

**confirm_button**: filled pill, `primary` background (`#266489`), label "Send £15.55"
(`onPrimary` white, `labelLarge`), full-width minus 16dp margins, `radius.full` (pill shape).
NOTE: CTA label MUST include the amount on this rail — per irreversible_action.cta_label_by_rail.

Back arrow in top bar / stepper back step reverts to Amount step (no pop, step transition).
Cancel icon or text (secondary) beside confirm navigates back to payments hub.

### 2.6 `content_no_eligible_accounts` state

Stepper visible (step 1 active). No account list. Full-width **empty_state** component centred:
- Title: "No eligible accounts" (`headlineSmall`, `onSurface`)
- Body: "This payment type requires a UK sort-code account. Your other accounts can't be used
  here." (`bodyMedium`, `onSurfaceVariant`)

No "Add account" CTA — omitting DebtorAccount is not exposed in this form. The PSU needs a
sort-code account to use this rail, and the screen truthfully says so.

### 2.7 `submitting` state

Stepper visible. confirm_button is GONE (unmounted, not disabled — the state-transition-unmount
guard). Replaced by **submitting_indicator** (progress/spinner, centred):

Label text below the indicator reflects the current SubmittingStage:
- `StagingConsent` → "Creating payment…"
- `AwaitingAuthorisation` → "Waiting for your bank…"
- `ConfirmingFunds` → "Checking available funds…"
- `SubmittingPayment` → "Sending payment…"

Indicator: `primary` colour circular indeterminate progress. The screen is non-interactive
during this phase. The step_indicator remains visible but all step items are dimmed
(`opacity.disabled` = 0.38).

### 2.8 `error` state

Step indicator visible. **error_panel** (full-width, `errorContainer` fill `#FFDAD6`,
`radius.md` corners, `error` icon at top):

Title: "Something went wrong" (`titleMedium`, `onErrorContainer`).

Below title: every entry in `Errors[]` is rendered separately — not only `[0]`. Each entry
shows the user-facing copy keyed from `ErrorCode + Path` (case-insensitive match on Path).

Example (NetworkError): body "We couldn't reach the server. Please check your connection." +
Retry button (filled, `primary`).

Example (ConsentNotAuthorised / U009): body "Your bank hasn't authorised this payment yet." +
"Re-authorise" CTA button (filled, `primary`).

Example (ConsentRevoked / 403): body "This consent has been revoked." + "View Consents" CTA
button navigating to consent-list.

No Retry on SignatureMissing (U019) or InitiationMismatch (U008) — those show a support
reference instead.

---

## 3. Component Hierarchy

### Top App Bar

```
TopAppBar [Fill × 64dp, Auto Layout Horizontal, padding 16dp]
  ├─ NavigationIcon: arrow_back (icon.md = 24dp, onSurface)
  ├─ Title: "Pay someone" (titleLarge, onSurface, Fill)
  └─ Actions: [] (none declared)
```

Tokens: `top_app_bar.container` = `surface` (#F7F9FF), `top_app_bar.title` = `onSurface` (#181C20).

### Step Indicator

```
StepperRow [Fill × 48dp, Auto Layout Horizontal, gap spacing.sm=8dp, padding H:16dp]
  ├─ StepItem[1] "Account"  (active  → labelMedium, primary #266489)
  ├─ Divider (outlineVariant, 1dp)
  ├─ StepItem[2] "Payee"    (pending → labelMedium, onSurfaceVariant #41474D)
  ├─ Divider
  ├─ StepItem[3] "Amount"   (pending → labelMedium, onSurfaceVariant)
  ├─ Divider
  └─ StepItem[4] "Review"   (pending → labelMedium, onSurfaceVariant)
```

### Debtor Account List Item

```
ListItem [Fill × 56dp min, Auto Layout Horizontal, padding H:16dp V:8dp, gap spacing.md=16dp]
  ├─ LeadingIcon: account_balance (icon.md=24dp, primary)
  ├─ ContentColumn [Auto Layout Vertical, Fill, gap spacing.xs=4dp]
  │   ├─ PrimaryText: "Current account" (bodyLarge, onSurface)
  │   └─ SupportText: "80200110203349" (bodyMedium, onSurfaceVariant, Roboto Mono)
  └─ TrailingContent: "£1,250.00" (bodyLarge, Roboto Mono, primary) + chevron_right icon
```

Ripple on press (onSurface at opacity.pressed = 0.12). Touch target: 48dp minimum.

### Ineligible Accounts Note

```
TextRow [Fill × Hug, padding H:16dp V:8dp]
  └─ Text: "2 accounts can't be used for this payment type…" (bodySmall, onSurfaceVariant)
```

### Manual Entry Fields

```
Column [Fill, Auto Layout Vertical, gap spacing.sm=8dp, padding H:16dp]
  ├─ SortCodeField [text_field, radius.sm=8dp, min_height=56dp]
  │   ├─ Label: "Sort code" (bodySmall, onSurfaceVariant)
  │   └─ Input: "00-00-00" placeholder (bodyLarge, onSurface, Roboto Mono)
  ├─ AccountNumberField [text_field, same spec]
  │   └─ Label: "Account number"
  └─ PayeeNameField [text_field, same spec]
      ├─ Label: "Payee name"
      └─ [ErrorText: "Payee name is required" (bodySmall, error #BA1A1A) when empty + blur]
```

### Amount Field

```
AmountField [Fill, Auto Layout Horizontal, min_height=56dp, padding H:16dp, radius.sm=8dp]
  ├─ Prefix: "£" (headlineSmall, onSurfaceVariant, non-editable)
  └─ Input [Fill] (headlineSmall, Roboto Mono, onSurface)
```

Below field when amountProblem != null:
```
ErrorText: "<problem message>" (bodySmall, error #BA1A1A)
```

### Review Card

```
ReviewCard [Fill, Auto Layout Vertical, padding spacing.md=16dp, gap spacing.sm=8dp,
  radius.md=12dp, container=surfaceContainer #EBEEF3, elevation=1]
  ├─ ReviewRow "Pay from" / "Current account · 802001 10203349"
  ├─ ReviewRow "Pay to"   / "Mr Mark · 802001 10203348"
  ├─ ReviewRow "Amount"   / "£15.55" (Roboto Mono)
  ├─ ReviewRow "Reference"/ "Rent August" (hidden when blank)
  └─ ReviewRow "Fee"      / "£0.05" (Roboto Mono, onSurfaceVariant, from Charges[])
```

Each ReviewRow: horizontal flex, label `bodyMedium onSurfaceVariant`, value `bodyLarge onSurface`.

### Confirm Button

```
FilledPillButton [Fill minus 32dp, height=56dp, radius.full=9999dp,
  container=primary #266489, label=onPrimary #FFFFFF, labelLarge]
  Label: "Send £15.55"
```

On tap: button UNMOUNTS (state transition to Submitting), replaced by submitting_indicator.
This makes double-submit structurally impossible.

### Error Panel

```
ErrorPanel [Fill, Auto Layout Vertical, padding spacing.md=16dp, gap spacing.sm=8dp,
  container=errorContainer #FFDAD6, radius.md=12dp]
  ├─ Icon: error (icon.lg=32dp, onErrorContainer #93000A)
  ├─ Title: "Something went wrong" (titleMedium, onErrorContainer)
  ├─ [FOR EACH entry in Errors[]]:
  │   └─ ErrorMessage: "<copy from ErrorCode+Path lookup>" (bodyMedium, onErrorContainer)
  └─ [RetryButton or SupportRefButton depending on error.type]
```

### Bottom Navigation

```
BottomNav [Fill × 80dp, container=surfaceContainer #EBEEF3]
  ├─ Tab: Home       (home icon, inactive = onSurfaceVariant)
  ├─ Tab: Accounts   (account_balance, inactive)
  ├─ Tab: Pay        (payments, ACTIVE = primary #266489, labelSmall bold)
  └─ Tab: More       (more_horiz, inactive)
```

---

## 4. Component ↔ API Binding Table

| Component | ViewModel Action | API Call | State Transition |
|---|---|---|---|
| `debtor_account_list` row tap | `SelectDebtorAccount(accountId)` | None (local filter) | Content(Account) → Content(Payee) |
| `beneficiary_list` row tap | `SelectCreditor(BeneficiarySelection)` | None (local filter) | Content(Payee) → Content(Amount) |
| `confirm_button` tap | `ConfirmAndStageConsent` | POST /domestic-payment-consents | Content(Review) → Submitting(StagingConsent) |
| Auto (resume from payment-consent) | `ConfirmFunds(consentId)` | GET /domestic-payment-consents/{id}/funds-confirmation | Submitting(ConfirmingFunds) |
| Auto (funds Available) | `SubmitPayment(consentId)` | POST /domestic-payments | Submitting(SubmittingPayment) → NavigateToPaymentStatus |
| error state Retry button | `RetrySubmit` | Re-runs submit (same idempotency key) | Error → Submitting(SubmittingPayment) |
| error state Re-authorise | `NavigateToPaymentConsent` | (navigation only) | Error → payment-consent |
| error state View Consents | (navigation) | (navigation only) | Error → consent-list |

---

## 5. Partial-Failure Taxonomy

| Failure | When | UI Surface | User Path |
|---|---|---|---|
| `NetworkError` on stage | IOException / timeout during POST /domestic-payment-consents | error_panel + Retry | Retry re-uses same idempotency key — safe, no double stage |
| `NetworkError` on submit | IOException / timeout during POST /domestic-payments | error_panel + Retry | Retry re-uses same idempotency key — safe, no double charge |
| `TokenExpired` (401) | Client-credentials or PSU token expired | error_panel + Retry | Retry after token refresh |
| `SignatureMissing` (U019) | x-jws-signature omitted or malformed | error_panel + Support ref | Not user-recoverable; show OB envelope ID for support |
| `ConsentNotAuthorised` (U009) | PSU did not complete bank auth before submit | error_panel + Re-authorise CTA | Re-authorise CTA re-enters payment-consent |
| `InitiationMismatch` (U008) | Submitted Initiation does not match authorised consent | error_panel + Support ref | Not user-recoverable; re-read authorised consent in next attempt |
| `InsufficientFunds` | GET funds-confirmation returns FundsAvailable=false | error_panel (returns to Amount step) | PSU changes the amount |
| `ConsentRevoked` (403) | Bank revoked the consent | error_panel + View Consents CTA | Navigate to consent-list |
| `IneligibleAccount` (U002 / U027) | Ineligible debtor or creditor reached API | error_panel (should be unreachable) | Return to account or payee step |
| Multiple Errors[] entries | Bank returns 2 entries simultaneously (R13-10, R9-11) | error_panel iterates ALL entries | Each entry shown separately; both must be resolved |
| ACSP on submit response | Normal — settlement is async, batched | in_progress chip in payment-status | Not a failure; poll until ACCC or RJCT |
