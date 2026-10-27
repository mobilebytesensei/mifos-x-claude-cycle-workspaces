---
design_md_hash: c1e7dbe50f7725a08e0369f4cb0659b8c1e56ac645d128a4c90c66b8618666ef
app_shell_hash: 264d7f9fcb782395f19aa57e9b86ba58ec08c244a0a79396c86f22acdcf7db41
design_read_hash: 

design_read_aesthetic: taste-default
design_read_dials: {variance: 7, motion: 6, density: 4}
aesthetic_variant_override: null
archetype: list_screen

feature: offlineSync
state: loading
state_visibility: loading

project_id: '10780096558615730514'
design_system_id: '9551377288795375599'

generated_by: stitch-prompt-build.ts v2.1.0
prompt_template_version: stitch-per-state-v3.1.0
craft_rules_version: v1.2.0
polished_by: claude-in-session (Step 2 POLISH, source = screens/offlineSync/preview/loading.html)
---

# offlineSync — loading state

> Polished from screens/offlineSync/ui.yaml + the approved preview tier.
> Stitch DesignSystem: 9551377288795375599

↓↓↓ MOCKUP PROMPT

Design the loading state of the Offline sync screen for **Mifos X Field Officer**, a microfinance field-officer app that keeps centres, groups and clients on the phone so the officer can work where there is no signal. Material 3 light theme, 412×915dp phone, the design system's own type scale (do not change the font).

Palette: background #FAFAFB, surface #FFFFFF, onSurface #0F172A, onSurfaceVariant #475569, shimmerBase #E2E8F0, shimmerHighlight #F1F5F9, outlineVariant #CBD5E1.

Shell: this is a Settings sub-screen. Top app bar with a back arrow and the title only. NO bottom navigation bar, NO drawer, NO FAB.

**Component 1 - Top App Bar** (64dp tall, background #FAFAFB): back arrow #475569 and the real title "Offline sync" semibold title-large #0F172A (the title is known before data loads).

**Component 2 - Summary Skeleton Card** (full width minus 16dp insets, 16dp radius, white, 1dp #CBD5E1 border, 16dp padding): two pill shimmer chips (84dp and 96dp wide, 32dp tall), a row of three equal 70dp shimmer tiles, one text-line shimmer at about half width, and a full-width 48dp pill shimmer where the button will be. Shimmer gradient #E2E8F0 to #F1F5F9.

**Component 3 - List Skeleton Card** (same card style, list_screen archetype skeleton): a heading shimmer at a third of the width, three 36dp shimmer tabs side by side, then three divided rows, each with a 40dp rounded-square shimmer avatar and three stacked text-line shimmers of decreasing width.

DO NOT show a spinner, a progress percentage or any real numbers. DO NOT show sections other than these two skeleton cards. DO NOT render a bottom navigation bar or a FAB. DO NOT use em-dash characters anywhere.

Quiet and instant: soft grey placeholders in exactly the shapes of the content, so the screen feels already there while local data opens.

↑↑↑ MOCKUP PROMPT
