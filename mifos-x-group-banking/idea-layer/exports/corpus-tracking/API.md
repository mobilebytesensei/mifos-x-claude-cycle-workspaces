# API — corpus-tracking
# MifosSave (mifos-x-group-banking) | Feature FR-018
# Generated: 2026-05-06

---

## Endpoints Table

| Method | Path | Description | Auth | Cache Strategy |
|--------|------|-------------|------|---------------|
| GET | /fineract-provider/api/v1/groups/{groupId} | Fetch group data | BasicAuth | stale-while-revalidate, TTL 300s |
| GET | /fineract-provider/api/v1/groups/{groupId}/accounts | Fetch savings and loan accounts linked to group | BasicAuth | stale-while-revalidate, TTL 180s |
| GET | /fineract-provider/api/v1/datatables/dt_group_corpus/{groupId} | Fetch real-time corpus balance from custom datatable | BasicAuth | network-first, TTL 60s |
| GET | /fineract-provider/api/v1/datatables/dt_group_config/{groupId} | Fetch group rules including minimumDisbursementThreshold | BasicAuth | stale-while-revalidate, TTL 600s |
| PUT | /fineract-provider/api/v1/datatables/dt_group_corpus/{groupId} | Update corpus to closingCorpus after meeting | BasicAuth | no cache (write) |

---

## Request/Response Details

### GET /groups/{groupId}
**Path params:** groupId (Long — from nav params)
**Response:** Group object (subset shown below)
**Cache:** TTL 300s, stale-while-revalidate, offline: show_cached
**Error handling:** 401 → redirect login; 403 → forbidden error state; 404 → "Group not found" error; 500 → show cached

### GET /groups/{groupId}/accounts
**Path params:** groupId (Long)
**Response:** GroupAccountsResponse with savings and loan accounts arrays
**Cache:** TTL 180s, stale-while-revalidate, offline: show_cached
**Error handling:** 401 → redirect login; 404 → group accounts not found; 500 → show cached

### GET /datatables/dt_group_corpus/{groupId}
**Path params:** groupId (Long)
**Response:** CorpusRecord — currentBalance, openingBalance, totalContributionsThisCycle, totalLoansOutstanding, lastUpdated
**Cache:** TTL 60s, network-first (short TTL for real-time accuracy)
**Error handling:** 401 → redirect login; 404 → corpus record not found → show KES 0 balance with note; 500 → show cached with warning chip

### GET /datatables/dt_group_config/{groupId}
**Path params:** groupId (Long)
**Response:** GroupConfigRecord with all group rules
**Cache:** TTL 600s (config changes rarely)
**Error handling:** 404 → use defaults (contributionMin=100, contributionMax=500, minimumDisbursementThreshold=1000)

### PUT /datatables/dt_group_corpus/{groupId}
**Path params:** groupId (Long)
**Body:** UpdateCorpusRequest
**Response:** DataTableEntryResponse
**Error handling:** 400 → validation error, log and show snackbar; 5xx → queue to SyncQueue (highest priority = priority 1)

---

## DTOs

### GroupCorpus (from GET dt_group_corpus)
| Field | Type | Notes |
|-------|------|-------|
| currentBalance | Double | Current corpus balance in KES; primary KES display value |
| openingBalance | Double | Balance at start of current cycle (KES 0 at cycle start) |
| totalContributionsThisCycle | Double | Cumulative group savings deposited into corpus |
| totalLoansOutstanding | Double | Sum of all outstanding loan principal |
| lastUpdated | String | Date of last update: "dd MMMM yyyy" |

**Demo data (GroupDashboard):**
- currentBalance: 47,500.00 (KES)
- openingBalance: 0.00 (cycle just started)
- totalContributionsThisCycle: 52,500.00 (all savings ever deposited)
- totalLoansOutstanding: 5,000.00 (active loans)
- lastUpdated: "07 May 2026" (after Meeting #4)

### GroupConfig (from GET dt_group_config)
| Field | Type | Notes |
|-------|------|-------|
| contributionMin | Double | Minimum KES per member per meeting — 100.00 (group-dashboard demo shows 100-500 range) |
| contributionMax | Double | Maximum KES per member per meeting — 500.00 |
| loanMultiplier | Double | Max loan = member_savings × loanMultiplier — 3.0 |
| interestRate | Double | Annual interest rate — 10.0% |
| cycleLengthMonths | Int | 12 |
| fineAmount | Double | Per-meeting fine for late/absent — 50.00 |
| minimumDisbursementThreshold | Double | Corpus must be >= this to disburse loans — 5,000.00 |

### Group (from GET /groups/{groupId})
| Field | Type | Notes |
|-------|------|-------|
| id | String | Fineract group ID |
| name | String | "Mwangaza Women's Group" |
| cycleNumber | Int | 1 (first cycle) |
| cycleLengthMonths | Int | 12 |
| meetingFrequency | String | "Weekly" |
| memberCount | Int | 5 |
| overdueLoansCount | Int | 0 (no overdue loans in demo) |
| status | String | "ACTIVE" |

### GroupAccounts (computed from /groups/{groupId}/accounts)
| Field | Type | Notes |
|-------|------|-------|
| savingsBalance | Double | Total savings account balance — KES 52,500 |
| loansOutstanding | Double | Total outstanding loan balance — KES 5,000 |
| activeLoanCount | Int | Number of active loans — 1 |

### ActivityItem (app-level entity for recent activity feed)
| Field | Type | Values |
|-------|------|--------|
| id | String | |
| type | String | MEETING, DEPOSIT, LOAN, PENALTY, SHARE_OUT |
| description | String | Human-readable e.g. "Meeting #4 conducted" |
| amount | Double? | KES amount if applicable |
| date | String | Display date |
| memberName | String? | Member name if applicable |

### UpdateCorpusRequest (PUT body)
| Field | Type | Notes |
|-------|------|-------|
| corpusBalance | Long | closingCorpus from wizard — e.g. 12,450 |
| lastUpdatedMeeting | Int | meetingNumber — e.g. 4 |
| lastUpdatedDate | String | today: "07 May 2026" |
| locale | String | "en" |
| dateFormat | String | "dd MMMM yyyy" |

### DataTableEntryResponse (PUT response)
| Field | Type | Notes |
|-------|------|-------|
| resourceId | Long | Updated datatable row ID |
| resourceIdentifier | String | Echo of groupId as string |

### GroupAccountsResponse (GET /groups/{groupId}/accounts)
| Field | Type | Notes |
|-------|------|-------|
| savingsAccounts | List\<SavingsAccountItem\> | All savings accounts |
| loanAccounts | List\<LoanAccountItem\> | All loan accounts |

### SavingsAccountItem
| Field | Type |
|-------|------|
| id | Long |
| productName | String |
| accountBalance | Double |
| status.id | Int |
| status.value | String |

### LoanAccountItem
| Field | Type |
|-------|------|
| id | Long |
| productName | String |
| loanBalance | Double |
| status.id | Int |
| status.value | String |
