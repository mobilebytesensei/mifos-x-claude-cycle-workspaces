---
feature: pay-international-scheduled
state: content_no_eligible_accounts
state_visibility: content_no_eligible_accounts
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
generated_by: idea-feature-export
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-international-scheduled — content_no_eligible_accounts state

> Source: screens/pay-international-scheduled/ui.yaml · Design system: Open Banking — Trust Blue
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

<!-- COPY PROVENANCE: both strings on this state are VERBATIM
     strings.payment.no_eligible_accounts_{title,body}; the screen title is
     strings.pay_international_scheduled.title. Nothing here is invented. -->

↓↓↓ MOCKUP PROMPT

> DO NOT invent tabs or screens beyond the declared app-shell (Home, Accounts, Pay, More).
> The empty state is informational, not an error. No error styling.

## Archetype: screen

## Layout
- type: scrollable_column
- padding: spacing/md · gap: spacing/lg · alignment: start (stepper), center (empty state)

## Composition (top → bottom)

1. **TopAppBar** — back icon (left), "Pay abroad on a date" (titleLarge, onSurface)
2. **stepper** (#step_indicator) — 6 steps, ALL inactive (outlineVariant dots). Labels: "Account" "Recipient" "Amount" "Date" "Charges" "Review" (labelSmall, onSurfaceVariant). Form cannot advance.
3. **empty_state** (#no_eligible_accounts) — vertically and horizontally centered in remaining space.
   - Icon: account_balance_wallet (icon/xl 48dp, onSurfaceVariant)
   - Title: headlineSmall, onSurface, center — "No account you can pay from"
   - Body: bodyMedium, onSurfaceVariant, center, padding H spacing/xl — "This payment can only
     be made from an account with a sort code and account number. None of the accounts you have
     shared can be used for it."
   <!-- Do NOT reuse payment.no_payees_title / .no_payees_body here — those describe a missing
        PAYEE, not a missing eligible DEBTOR account. Different fault entirely. -->

## State-specific behavior
- Zero eligible debtor accounts. No account list shown.
- All 6 step indicator dots inactive — the form cannot advance.
- No "Next" or "Schedule payment" button shown.
- Back arrow tappable, exits to payments hub.
- This is an informational state, not a failure. Do not style with error colors.

## Content source manifest
- eligible accounts: 0
- Empty state title + body: catalogue copy above, verbatim

## Shell
- Home / Accounts / Pay (active) / More — BottomNav present

## Tokens
- surface: background · onSurface: title, TopAppBar text
- onSurfaceVariant: all step labels (inactive), empty_state icon and body text
- outlineVariant: all 6 step dots (decorative)
- icon/xl (48dp): empty state icon · radius/full: step dot corners
- spacing/md: screen padding · spacing/lg: gap stepper to empty state · spacing/xl: body horizontal padding

## Self-Validation Checklist (MANDATORY)

- [ ] **Per-state shape**: empty state only. No account list, form fields, shimmer, or error panel.
- [ ] **No invented copy**: title and body are the catalogue copy above, verbatim.
- [ ] **Token fidelity**: onSurfaceVariant for icon and body; onSurface for title. No hex literals.
- [ ] **Component vocabulary**: TopAppBar, Stepper (all inactive), EmptyState.
- [ ] **No error styling**: empty state uses onSurfaceVariant, not error or errorContainer.
- [ ] **App-shell parity**: Home / Accounts / Pay (active) / More bottom nav.

↑↑↑ MOCKUP PROMPT
