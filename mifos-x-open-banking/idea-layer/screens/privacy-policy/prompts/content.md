---
ui_yaml_sha: 0c38e9435e7390ff01a27e8013761c2e727c06d118d7d9934a28dabd99123a2c
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: 396e31f9bca446703369dda1d2f227cc297c54d34c84812bd575572717d61739

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: settings

feature: privacy-policy
state: content
state_visibility: content

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# privacy-policy — content state

> Auto-generated from screens/privacy-policy/ui.yaml @ SHA 5b0d2eb236693825
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
1. **stack** (#pp_root) — 1 items: "Privacy Policy"
2. **banner** (#pp_gdpr_banner)
3. **text** (#pp_gdpr_banner_text) — content: "Mifos X Open Banking is an open-source UK Open Banking reference client, maintai"
4. **card** (#pp_data_collection_card)
5. **text** (#pp_data_collection_header) — content: "Data This App Touches"
6. **text** (#pp_data_collection_body) — content: "The app handles only what it needs: (a) Access tokens — issued by your bank afte"
7. **card** (#pp_lawful_basis_card)
8. **text** (#pp_lawful_basis_header) — content: "Lawful Basis for Processing"
9. **text** (#pp_lawful_basis_body) — content: "Where GDPR applies, processing rests on: (a) Contract performance — exchanging y"
10. **card** (#pp_purpose_card)
11. **text** (#pp_purpose_header) — content: "How Your Data Is Used"
12. **text** (#pp_purpose_body) — content: "Your sandbox credentials are sent once at sign-in and exchanged for a short-live"
13. **card** (#pp_local_storage_card)
14. **text** (#pp_local_storage_header) — content: "Where Your Data Lives"
15. **text** (#pp_local_storage_body) — content: "Your session token and preferences are kept in app-private storage on this devic"
16. **card** (#pp_diagnostics_card)
17. **text** (#pp_diagnostics_header) — content: "Diagnostics & Crash Reporting"
18. **text** (#pp_diagnostics_body) — content: "Builds of this app may include a diagnostics module that records crash reports a"
19. **card** (#pp_third_party_card)
20. **text** (#pp_third_party_header) — content: "Data Sharing"
21. **text** (#pp_third_party_body) — content: "Data leaves this app in exactly one direction: API requests to your bank's Open "
22. **card** (#pp_retention_card)
23. **text** (#pp_retention_header) — content: "Data Retention"
24. **text** (#pp_retention_body) — content: "Your banking data lives at your bank and follows its retention schedule — this a"
25. **card** (#pp_user_rights_card)
26. **text** (#pp_user_rights_header) — content: "Your Rights"
27. **text** (#pp_user_rights_body) — content: "Because personal data stays on your device, you can act on most rights directly:"
28. **card** (#pp_dpo_card)
29. **text** (#pp_dpo_header) — content: "Contact"
30. **text** (#pp_dpo_body) — content: "Mifos X Open Banking is community-maintained open-source software associated wit"
31. **text** (#pp_last_updated_text) — content: "Last updated: 28 May 2026 · Version 1.0"

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
