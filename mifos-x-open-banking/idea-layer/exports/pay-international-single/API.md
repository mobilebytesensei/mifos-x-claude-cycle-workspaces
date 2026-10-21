# API — Pay Abroad (International Single Payment)

Client contracts for `pay-international-single`. Ktorfit contracts against the HSBC OBIE v4.0
sandbox — not project-owned schema.

**Resource host:** `https://secure.sandbox.ob.hsbc.co.uk`
**Base path:** `/obie/open-banking/v4.0/pisp`
**Authorise host (browser leg only):** `https://sandbox.ob.hsbc.co.uk/obie/open-banking/v1.1/oauth2/authorize`

Auth scheme: mTLS + `private_key_jwt` (PS256) + OAuth authorization-code, FAPI 1.0 Advanced.
Consumer: `PaymentInitiationRepository`.

---

## Endpoint table

| ID | Method | Path | Auth |
|----|--------|------|------|
| stage_international_payment_consent | POST | `/international-payment-consents` | client_credentials_payments_scope |
| get_international_payment_consent_status | GET | `/international-payment-consents/{ConsentId}` | client_credentials_payments_scope |
| funds_confirmation | GET | `/international-payment-consents/{ConsentId}/funds-confirmation` | psu_authorization_code |
| submit_international_payment | POST | `/international-payments` | psu_authorization_code |
| get_international_payment_status | GET | `/international-payments/{InternationalPaymentId}` | client_credentials_payments_scope |

---

## 1 — Stage international payment consent

**POST** `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp/international-payment-consents`

Required headers: `x-jws-signature`, `x-idempotency-key`

### Request body

```json
{
  "Data": {
    "Initiation": {
      "InstructionIdentification": "<generated>",
      "EndToEndIdentification": "<generated>",
      "CurrencyOfTransfer": "<ISO 4217 — currency the creditor receives; MANDATORY>",
      "InstructedAmount": {
        "Amount": "<major-unit string, decimals per currency — e.g. '5.00' GBP, '1000' JPY>",
        "Currency": "<ISO 4217 — currency the debtor is charged in>"
      },
      "DebtorAccount": {
        "SchemeName": "UK.OBIE.SortCodeAccountNumber",
        "Identification": "<14-digit concatenated sort code + account number>"
      },
      "CreditorAccount": {
        "SchemeName": "UK.OBIE.IBAN",
        "Identification": "<IBAN — any country, mod-97 valid>",
        "Name": "<payee name>"
      },
      "CreditorAgent": {
        "SchemeName": "UK.OBIE.BICFI",
        "Identification": "<11-character BIC — OMIT THIS ENTIRE BLOCK IF BLANK>"
      },
      "ChargeBearer": "BorneByCreditor | Shared | BorneByDebtor"
    }
  },
  "Risk": {
    "CategoryPurposeCode": "EPAY"
  }
}
```

### Mandatory / forbidden field contract

| Field | Rule | Error if violated |
|-------|------|-------------------|
| `Data.Initiation.CurrencyOfTransfer` | MANDATORY | `U004 Field is missing` |
| `Data.Initiation.ChargeBearer` | MANDATORY | `U004 Field is missing @ Data.Initiation.ChargeBearer` |
| `Data.Initiation.RemittanceInformation` | FORBIDDEN — never send | `U005 Field is not expected` |
| `Data.Initiation.CreditorAccount.SchemeName` | Must be `UK.OBIE.IBAN` | `U027` |
| `Data.Initiation.CreditorAgent` | Optional, but presence makes `Identification` mandatory | `U004 @ Data.Initiation.CreditorAgent.Identification` |
| `Data.Initiation.CreditorAgent.Identification` | Exactly 11 characters | `U002 Invalid Bank Code` (8-char BICs refused) |
| `Data.Initiation.ExchangeRateInformation` | FORBIDDEN — refused for all three RateType values | `U005` |

### Accepted values for ChargeBearer

`BorneByCreditor`, `Shared`, `BorneByDebtor` — all three stage 201 (INT-11, INT-12). None is a
bank default; the PSU chooses.

### CreditorAgent partial-object trap

Sending the `CreditorAgent` key at all makes `Identification` mandatory. Scenarios R8-01 through
R8-10 and R3-08 all sent a `CreditorAgent` with only `PostalAddress.Country` or `Name` and all
returned `U004 @ Data.Initiation.CreditorAgent.Identification`. Scenario R8-11 — the identical
body with the key removed — staged 201. The block is emitted **whole** (with an 11-character
Identification) or **omitted entirely**. The serialiser must not produce an empty-but-present
object when the BIC field is blank.

### BIC length rule

The 8-character refusal is length-driven, not country-mismatch-driven. R2-07 paired a MATCHING
French BIC (`NWBKFRPP`) with a French IBAN and still received `U002 Invalid Bank Code`. R3-04's
11-character `COBADEFFXXX` staged 201. The local validator checks **length only** — a BIC-to-IBAN
country correlation would reject valid cross-border routings the endpoint accepts.

### Success response

`201` with `Data.ConsentId` (e.g. `"45264"`) and `Data.Status: "AWAU"`.

`Charges`, `CutOffDateTime`, `ExpectedExecutionDateTime`, `ExpectedSettlementDateTime` are **absent**
from this response — the keys do not appear, they are not empty arrays. Parse all four as nullable.

**Echo key order:** The server reorders `Initiation` keys — it returns `ChargeBearer`,
`CurrencyOfTransfer`, `InstructedAmount`, `[MandateRelatedInformation]`, `[CreditorAgent]`,
`[DebtorAccount]`, `CreditorAccount` regardless of the request order. Do not string-compare the
local form model against the read-back; compare field-by-field or not at all.

**Demo-data fixture** (R18-B02):
```json
{
  "Data": {
    "ConsentId": "45264",
    "Status": "AWAU",
    "StatusUpdateDateTime": "2026-08-06T17:17:56+00:00",
    "Initiation": {
      "ChargeBearer": "BorneByCreditor",
      "CurrencyOfTransfer": "EUR",
      "InstructedAmount": { "Amount": "5.00", "Currency": "GBP" },
      "DebtorAccount": { "SchemeName": "UK.OBIE.SortCodeAccountNumber", "Identification": "80200110203349" },
      "CreditorAccount": { "SchemeName": "UK.OBIE.IBAN", "Identification": "DE89370400440532013000", "Name": "Klara Weiss" }
    }
  },
  "Risk": { "CategoryPurposeCode": "EPAY" }
}
```

ConsentId `"45264"` is a short sequential integer-as-string. Never log it, deep-link it, or include
it in any PSU-visible error string — it is enumerable, not a UUID.

---

## 2 — Get international payment consent status

**GET** `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp/international-payment-consents/{ConsentId}`

### Consent status ladder

| Status | Meaning | Action |
|--------|---------|--------|
| `AWAU` | Awaiting PSU authorisation at the bank | Poll |
| `AUTH` | PSU authorised | Proceed to funds confirmation |
| `RJCT` | PSU rejected — terminal | Show rejection message; offer fresh payment |
| `COND` | Consumed | Payment submitted |

`StatusUpdateDateTime` does not advance on the `AWAU → AUTH` transition — this is observed
behaviour on every HSBC OBIE family. Do not derive elapsed time from this field.

`RJCT` is a real observed terminal state (consent 45121). A rejected consent cannot be reused —
offer a fresh payment, never a resubmit.

---

## 3 — Funds confirmation

**GET** `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp/international-payment-consents/{ConsentId}/funds-confirmation`

Requires `AUTH` consent. Auth: `psu_authorization_code`.

**Success:** `200` with `Data.FundsAvailableResult.FundsAvailable: "Available" | "NotAvailable"`

**Demo-data fixture:**
```json
{ "Data": { "FundsAvailableResult": { "FundsAvailable": "Available" } } }
```

If `FundsAvailable` is `"NotAvailable"`, set `uiState = Error(InsufficientFunds)` and return the
PSU to the Amount step.

**FX window:** Guide §21.10.1 describes a 40-second FX window with 5 seconds for the TPP to POST
and instructs TPPs not to call funds-confirmation. Observed: both authorised FX flows on this
endpoint called it and submitted minutes later without rejection. The window was not enforced —
do not implement a countdown.

---

## 4 — Submit international payment

**POST** `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp/international-payments`

Required headers: `x-jws-signature`, `x-idempotency-key` (same key as staging — idempotent on retry).

### Request body

```json
{
  "Data": {
    "ConsentId": "<from the authorised consent GET read-back>",
    "Initiation": "<parsed Initiation object from the authorised consent GET — not re-serialised from the local model>"
  },
  "Risk": "<Risk object from the authorised consent GET read-back>"
}
```

**Echo fidelity rule:** `Initiation` must be the **parsed object** from the authorised consent
read-back. The server reorders keys; a re-serialisation of the local request model produces a
different byte sequence and would abort a payment the bank accepts.

**Success:** `201` with `Data.InternationalPaymentId` (e.g. `"19906"`) and `Data.Status: "ACSP"`.

**Demo-data fixture:**
```json
{
  "Data": {
    "InternationalPaymentId": "19906",
    "ConsentId": "45104",
    "Status": "ACSP",
    "CreationDateTime": "2026-08-06T09:04:36+00:00"
  }
}
```

---

## 5 — Get international payment status

**GET** `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp/international-payments/{InternationalPaymentId}`

### Payment status ladder

| Status | Meaning | Disposition |
|--------|---------|-------------|
| `ACSP` | AcceptedSettlementInProcess | `in_progress` (secondaryContainer chip) |
| `ACCC` | AcceptedCreditSettlementCompleted | `terminal_success` (primaryContainer chip) |

Settlement is batched on five-minute boundaries (observed booking timestamps on 19906–19911).
`ACSP` persists for minutes on a payment that will succeed — this is normal and must not be styled
as a problem or shortened with a faster poll.

**Read-back response shape:** `Charges`, `CutOffDateTime`, `ExpectedExecutionDateTime`, and
`ExpectedSettlementDateTime` are **absent** from every read-back on this rail (verified: 19906,
19907, 19910, 19911). Parse as nullable.

**Demo-data fixture:**
```json
{
  "Data": {
    "InternationalPaymentId": "19906",
    "Status": "ACCC",
    "StatusUpdateDateTime": "2026-08-06T09:06:10+00:00"
  }
}
```

---

## Error contract

All 400 responses arrive in the envelope documented in `dtos/ObPaymentError.yaml`.

**Rendering rules for this screen:**

1. `Errors` is an **array** and may carry two entries. Render every entry in wire order. Never
   render only `Errors[0]` — the second entry is frequently the actionable one (R13-10 and R9-11
   both return `U027 @ CreditorAccount.SchemeName` then `U002 "Debtor and Creditor Account cannot
   be same"`; the second is the one the PSU can act on).

2. The scheme check (`U027`) fires **before** the business rule (`U002`) — preserve wire order.

3. Copy is keyed by `ErrorCode + Path`, never by `Message`. `U004` alone carries four distinct
   Message strings across the corpus; a Message-keyed switch stops matching when HSBC edits a string.

### Error codes on this rail

| Code | HTTP | Trigger | Recovery |
|------|------|---------|----------|
| `U004` | 400 | `ChargeBearer` omitted | Implementation fault |
| `U004` | 400 | `CurrencyOfTransfer` omitted | Implementation fault |
| `U004` | 400 | `CreditorAgent` sent without `Identification` | Implementation fault |
| `U005` | 400 | `RemittanceInformation` sent | Implementation fault |
| `U005` | 400 | `ExchangeRateInformation` sent | Implementation fault |
| `U027` | 400 | Sort-code creditor | Unreachable — form only accepts IBAN |
| `U027` | 400 | HSBC local-account schemes (`UK.HSBC.LocalAccountNumber`) | Unreachable — no local rail on this sandbox |
| `U002` | 400 | 8-character BIC | Return to Recipient step |
| `U002` | 400 | Global Money business-rule violations | Return to Recipient or Amount step |
| `U019` | 400 | Missing `x-jws-signature` | Not user-recoverable |
| `U009` | 400 | Consent not authorised | Re-authorise |

**Two-entry error fixture** (R13-10 — the fixture the error panel must be built against):
```json
{
  "Errors": [
    { "ErrorCode": "U027", "Message": "Unsupported scheme", "Path": "Data.Initiation.CreditorAccount.SchemeName" },
    { "ErrorCode": "U002", "Message": "Debtor and Creditor Account cannot be same", "Path": "Data.Initiation.DebtorAccount.Identification" }
  ]
}
```

---

<!-- Generated 2026-08-07 by /idea-feature-export from screens/pay-international-single/api.yaml. -->
