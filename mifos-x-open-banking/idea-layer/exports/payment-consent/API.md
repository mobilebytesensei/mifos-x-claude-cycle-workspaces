# payment-consent — API Contracts

> Generated from `screens/payment-consent/api.yaml` by `/idea-feature-export`
> Schema version: 4.0
> api_source_ref: API-003
> Endpoints: 2
> DTOs: ObTokenResponse, ObPaymentStatus
> base_path: `/obie/open-banking/v4.0/pisp`

---

## Host Split (Critical)

Two different hosts are used. **NEVER derive one from the other by string manipulation.**

| Role | Host | Used by |
|---|---|---|
| Authorise | `sandbox.ob.hsbc.co.uk` | `oauth2/authorize` (browser leg only — NOT an API call this screen makes) |
| Resource | `secure.sandbox.ob.hsbc.co.uk` | `exchange_authorization_code`, `get_consent_status`, all consent-staging calls |

**Failure mode**: Sending the PSU to the resource host produces a consent stuck at `AWAU` until the poll deadline — indistinguishable from abandonment.

**Authorise URL construction**: The consent-staging response carries NO authorisation link. `Links` holds only `Self`; `Meta` holds only `TotalPages`. The app constructs the `oauth2/authorize` URL from the `ConsentId` itself. Confirmed on VRP; treated as the general shape across all seven families.

---

## Endpoint Summary

| # | ID | Method | Path | Auth | Host |
|---|---|---|---|---|---|
| 1 | `exchange_authorization_code` | POST | `/v1.1/oauth2/token` | `private_key_jwt` | `secure.sandbox.ob.hsbc.co.uk` |
| 2 | `get_consent_status` | GET | `/{familyConsentPath}/{consentId}` | `client_credentials_payments_scope` | `secure.sandbox.ob.hsbc.co.uk` |

---

## Endpoint Details

### 1. `exchange_authorization_code` — Spend the authorisation code for a PSU access token

| Attribute | Value |
|---|---|
| ID | `exchange_authorization_code` |
| Method | POST |
| Path | `/v1.1/oauth2/token` |
| Host | `secure.sandbox.ob.hsbc.co.uk` |
| Auth | `private_key_jwt` client assertion (`client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer`) |
| Grant type | `authorization_code` |
| Scope | `payments` |
| Cache | none |
| Pagination | none |

#### Ordering Rule (Critical)

Both the `state` check and the `nonce` check (from `id_token`) MUST run **before** the code is spent. An authorisation code is single-use; validating after exchange leaves nothing to retry with.

The exchange MUST be the **very first action** after the state check passes — no analytics call, no persistence write, no navigation animation in front of it. Codes were lost twice in the corpus by doing other work first.

#### No-Recovery Rule (Critical)

A spent or expired code has NO recovery path. The consent it belongs to has already reached `AUTH` and **cannot be re-sent through the authorise leg** — the sandbox rejects the attempt. The only recovery is staging a FRESH consent from the originating type screen.

#### Request Parameters

| Param | Type | Required | Description |
|---|---|:---:|---|
| `grant_type` | `String` | Yes | Always `"authorization_code"` |
| `code` | `String` | Yes | The authorisation code returned by HSBC in the redirect |
| `redirect_uri` | `String` | Yes | Must match exactly: `https://thekalpeshpawar.github.io/obp-callback/callback/` |
| `client_assertion_type` | `String` | Yes | `"urn:ietf:params:oauth:client-assertion-type:jwt-bearer"` |
| `client_assertion` | `String` | Yes | A signed `private_key_jwt` — self-signed JWT using the TPP signing key |

#### Response Schema

**Returns type**: `ObTokenResponse` (flat RFC 6749 JSON — NOT the OBIE `Data/Risk/Links/Meta` envelope)

```yaml
access_token:
  type: string
  required: true
  description: >
    PSU token. Required by funds-confirmation and by payment submission on every family.
    The client-credentials token is refused for those operations.
  observed_prefix: "pmt."
  redaction: NEVER log, capture, or emit to analytics. Redact to length only.

token_type:
  type: string
  required: true
  const: "Bearer"

expires_in:
  type: integer
  required: true
  description: >
    Observed 299s on PIS authorise legs; 3599s on AIS. Build to 299 — a 299s budget
    must cover both funds-confirmation AND submit before the token expires.

scope:
  type: string
  required: true
  observed: "openid payments"

id_token:
  type: string
  required: true
  description: >
    Carries the nonce that is validated IMMEDIATELY after exchange (before any other action).
    If nonce mismatches, discard the token.
  redaction: NEVER log or capture.

refresh_token:
  type: string
  required: false
  description: >
    Returned on the VRP leg only. Absent on the six single-use PIS families — their consent
    reaches COND after one payment, so there is nothing to refresh.
  redaction: NEVER log or capture.
```

#### Error Matrix

| Code | When | Retry | User message key | Recovery UI |
|---|---|:---:|---|---|
| `400 invalid_grant` | Code spent, expired, or `redirect_uri` mismatch | No | `strings.error.payment_consent.code_expired` | "Restart authorisation" CTA — stages a NEW consent from the originating screen |
| `401 invalid_client` | `client_assertion` rejected (signing-key, `kid`, or `aud` fault) | No | `strings.error.payment_consent.network_error` | Abandon — not a PSU fault; TPP configuration issue |

---

### 2. `get_consent_status` — Poll the originating family's consent endpoint until AUTH

| Attribute | Value |
|---|---|
| ID | `get_consent_status` |
| Method | GET |
| Path template | `/{familyConsentPath}/{consentId}` |
| Full base path | `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp/{familyConsentPath}/{consentId}` |
| Auth | `client_credentials_payments_scope` (background token; no PSU credential) |
| Polled to | `AUTH` |
| Interval | 2 000ms, backoff ×1.5, max interval 15 000ms, max duration 180 000ms |
| Cache | none |
| Pagination | none |

#### Family Resolution — Path Table

| `paymentFamily` nav param | Resolved `familyConsentPath` |
|---|---|
| `domestic-payment` | `domestic-payment-consents` |
| `domestic-scheduled-payment` | `domestic-scheduled-payment-consents` |
| `domestic-standing-order` | `domestic-standing-order-consents` |
| `international-payment` | `international-payment-consents` |
| `international-scheduled-payment` | `international-scheduled-payment-consents` |
| `international-standing-order` | `international-standing-order-consents` |
| `domestic-vrp` | `domestic-vrp-consents` |

**Invariant**: The path MUST be resolved from the `paymentFamily` nav param, never hardcoded. A hardcoded `domestic-payment-consents` silently polls the wrong resource for six of the seven families and never observes `AUTH`.

#### Request Parameters

| Param | Type | Required | Source | Description |
|---|---|:---:|---|---|
| `consentId` | `String` | Yes | `SavedStateHandle` (nav param) | Short sequential integer-as-string — e.g. `"812774903"`. Never a UUID. |
| `paymentFamily` | `PaymentFamily` (enum) | Yes | `SavedStateHandle` (nav param) | Drives path resolution via the table above |

#### Response Schema

**Returns type**: `ObPaymentStatus` (OBIE envelope — `Data` + `Risk` + `Links` + `Meta`)

```yaml
Data.ConsentId:
  type: string
  required: true
  description: Echoes the nav param. Short sequential integer-as-string — enumerable, not a secret.

Data.Status:
  type: enum [AWAU, AUTH, COND, RJCT]
  required: true
  description: >
    THE ONLY FIELD THIS POLL READS. Stop when AUTH or RJCT. See critical note below.
  ladder:
    six_pis_families: "AWAU -> AUTH, then COND after first payment submission"
    vrp: "AWAU -> AUTH and stays AUTH forever — VRP consent is never COND"
    rejected: "RJCT — PSU denied at the bank. Observed on consent 45121."

Data.StatusUpdateDateTime:
  type: datetime (ISO 8601)
  required: true
  description: >
    PRESENT BUT INERT. Equals CreationDateTime even after AWAU -> AUTH. All five
    authorised consents in the corpus transitioned with it unchanged. NEVER poll on
    this field — a timestamp-keyed poll spins to the deadline on every payment.

Data.CreationDateTime:
  type: datetime (ISO 8601)
  required: true

Data.Initiation:
  type: object
  required: true
  description: >
    Authoritative ONLY after AUTH. Where the TPP omitted DebtorAccount, the bank
    OVERWRITES it with the PSU's picker choice and enriches it with a Name. The staged
    Initiation and the authorised Initiation are not the same document. Hand the
    authorised copy back with the consentId — the originating screen must submit what
    the bank holds, not its own staged copy.

Data.Permission:
  type: string
  required: false
  description: "Present on scheduled and standing-order families only. Always 'Create'."

Data.Charges:
  type: array
  required: false
  description: >
    Domestic families only. Always a single 0.05 GBP entry typed UK.OBIE.CHAPSOut with
    ChargeBearer BorneByDebtor. ABSENT from every international consent — the international
    fee is not disclosable before the PSU authorises.

Data.CutOffDateTime:
  type: datetime (ISO 8601)
  required: false
  description: "Domestic consents only. Undocumented by HSBC but consistently returned."

Data.ExpectedExecutionDateTime:
  type: datetime (ISO 8601)
  required: false
  description: "Domestic only. Equals CreationDateTime at staging."

Data.ExpectedSettlementDateTime:
  type: datetime (ISO 8601)
  required: false
  description: "Domestic only. Equals CreationDateTime at staging."

Risk:
  type: object
  required: true

Links.Self:
  type: string (URI)
  required: true
  description: >
    THE ONLY Links member. There is no authorisation href, no redirect link.
    The authorise URL is app-constructed from the ConsentId — not read from here.

Meta.TotalPages:
  type: integer
  required: true
  observed: 1
```

**Absent fields rule**: `ExchangeRateInformation` is NEVER present at any status on any family. It is refused on write with `U005` and never emitted on read. Do NOT render an FX rate on this screen or on the screen that called it.

#### Poll Stop Conditions

| Signal | Field | Action |
|---|---|---|
| `Data.Status == "AUTH"` | `Data.Status` | Emit `PaymentConsentEvent.Authorised` with `consentId`, `psuToken`, and `Data.Initiation` |
| `Data.Status == "RJCT"` | `Data.Status` | `Error(ConsentRejected)` — PSU denied at the bank |
| Deadline (180 000ms) reached | poll timer | `Error(AuthorisationTimedOut)` — non-terminal; PSU may still be authenticating |

**AUTH is not payability**: `AUTH` means the PSU approved the consent — it does NOT mean the payment can succeed. A credit-card VRP consent reaches `AUTH`, passes funds-confirmation, and then refuses every payment with `U021`. No field on the consent signals this. Hand-back on `AUTH` is still correct because no better signal exists; the defence is the type screens' debtor pre-filter (FR-018). No compensating check belongs on this screen.

#### Error Matrix

| Code | When | Retry | User message key | Recovery UI |
|---|---|:---:|---|---|
| `400 U009` | Read against a consent in a status the operation does not allow | No | `strings.error.payment_consent.network_error` | Abandon |
| `400 U011` | Resource not found — VRP-only after consent `DELETE` | No | `strings.error.payment_consent.network_error` | Abandon |
| `IOException / timeout` | Network failure during poll | Yes (idempotent read) | `strings.error.payment_consent.network_error` | Restart CTA |
| Poll deadline reached | 180 000ms with `Data.Status` still `AWAU` | Manual | `strings.error.payment_consent.timed_out` | "Check again" CTA |

---

## DTO Definitions

### DTO: `ObTokenResponse`

```kotlin
@Serializable
data class ObTokenResponse(
    val access_token: String,
    val token_type: String,
    val expires_in: Int,
    val scope: String,
    val id_token: String,
    val refresh_token: String? = null,
)
```

| Field | Type | Nullable | Description |
|---|---|:---:|---|
| `access_token` | `String` | No | PSU payment-scope token; NEVER persisted to `ConsentSession` |
| `token_type` | `String` | No | Always `"Bearer"` |
| `expires_in` | `Int` | No | Observed 299s on PIS legs; build to this shorter figure |
| `scope` | `String` | No | Observed `"openid payments"` |
| `id_token` | `String` | No | Carries `nonce`; validated immediately after exchange |
| `refresh_token` | `String?` | Yes | VRP only; absent on six single-use PIS families |

### DTO: `ObPaymentStatus`

```kotlin
@Serializable
data class ObPaymentStatus(
    val Data: PaymentStatusData,
    val Risk: JsonObject,
    val Links: StatusLinks,
    val Meta: StatusMeta,
)

@Serializable
data class PaymentStatusData(
    val ConsentId: String,
    val Status: String,                              // poll reads ONLY this field
    val CreationDateTime: String,
    val StatusUpdateDateTime: String,               // INERT — never poll on this
    val Initiation: JsonObject? = null,             // present and authoritative after AUTH
    val Permission: String? = null,
    val Charges: List<JsonObject>? = null,
    val CutOffDateTime: String? = null,
    val ExpectedExecutionDateTime: String? = null,
    val ExpectedSettlementDateTime: String? = null,
)

@Serializable
data class StatusLinks(val Self: String)

@Serializable
data class StatusMeta(val TotalPages: Int)
```

---

## Security Rules

| Rule | Detail |
|---|---|
| Token isolation | `access_token` and `refresh_token` MUST NOT be written to `ConsentSession` |
| Token redaction | `access_token`, `refresh_token`, `id_token` MUST NOT appear in logs, crash reports, analytics, or capture artefacts |
| ConsentId privacy | `ConsentId` is enumerable (short integer). MUST NOT appear in URLs, logs, share sheets, or crash reports |
| State check first | `state` check runs before the code is spent; a mismatch aborts without spending the code |
| Nonce check next | `nonce` check from `id_token` runs immediately after exchange; mismatch discards the token |
| Exchange first | Zero analytics, persistence, or navigation work between receiving the redirect and issuing `POST /oauth2/token` |
| No re-authorisation | A consent that has reached `AUTH` cannot be re-sent through the authorise leg. Recovery = stage a NEW consent |

---

## Cross-Feature API Usage

| Endpoint | Also Used By |
|---|---|
| `POST /v1.1/oauth2/token` (`authorization_code`) | `consent-callback` (AIS scope — `openid accounts`; different scope, same token endpoint shape) |
| `GET /{familyPath}/{consentId}` | Each of the seven originating type screens may read the same endpoint after submit to confirm the final status |
