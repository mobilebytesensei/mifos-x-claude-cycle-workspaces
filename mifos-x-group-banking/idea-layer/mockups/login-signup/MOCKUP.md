# Login / Signup — Mockup Spec

## Design Language

CommonPurse uses Material Design 3 with a VSLA-inspired brand palette designed for low-literacy rural users in East Africa. All touch targets are minimum 48dp. Typography uses the system stack (Roboto on Android / SF Pro on iOS) at comfortable density with an emphasis on clarity for outdoor viewing. Login/Signup follows the app's `minimalist-ui` family (variance 3/10, motion 3/10, density 7/10) — grid-aligned, predictable, subtle transitions. As the app's entry surface it also carries the brand mark, so it renders with slightly more vertical breathing room than in-app screens.

**Brand colours (from `design-system/DESIGN.md`)**:
- Primary 700: #2E7D32 (base VSLA-green — Sign In / Create Account CTAs, tab indicator)
- Primary 900: #1B5E20 (pressed CTA states)
- Primary 500: #43A047 (hover / focus highlight)
- Primary 100: #C8E6C9 (biometric icon-button hover background, chip fills)
- Accent 700: #FF8F00 (unused on this surface — reserved for pooled-fund emphasis inside the app)
- Success: #2E7D32 (form-field focused border)
- Warning: #F57C00 (offline / low-bandwidth banner if surfaced)
- Danger: #C62828 (error banner background base, invalid-credential inline errors)
- Info: #1565C0 (informational hints)
- Bg canvas: #FFFFFF (surface, card containers)
- Bg subtle: #FAFAFA (screen background)
- Bg muted: #F5F5F5 (filled/disabled input backgrounds)
- Border subtle: #EEEEEE (dividers, `divider_or` line)
- Border default: #E0E0E0 (outlined field borders at rest)
- Text primary: #212121 (form values, headings)
- Text secondary: #616161 (labels, helper text)
- Text disabled: #9E9E9E (unselected tab label, forgot-password link at rest)

**Typography**: Roboto / SF Pro. displaySmall=36sp, headlineMedium=28sp, headlineSmall=24sp, titleLarge=22sp, titleMedium=18sp, bodyLarge=16sp, bodyMedium=14sp, labelLarge=14sp, labelMedium=12sp. Auth title "Welcome to MifosX" renders in headlineMedium (28sp) centered; tab labels are labelLarge semibold; helper / validation text is bodyMedium.

**Shapes**: cornerRadius sm=8dp (chips, small buttons, error banner), md=12dp (input fields, cards), lg=16dp (biometric icon-button surround, illustration frame), full=9999dp (filled Sign In / Create Account CTAs, tab pills).

**Elevation**: The auth screen is intentionally flat — logo/title/tabs at 0dp, input fields outlined at 0dp, filled CTAs at 0dp. Only the error_banner uses 0dp tonal fill (no shadow) so it feels informative rather than alarming.

---

## Screen-by-Screen

### LoginSignupScreen (single-screen tabbed auth host)

**Layout**: Scaffold with no top bar; scrollable centered Column body. Background: `#FAFAFA`. Content vertically centered on tall screens, top-aligned with 32dp safe padding when the keyboard is up. Same host renders all four `screen_state` members (`Content`, `Loading`, `Error`, `ZeroGroups`) — visibility of individual components is driven by `mode` (Login vs Signup) plus reactive fields (`isBiometricAvailable`, `isSubmitting`, `error`).

Route: `/auth` — mounted at the app root, reached from `app_launch:unauthenticated_start` and `any_screen:session_expired`.

**States** (mapped 1:1 to `ui.yaml#states`):
- `content` (initial_state, mode-adaptive) — form visible; Login mode renders email/password + biometric affordance + Forgot Password link + Sign In CTA; Signup mode renders name/email/password + Create Account CTA
- `loading` (`isSubmitting == true`) — form fields disabled at 40% opacity; the mode's CTA (Sign In or Create Account) shows a centered spinner in place of its label; tab toggle disabled; biometric icon-button hidden
- `error` (`error != null`) — `error_banner` visible above the form; form re-enabled and prefilled for retry; validation errors additionally surface as inline field helpers for `WeakPassword` / field-level errors
- `zero_groups` (post-success, `groupMemberships.isEmpty()`) — auth chrome swapped for onboarding: illustration + "You're all set!" + primary "Create Your First Group" and outlined "Join with Invite Code" CTAs; no mode toggle or form fields visible in this state

**Components** (grounded in `ui.yaml#components` — every `id` here maps to a real entry):

| Component | Type | Style Summary | Interaction |
|-----------|------|---------------|-------------|
| auth_header_logo | Image | Asset `ic_mifos_logo` 72dp × 72dp, alignment center, top_padding 32dp. Accessibility label "Mifos X logo". | Non-interactive |
| auth_title | Text | "Welcome to MifosX" — headlineMedium (28sp), color onSurface (#212121), alignment center, top_padding 16dp. | Non-interactive |
| mode_toggle_tabs | TabRow | Two pills [Sign In, Sign Up] full-width row 48dp, background surface (#FFFFFF), corner_radius md (12dp), border_subtle divider under row. Selected label color primary (#2E7D32), unselected onSurfaceVariant (#616161). Indicator 3dp bar primary (#2E7D32) under the active tab. Selected reflects `state.mode` (AuthMode.Login default). | Tap → OnModeToggle(mode) — flips `state.mode`, clears name/emailPhone/password + validationErrors + error so the newly-shown tab renders clean (per `action_contract.effect: transform_state`) |
| signup_name_field | OutlinedTextField | Visible when `mode == AuthMode.Signup`. Label "Full Name", placeholder "e.g. Grace Wanjiku", value bound to `state.name`, keyboard text, IME next, max_length 80, corner_radius md (12dp), min_height 56dp, margin_horizontal 24dp, top_padding 16dp. Validation `{min_length: 2, required: true, error_key: error_name_required}`; error border 2dp danger (#C62828) + helper text "Full name is required." bodyMedium danger. | Type → OnNameChange(value) — updates `state.name` and clears its validationErrors entry; focus-out runs min-length-2 check |
| email_phone_field | OutlinedTextField | Shared across login/signup forms. Label "Email or Phone", placeholder "email@example.com or +254700000000", value bound to `state.emailPhone`, keyboard email, IME next, max_length 100, corner_radius md (12dp), min_height 56dp, margin_horizontal 24dp, top_padding 8dp. Validation `{required: true, pattern: email_or_e164_phone, error_key: error_email_phone_invalid}`; error border + helper "Enter a valid email address or phone number." | Type → OnEmailPhoneChange(value) — updates `state.emailPhone`; focus-out validates pattern |
| password_field | OutlinedTextField (variant: password) | Shared. Label "Password", placeholder adapts by mode ("Your password" login / "Minimum 8 characters" signup), value bound to `state.password`, masked with trailing eye toggle, max_length 64, corner_radius md (12dp), min_height 56dp, margin_horizontal 24dp, top_padding 8dp. Validation `{required: true, min_length: 8, error_key: error_password_weak}`; error border + helper "Password must be at least 8 characters." Value held in memory only — never logged, never cached. | Type → OnPasswordChange(value) — updates `state.password`; signup-mode focus-out runs 8-char strength check |
| forgot_password_link | TextButton | Visible when `mode == AuthMode.Login`. Label "Forgot password?" labelMedium (12sp), text_color primary (#2E7D32), alignment end, top_padding 4dp, margin_horizontal 24dp. Min touch target 48dp with 12dp side padding. | Tap → OnForgotPassword — emits `ShowSnackbar("Reset your password via the web portal or your group organizer.")`; no state mutation, no network call (MVP has no in-app reset endpoint) |
| login_button | FilledButton | Visible when `mode == AuthMode.Login`. Label "Sign In", full_width (minus 24dp horizontal margin), min_height 56dp, corner_radius full (9999dp), background primary (#2E7D32), text_color onPrimary (#FFFFFF), top_padding 24dp. Loading state (`isSubmitting == true`): 24dp CircularProgressIndicator onPrimary replaces label; button disabled. Disabled state (offline + `error.type == BiometricFailed` transient): background primary at 40% opacity. | Tap → OnLoginTap → POST `/companion/auth/login` via core/network; on success persists sessionToken to encrypted core/session SessionStore and routes on groupMemberships (non-empty → personal-dashboard / group-list, empty → ZeroGroups); 401 sets `state.error = InvalidCredentials` |
| signup_button | FilledButton | Visible when `mode == AuthMode.Signup`. Label "Create Account", same shape as login_button. Loading state identical. | Tap → OnSignupTap → POST `/companion/auth/self-register` via core/network — atomically creates companion user + linked Fineract client; persists sessionToken; empty groupMemberships always routes to ZeroGroups; 409 surfaces `error_account_exists` |
| biometric_unlock_button | IconButton | Visible when `isBiometricAvailable == true && mode == AuthMode.Login`. Icon `fingerprint` 48dp, icon_tint primary (#2E7D32), alignment center, top_padding 12dp, wrapped in a 64dp circular tap surface with primaryContainer (#C8E6C9) hover fill. Accessibility label "Sign in with biometrics". | Tap → OnBiometricUnlock → platform biometric prompt via core/biometric → on hardware success calls GET `/companion/auth/me` via core/network → refreshes profile + groupMemberships → routes on membership count (non-empty → personal-dashboard, empty → ZeroGroups). Offline biometric surfaces `error_biometric_failed`. |
| divider_or | LabeledDivider | Visible when `isBiometricAvailable == true && mode == AuthMode.Login`. Horizontal 1dp line border_subtle (#EEEEEE) with centered "or" chip — labelSmall (12sp) onSurfaceVariant (#616161) on background surface pill. margin_horizontal 24dp, top_padding 16dp. Sits between login_button and biometric_unlock_button. | Non-interactive |
| error_banner | Banner | Visible when `error != null`. Icon `error_outline` 20dp onErrorContainer, message `{{error.localizedMessage}}` bodyMedium onErrorContainer, background errorContainer (danger-tinted #FFDAD6), corner_radius 8dp, padding 12dp, margin_horizontal 24dp, top_padding 16dp. live_region assertive so it's announced immediately. Trailing "Retry" TextButton labelLarge onErrorContainer bold — only rendered when `error.retry == true` (InvalidCredentials, Network, Server, BiometricFailed). | "Retry" tap → re-fires the last submit action (OnLoginTap / OnSignupTap / OnBiometricUnlock) based on `state.mode` + `isBiometricAvailable` |
| zero_groups_illustration | Image | Zero-groups state only. Asset `ic_empty_groups` 120dp × 120dp, alignment center, top_padding 48dp. Accessibility label "Empty groups illustration". | Non-interactive |
| zero_groups_title | Text | Zero-groups state only. "You're all set!" headlineSmall (24sp) onSurface (#212121), alignment center, top_padding 16dp. | Non-interactive |
| zero_groups_body | Text | Zero-groups state only. "You don't belong to any savings group yet. Create your first group or join one with an invite code." bodyMedium onSurfaceVariant (#616161), alignment center, horizontal_padding 24dp, top_padding 8dp. | Non-interactive |
| create_group_button | FilledButton | Zero-groups state only. Label "Create Your First Group", full_width (minus 24dp horizontal margin), min_height 56dp, corner_radius full (9999dp), background primary (#2E7D32), text_color onPrimary (#FFFFFF), top_padding 32dp. | Tap → OnCreateGroupTap → NavController navigates to `group-type-picker`; carries session identity; no write at tap time |
| join_with_code_button | OutlinedButton | Zero-groups state only. Label "Join with Invite Code", full_width, min_height 56dp, corner_radius full (9999dp), border 1dp primary (#2E7D32), text_color primary, background surface (#FFFFFF), top_padding 12dp. | Tap → OnJoinWithCodeTap → NavController navigates to `join-with-code`; membership write happens on that screen's submit |

**Layout structure (Content, Login mode, biometric available)**:

```
[Status bar — light content over #FAFAFA]
[32dp top safe padding]
[ic_mifos_logo — 72dp × 72dp, centered]
[16dp gap]
["Welcome to MifosX" — headlineMedium onSurface, centered]
[32dp gap]
[mode_toggle_tabs — [ Sign In · Sign Up ], Sign In active, 48dp row]
[24dp gap]
[email_phone_field — "grace.wanjiku@example.com" prefilled from demo]
[8dp gap]
[password_field — masked "•••••••••••••", trailing eye]
[4dp gap]
[forgot_password_link — right-aligned "Forgot password?"]
[24dp gap]
[login_button — "Sign In" full-width filled primary pill]
[16dp gap]
[divider_or — "─── or ───"]
[12dp gap]
[biometric_unlock_button — fingerprint 48dp centered, primary tint]
[bottom safe area]
```

**Layout structure (Content, Signup mode)**:

```
[32dp top safe padding]
[ic_mifos_logo]
[16dp gap]
["Welcome to MifosX"]
[32dp gap]
[mode_toggle_tabs — Sign Up active]
[24dp gap]
[signup_name_field — placeholder "e.g. Grace Wanjiku"]
[8dp gap]
[email_phone_field — placeholder "email@example.com or +254700000000"]
[8dp gap]
[password_field — placeholder "Minimum 8 characters"]
[24dp gap]
[signup_button — "Create Account" full-width filled primary pill]
[bottom safe area]
```

**Layout structure (ZeroGroups)**:

```
[48dp top gap]
[ic_empty_groups — 120dp × 120dp centered]
[16dp gap]
["You're all set!" — headlineSmall centered]
[8dp gap]
["You don't belong to any savings group yet…" — bodyMedium centered, 24dp horizontal padding]
[32dp gap]
[create_group_button — "Create Your First Group" filled primary pill]
[12dp gap]
[join_with_code_button — "Join with Invite Code" outlined primary pill]
[bottom safe area]
```

---

## Interaction Patterns

**Mode toggle (tab flip)**:
1. User taps the currently-inactive tab in `mode_toggle_tabs`.
2. OnModeToggle(mode) dispatched — `state.mode` flips, `state.name` / `state.emailPhone` / `state.password` and `validationErrors` + `error` are cleared per the `action_contract.effect: transform_state` contract, so the newly-shown tab is clean.
3. Component visibility recomposes: signup_name_field animates in/out (fade+height, motion=short_3=150ms). login_button ↔ signup_button cross-fade (150ms). forgot_password_link + biometric_unlock_button + divider_or gate on the login predicate and animate accordingly.
4. Tab indicator (3dp bar) slides between pill positions (standard easing, medium_1=250ms).

**Field entry (name / emailPhone / password)**:
1. User types; OnNameChange / OnEmailPhoneChange / OnPasswordChange dispatched per keystroke.
2. Corresponding `state` field updates; any prior `validationErrors` entry for that field is cleared so the danger border retracts immediately as the user starts typing.
3. On focus-out, the field-level validation runs: name min_length 2, email/phone `email_or_e164_phone` pattern, password min_length 8 (signup only). Failures set `validationErrors[field] = error_key` and repaint the field with a 2dp danger border + bodyMedium helper text.

**Forgot password**:
1. User taps `forgot_password_link` (login mode only).
2. OnForgotPassword dispatched → `ShowSnackbar("Reset your password via the web portal or your group organizer.")` event emitted.
3. No state mutation, no network call. Bottom snackbar surface auto-dismisses after 4s.

**Sign In (OnLoginTap → success)**:
1. User taps `login_button`.
2. Client-side validation runs on emailPhone + password; any failure sets `validationErrors` and blocks the request (no network call).
3. On pass: `isSubmitting = true` → screen_state = `Loading`. login_button label cross-fades to spinner (150ms); fields dim to 40% opacity and become non-interactive; biometric_unlock_button hides.
4. POST `/companion/auth/login` via core/network with `{emailPhone, password}` body. Demo response for Grace Wanjiku: `userId=usr_01J5KT2N8XQWRP7M3B4C6DE9FA`, sessionToken (JWT-shaped), `groupMemberships=[Mwangaza Women's Group (TREASURER), Jua Kali Savings Circle (MEMBER)]`.
5. sessionToken persisted to encrypted core/session SessionStore; groupMemberships cache hydrated.
6. Routing:
   - `groupMemberships.size == 1` → `NavigateToPersonalDashboard` (member/treasurer single-group happy path).
   - `groupMemberships.size > 1` → `NavigateToGroupList` (multi-group organizer).
   - `groupMemberships.isEmpty()` → screen_state = `ZeroGroups` (in-place swap — no navigation; the same host renders zero_groups_* components).

**Sign In (OnLoginTap → error paths)**:
- 401 InvalidCredentials → `state.error = InvalidCredentials`, screen_state = `Error`. error_banner shows "Incorrect email or password. Please try again." with Retry.
- Network offline → `state.error = Network`, banner "No internet connection. Please try again." with Retry.
- 5xx Server → `state.error = Server`, banner "Something went wrong on our end. Please retry." with Retry.
- Any error re-enables the form for edit; the last-entered emailPhone is retained; the password is retained too (not cleared) so a typo can be corrected without retyping.

**Create Account (OnSignupTap)**:
1. Client-side validation runs on name (min 2), emailPhone (pattern), password (min 8).
2. On pass: `isSubmitting = true` → screen_state = `Loading`; signup_button spinner replaces label.
3. POST `/companion/auth/self-register` via core/network with `{name, emailPhone, password}`. Backend atomically creates the companion user AND the linked Fineract client in one transaction.
4. On success: sessionToken persisted; `groupMemberships` always empty for a fresh registration → screen_state = `ZeroGroups` (in-place swap, no navigation event).
5. On 409 AccountExists → `state.error = AccountExists`, banner "An account with this email or phone already exists. Please sign in." Retry=false — user must switch to Sign In tab; the tab toggle remains available (not disabled) even in error state.

**Biometric unlock**:
1. On screen mount, if a stored sessionToken exists AND platform biometric hardware is available AND enrolled, ViewModel sets `isBiometricAvailable = true` → biometric_unlock_button + divider_or render.
2. On mount only (not on every recomposition), if the stored session is unexpired the ViewModel dispatches `PromptBiometric` — the system prompt appears automatically without a tap. If the user cancels the prompt, they fall back to typed credentials on the same screen.
3. On tap: OnBiometricUnlock → invokes platform biometric prompt via core/biometric → on hardware success calls GET `/companion/auth/me` via core/network → refreshes profile + groupMemberships → routes on membership count.
4. On hardware failure or offline: `state.error = BiometricFailed`, banner "Biometric authentication failed. Please sign in manually." + Retry (retry=true — user may try biometric again once network returns) OR user falls through to the password field.

**ZeroGroups → onward**:
1. In the `ZeroGroups` state, only the illustration + title + body + two CTAs render — the tab toggle and form fields are unmounted. There is no back affordance (session established; user cannot un-register).
2. Tap `create_group_button` → OnCreateGroupTap → NavController navigates to `group-type-picker` carrying session identity via the SessionStore.
3. Tap `join_with_code_button` → OnJoinWithCodeTap → NavController navigates to `join-with-code`. The membership write happens on the submit action in that screen, not here.

**Session-expired re-entry**:
1. When any in-app screen dispatches a request that returns 401, the app pops the back stack to `/auth` and remounts LoginSignupScreen with `mode = AuthMode.Login`, `state.emailPhone` prefilled from the last-known session, and a one-shot snackbar "Your session has expired. Please sign in again."
2. If `isBiometricAvailable == true`, PromptBiometric fires automatically to enable a one-tap resume.

---

## Accessibility

**WCAG AA compliance**:
- Primary (#2E7D32) on background subtle (#FAFAFA): 5.83:1 — passes AA normal text
- onPrimary (#FFFFFF) on primary (#2E7D32): 13.5:1 — passes AAA (CTA labels)
- Danger (#C62828) on errorContainer (#FFDAD6): 6.9:1 — passes AA (error banner text)
- Text primary (#212121) on background (#FAFAFA): 15.4:1 — passes AAA (auth title, form values)
- Text secondary (#616161) on background (#FAFAFA): 5.9:1 — passes AA (labels, helper text)
- Primary (#2E7D32) on background (#FFFFFF, biometric icon-button hover): 5.98:1 — passes AA

**Touch targets**: All interactive elements minimum 48dp. Filled CTAs (login_button, signup_button, create_group_button, join_with_code_button) are 56dp for confidence. `forgot_password_link` is a labelMedium TextButton with 12dp side padding so the labelled tap area meets 48dp. `biometric_unlock_button` uses a 48dp icon inside a 64dp tap surface for high-frequency use.

**Content descriptions & live regions**:
- `auth_header_logo` accessibility_label: "Mifos X logo".
- `auth_title` announced as a heading (Compose semantics `heading()`).
- `mode_toggle_tabs`: each tab announced as "Sign In tab" / "Sign Up tab", selection state "selected" / "not selected".
- Every text field: label read as the accessibility label; validation errors read as a live_region assertive on populate; character counter announced as label state change, not each keystroke.
- `forgot_password_link` accessibility_label: "Forgot password? Opens password reset guidance." Snackbar body read as live_region polite on tap.
- `login_button` / `signup_button`: label announced. Loading state announces "Signing you in, please wait." / "Creating your account, please wait." once when `isSubmitting` becomes true (not on every recomposition).
- `biometric_unlock_button` accessibility_label: "Sign in with biometrics". Automatically-fired system biometric prompt is announced by the OS.
- `error_banner`: live_region assertive; announced immediately on error. Message text is the resolved localizedMessage; Retry button announced as "Retry, button" following the message.
- ZeroGroups state: `zero_groups_illustration` accessibility_label "Empty groups illustration"; title announced as heading; body announced as bodyMedium; CTAs announced sequentially.

**Focus order (Content — Login mode, biometric available)**: auth_title → mode_toggle_tabs (Sign In) → mode_toggle_tabs (Sign Up) → email_phone_field → password_field → forgot_password_link → login_button → biometric_unlock_button. `divider_or` skipped by TalkBack (`hideFromAccessibility = true`).

**Focus order (Content — Signup mode)**: auth_title → mode_toggle_tabs (Sign In) → mode_toggle_tabs (Sign Up) → signup_name_field → email_phone_field → password_field → signup_button.

**Focus order (Error state)**: error_banner (announced first, then focusable) → Retry (if visible) → back to the field/CTA sequence for the current mode.

**Focus order (ZeroGroups)**: zero_groups_title → zero_groups_body → create_group_button → join_with_code_button.

**Keyboard / IME behaviour**: Login mode — email_phone_field IME `next` → password_field IME `done`; `done` triggers OnLoginTap (submits) only when the touch focus order originated from typing (never when the field is refocused by TalkBack navigation, to prevent an unintended submit). Signup mode — signup_name_field IME `next` → email_phone_field IME `next` → password_field IME `done`; `done` triggers OnSignupTap under the same rule.

**Screen reader mode**: When TalkBack / VoiceOver active, IME `done` does NOT auto-submit — the user must explicitly tap login_button / signup_button. The mode-toggle animation is replaced by an instant swap. The biometric prompt still fires on mount (it's an OS-level event and self-announces). The Loading state announces the "Signing you in…" / "Creating your account…" line once; no repeat on progress ticks. The offline error banner does not repeat if the user retries the same failing request within 5s.

---

## Empty / Error / Loading States

**Empty (first mount, Login mode default)**: All form fields render at their `default` values from `state_model` — name/emailPhone/password all empty. The Sign In CTA is enabled at all times — validation runs on tap; empty required fields produce inline errors rather than a globally-disabled CTA. This mirrors CommonPurse's "trust the user, guide with errors" pattern used across the app. `isBiometricAvailable` starts false; the ViewModel probes hardware + stored-session on mount and, if both hit, sets it true and the biometric affordance + divider_or animate in (fade+height, 150ms).

**Loading (submitting state)**: The mode's CTA (Sign In or Create Account) shows a 24dp CircularProgressIndicator onPrimary in place of its label; button disabled. All form fields disabled at 40% opacity — they remain visible so the user can see what's being sent but cannot mutate. Tab toggle disabled. `biometric_unlock_button` hides (not just disables) to prevent a double-submit path. No overlaid scrim. Duration expectation: <2s online, <500ms local biometric round-trip. If the request takes >4s (arbitrary threshold from RESEARCH.md low-bandwidth budget), a bodyMedium helper "Still working… we'll retry automatically if this fails." fades in below the CTA (does not spawn a new banner).

**Error (post-submit)**: `error_banner` appears above the form (top_padding 16dp from mode_toggle_tabs). Message pulls from `error.localizedMessage`. Retry button rendered only when `error.retry == true` per `LoginSignupError` types (InvalidCredentials, Network, Server, BiometricFailed retry=true; AccountExists, WeakPassword retry=false). When retry=false, the user is expected to switch tab or edit the fields — the banner also shows a bodyMedium hint under the message (e.g. "Please tap Sign In instead." for AccountExists). Form re-enabled with prior values retained. First-focus goes to the banner so the assistive tech announcement is heard, then TalkBack advances back into the fields.

**ZeroGroups**: The entire auth chrome (logo, title, tabs, form fields, biometric affordance) unmounts and is replaced by the four ZeroGroups components (illustration, title, body, two CTAs). No back affordance — the user is authenticated; the only paths forward are Create Group or Join with Invite Code. If the user backgrounds the app in this state and returns, the app comes back into the same ZeroGroups state (session persists), NOT the Login form.

**Session expired re-mount**: On re-mount from a 401 elsewhere in the app, the screen renders in `Content` / Login mode with:
- `emailPhone` prefilled from the last known session (never the password)
- A one-shot Snackbar (info palette) "Your session has expired. Please sign in again." — 5s duration, not sticky.
- If `isBiometricAvailable == true`, PromptBiometric fires automatically 300ms after mount to enable one-tap resume.

---

## Notes for Implementation

- **Single ViewModel host** — LoginSignupViewModel is the sole `di` boundary. It aggregates AuthRepository (network call), BiometricManager (platform prompt), SessionStore (encrypted persistence), NetworkMonitor (offline gate) — see `state_model.LoginSignupViewModel.di`.
- **Companion self-registration atomicity** — Signup calls a single `/companion/auth/self-register` endpoint that atomically creates the companion user + linked Fineract client in one backend transaction. The client MUST NOT hand-roll the Fineract self-service register call; the presence of a `AuthRepository.selfRegister(request): AuthResponse` method routed through `core/network` is the contract.
- **Session persistence** — sessionToken persisted to `core/session` SessionStore backed by platform secure storage (Android KeyStore / iOS Keychain via `com.russhwolf.settings.Settings` KeychainSettings). Token never logged; never emitted to the Kermit tag; never included in analytics events.
- **Password handling** — held in `state.password` only for the lifetime of the form; on successful login/signup the field is cleared as `LoginSignupViewModel` re-enters the `content` state or unmounts. On tab flip, cleared per `OnModeToggle.action_contract`. On error, retained per user-friendliness above.
- **Biometric gating** — `BiometricManager.isAvailable()` is called in `LaunchedEffect` on mount; response drives `isBiometricAvailable`. On Android, "available" means hardware present + enrolled biometrics + not locked out. On iOS, means Face ID / Touch ID hardware present + policy authorised. Web/desktop platforms always report false — the biometric_unlock_button + divider_or never render there.
- **Routing decision** — routing between `NavigateToPersonalDashboard` / `NavigateToGroupList` / in-place ZeroGroups swap happens in the ViewModel post-success handler, driven entirely by `groupMemberships.size`. No screen-level branching.
- **Companion routes touched** — POST `/companion/auth/login`, POST `/companion/auth/self-register`, GET `/companion/auth/me`. All three declared in `api.yaml`.
- **Analytics** (legacy_metadata.analytics — see docs.yaml):
  - screen_view: `login_signup_viewed`
  - tab flip: `auth_mode_toggled { mode: "login" | "signup" }`
  - Sign In tap: `login_attempted { has_biometric: Boolean }`
  - Create Account tap: `signup_attempted`
  - biometric tap: `biometric_unlock_attempted`
  - auth error: `auth_error { type: String, retry: Boolean }` — `type` is the LoginSignupError enum name, never the raw HTTP body
  - success login: `login_succeeded { group_count: Int }`
  - success signup: `signup_succeeded`
  - ZeroGroups seen: `zero_groups_shown { path: "signup" | "login" }`
  - Zero-groups CTA tap: `zero_groups_action_tapped { action: "create" | "join" }`
- **Route** — `/auth` — mounted at the NavHost root under an unauthenticated nav graph. No deep-link surface (the app treats deep links to protected routes as an entry pointer that redirects here on 401).
- **Icon set** — Fingerprint (biometric_unlock_button), error_outline (error_banner). Rendered via `androidx.compose.material.icons` on Android + shared Compose Multiplatform Icons on iOS/desktop for parity.

---

## Related Screens

- **personal-dashboard** — Success destination when `groupMemberships.size == 1` (single-group happy path).
- **group-list** — Success destination when `groupMemberships.size > 1`.
- **group-type-picker** — ZeroGroups → OnCreateGroupTap destination.
- **join-with-code** — ZeroGroups → OnJoinWithCodeTap destination.
- **member-onboarding** — Downstream of ZeroGroups → group-type-picker → group-create; this is where the first-group organizer completes the onboarding sequence.
