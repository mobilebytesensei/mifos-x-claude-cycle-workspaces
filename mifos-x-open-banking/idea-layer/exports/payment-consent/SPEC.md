# payment-consent — Feature Specification

> Generated from `screens/payment-consent/*.yaml` by `/idea-feature-export`
> Schema version: 4.0
> Contract version: 2.0.0
> Quality score: 90/100
> Endpoints: 2 · DTOs: 2 (ObTokenResponse, ObPaymentStatus) · Components: 7 · Test scenarios: 11

---

## Lossless Export Contract

This SPEC is the single input for `/kmp-viewmodel-gen`, `/kmp-screen-gen`, and `/verify --tests`.

- **State Defaults** — initial values per state field declared in §3
- **Error Matrix** — endpoint × error-code × (retry, user message, recovery) in §5
- **Nav Origins** — hand-back is an event, not a nav call; originator handles routing
- **Token Isolation Invariant** — the payment-scope token MUST NOT be written to `ConsentSession`

---

## 1. Overview

The shared app-to-app authorise return leg for all seven payment families. It is headless: it validates the redirect (`state` + `nonce` checks before the code is spent), exchanges the authorisation code for a PSU access token, polls the originating family's consent-status endpoint until `AUTH`, then emits an event so the originating type screen can submit the payment.

There is no UI chrome beyond a progress indicator, a per-step description, and terminal states (authorised / error). This screen never navigates to Home.

| Attribute | Value |
|---|---|
| Feature ID | `payment-consent` |
| Cluster | `payment-initiation` |
| Flow | `payment-initiation` (shared leg across seven rails) |
| Status | `enriched` (revalidation owed — approval predates the 2026-08-06 seven-type rewrite) |
| Quality Score | 90/100 |
| Capability Tags | `rest-client`, `oauth-callback`, `error-recovery` |
| Dependency Tier | `feature` |
| spec_ahead_of_source | true — no feature module exists yet; `mirror_when_implemented: feature/consent-callback` |

### Why This Is a Separate Feature from consent-callback

- `consent-callback` is AIS scope (`openid accounts`), persists the PSU token to `ConsentSession`, and re-routes to Home on success.
- `payment-consent` is PISP scope (`payments`), must NOT overwrite `ConsentSession`, and returns to the originating type screen via event.
- The consent-status poll is load-bearing here: submitting against a non-Authorised consent returns `400 U009`.

---

## 2. Screens

| # | Screen | ViewModel | States | Description |
|---|---|---|---|---|
| 1 | `payment-consent` | `PaymentConsentViewModel` | validating, exchanging, checking, authorised, error | Headless OAuth return leg; shows progress per step and terminal result |

### Screen Relationships

Single-screen feature. Entry is via the per-platform `ConsentRedirectBus` (already shipped for AIS consent-callback). Exit is via `PaymentConsentEvent` — three members: `Authorised`, `RestartAuthorisation`, `Abandoned`.

### State Role Mapping

The canonical `loading / content / empty / error` roles map as follows (deliberate departure from defaults — three distinct waiting phases fail differently and render separate previews):

| Canonical Role | Mapped States |
|---|---|
| `loading` | `validating`, `exchanging`, `checking` |
| `content` | `authorised` |
| `error` | `error` |
| `empty` | n/a — no collection is rendered |

---

## 3. State Model

### PaymentConsentViewModel

#### State: `PaymentConsentState`

| Field | Type | Default | Nullable | Purpose |
|---|---|---|:---:|---|
| `uiState` | `PaymentConsentUiState` | `Validating` | No | Current leg of the authorisation |
| `consentId` | `String` | — (from `SavedStateHandle`) | No | Echoes the nav param; keys all API calls |

#### State Defaults (for `/kmp-viewmodel-gen` initial-value emission)

```kotlin
val initial = PaymentConsentState(
    uiState = PaymentConsentUiState.Validating,
    consentId = savedStateHandle.get<String>("consentId") ?: error("consentId required"),
)
```

#### Screen State: `PaymentConsentUiState`

```kotlin
sealed interface PaymentConsentUiState {
    data object Validating : PaymentConsentUiState   // checking state/nonce against PendingAuthStore
    data object Exchanging : PaymentConsentUiState   // spending the authorisation code
    data object Checking   : PaymentConsentUiState   // polling consent status until AUTH
    data object Authorised : PaymentConsentUiState   // consentId + payment-scoped token ready
    data class  Error(
        val type: PaymentConsentErrorKind,
        val message: String,
    ) : PaymentConsentUiState
}
```

#### Errors: `PaymentConsentErrorKind`

| Type | Retry | Display | Recovery | Message Key |
|---|:---:|---|---|---|
| `StateMismatch` | No | Error state, no restart CTA | Abandon — possible CSRF | `strings.error.payment_consent.state_mismatch` |
| `NoPendingAuthorisation` | No | Error state, no restart CTA | Return to originating screen | `strings.error.payment_consent.no_pending` |
| `CodeExpired` | via restart | Error state, Restart CTA | Stage a NEW consent — the lost code is unrecoverable and the existing consent CANNOT be re-authorised | `strings.error.payment_consent.code_expired` |
| `ConsentRejected` | No | Error state, no restart CTA | Return to originating screen, offer a new payment | `strings.error.payment_consent.rejected` |
| `AuthorisationTimedOut` | via restart | Error state, Restart CTA | Manual retry or stage a NEW consent | `strings.error.payment_consent.timed_out` |
| `NetworkError` | via restart | Error state, Restart CTA | Retry — safe, no payment submitted | `strings.error.payment_consent.network_error` |

**Restartable types**: `CodeExpired`, `AuthorisationTimedOut`, `NetworkError`. The restart CTA is visible only when `error.type` is in this set.

#### Events: `PaymentConsentEvent`

| Event | Params | Trigger |
|---|---|---|
| `Authorised` | `consentId: String`, `psuToken: String`, `authorisedInitiation: Initiation` | `Data.Status == AUTH`; carries the AUTHORISED consent's `Initiation` (bank may have overwritten `DebtorAccount`) |
| `RestartAuthorisation` | (none — no consentId, by design) | `retry_authorisation` action; originator must stage a FRESH consent |
| `Abandoned` | (none) | `abandon_payment` action; staged consent left to expire |

#### Actions: `PaymentConsentActions`

| Action | Params | User Trigger |
|---|---|---|
| `ValidateRedirect` | `state: String, code: String` | On mount — first action |
| `ExchangeCode` | `code: String` | Immediately after state/nonce validation passes |
| `PollConsentStatus` | `consentId: String` | After successful token exchange |
| `CheckAgain` | (none) | "Check again" button visible in `Checking` state |
| `RetryAuthorisation` | (none) | "Restart authorisation" button visible in restartable error states |
| `AbandonPayment` | (none) | "Abandon payment" button visible in all error states |

#### DI (Constructor Injection)

- `SavedStateHandle` — supplies `consentId` and `paymentFamily` nav params
- `PaymentConsentRepository` — wraps token exchange + consent-status polling
- `PendingAuthStore` — single-use read/consume of pending `state`/`nonce`/`consentId`; already shipped for AIS consent-callback

---

## 4. Navigation

### Entry Points

| Source | Trigger | Params |
|---|---|---|
| Any of the seven originating type screens | Deep link via per-platform `ConsentRedirectBus` — HSBC redirects back after PSU SCA | `consentId: String` (required), `paymentFamily: PaymentFamily` (required), `code: String` (from redirect), `state: String` (from redirect) |

**Host note**: The authorise leg runs on `sandbox.ob.hsbc.co.uk` (NOT the resource host `secure.sandbox.ob.hsbc.co.uk`). These are different constants — never derive one from the other.

### Seven Originating Screens

| Screen | Rail |
|---|---|
| `pay-domestic-single` | Domestic single immediate payment |
| `pay-domestic-scheduled` | Domestic scheduled payment |
| `pay-domestic-standing-order` | Domestic standing order |
| `pay-international-single` | International single immediate payment |
| `pay-international-scheduled` | International scheduled payment |
| `pay-international-standing-order` | International standing order |
| `pay-vrp-mandate` | Domestic VRP mandate |

### Outgoing Navigation (via Event)

| Event | Destination | Condition | Notes |
|---|---|---|---|
| `PaymentConsentEvent.Authorised` | `{originating type screen}` | `Data.Status == AUTH` | Returns event, not a nav call; originator retains idempotency key and submits using the AUTHORISED consent's `Initiation` |
| `PaymentConsentEvent.RestartAuthorisation` | `{originating type screen}` | `error.type in {CodeExpired, AuthorisationTimedOut, NetworkError}` | Originator MUST stage a fresh consent — NOT relaunch the existing one |
| `PaymentConsentEvent.Abandoned` | `{originating type screen}` | Any `abandon_payment` action | Staged consent left to expire; no revocation call |

### Nav Params

| Param | Type | Required | Source |
|---|---|:---:|---|
| `consentId` | `String` | Yes | Originating screen when it launches the bank authorise URL |
| `paymentFamily` | `PaymentFamily` (enum) | Yes | Originating screen; selects which consent-status endpoint to poll |

### Route Definition

- **Route**: `PaymentConsentRoute`
- **Params**: `consentId: String` (required), `paymentFamily: PaymentFamily` (required)
- **Entry mechanism**: `ConsentRedirectBus` deep link — not a standard navigation call

### Hand-Back Contract

On `PaymentConsentEvent.Authorised`, the originator receives:
1. `consentId` — the consent that reached `AUTH`
2. `psuToken` — the payment-scoped PSU access token (never written to `ConsentSession`)
3. `authorisedInitiation` — the `Initiation` block as returned by the AUTHORISED consent read

The originator MUST submit using `authorisedInitiation`, not its locally staged copy. Where the TPP omitted `DebtorAccount`, the bank overwrites it with the PSU's picker choice and enriches it with a `Name`; echoing the staged copy returns `U008`.

---

## 5. API Dependencies

| # | Endpoint | Method | Auth | Host | Cache | Offline |
|---|---|---|---|---|---|---|
| 1 | `exchange_authorization_code` | `POST /v1.1/oauth2/token` | `private_key_jwt` | `secure.sandbox.ob.hsbc.co.uk` | none | none |
| 2 | `get_consent_status` | `GET /{familyConsentPath}/{consentId}` | `client_credentials_payments_scope` | `secure.sandbox.ob.hsbc.co.uk` | none | none |

### Error Matrix

| Endpoint | Code | When | Retry | i18n Key | Recovery UI |
|---|---|---|:---:|---|---|
| `exchange_authorization_code` | `400 invalid_grant` | Code spent, expired, or redirect_uri mismatch | No | `code_expired` | Restart CTA (stage NEW consent) |
| `exchange_authorization_code` | `401 invalid_client` | `client_assertion` rejected — signing-key, kid or aud fault | No | `network_error` (generic) | Abandon |
| `get_consent_status` | `400 U009` | Consent not in a status that allows reads | No | `network_error` | Abandon |
| `get_consent_status` | `400 U011` | Resource not found — VRP-only after consent `DELETE` | No | `network_error` | Abandon |
| Both | `IOException / timeout` | Network failure | Yes | `network_error` | Restart CTA |

### Family Resolution — `get_consent_status` Path

| `paymentFamily` param | Resolved path segment |
|---|---|
| `domestic-payment` | `domestic-payment-consents` |
| `domestic-scheduled-payment` | `domestic-scheduled-payment-consents` |
| `domestic-standing-order` | `domestic-standing-order-consents` |
| `international-payment` | `international-payment-consents` |
| `international-scheduled-payment` | `international-scheduled-payment-consents` |
| `international-standing-order` | `international-standing-order-consents` |
| `domestic-vrp` | `domestic-vrp-consents` |

Full path: `GET /obie/open-banking/v4.0/pisp/{resolved-segment}/{consentId}`

---

## 6. Design Tokens Used

| Token | Value (light) | Used By |
|---|---|---|
| `colors.surface` | `#F7F9FF` | Screen background |
| `colors.primary` | `#266489` | Progress indicator (circular) |
| `colors.on_surface` | `#181C20` | Progress detail text |
| `colors.on_surface_variant` | `#41474D` | Secondary / supporting text |
| `colors.error` | `#BA1A1A` | Error state icon and title |
| `colors.error_container` | `#FFDAD6` | Error state container |
| `colors.on_error_container` | `#93000A` | Error state text |
| `colors.primary_container` | `#C9E6FF` | Authorised state (success variant) container |
| `colors.on_primary_container` | `#004B6F` | Authorised state text |
| `semantic.status.success` → `primary` | `#C9E6FF` / `#004B6F` | `empty_state` variant `success` |
| `spacing.md` | 16dp | Screen padding |
| `spacing.lg` | 24dp | Inter-component gap |
| `radius.xl` | 28dp | Button corners |
| `radius.full` | 9999dp | Filled button (pill) |
| `icon.md` | 24dp | Inline icons |
| `icon.xl` | 48dp | State illustration icons |

---

## 7. Testing

| ID | Scenario | Priority | Description |
|---|---|:---:|---|
| TC-PCON-001 | State check before code exchange | P0 | `validate_and_exchange` invariant — state mismatch aborts before spending code |
| TC-PCON-002 | Token never written to ConsentSession | P0 | `token_isolation_invariant` — zero writes to `ConsentSession` |
| TC-PCON-003 | Family resolution | P0 | `family_resolution_invariant` — resolved path matches `paymentFamily` for all seven |
| TC-PCON-004 | Status field only | P0 | `status_field_only_invariant` — AUTH detected from `Data.Status`, not `StatusUpdateDateTime` |
| TC-PCON-005 | Timeout is non-terminal | P0 | `timeout_is_not_failure_invariant` — deadline yields retry state, not failure |
| TC-PCON-006 | Rejected is terminal | P1 | `rejected_is_terminal_invariant` — RJCT emits `Abandoned`, no resubmit offered |
| TC-PCON-007 | PendingAuthStore single-use | P1 | Second read returns null after `consume()` |
| TC-PCON-008 | Poll reaches AUTH | P1 | Sequence `[AWAU, AWAU, AUTH]` → `Authorised` event |
| TC-PCON-009 | Initiation read-back | P1 | `Authorised` event carries `authorisedInitiation` from AUTHORISED consent, not staged copy |
| TC-PCON-010 | Code exchange first | P1 | No analytics/persistence write between state-check and `POST /oauth2/token` |
| TC-PCON-011 | Restart emits no consentId | P1 | `RestartAuthorisation` event carries no `consentId` — originator must stage fresh |

**Test scenario count**: 11 (5 P0, 6 P1, 0 P2)

### Test File Mapping

| Test Class | Module | Scenarios Covered |
|---|---|---|
| `PaymentConsentViewModelTest` | `feature/payment-consent/src/commonTest` | TC-PCON-001..011 |
| `PendingAuthStoreTest` | `core/auth/src/commonTest` | TC-PCON-007 |

---

## 8. Edge Cases

| Scenario | Expected Behaviour |
|---|---|
| App restarted mid-authorisation | `PendingAuthStore.consume()` returns null → `NoPendingAuthorisation` error, return to originating screen |
| Consent already at AUTH when polled (very fast bank) | First poll returns `AUTH` immediately → `Authorised` event emitted without waiting for next interval |
| VRP mandate — token is longer-lived | Token still never written to `ConsentSession`; VRP consent stays `AUTH` forever (never reaches `COND`) |
| Credit-card VRP reaches AUTH but cannot pay | `Authorised` event emitted correctly — no compensating check here (no data for it); defence is upstream debtor pre-filter FR-018 |
| Multiple live consents on same family | Screen keys entirely off `consentId` nav param; no "current consent" resolution |
| ConsentId enumerable (short integer) | Never rendered in URL, log, crash report, or share sheet |

---

## 9. Feature Flags

(none — the full feature is under spec-ahead-of-source; no partial-rollout flag is defined)

---

## 10. Data Flow

| Screen | Trigger | Calls | Produces State | Error Paths |
|---|---|---|---|---|
| `payment-consent` | On mount | `PendingAuthStore.consume()` → local state/nonce check | `Validating` → `Exchanging` or `Error(StateMismatch)` | `StateMismatch`, `NoPendingAuthorisation` |
| `payment-consent` | After state match | `POST /v1.1/oauth2/token` | `Exchanging` → `Checking` | `CodeExpired`, `NetworkError` |
| `payment-consent` | After token received | `GET /{familyPath}/{consentId}` (polled every 2s → up to 15s backoff, 180s ceiling) | `Checking` → `Authorised` or `Error(ConsentRejected)` or `Error(AuthorisationTimedOut)` | `ConsentRejected`, `AuthorisationTimedOut`, `NetworkError` |
| `payment-consent` | `CheckAgain` action | `GET /{familyPath}/{consentId}` (single call) | `Checking` → `Authorised` or stays `Checking` | `NetworkError` |

### Side Effects

| Screen | Trigger | Kind | Target |
|---|---|---|---|
| `payment-consent` | `Authorised` state | emit event | `PaymentConsentEvent.Authorised(consentId, psuToken, authorisedInitiation)` |
| `payment-consent` | `RetryAuthorisation` action | emit event | `PaymentConsentEvent.RestartAuthorisation` |
| `payment-consent` | `AbandonPayment` action | emit event | `PaymentConsentEvent.Abandoned` |
| `payment-consent` | `PendingAuthStore.consume()` | local store mutation | Clears pending record (single-use) |

---

## 11. Referenced Journeys

Resolved against `idea-layer/journeys/*.yaml` — a journey is listed here only when this feature's
screen appears in that journey's `screen_sequence`.

| Journey | Name | Persona | Tier | Where this screen appears |
|---|---|---|---|---|
| `consumer-accounts-payments` | Consumer Accounts & Payments | returning consumer | maximum | Step 10 — "authorise the payment at the bank", between `pay-domestic-single` review and `payment-status` |

That step is flagged in the journey as the single largest drop-off risk in the flow: the PSU leaves
the app entirely and authenticates on HSBC's own site.

Only the domestic-single rail has a journey, so only one of this screen's seven originating rails is
exercised by any journey. The other six reach this screen in the spec but in no journey.

The row previously printed here named `payment-initiation` — that is a **flow** id
(`§1` Attributes, `Flow`), not a journey. It was listed under a journeys heading and described as
"entered from every one of the seven rail journeys"; there are no seven rail journeys. Corrected
2026-08-07.

---

## 12. DTOs Consumed

| DTO | Source | Kind |
|---|---|---|
| `ObTokenResponse` | `POST /v1.1/oauth2/token` response (RFC 6749 flat JSON, not OB envelope) | Response — `access_token`, `token_type`, `expires_in`, `scope`, `id_token`, `refresh_token?` |
| `ObPaymentStatus` | `GET /{familyPath}/{consentId}` response (`Data` + `Risk` + `Links` + `Meta` envelope) | Response — only `Data.Status` is polled; `Data.Initiation` is handed back on `Authorised` |

---

## 13. Dependencies

**Tier**: feature

| Dependency | Type | Required | Note |
|---|---|:---:|---|
| `{originating type screen}` (one of seven) | parent | Yes | Dynamic — never hardcoded; carries `consentId` and `paymentFamily` |
| `consent-list` | error-recovery | No | Offered on `ConsentRejected` as a path to review existing consents |
| `PendingAuthStore` | library (in-repo) | Yes | Already shipped for `consent-callback`; reused here |
| `ConsentRedirectBus` | library (in-repo, `cmp-navigation`) | Yes | Per-platform deep-link republisher; already shipped |
| `ktorfit` | REST client | Yes | `de.jensklingenberg.ktorfit:ktorfit-lib:2.x` |
