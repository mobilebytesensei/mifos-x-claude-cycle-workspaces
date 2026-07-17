# Group List — Feature Spec

## Overview

Entry hub showing all groups the authenticated user belongs to. Loads paginated via
`get_my_groups` (COMP-GRP-001). Client-side search filters the loaded list — no additional
API call. Health indicator computed client-side from `overdueRate`. FAB navigates to
`group-type-picker` to create a new group. Empty state (zero groups) shows dual CTAs:
Create Group and Join with Code.

**Acceptance Criteria:**

- AC1: On mount call `get_my_groups` (paginated, page_size=20); paginate on scroll with
       `append_to_existing` strategy.
- AC2: Search is client-side filter of the loaded list — does NOT trigger an API call.
- AC3: Health indicator chip per card is derived client-side from `overdueRate`
       (GREEN <5%, AMBER <20%, RED ≥20%).
- AC4: Pull-to-refresh bypasses cache and forces a fresh fetch (`bypass_and_refresh`).
- AC5: FAB leads to `group-type-picker`.
- AC6: Zero groups state shows Create Group CTA (→ group-type-picker) and
       Join with Code CTA (→ join-with-code).

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| group-list | `GroupListScreen` | Scrollable list + FAB | My groups; client-side search; paginated |

## State Model

### GroupListViewModel

**State — `GroupListState`**

| Field | Type | Default | Description |
|---|---|---|---|
| groups | List<GroupSummary> | `emptyList()` | Loaded groups (all pages so far) |
| filteredGroups | List<GroupSummary> | `emptyList()` | Client-side filtered view |
| searchQuery | String | `""` | Search input |
| isLoading | Boolean | `true` | Initial load |
| isRefreshing | Boolean | `false` | Pull-to-refresh in progress |
| isLoadingMore | Boolean | `false` | Pagination in progress |
| hasMore | Boolean | `false` | Whether more pages available |
| error | String? | `null` | Error banner |

**Health indicator computed field (per GroupSummary):**

```
healthIndicator = when {
    overdueRate < 0.05 -> "GREEN"
    overdueRate < 0.20 -> "AMBER"
    else -> "RED"
}
```

**Screen States**

| State | Components |
|---|---|
| `Loading` | Shimmer list items |
| `Content` | search_bar, group_card_list (with health chips), FAB |
| `Empty` | zero_groups_illustration, create_group_cta, join_with_code_cta |
| `Error` | error_banner + retry_button |
| `SearchEmpty` | "No groups match '{query}'" empty results message |

**Actions — `GroupListAction`**

| Action | Trigger |
|---|---|
| `OnSearchChange(query)` | Search input change |
| `OnSearchClear` | Clear search |
| `OnGroupTap(groupId)` | Tap a group card |
| `OnLoadMore` | Scroll to end of list |
| `OnRefresh` | Pull-to-refresh |
| `OnCreateGroup` | FAB tap or zero state CTA |
| `OnJoinGroup` | Zero state "Join with Code" CTA |
| `OnRetry` | Tap retry on error |

**Events — `GroupListEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToGroupDashboard` | groupId: String | `OnGroupTap` |
| `NavigateToGroupTypePicker` | — | `OnCreateGroup` / FAB |
| `NavigateToJoinWithCode` | — | `OnJoinGroup` |

**DI Dependencies**

- `GroupRepository` — get_my_groups
- `SessionManager`

## Navigation

| Action | Destination | Params |
|---|---|---|
| `OnGroupTap` | `group-dashboard` | `groupId` |
| `OnCreateGroup` | `group-type-picker` | — |
| `OnJoinGroup` | `join-with-code` | — |

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `get_my_groups` | GET | `/companion/groups?userId={userId}&limit={limit}&offset={offset}` | COMP-GRP-001 | no |

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `group_list_cache` | groupId | upsert | stale_while_revalidate 300 s; bypass_and_refresh on pull-to-refresh; append_to_existing on pagination |

**Sync Queue:** none (read-only screen).

**Pagination:** page_size=20; `hasMore` derived from `totalCount > loaded.size`.
Pull-to-refresh: clears cache + reloads from offset=0.

## DTOs

See `exports/group-list/API.md` for full DTO schemas.

Key types: `GroupSummary` (groupId, groupName, groupType, poolModel, memberCount,
overdueRate, isCycleEnd, viewerRole), `GroupListResponse` (items, totalCount, hasMore).

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/group-list/prompts/`
- **Preview HTML:** `idea-layer/screens/group-list/preview/`
- **Design conformance:** Each group card shows group name in titleMedium, type badge
  in a small chip, member count, and a health indicator chip (color-coded circle).
  Search bar is sticky below the top app bar. FAB is `+` with label "New Group". Zero
  state illustration is a village scene with two buttons vertically stacked:
  "Create a Group" (filled primary) + "Join with Code" (outlined).
