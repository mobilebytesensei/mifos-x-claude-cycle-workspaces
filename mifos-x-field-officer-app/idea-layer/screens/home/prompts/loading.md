---
ui_yaml_sha: 86f8421ce713115bc2bfbea9e46365b0aec4c3aadc01880564ecc3d7d29964db
design_md_hash: c1e7dbe50f7725a08e0369f4cb0659b8c1e56ac645d128a4c90c66b8618666ef
app_shell_hash: db8da7f442f6b5759a907f50239088382e54225e9674781c0a8064f3ffd22bb0
design_read_hash: 
content_hash: 19b95db20534e5b1e84622bff1ff148ad164467e8203fc57571799932a424294

design_read_aesthetic: taste-default
design_read_dials: {variance: 7, motion: 6, density: 4}
aesthetic_variant_override: null
archetype: skeleton_screen

feature: home
state: loading
state_visibility: loading

project_id: '10780096558615730514'
design_system_id: '9551377288795375599'

generated_by: stitch-prompt-build.ts v2.1.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.2.0
---

# home — loading state

> Auto-generated from screens/home/ui.yaml @ SHA be5169c7414068e9
> Stitch DesignSystem: 9551377288795375599
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Profile) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.
> The concrete figures below are REALISTIC SAMPLE (demo) data, not fixed values — render believable content of the same KIND and MAGNITUDE (currency amounts, counts, percentages, names, timestamps). Exact reproduction is NOT required; realism and consistency ARE. Never use lorem, generic numbered placeholders, or empty content.
> **EXCEPTION — RENDER VERBATIM, NEVER SUBSTITUTE.** The licence above does NOT apply to any of the following, which must appear EXACTLY as declared, character for character, or be omitted entirely: emergency / crisis / helpline numbers and shortcodes (e.g. 988, 741741) and the ORGANISATION NAMES attached to them · legal, consent, privacy and medical-disclaimer text · medication names and dosages · security codes, auth codes and account identifiers. For these, a plausible substitute is a FABRICATION, not realism: inventing or renaming a crisis line sends a person in danger to something that does not answer. If such a value is absent from the declared data, render the element EMPTY and leave it visibly unresolved — never fill the gap with an invented one.

## Archetype: skeleton_screen

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **header** (#header) — title: "Good morning, Irving", subtitle: "CENTRAL · Mon 26 Oct 2026 · Mifos field officer gateway"
2. **shimmer** (#card_skeletons)

## State-specific behavior
- Show shimmer/skeleton loaders matching the content layout block-for-block — no real text, no images. This is the screen's initial state.

## Content source manifest
- (no demo collections bound for this state)

## Components (vocabulary used in this prompt)
- header
- shimmer

## Shell (app-shell resolved for this state)
- Home: navigates to home
- Clients: navigates to clients
- Profile: navigates to profile
- Render MUST keep nav/bar elements consistent with the list above — present or absent, never partial.

## Tokens (design-tokens roles consumed)
- Colors: primary / secondary / surface / on-surface / on-surface-variant / error (M3 standard roles).
- Typography: body-large / title-large (M3 standard roles).
- Spacing: gap.sm / gap.md / gap.lg.
- ALL token references are by name from the uploaded design system — no hex literals, no inline size values.

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. If any fails, FIX the output and re-render.

- [ ] **Per-state shape:** the render shows ONLY this state ("loading"). Do not blend multiple states into one mockup.
- [ ] **Realistic content:** every text label and data point is realistic, believable, and consistent with the ILLUSTRATIVE sample content above (this project's own domain). Figures may differ from the samples as long as they are realistic and of the same kind/magnitude — verbatim reproduction is NOT required. NO lorem, NO generic numbered placeholders, NO empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "skeleton_screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.
- [ ] **Every affordance leads somewhere:** each button, link, tab and card that LOOKS interactive resolves to a real destination — a route in this project or a section on this page. Nothing is decorative-but-clickable, and nothing points at a page that does not exist.
- [ ] **No em-dashes:** the rendered output contains NO em-dash character. Use a colon, a comma, or a full stop instead — including inside <title>, headings, and any separator between a page name and the brand name.
- [ ] **One shape system:** corner radii come from at most THREE distinct values across the whole render. Do not mix many radii.
- [ ] **Responsive, phone-first:** the PRIMARY layout is the phone. Multi-column regions are only used where they genuinely read at phone width (a dense 2-column KPI grid is fine); anything wider must stack. Never assume a desktop viewport.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 10 checkpoints pass.

↑↑↑ MOCKUP PROMPT
