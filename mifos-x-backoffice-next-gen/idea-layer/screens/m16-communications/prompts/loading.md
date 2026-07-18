---
ui_yaml_sha: f1148bbba20463e7633391c7136c2911c2e4b3b393eedc8d015d2f357cbcd2d0
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: 873418114b5d97eb38347e5a46c640cdcac47be29a967ffc027375c26cbb71f8

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: skeleton_screen

feature: m16-communications
state: loading
state_visibility: loading

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m16-communications — loading state

> Auto-generated from screens/m16-communications/ui.yaml @ SHA 433171ef9c3f7756
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
1. **header** (#m16_header) — label: "{strings.m16_title}"
2. **banner** (#offline_banner) — label: "{strings.m16_offline_banner}"
3. **chip** (#comms_tabs) — label: "{strings.m16_tabs}", on_click: { action: switch_comms_tab }
4. **content_area** (#comms_content) — label: "{strings.m16_content_label}"
5. **list_item** (#campaign_row) — label: "{strings.m16_campaign_row}", on_click: { action: open_campaign_detail, target: m16-communications }
6. **fab** (#new_campaign_button) — label: "{strings.m16_new_campaign}", on_click: { action: create_campaign_form, target: dynamic-template-forms }
7. **button** (#edit_campaign_button) — label: "{strings.m16_edit_campaign}", on_click: { action: edit_campaign_form, target: dynamic-template-forms }
8. **button** (#activate_campaign_button) — label: "{strings.m16_activate_campaign}", on_click: { action: activate_campaign }
9. **button** (#close_campaign_button) — label: "{strings.m16_close_campaign}", on_click: { action: close_campaign }
10. **button** (#view_recipient_report_button) — label: "{strings.m16_view_report}", on_click: { action: view_recipient_report }
11. **button** (#new_template_button) — label: "{strings.m16_new_template}", on_click: { action: create_template_form, target: dynamic-template-forms }
12. **button** (#register_hook_button) — label: "{strings.m16_register_hook}", on_click: { action: register_hook_form, target: dynamic-template-forms }
13. **button** (#edit_email_config_button) — label: "{strings.m16_edit_email_config}", on_click: { action: save_email_config, target: dynamic-template-forms }
14. **button** (#review_failed_button) — label: "{strings.m16_review_failed}", on_click: { action: open_needs_attention, target: needs-attention-inbox }
15. **button** (#retry_button) — label: "{strings.m16_retry}", on_click: { action: retry_load }

## State-specific behavior
- Show shimmer/skeleton loaders matching the content layout block-for-block — no real text, no images. This is the screen's initial state.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("loading"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "master_detail" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
