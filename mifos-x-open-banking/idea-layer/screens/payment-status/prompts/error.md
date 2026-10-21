# Payment Status — Error State Prompt

> Feature: payment-status · State: error
> Design system: Open Banking — Trust Blue (Material 3, seed #266489)
> Every quoted string below is VERBATIM from `_strings/strings.yaml`. Do not paraphrase.

## Shell

Top app bar: leading `back_button` (arrow_back), title "Payment status". Bottom nav visible,
Pay tab active. Error content centred vertically in the scrollable zone.

## Layout

```
error_state (Fill, Auto Layout Vertical, centred, padding=spacing/md, gap=spacing/md)
  ├─ Icon: error_outline (icon/xl = 48dp, color/error)
  ├─ Title: "Could not load payment" (headlineSmall, color/onSurface, centre-aligned)
  ├─ Message: {error.message} (bodyMedium, color/onSurfaceVariant, centre-aligned)
  └─ retry_button (Hug × 48dp, filled, radius/full, color/primary / color/onPrimary)
        Label: "Try again"
        Visible only when error.type is retryable
```

`ui.yaml` binds ONE title key for every error type. Per-type titles ("Payment not found",
"Session expired", "Connection unavailable", "Something went wrong") are **UNSOURCED — no key
exists for them.** Render the single title above on every sub-variant.

## Error types — only the message varies

| Type | Trigger | Message (verbatim) | retry_button |
|---|---|---|---|
| `PaymentNotFound` | 404 / 400 U011 | "This payment could not be found." | hidden — the resource does not exist |
| `TokenExpired` | 401 | "Your session has expired. Sign in again to view this payment." | shown |
| `ConsentRevoked` | 403 | "Permission for this payment was withdrawn. Payments already completed are not affected." | hidden — a retry returns another 403 |
| `NetworkError` | IOException / timeout | "No network connection. Check your connection and try again." | shown |

Copy rule for `ConsentRevoked`: the clause "Payments already completed are not affected" is
load-bearing. A revoked consent does not reverse a payment that settled before revocation.
Do not shorten or reword it.

## Tokens

Error icon `color/error` · title `color/onSurface` · message `color/onSurfaceVariant` ·
retry container `color/primary`, retry label `color/onPrimary` · background `color/surface` ·
button radius `radius/full` · touch target 48dp.

## Accessibility

- `error_state` announces its title to screen readers on render.
- `retry_button` contentDescription: "Retry loading this payment"
- `back_button` is always reachable as the exit from every sub-variant.

## Copy index — verbatim from `_strings/strings.yaml`

| Key | Value |
|---|---|
| `payment_status.error_title` | "Could not load payment" |
| `payment_status.retry` | "Try again" |
| `payment_status.retry_a11y` | "Retry loading this payment" |
| `error.payment_status.not_found` | "This payment could not be found." |
| `error.payment_status.token_expired` | "Your session has expired. Sign in again to view this payment." |
| `error.payment_status.consent_revoked` | "Permission for this payment was withdrawn. Payments already completed are not affected." |
| `error.payment_status.network_error` | "No network connection. Check your connection and try again." |

## Removed — unsourced VRP sub-variant

An earlier version of this prompt specified a `MandateRevoked` / VRP sub-variant with a
"Mandate cancelled" chip, a "Set up a new mandate" CTA and a `strings.error.vrp.revoked` key.
`payment-status` declares exactly four error types and none is `MandateRevoked`; none of that
copy exists in `_strings/strings.yaml`. It has been removed rather than rendered as finished
copy. If the VRP rail needs this treatment, add the keys first.

## Retry safety

Every error here comes from a GET, so retrying has no side effects. The retry_button is hidden
only where a retry would always fail (404 resource absent, 403 consent terminated) — not
because retrying would be harmful.
