---
ui_yaml_sha: d9528edd0e46ffd40d2bc4d46a13b342df0eb638fa6d3a2a5c1102c1e4bfc727
design_md_hash: c3a638b3a93523cbf2275539bdb5429cbf6921a4039cb7fbabc59f9d4146144f
app_shell_hash: 
design_read_hash: a302d6f69664249ea05a7525c838bbe835406f040bc22c6e6b0972a494796feb
content_hash: handcrafted-share-out-execute-error-v2

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: screen

feature: share-out-execute
state: error
state_visibility: error

project_id: 'null'
design_system_id: 'null'

generated_by: handcrafted-v2
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# share-out-execute — error state

> Bindings resolved to demo values: full failure — all 5 payouts failed, server error
> Stitch DesignSystem: CommonPurse forest green #2E7D32 / amber #FF8F00, minimalist-ui
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: screen

## Layout
- type: scrollable_column
- padding: default
- alignment: start

## Palette (CommonPurse)
- Primary: #2E7D32 (forest green) — top bar and avatar circles only
- Error: #B3261E (red) — error banner border, error icon, FAILED status icons and labels, try-again button
- Error Container: #FDECEA — error banner card background (light red tint)
- On Error Container: #8B0000 — error banner body text
- Surface: #FFFFFF
- Background: #FAFAFA
- Text primary: #212121
- Text secondary: #616161
- Roboto / SF Pro system stack

## Composition (top → bottom)
1. **top-bar** — title "Execute Share-Out", back arrow icon (ENABLED — user can navigate away), primary green background
2. **error-banner-card** — Error Container background (light red tint), error border: large centered error circle icon (error/red fill, white "X" or "!" inside) + heading "Share-Out Failed" (bold, error color) + body "Server error — please try again" (onErrorContainer color)
3. **section-header** — "MEMBER PAYOUTS" uppercase label
4. **member-payout-list** — 5 rows, ALL FAILED:
   - Row 1: avatar "AH" (green) + "Amina Hassan" / "KES 6,792 (28.3%)" + red error circle icon + "FAILED" label (error color)
   - Row 2: avatar "JK" (green) + "Joseph Kamau" / "KES 5,208 (21.7%)" + red error circle + "FAILED"
   - Row 3: avatar "GW" (green) + "Grace Wanjiku" / "KES 4,800 (20.0%)" + red error circle + "FAILED"
   - Row 4: avatar "PO" (green) + "Peter Otieno" / "KES 4,392 (18.3%)" + red error circle + "FAILED"
   - Row 5: avatar "MA" (green) + "Mary Akinyi" / "KES 2,808 (11.7%)" + red error circle + "FAILED"
5. **try-again-button** — sticky footer, full-width OUTLINED button (not filled) "Try Again", outlined border and label in error/red color, transparent background — signals a secondary recovery action

## State-specific behavior
- Full failure — all 5 payouts failed (server error).
- Error banner (red) is the primary visual emphasis — NOT amber (amber is for partial failure).
- Try Again is an outlined button to differentiate from the amber filled retry in partial_failure state.
- Back arrow enabled — treasurer can exit and retry later.
- No green checkmarks or amber elements visible — this is a full error state.

## Content source manifest
- pool_total: "KES 24,000"
- failure_count: 5
- failure_type: "server error"
- error_heading: "Share-Out Failed"
- error_body: "Server error — please try again"
- member_rows:
  - {initials: "AH", name: "Amina Hassan", payout: "KES 6,792", status: "FAILED"}
  - {initials: "JK", name: "Joseph Kamau", payout: "KES 5,208", status: "FAILED"}
  - {initials: "GW", name: "Grace Wanjiku", payout: "KES 4,800", status: "FAILED"}
  - {initials: "PO", name: "Peter Otieno", payout: "KES 4,392", status: "FAILED"}
  - {initials: "MA", name: "Mary Akinyi", payout: "KES 2,808", status: "FAILED"}

## Components (vocabulary used in this prompt)
- top-bar, card, banner, text, button

## Shell (app-shell resolved for this state)
- No bottom navigation — full-screen execution result.
- Top bar with back arrow (enabled). Sticky footer with try-again button.

## Tokens (design-tokens roles consumed)
- Colors: primary (#2E7D32) / error (#B3261E) / errorContainer / onErrorContainer / surface / onSurface (M3 roles by name).
- Typography: from design system — titleMedium / headlineMedium (error heading) / bodyLarge / bodyMedium.
- Spacing: from design system — gap.md / gap.sm.
- ALL token references are by name from the uploaded design system — no inline size values.

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. If any fails, FIX the output and re-render.

- [ ] **Per-state shape:** red error banner at top (NOT amber); all 5 rows show red error icon "FAILED"; Try Again button is OUTLINED (not filled) in red.
- [ ] **No amber elements** — this is a full error state, not a partial failure. No green checkmarks.
- [ ] **Real content:** "Share-Out Failed", "Server error — please try again", 5 East African names with individual amounts. All FAILED.
- [ ] **Token fidelity:** error color roles for banner/FAILED icons; primary green only for top bar and avatars; no inline size literals.
- [ ] **Archetype honored:** scrollable column, top→bottom, sticky footer with outlined try-again button.
- [ ] **App-shell parity:** no bottom nav. Top bar green, back arrow enabled.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
