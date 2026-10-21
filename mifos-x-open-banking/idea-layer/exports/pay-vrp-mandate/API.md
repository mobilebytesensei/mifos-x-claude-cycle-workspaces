# API Reference — pay-vrp-mandate

**Base path:** `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp`  
**Authorise URL:** `https://sandbox.ob.hsbc.co.uk/obie/open-banking/v1.1/oauth2/authorize`  
**Auth scheme:** mTLS + `private_key_jwt` (PS256) + OAuth authorization-code, FAPI 1.0 Advanced  
**Currency:** GBP only on all amounts and limits  
**Scheme:** `UK.OBIE.SortCodeAccountNumber` required on **both** debtor and creditor sides

---

## Operation 1 — Create VRP Consent

**`POST /domestic-vrp-consents`**  
**Auth:** `client_credentials` with `payments` scope  
**Headers:** `x-jws-signature`, `x-idempotency-key`

Stages a new mandate. Runs **exactly once** per mandate lifetime. The consent reaches `AWAU` immediately; the PSU must then authorise it via the app-to-app leg before any payments can be made.

**Mandatory blocks — U004 if any are omitted:**
- `Data.ControlParameters`
- `Data.ControlParameters.MaximumIndividualAmount` (GBP)
- `Data.ControlParameters.PeriodicLimits` (array, at least one entry, GBP)

**Request shape:**
```json
{
  "Data": {
    "ReadRefundAccount": "Yes",
    "ControlParameters": {
      "MaximumIndividualAmount": { "Amount": "10.00", "Currency": "GBP" },
      "PeriodicLimits": [
        { "PeriodType": "Week", "PeriodAlignment": "Calendar", "Amount": "50.00", "Currency": "GBP" }
      ],
      "VRPType": ["UK.OBIE.VRPType.Sweeping"],
      "PSUAuthenticationMethods": ["UK.OBIE.SCANotRequired"],
      "PSUInteractionTypes": ["InSession"]
    },
    "Initiation": {
      "DebtorAccount": {
        "SchemeName": "UK.OBIE.SortCodeAccountNumber",
        "Identification": "12345679100000"
      },
      "CreditorAccount": {
        "SchemeName": "UK.OBIE.SortCodeAccountNumber",
        "Identification": "40180000133787",
        "Name": "test user"
      }
    }
  },
  "Risk": {}
}
```

**Success:** `201` with `Data.ConsentId` (short sequential integer string, e.g. `"45223"`) and `Data.Status: "AWAU"`

**No redirect link in the response.** The response carries only `Links.Self` and `Meta.TotalPages`. The app constructs the authorise URL from `Data.ConsentId` itself. An implementer searching the response body for a redirect URL will not find one.

**PSUAuthenticationMethods note:** `UK.OBIE.SCANotRequired` is the only accepted value. `UK.OBIE.SCA` returns `U002 Invalid value`. The name is misleading — SCA IS performed once at consent setup; the field describes delegated SCA, not the absence of SCA.

**Error codes on this operation:**

| Code | HTTP | Trigger |
|---|---|---|
| U004 | 400 | ControlParameters, PeriodicLimits or MaximumIndividualAmount omitted |
| U023 | 400 | MaximumIndividualAmount currency is not GBP |
| U005 | 400 | PeriodicLimits currency is not GBP |
| U002 | 400 | PSUAuthenticationMethods is `UK.OBIE.SCA`, or TPP-named Global Money debtor |
| U021 | 400 | Debtor or creditor is not on `UK.OBIE.SortCodeAccountNumber` |
| U019 | 400 | x-jws-signature missing or invalid |

**Validation trap:** The API short-circuits on the parent. Omitting `ControlParameters` returns only U004 on the parent — not the nested `PeriodicLimits` and `MaximumIndividualAmount` faults that are equally true. A round trip cannot produce a full fault list. Validate every control parameter client-side before submitting.

**Batched errors at the same level (VRP-16):** Both currency fields non-GBP returns two errors in field order — U023 on `MaximumIndividualAmount.Currency` then U005 on `PeriodicLimits[0].Currency`. Render every entry in `Errors[]`.

---

## Operation 2 — Get Consent Status

**`GET /domestic-vrp-consents/{ConsentId}`**  
**Auth:** `client_credentials`

Refreshes mandate status on list mount and before each payment attempt.

**Consent ladder:** `AWAU → AUTH` — and stays `AUTH`. The VRP consent state model **explicitly omits Consumed**. Every other payment family moves its consent to `COND` on first use; VRP does not. Verified on three authorised runs, two payments each, consent still `AUTH` afterwards. `StatusUpdateDateTime` does not move on `AWAU → AUTH`.

**After DELETE:** returns `400 U011` with `Path: "/domestic-vrp-consents/{ConsentId}"` — a URL path, not a JSON field pointer. This is not an error. Map U011 to revoked before any generic Path→field mapper runs. The generic mapper misfires on the leading slash.

**Health derivation:** Consent status is an input to health, never a synonym. Three of the four health states coexist with `AUTH`:
- `active` — AUTH, no recent ExemptionNotApplied
- `failing` — AUTH, recent payments carry `StatusReason: UK.OBIE.ExemptionNotApplied`
- `unpayable` — AUTH, local record shows `unpayableAt != null`
- `revoked` — local `revokedAt != null`, or this call returns 400 U011, or event poll returns `UK.OBIE.Consent-Authorization-Revoked`

---

## Operation 3 — Revoke (DELETE)

**`DELETE /domestic-vrp-consents/{ConsentId}`**  
**Auth:** `client_credentials`  
**Headers:** none

The **only DELETE in the entire payment surface**. PSD2 Article 80 forbids revoking an authorised payment-order consent for the other six families; the VRP profile explicitly grants revocation.

**Success:** `204` with an empty body.

**Write the local revoked record immediately after the 204.** Subsequent GETs return 400 U011 forever — there is no revoked status in the API. If the local write is skipped, the mandate becomes indistinguishable from a broken one.

**Payments made under a revoked mandate** still read back correctly on `GET /domestic-vrps/{id}`.

---

## Operation 4 — Funds Confirmation

**`POST /domestic-vrp-consents/{ConsentId}/funds-confirmation`**  
**Auth: PSU authorisation-code token — client_credentials returns 401**  
**Headers:** `x-jws-signature`, `x-idempotency-key`

Checks whether the amount about to be paid is present in the debtor account. **POST, not GET**, because a VRP consent has no fixed amount — the TPP supplies the one it is about to pay. A PISP single-payment consent carries one fixed amount already, so a GET suffices there.

**Request shape:**
```json
{
  "Data": {
    "ConsentId": "45223",
    "Reference": "VRP-check",
    "InstructedAmount": { "Amount": "5.00", "Currency": "GBP" }
  }
}
```

**Success:** `201` with:
```json
{ "Data": { "FundsAvailableResult": { "FundsAvailable": "Available" } } }
```

`FundsAvailable` is the **string** `"Available"` — not a boolean. Compare by string equality.

**Critical:** `"Available"` is **never** a promise that the payment will succeed. Consent 45224: funds-confirmation returned `"Available"`, then every payment failed 400 U021 because the bank had written a `UK.OBIE.PAN` debtor into the authorised consent. The check answers whether the amount is present, not whether the debtor can pay on this rail.

---

## Operation 5 — Create VRP Payment

**`POST /domestic-vrps`**  
**Auth: PSU authorisation-code token**  
**Headers:** `x-jws-signature`, `x-idempotency-key`

Executes a payment under an existing mandate. **No re-authentication.** The defining VRP property — one authorisation funds many payments.

**Initiation source rule:** Read the `Initiation` back from the **authorised** consent (`GET /domestic-vrp-consents/{ConsentId}`) immediately before this call. Never use the staged copy. When the TPP omits `DebtorAccount`, the bank overwrites `Initiation.DebtorAccount` with the PSU's choice. Submitting the stale staged copy is refused.

**Request shape:**
```json
{
  "Data": {
    "ConsentId": "45223",
    "Initiation": "<from authorised consent GET>",
    "VRPType": "UK.OBIE.VRPType.Sweeping",
    "Instruction": {
      "InstructionIdentification": "VRP<hex>",
      "EndToEndIdentification": "E2E<hex>",
      "InstructedAmount": { "Amount": "5.00", "Currency": "GBP" },
      "CreditorAccount": {
        "SchemeName": "UK.OBIE.SortCodeAccountNumber",
        "Identification": "40180000133787",
        "Name": "test user"
      },
      "RemittanceInformation": { "Unstructured": ["VRP-5.00"] }
    },
    "PSUAuthenticationMethod": "UK.OBIE.SCANotRequired"
  },
  "Risk": {}
}
```

`CreditorAccount` appears in both `Initiation` and `Instruction` — send it in both; they were identical on all eight observed payments.

`RemittanceInformation` lives in `Data.Instruction` only. `Data.Initiation` on a VRP payment has no `RemittanceInformation` member. Each payment carries its own reference; the consent's `Unstructured` value does not propagate into payments.

**Success:** `201` with:
- `Data.DomesticVRPId` — e.g. `"19929"`
- `Data.Status: "AcceptedCreditSettlementCompleted"` — v3.1 **long-name encoding** (not `ACCC`)
- `Data.ExpectedExecutionDateTime` and `Data.ExpectedSettlementDateTime` — exactly `CreationDateTime + 30 seconds` on all eight observed payments. The only place in the payment surface where these fields carry honest information.
- `Data.Charges: [{ "Type": "UK.OBIE.CHAPSOut", "Amount": { "Amount": "0.05", "Currency": "GBP" } }]` — charged per payment, on every debtor type

**Status encoding warning:** This endpoint returns the v3.1 long name `AcceptedCreditSettlementCompleted` where every other endpoint returns the v4.0 short code `ACCC`. A short-code-only mapper treats a completed payment as unrecognised and, per the fail-open rule, renders it as permanently in progress. The status mapper must accept both encodings.

**Append to the local spend ledger immediately** after a `201`. Nothing in the API tracks spend against periodic limits.

**Error codes on this operation:**

| Code | HTTP | Trigger | Action |
|---|---|---|---|
| U014 | 400 | Payment breaches MaximumIndividualAmount or any periodic limit | Show all limits — the bank does not say which was hit |
| U021 | 400 | Debtor or creditor not on SortCodeAccountNumber — including bank-written PAN debtor | Mark mandate `unpayable` locally; never retry |
| Fraud window rejection | 400 | Payment submitted 18:00–23:45; HSBC fraud checks | Show window, no auto-retry, health unchanged |

---

## Operation 6 — Get Payment Status

**`GET /domestic-vrps/{DomesticVRPId}`**  
**Auth:** `client_credentials`

Reads back a payment's status. Returns the v3.1 long-name encoding (see Operation 5 warning).

**Status ladder:** `ACSP → AcceptedCreditSettlementCompleted` (displayed as `ACCC` in the UI)

`StatusReason: UK.OBIE.ExemptionNotApplied` on a payment indicates the trusted-beneficiary exemption check failed. Accumulating this reason across recent payments drives the `failing` health state.

---

## Error Envelope

All errors conform to `dtos/ObPaymentError.yaml`. Key rules:
- Key off `ErrorCode + Path` — never off `Message`. U002 arrives as both `"Invalid Field"` (VRP-03) and `"Invalid value"` (VRP-12) on this family.
- Render **every** entry in `Errors[]` — errors can batch at the same level (VRP-16).
- Path notation inconsistency: bracket notation (`PeriodicLimits[0].Currency`) and dot-index notation (`PSUAuthenticationMethods.0`) both occur on this family.
- U011's Path is a URL (`/domestic-vrp-consents/45205`), not a JSON field pointer. Intercept it before any Path→field mapper.
