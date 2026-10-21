---
ui_yaml_sha: cc685253e60db3f0c34cb879984b188ba697cb33b60ec52a7ecd79f013a1d86d
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: auto

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: error_state

feature: pay-international-single
state: error
state_visibility: error

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# pay-international-single — error state

> COPY PROVENANCE: heading = `strings.payment.error_title`, retry CTA = `strings.payment.retry`,
> both VERBATIM. Row text is the bank's wire `Message`, keyed by `ErrorCode + Path`, not app
> copy. "Back to payment" is [UNSOURCED]: no key covers it.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).
> Only elements that navigate or act may look tappable.

## Archetype: error_state

A 400 came back after the consent was staged or submitted. The panel renders EVERY entry in
`Errors[]`, in wire order. Render the **two-entry fixture** (R13-10 / R9-11).
Layout: scrollable_column · padding spacing.md · gap spacing.md · alignment start

## Composition (top → bottom)

1. **Top app bar** — title "Pay abroad", arrow_back
2. **stepper** (#step_indicator) — 5 steps; step 5 (Review) most recently active
3. **error_panel** (#error_panel) — errorContainer fill, radius.md:
   - Header: error icon (24dp onErrorContainer) + "Payment could not be completed"
     (titleSmall, onErrorContainer)
   - Divider (outlineVariant, decorative)
   - Row 1: `U027` / "Unsupported scheme" / `Data.Initiation.CreditorAccount.SchemeName` —
     bodyMedium onErrorContainer; path labelSmall Roboto Mono onSurfaceVariant
   - Divider
   - Row 2 (the actionable entry): `U002` / "Debtor and Creditor Account cannot be same" /
     `Data.Initiation.DebtorAccount.Identification`
4. **button** "Try again" — outlined, primary border + text, radius.full, 48dp; triggers
   RetrySubmit with the original idempotency key
5. **button** "Back to payment" [UNSOURCED] — text button, onSurface, 48dp; returns to Review

## State-specific behavior
- Every `Errors[]` entry renders in **wire order** — never only `Errors[0]`. Row 1 is the
  scheme check (U027), already unreachable through this form. Row 2 (U002) is actionable; a
  renderer bound to `Errors[0]` hides it.
- Row copy is selected by `ErrorCode + Path`, never by `Message`: U004 alone carries four
  Messages across the corpus, so a Message-keyed lookup stops matching the day HSBC edits a
  string — and the failure mode is a blank error row.
- Not user fault. No "you entered", no "invalid input". The bank rejected the request.
- Form fields and confirm are NOT shown — the panel takes the primary position.
- Source: `demo-data.yaml#error_responses.two_entry_error`.

## Shell + Tokens
Home → home · Accounts → accounts · Pay → payments (active) · More → settings.
Panel `errorContainer`/`onErrorContainer` · path `onSurfaceVariant` + mono · dividers
`outlineVariant` · retry `primary` · radius.md · radius.full · 48dp target. All by name.

## Self-Validation Checklist (MANDATORY)

- [ ] **Per-state shape:** error only. No account list, form fields, or review card.
- [ ] **Two rows rendered:** U027 then U002, in wire order. NOT just U027.
- [ ] **Real error content:** ErrorCode + Message + Path from the manifest.
- [ ] **Tokens:** errorContainer fill, onErrorContainer text, by name. No invented hex.
- [ ] **Error framing:** no blame, no "you entered", no "invalid input".
- [ ] **App-shell parity:** top bar + back; bottom nav Home/Accounts/Pay(active)/More.

↑↑↑ MOCKUP PROMPT
