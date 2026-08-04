# Loan Detail — Mockup Specification

**Feature**: loan-detail | **Route**: `/loans/{loanId}` | **Type**: detail
**Feature group**: loan-management | **Flow**: loan-management-flow
**Generated from**: `screens/loan-detail/ui.yaml`, `screens/loan-detail/demo-data.yaml`, `screens/loan-detail/preview/*.html` (3 states rendered 2026-07-17)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature loan-detail`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: MifosSave-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — top bar, tab indicator, Record Repayment CTA, Retry CTA, transaction amount text
**Accent**: `#FF8F00` (`--accent-700`, amber) — not used on this screen (accent reserved for pooled-fund emphasis screens)
**Success**: `#2E7D32` — PAID row text on `#F1F8E9` chip
**Warning**: `#E65100` on `#FFF9C4` — PARTIAL row + partial-payment surfaces
**Danger**: `#B71C1C` on `#FFCDD2` — OVERDUE badge + row · `error` container backs Mark Defaulted CTA
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` filled inputs
**Corner radius**: 12px cards, badges, buttons (24dp CTAs full-pill) · 8dp per ui.yaml component styles
**Min touch target**: 48dp (tabs, badges) · 48dp CTAs (weight-1 half-width primary/danger buttons)

---

## Screen: Loan Detail

### Entry
- From **loan-list** — tap a loan card (nav param `loanId: Long`)
- Back navigation returns to loan-list (no draft — pure read screen with role-gated write CTAs)

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹]  Loan Detail              [↻]       │  TopAppBar — primary green #2E7D32,
│                                          │  onPrimary text, refresh action right
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │  Grace Akinyi                     │   │  member_header_card — primaryContainer
│  │  Group Solidarity Loan            │   │  bg, onPrimaryContainer text, 12dp
│  │  Principal: KES 8,000             │   │  radius, 16dp padding, 0dp elevation
│  │  Disbursed: 2026-05-05            │   │  Text stack: headlineSmall + bodyMedium
│  │  Interest: 0.83% per week         │   │  + bodyLarge + bodySmall × 2
│  │                                    │   │
│  │                    [ ACTIVE ]     │   │  loan_status_badge — #C8E6C9 bg,
│  └──────────────────────────────────┘   │  #1B5E20 text (ACTIVE style)
├─────────────────────────────────────────┤
│  [ Outstanding · KES 7,034 ]            │  info-chip · secondaryContainer bg,
│                                          │  onSecondaryContainer text
│  ( Overdue chip hidden — totalOverdue=0)│  visible_when: loan.totalOverdue > 0
├─────────────────────────────────────────┤
│  ┌────────────────────────────────┐     │
│  │  Schedule  │  Repayment History │     │  detail_tabs — surface bg, primary
│  │  ▔▔▔▔▔▔▔▔ │                    │     │  indicator under selected tab
│  └────────────────────────────────┘     │  selectedTab = SCHEDULE (default)
├─────────────────────────────────────────┤
│  Wk│  Due Date  │  Due │  Paid │Balance│Status │  schedule_table headers
│  ───┼─────────────┼──────┼───────┼───────┼───────
│  1 │ 2026-05-12 │1,066 │ 1,066 │6,934  │ PAID  │  #F1F8E9 bg / #33691E text
│  2 │ 2026-05-19 │1,059 │   0   │5,875  │UPCOM. │  surface bg / onSurface text
│  3 │ 2026-05-26 │1,051 │   0   │4,824  │UPCOM. │
│  4 │ 2026-06-02 │1,043 │   0   │3,781  │UPCOM. │
│  5 │ 2026-06-09 │1,035 │   0   │2,746  │UPCOM. │
│  6 │ 2026-06-16 │1,027 │   0   │1,719  │UPCOM. │
│  7 │ 2026-06-23 │1,019 │   0   │  700  │UPCOM. │
│  8 │ 2026-06-30 │  706 │   0   │    0  │UPCOM. │
├─────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐     │
│  │  Record       │  │  Mark        │     │  action_buttons_row — 16dp padding,
│  │  Repayment    │  │  Defaulted   │     │  12dp gap between the two buttons
│  └──────────────┘  └──────────────┘     │  each weight:1 half-width
│  #2E7D32 primary   #B00020 danger        │  24dp pill radius, 48dp min touch
│  role: TREASURER   role: CHAIRPERSON     │  visible_when role + status gate
└─────────────────────────────────────────┘
```

Column widths per ui.yaml: Wk 40dp · Due Date 96dp · Due 88dp · Paid 88dp · Balance 88dp · Status 72dp.

### Demo Data (state: `content`)

- **loan** (single `LoanDetail` DTO):
  - memberName: "Grace Akinyi" (id 303)
  - loanProductName: "Group Solidarity Loan"
  - principalAmount: KES 8,000.00 · disbursedDate: 2026-05-05
  - interestRatePercent: 0.83 (per period, declining balance)
  - totalOutstanding: KES 7,034.00 · totalOverdue: KES 0.00 → overdue chip hidden
  - status: ACTIVE → green ACTIVE badge, Record Repayment CTA eligible, Mark Defaulted hidden
- **repaymentSchedule[]** (8 rows, 1 PAID + 7 UPCOMING, weekly cadence 2026-05-12 → 2026-06-30)
- **repaymentHistory[]** (2 rows, hidden on the SCHEDULE tab — see HISTORY tab below):
  - `#5001 DISBURSEMENT · 2026-05-05 · KES 8,000.00`
  - `#5002 REPAYMENT · 2026-05-12 · KES 1,066.40`
- **role flags**: `canRecordRepayment=true` (treasurer session), `canMarkDefaulted=false` (ACTIVE status hides it)

### Layout (state: `content` — HISTORY tab)

```
┌─────────────────────────────────────────┐
│  Schedule  │  Repayment History         │  tab_history active, indicator moves
├─────────────────────────────────────────┤
│  DISBURSEMENT                            │  list-item · transaction_row
│  2026-05-05                              │  onSurfaceVariant date · bodySmall
│                       KES 8,000.00       │  primary #2E7D32 amount · bodyMedium
│  ───────────────────────────────────    │
│  REPAYMENT                               │
│  2026-05-12                              │
│                       KES 1,066.40       │
└─────────────────────────────────────────┘
```

Empty-state text (when `repaymentHistory` is empty): "No repayments recorded yet."

---

## States

The ui.yaml declares 3 `screen_state` members (`Loading`, `Content`, `Error`) — all 3 render as distinct preview surfaces at `screens/loan-detail/preview/{state}.html`.

### `loading`
Shimmer skeleton — 3 cards of 120dp height, 12dp radius, `surfaceVariant` fill. Top bar retains "Loan Detail" title; refresh action inactive.

```
┌ Loan Detail ─────────────────────────┐
│  [shimmer card 120dp · 12dp radius ]  │  ← replaces member_header_card
│  [shimmer card 120dp · 12dp radius ]  │  ← replaces outstanding + tabs area
│  [shimmer card 120dp · 12dp radius ]  │  ← replaces schedule_table
└──────────────────────────────────────┘
```

- Fields: `--bg-muted` shimmer gradient (1.4s ease-in-out infinite)
- Respects `prefers-reduced-motion: reduce` (animation disabled)
- Back nav-icon retained (loading is cancellable via back)

### `content` (see two layouts above)
Two sub-modes controlled by `selectedTab`:
- **SCHEDULE tab (default)** — `schedule_table` visible, `history_list` hidden
- **HISTORY tab** — `schedule_table` hidden, `history_list` visible (empty text if list empty)

Action-button visibility rules (composed):
- `record_repayment_button` shown ⇔ `canRecordRepayment && loan.status == ACTIVE`
- `mark_defaulted_button` shown ⇔ `canMarkDefaulted && loan.status == OVERDUE`
- Both hidden for a CLOSED loan (read-only view)

### `error`
Full-screen error surface — cloud_off illustration + title + body + primary Retry CTA.

```
┌ Loan Detail ─────────────────────────┐
│                                         │
│               ☁                         │  cloud_off icon
│         Could not load loan             │  titleLarge
│    {{error.message}} interpolated       │  bodyMedium, --text-secondary
│                                         │
│  ┌────── Retry ─────────────────────┐  │  primary #2E7D32, 48dp full width
│  └──────────────────────────────────┘  │  → Retry action (call_api)
└────────────────────────────────────────┘
```

Error types (from `LoanDetailError`):
- `Network` — retry:true, `error_network` "No internet. Showing cached data."
- `Server` — retry:true, `error_server` "Server error. Please try again."
- `NotFound` — retry:false, `error_not_found` "Loan not found."
- `Auth` — retry:false, `error_auth` → redirect to `login`

---

## Interaction Patterns

1. **Screen load** → `LoanDetailViewModel` calls `LoanRepository.getLoanDetail(loanId)` — Store5 stale-while-revalidate over SQLDelight cache, then network refresh via Fineract `GET /loans/{loanId}`; `cmp-network-monitor` surfaces offline. Splits response into header summary, `RepaymentScheduleRow[]`, `RepaymentTransaction[]`.
2. **Refresh tap** → `OnRefresh` (effect: `call_api`) → re-fetches network-first, invalidates cache, re-emits LoanDetailState.
3. **Tab tap** → `OnTabChange(SCHEDULE|HISTORY)` (effect: `transform_state`) — pure ViewModel `selectedTab` write; no I/O (schedule + history already loaded).
4. **Record Repayment tap** → `OnRecordRepayment` (effect: `call_api`) — opens `loan-repayment-dialog`; on confirm calls `LoanRepository.recordRepayment(loanId, amount, externalId)` → POST /loans/{loanId}/transactions (Fineract) with idempotent externalId → fresh balance re-cached via Store5 → schedule re-emitted.
5. **Mark Defaulted tap** → `OnMarkDefaulted` (effect: `call_api`) — opens `loan-mark-defaulted-dialog`; on confirm calls `LoanRepository.markDefaulted(loanId, externalId)` → updates Fineract `m_loan.status` to DEFAULTED → badge + action gating refresh.
6. **Back tap** → `OnBack` (effect: `navigate`) — pops loan-detail off NavController; returns to loan-list.
7. **Retry tap** (error state) → `Retry` (effect: `call_api`) — re-invokes `getLoanDetail`, `cmp-network-monitor` distinguishes offline vs server so ViewModel restores Content or re-surfaces error.

---

## Role & Status Gating

| Role | Status ACTIVE | Status OVERDUE | Status CLOSED |
|------|---------------|----------------|---------------|
| Treasurer | Record Repayment visible | Record Repayment + Mark Defaulted visible (chairperson-authored) | read-only |
| Chairperson | Record Repayment hidden, Mark Defaulted hidden (not OVERDUE) | Record Repayment hidden, Mark Defaulted visible | read-only |
| Member | read-only | read-only | read-only |

`canRecordRepayment` / `canMarkDefaulted` are derived by ViewModel from `SessionManager.roles` × `loan.status`. Neither button reveals for a member session.

---

## Accessibility

- Every clickable surface carries an accessibility label — refresh icon uses `Refresh loan data` content_description (declared in ui.yaml); Record Repayment / Mark Defaulted labels are their visible text.
- Min touch target 48dp on tabs, badges, action buttons; 48dp on refresh icon (icon-button min).
- Status badges combine text + colour (ACTIVE / OVERDUE / CLOSED never encoded by colour alone).
- OVERDUE row backgrounds (#FFCDD2 on #B71C1C text) — WCAG AA passes at bodyMedium.
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honoured on iOS; 200% scale layout survives (schedule table becomes horizontally scrollable per MD3 data-table pattern).
- Locales covered: English, Swahili (`Maelezo ya Mkopo` / `Ratiba` / `Rekodi Malipo`), French (`Détail du Prêt` / `Calendrier` / `Enregistrer un Remboursement`), Hindi (`ऋण विवरण` / `कार्यक्रम` / `पुनर्भुगतान दर्ज करें`).

---

## Motion & Feedback

- Shimmer skeleton (loading state): 1.4s ease-in-out infinite — disabled under `prefers-reduced-motion`.
- Tab indicator slide: MD3 standard easing ~200ms; SCHEDULE ↔ HISTORY content swap is a fade (150ms).
- Refresh icon: 200ms spin on `OnRefresh` dispatch (rotate 360°, ease-in-out) — collapsed to 0ms under reduced motion.
- Snackbar (`ShowSnackbar` event): MD3 standard slide-up + auto-dismiss 4s (used post record-repayment / mark-defaulted success from the dialogs).

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `Store5`, `SQLDelight`, `Fineract m_loan`
**Internal lib**: `cmp-network-monitor`

Read paths:
- `LoanDetail` ← `LoanRepository.getLoanDetail(loanId)` via Store5 (SQLDelight cache) → Fineract `GET /loans/{loanId}` on refresh
- `RepaymentScheduleRow[]` ← split from same response, `List<RepaymentScheduleRow>` in state
- `RepaymentTransaction[]` ← split from same response, `List<RepaymentTransaction>` in state
- `canRecordRepayment`, `canMarkDefaulted` ← `SessionManager` role × `loan.status`

Write paths:
- `LoanRepository.recordRepayment(loanId, amount, externalId)` → `POST /loans/{loanId}/transactions` — idempotent externalId; refresh cascades to Store5 cache and re-emits schedule + outstanding.
- `LoanRepository.markDefaulted(loanId, externalId)` → `PUT /loans/{loanId}/status` (defaulted) — idempotent externalId; loan row + badge + action gating refresh.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/loan-detail/ui.yaml` |
| API contract | `idea-layer/screens/loan-detail/api.yaml` |
| Data flow | `idea-layer/screens/loan-detail/data-flow.yaml` |
| Demo data | `idea-layer/screens/loan-detail/demo-data.yaml` |
| Flow | `idea-layer/screens/loan-detail/flow.yaml` |
| Tests | `idea-layer/screens/loan-detail/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/loan-detail/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/loan-detail/preview/content.html` |
| Preview HTML (error)   | `idea-layer/screens/loan-detail/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/loan-detail/prompts/{loading,content,error}.md` |
| Legacy stitch mockup   | `idea-layer/mockups/loan-detail/stitch/01-loan-detail-content/` (pre-2026-07 · MD only) |
| Feature-group mockup   | `idea-layer/mockups/loan-management/MOCKUP.md` (loan-detail section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (3/3 states rendered 2026-07-17 19:20–19:21) + ui.yaml + demo-data.yaml + DESIGN.md tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features loan-detail
  ```
- Design-conformance verifier: preview HTML mirrors the layout above; any hand-edit to `ui.yaml` components/states or `demo-data.yaml` schedule/history flips `needs_generate_mockup` on the next `/idea-sync` cascade.
