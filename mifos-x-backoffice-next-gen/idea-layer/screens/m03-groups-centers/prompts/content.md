---
ui_yaml_sha: 18a697e54e948053fcc642bf834ee31cc46c30a0d8df677fbbf4a44aaf925d2c
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: 037baf44fc2d84571e1ac02f537478842f86552d8da8c41e2ba44c11fb9659ce

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: master_detail

feature: m03-groups-centers
state: content
state_visibility: content

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m03-groups-centers — content state

> Auto-generated from screens/m03-groups-centers/ui.yaml @ SHA a09432736d402540
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
1. **header** (#header) — label: "{strings.m03_title}"
2. **tab_bar** (#scope_tabs) — label: "{strings.m03_scope_tabs}", on_click: { action: switch_scope_tab, target: content }
3. **content_area** (#content_area) — label: "Center/group list (office-scoped) — or a group/center detail with members, group"
4. **list_item** (#group_center_row) — 1 items: "Kibera Women's Cluster"
5. **list_item** (#member_row) — 3 items: "Grace Wanjiru Mwangi", "Samuel Otieno Odhiambo", "Amina Hassan Ali"
6. **toggle** (#attendance_toggle) — label: "Per-member present/absent toggle for the selected meeting", on_click: { action: toggle_member_attendance, target: content }
7. **button** (#save_attendance_button) — label: "{strings.m03_save_attendance}", on_click: { action: save_attendance }
8. **button** (#activate_button) — label: "{strings.m03_activate}", on_click: { action: activate_group_center }
9. **button** (#assign_staff_button) — label: "{strings.m03_assign_staff}", on_click: { action: assign_staff, target: dynamic-template-forms }
10. **button** (#manage_members_button) — label: "{strings.m03_manage_members}", on_click: { action: manage_members, target: m02-clients }
11. **fab** (#create_group_center_fab) — label: "{strings.m03_new_group_center}", on_click: { action: start_group_center_creation, target: dynamic-template-forms }
12. **button** (#retry_button) — label: "{strings.m03_retry}", on_click: { action: retry_load, target: loading }

## State-specific behavior
- Fully populated with the real demo content listed below.

## Content source manifest
- demo-data.centers[0..0]
- demo-data.members[0..2]

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
