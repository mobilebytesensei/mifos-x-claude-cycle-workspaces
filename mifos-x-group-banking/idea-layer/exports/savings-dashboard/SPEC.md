# Savings Dashboard — Feature Spec

## Overview

Group-level savings overview with two tabs: GROUP (aggregate) and INDIVIDUAL (viewer's
savings). Makes 2 parallel API calls on mount. Both tabs present contribution-model-aware
displays — the `cycle_progress_card` adapts its labels to `contributionModel`. The shared
`savings_transactions` table is used across savings-dashboard, member-savings-detail, and
personal-dashboard.

**Acceptance Criteria:**

- AC1: 2 parallel calls on mount: `get_group_savings_summary` and
       `get_individual_savings_summary` (both 300 s SWR).
- AC2: GROUP tab: bar chart of weekly contributions; cycle progress card adapts label:
  - `SHARE_BASED_VARIABLE` → "X shares × KES Y / share"
  - `FIXED_AMOUNT` → "KES Z / meeting"
  - `FIXED_NEGOTIATED` → "Negotiated contribution"
- AC3: INDIVIDUAL tab: sparkline of personal savings over cycle; personal totals card.
- AC4: Pull-to-refresh on either tab refreshes both summaries.
- AC5: Tap on a member row in GROUP tab → navigates to `member-savings-detail`.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| savings-dashboard | `SavingsDashboardScreen` | TabRow (GROUP / INDIVIDUAL) + scrollable content per tab | Group and individual savings overview |

## State Model

### SavingsDashboardViewModel

**State — `SavingsDashboardState`**

| Field | Type | Default | Description |
|---|---|---|---|
| groupId | String | `""` | From nav params |
| contributionModel | String | `""` | From typeConfig (nav arg or group cache) |
| selectedTab | Int | `0` | 0 = GROUP, 1 = INDIVIDUAL |
| groupSummary | GroupSavingsSummary? | `null` | From get_group_savings_summary |
| individualSummary | IndividualSavingsSummary? | `null` | From get_individual_savings_summary |
| isLoading | Boolean | `true` | Initial parallel load |
| isRefreshing | Boolean | `false` | Pull-to-refresh in progress |
| error | String? | `null` | Error banner |

**Screen States**

| State | Components |
|---|---|
| `Loading` | Skeleton for tab content |
| `GroupTabContent` | bar_chart, cycle_progress_card (model-adaptive), member_savings_list |
| `IndividualTabContent` | sparkline_chart, personal_totals_card, transaction_list |
| `Error` | error_banner + retry_button |

**Contribution Model Label Map (client-side)**

| contributionModel | cycle_progress_card label |
|---|---|
| SHARE_BASED_VARIABLE | "{sharesTotal} shares × KES {shareValue} / share" |
| FIXED_AMOUNT | "KES {contributionAmount} / meeting" |
| FIXED_NEGOTIATED | "Negotiated contribution" |

**Actions — `SavingsDashboardAction`**

| Action | Trigger |
|---|---|
| `OnTabSelect(index)` | Tab tap |
| `OnMemberTap(memberId)` | Tap member row in GROUP tab |
| `OnRefresh` | Pull-to-refresh |
| `OnBack` | Back arrow |
| `OnRetry` | Retry on error |

**Events — `SavingsDashboardEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToMemberSavingsDetail` | groupId: String, memberId: String | `OnMemberTap` |
| `NavigateBack` | — | `OnBack` |

**DI Dependencies**

- `SavingsRepository` — both API calls

## Navigation

| Action | Destination | Params |
|---|---|---|
| `OnMemberTap` | `member-savings-detail` | groupId, memberId |
| `OnBack` | `group-dashboard` | — |

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `get_group_savings_summary` | GET | `/companion/groups/{groupId}/savings` | — | no |
| `get_individual_savings_summary` | GET | `/companion/groups/{groupId}/savings/individual` | — | no |

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `group_savings_cache` | groupId | upsert | stale_while_revalidate 300 s |
| `individual_savings_cache` | groupId | upsert | stale_while_revalidate 300 s |
| `savings_transactions` | transactionId | upsert | shared; serve_stale offline |

**Sync Queue:** none (read-only screen).

## DTOs

See `exports/savings-dashboard/API.md` for full DTO schemas.

Key types: `GroupSavingsSummary` (totalCorpus, weeklyContributionData[], memberSavings[],
cycleProgress), `IndividualSavingsSummary` (myTotalSavings, mySharesHeld?,
sparklineData[], recentTransactions[]).

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/savings-dashboard/prompts/`
- **Preview HTML:** `idea-layer/screens/savings-dashboard/preview/`
- **Design conformance:** TabRow at top with "Group" and "Individual" tabs. GROUP tab
  leads with a bar chart (7 bars = last 7 meetings). Below is the cycle_progress_card:
  tinted card showing contribution model label, meetings completed / cycle total, and
  a linear progress bar. Member savings list rows show avatar, name, total saved in
  bodyMedium, and a small "→" icon. INDIVIDUAL tab leads with a sparkline (line chart)
  and a personal totals card (total saved, shares held for SHARE_BASED_VARIABLE only).
