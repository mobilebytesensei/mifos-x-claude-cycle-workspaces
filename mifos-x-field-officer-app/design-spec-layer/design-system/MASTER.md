# template_meta
# template_version: "2.84.0"
# template_path: "workspaces/mifos-x/mifos-x-field-officer-app/design-spec-layer/design-system/MASTER.md"
# last_modified: "2026-03-20"

# Mifos X Field Officer App - Design System

> **Version**: 1.0.0
> **Generated**: 2026-03-13
> **Category**: Banking/Finance
> **Pattern**: Trust + Clarity
> **Framework**: Material Design 3
> **Platform**: Compose Multiplatform (Android, iOS, Desktop, Web)
> **WCAG Compliance**: AA (4.5:1 text, 3:1 UI elements)

---

## Overview

The Mifos X Field Officer App design system is built for **trust, clarity, and efficiency** in financial field operations. Field officers manage client portfolios, loan disbursements, repayment collections, and center coordination - often in low-connectivity environments. The design language prioritizes legibility, clear data hierarchy, and confident interactions.

**Seed Color**: `#1565C0` - Professional Blue communicates trust, reliability, and institutional credibility - core values for a banking/microfinance application.

**Design Principles**:
1. **Trust First** - Every interaction must feel secure and deliberate. Destructive or financial actions require confirmation.
2. **Data Clarity** - Financial data (amounts, dates, IDs) must be unambiguous. Use consistent formatting.
3. **Offline Resilience** - Always show sync status. Gracefully handle offline/online transitions.
4. **Field-Ready** - Large touch targets, high contrast, readable in bright sunlight.
5. **Efficiency** - Common actions (collect payment, view client) must be accessible within 2 taps.

---

## Color System (Material Design 3)

**Seed Color**: `#1565C0` (Professional Blue)
**Tonal Palette Source**: M3 HCT color space derivation from seed

### Light Theme

| Role | Hex | Usage |
|------|-----|-------|
| `primary` | `#1B5EA6` | Primary actions, key UI elements, active states |
| `onPrimary` | `#FFFFFF` | Text/icons on primary color |
| `primaryContainer` | `#D6E3FF` | Subtler primary backgrounds, chips, selected states |
| `onPrimaryContainer` | `#001A41` | Text/icons on primary container |
| `secondary` | `#1B6073` | Secondary actions, complementary accents |
| `onSecondary` | `#FFFFFF` | Text/icons on secondary color |
| `secondaryContainer` | `#BDE9F9` | Secondary tonal backgrounds |
| `onSecondaryContainer` | `#001F28` | Text/icons on secondary container |
| `tertiary` | `#006A4E` | Success states, approved loans, positive indicators |
| `onTertiary` | `#FFFFFF` | Text/icons on tertiary color |
| `tertiaryContainer` | `#89F8CF` | Success/approved backgrounds |
| `onTertiaryContainer` | `#002116` | Text/icons on tertiary container |
| `error` | `#BA1A1A` | Errors, overdue loans, rejected states |
| `onError` | `#FFFFFF` | Text/icons on error color |
| `errorContainer` | `#FFDAD6` | Error backgrounds, overdue indicators |
| `onErrorContainer` | `#410002` | Text/icons on error container |
| `background` | `#F8F9FF` | App background |
| `onBackground` | `#191C20` | Primary text on background |
| `surface` | `#F8F9FF` | Card and sheet surfaces |
| `onSurface` | `#191C20` | Primary content on surfaces |
| `surfaceVariant` | `#E0E2EC` | Alternative surface backgrounds |
| `onSurfaceVariant` | `#44474F` | Secondary text, icons on surface variant |
| `outline` | `#74777F` | Borders, dividers, text field outlines |
| `outlineVariant` | `#C4C6CF` | Subtle dividers, disabled borders |
| `inverseSurface` | `#2E3036` | Snackbar backgrounds |
| `inverseOnSurface` | `#EFF0F7` | Snackbar text |
| `inversePrimary` | `#A8C8FF` | Snackbar actions, inverse primary uses |
| `scrim` | `#000000` | Modal scrims (at 32% opacity) |
| `shadow` | `#000000` | Component shadows |

### Dark Theme

| Role | Hex | Usage |
|------|-----|-------|
| `primary` | `#A8C8FF` | Primary actions in dark mode |
| `onPrimary` | `#00316B` | Text/icons on dark mode primary |
| `primaryContainer` | `#164895` | Dark primary container backgrounds |
| `onPrimaryContainer` | `#D6E3FF` | Text/icons on dark primary container |
| `secondary` | `#91CDE1` | Secondary actions in dark mode |
| `onSecondary` | `#003544` | Text/icons on dark secondary |
| `secondaryContainer` | `#004D61` | Dark secondary container backgrounds |
| `onSecondaryContainer` | `#BDE9F9` | Text/icons on dark secondary container |
| `tertiary` | `#6CDBAD` | Success/approved states in dark mode |
| `onTertiary` | `#003828` | Text/icons on dark tertiary |
| `tertiaryContainer` | `#00513B` | Dark success container backgrounds |
| `onTertiaryContainer` | `#89F8CF` | Text/icons on dark tertiary container |
| `error` | `#FFB4AB` | Errors in dark mode |
| `onError` | `#690005` | Text/icons on dark error |
| `errorContainer` | `#93000A` | Dark error container backgrounds |
| `onErrorContainer` | `#FFDAD6` | Text/icons on dark error container |
| `background` | `#111318` | Dark app background |
| `onBackground` | `#E1E2E9` | Primary text on dark background |
| `surface` | `#111318` | Dark card and sheet surfaces |
| `onSurface` | `#E1E2E9` | Primary content on dark surfaces |
| `surfaceVariant` | `#44474F` | Dark alternative surface backgrounds |
| `onSurfaceVariant` | `#C4C6CF` | Secondary text/icons in dark mode |
| `outline` | `#8E9099` | Dark borders and dividers |
| `outlineVariant` | `#44474F` | Subtle dark dividers |
| `inverseSurface` | `#E1E2E9` | Dark snackbar backgrounds |
| `inverseOnSurface` | `#2E3036` | Dark snackbar text |
| `inversePrimary` | `#1B5EA6` | Dark inverse primary |
| `scrim` | `#000000` | Modal scrims |
| `shadow` | `#000000` | Component shadows |

### Semantic Color Usage (Banking Context)

| Semantic | Light Hex | Dark Hex | Usage |
|----------|-----------|----------|-------|
| Approved/Success | `#006A4E` (tertiary) | `#6CDBAD` | Approved loans, successful payments |
| Pending | `#6B5E0D` (custom warning) | `#DFBE02` | Pending approvals, processing states |
| Overdue/Error | `#BA1A1A` (error) | `#FFB4AB` | Overdue loans, missed payments |
| Active | `#1B5EA6` (primary) | `#A8C8FF` | Active clients, active loans |
| Inactive | `#74777F` (outline) | `#8E9099` | Inactive/closed accounts |

---

## Typography Scale (Inter)

All type uses **Inter** - a clean, professional sans-serif optimized for screen readability.

| Style | Size | Weight | Line Height | Letter Spacing | Use Case |
|-------|------|--------|-------------|----------------|----------|
| `displayLarge` | 57sp | 400 | 64sp | -0.25sp | Hero headers, splash screens |
| `displayMedium` | 45sp | 400 | 52sp | 0sp | Large feature titles |
| `displaySmall` | 36sp | 400 | 44sp | 0sp | Section display text |
| `headlineLarge` | 32sp | 400 | 40sp | 0sp | Screen titles, dashboard headers |
| `headlineMedium` | 28sp | 400 | 36sp | 0sp | Section headings, dialog titles |
| `headlineSmall` | 24sp | 400 | 32sp | 0sp | Card headings, list section headers |
| `titleLarge` | 22sp | 500 | 28sp | 0sp | Top app bar title, modal titles |
| `titleMedium` | 16sp | 500 | 24sp | 0.15sp | List primary text, card titles |
| `titleSmall` | 14sp | 500 | 20sp | 0.1sp | Subtitle text, secondary card headers |
| `bodyLarge` | 16sp | 400 | 24sp | 0.5sp | Primary body, form fields, descriptions |
| `bodyMedium` | 14sp | 400 | 20sp | 0.25sp | Secondary body, loan details, client info |
| `bodySmall` | 12sp | 400 | 16sp | 0.4sp | Captions, timestamps, helper text |
| `labelLarge` | 14sp | 500 | 20sp | 0.1sp | Button text, tab labels, chip labels |
| `labelMedium` | 12sp | 500 | 16sp | 0.5sp | Badge text, navigation labels |
| `labelSmall` | 11sp | 500 | 16sp | 0.5sp | Overlines, status indicators, micro-labels |

### Typography Rules

- **Minimum font size**: 12sp (bodySmall) for any visible UI text
- **Financial amounts**: Use `titleMedium` or `headlineSmall` with `500` weight for currency display
- **Status labels**: Use `labelSmall` (uppercase) for status chips
- **Form labels**: Use `bodySmall` for helper text, `bodyLarge` for input values
- **Never** mix more than 3 type styles within a single card component

---

## Spacing and Layout (8dp Grid)

All spacing values are multiples of the **8dp base grid unit**.

| Token | Value | Use Case |
|-------|-------|----------|
| `xs` | 4dp | Icon internal padding, dense list separators |
| `sm` | 8dp | Icon-to-text gap, chip padding, compact spacing |
| `md` | 16dp | Standard horizontal screen padding, card internal padding |
| `lg` | 24dp | Section spacing, between major content groups |
| `xl` | 32dp | Large section breaks, hero spacing |
| `xxl` | 48dp | Full-screen padding, dramatic section spacing |

### Layout Rules

- **Screen horizontal padding**: 16dp on all screens
- **Card internal padding**: 16dp
- **List item height**: 56dp minimum (standard), 72dp (with subtitle), 88dp (with three lines)
- **Section header spacing**: 24dp above, 8dp below
- **Bottom navigation height**: 80dp (56dp bar + 24dp safe area)
- **Top app bar height**: 64dp (compact), 112dp (medium), 152dp (large)
- **FAB margin from edge**: 16dp

---

## Corner Radius

| Token | Value | Applied To |
|-------|-------|------------|
| `none` | 0dp | Top app bar, navigation bar, full-bleed images |
| `xs` | 4dp | Text field containers, dense chips |
| `sm` | 8dp | Chips, badges, filter pills, small cards |
| `md` | 12dp | Standard cards, client/loan cards, tiles |
| `lg` | 16dp | Modal bottom sheets (top corners only), search bar |
| `xl` | 28dp | Dialogs, large modal surfaces |
| `full` | 9999dp | Buttons (filled/outlined/text), FAB, avatar chips |

---

## Elevation System

M3 uses tonal color overlays (not just drop shadows) to communicate elevation in light mode.

| Level | Value | Applied To |
|-------|-------|------------|
| `level0` | 0dp | Flat surfaces, cards at rest, navigation bar |
| `level1` | 1dp | Elevated cards, dropdown menus, bottom sheets |
| `level2` | 3dp | Top app bar (on scroll), navigation drawer, raised FAB |
| `level3` | 6dp | Dialogs, date pickers, time pickers, floating FAB |
| `level4` | 8dp | Navigation rail (expanded), persistent search bar |
| `level5` | 12dp | Top app bar (prominent), side navigation rail |

---

## Touch Targets

All interactive elements must meet WCAG 2.1 SC 2.5.8 (minimum 24x24dp visual, 48x48dp touch).

| Element | Touch Target | Notes |
|---------|-------------|-------|
| Icon buttons | 48x48dp | Always use 48dp touch target even for 24dp icons |
| Text buttons | 40dp height, full width | Minimum |
| Filled buttons | 40dp height | Standard |
| Extended FAB | 56dp height | Minimum |
| Navigation items | 56dp height | Full bottom nav item |
| List items | 56dp height | Standard; 72dp with subtitle |
| Chips | 32dp height, 48dp min width | Tappable area padded to 48dp |
| Checkboxes | 48x48dp touch | 20dp visual |
| Radio buttons | 48x48dp touch | 20dp visual |
| Switch | 48x32dp touch | 52x32dp visual |

**Field Officer Consideration**: Officers may use apps with gloves or in bright sunlight. Prefer 56dp+ touch targets for primary actions.

---

## Icon Library

**Library**: FluentUI System Icons
**Package**: `dev.niyajali.fluentui.icons`

| Size Token | Value | Use Case |
|-----------|-------|----------|
| Small | 20dp | Inline icons, chip icons, dense lists |
| Default | 24dp | Standard UI icons, navigation icons |
| Large | 32dp | Feature icons, empty state illustrations |

### Banking-Specific Icon Set

| Icon Name | FluentUI Token | Usage |
|-----------|---------------|-------|
| Clients | `Person24Regular` | Client list, client management |
| Loans | `Money24Regular` | Loan management, disbursements |
| Collections | `WalletCreditCard24Regular` | Payment collection |
| Centers | `BuildingBank24Regular` | Center/group management |
| Search | `Search24Regular` | Search bar |
| Filter | `Filter24Regular` | Filter/sort |
| Add New | `Add24Regular` | FAB, create actions |
| Edit | `Edit24Regular` | Edit client/loan data |
| Delete | `Delete24Regular` | Delete (destructive - show with error color) |
| Sync | `ArrowSync24Regular` | Offline/online sync status |
| Offline | `CloudOff24Regular` | Offline indicator |
| Online | `CloudCheckmark24Regular` | Online/synced indicator |
| Calendar | `Calendar24Regular` | Due dates, schedules |
| Location | `Location24Regular` | Client location, center location |
| Phone | `Phone24Regular` | Client contact |
| Document | `Document24Regular` | Loan documents, forms |
| Settings | `Settings24Regular` | App settings |
| Sign Out | `SignOut24Regular` | Logout |
| Warning | `Warning24Regular` | Overdue alerts, caution states |
| Check | `Checkmark24Regular` | Success confirmation, approved state |
| Error | `ErrorCircle24Regular` | Error states, failed operations |

---

## Accessibility Guidelines

### Color Contrast (WCAG AA)

| Pair | Ratio | Standard |
|------|-------|----------|
| `onPrimary` on `primary` | 9.1:1 | Exceeds AA (4.5:1) |
| `onBackground` on `background` | 14.2:1 | Exceeds AA |
| `onSurface` on `surface` | 14.2:1 | Exceeds AA |
| `onSurfaceVariant` on `surfaceVariant` | 5.1:1 | Passes AA |
| `outline` on `background` | 4.6:1 | Passes AA |
| Dark: `primary` on `background` | 5.2:1 | Passes AA |
| Dark: `onSurfaceVariant` on `surfaceVariant` | 4.6:1 | Passes AA |

### Accessibility Checklist

- All text meets 4.5:1 contrast ratio against its background
- All UI components (buttons, inputs, icons) meet 3:1 contrast
- Touch targets are minimum 48x48dp for all interactive elements
- Focusable elements have visible focus indicators (primary color outline)
- Form fields have visible labels (never placeholder-only)
- Financial amounts use both color and icon/text to convey status (not color alone)
- Error messages are descriptive and appear near the field in error
- Screen transitions are under 400ms to avoid disorientation
- All images/icons have content descriptions for screen readers
- Loading states use skeleton screens (not indefinite spinners for content loads)

### Color-Independent Status Communication

Never rely on color alone for status. Always pair color with:
- An icon (checkmark for approved, warning for pending, X for error)
- A text label ("Approved", "Pending", "Overdue")
- A shape or pattern difference when possible

---

## Banking/Finance UI Guidelines

### Amount Display

- Always show currency symbol: `USD 1,250.00` or `$1,250.00`
- Use `headlineSmall` or `titleMedium` weight 500 for prominent amounts
- Negative amounts: Use `error` color + minus sign prefix
- Large amounts: Use comma separators (1,000,000.00)
- Loan balance vs. amount due: Use visual hierarchy to differentiate

### Sensitive Data Handling

- Loan IDs: Display with `#` prefix in `labelMedium` style
- Client account numbers: Show last 4 digits with masking where appropriate
- National IDs: Never display in full on list views - show `***-***-XXXX` pattern

### Financial Status Color Coding

| Status | Color Token | Text Label | Icon |
|--------|-------------|------------|------|
| Active | `primary` | "Active" | Filled circle |
| Approved | `tertiary` | "Approved" | Checkmark |
| Pending | Warning amber | "Pending" | Clock icon |
| Overdue | `error` | "Overdue" | Warning triangle |
| Closed | `onSurfaceVariant` | "Closed" | Minus circle |
| Write-off | `error` container | "Written Off" | X circle |

### Offline/Sync State Communication

Field officers frequently operate in areas with poor connectivity. The app must:

1. Show a persistent sync indicator in the top app bar (cloud icon with status)
2. Display "Last synced: [time]" in the dashboard header
3. Differentiate between locally-saved (pending sync) and server-confirmed data with a subtle indicator
4. Queue all offline actions and show a count badge on the sync button
5. Auto-sync when connectivity is restored (with a brief snackbar notification)

### List Density

Field officers view many clients/loans per session. Use **standard** density (not compact) to maintain touch target sizes, but optimize information density within each list item:

- Primary line: Client name + Loan ID
- Secondary line: Amount due + Due date
- Trailing: Status chip

---

## Dark Mode Guidelines

The app supports both light and dark themes following M3 dark theme specifications:

1. Background shifts from `#F8F9FF` to `#111318` (not pure black)
2. Elevation is expressed via lighter surface tones (level1 = `surfaceContainerLow`)
3. Primary color brightens from `#1B5EA6` to `#A8C8FF` for legibility on dark backgrounds
4. Container colors invert: light containers become dark containers
5. Shadows are less visible; rely on tonal surface differentiation

**Auto-detect system preference** via `isSystemInDarkTheme()` in Compose. Provide a manual override in Settings.

---

## Motion and Animation

| Type | Duration | Easing | Use Case |
|------|----------|--------|----------|
| Quick response | 100ms | Standard | Button state changes, toggle |
| Short transition | 200ms | Emphasized | Chip selection, icon swap |
| Medium transition | 300ms | Emphasized | Screen enter/exit, card expand |
| Long transition | 400ms | Emphasized decelerate | Modal appear, bottom sheet rise |
| Exit | 200ms | Emphasized accelerate | Dismiss, close |

**Financial confirmation actions** (payment submission, loan approval) should use a brief 100ms haptic + visual ripple to confirm the action was registered.

---

## Platform Adaptations

| Platform | Adaptations |
|----------|------------|
| Android | Use Material 3 Compose components natively; NavigationBar for bottom nav |
| iOS | Adapt M3 colors/spacing; use platform back gesture; NavigationBar translucency |
| Desktop | Expand to NavigationRail for side navigation; wider cards in grid layout |
| Web | Responsive breakpoints: compact (<600dp), medium (600-1199dp), expanded (1200dp+) |

---

## Anti-Patterns (Do NOT Use)

- Never use red (#FF0000) or pure green (#00FF00) as primary brand colors
- Never use white text on `primaryContainer` (#D6E3FF) - fails WCAG contrast
- Never use less than 48dp touch targets for any interactive element
- Never display raw unformatted numeric IDs or account numbers
- Never use pure black (#000000) or pure white (#FFFFFF) as surface colors
- Never skip loading/offline states - field officers work in variable connectivity
- Never use more than 3 primary colors in a single screen composition
- Never use font sizes below 12sp for any user-facing text
- Never use color alone to convey financial status (always pair with text/icon)
- Never auto-submit financial forms - always require explicit confirmation

---

## File Structure

```
design-system/
├── MASTER.md                    (this file - human-readable guide)
├── COMPONENTS.md                (component specifications)
├── design-tokens.json           (machine-readable tokens)
├── design-tokens.v1.0.0.json   (versioned copy)
├── CHANGELOG.md                 (version history)
└── pages/                       (page-specific overrides)
    └── .gitkeep
```
