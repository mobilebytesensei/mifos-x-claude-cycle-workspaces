# Group-Linked Savings — Feature Specification
**Project**: CommonPurse (mifos-x-group-banking)
**Feature ID**: group-linked-savings
**Requirements**: FR-017
**Version**: 1.0.0
**Status**: enriched

---

## Overview

Group-linked savings implements the dual savings model for VSLA groups: mandatory group savings collected at every meeting, and voluntary individual savings deposited anytime. The savings dashboard provides a treasurer/chairperson overview with two tabs — Group Savings (bar chart of weekly contributions, cycle progress indicator, per-member contribution totals) and Individual Savings (line chart, total balance card, per-member balances with deposit/withdrawal chips). Data is offline-first: cached balances are displayed with a last-sync timestamp, and a background fetch refreshes when connectivity is available.

---

## Acceptance Criteria

- **FR-017**: The app supports two distinct savings types per group:
  1. **Group-linked (mandatory)**: Each member contributes a fixed minimum amount (KES 200) at every group meeting. These are collected via the meeting wizard (step 3 savings collection) and posted to the group's mandatory savings account.
  2. **Individual (voluntary)**: Each member may deposit or withdraw any amount at any time via their personal savings account linked to the group.
  The savings dashboard shows both types in separate tabs with weekly trend charts. Cycle progress tracks total mandatory savings collected vs cycle target. Individual tab shows live balances per member. Tapping a member row navigates to member-savings-detail.

---

## Screens Table

| Screen ID | Route | Type | Role Required |
|-----------|-------|------|---------------|
| savings-dashboard | /savings | dashboard | Treasurer, Chairperson |

---

## State Model

### SavingsDashboardViewModel
| Field | Type | Default |
|-------|------|---------|
| selectedTab | SavingsTab | SavingsTab.GROUP |
| groupSavingsSummary | GroupSavingsSummary? | null |
| individualSavingsSummary | IndividualSavingsSummary? | null |
| weeklyTrend | List<WeeklyContributionPoint> | emptyList() |
| isLoading | Boolean | true |
| isRefreshing | Boolean | false |
| error | String? | null |
| lastSyncAt | String? | null |
| centerId | Int | 0 |
| cycleTarget | Long | 0L |
| cycleCollected | Long | 0L |

**Screen states**: Loading, Content (Group tab), Content (Individual tab), ContentWithError, Empty, Error

**Actions**: LoadDashboard, RefreshDashboard, SelectTab(tab: SavingsTab), OpenMemberDetail(memberId, savingsType)

**Events**: NavigateToMemberDetail(memberId, savingsType), ShowError(message)

**DI**: SavingsRepository, NavigationManager, ConnectivityObserver, LocalSavingsDao (SQLDelight)

---

## Navigation Table

| From | Action | To | Params |
|------|--------|----|--------|
| home-dashboard | Tap Savings nav | savings-dashboard | centerId |
| bottom_nav | Savings tab selected | savings-dashboard | centerId |
| savings-dashboard | Tap member row (GROUP tab) | member-savings-detail | memberId, savingsType=GROUP_LINKED |
| savings-dashboard | Tap member row (INDIVIDUAL tab) | member-savings-detail | memberId, savingsType=INDIVIDUAL |

---

## API Endpoints Table

| Method | Path | Description |
|--------|------|-------------|
| GET | /savingsaccounts/{groupSavingsId}/transactions | Group (mandatory) savings transactions — compute per-member contributions |
| GET | /clients/{clientId}/accounts | Individual savings accounts per member |
| GET | /savingsaccounts/{individualSavingsId}/transactions | Individual savings transactions per member |

---

## Shared Entities

### SavingsTab (enum)
| Value | Tab Label | Chart Type |
|-------|-----------|-----------|
| GROUP | Group Savings | Bar chart (primary green) |
| INDIVIDUAL | Individual | Line chart (secondary amber) |

### GroupSavingsSummary
| Field | Type | Description |
|-------|------|-------------|
| totalCollected | Long | Total KES collected across all meetings in current cycle |
| cycleTarget | Long | Target KES for full cycle (= members × min × meetings) |
| cycleProgress | Float | totalCollected / cycleTarget (0.0–1.0) |
| memberRows | List<MemberGroupSavingsRow> | Per-member contribution breakdown |

### IndividualSavingsSummary
| Field | Type | Description |
|-------|------|-------------|
| totalBalance | Long | Sum of all member individual savings account balances |
| memberRows | List<MemberIndividualSavingsRow> | Per-member balance + last transaction |

### MemberGroupSavingsRow
| Field | Type | Description |
|-------|------|-------------|
| memberId | String | Fineract client ID |
| name | String | Full display name |
| totalContributed | Long | Total KES contributed this cycle |
| lastContribution | Long | Amount contributed in most recent meeting |
| meetingsContributed | Int | Count of meetings where member contributed |

### MemberIndividualSavingsRow
| Field | Type | Description |
|-------|------|-------------|
| memberId | String | Fineract client ID |
| name | String | Full display name |
| currentBalance | Long | Current balance in individual savings account |
| lastTransaction | Long? | Amount of last transaction (positive = deposit, negative = withdrawal) |
| lastTransactionDate | String? | Formatted date of last transaction |

### WeeklyContributionPoint
| Field | Type | Description |
|-------|------|-------------|
| weekLabel | String | "W48", "W49", ... "W3" (ISO week labels) |
| groupAmount | Long | Total mandatory savings collected that week |
| individualAmount | Long | Net individual savings deposits that week |

---

## Design Tokens Used

| Token | Value | Usage |
|-------|-------|-------|
| primary | #2E7D32 | Group savings chart bars, Sync Now, cycle progress bar |
| primaryContainer | #A6F1A6 | Cycle progress card background, group total chip |
| onPrimaryContainer | #002106 | Cycle progress card text |
| secondary | #FF8F00 | Individual savings line chart, member balance text |
| secondaryContainer | #FFDDB3 | Group savings member avatar backgrounds, individual total card |
| onSecondaryContainer | #2A1700 | Individual total card text |
| tertiaryContainer | #D2E4FF | Individual savings member avatar backgrounds |
| onTertiaryContainer | #001C39 | Individual avatar initials |
| primaryContainer (chip deposit) | #A6F1A6 | Deposit chip background |
| errorContainer | #FFDAD6 | Withdrawal chip background |
| onPrimaryContainer (chip) | #002106 | Deposit chip text |
| onErrorContainer | #410002 | Withdrawal chip text |
| surface | #FAFAFA | Card backgrounds |
| surfaceVariant | #DEE5DA | Last-sync band background |
| onSurfaceVariant | #424942 | Subtitles, chart labels, secondary text |
