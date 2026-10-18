---
ui_yaml_sha: 96c765264083eb0d43850599756cc9befa717590136d3fbe8134eb87730aeae7
design_md_hash: c1e7dbe50f7725a08e0369f4cb0659b8c1e56ac645d128a4c90c66b8618666ef
app_shell_hash: db8da7f442f6b5759a907f50239088382e54225e9674781c0a8064f3ffd22bb0
design_read_hash: 
content_hash: e92a05a82d35054dc30686de9ddfd3a4d07499748846febf6d53fb661f5e38d7

design_read_aesthetic: taste-default
design_read_dials: {variance: 7, motion: 6, density: 4}
aesthetic_variant_override: null
archetype: form

feature: signin
state: success
state_visibility: success

project_id: '10780096558615730514'
design_system_id: '9551377288795375599'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.2.0
---

# signin — success state

> Auto-generated from screens/signin/ui.yaml @ SHA a1e14bc7bb21d8d0
> Stitch DesignSystem: 9551377288795375599
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.
> The concrete figures below are REALISTIC SAMPLE (demo) data, not fixed values — render believable content of the same KIND and MAGNITUDE (currency amounts, counts, percentages, names, timestamps). Exact reproduction is NOT required; realism and consistency ARE. Never use lorem, generic numbered placeholders, or empty content.
> **EXCEPTION — RENDER VERBATIM, NEVER SUBSTITUTE.** The licence above does NOT apply to any of the following, which must appear EXACTLY as declared, character for character, or be omitted entirely: emergency / crisis / helpline numbers and shortcodes (e.g. 988, 741741) and the ORGANISATION NAMES attached to them · legal, consent, privacy and medical-disclaimer text · medication names and dosages · security codes, auth codes and account identifiers. For these, a plausible substitute is a FABRICATION, not realism: inventing or renaming a crisis line sends a person in danger to something that does not answer. If such a value is absent from the declared data, render the element EMPTY and leave it visibly unresolved — never fill the gap with an invented one.

## Archetype: form

## Visual treatment (THIS SCREEN'S OWN brief — overrides the form archetype default; honor this hierarchy)
- A calm, confident CREDENTIAL screen for a field worker: generous vertical rhythm, one clear primary action, nothing competing with it. This is the first screen of a banking tool — it should read as trustworthy and quiet, not playful.
- Vertical order: a small instance chip at the very top, then the brand mark, then a two-line title, then the two fields, then the primary submit, then the biometric accelerator when present. A short legal consent line sits pinned at the bottom.
- The INSTANCE CHIP is the signature element and must not look like a button: a compact, low-contrast pill with a small server glyph showing host and tenant, with a subtle chevron implying it can be changed. It is information first and an affordance second.
- CLOSED SET — render EXACTLY the components listed in the Composition and NOTHING ELSE. Every element here maps to shipped code; an extra affordance is a claim this product does not support.
- DO NOT add: 'remember me', 'forgot password', 'create account'/'sign up', social or SSO buttons, a QR scanner, an offline-cache banner, an officer/employee ID field, a language picker, or a version footer. None of these exist.
- NO TOP APP BAR and no chrome above the instance chip: no gear, no overflow, no back arrow. This is the unauthenticated gate — there is nowhere to go back to.

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **assist_chip** (#instance_chip) — label: "apis.mifos.community · mifos-bank-1", on_click: { action: navigate, target: serverconfig }
2. **image** (#logo)
3. **text_block** (#title)
4. **outlined_text_field** (#username_field)
5. **outlined_text_field** (#password_field)
6. **button** (#login_button) — on_click: { action: submit, target: authenticate }
7. **legal_text** (#consent_text)

## State-specific behavior
- Custom state "Success" — render per the composition below.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("success"). Do not blend multiple states into one mockup.
- [ ] **Realistic content:** every text label and data point is realistic, believable, and consistent with the ILLUSTRATIVE sample content above (this project's own domain). Figures may differ from the samples as long as they are realistic and of the same kind/magnitude — verbatim reproduction is NOT required. NO lorem, NO generic numbered placeholders, NO empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "form" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.
- [ ] **Every affordance leads somewhere:** each button, link, tab and card that LOOKS interactive resolves to a real destination — a route in this project or a section on this page. Nothing is decorative-but-clickable, and nothing points at a page that does not exist.
- [ ] **No em-dashes:** the rendered output contains NO em-dash character. Use a colon, a comma, or a full stop instead — including inside <title>, headings, and any separator between a page name and the brand name.
- [ ] **One shape system:** corner radii come from at most THREE distinct values across the whole render. Do not mix many radii.
- [ ] **Responsive, phone-first:** the PRIMARY layout is the phone. Multi-column regions are only used where they genuinely read at phone width (a dense 2-column KPI grid is fine); anything wider must stack. Never assume a desktop viewport.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 10 checkpoints pass.

↑↑↑ MOCKUP PROMPT
