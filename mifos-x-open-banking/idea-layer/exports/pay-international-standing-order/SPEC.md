# Overseas Standing Order — Feature Specification

> Source: `screens/pay-international-standing-order/*.yaml` schema 4.0
> Contract version: 2.0.0 · Quality score: 89/100
> Endpoints: 4 · States: 3 · Actions: 16 · Test scenarios: 13 (P0: 6, P1: 6, P2: 1)

## Lossless Export Contract

This SPEC is consumed by `/kmp-viewmodel-gen`, `/kmp-screen-gen`, and `/verify --tests`. Sections below supply:
- State defaults — initial field values for `/kmp-viewmodel-gen`
- Error matrix — error code × user message key × recovery path
- Nav origins — which action triggers which destination

---

## 1. Overview

International standing order: a recurring overseas mandate to an IBAN creditor. Five steps — Recipient → Schedule → Amount → Charges → Review. No funding-account step (product simplification; DebtorAccount is accepted by the API but not sent by this form). No varying-amounts option — that shape belongs to the FirstPaymentAmount family, which this rail refuses with U005. Cannot be amended or cancelled through this app.

| Attribute | Value |
|---|---|
| Feature ID | `pay-international-standing-order` |
| Screen name | Overseas standing order |
| Flow ref | `pay-international-standing-order` |
| Archetype | form |
| Status | enriched |
| Cluster | payment-initiation |
| Dependency tier | feature |
| Acceptance refs | FR-012, FR-015 (open — see §5), FR-016, FR-017, FR-018, FR-019, FR-020, FR-021 |

---

## 2. Screen Inventory

| # | Screen ID | Name | ViewModel | States | Initial step |
|---|---|---|---|---|---|
| 1 | pay-international-standing-order | Overseas standing order | PayInternationalStandingOrderViewModel | Content(step), Submitting(stage), Error(type) | Recipient |

No loading state. This screen reads neither accounts nor beneficiaries; the form opens directly on the Recipient step on mount (on_mount: compute picker bounds, open on Recipient step — no network call).

---

## 3. State Model

### PayInternationalStandingOrderViewModel

#### UiState sealed interface

```kotlin
sealed interface PayInternationalStandingOrderUiState {
    data class Content(val step: Step) : PayInternationalStandingOrderUiState
    data class Submitting(val stage: SubmitStage) : PayInternationalStandingOrderUiState
    data class Error(val type: ErrorType) : PayInternationalStandingOrderUiState
}

enum class Step { Recipient, Schedule, Amount, Charges, Review }
enum class SubmitStage { StagingConsent, AwaitingAuthorisation, SubmittingPayment }
enum class FrequencyType { WEEK, FRTN, MNTH, QURT, YEAR }
enum class ChargeBearer { BorneByCreditor, Shared, BorneByDebtor }
```

#### Content state fields

| Field | Kotlin Type | Default | Nullable | Purpose |
|---|---|---|---|:---:|
| iban | String | `""` | No | CreditorAccount.Identification — UK.OBIE.IBAN scheme |
| payeeName | String | `""` | No | CreditorAccount.Name |
| bic | String | `""` | No | CreditorAgent.Identification (11-char if present; optional) |
| frequency | FrequencyType? | `null` | Yes | MandateRelatedInformation.Frequency.Type |
| firstPaymentDate | LocalDate? | `null` | Yes | MandateRelatedInformation.FirstPaymentDateTime |
| hasEndDate | Boolean | `false` | No | Drives optional FinalPaymentDateTime |
| finalPaymentDate | LocalDate? | `null` | Yes | MandateRelatedInformation.FinalPaymentDateTime (open-ended if null) |
| instructedAmountMinorUnits | String | `""` | No | InstructedAmount in minor units (pence/cents) |
| amountProblem | AmountError? | `null` | Yes | Client-side validation result |
| instructedCurrency | String | `"GBP"` | No | InstructedAmount.Currency (ISO 4217) |
| transferCurrency | String | `"USD"` | No | CurrencyOfTransfer (ISO 4217 — independent of instructedCurrency) |
| chargeBearer | ChargeBearer? | `null` | Yes | ChargeBearer on the wire |
| step | Step | `Step.Recipient` | No | Active wizard step |

#### Initial values (for /kmp-viewmodel-gen)

```kotlin
val initial = Content(
    iban = "",
    payeeName = "",
    bic = "",
    frequency = null,
    firstPaymentDate = null,
    hasEndDate = false,
    finalPaymentDate = null,
    instructedAmountMinorUnits = "",
    amountProblem = null,
    instructedCurrency = "GBP",
    transferCurrency = "USD",
    chargeBearer = null,
    step = Step.Recipient,
)
```

#### Error types

| Type | Trigger | User message key | Recovery | Retry |
|---|---|---|---|:---:|
| FieldNotExpected | 400 U005 — FirstPaymentAmount or RemittanceInformation sent | `error.payment.field_not_expected` | Implementation fault — wrong amount field | No |
| MissingRequiredField | 400 U004 — Permission, CurrencyOfTransfer, or ChargeBearer omitted | `error.payment.missing_field` | Implementation fault | No |
| InvalidMandateDates | 400 U003 — final before first, beyond 12 months, or today/tomorrow | `error.payment.invalid_mandate_dates` | Return to Schedule step | No |
| InvalidFieldValue | 400 U002 — frequency outside 5 values, or BIC not 11 characters | `error.payment.invalid_bank_code` | Return to relevant step | No |
| UnsupportedScheme | 400 U027 — sort-code creditor (unreachable — form takes IBAN) | `error.payment.unsupported_scheme` | Unreachable by design | No |
| SignatureMissing | 400 U019 — x-jws-signature missing | `error.payment.signature_missing` | Not user-recoverable | No |
| ConsentNotAuthorised | 400 U009 — consent not yet authorised | `error.payment.consent_not_authorised` | Re-authorise at bank | No |
| NetworkError | IOException / timeout | `error.payment.network_error` | Retry (idempotency key reused) | Yes |

#### Actions

| Action | Signature | User trigger |
|---|---|---|
| EnterIban | `fun enterIban(iban: String)` | Text input — Recipient step |
| EnterPayeeName | `fun enterPayeeName(name: String)` | Text input — Recipient step |
| EnterBic | `fun enterBic(bic: String)` | Text input — Recipient step (optional) |
| SelectFrequency | `fun selectFrequency(type: FrequencyType)` | Frequency picker — Schedule step |
| SelectFirstPaymentDate | `fun selectFirstPaymentDate(date: LocalDate)` | Date picker — Schedule step |
| ToggleEndDate | `fun toggleEndDate(hasEnd: Boolean)` | Switch — Schedule step |
| SelectFinalPaymentDate | `fun selectFinalPaymentDate(date: LocalDate)` | Date picker — Schedule step (when hasEndDate) |
| EnterInstructedAmount | `fun enterInstructedAmount(minorUnits: String)` | Amount field — Amount step |
| SelectInstructedCurrency | `fun selectInstructedCurrency(iso4217: String)` | Currency picker — Amount step |
| SelectTransferCurrency | `fun selectTransferCurrency(iso4217: String)` | Currency picker — Amount step |
| SelectChargeBearer | `fun selectChargeBearer(bearer: ChargeBearer)` | Radio group — Charges step |
| ReviewMandate | `fun reviewMandate()` | Next from Charges step |
| ConfirmAndStageConsent | `suspend fun confirmAndStageConsent()` | "Set up standing order" button — Review step |
| SubmitStandingOrder | `suspend fun submitStandingOrder(consentId: String)` | Internal — called after consent reaches AUTH |
| RetrySubmit | `fun retrySubmit()` | Retry button — Error state |
| BackStep | `fun backStep()` | Back navigation — any step |
| CancelMandate | `fun cancelMandate()` | Cancel / Back from Recipient step |

#### Events

| Event | Params | Trigger |
|---|---|---|
| NavigateToPaymentConsent | consentId: String, paymentFamily: "international-standing-order" | ConfirmAndStageConsent returns 201 |
| NavigateToPaymentStatus | paymentId: String, paymentFamily: "international-standing-order" | SubmitStandingOrder returns 201 |

#### DI

- `PaymentInitiationRepository` — sole dependency.

No `AccountsOverviewRepository` — the form does not offer a funding-account step. Note: DebtorAccount IS accepted by the API (corrected 2026-08-07); the absence here is a product choice, not a schema constraint.

No `BeneficiariesRepository` — sort-code payees are refused on international rails (U027 is resolved-account dependent; only Global Money GMA is addressable by sort code). The IBAN form makes all saved-payee lookup unreachable anyway.

---

## 4. Navigation

### Entry point

| Source | Trigger | Params |
|---|---|---|
| payments | Tap International standing order tile | none |

### Outgoing navigation

| Target | Trigger | Origin component | Params |
|---|---|---|---|
| payment-consent | ConfirmAndStageConsent succeeds (201) | confirm_button | consentId, paymentFamily="international-standing-order" |
| payment-status | SubmitStandingOrder succeeds (201) | (internal, post-auth resume) | paymentId, paymentFamily="international-standing-order" |
| payments | CancelMandate or Back from Recipient | (back / cancel gesture) | none |

### Post-creation constraints

The success state offers no edit CTA and no cancel CTA. OBL Customer Experience Guidelines mandate directing the PSU to their bank's own channel for any amendment or cancellation. This is stated by `amend_notice` (warning severity) on both the Review step and the success state.

Do not attempt to surface the new mandate in any AIS standing-orders list — AIS carries no identifier that maps to a PIS mandate ID, and the AIS standing-orders read is refused outright (400) on savings accounts and Global Money.

---

## 5. API Dependencies

### Host and auth

- Host: `https://secure.sandbox.ob.hsbc.co.uk`
- Base path: `/obie/open-banking/v4.0/pisp`
- Auth server: `https://sandbox.ob.hsbc.co.uk/obie/open-banking/v1.1/oauth2/authorize`
- Auth scheme: mTLS + `private_key_jwt` (PS256) + authorization-code — FAPI 1.0 Advanced

### CRITICAL — amount field inversion

```
domestic standing order      → sends FirstPaymentAmount   refuses InstructedAmount  (U005)
international standing order → sends InstructedAmount     refuses FirstPaymentAmount (U005)
```

These are proven mutually exclusive (Round 15, both directions). Copying the domestic mandate and changing the endpoint yields U005 on every request. There is no `FirstPaymentAmount` on this rail and no Recurring or Final sibling — they belong to the domestic shape.

### Frequency enum — exactly five values

`MandateRelatedInformation.Frequency.Type` accepts: `WEEK`, `FRTN`, `MNTH`, `QURT`, `YEAR`.

Rejected (all return U002): `DAIL`, `ADHO`, `INDA`, `MIAN`. The frequency picker must offer exactly these five values.

### Endpoint summary

| # | Method | Endpoint | Auth | Success status |
|---|---|---|---|---|
| 1 | POST | /international-standing-order-consents | client_credentials_payments_scope | 201, Status=AWAU |
| 2 | GET | /international-standing-order-consents/{ConsentId} | client_credentials_payments_scope | 200, Status=AUTH |
| 3 | POST | /international-standing-orders | psu_authorization_code | 201, Status=INCO |
| 4 | GET | /international-standing-orders/{InternationalStandingOrderId} | client_credentials_payments_scope | 200, Status=INCO |

Consent status ladder: `AWAU → AUTH → COND`
Resource status ladder: `INCO → INCO` — never emits PDNG.

### Error matrix

| Endpoint | Code | Trigger | Recovery |
|---|---|---|---|
| POST /consents | U004 | Permission, CurrencyOfTransfer, or ChargeBearer omitted | Implementation fault |
| POST /consents | U005 | FirstPaymentAmount or RemittanceInformation sent | Implementation fault — wrong amount field |
| POST /consents | U002 | Frequency outside 5 values, or BIC not 11 characters | Return to relevant step |
| POST /consents | U003 | Final date before first, beyond 12 months, today/tomorrow | Return to Schedule step |
| POST /consents | U027 | Creditor unresolvable (sort-code) — unreachable | Unreachable |
| POST /consents | U019 | Missing x-jws-signature | Not user-recoverable |
| POST /orders | U009 | Consent not authorised | Re-authorise |
| Any | NetworkError | IOException / timeout | Retry (same idempotency key) |

Errors is an **array** — can carry two entries (SO-I04 returns two U002 rules together). Render every entry in wire order, keyed by ErrorCode + Path, not by Message.

### Charge visibility

| Stage | Charges field | Fee shown |
|---|---|---|
| Consent staged (AWAU) | KEY ABSENT — not an empty array | Unknown (fee row reads unknown) |
| Consent authorised (AUTH) | KEY ABSENT | Unknown |
| Resource created (INCO) | 0.50 in InstructedAmount.Currency | Shown |

Parse `Charges` as nullable. Defaulting to `[]` renders a 0.50 mandate as free at consent.

Charge currency: follows InstructedAmount.Currency, not CurrencyOfTransfer. Evidence: resource 19918 — 5.00 GBP instructed, USD transfer, charge 0.50 GBP.

Whether the 0.50 recurs per execution or applies once at setup is not stated by the API. The screen must not answer either way.

### FR-015 open question

FR-015 requires a consumer PaymentContextCode on every payment. Zero observed international standing orders sent PaymentContextCode, and all staged 201 with an empty `Risk {}`. This rail carries neither `CategoryPurposeCode` nor `PaymentContextCode` on any observed scenario. If the field is refused, FR-015 is unsatisfiable here and the requirement needs amending. Do not add PaymentContextCode on the strength of FR-015 alone.

### FX contract

`ExchangeRateInformation` is refused for all three `RateType` values (Actual, Indicative, Agreed — R16-O1/O2/O3). Controls without the block staged 201. OBIE has no per-execution FX model. No rate is shown, no projected total, no estimated per-instalment received amount.

---

## 6. Design Tokens Used

| Token | Value (light) | Used by |
|---|---|---|
| `colors.primary` | `#266489` | confirm_button fill, stepper active step, amount field focus outline |
| `colors.error` | `#BA1A1A` | error_panel text, validation error text, field outline on error |
| `colors.secondary` | `#50606E` | submitting_indicator secondary label |
| `colors.surface` | `#F7F9FF` | screen background |
| `colors.on_surface` | `#181C20` | primary text — review_card row values |
| `colors.on_surface_variant` | `#41474D` | helper text, field labels, no_varying_amounts_note |
| `colors.surface_container` | `#EBEEF3` | review_card container |
| `colors.tertiary_container` | `#EADDFF` | fx_not_fixed_notice warning banner container |
| `colors.on_tertiary_container` | `#4C4162` | fx_not_fixed_notice warning banner text |
| `colors.secondary_container` | `#D3E5F5` | deferred_charge_note info banner container |
| `colors.on_secondary_container` | `#384956` | deferred_charge_note info banner text |
| `semantic.payment_disposition.instruction_established` | surfaceVariant neutral | payment-status chip for INCO on payment-status screen |
| `semantic.payment_disposition.instruction_established.icon` | `event_repeat` | instruction_established chip icon |
| `typography.mono` / Roboto Mono | — | amount_field digit display (form.amount_field.font) |
| `radius.sm` | 8dp | text_field inputs (form.field.radius) |
| `radius.md` | 12dp | review_card, summary_card corner |
| `radius.full` | 9999dp | confirm_button (filled_pill variant) |
| `spacing.md` | 16dp | screen_padding, default component inset |
| `spacing.sm` | 8dp | intra-step field gap |
| `spacing.lg` | 24dp | section-to-section gap |
| `touch_targets.comfortable` | 48dp | all interactive elements — minimum touch target |

---

## 7. Referenced Journeys

**None. No journey in `idea-layer/journeys/` walks this screen.**

All five journeys were checked against their `screen_sequence`: `consumer-authentication`,
`consumer-accounts-payments`, `consumer-cards-financing`, `consumer-insights-utilities`,
`consumer-profile-settings`. This feature appears in none of them.

`consumer-insights-utilities` is the only journey that reaches an international rail, and it walks
`pay-international-single` — the immediate shape, not the mandate. `consumer-cards-financing` ends on
the `payments` hub tapping a *domestic* standing-order tile. So no journey exercises the recurring
overseas shape at all.

That leaves the rail's two most distinctive behaviours unexercised end-to-end:

- The **amount-field inversion** (§5) — this rail sends `InstructedAmount` and refuses
  `FirstPaymentAmount` with U005, exactly inverting the domestic mandate. Only TC scenarios cover it.
- The **charge-visibility gap** (§5) — `Charges` is key-absent at consent and appears only at resource
  creation, so the fee row genuinely reads unknown through the whole authorisation leg.

Recorded as a gap in `journeys/INDEX.md` § "Coverage gaps owed". To close it:
`/idea journey new --cover pay-international-standing-order`.
