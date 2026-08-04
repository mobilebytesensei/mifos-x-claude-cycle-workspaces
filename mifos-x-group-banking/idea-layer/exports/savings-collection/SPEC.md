# SPEC — savings-collection
# MifosSave (mifos-x-group-banking) | Feature FR-004 / FR-017
# Generated: 2026-05-06

---

## Overview

The savings-collection feature enables the Mwangaza Women's Group admin (treasurer/chairperson) to collect and track savings contributions from all group members. It implements FR-004 (savings collection during meetings) and FR-017 (dual savings: mandatory group-linked savings + optional individual savings). The feature surfaces on two screens: the SavingsDashboard for group-wide visibility, and within Step 3 of the MeetingConductScreen wizard for real-time collection during meetings. Savings are stored as Fineract savings account transactions and cached offline-first via SQLDelight.

**Priority:** must | **Client:** admin | **Version:** 1.0.0

---

## Acceptance Criteria

- AC-SC-001: Admin can view a SavingsDashboard with two tabs: Group Savings (mandatory) and Individual Savings (voluntary).
- AC-SC-002: Group Savings tab shows a bar chart of weekly contributions (last 6 weeks, primary green bars), cycle progress card (KES collected vs target), and per-member contribution rows.
- AC-SC-003: Individual Savings tab shows an amber line chart of weekly net deposits, total balance card, and per-member current balance rows.
- AC-SC-004: Per-member rows in both tabs are tappable → navigates to member-savings-detail with correct memberId and savingsType params.
- AC-SC-005: Last-sync timestamp band appears below TopAppBar when data is from cache; hidden when data is fresh.
- AC-SC-006: Pull-to-refresh works when online; shows "Cannot refresh — you're offline" snackbar when offline.
- AC-SC-007: During meeting-conduct wizard step 3, all 5 group members (Amina Hassan, Peter Otieno, Grace Wanjiku, John Mwangi, Mary Akinyi) have group savings and individual savings input fields.
- AC-SC-008: Group savings input requires minimum KES 200 per member (FR-020); field shows error "Below minimum KES 200 required" for amounts below this threshold; amounts above KES 10,000 are rejected.
- AC-SC-009: Individual savings input is optional (no minimum); keyboard is numeric for both inputs.
- AC-SC-010: Running total banner on step 3 updates in real-time (≤100ms) as amounts are entered.
- AC-SC-011: On meeting submission, savings transactions are posted to Fineract as POST /savingsaccounts/{savingsId}/transactions (one call per member per savings type with transactionAmount > 0).
- AC-SC-012: Meeting summary screen shows group savings and individual savings as separate metric cards with correct KES values.

---

## Screens Table

| Screen ID | Composable | Layout | Description |
|-----------|-----------|--------|-------------|
| savings-dashboard | SavingsDashboardScreen | Column (TopAppBar + SyncBand + TabRow + TabContent[Chart + CycleProgress / TotalCard + MemberList]) | Two-tab savings overview with charts, cycle progress, per-member rows |
| meeting-conduct (step 3) | Step3SavingsCollection (inside MeetingConductScreen) | Column (Header + MinContribChip + LazyColumn[SavingsMemberRow] + RunningTotalBand) | In-wizard savings collection form |

---

## State Model

### SavingsDashboardViewModel

| Field | Type | Default |
|-------|------|---------|
| selectedTab | SavingsTab | SavingsTab.GROUP |
| groupSavingsSummary | GroupSavingsSummary? | null |
| individualSavingsSummary | IndividualSavingsSummary? | null |
| weeklyTrend | List\<WeeklyContributionPoint\> | emptyList() |
| isLoading | Boolean | true |
| isRefreshing | Boolean | false |
| error | String? | null |
| lastSyncAt | String? | null |
| centerId | Int | 0 |
| cycleTarget | Long | 0L |
| cycleCollected | Long | 0L |

**Screen states:** Loading, Content (GROUP tab), Content (INDIVIDUAL tab), Empty, Error
**Actions:** LoadDashboard, RefreshDashboard, SelectTab, OpenMemberDetail
**Events:** NavigateToMemberDetail, ShowError
**DI:** SavingsRepository, NavigationManager, ConnectivityObserver, LocalSavingsDao (SQLDelight)

### Step3SavingsCollection (within MeetingConductViewModel)

Relevant fields from MeetingConductState:

| Field | Type | Notes |
|-------|------|-------|
| savingsMap | Map\<String, SavingsEntry\> | keyed by memberId; each entry has groupAmount + individualAmount |
| runningSavingsTotal | Long | sum of all group + individual amounts |
| groupMembers | List\<GroupMember\> | loaded in screen init |
| stepValidationError | String? | set when any member groupAmount < 200 on NextStep |

**Actions (step 3 specific):**
- SetSavingsAmount(memberId, amount, type: SavingsType) — triggered on each input change
- NextStep — triggers validation (all groupAmounts >= 200)

---

## Navigation Table

| From | To | Condition | Params |
|------|----|-----------|--------|
| home-dashboard | savings-dashboard | user_taps_savings_nav | centerId |
| bottom_nav | savings-dashboard | savings_tab_selected | centerId |
| savings-dashboard (GROUP row) | member-savings-detail | user_taps_member_row | memberId, savingsType=GROUP_LINKED |
| savings-dashboard (INDIVIDUAL row) | member-savings-detail | user_taps_member_row | memberId, savingsType=INDIVIDUAL |
| meeting-conduct step 3 | (no navigation — in-wizard) | input changes only | — |

---

## API Endpoints Table

| ID | Method | Path | Description |
|----|--------|------|-------------|
| get_group_savings_transactions | GET | /fineract-provider/api/v1/savingsaccounts/{groupSavingsId}/transactions?limit=50 | Mandatory savings history |
| get_client_savings_accounts | GET | /fineract-provider/api/v1/clients/{clientId}/accounts | Individual savings account per member |
| get_individual_savings_transactions | GET | /fineract-provider/api/v1/savingsaccounts/{individualSavingsId}/transactions?limit=20 | Individual savings transactions per member |
| post_savings_transaction | POST | /fineract-provider/api/v1/savingsaccounts/{savingsId}/transactions | Post deposit (one per member per type on submit) |

---

## Design Tokens Used

| Token | Value | Usage |
|-------|-------|-------|
| primary | #2E7D32 | Group savings bar chart bars, cycle progress bar, KES amounts |
| primary_container | #A6F1A6 | Cycle progress card, group total chip, running total band |
| secondary | #FF8F00 | Individual savings line chart color |
| secondary_container | #FFDDB3 | Member avatar backgrounds, individual total card |
| tertiary_container | #D2E4FF | Individual savings balance trailing text (via tertiary) |
| surface_variant | #DEE5DA | Tab row divider, last-sync band background |
| on_surface_variant | #424942 | Section headers, sub-labels |
| error | #D32F2F | TextField error outline and error text |
| Noto Sans | font | All text |
| min_touch_target | 48dp | All inputs and tappable rows |
