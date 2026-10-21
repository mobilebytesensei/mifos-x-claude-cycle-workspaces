# State: paying — pay-vrp-mandate-detail

> COPY SOURCE — every string is the verbatim `_strings/strings.yaml` value for the key cited
> inline. ⚠ STILL UNSOURCED — no catalogue key AND no component in `ui.yaml`: the sheet CTA
> ("Pay £5.00"), the field helper texts, and the transient "Checking funds…" step.

Compose the variable payment detail screen in the Paying state: amount sheet open, PSU about to
pay under consent 45223.

## Shell

TopAppBar: title "Variable payment" `{vrp.detail_title}` · titleLarge · onSurface ·
navigationIcon=arrow_back · container=surface. No bottom nav.

### Summary card (behind the sheet)

ElevatedCard: radius=12dp · surfaceContainer · elevation=1dp · full width · padding=16dp.
Rows (vertical, 8dp). Labels bodyMedium · onSurfaceVariant; values bodyLarge · onSurface.

1. "To" `{vrp.review.to}` / "test user · 401800 00133787"
2. "Most per payment" `{vrp.review.max_per_payment}` / "£10.00" (Roboto Mono)
3. "Status" `{vrp.detail.status}` / MandateHealthChip(active · primaryContainer · autorenew ·
   "Active" `{vrp.health.active}`)

### Limits and spending

Section label: "Limits and spending" `{vrp.detail.headroom}` · titleMedium · onSurface.
Deliberately NOT "What's left" — the figure is this app's own tally.

HeadroomCard (ElevatedCard: radius=12dp · surfaceContainer · elevation=1dp · padding=16dp):
- "Weekly limit" (bodyMedium · onSurface) / "£50.00 limit · £10.00 counted from payments made in
  this app" (bodySmall · onSurfaceVariant)
- LinearProgressIndicator: progress=0.20 · primary / primaryContainer · height=4dp

Below it, Icon(info · 16dp · onSurfaceVariant) + Text (bodySmall · onSurfaceVariant):
"Your first period may allow less than this, because it starts partway through. HSBC works that out and does not share the figure, so this app cannot show how much is left in it."
`{vrp.pro_rating_notice}`

## Payment sheet (BottomSheet)

ModalBottomSheet: top radius=28dp · surfaceContainerHigh · elevation=3dp. Handle: 32×4dp rounded
rect · outline · centred · margin-bottom=16dp. Interior: vertical · 16dp · padding=24dp.

### Amount field

Label: "Amount" `{vrp.payment_amount_label}` · titleMedium · onSurface

AmountField: prefix "£" (non-editable) + input, both Roboto Mono · headlineSmall · onSurface.
Value "5.00". Stroke=outline · radius=8dp · fill=surfaceContainerLow · focus stroke=primary 2dp ·
min height 64dp.

Helper: "Maximum £10.00 per payment" · bodySmall · onSurfaceVariant — the only figure the bank
publishes. No remaining-balance figure here.

Validation: ≤ MaximumIndividualAmount (£10.00) AND ≤ the headroom this app has counted on every
periodic limit; local check before any API call. Error: stroke=error · helper=error.

### Reference field

OutlinedTextField: label "Reference (optional)" `{vrp.payment_reference_label}` · bodyLarge ·
stroke=outline · radius=8dp · fill=surfaceContainerLow. Value "VRP-5.00".

### CTA

FilledButton: label="Pay £5.00" · radius=full · primary / onPrimary · labelLarge · full width.
Action: ConfirmFundsAndPay. On tap: disable, CircularProgressIndicator(18dp · onPrimary) in the
label. POST funds-confirmation (PSU token) → GET consent → POST /domestic-vrps.

## Design constraints

- CTA names the amount ("Pay £5.00"), not "Confirm". Money moves now on this rail.
- Reference is per-payment → Data.Instruction.RemittanceInformation.Unstructured.
- NEVER present a consumed or remaining figure as the bank's arithmetic. The API exposes no consumed amount, no remaining amount and no period boundary; every figure here is counted locally and a reinstall restarts it at zero. When the local check blocks an amount, name the limit that stopped it AND say the count is this app's own.
- "Available" from the funds check is transient, never a standing reassurance — consent 45224 showed it can be wrong.
- No re-authentication, no redirect. The defining property of the rail.
