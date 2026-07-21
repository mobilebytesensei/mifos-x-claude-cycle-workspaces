<!--
  generated_from_feature: loan-list
  generated_from_feature_version: "1.0.0"
  contract_version: "2.0.0"
  source_siblings: [ui.yaml, api.yaml, docs.yaml, flow.yaml, tests.yaml]
  generated_by: /idea-feature-export-spec
  status: approved (quality_score 88)
-->

# Loan List — Feature Spec

## Overview

Paginated list of all loans in the selected savings group. Each card shows member name, loan
amount, outstanding balance, a color-coded status badge, next repayment date, and a red overdue
indicator when applicable. Chairperson and treasurer may apply for a new loan via the FAB. A
Store5 stream sources loans from the SQLDelight `loans` cache first, then background-refreshes
paginated pages from the Fineract companion API; `cmp-network-monitor` gates the refresh so
offline shows cached rows. Status-filter chips and next-page loads transform the in-memory list
without a network call.

**Route:** `/groups/{groupId}/loans` · **Entry:** `group-dashboard` (Loans), bottom_nav (when group_selected)
**Nav params:** `groupId: Long (required)`

**Acceptance Criteria:**

- AC1: On mount, fetch first page (limit 20, offset 0); Loading → Content (or Empty).
- AC2: Filter chips (ALL/ACTIVE/OVERDUE/CLOSED) recompute `filteredLoans` client-side; no API call.
- AC3: Tapping a `loan_card` emits `NavigateToLoanDetail(loanId)`.
- AC4: FAB visible only when `canApplyLoan`; emits `NavigateToLoanApply(groupId)`.
- AC5: `OnLoadNextPage` appends the next 20-row page (offset increment); halts on empty page.
- AC6: Pull-to-refresh resets to offset 0 and re-fetches network-first; offline serves cached rows.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| loan-list-screen | `LoanListScreen` | List, paginated | Filterable, paginated list of loans with FAB for new application |

## State Model

### LoanListViewModel

**State — `LoanListState`**

| Field | Type | Default | Description |
|---|---|---|---|
| isLoading | Boolean | `true` | Initial load in flight |
| loans | List<LoanSummary> | `emptyList()` | All loaded loans |
| selectedFilter | LoanStatusFilter | `LoanStatusFilter.ALL` | Active status filter |
| filteredLoans | List<LoanSummary> | `emptyList()` | Filtered view of loans |
| isRefreshing | Boolean | `false` | Pull-to-refresh in flight |
| error | LoanListError? | `null` | Error state |
| groupId | Long | `0L` | Current group |
| canApplyLoan | Boolean | `false` | FAB role gate |

**Screen States — `LoanListScreenState`**: `Loading`, `Content`, `Error`, `Empty`

| State | Components |
|---|---|
| `Loading` | top_bar, filter_chips_row, shimmer_list |
| `Content` | top_bar, filter_chips_row, loan_card, apply_loan_fab |
| `Empty` | top_bar, filter_chips_row, empty_state, apply_loan_fab |
| `Error` | top_bar, error_state |

**Errors — `LoanListError`**

| Type | Retry | Message Key | Notes |
|---|---|---|---|
| Network | yes | error_network | Offline — shows cached |
| Server | yes | error_server | 5xx |
| Auth | no | error_auth | 401 → redirect login |

**Actions — `LoanListAction`**

| Action | Params | Trigger | Effect |
|---|---|---|---|
| `OnLoanClick` | loanId: Long | Tap loan card | navigate — to loan-detail |
| `OnFilterChange` | filter: LoanStatusFilter | Tap filter chip | transform_state — recompute filteredLoans |
| `OnApplyLoan` | — | Tap FAB | navigate — to loan-apply |
| `OnRefresh` | — | Pull to refresh | call_api — network-first re-fetch offset 0 |
| `Retry` | — | Tap retry on error | call_api — re-trigger Store5 stream fresh=true |
| `OnLoadNextPage` | — | Scroll to list end | call_api — next page (offset increment) |
| `OnBack` | — | Tap nav icon | navigate — pop to group-dashboard |

**Events — `LoanListEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToLoanDetail` | loanId: Long | `OnLoanClick` |
| `NavigateToLoanApply` | groupId: Long | `OnApplyLoan` |
| `ShowSnackbar` | message: String | Errors |

**DI Dependencies**

- `LoanRepository` — getGroupLoans, getLoansByStatus
- `NetworkMonitor` (cmp-network-monitor)
- `SessionManager`

## Navigation

| Condition | Destination | Params |
|---|---|---|
| `OnLoanClick` | `loan-detail` | `loanId` |
| `OnApplyLoan` | `loan-apply` | `groupId` |
| `OnBack` | `group-dashboard` | — |

**navigates_to:** `loan-apply`, `loan-detail`

## API Endpoints (1)

| ID | Method | Endpoint | Cache | Writable |
|---|---|---|---|---|
| `get_group_loans` | GET | `/groups/{groupId}/loans` | 180 s stale-while-revalidate, offset pagination (page 20), offline show_cached | no |

See `exports/loan-list/API.md`.

## Flow Logic

| Trigger | Steps |
|---|---|
| `on_load` | fetch_loans (get_group_loans) → on_success show_content / on_empty show_empty / on_error show_error / offline show_cached_data |
| `on_filter_change` | filter_loans_locally (client-side by status, no API call) |
| `on_refresh` | fetch_loans (invalidate_cache: true) |
| `on_loan_click` | navigate loan-detail (params loanId) |
| `on_apply_loan` | navigate loan-apply (params groupId) |
| `on_load_next_page` | fetch_loans (pagination: increment_offset) |

## Dependencies

- **Features:** `group-dashboard` (entry), `loan-detail`, `loan-apply`
- **Libraries:** `cmp-network-monitor`; external: SQLDelight, Store5
- **Local DB tables:** loans (SQLDelight Loan entity)

## DTOs

See `exports/loan-list/API.md`. Key types: `LoanSummary`,
`LoanStatus` (ACTIVE, OVERDUE, CLOSED, PENDING, REJECTED),
`LoanStatusFilter` (ALL, ACTIVE, OVERDUE, CLOSED).

## Testing (18 scenarios)

| ID | Priority | Scenario |
|---|---|---|
| TC-LL-001 | P0 | Loading fetches first page → Content |
| TC-LL-002 | P1 | Empty state when no loans match |
| TC-LL-003 | P1 | Error state renders error_state with retry CTA |
| TC-LL-004 | P0 | Filter chips recompute filteredLoans client-side |
| TC-LL-005 | P1 | OVERDUE filter surfaces only overdue loans |
| TC-LL-006 | P0 | Tap loan_card emits NavigateToLoanDetail |
| TC-LL-007 | P0 | FAB navigates to loan-apply when canApplyLoan |
| TC-LL-008 | P1 | FAB hidden when canApplyLoan=false |
| TC-LL-009 | P1 | OnLoadNextPage appends next 20-row page (atomic replacePage) |
| TC-LL-010 | P2 | OnLoadNextPage halts on empty pageItems |
| TC-LL-011 | P1 | Pull-to-refresh resets offset 0, re-fetches network-first |
| TC-LL-012 | P1 | Retry re-triggers Store5 stream fresh=true |
| TC-LL-013 | P0 | Auth 401 redirects to login-signup |
| TC-LL-014 | P1 | 403 forbidden shows insufficient-permissions error |
| TC-LL-015 | P2 | 404 group-not-found shows empty state |
| TC-LL-016 | P1 | 500 server error shows retry |
| TC-LL-017 | P0 | Offline stale-while-revalidate serves cached loans |
| TC-LL-018 | P1 | loan_card conditional rows (next-repayment ACTIVE, overdue indicator isOverdue) |

Coverage targets: ViewModel 90%+, Screen 80%+, Repository 85%+.

## Designed UX Reference

- **Stitch prompts:** `idea-layer/screens/loan-list/prompts/`
- **Preview HTML:** `idea-layer/screens/loan-list/preview/`
- **Design conformance:** horizontal `filter_chips_row` (All/Active/Overdue/Closed) with the
  Overdue chip in errorContainer. Each `loan_card` (surface, 2dp elevation, 72dp min-touch)
  shows member avatar, name, amount, outstanding, a color-coded status badge (ACTIVE green /
  OVERDUE red / CLOSED grey / PENDING amber), a next-repayment line only for ACTIVE loans, and a
  bold red overdue indicator when `loan.isOverdue`. FAB (primary, 56dp) is bottom-end and shown
  only for chairperson/treasurer. `empty_state` and full-screen `error_state` cover the other states.
