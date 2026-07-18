---
ui_yaml_sha: 64e792bbb9d2f16e727142c1ef33541c34dee7b3b1605b806253d07824fd930b
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: d86eb4ae53375a34ece3c21a4b789a7606745902d139319a6f78d1b0bc359da8

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: master_detail

feature: m11-tellers-cash
state: pending_approval
state_visibility: pending_approval

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m11-tellers-cash — pending_approval state

> Auto-generated from screens/m11-tellers-cash/ui.yaml @ SHA 16da866a1d3ca10e
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
1. **header** (#m11_header) — label: "{strings.m11_title}"
2. **banner** (#offline_banner) — label: "{strings.m11_offline_banner}"
3. **content_area** (#teller_content) — label: "{strings.m11_content_label}"
4. **chip** (#date_range_filter) — label: "{strings.m11_date_range}", on_click: { action: change_cashier_date_range }
5. **list_item** (#teller_row) — label: "{strings.m11_teller_row}", on_click: { action: open_teller_detail, target: m11-tellers-cash }
6. **fab** (#new_teller_button) — label: "{strings.m11_new_teller}", on_click: { action: create_teller_form, target: dynamic-template-forms }
7. **button** (#edit_teller_button) — label: "{strings.m11_edit_teller}", on_click: { action: edit_teller_form, target: dynamic-template-forms }
8. **button** (#assign_cashier_button) — label: "{strings.m11_assign_cashier}", on_click: { action: assign_cashier, target: dynamic-template-forms }
9. **button** (#allocate_cash_button) — label: "{strings.m11_allocate_cash}", on_click: { action: allocate_cash_to_cashier, target: dynamic-template-forms }
10. **button** (#settle_cash_button) — label: "{strings.m11_settle_cash}", on_click: { action: settle_cash_from_cashier, target: dynamic-template-forms }
11. **button** (#view_ledger_button) — label: "{strings.m11_view_ledger}", on_click: { action: view_teller_transactions }
12. **button** (#review_failed_button) — label: "{strings.m11_review_failed}", on_click: { action: open_needs_attention, target: needs-attention-inbox }
13. **button** (#retry_button) — label: "{strings.m11_retry}", on_click: { action: retry_load }

## State-specific behavior
- Custom state "Pending Approval" — render per the composition below.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("pending_approval"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "master_detail" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
