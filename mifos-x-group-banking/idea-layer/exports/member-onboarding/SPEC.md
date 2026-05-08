# Member Onboarding — Feature Spec

## Overview

Member Onboarding enables administrators to build and manage the membership roster of each savings group. The feature covers three screens: member-list (paginated roster with role badges and loan status), member-profile (detailed per-member view with savings sparkline, active loan summary, and attendance rate), and member-add (single-page form to create a new Fineract Client with photo, phone validation, and role assignment). All member data is backed by Fineract Clients API with role metadata in the `dt_member_role` custom datatable. Offline queueing via SyncQueue ensures new members can be added even without connectivity.

**Feature ID**: member-onboarding
**Priority**: Must
**Client**: Admin (staff auth)
**Version**: 1.0.0
**FR Coverage**: FR-002 (onboard members with name, photo, phone, role assignment)
**Fineract Mapping**: Clients API (`/clients`, `/clients/{id}`, `/clients/{id}/accounts`, `/clients/{id}/images`) + `dt_member_role` datatable

**Acceptance Criteria**
- Admin can view a paginated list of all members in a group, with each row showing avatar (photo or initials), name, role badge (CHAIRPERSON/TREASURER/SECRETARY/MEMBER), savings balance, and loan status (ACTIVE/NONE/OVERDUE).
- Admin can navigate to a member's profile by tapping the row or using swipe-to-reveal action.
- Member profile displays: large avatar, full name, phone number, join date, role badge, savings history sparkline chart, current savings balance, active loan summary (with arrears warning if applicable), and meeting attendance rate (fraction + progress bar).
- Chairperson can change a member's role via a bottom sheet (accessible through "Edit Role" button visible only to chairpersons).
- Admin can add a new member via a form: first name, last name, phone (Kenya E.164 format, validated), optional photo (camera or gallery), and role selection dropdown.
- Phone uniqueness is validated: duplicate phone triggers PhoneAlreadyExists error.
- Member-add supports offline queueing: when offline, the member creation is stored in SyncQueue (operations: CREATE_MEMBER + ASSIGN_MEMBER_ROLE + UPLOAD_MEMBER_PHOTO).
- Pagination: member list fetches 20 per page, loads more on scroll to end.

---

## Screens

| Screen | Composable | Layout | Description |
|--------|-----------|--------|-------------|
| member-list | `MemberListScreen` | `Scaffold` + `LazyColumn` + `FloatingActionButton` | Paginated member roster with role badges and loan status |
| member-profile | `MemberProfileScreen` | `Scaffold` + `LazyColumn` (scrollable sections) | Per-member detail with sparkline, loan summary, attendance |
| member-add | `MemberAddScreen` | `Scaffold` + `Column` + scrollable form | Single-page form for new member creation with photo capture |

---

## State Model

### MemberListViewModel

**State fields**:

| Name | Type | Default |
|------|------|---------|
| isLoading | Boolean | true |
| members | List\<Member\> | emptyList() |
| groupId | String | "" |
| groupName | String | "" |
| isLoadingMore | Boolean | false |
| hasMorePages | Boolean | true |
| currentOffset | Int | 0 |
| error | MemberListError? | null |
| isRefreshing | Boolean | false |

**Actions**:
- `OnMemberClick(memberId: String)` — Tap member row or swipe action
- `OnAddMember` — Tap FAB
- `OnLoadMore` — Scroll to end of list
- `OnRefresh` — Pull to refresh
- `Retry` — Tap retry on error
- `OnBack` — Tap back

**Events**:
- `NavigateToMemberProfile(memberId: String, groupId: String)`
- `NavigateToAddMember(groupId: String)`
- `ShowSnackbar(message: String)`

**DI**: `MemberRepository`, `GroupRepository`, `NetworkMonitor`

---

### MemberProfileViewModel

**State fields**:

| Name | Type | Default |
|------|------|---------|
| isLoading | Boolean | true |
| member | Member? | null |
| accounts | MemberAccounts? | null |
| role | MemberRole? | null |
| savingsHistory | List\<SavingsDataPoint\> | emptyList() |
| attendanceRate | Float | 0f |
| meetingsAttended | Int | 0 |
| totalMeetings | Int | 0 |
| isCurrentUserChairperson | Boolean | false |
| isEditingRole | Boolean | false |
| selectedRole | MemberRole? | null |
| isUpdatingRole | Boolean | false |
| error | MemberProfileError? | null |

**Actions**:
- `OnEditRole` — Tap Edit Role button (chairperson only)
- `OnRoleSelected(role: MemberRole)` — Select role in sheet
- `OnConfirmRoleChange` — Tap Confirm in role edit sheet
- `OnDismissRoleEdit` — Dismiss sheet
- `OnRefresh` — Pull to refresh
- `Retry` — Tap retry on error
- `OnBack` — Tap back arrow

**Events**:
- `NavigateBack`
- `ShowRoleEditSheet`
- `DismissRoleEditSheet`
- `ShowSnackbar(message: String)`

**DI**: `MemberRepository`, `AttendanceRepository`, `NetworkMonitor`, `SessionManager`

---

### MemberAddViewModel

**State fields**:

| Name | Type | Default |
|------|------|---------|
| firstName | String | "" |
| lastName | String | "" |
| phone | String | "" |
| photoUri | String? | null |
| selectedRole | MemberRole | MemberRole.MEMBER |
| validationErrors | Map\<String, String\> | emptyMap() |
| isSubmitting | Boolean | false |
| isSubmitSuccess | Boolean | false |
| isOffline | Boolean | false |
| error | MemberAddError? | null |
| showPhotoPicker | Boolean | false |
| groupId | String | "" |

**Actions**:
- `OnFirstNameChange(value: String)`, `OnLastNameChange(value: String)`, `OnPhoneChange(value: String)`
- `OnPhotoPickerOpen` — Tap photo area
- `OnPhotoCaptured(uri: String)` — Camera capture complete
- `OnPhotoSelected(uri: String)` — Gallery image selected
- `OnPhotoRemoved` — Tap remove photo
- `OnRoleSelected(role: MemberRole)` — Select from dropdown
- `OnSubmit` — Tap Save Member
- `OnBack` — Tap back or close

**Events**:
- `NavigateToMemberProfile(memberId: String, groupId: String)`
- `NavigateBack`
- `ShowPhotoPicker`
- `ShowOfflineSyncDialog`
- `ShowSnackbar(message: String)`

**DI**: `MemberRepository`, `SyncQueueRepository`, `ImagePickerHelper`, `NetworkMonitor`, `SessionManager`

---

## Navigation

| From | To | Condition | Params |
|------|----|-----------|--------|
| group-dashboard "Members" button | member-list | always | groupId: String |
| member-list row tap | member-profile | always | memberId: String, groupId: String |
| member-list swipe action | member-profile | always | memberId: String, groupId: String |
| member-list FAB | member-add | always | groupId: String |
| member-add success | member-profile | always | memberId: String (from create_client response), groupId: String |
| member-add offline queue | member-list | offline queue triggered | — |
| member-add back | member-list | always | — |
| member-profile back | member-list | always | — |
| member-profile "Edit Role" | role edit bottom sheet | isCurrentUserChairperson=true | — |

---

## API Endpoints

| ID | Method | Path | Auth | Cache |
|----|--------|------|------|-------|
| get_group_members | GET | /groups/{groupId}/clients | Bearer | TTL 120s, stale-while-revalidate |
| get_client | GET | /clients/{clientId} | Bearer | TTL 300s, stale-while-revalidate |
| get_client_accounts | GET | /clients/{clientId}/accounts | Bearer | TTL 120s, stale-while-revalidate |
| get_member_role | GET | /datatables/dt_member_role/{clientId} | Bearer | TTL 300s, stale-while-revalidate |
| update_member_role | PUT | /datatables/dt_member_role/{clientId} | Bearer (chairperson only) | — |
| create_client | POST | /clients | Bearer | — |
| assign_member_role | POST | /datatables/dt_member_role/{clientId} | Bearer | — |
| upload_photo | POST | /clients/{clientId}/images | Bearer | — |

---

## Design Tokens Used

| Token | Value | Usage |
|-------|-------|-------|
| primary | #2E7D32 | Top bars, FABs, filled buttons, savings balance text |
| onPrimary | #FFFFFF | Text and icons on primary backgrounds |
| primaryContainer | #A6F1A6 | Member header card background, swipe-action background |
| onPrimaryContainer | #002106 | Text on pale-green header card |
| secondary | #FF8F00 | Amber — TREASURER role chip on profile |
| secondaryContainer | #FFDDB3 | Avatar fallback background, TREASURER list chip |
| onSecondaryContainer | #2A1700 | Text on amber chip |
| tertiary | #1565C0 | SECRETARY role chip on profile, attendance rate text |
| tertiaryContainer | #D2E4FF | SECRETARY list chip background, offline banner |
| onTertiaryContainer | #001C39 | Text on offline banner |
| error | #D32F2F | Arrears border on active loan card |
| errorContainer | #FFDAD6 | Arrears banner background, OVERDUE loan badge bg |
| onErrorContainer | #410002 | Arrears banner text |
| surface | #FAFAFA | All card backgrounds |
| onSurface | #1A1C19 | Primary body text |
| surfaceVariant | #DEE5DA | Shimmer, dividers, MEMBER chip background |
| onSurfaceVariant | #424942 | Supporting text |
| cornerRadius.full | 9999dp | Circular avatars |
| cornerRadius.large | 16dp | Profile section cards |
| cornerRadius.medium | 12dp | Member list items (swipe) |
| elevation.level2 | 3dp | Profile section cards |
| spacing.lg | 16dp | Card padding |
| spacing.xl | 20dp | Profile header padding |
| minTouchTarget | 48dp | Standard; 56dp for Save Member button and FAB |
| headlineMedium | 28sp / 400 | Savings balance on profile |
| titleMedium | 16sp / 500 | Card section labels |
| bodyLarge | 16sp / 400 | Member name in list |
| bodySmall | 12sp / 400 | Supporting text in list |
| chart.sparkline | line_color=#2E7D32, fill=#A6F1A6 | Savings history chart |
| progress.attendance | indicator: ≥80%=#1565C0, ≥60%=#FF8F00, <60%=#D32F2F | Attendance bar color |
