# Personal Dashboard — Mockup Specification

**Feature**: personal-dashboard | **Route**: `/dashboard/member` | **Type**: dashboard
**Feature group**: end-user-dashboard | **Flow**: end-user-dashboard-flow
**Generated from**: `screens/personal-dashboard/ui.yaml`, `screens/personal-dashboard/demo-data.yaml`, `screens/personal-dashboard/preview/*.html` (5 states)
**Generated at**: 2026-08-01 (by `/idea-render-mockup --feature personal-dashboard`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001). Regenerated for the un-deferred **loan entry card** + top-bar **profile overflow menu** (Settings / Sync Status).

---

## Design Language

**System**: MifosSave-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, group banner, pull-to-refresh spinner, savings-icon tint, deposit chevron
**Accent**: `#FF8F00` (`--accent-700`, amber) — pooled fund emphasis · share-out projection trophy tint (secondary usage on this screen)
**Success**: `#2E7D32` on `#C8E6C9` — deposit indicator, primary CTA
**Warning**: `#F57C00` on `#FFE0B2` — overdue-adjacent hints (not directly used on this screen)
**Danger**: `#C62828` on `#FFCDD2` — withdrawal icon tint, unauthorized error banner
**Muted**: `#757575` on `#F5F5F5` — supporting captions, dividers
**Secondary container**: `#FFE082` (`--accent-100`) — share-out / rotation card background (amber pool emphasis)
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (shimmer, dividers)
**Corner radius**: 16dp savings + share-out cards · 12dp shimmer skeletons · full-round currency chip + group-selector chips
**Elevation**: 2dp savings summary card · 0dp share-out card (flat on secondaryContainer) · 0dp group banner
**Min touch target**: 56dp savings card · 48dp list-item + group-selector chip · 48dp notification icon-button
**Top-negative margin**: savings summary card overlaps the group banner (`margin_top: -20dp`) — signature "card-on-banner" motif.

---

## Screen: Personal Dashboard

### Entry
- From **app launch** when `user_authenticated && !isOrganizerInAnyGroup` (default member entry)
- From **app launch** when `user_authenticated && isOrganizerInAnyGroup && sessionRoleHint == 'member'` (organizer switched to member view)
- No `clientId` / `selfServiceToken` nav-params — unified identity resolves from the auth token
- Back navigation is intercepted by the app shell (root member surface) — no manual pop

### Layout (state: `content`, ACCUMULATING demo — Mwangaza Women's Group)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│  Good morning, Amina Wanjiru    [🔔³][⋮] │  top_bar · primary #2E7D32, onPrimary
│                                          │  text, notification badge + overflow (⋮)
│                                 ┌────────┐│  profile_overflow_menu (more_vertical):
│                                 │Settings ││  → OnSettingsClick → settings
│                                 │Sync…    ││  → OnSyncStatusClick → sync-status
│                                 └────────┘│
├═════════════════════════════════════════┤  (group_banner — primary, flat, 16/24dp)
│  Mwangaza Women's Group      [ KES ]    │  group_name_text · bodyLarge/semibold,
│                                          │  currency_chip · primaryContainer pill
│  ┌─Mwangaza VSLA*─┐ ┌─Tumaini ROSCA─┐   │  group_selector_row · visible_when
│  └────────────────┘ └───────────────┘   │  myGroups.size > 1, horizontal scroll
├─────────────────────────────────────────┤
│  ┌───────────────────────────────────┐  │  savings_summary_card
│  │ [💰]  Total Savings          [›]  │  │  elevation 2dp, corner 16dp,
│  │                                    │  │  margin-top -20dp overlaps banner
│  │       KES 4,300                    │  │  amount · displaySmall, bold, onSurface
│  │                                    │  │
│  │  ● Group-linked: KES 3,500         │  │  green dot · bodySmall, --primary-700
│  │  ● Individual:   KES 800           │  │  amber dot · bodySmall, --secondary
│  └───────────────────────────────────┘  │  → OnSavingsCardClick → personal-savings
├─────────────────────────────────────────┤
│  ┌───────────────────────────────────┐  │  loan_card · surface, corner lg,
│  │ [💳]  My Loans               [›]  │  │  elevation 2dp, 20dp padding, 12dp top
│  │       View your loans and          │  │  loan_icon tertiary tint; labelLarge +
│  │       request a new one            │  │  bodyMedium sublabel; trailing chevron
│  └───────────────────────────────────┘  │  → OnLoansCardClick → personal-loans
├─────────────────────────────────────────┤  (pure nav, forwards clientId; no balance)
│  ┌───────────────────────────────────┐  │  shareout_projection_card
│  │ [🏆]  Projected Share-Out          │  │  secondaryContainer #FFE082, corner 16dp,
│  │                                    │  │  elevation 0dp, 16dp padding
│  │       KES 9,200                    │  │  headlineSmall, bold, onSecondaryContainer
│  └───────────────────────────────────┘  │  (visible_when poolModel != ROTATING_PAYOUT)
├─────────────────────────────────────────┤
│  Recent Activity                        │  titleMedium, semibold, 16dp/24dp margin
├─────────────────────────────────────────┤
│  [⬇]  + KES 300                         │  recent_activity_list · list-item
│       DEPOSIT · 2026-05-09              │  bodyLarge/semibold + bodyMedium supporting
├─────────────────────────────────────────┤
│  [⬇]  + KES 300                         │  divider between rows
│       DEPOSIT · 2026-05-02              │
├─────────────────────────────────────────┤
│  [⬇]  + KES 300                         │
│       DEPOSIT · 2026-04-25              │
├─────────────────────────────────────────┤
│              ↕ scroll                    │  page vertical scroll only; no FAB on this screen
└─────────────────────────────────────────┘
```

### Layout variant (state: `content`, ROTATING_PAYOUT demo — Tumaini ROSCA, member = Joseph Kamau)

```
┌ Tumaini ROSCA                    [ KES ]┐  group_banner switches to ROSCA context
│  (single-group member, no chip row)     │
├─────────────────────────────────────────┤
│  ┌───────────────────────────────────┐  │
│  │ [💰]  Total Savings          [›]  │  │
│  │       KES 5,000                    │  │  groupLinked 5,000 + individual 0
│  │  ● Group-linked: KES 5,000         │  │
│  │  ● Individual:   KES 0             │  │
│  └───────────────────────────────────┘  │
├─────────────────────────────────────────┤
│  ┌───────────────────────────────────┐  │  shareout_projection_card variant
│  │ [🔁]  Your Rotation Position       │  │  icon swap_horiz_24_filled
│  │       #3 in queue                  │  │  rotation_position_text · headlineSmall
│  │       Your turn: ~2026-06-15       │  │  next_recipient_eta_text · bodySmall
│  └───────────────────────────────────┘  │  amount_row hidden; rotation row shown
├─────────────────────────────────────────┤
│  Recent Activity                        │
├─────────────────────────────────────────┤
│  [⬇]  + KES 1,000                       │
│       DEPOSIT · 2026-05-09              │
├─────────────────────────────────────────┤
│  [⬇]  + KES 1,000                       │
│       DEPOSIT · 2026-04-25              │
└─────────────────────────────────────────┘
```

### Demo Data (state: `content`, from `demo-data.yaml`)

Two demo members cover both pool models the dashboard must render:

| memberName      | Groups                                              | Selected            | Model            | Group-linked | Individual | Share-out / Rotation                   | Recent tx count |
|-----------------|-----------------------------------------------------|---------------------|------------------|--------------|------------|----------------------------------------|-----------------|
| Amina Wanjiru   | Mwangaza Women's Group (ACC) · Tumaini ROSCA (ROT)  | Mwangaza (ACC)      | ACCUMULATING     | 3,500        | 800        | Projected Share-Out **KES 9,200**      | 3 deposits      |
| Joseph Kamau    | Tumaini ROSCA (ROT) only                            | Tumaini (ROT)       | ROTATING_PAYOUT  | 5,000        | 0          | Position **#3** · ETA **2026-06-15**   | 2 deposits      |

- **Multi-group selector** — Amina has 2 groups → `group_selector_row` renders both chips, Mwangaza selected; Joseph has 1 group → chip row hidden.
- **Pool-model discrimination** — Amina renders `Projected Share-Out KES 9,200` (ACCUMULATING); Joseph renders `#3 in queue` + `Your turn: ~2026-06-15` (ROTATING_PAYOUT).
- **Recent transactions** all `DEPOSIT` type (green download chevron); reflect the KES 300/week (Mwangaza) and KES 1,000/round (Tumaini) contribution cadence.
- **Notification badge**: unread_count sourced from session; the seed set displays a small pip count on the top-bar bell.

---

## States

The ui.yaml declares 4 `screen_state` members (`Loading`, `Content`, `Error`, `Empty`) plus a `refreshing` overlay — each renders as a distinct HTML preview surface under `preview/`.

### `loading`
Shimmer skeleton mirroring the content layout — parallel fetch of the companion API (`/companion/member/dashboard`) with SQLDelight cache warm-up via Store5.

```
[top_bar with greeting placeholder]         ← primary #2E7D32 fill, no interaction
[group_banner with shimmer chip row]        ← shimmer over group name + currency + selector
────────────────────────────────────────
[shimmer card ] ← 100dp × full width - 32dp margin, corner 16dp, surfaceVariant
[shimmer card ]
[shimmer card ]   ← shimmer_loading count: 4
[shimmer card ]
```

- Cards: 100dp × (full width − 32dp horizontal margin), corner 16dp, `surfaceVariant` background shimmering 1.4s ease-in-out infinite.
- Respects `prefers-reduced-motion: reduce` (animation disabled).
- Top bar and group banner render structurally; text collapses to shimmer bars — no greeting flash before data.
- Notification icon-button inert (no ripple, `pointer-events: none`) but visible.

### `content` (see layouts above)
Data loaded from Store5 stream backed by `MemberDashboardRepository`. Pool-model-adaptive rendering:
- `poolModel == ACCUMULATING` → `shareout_amount` visible (`KES {shareOutProjection}`)
- `poolModel == ROTATING_PAYOUT` → `rotation_position_text` + `next_recipient_eta_text` visible; `shareout_amount` hidden
- `myGroups.size > 1` → `group_selector_row` visible; else hidden and banner shows the single group
Pull-to-refresh available at all times; savings summary card is the primary CTA (chevron affordance).

### `refreshing`
Pull-to-refresh in progress. All content components remain visible; a `pull_to_refresh` overlay pinned to the top scroll region shows the MD3 refresh spinner tinted `--primary-700`.

```
[top_bar]                                      ← identical to content
[group_banner]
    ┌── ↻  ──┐                                 ← pull_to_refresh spinner, primary tint
    └────────┘
[savings_summary_card + shareout_projection_card + list unchanged]
```

- Content stays interactive; taps queue behind the refresh network call.
- Refresh completes → transitions back to `content` (or `error` on failure).

### `empty`
New member — authenticated identity resolved, but the caller belongs to zero groups (`myGroups.size == 0`).

```
┌ Good morning, {memberName}          [🔔] ┐
├──────────────────────────────────────────┤
│  (no group_banner content — banner       │  banner renders as a thin primary strip
│   collapses to a 0dp title state)         │  without the group_name / chip row
├──────────────────────────────────────────┤
│                                            │
│               👥                           │  empty_state · icon groups_24_regular
│         You're not in a group yet          │  title · titleLarge, --text-primary
│    Ask your group organizer to add you     │  body · bodyMedium, --text-secondary
│    to a group, or join one from the        │
│    Groups tab.                             │
│                                            │
└──────────────────────────────────────────┘
```

- No savings card, share-out card, or list — the layout collapses to `[top_bar, group_banner]` per `states.empty.components`.
- The nav call-to-action ("Groups tab") is instructional only — deep-linking to a group-list is handled by the bottom nav shell, not this screen.

### `error`
Companion API failed AND cache is empty — retry surface. When cache HAS rows, the fallback keeps content visible and surfaces a non-blocking snackbar (see `Network` copy below).

```
┌ Good morning, {memberName}          [🔔] ┐
├──────────────────────────────────────────┤
│  (group_banner shell retained but empty)  │
├──────────────────────────────────────────┤
│                                            │
│               📡✗                          │  error_state · wifi_off_24_filled
│      Could not load dashboard              │  title · titleLarge
│                                            │
│    Check your internet connection          │  body · bodyMedium, --text-secondary
│    and try again.                          │
│                                            │
│  ┌──────── Try Again ─────────────────┐   │  cta_label · primary #2E7D32, 48dp,
│  └───────────────────────────────────┘   │  → OnRetry action_contract effect: call_api
│                                            │  cmp-network-monitor guards, Store5 refetches
└──────────────────────────────────────────┘
```

Error types (from `DashboardError`):
- `Network` — retry:true, `error_network` "No internet connection. Showing cached data." (banner if cache warm, full state if empty)
- `Server` — retry:true, `error_server` "Server error. Please try again."
- `Unauthorized` — retry:false, `error_session_expired` "Session expired." → app shell handles re-auth (no navigate: login)

---

## Interaction Patterns

1. **Savings card tap** → `OnSavingsCardClick` (effect: `navigate`) → NavController push `personal-savings` carrying `groupId: selectedGroup.groupId` + `typeConfig`. Full 56dp+ card ripple, chevron affordance on trailing edge.
2. **Group chip tap** (multi-group only) → `OnSelectGroup(groupId)` (effect: `call_api`) → `MemberDashboardRepository` re-fetches with `selectedGroupId = groupId`; `cmp-network-monitor` serves cache when offline; savings + share-out cards + recent activity all recompute against the new group's payload.
3. **Pull-to-refresh** → `OnRefresh` (flow `invalidate_cache: true`) → Store5 `fresh=true` reload with `selectedGroupId = selectedGroup.groupId`; state transitions `content → refreshing → content|error`.
4. **Retry tap (error state)** → `OnRetry` (effect: `call_api`, external: Store5) → same Store5 stream re-hit; clears `error` and re-enters `loading` before landing in `content` or bouncing back to `error`.
5. **Loan card tap** → `OnLoansCardClick` (effect: `navigate`) → `NavigateToLoans(clientId)` → NavController push `personal-loans` forwarding `clientId`. Pure navigation — no cache write, no network call. The loans screen's FAB then reaches `loan-request`.
6. **Overflow menu → Settings** → `OnSettingsClick` (effect: `navigate`) → `NavigateToSettings` → NavController push shared `settings`. No data mutation.
7. **Overflow menu → Sync Status** → `OnSyncStatusClick` (effect: `navigate`) → `NavigateToSyncStatus` → NavController push shared `sync-status`. No data mutation.
8. **Notification icon tap** → shell-owned; opens the notifications tray (delegated to the app shell — no in-screen action).
9. **Back tap** → intercepted by app shell (root member surface); no manual pop, no state to persist.

---

## Accessibility

- Savings summary card exposes a single semantic action ("Open your savings summary for {selectedGroup.name}, KES {total} total, group-linked KES {groupLinked}, individual KES {individual}").
- Amounts render as text + colored dot — never color-only (dot label always present).
- Group chip row uses role `tab` with `aria-selected="true"` on the active group; scrolls horizontally with keyboard arrow support.
- Notification icon-button carries `contentDescription` including unread count ("Notifications, {unread_count} unread").
- Pool-model-discriminated labels use bold `headlineSmall` on `onSecondaryContainer` — WCAG AA contrast ≥ 4.5:1 on `#FFE082`.
- Recent-activity list items carry `min_touch_target: 48dp`; trailing divider drawn on `--outline`.
- Locales covered: English, Swahili (`Habari za asubuhi`, `Akiba ya jumla`), French (`Bonjour`, `Épargne totale`), Hindi (`सुप्रभात`, `कुल बचत`).
- Font stack respects system settings (Roboto / SF Pro system); dynamic type honored on iOS; amounts use tabular numerals via Roboto Mono / SF Mono.

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- Card ripple: MD3 standard 300ms ease-out on tap for savings card + group chip + retry.
- Group chip selection: fill transition 150ms on `primaryContainer` → active `primary`.
- Pull-to-refresh spinner: MD3 refresh indicator tinted `#2E7D32`; fade-in 200ms.
- Snackbar (`ShowSnackbar` event): standard MD3 slide-up + auto-dismiss 4s (used for cached-data fallback banner "No internet connection. Showing cached data.").
- Notification badge count animates a subtle 200ms scale (`prefers-reduced-motion` disables).

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `Store5`, `SQLDelight`, `MemberDashboardRepository`
**Internal lib**: `cmp-network-monitor`

Read paths (offline-first, unified identity):
- `memberName` ← `SessionManager.displayName` (no clientId nav-param)
- `myGroups[]` + `selectedGroup` ← `MemberDashboardRepository.getMemberDashboard(selectedGroupId?)` via Store5 stream
  - Source of truth: SQLDelight `member_dashboard` cache
  - Fetcher: companion API `GET /companion/member/dashboard?selectedGroupId=…` (gated by `cmp-network-monitor`)
  - `OnRetry` triggers `fresh=true`; `OnRefresh` triggers cache invalidation; `OnSelectGroup` re-fetches with a new `selectedGroupId`
- `poolModel` derives from `selectedGroup.typeConfig` (`ACCUMULATING` | `ROTATING_PAYOUT` | `NONE`)
- `groupLinkedSavingsBalance` / `individualSavingsBalance` — server-computed from selected group + member wallet
- `shareOutProjection` (ACCUMULATING) OR `rotationPosition` + `nextRecipientEta` (ROTATING_PAYOUT) — mutually exclusive per pool model
- `recentTransactions[]` — top-N most-recent `SavingsTransactionDto` rows for `selectedGroup`

Write path: none (this screen is read-only; savings actions happen on `personal-savings`, group actions on `group-list`).

Offline behavior: when `NetworkMonitor.isOffline == true`, cache rows still render and `Network` error surfaces as a non-blocking snackbar/toast ("No internet connection. Showing cached data.") — the dashboard itself stays in `content` state and the group-selector still functions against cached group summaries.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/personal-dashboard/ui.yaml` |
| API contract | `idea-layer/screens/personal-dashboard/api.yaml` |
| Data flow | `idea-layer/screens/personal-dashboard/data-flow.yaml` |
| Demo data | `idea-layer/screens/personal-dashboard/demo-data.yaml` |
| Flow | `idea-layer/screens/personal-dashboard/flow.yaml` |
| Tests | `idea-layer/screens/personal-dashboard/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/personal-dashboard/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/personal-dashboard/preview/content.html` |
| Preview HTML (refreshing) | `idea-layer/screens/personal-dashboard/preview/refreshing.html` |
| Preview HTML (empty) | `idea-layer/screens/personal-dashboard/preview/empty.html` |
| Preview HTML (error) | `idea-layer/screens/personal-dashboard/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/personal-dashboard/prompts/{loading,content,empty,error,refreshing}.md` |
| Stitch mockup (probe deferred) | `idea-layer/mockups/personal-dashboard/stitch/` (regenerate on next Stitch-enabled pass) |
| Figma links | `idea-layer/mockups/personal-dashboard/FIGMA_LINKS.md` |
| Feature-group mockup | `idea-layer/mockups/end-user-dashboard/MOCKUP.md` (Screen 1 section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (5/5 states rendered 2026-07-17) + ui.yaml + demo-data.yaml + design-system tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The legacy stitch bundle under `mockups/personal-dashboard/stitch/` (2026-05-20) is stale relative to the current unified-identity + multi-group + pool-model-adaptive ui.yaml (v2.0) and the current MemberDashboardResponse demo dataset; it will be regenerated on the next Stitch-enabled `/idea-feature-stitch --features personal-dashboard` pass.
- The `FIGMA_LINKS.md` sibling captures the historical Figma reference; layout is authoritative here, not in Figma.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features personal-dashboard
  ```
- Design conformance verifier: preview HTML mirrors both ACCUMULATING and ROTATING_PAYOUT variants above; any hand-edit to ui.yaml components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
- Pool-model discrimination is the load-bearing contract for this screen: any regeneration MUST preserve mutually-exclusive rendering of `shareout_amount` vs `rotation_position_text + next_recipient_eta_text` keyed off `poolModel`.
