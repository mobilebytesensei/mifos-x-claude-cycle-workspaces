---
# ─── DESIGN.md — @google/design.md alpha spec ───────────────────────────────
# Design-system SoT for mifos-x-backoffice-next-gen. Uploaded to Stitch once per
# content hash by .claude-runtime/scripts/design-md-upload.ts; consumed by every
# downstream design skill (RULE-DESIGN-MD-001). Seeded from §identity + §branding
# + app-shell.yaml on 2026-07-17.
# Lint: npx @google/design.md lint idea-layer/design-system/DESIGN.md
# ─────────────────────────────────────────────────────────────────────────────

name: "Mifos-X Back Office NextGen"
version: "alpha"
description: "A permission-gated, offline-first Fineract back-office. One binary renders the entire Fineract feature surface, each module visible only per the signed-in user's PermissionSet. Premium, polished, trustworthy financial-admin UI — refined Material 3 with a deep Blue primary, Teal accent, a rich blue→teal hero gradient, and soft layered elevation on cards (all WCAG-AA). Dense and legible, but with real depth, generous rounding, and App-Store-grade finish."

# ─── Colors (M3 role tokens — Stitch treats these as hard constraints) ───────
colors:
  primary:                 "#006098"
  on-primary:              "#FFFFFF"
  primary-container:       "#CBE6FF"
  on-primary-container:    "#001E30"
  secondary:               "#00796B"
  on-secondary:            "#FFFFFF"
  secondary-container:     "#B8F2E6"
  on-secondary-container:  "#00201A"
  tertiary:                "#5B5891"
  on-tertiary:             "#FFFFFF"
  tertiary-container:      "#E3DFFF"
  on-tertiary-container:   "#17124B"
  surface:                 "#FCFCFF"
  on-surface:              "#1A1C1E"
  surface-variant:         "#DEE3EB"
  on-surface-variant:      "#42474E"
  surface-container-low:   "#F3F4F9"
  background:              "#FCFCFF"
  on-background:           "#1A1C1E"
  outline:                 "#72777F"
  success:                 "#2E7D32"
  warning:                 "#F57C00"
  warning-strong:          "#B45309"
  error:                   "#BA1A1A"
  on-error:                "#FFFFFF"
  error-container:         "#FFDAD6"
  on-error-container:      "#410002"
  # ─── Data-viz palette (chart series + signed deltas) — stitch-llm-prompt-enrichment P3.
  # Consumed by donut/gauge/area-chart/sparkline treatments; on-hero for text over the gradient.
  positive:                "#2E7D32"
  negative:                "#BA1A1A"
  chart-1:                 "#006098"
  chart-2:                 "#00796B"
  chart-3:                 "#5B5891"
  chart-4:                 "#F57C00"
  chart-5:                 "#00A3B4"
  chart-track:             "#DEE3EB"
  # ─── Gradient stops (brand-token hero, per CRAFT_RULES — blue→teal, NOT stock purple) ───
  gradient-hero-from:      "#006098"
  gradient-hero-to:        "#00897B"
  on-hero:                 "#FFFFFF"

# ─── Typography ──────────────────────────────────────────────────────────────
typography:
  h1:
    fontFamily: Roboto
    fontSize: 2rem
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: 0
  h2:
    fontFamily: Roboto
    fontSize: 1.75rem
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: 0
  h3:
    fontFamily: Roboto
    fontSize: 1.375rem
    fontWeight: 600
    lineHeight: 1.35
    letterSpacing: 0
  body:
    fontFamily: Roboto
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0
  label:
    fontFamily: Roboto
    fontSize: 0.875rem
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0.1
  caption:
    fontFamily: Roboto
    fontSize: 0.75rem
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0.4
  mono:
    fontFamily: Roboto Mono
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: 0

# ─── Rounded (corner radii) ──────────────────────────────────────────────────
rounded:
  sm: 8px
  md: 12px
  lg: 20px
  xl: 28px

# ─── Spacing (4dp base scale) ────────────────────────────────────────────────
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px

# ─── Elevation (soft, diffuse shadows — premium layered depth) ───────────────
# Consumed by card / kpi-card / hero / fab / sheet treatments. Soft and diffuse
# (low opacity, large blur, minimal spread) — never harsh. Depth is the primary
# premium-vs-flat lever, so cards sit on real elevation, not just a border.
elevation:
  level-0: "none"
  level-1: "0 1px 2px rgba(16,24,40,0.06), 0 1px 3px rgba(16,24,40,0.10)"
  level-2: "0 4px 8px rgba(16,24,40,0.08), 0 2px 4px rgba(16,24,40,0.06)"
  level-3: "0 12px 24px rgba(16,24,40,0.10), 0 4px 8px rgba(16,24,40,0.06)"
  level-4: "0 24px 48px rgba(16,24,40,0.14), 0 8px 16px rgba(16,24,40,0.08)"

# ─── Components (the Stitch contract — token refs {path.to.token}) ───────────
# Flat-keyed entries; variant states are flat siblings with a recognized suffix
# (-disabled, -selected, -error, -hover, -pressed), NOT nested objects (STN5).
components:
  app-bar:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
  bottom-navigation:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface-variant}"
  bottom-navigation-selected:
    backgroundColor: "{colors.primary-container}"
    textColor: "{colors.on-primary-container}"
  navigation-rail:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface-variant}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.xl}"
    padding: "{spacing.md}"
  button-primary-disabled:
    backgroundColor: "{colors.surface-variant}"
    textColor: "{colors.on-surface-variant}"
    rounded: "{rounded.xl}"
    padding: "{spacing.md}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.primary}"
    rounded: "{rounded.xl}"
    padding: "{spacing.md}"
  fab:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.on-secondary}"
    rounded: "{rounded.lg}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.lg}"
    padding: "{spacing.md}"
  kpi-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
  list-row:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    padding: "{spacing.md}"
  data-table:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
  status-chip:
    backgroundColor: "{colors.secondary-container}"
    textColor: "{colors.on-secondary-container}"
    rounded: "{rounded.sm}"
  status-chip-error:
    backgroundColor: "{colors.error-container}"
    textColor: "{colors.on-error-container}"
    rounded: "{rounded.sm}"
  text-field:
    backgroundColor: "{colors.surface-variant}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md}"
  text-field-error:
    backgroundColor: "{colors.surface-variant}"
    textColor: "{colors.on-error-container}"
    rounded: "{rounded.sm}"
    padding: "{spacing.md}"
  banner:
    backgroundColor: "{colors.secondary-container}"
    textColor: "{colors.on-secondary-container}"
    padding: "{spacing.md}"
  offline-banner:
    backgroundColor: "{colors.warning-strong}"
    textColor: "{colors.on-primary}"
    padding: "{spacing.md}"
  bottom-sheet:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
  shimmer-skeleton:
    backgroundColor: "{colors.surface-variant}"
    rounded: "{rounded.md}"
  empty-state:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface-variant}"
    padding: "{spacing.xl}"
---

## Overview

Mifos-X Back Office NextGen is a permission-gated, offline-first administrative console for the Mifos/Fineract core-banking platform. The same binary renders the entire Fineract feature surface, but every module, KPI card, quick action, and mutating control is resolved through a PermissionEvaluator — a user sees only what their PermissionSet grants. The design language is **premium, polished, and dense**: this is a tool operated all day by accountants, tellers, branch managers, and auditors, so legibility and information density matter — but it should feel like a best-in-class fintech product, not a spreadsheet. The palette is light-mode by default, anchored by a confident deep-Blue primary (`#006098`) and a Teal secondary/accent (`#00796B`) reserved for positive/primary-action emphasis, with a rich blue→teal hero gradient for the headline metric. Surfaces sit on **soft, layered elevation** (diffuse low-opacity shadows) with generous rounding, so cards read as tactile, liftable tiles — depth and hierarchy carry the eye, not clutter. Motion is purposeful and subtle. The mood is trustworthy financial infrastructure rendered with App-Store-grade finish — a digital ledger that feels crafted.

## Colors

The `colors:` block is the closed set Stitch may draw from; never invent a value. Every fill/text pair passes WCAG AA (≥4.5:1). **Primary** (`#006CB5`, a confident deep Light-Blue) fills the top app bar accents, primary buttons, active navigation, and links, always with white (`on-primary`) text. **Secondary/Teal** (`#00796B`) is the accent — used for the FAB, positive status emphasis, and confirmation; it is not a second primary, so use it sparingly (the bright `secondary-container #B8F2E6` carries the teal feel on chips). **Tertiary** is a muted indigo for informational chips and secondary highlights. Semantic roles are explicit: `success` (`#2E7D32`) for approved/posted/reconciled, `warning` (`#F57C00`) for overdue/attention text and chips, `warning-strong` (`#B45309`) for the persistent white-on-amber offline banner fill, `error` (`#BA1A1A`) for failed/rejected/validation. Neutrals (`surface`, `surface-variant`, `surface-container-low`, `outline`, `on-surface`, `on-surface-variant`) carry the dense admin chrome: cards on `surface` lifted by soft elevation, filled inputs on `surface-variant`, metadata in `on-surface-variant`. The headline dashboard metric uses the `gradient-hero-from`→`gradient-hero-to` (blue→teal) gradient; data-viz uses the `chart-1..5` series with `chart-track` rails and `positive`/`negative` for signed deltas. Keep gradients purposeful — the hero and, sparingly, a data-viz fill — never as generic decoration; every other surface stays a clean token fill lifted by elevation, not by an extra hue.

## Typography

Roboto is the type family across all roles (Roboto Mono for tabular numerics — amounts, account IDs, balances in tables so digits align). The scale maps: `h1` (2rem/700) for screen-level page titles, `h2` (1.75rem/600) for section headers, `h3` (1.375rem/600) for card titles and dialog headers, `body` (1rem/400) for primary content and form values, `label` (0.875rem/500) for buttons, field labels, chips, and tab labels, `caption` (0.75rem/400) for metadata, timestamps, and helper text. Support text scaling to 200% without layout breakage; never redeclare font sizes inside a screen prompt — they come from this file.

## Layout

Default screen padding is `{spacing.md}` (16dp) on phone, `{spacing.lg}` (24dp) on tablet/desktop. The app is adaptive (Material 3 adaptive scaffold): **phone** uses a bottom navigation (Home / Clients / Collections / Sync — the default field-officer surface, permission-filtered) plus a `small` top app bar with a `screen`-sourced title; **tablet/desktop** promotes navigation to a permanent NavigationRail/drawer populated from the permission-gated module roots. Lists are single-column; dashboards use an independent-card grid where each KPI/quick-action/activity tile hydrates and fails independently. A FAB (bottom-end) hosts the primary create action per screen where applicable. Respect safe areas (top/bottom respected, notch extend-and-pad). A snackbar host sits bottom for transient confirmations.

## Elevation & Depth

Depth is the primary premium-vs-flat lever — surfaces sit on **soft, layered elevation**, not flat borders. Shadows are diffuse and low-opacity (large blur, minimal spread, cool near-black tint) so cards read as tactile, liftable tiles. Use the `elevation` tokens: **level-1** for standard `card`s, list groups, and the top app bar (a gentle lift off the background); **level-2** for `kpi-card`s and the hero metric so the dashboard tiles feel raised and scannable; **level-3** for the FAB, popovers, and hover/pressed emphasis; **level-4** for bottom sheets, dialogs, and menus over a 32% scrim. Cards get a hairline `outline` border ONLY on `surface-container-low` fills where contrast needs it — otherwise elevation alone separates them from the background. Never render a KPI/stat card or the hero as a flat bordered box with no shadow; that reads as unfinished. One shadow per surface — layer via the token, don't stack ad-hoc shadows.

## Shapes

Corner radii come from the `rounded` tokens. Cards, KPI cards, sheets, and the FAB use `{rounded.lg}` (20px) for a soft, premium feel. Buttons and chips-that-act use `{rounded.xl}` (28px, pill). Text fields, status chips, and shimmer blocks use `{rounded.sm}`–`{rounded.md}` (8–12px) for a crisp, data-dense feel. Nothing is sharp-cornered; nothing beyond the FAB and pill buttons is fully rounded. Data tables are square-edged within a `{rounded.lg}` card container. Generous rounding + soft elevation is the signature — cards should feel like rounded, liftable tiles.

## Components

- **app-bar** — small M3 top app bar, `surface` fill with `on-surface` title; leading auto (back/menu), screen-sourced title.
- **bottom-navigation** / **bottom-navigation-selected** — phone nav bar; active item uses the `primary-container` pill indicator, rest are `on-surface-variant`. Same item order on every screen.
- **navigation-rail** — tablet/desktop equivalent; permission-filtered module roots.
- **button-primary** / **button-primary-disabled** — primary CTA; disabled variant is the tonal `surface-variant` fill (used when an action requires network and the app is offline).
- **button-secondary** — outlined/tonal secondary action.
- **fab** — Teal accent create action, bottom-end, `{rounded.lg}`.
- **card** / **kpi-card** — the dashboard/detail building blocks, softly elevated (level-1 / level-2) rounded `surface` tiles with generous internal padding; `kpi-card` carries a small colored icon chip (`chart-1..5` / semantic role), the value large in Roboto Mono, and a muted caption — a raised, scannable metric tile, never a flat bordered box.
- **list-row** — dense single-line/two-line list item, 44dp min touch target.
- **data-table** — tabular records with Roboto Mono numerics; header row on `surface-variant`.
- **status-chip** / **status-chip-error** — semantic state pills (approved/pending/overdue/failed).
- **text-field** / **text-field-error** — filled inputs on `surface-variant`; error variant tints text/helper with the error role.
- **banner** — informational inline banner (e.g. maker-checker pending).
- **offline-banner** — persistent `warning`-filled banner shown while offline; figures below may be stale and refresh on next sync.
- **bottom-sheet** — action/detail sheet with drag handle, `{rounded.lg}` top corners.
- **shimmer-skeleton** — loading placeholder; its layout must match the content composition block-for-block.
- **empty-state** — centered friendly empty message with an optional CTA; used when a list has no rows or the user holds no permission for any tile.

## Do's and Don'ts

- Always use bottom-navigation on phone screens that show it, with the four items (Home / Clients / Collections / Sync) in the same order on every screen; promote to a NavigationRail on wide screens.
- Always match the app-bar title style and leading (back/menu) placement across all module and detail screens.
- Always render a persistent `offline-banner` (warning fill) across the top when offline, and tint any network-requiring action as `button-primary-disabled` until sync is available.
- Always match the loading-state shimmer-skeleton layout to the content-state composition block-for-block — same card grid, same row heights.
- Always use Roboto Mono for amounts, balances, and account/loan IDs in tables and detail rows so digits align.
- Never invent colour values — use only the tokens in the `colors:` block (including the `gradient-hero-*` and `chart-*` roles). Gradients are reserved for the hero metric and, sparingly, data-viz fills — not generic decoration.
- Always lift cards, KPI tiles, and the hero on soft `elevation` (level-1/level-2) — never render them as flat bordered boxes with no shadow; that reads as unfinished.
- Never redeclare font sizes, spacing, radii, or shadow values inside a screen prompt — they come from this file's tokens.
- Never blank an entire dashboard when one tile fails; isolate the failure to that card's inline error with a per-tile Retry.
