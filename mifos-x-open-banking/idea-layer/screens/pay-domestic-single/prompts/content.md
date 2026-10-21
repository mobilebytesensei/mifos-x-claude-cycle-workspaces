---
ui_yaml_sha: auto
design_md_hash: auto
feature: pay-domestic-single
state: content
state_visibility: content
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-single — content state (Step 1: Account)

> Source: screens/pay-domestic-single/ui.yaml + demo-data.yaml · design-system/DESIGN.md
> DO NOT redeclare colors, fonts, or spacing — they live in the uploaded design system.
> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or act may look tappable. Section labels, note text and
> non-interactive icons are NOT tappable.

## Archetype: screen

## State

`content` — Step 1 (Account). Three eligible debtor accounts loaded, two ineligible. Only
step_indicator, debtor_account_list and ineligible_accounts_note render.

## Layout

Scrollable column, 16dp screen_padding, start-aligned.

## Composition (top → bottom)

1. **TopAppBar** — title "Pay someone", `titleLarge` `onSurface`, back icon `arrow_back`,
   background `surface`.

2. **StepIndicator** — horizontal row, full width, 48dp tall, 16dp side padding. Four steps
   separated by 1dp `outlineVariant`; step 1 active (`labelMedium` `primary`), steps 2–4
   inactive (`labelMedium` `onSurfaceVariant`).
   Labels: "Account" · "Payee" · "Amount" · "Review"

3. **Section label** — "Choose the account to pay from", `bodyMedium` `onSurfaceVariant`,
   16dp left padding, 8dp bottom gap.

4. **debtor_account_list** — three rows, 1dp `outlineVariant` dividers, each 56dp min-height
   and tappable to select. Row: `account_balance` icon (24dp `primary`) · name (`bodyLarge`
   `onSurface`) · identification (`bodyMedium` `onSurfaceVariant`, Roboto Mono) · balance
   (`bodyLarge` Roboto Mono, credit colour) + `chevron_right` (24dp `onSurfaceVariant`).
   - "Current account" · 80200110203349 · £1,250.00
   - "Current account 2" · 80200110203348 · £480.00
   - "BMM ACCOUNT" · 80122590953695 · £8,000.00

5. **ineligible_accounts_note** — visible (hiddenAccountCount = 2). Inline text below the list,
   16dp horizontal padding, 12dp top gap, `bodySmall` `onSurfaceVariant`. Text:
   "Some of your accounts are not shown. This payment can only be made from an account with a
   sort code and account number."

6. **BottomNav** — 80dp `surfaceContainer`. Pay tab active (`primary`), others
   `onSurfaceVariant`. Home → home · Accounts → accounts · Pay → payments · More → settings.

Hidden from the picker, counted in the note: "GLOBAL MONEY ACCOUNT", "Credit card".

## Design tokens (by name only)

Colors `surface` `onSurface` `onSurfaceVariant` `primary` `outlineVariant` `surfaceContainer` ·
Type `titleLarge` `bodyLarge` `bodyMedium` `bodySmall` `labelMedium` · Spacing `spacing/md`
`spacing/sm` `spacing/xs` · Icons `account_balance` `chevron_right` `arrow_back`.

## Self-Validation Checklist

- [ ] Only Step 1 components — no payee list, amount field, review card, confirm or error panel.
- [ ] Exactly 3 account rows with the real names, identifications and balances above.
- [ ] Step indicator: "Account" active, other three inactive.
- [ ] Balances in Roboto Mono, credit colour.
- [ ] Tokens by name — no hex literals.
- [ ] BottomNav: Pay tab active.

If any checkpoint fails → fix the output before returning.

↑↑↑ MOCKUP PROMPT
