---
ui_yaml_sha: 540a080783e58249414d730539dc09a72e3621efe763e7172cf365c7e209b939
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: 16e64fcbebf54bd20dd6de63931ba06ef534105e747834934163b188181bc184

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: detail_screen

feature: consent-detail
state: revoke_confirm
state_visibility: revoke_confirm

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# consent-detail — revoke_confirm state

> Auto-generated from screens/consent-detail/ui.yaml @ SHA c8737020f6f9ef62
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
1. **progress_circular** (#load_progress)
2. **progress_circular** (#revoke_progress) — label: "{strings.consent_detail.revoking_label}"
3. **card** (#status_header_card) — "status_header_card"
   - **row** (#bank_identity_row) — "bank_identity_row"
      - **image** (#bank_logo)
      - **chip** (#status_chip) — label: "{consent.Data.Status}"
   - **text** (#consent_id_label) — content: "{strings.consent_detail.consent_id_prefix}: {consent.Data.ConsentId}"
4. **card** (#expiry_warning_banner) — "expiry_warning_banner"
   - **row** (#expiry_warning_row) — "expiry_warning_row"
      - **icon** (#expiry_warning_icon)
      - **text** (#expiry_warning_text) — content: "{strings.consent_detail.expiry_warning}"
5. **section_header** (#dates_header) — label: "{strings.consent_detail.section.access_period}"
6. **list** (#dates_list) — "dates_list"
   - **list_item** (#created_date_row) — icon: "event"
   - **list_item** (#expiry_date_row) — icon: "event_busy"
   - **list_item** (#transaction_from_row) — icon: "history"
   - **list_item** (#transaction_to_row) — icon: "event_available"
7. **button** (#reconfirm_button) — label: "{strings.consent_detail.reconfirm_button}", icon: "refresh", on_click: { action: navigate_reconfirm, target: login }
8. **section_header** (#permissions_header) — label: "{strings.consent_detail.section.data_shared}"
9. **list** (#permissions_list) — "permissions_list"
   - **list_item** (#permission_row) — icon: "check_circle_outline"
10. **button** (#revoke_button) — label: "{strings.consent_detail.revoke_button}", icon: "link_off", on_click: { action: confirm_revoke }
11. **dialog** (#revoke_confirm_dialog) — "{strings.consent_detail.revoke_dialog.title}"
   - **button** (#dialog_cancel_button) — label: "{strings.consent_detail.revoke_dialog.cancel}", on_click: { action: dismiss_revoke_confirm }
   - **button** (#dialog_confirm_button) — label: "{strings.consent_detail.revoke_dialog.confirm}", on_click: { action: execute_revoke }
12. **error_state** (#error_state) — "{strings.consent_detail.error.title}"
   - **button** (#retry_button) — label: "{strings.consent_detail.error.retry}", on_click: { action: retry_load }
13. **empty_state** (#empty_state) — "{strings.consent_detail.empty.title}"
   - **button** (#empty_go_back_button) — label: "{strings.consent_detail.empty.go_back}", on_click: { action: navigate_back, target: consent-list }

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
- [ ] **Archetype honored:** the layout follows the "detail_screen" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
