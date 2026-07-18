# Admin Dashboard — Feature Spec

## Overview

Organizer/administrator home screen. Makes a single API call with no identity parameters —
the companion resolves the caller's identity from the Bearer token. Displays 4 KPI cards
with organizer-scoped metrics (NOT Fineract admin totals): My Groups, Active Members,
Upcoming Share-Outs, and Share-Outs Due. Optional Field Officer tile gated by
`fieldOfficerEnabled` flag. 403 response means the caller is not an organizer and the
screen redirects to `personal-dashboard`.

**Acceptance Criteria:**

- AC1: Single call `get_organizer_dashboard` on mount (GET
       `/companion/organizer/dashboard` — no userId param, identity from token).
- AC2: 4 KPI cards:
  1. `myGroupCount` — "My Groups" (NOT total groups in system)
  2. `activeMemberCount` — "Active Members"
  3. `pendingShareOutCount` — "Share-Outs Due" (NOT overdue loans)
  4. `upcomingMeetingCount` — "Upcoming Meetings"
- AC3: Optional `field_officer_tile` shown only when `fieldOfficerEnabled == true`.
- AC4: `403 Forbidden` response → navigate to `personal-dashboard`.
- AC5: Today's Schedule section lists scheduled meetings for today. Recent Activity
       section lists last 10 activity items.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| admin-dashboard | `AdminDashboardScreen` | Scrollable column | Organizer KPIs, quick nav, schedule, recent activity |

## State Model

### AdminDashboardViewModel

**State — `AdminDashboardState`**

| Field | Type | Default | Description |
|---|---|---|---|
| myGroupCount | Int | `0` | Groups the organizer runs |
| activeMemberCount | Int | `0` | Members across my groups |
| pendingShareOutCount | Int | `0` | Groups with shareout due |
| upcomingMeetingCount | Int | `0` | Meetings scheduled this week |
| fieldOfficerEnabled | Boolean | `false` | Flag for optional tile |
| todaysSchedule | List<ScheduledMeeting> | `emptyList()` | Today's meetings |
| recentActivity | List<ActivityItem> | `emptyList()` | Last 10 activity events |
| isLoading | Boolean | `true` | Initial fetch |
| isRefreshing | Boolean | `false` | Pull-to-refresh |
| error | String? | `null` | Error banner |

**Screen States**

| State | Components |
|---|---|
| `Loading` | Skeleton for KPI cards and lists |
| `Content` | 4 kpi_cards, quick_nav_section, todays_schedule, recent_activity |
| `Error` | error_banner + retry_button |
| `Forbidden` | (instant redirect — no render) |

**Actions — `AdminDashboardAction`**

| Action | Trigger |
|---|---|
| `OnGroupsTap` | Tap "My Groups" KPI card or quick nav |
| `OnMembersTap` | Tap "Active Members" |
| `OnShareOutsTap` | Tap "Share-Outs Due" |
| `OnFieldOfficerTap` | Tap Field Officer tile (if enabled) |
| `OnRefresh` | Pull-to-refresh |
| `OnRetry` | Tap retry on error |

**Events — `AdminDashboardEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToGroupList` | — | `OnGroupsTap` |
| `NavigateToPersonalDashboard` | — | 403 redirect |

**DI Dependencies**

- `OrganizerDashboardRepository` — get_organizer_dashboard
- `SessionManager`
- `NetworkMonitor`

## Navigation

| Condition | Destination | Params |
|---|---|---|
| `OnGroupsTap` | `group-list` | — |
| `403 response` | `personal-dashboard` | — (replace back stack) |

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `get_organizer_dashboard` | GET | `/companion/organizer/dashboard` | — | no |

**Identity:** resolved entirely from Bearer token on server side. No `userId`, `staffId`,
or `selfServiceToken` parameters.

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `organizer_dashboard_cache` | userId | upsert | stale_while_revalidate 300 s |
| `scheduled_meetings_cache` | groupId:meetingTime | upsert | stale_while_revalidate 300 s |
| `activity_feed_cache` | id | upsert | serve_stale offline |

**Sync Queue:** none (read-only screen).

## DTOs

See `exports/admin-dashboard/API.md` for full DTO schemas.

Key types: `OrganizerDashboardSummary` (myGroupCount, activeMemberCount,
pendingShareOutCount, upcomingMeetingCount, fieldOfficerEnabled, todaysSchedule[],
recentActivity[]), `ScheduledMeeting` (groupId, groupName, meetingTime, meetingDay,
memberCount), `ActivityItem` (id, groupId, groupName, activityType, actorName,
timestamp, amount?).

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/admin-dashboard/prompts/`
- **Preview HTML:** `idea-layer/screens/admin-dashboard/preview/`
- **Design conformance:** KPI cards are a 2×2 grid of `ElevatedCard` with icon, metric
  label, and value in headlineMedium. "My Groups" card uses a groups icon; "Share-Outs
  Due" uses a clock-with-exclamation icon (NOT a loan/debt icon — this is savings groups).
  Quick nav is a horizontal scrollable row of icon+label chips. Today's Schedule is a
  vertical list with meeting time on the left and group name on the right. Recent Activity
  uses a timeline design with activity type icons. Field Officer tile (when enabled) is
  a full-width outlined card below quick nav.
