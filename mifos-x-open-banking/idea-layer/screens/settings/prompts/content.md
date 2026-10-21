---
ui_yaml_sha: d12e75b67681b6679b10175fd57521fd220ccaff37b8ed05cb6705d09c96f19b
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: ada11dac6f0f5ef0cfde42a6dd3f68f20f8f2c29d9b1798f560ffb74ca77151a

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: settings

feature: settings
state: content
state_visibility: content

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# settings — content state

> Auto-generated from screens/settings/ui.yaml @ SHA f6d5a5d44fdd77c9
> Stitch DesignSystem: 2047482829824847747
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: settings

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **section_header** (#appearance_header) — label: "{strings.settings.section.appearance}"
2. **select** (#theme_row) — label: "{strings.settings.theme.label}", on_click: { action: togglethememenu }
3. **section_header** (#account_header) — label: "{strings.settings.section.account}"
4. **list_item** (#consents_row) — 3 items: "content", "empty", "error"
5. **section_header** (#about_header) — label: "{strings.settings.section.about_legal}"
6. **list_item** (#privacy_row) — 3 items: "content", "empty", "error"
7. **list_item** (#licences_row) — 3 items: "content", "empty", "error"
8. **list_item** (#app_version_row) — 3 items: "content", "empty", "error"
9. **empty_state** (#settings_empty) — title: "{strings.settings.empty.title}"
10. **error_state** (#settings_error) — "{strings.settings.error.title}"
   - **button** (#retry_button) — label: "{strings.settings.error.retry}", on_click: { action: retryload }

## State-specific behavior
- Fully populated with the real demo content listed below. This is the screen's initial state.

## Content source manifest
- demo-data.states[0..2]
- demo-data.states[0..2]
- demo-data.states[0..2]
- demo-data.states[0..2]

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
