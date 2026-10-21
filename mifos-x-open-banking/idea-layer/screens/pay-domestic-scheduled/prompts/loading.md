---
feature: pay-domestic-scheduled
state: loading
archetype: skeleton_screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
generated_by: idea-feature-export v1.0.0
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-scheduled — loading state

> Auto-generated from screens/pay-domestic-scheduled/ui.yaml
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: skeleton_screen

## Layout
- type: scrollable_column
- padding: default (16dp screen padding)
- alignment: start
- responsive: single-column, mobile-first; never a fixed multi-column grid

## Composition (top → bottom)
1. **top_app_bar** — back icon left, title "Pay on a date" centre
2. **stepper** (#step_indicator) — 5 steps: Account · Payee · Amount · Date · Review; shimmer/skeleton for loading state
3. **skeleton_label** — shimmer block 120dp wide × 20dp tall (section heading placeholder)
4. **skeleton_list_item** (#debtor_account_list placeholder) — two shimmer rows, each 72dp tall, full-width, radius medium
5. **skeleton_note** — shimmer block 200dp wide × 16dp tall (ineligible accounts note placeholder)
6. **bottom_nav** — Home · Accounts · Pay (active) · More

## State-specific behavior
- Show shimmer/skeleton loaders matching the content layout block-for-block.
- The stepper renders but its step labels are shimmer-obscured or muted — the active step is not yet known.
- No real text, no account data, no images visible in this state.
- Loaders animate left-to-right (1.5s loop, surfaceContainerLow → surfaceContainer gradient).
- This is the initial screen state before accounts and beneficiaries have loaded.

## Content source manifest
- (no demo data bound — loading state shows only skeleton shapes)

## Shell

Home → home · Accounts → accounts · Pay → payments (current) · More → settings. Nav elements
are present or absent, never partial.

## Tokens

Colors surface / surfaceContainerLow / surfaceContainer (shimmer gradient) / onSurface (muted) ·
Type titleLarge / labelSmall · Spacing gap.sm / gap.md / gap.lg. All by name — no hex literals.

## Self-Validation Checklist

- [ ] Only the loading state — no account rows, no real content.
- [ ] Every placeholder is a shimmer shape — no filler text, no "Loading…" label.
- [ ] Shimmer gradient surfaceContainerLow → surfaceContainer by name; no hex codes.
- [ ] Every element maps to a named design-system component.
- [ ] skeleton_screen — matches the content state's shape without real data.
- [ ] TopAppBar + BottomNav present and consistent with the shell.

Return ONLY when all checkpoints pass.

↑↑↑ MOCKUP PROMPT
