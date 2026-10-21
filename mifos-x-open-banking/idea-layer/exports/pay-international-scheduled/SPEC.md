# Pay Abroad on a Date — Feature Specification

> Generated from `screens/pay-international-scheduled/{docs,ui,api,flow}.yaml`
> Schema version: 4.0  contract_version: 2.0.0
> Endpoints: 4 · Components: 10 own + 13 inherited · Test scenarios: 12
> Quality score: 91/100

## Lossless Export Contract

This SPEC enables `/kmp-viewmodel-gen`, `/kmp-screen-gen`, and `/verify --tests` to consume it alone:
- State Defaults — initial values per field
- Error Matrix — endpoint × code × (retry, message key, recovery)
- Nav Origins — which component triggers which route
- Test Mapping — TC-PISCH-NNN → expected file path

---

## 1. Overview

International scheduled payment: one overseas transfer to an IBAN creditor on a single future date (T+1..T+365). Six-step form combining the international field contract (IBAN creditor, currency pair, charge bearer) with the scheduled date contract (RequestedExecutionDateTime). No funds confirmation; PSU cannot amend or cancel via PISP.

| Attribute | Value |
|-----------|-------|
| Feature ID | `pay-international-scheduled` |
| Flow | pay-international-scheduled |
| Cluster | payment-initiation |
| Quality Score | 91/100 |
| Dependency Tier | feature |
| Archetype | form |
| Acceptance Refs | FR-012, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021 |

### User Stories

- As a retail banking customer, I want to schedule a future-dated international payment to an IBAN so that I can transfer money abroad on a specific date without initiating it manually.
- As a customer, I want to choose who bears the transfer charge before I authorise so that I understand my cost obligations.
- As a customer, I want to be told honestly that the exact fee and FX rate cannot be shown before authorisation so that I am not misled into thinking the payment is free or at a disclosed rate.

### Success Metrics

| Metric | Target |
|--------|--------|
| Consent staged successfully on first attempt | ≥ 95% |
| Date validation error rate | < 2% |
| Form completion (Step 1 → Review → Submit) | ≥ 80% |
| P0 scenario pass rate | 100% |

---

## 2. Screens

| # | Screen | ViewModel | States | Description |
|---|--------|-----------|--------|-------------|
| 1 | pay-international-scheduled | PayInternationalScheduledViewModel | loading, content, content_no_eligible_accounts, submitting, error | Six-step wizard: Account → Recipient → Amount → Date → Charges → Review. Steps are internal state transitions; no new screen is mounted per step. |

### Screen Relationships

Single screen. Steps driven by `Content(step: PaymentStep)`. Back navigation returns to prior step; Cancel exits to payments hub.

---

## 3. State Model

### PayInternationalScheduledViewModel

**ViewModel**: `PayInternationalScheduledViewModel`  
**UiState type**: `PayInternationalScheduledUiState`  
**DI**: `AccountsOverviewRepository`, `PaymentInitiationRepository`

#### State: `Loading`

| Field | Type | Default | Nullable | Purpose |
|-------|------|---------|:--------:|---------|
| — | — | — | — | Initial mount state; step_indicator only visible |

#### State: `Content(step: PaymentStep)`

| Field | Type | Default | Nullable | Purpose |
|-------|------|---------|:--------:|---------|
| step | PaymentStep | Account | No | Current wizard step |
| eligibleDebtorAccounts | List\<DebtorAccountUiModel\> | emptyList() | No | SortCodeAccountNumber accounts, Global Money excluded |
| hiddenAccountCount | Int | 0 | No | Filtered account count; drives ineligible_accounts_note |
| selectedDebtorAccount | DebtorAccountUiModel? | null | Yes | Chosen funding account |
| ibanValue | String | "" | No | Raw IBAN input |
| payeeName | String | "" | No | Creditor display name |
| bicValue | String | "" | No | BIC; optional but must be 11 chars if supplied |
| amountMinorUnits | Long | 0L | No | Instructed amount in minor units |
| instructedCurrency | String | "GBP" | No | ISO 4217 — independent of transferCurrency |
| transferCurrency | String | "" | No | ISO 4217 — independent of instructedCurrency |
| requestedExecutionDate | LocalDate? | null | Yes | T+1..T+365; null until selected |
| chargeBearerOption | ChargeBearer? | null | Yes | BorneByCreditor / Shared / BorneByDebtor |
| ibanError | String? | null | Yes | Inline IBAN validation |
| bicError | String? | null | Yes | BIC length error |
| amountError | String? | null | Yes | Amount validation |
| dateError | String? | null | Yes | Past-date or out-of-range error |
| feeLabel | String? | null | Yes | Null until resource created; 0.50 in instructed currency post-submit |

#### State Defaults

```kotlin
val initial = Content(
  step = PaymentStep.Account,
  eligibleDebtorAccounts = emptyList(),
  hiddenAccountCount = 0,
  selectedDebtorAccount = null,
  ibanValue = "",
  payeeName = "",
  bicValue = "",
  amountMinorUnits = 0L,
  instructedCurrency = "GBP",
  transferCurrency = "",
  requestedExecutionDate = null,
  chargeBearerOption = null,
  ibanError = null,
  bicError = null,
  amountError = null,
  dateError = null,
  feeLabel = null,
)
```

#### State: `Submitting(stage: SubmissionStage)`

| Field | Type | Default | Nullable | Purpose |
|-------|------|---------|:--------:|---------|
| stage | SubmissionStage | StagingConsent | No | Current async stage |
| consentId | String? | null | Yes | Set when AwaitingAuthorisation |

```kotlin
sealed interface SubmissionStage {
    data object StagingConsent : SubmissionStage
    data class AwaitingAuthorisation(val consentId: String) : SubmissionStage
    data object SubmittingPayment : SubmissionStage
}
```

#### State: `Error(type: PaymentError)`

| Field | Type | Default | Nullable | Purpose |
|-------|------|---------|:--------:|---------|
| type | PaymentError | NetworkError | No | Error class |
| apiErrors | List\<ObPaymentErrorEntry\> | emptyList() | No | All entries from 400 Errors array, wire order |

#### Errors

| Type | Retry | i18n Key | Recovery |
|------|:-----:|----------|----------|
| MissingRequiredField | No | strings.error.payment.missing_field | Implementation fault |
| FieldNotExpected | No | strings.error.payment.field_not_expected | Implementation fault |
| DateInPast | Yes | strings.error.payment.date_in_past | BackStep to Date |
| DateOutOfRange | Yes | strings.error.payment.date_out_of_range | BackStep to Date |
| UnsupportedScheme | No | strings.error.payment.unsupported_scheme | Unreachable — IBAN-only form |
| SignatureMissing | No | strings.error.payment.signature_missing | Not user-recoverable |
| ConsentNotAuthorised | Yes | strings.error.payment.consent_not_authorised | Re-authorise |
| NetworkError | Yes | strings.error.payment.network_error | Retry (same idempotency key) |

#### Events

| Event | Params | Trigger |
|-------|--------|---------|
| NavigateToPaymentConsent | consentId: String, paymentFamily: String | Consent staged 201 |
| NavigateToPaymentStatus | paymentId: String, paymentFamily: String | Payment submitted 201 |

#### Actions

| Action | Params | User Trigger |
|--------|--------|-------------|
| LoadPaymentSources | — | Screen mount |
| SelectDebtorAccount | account: DebtorAccountUiModel | Tap account list item |
| EnterIban | iban: String | IBAN field change |
| EnterPayeeName | name: String | Payee name field change |
| EnterBic | bic: String | BIC field change |
| EnterAmount | amount: String | Amount field change |
| SelectInstructedCurrency | currency: String | Instructed currency picker |
| SelectTransferCurrency | currency: String | Transfer currency picker |
| SelectExecutionDate | date: LocalDate | Date picker selection |
| SelectChargeBearer | bearer: ChargeBearer | Charge bearer picker |
| ReviewPayment | — | Advance to Review |
| ConfirmAndStageConsent | — | Tap confirm_button |
| SubmitPayment | consentId: String | Post-AUTH, internal |
| RetrySubmit | — | Tap retry in error state |
| BackStep | — | Back icon |
| CancelPayment | — | Cancel / back from Account step |

---

## 4. Navigation

### Entry Points

| Source | Trigger | Params |
|--------|---------|--------|
| payments hub | Tap "International scheduled" tile | none |

### Outgoing Navigation

| Target | Event | Origin Component | Param Map | Condition |
|--------|-------|------------------|-----------|-----------|
| payment-consent | NavigateToPaymentConsent | confirm_button | consentId, paymentFamily="international-scheduled-payment" | 201 on consent stage |
| payment-status | NavigateToPaymentStatus | (internal post-AUTH) | paymentId, paymentFamily="international-scheduled-payment" | 201 on submit |
| payments | CancelPayment | back icon / cancel | none | Back from Account or cancel |

### Nav Origins

| Component | on_click.action | Target | Params Resolved From |
|-----------|-----------------|--------|----------------------|
| confirm_button | ConfirmAndStageConsent | payment-consent | uiState.consentId after 201 |
| back icon | BackStep / CancelPayment | payments (from step Account) | none |

---

## 5. API Dependencies

| # | Endpoint | Method | Auth | Cache | Offline |
|---|----------|--------|:----:|-------|---------|
| 1 | /international-scheduled-payment-consents | POST | client_credentials + mTLS | none | No |
| 2 | /international-scheduled-payment-consents/{id} | GET | client_credentials + mTLS | none | No |
| 3 | /international-scheduled-payments | POST | psu_authorization_code + mTLS | none | No |
| 4 | /international-scheduled-payments/{id} | GET | client_credentials + mTLS | none | No |

### Error Matrix

| Endpoint | Code | When | Retry | i18n Key | Recovery UI |
|----------|------|------|:-----:|----------|-------------|
| POST /…consents | U004 | Permission/date/CurrencyOfTransfer/ChargeBearer omitted | No | missing_field | error_panel |
| POST /…consents | U005 | RemittanceInformation or ExchangeRateInformation sent | No | field_not_expected | error_panel |
| POST /…consents | U003 | Date is today or past | Yes | date_in_past | error_panel + BackStep to Date |
| POST /…consents | U002 | Date > T+365 or BIC not 11 chars | Yes | date_out_of_range | error_panel + BackStep |
| POST /…consents | U019 | Missing x-jws-signature | No | signature_missing | error_panel |
| POST /…payments | U009 | Consent not in AUTH | Yes | consent_not_authorised | error_panel |
| Any | IOException | Network failure | Yes | network_error | error_panel + retry |

---

## 6. Design Tokens Used

| Token | Value (light) | Used By |
|-------|--------------|---------|
| colors.primary | #266489 | confirm_button fill, step_indicator active, selected account |
| colors.onPrimary | #FFFFFF | confirm_button label |
| colors.surface | #F7F9FF | screen background |
| colors.onSurface | #181C20 | primary labels, amount input text |
| colors.onSurfaceVariant | #41474D | helper text, field labels, date_normalisation_note |
| colors.surfaceContainer | #EBEEF3 | review_card, summary rows |
| colors.outline | #72787E | text_field default border |
| colors.error | #BA1A1A | field error text, error_panel icon |
| colors.errorContainer | #FFDAD6 | error_panel background |
| semantic.payment_disposition.instruction_established | surfaceVariant/onSurfaceVariant | payment-status INCO chip |
| radius.sm | 8dp | text_field, amount_field, date_picker corners |
| radius.md | 12dp | review_card, summary_card |
| radius.full | 9999dp | confirm_button (filled_pill) |
| typography.bodySmall | Roboto 12/16 400 | date_normalisation_note, field helper_text |
| typography.bodyLarge | Roboto 16/24 400 | account list item primary label |
| typography.headlineSmall | Roboto Mono 24/32 400 | amount_field input |
| typography.labelLarge | Roboto 14/20 500 | confirm_button label, step labels |
| spacing.md | 16dp | screen_padding, major gaps |
| spacing.sm | 8dp | intra-card row gaps |

---

## 7. Testing

| ID | Scenario | Priority | Expected Test File |
|----|----------|:--------:|--------------------|
| TC-PISCH-001 | End-to-end: stage consent → AUTH → submit → INCO | P0 | PayInternationalScheduledViewModelTest |
| TC-PISCH-002 | Date T-1 rejected U003 | P0 | PayInternationalScheduledViewModelTest |
| TC-PISCH-003 | Date T+366 rejected U002 | P0 | PayInternationalScheduledViewModelTest |
| TC-PISCH-004 | Fee row reads UNKNOWN at review (Charges absent on consent) | P0 | PayInternationalScheduledViewModelTest |
| TC-PISCH-005 | Resource status INCO accepted at creation — never PDNG | P0 | PayInternationalScheduledViewModelTest |
| TC-PISCH-006 | RemittanceInformation absent from consent body | P0 | PayInternationalScheduledViewModelTest |
| TC-PISCH-007 | ChargeBearer required — U004 when omitted | P0 | PayInternationalScheduledViewModelTest |
| TC-PISCH-008 | BIC rejected if not 11 chars (8-char BIC → U002) | P1 | PayInternationalScheduledViewModelTest |
| TC-PISCH-009 | deferred_charge_note shown at review; fee populated from resource Charges | P0 | PayInternationalScheduledViewModelTest |
| TC-PISCH-010 | InstructedCurrency and TransferCurrency are independent | P1 | PayInternationalScheduledViewModelTest |
| TC-PISCH-011 | SP-I04: both Errors entries rendered in wire order | P1 | PayInternationalScheduledViewModelTest |
| TC-PISCH-012 | amend_notice shown on Review step and Success state | P2 | PayInternationalScheduledViewModelTest |

**Coverage Target**: 100% P0 · 80% P1 · 50% P2

---

## 8. Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Charges key absent on consent (not empty array) | fee_label = null; review fee row → strings.payment.fee_unknown; never "0.00" or blank |
| Charges defaulted to [] by parser | FORBIDDEN — renders 0.50 payment as free at consent step |
| BIC supplied but not 11 characters | bic_length_error shown inline; step advance blocked |
| Date T+0 (today) | DateInPast error; BackStep to Date |
| Date T+366 | DateOutOfRange error; BackStep to Date |
| RequestedExecutionDateTime normalised to midnight | date_normalisation_note informs user; no UI action needed |
| Server reorders Initiation keys on echo | Submit body from parsed read-back, never re-serialised local model |
| SP-I04 two-entry Errors array | error_panel renders BOTH entries in wire order; first is creditor, second is currency |
| ExchangeRateInformation sent | Must NOT send — refused U005 for all RateType values |
| No eligible debtor accounts | content_no_eligible_accounts state; no_eligible_accounts component only |
| Fee visibility before authorisation | IMPOSSIBLE — charge appears only at resource creation; form states this with deferred_charge_note |

---

## 9. Feature Flags

| Flag | Type | Default | Rollout |
|------|------|---------|---------|
| (none) | — | — | — |

---

## 10. Data Flow

| Screen | Trigger | Endpoints | DTOs | Produces State | Cache | Error Paths |
|--------|---------|-----------|------|----------------|-------|-------------|
| pay-international-scheduled | mount | accounts-list (AISP) | DebtorAccountDto | content / content_no_eligible_accounts / error | memory (AccountsOverviewStore) | error |
| pay-international-scheduled | stage_consent | POST /international-scheduled-payment-consents | ConsentRequest, ConsentResponse | submitting(StagingConsent → AwaitingAuthorisation) | none | error(U003/U004/U005/U002) |
| pay-international-scheduled | resume_after_authorisation | GET /consents/{id}, POST /international-scheduled-payments | ConsentResponse, PaymentResponse | submitting(SubmittingPayment) → navigate payment-status | none | error(U009/network) |
| pay-international-scheduled | retry | POST /international-scheduled-payments (same idempotency key) | PaymentResponse | submitting → navigate payment-status | none | error |

### Side Effects

| Screen | Trigger | Kind | Target |
|--------|---------|------|--------|
| pay-international-scheduled | stage_consent | navigate | payment-consent(consentId, paymentFamily="international-scheduled-payment") |
| pay-international-scheduled | submit | navigate | payment-status(paymentId, paymentFamily="international-scheduled-payment") |

---

## 11. Referenced Journeys

**None. No journey in `idea-layer/journeys/` walks this screen.**

All five journeys were checked against their `screen_sequence`: `consumer-authentication`,
`consumer-accounts-payments`, `consumer-cards-financing`, `consumer-insights-utilities`,
`consumer-profile-settings`. This feature appears in none of them.

`consumer-insights-utilities` is the only journey that reaches an international rail, and it walks
`pay-international-single` — the immediate shape. Nothing covers the international *deferred* shape,
which is where this rail's two hardest behaviours live: the resource status arriving as **INCO at
creation and never PDNG** (TC-PISCH-005), and the fee being genuinely unknowable before authorisation
because `Charges` is key-absent rather than empty (TC-PISCH-004, TC-PISCH-009). Both are currently
covered by unit scenarios only.

Recorded as a gap in `journeys/INDEX.md` § "Coverage gaps owed". To close it:
`/idea journey new --cover pay-international-scheduled`.

---

## 12. DTOs Consumed

| DTO | Source | Kind |
|-----|--------|------|
| InternationalScheduledPaymentConsentRequest | POST /international-scheduled-payment-consents body | Request |
| InternationalScheduledPaymentConsentResponse | POST/GET /international-scheduled-payment-consents | Response |
| InternationalScheduledPaymentRequest | POST /international-scheduled-payments body | Request |
| InternationalScheduledPaymentResponse | POST/GET /international-scheduled-payments | Response |
| ObPaymentError (dtos/ObPaymentError.yaml) | Any 400 body | Error envelope |

---

## 13. Dependencies

**Tier**: feature

| Dependency | Type | Required | Check |
|------------|------|:--------:|-------|
| accounts | data_source | Yes | Eligible debtors before step 1 |
| payment-consent | child | Yes | App-to-app authorise leg |
| payment-status | child | Yes | Receives INCO payment ID after submit |
| payments | parent | Yes | Entry point (hub tile) |
