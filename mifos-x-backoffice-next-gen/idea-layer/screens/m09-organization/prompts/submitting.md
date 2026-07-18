---
ui_yaml_sha: b95888726851db82a576989034c365d336893a2bc5d361bfa5f2866806d1f0f7
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: 2a409f420b304dd869fe53fd59d994404a909851417c4a48d63afc968fa8d992

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: master_detail

feature: m09-organization
state: submitting
state_visibility: submitting

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m09-organization — submitting state

> Auto-generated from screens/m09-organization/ui.yaml @ SHA 62d4538732b2677b
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
1. **header** (#header) — label: "{strings.m09_title}"
2. **content_area** (#entity_tabs) — label: "{strings.m09_entity_tabs}"
3. **content_area** (#org_content) — label: "{strings.m09_content_label}"
4. **list_item** (#office_row) — label: "{strings.m09_office_row}", on_click: { action: open_office_detail, target: m09-organization }
5. **list_item** (#staff_row) — label: "{strings.m09_staff_row}", on_click: { action: open_staff_detail, target: m09-organization }
6. **list_item** (#code_row) — label: "{strings.m09_code_row}", on_click: { action: open_code_detail, target: m09-organization }
7. **button** (#new_office_button) — label: "{strings.m09_new_office}", on_click: { action: create_office }
8. **button** (#new_staff_button) — label: "{strings.m09_new_staff}", on_click: { action: create_staff }
9. **button** (#add_currency_button) — label: "{strings.m09_add_currency}", on_click: { action: configure_currencies }
10. **button** (#new_holiday_button) — label: "{strings.m09_new_holiday}", on_click: { action: create_holiday }
11. **button** (#activate_holiday_button) — label: "{strings.m09_activate_holiday}", on_click: { action: activate_holiday }
12. **button** (#edit_working_days_button) — label: "{strings.m09_edit_working_days}", on_click: { action: edit_working_days }
13. **button** (#new_fund_button) — label: "{strings.m09_new_fund}", on_click: { action: create_fund }
14. **button** (#new_payment_type_button) — label: "{strings.m09_new_payment_type}", on_click: { action: create_payment_type }
15. **button** (#add_code_value_button) — label: "{strings.m09_add_code_value}", on_click: { action: add_code_value }
16. **button** (#bulk_reassign_button) — label: "{strings.m09_bulk_reassign}", on_click: { action: bulk_reassign_loans }
17. **button** (#empty_new_cta) — label: "{strings.m09_new_office}", on_click: { action: create_office }
18. **button** (#retry_button) — label: "{strings.m09_retry}", on_click: { action: retry_load }

## State-specific behavior
- Custom state "Submitting" — render per the composition below.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("submitting"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "master_detail" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
