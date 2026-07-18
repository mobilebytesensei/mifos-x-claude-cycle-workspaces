---
ui_yaml_sha: 0903e3acfde98d6e1c8914da46903aaf9149d655d75727ee70d9b9929b0dc47d
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: ceb9a3dd5ae0eeeec0b8ec701393df7878508bdb2d14ba965a9273660a9f040c

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: empty_state

feature: m02-clients
state: empty
state_visibility: empty

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m02-clients — empty state

> Auto-generated from screens/m02-clients/ui.yaml @ SHA af20308d67c551ae
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
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **header** (#clients_header) — label: "{strings.m02_title}"
2. **input** (#clients_search_field) — label: "{strings.m02_search_hint}", on_click: { action: search_clients }
3. **content_area** (#clients_content) — label: "{strings.m02_content_label}"
4. **list_item** (#client_row) — label: "{strings.m02_row_label}", on_click: { action: open_client_360, target: client-detail-360 }
5. **chip** (#client_status_chip) — label: "{strings.m02_status_chip}"
6. **fab** (#new_client_fab) — label: "{strings.m02_new_client}", on_click: { action: start_client_onboarding, target: dynamic-template-forms }
7. **tab_bar** (#client_360_tabs) — label: "{strings.m02_tabs_label}", on_click: { action: select_360_tab }
8. **button** (#client_edit_button) — label: "{strings.m02_edit}", on_click: { action: edit_client, target: dynamic-template-forms }
9. **button** (#add_identifier_button) — label: "{strings.m02_add_identifier}", on_click: { action: add_client_identifier, target: dynamic-template-forms }
10. **button** (#upload_document_button) — label: "{strings.m02_upload_document}", on_click: { action: upload_client_document }
11. **button** (#add_note_button) — label: "{strings.m02_add_note}", on_click: { action: add_client_note }
12. **button** (#activate_client_button) — label: "{strings.m02_activate}", on_click: { action: activate_client }
13. **button** (#close_client_button) — label: "{strings.m02_close}", on_click: { action: close_client }
14. **button** (#reject_client_button) — label: "{strings.m02_reject}", on_click: { action: reject_client }
15. **button** (#withdraw_client_button) — label: "{strings.m02_withdraw}", on_click: { action: withdraw_client }
16. **button** (#propose_transfer_button) — label: "{strings.m02_propose_transfer}", on_click: { action: propose_client_transfer, target: dynamic-template-forms }
17. **button** (#retry_button) — label: "{strings.m02_retry}", on_click: { action: retry_load }

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
- [ ] **Archetype honored:** the layout follows the "list_screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
