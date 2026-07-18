---
ui_yaml_sha: db62056b814559736bcf845957019a387bc2771e31179fa2a46f45a0f7767b6f
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: 9ab5327d65e10ce086c07dc5ac72d43afd990401db0e5fa5ea04916c5794bc6c

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: error_state

feature: m04-loan-portfolio
state: error
state_visibility: error

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m04-loan-portfolio — error state

> Auto-generated from screens/m04-loan-portfolio/ui.yaml @ SHA c168655e6a94b2ed
> Stitch DesignSystem: 6486719301524192685
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Collections, Sync) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.

## Archetype: master_detail

## Layout
- type: scrollable_column
- padding: default
- alignment: start

## Composition (top → bottom)
1. **header** (#header) — label: "{strings.m04_title}"
2. **text_field** (#loan_search_field) — label: "{strings.m04_loan_search}", on_click: { action: search_loans }
3. **content_area** (#loan_list) — label: "{strings.m04_loan_list}"
4. **list_item** (#loan_row) — label: "{strings.m04_loan_row}", on_click: { action: open_loan_detail, target: loan-detail }
5. **fab** (#new_loan_fab) — label: "{strings.m04_new_loan}", on_click: { action: start_loan_application, target: loan-application-wizard }
6. **chip** (#view_schedule_tab) — label: "{strings.m04_repayment_schedule}", on_click: { action: view_repayment_schedule, target: loan-detail }
7. **chip** (#view_transactions_tab) — label: "{strings.m04_transactions}", on_click: { action: view_transactions, target: loan-detail }
8. **chip** (#view_charges_tab) — label: "{strings.m04_charges}", on_click: { action: view_charges, target: loan-detail }
9. **chip** (#view_guarantors_tab) — label: "{strings.m04_guarantors}", on_click: { action: view_guarantors, target: loan-detail }
10. **chip** (#view_collateral_tab) — label: "{strings.m04_collateral}", on_click: { action: view_collateral, target: loan-detail }
11. **chip** (#view_documents_tab) — label: "{strings.m04_documents}", on_click: { action: view_documents, target: loan-detail }
12. **button** (#approve_loan_button) — label: "{strings.m04_approve}", on_click: { action: approve_loan }
13. **button** (#reject_loan_button) — label: "{strings.m04_reject}", on_click: { action: reject_loan }
14. **button** (#withdraw_loan_button) — label: "{strings.m04_withdraw}", on_click: { action: withdraw_loan }
15. **button** (#disburse_loan_button) — label: "{strings.m04_disburse}", on_click: { action: disburse_loan, target: loan-application-wizard }
16. **button** (#undo_approval_button) — label: "{strings.m04_undo_approval}", on_click: { action: undo_approval }
17. **button** (#undo_disbursal_button) — label: "{strings.m04_undo_disbursal}", on_click: { action: undo_disbursal }
18. **button** (#record_repayment_button) — label: "{strings.m04_record_repayment}", on_click: { action: record_repayment }
19. **button** (#prepay_loan_button) — label: "{strings.m04_prepay}", on_click: { action: make_prepayment }
20. **button** (#waive_interest_button) — label: "{strings.m04_waive_interest}", on_click: { action: waive_interest }
21. **button** (#write_off_button) — label: "{strings.m04_write_off}", on_click: { action: write_off_loan }
22. **button** (#foreclose_button) — label: "{strings.m04_foreclose}", on_click: { action: foreclose_loan }
23. **button** (#reschedule_button) — label: "{strings.m04_reschedule}", on_click: { action: reschedule_loan }
24. **button** (#add_charge_button) — label: "{strings.m04_add_charge}", on_click: { action: add_loan_charge }
25. **button** (#pay_charge_button) — label: "{strings.m04_pay_charge}", on_click: { action: pay_loan_charge }
26. **button** (#waive_charge_button) — label: "{strings.m04_waive_charge}", on_click: { action: waive_loan_charge }
27. **button** (#recalculate_schedule_button) — label: "{strings.m04_schedule_preview}", on_click: { action: recalculate_schedule }
28. **button** (#empty_new_loan_cta) — label: "{strings.m04_new_loan}", on_click: { action: start_loan_application, target: loan-application-wizard }
29. **button** (#retry_button) — label: "{strings.m04_retry}", on_click: { action: retry_load }

## State-specific behavior
- Show an error illustration, a short message, and a single Retry action. No content rails visible.

## Content source manifest
- (no demo collections bound for this state)

## Components (vocabulary used in this prompt)
- (no named components extracted — see composition)

## Shell (app-shell resolved for this state)
- Home: navigates to m01-dashboard
- Clients: navigates to m02-clients
- Collections: navigates to m06-collections
- Sync: navigates to m17-sync-settings
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
- [ ] **Archetype honored:** the layout follows the "master_detail" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
