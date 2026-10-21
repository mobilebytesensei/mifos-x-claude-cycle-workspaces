# Standing Order (Domestic) — Feature Specification

> Generated from `screens/pay-domestic-standing-order/*.yaml` by `/idea-feature-export`
> Schema version: 4.0  Contract version: 2.1.0
> Cluster: payment-initiation  Quality score: 88/100
> Endpoints: 4  Components: 15  Actions: 17  Test scenarios: 15  Error types: 6

## Lossless Export Contract

This SPEC is lossless per RULE-EXPORT-ROUNDTRIP-001. The sections below enable `/kmp-viewmodel-gen`, `/kmp-screen-gen`, and `/verify --tests` to consume SPEC.md alone:
- State Defaults — initial values for every Content field
- Error Matrix — endpoint × error-code × (retry?, user message key, recovery)
- Test Mapping — TC-PSO-NNN → expected test file
- Nav Origins — which component triggers which route

## 1. Overview

A domestic standing order is a **recurring sterling mandate** to a UK sort code and account number — not a payment. The user selects a payee, configures a schedule (frequency, first date, optional end date), enters a first payment amount and an optional reference, reviews, then authorises at their bank. There is **no funding-account step** because `DebtorAccount` is absent from this schema; the source account is chosen by the PSU at the bank during authorisation. A standing order created by a PISP cannot be amended or cancelled through the PISP.

| Attribute | Value |
|-----------|-------|
| Feature ID | `pay-domestic-standing-order` |
| Cluster | `payment-initiation` |
| Archetype | form |
| Flow | pay-domestic-standing-order |
| Quality Score | 88/100 |
| Dependency Tier | feature |
| Status | enriched |
| Inherits from | pay-domestic-single (payee components only) |
| Acceptance refs | FR-012, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021 |

### Rail Characteristics

| Attribute | Value |
|-----------|-------|
| Amount field | `FirstPaymentAmount` — never `InstructedAmount` (U005 if sent) |
| Frequency | Exactly 5 values: WEEK, FRTN, MNTH, QURT, YEAR |
| Funds confirmation | None (no per-mandate balance check) |
| Reference channel | `Data.Initiation.RemittanceInformation.Unstructured[0]` |
| Risk block | `{}` (empty — no single e-commerce context for a mandate) |
| Charge at staging | 0.05 GBP; render amount + currency only, never `Charges[].Type` |
| Consent status ladder | AWAU → AUTH → COND |
| Resource status ladder | PDNG → INCO |
| Per-instalment status | None — OBIE has no per-execution status on this rail |
| Amendment/cancellation | Forbidden via PISP; redirect PSU to bank channel |

---

## 2. Screens

| # | Screen ID | ViewModel | UI States | Description |
|---|-----------|-----------|-----------|-------------|
| 1 | pay-domestic-standing-order | PayDomesticStandingOrderViewModel | Loading · Content(step) · Submitting(stage) · Error(type) | Four-step form: Payee → Schedule → Amount → Review. |

### Screen Relationships

Single screen with internal step navigation (Payee → Schedule → Amount → Review). After staging the consent the screen navigates to `payment-consent`; on return it resumes at submit. After a successful submit it navigates to `payment-status`. Back from Payee step returns to `payments` hub.

---

## 3. State Model

### PayDomesticStandingOrderViewModel

#### State: `Content`

| Field | Type | Default | Nullable | Purpose |
|-------|------|---------|:--------:|---------|
| step | Step | Payee | No | Current wizard step enum: Payee, Schedule, Amount, Review |
| beneficiaries | List\<Beneficiary\> | emptyList() | No | Saved payees loaded on mount |
| selectedCreditor | Creditor? | null | Yes | Chosen payee: SchemeName, Identification, Name |
| frequency | FrequencyType? | null | Yes | One of: WEEK, FRTN, MNTH, QURT, YEAR |
| firstPaymentDate | LocalDate? | null | Yes | Always sent to API; leaving it null produces an unusable review screen |
| hasEndDate | Boolean | false | No | When false, FinalPaymentDateTime is omitted (open-ended mandate) |
| finalPaymentDate | LocalDate? | null | Yes | Required when hasEndDate = true; must be within 12 months of today |
| firstPaymentAmountMinor | Long? | null | Yes | Pence; rendered as major-unit string on wire |
| varyingAmounts | Boolean | false | No | Advanced: exposes RecurringPaymentAmount and FinalPaymentAmount |
| recurringAmountMinor | Long? | null | Yes | Optional; only when varyingAmounts = true |
| finalAmountMinor | Long? | null | Yes | Optional; only when varyingAmounts AND hasEndDate |
| reference | String | "" | No | max 35 chars; maps to RemittanceInformation.Unstructured[0]; omitted when blank |
| scheduleProblem | ValidationError? | null | Yes | Client-side final-date validation: after first, within 12 months, not today/tomorrow |

#### State Defaults (for `/kmp-viewmodel-gen` initial-value emission)

```kotlin
val initial = ContentData(
    step = Step.Payee,
    beneficiaries = emptyList(),
    selectedCreditor = null,
    frequency = null,
    firstPaymentDate = null,
    hasEndDate = false,
    finalPaymentDate = null,
    firstPaymentAmountMinor = null,
    varyingAmounts = false,
    recurringAmountMinor = null,
    finalAmountMinor = null,
    reference = "",
    scheduleProblem = null,
)
```

#### Screen State: `PayDomesticStandingOrderUiState`

```kotlin
sealed interface PayDomesticStandingOrderUiState {
    data object Loading : PayDomesticStandingOrderUiState
    data class Content(val data: ContentData, val step: Step) : PayDomesticStandingOrderUiState
    data class Submitting(val stage: SubmitStage) : PayDomesticStandingOrderUiState
    data class Error(val type: ErrorType) : PayDomesticStandingOrderUiState
}

enum class Step { Payee, Schedule, Amount, Review }

enum class SubmitStage { StagingConsent, AwaitingAuthorisation, SubmittingPayment }

enum class FrequencyType { WEEK, FRTN, MNTH, QURT, YEAR }
```

#### Errors: `ErrorType`

| Type | Code | HTTP | Retry | User Message Key | Recovery |
|------|------|:----:|:-----:|------------------|----------|
| FieldNotExpected | U005 | 400 | No | strings.error.payment.field_not_expected | Error panel — implementation fault |
| InvalidMandateDates | U003 | 400 | No | strings.error.payment.invalid_mandate_dates | Return to Schedule step |
| InvalidFrequency | U002 | 400 | No | strings.error.payment.invalid_frequency | Error panel — unreachable if picker correct |
| SignatureMissing | U019 | 400 | No | strings.error.payment.signature_missing | Error panel — not user-recoverable |
| ConsentNotAuthorised | U009 | 400 | Yes | strings.error.payment.consent_not_authorised | Error panel with re-authorise CTA |
| NetworkError | IOException | — | Yes | strings.error.payment.network_error | Error panel with retry; idempotency key reused |

#### Events

| Event | Params | Trigger |
|-------|--------|---------|
| NavigateToPaymentConsent | consentId: String, paymentFamily: String | 201 from POST /domestic-standing-order-consents |
| NavigateToPaymentStatus | paymentId: String, paymentFamily: String | 201 from POST /domestic-standing-orders |

#### Actions

| Action | Signature | User Trigger |
|--------|-----------|-------------|
| LoadBeneficiaries | `fun loadBeneficiaries()` | Screen mount |
| SelectCreditor | `fun selectCreditor(creditor: Creditor)` | Tap payee row |
| SelectFrequency | `fun selectFrequency(type: FrequencyType)` | Dropdown selection |
| SelectFirstPaymentDate | `fun selectFirstPaymentDate(date: LocalDate)` | Date picker confirm |
| ToggleEndDate | `fun toggleEndDate(enabled: Boolean)` | Switch toggle |
| SelectFinalPaymentDate | `fun selectFinalPaymentDate(date: LocalDate)` | Date picker confirm |
| EnterFirstPaymentAmount | `fun enterFirstPaymentAmount(text: String)` | Keyboard in amount_field |
| ToggleVaryingAmounts | `fun toggleVaryingAmounts(enabled: Boolean)` | Switch toggle |
| EnterRecurringAmount | `fun enterRecurringAmount(text: String)` | Keyboard in recurring_amount_field |
| EnterFinalAmount | `fun enterFinalAmount(text: String)` | Keyboard in final_amount_field |
| EnterReference | `fun enterReference(text: String)` | Keyboard in reference_field; max 35 chars enforced |
| ReviewMandate | `fun reviewMandate()` | Tap "Next" on Amount step |
| ConfirmAndStageConsent | `suspend fun confirmAndStageConsent()` | Tap confirm_button on Review step |
| SubmitStandingOrder | `suspend fun submitStandingOrder(consentId: String)` | Return from payment-consent with AUTH |
| RetrySubmit | `fun retrySubmit()` | Tap retry on NetworkError |
| BackStep | `fun backStep()` | Back button or system Back |
| CancelMandate | `fun cancelMandate()` | Cancel from Payee step |

#### DI (Constructor Injection)

- `BeneficiariesRepository` — loads saved payees; also used by pay-domestic-single
- `PaymentInitiationRepository` — stages consent (`POST /domestic-standing-order-consents`) and submits (`POST /domestic-standing-orders`)

`AccountsOverviewRepository` is deliberately **NOT** injected. This rail has no debtor-account step.

---

## 4. Navigation

### Entry Points

| Source | Trigger | Params |
|--------|---------|--------|
| payments | Tap "Domestic standing order" tile | none |

### Outgoing Navigation

| Target | Event | Origin Component | Param Map | Condition |
|--------|-------|------------------|-----------|-----------|
| payment-consent | NavigateToPaymentConsent | confirm_button → ConfirmAndStageConsent | consentId, paymentFamily="domestic-standing-order" | POST consents returns 201 |
| payment-status | NavigateToPaymentStatus | (post-authorisation resume) | paymentId, paymentFamily="domestic-standing-order" | POST orders returns 201 |
| payments | CancelMandate | back_icon on Payee step | none | User exits from first step |

### Route Definition

- **Route**: `PayDomesticStandingOrderRoute`
- **Params**: none on entry
- **Deep Link**: none (no deep_link system_capability declared)

### Nav Origins

| Component | Action | Target | Params Resolved From |
|-----------|--------|--------|----------------------|
| confirm_button | ConfirmAndStageConsent | payment-consent | stagedConsent.Data.ConsentId + literal |
| (post-consent resume) | SubmitStandingOrder | payment-status | mandate.Data.DomesticStandingOrderId + literal |
| back_icon (Payee) | CancelMandate | payments | none |

---

## 5. API Dependencies

| # | Endpoint | Method | Auth | Headers |
|---|----------|--------|:----:|---------|
| 1 | /domestic-standing-order-consents | POST | client_credentials_payments_scope | x-jws-signature, x-idempotency-key |
| 2 | /domestic-standing-order-consents/{ConsentId} | GET | client_credentials_payments_scope | — |
| 3 | /domestic-standing-orders | POST | psu_authorization_code | x-jws-signature, x-idempotency-key |
| 4 | /domestic-standing-orders/{DomesticStandingOrderId} | GET | client_credentials_payments_scope | — |

### Error Matrix

| Endpoint | Code | When | Retry | Message Key | Recovery |
|----------|------|------|:-----:|-------------|----------|
| POST consents | U004 | Permission or MandateRelatedInformation omitted | No | field_not_expected | Error panel |
| POST consents | U005 | InstructedAmount, PointInTime, or MandateRelatedInformation.Reference sent | No | field_not_expected | Error panel |
| POST consents | U002 | Frequency.Type outside accepted 5 values | No | invalid_frequency | Error panel |
| POST consents | U003 | FinalPaymentDateTime before first / beyond 12 months / today or tomorrow | No | invalid_mandate_dates | Return to Schedule |
| POST consents | U019 | x-jws-signature missing | No | signature_missing | Error panel |
| POST orders | U009 | Consent not Authorised | Yes | consent_not_authorised | Error panel with re-authorise |
| Any | IOException | Network timeout | Yes | network_error | Error panel with retry |

---

## 6. Design Tokens Used

| Token Path | Light Value | Used By |
|-----------|------------|---------|
| colors.primary | #266489 | confirm_button background, outline_focus |
| colors.onPrimary | #FFFFFF | confirm_button label |
| colors.surface | #F7F9FF | screen background |
| colors.surfaceContainerLow | #F1F4F9 | beneficiary_list item background |
| colors.onSurface | #181C20 | review_card row values, amount input text |
| colors.onSurfaceVariant | #41474D | field labels, helper text, supporting text |
| colors.error | #BA1A1A | form.field.outline_error, error_panel icon |
| colors.surfaceVariant | #DDE3EA | instruction_established chip container (INCO) |
| semantic.status.warning_container | #EADDFF / #4C4162 | amend_notice banner container |
| semantic.payment_disposition.instruction_established.icon | event_repeat | INCO status chip |
| form.field.radius | radius.sm (8dp) | text_field corners |
| radius.full | 9999dp | confirm_button (filled_pill style) |
| radius.md | 12dp | review_card, no_debtor_note banner |
| typography.font_family.mono | Roboto Mono | amount_field input display |

---

## 7. Testing

| ID | Scenario | Priority | Expected Test File |
|----|----------|:--------:|--------------------|
| TC-PSO-001 | Happy path: weekly mandate staged and submitted | P0 | PayDomesticStandingOrderViewModelTest |
| TC-PSO-002 | InstructedAmount returns U005 | P0 | PayDomesticStandingOrderViewModelTest |
| TC-PSO-003 | Invalid frequency returns U002 | P0 | PayDomesticStandingOrderViewModelTest |
| TC-PSO-004 | FinalPaymentDateTime beyond 12 months returns U003 | P0 | PayDomesticStandingOrderViewModelTest |
| TC-PSO-005 | No DebtorAccount in staged body | P0 | PayDomesticStandingOrderViewModelTest |
| TC-PSO-006 | Reference in RemittanceInformation.Unstructured stages 201 | P0 | PayDomesticStandingOrderViewModelTest |
| TC-PSO-007 | Open-ended mandate (no FinalPaymentDateTime) stages 201 | P0 | PayDomesticStandingOrderViewModelTest |
| TC-PSO-008 | INCO renders instruction_established disposition, not success | P0 | PaymentStatusViewModelTest |
| TC-PSO-009 | New mandate absent from AIS list — no list refresh attempted | P0 | (integration-level; ViewModel boundary) |
| TC-PSO-010 | MNTH accepted; MONT typo returns U002 | P1 | PayDomesticStandingOrderViewModelTest |
| TC-PSO-011 | FirstPaymentDateTime always sent even when schema-optional | P1 | PayDomesticStandingOrderViewModelTest |
| TC-PSO-012 | Date values echo byte-identical; Initiation key order normalised on submit | P1 | PayDomesticStandingOrderViewModelTest |
| TC-PSO-013 | MandateRelatedInformation.Reference refused (U005) | P1 | PayDomesticStandingOrderViewModelTest |
| TC-PSO-014 | Amount is quoted 2dp string; CountPerPeriod is unquoted number | P1 | PayDomesticStandingOrderViewModelTest |
| TC-PSO-015 | Error surface iterates full Errors[] array | P2 | PayDomesticStandingOrderViewModelTest |

**Coverage target**: 95% (P0 + P1)

---

## 8. Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| FinalPaymentDateTime omitted | Mandate stages open-ended; success renders "Until further notice" for end date row |
| Picker offers only 5 frequencies | ADHO, INDA, MIAN, DAIL unreachable; U002 should be an impossible state |
| AIS read after create | New mandate NOT in AIS list; screen does not navigate to or refresh standing-orders |
| varyingAmounts = true with 1.00/2.00/3.00 | Stages 201; equality rule may fire at authorisation/execution (untested; open gap GAP-PSO-AMOUNT-EQUALITY) |
| FirstPaymentDateTime in response | Always present because this app always sends it; review screen always has a truthful date |
| PointInTime present in AIS-read mandate | Strip before replaying as PIS consent (U005 if sent on write side) |
| StatusUpdateDateTime unchanged on AWAU→AUTH | Do not surface as "last updated"; it is a known API behaviour, not missing data |
| Bank writes DebtorAccount (UK.OBIE.PAN) into authorised consent | Echo it in submit; do not re-derive or omit |

---

## 9. Feature Flags

(none)

---

## 10. Data Flow

| Screen | Trigger | Endpoints Called | Produces State | Error Paths |
|--------|---------|-----------------|----------------|-------------|
| pay-domestic-standing-order | on_mount | GET /beneficiaries | Content(Payee) | Error(NetworkError) |
| pay-domestic-standing-order | stage_consent | POST /domestic-standing-order-consents | Submitting(StagingConsent → AwaitingAuthorisation) | Error(U002/U003/U004/U005/U019) |
| pay-domestic-standing-order | resume_after_authorisation | GET /domestic-standing-order-consents/{id}, POST /domestic-standing-orders | Submitting(SubmittingPayment) → NavigateToPaymentStatus | Error(U009/NetworkError) |
| pay-domestic-standing-order | retry_submit | Same as resume (reused idempotency key) | Same | Same |

### Side Effects

| Screen | Trigger | Kind | Target |
|--------|---------|------|--------|
| pay-domestic-standing-order | stage_consent | navigation | payment-consent (consentId, paymentFamily) |
| pay-domestic-standing-order | submit success | navigation | payment-status (paymentId, paymentFamily) |

---

## 11. Referenced Journeys

**None. No journey in `idea-layer/journeys/` walks this screen.**

All five journeys were checked against their `screen_sequence`: `consumer-authentication`,
`consumer-accounts-payments`, `consumer-cards-financing`, `consumer-insights-utilities`,
`consumer-profile-settings`. This feature appears in none of them.

`consumer-cards-financing` (read its `name` — "Consumer Recurring Payments Review") comes closest and
still stops short: its final step lands on the `payments` hub with the intent *"set up a NEW standing
order, since the existing one cannot be edited here"* and the success signal *"taps the Domestic
standing order tile"* — the journey ends on the tap. It never enters this form. That hand-off exists
because a PISP may not amend or cancel a standing order (OBL Customer Experience Guidelines), which
is the same constraint §4 records under Post-creation constraints.

Recorded as a gap in `journeys/INDEX.md` § "Coverage gaps owed". To close it:
`/idea journey new --cover pay-domestic-standing-order` — extending `consumer-cards-financing` by one
step is the natural shape, since the journey already delivers the PSU to the tile.

---

## 12. DTOs Consumed

| DTO | Source | Kind |
|-----|--------|------|
| ObPaymentError | dtos/ObPaymentError.yaml | Shared error shape; all 400s on all four endpoints deserialise to this |
| DomesticStandingOrderConsent | api.yaml | Consent resource (ConsentId, Status, Initiation, Charges) |
| DomesticStandingOrder | api.yaml | Payment resource (DomesticStandingOrderId, Status) |

---

## 13. Dependencies

**Tier**: feature

| Dependency | Type | Required | Notes |
|------------|------|:--------:|-------|
| beneficiaries | data_source | Yes | BeneficiaryListLoaded before Payee step is usable |
| payment-consent | child | Yes | Receives consentId + paymentFamily="domestic-standing-order" |
| payment-status | child | Yes | Receives paymentId + paymentFamily="domestic-standing-order" |
| payments | parent | Yes | Entry point — "Domestic standing order" tile |
| accounts | explicitly absent | No | No debtor-account step; AccountsOverviewRepository not injected |
