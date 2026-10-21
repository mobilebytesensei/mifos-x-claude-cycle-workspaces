# Payment Status — Loading State Prompt

> Feature: payment-status · State: loading
> Design system: Open Banking — Trust Blue (Material 3, seed #266489)
> Input to Stitch run — component names and tokens by NAME, no inline sizes
> Every quoted string below is VERBATIM from `_strings/strings.yaml`. Do not paraphrase.

---

## Purpose

Shown while the ViewModel dispatches the first `GET /{familyResourcePath}/{paymentId}` call.
The PSU has just submitted a payment or instruction and is waiting for the tracker to resolve
its initial status. This is an ephemeral state — on fast connections it appears for under a second;
on the four deferred family first reads it can persist longer while the family resolver runs.

The loading screen must convey: something is happening, not that there is a problem. No error
chrome, no skeleton cards with slots that would imply a specific layout before the data arrives.

---

## Screen Shell

- Top app bar visible, leading: `back_button` (arrow_back icon, `icon_button` component)
- Title: "Payment status" resolved from `strings.payment_status.screen_title`
- Bottom navigation visible, Pay tab active
- No FAB

---

## Component Tree

**PaymentStatusLoadingScreen** (`detail_screen` archetype, `surface` background)

- `CircularProgressIndicator`
  - Colour: `color/primary`
  - Size: `icon/xl` (48dp)
  - Positioned: centred horizontally and vertically in the scrollable content zone
  - Accessibility: `strings.payment_status.loading_label` → "Loading payment" as contentDescription
  - Animation: standard M3 indeterminate circular — no custom easing, low-motion flag respected

No other components are visible in this state. No skeleton shimmer — the payment summary card
layout is not known until the API response resolves the family and initiation.

---

## Token References

| Role                  | Token                    |
|-----------------------|--------------------------|
| Screen background     | `color/surface`          |
| Progress indicator    | `color/primary`          |
| Top app bar container | `color/surface`          |
| Top app bar title     | `color/onSurface`        |
| Back button icon      | `color/onSurface`        |
| Bottom nav container  | `color/surfaceContainerLow` |
| Bottom nav active tab | `color/primary`          |

---

## Copy

| Key                                   | Value                        |
|---------------------------------------|------------------------------|
| `strings.payment_status.screen_title` | "Payment status"             |
| `strings.payment_status.loading_label`| "Loading payment"            |
| `strings.payment_status.back_label`   | "Back"                       |

---

## Accessibility

- `CircularProgressIndicator` has `semanticsRole = ProgressBar` and `contentDescription` bound to the loading_label string.
- Back button min touch target: `touch_targets.comfortable` (48dp).
- Screen announces "Loading payment" to screen readers on entry.
- `reduce_motion_supported: true` — the circular indicator switches to a non-animated progress bar when the system reduce-motion flag is set.

---

## Transition

When `payment_status_load` completes:
- **Success** → animate to `content` state; the status_chip and payment_summary card slide in from below with a 300ms `DecelerateInterpolator` enter.
- **Error** → fade to `error` state (150ms fade).

No intermediate skeleton — the transition is direct.
