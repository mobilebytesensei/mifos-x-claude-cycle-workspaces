# Settings Logout Dialog — Mockup Specification

**Feature**: settings-logout-dialog | **Route**: `dialog (overlaid on settings)` | **Type**: dialog
**Feature group**: authentication | **Flow**: settings-flow
**Generated from**: `screens/settings-logout-dialog/ui.yaml`, `screens/settings-logout-dialog/demo-data.yaml`, `design-system/DESIGN.md` (3 states declared — idle, logging_out, error)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature settings-logout-dialog`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: MifosSave-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first · regulated-industry
**Font**: Roboto (Android) / SF Pro (iOS) — system stack
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — Cancel button text color
**Danger**: `#C62828` (`--danger`) — Log Out button background (destructive CTA)
**On danger**: `#FFFFFF` (onError) — Log Out button label + spinner tint
**Error text**: `#C62828` (error) — inline logout_error_text
**Surface**: `#FFFFFF` (`--bg-canvas`) — dialog surface
**Surface variant text**: `#616161` (`--text-secondary`, onSurfaceVariant) — body copy
**On surface**: `#212121` (`--text-primary`) — title
**Scrim**: `#000000` @ 32% opacity — modal backdrop over the settings screen
**Corner radius**: 28dp dialog container · 20dp button (MD3 filled) · full-round text button
**Elevation**: 6dp dialog surface over scrim
**Min touch target**: 48dp Cancel button · 48dp Log Out button · 24dp minimum gap between actions

---

## Screen: Settings Logout Dialog

### Entry
- From **settings** (source screen) when the user taps the "Log Out" list item / button — trigger `user_taps_logout_button`
- The dialog is a modal overlay: parent settings screen stays rendered underneath the scrim, no route push
- Back gesture / outside-tap dismisses the dialog (equivalent to Cancel — no session mutation)

### Layout (state: `idle`)

```
┌─────────────────────────────────────────┐
│                                          │
│    (Settings screen dimmed behind        │  scrim · #000 @ 32%
│     32% black scrim — visible but        │  parent-composed
│     inert; tap outside = dismiss)        │
│                                          │
│      ┌─────────────────────────────┐    │
│      │                              │    │  dialog surface · #FFFFFF
│      │  Log Out?                    │    │  dialog_title · titleLarge, onSurface
│      │                              │    │  weight 500, 22sp
│      │  You will be logged out of   │    │  logout_body_text · bodyMedium,
│      │  your account. Any unsynced  │    │  onSurfaceVariant #616161, 14sp
│      │  changes will be lost.       │    │  line-height 20, max-width 296dp
│      │                              │    │
│      │                              │    │  24dp gap → dialog_actions_row
│      │            [Cancel] [Log Out]│    │  actions row · justify end, gap 8dp
│      │                              │    │  Cancel — text button, primary #2E7D32
│      └─────────────────────────────┘    │  Log Out — filled button, danger #C62828,
│                                          │  onError #FFFFFF label
│                                          │
│      radius 28dp · elevation 6dp         │
│      inset 24dp · width min(312dp, 90vw) │
│                                          │
└─────────────────────────────────────────┘
```

### Demo Data (state: `idle`, from `demo-data.yaml`)

Single-session context — Amina Hassan is the group ORGANIZER logging out from Mwangaza Women's Group:

| Field                | Value                     | Notes                                            |
|----------------------|---------------------------|--------------------------------------------------|
| username             | `amina.hassan`            | SessionInfoDto — cached in multiplatform-settings |
| displayName          | `Amina Hassan`            | Not rendered on the dialog itself (privacy)      |
| memberRole           | `ORGANIZER`               | Session role (permission source for FABs elsewhere) |
| lastSync             | `2026-05-09T08:30:00Z`    | Used only if pendingSyncCount > 0 warn banner    |
| pendingSyncCount     | `2`                       | Two queued offline ops — informs SyncFlushResult |
| clientId             | `101`                     | Fineract client binding                          |
| groupId              | `1`                       | Currently-selected group                         |
| isLoggingOut         | `false`                   | SettingsLogoutDialogState — idle default         |
| logoutError          | `null`                    | Error text hidden                                |
| SyncFlushResult      | 2 flushed / 0 failed / 1420ms / SUCCESS | Materializes after OnConfirmLogout runs |

- **Body copy is deliberately generic** — no username / role is echoed on the dialog itself; the confirmation is context-free per regulated-industry taste dial.
- **Warn-first behavior**: because `pendingSyncCount == 2`, the ui.yaml `business_logic` flushes queued offline ops FIRST (Store5 → SQLDelight `SyncQueueRepository`), then clears session. On failure, `error` state shows the inline error text.
- **No Fineract call**: this is a client-side-only mutation — no `/authentication/logout` endpoint hit; `api.yaml` declares no server-facing op for this feature.

---

## States

The ui.yaml declares 3 `screen_state` members (`Idle`, `LoggingOut`, `Error`) — each renders as a distinct dialog surface.

### `idle` (see layout above)
Default entry state — awaiting user confirmation. Both buttons enabled. No spinner. Body text visible. Error text hidden.

- Cancel button — text variant, primary `#2E7D32`, 14sp uppercase-free label, no elevation.
- Log Out button — filled danger `#C62828`, onError `#FFFFFF` label, 20dp corner, 48dp height, 24dp horizontal padding.
- Tap outside dialog OR back gesture behaves identically to Cancel (`OnDismiss`).

### `logging_out`
User has tapped Log Out — `isLoggingOut == true`. Log Out button disabled and shows an inline spinner; Cancel button remains tappable (user can still abort before the flush completes — but the client-side lifecycle honors the button label change).

```
      ┌─────────────────────────────┐
      │                              │
      │  Log Out?                    │  dialog_title unchanged
      │                              │
      │  You will be logged out of   │
      │  your account. Any unsynced  │
      │  changes will be lost.       │
      │                              │
      │            [Cancel] [ ◐ ]    │  Log Out button — 20dp circular progress
      │                              │  onError tint, disabled state,
      └─────────────────────────────┘  same background #C62828
```

- Spinner: 20dp circular indeterminate, 2dp stroke, MD3 progress spec.
- `enabled_when: !isLoggingOut` → button non-clickable, ripple suppressed.
- Cancel remains enabled (client-side session state is NOT yet cleared — user can still bail).
- Body copy and title do NOT change — this is a brief transient state (~1.4s per `SyncFlushResult.durationMs`).

### `error`
Logout attempt failed — `logoutError != null`, `isLoggingOut == false`. Inline error text appears between the body and the actions row; both buttons re-enable so the user can retry or cancel.

```
      ┌─────────────────────────────┐
      │                              │
      │  Log Out?                    │  dialog_title unchanged
      │                              │
      │  You will be logged out of   │
      │  your account. Any unsynced  │
      │  changes will be lost.       │
      │                              │
      │  Failed to log out. Please   │  logout_error_text · bodySmall 12sp
      │  try again.                  │  color error #C62828, 8dp top gap
      │                              │
      │            [Cancel] [Log Out]│  both re-enabled
      └─────────────────────────────┘
```

- Error text bound to `{{logoutError}}` — populated from `SettingsLogoutDialogState.errors.LogoutFailed`.
- Visible_when: `logoutError != null` — the error slot is absent from the composition tree in idle/logging_out.
- Retry pathway: user re-taps Log Out → transitions back to `logging_out` → attempts flush + session clear again.
- No auto-dismiss; error persists until user acts.

---

## Interaction Patterns

1. **Cancel tap** → `OnDismiss` (effect: `navigate`) → dismisses the dialog and pops back to the settings screen via NavController. No session data is touched; no destructive work runs. Also triggered by scrim tap and system back gesture.
2. **Log Out tap** → `OnConfirmLogout` (effect: `delete`, external libs: SQLDelight, Store5, multiplatform-settings) → sequence:
   1. Flush pending offline ops from Store5/SQLDelight `SyncQueueRepository` (2 queued per demo).
   2. If flush fails and `pendingSyncCount > 0`, surface warn (implementation may branch to a nested "Discard unsynced?" prompt; ui.yaml keeps this to a single inline error).
   3. Clear local session via `SessionManager` (release in-memory tokens).
   4. Delete cached auth tokens from `multiplatform-settings` DataStore.
   5. Emit `NavigateToLogin` event → NavController push `login-signup`, clearing the back stack.
3. **Outside-tap / back gesture** → equivalent to `OnDismiss`; no separate action contract.
4. **Retry from `error`** → re-tap Log Out repeats the sequence from step 2.1 with fresh state.

---

## Accessibility

- Dialog announced as an alert (`role="alertdialog"` / `Semantics(dialog=true, ...)` on Compose Multiplatform) with `dialog_title` labeling the surface.
- Focus is trapped inside the dialog while it is open; initial focus lands on the Cancel button (safer default per destructive-action safeguard — user must intentionally reach for Log Out).
- Scrim intercepts pointer events on the parent settings screen; screen readers skip the dimmed content.
- Log Out button carries an accessibility label of the full sentence "Log out of Amina Hassan's account, this cannot be undone" derived from session + copy; the visible label stays terse ("Log Out").
- Error text is announced via `aria-live="assertive"` when it appears — the user hears the failure without navigating.
- Both buttons meet the 48dp min touch target; horizontal gap 8dp between them keeps them within thumb reach but distinct.
- Locales covered (from `ui.yaml#i18n`):
  - English — Log Out? / Cancel / Log Out / Failed to log out. Please try again.
  - Swahili — Toka? / Ghairi / Toka
  - French — Se Déconnecter? / Annuler / Se Déconnecter
  - Hindi — लॉग आउट? / रद्द करें / लॉग आउट

---

## Motion & Feedback

- Dialog entrance: MD3 dialog motion — fade-in scrim 150ms + scale-from-95% + fade-in dialog surface 200ms ease-out (motion dial 3/10 — subtle).
- Dialog exit: reverse — scale-to-95% + fade-out 150ms.
- Log Out button press: MD3 ripple, 300ms ease-out, danger `#C62828` container with lightened onError overlay.
- Spinner (`logging_out`): 20dp circular indeterminate, 1.4s rotation cycle, respects `prefers-reduced-motion` (falls back to static static circle with pulsing opacity).
- Error text appearance (`error` state): fade-in 120ms with 4dp slide-down; NOT auto-dismissed.
- No snackbar / toast on this feature — errors stay inline.

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `SQLDelight`, `Store5`, `multiplatform-settings`
**Internal collaborators**: `SessionManager`, `NavigationManager`

Read paths:
- `SessionInfoDto` ← `SessionManager.getCurrentSession()` (from cached multiplatform-settings on cold start of settings screen; already resolved when this dialog opens).
- `pendingSyncCount` ← `SyncQueueRepository.pendingCount()` via Store5 stream over SQLDelight — determines whether the pre-flush step warrants a warn banner.

Write path (fired on `OnConfirmLogout`, single sequence):
1. `SyncQueueRepository.flushAll()` — returns `SyncFlushResult { flushedCount, failedCount, durationMs, status }` per `demo-data.yaml`.
2. `SessionManager.clearSession()` — releases in-memory session + emits session-cleared event.
3. `AuthTokenStore.clearAll()` (multiplatform-settings) — removes access + refresh tokens from disk.
4. `NavigationManager.navigateTo(login-signup) { popUpTo(root, inclusive = true) }` — no back-stack retention.

Offline behavior:
- No network dependency — logout is client-side only. Works fully offline.
- If the SyncQueueRepository flush fails because there is no connectivity, the ui.yaml contract STILL clears the session locally (queued ops persist in SQLDelight until next login), but surfaces the `error` state so the user is informed their offline work is deferred.

Failure surfaces (from `SettingsLogoutDialogState.errors`):
- `LogoutFailed` — generic wrapper for any of: flush failure with unsynced entries + user opted "keep session", `SessionManager` throw, or `AuthTokenStore` delete failure. Copy: "Failed to log out. Please try again."

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/settings-logout-dialog/ui.yaml` |
| API contract | `idea-layer/screens/settings-logout-dialog/api.yaml` (no server ops — client-side only) |
| Data flow | `idea-layer/screens/settings-logout-dialog/data-flow.yaml` |
| Demo data | `idea-layer/screens/settings-logout-dialog/demo-data.yaml` |
| Flow | `idea-layer/screens/settings-logout-dialog/flow.yaml` |
| Tests | `idea-layer/screens/settings-logout-dialog/tests.yaml` |
| Docs (lifecycle) | `idea-layer/screens/settings-logout-dialog/docs.yaml` |
| Preview HTML (idle) | `idea-layer/screens/settings-logout-dialog/preview/idle.html` |
| Preview HTML (logging_out) | `idea-layer/screens/settings-logout-dialog/preview/logging_out.html` |
| Preview HTML (error) | `idea-layer/screens/settings-logout-dialog/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/settings-logout-dialog/prompts/{idle,logging_out,error}.md` |
| Legacy Stitch mockup (2026-05-09, content only) | `idea-layer/mockups/settings-logout-dialog/stitch/01-settings-logout-dialog-content/{code.html,screen.png}` |
| Parent screen mockup | `idea-layer/mockups/authentication/` (dialog opens from settings) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from `ui.yaml` + `demo-data.yaml` + design-system tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The legacy Stitch artifact under `stitch/01-settings-logout-dialog-content/` (2026-05-09) covers only the `content` state (idle equivalent) and is stale relative to the current 3-state ui.yaml (adds `logging_out` + `error`); it will be regenerated on the next Stitch-enabled `/idea-feature-stitch --features settings-logout-dialog` pass.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features settings-logout-dialog
  ```
- Destructive-action safeguard: initial focus on Cancel, danger-tinted destructive CTA, generic body copy (no username echoed), and inline error surface (no auto-dismiss) — all consistent with the `regulated-industry` taste dial and the MifosSave "calm digital ledger" voice.
- Design conformance verifier: preview HTML mirrors the layouts above; any hand-edit to `ui.yaml#components` / `states` triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
