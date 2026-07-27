<!--
  generated_from_feature: loan-repayment-dialog
  generated_from_feature_version: "1.0.0"
  contract_version: "2.0.0"
  source_siblings: [ui.yaml, api.yaml, docs.yaml, flow.yaml, tests.yaml]
  generated_by: /idea-feature-export-spec
  status: approved (quality_score 85)
-->

# Loan Repayment Dialog — Feature Spec

## Overview

Modal dialog letting the treasurer record a loan repayment for a specific member. Pre-fills the
amount from the current schedule installment (nav param). Validates the entered amount is a
positive number within the outstanding balance (via `InputValidator`), resolves the selected
`PaymentMethod` to a Fineract `paymentTypeId` (MPESA=1, CASH=2), then POSTs a repayment against
`m_loan` via `make_repayment` (`POST /loans/{loanId}/transactions?command=repayment`).
`cmp-network-monitor` gates submission offline; the money move is idempotent so a retry after a
timeout never double-posts. On success it dismisses, emits `RepaymentRecorded`, and triggers a
refresh on the parent `loan-detail`.

**Archetype:** dialog · **Parent screen:** `loan-detail`
**Nav params:** `loanId: Long (required)`, `memberId: Long (required)`, `installmentAmount: Double (required)`

**Acceptance Criteria:**

- AC1: Dialog opens with `amount` pre-filled from `installmentAmount`; `paymentMethod` defaults MPESA.
- AC2: `OnAmountChanged` runs the positive-number check inline; invalid entry sets `amountError`
       and keeps submit disabled.
- AC3: Valid amount clears `amountError` and enables submit.
- AC4: Payment method chips (MPESA / CASH) are single-select; optional reference number carried
       into `receiptNumber`.
- AC5: `OnSubmit` re-validates, POSTs repayment; on success emits `RepaymentRecorded(loanId)` and
       dismisses; cache refreshed.
- AC6: `cmp-network-monitor` blocks offline submit; server error sets `submitError` and keeps the
       dialog open.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| loan-repayment-dialog | `LoanRepaymentDialog` | Modal dialog | Amount + payment-method + reference form with action row |

## State Model

### LoanRepaymentDialogViewModel

**State — `LoanRepaymentDialogState`**

| Field | Type | Default | Description |
|---|---|---|---|
| amount | String | `""` | Pre-filled from installmentAmount nav param |
| paymentMethod | PaymentMethod | `PaymentMethod.MPESA` | Selected payment method |
| referenceNumber | String | `""` | Optional M-Pesa receipt code |
| isSubmitting | Boolean | `false` | Repayment call in flight |
| amountError | String? | `null` | Inline amount validation error |
| submitError | String? | `null` | API error message |

**Screen States**: `idle`, `submitting`, `error`

| State | Components |
|---|---|
| `idle` | dialog_title, amount_field, payment_method_label, payment_method_chips, reference_number_field, dialog_actions_row |
| `submitting` | same as idle (Record Repayment shows loading, inputs disabled) |
| `error` | idle components + submit_error_text |

**Actions — `LoanRepaymentDialogAction`**

| Action | Params | Trigger | Effect |
|---|---|---|---|
| `OnAmountChanged` | value: String | Edit amount field | transform_state — update amount, clear amountError, run positive-number check |
| `OnPaymentMethodSelected` | method: PaymentMethod | Select payment method chip | transform_state — set paymentMethod (resolves paymentTypeId) |
| `OnReferenceNumberChanged` | value: String | Edit reference field | transform_state — update referenceNumber |
| `OnSubmit` | — | Tap Record Repayment | call_api — make_repayment (idempotent, connectivity-gated) |
| `OnDismiss` | — | Tap Cancel or outside dialog | navigate — emit Dismiss, discard entries |

**Events — `LoanRepaymentDialogEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `Dismiss` | — | Cancel / outside tap |
| `RepaymentRecorded` | loanId: Long | Repayment success |
| `ShowError` | message: String | Failure |

**DI Dependencies**

- `LoanRepository` — recordRepayment
- `InputValidator` — positive-number / within-outstanding checks
- (cmp-network-monitor connectivity check)

## Navigation

| Condition | Destination | Params |
|---|---|---|
| Success / Dismiss | back to `loan-detail` (parent) | emits event to parent |

**navigates_to:** `[]` (dialog — resolves to parent `loan-detail`)

## API Endpoints (1)

| ID | Method | Endpoint | Writable |
|---|---|---|---|
| `make_repayment` | POST | `/loans/{loanId}/transactions?command=repayment` | yes |

See `exports/loan-repayment-dialog/API.md`.

## Flow Logic

| Trigger | Steps |
|---|---|
| `on_open` | pre_fill_amount (installmentAmount → amount string) |
| `on_submit` | validate_amount (guard: > 0 and numeric, on_fail set_amountError) · post_repayment (make_repayment) → on_success emit_RepaymentRecorded_then_dismiss / on_error set_submitError |
| `on_dismiss` | emit_Dismiss |

## Dependencies

- **Features:** `loan-detail` (parent)
- **Libraries:** `cmp-network-monitor`; external: Store5, SQLDelight
- **Role gate:** treasurer

## DTOs

`PaymentMethod` enum (MPESA "M-Pesa", CASH "Cash"). See `exports/loan-repayment-dialog/API.md`.

## Testing (9 scenarios)

| ID | Priority | Scenario |
|---|---|---|
| TC-LRD-001 | P0 | Dialog initialises from nav_params; paymentMethod defaults MPESA |
| TC-LRD-002 | P0 | Non-numeric / zero amount shows inline error, disables submit |
| TC-LRD-003 | P0 | Valid amount clears amountError, enables submit |
| TC-LRD-004 | P1 | Payment method defaults MPESA; can switch to CASH |
| TC-LRD-005 | P1 | Reference number field optional (shown for MPESA) |
| TC-LRD-006 | P0 | OnSubmit POSTs repayment, emits RepaymentRecorded, refreshes cache |
| TC-LRD-007 | P1 | Server error shows submitError; dialog stays open |
| TC-LRD-008 | P0 | OnDismiss closes dialog without API call |
| TC-LRD-009 | P1 | Loading spinner on Record Repayment while isSubmitting |

Coverage targets: ViewModel 90%+, Screen 80%+, Repository 85%+.

## Designed UX Reference

- **Stitch prompts:** `idea-layer/screens/loan-repayment-dialog/prompts/`
- **Preview HTML:** `idea-layer/screens/loan-repayment-dialog/preview/`
- **Design conformance:** decimal-keyboard `amount_field` (8dp radius) with inline `amountError`;
  single-select `payment_method_chips` (M-Pesa / Cash) styled primaryContainer when selected;
  optional `reference_number_field` for the receipt code. `submit_error_text` (error color) appears
  above the action row only when `submitError != null`. End-aligned actions: text Cancel + filled
  primary Record Repayment (24dp radius) that shows a spinner and disables inputs while submitting.
