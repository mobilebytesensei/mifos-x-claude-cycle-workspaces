---
ui_yaml_sha: a0a16e9421d9390ac64777fd44cedff6ee938d334ba08638215b73e5e4576512
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: 0db11ff295364066160af0b06e8bd00f10c8edd4cee31262b13c25a020187a92

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: empty_state

feature: m17-sync-settings
state: empty
state_visibility: empty

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m17-sync-settings — empty state

> Auto-generated from screens/m17-sync-settings/ui.yaml @ SHA 00306ff676507f64
> Stitch DesignSystem: 6486719301524192685
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Collections, Sync) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: settings_console

## Layout
- type: scrollable_column
- padding: default
- alignment: start

## Composition (top → bottom)
1. **header** (#sync_settings_header) — label: "{strings.m17_title}"
2. **status_banner** (#sync_status_banner) — label: "{strings.m17_sync_status}"
3. **content_area** (#settings_content) — label: "{strings.m17_content}"
4. **button** (#sync_now_button) — label: "{strings.m17_sync_now}", on_click: { action: trigger_sync }
5. **button** (#pull_latest_button) — label: "{strings.m17_pull_latest}", on_click: { action: trigger_delta_pull }
6. **list_item** (#needs_attention_entry) — label: "{strings.m17_needs_attention}", on_click: { action: open_needs_attention, target: needs-attention-inbox }
7. **list_item** (#switch_server_row) — label: "{strings.m17_switch_server}", on_click: { action: switch_tenant_server }
8. **list_item** (#clear_cache_row) — label: "{strings.m17_clear_cache}", on_click: { action: clear_reference_cache }
9. **list_item** (#refresh_reference_row) — label: "{strings.m17_refresh_reference}", on_click: { action: refresh_reference_data }
10. **switch** (#theme_toggle) — label: "{strings.m17_theme}", on_click: { action: toggle_theme }
11. **list_item** (#language_selector) — label: "{strings.m17_language}", on_click: { action: change_language }
12. **switch** (#biometric_lock_toggle) — label: "{strings.m17_biometric}", on_click: { action: toggle_biometric_lock }
13. **list_item** (#about_diagnostics_row) — label: "{strings.m17_about}", on_click: { action: open_about_diagnostics, target: m17-sync-settings }
14. **button** (#logout_button) — label: "{strings.m17_logout}", on_click: { action: logout, target: login-tenant }

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
- [ ] **Archetype honored:** the layout follows the "settings_console" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
