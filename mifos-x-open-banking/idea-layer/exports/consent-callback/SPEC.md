# SPEC — Authorisation Callback

| Field         | Value                      |
|---------------|----------------------------|
| Feature       | consent-callback           |
| Flavor        | consumer                   |
| Status        | approved                   |
| Quality Score | 95                         |
| ViewModel     | ConsentCallbackViewModel   |
| Archetype     | empty_state                |

---

## Overview

The return leg of the FAPI redirect. HSBC sends the PSU back to the app's registered redirect URI
with an auth code; this screen exchanges that code for a PSU token, confirms the consent actually
reached `Authorised`, and moves the customer on.

It is a **transitional screen with no chrome** — no top app bar, no bottom navigation — because the
customer is mid-journey between HSBC and the app, and offering navigation here would let them
strand a half-completed authorisation.

Its six states exist because the return leg has six genuinely different outcomes, and three of them
are not errors in the ordinary sense:

- **Awaiting** — the exchange succeeded but HSBC has not yet flipped the consent to `Authorised`. Recoverable by polling, not by retrying the exchange.
- **AccessDenied** — the PSU actively declined at the bank. Nothing failed; they said no.
- **SecurityError** — the FAPI `state`/`nonce` did not match. This is a CSRF/replay signal and must never be retried silently.

---

## Screens

| ID               | Name                   | ViewModel                | Archetype   |
|------------------|------------------------|--------------------------|-------------|
| consent-callback | Authorisation Callback | ConsentCallbackViewModel | empty_state |

**Shell:** no top app bar, no bottom navigation, no FAB. Deliberately chrome-free.

---

## Components

| ID                     | Type              | Description                                          |
|------------------------|-------------------|-------------------------------------------------------|
| loading_layout         | stack             | Exchange-in-progress container                       |
| └ loading_spinner      | progress_circular | Token exchange running                               |
| └ loading_headline     | text              | Progress headline                                    |
| └ loading_body         | text              | Progress detail                                      |
| success_layout         | stack             | Authorised container                                 |
| └ success_icon         | icon              | Success glyph                                        |
| └ success_headline     | text              | Success headline                                     |
| └ success_body         | text              | Success detail                                       |
| awaiting_state         | empty_state       | Consent not yet `Authorised` at the bank             |
| └ poll_again_button    | button            | Re-checks status → `PollConsentStatus`               |
| error_state            | error_state       | Exchange or status failure — `role: alert`           |
| └ retry_button         | button            | `NavigateRetry` → login, clearing partial OAuth state |
| access_denied_state    | error_state       | PSU declined at HSBC (`error=access_denied`)         |
| └ denied_cta_button    | button            | Outlined — restart the consent flow voluntarily      |
| security_error_state   | error_state       | FAPI `state`/`nonce` mismatch (CSRF/replay)          |
| └ security_retry_button| button            | Restart authorisation from a clean session           |

`access_denied_state` uses an **outlined** CTA rather than a filled one: the customer made a
deliberate choice, so the restart affordance is offered at lower urgency rather than pushed.

---

## States

Initial state: `loading`. Six states, matching `ConsentCallbackUiState` one-for-one.

| State           | Meaning                                                              | Recovery |
|-----------------|-----------------------------------------------------------------------|----------|
| loading         | Token exchange in flight                                              | —        |
| awaiting        | Exchanged, but `Data.Status == AwaitingAuthorisation`                 | Poll again |
| content         | `Data.Status == Authorised` — success                                 | proceed  |
| access_denied   | PSU declined at the HSBC portal                                       | restart voluntarily |
| security_error  | FAPI `state`/`nonce` mismatch                                         | restart from clean session |
| error           | 400/401 on exchange, or `Status ∈ {Rejected, Revoked}`                | retry via login |

The split between `awaiting` and `error` is the important one: HSBC can take a moment to update
consent status after authorisation, so a not-yet-`Authorised` consent is a **timing** condition with
a poll affordance, not a failure.

---

## State Model

**ViewModel:** `ConsentCallbackViewModel`.

**State:** `ConsentCallbackState` — `uiState: ConsentCallbackUiState`, default `Loading`.

**Screen state:** sealed `ConsentCallbackUiState` — `Loading`, `Awaiting`, `Content`,
`AccessDenied`, `SecurityError`, `Error`.

**Actions:** `ProcessCallback`, `PollConsentStatus`, `NavigateRetry`, `NavigateLogin`.

**DI:** `ConsentCallbackRepository`, `ConsentSession`, `redirectUri`.

`ConsentSession` holds the `state`/`nonce` the authorisation was launched with — it is what makes
`SecurityError` detectable at all.

---

## Navigation

| From             | To     | Trigger                                       | Type    |
|------------------|--------|-----------------------------------------------|---------|
| consent-callback | login  | `NavigateRetry` — after failure, denial or security error | replace |

Entry is not a tap: the screen is reached by the HSBC authorisation redirect returning to the
registered `redirect_uri` with an auth code. It is reachable only via flow, never via a nav edge —
which is why orphan-screen checks must count flow reachability rather than nav edges alone.

Every recovery path routes back to `login` and **clears partial OAuth state** (`oauth_state`,
`ConsentId`) so the next attempt starts clean.

---

## API Endpoints

| ID                  | Endpoint                                    | Auth                | Purpose                               |
|---------------------|---------------------------------------------|---------------------|---------------------------------------|
| fapi-token-exchange | `POST /oauth2/token`                        | none (private_key_jwt assertion) | Auth code → PSU bearer token |
| consent-status      | `GET /account-access-consents/{ConsentId}`  | **client_credentials** | Confirm `Status == Authorised`     |

Base URL: `https://api.hsbc.com/open-banking/v4.0`.

Note the two calls authenticate differently — the status check uses the **client_credentials**
token, not the PSU bearer just obtained. Full request shape and status mapping: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto. The three failure surfaces are
differentiated by glyph and CTA emphasis rather than by colour alone — `error` for a genuine
failure, `block` for a deliberate denial, `security` for a state mismatch. Components reference
semantic roles, so both theme modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is
the canonical brand spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/consent-callback/{ui,api,flow,docs}.yaml. -->
