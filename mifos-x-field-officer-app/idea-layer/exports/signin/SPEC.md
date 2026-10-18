<!--
generated_by: /idea-feature-export-spec
generated_at: 2026-10-03
feature_id: signin
generated_from_feature_version: "2.0"
sources:
  - screens/signin/docs.yaml
  - screens/signin/ui.yaml
  - screens/signin/api.yaml
  - screens/signin/flow.yaml
  - screens/signin/tests.yaml
  - design-system/design-tokens.yaml
  - design-system/app-shell.yaml
  - REQUIREMENTS.md
design_tier_consumed: stitch          # RULE-UI-SOURCE-001 US9: Stitch > LLM preview > ui.yaml
-->

# SPEC — Sign in

Authenticates a field officer against the configured Fineract instance and establishes the session
every other screen depends on. Surfaces **which** instance it will authenticate against before the
user types, and is the only route to server configuration: a first-run user has no server URL and
therefore cannot sign in until one is set.

| | |
|---|---|
| Feature id | `signin` |
| Module | `feature/signin` |
| Route | `SignInRoute` (no params) |
| Entry point | yes — the unauthenticated gate |
| Bottom nav | no |
| Version | 2.0 (v1 = `6b66e8a43`) |

> **v1 is the context, not the ceiling.** The original fixes WHAT this screen does; v2 designs HOW,
> using capabilities the template already ships. Every v2 addition below is capability-cited.

## Capabilities

### authenticate-with-credentials
Submit username + password to the configured Fineract instance and establish a session.
Backed by `core/data` `AuthCommandRepository` under `MutationPolicy.OnlineRequired`.

### see-the-target-instance
Show the host and tenant this sign-in will hit, before the user types, and allow changing it.
Backed by the `serverConfig` feature + `ServerConfig`. **(v2)**

### unlock-with-biometrics
A returning officer with a stored session unlocks without retyping a password.
Backed by `core-base/security` `BiometricAuthenticator` (android / ios / desktop / js actuals). **(v2)**

### throttle-repeated-failures
Warn as failures accumulate, then pause sign-in once the policy threshold is reached.
Backed by `core-base/security` `FailedAttemptTracker` + `SecureAuthManager`. **(v2)**

### state-terms-at-point-of-collection
Present terms and privacy adjacent to the action that collects the credential. **(v2)**

## Screens

| Screen | ViewModel | States handled |
|---|---|---|
| `SignInScreen` | `SignInViewModel` | empty, biometric_ready, submitting, validation_error, transport_error, offline, locked_out, success |

## State Model

### SignInViewModel

| State | Renders | Source |
|---|---|---|
| `empty` | pristine form; instance chip states the target | `LoginUiState.Empty` |
| `biometric_ready` | unlock accelerator above a still-usable form | **v2** |
| `submitting` | modal overlay over the form; fields keep their values | `LoginUiState.ShowProgress` |
| `validation_error` | error text + trailing error icon on the OFFENDING field only | `LoginUiState.ShowValidationError` |
| `transport_error` | snackbar; fields preserved; remaining-attempts hint | `LoginUiState.ShowError` |
| `offline` | snackbar, distinct from a rejected credential | port addition |
| `locked_out` | submit disabled, banner states cause and clearing time | **v2** |
| `success` | session persisted; root state machine routes onward | `LoginUiState.HomeActivityIntent` |

Initial state: `empty`.

| Field | Type |
|---|---|
| `username` | `String` |
| `password` | `SensitiveString` (AutoCloseable; zeroes its CharArray) |
| `isSubmitting` | `Boolean` |
| `error` | `SignInError?` |

`SignInError` = `UsernameTooShort | PasswordTooShort | Rejected | Offline | LockedOut`.
Distinct causes, because the officer's next step differs for each.

## App-Shell

Resolved from `design-system/app-shell.yaml` + `ui.yaml#shell`.

| Element | Resolved | Why |
|---|---|---|
| Top app bar | **hidden** | unauthenticated gate; nowhere to navigate back to |
| Bottom navigation | **hidden** | no tab to switch to before authentication |
| FAB | hidden | no secondary action |
| Safe area | respect top + bottom | |

The project default is the authenticated shell (top bar + bottom nav); this screen opts out
explicitly. Any chrome here would be a dead affordance.

## API

| Endpoint | Method | Request | Response | Success condition |
|---|---|---|---|---|
| `authentication` | POST | `username(String)`, `password(String)` | `PostAuthenticationResponse` | `200 AND body.authenticated == true` |

Write policy **`OnlineRequired`** — an authentication cannot be queued. A credential check that
"succeeds" locally and syncs later would admit a user the server never agreed to. Offline yields
`MutationResult.Blocked(OFFLINE)`.

Full contracts: `API.md`.

## Navigation

| | |
|---|---|
| Route | `SignInRoute` |
| Entry points | `rootNav` — `RootNavState.Auth` \| `ShowOnboarding` \| `UserLocked` |
| Navigates to | `serverConfig` (instance chip), `home` (on success) |

`SignInScreen` is deliberately **not** annotated `@FeatureDestination`: that annotation registers
onto the AUTHENTICATED graph (`AuthenticatedNavigation.kt:54`), which is the one graph this gate
must sit in front of. The feature exposes a plain `NavGraphBuilder` extension the shell installs on
the root graph.

## Flow Logic

| Decision | Condition | True path | False path |
|---|---|---|---|
| local validation | `CredentialRules.username` + `.password` pass | issue the request | `validation_error`, zero network calls |
| call outcome | `MutationResult` | `Applied` → check `authenticated` | `Blocked(OFFLINE)` → `offline`; `Failed` → `transport_error` |
| authenticated flag | `body.authenticated == true` | persist session, emit `LoggedIn` | `transport_error` — a successful CALL is not a successful LOGIN |
| failure count | `FailedAttemptTracker.isLockedOut` | `locked_out`, submit disabled | warn with remaining attempts |
| returning officer | stored session AND `BiometricAuthenticator.isAvailable()` | offer `biometric_ready` | credential form only |

## Visual Assets

| id | kind | produced by | status |
|---|---|---|---|
| `signin_brand_mark` | logo | `/idea-branding` | produced |

216×216 RGBA, 7,596 B, derived from the shipped adaptive-icon foreground at its alpha bbox.
Replaces a 75,684 B opaque JPEG that could not sit in a tinted tile or invert for dark theme.
Byte-derived from the launcher icon, so sign-in and the home-screen icon cannot drift apart.

## Testing

| id | Scenario | Priority |
|---|---|---|
| T1 | username < 4 → username error AND zero network calls | P0 |
| T2 | password < 6 → password error only; username stays clean | P0 |
| T3 | 200 with `authenticated == false` → rejected, not success | P0 |
| T4 | `Blocked(OFFLINE)` → offline message, distinct from rejected | P0 |
| T5 | success persists the session and emits `LoggedIn` | P0 |
| T6 | the raw password is never persisted | P0 |
| T7 | sign-in after sign-out reaches authenticated AND unlocked | P1 |
| T8 | an invalid password stays masked while its error icon shows | P0 |
| T9 | error icon replaces the visibility toggle, never joins it | P1 |
| T10 | submitting covers the form and keeps the instance chip reachable | P1 |

Device-verified 2026-10-03 on OnePlus CPH2423 against live `apis.mifos.community`:
`empty`, `validation_error` (both fields), `submitting`, `success`.
Not device-verified: `transport_error`, `offline`, `locked_out`, `biometric_ready`.

## Known Gaps

- **`expectSuccess` unset** (`core-base/network`) — a non-2xx body deserializes onto DTO defaults.
  Masked here by the explicit `authenticated` check; surfaced elsewhere as "Nothing here yet" on a
  401/502. Raised for upstream.
- **`onboarding` screen absent** — `RootNavState.ShowOnboarding` falls through to this screen.
  Recorded as a product decision, not silently built.
- **6 of 8 Stitch renders show a stale hostname** (`demo.mifos.io`). Prompts now carry the true
  instance; the renders need regeneration once the Stitch backend recovers.
