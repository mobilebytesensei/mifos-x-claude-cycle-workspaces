---
ui_yaml_sha: auto
design_md_hash: auto
feature: pay-domestic-standing-order
state: content
sub_state: schedule
state_visibility: content
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-standing-order — content state (Step 2: Schedule)

> Source: screens/pay-domestic-standing-order/ui.yaml + demo-data.yaml · design-system/DESIGN.md
> DO NOT redeclare colors, fonts, or spacing — they live in the uploaded design system.
> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or act may look tappable. Section labels and helper text are
> NOT tappable.

## Archetype: screen

## State

`content` — Step 2 (Schedule). Frequency picker showing "Monthly" (MNTH) selected. First
payment date set to 1 Sep 2026. End-date switch is OFF (default) — final_payment_date_picker
is hidden. frequency_picker, first_payment_date_picker and has_end_date_switch all render.

## Layout

Scrollable column, 16dp screen_padding, start-aligned.

## Composition (top → bottom)

1. **TopAppBar** — title "Standing order", `titleLarge` `onSurface`, back `arrow_back`,
   background `surface`.

2. **StepIndicator** — 4 steps, full width, 48dp. Step 2 "Schedule" active (`labelMedium`
   `primary`); steps 1, 3–4 inactive (`labelMedium` `onSurfaceVariant`).
   Labels: "Payee" · "Schedule" · "Amount" · "Review"

3. **frequency_picker** — M3 dropdown/exposed dropdown, 56dp, radius `rounded.small`,
   outline `outline` focus `primary`. Label above: "How often", `bodyMedium` `onSurfaceVariant`.
   Selected value showing in field: "Monthly". Expanded, the five options are:
   - "Weekly" (WEEK)
   - "Every 2 weeks" (FRTN)
   - "Monthly" (MNTH) ← active selection
   - "Every 3 months" (QURT)
   - "Yearly" (YEAR)
   Exactly five. No "Daily", no "Ad-hoc" — both return U002 from HSBC.

4. **first_payment_date_picker** — date input/calendar, 56dp, radius `rounded.small`.
   Label: "First payment date", `bodyMedium` `onSurfaceVariant`.
   Selected value: "1 Sep 2026". Minimum selectable: tomorrow. Weekends are selectable
   (Saturday dates staged 201 in testing; the Guide's working-day rule was not enforced).

5. **has_end_date_switch** — full-width row, 56dp, background `surface`. Leading label
   `bodyLarge` `onSurface`: "Set an end date". Trailing M3 Switch in the OFF state
   (`onSurface` track, `surfaceVariant` thumb). 16dp horizontal padding.
   Switch is OFF — final_payment_date_picker is NOT rendered.

6. **Primary action** — `button_filled` pill, full width, 56dp, `primary`/`onPrimary`,
   `labelLarge`. Text: "Next" (advances to the Amount step).

7. **BottomNav** — 80dp `surfaceContainer`. Pay tab active.

## Design tokens (by name only)

Colors `surface` `onSurface` `onSurfaceVariant` `surfaceVariant` `primary` `outline`
`surfaceContainer` · Type `titleLarge` `bodyLarge` `bodyMedium` `labelLarge`
`labelMedium` · Spacing `rounded.small` · Icons `arrow_back` `expand_more`.

## Self-Validation Checklist

- [ ] Step 2 "Schedule" active; 4-step stepper, labels "Payee · Schedule · Amount · Review".
- [ ] frequency_picker shows exactly 5 options — no "Daily", no "Ad-hoc", no 9-option list.
- [ ] "Monthly" is the currently selected value in the picker field.
- [ ] First payment date: "1 Sep 2026", minimum tomorrow, weekends selectable.
- [ ] has_end_date_switch is OFF — final_payment_date_picker NOT rendered.
- [ ] no_debtor_note NOT shown on this step (it appears on Payee step only).
- [ ] Tokens by name — no hex literals.

If any checkpoint fails → fix the output before returning.

↑↑↑ MOCKUP PROMPT
