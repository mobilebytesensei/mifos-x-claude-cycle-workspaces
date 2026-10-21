---
ui_yaml_sha: a50bd4c779922b076a9a89379d0dabf47f84f34c456672df596ef1fec9957914
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: 9a33b1400b1faae0073d801c4d0b72e9039b29d2907b723bb0a85fa5604ad5f4

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: error_state

feature: direct-debit-detail
state: error
state_visibility: error

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# direct-debit-detail — error state

> Auto-generated from screens/direct-debit-detail/ui.yaml @ SHA d1207b355ea00fb3
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
1. **stack** (#ddd_root)
2. **stack** (#ddd_merchant_hero)
3. **text** (#ddd_merchant_name) — content: "Netflix"
4. **status_chip** (#ddd_mandate_status_badge) — label: "{mandate.statusLabel}"
5. **text** (#ddd_mandate_amount_value) — content: "£15.99"
6. **text** (#ddd_mandate_frequency_text) — content: "Monthly"
7. **card** (#ddd_mandate_details_card)
8. **text** (#ddd_details_header) — content: "Mandate Details"
9. **stack** (#ddd_next_payment_row)
10. **text** (#ddd_next_payment_label) — content: "Next Payment"
11. **text** (#ddd_next_payment_value) — content: "15 Jun 2026"
12. **divider** (#ddd_divider_1)
13. **stack** (#ddd_account_row)
14. **text** (#ddd_account_label) — content: "Account"
15. **stack** (#ddd_account_value_group)
16. **text** (#ddd_account_name) — content: "Current Account"
17. **text** (#ddd_account_number) — content: "••••4521"
18. **divider** (#ddd_divider_2)
19. **stack** (#ddd_mandate_ref_row)
20. **text** (#ddd_mandate_ref_label) — content: "Mandate Ref"
21. **text** (#ddd_mandate_ref_value) — content: "DD-NF-20240301"
22. **divider** (#ddd_divider_3)
23. **stack** (#ddd_start_date_row)
24. **text** (#ddd_start_date_label) — content: "Start Date"
25. **text** (#ddd_start_date_value) — content: "1 Mar 2024"
26. **card** (#ddd_payment_history_card)
27. **stack** (#ddd_history_header_row)
28. **text** (#ddd_history_header) — content: "Recent Payments"
29. **link** (#ddd_history_view_all_link) — label: "View all", on_click: { action: navigate, target: transactions }
30. **list** (#ddd_history_list)
31. **list_item** (#ddd_history_row)
32. **text** (#ddd_history_row_date) — content: "15 May 2026"
33. **text** (#ddd_history_row_amount) — content: "-£15.99"
34. **button** (#ddd_cancel_button) — label: "Cancel Mandate", on_click: { action: cancel_requested, target: ddd_cancel_dialog }
35. **dialog** (#ddd_cancel_dialog) — title: "Cancel Direct Debit?", label: "Cancel Direct Debit?"
36. **button** (#ddd_cancel_confirm_cta) — label: "Yes, Cancel Mandate", on_click: { action: cancel_confirmed, target: direct-debit-detail }
37. **button** (#ddd_cancel_dismiss_cta) — label: "Keep Mandate", on_click: { action: cancel_dismissed }
38. **skeleton** (#ddd_loading_skeleton)
39. **stack** (#ddd_error_state)
40. **icon** (#ddd_error_icon) — content: "cloud_off"
41. **text** (#ddd_error_title) — content: "Unable to load mandate"
42. **text** (#ddd_error_message) — content: "Check your connection and try again"
43. **button** (#ddd_retry_button) — label: "Retry", on_click: { action: retry, target: direct-debit-detail }
44. **stack** (#ddd_empty_state)
45. **icon** (#ddd_empty_icon) — content: "event_busy"
46. **text** (#ddd_empty_title) — content: "Mandate not available"
47. **text** (#ddd_empty_message) — content: "This direct debit could not be found. It may have already been cancelled or expi"
48. **button** (#ddd_empty_back_button) — label: "Back to Direct Debits", on_click: { action: navigate_back, target: direct-debits }

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
