<!--
  generated_from_feature: loan-detail
  generated_from_feature_version: "1.0.0"
  contract_version: "2.0.0"
  source_siblings: [ui.yaml, api.yaml, docs.yaml, flow.yaml, tests.yaml]
  generated_by: /idea-feature-export-spec
  status: approved (quality_score 87)
-->

# Loan Detail — Feature Spec

## Overview

Full detail view for a single loan. Displays member identity, disbursement info, interest
rate, total outstanding, and overdue amount, then two tabs: **Schedule** (weekly repayment
table) and **Repayment History** (recorded transactions). A treasurer may record a repayment;
a chairperson may mark the loan defaulted. Loads from the local SQLDelight cache
(stale-while-revalidate, TTL 120 s) then refreshes from Fineract `m_loan` through the companion
API; `cmp-network-monitor` gates offline fallback. The response is split into header summary,
weekly `RepaymentScheduleRow` rows, and `RepaymentTransaction` history, re-cached via Store5.

**Route:** `/loans/{loanId}` · **Entry:** `loan-list` (loan card tap)
**Nav params:** `loanId: Long (required)`

**Acceptance Criteria:**

- AC1: On mount, load loan detail + repayment schedule + history from `LoanRepository`;
       Loading → Content.
- AC2: Default tab is `SCHEDULE`; `OnTabChange` is a pure transform switching `selectedTab`
       (data already loaded, no network).
- AC3: `Record Repayment` button visible only when `canRecordRepayment && loan.status == ACTIVE`.
- AC4: `Mark Defaulted` button visible only when `canMarkDefaulted && loan.status == OVERDUE`.
- AC5: `OnRefresh` / top-bar refresh re-fetches network-first and re-caches via Store5.
- AC6: Offline stale-while-revalidate serves cached detail; 404 → NotFound (no retry);
       401 → Auth redirect login.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| loan-detail-screen | `LoanDetailScreen` | Detail, tabbed | Tabbed detail screen with schedule and repayment history |

## State Model

### LoanDetailViewModel

**State — `LoanDetailState`**

| Field | Type | Default | Description |
|---|---|---|---|
| isLoading | Boolean | `true` | Load in flight |
| loan | LoanDetail? | `null` | Loan header/summary |
| repaymentSchedule | List<RepaymentScheduleRow> | `emptyList()` | Weekly schedule rows |
| repaymentHistory | List<RepaymentTransaction> | `emptyList()` | Recorded transactions |
| selectedTab | LoanDetailTab | `LoanDetailTab.SCHEDULE` | Active tab |
| error | LoanDetailError? | `null` | Error state |
| isRecordingRepayment | Boolean | `false` | Repayment dialog in flight |
| canRecordRepayment | Boolean | `false` | Treasurer role gate |
| canMarkDefaulted | Boolean | `false` | Chairperson role gate |

**Screen States — `LoanDetailScreenState`**: `Loading`, `Content`, `Error`

| State | Components |
|---|---|
| `Loading` | top_bar, shimmer_detail |
| `Content` | top_bar, member_header_card, outstanding_summary_row, detail_tabs, schedule_table, history_list, action_buttons_row |
| `Error` | top_bar, error_state |

**Errors — `LoanDetailError`**

| Type | Retry | Message Key | Notes |
|---|---|---|---|
| Network | yes | error_network | Offline — shows cached |
| Server | yes | error_server | 5xx |
| NotFound | no | error_not_found | 404 |
| Auth | no | error_auth | 401 → redirect login |

**Actions — `LoanDetailAction`**

| Action | Params | Trigger | Effect |
|---|---|---|---|
| `OnTabChange` | tab: LoanDetailTab | Tap tab | transform_state — switch selectedTab |
| `OnRecordRepayment` | — | Tap Record Repayment | call_api — opens loan-repayment-dialog, recordRepayment via Store5 |
| `OnMarkDefaulted` | — | Tap Mark Defaulted | call_api — opens loan-mark-defaulted-dialog, markDefaulted via Store5 |
| `OnBack` | — | Tap back / nav icon | navigate — pop to loan-list |
| `Retry` | — | Tap retry on error | call_api — re-fetch getLoanDetail |
| `OnRefresh` | — | Pull to refresh / top-bar refresh | call_api — network-first re-fetch, re-cache |

**Events — `LoanDetailEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateBack` | — | `OnBack` |
| `ShowRepaymentDialog` | — | `OnRecordRepayment` |
| `ShowDefaultConfirmDialog` | — | `OnMarkDefaulted` |
| `ShowSnackbar` | message: String | Errors |

**DI Dependencies**

- `LoanRepository` — getLoanDetail, recordRepayment, markDefaulted
- `NetworkMonitor` (cmp-network-monitor)
- `SessionManager`

## Navigation

| Condition | Destination | Params |
|---|---|---|
| `OnBack` | `loan-list` | — |
| `OnRecordRepayment` | `loan-repayment-dialog` (dialog) | loanId |
| `OnMarkDefaulted` | `loan-mark-defaulted-dialog` (dialog) | loanId |

**navigates_to:** `loan-list`

## API Endpoints (1)

| ID | Method | Endpoint | Cache | Writable |
|---|---|---|---|---|
| `get_loan_detail` | GET | `/loans/{loanId}` | 120 s stale-while-revalidate, offline show_cached | no |

Repository also exposes `recordRepayment` and `markDefaulted` write paths (see repayment /
mark-defaulted dialog features). See `exports/loan-detail/API.md`.

## Flow Logic

| Trigger | Steps |
|---|---|
| `on_load` | fetch_loan_detail (get_loan_detail) → on_success show_content / on_error show_error / offline show_cached_data |
| `on_tab_change` | update_selected_tab (data already loaded) |
| `on_record_repayment` | show_repayment_dialog (guard: canRecordRepayment / treasurer) |
| `on_mark_defaulted` | show_confirm_dialog (guard: canMarkDefaulted / chairperson) |
| `on_refresh` | fetch_loan_detail (invalidate_cache: true) |

## Dependencies

- **Features:** `loan-list` (entry/back), `loan-repayment-dialog`, `loan-mark-defaulted-dialog`
- **Libraries:** `cmp-network-monitor`; external: SQLDelight, Store5
- **Local DB tables:** loans, loan_repayments

## DTOs

See `exports/loan-detail/API.md`. Key types: `LoanDetail`, `RepaymentScheduleRow`,
`RepaymentRowStatus` (PAID, PARTIAL, UPCOMING, OVERDUE), `RepaymentTransaction`,
`LoanDetailTab` (SCHEDULE, HISTORY).

## Testing (14 scenarios)

| ID | Priority | Scenario |
|---|---|---|
| TC-LD-001 | P0 | On mount, detail + schedule + history load from LoanRepository |
| TC-LD-002 | P0 | Default tab SCHEDULE; tapping HISTORY switches selectedTab |
| TC-LD-003 | P0 | Record Repayment button visible only when canRecordRepayment |
| TC-LD-004 | P0 | OnRecordRepayment emits ShowRepaymentDialog |
| TC-LD-005 | P1 | Mark Defaulted button visible only when canMarkDefaulted |
| TC-LD-006 | P1 | OnMarkDefaulted emits ShowDefaultConfirmDialog |
| TC-LD-007 | P0 | Schedule shows installment rows with due date/amount/status |
| TC-LD-008 | P1 | Error state shows retry on network/server failure |
| TC-LD-009 | P1 | OnRetry re-fetches loan detail |
| TC-LD-010 | P1 | Pull-to-refresh reloads without full-screen shimmer |
| TC-LD-011 | P1 | 404 → NotFound (no retry) |
| TC-LD-012 | P0 | 401 → Auth redirect login |
| TC-LD-013 | P1 | top_bar refresh re-fetches network-first, re-caches via Store5 |
| TC-LD-014 | P1 | Offline stale-while-revalidate serves cached detail |

Coverage targets: ViewModel 90%+, Screen 80%+, Repository 85%+.

## Designed UX Reference

- **Stitch prompts:** `idea-layer/screens/loan-detail/prompts/`
- **Preview HTML:** `idea-layer/screens/loan-detail/preview/`
- **Design conformance:** `member_header_card` (primaryContainer) carries member name, product,
  principal, disbursed date, interest rate, and a color-coded status badge (ACTIVE green /
  OVERDUE red / CLOSED grey). `outstanding_summary_row` shows an Outstanding chip plus an Overdue
  chip that turns errorContainer when `loan.totalOverdue > 0`. `detail_tabs` toggle between a
  color-coded `schedule_table` (PAID/PARTIAL/OVERDUE/UPCOMING row styles) and the `history_list`.
  Action buttons are role- and status-gated (primary Record Repayment, error-styled Mark Defaulted).
