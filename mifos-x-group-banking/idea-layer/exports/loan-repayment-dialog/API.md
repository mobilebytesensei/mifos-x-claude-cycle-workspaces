<!--
  generated_from_feature: loan-repayment-dialog
  contract_version: "2.0.0"
  source: idea-layer/screens/loan-repayment-dialog/api.yaml
  generated_by: /idea-feature-export-spec
-->

# Loan Repayment Dialog — API Contract

## Endpoints (1)

| ID | Function | Method | Endpoint | Auth | Writable |
|---|---|---|---|---|---|
| `make_repayment` | make_repayment | POST | `/loans/{loanId}/transactions?command=repayment` | Basic | yes |

Base path: `/fineract-provider/api/v1` · Tenant header: `X-Fineract-Platform-TenantId: default`.
Idempotent money move — a retry after a timeout must not double-post.

## Request / Response Details

### POST /loans/{loanId}/transactions?command=repayment

**Params:** `loanId: Long (required, nav_params)`.

**Body**

| Field | Type | Source | Notes |
|---|---|---|---|
| transactionDate | String | system | Today's date, `dd MMMM yyyy` |
| transactionAmount | Double | state.amount | Repayment amount (KES) |
| paymentTypeId | Int | resolved from paymentMethod | MPESA=1, CASH=2 |
| receiptNumber | String? | state.referenceNumber | Optional M-Pesa receipt code |
| locale | String | default `en` | |
| dateFormat | String | default `dd MMMM yyyy` | |

**Response**

| Field | Type |
|---|---|
| officeId | Int |
| clientId | Long |
| loanId | Long |
| resourceId | Long |

**Errors**

| Code | Meaning |
|---|---|
| 400 | Validation error (amount exceeds outstanding) |
| 401 | Unauthorized |
| 403 | Forbidden (role check) |
| 404 | Loan not found |
| 500 | Server error |

## DTOs

### PaymentMethod (enum)
```
MPESA  -> label "M-Pesa"  -> paymentTypeId 1
CASH   -> label "Cash"    -> paymentTypeId 2
```

## Repository Contract

`LoanRepository`:
- `recordRepayment(loanId: Long, memberId: Long, amount: Double, paymentMethod: String, referenceNumber: String?): Flow<Unit>`

Services: `InputValidator` (amount positive + within outstanding).

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `Validation` (amount) | Inline `amountError` (error_amount_required / invalid / exceeds); submit disabled |
| `network.offline` | Submit blocked by cmp-network-monitor |
| `400 Validation` | Amount exceeds outstanding — submitError shown |
| `401 Unauthorized` | Session expired |
| `403 Forbidden` | Role check failed |
| `500 Server` | error_server — submitError set; dialog stays open for retry |

## Offline Behaviour

`cmp-network-monitor` blocks submission when offline. The repayment carries an idempotent
external/receipt identifier so a retry after a network timeout never double-posts. On success the
Store5/SQLDelight loan cache is refreshed so the parent `loan-detail` schedule/balance update.
