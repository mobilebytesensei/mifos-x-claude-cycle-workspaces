---
ui_yaml_sha: b36a070657843bdde9106db0b07bebb5dda3e4d79c327b3a57f24eb9216425f5
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: caea79319e63e3bfecb164ab09ead4c01a609a216c8403f8a79f93fec6c36310

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: index_list

feature: atm-locator
state: no_network
state_visibility: no_network

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# atm-locator — no_network state

> Auto-generated from screens/atm-locator/ui.yaml @ SHA e2d45509b11745b5
> Stitch DesignSystem: 2047482829824847747
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: index_list

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **text** (#atm_locator_title) — content: "ATM & Branches"
2. **image** (#atm_map_area) — content: "ATM map"
3. **stack** (#atm_search_row)
4. **input** (#location_search_input) — label: "Search location", on_click: { action: query_changed, target: atm_locator_main }
5. **icon_button** (#use_my_location_button) — content: "my_location", on_click: { action: request_user_location, target: atm_locator_main }
6. **text** (#nearby_results_header) — content: "4 ATMs near you"
7. **box** (#atm_result_kcb_westlands) — on_click: { action: select_atm, target: atm_locator_main }
8. **text** (#atm_kcb_name) — content: "KCB Westlands ATM"
9. **text** (#atm_kcb_hours) — content: "Open 24 hours"
10. **badge** (#atm_kcb_distance) — content: "320 m"
11. **text** (#atm_kcb_address) — content: "Westlands Commercial Centre, Waiyaki Way, Nairobi, Nairobi County, 00100"
12. **chip** (#atm_kcb_accessible_chip) — label: "Accessible", content: "accessible"
13. **chip** (#atm_kcb_deposits_chip) — label: "Deposits", content: "deposits"
14. **button** (#atm_kcb_directions) — label: "Directions", on_click: { action: open_directions, target: atm_locator_main }
15. **box** (#atm_result_equity_cbd) — on_click: { action: select_atm, target: atm_locator_main }
16. **text** (#atm_equity_name) — content: "Equity Bank CBD ATM"
17. **text** (#atm_equity_hours) — content: "Open 24 hours"
18. **badge** (#atm_equity_distance) — content: "1.2 km"
19. **box** (#atm_result_coop_karen) — on_click: { action: select_atm, target: atm_locator_main }
20. **text** (#atm_coop_name) — content: "Co-op Bank Karen ATM"
21. **text** (#atm_coop_hours) — content: "Daily 06:00–22:00"
22. **badge** (#atm_coop_distance) — content: "6.4 km"
23. **stack** (#atm_empty_state)
24. **icon** (#atm_empty_icon) — content: "location_off"
25. **text** (#atm_empty_title) — content: "No ATMs nearby"
26. **text** (#atm_empty_message) — content: "None of your banks have published ATM locations yet."
27. **stack** (#atm_error_state)
28. **icon** (#atm_error_icon) — content: "cloud_off"
29. **text** (#atm_error_title) — content: "Couldn't load ATMs"
30. **text** (#atm_error_message) — content: "Check your connection and try again"
31. **button** (#atm_retry_button) — label: "Retry", on_click: { action: retry_load, target: atm_locator_main }

## State-specific behavior
- Custom state "No Network" — render per the composition below.

## Content source manifest
- (no demo collections bound for this state)

## Components (vocabulary used in this prompt)
- (no named components extracted — see composition)

## Shell (app-shell resolved for this state)
- Home: navigates to home
- Accounts: navigates to accounts
- Pay: navigates to payments
- More: navigates to settings
- Render MUST keep nav/bar elements consistent with the list above — present or absent, never partial.

## Tokens (design-tokens roles consumed)
- Colors: primary / secondary / surface / on-surface / on-surface-variant / error (M3 standard roles).
- Typography: body-large / title-large (M3 standard roles).
- Spacing: gap.sm / gap.md / gap.lg.
- ALL token references are by name from the uploaded design system — no hex literals, no inline size values.

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. If any fails, FIX the output and re-render.

- [ ] **Per-state shape:** the render shows ONLY this state ("no_network"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "index_list" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
