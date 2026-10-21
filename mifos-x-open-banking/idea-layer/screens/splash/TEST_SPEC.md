# TEST SPEC — Splash

| Field      | Value                                |
|------------|--------------------------------------|
| Feature    | splash                               |
| Source     | `screens/splash/tests.yaml`          |
| Scenarios  | 7                                    |
| Priorities | high 4 · medium 3                    |
| States     | loading 4 · navigating 3             |
| Module     | _none yet — spec-only feature_       |

> No source module exists. These are **forward specs** derived from the feature's idea-layer
> siblings, not reverse-synced from a shipped suite.

---

## Coverage

| State      | Scenarios | Covered |
|------------|-----------|---------|
| loading    | 4 | TC-SPLASH-001, -005, -006, -007 |
| navigating | 3 | TC-SPLASH-002, -003, -004 |

Two states, both covered. No error state, correctly — this screen decides nothing and so has
nothing to fail at. If the session check errors, the routing authority handles it and this screen
simply hands off.

---

## The screen holds no authority

Three scenarios say the same thing from different directions, and it is the whole design:

- **TC-SPLASH-003** — `SplashViewModel` does **not** decide the target; `RootNavState` (Auth) drives it.
- **TC-SPLASH-004** — routing originates from `RootNavState` (`UserUnlocked`), not from `SplashViewModel`.
- **TC-SPLASH-007** — the ViewModel's only state field is `reducedMotion`; no DI, no `LoginRepository`, no `SessionManager`, and it never reads auth state.

Same principle as `profile` TC-PROF-009: one authority for "am I signed in", observed rather than
asked. A splash screen that read the token itself would be a second place that can disagree with
`RootNavViewModel` about whether the customer is authenticated — and the disagreement would show
up as an app that opens on the wrong screen.

---

## The two-second hold is asymmetric

| Session | Delay | Scenario |
|---------|:-----:|----------|
| `hasValidToken == false` → login | **2000 ms** | TC-SPLASH-003 |
| `hasValidToken == true` → home | **0 ms** | TC-SPLASH-004 |

A returning customer pays nothing; a signed-out one waits two seconds to be shown a login form.
That is branding time charged to the person with the least patience for it — someone who has to
type credentials next. Recorded as a deliberate asymmetry, not a bug, but worth a second look.

---

## TC-SPLASH-001 — Loading state renders the full branded stack

**Priority:** high · **State:** loading

- **Given** App cold start; `RootNavViewModel` has not yet resolved `RootNavState`
- **When** Splash mounts
- **Then**
  - `splash_logo` visible, tinted `primary`, 120dp square, a11y label "Mifos X application logo"
  - `splash_app_name` visible with text "Mifos X Open Banking" as a heading
  - `splash_tagline` visible with text "Banking for Everyone"
  - `splash_loading_indicator` visible as a `circular_indeterminate` progressbar, a11y label "Loading, please wait"
  - Layout is a centre-aligned column on `surface` background

The tagline here reads "Banking for Everyone"; `about` TC-ABOUT-002 asserts `about_tagline_text`
reads "**Open** Banking for Everyone". Two taglines for one app. Minor, and the kind of divergence
that survives indefinitely once both are pinned by a test — worth settling on one.

---

## TC-SPLASH-002 — Navigating state keeps the same visible components while routing resolves

**Priority:** medium · **State:** navigating

- **Given** `RootNavViewModel` has resolved a destination but the transition has not completed
- **When** State moves loading → navigating
- **Then**
  - All four components remain visible — no flash of an empty or partially-composed frame
  - `splash_loading_indicator` still animating

The reason `navigating` is a separate state at all. Without it the composition could tear down
before the destination is on screen, and a blank frame on cold start reads as a crash.

---

## TC-SPLASH-003 — Unauthenticated start routes to login after the 2s hold

**Priority:** high · **State:** navigating

- **Given** `hasValidToken == false`
- **When** Session check completes and the `nav_to_login` condition is met
- **Then**
  - App navigates to `login` after `delay_ms: 2000`
  - Navigation is triggered automatically (`trigger: auto`) — no user interaction required
  - `SplashViewModel` does **NOT** decide the target; `RootNavState` (Auth) drives it

---

## TC-SPLASH-004 — Authenticated start routes straight to home with no artificial delay

**Priority:** high · **State:** navigating

- **Given** `hasValidToken == true`
- **When** Session check completes and the `nav_to_consumer_home` condition is met
- **Then**
  - App navigates to `home` with `delay_ms: 0`
  - `login` is never placed on the back stack
  - Routing originates from `RootNavState` (`UserUnlocked`), not from `SplashViewModel`

"`login` is never placed on the back stack" is the assertion that protects the back gesture. A
customer on `home` pressing back should leave the app, not land on a login screen they never saw.

---

## TC-SPLASH-005 — Reduced-motion preference swaps the indicator for a static logo

**Priority:** medium · **State:** loading

- **Given** `reducedMotion == true` (system accessibility preference enabled)
- **When** Splash mounts
- **Then**
  - `reduced_motion_fallback` `static_logo` is rendered in place of the animated indicator
  - No indefinite animation runs
  - `splash_logo`, `splash_app_name` and `splash_tagline` still visible

The third assertion keeps the fallback from becoming a downgrade — reduced motion removes the
animation, not the screen.

Note this is the ViewModel's *only* state field (TC-SPLASH-007), so the accessibility preference
is the single thing this screen is permitted to know.

---

## TC-SPLASH-006 — Splash does not hang past its motion ceiling

**Priority:** medium · **State:** loading

- **Given** Session check is slow or stalled
- **When** `max_duration` 10000 ms elapses
- **Then**
  - Splash does not remain indefinitely — routing resolves or the app surfaces its next state
  - The loading indicator does not animate past the declared ceiling

The assertion is a disjunction — "routing resolves **or** the app surfaces its next state" — which
leaves the actual behaviour at 10 seconds undefined. Given TC-SPLASH-007's insistence that this
screen holds no authority, it cannot route itself out of a stall; the timeout must be enforced by
`RootNavViewModel`. Which component owns the ceiling is worth stating explicitly, otherwise the
scenario passes trivially and a genuine hang ships.

---

## TC-SPLASH-007 — SplashViewModel stays a thin visual host

**Priority:** high · **State:** loading

- **Given** `SplashViewModel` is constructed
- **When** Its contract is inspected
- **Then**
  - Its only state field is `reducedMotion: Boolean` (default false)
  - It declares no errors, no events, no actions and no DI
  - It does not hold `LoginRepository` or `SessionManager` and never reads auth state

---

## Traceability

| Condition | Destination | Delay | Scenario |
|-----------|-------------|:-----:|----------|
| `nav_to_login` | `login` | 2000 ms | TC-SPLASH-003 |
| `nav_to_consumer_home` | `home` | 0 ms | TC-SPLASH-004 |

Both declared navigation conditions are covered. The screen exposes no user-triggered action at
all — every transition is `trigger: auto`.

---

_Generated by /idea-feature-test-export | 2026-08-04_
