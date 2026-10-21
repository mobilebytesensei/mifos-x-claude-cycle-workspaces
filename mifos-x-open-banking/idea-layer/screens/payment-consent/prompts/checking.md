# payment-consent · state: checking

> Feature: payment-consent · State role: loading (step 3 of 3)
> Archetype: headless / transitional
> Design system: Open Banking — Trust Blue (Material 3, seed #266489)
> Every quoted string is VERBATIM from `_strings/strings.yaml`. Do not paraphrase.

---

## What This State Is

The app polls the consent endpoint with a client-credentials token until `Data.Status` reaches
`AUTH`. The poll is load-bearing: submitting against a consent that is not Authorised returns
`400 U009` on every family.

Schedule: initial 2 000ms, backoff 1.5×, max interval 15 000ms, max total 180 000ms. At the
deadline the state stays rendered — the PSU may still be at the bank — and `check_again_button`
becomes the primary affordance.

**Critical poll rule**: `StatusUpdateDateTime` is NEVER the poll signal. All five authorised
consents in the corpus went `AWAU → AUTH` with it unchanged. Read `Data.Status` only.

---

## Visual Layout

**Shell**: identical to `validating` and `exchanging` — `TopAppBar` titled "Authorising
payment", no bottom navigation, no leading icon.
**Content**: vertically centred column, padding `spacing.md`, gap `spacing.lg`.

1. **`CircularProgressIndicator`** (`authorising_indicator`) — indeterminate, 48 × 48dp,
   stroke 4dp, `colors.primary`. contentDescription: "Authorising your payment"
2. **`Text`** (`progress_detail`) — `bodyLarge`, `colors.on_surface`, centred, max 280dp.
   Content: "Confirming with your bank. This usually takes a few seconds."
3. **`TextButton`** (`check_again_button`) — unique to this state. Label "Check again",
   `labelLarge`, `colors.primary`, min height 48dp, padding horizontal `spacing.lg` / vertical
   `spacing.sm`, radius `radius.full`. Action `check_again` → one immediate re-poll.
   contentDescription: "Check with your bank again for the authorisation result"

It is the ONLY interactive component across the three loading states. The automatic poll
continues in parallel — tapping it adds a single immediate call on top.

**One string, three states**: `ui.yaml` binds the SAME `progress_detail` and `progress_label`
keys across `validating`, `exchanging` and `checking`, and the catalogue holds ONE value for
each. Per-phase wording ("Waiting for your bank to confirm…") is UNSOURCED — no key exists.

---

## Token Reference

`colors.surface` (background) · `colors.on_surface` (top bar title, progress label) ·
`colors.primary` (indicator stroke, check-again label) · `spacing.md/.lg/.sm` 16/24/8dp ·
`radius.full` 9999dp · `icon.xl` 48dp. All by name — no hex literals.

---

## Strings — verbatim from `_strings/strings.yaml`

| Key | Value |
|---|---|
| `payment_consent.screen_title` | "Authorising payment" |
| `payment_consent.progress_label` | "Authorising your payment" |
| `payment_consent.progress_detail` | "Confirming with your bank. This usually takes a few seconds." |
| `payment_consent.check_again` | "Check again" |
| `payment_consent.check_again_a11y` | "Check with your bank again for the authorisation result" |

---

## Poll Family Resolution

Path resolves from the `paymentFamily` nav param over `/obie/open-banking/v4.0/pisp/{path}/
{consentId}`, `{path}` ∈ `{domestic,international}-payment-consents`,
`{domestic,international}-scheduled-payment-consents`,
`{domestic,international}-standing-order-consents`, `domestic-vrp-consents`.

---

## Transitions Out

`AUTH` → `authorised` · `RJCT` → `error(ConsentRejected)` · deadline reached still `AWAU` →
stays `checking` with check-again prominent · network failure → `error(NetworkError)`.

---

## What This State Must NOT Do

- Do NOT poll `StatusUpdateDateTime`.
- Do NOT call a different family's consent path — `paymentFamily` resolves it.
- Do NOT abandon the consent on deadline. Timeout is non-terminal.
- Do NOT add a progress percentage or countdown. The bank exposes no reliable timeline.
