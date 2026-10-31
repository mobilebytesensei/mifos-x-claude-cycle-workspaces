<!--
generated_by: /idea-feature-export
generated_at: 2026-10-27
feature_id: home
sources:
  - screens/home/api.yaml
  - screens/home/data-flow.yaml
-->

# API — Home

All calls go over the existing authenticated Ktor client (Basic auth + tenant from the live instance)
and are read through Store5 `NETWORK_WITH_CACHE` streams — every card shows cached figures with their age
when offline. Verified against the sandbox OpenAPI spec (Fineract 1.17.0-SNAPSHOT) and the gateway.

## Endpoints (10)

| id | Method · path | Permission | Used for |
|---|---|---|---|
| getBusinessDate | `GET businessdate/BUSINESS_DATE` | READ_BUSINESS_DATE | the date "today" means — never the device clock |
| getOwnUser | `GET users/{userId}` | own record | firstname, office, **staff link** (portfolio scope) |
| generateCollectionSheet | `POST collectionsheet?command=generateCollectionSheet` | READ_COLLECTIONSHEET | today's due clients + loans (a read despite POST) |
| getCheckerTasks | `GET makercheckers` | any *_CHECKER / CHECKER_SUPER_USER | checker inbox count |
| getLoansByStatus | `GET loans?status=100\|200\|300&offset&limit=200&orderBy=id&sortOrder=DESC` | READ_LOAN | approval / disbursal queues, active portfolio |
| getClientsByStatus | `GET clients?status=pending\|active&officeId&limit=1` | READ_CLIENT | counts via `totalFilteredRecords` |
| getPendingReschedules | `GET rescheduleloans?command=pending` | READ_RESCHEDULELOAN | reschedule count |
| getCentersWithCalendar | `GET centers/{id}?associations=collectionMeetingCalendar` | READ_CENTER + READ_CALENDAR | meetings today |
| getCountsByScope | `GET groups \| centers` | READ_GROUP / READ_CENTER | groups and centres in scope |
| getSavingsAccounts | `GET savingsaccounts?offset&limit=200` | READ_SAVINGSACCOUNT | savings balance per currency |

## Request — generateCollectionSheet

```json
{ "officeId": 1, "staffId": 1, "transactionDate": "26 October 2026",
  "dateFormat": "dd MMMM yyyy", "locale": "en" }
```

`staffId` only when the user is staff-linked.

## Paging + scope

- `GET loans` has **no loanOfficerId filter**. Pages of 200 are walked until `totalFilteredRecords` is
  covered (cap 2,000 rows); "own" is filtered client-side.
- Counts use `limit=1` and read `totalFilteredRecords` only.
- Money is grouped **per currency**, never summed across currencies.

## Read substrate

| Store (`@StoreProvider`) | Key | Value |
|---|---|---|
| `dashboardUser` | userId | `DashboardUser(id, firstname, officeId, officeName, staffId)` |
| `dashboardBusinessDate` | Unit | `yyyy-MM-dd` |
| `dashboardLoans` | status | `List<DashboardLoan>` (principal, outstanding, overdue, arrears, currency, officer, submitter) |
| `dashboardClientCount` | (officeId, status) | Int |
| `dashboardSavings` | Unit | `List<DashboardSavings>` |

Repository: `DashboardRepository` — `userStream`, `businessDateStream`, `loansStream(status)`,
`clientCountStream(officeId, status)`, `savingsStream`, all `asScreenStream(…, NETWORK_WITH_CACHE)`.

## Not used

| Endpoint | Why |
|---|---|
| `runreports/*` (Portfolio at Risk, Active Loans – Summary, FieldAgentStats, Aging) | BadSqlGrammarException on the PostgreSQL sandbox — figures are computed from core APIs |
| `centers?meetingDate=` | does not filter |
| `userdetails` | OAuth deployments only — 404 on the gateway |

## Error mapping

| Error | Behaviour |
|---|---|
| NoNetwork | card keeps cached figures with their age; if nothing is cached anywhere → screen error |
| ServerError | that card's own error banner + Retry |
| Forbidden | should never surface (gated cards are not subscribed) — treated as a card error |
| Unauthorized | the app's existing session-expiry path |
