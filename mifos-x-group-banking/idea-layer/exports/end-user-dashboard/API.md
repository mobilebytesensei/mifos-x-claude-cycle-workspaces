# End-User Dashboard — API Contract

## Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /self/clients/{clientId}/accounts | Get all savings + loan accounts for authenticated self-service client | selfServiceToken (Basic base64) |
| GET | /self/savingsaccounts/{savingsId} | Get detailed savings account with balance and summary | selfServiceToken |
| GET | /self/savingsaccounts/{savingsId}/transactions | Get transaction history for a savings account | selfServiceToken |
| GET | /self/loans | Get all loans for authenticated self-service client including repayment schedule | selfServiceToken |
| POST | /datatables/dt_loan_request | Submit a loan application datatable entry for admin review | selfServiceToken |

All self-service endpoints use `Authorization: Basic {base64EncodedAuthenticationKey}` header from the SelfAuthResponse token stored at login.

---

## Request / Response Details

### get_client_accounts

**Request**:

| Parameter | Type | Required | Source |
|-----------|------|----------|--------|
| clientId | Long (path) | Yes | nav_params.clientId |

```
GET /self/clients/2081/accounts
Authorization: Basic Z3JhY2UubXdhbmdpOm15c2VjcmV0
```

**Response**:

| Field | Type | Description |
|-------|------|-------------|
| savingsAccounts | List\<SavingsAccountSummaryDto\> | All savings accounts for the client |
| loanAccounts | List\<LoanAccountSummaryDto\> | All loan accounts for the client |

**savingsAccounts items**:

| Field | Type |
|-------|------|
| id | Long |
| accountNo | String |
| savingsProductId | Long |
| savingsProductName | String |
| balance | Double |
| status | AccountStatusDto |

**loanAccounts items**:

| Field | Type |
|-------|------|
| id | Long |
| accountNo | String |
| loanProductId | Long |
| loanProductName | String |
| loanBalance | Double |
| status | AccountStatusDto |

**Errors**:

| Code | Meaning | Action |
|------|---------|--------|
| 401 | Session expired | Navigate to login; clear session |
| 404 | Client not found | Show error state |
| 503 | Server unavailable | Use SQLDelight cache |

**Cache**: TTL 300s, stale-while-revalidate. Offline: serve from SQLDelight.

---

### get_savings_account

**Request**:

| Parameter | Type | Required | Source |
|-----------|------|----------|--------|
| savingsId | Long (path) | Yes | from get_client_accounts response |

```
GET /self/savingsaccounts/30042
Authorization: Basic Z3JhY2UubXdhbmdpOm15c2VjcmV0
```

**Response**:

| Field | Type | Description |
|-------|------|-------------|
| id | Long | Account ID |
| accountNo | String | Display account number |
| savingsProductName | String | Product display name |
| currency.code | String | "KES" |
| currency.displaySymbol | String | "KES" |
| summary.totalDeposits | Double | Cumulative deposits |
| summary.totalWithdrawals | Double | Cumulative withdrawals |
| summary.accountBalance | Double | Current balance |
| summary.availableBalance | Double | Available for withdrawal |
| status.active | Boolean | Account active? |

**Errors**:

| Code | Meaning | Action |
|------|---------|--------|
| 401 | Session expired | Navigate to login |
| 404 | Account not found | Show error |
| 503 | Server unavailable | Use cache |

**Cache**: TTL 300s, stale-while-revalidate.

---

### get_group_linked_transactions / get_individual_transactions

Both endpoints share identical schema. The path parameter `savingsId` differs.

**Request**:

| Parameter | Type | Required | Default | Source |
|-----------|------|----------|---------|--------|
| savingsId | Long (path) | Yes | — | nav_params |
| limit | Int (query) | No | 50 | hardcoded |
| offset | Int (query) | No | 0 | pagination |

```
GET /self/savingsaccounts/30042/transactions?limit=50&offset=0
Authorization: Basic Z3JhY2UubXdhbmdpOm15c2VjcmV0
```

**Response** (array of SavingsTransactionDto):

| Field | Type | Description |
|-------|------|-------------|
| id | Long | Transaction ID |
| transactionType.value | Int | Type code |
| transactionType.code | String | e.g. "savingsAccountTransactionType.deposit" |
| transactionType.description | String | Human-readable |
| date | List\<Int\> | [YYYY, MM, DD] |
| amount | Double | Transaction amount in KES |
| runningBalance | Double | Balance after transaction |
| currency.code | String | "KES" |
| currency.displaySymbol | String | "KES" |

**Errors**:

| Code | Meaning | Action |
|------|---------|--------|
| 401 | Session expired | Navigate to login |
| 404 | Account not found | Show error |
| 503 | Server unavailable | Use SQLDelight cache |

**Cache**: TTL 300s, stale-while-revalidate.

---

### get_self_loans

**Request**:

| Parameter | Type | Required | Default | Source |
|-----------|------|----------|---------|--------|
| associations | String (query) | No | "repaymentSchedule" | hardcoded |

```
GET /self/loans?associations=repaymentSchedule
Authorization: Basic Z3JhY2UubXdhbmdpOm15c2VjcmV0
```

**Response** (array of LoanDto):

| Field | Type | Description |
|-------|------|-------------|
| id | Long | Loan ID |
| accountNo | String | Display account number |
| productName | String | Loan product name |
| loanProductId | Long | Product ID |
| status.id | Int | Status code |
| status.code | String | e.g. "loanStatusType.active" |
| status.value | String | "Active" |
| status.active | Boolean | Is loan currently active? |
| status.closed | Boolean | Is loan closed? |
| principal | Double | Original loan principal |
| interestRatePerPeriod | Double | Interest rate (group-set) |
| termFrequency | Int | Number of periods |
| repaymentSchedule.totalPrincipalExpected | Double | Total principal |
| repaymentSchedule.totalInterestCharged | Double | Total interest |
| repaymentSchedule.totalRepaymentExpected | Double | Grand total |
| repaymentSchedule.periods | List\<RepaymentPeriodDto\> | Per-period schedule |
| summary.principalDisbursed | Double | Disbursed amount |
| summary.principalOutstanding | Double | Remaining principal |
| summary.totalOutstanding | Double | Total remaining |
| summary.totalRepayment | Double | Total paid so far |

**RepaymentPeriodDto fields**:

| Field | Type | Description |
|-------|------|-------------|
| period | Int | Period number (1, 2, 3…) |
| dueDate | List\<Int\> | [YYYY, MM, DD] |
| principalDue | Double | Principal portion due this period |
| interestDue | Double | Interest portion due this period |
| totalDueForPeriod | Double | Total due (principal + interest) |
| totalPaidForPeriod | Double | Amount paid for this period |
| complete | Boolean | Period fully paid? |

**Errors**:

| Code | Meaning | Action |
|------|---------|--------|
| 401 | Session expired | Navigate to login |
| 503 | Server unavailable | Use SQLDelight cache |

**Cache**: TTL 180s, stale-while-revalidate.

---

### submit_loan_request

**Request**:

| Parameter | Type | Required | Source |
|-----------|------|----------|--------|
| clientId | Long | Yes | nav_params |
| requested_amount | Double | Yes | user_input |
| purpose | String | Yes | user_input |
| duration_weeks | Int | Yes | user_input |
| savings_balance_at_request | Double | Yes | session |
| submitted_at | String | Yes | system (ISO-8601) |
| status | String | Yes | hardcoded "PENDING" |

```
POST /datatables/dt_loan_request
Authorization: Basic Z3JhY2UubXdhbmdpOm15c2VjcmV0
Content-Type: application/json

{
  "clientId": 2081,
  "requested_amount": 15000.0,
  "purpose": "SCHOOL_FEES",
  "duration_weeks": 12,
  "savings_balance_at_request": 12450.0,
  "submitted_at": "2026-05-06T09:30:00Z",
  "status": "PENDING"
}
```

**Response**:

| Field | Type | Description |
|-------|------|-------------|
| resourceId | Long | Created datatable entry ID |
| officeId | Long | Office ID |
| clientId | Long | Client ID (confirmed) |
| resourceExternalId | String | External reference ID |

**Errors**:

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Validation error — missing or invalid field | Show inline field errors |
| 401 | Session expired | Navigate to login |
| 409 | Duplicate request pending | Show "You already have a pending loan request" message |
| 503 | Server unavailable | Queue to SyncQueue; show offline success dialog |

**Cache**: no-cache. Offline fallback: queue_to_syncqueue.

**Offline behaviour**: When ConnectivityManager.isOnline() = false, the LoanRequestPayload is serialised to JSON and stored as a SyncQueueEntry with entityType="dt_loan_request", status="PENDING". The SyncQueue worker retries when connectivity is restored.

---

## DTOs

### ClientAccountsResponse

| Field | Type |
|-------|------|
| savingsAccounts | List\<SavingsAccountSummaryDto\> |
| loanAccounts | List\<LoanAccountSummaryDto\> |

### SavingsAccountSummaryDto

| Field | Type |
|-------|------|
| id | Long |
| accountNo | String |
| savingsProductId | Long |
| savingsProductName | String |
| balance | Double |
| status | AccountStatusDto |

### LoanAccountSummaryDto

| Field | Type |
|-------|------|
| id | Long |
| accountNo | String |
| loanProductId | Long |
| loanProductName | String |
| loanBalance | Double |
| status | AccountStatusDto |

### SavingsAccountDetailDto

| Field | Type |
|-------|------|
| id | Long |
| accountNo | String |
| savingsProductName | String |
| currency | CurrencyDto |
| summary | SavingsSummaryDto |
| status | AccountStatusDto |

### SavingsTransactionDto

| Field | Type |
|-------|------|
| id | Long |
| transactionType | TransactionTypeDto |
| date | List\<Int\> |
| amount | Double |
| runningBalance | Double |
| currency | CurrencyDto |

### TransactionTypeDto

| Field | Type |
|-------|------|
| value | Int |
| code | String |
| description | String |

### CurrencyDto

| Field | Type |
|-------|------|
| code | String |
| displaySymbol | String |

### LoanDto

| Field | Type |
|-------|------|
| id | Long |
| accountNo | String |
| productName | String |
| loanProductId | Long |
| status | LoanStatusDto |
| principal | Double |
| interestRatePerPeriod | Double |
| termFrequency | Int |
| repaymentSchedule | RepaymentScheduleDto |
| summary | LoanSummaryDto |
| isOverdue | Boolean |

### LoanStatusDto

| Field | Type |
|-------|------|
| id | Int |
| code | String |
| value | String |
| active | Boolean |
| closed | Boolean |

### RepaymentScheduleDto

| Field | Type |
|-------|------|
| totalPrincipalExpected | Double |
| totalInterestCharged | Double |
| totalRepaymentExpected | Double |
| periods | List\<RepaymentPeriodDto\> |

### RepaymentPeriodDto

| Field | Type |
|-------|------|
| period | Int |
| dueDate | List\<Int\> |
| principalDue | Double |
| interestDue | Double |
| totalDueForPeriod | Double |
| totalPaidForPeriod | Double |
| complete | Boolean |

### LoanSummaryDto

| Field | Type |
|-------|------|
| principalDisbursed | Double |
| principalOutstanding | Double |
| totalOutstanding | Double |
| totalRepayment | Double |

### LoanRequestPayload

| Field | Type |
|-------|------|
| clientId | Long |
| requested_amount | Double |
| purpose | String |
| duration_weeks | Int |
| savings_balance_at_request | Double |
| submitted_at | String |
| status | String |

### LoanRequestResponse

| Field | Type |
|-------|------|
| resourceId | Long |
| officeId | Long |
| clientId | Long |
| resourceExternalId | String |

### SyncQueueEntry

| Field | Type |
|-------|------|
| id | Long |
| entityType | String |
| payload | String |
| status | String |
| createdAt | String |
| retryCount | Int |

### LoanSummary (dashboard model)

| Field | Type |
|-------|------|
| loanId | Long |
| productName | String |
| principalAmount | Double |
| outstandingBalance | Double |
| nextRepaymentDate | String |
| nextRepaymentAmount | Double |
| isOverdue | Boolean |
