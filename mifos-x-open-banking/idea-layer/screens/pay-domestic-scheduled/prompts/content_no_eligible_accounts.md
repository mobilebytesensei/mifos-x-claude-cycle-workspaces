---
feature: pay-domestic-scheduled
state: content_no_eligible_accounts
archetype: empty_state
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
generated_by: idea-feature-export v1.0.0
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-scheduled — content_no_eligible_accounts state

> Auto-generated from screens/pay-domestic-scheduled/ui.yaml
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs or screens beyond the app-shell (Home, Accounts, Pay, More)
> plus the composition below.
> Only elements that navigate or act may look tappable. Titles, headings, icons and static
> labels are NOT interactive.

## Archetype: empty_state

## Layout

Scrollable column, 16dp screen padding; empty-state content centred vertically in the
available region. Single-column, mobile-first.

## Composition (top → bottom)

1. **top_app_bar** — back icon left, title "Pay on a date".
2. **stepper** (#step_indicator) — 5 steps; step 1 active (primary chip), steps 2–5 upcoming
   (outline). Labels: "Account" · "Payee" · "Amount" · "Date" · "Review"
3. **empty_state** (#no_eligible_accounts) — centred vertically in the scroll region:
   icon `account_balance_wallet` (48dp, onSurfaceVariant), then title, then body. No CTA.
   - Title: headlineSmall, onSurface, centred — "No account you can pay from"
   - Body: bodyMedium, onSurfaceVariant, centred —
     "This payment can only be made from an account with a sort code and account number. None
     of the accounts you have shared can be used for it."
4. **bottom_nav** — Home · Accounts · Pay (active) · More

## State-specific behavior

- Accounts loaded but NONE eligible (no UK sort code + account number). The empty state
  replaces the account list entirely — no rows visible.
- No "Next" or "Continue" action; the PSU cannot proceed from here.
- Informational, not an error: it explains WHY the list is empty, not merely that it is.

## Components

- **top_app_bar**: title, back icon
- **stepper**: 5-step horizontal indicator, step 1 active
- **empty_state**: centred icon + title + supporting body; no CTA button

## Shell

Home → home · Accounts → accounts · Pay → payments (current) · More → settings.

## Tokens

Colors primary / surface / onSurface / onSurfaceVariant / outline · Type titleLarge /
headlineSmall / bodyMedium / labelSmall · Icon account_balance_wallet · Spacing gap.md /
gap.lg / gap.xl. All by name — no hex literals.

## Self-Validation Checklist

- [ ] No account rows — only the empty_state block in the scroll content.
- [ ] Title and body are the catalogue copy above, verbatim.
- [ ] Icon onSurfaceVariant, title onSurface, body onSurfaceVariant — all by token name.
- [ ] empty_state = icon + title + body; no invented layouts, no CTA.
- [ ] Centred empty_state in a scrollable column, top → bottom per the composition.
- [ ] TopAppBar + BottomNav present and consistent.

Return ONLY when all checkpoints pass.

↑↑↑ MOCKUP PROMPT
