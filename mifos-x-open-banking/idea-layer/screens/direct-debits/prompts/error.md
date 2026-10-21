---
ui_yaml_sha: 1bab00586109de79fca77dcebcbf905484b11381d46ac86223beb9e5aaef3b87
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: 23be166abaeb65e4ae24bc1764d801fac64ad6ab100926a9fa39b2c49b025dd3

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: error_state

feature: direct-debits
state: error
state_visibility: error

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# direct-debits — error state

> Auto-generated from screens/direct-debits/ui.yaml @ SHA e946a6fc3ca64838
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
1. **skeleton** (#loading_skeleton)
2. **icon_button** (#back_button) — icon: "arrow_back", on_click: { action: navigate_back, target: account-detail }
3. **chip_group** (#mandate_summary_chips)
4. **list** (#direct_debits_list) — "direct_debits_list"
   - **card** (#direct_debit_card) — "direct_debit_card"
      - **text** (#dd_originator_name) — content: "{item.name}"
      - **status_chip** (#dd_status_badge) — label: "{item.statusLabel}"
      - **text** (#dd_previous_amount) — content: "{item.amountLabel}"
      - **text** (#dd_previous_date) — content: "{strings.direct_debits.last_collected_prefix} {item.lastCollectedLabel}"
      - **text** (#dd_mandate_id) — content: "{strings.direct_debits.mandate_prefix} {item.mandateId}"
5. **empty_state** (#empty_direct_debits) — title: "{strings.direct_debits.empty_title}", icon: "subscriptions"
6. **empty_state** (#unsupported_direct_debits) — title: "{strings.direct_debits.unsupported_title}", icon: "info_outline"
7. **error_state** (#error_state) — "{strings.direct_debits.error_title}"
   - **button** (#retry_button) — label: "{strings.direct_debits.retry_label}", on_click: { action: retryload }

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
