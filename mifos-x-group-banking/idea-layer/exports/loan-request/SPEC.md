<!--
  generated_from_feature: loan-request
  generated_from_feature_version: "1.0.0"
  contract_version: "2.0.0"
  source_siblings: [ui.yaml, api.yaml, docs.yaml, flow.yaml, tests.yaml]
  generated_by: /idea-feature-export-spec
  status: approved (quality_score 90)
-->

# Loan Request — Feature Spec

## Overview

Member-side (member role, per-group) loan application form. Captures amount, purpose, and
repayment duration; validates the amount locally against `savingsBalance × loanMultiplier`. On
submit, POSTs a `LoanRequestPayload` to the `dt_loan_request` datatable via Ktor, creating a
`PENDING` entry for organizer review at the next group meeting. When `cmp-network-monitor`
reports offline, the payload is queued to `SyncQueue` via SQLDelight for automatic background
retry. Covers FR-016.

**Route:** `/loan-request` · **Entry:** `personal-dashboard` (Request Loan CTA), `personal-loans` (FAB)
**Nav params:** `clientId: Long (required)`, `savingsBalance: Double (required)`, `loanMultiplier: Double (optional, default 3.0)`

**Acceptance Criteria:**

- AC1: `maxLoanAmount = savingsBalance × loanMultiplier`; shown in the savings limit card.
- AC2: `OnAmountChange` is a pure transform — validates against `maxLoanAmount`, recomputes
       `repaymentEstimate`, sets/clears `requestedAmountError`.
- AC3: `isFormValid` true only when amount valid, purpose selected, `durationWeeks > 0`; submit
       enabled only when `isFormValid && !isSubmitting`.
- AC4: Online submit POSTs `/datatables/dt_loan_request`; on success show success dialog →
       navigate to `personal-dashboard`.
- AC5: Offline submit enqueues to `SyncQueue` and transitions to `OfflineQueued` with the offline
       banner + saved confirmation.
- AC6: 401 → session-expired redirect to login; server/validation error → error snackbar with retry.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| loan_request_screen | `LoanRequestScreen` | Scaffold (top-bar + scrollable Column + bottom submit bar) | Loan application form with inline validation and offline queue support |

## State Model

### LoanRequestViewModel

**State — `LoanRequestState`**

| Field | Type | Default | Description |
|---|---|---|---|
| clientId | Long | `0L` | From nav_params |
| savingsBalance | Double | `0.0` | From nav_params |
| loanMultiplier | Double | `3.0` | From nav_params (default 3.0) |
| maxLoanAmount | Double | `0.0` | `savingsBalance × loanMultiplier` |
| requestedAmount | String | `""` | Raw amount input |
| requestedAmountError | String? | `null` | Inline amount error |
| purpose | LoanPurpose? | `null` | Selected purpose |
| purposeError | String? | `null` | Purpose error |
| durationWeeks | Int | `12` | Repayment duration (slider 4–52) |
| repaymentEstimate | Double | `0.0` | Weekly repayment estimate |
| isOfflineMode | Boolean | `false` | Drives offline banner |
| isSubmitting | Boolean | `false` | Submission in flight |
| isFormValid | Boolean | `false` | Enables submit |
| submitError | SubmitError? | `null` | Submission error |
| successDialogVisible | Boolean | `false` | Drives success dialog |

**Screen States — `LoanRequestScreenState`**: `Content`, `Submitting`, `SubmitSuccess`, `SubmitError`, `OfflineQueued`

| State | Components |
|---|---|
| `Content` | top_bar, offline_mode_banner, savings_limit_card, amount_field, purpose_dropdown, duration_selector, repayment_summary_card, submit_button |
| `Submitting` | top_bar, savings_limit_card, form fields, submitting_indicator |
| `SubmitSuccess` | Content fields + success_dialog |
| `SubmitError` | Content fields + error_snackbar |
| `OfflineQueued` | Content fields + offline_mode_banner + success_dialog (offline copy) |

**Errors — `SubmitError`**

| Type | Retry | Message Key | Notes |
|---|---|---|---|
| Network | yes | error_network_queued | Offline — request saved to SyncQueue |
| Server | yes | error_server | 5xx / 503 |
| Validation | no | error_validation | 400 |
| Unauthorized | no | error_session_expired | 401 → login |

**Actions — `LoanRequestAction`**

| Action | Params | Trigger | Effect |
|---|---|---|---|
| `OnAmountChange` | value: String | Type in amount field | transform_state — validate + recompute repaymentEstimate |
| `OnPurposeSelected` | purpose: LoanPurpose | Select purpose | transform_state — set purpose, re-eval isFormValid |
| `OnDurationChanged` | weeks: Int | Slide duration selector | transform_state — set durationWeeks, recompute estimate |
| `OnSubmitClick` | — | Tap Submit Application | call_api — submit_loan_request (offline → SyncQueue) |
| `OnSuccessDialogDismiss` | — | Tap OK on success dialog | navigate — to personal-dashboard |
| `OnRetry` | — | Tap Retry on error snackbar | call_api — re-post, re-queue on offline |

**Events — `LoanRequestEvent`**

| Event | Trigger |
|---|---|
| `NavigateToDashboardAfterSuccess` | Success dialog OK |
| `NavigateBack` | top-bar back → personal-loans |
| `ShowOfflineQueuedConfirmation` | Offline submit queued |

**DI Dependencies**

- `LoanRequestRepository` — submit
- `SyncQueueRepository` — offline enqueue
- `SessionManager`
- `ConnectivityManager` (cmp-network-monitor)

## Navigation

| Condition | Destination | Params |
|---|---|---|
| Submission success | `personal-dashboard` | — |
| top-bar back | `personal-loans` | — |
| Offline queued (dismiss) | `personal-dashboard` | — |

**navigates_to:** `personal-dashboard` (submission_success), `personal-loans` (user_taps_back)

## API Endpoints (1)

| ID | Method | Endpoint | Cache | Writable |
|---|---|---|---|---|
| `submit_loan_request` | POST | `/datatables/dt_loan_request` | no-cache, offline queue_to_syncqueue | yes |

See `exports/loan-request/API.md`.

> Source note: `tests.yaml` (TC-LRQ-003) references a `COMP-GRP-001 /companion/groups/{groupId}/loans`
> path, but the endpoint SoT (`api.yaml`) declares the `dt_loan_request` datatable POST above.
> This spec follows `api.yaml`; the test wording is a source inconsistency to reconcile.

## Flow Logic

| Decision | Branches |
|---|---|
| `amount_validation` | `requestedAmount > maxLoanAmount` → error (max exceeded) · `<= 0` → error (must be positive) · valid → clear error, recompute repaymentEstimate |
| `connectivity_on_submit` | online → POST dt_loan_request, navigate dashboard on 200 · offline → add to SyncQueue, show offline confirmation, navigate dashboard |
| `form_validity` | amount valid && purpose selected && durationWeeks > 0 → isFormValid=true (enable submit) · any invalid → isFormValid=false |

## Dependencies

- **Features:** `end-user-dashboard` (parent flow), `personal-dashboard`, `personal-loans`
- **Libraries:** `cmp-network-monitor`; external: Ktor, SQLDelight
- **Shared entities:** Loan, SyncQueue, Member

## DTOs

See `exports/loan-request/API.md`. Key types: `LoanRequestPayload`, `LoanRequestResponse`,
`SyncQueueEntry`, `LoanPurpose` (SCHOOL_FEES, MEDICAL, BUSINESS, FARMING, HOME_IMPROVEMENT,
EMERGENCY, OTHER).

## Testing (8 scenarios)

| ID | Priority | Scenario |
|---|---|---|
| TC-LRQ-001 | P0 | Eligible amount computed from savingsBalance × loanMultiplier |
| TC-LRQ-002 | P0 | Amount over eligibility disables submit, shows inline error |
| TC-LRQ-003 | P0 | Online submit POSTs and emits SubmitSuccess |
| TC-LRQ-004 | P0 | Offline submit enqueues to SyncQueue → OfflineQueued |
| TC-LRQ-005 | P1 | OfflineQueued shows pending message, navigates on dismiss |
| TC-LRQ-006 | P1 | Server-side SubmitError shows error, allows retry |
| TC-LRQ-007 | P1 | Duration slider range clamped 4–52, default 12 |
| TC-LRQ-008 | P0 | 401 redirects to login-signup |

Coverage targets: ViewModel 90%+, Screen 80%+, Repository 85%+.

## Designed UX Reference

- **Stitch prompts:** `idea-layer/screens/loan-request/prompts/`
- **Preview HTML:** `idea-layer/screens/loan-request/preview/`
- **Design conformance:** secondaryContainer `offline_mode_banner` (wifi_off) shown only when
  `isOfflineMode`. tertiaryContainer `savings_limit_card` shows savings balance + max-borrow
  (3× hint). `amount_field` (KES prefix, currency icon) with inline error + supporting text.
  `purpose_dropdown` (7 options). `duration_selector` card with a 4–52 week slider (12 steps).
  `repayment_summary_card` (principal / interest / total) appears only when the amount is valid.
  Full-width filled submit button (`corner_radius: full`, 56dp) enabled only when the form is valid.
  `success_dialog` (checkmark, primary) and errorContainer `error_snackbar` with Retry cover the
  terminal states.
