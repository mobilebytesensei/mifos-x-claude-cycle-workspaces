---
feature: pay-domestic-standing-order
state: loading
state_visibility: loading
generated_by: idea-feature-export
design_system: Open Banking — Trust Blue v1.4.0
tokens: design-tokens.yaml v2.4.0
---

# pay-domestic-standing-order — loading state

> Source: `screens/pay-domestic-standing-order/ui.yaml`
> Design system: DESIGN.md. Token file: design-tokens.yaml.
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md and design-tokens.yaml.
> Token references must be by NAME (e.g. `color/primary`, `radius/md`) — never hex literals.
> No inline font sizes. Use type scale names from DESIGN.md (e.g. `titleLarge`, `bodyMedium`).

<!-- COPY PROVENANCE: the top-bar title "Standing order" is
     strings.pay_domestic_standing_order.title VERBATIM. There is no other user-facing copy in
     this state; it is shimmer-only. -->

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home · Accounts · Pay · More).
> DO NOT render real data, real names, or tappable rows during loading.
> This state ONLY shows the skeleton/shimmer version — no form fields, no live text, no interactive elements.

## Archetype: skeleton_screen

## App Shell

- **Top app bar**: back icon (`arrow_back`, `color/onSurface`); title "Standing order" (`titleLarge`, `color/onSurface`); `color/surface` background
- **Bottom nav**: Home · Accounts · Pay (active) · More; `color/surfaceContainerHighest` background

## Layout

- Type: scrollable_column
- Background: `color/surface`
- Padding: `spacing/md` horizontal
- Gap between skeleton blocks: `spacing/sm`

## Visible Components (loading state)

**Step indicator [step_indicator] — skeleton**
- Four step circles in a row; all rendered as shimmer rectangles
- Each step: shimmer circle (24 × 24dp, `color/surfaceContainerHigh`, `radius/full`) + short shimmer line (40 × 10dp)
- Connectors between steps: 1dp line, `color/outlineVariant`
- Height: 40dp; full width; padding `spacing/md`

## Shimmer Placeholders (matching content layout)

After the step indicator, show shimmer blocks matching the Payee step's content layout:

1. **Info banner placeholder** — Fill × 52dp, `color/surfaceContainerLow`, `radius/md`
2. **Section label placeholder** — 80 × 14dp, `color/surfaceContainerHigh`, `radius/sm`
3. **Payee row placeholder × 2** — Fill × 72dp, `color/surfaceContainerLow`, `radius/md`
   Each row: leading circle (40 × 40dp) + two stacked lines (120 × 14dp, 80 × 12dp)
4. **Text button placeholder** — 180 × 16dp, `color/surfaceContainerHigh`, `radius/sm`

## Shimmer Animation

- Effect: horizontal sweep, `color/surfaceContainerHigh` to `color/surfaceContainerLow` to `color/surfaceContainerHigh`
- Duration: 1.5s loop
- Easing: `motion.emphasis_easing`
- Reduce-motion: static shapes, no animation

## State-Specific Rules

- No real payee names, no account numbers, no amounts visible.
- No tappable elements — this state is read-only.
- Step indicator shimmer does not highlight any step as active.
- The confirm button and all form fields are ABSENT in this state.

## Self-Validation Checklist

- [ ] Renders ONLY the loading state — no form fields, no real data, no interactive rows
- [ ] Shimmer blocks match the Payee step layout shape (same row heights and widths as content)
- [ ] All colours come from token names, not hex literals
- [ ] Step indicator is present as a skeleton row, not with active step highlighted
- [ ] App shell (top app bar + bottom nav) matches the declared shell exactly
- [ ] No additional screens, nav items, or tabs invented beyond Home · Accounts · Pay · More
- [ ] No readable copy anywhere except the top-bar title

Return ONLY when all 7 checkpoints pass.

↑↑↑ MOCKUP PROMPT
