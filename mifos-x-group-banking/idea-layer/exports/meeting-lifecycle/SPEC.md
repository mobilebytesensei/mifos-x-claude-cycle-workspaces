# SPEC — meeting-lifecycle
# MifosSave (mifos-x-group-banking) | Feature FR-003 / FR-019
# Generated: 2026-05-06

---

## Overview

The meeting-lifecycle feature provides the complete end-to-end flow for conducting weekly VSLA group meetings for the Mwangaza Women's Group. It covers scheduling and listing meetings, conducting a 7-step wizard meeting (attendance, savings, loans, reconciliation), reviewing the previous meeting before beginning a new one, and reviewing a post-meeting summary. The feature is offline-first: all wizard state is persisted to SQLDelight and submitted via SyncQueue when offline. It addresses FR-003 (meeting conduct) and FR-019 (enhanced previous-meeting review before each new meeting).

**Priority:** must | **Client:** admin (treasurer, chairperson) | **Version:** 1.0.0

---

## Acceptance Criteria

- AC-ML-001: Admin can view a list of all scheduled and past meetings for the group in chronological order.
- AC-ML-002: Upcoming meeting card is pinned at top with "Start Meeting" CTA when an upcoming meeting exists.
- AC-ML-003: Tapping "Start Meeting" navigates to the 7-step meeting conduct wizard with correct meetingId, meetingNumber, groupId params.
- AC-ML-004: Wizard step 0 displays the previous meeting summary (Meeting #3: KES 1,850 collected, corpus KES 12,400, 5/5 attendance); first meeting shows empty state.
- AC-ML-005: Wizard step 1 requires attendance recorded for all 5 group members (Amina Hassan, Peter Otieno, Grace Wanjiku, John Mwangi, Mary Akinyi) before advancing; LATE = KES 50 fine, ABSENT = KES 100 fine (FR-012).
- AC-ML-006: Wizard step 2 confirms opening corpus (KES 12,400) and cash on hand (KES 2,000) from dt_group_corpus.
- AC-ML-007: Wizard step 3 validates minimum KES 200 group savings per member (FR-020); blocks advance if any member is below minimum; max KES 10,000 per member.
- AC-ML-008: Wizard step 4 accepts loan repayments; validates repayment does not exceed outstanding balance.
- AC-ML-009: Wizard step 5 enables group voting (For/Against) and chairperson-only approval of loan applications; corpus gate blocks approval if disbursement would make closing corpus negative.
- AC-ML-010: Wizard step 6 computes closing corpus = opening + savings + repayments + fines - disbursements; Submit button triggers all 6 sequential API calls.
- AC-ML-011: When offline, all 6 payload groups are enqueued to SyncQueueRepository and optimistic success is shown.
- AC-ML-012: Meeting summary screen displays total KES collected, attendance, group/individual savings breakdown, corpus reconciliation.
- AC-ML-013: Previous meeting review screen shows unresolved items (unpaid fines, pending loan votes) when they exist.
- AC-ML-014: Tapping a completed meeting on the calendar navigates to previous-meeting-review with launchedFrom=calendar; tapping from step 0 sets launchedFrom=conduct.

---

## Screens Table

| Screen ID | Composable | Layout | Description |
|-----------|-----------|--------|-------------|
| meeting-calendar | MeetingCalendarScreen | Column (TopAppBar + ViewToggle + PinnedUpcoming + LazyColumn) | List/calendar toggle view of all meetings; upcoming card pinned at top; tapping past meetings navigates to review |
| meeting-conduct | MeetingConductScreen | Column (TopAppBar + StepperHeader + CorpusBand + StepContent + NavigationFooter) | 7-step wizard for conducting a meeting; corpus band visible on steps 2-6; sticky navigation footer |
| meeting-summary | MeetingSummaryScreen | Column (TopAppBar + LazyColumn[HeroCard + MetricGrid + SavingsBreakdown + CorpusReconciliation + DoneBtn]) | Read-only post-meeting summary with hero card, 2x3 metric grid, per-member savings breakdown |
| previous-meeting-review | PreviousMeetingReviewScreen | Column (TopAppBar + ContextBanner + LazyColumn[MetricsSummary + AttendanceDetail + SavingsDetail + LoanStatus + UnresolvedAlert]) | Read-only previous meeting detail; context-aware banner; optional Start Meeting CTA |

---

## State Model

### MeetingCalendarViewModel

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| meetings | List\<MeetingListItem\> | emptyList() | Loaded from API / cache |
| isLoading | Boolean | true | Skeleton shown while true |
| isRefreshing | Boolean | false | Pull-to-refresh in progress |
| viewMode | ViewMode | ViewMode.LIST | LIST or CALENDAR |
| error | String? | null | Inline error message |
| groupId | Int | 0 | Navigation param |

**Actions:** LoadMeetings, RefreshMeetings, ToggleViewMode, StartMeeting, OpenPastMeeting
**Events:** NavigateToConduct, NavigateToReview, ShowError

### MeetingConductViewModel

| Field | Type | Default |
|-------|------|---------|
| currentStep | Int | 0 |
| totalSteps | Int | 7 |
| meetingId | String | "" |
| meetingNumber | Int | 0 |
| groupId | Int | 0 |
| previousMeetingSummary | PreviousMeetingSummary? | null |
| groupMembers | List\<GroupMember\> | emptyList() |
| attendanceMap | Map\<String, AttendanceStatus\> | emptyMap() |
| lateFines | Map\<String, Long\> | emptyMap() |
| absentFines | Map\<String, Long\> | emptyMap() |
| openingCorpus | Long | 0L |
| cashOnHand | Long | 0L |
| savingsMap | Map\<String, SavingsEntry\> | emptyMap() |
| runningSavingsTotal | Long | 0L |
| activeLoans | List\<LoanSummary\> | emptyList() |
| loanRepayments | Map\<String, Long\> | emptyMap() |
| loanFines | Map\<String, Long\> | emptyMap() |
| pendingLoanApplications | List\<LoanApplication\> | emptyList() |
| loanVotes | Map\<String, LoanVote\> | emptyMap() |
| closingCorpus | Long | 0L |
| totalCashCollected | Long | 0L |
| totalLoansDisbursed | Long | 0L |
| totalRepayments | Long | 0L |
| totalFinesCollected | Long | 0L |
| isSubmitting | Boolean | false |
| isOffline | Boolean | false |
| submitError | String? | null |
| stepValidationError | String? | null |
| isSavingProgress | Boolean | false |

**Actions:** LoadMeetingData, NextStep, PreviousStep, SetAttendance, SetSavingsAmount, SetLoanRepayment, SetLoanFine, CastLoanVote, ApproveLoanApplication, SubmitMeeting, ViewFullPreviousMeeting, SaveProgressLocally, DismissError
**Events:** NavigateToMeetingSummary, NavigateToPreviousMeetingReview, NavigateBack, ShowStepError, ShowSubmitSuccess, ShowSubmitError

**DI:** MeetingRepository, SavingsRepository, LoanRepository, CorpusRepository, SyncQueueRepository, NavigationManager, ConnectivityObserver, LocalMeetingDao, SyncQueueDao

---

## Navigation Table

| From | To | Condition | Params |
|------|----|-----------|--------|
| meeting-calendar | meeting-conduct | user_taps_start_meeting | meetingId, meetingNumber, groupId |
| meeting-calendar | previous-meeting-review | user_taps_completed_meeting | meetingId, meetingNumber, groupId |
| meeting-conduct | meeting-summary | wizard_submitted_successfully | meetingId, meetingNumber, groupId |
| meeting-conduct | previous-meeting-review | user_taps_view_full_previous | meetingId, groupId |
| meeting-conduct | meeting-calendar | user_taps_back_or_cancel | — |
| previous-meeting-review | meeting-conduct | user_taps_start_meeting (launchedFrom=conduct) | meetingId, meetingNumber, groupId |
| previous-meeting-review | meeting-calendar | user_taps_back (launchedFrom=calendar) | — |
| meeting-summary | meeting-calendar | user_taps_done_or_back | — |

---

## API Endpoints Table

| ID | Method | Path | Description |
|----|--------|------|-------------|
| get_group_meetings | GET | /fineract-provider/api/v1/groups/{groupId}/meetings | Fetch scheduled meetings for calendar |
| get_meeting_records_datatable | GET | /fineract-provider/api/v1/datatables/dt_meeting_record/{groupId} | Fetch completed meeting records |
| get_previous_meeting_record | GET | /fineract-provider/api/v1/datatables/dt_meeting_record/{groupId}?meetingNumber={n-1} | Step 0 previous meeting data |
| get_group_members | GET | /fineract-provider/api/v1/groups/{groupId} | Group members for attendance/savings |
| get_group_corpus | GET | /fineract-provider/api/v1/datatables/dt_group_corpus/{groupId} | Opening corpus and cash on hand |
| get_active_loans | GET | /fineract-provider/api/v1/loans?groupId=X&loanStatus=active | Active loans for step 4 |
| get_loan_votes | GET | /fineract-provider/api/v1/datatables/dt_loan_vote/{loanId} | Existing vote tallies for step 5 |
| post_meeting_record | POST | /fineract-provider/api/v1/datatables/dt_meeting_record | Create meeting record on submit |
| post_meeting_attendance | POST | /fineract-provider/api/v1/datatables/dt_meeting_attendance | Per-member attendance on submit |
| post_savings_transaction | POST | /fineract-provider/api/v1/savingsaccounts/{savingsId}/transactions | Savings deposit per member |
| post_loan_repayment | POST | /fineract-provider/api/v1/loans/{loanId}/transactions?command=repayment | Loan repayment on submit |
| post_loan_disbursal | POST | /fineract-provider/api/v1/loans/{loanId}/transactions?command=disburse | Loan disbursement on submit |
| patch_corpus | PUT | /fineract-provider/api/v1/datatables/dt_group_corpus/{groupId} | Update corpus to closingCorpus |

---

## Design Tokens Used

| Token | Value | Usage |
|-------|-------|-------|
| primary | #2E7D32 | Start Meeting button, progress indicators, KES amounts |
| on_primary | #FFFFFF | Text on primary buttons |
| primary_container | #A6F1A6 | Upcoming meeting card background, attendance chips |
| on_primary_container | #002106 | Text on primary container |
| secondary | #FF8F00 | Individual savings trailing amounts |
| secondary_container | #FFDDB3 | Member avatar backgrounds in savings step |
| tertiary | #1565C0 | Corpus band background |
| tertiary_container | #D2E4FF | Corpus band fill |
| error | #D32F2F | Corpus insufficient text, ABSENT attendance chip |
| error_container | #FFDAD6 | Error banner, overdue loan chip, fine chips |
| warning_container | warningContainer | Late fine chips, unresolved items alert |
| surface_variant | #DEE5DA | Previous meeting summary card, reconciliation background |
| Noto Sans | font | All text; bold weight for large KES amounts |
| min_touch_target | 48dp | All interactive elements |
| corner_radius lg | 16dp | Upcoming meeting card, corpus card |
| elevation level_4 | 8dp | Wizard navigation footer |
