---
ui_yaml_sha: 7c0cb9e1f948ae6b363320a673f0e82970a46883f49cfaefe44df132d000e6a8
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: f17f02b8e080628c9a68b0b530b2613a030d0d6ae9e01e4883863a542dbd9481

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: detail_screen

feature: standing-order-detail
state: no_network
state_visibility: no_network

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# standing-order-detail — no_network state

> Auto-generated from screens/standing-order-detail/ui.yaml @ SHA b71d8d8f0ccad1ce
> Stitch DesignSystem: 2047482829824847747
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Accounts, Pay, More) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: detail_screen

## Layout
- type: column
- padding: spacing.xl
- alignment: center
- responsive: any multi-column region MUST be mobile-first and collapse to a single column at narrow/phone widths — never a fixed multi-column grid with no single-column fallback.

## Composition (top → bottom)
1. **stack** (#sod_root)
2. **card** (#sod_recipient_card)
3. **text** (#sod_recipient_header) — content: "RECIPIENT"
4. **stack** (#sod_recipient_name_row)
5. **text** (#sod_recipient_name_label) — content: "Name"
6. **text** (#sod_recipient_name_value) — content: "Landlord Holdings Ltd"
7. **stack** (#sod_recipient_account_row)
8. **text** (#sod_recipient_account_label) — content: "Account"
9. **text** (#sod_recipient_account_value) — content: "····s001"
10. **card** (#sod_schedule_card)
11. **text** (#sod_schedule_header) — content: "SCHEDULE"
12. **stack** (#sod_status_row)
13. **text** (#sod_status_label) — content: "Status"
14. **text** (#sod_status_value) — content: "Active"
15. **stack** (#sod_frequency_row)
16. **text** (#sod_frequency_label) — content: "Frequency"
17. **text** (#sod_frequency_value) — content: "Monthly"
18. **stack** (#sod_first_payment_row)
19. **text** (#sod_first_payment_label) — content: "First Payment"
20. **text** (#sod_first_payment_value) — content: "1 Jan 2026"
21. **stack** (#sod_last_payment_row)
22. **text** (#sod_last_payment_label) — content: "Last Payment"
23. **text** (#sod_last_payment_value) — content: "1 May 2026"
24. **stack** (#sod_next_payment_row)
25. **text** (#sod_next_payment_label) — content: "Next Payment"
26. **text** (#sod_next_payment_value) — content: "1 Jun 2026"
27. **stack** (#sod_final_date_row)
28. **text** (#sod_final_date_label) — content: "Final Date"
29. **text** (#sod_final_date_value) — content: "Ongoing"
30. **card** (#sod_amount_card)
31. **text** (#sod_amount_header) — content: "PAYMENT AMOUNT"
32. **stack** (#sod_amount_value_row)
33. **text** (#sod_amount_value) — content: "£1,200.00"
34. **badge** (#sod_currency_badge) — content: "GBP"
35. **card** (#sod_history_card)
36. **text** (#sod_history_header) — content: "RECENT EXECUTIONS"
37. **list** (#sod_history_list)
38. **list_item** (#sod_history_row) — on_click: { action: navigate, target: transaction-detail }
39. **text** (#sod_history_row_date) — content: "1 May 2026"
40. **text** (#sod_history_row_status) — content: "Completed"
41. **text** (#sod_history_row_amount) — content: "£1,200.00"
42. **banner** (#sod_amend_notice) — title: "{strings.standing_order.amend_notice_title}", content: "{strings.standing_order.amend_notice_body}", icon: "info_outline"
43. **link** (#sod_vrp_alternative_link) — label: "{strings.standing_order.vrp_alternative}", on_click: { action: navigate, target: pay-vrp-mandate }

## State-specific behavior
- Custom state "No Network" — render per the composition below.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("no_network"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "detail_screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
