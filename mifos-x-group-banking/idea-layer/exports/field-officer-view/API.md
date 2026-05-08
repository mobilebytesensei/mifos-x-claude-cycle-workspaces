# Field Officer View — API Reference
**Feature**: field-officer-view | **Requirement**: FR-009
**Backend**: Mifos Fineract REST API

---

## Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /fineract-provider/api/v1/centers?staffId={staffId}&limit=100 | All centers supervised by this field officer | BasicAuth (staff) |
| GET | /fineract-provider/api/v1/loans?groupId={groupId}&loanStatus=active | Active loans for a group (for overdue rate calculation) | BasicAuth |
| GET | /fineract-provider/api/v1/datatables/dt_group_corpus/{centerId} | Corpus balance for a group | BasicAuth |

---

## Request / Response Details

### GET /centers?staffId={staffId}&limit=100

**Purpose**: Fetch all VSLA centers (groups) this field officer supervises. Called once on dashboard load.

**Query params**: `staffId={staffId}` (Fineract staff ID from session), `limit=100`

**Response**:
```json
{
  "totalFilteredRecords": 8,
  "pageItems": [
    {
      "id": 7,
      "name": "Mwangaza Women's Group",
      "status": { "value": "Active" },
      "staffId": 3,
      "staffName": "James Otieno",
      "officeId": 1,
      "officeName": "Nairobi Branch"
    },
    {
      "id": 12,
      "name": "Tumaini Savings Circle",
      "status": { "value": "Active" },
      "staffId": 3,
      "staffName": "James Otieno",
      "officeId": 1,
      "officeName": "Nairobi Branch"
    },
    {
      "id": 15,
      "name": "Umoja Welfare Group",
      "status": { "value": "Active" },
      "staffId": 3,
      "staffName": "James Otieno",
      "officeId": 2,
      "officeName": "Mombasa Branch"
    },
    {
      "id": 18,
      "name": "Pamoja",
      "status": { "value": "Active" },
      "staffId": 3,
      "staffName": "James Otieno",
      "officeId": 2,
      "officeName": "Mombasa Branch"
    },
    {
      "id": 21,
      "name": "Maisha Bora Circle",
      "status": { "value": "Active" },
      "staffId": 3,
      "staffName": "James Otieno",
      "officeId": 3,
      "officeName": "Kisumu Branch"
    }
  ]
}
```

**Errors**:
- 401: Session expired — redirect to login
- 404: Staff has no centers assigned — show empty state
- 5xx: Show cached data from SQLDelight

---

### GET /loans?groupId={groupId}&loanStatus=active

**Purpose**: Fetch active loans for a group to compute overdueRate = overdueCount / totalActiveLoans.

**Query params**: `groupId={groupId}`, `loanStatus=active`

**Response**:
```json
{
  "totalFilteredRecords": 4,
  "pageItems": [
    {
      "id": 1001,
      "clientId": 101,
      "clientName": "Peter Otieno",
      "status": { "value": "Active" },
      "isNPA": false
    },
    {
      "id": 1002,
      "clientId": 102,
      "clientName": "Grace Mwangi",
      "status": { "value": "Active" },
      "isNPA": true
    }
  ]
}
```

**overdueRate computation**:
```
overdueCount = pageItems.count { it.isNPA == true }
totalActiveLoans = totalFilteredRecords
overdueRate = if (totalActiveLoans > 0) overdueCount.toFloat() / totalActiveLoans else 0.0f
```

**Errors**:
- 404: Group has no active loans → overdueRate = 0.0 → GREEN health

---

### GET /datatables/dt_group_corpus/{centerId}

**Purpose**: Fetch total savings (corpus balance) for each group.

**Response**:
```json
{
  "centerId": 7,
  "corpusBalance": 47500,
  "cashOnHand": 5000,
  "lastUpdatedMeeting": 4,
  "lastUpdatedDate": "06 May 2026"
}
```

**Errors**:
- 404: No corpus record yet → corpusBalance = 0 → group is new

---

## Client-Side KPI Computation

After fetching all groups, KPIs are computed:

```
kpiTotalGroups = centers.size
kpiTotalMembers = centers.sumOf { it.activeClientMembers.size }  // from centers detail
kpiTotalSavings = corpora.sumOf { it.corpusBalance }
kpiLoansOutstanding = activeLoans.sumOf { it.principal - it.totalAmountRepaid }
```

**KPI Demo Computation**:
```
kpiTotalGroups = 8
kpiTotalMembers = 94  (avg ~12 members × 8 groups)
kpiTotalSavings = sum of all corpus balances = KES 142,000
kpiLoansOutstanding = sum of outstanding loan balances = KES 87,500
```

---

## DTOs

### CenterSummary (from GET /centers)
| Field | Type | Description |
|-------|------|-------------|
| id | Long | Center ID (used as groupId) |
| name | String | Group name |
| status | CenterStatus | Active / Pending / Closed |
| staffId | Long | Assigned field officer staff ID |
| staffName | String | Field officer name |
| officeId | Long | Branch office ID |
| officeName | String | Branch name (used as Region filter) |

### LoanItem (from GET /loans)
| Field | Type | Description |
|-------|------|-------------|
| id | Long | Loan ID |
| clientId | Long | Borrower client ID |
| clientName | String | Borrower name |
| status | LoanStatus | Active, Closed |
| isNPA | Boolean | Non-performing asset = overdue |

### CorpusRecord (from dt_group_corpus)
| Field | Type | Description |
|-------|------|-------------|
| centerId | Long | Center ID |
| corpusBalance | Long | Total group corpus in KES |
| cashOnHand | Long | Physical cash on hand |
| lastUpdatedMeeting | Int | Meeting number of last update |
| lastUpdatedDate | String | Date of last corpus update |

### GroupHealthCard (computed)
| Field | Type | Description |
|-------|------|-------------|
| groupId | Long | Fineract center ID |
| groupName | String | Group display name |
| region | String | officeName (branch) |
| status | GroupStatus | ACTIVE / PENDING / CLOSED |
| memberCount | Int | Number of active members |
| totalSavings | Long | corpusBalance in KES |
| overdueRate | Float | overdueCount / totalActiveLoans (0.0–1.0) |
| overdueCount | Int | Count of NPA loans |
| totalActiveLoans | Int | Total active loans in group |
| healthLevel | HealthLevel | GREEN / AMBER / RED |

### HealthLevel (computed)
| Value | Condition | Primary Color | Container Color |
|-------|-----------|--------------|----------------|
| GREEN | overdueRate < 0.05 | primary #2E7D32 | primaryContainer #A6F1A6 |
| AMBER | 0.05 ≤ overdueRate < 0.20 | secondary #FF8F00 | secondaryContainer #FFDDB3 |
| RED | overdueRate ≥ 0.20 | error #D32F2F | errorContainer #FFDAD6 |

---

## Demo Data — 5 Groups (field officer: James Otieno, staffId=3)

| Group | groupId | Region | Members | Savings | Overdue | Health |
|-------|---------|--------|---------|---------|---------|--------|
| Mwangaza Women's Group | 7 | Nairobi | 12 | KES 47,500 | 0% | GREEN |
| Tumaini Savings Circle | 12 | Nairobi | 10 | KES 28,000 | 12% | AMBER |
| Umoja Welfare Group | 15 | Mombasa | 18 | KES 35,000 | 25% | RED |
| Pamoja | 18 | Mombasa | 8 | KES 18,500 | 3% | GREEN |
| Maisha Bora Circle | 21 | Kisumu | 11 | KES 13,000 | 8% | AMBER |

*Note: Full demo includes 8 groups total; 5 shown above are the primary rendered groups.*

**Total KPIs (all 8 groups)**:
- kpiTotalGroups: 8
- kpiTotalMembers: 94
- kpiTotalSavings: KES 142,000
- kpiLoansOutstanding: KES 87,500

---

## Export Report (CSV)

The Export Report action generates a CSV with one row per group:

```csv
Group Name,Region,Status,Members,Total Savings (KES),Active Loans,Overdue Count,Overdue Rate,Health
Mwangaza Women's Group,Nairobi,ACTIVE,12,47500,3,0,0%,GREEN
Tumaini Savings Circle,Nairobi,ACTIVE,10,28000,5,1,12%,AMBER
Umoja Welfare Group,Mombasa,ACTIVE,18,35000,8,2,25%,RED
Pamoja,Mombasa,ACTIVE,8,18500,2,0,3%,GREEN
Maisha Bora Circle,Kisumu,ACTIVE,11,13000,4,1,8%,AMBER
...
```

**Android implementation**: Written to app's cache directory → shared via `FileProvider` intent → user selects share target (email, WhatsApp, Google Drive, etc.)
