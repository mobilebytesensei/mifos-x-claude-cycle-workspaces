---
ui_yaml_sha: 081ce116fcd76039f9443f4d719819be752079e27aebc935d9dffc52dc44c151
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: ecbe8c25cf5b1f682a419cb6b1946e055cf17e3363bb3eb3962142948f114783

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: detail_screen

feature: m01-dashboard
state: content
state_visibility: content

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m01-dashboard — content state

> Auto-generated from screens/m01-dashboard/ui.yaml @ SHA f53dddb9d58a5ee4
> Stitch DesignSystem: 6486719301524192685
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Collections, Sync) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: detail_screen

## Layout
- type: scrollable_column
- padding: default
- alignment: start

## Composition (top → bottom)
1. **header** (#header) — label: "{strings.m01_title}"
2. **banner** (#offline_banner) — label: "{strings.m01_offline_banner}"
3. **content_area** (#tile_grid) — label: "{strings.m01_tile_grid}"
4. **card** (#kpi_portfolio_at_risk_card) — label: "{strings.m01_kpi_par}", on_click: { action: open_portfolio_at_risk, target: report-runner }
5. **card** (#kpi_active_clients_card) — label: "{strings.m01_kpi_active_clients}", on_click: { action: open_active_clients, target: client-list }
6. **card** (#kpi_collections_due_card) — label: "{strings.m01_kpi_collections_due}", on_click: { action: open_todays_route, target: collection-sheet }
7. **card** (#kpi_pending_approvals_card) — label: "{strings.m01_kpi_pending_approvals}", on_click: { action: open_checker_inbox, target: checker-inbox }
8. **tappable_card** (#quick_action_new_client_tile) — label: "{strings.m01_qa_new_client}", on_click: { action: quick_new_client, target: client-list }
9. **tappable_card** (#quick_action_take_repayment_tile) — label: "{strings.m01_qa_take_repayment}", on_click: { action: quick_take_repayment, target: loan-detail }
10. **content_area** (#recent_activity_list) — label: "{strings.m01_recent_activity}", on_click: { action: open_activity_item, target: needs-attention-inbox }
11. **button** (#retry_tile_button) — label: "{strings.m01_retry_tile}", on_click: { action: retry_failed_tile }
12. **button** (#retry_dashboard_button) — label: "{strings.m01_retry_dashboard}", on_click: { action: retry_dashboard }
13. **link** (#view_access_link) — label: "{strings.m01_view_access}", on_click: { action: view_access, target: permission-capability-engine }

## State-specific behavior
- Fully populated with the real demo content listed below.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("content"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "detail_screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
