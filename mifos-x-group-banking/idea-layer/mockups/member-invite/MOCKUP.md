# Member Invite — Mockup Specification

**Feature**: member-invite | **Route**: `/groups/{groupId}/invite` | **Type**: form
**Feature group**: group-management | **Flow**: member-onboarding-flow
**Generated from**: `screens/member-invite/ui.yaml`, `screens/member-invite/demo-data.yaml`, `screens/member-invite/preview/*.html` (5 states rendered)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature member-invite`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for the invite code
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, Generate Code CTA, back button, Share button
**Accent**: `#FF8F00` (`--accent-700`, amber) — reserved for pooled-fund emphasis (not used on this screen)
**Success**: `#1B5E20` on `#C8E6C9` — accepted-invite badges (rare — pending list only shows unaccepted)
**Warning**: `#F57C00` on `#FFE082` — near-expiry indicator on pending invite rows
**Danger**: `#C62828` on `#FFCDD2` — Revoke text button, error banner icon, error banner text
**Muted**: `#616161` on `#F5F5F5` — expiry timestamp metadata, empty-state copy
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant · `#C8E6C9` `secondaryContainer` (generated code card)
**Corner radius**: 8dp form fields · 16dp generated_code_card · 8dp chips · 12dp banner
**Elevation**: 0dp form panel · 2dp generated_code_card · 0dp banner (colored fill only)
**Min touch target**: 56dp Generate/Share buttons · 48dp Copy Code / Copy Link outlined buttons · 48dp Revoke text button · 48dp Retry action

---

## Screen: Invite Member

### Entry
- From **member-list** (invite FAB tap); nav-param `groupId: String`
- From **group-dashboard** ("Invite member" action); nav-param `groupId: String`
- Back navigation pops the route and returns to the caller (`OnBack` → `NavigateBack`)

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [‹]  Invite Member           [#2E7D32]  │  top_bar — primary green, onPrimary text
├─────────────────────────────────────────┤
│  Send Invite                             │  create_invite_section_header
│                                          │  titleSmall, --primary-700, padding 16/8dp
│  ┌──────────────────────────────────┐   │
│  │ Phone or Email                   │   │  email_phone_field · text-field
│  │ e.g. +254712345678 or            │   │  keyboard: email, max_length 100
│  │      name@email.com              │   │  required: true, empty on `content`
│  └──────────────────────────────────┘   │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │ Role                        ▾    │   │  role_dropdown · text-field(dropdown)
│  │ Member                            │   │  default: "member"
│  └──────────────────────────────────┘   │  options: Member / Treasurer /
│                                          │           Secretary / Chairperson
│                                          │
│  ┌──────────────────────────────────┐   │
│  │        Generate Code              │   │  generate_button · filled, full_width,
│  │                                    │   │  56dp, --primary-700, onPrimary text
│  └──────────────────────────────────┘   │  enabled_when: emailPhone.isNotBlank()
│                                          │  loading spinner when isGenerating==true
├─────────────────────────────────────────┤
│  ───────────────────────────────         │  divider · 16dp vertical padding
├─────────────────────────────────────────┤
│  Pending Invites                         │  pending_invites_section_header
│                                          │  titleSmall, --primary-700, 8dp bottom
│  ┌──────────────────────────────────┐   │
│  │ +254712345678         [treasurer]│   │  pending_invite_row #1
│  │ Expires 2026-07-24T08:00:00Z     │   │  bodyMedium contact · labelSmall expiry
│  │                       [🗙 Revoke]│   │  chip: primaryContainer / onPrimaryContainer
│  └──────────────────────────────────┘   │  Revoke: text-button, --danger #C62828
│  ┌──────────────────────────────────┐   │
│  │ amina.omondi@email.com   [member]│   │  pending_invite_row #2
│  │ Expires 2026-07-25T14:30:00Z     │   │
│  │                       [🗙 Revoke]│   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Demo Data (state: `content`, from `demo-data.yaml` + ui.yaml `states.content.demo_data`)

Pending invite list for Mwangaza Women's Group (groupId=42) — 2 rows displayed (the third demo row `T5N1HW` was already accepted 2026-07-19 and would not appear in a live COMP-DT-003 response):

| rowId | Contact                    | Role      | Expires (UTC)          | Status  |
|-------|----------------------------|-----------|------------------------|---------|
| 101   | `+254712345678`            | treasurer | 2026-07-24T08:00:00Z   | pending |
| 102   | `amina.omondi@email.com`   | member    | 2026-07-25T14:30:00Z   | pending |

- **Form seed** — `emailPhone: ""`, `selectedRole: "member"`, `isGenerating: false`, `isLoadingPending: false`.
- **Third seed row** — `rowId: 100` (`T5N1HW`, secretary) is accepted; excluded from `content` render but retained in `demo-data.yaml` for `join-with-code` cross-feature test fixtures.
- **Generate flow** — the reference `CreateInviteRequest` (phone `+254711223344`, role `treasurer`, expires 2026-07-24) demonstrates the E.164-formatted body the button emits.

---

## States

The ui.yaml declares 5 `screen_state` members (`Content`, `Generating`, `Generated`, `Loading`, `Error`) — each renders as a distinct HTML preview surface under `preview/`.

### `loading`
First-paint state while COMP-DT-003 fetches unaccepted invites for the group. The create-invite panel is fully editable while the pending panel shows a centered spinner.

```
[Invite Member header]                     ← top_bar visible, back arrow enabled
────────────────────────────────────────
Send Invite
[ Phone or Email (empty) ]                  ← email_phone_field editable
[ Role: Member ▾ ]                          ← role_dropdown editable
[ Generate Code (disabled) ]                ← generate_button disabled
                                              (emailPhone still blank)
────────────────────────────────────────
Pending Invites
              ◐ loading                     ← pending_invites_loading_indicator
                                              MD3 CircularProgressIndicator,
                                              --primary-700, 40dp, centered, 24dp pad
```

- Spinner size 40dp with 24dp padding around it — matches MD3 loading-indicator guidance.
- Respects `prefers-reduced-motion` (indicator becomes a static filled circle).
- Create-invite form remains fully interactive during pending fetch — organizer can start typing while the list resolves.
- Generate button stays disabled (blank field), not because of loading — this is the natural entry state.

### `content` (see layout above)
Both panels resolved. Empty form + pending list rendered from Store5 cache-hydrate + COMP-DT-003 network freshness.

- Empty-pending sub-state renders `pending_invites_empty_state` copy in place of the list: *"No pending invites. Generate a code above to invite members."* (bodyMedium, `--outline` #757575, 24dp padding, center-aligned).
- Generate Code stays disabled until the organizer types ≥1 character.

### `generating`
Organizer typed `+254798765432`, selected role `secretary`, tapped Generate Code. COMP-DT-002 in-flight.

```
Send Invite
[ Phone or Email:  +254798765432 ]
[ Role: Secretary ▾ ]
[ ◐ Generating…      ] ← generate_button loading=true, spinner inside button,
                          label replaced by MD3 CircularProgressIndicator (20dp),
                          button disabled during flight
────────────────────────────────────────
Pending Invites
[ +254712345678 · treasurer · Expires … · Revoke ]
[ amina.omondi@email.com · member · Expires … · Revoke ]
```

- Only the Generate Code button changes: label swaps to a 20dp spinner (MD3 button-loading affordance), background stays `--primary-700`, ripple disabled.
- Form fields remain populated but disabled (visually still colored, not greyed) so the input can't be edited mid-request.
- Pending list stays visible — organizers can see existing invites while creating a new one.
- On success → `generated` state (below); on failure → `error` state with editable form preserved.

### `generated`
COMP-DT-002 returned `token: "K7X2P9"`, `inviteLink: "https://mifos.app/join?token=K7X2P9&group=42"`. Code card appears between the Generate Code button and the divider.

```
Send Invite
[ Phone or Email:  +254798765432 ]
[ Role: Secretary ▾ ]
[ Generate Code ]                           ← button re-enabled; ready for next invite

┌──────────────────────────────────────┐    generated_code_card
│  INVITE CODE                          │    background: --secondaryContainer #C8E6C9
│                                        │   elevation 2dp, corner 16dp, padding 20dp
│      K 7 X 2 P 9                       │    displaySmall, onSecondaryContainer,
│                                        │   monospace, letter-spacing 4sp
│  Join Link                             │    labelMedium, padding_top 12dp
│  https://mifos.app/join?token=K7X2P…   │    bodySmall, --secondary, ellipsize=end,
│                                        │   max_lines 2
│  ┌────────────┐ ┌────────────┐ ┌────┐│    code_actions_row, gap 8dp
│  │ 📋 Copy Code│ │ 🔗 Copy Link│ │ ↗  ││    Copy Code: outlined, --primary border+text
│  └────────────┘ └────────────┘ └────┘│    Copy Link: outlined, --primary border+text
│                                        │    Share:     filled,   --primary bg, onPrimary
└──────────────────────────────────────┘
────────────────────────────────────────
Pending Invites  (unchanged 2 rows)
```

- Code letter-spacing 4sp so `K7X2P9` scans as six discrete glyphs — matches SMS-friendly transcription.
- Copy Code / Copy Link show a snackbar (`ShowSnackbar` event) *"Code copied"* / *"Link copied"* on tap.
- Share button opens the native OS share sheet (`ShowShareSheet(link, code)`) — WhatsApp / SMS / email / any registered target.
- Once a code is shared and accepted, the new row appears in Pending Invites on the next COMP-DT-003 refresh (Store5 stream + poll on resume).

### `error`
Any Fineract call (COMP-DT-002 generate, COMP-DT-003 load-pending, COMP-DT-005 revoke) failed. Banner surfaces at the top of the panel with a Retry action; the create-invite form and pending list stay editable / visible.

```
[Invite Member header]
────────────────────────────────────────
Send Invite
[ Phone or Email:  +254798765432 ]         ← form retains draft — organizer
[ Role: Secretary ▾ ]                        doesn't lose their entry
[ Generate Code ]                           ← re-enabled once error surfaces

┌ ⚠ No internet connection. Please check ┐    error_banner
│    your network and try again.          │    background: --errorContainer #FFCDD2
│                              [ Retry ]  │    text: onErrorContainer #B71C1C
└─────────────────────────────────────────┘    icon: error_outline
                                                Retry: text button, right-aligned
────────────────────────────────────────
Pending Invites  (stale cached rows shown when available)
```

Error variants (from `MemberInviteError`):
- `Validation` — retry:false, `error_validation` *"Please enter a valid phone number or email address."* (shown inline under the field, not banner)
- `Network` — retry:true, `error_network` *"No internet connection. Please check your network and try again."* → `OnRetry` re-issues last call
- `Server` — retry:true, `error_server` *"Server error. Please try again."*
- `Auth` — retry:false, `error_auth` *"Session expired. Please log in again."* → redirect to `login`
- `RevokeFailure` — retry:true, `error_revoke` *"Failed to revoke invite. Please try again."*; the optimistically-removed row is re-inserted at its original position before the banner appears.

---

## Interaction Patterns

1. **Type in phone/email field** → `OnEmailPhoneChange(value)` (effect: `transform_state`) — updates `emailPhone` on every keystroke; Generate Code button re-evaluates `enabled = emailPhone.isNotBlank()` (no debounce, purely local).
2. **Pick role from dropdown** → `OnRoleSelect(role)` (effect: `transform_state`) — dropdown collapses; `selectedRole` mirrors the pick; MD3 dropdown ripple + trailing icon rotation 150ms.
3. **Tap Generate Code** → `OnGenerateInvite` (effect: `call_api`, external: fineract-rest) → POST COMP-DT-002 with `{groupId, invitedEmailPhone, roleToAssign, expiresAt=now()+7d ISO-8601}` → on 2xx transitions `generating → generated`; on error transitions `generating → error`. `cmp-network-monitor` gates the call — offline emits `MemberInviteError.Network` immediately without a network attempt.
4. **Tap Copy Code** → `OnCopyCode` (effect: `copy_clipboard`) → writes the 6-char token to the platform clipboard via `ClipboardManager`; emits `ShowSnackbar("Code copied")` (4s auto-dismiss).
5. **Tap Copy Link** → `OnCopyLink` (effect: `copy_clipboard`) → writes the full `mifos.app/join?token=…&group=…` URL; emits `ShowSnackbar("Link copied")`.
6. **Tap Share** → `OnShareLink` (effect: `share_external`) → emits `ShowShareSheet(link, code)`; platform layer opens the OS share sheet pre-populated with the code and link.
7. **Tap Revoke on a pending row** → `OnRevokeInvite(inviteId=rowId)` (effect: `delete`, external: fineract-rest) → DELETE COMP-DT-005 with rowId; optimistically removes the row from `pendingInvites` before the network call; on 4xx/5xx re-inserts the row and shows `RevokeFailure` banner. Row-level ripple + 300ms fade-out on optimistic removal (respects reduced-motion).
8. **Tap Retry on error banner** → `OnRetry` (effect: `call_api`) → re-issues the last failed call (generate / load / revoke). Banner disappears on success; a new banner surfaces on repeated failure.
9. **Tap back arrow / system back** → `OnBack` (effect: `navigate`) → emits `NavigateBack`; NavController pops to the caller (`member-list` or `group-dashboard`). Any in-progress form draft is discarded (no auto-save — organizer must explicitly Generate to persist).

---

## Accessibility

- Every input carries a real label (`Phone or Email`, `Role`) — no placeholder-only labelling.
- Placeholder text `e.g. +254712345678 or name@email.com` is a hint, not a label — clears on focus.
- Generate Code discloses disabled-state via `aria-disabled="true"` when `emailPhone.isBlank()`.
- Generated code is grouped as an ARIA region with `aria-label="Invite code K7X2P9, join link https://mifos.app/join?token=K7X2P9&group=42"` for screen readers.
- Code characters have letter-spacing 4sp so a screen reader announces them individually.
- Copy Code / Copy Link / Share expose distinct labels (never icon-only); icons are 24dp with `--primary-700` tint.
- Revoke button uses `--danger` red AND the cancel icon — never color-only.
- Pending invite rows announce as *"Invite for {invitedEmailPhone}, role {roleToAssign}, expires {expiresAt}, Revoke"* to screen readers.
- Error banner uses `role="alert"` so it announces immediately on appearance.
- Min touch target 56dp on Generate/Share, 48dp on Copy/Retry/Revoke, 48dp on dropdown trigger.
- Locales covered: English (default), Swahili (`Mwalike Mwanachama` / `Tuma Mwaliko`), French (`Inviter un membre`), Hindi (`सदस्य आमंत्रित करें`) — via `{strings.*}` tokens from `_strings/strings.yaml`.

---

## Motion & Feedback

- Field focus: MD3 outlined text-field focus-ring 150ms ease-out, ring color `--primary-700`.
- Dropdown open: 150ms ease-out expand + trailing icon 180° rotation.
- Generate Code press: MD3 ripple 300ms; on `isGenerating=true` the button label cross-fades to a 20dp CircularProgressIndicator over 100ms.
- Generated code card entrance: 200ms ease-out fade-in + 8dp Y translate; disabled under `prefers-reduced-motion`.
- Copy / Share buttons: MD3 ripple 300ms; snackbar slide-up 200ms, auto-dismiss 4s.
- Revoke optimistic removal: row fade-out 300ms ease-in — collapses list gap over 200ms; on failure the row fades back in (250ms).
- Error banner: slide-down 200ms from top of the panel; Retry press = MD3 ripple.
- Loading spinner (pending panel): MD3 rotate 1.4s linear infinite; static filled circle under `prefers-reduced-motion`.

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `fineract-rest` (companion invitations datatable)
**Internal libs**: `core/network`, `cmp-network-monitor`
**DI**: `InvitationRepository`, `ClipboardManager`

Read path:
- `pendingInvites[]` ← `InvitationRepository.getPendingInvites(groupId)` via Store5 stream
  - Source of truth: SQLDelight companion cache (excludes rows where `acceptedAt != null`)
  - Fetcher: Fineract `GET COMP-DT-003 /datatables/mifosx_invitations?groupId={groupId}&acceptedAt=is.null` gated by `cmp-network-monitor`
  - `OnRetry` triggers `fresh=true`; pull-to-refresh (`OnRefresh`, not wired on this screen) would too

Write paths:
- `OnGenerateInvite` → POST COMP-DT-002 with `{groupId, invitedEmailPhone, roleToAssign, expiresAt}` — returns `{token, inviteLink, rowId}` — Store5 upsert on success, pending list refetches on next resume.
- `OnRevokeInvite(rowId)` → DELETE COMP-DT-005 by rowId — Store5 optimistic remove; on failure Store5 re-inserts.

Local-only:
- `OnEmailPhoneChange`, `OnRoleSelect`, `OnCopyCode`, `OnCopyLink`, `OnShareLink`, `OnBack` — no network.

Offline behavior: `cmp-network-monitor.isOffline == true` at `OnGenerateInvite` / `OnRevokeInvite` short-circuits with `MemberInviteError.Network`; the pending list still renders cached rows because the Store5 stream serves SoT.

Auth: `MemberInviteError.Auth` on any 401 → emits `NavigateBack` after redirecting to `login`; the token flow requires a signed-in session.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/member-invite/ui.yaml` |
| API contract | `idea-layer/screens/member-invite/api.yaml` |
| Data flow | `idea-layer/screens/member-invite/data-flow.yaml` |
| Demo data | `idea-layer/screens/member-invite/demo-data.yaml` |
| Flow | `idea-layer/screens/member-invite/flow.yaml` |
| Tests | `idea-layer/screens/member-invite/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/member-invite/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/member-invite/preview/content.html` |
| Preview HTML (generating) | `idea-layer/screens/member-invite/preview/generating.html` |
| Preview HTML (generated) | `idea-layer/screens/member-invite/preview/generated.html` |
| Preview HTML (error) | `idea-layer/screens/member-invite/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/member-invite/prompts/{loading,content,generating,generated,error}.md` |
| Stitch mockup (probe deferred) | `idea-layer/mockups/member-invite/stitch/` |
| Feature-group mockup | `idea-layer/mockups/group-management/MOCKUP.md` (Member Invite section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from ui.yaml (5 states, 15 components, action_contract-bearing on_click handlers), demo-data.yaml (3 DTOs: `PendingInvite`, `CreateInviteRequest`, `GeneratedInvite`), and design-system tokens (`--primary-700`, `secondaryContainer`, `errorContainer`) per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The five `screen_state` members (`Content`, `Generating`, `Generated`, `Loading`, `Error`) each own a distinct visual composition; `generating` is intentionally NOT collapsed into `content` with an inline spinner because the Generate Code button label swap AND the disabled form fields are two coordinated changes that the ViewModel emits as a single state transition.
- The generated code card uses `secondaryContainer` (light green `#C8E6C9`) rather than surface-elevation — the intent is a "receipt" affordance that reads as *"here is what you just made"* rather than *"another form field"*.
- `Revoke` uses `--danger` red on white (not red-on-white-with-red-fill) because the row is inline within a neutral surface — the visual weight comes from the icon + color, not a filled destructive button.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features member-invite
  ```
- Design conformance verifier: preview HTML mirrors the layouts above; any hand-edit to `ui.yaml#components` or `states.*.demo_data` triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
