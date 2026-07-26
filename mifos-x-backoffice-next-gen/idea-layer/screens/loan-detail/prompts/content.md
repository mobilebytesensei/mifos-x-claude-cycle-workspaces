---
ui_yaml_sha: 2ad7eecddfa4f2fddc08b4730e884fe742b5d39ed76e5c183e891bb16dbf441f
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: d17d4e9ba1d1b8295d2f03316fded3fff26f02c0cdc8a5b83ce13e9f402dc02a

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: detail

feature: loan-detail
state: content
state_visibility: content

project_id: '10243803383444073820'
design_system_id: '312064780206383264'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# loan-detail — content state

> Auto-generated from screens/loan-detail/ui.yaml @ SHA 81b8a1e5c4a7e156
> Stitch DesignSystem: 312064780206383264
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Collections, Sync) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: detail

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **header** (#ld_header) — label: "{strings.loandet_header}"
2. **list_item** (#ld_client_link) — 3 items: "2024-03-06", "2024-04-05", "2024-05-06"
3. **tab_row** (#ld_tabs) — 3 items: "2024-03-06", "2024-04-05", "2024-05-06"
4. **button** (#ld_repayment) — label: "{strings.loandet_repayment}", on_click: { action: make_repayment, target: loan-detail }
5. **button** (#ld_approve) — label: "{strings.loandet_approve}", on_click: { action: approve_loan, target: loan-detail }
6. **button** (#ld_disburse) — label: "{strings.loandet_disburse}", on_click: { action: disburse_loan, target: loan-detail }
7. **button** (#ld_error_retry) — label: "{strings.loandet_retry}", on_click: { action: retry, target: loan-detail }

## State-specific behavior
- Fully populated with the real demo content listed below.

## Content source manifest
- demo-data.transactions[0..2]
- demo-data.transactions[0..2]

## Components (vocabulary used in this prompt)
- (no named components extracted — see composition)

## Shell (app-shell resolved for this state)
- Home: navigates to m01-dashboard
- Clients: navigates to m02-clients
- Collections: navigates to m06-collections
- Sync: navigates to m17-sync-settings
- Render MUST keep nav/bar elements consistent with the list above — present or absent, never partial.

## Tokens (design-tokens roles consumed)
- Colors: primary / secondary / surface / on-surface / on-surface-variant / error (M3 standard roles).
- Typography: body-large / title-large (M3 standard roles).
- Spacing: gap.sm / gap.md / gap.lg.
- ALL token references are by name from the uploaded design system — no hex literals, no inline size values.

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. If any fails, FIX the output and re-render.

- [ ] **Per-state shape:** the render shows ONLY this state ("content"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "detail" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
