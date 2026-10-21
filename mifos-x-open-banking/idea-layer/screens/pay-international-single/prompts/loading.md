---
ui_yaml_sha: cc685253e60db3f0c34cb879984b188ba697cb33b60ec52a7ecd79f013a1d86d
design_md_hash: dad4a3ee16afd9663516aa33ebf1647c1d6ede5dc90a1c9bb2c448cd63c225fb
app_shell_hash: e267a146a693f7d8b57131c73d180b6010ff34beca799edb4ca3c85c5879e0b4
design_read_hash: 8f83034d22434d75ef7d377035c51c37ef557f4bbb2e0bf510409a4804964a50
content_hash: 8607734160d1bd5f4099e5f684bd37e7eef0ce6f8d1a43b6d8717d6fce117254

design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
aesthetic_variant_override: null
archetype: skeleton_screen

feature: pay-international-single
state: loading
state_visibility: loading

project_id: '17153754672098888646'
design_system_id: '2047482829824847747'

generated_by: stitch-prompt-build.ts v2.0.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.0.0
---

# pay-international-single — loading state

> COPY PROVENANCE: the top-bar title "Pay abroad" is VERBATIM
> `strings.pay_international_single.title`. This state is shimmer-only — no other user-facing
> copy renders.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).
> Only elements that navigate or act may look tappable.

## Archetype: skeleton_screen

Initial state while eligible debtor accounts are fetched from the AISP store. No real text, no
amounts, no account names. Skeleton cards shimmer block-for-block where account cards will appear.

## Layout
scrollable_column · padding spacing.md · gap spacing.md · alignment start · single-column

## Composition (top → bottom)

1. **Top app bar** — title "Pay abroad", arrow_back; no trailing actions
2. **stepper** (#step_indicator) — 5 steps, all labels onSurfaceVariant (no active step),
   circles outlined, connectors outlineVariant
3–5. **skeleton cards** ×3 (slots for debtor_account_list rows) — 72dp, surfaceContainerHighest,
   radius.md, shimmer 150ms

## State-specific behavior
- Shimmer is a left→right gradient sweep over surfaceContainerHighest, looping at
  motion.durations.short. Reduced-motion: static placeholder fill, no animation.
- No real text, amounts, or account identifiers. No buttons, no form fields.
- Bottom navigation present and navigable.

## Content source manifest
No demo data bound — all content blocks are skeleton placeholders.

## Shell
Home → home · Accounts → accounts · Pay → payments (active) · More → settings

## Tokens
surface · surfaceContainerHighest (skeleton fill) · onSurfaceVariant (step labels) ·
outlineVariant (connectors) · radius.md · spacing.md · motion.durations.short.
ALL token references by name — no hex literals, no inline sizes.

## Self-Validation Checklist (MANDATORY)

- [ ] **Per-state shape:** loading only. No real account names, amounts, or form fields.
- [ ] **Skeletons match content slots:** three cards at account-card height, not generic bars.
- [ ] **Token fidelity:** skeleton fill `surfaceContainerHighest` by name; no invented hex.
- [ ] **Step indicator present:** 5 steps, all labels onSurfaceVariant, no active step.
- [ ] **App-shell parity:** top bar + back; bottom nav Home/Accounts/Pay(active)/More.
- [ ] **No tappable decoration:** skeletons are not tappable; only back arrow and nav tabs are.

If any fail and the fix isn't clear → halt and surface "Self-validation failed at: {checkpoint}."

↑↑↑ MOCKUP PROMPT
