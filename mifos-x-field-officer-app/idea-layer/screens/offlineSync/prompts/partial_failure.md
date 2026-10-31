---
design_md_hash: c1e7dbe50f7725a08e0369f4cb0659b8c1e56ac645d128a4c90c66b8618666ef
app_shell_hash: 264d7f9fcb782395f19aa57e9b86ba58ec08c244a0a79396c86f22acdcf7db41
design_read_hash: 

design_read_aesthetic: taste-default
design_read_dials: {variance: 7, motion: 6, density: 4}
aesthetic_variant_override: null
archetype: list_screen

feature: offlineSync
state: partial_failure
state_visibility: content

project_id: '10780096558615730514'
design_system_id: '9551377288795375599'

generated_by: stitch-prompt-build.ts v2.1.0
prompt_template_version: stitch-per-state-v3.1.0
craft_rules_version: v1.2.0
polished_by: claude-in-session (Step 2 POLISH, source = screens/offlineSync/preview/partial_failure.html)
---

# offlineSync — partial_failure state

> Polished from screens/offlineSync/ui.yaml + the approved preview tier.
> Stitch DesignSystem: 9551377288795375599

↓↓↓ MOCKUP PROMPT

Design the partial failure state of the Offline sync screen for **Mifos X Field Officer**, a microfinance field-officer app that keeps centres, groups and clients on the phone so the officer can work where there is no signal. Material 3 light theme, 412×915dp phone, the design system's own type scale (do not change the font).

Palette: background #FAFAFB, surface #FFFFFF, onSurface #0F172A, onSurfaceVariant #475569, primary #4338CA, onPrimary #FFFFFF, primaryContainer #E0E7FF, secondary #059669, secondaryContainer #D1FAE5, error #DC2626, errorContainer #FFE4E1, onErrorContainer #9F1239, outline #94A3B8, outlineVariant #CBD5E1.

Shell: this is a Settings sub-screen. Top app bar with a back arrow and the title only. NO bottom navigation bar, NO drawer. One extended FAB.

**Component 1 - Top App Bar** (64dp tall, background #FAFAFB): back arrow, title "Offline sync" semibold title-large #0F172A.

**Component 2 - Summary Card** (full width minus 16dp insets, 16dp radius, white, 1dp #CBD5E1 border, 16dp padding): chips "Online" (#D1FAE5) and "3 failed" (#FFE4E1, #9F1239 text, error icon). Three level tiles: "2" Centres, "5" Groups, "43" Clients. Caption "Last synced 4 min ago, Manual". Full-width 48dp pill button "Sync now" #4338CA.

**Component 3 - Result Card** (same width, 16dp radius, 1dp #FECDD3 border, 40dp icon tile in the header, 40dp tall pill button in the footer): a #FFE4E1 header band with a white icon tile holding a #9F1239 error icon, title "Done, 1,037 synced, 3 failed" semibold #9F1239, subtitle "Everything else opens offline". Three divided failure rows, each with a leading #DC2626 icon, a bold what-failed line and the server message with a bold reason prefix in #9F1239. Row one, lock icon: Loan 000001475, documents, with the message "Access denied (403): User has no authority to: READ_DOCUMENT". Row two, table icon: FOTest Asha, DATOS_CONTACTO, with the message "Access denied (403): Not authorised to read datatable: DATOS_CONTACTO". Row three, document icon: Rosa Elena Cruz, INE frente.jpg, with the message "Not found (404): Document with identifier 88 does not exist". A footer row shows "4 min ago, took 2 min 51 s" in #475569 and the pill button "Retry failed" filled #9F1239 with a replay icon.

**Component 4 - On this device Card** (list_screen archetype, rows with 40dp #F3E8FF avatars): heading, Chip Row "Centres 2", "Groups 5" selected, "Clients 43"; the Groups and Clients chips each carry a small #DC2626 dot. Group rows: Girasoles, 9 clients and 25 accounts, via Centro Arin, status 2 failed, synced 4 min ago in #DC2626; MARIPOSAS MONARCAS, 12 clients and 27 accounts, via Centro Arin, status 1 failed in #DC2626; Las Margaritas, via Centro Arin, status Synced 4 min ago in #059669; Las Palomas, 6 clients and 13 accounts, via Arin Savings, status Synced 4 min ago in #059669. Each row has a trailing expand chevron.

**Component 5 - Sync Card**: segmented control "Manual" selected, "Automatic"; info line "Your records sync only when you tap Sync now. Do it before you head out."

**Component 6 - Extended FAB** (56dp, 16dp radius, #E0E7FF, bottom-right): plus icon and "Add records".

DO NOT invent failure reasons beyond the three listed, and keep each server message verbatim. DO NOT show uploads, payloads, queues or pending transactions; this screen only downloads. DO NOT render a bottom navigation bar or a hero banner. DO NOT use em-dash characters anywhere.

Honest but not alarming: the rose #FFE4E1 result card owns the problem with the server's own words and one clear retry, while the rest of the screen stays calm white to show the bulk of the data is safely on the phone.

↑↑↑ MOCKUP PROMPT
