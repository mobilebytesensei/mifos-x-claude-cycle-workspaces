<!--
  generated_from_feature: loan-mark-defaulted-dialog
  contract_version: "2.0.0"
  source: idea-layer/screens/loan-mark-defaulted-dialog/api.yaml
  generated_by: /idea-feature-export-spec
-->

# Mark Loan Defaulted Dialog — API Contract

## Endpoints (1)

| ID | Function | Method | Endpoint | Auth | Writable |
|---|---|---|---|---|---|
| `mark_loan_defaulted` | write_off_loan | POST | `/loans/{loanId}/transactions?command=writeoff` | Basic | yes |

Base path: `/fineract-provider/api/v1` · Tenant header: `X-Fineract-Platform-TenantId: default`.
Irreversible write-off of the `m_loan` record. No offline queue — connectivity is required.

## Request / Response Details

### POST /loans/{loanId}/transactions?command=writeoff

**Params:** `loanId: Long (required, nav_params)`.

**Body**

| Field | Type | Notes |
|---|---|---|
| transactionDate | String | Today's date, `dd MMMM yyyy` |
| locale | String | default `en` |
| dateFormat | String | default `dd MMMM yyyy` |

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
| 401 | Unauthorized |
| 403 | Forbidden (chairperson role required) |
| 404 | Loan not found |
| 409 | Loan is not in an eligible state for write-off |
| 500 | Server error |

## Repository Contract

`LoanRepository`:
- `markDefaulted(loanId: Long): Flow<Unit>`

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `network.offline` | Submit blocked (no queue); offline warning; isSubmitting stays false |
| `403 Forbidden` | error_forbidden — "You do not have permission" |
| `409 Ineligible` | error_ineligible — "This loan cannot be defaulted in its current state" |
| `401 Unauthorized` | Session expired |
| `500 Server` | error_server — submitError set; dialog stays open for retry |

## Offline Behaviour

None. This is a destructive, irreversible action; `cmp-network-monitor` blocks submission when
offline rather than queuing. On success the Store5/SQLDelight loan cache is refreshed so the
parent `loan-detail` badge and action gating update.
