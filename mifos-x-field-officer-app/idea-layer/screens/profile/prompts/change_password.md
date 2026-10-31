---
ui_yaml_sha: d507f376f860c014e7068f2bf3fd3fb66cac58d618ddf536c9e4dc0c77b505f4
design_md_hash: c1e7dbe50f7725a08e0369f4cb0659b8c1e56ac645d128a4c90c66b8618666ef
app_shell_hash: 89077f8f960080911cf9c2b934ba619c11591fcb24da55987a5a1bb79f349739
design_read_hash: 
content_hash: 6bb2ca2f92f275b1f9f576ef634cbb8944fa491ba947d237755a37d60560c896

design_read_aesthetic: taste-default
design_read_dials: {variance: 7, motion: 6, density: 4}
aesthetic_variant_override: null
archetype: detail_screen

feature: profile
state: change_password
state_visibility: change_password

project_id: '10780096558615730514'
design_system_id: '9551377288795375599'

generated_by: stitch-prompt-build.ts v2.1.0
prompt_template_version: stitch-per-state-v3.1.0
craft_rules_version: v1.2.0
polished_by: claude-in-session (Step 2 POLISH, source = screens/profile/preview/change_password.html; v2 after the first render invented an ID, a session chip and an assignment card)
---

# profile — change_password state

> Polished from screens/profile/ui.yaml + the approved preview tier.
> Stitch DesignSystem: 9551377288795375599

↓↓↓ MOCKUP PROMPT

Design the change_password state of the Profile screen for **Mifos X Field Officer**, a microfinance field-officer app. A bottom sheet is open over the Profile screen; the officer has typed two different passwords, so the second field shows the mismatch and Save is disabled. Material 3 light theme, 412×915dp phone, the design system's own type scale (do not change the font).

Palette: background #FAFAFB, surface #FFFFFF, onSurface #0F172A, onSurfaceVariant #475569, primary #4338CA, onPrimary #FFFFFF, primaryContainer #E0E7FF, surfaceVariant #E2E8F0, error #DC2626, outline #94A3B8, outlineVariant #CBD5E1.

Shell: the Profile detail screen sits underneath, dimmed. Top app bar with a back arrow and the title "Profile" only. NO status bar mock, NO bottom navigation bar, NO drawer, NO FAB.

**Component 1 - Dimmed Profile** (behind a 42% #0F172A scrim, left aligned, top half of the screen only): the top app bar with "Profile", then a 72dp "IZ" avatar on #E0E7FF beside the name "Irving Zepeda" and the username "fieldofficer". Nothing else behind the scrim: no ID number, no session chip, no role line, no cards.

**Component 2 - Bottom Sheet** (white, 28dp top corners, 24dp side padding, 16dp gaps, a 32dp by 4dp #CBD5E1 drag handle on top): title "Change password" semibold headline-small #0F172A, then a body-medium #475569 line "You stay signed in on this device after the change."

**Component 3 - New Password Field** (56dp outlined text field, 8dp radius, 1dp #94A3B8 outline): floating label "New password", masked dots, trailing eye icon. Under it a body-small #475569 hint "12 to 50 characters, with upper and lower case, a number and a symbol".

**Component 4 - Repeat Password Field** (same field with a 2dp error #DC2626 outline and an error-coloured label): floating label "Repeat new password", masked dots, trailing eye icon. Under it an error icon and "Passwords do not match" in body-small #DC2626.

**Component 5 - Sheet Actions** (right aligned, 8dp gap, 40dp pills): text button "Cancel" #4338CA, and a disabled filled button "Save password" (#E2E8F0 fill, #94A3B8 label).

DO NOT invent staff IDs, employee numbers, session or status chips, branch, centre or portfolio details, or any card behind the sheet. DO NOT show a current-password field, a strength meter, or any field not listed. DO NOT render a bottom navigation bar or a FAB. DO NOT use em-dash characters anywhere.

Precise: the one red #DC2626 field says exactly what to fix, and the disabled Save makes it clear nothing has been sent yet.

↑↑↑ MOCKUP PROMPT
