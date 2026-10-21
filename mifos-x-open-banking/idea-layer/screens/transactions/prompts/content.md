---
ui_yaml_sha: f51833653c43c2ea2267035178c7fa93ca4b2f76046ad99697c607a34492c4ad
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: b0cd046b90d2e5f5f14f5a22bb1a8c8840f2c97bd67a8419e0aa33fa3c40c226

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: index_list

feature: transactions
state: content
state_visibility: content

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# transactions — content state

> Auto-generated from screens/transactions/ui.yaml @ SHA 82893cf5763dbd66
> Stitch DesignSystem: 2047482829824847747
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: index_list

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **progress_circular** (#loading_spinner)
2. **stat_block** (#period_summary)
3. **chip_row** (#filter_chips) — "filter_chips"
   - **chip** (#filter_all) — label: "{strings.transactions.filter.all}", on_click: { action: filter_transactions }
   - **chip** (#filter_money_in) — label: "{strings.transactions.filter.money_in}", icon: "arrow_downward", on_click: { action: filter_transactions }
   - **chip** (#filter_money_out) — label: "{strings.transactions.filter.money_out}", icon: "arrow_upward", on_click: { action: filter_transactions }
   - **chip** (#filter_date_range) — label: "{strings.transactions.filter.date_range}", icon: "date_range", on_click: { action: open_date_range_picker }
4. **search_bar** (#search_field) — label: "{strings.transactions.search.label}"
5. **list** (#transactions_list) — "transactions_list"
   - **section_header** (#date_group_header) — label: "{group.date}"
   - **list_item** (#transaction_row) — "transaction_row"
      - **text** (#tx_merchant)
      - **chip** (#tx_category_tag)
      - **status_chip** (#tx_pending_badge) — label: "{strings.transactions.status.pending}"
6. **button** (#load_more_button) — label: "{strings.transactions.load_more}", on_click: { action: load_more_transactions }
7. **progress_linear** (#pagination_loader)
8. **empty_state** (#empty_transactions) — "{strings.transactions.empty.title}"
   - **button** (#clear_filters_button) — label: "{strings.transactions.empty.clear_filters}", on_click: { action: clear_filters }
9. **error_state** (#error_state) — "{strings.transactions.error.title}"
   - **chip** (#error_status_chip) — icon: "warning_amber"
   - **text** (#error_consent_hint) — content: "{strings.transactions.error.consent_hint}"
   - **button** (#retry_button) — label: "{strings.transactions.error.retry}", on_click: { action: retry_load }

## State-specific behavior
- Fully populated with the real demo content listed below.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("content"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "index_list" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
