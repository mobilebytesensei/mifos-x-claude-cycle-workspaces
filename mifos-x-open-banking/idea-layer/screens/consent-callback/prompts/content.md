---
ui_yaml_sha: c2f6f937de1106fab0c56bcefec63f1872fbcc86957e913aeffb7712571854b1
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: 5a3a5c5e16e7c1dec5b7d081f5aa3662449492fb01982b7db97877d095f48c10

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: empty_state

feature: consent-callback
state: content
state_visibility: content

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# consent-callback — content state

> Auto-generated from screens/consent-callback/ui.yaml @ SHA 9314fc9e289122a0
> Stitch DesignSystem: 2047482829824847747
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: empty_state

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **stack** (#loading_layout) — "loading_layout"
   - **progress_circular** (#loading_spinner)
   - **spacer**
   - **text** (#loading_headline) — content: "{strings.consent_callback_loading_title}"
   - **spacer**
   - **text** (#loading_body) — content: "{strings.consent_callback_loading_body}"
2. **stack** (#success_layout) — "success_layout"
   - **icon** (#success_icon)
   - **spacer**
   - **text** (#success_headline) — content: "{strings.consent_callback_success_title}"
   - **spacer**
   - **text** (#success_body) — content: "{strings.consent_callback_success_body}"
3. **empty_state** (#awaiting_state) — "{strings.consent_callback_awaiting_title}"
   - **button** (#poll_again_button) — label: "{strings.consent_callback_poll_again}", on_click: { action: poll_consent_status }
4. **error_state** (#error_state) — "{strings.consent_callback_error_title}"
   - **button** (#retry_button) — label: "{strings.consent_callback_retry}", on_click: { action: navigate_retry, target: login }
5. **error_state** (#access_denied_state) — "{strings.consent_callback_denied_title}"
   - **button** (#denied_cta_button) — label: "{strings.consent_callback_denied_cta}", on_click: { action: navigate_retry, target: login }
6. **error_state** (#security_error_state) — "{strings.consent_callback_security_error_title}"
   - **button** (#security_retry_button) — label: "{strings.consent_callback_security_cta}", on_click: { action: navigate_login, target: login }

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
- [ ] **Archetype honored:** the layout follows the "empty_state" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
