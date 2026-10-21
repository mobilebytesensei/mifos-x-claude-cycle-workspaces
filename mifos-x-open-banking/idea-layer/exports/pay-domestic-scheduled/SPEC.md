# pay-domestic-scheduled — Feature Specification

> Generated from `screens/pay-domestic-scheduled/{docs,ui,api,flow,data-flow,demo-data}.yaml`
> Schema version: 4.0
> Contract version: 2.1.0
> Quality score: 91/100
> Endpoints: 4 · States: 5 · Actions: 12 · Events: 2 · Test scenarios: 14

## Lossless Export Contract

This SPEC is lossless. The sections below give `/kmp-viewmodel-gen`, `/kmp-screen-gen`, and
`/verify --tests` everything they need to consume from SPEC.md alone:

- **State Defaults** — initial values per state field
- **Error Matrix** — endpoint × error-code × (retry, user message, recovery)
- **Nav Origins** — which component triggers which route
- **Date boundary invariant** — T+1..T+365 picker bounds with asymmetric evidence standing
- **Divergence traps** — five named patterns that produce incorrect behaviour if ported from the reference single-payment rail

---

## 1. Overview

Domestic scheduled payment — one payment to a UK sort code and account number, on a single future
date chosen by the PSU. Five steps in one route (Account → Payee → Amount → Date → Review) backed
by a single ViewModel; back is always a step transition, not a navigation pop. Stages a
domestic-scheduled-payment-consent, hands off to payment-consent for the bank authorisation leg,
then submits directly — there is no funds-confirmation step on this rail family. The instruction
is established at the bank with status PDNG; there is no per-execution status anywhere in OBIE, so
the UI reports setup only, never delivery. The PSU must be told that a PISP cannot amend or cancel
the scheduled payment — they must use the bank's own channel instead.

| Attribute | Value |
|---|---|
| Feature ID | `pay-domestic-scheduled` |
| Flow ref | `pay-domestic-scheduled` |
| Cluster | `payment-initiation` |
| Status | `enriched` |
| Priority | P0 (7 scenarios) / P1 (5 scenarios) / P2 (2 scenarios) |
| Quality Score | 91/100 |
| Dependency Tier | `feature` |
| Archetype | `form` |
| Acceptance refs | FR-012, FR-015, FR-016, FR-017, FR-018, FR-020, FR-021 |
| Inherits from | `pay-domestic-single` (reference rail) |

### User Stories

- As a PSU, I want to schedule a payment on a specific future date, so that I can arrange a
  transfer that happens automatically without being in the app on the day.
- As a PSU, I want a clear date picker showing exactly which dates I may choose, so that I never
  reach an API error by picking an invalid date.
- As a PSU, I want to understand before confirming that I cannot change or cancel the scheduled
  payment through this app, so that I know to use my bank's own channel if I change my mind.
- As a PSU with no eligible accounts, I want a clear explanation of why no accounts are shown,
  so that I understand the limitation rather than assuming the app is broken.

### Success Metrics

| Metric | Target |
|---|---|
| Payment consent staging success rate (sandbox) | ≥ 95% of eligible-account PSUs |
| U003 / U002 date errors from API | 0 (picker bounds block them client-side) |
| Double-submit incidents | 0 (idempotency-key invariant) |
| PSU confusion about amendment/cancellation | 0 (amend_notice shown at Review and Success) |

---

## 2. Screens

| # | Screen | ViewModel | States | Description |
|---|---|---|---|---|
| 1 | `pay-domestic-scheduled` | `PayDomesticScheduledViewModel` | loading, content, content_no_eligible_accounts, submitting, error | Five-step form: Account → Payee → Amount → Date → Review |

### Screen Relationships

Single screen with an internal `step` discriminator. Back from any step after Account is a step
transition (`BackStep` action), not a navigation pop. The route is entered from the payments hub
and exits to `payment-consent` (after consent staging), resumes and submits without a funds check,
then exits to `payment-status`.

---

## 3. State Model

### PayDomesticScheduledViewModel

#### State: `PayDomesticScheduledUiState`

The sealed state hierarchy has four top-level variants with an inner `step` on Content:

| Variant | Inner discriminator | Purpose |
|---|---|---|
| `Loading` | — | Fetching accounts and beneficiaries on mount |
| `Content(step: PaymentStep)` | `Account \| Payee \| Amount \| Date \| Review` | Active form, five-step |
| `Submitting(stage: SubmittingStage)` | `StagingConsent \| AwaitingAuthorisation \| SubmittingPayment` | In-flight API call |
| `Error(type: PaymentErrorType)` | — | Terminal error surface |

#### Content State Fields

| Field | Type | Default | Nullable | Purpose |
|---|---|---|---|---|
| `step` | `PaymentStep` | `PaymentStep.Account` | No | Current form step (five variants) |
| `eligibleDebtorAccounts` | `List<AccountSummary>` | `emptyList()` | No | SortCodeAccountNumber accounts only |
| `hiddenAccountCount` | `Int` | `0` | No | Count of accounts excluded from picker |
| `debtorAccountId` | `String?` | `null` | Yes | Selected funding account ID |
| `beneficiaries` | `List<BeneficiarySummary>` | `emptyList()` | No | Eligible payees |
| `creditor` | `BeneficiarySelection?` | `null` | Yes | Selected or manually-entered payee |
| `manualEntryVisible` | `Boolean` | `false` | No | Whether manual sort-code / account-number fields are shown |
| `sortCodeInput` | `String` | `""` | No | Raw sort-code input (stripped to 6 digits before wire) |
| `accountNumberInput` | `String` | `""` | No | Raw account-number input (8 digits) |
| `payeeNameInput` | `String` | `""` | No | CreditorAccount.Name — mandatory on this rail |
| `amountMinorUnits` | `Long` | `0L` | No | Payment amount in pence; converted to major-unit string at OBIE boundary |
| `amountProblem` | `AmountProblem?` | `null` | Yes | Inline validation: NotANumber, NotPositive |
| `referenceInput` | `String` | `""` | No | Unstructured remittance reference (omitted if blank) |
| `requestedExecutionDate` | `LocalDate?` | `null` | Yes | PSU-chosen execution date; set by `SelectExecutionDate` |
| `dateProblem` | `DateProblem?` | `null` | Yes | Null when date is valid; set when programmatic path violates bounds |
| `minSelectableDate` | `LocalDate` | `today + 1` | No | Picker lower bound (follows Guide §22.2.1 — not a measured value) |
| `maxSelectableDate` | `LocalDate` | `today + 365` | No | Picker upper bound (measured: T+365 stages 201, T+366 returns U002) |
| `feeLabel` | `String?` | `null` | Yes | Populated from Charges[] after staging; null before consent exists |
| `idempotencyKey` | `String` | `""` | No | Generated once, reused for stage + submit + retries |
| `stagedConsentId` | `String?` | `null` | Yes | From POST /domestic-scheduled-payment-consents |
| `authorisedInitiation` | `DomesticScheduledInitiation?` | `null` | Yes | Parsed object from authorised consent; forwarded as-is on submit |

#### State Defaults (for /kmp-viewmodel-gen)

```kotlin
val initial = PayDomesticScheduledUiState.Loading
// After load:
val initialContent = PayDomesticScheduledUiState.Content(
  step = PaymentStep.Account,
  eligibleDebtorAccounts = emptyList(),
  hiddenAccountCount = 0,
  debtorAccountId = null,
  beneficiaries = emptyList(),
  creditor = null,
  manualEntryVisible = false,
  sortCodeInput = "",
  accountNumberInput = "",
  payeeNameInput = "",
  amountMinorUnits = 0L,
  amountProblem = null,
  referenceInput = "",
  requestedExecutionDate = null,
  dateProblem = null,
  minSelectableDate = LocalDate.now().plusDays(1),
  maxSelectableDate = LocalDate.now().plusDays(365),
  feeLabel = null,
  idempotencyKey = "",
  stagedConsentId = null,
  authorisedInitiation = null,
)
```

#### Screen State Enum: `PaymentStep`

```kotlin
enum class PaymentStep { Account, Payee, Amount, Date, Review }
```

Note: `Date` is the only step this rail adds over the reference single-payment rail.

#### Submitting Stage Enum: `SubmittingStage`

```kotlin
enum class SubmittingStage { StagingConsent, AwaitingAuthorisation, SubmittingPayment }
```

Note: There is NO `ConfirmingFunds` stage. This rail has no funds-confirmation endpoint.
Inserting one would call an endpoint that does not exist.

#### Error Types: `PaymentErrorType`

| Type | Retry | Display | Recovery | Message Key |
|---|---|---|---|---|
| `MissingRequiredField` | No | error_panel | Implementation fault — Permission and date are always sent | `strings.error.payment.missing_field` |
| `DateInPast` | No | error_panel + Return to date CTA | Picker bounds prevent this; unreachable in normal flow | `strings.error.payment.date_in_past` |
| `DateOutOfRange` | No | error_panel + Return to date CTA | Picker bounds prevent this; unreachable in normal flow | `strings.error.payment.date_out_of_range` |
| `SignatureMissing` | No | error_panel | Not user-recoverable | `strings.error.payment.signature_missing` |
| `ConsentNotAuthorised` | Yes | error_panel + Re-authorise CTA | Re-authorise restarts app-to-app leg | `strings.error.payment.consent_not_authorised` |
| `InitiationMismatch` | No | error_panel | Re-read authorised consent and resubmit | `strings.error.payment.initiation_mismatch` |
| `NetworkError` | Yes | error_panel | Retry — idempotency key reused | `strings.error.payment.network_error` |

#### Events: `PayDomesticScheduledEvent`

| Event | Params | Trigger |
|---|---|---|
| `NavigateToPaymentConsent` | `consentId: String, paymentFamily: String` | After 201 on POST /domestic-scheduled-payment-consents |
| `NavigateToPaymentStatus` | `paymentId: String, paymentFamily: String` | After 201 on POST /domestic-scheduled-payments |

#### Actions: `PayDomesticScheduledAction`

| Action | Params | User Trigger |
|---|---|---|
| `LoadPaymentSources` | — | On mount |
| `SelectDebtorAccount` | `accountId: String` | Tap account row in debtor_account_list (Step 1) |
| `SelectCreditor` | `selection: BeneficiarySelection` | Tap beneficiary row (Step 2) or confirm manual fields |
| `EnterAmount` | `rawInput: String` | Keystroke in amount_field (Step 3) |
| `EnterReference` | `text: String` | Keystroke in reference_field (Step 3) |
| `SelectExecutionDate` | `date: LocalDate` | Tap day in execution_date_picker (Step 4) |
| `ReviewPayment` | — | Advance from Date step to Review |
| `ConfirmAndStageConsent` | — | Tap confirm_button (Step 5 / Review) |
| `SubmitPayment` | `consentId: String` | Auto-triggered after payment-consent returns AUTH |
| `RetrySubmit` | — | Tap Retry when error.type is NetworkError or ConsentNotAuthorised |
| `BackStep` | — | Tap system Back / navigation_icon while on Steps 2–5 |
| `CancelPayment` | — | Tap Cancel or Back on Step 1 |

#### DI (Constructor Injection)

- `AccountsOverviewRepository` — supplies accounts list for debtor picker
- `BeneficiariesRepository` — supplies beneficiaries list for payee picker
- `PaymentInitiationRepository` — stage consent, submit payment (no funds-confirmation call)

---

## 4. Navigation

### Entry Points

| Source | Trigger | Params |
|---|---|---|
| `payments` hub | Tap "Pay on a date" / domestic scheduled tile | none |

### Outgoing Navigation

| Target | Event | Origin Component | Param Map | Condition |
|---|---|---|---|---|
| `payment-consent` | `NavigateToPaymentConsent` | `confirm_button` (indirect, via ViewModel) | `consentId`, `paymentFamily="domestic-scheduled-payment"` | 201 on POST /domestic-scheduled-payment-consents |
| `pay-domestic-scheduled` | (resume) | payment-consent callback | `consentId` | Consent reaches AUTH — resumes at submit, skipping funds check |
| `payment-status` | `NavigateToPaymentStatus` | Auto (ViewModel, after submit) | `paymentId`, `paymentFamily="domestic-scheduled-payment"` | 201 on POST /domestic-scheduled-payments |
| `payments` | Cancel / BackStep on Account | `navigation_icon` / system Back on Step 1 | none | User cancels |

### Route Definition

- **Route**: `PayDomesticScheduledRoute`
- **Params**: none (entered from payments hub with no deep-link payload); `consentId` is passed
  back on resume from payment-consent
- **Deep Link**: none declared

### Nav Params Mirror

| Target | Param | Type | Required | Source |
|---|---|---|---|---|
| `payment-consent` | `consentId` | `String` | Yes | `stagedConsent.Data.ConsentId` (e.g. "45175") |
| `payment-consent` | `paymentFamily` | `String` | Yes | Hard-coded `"domestic-scheduled-payment"` |
| `payment-status` | `paymentId` | `String` | Yes | `submit.Data.DomesticScheduledPaymentId` (e.g. "19919") |
| `payment-status` | `paymentFamily` | `String` | Yes | Hard-coded `"domestic-scheduled-payment"` |

### Nav Origins

| Component | Action | Target | Params Resolved From |
|---|---|---|---|
| `confirm_button` | `ConfirmAndStageConsent` | `payment-consent` | `stagedConsent.Data.ConsentId` |
| `navigation_icon` / Back on Account | `CancelPayment` | `payments` | — |
| Auto (ViewModel) after auth return | `SubmitPayment` | `payment-status` | `payment.Data.DomesticScheduledPaymentId` |

---

## 5. API Dependencies

| # | Operation ID | Endpoint | Method | Auth | Funds Conf. | Cache | Offline |
|---|---|---|---|---|---|---|---|
| 1 | `stage_domestic_scheduled_consent` | `/obie/open-banking/v4.0/pisp/domestic-scheduled-payment-consents` | POST | client_credentials | None (no endpoint) | none | error |
| 2 | `get_domestic_scheduled_consent_status` | `/obie/open-banking/v4.0/pisp/domestic-scheduled-payment-consents/{ConsentId}` | GET | client_credentials | — | none | error |
| 3 | `submit_domestic_scheduled_payment` | `/obie/open-banking/v4.0/pisp/domestic-scheduled-payments` | POST | psu_authorization_code | — | none | error |
| 4 | `get_domestic_scheduled_payment_status` | `/obie/open-banking/v4.0/pisp/domestic-scheduled-payments/{DomesticScheduledPaymentId}` | GET | client_credentials | — | none | error |

Resource host: `https://secure.sandbox.ob.hsbc.co.uk`
Authorize host (browser leg only): `https://sandbox.ob.hsbc.co.uk/obie/open-banking/v1.1/oauth2/authorize`
Auth scheme: mTLS + `private_key_jwt` (PS256) + authorization-code, FAPI 1.0 Advanced

### Error Matrix

| Endpoint | Code | When | Retry | Recovery UI |
|---|---|---|---|---|
| stage_consent | U004 | `Data.Permission` omitted | No | Implementation fault — always send `"Create"` |
| stage_consent | U004 | `RequestedExecutionDateTime` omitted | No | Return to date step |
| stage_consent | U003 | Date is today or in the past | No | Return to date step — picker should prevent |
| stage_consent | U002 | Date beyond T+365 | No | Return to date step — picker should prevent |
| stage_consent | U019 | x-jws-signature missing or invalid | No | Not user-recoverable |
| submit_payment | U009 | Consent not in Authorised status | Yes | Re-authorise CTA |
| submit_payment | U008 | Submitted Initiation does not match authorised consent | No | Re-read authorised consent |
| submit_payment | U019 | x-jws-signature missing | No | Not user-recoverable |
| Any | IOException/timeout | Network failure | Yes | Retry — idempotency key reused, safe |

### Endpoint Details

#### `stage_domestic_scheduled_consent` (POST)

Stages a domestic-scheduled-payment-consent. Requires `Data.Permission: "Create"` (mandatory field
absent from the single-payment reference rail) and `Initiation.RequestedExecutionDateTime` (ISO 8601,
strictly tomorrow to T+365). Returns ConsentId and status AWAU. The Charges[] array holds
`0.05 GBP UK.OBIE.CHAPSOut` at staging.

**Mandatory body fields not on the single-payment rail**:
- `Data.Permission: "Create"` — omit → U004 at `Data.Permission`
- `Data.Initiation.RequestedExecutionDateTime` — omit → U004 at `Data.Initiation.RequestedExecutionDateTime`

**Date bounds** (measured against HSBC sandbox):
- T+0 → U003 "You cannot trigger a Payment request for a date in the past"
- T+7 → 201 AWAU (lowest value ever accepted in corpus)
- T+365 → 201 AWAU (exact ceiling, measured)
- T+366 → U002 "Initiation.RequestedExecutionDateTime is invalid"
- T+1..T+6: never probed; floor follows Guide §22.2.1 ("Today +1"), not observation

**Timestamp normalisation**: Time component is discarded. `2026-08-13T10:28:58+00:00` becomes
`2026-08-13T00:00:00+00:00`. The Review step must show the date only — the bank does not honour
the time.

**Errors**: U004 (Permission or DateTime omitted), U003 (date in past), U002 (date > T+365), U019

#### `get_domestic_scheduled_consent_status` (GET)

Polls for consent status. Status ladder: AWAU → AUTH → COND.
`StatusUpdateDateTime` does NOT move on the AWAU → AUTH transition (five response timestamps
are all identical stub values on every domestic 201). Auth must be detected from `Data.Status` only.

#### `submit_domestic_scheduled_payment` (POST)

Submits the payment after consent reaches AUTH. Forwards the parsed `Initiation` object read from
the authorised consent (not a re-serialised copy — the server reorders Initiation keys between
SP-D06 and SP-I07, so string comparison or hashing would reject a valid payment). No
funds-confirmation call precedes this. Returns `DomesticScheduledPaymentId` and status PDNG.

**Errors**: U009 (consent not AUTH), U008 (Initiation mismatch), U019

#### `get_domestic_scheduled_payment_status` (GET)

Reads resource status. Ladder: PDNG → INCO. Both mean the instruction is established — neither
means money moved. There is no per-execution status in OBIE. The UI must never render either
as "paid", "sent", or "completed".

---

## 6. Design Tokens Used

| Token | Value | Used By |
|---|---|---|
| `colors.primary` | `#266489` | confirm_button fill, step_indicator active step |
| `colors.onPrimary` | `#FFFFFF` | confirm_button label |
| `colors.surface` | `#F7F9FF` | screen background |
| `colors.surfaceContainerLow` | `#F1F4F9` | review_card background |
| `colors.onSurface` | `#181C20` | primary text labels |
| `colors.onSurfaceVariant` | `#41474D` | date_normalisation_note, helper text, secondary rows |
| `colors.secondaryContainer` | `#D3E5F5` | no_funds_check_note banner background |
| `colors.onSecondaryContainer` | `#384956` | no_funds_check_note banner text |
| `colors.error` | `#BA1A1A` | error_panel, field error text |
| `semantic.payment_disposition.instruction_established.container` | `#DDE3EA` (light) | status chip after submit |
| `semantic.payment_disposition.instruction_established.on_container` | `#41474D` (light) | status chip text |
| `typography.bodyLarge` | 16sp / 400 | list primary text, field input |
| `typography.bodySmall` | 12sp / 400 | date_normalisation_note, field helper |
| `typography.headlineSmall` | 24sp / 400 | amount_field input |
| `typography.titleMedium` | 16sp / 500 | review_card section label |
| `typography.labelLarge` | 14sp / 500 | confirm_button label |
| `radius.sm` | 8dp | text_field, date_picker frame |
| `radius.md` | 12dp | review_card, banners |
| `radius.full` | 9999dp | confirm_button pill |
| `spacing.md` | 16dp | screen padding, component gap |

---

## 7. Testing

| ID | Scenario | Priority | Coverage |
|---|---|---|---|
| TC-PSCH-001 | Account step shows only SortCodeAccountNumber accounts | P0 | eligibility filter |
| TC-PSCH-002 | Date picker lower bound is tomorrow (T+1 per Guide §22.2.1) | P0 | date boundary |
| TC-PSCH-003 | Date picker upper bound is T+365; T+366 disabled | P0 | date boundary |
| TC-PSCH-004 | Saturday is selectable (observed: 2026-09-05 staged 201) | P0 | weekend acceptance |
| TC-PSCH-005 | No funds-confirmation call is made at any point in the flow | P0 | no funds check |
| TC-PSCH-006 | PDNG and INCO both render as "instruction established", never "paid" | P0 | truthfulness invariant |
| TC-PSCH-007 | amend_notice is visible on Review step and on Success state | P0 | amendment disclosure |
| TC-PSCH-008 | Review shows RequestedExecutionDate chosen by PSU, not a stub timestamp | P1 | timestamp display |
| TC-PSCH-009 | Confirm button label reads "Schedule payment", not "Send £X.XX" | P1 | CTA label |
| TC-PSCH-010 | no_funds_check_note banner is present on Review step | P1 | UX copy |
| TC-PSCH-011 | Request body contains no ExchangeRateInformation block | P1 | request shape |
| TC-PSCH-012 | SCASupportData block does not skip the payment-consent auth leg | P1 | SCA exemption |
| TC-PSCH-013 | Error surface renders every entry in Errors[] (two entries at once possible) | P2 | error rendering |
| TC-PSCH-014 | Idempotency key is stable across retries (reused, not regenerated) | P2 | idempotency |

**Coverage target**: P0 (7): 100% · P1 (5): 100% · P2 (2): best-effort

---

## 8. Edge Cases

| Scenario | Expected Behavior |
|---|---|
| PSU selects T+365 (the last valid date) | Picker allows it; consent stages 201 |
| PSU selects a Saturday | Picker allows it; consent stages 201 (observed vs. Guide §22.2.1) |
| Date normalisation: time component sent → discarded | Review shows date only, no time of day |
| Consent status stays AWAU after app-to-app authorise round-trip | Not authorised; re-authorise CTA shown |
| Five stub timestamps arrive on 201 response | None displayed; show requestedExecutionDate instead |
| Errors[] array has two entries | Both displayed; keyed on ErrorCode + Path (case-insensitive) |
| ConsentId is a short integer string ("45175") | Never logged, never placed in URLs or analytics |
| PSU retries after NetworkError | Same idempotency key reused; no double-charge risk |

---

## 9. Feature Flags

(none)

---

## 10. Data Flow

| Trigger | Endpoints Called | Produces State | Cache | Error Paths |
|---|---|---|---|---|
| on_mount / LoadPaymentSources | accounts-list, beneficiaries-list | Loading → Content(Account) | memory (AccountsOverviewStore, BeneficiariesStore) | Error(NetworkError) |
| ConfirmAndStageConsent | POST /domestic-scheduled-payment-consents | Content(Review) → Submitting(StagingConsent) → Submitting(AwaitingAuthorisation) | none | Error(MissingRequiredField \| DateInPast \| DateOutOfRange \| SignatureMissing) |
| resume_after_authorisation | GET /domestic-scheduled-payment-consents/{id}, POST /domestic-scheduled-payments | Submitting(AwaitingAuthorisation) → Submitting(SubmittingPayment) → payment-status | none | Error(ConsentNotAuthorised \| InitiationMismatch \| NetworkError) |
| retry_submit | GET /domestic-scheduled-payment-consents/{id}, POST /domestic-scheduled-payments | Same as resume_after_authorisation | none | Same as above |

### Side Effects

| Trigger | Kind | Target |
|---|---|---|
| ConfirmAndStageConsent | deep_link / hand-off | payment-consent feature with consentId |
| resume_after_authorisation (submit 201) | navigate | payment-status feature with paymentId |

---

## 11. Referenced Journeys

**None. No journey in `idea-layer/journeys/` walks this screen.**

All five journeys were checked against their `screen_sequence`: `consumer-authentication`,
`consumer-accounts-payments`, `consumer-cards-financing`, `consumer-insights-utilities`,
`consumer-profile-settings`. `pay-domestic-scheduled` appears in none of them —
`consumer-accounts-payments` walks the domestic *single* rail, and no journey covers a deferred rail.
This is a known, recorded gap: `journeys/INDEX.md` § "Coverage gaps owed" names this feature.

The row previously printed here — "UK PSU scheduling a future-dated domestic transfer" — was not a
journey. It was a restatement of this feature's own first user story, formatted as if it had been
resolved from a journey file. Removed 2026-08-07.

To close the gap: `/idea journey new --cover pay-domestic-scheduled`.

---

## 12. DTOs Consumed

| DTO | Version | Source | Kind |
|---|---|---|---|
| `DomesticScheduledPaymentConsentRequest` | v4.0 | POST /domestic-scheduled-payment-consents body | request |
| `DomesticScheduledPaymentConsentResponse` | v4.0 | POST/GET /domestic-scheduled-payment-consents response | response |
| `DomesticScheduledPaymentRequest` | v4.0 | POST /domestic-scheduled-payments body | request |
| `DomesticScheduledPaymentResponse` | v4.0 | POST/GET /domestic-scheduled-payments response | response |
| `ObPaymentError` | shared | 400 body on all four operations | error |

---

## 13. Dependencies

**Tier**: `feature`

| Dependency | Type | Required | Notes |
|---|---|---|---|
| `accounts` | data_source | Yes | Debtor account picker |
| `beneficiaries` | data_source | Yes | Payee picker |
| `payment-consent` | child | Yes | Bank authorisation leg |
| `payment-status` | child | Yes | Result surface after submit |
| `payments` | parent | Yes | Hub entry point |

**Library**: `de.jensklingenberg.ktorfit:ktorfit-lib:2.x` — REST client for the four endpoints.

---

## Divergence Traps (from docs.yaml — implementation MUST avoid)

| Trap | Why Wrong | Correct |
|---|---|---|
| Reusing funds-confirmation step from single-payment rail | No such endpoint on this family; today's balance says nothing about execution day | No funds check. Review step shows `no_funds_check_note` banner |
| Mapping INCO to terminal_success disposition | INCO means the instruction is established, not that money moved | Both PDNG and INCO → `instruction_established` chip; never "paid" |
| Filtering date picker to working days | HSBC accepted a Saturday (2026-09-05, R15-A02) despite Guide §22.2.1 | Allow weekends; bound T+1..T+365 only |
| Rendering CutOffDateTime as a submit-by deadline | It is a copy of CreationDateTime and is already past when read | Display only the PSU-chosen requestedExecutionDate |
| Treating an accepted SCASupportData exemption as authorisation granted | The block is echoed back inert; consent still lands AWAU | Always route through payment-consent; never infer auth from a 201 |
