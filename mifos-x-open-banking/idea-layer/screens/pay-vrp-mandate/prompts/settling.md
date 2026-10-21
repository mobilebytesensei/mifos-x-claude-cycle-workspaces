# State: settling — pay-vrp-mandate-detail

> COPY SOURCE — every string is the verbatim `_strings/strings.yaml` value for the key cited
> inline; `vrp.settling` is "Sending your payment". ⚠ STILL UNSOURCED — no catalogue key AND no
> component in `ui.yaml` for the charge note ("£0.05 bank charge applied to this payment").

Compose the variable payment detail screen immediately after POST /domestic-vrps returned 201 for
payment 19929. A 30-second settling indicator is running — the only rail where this countdown is
honest.

## Shell

TopAppBar:
- title: "Variable payment" `{vrp.detail_title}` · titleLarge · onSurface
- navigationIcon: arrow_back
- container: surface

No bottom nav.

## Background — summary card

ElevatedCard: radius=12dp · surfaceContainer · elevation=1dp · full width · padding=16dp.

Rows (vertical, 8dp). Labels bodyMedium · onSurfaceVariant; values bodyLarge · onSurface.
1. "To" `{vrp.review.to}` / "test user · 401800 00133787"
2. "Most per payment" `{vrp.review.max_per_payment}` / "£10.00" (Roboto Mono)
3. "Status" `{vrp.detail.status}` / MandateHealthChip(active · primaryContainer · autorenew ·
   "Active" `{vrp.health.active}` · onPrimaryContainer)

## Settling card

ElevatedCard: radius=12dp · surfaceContainer · elevation=1dp · full width · padding=16dp ·
margin-top=12dp. Interior: horizontal · center-start · spacing=16dp.

CircularProgressIndicator: 40dp · strokeWidth=4dp · fill=secondary (#50606E) ·
track=secondaryContainer (#D3E5F5) · indeterminate=false · animating.

Text column (vertical, spacing=4dp):
- "Sending your payment" `{vrp.settling}` · titleMedium · onSurface
- "Expected by 15:19:48" · bodyMedium · onSurfaceVariant
  (ExpectedSettlementDateTime = CreationDateTime + 30s. Payment 19929: 15:19:18 → 15:19:48)

## Limits and spending (updated after payment)

Section label: "Limits and spending" `{vrp.detail.headroom}` · titleMedium · onSurface ·
margin-top=16dp. Deliberately NOT "What's left" — the figure is this app's own tally.

HeadroomCard (ElevatedCard: radius=12dp · surfaceContainer · elevation=1dp · padding=16dp):
- "Weekly limit" (bodyMedium · onSurface) / "£50.00 limit · £10.00 counted from payments made in
  this app" (bodySmall · onSurfaceVariant)
  (£5.00 just appended to the local ledger; previous entry also £5.00)
- LinearProgressIndicator: progress=0.20 · primary / primaryContainer · height=4dp · radius=full

Below the card, Icon(info · 16dp · onSurfaceVariant) + Text (bodySmall · onSurfaceVariant):
"Your first period may allow less than this, because it starts partway through. HSBC works that out and does not share the figure, so this app cannot show how much is left in it."
`{vrp.pro_rating_notice}`

## Charge note

Row below the pro-rating note: Icon(info · 16dp · onSurfaceVariant) + Text("£0.05 bank charge
applied to this payment" · bodySmall · onSurfaceVariant).

## No action buttons

Pay now and the cancel action are both hidden during settling. They reappear when the state ends
(settlement confirmed, or the indicator lapses to in-progress).

## Design constraints

- CircularProgressIndicator uses secondary, not primary. Primary is the credit colour here; neutral slate reads as "working".
- The countdown is driven from the returned ExpectedSettlementDateTime, NEVER a hardcoded 30 seconds. If settlement runs long, lapse to a plain in-progress state with no error — nothing has failed.
- Charge (£0.05 UK.OBIE.CHAPSOut) is shown here, not on the consent screen. Charges appear per payment.
- No celebration, no confetti, no green. "Sending your payment" is the accurate statement: the payment is in progress, not sent.
- NEVER present a consumed or remaining figure as the bank's arithmetic. The ledger is updated locally on the 201 response; the API confirms none of it.
