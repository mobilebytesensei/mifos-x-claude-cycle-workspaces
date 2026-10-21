---
ui_yaml_sha: auto
design_md_hash: auto
feature: pay-domestic-single
state: loading
state_visibility: loading
archetype: skeleton_screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-single — loading state

> Source: screens/pay-domestic-single/ui.yaml · design-system/DESIGN.md
> DO NOT redeclare colors, fonts, or spacing — they live in the uploaded design system.
> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More).

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or perform an action may look tappable. DO NOT add tap
> affordances to decorative content — page titles, section headings, static labels, shimmer
> rectangles are NOT interactive.

## Archetype: skeleton_screen

## State

`loading` — the ViewModel has called `loadPaymentSources()` and is awaiting the accounts and
beneficiaries API responses. No content is available yet.

## Layout

- type: scrollable_column
- padding: screen_padding (16dp on each side)
- alignment: start
- The content area is the screen minus: status bar (44dp) + TopAppBar (64dp) + BottomNav (80dp)

## Visible components in this state

Per `ui.yaml#states.loading.layout.visible_components`: **step_indicator only**.

The step_indicator itself renders as shimmer in this state — its step labels are not yet loaded.

## Composition (top → bottom)

1. **TopAppBar** — Title "Pay someone", back/close icon (arrow_back), no action icons.
   Background: `surface`. Title: `titleLarge`, `onSurface`.

2. **StepIndicatorSkeleton** — Full-width row (48dp tall). Four shimmer rectangles
   (72dp × 16dp each) separated by 1dp dividers, fill `surfaceContainerLow`, radius `radius/sm`.
   NO step labels visible.

3. **SkeletonContent** — Three shimmer rows below, each 56dp tall × full width − 32dp, fill
   `surfaceContainerLow`, radius `radius/sm`, gap 12dp between rows. These represent
   the skeleton of the account list that will appear in the content state.

4. **BottomNav** — 80dp, fill `surfaceContainer`. Tab "Pay" is active (`primary`); tabs Home,
   Accounts, More are inactive (`onSurfaceVariant`).

## State-specific behavior

- Shimmer animation: left-to-right opacity sweep (0.4 → 0.9 → 0.4), 1.5 s loop. Low-motion:
  shimmer is a static `surfaceContainerLow` fill with no animation (per `motion.intensity: low`).
- ZERO real text, zero data values, zero images in this state.
- The confirm button does NOT appear here.

## Content source manifest

(none — no real data available in the loading state)

## Shell

- Home: navigates to home screen
- Accounts: navigates to accounts screen
- Pay: navigates to payments hub (current tab is Pay — this form is inside it)
- More: navigates to settings / more menu

## Design-token references (by name only — no hex literals, no inline size values)

- Colors: `surface`, `surfaceContainerLow`, `onSurface`, `onSurfaceVariant`, `primary`, `surfaceContainer`
- Typography: `titleLarge` (TopAppBar title)
- Spacing: `spacing/md` (16dp screen padding), `spacing/sm` (8dp gap)
- Radius: `radius/sm` (skeleton rectangles)

## Self-Validation Checklist (MANDATORY before rendering)

- [ ] Only the loading state is shown — no account rows, no amounts, no field inputs.
- [ ] All content areas are shimmer rectangles — zero real data or text labels.
- [ ] No confirm button, no form fields, no payee list.
- [ ] Token references are by name (e.g. `surface`, `primary`) — no hex literals.
- [ ] Archetype is skeleton_screen — shimmer fills, not empty boxes.
- [ ] App-shell parity: TopAppBar shows "Pay someone" + back icon; BottomNav shows Pay tab active.

If any checkpoint fails → fix the output before returning.

↑↑↑ MOCKUP PROMPT
