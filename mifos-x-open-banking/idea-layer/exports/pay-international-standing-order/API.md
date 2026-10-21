# Overseas Standing Order — API Contracts

> Source: `screens/pay-international-standing-order/api.yaml` schema 4.0
> Host: `https://secure.sandbox.ob.hsbc.co.uk`
> Base path: `/obie/open-banking/v4.0/pisp`
> Auth server: `https://sandbox.ob.hsbc.co.uk/obie/open-banking/v1.1/oauth2/authorize`
> Auth scheme: mTLS + `private_key_jwt` (PS256) + authorization-code — FAPI 1.0 Advanced
> Endpoints: 4

---

## CRITICAL — InstructedAmount vs. FirstPaymentAmount

This rail and the domestic standing-order rail gather nearly identical inputs and differ in exactly one field. They are proven mutually exclusive (Round 15, both directions):

| Rail | Amount field on the wire | Field refused | Error on wrong field |
|---|---|---|---|
| **domestic** standing order | `FirstPaymentAmount` | `InstructedAmount` | U005 Field is not expected |
| **international** standing order | `InstructedAmount` | `FirstPaymentAmount` | U005 Field is not expected |

Copying the domestic mandate screen and changing the endpoint yields U005 on every submit. The error names a field the developer believes is correct, making the failure look like a bank problem rather than a client one.

Also refused on all international shapes (U005):
- `RemittanceInformation`
- `ExchangeRateInformation` — all three RateType values (Actual, Indicative, Agreed)

There is no `RecurringPaymentAmount` or `FinalPaymentAmount` on this rail. Those siblings belong to the FirstPaymentAmount shape, which this rail refuses.

---

## Frequency enum — exactly five values

`MandateRelatedInformation.Frequency.Type` accepts exactly:

| Value | Meaning |
|---|---|
| `WEEK` | Weekly |
| `FRTN` | Fortnightly |
| `MNTH` | Monthly |
| `QURT` | Quarterly |
| `YEAR` | Annual |

Values that return U002 (tested): `DAIL`, `ADHO`, `INDA`, `MIAN`. The frequency picker must offer exactly these five values and no others.

---

## Endpoint Summary

| # | Method | Endpoint | Auth | Success |
|---|---|---|---|---|
| 1 | POST | /international-standing-order-consents | client_credentials_payments_scope | 201 |
| 2 | GET | /international-standing-order-consents/{ConsentId} | client_credentials_payments_scope | 200 |
| 3 | POST | /international-standing-orders | psu_authorization_code | 201 |
| 4 | GET | /international-standing-orders/{InternationalStandingOrderId} | client_credentials_payments_scope | 200 |

---

## 1. POST /international-standing-order-consents — Stage consent

**Auth**: `client_credentials_payments_scope`

**Headers required**: `x-jws-signature`, `x-idempotency-key`

### Request body

```json
{
  "Data": {
    "Permission": "Create",
    "Initiation": {
      "MandateRelatedInformation": {
        "Frequency": {
          "Type": "WEEK | FRTN | MNTH | QURT | YEAR"
        },
        "FirstPaymentDateTime": "<ISO 8601 — optional>",
        "FinalPaymentDateTime": "<ISO 8601 — optional; omit for open-ended mandate>"
      },
      "InstructedAmount": {
        "Amount": "<major-unit string e.g. '1.02'>",
        "Currency": "<ISO 4217 e.g. 'USD'>"
      },
      "CreditorAccount": {
        "SchemeName": "UK.OBIE.IBAN",
        "Identification": "<IBAN e.g. 'FR29NWBK60161331926819'>",
        "Name": "<payee name>"
      },
      "CurrencyOfTransfer": "<ISO 4217 — independent of InstructedAmount.Currency>",
      "ChargeBearer": "BorneByCreditor | Shared | BorneByDebtor",
      "CreditorAgent": {
        "_presence": "optional",
        "SchemeName": "UK.OBIE.BICFI",
        "Identification": "<11-character BIC only — 8-char returns U002; object must be whole or absent>"
      },
      "DebtorAccount": {
        "_presence": "optional — accepted but NOT sent by this form",
        "SchemeName": "<scheme>",
        "Identification": "<identifier>",
        "_name_forbidden": "Name is NEVER sent in DebtorAccount on this rail"
      }
    }
  },
  "Risk": {}
}
```

**Mandatory fields** (omission returns U004):
- `Data.Permission` = `"Create"`
- `Data.Initiation.CurrencyOfTransfer`
- `Data.Initiation.ChargeBearer`

**Fields refused on this rail** (all return U005):
- `Data.Initiation.FirstPaymentAmount`
- `Data.Initiation.RecurringPaymentAmount`
- `Data.Initiation.FinalPaymentAmount`
- `Data.Initiation.RemittanceInformation`
- `Data.Initiation.ExchangeRateInformation` (all three RateType values)
- `Data.Initiation.MandateRelatedInformation.Frequency.PointInTime`

**CreditorAgent wholeness trap**: sending `CreditorAgent` at all makes `Identification` mandatory. An 8-character BIC returns U002 (length-driven, not country-mismatch-driven). Send the complete object or omit it entirely.

**Open-ended mandate**: omitting `FinalPaymentDateTime` stages 201 as an open-ended mandate. Combined with amendment_prohibition (the PSU cannot cancel through this app), this is a materially different commitment from a bounded mandate.

### Response — 201

```json
{
  "Data": {
    "ConsentId": "45173",
    "CreationDateTime": "2026-08-06T10:36:21+00:00",
    "Status": "AWAU",
    "StatusUpdateDateTime": "2026-08-06T10:36:21+00:00",
    "Permission": "Create",
    "Initiation": {
      "ChargeBearer": "BorneByCreditor",
      "CurrencyOfTransfer": "USD",
      "InstructedAmount": { "Amount": "1.02", "Currency": "USD" },
      "MandateRelatedInformation": {
        "Frequency": { "Type": "MNTH" },
        "FirstPaymentDateTime": "2026-08-13T10:36:18+00:00",
        "FinalPaymentDateTime": "2027-02-24T10:36:18+00:00"
      },
      "CreditorAccount": {
        "SchemeName": "UK.OBIE.IBAN",
        "Identification": "FR29NWBK60161331926819",
        "Name": "Mr Mark"
      }
    }
  },
  "Risk": {}
}
```

**Key observations**:
- `Charges`, `CutOffDateTime`, `ExpectedExecutionDateTime`, `ExpectedSettlementDateTime` are **KEY ABSENT** from every international consent — not an empty object or empty array. Parse `Charges` as nullable. Defaulting to `[]` renders a 0.50 mandate as free.
- Server **reorders** `Initiation` keys on echo. Echo the PARSED object from read-back into the submit body; never re-serialise the local model and string-compare.
- `Risk {}` — empty. This rail carries neither `CategoryPurposeCode` nor `PaymentContextCode` on any observed scenario.
- `ConsentId` is a short sequential integer-as-string (e.g. `"45173"`) — not a UUID, not deep-linkable, must not be logged.

---

## 2. GET /international-standing-order-consents/{ConsentId} — Poll consent status

**Auth**: `client_credentials_payments_scope`

**Status ladder**: `AWAU → AUTH → COND`

Poll until `AUTH`. `StatusUpdateDateTime` does not advance on the `AWAU → AUTH` transition.

```json
{
  "Data": {
    "ConsentId": "45173",
    "Status": "AUTH",
    "StatusUpdateDateTime": "2026-08-06T10:36:21+00:00"
  }
}
```

---

## 3. POST /international-standing-orders — Submit standing order

**Auth**: `psu_authorization_code` (after PSU authorises at their bank)

**Headers required**: `x-jws-signature`, `x-idempotency-key`

### Request body

```json
{
  "Data": {
    "ConsentId": "45173",
    "Initiation": "<parsed Initiation object from GET /international-standing-order-consents/{ConsentId}>"
  },
  "Risk": {}
}
```

Echo the **parsed** read-back object, not a re-serialised local model. The server reorders Initiation keys.

### Response — 201

```json
{
  "Data": {
    "InternationalStandingOrderId": "19917",
    "ConsentId": "45173",
    "Status": "INCO",
    "CreationDateTime": "2026-08-06T10:37:45+00:00",
    "Charges": [
      {
        "ChargeBearer": "BorneByCreditor",
        "Type": "UK.OBIE.CHAPSOut",
        "Amount": { "Amount": "0.50", "Currency": "USD" }
      }
    ]
  }
}
```

**Key observations**:
- Status is `INCO` at creation — this rail **never** emits `PDNG`.
- Charge: 0.50 in `InstructedAmount.Currency`, not `CurrencyOfTransfer`. Evidence: resource 19918 — 5.00 GBP instructed, USD transfer, charge 0.50 GBP.
- Whether the 0.50 recurs per execution or applies once at setup is not stated. The screen must not answer either way.

---

## 4. GET /international-standing-orders/{InternationalStandingOrderId} — Read status

**Auth**: `client_credentials_payments_scope`

**Status ladder**: `INCO → INCO`

No further status transitions. There is no per-execution status on this rail. PIS-created mandates do not surface in AIS and cannot be correlated with AIS standing-order reads. A PISP cannot amend or cancel the mandate — the customer must use their bank's own channel.

```json
{
  "Data": {
    "InternationalStandingOrderId": "19917",
    "Status": "INCO"
  }
}
```

---

## Error Code Reference

| Code | HTTP | Trigger | Notes |
|---|---|---|---|
| U004 | 400 | Required field omitted | Permission, CurrencyOfTransfer, ChargeBearer each independently produce U004 |
| U005 | 400 | Unexpected field sent | FirstPaymentAmount, RemittanceInformation, ExchangeRateInformation |
| U002 | 400 | Invalid field value | Frequency outside 5 values; BIC not 11 characters |
| U003 | 400 | Invalid mandate dates | Final before first, beyond 12 months, or today/tomorrow |
| U027 | 400 | Creditor unresolvable | Resolved-account dependent — not scheme driven; same scheme string gives different outcomes |
| U019 | 400 | Missing JWS signature | Not user-recoverable |
| U009 | 400 | Consent not authorised | Re-authorise |

**Error array**: `Errors` is an array and can carry two entries. SO-I04 returns two U002 Global Money rules together; SO-I05 fixes the first and receives the second alone. The scheme check (U027) precedes the business rule (U002). Render every entry in wire order — never just `Errors[0]`. Copy keyed by `ErrorCode + Path`, never by `Message` (U004 carries four different Message strings across the corpus).

---

## FX Contract

`ExchangeRateInformation` is refused for all three RateType values: Actual (R16-O1), Indicative (R16-O2), Agreed with a real rate 1.15 and contract identifier (R16-O3). Controls without the block staged 201. The same refusal holds on the single and scheduled international rails.

OBIE has no per-execution FX model. HSBC calls FX quoting "not applicable" for international scheduled and standing orders. Convergent bank evidence (Citi, Bank of Scotland, Coutts) points to the rate prevailing at each execution, but none is authoritative for HSBC. No rate, projected total, or estimated received amount appears anywhere on this screen. The `fx_not_fixed_notice` banner (warning severity) is the definitive FX disclosure — not a placeholder for a rate source that will be integrated later.

---

## Charge Currency Evidence

| Resource | InstructedAmount.Currency | CurrencyOfTransfer | Charge | Rule confirmed |
|---|---|---|---|---|
| 19917 | USD | USD | 0.50 USD | consistent (currencies equal — not decisive) |
| 19918 | GBP | USD | 0.50 GBP | **decisive** — charge follows instructed, not transfer |

---

## U027 — Creditor Resolution

`U027 @ CreditorAccount.SchemeName` is resolved-account dependent, not scheme dependent. The same scheme string `UK.OBIE.SortCodeAccountNumber` with Identification `80119770009652` (Global Money GMA) stages 201, while a different sort-code creditor under the same scheme returns U027. The same split appears on the scheduled rail (SP-I08 refused against SP-I05 accepted). This form takes an IBAN, so U027 is unreachable in practice.
