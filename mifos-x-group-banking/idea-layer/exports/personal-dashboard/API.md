# Personal Dashboard — API Contract

## Endpoints

| ID | Method | Endpoint | Auth | Writable | Cache |
|---|---|---|---|---|---|
| `get_member_dashboard` | GET | `/companion/member/dashboard` | Bearer | no | 300 s SWR (keyed per userId:groupId) |

**Identity:** No userId, selfServiceToken, or clientId params. Bearer token resolves identity.

## Request / Response Details

### GET /companion/member/dashboard

**Query Params**

| Param | Type | Required | Description |
|---|---|---|---|
| selectedGroupId | String? | no | If null, server returns primary (first) group summary |

Group chip selection triggers a new call with `selectedGroupId` set to the chosen group.
Cache key is `userId:selectedGroupId` — each group selection has its own cached record.

**Response**

| Field | Type | Description |
|---|---|---|
| myGroups | List<GroupSummary> | All groups the caller belongs to |
| selectedGroupId | String | Which group's summary is in this response |
| selectedGroupName | String | Display name of selected group |
| poolModel | String | ACCUMULATING \| ROTATING_PAYOUT \| NONE |
| contributionModel | String | SHARE_BASED_VARIABLE \| FIXED_AMOUNT \| FIXED_NEGOTIATED |
| myTotalSavings | Long | KES saved in selected group |
| mySharesHeld | Int? | SHARE_BASED_VARIABLE only |
| projectedShareOut | Long? | ACCUMULATING: projected end-of-cycle payout |
| rotationQueuePosition | Int? | ROTATING_PAYOUT: caller's queue position |
| nextPayoutEta | String? | ROTATING_PAYOUT: ISO-8601 date of next payout for caller |
| recentTransactions | List<SavingsTransaction> | Last 5 transactions in selected group |

**Errors**

| Code | Meaning |
|---|---|
| 401 | Unauthorized → navigate to login-signup |
| 404 | selectedGroupId not found or caller not a member → reset to primary group |
| 500 | Server error |

---

## DTOs

### MemberDashboardResponse
```
myGroups: List<GroupSummary>
selectedGroupId: String
selectedGroupName: String
poolModel: String
contributionModel: String
myTotalSavings: Long
mySharesHeld: Int?
projectedShareOut: Long?
rotationQueuePosition: Int?
nextPayoutEta: String?
recentTransactions: List<SavingsTransaction>
```

### GroupSummary (for group selector chips)
```
groupId: String
name: String
poolModel: String   // drives chip icon
```

### SavingsTransaction (shared DTO)
```
transactionId: String
transactionDate: String    // ISO-8601
amount: Long               // KES (cents)
transactionType: String    // CREDIT | DEBIT
description: String
```

## Shareout Projection Display Logic (client-side)

| poolModel | Card content |
|---|---|
| ACCUMULATING | "Projected Share-Out KES {projectedShareOut}" |
| ROTATING_PAYOUT | "#{rotationQueuePosition} in queue · Next payout {nextPayoutEta}" |
| NONE | Card hidden |

## Cache Design

`member_dashboard_cache` is keyed `userId:groupId`:
- Initial load: `selectedGroupId = null` → server returns primary group; client caches with key `userId:primaryGroupId`
- Group chip tap: new call with `selectedGroupId = {groupId}` → cached separately at `userId:{groupId}`
- Each group chip has independent cache; switching chips may serve stale or fresh depending on recency

## Offline Behaviour

When offline, `member_dashboard_cache` (keyed per selected group) serves stale data.
A "Last synced" banner shown. Group chip switches while offline serve the stale cache
for that group if available, or show "Loading unavailable offline" for groups not yet
cached.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `network.offline (cache available)` | Serve stale + last-synced banner |
| `network.offline (no cache)` | Offline error state with retry |
| `empty myGroups` | ZeroGroups state — Create Group + Join with Code CTAs |
| `404 selectedGroupId` | Reset to null (primary group) and retry |
| `401 Unauthorized` | Navigate to login-signup |
| `500 Server` | Error banner + retry |
