---
ui_yaml_sha: 28ffcedb3403fd8682d9a61f3b2c54646577285608ffa7ea0e6a08408ec45ddb
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: fb029041c6adc5374d84f58e9a9916a356b4e76d61202edc7e30a928be53c14d

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: list_screen

feature: m13-scheduler-jobs
state: content
state_visibility: content

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m13-scheduler-jobs — content state

> Auto-generated from screens/m13-scheduler-jobs/ui.yaml @ SHA 6264ea5d292db161
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
1. **header** (#scheduler_header) — label: "{strings.m13_title}"
2. **banner** (#offline_banner) — label: "{strings.m13_offline_banner}"
3. **switch** (#scheduler_master_switch) — label: "{strings.m13_scheduler_switch}", on_click: { action: toggle_scheduler }
4. **content_area** (#business_date_header) — label: "{strings.m13_business_date}"
5. **content_area** (#scheduler_content) — label: "{strings.m13_content_label}"
6. **list_item** (#job_row) — 8 items: "Loan Close Of Business", "Update Loan Arrears Ageing", "Apply Annual Fee For Savings", "Apply Charge To Overdue Savings Accounts", "Post Interest For Savings", "Recalculate Interest For Loans", "Update Non Performing Assets", "Execute Standing Instruction Renewal" …and 1 more similar cards
7. **chip** (#job_status_chip) — label: "{strings.m13_status_chip}"
8. **button** (#run_job_button) — label: "{strings.m13_run_job}", on_click: { action: execute_job }
9. **button** (#toggle_job_active_button) — label: "{strings.m13_toggle_active}", on_click: { action: toggle_job_active }
10. **button** (#edit_schedule_button) — label: "{strings.m13_edit_schedule}", on_click: { action: edit_job_schedule, target: dynamic-template-forms }
11. **button** (#advance_business_date_button) — label: "{strings.m13_advance_business_date}", on_click: { action: advance_business_date, target: dynamic-template-forms }
12. **button** (#view_run_history_button) — label: "{strings.m13_view_run_history}", on_click: { action: view_run_history }
13. **button** (#retry_button) — label: "{strings.m13_retry}", on_click: { action: retry_load }

## State-specific behavior
- Fully populated with the real demo content listed below.

## Content source manifest
- demo-data.jobs[0..7] (+1)

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
- [ ] **Archetype honored:** the layout follows the "list_screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
