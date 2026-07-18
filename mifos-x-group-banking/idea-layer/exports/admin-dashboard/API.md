# Admin Dashboard — API Contract

## Endpoints

| ID | Method | Endpoint | Auth | Writable | Cache |
|---|---|---|---|---|---|
| `get_organizer_dashboard` | GET | `/companion/organizer/dashboard` | Bearer | no | 300 s SWR |

**Identity:** No userId, staffId, or selfServiceToken params. Identity resolved entirely
from Bearer token server-side. This is the unified identity pattern — no admin client type.

## Request / Response Details

### GET /companion/organizer/dashboard

**Request:** no query params.

**Response**

| Field | Type | Description |
|---|---|---|
| myGroupCount | Int | Groups this organizer administers (NOT system total) |
| activeMemberCount | Int | Active members across my groups |
| pendingShareOutCount | Int | Groups with shareout due (NOT overdue loans) |
| upcomingMeetingCount | Int | Meetings this week across my groups |
| fieldOfficerEnabled | Boolean | Whether field officer functionality is active |
| todaysSchedule | List<ScheduledMeeting> | Today's group meetings |
| recentActivity | List<ActivityItem> | Last 10 activity events across my groups |

**Errors**

| Code | Meaning | Behaviour |
|---|---|---|
| 401 | Unauthorized | Navigate to login-signup |
| 403 | Caller is not an organizer | Navigate to personal-dashboard (replace back stack) |
| 500 | Server error | Show error banner + retry |

---

## DTOs

### OrganizerDashboardSummary
```
myGroupCount: Int
activeMemberCount: Int
pendingShareOutCount: Int
upcomingMeetingCount: Int
fieldOfficerEnabled: Boolean
todaysSchedule: List<ScheduledMeeting>
recentActivity: List<ActivityItem>
```

### ScheduledMeeting
```
groupId: String
groupName: String
meetingTime: String    // HH:MM
meetingDay: String     // e.g. "Monday"
memberCount: Int
```

### ActivityItem
```
id: String
groupId: String
groupName: String
activityType: String   // MEMBER_JOINED | CONTRIBUTION_MADE | SHAREOUT_EXECUTED | INVITE_SENT
actorName: String
timestamp: String      // ISO-8601
amount: Long?          // KES — present for CONTRIBUTION_MADE and SHAREOUT_EXECUTED
```

## KPI Field Name Notes

| Old Fineract field | Companion field | Reason |
|---|---|---|
| `totalGroups` | `myGroupCount` | Scoped to organizer's own groups, not system total |
| `overdueLoansCount` | `pendingShareOutCount` | Savings groups product — no loan overdue concept |

## Offline Behaviour

`organizer_dashboard_cache` (300 s SWR) serves stale data offline. A "Last synced"
timestamp banner appears at the top. Pull-to-refresh while offline shows a "No internet"
snackbar.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `403 Forbidden` | Redirect to personal-dashboard (back stack replaced — no back to admin) |
| `network.offline` | Serve `organizer_dashboard_cache` + `scheduled_meetings_cache` + `activity_feed_cache` |
| `401 Unauthorized` | Navigate to login-signup |
| `500 Server` | Error banner + retry button |
