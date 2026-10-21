# payment-consent · state: exchanging

> Feature: payment-consent · State role: loading (step 2 of 3)
> Archetype: headless / transitional
> Design system: Open Banking — Trust Blue (Material 3, seed #266489)
> Every quoted string is VERBATIM from `_strings/strings.yaml`. Do not paraphrase.

---

## What This State Is

The app is spending the authorisation code: `POST /v1.1/oauth2/token` with
`grant_type=authorization_code` against `secure.sandbox.ob.hsbc.co.uk`, producing a PSU access
token scoped to `payments`.

This is the most time-critical operation in the feature. The code TTL is documented at 30–60
seconds and observed as minutes; the shorter figure is the safe one to engineer to. Codes were
lost twice in the corpus by doing analytics writes, persistence writes, or navigation
animations between receiving the redirect and issuing this call.

---

## Visual Layout

**Shell**: identical to `validating` — same `TopAppBar` titled "Authorising payment", no bottom
navigation, no leading icon, no trailing action.

**Content area**: vertically centred column, padding `spacing.md`, gap `spacing.lg`.

**Component 1 — `CircularProgressIndicator` (id: `authorising_indicator`)**
- Indeterminate, 48 × 48dp, stroke 4dp, `colors.primary`
- contentDescription: "Authorising your payment"

**Component 2 — `Text` (id: `progress_detail`)**
- Content: "Confirming with your bank. This usually takes a few seconds."
- `bodyLarge`, `colors.on_surface`, centred, max width 280dp

No buttons. The PSU cannot interact with this state.

---

## What Changes from `validating`

Visually: nothing. `ui.yaml` binds the SAME `progress_detail` and `progress_label` keys across
`validating`, `exchanging` and `checking`, and the catalogue holds ONE value for each.

Per-phase wording ("Connecting to your bank…") is **UNSOURCED — no key exists for it.** The
earlier version of this prompt claimed the label changes between phases; it does not. Render
the single catalogue value. If per-phase wording is wanted, add the keys first.

---

## Token Reference

| Token | Light | Dark | Applied to |
|---|---|---|---|
| `colors.surface` | #F7F9FF | #101417 | Screen background |
| `colors.on_surface` | #181C20 | #E0E3E8 | Top bar title, progress label |
| `colors.primary` | #266489 | #95CDF7 | Progress indicator stroke |
| `spacing.md` | 16dp | — | Screen padding |
| `spacing.lg` | 24dp | — | Gap between indicator and text |
| `icon.xl` | 48dp | — | Indicator size |

---

## Strings — verbatim from `_strings/strings.yaml`

| Key | Value |
|---|---|
| `payment_consent.screen_title` | "Authorising payment" |
| `payment_consent.progress_label` | "Authorising your payment" |
| `payment_consent.progress_detail` | "Confirming with your bank. This usually takes a few seconds." |

---

## Token Exchange Security Contract

The PSU `access_token` produced here is held in the ViewModel only. It is NEVER written to
`ConsentSession` (which holds the AIS data-sharing token), NEVER logged or emitted to
analytics, and NEVER persisted. It is passed to the originating screen only via
`PaymentConsentEvent.Authorised`, used immediately for funds-confirmation and submission, then
discarded. The `id_token` carries the `nonce`, validated immediately; on mismatch the token is
discarded and the screen transitions to `error`.

---

## Transitions Out

| Condition | Next state |
|---|---|
| 200 and `id_token.nonce` matches | `checking` |
| 200 but `nonce` does not match | `error` (`StateMismatch`) |
| `400 invalid_grant` | `error` (`CodeExpired`) |
| `401 invalid_client` | `error` (`NetworkError`) |
| Network failure / timeout | `error` (`NetworkError`) |

---

## What This State Must NOT Do

- No navigation animation in front of the API call.
- No analytics event between receiving the redirect and completing the exchange.
- No persistence write before the exchange.
- The token MUST NOT be written to `ConsentSession` at any point.
