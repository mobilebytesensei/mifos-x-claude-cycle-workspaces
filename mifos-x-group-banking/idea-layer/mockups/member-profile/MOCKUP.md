# Member Profile — Mockup Specification

**Feature**: member-profile | **Route**: `/groups/{groupId}/members/{memberId}` | **Type**: detail
**Feature group**: member-onboarding | **Flow**: member-onboarding-flow
**Generated from**: `screens/member-profile/ui.yaml`, `screens/member-profile/demo-data.yaml`, `screens/member-profile/preview/*.html` (3 states rendered 2026-07-17)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature member-profile`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for balances
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, avatar fill, sparkline stroke, Confirm CTA, Retry CTA
**Primary container**: `#C8E6C9` — member header card background, sparkline fill (light)
**Secondary**: `#FF8F00` (`--accent-700`, amber) — TREASURER role chip fill (`onSecondary` text)
**Tertiary**: `#00838F` (teal) — SECRETARY role chip, attendance fraction number, attendance progress ≥ 80%
**Success**: `#1B5E20` on `#C8E6C9` — status affirmations, "Active" member state
**Warning**: `#E65100` on `#FFF9C4` — attendance progress 60–79%
**Danger / error**: `#B71C1C` on `#FFCDD2` — arrears banner, arrears border, attendance < 60%
**Muted**: `#757575` on `#F5F5F5` — MEMBER role chip, shimmer skeleton
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (shimmer, chips)
**Corner radius**: 16dp cards + shimmer skeletons · 8dp chip · full-round avatar / progress track
**Elevation**: 0dp header card (tinted) · 2dp savings/loan/attendance cards · 8dp bottom sheet
**Min touch target**: 48dp back arrow · 40dp Edit Role button · 56dp role list-item + Confirm CTA · full-row savings/loan/attendance card taps

---

## Screen: Member Profile

### Entry
- From **member-list** (row tap → `member_row_tap`); nav-params `memberId: String, groupId: String`
- From **group-management** → member roster row tap (chairperson admin path)
- Back navigation pops the route and returns to `member-list` (retains group scroll position)

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹]  Member Profile          [#2E7D32]  │  top_bar — primary green, onPrimary text
├─────────────────────────────────────────┤  16dp gutter, 16dp vertical padding
│  ┌──────────────────────────────────┐   │
│  │ ┌───┐  Amina Wanjiru             │   │  member_header_card
│  │ │ A │  Member since Jan 15, 2026 │   │  primaryContainer #C8E6C9, corner 16dp
│  │ │ W │  +254 712 345 678          │   │  avatar 72dp — primary #2E7D32 fill,
│  │ └───┘                            │   │  onPrimary "AW" initials, headlineSmall
│  │        [ TREASURER ]  [Edit Role]│   │  role_chip — secondary #FF8F00 amber pill
│  │                                   │   │  edit_role_button — outlined, primary
│  └──────────────────────────────────┘   │  visible_when isCurrentUserChairperson
├─────────────────────────────────────────┤
│  ┌──────────────────────────────────┐   │
│  │ Savings History                   │   │  savings_history_card
│  │ KES 3,500                         │   │  elevation 2dp, corner 16dp
│  │                                   │   │  balance · displaySmall, primary
│  │      ╱╲    ╱─                     │   │  sparkline · 80dp, primary stroke,
│  │  ╱──╱  ╲──╱                       │   │  primaryContainer fill · 7 weekly points
│  │ ╱                                 │   │  KES 500 → 3,500 (Jan 20 – Mar 3)
│  │                                   │   │
│  │              View Full History →  │   │  text button, primary
│  └──────────────────────────────────┘   │  → on_click OnViewSavings
├─────────────────────────────────────────┤  → navigate member-savings-detail
│  ┌──────────────────────────────────┐   │
│  │  (hidden — activeLoan == null)   │   │  active_loan_card
│  └──────────────────────────────────┘   │  visible_when accounts.activeLoan != null
├─────────────────────────────────────────┤  see "Content variant B" below
│  ┌──────────────────────────────────┐   │
│  │ Meeting Attendance                │   │  attendance_card
│  │ 14 / 15                           │   │  fraction · headlineMedium, tertiary teal
│  │ 93% attendance rate               │   │  rate · bodyMedium, onSurfaceVariant
│  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░       │   │  progress bar — tertiary track (≥80),
│  │                                   │   │  full-round, 8dp thick
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Content variant B — with active loan in arrears (`MemberAccounts_WithActiveLoan`)

Same layout, but `active_loan_card` renders between savings and attendance cards
with a 2dp red (`#B71C1C`) border and an inline error banner:

```
┌──────────────────────────────────┐
│ Active Loan               [red2dp]│  border color=error, width=2dp
│ Chama Emergency Loan              │  productName · bodyMedium, onSurfaceVariant
│ KES 12,500 outstanding            │  titleLarge, onSurface, Roboto Mono
│ ┌──────────────────────────────┐ │
│ │ ⚠  This loan is in arrears.  │ │  loan_arrears_banner
│ │    Due: 2026-07-10           │ │  errorContainer #FFCDD2, onErrorContainer text
│ └──────────────────────────────┘ │  warning icon 20dp
└──────────────────────────────────┘
```

### Demo Data (state: `content`, from `demo-data.yaml`)

**Primary persona — treasurer, no active loan** (`MemberProfileState`, viewer = chairperson):

| Field                    | Value                              |
|--------------------------|------------------------------------|
| displayName              | Amina Wanjiru                      |
| joinDate                 | 2026-01-15 → "Member since Jan 15" |
| phone                    | +254 712 345 678                   |
| role                     | TREASURER (amber chip)             |
| isCurrentUserChairperson | true → Edit Role visible           |
| savingsBalance           | KES 3,500.00                       |
| savingsHistory           | 7 weekly points, KES 500 → 3,500   |
| activeLoan               | null (card hidden)                 |
| meetingsAttended         | 14                                 |
| totalMeetings            | 15                                 |
| attendanceRate           | 0.93 → "93% attendance rate"       |
| attendance color band    | ≥ 80% → tertiary teal              |

**Variant persona — member with active loan in arrears** (`MemberAccounts_WithActiveLoan`):

| Field                    | Value                              |
|--------------------------|------------------------------------|
| savingsBalance           | KES 8,200.00 (grew from KES 4,000) |
| savingsHistory            | 7 weekly points, KES 4,000 → 8,200 |
| activeLoan.productName   | Chama Emergency Loan               |
| activeLoan.outstanding   | KES 12,500.00                      |
| activeLoan.inArrears     | true → red border + banner         |
| activeLoan.dueDate       | 2026-07-10 (past-due)              |
| repayment ledger         | 4 monthly instalments, KES 2,500 ea |

**Role edit variant** (`MemberProfileState_ChairpersonEdit`, bottom sheet open):

| Field           | Value                              |
|-----------------|------------------------------------|
| isEditingRole   | true → bottom sheet slides up      |
| selectedRole    | SECRETARY (radio pre-selected)     |
| isUpdatingRole  | false → Confirm not spinning       |

- **Fineract client id**: `101` (client_001) — savings account `SAV-001-2026`.
- **Group context**: Mwangaza Women's Group, Kisumu West Branch, KES, weekly savings.
- **Attendance ledger**: 5 recorded meetings (Mar–Jul 2026), 1 ABSENT (May), 4 PRESENT.
- **Session role**: chairperson viewing treasurer — full edit affordance active.

---

## States

The ui.yaml declares 3 `screen_state` members (`Loading`, `Content`, `Error`) — each renders as a distinct HTML preview surface under `preview/`. The bottom sheet is an overlay of `content`, not a separate screen state.

### `loading`
Shimmer skeleton mirroring the 4-card content layout — parallel fanout of `get_client`, `get_client_accounts`, `get_member_role` through the Store5 read store.

```
[Member Profile header]                       ← top_bar visible with title
────────────────────────────────────────
[shimmer card ]  ← 100dp × full width, corner 16dp, surfaceVariant
[shimmer card ]
[shimmer card ]  ← shimmer count: 4 (header + savings + loan + attendance)
[shimmer card ]
```

- Cards: 100dp × full width, corner 16dp, `surfaceVariant` background shimmering 1.4s ease-in-out infinite.
- Respects `prefers-reduced-motion: reduce` (animation disabled → static skeleton).
- Top bar retains title "Member Profile" (back navigation always available; no chip render).
- No FAB, no interactive surfaces on loading — pointer events inert.

### `content` (see layout above)
All three parallel Fineract reads resolved via Store5 stream; SQLDelight cache satisfies re-entry within the 300s stale-while-revalidate window. Attendance rate computed locally from `meetingsAttended / totalMeetings`. Role edit sheet overlays this state on demand.

**Role edit overlay (bottom sheet)** — triggered from `content` when chairperson taps `Edit Role`:

```
┌─────────────────────────────────────────┐
│      Change Member Role                  │  sheet title · titleLarge, onSurface
├─────────────────────────────────────────┤
│  ◯  Chairperson                          │  list-item, 56dp, radio trailing
│  ◯  Treasurer                            │  selected = primary radio, unselected = outline
│  ◉  Secretary                            │  ← selectedRole seeded from ui state
│  ◯  Member                               │
├─────────────────────────────────────────┤
│  ┌──────── Confirm ───────────────────┐ │  filled button, primary, full-width, 56dp
│  └────────────────────────────────────┘ │  loading spinner when isUpdatingRole == true
└─────────────────────────────────────────┘
```

- Sheet elevation 8dp, top corners 24dp, `surface` background.
- Backdrop scrim 32% opacity; tap-outside dispatches `OnDismissRoleEdit`.
- Confirm button disabled when `selectedRole == role` (no-op guard).
- Radio rows are 56dp with full-row ripple; every tap dispatches `OnRoleSelected(role)` locally (no network).

### `error`
The Store5 read store's terminal Failure path — Fineract API failed AND cache is empty for this member. Renders full-viewport error state.

```
┌ Member Profile ────────────────────────┐
│                                          │
│                                          │
│               ☁                          │  error_state · cloud_off icon, 64dp
│      Could not load profile              │  title · titleLarge
│                                          │
│   {error.message}                        │  body · bodyMedium, --text-secondary
│   e.g. "No internet. Showing             │
│   cached profile."                       │
│                                          │
│  ┌─────── Retry ──────────────────┐    │  cta_label · primary #2E7D32, 48dp,
│  └────────────────────────────────┘    │  filled button
│                                          │  → Retry action_contract effect: call_api
└─────────────────────────────────────────┘  fresh=true, re-triggers Store5 stream
```

Error types (from `MemberProfileError`):
- `Network` — retry:true, `error_network` "No internet. Showing cached profile." (when cache HAS this member, this surfaces as a non-blocking snackbar and `content` stays visible instead).
- `Server` — retry:true, `error_server` "Server error. Please retry."
- `NotFound` — retry:false, `error_not_found` "Member not found." (dead memberId param).
- `Auth` — retry:false, `error_auth` "Session expired." → redirect to `login`.
- `RoleUpdateFailed` — snackbar-only overlay, does NOT transition the screen out of `content`.

---

## Interaction Patterns

1. **Back tap** → `OnBack` (effect: `navigate`) → pops the route back to `member-list` with the previous `groupId` param.
2. **Edit Role tap** → `OnEditRoleTap` (effect: `transform_state`) → sets `isEditingRole = true`, seeds `selectedRole = role`; only clickable when `isCurrentUserChairperson == true`. Sheet animates up 300ms MD3 emphasized.
3. **Role option tap (in sheet)** → `OnRoleSelected(role)` (effect: `transform_state`) → updates `selectedRole` locally, no network. Confirm activates when `selectedRole != role`.
4. **Confirm role change** → `OnConfirmRoleChange` (effect: `call_api`, external: Fineract-REST) → `MemberRepository.updateMemberRole(clientId, selectedRole)` calls `PUT /datatables/dt_member_role/{clientId}`. On 2xx: Store5 cache invalidates, `role` updates, sheet dismisses, `ShowSnackbar("Role updated successfully.")`. On error: `isUpdatingRole = false`, snackbar `error_role_update`. Gated by `cmp-network-monitor.isOnline`.
5. **Sheet dismiss** → `OnDismissRoleEdit` (effect: `transform_state`) → `isEditingRole = false`, `selectedRole = null`; scrim tap or hardware back.
6. **View Full History tap** → `OnViewSavings` (effect: `navigate`) → NavController push `member-savings-detail(memberId, groupId)`.
7. **Savings card tap (whole surface)** → also dispatches `OnViewSavings` — matches list-detail affordance.
8. **Retry tap (error state)** → `Retry` (effect: `call_api`, external: Fineract-REST) → parallel re-fanout of `get_client` + `get_client_accounts` + `get_member_role`; transitions screen back to `loading` first, then `content` or `error`.

---

## Accessibility

- Avatar exposes `contentDescription = "{{member.displayName}} profile photo"` (or `"initials {{member.initials}}"` when photoUri is null).
- Role chip: text + colored fill — never color-only (CHAIRPERSON/TREASURER/SECRETARY/MEMBER label always readable).
- Arrears banner: warning icon + explicit "in arrears" copy — supplements red border.
- Attendance progress bar: colored fill + explicit "{{rate}} attendance rate" text — 80/60 thresholds communicated in copy, not color alone.
- Bottom sheet role list: role `radiogroup`; each row role `radio` with `aria-checked` state.
- Confirm button `aria-disabled="true"` when `selectedRole == role`; loading state announces "Updating role…" via `aria-live="polite"`.
- Min touch targets: 48dp back arrow · 40dp Edit Role button · 56dp role list-item + Confirm CTA · full-row savings/loan/attendance card taps.
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS; text scaling to 200% keeps layout intact.
- Locales covered: English, Swahili (`Wasifu wa Mwanachama` / `Hariri Jukumu`), French (`Profil du Membre`), Hindi (`सदस्य प्रोफ़ाइल`).

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- Card ripple: MD3 standard 300ms ease-out on tap (savings card, loan card).
- Bottom sheet enter: 300ms MD3 emphasized decelerate; exit: 200ms accelerate.
- Backdrop scrim fade: 200ms linear, 0 → 32% opacity.
- Sparkline draw: 400ms ease-out on first paint; static under `prefers-reduced-motion`.
- Attendance progress fill: 500ms ease-out on first paint, no re-animation on state re-entry.
- Confirm button loading: MD3 circular indicator, primary stroke, 24dp inside the button.
- Snackbar (`ShowSnackbar`): MD3 slide-up + auto-dismiss 4s (role updated / role update failed / cached-profile fallback).
- Arrears banner: no motion — always-on emphasis.

---

## Data Flow (ui.yaml `business_logic.kind: aggregator`)

**External libs**: `Store5`, `SQLDelight`, `fineract-rest`
**Internal lib**: `cmp-network-monitor`

Read paths (offline-first, parallel):
- `member` ← `MemberRepository.getMember(memberId)` via Store5 stream
  - Source of truth: SQLDelight `members` cache (300s stale-while-revalidate)
  - Fetcher: Fineract `GET /clients/{memberId}` (identity, joinDate, phone)
- `accounts` ← `MemberRepository.getMemberAccounts(memberId)` via Store5 stream
  - Source of truth: SQLDelight `member_accounts` cache
  - Fetcher: Fineract `GET /clients/{memberId}/accounts` (savings balance + weekly sparkline + active loan)
- `role` ← `MemberRepository.getMemberRole(memberId)` via Store5 stream
  - Source of truth: SQLDelight `member_roles` cache
  - Fetcher: Fineract `GET /datatables/dt_member_role/{memberId}`
- `attendanceRate` — derived locally: `meetingsAttended.toDouble() / totalMeetings` (no network).
- `isCurrentUserChairperson` ← `SessionManager.currentRole == CHAIRPERSON` (in-memory).

Write path:
- `updateMemberRole(memberId, role)` → Fineract `PUT /datatables/dt_member_role/{memberId}` → on 2xx, `MemberRepository` invalidates `getMemberRole` cache and re-emits.
- Gated by `NetworkMonitor.isOnline == true`; offline attempt dispatches `ShowSnackbar(error_role_update)`.

Offline behavior: when `NetworkMonitor.isOffline == true` at screen entry, cache-only render is preferred — `content` state stays visible with any cached fields; the `Network` error surfaces as a non-blocking snackbar ("No internet. Showing cached profile."). Role edit is disabled offline (Confirm greyed with tooltip "Requires internet").

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/member-profile/ui.yaml` |
| API contract | `idea-layer/screens/member-profile/api.yaml` |
| Data flow | `idea-layer/screens/member-profile/data-flow.yaml` |
| Demo data | `idea-layer/screens/member-profile/demo-data.yaml` |
| Flow | `idea-layer/screens/member-profile/flow.yaml` |
| Tests | `idea-layer/screens/member-profile/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/member-profile/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/member-profile/preview/content.html` |
| Preview HTML (error) | `idea-layer/screens/member-profile/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/member-profile/prompts/{loading,content,error}.md` |
| Stitch mockup (probe deferred) | `idea-layer/mockups/member-profile/stitch/01-member-profile-content/{code.html,screen.png}` |
| Feature-group mockup | `idea-layer/mockups/member-onboarding/MOCKUP.md` (Member Profile section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from ui.yaml + demo-data.yaml + design-system tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The legacy stitch artifact under `stitch/01-member-profile-content/` (if present) will be regenerated on the next Stitch-enabled `/idea-feature-stitch --features member-profile` pass; the current 3-state ui.yaml and role-edit bottom sheet are the authoritative reference.
- The `active_loan_card` is variant-driven — swap `MemberAccounts` for `MemberAccounts_WithActiveLoan` in `demo-data.yaml` to render Content variant B (arrears path). Both variants share the same `content` state — activation is `accounts.activeLoan != null`, not a state transition.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features member-profile
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to ui.yaml components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
