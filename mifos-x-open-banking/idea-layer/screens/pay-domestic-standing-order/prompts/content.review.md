---
ui_yaml_sha: auto
design_md_hash: auto
feature: pay-domestic-standing-order
state: content
sub_state: review
state_visibility: content
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-standing-order — content state (Step 4: Review)

> Source: screens/pay-domestic-standing-order/ui.yaml + demo-data.yaml · design-system/DESIGN.md
> DO NOT redeclare colors, fonts, or spacing — they live in the uploaded design system.
> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or act may look tappable. Review rows, banners and non-interactive
> text are NOT tappable.

## Archetype: screen

## State

`content` — Step 4 (Review). Payee "Mr Mark" (80200110203349). Frequency Weekly. First payment
13 Aug 2026. Final payment 4 Dec 2026. Amount £0.01. No reference entered. Consent staged;
Charges returns 0.05 GBP. review_card, amend_notice (WARNING) and confirm_button all render.

## Layout

Scrollable column, 16dp screen_padding, start-aligned.

## Composition (top → bottom)

1. **TopAppBar** — title "Standing order", `titleLarge` `onSurface`, back `arrow_back`,
   background `surface`.

2. **StepIndicator** — 4 steps, full width, 48dp. Steps 1–3 inactive (`labelMedium`
   `onSurfaceVariant`), step 4 "Review" active (`labelMedium` `primary`).
   Labels: "Payee" · "Schedule" · "Amount" · "Review"
   (No "Account" step — this rail sends no DebtorAccount.)

3. **review_card** — `review_card` component, radius `rounded.medium`,
   container `surfaceContainer`, elevation 1. Six rows:
   - "To" → "Mr Mark  ·  80200110203349"
   - "How often" → "Weekly"
   - "First payment" → "13 Aug 2026"
   - "Final payment" → "4 Dec 2026"
   - "Amount" → "£0.01" (Roboto Mono, `onSurface`)
   - "HSBC's charge" → "0.05 GBP" (Roboto Mono, `onSurface`)
   No "From" row — no debtor account step on this rail.
   No Reference row — reference left blank in this scenario.
   Row: `bodyMedium` label `onSurfaceVariant` left · `bodyLarge` value `onSurface` right,
   1dp `outlineVariant` dividers, 16dp horizontal padding, 14dp vertical padding.

4. **amend_notice** — WARNING-severity banner, `tertiaryContainer` background,
   `onTertiaryContainer` text, `warning` icon 24dp, `bodyMedium`.
   Text: "Once this standing order is set up, this app cannot change it or cancel it. To
   change the amount or the schedule, or to stop it altogether, use the HSBC app or
   online banking."
   Visually prominent — not a footnote.

5. **confirm_button** — `button_filled` pill, full width, 56dp, container `primary`,
   label `onPrimary`, `labelLarge`. Text: "Set up this standing order".

6. **Cancel** — text button, centred, `bodyLarge` `primary`. Text: "Cancel".

7. **BottomNav** — 80dp `surfaceContainer`. Pay tab active.

## Design tokens (by name only)

Colors `surface` `onSurface` `onSurfaceVariant` `primary` `outlineVariant`
`surfaceContainer` `tertiaryContainer` `onTertiaryContainer` · Type `titleLarge`
`bodyLarge` `bodyMedium` `labelLarge` `labelMedium` · Icons `arrow_back` `warning`.

## Self-Validation Checklist

- [ ] Stepper: 4 steps, labels "Payee · Schedule · Amount · Review". Step 4 active. No "Account".
- [ ] review_card: 6 rows — To, How often, First payment, Final payment, Amount, HSBC's charge.
  No "From" row. No Reference row.
- [ ] Amount and fee values in Roboto Mono.
- [ ] amend_notice uses WARNING (`tertiaryContainer`), NOT info — open-ended mandate warrants it.
- [ ] Confirm CTA reads "Set up this standing order" — NOT "Send £0.01".
- [ ] No FX rate, no "payment submitted" claim.
- [ ] Tokens by name — no hex literals.

If any checkpoint fails → fix the output before returning.

↑↑↑ MOCKUP PROMPT
