---
ui_yaml_sha: auto
design_md_hash: auto
feature: pay-international-standing-order
state: content
sub_state: schedule
state_visibility: content
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-international-standing-order — content state (Step 2: Schedule)

> Source: screens/pay-international-standing-order/ui.yaml + demo-data.yaml · design-system/DESIGN.md
> DO NOT redeclare colors, fonts, or spacing — they live in the uploaded design system.
> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or act may look tappable. Section labels and helper text are
> NOT tappable.

## Archetype: screen

## State

`content` — Step 2 (Schedule). Frequency "Monthly" selected. First payment 1 Sep 2026.
End-date switch is ON — final_payment_date_picker visible with value 1 Mar 2027. All four
schedule controls render.

## Layout

Scrollable column, 16dp screen_padding, start-aligned.

## Composition (top → bottom)

1. **TopAppBar** — title "Overseas standing order", `titleLarge` `onSurface`, back `arrow_back`,
   background `surface`.

2. **StepIndicator** — 5 steps, full width, 48dp. Step 2 "Schedule" active (`labelMedium`
   `primary`); steps 1, 3–5 inactive (`labelMedium` `onSurfaceVariant`).
   Labels: "Recipient" · "Schedule" · "Amount" · "Charges" · "Review"

3. **frequency_picker** — M3 dropdown, 56dp, radius `rounded.small`, outline `outline`
   focus `primary`. Label: "How often", `bodyMedium` `onSurfaceVariant`.
   Selected value: "Monthly". The five accepted options:
   - "Weekly" (WEEK)
   - "Every 2 weeks" (FRTN)
   - "Monthly" (MNTH) ← active selection
   - "Every 3 months" (QURT)
   - "Yearly" (YEAR)
   Exactly five. No "Daily", no "Ad-hoc" — both refused with U002.

4. **first_payment_date_picker** — date input, 56dp, radius `rounded.small`.
   Label: "First payment date", `bodyMedium` `onSurfaceVariant`. Selected: "1 Sep 2026".
   Minimum: tomorrow. Weekends selectable. Time component is preserved on this rail —
   mandate dates are NOT normalised to midnight.

5. **has_end_date_switch** — full-width row, 56dp, background `surface`. Leading label
   `bodyLarge` `onSurface`: "Set an end date". Trailing M3 Switch in the ON state.
   Switch is ON — final_payment_date_picker IS rendered.

6. **final_payment_date_picker** — date input, 56dp, radius `rounded.small`.
   Label: "Final payment date", `bodyMedium` `onSurfaceVariant`. Selected: "1 Mar 2027".
   Min: day after first payment. Max: 12 months from today (U003 constraint). Must not be
   today, tomorrow, or on/before first payment date.

7. **Primary action** — `button_filled` pill, full width, 56dp, `primary`/`onPrimary`,
   `labelLarge`. Text: "Next" (advances to Amount step).

8. **BottomNav** — 80dp `surfaceContainer`. Pay tab active.

## Design tokens (by name only)

Colors `surface` `onSurface` `onSurfaceVariant` `primary` `outline`
`surfaceContainer` · Type `titleLarge` `bodyLarge` `bodyMedium` `labelLarge`
`labelMedium` · Spacing `rounded.small` · Icons `arrow_back` `expand_more` `calendar_today`.

## Self-Validation Checklist

- [ ] Stepper: 5 steps, "Recipient · Schedule · Amount · Charges · Review". Step 2 active.
- [ ] frequency_picker: exactly 5 options — no "Daily", no "Ad-hoc".
- [ ] "Monthly" is the selected value.
- [ ] First payment: "1 Sep 2026" — min is tomorrow, weekends selectable.
- [ ] has_end_date_switch is ON — final_payment_date_picker IS rendered.
- [ ] Final payment: "1 Mar 2027" — after first payment, within 12 months, not today/tomorrow.
- [ ] Time component NOT normalised to midnight on this rail — mandate dates echo with time intact.
- [ ] Tokens by name — no hex literals.

If any checkpoint fails → fix the output before returning.

↑↑↑ MOCKUP PROMPT
