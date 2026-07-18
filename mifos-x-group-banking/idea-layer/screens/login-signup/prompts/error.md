---
ui_yaml_sha: 187cf02d3e5d03cbf806bef2fdb8df38b122d15c26dedf18d2c5e412a503d796
design_md_hash: c3a638b3a93523cbf2275539bdb5429cbf6921a4039cb7fbabc59f9d4146144f
app_shell_hash: 
design_read_hash: a302d6f69664249ea05a7525c838bbe835406f040bc22c6e6b0972a494796feb
content_hash: ac90fee48e92ce70ed38405b24085e58c85481220ec248d25f0eac6ef42750b0

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: error_state

feature: login-signup
state: error
state_visibility: error

project_id: 'null'
design_system_id: 'null'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# login-signup — error state

> Auto-generated from screens/login-signup/ui.yaml @ SHA dcd69d3a5c037463
> Stitch DesignSystem: (pending DESIGN.md upload — run /idea-feature-stitch sub-plan 02)
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: screen

## Layout
- type: scrollable_column
- padding: default
- alignment: start

## Composition (top → bottom)
1. **image** (#auth_header_logo)
2. **text** (#auth_title)
3. **tab-row** (#mode_toggle_tabs) — on_click: { action: onmodetoggle, target: login-signup }
4. **text-field** (#signup_name_field) — label: "{strings.field_name}", on_click: { action: onnamechange, target: login-signup }
5. **text-field** (#email_phone_field) — label: "{strings.field_email_phone}", on_click: { action: onemailphonechange, target: login-signup }
6. **text-field** (#password_field) — label: "{strings.field_password}", on_click: { action: onpasswordchange, target: login-signup }
7. **text-button** (#forgot_password_link) — label: "{strings.link_forgot_password}", on_click: { action: onforgotpassword, target: login-signup }
8. **button** (#login_button) — label: "{strings.btn_sign_in}", on_click: { action: onlogintap, target: personal-dashboard }
9. **button** (#signup_button) — label: "{strings.btn_create_account}", on_click: { action: onsignuptap, target: personal-dashboard }
10. **icon-button** (#biometric_unlock_button) — label: "{strings.btn_biometric}", icon: "fingerprint", on_click: { action: onbiometricunlock, target: personal-dashboard }
11. **banner** (#error_banner) — icon: "error_outline"
12. **divider-labeled** (#divider_or) — label: "{strings.divider_or}"
13. **image** (#zero_groups_illustration)
14. **text** (#zero_groups_title)
15. **text** (#zero_groups_body)
16. **button** (#create_group_button) — label: "{strings.btn_create_group}", on_click: { action: oncreategrouptap, target: group-type-picker }
17. **button** (#join_with_code_button) — label: "{strings.btn_join_with_code}", on_click: { action: onjoinwithcodetap, target: join-with-code }

## State-specific behavior
- Show an error illustration, a short message, and a single Retry action. No content rails visible.

## Content source manifest
- (no demo collections bound for this state)

## Components (vocabulary used in this prompt)
- (no named components extracted — see composition)

## Shell (app-shell resolved for this state)
- App-shell rules are defined per project; per-screen overrides are merged in.
- Render MUST keep nav/bar elements consistent with the resolved shell — present or absent, never partial.

## Tokens (design-tokens roles consumed)
- Colors: primary / secondary / surface / on-surface / on-surface-variant / error (M3 standard roles).
- Typography: body-large / title-large (M3 standard roles).
- Spacing: gap.sm / gap.md / gap.lg.
- ALL token references are by name from the uploaded design system — no hex literals, no inline size values.

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. If any fails, FIX the output and re-render.

- [ ] **Per-state shape:** the render shows ONLY this state ("error"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
