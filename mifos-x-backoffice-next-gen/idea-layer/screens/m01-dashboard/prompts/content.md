---
ui_yaml_sha: b46a9e7ad753c41978e967fee684645a38ab88ab9031299135ddd5ad813993a1
design_md_hash: c7c22ff8e82c0a6bfeee29f51754cf9c892fb87c09b4c35a9735c17d9b5a66c2
app_shell_hash: 3b51792a3cf0662637b47a6b9105fb9030edf792e8caad095b354b7f26ea4461
design_read_hash: 8b8137721c408df984b6d20181ea8393668f91b1d4eb021ca164b01c647e8a44
content_hash: 9e02ae3881470654d935eea592710543952b02888864d4f310d40ce22ef139f0

design_read_aesthetic: premium-material
design_read_dials: {variance: 6, motion: 4, density: 7}
aesthetic_variant_override: null
archetype: dashboard

feature: m01-dashboard
state: content
state_visibility: content

project_id: '10243803383444073820'
design_system_id: '15039232982240872325'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.1.0
---

# m01-dashboard — content state

> Auto-generated from screens/m01-dashboard/ui.yaml @ SHA c9f38d1a10271172
> Stitch DesignSystem: 15039232982240872325
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Collections, Sync) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.
> The concrete figures below are REALISTIC SAMPLE (demo) data, not fixed values — render believable content of the same KIND and MAGNITUDE (currency amounts, counts, percentages, names, timestamps). Exact reproduction is NOT required; realism and consistency ARE. Never use lorem, generic numbered placeholders, or empty content.

## Archetype: dashboard

## Visual treatment (professional design brief — honor this hierarchy)
- Lead with ONE bold summary HERO for the primary KPI — a full-width brand-gradient card (`gradient-hero-from`→`gradient-hero-to`, `on-hero` text) with the value in the display scale and a subtle sparkline; it must visually dominate.
- Below the hero, a responsive GRID of secondary stat cards — each a `surface` tile LIFTED BY A SOFT DROP SHADOW (raised, NOT flat outline-bordered boxes), generously rounded, with a colored icon chip (`chart-1`..`chart-5`), the value large in tabular-mono, a muted caption.
- Then a compact QUICK-ACTIONS row (icon-over-label buttons in `primary-container`), then a clean RECENT-ACTIVITY list (leading status icon, primary text, trailing timestamp) in its own softly-elevated card.
- Hierarchy is everything: hero dominates, stat cards equal and softly elevated, generous spacing and rounding, numerics tabular-mono. App-Store fidelity — premium and polished; one focal gradient, the rest clean surfaces lifted by soft shadow.

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: the primary HERO card spans FULL WIDTH; the secondary KPI/stat cards form a COMPACT 2-COLUMN GRID (2×2 for four cards) that is INTENDED and RETAINED at phone width — this dense KPI grid IS the professional dashboard layout, so do NOT collapse the stat cards to a single column. Only genuine list/activity regions remain single-column.
- grid-fit: a stat card whose value is a LONG amount (large currency figure like a full monetary total) MUST span the FULL grid width (both columns) so the figure never truncates, wraps awkwardly, or overflows its cell; compact KPIs (counts, short percentages, small integers) sit two-per-row. Keep every numeric value and its trailing badge fully inside its card — nothing may spill past the card edge.

## Composition (top → bottom)
1. **header** (#header) — label: "{strings.m01_title}"
2. **banner** (#offline_banner) — label: "{strings.m01_offline_banner}"
3. **content_area** (#tile_grid) — label: "{strings.m01_tile_grid}"
4. **card** (#kpi_portfolio_at_risk_card) — "Portfolio at Risk" = 4.2% (PAR30 · all offices)
     → RENDER AS a full-width HERO card with a brand gradient background (linear-gradient from token `gradient-hero-from` to `gradient-hero-to`), `on-hero` text, elevated rounded-xl; the metric value in the display type scale (bold, tabular-mono), the label small UPPERCASE above it, the subtitle at reduced opacity; add a subtle light sparkline/area line across the bottom. (emphasis: hero)
5. **card** (#kpi_active_clients_card) — "Active Clients" = 18,204 (across 12 branches)
     → RENDER AS a soft-shadow-raised `surface` stat card (rounded-lg, NOT flat-bordered): a colored icon chip (`chart-1`..`chart-5`) beside a muted label, the value large in tabular-mono, a caption below. (emphasis: primary)
6. **card** (#kpi_collections_due_card) — "Collections Due Today" = KES 1,940,500 (612 dues)
     → RENDER AS a soft-shadow-raised `surface` stat card (rounded-lg, NOT flat-bordered): a colored icon chip (`chart-1`..`chart-5`) beside a muted label, the value large in tabular-mono, a caption below. (emphasis: primary)
7. **card** (#kpi_pending_approvals_card) — "Approvals Waiting" = 37 (maker-checker queue)
     → RENDER AS a soft-shadow-raised `surface` stat card (rounded-lg, NOT flat-bordered): a colored icon chip (`chart-1`..`chart-5`) beside a muted label, the value large in tabular-mono, a caption below. (emphasis: primary)
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
