# Add Member — Mockup Specification

**Feature**: member-add | **Route**: `/groups/{groupId}/members/add` | **Type**: form
**Feature group**: group-management | **Flow**: member-add-flow
**Generated from**: `screens/member-add/ui.yaml`, `screens/member-add/demo-data.yaml`, `screens/member-add/api.yaml`, `screens/member-add/preview/*.html` (4 states rendered 2026-07-17)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature member-add`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: MifosSave-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, Save FAB button, focus rings
**On primary**: `#FFFFFF` — TopAppBar text + close icon, Save Member label
**Success**: `#1B5E20` on `#C8E6C9` — success snackbar / role selection confirmation
**Warning**: `#F57C00` on `#FFF9C4` — offline banner text emphasis
**Danger**: `#C62828` on `#FFCDD2` — validation error text, "PhoneAlreadyExists" inline error, photo remove icon
**Tertiary container**: `#FFE082` on `#FF8F00` — offline banner surface (amber, matches accent)
**Muted**: `#757575` on `#F5F5F5` — placeholder text, helper copy, photo picker surface
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (photo placeholder circle, filled inputs)
**Corner radius**: 60dp photo picker circle · 4dp text-field outlines · 12dp Save button · 16dp bottom-sheet top corners
**Elevation**: 0dp photo picker card (borderless surface) · 2dp save button pressed · 8dp bottom sheet
**Min touch target**: 120dp photo picker · 56dp every text-field + Save button · 56dp bottom-sheet list-items

---

## Screen: Add Member

### Entry
- From **member-list** FAB tap ("Add member") — the only entry point per `entry_points[]`
- Nav-param `groupId: String` (required, threaded from the parent group's route)
- Back / close navigation (via `close` icon in the top bar) pops the route and returns to `member-list`; the in-progress form is discarded, no member is created

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [✕]  Add Member              [#2E7D32]  │  top_bar — primary green fill, onPrimary
│                                          │  close icon (nav_icon: close) → OnBack
├─────────────────────────────────────────┤
│                                          │
│                ┌───────┐                 │  photo_picker_area
│                │  ＋📷 │                 │  120dp × 120dp, corner 60dp (perfect circle)
│                │       │                 │  surfaceVariant fill (#F5F5F5)
│                └───────┘                 │  centered · add_a_photo icon 40dp #757575
│                                          │  visible_when photoUri == null
│                                          │  → on_click OnPhotoPickerOpen → bottom sheet
│                                          │
│  First Name *                            │  first_name_field · text-field, 56dp
│  ┌────────────────────────────────────┐  │  label + required (*) marker
│  │ Grace                              │  │  demo value ("Grace")
│  └────────────────────────────────────┘  │  → on_change OnFirstNameChange
│                                          │
│  Last Name *                             │  last_name_field · text-field, 56dp
│  ┌────────────────────────────────────┐  │
│  │ Achieng                            │  │  demo value ("Achieng")
│  └────────────────────────────────────┘  │  → on_change OnLastNameChange
│                                          │
│  Phone Number *                          │  phone_field · text-field, 56dp
│  ┌──[+254]────────────────────────────┐  │  prefix "+254" pinned, keyboard: phone
│  │ 723456789                          │  │  max_length 13 · demo tail "723456789"
│  └────────────────────────────────────┘  │  → on_change OnPhoneChange
│  Kenyan number: +254 or 07XXXXXXXX       │  helper · bodySmall, --text-secondary
│                                          │
│  Role *                                  │  role_dropdown · text-field variant:dropdown
│  ┌────────────────────────────────────┐  │  56dp, options {Chairperson, Treasurer,
│  │ Secretary                     ▾    │  │  Secretary, Member}; demo = SECRETARY
│  └────────────────────────────────────┘  │  → on_change OnRoleSelected
│                                          │
│  ┌─────────────────────────────────────┐ │  save_button · filled, full_width, 56dp
│  │           Save Member              │ │  #2E7D32 fill, onPrimary text, corner 12dp
│  └─────────────────────────────────────┘ │  → on_click OnSubmit → member-list
│                                          │  (target: member-list per action_contract)
└─────────────────────────────────────────┘
```

### Layout (state: `content`, offline variant)

Same skeleton, plus the offline banner rendered above the Save button:

```
│  ┌─🚫 wifi_off ────────────────────────┐ │  offline_banner · visible_when isOffline
│  │ You are offline. This member will  │ │  tertiaryContainer fill (#FFE082),
│  │ be added when you reconnect.       │ │  onTertiaryContainer text (#FF8F00 emphasis)
│  └─────────────────────────────────────┘ │
```

### Bottom sheet: `photo_source_bottom_sheet`

Rendered as an MD3 bottom sheet with drag handle (24dp inset, 16dp top corner radius) when `showPhotoPicker == true` (triggered by tapping the photo circle):

```
┌─────────────────────────────────────────┐
│              ═══                         │  drag_handle · 32dp × 4dp, #E0E0E0
│                                          │
│  Add Photo                               │  title · titleLarge, --text-primary
│                                          │
│  📷  Take Photo                          │  camera_option · list-item, 56dp
│      Uses device camera                  │  → OnPhotoCaptured (system: camera)
│  ─────────────────────────────────────── │  → filekit-core record_media
│  🖼  Choose from Gallery                 │  gallery_option · list-item, 56dp
│      Pick an existing image              │  → OnPhotoSelected (system: gallery)
│                                          │  → filekit-core persist_file
└─────────────────────────────────────────┘
```

Once a photo is chosen the picker collapses and `photo_picker_area` swaps to:

```
        ┌───────┐
        │ [img] │   photo_preview visible_when photoUri != null
        │       │   fill:true, corner_radius 60dp
        │       │
        └───────┘─❌  photo_remove_button · icon-button (cancel, 24dp #C62828)
                     top_end, visible_when photoUri != null
                     → OnPhotoRemoved (effect: transform_state, photoUri = null)
```

### Demo Data (state: `content`, from `demo-data.yaml#MemberAddState`)

Grace Achieng being onboarded as SECRETARY into Mwangaza Women's Group (groupId 42, Kisumu West Branch, KES):

| Field           | Value                     | Notes                                        |
|-----------------|---------------------------|----------------------------------------------|
| firstName       | Grace                     | required, max 50, keyboard: name             |
| lastName        | Achieng                   | required, max 50, keyboard: name             |
| phone           | +254723456789             | prefix `+254`, E.164 Kenyan format           |
| selectedRole    | SECRETARY                 | one of {CHAIRPERSON, TREASURER, SECRETARY, MEMBER} |
| photoUri        | null                      | placeholder circle rendered                  |
| isOffline       | false                     | offline_banner hidden                        |
| isSubmitting    | false                     | Save button enabled                          |
| validationErrors| {}                        | no field-level errors                        |
| groupId         | "42"                      | threaded from member-list                    |

**Peer members (from `MemberWithSavingsContext`)** — how Grace will appear on member-list after the successful create/assign chain:

| clientId | Member         | Role        | Phone         | Savings (KES) | Activated  |
|----------|----------------|-------------|---------------|---------------|------------|
| 1006     | Grace Achieng  | SECRETARY   | +254723456789 | 1,500         | 2026-05-09 |
| 1007     | Amina Wanjiru  | TREASURER   | +254711223344 | 3,200         | 2026-05-16 |
| 1008     | John Kamau     | CHAIRPERSON | +254733889900 | 2,750         | 2026-05-16 |

**Offline variant (`MemberAddState_Offline`)**: `Faith Mutua` / `+254745000006` / MEMBER, `isOffline: true` — the amber banner renders and Submit will enqueue instead of navigate.

**Validation-error variant (`MemberAddState_ValidationError`)**: `firstName=""`, `phone="0712"` → the form displays inline error copy under both offending fields; Save button stays enabled but the tap is intercepted, no API call.

---

## States

The ui.yaml `state_model.screen_state.members` declares 4 states — `Content`, `Submitting`, `Success`, `Error` — each rendered as a distinct HTML preview under `preview/`.

### `content` (see layout above)

Default landing state. Form ready for input; all fields editable; offline banner rendered only when `isOffline == true`. FAB-styled Save button remains anchored below the role dropdown (not floating). Rendering pulls seed values from `demo-data.yaml#MemberAddState`.

### `submitting`

The Save button flips into a loading spinner; every field (text inputs, dropdown, photo picker) is disabled to prevent mid-flight edits.

```
│  ┌─────────────────────────────────────┐ │  save_button · loading = true
│  │        ⟳   Saving...               │ │  spinner + label, MD3 progress
│  └─────────────────────────────────────┘ │  bg = primary (#2E7D32), disabled tint
```

- All text-fields render at `opacity: 0.6`, `pointer-events: none`.
- Photo picker card is inert (no ripple), the remove `✕` icon is hidden.
- Top-bar close icon stays enabled — user can still abort (issues an implicit cancel on the in-flight request; the ViewModel treats it as `OnBack` and drops the request).
- Duration: bounded by the composite chain — `create_client` → `assign_member_role` → optional `upload_photo`. Median ~1.2s online, capped by `HttpTimeout` + `HttpRequestRetry`.

### `success`

Post-submit terminal state — the ViewModel emits `NavigateToMemberProfile(memberId, groupId)`. Rather than an intermediate screen, this state is a transient rendering (~200ms) that shows the success confirmation before the NavController pops+pushes `member-profile`.

```
┌─────────────────────────────────────────┐
│ [✕]  Add Member              [#2E7D32]  │
├─────────────────────────────────────────┤
│                                          │
│                  ✓                       │  success_icon · check_circle, 96dp
│                                          │  #1B5E20 on #C8E6C9 (success token)
│         Member added                     │  title · titleLarge, --text-primary
│                                          │
│     Grace Achieng has been               │  body · bodyMedium, --text-secondary
│     added to Mwangaza Women's Group.     │  interpolated from firstName/lastName + group
│                                          │
│  [ Opening profile… ]                    │  micro-copy · bodySmall, --text-secondary
│                                          │
└─────────────────────────────────────────┘
```

- On dispatch, `NavigateToMemberProfile` pops `member-add` off the back-stack and pushes `member-profile` with the newly-minted `clientId` from `create_client.response.clientId`.
- No user action is required — animation duration total 300ms.
- If the user hits back during this transient render, the ViewModel treats it as `NavigateBack` and returns to `member-list` (the freshly-created member appears in the list via the Store5 stream).

### `error`

Fineract API failed AND the request was NOT auto-queued for offline sync (i.e. Server / Auth / PhoneAlreadyExists / non-network Validation from the server). The form retains user input; inline error copy renders directly below the Save button.

```
┌─────────────────────────────────────────┐
│ [✕]  Add Member              [#2E7D32]  │
├─────────────────────────────────────────┤
│  [photo circle]                          │  photo_picker_area · content preserved
│                                          │
│  First Name *                            │
│  ┌────────────────────────────────────┐  │
│  │ Grace                              │  │  user input preserved
│  └────────────────────────────────────┘  │
│  … (last_name, phone, role rendered) …   │
│                                          │
│  ⚠ A member with this phone number      │  inline error banner
│    already exists.                       │  #C62828 text on #FFCDD2 surface,
│                                          │  bodyMedium, 12dp padding
│                                          │
│  ┌─────────────────────────────────────┐ │  save_button re-enabled (retry:true errors)
│  │           Save Member              │ │  Auth error → button hidden, redirect flow
│  └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

Error types (from `state_model.errors.MemberAddError`):

| Type                | Retry | Message key            | Copy                                                | Handling                                            |
|---------------------|-------|------------------------|-----------------------------------------------------|-----------------------------------------------------|
| `Validation`        | false | `error_validation`     | "Please fix the highlighted fields."                | Highlight offending fields (see validation variant) |
| `Network`           | true  | `error_network`        | "No internet. Member queued for sync."              | Falls back to `queue_offline` — see `submitting` → offline branch below |
| `Server`            | true  | `error_server`         | "Server error. Please retry."                       | Save button re-enabled; tap re-runs the composite    |
| `Auth`              | false | `error_auth`           | "Session expired."                                  | Redirect to `login` route; form state persisted     |
| `PhoneAlreadyExists`| false | `error_phone_exists`   | "A member with this phone number already exists."   | Inline banner + phone field highlighted red         |

**Network + offline branch**: when `NetworkMonitor.isOffline == true` at submit time, the ViewModel skips the API chain, enqueues a `CREATE_MEMBER` op to the SQLDelight `sync_queue`, emits `ShowOfflineSyncDialog` (transient success confirmation) → transitions to `success` state, and the composite drains later when connectivity resumes.

---

## Interaction Patterns

1. **Text-field type** → `OnFirstNameChange(value)` / `OnLastNameChange(value)` / `OnPhoneChange(value)` (all `effect: transform_state`) → per-keystroke VM update; simultaneously clears the corresponding key in `validationErrors` map. No network call. Phone field additionally re-runs the Kenyan E.164 format check.
2. **Photo circle tap** → `OnPhotoPickerOpen` (`effect: transform_state`) → sets `showPhotoPicker = true` → renders the bottom sheet. Pure VM flip, no I/O.
3. **Take Photo tap** → `OnPhotoCaptured(uri)` (`effect: record_media`, `filekit-core`) → launches native camera → on capture, writes returned path to `photoUri`. Sheet dismisses.
4. **Choose from Gallery tap** → `OnPhotoSelected(uri)` (`effect: persist_file`, `filekit-core`) → opens document picker → chosen `PlatformFile` path stored to `photoUri`. Sheet dismisses.
5. **Remove photo tap** (✕ overlay on preview) → `OnPhotoRemoved` (`effect: transform_state`) → sets `photoUri = null`, reverts to placeholder icon. No disk cleanup (Fineract multipart owns the eventual upload contract).
6. **Role dropdown select** → `OnRoleSelected(role)` (`effect: transform_state`) → sets `selectedRole` enum. Default value is `MEMBER` per ui.yaml.
7. **Save Member tap** → `OnSubmit` (`effect: call_api`, `library_refs: [cmp-network-monitor]`, `external_library_refs: [Fineract REST /clients, SQLDelight]`) → the composite:
   - Client-side validate `firstName` non-empty, `lastName` non-empty, `phone` matches Kenyan E.164; on failure → surface `Validation` error, halt.
   - `cmp-network-monitor` gate: online → chain `POST /clients` → `POST /datatables/dt_member_role/{clientId}` → optional `POST /clients/{clientId}/images` (multipart); on success emit `NavigateToMemberProfile`.
   - Offline → enqueue `CREATE_MEMBER` + `ASSIGN_MEMBER_ROLE` + optional `UPLOAD_MEMBER_PHOTO` ops to `sync_queue`, emit `ShowOfflineSyncDialog` → `success` transient render → pop.
   - Retryable server error → back to `content` with `error` banner + Save re-enabled.
8. **Close (top-bar ✕) tap** → `OnBack` (`effect: navigate`) → NavController pops route; in-progress form discarded; no `NavigateBack` event pre-hook — direct pop.

---

## Accessibility

- Every text-field carries a visible label AND the required-star (`*`) marker; the label doubles as the AccessibilityLabel for TalkBack / VoiceOver.
- Phone field's `+254` prefix is announced ("Kenya country code plus two-five-four") ahead of the editable region.
- Photo picker card exposes a single semantic action ("Add member photo, tap to open picker"); when a photo is present the label becomes "Member photo, tap to change; use remove button to clear."
- Bottom sheet list-items expose role `button`; the drag-handle carries `aria-hidden`.
- Inline validation copy is read INSTEAD of the field's helper (live-region assertive) so screen reader users hear the fix-me guidance immediately.
- Save button spinner in `submitting` state announces `"Saving member, please wait"` via aria-live.
- Min touch target 56dp on every text-field + dropdown + Save button + bottom-sheet list-item; 120dp on the photo picker (well above 44dp WCAG floor).
- Focus ring `--primary-700` 2dp solid, 2dp offset — visible on tab navigation across desktop-web target.
- Locales covered: English, Swahili (`Ongeza Mwanachama` / `Hifadhi Mwanachama`), French (`Ajouter un Membre` / `Enregistrer le Membre`), Hindi (`सदस्य जोड़ें` / `सदस्य सहेजें`).

---

## Motion & Feedback

- Bottom sheet slide-up: 300ms `cubic-bezier(0.4, 0, 0.2, 1)` — matches `--motion-slow`; slide-down on dismiss 200ms.
- Photo circle press: MD3 ripple 300ms ease-out; a tap without prior selection triggers the sheet, not a `record_media` shortcut.
- Save button loading spinner: MD3 circular progress, 1.4s rotation infinite — disabled under `prefers-reduced-motion` (spinner freezes, label shows "Saving…" plain-text).
- Success state check-icon: 200ms scale-in (0.6 → 1.0) + 200ms fade-in; then 300ms hold before pop-and-push to `member-profile`. All collapsed to 0ms under reduced motion.
- Offline banner slide-down: 150ms fade + 8dp translate, one-shot on `isOffline` flip.
- Snackbar (`ShowSnackbar` event, e.g. offline confirmation): MD3 4s auto-dismiss slide-up.
- Field focus / blur: 150ms border-color transition (`--border-default` → `--primary-700`).

---

## Data Flow (ui.yaml `business_logic.kind: composite`)

**External libs**: `filekit-core`, `SQLDelight`, `Store5`, `Fineract REST /clients`
**Internal libs**: `cmp-network-monitor`, `cmp-network-monitor-compose`

Read paths:
- `selectedRole` options → static enum backed by `MemberRole` DTO (resolved in VM; no API load).
- `groupId` → nav param threaded from `member-list`.
- `isOffline` → `NetworkMonitor.isOffline` stream (from `cmp-network-monitor`); flips the amber banner and gates the submit branch.

Write paths (all triggered by `OnSubmit`):
1. `MemberRepository.createMember(request)` → `POST /clients` → returns `resourceId` + `clientId`.
2. `MemberRepository.assignRole(memberId, role)` → `POST /datatables/dt_member_role/{clientId}` (uses the clientId from step 1) — writes to a Fineract custom datatable.
3. `MemberRepository.uploadPhoto(memberId, uri)` → `POST /clients/{clientId}/images` (multipart) — only when `photoUri != null`.

Offline behavior: when `NetworkMonitor.isOffline == true`, all three ops are enqueued via `SyncQueueRepository.enqueue` into the SQLDelight `sync_queue` table with operation codes `CREATE_MEMBER` / `ASSIGN_MEMBER_ROLE` / `UPLOAD_MEMBER_PHOTO`. On reconnect, the Store5-backed sync loop drains the queue in FIFO order and only pushes the new member onto the `member-list` stream once every op succeeds.

No local Store5 cache is read on this screen — the form is create-only; the freshly-created member becomes visible on `member-list` via the parent's Store5 stream after the composite completes.

---

## Related Artifacts

| Type                        | Path                                                             |
|-----------------------------|------------------------------------------------------------------|
| Screen YAML                 | `idea-layer/screens/member-add/ui.yaml`                          |
| API contract                | `idea-layer/screens/member-add/api.yaml`                         |
| Data flow                   | `idea-layer/screens/member-add/data-flow.yaml`                   |
| Demo data                   | `idea-layer/screens/member-add/demo-data.yaml`                   |
| Flow                        | `idea-layer/screens/member-add/flow.yaml`                        |
| Tests                       | `idea-layer/screens/member-add/tests.yaml`                       |
| Preview HTML (content)      | `idea-layer/screens/member-add/preview/content.html`             |
| Preview HTML (submitting)   | `idea-layer/screens/member-add/preview/submitting.html`          |
| Preview HTML (success)      | `idea-layer/screens/member-add/preview/success.html`             |
| Preview HTML (error)        | `idea-layer/screens/member-add/preview/error.html`               |
| Stitch prompts (per state)  | `idea-layer/screens/member-add/prompts/{content,submitting,success,error}.md` |
| Feature-group mockup        | `idea-layer/mockups/group-management/MOCKUP.md` (Add Member section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001; `requires_stitch: true` is honored in ui.yaml but the generator halted on missing key). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (4/4 states rendered 2026-07-17) + ui.yaml + api.yaml + demo-data.yaml + design-system tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The composite `business_logic.kind` (not `crud`) is load-bearing: `/implement` STEP 1.CONTEXT branches into `_shared/impl-context-rich-dispatch.md` (per RULE-IDEA-IMPL-INTELLIGENCE-001 II-4) so the generated `MemberAddViewModel` MUST import `cmp-network-monitor` + reference the Fineract REST DTOs listed in `business_logic.external_library_refs` — a plain `NoOp*Impl` will fail G-IMPL-STUB.
- The photo picker `bottom-sheet` is a distinct component from the picker `card`; the sheet is toggled by `showPhotoPicker` (transform_state) and never rendered in the top-level `states[].components` list (it's a `visible_when` overlay).
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features member-add
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to `ui.yaml#components` or `states[]` triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
