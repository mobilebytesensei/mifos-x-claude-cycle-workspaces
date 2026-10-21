---
ui_yaml_sha: 1ebebde0f4a338d4bc5dbcfdf4fe8afef040c43da675dc53dfcd079ade3a5df4
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: febdf8929f602576a19f65417b6401022c3a0af390b9c1786dd39057c433ab66

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: settings

feature: about
state: content
state_visibility: content

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# about — content state

> Auto-generated from screens/about/ui.yaml @ SHA 0de23b5458328123
> Stitch DesignSystem: 2047482829824847747
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: settings

## Layout
- type: column
- padding: spacing.lg
- alignment: start
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **stack** (#about_root)
2. **stack** (#about_logo_section)
3. **image** (#about_logo_image) — label: "Mifos X logo", content: "account_balance"
4. **text** (#about_app_name_text) — content: "Mifos X Open Banking"
5. **text** (#about_tagline_text) — content: "Open Banking for Everyone"
6. **text** (#about_version_inline) — content: "Version 1.0.0"
7. **card** (#about_app_info_card)
8. **text** (#about_app_info_header) — content: "App"
9. **stack** (#about_version_row)
10. **text** (#about_version_label) — content: "Version"
11. **text** (#about_version_value) — content: "1.0.0"
12. **divider** (#about_divider_1)
13. **stack** (#about_license_row)
14. **text** (#about_license_label) — content: "License"
15. **text** (#about_license_value) — content: "MPL-2.0"
16. **divider** (#about_divider_2)
17. **stack** (#about_platform_row)
18. **text** (#about_platform_label) — content: "Platform"
19. **text** (#about_platform_value) — content: "Kotlin Multiplatform"
20. **card** (#about_project_card)
21. **text** (#about_project_header) — content: "About this app"
22. **text** (#about_project_body) — content: "Mifos X Open Banking is an open-source UK Open Banking reference client. It show"
23. **text** (#about_mifos_subheading) — content: "The Mifos Initiative"
24. **text** (#about_mifos_body) — content: "Built and maintained by the Mifos Initiative, a global community working to expa"
25. **text** (#about_openbanking_subheading) — content: "HSBC UK Open Banking sandbox"
26. **text** (#about_openbanking_body) — content: "All account, transaction, and payee data shown in this app comes from the HSBC U"
27. **card** (#about_legal_card)
28. **text** (#about_legal_header) — content: "Legal & resources"
29. **stack** (#about_mifos_link_row)
30. **link** (#about_mifos_link) — label: "Mifos Initiative", on_click: { action: open_external, target: https-mifos-org }
31. **icon** (#about_mifos_link_icon) — content: "open_in_new"
32. **divider** (#about_divider_3)
33. **stack** (#about_openbanking_link_row)
34. **link** (#about_openbanking_link) — label: "HSBC Open Banking developer portal", on_click: { action: open_external, target: https-develop-hsbc-com }
35. **icon** (#about_openbanking_link_icon) — content: "open_in_new"
36. **divider** (#about_divider_4)
37. **stack** (#about_github_link_row)
38. **link** (#about_github_link) — label: "Source code on GitHub", on_click: { action: open_external, target: https-github-com-openmf }
39. **icon** (#about_github_link_icon) — content: "open_in_new"
40. **divider** (#about_divider_5)
41. **stack** (#about_mpl_link_row)
42. **link** (#about_mpl_link) — label: "Mozilla Public License 2.0", on_click: { action: open_external, target: https-mozilla-org-mpl-2-0 }
43. **icon** (#about_mpl_link_icon) — content: "open_in_new"
44. **text** (#about_attribution) — content: "Made with Kotlin Multiplatform and Compose Multiplatform by the Mifos community."

## State-specific behavior
- Fully populated with the real demo content listed below. This is the screen's initial state.

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
- [ ] **Archetype honored:** the layout follows the "settings" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
