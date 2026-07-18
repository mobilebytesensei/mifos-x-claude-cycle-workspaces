---
ui_yaml_sha: 25944cd776850035c3c10fdb20b292e110bc65a46209f544339db98377b6255c
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: afa911b3686aa6179883b37af682212c161e254047476a3aebd096a83aa6c46c

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: tab_screen

feature: m14-reports-search-audit
state: content
state_visibility: content

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m14-reports-search-audit — content state

> Auto-generated from screens/m14-reports-search-audit/ui.yaml @ SHA 0e5fc4ee55e6379f
> Stitch DesignSystem: 6486719301524192685
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Collections, Sync) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: tab_screen

## Layout
- type: scrollable_column
- padding: default
- alignment: start

## Composition (top → bottom)
1. **header** (#header) — label: "{strings.m14_title}"
2. **chip** (#tab_strip) — label: "{strings.m14_tabs}", on_click: { action: select_tab }
3. **content_area** (#content_area) — label: "{strings.m14_content}"
4. **list_item** (#report_row) — 5 items: "Active Loans - Summary", "Portfolio at Risk", "Client Listing", "Trial Balance", "Client Loan Repayment Report"
5. **button** (#run_report_button) — label: "{strings.m14_run_report}", on_click: { action: run_report }
6. **button** (#export_button) — label: "{strings.m14_export}", on_click: { action: export_report }
7. **text_field** (#search_input) — label: "{strings.m14_search_hint}", on_click: { action: run_global_search }
8. **list_item** (#search_result_row) — 4 items: "Faith Njeri", "Loan #55021", "Njeri Women's Group", "Savings #77140"
9. **button** (#audit_filter_button) — label: "{strings.m14_audit_filter}", on_click: { action: apply_audit_filter }
10. **list_item** (#audit_row) — 4 items: "DISBURSE", "REPAYMENT", "CREATE", "UPDATE"
11. **button** (#retry_button) — label: "{strings.m14_retry}", on_click: { action: retry_load }

## State-specific behavior
- Fully populated with the real demo content listed below.

## Content source manifest
- demo-data.report_catalog[0..4]
- demo-data.search_results[0..3]
- demo-data.audit_entries[0..3]

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
- [ ] **Archetype honored:** the layout follows the "tab_screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
