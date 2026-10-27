---
ui_yaml_sha: d507f376f860c014e7068f2bf3fd3fb66cac58d618ddf536c9e4dc0c77b505f4
design_md_hash: c1e7dbe50f7725a08e0369f4cb0659b8c1e56ac645d128a4c90c66b8618666ef
app_shell_hash: 89077f8f960080911cf9c2b934ba619c11591fcb24da55987a5a1bb79f349739
design_read_hash: 
content_hash: 93feb4090c7c1ba5f53f26b12b5543fca51de8585d3a47aff2ac654a2cd3fd29

design_read_aesthetic: taste-default
design_read_dials: {variance: 7, motion: 6, density: 4}
aesthetic_variant_override: null
archetype: error_state

feature: profile
state: error
state_visibility: error

project_id: '10780096558615730514'
design_system_id: '9551377288795375599'

generated_by: stitch-prompt-build.ts v2.1.0
prompt_template_version: stitch-per-state-v3.1.0
craft_rules_version: v1.2.0
polished_by: claude-in-session (Step 2 POLISH, source = screens/profile/preview/error.html)
---

# profile — error state

> Polished from screens/profile/ui.yaml + the approved preview tier.
> Stitch DesignSystem: 9551377288795375599

↓↓↓ MOCKUP PROMPT

Design the error state of the Profile screen for **Mifos X Field Officer**, a microfinance field-officer app. The server could not return the officer's full name, so the screen keeps everything saved at sign-in and shows one inline error with a retry. This is NOT a full-screen error. Material 3 light theme, 412×915dp phone, the design system's own type scale (do not change the font).

Palette: background #FAFAFB, surface #FFFFFF, onSurface #0F172A, onSurfaceVariant #475569, primary #4338CA, primaryContainer #E0E7FF, secondaryContainer #D1FAE5, error #DC2626, errorContainer #FFE4E1, onErrorContainer #9F1239, outlineVariant #CBD5E1.

Shell: a detail screen opened from the Home avatar. Top app bar with a back arrow and the title only. NO bottom navigation bar, NO drawer, NO FAB.

**Component 1 - Top App Bar** (64dp tall, background #FAFAFB): back arrow, title "Profile" semibold title-large #0F172A.

**Component 2 - Identity Header** (no card, left aligned, 16dp gap): a 72dp circle avatar on primaryContainer #E0E7FF with the letter "F" bold #4338CA. Beside it the username "fieldofficer" semibold headline-small #0F172A and the office "CENTRAL" in body-medium #475569.

**Component 3 - Inline Error** (directly under the header, 12dp radius, errorContainer #FFE4E1, onErrorContainer #9F1239, 8dp by 16dp padding): an error icon, the message "Couldn't load your name from the server." with a smaller second line "Server error (500). Try again.", and a trailing text button "Retry" semibold #DC2626.

**Component 4 - Office Card** (16dp radius, white, 1dp #CBD5E1 border, 56dp rows with 1dp #E2E8F0 dividers): a row with label "Office", value "CENTRAL"; a row with label "What Home shows", value "Office: CENTRAL", and the supporting line "Your own portfolio when you're linked to a staff record, otherwise your whole office."

**Component 5 - Roles** (section heading "Roles", same card style): one outlined 32dp chip with an 8dp radius and the role "OFICIAL DE CAMPO".

**Component 6 - Signed In Card** (section heading "Signed in to", same card style): the instance "Mifos field officer gateway" with a 22dp "Live" pill (#D1FAE5); a row with label "Server", value "https://apis.mifos.community/1.0/field/v1/"; a row with label "Tenant", value "mifos-bank-1"; the link "Server settings" #4338CA with a chevron.

**Component 7 - Account Card** (same card style): a row "Change password" with a chevron; a row "Sign out" in error #DC2626.

DO NOT replace the screen with an empty error illustration; DO NOT hide the sections below the error. DO NOT render a bottom navigation bar or a FAB. DO NOT use em-dash characters anywhere.

Contained: one rose #DC2626 strip names the single thing that failed, and the rest of the account stays readable and usable around it.

↑↑↑ MOCKUP PROMPT
