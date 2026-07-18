# Member Savings Detail — API Contract

## Endpoints

| ID | Method | Endpoint | Auth | Writable | Cache |
|---|---|---|---|---|---|
| `get_member_savings_detail` | GET | `/companion/groups/{groupId}/members/{memberId}/savings` | Bearer | no | 120 s SWR |

## Request / Response Details

### GET /companion/groups/{groupId}/members/{memberId}/savings

**Query Params**

| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| limit | Int | no | `20` | Page size |
| offset | Int | no | `0` | Pagination offset |

**Response**

| Field | Type | Description |
|---|---|---|
| member | Member | Member identity |
| totalSaved | Long | Total KES deposited |
| sharesHeld | Int? | SHARE_BASED_VARIABLE only — number of shares |
| shareValue | Long? | SHARE_BASED_VARIABLE only — KES per share |
| totalWithdrawals | Long | Total KES withdrawn |
| savingsDataPoints | List<SavingsDataPoint> | Cumulative sparkline data |
| transactions | List<SavingsTransaction> | Current page |
| totalCount | Int | Total transaction count |
| hasMore | Boolean | More pages available |

---

## DTOs

### MemberSavingsDetailResponse
```
member: Member
totalSaved: Long
sharesHeld: Int?         // SHARE_BASED_VARIABLE only
shareValue: Long?        // SHARE_BASED_VARIABLE only
totalWithdrawals: Long
savingsDataPoints: List<SavingsDataPoint>
transactions: List<SavingsTransaction>
totalCount: Int
hasMore: Boolean
```

### Member
```
memberId: String
memberName: String
memberPhone: String?
```

### SavingsDataPoint (shared DTO)
```
date: String           // ISO-8601
cumulativeAmount: Long // KES (cents)
```

### SavingsTransaction (shared DTO — also used by savings-dashboard and personal-dashboard)
```
transactionId: String
transactionDate: String    // ISO-8601
amount: Long               // KES (cents)
transactionType: String    // CREDIT | DEBIT
description: String
```

### TransactionType (enum)
```
CREDIT    // Deposit
DEBIT     // Withdrawal
```

### TransactionFilter (local enum — client-side only, NOT an API param)
```
ALL
DEPOSITS    // maps to transactionType == CREDIT
WITHDRAWALS // maps to transactionType == DEBIT
```

## Pagination Contract

- `page_size = 20`
- On scroll to bottom → increment `offset` by 20 → fetch next page
- New transactions **appended** to `savings_transactions` cache (`append_to_existing`)
- Pull-to-refresh → reset `offset = 0`, clear cache, reload
- `hasMore == false` → stop paginating

## Offline Behaviour

`member_savings_cache` (120 s SWR) and `savings_transactions` (shared table) serve stale
data offline. A "Last synced" banner is shown. Pagination while offline loads no new data
and shows a "Requires internet for more" message at list bottom.

## Error Type Map

| Error Class | Behaviour |
|---|---|
| `network.offline` | Serve stale from `member_savings_cache` + `savings_transactions` |
| `404 Not found` | "Member not found" error state — back to savings-dashboard |
| `403 Forbidden` | "Not authorised to view this member" error state |
| `401 Unauthorized` | Navigate to login-signup |
| `500 Server` | Error banner + retry |
