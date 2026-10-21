---
ui_yaml_sha: auto
design_md_hash: auto
feature: pay-international-standing-order
state: content
sub_state: review
state_visibility: content
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-international-standing-order — content state (Step 5: Review)

> Source: screens/pay-international-standing-order/ui.yaml + demo-data.yaml · design-system/DESIGN.md
> DO NOT redeclare colors, fonts, or spacing — they live in the uploaded design system.
> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or act may look tappable. Review rows, banners and non-interactive
> text are NOT tappable.

## Archetype: screen

## State

`content` — Step 5 (Review). IBAN FR29NWBK60161331926819, "Mr Mark", no BIC. Monthly,
first 13 Aug 2026, final 24 Feb 2027. USD 1.02 instructed + transfer. BorneByCreditor.
Consent staged, Charges ABSENT. All three banners render; open_ended_mandate_note hidden.

## Layout

Scrollable column, 16dp screen_padding, start-aligned.

## Composition (top → bottom)

1. **TopAppBar** — title "Overseas standing order", `titleLarge` `onSurface`, back `arrow_back`,
   background `surface`.

2. **StepIndicator** — 5 steps, full width, 48dp. Step 5 "Review" active
   (`labelMedium` `primary`); steps 1–4 inactive.
   Labels: "Recipient" · "Schedule" · "Amount" · "Charges" · "Review"

3. **review_card** — `review_card` component, radius `rounded.medium`,
   container `surfaceContainer`, elevation 1. Eight rows:
   - "To" → "FR29NWBK60161331926819" (Roboto Mono)
   - "How often" → "Monthly"
   - "First payment" → "13 Aug 2026"
   - "Final payment" → "24 Feb 2027"
   - "Amount" → "USD 1.02" (Roboto Mono)
   - "Arrives in" → "USD"
   - "Who pays the fees" → "The recipient pays all the fees"
   - "HSBC's charge" → "Your bank has not quoted a fee yet" (`onSurfaceVariant`)
   Row: `bodyMedium` label · `bodyLarge` value, `outlineVariant` dividers.

4. **fx_not_fixed_notice** — WARNING banner, `tertiaryContainer`/`onTertiaryContainer`,
   `warning` icon, `bodyMedium`. Strings key: `payment.intl_so_fx_not_fixed`.

5. **deferred_charge_note** — info banner, `surfaceContainer`/`onSurface`,
   `info` icon, `bodyMedium`. Strings key: `payment.deferred_charge_note`.

6. **amend_notice** — WARNING banner, `tertiaryContainer`/`onTertiaryContainer`,
   `warning` icon, `bodyMedium`. Strings key: `payment.amend_notice_standing_order`.
   Visually prominent.

7. **confirm_button** — `button_filled` pill, full width, 56dp, container `primary`,
   label `onPrimary`, `labelLarge`. Text: "Set up this standing order".

8. **Cancel** — text button, centred, `bodyLarge` `primary`. Text: "Cancel".

9. **BottomNav** — 80dp `surfaceContainer`. Pay tab active.

## Design tokens (by name only)

Colors `surface` `onSurface` `onSurfaceVariant` `primary` `outlineVariant`
`surfaceContainer` `tertiaryContainer` `onTertiaryContainer` · Type `titleLarge`
`bodyLarge` `bodyMedium` `labelLarge` `labelMedium` · Icons `arrow_back` `warning` `info`.

## Self-Validation Checklist

- [ ] Stepper: 5 steps, "Recipient · Schedule · Amount · Charges · Review". Step 5 active.
- [ ] review_card: 8 rows — To, How often, First/Final payment, Amount, Arrives in,
  Who pays fees, HSBC's charge. No From, no BIC, no reference row.
- [ ] Fee row: "Your bank has not quoted a fee yet" — not blank, not "0.00".
- [ ] No FX rate, no converted amount, no "you'll receive" figure anywhere.
- [ ] fx_not_fixed_notice AND amend_notice: both WARNING (`tertiaryContainer`), not info.
- [ ] open_ended_mandate_note hidden (end date set in scenario).
- [ ] Confirm CTA: "Set up this standing order".
- [ ] Tokens by name — no hex literals.

If any checkpoint fails → fix the output before returning.

↑↑↑ MOCKUP PROMPT
