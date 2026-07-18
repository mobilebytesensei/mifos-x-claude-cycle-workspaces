---
ui_yaml_sha: 43e6870edccc8314ef54e43fd4f90aa01e83ab19fef7583ca741a08a10565378
design_md_hash: b876656937552e0aa54c20cca516199c301dd5a381c6c9ba0eeeaf008bad7ee2
app_shell_hash: 002d539e63f75ae4c75647f7873343c7b914ed7430fef085387d6267e6a0867b
design_read_hash: 1bb88b83ca0ec1f4bb6eec3ee4156944dc86d382dd039ce263f6afa55009df03
content_hash: 4dc049ae2568bb5eec98a8d5147d171c2b516c77555fd4b3170bba3099c5b2e6

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 3, density: 7}
aesthetic_variant_override: null
archetype: master_detail

feature: m05-savings-deposits-shares
state: content
state_visibility: content

project_id: '16649445309504448812'
design_system_id: '6486719301524192685'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# m05-savings-deposits-shares — content state

> Auto-generated from screens/m05-savings-deposits-shares/ui.yaml @ SHA e6ebd5ac071af026
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
1. **header** (#m05_header) — label: "{strings.m05_title}"
2. **chip** (#account_type_tabs) — label: "{strings.m05_tabs}", on_click: { action: switch_account_type }
3. **content_area** (#account_list) — label: "{strings.m05_list_label}"
4. **list_item** (#account_row) — 3 items: "Savings", "Fixed Deposit", "Share"
5. **fab** (#open_account_button) — label: "{strings.m05_open_account}", on_click: { action: open_account_form, target: dynamic-template-forms }
6. **button** (#edit_account_button) — label: "{strings.m05_edit_account}", on_click: { action: edit_account_form, target: dynamic-template-forms }
7. **button** (#approve_account_button) — label: "{strings.m05_approve}", on_click: { action: approve_account }
8. **button** (#activate_account_button) — label: "{strings.m05_activate}", on_click: { action: activate_account }
9. **button** (#deposit_button) — label: "{strings.m05_deposit}", on_click: { action: record_deposit, target: dynamic-template-forms }
10. **button** (#withdrawal_button) — label: "{strings.m05_withdrawal}", on_click: { action: record_withdrawal, target: dynamic-template-forms }
11. **button** (#hold_amount_button) — label: "{strings.m05_hold}", on_click: { action: hold_amount }
12. **button** (#post_interest_button) — label: "{strings.m05_post_interest}", on_click: { action: post_interest }
13. **button** (#premature_close_button) — label: "{strings.m05_premature_close}", on_click: { action: premature_close_deposit, target: dynamic-template-forms }
14. **button** (#subscribe_shares_button) — label: "{strings.m05_subscribe_shares}", on_click: { action: subscribe_shares, target: dynamic-template-forms }
15. **button** (#redeem_shares_button) — label: "{strings.m05_redeem_shares}", on_click: { action: redeem_shares, target: dynamic-template-forms }
16. **button** (#account_transfer_button) — label: "{strings.m05_transfer}", on_click: { action: account_transfer, target: dynamic-template-forms }
17. **button** (#standing_instruction_button) — label: "{strings.m05_standing_instruction}", on_click: { action: create_standing_instruction, target: dynamic-template-forms }
18. **button** (#close_account_button) — label: "{strings.m05_close}", on_click: { action: close_account, target: dynamic-template-forms }
19. **button** (#review_failed_button) — label: "{strings.m05_review_failed}", on_click: { action: open_needs_attention, target: needs-attention-inbox }
20. **button** (#retry_button) — label: "{strings.m05_retry}", on_click: { action: retry_load }

## State-specific behavior
- Fully populated with the real demo content listed below.

## Content source manifest
- demo-data.items[0..2]

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

- [ ] **Per-state shape:** the render shows ONLY this state ("content"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "master_detail" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
