---
ui_yaml_sha: auto
design_md_hash: auto
feature: pay-international-single
state: content
sub_state: review
state_visibility: content
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-international-single — content state (Step 5: Review)

> Source: screens/pay-international-single/ui.yaml + demo-data.yaml · design-system/DESIGN.md
> DO NOT redeclare colors, fonts, or spacing — they live in the uploaded design system.
> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or act may look tappable. Review rows and non-interactive text
> are NOT tappable.

## Archetype: screen

## State

`content` — Step 5 (Review). Account "Current account" (80200110203349). Recipient IBAN
DE89370400440532013000, name "Klara Weiss", BIC "COBADEFFXXX". Instructed £5.00 GBP,
transfer currency EUR. Charge bearer BorneByCreditor. Consent staged with NO Charges array.
review_card and confirm_button render. No fee row, no reference row.

## Layout

Scrollable column, 16dp screen_padding, start-aligned.

## Composition (top → bottom)

1. **TopAppBar** — title "Pay abroad", `titleLarge` `onSurface`, back `arrow_back`,
   background `surface`.

2. **StepIndicator** — 5 steps, full width, 48dp. Steps 1–4 inactive (`labelMedium`
   `onSurfaceVariant`), step 5 "Review" active (`labelMedium` `primary`).
   Labels: "Account" · "Recipient" · "Amount" · "Charges" · "Review"

3. **review_card** — `review_card` component, radius `rounded.medium`,
   container `surfaceContainer`, elevation 1. Six rows:
   - "From" → "Current account  ·  80200110203349"
   - "To" → "DE89370400440532013000" (Roboto Mono, `onSurface`)
   - "Recipient's bank" → "COBADEFFXXX"
   - "Amount" → "£5.00" (Roboto Mono, `onSurface`)
   - "Arrives in" → "EUR"
   - "Who pays the fees" → "The recipient pays all the fees"
   NO fee row — this rail returns no Charges array (verified across 33 consents).
   NO reference row — RemittanceInformation is refused on international rails with U005.
   Row: `bodyMedium` label `onSurfaceVariant` left · `bodyLarge` value `onSurface` right,
   1dp `outlineVariant` dividers, 16dp horizontal padding, 14dp vertical padding.

4. **confirm_button** — `button_filled` pill, full width, 56dp, container `primary`,
   label `onPrimary`, `labelLarge`. Text: "Send £5.00".
   Money moves on tap — amount-bearing CTA per DESIGN.md §Do's.

5. **Cancel** — text button, centred, `bodyLarge` `primary`. Text: "Cancel".

6. **BottomNav** — 80dp `surfaceContainer`. Pay tab active.

## Design tokens (by name only)

Colors `surface` `onSurface` `onSurfaceVariant` `primary` `outlineVariant`
`surfaceContainer` · Type `titleLarge` `bodyLarge` `bodyMedium` `labelLarge`
`labelMedium` · Icons `arrow_back`.

## Self-Validation Checklist

- [ ] Stepper: 5 steps, "Account · Recipient · Amount · Charges · Review". Step 5 active.
- [ ] review_card: exactly 6 rows — From, To, Recipient's bank, Amount, Arrives in,
  Who pays the fees.
- [ ] NO fee row — this rail carries no Charges. Do NOT render "£0.00", "No fee" or blank.
- [ ] NO reference row — the international rail refuses RemittanceInformation.
- [ ] NO exchange rate, NO converted amount, NO "you'll receive" figure anywhere.
- [ ] NO amend notice — this is an instant payment, not deferred.
- [ ] Confirm CTA reads "Send £5.00" — amount-bearing because money moves on tap.
- [ ] IBAN in Roboto Mono.
- [ ] Confirm button NOT `error` colour — `primary` filled pill only.
- [ ] Tokens by name — no hex literals.

If any checkpoint fails → fix the output before returning.

↑↑↑ MOCKUP PROMPT
