---
ui_yaml_sha: generated-2026-08-07
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
state: content
feature: payments
schema_version: "4.0"
generated_by: idea-feature-export (2026-08-07)
prompt_template_version: stitch-per-state-v3.0.0
---

# payments — content state

> Source: screens/payments/ui.yaml · Design: Open Banking — Trust Blue (design-tokens.yaml v2.4.0)
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.
> Nav: Home · Accounts · Pay (active) · More. No other tabs exist.

↓↓↓ MOCKUP PROMPT

## Archetype: screen

## Layout
- Scrollable column, background surface, screen_padding 16dp horizontal
- No top app bar (Pay tab landing — no back affordance)
- Bottom nav 80dp, surfaceContainer background, Pay tab active (filled icon, primary)

## Composition (top → bottom)

**hub_heading** — text, "How do you want to pay?", titleMedium, onSurface, role=header

**payment_type_grid** — 3-column grid, gap 12dp, square tiles, role=list

Row 1:
- **tile_domestic_single** — icon `payments` (primary), label "Pay someone" (labelMedium, onSurface), description "One payment, sent now" (bodySmall, onSurfaceVariant); tappable → pay-domestic-single
- **tile_domestic_scheduled** — icon `event` (primary), label "Pay on a date", description "One payment, on a future date"; tappable → pay-domestic-scheduled
- **tile_domestic_standing_order** — icon `repeat` (primary), label "Standing order", description "Same payment, repeating"; tappable → pay-domestic-standing-order

Row 2:
- **tile_international_single** — icon `public` (primary), label "Pay abroad", description "One overseas payment, sent now"; tappable → pay-international-single
- **tile_international_scheduled** — icon `public_off` (primary), label "Pay abroad on a date", description "One overseas payment, on a future date"; tappable → pay-international-scheduled
- **tile_international_standing_order** — icon `currency_exchange` (primary), label "Overseas standing order", description "Same overseas payment, repeating"; tappable → pay-international-standing-order

Row 3 (left-aligned, two empty cells to the right):
- **tile_vrp_mandate** — icon `all_inclusive` (primary), label "Variable payments", description "Set limits once, pay any amount within them"; tappable → pay-vrp-mandate

Each tile: card, background surfaceContainerLow, border 1dp outlineVariant (decorative), corner radius.md (12dp), elevation level1, internal padding spacing.md, stack icon → label → description.

**amend_notice** — text, "To change or cancel a standing order or a scheduled payment you have already set up, use the HSBC app or online banking. Open Banking does not let this app change them.", bodySmall, onSurfaceVariant, NOT tappable

## Tokens (by name — no hex literals)
Colors: primary · onSurface · onSurfaceVariant · surface · surfaceContainerLow · surfaceContainer · outlineVariant
Typography: titleMedium · labelMedium · bodySmall
Spacing: spacing.md · spacing.sm · spacing.lg
Radius: radius.md · Icon: icon.md

## Self-Validation Checklist

- [ ] ONLY content state rendered — no loading, empty, or error UI
- [ ] Exactly 7 tiles visible: Pay someone · Pay on a date · Standing order · Pay abroad · Pay abroad on a date · Overseas standing order · Variable payments
- [ ] Row 3: VRP tile left-aligned; two empty cells right (not centred)
- [ ] Each tile: icon (primary) + label (labelMedium/onSurface) + description (bodySmall/onSurfaceVariant)
- [ ] Tile 2 description "on a future date", tile 3 "repeating" — not swapped
- [ ] amend_notice below grid; bodySmall/onSurfaceVariant; not tappable
- [ ] No top app bar rendered
- [ ] Bottom nav: Pay tab active (filled icon, primary); three others inactive (onSurfaceVariant)
- [ ] All tokens referenced by name — zero hex literals in render

Return ONLY when all items pass.

↑↑↑ MOCKUP PROMPT
