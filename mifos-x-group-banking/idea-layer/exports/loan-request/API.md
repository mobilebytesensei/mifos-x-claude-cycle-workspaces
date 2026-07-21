<!--
  generated_from_feature: loan-request
  contract_version: "2.0.0"
  source: idea-layer/screens/loan-request/api.yaml
  generated_by: /idea-feature-export-spec
-->

# Loan Request — API Contract

## Endpoints (1)

| ID | Function | Method | Endpoint | Auth | Writable |
|---|---|---|---|---|---|
| `submit_loan_request` | submit_loan_request | POST | `/datatables/dt_loan_request` | Basic (self-service) | yes |

Base path: `/fineract-provider/api/v1` · Tenant header: `X-Fineract-Platform-TenantId: default`.
Offline-capable — falls back to `SyncQueue` when no connectivity.

## Request / Response Details

### POST /datatables/dt_loan_request

**Params**

| Param | Type | Source |
|---|---|---|
| clientId | Long | nav_params |
| requestedAmount | Double | user_input |
| purpose | String | user_input |
| durationWeeks | Int | user_input |
| savingsBalance | Double | session |
| submittedAt | String | system (ISO-8601) |

**Request body**

| Field | Type | Notes |
|---|---|---|
| clientId | Long | |
| requested_amount | Double | |
| purpose | String | |
| duration_weeks | Int | |
| savings_balance_at_request | Double | |
| submitted_at | String | |
| status | String | default `PENDING` |

**Response**

| Field | Type |
|---|---|
| resourceId | Long |
| officeId | Long |
| clientId | Long |
| resourceExternalId | String |

**Errors**

| Code | Meaning |
|---|---|
| 400 | Validation error — field missing or invalid |
| 401 | Session expired |
| 409 | Duplicate loan request pending |
| 503 | Server unavailable — queue for sync |

**Cache:** `ttl: 0`, `no-cache`, offline `queue_to_syncqueue`.

## DTOs

### LoanRequestPayload
```
clientId: Long
requested_amount: Double
purpose: String
duration_weeks: Int
savings_balance_at_request: Double
submitted_at: String
status: String   # PENDING
```

### LoanRequestResponse
```
resourceId: Long
officeId: Long
clientId: Long
resourceExternalId: String
```

### SyncQueueEntry
```
id: Long
entityType: String
payload: String
status: String
createdAt: String
retryCount: Int
```

### LoanPurpose (dropdown values)
```
SCHOOL_FEES | MEDICAL | BUSINESS | FARMING | HOME_IMPROVEMENT | EMERGENCY | OTHER
```

## Dependencies

- Services: `LoanRequestRepository`, `SyncQueueRepository`, `SessionManager`, `ConnectivityManager`
- Shared entities: `Loan`, `SyncQueue`, `Member`
- Parent feature: `end-user-dashboard`

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `Validation` (400) | `SubmitError.Validation` (error_validation), no retry |
| `network.offline` / 503 | `SubmitError.Network`; enqueue to SyncQueue (error_network_queued); OfflineQueued state |
| `409 Duplicate` | Duplicate loan request pending — surfaced as submit error |
| `401 Unauthorized` | `SubmitError.Unauthorized` (error_session_expired) → redirect login |
| `500 Server` | `SubmitError.Server` (retry); error snackbar with Retry |

## Offline Behaviour

When `ConnectivityManager` / `cmp-network-monitor` reports offline, the `LoanRequestPayload` is
serialized and written to the `SyncQueue` (SQLDelight) as a `SyncQueueEntry`; a background worker
drains it when connectivity returns. The screen shows the offline banner and the offline success
copy, and navigates to `personal-dashboard`. The `dt_loan_request` row lands `PENDING` for
organizer review at the next meeting.

> Source note: `tests.yaml` TC-LRQ-003 references a companion path
> `POST /companion/groups/{groupId}/loans` (COMP-GRP-001); the endpoint SoT here is `api.yaml`'s
> `dt_loan_request` datatable POST. Reconcile the test wording with `api.yaml`.
