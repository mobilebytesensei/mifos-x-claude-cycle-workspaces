<!--
  generated_from_feature: meeting-conduct
  generated_from_feature_version: "1.0.0"
  contract_version: "2.0.0"
  source_siblings: [ui.yaml, api.yaml, docs.yaml, flow.yaml, tests.yaml]
  generated_by: /idea-feature-export-spec
  status: approved (quality_score 92)
-->

# Meeting Conduct — Feature Spec

## Overview

THE CORE SCREEN — a stateful 7-step (0-indexed) wizard for conducting a weekly group meeting.
Steps: Previous Meeting Review (0), Attendance (1), Opening Balance (2), Savings Collection (3),
Loan Review (4), Loan Applications (5), Closing Balance (6). Loads members, corpus, and active
loans via Fineract REST, then records attendance, savings, loan repayments, votes, and
disbursements in local state. On submit it sequences POSTs through the Fineract collection-sheet
backend in a strict order; on any 5xx or offline it persists the full payload to a SQLDelight
`sync_queue` and drains it via Store5 on reconnect. Wizard state is persisted to the local DB on
each step advance. A **corpus gate** blocks loan disbursement when the closing corpus would go
negative. Covers FR-003/FR-004/FR-006/FR-012/FR-017/FR-019/FR-020.

**Route:** `/meetings/{meetingId}/conduct` · **Entry:** `meeting-calendar` (Start Meeting on upcoming card)
**Nav params:** `meetingId: String (required)`, `meetingNumber: Int (required)`, `centerId: Int (required)`

**Acceptance Criteria:**

- AC1: On mount, parallel-load previous record + members + corpus + active loans + loan votes;
       success → Content, any failure → SubmitError.
- AC2: Step 1 requires attendance for all members; late = KES 50 / absent = KES 100 auto-fine.
- AC3: Step 3 requires each member's group savings ≥ KES 200; recomputes runningSavingsTotal.
- AC4: Step 4 repayment must not exceed the loan's outstanding balance.
- AC5: Step 5 corpus gate: `prospectiveClosing = openingCorpus + savings + repayments + fines −
       disbursed − disbursementAmount`; if `< 0` → CorpusInsufficient.
- AC6: Step 6 computes `closingCorpus`; Submit runs the ordered 6-call sequence online, or
       enqueues the full payload to `sync_queue` (ordered priority) offline (optimistic success).

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| meeting-conduct-screen | `MeetingConductScreen` | Column (TopAppBar + StepperHeader + CorpusBand + StepContent + NavigationFooter) | Full-screen 7-step wizard with sticky stepper and back/next footer |

## State Model

### MeetingConductViewModel

**State — `MeetingConductState`** (key fields)

| Field | Type | Default | Description |
|---|---|---|---|
| currentStep | Int | `0` | Active wizard step (0–6) |
| totalSteps | Int | `7` | Total steps |
| meetingId | String | `""` | From nav_params |
| meetingNumber | Int | `0` | From nav_params |
| centerId | Int | `0` | From nav_params |
| previousMeetingSummary | PreviousMeetingSummary? | `null` | Step 0 review data |
| groupMembers | List<GroupMember> | `emptyList()` | Members for attendance/savings |
| attendanceMap | Map<String, AttendanceStatus> | `emptyMap()` | Per-member attendance |
| lateFines / absentFines | Map<String, Long> | `emptyMap()` | Auto-derived fines |
| openingCorpus | Long | `0L` | Step 2 opening corpus |
| cashOnHand | Long | `0L` | Step 2 cash |
| savingsMap | Map<String, SavingsEntry> | `emptyMap()` | Per-member group + individual savings |
| runningSavingsTotal | Long | `0L` | Sum of savings |
| activeLoans | List<LoanSummary> | `emptyList()` | Step 4 loans |
| loanRepayments | Map<String, Long> | `emptyMap()` | Per-loan repayment |
| loanFines | Map<String, Long> | `emptyMap()` | Per-loan overdue fine |
| pendingLoanApplications | List<LoanApplication> | `emptyList()` | Step 5 applications |
| loanVotes | Map<String, LoanVote> | `emptyMap()` | Per-application vote |
| closingCorpus | Long | `0L` | Step 6 computed close |
| totalCashCollected / totalLoansDisbursed / totalRepayments / totalFinesCollected | Long | `0L` | Aggregates |
| isSubmitting | Boolean | `false` | Submit sequence in flight |
| isOffline | Boolean | `false` | Drives offline chip/note |
| submitError | String? | `null` | Submit failure |
| stepValidationError | String? | `null` | Step gate failure |
| isSavingProgress | Boolean | `false` | Local persist in flight |

**Screen States — `MeetingConductScreenState`**: `Loading`, `Content`, `Submitting`, `SubmitSuccess`, `SubmitError`

| State | Components |
|---|---|
| `Loading` | top_app_bar, step_stepper (5 parallel fetches) |
| `Content` | top_app_bar, step_stepper, corpus_band (steps ≥2), step0..step6 content, wizard_footer |
| `Submitting` | top_app_bar, step_stepper, corpus_band, step6, wizard_footer (overlay progress) |
| `SubmitSuccess` | brief toast → navigate to meeting-summary |
| `SubmitError` | step6 + submit_error_snackbar (Retry; offline → optimistic success) |

**Errors**

| Error | Message |
|---|---|
| CorpusInsufficient | "Corpus balance insufficient to disburse this loan. Current corpus: KES {{currentCorpus}}." |
| AttendanceIncomplete | "Please record attendance for all {{totalMembers}} members before proceeding." |
| SavingsValidation | "Savings amount cannot exceed KES 10,000 per member per meeting." |
| SubmitFailed | "Meeting submission failed. Data saved offline and will sync when connected." |
| MinContributionNotMet | "{{member_name}} has not met the minimum contribution of KES {{min_amount}}." |
| RepaymentExceedsBalance | "Repayment amount exceeds outstanding balance for {{member_name}}." |

**Actions — `MeetingConductAction`**

| Action | Params | Trigger | Effect |
|---|---|---|---|
| `LoadMeetingData` | — | Screen enters composition | call_api — 5 parallel fetches |
| `NextStep` | — | Tap Next/Continue | transform_state — validate + advance + save progress |
| `PreviousStep` | — | Tap Back | transform_state — decrement step (preserve data) |
| `SetAttendance` | memberId, status | Tap attendance toggle | transform_state — set status + auto-fine |
| `SetSavingsAmount` | memberId, amount, type | Edit savings input | transform_state — update savingsMap + runningSavingsTotal |
| `SetLoanRepayment` | loanId, amount | Edit repayment input | transform_state — update loanRepayments + totalRepayments |
| `SetLoanFine` | loanId, fineAmount | Edit fine input | transform_state — update loanFines + totalFinesCollected |
| `CastLoanVote` | loanId, vote | Tap For/Against | transform_state — update loanVotes tally |
| `ApproveLoanApplication` | loanId | Chairperson taps Approve | transform_state — mark approved (corpus-gated) |
| `SubmitMeeting` | — | Tap Submit on step 6 | call_api — ordered 6-call submit sequence |
| `ViewFullPreviousMeeting` | — | Tap View Full Report (step 0) | navigate — to previous-meeting-review |
| `SaveProgressLocally` | — | App background / step advance | persist — meeting_wizard_state |
| `DismissError` | — | Snackbar dismiss | emit_event — clear stepValidationError |

**Events — `MeetingConductEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToMeetingSummary` | meetingId, meetingNumber, centerId | Submit success |
| `NavigateToPreviousMeetingReview` | meetingId, centerId | View Full Report |
| `NavigateBack` | — | Close / back |
| `ShowStepError` | message: String | Step validation fail |
| `ShowSubmitSuccess` | — | Submit success |
| `ShowSubmitError` | message: String | Submit fail |

**DI Dependencies**

- `MeetingRepository`, `SavingsRepository`, `LoanRepository`, `CorpusRepository`, `SyncQueueRepository`
- `NavigationManager`, `ConnectivityObserver` (cmp-network-monitor), `LocalMeetingDao`

## Navigation

| Condition | Destination | Params |
|---|---|---|
| Wizard submitted successfully | `meeting-summary` | meeting_id, meeting_number, center_id |
| Tap View Full Previous Meeting | `previous-meeting-review` | meeting_id, meeting_number, center_id |
| Back / cancel | `meeting-calendar` | — |

**navigates_to:** `meeting-summary`, `previous-meeting-review`, `meeting-calendar`

## API Endpoints (11 — 5 read, 6 write)

| ID | Method | Endpoint | Writable |
|---|---|---|---|
| `get_previous_meeting_record` | GET | `/datatables/dt_meeting_record/{centerId}` | no |
| `get_group_members` | GET | `/centers/{centerId}` | no |
| `get_group_corpus` | GET | `/datatables/dt_group_corpus/{centerId}` | no |
| `get_active_loans` | GET | `/loans` | no |
| `get_loan_votes` | GET | `/datatables/dt_loan_vote/{loanId}` | no |
| `post_meeting_record` | POST | `/datatables/dt_meeting_record` | yes (submit #1) |
| `post_meeting_attendance` | POST | `/datatables/dt_meeting_attendance` | yes (submit #2, per member) |
| `post_savings_transaction` | POST | `/savingsaccounts/{savingsId}/transactions` | yes (submit #3, per member per type) |
| `post_loan_repayment` | POST | `/loans/{loanId}/transactions?command=repayment` | yes (submit #4, per loan) |
| `post_loan_disbursal` | POST | `/loans/{loanId}/transactions?command=disburse` | yes (submit #5, per approved) |
| `patch_corpus` | PUT | `/datatables/dt_group_corpus/{centerId}` | yes (submit #6) |

See `exports/meeting-conduct/API.md`.

## Flow Logic

**screen_init:** parallel_load (5 APIs) → all success = Content + emit meeting_started; any failure = SubmitError.

**step_advance gates:**

| Step | Validation | On valid |
|---|---|---|
| 0 Review | none | advance |
| 1 Attendance | all members' attendance set (else AttendanceIncomplete) | auto-calc fines (late 50 / absent 100), update totalFinesCollected, save, advance |
| 2 Opening Balance | none | save, advance |
| 3 Savings | all savings ≥ 200 (else MinContributionNotMet) | update runningSavingsTotal, save, advance |
| 4 Loan Review | repayments ≤ outstanding (else RepaymentExceedsBalance) | update totalRepayments, save, advance |
| 5 Loan Applications | corpus gate (prospectiveClosing ≥ 0 else CorpusInsufficient) | update totalLoansDisbursed, save, advance |
| 6 Closing | compute `closingCorpus = openingCorpus + savings + repayments + fines − disbursed` | enable Submit |

**submit_meeting:**
- Online → Submitting → sequential (1 record → 2 attendance/member → 3 savings/member/type → 4 repayment/loan → 5 disbursal/approved → 6 patch corpus) → all 2xx = SubmitSuccess + navigate meeting-summary; any 5xx = fall through to offline path.
- Offline → enqueue all payloads to sync_queue (ordered priority, keyed by meeting_id) → optimistic SubmitSuccess + offline toast + navigate meeting-summary (cached) + emit meeting_submitted(is_offline=true).

## Dependencies

- **Features:** `meeting-calendar` (entry), `meeting-summary`, `previous-meeting-review`
- **Libraries:** `cmp-network-monitor`; external: fineract-rest, sqldelight, store5
- **Local DB tables:** meeting_wizard_state (LocalMeetingDao), sync_queue (SyncQueueDao)

## DTOs

See `exports/meeting-conduct/API.md`. Key types: `GroupMember`, `AttendanceStatus` (PRESENT,
LATE, ABSENT), `SavingsEntry`, `SavingsType` (GROUP_LINKED, INDIVIDUAL), `LoanSummary`,
`LoanApplication`, `LoanVote` (FOR, AGAINST, ABSTAIN), `PreviousMeetingSummary`,
`CorpusRecord`, and the six submit request DTOs.

## Testing (12 scenarios)

| ID | Priority | Scenario |
|---|---|---|
| TC-MCO-001 | P0 | On mount, meeting data loads; wizard starts at attendance |
| TC-MCO-002 | P0 | Attendance step marks member present/absent |
| TC-MCO-003 | P0 | Next advances attendance → savings |
| TC-MCO-004 | P0 | Savings step records per-member collection amount |
| TC-MCO-005 | P1 | Loans step records disbursement for approved loans |
| TC-MCO-006 | P1 | Votes step records resolution outcome |
| TC-MCO-007 | P0 | Offline submit queues meeting data to sync_queue |
| TC-MCO-008 | P0 | Online submit POSTs outcomes; emits MeetingCompleted → summary |
| TC-MCO-009 | P1 | Back from first step shows abort confirmation |
| TC-MCO-010 | P1 | Previous step moves wizard one step back |
| TC-MCO-011 | P1 | Error state shows retry on load failure |
| TC-MCO-012 | P2 | Step progress indicator shows correct step number of 7 |

Coverage targets: ViewModel 90%+, Screen 80%+, Repository 85%+.

> Source note: several test scenarios (TC-MCO-008) describe a single companion
> `POST /companion/groups/{groupId}/meetings/{meetingId}/complete` call, whereas `api.yaml` and
> `flow.yaml` define the ordered 6-endpoint Fineract submit sequence above. This spec follows the
> `api.yaml`/`flow.yaml` sequence (endpoint SoT); reconcile the test wording.

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/meeting-conduct/MOCKUP.md`
- **Preview HTML:** `idea-layer/screens/meeting-conduct/preview/`
- **Design conformance:** sticky horizontal `step_stepper` (7 icons: Review/Attendance/Balance/
  Savings/Loans/Apply/Close) with active/completed/inactive states. Persistent `corpus_band`
  (tertiaryContainer) shows corpus + cash on hand on steps 2–6. Step 1 uses per-member
  PRESENT/LATE/ABSENT segmented buttons with an errorContainer fine chip; step 3 uses group +
  individual savings inputs with a running-total band; step 4 shows loan rows with an OVERDUE chip
  and repayment/fine inputs; step 5 shows loan-application cards with For/Against vote buttons and
  a chairperson-only Approve gated on votesFor > votesAgainst; step 6 shows the reconciliation
  card and a full-width Submit. An offline chip + offline submit note surface when `isOffline`.
