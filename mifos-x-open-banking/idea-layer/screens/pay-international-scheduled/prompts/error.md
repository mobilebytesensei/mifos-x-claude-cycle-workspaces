---
feature: pay-international-scheduled
state: error
state_visibility: error
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
generated_by: idea-feature-export
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-international-scheduled — error state

> Source: screens/pay-international-scheduled/ui.yaml · Design system: Open Banking — Trust Blue
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

<!-- COPY PROVENANCE: panel HEADER = strings.payment.error_title VERBATIM. Per-entry MESSAGES
     have no key at all — ui.yaml keys them by ErrorCode + Path and the panel renders the bank's
     own wire Message, which is not recorded in the idea-layer. COPY GAP = render code + path
     only, no message text. -->

↓↓↓ MOCKUP PROMPT

> DO NOT invent tabs or screens beyond the app-shell (Home, Accounts, Pay, More).
> Only the bottom button and the back arrow are tappable.

## Layout
- scrollable_column · padding: spacing/md · gap: spacing/md · alignment: start

## Composition (top → bottom)

1. **TopAppBar** — back icon (tappable), "Pay abroad on a date" (titleLarge, onSurface)
2. **stepper** (#step_indicator) — 6 steps, step 6 active (primary), 1–5 completed.
3. **error_panel** (#error_panel) — Card (errorContainer, radius/md, padding spacing/md)
   - Header: icon error (icon/md, error) + "Payment could not be completed" (titleMedium, onErrorContainer) — payment.error_title VERBATIM
   - Entry 1: code badge "U027" + path "Data.Initiation.CreditorAccount.SchemeName" (labelSmall / bodySmall, onErrorContainer). Message line: RENDER EMPTY.
   - Divider (outlineVariant — decorative)
   - Entry 2: code badge "U002" + path "Data.Initiation.CurrencyOfTransfer". Message line: RENDER EMPTY.
   - BOTH entries in wire order. Errors[0] alone hides the currency fault.
   <!-- COPY GAP ×2: no key for either message, and the HSBC wire strings for SP-I04 are not
        recorded in the idea-layer. Reserve the line; write no text. Never key copy off
        Message — U004 alone carries four wordings across the corpus. -->
4. **button** (#new_payment_button) — text style, "Start a new payment" (labelLarge, primary), radius/full
   <!-- UNSOURCED: ui.yaml declares no such button and no key. Nearest catalogue string is
        payment_status.new_payment ("Make a new payment") — a different screen, not bound here. -->

## State rules
- Renders SP-I04: two-entry Errors array — creditor scheme (U027) then currency (U002).
- Both entries in wire order. Not retryable (input fault) — no "Try again" button.
- No form fields, review card, or confirm button visible.
- No FX rate and no fee figure — neither is knowable on this rail before authorisation.

## Content manifest
- Error: SP-I04 (400, two entries). Retry: false
- Entry 1: U027 @ Data.Initiation.CreditorAccount.SchemeName — message COPY GAP
- Entry 2: U002 @ Data.Initiation.CurrencyOfTransfer — message COPY GAP

## Shell + Tokens
- BottomNav: Home / Accounts / Pay (active) / More
- errorContainer: card fill · onErrorContainer: header, badges, paths · error: leading icon
- outlineVariant: dividers · primary: button label · surface / onSurface / onSurfaceVariant
- radius/md, radius/full, spacing/md

## Self-Validation (MANDATORY)

- [ ] Error state only. No form fields, account list, or progress indicator.
- [ ] U027 and U002 both shown in wire order — not just Errors[0].
- [ ] Nothing rendered into any slot marked COPY GAP; no generic "An error occurred."
- [ ] errorContainer / onErrorContainer by name. No hex literals.
- [ ] No blame wording. No FX rate, converted amount, or fee figure.
- [ ] Components: TopAppBar, Stepper, Card (error), TextButton.
- [ ] BottomNav Home / Accounts / Pay (active) / More.

↑↑↑ MOCKUP PROMPT
