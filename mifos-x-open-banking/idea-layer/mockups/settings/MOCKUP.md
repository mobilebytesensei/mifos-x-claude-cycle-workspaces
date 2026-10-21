# MOCKUP — Settings

| Field   | Value    |
|---------|----------|
| Feature | settings |
| Flavor  | shared   |

---

## Screen Layout

The settings screen is a scrollable column on a `surface_container` background, padded `spacing.lg` (24 dp) on all sides. It is organized into four cards stacked vertically:

1. **Appearance card** — Dark Mode toggle row + Language select row
2. **Notifications card** — Push Notifications toggle + Transaction Alerts toggle
3. **Security card** — Biometric Login toggle
4. **About card** — About Mifos X link + App Version display row

Each card uses border-radius `radius.md`, padding `spacing.md` (16 dp), and margin-bottom `spacing.md`, separated by the background gap between cards.

---

## Components

### Appearance Card

**settings_appearance_group**
- Card on `surface`, border-radius `radius.md`, padding `spacing.md`, margin-bottom `spacing.md`

**settings_appearance_header**
- Content: "Appearance"
- Style: `titleMedium` (16 sp, 500 weight, Roboto), color `primary`, padding-bottom `spacing.sm` (8 dp)

**settings_dark_mode_row**
- Horizontal row: label group (left, flex) + switch (right)
- Label: "Dark Mode" (`bodyLarge`, `on_surface`)
- Description: "Switch to a darker color scheme" (`bodySmall`, `on_surface_variant`)
- Switch: active track `primary` / inactive track `outline`; prefilled from `isDarkModeEnabled`

**settings_divider_1**
- Thin horizontal rule, color `outline`, margin-top and margin-bottom `spacing.xs` (4 dp)

**settings_language_row**
- Horizontal row: label group (left, flex) + combobox select (right)
- Label: "Language" (`bodyLarge`, `on_surface`)
- Description: "Choose your preferred display language" (`bodySmall`, `on_surface_variant`)
- Select: min-width 140 dp, options: English / Spanish / French / Hindi / Arabic; prefilled from `selectedLanguage` (default="en")

---

### Notifications Card

**settings_notifications_group**
- Card on `surface`, border-radius `radius.md`, padding `spacing.md`, margin-bottom `spacing.md`

**settings_notifications_header**
- Content: "Notifications"
- Style: `titleMedium`, color `primary`

**settings_push_notifications_row**
- Label: "Push Notifications" (`bodyLarge`, `on_surface`)
- Description: "Receive alerts and updates from Mifos X" (`bodySmall`, `on_surface_variant`)
- Switch: active track `primary`; prefilled from `isPushNotificationsEnabled` (default=true)

**settings_divider_2**
- Thin horizontal rule, color `outline`

**settings_transaction_alerts_row**
- Label: "Transaction Alerts" (`bodyLarge`, `on_surface`)
- Description: "Notify me for every debit and credit activity" (`bodySmall`, `on_surface_variant`)
- Switch: active track `primary`; indented one step and disabled at `opacity.disabled` when `!isPushNotificationsEnabled`

---

### Security Card

**settings_security_group**
- Card on `surface`, border-radius `radius.md`, padding `spacing.md`, margin-bottom `spacing.md`

**settings_security_header**
- Content: "Security"
- Style: `titleMedium`, color `primary`

**settings_biometric_row**
- Label: "Biometric Login" (`bodyLarge`, `on_surface`)
- Description: "Use fingerprint or face ID to sign in faster" (`bodySmall`, `on_surface_variant`)
- Switch: active track `primary`; disabled at `opacity.disabled` when `!isBiometricAvailableOnDevice` (device capability check)

---

### About Card

**settings_about_group**
- Card on `surface`, border-radius `radius.md`, padding `spacing.md`, margin-bottom `spacing.md`

**settings_about_header**
- Content: "About"
- Style: `titleMedium`, color `primary`

**settings_about_link_row**
- Horizontal row: "About Mifos X Open Banking" link (`bodyLarge`, `on_surface`, flex) + chevron_right icon (`icon.sm`, `on_surface_variant`)
- Full row is tappable; navigates to `about` screen

**settings_divider_3**
- Thin horizontal rule, color `outline`

**settings_app_version_row**
- Horizontal row: "App Version" label (`bodyLarge`, `on_surface`) + "v1.0.0" value (`bodySmall`, `on_surface_variant`)
- Not tappable (display only)

---

## Interaction Patterns

| Element                         | Gesture | Outcome                                                                         |
|---------------------------------|---------|---------------------------------------------------------------------------------|
| settings_dark_mode_toggle       | Toggle  | `onDarkModeToggled()` → DataStore write → app-wide theme recomposition          |
| settings_language_select        | Tap     | Opens dropdown with 5 language options; `onLanguageSelected(language)` → LocaleManager update |
| settings_push_notifications_toggle| Toggle| `onPushNotificationsToggled()` → DataStore; if false, disables transaction alerts switch |
| settings_transaction_alerts_toggle| Toggle| `onTransactionAlertsToggled()` → DataStore; only active when push is enabled   |
| settings_biometric_toggle       | Toggle  | `onBiometricToggled()` → BiometricManager enrollment flow if enabling for first time |
| settings_about_link_row         | Tap     | Navigates to `about` screen                                                     |
| settings_app_version_row        | None    | Display only — no interaction                                                   |

**Cascade behavior:**
- Disabling Push Notifications immediately dims and disables the Transaction Alerts switch. Re-enabling Push Notifications restores the Transaction Alerts switch to its last persisted state.

**Loading state:**
- On screen entry, skeleton shimmer cards replace all four preference cards while DataStore values are read. Once loaded, the shimmer dissolves (crossfade) and actual preference values are shown.

---

## Content Data

| Component                          | Content Value                                      |
|------------------------------------|----------------------------------------------------|
| settings_appearance_header         | "Appearance"                                       |
| settings_dark_mode_label           | "Dark Mode"                                        |
| settings_dark_mode_description     | "Switch to a darker color scheme"                  |
| settings_language_label            | "Language"                                         |
| settings_language_description      | "Choose your preferred display language"           |
| settings_language_select options   | English (en), Spanish (es), French (fr), Hindi (hi), Arabic (ar) |
| settings_notifications_header      | "Notifications"                                    |
| settings_push_notifications_label  | "Push Notifications"                               |
| settings_push_notifications_desc   | "Receive alerts and updates from Mifos X"          |
| settings_transaction_alerts_label  | "Transaction Alerts"                               |
| settings_transaction_alerts_desc   | "Notify me for every debit and credit activity"    |
| settings_security_header           | "Security"                                         |
| settings_biometric_label           | "Biometric Login"                                  |
| settings_biometric_description     | "Use fingerprint or face ID to sign in faster"     |
| settings_about_header              | "About"                                            |
| settings_about_link                | "About Mifos X Open Banking"                       |
| settings_app_version_label         | "App Version"                                      |
| settings_app_version_value         | "v1.0.0"                                           |

---

## Design Notes

**Color usage:**
- All section headers use `primary` — creating consistent visual grouping anchors throughout the scroll.
- **Every switch shares the same `primary` active track.** The Transaction Alerts toggle previously used a teal accent to signal that it is subordinate to the master Push Notifications switch. Teal is not a family this palette ships, and more importantly a different colour is the wrong tool for that job: subordination is now shown structurally — the row is indented one step beneath its parent and physically dims to `opacity.disabled` when the parent is off. That is a state a screen reader can announce; a hue is not.
- `outline` on inactive switch tracks, dividers, and the chevron icon provides a uniform passive tone.

**Typography:**
- Consistent `titleMedium` for all section headers — the 500 weight distinguishes it from row labels without requiring a colour change.
- `bodyLarge` for row labels provides good legibility in list contexts.
- `bodySmall` for descriptions creates a clear two-level text hierarchy within each row.
- Roboto throughout, per `typography.font_family`.

**Spacing:**
- Cards use `radius.md`, aligned with the MD3 medium-component shape spec.
- Row padding-top/bottom `spacing.sm` (8 dp) creates comfortable touch targets while keeping the list dense enough to show multiple settings without excessive scrolling.
- Dividers use `spacing.xs` (4 dp) top and bottom margins for minimal visual weight while still providing clear row separation.

**Accessibility:**
- All switch components have role=switch with explicit label strings.
- The Transaction Alerts switch conveys its disabled state through opacity and the `disabled_when` property — screen readers announce "dimmed" or "unavailable" to communicate the conditional state, so the parent/child relationship never depends on colour.
- The Language select has role=combobox, allowing screen readers to announce the current selected language and available options.
- The chevron icon on the About row has an empty label (decorative) — the link label "Navigate to About Mifos X Open Banking" carries the full accessible meaning.
- All row labels in the About section use meaningful non-generic text.

---

_Generated by /idea export | 2026-08-03_
