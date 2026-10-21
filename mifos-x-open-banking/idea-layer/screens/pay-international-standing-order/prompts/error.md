---
feature: pay-international-standing-order
state: error
state_visibility: error
archetype: error_state
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
generated_by: idea-feature-export
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-international-standing-order — error state

> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.
> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More).
> Only elements that navigate or perform an action may look tappable.

<!-- COPY PROVENANCE: ui.yaml gives this panel NO title binding and no per-row copy keys — by
     contract the row renders the bank's own wire Message. The one Message quoted below is a
     WIRE-OBSERVED string from the HSBC corpus, not catalogue copy. The retry label is VERBATIM
     strings.payment.retry. A panel header remains a COPY GAP — no key is bound to this slot. -->

↓↓↓ MOCKUP PROMPT

## Shell
- Top app bar: title "Overseas standing order", back arrow, no actions
- Bottom nav: Home / Accounts / Pay (active) / More — present and consistent

## Layout
- Scrollable column · padding spacing.md · gap spacing.lg · mobile-first, single column

## Composition — Error state

Form controls hidden. Only the stepper and the error panel are visible.

1. **stepper** (#step_indicator)
   - 5 steps: Recipient · Schedule · Amount · Charges · Review
   - Step 5 (Review) active — errors occur at or after submit
   - Dots: primary for active, outline for others

2. **error_panel** (#error_panel)
   - Container: errorContainer · radius.md · padding spacing.md
   - ONE ROW PER ENTRY in the bank's Errors array, in wire order. Two rows can appear at once
     (SO-I04 batching). Do not merge, sort, or truncate.
   - Row: code badge (labelMedium, error) · Path (bodySmall, onSurfaceVariant) ·
     Message (bodyMedium, onErrorContainer)
   - No panel header text and no title above the panel.
     <!-- COPY GAP: ui.yaml binds no header key here. Render the rows alone. -->

   Render this WIRE-OBSERVED example (HSBC corpus, not catalogue copy):
   ```
   U005
   Data.Initiation.FirstPaymentAmount
   "Field is not expected"
   ```

   - Retry (outlined button): ONLY when error type = NetworkError. Label "Try again"
     (payment.retry VERBATIM). Omit the button entirely in this frame.
   - U005 / U004 / U002 / U003 / U027 are non-retryable — no retry button.

## Hidden in this state

- amount_field, iban_field, payee_name_field, bic_field, review_card, fx_not_fixed_notice,
  deferred_charge_note, amend_notice, confirm_button, submitting_indicator — all hidden
- No exchange rate, converted amount or fee figure — none is knowable on this rail

## Error rendering rules

- No generic "Something went wrong" illustration and no icon above the panel. The structured
  bank response IS the communication.
- Copy is keyed by ErrorCode + Path, NEVER by Message (U004 carries four distinct Messages
  across the corpus; this rail's own U004 is "Field is missing" @ ChargeBearer).

## Tokens
- error / errorContainer / onErrorContainer / onSurfaceVariant — M3 role names
- labelMedium / bodySmall / bodyMedium · spacing.md / spacing.lg · radius.md
- ALL references by token name — no hex literals, no inline dp values

## Self-Validation

- [ ] Error state only — no form fields, review card or confirm button
- [ ] error_panel visible, errorContainer fill, at least one row, no panel header text
- [ ] Row reads "U005 / Data.Initiation.FirstPaymentAmount / Field is not expected"
- [ ] No retry button (U005 is non-retryable); nothing in a slot marked COPY GAP
- [ ] Stepper shows step 5 (Review) active; app shell matches declared shell
- [ ] No hex literals anywhere; no FX rate, converted amount or fee

↑↑↑ MOCKUP PROMPT
