# Personal Dashboard — Feature Spec

## Overview

Member home screen showing savings summary and shareout projection across all groups the
caller belongs to. A group selector chip row appears when the caller is in multiple groups
(`myGroups.size > 1`) — selecting a chip calls the API with `selectedGroupId` and updates
the dashboard. Shareout projection card adapts by `poolModel`: ACCUMULATING shows projected
KES amount; ROTATING_PAYOUT shows queue position and next payout ETA. Loan summary card
is **deferred to v1.1**. Zero groups state shows dual CTAs: Create Group + Join with Code.
Identity resolved from token — no `selfServiceToken` parameter.

**Acceptance Criteria:**

- AC1: Fetch `get_member_dashboard` on mount (GET `/companion/member/dashboard`,
       optional `selectedGroupId` param; cache 300 s SWR per `userId:groupId`).
- AC2: `group_selector_row` visible only when `myGroups.size > 1`. Tapping a chip
       calls API with the selected `groupId` and updates all summary cards.
- AC3: Savings summary card shows `myTotalSavings` and `mySharesHeld`
       (if SHARE_BASED_VARIABLE) for the selected group.
- AC4: Shareout projection card adapts by `poolModel`:
  - `ACCUMULATING` → "Projected Share-Out KES {amount}"
  - `ROTATING_PAYOUT` → "#N in queue · Next payout {ETA date}"
- AC5: Loan summary card deferred — NOT rendered in v1.0.
- AC6: Zero groups state → dual CTAs: "Create a Group" (→ group-type-picker) and
       "Join with Code" (→ join-with-code).
- AC7: No `selfServiceToken`, `clientId`, or `staffId` nav params — identity from token.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| personal-dashboard | `PersonalDashboardScreen` | Scrollable column | Member home: group selector, savings summary, shareout projection |

## State Model

### PersonalDashboardViewModel

**State — `PersonalDashboardState`**

| Field | Type | Default | Description |
|---|---|---|---|
| myGroups | List<GroupSummary> | `emptyList()` | All groups caller belongs to |
| selectedGroupId | String? | `null` | Currently selected group (null = first group / primary) |
| selectedGroupName | String | `""` | For display in header |
| poolModel | String | `""` | ACCUMULATING \| ROTATING_PAYOUT \| NONE for selected group |
| contributionModel | String | `""` | For savings card label |
| myTotalSavings | Long | `0L` | KES saved in selected group |
| mySharesHeld | Int? | `null` | SHARE_BASED_VARIABLE only |
| projectedShareOut | Long? | `null` | ACCUMULATING: projected payout |
| rotationQueuePosition | Int? | `null` | ROTATING_PAYOUT: position in queue |
| nextPayoutEta | String? | `null` | ROTATING_PAYOUT: ISO-8601 date |
| recentTransactions | List<SavingsTransaction> | `emptyList()` | Last 5 transactions |
| isLoading | Boolean | `true` | Initial load |
| isRefreshing | Boolean | `false` | Pull-to-refresh |
| error | String? | `null` | Error banner |

**Screen States**

| State | Components |
|---|---|
| `Loading` | Skeleton for cards |
| `ZeroGroups` | zero_groups_illustration, create_group_cta, join_group_cta |
| `Content` | group_selector_row (if >1 group), savings_summary_card, shareout_projection_card, recent_transactions |
| `Error` | error_banner + retry_button |

**Actions — `PersonalDashboardAction`**

| Action | Trigger |
|---|---|
| `OnGroupSelect(groupId)` | Tap group chip in selector |
| `OnRefresh` | Pull-to-refresh |
| `OnViewSavings` | Tap savings card |
| `OnViewGroup` | Tap group name in header |
| `OnCreateGroup` | Zero state CTA |
| `OnJoinGroup` | Zero state CTA |
| `OnRetry` | Retry on error |

**Events — `PersonalDashboardEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToSavingsDashboard` | groupId: String | `OnViewSavings` |
| `NavigateToGroupDashboard` | groupId: String | `OnViewGroup` |
| `NavigateToGroupTypePicker` | — | `OnCreateGroup` |
| `NavigateToJoinWithCode` | — | `OnJoinGroup` |

**DI Dependencies**

- `MemberDashboardRepository` — get_member_dashboard
- `SessionManager`
- `NetworkMonitor`

## Navigation

| Action | Destination | Params |
|---|---|---|
| `OnViewSavings` | `savings-dashboard` | groupId |
| `OnViewGroup` | `group-dashboard` | groupId |
| `OnCreateGroup` | `group-type-picker` | — |
| `OnJoinGroup` | `join-with-code` | — |

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `get_member_dashboard` | GET | `/companion/member/dashboard` | — | no |

**Identity:** resolved entirely from Bearer token. No userId param.
Optional `selectedGroupId` query param (first call uses `null` → server returns primary
group summary).

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `member_dashboard_cache` | userId:groupId | upsert | stale_while_revalidate 300 s; keyed per group — chip switch triggers new API call (different key) |
| `savings_transactions` | transactionId | upsert | shared; serve_stale offline |

**Key design:** cache is keyed `userId:groupId`. When the user switches the group chip,
the new groupId produces a different cache key → a new API call is made (not client-side
filtering of a single shared record).

**Sync Queue:** none (read-only screen).

## DTOs

See `exports/personal-dashboard/API.md` for full DTO schemas.

Key types: `MemberDashboardResponse` (myGroups[], selectedGroupSummary,
myTotalSavings, mySharesHeld?, poolModel, projectedShareOut?, rotationQueuePosition?,
nextPayoutEta?, recentTransactions[]), `GroupSummary` (groupId, name, poolModel),
`SavingsTransaction` (transactionId, transactionDate, amount, transactionType, description).

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/personal-dashboard/prompts/`
- **Preview HTML:** `idea-layer/screens/personal-dashboard/preview/`
- **Design conformance:** Group selector is a horizontal scrollable chip row with group
  initials and abbreviated name. Selected chip has filled background. Savings summary card
  shows "My Savings" in labelLarge, total in displaySmall, and shares (if applicable) in
  bodyMedium below. Shareout projection card: ACCUMULATING shows a coins icon + "Projected
  Share-Out KES X" with a tagline "End of {month}"; ROTATING_PAYOUT shows a queue-number
  badge (#N) and "Next payout: {date}". Loan summary card is completely absent in v1.0
  — no placeholder, no "coming soon" tile. Zero state: village illustration with two
  stacked buttons (Create a Group primary, Join with Code outlined).
