# Group Management — API Contract

> **Companion API note (global self-signup pivot, 2026-07-17):** Group orchestration ops that require
> back-office privileges (create group, activate, associate clients, assign roles, assign staff) are
> implemented as **COMP-GRP-001..005** tools in mcp-mifosx (`go/tools/companion_groups.go`). The
> companion layer executes these with a service credential on behalf of the self-signed-up organizer.
> Calendar + collection-sheet tooling is **COMP-CAL-001..003** (`go/tools/companion_calendar.go`).
> These tools require the companion API to be deployed before use.
> Build spec: `server-layer/COMPANION_API_BUILD_DEPLOY.md §1a (TIER-1)`

## Companion API Endpoints (group orchestration — mcp-mifosx)

| Contract | Method | Path |
|----------|--------|------|
| COMP-GRP-001 | POST/GET | `/companion/groups*` |
| COMP-GRP-002 | POST | `/companion/groups/{id}/activate` |
| COMP-GRP-003 | POST | `/companion/groups/{id}/associate-clients` |
| COMP-GRP-004 | POST | `/companion/groups/{id}/assign-role` |
| COMP-GRP-005 | POST | `/companion/groups/{id}/assign-staff` |
| COMP-CAL-001 | POST | `/companion/groups/{id}/calendar` |
| COMP-CAL-002 | GET | `/companion/groups/{id}/collection-sheet` |
| COMP-CAL-003 | POST | `/companion/groups/{id}/collection-sheet` (save) |

## Fineract Direct Endpoints

## Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /centers | List all Fineract Centers managed by the logged-in staff member | Bearer token (staffId param from session) |
| GET | /centers/{centerId} | Fetch a single Center (group) by ID | Bearer token |
| GET | /centers/{centerId}/accounts | Fetch savings and loan accounts linked to the group | Bearer token |
| GET | /datatables/dt_group_corpus/{centerId} | Fetch real-time corpus fund balance from custom datatable | Bearer token |
| GET | /datatables/dt_group_config/{centerId} | Fetch group configuration rules | Bearer token |
| GET | /offices | Fetch list of offices for the office dropdown during group creation | Bearer token |
| POST | /centers | Create a new Fineract Center (savings group) | Bearer token |
| POST | /datatables/dt_group_config/{centerId} | Write group rules to the dt_group_config custom datatable | Bearer token |

---

## Request / Response Details

### get_centers

**Request**
```
GET /centers
Query params:
  staffId: Long (optional, sourced from session)
  paged: Boolean = true
  limit: Int = 20
  offset: Int = 0
```

**Response**
```json
{
  "totalFilteredRecords": 3,
  "pageItems": [
    {
      "id": 101,
      "name": "Mwangaza Women's Group",
      "status": { "id": 300, "value": "Active" },
      "activationDate": [2026, 1, 15],
      "meetingSchedule": "Weekly on Monday",
      "staffId": 42,
      "officeId": 1
    }
  ]
}
```

**Errors**
- 401: Unauthorized — redirect to login
- 403: Forbidden — insufficient permissions
- 500: Server error — show retry snackbar

**Cache**: TTL 300s, stale-while-revalidate, offline shows cached

---

### get_center

**Request**
```
GET /centers/{centerId}
Path params:
  centerId: Long (required, from nav params)
```

**Response**
```json
{
  "id": 101,
  "name": "Mwangaza Women's Group",
  "status": { "id": 300, "value": "Active" },
  "activationDate": [2026, 1, 15],
  "staffId": 42,
  "officeId": 1,
  "meetingSchedule": "Weekly on Monday"
}
```

**Errors**: 401, 403, 404 (group not found), 500

**Cache**: TTL 300s, stale-while-revalidate

---

### get_center_accounts

**Request**
```
GET /centers/{centerId}/accounts
Path params:
  centerId: Long (required)
```

**Response**
```json
{
  "savingsAccounts": [
    {
      "id": 201,
      "productName": "Group Savings",
      "accountBalance": 52500.00,
      "status": { "id": 300, "value": "Active" }
    }
  ],
  "loanAccounts": [
    {
      "id": 301,
      "productName": "Group Loan",
      "loanBalance": 5000.00,
      "status": { "id": 300, "value": "Active" }
    }
  ]
}
```

**Errors**: 401, 404, 500

**Cache**: TTL 180s, stale-while-revalidate

---

### get_group_corpus

**Request**
```
GET /datatables/dt_group_corpus/{centerId}
Path params:
  centerId: Long (required)
```

**Response**
```json
{
  "currentBalance": 47500.00,
  "openingBalance": 0.00,
  "totalContributionsThisCycle": 52500.00,
  "totalLoansOutstanding": 5000.00,
  "lastUpdated": "2026-04-28"
}
```

**Errors**: 401, 404 (show zero balance), 500

**Cache**: TTL 60s, network-first (real-time balance is critical for disbursement gate FR-018)

---

### get_group_config

**Request**
```
GET /datatables/dt_group_config/{centerId}
Path params:
  centerId: Long (required)
```

**Response**
```json
{
  "contributionMin": 100.00,
  "contributionMax": 500.00,
  "loanMultiplier": 3.0,
  "interestRate": 10.0,
  "cycleLengthMonths": 12,
  "fineAmount": 50.00,
  "minimumDisbursementThreshold": 5000.00
}
```

**Errors**: 401, 404, 500

**Cache**: TTL 600s, stale-while-revalidate

---

### get_offices

**Request**
```
GET /offices
Query params:
  orderBy: String = "name"
```

**Response**
```json
[
  { "id": 1, "name": "Nairobi Head Office", "nameDecorated": ". Nairobi Head Office", "externalId": "NBO-001" }
]
```

**Errors**: 401, 500

**Cache**: TTL 3600s, stale-while-revalidate

---

### create_center

**Request**
```
POST /centers
Body (application/json):
{
  "name": "Mwangaza Women's Group",
  "officeId": 1,
  "staffId": 42,
  "active": true,
  "activationDate": "15 May 2026",
  "locale": "en",
  "dateFormat": "dd MMMM yyyy",
  "meetingFrequency": "1",
  "meetingDay": "MO"
}
```

**Response**
```json
{ "resourceId": 101, "groupId": 101 }
```

**Errors**
- 400: Validation error (invalid fields — surfaced inline per field)
- 401: Unauthorized
- 403: Forbidden
- 500: Server error

**Offline Queue**: table `sync_queue`, operation `CREATE_GROUP`. Payload includes full body JSON. Retried with exponential backoff on reconnect.

---

### create_group_config

**Request**
```
POST /datatables/dt_group_config/{centerId}
Path params:
  centerId: Long (from create_center response.resourceId)
Body (application/json):
{
  "contribution_min": 100.00,
  "contribution_max": 500.00,
  "loan_multiplier": 3.0,
  "interest_rate": 10.0,
  "cycle_length_months": 12,
  "fine_amount": 50.00
}
```

**Response**
```json
{ "resourceId": 201 }
```

**Errors**: 400, 401, 500

**Offline Queue**: table `sync_queue`, operation `CREATE_GROUP_CONFIG`. Chained after `CREATE_GROUP` completes.

---

## DTOs

### Group
| Field | Type | Notes |
|-------|------|-------|
| id | String | Internal app ID |
| fineractCenterId | Long | Maps to Fineract Center.id |
| name | String | Display name |
| cycleNumber | Int | Current cycle (1-based) |
| cycleLengthMonths | Int | From dt_group_config |
| meetingFrequency | String | "Weekly", "Bi-weekly", "Monthly" |
| memberCount | Int | Derived from members API |
| overdueLoansCount | Int | Computed from loanAccounts |
| status | String | "Active", "Inactive" |

### GroupCorpus
| Field | Type | Notes |
|-------|------|-------|
| currentBalance | Double | KES — real-time fund balance (FR-018 gate) |
| openingBalance | Double | KES — balance at cycle start |
| totalContributionsThisCycle | Double | KES — cumulative deposits this cycle |
| totalLoansOutstanding | Double | KES — total undisbursed loan principal |
| lastUpdated | String | ISO date string |

### GroupConfig
| Field | Type | Notes |
|-------|------|-------|
| contributionMin | Double | Minimum KES per meeting (FR-020 penalty trigger) |
| contributionMax | Double | Maximum KES per meeting |
| loanMultiplier | Double | Member can borrow up to X × their total savings |
| interestRate | Double | Flat interest rate per loan cycle (%) |
| cycleLengthMonths | Int | Total months in one savings cycle |
| fineAmount | Double | KES penalty for missing minimum contribution |
| minimumDisbursementThreshold | Double | KES — corpus must exceed this to disburse a loan |

### GroupAccounts
| Field | Type | Notes |
|-------|------|-------|
| savingsBalance | Double | Total group savings balance KES |
| loansOutstanding | Double | Total active loan principal KES |
| activeLoanCount | Int | Count of open loan accounts |

### CreateGroupRequest
| Field | Type | Notes |
|-------|------|-------|
| name | String | 3–60 chars |
| officeId | Long | Selected office |
| staffId | Long | From session |
| active | Boolean | true at creation |
| activationDate | String | dd MMMM yyyy |
| meetingDay | String | Day of week |
| meetingTime | String | HH:mm |
| contributionMin | Double | KES |
| contributionMax | Double | KES |
| loanMultiplier | Double | Multiplier (1–10) |
| interestRate | Double | Flat % (0–100) |
| cycleLengthMonths | Int | 1–60 months |
| fineAmount | Double | KES late penalty |
| currency | String | Default "KES" |

### ActivityItem
| Field | Type | Notes |
|-------|------|-------|
| id | String | Unique event ID |
| type | String | MEETING, DEPOSIT, LOAN, PENALTY, SHARE_OUT |
| description | String | Human-readable event text |
| amount | Double? | KES amount (optional) |
| date | String | ISO date string |
| memberName | String? | Associated member name (optional) |

### HealthIndicator
| Value | Condition |
|-------|-----------|
| GREEN | overdueRate < 0.05 (less than 5% of loans overdue) |
| AMBER | overdueRate >= 0.05 && overdueRate < 0.20 |
| RED | overdueRate >= 0.20 (20% or more loans overdue) |
