---
ui_yaml_sha: auto
design_md_hash: auto
feature: pay-domestic-single
state: content
sub_state: review
state_visibility: content
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-single — content state (Step 4: Review)

> Source: screens/pay-domestic-single/ui.yaml + demo-data.yaml · design-system/DESIGN.md
> DO NOT redeclare colors, fonts, or spacing — they live in the uploaded design system.
> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or act may look tappable. Review rows, banners and non-interactive
> text are NOT tappable.

## Archetype: screen

## State

`content` — Step 4 (Review). Account "Current account" (80200110203349) selected. Payee
"Mr Mark" (80200110203348) selected. Amount £15.55. Reference "Rent August". Consent staged;
Charges returns 0.05 GBP. review_card, confirm_button and cancel render.

## Layout

Scrollable column, 16dp screen_padding, start-aligned.

## Composition (top → bottom)

1. **TopAppBar** — title "Pay someone", `titleLarge` `onSurface`, back icon `arrow_back`,
   background `surface`.

2. **StepIndicator** — 4 steps, full width, 48dp. Steps 1–3 inactive (`labelMedium`
   `onSurfaceVariant`), step 4 "Review" active (`labelMedium` `primary`).
   Labels: "Account" · "Payee" · "Amount" · "Review"

3. **review_card** — `review_card` component, radius `rounded.medium`,
   container `surfaceContainer`, elevation 1. Five rows:
   - "From" → "Current account  ·  80200110203349"
   - "To" → "Mr Mark  ·  80200110203348"
   - "Amount" → "£15.55" (Roboto Mono, `onSurface`)
   - "Reference" → "Rent August"
   - "HSBC's charge" → "0.05 GBP" (Roboto Mono, `onSurface`)
   Row: `bodyMedium` label `onSurfaceVariant` left · `bodyLarge` value `onSurface` right,
   1dp `outlineVariant` dividers, 16dp horizontal padding, 14dp vertical padding per row.

4. **confirm_button** — `button_filled` pill, full width, 56dp min-height,
   container `primary`, label `onPrimary`, `labelLarge`.
   Text: "Send £15.55". Unmounts on tap — no disabled state.

5. **Cancel** — text button below confirm_button, centred, `bodyLarge` `primary`.
   Text: "Cancel".

6. **BottomNav** — 80dp `surfaceContainer`. Pay tab active (`primary`),
   others `onSurfaceVariant`.

## Design tokens (by name only)

Colors `surface` `onSurface` `onSurfaceVariant` `primary` `outlineVariant`
`surfaceContainer` · Type `titleLarge` `bodyLarge` `bodyMedium` `labelLarge`
`labelMedium` · Spacing `rounded.medium` · Icons `arrow_back`.

## Self-Validation Checklist

- [ ] Step 4 "Review" active; steps 1–3 inactive. Four-step stepper.
- [ ] review_card has exactly 5 rows: From, To, Amount, Reference, HSBC's charge.
- [ ] Amount and fee values in Roboto Mono.
- [ ] Confirm CTA reads "Send £15.55" — not "Confirm" and not a bare "Send".
- [ ] Confirm button NOT `error` colour — `primary` filled pill only.
- [ ] No FX rate, no "payment submitted", no amend notice (instant payment rail).
- [ ] Tokens by name — no hex literals.
- [ ] BottomNav: Pay tab active.

If any checkpoint fails → fix the output before returning.

↑↑↑ MOCKUP PROMPT
