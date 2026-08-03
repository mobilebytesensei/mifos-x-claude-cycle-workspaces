---
ui_yaml_sha: d42abf3996d0d3264dc67d4123e88fdc30346e1c84cbd3f817c12dace8801789
design_md_hash: 2afa0f4eedf3e819ca6989ce07e731bc233c9ae41f84fea348d1aede1a951d47
app_shell_hash: 3b51792a3cf0662637b47a6b9105fb9030edf792e8caad095b354b7f26ea4461
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: 4e1cfd57bf207df62c7d1e3a27703ff5a027740e850740c118c079ab88c09411

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: form_screen

feature: product-editor
state: saving
state_visibility: saving

project_id: '10243803383444073820'
design_system_id: '312064780206383264'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# product-editor — saving state

> Auto-generated from screens/product-editor/ui.yaml @ SHA 343656512a8f4398
> Stitch DesignSystem: 312064780206383264
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Collections, Sync) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: form_screen

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **expandable_section** (#pe_section) — label: "{strings.prodedit_section}", on_click: { action: expand_section, target: product-editor }
2. **dynamic_form_field** (#pe_field) — label: "{strings.prodedit_field}", on_click: { action: field_change, target: product-editor }
3. **dropdown_select** (#pe_currency_select) — label: "{strings.prodedit_currency}", on_click: { action: select_currency, target: product-editor }
4. **dropdown_select** (#pe_amortisation_select) — label: "{strings.prodedit_amortisation}", on_click: { action: select_amortisation, target: product-editor }
5. **dropdown_select** (#pe_interest_type_select) — label: "{strings.prodedit_interest_type}", on_click: { action: select_interest_type, target: product-editor }
6. **dropdown_select** (#pe_accounting_rule_select) — label: "{strings.prodedit_accounting_rule}", on_click: { action: select_accounting_rule, target: product-editor }
7. **button** (#pe_add_charge) — label: "{strings.prodedit_add_charge}", on_click: { action: add_charge, target: product-editor }
8. **icon_button** (#pe_remove_charge) — label: "{strings.prodedit_remove_charge}", on_click: { action: remove_charge, target: product-editor }
9. **dropdown_select** (#pe_gl_mapping) — label: "{strings.prodedit_gl_mapping}", on_click: { action: edit_gl_mapping, target: product-editor }
10. **button** (#pe_validate) — label: "{strings.prodedit_validate}", on_click: { action: validate_form, target: product-editor }
11. **button** (#pe_save) — label: "{strings.prodedit_save}", on_click: { action: save_product, target: product-editor }
12. **button** (#pe_cancel) — label: "{strings.prodedit_cancel}", on_click: { action: cancel, target: m08-products-charges }
13. **button** (#pe_error_retry) — label: "{strings.prodedit_retry}", on_click: { action: retry, target: product-editor }

## State-specific behavior
- Custom state "Saving" — render per the composition below.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("saving"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "form_screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
