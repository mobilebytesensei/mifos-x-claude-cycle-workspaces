---
feature: pay-international-scheduled
state: submitting
state_visibility: submitting
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
generated_by: idea-feature-export
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-international-scheduled — submitting state

> Source: screens/pay-international-scheduled/ui.yaml · Design system: Open Banking — Trust Blue
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

<!-- COPY PROVENANCE: ui.yaml binds the three stage labels to strings.payment.staging /
     .awaiting_authorisation / .submitting and all three are quoted VERBATIM below. KEY NOTE:
     payment.submitting is the shared caption and reads "Sending your payment", which is
     accurate on the single rail but not on this one — nothing is sent at submit time here.
     Flagged for the catalogue owner; render it verbatim, never paraphrased. -->

↓↓↓ MOCKUP PROMPT

> DO NOT invent tabs or screens beyond the declared app-shell (Home, Accounts, Pay, More).
> The form is locked during submission. Nothing is tappable except the bottom nav.

## Archetype: screen

## Layout
- type: column · padding: spacing/md · gap: spacing/lg
- alignment: top for step_indicator; center (vertical + horizontal) for progress block

## Composition (top → bottom)

1. **TopAppBar** — back icon (disabled, non-tappable), "Pay abroad on a date" (titleLarge, onSurface)
2. **stepper** (#step_indicator) — 6 steps, step 6 active (primary dot), steps 1–5 completed.
3. **progress** (#submitting_indicator) — centered in remaining content area:
   - CircularProgressIndicator: 48dp, stroke 4dp, primary, indeterminate
   - Stage label below (bodyLarge, onSurface, center). Render the AwaitingAuthorisation stage:
     "Waiting for your approval at HSBC". The other two: StagingConsent "Setting up your payment
     with HSBC" · SubmittingPayment "Sending your payment".
   <!-- This rail returns INCO — the instruction is established, no money moved. Nothing on this
        screen may say "sent", "paid" or "complete". -->

## State-specific behavior
- Form fully locked. No account list, input fields, confirm button, or error content visible.
- Step 6 active (user was at Review when submission started).
- Progress indicator is indeterminate — no percentage value.
- THREE stages only: StagingConsent / AwaitingAuthorisation / SubmittingPayment.
- No "Checking funds" stage — this rail has no funds-confirmation endpoint.
- Render the AwaitingAuthorisation stage and its label.

## Content source manifest
- Stage label: "Waiting for your approval at HSBC" (payment.awaiting_authorisation, verbatim)
- No payment amounts, FX rate, fee or account details shown during submission.

## Shell
- Home / Accounts / Pay (active) / More — BottomNav present

## Tokens
- primary: CircularProgressIndicator, active step dot
- surface: background · onSurface: stage label, TopAppBar title
- onSurfaceVariant: completed step labels
- spacing/md: screen padding · spacing/lg: gap stepper to progress block

## Self-Validation Checklist (MANDATORY)

- [ ] **Per-state shape**: submitting only. No form fields, account list, review card, or error panel.
- [ ] **No invented copy**: the stage label is the catalogue string above, verbatim.
- [ ] **No completion language**: nothing reads "sent", "paid" or "complete".
- [ ] **Token fidelity**: primary for progress indicator by name. No hex literals.
- [ ] **Component vocabulary**: TopAppBar, Stepper, CircularProgressIndicator, Text.
- [ ] **No funds step**: render does NOT include a "Checking funds…" stage label.
- [ ] **App-shell parity**: Home / Accounts / Pay (active) / More bottom nav.

↑↑↑ MOCKUP PROMPT
