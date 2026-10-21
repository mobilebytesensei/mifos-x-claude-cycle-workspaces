# MOCKUP — Login

| Field   | Value  |
|---------|--------|
| Feature | login  |
| Flavor  | shared |

---

## Screen Layout

The login screen is a single scrollable column on a `surfaceContainerLow` background, padded `spacing.lg` (24 dp) on all sides. The hierarchy from top to bottom is:

1. Mifos X logo (80×80 dp, centered)
2. "Welcome Back" headline
3. "Sign in to your Mifos X account" subtitle
4. Username text field
5. Password text field (with visibility toggle)
6. Remember-me row (checkbox + label)
7. Error banner (conditional — visible only in `error` state)
8. "Sign In" filled CTA button
9. OR divider row (line / text / line)
10. "Sign in with OBP Account" outlined button
11. OAuth hint text
12. Bottom divider
13. "Forgot Password?" link

---

## Components

### login_header_logo
- **Description:** Mifos X brand mark asset `mifos_logo` scaled to 80×80 dp
- **Position:** Top-center of scroll area, padding-bottom = `spacing.md` (16 dp)
- **Style tokens:** tint `primary`, alignment=center

### login_header_title
- **Description:** Static text "Welcome Back"
- **Position:** Below logo
- **Style tokens:** `headlineLarge` (32 sp, weight 400, Roboto), color `primary`, alignment=center, padding-bottom `spacing.xs` (4 dp)

### login_header_subtitle
- **Description:** Static text "Sign in to your Mifos X account"
- **Style tokens:** `bodyMedium` (14 sp, Roboto), color `onSurfaceVariant`, alignment=center, padding-bottom `spacing.xl` (32 dp)

### login_username_input
- **Description:** Outlined text field, label "Username", placeholder "Enter your username"
- **Position:** Below subtitle
- **Style tokens:** background `surfaceContainerLowest`, border `outline` (rest) / `primary` (focused, `border.focus`), `bodyLarge`, radius `radius.sm`, padding `spacing.md`
- **Behavior:** keyboard_type=text, ime_action=next (tab focus to password field)

### login_password_input
- **Description:** Outlined password field, label "Password", placeholder "Enter your password"; trailing visibility toggle icon
- **Style tokens:** Same as username input; trailing icon `visibility_toggle` (`icon.md`, `onSurfaceVariant`)
- **Behavior:** keyboard_type=text, ime_action=done; toggle shows/hides password characters

### login_remember_me_row
- **Description:** Horizontal row — checkbox on left, "Keep me signed in" label on right
- **Style tokens:** Checkbox color `primary`; label `bodyMedium`, color `onSurface`, padding-start `spacing.sm`
- **Behavior:** Checkbox state persists session token in CredentialStore

### login_error_banner
- **Description:** Filled card visible only in `error` state; shows error_outline icon + error message in a row
- **Position:** Below remember-me row, above CTA button
- **Style tokens:** background `errorContainer`, border `error` (`border.thin`), border-radius `radius.sm`, padding `spacing.md`, margin-bottom `spacing.md`
- **Content:** "Invalid username or password. Please check your credentials and try again." (`bodySmall`, color `onErrorContainer`)

### login_cta_button
- **Description:** Full-width filled button "Sign In"
- **Style tokens:** container `primary`, label `onPrimary`, `labelLarge`, border-radius `radius.sm`, margin-top `spacing.lg`
- **Behavior:** Disabled at `opacity.disabled` when username or password fields are empty; shows circular loading spinner during `authenticating` state

### OR divider row
- **Description:** Horizontal row — full-width divider (`outlineVariant`, flex=1) / "OR" label (`onSurfaceVariant`, `labelMedium`) / divider
- **Position:** Below CTA, padding-top and padding-bottom `spacing.lg`

### login_oauth_button
- **Description:** Full-width outlined button "Sign in with OBP Account" with leading `open_in_browser` icon
- **Style tokens:** border `outline` (`border.thin`), text `primary`, `labelLarge`, border-radius `radius.sm`

### login_oauth_hint
- **Description:** Static text "Redirects to Open Bank Project for secure authentication"
- **Style tokens:** `bodySmall` (12 sp, Roboto), color `onSurfaceVariant`, alignment=center

### login_forgot_password_link
- **Description:** Inline link "Forgot Password?"
- **Style tokens:** `bodyMedium`, color `secondary`, alignment=center
- **Behavior:** Navigates to `forgot-password` screen on tap

---

## Interaction Patterns

| Element                   | Gesture | Outcome                                                              |
|---------------------------|---------|----------------------------------------------------------------------|
| login_cta_button          | Tap     | Fires `onDirectLoginClicked()`; transitions to `authenticating` state|
| login_oauth_button        | Tap     | Fires `onOAuthLoginClicked()`; opens system browser to OBP OIDC auth|
| login_password_input trailing icon | Tap | Toggles password character visibility                       |
| login_remember_me_checkbox | Tap    | Toggles `rememberMe` boolean in ViewModel state                      |
| login_forgot_password_link | Tap    | Navigates to `forgot-password` screen                               |
| Username field            | Focus   | Input border turns `primary` at `border.focus` width                |
| Password field            | Focus   | Input border turns `primary` at `border.focus` width                |

**State transitions:**
- `idle` → `authenticating` on Sign In tap
- `authenticating` → `idle` on success (then navigate) or `error` on 400/401
- `idle` → `oauth_redirecting` on OAuth button tap
- `oauth_redirecting` → `oauth_exchanging` on app callback receipt
- `oauth_exchanging` → success navigate or `error`

---

## Content Data

| Component             | Sample Content Value                                                           |
|-----------------------|--------------------------------------------------------------------------------|
| login_header_title    | "Welcome Back"                                                                 |
| login_header_subtitle | "Sign in to your Mifos X account"                                              |
| login_username_input  | placeholder: "Enter your username"                                             |
| login_password_input  | placeholder: "Enter your password"                                             |
| login_remember_me_label| "Keep me signed in"                                                           |
| login_error_message   | "Invalid username or password. Please check your credentials and try again."   |
| login_cta_button      | "Sign In"                                                                      |
| login_or_text         | "OR"                                                                           |
| login_oauth_button    | "Sign in with OBP Account"                                                     |
| login_oauth_hint      | "Redirects to Open Bank Project for secure authentication"                     |
| login_forgot_password | "Forgot Password?"                                                             |

---

## Design Notes

**Color usage:**
- `primary` dominates interactive elements (logo tint, headline, focused borders, CTA container, checkbox, OAuth text) — creating a consistent "brand = action" visual language.
- The error banner uses the palette's own error family end-to-end: `errorContainer` surface, `error` border, `onErrorContainer` text. That triad is guaranteed at AA and is visually distinct from the trust-blue brand, so a failed sign-in is never ambiguous.
- `secondary` (neutral slate) carries the Forgot Password link — keeping the secondary escape path visually subordinate to the primary CTA. `tertiary` is deliberately avoided here: as of DESIGN.md 1.3.0 it means warning / attention-needed, and a password-reset link is neither.

**Typography:**
- Roboto throughout — the single brand and plain face declared in `typography.font_family`. The previous Inter/Manrope pairing was outside the system entirely.
- Hierarchy is carried by the type scale, not by mixing families: `headlineLarge` > `bodyMedium` > `labelLarge` (buttons) > `bodySmall` (hints/errors).

**Spacing:**
- Generous padding-bottom `spacing.xl` (32 dp) below the subtitle creates clear separation between the brand header block and the form inputs.
- Consistent `spacing.md` (16 dp) padding inside all input fields for comfortable touch targets.
- OR divider `spacing.lg` (24 dp) top and bottom creates visual breathing room between auth method blocks.

**Accessibility:**
- Error banner uses `role=alert` on the message text, ensuring TalkBack announces the error immediately when it appears.
- CTA button `label="Sign In with DirectLogin"` disambiguates from the OAuth button for screen reader users.
- Password field `label="Password, hidden"` communicates that content is obscured.
- OAuth button label "Sign in using your Open Bank Project account via OAuth" is descriptive for screen readers.
- Minimum touch target `touch_targets.comfortable` (48×48 dp) met by all interactive elements.

---

_Generated by /idea export | 2026-08-03_
