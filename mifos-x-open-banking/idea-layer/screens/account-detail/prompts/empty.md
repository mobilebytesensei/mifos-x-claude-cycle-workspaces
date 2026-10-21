---
ui_yaml_sha: 3750313d0e3e4b069a1ea9038fa14749da04c25b496644b72c17ffeae356bacc
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: 0e9872fc25ba4e34bf0cc8b339824567a2030388be7c3b5ca2cfd5ee19cf897a

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: empty_state

feature: account-detail
state: empty
state_visibility: empty

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# account-detail — empty state

> Auto-generated from screens/account-detail/ui.yaml @ SHA 6891e3f82625ae6c
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
1. **progress_circular** (#loading_spinner)
2. **icon_button** (#back_button) — icon: "arrow_back", on_click: { action: navigate_back, target: accounts }
3. **card** (#account_header_card) — "account_header_card"
   - **text** (#account_subtype_label) — content: "{account.AccountSubType}"
   - **text** (#account_nickname) — content: "{account.Nickname}"
   - **text** (#account_identification) — content: "{account.Account.Identification}"
   - **text** (#account_currency) — content: "{account.Currency}"
   - **text** (#account_servicer) — content: "{account.Servicer.Identification}"
   - **text** (#account_last_updated) — content: "{strings.account_detail_last_updated} {account.StatusUpdateDateTime}"
4. **card** (#open_banking_badge) — "open_banking_badge"
   - **text** (#open_banking_badge_text) — content: "{strings.account_detail_open_banking_badge}"
5. **card** (#account_description_card) — "account_description_card"
   - **text** (#account_description_label) — content: "{strings.account_detail_description_label}"
   - **text** (#account_description_value) — content: "{account.Description}"
6. **section_header** (#balances_header) — label: "{strings.account_detail_section_balances}"
7. **list** (#balances_list) — "balances_list"
   - **list_item** (#balance_row)
8. **empty_state** (#balances_empty_state) — title: "{strings.account_detail_balances_empty_title}", icon: "account_balance_wallet"
9. **section_header** (#actions_header) — label: "{strings.account_detail_section_explore}"
10. **chip_row** (#action_chips) — "action_chips"
   - **chip** (#chip_transactions) — label: "{strings.nav_chip_transactions}", icon: "receipt_long", on_click: { action: navigate_transactions, target: transactions }
   - **chip** (#chip_statements) — label: "{strings.nav_chip_statements}", icon: "description", on_click: { action: navigate_statements, target: statements }
   - **chip** (#chip_standing_orders) — label: "{strings.nav_chip_standing_orders}", icon: "autorenew", on_click: { action: navigate_standing_orders, target: standing-orders }
   - **chip** (#chip_direct_debits) — label: "{strings.nav_chip_direct_debits}", icon: "subscriptions", on_click: { action: navigate_direct_debits, target: direct-debits }
   - **chip** (#chip_scheduled_payments) — label: "{strings.nav_chip_scheduled}", icon: "schedule", on_click: { action: navigate_scheduled_payments, target: scheduled-payments }
   - **chip** (#chip_beneficiaries) — label: "{strings.nav_chip_beneficiaries}", icon: "people", on_click: { action: navigate_beneficiaries, target: beneficiaries }
   - **chip** (#chip_atm_locator) — label: "{strings.account_detail.nav_chip_atm_label}", icon: "atm", on_click: { action: navigate_atm_locator, target: _placeholder-atm-locator }
   - **chip** (#chip_product) — label: "{strings.nav_chip_product}", icon: "description", on_click: { action: navigate_product, target: product }
   - **chip** (#chip_party) — label: "{strings.nav_chip_party}", icon: "person", on_click: { action: navigate_party, target: account-holder }
11. **error_state** (#error_state) — "{strings.account_detail_error_title}"
   - **button** (#retry_button) — label: "{strings.account_detail_retry}", on_click: { action: retry_load }

## State-specific behavior
- Show an empty-state illustration, a friendly message, and one primary call-to-action button.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("empty"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "detail_screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
