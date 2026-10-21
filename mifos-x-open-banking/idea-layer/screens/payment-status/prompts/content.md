# Payment Status — Content State Prompt

> Feature: payment-status · State: content · Design system: Open Banking — Trust Blue (M3, #266489)
> Quoted strings are VERBATIM from `_strings/strings.yaml` unless marked UNSOURCED.
> The four chip LABELS and all summary row LABELS are UNSOURCED — no keys exist. Render them
> as visibly provisional; do not present them as final copy.

## Shell

Top app bar: `back_button` (arrow_back), title "Payment status". Bottom nav visible, Pay active.
Scrollable column, padding `spacing/md`, gap `spacing/md`.

## Four disposition sub-variants — all four as named frames

Tree identical; only chip fill/icon/label, note, and button set change. Chip: `radius/full`,
padding `spacing/sm` × `spacing/md`, icon 24dp Outlined.

### A — in_progress (ACSP, AWOP, PDNG, unrecognised → fail-open)
- chip `semantic.payment_disposition.in_progress.container`/`…on_container`, icon `schedule`
- label must NOT read "sent", "paid" or "complete" — ACSP means accepted, not settled
- in_progress_note (bodyMedium, `onSurfaceVariant`)
- refresh_button (tonal, fill × 48dp, `secondaryContainer`)

### B — terminal_success (ACCC, ACSC + v3.1 long forms)
- chip `primaryContainer`/`onPrimaryContainer`, icon `check_circle`. No note, no buttons.

### C — terminal_failure (RJCT, BLCK + v3.1 long forms)
- chip `errorContainer`/`onErrorContainer`, icon `error`
- Forbidden here: "invalid", "your account/card", any wording implying customer error.
- new_payment_button (filled, `primary`/`onPrimary`, fill × 48dp) — a NEW instruction, not a
  resubmit. No refresh_button; a terminal status cannot change.

### D — instruction_established (INCO; the four deferred families)
- chip `surfaceVariant`/`onSurfaceVariant`, icon `event_repeat`. Hue-less by design.
- FORBIDDEN icons: `check_circle` (claims money moved), `schedule` (claims motion now).
- Forbidden label substrings: paid, sent, complete, completed, successful, past-tense amount.
- instruction_established_note. No buttons. Polling stopped — INCO is a resting status.

## payment_summary (Card)

`surfaceContainerLow`, radius `radius/md`, elevation `elevation/level1`, padding `spacing/md`,
row gap `spacing/sm`. Row = label left (bodySmall `onSurfaceVariant`) / value right (bodyMedium
`onSurface`; amount titleMedium mono).

Rows: Amount `content.amountLabel` · To `content.creditorName` · From
`content.debtorAccountLabel` · Reference `content.referenceLabel` (hidden when null) ·
Submitted `content.submittedAtLabel`. On deferred rails the amount is the FIRST payment
(`FirstPaymentAmount`) and Frequency / First payment / Final payment rows are added; no
Reference row (U005). Never render `ExpectedExecutionDateTime`, `ExpectedSettlementDateTime`
or `CutOffDateTime` — they equal `CreationDateTime` on deferred families.

## Accessibility

chip = its visible label · summary `summary_a11y` · refresh `refresh_a11y` · new payment
`new_payment_a11y`. All interactive: min 48dp. Focus: back → chip → summary → note → button.

## Copy index — verbatim from `_strings/strings.yaml`

| Key | Value |
|---|---|
| `payment_status.screen_title` | "Payment status" |
| `payment_status.back_label` | "Back" |
| `payment_status.summary_a11y` | "Payment details" |
| `payment_status.in_progress_note` | "Your bank has accepted this payment. The money has not left your account yet." |
| `payment_status.instruction_established_note` | "This instruction is set up with your bank. No payment has been made yet — the first one goes out on its due date." |
| `payment_status.refresh` | "Refresh" |
| `payment_status.refresh_a11y` | "Check the payment status again" |
| `payment_status.new_payment` | "Make a new payment" |
| `payment_status.new_payment_a11y` | "Start a new payment" |

**NO KEY EXISTS** for: the four chip labels, the payment_summary row labels, or a per-rail
variant of `instruction_established_note` (the catalogue has one value covering both the
standing-order and scheduled cases). Do not invent them.
