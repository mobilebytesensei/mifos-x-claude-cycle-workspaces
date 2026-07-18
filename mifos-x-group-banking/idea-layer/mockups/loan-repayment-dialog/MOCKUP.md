# Loan Repayment Dialog — Mockup Specification

**Feature**: loan-repayment-dialog | **Route**: modal — `/groups/{groupId}/loans/{loanId}` (dialog overlay)
**Feature group**: loan-management | **Flow**: loan-management-flow
**Parent screen**: `loan-detail` | **Type**: modal dialog
**Generated from**: `screens/loan-repayment-dialog/ui.yaml`, `screens/loan-repayment-dialog/demo-data.yaml`, `screens/loan-repayment-dialog/flow.yaml`, `screens/loan-repayment-dialog/preview/*.html` (3 states rendered 2026-07-17)
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature loan-repayment-dialog`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — comfortable density, modal-dialog surface
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first · regulated-industry
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — Record Repayment button (filled), selected chip container, focused text field outline
**Accent**: `#FF8F00` (`--accent-700`, amber) — reserved for pooled-fund emphasis (not used on this dialog)
**Container tones**: `primaryContainer` `#C8E6C9` (selected chip fill) · `onPrimaryContainer` `#1B5E20` (selected chip text)
**Surface variant**: `#F5F5F5` (unselected chip background) · `onSurfaceVariant` `#757575` (unselected chip text, labels)
**Error**: `#B71C1C` (`error` — validation copy, error state divider, submit error text)
**Background**: modal `surface` `#FFFFFF` · scrim `rgba(0, 0, 0, 0.32)` over the dimmed loan-detail screen
**Corner radius**: 28dp dialog container · 8dp text fields · 8dp chips · 24dp Record Repayment button (pill) · 4dp Cancel text button
**Elevation**: dialog 24dp (MD3 modal) · button ripple 300ms · chip selection fill 150ms
**Min touch target**: 48dp on every interactive control (text fields, chips, buttons) — treasurer typically operates one-handed on a mid-range Android

---

## Screen: Record Repayment (modal dialog)

### Entry

- From **loan-detail** — treasurer taps the "Record Repayment" primary CTA on an ACTIVE or OVERDUE loan
- Nav params:
  - `loanId: Long` — target `m_loan` row on Fineract
  - `memberId: Long` — group-member the loan belongs to (analytics + audit)
  - `installmentAmount: Double` — current-week installment (pre-fills the amount field)
- Exit paths:
  - **Cancel** → dismiss dialog, pop back to `loan-detail` unchanged
  - **Success** → emit `RepaymentRecorded(loanId)`, dismiss, parent `loan-detail` re-streams the ledger from Store5
  - **Backdrop tap** → same as Cancel (`OnDismiss`)

### Layout (state: `idle`)

```
       (loan-detail dimmed with scrim rgba(0,0,0,0.32))
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒┌───────────────────────────────┐▒▒   dialog surface · corner 28dp
        ▒▒│                               │▒▒   elevation 24dp
        ▒▒│  Record Repayment             │▒▒   dialog_title · titleLarge, onSurface
        ▒▒│                               │▒▒
        ▒▒│  ┌───────────────────────────┐│▒▒   amount_field · outlined, corner 8dp
        ▒▒│  │ Amount (KES)              ││▒▒   label · onSurfaceVariant labelMedium
        ▒▒│  │ 125.00                    ││▒▒   value · titleMedium, Roboto Mono
        ▒▒│  └───────────────────────────┘│▒▒   min touch 48dp · keyboard number_decimal
        ▒▒│                               │▒▒
        ▒▒│  Payment Method               │▒▒   payment_method_label · labelMedium
        ▒▒│                               │▒▒   onSurfaceVariant #757575
        ▒▒│  ┌────────┐  ┌────────┐       │▒▒   payment_method_chips · single-select
        ▒▒│  │M-Pesa* │  │  Cash  │       │▒▒   selected: primaryContainer #C8E6C9
        ▒▒│  └────────┘  └────────┘       │▒▒   unselected: surfaceVariant #F5F5F5
        ▒▒│                               │▒▒   gap 8dp, corner 8dp, min touch 48dp
        ▒▒│  ┌───────────────────────────┐│▒▒   reference_number_field · outlined
        ▒▒│  │ Reference Number (opt.)   ││▒▒   corner 8dp, min touch 48dp
        ▒▒│  │ e.g. QJZ7X9A1BK           ││▒▒   keyboard text · placeholder
        ▒▒│  └───────────────────────────┘│▒▒
        ▒▒│                               │▒▒
        ▒▒│              Cancel   [ Record ]│▒▒   dialog_actions_row · gap 12dp
        ▒▒│                       Repayment │▒▒   Cancel · text button, primary #2E7D32
        ▒▒│                                 │▒▒   Record · filled button, primary bg,
        ▒▒└─────────────────────────────────┘▒   onPrimary text, corner 24dp
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
```

### Demo Data (state: `idle`, from `demo-data.yaml`)

**PaymentMethod enum** (2 values, offline-first — M-Pesa primary, Cash fallback):

| Value | Label   | paymentTypeId | Notes                                     |
|-------|---------|---------------|-------------------------------------------|
| MPESA | M-Pesa  | 1             | Primary — receiptNumber captured          |
| CASH  | Cash    | 2             | Fallback when M-Pesa offline — no receipt |

**Idle-state field bindings**:
- `amount: "125.00"` — pre-filled from `installmentAmount` nav param (weekly installment for member 1002 on loan 5002)
- `paymentMethod: MPESA` — M-Pesa chip selected by default
- `referenceNumber: ""` — empty, ready for the M-Pesa receipt code
- `isSubmitting: false` · `amountError: null` · `submitError: null`

**Representative repayment bodies** (three request seeds, all `transactionDate: "18 July 2026"`, `locale: "en"`, `dateFormat: "dd MMMM yyyy"`):

| # | Amount (KES) | paymentTypeId | receiptNumber   |
|---|--------------|---------------|-----------------|
| 1 | 700.00       | 1 (MPESA)     | `MPE2026071801` |
| 2 | 1,000.00     | 2 (CASH)      | `null`          |
| 3 | 500.00       | 1 (MPESA)     | `MPE2026071802` |

**Representative success response** (member 1002, loan 5002 → treasurer records the 700 KES M-Pesa repayment):

```json
{ "officeId": 1, "clientId": 1002, "loanId": 5002, "resourceId": 6002 }
```

- `resourceId` = the newly-created `m_loan_transaction` id — parent `loan-detail` uses it to highlight the fresh ledger row.
- `officeId: 1` = Kisumu West Branch (matches the `loan-list` seed context).

---

## States

The ui.yaml declares 3 dialog states — `idle`, `submitting`, `error` — each rendered as an HTML preview under `preview/`.

### `idle` (see layout above)

Default state on open. Amount pre-filled from `installmentAmount`, M-Pesa chip selected, reference number empty. `Record Repayment` enabled the moment the amount validates as a positive number ≤ outstanding balance. `InputValidator` runs on every keystroke — invalid entries surface `amountError` inline under the amount field before the user can submit.

### `submitting`

Same layout as `idle`, but every input is disabled and the `Record Repayment` button swaps its label for an MD3 circular progress indicator.

```
        ▒▒┌───────────────────────────────┐▒▒
        ▒▒│  Record Repayment             │▒▒   title unchanged
        ▒▒│                               │▒▒
        ▒▒│  ┌─── Amount (KES) ──────────┐│▒▒   amount_field · disabled tint
        ▒▒│  │ 125.00                    ││▒▒   text muted (--text-secondary)
        ▒▒│  └───────────────────────────┘│▒▒
        ▒▒│                               │▒▒
        ▒▒│  Payment Method               │▒▒
        ▒▒│  ┌────────┐  ┌────────┐       │▒▒   chips inert (pointer-events: none)
        ▒▒│  │M-Pesa* │  │  Cash  │       │▒▒
        ▒▒│  └────────┘  └────────┘       │▒▒
        ▒▒│                               │▒▒
        ▒▒│  ┌─── Reference Number ─────┐ │▒▒   reference_number_field · disabled
        ▒▒│  │                          │ │▒▒
        ▒▒│  └──────────────────────────┘ │▒▒
        ▒▒│                               │▒▒
        ▒▒│              Cancel   [ ⟳   ] │▒▒   filled button shows MD3 ProgressIndicator
        ▒▒│                     recording │▒▒   24dp indicator, onPrimary tint
        ▒▒└───────────────────────────────┘▒▒   Cancel remains enabled to abort
```

- Cancel stays live so the treasurer can back out if the network stalls; abort discards the in-flight request via `cmp-network-monitor`.
- Backdrop taps are suppressed while `isSubmitting == true` (prevents accidental dismissal mid-money-move).
- Progress indicator: MD3 CircularProgressIndicator 24dp, `onPrimary` tint, 1.6s rotation — disabled under `prefers-reduced-motion`.

### `error`

Server rejected the repayment OR validation failed at submission time. All inputs return to enabled, the previous entries are preserved, and the red `submit_error_text` surfaces above the actions row.

```
        ▒▒┌───────────────────────────────┐▒▒
        ▒▒│  Record Repayment             │▒▒
        ▒▒│                               │▒▒
        ▒▒│  ┌─── Amount (KES) ──────────┐│▒▒   amount_field re-enabled
        ▒▒│  │ 125.00                    ││▒▒
        ▒▒│  └───────────────────────────┘│▒▒
        ▒▒│                               │▒▒
        ▒▒│  Payment Method               │▒▒
        ▒▒│  ┌────────┐  ┌────────┐       │▒▒
        ▒▒│  │M-Pesa* │  │  Cash  │       │▒▒
        ▒▒│  └────────┘  └────────┘       │▒▒
        ▒▒│                               │▒▒
        ▒▒│  ┌─── Reference Number ─────┐ │▒▒
        ▒▒│  │ QJZ7X9A1BK               │ │▒▒
        ▒▒│  └──────────────────────────┘ │▒▒
        ▒▒│                               │▒▒
        ▒▒│  ⚠ Could not record repayment │▒▒   submit_error_text · bodySmall, error #B71C1C
        ▒▒│    Please try again.          │▒▒   visible_when: submitError != null
        ▒▒│                               │▒▒
        ▒▒│              Cancel   [ Record ]│▒▒   Record Repayment re-enabled
        ▒▒│                       Repayment │▒▒
        ▒▒└─────────────────────────────────┘▒
```

**Error copy vocabulary** (from ui.yaml `i18n.en`):

- `error_amount_required` — "Please enter a repayment amount." (inline under amount field)
- `error_amount_invalid` — "Amount must be a valid positive number." (inline under amount field)
- `error_amount_exceeds` — "Amount cannot exceed the outstanding balance." (inline under amount field)
- `error_server` — "Could not record repayment. Please try again." (surfaced as `submit_error_text`)

Inline field-level errors set `amountError`; API-level errors set `submitError`. The two error surfaces never render together — a validation failure short-circuits the submit before `make_repayment` is called.

---

## Interaction Patterns

1. **Amount edit** → `OnAmountChanged(value)` (effect: `transform_state`) → `amount` is updated and `amountError` is cleared as the treasurer types. `InputValidator` positive-number check runs on every keystroke so a bad entry surfaces inline before `Record Repayment` becomes enabled.
2. **Payment method select** → `OnPaymentMethodSelected(method)` (effect: `transform_state`) → sets `paymentMethod` to `MPESA` or `CASH`. Pure in-VM state change — no network or persistence side-effect until submit. Selected chip fills with `primaryContainer` (`#C8E6C9`) and text switches to `onPrimaryContainer` (`#1B5E20`).
3. **Reference number edit** → `OnReferenceNumberChanged(value)` (effect: `transform_state`) → updates the optional `referenceNumber`. Carried verbatim into the `make_repayment` `receiptNumber` body field. No network call on change; empty string maps to a `null` receipt on Cash payments.
4. **Record Repayment tap** → `OnSubmit` (effect: `call_api`, external: `make_repayment`) →
   - Re-validate amount (positive number, ≤ outstanding balance).
   - `cmp-network-monitor` blocks submission when offline — instead of failing, the button stays enabled and a snackbar surfaces "No internet connection. Try again when back online."
   - POST `/loans/{loanId}/transactions?command=repayment` with `paymentTypeId` derived from the chip (`MPESA → 1`, `CASH → 2`), `transactionAmount` from the field, `transactionDate: today` (Fineract `dd MMMM yyyy`, locale `en`), and `receiptNumber` from the reference field (`null` if empty AND `paymentTypeId == 2`).
   - Idempotent money move: retry after a timeout MUST NOT double-post (client sends a stable request-id derived from `loanId + transactionDate + amount + receipt`, server dedupes).
   - On success → emit `RepaymentRecorded(loanId)` → dismiss dialog → parent `loan-detail` refreshes.
   - On failure → set `submitError`, transition to `error` state, keep every field intact.
5. **Cancel tap** → `OnDismiss` (effect: `navigate`) → emit `Dismiss`, pop back to `loan-detail`. Discards the entered amount and reference; no analytics side-effect beyond `loan_repayment_dialog_dismissed`.
6. **Backdrop tap** → same as Cancel, unless `isSubmitting == true` (blocked during money move).

---

## Accessibility

- Every input has a labelled role (`role="textbox"`) with `aria-label` sourced from the i18n copy; the payment method group is a `role="radiogroup"` with each chip a `role="radio"` and `aria-checked` mirroring `selectedPaymentMethod`.
- Amount field announces the currency ("Kenyan Shillings") in screen-reader hint text; number-decimal keyboard on Android, `inputmode="decimal"` on web.
- Inline `amountError` messages are `role="alert"` — announced immediately when set.
- `submit_error_text` is `aria-live="polite"` so an error transition doesn't interrupt other announcements.
- Colour never carries the only signal — every error uses red text + explicit copy; every selected chip uses a fill change + `aria-checked`.
- Min touch target 48dp on every interactive control — treasurer typically operates one-handed on a mid-range Android.
- Locales covered by the ui.yaml `i18n` block: English, Swahili (`Rekodi Malipo` / `Ghairi`), French (`Enregistrer un Remboursement` / `Annuler`), Hindi (`पुनर्भुगतान दर्ज करें` / `रद्द करें`).
- Dialog traps focus while open; ESC (web) / hardware back (Android) triggers `OnDismiss`. Focus returns to the "Record Repayment" CTA on `loan-detail` when the dialog closes.

---

## Motion & Feedback

- Dialog enter: MD3 fade + 8dp scale-up over 250ms ease-out.
- Dialog exit: MD3 fade + 8dp scale-down over 200ms ease-in.
- Chip selection: fill transition 150ms.
- Button ripple: MD3 standard 300ms ease-out on tap.
- Text field focus: 2dp outline draw from left to right, 150ms.
- Submitting spinner: 1.6s rotation, disabled under `prefers-reduced-motion`.
- Success snackbar (on the parent `loan-detail` after dismiss): "Repayment recorded — KES {amount} for {memberName}", auto-dismiss 4s.
- Error transition: `submit_error_text` fades in 150ms; no shake / no attention-grab animation (regulated-industry constraint).

---

## Data Flow (ui.yaml `business_logic.kind: composite`)

**External libs**: `Store5`, `SQLDelight`, `Fineract m_loan`
**Internal lib**: `cmp-network-monitor`

Write path (idempotent money move):
- `LoanRepository.recordRepayment(loanId, request)` — Store5 mutation
  - Source of truth: SQLDelight `loans` cache (`outstanding_balance` decremented) + `loan_transactions` cache (new row inserted with the returned `resourceId`)
  - Fetcher: Fineract `POST /loans/{loanId}/transactions?command=repayment` (gated by `cmp-network-monitor`)
  - Request shape: `{ transactionDate, transactionAmount, paymentTypeId, receiptNumber, locale, dateFormat }` per `demo-data.yaml` seeds
  - Response shape: `{ officeId, clientId, loanId, resourceId }` — `resourceId` is the new `m_loan_transaction` id
  - Idempotency: request-id = `sha256(loanId + transactionDate + amount + receipt)` — the same tuple retried returns the original `resourceId`, never a second transaction row
  - Offline: `cmp-network-monitor.isOffline == true` → snackbar surfaces "No internet connection. Try again when back online." — request is NOT queued (money moves are user-consent-per-attempt, not background retryable)
- On success → emit `RepaymentRecorded(loanId)` (LoanRepaymentDialogEvent) → parent `loan-detail` observes the Store5 stream and re-renders the ledger row automatically.
- On failure → surface `error_server` copy in `submit_error_text`; local state (amount, method, reference) is preserved so the treasurer can retry without re-entering.

Read paths (dialog is write-only, but pulls one derived value):
- `outstanding_balance` ← observed once on open from the parent `loan-detail` state (used to cap the amount validator). No fresh network read — the dialog trusts the parent's Store5 snapshot.

---

## Analytics

Events (from `docs.yaml.legacy_metadata.analytics`):

| Trigger | Event name | Params |
|---------|-----------|--------|
| Dialog opened | `loan_repayment_dialog_opened` | `loan_id: Long, installment_amount: Double` |
| Payment method changed | `loan_repayment_payment_method_changed` | `method: String` (`MPESA` / `CASH`) |
| Repayment submitted | `loan_repayment_submitted` | `loan_id: Long, amount: Double, method: String` |
| Repayment succeeded | `loan_repayment_success` | `loan_id: Long` |
| Repayment failed | `loan_repayment_error` | `loan_id: Long, error: String` (redacted — no PII) |
| Dialog dismissed | `loan_repayment_dialog_dismissed` | `loan_id: Long` |

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/loan-repayment-dialog/ui.yaml` |
| API contract | `idea-layer/screens/loan-repayment-dialog/api.yaml` |
| Data flow | `idea-layer/screens/loan-repayment-dialog/data-flow.yaml` |
| Demo data | `idea-layer/screens/loan-repayment-dialog/demo-data.yaml` |
| Flow | `idea-layer/screens/loan-repayment-dialog/flow.yaml` |
| Tests | `idea-layer/screens/loan-repayment-dialog/tests.yaml` |
| Preview HTML (idle) | `idea-layer/screens/loan-repayment-dialog/preview/idle.html` |
| Preview HTML (submitting) | `idea-layer/screens/loan-repayment-dialog/preview/submitting.html` |
| Preview HTML (error) | `idea-layer/screens/loan-repayment-dialog/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/loan-repayment-dialog/prompts/{idle,submitting,error}.md` |
| Stitch mockup (probe deferred) | `idea-layer/mockups/loan-repayment-dialog/stitch/` |
| Feature-group mockup | `idea-layer/mockups/loan-management/MOCKUP.md` (Screen: Repayment dialog section) |
| Parent screen mockup | `idea-layer/mockups/loan-detail/MOCKUP.md` (entry point for this dialog) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from the fresh preview HTML (3/3 states rendered 2026-07-17) + ui.yaml + demo-data.yaml + flow.yaml + design-system tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- The dialog is a **modal overlay** — layout coordinates are relative to the dialog surface, not the parent screen; the scrim + dimmed loan-detail is implicit context.
- The money move is **idempotent by design** — the retry pattern on error state MUST NOT introduce double-posts. This is enforced in `LoanRepository.recordRepayment` via a stable request-id derived from the (loanId, date, amount, receipt) tuple.
- The dialog trusts the parent `loan-detail` for `outstanding_balance` — it does NOT re-fetch the balance on open. If the parent snapshot is stale, validation will still cap the amount at the shown balance and Fineract's own server-side check catches any residual drift.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features loan-repayment-dialog
  ```
- Design conformance verifier: preview HTML mirrors the layouts above; any hand-edit to ui.yaml components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
