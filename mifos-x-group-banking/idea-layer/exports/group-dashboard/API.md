# Group Dashboard — API Contract

## Endpoints

| ID | Method | Endpoint | Auth | Writable | Companion Tool | Cache |
|---|---|---|---|---|---|---|
| `get_group` | GET | `/companion/groups/{groupId}` | Bearer | no | COMP-GRP-001 | 300 s SWR |
| `get_viewer_role` | GET | `/companion/datatables/dt_member_role/{groupId}` | Bearer | no | COMP-DT-002 read | 300 s SWR |
| `get_group_corpus` | GET | `/companion/groups/{groupId}/corpus` | Bearer | no | — | 60 s SWR |
| `get_group_accounts` | GET | `/companion/groups/{groupId}/accounts` | Bearer | no | — | 300 s SWR |

All 4 calls are executed in parallel on mount. Short 60 s cache on corpus reflects financial freshness requirement.

## Request / Response Details

### GET /companion/groups/{groupId} (COMP-GRP-001 — read)

**Response**

| Field | Type | Description |
|---|---|---|
| groupId | String | Companion group ID |
| groupName | String | Display name |
| groupType | String | typeSlug (vsla, rosca, etc.) |
| poolModel | String | ACCUMULATING \| ROTATING_PAYOUT \| NONE |
| contributionModel | String | SHARE_BASED_VARIABLE \| FIXED_AMOUNT \| FIXED_NEGOTIATED |
| memberCount | Int | Total member count |
| isCycleEnd | Boolean | Whether cycle is in shareout window |
| overdueRate | Double | Fraction of members overdue (0.0–1.0) |

---

### GET /companion/datatables/dt_member_role/{groupId} (COMP-DT-002 read — viewer role)

Returns the authenticated user's role row in this group.

**Response**

| Field | Type | Description |
|---|---|---|
| rowId | Long | Datatable row ID |
| groupId | String | Group |
| memberId | String | Caller's member ID |
| role | String | ORGANIZER \| TREASURER \| SECRETARY \| MEMBER |

**Error:** 404 → caller not in this group → redirect to group-list.

---

### GET /companion/groups/{groupId}/corpus

**Response — ACCUMULATING pool_model:**

| Field | Type | Description |
|---|---|---|
| poolModel | String | "ACCUMULATING" |
| totalCorpus | Long | Total pooled KES (cents) |
| projectedShareout | Long | Expected per-member shareout amount |
| cycleNumber | Int | Current cycle number |

**Response — ROTATING_PAYOUT pool_model:**

| Field | Type | Description |
|---|---|---|
| poolModel | String | "ROTATING_PAYOUT" |
| currentRotationNumber | Int | Which payout turn is active |
| totalRotations | Int | Total members in payout queue |
| nextRecipientName | String | Display name of next recipient |
| nextRecipientEta | String | ISO-8601 date of next payout |
| cycleNumber | Int | Current cycle number |

---

### GET /companion/groups/{groupId}/accounts

**Response**

| Field | Type | Description |
|---|---|---|
| savingsAccountId | String | Active Fineract savings account |
| loanAccountId | String? | Active loan account (null if no loan product) |

---

## DTOs

### GroupDetail
```
groupId: String
groupName: String
groupType: String
poolModel: String
contributionModel: String
memberCount: Int
isCycleEnd: Boolean
overdueRate: Double
```

### ViewerRoleRow
```
rowId: Long
groupId: String
memberId: String
role: String   // ORGANIZER | TREASURER | SECRETARY | MEMBER
```

### GroupCorpus (sealed / discriminated by poolModel)
```
// ACCUMULATING
poolModel: String = "ACCUMULATING"
totalCorpus: Long
projectedShareout: Long
cycleNumber: Int

// ROTATING_PAYOUT
poolModel: String = "ROTATING_PAYOUT"
currentRotationNumber: Int
totalRotations: Int
nextRecipientName: String
nextRecipientEta: String
cycleNumber: Int
```

### GroupAccounts
```
savingsAccountId: String
loanAccountId: String?
```

## Computed Fields (client-side)

| Field | Derivation |
|---|---|
| `healthIndicator` | `if overdueRate < 0.05 → GREEN; < 0.20 → AMBER; else RED` |
| `canShareOut` | `isCycleEnd && role ∈ {ORGANIZER, TREASURER}` |

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `404 get_viewer_role` | Caller not a member → navigate to group-list |
| `404 get_group` | Group deleted → navigate to group-list with error snackbar |
| `network.offline` | Serve stale from each cache table + "Last synced" banner |
| `partial failure (1–3 of 4 calls fail)` | Show content with warning banner for failed sections |
| `401 Unauthorized` | Navigate to login-signup |
