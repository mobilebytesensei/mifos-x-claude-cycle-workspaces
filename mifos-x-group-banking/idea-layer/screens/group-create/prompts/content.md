---
ui_yaml_sha: d9528edd0e46ffd40d2bc4d46a13b342df0eb638fa6d3a2a5c1102c1e4bfc727
design_md_hash: c3a638b3a93523cbf2275539bdb5429cbf6921a4039cb7fbabc59f9d4146144f
app_shell_hash: 
design_read_hash: a302d6f69664249ea05a7525c838bbe835406f040bc22c6e6b0972a494796feb
content_hash: handcrafted-group-create-content-v1

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: screen

feature: group-create
state: content
state_visibility: content

project_id: 'null'
design_system_id: 'null'

generated_by: handcrafted-v1
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# group-create — content state (4-step wizard, Step 1 shown)

> Auto-generated from screens/group-create/ui.yaml (bindings resolved to demo values)
> Stitch DesignSystem: CommonPurse forest green #2E7D32 / amber #FF8F00, minimalist-ui
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: screen

## Layout
- type: scrollable_column
- padding: default horizontal
- alignment: start

## Palette (CommonPurse)
- Primary: #2E7D32 (forest green) — app bars, primary CTAs
- Accent: #FF8F00 (amber) — pooled fund emphasis
- Surface: #FFFFFF — cards
- Background: #FAFAFA
- Text primary: #212121
- Text secondary: #616161
- Roboto / SF Pro system stack

## Composition (top → bottom) — Step 1 of 4: Identity
1. **top-bar** — title "New VSLA Group", close icon (X) on left, primary green background
2. **chip** — "VSLA" label with category icon, secondaryContainer background, standard horizontal margin
3. **step-indicator** — 4 steps, step 1 active (filled green circle), labels: Identity / Rules / Members / Review
4. **group-name-field** — text field, label "Group Name", placeholder cleared, value "Mwangaza Women's Group"
5. **office-dropdown** — dropdown, label "Office", value "Kisumu West Branch"
6. **currency-dropdown** — dropdown, label "Currency", value "KES"
7. **meeting-day-dropdown** — dropdown, label "Meeting Day", value "Monday"
8. **meeting-time-picker** — time picker, label "Meeting Time", value "09:00"
9. **next-button** — filled button, label "Next", primary green, full width, enabled

## State-specific behavior
- Wizard is on Step 1 (Identity). Steps 2–4 not visible.
- Group type is VSLA (shown in the amber chip below the top bar).
- All required fields filled with real East African demo content.
- Next button is enabled (all step-1 fields valid).

## Content source manifest
- group_name: "Mwangaza Women's Group"
- group_type: "VSLA"
- office: "Kisumu West Branch"
- currency: "KES"
- meeting_day: "Monday"
- meeting_time: "09:00"

## Components (vocabulary used in this prompt)
- top-bar, chip, step-indicator, text-field, button

## Shell (app-shell resolved for this state)
- No bottom navigation visible — full-screen wizard flow.
- Top bar with close icon is the only navigation surface.

## Tokens (design-tokens roles consumed)
- Colors: primary (#2E7D32) / secondaryContainer / onSecondaryContainer / surface / on-surface / outline (M3 roles).
- Typography: titleMedium (chip label) / bodyLarge (form fields) / labelLarge (button).
- Spacing: gap.md (between form fields) / gap.sm (within sections).
- ALL token references are by name from the uploaded design system — no hex literals, no inline size values.

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. If any fails, FIX the output and re-render.

- [ ] **Per-state shape:** the render shows ONLY Step 1 (Identity) of the wizard — no step 2/3/4 fields visible.
- [ ] **Real content:** group name is "Mwangaza Women's Group", office "Kisumu West Branch", currency "KES", meeting "Monday 09:00". No generic item labels, no placeholder text.
- [ ] **Token fidelity:** colors from design system by name; spacing from declared scale tokens. No invented hex codes.
- [ ] **Component vocabulary:** top-bar, chip, step-indicator, text-field, button — all design-system registered.
- [ ] **Archetype honored:** scrollable column, top→bottom composition order matches.
- [ ] **App-shell parity:** no bottom nav (wizard modal flow). Top bar present with close icon.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
