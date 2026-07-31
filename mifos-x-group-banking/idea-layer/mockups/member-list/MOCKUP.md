# Member List — Mockup Specification

**Feature**: member-list | **Route**: `/groups/{groupId}/members` | **Type**: list
**Feature group**: member-management | **Flow**: member-management-flow
**Generated from**: `screens/member-list/ui.yaml`, `screens/member-list/demo-data.yaml`, `screens/member-list/preview/*.html` (4 states rendered 2026-07-17)
**Generated at**: 2026-07-31 (by `/idea-render-mockup --feature member-list`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001). Foundation-wave refresh: top_bar now carries the **Invite** action (→ member-invite).

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, FAB, back button, primary chips
**Accent**: `#FF8F00` (`--accent-700`, amber) — pooled fund emphasis (not used on this screen)
**Success**: `#1B5E20` on `#C8E6C9` — ACTIVE loan badges
**Danger**: `#B71C1C` on `#FFCDD2` — OVERDUE loan badges
**Muted**: `#757575` on `#F5F5F5` — NONE badges, MEMBER role chip, dividers
**Role container tones (MD3)**: `primaryContainer` (CHAIRPERSON) · `secondaryContainer` (TREASURER) · `tertiaryContainer` (SECRETARY) · `surfaceVariant` (MEMBER)
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (shimmer, dividers)
**Corner radius**: 12dp cards · 4dp shimmer skeletons · full-round FAB · full-round chips
**Elevation**: 0dp list rows (divider-separated) · 6dp FAB
**Min touch target**: 72dp member row · 48dp role chip · 56dp FAB

---

## Screen: Members

### Entry
- From **group-dashboard** ("View Members" button); nav-param `groupId: String`
- Back navigation pops the route and returns to `group-dashboard`

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹]  Members              [👤﹢ Invite] │  TopAppBar — primary #2E7D32, onPrimary text;
│      Mwangaza Women's Group             │  trailing invite_action (icon person_add_alt,
│                                          │  label "Invite") → OnInviteMember → member-invite
│                                          │  subtitle · {{groupName}} · titleSmall / 0.87
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ ⓐⓦ  Amina Wanjiru      [TREAS. ] │   │  member_list_item · 72dp min touch,
│  │      Savings: KES 3,500  [ NONE ]│   │  divider bottom, swipe→ "View Profile"
│  └──────────────────────────────────┘   │  leading=avatar (initials "AW", 48dp,
│  ─────────────────────────────────────  │  secondaryContainer bg)
│  ┌──────────────────────────────────┐   │  role_chip: TREASURER → secondaryContainer
│  │ ⓙⓚ  Joseph Kamau       [CHAIR. ] │   │  loan_status_badge: NONE → surfaceVariant grey
│  │      Savings: KES 4,200  [ACTIVE]│   │
│  └──────────────────────────────────┘   │  CHAIR. → primaryContainer / onPrimaryContainer
│  ─────────────────────────────────────  │  ACTIVE → #C8E6C9 / #1B5E20
│  ┌──────────────────────────────────┐   │
│  │ ⓖⓐ  Grace Achieng      [SECRET.] │   │  SECRET. → tertiaryContainer / onTertiaryContainer
│  │      Savings: KES 2,800  [ NONE ]│   │
│  └──────────────────────────────────┘   │  → on_click OnMemberClick(client_003)
│  ─────────────────────────────────────  │
│  ┌──────────────────────────────────┐   │
│  │ ⓟⓞ  Peter Otieno       [MEMBER ] │   │  MEMBER → surfaceVariant / onSurfaceVariant
│  │      Savings: KES 1,500  [OVERDU]│   │  OVERDUE → #FFCDD2 / #B71C1C (red pill)
│  └──────────────────────────────────┘   │
│  ─────────────────────────────────────  │
│  ┌──────────────────────────────────┐   │
│  │ ⓜⓝ  Mary Njeri         [MEMBER ] │   │
│  │      Savings: KES 2,000  [ NONE ]│   │  (rows continue client_006 … client_014,
│  └──────────────────────────────────┘   │   scroll)
│              ↕ scroll                    │  page_size 20 · OnLoadMore fires on end-reached
├─────────────────────────────────────────┤
│                          ┌──[ + Add ]──┐│  add_member_fab · primary #2E7D32,
│                          │              ││  56dp, bottom_end, always visible on content
│                          └──────────────┘│  → on_click OnAddMember → member-add(groupId)
└─────────────────────────────────────────┘
```

### Demo Data (state: `content`, from `demo-data.yaml`)

Fourteen members in Mwangaza Women's Group (groupId `GRP-20260509-001`, Kisumu West Branch, KES):

| id         | Member           | Role        | Savings (KES) | Loan Status | Attendance |
|------------|------------------|-------------|--------------:|-------------|-----------:|
| client_001 | Amina Wanjiru    | TREASURER   |         3,500 | NONE        |       0.95 |
| client_002 | Joseph Kamau     | CHAIRPERSON |         4,200 | ACTIVE      |       1.00 |
| client_003 | Grace Achieng    | SECRETARY   |         2,800 | NONE        |       0.90 |
| client_004 | Peter Otieno     | MEMBER      |         1,500 | OVERDUE     |       0.65 |
| client_005 | Mary Njeri       | MEMBER      |         2,000 | NONE        |       0.85 |
| client_006 | Samuel Mwangi    | MEMBER      |         2,650 | ACTIVE      |       0.80 |
| client_007 | Esther Nyambura  | MEMBER      |         1,200 | NONE        |       0.75 |
| client_008 | David Kiprop     | MEMBER      |         1,850 | ACTIVE      |       0.88 |
| client_009 | Rebecca Auma     | MEMBER      |         2,100 | NONE        |       0.92 |
| client_010 | James Ochieng    | MEMBER      |           950 | OVERDUE     |       0.55 |
| client_011 | Faith Chebet     | MEMBER      |         1,750 | NONE        |       0.83 |
| client_012 | Michael Njoroge  | MEMBER      |         3,100 | ACTIVE      |       0.97 |
| client_013 | Susan Wangari    | MEMBER      |         1,400 | NONE        |       0.70 |
| client_014 | Daniel Mutua     | MEMBER      |         2,250 | NONE        |       0.86 |

- **Role distribution** — CHAIRPERSON 1, TREASURER 1, SECRETARY 1, MEMBER 11 → every `role_chip` container tone renders at least once.
- **Loan status distribution** — ACTIVE 4, OVERDUE 2, NONE 8 → every badge color surfaces.
- **Fits within page_size=20**: `OnLoadMore` never triggers on the seed page; the load-more path is exercised via a paging-race test that mocks `page_size=10` (page 1: 10 rows, `hasMorePages=true`; page 2: 4 rows, `hasMorePages=false`).
- **Avatar fallback**: every `photoUri` is `null` in the seed → all rows render initials (e.g. "AW", "JK") over `secondaryContainer` background.
- **MemberListState fixture**: `groupId="42"` / `groupName="Mwangaza Women's Group"` / `isRefreshing=false` / `hasMorePages=false`.

---

## States

The ui.yaml declares 4 `screen_state` members (`Loading`, `Content`, `Error`, `Empty`) — each renders as a distinct HTML preview surface under `preview/`.

### `loading`
Shimmer skeleton mirroring the content layout — parallel fetch of `members` from SQLDelight cache + Fineract API.

```
[Members header]                           ← top_bar visible with title + subtitle stub
────────────────────────────────────────
[shimmer row ]  ← 72dp × full width, corner 4dp, surfaceVariant
[shimmer row ]
[shimmer row ]
[shimmer row ]   ← shimmer_list count: 6
[shimmer row ]
[shimmer row ]
```

- Rows: 72dp × full width, corner 4dp, `surfaceVariant` background shimmering 1.4s ease-in-out infinite.
- Respects `prefers-reduced-motion: reduce` (animation disabled).
- Top bar retains title "Members" and the group name subtitle, the back arrow, and the trailing **Invite** action (`invite_action` → OnInviteMember → member-invite) — the invite action is present in every state's top bar.
- FAB is NOT rendered in the loading state (per `states.loading.components`).
- Back arrow remains enabled — user can always retreat to `group-dashboard`.

### `content` (see layout above)
Members loaded from Store5 stream. Rows render with real avatars/initials, role chip color coded by role, and loan-status badge color coded by loan state. FAB always visible. `load_more_indicator` (linear progress bar, `primary` tint) appears at list foot only while `isLoadingMore == true`.

### `empty`
No members registered under this group yet (fresh group, no roster).

```
┌ Members ───────────────────────────────┐
│      Mwangaza Women's Group             │
├────────────────────────────────────────┤
│                                          │
│                                          │
│               👥                         │  empty_state · icon group_add, 64dp,
│         No members yet                   │  onSurfaceVariant tint
│    Add the first member to               │  title · titleLarge
│    this group.                           │  body · bodyMedium, --text-secondary
│                                          │
│  ┌─────── Add Member ─────────────┐    │  cta_label · primary #2E7D32, 48dp,
│  └────────────────────────────────┘    │  full-width filled button
│                                          │
│                          ┌──[ + Add ]──┐│  add_member_fab still visible
│                          └──────────────┘│  → OnAddMember → member-add(groupId)
└─────────────────────────────────────────┘
```

- CTA and FAB both resolve to the same `OnAddMember` action → `member-add` (double-affordance is intentional; the FAB stays consistent across all states so muscle memory holds).
- Empty state illustration uses `group_add` outlined icon at 64dp with `onSurfaceVariant` tint.

### `error`
Fineract API failed AND cache is empty — retry surface. When cache HAS rows, the toast fallback keeps the content visible (see `error_network` copy).

```
┌ Members ───────────────────────────────┐
│      Mwangaza Women's Group             │
├────────────────────────────────────────┤
│                                          │
│                                          │
│               ☁                          │  error_state · cloud_off icon, 64dp
│      Could not load members              │  title · titleLarge
│                                          │
│    {error.message}                       │  body · bodyMedium, --text-secondary
│    e.g. "No internet. Showing            │
│    cached members."                      │
│                                          │
│  ┌─────── Retry ──────────────────┐    │  cta_label · primary #2E7D32, 48dp
│  └────────────────────────────────┘    │  → Retry action_contract effect: call_api,
│                                          │  cmp-network-monitor library_ref
│                                          │  resets offset to 0, re-hits Store5 stream
└─────────────────────────────────────────┘
```

Error types (from `MemberListError`):
- `Network` — retry:true, `error_network` "No internet. Showing cached members."
- `Server` — retry:true, `error_server` "Server error. Please retry."
- `Auth` — retry:false, `error_auth` "Session expired." → redirect to `login`

Note: FAB is NOT rendered in the error state (per `states.error.components`) — the user must recover the roster before they can add a new member.

---

## Interaction Patterns

1. **Member row tap** → `OnMemberClick(memberId)` (effect: `navigate`) → NavController push `member-profile` with `memberId` + `groupId` route args. Row uses 72dp min touch target and full-row ripple.
2. **Member row swipe (start_to_end)** → `OnMemberClick(memberId)` (effect: `navigate`, same destination as tap) → gesture shortcut. Swipe surface shows `person` icon + "View Profile" label over `primaryContainer` background.
3. **FAB tap** → `OnAddMember(groupId)` (effect: `navigate`) → NavController push `member-add` with `groupId` route arg. FAB is always visible on `content` and `empty` states.
4. **Empty-state CTA tap** → `OnAddMember(groupId)` (effect: `navigate`) → same destination as the FAB.
5. **Pull to refresh** → `OnRefresh` (flow `invalidate_cache: true`) → Store5 `fresh=true` reload, keeps scroll position and pagination state.
6. **Scroll to list end** → `OnLoadMore` → paginated fetch (`currentOffset` += `page_size`) via Fineract `GET /groups/{groupId}/clients`; `hasMorePages=false` silently no-ops.
7. **Retry tap (error state)** → `Retry` (effect: `call_api`, `library_refs: [cmp-network-monitor]`) → connectivity check → Store5 stream with `fresh=true`, offset reset to 0, error cleared.
8. **Back tap** → `OnBack` (effect: `navigate`) → pops the route back to `group-dashboard`; cancels any in-flight pagination fetch; no persistence or roster mutation on back.

---

## Accessibility

- Member row exposes a single semantic action ("Open profile for {displayName}, {role}, KES {savingsBalance}, loan {loanStatus}").
- Role AND loan status are text + colored container — never color-only. Badge labels always readable, chip labels always visible.
- Role chip container tones map 1:1 to the 4 role enum values — swapping the theme's `primaryContainer` etc. propagates without code change.
- Swipe action carries an explicit label "View Profile" — gesture is never the sole affordance (tap works too).
- Min touch target 72dp on member rows, 48dp on role chips, 56dp on FAB.
- Avatars fall back to initials when `photoUri` is null; initials render at 48dp with `onSecondaryContainer` on `secondaryContainer` — WCAG AA contrast at all supported theme variants.
- Locales covered: English (default) — with keys for `screen_title`, `savings_label`, `role_*`, `loan_*`, `fab_label`, `swipe_label`, `empty_*`, `error_*`.
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS.

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- Row ripple: MD3 standard 300ms ease-out on tap.
- Swipe reveal: 200ms ease-out spring; snap-back if released before threshold (40% of row width).
- FAB press: MD3 elevation change 6dp → 12dp + ripple.
- Load-more indicator: linear progress bar, indeterminate, `primary` tint, appears/disappears with 150ms cross-fade.
- Pull-to-refresh spinner: MD3 refresh indicator, matches primary `#2E7D32`.
- Snackbar (`ShowSnackbar` event): standard MD3 slide-up + auto-dismiss 4s (used for the cached-data fallback banner).

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `Store5`, `SQLDelight`, `Fineract m_client`
**Internal lib**: `cmp-network-monitor`

Read paths (offline-first):
- `members[]` ← `MemberRepository.getGroupMembers(groupId, offset, limit)` via Store5 stream
  - Source of truth: SQLDelight `members` cache
  - Fetcher: Fineract `GET /groups/{groupId}/clients?limit=20&offset={currentOffset}` (paged, gated by `cmp-network-monitor`)
  - `Retry` triggers `fresh=true` + resets `currentOffset=0`
  - `OnRefresh` triggers cache invalidation
- `groupName` ← `GroupRepository.getGroup(groupId).name` (single-row cache, populated on entry)
- `hasMorePages` — derived from Fineract response `totalFilteredRecords` vs current cursor
- Role and loan status resolved server-side and returned on the DTO — no client-side join

Write path: none (this screen is read-only; roster mutation happens on `member-add` and `member-profile`).

Offline behavior: when `NetworkMonitor.isOffline == true`, cache rows still render and `Network` error surfaces as a non-blocking snackbar/toast ("No internet. Showing cached members.") — the list itself stays in `content` state.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/member-list/ui.yaml` |
| API contract | `idea-layer/screens/member-list/api.yaml` |
| Data flow | `idea-layer/screens/member-list/data-flow.yaml` |
| Demo data | `idea-layer/screens/member-list/demo-data.yaml` |
| Flow | `idea-layer/screens/member-list/flow.yaml` |
| Tests | `idea-layer/screens/member-list/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/member-list/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/member-list/preview/content.html` |
| Preview HTML (empty) | `idea-layer/screens/member-list/preview/empty.html` |
| Preview HTML (error) | `idea-layer/screens/member-list/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/member-list/prompts/{loading,content,empty,error}.md` |
| Feature-group mockup | `idea-layer/mockups/member-management/MOCKUP.md` (Screen 1 section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (4/4 states) + ui.yaml + demo-data.yaml + design-system tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The FAB visibility contract is intentionally state-scoped: shown on `content` + `empty`, hidden on `loading` + `error`. Rationale — the user needs a stable path to add a member the moment the roster is either populated or confirmed empty, but hiding the FAB during load prevents accidental double-navigation while the list is still resolving, and hiding it during an error keeps the retry action visually primary.
- Every role and every loan-status value in the seed demo dataset renders at least once, so the mockup exercises every distinct container/badge tone in a single preview. Adding a new role enum requires a new `role_chip.style.<ROLE>` entry — the color mapping is data-driven, not conditional.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features member-list
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to ui.yaml components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
