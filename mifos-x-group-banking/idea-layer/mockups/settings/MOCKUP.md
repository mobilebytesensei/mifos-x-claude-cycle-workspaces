# Settings — Mockup Specification

**Feature**: settings | **Route**: `/settings` | **Type**: settings
**Feature group**: platform-settings | **Flow**: settings-flow
**Generated from**: `screens/settings/ui.yaml`, `screens/settings/demo-data.yaml`, `screens/settings/preview/*.html` (3 states rendered 2026-07-17)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature settings`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for version strings
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar fill, section-header labels, radio selected dot, switch track (on), primary CTA styling
**Accent**: `#FF8F00` (`--accent-700`, amber) — not used on this screen (settings is admin-neutral)
**Success**: `#2E7D32` — snackbar "PIN updated successfully" fill
**Warning**: `#F57C00` (`--warning`) — reserved (unused here)
**Danger**: `#C62828` (`--danger`) — Logout button border + label, inline PIN-change error text, destructive dialog affordance
**Muted**: `#616161` (`--text-secondary`) on `#F5F5F5` — supporting text under toggle labels, disabled biometric row
**Background**: `#FFFFFF` canvas (list items, dialog) · `#FAFAFA` app (screen root) · `#F5F5F5` surfaceVariant (filled inputs, disabled state)
**Corner radius**: 12dp dialog · 8dp text-field · full-round switch thumb · 4dp radio · 8dp outlined button
**Elevation**: 0dp list rows (border-only per §component conventions) · 4dp dialog · 0dp Logout button (outlined)
**Min touch target**: 56dp list-item rows · 48dp radio row · 56dp Logout button · 48dp dialog fields

---

## Screen: Settings

### Entry
- From the **personal-dashboard profile overflow menu** → Settings (`trigger: profile_overflow_menu_settings_selected`); no nav-params
- Back navigation returns to personal-dashboard (pushed screen — TopAppBar back affordance)
- Deep-link `/settings` supported

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│  Settings                     [#2E7D32] │  top_bar — primary green fill, onPrimary text, 56dp
├─────────────────────────────────────────┤
│  LANGUAGE                                │  language_section_header · labelLarge, primary #2E7D32
│                                          │  padding 16dp / 16dp / 4dp
│  ○ 🇬🇧  English                          │  language_selector_group · radio-group, 48dp rows
│         English                          │  supporting text · bodySmall, onSurfaceVariant
│  ● 🇰🇪  Kiswahili           ← selected  │  selected = ENGLISH (bold ring + primary dot)
│         Kiswahili                        │  (demo shows ENGLISH selected — this row would flip)
│  ○ 🇫🇷  Français                         │
│         Français                         │
│  ○ 🇮🇳  हिन्दी                            │
│         हिन्दी                            │
│                                          │  → on_click OnLanguageSelected(language)
│                                          │     effect: persist_db (multiplatform-settings)
├─────────────────────────────────────────┤
│  APPEARANCE                              │  appearance_section_header · labelLarge, primary
│                                          │
│  ○ Light                                 │  theme_selector_group · radio-group, 48dp rows
│  ○ Dark                                  │
│  ● System Default          ← selected   │  demo default = SYSTEM
│                                          │  → on_click OnThemeSelected(theme)
│                                          │     effect: persist_db (multiplatform-settings)
├─────────────────────────────────────────┤
│  SECURITY                                │  security_section_header · labelLarge, primary
│                                          │
│  Biometric Unlock              [ OFF ]  │  biometric_toggle_row · list-item 56dp
│  Use fingerprint or face ID to log in    │  supporting · bodySmall, onSurfaceVariant
│                                          │  trailing = MD3 Switch, checked = false (demo)
│                                          │  → on_change OnBiometricToggled(enabled)
│                                          │     effect: persist_db (multiplatform-settings)
│  ┌─────────────────────────────────────┐│
│  │ Change PIN                       ›  ││  change_pin_row · list-item 56dp
│  │ Update your 4-digit security PIN    ││  trailing = chevron_right, onSurfaceVariant tint
│  └─────────────────────────────────────┘│  → on_click OnChangePinTapped
│                                          │     effect: transform_state (open dialog)
├─────────────────────────────────────────┤
│  NOTIFICATIONS                           │  notifications_section_header · labelLarge, primary
│                                          │
│  Push Notifications            [ ON  ]  │  notifications_toggle_row · list-item 56dp
│  Receive alerts for meetings,            │  supporting · bodySmall, onSurfaceVariant
│  repayments, and sync events             │  trailing = MD3 Switch, checked = true (demo)
│                                          │  → on_change OnNotificationsToggled(enabled)
│                                          │     effect: persist_db (multiplatform-settings)
├─────────────────────────────────────────┤
│  ABOUT                                   │  about_section_header · labelLarge, primary
│                                          │
│  App Version              1.0.0 (42)    │  app_version_row · list-item 48dp
│                                          │  trailing text · bodyMedium mono, onSurfaceVariant
├─────────────────────────────────────────┤
│                                          │
│  ┌─────────────────────────────────────┐│
│  │           Logout                    ││  logout_button · outlined, error border/text
│  │                                     ││  56dp height, full width, 16dp margin
│  └─────────────────────────────────────┘│  → on_click OnLogoutTapped
│                                          │     effect: emit_event ShowLogoutDialog
├─────────────────────────────────────────┤
│              ↕ scroll                    │  pushed screen (from personal-dashboard overflow
└─────────────────────────────────────────┘  menu); back returns to the member dashboard
```

### Demo Data (state: `content`, from `demo-data.yaml`)

Single seeded `AppSettingsDto` row for the signed-in user (userId `101`, a chairperson session):

| Field                      | Value             | UI effect                                              |
|----------------------------|-------------------|--------------------------------------------------------|
| `selectedLanguage`         | `ENGLISH`         | English radio selected; other 3 languages inactive     |
| `selectedTheme`            | `SYSTEM`          | "System Default" radio selected                        |
| `isBiometricEnabled`       | `false`           | Biometric switch OFF                                   |
| `isBiometricAvailable`     | `true`            | Biometric row ENABLED (not greyed out)                 |
| `isNotificationsEnabled`   | `true`            | Push Notifications switch ON                           |
| `appVersion`               | `"1.0.0"`         | Trailing text `1.0.0 (42)` in About row                |
| `buildNumber`              | `"42"`            | Bracketed build-number tail on the version row         |
| `lastPinChangedAt`         | `2026-04-01T10:00`| Not shown on screen (metadata for `change_pin` API)    |

- **Sibling `SettingsState`** mirrors the same defaults with UI transient flags: `isChangingPin=false`, `pinChangeError=null`, `pinChangeSuccess=false`, `isLoggingOut=false`.
- **`ChangePinRequest`** demo body: `{ password: "5678", repeatPassword: "5678" }` (no `userId` — Fineract resolves the caller from BasicAuth).
- **`ChangePinResponse`** happy path: `{ resourceId: 101 }` — triggers dialog close + success snackbar.
- All four language rows always visible regardless of the current selection (per FR-010 language coverage).

---

## States

The ui.yaml declares 3 `screen_state` members (`Content`, `ChangingPin`, `LoggingOut`) — each renders as a distinct HTML preview surface under `preview/`.

### `content` (see layout above)
All 6 sections visible in a single vertical scroll: Language · Appearance · Security · Notifications · About · Logout. Preferences are hydrated from `multiplatform-settings` key-value storage on entry; no network round-trip.

### `changing_pin`
The full settings surface remains visible underneath a MD3 dialog scrim; `change_pin_dialog` is the modal focus surface.

```
┌ Settings ─────────────────────────────────┐
│  ▒▒▒ background settings dimmed ▒▒▒       │  scrim · onSurface @ 32% opacity
│                                            │
│  ┌────────────────────────────────────┐   │
│  │ Change PIN                          │   │  dialog · surface #FFFFFF, radius 12dp, elev 4dp
│  │────────────────────────────────────│   │  title · titleLarge, onSurface
│  │                                    │   │
│  │ Current PIN                        │   │  current_pin_field · text-field, password mask
│  │ ┌────────────────────────────────┐│   │  input_type: password, keyboard: number, 48dp
│  │ │ • • • •                        ││   │
│  │ └────────────────────────────────┘│   │
│  │                                    │   │
│  │ New PIN (min 4 digits)             │   │  new_pin_field · text-field, password mask
│  │ ┌────────────────────────────────┐│   │  input_type: password, keyboard: number, 48dp
│  │ │ • • • •                        ││   │
│  │ └────────────────────────────────┘│   │
│  │                                    │   │
│  │ PIN change failed. Check your      │   │  pin_change_error_text · bodySmall, error #C62828
│  │ current PIN and try again.         │   │  visible_when: pinChangeError != null
│  │                                    │   │
│  │              [ Cancel ] [ Update ] │   │  cancel = text, confirm = filled primary
│  └────────────────────────────────────┘   │  → Update PIN OnSubmitPinChange
│                                            │     effect: call_api (ktor-client)
└────────────────────────────────────────────┘
```

- Both PIN fields use numeric keyboard + password-dot masking; supported by soft-keyboard OS input.
- **Cancel** → `OnDismissPinDialog` (effect: `transform_state`) — closes dialog, clears the two input fields.
- **Update PIN** → `OnSubmitPinChange(currentPin, newPin)` (effect: `call_api`) — PUT to Fineract `self/user/updatePassword` via ktor-client.
- Inline `pin_change_error_text` only renders when `pinChangeError != null` (validation or 400 response).
- On success: dialog dismisses, `pinChangeSuccess = true`, `ShowSnackbar("PIN updated successfully")` fires (snackbar transient, MD3 slide-up).
- On 401 `SessionExpired`: dialog dismisses, `ShowSnackbar("Session expired. Please log in again.")`, then `NavigateToLogin` event.

### `logging_out`
A trimmed frame — only the TopAppBar + the Logout button remain interactive; the button reflects loading via `loading_when: isLoggingOut`.

```
┌ Settings ─────────────────────────────────┐
│                                            │
│                                            │
│                                            │
│                                            │
│                                            │
│  ┌─────────────────────────────────────┐  │
│  │        ⟳  Logging out…              │  │  logout_button · loading spinner
│  └─────────────────────────────────────┘  │  outlined error border, disabled during transition
│                                            │
│                                            │
└────────────────────────────────────────────┘
```

- The rest of the settings body is hidden or dimmed (per ui.yaml `components: [top_bar, logout_button]`).
- Once the session clear completes: `NavigateToLogin` event fires and the login screen replaces the current route (nav-back stack cleared).
- No cancel affordance during this state — logout is intentionally irreversible once confirmed.

---

## Interaction Patterns

1. **Language radio tap** → `OnLanguageSelected(language)` (effect: `persist_db`, external: `multiplatform-settings`) → writes AppLanguage to key-value storage, re-applies locale live (Compose recomposes with new strings resource).
2. **Theme radio tap** → `OnThemeSelected(theme)` (effect: `persist_db`, external: `multiplatform-settings`) → writes AppTheme; Material theme switch is immediate, no restart.
3. **Biometric switch toggle** → `OnBiometricToggled(enabled)` (effect: `persist_db`, external: `multiplatform-settings`) → writes the toggle preference. Switch is disabled (unclickable, greyed) when `isBiometricAvailable == false`.
4. **Change PIN row tap** → `OnChangePinTapped` (effect: `transform_state`) → flips `isChangingPin = true`; VM state transition surfaces the dialog.
5. **PIN dialog Cancel** → `OnDismissPinDialog` (effect: `transform_state`) → sets `isChangingPin = false` and clears both PIN fields.
6. **PIN dialog Update PIN** → `OnSubmitPinChange(currentPin, newPin)` (effect: `call_api`, external: `ktor-client`) → PUT `/self/user/updatePassword`. 200 → close + success snackbar. 400 → inline error. 401 → clear session + `NavigateToLogin`.
7. **Notifications switch toggle** → `OnNotificationsToggled(enabled)` (effect: `persist_db`, external: `multiplatform-settings`) → writes push-notification preference; controls the alert channel used for meetings, repayments, sync events.
8. **Logout button tap** → `OnLogoutTapped` (effect: `emit_event ShowLogoutDialog`) → the host presents a confirmation dialog; on confirm the ViewModel transitions to `logging_out` and clears the session, then emits `NavigateToLogin`.

---

## Accessibility

- Every radio row exposes label + supporting text jointly (`accessibility_label` = "English, English", "Kiswahili, Kiswahili", …) for screen readers; the flag emoji is decorative (aria-hidden).
- Switch rows announce headline + trailing state ("Biometric Unlock, off", "Push Notifications, on"); when disabled, the announcement extends with "Biometric hardware not available on this device."
- Change PIN row announces "Change PIN, Update your 4-digit security PIN, button".
- Section headers use `role="heading"` semantic (aria-level 2 on web, `heading()` semantics on Compose).
- Logout button announces "Logout, button" with error-color styling supplemented by explicit text (never color-only).
- Min touch targets: 48dp on every radio row + dialog field; 56dp on toggle rows, Change PIN row, Logout button.
- Font stack respects system settings (Roboto / SF Pro) — dynamic type scaling up to 200% (§accessibility) preserves layout via Column-based sections (no fixed heights on text bodies).
- Locales covered on this screen: English (default), Swahili (`Mipangilio` / `Toka`), French (`Paramètres` / `Se Déconnecter`), Hindi (`सेटिंग्स` / `लॉग आउट`) — full FR-010 four-locale coverage in `i18n:` block.
- PIN masking uses password dots (`•`); character count and error copy is screen-reader announced.

---

## Motion & Feedback

- Radio selection: 150ms fill + dot transition (MD3 fast preset per §motion `fast:150ms`).
- Switch toggle: track color slide 200ms + thumb translation 200ms (MD3 base preset).
- Dialog present: MD3 scale-fade 200ms; dismiss: 150ms fade.
- Snackbar (`ShowSnackbar`): slide-up 300ms, auto-dismiss 4s, MD3 low elevation.
- Logout button pressed: MD3 outlined-button ripple 300ms; when `isLoggingOut = true`, the button label swaps to a MD3 CircularProgressIndicator + "Logging out…" copy.
- Respects `prefers-reduced-motion`: collapses all transitions to 0ms per §motion contract.
- No decorative animation — this is a functional admin surface (variance 3/10).

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `multiplatform-settings` (all local preference persistence), `ktor-client` (PIN change PUT only)
**Internal libs**: `SessionManager` (logout), `BiometricManager` (probe availability), `NavigationManager` (login redirect)

Read paths (offline-first, local-only):
- `selectedLanguage` ← `SettingsRepository.getLanguage()` via multiplatform-settings key `pref.language`
- `selectedTheme` ← `SettingsRepository.getTheme()` via key `pref.theme`
- `isBiometricEnabled` ← key `pref.biometric.enabled` (default `false`)
- `isNotificationsEnabled` ← key `pref.notifications.enabled` (default `true`)
- `isBiometricAvailable` ← `BiometricManager.isHardwareAvailable()` (platform probe on entry; `expect/actual`)
- `appVersion`, `buildNumber` ← `BuildConfig` / `Bundle.infoDictionary` (platform bind via `expect/actual`)

Write paths:
- `OnLanguageSelected` → `SettingsRepository.setLanguage(lang)` → multiplatform-settings write + `LocaleController.apply(lang)`
- `OnThemeSelected` → `SettingsRepository.setTheme(theme)` → multiplatform-settings write + `ThemeController.apply(theme)`
- `OnBiometricToggled` → `SettingsRepository.setBiometricEnabled(enabled)` → multiplatform-settings write
- `OnNotificationsToggled` → `SettingsRepository.setNotificationsEnabled(enabled)` → multiplatform-settings write + push subscription resubscribe/unsubscribe hook
- `OnSubmitPinChange` → `SettingsRepository.changePin(currentPin, newPin)` → **only** network write: PUT `/self/user/updatePassword` via ktor-client, BasicAuth on caller session

Session path:
- `OnLogoutTapped` → emits `ShowLogoutDialog` event to the UI host; on confirmed logout the VM sets `isLoggingOut = true`, calls `SessionManager.clear()` (drops BasicAuth token, purges Store5 caches, revokes push subscription), then emits `NavigateToLogin`.

Offline behavior: every screen-local preference is available offline (all local); the PIN change dialog surfaces a "No internet connection" copy via `pin_change_error_text` when `NetworkMonitor.isOffline == true` at submit time — no request is dispatched. The rest of the screen never blocks on the network.

Screen states vs data flow: `Content` is the steady state; `ChangingPin` overlays the same underlying `SettingsState` (no source-of-truth swap); `LoggingOut` is a transient purge state (all reads suspended; UI switches to a barebones frame).

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/settings/ui.yaml` |
| API contract | `idea-layer/screens/settings/api.yaml` |
| Data flow | `idea-layer/screens/settings/data-flow.yaml` |
| Demo data | `idea-layer/screens/settings/demo-data.yaml` |
| Flow | `idea-layer/screens/settings/flow.yaml` |
| Tests | `idea-layer/screens/settings/tests.yaml` |
| Preview HTML (content) | `idea-layer/screens/settings/preview/content.html` |
| Preview HTML (changing_pin) | `idea-layer/screens/settings/preview/changing_pin.html` |
| Preview HTML (logging_out) | `idea-layer/screens/settings/preview/logging_out.html` |
| Stitch prompts (per state) | `idea-layer/screens/settings/prompts/{content,changing_pin,logging_out}.md` |
| Feature-group mockup | `idea-layer/mockups/platform-settings/MOCKUP.md` (Settings section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (3/3 states rendered 2026-07-17) + ui.yaml + demo-data.yaml + `design-system/DESIGN.md` tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The `preview/` HTML already reflects the 3-state ui.yaml (`content`, `changing_pin`, `logging_out`) and the demo `AppSettingsDto` values — no drift observed at generation time.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features settings
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to `ui.yaml#components`/`states` triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
- FR-010 language coverage is intentional and exhaustive here — the four-radio Language section is the source of truth for the app-wide locale switch; every other feature reads from `SettingsRepository.getLanguage()`.
- Logout is deliberately gated behind a confirmation dialog (event `ShowLogoutDialog`) hosted by the outer settings navigator — the button itself only emits the event; the actual session clear is a two-step user-mediated affordance to avoid accidental sign-out in the field.
