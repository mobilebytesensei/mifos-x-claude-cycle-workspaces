# Member Savings Detail — Feature Spec

## Overview

Per-member savings drill-down screen showing header card (adapted by `contributionModel`),
a savings sparkline, filter chips (ALL / DEPOSITS / WITHDRAWALS — client-side only, no
API call), and a paginated transaction list. Shares-related fields (`sharesHeld`,
`shareValue`) are shown only for `SHARE_BASED_VARIABLE` groups.

**Acceptance Criteria:**

- AC1: Fetch `get_member_savings_detail` on mount (paginated: `limit=20, offset=0`;
       cache 120 s SWR).
- AC2: Header card adapts by `contributionModel`:
  - `SHARE_BASED_VARIABLE` → shows `sharesHeld` and `shareValue` fields
  - `FIXED_AMOUNT` / `FIXED_NEGOTIATED` → shows total deposits and total withdrawals only
- AC3: Filter chips (ALL / DEPOSITS / WITHDRAWALS) filter the locally-loaded transaction
       list — they do NOT trigger a new API call.
- AC4: Pagination: scroll to bottom → fetch next page (offset += 20); `append_to_existing`.
- AC5: Sparkline is rendered from `savingsDataPoints[]` returned by the initial fetch.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| member-savings-detail | `MemberSavingsDetailScreen` | Scrollable with sticky filter chips | Per-member savings header + transaction list |

## State Model

### MemberSavingsDetailViewModel

**State — `MemberSavingsDetailState`**

| Field | Type | Default | Description |
|---|---|---|---|
| groupId | String | `""` | From nav params |
| memberId | String | `""` | From nav params |
| memberName | String | `""` | From API response |
| contributionModel | String | `""` | SHARE_BASED_VARIABLE \| FIXED_AMOUNT \| FIXED_NEGOTIATED |
| totalSaved | Long | `0L` | KES total deposited |
| sharesHeld | Int? | `null` | SHARE_BASED_VARIABLE only |
| shareValue | Long? | `null` | SHARE_BASED_VARIABLE only — KES per share |
| totalWithdrawals | Long | `0L` | KES total withdrawn |
| sparklineData | List<SavingsDataPoint> | `emptyList()` | For chart |
| transactions | List<SavingsTransaction> | `emptyList()` | All loaded pages |
| filteredTransactions | List<SavingsTransaction> | `emptyList()` | Client-side filtered view |
| activeFilter | TransactionFilter | `ALL` | ALL \| DEPOSITS \| WITHDRAWALS |
| isLoading | Boolean | `true` | Initial load |
| isLoadingMore | Boolean | `false` | Pagination in progress |
| hasMore | Boolean | `false` | More pages available |
| error | String? | `null` | Error banner |

**Screen States**

| State | Components |
|---|---|
| `Loading` | Skeleton for header card + transaction list |
| `Content` | header_card (model-adaptive), sparkline_chart, filter_chips, transaction_list |
| `Error` | error_banner + retry_button |

**TransactionFilter Enum**

```
ALL, DEPOSITS, WITHDRAWALS
```

Client-side filter: `DEPOSITS` shows `transactionType == CREDIT`;
`WITHDRAWALS` shows `transactionType == DEBIT`.

**Actions — `MemberSavingsDetailAction`**

| Action | Trigger |
|---|---|
| `OnFilterSelect(filter)` | Tap filter chip |
| `OnLoadMore` | Scroll to list bottom |
| `OnRefresh` | Pull-to-refresh |
| `OnBack` | Back arrow |
| `OnRetry` | Retry on error |

**Events — `MemberSavingsDetailEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateBack` | — | `OnBack` |

**DI Dependencies**

- `SavingsRepository` — get_member_savings_detail

## Navigation

| Action | Destination |
|---|---|
| `OnBack` | `savings-dashboard` |

Entry from: `savings-dashboard` → GROUP tab member row tap.

## API Endpoints

| ID | Method | Endpoint | Companion Tool | Writable |
|---|---|---|---|---|
| `get_member_savings_detail` | GET | `/companion/groups/{groupId}/members/{memberId}/savings` | — | no |

## Data-Flow

**Tables**

| Table | PK | Mutation | Strategy |
|---|---|---|---|
| `member_savings_cache` | groupId:memberId | upsert | stale_while_revalidate 120 s |
| `savings_transactions` | transactionId | upsert | shared; `append_to_existing` on pagination; serve_stale offline |

**Sync Queue:** none.

**Client-side filter:** never triggers an API call. `filteredTransactions` is a derived
`State` computed from `transactions + activeFilter`.

## DTOs

See `exports/member-savings-detail/API.md` for full DTO schemas.

Key types: `MemberSavingsDetailResponse` (member, totalSaved, sharesHeld?, shareValue?,
totalWithdrawals, savingsDataPoints[], transactions, hasMore, totalCount),
`SavingsTransaction` (transactionId, transactionDate, amount, transactionType, description),
`TransactionType` (CREDIT, DEBIT), `SavingsDataPoint` (date, cumulativeAmount).

## Designed UX Reference

- **Stitch mockups:** `idea-layer/screens/member-savings-detail/prompts/`
- **Preview HTML:** `idea-layer/screens/member-savings-detail/preview/`
- **Design conformance:** Header card is tinted. For `SHARE_BASED_VARIABLE`, it shows two
  rows: "Shares Held: {N}" and "Share Value: KES {X}" below the total-saved amount.
  For other models it shows "Total Deposits" and "Total Withdrawals" as the two metric
  rows. Sparkline is a compact line chart with gradient fill below. Filter chips
  (ALL / Deposits / Withdrawals) are sticky below the sparkline — they scroll with content
  but freeze when the sparkline scrolls off. Transaction rows show date on left, description
  in center, and amount (green for deposits, red for withdrawals) on right.
