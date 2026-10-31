---
ui_yaml_sha: d507f376f860c014e7068f2bf3fd3fb66cac58d618ddf536c9e4dc0c77b505f4
design_md_hash: c1e7dbe50f7725a08e0369f4cb0659b8c1e56ac645d128a4c90c66b8618666ef
app_shell_hash: 89077f8f960080911cf9c2b934ba619c11591fcb24da55987a5a1bb79f349739
design_read_hash: 
content_hash: a0d5fce2b89e0f34ed527112fa7e9d8c82ccf130fd1ce756647f9de87983293c

design_read_aesthetic: taste-default
design_read_dials: {variance: 7, motion: 6, density: 4}
aesthetic_variant_override: null
archetype: skeleton_screen

feature: profile
state: loading
state_visibility: loading

project_id: '10780096558615730514'
design_system_id: '9551377288795375599'

generated_by: stitch-prompt-build.ts v2.1.0
prompt_template_version: stitch-per-state-v3.1.0
craft_rules_version: v1.2.0
polished_by: claude-in-session (Step 2 POLISH, source = screens/profile/preview/loading.html; v2 after the first render added an invented footer)
---

# profile — loading state

> Polished from screens/profile/ui.yaml + the approved preview tier.
> Stitch DesignSystem: 9551377288795375599

↓↓↓ MOCKUP PROMPT

Design the loading state of the Profile screen for **Mifos X Field Officer**, a microfinance field-officer app. The account saved at sign-in shows at once; only the officer's full name and email are still arriving from the server. Material 3 light theme, 412×915dp phone, the design system's own type scale (do not change the font).

Palette: background #FAFAFB, surface #FFFFFF, onSurface #0F172A, onSurfaceVariant #475569, primary #4338CA, primaryContainer #E0E7FF, surfaceVariant #E2E8F0, outlineVariant #CBD5E1.

Shell: a detail screen opened from the Home avatar. Top app bar with a back arrow and the title only. NO bottom navigation bar, NO drawer, NO FAB.

**Component 1 - Top App Bar** (64dp tall, background #FAFAFB): back arrow, title "Profile" semibold title-large #0F172A.

**Component 2 - Identity Header** (no card, left aligned, 16dp gap, shimmer bars with 6dp rounded ends in a soft #E2E8F0 to #FAFAFB gradient): a 72dp circle avatar on primaryContainer #E0E7FF with the single letter "F" bold #4338CA. Beside it a 28dp tall shimmer bar about 70% wide where the name will be, then the username "fieldofficer" in body-medium #475569, then a thinner shimmer bar about 55% wide.

**Component 3 - Office Card** (16dp radius, white, 1dp #CBD5E1 border, 56dp rows with 1dp #E2E8F0 dividers): a row with an apartment icon, label "Office", value "CENTRAL"; a row with an insights icon, label "What Home shows" and a short shimmer bar in place of its value.

**Component 4 - Roles** (section heading "Roles" #475569 above a card of the same style): one outlined 32dp chip with an 8dp radius, a badge icon #4338CA and the role "OFICIAL DE CAMPO".

**Component 5 - Signed In Card** (section heading "Signed in to", same card style): a row with the instance "Mifos field officer gateway"; a row with label "Server", value "https://apis.mifos.community/1.0/field/v1/"; a row with label "Tenant", value "mifos-bank-1".

Nothing below the Signed In Card: leave calm empty background. DO NOT add a footer, a caption, a security note or any text not listed. DO NOT show a full-screen spinner or a progress bar; the screen is usable while the name loads. DO NOT render a bottom navigation bar or a FAB. DO NOT use em-dash characters anywhere.

Already there: the officer recognises their own account the moment the screen opens on the indigo #4338CA initial, with only two quiet bars still filling in.

↑↑↑ MOCKUP PROMPT
