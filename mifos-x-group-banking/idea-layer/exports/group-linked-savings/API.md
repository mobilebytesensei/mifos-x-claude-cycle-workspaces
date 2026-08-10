# Group-Linked Savings — API Reference
**Feature**: group-linked-savings | **Requirement**: FR-017
**Backend**: Mifos Fineract REST API

---

## Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /fineract-provider/api/v1/savingsaccounts/{groupSavingsId}/transactions | Fetch group mandatory savings transactions (up to 50) | BasicAuth |
| GET | /fineract-provider/api/v1/clients/{clientId}/accounts | Fetch individual savings accounts for a member | BasicAuth |
| GET | /fineract-provider/api/v1/savingsaccounts/{individualSavingsId}/transactions | Fetch individual savings transactions for a member | BasicAuth |

---

## Request / Response Details

### GET /savingsaccounts/{groupSavingsId}/transactions

**Purpose**: Fetch all mandatory group savings transactions. Used to compute per-member contribution totals by matching transaction notes to member names.

**Query params**: `limit=50` (covers up to 10 members × 5 meetings)

**Response**:
```json
{
  "pageItems": [
    {
      "id": "9001",
      "transactionType": "DEPOSIT",
      "date": [2026, 5, 6],
      "amount": 200.0,
      "runningBalance": 12600.0,
      "note": "Meeting #4 savings — Mary Akinyi"
    },
    {
      "id": "9002",
      "transactionType": "DEPOSIT",
      "date": [2026, 5, 6],
      "amount": 300.0,
      "runningBalance": 12900.0,
      "note": "Meeting #4 savings — John Mwangi"
    },
    {
      "id": "9003",
      "transactionType": "DEPOSIT",
      "date": [2026, 4, 29],
      "amount": 200.0,
      "runningBalance": 10800.0,
      "note": "Meeting #3 savings — Mary Akinyi"
    },
    {
      "id": "9004",
      "transactionType": "DEPOSIT",
      "date": [2026, 4, 29],
      "amount": 300.0,
      "runningBalance": 11100.0,
      "note": "Meeting #3 savings — John Mwangi"
    }
  ],
  "totalFilteredRecords": 20
}
```

**Errors**:
- 404: Group has no mandatory savings account — show empty group savings state
- 5xx: Show cached data from SQLDelight with last-sync band

### GET /clients/{clientId}/accounts

**Purpose**: Discover a member's individual savings account ID. Called once per member during dashboard load. Results cached in SQLDelight.

**Response**:
```json
{
  "savingsAccounts": [
    {
      "id": "601",
      "productId": "3",
      "productName": "Individual Voluntary Savings",
      "status": "Active",
      "accountBalance": 1500.0
    },
    {
      "id": "501",
      "productId": "1",
      "productName": "Group Mandatory Savings",
      "status": "Active",
      "accountBalance": 0.0
    }
  ]
}
```

**Filtering**: The dashboard uses only accounts where `productName` contains "Individual" or `productId` matches the group's individual savings product.

**Errors**:
- 404: Member has no accounts — row shows KES 0 balance with no transaction chip

### GET /savingsaccounts/{individualSavingsId}/transactions

**Purpose**: Fetch last 20 individual savings transactions per member. Used to determine current balance, last transaction type (deposit/withdrawal), and weekly trend data.

**Query params**: `limit=20`

**Response**:
```json
{
  "pageItems": [
    {
      "id": "8001",
      "transactionType": "DEPOSIT",
      "date": [2026, 5, 4],
      "amount": 500.0,
      "runningBalance": 1500.0,
      "note": "Individual deposit — Amara Diallo"
    },
    {
      "id": "8002",
      "transactionType": "WITHDRAWAL",
      "date": [2026, 4, 20],
      "amount": 200.0,
      "runningBalance": 1000.0,
      "note": "Individual withdrawal — Amara Diallo"
    }
  ],
  "totalFilteredRecords": 5
}
```

**Errors**:
- 404: No individual transactions yet — show KES 0 balance, no chip

---

## Client-Side Computation

### Per-Member Group Savings Totals
The Fineract savings account belongs to the group (mandatory savings product). Individual transactions reference member names via the `note` field (`"Meeting #N savings — {memberName}"`). The client parses this to aggregate per-member totals:

```
For each transaction t in groupSavingsTransactions:
  memberName = t.note.substringAfter("savings — ").trim()
  memberContributions[memberName] += t.amount
  meetingCounts[memberName]++
```

**Meetings contributed**: Count of distinct transactions per member in the group savings account.

**Last contribution**: The most recent transaction amount for that member.

**Cycle target**: `minContribution (KES 200) × memberCount (5) × plannedMeetings (26)` = KES 26,000 for demo group.

**Cycle collected**: Running total of all mandatory savings deposits in the current cycle.

**Cycle progress**: `cycleCollected / cycleTarget` — shown as LinearProgressIndicator.

### Weekly Trend Data
Group weekly trend:
```
For each transaction t: weekLabel = ISO week of t.date
weeklyGroupAmounts[weekLabel] += t.amount
```

Individual weekly trend (per member, then summed):
```
For each member m, for each transaction t in m.individualTransactions:
  weekLabel = ISO week of t.date
  if DEPOSIT: weeklyIndividualAmounts[weekLabel] += t.amount
  if WITHDRAWAL: weeklyIndividualAmounts[weekLabel] -= t.amount
```

---

## DTOs

### SavingsTransactionListResponse
| Field | Type | Description |
|-------|------|-------------|
| pageItems | List<SavingsTransaction> | Ordered by date descending |
| totalFilteredRecords | Int | Total transaction count in account |

### SavingsTransaction
| Field | Type | Description |
|-------|------|-------------|
| id | String | Transaction ID |
| transactionType | String | "DEPOSIT" or "WITHDRAWAL" |
| date | List<Int> | [year, month, day] — e.g. [2026, 5, 6] |
| amount | Double | KES amount |
| runningBalance | Double | Account balance after this transaction |
| note | String? | Free-text note (includes member name for group savings) |

### ClientAccountsResponse
| Field | Type | Description |
|-------|------|-------------|
| savingsAccounts | List<SavingsAccountSummary> | All savings accounts for this client |

### SavingsAccountSummary
| Field | Type | Description |
|-------|------|-------------|
| id | String | Savings account ID (used for transactions endpoint) |
| productId | String | Product ID (used to distinguish mandatory vs individual) |
| productName | String | Human-readable product name |
| status | String | "Active", "Closed", "Dormant" |
| accountBalance | Double | Current balance in KES |

### MemberGroupSavingsRow (computed)
| Field | Type | Description |
|-------|------|-------------|
| memberId | String | Fineract client ID |
| name | String | Full name |
| totalContributed | Long | Sum of deposits tagged with this member's name |
| lastContribution | Long | Most recent deposit amount |
| meetingsContributed | Int | Distinct meeting deposits counted |

### MemberIndividualSavingsRow (computed)
| Field | Type | Description |
|-------|------|-------------|
| memberId | String | Fineract client ID |
| name | String | Full name |
| currentBalance | Long | From SavingsAccountSummary.accountBalance |
| lastTransaction | Long? | Amount of most recent transaction |
| lastTransactionDate | String? | Formatted: "06 May 2026" |
| lastTransactionType | String? | "DEPOSIT" or "WITHDRAWAL" |

### WeeklyContributionPoint (computed)
| Field | Type | Description |
|-------|------|-------------|
| weekLabel | String | ISO week label e.g. "W48" |
| groupAmount | Long | Total mandatory savings that week |
| individualAmount | Long | Net individual savings activity that week |

---

## Demo Data

### Group: Mwangaza Women's Group
**groupId**: 7 | **groupSavingsAccountId**: 200

**5 members with group savings contributions (Cycle 1, Meetings #1–4)**:

| Member | memberId | individualSavingsAccountId | Group contributions | Individual balance |
|--------|----------|--------------------------|--------------------|--------------------|
| Amara Diallo | 101 | 601 | KES 800 (4 meetings × KES 200) | KES 1,500 |
| Peter Otieno | 102 | 602 | KES 1,200 (4 meetings × KES 300) | KES 750 |
| Grace Mwangi | 103 | 603 | KES 800 (4 meetings × KES 200) | KES 2,200 |
| John Mwangi | 104 | 604 | KES 1,200 (4 meetings × KES 300) | KES 400 |
| Mary Akinyi | 105 | 605 | KES 600 (3 meetings × KES 200, 1 absent) | KES 0 |

**GroupSavingsSummary (demo)**:
- totalCollected: KES 4,600
- cycleTarget: KES 26,000
- cycleProgress: 0.177 (17.7%)
- memberRows: 5 rows as above

**IndividualSavingsSummary (demo)**:
- totalBalance: KES 4,850
- memberRows: 5 rows as above

**WeeklyTrend (demo — last 6 weeks)**:

| weekLabel | groupAmount | individualAmount |
|-----------|-------------|-----------------|
| W48 | 1,000 | 300 |
| W49 | 1,200 | 500 |
| W50 | 850 | 200 |
| W51 | 1,500 | 700 |
| W52 | 1,200 | 400 |
| W3 | 1,850 | 650 |
