---
ui_yaml_sha: 4be40d1bcf5b17180d04b20e51e9b692e2cb3642ba257859887d69f302ff9e7e
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: 4698631170745769c65baccb87167ee0eff58445b3a9d134e75634aff7f7b8cd

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: error_state

feature: notifications
state: error
state_visibility: error

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# notifications — error state

> Auto-generated from screens/notifications/ui.yaml @ SHA a778470e30ee6c6d
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
1. **stack** (#title_action_row) — label: "Notifications header row"
2. **text** (#notifications_title) — label: "Notifications", content: "Notifications"
3. **button** (#mark_all_read_button) — label: "Mark All Read", on_click: { action: mark_all_read }
4. **text** (#section_today_label) — label: "Today", content: "Today"
5. **box** (#notification_payment_james) — label: "Payment received from James Wilson", content: "Payment received from James Wilson", on_click: { action: open_notification, target: transaction-detail }
6. **stack** (#payment_james_row) — label: "Payment from James Wilson row"
7. **box** (#payment_james_icon_bg) — label: "Payment received icon background"
8. **icon** (#payment_james_icon) — label: "Incoming payment"
9. **stack** (#payment_james_text_col) — label: "Payment from James Wilson text"
10. **text** (#payment_james_title) — label: "Payment received", content: "Payment received"
11. **text** (#payment_james_message) — label: "Payment of £50.00 received from James Wilson", content: "Payment of £50.00 received from James Wilson"
12. **text** (#payment_james_time) — label: "10 min ago", content: "10 min ago"
13. **box** (#unread_dot_payment_james) — label: "Unread indicator"
14. **box** (#notification_kyc_approved) — label: "KYC verification approved", content: "KYC verification approved", on_click: { action: open_notification, target: profile }
15. **stack** (#kyc_approved_row) — label: "KYC approved notification row"
16. **box** (#kyc_approved_icon_bg) — label: "KYC approved icon background"
17. **icon** (#kyc_approved_icon) — label: "Identity verified"
18. **stack** (#kyc_approved_text_col) — label: "KYC approved text"
19. **text** (#kyc_approved_title) — label: "KYC verification approved", content: "KYC verification approved"
20. **text** (#kyc_approved_message) — label: "Your identity has been verified. You now have full access to all account feature", content: "Your identity has been verified. You now have full access to all account feature"
21. **text** (#kyc_approved_time) — label: "1 hr ago", content: "1 hr ago"
22. **box** (#unread_dot_kyc) — label: "Unread indicator"
23. **text** (#section_earlier_label) — label: "Earlier", content: "Earlier"
24. **box** (#notification_netflix_mandate) — label: "Direct debit mandate created for Netflix", content: "Direct debit mandate created for Netflix", on_click: { action: open_notification, target: accounts }
25. **stack** (#netflix_mandate_row) — label: "Netflix mandate notification row"
26. **box** (#netflix_mandate_icon_bg) — label: "Direct debit mandate icon background"
27. **icon** (#netflix_mandate_icon) — label: "Direct debit"
28. **stack** (#netflix_mandate_text_col) — label: "Netflix mandate notification text"
29. **text** (#netflix_mandate_title) — label: "Direct debit mandate created", content: "Direct debit mandate created"
30. **text** (#netflix_mandate_message) — label: "Direct debit mandate created for Netflix — £15.99/month from your Current Accoun", content: "Direct debit mandate created for Netflix — £15.99/month from your Current Accoun"
31. **text** (#netflix_mandate_time) — label: "3 hr ago", content: "3 hr ago"
32. **box** (#notification_salary_credited) — label: "Salary credited notification", content: "Salary credited notification", on_click: { action: open_notification, target: transaction-detail }
33. **stack** (#salary_credited_row) — label: "Salary credited notification row"
34. **box** (#salary_credited_icon_bg) — label: "Salary credited icon background"
35. **icon** (#salary_credited_icon) — label: "Incoming payment"
36. **stack** (#salary_credited_text_col) — label: "Salary credited text"
37. **text** (#salary_credited_title) — label: "Salary credited", content: "Salary credited"
38. **text** (#salary_credited_message) — label: "£3,200.00 from Acme Ltd has been credited to your Current Account.", content: "£3,200.00 from Acme Ltd has been credited to your Current Account."
39. **text** (#salary_credited_time) — label: "Yesterday", content: "Yesterday"
40. **spacer** (#bottom_spacer)

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
- [ ] **Archetype honored:** the layout follows the "index_list" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
