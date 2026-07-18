# Field Officer Dashboard — Mockup Specification

**Feature**: field-officer-dashboard | **Route**: `/field-officer/dashboard` | **Type**: dashboard
**Feature group**: field-officer-management | **Flow**: field-officer-management-flow
**Generated from**: `screens/field-officer-dashboard/ui.yaml`, `screens/field-officer-dashboard/demo-data.yaml`, `design-system/DESIGN.md`
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature field-officer-dashboard`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for KES amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar fill, GREEN health chip, active filter chip fill, KPI Groups card
**Primary container**: `#C8E6C9` on `#1B5E20` — GREEN "Healthy" badge, KPI Groups card bg
**Secondary container**: — KPI Members card bg (blue-green tone)
**Tertiary container**: on `--accent-100` — KPI Savings card bg (amber tone, pooled-fund metaphor)
**Error container**: `#FFCDD2` on `#B71C1C` — KPI Loans Outstanding card bg (danger emphasis), RED "Critical" badge, Clear-Filters chip fill
**Warning container**: `#FFF9C4` on `#E65100` — AMBER "At Risk" badge
**Surface variant**: `#F5F5F5` — shimmer skeletons, unselected filter chip fill
**Background**: `#FFFFFF` canvas · `#FAFAFA` app
**Corner radius**: 12dp KPI cards + group cards + shimmer skeletons · 16px filter chips · 8px health badges
**Elevation**: 2dp group health cards · 0dp KPI cards (container-color only)
**Min touch target**: 72dp group card · 48dp filter chip · 44dp export action · 88dp KPI card min-height
**Reduced motion**: `prefers-reduced-motion: reduce` disables shimmer + pull-to-refresh spinner rotation

---

## Screen: Field Officer Dashboard

### Entry
- From **app_launch** when `userRole ∈ {FIELD_OFFICER, PROGRAM_MANAGER}` — default landing after login
- From **bottom_nav** "Dashboard" tab (for the same two roles)
- Back navigation exits the app (root of the field-officer session, no pop target)

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ Field Officer Dashboard        [ ⬇ ]    │  top_app_bar — primary #2E7D32 fill,
│                                          │  onPrimary title text · export_action icon
│                                          │  arrow_download_24_regular right, 44dp target
├─────────────────────────────────────────┤
│  ┌──────┐ ┌──────┐ ┌────────┐ ┌────────┐│  kpi_cards_row — horizontal scroll,
│  │  5   │ │ 54   │ │KES 178k│ │KES 129k││  16dp padding, 12dp gap, 88dp min-height
│  │Groups│ │Active│ │Savings │ │ Loans  ││  KPI card layout:
│  │Manag │ │Membrs│ │This Mon│ │Outstand││    - value  headlineMedium bold (top)
│  │  👥  │ │  🧑  │ │  🐖    │ │  💰    ││    - label  bodySmall
│  │primry│ │secndr│ │tertiary│ │ error  ││    - icon   24dp bottom-right corner
│  └──────┘ └──────┘ └────────┘ └────────┘│  bg tokens: primaryContainer /
│                                          │  secondaryContainer / tertiaryContainer /
│                                          │  errorContainer (4 distinct MD3 tones)
├─────────────────────────────────────────┤
│  [📍 All Regions] [🔎 All Statuses] →   │  filter_row — horizontal scroll,
│  [⚠ Any Overdue Rate]                    │  16dp horizontal padding, 8dp bottom, 8dp gap
│                                          │  filter_chip 16px corner · icon + label
│                                          │  selected_when != null → primaryContainer fill
├─────────────────────────────────────────┤
│  5 of 5 groups                           │  groups_list_header — titleSmall,
│                                          │  onSurfaceVariant, 16dp horizontal pad
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ Mwangaza Women's Group            │   │  group_health_card — surface bg, 2dp elev,
│  │ Kisumu West · Cycle 1             │   │  12dp corner, 16dp pad, 72dp min-touch,
│  │                                    │   │  16dp horizontal margin, 8dp bottom margin
│  │  [✓ Healthy]                       │   │  content:
│  └──────────────────────────────────┘   │    - name  titleMedium onSurface
│  ┌──────────────────────────────────┐   │    - office · cycle  bodySmall onSurfaceVariant
│  │ Tumaini Savings Group             │   │    - health_badge — GREEN primaryContainer,
│  │ Kisumu West · Cycle 2             │   │      AMBER warningContainer, RED errorContainer
│  │                                    │   │  → on_click OnGroupTapped → group-dashboard(id)
│  │  [⚠ At Risk]                       │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │ Baraka Chama                      │   │
│  │ Kisumu East · Cycle 3             │   │
│  │  [✓ Healthy]                       │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │ Imara Savings Circle              │   │
│  │ Kisumu East · Cycle 1             │   │
│  │  [✗ Critical]                      │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │ Upendo Women's Group              │   │
│  │ Kisumu West · Cycle 2             │   │
│  │  [✓ Healthy]                       │   │
│  └──────────────────────────────────┘   │
│              ↕ pull-to-refresh           │  OnRefresh gesture — Store5 fresh=true
└─────────────────────────────────────────┘
```

### KPI Card Detail (repeated pattern × 4)

```
┌──────────────────────┐
│                      │
│  5                   │  value  headlineMedium onPrimaryContainer bold (Roboto Mono)
│                      │
│  Groups Managed      │  label  bodySmall onPrimaryContainer, 4dp top margin
│                      │
│                 👥   │  icon   people_24_regular 20dp onPrimaryContainer,
│                      │  bottom-right corner
└──────────────────────┘
 min-width 140dp (or 156dp for Savings/Loans to fit KES notation)
 min-height 88dp · corner 12dp · padding 16dp
 bg: {primary|secondary|tertiary|error}Container per KPI
```

**Number formatting**: KES amounts use `| compact` filter — `KES 142,000` becomes `KES 142k`, `KES 1,250,000` becomes `KES 1.25M`. Groups + members shown as bare integers.

### Filter Chip Detail

Three filter dimensions (region / status / overdue-rate) plus a Clear-Filters chip that appears when any filter is active.

```
Unselected:  ┌ 📍 All Regions ────┐   surfaceVariant bg, onSurface text, 16px corner
             └───────────────────┘   → ShowRegionPickerDialog

Selected:    ┌ 📍 Kisumu West   ●─┐   primaryContainer bg, onPrimaryContainer text,
             └───────────────────┘   trailing dot indicates selection

Clear:       ┌ ✕ Clear Filters ──┐   errorContainer bg, onErrorContainer text,
             └───────────────────┘   visible_when any filter != null
                                     → OnClearFilters (transform_state)
```

- Region filter → `OnRegionFilterSelected(region)` after picker dialog
- Status filter → `OnStatusFilterSelected(status)` — ACTIVE / PENDING / CLOSED
- Overdue filter → `OnOverdueFilterSelected(filter)` — NONE / LESS_THAN_10 / GREATER_THAN_10
- Any of these emit a picker dialog first (`emit_event`) then the resolved value updates `selectedRegionFilter` / `selectedStatusFilter` / `selectedOverdueFilter` and recomputes `filteredGroups` client-side.

### Group Health Card Detail

```
┌──────────────────────────────────────┐
│ Baraka Chama                          │  group_name_text — titleMedium onSurface
│ Kisumu East · Cycle 3                 │  group_office_text — bodySmall onSurfaceVariant,
│                                       │  2dp top margin, format: "{officeName} · Cycle {n}"
│  [✓ Healthy]                          │  group_health_badge — 8dp top margin
└──────────────────────────────────────┘  full row clickable, ripple on onSurface
 elev 2dp · corner 12dp · pad 16dp · min-touch 72dp
 margin: 0dp horizontal 16dp bottom 8dp
```

Badge palette (single semantic dimension):

| healthIndicator | Fill                 | Text color         | Label      |
|-----------------|----------------------|--------------------|------------|
| GREEN           | primaryContainer     | onPrimaryContainer | "Healthy"  |
| AMBER           | warningContainer     | onWarningContainer | "At Risk"  |
| RED             | errorContainer       | onErrorContainer   | "Critical" |

Tap → `OnGroupTapped(groupId)` (navigate) → NavController push `group-dashboard` (read-only supervisory mode — field officers cannot mutate group state from that screen).

---

## Demo Data (state: `content`, from `demo-data.yaml`)

Field officer David Otieno (staffId 1001) manages 5 VSLA groups across Kisumu offices. Portfolio mix designed to exercise every health-indicator branch and both region-filter values.

### KPI aggregates (client-side sum over GroupHealthSummary list)

| KPI                  | Value       | Formula                                             |
|----------------------|-------------|-----------------------------------------------------|
| Groups Managed       | 5           | `groups.size`                                        |
| Active Members       | 54          | Σ `group.activeClientCount` (12+8+15+10+9)          |
| Savings This Month   | KES 178,100 | Σ `group.totalSavingsBalance` (Roboto Mono, compact) |
| Loans Outstanding    | KES 129,000 | Σ `group.totalLoansOutstanding`                     |

### Group portfolio

| id | Group                     | Office        | Members | Savings KES | Loans KES | Overdue | Health  | Cycle |
|----|---------------------------|---------------|---------|-------------|-----------|---------|---------|-------|
| 1  | Mwangaza Women's Group    | Kisumu West   | 12      | 48,000      | 32,000    | 2%      | GREEN   | 1     |
| 2  | Tumaini Savings Group     | Kisumu West   | 8       | 21,600      | 15,000    | 8%      | AMBER   | 2     |
| 3  | Baraka Chama              | Kisumu East   | 15      | 63,000      | 42,000    | 0%      | GREEN   | 3     |
| 4  | Imara Savings Circle      | Kisumu East   | 10      | 18,500      | 22,000    | 25%     | **RED** | 1     |
| 5  | Upendo Women's Group      | Kisumu West   | 9       | 27,000      | 18,000    | 4%      | GREEN   | 2     |

**Health indicator threshold** (business rule):
- `overdueRate ≤ 0.05` → GREEN (Healthy)
- `0.05 < overdueRate ≤ 0.20` → AMBER (At Risk)
- `overdueRate > 0.20` → RED (Critical)

### Available regions (derived client-side for picker)

`["Kisumu West", "Kisumu East"]` — extracted via `groups.map { it.officeName }.distinct()`.

### Session

- `staffId: 1001` · `userRole: FIELD_OFFICER` → `canExport: true`
- `isExporting: false` → export icon renders as static download glyph
- `selectedRegionFilter: null · selectedStatusFilter: null · selectedOverdueFilter: null` → all filter chips in unselected surfaceVariant state; Clear-Filters chip hidden

### Export payload (stub)

Tapping the export action posts a Fineract `runreports/FieldOfficerGroupReport?staffId=1001` request, receives `FieldOfficerGroupReport_1001.csv` (~2KB CSV), and hands it to the OS share sheet (`Intent.ACTION_SEND` on Android / `UIActivityViewController` on iOS).

---

## States (screen_state)

The ui.yaml declares 4 `screen_state` members driving the dashboard shell. Each renders as a distinct HTML preview surface under `preview/`.

### `loading`

Shimmer skeleton mirroring the content layout — parallel fetch of `groups`, `staff`, `kpis` from SQLDelight cache + Fineract API (`GET /centers?staffId=1001&fields=groups`).

```
┌ Field Officer Dashboard  [ ⬇ ]  ────────┐  top_bar visible with title (no shimmer)
├────────────────────────────────────────┤
│  [ shimmer 140dp × 88dp ] × 4           │  KPI row skeleton (surfaceVariant, 12dp corner)
├────────────────────────────────────────┤
│  [ shimmer 100dp × full ] × 6           │  Group card skeletons, 100dp height,
│  [ shimmer 100dp × full ]               │  12dp corner, 16dp horizontal margin,
│  [ shimmer 100dp × full ]               │  8dp bottom margin, 1.4s ease-in-out infinite
│  [ shimmer 100dp × full ]               │
│  [ shimmer 100dp × full ]               │
│  [ shimmer 100dp × full ]               │
└────────────────────────────────────────┘
```

- Top bar retains title; export action hidden until `canExport` resolved.
- Filter chips inert during load (no shimmer chip row per ui.yaml — only skeleton cards).
- Respects `prefers-reduced-motion: reduce` (animation disabled).

### `content` (see layout above)

Data loaded; 4 KPI cards + 3 filter chips + group health card list. Pull-to-refresh gesture triggers `OnRefresh` → Store5 `fresh=true` re-fetch.

### `empty` — no groups assigned

```
┌ Field Officer Dashboard  [ ⬇ ]  ────────┐  top_bar retained (export disabled — no data)
├────────────────────────────────────────┤
│                                          │
│                                          │
│                 👥                       │  empty_state · people_24_regular icon 64dp,
│         No Groups Assigned               │  onSurfaceVariant tint
│                                          │  title titleLarge, body bodyMedium
│  You don't have any groups assigned      │  --text-secondary
│  yet. Contact your office administrator. │
│                                          │
│                                          │
└──────────────────────────────────────────┘
```

- No KPI row (there's nothing to aggregate).
- No filter row (nothing to filter).
- Export action disabled (`canExport: true` but `groups.isEmpty()` — CSV would be empty).

### `empty_filter` — filters exclude all groups (composed state)

```
┌ Field Officer Dashboard  [ ⬇ ]  ────────┐
├────────────────────────────────────────┤
│  [KPI row remains — aggregates over ALL groups, not filtered] │
├────────────────────────────────────────┤
│  [📍 Kisumu North] [🔎 CLOSED] [⚠ >10%]  │  filter chips reflect active selection
│  [✕ Clear Filters]                       │
├────────────────────────────────────────┤
│  0 of 5 groups                           │  groups_list_header shows zero match
├────────────────────────────────────────┤
│                                          │
│                 🔍                       │  empty_filter_state
│    No Groups Match Filters               │  filter_dismiss_24_regular icon
│  Try adjusting or clearing your filters. │  title titleLarge, body bodyMedium
│                                          │
│   ┌────── Clear Filters ─────────────┐  │  cta_button — primary #2E7D32 fill,
│   └─────────────────────────────────┘  │  onPrimary text, 48dp min-height
│                                          │  → OnClearFilters (transform_state)
└──────────────────────────────────────────┘
```

- KPI cards remain populated (aggregates always compute over full `groups`, never `filteredGroups`).
- Filter chips remain in-place so the user sees which selections excluded the list.
- Clear Filters primary CTA duplicates the Clear-Filters chip's affordance (thumb-reach convenience).

### `error`

Fineract API failed AND cache is empty — full-surface retry state. When cache HAS rows, the toast fallback keeps the content visible (see `error_network` copy).

```
┌ Field Officer Dashboard  ─────────────  │  top_bar retained (no export — no data)
├────────────────────────────────────────┤
│                                          │
│                                          │
│               ☁                          │  error_state · wifi_off_24_regular icon 64dp
│    Could not load dashboard              │  title titleLarge
│                                          │
│    {error.message}                       │  body bodyMedium --text-secondary
│    e.g. "No internet connection.         │
│    Showing cached data."                 │
│                                          │
│   ┌────── Retry ────────────────────┐  │  cta_button — primary #2E7D32,
│   └──────────────────────────────────┘  │  onPrimary text, 48dp min-height
│                                          │  → OnRetry (call_api, fresh=true)
└──────────────────────────────────────────┘
```

Error taxonomy (typed via `FieldOfficerDashboardError`):
- `Network` — retry:true, `error_network` "No internet connection. Showing cached data."
- `Server` — retry:true, `error_server` "Server error. Please try again."
- `Auth` — retry:false, `error_auth` "Session expired. Please log in again." → redirect to `login`
- `NoGroupsAssigned` — retry:false, `error_no_groups` "No groups assigned to your account." → falls through to `empty` state visual

---

## Interaction Patterns

1. **KPI card view** (non-interactive) — 4 cards render aggregates; no tap handler by design (drill-down happens via group list, not KPI). Cards use 4 distinct MD3 container tones so each metric is visually distinguishable at a glance (primary=count, secondary=members, tertiary=savings, error=loans — matches the "loans outstanding demand attention" mental model).
2. **Group card tap** → `OnGroupTapped(groupId)` (effect: `navigate`) → NavController push `group-dashboard` with `groupId`. Card uses 72dp min-touch and full-row ripple; group opens in read-only supervisory mode (field officer cannot mutate group state).
3. **Region filter tap** → `ShowRegionPickerDialog` (emit_event) → modal picker built from `availableRegions` (client-derived from `groups.map { officeName }.distinct()`). Selection posts `OnRegionFilterSelected(region)` (transform_state).
4. **Status filter tap** → `ShowStatusPickerDialog` (emit_event) → modal picker with ACTIVE / PENDING / CLOSED options. Selection posts `OnStatusFilterSelected(status)`.
5. **Overdue filter tap** → `ShowOverduePickerDialog` (emit_event) → modal picker with `NONE / LESS_THAN_10 / GREATER_THAN_10` thresholds. Selection posts `OnOverdueFilterSelected(filter)`.
6. **Clear-filters chip tap** (visible only when any filter active) → `OnClearFilters` (transform_state) → resets all three selectors to `null` and restores `filteredGroups = groups`.
7. **Export report tap** (top app bar action, gated) → `OnExportReport` (call_api, external `Fineract runreports API`) → posts `runreports/FieldOfficerGroupReport?staffId={staffId}` over cmp-network-monitor-gated HTTP; receives CSV `FileResponse`; hands to OS share sheet. Action visible only when `canExport == true` (FIELD_OFFICER or PROGRAM_MANAGER); shows loading spinner while `isExporting == true`; failure surfaces `ShowSnackbar("Failed to generate report. Please try again.")`.
8. **Pull to refresh** → `OnRefresh` (transform_state → invalidate_cache) → Store5 `fresh=true` reload, resets `isRefreshing=true` during the fetch, retains active filter selections.
9. **Retry tap (error state)** → `OnRetry` (call_api) → re-runs the parallel `getCentersAndGroups` fetch, invalidates SQLDelight cache, re-aggregates KPIs.
10. **Empty-filter Clear tap** → `OnClearFilters` (transform_state) → same as filter chip Clear-Filters; also handles the empty-filter-results state as its own affordance.

---

## Accessibility

- KPI cards labeled semantically for TalkBack/VoiceOver: "{value} {label}" pattern — e.g. "5 Groups Managed", "KES 178 thousand Savings This Month". Icons are decorative (`accessibilityElementsHidden`).
- Filter chips carry `role: tab`; selected chip announces `aria-selected="true"`; state changes announce as "Region filter set to Kisumu West" / "Filter cleared".
- Group cards expose a single semantic action per row: "Open group {name} in {office} — health status {healthIndicator}, cycle {n}". Tap invokes `group-dashboard`.
- Health indicator is text + colored badge — never color-only (badge label always readable: "Healthy" / "At Risk" / "Critical").
- KPI colors mapped to MD3 containers WCAG-AA compliant (contrast ≥ 4.5:1 for body text): primaryContainer #C8E6C9 with onPrimaryContainer #1B5E20 = 8.2:1.
- Min touch targets: 72dp group card, 48dp filter chip, 44dp export action, 88dp KPI card min-height.
- Locales covered: English, Swahili (`Dashibodi ya Afisa Shamba` / `Vikundi Vinavyosimamiwa` / `Toa Ripoti`), French (`Tableau de Bord Agent de Terrain`), Hindi (`फील्ड ऑफिसर डैशबोर्ड` / `प्रबंधित समूह`).
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS up to 200% without layout breakage.
- Reduced motion: shimmer, pull-to-refresh spinner, and picker-dialog fade transitions all collapse to static frames under `prefers-reduced-motion`.

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- KPI value change (on refresh): 250ms crossfade primaryContainer highlight → base → normal.
- Filter chip selection: 150ms fill transition (surfaceVariant → primaryContainer) + 300ms ripple.
- Group card ripple: MD3 standard 300ms ease-out on tap over full-row surface.
- Pull-to-refresh: MD3 refresh indicator, matches primary `#2E7D32`, 800ms rotation cycle.
- Export action loading: MD3 CircularProgressIndicator swap in-place of download icon (24dp, onPrimary tint).
- Snackbar (`ShowSnackbar` event): standard MD3 slide-up + 4000ms auto-dismiss (used for export success/failure toasts).
- Health badge color: no motion — instant paint on data load (avoids attention-grabbing on a monitoring surface).

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `Fineract REST API`, `SQLDelight`
**Internal lib**: `cmp-network-monitor`

Read paths (offline-first, parallel):
- `groups[]` ← `GroupRepository.getStaffPortfolio(staffId)` via Store5 stream
  - Source of truth: SQLDelight `group_health_summary` cache (TTL 300s)
  - Fetcher: Fineract `GET /centers?staffId={staffId}&fields=groups,activeClientCount,totalSavingsBalance,totalLoansOutstanding,overdueRate` (gated by `cmp-network-monitor`)
  - `OnRetry` triggers `fresh=true`, `OnRefresh` triggers cache invalidation
- `staff` (session context) ← `StaffRepository.getCurrent()` from `SessionManager` (already resolved at app_launch; drives `canExport`)
- `filteredGroups[]` — derived state: `groups.filter { selectedRegionFilter/Status/Overdue matches }` (client-side, no network)
- `availableRegions[]` — derived: `groups.map { officeName }.distinct().sorted()` (client-side)
- KPI aggregates (`totalGroupsCount / totalActiveMembers / totalSavingsThisMonth / totalLoansOutstanding`) — computed client-side over `groups` (not `filteredGroups`, so aggregates reflect the full portfolio regardless of active filters)

Write paths:
- Export CSV (`OnExportReport`) → `ReportRepository.exportFieldOfficerGroupReport(staffId)` → Fineract `POST /runreports/FieldOfficerGroupReport` → `FileResponse{mimeType: "text/csv", filename, content: ByteArray}` → OS share sheet.

Offline behavior — when `NetworkMonitor.isOffline == true`, SQLDelight cache rows still render and `Network` error surfaces as a non-blocking snackbar/toast ("No internet connection. Showing cached data.") — the list itself stays in `content` state. Export is disabled offline (report generation requires live Fineract call).

Session gating — export action visibility is triple-gated: `canExport == true` (derived from `userRole ∈ {FIELD_OFFICER, PROGRAM_MANAGER}`) AND `groups.isNotEmpty()` (nothing to export from empty portfolio) AND `NetworkMonitor.isOnline` (offline mode disables generation).

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/field-officer-dashboard/ui.yaml` |
| API contract | `idea-layer/screens/field-officer-dashboard/api.yaml` |
| Data flow | `idea-layer/screens/field-officer-dashboard/data-flow.yaml` |
| Demo data | `idea-layer/screens/field-officer-dashboard/demo-data.yaml` |
| Flow | `idea-layer/screens/field-officer-dashboard/flow.yaml` |
| Tests | `idea-layer/screens/field-officer-dashboard/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/field-officer-dashboard/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/field-officer-dashboard/preview/content.html` |
| Preview HTML (empty) | `idea-layer/screens/field-officer-dashboard/preview/empty.html` |
| Preview HTML (error) | `idea-layer/screens/field-officer-dashboard/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/field-officer-dashboard/prompts/{loading,content,empty,error}.md` |
| Feature-group mockup | `idea-layer/mockups/field-officer-management/MOCKUP.md` |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from `ui.yaml` + `demo-data.yaml` + `design-system/DESIGN.md` per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The 4 KPI cards deliberately use 4 different MD3 container tones (primary / secondary / tertiary / error) instead of a uniform surface, following the design-system's "regulated-industry + accessibility-first" quiet constraint: distinct color coding lets a field officer scan the row at 3 metres without reading labels. The error-container tone on "Loans Outstanding" is intentional — it flags that this metric warrants monitoring in a lending portfolio, not that a specific alert is firing.
- The `crud` business_logic kind allows this screen to lean on the existing `kmp-screen-gen` template path (AC-03i zero-regression per RULE-IDEA-IMPL-INTELLIGENCE-001 II-4).
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features field-officer-dashboard
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to ui.yaml components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
