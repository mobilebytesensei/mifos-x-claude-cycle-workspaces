---
ui_yaml_sha: auto
design_md_hash: auto
feature: pay-international-scheduled
state: content
sub_state: review
state_visibility: content
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-international-scheduled — content state (Step 6: Review)

> Source: screens/pay-international-scheduled/ui.yaml + demo-data.yaml · design-system/DESIGN.md
> DO NOT redeclare colors, fonts, or spacing — they live in the uploaded design system.
> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or act may look tappable. Review rows, banners and non-interactive
> text are NOT tappable.

## Archetype: screen

## State

`content` — Step 6 (Review). Account 80200110203349. IBAN DE89370400440532013000
"Klara Weiss" COBADEFFXXX. £5.00 GBP → EUR, 13 Aug 2026. BorneByCreditor.
Charges ABSENT — fee row shows `payment.fee_unknown`. All three banners render.

## Layout

Scrollable column, 16dp screen_padding, start-aligned.

## Composition (top → bottom)

1. **TopAppBar** — title "Pay abroad on a date", `titleLarge` `onSurface`, back `arrow_back`,
   background `surface`.

2. **StepIndicator** — 6 steps, 48dp. Step 6 "Review" active (`labelMedium` `primary`);
   steps 1–5 inactive. Labels: "Account" · "Recipient" · "Amount" · "Date" · "Charges" · "Review"

3. **review_card** — `review_card` component, radius `rounded.medium`,
   container `surfaceContainer`, elevation 1. Eight rows:
   - "From" → "Current account  ·  80200110203349"
   - "To" → "DE89370400440532013000" (Roboto Mono)
   - "Recipient's bank" → "COBADEFFXXX"
   - "Amount" → "£5.00" (Roboto Mono)
   - "Arrives in" → "EUR"
   - "Payment date" → "13 Aug 2026"
   - "Who pays the fees" → "The recipient pays all the fees"
   - "HSBC's charge" → "Your bank has not quoted a fee yet" (`onSurfaceVariant`)
   No reference row. Row: `bodyMedium` label `onSurfaceVariant` · `bodyLarge` value `onSurface`,
   `outlineVariant` dividers, 16dp horizontal padding.

4. **deferred_charge_note** — info banner, `surfaceContainer` background,
   `onSurface` `bodyMedium`, `info` icon.
   Strings key: `payment.deferred_charge_note`.

5. **no_funds_check_note** — info banner, same style.
   Strings key: `payment.no_funds_check_note`.

6. **amend_notice** — info banner, same style. Visually prominent.
   Strings key: `payment.amend_notice_scheduled`.

7. **confirm_button** — `button_filled` pill, full width, 56dp, container `primary`,
   label `onPrimary`, `labelLarge`. Text: "Schedule this payment".

8. **Cancel** — text button, centred, `bodyLarge` `primary`. Text: "Cancel".

9. **BottomNav** — 80dp `surfaceContainer`. Pay tab active.

## Design tokens (by name only)

Colors `surface` `onSurface` `onSurfaceVariant` `primary` `outlineVariant`
`surfaceContainer` · Type `titleLarge` `bodyLarge` `bodyMedium` `labelLarge`
`labelMedium` · Icons `arrow_back` `info`.

## Self-Validation Checklist

- [ ] Stepper: 6 steps, "Account · Recipient · Amount · Date · Charges · Review". Step 6 active.
- [ ] review_card: exactly 8 rows — From, To, Recipient's bank, Amount, Arrives in, Payment date,
  Who pays the fees, HSBC's charge.
- [ ] Fee row text: "Your bank has not quoted a fee yet" — NOT blank, NOT "0.00", NOT "free".
- [ ] NO reference row — international rails refuse RemittanceInformation.
- [ ] NO exchange rate, NO converted amount, NO "you'll receive" figure.
- [ ] All three banners visible: deferred_charge_note, no_funds_check_note, amend_notice.
- [ ] Confirm CTA reads "Schedule this payment" — NOT "Send £5.00".
- [ ] Tokens by name — no hex literals.

If any checkpoint fails → fix the output before returning.

↑↑↑ MOCKUP PROMPT
