<!--
  generated_from_feature: loan-detail
  contract_version: "2.0.0"
  source: idea-layer/screens/loan-detail/api.yaml
  generated_by: /idea-feature-export-spec
-->

# Loan Detail — API Contract

## Endpoints (1)

| ID | Function | Method | Endpoint | Auth | Writable |
|---|---|---|---|---|---|
| `get_loan_detail` | get_loan | GET | `/loans/{loanId}` | Basic | no |

Base path: `/fineract-provider/api/v1` · Tenant header: `X-Fineract-Platform-TenantId: default`.
The `recordRepayment` and `markDefaulted` write paths are owned by the repayment /
mark-defaulted dialog features.

## Request / Response Details

### GET /loans/{loanId}

**Params:** `loanId: Long (required, nav_params)`,
`associations: String (default "repaymentSchedule,transactions")`.

**Response**

| Field | Type | Description |
|---|---|---|
| id | Long | Fineract loan id |
| clientId | Long | Borrower client id |
| clientName | String | Member name |
| loanProductName | String | Product name |
| principal | Double | Principal amount |
| approvedPrincipal | Double | Approved principal |
| disbursementDate | List<Int> | Fineract date array |
| interestRatePerPeriod | Double | Interest per period |
| interestType | {id, value} | Interest type |
| status | {id, value} | Loan status |
| summary | object | principalDisbursed/Paid/Outstanding, interestCharged/Paid/Outstanding, totalExpectedRepayment, totalOutstanding, totalOverdue |
| repaymentSchedule.periods[] | array | period, dueDate, principalDue, interestDue, totalInstallmentAmountForPeriod, totalPaidForPeriod, totalOutstandingForPeriod, complete |
| transactions[] | array | id, type{id,value}, date, amount |

**Errors:** 401 Unauthorized · 404 Loan not found · 500 Server error.

**Cache:** TTL 120 s, stale-while-revalidate, offline `show_cached`.

## DTOs

### LoanDetail
```
id: Long
memberId: Long
memberName: String
loanProductName: String
principalAmount: Double (KES)
disbursedDate: String
interestRatePercent: Double
totalOutstanding: Double (KES)
totalOverdue: Double (KES)
status: LoanStatus
fineractLoanId: Long
```

### RepaymentScheduleRow
```
weekNumber: Int
dueDate: String
dueAmount: Double (KES)
paidAmount: Double (KES)
balance: Double (KES)
status: RepaymentRowStatus
```

### RepaymentRowStatus (enum)
```
PAID | PARTIAL | UPCOMING | OVERDUE
```

### RepaymentTransaction
```
id: Long
type: String
date: String
amount: Double (KES)
```

### LoanDetailTab (enum)
```
SCHEDULE | HISTORY
```

## Repository Contract

`LoanRepository`:
- `getLoanDetail(loanId: Long): Flow<LoanDetail>`
- `recordRepayment(loanId: Long, amount: Double, date: String): Flow<Unit>`
- `markDefaulted(loanId: Long): Flow<Unit>`

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `404 NotFound` | `LoanDetailError.NotFound` (no retry) |
| `401 Unauthorized` | `LoanDetailError.Auth` → redirect login |
| `network.offline` | `LoanDetailError.Network` (retry); serve cached (stale-while-revalidate) |
| `500 Server` | `LoanDetailError.Server` (retry); error_state retry CTA |

## Offline Behaviour

Stale-while-revalidate (TTL 120 s): cached `LoanDetail` + schedule + history are served
immediately via `cmp-network-monitor` fallback; a background refresh reconciles from Fineract
and re-caches (`loans`, `loan_repayments`) via Store5.
