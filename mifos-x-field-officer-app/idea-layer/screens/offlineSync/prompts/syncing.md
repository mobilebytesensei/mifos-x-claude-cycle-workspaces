---
design_md_hash: c1e7dbe50f7725a08e0369f4cb0659b8c1e56ac645d128a4c90c66b8618666ef
app_shell_hash: 264d7f9fcb782395f19aa57e9b86ba58ec08c244a0a79396c86f22acdcf7db41
design_read_hash: 

design_read_aesthetic: taste-default
design_read_dials: {variance: 7, motion: 6, density: 4}
aesthetic_variant_override: null
archetype: list_screen

feature: offlineSync
state: syncing
state_visibility: content

project_id: '10780096558615730514'
design_system_id: '9551377288795375599'

generated_by: stitch-prompt-build.ts v2.1.0
prompt_template_version: stitch-per-state-v3.1.0
craft_rules_version: v1.2.0
polished_by: claude-in-session (Step 2 POLISH, source = screens/offlineSync/preview/syncing.html)
---

# offlineSync — syncing state

> Polished from screens/offlineSync/ui.yaml + the approved preview tier.
> Stitch DesignSystem: 9551377288795375599

↓↓↓ MOCKUP PROMPT

Design the syncing state of the Offline sync screen for **Mifos X Field Officer**, a microfinance field-officer app that keeps centres, groups and clients on the phone so the officer can work where there is no signal. Material 3 light theme, 412×915dp phone, the design system's own type scale (do not change the font).

Palette: background #FAFAFB, surface #FFFFFF, onSurface #0F172A, onSurfaceVariant #475569, primary #4338CA, onPrimary #FFFFFF, primaryContainer #E0E7FF, onPrimaryContainer #1F1D75, secondary #059669, secondaryContainer #D1FAE5, tertiary #D97706, tertiaryContainer #FEF3C7, error #DC2626, outline #94A3B8, outlineVariant #CBD5E1.

Shell: this is a Settings sub-screen. Top app bar with a back arrow and the title only. NO bottom navigation bar, NO drawer. One extended FAB.

**Component 1 - Top App Bar** (64dp tall, full width, background #FAFAFB): back arrow #475569, title "Offline sync" semibold title-large #0F172A.

**Component 2 - Summary Card** (full width minus 16dp insets, 16dp radius, surface #FFFFFF, 1dp #CBD5E1 border, 16dp padding): chips "Online, Wi-Fi" (#D1FAE5) and "Syncing 2" (#E0E7FF, sync icon). Three level tiles in one row: "2" Centres, "5" Groups, "43" Clients. Caption "Automatic, every 6 h, next at 16:00". Full-width 48dp pill button "Syncing..." disabled (#E2E8F0 fill, #94A3B8 label).

**Component 3 - Active Job Card** (same size, 2dp #4338CA border with a faint indigo glow, 16dp padding): 40dp #E0E7FF icon tile with a rotating sync icon, title "Downloading 2 records" semibold, subtitle "Arin Savings, Irving Zamora", trailing outlined pill button "Cancel". An 8dp rounded progress bar at 30% in #4338CA on #E2E8F0. A line "312 of 1,040 reads" with "~3 min left" right aligned. A step list: "Templates and products" done (check #059669, "7"), "Las Palomas, client loans" in progress (download icon #4338CA, "group 1 of 2"), "Irving Zamora" queued (#94A3B8).

**Component 4 - On this device Card** (list_screen archetype): heading "On this device", Chip Row "Centres 2" selected, "Groups 5", "Clients 43". Rows: "Arin Savings", "2 groups, 11 clients", status "Syncing... 38%" #4338CA with a thin 4dp progress bar under it; "Centro Arin", "3 groups, 31 clients, 74 accounts", status "Synced 2 h ago" #059669, trailing refresh icon and expand chevron.

**Component 5 - Sync Card**: segmented control with "Automatic" selected. Label "Re-sync your records", then interval chips "Every 1 h", "Every 6 h" (selected, #E0E7FF with #4338CA border), "Every 12 h", "Every 24 h". Two switch rows: "Wi-Fi only" ON (#4338CA track) and "Only while charging" OFF. Info line "Syncing downloads a lot of data. Only the records you chose come to this device."

**Component 6 - Extended FAB** (56dp, 16dp radius, #E0E7FF, bottom-right): plus icon and "Add records".

DO NOT add a hero banner, percentages other than the job and row progress, or any "ready" score. DO NOT show uploads, payloads, queues or pending transactions; this screen only downloads. DO NOT render a bottom navigation bar or invent sections. DO NOT use em-dash characters anywhere.

Focused and reassuring: one indigo-outlined job card carries the live motion while everything else stays calm white, so the officer sees progress without the screen feeling busy.

↑↑↑ MOCKUP PROMPT
