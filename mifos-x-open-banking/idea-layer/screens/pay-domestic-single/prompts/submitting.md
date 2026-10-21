---
ui_yaml_sha: auto
design_md_hash: auto
feature: pay-domestic-single
state: submitting
state_visibility: submitting
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-single — submitting state

> Source: screens/pay-domestic-single/ui.yaml · design-system/DESIGN.md
> DO NOT redeclare colors, fonts, or spacing — they live in the uploaded design system.
> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).

↓↓↓ MOCKUP PROMPT

> Non-interactive state. Nothing should look tappable except the top-bar back icon (present but
> navigating nowhere mid-submission). The confirm button is ABSENT — it unmounted on tap.

## Archetype: screen

## State

`submitting` — entered from Content(Review) when the PSU tapped "Send £15.55". Per the
state-transition-unmount pattern the `confirm_button` ceases to exist, so double-submission is
impossible; `submitting_indicator` replaces it. Only step_indicator and submitting_indicator
render.

Render the `SubmittingPayment` sub-stage — it is the one stage with catalogue copy.

## Layout

Scrollable column, 16dp screen_padding; the indicator is centred in the remaining area.

## Composition (top → bottom)

1. **TopAppBar** — title "Pay someone", `titleLarge` `onSurface`, back icon dimmed,
   background `surface`.

2. **StepIndicator** — full-width 48dp row, all four labels `onSurfaceVariant` at
   `opacity/disabled` (0.38); no step is selectable during submission. Step 4 is the last
   completed step. Labels: "Account" · "Payee" · "Amount" · "Review"

3. **SubmittingContent** — vertically centred between step_indicator and BottomNav:

   - **CircularProgressIndicator** — indeterminate, 48dp, `primary`, horizontally centred.
     Low-motion: a static spinner arc is acceptable (`motion.intensity: low`).
   - **Stage label** — `bodyLarge` `onSurface`, centred, 16dp top gap. For SubmittingPayment:
     "Sending your payment"

   Other sub-stage labels:
   - StagingConsent — "Setting up your payment with HSBC"
   - AwaitingAuthorisation — "Waiting for your approval at HSBC"
   - ConfirmingFunds — "Checking the money is available"

   Do NOT render the confirm button as disabled or greyed — it does not exist in this state.

4. **BottomNav** — 80dp `surfaceContainer`, Pay tab active (`primary`), tabs non-interactive
   (no ripple).

The ViewModel holds ConsentId 45116, GBP 15.55, debtor 80200110203349, creditor Mr Mark
80200110203348, reference "Rent August" — none of it is visible in this state.

## Design tokens (by name only)

Colors `surface` `onSurface` `onSurfaceVariant` `primary` `surfaceContainer` · Opacity
`opacity/disabled` · Type `titleLarge` `bodyLarge` `labelMedium` · Icon `arrow_back`.

## Self-Validation Checklist

- [ ] Circular progress + stage label centred in the content area.
- [ ] confirm_button ABSENT — not disabled, not greyed, truly not rendered.
- [ ] Stage label reads "Sending your payment".
- [ ] No account rows, review card, amount field or error panel.
- [ ] Step indicator visible, all steps dimmed at `opacity/disabled`.
- [ ] Nothing looks tappable except the back icon.
- [ ] Tokens by name — no hex literals.

If any checkpoint fails → fix the output before returning.

↑↑↑ MOCKUP PROMPT
