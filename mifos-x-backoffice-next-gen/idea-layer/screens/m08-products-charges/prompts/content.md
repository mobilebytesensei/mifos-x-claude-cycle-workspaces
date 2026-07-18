---
ui_yaml_sha: f426471f2c62acea3018860038e7a5545ba6cba0769183958534ef07916b478f
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: 8dffa32d18e409190bace1c7cf930db8f11576e3bd0f4d763a5ed19a6be1a016

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: master_detail

feature: m08-products-charges
state: content
state_visibility: content

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m08-products-charges — content state

> Auto-generated from screens/m08-products-charges/ui.yaml @ SHA 3beef4cccc4f84c6
> Stitch DesignSystem: 6486719301524192685
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Collections, Sync) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: master_detail

## Layout
- type: scrollable_column
- padding: default
- alignment: start

## Composition (top → bottom)
1. **header** (#header) — label: "{strings.m08_title}"
2. **chip** (#catalog_tabs) — label: "{strings.m08_catalog_tabs}", on_click: { action: switch_catalog_tab }
3. **text_field** (#catalog_search_field) — label: "{strings.m08_search}", on_click: { action: search_catalog }
4. **content_area** (#catalog_list) — label: "{strings.m08_catalog_list}"
5. **list_item** (#catalog_row) — 2 items: "Group Business Loan", "Individual Micro Loan"
6. **fab** (#create_loan_product_fab) — label: "{strings.m08_create_loan_product}", on_click: { action: create_loan_product }
7. **fab** (#create_savings_product_fab) — label: "{strings.m08_create_savings_product}", on_click: { action: create_savings_product }
8. **fab** (#create_charge_fab) — label: "{strings.m08_create_charge}", on_click: { action: create_charge }
9. **fab** (#create_fund_fab) — label: "{strings.m08_create_fund}", on_click: { action: create_fund }
10. **fab** (#create_tax_group_fab) — label: "{strings.m08_create_tax_group}", on_click: { action: create_tax_group }
11. **button** (#edit_product_button) — label: "{strings.m08_edit_product}", on_click: { action: edit_product }
12. **button** (#edit_charge_button) — label: "{strings.m08_edit_charge}", on_click: { action: edit_charge }
13. **button** (#delete_product_button) — label: "{strings.m08_delete_product}", on_click: { action: delete_product }
14. **switch** (#toggle_charge_active_button) — label: "{strings.m08_toggle_charge_active}", on_click: { action: toggle_charge_active }
15. **button** (#empty_create_cta) — label: "{strings.m08_create_first}", on_click: { action: create_charge }
16. **button** (#connect_to_edit_banner) — label: "{strings.m08_connect_to_edit}", on_click: { action: dismiss_config_offline_banner }
17. **button** (#retry_button) — label: "{strings.m08_retry}", on_click: { action: retry_load }

## State-specific behavior
- Fully populated with the real demo content listed below.

## Content source manifest
- demo-data.loan_products[0..1]

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
- [ ] **Archetype honored:** the layout follows the "master_detail" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
