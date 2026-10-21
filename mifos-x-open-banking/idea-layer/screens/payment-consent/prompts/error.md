# payment-consent · state: error

> payment-consent · error · headless/transitional · Open Banking — Trust Blue (M3, seed #266489)
> Every quoted string is VERBATIM from `_strings/strings.yaml`. Do not paraphrase or invent.
> SCA return leg: wrong copy tells a PSU to retry what cannot be retried, or implies money moved.

---

## Layout — one shape for all six error types

**Shell**: `TopAppBar` titled "Authorising payment", no bottom navigation, no leading icon.
**Content**: vertically centred column, padding `spacing.md`, gap `spacing.lg`.

1. **Icon** — `error_outline`, `icon.xl` (48dp), `colors.error`. Contrast 6.1:1, AA pass.
2. **Title** — "Authorisation could not be completed" (`headlineSmall`, `colors.on_surface`,
   centred). ONE title key covers every error type; per-type titles are UNSOURCED.
3. **Body** — `{error.message}` (`bodyMedium`, `colors.on_surface_variant`, centred, max 280dp).
4. **`FilledButton` (`restart_authorisation_button`)** — conditional. "Start again",
   `labelLarge`, `colors.primary`/`colors.on_primary`, `radius.full`, min 48dp, padding
   horizontal `spacing.xl`. a11y: "Start the payment authorisation again".
5. **`TextButton` (`abandon_button`)** — always visible. "Discard payment", `labelLarge`,
   `colors.on_surface_variant`, min 48dp, padding horizontal `spacing.lg`.
   a11y: "Discard this payment. No money will be sent."

---

## The six error types

| Type | Cause | Body copy (verbatim) | Restart CTA |
|---|---|---|:---:|
| `StateMismatch` | returned `state` ≠ pending authorisation | "This authorisation could not be verified, so the payment was stopped. Please start again." | Hidden |
| `NoPendingAuthorisation` | app restarted mid-authorisation | "There's no payment waiting to be authorised. Please start again." | Hidden |
| `CodeExpired` | `400 invalid_grant` | "The authorisation took too long and expired. No money was sent." | Shown |
| `ConsentRejected` | `Data.Status == "RJCT"` | "You declined this payment at your bank. Nothing has been sent." | Hidden |
| `AuthorisationTimedOut` | still `AWAU` past the 180 000ms deadline | "Your bank hasn't confirmed this payment yet. You can check again or start over." | Shown |
| `NetworkError` | IOException / timeout | "No network connection. The payment was not authorised." | Shown |

`abandon_button` is shown for all six.

---

## Copy rules

- Every body states plainly that nothing was sent, or that the payment was stopped. Do not drop
  or soften that clause — it is the whole point of the screen.
- No blame. "This authorisation could not be verified", not "your security check failed".
- `StateMismatch` does not explain the attack vector.
- `CodeExpired` and `ConsentRejected` are UNRECOVERABLE against the existing consent. The
  restart CTA offered on `CodeExpired` stages a NEW consent — it never re-authorises the old
  one. Copy must never suggest re-trying this payment; "Start again" is the accurate framing.

Body keys: `error.payment_consent.{state_mismatch, no_pending, code_expired, rejected,
timed_out, network_error}`. Shell/CTA keys: `payment_consent.{screen_title, error_title,
restart, restart_a11y, abandon, abandon_a11y}` — values as quoted above.

Tokens: `colors.{surface, on_surface, on_surface_variant, error, primary, on_primary}` ·
`spacing.md/.lg/.xl` 16/24/32dp · `radius.full` · 48dp touch target · `icon.xl` 48dp.

---

## Restart semantics — load-bearing

"Start again" emits `PaymentConsentEvent.RestartAuthorisation` carrying **no `consentId`** by
design. The originating type screen MUST stage a FRESH consent, build a new `oauth2/authorize`
URL from the NEW ConsentId, and relaunch. It MUST NOT reuse the handed `consentId` — a consent
already at `AUTH` cannot be sent back through the authorise leg. The previous staged consent is
left to expire; no revocation call, since an unauthorised consent cannot be submitted against.

Both CTAs are events to the originating screen; there is no self-managed transition out of
`error`.
