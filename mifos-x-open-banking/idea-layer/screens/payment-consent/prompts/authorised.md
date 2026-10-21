# payment-consent · state: authorised

> Feature: payment-consent · State role: content (terminal success)
> Archetype: headless / transitional
> Design system: Open Banking — Trust Blue (Material 3, seed #266489)
> Every quoted string is VERBATIM from `_strings/strings.yaml`. Do not paraphrase.

---

## What This State Is

The consent has reached `Data.Status == "AUTH"`. The app emits
`PaymentConsentEvent.Authorised(consentId, psuToken, authorisedInitiation)` and the originating
type screen proceeds to submit.

This state is transient — the originator usually dismisses the feature immediately — but it
MUST render as a discrete state rather than flashing blank: the originator may take a moment to
act, the gap is perceptible under memory pressure, and a blank flash between "waiting" and
"payment submitted" reads as a crash.

The copy confirms what happened at the bank. The payment is authorised, not yet submitted.

---

## Visual Layout

**Shell**: `TopAppBar` titled "Authorising payment", no bottom navigation, no leading icon.

**Content area**: vertically centred column, padding `spacing.md`, gap `spacing.lg`.

**Component 1 — Icon container** (part of `EmptyState` id: `authorised_state`, `variant: success`)
- 64 × 64dp, radius `radius.md` (12dp)
- Fill `colors.primary_container` (#C9E6FF light / #004B6F dark)
- Icon `verified_user`, `icon.xl` (48dp), `colors.on_primary_container`
- Contrast 7.3:1 — WCAG AA pass

**Component 2 — Title**
- Content: "Payment authorised"
- `headlineSmall`, `colors.on_surface`, centred

**Component 3 — Body**
- Content: "Your bank has approved this payment. Sending it now."
- `bodyMedium`, `colors.on_surface_variant`, centred, max width 280dp

No buttons. This state resolves when the originating screen acts on the event.

---

## Why `semantic.status.success` and not a celebration layout

The `success` semantic maps to `primary` — `primaryContainer` / `onPrimaryContainer`, the same
pair as `payment_disposition.terminal_success`. It reads as confirmation without excitement.

No confetti. No green tick. No large celebratory animation. Calm, regulated banking: "this is
done" is carried by the `verified_user` icon and the title. Trust-blue, not celebration-green.

---

## Token Reference

| Token | Light | Dark | Applied to |
|---|---|---|---|
| `colors.surface` | #F7F9FF | #101417 | Screen background |
| `colors.on_surface` | #181C20 | #E0E3E8 | Top bar title, state title |
| `colors.on_surface_variant` | #41474D | #C1C7CE | Body text |
| `colors.primary_container` | #C9E6FF | #004B6F | Icon container fill |
| `colors.on_primary_container` | #004B6F | #C9E6FF | Icon glyph |
| `spacing.md` / `.lg` | 16 / 24dp | — | Padding, gap |
| `radius.md` | 12dp | — | Icon container radius |
| `icon.xl` | 48dp | — | Icon size |

---

## Strings — verbatim from `_strings/strings.yaml`

| Key | Value |
|---|---|
| `payment_consent.screen_title` | "Authorising payment" |
| `payment_consent.authorised_title` | "Payment authorised" |
| `payment_consent.authorised_body` | "Your bank has approved this payment. Sending it now." |

---

## Hand-Back Contract

On entering this state the ViewModel emits:

```
PaymentConsentEvent.Authorised(
    consentId = state.consentId,
    psuToken  = state.psuToken,
    authorisedInitiation = lastPollResponse.Data.Initiation,
)
```

The originating screen MUST use `authorisedInitiation` when constructing the submit body — not
its own locally staged `Initiation`. Where the TPP omitted `DebtorAccount` the bank has
overwritten it with the PSU's picker choice; submitting the local copy returns `U008`.

The `psuToken` MUST NOT be written to `ConsentSession` at any point, including by the
originating screen. It is used immediately for funds-confirmation and submission, then discarded.

---

## Transitions Out

None from this screen. The originating screen acts on `PaymentConsentEvent.Authorised` and
dismisses the feature. There is nothing for the PSU to tap.
