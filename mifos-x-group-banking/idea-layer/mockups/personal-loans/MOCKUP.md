# Personal Loans — Mockup Specification

**Feature**: personal-loans | **Route**: `/loans` | **Type**: list
**Feature group**: personal-banking | **Flow**: personal-banking-flow
**Generated from**: `screens/personal-loans/ui.yaml`, `screens/personal-loans/demo-data.yaml`, `screens/personal-loans/preview/*.html` (4 states rendered 2026-07-17)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature personal-loans`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, back button, active filter chip fill
**Secondary**: `#FF8F00` (`--accent-700`, amber) — extended FAB "Request Loan" background
**Success**: `#1B5E20` on `#C8E6C9` — ACTIVE status chip (primaryContainer)
**Warning / Pending**: `#7B5B00` on `#FFF3C4` — PENDING APPROVAL chip (secondaryContainer)
**Danger / Overdue**: `#B71C1C` on `#FFCDD2` — OVERDUE chip (errorContainer) + overdue indicator text
**Muted / Closed**: `#757575` on `#F5F5F5` — CLOSED chip (surfaceVariant)
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (shimmer, closed chips)
**Corner radius**: 12dp cards (lg) + shimmer skeletons · 16px filter chips · full-round extended FAB
**Elevation**: 2dp loan cards · 6dp FAB
**Min touch target**: 72dp loan card · 48dp filter chip · 56dp FAB

---

## Screen: My Loans

### Entry
- From **personal-dashboard** (user taps their loan-summary card); nav-param `clientId: Long`
- Back navigation pops the route and returns to `personal-dashboard`
- Deep link `/loans?clientId={id}` (scoped to signed-in member's own clientId via `/self/loans` endpoint)

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹]  My Loans                [#2E7D32]  │  top_bar — primary green, onPrimary text,
│                                          │  navigation_icon arrow_left_24_regular
├─────────────────────────────────────────┤
│  [All*] [Active] [Closed]            →  │  filter_chips_row — horizontal scroll,
│                                          │  16dp margin · 6/14dp padding · single-select
│                                          │  selected = primaryContainer fill
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ Group Emergency Loan   [ACTIVE ] │   │  loan_card · elevation 2dp, corner 12dp,
│  │                          green   │   │  16dp padding · 12dp margin_bottom
│  │ KES 3,250                        │   │  outstanding_amount · headlineSmall bold
│  │ Next: KES 458 due 2026-05-20 ⚠  │   │  next_repayment_text · bodySmall,
│  │                            red   │   │  ERROR color when isOverdue==true,
│  │                              [∨] │   │  warning_24_filled overdue_icon
│  └──────────────────────────────────┘   │  → on_click OnLoanExpand(5001)
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ Seasonal Harvest Loan  [CLOSED ] │   │  CLOSED — surfaceVariant chip #F5F5F5
│  │                          grey    │   │
│  │ KES 0                            │   │  outstanding = 0 (obligations met)
│  │                              [∨] │   │  next_repayment_row hidden (status.active=false)
│  └──────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ Group Emergency Loan             │   │
│  │              [PENDING APPROVAL]  │   │  pending_approval — secondaryContainer amber
│  │ KES 0                            │   │  principalOutstanding == 0 until disbursed
│  │                              [∨] │   │  next_repayment_row hidden
│  └──────────────────────────────────┘   │
├─────────────────────────────────────────┤
│                     ┌──[ + Request Loan ]│  request_loan_fab · extended, amber #FF8F00,
│                     │                    │  onSecondary icon+text, 56dp, bottom_end,
│                     └────────────────────│  visible_when loans.isNotEmpty()
│                                          │  → on_click OnRequestLoanClick → loan-request
└─────────────────────────────────────────┘
```

### Layout (state: `content` — one card expanded)

Tap on loan 5001 (Group Emergency Loan, ACTIVE / in-arrears): `selectedLoanId = 5001` sets the expand-icon to `chevron_up` and reveals the `repayment_schedule_section` inline within the same card (no navigation).

```
┌──────────────────────────────────┐
│ Group Emergency Loan   [ACTIVE ] │
│ KES 3,250                        │
│ Next: KES 458 due 2026-05-20 ⚠  │
│                              [∧] │  chevron_up_24_regular
│  ─────────────────────────────   │
│  Repayment Schedule              │  schedule_header · labelLarge, onSurfaceVariant
│  ✓ Period #1 — 2026-01-20 458    │  period_row · checkmark_circle_24_filled primary
│  ✓ Period #2 — 2026-02-20 458    │  complete=true → primary tint on icon + amount
│  ✓ Period #3 — 2026-03-20 458    │
│  ✓ Period #4 — 2026-04-20 458    │
│  ○ Period #5 — 2026-05-20 458    │  circle_24_regular outline, onSurfaceVariant
│  ○ Period #6 — 2026-06-20 458    │  complete=false → onSurface amount
└──────────────────────────────────┘
```

### Demo Data (state: `content`, from `demo-data.yaml`)

Three loans exercising every status chip + row state declared by `ui.yaml`:

| id   | Product                | Principal | Outstanding | Status            | isOverdue | Next Repayment     |
|------|------------------------|-----------|-------------|-------------------|-----------|--------------------|
| 5001 | Group Emergency Loan   | 5,000     | 3,250       | ACTIVE (in-arrears)| **true**  | KES 458 · 2026-05-20 |
| 4001 | Seasonal Harvest Loan  | 8,000     | 0           | CLOSED            | false     | — (hidden)         |
| 6001 | Group Emergency Loan   | 4,000     | 0           | PENDING APPROVAL  | false     | — (hidden)         |

- **Filter distribution** — ACTIVE 1, CLOSED 1, PENDING 1 → every `LoanStatusFilter` chip renders a non-empty subset (ALL: 3, ACTIVE: 1, CLOSED: 1).
- **Product mix**: 2× Group Emergency Loan (product 3, 2.0%/period, 12-period term), 1× Seasonal Harvest Loan (product 2, 1.5%/period, 6-period term).
- **Session state**: `PersonalLoansState { clientId: 101, selectedLoanId: null, filterStatus: ALL, isLoading: false, isRefreshing: false, error: null }` — default preview shows 3 collapsed cards.
- **5001 schedule**: 6 periods total, 4 complete + 2 outstanding (period 5 is the "next due" carrying the overdue-red styling); demo data drives the expanded-card layout above.
- **6001 schedule**: `periods: []` — pending approval hides both `next_repayment_row` (via `status.active` guard) and any expandable rows on tap.

---

## States

The ui.yaml declares 4 `screen_state` members (`Loading`, `Content`, `Empty`, `Error`) — each renders as a distinct HTML preview surface under `preview/`.

### `loading`
Shimmer skeleton mirroring the content layout — parallel fetch of `loans` from SQLDelight cache + Fineract `/self/loans`.

```
[My Loans header]                          ← top_bar visible with title
[shimmer chip] [shimmer chip] [shimmer chip]  ← filter_chips_row skeleton
────────────────────────────────────────
[shimmer card ] ← 120dp × full width, corner 12dp, surfaceVariant
[shimmer card ]   ← shimmer_loading count: 3
[shimmer card ]
```

- Cards: 120dp × full width, corner 12dp (lg), 16dp horizontal margin, `surfaceVariant` background shimmering 1.4s ease-in-out infinite.
- Respects `prefers-reduced-motion: reduce` (animation disabled).
- Top bar retains title "My Loans" (back navigation still functional).
- Filter chips render as inert skeleton chips (no ripple, `pointer-events: none`).
- FAB **hidden** during loading (`visible_when: loans.isNotEmpty()` — empty during load).

### `content` (see layouts above)
Loans loaded from Store5 stream. Chips filter the in-memory list (no network call). Loan cards expand inline to reveal the repayment schedule. FAB visible whenever `loans.isNotEmpty()`.

### `empty`
No loans yet for this client (`loans.isEmpty() && !isLoading && error == null`).

```
┌ My Loans ──────────────────────────────┐
│                                          │
│                                          │
│               💰                         │  empty_state · money_24_regular icon,
│         No loans yet                     │  64dp, onSurfaceVariant tint
│    Apply for a loan of up to 3×          │  title · titleLarge
│    your savings balance.                 │  body · bodyMedium, onSurfaceVariant
│                                          │
│  ┌───── Request a Loan ─────────────┐  │  cta_label · secondary #FF8F00,
│  └────────────────────────────────────┘  │  onSecondary text, 48dp, corner full
│                                          │  → on_click OnRequestLoanClick → loan-request
│                                          │
└─────────────────────────────────────────┘
```

- Filter chips **hidden** in the empty state (per ui.yaml `states.empty.components: [top_bar, empty_state]`).
- Empty-state CTA and the FAB share the same action (`OnRequestLoanClick`) so the flow to `loan-request` is one tap regardless of state.
- Illustration uses `money_24_regular` outlined icon at 64dp, `onSurfaceVariant` tint.

### `error`
Fineract `/self/loans` failed AND cache is empty — retry surface. When cache HAS rows, the toast fallback keeps the content visible (see `error_network` copy).

```
┌ My Loans ──────────────────────────────┐
│  [All] [Active] [Closed]                 │  filter_chips_row retained
├────────────────────────────────────────┤
│                                          │
│               📡                         │  error_state · wifi_off_24_filled icon,
│                                          │  64dp, error tint
│      Could not load loans                │  title · titleLarge
│                                          │
│   {error.message}                        │  body · bodyMedium, onSurfaceVariant
│   e.g. "Check your internet              │
│   connection and try again."             │
│                                          │
│  ┌─────── Try Again ────────────────┐  │  cta_label · primary #2E7D32, 48dp
│  └────────────────────────────────────┘  │  → OnRetry action_contract effect: call_api
│                                          │  invalidates cache, re-fetches via ktor
└─────────────────────────────────────────┘
```

Error types (from `LoanError`):
- `Network` — retry:true, `error_network` "No internet connection. Showing cached data."
- `Server` — retry:true, `error_server` "Server error. Please try again."
- `Unauthorized` — retry:false, `error_session_expired` "Session expired. Please log in again." → redirect to `login`

---

## Interaction Patterns

1. **Loan card tap** → `OnLoanExpand(loanId)` (effect: `transform_state`) → sets `selectedLoanId` and toggles the inline `repayment_schedule_section` open/closed. Pure state transition — the `repaymentSchedule` was pre-fetched with the loan, so no network call. Chevron flips `chevron_down` ↔ `chevron_up`.
2. **Filter chip tap** → `OnFilterChange(status)` (effect: `transform_state`) → sets `filterStatus` and recomputes the visible loan list client-side (`ALL | ACTIVE | CLOSED`). No Fineract call. Chip shows selection via `primaryContainer` fill.
3. **FAB tap** → `OnRequestLoanClick` (effect: `navigate`) → NavController push `loan-request`, forwarding the current `clientId`. FAB `visible_when loans.isNotEmpty()`.
4. **Empty-state CTA tap** → `OnRequestLoanClick` (same action as FAB) → NavController push `loan-request` for the member's first loan.
5. **Pull to refresh** → `OnRefresh` (Store5 `fresh=true`) → invalidates the SQLDelight cache and re-fetches; sets `isRefreshing = true` during the round-trip. Selected chip preserved.
6. **Retry tap (error state)** → `OnRetry` (effect: `call_api`, external: `ktor-client` + `sqldelight`) → cmp-network-monitor gates the retry; only fires when connectivity is available; on success returns to `content`.
7. **Back tap** → `NavigateBack` (effect: `navigate`) → pops the route back to `personal-dashboard`; no state persistence needed.

---

## Accessibility

- Loan card exposes a single semantic action ("Expand loan for {productName}, KES {outstanding}, {status}").
- Status is text + colored chip — never color-only (chip label always readable).
- Overdue indicator is compounded: red `next_repayment_text` copy + `warning_24_filled` icon — no reliance on color alone.
- Filter chips carry role `tab`; selected chip communicates state via ARIA `aria-selected="true"`.
- Min touch target 72dp on loan cards, 48dp on filter chips, 56dp on extended FAB (+ CTA button 48dp).
- Locales covered: English, Swahili (`Mikopo Yangu` / `Omba Mkopo`), French (`Mes Prêts` / `Demander un Prêt`), Hindi (`मेरे ऋण` / `ऋण के लिए आवेदन`).
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS.
- Repayment-schedule rows use icon + text (`✓` / `○`) so completion status is never color-only.

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- Card ripple: MD3 standard 300ms ease-out on tap.
- Card expand / collapse: MD3 shared-axis-Y 200ms ease-in-out; chevron rotates 180°.
- Filter chip selection: fill transition 150ms.
- FAB press: MD3 elevation change 6dp → 12dp + ripple.
- Pull-to-refresh spinner: MD3 refresh indicator, matches primary `#2E7D32`.
- Snackbar (network-degraded banner): standard MD3 slide-up + auto-dismiss 4s (used for the cached-data fallback banner).

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `ktor-client`, `sqldelight`, `store5`
**Internal lib**: `cmp-network-monitor`
**Required modules**: `core/network`, `core/database`, `core/store`, `core/data`

Read paths (offline-first, 180s SWR TTL):
- `loans[]` ← `LoanRepository.getSelfLoans(clientId)` via Store5 stream
  - Source of truth: SQLDelight `loans` cache
  - Fetcher: Fineract `GET /self/loans` (scoped to signed-in member's clientId — no path-param)
  - Serve-stale-while-revalidate with 180s TTL; `OnRetry` triggers `fresh=true`, `OnRefresh` triggers cache invalidation
- `filteredLoans[]` — derived state: `loans.filter { filterStatus matches }` (client-side, from `filter_chips_row`)
- `selectedLoanId` — local UI state; drives the inline expand/collapse of `repayment_schedule_section` (schedule pre-fetched with each loan; no additional network call on expand)
- `clientId` ← nav-param from `personal-dashboard` entry (also mirrored on `SessionManager` for the /self scoping)

Write path: **none** (this screen is read-only; loan creation happens on `loan-request`, forwarded via `OnRequestLoanClick`).

Offline behavior: when `NetworkMonitor.isOffline == true`, cache rows still render and `Network` error surfaces as a non-blocking snackbar/toast ("No internet connection. Showing cached data.") — the list itself stays in `content` state. Retry is gated by `cmp-network-monitor` so it only fires when connectivity is restored.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/personal-loans/ui.yaml` |
| API contract | `idea-layer/screens/personal-loans/api.yaml` |
| Data flow | `idea-layer/screens/personal-loans/data-flow.yaml` |
| Demo data | `idea-layer/screens/personal-loans/demo-data.yaml` |
| Flow | `idea-layer/screens/personal-loans/flow.yaml` |
| Tests | `idea-layer/screens/personal-loans/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/personal-loans/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/personal-loans/preview/content.html` |
| Preview HTML (empty) | `idea-layer/screens/personal-loans/preview/empty.html` |
| Preview HTML (error) | `idea-layer/screens/personal-loans/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/personal-loans/prompts/{loading,content,empty,error}.md` |
| Stitch mockup | `idea-layer/mockups/personal-loans/stitch/` (probe deferred — RULE-STITCH-OPTIN-CONSISTENCY-001) |
| Feature-group mockup | `idea-layer/mockups/personal-banking/MOCKUP.md` (Screen section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (4/4 states rendered 2026-07-17) + ui.yaml + demo-data.yaml + design-system tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The `mockups/personal-loans/stitch/` directory exists as a scaffold — no `code.html` / `screen.png` yet; will be populated on the next Stitch-enabled `/idea-feature-stitch --features personal-loans` pass.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features personal-loans
  ```
- Design conformance verifier: preview HTML mirrors the layouts above; any hand-edit to `ui.yaml` components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
