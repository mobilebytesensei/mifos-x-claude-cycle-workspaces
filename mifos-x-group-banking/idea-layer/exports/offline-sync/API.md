# Offline Sync — API Reference
**Feature**: offline-sync | **Requirement**: FR-008
**Backend**: Mifos Fineract Batch API + SQLDelight local database

---

## Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /fineract-provider/api/v1/batches | Submit all pending SyncQueue items to Fineract in a single batch request | BasicAuth |

All other data reads (queue items, settings, sync timestamps) are sourced exclusively from the local SQLDelight database — no network call on screen load.

---

## Request / Response Details

### POST /batches — Batch Sync

**Trigger**: User taps "Sync Now" or SyncManager background job fires on connectivity restore.

**Request Body (BatchRequest)**:
```json
{
  "requests": [
    {
      "requestId": 1,
      "relativeUrl": "savingsaccounts/501/transactions",
      "method": "POST",
      "headers": { "Content-Type": "application/json" },
      "body": {
        "transactionDate": "06 May 2026",
        "transactionAmount": 200.0,
        "paymentTypeId": 1,
        "note": "Meeting #4 savings collection — Mary Akinyi",
        "locale": "en",
        "dateFormat": "dd MMMM yyyy"
      }
    },
    {
      "requestId": 2,
      "relativeUrl": "savingsaccounts/502/transactions",
      "method": "POST",
      "headers": { "Content-Type": "application/json" },
      "body": {
        "transactionDate": "06 May 2026",
        "transactionAmount": 300.0,
        "paymentTypeId": 1,
        "note": "Meeting #4 savings collection — John Mwangi",
        "locale": "en",
        "dateFormat": "dd MMMM yyyy"
      }
    },
    {
      "requestId": 3,
      "relativeUrl": "datatables/dt_meeting_record/7",
      "method": "POST",
      "headers": { "Content-Type": "application/json" },
      "body": {
        "meeting_number": 4,
        "meeting_date": "06 May 2026",
        "opening_corpus": 12400.0,
        "closing_corpus": 12950.0,
        "total_savings_collected": 1050.0,
        "total_fines_collected": 50.0,
        "total_repayments_collected": 0.0,
        "status": "completed",
        "locale": "en",
        "dateFormat": "dd MMMM yyyy"
      }
    }
  ]
}
```

**Response (BatchResponse)**:
```json
{
  "responses": [
    {
      "requestId": 1,
      "statusCode": 200,
      "body": {
        "officeId": 1,
        "savingsId": 501,
        "resourceId": 9101
      }
    },
    {
      "requestId": 2,
      "statusCode": 200,
      "body": {
        "officeId": 1,
        "savingsId": 502,
        "resourceId": 9102
      }
    },
    {
      "requestId": 3,
      "statusCode": 200,
      "body": {
        "resourceId": 4,
        "resourceIdentifier": "dt_meeting_record_4"
      }
    }
  ]
}
```

**Partial Failure Response** (some succeed, some fail):
```json
{
  "responses": [
    {
      "requestId": 1,
      "statusCode": 200,
      "body": { "resourceId": 9101 }
    },
    {
      "requestId": 2,
      "statusCode": 400,
      "body": {
        "defaultUserMessage": "The savings account balance cannot go below the minimum balance requirement.",
        "developerMessage": "Account 502 minimum balance constraint violated"
      }
    },
    {
      "requestId": 3,
      "statusCode": 200,
      "body": { "resourceId": 4 }
    }
  ]
}
```

**HTTP Errors**:
- 401: Authentication expired — refresh credentials, re-attempt
- 403: Forbidden — mark all items in batch as FAILED
- 500: Server error — retain items as PENDING, increment retry_count
- Network timeout (no response): retain items as PENDING

---

## SyncQueue Processing Logic

### Batch Construction
1. Read all `SyncQueueItem` records from SQLDelight where `status = 'pending'`
2. Group by `entity_type` for ordering: MEETING → SAVINGS → ATTENDANCE → LOAN → SHARE_OUT → MEMBER
3. Convert each item's `payload_json` to a BatchSubRequest using `relativeUrl` derived from entity type + operation
4. Mark all selected items `status = 'in_progress'` in SQLDelight before posting

### Entity Type → Relative URL Mapping

| EntityType | Operation | Relative URL Pattern |
|------------|-----------|----------------------|
| MEETING | CREATE | `datatables/dt_meeting_record/{centerId}` |
| MEETING | UPDATE | `datatables/dt_meeting_record/{centerId}/{rowId}` |
| ATTENDANCE | CREATE | `datatables/dt_meeting_attendance/{clientId}` |
| SAVINGS | CREATE | `savingsaccounts/{savingsAccountId}/transactions` |
| LOAN | CREATE | `loans` |
| LOAN | UPDATE | `loans/{loanId}` |
| SHARE_OUT | CREATE | `datatables/dt_share_out/{centerId}` |
| MEMBER | CREATE | `clients` |
| MEMBER | UPDATE | `clients/{clientId}` |

### Post-Batch Response Processing
- For each `BatchSubResponse` with `statusCode` 200 or 201: update corresponding SQLDelight row `status = 'synced'`
- For each `BatchSubResponse` with `statusCode` 4xx: update row `status = 'failed'`, write `error_message` from response body `defaultUserMessage`
- For each `BatchSubResponse` with `statusCode` 5xx: retain `status = 'pending'`, write `error_message`, update `retried_at`
- After processing: write `last_synced_at` to `app_settings` table with current UTC timestamp
- Emit `SyncCompleted` event; update `overallStatus` in ViewModel

---

## SQLDelight Database (Local — No Network)

### sync_queue table operations

**Read all pending items** (ViewModel load + Sync Now trigger):
```sql
SELECT * FROM sync_queue WHERE status = 'pending' ORDER BY created_at ASC;
```

**Read all failed items** (SyncStatusScreen display):
```sql
SELECT * FROM sync_queue WHERE status = 'failed' ORDER BY retried_at DESC;
```

**Read pending count by entity type** (pendingByType map):
```sql
SELECT entity_type, COUNT(*) as count FROM sync_queue
WHERE status = 'pending'
GROUP BY entity_type;
```

**Mark items in-progress before batch POST**:
```sql
UPDATE sync_queue SET status = 'in_progress' WHERE id IN (?, ?, ?);
```

**Mark item synced after successful batch response**:
```sql
UPDATE sync_queue SET status = 'synced' WHERE id = ?;
```

**Mark item failed with error message**:
```sql
UPDATE sync_queue SET status = 'failed', error_message = ?, retried_at = ? WHERE id = ?;
```

**Retry a specific failed item** (OnRetryOperation action):
```sql
UPDATE sync_queue SET status = 'pending', error_message = NULL WHERE id = ?;
```

**Count conflicts** (items with conflicting entity_type + operation combinations):
```sql
SELECT COUNT(*) FROM sync_queue
WHERE status = 'pending'
AND entity_type || '_' || operation IN (
  SELECT entity_type || '_' || operation FROM sync_queue
  WHERE status = 'failed'
);
```

### app_settings table operations

**Read last sync timestamp**:
```sql
SELECT value FROM app_settings WHERE key = 'last_synced_at';
```

**Write last sync timestamp** (after successful batch):
```sql
INSERT OR REPLACE INTO app_settings (key, value, last_synced_at)
VALUES ('last_synced_at', '2026-05-05T08:30:00Z', '2026-05-05T08:30:00Z');
```

---

## DTOs

### SyncQueueItem
| Field | Type | Description |
|-------|------|-------------|
| id | Long | Auto-increment primary key |
| entityType | EntityType | MEETING, LOAN, SAVINGS, ATTENDANCE, SHARE_OUT, MEMBER |
| operation | SyncOperation | CREATE, UPDATE, DELETE |
| payloadJson | String | Serialized request body for Fineract |
| status | SyncStatus | pending, in_progress, synced, failed |
| createdAt | Instant | When the local write was queued |
| retriedAt | Instant? | Last retry attempt timestamp |
| errorMessage | String? | Last Fineract error if status=failed |

### EntityType (enum)
| Value | Fineract Target |
|-------|----------------|
| MEETING | dt_meeting_record datatable |
| SAVINGS | savingsaccounts transactions |
| LOAN | loans |
| ATTENDANCE | dt_meeting_attendance datatable |
| SHARE_OUT | dt_share_out datatable |
| MEMBER | clients |

### SyncOperation (enum)
| Value | HTTP Method |
|-------|-------------|
| CREATE | POST |
| UPDATE | PUT |
| DELETE | DELETE |

### SyncStatus (enum)
| Value | Description |
|-------|-------------|
| pending | Awaiting network — will be included in next batch |
| in_progress | Included in an active batch POST (transient) |
| synced | Successfully committed to Fineract |
| failed | Last batch attempt returned 4xx error |

### SyncOverallStatus (enum)
| Value | Condition | Color |
|-------|-----------|-------|
| SYNCED | pendingCount == 0 && failedCount == 0 | #C8E6C9 background, primary #2E7D32 text |
| PENDING | pendingCount > 0 | #FFF9C4 background, #E65100 text |
| FAILED | failedCount > 0 | #FFCDD2 background, error #D32F2F text |

### BatchSubRequest
| Field | Type | Description |
|-------|------|-------------|
| requestId | Int | Sequential ID matching SyncQueueItem.id |
| relativeUrl | String | Fineract relative endpoint path |
| method | String | POST, PUT, or DELETE |
| headers | Map<String, String> | Content-Type: application/json |
| body | JsonObject | Deserialized from SyncQueueItem.payloadJson |

### BatchSubResponse
| Field | Type | Description |
|-------|------|-------------|
| requestId | Int | Matches the corresponding BatchSubRequest |
| statusCode | Int | HTTP status (200, 201, 400, 403, 500, etc.) |
| body | JsonObject | Fineract response or error body |

### SyncSummary (computed in ViewModel)
| Field | Type | Source |
|-------|------|--------|
| pendingCount | Int | COUNT(*) WHERE status='pending' |
| failedCount | Int | COUNT(*) WHERE status='failed' |
| conflictCount | Int | Overlapping pending+failed entity/operation pairs |
| lastSyncAt | Instant? | app_settings WHERE key='last_synced_at' |
| pendingByType | Map<EntityType, Int> | GROUP BY entity_type WHERE status='pending' |
| failedOperations | List<SyncQueueItem> | WHERE status='failed' ORDER BY retried_at DESC |
| overallStatus | SyncOverallStatus | Derived from pendingCount + failedCount |

---

## Demo State (sync-status screen — from SQLDelight)

**Current demo sync_queue contents**:

| id | entity_type | operation | status | created_at | error_message |
|----|------------|-----------|--------|-----------|---------------|
| 1 | MEETING | CREATE | pending | 2026-05-06T10:15:00Z | null |
| 2 | SAVINGS | CREATE | pending | 2026-05-06T10:15:01Z | null |
| 3 | SAVINGS | CREATE | pending | 2026-05-06T10:15:02Z | null |

**Resulting ViewModel state**:
- `isOnline`: true
- `overallStatus`: PENDING
- `pendingCount`: 3
- `failedCount`: 0
- `conflictCount`: 0
- `pendingByType`: { MEETING: 1, SAVINGS: 2 }
- `lastSyncAt`: 2026-05-05T08:30:00Z
- `failedOperations`: []
- `isSyncing`: false
