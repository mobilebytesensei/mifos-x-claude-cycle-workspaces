# Group List — API Contract

## Endpoints

| ID | Method | Endpoint | Auth | Writable | Companion Tool | Cache |
|---|---|---|---|---|---|---|
| `get_my_groups` | GET | `/companion/groups` | Bearer | no | COMP-GRP-001 | 300 s SWR |

## Request / Response Details

### GET /companion/groups (COMP-GRP-001 — list)

**Query Params**

| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| userId | String | yes (from token) | — | Caller identity (resolved from Bearer token server-side) |
| limit | Int | no | `20` | Page size |
| offset | Int | no | `0` | Pagination offset |

**Response**

| Field | Type | Description |
|---|---|---|
| items | List<GroupSummary> | Page of groups caller belongs to |
| totalCount | Int | Total groups for this user |
| hasMore | Boolean | Whether more pages exist |

---

## DTOs

### GroupSummary
```
groupId: String
groupName: String
groupType: String           // typeSlug: vsla, rosca, etc.
poolModel: String           // ACCUMULATING | ROTATING_PAYOUT | NONE
memberCount: Int
overdueRate: Double         // 0.0 – 1.0 fraction
isCycleEnd: Boolean
viewerRole: String          // ORGANIZER | TREASURER | SECRETARY | MEMBER
```

### GroupListResponse
```
items: List<GroupSummary>
totalCount: Int
hasMore: Boolean
```

## Computed Fields (client-side)

| Field | Derivation |
|---|---|
| `healthIndicator` | `overdueRate < 0.05 → GREEN; < 0.20 → AMBER; else RED` |

Health indicator is NOT returned by the API — computed from `overdueRate` on each card render.

## Pagination Contract

- `page_size = 20`
- Append to `group_list_cache` on each page: `append_to_existing`
- Pull-to-refresh: `bypass_and_refresh` — clears cache, loads offset=0 fresh
- `hasMore` → trigger `OnLoadMore` on scroll to bottom

## Offline Behaviour

`group_list_cache` serves stale data (300 s SWR) when offline. A "Last synced" banner
is shown when serving cache. Pull-to-refresh while offline shows a "No internet" snackbar
and does not clear the cache.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `network.offline` | Serve stale list from `group_list_cache` + last-synced banner |
| `401 Unauthorized` | Navigate to login-signup |
| `500 Server` | Show error banner + retry button |
| `empty response (totalCount == 0)` | Render `Empty` state with Create Group + Join with Code CTAs |
