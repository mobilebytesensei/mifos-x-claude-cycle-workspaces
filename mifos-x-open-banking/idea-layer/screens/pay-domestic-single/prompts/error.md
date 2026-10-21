---
ui_yaml_sha: auto
design_md_hash: auto
feature: pay-domestic-single
state: error
state_visibility: error
archetype: screen
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-single — error state

> Source: screens/pay-domestic-single/ui.yaml + demo-data.yaml · design-system/DESIGN.md
> DO NOT redeclare colors, fonts, or spacing — they live in the uploaded design system.
> DO NOT invent navigation, tabs, or screens beyond the app-shell (Home, Accounts, Pay, More).

↓↓↓ MOCKUP PROMPT

> Only the CTA buttons inside the error_panel are tappable. Step indicator, title and error
> message text are NOT interactive.

## Archetype: screen

## State

`error` — after a failed call during consent staging or submission. Only step_indicator and
error_panel render; the panel REPLACES the form content.

Primary render: the **network** scenario — staging returned an IOException.

## Layout

Scrollable column, 16dp screen_padding, start-aligned.

## Composition (top → bottom)

1. **TopAppBar** — title "Pay someone", `titleLarge` `onSurface`, back icon `arrow_back`.

2. **StepIndicator** — 48dp row. Step 4 was active when the error occurred; all labels
   `onSurfaceVariant` at full opacity.

3. **error_panel** — full-width card (minus 16dp each side), vertical auto-layout, 16dp
   padding, 12dp gap, fill `errorContainer`, radius `radius/md`:

   - **Icon** `error_outline`, 32dp `onErrorContainer`.
   - **Title** "Payment could not be completed" — `titleMedium` `onErrorContainer`.
   - **Message** — `bodyMedium` `onErrorContainer`. The panel iterates the WHOLE Errors[]
     array, one paragraph per entry. For this render:
     "No network connection. Nothing was sent — check your connection and try again."
   - **Action row** — FilledButton "Try again": fill `primary`, label `onPrimary`,
     `labelLarge`, `radius/full`, triggers RetrySubmit. No secondary CTA.

   **Variant frames** — same panel structure, copy per ErrorCode:

   U009 consent not authorised
   - "This payment was not authorised with your bank. Authorise again to continue."
   - CTA: "Authorise again"

   U019 signature missing (not user-recoverable)
   - "This payment could not be signed, so your bank rejected it. Nothing has been sent.
     Please report reference %1$s."
   - No Retry CTA.
     <!-- COPY GAP: no catalogue key for the support/reference CTA label. -->

   U027 unsupported debtor scheme
     <!-- COPY GAP: error.payment.* has no U027 counterpart and no "return to Step 1" CTA
          label. Do NOT render invented wording. -->

   Two simultaneous Errors[] entries (R13-10 / R9-11 class)
   - BOTH rendered as separate `bodyMedium` paragraphs — never Errors[0] alone.

4. **BottomNav** — 80dp `surfaceContainer`, Pay tab active (`primary`).

**Copy selection rule**: copy comes from `ErrorCode` + `Path` (case-insensitive), never from
the API `Message`. Never display the raw `Message`.

## Design tokens (by name only)

Colors `surface` `onSurface` `onSurfaceVariant` `primary` `onPrimary` `errorContainer`
`onErrorContainer` `surfaceContainer` · Type `titleLarge` `titleMedium` `bodyMedium`
`labelLarge` · Radius `radius/md` `radius/full` · Icons `error_outline` `arrow_back`.

## Self-Validation Checklist

- [ ] Only step_indicator and error_panel render — no form fields, list, review or confirm.
- [ ] Panel uses `errorContainer` fill, `onErrorContainer` text and icon.
- [ ] Primary render is the network scenario with the "Try again" CTA.
- [ ] Message text is catalogue copy, not the raw API Message string.
- [ ] Multi-error variant shows BOTH entries separately.
- [ ] Tokens by name — no hex literals.

If any checkpoint fails → fix the output before returning.

↑↑↑ MOCKUP PROMPT
