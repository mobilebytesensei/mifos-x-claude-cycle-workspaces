---
ui_yaml_sha: ee1240b9da7ef5f6b0b547af7c1520884e5c0222a57bea3c341e39c009915c27
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: c401f59082f9e178cc01a7e2c000796c0c6ba63a1cd2d4e0ddb0687b6fd22f73

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: index_list

feature: consent-list
state: error_auth
state_visibility: error_auth

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# consent-list — error_auth state

> Auto-generated from screens/consent-list/ui.yaml @ SHA 1466d05565464e36
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
1. **progress_circular**
2. **banner** (#reconfirm_banner) — title: "{strings.consent_list_reconfirm_banner_title}", icon: "warning_amber"
3. **text** (#active_section_label) — content: "{strings.consent_list_section_active}"
4. **list** (#active_consents_list) — "active_consents_list"
   - **card** (#consent_card) — "consent_card"
      - **row** (#consent_card_header_row) — "consent_card_header_row"
         - **image** (#bank_logo)
         - **chip** (#status_chip) — label: "{item.Data.Status}", icon: "{item.status_icon}"
      - **chip** (#reconfirm_urgency_chip) — label: "{strings.consent_list_reconfirm_chip}", icon: "warning_amber"
      - **text** (#permission_summary) — content: "{strings.consent_list_permissions}"
      - **text** (#expiry_countdown) — content: "{strings.consent_list_expires_in}"
      - **text** (#granted_since) — content: "{strings.consent_list_connected_on}"
5. **divider** (#section_divider)
6. **text** (#history_section_label) — content: "{strings.consent_list_section_history}"
7. **list** (#history_consents_list) — "history_consents_list"
   - **card** (#history_consent_card) — "history_consent_card"
      - **row** (#history_card_header_row) — "history_card_header_row"
         - **image** (#bank_logo_history)
         - **chip** (#history_status_chip) — label: "{item.Data.Status}", icon: "{item.status_icon}"
      - **text** (#history_expiry_label) — content: "{strings.consent_list_expired_on}"
      - **text** (#history_connected_on) — content: "{strings.consent_list_connected_on}"
8. **empty_state** (#empty_state) — "{strings.consent_list_empty_title}"
   - **button** (#connect_button) — label: "{strings.consent_list_connect}", on_click: { action: navigate_connect, target: login }
9. **error_state** (#error_state) — "{strings.consent_list_error_title}"
   - **button** (#retry_button) — label: "{strings.consent_list_retry}", on_click: { action: retry_load }
10. **error_state** (#auth_error_state) — "{strings.consent_list_auth_error_title}"
   - **button** (#reauth_button) — label: "{strings.consent_list_reauth}", on_click: { action: navigate_reauth, target: login }

## State-specific behavior
- Show an error illustration, a short message, and a single Retry action. No content rails visible.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("error_auth"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "index_list" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
