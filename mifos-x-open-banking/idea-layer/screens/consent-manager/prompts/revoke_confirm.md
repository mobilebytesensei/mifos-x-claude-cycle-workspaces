---
ui_yaml_sha: e5f589b90d650c2804449869a47f31d7e4816973b2e2e3d153ad94c9d8683789
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: 698c8282cb2e85d947df4e7993190f7919fb62a00a5d23ebcc013f360f52b0bc

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: index_list

feature: consent-manager
state: revoke_confirm
state_visibility: revoke_confirm

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# consent-manager — revoke_confirm state

> Auto-generated from screens/consent-manager/ui.yaml @ SHA 833bb6d6640014fb
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
1. **text** (#consent_title) — label: "Connected Apps", content: "Connected Apps"
2. **text** (#consent_subtitle) — label: "Manage third-party apps that have access to your account data", content: "Manage third-party apps that have access to your account data"
3. **box** (#consent_moneymanager) — label: "MoneyManager Pro consent card", content: "MoneyManager Pro consent card", on_click: { action: view_consent_detail }
4. **stack** (#moneymanager_header_row) — label: "MoneyManager Pro header row"
5. **image** (#moneymanager_logo) — label: "MoneyManager Pro logo", content: "app_logo_moneymanager"
6. **stack** (#moneymanager_info) — label: "MoneyManager Pro app info"
7. **text** (#moneymanager_name) — label: "MoneyManager Pro", content: "MoneyManager Pro"
8. **text** (#moneymanager_dates) — label: "Granted 1 Mar 2026 · Expires 1 Mar 2027", content: "Granted 1 Mar 2026 · Expires 1 Mar 2027"
9. **box** (#moneymanager_active_badge) — label: "ACTIVE", content: "ACTIVE"
10. **stack** (#moneymanager_scopes_row) — label: "MoneyManager Pro consent scopes"
11. **box** (#moneymanager_scope_read_accounts) — label: "Read Accounts", content: "Read Accounts"
12. **box** (#moneymanager_scope_view_transactions) — label: "View Transactions", content: "View Transactions"
13. **box** (#moneymanager_scope_check_balances) — label: "Check Balances", content: "Check Balances"
14. **button** (#moneymanager_revoke_button) — label: "Revoke Access", on_click: { action: revoke_consent }
15. **box** (#consent_taxhelper) — label: "TaxHelper consent card", content: "TaxHelper consent card", on_click: { action: view_consent_detail }
16. **stack** (#taxhelper_header_row) — label: "TaxHelper header row"
17. **image** (#taxhelper_logo) — label: "TaxHelper logo", content: "app_logo_taxhelper"
18. **stack** (#taxhelper_info) — label: "TaxHelper app info"
19. **text** (#taxhelper_name) — label: "TaxHelper", content: "TaxHelper"
20. **text** (#taxhelper_dates) — label: "Granted 15 Jan 2026 · Expires 15 Jan 2027", content: "Granted 15 Jan 2026 · Expires 15 Jan 2027"
21. **box** (#taxhelper_active_badge) — label: "ACTIVE", content: "ACTIVE"
22. **stack** (#taxhelper_scopes_row) — label: "TaxHelper consent scopes"
23. **box** (#taxhelper_scope_view_transactions) — label: "View Transactions", content: "View Transactions"
24. **box** (#taxhelper_scope_read_accounts) — label: "Read Accounts", content: "Read Accounts"
25. **button** (#taxhelper_revoke_button) — label: "Revoke Access", on_click: { action: revoke_consent }
26. **box** (#consent_budgetwise) — label: "BudgetWise consent card", content: "BudgetWise consent card", on_click: { action: state_change, target: view_consent_detail }
27. **stack** (#budgetwise_header_row) — label: "BudgetWise header row"
28. **image** (#budgetwise_logo) — label: "BudgetWise logo", content: "app_logo_budgetwise"
29. **stack** (#budgetwise_info) — label: "BudgetWise app info"
30. **text** (#budgetwise_name) — label: "BudgetWise", content: "BudgetWise"
31. **text** (#budgetwise_dates) — label: "Granted 10 Oct 2025 · Expired 10 Apr 2026", content: "Granted 10 Oct 2025 · Expired 10 Apr 2026"
32. **box** (#budgetwise_expired_badge) — label: "EXPIRED", content: "EXPIRED"
33. **stack** (#budgetwise_scopes_row) — label: "BudgetWise consent scopes"
34. **box** (#budgetwise_scope_check_balances) — label: "Check Balances", content: "Check Balances"
35. **button** (#budgetwise_remove_button) — label: "Remove", on_click: { action: revoke_consent }
36. **box** (#revoke_confirm_dialog) — label: "Revoke access confirmation dialog", content: "Revoke access confirmation dialog"
37. **text** (#revoke_dialog_title) — label: "Revoke access?", content: "Revoke access?"
38. **text** (#revoke_dialog_body) — label: "This will immediately remove this app's access to your account data. You can rec", content: "This will immediately remove this app's access to your account data. You can rec"
39. **stack** (#revoke_dialog_actions) — label: "Revoke dialog action buttons"
40. **button** (#revoke_dialog_cancel_button) — label: "Cancel", on_click: { action: dismiss_revoke_dialog }
41. **button** (#revoke_dialog_confirm_button) — label: "Revoke", on_click: { action: confirm_revoke_consent }
42. **image** (#empty_state_icon) — label: "No connected apps illustration", content: "ic_link_off"
43. **text** (#empty_state_title) — label: "No apps connected", content: "No apps connected"
44. **text** (#empty_state_body) — label: "Third-party apps you authorise will appear here. Visit your bank's app marketpla", content: "Third-party apps you authorise will appear here. Visit your bank's app marketpla"

## State-specific behavior
- Custom state "Revoke Confirm" — render per the composition below.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("revoke_confirm"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "index_list" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
