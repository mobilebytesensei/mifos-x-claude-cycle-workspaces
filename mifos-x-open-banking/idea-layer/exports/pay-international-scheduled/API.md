# Pay International Scheduled — API Reference

> Host: `https://secure.sandbox.ob.hsbc.co.uk`
> Base path: `/obie/open-banking/v4.0/pisp`
> Authorisation endpoint: `https://sandbox.ob.hsbc.co.uk/obie/open-banking/v1.1/oauth2/authorize`
> Auth scheme: mTLS + `private_key_jwt` (PS256) + FAPI 1.0 Advanced (authorization-code flow)
> Rail: `international-scheduled-payment`
> Evidence: 25 scenarios (captures/by-type/scheduled-international.md); resource 19921 authorised

---

## Auth Flow Summary

1. Obtain client-credentials access token using `private_key_jwt` (PS256) over mTLS.
2. Stage consent → receive `ConsentId`.
3. Redirect PSU to the authorisation endpoint with `consentId` and `paymentFamily`.
4. The `payment-consent` screen handles the app-to-app redirect leg.
5. On `AUTH`, return to this feature and submit.

---

## Operations

### 1. Stage International Scheduled Payment Consent

**Method**: `POST`
**Path**: `/international-scheduled-payment-consents`
**Auth**: `client_credentials` (payments scope) + mTLS
**Required headers**: `x-jws-signature`, `x-idempotency-key`

#### Request Body

```json
{
  "Data": {
    "Permission": "Create",
    "ReadRefundAccount": "No",
    "Initiation": {
      "InstructionIdentification": "<generated>",
      "EndToEndIdentification": "<generated>",
      "LocalInstrument": "UK.OBIE.SWIFT",
      "RequestedExecutionDateTime": "<ISO 8601 strictly > today and <= T+365>",
      "InstructedAmount": {
        "Amount": "<major-unit string, e.g. 1.01>",
        "Currency": "<ISO 4217, e.g. GBP>"
      },
      "DebtorAccount": {
        "SchemeName": "UK.OBIE.SortCodeAccountNumber",
        "Identification": "<14 digits>"
      },
      "CreditorAccount": {
        "SchemeName": "UK.OBIE.IBAN",
        "Identification": "<IBAN, e.g. FR29NWBK60161331926819>",
        "Name": "<payee name>"
      },
      "CurrencyOfTransfer": "<ISO 4217, e.g. EUR>",
      "ChargeBearer": "BorneByCreditor"
    }
  },
  "Risk": {
    "CategoryPurposeCode": "EPAY"
  }
}
```

**MUST NOT include**:
- `Data.Initiation.RemittanceInformation` → U005 (Field is not expected)
- `Data.Initiation.ExchangeRateInformation` → U005 for all RateType values (Actual / Indicative / Agreed)

**Mandatory fields** (omitting any → U004):
- `Data.Permission = "Create"`
- `Data.Initiation.RequestedExecutionDateTime`
- `Data.Initiation.CurrencyOfTransfer`
- `Data.Initiation.ChargeBearer`

#### Response — 201 Created

```json
{
  "Data": {
    "ConsentId": "45176",
    "Status": "AWAU",
    "CreationDateTime": "2026-08-06T10:42:35+00:00",
    "StatusUpdateDateTime": "2026-08-06T10:42:35+00:00",
    "Permission": "Create",
    "Initiation": {
      "ChargeBearer": "BorneByCreditor",
      "CurrencyOfTransfer": "EUR",
      "InstructedAmount": { "Amount": "1.01", "Currency": "GBP" },
      "CreditorAccount": {
        "SchemeName": "UK.OBIE.IBAN",
        "Identification": "FR29NWBK60161331926819",
        "Name": "Mr Lee"
      }
    }
  },
  "Risk": { "CategoryPurposeCode": "EPAY" }
}
```

**Charges**: key is **ABSENT** — not an empty array. Parse as nullable `List<Charge>?`. Do NOT default to `[]`.  
Also absent: `CutOffDateTime`, `ExpectedExecutionDateTime`, `ExpectedSettlementDateTime`.  
**Server key reorder**: the echo order is `ChargeBearer, CurrencyOfTransfer, InstructedAmount, MandateRelatedInformation, [CreditorAgent], [DebtorAccount], CreditorAccount` regardless of request order.

#### Error Codes

| Code | HTTP | Trigger | Path Example |
|------|------|---------|--------------|
| U004 | 400 | Permission / RequestedExecutionDateTime / CurrencyOfTransfer / ChargeBearer omitted | Data.Initiation.ChargeBearer |
| U005 | 400 | RemittanceInformation or ExchangeRateInformation sent | Data.Initiation.RemittanceInformation |
| U003 | 400 | RequestedExecutionDateTime is today or in the past | Data.Initiation.RequestedExecutionDateTime |
| U002 | 400 | RequestedExecutionDateTime > T+365, or BIC not 11 characters | Data.Initiation.RequestedExecutionDateTime |
| U019 | 400 | Missing x-jws-signature header | — |
| U027 | 400 | Sort-code creditor (not IBAN) — unreachable on this form | Data.Initiation.CreditorAccount.SchemeName |

---

### 2. Get International Scheduled Payment Consent Status

**Method**: `GET`
**Path**: `/international-scheduled-payment-consents/{ConsentId}`
**Auth**: `client_credentials` + mTLS

#### Response — 200 OK

```json
{
  "Data": {
    "ConsentId": "45176",
    "Status": "AUTH",
    "StatusUpdateDateTime": "2026-08-06T10:42:35+00:00"
  }
}
```

**Status ladder**: `AWAU → AUTH → COND`
**Important**: `StatusUpdateDateTime` does NOT advance on the `AWAU → AUTH` transition. Poll by `Status` value, not timestamp change.

---

### 3. Submit International Scheduled Payment

**Method**: `POST`
**Path**: `/international-scheduled-payments`
**Auth**: `psu_authorization_code` + mTLS
**Required headers**: `x-jws-signature`, `x-idempotency-key`

#### Request Body

Echo the authorised consent's `Initiation` and `Risk` verbatim. Use the **parsed read-back object**, not a re-serialised local model — the server reorders keys on echo, so a string comparison will fail on a correct body.

```json
{
  "Data": {
    "ConsentId": "45176",
    "Initiation": "<verbatim from GET /consents/{id} response Data.Initiation>"
  },
  "Risk": "<verbatim echo of Risk>"
}
```

#### Response — 201 Created

```json
{
  "Data": {
    "InternationalScheduledPaymentId": "19921",
    "ConsentId": "45176",
    "Status": "INCO",
    "CreationDateTime": "2026-08-06T10:44:12+00:00",
    "Charges": [
      {
        "ChargeBearer": "BorneByCreditor",
        "Type": "UK.OBIE.CHAPSOut",
        "Amount": { "Amount": "0.50", "Currency": "GBP" }
      }
    ]
  }
}
```

**Status**: always `INCO` at creation. This rail **never emits `PDNG`**. `INCO` is the normal creation status, not anomalous.

**Charge currency rule**: the 0.50 charge is denominated in `InstructedAmount.Currency`, NOT `CurrencyOfTransfer`.  
Evidence (three resources): 19918 (GBP instructed / USD transfer → 0.50 GBP), 19921 (GBP / EUR → 0.50 GBP), 19917 (USD / USD → 0.50 USD).

**This is the first and only moment the fee is available.** The charge is absent on the consent at AWAU and absent at AUTH. A PISP cannot show an international deferred fee at any point before the PSU authorises.

#### Error Codes

| Code | HTTP | Trigger |
|------|------|---------|
| U009 | 400 | Consent not in AUTH status |
| U019 | 400 | Missing x-jws-signature header |

---

### 4. Get International Scheduled Payment Status

**Method**: `GET`
**Path**: `/international-scheduled-payments/{InternationalScheduledPaymentId}`
**Auth**: `client_credentials` + mTLS

#### Response — 200 OK

```json
{
  "Data": {
    "InternationalScheduledPaymentId": "19921",
    "Status": "INCO"
  }
}
```

**Status ladder**: `INCO → INCO` — no transition observed on this rail.
**INCO semantics**: the instruction is registered at the bank. It does NOT mean a payment has executed; execution occurs on `RequestedExecutionDateTime`. No per-execution status is ever surfaced by PISP APIs on this rail.
**Design token**: render using `semantic.payment_disposition.instruction_established` (surfaceVariant / onSurfaceVariant, icon `event_repeat`). Label: "Scheduled for \<date\>". FORBIDDEN substrings: paid, sent, complete, successful, any past-tense amount.

---

## Key Constraints Summary

| Constraint | Value | Error if violated |
|------------|-------|-------------------|
| RequestedExecutionDateTime minimum | T+1 (tomorrow) | U003 |
| RequestedExecutionDateTime maximum | T+365 | U002 |
| Date normalisation by server | Truncated to midnight UTC | Server echo shows `T00:00:00+00:00` |
| CreditorAccount scheme | UK.OBIE.IBAN only | U027 if sort-code |
| BIC length (if CreditorAgent sent) | Exactly 11 characters | U002 if 8-char |
| RemittanceInformation | FORBIDDEN | U005 |
| ExchangeRateInformation | FORBIDDEN (all RateType values) | U005 |
| Funds confirmation endpoint | DOES NOT EXIST for this rail | — |
| Charge disclosure before authorisation | IMPOSSIBLE — absent at AWAU and AUTH | — |
| FX rate disclosure | IMPOSSIBLE — ExchangeRateInformation refused; no rate endpoint | — |
| Amendment / cancellation via PISP | NOT PERMITTED | Redirect PSU to bank channel (OBL CEG obligation) |
| Submit body construction | Parse read-back, never re-serialise local model | Byte mismatch (key reorder) |

---

## Error Envelope (all 400 responses)

Per `dtos/ObPaymentError.yaml`. The `Errors` field is an **array** — render every entry in wire order, keyed by `ErrorCode + Path`. Do NOT bind UI to `Errors[0]` alone. SP-I04 (this rail's own two-entry case) has `Errors[0]` naming the creditor and `Errors[1]` naming the currency; rendering only the first sends the PSU to fix the wrong thing.

```json
{
  "Errors": [
    { "ErrorCode": "U027", "Message": "Unsupported scheme", "Path": "Data.Initiation.CreditorAccount.SchemeName" },
    { "ErrorCode": "U002", "Message": "...", "Path": "Data.Initiation.CurrencyOfTransfer" }
  ]
}
```

Copy is keyed by `ErrorCode + Path`, never by `Message` — U004 alone carries four distinct wordings in the corpus.
