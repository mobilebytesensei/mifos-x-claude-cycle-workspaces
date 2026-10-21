---
feature: pay-domestic-scheduled
state: content
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
generated_by: idea-feature-export v1.0.0
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-scheduled — content state

> Auto-generated from screens/pay-domestic-scheduled/ui.yaml
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs or screens beyond the app-shell (Home, Accounts, Pay, More)
> plus the composition below.
> Only elements that navigate or act may look tappable. Titles, section headings, icons,
> badges and static labels are NOT interactive.

## Archetype: screen

## Layout

Scrollable column, 16dp screen padding, start-aligned, single-column mobile-first.

## Composition (top → bottom) — Step 1: Account

All five steps share one route and chrome; only step-specific components are in focus here.

1. **top_app_bar** — back icon left, title "Pay on a date", `surface` background.
2. **stepper** (#step_indicator) — 5 steps; step 1 active (primaryContainer chip), steps 2–5
   upcoming (outline chip). Labels: "Account" · "Payee" · "Amount" · "Date" · "Review"
3. **section_label** — "Choose the account to pay from" (titleMedium, onSurface)
4. **list** (#debtor_account_list) — account rows, each tappable → advances to Step 2
5. **text** (#ineligible_accounts_note) — below the list, bodySmall, onSurfaceVariant, shown
   only when at least one account was filtered out. Text:
   "Some of your accounts are not shown. This payment can only be made from an account with a
   sort code and account number."
6. **bottom_nav** — Home · Accounts · Pay (active) · More

## State-specific behavior

- Real account list from the demo content below; no date picker, review card or confirm button.
- Selecting a row advances to Step 2 immediately — this step has no "Next" button.

## Content source (demo-data.yaml, inherited from pay-domestic-single)

- "Current Account" · 40-20-01 · 10203351 · £2,450.00 · eligible
- "Savings Account" · 40-20-01 · 10203352 · £500.00 · eligible
- 1 ineligible account (credit card — no sort code / account number)

## Components

- **stepper**: 5-step horizontal indicator; active + completed = primaryContainer chip,
  upcoming = outline chip
- **list_item** (AccountListItem): leading `account_balance` icon (primary), account name
  (bodyLarge), "sort-code / account" supporting text (bodyMedium, onSurfaceVariant), trailing
  balance (bodyLarge, mono, onSurface)

## Shell

Home → home · Accounts → accounts · Pay → payments (active) · More → settings.

## Tokens

Colors primary / primaryContainer / onPrimaryContainer / surface / onSurface /
onSurfaceVariant / outline · Type titleLarge / titleMedium / bodyLarge / bodyMedium /
bodySmall / labelSmall · Spacing gap.sm / gap.md / gap.lg · Radius radius.md, radius.full.
All by name — no hex literals, no inline size values.

## Self-Validation Checklist

- [ ] Step 1 only — no date picker, review card or confirm button.
- [ ] Real account names and balances above — no "Account 1" / filler text.
- [ ] Tokens by name — no invented hex codes or inline sizes.
- [ ] Every element maps to a named design-system component.
- [ ] Scrollable column, top → bottom per the composition.
- [ ] TopAppBar "Pay on a date" + BottomNav Home/Accounts/Pay(active)/More.

Return ONLY when all checkpoints pass.

↑↑↑ MOCKUP PROMPT
