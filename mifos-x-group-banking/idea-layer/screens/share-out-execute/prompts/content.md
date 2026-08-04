---
ui_yaml_sha: d9528edd0e46ffd40d2bc4d46a13b342df0eb638fa6d3a2a5c1102c1e4bfc727
design_md_hash: c3a638b3a93523cbf2275539bdb5429cbf6921a4039cb7fbabc59f9d4146144f
app_shell_hash: 
design_read_hash: a302d6f69664249ea05a7525c838bbe835406f040bc22c6e6b0972a494796feb
content_hash: handcrafted-share-out-execute-content-v2

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: screen

feature: share-out-execute
state: content
state_visibility: content

project_id: 'null'
design_system_id: 'null'

generated_by: handcrafted-v2
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# share-out-execute — content state

> Bindings resolved to demo values: KES 24,000 pool, 5 members, awaiting double-confirmation
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
- Primary: #2E7D32 (forest green) — top bar, avatar circles, primary CTA
- Accent: #FF8F00 (amber) — pool amount emphasis
- Primary Container: #C8E6C9 — summary card background
- Surface: #FFFFFF — cards, rows
- Background: #FAFAFA
- Text primary: #212121
- Text secondary: #616161
- Disabled: #9E9E9E — disabled execute button label
- Disabled Container: #E0E0E0 — disabled execute button background
- Roboto / SF Pro system stack

## Composition (top → bottom)
1. **top-bar** — title "Execute Share-Out", back arrow icon on left (enabled), primary green background
2. **summary-card** — primaryContainer background card: wallet icon + label "Total Distribution Pool" + bold amount "KES 24,000" in primary green + subtitle "5 members to receive payouts"
3. **section-header** — label "MEMBER PAYOUTS" in uppercase, secondary text, above the list
4. **member-payout-list** — 5 rows with thin dividers between:
   - Row 1: avatar circle (green, initials "AH") + "Amina Hassan" / "KES 6,792 (28.3%)" + trailing "PENDING" chip (grey)
   - Row 2: avatar "JK" + "Joseph Kamau" / "KES 5,208 (21.7%)" + trailing "PENDING" chip
   - Row 3: avatar "GW" + "Grace Wanjiku" / "KES 4,800 (20.0%)" + trailing "PENDING" chip
   - Row 4: avatar "PO" + "Peter Otieno" / "KES 4,392 (18.3%)" + trailing "PENDING" chip
   - Row 5: avatar "MA" + "Mary Akinyi" / "KES 2,808 (11.7%)" + trailing "PENDING" chip
5. **offline-banner** — NOT visible (device is online)
6. **double-confirmation-card** — surface card: heading "Confirm Share-Out", instruction text 'Type "SHARE OUT" below or use biometric', outlined text field with placeholder "SHARE OUT" (empty, no value entered yet), "Use Biometric Instead" text button below field
7. **execute-button** — sticky footer, full-width filled button, label "Execute Share-Out", DISABLED state (grey background, grey label — confirmation phrase not yet typed)

## State-specific behavior
- Pre-execution state: user must type "SHARE OUT" or use biometric before execute button activates.
- Execute button is disabled (greyed out) because confirmation text field is empty.
- Back navigation is available (back arrow enabled).
- Offline banner is hidden (device online).

## Content source manifest
- group_name: "Mwangaza Women's Group"
- pool_total: "KES 24,000"
- member_count: 5
- member_rows:
  - {initials: "AH", name: "Amina Hassan", payout: "KES 6,792", share: "28.3%"}
  - {initials: "JK", name: "Joseph Kamau", payout: "KES 5,208", share: "21.7%"}
  - {initials: "GW", name: "Grace Wanjiku", payout: "KES 4,800", share: "20.0%"}
  - {initials: "PO", name: "Peter Otieno", payout: "KES 4,392", share: "18.3%"}
  - {initials: "MA", name: "Mary Akinyi", payout: "KES 2,808", share: "11.7%"}

## Components (vocabulary used in this prompt)
- top-bar, card, text, chip, text-field, button

## Shell (app-shell resolved for this state)
- No bottom navigation — full-screen execution flow.
- Top bar with back arrow. Sticky footer with execute button.

## Tokens (design-tokens roles consumed)
- Colors: primary (#2E7D32) / primaryContainer / onPrimaryContainer / surface / onSurface / onSurfaceVariant / disabled / disabledContainer (M3 roles by name).
- Typography: from design system — titleMedium (top bar) / bodyLarge (amounts) / bodyMedium (member names, labels).
- Spacing: from design system — gap.md between sections / gap.sm within rows.
- ALL token references are by name from the uploaded design system — no inline size values.

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. If any fails, FIX the output and re-render.

- [ ] **Per-state shape:** double-confirmation card visible with empty text field; execute button DISABLED (grey).
- [ ] **Real content:** pool "KES 24,000", 5 East African member names with individual KES amounts and percentages. All statuses show "PENDING".
- [ ] **Token fidelity:** colors by M3 role name; no inline size literals.
- [ ] **Component vocabulary:** top-bar, card, text, chip, text-field, button — design-system registered.
- [ ] **Archetype honored:** scrollable column, top→bottom composition, sticky footer for execute button.
- [ ] **App-shell parity:** no bottom nav. Top bar with back arrow enabled. Execute button disabled.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
