# SPEC — corpus-tracking
# MifosSave (mifos-x-group-banking) | Feature FR-018
# Generated: 2026-05-06

---

## Overview

The corpus-tracking feature provides real-time visibility into the Mwangaza Women's Group's shared fund balance (corpus) across the app. The corpus is the total pooled capital available for loan disbursement. FR-018 requires: (1) the corpus balance is displayed on the GroupDashboard, (2) it updates in real-time during meetings (via the CorpusBand in the wizard), and (3) loan disbursement is blocked when the corpus balance is insufficient. The corpus is stored in the dt_group_corpus custom datatable and updated after each meeting via PUT.

**Priority:** must | **Client:** admin | **Version:** 1.0.0

**Corpus formula:**
```
closing_corpus = opening_corpus
              + total_savings_collected
              + total_loan_repayments
              + total_fines_collected
              - total_loans_disbursed
```

---

## Acceptance Criteria

- AC-CT-001: GroupDashboard shows the corpus fund balance (KES 47,500) in a prominently styled card (displaySmall 36sp, primary #2E7D32).
- AC-CT-002: Corpus card shows three sub-stats: Opening Balance (KES 0 at cycle start), Contributions This Cycle (KES 52,500), and Loans Outstanding (KES 5,000).
- AC-CT-003: When corpus balance is below minimumDisbursementThreshold (from dt_group_config), a red warning banner appears on the corpus card: "Loan disbursement is blocked — corpus balance is below minimum threshold."
- AC-CT-004: CorpusBand is visible on wizard steps 2–6 of MeetingConductScreen; it shows live corpus: "Corpus: KES X" and "Cash on Hand: KES Y".
- AC-CT-005: CorpusBand updates in real-time (≤100ms latency) as savings amounts, loan repayments, and loan disbursements are entered in the wizard.
- AC-CT-006: ApproveLoanApplication in step 5 is blocked if the prospective closing corpus would be < 0; error snackbar shown: "Corpus insufficient for this disbursement — available KES X."
- AC-CT-007: On meeting submission, corpus is updated via PUT /fineract-provider/api/v1/datatables/dt_group_corpus/{centerId} with the computed closingCorpus as the new corpusBalance.
- AC-CT-008: Corpus data is cached offline (SQLDelight); if offline, corpus is shown from cache with last-updated meeting number.
- AC-CT-009: GroupDashboard corpus card uses network-first strategy (TTL 60s) to ensure real-time accuracy.
- AC-CT-010: The Start Meeting quick action on GroupDashboard navigates to meeting-calendar even when corpus is insufficient (the block is on loan disbursement, not meeting start).

---

## Screens Table

| Screen ID | Composable | Layout | Description |
|-----------|-----------|--------|-------------|
| group-dashboard | GroupDashboardScreen | Column (TopBar + LazyColumn[GroupHeaderCard + CorpusCard + QuickActions + SavingsSummary + ActivityFeed]) | Central hub; CorpusCard shows fund balance with block banner; activity feed shows recent transactions |
| meeting-conduct (CorpusBand) | CorpusBand (inside MeetingConductScreen) | Row (corpus label + value, cash on hand label + value) | Persistent band on steps 2-6 showing live corpus; updates as inputs change |
| meeting-conduct (step 5 gate) | CorpusGateChip + ApproveLoanApplication | Chip in Step5LoanApplications | Shows available-to-disburse balance; blocks approval when corpus would go negative |

---

## State Model

### GroupDashboardViewModel

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| isLoading | Boolean | true | |
| group | Group? | null | From get_center |
| corpus | GroupCorpus? | null | From dt_group_corpus |
| config | GroupConfig? | null | From dt_group_config |
| accounts | GroupAccounts? | null | From get_center_accounts |
| recentActivity | List\<ActivityItem\> | emptyList() | |
| isCorpusInsufficient | Boolean | false | computed: corpus.currentBalance < config.minimumDisbursementThreshold |
| isCycleEnd | Boolean | false | computed: group.cycleWeek == group.cycleLengthWeeks |
| error | GroupDashboardError? | null | |

**Screen states:** Loading, Content, Error
**Errors:** Network, Server, NotFound, Auth
**Actions:** OnStartMeeting, OnViewMembers, OnViewLoans, OnShareOut, OnRefresh, Retry, OnBack
**Events:** NavigateToMeetingCalendar, NavigateToMemberList, NavigateToLoanList, NavigateToShareOut, ShowCorpusBlockedDialog, ShowSnackbar

**DI:** GroupRepository, CorpusRepository, NetworkMonitor, SessionManager

### CorpusBand — Computed from MeetingConductState

| Computed Field | Formula |
|----------------|---------|
| displayCorpus | openingCorpus + runningSavingsTotal + totalRepayments + totalFinesCollected - totalLoansDisbursed |
| isCorpusWarning | displayCorpus < 0 (only possible if step 5 loan approval bypasses gate) |
| availableForDisbursal | displayCorpus (used for corpus gate chip in step 5) |

---

## Navigation Table

| From | To | Condition | Params |
|------|----|-----------|--------|
| group-list | group-dashboard | user_taps_group | groupId |
| group-dashboard | meeting-calendar | OnStartMeeting | groupId |
| group-dashboard | member-list | OnViewMembers | groupId |
| group-dashboard | loan-list | OnViewLoans | groupId |
| group-dashboard | share-out-preview | OnShareOut (only when isCycleEnd=true) | groupId |

---

## API Endpoints Table

| ID | Method | Path | Description |
|----|--------|------|-------------|
| get_center | GET | /fineract-provider/api/v1/centers/{centerId} | Fetch group center data |
| get_center_accounts | GET | /fineract-provider/api/v1/centers/{centerId}/accounts | Fetch savings and loan accounts |
| get_group_corpus | GET | /fineract-provider/api/v1/datatables/dt_group_corpus/{centerId} | Fetch real-time corpus balance |
| get_group_config | GET | /fineract-provider/api/v1/datatables/dt_group_config/{centerId} | Fetch group config including minimumDisbursementThreshold |
| put_group_corpus | PUT | /fineract-provider/api/v1/datatables/dt_group_corpus/{centerId} | Update corpus balance after meeting |

---

## Design Tokens Used

| Token | Value | Usage |
|-------|-------|-------|
| primary | #2E7D32 | Corpus balance large display number |
| primary_container | #A6F1A6 | Group dashboard header card |
| error | #D32F2F | Corpus insufficient text, border on corpus card |
| error_container | #FFDAD6 | Corpus block banner background |
| on_error_container | #410002 | Corpus block banner text |
| tertiary_container | #D2E4FF | CorpusBand background in wizard |
| on_tertiary_container | #001C39 | CorpusBand text |
| surface_variant | #DEE5DA | Sub-stat backgrounds on corpus card |
| displaySmall | 36sp | Corpus KES balance number |
| min_touch_target | 48dp | All action buttons (Start Meeting, Members, Loans, Share-Out) |
| corner large | 16dp | Corpus card corner radius |
| elevation level_2 | 3dp | Corpus card shadow |
