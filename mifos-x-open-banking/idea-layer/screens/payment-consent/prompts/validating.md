# payment-consent · state: validating

> Feature: payment-consent · State role: loading (step 1 of 3)
> Archetype: headless / transitional
> Design system: Open Banking — Trust Blue (Material 3, seed #266489)
> Every quoted string is VERBATIM from `_strings/strings.yaml`. Do not paraphrase.

---

## What This State Is

The app has just received the redirect from HSBC after the PSU approved the payment at their
bank. Before spending the authorisation code it checks the returned `state` parameter against
the one it generated. The check is local and synchronous — no network call. It renders for
under a second on the normal path, but it is a named state because a mismatch is a possible
CSRF signal and the PSU must see the app detected it and stopped.

---

## Visual Layout

**Shell**: `Scaffold` + `TopAppBar`. No bottom navigation. No leading icon — the PSU cannot
back out of an in-flight authorisation return.

**TopAppBar**: title "Authorising payment" (`titleLarge`, `colors.on_surface`), container
`colors.surface`, no leading, no trailing.

**Content area**: vertically centred column, padding `spacing.md` (16dp), gap `spacing.lg` (24dp).

**Component 1 — `CircularProgressIndicator` (id: `authorising_indicator`)**
- Indeterminate, 48 × 48dp, stroke 4dp, `colors.primary`
- contentDescription: "Authorising your payment"

**Component 2 — `Text` (id: `progress_detail`)**
- Content: "Confirming with your bank. This usually takes a few seconds."
- `bodyLarge`, `colors.on_surface`, centred, max width 280dp

No buttons. The PSU cannot interact with this state; it resolves automatically to `exchanging`
on match, or to `error` on mismatch.

---

## One string, three states — do not vary it

`ui.yaml` binds the SAME `progress_detail` and `progress_label` keys across `validating`,
`exchanging` and `checking`, and the catalogue holds ONE value for each. Per-state progress
wording ("Confirming your approval…", "Connecting to your bank…", "Waiting for your bank to
confirm…") is **UNSOURCED — no keys exist for it.** Render the single catalogue value in all
three states. If per-phase wording is wanted, add the keys first.

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

## Transitions Out

| Condition | Next state |
|---|---|
| `state` param matches the `PendingAuthStore` record | `exchanging` |
| `state` param does not match | `error` (`StateMismatch`) |
| `PendingAuthStore` has no record (app restarted) | `error` (`NoPendingAuthorisation`) |

---

## What This State Must NOT Do

- No analytics call before the state check resolves.
- No persistence write.
- No navigation animation that could delay reaching `exchanging`.
- No back/close affordance — backing out of an in-flight return is not a safe operation.
