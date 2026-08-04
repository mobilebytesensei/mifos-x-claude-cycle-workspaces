# Group Management — Feature Spec

## Overview

Group Management is the foundational admin feature of MifosSave. It enables field officers and treasurers to create and configure VSLA savings groups (modelled as Fineract Centers), view their full portfolio of groups on a list screen, and access per-group operational dashboards. The group dashboard is the central hub for corpus fund monitoring (FR-018), cycle tracking, and quick navigation to meetings, members, and loans. Group creation is a 3-step wizard that writes both a Fineract Center and a `dt_group_config` datatable entry. All screens are offline-first with stale-while-revalidate caching and offline queueing via SyncQueue.

**Feature ID**: group-management
**Priority**: Must
**Client**: Admin (staff auth)
**Version**: 1.0.0
**FR Coverage**: FR-001 (group creation + config), FR-018 (corpus fund real-time tracking), FR-020 (penalty/contribution rules defined at creation)
**Fineract Mapping**: Centers API + `dt_group_config` datatable + `dt_group_corpus` datatable

**Acceptance Criteria**
- Admin can create a savings group with group name (3–60 chars), office assignment, currency (default KES), meeting day, meeting time, minimum contribution, maximum contribution, loan multiplier, interest rate, cycle length in months, and late fine amount.
- Group list shows all groups managed by the logged-in staff member, each with group name, cycle number, member count, last meeting date, and health indicator (GREEN/AMBER/RED based on overdue loan rate).
- Group dashboard displays real-time corpus fund balance; a warning banner blocks loan disbursement when `corpus.currentBalance < config.minimumDisbursementThreshold`.
- Group creation supports offline queueing: when offline, the group is stored in SyncQueue and submitted when connectivity is restored.
- Search on group list filters by group name client-side without additional API calls.
- Share-Out quick action on the dashboard is only enabled when the group has reached the end of its cycle (`cycleWeek == cycleLengthWeeks`).
- All API responses are cached with stale-while-revalidate; offline reads show cached data.

---

## Screens

| Screen | Composable | Layout | Description |
|--------|-----------|--------|-------------|
| group-list | `GroupListScreen` | `Scaffold` + `LazyColumn` + `FloatingActionButton` | Scrollable list of all managed groups; search bar at top; FAB to create group |
| group-dashboard | `GroupDashboardScreen` | `Scaffold` + `LazyColumn` (scrollable sections) | Single-group hub: corpus card, quick actions, savings summary, activity feed |
| group-create | `GroupCreateScreen` | `Scaffold` + `Pager` (3-step wizard) | 3-step wizard: Step 1 Identity, Step 2 Rules, Step 3 Review |

---

## State Model

### GroupListViewModel

**State fields**:

| Name | Type | Default |
|------|------|---------|
| isLoading | Boolean | true |
| groups | List\<Group\> | emptyList() |
| searchQuery | String | "" |
| filteredGroups | List\<Group\> | emptyList() |
| error | GroupListError? | null |
| isRefreshing | Boolean | false |

**Actions**:
- `OnGroupClick(groupId: String)` — Tap group card
- `OnSearch(query: String)` — Type in search bar
- `OnClearSearch` — Tap clear icon in search bar
- `OnCreateGroup` — Tap FAB
- `OnRefresh` — Pull to refresh
- `Retry` — Tap retry button on error state

**Events**:
- `NavigateToGroupDashboard(groupId: String)`
- `NavigateToCreateGroup`
- `ShowSnackbar(message: String)`

**DI**: `GroupRepository`, `NetworkMonitor`, `SessionManager`

---

### GroupDashboardViewModel

**State fields**:

| Name | Type | Default |
|------|------|---------|
| isLoading | Boolean | true |
| group | Group? | null |
| corpus | GroupCorpus? | null |
| config | GroupConfig? | null |
| accounts | GroupAccounts? | null |
| recentActivity | List\<ActivityItem\> | emptyList() |
| isCorpusInsufficient | Boolean | false |
| isCycleEnd | Boolean | false |
| error | GroupDashboardError? | null |

**Actions**:
- `OnStartMeeting` — Tap Start Meeting button
- `OnViewMembers` — Tap View Members button
- `OnViewLoans` — Tap View Loans button
- `OnShareOut` — Tap Share-Out button
- `OnRefresh` — Pull to refresh
- `Retry` — Tap retry on error
- `OnBack` — Tap back arrow

**Events**:
- `NavigateToMeetingCalendar(groupId: String)`
- `NavigateToMemberList(groupId: String)`
- `NavigateToLoanList(groupId: String)`
- `NavigateToShareOut(groupId: String)`
- `ShowCorpusBlockedDialog`
- `ShowSnackbar(message: String)`

**DI**: `GroupRepository`, `CorpusRepository`, `NetworkMonitor`, `SessionManager`

---

### GroupCreateViewModel

**State fields**:

| Name | Type | Default |
|------|------|---------|
| currentStep | Int | 1 |
| totalSteps | Int | 3 |
| groupName | String | "" |
| officeId | Long? | null |
| officeName | String | "" |
| currency | String | "KES" |
| meetingDay | String | "" |
| meetingTime | String | "" |
| contributionMin | String | "" |
| contributionMax | String | "" |
| loanMultiplier | String | "3" |
| interestRate | String | "10" |
| cycleLengthMonths | String | "12" |
| fineAmount | String | "" |
| isSubmitting | Boolean | false |
| isSubmitSuccess | Boolean | false |
| officeList | List\<Office\> | emptyList() |
| validationErrors | Map\<String, String\> | emptyMap() |
| error | GroupCreateError? | null |
| isOffline | Boolean | false |

**Actions**:
- `OnNameChange(value: String)`, `OnOfficeSelect(officeId: Long, officeName: String)`, `OnCurrencyChange(value: String)`, `OnMeetingDaySelect(day: String)`, `OnMeetingTimeSelect(time: String)`, `OnContributionMinChange(value: String)`, `OnContributionMaxChange(value: String)`, `OnLoanMultiplierChange(value: String)`, `OnInterestRateChange(value: String)`, `OnCycleLengthChange(value: String)`, `OnFineAmountChange(value: String)`, `OnNextStep`, `OnPreviousStep`, `OnSubmit`, `OnBack`

**Events**:
- `NavigateToGroupDashboard(groupId: String)`
- `NavigateBack`
- `ShowOfflineSyncDialog`
- `ShowSnackbar(message: String)`

**DI**: `GroupRepository`, `OfficeRepository`, `SyncQueueRepository`, `NetworkMonitor`

---

## Navigation

| From | To | Condition | Params |
|------|----|-----------|--------|
| Bottom Nav / App Launch | group-list | user_authenticated | — |
| group-list card tap | group-dashboard | always | groupId: String |
| group-list FAB | group-create | always | — |
| group-create success | group-dashboard | submit success | groupId: String (from create_center response) |
| group-create back | group-list | always | — |
| group-dashboard "Start Meeting" | meeting-calendar | corpus sufficient | groupId: String |
| group-dashboard "Members" | member-list | always | groupId: String |
| group-dashboard "Loans" | loan-list | always | groupId: String |
| group-dashboard "Share-Out" | share-out-preview | isCycleEnd == true | groupId: String |
| group-dashboard back | group-list | always | — |

---

## API Endpoints

| ID | Method | Path | Auth | Cache |
|----|--------|------|------|-------|
| get_centers | GET | /centers | Bearer (staffId from session) | TTL 300s, stale-while-revalidate |
| get_center | GET | /centers/{centerId} | Bearer | TTL 300s, stale-while-revalidate |
| get_center_accounts | GET | /centers/{centerId}/accounts | Bearer | TTL 180s, stale-while-revalidate |
| get_group_corpus | GET | /datatables/dt_group_corpus/{centerId} | Bearer | TTL 60s, network-first |
| get_group_config | GET | /datatables/dt_group_config/{centerId} | Bearer | TTL 600s, stale-while-revalidate |
| get_offices | GET | /offices | Bearer | TTL 3600s, stale-while-revalidate |
| create_center | POST | /centers | Bearer | — |
| create_group_config | POST | /datatables/dt_group_config/{centerId} | Bearer | — |

---

## Design Tokens Used

| Token | Value | Usage |
|-------|-------|-------|
| primary | #2E7D32 | Top bar background, FAB, filled buttons, corpus balance text |
| onPrimary | #FFFFFF | Top bar text, FAB icon, button labels |
| primaryContainer | #A6F1A6 | Group header card background, group dashboard header |
| onPrimaryContainer | #002106 | Text on group header card |
| secondary | #FF8F00 | Amber chip cycle text, share-out button border |
| secondaryContainer | #FFDDB3 | Cycle chip background, member count chip |
| onSecondaryContainer | #2A1700 | Cycle chip text |
| tertiary | #1565C0 | Total savings balance text |
| tertiaryContainer | #D2E4FF | Offline notice banner background |
| onTertiaryContainer | #001C39 | Offline notice text |
| error | #D32F2F | Corpus block banner border, arrears indicators |
| errorContainer | #FFDAD6 | Corpus block banner background |
| onErrorContainer | #410002 | Corpus block banner text |
| surface | #FAFAFA | Card backgrounds |
| onSurface | #1A1C19 | Primary body text |
| surfaceVariant | #DEE5DA | Shimmer backgrounds |
| onSurfaceVariant | #424942 | Supporting text, inactive chips |
| cornerRadius.medium | 12dp | Group list card, shimmer |
| cornerRadius.large | 16dp | Dashboard section cards |
| elevation.level2 | 3dp | Group list cards |
| elevation.level4 | 8dp | Corpus card |
| spacing.lg | 16dp | Standard card padding |
| spacing.xl | 24dp | Corpus card inner padding |
| minTouchTarget | 48dp | Search bar; 56dp for FAB and action buttons |
| titleMedium | 16sp / 500 weight | Card section labels |
| displaySmall | 36sp / 400 weight | Corpus balance figure |
| bodySmall | 12sp / 400 weight | Supporting text on group cards |
