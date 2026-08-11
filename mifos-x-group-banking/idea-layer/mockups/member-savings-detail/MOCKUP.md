# Member Savings Detail — Mockup Specification

**Feature**: member-savings-detail | **Route**: `/groups/{groupId}/members/{memberId}/savings` | **Type**: list
**Feature group**: savings-management | **Flow**: savings-management-flow
**Generated from**: `screens/member-savings-detail/ui.yaml`, `screens/member-savings-detail/demo-data.yaml`, `screens/member-savings-detail/preview/*.html` (4 states)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature member-savings-detail`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: MifosSave-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, avatar, sparkline line, active filter chip, retry button
**Primary container**: `#C8E6C9` (`--primary-100`) — member header card background, sparkline fill
**Accent**: `#FF8F00` (`--accent-700`, amber) — reserved for pooled-fund emphasis (not used on this screen)
**Success (deposit)**: `#1B5E20` — deposit arrow icon + `+ KES` amount text
**Danger (withdrawal)**: `#B71C1C` — withdrawal arrow icon + `- KES` amount text
**Muted / Reversed**: `#757575` on `#F5F5F5` — REVERSED badge on reversed transaction rows
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (shimmer, dividers, reversed badge)
**Corner radius**: 16dp header + sparkline cards · 12dp shimmer skeletons · 16px filter chips
**Elevation**: 0dp header card (primaryContainer fill carries hierarchy) · 2dp sparkline card
**Min touch target**: 72dp transaction row · 48dp filter chip · 48dp back arrow · 48dp retry CTA

---

## Screen: Member Savings

### Entry
- From **savings-dashboard** (tap on a member row); nav-params `memberId: String, groupId: String, typeConfig: GroupTypeConfig`
- From **member-profile** ("View full history" button); nav-params `memberId, groupId, typeConfig`
- Back navigation pops the route and returns to the previous screen in the back stack (`savings-dashboard` or `member-profile`)

### Layout (state: `content`, contribution model: `SHARE_BASED_VARIABLE` — VSLA/SILC)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹]  Member Savings          [#2E7D32]  │  TopAppBar — primary green, onPrimary text
│      Amina Wanjiru                       │  subtitle · {{member.displayName}}
├─────────────────────────────────────────┤
│ ┌───────────────────────────────────┐   │
│ │ ╭──╮                              │   │  member_header_card
│ │ │AW│  Amina Wanjiru               │   │  primaryContainer #C8E6C9 · elevation 0dp
│ │ ╰──╯  Shares Held                 │   │  corner 16dp · padding 16dp
│ │        20 shares @ KES 1000/share │   │  savings_balance_amount · displaySmall bold
│ │        = KES 20,000 total         │   │  savings_balance_total · titleMedium
│ │        Account: SA-00012345       │   │  account_no_text · bodySmall
│ └───────────────────────────────────┘   │
├─────────────────────────────────────────┤
│ ┌───────────────────────────────────┐   │
│ │ 6-Month Trend                     │   │  savings_sparkline_card
│ │                                    │   │  surface · elevation 2dp · corner 16dp
│ │      ╱‾‾╲    ╱‾‾‾‾╲               │   │  sparkline · line #2E7D32
│ │     ╱    ╲__╱      ╲___╱‾‾‾       │   │  fill #C8E6C9 · height 80dp
│ │   D  J  F  M  A  M                 │   │  x_key: date · y_key: balance
│ └───────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  [All*] [Deposits] [Withdrawals]  →     │  filter_chips_row · horizontal scroll
│                                          │  selected chip = primary #2E7D32 fill
├─────────────────────────────────────────┤
│  ┌───────────────────────────────┐      │
│  │ ↓  Deposit         + KES 300  │      │  transaction_card (TXN-1001)
│  │    2026-05-09    Balance: 6,000│      │  green ↓ icon · +KES amount success #1B5E20
│  └───────────────────────────────┘      │  min-touch 72dp · divider between rows
├─────────────────────────────────────────┤
│  ┌───────────────────────────────┐      │
│  │ ↓  Deposit         + KES 300  │      │  transaction_card (TXN-1002)
│  │    2026-05-02    Balance: 5,700│      │
│  └───────────────────────────────┘      │
├─────────────────────────────────────────┤
│  ┌───────────────────────────────┐      │
│  │ ↓  Deposit         + KES 300  │      │  transaction_card (TXN-1003)
│  │    2026-04-25    Balance: 5,400│      │
│  └───────────────────────────────┘      │
├─────────────────────────────────────────┤
│  ┌───────────────────────────────┐      │
│  │ ↑  Withdrawal      - KES 300  │      │  transaction_card (TXN-3007, WITHDRAWAL)
│  │    2026-03-22    Balance: 395.80│    │  red ↑ icon · -KES amount danger #B71C1C
│  └───────────────────────────────┘      │
├─────────────────────────────────────────┤
│  ┌───────────────────────────────┐      │
│  │ ↑  Withdrawal      - KES 100  │      │  transaction_card (TXN-3009 — reversed)
│  │    2026-02-14    Balance: 250 │      │
│  │                      [REVERSED]│      │  reversed_badge · surfaceVariant grey pill
│  └───────────────────────────────┘      │  visible_when transaction.reversed == true
├─────────────────────────────────────────┤
│  ┌───────────────────────────────┐      │
│  │ ⇗  Interest Posting  KES 4.20 │      │  transaction_card (TXN-3003, INTEREST)
│  │    2026-04-15    Balance: 700 │      │  trending_up icon · onSurfaceVariant tint
│  └───────────────────────────────┘      │
├─────────────────────────────────────────┤
│                 ◐ (loading more)         │  load_more_indicator · circular 32dp
│                                          │  visible_when isLoadingNextPage
│                    ↕ scroll              │  OnLoadMore triggers on end-reached
└─────────────────────────────────────────┘
```

### Demo Data (state: `content`, from `demo-data.yaml`)

Two `MemberSavingsDetailResponse` variants (contribution-model duality):

**Variant 1 — Peter Otieno (FIXED_AMOUNT — ROSCA/SHG)**

| Field              | Value                        |
|--------------------|------------------------------|
| memberId           | MBR-104                      |
| displayName        | Peter Otieno                 |
| savingsAccountNo   | SAV-104-2026                 |
| savingsBalance     | KES 1,500                    |
| sharesHeld         | null                         |
| shareValue         | null                         |
| totalTransactions  | 12                           |
| hasNextPage        | true                         |

**Variant 2 — Amina Wanjiru (SHARE_BASED_VARIABLE — VSLA)**

| Field              | Value                        |
|--------------------|------------------------------|
| memberId           | MBR-101                      |
| displayName        | Amina Wanjiru                |
| savingsAccountNo   | SAV-101-2026                 |
| savingsBalance     | KES 6,000 (equivalent)       |
| sharesHeld         | 20                           |
| shareValue         | 6,000                        |
| totalTransactions  | 20                           |
| hasNextPage        | true                         |

**Transactions (mixed type coverage — every filter chip yields non-empty results):**

| id       | Date       | Type              | Amount    | Balance    | Reversed |
|----------|------------|-------------------|-----------|------------|----------|
| TXN-3001 | 2026-05-06 | DEPOSIT           | +400.00   | 1,500.00   | false    |
| TXN-3002 | 2026-04-29 | DEPOSIT           | +400.00   | 1,100.00   | false    |
| TXN-3003 | 2026-04-15 | INTEREST_POSTING  |    4.20   | 700.00     | false    |
| TXN-3007 | 2026-03-22 | WITHDRAWAL        | -300.00   | 395.80     | false    |
| TXN-3006 | 2026-03-10 | FEE_DEDUCTION     |  -50.00   | 345.80     | false    |
| TXN-3009 | 2026-02-14 | WITHDRAWAL        | -100.00   | 250.00     | **true** |
| TXN-3011 | 2025-12-10 | DEPOSIT           | +150.00   | 100.00     | false    |

- **Filter distribution** — DEPOSIT 3, WITHDRAWAL 2, INTEREST_POSTING 1, FEE_DEDUCTION 1 → every `TransactionFilter` chip (All / Deposits / Withdrawals) renders a non-empty subset.
- **Reversed row (TXN-3009)** backs the `reversed_badge` `visible_when: transaction.reversed` binding — proves the badge renders in real data, not only in code.
- **Sparkline** — 7 monthly points (2025-11-01 → 2026-05-01), monotonic rise 100 → 1,500 KES for Peter (FIXED_AMOUNT), 0 → 6,000 KES for Amina (SHARE_BASED_VARIABLE).
- **Pagination** — Peter shows 5 rows of 12 (`hasNextPage: true`); Amina shows 3 rows of 20. `OnLoadMore` fires on scroll-end to fetch offset+20.

---

## States

The `ui.yaml` declares 4 `screen_state` members (`Loading`, `Content`, `Empty`, `Error`) — each renders as a distinct HTML preview surface under `preview/`.

### `loading`
Shimmer skeleton mirroring the content layout — parallel fetch of member profile and savings account from the companion API (Store5 stream, SQLDelight cache first, network revalidate).

```
[Member Savings header]                    ← top_bar visible with title (no subtitle yet)
──────────────────────────────────────────
[shimmer card ] ← 72dp × full width, corner 12dp, surfaceVariant
[shimmer card ]
[shimmer card ]   ← shimmer_list count: 6
[shimmer card ]
[shimmer card ]
[shimmer card ]
```

- Cards: 72dp × full width, corner 12dp, `surfaceVariant` background shimmering 1.4s ease-in-out infinite.
- Respects `prefers-reduced-motion: reduce` (animation disabled).
- Top bar retains title "Member Savings" (subtitle blank until member data arrives).
- Header card, sparkline card, and filter chips are NOT rendered during loading — the shimmer_list stands in for the whole scroll region.

### `content` (see layout above)
All member savings data loaded from Store5 stream — SQLDelight cache renders immediately, companion API revalidates in background. Chips filter the in-memory transaction list (no network call). Pull-to-refresh forces `fresh=true`. Infinite scroll paginates via `OnLoadMore` (offset+20).

**Contribution-model duality** — the `member_header_card` adapts:
- **SHARE_BASED_VARIABLE** (VSLA/SILC): label `Shares Held` → amount `20 shares @ KES 1000/share` → total `= KES 20,000 total` (three lines).
- **FIXED_AMOUNT / FIXED_NEGOTIATED** (ROSCA/SHG): label `Savings Balance` → amount `KES 1,500` (two lines; `savings_balance_total` hidden by `visible: false`).

### `empty`
No transactions match the selected filter (e.g. chip "Withdrawals" while the account has only deposits, or a fresh account with 0 posted transactions).

```
┌ Member Savings ────────────────────────┐
│      Amina Wanjiru                      │  subtitle preserved
├────────────────────────────────────────┤
│ [member_header_card retained]           │  header + sparkline still visible so the
│ [savings_sparkline_card retained]       │  user keeps context on WHOSE savings
├────────────────────────────────────────┤
│  [All] [Deposits] [Withdrawals*]        │  filter_chips_row retained
├────────────────────────────────────────┤
│                                          │
│               💼                         │  empty_state · icon account_balance_wallet
│         No transactions                  │  title · titleLarge
│    No transactions match                 │  body · bodyMedium, --text-secondary
│    the selected filter.                  │
│                                          │
└─────────────────────────────────────────┘
```

- Header + sparkline are RETAINED (not replaced) so the user still sees the account context; only the transaction rows collapse to the empty state.
- Illustration uses `account_balance_wallet` outlined icon at 64dp, `onSurfaceVariant` tint.
- Chip stays selected so switching back to `All` reveals rows without a re-fetch.

### `error`
Companion API failed AND cache is empty — retry surface. When cache HAS rows, the `Network` error surfaces as a non-blocking snackbar/toast ("No internet. Showing cached savings data.") and `content` stays visible.

```
┌ Member Savings ────────────────────────┐
│                                          │  (top_bar retained; header/sparkline
│                                          │   suppressed because no data at all)
├────────────────────────────────────────┤
│                                          │
│               ☁                          │  error_state · cloud_off icon
│      Could not load savings              │  title · titleLarge
│                                          │
│    {error.message}                       │  body · bodyMedium, --text-secondary
│    e.g. "No internet. Showing            │
│    cached savings data."                 │
│                                          │
│  ┌─────── Retry ──────────────────┐    │  cta_label · primary #2E7D32, 48dp
│  └────────────────────────────────┘    │  → Retry action_contract effect: call_api
│                                          │  fresh=true, resets offset, re-triggers
└─────────────────────────────────────────┘  Store5 stream
```

Error types (from `MemberSavingsError`):
- `Network` — retry:true, `error_network` "No internet. Showing cached savings data." (also used for the non-blocking toast when cache has rows).
- `Server` — retry:true, `error_server` "Server error. Please retry."
- `NotFound` — retry:false, `error_not_found` "Savings account not found."
- `Auth` — retry:false, `error_auth` "Session expired. Please log in again." → redirect to `login`.

---

## Interaction Patterns

1. **Back arrow tap** → `OnBack` (effect: `navigate`) → pops the route back to the previous screen (`savings-dashboard` or `member-profile`); no state persistence needed.
2. **Filter chip tap** → `OnFilterSelected(filter)` (effect: `transform_state`) → sets `selectedFilter` in `MemberSavingsDetailState` and recomputes the visible transaction subset in-memory (no network call). Chips reflect selection via `primary #2E7D32` fill on the selected chip; unselected chips render as outlined `surface`.
3. **Transaction row tap** → `OnTransactionSelected(transactionId)` (effect: `transform_state`) → expands the tapped `SavingsTransaction` row in-place to reveal its full receipt (transaction id, posting date, meeting reference, running balance, reversal status). No network call — all data is already in the `savings_transactions` cache. Row uses 72dp min touch target and full-row ripple.
4. **Pull to refresh** → `OnRefresh` (flow `invalidate_cache: true`, `isRefreshing = true`) → Store5 `fresh=true` reload against the companion API, keeps the selected filter chip, resets `currentOffset = 0`.
5. **Scroll to list end** → `OnLoadMore` → paginated companion API fetch (`offset += 20`); guarded by `hasNextPage == true && !isLoadingNextPage`; empty next page silently no-ops and sets `hasNextPage = false`. `load_more_indicator` renders as a 32dp circular progress under the last row while the request is in flight.
6. **Retry tap (error state)** → `Retry` (effect: `call_api`, external: `Store5`, guard: `cmp-network-monitor`) → Store5 stream with `fresh=true`, resets `currentOffset = 0`, invalidates SQLDelight `savings_transactions` cache, re-hits `GET /companion/groups/{groupId}/members/{memberId}/savings`.

---

## Accessibility

- Transaction row exposes a single semantic action ("Open {type} for {date}, KES {amount}, running balance KES {runningBalance}"); reversed rows append " — REVERSED" to the label.
- Transaction type is text + colored icon — never color-only (row headline always readable: "Deposit" / "Withdrawal" / "Interest Posting" / "Fee Deduction" / "Transfer").
- Amount sign is text + color (`+ KES` / `- KES` prefix) — screen readers announce direction regardless of color perception.
- `REVERSED` badge is a text pill (`surfaceVariant` fill) — never conveyed by strikethrough alone.
- Filter chips carry role `tab`; selected chip communicates state via ARIA `aria-selected="true"`.
- Sparkline card is decorative for accessibility purposes; the numerical trend is announced via a hidden text summary ("Balance rose from KES 100 in November to KES 1,500 in May").
- Min touch target 72dp on transaction rows, 48dp on filter chips, 48dp on back arrow, 48dp on Retry CTA.
- Contribution-model duality is announced: header reads "Shares Held: 20 shares at KES 1000 per share, total KES 20,000" for VSLA members and "Savings Balance: KES 1,500" for FIXED_AMOUNT members.
- Locales covered: English, Swahili (`Akiba ya Mwanachama` / `Amana` / `Toa`), French (`Épargne du Membre`), Hindi (`सदस्य की बचत`).
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS.

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- Sparkline draw-in: 400ms ease-out path animation on first render — disabled under `prefers-reduced-motion`.
- Row ripple: MD3 standard 300ms ease-out on tap.
- Filter chip selection: fill transition 150ms.
- Pull-to-refresh spinner: MD3 refresh indicator, matches primary `#2E7D32`.
- Load-more indicator: 32dp circular progress, fades in over 120ms when `isLoadingNextPage == true`.
- Snackbar (`ShowSnackbar` event): standard MD3 slide-up + auto-dismiss 4s (used for the cached-data fallback banner and for successful refresh confirmation).
- Row expansion (on `OnTransactionSelected`): MD3 expressive expand-collapse, 250ms ease-in-out.

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `Store5`, `SQLDelight`, `fineract-rest` (via companion API)
**Internal lib**: `cmp-network-monitor`

Read paths (offline-first):
- `member`, `savingsAccountNo`, `savingsBalance`, `sharesHeld`, `shareValue`, `sparklineData`, `transactions[]` ← `MemberRepository.getMemberSavings(groupId, memberId)` via Store5 stream
  - Source of truth: SQLDelight `savings_transactions` + `savings_account` caches
  - Fetcher: Companion API `GET /companion/groups/{groupId}/members/{memberId}/savings?limit=20&offset=…` which fronts Fineract `savingsaccounts/{id}/transactions`
  - `Retry` triggers `fresh=true`, `OnRefresh` triggers cache invalidation and offset reset
- `filteredTransactions[]` — derived state: `transactions.filter { selectedFilter matches (ALL | DEPOSIT | WITHDRAWAL) }` (client-side)
- `contributionModel`, `typeConfig` ← passed via nav-param from `savings-dashboard` / `member-profile` (drives header display duality)
- `hasNextPage` — derived from companion API response envelope; controls `OnLoadMore` guard
- Network status ← `NetworkMonitor.isOffline` (cmp-network-monitor) — gates fetcher, drives cache-fallback toast

Write path: none (this screen is read-only; deposits/withdrawals happen on `savings-deposit` and `savings-withdrawal` screens).

Offline behavior: when `NetworkMonitor.isOffline == true`, cache rows still render and `Network` error surfaces as a non-blocking snackbar/toast ("No internet. Showing cached savings data.") — the transaction list itself stays in `content` state. When cache is EMPTY and network is offline, the screen falls through to the `error` state with the same message.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/member-savings-detail/ui.yaml` |
| API contract | `idea-layer/screens/member-savings-detail/api.yaml` |
| Data flow | `idea-layer/screens/member-savings-detail/data-flow.yaml` |
| Demo data | `idea-layer/screens/member-savings-detail/demo-data.yaml` |
| Flow | `idea-layer/screens/member-savings-detail/flow.yaml` |
| Tests | `idea-layer/screens/member-savings-detail/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/member-savings-detail/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/member-savings-detail/preview/content.html` |
| Preview HTML (empty) | `idea-layer/screens/member-savings-detail/preview/empty.html` |
| Preview HTML (error) | `idea-layer/screens/member-savings-detail/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/member-savings-detail/prompts/{loading,content,empty,error}.md` |
| Stitch mockup (probe deferred) | `idea-layer/mockups/member-savings-detail/stitch/` |
| Feature-group mockup | `idea-layer/mockups/savings-management/MOCKUP.md` (Member Savings section) |
| Figma links | `idea-layer/mockups/member-savings-detail/FIGMA_LINKS.md` |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from the fresh ui.yaml (4 states) + demo-data.yaml (2 MemberSavingsDetailResponse variants covering both contribution models + 7 SavingsTransaction rows covering every TransactionType + one reversed row) + design-system tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- **Contribution-model duality is load-bearing**: the same screen renders VSLA members as "20 shares @ KES 1000/share = KES 20,000 total" (three-line header) and ROSCA/SHG members as "KES 1,500" (two-line header). This is driven by the nav-param `typeConfig: GroupTypeConfig` and the `contributionModel` state field. The `savings_balance_total` component is hidden via `visible: {{contributionModel == 'SHARE_BASED_VARIABLE'}}` for non-share models.
- **Reversed transaction is a design invariant** — TXN-3009 in demo-data.yaml carries `reversed: true` to prove the `reversed_badge` `visible_when` binding renders in real data. Any regeneration of demo-data.yaml MUST preserve at least one `reversed: true` row.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features member-savings-detail
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to ui.yaml components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
