---
ui_yaml_sha: e72e04a91d558e4a502994bd6e0c2ab2c19e3c197a0b646570e7e93e26752c29
design_md_hash: c1e7dbe50f7725a08e0369f4cb0659b8c1e56ac645d128a4c90c66b8618666ef
app_shell_hash: 264d7f9fcb782395f19aa57e9b86ba58ec08c244a0a79396c86f22acdcf7db41
design_read_hash: 
content_hash: edc4cb36f55b2814f0ddc4283ecd107d72f9bd0b004bfc024169f78796f10fa5

design_read_aesthetic: taste-default
design_read_dials: {variance: 7, motion: 6, density: 4}
aesthetic_variant_override: null
archetype: list_screen

feature: offlineSync
state: content
state_visibility: content

project_id: '10780096558615730514'
design_system_id: '9551377288795375599'

generated_by: stitch-prompt-build.ts v2.1.0
prompt_template_version: stitch-per-state-v3.1.0
craft_rules_version: v1.2.0
polished_by: claude-in-session (Step 2 POLISH, source = screens/offlineSync/preview/content.html)
---

# offlineSync — content state

> Polished from screens/offlineSync/ui.yaml @ SHA 7af58ab8e2f172e3 + the approved preview tier.
> Stitch DesignSystem: 9551377288795375599

↓↓↓ MOCKUP PROMPT

Design the content state of the Offline sync screen for **Mifos X Field Officer**, a microfinance field-officer app that keeps centres, groups and clients on the phone so the officer can work where there is no signal. Material 3 light theme, 412×915dp phone, the design system's own type scale (do not change the font).

Palette: background #FAFAFB, surface #FFFFFF, onSurface #0F172A, onSurfaceVariant #475569, primary #4338CA, onPrimary #FFFFFF, primaryContainer #E0E7FF, onPrimaryContainer #1F1D75, secondary #059669, secondaryContainer #D1FAE5, tertiary #D97706, tertiaryContainer #FEF3C7, error #DC2626, outline #94A3B8, outlineVariant #CBD5E1.

Shell: this is a Settings sub-screen. Top app bar with a back arrow and the title only. NO bottom navigation bar, NO drawer, NO tabs in the app bar. One extended FAB.

**Component 1 - Top App Bar** (64dp tall, full width, background #FAFAFB): leading back-arrow icon #475569, title "Offline sync" semibold title-large #0F172A, left aligned. No trailing actions.

**Component 2 - Summary Card** (full width minus 16dp insets, 16dp radius, surface #FFFFFF, 1dp #CBD5E1 border, soft shadow, 16dp padding, 12dp vertical gap): a chip row with "Online" (secondaryContainer #D1FAE5, a small #064E3B dot) and "3 to sync" (tertiaryContainer #FEF3C7, sync-problem icon). Below, three equal level tiles in one row, each 12dp radius on #FAFAFB with a 1dp #E2E8F0 border: big number then caption with icon: "2" Centres, "5" Groups, "43" Clients, numbers tabular. Caption "Last synced 2 h ago, Manual" in #475569. Full-width 48dp pill button "Sync now" filled #4338CA with a sync icon.

**Component 3 - On this device Card** (full width minus 16dp insets, same card style, list_screen archetype, rows 68dp tall with 40dp rounded-square initials avatars, indented child rows 56dp tall with 32dp avatars on #FBFBFD): heading "On this device" semibold. A Chip Row of three level tabs, 36dp tall, 8dp radius: "Centres 2" selected (primaryContainer #E0E7FF fill, #4338CA border), "Groups 5" and "Clients 43" outlined #CBD5E1. Then divided rows, each with an avatar (#E0E7FF for centres, #F3E8FF for groups), name, a counts line in #475569 and a small status line with icon. Row one: Arin Savings, counts 2 groups and 11 clients, status Waiting to sync, chosen just now, in #4338CA with a clock icon, trailing delete icon and expand chevron. Row two: Centro Arin, counts 3 groups, 31 clients and 74 accounts, status Synced 2 h ago in #059669 with a check-circle icon, trailing refresh icon and a collapse chevron because it is expanded. Under it, three indented group rows each with a trailing chevron: MARIPOSAS MONARCAS with status 12 clients, synced in #059669; Las Margaritas with status 10 clients, synced in #059669; Girasoles with status 9 clients, 2 failed in #DC2626 with an error icon.

**Component 4 - Sync Card** (same card style): heading "Sync". A two-option segmented control in a #E2E8F0 pill track: "Manual" selected (white thumb, touch icon) and "Automatic" (schedule icon). Two info lines in #475569 with leading icons: "Your records sync only when you tap Sync now. Do it before you head out." and "Syncing downloads a lot of data. Only the records you chose come to this device."

**Component 5 - Extended FAB** (56dp tall, 16dp radius, primaryContainer #E0E7FF, onPrimaryContainer label, anchored bottom-right with 24dp margin): plus icon and "Add records".

DO NOT add a hero banner, percentages, KPI sparklines or any "ready" score. DO NOT show anything about uploads, payloads, queues or pending transactions; this screen only downloads. DO NOT render a bottom navigation bar or invent sections not listed. DO NOT use em-dash characters anywhere.

Calm, practical and trustworthy: white cards on a soft #FAFAFB page with the indigo #4338CA reserved for the one primary action and the selected tab, so the officer reads at a glance what is on the phone and what still needs syncing.

↑↑↑ MOCKUP PROMPT
