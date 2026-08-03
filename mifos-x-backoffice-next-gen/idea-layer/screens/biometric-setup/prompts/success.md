---
ui_yaml_sha: 57719758961245d30c066131020d2b8c70c9cc451cd083d519273e8bd10d0cbf
design_md_hash: 2afa0f4eedf3e819ca6989ce07e731bc233c9ae41f84fea348d1aede1a951d47
app_shell_hash: 3b51792a3cf0662637b47a6b9105fb9030edf792e8caad095b354b7f26ea4461
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: 4c0aa0254d5b7aa4391d77ea3a3b12a25f381d4d6b6d178101b1f352bbcd19c4

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: success_state

feature: biometric-setup
state: success
state_visibility: success

project_id: '10243803383444073820'
design_system_id: '312064780206383264'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# biometric-setup — success state

> Auto-generated from screens/biometric-setup/ui.yaml @ SHA 30a7ab969f3d61a4
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
1. **header** (#header) — label: "{strings.biometric_setup_title}"
2. **image** (#illustration) — label: "{strings.biometric_setup_illustration}"
3. **text** (#description_text) — label: "{strings.biometric_setup_description}"
4. **button** (#enroll_button) — label: "{strings.biometric_setup_enroll}", on_click: { action: start_enrollment }
5. **button** (#skip_button) — label: "{strings.biometric_setup_skip}", on_click: { action: skip_enrollment }
6. **button** (#open_os_settings_button) — label: "{strings.biometric_setup_open_settings}", on_click: { action: open_device_security_settings }
7. **button** (#done_button) — label: "{strings.biometric_setup_done}", on_click: { action: finish_setup }
8. **button** (#retry_button) — label: "{strings.biometric_setup_retry}", on_click: { action: start_enrollment }

## State-specific behavior
- Custom state "Success" — render per the composition below.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("success"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "form_screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
