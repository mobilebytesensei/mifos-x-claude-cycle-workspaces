# Authentication — Stitch Prompts

---

## 1. Design System Context

### Overview

CommonPurse is a Kotlin Multiplatform group-banking app for VSLA (Village Savings and Loan Associations) in rural East Africa. The design system is Material Design 3 (M3) with a VSLA-specific brand palette and typography scale optimised for outdoor readability and low-literacy users.

### Brand Identity

The app name is CommonPurse. The logo is a leaf-and-coin SVG mark representing community growth and shared savings. The visual language conveys trust, community, and financial empowerment. All copy is warm and supportive, not corporate.

### Full Color Palette — Light Mode

| Token | Hex | Usage |
|-------|-----|-------|
| primary | #2E7D32 | Main brand colour — VSLA green. Buttons, active states, icons, progress. |
| on_primary | #FFFFFF | Text and icons on primary backgrounds. |
| primary_container | #A6F1A6 | Soft green — admin tile background, chip fills. |
| on_primary_container | #002106 | Dark green — text/icons on primary_container. |
| secondary | #FF8F00 | Warm amber — harvest, shared coin. FAB, secondary actions. |
| on_secondary | #FFFFFF | Text/icons on secondary. |
| secondary_container | #FFDDB3 | Light amber — member tile background. |
| on_secondary_container | #2A1700 | Dark brown — text on secondary_container. |
| tertiary | #1565C0 | Trust-blue — info chips, links, loan balance highlights. |
| on_tertiary | #FFFFFF | Text/icons on tertiary. |
| tertiary_container | #D2E4FF | Light blue — info container backgrounds. |
| on_tertiary_container | #001C39 | Deep navy — text on tertiary_container. |
| error | #D32F2F | Alert red — errors, overdue badges. |
| on_error | #FFFFFF | Text/icons on error. |
| error_container | #FFDAD6 | Soft red — inline error banner background. |
| on_error_container | #410002 | Deep red — text on error_container. |
| background | #FFFFFF | Page background. |
| on_background | #1A1C19 | Primary text on background. |
| surface | #FAFAFA | Card and sheet surfaces. |
| on_surface | #1A1C19 | Primary text on surface. |
| surface_variant | #DEE5DA | Chip backgrounds, dividers, icon containers. |
| on_surface_variant | #424942 | Secondary text, captions, icons. |
| outline | #727971 | Input borders, dividers, version text. |
| outline_variant | #C2C9BD | Inactive borders, PIN empty dots, light dividers. |
| scrim | #000000 | Modal overlays at 40% opacity. |
| inverse_surface | #2F312D | Snackbar background. |
| inverse_on_surface | #F0F1EB | Snackbar text. |
| inverse_primary | #8BD68F | Accent on dark backgrounds. |

### Full Color Palette — Dark Mode

| Token | Hex | Usage |
|-------|-----|-------|
| primary | #8BD68F | Lighter green — maintains brand in dark mode |
| on_primary | #003910 | Dark green on primary |
| primary_container | #00531A | Dark green container |
| on_primary_container | #A6F1A6 | Soft green text |
| secondary | #FFB95C | Brighter amber for dark mode contrast |
| on_secondary | #472A00 | Dark text on secondary |
| secondary_container | #653E00 | Dark amber container |
| on_secondary_container | #FFDDB3 | Light text on dark amber |
| tertiary | #9FCAFF | Lighter blue |
| on_tertiary | #00325B | Dark blue on tertiary |
| tertiary_container | #004A82 | Deep blue container |
| on_tertiary_container | #D2E4FF | Light text on tertiary_container |
| error | #FFB4AB | Soft red for dark |
| on_error | #690005 | Dark red text |
| error_container | #93000A | Dark red container |
| on_error_container | #FFDAD6 | Soft red text |
| background | #1A1C19 | Dark background |
| on_background | #E2E3DD | Off-white text |
| surface | #121412 | Very dark surface |
| on_surface | #E2E3DD | Light text |
| surface_variant | #424942 | Medium grey containers |
| on_surface_variant | #C2C9BD | Light grey secondary text |
| outline | #8C9388 | Medium grey borders |
| outline_variant | #424942 | Dark dividers |

### Typography Scale

Font family: **Noto Sans** (supports Latin, Devanagari, Arabic; good Unicode coverage for Swahili/French).
Scale: Large (+1 from standard M3, for outdoor/low-vision readability).

| Style Token | Size (sp) | Line Height (sp) | Tracking (sp) | Weight | Use |
|-------------|-----------|-----------------|---------------|--------|-----|
| displayLarge | 57 | 64 | -0.25 | 400 | Hero numbers (rare) |
| displayMedium | 45 | 52 | 0 | 400 | Large balance figures |
| displaySmall | 36 | 44 | 0 | 400 | Balance primary figure |
| headlineLarge | 32 | 40 | 0 | 400 | App title on splash |
| headlineMedium | 28 | 36 | 0 | 400 | Screen titles (Login) |
| headlineSmall | 24 | 32 | 0 | 400 | Card headings |
| titleLarge | 22 | 28 | 0 | 500 | Tile labels, top-bar |
| titleMedium | 16 | 24 | 0.15 | 500 | Section headers |
| titleSmall | 14 | 20 | 0.1 | 500 | Chip labels |
| bodyLarge | 16 | 24 | 0.5 | 400 | Main body, input text |
| bodyMedium | 14 | 20 | 0.25 | 400 | Descriptions, error text |
| bodySmall | 12 | 16 | 0.4 | 400 | Supporting text |
| labelLarge | 14 | 20 | 0.1 | 500 | Button labels |
| labelMedium | 12 | 16 | 0.5 | 500 | Status chips, captions |
| labelSmall | 11 | 16 | 0.5 | 500 | Version number, fine print |

### Spacing Scale

| Token | dp Value | Common Use |
|-------|---------|------------|
| spacing_xxs | 2 | Fine dividers |
| spacing_xs | 4 | Icon-text gap |
| spacing_sm | 8 | Component inner padding |
| spacing_md | 12 | Card padding secondary |
| spacing_lg | 16 | Standard horizontal margin |
| spacing_xl | 24 | Card padding primary |
| spacing_xxl | 32 | Screen section gap |
| spacing_3xl | 48 | Large top/bottom gaps |
| spacing_4xl | 64 | Splash top padding |

### Shape Tokens

| Token | Radius | Use |
|-------|--------|-----|
| shape_none | 0dp | Sharp corners (dividers) |
| shape_extra_small | 4dp | Dense chips |
| shape_small | 8dp (cornerRadius sm) | Subtle rounding, banners |
| shape_medium | 12dp (cornerRadius md) | PIN pad, text fields |
| shape_large | 16dp (cornerRadius lg) | Main cards, tiles |
| shape_extra_large | 28dp | Bottom sheet corners |
| shape_full | 9999dp | Pill buttons, circular chips |

### Elevation Levels

| Level | Shadow dp | Tonal Alpha | Use |
|-------|-----------|------------|-----|
| level_0 | 0 | 0.00 | Flat surfaces, top bars |
| level_1 | 1 | 0.05 | Slightly raised items |
| level_2 | 3 | 0.08 | Cards, tiles |
| level_3 | 6 | 0.11 | Dialogs, navigation drawers |
| level_4 | 8 | 0.12 | Modal bottom sheets |
| level_5 | 12 | 0.14 | FAB, menus |

### Motion & Animation Durations

| Token | Duration (ms) | Easing | Use |
|-------|--------------|--------|-----|
| short_1 | 50 | standard | PIN dot micro-animation |
| short_2 | 100 | standard | Icon state changes |
| short_3 | 150 | standard | PIN dot fill animation |
| short_4 | 200 | standard | Tile ripple, button press |
| medium_1 | 250 | emphasized | Navigation fade |
| medium_2 | 300 | emphasized | Mode toggle transitions |
| medium_3 | 350 | emphasized | Card entrance |
| medium_4 | 400 | emphasized | Full page transitions |
| long_1 | 450 | decelerated | Complex content loading |
| long_2 | 500 | decelerated | Hero animations |

Easing curves:
- standard: cubic-bezier(0.2, 0.0, 0, 1.0)
- emphasized: cubic-bezier(0.2, 0.0, 0, 1.0)
- decelerated: cubic-bezier(0.0, 0.0, 0, 1.0)
- accelerated: cubic-bezier(0.3, 0.0, 1.0, 1.0)

### Accessibility Baseline

- Minimum touch target: 48dp × 48dp (all interactive elements)
- Contrast normal text: 4.5:1 minimum (WCAG AA)
- Contrast large text (≥18sp or ≥14sp bold): 3.0:1 minimum
- Focus ring width: 3dp
- All icon-only buttons must have contentDescription
- Error states must use live_region="polite" for screen readers
- Biometric button uses 56dp for safer activation area

---

## 2. Screen Layouts

### ClientTypeSelectorScreen — Full Component Tree

Screen dimensions: 360dp × 800dp (compact baseline).
Safe area: status bar 24dp top, navigation bar 48dp bottom.
Background: #FFFFFF.
Scroll: None (Column, verticalArrangement = Center, horizontalAlignment = CenterHorizontally).

```
Screen (360dp × 800dp)
└── Column(
      modifier = fillMaxSize().padding(bottom = 48dp /* nav bar */),
      verticalArrangement = Arrangement.Center,
      horizontalAlignment = Alignment.CenterHorizontally
    )
    ├── Spacer(height = 64dp)                          [spacing_4xl]
    ├── AppLogo
    │     width = 80dp, height = 80dp
    │     contentDescription = "CommonPurse logo"
    │
    ├── Spacer(height = 12dp)                          [spacing_md]
    ├── AppTitle
    │     text = "CommonPurse"
    │     style = headlineLarge (32sp, weight 400, Noto Sans)
    │     color = on_surface (#1A1C19)
    │     textAlign = Center
    │
    ├── Spacer(height = 4dp)                           [spacing_xs]
    ├── AppSubtitle
    │     text = "Your community savings group"
    │     style = bodyLarge (16sp)
    │     color = on_surface_variant (#424942)
    │     textAlign = Center
    │     paddingBottom = 48dp                         [spacing_3xl]
    │
    ├── AdminTile                                      [full-width minus 48dp for 24dp margins each side]
    │     width = 312dp (360 - 48)
    │     minHeight = 120dp
    │     background = primary_container (#A6F1A6)
    │     cornerRadius = 16dp                          [shape_large]
    │     elevation = 3dp                              [level_2]
    │     padding = 24dp                               [spacing_xl]
    │     marginBottom = 16dp                          [spacing_lg]
    │     ├── FluentIcons.people_community_24_filled
    │     │     size = 48dp, tint = on_primary_container (#002106)
    │     ├── Text "I manage a group"
    │     │     style = titleLarge (22sp, weight 500)
    │     │     color = on_primary_container (#002106)
    │     └── Text "Treasurer · Chairperson · Field Officer"
    │           style = bodyMedium (14sp)
    │           color = on_primary_container (#002106)
    │
    ├── MemberTile                                     [full-width minus 48dp]
    │     width = 312dp
    │     minHeight = 120dp
    │     background = secondary_container (#FFDDB3)
    │     cornerRadius = 16dp                          [shape_large]
    │     elevation = 3dp                              [level_2]
    │     padding = 24dp                               [spacing_xl]
    │     marginBottom = 16dp                          [spacing_lg]
    │     ├── FluentIcons.person_circle_24_filled
    │     │     size = 48dp, tint = on_secondary_container (#2A1700)
    │     ├── Text "I'm a group member"
    │     │     style = titleLarge (22sp, weight 500)
    │     │     color = on_secondary_container (#2A1700)
    │     └── Text "Check savings · Request loans"
    │           style = bodyMedium (14sp)
    │           color = on_secondary_container (#2A1700)
    │
    ├── Spacer(weight = 1f)                            [fills remaining vertical space]
    └── VersionLabel
          text = "v1.0.0"
          style = labelSmall (11sp, weight 500)
          color = outline (#727971)
          textAlign = Center
          paddingBottom = 24dp
```

Z-ordering: All elements in natural stack order. No overlapping components on this screen.

---

### LoginScreen — Full Component Tree

Screen dimensions: 360dp × 800dp (compact baseline).
Safe area: status bar 24dp top, navigation bar 48dp bottom.
Background: #FAFAFA.
Scroll: Column with verticalScroll(rememberScrollState()) — handles small screens.

```
Screen (360dp × 800dp)
└── Scaffold(
      topBar = LoginTopBar,
      containerColor = surface (#FAFAFA)
    )
    ├── LoginTopBar
    │     height = 64dp, background = surface (#FAFAFA), elevation = 0dp
    │     ├── IconButton (back)
    │     │     icon = FluentIcons.arrow_left_24_regular
    │     │     tint = on_surface (#1A1C19)
    │     │     size = 48dp touch target
    │     │     paddingStart = 4dp
    │     └── [no title]
    │
    └── Content (Column, scrollable)
          paddingTop = 0dp
          paddingHorizontal = 0dp  (individual components manage horizontal padding)
          │
          ├── LoginLogo
          │     width = 64dp, height = 64dp
          │     alignment = Center
          │     marginTop = 24dp
          │
          ├── LoginTitle
          │     [admin] text = "Staff Login"
          │     [member] text = "Member Login"
          │     style = headlineMedium (28sp, weight 400, Noto Sans)
          │     color = on_surface (#1A1C19)
          │     textAlign = Center
          │     marginTop = 8dp
          │
          ├── LoginSubtitle
          │     text = "Mwangaza Women's Group"
          │     style = bodyLarge (16sp)
          │     color = primary (#2E7D32)
          │     textAlign = Center
          │     marginBottom = 32dp
          │
          ├── [visible when isPinMode == false]
          │   UsernameField (OutlinedTextField)
          │     width = 312dp (24dp margin each side)
          │     height = 56dp min
          │     label = "Username"
          │     placeholder = "Enter your username"
          │     leadingIcon = FluentIcons.person_24_regular, 24dp, on_surface_variant
          │     keyboard = KeyboardType.Text, ImeAction.Next
          │     activeColor = primary (#2E7D32)
          │     unfocusedBorderColor = outline (#727971)
          │     focusedBorderColor = primary (#2E7D32)
          │     marginBottom = 12dp
          │
          ├── [visible when isPinMode == false]
          │   PasswordField (OutlinedTextField)
          │     width = 312dp
          │     height = 56dp min
          │     label = "Password"
          │     placeholder = "Enter your password"
          │     leadingIcon = FluentIcons.lock_closed_24_regular, 24dp
          │     trailingIcon = FluentIcons.eye_24_regular / eye_off toggle
          │     visualTransformation = PasswordVisualTransformation()
          │     keyboard = KeyboardType.Password, ImeAction.Done
          │     marginBottom = 8dp
          │
          ├── SwitchToPinButton (TextButton)
          │     [isPinMode=false] text = "Use PIN instead"
          │     [isPinMode=true] text = "Use password instead"
          │     style = labelLarge (14sp, weight 500)
          │     color = primary (#2E7D32)
          │     alignment = End (right-aligned)
          │     paddingHorizontal = 24dp
          │     marginBottom = 16dp
          │     minTouchTarget = 48dp
          │
          ├── [visible when isPinMode == true]
          │   PinPad (Card)
          │     width = 312dp
          │     background = surface (#FAFAFA)
          │     cornerRadius = 12dp [shape_medium]
          │     padding = 16dp
          │     marginHorizontal = 24dp
          │     ├── PinDotsRow (Row, centred, gap 16dp)
          │     │     4× Circle(
          │     │       size = 16dp,
          │     │       filled: color = primary (#2E7D32)
          │     │       empty: color = outline_variant (#C2C9BD)
          │     │     )
          │     │     marginBottom = 20dp
          │     └── NumGrid (LazyVerticalGrid columns=3, gap=8dp)
          │           Digits: 1-9, backspace, 0, delete
          │           Each digit button: 72dp × 72dp
          │           text style = headlineSmall (24sp)
          │           color = on_surface (#1A1C19)
          │           background = surface_variant (#DEE5DA)
          │           cornerRadius = full (9999dp)
          │
          ├── [visible when isBiometricAvailable == true]
          │   BiometricButton (OutlinedButton)
          │     shape = CircleShape
          │     size = 64dp
          │     borderColor = primary (#2E7D32)
          │     icon = FluentIcons.fingerprint_24_filled, 32dp, tint = primary (#2E7D32)
          │     alignment = Center
          │     marginTop = 8dp
          │     minTouchTarget = 56dp
          │
          ├── [visible when isLoading == false]
          │   LoginButton (FilledButton)
          │     width = 312dp
          │     minHeight = 56dp
          │     background = primary (#2E7D32)
          │     text = "Login"
          │     textColor = on_primary (#FFFFFF)
          │     style = labelLarge (14sp, weight 500)
          │     cornerRadius = 9999dp [shape_full]
          │     marginHorizontal = 24dp
          │     marginTop = 24dp
          │     disabled: background = surface_variant (#DEE5DA), textColor = on_surface_variant
          │
          ├── [visible when isLoading == true]
          │   CircularProgressIndicator
          │     size = 32dp
          │     color = primary (#2E7D32)
          │     alignment = Center
          │     marginTop = 24dp
          │     strokeWidth = 3dp
          │
          └── [visible when error != null]
              ErrorBanner (Card)
                width = 312dp
                background = error_container (#FFDAD6)
                cornerRadius = 12dp [shape_medium]
                padding = 12dp
                marginHorizontal = 24dp
                marginTop = 8dp
                Row(verticalAlignment = CenterVertically, gap = 8dp)
                  ├── FluentIcons.warning_24_filled, 20dp, tint = on_error_container (#410002)
                  └── Text
                        style = bodyMedium (14sp)
                        color = on_error_container (#410002)
                        text = [localised error message]
```

Keyboard avoidance: Scaffold uses `WindowCompat.setDecorFitsSystemWindows(window, false)` + `imePadding()` modifier on the Column. The entire form scrolls up to keep the active field visible above the soft keyboard.

---

## 3. Component Specifications

### AdminTile — Complete Spec

**Purpose**: Large, highly tappable entry point for admin/staff users. Designed for users who may have thick fingers or be accessing in outdoor conditions.

**Default state**:
- Background: primary_container (#A6F1A6)
- Elevation shadow: 3dp (level_2 tonal overlay)
- Corner radius: 16dp
- Padding: 24dp all sides
- Minimum height: 120dp (robust touch target)
- Margin horizontal: 24dp (full-width feel with breathing room)

**Pressed state**:
- Ripple: colour on_primary_container (#002106) at 12% opacity
- Ripple duration: 200ms (short_4)
- Scale: none (M3 does not scale cards, uses ripple only)
- Elevation: unchanged (stays at 3dp)

**Disabled state** (during navigation):
- Pointer events: none
- Opacity: 0.38 (M3 disabled alpha)
- Animation: fade to 0.38 over 150ms (short_3)

**Focused state** (keyboard/TalkBack):
- Focus ring: 3dp width, colour primary (#2E7D32), 2dp offset
- Background: unchanged

**Icon layout**:
- FluentIcons.people_community_24_filled
- Rendered size: 48dp × 48dp (larger than icon name suggests — custom size)
- Tint: on_primary_container (#002106)
- Position: Row, vertical centred, trailing the text block in Icon+Text layout
- Alternative layout: Icon top, text below (portrait with small tiles) — see Responsive Rules §6

**Text layout**:
- "I manage a group" — titleLarge (22sp, weight 500), on_primary_container (#002106), Noto Sans
- "Treasurer · Chairperson · Field Officer" — bodyMedium (14sp, weight 400), on_primary_container (#002106), opacity 0.87
- Vertical arrangement: title above subtitle with 4dp gap

**Accessibility**:
- role: Button
- contentDescription: "I manage a group — staff or treasurer login"
- Semantic heading: false
- Min touch target: 120dp height ensures far exceeds 48dp requirement

---

### MemberTile — Complete Spec

**Purpose**: Entry for end users (group members), visually differentiated from AdminTile via amber colour scheme.

**Default state**:
- Background: secondary_container (#FFDDB3)
- All other structural properties identical to AdminTile
- Icon: FluentIcons.person_circle_24_filled, 48dp, tint on_secondary_container (#2A1700)
- Title text colour: on_secondary_container (#2A1700)

**Pressed state**:
- Ripple: colour on_secondary_container (#2A1700) at 12% opacity, duration 200ms

**Contrast check**:
- on_secondary_container (#2A1700) on secondary_container (#FFDDB3): 8.4:1 — AAA

---

### UsernameField — Complete Spec

**Variants**:
- Default (unfocused): border outline (#727971) 1dp, label floated at bodySmall above
- Focused: border primary (#2E7D32) 2dp, label colour primary
- Filled (has value): label floated, text visible, border outline
- Error: border error (#D32F2F) 2dp, label colour error, supporting text in error colour
- Disabled: border outline_variant 1dp, opacity 0.38, pointer-events none

**Layout inside field**:
- Leading icon: FluentIcons.person_24_regular, 24dp, on_surface_variant (#424942)
  - Icon left-padded: 12dp from edge
- Label text: "Username" — bodyLarge floats to labelSmall on focus/fill
- Input text: bodyLarge (16sp), on_surface (#1A1C19), Noto Sans
- Placeholder text: "Enter your username" — on_surface_variant (#424942) at 60% opacity
- Height: 56dp (M3 filled text field height)
- Corner radius: 12dp (shape_medium) — rounded top corners, square bottom in filled variant; all-round in outlined variant

**Keyboard behaviour**:
- IME action: Next (advances focus to PasswordField)
- KeyboardType: Text
- Autocorrect: false
- AutoFill hint: username (for password manager support)

---

### PasswordField — Complete Spec

**Inherits**: all UsernameField properties except:
- Leading icon: FluentIcons.lock_closed_24_regular
- Trailing icon toggle:
  - Eye closed (password hidden): FluentIcons.eye_off_24_regular, 24dp, on_surface_variant
  - Eye open (password visible): FluentIcons.eye_24_regular, 24dp, primary (#2E7D32)
- VisualTransformation: PasswordVisualTransformation (•••)
  - When isPasswordVisible = true: no transformation (plain text)
- IME action: Done (triggers OnLoginClick if fields valid)
- KeyboardType: Password (disables predictive text, suggestions)
- AutoFill hint: password

**Toggle animation**:
- Icon crossfade: duration 100ms (short_2)
- Password characters reveal: immediate on toggle (no animation — security)

---

### PinPad — Complete Spec

**Container**:
- Background: surface (#FAFAFA)
- Corner radius: 12dp (shape_medium)
- Padding: 16dp
- No elevation (flat)
- Width: fill (minus 24dp horizontal margin)

**PIN Dots Row**:
- Horizontal Row, centred, gap 16dp between dots
- 4× Circle indicators:
  - Size: 16dp diameter
  - Filled state: background primary (#2E7D32), no border
  - Empty state: background transparent, border 2dp outline_variant (#C2C9BD)
  - Transition: empty→filled in 150ms (short_3) with scale-in from 60% to 100%
  - Transition: filled→empty (backspace) in 100ms (short_2) scale-out
- Row margin bottom: 20dp

**Numpad Grid**:
- 3 columns × 4 rows = 12 buttons (1-9, backspace, 0, submit/delete)
- Grid gap: 8dp row and column
- Each digit button:
  - Size: 72dp × 72dp
  - Shape: CircleShape (full pill)
  - Background: surface_variant (#DEE5DA)
  - Text: digit character, headlineSmall (24sp), on_surface (#1A1C19), weight 400
  - Pressed ripple: on_surface (#1A1C19) at 12%, duration 100ms
  - Touch target: 72dp (exceeds 48dp minimum)
- Backspace button (row 4, col 1):
  - Icon: FluentIcons.backspace_24_regular, 24dp, on_surface (#1A1C19)
  - Background: transparent
  - Long press: clear all digits (hold 500ms)
- Zero button (row 4, col 2): standard digit style
- Row 4, col 3: empty (no button) or confirmation icon if all 4 digits filled

**Auto-submit behaviour**:
- 4th digit entered → 200ms delay (short_4) → auto-submit OnPinSubmit
- During 200ms: all buttons disabled, 4th dot animation completes
- On error: all dots shake (see Interaction Patterns §4), all cleared after 1 second

---

### BiometricButton — Complete Spec

**Visibility**: Only rendered when isBiometricAvailable = true (checked on screen entry via BiometricManager.canAuthenticate()).

**Default state**:
- Shape: CircleShape
- Size: 64dp × 64dp
- Border: 2dp, primary (#2E7D32)
- Background: transparent
- Icon: FluentIcons.fingerprint_24_filled, 32dp, tint primary (#2E7D32)
- Alignment: centred horizontally
- Margin top: 8dp

**Pressed state**:
- Ripple: primary (#2E7D32) at 20% opacity, fills circle
- Scale: 0.95 on press, return to 1.0 on release (duration 100ms each)

**Processing state** (after tap, while OS dialog appears):
- Icon pulses: scale 1.0→1.1→1.0, duration 600ms per cycle, repeat until OS dialog shows

**Error state** (BiometricFailed):
- Icon temporarily changes to FluentIcons.warning_24_filled, tint error (#D32F2F)
- Duration: 1500ms, then reverts to fingerprint icon

**Accessibility**:
- contentDescription: "Login with fingerprint or face"
- minimumTouchTarget: 56dp (slightly larger than visual for safe biometric activation)

---

### LoginButton — Complete Spec

**Enabled state**:
- Background: primary (#2E7D32)
- Text: "Login" — labelLarge (14sp, weight 500)
- Text colour: on_primary (#FFFFFF)
- Corner radius: 9999dp (shape_full — pill)
- Width: fill (minus 24dp horizontal margin = 312dp on 360dp screen)
- Min height: 56dp

**Disabled state**:
- Background: on_surface (#1A1C19) at 12% opacity → effectively #E0E0E0
- Text colour: on_surface (#1A1C19) at 38% opacity
- Cursor: default (non-interactive visual)

**Loading state** (isLoading = true):
- LoginButton hidden (alpha 0, no layout space)
- Replaced by CircularProgressIndicator: 32dp, stroke 3dp, primary (#2E7D32)
- Transition: button fades out (150ms), spinner fades in (150ms)

**Pressed state**:
- Ripple: on_primary (#FFFFFF) at 20%
- Scale: 0.97 during press, 1.0 on release
- Duration: 150ms

**Success transition** (auth complete):
- Button colour crossfades primary → transparent (300ms, medium_2)
- Navigation fires immediately

---

### ErrorBanner — Complete Spec

**Visibility**: Shown when error != null AND isLoading == false.
**Entry animation**: Slides down from above with fade-in (duration 200ms, short_4, decelerated easing).
**Exit animation**: Fades out + slides up (duration 150ms, short_3).

**Layout**:
- Background: error_container (#FFDAD6)
- Corner radius: 12dp
- Padding: 12dp
- Margin horizontal: 24dp
- Margin top: 8dp
- Row layout: icon + text, verticalAlignment = CenterVertically, gap 8dp

**Icon**: FluentIcons.warning_24_filled, 20dp, on_error_container (#410002)

**Text content by error type**:
- InvalidCredentials: "Incorrect username or password. Please try again."
- Network: "No internet connection. Login with your PIN."
- Server: "Server error. Please try again later."
- PinNotSet: "PIN not set up. Please login with your password first."
- BiometricFailed: "Biometric not recognised. Try again or use your password."

**Dismiss behaviour**: Banner clears automatically when user begins typing in username or password field (OnUsernameChange or OnPasswordChange fires → error set to null).

**Accessibility**: live_region = "polite" — screen reader announces error text when it appears.

---

## 4. Interaction Patterns

### Client Type Selection — Full Flow

**Trigger**: User taps AdminTile or MemberTile on ClientTypeSelectorScreen.

**Step-by-step**:
1. Finger down on tile → Material press state activates (ripple starts from touch point, colour on_primary_container at 12%, expands outward)
2. Ripple duration: 200ms (short_4), easing: standard cubic-bezier(0.2, 0.0, 0, 1.0)
3. Finger up → ripple completes (snaps to full fill briefly)
4. `OnAdminSelected` or `OnMemberSelected` action dispatched
5. `isNavigating` set to true
6. Both tiles receive alpha 0.38 (disabled visual) over 150ms
7. Navigation event emitted
8. Screen transition: fade-through (M3 container transform not applicable here; use shared-axis horizontal) — current screen slides left (300ms medium_2), login screen slides in from right
9. Analytics event fired: `client_type_selected` with `client_type: "admin"` or `client_type: "end_user"`

### Login Button Tap — Full Flow

**Trigger**: User taps LoginButton (enabled state only).

**Step-by-step**:
1. Press haptic feedback: light impact (10ms)
2. Button scale: 0.97 over 50ms
3. Button scale return: 1.0 over 100ms
4. `OnLoginClick` action dispatched
5. `isLoading` set to true
6. LoginButton fades out (alpha 0) over 150ms
7. CircularProgressIndicator fades in over 150ms
8. Username + password fields set to readOnly = true (visually same, pointer-events disabled)
9. SwitchToPinButton hidden (alpha 0)
10. API call initiated (POST /authentication or /self/authentication)

**On success (HTTP 200)**:
11. `isLoading` set to false
12. LoginButton fades back (150ms) — brief re-appearance before navigation
13. Navigation event emitted (NavigateToAdminDashboard or NavigateToEndUserDashboard)
14. Screen transition: fade-through horizontal (300ms) to dashboard
15. Analytics: `login_success` event

**On error**:
11. `isLoading` set to false
12. LoginButton fades back in (150ms)
13. Fields re-enabled
14. `error` state set → ErrorBanner slides in (200ms)
15. Keyboard maintained (do not dismiss)
16. Analytics: `login_failed` event with error_type

### PIN Entry — Complete Flow

**Trigger**: User is in isPinMode=true. Numpad visible.

**Step 1 — Digit tap**:
1. Press haptic: light impact (10ms)
2. Button ripple (100ms, short_2)
3. `OnPinChange(digit)` dispatched
4. Corresponding dot (1st, 2nd, 3rd, 4th available) fills:
   - Scale animation: 0.0 → 1.0 over 150ms (short_3)
   - Color: transparent/outline → primary (#2E7D32)
5. pin state updated

**Step 2 — Backspace tap**:
1. Last filled dot empties:
   - Scale: 1.0 → 0.0 over 100ms (short_2)
   - Color: primary → outline_variant
2. `pin` loses last character

**Step 3 — 4th digit entered**:
1. 4th dot fills (150ms)
2. Brief pause 200ms
3. During pause: all digit buttons disabled (opacity 0.5)
4. `OnPinSubmit` dispatched → same loading flow as LoginButton tap
5. If success: navigate to appropriate dashboard
6. If error: 
   - All 4 dots shake animation: translate X by +4dp → -4dp → +4dp → -4dp → 0
   - Each oscillation: 50ms (short_1)
   - Total shake: 200ms
   - After shake: all dots clear (scale-out 100ms each, staggered by 50ms)
   - ErrorBanner appears

**Step 4 — Long-press backspace** (hold > 500ms):
- All dots clear simultaneously: staggered scale-out (50ms per dot, starting from 4th)
- `pin` state cleared to ""
- Haptic: medium impact

### Password Visibility Toggle — Flow

**Trigger**: User taps eye icon in PasswordField trailing icon area.

**Step-by-step**:
1. `OnTogglePasswordVisibility` dispatched
2. `isPasswordVisible` toggled
3. Eye icon crossfade: eye_off → eye or eye → eye_off (100ms, short_2)
4. VisualTransformation changes: password chars briefly flash visible then hide (or vice versa)
5. No cursor position change
6. No keyboard dismiss

### Mode Toggle (Password ↔ PIN) — Full Transition

**Trigger**: Tap "Use PIN instead" / "Use password instead"

**Animation sequence** (300ms total, medium_2):
1. `OnTogglePinMode` dispatched
2. `isPinMode` toggled
3. Outgoing components (password mode → pin mode):
   - UsernameField: alpha 1→0, translationY 0→-20dp, duration 150ms, accelerated easing
   - PasswordField: alpha 1→0, translationY 0→-20dp, delay 50ms, duration 150ms
4. Incoming components:
   - PinPad: alpha 0→1, translationY +20dp→0, delay 100ms, duration 200ms, decelerated easing
5. SwitchToPinButton text changes at midpoint (after outgoing completes)
6. BiometricButton remains visible throughout
7. LoginButton remains visible; enabled state recalculates for pin mode (pin.length == 4)

### Biometric Authentication — Full Flow

**Trigger**: Tap BiometricButton

**Step-by-step**:
1. `OnBiometricClick` dispatched
2. BiometricButton icon pulses (scale 1.0→1.1→1.0, 600ms loop)
3. `ShowBiometricPrompt` event emitted
4. Android BiometricPrompt.authenticate() called
5. OS bottom sheet slides up (system-controlled animation, ~300ms)
6. Screen behind biometric sheet: scrim overlay (#000000 at 40%)

**On biometric SUCCESS**:
7. OS sheet dismisses (system animation)
8. Scrim fades out (200ms)
9. BiometricButton icon pulse stops
10. isLoading = true → spinner shown
11. Session restored from local cache (no network call)
12. Navigate to appropriate dashboard (admin or end-user based on stored clientType)

**On biometric FAILURE** (wrong fingerprint, etc.):
7. OS sheet shows error state (system-controlled)
8. User may retry via OS sheet (up to 5 attempts system limit)
9. If all attempts exhausted: OS sheet dismisses
10. BiometricButton icon shows warning_24_filled in error (#D32F2F) for 1500ms
11. ErrorBanner slides in: "Biometric not recognised. Try again or use your password."

**On biometric CANCEL** (user taps cancel on OS sheet):
7. OS sheet dismisses
8. Scrim fades out
9. BiometricButton icon pulse stops
10. No error banner — return to normal content state

### Loading State Transitions

**Entry into loading_auth state**:
- Duration: 150ms (short_3)
- LoginButton fades to alpha 0
- CircularProgressIndicator fades to alpha 1
- All input fields: enabled → readOnly (no visual change, just interaction blocked)
- SwitchToPinButton: alpha 0.38 (disabled visual)
- BiometricButton: alpha 0.38

**Exit from loading_auth state** (success):
- Duration: 100ms (short_2)
- All components snap back (not needed — navigation fires immediately)

**Exit from loading_auth state** (error):
- Duration: 150ms (short_3)
- CircularProgressIndicator fades to alpha 0
- LoginButton fades to alpha 1 (enabled or disabled based on field state)
- Input fields re-enabled
- ErrorBanner slides in (200ms, from translateY -12dp to 0, with alpha 0→1)

---

## 5. Content Data

### Real Member Data — Mwangaza Women's Group

**Group name**: Mwangaza Women's Group
**Location**: Kisumu County, Kenya
**Currency**: KES (Kenyan Shillings)
**Meeting frequency**: Weekly (every Thursday, 2:00 PM)
**Cycle**: Cycle 3, began 4 January 2026, ends 31 December 2026
**Group size**: 18 members

**Admin user accounts** (treasurer/staff):

| Username | Role | Office |
|---------|------|--------|
| mwangaza_treasurer | TREASURER | Kisumu Branch |
| mwangaza_chair | CHAIRPERSON | Kisumu Branch |
| mwangaza_secretary | SECRETARY | Kisumu Branch |
| field_officer_001 | FIELD_OFFICER | Kisumu Region |

**Admin login sample credentials** (for UI demo):
- Username: `mwangaza_treasurer`
- Password: `••••••••` (masked)
- POST /authentication response:
  - userId: 1042
  - authenticated: true
  - roles: ["ROLE_TELLER", "ROLE_LOAN_OFFICER"]
  - officeId: 7
  - officeName: "Kisumu Branch"

**End-user member accounts** (self-service):

| Username | Member Name | clientId |
|---------|------------|---------|
| grace.mwangi | Grace Mwangi | 2081 |
| amara.diallo | Amara Diallo | 2082 |
| fatuma.hassan | Fatuma Hassan | 2083 |
| priscilla.ochieng | Priscilla Ochieng | 2084 |
| mary.akinyi | Mary Akinyi | 2085 |
| esther.wanjiku | Esther Wanjiku | 2086 |
| janet.chebet | Janet Chebet | 2087 |
| alice.otieno | Alice Otieno | 2088 |
| florence.kamau | Florence Kamau | 2089 |
| beatrice.njeri | Beatrice Njeri | 2090 |

**Sample end-user login** (Grace Mwangi):
- Username: `grace.mwangi`
- Password: `••••••••` (masked)
- POST /self/authentication response:
  - userId: 2081
  - authenticated: true
  - clientId: 2081
  - clientName: "Grace Mwangi"
  - base64EncodedAuthenticationKey: "Z3JhY2UubXdhbmdpOm15c2VjcmV0"

**PIN scenario** (Grace Mwangi, offline):
- Stored PIN hash: locally encrypted on device
- PIN: 4 digits, set during first successful password login
- PIN entry on-device: validates against stored hash (no network)
- Successful PIN login restores cached session token for offline mode

**Biometric scenario** (Grace Mwangi, Android 11+ device):
- Device: Samsung Galaxy A32 (common VSLA user device)
- Fingerprint enrolled: Yes
- BiometricManager.canAuthenticate() = BIOMETRIC_SUCCESS
- BiometricButton shown
- On successful fingerprint: restores cached session, navigates to personal-dashboard(clientId=2081)

**Error scenarios with real data**:

Scenario 1 — Wrong password:
- User enters: username=grace.mwangi, password=wrongpassword123
- HTTP 401 response
- ErrorBanner shows: "Incorrect username or password. Please try again."
- Fields remain filled (username preserved, password cleared for re-entry)

Scenario 2 — Network offline:
- User taps Login with fields filled
- ConnectivityManager.isOnline() = false
- ErrorBanner shows: "No internet connection. Login with your PIN."
- SwitchToPinButton highlighted briefly (pulse animation 500ms) to draw attention

Scenario 3 — Server timeout:
- POST /authentication response: 503
- ErrorBanner shows: "Server error. Please try again later."
- Retry button not shown inline — user taps Login button again

Scenario 4 — PIN not set (member tries PIN before first password login):
- user taps "Use PIN instead" on a fresh device
- Attempts PIN entry
- PinManager.isPinConfigured() = false
- ErrorBanner shows: "PIN not set up. Please login with your password first."
- Auto-toggle back to password mode after 2 seconds

### Analytics Events — Sample Payload

**client_type_selected** (admin path):
```
{
  "event": "client_type_selected",
  "client_type": "admin",
  "timestamp": "2026-05-06T09:14:22Z",
  "session_id": "abc123"
}
```

**login_success** (Grace Mwangi, password mode):
```
{
  "event": "login_success",
  "client_type": "end_user",
  "mode": "password",
  "client_id": 2081,
  "timestamp": "2026-05-06T09:15:01Z"
}
```

**login_failed** (wrong password):
```
{
  "event": "login_failed",
  "client_type": "end_user",
  "mode": "password",
  "error_type": "InvalidCredentials",
  "timestamp": "2026-05-06T09:14:55Z"
}
```

**biometric_triggered**:
```
{
  "event": "biometric_triggered",
  "client_type": "end_user",
  "timestamp": "2026-05-06T09:14:28Z"
}
```

---

## 6. Responsive Rules

### Compact (0–599dp width) — Phones (Primary Target)

**ClientTypeSelectorScreen**:
- Tiles: full-width minus 24dp horizontal margin each side → width = screenWidth - 48dp
- Logo: 80dp
- Tiles arranged vertically (Column) with 16dp gap
- VersionLabel: fixed to bottom

**LoginScreen**:
- UsernameField + PasswordField: full-width minus 24dp margin → width = screenWidth - 48dp
- PinPad: full-width minus 24dp margin
- PinPad digit buttons: 72dp × 72dp (fits 3 across with 8dp gaps in 312dp content area: 3×72 + 2×8 = 232dp + rest for padding)
- LoginButton: full-width minus 24dp margin → pill spanning full usable width
- Top bar height: 56dp
- Content scrollable with imePadding

**Typography**: No adjustment from base scale (already large-scale M3).

**Navigation**: BottomNavigationBar not shown on auth screens (bottom_nav: false for both screens).

---

### Medium (600–839dp width) — Foldables, Small Tablets

**ClientTypeSelectorScreen**:
- Tiles: max-width 480dp, centred horizontally with auto margins
- Logo: 96dp
- Increased padding between sections: xl → xxl

**LoginScreen**:
- Form: max-width 480dp, centred (HorizontalAlignment.CenterHorizontally)
- PinPad digit buttons: 80dp × 80dp (more room, better UX for reading-glasses users)
- BiometricButton: 72dp (slightly larger)
- LoginButton: max-width 480dp, centred
- Top bar: same height, wider → show organisation name "CommonPurse" as centred title

---

### Expanded (≥840dp width) — Tablets and Desktop

**ClientTypeSelectorScreen**:
- Two-column layout: Logo+title stack on LEFT, tiles on RIGHT
- Left pane: 400dp, right pane: remaining width
- Background: left pane primary (#2E7D32), right pane white
- Logo: 120dp, white version
- App title: white (on_primary)
- Tiles: max-width 400dp in right pane

**LoginScreen**:
- Two-column layout: branding left, form right
- Left pane (400dp): green background (#2E7D32), white logo, white app title, tagline
- Right pane: white, centred form with max-width 400dp
- PinPad digit buttons: 88dp × 88dp
- LoginButton: max-width 400dp
- Navigation: NavigationRail instead of BottomNav (not applicable on auth screens, but note for post-login screens)

**Form layout changes**:
- No keyboard avoidance needed (external keyboard; no soft keyboard obscuring form)
- imePadding() still applied for connected soft keyboard on foldables

---

### Navigation Pattern by Breakpoint

| Screen | Compact | Medium | Expanded |
|--------|---------|--------|---------|
| auth screens | No bottom nav | No bottom nav | No bottom nav |
| post-login (dashboard) | BottomNavigationBar | BottomNavigationBar | NavigationRail |
| Drawer | Not used | Not used | Optional permanent drawer |

### Orientation Handling

**Portrait (default)**:
- Both auth screens use vertical stack layout as described above

**Landscape (compact)**:
- ClientTypeSelectorScreen: Tiles arranged in Row (2 columns) instead of Column
- LoginScreen: Form width capped at 400dp; screen scrolls
- VersionLabel: moved to end of form content (not fixed to bottom)
- PinPad: digit buttons reduced to 64dp to fit available height
- Logo hidden in landscape login to save vertical space

**Landscape (medium/expanded)**:
- Same as expanded portrait layout (two-column)

---

## Appendix A — State Transition Diagram (Authentication)

The following describes every state and valid transition for the LoginScreen state machine.

### LoginScreenState Transitions

**Idle → Loading**
- Trigger: Screen first composable; BiometricManager.canAuthenticate() check runs
- Duration: typically < 100ms
- Visual: logo + title only; no fields yet

**Loading → Content**
- Trigger: BiometricManager check complete; no stored session found
- Visual transition: fields fade in sequentially (staggered 50ms each, total ~300ms)
- Fields appear in order: LoginTitle, LoginSubtitle, UsernameField, PasswordField, SwitchToPinButton, BiometricButton (if available), LoginButton

**Content → Loading_auth**
- Trigger: OnLoginClick dispatched with valid credentials
- Visual: LoginButton fades out, CircularProgressIndicator fades in (150ms)

**Content → BiometricPrompt**
- Trigger: OnBiometricClick dispatched
- Visual: OS BiometricPrompt appears over screen

**Loading_auth → Success**
- Trigger: API returns HTTP 200 with valid token
- Visual: brief flash of button returning, then navigation

**Loading_auth → Error**
- Trigger: API returns HTTP 401, 503, or network exception
- Visual: spinner fades out, button returns, ErrorBanner slides in

**Error → Content**
- Trigger: User begins typing (OnUsernameChange or OnPasswordChange)
- Visual: ErrorBanner slides out, fields re-enabled

**Content → Pin_mode**
- Trigger: OnTogglePinMode (isPinMode toggled to true)
- Visual: password fields fade+slide out, PinPad fades+slides in

**Pin_mode → Content**
- Trigger: OnTogglePinMode (isPinMode toggled to false)
- Visual: PinPad fades+slides out, password fields fade+slides in

**BiometricPrompt → Content**
- Trigger: Biometric authentication fails or user cancels
- Visual: OS sheet dismisses, screen returns to content

**BiometricPrompt → Success**
- Trigger: Biometric authentication succeeds
- Visual: Navigate to appropriate dashboard

---

## Appendix B — i18n String Table (Authentication Feature)

All strings used in the authentication feature. Strings are keyed by i18n key. Default locale: English (en). Additional locales: Swahili (sw), French (fr), Hindi (hi).

### ClientTypeSelectorScreen strings

| Key | English | Swahili | French |
|-----|---------|---------|--------|
| subtitle | "Your community savings group" | "Kikundi chako cha akiba" | "Votre groupe d'épargne communautaire" |
| admin_tile_label | "I manage a group" | "Nasimamia kikundi" | "Je gère un groupe" |
| admin_tile_sublabel | "Treasurer · Chairperson · Field Officer" | "Mweka hazina · Mwenyekiti · Afisa Uwanjani" | "Trésorier · Président · Agent de terrain" |
| member_tile_label | "I'm a group member" | "Mimi ni mwanachama" | "Je suis membre du groupe" |
| member_tile_sublabel | "Check savings · Request loans" | "Angalia akiba · Omba mkopo" | "Vérifier les économies · Demander un prêt" |
| version_prefix | "Version" | "Toleo" | "Version" |

### LoginScreen strings

| Key | English | Swahili | French |
|-----|---------|---------|--------|
| admin_login_title | "Staff Login" | "Kuingia kwa Wafanyakazi" | "Connexion Personnel" |
| member_login_title | "Member Login" | "Kuingia kwa Mwanachama" | "Connexion Membre" |
| username_label | "Username" | "Jina la mtumiaji" | "Nom d'utilisateur" |
| username_placeholder | "Enter your username" | "Ingiza jina lako la mtumiaji" | "Entrez votre nom d'utilisateur" |
| password_label | "Password" | "Nenosiri" | "Mot de passe" |
| password_placeholder | "Enter your password" | "Ingiza nenosiri lako" | "Entrez votre mot de passe" |
| use_pin_instead | "Use PIN instead" | "Tumia PIN badala yake" | "Utiliser le code PIN" |
| use_password_instead | "Use password instead" | "Tumia nenosiri badala yake" | "Utiliser le mot de passe" |
| login_button | "Login" | "Ingia" | "Se connecter" |
| error_invalid_credentials | "Incorrect username or password. Please try again." | "Jina la mtumiaji au nenosiri si sahihi. Jaribu tena." | "Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer." |
| error_network | "No internet connection. Login with your PIN." | "Hakuna muunganisho wa intaneti. Ingia kwa PIN yako." | "Pas de connexion internet. Connectez-vous avec votre code PIN." |
| error_server | "Server error. Please try again later." | "Hitilafu ya seva. Tafadhali jaribu tena baadaye." | "Erreur de serveur. Veuillez réessayer plus tard." |
| error_pin_not_set | "PIN not set up. Please login with your password first." | "PIN haijawekwa. Tafadhali ingia na nenosiri lako kwanza." | "Code PIN non configuré. Veuillez d'abord vous connecter avec votre mot de passe." |
| error_biometric_failed | "Biometric not recognised. Try again or use your password." | "Biometriki haikutambuliwa. Jaribu tena au tumia nenosiri lako." | "Biométrique non reconnu. Réessayez ou utilisez votre mot de passe." |

---

## Appendix C — Security Considerations for Authentication UI

### Password Field Security

- VisualTransformation applied by default; user must explicitly toggle visibility
- Password text is never written to clipboard automatically
- Password field does NOT support paste from clipboard in PIN mode (PIN is numeric only)
- Password field: autofill supported via `AutofillType.Password` hint
- Biometric hardware keystore used for PIN hash storage (Android Keystore API)

### PIN Storage

- PIN is hashed using PBKDF2 with HMAC-SHA256
- Salt: 16 bytes random per-device, stored in EncryptedSharedPreferences
- Iterations: 10,000
- Hash result stored in Android Keystore-backed EncryptedSharedPreferences
- PIN is never transmitted over network
- PIN cleared on logout, app uninstall, or password change

### Session Token Storage

- base64EncodedAuthenticationKey stored in EncryptedSharedPreferences
- Android Keystore AES-256-GCM encryption
- Token cleared on logout
- Token has no server-side expiry in Fineract community edition; app enforces 7-day local expiry

### Biometric Binding

- Biometric authentication is bound to the PIN hash (requires PIN to be set first)
- BiometricPrompt uses CryptoObject with SecretKey from Android Keystore
- Key invalidated on: new biometric enrolled, all biometrics removed, device factory reset
- BiometricManager.canAuthenticate(BIOMETRIC_STRONG) required (not BIOMETRIC_WEAK)

### Network Security

- All API calls use HTTPS (TLS 1.2+)
- Certificate pinning enforced for production Fineract host
- Credentials never logged (logcat or analytics)
- Analytics events never include credentials, only client_type and error_type

---

## Appendix D — Testing Scenarios for Authentication

### UI Automation Test Cases

| Test ID | Screen | Scenario | Expected Result |
|---------|--------|----------|----------------|
| AUTH-UI-001 | ClientTypeSelector | App launched with no saved session | ClientTypeSelectorScreen shown with both tiles |
| AUTH-UI-002 | ClientTypeSelector | Tap AdminTile | Navigate to LoginScreen with clientType=ADMIN |
| AUTH-UI-003 | ClientTypeSelector | Tap MemberTile | Navigate to LoginScreen with clientType=END_USER |
| AUTH-UI-004 | LoginScreen | Admin screen loaded | Title shows "Staff Login" |
| AUTH-UI-005 | LoginScreen | Member screen loaded | Title shows "Member Login" |
| AUTH-UI-006 | LoginScreen | Type in username field | State.username updates; LoginButton remains disabled |
| AUTH-UI-007 | LoginScreen | Fill both username and password | LoginButton becomes enabled |
| AUTH-UI-008 | LoginScreen | Tap Login with valid credentials | Loading indicator shown; navigation fires |
| AUTH-UI-009 | LoginScreen | Tap Login with wrong password | ErrorBanner shows InvalidCredentials message |
| AUTH-UI-010 | LoginScreen | Tap eye icon in password field | Password text revealed; icon changes |
| AUTH-UI-011 | LoginScreen | Tap "Use PIN instead" | PinPad appears; username/password fields hidden |
| AUTH-UI-012 | LoginScreen | Tap "Use password instead" | PinPad hidden; username/password fields return |
| AUTH-UI-013 | LoginScreen | Enter 4 PIN digits | Auto-submit triggered after 200ms delay |
| AUTH-UI-014 | LoginScreen | Enter wrong PIN | Dots shake; all dots cleared; ErrorBanner shown |
| AUTH-UI-015 | LoginScreen | Biometric button shown | Only visible when isBiometricAvailable = true |
| AUTH-UI-016 | LoginScreen | Tap back arrow | Navigate back to ClientTypeSelectorScreen |
| AUTH-UI-017 | LoginScreen | Start typing after error | ErrorBanner dismisses automatically |
| AUTH-UI-018 | LoginScreen | Network offline + tap Login | ErrorBanner shows network error; PIN mode suggested |

### ViewModel Unit Test Cases

| Test ID | ViewModel | Scenario | Expected State |
|---------|-----------|----------|---------------|
| AUTH-VM-001 | LoginViewModel | OnUsernameChange("grace") | state.username = "grace" |
| AUTH-VM-002 | LoginViewModel | OnPasswordChange("secret") | state.password = "secret" |
| AUTH-VM-003 | LoginViewModel | Both fields non-empty | isFormValid would enable login (validation computed in UI) |
| AUTH-VM-004 | LoginViewModel | OnTogglePinMode | state.isPinMode toggles |
| AUTH-VM-005 | LoginViewModel | OnPinChange("1") + OnPinChange("2") + OnPinChange("3") + OnPinChange("4") | state.pin = "1234"; OnPinSubmit triggered |
| AUTH-VM-006 | LoginViewModel | Successful admin auth | Event NavigateToAdminDashboard emitted with userId + roles |
| AUTH-VM-007 | LoginViewModel | Successful end_user auth | Event NavigateToEndUserDashboard emitted with clientId + token |
| AUTH-VM-008 | LoginViewModel | 401 response | state.error = LoginError.InvalidCredentials |
| AUTH-VM-009 | LoginViewModel | 503 response | state.error = LoginError.Server |
| AUTH-VM-010 | LoginViewModel | Network exception | state.error = LoginError.Network |
