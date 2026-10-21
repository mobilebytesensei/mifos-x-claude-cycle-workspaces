# pay-domestic-scheduled — API Contracts

> Generated from `screens/pay-domestic-scheduled/api.yaml` by `/idea export`
> Schema version: 4.0
> Contract version: 2.1.0
> Endpoints: 4
> Host: `https://secure.sandbox.ob.hsbc.co.uk`
> Base path: `/obie/open-banking/v4.0/pisp`
> Auth: mTLS + `private_key_jwt` (PS256) + authorization-code, FAPI 1.0 Advanced
> Authorize URL: `https://sandbox.ob.hsbc.co.uk/obie/open-banking/v1.1/oauth2/authorize`

---

## Endpoint Summary

| # | ID | Method | Path | Auth | Returns |
|---|---|---|---|---|---|
| 1 | `stage_domestic_scheduled_consent` | POST | `/domestic-scheduled-payment-consents` | client_credentials | `201 ConsentId, AWAU` |
| 2 | `get_domestic_scheduled_consent_status` | GET | `/domestic-scheduled-payment-consents/{ConsentId}` | client_credentials | `200 Status` |
| 3 | `submit_domestic_scheduled_payment` | POST | `/domestic-scheduled-payments` | psu_authorization_code | `201 DomesticScheduledPaymentId, PDNG` |
| 4 | `get_domestic_scheduled_payment_status` | GET | `/domestic-scheduled-payments/{DomesticScheduledPaymentId}` | client_credentials | `200 Status` |

---

## Endpoint Details

### 1. `stage_domestic_scheduled_consent` — Stage consent for a future-dated domestic payment

| Attribute | Value |
|---|---|
| ID | `stage_domestic_scheduled_consent` |
| Method | POST |
| Path | `/obie/open-banking/v4.0/pisp/domestic-scheduled-payment-consents` |
| Auth | `client_credentials` (payments scope) |
| Required headers | `x-jws-signature`, `x-idempotency-key` |
| Funds confirmation | None — endpoint does not exist on this rail family |
| Cache | none |
| Offline | error |

#### Request Body

```yaml
Data:
  Permission: "Create"                          # MANDATORY. Omit → U004 at Data.Permission.
  ReadRefundAccount: "No"                       # Optional. "Yes" accepted but returns Data.Debtor
                                                # (not DebtorAccount) with no Name — carries no
                                                # new information.
  Initiation:
    InstructionIdentification: String           # Generated; unique per payment
    EndToEndIdentification: String              # Generated; unique per payment
    LocalInstrument: "UK.OBIE.FPS"
    RequestedExecutionDateTime: String          # MANDATORY. ISO 8601. Strictly tomorrow to T+365.
                                                # Omit → U004. Today → U003. T+366+ → U002.
                                                # Time component is silently discarded (midnight).
    InstructedAmount:
      Amount: String                            # Major-unit string e.g. "1.01"
      Currency: "GBP"
    DebtorAccount:
      SchemeName: "UK.OBIE.SortCodeAccountNumber"
      Identification: String                    # 14-digit: 6-digit sort code + 8-digit account
    CreditorAccount:
      SchemeName: "UK.OBIE.SortCodeAccountNumber"
      Identification: String                    # 14-digit: payee sort code + account number
      Name: String                              # Payee name — mandatory; omit → U004
    RemittanceInformation:
      Unstructured:
        - String                                # Reference text. Accepted and persists.
  # Optional blocks:
  Authorisation:                                # Optional
    AuthorisationType: String
    CompletionDateTime: String                  # Accepted but midnight-truncated on echo (like
                                                # RequestedExecutionDateTime). Do not build
                                                # countdowns from the echoed value.
  SCASupportData:                               # Optional — echoed verbatim, no exemption effect.
    RequestedSCAExemptionType: String           # Consent still lands AWAU. Always route through
    AppliedAuthenticationApproach: String       # payment-consent regardless.
    ReferencePaymentOrderId: String
Risk:
  PaymentContextCode: "TransferToThirdParty"   # Or "TransferToSelf". Domestic rail always sends
                                                # PaymentContextCode. Do NOT send
                                                # ExchangeRateInformation — U005 on all RateTypes,
                                                # and U005 fires before U004 (masking missing fields).
```

#### Response Schema (201 Created)

```yaml
Data:
  ConsentId: String                             # Short sequential integer-as-string e.g. "45175"
                                                # NOT a UUID. Keep out of URLs, logs, analytics.
  CreationDateTime: String                      # ISO 8601 timestamp
  Status: "AWAU"                                # Always AWAU on 201
  StatusUpdateDateTime: String                  # STUB: same value as CreationDateTime on every 201.
                                                # Do not derive auth-detection from this field.
  Permission: "Create"
  ReadRefundAccount: "No"                       # Echoed
  Initiation:
    InstructionIdentification: String
    EndToEndIdentification: String
    LocalInstrument: "UK.OBIE.FPS"
    RequestedExecutionDateTime: String          # NORMALISED to midnight UTC. "2026-08-13T10:28:58+00:00"
                                                # becomes "2026-08-13T00:00:00+00:00". Review step
                                                # shows date only — the time is NOT honoured.
    InstructedAmount:
      Amount: String
      Currency: "GBP"
    DebtorAccount:
      SchemeName: "UK.OBIE.SortCodeAccountNumber"
      Identification: String
    CreditorAccount:
      SchemeName: "UK.OBIE.SortCodeAccountNumber"
      Identification: String
      Name: String
    RemittanceInformation:
      Unstructured:
        - String
  Charges:
    - ChargeBearer: "BorneByDebtor"
      Type: "UK.OBIE.CHAPSOut"
      Amount:
        Amount: "0.05"                          # Observed at staging (sandbox)
        Currency: "GBP"
Risk:
  PaymentContextCode: String                    # Echoed from request
```

Demo fixture (from demo-data.yaml):
```yaml
Data:
  ConsentId: "45175"
  Status: "AWAU"
  Initiation:
    RequestedExecutionDateTime: "2026-08-13T00:00:00+00:00"   # normalised from T10:28:58
    InstructedAmount: { Amount: "1.01", Currency: "GBP" }
    CreditorAccount: { Name: "Ramu", Identification: "40200110203351" }
    RemittanceInformation: { Unstructured: ["Rent"] }
  Charges:
    - { Type: "UK.OBIE.CHAPSOut", Amount: { Amount: "0.05", Currency: "GBP" } }
```

#### Error Matrix

| Code | HTTP | When | Retry | Recovery UI |
|---|---|---|---|---|
| U004 | 400 | `Data.Permission` omitted | No | Implementation fault — always send `"Create"` |
| U004 | 400 | `RequestedExecutionDateTime` omitted | No | Return to date step |
| U004 | 400 | `CreditorAccount.Name` omitted | No | Return to payee step |
| U003 | 400 | Date is today or in the past | No | Return to date step; picker should prevent |
| U002 | 400 | Date beyond T+365 | No | Return to date step; picker should prevent |
| U005 | 400 | `ExchangeRateInformation` present (any RateType) | No | Never send this block — it fires before U004 |
| U019 | 400 | `x-jws-signature` missing or invalid | No | Not user-recoverable |
| IOException | — | Network failure / timeout | Yes | Retry with same idempotency key |

---

### 2. `get_domestic_scheduled_consent_status` — Poll for consent status after authorisation

| Attribute | Value |
|---|---|
| ID | `get_domestic_scheduled_consent_status` |
| Method | GET |
| Path | `/obie/open-banking/v4.0/pisp/domestic-scheduled-payment-consents/{ConsentId}` |
| Auth | `client_credentials` |
| Status ladder | AWAU → AUTH → COND |
| Polled until | AUTH |
| Cache | none |

#### Request Parameters

| Param | Type | Required | Source |
|---|---|---|---|
| `ConsentId` | `String` (path) | Yes | `stagedConsent.Data.ConsentId` |

#### Response Schema (200 OK)

```yaml
Data:
  ConsentId: String
  Status: String                                # AWAU | AUTH | COND
  StatusUpdateDateTime: String                  # STUB: does NOT move on AWAU → AUTH transition.
                                                # Detect auth by reading Data.Status only.
  CreationDateTime: String
  Permission: "Create"
  Initiation:
    # ... (same shape as POST response)
    # IMPORTANT: Forward the parsed Initiation OBJECT from this response as the submit body.
    # Do not re-serialise it: the server reorders Initiation keys on echo (LocalInstrument
    # lands in a different position on different requests). String-compare or hash would
    # incorrectly reject valid payments.
```

Demo fixture (from demo-data.yaml — authorised):
```yaml
Data:
  ConsentId: "45175"
  Status: "AUTH"
  StatusUpdateDateTime: "2026-08-06T10:40:48+00:00"   # same as CreationDateTime — did not move
```

#### Error Matrix

| Code | HTTP | When | Retry | Recovery UI |
|---|---|---|---|---|
| 404 | — | ConsentId not found | No | Not expected; indicates stale flow state |
| IOException | — | Network failure | Yes | Retry |

---

### 3. `submit_domestic_scheduled_payment` — Submit after consent is authorised

| Attribute | Value |
|---|---|
| ID | `submit_domestic_scheduled_payment` |
| Method | POST |
| Path | `/obie/open-banking/v4.0/pisp/domestic-scheduled-payments` |
| Auth | `psu_authorization_code` |
| Required headers | `x-jws-signature`, `x-idempotency-key` |
| Funds confirmation | None — no such endpoint on this family |
| Cache | none |

#### Request Body

```yaml
Data:
  ConsentId: String                             # From authorised consent GET
  Initiation: Object                            # The parsed Initiation object read from the
                                                # authorised consent. Forward as an object —
                                                # do NOT re-serialise or hash. Key order changes
                                                # between responses; only VALUES are stable.
Risk: Object                                    # The Risk object from the authorised consent.
```

#### Response Schema (201 Created)

```yaml
Data:
  DomesticScheduledPaymentId: String            # Short sequential integer-as-string e.g. "19919"
  ConsentId: String
  Status: "PDNG"                                # Always PDNG on 201
  CreationDateTime: String
  ExpectedExecutionDateTime: String             # STUB: equals CreationDateTime on every 201.
                                                # Do NOT display as "your payment will arrive on".
  ExpectedSettlementDateTime: String            # STUB: same value as above.
  Initiation:
    # ... (echoed from authorised consent, with possible key reordering)
```

Demo fixture (from demo-data.yaml):
```yaml
Data:
  DomesticScheduledPaymentId: "19919"
  ConsentId: "45175"
  Status: "PDNG"
  CreationDateTime: "2026-08-06T10:42:08+00:00"
  ExpectedExecutionDateTime: "2026-08-06T10:42:08+00:00"   # STUB — equals creation timestamp
  ExpectedSettlementDateTime: "2026-08-06T10:42:08+00:00"  # STUB — equals creation timestamp
```

#### Error Matrix

| Code | HTTP | When | Retry | Recovery UI |
|---|---|---|---|---|
| U009 | 400 | Consent not in Authorised status | Yes | Re-authorise CTA |
| U008 | 400 | Initiation does not match authorised consent | No | Re-read authorised consent |
| U019 | 400 | `x-jws-signature` missing | No | Not user-recoverable |
| IOException | — | Network failure | Yes | Retry with same idempotency key |

---

### 4. `get_domestic_scheduled_payment_status` — Read resource status after submission

| Attribute | Value |
|---|---|
| ID | `get_domestic_scheduled_payment_status` |
| Method | GET |
| Path | `/obie/open-banking/v4.0/pisp/domestic-scheduled-payments/{DomesticScheduledPaymentId}` |
| Auth | `client_credentials` |
| Status ladder | PDNG → INCO |
| Cache | none |

#### Request Parameters

| Param | Type | Required | Source |
|---|---|---|---|
| `DomesticScheduledPaymentId` | `String` (path) | Yes | `submit.Data.DomesticScheduledPaymentId` |

#### Response Schema (200 OK)

```yaml
Data:
  DomesticScheduledPaymentId: String
  Status: String                                # PDNG | INCO
```

Status meanings:
- `PDNG` — Pending. The instruction is set up and waiting for the execution date. NOT "money is moving now."
- `INCO` — InitiationCompleted. The instruction is established. NOT "the money moved." There is no per-execution status in OBIE.

Both statuses map to `instruction_established` disposition (neutral chip, `event_repeat` icon).
NEITHER maps to `terminal_success`. Payment execution status cannot be confirmed through the
PIS or AIS API — the UI must never claim a scheduled payment has paid.

Demo fixture (from demo-data.yaml — read back later):
```yaml
Data:
  DomesticScheduledPaymentId: "19919"
  Status: "INCO"
```

#### Error Matrix

| Code | HTTP | When | Retry | Recovery UI |
|---|---|---|---|---|
| 404 | — | PaymentId not found | No | Not expected |
| IOException | — | Network failure | Yes | Retry |

---

## DTO Definitions

### ObPaymentError (shared across all seven PIS rails)

```kotlin
@Serializable
data class ObPaymentError(
  val Errors: List<ObPaymentErrorEntry>
)

@Serializable
data class ObPaymentErrorEntry(
  val ErrorCode: String,                        // e.g. "U004", "U003", "U002"
  val Message: String,                          // Unstable wording — do NOT key off this.
                                                // U004 has four observed wordings incl. bare
                                                // "Field is missing" with no path information.
  val Path: String?,                            // e.g. "Data.Permission" or
                                                // "Data.Initiation.RequestedExecutionDateTime"
                                                // Path casing is not stable across responses.
                                                // Match case-insensitively.
  val Url: String? = null
)
```

Key rendering rules:
- `Errors` is an ARRAY. Render ALL entries — two entries at once is observed.
- Key copy off `ErrorCode` + `Path` (case-insensitive Path match). Never off `Message`.
- U003 and U002 on the date field should be unreachable in normal flow — the picker's bounds prevent them.
- U005 fires BEFORE U004: an unexpected field masks a missing mandatory one. Never send `ExchangeRateInformation`.

### DomesticScheduledPaymentConsentResponse

```kotlin
@Serializable
data class DomesticScheduledPaymentConsentResponse(
  val Data: DomesticScheduledConsentData,
  val Risk: PaymentRisk
)

@Serializable
data class DomesticScheduledConsentData(
  val ConsentId: String,
  val CreationDateTime: String,
  val Status: String,                           // AWAU | AUTH | COND
  val StatusUpdateDateTime: String,             // STUB — equals CreationDateTime
  val Permission: String,                       // "Create"
  val Initiation: DomesticScheduledInitiation,
  val Charges: List<PaymentCharge>? = null
)

@Serializable
data class DomesticScheduledInitiation(
  val InstructionIdentification: String,
  val EndToEndIdentification: String,
  val LocalInstrument: String,
  val RequestedExecutionDateTime: String,       // Midnight-normalised on echo
  val InstructedAmount: PaymentAmount,
  val DebtorAccount: PaymentAccount? = null,
  val CreditorAccount: PaymentAccount,
  val RemittanceInformation: RemittanceInfo? = null
)
```

---

## Cross-Feature API Usage

| Endpoint | Also Used By |
|---|---|
| `/domestic-scheduled-payment-consents` | payment-consent (polling for AUTH status) |
| `/domestic-scheduled-payments` | payment-status (polling PDNG → INCO) |

---

## Rail-Specific Invariants

| Invariant | Consequence |
|---|---|
| `Data.Permission: "Create"` is mandatory on this rail (absent on pay-domestic-single) | Omitting it → U004; client must always include it |
| `RequestedExecutionDateTime` is mandatory (absent on pay-domestic-single) | Omitting it → U004; client must always include it |
| No funds-confirmation endpoint exists | Never add a ConfirmingFunds stage or substitute a balance check |
| Status ladder is PDNG → INCO, not ACSP → ACCC | INCO means instruction established, never "money moved" |
| Five response timestamps are stubs (all equal CreationDateTime) | Show only the PSU-chosen requestedExecutionDate in the UI |
| Initiation key order is unstable on echo | Forward the parsed object; never re-serialise or hash |
| PISP cannot amend or cancel | Mandatory disclosure in UI at Review step and Success state |
