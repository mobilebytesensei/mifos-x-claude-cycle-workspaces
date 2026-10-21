---
feature: pay-domestic-standing-order
state: error
generated_by: idea-feature-export
design_system: Open Banking — Trust Blue v1.4.0
---

# pay-domestic-standing-order — error state

> Tokens by NAME only. No hex, no inline sizes.

<!-- COPY PROVENANCE: ui.yaml declares no error_panel of its own — this screen renders the
     shared PISP panel, so the title is strings.payment.error_title and three variants map
     exactly onto error.payment.* and use it VERBATIM. The rest are marked UNSOURCED / COPY GAP
     and kept only as intent. -->

↓↓↓ MOCKUP PROMPT

Render FIVE sub-frames, one per error class. Shared layout in all frames:
- Top app bar: `arrow_back`; "Standing order" (`titleLarge`, `color/onSurface`)
- Step indicator [step_indicator] always visible
- Bottom nav: Home · Accounts · Pay (active) · More

## Shared Error Layout

```
ErrorContent (Fill, center, padding spacing/xl, gap spacing/md, Auto Layout Vertical)
  ErrorIcon (icon/xl, color/error)
  Title (titleMedium, color/onSurface, center): "Payment could not be completed"
  Message (bodyMedium, color/onSurfaceVariant, center, max-width 280dp)
  [ErrorEntries — Variant 4 only]
  [RetryButton — retryable only]
  GoBackButton text: "Go back" (labelLarge, color/primary)  <!-- UNSOURCED: no payments key -->
```

## Error Variants

All five share the layout above and the same title. Render icon, title, then the message.

1. **NetworkError** · `cloud_off` · retry
   "No network connection. Nothing was sent — check your connection and try again."
   — error.payment.network_error VERBATIM
2. **InvalidMandateDates U003** · `event_busy` · retry
   "The end date must be after the first payment date, within 12 months, and not today or tomorrow."
   <!-- UNSOURCED: no key. Kept because U003 returns all three rules in one message. -->
3. **ConsentNotAuthorised U009** · `lock_open` · retry
   "This payment was not authorised with your bank. Authorise again to continue."
   — error.payment.consent_not_authorised VERBATIM
4. **FieldNotExpected U005** · `error_outline` · no retry
   Message slot EMPTY. <!-- COPY GAP: no key; the panel shows the Errors[] chips only. -->
5. **SignatureMissing U019** · `security` · no retry
   "This payment could not be signed, so your bank rejected it. Nothing has been sent. Please report reference %1$s."
   — error.payment.signature_missing VERBATIM (%1$s = the x-fapi-interaction-id)

**RetryButton** (Variants 1, 2, 3): `color/primary`, `radius/full`, 56dp; label `labelLarge`,
`color/onPrimary`, text "Try again" — payment.retry VERBATIM. Do NOT relabel it per variant.

## Variant 4 — Multi-Error Surface

Two stacked error entry chips in place of the message (renders the full `Errors[]` array):
- Chip 1: `color/errorContainer`, `radius/sm`, icon `error` (`icon/sm`); "U005 · Data.Initiation.InstructedAmount" (`labelSmall`, `color/onErrorContainer`)
- Chip 2: same; "U004 · Data.Initiation.FirstPaymentAmount"

## Token Usage

- Screen bg `color/surface` · error icon `color/error` · message `color/onSurfaceVariant`
- Chips `color/errorContainer` / `color/onErrorContainer`
- Retry `color/primary` / `color/onPrimary` · Go back `color/primary`

## Rules

1. Render full `Errors[]` — never only `Errors[0]`.
2. Copy keyed off `ErrorCode` + `Path`, never `Message` (U003's message carries 3 rules).
3. No blame language. 4. `confirm_button` is never `color/error` on any rail.

## Self-Validation

- [ ] Five sub-frames rendered; step indicator visible in all
- [ ] Every variant carries the same title; nothing in a slot marked COPY GAP or UNSOURCED
- [ ] RetryButton only on Variants 1, 2, 3, always labelled "Try again"
- [ ] Variant 4 shows two error entry chips and no message text
- [ ] No blame language; all tokens by NAME; no hex

↑↑↑ MOCKUP PROMPT
