---
ui_yaml_sha: e9e7a60f5fa9c739a8fc883ab0e4b04b3a061642f48cbbb3373322260ddf762f
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: 86c0122cd50ebfce305f6e58a7e66221f73ed7b7f917efbe746ffa4f41092db8

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: skeleton_screen

feature: accounts
state: loading
state_visibility: loading

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# accounts — loading state

> Auto-generated from screens/accounts/ui.yaml @ SHA 8d19e30a3f9a3ae8
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
1. **stack** (#loading_skeleton) — "loading_skeleton"
   - **shimmer** (#skeleton_card_1)
   - **shimmer** (#skeleton_card_2)
   - **shimmer** (#skeleton_card_3)
2. **chip_group** (#account_type_filter)
3. **list** (#accounts_list) — "accounts_list"
   - **card** (#account_card) — "account_card"
      - **stack**
         - **icon** (#account_type_icon)
         - **stack** (#account_text_column) — "account_text_column"
            - **text** (#account_subtype) — content: "{item.accountSubType}"
            - **text** (#account_nickname) — content: "{item.nickname}"
            - **text** (#account_number) — content: "{item.identifier}"
         - **stack** (#balance_column) — "balance_column"
            - **text** (#balance_amount) — content: "{item.balanceLabel}"
            - **badge** (#balance_owed_badge) — label: "{strings.accounts.card.balance.owed_label}"
4. **empty_state** (#empty_accounts) — title: "{strings.accounts.empty.title}", icon: "account_balance_wallet"
5. **error_state** (#error_accounts) — "{strings.accounts.error.title}"
   - **button** (#retry_button) — label: "{strings.accounts.error.retry_button}", on_click: { action: retryload }

## State-specific behavior
- Show shimmer/skeleton loaders matching the content layout block-for-block — no real text, no images. This is the screen's initial state.

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

- [ ] **Per-state shape:** the render shows ONLY this state ("loading"). Do not blend multiple states into one mockup.
- [ ] **Real content:** every text label, image, and data point reflects the content source manifest above — no numbered generic items, no filler text, no dummy text, no empty strings.
- [ ] **Token fidelity:** colors come from the uploaded design system (primary/secondary/surface/etc.) by name; spacing comes from declared scale tokens. No invented hex codes, no invented size literals.
- [ ] **Component vocabulary:** every component in the render maps to a named design-system component (Card, FAB, BottomBar, etc.) — no invented or off-system components.
- [ ] **Archetype honored:** the layout follows the "index_list" archetype skeleton — composition order top → bottom matches the Composition section.
- [ ] **App-shell parity:** if a bottom nav, top app bar, or FAB appears in the render, it matches the resolved shell from the app-shell config. Shell elements are either present-and-consistent OR absent — never partial.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 6 checkpoints pass.

↑↑↑ MOCKUP PROMPT
