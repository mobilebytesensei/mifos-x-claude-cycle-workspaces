---
ui_yaml_sha: d507f376f860c014e7068f2bf3fd3fb66cac58d618ddf536c9e4dc0c77b505f4
design_md_hash: c1e7dbe50f7725a08e0369f4cb0659b8c1e56ac645d128a4c90c66b8618666ef
app_shell_hash: 89077f8f960080911cf9c2b934ba619c11591fcb24da55987a5a1bb79f349739
design_read_hash: 
content_hash: bf66fa83eac05d3dda59a041f7392a08fc8e88af66b4722e7839573b5423d41c

design_read_aesthetic: taste-default
design_read_dials: {variance: 7, motion: 6, density: 4}
aesthetic_variant_override: null
archetype: detail_screen

feature: profile
state: content
state_visibility: content

project_id: '10780096558615730514'
design_system_id: '9551377288795375599'

generated_by: stitch-prompt-build.ts v2.1.0
prompt_template_version: stitch-per-state-v3.1.0
craft_rules_version: v1.2.0
polished_by: claude-in-session (Step 2 POLISH, source = screens/profile/preview/content.html)
---

# profile — content state

> Polished from screens/profile/ui.yaml + the approved preview tier.
> Stitch DesignSystem: 9551377288795375599

↓↓↓ MOCKUP PROMPT

Design the content state of the Profile screen for **Mifos X Field Officer**, a microfinance field-officer app. It shows the signed-in officer who they are, which office their Home figures cover, and which server they are signed in to. Material 3 light theme, 412×915dp phone, the design system's own type scale (do not change the font).

Palette: background #FAFAFB, surface #FFFFFF, onSurface #0F172A, onSurfaceVariant #475569, primary #4338CA, primaryContainer #E0E7FF, secondary #059669, secondaryContainer #D1FAE5, error #DC2626, outline #94A3B8, outlineVariant #CBD5E1.

Shell: a detail screen opened from the Home avatar. Top app bar with a back arrow and the title only. NO bottom navigation bar, NO drawer, NO FAB.

**Component 1 - Top App Bar** (64dp tall, background #FAFAFB): back arrow, title "Profile" semibold title-large #0F172A.

**Component 2 - Identity Header** (no card, left aligned, 16dp gap): a 72dp circle avatar on primaryContainer #E0E7FF with the initials "IZ" bold #4338CA and a 4dp white ring. Beside it the full name "Irving Zepeda" semibold headline-small #0F172A, then the username "fieldofficer" and the email "oficial.campo@gmail.com" in body-medium #475569 on their own lines.

**Component 3 - Office Card** (16dp radius, white, 1dp #CBD5E1 border, 56dp rows with 1dp #E2E8F0 dividers): a row with an apartment icon, label "Office", value "CENTRAL". A row with an insights icon, label "What Home shows", value "Office: CENTRAL", and a supporting line "Your own portfolio when you're linked to a staff record, otherwise your whole office."

**Component 4 - Roles** (small section heading "Roles" #475569 above a card of the same style): one outlined 32dp chip with an 8dp radius, a badge icon #4338CA and the role "OFICIAL DE CAMPO".

**Component 5 - Signed In Card** (section heading "Signed in to", same card style): a row with a dns icon, the instance "Mifos field officer gateway" and a small 22dp pill "Live" (#D1FAE5 fill, #064E3B text, green dot). A row with label "Server", value "https://apis.mifos.community/1.0/field/v1/". A row with label "Tenant", value "mifos-bank-1". A last row with the link "Server settings" semibold #4338CA, a tune icon and a trailing chevron.

**Component 6 - Account Card** (same card style): a row "Change password" with a lock-reset icon and a trailing chevron; a row "Sign out" with a logout icon, both icon and label in error #DC2626.

DO NOT add a bottom navigation bar, a drawer, a FAB, an edit-profile button, a photo upload, statistics, badges or sections not listed. DO NOT use em-dash characters anywhere.

Calm and certain: the indigo #4338CA initials and the name are the one bold moment, everything below reads like a quiet settings list, and Sign out is the only red on the page.

↑↑↑ MOCKUP PROMPT
