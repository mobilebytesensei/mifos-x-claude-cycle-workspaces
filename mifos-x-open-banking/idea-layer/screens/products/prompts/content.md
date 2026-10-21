---
ui_yaml_sha: ca9a781f66fbed410849961f64b3552e9a1ff91dcc8b58452bedbfd5939f162e
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: ea5a852e2b9ba977559b6552eb1b460f9cfdeb3537ecdd66c7fb74cd00eec0ef

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: index_list

feature: products
state: content
state_visibility: content

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# products — content state

> Auto-generated from screens/products/ui.yaml @ SHA 7f29f533aaf0c92b
> Stitch DesignSystem: 2047482829824847747
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: index_list

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **text** (#products_title) — label: "Products", content: "Products"
2. **text** (#products_public_caption) — label: "Public catalogue caption", content: "Published product information from HSBC UK and first direct. No sign-in needed."
3. **tab_bar** (#products_family_tabs) — label: "Product family tabs", on_click: { action: onfamilyselected }
4. **text** (#products_tab_personal) — label: "Personal", content: "Personal", on_click: { action: onfamilyselected, target: pca }
5. **text** (#products_tab_business) — label: "Business", content: "Business", on_click: { action: onfamilyselected, target: bca }
6. **text** (#products_tab_cards) — label: "Commercial cards", content: "Commercial cards", on_click: { action: onfamilyselected, target: ccc }
7. **text** (#products_tab_loans) — label: "Business loans", content: "Business loans", on_click: { action: onfamilyselected, target: smel }
8. **chip_group** (#products_segment_chips) — label: "Segment filter", on_click: { action: onsegmentselected }
9. **chip** (#products_segment_chip) — label: "Segment", content: "Segment", on_click: { action: onsegmentselected, target: segment }
10. **text** (#products_brand_heading) — label: "Brand", content: "Brand"
11. **card** (#product_card) — label: "Product", content: "Product", on_click: { action: open_url, target: product_url }
12. **text** (#product_name) — label: "Product name", content: "Product name"
13. **badge** (#product_offer_badge) — label: "Offer", content: "Offer"
14. **badge** (#product_segment_badge) — label: "Segment", content: "Segment"
15. **text** (#product_more_info) — label: "More info", content: "More info", on_click: { action: open_url, target: product_url }
16. **text** (#products_family_load_failed) — label: "Couldn't load these products", content: "Couldn't load these products"
17. **button** (#products_family_retry) — label: "Try again", content: "Try again", on_click: { action: onretry }
18. **text** (#products_segment_empty) — label: "No products in this segment", content: "No products in this segment"

## State-specific behavior
- Fully populated with the real demo content listed below.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("content"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "index_list" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
