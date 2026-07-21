<!--
  generated_from_feature: loan-list
  contract_version: "2.0.0"
  source: idea-layer/screens/loan-list/api.yaml
  generated_by: /idea-feature-export-spec
-->

# Loan List — API Contract

## Endpoints (1)

| ID | Function | Method | Endpoint | Auth | Writable |
|---|---|---|---|---|---|
| `get_group_loans` | get_group_loans | GET | `/groups/{groupId}/loans` | Basic | no |

Base path: `/fineract-provider/api/v1` · Tenant header: `X-Fineract-Platform-TenantId: default`.

## Request / Response Details

### GET /groups/{groupId}/loans

**Params**

| Param | Type | Notes |
|---|---|---|
| groupId | Long | required, nav_params |
| limit | Int | default 20 |
| offset | Int | default 0 |
| loanStatus | String | optional — active\|overdue\|closed\|all |

**Response**

| Field | Type | Description |
|---|---|---|
| totalFilteredRecords | Int | Total matching records |
| pageItems[] | array | Loan rows (see below) |

`pageItems[]` item: `{ id: Long, clientId: Long, clientName: String, loanProductName: String,
principal: Double (KES), summary{ principalOutstanding: Double, totalOverdue: Double },
status{ id, value }, timeline{ expectedDisbursementDate: List<Int>,
actualDisbursementDate: List<Int> }, nextRepaymentDate: List<Int> }`.

**Errors:** 401 Unauthorized (→ login) · 403 Forbidden (insufficient permissions) ·
404 Group not found · 500 Server error (→ retry).

**Cache:** TTL 180 s, stale-while-revalidate, offline `show_cached`.
**Pagination:** offset-based, page size 20.

## DTOs

### LoanSummary
```
id: Long
memberId: Long
memberName: String
memberPhotoUrl: String?
loanProductName: String
principalAmount: Double (KES)
outstandingBalance: Double (KES)
overdueAmount: Double (KES)
status: LoanStatus
nextRepaymentDate: String?
isOverdue: Boolean
fineractLoanId: Long
```

### LoanStatus (enum)
```
ACTIVE | OVERDUE | CLOSED | PENDING | REJECTED
```

### LoanStatusFilter (enum)
```
ALL | ACTIVE | OVERDUE | CLOSED
```

## Repository Contract

`LoanRepository`:
- `getGroupLoans(groupId: Long, limit: Int, offset: Int): Flow<List<LoanSummary>>`
- `getLoansByStatus(groupId: Long, status: LoanStatusFilter): Flow<List<LoanSummary>>`

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `401 Unauthorized` | `LoanListError.Auth` → redirect login-signup |
| `403 Forbidden` | Insufficient-permissions error; Error state |
| `404 NotFound` | Empty state (error_group_not_found) |
| `network.offline` | `LoanListError.Network` (retry); serve cached (stale-while-revalidate) |
| `500 Server` | `LoanListError.Server` (retry); error_state retry CTA |

## Offline Behaviour

Store5 stream reads the `loans` SQLDelight cache first (TTL 180 s stale-while-revalidate); when
offline, `cmp-network-monitor` serves cached `LoanSummary` rows so Content is reachable. Filter
changes and paging operate on the in-memory list without a network call; next-page loads upsert
new rows atomically (replacePage).
