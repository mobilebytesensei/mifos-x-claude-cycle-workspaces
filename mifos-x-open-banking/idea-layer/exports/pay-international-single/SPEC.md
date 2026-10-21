# SPEC — Pay Abroad (International Single Payment)

| Field         | Value                                     |
|---------------|-------------------------------------------|
| Feature       | pay-international-single                  |
| Flavor        | consumer                                  |
| Status        | enriched                                  |
| Quality Score | 93                                        |
| ViewModel     | PayInternationalSingleViewModel           |
| Archetype     | form (five-step)                          |
| Rail          | international-single                      |
| Cluster       | payment-initiation                        |
| Inherits from | pay-domestic-single                       |

---

## Overview

International single payment — send money to an overseas IBAN right now. Five steps: funding account
selection, recipient details (IBAN and optional 11-character BIC), amount with separate instructed
and transfer currency pickers, charge-bearer choice, and a review surface before the consent is
staged. Once authorised at the bank the app re-reads the consent, runs funds confirmation, and
submits immediately.

This rail differs from every other payment shape in three ways. First, it is the only shape in the
entire surface that returns **no Charges at any stage** — not at consent creation, not on the
authorised resource, not at ACCC (verified: 0 of 33 consents, 0 of 4 authorised resources). The
screen explains this rather than leaving a blank row. Second, `RemittanceInformation` is refused
with `U005`, so the form has no reference field — the absence is named on the Amount step.  Third,
no exchange rate is available: the endpoint refuses `ExchangeRateInformation` for every `RateType`
value (Indicative, Actual, Agreed), so the bank sets the converted amount and the screen says so.

`BeneficiariesRepository` is deliberately **not** injected. Saved payees carry sort-code
identifiers; this rail refuses a sort-code creditor with `U027` — offering the beneficiary list
would render a picker where every entry fails on submission.

---

## Screens

| ID                       | Name       | ViewModel                       | Archetype |
|--------------------------|------------|---------------------------------|-----------|
| pay-international-single | Pay abroad | PayInternationalSingleViewModel | form      |

**Shell:** top app bar, title `{strings.pay_international_single.title}`, `back` leading icon, no
overflow actions. Bottom navigation visible.

**Step indicator (`step_indicator`):** 5-step horizontal stepper labelled Account · Recipient ·
Amount · Charges · Review. Always visible regardless of the active step.

---

## Components

The form is a single screen screen advancing through five named steps. Component visibility is
controlled by the current step and `uiState`.

| ID                         | Type           | Visible when                            | Purpose |
|----------------------------|----------------|-----------------------------------------|---------|
| step_indicator             | stepper        | always                                  | 5-step progress header |
| debtor_account_list        | list           | step=Account, state=content             | Select the funding sort-code account |
| ineligible_accounts_note   | text           | step=Account, hiddenAccountCount > 0    | Global Money excluded note |
| no_eligible_accounts       | empty_state    | state=content_no_eligible_accounts      | No payable accounts at all |
| iban_field                 | text_field     | step=Recipient                          | IBAN; mod-97 + per-country length |
| payee_name_field           | text_field     | step=Recipient                          | Payee name → CreditorAccount.Name |
| bic_field                  | text_field     | step=Recipient                          | Optional 11-char BIC |
| bic_length_error           | text           | step=Recipient, bic non-blank, len≠11   | Length validation copy |
| amount_field               | text_field     | step=Amount                             | Currency-aware, no ceiling |
| instructed_currency_picker | dropdown       | step=Amount                             | Currency debtor is charged in |
| transfer_currency_picker   | dropdown       | step=Amount                             | Currency creditor receives (mandatory) |
| fx_disclosure              | banner         | step=Amount, currencies differ          | Bank sets the converted amount |
| no_reference_note          | text           | step=Amount                             | Reference not available on this rail |
| charge_bearer_picker       | radio_group    | step=Charges                            | BorneByDebtor / Shared / BorneByCreditor |
| no_charge_note             | text           | step=Charges                            | HSBC quotes no fee on this rail |
| review_card                | summary_card   | step=Review, state=content              | All committed values (no fee row, no reference row) |
| confirm_button             | button         | step=Review, state=content              | Stage consent + hand off |
| submitting_indicator       | progress       | state=Submitting                        | Stage labels |
| error_panel                | error_panel    | state=Error                             | All Errors entries, wire order |

**review_card rows** (no fee row, no reference row — both absent by design):

| Label | Value |
|-------|-------|
| `{strings.payment.review.from}` | `debtorAccountLabel` |
| `{strings.payment.review.to}` | `creditorIbanLabel` |
| `{strings.payment.review.bank}` | `bicLabel` (hidden when bic is blank) |
| `{strings.payment.review.amount}` | `instructedAmountLabel` |
| `{strings.payment.review.arrives_in}` | `transferCurrencyLabel` |
| `{strings.payment.review.charges}` | `chargeBearerLabel` |

---

## States

Initial state: `loading`.

| State                        | Meaning |
|------------------------------|---------|
| loading                      | Fetching eligible debtor accounts |
| content                      | Five-step form active |
| content_no_eligible_accounts | No sort-code accounts available; form cannot proceed |
| submitting                   | StagingConsent → AwaitingAuthorisation → ConfirmingFunds → SubmittingPayment |
| error                        | 400 response, funds not available, or network failure |

---

## State Model

**ViewModel:** `PayInternationalSingleViewModel`

**UiState sealed type:** `PayInternationalSingleUiState`
- `Loading`
- `Content(step: Step)` — step ∈ `Account | Recipient | Amount | Charges | Review`
- `Submitting(stage: SubmitStage)` — stage ∈ `StagingConsent | AwaitingAuthorisation | ConfirmingFunds | SubmittingPayment`
- `Error(type: PaymentErrorType)`

**State fields inside `Content`:**

| Field | Type | Notes |
|-------|------|-------|
| eligibleDebtorAccounts | `List<DebtorAccount>` | SortCodeAccountNumber only; Global Money excluded |
| hiddenAccountCount | `Int` | Drives `ineligible_accounts_note` |
| selectedDebtorAccount | `DebtorAccount?` | Null until Account step complete |
| iban | `String` | Empty until entered; validated mod-97 + per-country length |
| payeeName | `String` | Sent as `CreditorAccount.Name` |
| bic | `String` | Blank or exactly 11 characters |
| bicProblem | `BicProblem?` | `WrongLength` when bic is non-blank and length ≠ 11 |
| amountMinorUnits | `Long` | Held as pence-equivalent; displayed formatted to currency's decimal places |
| instructedCurrency | `String` | ISO 4217 — what the debtor pays in |
| currencyOfTransfer | `String` | ISO 4217 — what the creditor receives; mandatory on the wire |
| chargeBearer | `ChargeBearer?` | `BorneByDebtor \| Shared \| BorneByCreditor`; mandatory |
| stagedConsentId | `String?` | Set after POST 201; never logged, deep-linked or shown |
| idempotencyKey | `String` | Generated once on first attempt; reused on every retry |

**Actions:**

| Action | Signature |
|--------|-----------|
| LoadPaymentSources | `suspend fun loadPaymentSources()` |
| SelectDebtorAccount | `fun selectDebtorAccount(account: DebtorAccount)` |
| EnterIban | `fun enterIban(iban: String)` |
| EnterPayeeName | `fun enterPayeeName(name: String)` |
| EnterBic | `fun enterBic(bic: String)` |
| EnterAmount | `fun enterAmount(raw: String)` |
| SelectInstructedCurrency | `fun selectInstructedCurrency(code: String)` |
| SelectTransferCurrency | `fun selectTransferCurrency(code: String)` |
| SelectChargeBearer | `fun selectChargeBearer(value: ChargeBearer)` |
| ReviewPayment | `fun reviewPayment()` |
| ConfirmAndStageConsent | `suspend fun confirmAndStageConsent()` |
| ConfirmFunds | `suspend fun confirmFunds()` |
| SubmitPayment | `suspend fun submitPayment()` |
| RetrySubmit | `suspend fun retrySubmit()` — reuses idempotency key |
| BackStep | `fun backStep()` |
| CancelPayment | `fun cancelPayment()` |

**Events:** `NavigateToPaymentConsent(consentId, paymentFamily)`, `NavigateToPaymentStatus(paymentId, paymentFamily)`

**DI:** `AccountsOverviewRepository`, `PaymentInitiationRepository`

Note: `BeneficiariesRepository` is not injected. Sort-code payees fail with `U027` on this rail.

---

## Navigation

| From                     | To                | Trigger                                       | Params |
|--------------------------|-------------------|-----------------------------------------------|--------|
| payments hub             | pay-international-single | Tap the International single tile      | — |
| pay-international-single | payment-consent   | Review confirmed, consent staged 201          | `consentId`, `paymentFamily="international-payment"` |
| payment-consent          | pay-international-single | Consent reaches AUTH — resume          | `consentId` |
| payment-consent          | pay-international-single | Consent reaches RJCT — PSU denied      | `consentId` |
| pay-international-single | payment-status    | Submit returns 201                            | `paymentId`, `paymentFamily="international-payment"` |
| pay-international-single | payments hub      | Back from Account step, or Cancel             | — |

A `RJCT` consent is a real observed terminal state (consent 45121). The app returns to the form
with a rejection message and a fresh-payment CTA. A rejected consent cannot be reused.

---

## API Endpoints

| ID | Method | Path | Auth |
|----|--------|------|------|
| stage_international_payment_consent | POST | `/obie/open-banking/v4.0/pisp/international-payment-consents` | client_credentials_payments_scope |
| get_international_payment_consent_status | GET | `/obie/open-banking/v4.0/pisp/international-payment-consents/{ConsentId}` | client_credentials_payments_scope |
| funds_confirmation | GET | `/obie/open-banking/v4.0/pisp/international-payment-consents/{ConsentId}/funds-confirmation` | psu_authorization_code |
| submit_international_payment | POST | `/obie/open-banking/v4.0/pisp/international-payments` | psu_authorization_code |
| get_international_payment_status | GET | `/obie/open-banking/v4.0/pisp/international-payments/{InternationalPaymentId}` | client_credentials_payments_scope |

Full request / response shapes and the error contract: `API.md`.

**Critical wire constraints:**
- `CurrencyOfTransfer` mandatory — `U004` if omitted
- `ChargeBearer` mandatory — `U004 @ Data.Initiation.ChargeBearer` if omitted (R18-B01/B02)
- `RemittanceInformation` refused — `U005` if sent
- `CreditorAccount.SchemeName` must be `UK.OBIE.IBAN` — `U027` for any other scheme
- `CreditorAgent` optional, but if sent must carry an 11-character `Identification` — 8-char BICs return `U002 Invalid Bank Code` (the check is length-only, not BIC-country vs IBAN-country)
- `Charges`, `CutOffDateTime`, `ExpectedExecutionDateTime`, `ExpectedSettlementDateTime` are **absent** (not empty) from every 200/201 — parse as nullable
- `ExchangeRateInformation` refused for every `RateType` value — no rate to show before authorisation

---

## Design Tokens

Design system: **Open Banking — Trust Blue** — Material 3, seed `#266489`, Roboto / Roboto Mono.
Full values in `design-system/design-tokens.yaml`. Brand spec in `design-system/DESIGN.md`.

| Purpose | Token | Light value |
|---------|-------|-------------|
| Primary action / confirm button | `colors.light.primary` | `#266489` |
| Surface background | `colors.light.surface` | `#F7F9FF` |
| Card container | `colors.light.surfaceContainer` | `#EBEEF3` |
| Secondary / helper text | `colors.light.onSurfaceVariant` | `#41474D` |
| Error text and debit amounts | `colors.light.error` | `#BA1A1A` |
| Text field radius | `radius.sm` | 8 dp |
| Card radius | `radius.md` | 12 dp |
| Confirm button radius | `radius.full` | 9999 dp |
| Amount font | `typography.font_family.mono` | Roboto Mono |
| Amount type scale | `form.amount_field.typography` | headlineSmall |
| Screen padding | `spacing.md` | 16 dp |
| Touch target floor | `touch_targets.comfortable` | 48 dp |

The confirm button stays `primary`, not `error`. Red is reserved for genuine failures; the weight
of an irreversible action comes from the review surface and the amount in the button label
("Send £5.00"), not from alarm colour.

---

## Referenced Journeys

Resolved against `idea-layer/journeys/*.yaml` — a journey is listed here only when this feature's
screen appears in that journey's `screen_sequence`.

| Journey | Name | Persona | Tier | Where this screen appears |
|---|---|---|---|---|
| `consumer-insights-utilities` | Consumer Insights & Utilities | returning consumer | medium | Step 3 — "enter the IBAN, amount and transfer currency", reached from the `payments` hub |

The journey's success signal for this step is worth reading before implementing the Amount step: the
form must accept an IBAN creditor and a transfer currency distinct from the instructed one, **and
state that the bank sets the final converted amount rather than showing a rate**. That is the
`fx_disclosure` banner, and the journey treats it as the pass condition, not as decoration.

Two of the journey's failure modes recover to this screen: an IBAN that fails its local checksum,
and an 8-character BIC pasted from a bank directory (blocked locally, because HSBC returns
`U002 Invalid Bank Code` the PSU cannot act on).

This journey replaced an older `fx-rates → send-money` pair on 2026-08-06. Its success metric is now
`payments_hub_opened → intl_type_tile_tapped`; the previous metric started on the `fx-rates` screen,
which has no OBIE data source.

This is the only international rail with journey coverage. `pay-international-scheduled` and
`pay-international-standing-order` are journey-uncovered.

---

<!-- Generated 2026-08-07 by /idea-feature-export from screens/pay-international-single/{ui,api,flow,docs,data-flow}.yaml. -->
