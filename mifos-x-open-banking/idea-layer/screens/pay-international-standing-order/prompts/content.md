---
feature: pay-international-standing-order
state: content
state_visibility: content
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
generated_by: idea-feature-export
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-international-standing-order — content state

> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.
> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).
> Only elements that navigate or act may look tappable. Labels, headings and banners are NOT.

<!-- COPY PROVENANCE: every string below is VERBATIM _strings/strings.yaml —
     strings.pay_international_standing_order.title and strings.payment.*. Nothing is
     paraphrased and nothing is invented. -->

↓↓↓ MOCKUP PROMPT

## Shell
- Top app bar: title "Overseas standing order", back arrow, no actions
- Bottom nav: Home / Accounts / Pay (active) / More — present and consistent, never partial

## Layout
- Scrollable column · padding spacing.md · section gap spacing.lg · mobile-first, single column

## Composition — Recipient step (initial state, step 1 of 5)

Active step: **Recipient** (step 1). Show only components visible on this step.

1. **stepper** (#step_indicator)
   - 5 steps: Recipient · Schedule · Amount · Charges · Review
   - Step 1 active — primary dot; steps 2–5 inactive — outlineVariant dots
   - Labels below dots in labelSmall, onSurfaceVariant

2. **text** (#no_debtor_note) — bodySmall, onSurfaceVariant: "You choose the account this comes
   from when you approve the standing order with HSBC, not here."

3. **text_field** (#iban_field) — label "Recipient's IBAN"; helper "The international account
   number for the account you are paying. Your recipient will find it on their statement.";
   outline (primary 2dp focus); radius.sm; 56dp min

4. **text_field** (#payee_name_field) — label "Recipient's name"; outline; radius.sm; 56dp min

5. **text_field** (#bic_field) — label "Recipient's BIC (optional)"; helper "Use the
   11-character form. The shorter 8-character form is not accepted. Leave this blank if you are
   not sure."; outline; radius.sm; 56dp min. Error state (bic present, length ≠ 11), bodySmall
   error: "A BIC must be exactly 11 characters"

## Step-specific notes

- No reference field. RemittanceInformation is refused on this rail (U005). By design.
- No funding-account step. The PSU picks the source account at their bank.
- No loading state — the form opens on Recipient; no network call on mount.
- Render NO exchange rate, converted amount, "you'll receive" figure or fee. fx_not_fixed_notice
  and deferred_charge_note live on Amount/Review, which have no prompt file.
- Frequency (Schedule step, no prompt file) has EXACTLY five values — WEEK, FRTN, MNTH, QURT,
  YEAR. Never render Daily or Ad-hoc.

## Tokens
- primary / onPrimary / outline / onSurfaceVariant / onSurface / surface — M3 role names
- bodySmall / bodyMedium / labelSmall · spacing.sm/md/lg · radius.sm inputs · 48dp targets
- ALL references by token name — no hex literals, no inline dp values

## Self-Validation

- [ ] Content state, Recipient step only. No blending of states.
- [ ] Three text_fields (iban, payee_name, bic); stepper step 1 active, 2–5 inactive
- [ ] All labels, helpers and the note are catalogue copy verbatim — nothing paraphrased
- [ ] No reference field; no FX rate, converted amount or fee; no hex
- [ ] App shell matches declared shell — present and consistent

↑↑↑ MOCKUP PROMPT
