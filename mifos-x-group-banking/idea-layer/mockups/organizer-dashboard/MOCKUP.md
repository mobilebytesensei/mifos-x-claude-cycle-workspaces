# Organizer Dashboard — Mockup Specification

**Feature**: organizer-dashboard | **Route**: `/dashboard/organizer` | **Type**: dashboard
**Feature group**: unified-auth | **Flow**: auth-flow
**Generated from**: `screens/organizer-dashboard/ui.yaml`, `screens/organizer-dashboard/demo-data.yaml`, `screens/organizer-dashboard/preview/*.html` (4 states rendered 2026-07-17)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature organizer-dashboard`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first · regulated-industry
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for KPI amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, KPI values, primary containers
**Primary container**: `#C8E6C9` (`--primary-100`) — welcome header, All-Groups quick-nav tile
**Accent**: `#FF8F00` (`--accent-700`, amber) — pooled fund emphasis (badge highlights, share-out contexts)
**Secondary container**: `#FFE082` (`--accent-100`) — Field-Officer optional-tier tile (v1.1)
**Tertiary container**: `#E1F5FE` on `#01579B` — schedule count chip
**Warning**: `#F57C00` (`--warning`) — pending share-outs, attention
**Danger**: `#C62828` (`--danger`) — nonzero Share-Outs Due value + KPI card border
**Muted**: `#616161` on `#F5F5F5` — labels, dividers, disabled
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (shimmer)
**Corner radius**: 12dp KPI cards · 16dp section cards · 0dp welcome header · 12dp shimmer skeletons
**Elevation**: 0dp welcome header + primary/secondary-container quick-nav tiles · 2dp KPI + section cards
**Min touch target**: 48dp KPI card · 56dp meeting-row list item · 56dp quick-nav tile

---

## Screen: Dashboard

### Entry
- From **app_launch** when `user_authenticated && isOrganizerInAnyGroup` (session `dt_member_role` resolves ≥1 group with organizer/treasurer/chairperson role) — unified identity, no admin login type
- Bottom-nav `home` tab is the selected tab on this route
- Back navigation exits the app (root of the organizer tab)

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│  Dashboard                    [🔔]      │  top_bar — primary #2E7D32, onPrimary text
│                                          │  bell icon → OnOpenNotifications (deferred snackbar)
├─────────────────────────────────────────┤
│  Welcome back, David Otieno              │  welcome_header · primaryContainer #C8E6C9,
│  Here's your overview for today          │  onPrimaryContainer text, 0dp elevation,
│                                          │  16 / 16 / 12 / 16 dp padding
├─────────────────────────────────────────┤
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────┐│  kpi_summary_row · 12dp gap, 12/16dp padding
│  │   5    │ │   42   │ │   1    │ │ 2  ││  Each card: surface bg, 2dp elev, 12dp corner,
│  │ My     │ │Members │ │Share-  │ │Mtgs││  14dp padding, flex:1
│  │Groups  │ │        │ │Outs Due│ │Today│  headlineMedium primary #2E7D32 for value
│  │        │ │        │ │ (RED)  │ │(sec)│  labelSmall onSurfaceVariant for label
│  └────────┘ └────────┘ └────────┘ └────┘│  Share-Outs Due: RED border (1dp error) when >0,
│                                          │  value tints error #C62828 when nonzero
│                                          │  Meetings Today: secondary color #FF8F00
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │  quick_nav_section · surface, 2dp elev,
│  │ Quick Navigation                  │   │  16dp corner, 16dp padding, 0/16/8/16 dp margin
│  │                                    │   │
│  │  ┌────────────┐ ┌────────────┐   │   │  quick_nav_grid · 2 cols, 12dp gap
│  │  │ [👥]       │ │ [📍] Opt   │   │   │  nav_group_list_card · primaryContainer #C8E6C9,
│  │  │ All Groups │ │ Field      │   │   │  onPrimaryContainer text, 12dp corner, 0dp elev
│  │  │ 5 groups   │ │ Officers   │   │   │  → OnViewAllGroups → group-list
│  │  │            │ │ Officer    │   │   │
│  │  │            │ │ overview   │   │   │  nav_field_officer_card · secondaryContainer,
│  │  └────────────┘ └────────────┘   │   │  onSecondaryContainer text, "Optional" badge,
│  │                                    │   │  visible_when fieldOfficerEnabled == true
│  └──────────────────────────────────┘   │  (HIDDEN by default in this demo state)
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │  todays_schedule_section · surface, 2dp elev
│  │ Today's Schedule    [2 meetings] │   │  header row: titleMedium onSurface + chip
│  │                                    │   │  chip: tertiaryContainer, tertiary text
│  │  📅 Mwangaza Women's Group    ›  │   │  list-item · 56dp min touch, divider true
│  │     09:00 • 12 members            │   │  headline / supporting / trailing arrow
│  │  ─────────────────────────────    │   │  → OnMeetingGroupClick(groupId="GRP-…-001")
│  │  📅 Tumaini Savings Group     ›  │   │      → group-list with groupId nav-param
│  │     14:00 • 8 members             │   │
│  └──────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │  recent_activity_section · surface, 2dp elev
│  │ Recent Activity                   │   │  titleMedium onSurface
│  │                                    │   │
│  │  ⬆ Weekly contribution            │   │  activity_list_item · leading activity_type_icon,
│  │     — Amina Wanjiru               │   │  headline description, supporting date • group,
│  │     2026-05-09 • Mwangaza Women's │   │  trailing amount (Roboto Mono, currency: KES)
│  │                          KES 300  │   │
│  │  💰 Loan disbursed — Grace Akinyi │   │
│  │     2026-05-08 • Tumaini Savings  │   │
│  │                        KES 8,000  │   │
│  │  🎯 Share-out executed — cycle 1  │   │
│  │     2026-05-06 • Baraka Chama     │   │
│  │                       KES 24,000  │   │
│  │  ⬆ Weekly contribution            │   │
│  │     — Fatuma Hassan               │   │
│  │     2026-05-06 • Baraka Chama     │   │
│  │                          KES 400  │   │
│  │  👤 New member joined             │   │
│  │     — John Odhiambo               │   │  amount=null → trailing hidden
│  │     2026-05-05 • Baraka Chama     │   │
│  └──────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  [🏠 Home*] [📅 Meetings] [👤 Profile] │  bottom_nav · home tab selected
└─────────────────────────────────────────┘
```

### Demo Data (state: `content`, from `demo-data.yaml`)

Organizer David Otieno holds an organizer/treasurer/chairperson role across 5 active savings groups in the Kisumu region. Identity resolved server-side from the auth token via `dt_member_role` — no staffId param (replaces the old StaffSummary DTO):

| Field | Value | Notes |
|-------|-------|-------|
| organizerName | David Otieno | From `session.displayName` (unified identity) |
| myGroupCount | 5 | Groups where user holds organizer/treasurer/chairperson |
| totalMembers | 42 | Aggregate across all 5 groups |
| pendingShareOutCount | 1 | Share-outs due — savings-group analogue of "overdue loans" (loans→savings pivot) |
| meetingsTodayCount | 2 | Typical for a weekly-cycle Wednesday |
| fieldOfficerEnabled | false | Standard community organizer tier — v1.1 enterprise flag hidden by default |

**Today's Schedule (2 meetings):**

| groupId              | Group                       | Time  | Members | Location                                |
|----------------------|-----------------------------|-------|---------|-----------------------------------------|
| GRP-20260509-001     | Mwangaza Women's Group      | 09:00 | 12      | Mwangaza Community Centre, Kisumu West  |
| GRP-20260215-002     | Tumaini Savings Group       | 14:00 | 8       | St. Mary's Hall, Kisumu West            |

**Recent Activity (8 items, top 5 shown; scrolls):**

| id      | type       | Description                              | Amount (KES) | Date       | Group                       |
|---------|------------|------------------------------------------|--------------|------------|-----------------------------|
| ACT-001 | DEPOSIT    | Weekly contribution — Amina Wanjiru      | 300          | 2026-05-09 | Mwangaza Women's Group      |
| ACT-002 | DEPOSIT    | Weekly contribution — Joseph Kamau       | 500          | 2026-05-09 | Mwangaza Women's Group      |
| ACT-003 | LOAN       | Loan disbursed — Grace Akinyi            | 8,000        | 2026-05-08 | Tumaini Savings Group       |
| ACT-004 | MEETING    | Weekly meeting recorded                  | —            | 2026-05-07 | Mwangaza Women's Group      |
| ACT-005 | DEPOSIT    | Weekly contribution — Peter Mwangi       | 200          | 2026-05-07 | Mwangaza Women's Group      |
| ACT-006 | SHARE_OUT  | Share-out executed — cycle 1 complete    | 24,000       | 2026-05-06 | Baraka Chama                |
| ACT-007 | DEPOSIT    | Weekly contribution — Fatuma Hassan      | 400          | 2026-05-06 | Baraka Chama                |
| ACT-008 | NEW_MEMBER | New member joined — John Odhiambo        | —            | 2026-05-05 | Baraka Chama                |

- **KPI cards** — all four are tappable and route to `group-list` (except Meetings Today which also routes to group-list; group filter is not applied at KPI level).
- **Share-Outs Due card** — `pendingShareOutCount == 1` triggers RED 1dp border (`--danger #C62828`) and value tints error color. When 0, card renders in default primary color with no border.
- **Field Officer tile** — hidden in this demo (`fieldOfficerEnabled: false`). When enabled (v1.1), tile appears in the right column of `quick_nav_grid` with "Optional" badge and `person_pin_circle` icon.

---

## States

The ui.yaml declares 4 `screen_state` members (`Loading`, `Content`, `Error`, `Empty`) — each renders as a distinct HTML preview surface under `preview/`.

### `loading`
Shimmer skeleton mirroring the dashboard layout — parallel fetch of `OrganizerDashboardSummary` from SQLDelight cache + companion API `/companion/organizer/dashboard`.

```
[Dashboard header]                          ← top_bar visible, primary green
[Welcome back, {name}]                      ← welcome_header visible with primaryContainer bg
────────────────────────────────────────
[shimmer 100dp × full width, 16dp corner]   ← shimmer_dashboard count: 4
[shimmer 100dp × full width, 16dp corner]      surfaceVariant #F5F5F5
[shimmer 100dp × full width, 16dp corner]      1.4s ease-in-out infinite
[shimmer 100dp × full width, 16dp corner]      one per section (KPI row / quick-nav / schedule / activity)
```

- Cards: 100dp × full width, 16dp corner, `surfaceVariant` background shimmering 1.4s ease-in-out infinite.
- Respects `prefers-reduced-motion: reduce` (animation disabled).
- Top bar retains title "Dashboard" and the notifications bell (inert, no ripple).
- Welcome header retains greeting with a shimmer over `{{organizerName}}` if session not yet resolved.

### `content` (see layout above)
Dashboard summary loaded from Store5 stream over SQLDelight-cached companion response. All KPI cards, quick-nav grid, Today's Schedule, and Recent Activity render live. Bottom-nav visible with the home tab selected.

### `empty`
Session user has no groups assigned (edge case — `myGroupCount == 0`); e.g. a freshly-invited chairperson before the first group has been synced from the branch.

```
┌ Dashboard ─────────────────────────────┐
│  Welcome back, David Otieno             │  welcome_header retained
├────────────────────────────────────────┤
│                                          │
│               🗂                         │  empty_state · icon dashboard_customize
│           No groups yet                  │  title · titleLarge
│                                          │
│    Groups you organize will              │  body · bodyMedium, --text-secondary
│    appear here once set up.              │
│                                          │
│  ┌─────── View Groups ─────────────┐   │  cta_label · primary #2E7D32, 48dp
│  └────────────────────────────────┘    │  → OnViewAllGroups (effect: navigate)
│                                          │      → group-list
└─────────────────────────────────────────┘
```

- Illustration uses `dashboard_customize` outlined icon at 64dp, `onSurfaceVariant` tint.
- CTA is enabled even in empty state — tapping opens the (also-empty) group-list where the organizer can start setup.
- KPI row, quick-nav grid, Today's Schedule, and Recent Activity are suppressed — welcome_header + empty_state only.

### `error`
Companion API failed AND cache is empty — full-screen retry surface. When cache HAS rows, the toast fallback keeps the content visible (see `error_network` copy).

```
┌ Dashboard ─────────────────────────────┐
│                                          │
│                                          │
│               ☁                          │  error_state · cloud_off icon
│      Could not load dashboard            │  title · titleLarge
│                                          │
│    {error.message}                       │  body · bodyMedium, --text-secondary
│    e.g. "No internet connection.         │
│    Showing cached data."                 │
│                                          │
│  ┌─────── Retry ──────────────────┐    │  cta_label · primary #2E7D32, 48dp
│  └────────────────────────────────┘    │  → Retry action_contract effect: call_api
│                                          │  cmp-network-monitor gated; re-hits companion
│                                          │  API with fresh=true, bypasses SWR cache
└─────────────────────────────────────────┘
```

Error types (from `OrganizerDashboardError`):
- `Network` — retry:true, `error_network` "No internet connection. Showing cached data."
- `Server` — retry:true, `error_server` "Server error. Please try again."
- `Auth` — retry:false, `error_auth` "Session expired. Please log in again." → redirect to `group-list` (unified identity re-landing)

---

## Interaction Patterns

1. **KPI card tap (My Groups / Members / Share-Outs Due / Meetings Today)** → `OnViewAllGroups` (effect: `navigate`) → NavController push `group-list`. All four KPIs currently route to the same destination (no per-KPI filter at this tier).
2. **All Groups quick-nav tile tap** → `OnViewAllGroups` (effect: `navigate`) → NavController push `group-list`. Same target as the KPI cards; the sublabel `"{{totalGroups}} groups"` shows the live count (5 in demo).
3. **Field Officer quick-nav tile tap (v1.1 only)** → `OnViewFieldOfficer` (effect: `navigate`) → NavController push `field-officer-dashboard`. Guarded by `flow_logic.on_view_field_officer.guard: fieldOfficerEnabled` — dispatched only when the flag is true in the companion response.
4. **Today's Schedule meeting row tap** → `OnMeetingGroupClick(groupId)` (effect: `navigate`) → NavController push `group-list` with `groupId` nav-param (pre-filter). 56dp min touch target with full-row ripple + trailing chevron.
5. **Notifications bell tap** → `OnOpenNotifications` (effect: `emit_event`) → emits a `NotificationsDeferred` event surfaced as a snackbar informing the organizer that the notifications centre arrives in a later release (deferred per `release_plan.deferred[]`); no navigation until that screen ships.
6. **Pull to refresh** → `OnRefresh` (flow `invalidate_cache: true`) → Store5 fresh=true reload; welcome header + top_bar remain, all cards shimmer-swap in place, `isRefreshing: true` while in flight.
7. **Retry tap (error state)** → `Retry` (effect: `call_api`, external: Store5 + cmp-network-monitor) → Store5 stream with `fresh=true` re-hits companion `GET /companion/organizer/dashboard` and repopulates all four sections.

---

## Accessibility

- Every KPI card exposes a single semantic action ("Show groups; {value} {label}").
- Share-Outs Due card communicates the nonzero warning via both text (RED value) AND the error-tinted border — never color-only. The badge/border is supplemented by the explicit label "Share-Outs Due".
- Field Officer tile carries an "Optional" badge — screen readers announce it as `role="button"` with an appended "optional" hint so users don't confuse the tier gate for a bug.
- Notifications bell has `content_description: "Notifications"`; the deferred snackbar itself is announced via `ARIA live=polite`.
- Meeting rows carry semantic label "Go to {groupName}, meeting at {meetingTime} with {memberCount} members".
- Min touch target 48dp on KPI cards, 56dp on meeting-row list items, 56dp on quick-nav tiles.
- Locales covered: English, Swahili (`Vikundi Vyangu` / `Ratiba ya Leo`), French (`Mes Groupes` / `Programme du Jour`), Hindi (`मेरे समूह` / `आज का कार्यक्रम`).
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS.

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- KPI card ripple: MD3 standard 300ms ease-out on tap.
- Quick-nav tile press: MD3 elevation change 0dp → 2dp + ripple.
- Meeting row ripple: full-row 300ms ease-out with 56dp min touch.
- Share-Outs Due nonzero transition: border color animates from transparent → `#C62828` over 200ms when `pendingShareOutCount` crosses 0→n.
- Pull-to-refresh spinner: MD3 refresh indicator, matches primary `#2E7D32`.
- Snackbar (`ShowSnackbar` event): standard MD3 slide-up + auto-dismiss 4s (used for the notifications-deferred banner and the cached-data fallback banner).

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `Store5`, `SQLDelight`
**Internal lib**: `cmp-network-monitor`

Read paths (offline-first):
- `OrganizerDashboardSummary` ← `OrganizerDashboardRepository.getOrganizerDashboard()` via Store5 stream
  - Source of truth: SQLDelight `organizer_dashboard_cache` entity
  - Fetcher: companion `GET /companion/organizer/dashboard` (single call replaces the legacy 3 raw Fineract calls: `/staff/{id}/summary` + `/centers` + `/journal-entries`)
  - Gated by `cmp-network-monitor` — when `NetworkMonitor.isOffline == true`, cache rows still render and `Network` error surfaces as a non-blocking snackbar/toast, the four sections stay in `content` state.
  - `Retry` triggers `fresh=true`, `OnRefresh` triggers cache invalidation
- Session-derived fields:
  - `organizerName` ← `SessionManager.displayName` (unified identity — no `staffId` param)
  - `isOrganizerInAnyGroup` ← resolved server-side from `dt_member_role` join, exposed on the summary DTO (`myGroupCount > 0` implies true)
  - `fieldOfficerEnabled` ← per-tenant flag on the summary DTO (v1.1 optional tier)

Write path: none (this screen is read-only; all mutations happen on `group-list`, `group-detail`, and the meeting/share-out screens).

Offline behavior: the entire dashboard is offline-tolerant — the SQLDelight cache is the SoT and every network call is a background refresh. First-launch-offline shows the shimmer for the network-timeout window, then transitions to `error` state with the "No internet connection. Showing cached data." copy (which becomes moot on subsequent launches once the cache is warm).

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/organizer-dashboard/ui.yaml` |
| API contract | `idea-layer/screens/organizer-dashboard/api.yaml` |
| Data flow | `idea-layer/screens/organizer-dashboard/data-flow.yaml` |
| Demo data | `idea-layer/screens/organizer-dashboard/demo-data.yaml` |
| Flow | `idea-layer/screens/organizer-dashboard/flow.yaml` |
| Tests | `idea-layer/screens/organizer-dashboard/tests.yaml` |
| Docs metadata | `idea-layer/screens/organizer-dashboard/docs.yaml` |
| Preview HTML (loading) | `idea-layer/screens/organizer-dashboard/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/organizer-dashboard/preview/content.html` |
| Preview HTML (empty) | `idea-layer/screens/organizer-dashboard/preview/empty.html` |
| Preview HTML (error) | `idea-layer/screens/organizer-dashboard/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/organizer-dashboard/prompts/{loading,content,empty,error}.md` |
| Legacy Stitch mockup | `idea-layer/mockups/organizer-dashboard/stitch/` (2026-05-20 — stale relative to unified-identity pivot; regenerate on next Stitch-enabled pass) |
| Feature-group mockup | `idea-layer/mockups/unified-auth/MOCKUP.md` (Organizer landing section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (4/4 states rendered 2026-07-17) + ui.yaml + demo-data.yaml + design-system tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The legacy Stitch artifact under `stitch/` (2026-05-20) is stale relative to the current unified-identity model (organizerName from session.displayName, no staffId), the savings-pivot KPIs (Share-Outs Due, not Overdue Loans), and the v1.1 optional Field-Officer tile — regenerate on the next Stitch-enabled `/idea-feature-stitch --features organizer-dashboard` pass.
- The "admin" concept is intentionally gone: any user whose `dt_member_role` resolves ≥1 group with organizer/treasurer/chairperson role reaches this screen through the same unified auth flow — no separate admin login type, no staffId nav-param.
- KPI copy pivot (loans → savings-group): "Overdue Loans" → "Share-Outs Due"; "Total Groups" → "My Groups" (organizer-scoped, not all-branch); the error-red border/value tint moved from overdue-loans onto share-outs due.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features organizer-dashboard
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to `ui.yaml` components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
