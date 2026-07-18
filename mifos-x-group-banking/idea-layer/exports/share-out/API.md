# Share-Out — API Reference
**Feature**: share-out | **Requirement**: FR-007
**Backend**: Mifos Fineract REST API + dt_share_out custom datatable + Companion API (COMP-DIST)

> **Companion API note (global self-signup pivot, 2026-07-17):** The distribution execute step
> (pro-rata share-out and ROSCA rotation payout) routes through **COMP-DIST-001/002** in mcp-mifosx
> (`go/tools/datatables.go`). The client computes the payout distribution locally; the companion server
> re-validates corpus sufficiency and executes GSIM withdrawal / account-transfer + journal entries
> (CK4 security contract). The Fineract direct endpoints below handle read operations and the
> individual savings withdrawals that the companion dispatch drives.
> Build spec: `server-layer/COMPANION_API_BUILD_DEPLOY.md §1b (COMP-DIST-001/002)`

| Contract | Method | Path | Description |
|----------|--------|------|-------------|
| COMP-DIST-001 | POST | `/companion/groups/{id}/shareout/execute` | Pro-rata share-out: server re-validates + executes payouts |
| COMP-DIST-002 | POST | `/companion/groups/{id}/rotation/execute` | ROSCA rotation payout: drives next-recipient withdrawal |

---

## Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /fineract-provider/api/v1/centers/{centerId}/accounts | Savings+loan accounts for corpus+profit computation | BasicAuth |
| GET | /fineract-provider/api/v1/datatables/dt_share_out/{centerId} | Existing share-out records for this cycle | BasicAuth |
| POST | /fineract-provider/api/v1/datatables/dt_share_out/{centerId} | Create share-out record | BasicAuth |
| POST | /fineract-provider/api/v1/savingsaccounts/{savingsAccountId}/transactions | Member withdrawal (payout) | BasicAuth |

---

## Request / Response Details

### GET /centers/{centerId}/accounts
**Response**:
```json
{
  "savingsAccounts": [
    {
      "id": 501,
      "accountBalance": 20000.0,
      "accountNo": "000000501",
      "productName": "Group Mandatory Savings",
      "status": { "value": "Active" }
    },
    {
      "id": 502,
      "accountBalance": 5600.0,
      "productName": "Amara Diallo — Individual Savings",
      "status": { "value": "Active" }
    }
  ],
  "loanAccounts": [
    { "id": 1001, "totalInterestPaid": 3200.0 },
    { "id": 1002, "totalInterestPaid": 800.0 }
  ]
}
```

### GET /datatables/dt_share_out/{centerId}
```json
[
  {
    "id": 1,
    "cycle_number": 1,
    "total_pool": 24000.0,
    "executed_at": "07 May 2026",
    "status": "completed"
  }
]
```
**404 response**: No share-out record yet — treat as fresh cycle, proceed with calculation.

### POST /datatables/dt_share_out/{centerId}
**Body (CreateShareOutRequest)**:
```json
{
  "cycle_number": 1,
  "total_pool": 24000.0,
  "executed_at": "07 May 2026",
  "status": "completed",
  "locale": "en",
  "dateFormat": "dd MMMM yyyy"
}
```
**Response (DataTableEntryResponse)**:
```json
{
  "resourceId": 1,
  "resourceIdentifier": "dt_share_out_1"
}
```
**Errors**:
- 400: Validation error (e.g. duplicate cycle number)
- 403: Forbidden — chairperson role required
- 500: Server error — queue to SyncQueue

### POST /savingsaccounts/{savingsAccountId}/transactions (member payout)
**Body (SavingsWithdrawalRequest)**:
```json
{
  "transactionDate": "07 May 2026",
  "transactionAmount": 6792.0,
  "paymentTypeId": 1,
  "note": "Share-out payout — Cycle 1",
  "locale": "en",
  "dateFormat": "dd MMMM yyyy"
}
```
**Response (SavingsTransactionResponse)**:
```json
{
  "officeId": 1,
  "savingsId": 1001,
  "resourceId": 9001
}
```
**Errors**:
- 400: Insufficient balance or validation error — set member status FAILED
- 403: Forbidden — set member status FAILED
- 500: Server error — set member status FAILED

---

## DTOs

### MemberPayout
| Field | Type | Description |
|-------|------|-------------|
| memberId | Long | Fineract client ID |
| memberName | String | Full display name |
| memberInitials | String | Computed 2-char initials (e.g. "AD") |
| totalSavings | Double (KES) | Total savings contributed this cycle |
| sharePercent | Double | Fraction of total group savings (0.0–1.0) |
| payoutAmount | Double (KES) | Computed: sharePercent × totalPool |
| savingsAccountId | Long | Fineract savings account ID for withdrawal |

### MemberExecutionStatus
| Value | Description |
|-------|-------------|
| PENDING | Not yet started |
| IN_PROGRESS | Withdrawal POST in flight |
| DONE | Withdrawal succeeded |
| FAILED | Withdrawal failed — added to failedPayouts |
| QUEUED | Enqueued to SyncQueue (offline path) |

### CreateShareOutRequest
| Field | Type | Required |
|-------|------|----------|
| cycle_number | Int | Yes |
| total_pool | Double | Yes |
| executed_at | String (dd MMMM yyyy) | Yes |
| status | String ("completed") | Yes |
| locale | String ("en") | Yes |
| dateFormat | String | Yes |

### SavingsWithdrawalRequest
| Field | Type | Notes |
|-------|------|-------|
| transactionDate | String | dd MMMM yyyy format |
| transactionAmount | Double | Member payout amount in KES |
| paymentTypeId | Int | 1 = Cash |
| note | String | "Share-out payout — Cycle {{cycleNumber}}" |
| locale | String | "en" |
| dateFormat | String | "dd MMMM yyyy" |

### CenterAccounts (computed)
| Field | Type | Source |
|-------|------|--------|
| totalCorpus | Double (KES) | Sum of all savingsAccounts.accountBalance |
| totalInterestEarned | Double (KES) | Sum of all loanAccounts.totalInterestPaid |

### ShareOutRecord (dt_share_out)
| Field | Type | Description |
|-------|------|-------------|
| id | Long | Datatable row ID |
| cycleNumber | Int | Cycle number (1-indexed) |
| totalPool | Double (KES) | Total amount distributed |
| executedAt | String? | ISO date or null if not executed |
| status | String | "pending" or "completed" |
