---
feature: pay-domestic-standing-order
state: submitting
state_visibility: submitting
generated_by: idea-feature-export
design_system: Open Banking — Trust Blue v1.4.0
tokens: design-tokens.yaml v2.4.0
---

# pay-domestic-standing-order — submitting state

> Source: `screens/pay-domestic-standing-order/ui.yaml`
> Token references: by NAME only. No hex, no inline sizes.

<!-- COPY PROVENANCE: ui.yaml binds the three stage labels to strings.payment.staging /
     .awaiting_authorisation / .creating_mandate, and all three are quoted VERBATIM below.
     strings.payment.submitting ("Sending your payment") is a DIFFERENT concept and is NOT used
     on this rail: a standing order establishes a mandate and returns INCO; no money moves at
     submit time. The sub-labels, which ui.yaml does not declare at all, stay UNSOURCED =
     render the slot EMPTY. -->

↓↓↓ MOCKUP PROMPT

> Show THREE sub-frames — one per submit stage: StagingConsent, AwaitingAuthorisation, SubmittingPayment.
> Sequential states. The UI is non-interactive while submitting.
> DO NOT show form fields, payee rows, date pickers, or the confirm button.

## Archetype: progress_screen

## App Shell

- **Top app bar**: no back icon (in-flight — cannot cancel); "Standing order" (`titleLarge`, `color/onSurface`); `color/surface`
- **Bottom nav**: Home · Accounts · Pay (active) · More; `color/surfaceContainerHighest`

## Visible Components [submitting state]

**Step indicator [step_indicator]**
- Step 4 (Review) highlighted (active=Review, `color/primary`)

**Progress indicator [submitting_indicator]**
- Centered vertically and horizontally; Auto Layout Vertical, center, gap `spacing/lg`

## All three stages — identical shape

**CircularProgressIndicator** — 48dp, `color/primary`, indeterminate

**Stage label** — `titleMedium`, `color/onSurface`, center. One per sub-frame:
1. StagingConsent — "Setting up your payment with HSBC"
2. AwaitingAuthorisation — "Waiting for your approval at HSBC"
3. SubmittingPayment — "Setting up your standing order"

**Sub-label slot** — `bodyMedium`, `color/onSurfaceVariant`, center — RENDER EMPTY (one line)

The three sub-frames differ ONLY in the stage label and which step-indicator stage is active.

<!-- UNSOURCED (sub-labels): ui.yaml declares no sub-label component and no key exists.
     The previous "Please don't close this app" / "Your bank's app will open to complete
     authorisation." wordings were invented from the stage names. Left out, not rewritten. -->

## Token Usage

| Element | Token |
|---------|-------|
| Screen background | `color/surface` |
| Progress indicator | `color/primary` |
| Stage label | `color/onSurface` |
| Sub-label | `color/onSurfaceVariant` |
| Top app bar | `color/surface` / `color/onSurface` |
| Bottom nav | `color/surfaceContainerHighest` |

## Interaction Constraints

- The confirm button, all form fields, and the step back button are ABSENT.
- No interactive elements; back gesture disabled while in flight.
- No success state here; the screen transitions away on 201.

## Self-Validation

- [ ] Three sub-frames — StagingConsent, AwaitingAuthorisation, SubmittingPayment
- [ ] Each: step indicator (active=Review) + circular progress + its stage label, sub-label EMPTY
- [ ] Nothing rendered into any slot marked UNSOURCED
- [ ] Nothing reads "sent", "paid", "complete" or "sending money"
- [ ] No form fields, payee rows or confirm button visible
- [ ] All tokens by name; no hex; no inline sizes; no back icon in flight

↑↑↑ MOCKUP PROMPT
