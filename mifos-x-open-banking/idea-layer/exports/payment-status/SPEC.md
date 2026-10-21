# Payment Status — Feature Specification

> Generated from `screens/payment-status/*.yaml` by `/idea-feature-export`
> Schema version: 4.0 · Contract version: 2.0.0
> Quality score: 91/100
> Endpoints: 2 · DTOs: 2 · Components: 9 · Test scenarios: 9

## Lossless Export Contract

This SPEC is the source `/kmp-viewmodel-gen`, `/kmp-screen-gen`, and `/verify --tests` consume.
All sections include: State Defaults, Error Matrix, Nav Origins, and Test Mapping.

---

## 1. Overview

Settlement tracker for a submitted payment or created instruction, **shared by all seven payment
families**. Resolves its endpoint and status ladder from the `paymentFamily` nav param, reads the
family's resource-status GET alongside the consent GET, and renders the current status with the
echoed Initiation. Exists because a successful HSBC submit returns `AcceptedSettlementInProcess`
— accepted, not settled — and without this screen the PSU is told "sent" with no way to learn
whether the money actually landed. For the four deferred families (scheduled and standing-order
variants) it reports that the instruction is set up and says explicitly that individual future
payments cannot be tracked here.

| Attribute         | Value                                      |
|-------------------|--------------------------------------------|
| Feature ID        | `payment-status`                           |
| Cluster           | payment-initiation                         |
| Flow ref          | payments-hub                               |
| Archetype         | detail_screen                              |
| Quality Score     | 91/100                                     |
| Dependency Tier   | feature                                    |
| Acceptance refs   | FR-014, FR-021                             |
| Status            | enriched (re-enriched 2026-08-07)          |
| Revalidation      | owed — approval predates seven-type rewrite |

### Why this screen exists

1. `ACSP` (AcceptedSettlementInProcess) is accepted-NOT-YET-BOOKED. Settlement is asynchronous
   and batched on five-minute boundaries (booking timestamps observed at :01/:02 seconds on every
   boundary). A balance read taken immediately after submit can show no movement for a payment that
   settles minutes later.
2. For the four deferred families, OBIE exposes no per-execution status at all. The resource status
   describes instruction SETUP, not the Nth payment.
3. Write-then-read correlation with AIS is impossible in principle — a PIS standing order (19936)
   was invisible in AIS five minutes after creation; StandingOrderId is absent from every AIS
   standing-order element. The PIS resource is the only source.

---

## 2. Screen Inventory

| # | Screen          | ViewModel                | States               | Description                                   |
|---|-----------------|--------------------------|----------------------|-----------------------------------------------|
| 1 | payment-status  | PaymentStatusViewModel   | loading, content, error | Single resource-status view across 7 families |

No empty state — this screen renders a single payment resource, not a collection.

---

## 3. State Model

### PaymentStatusViewModel

#### State: `PaymentStatusState`

| Field       | Type   | Default   | Nullable | Purpose                                                |
|-------------|--------|-----------|:--------:|--------------------------------------------------------|
| paymentId   | String | ""        | No       | Resource identifier, supplied by nav                   |
| uiState     | PaymentStatusUiState | Loading | No  | Screen rendering state                    |

#### State Defaults

```kotlin
val initial = PaymentStatusState(
  paymentId = "",
  uiState = PaymentStatusUiState.Loading,
)
```

#### Screen State: `PaymentStatusUiState`

```kotlin
sealed interface PaymentStatusUiState {
    data object Loading : PaymentStatusUiState
    data class Content(
        val statusCode: String,
        val disposition: Disposition,
        val statusLabel: String,
        val amountLabel: String,
        val creditorName: String,
        val referenceLabel: String?,
        val debtorAccountLabel: String,
        val submittedAtLabel: String,
        val isMandate: Boolean,
        val scheduleLabel: String?,
    ) : PaymentStatusUiState
    data class Error(
        val type: PaymentStatusErrorKind,
        val message: String,
    ) : PaymentStatusUiState
}
```

#### Disposition Enum

```kotlin
enum class Disposition {
    IN_PROGRESS,             // ACSP, AWOP, PDNG, unknown codes
    TERMINAL_SUCCESS,        // ACCC, ACSC, AcceptedCreditSettlementCompleted, AcceptedSettlementCompleted
    TERMINAL_FAILURE,        // RJCT, Rejected, BLCK, Blocked
    INSTRUCTION_ESTABLISHED, // INCO, InitiationCompleted — deferred rails only
}
```

Both v4.0 short forms and v3.1 long forms are matched on EVERY endpoint. A status not in the
vocabulary maps to `IN_PROGRESS` (fail-open safety net — not a substitute for mapping known codes).

#### Errors: `PaymentStatusErrorKind`

| Type             | Retry | Display                                         | Recovery                        | Message Key                              |
|------------------|:-----:|-------------------------------------------------|---------------------------------|------------------------------------------|
| PaymentNotFound  | No    | Informational                                   | Back — resource does not exist  | error.payment_status.not_found           |
| MandateRevoked   | No    | Neutral — rendered from local mandate record    | New mandate, never retry        | error.vrp.revoked                        |
| TokenExpired     | Yes   | Transient                                       | Retry after token refresh       | error.payment_status.token_expired       |
| ConsentRevoked   | No    | Informational — settled payments are unaffected | View Consents CTA               | error.payment_status.consent_revoked     |
| NetworkError     | Yes   | Transient                                       | Retry CTA                       | error.payment_status.network_error       |

MandateRevoked (HTTP 400 + ErrorCode U011 on VRP consent GET) is NOT an error state. The mandate
was deliberately revoked. Render from the local record; offer a new mandate. The U011 Path field
contains a URL, not a JSON pointer — a generic Path-to-field mapper must special-case this code.

#### Actions

| Action           | Params             | User Trigger                                     | Visibility condition              |
|------------------|--------------------|--------------------------------------------------|-----------------------------------|
| LoadPaymentStatus | paymentId: String | On mount; called by RefreshStatus                | Always                            |
| RefreshStatus    | (none)             | Tap refresh_button; auto backing-off poll        | While disposition == in_progress  |
| StartNewPayment  | (none)             | Tap new_payment_button                           | disposition == terminal_failure   |
| NavigateBack     | (none)             | Tap back_button                                  | Always                            |

#### DI (Constructor Injection)

- `SavedStateHandle` — supplies `paymentId` and `paymentFamily` route args
- `PaymentStatusRepository` — wraps the Ktorfit PISP client + the family resolver

---

## 4. Navigation

### Entry Points

| Source                           | Trigger                                   | Params                              |
|----------------------------------|-------------------------------------------|-------------------------------------|
| pay-domestic-single              | Tap "View status" after payment created   | paymentId, paymentFamily            |
| pay-domestic-scheduled           | Tap "View status" after instruction set up| paymentId, paymentFamily            |
| pay-domestic-standing-order      | Tap "View status" after instruction set up| paymentId, paymentFamily            |
| pay-international-single         | Tap "View status" after payment created   | paymentId, paymentFamily            |
| pay-international-scheduled      | Tap "View status" after instruction set up| paymentId, paymentFamily            |
| pay-international-standing-order | Tap "View status" after instruction set up| paymentId, paymentFamily            |
| pay-vrp-mandate                  | Tap "View status" after mandate created   | paymentId, paymentFamily            |
| app_shell_bottom_nav (Pay tab)   | In-flight payment resurface               | paymentId, paymentFamily            |

### Outgoing Navigation

| Target                    | Trigger              | Origin Component     | Condition                      |
|---------------------------|----------------------|----------------------|--------------------------------|
| {originating type screen} | Back button          | back_button          | Always                         |
| payments (hub)            | New payment button   | new_payment_button   | disposition == terminal_failure |
| pay-vrp-mandate           | Manage mandate       | (not in ui.yaml)     | paymentFamily == domestic-vrp  |

### Route Definition

- **Route**: `PaymentStatusRoute`
- **Params**: `paymentId: String (required)`, `paymentFamily: PaymentFamily (required)`
- **Deep Link**: none

### Nav Origins

| Component           | on_click.action   | Target                            | Params Resolved From         |
|---------------------|-------------------|-----------------------------------|------------------------------|
| back_button         | navigate_back     | {originating type screen}         | paymentFamily nav param      |
| refresh_button      | refresh_status    | (none — re-reads same resource)   | current paymentId            |
| new_payment_button  | navigate          | payments hub                      | (cleared form)               |
| retry_button        | refresh_status    | (none — re-reads same resource)   | current paymentId            |

---

## 5. API Dependencies

### Seven-Family Endpoint Resolution Table

| paymentFamily                  | Resource path                        | ID field                     | Consent path                          | Ladder              |
|-------------------------------|--------------------------------------|------------------------------|---------------------------------------|---------------------|
| domestic-payment              | domestic-payments                    | DomesticPaymentId            | domestic-payment-consents             | single              |
| domestic-scheduled-payment    | domestic-scheduled-payments          | DomesticScheduledPaymentId   | domestic-scheduled-payment-consents   | domestic_deferred   |
| domestic-standing-order       | domestic-standing-orders             | DomesticStandingOrderId      | domestic-standing-order-consents      | domestic_deferred   |
| international-payment         | international-payments               | InternationalPaymentId       | international-payment-consents        | single              |
| international-scheduled-payment | international-scheduled-payments   | InternationalScheduledPaymentId | international-scheduled-payment-consents | international_deferred |
| international-standing-order  | international-standing-orders        | InternationalStandingOrderId | international-standing-order-consents | international_deferred |
| domestic-vrp                  | domestic-vrps                        | DomesticVRPId                | domestic-vrp-consents                 | vrp                 |

Base: `https://secure.sandbox.ob.hsbc.co.uk/obie/open-banking/v4.0/pisp`

### Operations Summary

| # | Operation           | Method | Path template                          | Auth                              | Cache  |
|---|---------------------|--------|----------------------------------------|-----------------------------------|--------|
| 1 | get_payment_status  | GET    | /{familyResourcePath}/{paymentId}      | client_credentials_payments_scope | memory |
| 2 | get_consent_status  | GET    | /{familyConsentPath}/{consentId}       | client_credentials_payments_scope | memory |

### Error Matrix

| Operation          | HTTP | Code  | When                                         | Retry | Recovery                              | i18n key                              |
|--------------------|------|-------|----------------------------------------------|:-----:|---------------------------------------|---------------------------------------|
| get_payment_status | 404  | —     | Unknown paymentId                            | No    | Back CTA                              | error.payment_status.not_found        |
| get_consent_status | 400  | U011  | VRP consent GET after revocation             | No    | Render revoked from local record      | error.vrp.revoked                     |
| get_payment_status | 401  | —     | Expired token                                | Yes   | Retry after refresh                   | error.payment_status.token_expired    |
| get_payment_status | 403  | —     | Consent revoked or expired                   | No    | View Consents CTA                     | error.payment_status.consent_revoked  |
| get_payment_status | 429  | U002  | Rate limited                                 | Yes   | Double poll interval; keep last status| (inline banner)                       |
| get_payment_status | I/O  | —     | Network error / timeout                      | Yes   | Retry CTA                             | error.payment_status.network_error    |

### Polling Configuration

| Parameter           | Value                                              |
|---------------------|----------------------------------------------------|
| Starts only if      | disposition == in_progress                         |
| Stops on            | terminal_success, terminal_failure, instruction_established |
| Initial interval    | 3 000 ms                                           |
| Backoff multiplier  | 1.5×                                               |
| Max interval        | 30 000 ms                                          |
| Max duration        | 600 000 ms (10 min)                                |
| On 429              | Double current interval; keep last known status    |
| Deferred note       | Stops on first read — INCO is terminal and stable  |

---

## 6. Design Tokens Used

| Token                                          | Role                | Usage                                         |
|------------------------------------------------|---------------------|-----------------------------------------------|
| semantic.payment_disposition.in_progress       | secondary           | status_chip, in_progress_note visibility      |
| semantic.payment_disposition.terminal_success  | primary             | status_chip                                   |
| semantic.payment_disposition.terminal_failure  | error               | status_chip, new_payment_button visibility    |
| semantic.payment_disposition.instruction_established | onSurfaceVariant | status_chip, instruction_established_note  |
| colors.primary `#266489`                       | primary             | back_button, tonal buttons                    |
| colors.error `#BA1A1A`                         | error               | error_state icon                              |
| colors.surfaceVariant `#DDE3EA`                | surfaceVariant      | instruction_established chip container        |
| colors.onSurfaceVariant `#41474D`              | onSurfaceVariant    | instruction_established chip text, notes      |
| typography.bodyMedium (14/20/400)              | body                | note texts, supporting labels                 |
| typography.titleMedium (16/24/500)             | title               | payment summary card labels                   |
| typography.font_family.mono                    | mono                | amountLabel                                   |
| radius.md (12dp)                               | card                | payment_summary card corner                   |
| spacing.md (16dp)                              | padding             | screen padding, card insets                   |
| spacing.sm (8dp)                               | gap                 | card row gaps                                 |

---

## 7. Testing

| ID           | Scenario                                        | Priority | Expected Test File                                      |
|--------------|-------------------------------------------------|:--------:|---------------------------------------------------------|
| TC-PSTAT-001 | Loading spinner visible on mount                | P0       | PaymentStatusViewModelTest#test_TC_PSTAT_001_loading    |
| TC-PSTAT-002 | ACSP renders as in_progress, never "sent"       | P0       | PaymentStatusViewModelTest#test_TC_PSTAT_002_acsp_in_progress |
| TC-PSTAT-003 | ACCC renders as terminal_success                | P0       | PaymentStatusViewModelTest#test_TC_PSTAT_003_terminal_success |
| TC-PSTAT-004 | Long-form AcceptedCreditSettlementCompleted = ACCC | P1    | PaymentStatusViewModelTest#test_TC_PSTAT_004_dual_encoding |
| TC-PSTAT-005 | INCO renders as instruction_established, not in_progress | P1 | PaymentStatusViewModelTest#test_TC_PSTAT_005_inco_neutral |
| TC-PSTAT-006 | StatusUpdateDateTime not used as poll signal    | P1       | PaymentStatusViewModelTest#test_TC_PSTAT_006_status_field_only |
| TC-PSTAT-007 | Stub Expected* fields never rendered            | P1       | PaymentStatusViewModelTest#test_TC_PSTAT_007_stub_fields |
| TC-PSTAT-008 | 400 U011 renders as revoked, not not-found      | P1       | PaymentStatusViewModelTest#test_TC_PSTAT_008_u011_revoked |
| TC-PSTAT-009 | Loading state visible while fetch pending       | P2       | PaymentStatusViewModelTest#test_TC_PSTAT_009_loading_state |

**Coverage**: P0: 3, P1: 5, P2: 1 (9 total)

---

## 8. Edge Cases

| Scenario                                           | Expected Behavior                                                              |
|----------------------------------------------------|--------------------------------------------------------------------------------|
| Status outside mapped vocabulary                   | Map to in_progress (fail-open safety net); keep polling                        |
| ACSP after 5 minutes with no balance change        | Continue polling; do not infer failure — settlement is batched                 |
| INCO on first read (international deferred)        | Render instruction_established immediately; never start polling                |
| domestic-vrp consent GET returns 400 U011          | Render MandateRevoked from local record; NOT an error state                    |
| Charges absent on international response           | Parse as null; never render "no charge information" as "no charge"             |
| ChargeBearer contradicts Initiation.ChargeBearer   | Show neither, or show Charges[] value only                                     |
| Charges[].Type = UK.OBIE.CHAPSOut on every family  | Never render Type raw to a PSU                                                 |
| ExpectedExecutionDateTime == CreationDateTime      | Do not render it; show Initiation.RequestedExecutionDateTime instead           |
| VRP: ExpectedExecution = CreationDateTime + 30s   | Legitimate settling indicator on VRP only                                      |
| 429 during poll                                    | Double interval; keep last known status; do not render as error                |
| ConsentRevoked (403) after a payment that settled  | Inform only; do not imply the money came back                                  |

---

## 9. Data Flow

| Trigger              | Steps                                                                | Produces State | Stop Set                                    |
|----------------------|----------------------------------------------------------------------|----------------|---------------------------------------------|
| payment_status_load  | resolve family → GET resource → dispositionFor → statusLabelFor     | content / error | —                                          |
| consent_status_load  | GET consent → consentStatus → consentDisposition                    | (enriches content) | —                                        |
| auto_poll            | re-runs payment_status_load on backing-off interval                 | content / error | terminal_success, terminal_failure, instruction_established |
| refresh_status       | re-runs payment_status_load on demand                               | content / error | —                                          |

Cache strategy: `createMemoryStore(fetcher)` keyed by `(paymentFamily, paymentId)`. No Room
persistence — a status written to disk could outlive the consent that permitted the read.

### Side Effects

| Trigger              | Kind      | Target                                    |
|----------------------|-----------|-------------------------------------------|
| navigate_back        | navigate  | {originating type screen via paymentFamily}|
| navigate_to_new_payment | navigate | payments hub                            |

---

## 10. Dependencies

**Tier**: feature

| Dependency                   | Type            | Required | Notes                                          |
|------------------------------|-----------------|:--------:|------------------------------------------------|
| {originating type screen}    | parent          | Yes      | One of the seven; never a fixed screen         |
| payments hub                 | retry-target    | No       | Only on terminal_failure                       |
| ktorfit 2.x                  | library         | Yes      | Seven resource GETs; endpoint resolved from paymentFamily |
| PaymentStatusRepository      | DI              | Yes      | Wraps Ktorfit PISP client + family resolver    |
| SavedStateHandle             | DI              | Yes      | Supplies paymentId + paymentFamily             |

---

## 11. Referenced Journeys

Resolved against `idea-layer/journeys/*.yaml` — a journey is listed here only when this feature's
screen appears in that journey's `screen_sequence`.

| Journey | Name | Persona | Tier | Where this screen appears |
|---|---|---|---|---|
| `consumer-accounts-payments` | Consumer Accounts & Payments | returning consumer | maximum | Step 11 — "confirm the payment actually went", after `payment-consent` and before the return to `home` |

The journey states this screen's core invariant in its own success signal: status reads *in progress*
(ACSP), then settles to ACCC — with the explicit note that it **must NOT read as "sent" on ACSP,
because a successful submit means accepted, not settled**. That is invariant 1 in §12, arrived at
independently from the journey side.

Coverage is one family out of seven. The journey walks `domestic-payment` only, so the `single`
ladder is the only one exercised end-to-end; `domestic_deferred`, `international_deferred` and `vrp`
— the three ladders that carry the INCO / instruction-established and U011 / revoked behaviours — are
reached by no journey. Those depend entirely on TC-PSTAT-005 and TC-PSTAT-008.

---

## 12. Key Invariants

1. **Truthfulness**: Never describe `in_progress` as sent, complete, or successful.
2. **Mandate truthfulness**: Deferred rails report instruction setup; never imply a payment occurred.
3. **Dual encoding**: dispositionFor accepts both v4.0 short codes and v3.1 long forms on every endpoint.
4. **Status field only**: Transitions detected from `Data.Status`; `StatusUpdateDateTime` is inert.
5. **Stub fields**: `ExpectedExecutionDateTime`, `ExpectedSettlementDateTime`, `CutOffDateTime` never rendered on deferred families.
6. **U011**: Renders as revoked mandate from local record, not as generic failure.
7. **No AIS fallback**: Never tell a PSU to check the standing-orders list to verify an instruction.
8. **Charges**: Parse as nullable; never render `Type` raw; show quote as estimated or not at all.
