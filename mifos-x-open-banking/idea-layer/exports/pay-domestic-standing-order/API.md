# Standing Order (Domestic) — API Contracts

> Generated from `screens/pay-domestic-standing-order/api.yaml` by `/idea-feature-export`
> Schema version: 4.0  Contract version: 2.1.0
> Host: `https://secure.sandbox.ob.hsbc.co.uk`
> Base path: `/obie/open-banking/v4.0/pisp`
> Auth base: `https://sandbox.ob.hsbc.co.uk/obie/open-banking/v1.1/oauth2/authorize`
> Auth scheme: mTLS + private_key_jwt (PS256) + authorization-code, FAPI 1.0 Advanced
> Endpoints: 4

## Rail Summary

This is a **MANDATE rail**, not a single-payment rail. The payload is intentionally smaller:
`DebtorAccount`, `LocalInstrument`, `InstructionIdentification`, `EndToEndIdentification`,
and `RemittanceInformation` at the mandate-model level are all absent. The bank picks the
settlement rail per instalment, which is why `LocalInstrument` disappears. `Risk` is an empty
object `{}` because there is no single e-commerce context for a recurring instruction.

**Critical field distinction**: this rail uses `FirstPaymentAmount`, NOT `InstructedAmount`.
The international standing order is the exact inverse. Sending `InstructedAmount` on this
rail returns `U005 Field is not expected`. Sending `FirstPaymentAmount` on the international
rail also returns `U005`. These rails share no amount field.

**Reference channel**: `Data.Initiation.RemittanceInformation.Unstructured[0]` is ACCEPTED
(R17-D01 → 201). `MandateRelatedInformation.Reference` is REFUSED on both the domestic and
international standing-order rails. The Unstructured path is where the reference belongs.

## Endpoint Summary

| # | ID | Method | Path | Auth |
|---|----|--------|------|:----:|
| 1 | stage_domestic_standing_order_consent | POST | /domestic-standing-order-consents | client_credentials_payments_scope |
| 2 | get_domestic_standing_order_consent_status | GET | /domestic-standing-order-consents/{ConsentId} | client_credentials_payments_scope |
| 3 | submit_domestic_standing_order | POST | /domestic-standing-orders | psu_authorization_code |
| 4 | get_domestic_standing_order_status | GET | /domestic-standing-orders/{DomesticStandingOrderId} | client_credentials_payments_scope |

---

## Endpoint Details

### 1. `stage_domestic_standing_order_consent` — Stage consent for a new standing order

| Attribute | Value |
|-----------|-------|
| Method | POST |
| Path | `/obie/open-banking/v4.0/pisp/domestic-standing-order-consents` |
| Auth | client_credentials — scope `payments` |
| Required headers | `x-jws-signature` (PS256 detached JWS), `x-idempotency-key` |

#### Request Body

```json
{
  "Data": {
    "Permission": "Create",
    "Initiation": {
      "MandateRelatedInformation": {
        "Frequency": {
          "Type": "WEEK | FRTN | MNTH | QURT | YEAR"
        },
        "FirstPaymentDateTime": "2026-08-13T10:38:41+00:00",
        "FinalPaymentDateTime": "2026-12-04T10:38:41+00:00"
      },
      "FirstPaymentAmount": {
        "Amount": "25.00",
        "Currency": "GBP"
      },
      "RecurringPaymentAmount": {
        "Amount": "25.00",
        "Currency": "GBP"
      },
      "FinalPaymentAmount": {
        "Amount": "25.00",
        "Currency": "GBP"
      },
      "CreditorAccount": {
        "SchemeName": "UK.OBIE.SortCodeAccountNumber",
        "Identification": "80200110203349",
        "Name": "Mr Mark"
      },
      "RemittanceInformation": {
        "Unstructured": ["Monthly rent"]
      }
    }
  },
  "Risk": {}
}
```

#### Request Field Rules

| Field | Mandatory? | Constraint | Error if Violated |
|-------|:----------:|------------|:-----------------:|
| Data.Permission | Yes | Must be exactly `"Create"` | U004 |
| Data.Initiation.MandateRelatedInformation | Yes | HSBC TIGHTENS OBIE: OBIE says 0..1, HSBC returns U004 if omitted | U004 |
| MandateRelatedInformation.Frequency | Yes | Required when MandateRelatedInformation present | U004 |
| MandateRelatedInformation.Frequency.Type | Yes | Exactly one of: WEEK, FRTN, MNTH, QURT, YEAR | U002 |
| MandateRelatedInformation.Frequency.PointInTime | Forbidden | REFUSED — U005 even though AIS returns it on read | U005 |
| MandateRelatedInformation.Reference | Forbidden | REFUSED on both domestic and international rails | U005 |
| MandateRelatedInformation.FirstPaymentDateTime | App-required | Schema-optional (R17-B01 → 201 without it) but always sent so review screen has a real first date | — |
| MandateRelatedInformation.FinalPaymentDateTime | Optional | If present: after FirstPaymentDateTime, within 12 months, not today/tomorrow | U003 |
| Data.Initiation.FirstPaymentAmount | Yes | QUOTED 2dp string — "25.00". THIS rail's amount field. | U004 |
| Data.Initiation.InstructedAmount | Forbidden | U005 Field is not expected on this rail | U005 |
| Data.Initiation.RecurringPaymentAmount | Optional | QUOTED 2dp string; Guide §20.2.1 requires it equals FirstPaymentAmount if present (not enforced at staging) | — |
| Data.Initiation.FinalPaymentAmount | Optional | QUOTED 2dp string; requires hasEndDate = true; same equality caveat | — |
| Data.Initiation.DebtorAccount | Forbidden | Not in the standing-order schema | — |
| Data.Initiation.LocalInstrument | Forbidden | Not in schema; bank picks rail per instalment | — |
| Data.Initiation.InstructionIdentification | Forbidden | Not in schema | — |
| Data.Initiation.EndToEndIdentification | Forbidden | Not in schema | — |
| Data.Initiation.RemittanceInformation.Unstructured | Optional | Array of strings, max 35 chars each; ACCEPTED (R17-D01 → 201) | — |
| Data.Initiation.RemittanceInformation.Structured | Optional | Must be an ARRAY (not bare object); ACCEPTED (R17-D03 → 201) | U002 if bare object |
| Risk | Yes | Must be present as empty object `{}` | — |

#### Frequency Enum — Five Accepted Values

| OBIE Code | Consumer Label | Accepted by HSBC Personal |
|-----------|---------------|:------------------------:|
| WEEK | Weekly | Yes |
| FRTN | Every 2 weeks | Yes |
| MNTH | Monthly | Yes |
| QURT | Every 3 months | Yes |
| YEAR | Yearly | Yes |
| ADHO | — | No — U002 |
| INDA | — | No — U002 (named in Guide §20.3.1) |
| MIAN | — | No — U002 (named in Guide §20.3.1) |
| DAIL | — | No — U002 (NOT named in §20.3.1; the Guide's exclusion list is incomplete) |

#### FinalPaymentDateTime Constraints (all three from single U003 message)

All three constraints are enforced client-side by the picker's bounds because U003 is ONE
undifferentiated error message carrying all three rules. The app cannot tell which rule
fired from the response.

| Constraint | Rule |
|------------|------|
| After first payment date | FinalPaymentDateTime > FirstPaymentDateTime |
| Within 12 months | FinalPaymentDateTime ≤ today + 12 months |
| Not today or tomorrow | FinalPaymentDateTime > today + 2 days |

#### Wire Type Rules

| Field Type | Wire Format | Example | Error if Wrong |
|------------|------------|---------|:-------------:|
| Amount | Quoted 2dp string | `"25.00"` | U002/U004 |
| CountPerPeriod | Unquoted JSON number | `12` | U002 |
| PointInTime | Quoted zero-padded string | `"01"` | Refused (U005) on write |

#### Response (201 Created)

```json
{
  "Data": {
    "ConsentId": "45171",
    "Status": "AWAU",
    "StatusUpdateDateTime": "2026-08-06T10:32:58+00:00",
    "Permission": "Create",
    "Initiation": {
      "MandateRelatedInformation": {
        "FirstPaymentDateTime": "2026-08-13T10:32:55+00:00",
        "FinalPaymentDateTime": "2026-12-04T10:32:55+00:00",
        "Frequency": { "Type": "WEEK" }
      },
      "FirstPaymentAmount": { "Amount": "25.00", "Currency": "GBP" },
      "CreditorAccount": {
        "SchemeName": "UK.OBIE.SortCodeAccountNumber",
        "Identification": "80200110203349",
        "Name": "Mr Mark"
      }
    },
    "Charges": [
      {
        "ChargeBearer": "BorneByDebtor",
        "Type": "UK.OBIE.CHAPSOut",
        "Amount": { "Amount": "0.05", "Currency": "GBP" }
      }
    ]
  },
  "Risk": {}
}
```

**Date echo**: `FirstPaymentDateTime` and `FinalPaymentDateTime` echo byte-identical (+00:00
offset preserved, seconds intact). The server normalises key ORDER inside Initiation and
MandateRelatedInformation but does not modify date values.

**Charge rendering**: render `Charges[].Amount` and `Currency` only. `Charges[].Type`
returns `UK.OBIE.CHAPSOut` on this standing-order rail — a CHAPS label on a recurring
domestic mandate that will not travel by CHAPS. Rendering `Type` tells the PSU something
false about how their money moves.

**ConsentId shape**: short sequential integer-as-string (`"45171"`). Enumerable, not a UUID.
Keep out of URLs, logs, crash reports and analytics.

#### Error Matrix

| Code | HTTP | Trigger | Retry | Recovery |
|------|:----:|---------|:-----:|----------|
| U004 | 400 | Permission omitted OR MandateRelatedInformation omitted | No | Implementation fault |
| U005 | 400 | InstructedAmount sent / PointInTime sent / MandateRelatedInformation.Reference sent | No | Implementation fault |
| U002 | 400 | Frequency.Type outside the five accepted values | No | Picker should prevent |
| U003 | 400 | FinalPaymentDateTime before first / beyond 12 months / today or tomorrow | No | Return to Schedule step |
| U019 | 400 | x-jws-signature missing or invalid | No | Not user-recoverable |

**U003 note**: R17-B03 proves that omitting `MandateRelatedInformation` returns only U004 on
the parent — the nested Frequency error is never emitted. A body with two faults reports one.
Validate the whole body locally before submitting.

---

### 2. `get_domestic_standing_order_consent_status` — Poll consent until AUTH

| Attribute | Value |
|-----------|-------|
| Method | GET |
| Path | `/obie/open-banking/v4.0/pisp/domestic-standing-order-consents/{ConsentId}` |
| Auth | client_credentials — scope `payments` |
| Poll target | STATUS == AUTH |

#### Status Ladder

| Status | Code | Meaning |
|--------|:----:|---------|
| Awaiting authorisation | AWAU | Consent staged; PSU not yet authorised at bank |
| Authorised | AUTH | PSU completed app-to-app authorisation |
| Consumed | COND | Standing order submitted; mandate is established |

`StatusUpdateDateTime` does NOT move on the AWAU → AUTH transition. Do not use it as an
"authorised at" timestamp.

#### Response (200 OK) — AUTH state example

```json
{
  "Data": {
    "ConsentId": "45171",
    "Status": "AUTH",
    "StatusUpdateDateTime": "2026-08-06T10:32:58+00:00",
    "Initiation": {
      "DebtorAccount": {
        "SchemeName": "UK.OBIE.PAN",
        "Identification": "1234567890123456"
      },
      "MandateRelatedInformation": {
        "Frequency": { "Type": "WEEK" },
        "FirstPaymentDateTime": "2026-08-13T10:32:55+00:00",
        "FinalPaymentDateTime": "2026-12-04T10:32:55+00:00"
      },
      "FirstPaymentAmount": { "Amount": "25.00", "Currency": "GBP" }
    }
  }
}
```

**Bank-written DebtorAccount**: after authorisation the bank injects a `DebtorAccount`
(UK.OBIE.PAN) into the consent even though the TPP could not send one. Echo this in the
submit body — it is what the mandate must match.

---

### 3. `submit_domestic_standing_order` — Create the standing order resource

| Attribute | Value |
|-----------|-------|
| Method | POST |
| Path | `/obie/open-banking/v4.0/pisp/domestic-standing-orders` |
| Auth | psu_authorization_code |
| Required headers | `x-jws-signature`, `x-idempotency-key` (reused from consent staging) |

#### Request Body

```json
{
  "Data": {
    "ConsentId": "45171",
    "Initiation": "<parsed Initiation object from the AUTHORISED consent GET response>"
  },
  "Risk": {}
}
```

**Echo rule**: forward the PARSED `Initiation` object from the authorised consent GET
response. Do NOT re-serialise and string-compare: the server normalises key order on every
echo (inside `MandateRelatedInformation`, response emits `FirstPaymentDateTime`,
`FinalPaymentDateTime`, `Frequency` — though requests send `Frequency` first; inside
`Frequency`, response emits `CountPerPeriod` before `Type`). The date VALUES echo
byte-identical, but the object structure is reordered.

#### Response (201 Created)

```json
{
  "Data": {
    "DomesticStandingOrderId": "19916",
    "ConsentId": "45171",
    "Status": "PDNG",
    "CreationDateTime": "2026-08-06T10:35:56+00:00"
  }
}
```

#### Error Matrix

| Code | HTTP | Trigger | Retry |
|------|:----:|---------|:-----:|
| U009 | 400 | Consent not in AUTH status | Yes |
| IOException | — | Network timeout | Yes |

---

### 4. `get_domestic_standing_order_status` — Read mandate status

| Attribute | Value |
|-----------|-------|
| Method | GET |
| Path | `/obie/open-banking/v4.0/pisp/domestic-standing-orders/{DomesticStandingOrderId}` |
| Auth | client_credentials — scope `payments` |

#### Status Ladder

| Status | Code | Disposition | Chip |
|--------|:----:|-------------|------|
| Pending | PDNG | instruction_established | `event_repeat` icon, neutral surfaceVariant chip |
| InitiationCompleted | INCO | instruction_established | `event_repeat` icon, neutral surfaceVariant chip |

**No per-execution status exists.** `PDNG → INCO` describes the MANDATE's setup — not that
money moved. A TPP cannot learn whether instalment 3 failed insufficient funds by any API
means. The UI must never render an instalment progress indicator and must never tell the
customer to check the standing-orders list.

**INCO render rule**: use `semantic.payment_disposition.instruction_established` (neutral
`surfaceVariant` chip, `event_repeat` icon, label "Standing order set up"). FORBIDDEN label
substrings: paid, sent, complete, completed, successful, any past-tense amount.

**AIS correlation**: A PIS-created standing order does NOT appear in the AIS standing-orders
list. `StandingOrderId` is absent from every AIS element; write-to-read correlation is
impossible by construction. Do not attempt a post-creation list refresh.

---

## Amendment Prohibition

A PISP cannot amend or cancel a standing order. There is no DELETE or PATCH on this
endpoint family. This is a MANDATORY obligation under OBL Customer Experience Guidelines:
the TPP must redirect the PSU to their bank's own channel.

The UI surfaces `amend_notice` (severity: warning) on the Review step AND the Success state.
This notice is not optional. The alternative for a mutable recurring payment is VRP.

---

## AIS Correlation Impossibility

**Tested**: standing order 19936 was pinned to account 80200110203349 (the one account whose
AIS standing-orders read returns 200). Five minutes after creation the AIS read returned
only the two pre-seeded 2019 fixtures. The mandate itself was healthy (INCO, consent COND).

**Structural cause**: `StandingOrderId` is absent from every element of the AIS
standing-orders read. There is no field that could ever hold a PIS `DomesticStandingOrderId`.

**Note on AIS-read mandates**: the AIS read side returns `PointInTime` in the Frequency
object — a field the WRITE side refuses with U005. An AIS-read standing order cannot be
replayed as a PIS consent without stripping `PointInTime` first.
