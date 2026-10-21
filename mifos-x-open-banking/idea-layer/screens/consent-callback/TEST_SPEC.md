# TEST SPEC — Consent Callback

| Field      | Value                                  |
|------------|----------------------------------------|
| Feature    | consent-callback                       |
| Source     | `screens/consent-callback/tests.yaml`  |
| Scenarios  | 6                                      |
| Priorities | high 5 · medium 1                      |
| States     | loading · content · awaiting · error · access_denied · security_error |
| Module     | `feature/consent-callback`             |

---

## Coverage

Six declared states, six scenarios — **1:1, complete**. That matters more here than on most
screens: this is the app's security boundary, and every state it can reach on an untrusted
external redirect has a covering test.

| State          | Scenario       | Token exchange attempted? |
|----------------|----------------|---------------------------|
| loading        | TC-CALLBACK-001 | in flight |
| content        | TC-CALLBACK-002 | yes, succeeded |
| awaiting       | TC-CALLBACK-003 | yes, consent not yet authorised |
| error          | TC-CALLBACK-004 | yes, failed |
| access_denied  | TC-CALLBACK-005 | **no** |
| security_error | TC-CALLBACK-006 | **no** |

The last column is the security contract. Two scenarios assert a request is **not** made.

---

## TC-CALLBACK-001 — Loading state shown during auth-code exchange and consent-status poll

**Priority:** high · **State:** loading

- **Given** Deep-link callback received with valid auth code and matching state param; exchange in flight
- **When** Screen mounts and `exchange_and_verify` is triggered
- **Then**
  - Circular progress indicator visible in `loading_layout` stack
  - `{strings.consent_callback_loading_title}` headline visible
  - `{strings.consent_callback_loading_body}` body text visible
  - `success_layout`, `awaiting_state`, `error_state`, `access_denied_state`, `security_error_state` all hidden

---

## TC-CALLBACK-002 — Success state shown when consent confirmed Authorised; auto-navigates to accounts after 1.5 s

**Priority:** high · **State:** content

- **Given** Auth code exchanged successfully; consent-status returns `Status: Authorised`
- **When** `exchange_and_verify` completes with `Authorised` status
- **Then**
  - `check_circle` icon in `primary` colour visible in `success_layout`
  - `{strings.consent_callback_success_title}` headline visible
  - `{strings.consent_callback_success_body}` body text visible
  - App navigates to `accounts` after a 1.5 s delay
  - `loading_layout` hidden

---

## TC-CALLBACK-003 — Awaiting state shown when consent still AwaitingAuthorisation after exchange

**Priority:** medium · **State:** awaiting

- **Given** Token exchange succeeded but HSBC consent-status still returns `AwaitingAuthorisation`
- **When** `exchange_and_verify` completes with an `AwaitingAuthorisation` consent status
- **Then**
  - `{strings.consent_callback_poll_again}` button visible and enabled
  - Tapping "Check again" retriggers the `poll_consent_status` action

Covers the real gap between portal authorisation and consent activation — the bank may still be
settling when the redirect returns.

---

## TC-CALLBACK-004 — Error state shown on PSU rejection or token exchange failure

**Priority:** high · **State:** error

- **Given** HSBC returns `Rejected` consent status **or** token exchange returns HTTP 400
- **When** `exchange_and_verify` fails
- **Then**
  - `cancel` icon visible in `error_state`
  - `{strings.consent_callback_error_title}` title visible
  - `{strings.consent_callback_error_body}` body text visible
  - `{strings.consent_callback_retry}` button visible and enabled
  - Tapping "Try again" navigates to the login screen
  - `LocalStorage.clearOAuthState()` and `clearConsentId()` side-effects invoked

The cleanup assertions matter: a failed exchange must not leave a stale `state` or consent id
behind for the next attempt to pick up.

---

## TC-CALLBACK-005 — Access denied state shown when HSBC redirect carries error=access_denied

**Priority:** high · **State:** access_denied

- **Given** Deep-link URI arrives with `error=access_denied&state={valid_state}` — PSU denied at the HSBC portal
- **When** `check_oauth_error` trigger fires and classifies the error as `access_denied`
- **Then**
  - `block` icon visible in `access_denied_state`
  - `{strings.consent_callback_denied_title}` title visible
  - `{strings.consent_callback_denied_body}` body text visible
  - `{strings.consent_callback_denied_cta}` outlined button visible
  - **Token exchange NOT attempted** (`exchange_and_verify` not triggered)
  - Tapping "Start over" navigates to the login screen

Declining consent is a legitimate customer choice, rendered as its own state rather than an
error — and no exchange is attempted, because there is no code to exchange.

---

## TC-CALLBACK-006 — Security error state shown when FAPI state parameter or id_token nonce does not match

**Priority:** high · **State:** security_error

- **Given** Deep-link URI arrives with a `state` param or `id_token` nonce that does not match `local_storage.oauth_state` / `local_storage.oauth_nonce`
- **When** `validate_state_param` trigger fires and detects a mismatch
- **Then**
  - `security` icon visible in `security_error_state`
  - `{strings.consent_callback_security_error_title}` title visible
  - `{strings.consent_callback_security_error_body}` body text visible
  - `{strings.consent_callback_security_cta}` filled button visible
  - **Token exchange NOT attempted** (`short_circuit_on_mismatch=true`)
  - Tapping "Start again" triggers `LocalStorage.clearAll()` and `TokenStore.revokeAll()`, then navigates to login

The most important scenario in the feature. A `state`/nonce mismatch is a possible CSRF or
token-substitution attempt, so the assertion is that validation **short-circuits before** any
exchange, and that recovery wipes all local auth material rather than reusing it.

---

## Traceability

| Security invariant | Pinned by |
|--------------------|-----------|
| No exchange on `state`/nonce mismatch | TC-CALLBACK-006 |
| No exchange on OAuth error redirect | TC-CALLBACK-005 |
| OAuth state cleared after failure | TC-CALLBACK-004 |
| Full credential wipe after a security event | TC-CALLBACK-006 |

---

_Generated by /idea-feature-test-export | 2026-08-03_
