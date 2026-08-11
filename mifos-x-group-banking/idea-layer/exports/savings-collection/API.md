# API — savings-collection
# MifosSave (mifos-x-group-banking) | Feature FR-004 / FR-017
# Generated: 2026-05-06

---

## Endpoints Table

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /fineract-provider/api/v1/savingsaccounts/{groupSavingsId}/transactions | Fetch group savings transactions for trend chart and per-member contributions | BasicAuth |
| GET | /fineract-provider/api/v1/clients/{clientId}/accounts | Fetch client accounts including individual savings account ID | BasicAuth |
| GET | /fineract-provider/api/v1/savingsaccounts/{individualSavingsId}/transactions | Fetch individual savings transactions per member | BasicAuth |
| POST | /fineract-provider/api/v1/savingsaccounts/{savingsId}/transactions | Post savings deposit (called per member per savings type on meeting submit) | BasicAuth |

---

## Request/Response Details

### GET /savingsaccounts/{groupSavingsId}/transactions
**Path params:** groupSavingsId (String — the group-linked savings account ID)
**Query params:** limit=50 (returns last 50 transactions)
**Response:** SavingsTransactionListResponse
**Error handling:** 401 → redirect login; 404 → empty state "No group savings data yet"; 5xx → show cached data with last-sync band

### GET /clients/{clientId}/accounts
**Path params:** clientId (String — Fineract client ID for each group member)
**Response:** ClientAccountsResponse
**Error handling:** 404 → member has no individual savings account yet — show "KES 0 balance" placeholder
**Called:** Once per member when loading IndividualSavingsTab

### GET /savingsaccounts/{individualSavingsId}/transactions
**Path params:** individualSavingsId (String — from ClientAccountsResponse.savingsAccounts[0].id where productName matches individual savings product)
**Query params:** limit=20
**Response:** SavingsTransactionListResponse
**Error handling:** 404 → no transactions yet, show empty state with KES 0 balance

### POST /savingsaccounts/{savingsId}/transactions
**Path params:** savingsId (String)
**Body:** SavingsTransactionRequest
**Response:** SavingsTransactionResponse {officeId, savingsId, resourceId}
**Error handling:** 400 → validation error snackbar; 5xx → queue to SyncQueueRepository
**Called:** Once per member per savings type where amount > 0 during meeting submission

---

## DTOs

### SavingsTransactionListResponse
| Field | Type | Notes |
|-------|------|-------|
| pageItems | List\<SavingsTransaction\> | Ordered newest-first |
| totalFilteredRecords | Int | Total count in DB |

### SavingsTransaction
| Field | Type | Notes |
|-------|------|-------|
| id | String | Unique transaction ID |
| transactionType | String | "DEPOSIT" or "WITHDRAWAL" |
| date | List\<Int\> | [year, month, day] — e.g. [2026, 5, 7] |
| amount | Double | Transaction amount in KES |
| runningBalance | Double | Account balance after this transaction |
| note | String? | Optional memo |

### ClientAccountsResponse
| Field | Type | Notes |
|-------|------|-------|
| savingsAccounts | List\<SavingsAccountSummary\> | Includes both group-linked and individual accounts |

### SavingsAccountSummary
| Field | Type | Notes |
|-------|------|-------|
| id | String | Savings account ID |
| productId | String | Fineract savings product ID |
| productName | String | e.g. "Group Savings" or "Individual Savings" |
| status | String | "ACTIVE", "APPROVED", "CLOSED" |
| accountBalance | Double | Current balance in KES |

### SavingsTransactionRequest
| Field | Type | Default | Notes |
|-------|------|---------|-------|
| transactionDate | String | today | Format: "dd MMMM yyyy" e.g. "07 May 2026" |
| transactionAmount | Long | from input | Must be > 0; group savings >= 200 (FR-020 enforced client-side) |
| paymentTypeId | Int | 1 | 1 = Cash |
| locale | String | "en" | |
| dateFormat | String | "dd MMMM yyyy" | |

### SavingsTransactionResponse
| Field | Type | Notes |
|-------|------|-------|
| officeId | Int | Fineract office ID |
| savingsId | Long | Savings account ID (echoed) |
| resourceId | Long | Created transaction ID |

### GroupSavingsSummary (app-level DTO, computed from transactions)
| Field | Type | Notes |
|-------|------|-------|
| totalCollected | Long | Sum of all group savings deposits this cycle |
| cycleTarget | Long | cycleTarget = cycleWeeks × minContribution × memberCount |
| cycleProgress | Float | totalCollected / cycleTarget (0.0–1.0) |
| memberRows | List\<MemberGroupSavingsRow\> | Per-member computed summary |

### MemberGroupSavingsRow
| Field | Type | Notes |
|-------|------|-------|
| memberId | String | |
| name | String | |
| totalContributed | Long | Sum of deposits attributed to member |
| lastContribution | Long | Most recent single deposit amount |
| meetingsContributed | Int | Count of weeks with non-zero deposit |

### IndividualSavingsSummary (app-level DTO)
| Field | Type | Notes |
|-------|------|-------|
| totalBalance | Long | Sum of all member individual savings balances |
| memberRows | List\<MemberIndividualSavingsRow\> | |

### MemberIndividualSavingsRow
| Field | Type | Notes |
|-------|------|-------|
| memberId | String | |
| name | String | |
| currentBalance | Long | accountBalance from SavingsAccountSummary |
| lastTransaction | Long | Most recent transaction amount (absolute value) |
| lastTransactionType | String | "DEPOSIT" or "WITHDRAWAL" |
| lastTransactionDate | String | Formatted display date |
