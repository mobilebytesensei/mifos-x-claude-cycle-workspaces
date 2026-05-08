# Authentication — Mockup Spec

## Design Language

CommonPurse uses Material Design 3 with a VSLA-inspired brand palette designed for low-literacy rural users in East Africa. All touch targets are minimum 48dp. Typography uses Noto Sans at comfortable density with a large scale (+1 step above standard M3) for readability in outdoor environments.

**Brand colours**:
- Primary: #2E7D32 (deep VSLA-green — growth, trust)
- Primary Container: #A6F1A6 (soft green — tile backgrounds)
- Secondary: #FF8F00 (warm amber — harvest, shared coin)
- Secondary Container: #FFDDB3 (light amber — member tile)
- Tertiary: #1565C0 (trust-blue — informational)
- Error: #D32F2F (alert red)
- Surface: #FAFAFA (off-white card surface)
- Background: #FFFFFF

**Typography**: Noto Sans. displaySmall=36sp, headlineMedium=28sp, titleLarge=22sp, bodyLarge=16sp, labelSmall=11sp.

**Shapes**: cornerRadius sm=8dp, md=12dp, lg=16dp, full=9999dp (pill).

**Elevation**: cards use level_2 (3dp tonal shadow); top bars use 0dp.

---

## Screen-by-Screen

### ClientTypeSelectorScreen

**Layout**: Column — vertically centred, full screen, no scroll. Background: `#FFFFFF`.

**States**:
- `content` — both tiles fully rendered, ready for tap
- `navigating` — brief ripple animation then navigate; tiles disabled

**Components**:

| Component | Type | Style Summary | Interaction |
|-----------|------|--------------|-------------|
| AppLogo | Image | 80dp centred, margin_top 64dp. CommonPurse leaf+coin SVG mark. | Non-interactive |
| AppTitle | Text | "CommonPurse" — headlineLarge (32sp), bold, Noto Sans, colour onSurface (#1A1C19), centred, margin_top 12dp | Non-interactive |
| AppSubtitle | Text | "Your community savings group" — bodyLarge (16sp), colour onSurfaceVariant (#424942), centred, margin_bottom 48dp | Non-interactive |
| AdminTile | Card | Background primaryContainer (#A6F1A6), cornerRadius lg (16dp), padding 24dp, min_height 120dp, elevation 3dp, margin_horizontal 24dp, margin_bottom 16dp. Icon: FluentIcons.people_community_24_filled 48dp onPrimaryContainer. Label: "I manage a group" titleLarge semibold onPrimaryContainer. Sublabel: "Treasurer · Chairperson · Field Officer" bodyMedium onPrimaryContainer. | Tap → OnAdminSelected → login(client_type=admin) |
| MemberTile | Card | Background secondaryContainer (#FFDDB3), cornerRadius lg (16dp), padding 24dp, min_height 120dp, elevation 3dp, margin_horizontal 24dp, margin_bottom 16dp. Icon: FluentIcons.person_circle_24_filled 48dp onSecondaryContainer. Label: "I'm a group member" titleLarge semibold onSecondaryContainer. Sublabel: "Check savings · Request loans" bodyMedium onSecondaryContainer. | Tap → OnMemberSelected → login(client_type=end_user) |
| VersionLabel | Text | "v1.0.0" — labelSmall (11sp), colour outline (#727971), centred, margin_bottom 24dp, pinned to screen bottom | Non-interactive |

**Layout structure (top to bottom)**:
```
[64dp top padding]
AppLogo           — 80dp × 80dp, centred
[12dp gap]
AppTitle          — headlineLarge, centred
AppSubtitle       — bodyLarge, centred
[48dp gap]
AdminTile         — full width minus 24dp horizontal margin, 120dp min height
[16dp gap]
MemberTile        — full width minus 24dp horizontal margin, 120dp min height
[flex spacer]
VersionLabel      — centred, 24dp bottom
```

---

### LoginScreen

**Layout**: Scaffold with flat top bar + scrollable Column body. Background: `#FAFAFA`.

**States**:
- `loading` — brief splash while checking session / biometric availability; shows logo + title only
- `content` — form ready in password mode; all fields visible
- `pin_mode` — PIN pad visible; username/password hidden
- `loading_auth` — auth in progress; login button replaced by spinner; fields disabled
- `error` — auth failed; error banner below button; fields re-enabled
- `biometric_prompt` — OS biometric dialog overlaying screen

**Components**:

| Component | Type | Style Summary | Interaction |
|-----------|------|--------------|-------------|
| LoginTopBar | TopBar | Background surface (#FAFAFA), elevation 0dp. Back arrow FluentIcons.arrow_left_24_regular onSurface. No title text. | Tap back → navigate to client-type-selector |
| LoginLogo | Image | 64dp centred, margin_top 24dp. CommonPurse SVG. | Non-interactive |
| LoginTitle | Text | Admin: "Staff Login" / Member: "Member Login" — headlineMedium (28sp), bold, Noto Sans, onSurface, centred, margin_top 8dp | Non-interactive. Changes text based on clientType. |
| LoginSubtitle | Text | "Mwangaza Women's Group" — bodyLarge (16sp), colour primary (#2E7D32), centred, margin_bottom 32dp | Non-interactive. Group name from session context. |
| UsernameField | OutlinedTextField | label "Username", placeholder "Enter your username", leading icon FluentIcons.person_24_regular, keyboard text, IME next, margin_horizontal 24dp, margin_bottom 12dp. Hidden when isPinMode=true. | Type → OnUsernameChange |
| PasswordField | OutlinedTextField | label "Password", placeholder "Enter your password", leading icon FluentIcons.lock_closed_24_regular, trailing icon eye toggle, input type password, IME done, margin_horizontal 24dp, margin_bottom 8dp. Hidden when isPinMode=true. | Type → OnPasswordChange. Trailing tap → OnTogglePasswordVisibility |
| SwitchToPinButton | TextButton | Text: "Use PIN instead" / "Use password instead", colour primary (#2E7D32), alignment end, margin_horizontal 24dp, margin_bottom 16dp, min_touch_target 48dp | Tap → OnTogglePinMode |
| PinPad | Card | Visible when isPinMode=true. Surface background, cornerRadius md (12dp), margin_horizontal 24dp, padding 16dp. PIN dots row: 4 circles, filled primary (#2E7D32), empty outlineVariant (#C2C9BD). Numpad grid 3×4, digit button size 72dp, headlineSmall text. | Digit tap → OnPinChange. 4th digit → OnPinSubmit |
| BiometricButton | OutlinedButton | Visible when isBiometricAvailable=true. Circular 64dp, icon FluentIcons.fingerprint_24_filled 32dp, tint primary (#2E7D32), border primary, min_touch_target 56dp, centred, margin_top 8dp | Tap → OnBiometricClick → ShowBiometricPrompt |
| LoginButton | FilledButton | Text "Login", background primary (#2E7D32), text onPrimary (#FFFFFF), cornerRadius full (9999dp), min_height 56dp, margin_horizontal 24dp, margin_top 24dp. Disabled when username+password empty (or pin < 4 digits). | Tap → OnLoginClick |
| LoginLoadingIndicator | CircularProgressIndicator | Visible when isLoading=true. Size 32dp, colour primary (#2E7D32), centred, replaces login button | Non-interactive |
| ErrorBanner | Card | Visible when error!=null. Background errorContainer (#FFDAD6), cornerRadius md (12dp), padding 12dp, margin_horizontal 24dp, margin_top 8dp. Icon FluentIcons.warning_24_filled 20dp onErrorContainer. Text bodyMedium onErrorContainer (#410002). live_region polite. | Non-interactive. Disappears when user types. |

---

## Interaction Patterns

**Tile tap (ClientTypeSelectorScreen)**:
1. User taps AdminTile or MemberTile
2. Immediate Material ripple effect (duration short_4 = 200ms, standard easing)
3. `isNavigating` set to true; tiles disabled (pointer events none)
4. Navigate to `/login` with client_type param

**Mode toggle (LoginScreen)**:
1. User taps "Use PIN instead"
2. Username + password fields animate out (fade + slide-up, duration medium_2 = 300ms)
3. PinPad animates in (fade + slide-down, duration medium_2 = 300ms)
4. Button text changes to "Use password instead"
5. State `isPinMode` set to true

**PIN entry**:
1. Each digit tap triggers haptic feedback (light impact)
2. Dot fills with primary colour (animation duration short_3 = 150ms)
3. On 4th digit: brief 200ms pause, then auto-submits (OnPinSubmit)
4. On error: dots shake animation (4× horizontal translate ±4dp, duration 50ms each)

**Biometric prompt**:
1. Tap biometric button → OS bottom sheet appears (Android BiometricPrompt)
2. Screen blurs behind (scrim overlay 40% opacity)
3. On success: same navigation flow as password login
4. On failure: ErrorBanner shows `error_biometric_failed`

**Login button enabled state**:
- Password mode: enabled when username.isNotBlank() AND password.isNotBlank()
- PIN mode: enabled when pin.length == 4
- Loading state: disabled, shows spinner in place

---

## Accessibility

**WCAG AA compliance**:
- Primary (#2E7D32) on white: 5.83:1 — passes AA normal text
- onPrimary (#FFFFFF) on primary (#2E7D32): 13.5:1 — passes AAA
- onErrorContainer (#410002) on errorContainer (#FFDAD6): passes AA

**Touch targets**: All interactive elements minimum 48dp. BiometricButton is 56dp for safer biometric tap area.

**Content descriptions**:
- AdminTile: "I manage a group — staff or treasurer login"
- MemberTile: "I am a group member — member login"
- BiometricButton: "Login with fingerprint or face"
- LoginButton: "Login to CommonPurse"
- ErrorBanner: live_region polite for screen reader announcements

**Focus order** (LoginScreen): TopBar back → LoginLogo → LoginTitle → LoginSubtitle → UsernameField → PasswordField → SwitchToPinButton → BiometricButton → LoginButton

**PIN pad**: Each digit button has contentDescription "Digit {n}". PIN dot row contentDescription: "PIN: {n} of 4 entered".

**Screen reader mode**: When TalkBack/Voice Access active, PIN pad digits announced individually. Auto-submit disabled — user must tap Login button manually.
