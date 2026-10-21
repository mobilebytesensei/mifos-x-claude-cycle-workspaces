---
ui_yaml_sha: 1728f27ae1921438ccd1d2ca80e96675aeff04cf130add8429476eedb3d5c86b
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: 797a7ae6817522a6ad1d538dab5cd0a95ef7febc1f828122306defbe3a21c61d

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: error_state

feature: transaction-detail
state: error
state_visibility: error

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# transaction-detail — error state

> Auto-generated from screens/transaction-detail/ui.yaml @ SHA d814a92e0568f383
> Stitch DesignSystem: 2047482829824847747
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: detail_screen

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **progress_circular**
2. **icon_button** (#back_button) — icon: "arrow_back", on_click: { action: navigate_back, target: transactions }
3. **text** (#amount_header) — content: "{transaction.CreditDebitIndicator == 'Credit' ? '+' : '-'}£{transaction.Amount.A"
4. **text** (#transaction_currency_meta) — content: "{transaction.Amount.Currency}"
5. **text** (#merchant_name) — content: "{transaction.MerchantDetails.MerchantName || transaction.TransactionInformation}"
6. **chip** (#status_badge) — label: "{transaction.Status}"
7. **divider** (#header_separator)
8. **card** (#detail_card) — "detail_card"
   - **text** (#detail_card_header) — content: "{strings.transaction_detail_card_title}"
   - **list_item** (#booking_date_row)
   - **divider**
   - **list_item** (#value_date_row)
   - **divider**
   - **list_item** (#category_row)
   - **divider**
   - **list_item** (#mcc_row)
   - **divider**
   - **list_item** (#balance_after_row)
   - **divider**
   - **list_item** (#reference_row) — on_click: { action: copy_to_clipboard }
   - **divider**
   - **list_item** (#bank_code_row)
9. **error_state** (#error_state) — "{strings.transaction_detail_error_title}"
   - **button** (#retry_button) — label: "{strings.transaction_detail_retry}", on_click: { action: retry_load }
   - **button** (#go_back_button) — label: "{strings.transaction_detail_go_back}", on_click: { action: navigate_back }
10. **empty_state** (#transaction_empty_state) — "{strings.transaction_detail_empty_title}"
   - **button** (#transaction_empty_back_button) — label: "{strings.transaction_detail_go_back}", on_click: { action: navigate_back, target: transactions }

## State-specific behavior
- Show an error illustration, a short message, and a single Retry action. No content rails visible.

## Content source manifest
- (no demo collections bound for this state)

## Components (vocabulary used in this prompt)
- (no named components extracted — see composition)

## Shell (app-shell resolved for this state)
- Home: navigates to home
- Accounts: navigates to accounts
- Pay: navigates to payments
- More: navigates to settings
- Render MUST keep nav/bar elements consistent with the list above — present or absent, never partial.

## Tokens (design-tokens roles consumed)
- Colors: primary / secondary / surface / on-surface / on-surface-variant / error (M3 standard roles).
- Typography: body-large / title-large (M3 standard roles).
- Spacing: gap.sm / gap.md / gap.lg.
- ALL token references are by name from the uploaded design system — no hex literals, no inline size values.

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. If any fails, FIX the output and re-render.

- [ ] **Per-state shape:** the render shows ONLY this state ("error"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "detail_screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
