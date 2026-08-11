# Group Create — API Contract

## Endpoints

| ID | Method | Endpoint | Auth | Writable | Companion Tool |
|---|---|---|---|---|---|
| `get_offices` | GET | `/offices` | Bearer | no | — (Fineract pass-through) |
| `create_group_orchestrate` | POST | `/companion/groups` | Bearer | yes | COMP-GRP-001 |

## Request / Response Details

### GET /offices

**Response**

| Field | Type | Description |
|---|---|---|
| id | String | Fineract office ID |
| name | String | Office display name |
| nameDecorated | String? | Hierarchical decorated name |

**Cache:** TTL 3600 s, stale-while-revalidate.

---

### POST /companion/groups (COMP-GRP-001 — create orchestration)

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| groupName | String | yes | Display name |
| officeId | String | yes | Fineract office |
| currency | String | yes | ISO currency code (default KES) |
| meetingDay | String | yes | Day of week |
| meetingTime | String | yes | HH:MM format |
| typeConfig | GroupTypeConfig | yes | Full config from group-type-picker nav arg |

**GroupTypeConfig fields in request:**

| Field | Type | Description |
|---|---|---|
| group_type | String | typeSlug (e.g. "vsla") |
| pool_model | String | ACCUMULATING \| ROTATING_PAYOUT \| NONE |
| contribution_model | String | SHARE_BASED_VARIABLE \| FIXED_AMOUNT \| FIXED_NEGOTIATED |
| shareout_formula | String | PRORATA_SHARES \| PRORATA_SAVINGS \| EQUAL \| FIXED_ORDER \| LOTTERY \| AUCTION |
| payout_order_method | String? | FIXED_ORDER \| LOTTERY \| AUCTION (ROTATING_PAYOUT only) |
| share_value | Long? | KES per share (SHARE_BASED_VARIABLE) |
| contribution_amount | Long? | KES per meeting (FIXED_AMOUNT) |
| social_fund_enabled | Boolean | |
| social_fund_percent | Double? | |
| cycle_length_months | Int | |
| loan_multiplier | Double? | |
| interest_rate | Double? | |
| fine_amount | Long? | |
| max_members | Int | |

**Response**

| Field | Type | Description |
|---|---|---|
| groupId | String | Companion group ID |
| inviteCode | String | Auto-generated first invite code |

**Server orchestration steps (atomic in companion):**
1. `POST /fineract/groups` — creates Fineract group
2. `POST /fineract/groups/{id}?command=activate` — activates group
3. `POST /fineract/groups/{id}/groupmembers` — associates creator
4. `POST /companion/datatables/dt_member_role/{groupId}` — assigns ORGANIZER role
5. `POST /companion/datatables/dt_group_type_config/{groupId}` — provisions group config

**Errors**

| Code | Meaning |
|---|---|
| 400 | Validation error (missing name, invalid currency) |
| 401 | Unauthorized |
| 403 | Not authorised to create groups in this office |
| 409 | Group name already taken in this office |
| 503 | Fineract unavailable — companion falls back to sync queue |

---

## DTOs

### CreateGroupOrchestrationRequest
```
groupName: String
officeId: String
currency: String
meetingDay: String
meetingTime: String
typeConfig: GroupTypeConfig
```

### GroupTypeConfig (in request + cached locally)
```
group_type: String
pool_model: String
contribution_model: String
shareout_formula: String
payout_order_method: String?
share_value: Long?
contribution_amount: Long?
social_fund_enabled: Boolean
social_fund_percent: Double?
cycle_length_months: Int
loan_multiplier: Double?
interest_rate: Double?
fine_amount: Long?
max_members: Int
```

### CreateGroupOrchestrationResponse
```
groupId: String
inviteCode: String
```

### Office
```
id: String
name: String
nameDecorated: String?
```

## Offline Behaviour

When offline, the full `CreateGroupOrchestrationRequest` is serialized and written to the
`sync_queue` table with:
- `entity_type: CREATE_GROUP_ORCHESTRATE`
- `priority: NORMAL`
- `idempotency_key: "name:{name}:officeId:{officeId}:userId:{userId}"`

The companion API enforces 409 on duplicate execution if the sync drains multiple times.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `400 Validation` | Show field-level `validationErrors` |
| `409 Conflict` | "Group name already taken" inline error on name field |
| `network.offline` | Enqueue to sync_queue + `ShowOfflineSyncDialog` |
| `401 Unauthorized` | Navigate to `login-signup` |
| `500/503 Server` | Show retry banner |
