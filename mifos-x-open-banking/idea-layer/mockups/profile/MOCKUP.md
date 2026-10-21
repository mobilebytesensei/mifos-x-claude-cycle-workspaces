# MOCKUP — User Profile

| Field   | Value   |
|---------|---------|
| Feature | profile |
| Flavor  | shared  |

---

## Screen Layout

The profile screen is a scrollable column on a `surfaceContainerLow` background, padded `spacing.lg` (24 dp) on all sides. It is divided into four distinct visual sections from top to bottom:

1. **Avatar section** — centered column with circular avatar, overlaid edit icon, and display name
2. **Personal Information card** — card with three editable input fields
3. **Action section** — Save Changes (filled) + Change Password (outlined) buttons
4. **Danger section** — card containing the Log Out text button

---

## Components

### profile_avatar_section
- **Description:** Centered column containing the user's avatar, an edit badge, and their display name
- **Position:** Top of screen, below top app bar
- **Style tokens:** alignment=center, padding-bottom `spacing.xl` (32 dp)

### profile_avatar_image
- **Description:** Circular portrait image `user_avatar_placeholder`; falls back to initials on placeholder background when no `avatarUrl` is set
- **Position:** Center-aligned in avatar section
- **Style tokens:** width/height 96 dp, border-color `primary`, border-width `border.medium`, background `primaryContainer` (placeholder), initials in `onPrimaryContainer`
- **Accessibility:** role=image, label="Your profile photo"

### profile_avatar_edit_icon
- **Description:** Circular badge icon `edit_photo` overlaid at the bottom-right of the avatar; tapping opens the photo picker
- **Position:** Offset relative to avatar bottom-right corner
- **Style tokens:** background `primary`, icon color `onPrimary`, size 28 dp
- **Accessibility:** role=button, label="Change profile photo"

### profile_display_name
- **Description:** Current user's full name rendered from `ProfileUiState.fullName`; sample value "Maria Santos"
- **Position:** Below avatar image; padding-top `spacing.sm` (8 dp)
- **Style tokens:** `headlineSmall` (24 sp, Roboto), color `primary`, alignment=center

### profile_form_section
- **Description:** Card with rounded corners containing the Personal Information section header and three input fields
- **Style tokens:** background `surfaceContainerLowest`, border-radius `radius.md`, padding `spacing.lg`, margin-bottom `spacing.md`

### profile_section_header
- **Content:** "Personal Information"
- **Style tokens:** `titleMedium` (16 sp, weight 500, Roboto), color `primary`, padding-bottom `spacing.md`

### profile_full_name_input
- **Description:** Outlined text field, label "Full Name", placeholder "e.g. Maria Santos"; pre-filled from `ProfileUiState.fullName`
- **Style tokens:** background `surfaceContainerLow`, `bodyLarge`, border `outline` (rest, `border.thin`) / `primary` (focused, `border.focus`), radius `radius.sm`, margin-bottom `spacing.md`
- **Behavior:** keyboard_type=text, ime_action=next

### profile_email_input
- **Description:** Email-type field, label "Email Address", placeholder "e.g. maria.santos@example.com"; pre-filled from `ProfileUiState.email`
- **Style tokens:** Same as full name input
- **Behavior:** keyboard_type=email, ime_action=next; validated against RFC-5322 on save

### profile_phone_input
- **Description:** Tel-type field, label "Phone Number", placeholder "e.g. +63 917 123 4567"; pre-filled from `ProfileUiState.phoneNumber`
- **Style tokens:** Same as other inputs (no margin-bottom — last field in card)
- **Behavior:** keyboard_type=tel, ime_action=done; validated for E.164 format on save

### profile_save_button
- **Description:** Full-width filled button "Save Changes"
- **Style tokens:** container `primary`, label `onPrimary`, `labelLarge`, border-radius `radius.sm`, margin-bottom `spacing.sm`
- **Behavior:** Disabled at `opacity.disabled` when `uiState==Viewing` or `!hasUnsavedChanges`; shows loading spinner when `uiState==Saving`

### profile_change_password_button
- **Description:** Full-width outlined button "Change Password"
- **Style tokens:** border `outline` (`border.thin`), text `primary`, `labelLarge`, border-radius `radius.sm`

### profile_save_success_banner
- **Description:** Confirmation card visible only in `saved` state
- **Position:** Top of scroll content, above avatar section, when visible
- **Style tokens:** background `primaryContainer`, border `primary` (`border.thin`), border-radius `radius.sm`, padding `spacing.md`
- **Content:** check_circle icon (`onPrimaryContainer`, `icon.sm`) + "Your profile has been updated successfully." (`bodySmall`, `onPrimaryContainer`)
- **Behavior:** Auto-transitions to `viewing` state after 2 seconds

### profile_danger_section
- **Description:** Card at the bottom of the form, visually isolated from the action section by margin-top
- **Style tokens:** background `surfaceContainerLowest`, border-radius `radius.md`, padding `spacing.lg`, margin-top `spacing.md`
- **Contents:** `profile_logout_button` only

### profile_logout_button
- **Description:** Full-width text-variant button "Log Out"
- **Style tokens:** `labelLarge`, color `error`, padding `spacing.md`
- **Behavior:** Clears session token via `SessionManager`, navigates to login

---

## Interaction Patterns

| Element                      | Gesture | Outcome                                                              |
|------------------------------|---------|----------------------------------------------------------------------|
| profile_avatar_edit_icon     | Tap     | Opens system photo picker (ACTION_PICK intent)                       |
| profile_full_name_input      | Focus   | Border turns `primary`; sets `hasUnsavedChanges=true` on text change |
| profile_email_input          | Focus   | Border turns `primary`; sets `hasUnsavedChanges=true` on text change |
| profile_phone_input          | Focus   | Border turns `primary`; sets `hasUnsavedChanges=true` on text change |
| profile_save_button          | Tap     | Fires `onSaveClicked()`; transitions to `saving` state              |
| profile_change_password_button| Tap    | Navigates to `change-password` screen                               |
| profile_logout_button        | Tap     | Shows confirmation dialog → `onLogoutClicked()` → navigate to login |
| profile_save_success_banner  | Auto   | Auto-dismisses after 2 s; screen transitions to `viewing`           |

**State transitions:**
- `viewing` → `editing` when any input value changes
- `editing` → `saving` on Save tapped
- `saving` → `saved` on API success
- `saving` → `error` on API failure
- `saved` → `viewing` after 2 s auto-timeout

---

## Content Data

| Component              | Sample Content Value                                   |
|------------------------|--------------------------------------------------------|
| profile_display_name   | "Maria Santos"                                         |
| profile_full_name_input| prefill: "Maria Santos" (from ProfileUiState.fullName) |
| profile_email_input    | prefill: "maria.santos@example.com" (from state)      |
| profile_phone_input    | prefill: "+63 917 123 4567" (from state)              |
| profile_success_message| "Your profile has been updated successfully."          |
| profile_section_header | "Personal Information"                                 |
| profile_save_button    | "Save Changes"                                         |
| profile_change_password| "Change Password"                                      |
| profile_logout_button  | "Log Out"                                              |

---

## Design Notes

**Color usage:**
- `primary` is applied to the avatar border, display name, section headers, focused input borders, and Save button — the entire "identity and action" layer carries the brand trust-blue.
- `error` is used exclusively for Log Out — an unmistakable visual signal for a destructive action.
- **Success uses the primary family, not green:** the saved-confirmation banner is `primaryContainer` / `primary` / `onPrimaryContainer`. This palette ships no green, and DESIGN.md maps the terminal-success semantic onto primary — the same pair used for a settled payment, so a successful save and a successful payment read alike.
- The placeholder avatar background is `primaryContainer`, giving initials-based fallbacks brand coherence.

**Typography:**
- `headlineSmall` (24 sp) for the display name — prominent but subordinate to the avatar image in visual weight.
- `titleMedium` (16 sp, 500 weight) for section headers — clear structural wayfinding without competing with the form content.
- `bodyLarge` (16 sp) in inputs for maximum legibility of personal data at default font sizes.
- `labelLarge` (14 sp, 500 weight) for button labels — uniform with the design system button spec.
- Roboto throughout; the previous Inter/Manrope pairing was outside the declared `typography.font_family`.

**Spacing:**
- Avatar section padding-bottom `spacing.xl` (32 dp) creates a clear visual break between the avatar identity block and the form card.
- Cards use `radius.md`, consistent with the MD3 large-component shape spec.
- `spacing.md` (16 dp) above the danger section creates spatial isolation from the main action buttons.

**Accessibility:**
- The edit icon on the avatar carries `role=button` with the explicit label "Change profile photo" — its 28 dp visual size is compensated by a touch-target expansion to `touch_targets.comfortable` (48 dp).
- The success banner message carries `role=alert` so TalkBack announces the confirmation automatically, and pairs its tone with a `check_circle` icon so the outcome is not colour-only.
- All three inputs carry role=textbox with descriptive labels including the field name.
- The Log Out label in `error` meets 4.5:1 against the card background.

---

_Generated by /idea export | 2026-08-03_
