---
ui_yaml_sha: 8737ec7faf014eddb71f22b022a3172f8c2e6ab6bf756d2e56d19ee3a714c20b
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: 2e2a1b81b1237e02e19483d4488d256bf9b95ccf326f8025e0e2c72be7c02311

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: skeleton_screen

feature: product
state: loading
state_visibility: loading

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# product — loading state

> Auto-generated from screens/product/ui.yaml @ SHA 4385147142d7d7ca
> Stitch DesignSystem: 2047482829824847747
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: detail_screen

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **progress_circular**
2. **card** (#product_header_card) — "product_header_card"
   - **text** (#product_type_label) — content: "{product.ProductType}"
   - **text** (#product_name) — content: "{product.ProductName}"
   - **text** (#product_id) — content: "{strings.product_id_label}"
3. **section_header** (#fees_header) — label: "{strings.product_section_fees}"
4. **list_item** (#monthly_max_charge_row)
5. **section_header** (#credit_interest_header) — label: "{strings.product_section_credit_interest}"
6. **list** (#credit_interest_list) — "credit_interest_list"
   - **list** (#tier_band_list) — "tier_band_list"
      - **list_item** (#tier_band_row)
7. **section_header** (#overdraft_header) — label: "{strings.product_section_overdraft}"
8. **list** (#overdraft_list) — "overdraft_list"
   - **list** (#overdraft_tier_list) — "overdraft_tier_list"
      - **list_item** (#overdraft_tier_row)
9. **section_header** (#features_header) — label: "{strings.product_section_features}"
10. **list** (#features_list) — "features_list"
   - **list_item** (#feature_row)
11. **empty_state** (#empty_product_state) — title: "{strings.product_empty_title}", icon: "info_outline"
12. **error_state** (#error_state) — "{strings.product_error_title}"
   - **button** (#retry_button) — label: "{strings.product_retry_button}", on_click: { action: retry_load }

## State-specific behavior
- Show shimmer/skeleton loaders matching the content layout block-for-block — no real text, no images. This is the screen's initial state.

## Content source manifest
- (no demo collections bound for this state)

## Components (vocabulary used in this prompt)
- (no named components extracted — see composition)

## Shell (app-shell resolved for this state)
- Home: navigates to home
- Accounts: navigates to accounts
- Pay: navigates to payments
- More: navigates to settings
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
- [ ] **Archetype honored:** the layout follows the "detail_screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
