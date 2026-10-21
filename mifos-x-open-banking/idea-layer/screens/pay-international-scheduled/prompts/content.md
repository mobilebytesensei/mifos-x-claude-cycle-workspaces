---
feature: pay-international-scheduled
state: content
state_visibility: content
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
generated_by: idea-feature-export
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-international-scheduled — content state (Step 1: Account)

> Source: screens/pay-international-scheduled/ui.yaml · Design system: Open Banking — Trust Blue
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

<!-- COPY PROVENANCE: all quoted copy is VERBATIM _strings/strings.yaml — strings.payment.* and
     strings.pay_international_scheduled.title. The Next button is the one exception, marked
     UNSOURCED: ui.yaml declares no such component and no key covers it. -->

↓↓↓ MOCKUP PROMPT

> DO NOT invent tabs or screens beyond the app-shell. Only elements that navigate or act may
> look tappable — static labels, headings and banners are NOT interactive.

## Layout
- scrollable_column · padding: spacing/md · gap: spacing/md · alignment: start

## Composition (top → bottom)

1. **TopAppBar** — back icon (left), "Pay abroad on a date" (titleLarge, onSurface)
2. **stepper** (#step_indicator) — 6 steps. Step 1 active (primary dot), 2–6 inactive (outlineVariant). Labels: "Account" "Recipient" "Amount" "Date" "Charges" "Review" (labelSmall, onSurfaceVariant).
3. **banner** (#ineligible_accounts_note) — severity info, secondaryContainer. Icon info_outline. Text (bodySmall, onSurfaceVariant): "Some of your accounts are not shown. This payment can only be made from an account with a sort code and account number."
4. **section_header** — "Choose the account to pay from" (titleSmall, onSurface) — payment.debtor_list_label VERBATIM
5. **list_item** (account 1) — surfaceContainerLow, radius/md, level1, 56dp min. Bank icon (icon/md, primary) · "Barclays Current Account" (bodyLarge, onSurface) / "•••• 4231" (bodyMedium, onSurfaceVariant) · trailing "£2,450.00" (bodyLarge, mono).
6. **list_item** (account 2) — same. "HSBC Advance" / "•••• 7819" / "£800.50"
7. **button** (#next_button) — filled_pill, "Next" (labelLarge, onPrimary), radius/full, full width, 56dp.
   <!-- UNSOURCED: ui.yaml declares no next_button and no key for "Next"; label unverified.
        Do NOT label it "Send" / "Pay now" — nothing is sent on this rail today. -->

<!-- fx_disclosure, deferred_charge_note and amend_notice live on the Review step, which has NO
     prompt file. Never render an FX rate, a converted "you'll receive" figure, or a fee here. -->

## State rules
- Step 1 of 6. Account rows tappable. ineligible_accounts_note shown with its catalogue text.
- No IBAN, amount, date or charge-bearer fields. Back arrow exits to the payments hub.

## Content manifest (demo data, not catalogue copy)
- Barclays Current Account •••• 4231 £2,450.00 · HSBC Advance •••• 7819 £800.50
- Hidden: 1 account (Global Money — excluded from intl rails)

## Shell + Tokens
- BottomNav: Home / Accounts / Pay (active) / More
- primary: active step dot, Next button · onPrimary: Next label
- surface / onSurface / surfaceContainerLow: background, text, account cards
- onSurfaceVariant: supporting + step labels · secondaryContainer: info banner
- outlineVariant: inactive step dots · radius/md, radius/full, spacing/md

## Self-Validation (MANDATORY)

- [ ] Step 1 only. No review card, date picker, submitting indicator.
- [ ] Nothing rendered into any slot marked UNSOURCED beyond the label given.
- [ ] No exchange rate, converted amount, or fee figure anywhere.
- [ ] All colors by token name. No hex literals.
- [ ] Components: TopAppBar, Stepper, ListItem, Banner, FilledButton only.
- [ ] BottomNav Home / Accounts / Pay (active) / More.

↑↑↑ MOCKUP PROMPT
