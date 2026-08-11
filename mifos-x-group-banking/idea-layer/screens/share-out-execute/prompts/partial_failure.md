---
ui_yaml_sha: d9528edd0e46ffd40d2bc4d46a13b342df0eb638fa6d3a2a5c1102c1e4bfc727
design_md_hash: c3a638b3a93523cbf2275539bdb5429cbf6921a4039cb7fbabc59f9d4146144f
app_shell_hash: 
design_read_hash: a302d6f69664249ea05a7525c838bbe835406f040bc22c6e6b0972a494796feb
content_hash: handcrafted-share-out-execute-partial-failure-v2

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: screen

feature: share-out-execute
state: partial_failure
state_visibility: partial_failure

project_id: 'null'
design_system_id: 'null'

generated_by: handcrafted-v2
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# share-out-execute — partial_failure state

> Bindings resolved to demo values: 3 of 5 succeeded, 2 failed (Peter Otieno, Mary Akinyi)
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
- Primary: #2E7D32 (forest green) — top bar, DONE status icons, avatar circles
- Accent: #FF8F00 (amber) — warning banner border, retry button background
- Warning Container: #FFF8E1 — warning banner card background
- On Warning: #E65100 — warning banner text
- Error: #B3261E — FAILED status icon and label
- Primary Container: #C8E6C9 — DONE chip background
- On Primary Container: #1B5E20 — DONE chip text
- Surface: #FFFFFF
- Background: #FAFAFA
- Text primary: #212121
- Text secondary: #616161
- Roboto / SF Pro system stack

## Composition (top → bottom)
1. **top-bar** — title "Execute Share-Out", back arrow icon (enabled — user can navigate away), primary green background
2. **warning-banner-card** — Warning Container background card, amber left border or outline: warning triangle icon (accent/amber) + heading "2 payouts failed — network error" (bold, onWarning/error color) + body "The other 3 payouts succeeded." (onWarning color)
3. **section-header** — "MEMBER PAYOUTS" uppercase label
4. **member-payout-list** — 5 rows, mixed status:
   - Row 1: avatar "AH" (green) + "Amina Hassan" / "KES 6,792 (28.3%)" + green checkmark + "DONE" chip (primaryContainer)
   - Row 2: avatar "JK" (green) + "Joseph Kamau" / "KES 5,208 (21.7%)" + green checkmark + "DONE"
   - Row 3: avatar "GW" (green) + "Grace Wanjiku" / "KES 4,800 (20.0%)" + green checkmark + "DONE"
   - Row 4: avatar "PO" (green) + "Peter Otieno" / "KES 4,392 (18.3%)" + red error circle icon + "FAILED" label (error color)
   - Row 5: avatar "MA" (green) + "Mary Akinyi" / "KES 2,808 (11.7%)" + red error circle icon + "FAILED" label (error color)
5. **retry-button** — sticky footer, full-width filled button "Retry Failed Payouts", amber/accent background (ENABLED), white text — retries only the 2 failed members

## State-specific behavior
- Partial completion: 3 of 5 payouts succeeded; 2 failed (network error).
- Warning banner (amber) summarizes mixed outcome — NOT a success (green) and NOT a full error (red).
- Retry button in amber triggers retry for failed members only.
- Back arrow is enabled — treasurer can exit and retry later.
- Progress bar is NOT shown — execution phase is complete.

## Content source manifest
- pool_total: "KES 24,000"
- success_count: 3
- failure_count: 2
- failure_reason: "network error"
- warning_heading: "2 payouts failed — network error"
- warning_body: "The other 3 payouts succeeded."
- member_rows:
  - {initials: "AH", name: "Amina Hassan", payout: "KES 6,792", status: "DONE"}
  - {initials: "JK", name: "Joseph Kamau", payout: "KES 5,208", status: "DONE"}
  - {initials: "GW", name: "Grace Wanjiku", payout: "KES 4,800", status: "DONE"}
  - {initials: "PO", name: "Peter Otieno", payout: "KES 4,392", status: "FAILED"}
  - {initials: "MA", name: "Mary Akinyi", payout: "KES 2,808", status: "FAILED"}

## Components (vocabulary used in this prompt)
- top-bar, card, banner, text, chip, button

## Shell (app-shell resolved for this state)
- No bottom navigation — full-screen execution result flow.
- Top bar with back arrow (enabled). Sticky footer with retry button.

## Tokens (design-tokens roles consumed)
- Colors: primary (#2E7D32) / accent (#FF8F00) / error (#B3261E) / primaryContainer / onPrimaryContainer / surface / onSurface (M3 roles by name).
- Typography: from design system — titleMedium / bodyLarge / bodyMedium / labelSmall.
- Spacing: from design system — gap.md / gap.sm.
- ALL token references are by name from the uploaded design system — no inline size values.

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. If any fails, FIX the output and re-render.

- [ ] **Per-state shape:** amber warning banner visible; rows 1-3 DONE (green), rows 4-5 FAILED (red); amber retry button enabled.
- [ ] **Real content:** "2 payouts failed — network error", 5 East African names, specific KES amounts. Peter Otieno and Mary Akinyi FAILED.
- [ ] **Color semantics:** warning amber for banner/retry; error red for FAILED icons; green only for DONE.
- [ ] **Token fidelity:** colors by M3 role name; no inline size literals in composition.
- [ ] **Archetype honored:** scrollable column, top→bottom, sticky footer with retry button.
- [ ] **App-shell parity:** no bottom nav. Top bar green, back arrow enabled.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
