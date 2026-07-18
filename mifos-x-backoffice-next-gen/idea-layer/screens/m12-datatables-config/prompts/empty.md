---
ui_yaml_sha: 5cf837f96bad44a6987603a39cb0174263e5f014b304a91f06ba379a7ee8a285
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: 58579160284e0d02199d8e1a964960d60202781c5dbc29cd7a39acfe3c0eb281

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: empty_state

feature: m12-datatables-config
state: empty
state_visibility: empty

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m12-datatables-config — empty state

> Auto-generated from screens/m12-datatables-config/ui.yaml @ SHA 99ed3ace1788d0f0
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
1. **header** (#header) — label: "{strings.m12_title}"
2. **content_area** (#config_tabs) — label: "{strings.m12_config_tabs}"
3. **content_area** (#config_content) — label: "{strings.m12_content_label}"
4. **list_item** (#datatable_row) — label: "{strings.m12_datatable_row}", on_click: { action: open_datatable_detail, target: m12-datatables-config }
5. **list_item** (#config_row) — label: "{strings.m12_config_row}", on_click: { action: open_config_detail, target: m12-datatables-config }
6. **list_item** (#external_service_row) — label: "{strings.m12_external_service_row}", on_click: { action: open_external_service_detail, target: m12-datatables-config }
7. **button** (#register_datatable_button) — label: "{strings.m12_register_datatable}", on_click: { action: register_datatable }
8. **button** (#add_column_button) — label: "{strings.m12_add_column}", on_click: { action: add_datatable_column }
9. **button** (#deregister_datatable_button) — label: "{strings.m12_deregister_datatable}", on_click: { action: deregister_datatable }
10. **switch** (#toggle_config_switch) — label: "{strings.m12_toggle_config}", on_click: { action: toggle_global_config }
11. **button** (#new_entity_check_button) — label: "{strings.m12_new_entity_check}", on_click: { action: create_entity_datatable_check }
12. **button** (#delete_entity_check_button) — label: "{strings.m12_delete_entity_check}", on_click: { action: delete_entity_datatable_check }
13. **button** (#edit_external_service_button) — label: "{strings.m12_edit_external_service}", on_click: { action: edit_external_service }
14. **button** (#empty_register_cta) — label: "{strings.m12_register_datatable}", on_click: { action: register_datatable }
15. **button** (#retry_button) — label: "{strings.m12_retry}", on_click: { action: retry_load }

## State-specific behavior
- Show an empty-state illustration, a friendly message, and one primary call-to-action button.

## Content source manifest
- (no demo collections bound for this state)

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

- [ ] **Per-state shape:** the render shows ONLY this state ("empty"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "master_detail" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
