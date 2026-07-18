---
ui_yaml_sha: d6ca6a4119b2e29658d367f31b230f06580eab50830d77d522036d6464b4fe76
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: f45c68e978e7ec4210d9f5df64e41fef4a2ba608f30dd4967d6eba1e0fb6a391

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: list

feature: m15-approvals-makerchecker
state: submitting
state_visibility: submitting

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m15-approvals-makerchecker — submitting state

> Auto-generated from screens/m15-approvals-makerchecker/ui.yaml @ SHA 1aa5818dd3ba84f6
> Stitch DesignSystem: 6486719301524192685
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Collections, Sync) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: list

## Layout
- type: scrollable_column
- padding: default
- alignment: start

## Composition (top → bottom)
1. **header** (#header) — label: "{strings.m15_title}"
2. **segmented_control** (#group_by_selector) — label: "{strings.m15_group_by}", on_click: { action: switch_group_by, target: content }
3. **filter_chip_row** (#filter_bar) — label: "{strings.m15_filter}", on_click: { action: apply_search_template_filter, target: loading }
4. **content_area** (#content_area) — label: "Self-scoped checker queue of pending commands, grouped by entity / action / make"
5. **group_header** (#group_header) — label: "Group header with the grouping key (entity / action / maker) + pending count"
6. **list_item** (#command_row) — label: "One queued command row: action, target entity, maker, made-on, and a pending-app", on_click: { action: open_command_payload, target: m15-approvals-makerchecker }
7. **checkbox** (#select_toggle) — label: "{strings.m15_select_entry}", on_click: { action: toggle_entry_selection, target: content }
8. **badge** (#priority_badge) — label: "Pending-approval badge (queued command awaiting a checker)"
9. **button** (#approve_button) — label: "{strings.m15_approve}", on_click: { action: approve_entry, target: submitting }
10. **button** (#reject_button) — label: "{strings.m15_reject}", on_click: { action: reject_entry, target: submitting }
11. **button** (#delete_button) — label: "{strings.m15_delete}", on_click: { action: delete_entry, target: submitting }
12. **button** (#bulk_approve_button) — label: "{strings.m15_bulk_approve}", on_click: { action: bulk_approve_selected, target: submitting }
13. **text_link** (#open_needs_attention_link) — label: "{strings.m15_open_needs_attention}", on_click: { action: open_needs_attention, target: needs-attention-inbox }
14. **button** (#retry_button) — label: "{strings.m15_retry}", on_click: { action: retry_load, target: loading }

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
- [ ] **Archetype honored:** the layout follows the "list" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
