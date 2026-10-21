# TEST SPEC — Profile

| Field      | Value                                  |
|------------|----------------------------------------|
| Feature    | profile                                |
| Source     | `screens/profile/tests.yaml`           |
| Scenarios  | 13                                     |
| Priorities | high 8 · medium 5                      |
| States     | content 9 · error 3 · loading 1        |
| Module     | _none yet — spec-only feature_         |

> No source module exists. These are **forward specs** derived from the feature's idea-layer
> siblings, not reverse-synced from a shipped suite.

---

## Coverage

| State   | Scenarios | Covered |
|---------|-----------|---------|
| loading | 1 | TC-PROF-001 |
| content | 9 | TC-PROF-002 … -009, -013 |
| error   | 3 | TC-PROF-010, -011, -012 |

Three states. There is no empty state, correctly — a signed-in session always has a user.

---

## The screen is read-only, and three scenarios say so from different angles

| Assertion | Scenario |
|-----------|----------|
| All three fields are disabled `OutlinedTextField`s with no editable variant; no Save button | TC-PROF-003 |
| The avatar edit badge opens nothing and dispatches nothing | TC-PROF-006 |
| No control on the screen issues a write, and there is no write endpoint to issue one to | TC-PROF-013 |

TC-PROF-006 is the uncomfortable one. The badge carries `contentDescription` "Change profile
photo" and declares no `on_click` — so the screen tells a screen-reader user about an affordance
that does not exist. A decorative badge should have an empty label (as `notifications`
TC-NOTIF-005 does for its row icons) or the badge should not be there. The scenario records the
behaviour faithfully; the behaviour itself is worth changing.

---

## Cross-feature conflict — Change Password

TC-PROF-007 asserts `profile_change_password_button` renders **disabled**, labelled "Change
Password (not yet available)", and does not navigate to `change-password`.

But `change-password` is a fully specified feature with 15 scenarios, and its own TC-CHPW-001
places its entry point at "Screen entered from profile", with TC-CHPW-015 returning there. Two
specs describe the same edge in opposite terms: one says the door is locked, the other documents
the room behind it and names this screen as the way in.

Not settled here. Either `profile` enables the button once `change-password` ships (in which case
TC-PROF-007 becomes a temporary state that needs a dated waiver), or `change-password` is reached
from `settings` instead and its entry-point copy is wrong. Flagged for `/idea-sync`.

---

## TC-PROF-001 — Loading state shows only the centred spinner

**Priority:** high · **State:** loading

- **Given** `ScreenState.Loading` — the profile load is in flight
- **When** Screen mounts
- **Then**
  - `profile_loading_spinner` visible as a `circular_indeterminate` progressbar, a11y label "Loading your profile"
  - Avatar section, form section and both buttons **NOT** rendered

Hiding the logout button during load is a real consequence: a customer who opens Profile
specifically to sign out cannot, until the profile fetch resolves. On a failed fetch (TC-PROF-010)
logout stays hidden entirely.

---

## TC-PROF-002 — Content state renders the read-only profile

**Priority:** high · **State:** content

- **Given** The profile load resolves a display name and an email; `ScreenState.Content`
- **When** Screen renders
- **Then**
  - `profile_avatar_section`, `profile_form_section`, `profile_change_password_button` and `profile_logout_button` visible
  - `profile_avatar_initials` renders a circular `primaryContainer` box with up to two uppercase initials from `displayName`
  - `profile_display_name` shows the `displayName` as a heading
  - `profile_section_header` "Personal Information" visible
  - No profile photo is fetched — the avatar is initials only

---

## TC-PROF-003 — All three personal-information fields are display-only

**Priority:** high · **State:** content

- **Given** Content state with `ProfileContent` bound
- **When** The form fields render
- **Then**
  - `profile_full_name_field`, `profile_email_field` and `profile_phone_field` each render as a disabled `OutlinedTextField`
  - Each declares `supported_states: [disabled]` only — there is no editable variant
  - No Save button exists anywhere on the screen
  - Field outlines use the `outline` token (4.24:1) to satisfy WCAG 1.4.11

Disabled text fields for display-only values is a common pattern and a poor one: it looks like a
form the customer is not permitted to use, rather than a summary. The contrast assertion is here
precisely because disabled styling normally fails it.

---

## TC-PROF-004 — Phone renders empty because the screen has no source for it

**Priority:** medium · **State:** content

- **Given** `ProfileContent.phone` is hardcoded blank
- **When** `profile_phone_field` renders
- **Then**
  - The field is visible with its "Phone Number" label
  - Its value is empty — not a placeholder, not "null", not a fabricated number

The field is rendered knowing it can never have a value. Empty beats invented, but a field that is
structurally always blank would be better omitted than shown perpetually empty.

> Rebased 2026-08-07 — the reason is no longer the OBP `UserProfile` shape but the absence of any
> bound data source at all (`api.yaml` carries `api: []` under a DECISION OWED). The assertion is
> unchanged.

---

## TC-PROF-005 — displayName falls back to the email local-part when username is blank

**Priority:** medium · **State:** content

- **Given** The profile load resolves a blank username and email "amina.wanjiru@example.com"
- **When** `ProfileContent` is derived
- **Then**
  - `displayName` resolves to the email local-part
  - `initials` are derived from that resolved `displayName` via `initialsOf`

The second assertion is the one that catches a partial fix: deriving initials from the raw
username while the heading shows the fallback produces an avatar that does not match the name
under it.

---

## TC-PROF-006 — The avatar edit badge is decorative and not interactive

**Priority:** medium · **State:** content

- **Given** Content state
- **When** User taps `profile_avatar_edit_icon`
- **Then**
  - No photo picker opens
  - No navigation occurs and no action is dispatched
  - The badge carries `contentDescription` "Change profile photo" but declares no `on_click`

> See the read-only section above — the a11y label advertises an action that does not exist.

---

## TC-PROF-007 — Change Password renders disabled and is not reachable

**Priority:** high · **State:** content

- **Given** Content state
- **When** `profile_change_password_button` renders and is tapped
- **Then**
  - Button is visible but `enabled=false`
  - a11y label reads "Change Password (not yet available)"
  - Tapping dispatches nothing and does not navigate to `change-password`

> **Conflicts with the `change-password` spec** — see above. The "(not yet available)" suffix is
> the right handling for a disabled control: it says *why*, rather than leaving a dead button.

---

## TC-PROF-008 — Logout clears local credential material

**Priority:** high · **State:** content

- **Given** Content state with an authenticated session
- **When** User taps `profile_logout_button` (`logout`)
- **Then**
  - `ProfileViewModel.onLogout()` calls `UserDataRepository.setIsAuthenticated(false)`
  - `session.credentials` and `session.consentIds` are cleared from encrypted-shared-preferences
  - The bank-side consent is **NOT** revoked — it survives and must be revoked from `consent-manager`

The third assertion is the important one and it deserves surfacing in the UI, not only in a test.
Signing out looks like disconnecting; the customer's AISP consent keeps running at the bank until
they revoke it (`consent-manager` TC-CMGR-010). Nothing on this screen says so.

---

## TC-PROF-009 — Post-logout routing is reactive, never imperative

**Priority:** high · **State:** content

- **Given** `onLogout()` has flipped the session flag
- **When** `RootNavViewModel` observes `UserDataRepository.userData`
- **Then**
  - `RootNavViewModel` routes back to the auth graph
  - `ProfileScreen` itself issues no navigate call to login
  - No imperative navigation is declared on the screen (navigation carries only the reactive note)

One authority for "am I signed in" rather than two. A screen that also navigates imperatively
would race the observer and can strand the app between graphs.

---

## TC-PROF-010 — Error state renders the full-screen failure with Retry

**Priority:** high · **State:** error

- **Given** The profile load fails with HTTP 500 (`NETWORK_ERROR`)
- **When** Screen mounts
- **Then**
  - `profile_error_icon` (`error_outline`, `error` colour) visible
  - `profile_error_title` "Could not load your profile" visible as a heading
  - `profile_error_body` "Check your connection and try again." visible
  - `profile_error_retry_button` visible
  - Avatar, form and logout controls **NOT** rendered

Logout is unreachable in the error state. That is the wrong control to withhold on failure — it
needs no network and it is the one thing a customer with a broken session may urgently want.

---

## TC-PROF-011 — 401 surfaces the same user-facing error message

**Priority:** medium · **State:** error

- **Given** The profile load fails with HTTP 401 (`AUTH_ERROR`)
- **When** Screen mounts
- **Then**
  - `ui_message` "Could not load your profile" is shown
  - `ScreenState.Error` carries `isNetworkError` so the ViewModel can distinguish the cause

The state distinguishes the cause and the UI does not act on it. A 401 means the session is gone —
the screen could route to login (as TC-PROF-009's observer does on logout) instead of offering a
retry that will 401 again.

---

## TC-PROF-012 — Retry re-fetches the profile

**Priority:** high · **State:** error

- **Given** Error state is displayed
- **When** User taps `profile_error_retry_button` (`retry`)
- **Then**
  - `ProfileViewModel.onRetry()` calls `load()`
  - State transitions error → loading → content on a successful re-fetch
  - The call reads from `party` via ktorfit

---

## TC-PROF-013 — The screen writes nothing, and has no write endpoint to call

**Priority:** medium · **State:** content

- **Given** a network interceptor recording all outbound requests
- **When** Every interaction on the screen is exercised
- **Then**
  - No write request is issued by any control on the screen
  - The only side effect of any control is the local session clear in TC-PROF-008

> Rebased 2026-08-07. This previously read: "`ProfileApi` exposes `updateCurrentUser`
> (`PUT /obp/v4.0.0/users/current`) … `obp_update_user_profile` is never invoked — it is declared
> for contract completeness only". That endpoint was struck from `api.yaml` on 2026-08-06 and has
> **no OBIE counterpart**: party data is read-only, so there is no write side left to defer. The
> scenario survives because the guarantee it protects — this screen never writes — is still worth
> asserting; it is simply no longer a statement about an unused declared endpoint.

---

## Traceability

| Control | Scenario | Reachable |
|---------|----------|:---------:|
| `profile_avatar_edit_icon` | TC-PROF-006 | no (decorative) |
| `profile_change_password_button` | TC-PROF-007 | no (disabled) |
| `profile_logout_button` | TC-PROF-008, -009 | yes |
| `profile_error_retry_button` | TC-PROF-012 | yes (error state only) |

Two of the four controls on the content state do nothing. Logout is the only working action.

---

_Generated by /idea-feature-test-export | 2026-08-04_
