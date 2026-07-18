# Share-Out Execute — API Contract

## Endpoints

| ID | Method | Endpoint | Auth | Writable | Companion Tool |
|---|---|---|---|---|---|
| `execute_accumulating_shareout` | POST | `/companion/groups/{groupId}/shareout/execute` | Bearer | yes | COMP-DIST-001 |
| `execute_rotation_payout` | POST | `/companion/groups/{groupId}/rotation/execute` | Bearer | yes | COMP-DIST-002 |

Endpoint selected by `poolModel` nav arg: `ACCUMULATING → COMP-DIST-001`, `ROTATING_PAYOUT → COMP-DIST-002`.

## Request / Response Details

### POST /companion/groups/{groupId}/shareout/execute (COMP-DIST-001 — accumulating)

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| cycleNumber | Int | yes | Must match current cycle |
| idempotencyKey | String | yes | `"groupId:{groupId}:cycle:{cycleNumber}"` |
| memberDistributions | List<MemberDistributionInput> | yes | Per-member amounts to disburse |

**MemberDistributionInput**

| Field | Type | Description |
|---|---|---|
| memberId | String | Member to pay |
| amount | Long | KES amount (cents) |

**Response**

| Field | Type | Description |
|---|---|---|
| executionId | String | Unique execution ID |
| status | String | COMPLETED \| PARTIAL \| FAILED |
| memberResults | List<MemberExecutionResult> | Per-member outcome |

**MemberExecutionResult**

| Field | Type | Description |
|---|---|---|
| memberId | String | |
| memberName | String | |
| amount | Long | Disbursed amount |
| status | String | PAID \| FAILED |
| failureReason | String? | Null on success |

---

### POST /companion/groups/{groupId}/rotation/execute (COMP-DIST-002 — rotating payout)

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| cycleNumber | Int | yes | Current cycle |
| idempotencyKey | String | yes | `"groupId:{groupId}:cycle:{cycleNumber}"` |

**Response**

| Field | Type | Description |
|---|---|---|
| executionId | String | Unique execution ID |
| recipientMemberId | String | Who received the payout |
| recipientMemberName | String | Display name |
| amount | Long | KES (cents) |
| status | String | COMPLETED \| FAILED |
| nextRotationNumber | Int | Next recipient position |

**Errors (both endpoints)**

| Code | Meaning |
|---|---|
| 400 | Invalid request or cycle mismatch |
| 401 | Unauthorized |
| 403 | Caller not ORGANIZER or TREASURER |
| 409 | Already executed for this cycle (idempotency) — return prior response |
| 503 | Fineract unavailable — companion enqueues and returns 202 Accepted |

---

## DTOs

### ExecuteShareOutRequest (ACCUMULATING)
```
cycleNumber: Int
idempotencyKey: String
memberDistributions: List<MemberDistributionInput>
```

### MemberDistributionInput
```
memberId: String
amount: Long
```

### ExecuteShareOutResponse (ACCUMULATING)
```
executionId: String
status: String        // COMPLETED | PARTIAL | FAILED
memberResults: List<MemberExecutionResult>
```

### MemberExecutionResult
```
memberId: String
memberName: String
amount: Long
status: String        // PAID | FAILED
failureReason: String?
```

### ExecuteRotationPayoutRequest (ROTATING_PAYOUT)
```
cycleNumber: Int
idempotencyKey: String
```

### ExecuteRotationPayoutResponse (ROTATING_PAYOUT)
```
executionId: String
recipientMemberId: String
recipientMemberName: String
amount: Long
status: String        // COMPLETED | FAILED
nextRotationNumber: Int
```

### MemberExecutionStatus (local UI model)
```
memberId: String
memberName: String
amount: Long
status: String        // PENDING | PROCESSING | PAID | FAILED
failureReason: String?
```

## Offline Behaviour

When offline at time of execution, the request is serialized and enqueued to `sync_queue`:
- `entity_type: EXECUTE_SHAREOUT`
- `priority: HIGH`
- `idempotency_key: "groupId:{groupId}:cycle:{cycleNumber}"`

The idempotency key prevents double-execution if the queue drains multiple times (server
returns 409 on duplicate, which the client treats as success and marks the queue entry
`completed`).

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `409 Conflict (already executed)` | Show "Already completed" success state with prior executionId |
| `403 Forbidden` | "Only organisers/treasurers can execute shareout" error state |
| `PARTIAL status` | Per-member list with FAILED rows + individual retry buttons |
| `FAILED status` | All-failed error state with full retry |
| `network.offline` | Enqueue to sync_queue HIGH priority + show offline-queued state |
| `401 Unauthorized` | Navigate to login-signup |
| `500/503 Server` | Show error banner + retry |
