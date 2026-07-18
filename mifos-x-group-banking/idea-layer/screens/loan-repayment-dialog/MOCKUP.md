# Loan Repayment Dialog — Mockup Summary

**Status**: Content-fresh from `ui.yaml` v4.0 + `demo-data.yaml` v2.1.0
**Project**: mifos-x-group-banking (CommonPurse)
**Feature ID**: `loan-repayment-dialog`
**Device**: Mobile (Android — dialog surface, portrait)
**Regenerated**: 2026-07-18 (rewritten from current sibling YAML to bump mtime)
**Stitch artifacts**: pending re-generation (stitch key absent this run — legacy single-state artifact retained at `mockups/loan-repayment-dialog/stitch/01-loan-repayment-dialog-content/`; DEFERRED until stitch key restored)

## Nav params (entry contract)

- `loanId: Long` (required) — the `m_loan` row being repaid
- `memberId: Long` (required) — the group member acting as payer
- `installmentAmount: Double` (required) — pre-fills the amount field

## State model (`LoanRepaymentDialogViewModel`)

- **State**: `LoanRepaymentDialogState { amount, paymentMethod (default MPESA), referenceNumber, isSubmitting, amountError?, submitError? }`
- **Events**: `Dismiss`, `RepaymentRecorded(loanId)`, `ShowError(message)`
- **Actions**: `OnAmountChanged`, `OnPaymentMethodSelected`, `OnReferenceNumberChanged`, `OnSubmit`, `OnDismiss`
- **DI**: `LoanRepository`, `InputValidator`

## Business logic (kind: `composite`)

Validates the treasurer-entered amount is a positive number within the outstanding balance, resolves paymentMethod to a Fineract `paymentTypeId` (MPESA=1, CASH=2), then POSTs a repayment against `m_loan` via `make_repayment`. `cmp-network-monitor` gates submission offline. The money move is idempotent so a retry after a timeout never double-posts.

- **Library refs**: `cmp-network-monitor`
- **External library refs**: `Store5`, `SQLDelight`

## States covered (3)

| State | Purpose | Key components rendered | Distinguishing bindings |
|---|---|---|---|
| `idle` | Fresh dialog, treasurer entering values | `dialog_title`, `amount_field`, `payment_method_label`, `payment_method_chips`, `reference_number_field`, `dialog_actions_row` | `amount=125.00`, `paymentMethod=MPESA`, `isSubmitting=false`, no errors |
| `submitting` | Record Repayment tapped, awaiting API | Same set as `idle` | `isSubmitting=true` → Record Repayment button shows loading, inputs disabled |
| `error` | Validation or API error surfaced | Adds `submit_error_text` between reference field and actions row | `submitError != null` → red inline text; treasurer corrects and retries |

## Components (interactive surfaces)

- `amount_field` (text-field, `number_decimal`) — `on_change: OnAmountChanged` → transform_state (updates `amount`, clears `amountError`; validator runs inline)
- `payment_method_chips` (single-select) — `chip_mpesa` / `chip_cash`, each `on_click: OnPaymentMethodSelected(method)` → transform_state (pure in-VM; resolves to `paymentTypeId` at submit)
- `reference_number_field` (text-field) — `on_change: OnReferenceNumberChanged` → transform_state (optional, carried as `receiptNumber` on submit)
- `cancel_button` — `on_click: OnDismiss` → navigate (emits `Dismiss`, pops the dialog, discards edits)
- `record_repayment_button` — `on_click: OnSubmit` → call_api `make_repayment` `POST /loans/{loanId}/transactions?command=repayment` (cmp-network-monitor gates; idempotent; emits `RepaymentRecorded` then dismisses on success)

## Demo data (drives previews / stitch)

- **PaymentMethod** (2 values): `MPESA` ("M-Pesa"), `CASH` ("Cash")
- **RepaymentTransactionRequest** (3 samples, rural KES weekly installments 500–1200): mixes MPESA (with `receiptNumber`) and CASH (null `receiptNumber`); Fineract date shape `"18 July 2026"` + `locale=en`, `dateFormat="dd MMMM yyyy"`
- **RepaymentTransactionResponse** (1 sample): `officeId=1`, `clientId=1002`, `loanId=5002`, `resourceId=6002` — aligns with `idle` state 125.00 demo

## i18n coverage

- **en** — full (title, labels, placeholders, cancel, submit, 4 error strings)
- **sw** — dialog + fields + actions (no error strings yet)
- **fr** — dialog + labels + actions (no error strings yet)
- **hi** — dialog + labels + actions (no error strings yet)

## Artifacts

- **Preview HTML** (per state, fresh 2026-07-17):
  - `preview/idle.html`
  - `preview/submitting.html`
  - `preview/error.html`
- **Prompt files** (per state, for future stitch regen):
  - `prompts/idle.md`
  - `prompts/submitting.md`
  - `prompts/error.md`
- **Stitch mockup** (LEGACY, single-state — needs regen against current 3-state model when stitch key restored):
  - `../../mockups/loan-repayment-dialog/stitch/01-loan-repayment-dialog-content/code.html`
  - `../../mockups/loan-repayment-dialog/stitch/01-loan-repayment-dialog-content/screen.png`

## Regeneration TODO (when stitch is available)

Run `/idea-render-mockup --feature loan-repayment-dialog` to emit one stitch state per `states[]` entry (`idle`, `submitting`, `error`), replacing the single-state legacy artifact.
