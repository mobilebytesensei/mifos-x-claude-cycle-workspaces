---
ui_yaml_sha: 1219b6ab049627e0bf57934c222b7fa1fdf650f4e69dfb0b9a1e6446687790a8
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: 8150e5604d442c49ca5daf0e0a3ebafec9f92c8be6cfb2d6dcc443bdbe67f300

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: mutation_console

feature: offline-sync-engine
state: idle
state_visibility: idle

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# offline-sync-engine — idle state

> Auto-generated from screens/offline-sync-engine/ui.yaml @ SHA b4bedd37600644ee
> Stitch DesignSystem: 6486719301524192685
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Collections, Sync) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: mutation_console

## Layout
- type: scrollable_column
- padding: default
- alignment: start

## Composition (top → bottom)
1. **header** (#sync_header) — label: "Sync"
2. **status_banner** (#sync_status_banner) — label: "Last synced · N pending · watermark age (freshness chip)"
3. **content_area** (#outbox_list) — label: "Pending outbox commands (idempotency key · action · entity · age · status)"
4. **list_item** (#outbox_command_row) — label: "One queued command row: action + entity + amount + relative age + status chip", on_click: { action: view_command_detail, target: needs-attention-inbox }
5. **button** (#sync_now_button) — label: "Sync now", on_click: { action: trigger_sync }
6. **button** (#pull_latest_button) — label: "Pull latest", on_click: { action: trigger_delta_pull }
7. **button** (#review_failed_button) — label: "Review failed", on_click: { action: open_needs_attention, target: needs-attention-inbox }
8. **button** (#retry_failed_button) — label: "Retry all", on_click: { action: retry_failed }

## State-specific behavior
- Custom state "Idle" — render per the composition below. This is the screen's initial state.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("idle"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "mutation_console" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
