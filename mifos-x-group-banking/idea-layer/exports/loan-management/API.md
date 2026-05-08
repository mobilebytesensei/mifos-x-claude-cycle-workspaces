# Loan Management — API Reference
**Feature**: loan-management | **Requirements**: FR-005, FR-006
**Backend**: Mifos Fineract REST API

---

## Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /fineract-provider/api/v1/groups/{groupId}/loans | Paginated list of loans for a group | BasicAuth |
| GET | /fineract-provider/api/v1/loans/template | Loan application template for client+product | BasicAuth |
| GET | /fineract-provider/api/v1/loanproducts | All available loan products | BasicAuth |
| GET | /fineract-provider/api/v1/clients/{clientId}/accounts | Member accounts and savings balance | BasicAuth |
| GET | /fineract-provider/api/v1/datatables/dt_group_corpus/{groupId} | Group corpus balance | BasicAuth |
| GET | /fineract-provider/api/v1/datatables/dt_group_config/{groupId} | Group loan policy (multiplier) | BasicAuth |
| POST | /fineract-provider/api/v1/loans | Submit loan application | BasicAuth |
| GET | /fineract-provider/api/v1/loans/{loanId}?associations=repaymentSchedule,transactions | Full loan detail | BasicAuth |
| POST | /fineract-provider/api/v1/loans/{loanId}/transactions?command=repayment | Record repayment | BasicAuth |
| GET | /fineract-provider/api/v1/datatables/dt_loan_vote/{loanId} | Loan vote tally | BasicAuth |

---

## Request / Response Details

### GET /groups/{groupId}/loans
**Query params**: `limit=20`, `offset=0`, `loanStatus=active|overdue|closed|all`

**Response**:
```json
{
  "totalFilteredRecords": 12,
  "pageItems": [
    {
      "id": 101,
      "clientId": 201,
      "clientName": "Peter Otieno",
      "loanProductName": "Standard Group Loan",
      "principal": 15000.0,
      "summary": {
        "principalOutstanding": 11250.0,
        "totalOverdue": 0.0
      },
      "status": { "id": 300, "value": "Active" },
      "nextRepaymentDate": [2026, 5, 12]
    }
  ]
}
```

### POST /loans (Submit Application)
**Body**:
```json
{
  "clientId": 201,
  "productId": 3,
  "principal": 15000.0,
  "loanTermFrequency": 12,
  "loanTermFrequencyType": { "id": 1, "value": "Weeks" },
  "numberOfRepayments": 12,
  "repaymentEvery": 1,
  "repaymentFrequencyType": { "id": 1, "value": "Weeks" },
  "interestRatePerPeriod": 5.0,
  "amortizationType": { "id": 1, "value": "Equal installments" },
  "interestType": { "id": 0, "value": "Declining Balance" },
  "interestCalculationPeriodType": { "id": 1, "value": "Same as repayment period" },
  "transactionProcessingStrategyId": 1,
  "expectedDisbursementDate": "14 May 2026",
  "submittedOnDate": "07 May 2026",
  "loanPurposeId": 2,
  "locale": "en",
  "dateFormat": "dd MMMM yyyy"
}
```
**Response**: `{ "officeId": 1, "clientId": 201, "loanId": 101, "resourceId": 101 }`

### POST /loans/{loanId}/transactions?command=repayment
**Body**:
```json
{
  "transactionDate": "12 May 2026",
  "transactionAmount": 1250.0,
  "paymentTypeId": 1,
  "locale": "en",
  "dateFormat": "dd MMMM yyyy"
}
```
**Response**: `{ "officeId": 1, "loanId": 101, "resourceId": 501 }`

### GET /loans/{loanId}?associations=repaymentSchedule,transactions
**Response (abbreviated)**:
```json
{
  "id": 101,
  "clientName": "Peter Otieno",
  "loanProductName": "Standard Group Loan",
  "principal": 15000.0,
  "interestRatePerPeriod": 5.0,
  "status": { "id": 300, "value": "Active" },
  "summary": {
    "principalOutstanding": 11250.0,
    "totalOutstanding": 12000.0,
    "totalOverdue": 0.0
  },
  "repaymentSchedule": {
    "periods": [
      { "period": 1, "dueDate": [2026,4,21], "principalDue": 1250.0, "interestDue": 750.0, "totalInstallmentAmountForPeriod": 2000.0, "totalPaidForPeriod": 2000.0, "complete": true },
      { "period": 2, "dueDate": [2026,4,28], "principalDue": 1250.0, "interestDue": 687.5, "totalInstallmentAmountForPeriod": 1937.5, "totalPaidForPeriod": 1937.5, "complete": true },
      { "period": 3, "dueDate": [2026,5,5], "principalDue": 1250.0, "interestDue": 625.0, "totalInstallmentAmountForPeriod": 1875.0, "totalPaidForPeriod": 1875.0, "complete": true },
      { "period": 4, "dueDate": [2026,5,12], "principalDue": 1250.0, "interestDue": 562.5, "totalInstallmentAmountForPeriod": 1812.5, "totalPaidForPeriod": 0.0, "complete": false }
    ]
  }
}
```

---

## DTOs

### LoanSummary
| Field | Type | Description |
|-------|------|-------------|
| id | Long | Fineract loan ID |
| memberId | Long | Fineract client ID |
| memberName | String | Full display name |
| memberPhotoUrl | String? | Photo URL or null |
| loanProductName | String | Product name string |
| principalAmount | Double (KES) | Original loan principal |
| outstandingBalance | Double (KES) | Remaining balance |
| overdueAmount | Double (KES) | Amount overdue (0 if current) |
| status | LoanStatus | ACTIVE, OVERDUE, CLOSED, PENDING, REJECTED |
| nextRepaymentDate | String? | ISO date string |
| isOverdue | Boolean | Derived from overdueAmount > 0 |
| fineractLoanId | Long | Fineract resource ID |

### LoanDetail
| Field | Type | Description |
|-------|------|-------------|
| id | Long | Loan ID |
| memberName | String | Borrower name |
| loanProductName | String | Product name |
| principalAmount | Double (KES) | Disbursed principal |
| disbursedDate | String | ISO date |
| interestRatePercent | Double | Weekly interest % |
| totalOutstanding | Double (KES) | Total remaining |
| totalOverdue | Double (KES) | Overdue amount |
| status | LoanStatus | Current status |

### RepaymentScheduleRow
| Field | Type | Description |
|-------|------|-------------|
| weekNumber | Int | Repayment period number |
| dueDate | String | ISO date |
| dueAmount | Double (KES) | Total installment due |
| paidAmount | Double (KES) | Amount paid |
| balance | Double (KES) | Remaining for this period |
| status | RepaymentRowStatus | PAID, PARTIAL, UPCOMING, OVERDUE |

### LoanApplicationRequest
| Field | Type | Description |
|-------|------|-------------|
| memberId | Long | Selected member Fineract client ID |
| productId | Long | Selected loan product ID |
| amount | Double | Requested amount in KES |
| durationWeeks | Int | Loan term in weeks |
| purpose | LoanPurpose | MEDICAL, EDUCATION, BUSINESS, EMERGENCY, OTHER |
| groupId | Long | Group context for corpus check |
