# Personal Dashboard — Feature Spec

## Overview

Member home screen. Unified identity — no `selfServiceToken`/`clientId` nav-param; identity
resolves from the auth token. Fetches member dashboard data from the companion API
(`GET /companion/member/dashboard`) via `MemberDashboardRepository` using Store5
stale-while-revalidate with a SQLDelight offline cache. Supports multi-group context
(member in N groups): a group selector chip row appears when `myGroups.size > 1` — selecting
a chip re-calls the API with `selectedGroupId`. The share-out projection card adapts by
`poolModel`: ACCUMULATING shows a projected KES amount; ROTATING_PAYOUT shows the rotation
position (`#N in queue`) and next-recipient ETA. A **loan entry card** (un-deferred from
v1.1 now that personal-loans + loan-request ship) is a pure navigation tile into the member's
own loan list. The authenticated top bar hosts a **profile overflow menu** reaching the two
shared screens — Settings and Sync Status. Zero groups → Empty state.

**Acceptance Criteria:**

- AC1: Fetch `get_member_dashboard` on mount (GET `/companion/member/dashboard`,
       optional `selectedGroupId` param; cache 300 s SWR per `userId:groupId`).
- AC2: `group_selector_row` visible only when `myGroups.size > 1`. Tapping a chip
       (`OnSelectGroup`) re-calls the API with the selected `groupId` and updates all cards.
- AC3: Savings summary card shows the aggregate `groupLinkedSavingsBalance +
       individualSavingsBalance` with a per-source breakdown row; tap → `OnSavingsCardClick`
       → personal-savings (forwards clientId, groupLinkedSavingsId, individualSavingsId?).
- AC4: Share-out projection card adapts by `poolModel`:
  - `ACCUMULATING` → `shareout_amount` "Projected Share-Out KES {shareOutProjection}"
  - `ROTATING_PAYOUT` → `rotation_position_text` "#{rotationPosition} in queue" +
    `next_recipient_eta_text` "Your turn: ~{nextRecipientEta}"; `shareout_amount` hidden
- AC5: **Loan entry card rendered** — `loan_card` (icon + "My Loans" + sublabel + chevron);
       tap → `OnLoansCardClick` → personal-loans forwarding `clientId`. Pure navigation.
- AC6: **Profile overflow menu** on the top bar → `menu_settings` (`OnSettingsClick` →
       settings) and `menu_sync_status` (`OnSyncStatusClick` → sync-status).
- AC7: Empty state when `myGroups.isEmpty()` → layout collapses to `[top_bar, group_banner]`.
- AC8: No `selfServiceToken`, `clientId`, or `staffId` nav params — identity from token.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| personal-dashboard | `PersonalDashboardScreen` | Scrollable column | Member home: group selector, savings summary, loan entry, share-out projection, recent activity; overflow menu → settings/sync-status |

## State Model

### PersonalDashboardViewModel

**State — `PersonalDashboardState`**

| Field | Type | Default | Description |
|---|---|---|---|
| memberName | String | `""` | From session.displayName (no clientId nav-param) |
| clientId | Long | `0L` | From get_member_dashboard — forwarded to personal-savings + personal-loans |
| groupLinkedSavingsId | Long | `0L` | Forwarded to personal-savings |
| individualSavingsId | Long? | `null` | Optional voluntary individual account id — forwarded to personal-savings |
| myGroups | List<GroupSummary> | `emptyList()` | Multi-group support |
| selectedGroup | GroupSummary? | `null` | Active group context |
| poolModel | String | `""` | ACCUMULATING \| ROTATING_PAYOUT \| NONE (from selectedGroup.typeConfig) |
| groupLinkedSavingsBalance | Double | `0.0` | |
| individualSavingsBalance | Double | `0.0` | |
| shareOutProjection | Double | `0.0` | ACCUMULATING types |
| rotationPosition | Int? | `null` | ROTATING_PAYOUT types |
| nextRecipientEta | String? | `null` | ROTATING_PAYOUT types |
| recentTransactions | List<SavingsTransactionDto> | `emptyList()` | Recent activity |
| isRefreshing | Boolean | `false` | Pull-to-refresh |
| isLoading | Boolean | `true` | Initial load |
| error | DashboardError? | `null` | Typed error |

**Screen States**

| State | Components |
|---|---|
| `Loading` | top_bar, group_banner, shimmer_loading |
| `Content` | top_bar, group_banner, savings_summary_card, loan_card, shareout_projection_card, recent_activity_header, recent_activity_list, pull_to_refresh |
| `Error` | top_bar, group_banner, error_state |
| `Empty` | top_bar, group_banner |

**Actions — `PersonalDashboardAction`**

| Action | Trigger |
|---|---|
| `OnRefresh` | Pull-to-refresh |
| `OnRetry` | Tap Retry button |
| `OnSavingsCardClick` | Tap savings summary card |
| `OnSelectGroup(groupId)` | Tap group selector chip |
| `OnLoansCardClick` | Tap loan entry card |
| `OnSettingsClick` | Tap Settings in profile overflow menu |
| `OnSyncStatusClick` | Tap Sync Status in profile overflow menu |

**Events — `PersonalDashboardEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToSavings` | — | `OnSavingsCardClick` |
| `NavigateToGroupList` | — | (group context) |
| `NavigateToLoans` | clientId: Long | `OnLoansCardClick` |
| `NavigateToSettings` | — | `OnSettingsClick` |
| `NavigateToSyncStatus` | — | `OnSyncStatusClick` |

**DI Dependencies**

- `MemberDashboardRepository` — companion API /companion/member/dashboard
- `SessionManager`

## Navigation

| Action | Destination | Params |
|---|---|---|
| `OnSavingsCardClick` | `personal-savings` | clientId, groupLinkedSavingsId, individualSavingsId? |
| `OnLoansCardClick` | `personal-loans` | clientId |
| `OnSettingsClick` | `settings` | — |
| `OnSyncStatusClick` | `sync-status` | — |
| `OnSelectGroup` | (self re-fetch) | selectedGroupId |

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `get_member_dashboard` | GET | `/companion/member/dashboard` | — | no |

**Identity:** resolved entirely from Bearer token. No userId/clientId param.
Optional `selectedGroupId` query param (first call uses `null` → server returns primary
group summary). The loan/settings/sync-status navigations are pure client-side — no endpoints.

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `member_dashboard_cache` | userId:groupId | upsert | stale_while_revalidate 300 s; keyed per group — chip switch triggers new API call (different key) |
| `savings_transactions` | transactionId | upsert | shared; serve_stale offline |

**Navigation-only triggers** (no cache/network): `OnLoansCardClick` → personal-loans,
`OnSettingsClick` → settings, `OnSyncStatusClick` → sync-status.

**Sync Queue:** none (read-only screen).

## DTOs

See `exports/personal-dashboard/API.md` for full DTO schemas.

Key types: `MemberDashboardResponse` (memberName, clientId, groupLinkedSavingsId,
individualSavingsId?, myGroups[], selectedGroup, poolModel, groupLinkedSavingsBalance,
individualSavingsBalance, shareOutProjection?, rotationPosition?, nextRecipientEta?,
recentTransactions[]), `GroupSummary` (groupId, name, poolModel),
`SavingsTransactionDto` (id, date, type, amount).

## Designed UX Reference

- **Preview HTML:** `idea-layer/screens/personal-dashboard/preview/`
- **Mockup:** `idea-layer/mockups/personal-dashboard/MOCKUP.md`
- **Design conformance:** Top bar (primary #2E7D32) carries a notification bell and a
  **more-vertical overflow icon** opening a menu with Settings (`settings_24_regular`) and
  Sync Status (`arrow_sync_24_regular`). Savings summary card (elevation 2dp, corner lg,
  `margin_top: -20dp` overlapping the group banner) shows aggregate total in displaySmall +
  a colored-dot breakdown row. **Loan entry card** below it: `wallet_credit_card_24_filled`
  tertiary-tinted icon + "My Loans" labelLarge + "View your loans and request a new one"
  sublabel + trailing chevron — a pure navigation tile (no balance projected). Share-out
  projection card (secondaryContainer) discriminates ACCUMULATING vs ROTATING_PAYOUT
  mutually-exclusively off `poolModel`. Group selector is a horizontal scrollable chip row
  (visible only when `myGroups.size > 1`) with the active chip filled.
