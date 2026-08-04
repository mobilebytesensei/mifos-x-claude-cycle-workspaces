---
ui_yaml_sha: b46a9e7ad753c41978e967fee684645a38ab88ab9031299135ddd5ad813993a1
design_md_hash: 98bff520251b13fe61807f051f0971a6fd7f5cd1364b4d5c1317bdd6df16612d
app_shell_hash: 3b51792a3cf0662637b47a6b9105fb9030edf792e8caad095b354b7f26ea4461
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: 7c79d0ba068549ffab90117b2545977c25ab713b2f738c2d6e0e9267f63787b8

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: dashboard

feature: m01-dashboard
state: content
state_visibility: content

project_id: '10243803383444073820'
design_system_id: '15272366959787234099'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m01-dashboard — content state

> Auto-generated from screens/m01-dashboard/ui.yaml @ SHA f67014d7dc76aa56
> Stitch DesignSystem: 15272366959787234099
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Collections, Sync) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.
> The concrete figures below are REALISTIC SAMPLE (demo) data, not fixed values — render believable content of the same KIND and MAGNITUDE (currency amounts, counts, percentages, names, timestamps). Exact reproduction is NOT required; realism and consistency ARE. Never use lorem, generic numbered placeholders, or empty content.

## Archetype: dashboard

## Visual treatment (professional design brief — honor this hierarchy)
- Lead with ONE bold summary HERO for the primary KPI — a full-width brand-gradient card (`gradient-hero-from`→`gradient-hero-to`, `on-hero` text) with the value in the display scale and a subtle sparkline; it must visually dominate.
- Below the hero, a tidy responsive GRID of secondary stat cards — each an elevated `surface` card with a small colored icon chip (`chart-1`..`chart-5`), the value large in tabular-mono, and a muted caption.
- Then a compact QUICK-ACTIONS row (icon-over-label buttons in `primary-container`), then a clean RECENT-ACTIVITY list (leading status icon, primary text, trailing timestamp).
- Hierarchy is everything: hero dominates, stat cards are calm and equal, generous spacing, all numerics tabular-mono. App-Store-screenshot fidelity — professional, airy, one focal gradient and the rest typographic.

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **header** (#header) — label: "{strings.m01_title}"
2. **banner** (#offline_banner) — label: "{strings.m01_offline_banner}"
3. **content_area** (#tile_grid) — label: "{strings.m01_tile_grid}"
4. **card** (#kpi_portfolio_at_risk_card) — "Portfolio at Risk" = 4.2% (PAR30 · all offices)
     → RENDER AS a full-width HERO card with a brand gradient background (linear-gradient from token `gradient-hero-from` to `gradient-hero-to`), `on-hero` text, elevated rounded-xl; the metric value in the display type scale (bold, tabular-mono), the label small UPPERCASE above it, the subtitle at reduced opacity; add a subtle light sparkline/area line across the bottom. (emphasis: hero)
5. **card** (#kpi_active_clients_card) — "Active Clients" = 18,204 (across 12 branches)
     → RENDER AS an elevated stat card (`surface`, elevation token, rounded-lg): a small colored icon chip (from the `chart-1`..`chart-5` data-viz palette) beside a muted label, the metric value large in tabular-mono, a caption below. (emphasis: primary)
6. **card** (#kpi_collections_due_card) — "Collections Due Today" = KES 1,940,500 (612 dues)
     → RENDER AS an elevated stat card (`surface`, elevation token, rounded-lg): a small colored icon chip (from the `chart-1`..`chart-5` data-viz palette) beside a muted label, the metric value large in tabular-mono, a caption below. (emphasis: primary)
7. **card** (#kpi_pending_approvals_card) — "Approvals Waiting" = 37 (maker-checker queue)
     → RENDER AS an elevated stat card (`surface`, elevation token, rounded-lg): a small colored icon chip (from the `chart-1`..`chart-5` data-viz palette) beside a muted label, the metric value large in tabular-mono, a caption below. (emphasis: primary)
8. **tappable_card** (#quick_action_new_client_tile) — "New Client"
9. **tappable_card** (#quick_action_take_repayment_tile) — "Take Repayment"
10. **content_area** (#recent_activity_list) — label: "{strings.m01_recent_activity}", on_click: { action: open_activity_item, target: needs-attention-inbox }
11. **button** (#retry_tile_button) — label: "{strings.m01_retry_tile}", on_click: { action: retry_failed_tile }
12. **button** (#retry_dashboard_button) — label: "{strings.m01_retry_dashboard}", on_click: { action: retry_dashboard }
13. **link** (#view_access_link) — label: "{strings.m01_view_access}", on_click: { action: view_access, target: permission-capability-engine }

## State-specific behavior
- Fully populated with the real demo content listed below.

## Content source manifest
- demo-data.items[persona].tiles.kpi_par
- demo-data.items[persona].tiles.kpi_active_clients
- demo-data.items[persona].tiles.kpi_collections_due
- demo-data.items[persona].tiles.kpi_pending_approvals
- demo-data.items[persona].tiles.qa_new_client
- demo-data.items[persona].tiles.qa_take_repayment

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
- [ ] **Realistic content:** every text label and data point is realistic, believable, and consistent with the ILLUSTRATIVE sample content above (a microfinance back-office). Figures may differ from the samples as long as they are realistic and of the same kind/magnitude — verbatim reproduction is NOT required. NO lorem, NO generic numbered placeholders, NO empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "dashboard" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
