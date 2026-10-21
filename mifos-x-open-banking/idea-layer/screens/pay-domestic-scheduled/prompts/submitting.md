---
feature: pay-domestic-scheduled
state: submitting
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
generated_by: idea-feature-export v1.0.0
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-scheduled — submitting state

> Auto-generated from screens/pay-domestic-scheduled/ui.yaml
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs or screens beyond the app-shell (Home, Accounts, Pay, More)
> plus the composition below.
> Only elements that navigate or act may look tappable. Titles, headings, icons and static
> labels are NOT interactive.

## Archetype: screen

## Layout

Scrollable column, default padding; stepper top-aligned, progress block vertically centred in
the remaining space. Single-column, mobile-first.

## Composition (top → bottom)

1. **top_app_bar** — back icon left (disabled, non-interactive in this state), title
   "Pay on a date".
2. **stepper** (#step_indicator) — 5 steps; Review (step 5) active (primary chip), steps 1–4
   completed (primaryContainer).
3. **progress** (#submitting_indicator) — centred in the remaining scroll content: circular
   spinner + stage label.

## State-specific behavior

- Form fields, review card and confirm button are NOT visible — replaced by the in-progress view.
- Back gesture and back button are disabled while submitting; the top-bar back icon is present
  but non-interactive (opacity 0.38 or hidden).
- CRITICAL: this rail has NO funds-confirmation stage. The single-payment rail has one; this
  one does not. A "confirming funds" label must never appear here.

## Stage labels

Render the SubmittingPayment stage as representative.

- **SubmittingPayment**: "Sending your payment"
  <!-- KEY NOTE: strings.payment.submitting is the shared caption across all rails. Its wording
       says "Sending", which is accurate on the single rail but not on this one — nothing is
       sent today, the instruction is being scheduled. Flagged for the catalogue owner; render
       it verbatim, do not paraphrase it here. -->
- **StagingConsent**: "Setting up your payment with HSBC"
- **AwaitingAuthorisation**: "Waiting for your approval at HSBC"

## Components

- **top_app_bar**: title, back icon (disabled)
- **stepper**: 5 steps, Review active (primary), 1–4 completed (primaryContainer)
- **progress** (#submitting_indicator): CircularProgressIndicator (48dp, primary, stroke 4dp,
  indeterminate) + label below (bodyMedium, onSurfaceVariant, centred)

## Shell

Home → home · Accounts → accounts · Pay → payments · More → settings.

## Tokens

Colors primary / primaryContainer / onPrimary / surface / onSurface / onSurfaceVariant · Type
titleLarge / bodyMedium / labelSmall · Spacing gap.md / gap.lg. All by name — no hex literals.

## Self-Validation Checklist

- [ ] Only the submitting state — no form fields, review card or confirm button.
- [ ] No funds-confirmation label appears anywhere in the render.
- [ ] Stage label reads "Sending your payment" — not a generic "Loading…".
- [ ] Spinner uses primary by name, label onSurfaceVariant by name. No hex codes.
- [ ] Back icon non-interactive — the PSU cannot navigate back mid-flight.
- [ ] TopAppBar + BottomNav present and consistent with the shell.

Return ONLY when all checkpoints pass.

↑↑↑ MOCKUP PROMPT
