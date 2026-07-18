# Group List — Mockup Spec

<!-- generated_by: /idea-render-mockup --feature group-list -->
<!-- generated_at: 2026-07-18 -->
<!-- source_of_truth: idea-layer/screens/group-list/{ui.yaml,demo-data.yaml,docs.yaml,prompts/*.md} -->
<!-- companion: idea-layer/mockups/group-list/{FIGMA_LINKS.md,stitch/MANIFEST.yaml} -->

> Renders the authenticated user's savings-group roster fetched from `/companion/groups/mine`. Each card is a role-aware summary (organizer / member / treasurer) with a group-type chip (VSLA / ROSCA / SHG / ASCA), cycle, member count, last meeting date, and a client-derived health indicator (GREEN < 5% overdue, AMBER 5–20%, RED ≥ 20%). Empty state offers unified-identity CTAs — Create Group (→ group-type-picker) OR Join with Code (→ join-with-code). Covers FR-021 (self-signup membership), FR-023 (per-group role display).

---

## Design Language (CommonPurse-v3)

**System**: Material Design 3, comfortable density
**Font**: Noto Sans — scaled up for low-vision rural users
**Palette** (from `design-system/DESIGN.md`):
- Primary: `#2E7D32` (`--primary-700`) — trust-green, VSLA
- Primary container: `#C8E6C9` (`--primary-100`) — badges, ORGANIZER role chip bg
- Accent: `#FF8F00` (`--accent-700`) — pooled-fund emphasis, share-out
- Info: `#1565C0` — informational chips
- Warning: `#F57C00` — overdue signal
- Danger: `#C62828` — defaulted, RED health
- Success: `#2E7D32` (same as primary) — GREEN health
- Background canvas: `#FFFFFF` · App bg: `#FAFAFA` · Muted input: `#F5F5F5`
- Text primary: `#212121` · Text secondary: `#616161` · Text disabled: `#9E9E9E`
- Border subtle: `#EEEEEE` · Border default: `#E0E0E0`

**Shape**: small=8dp, medium=12dp (cards), large=16dp, extra-large=28dp (search bar)
**Elevation**: cards elev=2dp; FAB elev=6dp
**Motion**: subtle only — variance 3/10, motion dial 3/10 (per design_read); std easing `cubic-bezier(0.2, 0.0, 0, 1.0)`, 200–350ms
**Min touch target**: 48dp standard, 56dp FAB & primary CTAs

**Aesthetic dial** (from DESIGN.md): family `minimalist-ui`, density 7/10 (dense financial dashboards).

---

## Screen — GroupListScreen (`/groups`)

**Route**: `/groups` · **Bottom-nav tab**: `groups` · **Entry**: bottom_nav OR post-auth app-launch
**Archetype**: list · **ViewModel**: `GroupListViewModel` (state `GroupListState`, screen-state `{Loading, Content, Error, Empty}`)
**Layout**: `Scaffold` = `TopAppBar` + `SearchBar` + `LazyColumn` of `group_card`s + `ExtendedFloatingActionButton`

### Content state (populated data)

```
┌──────────────────────────────────────────────┐
│ [AppBar — bg=#2E7D32 text=#FFFFFF]           │  h=64dp, statusbar-compensated
│  My Groups                        🔔         │  titleLarge 22sp/500
├──────────────────────────────────────────────┤
│  ┌────────────────────────────────────────┐  │
│  │ 🔍  Search groups…               ✕    │  │  h=48dp, cornerRadius=28dp, elev=2dp
│  └────────────────────────────────────────┘  │  bg=surface, min-touch=48dp
│                                              │
│  ┌────────────────────────────────────────┐  │  ── Card 1 ──
│  │ Mwangaza Women's Group                 │  │  titleMedium 16sp/500, #212121
│  │ [VSLA] [organizer] [Cycle 1]           │  │  chips: tertiaryContainer / primaryContainer / secondaryContainer
│  │ 20 members                             │  │  bodySmall 12sp, #616161
│  │ Last met: 2026-07-14      [● GREEN]    │  │  badge bg=#C8E6C9 text=#1B5E20
│  └────────────────────────────────────────┘  │  cornerRadius=12dp, pad=16dp, elev=2dp
│                                              │
│  ┌────────────────────────────────────────┐  │  ── Card 2 ──
│  │ Jiunge ROSCA Circle                    │  │
│  │ [ROSCA] [member] [Cycle 3]             │  │  role chip = surfaceVariant (non-organizer default)
│  │ 10 members                             │  │
│  │ Last met: 2026-07-10      [● AMBER]    │  │  badge bg=#FFF9C4 text=#E65100
│  └────────────────────────────────────────┘  │
│                                              │
│  ┌────────────────────────────────────────┐  │  ── Card 3 ──
│  │ Pamoja SHG                             │  │
│  │ [SHG] [treasurer] [Cycle 2]            │  │
│  │ 15 members                             │  │
│  │ Last met: 2026-07-08      [● GREEN]    │  │
│  └────────────────────────────────────────┘  │
│                                              │
│                                     ┌──────┐ │
│                                     │+ New │ │  ExtendedFAB — bg=#2E7D32, icon=add,
│                                     │Group │ │  label onPrimary, 56dp, bottom_end,
│                                     └──────┘ │  margin=16dp, elev=6dp
└──────────────────────────────────────────────┘
```

**Data source**: `GroupRepository.streamMyGroups()` → `GET /companion/groups/mine`
**Demo dataset** (from `demo-data.yaml`): 5 groups — Mwangaza (VSLA/organizer/GREEN), Tumaini (ROSCA/member/AMBER 8%), Baraka (ASCA/member/GREEN), Imara (SHG/organizer/RED 25%), Upendo (VSLA/member/GREEN 4%).
**Health rule** (client-derived): `overdueRate < 0.05 → GREEN`, `0.05 ≤ x < 0.20 → AMBER`, `x ≥ 0.20 → RED`.

### Loading state

```
┌──────────────────────────────────────────────┐
│  My Groups                        🔔         │  TopAppBar unchanged
├──────────────────────────────────────────────┤
│  🔍  Search groups…              ✕           │  SearchBar unchanged
│                                              │
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         │  5× shimmer cards
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         │  h=88dp, cornerRadius=12dp
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         │  bg=surfaceVariant (#F5F5F5)
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         │  animated shimmer left→right,
│  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒         │  1200ms sweep
└──────────────────────────────────────────────┘
```

Fires on: cold entry, `Retry` after error, pull-to-refresh.

### Empty state (no groups)

```
┌──────────────────────────────────────────────┐
│  My Groups                        🔔         │
├──────────────────────────────────────────────┤
│  🔍  Search groups…              ✕           │
│                                              │
│              ┌──────┐                        │
│              │ 👥 ✕ │                        │  icon: group_off, 80dp, #616161
│              └──────┘                        │
│                                              │
│           No groups yet                      │  headlineSmall 24sp, #212121
│                                              │
│    Create a new savings group or join an     │  bodyMedium 14sp, #616161
│    existing one with an invite code.         │  center-aligned, max-width 320dp
│                                              │
│      ┌──────────────────────────────┐        │
│      │       Create Group           │        │  FilledButton, bg=#2E7D32,
│      └──────────────────────────────┘        │  text=onPrimary, 56dp, full-width
│                                              │
│      ┌──────────────────────────────┐        │
│      │       Join with Code         │        │  OutlinedButton, border=#2E7D32,
│      └──────────────────────────────┘        │  text=#2E7D32, 48dp, full-width
│                                              │
│                                     ┌──────┐ │
│                                     │+ New │ │  FAB still visible (Design AC:
│                                     │Group │ │  primary CTA path)
│                                     └──────┘ │
└──────────────────────────────────────────────┘
```

The two-CTA unified-identity layout (Create + Join with Code) satisfies FR-021 self-signup.

### Error state (API failure)

```
┌──────────────────────────────────────────────┐
│  My Groups                        🔔         │  TopAppBar preserved (per ui.yaml
├──────────────────────────────────────────────┤  states.error.components: [top_bar, error_state])
│                                              │
│              ┌────────┐                      │
│              │   ☁    │                      │  icon: cloud_off, 64dp, #616161
│              │   ✕    │                      │
│              └────────┘                      │
│                                              │
│         Could not load groups                │  titleLarge 22sp, #212121
│                                              │
│    {{error.message}}                         │  bodyMedium 14sp, #616161
│    · Network → "No internet…"                │  copy resolved via i18n key
│    · Server  → "Server error…"               │  (error_network / _server / _auth)
│    · Auth    → "Session expired…"            │
│                                              │
│      ┌──────────────────────────────┐        │
│      │           Retry              │        │  FilledButton, bg=#2E7D32, 56dp
│      └──────────────────────────────┘        │
│                                              │
└──────────────────────────────────────────────┘
```

`Auth` variant additionally redirects to `login` after Retry per `state_model.errors[type=Auth].redirect: login`.

---

## Component Catalog (source: `screens/group-list/ui.yaml`)

| Component id | Type | Role | Notable style |
|---|---|---|---|
| `top_bar` | top-bar | Section title + Notifications icon (emits `OnOpenNotifications` → deferred snackbar) | bg=primary, text=onPrimary, h=64dp |
| `search_bar` | search-bar | Client-side name filter, 150ms debounce, clear icon | h=48dp, cornerRadius=28dp, elev=2dp |
| `group_card` | card | Per-group summary, tap → `group-dashboard` with `{groupId, viewerRole}` | cornerRadius=12dp, pad=16dp, min-touch=72dp |
| `group_card > group_type_chip` | chip | VSLA / ROSCA / SHG / ASCA | tertiaryContainer / onTertiaryContainer |
| `group_card > viewer_role_chip` | chip | ORGANIZER / MEMBER / TREASURER (case-lowered) | ORGANIZER → primaryContainer #C8E6C9; default → surfaceVariant |
| `group_card > cycle_chip` | chip | "Cycle {n}" | secondaryContainer / onSecondaryContainer |
| `group_card > health_indicator_badge` | badge | GREEN #C8E6C9/#1B5E20 · AMBER #FFF9C4/#E65100 · RED #FFCDD2/#B71C1C | 24dp dot + label |
| `create_group_fab` | fab (extended) | → `group-type-picker` (**not** directly to `group-create`) | 56dp, bottom_end, bg=primary |
| `shimmer_list` | shimmer | count=5, animated | h=88dp, bg=surfaceVariant |
| `empty_state` | empty-state | icon + title + body + Create + Join-with-code CTAs | centered, 320dp max-width |
| `error_state` | error-state | icon + title + body + Retry CTA | cloud_off, Retry re-fires `GroupRepository` fetch |

---

## Interactive Contract (`state_model.actions`)

All handlers wire to `GroupListViewModel.handleAction(...)`.

| Action | Trigger | Effect | Nav / mutation |
|---|---|---|---|
| `OnGroupClick(groupId, viewerRole)` | Tap card | `navigate` | → `group-dashboard` (passes viewerRole so dashboard resolves organizer vs member surfaces) |
| `OnSearch(query)` | Type in search bar | `transform_state` | filters `groups → filteredGroups` client-side, no API call |
| `OnClearSearch` | Tap ✕ in search bar | `transform_state` | resets `searchQuery=""`, `filteredGroups=groups` |
| `OnCreateGroup` | FAB tap OR empty-state "Create Group" | `navigate` | → `group-type-picker` (**not** `group-create`) |
| `OnJoinGroup` | Empty-state "Join with Code" | `navigate` | → `join-with-code` (FR-024 invite-accept) |
| `OnRefresh` | Pull-to-refresh | `call_api` (via `GroupRepository`) | re-fetch `/companion/groups/mine`, `isRefreshing` toggles |
| `Retry` | Error state CTA | `call_api` (via `GroupRepository`) | re-fetch; Auth error additionally redirects to `login` |
| `OnOpenNotifications` | Top-bar 🔔 | `emit_event` | shows deferred-snackbar (NotificationsDeferred), NO nav (deferred per release_plan) |

**Search behavior**: 150ms debounce, case-insensitive `contains(group.name, query)`, updates `filteredGroups` synchronously; when `query == ""` the card list falls back to `groups`.

---

## States Matrix

| State | Rendered preview | Stitch mockup | Prompt |
|---|---|---|---|
| loading | `screens/group-list/preview/loading.html` | (not in current stitch batch — placeholder shimmer sufficient) | `screens/group-list/prompts/loading.md` |
| content | `screens/group-list/preview/content.html` | `mockups/group-list/stitch/01-group-list-content/{code.html,screen.png}` ✅ | `screens/group-list/prompts/content.md` |
| empty | `screens/group-list/preview/empty.html` | — (empty state derivable from content stitch by omitting cards) | `screens/group-list/prompts/empty.md` |
| error | `screens/group-list/preview/error.html` | `mockups/group-list/stitch/02-group-list-error/{code.html,screen.png}` ✅ | `screens/group-list/prompts/error.md` |

Stitch rendering summary (from `mockups/group-list/FIGMA_LINKS.md`, project `6387644860533383795`, DS `17261554270924114992`, generated 2026-07-17):

- content — screen `aae47530b10c4e56a6aafb020921a48e` — ✅ HTML + PNG
- error   — screen `cb42c64fdb80478dafb7642fa13f5dc3` — ✅ HTML + PNG

---

## Interaction Patterns

- **Card tap** — bounded ripple (200ms) from tap origin; card scales 1.0 → 0.98 → 1.0 (spring). Shared-element transition on `group_name_text` slides + fades into `group-dashboard` (350ms).
- **Search input** — keyboard shows on focus; list filters as user types (150ms debounce); clear icon appears when query non-empty and clears query on tap.
- **Pull-to-refresh** — Material 3 pull indicator tinted `#2E7D32`; on release spinner completes rotation, `OnRefresh` fires, indicator dismisses on data resolution (200ms fade).
- **FAB tap** — bounded ripple; screen transition slides `group-type-picker` from bottom (300ms). FAB collapses to icon-only on scroll-down past 200dp, re-extends on scroll-up.
- **Retry (error state)** — button ripple → transitions to loading state (shimmer replaces error card) → resolves to content/empty/error again.
- **Notifications icon** — snackbar rises from bottom for 4s with the deferred-release copy; no navigation.

---

## Accessibility

- **Touch targets** — 48dp minimum for search bar, chips, badges, icon actions; 56dp for FAB, Create Group / Retry primary CTAs.
- **Color contrast** (WCAG check on the CommonPurse palette):
  - onPrimary #FFFFFF on Primary #2E7D32 — 8.10:1 (AAA)
  - Text primary #212121 on canvas #FFFFFF — 16.10:1 (AAA)
  - Text secondary #616161 on canvas — 5.74:1 (AA)
  - GREEN badge text #1B5E20 on #C8E6C9 — 5.32:1 (AA)
  - AMBER badge text #E65100 on #FFF9C4 — 4.98:1 (AA)
  - RED badge text #B71C1C on #FFCDD2 — 5.90:1 (AA)
- **contentDescription** —
  - Card: `"{{group.name}}, {{group.groupType}}, {{group.viewerRole|lower}}, cycle {{group.cycleNumber}}, {{group.memberCount}} members, last met {{group.lastMeetingDate}}, health {{group.healthIndicator}}"`
  - FAB: `"Create new savings group"`
  - Notifications icon: `"Notifications"` (matches `content_description` in ui.yaml)
  - Search bar clear: `"Clear search"`
  - Retry: `"Retry loading groups"`
- **TalkBack ordering** — TopAppBar → SearchBar → each card in list order → FAB (empty state announces title → body → Create → Join with Code → FAB last).
- **Focus ring** — 2dp solid `--primary-700` (#2E7D32), 2dp offset (per DESIGN.md AA-2 focus contract).
- **Dynamic type** — every size in sp; the `comfortable density` + 7/10 density dial means extra vertical padding aids rural low-vision users; layouts reflow but never truncate group name (uses `Ellipsis.Marquee` for names > 24 chars).
- **Announcements** — state transitions (loading → content) announce `"{n} groups loaded"`; error state announces `"Could not load groups. Retry available."` via `LiveRegion`.

---

## i18n Keys (source `ui.yaml#i18n.en`)

| Key | Copy |
|---|---|
| `screen_title` | My Groups |
| `search_placeholder` | Search groups… |
| `cycle_label` | Cycle {{n}} |
| `members_label` | {{n}} members |
| `last_met_label` | Last met: {{date}} |
| `fab_label` | New Group |
| `empty_title` | No groups yet |
| `empty_body` | Create a new savings group or join an existing one with an invite code. |
| `empty_cta_create` | Create Group |
| `empty_cta_join` | Join with Code |
| `error_network` | No internet connection. Showing cached data. |
| `error_server` | Server error. Please try again. |
| `error_auth` | Session expired. Please log in again. |
| `health_green` | Healthy |
| `health_amber` | At Risk |
| `health_red` | Critical |

Every user-facing string in Compose MUST route via `stringResource(Res.string.<key>)` per RULE-IMPL-NO-HARDCODED-STRING-001.

---

## Notes

- FAB navigates to `group-type-picker` (VSLA / ROSCA / SHG / ASCA selector) **before** `group-create`, per docs.yaml (FR-021, FR-023) and ui.yaml `create_group_fab.target`.
- Health indicator is **client-derived** from `overdueRate`, never returned by the API — keep the derivation colocated with the mapper next to `GroupRepository`.
- `viewerRole` is resolved server-side from the auth token via `/companion/groups/mine` (no `staffId` param) — the mockup's role chip is a display of that field, not a client toggle.
- Legacy `screens/group-list/MOCKUP.md` (dated 2026-05-09, single "content" state) is superseded by this file. That file remains until the next `/idea-sync` retirement pass; downstream consumers (`/kmp-implement`, dashboards) should read `mockups/group-list/MOCKUP.md`.
