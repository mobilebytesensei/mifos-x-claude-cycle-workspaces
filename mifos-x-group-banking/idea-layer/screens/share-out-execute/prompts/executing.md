---
ui_yaml_sha: d9528edd0e46ffd40d2bc4d46a13b342df0eb638fa6d3a2a5c1102c1e4bfc727
design_md_hash: c3a638b3a93523cbf2275539bdb5429cbf6921a4039cb7fbabc59f9d4146144f
app_shell_hash: 
design_read_hash: a302d6f69664249ea05a7525c838bbe835406f040bc22c6e6b0972a494796feb
content_hash: handcrafted-share-out-execute-executing-v2

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: screen

feature: share-out-execute
state: executing
state_visibility: executing

project_id: 'null'
design_system_id: 'null'

generated_by: handcrafted-v2
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# share-out-execute — executing state

> Bindings resolved to demo values: COMP-DIST-001 in progress, 2 of 5 members paid
> Stitch DesignSystem: MifosSave forest green #2E7D32 / amber #FF8F00, minimalist-ui
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: screen

## Layout
- type: scrollable_column
- padding: default
- alignment: start

## Palette (MifosSave)
- Primary: #2E7D32 (forest green) — top bar, DONE status, progress bar fill, avatar circles
- Accent: #FF8F00 (amber) — IN_PROGRESS spinner
- Primary Container: #C8E6C9 — summary card background
- Surface: #FFFFFF — cards, rows
- Background: #FAFAFA
- Text primary: #212121
- Text secondary: #616161
- Disabled: #9E9E9E — PENDING status label and icon
- Roboto / SF Pro system stack

## Composition (top → bottom)
1. **top-bar** — title "Execute Share-Out", back arrow icon DISABLED (greyed, non-tappable — execution in progress), primary green background
2. **summary-card** — primaryContainer background: wallet icon + label "Total Distribution Pool" + bold amount "KES 24,000" + subtitle "5 members to receive payouts"
3. **section-header** — "MEMBER PAYOUTS" uppercase label
4. **member-payout-list** — 5 rows with dividers, mixed status icons:
   - Row 1: avatar "AH" (green) + "Amina Hassan" / "KES 6,792 (28.3%)" + filled green checkmark icon + "DONE" label (green) — completed
   - Row 2: avatar "JK" (green) + "Joseph Kamau" / "KES 5,208 (21.7%)" + amber circular spinner (animated) + "IN PROGRESS" label (amber) — active
   - Row 3: avatar "GW" (green) + "Grace Wanjiku" / "KES 4,800 (20.0%)" + grey circle icon + "PENDING" label (grey)
   - Row 4: avatar "PO" (green) + "Peter Otieno" / "KES 4,392 (18.3%)" + grey circle + "PENDING"
   - Row 5: avatar "MA" (green) + "Mary Akinyi" / "KES 2,808 (11.7%)" + grey circle + "PENDING"
5. **progress-row** — linear progress bar at 40% fill (primary green), track (secondary container), label "2 of 5 complete" below bar
6. (no double-confirmation card — execution started, card dismissed)
7. (no execute button in footer — footer empty during execution)

## State-specific behavior
- Active execution: back arrow disabled (cannot navigate away mid-execution).
- Row 1 complete (DONE — green checkmark), Row 2 in flight (IN PROGRESS — amber spinner animating), Rows 3-5 queued (PENDING — grey).
- Linear progress bar at 40% is the primary execution feedback.
- Double-confirmation card is NOT rendered.
- Execute button is NOT shown — footer is empty.

## Content source manifest
- pool_total: "KES 24,000"
- execution_id: "COMP-DIST-001"
- progress: "2 of 5 complete"
- member_rows:
  - {initials: "AH", name: "Amina Hassan", payout: "KES 6,792", status: "DONE"}
  - {initials: "JK", name: "Joseph Kamau", payout: "KES 5,208", status: "IN PROGRESS"}
  - {initials: "GW", name: "Grace Wanjiku", payout: "KES 4,800", status: "PENDING"}
  - {initials: "PO", name: "Peter Otieno", payout: "KES 4,392", status: "PENDING"}
  - {initials: "MA", name: "Mary Akinyi", payout: "KES 2,808", status: "PENDING"}

## Components (vocabulary used in this prompt)
- top-bar, card, text, chip, progress-indicator

## Shell (app-shell resolved for this state)
- No bottom navigation — full-screen execution flow.
- Top bar with back arrow (disabled/greyed). No sticky footer.

## Tokens (design-tokens roles consumed)
- Colors: primary (#2E7D32) / primaryContainer / onPrimaryContainer / surface / onSurface / onSurfaceVariant / disabled (M3 roles by name).
- Typography: from design system — titleMedium / bodyLarge / bodyMedium / labelSmall.
- Spacing: from design system — gap.md / gap.sm.
- ALL token references are by name from the uploaded design system — no inline size values.

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. If any fails, FIX the output and re-render.

- [ ] **Per-state shape:** no confirmation card, no execute button; progress bar at 40% visible; back arrow greyed out.
- [ ] **Status icons:** Row 1 green checkmark (DONE), Row 2 amber spinner (IN PROGRESS), Rows 3-5 grey circle (PENDING).
- [ ] **Real content:** "KES 24,000" pool, 5 East African names with individual amounts. Label "2 of 5 complete".
- [ ] **Token fidelity:** colors by M3 role name; no inline size literals in composition.
- [ ] **Archetype honored:** scrollable column, top→bottom, no footer.
- [ ] **App-shell parity:** no bottom nav. Top bar green, back arrow disabled.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
