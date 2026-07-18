---
ui_yaml_sha: 11ec2758f48b669564779997eac19c04eefc9cba9c4e5945ea437b6400e1f381
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: 1ed331b7a25e51f5dd71532fd1625190d7a44115852c122a4df48a56031bf79d

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: list_screen

feature: m07-accounting
state: submitting
state_visibility: submitting

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m07-accounting — submitting state

> Auto-generated from screens/m07-accounting/ui.yaml @ SHA e914306741f1f210
> Stitch DesignSystem: 6486719301524192685
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Collections, Sync) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: list_screen

## Layout
- type: scrollable_column
- padding: default
- alignment: start

## Composition (top → bottom)
1. **header** (#accounting_header) — label: "{strings.m07_title}"
2. **chip** (#accounting_type_filter) — label: "{strings.m07_type_filter}", on_click: { action: filter_gl_type }
3. **content_area** (#accounting_content) — label: "{strings.m07_content_label}"
4. **list_item** (#gl_account_row) — label: "{strings.m07_gl_row_label}", on_click: { action: open_gl_account }
5. **list_item** (#journal_entry_row) — label: "{strings.m07_journal_row_label}", on_click: { action: open_journal_entry }
6. **chip** (#journal_status_chip) — label: "{strings.m07_journal_status_chip}"
7. **fab** (#create_gl_account_fab) — label: "{strings.m07_create_gl_account}", on_click: { action: create_gl_account, target: dynamic-template-forms }
8. **button** (#start_journal_entry_button) — label: "{strings.m07_start_journal}", on_click: { action: start_journal_entry, target: dynamic-template-forms }
9. **button** (#add_debit_line_button) — label: "{strings.m07_add_debit_line}", on_click: { action: add_debit_line }
10. **button** (#add_credit_line_button) — label: "{strings.m07_add_credit_line}", on_click: { action: add_credit_line }
11. **content_area** (#balance_indicator) — label: "{strings.m07_balance_indicator}"
12. **button** (#post_journal_entry_button) — label: "{strings.m07_post_journal}", on_click: { action: post_journal_entry }
13. **button** (#reverse_journal_entry_button) — label: "{strings.m07_reverse_journal}", on_click: { action: reverse_journal_entry }
14. **button** (#create_gl_closure_button) — label: "{strings.m07_create_closure}", on_click: { action: create_gl_closure, target: dynamic-template-forms }
15. **button** (#financial_activity_mapping_button) — label: "{strings.m07_financial_activity}", on_click: { action: map_financial_activity, target: dynamic-template-forms }
16. **button** (#run_accruals_button) — label: "{strings.m07_run_accruals}", on_click: { action: run_periodic_accruals }
17. **button** (#retry_button) — label: "{strings.m07_retry}", on_click: { action: retry_load }

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
- [ ] **Archetype honored:** the layout follows the "list_screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
