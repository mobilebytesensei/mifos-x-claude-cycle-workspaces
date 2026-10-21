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
state: content_no_eligible_accounts
state_visibility: content_no_eligible_accounts

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# pay-international-single — content_no_eligible_accounts state

> COPY PROVENANCE: title and body are VERBATIM `strings.payment.no_eligible_accounts_{title,
> body}`; the screen title is `strings.pay_international_single.title`. The CTA is [UNSOURCED]
> — the inherited `no_eligible_accounts` empty_state declares title and body only, no button,
> and no key covers one.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).
> Only elements that navigate or act may look tappable.

## Archetype: screen

Empty state. Accounts loaded but no SortCodeAccountNumber account exists — only Global Money
accounts, which are excluded from this rail. The form cannot proceed.

## Layout
scrollable_column · padding spacing.md · gap spacing.md · alignment start · single-column

## Composition (top → bottom)

1. **Top app bar** — title "Pay abroad", arrow_back; no trailing actions
2. **stepper** (#step_indicator) — 5 steps; step 1 "current" but unavailable; all labels
   onSurfaceVariant
3. **empty_state** (#no_eligible_accounts) — centred:
   - Icon `account_balance_wallet`, icon.xl (48dp), onSurfaceVariant
   - Title: "No account you can pay from" (titleMedium, onSurface, centred)
   - Body: "This payment can only be made from an account with a sort code and account number.
     None of the accounts you have shared can be used for it." (bodyMedium, onSurfaceVariant,
     centred)
4. **button** [UNSOURCED] "Go to Accounts" — outlined, primary border + text, radius.full,
   48dp; navigates to the Accounts tab

## State-specific behavior
- Fires when `eligibleDebtorAccounts.isEmpty()` after load.
- Cause on this rail: every returned account is a Global Money account, bound by three U002
  business rules (same-account only, GBP instructed, EUR/USD transfer) — a conversion product,
  not a general payment source.
- `debtor_account_list` NOT shown. `ineligible_accounts_note` NOT shown — the empty_state
  replaces it and its body explains the absence.
- No form fields. The CTA is a navigational escape, not a primary action.

## Content source manifest
`demo-data.yaml` — AccountId "1123456843": Global Money, excluded. All other standard accounts
excluded in this demo scenario in order to trigger the empty state.

## Shell
Home → home · Accounts → accounts · Pay → payments (active) · More → settings

## Tokens
icon + body `colors.light.onSurfaceVariant` (icon.xl 48dp) · title `colors.light.onSurface`
(titleMedium) · CTA border + label `colors.light.primary` · radius.full · touch target 48dp.
All by name — no hex literals, no inline sizes.

## Self-Validation Checklist (MANDATORY)

- [ ] **Per-state shape:** the no-eligible-accounts empty state only. No account cards, no form
      fields, no amount/currency/charges steps.
- [ ] **Real content:** title and body are the catalogue copy above, verbatim.
- [ ] **Icon present:** account_balance_wallet at 48dp, onSurfaceVariant, centred above title.
- [ ] **CTA is outlined, not filled:** there is no primary action here, only an escape.
- [ ] **App-shell parity:** top bar + back; bottom nav Home/Accounts/Pay(active)/More.

↑↑↑ MOCKUP PROMPT
