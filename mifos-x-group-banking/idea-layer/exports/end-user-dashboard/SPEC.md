# End-User Dashboard — Feature Spec

## Overview

The end-user dashboard is the self-service surface for group members. It gives members a personal view of their savings (group-linked and individual), active loan status, share-out projection, and recent transactions. Members can also browse their full loan history and submit new loan requests — even when offline.

**Acceptance Criteria**
- FR-016: End user can submit loan request from personal dashboard; appears as pending in next admin meeting
- FR-017: Dual savings — mandatory group savings (meeting-collected) and voluntary individual savings (anytime)
- FR-014: End user client type has a distinct UI surface separate from the admin path
- FR-008: Full offline support — SQLDelight cache serves data when network unavailable; loan requests queued via SyncQueue when offline
- Dashboard loads with shimmer skeleton while fetching; pull-to-refresh available
- Savings screen shows two tabs: Group-linked and Individual (individual tab hidden when no account)
- Loans screen shows all loans with expandable repayment schedule; filter by All/Active/Closed
- Loan request form validates amount against savings × loan_multiplier (default 3.0×); inline error shown
- Offline badge shown when serving cached data
- Analytics events fired: `savings_card_tapped`, `loan_card_tapped`, `request_loan_cta_tapped`, `loan_expanded`, `filter_changed`, `loan_request_submitted`, `loan_request_success`

## Screens

| Screen | Composable | Layout | Description |
|--------|-----------|--------|-------------|
| Personal Dashboard | `PersonalDashboardScreen` | Scaffold (top-bar + bottom-nav + LazyColumn) | Home screen — savings card, loan card/CTA, share-out projection, recent activity |
| Personal Savings | `PersonalSavingsScreen` | Scaffold (top-bar + TabRow + LazyColumn per tab) | Dual savings detail — group-linked and individual tabs |
| Personal Loans | `PersonalLoansScreen` | Scaffold (top-bar + LazyColumn + FAB) | Full loan list with status filter and expandable repayment schedule |
| Loan Request | `LoanRequestScreen` | Scaffold (top-bar + Column scrollable + bottom submit bar) | Loan application form with offline queue support |

## State Model

### PersonalDashboardViewModel

**State fields**:

| Name | Type | Default |
|------|------|---------|
| clientId | Long | 0L |
| memberName | String | "" |
| groupName | String | "Mwangaza Women's Group" |
| groupLinkedSavingsBalance | Double | 0.0 |
| individualSavingsBalance | Double | 0.0 |
| activeLoan | LoanSummary? | null |
| shareOutProjection | Double | 0.0 |
| recentTransactions | List\<SavingsTransactionDto\> | emptyList() |
| isRefreshing | Boolean | false |
| isLoading | Boolean | true |
| error | DashboardError? | null |

**Actions**:
- `OnRefresh` — pull-to-refresh; re-fetches all data
- `OnRetry` — tap Retry button in error state
- `OnSavingsCardClick` — navigates to personal-savings
- `OnLoanCardClick` — navigates to personal-loans
- `OnRequestLoanClick` — navigates to loan-request

**Events**: NavigateToSavings, NavigateToLoans, NavigateToLoanRequest

**DI**: SelfServiceRepository, SavingsRepository, LoanRepository, SessionManager

---

### PersonalSavingsViewModel

**State fields**:

| Name | Type | Default |
|------|------|---------|
| clientId | Long | 0L |
| groupLinkedSavingsId | Long | 0L |
| individualSavingsId | Long? | null |
| selectedTab | SavingsTab | SavingsTab.GROUP_LINKED |
| groupLinkedBalance | Double | 0.0 |
| individualBalance | Double | 0.0 |
| groupLinkedTransactions | List\<SavingsTransactionDto\> | emptyList() |
| individualTransactions | List\<SavingsTransactionDto\> | emptyList() |
| contributionTarget | Double | 500.0 |
| meetingsAttended | Int | 0 |
| totalMeetings | Int | 0 |
| isLoading | Boolean | true |
| isRefreshing | Boolean | false |
| error | SavingsError? | null |

**Actions**:
- `OnTabSelected(tab: SavingsTab)` — switches between GROUP_LINKED and INDIVIDUAL views
- `OnRefresh` — pull-to-refresh
- `OnRetry` — tap Retry in error state

**Events**: NavigateBack

**DI**: SavingsRepository, SessionManager

---

### PersonalLoansViewModel

**State fields**:

| Name | Type | Default |
|------|------|---------|
| clientId | Long | 0L |
| loans | List\<LoanDto\> | emptyList() |
| selectedLoanId | Long? | null |
| filterStatus | LoanStatusFilter | LoanStatusFilter.ALL |
| isLoading | Boolean | true |
| isRefreshing | Boolean | false |
| error | LoanError? | null |

**Actions**:
- `OnRefresh` — pull-to-refresh
- `OnRetry` — tap Retry in error state
- `OnLoanExpand(loanId: Long)` — expands/collapses repayment schedule on a loan card
- `OnFilterChange(status: LoanStatusFilter)` — updates filter chip selection
- `OnRequestLoanClick` — navigates to loan-request

**Events**: NavigateToLoanRequest, NavigateBack

**DI**: LoanRepository, SessionManager

---

### LoanRequestViewModel

**State fields**:

| Name | Type | Default |
|------|------|---------|
| clientId | Long | 0L |
| savingsBalance | Double | 0.0 |
| loanMultiplier | Double | 3.0 |
| maxLoanAmount | Double | 0.0 |
| requestedAmount | String | "" |
| requestedAmountError | String? | null |
| purpose | LoanPurpose? | null |
| purposeError | String? | null |
| durationWeeks | Int | 12 |
| repaymentEstimate | Double | 0.0 |
| isOfflineMode | Boolean | false |
| isSubmitting | Boolean | false |
| isFormValid | Boolean | false |
| submitError | SubmitError? | null |
| successDialogVisible | Boolean | false |

**Actions**:
- `OnAmountChange(value: String)` — validates against maxLoanAmount; recalculates repaymentEstimate
- `OnPurposeSelected(purpose: LoanPurpose)` — clears purposeError
- `OnDurationChanged(weeks: Int)` — recalculates repaymentEstimate
- `OnSubmitClick` — submits via API or SyncQueue based on connectivity
- `OnSuccessDialogDismiss` — navigates to dashboard
- `OnRetry` — re-attempts submission

**Events**: NavigateToDashboardAfterSuccess, NavigateBack, ShowOfflineQueuedConfirmation

**DI**: LoanRequestRepository, SyncQueueRepository, SessionManager, ConnectivityManager

## Navigation

| From | To | Condition | Params |
|------|----|-----------|--------|
| login | personal-dashboard | end_user_login_success | clientId: Long, selfServiceToken: String |
| personal-dashboard | personal-savings | user_taps_savings_card | clientId, groupLinkedSavingsId, individualSavingsId? |
| personal-dashboard | personal-loans | user_taps_loan_card | clientId |
| personal-dashboard | loan-request | user_taps_request_loan_cta | clientId, savingsBalance, loanMultiplier |
| personal-savings | personal-dashboard | user_taps_back | — |
| personal-loans | loan-request | user_taps_fab | clientId, savingsBalance, loanMultiplier |
| personal-loans | personal-dashboard | user_taps_back | — |
| loan-request | personal-dashboard | submission_success | — |
| loan-request | personal-loans | user_taps_back | — |

## API Endpoints

| ID | Method | Path | Auth | Cache |
|----|--------|------|------|-------|
| get_client_accounts | GET | /self/clients/{clientId}/accounts | selfServiceToken | 300s stale-while-revalidate |
| get_savings_account | GET | /self/savingsaccounts/{savingsId} | selfServiceToken | 300s stale-while-revalidate |
| get_group_linked_transactions | GET | /self/savingsaccounts/{savingsId}/transactions | selfServiceToken | 300s stale-while-revalidate |
| get_individual_transactions | GET | /self/savingsaccounts/{savingsId}/transactions | selfServiceToken | 300s stale-while-revalidate |
| get_self_loans | GET | /self/loans | selfServiceToken | 180s stale-while-revalidate |
| submit_loan_request | POST | /datatables/dt_loan_request | selfServiceToken | no-cache; offline: SyncQueue |

## Design Tokens Used

- `primary` (#2E7D32) — top bar background, savings icons, progress bars, tab selection
- `onPrimary` (#FFFFFF) — top bar text, balance hero text
- `primaryContainer` (#A6F1A6) — group banner, savings tab unselected fill, currency chip
- `secondary` (#FF8F00) — FAB background, individual savings accent
- `onSecondary` (#FFFFFF) — FAB icon
- `secondaryContainer` (#FFDDB3) — share-out card background, offline banner, individual promo
- `tertiary` (#1565C0) — loan card icon tint, repayment estimate colour
- `tertiaryContainer` (#D2E4FF) — request-loan CTA card, savings limit card
- `onTertiaryContainer` (#001C39) — text on tertiaryContainer
- `error` (#D32F2F) — overdue indicators, withdrawal amounts
- `errorContainer` (#FFDAD6) — error banners
- `surface` (#FAFAFA) — card backgrounds
- `surfaceVariant` (#DEE5DA) — transaction icon containers, repayment summary card
- `onSurfaceVariant` (#424942) — section labels, secondary text
- `outline` (#727971) — dividers, date text
- Shape tokens: lg (16dp) for main cards, md (12dp) for duration card, full (9999dp) for filter chips and buttons
- Elevation level_2 (3dp) for main cards, level_5 (12dp) for FAB
