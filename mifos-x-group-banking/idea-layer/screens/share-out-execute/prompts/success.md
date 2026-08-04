---
ui_yaml_sha: d9528edd0e46ffd40d2bc4d46a13b342df0eb638fa6d3a2a5c1102c1e4bfc727
design_md_hash: c3a638b3a93523cbf2275539bdb5429cbf6921a4039cb7fbabc59f9d4146144f
app_shell_hash: 
design_read_hash: a302d6f69664249ea05a7525c838bbe835406f040bc22c6e6b0972a494796feb
content_hash: handcrafted-share-out-execute-success-v2

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: screen

feature: share-out-execute
state: success
state_visibility: success

project_id: 'null'
design_system_id: 'null'

generated_by: handcrafted-v2
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# share-out-execute — success state

> Bindings resolved to demo values: all 5 members paid, KES 24,000 fully distributed
> Stitch DesignSystem: MifosSave forest green #2E7D32 / amber #FF8F00, minimalist-ui
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: screen

## Layout
- type: scrollable_column
- padding: default
- alignment: center

## Palette (MifosSave)
- Primary: #2E7D32 (forest green) — top bar, checkmark icons, DONE chips, Done button
- Primary Container: #C8E6C9 — success banner card background, DONE chip background
- On Primary Container: #1B5E20 — text on primaryContainer
- Surface: #FFFFFF — member row background
- Background: #FAFAFA
- Text primary: #212121
- Text secondary: #616161
- Roboto / SF Pro system stack

## Composition (top → bottom)
1. **top-bar** — title "Execute Share-Out", NO back arrow (terminal state — navigation closed), primary green background
2. **success-banner-card** — primaryContainer background card, centered content: large circular checkmark icon (primary green fill, white checkmark inside) + heading "Share-Out Complete!" (bold, onPrimaryContainer color) + body text "Cycle 1 share-out of KES 24,000 distributed to all 5 members" (onPrimaryContainer)
3. **section-header** — "MEMBER PAYOUTS" uppercase label
4. **member-payout-list** — 5 rows, ALL showing DONE status:
   - Row 1: avatar "AH" (green) + "Amina Hassan" / "KES 6,792 (28.3%)" + filled green checkmark + "DONE" chip (primaryContainer bg, onPrimaryContainer text)
   - Row 2: avatar "JK" + "Joseph Kamau" / "KES 5,208 (21.7%)" + green checkmark + "DONE"
   - Row 3: avatar "GW" + "Grace Wanjiku" / "KES 4,800 (20.0%)" + green checkmark + "DONE"
   - Row 4: avatar "PO" + "Peter Otieno" / "KES 4,392 (18.3%)" + green checkmark + "DONE"
   - Row 5: avatar "MA" + "Mary Akinyi" / "KES 2,808 (11.7%)" + green checkmark + "DONE"
5. **done-button** — sticky footer, full-width filled button "Done", primary green (ENABLED), navigates to group dashboard

## State-specific behavior
- Terminal success state — all 5 payouts completed.
- No back arrow — user cannot return to execution screen.
- Only action is "Done" button navigating back to group dashboard.
- Success banner is the primary visual emphasis (large checkmark, celebratory green).
- No progress bar — execution complete.

## Content source manifest
- pool_total: "KES 24,000"
- cycle: "Cycle 1"
- success_message: "Share-Out Complete!"
- subtitle: "Cycle 1 share-out of KES 24,000 distributed to all 5 members"
- member_rows:
  - {initials: "AH", name: "Amina Hassan", payout: "KES 6,792", status: "DONE"}
  - {initials: "JK", name: "Joseph Kamau", payout: "KES 5,208", status: "DONE"}
  - {initials: "GW", name: "Grace Wanjiku", payout: "KES 4,800", status: "DONE"}
  - {initials: "PO", name: "Peter Otieno", payout: "KES 4,392", status: "DONE"}
  - {initials: "MA", name: "Mary Akinyi", payout: "KES 2,808", status: "DONE"}

## Components (vocabulary used in this prompt)
- top-bar, card, text, chip, button

## Shell (app-shell resolved for this state)
- No bottom navigation — full-screen terminal state.
- Top bar without back arrow. Sticky footer with Done button.

## Tokens (design-tokens roles consumed)
- Colors: primary (#2E7D32) / primaryContainer / onPrimaryContainer / surface / onSurface (M3 roles by name).
- Typography: from design system — titleMedium / headlineMedium (success heading) / bodyLarge.
- Spacing: from design system — gap.lg (between banner and list) / gap.md (within card).
- ALL token references are by name from the uploaded design system — no inline size values.

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. If any fails, FIX the output and re-render.

- [ ] **Per-state shape:** large checkmark success banner at top; all 5 rows show green checkmark "DONE"; "Done" button enabled green.
- [ ] **No back arrow** in top bar (terminal state).
- [ ] **Real content:** "Share-Out Complete!", "KES 24,000", "Cycle 1", 5 East African member names with individual amounts. All DONE.
- [ ] **Token fidelity:** colors by M3 role name; no inline size literals in composition.
- [ ] **Archetype honored:** scrollable column, top→bottom, sticky footer with Done button.
- [ ] **App-shell parity:** no bottom nav. Top bar green, no back arrow.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
