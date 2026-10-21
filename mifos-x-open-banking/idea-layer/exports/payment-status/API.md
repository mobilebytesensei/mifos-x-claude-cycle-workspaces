# Payment Status — API Reference

> Source: `screens/payment-status/api.yaml` (schema 4.0, rewritten 2026-08-06)
> Base: `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp`
> Auth: `client_credentials_payments_scope` on all operations
> DTOs: `ObPaymentStatus`, `ObPaymentError`

---

## Seven-Family Endpoint Resolution

The screen resolves its endpoint AND status ladder from the `paymentFamily` nav param.
There is no single shared resource path — seven families, four ladders, two status encodings.

| paymentFamily                   | Resource path                     | ID field                     | Consent path                         | Ladder               |
|---------------------------------|-----------------------------------|------------------------------|--------------------------------------|----------------------|
| domestic-payment                | domestic-payments                 | DomesticPaymentId            | domestic-payment-consents            | single               |
| domestic-scheduled-payment      | domestic-scheduled-payments       | DomesticScheduledPaymentId   | domestic-scheduled-payment-consents  | domestic_deferred    |
| domestic-standing-order         | domestic-standing-orders          | DomesticStandingOrderId      | domestic-standing-order-consents     | domestic_deferred    |
| international-payment           | international-payments            | InternationalPaymentId       | international-payment-consents       | single               |
| international-scheduled-payment | international-scheduled-payments  | InternationalScheduledPaymentId | international-scheduled-payment-consents | international_deferred |
| international-standing-order    | international-standing-orders     | InternationalStandingOrderId | international-standing-order-consents | international_deferred |
| domestic-vrp                    | domestic-vrps                     | DomesticVRPId                | domestic-vrp-consents                | vrp                  |

---

## Four Status Ladders

| Ladder               | Families                                    | Resource progression | Render rule                                    |
|----------------------|---------------------------------------------|-----------------------|------------------------------------------------|
| single               | domestic-payment, international-payment     | ACSP → ACCC           | ACSP = in_progress (never "sent"); ACCC = terminal_success |
| domestic_deferred    | domestic-scheduled, domestic-standing-order | PDNG → INCO           | Both = instruction_established; neither means money moved |
| international_deferred | international-scheduled, international-standing-order | INCO → INCO | Never emits PDNG; INCO on first read is normal |
| vrp                  | domestic-vrp                               | ACSP → ACCC; consent stays AUTH | 400 U011 on consent = revoked, not an error |

---

## Operation A1: `get_payment_status`

```
GET /{familyResourcePath}/{paymentId}
```

Pure read on every family. No JWS, no idempotency key.

### Response: HTTP 200

```json
{
  "Data": {
    "{id_field}": "string — name varies by family (see resolution table)",
    "ConsentId": "string",
    "Status": "enum — MUST match both v4.0 short form and v3.1 long form",
    "CreationDateTime": "datetime",
    "StatusUpdateDateTime": "datetime — INERT, equals CreationDateTime even across ACSP→ACCC",
    "Initiation": {
      "InstructedAmount": { "Amount": "string", "Currency": "string" },
      "FirstPaymentAmount": { "Amount": "string", "Currency": "string" },
      "DebtorAccount": { "SchemeName": "string", "Identification": "string", "Name": "string" },
      "CreditorAccount": { "SchemeName": "string", "Identification": "string", "Name": "string" },
      "RemittanceInformation": { "Unstructured": ["string"] },
      "MandateRelatedInformation": {
        "Frequency": { "Type": "string" },
        "FirstPaymentDateTime": "datetime",
        "FinalPaymentDateTime": "datetime"
      }
    },
    "Charges": [
      {
        "ChargeBearer": "BorneByDebtor — always, regardless of Initiation.ChargeBearer",
        "Type": "UK.OBIE.CHAPSOut — on ALL 116 observed objects; do not render raw",
        "Amount": { "Amount": "0.00 — always zero in observed corpus", "Currency": "GBP" }
      }
    ],
    "Refund": { "Account": { "SchemeName": "string", "Identification": "string", "Name": "string" } },
    "CutOffDateTime": "datetime — stub on deferred; never render",
    "ExpectedExecutionDateTime": "datetime — stub except VRP (CreationDateTime + 30s)",
    "ExpectedSettlementDateTime": "datetime — stub except VRP (CreationDateTime + 30s)"
  },
  "Links": { "Self": "string" },
  "Meta": { "TotalPages": 1 }
}
```

### Field rules

| Field                        | Rule                                                                                               |
|------------------------------|----------------------------------------------------------------------------------------------------|
| `Data.Status`                | Match BOTH v4.0 short (`ACCC`) and v3.1 long (`AcceptedCreditSettlementCompleted`) on every endpoint. Unrecognised → `in_progress`. |
| `Data.StatusUpdateDateTime`  | Inert — do not poll or diff. Equals `CreationDateTime` even after ACSP→ACCC transitions.          |
| `Data.Charges`               | ABSENT (not empty) on international families. Parse as nullable — never default to `[]`.           |
| `Charges[].Type`             | Never render raw. UK.OBIE.CHAPSOut appears on every observed object including EUR/USD transfers.   |
| `Charges[].ChargeBearer`     | Show this value or neither; never show `Initiation.ChargeBearer`. They contradict each other.      |
| `Charges[].Amount`           | Quote only, marked "estimated". Every observed transaction shows 0.00 regardless of quoted figure. |
| `ExpectedExecutionDateTime`  | Never render on deferred families — equals `CreationDateTime`. VRP only: `CreationDateTime + 30s` (legitimate settling window). |
| `ExpectedSettlementDateTime` | Same rule as above.                                                                                |
| `CutOffDateTime`             | Never render on any family.                                                                        |
| `Data.Initiation`            | Source of the REQUESTED execution date shown instead of stub fields.                               |
| `ExchangeRateInformation`    | NEVER present on any family. Do not render an FX rate or converted amount.                         |

### Dual Encoding Rule

Every status code MUST be matched against both its v4.0 short form and its v3.1 long form on
EVERY endpoint. The same endpoint rendered payment 19933 on `domestic-vrps` as `ACCC` at
15:12:26 and as `AcceptedCreditSettlementCompleted` on a later re-read with nothing changed.
Do NOT special-case `domestic-vrps`. A short-code-only mapper reads a completed VRP payment as
permanently in progress (fail-open sends unknowns to in_progress).

Full short-form ↔ long-form mapping:

| Short   | Long form                               | Disposition               |
|---------|-----------------------------------------|---------------------------|
| ACSP    | AcceptedSettlementInProcess             | in_progress               |
| AWOP    | AcceptedWithoutPosting                  | in_progress               |
| PDNG    | Pending                                 | in_progress               |
| ACCC    | AcceptedCreditSettlementCompleted       | terminal_success          |
| ACSC    | AcceptedSettlementCompleted             | terminal_success          |
| RJCT    | Rejected                               | terminal_failure          |
| BLCK    | Blocked                                 | terminal_failure          |
| INCO    | InitiationCompleted                     | instruction_established   |
| (other) | (any unrecognised string)               | in_progress (fail-open)   |

---

## Operation A2: `get_consent_status`

```
GET /{familyConsentPath}/{consentId}
```

Read alongside the resource on all six PIS families to distinguish a normally-consumed consent
from a rejected one. On VRP this is the PRIMARY read — mandate health lives on the consent.

### Response: HTTP 200

```json
{
  "Data": {
    "ConsentId": "string",
    "Status": "enum — AWAU | AUTH | COND | RJCT",
    "StatusUpdateDateTime": "datetime — inert (same as resource read)",
    "Initiation": {
      "DebtorAccount": "bank-authoritative after AUTH — carries the account the PSU selected"
    }
  },
  "Links": { "Self": "string" },
  "Meta": { "TotalPages": 1 }
}
```

### Consent status meanings

| Status | Meaning                                                                                     |
|--------|---------------------------------------------------------------------------------------------|
| AWAU   | Awaiting PSU authorisation                                                                  |
| AUTH   | Authorised — normal steady state on VRP (stays AUTH forever); transient on the six PIS families |
| COND   | Consumed — the six PIS families move here once the payment resource is created              |
| RJCT   | Rejected by the PSU at the bank                                                             |

VRP note: `AUTH` on a VRP consent is NOT proof the mandate can pay. A card-funded consent can
reach AUTH and then fail every payment with U021. Mandate health is derived from payment
outcomes, not from this consent status.

---

## Error Codes

| HTTP | Code  | Trigger                              | Render as                                     | Recovery                               |
|------|-------|--------------------------------------|-----------------------------------------------|----------------------------------------|
| 400  | U011  | VRP consent GET after revocation     | MandateRevoked — from local record, not error  | Offer new mandate, never retry         |
| 404  | —     | Unknown paymentId                    | PaymentNotFound                               | Back CTA; no retry                     |
| 401  | —     | Expired token                        | TokenExpired                                  | Retry after token refresh              |
| 403  | —     | Consent revoked or expired           | ConsentRevoked — settled payments unaffected   | View Consents CTA                      |
| 429  | U002  | Rate limited during poll             | Keep last known status; double poll interval   | No error banner needed                 |
| I/O  | —     | Network error / timeout              | NetworkError                                  | Retry CTA                              |

U011 path format note: the `Path` field in a U011 error body contains a URL
(`/domestic-vrp-consents/45205`), not a JSON pointer. A generic Path-to-field mapper will
misfire — U011 must be special-cased before any path resolution.

---

## No Per-Execution Status

For the four deferred families (`domestic-scheduled-payment`, `domestic-standing-order`,
`international-scheduled-payment`, `international-standing-order`), OBIE exposes no
per-execution status at all. The resource status describes the instruction's SETUP:

- `PDNG` (domestic deferred only): instruction received, pending submission.
- `INCO`: instruction successfully submitted to the bank. Terminal. Does not change.

Both map to `instruction_established`. The screen must say individual future payments cannot
be tracked here. No progress indicator implying instalments are being counted.

No AIS fallback is possible — PIS-created instructions have no shared identifier with AIS
standing-order elements (StandingOrderId is absent from every AIS element). Never tell a PSU
to check the standing-orders list to verify the instruction was created.
