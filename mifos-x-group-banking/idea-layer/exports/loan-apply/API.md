<!--
  generated_from_feature: loan-apply
  contract_version: "2.0.0"
  source: idea-layer/screens/loan-apply/api.yaml
  generated_by: /idea-feature-export-spec
-->

# Loan Apply — API Contract

## Endpoints (7)

| ID | Function | Method | Endpoint | Auth | Writable |
|---|---|---|---|---|---|
| `get_group_members` | get_group_members | GET | `/groups/{groupId}?associations=clientMembers` | Basic | no |
| `get_loan_products` | list_available_loan_products | GET | `/loanproducts` | Basic | no |
| `get_loan_template` | get_loan_app_template | GET | `/loans/template` | Basic | no |
| `get_member_savings` | get_savings | GET | `/clients/{clientId}/accounts` | Basic | no |
| `get_group_corpus` | get_group_corpus | GET | `/datatables/dt_group_corpus/{groupId}` | Basic | no |
| `get_group_config` | get_group_config | GET | `/datatables/dt_group_config/{groupId}` | Basic | no |
| `post_loan` | create_new_loan | POST | `/loans` | Basic | yes |

Base path: `/fineract-provider/api/v1` · Tenant header: `X-Fineract-Platform-TenantId: default`.

## Request / Response Details

### GET /groups/{groupId}?associations=clientMembers
Params: `groupId: Long (required, nav_params)`.
Response: `clientMembers[]` of `{ id: Long, displayName: String, imagePresent: Boolean }`.
Errors: 404 Group not found · 500 Server error. Cache: TTL 3600 s, cache-first.

### GET /loanproducts
Response: array of `{ id, name, shortName, principal, minPrincipal, maxPrincipal,
numberOfRepayments, interestRatePerPeriod }`. Cache: TTL 3600 s, cache-first.

### GET /loans/template
Params: `clientId: Long (required)`, `productId: Long (required)`,
`templateType: String (default "individual")`.
Response: `{ principal, numberOfRepayments, interestRatePerPeriod, interestType{id,value},
amortizationType{id,value}, repaymentEvery }`. Pre-fills defaults for the selected product.

### GET /clients/{clientId}/accounts
Params: `clientId: Long (required)`.
Response: `savingsAccounts[]` of `{ id: Long, accountBalance: Double, status{value} }`.
Used for eligibility computation.

### GET /datatables/dt_group_corpus/{groupId}
Params: `groupId: Long (required)`.
Response: `{ corpus_balance: Double, last_updated: String }`.

### GET /datatables/dt_group_config/{groupId}
Params: `groupId: Long (required)`.
Response: `{ loan_multiplier: Double, max_loan_amount: Double, meeting_frequency: String }`.

### POST /loans (create loan application)

**Body**

| Field | Type | Notes |
|---|---|---|
| clientId | Long | Selected member's Fineract client id |
| productId | Long | Selected loan product |
| principal | Double | Requested amount |
| loanTermFrequency | Int | = durationWeeks |
| loanTermFrequencyType | {id:1, value:"Weeks"} | |
| numberOfRepayments | Int | |
| repaymentEvery | 1 | |
| repaymentFrequencyType | {id:1, value:"Weeks"} | |
| interestRatePerPeriod | Double | |
| amortizationType | {id:1, value:"Equal installments"} | |
| interestType | {id:0, value:"Declining Balance"} | |
| interestCalculationPeriodType | {id:1, value:"Same as repayment period"} | |
| transactionProcessingStrategyId | 1 | |
| expectedDisbursementDate | String | |
| submittedOnDate | String | |
| loanPurposeId | Int | mapped from LoanPurpose enum |

**Response:** `{ officeId: Long, clientId: Long, loanId: Long, resourceId: Long }` —
loan created with status "submitted and pending approval".

**Errors:** 400 Validation error (show field errors) · 403 Forbidden (insufficient role) ·
500 Server error.

## DTOs

### GroupMember
```
id: Long
displayName: String
imagePresent: Boolean
fineractClientId: Long
```

### LoanProduct
```
id: Long
name: String
shortName: String
minPrincipal: Double
maxPrincipal: Double
interestRatePerPeriod: Double
```

### LoanPurpose (enum)
```
MEDICAL | EDUCATION | BUSINESS | EMERGENCY | OTHER
```

### LoanApplicationRequest
```
memberId: Long
productId: Long
amount: Double
durationWeeks: Int
purpose: LoanPurpose
groupId: Long
```

### GroupConfig
```
loanMultiplier: Double
maxLoanAmount: Double
```

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `AmountExceedsEligibility` | Inline `amountError` (error_amount_exceeds); submit disabled |
| `CorpusInsufficient` (422) | `LoanApplyError.CorpusInsufficient` (error_corpus), no retry |
| `network.offline` | Block submit; `LoanApplyError.Network` + ShowSnackbar(error_network) |
| `400 Validation` | Per-field validation errors surfaced |
| `403 Forbidden` | Insufficient-role error |
| `401 Unauthorized` | `LoanApplyError.Auth` → redirect to login |
| `500 Server` | `LoanApplyError.Server` (retry-able); error_state retry CTA |

## Offline Behaviour

Mount fetches are served from Store5/SQLDelight caches (`group_members`, `loan_products`,
`dt_group_config`) via `cmp-network-monitor` when offline, so the form and eligibility
recompute remain usable. Submission is **blocked offline** (risk policy forbids queued offline
loan submits) and surfaces `error_network`.
