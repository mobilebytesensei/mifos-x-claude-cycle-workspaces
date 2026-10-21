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
state: content
state_visibility: content

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# pay-international-single — content state

> COPY PROVENANCE: every quoted string is VERBATIM `_strings/strings.yaml` (`strings.payment.*`,
> `strings.pay_international_single.title`). Only the Next button is [UNSOURCED] — no key.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).
> Only elements that navigate or act may look tappable.

## Archetype: screen

Five-step form. Render the **Account step (step 1)** — the entry point once accounts load.
Layout: scrollable_column · padding spacing.md · gap spacing.md · alignment start

## Composition (top → bottom) — Step 1: Account

1. **Top app bar** — title "Pay abroad", arrow_back; no trailing actions
2. **stepper** (#step_indicator) — step 1 active (filled-primary circle, primary label);
   steps 2–5 outlined, onSurfaceVariant labels. Labels: "Account" · "Recipient" · "Amount" ·
   "Charges" · "Review"
3. **list** (#debtor_account_list) — account cards:
   - A: radio (unselected) | "Current Account" (bodyLarge onSurface) | "80-20-01  10203349"
     (bodyMedium Roboto Mono onSurfaceVariant) | "£1,234.56" (labelLarge Roboto Mono primary)
   - B: radio (unselected) | "Savings Account" | "80-20-01  20304050" | "£8,750.00"
4. **text** (#ineligible_accounts_note) — bodySmall onSurfaceVariant: "Some of your accounts are
   not shown. This payment can only be made from an account with a sort code and account number."
5. **button** (Next) [UNSOURCED] — disabled (opacity.disabled, primary fill) until an account
   is selected; radius.full; labelLarge onPrimary

## State-specific behavior
- Tapping a card fills the radio, applies primaryContainer fill, enables Next.
- No sort-code beneficiary list — saved payees fail U027, so none is offered.
- No reference field anywhere — this rail refuses RemittanceInformation with U005.
- No FX rate and no converted "you'll receive" figure at any step. No endpoint discloses one.

## Content source manifest — `demo-data.yaml`
- A and B above are both `UK.OBIE.SortCodeAccountNumber`
- `hiddenAccountCount: 1` (AccountId 1123456843 — Global Money, a conversion product)
- Charge bearers (Charges step): "You pay all the fees" · "You each pay your own bank's fees" ·
  "The recipient pays all the fees"
- IBAN DE89370400440532013000 · Klara Weiss · BIC COBADEFFXXX · £5.00 GBP instructed ·
  EUR transfer · CTA "Send £5.00" (payment.confirm "Send %1$s")

## Shell + Tokens
Home → home · Accounts → accounts · Pay → payments (active) · More → settings
primary · surfaceContainer (cards) · primaryContainer (selected) · onSurfaceVariant (helper) ·
typography.font_family.mono · radius.md · radius.full · opacity.disabled. All by name.

## Self-Validation Checklist (MANDATORY)

- [ ] Content at Step 1. No submitting spinner, no error panel.
- [ ] Account names, sort codes and balances from the manifest; balance in Roboto Mono +
      primary. Tokens by name, no hex literals.
- [ ] `ineligible_accounts_note` visible, catalogue copy verbatim.
- [ ] No FX claim: no rate, no converted amount, no "you'll receive" figure anywhere.
- [ ] Top bar + back; bottom nav Home/Accounts/Pay(active)/More.

↑↑↑ MOCKUP PROMPT
