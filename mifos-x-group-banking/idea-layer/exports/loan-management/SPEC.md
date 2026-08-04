# Loan Management — Feature Specification
**Project**: MifosSave (mifos-x-group-banking)
**Feature ID**: loan-management
**Requirements**: FR-005, FR-006
**Version**: 1.0.0
**Status**: enriched

---

## Overview

The Loan Management feature enables chairpersons and treasurers to apply for loans on behalf of group members, track repayment schedules, detect overdue loans, and record payments. Eligibility is computed client-side using the savings-multiplier rule (savings balance × loan_multiplier from dt_group_config). All screens are offline-first via SQLDelight cache with stale-while-revalidate sync from Fineract.

---

## Acceptance Criteria

- **FR-005**: A chairperson or treasurer can submit a loan application for any group member. The requested amount must not exceed `memberSavingsBalance × loanMultiplier`. A corpus balance check warns if disbursement would reduce the group fund below 10%.
- **FR-006**: Active loans show a weekly repayment schedule. Overdue loans are flagged with a red indicator and overdue amount. The treasurer can record repayments. The chairperson can mark a loan as defaulted. Repayment history is viewable in a tab.

---

## Screens Table

| Screen ID     | Route                          | Type    | Role Required       |
|---------------|-------------------------------|---------|---------------------|
| loan-list     | /groups/{groupId}/loans        | list    | Any authenticated   |
| loan-apply    | /groups/{groupId}/loans/apply  | form    | Chairperson/Treasurer |
| loan-detail   | /loans/{loanId}                | detail  | Any authenticated   |
| meeting-conduct (step 4, 5) | /meetings/{meetingId}/conduct | wizard | Chairperson/Treasurer |

---

## State Model

### LoanListViewModel
| Field | Type | Default |
|-------|------|---------|
| isLoading | Boolean | true |
| loans | List<LoanSummary> | emptyList() |
| selectedFilter | LoanStatusFilter | ALL |
| filteredLoans | List<LoanSummary> | emptyList() |
| isRefreshing | Boolean | false |
| error | LoanListError? | null |
| groupId | Long | 0L |
| canApplyLoan | Boolean | false |

**Actions**: OnLoanClick(loanId), OnFilterChange(filter), OnApplyLoan, OnRefresh, Retry, OnLoadNextPage
**Events**: NavigateToLoanDetail(loanId), NavigateToLoanApply(groupId), ShowSnackbar(message)
**DI**: LoanRepository, NetworkMonitor, SessionManager

### LoanApplyViewModel
| Field | Type | Default |
|-------|------|---------|
| selectedMember | GroupMember? | null |
| requestedAmount | String | "" |
| durationWeeks | Int | 12 |
| purpose | LoanPurpose | BUSINESS |
| selectedProduct | LoanProduct? | null |
| memberSavingsBalance | Double | 0.0 |
| loanMultiplier | Double | 3.0 |
| eligibleAmount | Double | 0.0 |
| corpusBalance | Double | 0.0 |
| corpusWarning | Boolean | false |
| isSubmitting | Boolean | false |
| amountError | String? | null |

**Actions**: OnMemberSelected, OnAmountChanged, OnDurationChanged, OnPurposeChanged, OnProductSelected, OnSubmit, OnBack
**DI**: LoanRepository, MemberRepository, GroupRepository, NetworkMonitor, SessionManager

### LoanDetailViewModel
| Field | Type | Default |
|-------|------|---------|
| isLoading | Boolean | true |
| loan | LoanDetail? | null |
| repaymentSchedule | List<RepaymentScheduleRow> | emptyList() |
| repaymentHistory | List<RepaymentTransaction> | emptyList() |
| selectedTab | LoanDetailTab | SCHEDULE |
| canRecordRepayment | Boolean | false |
| canMarkDefaulted | Boolean | false |

**Actions**: OnTabChange, OnRecordRepayment, OnMarkDefaulted, OnBack, Retry, OnRefresh
**DI**: LoanRepository, NetworkMonitor, SessionManager

---

## Navigation Table

| From | Action | To | Params |
|------|--------|----|--------|
| group-dashboard | Tap Loans button | loan-list | groupId |
| loan-list | Tap loan card | loan-detail | loanId |
| loan-list | Tap FAB (Apply) | loan-apply | groupId |
| loan-apply | Submit success | meeting-conduct | loanId |
| loan-detail | Tap back | loan-list | — |

---

## API Endpoints Table

| ID | Method | Path | Description |
|----|--------|------|-------------|
| get_group_loans | GET | /groups/{groupId}/loans | Paginated loan list for group |
| get_loan_template | GET | /loans/template | Pre-fill defaults for selected client+product |
| get_loan_products | GET | /loanproducts | Available loan products |
| get_member_savings | GET | /clients/{clientId}/accounts | Member savings balance for eligibility |
| get_group_corpus | GET | /datatables/dt_group_corpus/{groupId} | Corpus balance for disbursement check |
| get_group_config | GET | /datatables/dt_group_config/{groupId} | Loan multiplier and policy |
| post_loan | POST | /loans | Submit loan application to Fineract |
| get_loan_detail | GET | /loans/{loanId} | Full detail with schedule and history |
| post_repayment | POST | /loans/{loanId}/transactions?command=repayment | Record repayment |
| get_loan_votes | GET | /datatables/dt_loan_vote/{loanId} | Fetch vote tally for loan |
| post_loan_vote | POST | /datatables/dt_loan_vote | Record member vote on loan |

---

## Design Tokens Used

| Token | Value | Usage |
|-------|-------|-------|
| primary | #2E7D32 | TopBar, FAB, Submit button, active status badge |
| error | #D32F2F | Overdue indicator, Mark Defaulted button |
| primaryContainer | #A6F1A6 | Eligibility banner, active status badge bg |
| errorContainer | #FFDAD6 | Overdue status badge bg, corpus warning banner |
| warningContainer | #FFF9C4 | Corpus warning banner |
| surface | #FAFAFA | Card backgrounds |
| onSurfaceVariant | #424942 | Secondary text, outstanding labels |
| shape.medium | 12dp | Card corner radius |
| elevation.level_2 | 3dp | Loan cards |
| typography.titleMedium | 16sp/500 | Loan card member name |
| typography.bodySmall | 12sp/400 | Outstanding balance, next repayment date |
| min_touch_target | 48dp | All interactive elements |
