# Loan Mark Defaulted Dialog — Stitch Mockup

**Status**: Generated
**Project**: CommonPurse (mifos-x-group-banking)
**Stitch Project ID**: `2628966868931366090`
**Screen ID**: `82e538c1f29f418b8791477120067b9d`
**Design System**: CommonPurse-v3 (`assets/17261554270924114992`)
**Device**: Mobile (Android)
**Generated**: 2026-07-18
**Sources**: `ui.yaml` (2026-07-17), `demo-data.yaml` (2026-07-18)

## Summary

Destructive confirmation dialog shown to the chairperson when they tap "Mark Defaulted"
on the loan-detail screen. Displays an irreversible warning with the member name
and loan amount. Two actions: **Cancel** (dismiss) and **Mark Defaulted**
(red, calls Fineract write-off endpoint via `LoanRepository.markDefaulted(loanId)`).
On success, dismisses and emits `LoanMarkedDefaulted` to the parent loan-detail screen.

Business kind: `crud` — POST `/loans/{loanId}/transactions?command=writeoff` (irreversible
mutation on `m_loan`). Connectivity is checked via `cmp-network-monitor` before firing
(no offline queue for this destructive action); on success the Store5/SQLDelight loan
cache is refreshed.

## Preview

View in Stitch: `projects/2628966868931366090/screens/82e538c1f29f418b8791477120067b9d`

## States Covered

- `idle` — populated demo data (member Peter Otieno, KES 1,500 overdue loan; Cancel + Mark Defaulted actions)
- `submitting` — Mark Defaulted button shows loading indicator; both buttons disabled
- `error` — API error text rendered between warning body and action row

## Nav Params

- `loanId: Long` (required)
- `memberName: String` (required)
- `loanAmountKes: Double` (required)

## Interactions

- **Cancel** — `OnDismiss`; effect `none` — pure UI dismissal, no persistence.
- **Mark Defaulted** — `OnConfirm` → `write_off_loan`; effect `call_api`; guarded by `cmp-network-monitor`.
  On success: emits `LoanMarkedDefaulted(loanId)` and refreshes loan cache. On failure: sets `submitError`.

## Idle-state demo binding

- `memberName`: "Peter Otieno"
- `loanAmountKes`: 1500
- `isSubmitting`: false
- `submitError`: null

## Artifacts — preview (all states)

- HTML idle:       `preview/idle.html`
- HTML submitting: `preview/submitting.html`
- HTML error:      `preview/error.html`

## Artifacts — stitch (existing — content state only; regeneration deferred)

- HTML: `../../mockups/loan-mark-defaulted-dialog/stitch/01-loan-mark-defaulted-dialog-content/code.html`
- PNG:  `../../mockups/loan-mark-defaulted-dialog/stitch/01-loan-mark-defaulted-dialog-content/screen.png`

_Note: Stitch artifacts date from 2026-05-09 and cover only the single "content" state.
Regeneration for `submitting` + `error` states is deferred (Stitch endpoint probe unavailable in this run — PROBE+DEFER)._
