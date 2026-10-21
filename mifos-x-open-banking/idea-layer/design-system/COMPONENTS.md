---
name: Mifos X Open Banking — Components
version: "4.0.0"
generated_at: "2026-08-04"
generated_by: /design-system
token_source: design-tokens.yaml
token_source_version: "2.3.0"
palette: "Open Banking — Trust Blue (primary #266489)"
typography: Roboto
category: banking
supersedes:
  version: "3.0.0"
  generated_at: "2026-05-28"
  palette: "earth-green (#4C662B) — RETIRED BRAND"
  note: >-
    The 3.0.0 revision documented the retired earth-green brand and the Outfit type family.
    Its frontmatter already said token_source: design-tokens.yaml, which was true on
    2026-05-28 — the token file still held green then. The token file was rebranded to Trust
    Blue afterwards and this document was never re-derived, so it kept 2026-05-28's values
    under today's filename. Re-derived here from design-tokens.yaml 2.3.0.
---

# Mifos X Open Banking — Component Library

> Project-internal narrative component guide. Every value below is derived from
> `design-tokens.yaml` 2.3.0 — the canonical source of truth for Compose codegen and the
> preview renderer. Where a component needs a role the M3 set does not name, the mapping is
> stated inline rather than left implicit.
>
> **Provenance changed at 4.0.0.** The 3.0.0 revision was extracted from Figma file
> `tEEJwW4HkUR75fKhDq73Jz`, which holds the retired green design. This revision derives from
> the token file (a Material Theme Builder export, seed `#266489`), so Figma node references
> have been dropped rather than carried forward pointing at a design that no longer applies.

## Buttons

### Button / Filled
- **Spec**: `colors.light.primary` (`#266489`) background, `colors.light.onPrimary` (`#FFFFFF`) text, 40dp height, `radius.full` (9999) border-radius, 24dp horizontal padding
- **Typography**: `typography.roles.labelLarge` — Roboto Medium 14sp / 20sp line-height
- **Min touch target**: 48dp (via `touchTargets.min_touch_target`)
- **Compose**: `Button(colors = ButtonDefaults.buttonColors(containerColor = Primary))`
- **Token refs**: `component_tokens.button.height_default`, `component_tokens.button.padding_horizontal`, `component_tokens.button.radius`
- **Usage**: Primary actions — Login, Send, Confirm, Save, Apply

### Button / Outlined
- **Spec**: 1dp `colors.light.outline` (`#72787E`) border, `colors.light.primary` (`#266489`) text, 40dp height, `radius.full` (9999) border-radius, 24dp horizontal padding
- **Typography**: `typography.roles.labelLarge` — Roboto Medium 14sp
- **Compose**: `OutlinedButton(border = BorderStroke(1.dp, Outline))`
- **Usage**: Secondary actions — Continue with HSBC, Cancel, Skip

### Button / Text
- **Typography**: `typography.roles.labelLarge` — Roboto Medium 14sp, `colors.light.primary` (`#266489`) color
- **Compose**: `TextButton(colors = ButtonDefaults.textButtonColors(contentColor = Primary))`
- **Usage**: Tertiary actions — Forgot password, See all, navigation links

## FAB

### FAB / Primary
- **Spec**: 56dp square, `component_tokens.fab.radius` = `radius.lg` (16dp) border-radius, `colors.light.primary` (`#266489`) background, `colors.light.onPrimary` (`#FFFFFF`) "+" icon 28dp
- **Min touch target**: naturally 56dp — satisfies 48dp requirement
- **Compose**: `FloatingActionButton(containerColor = Primary, shape = RoundedCornerShape(16.dp))`
- **Token refs**: `component_tokens.fab.size`, `component_tokens.fab.radius`, `component_tokens.fab.background`
- **Usage**: Primary creation — New payment, Add beneficiary, New account

## Badges

### Badge / Success
- **Spec**: `colors.light.primary` (`#266489`) background, `colors.light.onPrimary` (`#FFFFFF`) text, 24dp height, `radius.sm` (8dp) border-radius, 10dp horizontal padding
- **Typography**: `typography.roles.labelMedium` — Roboto Medium 12sp
- **Role note**: `semantic.status.success` maps to **primary**, not a green. The palette ships no celebratory colour by design.
- **Token refs**: `component_tokens.badge.height`, `component_tokens.badge.radius`, `component_tokens.badge.variants.success`
- **Content**: "COMPLETED"

### Badge / Pending
- **Spec**: `colors.light.tertiary` (`#64597B`) background, `colors.light.onTertiary` (`#FFFFFF`) text, same dimensions
- **Role note**: the 3.0.0 revision used an amber `#E8A317` that exists in no spelling of this palette. `semantic.status.warning` maps to **tertiary** (`#64597B` light / `#CFC0E8` dark) with icon `schedule`. Adding an amber hue would mean introducing a fifth colour family the system does not have.
- **Token refs**: `component_tokens.badge.variants.pending`
- **Content**: "INITIATED"

### Badge / Failed
- **Spec**: `colors.light.error` (`#BA1A1A`) background, `colors.light.onError` (`#FFFFFF`) text, same dimensions
- **Token refs**: `component_tokens.badge.variants.failed`
- **Content**: "FAILED"

## Inputs

### TextField / Default
- **Spec**: `colors.light.surface` (`#F7F9FF`) background, 1dp `colors.light.outline` (`#72787E`) border, 56dp height (`component_tokens.text_field.height`), `radius.xs` (4dp) border-radius, 16dp horizontal padding, 8dp vertical padding
- **Label**: `typography.roles.labelSmall` — Roboto Medium 11sp, `colors.light.outline` (`#72787E`)
- **Value**: `typography.roles.bodyLarge` — Roboto Regular 16sp, `colors.light.onSurface` (`#181C20`)
- **Min touch target**: 56dp height satisfies 48dp; the label area also carries a 48dp interactive zone
- **Compose**: `OutlinedTextField(shape = RoundedCornerShape(4.dp))`
- **Token refs**: `component_tokens.text_field.height`, `component_tokens.text_field.radius`, `component_tokens.text_field.border_color`

## Surfaces

### Card / Base
- **Spec**: `colors.light.surface` (`#F7F9FF`) background, 1dp `colors.light.outlineVariant` (`#C1C7CE`) border, `radius.md` (12dp) border-radius, `spacing.md` (16dp) padding
- **Title**: `typography.roles.titleMedium` — Roboto Medium 16sp, `colors.light.onSurface` (`#181C20`)
- **Supporting text**: `typography.roles.bodyMedium` — Roboto Regular 14sp, `colors.light.onSurfaceVariant` (`#41474D`)
- **Compose**: `Card(border = BorderStroke(1.dp, OutlineVariant), shape = RoundedCornerShape(12.dp))`
- **Token refs**: `component_tokens.card.radius`, `component_tokens.card.padding`, `component_tokens.card.border_color`, `component_tokens.card.elevation`

### Balance Card (Banking)
- **Spec**: `colors.light.primaryContainer` (`#C9E6FF`) background, `radius.lg` (16dp) border-radius, 20dp padding, no border, `elevation.level0`
- **Label**: `typography.roles.bodyMedium` — Roboto Regular 14sp, `colors.light.onSurfaceVariant` (`#41474D`)
- **Amount**: `typography.roles.displaySmall` — Roboto 36sp / 44sp line-height, `colors.light.onPrimaryContainer` (`#004B6F`). Amounts use the mono family (`Roboto Mono`) where digit alignment matters across a column.
- **Subtitle**: `typography.roles.bodySmall` — Roboto Regular 12sp, `colors.light.onSurfaceVariant` (`#41474D`)
- **Compose**: `Card(colors = CardDefaults.cardColors(containerColor = PrimaryContainer), shape = RoundedCornerShape(16.dp))`

### Transaction Item (Banking)
- **Container**: `colors.light.surface` (`#F7F9FF`) fill, `colors.light.outlineVariant` (`#C1C7CE`) border, `radius.md` (12dp) border-radius, `spacing.md` (16dp) padding
- **Icon**: 40dp circle with `colors.light.surfaceContainer` (`#EBEEF3`) fill
- **Merchant**: `typography.roles.titleMedium` — Roboto Medium 16sp, `colors.light.onSurface` (`#181C20`)
- **Category**: `typography.roles.bodySmall` — Roboto Regular 12sp, `colors.light.onSurfaceVariant` (`#41474D`)
- **Amount (credit)**: `typography.roles.titleMedium` — Roboto Medium 16sp, `colors.light.primary` (`#266489`), rendered with a `+` sign
- **Amount (debit)**: `typography.roles.titleMedium` — Roboto Medium 16sp, `colors.light.error` (`#BA1A1A`), rendered with a `−` sign
- **Direction note**: colour and sign are always used together, so neither a colour-blind customer nor a greyscale screenshot loses direction.
- **Badge**: inline, right-aligned — see Badge section

## Navigation

### TopBar / Default
- **Spec**: `colors.light.background` (`#F7F9FF`) fill, `component_tokens.app_bar.height` (56dp) height, 16dp horizontal padding
- **Back arrow**: 24dp `colors.light.onSurface` (`#181C20`)
- **Title**: `typography.roles.titleLarge` — Roboto Regular 22sp / 28sp line-height
- **Gap**: 16dp between arrow and title
- **Min touch target**: back arrow tappable area padded to 48dp
- **Compose**: `TopAppBar(colors = TopAppBarDefaults.topAppBarColors(containerColor = Background))`
- **Token refs**: `component_tokens.app_bar.height`, `component_tokens.app_bar.background`

### BottomNav / Home
- **Spec**: `colors.light.background` (`#F7F9FF`) fill, 1dp `colors.light.outlineVariant` (`#C1C7CE`) border-top, `component_tokens.bottom_nav.height` (80dp) height
- **Layout**: 5 tabs evenly spaced — Home, Accounts, Pay, Cards, More (`PROJECT_CONFIG#tech.bottom_nav`)
- **Active tab**: icon inside a 64×28dp pill filled `colors.light.secondaryContainer` (`#D3E5F5`), 14dp pill radius. Label `typography.roles.labelSmall` — Roboto Medium 11sp, `colors.light.onSecondaryContainer` (`#384956`)
- **Role note**: the retired palette declared a bespoke `nav_active_indicator` (`#DCE7C8`). The canonical 35-role M3 set has no such role and `app-shell.yaml` declares no nav colour, so this maps to **secondaryContainer** — the role M3 specifies for a NavigationBar active indicator.
- **Inactive tab**: no pill. Label `typography.roles.labelSmall` — Roboto Medium 11sp, `colors.light.onSurfaceVariant` (`#41474D`)
- **Touch target per tab**: 80dp height satisfies 48dp; each tab is ≥78dp wide on a 390dp screen at 5 tabs
- **Compose**: `NavigationBar(containerColor = Background)`
- **Token refs**: `component_tokens.bottom_nav.height`, `component_tokens.bottom_nav.background`, `component_tokens.bottom_nav.border_top`, `component_tokens.bottom_nav.active_indicator`, `component_tokens.bottom_nav.tabs`

## Search

### Search Bar / Default
- **Spec**: `colors.light.surfaceContainer` (`#EBEEF3`) fill, `radius.full` (9999) border-radius, 56dp height, 16dp horizontal padding, search icon 24dp left, clear icon 24dp right (when active)
- **Placeholder**: `typography.roles.bodyLarge` — Roboto Regular 16sp, `colors.light.onSurfaceVariant` (`#41474D`)
- **Compose**: `SearchBar` or `DockedSearchBar` per M3 spec

## Feedback

### Loading States
- **Skeleton shimmer**: gradient sweep `colors.light.surfaceVariant` (`#DDE3EA`) → `colors.light.background` (`#F7F9FF`); `motion.duration.long1` (450ms) linear infinite
- **Circular spinner**: 3dp border, `colors.light.primaryContainer` (`#C9E6FF`) track, `colors.light.primary` (`#266489`) active arc; `motion.duration.long2` (500ms) linear
- **Pattern**: chrome (TopBar, BottomNav) stays real during loading. Content surfaces are replaced by skeletons matching the content layout geometry.

### Empty / Error States
- **Empty**: centered icon (48dp, `colors.light.onSurfaceVariant` `#41474D`) + title `typography.roles.titleMedium` + description `typography.roles.bodyMedium` (`#41474D`) + optional Button / Filled
- **Error**: same layout, icon colour `colors.light.error` (`#BA1A1A`), "Retry" Button / Filled
- **Distinction note**: empty and error must remain visually distinguishable at a glance — the icon pair carries that difference, so an implementation that renders both with the same glyph loses it.

### Dialog / Bottom Sheet
- **Dialog**: `colors.light.surfaceContainerHigh` (`#E5E8ED`) fill, `elevation.level3` (6dp) shadow, `radius.xl` (28dp) top corners, `spacing.lg` (24dp) content padding
- **Bottom Sheet**: as dialog, anchored to screen bottom, scrim `colors.light.scrim` (`#000000`) at 40% opacity light / 60% dark

## Design Tokens Quick Reference

| Token | Light | Dark |
|-------|-------|------|
| primary | `#266489` | `#95CDF7` |
| onPrimary | `#FFFFFF` | `#00344E` |
| primaryContainer | `#C9E6FF` | `#004B6F` |
| onPrimaryContainer | `#004B6F` | `#C9E6FF` |
| secondary | `#50606E` | `#B7C9D9` |
| secondaryContainer | `#D3E5F5` | `#384956` |
| tertiary (warning) | `#64597B` | `#CFC0E8` |
| background | `#F7F9FF` | `#101417` |
| surface | `#F7F9FF` | `#101417` |
| surfaceVariant | `#DDE3EA` | `#41474D` |
| surfaceContainer | `#EBEEF3` | `#1C2024` |
| error | `#BA1A1A` | `#FFB4AB` |
| outline | `#72787E` | `#8B9198` |
| outlineVariant | `#C1C7CE` | `#41474D` |
| onSurface (text primary) | `#181C20` | `#E0E3E8` |
| onSurfaceVariant (text secondary) | `#41474D` | `#C1C7CE` |
| scrim | `#000000` | `#000000` |

_Derived from `design-tokens.yaml` 2.3.0 · 2026-08-04 · seed `#266489` (Material Theme Builder export)_
