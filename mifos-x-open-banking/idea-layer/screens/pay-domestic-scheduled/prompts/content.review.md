---
ui_yaml_sha: auto
design_md_hash: auto
feature: pay-domestic-scheduled
state: content
sub_state: review
state_visibility: content
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-scheduled — content state (Step 5: Review)

> Source: screens/pay-domestic-scheduled/ui.yaml + demo-data.yaml · design-system/DESIGN.md
> DO NOT redeclare colors, fonts, or spacing — they live in the uploaded design system.
> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or act may look tappable. Review rows, banners and non-interactive
> text are NOT tappable.

## Archetype: screen

## State

`content` — Step 5 (Review). Account "Current account" (80200110203349). Payee "Ramu"
(40200110203351). Amount £1.01. Reference "Rent". Execution date 13 Aug 2026. Consent staged;
Charges returns 0.05 GBP. review_card, no_funds_check_note, amend_notice and confirm_button
all render.

## Layout

Scrollable column, 16dp screen_padding, start-aligned.

## Composition (top → bottom)

1. **TopAppBar** — title "Pay on a date", `titleLarge` `onSurface`, back `arrow_back`,
   background `surface`.

2. **StepIndicator** — 5 steps, full width, 48dp. Steps 1–4 inactive (`labelMedium`
   `onSurfaceVariant`), step 5 "Review" active (`labelMedium` `primary`).
   Labels: "Account" · "Payee" · "Amount" · "Date" · "Review"

3. **review_card** — `review_card` component, radius `rounded.medium`,
   container `surfaceContainer`, elevation 1. Six rows:
   - "From" → "Current account  ·  80200110203349"
   - "To" → "Ramu  ·  40200110203351"
   - "Amount" → "£1.01" (Roboto Mono, `onSurface`)
   - "Payment date" → "13 Aug 2026"
   - "Reference" → "Rent"
   - "HSBC's charge" → "0.05 GBP" (Roboto Mono, `onSurface`)
   Row: `bodyMedium` label `onSurfaceVariant` left · `bodyLarge` value `onSurface` right,
   1dp `outlineVariant` dividers, 16dp horizontal padding, 14dp vertical padding.

4. **no_funds_check_note** — info banner, `surfaceContainer` background,
   `onSurface` `bodyMedium`. `info` icon 24dp `onSurfaceVariant`.
   Text: "This app cannot check whether the money will be in your account on that date.
   Make sure there is enough to cover the payment."

5. **amend_notice** — info banner, same style. `bodyMedium`.
   Text: "Once this payment is set up, this app cannot change it or cancel it. To do
   either, use the HSBC app or online banking."
   Visually prominent — not a footnote paragraph.

6. **confirm_button** — `button_filled` pill, full width, 56dp, container `primary`,
   label `onPrimary`, `labelLarge`. Text: "Schedule this payment".

7. **Cancel** — text button, centred, `bodyLarge` `primary`. Text: "Cancel".

8. **BottomNav** — 80dp `surfaceContainer`. Pay tab active.

## Design tokens (by name only)

Colors `surface` `onSurface` `onSurfaceVariant` `primary` `outlineVariant`
`surfaceContainer` · Type `titleLarge` `bodyLarge` `bodyMedium` `labelLarge`
`labelMedium` · Icons `arrow_back` `info`.

## Self-Validation Checklist

- [ ] Step 5 "Review" active; steps 1–4 inactive. Five-step stepper.
- [ ] review_card has exactly 6 rows: From, To, Amount, Payment date, Reference, HSBC's charge.
- [ ] Amount and fee values in Roboto Mono.
- [ ] no_funds_check_note visible as info banner — this rail has no funds-confirmation endpoint.
- [ ] amend_notice visible as info banner — MANDATORY OBL CEG disclosure, not a footnote.
- [ ] Confirm CTA reads "Schedule this payment" — NOT "Send £1.01".
- [ ] No FX rate, no "payment submitted" claim.
- [ ] Tokens by name — no hex literals.

If any checkpoint fails → fix the output before returning.

↑↑↑ MOCKUP PROMPT
