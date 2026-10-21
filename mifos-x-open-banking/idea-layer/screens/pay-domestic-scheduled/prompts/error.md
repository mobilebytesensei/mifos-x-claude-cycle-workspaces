---
feature: pay-domestic-scheduled
state: error
archetype: error_state
design_read_aesthetic: minimalist-ui
design_read_dials: {variance: 3, motion: 2, density: 5}
generated_by: idea-feature-export v1.0.0
prompt_template_version: stitch-per-state-v3.0.0
---

# pay-domestic-scheduled — error state

> Auto-generated from screens/pay-domestic-scheduled/ui.yaml
> DO NOT redeclare colors / fonts / spacing — they live in DESIGN.md.

↓↓↓ MOCKUP PROMPT

> DO NOT invent navigation, tabs or screens beyond the app-shell (Home, Accounts, Pay, More)
> plus the composition below.
> Only elements that navigate or act may look tappable. Titles, headings, icons, badges and
> static labels are NOT interactive.

## Archetype: error_state

## Layout

Scrollable column, default padding; stepper top-aligned, error block centred in the remaining
area. Single-column, mobile-first.

## Composition (top → bottom)

1. **top_app_bar** — back icon left (active — the PSU can go back and fix inputs), title
   "Pay on a date".
2. **stepper** (#step_indicator) — 5 steps; the step where the error occurred is active
   (primary chip), completed steps primaryContainer.
3. **error_panel** (#error_panel) — centred: icon + title + body + optional retry CTA.

## State-specific behavior

- Form content (account list, date picker, review card, confirm button) is NOT visible; the
  error panel replaces it. The stepper persists, showing where the error occurred.
- ALL entries in the Errors[] array are displayed — it can hold two at once. Render as a
  stacked block, keyed on ErrorCode + Path (case-insensitive). NEVER key off Message: U004 has
  four observed wordings, including a bare "Field is missing".
- Render the network variant as the representative state.

## Error copy

Panel title (all variants): "Payment could not be completed"

- **network** — icon `wifi_off` / `signal_wifi_off` (48dp, error colour). Body:
  "No network connection. Nothing was sent — check your connection and try again."
  CTA: "Try again" (filled, primary, radius.full) → RetrySubmit.
- **ConsentNotAuthorised** — body: "This payment was not authorised with your bank. Authorise
  again to continue." CTA: "Authorise again".
- **SignatureMissing** — body: "This payment could not be signed, so your bank rejected it.
  Nothing has been sent. Please report reference %1$s." No retry CTA.
- **DateInPast** — no retry; returns to the Date step.
  <!-- COPY GAP: no catalogue key for a past-execution-date rejection. Do NOT invent wording. -->
- **DateOutOfRange** — no retry; returns to the Date step.
  <!-- COPY GAP: no catalogue key for an execution date beyond T+365. Do NOT invent wording. -->

## Components

- **error_panel**: icon `error_outline` (48dp, error colour) · title (headlineSmall, onSurface,
  centred) · body (bodyMedium, onSurfaceVariant, centred, max-width 300dp) · RetryButton when
  retryable (filled, primary, radius.full, labelLarge onPrimary)

## Shell

Home → home · Accounts → accounts · Pay → payments · More → settings.

## Tokens

Colors error / surface / onSurface / onSurfaceVariant / primary / onPrimary · Type titleLarge /
headlineSmall / bodyMedium / labelLarge / labelSmall · Spacing gap.md / gap.lg. All by name.

## Self-Validation Checklist

- [ ] Only the error state — no form fields, date picker or review card.
- [ ] Title and body are the catalogue copy above, not a generic "Error occurred".
- [ ] Retry CTA reads "Try again" — not "Retry" or "Submit".
- [ ] Tokens by name; error icon in error colour, retry in primary. No hex codes.
- [ ] The 5-step stepper is still visible above the error panel.
- [ ] TopAppBar + BottomNav present and consistent with the shell.
- [ ] No text rendered into a slot marked COPY GAP.

Return ONLY when all checkpoints pass.

↑↑↑ MOCKUP PROMPT
