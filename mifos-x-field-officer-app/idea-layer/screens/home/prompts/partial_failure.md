---
ui_yaml_sha: 86f8421ce713115bc2bfbea9e46365b0aec4c3aadc01880564ecc3d7d29964db
design_md_hash: c1e7dbe50f7725a08e0369f4cb0659b8c1e56ac645d128a4c90c66b8618666ef
app_shell_hash: db8da7f442f6b5759a907f50239088382e54225e9674781c0a8064f3ffd22bb0
design_read_hash: 
content_hash: ceab49caed246841df3f87ad521e2cb44aaf7bea560bd0a2b95e33bf6ea31f45

design_read_aesthetic: taste-default
design_read_dials: {variance: 7, motion: 6, density: 4}
aesthetic_variant_override: null
archetype: dashboard

feature: home
state: partial_failure
state_visibility: partial_failure

project_id: '10780096558615730514'
design_system_id: '9551377288795375599'

generated_by: stitch-prompt-build.ts v2.1.0
prompt_template_version: stitch-per-state-v3.0.0
craft_rules_version: v1.2.0
---

# home — partial_failure state

> Auto-generated from screens/home/ui.yaml @ SHA f1e1435f7754e621
> Stitch DesignSystem: 9551377288795375599
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs, or screens beyond the declared app-shell (Home, Clients, Profile) plus the composition below. Every nav item you render MUST come from that list.
> Only elements that navigate or perform an action may look tappable (cursor, ripple, pressed state). DO NOT add tap affordances to decorative content — page titles, section headings, avatars, standalone icons, badges, and static labels are NOT interactive.
> The concrete figures below are REALISTIC SAMPLE (demo) data, not fixed values — render believable content of the same KIND and MAGNITUDE (currency amounts, counts, percentages, names, timestamps). Exact reproduction is NOT required; realism and consistency ARE. Never use lorem, generic numbered placeholders, or empty content.
> **EXCEPTION — RENDER VERBATIM, NEVER SUBSTITUTE.** The licence above does NOT apply to any of the following, which must appear EXACTLY as declared, character for character, or be omitted entirely: emergency / crisis / helpline numbers and shortcodes (e.g. 988, 741741) and the ORGANISATION NAMES attached to them · legal, consent, privacy and medical-disclaimer text · medication names and dosages · security codes, auth codes and account identifiers. For these, a plausible substitute is a FABRICATION, not realism: inventing or renaming a crisis line sends a person in danger to something that does not answer. If such a value is absent from the declared data, render the element EMPTY and leave it visibly unresolved — never fill the gap with an invented one.

## Archetype: dashboard

## Visual treatment (professional design brief — honor this hierarchy)
- Lead with ONE bold summary HERO for the primary KPI — a full-width brand-gradient card (`gradient-hero-from`→`gradient-hero-to`, `on-hero` text) with the value in the display scale and a subtle sparkline; it must visually dominate.
- Below the hero, a responsive GRID of secondary stat cards — each a `surface` tile LIFTED BY A SOFT DROP SHADOW (raised, NOT flat outline-bordered boxes), generously rounded, with a colored icon chip (`chart-1`..`chart-5`), the value large in tabular-mono, a muted caption.
- Then a compact QUICK-ACTIONS row (icon-over-label buttons in `primary-container`), then a clean RECENT-ACTIVITY list (leading status icon, primary text, trailing timestamp) in its own softly-elevated card.
- Hierarchy is everything: hero dominates, stat cards equal and softly elevated, generous spacing and rounding, numerics tabular-mono. App-Store fidelity — premium and polished; one focal gradient, the rest clean surfaces lifted by soft shadow.

## Layout
- type: scrollable_column
- padding: default
- alignment: start
- responsive: the primary HERO card spans FULL WIDTH; the secondary KPI/stat cards form a COMPACT 2-COLUMN GRID (2×2 for four cards) that is INTENDED and RETAINED at phone width — this dense KPI grid IS the professional dashboard layout, so do NOT collapse the stat cards to a single column. Only genuine list/activity regions remain single-column.
- grid-fit: a stat card whose value is a LONG amount (large currency figure like a full monetary total) MUST span the FULL grid width (both columns) so the figure never truncates, wraps awkwardly, or overflows its cell; compact KPIs (counts, short percentages, small integers) sit two-per-row. Keep every numeric value and its trailing badge fully inside its card — nothing may spill past the card edge.

## Composition (top → bottom)
1. **header** (#header) — title: "Good morning, Irving", subtitle: "CENTRAL · Mon 26 Oct 2026 · Mifos field officer gateway"
2. **card** (#collections_card) — title: "Today's collections", subtitle: "Couldn't load this card · Retry", items: [Clients due today, Due today, Collected, Overdue clients] (render EXACTLY these, in this order — do not rename, add, or drop any), right_actions: [Open collection sheet]
3. **card** (#work_queue_card) — title: "Work queue", items: [Checker inbox tasks, Loans awaiting approval, Approved, awaiting disbursal, Clients pending activation, Pending reschedule requests, My unsynced drafts] (render EXACTLY these, in this order — do not rename, add, or drop any)
4. **list** (#meetings_card) "Meetings today" — 3 items: "Centro Arin", "MARIPOSAS MONARCAS", "Arin Savings"
5. **card** (#portfolio_card) — title: "Portfolio at a glance", subtitle: "1,098 active clients · 60 active loans · MX$1,284,500 outstanding · PAR 7.5%", items: [Active clients, Active loans, Outstanding, Overdue, Loans in arrears, PAR, Savings balance, Groups, Centres] (render EXACTLY these, in this order — do not rename, add, or drop any)
6. **action_grid** (#quick_actions) "Quick actions" — 6 items: "New client", "New group", "New centre", "Collection sheet", "Run reports", "Search"
7. **list** (#recent_card) "Recently opened" — 4 items: "FOTest Asha", "MARIPOSAS MONARCAS", "CREDITO A LA PALABRA · FOTest Asha", "Arin"
8. **error_state** (#card_error_retry) — title: "Couldn't load this card", label: "Retry", on_click: { action: retry_card }

## State-specific behavior
- Custom state "Partial Failure" — render per the composition below.

## Content source manifest
- demo-data.meetings[0..2]
- ui.yaml#/components[#quick_actions].properties.items[0..5]
- demo-data.recent[0..3]

## Components (vocabulary used in this prompt)
- action_grid
- card
- error_state
- header
- list

## Shell (app-shell resolved for this state)
- Home: navigates to home
- Clients: navigates to clients
- Profile: navigates to profile
- Render MUST keep nav/bar elements consistent with the list above — present or absent, never partial.

## Tokens (design-tokens roles consumed)
- Colors: primary / secondary / surface / on-surface / on-surface-variant / error (M3 standard roles).
- Typography: body-large / title-large (M3 standard roles).
- Spacing: gap.sm / gap.md / gap.lg.
- ALL token references are by name from the uploaded design system — no hex literals, no inline size values.

## Self-Validation Checklist (MANDATORY)

Before returning the rendered mockup, verify ALL of these are true. If any fails, FIX the output and re-render.

- [ ] **Per-state shape:** render ONLY the "partial_failure" state. Do not blend states.
- [ ] **Realistic content:** every label and figure realistic and of the same kind and magnitude as the samples; exact values may differ. No lorem, no numbered placeholders, no empty strings.
- [ ] **Token fidelity:** colors and spacing by design-system name. No invented hex, no invented size literals.
- [ ] **Component vocabulary:** every component maps to a named design-system component. Nothing off-system.
- [ ] **Archetype honored:** layout follows the "dashboard" skeleton; composition order top to bottom.
- [ ] **App-shell parity:** nav / app bar / FAB match the resolved shell exactly, or are absent. Never partial.
- [ ] **Every affordance leads somewhere:** anything that looks interactive resolves to a real destination. Nothing decorative-but-clickable.
- [ ] **No em-dashes:** zero em-dash characters anywhere, <title> included. Use a colon, comma or full stop.
- [ ] **One shape system:** at most THREE distinct corner radii.
- [ ] **Responsive, phone-first:** primary layout is the phone; multi-column only where it reads at phone width, everything wider stacks.

If any of these fail and the fix isn't clear → halt rendering and surface "Self-validation failed at: {checkpoint}."

Return ONLY when all 10 checkpoints pass.

↑↑↑ MOCKUP PROMPT
