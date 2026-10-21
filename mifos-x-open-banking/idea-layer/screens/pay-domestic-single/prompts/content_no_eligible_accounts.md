---
ui_yaml_sha: auto
design_md_hash: auto
feature: pay-domestic-single
state: content_no_eligible_accounts
state_visibility: content_no_eligible_accounts
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-single — content_no_eligible_accounts state

> Source: screens/pay-domestic-single/ui.yaml + demo-data.yaml · design-system/DESIGN.md
> DO NOT redeclare colors, fonts, or spacing — they live in the uploaded design system.
> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).

↓↓↓ MOCKUP PROMPT

> Only elements that navigate or act may look tappable. Title text, body paragraphs and icon
> illustrations are NOT interactive.

## Archetype: screen

## State

`content_no_eligible_accounts` — Step 1 (Account) is current, but filtering the PSU's accounts
to SchemeName == UK.OBIE.SortCodeAccountNumber leaves the eligible list empty: no account can
fund a domestic single payment on this rail.

A **real terminal informational state, not an error**. No retry, no "add account" affordance —
the PSU simply holds no payable account type. Only step_indicator and no_eligible_accounts
render.

## Layout

Scrollable column, 32dp padding, content centred vertically in the available area.

## Composition (top → bottom)

1. **TopAppBar** — title "Pay someone", `titleLarge` `onSurface`, back icon `arrow_back`.

2. **StepIndicator** — same row as the content state; step 1 active in `primary`, steps 2–4
   `onSurfaceVariant` inactive. Labels: "Account" · "Payee" · "Amount" · "Review"

3. **EmptyState** (no_eligible_accounts) — centred in the remaining scroll area, 32dp padding:

   - Icon: closest Material Symbols no-account / unavailable-account glyph (e.g.
     `account_balance` or `money_off`), 48dp `onSurfaceVariant`.
   - Title: `headlineSmall` `onSurface`, centred — "No account you can pay from"
   - Body: `bodyMedium` `onSurfaceVariant`, centred, max-width 300dp —
     "This payment can only be made from an account with a sort code and account number. None
     of the accounts you have shared can be used for it."

   No CTA button — informational, not an error with a recovery action.

4. **BottomNav** — 80dp `surfaceContainer`, Pay tab active (`primary`).

Reached when eligibleDebtorAccounts is empty because the PSU holds only ineligible types —
GLOBAL MONEY ACCOUNT (U002 when TPP-named) and a credit card (PAN scheme, U027).

## Design tokens (by name only)

Colors `surface` `onSurface` `onSurfaceVariant` `primary` `surfaceContainer` · Type
`titleLarge` `headlineSmall` `bodyMedium` `labelMedium` · Spacing `spacing/md` `spacing/lg` ·
Icon `arrow_back`.

## Self-Validation Checklist

- [ ] Only step_indicator and no_eligible_accounts render — no account rows, ineligible note,
      form fields, confirm button or error panel.
- [ ] Title and body are the catalogue copy above, verbatim.
- [ ] NO CTA button (not "Add account", not "Retry", not "Contact support").
- [ ] Step indicator: "Account" active, others inactive.
- [ ] Does NOT look like an error — no error colours, no error icon, no red.
- [ ] Tokens by name — no hex literals.

If any checkpoint fails → fix the output before returning.

↑↑↑ MOCKUP PROMPT
