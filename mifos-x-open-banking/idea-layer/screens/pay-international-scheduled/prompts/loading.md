---
feature: pay-international-scheduled
state: loading
state_visibility: loading
archetype: skeleton_screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
generated_by: idea-feature-export
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-international-scheduled — loading state

> Source: screens/pay-international-scheduled/ui.yaml · Design system: Open Banking — Trust Blue
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

<!-- COPY PROVENANCE: title is strings.pay_international_scheduled.title VERBATIM. No other
     user-facing copy in this state — it is shimmer-only. -->

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable. DO NOT add tap affordances to static labels, shimmer blocks, or decorative content.

## Archetype: skeleton_screen

## Layout
- type: scrollable_column
- padding: spacing/md (16dp) on all sides
- gap: spacing/md between shimmer blocks
- alignment: start (top)

## Composition (top → bottom)

1. **TopAppBar** — back icon (left), title "Pay abroad on a date" (titleLarge, onSurface)
2. **shimmer** — step indicator row: full-width rectangle, height 40dp, radius/sm, fill surfaceContainerHighest
3. **shimmer** — account card: full-width, height 64dp, radius/md, fill surfaceContainerHighest
4. **shimmer** — row label: width 60%, height 16dp, radius/sm, fill surfaceContainerHighest
5. **shimmer** — account card: full-width, height 64dp, radius/md, fill surfaceContainerHighest
6. **shimmer** — row label: width 50%, height 16dp, radius/sm, fill surfaceContainerHighest
7. **shimmer** — next button: full-width, height 56dp, radius/full, fill surfaceContainerHighest

## State-specific behavior
- Every text label, data value, and icon is replaced by a shimmer block matching the content component's dimensions.
- Shimmer fill surfaceContainerHighest, 1.5s left-to-right sweep (low-motion: opacity pulse).
- Do not render any readable text, account numbers, amounts, or icons during loading.
- TopAppBar title and back arrow stay non-shimmer.

## Content source manifest
- (no data available — screen is loading accounts)

## Shell (app-shell resolved for this state)
- Home: navigates to home
- Accounts: navigates to accounts
- Pay: navigates to payments hub (active tab)
- More: navigates to settings
- Bottom nav is present and consistent. Active tab: Pay.

## Tokens (design-tokens roles consumed)
- surfaceContainerHighest: shimmer block fill
- surface: screen background
- onSurface: TopAppBar title and back icon
- radius/sm (8dp): step indicator shimmer, label shimmers
- radius/md (12dp): account card shimmers
- radius/full (9999dp): button shimmer
- spacing/md (16dp): screen padding and gap between blocks

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. Fix and re-render if any fails.

- [ ] **Per-state shape**: renders ONLY the loading state. No real account data, no form fields, no amounts.
- [ ] **Shimmer only**: every content area is a shimmer rectangle — no readable text below the TopAppBar title.
- [ ] **Token fidelity**: shimmer fill is surfaceContainerHighest by name; background is surface by name. No hex literals.
- [ ] **Component vocabulary**: TopAppBar, shimmer rectangles, BottomNav — no invented components.
- [ ] **Archetype honored**: skeleton_screen — blocks match the content step-indicator + account list in shape.
- [ ] **App-shell parity**: bottom nav Home / Accounts / Pay (active) / More.

↑↑↑ MOCKUP PROMPT
