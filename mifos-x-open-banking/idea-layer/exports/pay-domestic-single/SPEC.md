# pay-domestic-single — Feature Specification

> Generated from `screens/pay-domestic-single/{docs,ui,api,flow}.yaml`
> Schema version: 4.0
> Contract version: 2.1.0
> Quality score: 94/100
> Endpoints: 5 · States: 5 · Actions: 13 · Events: 2 · Test scenarios: 16

## Lossless Export Contract

This SPEC is lossless. The sections below give `/kmp-viewmodel-gen`, `/kmp-screen-gen`, and
`/verify --tests` everything they need to consume from SPEC.md alone:

- **State Defaults** — initial values per state field
- **Error Matrix** — endpoint × error-code × (retry, user message, recovery)
- **Nav Origins** — which component triggers which route
- **Eligibility invariant** — client-side pre-filter rules for both pickers

---

## 1. Overview

Domestic single payment — pay a person now, in sterling, to a UK sort code and account number.
Four steps in one route (Account → Payee → Amount → Review) backed by a single ViewModel; back
is a step transition, not a nav pop. Stages a domestic-payment-consent, hands off to
payment-consent for the bank authorisation leg, runs funds-confirmation, then submits and forwards
the result to payment-status. This is the REFERENCE rail — the other five PIS types document their
differences as deltas from this contract.

| Attribute | Value |
|---|---|
| Feature ID | `pay-domestic-single` |
| Flow ref | `pay-domestic-single` |
| Cluster | `payment-initiation` |
| Status | `enriched` |
| Priority | P0 (9 scenarios) / P1 (6 scenarios) / P2 (1 scenario) |
| Quality Score | 94/100 |
| Dependency Tier | `feature` |
| Archetype | `form` |
| Acceptance refs | FR-012, FR-015, FR-016, FR-017, FR-018, FR-021 |

### User Stories

- As a PSU, I want to pay someone by sort code and account number now, so that I can send money
  immediately without leaving the app.
- As a PSU with a credit card and no current account, I want to see a clear explanation of why no
  accounts are available, so that I understand the limitation rather than assuming the app is broken.
- As a PSU, I want to review the exact amount, payee and fee before confirming, so that I know
  precisely what I am committing to before money moves.
- As a PSU, I want safe retry behaviour after a network failure, so that a dropped connection cannot
  cause me to be charged twice.

### Success Metrics

| Metric | Target |
|---|---|
| Payment submission success rate (sandbox) | ≥ 95% of eligible-account PSUs |
| Double-submit incidents | 0 (idempotency-key invariant) |
| Ineligible-account confusion reports | 0 (pre-filter + explanatory note) |
| U004 CreditorAccount.Name rejections from API | 0 (client-side validation gate) |

---

## 2. Screens

| # | Screen | ViewModel | States | Description |
|---|---|---|---|---|
| 1 | `pay-domestic-single` | `PayDomesticSingleViewModel` | loading, content, content_no_eligible_accounts, submitting, error | Single-route four-step form: Account → Payee → Amount → Review |

### Screen Relationships

Single screen with an internal `step` discriminator. Back from any step after Account is a step
transition (`BackStep` action), not a navigation pop. The route itself is entered from the payments
hub and exits to `payment-consent` (mid-flow), then resumes and exits to `payment-status`.

---

## 3. State Model

### PayDomesticSingleViewModel

#### State: `PayDomesticSingleUiState`

The sealed state hierarchy has four top-level variants with an inner `step` on Content:

| Variant | Inner discriminator | Purpose |
|---|---|---|
| `Loading` | — | Fetching accounts + beneficiaries on mount |
| `Content(step: PaymentStep)` | `Account \| Payee \| Amount \| Review` | Active form, step-by-step |
| `Submitting(stage: SubmittingStage)` | `StagingConsent \| AwaitingAuthorisation \| ConfirmingFunds \| SubmittingPayment` | In-flight API call |
| `Error(type: PaymentErrorType)` | — | Terminal error surface |

#### Content State Fields

| Field | Type | Default | Nullable | Purpose |
|---|---|---|---|---|
| `step` | `PaymentStep` | `PaymentStep.Account` | No | Current form step |
| `eligibleDebtorAccounts` | `List<AccountSummary>` | `emptyList()` | No | SortCodeAccountNumber accounts only |
| `hiddenAccountCount` | `Int` | `0` | No | Count of accounts excluded from picker |
| `debtorAccountId` | `String` | `""` | Yes | Selected funding account ID |
| `beneficiaries` | `List<BeneficiarySummary>` | `emptyList()` | No | Eligible payees (SortCode scheme only) |
| `creditor` | `BeneficiarySelection?` | `null` | Yes | Selected or manually-entered payee |
| `manualEntryVisible` | `Boolean` | `false` | No | Whether manual sort-code / account-number fields are shown |
| `sortCodeInput` | `String` | `""` | No | Raw sort-code input (stripped to 6 digits before wire) |
| `accountNumberInput` | `String` | `""` | No | Raw account-number input (8 digits) |
| `payeeNameInput` | `String` | `""` | No | CreditorAccount.Name — mandatory on this rail |
| `amountMinorUnits` | `Long` | `0L` | No | Payment amount in pence; converted to major-unit string at OBIE boundary |
| `amountProblem` | `AmountProblem?` | `null` | Yes | Inline validation: NotANumber, NotPositive, ExceedsAvailableBalance |
| `referenceInput` | `String` | `""` | No | Unstructured remittance reference (≤35 chars; omitted if blank) |
| `feeLabel` | `String?` | `null` | Yes | Populated from Charges[] after staging; null before consent exists |
| `idempotencyKey` | `String` | `""` | No | Generated once, reused for stage + submit + retries |
| `stagedConsentId` | `String?` | `null` | Yes | From POST /domestic-payment-consents response |
| `authorisedInitiation` | `DomesticInitiation?` | `null` | Yes | Parsed from authorised consent; used for submit echo |

#### State Defaults (for /kmp-viewmodel-gen)

```kotlin
val initial = PayDomesticSingleUiState.Loading
// After load:
val initialContent = PayDomesticSingleUiState.Content(
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
  feeLabel = null,
  idempotencyKey = "",
  stagedConsentId = null,
  authorisedInitiation = null,
)
```

#### Screen State Enum: `PaymentStep`

```kotlin
enum class PaymentStep { Account, Payee, Amount, Review }
```

#### Submitting Stage Enum: `SubmittingStage`

```kotlin
enum class SubmittingStage { StagingConsent, AwaitingAuthorisation, ConfirmingFunds, SubmittingPayment }
```

#### Amount Problem Enum: `AmountProblem`

```kotlin
sealed interface AmountProblem {
  data object NotANumber : AmountProblem
  data object NotPositive : AmountProblem
  data object ExceedsAvailableBalance : AmountProblem
}
```

#### Error Types: `PaymentErrorType`

| Type | Retry | Display | Recovery | Message Key |
|---|---|---|---|---|
| `SignatureMissing` | No | error_panel | Support reference — not user-recoverable | `strings.error.payment.signature_missing` |
| `ConsentNotAuthorised` | Yes | error_panel + Re-authorise CTA | Re-authorise CTA restarts app-to-app leg | `strings.error.payment.consent_not_authorised` |
| `InitiationMismatch` | No | error_panel | Not user-recoverable; re-read authorised consent and resubmit | `strings.error.payment.initiation_mismatch` |
| `IneligibleAccount` | No | error_panel | Return to account step (should be unreachable) | `strings.error.payment.ineligible_account` |
| `InsufficientFunds` | No | error_panel | Return to amount step; payment not submitted | `strings.error.payment.insufficient_funds` |
| `ConsentRevoked` | No | error_panel + View Consents CTA | Navigate to consent-list | `strings.error.payment.consent_revoked` |
| `TokenExpired` | Yes | error_panel | Retry after token refresh | `strings.error.payment.token_expired` |
| `NetworkError` | Yes | error_panel | Retry — idempotency key is reused, safe | `strings.error.payment.network_error` |

#### Events: `PayDomesticSingleEvent`

| Event | Params | Trigger |
|---|---|---|
| `NavigateToPaymentConsent` | `consentId: String, paymentFamily: String` | After 201 on POST /domestic-payment-consents |
| `NavigateToPaymentStatus` | `paymentId: String, paymentFamily: String` | After 201 on POST /domestic-payments |

#### Actions: `PayDomesticSingleAction`

| Action | Params | User Trigger |
|---|---|---|
| `LoadPaymentSources` | — | On mount |
| `SelectDebtorAccount` | `accountId: String` | Tap account row in debtor_account_list (Step 1) |
| `ShowManualCreditorEntry` | — | Tap enter_manually_button (Step 2) |
| `SelectCreditor` | `selection: BeneficiarySelection` | Tap beneficiary row in beneficiary_list (Step 2) |
| `EnterAmount` | `rawInput: String` | Keystroke in amount_field (Step 3) |
| `EnterReference` | `text: String` | Keystroke in reference_field (Step 3) |
| `ReviewPayment` | — | Advance from Amount step |
| `ConfirmAndStageConsent` | — | Tap confirm_button (Step 4 / Review) |
| `ConfirmFunds` | `consentId: String` | Auto-triggered after payment-consent returns AUTH |
| `SubmitPayment` | `consentId: String` | Auto-triggered after funds confirm Available |
| `RetrySubmit` | — | Tap Retry on error state when error.type ∈ {NetworkError, TokenExpired} |
| `BackStep` | — | Tap system Back / navigation_icon while on Step 2/3/4 |
| `CancelPayment` | — | Tap Cancel or Back on Step 1 |

#### DI (Constructor Injection)

- `AccountsOverviewRepository` — supplies accounts list for debtor picker
- `BeneficiariesRepository` — supplies beneficiaries list for payee picker
- `PaymentInitiationRepository` — stage consent, funds confirmation, submit payment

---

## 4. Navigation

### Entry Points

| Source | Trigger | Params |
|---|---|---|
| `payments` hub | Tap "Domestic single" tile | none |

### Outgoing Navigation

| Target | Event | Origin Component | Param Map | Condition |
|---|---|---|---|---|
| `payment-consent` | `NavigateToPaymentConsent` | `confirm_button` (indirect, via ViewModel) | `consentId`, `paymentFamily="domestic-payment"` | 201 on POST /domestic-payment-consents |
| `payment-status` | `NavigateToPaymentStatus` | Auto (ViewModel, after submit) | `paymentId`, `paymentFamily="domestic-payment"` | 201 on POST /domestic-payments |
| `payments` | Cancel / BackStep on Account | `navigation_icon` / system Back | none | User cancels or backs from Step 1 |

### Route Definition

- **Route**: `PayDomesticSingleRoute`
- **Params**: none (entered from payments hub with no deep-link payload)
- **Deep Link**: none declared

### Nav Params Mirror

| Target | Param | Type | Required | Source |
|---|---|---|---|---|
| `payment-consent` | `consentId` | `String` | Yes | `stagedConsent.Data.ConsentId` |
| `payment-consent` | `paymentFamily` | `String` | Yes | Hard-coded `"domestic-payment"` |
| `payment-status` | `paymentId` | `String` | Yes | `submit.Data.DomesticPaymentId` |
| `payment-status` | `paymentFamily` | `String` | Yes | Hard-coded `"domestic-payment"` |

### Nav Origins

| Component | Action | Target | Params Resolved From |
|---|---|---|---|
| `confirm_button` | `ConfirmAndStageConsent` | `payment-consent` | `stagedConsent.Data.ConsentId` |
| `navigation_icon` / Back on Account | `CancelPayment` | `payments` | — |
| Auto (ViewModel) after funds check + submit | `SubmitPayment` | `payment-status` | `payment.Data.DomesticPaymentId` |

---

## 5. API Dependencies

| # | Operation ID | Endpoint | Method | Auth | Funds Conf. | Cache | Offline |
|---|---|---|---|---|---|---|---|
| 1 | `stage_domestic_payment_consent` | `/obie/open-banking/v4.0/pisp/domestic-payment-consents` | POST | client_credentials | No | none | error |
| 2 | `get_domestic_payment_consent_status` | `/obie/open-banking/v4.0/pisp/domestic-payment-consents/{ConsentId}` | GET | client_credentials | No | none | error |
| 3 | `funds_confirmation` | `/obie/open-banking/v4.0/pisp/domestic-payment-consents/{ConsentId}/funds-confirmation` | GET | psu_authorization_code | Yes | none | error |
| 4 | `submit_domestic_payment` | `/obie/open-banking/v4.0/pisp/domestic-payments` | POST | psu_authorization_code | No | none | error |
| 5 | `get_domestic_payment_status` | `/obie/open-banking/v4.0/pisp/domestic-payments/{DomesticPaymentId}` | GET | client_credentials | No | none | error |

Resource host: `https://secure.sandbox.ob.hsbc.co.uk`
Authorize host (browser leg only): `https://sandbox.ob.hsbc.co.uk/obie/open-banking/v1.1/oauth2/authorize`

### Error Matrix

| Endpoint | Code | When | Retry | Recovery UI |
|---|---|---|---|---|
| stage_consent | U019 | x-jws-signature missing or invalid | No | Support reference; not user-recoverable |
| stage_consent | U002 | Invalid field (e.g. TPP-named Global Money debtor) | No | Return to account step |
| stage_consent | U004 | CreditorAccount.Name missing | No | Return to payee step — should be blocked by client-side validation |
| stage_consent | U027 | Unsupported scheme (PAN debtor or IBAN/PAN creditor) | No | Should be unreachable — picker prevents it |
| stage_consent | 401 | Token expired | Yes | Refresh token |
| submit_payment | U009 | Consent not in Authorised status | Yes | Re-authorise CTA |
| submit_payment | U008 | Submitted Initiation does not match authorised consent | No | Re-read authorised consent and resubmit |
| submit_payment | U019 | x-jws-signature missing | No | Support reference |
| submit_payment | 403 | Consent revoked | No | View Consents CTA → consent-list |
| funds_confirmation | FundsAvailable=false | Insufficient balance | No | Return to amount step |
| Any | IOException/timeout | Network failure | Yes | Retry (idempotency key reused — safe) |

### Endpoint Details

#### `stage_domestic_payment_consent` (POST)

Stages a domestic-payment-consent. Requires client-credentials token with payments scope plus
x-jws-signature (PS256, detached, b64:false, crit=[iat,iss,tan]) and a stable x-idempotency-key.

**Key invariants**:
- `CreditorAccount.Name` is MANDATORY — omitting it returns U004.
- `DebtorAccount` is OPTIONAL. Omitting it lets the PSU pick at the bank (only way Global Money
  can fund a payment). When provided, must be `UK.OBIE.SortCodeAccountNumber`.
- `RemittanceInformation.Structured`, if sent, MUST be a JSON ARRAY — a bare object returns U002.
- Do NOT include a `Creditor` party block unless a complete postal address with BuildingNumber
  is available. A partial block returns U004 at BuildingNumber.
- `Risk.PaymentContextCode` MUST be `TransferToThirdParty` or `TransferToSelf`. Merchant codes
  are forbidden in this consumer context.
- Returns `Charges[]` at staging: observed `0.05 GBP UK.OBIE.CHAPSOut` on all 14 domestic consents.
- `ConsentId` values are short sequential integers-as-strings (e.g. `"45116"`). Never log or
  surface them — treat as bearer-adjacent.
- `StatusUpdateDateTime` does NOT advance on AWAU→AUTH. Poll `Data.Status` only.

#### `get_domestic_payment_consent_status` (GET)

Polls consent status. Status ladder: `AWAU → AUTH → COND`. Submit is gated on `AUTH`. A
non-Authorised submit returns 400 U009.

#### `funds_confirmation` (GET)

Confirms funds on the PSU token. A PISP consent has one fixed amount, so no body is sent (unlike
VRP which uses POST). On `FundsAvailable=false`, block submit and return to Amount step.

#### `submit_domestic_payment` (POST)

Submits on the PSU token. Echo the `Initiation` object parsed from the AUTHORISED consent (not
the locally staged copy — when DebtorAccount was omitted, the bank writes the PSU's chosen
account into it). The server normalises key order on every echo; field-for-field equality is
required, not byte-for-byte. Reuse the same `x-idempotency-key` as the stage call. Returns
`DomesticPaymentId` with status `ACSP` (AcceptedSettlementInProcess — not settled, never render
as "sent").

#### `get_domestic_payment_status` (GET)

Polls resource status on client-credentials token. Status ladder: `ACSP → ACCC`. `ACCC` is the
terminal success state. All seven corpus payments ultimately reached ACCC after a settlement delay.

---

## 6. Design Tokens Used

| Token | Role / Value (light) | Used By |
|---|---|---|
| `colors.primary` | `#266489` | confirm_button background, step_indicator active |
| `colors.onPrimary` | `#FFFFFF` | confirm_button label |
| `colors.surface` | `#F7F9FF` | Screen background, list_item background |
| `colors.onSurface` | `#181C20` | Primary text in account/beneficiary rows |
| `colors.onSurfaceVariant` | `#41474D` | ineligible_accounts_note, field labels, helper text |
| `colors.error` | `#BA1A1A` | amount_error text, form.field.outline_error |
| `colors.outline` | `#72787E` | text_field default outline |
| `colors.surfaceContainer` | `#EBEEF3` | review_card container |
| `radius.sm` | `8dp` | text_field corner radius |
| `radius.md` | `12dp` | review_card corner radius |
| `radius.full` | `9999dp` | confirm_button pill shape |
| `form.field.min_height_dp` | `56dp` | sort_code_field, account_number_field, payee_name_field, amount_field, reference_field |
| `form.amount_field.typography` | `headlineSmall` | amount_field display scale |
| `form.amount_field.font` | `Roboto Mono` | amount_field — digits must not reflow |
| `typography.bodySmall` | 12sp Roboto | ineligible_accounts_note, amount_error, field helper text |
| `typography.bodyLarge` | 16sp Roboto | Debtor/beneficiary list primary text |
| `semantic.money.debit.role` | `error` | Debit amounts in review_card |
| `semantic.payment_disposition.in_progress` | `secondary` container | submitting_indicator chip |
| `touch_targets.comfortable` | `48dp` | All interactive list items and buttons |

---

## 7. Testing

| ID | Scenario | Priority | Expected Test File |
|---|---|---|---|
| TC-PDS-001 | Happy path: stage → AUTH → funds OK → submit → ACCC | P0 | `PayDomesticSingleViewModelTest#test_TC_PDS_001_happy_path` |
| TC-PDS-002 | No eligible accounts: credit-card-only PSU sees no_eligible_accounts state | P0 | `PayDomesticSingleViewModelTest#test_TC_PDS_002_no_eligible_accounts` |
| TC-PDS-003 | Debtor picker excludes PAN accounts (U027 prevented) | P0 | `PayDomesticSingleViewModelTest#test_TC_PDS_003_debtor_eligibility_filter` |
| TC-PDS-004 | Creditor picker excludes PAN and IBAN (U027 prevented) | P0 | `PayDomesticSingleViewModelTest#test_TC_PDS_004_creditor_eligibility_filter` |
| TC-PDS-005 | Manual payee entry: CreditorAccount.Name required | P0 | `PayDomesticSingleViewModelTest#test_TC_PDS_005_payee_name_mandatory` |
| TC-PDS-006 | Submit echoes Initiation from authorised consent, not staged copy | P0 | `PayDomesticSingleViewModelTest#test_TC_PDS_006_echo_from_authorised` |
| TC-PDS-007 | U009 on submit triggers Re-authorise CTA | P0 | `PayDomesticSingleViewModelTest#test_TC_PDS_007_u009_reauth` |
| TC-PDS-008 | Idempotency key reused across stage, submit, and all retries | P0 | `PayDomesticSingleViewModelTest#test_TC_PDS_008_idempotency_key_stable` |
| TC-PDS-009 | Amount stored as minor units, converted to major-unit string at wire | P0 | `PayDomesticSingleViewModelTest#test_TC_PDS_009_amount_precision` |
| TC-PDS-010 | InsufficientFunds returns to Amount step | P1 | `PayDomesticSingleViewModelTest#test_TC_PDS_010_insufficient_funds` |
| TC-PDS-011 | CreditorAccount.Name client-side validation blocks advance | P1 | `PayDomesticSingleUiTest#test_TC_PDS_011_payee_name_validation` |
| TC-PDS-012 | Amount client-side validation: NotANumber / NotPositive | P1 | `PayDomesticSingleUiTest#test_TC_PDS_012_amount_validation` |
| TC-PDS-013 | Global Money excluded from debtor picker; note shown | P1 | `PayDomesticSingleViewModelTest#test_TC_PDS_013_global_money_excluded` |
| TC-PDS-014 | error_panel iterates all Errors[] entries, not just [0] | P1 | `PayDomesticSingleViewModelTest#test_TC_PDS_014_error_panel_full_array` |
| TC-PDS-015 | Confirm button unmounts on tap; double-submit impossible | P1 | `PayDomesticSingleUiTest#test_TC_PDS_015_state_transition_unmount` |
| TC-PDS-016 | feeLabel populated from Charges[] after staging, not before | P2 | `PayDomesticSingleViewModelTest#test_TC_PDS_016_fee_after_staging` |

**Coverage Target**: 90%

---

## 8. Edge Cases

| Scenario | Expected Behavior |
|---|---|
| PSU omits DebtorAccount (would let bank choose Global Money) | Not exposed in this form — picker always includes a debtor. DebtorAccount is always sent. |
| Server reorders Initiation keys on echo | Forward parsed object, never re-serialise and string-compare (U008 otherwise). |
| StatusUpdateDateTime unchanged after AUTH | Poll Data.Status, never StatusUpdateDateTime — the timestamp is frozen at consent creation. |
| ConsentId is a short integer (e.g. "45116") | Never log, URL-expose, or include in analytics events — treat as bearer-adjacent. |
| Retry after network failure | Reuse identical idempotency key — the server returns the original result rather than double-charging. |
| Empty referenceInput | Omit RemittanceInformation.Unstructured entirely (do not send `[""]`). |
| Structured remittance reference | Must be a JSON ARRAY of objects — `[{ CreditorReferenceInformation: { Reference: "…" } }]`. Not sent by this form currently but the shape is recorded to prevent rediscovery. |
| Partial Creditor party block | Omit entirely — a block without BuildingNumber returns U004 at that field. |
| ACSP status on submit response | Render as "in progress" (secondaryContainer), NEVER as "sent" or "success". Settlement is asynchronous and may take minutes. |

---

## 9. Feature Flags

(none declared)

---

## 10. Data Flow

| Screen | Trigger | Endpoints | Produces State | Error Paths |
|---|---|---|---|---|
| pay-domestic-single | on_mount (load_payment_sources) | GET /accounts (AISP), GET /accounts/{id}/beneficiaries (AISP) | loading → content or content_no_eligible_accounts or error | 401 → Error(TokenExpired), 403 → Error(ConsentRevoked), IOException → Error(NetworkError) |
| pay-domestic-single | stage_consent (ConfirmAndStageConsent) | POST /domestic-payment-consents | Submitting(StagingConsent) → Submitting(AwaitingAuthorisation) + navigate to payment-consent | U019 → Error(SignatureMissing), U002 → Error(IneligibleAccount), 401 → Error(TokenExpired), IOException → Error(NetworkError) |
| pay-domestic-single | resume_after_authorisation | GET /domestic-payment-consents/{id} (re-read), GET /domestic-payment-consents/{id}/funds-confirmation | Submitting(ConfirmingFunds) | FundsAvailable=false → Error(InsufficientFunds) + return to Amount step |
| pay-domestic-single | submit_payment (SubmitPayment) | POST /domestic-payments | Submitting(SubmittingPayment) → NavigateToPaymentStatus | U009 → Error(ConsentNotAuthorised), U008 → Error(InitiationMismatch), U019 → Error(SignatureMissing), 403 → Error(ConsentRevoked), IOException → Error(NetworkError) |

### Side Effects

| Screen | Trigger | Kind | Target |
|---|---|---|---|
| pay-domestic-single | stage_consent | NavigateToPaymentConsent | payment-consent |
| pay-domestic-single | submit_payment | NavigateToPaymentStatus | payment-status |
| pay-domestic-single | cancel / back on Account | NavigateUp | payments hub |

---

## 11. Referenced Journeys

Resolved against `idea-layer/journeys/*.yaml` — a journey is listed here only when this feature's
screen appears in that journey's `screen_sequence`.

| Journey | Name | Persona | Tier | Where this screen appears |
|---|---|---|---|---|
| `consumer-accounts-payments` | Consumer Accounts & Payments | returning consumer | maximum | Steps 7 and 9 — the debtor-account pick, then amount + reference + review before `payment-consent` |

This is the only rail with journey coverage. The journey walks domestic single only; the other six
payment types are journey-uncovered (see `journeys/INDEX.md` § "Coverage gaps owed").

Two entries previously listed here — `pay-person-now` and `pay-person-now-global-money` — were not
journeys. No file of either name has ever existed under `journeys/`; they were invented at export
time from this feature's own user stories. Removed 2026-08-07. The Global Money / no-eligible-account
path they claimed to cover is a real behaviour, but it is covered by TC-PDS-002 and TC-PDS-013 in §7,
not by any journey.

---

## 12. DTOs Consumed

| DTO | Source | Kind |
|---|---|---|
| `ObPaymentError` | `dtos/ObPaymentError.yaml` | Error envelope (Errors[] array, ErrorCode + Path keyed) |
| `DomesticPaymentConsentRequest` | core/network PISP DTOs | POST /domestic-payment-consents request body |
| `DomesticPaymentConsentResponse` | core/network PISP DTOs | POST/GET consent response (ConsentId, Status, Charges[]) |
| `DomesticFundsConfirmationResponse` | core/network PISP DTOs | GET funds-confirmation (FundsAvailableResult.FundsAvailable) |
| `DomesticPaymentRequest` | core/network PISP DTOs | POST /domestic-payments request body |
| `DomesticPaymentResponse` | core/network PISP DTOs | POST /domestic-payments response (DomesticPaymentId, Status) |

---

## 13. Dependencies

**Tier**: feature (tier 1 — depends on `accounts` and `beneficiaries` data-layer features)

| Dependency | Type | Required | Notes |
|---|---|---|---|
| `accounts` | data_source | Yes | Supplies debtor account list; filtered to SortCodeAccountNumber on screen |
| `beneficiaries` | data_source | Yes | Supplies payee list; same SortCodeAccountNumber filter applies |
| `payment-consent` | child | Yes | Bank authorisation leg (app-to-app); receives consentId + paymentFamily |
| `payment-status` | child | Yes | Settlement polling; receives paymentId + paymentFamily |
| `payments` | parent | Yes | Entry point (hub tile) |
| `de.jensklingenberg.ktorfit:ktorfit-lib:2.x` | library | Yes | REST client for the five PISP endpoints |

**Spec ahead of source**: no Ktorfit service, no Store5 store, no repository, no feature module
exist yet (see `docs.yaml#spec_ahead_of_source`). Verification gates are non-assertable until
`/kmp-implement` delivers the module.
