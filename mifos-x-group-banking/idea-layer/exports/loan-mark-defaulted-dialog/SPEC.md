<!--
  generated_from_feature: loan-mark-defaulted-dialog
  generated_from_feature_version: "1.0.0"
  contract_version: "2.0.0"
  source_siblings: [ui.yaml, api.yaml, docs.yaml, flow.yaml, tests.yaml]
  generated_by: /idea-feature-export-spec
  status: approved (quality_score 85)
-->

# Mark Loan Defaulted Dialog — Feature Spec

## Overview

Destructive confirmation dialog shown to the chairperson when they tap "Mark Defaulted" on the
`loan-detail` screen. Displays an irreversible warning including the member name and loan amount.
Two actions: **Cancel** (dismiss) and **Mark Defaulted** (error-styled, calls the Fineract
write-off endpoint `POST /loans/{loanId}/transactions?command=writeoff` via
`LoanRepository.markDefaulted`). `cmp-network-monitor` guards connectivity first — there is **no
offline queue** for this destructive action. On success the dialog dismisses, emits
`LoanMarkedDefaulted`, and the Store5/SQLDelight loan cache refreshes so `loan-detail` re-renders.

**Archetype:** dialog · **Parent screen:** `loan-detail`
**Nav params:** `loanId: Long (required)`, `memberName: String (required)`, `loanAmountKes: Double (required)`

**Acceptance Criteria:**

- AC1: Dialog initialises `memberName` and `loanAmountKes` from nav_params on init.
- AC2: Idle state shows the error-tinted warning icon + irreversible warning body + Cancel /
       Mark Defaulted buttons.
- AC3: `OnConfirm` checks connectivity (cmp-network-monitor); if online, POSTs the write-off; on
       success emits `LoanMarkedDefaulted(loanId)` and refreshes cache.
- AC4: Offline → submit blocked, offline warning surfaced, no queue created, `isSubmitting` stays false.
- AC5: Server error → `submitError` set, dialog remains open for retry.
- AC6: `OnDismiss` emits `Dismiss`, closes dialog, makes no API call.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| loan-mark-defaulted-dialog | `LoanMarkDefaultedDialog` | Modal dialog | Destructive confirm dialog (warning icon + body + action row) |

## State Model

### LoanMarkDefaultedDialogViewModel

**State — `LoanMarkDefaultedDialogState`**

| Field | Type | Default | Description |
|---|---|---|---|
| isSubmitting | Boolean | `false` | Write-off call in flight |
| submitError | String? | `null` | Error message shown in dialog |
| memberName | String | `""` | Resolved from nav_params on init |
| loanAmountKes | Double | `0.0` | Resolved from nav_params on init |

**Screen States**: `idle`, `submitting`, `error`

| State | Components |
|---|---|
| `idle` | dialog_title, warning_icon, warning_body_text, dialog_actions_row |
| `submitting` | same as idle (Mark Defaulted shows loading, both buttons disabled) |
| `error` | dialog_title, warning_icon, warning_body_text, submit_error_text, dialog_actions_row |

**Actions — `LoanMarkDefaultedDialogAction`**

| Action | Trigger | Effect |
|---|---|---|
| `OnConfirm` | Tap Mark Defaulted button | call_api — write_off_loan via LoanRepository.markDefaulted (connectivity-gated) |
| `OnDismiss` | Tap Cancel or outside dialog | none — emit Dismiss, no side effect |

**Events — `LoanMarkDefaultedDialogEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `Dismiss` | — | Cancel / outside tap |
| `LoanMarkedDefaulted` | loanId: Long | Write-off success |
| `ShowError` | message: String | Failure |

**DI Dependencies**

- `LoanRepository` — markDefaulted
- (cmp-network-monitor connectivity check)

## Navigation

| Condition | Destination | Params |
|---|---|---|
| Success / Dismiss | back to `loan-detail` (parent) | emits event to parent |

**navigates_to:** `[]` (dialog — resolves to parent `loan-detail`)

## API Endpoints (1)

| ID | Method | Endpoint | Writable |
|---|---|---|---|
| `mark_loan_defaulted` | POST | `/loans/{loanId}/transactions?command=writeoff` | yes |

See `exports/loan-mark-defaulted-dialog/API.md`.

## Flow Logic

| Trigger | Steps |
|---|---|
| `on_confirm` | mark_defaulted (mark_loan_defaulted) → on_success emit_LoanMarkedDefaulted_then_dismiss / on_error set_submitError |
| `on_dismiss` | emit_Dismiss |

## Dependencies

- **Features:** `loan-detail` (parent)
- **Libraries:** `cmp-network-monitor`; external: Store5, SQLDelight
- **Role gate:** chairperson

## DTOs

No feature-local DTOs. Write-off response: `{ officeId, clientId, loanId, resourceId }`.
See `exports/loan-mark-defaulted-dialog/API.md`.

## Testing (7 scenarios)

| ID | Priority | Scenario |
|---|---|---|
| TC-LMD-001 | P0 | Dialog initialises memberName + loanAmountKes from nav_params |
| TC-LMD-002 | P0 | Warning icon + confirmation message visible in Idle |
| TC-LMD-003 | P0 | OnConfirm POSTs writeoff, emits LoanMarkedDefaulted, refreshes cache |
| TC-LMD-004 | P0 | Offline check blocks submit; no offline queue (irreversible) |
| TC-LMD-005 | P1 | Server error shows submitError; dialog stays open |
| TC-LMD-006 | P0 | OnDismiss fires Dismiss, closes dialog, no API call |
| TC-LMD-007 | P1 | Loading indicator on Mark Defaulted while isSubmitting |

Coverage targets: ViewModel 90%+, Screen 80%+, Repository 85%+.

## Designed UX Reference

- **Stitch prompts:** `idea-layer/screens/loan-mark-defaulted-dialog/prompts/`
- **Preview HTML:** `idea-layer/screens/loan-mark-defaulted-dialog/preview/`
- **Design conformance:** centered `warning_amber` icon (48dp, error color) above a centered
  irreversible-warning body that interpolates `memberName` and the KES amount. `submit_error_text`
  (error color) appears between body and actions only when `submitError != null`. End-aligned action
  row: outlined Cancel + filled error-colored Mark Defaulted (24dp radius) that shows a spinner and
  disables Cancel while submitting.
