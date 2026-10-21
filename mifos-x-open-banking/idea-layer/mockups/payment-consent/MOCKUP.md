# payment-consent — Mockup Specification

> Feature: payment-consent
> Archetype: headless / transitional
> States: validating · exchanging · checking · authorised · error
> Design system: Open Banking — Trust Blue (Material 3, seed #266489)

---

## Visual Character of This Screen

> COPY SOURCE: every quoted string is VERBATIM from `_strings/strings.yaml` unless marked
> UNSOURCED. `ui.yaml` binds ONE `progress_detail` and ONE `progress_label` key across all
> three loading states — per-phase progress wording has no keys and must not be invented.

`payment-consent` is a headless, transitional feature. It owns no form, no data table, no list. Its job is to make three sequential network operations legible to a PSU who is sitting with their phone after they just approved a payment at their bank. Each operation can fail in a different way, so each gets a named STATE — but all three share one progress string, because that is what the catalogue declares.

The visual vocabulary is centred, vertically stacked, low-chrome: a progress indicator above a label that names the current step, and nothing else until a terminal state is reached. Terminal states use the design system's `empty_state` and `error_state` full-screen layouts.

Bottom navigation is hidden. Top app bar is visible, titled with `strings.payment_consent.screen_title`, no leading navigation icon (the PSU cannot back out of an in-flight authorisation return), no trailing actions.

---

## Component Hierarchy

### Shell (all states)

```
Scaffold (surface: colors.surface / #F7F9FF)
  TopAppBar
    title: strings.payment_consent.screen_title
    titleTypography: titleLarge (22sp, weight 400)
    titleColor: colors.on_surface (#181C20)
    container: colors.surface (#F7F9FF)
    leading: none
    trailing: none
    bottom_navigation_visible: false
```

---

### State: `validating`

The first milliseconds after the redirect lands. The app checks the `state` parameter against the pending authorisation locally and synchronously. This state is typically sub-second but MUST be rendered because it names the security check.

```
CenteredColumn (padding: spacing.md = 16dp, gap: spacing.lg = 24dp)
  CircularProgressIndicator (id: authorising_indicator)
    color: colors.primary (#266489)
    size: 48dp
    strokeWidth: 4dp

  Text (id: progress_detail)
    content: strings.payment_consent.progress_detail  → "Confirming with your bank. This usually takes a few seconds."
    typography: bodyLarge (16sp, weight 400)
    color: colors.on_surface (#181C20)
    textAlign: center
    maxWidth: 280dp
```

**Token bindings**: `colors.primary`, `colors.on_surface`, `spacing.md`, `spacing.lg`

---

### State: `exchanging`

The app is spending the authorisation code. This is the most time-critical moment — the code TTL is minutes, so the app performs the exchange as the first action after the state check. The progress label changes to differentiate this from the checking phase.

```
CenteredColumn (padding: spacing.md, gap: spacing.lg)
  CircularProgressIndicator (id: authorising_indicator)
    color: colors.primary (#266489)
    size: 48dp

  Text (id: progress_detail)
    content: strings.payment_consent.progress_detail  → "Confirming with your bank. This usually takes a few seconds."
    typography: bodyLarge
    color: colors.on_surface
    textAlign: center
    maxWidth: 280dp
```

**Token bindings**: same as `validating` — the progress indicator and label are identical components, and the string is identical too. `progress_detail` is a single key with a single value; it does NOT change between `validating`, `exchanging` and `checking`.

---

### State: `checking`

The app is polling the consent endpoint. This is the longest phase — up to 3 minutes with exponential backoff. The PSU may have only just finished at the bank and the status has not yet propagated. A "Check again" button lets the PSU trigger a manual re-poll if they know they have already approved.

```
CenteredColumn (padding: spacing.md, gap: spacing.lg)
  CircularProgressIndicator (id: authorising_indicator)
    color: colors.primary (#266489)
    size: 48dp

  Text (id: progress_detail)
    content: strings.payment_consent.progress_detail  → "Confirming with your bank. This usually takes a few seconds."
    typography: bodyLarge
    color: colors.on_surface
    textAlign: center
    maxWidth: 280dp

  TextButton (id: check_again_button)
    label: strings.payment_consent.check_again  → "Check again"
    typography: labelLarge (14sp, weight 500)
    color: colors.primary (#266489)
    minHeight: 48dp   ← touch target floor
    paddingHorizontal: spacing.lg (24dp)
    paddingVertical: spacing.sm (8dp)
```

The "Check again" button is ONLY visible in the `checking` state. The automatic poll continues in parallel — tapping "Check again" triggers a single immediate re-poll on top of the scheduled one.

**Token bindings**: `colors.primary`, `colors.on_surface`, `spacing.md`, `spacing.lg`, `spacing.sm`, `touch_targets.comfortable (48dp)`

---

### State: `authorised`

Terminal success. The consent reached `AUTH`. The app will emit `PaymentConsentEvent.Authorised` and the originating screen will proceed to submit. This state is transient — the originating screen typically dismisses it immediately — but it must be rendered to avoid a blank flash.

```
EmptyState (id: authorised_state, variant: success)
  icon: verified_user
    size: icon.xl (48dp)
    color: semantic.status.success → colors.primary_container / colors.on_primary_container
          light: #C9E6FF container, #004B6F on-container

  title: strings.payment_consent.authorised_title  → "Payment authorised"
    typography: headlineSmall (24sp, weight 400)
    color: colors.on_surface (#181C20)
    textAlign: center

  body: strings.payment_consent.authorised_body  → "Your bank has approved this payment. Sending it now."
    typography: bodyMedium (14sp, weight 400)
    color: colors.on_surface_variant (#41474D)
    textAlign: center
    maxWidth: 280dp
```

**Visual treatment**: The `success` variant of `empty_state` uses `semantic.status.success`, which maps to `primary` — `primaryContainer` background for the icon container (`#C9E6FF` light), `onPrimaryContainer` for the icon glyph (`#004B6F` light). This is the same pair as `payment_disposition.terminal_success` — deliberately reused because they mean the same thing. Contrast: 7.27:1, WCAG AA pass.

**Token bindings**: `colors.primary_container`, `colors.on_primary_container`, `colors.on_surface`, `colors.on_surface_variant`, `icon.xl`, `typography.headlineSmall`, `typography.bodyMedium`

---

### State: `error`

One layout for all six error types. The `error.type` value changes which CTA(s) appear.

```
ErrorState (id: error_state)
  icon: error_outline
    size: icon.xl (48dp)
    color: colors.error (#BA1A1A)

  title: strings.payment_consent.error_title  → "Authorisation could not be completed"
    typography: headlineSmall (24sp, weight 400)
    color: colors.on_surface (#181C20)
    textAlign: center

  body: {error.message}  ← resolved from strings.error.payment_consent.{error_type}
    typography: bodyMedium (14sp, weight 400)
    color: colors.on_surface_variant (#41474D)
    textAlign: center
    maxWidth: 280dp

  [Conditional — visible when error.type in {CodeExpired, AuthorisationTimedOut, NetworkError}]
  FilledButton (id: restart_authorisation_button)
    label: strings.payment_consent.restart  → "Start again"
    typography: labelLarge (14sp, weight 500)
    container: colors.primary (#266489)
    labelColor: colors.on_primary (#FFFFFF)
    cornerRadius: radius.full (9999dp)
    minHeight: 48dp
    paddingHorizontal: spacing.xl (32dp)

  TextButton (id: abandon_button)  ← always visible in error state
    label: strings.payment_consent.abandon  → "Discard payment"
    typography: labelLarge (14sp, weight 500)
    color: colors.on_surface_variant (#41474D)
    minHeight: 48dp
    paddingHorizontal: spacing.lg (24dp)
```

**CTA visibility by error type**:

| Error type | Restart CTA visible | Abandon CTA visible |
|---|:---:|:---:|
| `StateMismatch` | No | Yes |
| `NoPendingAuthorisation` | No | Yes |
| `CodeExpired` | Yes | Yes |
| `ConsentRejected` | No | Yes |
| `AuthorisationTimedOut` | Yes | Yes |
| `NetworkError` | Yes | Yes |

**"Start again" semantics**: This CTA emits `PaymentConsentEvent.RestartAuthorisation` with NO `consentId`. The originating screen MUST stage a fresh consent. It MUST NOT relaunch the authorise leg against the existing `consentId` — an already-`AUTH` consent cannot be re-authorised (sandbox rejects the attempt).

**Token bindings**: `colors.error`, `colors.on_surface`, `colors.on_surface_variant`, `colors.primary`, `colors.on_primary`, `icon.xl`, `radius.full`, `touch_targets.comfortable`, `typography.headlineSmall`, `typography.bodyMedium`, `typography.labelLarge`, `spacing.xl`, `spacing.lg`

---

## Component ↔ API Binding

| Component | State(s) | API Operation | Trigger |
|---|---|---|---|
| `authorising_indicator` | validating, exchanging, checking | All three operations in flight | on mount → on_loading |
| `progress_detail` | validating, exchanging, checking | One key, one value across all three — the string does NOT change per step | State transition |
| `check_again_button` | checking | `get_consent_status` (single immediate re-poll) | User tap |
| `authorised_state` | authorised | None — rendered after successful `get_consent_status` poll | Terminal state |
| `restart_authorisation_button` | error (restartable types) | None — emits `PaymentConsentEvent.RestartAuthorisation` | User tap |
| `abandon_button` | error (all types) | None — emits `PaymentConsentEvent.Abandoned` | User tap |

---

## Partial-Failure Taxonomy

| Phase | What failed | Is payment lost? | CTA offered | Notes |
|---|---|---|---|---|
| State check | `state` mismatch | No payment staged or submitted | Abandon only | Possible CSRF or crossed authorisation; no retry |
| State check | `NoPendingAuthorisation` | No payment staged or submitted | Abandon only | App restarted mid-journey |
| Code exchange | `400 invalid_grant` (CodeExpired) | No payment staged or submitted | Restart + Abandon | Code unrecoverable; new consent needed |
| Code exchange | `401 invalid_client` | No payment staged or submitted | Abandon | TPP signing-key issue, not PSU fault |
| Consent poll | `RJCT` | No payment made | Abandon only | PSU denied at the bank — no resubmit |
| Consent poll | Timeout (AWAU past deadline) | No payment made | Restart + Abandon | PSU may still be authenticating; restart stages new consent |
| Consent poll | `IOException` | No payment made | Restart + Abandon | Safe to retry — reads are idempotent |

All paths reaching `error` leave the staged consent to expire on its own. There is no revocation call in any path: an unauthorised consent cannot be submitted against, and consent IDs are sequential integers that the app must not guess or enumerate. The consent expires server-side without any action from the client.

---

## Accessibility Notes

- Bottom navigation hidden → no distraction, full vertical space for centred content.
- Top app bar has no leading icon by design — backing out of an in-flight authorisation return is not a safe operation.
- All touch targets meet `touch_targets.comfortable` (48dp minimum height).
- Colour is never the sole signal: every terminal state carries a named icon + title text. WCAG 1.4.1.
- `authorising_indicator` has `accessibility_label: strings.payment_consent.progress_label` for screen readers.
- `progress_detail` text is `bodyLarge` (16sp) on `colors.on_surface` (#181C20) against `colors.surface` (#F7F9FF) — contrast >7:1, WCAG AA pass.
- The three loading states are `role: loading` in the canonical state map, so testing and screen readers see a unified loading semantic across the distinct YAML states.
