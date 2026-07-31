# Personal Dashboard — API Contract

## Endpoints

| ID | Method | Endpoint | Auth | Writable | Cache |
|---|---|---|---|---|---|
| `get_member_dashboard` | GET | `/companion/member/dashboard` | Bearer | no | 300 s SWR (keyed per userId:groupId) |

**Identity:** No userId, selfServiceToken, or clientId params. Bearer token resolves identity.

The loan-card, Settings, and Sync-Status affordances are **pure client-side navigation** —
they call no endpoint.

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
| memberName | String | Display name (session identity) |
| clientId | Long | Signed-in member's Fineract client id — forwarded to personal-savings + personal-loans nav_params |
| groupLinkedSavingsId | Long | Selected group's linked savings account id — forwarded to personal-savings |
| individualSavingsId | Long? | Optional voluntary individual savings account id (null when none) |
| myGroups | List<GroupSummary> | All groups the caller belongs to |
| selectedGroup | GroupSummary | Which group's summary is in this response |
| poolModel | String | ACCUMULATING \| ROTATING_PAYOUT \| NONE (from selectedGroup.typeConfig) |
| groupLinkedSavingsBalance | Double | KES saved in the selected group |
| individualSavingsBalance | Double | KES in the voluntary individual account |
| shareOutProjection | Double? | ACCUMULATING: projected end-of-cycle payout |
| rotationPosition | Int? | ROTATING_PAYOUT: caller's queue position |
| nextRecipientEta | String? | ROTATING_PAYOUT: ISO-8601 date of next payout for caller |
| recentTransactions | List<SavingsTransactionDto> | Recent transactions in selected group |

**Errors**

| Code | Meaning |
|---|---|
| 401 | Unauthorized → clear session (app shell re-auth; no in-screen navigate) |
| 404 | Member not found in any group |
| 500 | Server error |

---

## DTOs

### MemberDashboardResponse
```
memberName: String
clientId: Long
groupLinkedSavingsId: Long
individualSavingsId: Long?
myGroups: List<GroupSummary>
selectedGroup: GroupSummary
poolModel: String
groupLinkedSavingsBalance: Double
individualSavingsBalance: Double
shareOutProjection: Double?
rotationPosition: Int?
nextRecipientEta: String?
recentTransactions: List<SavingsTransactionDto>
```

### GroupSummary (for group selector chips)
```
groupId: String
name: String
poolModel: String   // ACCUMULATING | ROTATING_PAYOUT | NONE — drives chip + card variant
```

### SavingsTransactionDto (shared DTO)
```
id: String
date: String     // ISO-8601
type: String     // DEPOSIT | WITHDRAWAL
amount: Double   // KES
```

## Share-out Projection Display Logic (client-side)

| poolModel | Card content |
|---|---|
| ACCUMULATING | `shareout_amount` "Projected Share-Out KES {shareOutProjection}" |
| ROTATING_PAYOUT | `rotation_position_text` "#{rotationPosition} in queue" + `next_recipient_eta_text` "Your turn: ~{nextRecipientEta}" |
| NONE | Card content minimal (no pool projection) |

## Cache Design

`member_dashboard_cache` is keyed `userId:groupId`:
- Initial load: `selectedGroupId = null` → server returns primary group; cached at `userId:primaryGroupId`
- Group chip tap: new call with `selectedGroupId = {groupId}` → cached separately at `userId:{groupId}`
- Each group chip has independent cache; switching chips may serve stale or fresh depending on recency
- Pull-to-refresh: `bypass_and_refresh` replaces the current group's cache row

## Offline Behaviour

When offline, `member_dashboard_cache` (keyed per selected group) serves stale data via
`cmp-network-monitor` + Store5; an offline badge/snackbar is shown. Group chip switches while
offline serve the stale cache for that group if available.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `network.offline (cache available)` | Serve stale + offline badge |
| `network.offline (no cache)` | Error state with retry |
| `empty myGroups` | Empty state (layout collapses to top_bar + group_banner) |
| `404 Member not found` | Error / reset to primary group |
| `401 Unauthorized` | Clear session — app shell handles re-auth (no in-screen navigate) |
| `500 Server` | Error state + retry |
