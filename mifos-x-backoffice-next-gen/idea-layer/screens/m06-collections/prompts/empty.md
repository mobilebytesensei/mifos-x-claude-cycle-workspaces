---
ui_yaml_sha: f2bdbb614c600bff54d781211170a6bd128bae644d233f20faaf5451fb76b1e0
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: cf3acd60deab27db8750a885b715b8a955c1f2f9ac7ff0d592953f0ee1f6934c

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: empty_state

feature: m06-collections
state: empty
state_visibility: empty

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m06-collections — empty state

> Auto-generated from screens/m06-collections/ui.yaml @ SHA 749cbac545441b63
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
1. **header** (#header) — label: "{strings.m06_title}"
2. **button** (#sheet_context_picker) — label: "{strings.m06_pick_meeting}", on_click: { action: pick_sheet_context, target: dynamic-template-forms }
3. **content_area** (#content_area) — label: "Collection sheet — center/group header, per-group client rows with loan-repaymen"
4. **list_item** (#sheet_member_row) — label: "One client row on the sheet: client display name + external id, loan repayment d", on_click: { action: open_loan_detail, target: m04-loan-portfolio }
5. **text_field** (#capture_amount_field) — label: "{strings.m06_amount_collected}", on_click: { action: capture_member_collection, target: content }
6. **card** (#sheet_total_summary) — label: "{strings.m06_total_summary}", on_click: { action: none }
7. **button** (#submit_sheet_button) — label: "{strings.m06_submit_sheet}", on_click: { action: submit_collection_sheet }
8. **button** (#view_receipts_button) — label: "{strings.m06_view_receipts}", on_click: { action: generate_receipts }
9. **button** (#review_needs_attention_button) — label: "{strings.m06_review_failed}", on_click: { action: open_needs_attention, target: needs-attention-inbox }
10. **button** (#retry_button) — label: "{strings.m06_retry}", on_click: { action: retry_generate, target: loading }

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
