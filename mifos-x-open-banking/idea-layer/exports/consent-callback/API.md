# API — Authorisation Callback

Client contracts for `consent-callback`. This project owns no backend: these are Ktorfit contracts
against the HSBC UK/CE sandbox (OBIE Read/Write Standard, FAPI 1.0 Advanced), not owned schema.

Base URL: `https://api.hsbc.com/open-banking/v4.0`
Consumer: `ConsentCallbackRepository`.

The two calls run in sequence and **authenticate differently** — that distinction is the single
most important thing on this page.

---

## 1. fapi-token-exchange

| | |
|---|---|
| Endpoint | `POST /oauth2/token` |
| Requires auth | no — the request authenticates *itself* via `private_key_jwt` |
| Response DTO | `PsuTokenResponse` |

FAPI-1.0-Advanced `authorization_code` token exchange.

**Request body**

| Field                   | Value                                                        |
|-------------------------|--------------------------------------------------------------|
| `grant_type`            | `authorization_code`                                         |
| `code`                  | `{route_params.code}` — from the HSBC redirect               |
| `redirect_uri`          | `{registered_redirect_uri}` — must match the registered value |
| `client_assertion_type` | `urn:ietf:params:oauth:client-assertion-type:jwt-bearer`     |
| `client_assertion`      | `{private_key_jwt}`                                          |

**Returns:** `access_token` (the PSU bearer), `refresh_token`, `token_type=Bearer`, `expires_in`.
Stored in `EncryptedSharedPreferences`.

**Errors**

| Code | Cause | Maps to |
|------|-------|---------|
| 400 | Bad code, expired code, or `redirect_uri` mismatch | `error` state |
| 401 | `private_key_jwt` assertion invalid, or key not registered | `error` state |

A 401 here is a **TPP registration problem, not a customer problem** — the app's own key is wrong or
unregistered. It presents to the customer as a generic failure because there is nothing they can do
about it, but it should be read as an operational alert, not a user error.

---

## 2. consent-status

| | |
|---|---|
| Endpoint | `GET /account-access-consents/{ConsentId}` |
| Requires auth | yes — **`client_credentials`**, NOT the PSU bearer just obtained |
| Response DTO | `ConsentSummary` |
| Path param | `ConsentId: string` |

Called after the exchange to confirm the consent actually reached `Authorised`. Getting a token
back does not by itself mean the consent is live.

**Status → state mapping**

| `Data.Status`            | Condition           | Screen state     |
|--------------------------|---------------------|------------------|
| `Authorised`             | `success_condition` | `content`        |
| `AwaitingAuthorisation`  | `empty_condition`   | `awaiting`       |
| `Rejected` / `Revoked`   | `error_condition`   | `error`          |
| `Consumed`               | —                   | stale consent    |

`AwaitingAuthorisation` maps to `awaiting`, **not** to an error: HSBC may take a moment to update
status after the PSU authorises. The screen offers `poll_again_button` → `PollConsentStatus` rather
than restarting the whole flow, because the authorisation itself may well have succeeded.

**Errors**

| Code | Cause |
|------|-------|
| 401 | Client-credentials token invalid or expired |
| 404 | `ConsentId` not found — stale, or already consumed |

---

## Security: `state` / `nonce` mismatch

Not an HTTP error. Before either call is trusted, the `state` and `nonce` returned on the redirect
are compared against the values `ConsentSession` stored when the authorisation URL was built.

A mismatch means the callback did not originate from the authorisation this app started — a CSRF or
replay signal. It maps to `SecurityError` and **must not be retried silently**: recovery restarts
authorisation from a clean session, clearing `oauth_state` and `ConsentId`.

---

## `access_denied`

The redirect can carry `error=access_denied`, meaning the PSU declined at the HSBC portal. No call
is made. This is not a failure — the customer exercised a choice — and the UI reflects that with a
lower-urgency outlined CTA rather than an error-styled retry.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/consent-callback/api.yaml. -->
