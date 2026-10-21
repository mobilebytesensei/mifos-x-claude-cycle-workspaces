---
feature: pay-international-standing-order
state: submitting
state_visibility: submitting
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
generated_by: idea-feature-export
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-international-standing-order — submitting state

> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.
> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More).
> Only elements that navigate or perform an action may look tappable.

<!-- COPY PROVENANCE: ui.yaml binds the three stage labels to strings.payment.staging /
     .awaiting_authorisation / .creating_mandate and all three are quoted VERBATIM below.
     strings.payment.submitting ("Sending your payment") is a DIFFERENT concept and is NOT used
     on this rail: it establishes a mandate and returns INCO; no money moves at submit time. -->

↓↓↓ MOCKUP PROMPT

## Shell
- Top app bar: title "Overseas standing order", back arrow (disabled during submission), no actions
- Bottom nav: Home / Accounts / Pay (active) / More
- Shell present and consistent

## Layout
- Scrollable column
- padding: spacing.md
- gap: spacing.lg
- mobile-first, single column

## Composition — Submitting state

The form controls are hidden. Only the stepper and progress indicator are visible.

1. **stepper** (#step_indicator)
   - 5 steps: Recipient · Schedule · Amount · Charges · Review
   - Step 5 (Review) active — the step at which the PSU confirmed
   - Steps 1–4 shown as completed
   - Dots: primary for active, outline for completed or inactive

2. **progress** (#submitting_indicator)
   - Circular progress indicator, indeterminate, color: primary
   - Centered horizontally and vertically in the content area
   - Stage label below the indicator, bodyMedium, onSurface, centered. Render the StagingConsent
     stage (first stage): "Setting up your payment with HSBC". The other two:
     AwaitingAuthorisation "Waiting for your approval at HSBC" · SubmittingPayment "Setting up
     your standing order".
   - No percentage, no estimated time, no cancel button
   <!-- NO stage may read "sent", "paid", "complete" or "money on its way" — this rail returns
        INCO (instruction established) and never PDNG. The confirm_button label
        (strings.payment.confirm_standing_order) must not be quoted here as the caption of the
        step the PSU came from. -->

## What is hidden in this state

- amount_field, iban_field, payee_name_field, bic_field, frequency_picker — all hidden
- review_card, fx_not_fixed_notice, deferred_charge_note, amend_notice — all hidden
- confirm_button — hidden (visibility: step == Review AND uiState is Content)

## Tokens
- Colors: primary / onSurface / surface — by M3 role name
- Typography: bodyMedium for stage label — by M3 role name, no inline sizes
- Spacing: spacing.md / spacing.lg — by token name
- ALL references by token name — no hex literals, no inline dp values

## Self-Validation

- [ ] Shows ONLY the submitting state — no form fields, no review card, no confirm button
- [ ] Circular progress indicator visible, color: primary, indeterminate
- [ ] Stage label is the catalogue string above, verbatim — no substituted wording
- [ ] Nothing reads "sent", "paid" or "complete"
- [ ] No exchange rate, converted amount or fee figure anywhere
- [ ] Stepper visible showing step 5 (Review) active
- [ ] App shell matches declared shell — present and consistent

↑↑↑ MOCKUP PROMPT
