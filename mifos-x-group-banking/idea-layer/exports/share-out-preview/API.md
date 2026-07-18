# Share-Out Preview — API Contract

## Endpoints

| ID | Method | Endpoint | Auth | Writable | Companion Tool | Cache |
|---|---|---|---|---|---|---|
| `get_shareout_preview` | GET | `/companion/groups/{groupId}/shareout/preview` | Bearer | no | COMP-DIST-001 | network_first 60 s |

## Request / Response Details

### GET /companion/groups/{groupId}/shareout/preview

**Query Params**

| Param | Type | Required | Description |
|---|---|---|---|
| cycle | Int | yes | Cycle number to preview |

**Response (common fields)**

| Field | Type | Description |
|---|---|---|
| cycleNumber | Int | Cycle this preview is for |
| poolModel | String | ACCUMULATING \| ROTATING_PAYOUT |
| shareoutFormula | String | PRORATA_SHARES \| PRORATA_SAVINGS \| EQUAL \| FIXED_ORDER \| LOTTERY \| AUCTION |
| totalAmount | Long | Total KES to be distributed |

**Additional fields — ACCUMULATING:**

| Field | Type | Description |
|---|---|---|
| memberDistributions | List<MemberDistribution> | Per-member breakdown |

**Additional fields — ROTATING_PAYOUT:**

| Field | Type | Description |
|---|---|---|
| nextRecipient | RotationRecipient | Next payout recipient info |

**Errors**

| Code | Meaning |
|---|---|
| 400 | Invalid cycle number |
| 401 | Unauthorized |
| 403 | Not a member of this group |
| 404 | Group or cycle not found |
| 409 | Cycle not in shareout window yet |

---

## DTOs

### ShareOutPreviewResponse
```
cycleNumber: Int
poolModel: String
shareoutFormula: String
totalAmount: Long
memberDistributions: List<MemberDistribution>?   // ACCUMULATING only
nextRecipient: RotationRecipient?                // ROTATING_PAYOUT only
```

### MemberDistribution
```
memberId: String
memberName: String
sharesHeld: Int?        // SHARE_BASED_VARIABLE only
shareAmount: Long       // KES (cents)
percentOfTotal: Double  // 0.0–1.0
```

### RotationRecipient
```
memberId: String
memberName: String
rotationNumber: Int    // This recipient's position in queue
payoutAmount: Long     // KES (cents)
etaDate: String        // ISO-8601
```

## Formula Label Map (client-side derivation)

| shareoutFormula value | UI label |
|---|---|
| PRORATA_SHARES | "By Shares" |
| PRORATA_SAVINGS | "By Savings" |
| EQUAL | "Equal Split" |
| FIXED_ORDER | "Fixed Order" |
| LOTTERY | "Lottery" |
| AUCTION | "Auction" |

## Offline Behaviour

Preview requires connectivity (network_first, 60 s TTL). If offline and stale cache
exists, the stale data is shown with a "Data may be outdated" banner. If no cache, show
offline error state with "Requires internet" message.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `409 Conflict` | "Cycle not yet in shareout window" error state — back to group-dashboard |
| `403 Forbidden` | "Not authorised to view shareout" — back to group-dashboard |
| `network.offline (no cache)` | Offline error state |
| `network.offline (cache available)` | Stale data + outdated banner |
| `401 Unauthorized` | Navigate to login-signup |
