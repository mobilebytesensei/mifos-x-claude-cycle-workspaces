---
ui_yaml_sha: d507f376f860c014e7068f2bf3fd3fb66cac58d618ddf536c9e4dc0c77b505f4
design_md_hash: c1e7dbe50f7725a08e0369f4cb0659b8c1e56ac645d128a4c90c66b8618666ef
app_shell_hash: 89077f8f960080911cf9c2b934ba619c11591fcb24da55987a5a1bb79f349739
design_read_hash: 
content_hash: b859653baa8796690a7b88263699f9020452ca64bba20a36a3cc814fa764f0d1

design_read_aesthetic: taste-default
design_read_dials: {variance: 7, motion: 6, density: 4}
aesthetic_variant_override: null
archetype: detail_screen

feature: profile
state: offline
state_visibility: offline

project_id: '10780096558615730514'
design_system_id: '9551377288795375599'

generated_by: stitch-prompt-build.ts v2.1.0
prompt_template_version: stitch-per-state-v3.1.0
craft_rules_version: v1.2.0
polished_by: claude-in-session (Step 2 POLISH, source = screens/profile/preview/offline.html)
---

# profile — offline state

> Polished from screens/profile/ui.yaml + the approved preview tier.
> Stitch DesignSystem: 9551377288795375599

↓↓↓ MOCKUP PROMPT

Design the offline state of the Profile screen for **Mifos X Field Officer**, a microfinance field-officer app used where there is often no signal. The whole account still shows from what was saved at sign-in; only Change password needs a connection. Material 3 light theme, 412×915dp phone, the design system's own type scale (do not change the font).

Palette: background #FAFAFB, surface #FFFFFF, onSurface #0F172A, onSurfaceVariant #475569, primary #4338CA, primaryContainer #E0E7FF, tertiaryContainer #FEF3C7, onTertiaryContainer #78350F, error #DC2626, outline #94A3B8, outlineVariant #CBD5E1.

Shell: a detail screen opened from the Home avatar. Top app bar with a back arrow and the title only. NO bottom navigation bar, NO drawer, NO FAB.

**Component 1 - Top App Bar** (64dp tall, background #FAFAFB): back arrow, title "Profile" semibold title-large #0F172A.

**Component 2 - Offline Banner** (full width minus 16dp insets, 12dp radius, tertiaryContainer #FEF3C7, onTertiaryContainer #78350F, 12dp by 16dp padding): cloud-off icon and "You're offline. This is the account saved when you signed in."

**Component 3 - Identity Header** (no card, left aligned, 16dp gap): a 72dp circle avatar on primaryContainer #E0E7FF with "IZ" bold #4338CA; the name "Irving Zepeda" semibold headline-small, then the username "fieldofficer" and the email "oficial.campo@gmail.com" in body-medium #475569.

**Component 4 - Office Card** (16dp radius, white, 1dp #CBD5E1 border, 56dp rows with 1dp #E2E8F0 dividers): a row with label "Office", value "CENTRAL"; a row with label "What Home shows", value "Office: CENTRAL", and its supporting line.

**Component 5 - Roles** (section heading "Roles", same card style): one outlined 32dp chip with the role "OFICIAL DE CAMPO".

**Component 6 - Signed In Card** (section heading "Signed in to", same card style): the instance "Mifos field officer gateway" with NO Live pill; a row with label "Server", value "https://apis.mifos.community/1.0/field/v1/"; a row with label "Tenant", value "mifos-bank-1"; the link "Server settings" #4338CA.

**Component 7 - Account Card** (same card style): a row "Change password" DISABLED, icon and label in outline #94A3B8 with the supporting line "Connect to the internet to change your password." and no chevron; a row "Sign out" in error #DC2626, still enabled.

DO NOT show an error or a retry; being offline is a normal field condition. DO NOT render a bottom navigation bar or a FAB. DO NOT use em-dash characters anywhere.

Steady: one amber #FEF3C7 banner states the condition, and the account below is complete and calm.

↑↑↑ MOCKUP PROMPT
