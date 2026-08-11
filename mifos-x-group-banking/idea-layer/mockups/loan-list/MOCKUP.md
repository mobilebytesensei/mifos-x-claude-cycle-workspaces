# Loan List — Mockup Specification

**Feature**: loan-list | **Route**: `/groups/{groupId}/loans` | **Type**: list
**Feature group**: loan-management | **Flow**: loan-management-flow
**Generated from**: `screens/loan-list/ui.yaml`, `screens/loan-list/demo-data.yaml`, `screens/loan-list/preview/*.html` (4 states rendered 2026-07-17)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature loan-list`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: MifosSave-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, FAB, back button, active filter chip
**Accent**: `#FF8F00` (`--accent-700`, amber) — pooled fund emphasis (not used on this screen)
**Success**: `#1B5E20` on `#C8E6C9` — ACTIVE status badges
**Warning**: `#E65100` on `#FFF9C4` — PENDING status badges
**Danger**: `#B71C1C` on `#FFCDD2` — OVERDUE badges + overdue indicator text
**Muted**: `#757575` on `#F5F5F5` — CLOSED badges
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (shimmer, closed badges)
**Corner radius**: 12dp cards + shimmer skeletons · 16px filter chips · full-round FAB
**Elevation**: 2dp loan cards · 6dp FAB
**Min touch target**: 72dp loan card · 48dp filter chip · 56dp FAB

---

## Screen: Group Loans

### Entry
- From **group-dashboard** ("Loans" section link); nav-param `groupId: Long`
- From **bottom_nav** "Loans" tab when a group is selected (`condition: group_selected`)
- Back navigation pops the route and returns to `group-dashboard`

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹]  Group Loans             [#2E7D32]  │  TopAppBar — primary green, onPrimary text
├─────────────────────────────────────────┤
│  [All*] [Active] [Overdue] [Closed]  →  │  filter_chips_row — horizontal scroll,
│                                          │  8dp / 16dp padding · selected = primaryContainer
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ [👤] Amina Wangari      [ACTIVE] │   │  loan_card · elevation 2dp, corner 12dp
│  │      KES 8,000            green  │   │  memberName · titleMedium, onSurface
│  │      Outstanding: KES 5,600      │   │  principalAmount · bodyMedium, onSurfaceVariant
│  │      Next: 2026-07-25            │   │  outstandingBalance · bodySmall
│  └──────────────────────────────────┘   │  nextRepaymentDate visible_when status==ACTIVE
│                                          │  → on_click OnLoanClick → loan-detail(5001)
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ [👤] Joseph Otieno    [OVERDUE ] │   │  overdue → status_badge red pill
│  │      KES 12,000           red    │   │
│  │      Outstanding: KES 9,600      │   │
│  │      Next: 2026-07-18            │   │
│  │      OVERDUE — KES 600           │   │  overdue_indicator · labelSmall,
│  └──────────────────────────────────┘   │  error color, bold; visible_when isOverdue
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ [👤] Grace Wanjiku      [ACTIVE] │   │
│  │      KES 5,000           green   │   │
│  │      Outstanding: KES 3,000      │   │
│  │      Next: 2026-07-25            │   │
│  └──────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ [👤] Peter Kamau        [CLOSED] │   │  CLOSED — surfaceVariant badge #F5F5F5
│  │      KES 6,000            grey   │   │  next_repayment_text hidden
│  │      Outstanding: KES 0          │   │
│  └──────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ [👤] Mary Achieng       [ACTIVE] │   │  (rows continue 5005…5012 scroll)
│  │      KES 4,000           green   │   │
│  │      Outstanding: KES 2,800      │   │
│  │      Next: 2026-07-25            │   │
│  └──────────────────────────────────┘   │
│              ↕ scroll                    │  page_size 20 · OnLoadNextPage on end-reached
├─────────────────────────────────────────┤
│                          ┌──[ + Apply ]─│  apply_loan_fab · primary #2E7D32,
│                          │              │  56dp, bottom_end, visible_when canApplyLoan
│                          └──────────────│  → on_click OnApplyLoan → loan-apply(groupId)
└─────────────────────────────────────────┘
```

### Demo Data (state: `content`, from `demo-data.yaml`)

Twelve loans in Mwangaza Women's Group (Kisumu West Branch, KES, weekly repayment):

| id   | Member          | Principal | Outstanding | Overdue | Status  | Next Repayment |
|------|-----------------|-----------|-------------|---------|---------|----------------|
| 5001 | Amina Wangari   | 8,000     | 5,600       | 0       | ACTIVE  | 2026-07-25     |
| 5002 | Joseph Otieno   | 12,000    | 9,600       | 600     | OVERDUE | 2026-07-18     |
| 5003 | Grace Wanjiku   | 5,000     | 3,000       | 0       | ACTIVE  | 2026-07-25     |
| 5004 | Peter Kamau     | 6,000     | 0           | 0       | CLOSED  | —              |
| 5005 | Mary Achieng    | 4,000     | 2,800       | 0       | ACTIVE  | 2026-07-25     |
| 5006 | Faith Nyambura  | 3,000     | 2,100       | 0       | ACTIVE  | 2026-07-25     |
| 5007 | Samuel Omondi   | 15,000    | 13,500      | 1,500   | OVERDUE | 2026-07-11     |
| 5008 | Rebecca Atieno  | 2,500     | 1,750       | 0       | ACTIVE  | 2026-07-25     |
| 5009 | David Kiprono   | 7,500     | 5,250       | 0       | ACTIVE  | 2026-07-25     |
| 5010 | Esther Nyokabi  | 2,000     | 0           | 0       | CLOSED  | —              |
| 5011 | John Mwangi     | 10,000    | 10,000      | 0       | PENDING | —              |
| 5012 | Sarah Adhiambo  | 4,500     | 3,150       | 0       | ACTIVE  | 2026-07-25     |

- **Filter distribution** — ACTIVE 7, OVERDUE 2, CLOSED 2, PENDING 1 → every LoanStatusFilter chip renders a non-empty subset.
- **Product**: Group Solidarity Loan (0.83% / period, 4–52-week durations).
- **`canApplyLoan`**: `true` on the default demo (session role ∈ {chairperson, treasurer}); FAB rendered.
- **Fits within page_size=20**: `OnLoadNextPage` never triggers on the seed page.

---

## States

The ui.yaml declares 4 `screen_state` members (`Loading`, `Content`, `Error`, `Empty`) — each renders as a distinct HTML preview surface under `preview/`.

### `loading`
Shimmer skeleton mirroring the content layout — parallel fetch of `loans` from SQLDelight cache + Fineract API.

```
[Group Loans header]                       ← top_bar visible with title
[shimmer chip] [shimmer chip] [shimmer chip]  ← filter_chips_row skeleton
────────────────────────────────────────
[shimmer card ] ← 96dp × full width, corner 12dp, surfaceVariant
[shimmer card ]
[shimmer card ]   ← shimmer_list count: 5
[shimmer card ]
[shimmer card ]
```

- Cards: 96dp × full width, corner 12dp, `surfaceVariant` background shimmering 1.4s ease-in-out infinite.
- Respects `prefers-reduced-motion: reduce` (animation disabled).
- Top bar retains title "Group Loans" (no back navigation blocked; filter chips inert during load).
- Filter chips render as inert skeleton chips (no ripple, `pointer-events: none`).

### `content` (see layout above)
Loans loaded from Store5 stream. Chips filter the in-memory list (no network call). FAB visible only when `canApplyLoan == true`.

### `empty`
No loans match the selected filter (e.g. chip "Closed" with no CLOSED loans yet).

```
┌ Group Loans ───────────────────────────┐
│  [All] [Active] [Overdue] [Closed*]     │  filter_chips_row retained
├────────────────────────────────────────┤
│                                          │
│                                          │
│               💼                         │  empty_state · icon account_balance_wallet
│         No loans yet                     │  title · titleLarge
│    No loans match the                    │  body · bodyMedium, --text-secondary
│    selected filter.                      │
│                                          │
│                                          │
│                          ┌──[ + Apply ]─│  apply_loan_fab remains visible
└─────────────────────────────────────────┘
```

- Chairperson / treasurer can still tap the FAB and start a fresh application from the empty state.
- Illustration uses `account_balance_wallet` outlined icon at 64dp, `onSurfaceVariant` tint.

### `error`
Fineract API failed AND cache is empty — retry surface. When cache HAS rows, the toast fallback keeps the content visible (see `error_network` copy).

```
┌ Group Loans ───────────────────────────┐
│                                          │
│                                          │
│               ☁                          │  error_state · cloud_off icon
│       Could not load loans               │  title · titleLarge
│                                          │
│    {error.message}                       │  body · bodyMedium, --text-secondary
│    e.g. "No internet connection.         │
│    Showing cached data."                 │
│                                          │
│  ┌─────── Retry ──────────────────┐    │  cta_label · primary #2E7D32, 48dp
│  └────────────────────────────────┘    │  → Retry action_contract effect: call_api
│                                          │  fresh=true, re-triggers Store5 stream
└─────────────────────────────────────────┘
```

Error types (from `LoanListError`):
- `Network` — retry:true, `error_network` "No internet connection. Showing cached data."
- `Server` — retry:true, `error_server` "Server error. Please try again."
- `Auth` — retry:false, `error_auth` "Session expired. Please log in again." → redirect to `login`

---

## Interaction Patterns

1. **Loan card tap** → `OnLoanClick(loanId)` (effect: `navigate`) → NavController push `loan-detail` with `loanId` route arg. Card uses 72dp min touch target and full-row ripple.
2. **Filter chip tap** → `OnFilterChange(filter)` (effect: `transform_state`) → sets `selectedFilter` and recomputes `filteredLoans` in-memory (no network). Chips reflect selection via `primaryContainer` fill (`errorContainer` for Overdue chip).
3. **FAB tap** → `OnApplyLoan(groupId)` (effect: `navigate`) → NavController push `loan-apply` with `groupId` route arg. FAB `visible_when: canApplyLoan` (chairperson/treasurer only).
4. **Pull to refresh** → `OnRefresh` (flow `invalidate_cache: true`) → Store5 fresh=true reload, keeps existing chips selected.
5. **Scroll to list end** → `OnLoadNextPage` → paginated fetch (offset increment) via `get_group_loans`; empty next page silently no-ops.
6. **Retry tap (error state)** → `Retry` (effect: `call_api`, external: Store5) → Store5 stream with `fresh=true` re-hits Fineract `get_group_loans` and repopulates the list.
7. **Back tap** → `OnBack` (effect: `navigate`) → pops the route back to `group-dashboard`; no state persistence needed.

---

## Accessibility

- Loan card exposes a single semantic action ("Open loan for {memberName}, KES {principal}, {status}").
- Status is text + colored badge — never color-only (badge label always readable).
- Overdue indicator is bold labelSmall + red — supplemented by explicit "OVERDUE — KES {amount}" copy.
- Filter chips carry role `tab`; selected chip communicates state via ARIA `aria-selected="true"`.
- Min touch target 72dp on loan cards, 48dp on filter chips, 56dp on FAB.
- Locales covered: English, Swahili (`Mikopo ya Kikundi` / `Omba Mkopo`), French (`Prêts du Groupe`), Hindi (`समूह ऋण`).
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS.

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- Card ripple: MD3 standard 300ms ease-out on tap.
- Filter chip selection: fill transition 150ms.
- FAB press: MD3 elevation change 6dp → 12dp + ripple.
- Pull-to-refresh spinner: MD3 refresh indicator, matches primary `#2E7D32`.
- Snackbar (`ShowSnackbar` event): standard MD3 slide-up + auto-dismiss 4s (used for the cached-data fallback banner).

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `Store5`, `SQLDelight`, `Fineract m_loan`
**Internal lib**: `cmp-network-monitor`

Read paths (offline-first):
- `loans[]` ← `LoanRepository.getGroupLoans(groupId)` via Store5 stream
  - Source of truth: SQLDelight `loans` cache
  - Fetcher: Fineract `GET /groups/{groupId}/loans?limit=20&offset=…` (paged, gated by `cmp-network-monitor`)
  - `Retry` triggers `fresh=true`, `OnRefresh` triggers cache invalidation
- `filteredLoans[]` — derived state: `loans.filter { selectedFilter matches }` (client-side)
- `canApplyLoan` ← `SessionManager` role check (chairperson OR treasurer)

Write path: none (this screen is read-only; loan creation happens on `loan-apply`).

Offline behavior: when `NetworkMonitor.isOffline == true`, cache rows still render and `Network` error surfaces as a non-blocking snackbar/toast ("No internet connection. Showing cached data.") — the list itself stays in `content` state.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/loan-list/ui.yaml` |
| API contract | `idea-layer/screens/loan-list/api.yaml` |
| Data flow | `idea-layer/screens/loan-list/data-flow.yaml` |
| Demo data | `idea-layer/screens/loan-list/demo-data.yaml` |
| Flow | `idea-layer/screens/loan-list/flow.yaml` |
| Tests | `idea-layer/screens/loan-list/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/loan-list/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/loan-list/preview/content.html` |
| Preview HTML (empty) | `idea-layer/screens/loan-list/preview/empty.html` |
| Preview HTML (error) | `idea-layer/screens/loan-list/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/loan-list/prompts/{loading,content,empty,error}.md` |
| Stitch mockup (probe deferred) | `idea-layer/mockups/loan-list/stitch/01-loan-list-content/{code.html,screen.png}` |
| Feature-group mockup | `idea-layer/mockups/loan-management/MOCKUP.md` (Screen 1 section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (4/4 states rendered 2026-07-17) + ui.yaml + demo-data.yaml + design-system tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The legacy stitch artifact under `stitch/01-loan-list-content/` (2026-05-20) is stale relative to the current 12-row demo dataset and 4-state ui.yaml; it will be regenerated on the next Stitch-enabled `/idea-feature-stitch --features loan-list` pass.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features loan-list
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to ui.yaml components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
