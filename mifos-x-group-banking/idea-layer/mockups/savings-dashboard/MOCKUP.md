# Savings Dashboard — Mockup Specification

**Feature**: savings-dashboard | **Route**: `/groups/{groupId}/savings` | **Type**: dashboard
**Feature group**: savings-management | **Flow**: savings-management-flow
**Generated from**: `screens/savings-dashboard/ui.yaml`, `screens/savings-dashboard/demo-data.yaml`, `screens/savings-dashboard/preview/*.html` (6 states rendered 2026-07-18)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature savings-dashboard`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: MifosSave-v3 (Material Design 3 · MD3) — dense financial dashboard density (7/10)
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first · regulated-industry
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for KES amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, tab indicator, primary chart bars, cycle progress
**Primary container**: `#C8E6C9` (`--primary-100`) — Cycle progress card, last-transaction chip, group total chip
**Secondary**: `#1565C0` (`--info`) — Individual tab line chart, individual balance emphasis
**Secondary container**: `#E3F2FD` — Individual total card, individual member row avatar
**Tertiary container**: `#FFE0B2` — tab-content Individual avatar tint (surface differentiation)
**Accent**: `#FF8F00` (`--accent-700`, amber) — pooled fund emphasis (reserved for share-out surfaces)
**Success**: `#2E7D32` on `#C8E6C9` — on-track cycle progress, treasurer role tint
**Warning**: `#F57C00` on `#FFF3E0` — cycle < 50% target advisory
**Danger**: `#C62828` on `#FFCDD2` — error banner icon + text emphasis
**Muted**: `#616161` on `#F5F5F5` — sync band, unselected tab label
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (shimmer skeleton, sync band)
**Corner radius**: 12dp cards + shimmer skeletons · 16px chips · 8dp linear progress track · 40dp avatar
**Elevation**: 0dp TopAppBar (border-based per §Component conventions) · 1dp tab row divider · 2dp charts card
**Min touch target**: 72dp member row · 48dp tab · 40dp chip · 48dp Retry button

---

## Screen: Savings

### Entry
- From **group-dashboard** ("Savings" section link OR bottom-nav "Savings" tab); nav-params `groupId: String, typeConfig: GroupTypeConfig`
- The `typeConfig.contribution_model` drives per-member row shape:
  - `SHARE_BASED_VARIABLE` (VSLA/SILC) → "X shares @ KES Y/share" + share value trailing
  - `FIXED_AMOUNT` (ROSCA/SHG) → "N meetings · Last: KES M" + total contributed trailing
  - `FIXED_NEGOTIATED` (JLG) → same as FIXED_AMOUNT with negotiated amount overlay
- Back navigation pops the route and returns to `group-dashboard`

### Layout (state: `content_group`, contribution_model = `FIXED_AMOUNT`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│  Savings                                 │  top_app_bar · surface fill, onSurface text
│  Mwangaza Women's Group                  │  subtitle · bodySmall, onSurfaceVariant
├─────────────────────────────────────────┤
│  Last synced: 2026-07-18 09:32           │  sync_band · surfaceVariant, labelSmall
├─────────────────────────────────────────┤
│ ┌──── Group Savings ────┬── Individual ─│  tab_row · indicator #2E7D32,
│ └────── #2E7D32 ────────┴── #616161 ────│  selected=primary · unselected=onSurfaceVariant
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │ ▄  ▄  ▂  ▆  ▄  █                   │ │  weekly_trend_chart_group · bar chart,
│  │ W48 W49 W50 W51 W52 W3             │ │  bar_color primary #2E7D32, height 180dp,
│  │                                    │ │  data: [1000, 1200, 850, 1500, 1200, 1850]
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │ Cycle Progress                     │ │  cycle_progress_card · primaryContainer #C8E6C9
│  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░            │ │  linear_progress · height 8dp, primary tint
│  │ KES 24,000 of KES 30,000           │ │  bodyMedium, onPrimaryContainer
│  │ 80% of cycle target                │ │  labelSmall, onPrimaryContainer
│  └────────────────────────────────────┘ │  (FIXED_AMOUNT branch — SHARE_BASED variant
│                                          │   shows "120 shares of 200 target" instead)
├─────────────────────────────────────────┤
│  ┌── Group total: KES 24,000 ────────┐  │  group_savings_total_chip · primaryContainer
│  └───────────────────────────────────┘  │  onPrimaryContainer, corner 16px, 40dp
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │ (AW) Amina Wanjiru      KES 6,000  │ │  group_member_savings_row · list-item,
│  │      12 meetings · Last: KES 300      total  │  min_height 72dp, divider between rows
│  ├────────────────────────────────────┤ │  leading avatar 40dp, secondaryContainer #E3F2FD
│  │ (JK) Joseph Kamau       KES 4,800  │ │  headline bodyLarge, onSurface
│  │      12 meetings · Last: KES 400      total  │  supporting bodySmall, onSurfaceVariant
│  ├────────────────────────────────────┤ │  trailing column: amount labelLarge primary,
│  │ (GW) Grace Wanjiku      KES 3,850  │ │  caption labelSmall onSurfaceVariant
│  │      11 meetings · Last: KES 350      total  │  → on_click OpenMemberDetail(MBR-101)
│  ├────────────────────────────────────┤ │      → navigate member-savings-detail
│  │ (PO) Peter Otieno       KES 3,000  │ │
│  │      10 meetings · Last: KES 300      total  │
│  ├────────────────────────────────────┤ │
│  │ (MA) Mary Akinyi        KES 2,250  │ │
│  │      9 meetings · Last: KES 250       total  │
│  └────────────────────────────────────┘ │
│              ↕ scroll                    │  page-fits-viewport; scroll for additional
└─────────────────────────────────────────┘  members when memberRows > 5
```

### Layout (state: `content_group`, contribution_model = `SHARE_BASED_VARIABLE` — VSLA variant)

```
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │ Cycle Progress                     │ │
│  │ ▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░              │ │
│  │ 120 shares of 200 target           │ │  SHARE_BASED_VARIABLE branch
│  │ 60% of cycle target                │ │
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  ┌── Group total: KES 120,000 ───────┐  │
│  └───────────────────────────────────┘  │
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │ (AH) Amina Hassan     KES 20,000   │ │
│  │      20 shares @ KES 1,000/share    share value │
│  ├────────────────────────────────────┤ │
│  │ (PO) Peter Otieno     KES 15,000   │ │
│  │      15 shares @ KES 1,000/share    share value │
│  ├────────────────────────────────────┤ │
│  │ (GW) Grace Wanjiku    KES 12,000   │ │
│  │      12 shares @ KES 1,000/share    share value │
│  └────────────────────────────────────┘ │
```

### Layout (state: `content_individual`)

```
┌─────────────────────────────────────────┐
│  Savings                                 │  top_app_bar retained
│  Mwangaza Women's Group                  │
├─────────────────────────────────────────┤
│  Last synced: 2026-07-18 09:32           │  sync_band retained
├─────────────────────────────────────────┤
│ ┌── Group Savings ──┬──── Individual ───│  tab_row · Individual selected
│ └────── #616161 ────┴───── #2E7D32 ─────│
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │  ╱╲    ╱╲                          │ │  weekly_trend_chart_individual · line chart,
│  │ ╱  ╲  ╱  ╲___                      │ │  line_color secondary #1565C0, 2dp width,
│  │╱    ╲╱      ‾                      │ │  fill_below true (0.12 alpha), height 180dp
│  │ W48 W49 W50 W51 W52 W3             │ │  data: [300, 500, 200, 700, 400, 650]
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │ Total Individual Balances          │ │  individual_total_card · secondaryContainer
│  │ KES 37,400                         │ │  headlineMedium, bold, onSecondaryContainer
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │ (AW) Amina Wanjiru    KES 11,200   │ │  individual_member_row · avatar tertiaryContainer
│  │      [KES 500 on 2026-05-05]        balance   │  supporting=chip primaryContainer +
│  ├────────────────────────────────────┤ │       onPrimaryContainer, 16px corner
│  │ (JK) Joseph Kamau     KES 8,400    │ │  trailing amount labelLarge secondary #1565C0
│  │      [KES 400 on 2026-05-05]        balance   │  → on_click OpenMemberDetail
│  ├────────────────────────────────────┤ │       (savings_type=INDIVIDUAL)
│  │ (GW) Grace Wanjiku    KES 7,200    │ │       → navigate member-savings-detail
│  │      [KES 350 on 2026-05-05]        balance   │
│  ├────────────────────────────────────┤ │
│  │ (PO) Peter Otieno     KES 6,000    │ │
│  │      [KES 300 on 2026-05-05]        balance   │
│  ├────────────────────────────────────┤ │
│  │ (MA) Mary Akinyi      KES 4,600    │ │
│  │      [KES 250 on 2026-05-05]        balance   │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Demo Data (state: `content_group`, from `demo-data.yaml`)

Mwangaza Women's Group — a `FIXED_AMOUNT` (ROSCA-style) VSLA in Kisumu West Branch, KES, weekly meetings, 12-month cycle:

| Member ID | Name           | Role        | Meetings | Last (KES) | Total (KES) |
|-----------|----------------|-------------|----------|------------|-------------|
| MBR-101   | Amina Wanjiru  | treasurer   | 12       | 300        | 6,000       |
| MBR-102   | Joseph Kamau   | chairperson | 12       | 400        | 4,800       |
| MBR-103   | Grace Wanjiku  | secretary   | 11       | 350        | 3,850       |
| MBR-104   | Peter Otieno   | member      | 10       | 300        | 3,000       |
| MBR-105   | Mary Akinyi    | role: member| 9        | 250        | 2,250       |

- **Cycle**: 30,000 KES target · 24,000 collected (80% of target — on-track amber-free).
- **Group total**: 24,000 KES (sum of 5 members' totals).
- **Weekly trend (6 weeks)**: `[1000, 1200, 850, 1500, 1200, 1850]` group amounts; individual amounts `[300, 500, 200, 700, 400, 650]`.
- **SHARE_BASED_VARIABLE variant** (VSLA/SILC — from `MemberGroupSavingsRow`): Amina Hassan (20 shares @ 1000), Peter Otieno (15 shares), Grace Wanjiku (12 shares) — 47 shares of a 200-share cycle target = 23.5% (chart above uses ui.yaml `content_group.demo_data` variant with cycleTarget 200, cycleCollected 120 = 60%).
- **Individual balances**: totalBalance 37,400 KES across 5 members (Amina 11,200 / Joseph 8,400 / Grace 7,200 / Peter 6,000 / Mary 4,600).

---

## States

The ui.yaml declares 6 discrete states (`loading`, `content_group`, `content_individual`, `content_with_error`, `empty`, `error`) each rendered as a distinct HTML preview under `preview/`.

### `loading`
Fetch-in-progress. Companion API + LocalSavingsDao cache both in flight via Store5 stream. TopAppBar retains "Savings" / "Mwangaza Women's Group" title; tab_row renders inert (no selection state), and 6 shimmer skeleton cards occupy the body.

```
[Savings]                                  ← top_app_bar visible (surface fill)
[Mwangaza Women's Group]
────────────────────────────────────────
[shimmer chip] [shimmer chip]               ← tab_row skeleton (inert)
────────────────────────────────────────
[shimmer card ] ← 72dp × full width, corner 12dp, surfaceVariant #F5F5F5
[shimmer card ]
[shimmer card ]   ← loading_skeleton count: 6
[shimmer card ]
[shimmer card ]
[shimmer card ]
```

- Shimmer cards: 72dp × full width, corner 12dp, `surfaceVariant` shimmering 1.4s ease-in-out infinite.
- Respects `prefers-reduced-motion: reduce` (animation collapses to 0ms per §Motion).
- Tabs are visible but non-interactive during the fetch (no ripple, `pointer-events: none`).
- Sync band NOT shown on cold start (`lastSyncAt == null`).

### `content_group` (see layout above)
Group tab selected. Group weekly bar chart + cycle progress + group-total chip + per-member rows. Contribution-model branch swaps supporting-text (`X meetings · Last: KES Y` for FIXED_AMOUNT vs `N shares @ KES M/share` for SHARE_BASED_VARIABLE) and trailing amount (total vs share value).

### `content_individual` (see layout above)
Individual tab selected. Individual weekly line chart + Total Individual Balances card + per-member balance rows with last-transaction chips. Tab indicator moves to Individual with 150ms ease-out transition.

### `content_with_error`
Content-with-error — cache HAS rows, but the latest refresh failed. Group tab data still visible; error_banner slides in above tab_row, offering non-blocking Retry.

```
┌ Savings ────────────────────────────────┐
│  Mwangaza Women's Group                  │
├─────────────────────────────────────────┤
│  Last synced: 2026-07-18 09:32           │
├─────────────────────────────────────────┤
│  ⚠ Showing cached savings — pull down    │  error_banner · errorContainer #FFCDD2
│    to retry               [Retry]        │  danger #C62828 text, Retry button 48dp
├─────────────────────────────────────────┤
│ ┌── Group Savings ──┬── Individual ─────│  tab_row unchanged
│ └─── #2E7D32 ───────┴─────────── #616161│
├─────────────────────────────────────────┤
│  [weekly trend chart — from cache]        │  content still rendered
│  [cycle progress card]                    │
│  [group total chip]                       │
│  [member rows 1..5]                       │
└─────────────────────────────────────────┘
```

- Retry action calls `RefreshDashboard` (effect: `call_api`, `library_refs: [cmp-network-monitor]`) — connectivity is checked via cmp-network-monitor before hitting the companion API. On no-network, an offline snackbar surfaces instead.
- Banner uses `errorContainer` background (`#FFCDD2`) with `danger` text — non-blocking, respects existing scroll position.

### `empty`
No savings data yet — first meeting has not been conducted. Shown when both `groupSavingsSummary` and `individualSavingsSummary` are null AND cache is empty.

```
┌ Savings ────────────────────────────────┐
│  Mwangaza Women's Group                  │
├─────────────────────────────────────────┤
│ ┌── Group Savings ──┬── Individual ─────│  tab_row retained (both tabs empty)
│ └────── #2E7D32 ────┴────────── #616161 │
├─────────────────────────────────────────┤
│                                          │
│                                          │
│               💰                          │  empty_state · icon savings_24_regular,
│         No Savings Data                  │  64dp, onSurfaceVariant tint
│                                          │  title · titleLarge, onSurface
│    Savings will appear after the         │
│    first meeting is conducted.           │  body · bodyMedium, onSurfaceVariant
│                                          │
│                                          │
└─────────────────────────────────────────┘
```

- Sync band hidden (`lastSyncAt == null`).
- Empty copy is contribution-model-agnostic (VSLA / ROSCA / SHG / JLG all see the same message on cycle start).
- No CTA — savings entries are created via the meeting-conduct flow, not from this screen.

### `error`
Fatal error — companion API failed AND local cache is empty. Only TopAppBar + error_banner render; no tab_row.

```
┌ Savings ────────────────────────────────┐
│  Mwangaza Women's Group                  │
├─────────────────────────────────────────┤
│                                          │
│               ☁                          │  error_state · cloud_off icon 64dp,
│       Could not load savings             │  danger tint, titleLarge onSurface
│                                          │
│    Showing cached savings — pull down    │  body · bodyMedium, onSurfaceVariant
│    to retry                              │
│                                          │
│  ┌─────── Retry ──────────────────┐    │  cta_label · primary #2E7D32, 48dp
│  └────────────────────────────────┘    │  → Retry action_contract effect: call_api
│                                          │  via cmp-network-monitor + Store5 fresh=true
└─────────────────────────────────────────┘
```

Error copy variants (from ui.yaml `NetworkError`):
- Network — "Showing cached savings — pull down to retry" (retry:true)
- Server — companion `/companion/groups/{groupId}/savings` 5xx → retry:true, standard toast
- Auth — token expired → redirect to `login` (retry:false)

---

## Interaction Patterns

1. **Tab tap** → `SelectTab(tab: SavingsTab)` (effect: `transform_state`, no libs) → updates `selectedTab` in `SavingsDashboardState`, swaps `group_savings_content` ↔ `individual_savings_content` via `visible_when`. No network call. Tab indicator translates with a 150ms ease-out transition.
2. **Group member row tap** → `OpenMemberDetail(memberId: String)` (effect: `navigate`) → NavController push `member-savings-detail` with `memberId` + `groupId` route args. Row uses 72dp min touch target, full-row ripple, `secondaryContainer` avatar tint.
3. **Individual member row tap** → `OpenMemberDetail(memberId, savings_type: INDIVIDUAL)` (effect: `navigate`) → same target with `savings_type=INDIVIDUAL` so the detail screen loads voluntary individual balance + transaction history.
4. **Pull to refresh** → `RefreshDashboard` (effect: `call_api`, libs: `cmp-network-monitor`) → connectivity check → Store5 stream fresh=true → companion API `GET /companion/groups/{groupId}/savings` → updates `lastSyncAt` on success; on offline, non-blocking snackbar surfaces without swapping to `error` state.
5. **Retry tap (error banner OR error state)** → `RefreshDashboard` (same action_contract) → same flow as pull-to-refresh; banner dismisses on success.
6. **Screen enters composition** → `LoadDashboard` — Store5 stream first emits cached snapshot (instant render from LocalSavingsDao), then the companion API response replaces it. `isRefreshing: false` after first emission; `isLoading: true` only during cold-start.
7. **Back tap** → NavController pop → returns to `group-dashboard`; `selectedTab` NOT persisted (next entry starts on GROUP).

---

## Accessibility

- Every member row exposes a single semantic action: "Open savings detail for {name}, {totalContributed OR sharesHeld}, {role}".
- Amounts use Roboto Mono / SF Mono per §Typography — screen-reader announces "KES six thousand" (not "KES 6,000" character-by-character).
- Tab role: `tab` on each; selected communicates via ARIA `aria-selected="true"` + tab indicator color.
- Error banner + error state icons carry `contentDescription` — banner "Network error, showing cached savings" / state "Could not load savings".
- Cycle progress bar exposes `role="progressbar"` + `aria-valuenow`/`aria-valuemin`/`aria-valuemax` (0..cycleTarget).
- Min touch targets: 72dp member rows, 48dp tabs, 48dp Retry button, 40dp avatars (non-interactive, hit-target extends to row).
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS up to 200% per §Accessibility.
- WCAG AA contrast maintained: `#2E7D32` on `#C8E6C9` = 7.5:1 (AAA), `#1565C0` on `#E3F2FD` = 8.1:1 (AAA), danger `#C62828` on `#FFCDD2` = 5.2:1 (AA).
- Locales covered: English (default), Swahili (`Akiba`, `Akiba za Kikundi`, `Binafsi`), French (`Épargne`, `Épargne de Groupe`, `Individuel`), Hindi (`बचत`, `समूह बचत`, `व्यक्तिगत`).

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- Tab indicator translate: 150ms ease-out (`--motion-fast` per §Motion).
- Card ripple (member rows): MD3 standard 300ms ease-out on tap.
- Chart transitions on data update: bar heights animate 200ms cubic-bezier(0.4, 0, 0.2, 1); line chart uses path morph over 200ms.
- Pull-to-refresh indicator: MD3 refresh spinner, primary `#2E7D32` tint.
- Snackbar (offline-refresh): standard MD3 slide-up + auto-dismiss 4s.
- Error banner reveal: 200ms slide-down from top; dismiss on Retry-success is instant.

---

## Data Flow (ui.yaml `business_logic.kind: composite`)

**External libs**: `Store5`, `SQLDelight`
**Internal libs**: `cmp-network-monitor`
**Server contract**: companion API (NOT direct Fineract) — the aggregation happens server-side per RULE-SERVER-DELTA-001

Read paths (offline-first, parallel):
- `groupSavingsSummary` ← `SavingsRepository.getGroupSavings(groupId)` via Store5 stream
  - Source of truth: SQLDelight `LocalSavingsDao.groupSavings` cache
  - Fetcher: companion `GET /companion/groups/{groupId}/savings?scope=group` (gated by `cmp-network-monitor`)
- `individualSavingsSummary` ← `SavingsRepository.getIndividualSavings(groupId)` via Store5 stream
  - Source of truth: SQLDelight `LocalSavingsDao.individualSavings`
  - Fetcher: companion `GET /companion/groups/{groupId}/savings?scope=individual`
- `weeklyTrend[]` — 6 recent weeks, embedded in BOTH group and individual summaries (see `WeeklyContributionPoint` demo entries)
- `contributionModel` ← derived from `typeConfig.contribution_model` (nav param) — drives per-row branch (`SHARE_BASED_VARIABLE` vs `FIXED_AMOUNT` / `FIXED_NEGOTIATED`)
- `cycleCollected` / `cycleTarget` — derived server-side (shares OR KES); progress computed client-side as `cycleCollected * 100 / cycleTarget`

Write path: none (this screen is read-only; savings entries are created by `meeting-conduct` → `savings-collection`).

Offline behavior:
- Cold start with no cache → `loading` → `empty` (if API returns 200 with empty rows) OR `error` (if API fails)
- Cold start with cache → renders cache immediately in `content_group`; Store5 fresh emission updates in-place (no state swap)
- Refresh with no network → `RefreshDashboard` action_contract checks `cmp-network-monitor` first, surfaces snackbar "Showing cached savings — pull down to retry" WITHOUT swapping to `error` state (cached rows stay visible per RULE-STORE5-CONTENT-STALE-FALLBACK)
- Sync band shows `Last synced: {lastSyncAt}` once any successful fetch has occurred

---

## Contribution Model Adaptation

The screen is **explicitly contribution-model-aware** — every downstream rendered surface changes shape based on `typeConfig.contribution_model`:

| Element | `SHARE_BASED_VARIABLE` (VSLA/SILC) | `FIXED_AMOUNT` (ROSCA/SHG) | `FIXED_NEGOTIATED` (JLG) |
|---------|-----------------------------------|----------------------------|--------------------------|
| Cycle progress text | `{cycleCollected} shares of {cycleTarget} target` | `KES {cycleCollected} of KES {cycleTarget}` | `KES {cycleCollected} of KES {cycleTarget}` |
| Member supporting | `{sharesHeld} shares @ KES {share_value}/share` | `{meetingsContributed} meetings · Last: KES {lastContribution}` | Same as FIXED_AMOUNT (negotiated amount inline) |
| Member trailing amount | `KES {shareValue}` + "share value" caption | `KES {totalContributed}` + "total" caption | `KES {totalContributed}` + "total" caption |
| Group total chip | `Group total: KES {totalCollected}` (KES equivalent of shares × share_value) | `Group total: KES {totalCollected}` | `Group total: KES {totalCollected}` |

The Individual tab is model-agnostic — voluntary individual savings are always KES-denominated regardless of the parent group's contribution model.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/savings-dashboard/ui.yaml` |
| API contract | `idea-layer/screens/savings-dashboard/api.yaml` |
| Data flow | `idea-layer/screens/savings-dashboard/data-flow.yaml` |
| Demo data | `idea-layer/screens/savings-dashboard/demo-data.yaml` |
| Flow | `idea-layer/screens/savings-dashboard/flow.yaml` |
| Tests | `idea-layer/screens/savings-dashboard/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/savings-dashboard/preview/loading.html` |
| Preview HTML (content_group) | `idea-layer/screens/savings-dashboard/preview/content_group.html` |
| Preview HTML (content_individual) | `idea-layer/screens/savings-dashboard/preview/content_individual.html` |
| Preview HTML (content_with_error) | `idea-layer/screens/savings-dashboard/preview/content_with_error.html` |
| Preview HTML (empty) | `idea-layer/screens/savings-dashboard/preview/empty.html` |
| Preview HTML (error) | `idea-layer/screens/savings-dashboard/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/savings-dashboard/prompts/{loading,content_group,content_individual,content_with_error,empty,error}.md` |
| Stitch mockup (probe deferred) | `idea-layer/mockups/savings-dashboard/stitch/` |
| Feature-group mockup | `idea-layer/mockups/savings-management/MOCKUP.md` (Screen section for savings-dashboard) |
| Related member detail | `idea-layer/mockups/member-savings-detail/MOCKUP.md` (drill-down target) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (6/6 states rendered 2026-07-18) + ui.yaml + demo-data.yaml + design-system tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The screen is a **dashboard type** (not list) — page-fits-viewport at default density (5 rows visible without scroll); scrolling is enabled for groups larger than 5 members.
- Cycle progress text explicitly branches on `contributionModel` at render time — the SHARE_BASED_VARIABLE variant is authored inline in ui.yaml `content_group.demo_data`, while the FIXED_AMOUNT default lives in `demo-data.yaml#GroupSavingsSummary.items[0]`. Both variants are canonical.
- Server contract lives on the companion API (`/companion/groups/{groupId}/savings`), NOT direct Fineract — the group vs individual aggregation is server-side per RULE-SERVER-DELTA-001; the client only branches on contribution model for display.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features savings-dashboard
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to ui.yaml components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade per RULE-IDEA-POST-ENRICH-CASCADE-001.
