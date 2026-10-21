---
ui_yaml_sha: 85be878bd98970c57b1c3c202edb4d79a594f45200c8e5f7afe783f8e108cf64
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: 03245ddf362d914075927c35122ed3d40b907c8936c99d3683c50764677a0742

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: settings

feature: terms-of-service
state: content
state_visibility: content

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# terms-of-service — content state

> Auto-generated from screens/terms-of-service/ui.yaml @ SHA 5c825df24495a001
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
1. **stack** (#tos_root) — 1 items: "Terms of Service"
2. **card** (#tos_intro_card)
3. **text** (#tos_intro_header) — content: "Agreement Overview"
4. **text** (#tos_intro_body) — content: "These Terms of Service govern your use of Mifos X Open Banking, an open-source U"
5. **card** (#tos_acceptance_card)
6. **text** (#tos_acceptance_header) — content: "1. Acceptance of Terms"
7. **text** (#tos_acceptance_body) — content: "By installing the app, granting it an Open Banking consent at your bank, or othe"
8. **card** (#tos_demo_service_card)
9. **text** (#tos_demo_service_header) — content: "2. A Demonstration Service, Not a Real Bank"
10. **text** (#tos_demo_service_body) — content: "Mifos X Open Banking is a reference application. It is not a bank and never hold"
11. **card** (#tos_account_usage_card)
12. **text** (#tos_account_usage_header) — content: "3. Accounts and Credentials"
13. **text** (#tos_account_usage_body) — content: "Access is granted by the consent you approve at your bank. This app has no accou"
14. **card** (#tos_prohibited_card)
15. **text** (#tos_prohibited_header) — content: "4. Acceptable Use"
16. **text** (#tos_prohibited_body) — content: "You agree not to: (a) attack, overload, or attempt to circumvent the security co"
17. **card** (#tos_licensing_card)
18. **text** (#tos_licensing_header) — content: "5. Open-Source Licensing and Intellectual Property"
19. **text** (#tos_licensing_body) — content: "The source code of Mifos X Open Banking is licensed under the Mozilla Public Lic"
20. **card** (#tos_data_handling_card)
21. **text** (#tos_data_handling_header) — content: "6. Sandbox Data"
22. **text** (#tos_data_handling_body) — content: "Anything you enter into the app — a payee's details, an amount, a payment refere"
23. **card** (#tos_warranty_card)
24. **text** (#tos_warranty_header) — content: "7. Disclaimer of Warranty"
25. **text** (#tos_warranty_body) — content: "The app and the sandbox services behind it are provided "as is" and "as availabl"
26. **card** (#tos_liability_card)
27. **text** (#tos_liability_header) — content: "8. Limitation of Liability"
28. **text** (#tos_liability_body) — content: "To the maximum extent permitted by applicable law, the Mifos Initiative and the "
29. **card** (#tos_changes_card)
30. **text** (#tos_changes_header) — content: "9. Changes to These Terms"
31. **text** (#tos_changes_body) — content: "These terms may be revised as the demonstration evolves. Material changes are an"
32. **card** (#tos_contact_card)
33. **text** (#tos_contact_header) — content: "10. Contact"
34. **text** (#tos_contact_body) — content: "Questions about these terms are welcome through the Mifos Initiative community a"
35. **text** (#tos_last_updated_text) — content: "Last updated: 28 May 2026 — Version 1.0"

## State-specific behavior
- Fully populated with the real demo content listed below. This is the screen's initial state.

## Content source manifest
- demo-data.document_metadata[0..0]

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
