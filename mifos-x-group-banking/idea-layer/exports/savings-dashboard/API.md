# Savings Dashboard — API Contract

## Endpoints

| ID | Method | Endpoint | Auth | Writable | Cache |
|---|---|---|---|---|---|
| `get_group_savings_summary` | GET | `/companion/groups/{groupId}/savings` | Bearer | no | 300 s SWR |
| `get_individual_savings_summary` | GET | `/companion/groups/{groupId}/savings/individual` | Bearer | no | 300 s SWR |

Both calls are executed in parallel on mount.

## Request / Response Details

### GET /companion/groups/{groupId}/savings

**Request:** no query params.

**Response**

| Field | Type | Description |
|---|---|---|
| totalCorpus | Long | Total group savings pool (KES, cents) |
| cycleProgress | CycleProgress | Meetings completed / total |
| weeklyContributionData | List<WeeklyContribution> | Last N meetings bar chart data |
| memberSavings | List<MemberSavingsRow> | Per-member total savings |

**CycleProgress**
```
meetingsCompleted: Int
cycleTotalMeetings: Int
currentCycleNumber: Int
```

**WeeklyContribution**
```
meetingDate: String    // ISO-8601
totalContributed: Long // KES (cents)
```

**MemberSavingsRow**
```
memberId: String
memberName: String
totalSaved: Long       // KES (cents)
sharesHeld: Int?       // SHARE_BASED_VARIABLE only
```

---

### GET /companion/groups/{groupId}/savings/individual

Returns the authenticated caller's individual savings within this group.

**Response**

| Field | Type | Description |
|---|---|---|
| myTotalSavings | Long | Total KES saved by caller |
| mySharesHeld | Int? | SHARE_BASED_VARIABLE only |
| sparklineData | List<SavingsDataPoint> | Cumulative savings over cycle |
| recentTransactions | List<SavingsTransaction> | Last 10 transactions |

---

## DTOs

### GroupSavingsSummary
```
totalCorpus: Long
cycleProgress: CycleProgress
weeklyContributionData: List<WeeklyContribution>
memberSavings: List<MemberSavingsRow>
```

### CycleProgress
```
meetingsCompleted: Int
cycleTotalMeetings: Int
currentCycleNumber: Int
```

### WeeklyContribution
```
meetingDate: String
totalContributed: Long
```

### MemberSavingsRow
```
memberId: String
memberName: String
totalSaved: Long
sharesHeld: Int?
```

### IndividualSavingsSummary
```
myTotalSavings: Long
mySharesHeld: Int?
sparklineData: List<SavingsDataPoint>
recentTransactions: List<SavingsTransaction>
```

### SavingsDataPoint (shared DTO)
```
date: String           // ISO-8601
cumulativeAmount: Long // KES (cents)
```

### SavingsTransaction (shared DTO — also used by member-savings-detail and personal-dashboard)
```
transactionId: String
transactionDate: String     // ISO-8601
amount: Long                // KES (cents)
transactionType: String     // CREDIT | DEBIT
description: String
```

## Offline Behaviour

Both summaries serve from cache (300 s SWR) when offline. A "Last synced" banner is shown
below the TabRow. Pull-to-refresh while offline shows a "No internet" snackbar and does
not clear the cache.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `network.offline` | Serve stale summaries + last-synced banner |
| `partial failure (1 of 2 calls)` | Load available tab; show warning on other tab |
| `401 Unauthorized` | Navigate to login-signup |
| `403 Forbidden` | "Not a member of this group" — back to group-list |
| `500 Server` | Error banner + retry |
