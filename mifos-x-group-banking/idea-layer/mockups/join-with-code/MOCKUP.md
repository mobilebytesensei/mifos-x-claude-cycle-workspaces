# Join With Code — Mockup Spec

> Feature: `join-with-code` · Flow: `member-invitations-flow` · Route: `/groups/join`
> Single-screen invite-code entry + group preview + confirmation. Handles auth-gated resume via `login-signup` fallback.
> Derived from `screens/join-with-code/{ui,demo-data,flow}.yaml` + `screens/join-with-code/preview/*.html`.

## Design Language

**System**: Material Design 3, comfortable density
**Font**: Noto Sans — scaled up for low-vision rural users
**Palette**:
- Primary: #2E7D32 (VSLA-green) — trust, growth (top bar, hero icon, validate + join buttons, group name)
- Secondary: #FF8F00 (amber) — role chip accent (TREASURER)
- Secondary container: #FFDDB3 — role-chip background
- On secondary container: #2A1800 — role-chip text
- Surface: #FAFAFA — preview card background
- Surface variant: #ECEFE7 — subtle row separators
- Background: #FFFFFF
- Error container: #F9DEDC — error card bg
- On error container: #410E0B — error icon + message text
- Outline: #C2C9BD — text-field stroke

**Shape**: full=9999dp (chips), large=16dp (preview card), medium=12dp (error card), small=8dp (text-field)
**Elevation**: level_2 (3dp) for preview card, level_0 for error card (uses tonal bg)
**Min touch target**: 48dp (retry text-button, back arrow), 56dp (Validate, Join Group primary buttons)
**Motion**: Standard easing 250–400ms for state swaps, fade + slide-up 200ms for preview card reveal, 150ms for chip / spinner

---

## Screen-by-Screen

### JoinWithCodeScreen (`/groups/join?code={inviteCode}`)

**Layout**: `Scaffold` + `TopAppBar` + `Column` (centered, verticalScroll for small viewports) + IME-safe bottom padding

**Entry points**:
- Personal dashboard → "Join a Group" chip / CTA → `NavigateToJoinWithCode()` (no code prefill)
- Deep-link `app://groups/join?code=MWG7X2` → prefills `inviteCode` nav param → auto-focus + auto-validate on mount
- Unauthenticated deep-link → redirected to `login-signup` with `pendingInviteCode` param → returns here post-auth and auto-validates

**State machine**: `Initial → Validating → (Preview | ErrorInvalidCode | ErrorExpired | ErrorAlreadyMember | ErrorNetwork) → Joining → Success (navigates away)`

---

#### State: initial

```
┌─────────────────────────────────────────┐
│ [←] Join a Group                        │  TopAppBar h=56dp, bg=#2E7D32, text=#FFFFFF
├─────────────────────────────────────────┤
│                                         │  pad_top=32dp
│              ┌─────────┐                │
│              │  👥+    │                │  hero icon group_add, size=64dp
│              └─────────┘                │  tint=#2E7D32, centered
│                                         │  gap=24dp
│         Enter your invite code          │  bodyMedium 14sp, #424942, centered
│                                         │  gap=16dp
│  ┌────────────────────────────────────┐ │  text-field, filled, h=64dp
│  │                                    │ │  headlineMedium 28sp, letter-spacing=8sp
│  │           _ _ _ _ _ _              │ │  text_align=center, all-caps enforced
│  │                                    │ │  bg=#F0F2ED, stroke=#C2C9BD, radius=8dp
│  └────────────────────────────────────┘ │
│         Invite Code (6 chars)           │  label bodySmall 12sp, #6D6D6D
│                                         │  gap=24dp
│  ┌────────────────────────────────────┐ │
│  │           Validate Code            │ │  FilledButton, h=56dp, full-width
│  │  (disabled — grey #DDE5D9)         │ │  bg=#DDE5D9 (disabled), text=#8A938A
│  └────────────────────────────────────┘ │  radius=24dp
│                                         │
│                                         │
└─────────────────────────────────────────┘
```

- IME behavior: soft keyboard opens on mount (auto-focus field); keyboard=text with `capsLock=CHARS`, `maxLength=6`; content behind keyboard scrolls, Validate button rides above IME (`imePadding`).
- Validate button remains disabled (bg=disabled tint, text=onDisabled) until `state.inviteCode.length == 6` AND `state.inviteCode.matches("^[A-Z0-9]{6}$")`.
- Paste behavior: pasted string is uppercased, filtered to `[A-Z0-9]`, truncated to 6 — then triggers `OnCodeChange`.

**Demo data**: `inviteCode=""`, `inviteStatus=IDLE`, `error=null`.

---

#### State: validating

```
┌─────────────────────────────────────────┐
│ [←] Join a Group                        │
├─────────────────────────────────────────┤
│                                         │
│              ┌─────────┐                │
│              │  👥+    │                │  hero icon (unchanged)
│              └─────────┘                │
│                                         │
│         Enter your invite code          │
│                                         │
│  ┌────────────────────────────────────┐ │
│  │           M W G 7 X 2              │ │  invite_code_field (filled, focus-off,
│  │        (read-only during validate) │ │   not editable during API call)
│  └────────────────────────────────────┘ │
│                                         │  gap=24dp
│              ⟳ Checking code…           │  loading-indicator: 24dp circular spinner
│                                         │  tint=#2E7D32, label bodyMedium 14sp
│                                         │  #2E7D32, centered horizontally
│                                         │
│                                         │
└─────────────────────────────────────────┘
```

- Validate button is REPLACED by `validating_indicator` (not overlaid); spinner is a `CircularProgressIndicator` (indeterminate) with label to its right.
- text-field is visually locked (focused-container tint, cursor hidden) for the duration of the call — announces via `accessibility_label = "Validating invite code, please wait"`.
- On API return: transition duration 200ms fade-out spinner → 200ms fade-in preview OR error card (crossfade).

**Demo data**: `inviteCode="MWG7X2"`, `inviteStatus=VALIDATING`.

---

#### State: preview

```
┌─────────────────────────────────────────┐
│ [←] Join a Group                        │
├─────────────────────────────────────────┤
│                                         │
│              ┌─────────┐                │
│              │  👥+    │                │  hero icon (unchanged, smaller top pad = 16dp)
│              └─────────┘                │
│                                         │
│  ┌────────────────────────────────────┐ │
│  │           M W G 7 X 2              │ │  text-field: enabled, cursor hidden,
│  │                                    │ │  bg=#F0F2ED (still filled; hint that
│  └────────────────────────────────────┘ │  editing → re-validate)
│                                         │  gap=16dp
│  ┌────────────────────────────────────┐ │  preview card, elev=2dp, radius=16dp
│  │  You're invited to join            │ │  titleMedium 16sp, #424942 pad=20dp
│  │                                    │ │  gap=8dp
│  │  Mwangaza Women's Group            │ │  headlineSmall 24sp, #2E7D32, bold
│  │                                    │ │  gap=12dp
│  │  Type          Savings & Credit    │ │  row: label bodySmall 12sp #6D6D6D
│  │                                    │ │        value bodyMedium 14sp #424942
│  │  Organiser     Jane Otieno         │ │  gap=6dp between rows
│  │                                    │ │
│  │  Members       14 members          │ │
│  │                                    │ │  gap=16dp
│  │                        [ Member ]  │ │  role chip: bg=#FFDDB3 text=#2A1800
│  │                                    │ │  h=32dp, radius=8dp, trailing-align
│  └────────────────────────────────────┘ │
│                                         │  gap=24dp
│  ┌────────────────────────────────────┐ │
│  │            Join Group              │ │  FilledButton, h=56dp, full-width
│  │                                    │ │  bg=#2E7D32, text=#FFFFFF
│  └────────────────────────────────────┘ │  radius=24dp
│                                         │
└─────────────────────────────────────────┘
```

- Preview card enters via 200ms slide-up 12dp + fade; height animates (`animateContentSize`) so subsequent state changes feel continuous.
- Editing the invite-code field in this state resets `inviteStatus → IDLE`, hides the preview card, and re-disables Join Group — Validate re-appears.
- Role chip color adapts by role (from `demo-data.roleToAssign`): TREASURER → #FF8F00 / #FFFFFF; CHAIRPERSON → #A6F1A6 / #002106; SECRETARY → #D2E4FF / #002106; MEMBER (default) → #FFDDB3 / #2A1800.
- Card is announced as a single accessibility group ("Group preview details, Mwangaza Women's Group, Savings and Credit, organiser Jane Otieno, 14 members, your role Member").

**Demo data**: `groupPreview={groupName: "Mwangaza Women's Group", groupType: "Savings & Credit", organizerName: "Jane Otieno", memberCount: 14, roleToAssign: "Member"}`.

---

#### State: joining

Identical layout to `preview`, with Join Group button replaced by loading affordance:

```
│  ┌────────────────────────────────────┐ │
│  │        ⟳  Joining…                 │ │  FilledButton bg=#2E7D32 (unchanged)
│  └────────────────────────────────────┘ │  spinner 20dp tint=#FFFFFF + label
```

- Button is not disabled visually (background stays primary) but is un-clickable; `role=button, state=busy` for accessibility.
- text-field, top bar back arrow are BOTH disabled during joining (`onBack` guarded — a back tap during joining triggers a `ShowSnackbar("Please wait — joining group…")` instead of navigating away).

**Demo data**: `isJoining=true`, rest same as `preview`.

---

#### State: success (transient — dispatches nav)

- No visible surface; the ViewModel emits `NavigateToGroupDashboard(groupId=<from preview>)` inside a `LaunchedEffect(state.inviteStatus == VALID && !state.isJoining && state.joinAcknowledged)`.
- Optional 200ms confetti-free micro-transition: primary-tinted checkmark 48dp fades in for 300ms while nav dispatches — avoids a hard cut on slow devices.

---

#### State: error_invalid_code

```
┌─────────────────────────────────────────┐
│ [←] Join a Group                        │
├─────────────────────────────────────────┤
│              ┌─────────┐                │
│              │  👥+    │                │
│              └─────────┘                │
│                                         │
│  ┌────────────────────────────────────┐ │
│  │           X X X X X X              │ │  text-field: bg=#FFF6F5 (error tint),
│  │                                    │ │  stroke=#B3261E, cursor visible
│  └────────────────────────────────────┘ │
│                                         │  gap=12dp
│  ┌────────────────────────────────────┐ │  error card
│  │ ⚠  This invite code is not valid.  │ │  bg=#F9DEDC radius=12dp pad=16dp
│  │    Please check and try again.     │ │  icon 20dp #410E0B, message
│  │                                    │ │  bodyMedium 14sp #410E0B
│  │                                    │ │
│  │                       [ Retry ]    │ │  TextButton, text=#2E7D32 h=48dp
│  └────────────────────────────────────┘ │  aligned trailing
│                                         │  gap=24dp
│  ┌────────────────────────────────────┐ │
│  │           Validate Code            │ │  Validate re-enabled once user types
│  │  (disabled — needs new 6 chars)    │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

- Error card slides in below the field (12dp slide-up + fade, 200ms).
- Retry button dispatches `OnRetry` → same as tapping Validate with the current field value.
- text-field stroke error tint clears the moment the user types a new character.

**Demo data**: `inviteCode="XXXXXX"`, `error={type: InvalidCode, message: "This invite code is not valid...", retry: true}`.

---

#### State: error_expired

Same layout as `error_invalid_code` with two changes:

- Error message: **"This invite code has expired."**
- Below the message: **hint_expired** row (visible only for this state): "Ask your group organiser for a new invite code." (bodySmall 12sp #410E0B, italic).
- **No Retry button** (`error.retry == false`). The Validate button below stays disabled unless the user types a fresh code.

**Demo data**: `inviteCode="EXP001"`, `error={type: ExpiredCode, message: "This invite code has expired.", retry: false}`.

---

#### State: error_already_member

Same layout as `error_invalid_code` with:

- Error message: **"You are already a member of this group."**
- **No Retry button** (`error.retry == false`).
- Below the error card, secondary CTA (TextButton): **"Open Group"** → dispatches `NavigateToGroupDashboard(groupId=<from token payload>)` — friendly landing rather than dead-end.

**Demo data**: `inviteCode="MWG7X2"`, `error={type: AlreadyMember, message: "You are already a member of this group.", retry: false}`.

---

#### State: error_network

Same layout as `error_invalid_code` with:

- Icon: `cloud_off` 20dp tint=#410E0B.
- Error message: **"No internet connection. Please check your network and retry."**
- Retry button visible (`error.retry == true`).
- text-field is NOT tinted error (network failure is not a code failure); user's typed code preserved verbatim.

**Demo data**: `inviteCode="MWG7X2"`, `inviteStatus=IDLE`, `error={type: Network, message: "...", retry: true}`.

---

## Interaction Contracts (from ui.yaml `action_contract`)

| Action | Trigger | Effect | writes_to | reads_from | Library refs |
|---|---|---|---|---|---|
| `OnCodeChange(value)` | Type or paste in invite_code_field | transform_state | `state.inviteCode`, `state.inviteStatus`, `state.error` | — | — |
| `OnValidateCode` | Tap Validate / auto on 6-char reach with deep-link | call_api | `pending_invite_cache`, `state.groupPreview`, `state.inviteStatus` | `state.inviteCode` | InvitationRepository, GroupRepository |
| `OnConfirmJoin` | Tap Join Group | call_api | `pending_invite_cache`, `group_memberships_cache`, `state.isJoining` | `state.groupPreview`, `pending_invite_cache` | GroupRepository, AuthRepository, InvitationRepository |
| `OnRetry` | Tap Retry (error card) | call_api | `state.error`, `state.inviteStatus`, `state.groupPreview` | `state.inviteCode` | InvitationRepository, GroupRepository |
| `OnBack` | System back / top-bar back arrow | navigate | — (blocked during `joining`) | — | — |

**Auth gating**: `OnConfirmJoin` first reads `AuthRepository.isAuthenticated()`. If false → writes `pending_invite_cache = { code, groupId, expiresAt }` and emits `NavigateToLoginSignup(pendingInviteCode = state.inviteCode)`. On return from login, `LaunchedEffect(auth.isAuthenticated)` re-hydrates `pending_invite_cache` and auto-dispatches `OnConfirmJoin`.

**Deep-link handling**: `nav_params.inviteCode` non-null on mount →
1. Populate `state.inviteCode`
2. Skip Initial state, land directly on Validating (auto-dispatch `OnValidateCode`)
3. If unauthenticated at step 2 → detour to login-signup with `pendingInviteCode`, then resume validation post-auth.

---

## Accessibility

- Top bar back arrow: `accessibility_label="Back"`, `accessibility_role="button"`.
- Hero icon: `accessibility_label="Join a group illustration"`, `accessibility_hidden_when_focused_elsewhere=false` (decorative but described).
- Invite-code field: `accessibility_label="Invite code text field, 6 characters"`, `accessibility_hint="Enter 6 uppercase letters or digits"`, `accessibility_value` announces current chars.
- Validate button: `accessibility_label="Validate the entered invite code"`, `accessibility_state.disabled` reflects enabled binding.
- Validating indicator: `accessibility_label="Validating invite code, please wait"`, `accessibility_live_region=polite`.
- Preview card: single accessibility group (`mergeDescendants=true`); announced label concatenates title + group name + type + organiser + member count + role.
- Role chip: `accessibility_label="Your role in the group, {roleToAssign}"`.
- Confirm join button: `accessibility_label="Confirm and join the group"`, `accessibility_state.busy=isJoining`.
- Error card: `accessibility_live_region=assertive` on state entry so screen readers announce immediately.
- Retry button: `accessibility_label="Retry validating the invite code"`.

Contrast: all primary text (#424942 / #FFFFFF on #2E7D32 / #002106 on #A6F1A6 / #410E0B on #F9DEDC) meets WCAG AA 4.5:1. Chip tone pairs verified against MD3 tonal palette.

---

## Copy (i18n keys)

Sourced verbatim from `ui.yaml#i18n.en` — all UI strings resolve through `Res.string.<key>` per RULE-IMPL-NO-HARDCODED-STRING-001:

| Key | English |
|---|---|
| `screen_title` | Join a Group |
| `field_invite_code` | Invite Code |
| `field_invite_code_placeholder` | e.g. MWG7X2 |
| `btn_validate` | Validate Code |
| `btn_join_group` | Join Group |
| `btn_retry` | Retry |
| `label_validating` | Checking code… |
| `label_group_preview_title` | You're invited to join |
| `label_group_type` | Type |
| `label_organizer` | Organiser |
| `label_member_count` | Members |
| `label_members` | members |
| `hint_ask_organizer` | Ask your group organiser for a new invite code. |
| `error_invalid_code` | This invite code is not valid. Please check and try again. |
| `error_invalid_code_format` | Invite codes are 6 uppercase letters or digits. |
| `error_expired` | This invite code has expired. |
| `error_already_member` | You are already a member of this group. |
| `error_network` | No internet connection. Please check your network and retry. |
| `error_auth` | Your session has expired. Please log in again. |

Accessibility strings (`accessibility_*` keys) resolve identically — never inlined as `contentDescription = "…"` literal.

---

## Cross-Screen Dependencies

- **Login-Signup**: consumes `pendingInviteCode` nav param. On auth success it navigates back with `restore_intent=join-with-code` — `JoinWithCodeScreen` reads `pending_invite_cache` in `LaunchedEffect` and auto-resumes.
- **Group Dashboard**: destination for successful join. `groupId` sourced from validated invite response (not from user input).
- **Personal Dashboard**: entry point via "Join a Group" CTA. Return path on back = personal dashboard.
- **Companion invitations datatable (COMP-DT-004)**: read for token validation; write on accept (`accepted_at`, `accepted_by`).
- **Group repository (COMP-GRP-003)**: `associate_client_to_group(groupId, clientId, role)` on confirm.

---

## Analytics Events

Emitted per `docs.yaml#legacy_metadata.analytics`:

- `invite_code_entered` on `state.inviteCode.length == 6` transition (params: `code_length: 6`).
- `invite_code_validate_tapped` on `OnValidateCode` dispatch.
- `invite_token_valid` on `inviteStatus == VALID` (params: `group_id`, `role`).
- `invite_token_invalid` on error emission (params: `error_type ∈ {InvalidCode, ExpiredCode, AlreadyMember, Network, Auth}`).
- `join_group_confirmed` on `OnConfirmJoin` (params: `group_id`).
- `join_group_success` on Success state entry (params: `group_id`, `role`).
- `join_redirected_to_login` on Auth-redirect branch (params: `pending_code`).

Screen view: `screen_view=join_with_code_viewed` on `Initial | deep-link Validating` entry.

---

## Notes for Implementation

- Uses standard MD3 `Scaffold` — no custom top-bar; the hero + form is one `Column(Modifier.verticalScroll(rememberScrollState()).imePadding().safeContentPadding())`.
- Field uses `OutlinedTextField` with `visualTransformation` for uppercase enforcement and `KeyboardOptions(capitalization=Characters, imeAction=Done)`.
- Preview card is `Card(elevation=CardDefaults.cardElevation(defaultElevation=2.dp))` — never `ElevatedCard` (elevation drift under MD3 tonal surface).
- All screen dimensions declared here are IDEAL / mockup values; the actual Compose implementation uses design-token references (`MaterialTheme.colorScheme.primary`, `dimensionResource(R.dimen.spacing_medium)`) — hex values here are for designer alignment only.
- No hardcoded strings in Compose output — every visible literal resolves through `stringResource(Res.string.<key>)` per RULE-IMPL-NO-HARDCODED-STRING-001.
- Per-state Maestro coverage lives in `screens/join-with-code/tests.yaml`; the executed E2E walk is authored by `journey-maestro-gen` off `journeys/member-invitations-journey.yaml`.
