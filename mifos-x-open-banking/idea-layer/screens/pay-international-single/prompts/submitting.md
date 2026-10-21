---
ui_yaml_sha: cc685253e60db3f0c34cb879984b188ba697cb33b60ec52a7ecd79f013a1d86d
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: auto

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: screen

feature: pay-international-single
state: submitting
state_visibility: submitting

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# pay-international-single — submitting state

> COPY PROVENANCE: screen title and all four stage labels are VERBATIM `_strings/strings.yaml`
> — `strings.pay_international_single.title` and
> `strings.payment.{staging, awaiting_authorisation, confirming_funds, submitting}`.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).
> Only elements that navigate or act may look tappable.

## Archetype: screen

In-progress submission. The form was confirmed and the consent is being staged. Render the
`StagingConsent` sub-stage — the first stage the PSU sees after tapping the confirm CTA.
Layout: scrollable_column · padding spacing.md · progress block centred vertically.

## Composition (top → bottom)

Only `submitting` components. All form step components are unmounted.

1. **Top app bar** — title "Pay abroad", arrow_back; no trailing actions
2. **stepper** (#step_indicator) — all 5 steps; step 5 (Review) most recently active,
   steps 1–4 completed
3. **progress** (#submitting_indicator) — centred: CircularProgressIndicator (indeterminate,
   48dp, primary stroke); stage label below (bodyLarge, onSurface, centred)

## Stage labels — catalogue verbatim

| Stage | Label |
|-------|-------|
| StagingConsent | "Setting up your payment with HSBC" |
| AwaitingAuthorisation | "Waiting for your approval at HSBC" |
| ConfirmingFunds | "Checking the money is available" |
| SubmittingPayment | "Sending your payment" |

## State-specific behavior
- Form fields, step-gated components and confirm/cancel are NOT rendered — the form unmounts
  when `uiState = Submitting`. The step indicator stays for consistent chrome.
- No cancel affordance — the consent is staged; a partial cancel would orphan it at the bank.
- **No FX rate, no fee estimate, no countdown.** There is no FX window timer on this rail.
- After AwaitingAuthorisation the flow hands off to `payment-consent`, then returns here for
  ConfirmingFunds and SubmittingPayment.

## Content source manifest — `demo-data.yaml`
- Staged consent: ConsentId "45264", AWAU · Funds: FundsAvailable "Available"
- Submit: InternationalPaymentId "19906", ACSP → navigates to payment-status
- Constraint: no exchange rate at any stage (ExchangeRateInformation refused for all three
  RateType values); no charges (this rail returns no Charges array, across 33 consents)

## Shell + Tokens
Home → home · Accounts → accounts · Pay → payments (active) · More → settings.
Progress stroke `colors.light.primary` · stage label `colors.light.onSurface` / `bodyLarge` ·
background `colors.light.surface` · indicator 48dp. All by name — no hex literals.

## Self-Validation Checklist (MANDATORY)

- [ ] **Per-state shape:** submitting only (StagingConsent). No form fields, account list,
      review card, or confirm/cancel buttons.
- [ ] **Real content:** stage label is the StagingConsent label, not "Loading…".
- [ ] **Progress indicator:** CircularProgressIndicator, indeterminate, primary, centred.
- [ ] **No FX or fee claims:** no exchange rate, fee estimate, or countdown anywhere.
- [ ] **App-shell parity:** top bar + back; bottom nav Home/Accounts/Pay(active)/More.

↑↑↑ MOCKUP PROMPT
