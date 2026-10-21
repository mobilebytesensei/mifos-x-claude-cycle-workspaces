# pay-domestic-single — API Contracts

> Generated from `screens/pay-domestic-single/api.yaml`
> Schema version: 4.0
> Contract version: 2.1.0
> Endpoints: 5
> Resource host: `https://secure.sandbox.ob.hsbc.co.uk`
> Base path: `/obie/open-banking/v4.0/pisp`
> Authorize host (browser leg only): `https://sandbox.ob.hsbc.co.uk/obie/open-banking/v1.1/oauth2/authorize`
> Auth: mTLS + `private_key_jwt` (PS256) + OAuth 2.0 authorization-code, FAPI 1.0 Advanced

---

## Endpoint Summary

| # | ID | Method | Full URL | Auth | x-jws-sig | x-idempotency-key |
|---|---|---|---|---|---|---|
| 1 | `stage_domestic_payment_consent` | POST | `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp/domestic-payment-consents` | `client_credentials_payments_scope` | Required | Required |
| 2 | `get_domestic_payment_consent_status` | GET | `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp/domestic-payment-consents/{ConsentId}` | `client_credentials_payments_scope` | Forbidden | Not required |
| 3 | `funds_confirmation` | GET | `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp/domestic-payment-consents/{ConsentId}/funds-confirmation` | `psu_authorization_code` | Forbidden | Not required |
| 4 | `submit_domestic_payment` | POST | `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp/domestic-payments` | `psu_authorization_code` | Required | Required (same key as stage) |
| 5 | `get_domestic_payment_status` | GET | `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp/domestic-payments/{DomesticPaymentId}` | `client_credentials_payments_scope` | Forbidden | Not required |

---

## Write Header Contract

Applies to endpoints 1 and 4 (POST calls only):

| Header | Endpoint 1 (stage) | Endpoint 4 (submit) | Notes |
|---|---|---|---|
| `x-jws-signature` | Required | Required | PS256, detached JWS, b64=false, crit=[iat,iss,tan], typ=JOSE, cty=application/json. Sending on AIS endpoints is REJECTED with UK.OBIE.Header.Unexpected. |
| `x-idempotency-key` | Required | Required (same key as stage) | UUID v4, ≤40 chars. Generated ONCE per staged payment; reused for all retries of both calls. |
| `x-fapi-interaction-id` | Required | Required | Per-call UUID (correlation id, NOT the same as idempotency key). Echo in support references. |
| `x-fapi-financial-id` | Not sent | Not sent | Absent from every call in the observed corpus; nothing rejects its absence. |

---

## Endpoint Details

### 1. `stage_domestic_payment_consent` — POST /domestic-payment-consents

Stage a domestic-payment-consent on the client-credentials token. Returns a ConsentId and the
Charges the bank will apply. The PSU has not yet approved at this stage (status AWAU).

| Attribute | Value |
|---|---|
| ID | `stage_domestic_payment_consent` |
| Method | POST |
| Auth | `client_credentials_payments_scope` |
| RLS enforced | No (server-side API, not Supabase) |
| Cache TTL | None — never cache a consent |
| Cache offline | error |
| Pagination | none |

#### Request Body

```yaml
Data:
  Initiation:
    InstructionIdentification: string   # ≤35 chars, generated per payment
    EndToEndIdentification:   string   # ≤35 chars, generated per payment
    LocalInstrument:          "UK.OBIE.FPS"
    InstructedAmount:
      Amount:   string   # major-unit decimal — e.g. "15.55". Integer arithmetic only; no float.
      Currency: "GBP"
    DebtorAccount:             # OPTIONAL. Omit to let PSU pick at the bank.
      SchemeName:      "UK.OBIE.SortCodeAccountNumber"
      Identification:  string   # 14 digits: 6 sort-code + 8 account-number, concatenated
      Name:            string   # OPTIONAL — contrast with CreditorAccount.Name which is mandatory
    CreditorAccount:           # MANDATORY
      SchemeName:      "UK.OBIE.SortCodeAccountNumber"
      Identification:  string   # 14 digits
      Name:            string   # MANDATORY — U004 if omitted (R9-07)
    RemittanceInformation:     # Whole block is optional; omit entirely when blank
      Unstructured:   [string]  # array with one element, ≤35 chars; omit entirely when reference is blank
      Structured:     [object]  # MUST BE AN ARRAY — bare object returns U002. Shape per R6-10.
Risk:
  PaymentContextCode: "TransferToThirdParty" | "TransferToSelf"
  # FORBIDDEN: EcommerceMerchantInitiatedPayment, BillingGoodsAndServicesInAdvance,
  # BillingGoodsAndServicesInArrears, FaceToFacePointOfSale
  # FORBIDDEN fields: MerchantCategoryCode, MerchantCustomerIdentification, DeliveryAddress
```

**Field rules enforced by the bank:**

- `CreditorAccount.Name` MANDATORY — R9-07 returns U004 "CreditorAccount.Name is missing".
- `DebtorAccount.Name` optional — no scenario rejects its absence.
- `CreditorAccount.SchemeName` MUST be `UK.OBIE.SortCodeAccountNumber` — IBAN → U027, PAN → U027
  (all eight BT scenarios including UK.OBIE.BalanceTransfer).
- `DebtorAccount.SchemeName` MUST be `UK.OBIE.SortCodeAccountNumber` if supplied — PAN → U027,
  Global Money TPP-named → U002 (but omitting DebtorAccount lets the bank nominate it).
- `Creditor` (party block with postal address) — if included, BuildingNumber is required. Omit
  entirely rather than send a partial block.
- `RemittanceInformation.Structured` — MUST be an array. Bare object → U002 (BT-07, BT-08).

#### Response Schema (201 Created)

```yaml
Data:
  ConsentId:              string   # Short sequential integer-as-string, e.g. "45116". NOT a UUID.
  CreationDateTime:       string   # ISO 8601
  Status:                 "AWAU"   # AwaitingAuthorisation — always on initial stage
  StatusUpdateDateTime:   string   # Matches CreationDateTime on initial stage
  Initiation:             object   # Echo of the staged Initiation
  Charges:
    - ChargeBearer:  "BorneByDebtor"
      Type:          "UK.OBIE.CHAPSOut"   # Observed on all 14 domestic consents, regardless of FPS instrument
      Amount:
        Amount:    "0.05"
        Currency:  "GBP"
Risk:
  PaymentContextCode: string   # Echoed from request
```

**ConsentId handling**: short sequential integers (e.g. `"45116"`), not UUIDs. Never place a
ConsentId in a URL, log line, crash report, or analytics event — treat as bearer-adjacent.

**Charges**: returned at staging, unlike the international rail. The charge is `0.05 GBP
UK.OBIE.CHAPSOut` on all observed consents. Populate `feeLabel` in the review_card from
`Charges[].Amount` after this call — the figure is only knowable after the consent exists.

#### Error Matrix

| Code | HTTP | When | Retry | Recovery |
|---|---|---|---|---|
| U019 | 400 | x-jws-signature missing or invalid | No | Support reference (OB envelope Id). Not user-recoverable — implementation fault. |
| U002 | 400 | Invalid field value (TPP-named Global Money debtor, or other field shape) | No | Return to account step. Should be unreachable — debtor picker prevents it. |
| U004 | 400 | Mandatory field missing — most likely CreditorAccount.Name | No | Return to payee step. Client-side validation should prevent this. |
| U027 | 400 | Unsupported scheme — PAN or IBAN on debtor/creditor | No | Should be unreachable — both pickers filter to SortCodeAccountNumber. |
| 401 | 401 | Token expired | Yes | Refresh client-credentials token and retry. |
| 500 | 500 | Upstream bank error | Yes | Retry — idempotency key is stable. |

---

### 2. `get_domestic_payment_consent_status` — GET /domestic-payment-consents/{ConsentId}

Poll the consent status after the PSU has authorised (or rejected) at the bank. This call is
handled by the `payment-consent` shared screen, not this ViewModel, but is documented here for
completeness.

| Attribute | Value |
|---|---|
| ID | `get_domestic_payment_consent_status` |
| Method | GET |
| Auth | `client_credentials_payments_scope` |
| Path param | `{ConsentId}` — from stage response |
| Cache TTL | None |
| Pagination | none |

#### Response Schema (200 OK)

```yaml
Data:
  ConsentId:              string
  Status:                 "AWAU" | "AUTH" | "COND" | "RJCT"
  StatusUpdateDateTime:   string   # WARNING: does NOT advance on AWAU→AUTH transition.
  CreationDateTime:       string
```

**Status meanings**:

| Status | Meaning |
|---|---|
| AWAU | AwaitingAuthorisation — staged, PSU not yet approved |
| AUTH | Authorised — PSU approved; consent may now be submitted |
| COND | Consumed — a domestic-payment resource has been created; single-use |
| RJCT | Rejected — PSU denied at the bank |

**Critical**: `StatusUpdateDateTime` does NOT move on AWAU→AUTH. All five authorised consents in
the corpus had StatusUpdateDateTime equal to CreationDateTime after authorisation. Poll
`Data.Status`, never `StatusUpdateDateTime`.

#### Error Matrix

| Code | HTTP | When | Retry | Recovery |
|---|---|---|---|---|
| 401 | 401 | Token expired | Yes | Refresh token |
| 404 | 404 | ConsentId not found | No | Implementation fault |

---

### 3. `funds_confirmation` — GET /domestic-payment-consents/{ConsentId}/funds-confirmation

Checks whether the debtor account holds sufficient funds for the consented amount. Requires the
PSU authorization-code token (not client-credentials). Called after the PSU authorises at the
bank. A PISP consent has a single fixed amount already staged, so no body is needed — this is a
GET, unlike VRP funds confirmation which is a POST.

| Attribute | Value |
|---|---|
| ID | `funds_confirmation` |
| Method | GET |
| Auth | `psu_authorization_code` |
| Prerequisite | Consent must be in AUTH status |
| Cache TTL | None |
| Pagination | none |

#### Request Parameters

| Param | Type | Required | Source |
|---|---|---|---|
| `{ConsentId}` | path string | Yes | From `stage_domestic_payment_consent` response |

#### Response Schema (200 OK)

```yaml
Data:
  FundsAvailableResult:
    FundsAvailable:         "Available" | "NotAvailable"
    FundsAvailableDateTime: string   # ISO 8601 — e.g. "2026-08-06T09:22:10+00:00"
```

**Demo fixture**:
```yaml
Data:
  FundsAvailableResult:
    FundsAvailable: "Available"
    FundsAvailableDateTime: "2026-08-06T09:22:10+00:00"
```

#### Error Matrix

| Condition | Action |
|---|---|
| `FundsAvailable = "NotAvailable"` | `uiState = Error(InsufficientFunds)`; return PSU to Amount step |
| 401 | Token expired → refresh |
| 403 | Consent revoked → `Error(ConsentRevoked)` |

---

### 4. `submit_domestic_payment` — POST /domestic-payments

Submit the payment on the PSU authorization-code token after funds confirmation passes. Echo
the `Initiation` object parsed from the AUTHORISED consent (not the locally staged copy).
Reuse the same `x-idempotency-key` as the stage call.

| Attribute | Value |
|---|---|
| ID | `submit_domestic_payment` |
| Method | POST |
| Auth | `psu_authorization_code` |
| Prerequisite | Consent in AUTH; funds confirmed Available |
| Cache TTL | None — payment resource is write-once |
| Cache offline | error |
| Pagination | none |

#### Request Body

```yaml
Data:
  ConsentId:   string   # from authorised consent
  Initiation:  object   # parsed Initiation read from the AUTHORISED consent, forwarded as-is
Risk:          object   # forwarded from the authorised consent
```

**Initiation echo rule**: The Initiation must match the authorised consent field-for-field. The
server normalises key order on every echo — bytes differ, but values are preserved. Therefore:
- Forward the parsed Initiation object from the GET consent response.
- Never re-serialise from the locally staged copy.
- Never compare by string or hash.
- When DebtorAccount was omitted at stage, the bank writes the PSU's choice into the authorised
  consent — so the authorised copy has a DebtorAccount the stage request did not.

#### Response Schema (201 Created)

```yaml
Data:
  DomesticPaymentId:  string   # e.g. "19908" — short sequential integer-as-string
  ConsentId:          string
  Status:             "ACSP"   # AcceptedSettlementInProcess — ALWAYS on submit response
  CreationDateTime:   string   # ISO 8601
```

**Settlement**: `ACSP` persists for minutes — settlement is batched (observed on five-minute
boundaries). Render as "in progress" (semantic.payment_disposition.in_progress / secondaryContainer).
NEVER render ACSP as "sent", "complete", or "success".

**Demo fixture**:
```yaml
Data:
  DomesticPaymentId: "19908"
  ConsentId: "45116"
  Status: "ACSP"
  CreationDateTime: "2026-08-06T09:22:35+00:00"
```

#### Error Matrix

| Code | HTTP | When | Retry | Recovery |
|---|---|---|---|---|
| U009 | 400 | Consent not in Authorised status | Yes | Re-authorise CTA — restarts app-to-app leg |
| U008 | 400 | Submitted Initiation does not match authorised consent | No | Re-read authorised consent and forward its Initiation |
| U019 | 400 | x-jws-signature missing or invalid | No | Support reference — implementation fault |
| U014 | 400 | Payment outside consent control parameters | No | Return to amount step |
| U027 | 400 | Unsupported scheme | No | Should be unreachable — pickers prevent it |
| U002 | 400 | Invalid field value | No | Return to account step |
| 403 | 403 | Consent revoked | No | View Consents CTA → consent-list |
| 401 | 401 | Token expired | Yes | Retry with refreshed token (idempotency key reused — safe) |
| IOException | — | Network timeout | Yes | Retry (idempotency key reused — same key = same result, no double charge) |

---

### 5. `get_domestic_payment_status` — GET /domestic-payments/{DomesticPaymentId}

Read back the payment status. Used by the downstream `payment-status` screen; documented here
because the resource ladder belongs to this payment family.

| Attribute | Value |
|---|---|
| ID | `get_domestic_payment_status` |
| Method | GET |
| Auth | `client_credentials_payments_scope` |
| Path param | `{DomesticPaymentId}` — from submit response |
| Cache TTL | None (polled until terminal) |
| Pagination | none |

#### Response Schema (200 OK)

```yaml
Data:
  DomesticPaymentId:      string
  Status:                 "ACSP" | "ACCC" | "RJCT"
  StatusUpdateDateTime:   string   # ISO 8601
  Charges:
    - Type:    "UK.OBIE.CHAPSOut"
      Amount:
        Amount:   "0.05"
        Currency: "GBP"
```

**Status ladder**:

| Status | Disposition | Render as |
|---|---|---|
| ACSP | `in_progress` | "In progress" (secondaryContainer + schedule icon) |
| ACCC | `terminal_success` | "Payment sent" (primaryContainer + check_circle icon) |
| RJCT | `terminal_failure` | "Payment rejected" (errorContainer + error icon) |

**Settlement timing**: All seven corpus payments ultimately reached ACCC. Settlement is
asynchronous and batched on five-minute boundaries — a payment confirmed minutes after ACSP is
normal behaviour, not an error.

**Demo fixture (read-back hours later)**:
```yaml
Data:
  DomesticPaymentId: "19908"
  Status: "ACCC"
  StatusUpdateDateTime: "2026-08-06T09:22:35+00:00"
  Charges:
    - Type: "UK.OBIE.CHAPSOut"
      Amount: { Amount: "0.05", Currency: "GBP" }
```

#### Error Matrix

| Code | HTTP | When | Retry | Recovery |
|---|---|---|---|---|
| 401 | 401 | Token expired | Yes | Refresh client-credentials token |
| 404 | 404 | DomesticPaymentId not found | No | Implementation fault |

---

## DTO Definitions

### DTO: `ObPaymentError`

All 400 responses on all five operations deserialise to this shape. See
`dtos/ObPaymentError.yaml` for the full contract (envelope shape, fail-fast ordering,
overloaded U002 cases, U004 four-wording issue, Path casing instability). The summary:

```kotlin
@Serializable
data class ObPaymentError(
  val Code:    String? = null,     // HTTP status as string, e.g. "400 BadRequest"
  val Message: String? = null,     // Not stable per ErrorCode — do NOT key on this
  val Errors:  List<ObPaymentErrorItem> = emptyList()   // ALWAYS iterate the whole array
)

@Serializable
data class ObPaymentErrorItem(
  val ErrorCode: String,           // e.g. "U019", "U004", "U002"
  val Message:   String,           // Four different wordings for U004 alone — do NOT key on this
  val Path:      String,           // e.g. "Data.Initiation.CreditorAccount.Name" — match case-insensitively
  val Url:       String? = null    // Optional OB specification link
)
```

**Critical rendering rules**:
1. Iterate the WHOLE `Errors[]` array — not just `[0]`. The bank returns TWO entries at once
   in scenarios R13-10 and R9-11.
2. Key display copy off `ErrorCode + Path` (case-insensitive on Path), never off `Message`.
3. U021 does NOT appear in the 139 single-payment scenarios — it is VRP-only. Do not map it
   on this screen.

### DTO: `DomesticFundsConfirmationResponse`

```kotlin
@Serializable
data class DomesticFundsConfirmationResponse(
  val Data: FundsAvailableData
)

@Serializable
data class FundsAvailableData(
  val FundsAvailableResult: FundsAvailableResult
)

@Serializable
data class FundsAvailableResult(
  val FundsAvailable:         String,   // "Available" or "NotAvailable"
  val FundsAvailableDateTime: String    // ISO 8601
)
```

---

## Eligibility Rules Summary

### Debtor accounts (picker filter: `SchemeName == "UK.OBIE.SortCodeAccountNumber"`)

| Account type | Scheme | Result if sent | UI action |
|---|---|---|---|
| Current account (e.g. AccountId 123456791, Identification 80200110203349) | SortCodeAccountNumber | 201 AWAU | Shown in picker |
| Current account 2 (AccountId 123456792, Identification 80200110203348) | SortCodeAccountNumber | 201 AWAU | Shown in picker |
| BMM ACCOUNT / savings (AccountId 1123456841) | SortCodeAccountNumber | 201 AWAU | Shown in picker |
| GLOBAL MONEY ACCOUNT (AccountId 1123456843) | SortCodeAccountNumber | U002 when TPP-names it | Hidden from picker — ineligible_accounts_note shown (hiddenAccountCount += 1) |
| Credit card (AccountId 1123456842) | PAN | U027 | Hidden from picker (hiddenAccountCount += 1) |

**Error is undiagnosable**: U002 @ `Data.Initiation.DebtorAccount.Identification` is overloaded
across three distinct causes (Global Money, sort-code-addressed credit card, PAN credit card on
international rail) — all with identical ErrorCode, Message, and Path. Client-side pre-filtering
is the ONLY design that produces a truthful message.

### Creditor accounts (picker filter: same `SchemeName == "UK.OBIE.SortCodeAccountNumber"`)

| Scheme | Result | Notes |
|---|---|---|
| SortCodeAccountNumber | 201 AWAU | Accepted |
| IBAN | U027 | Belongs on international rail |
| PAN | U027 | Refused under ALL LocalInstruments including BalanceTransfer (BT-09) |

---

## Cross-Feature API Usage

| Endpoint | Also Used By |
|---|---|
| `GET /domestic-payment-consents/{ConsentId}` | `payment-consent` (polls to AUTH) |
| `GET /domestic-payments/{DomesticPaymentId}` | `payment-status` (polls to terminal) |
| `GET /accounts` | `accounts` feature (AISP scope, same PSU session) |
| `GET /accounts/{AccountId}/beneficiaries` | `beneficiaries` feature (AISP scope) |

---

## Observed Demo Data

### Staged consent (demo-data.yaml fixture)

```
ConsentId: "45116"
Status: AWAU → AUTH (StatusUpdateDateTime frozen at CreationDateTime in both)
Amount: GBP 15.55
Debtor: 80200110203349 (Current account, AccountId 123456791)
Creditor: 80200110203348 (Name: Mr Mark)
Reference: "Rent August"
Fee: 0.05 GBP UK.OBIE.CHAPSOut
```

### Submit response + status readback

```
DomesticPaymentId: "19908"
Submit status: ACSP (always)
Readback status: ACCC (observed hours later — all seven corpus payments)
```
