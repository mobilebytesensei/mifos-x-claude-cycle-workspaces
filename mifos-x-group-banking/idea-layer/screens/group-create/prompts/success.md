---
ui_yaml_sha: d9528edd0e46ffd40d2bc4d46a13b342df0eb638fa6d3a2a5c1102c1e4bfc727
design_md_hash: c3a638b3a93523cbf2275539bdb5429cbf6921a4039cb7fbabc59f9d4146144f
app_shell_hash: 
design_read_hash: a302d6f69664249ea05a7525c838bbe835406f040bc22c6e6b0972a494796feb
content_hash: handcrafted-group-create-success-v1

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: screen

feature: group-create
state: success
state_visibility: success

project_id: 'null'
design_system_id: 'null'

generated_by: handcrafted-v1
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# group-create — success state

> Bindings resolved to demo values: group "Mwangaza Women's Group", VSLA type
> Stitch DesignSystem: CommonPurse forest green #2E7D32 / amber #FF8F00, minimalist-ui
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: screen

## Layout
- type: scrollable_column
- padding: default
- alignment: center

## Palette (CommonPurse)
- Primary: #2E7D32 (forest green) — success icon, top bar, CTA
- Accent: #FF8F00 (amber) — group type chip accent
- Surface: #FFFFFF — cards
- Background: #FAFAFA
- Text primary: #212121
- Success semantic: #2E7D32
- Roboto / SF Pro system stack

## Composition (top → bottom)
1. **top-bar** — title "Group Created", no close icon (wizard complete), primary green background
2. **success-illustration** — large circular check icon (#2E7D32), centered, prominent display size
3. **success-heading** — text "Mwangaza Women's Group created!", titleLarge, centered, bold
4. **success-subtitle** — text "Your VSLA group is ready. Share the invite code with members.", bodyLarge, centered, #616161
5. **invite-code-card** — card with label "Invite Code" and bold code value "MW-2847", copy icon on right, secondaryContainer background
6. **group-details-card** — surface card with summary rows:
   - Group Type: "VSLA"
   - Office: "Kisumu West Branch"
   - Currency: "KES"
   - Meeting: "Mondays at 09:00"
   - Cycle: "12 months"
7. **go-to-group-button** — filled button, label "Go to Group Dashboard", primary green, full width
8. **share-invite-button** — outlined button, label "Share Invite Code", outline color primary green, full width

## State-specific behavior
- Wizard complete — group was successfully created via Fineract companion API.
- Auto-generated invite code "MW-2847" displayed prominently for sharing.
- Two CTAs: navigate to new group dashboard, or share invite code.
- No form fields visible — wizard concluded.

## Content source manifest
- group_name: "Mwangaza Women's Group"
- group_type: "VSLA"
- invite_code: "MW-2847"
- office: "Kisumu West Branch"
- currency: "KES"
- meeting: "Mondays at 09:00"
- cycle_length: "12 months"

## Components (vocabulary used in this prompt)
- top-bar, card, text, button

## Shell (app-shell resolved for this state)
- No bottom navigation visible — wizard completion screen.
- Top bar present, no close icon (cannot go back from success).

## Tokens (design-tokens roles consumed)
- Colors: primary (#2E7D32) / secondaryContainer / onSecondaryContainer / surface / on-surface / on-surface-variant.
- Typography: titleLarge (heading) / bodyLarge (subtitle, detail rows) / titleMedium (invite code value).
- Spacing: gap.lg (between sections) / gap.md (within cards).
- ALL token references are by name from the uploaded design system — no hex literals, no inline size values.

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. If any fails, FIX the output and re-render.

- [ ] **Per-state shape:** render shows ONLY the success state — large check icon + group details + invite code + two CTAs. No wizard form fields.
- [ ] **Real content:** group name "Mwangaza Women's Group", type "VSLA", invite code "MW-2847", office "Kisumu West Branch". No generic items.
- [ ] **Token fidelity:** colors from design system; no hex literals except where specified in the Palette block above.
- [ ] **Component vocabulary:** top-bar, card, text, button — design-system registered.
- [ ] **Archetype honored:** centered column, composition top→bottom matches.
- [ ] **App-shell parity:** no bottom nav on wizard completion screen. Top bar present without close icon.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
