# State: error — pay-vrp-mandate-detail

> COPY SOURCE — every string is the verbatim `_strings/strings.yaml` value for the key cited
> inline. SHAPE MISMATCH RESOLVED — the banner is now ONE text run, matching the single `content`
> key `ui.yaml#unpayable_mandate_banner` declares. The former four separate runs are gone.
> No unsourced copy remains in this state.

Compose the variable payment detail screen in the AUTH-but-unpayable state: consent 45224,
health=unpayable. The PSU completed SCA, the consent is authorised, the funds check said
"Available" — and every payment failed 400 U021 because the bank wrote a UK.OBIE.PAN (credit
card) debtor into it.

## Shell

TopAppBar: title "Variable payment" `{vrp.detail_title}` · titleLarge · onSurface ·
navigationIcon=arrow_back · container=surface. No bottom nav.

## Summary card

ElevatedCard: radius=12dp · surfaceContainer · elevation=1dp · full width · padding=16dp.
Rows (vertical, 8dp):
1. "To" `{vrp.review.to}` / "savings account · 401800 00133788"
2. "Most per payment" `{vrp.review.max_per_payment}` / "£5.00" (Roboto Mono · bodyLarge)
3. "Status" `{vrp.detail.status}` / MandateHealthChip(unpayable): fill=errorContainer ·
   Icon=error 16dp · tint=onErrorContainer · label="Cannot make payments"
   `{vrp.health.unpayable}` labelSmall · radius=full · padding 8/4dp

## Error banner

ErrorBanner: full width · fill=errorContainer (#FFDAD6) · radius=12dp · padding=16dp ·
margin-top=12dp. Interior: horizontal · top-start · 12dp. Icon: error · 24dp ·
tint=onErrorContainer (#93000A).

ONE text run · bodyMedium · onErrorContainer:
"This variable payment cannot make any payments. The account you chose at HSBC cannot be used for them, and that cannot be changed now. The funds check said the money was there, but every payment has been turned down. Cancel this one and set up a new one against an account with a sort code and account number."
`{vrp.unpayable_banner}`

## Limits and spending

Section label: "Limits and spending" `{vrp.detail.headroom}` · titleMedium · onSurface. NOT
"What's left" — the figure is this app's own tally.

HeadroomCard (ElevatedCard: radius=12dp · surfaceContainer · elevation=1dp · padding=16dp):
- "Weekly limit" (bodyMedium · onSurface) / "£25.00 limit · nothing counted from payments made in
  this app" (bodySmall · onSurfaceVariant)
- LinearProgressIndicator: progress=0.00 · primary / primaryContainer · height=4dp

Below it, Icon(info · 16dp · onSurfaceVariant) + Text (bodySmall · onSurfaceVariant):
"Your first period may allow less than this, because it starts partway through. HSBC works that out and does not share the figure, so this app cannot show how much is left in it."
`{vrp.pro_rating_notice}`

All three attempts failed U021, and failed payments are excluded from periodic totals per spec,
so the local count is genuinely nothing — not a stale zero.

## Action buttons

Pay now: HIDDEN (health == unpayable).

RevokeButton: TextButton · label="Cancel this variable payment" `{vrp.revoke}` · colour=error
(#BA1A1A) · labelLarge · full width · margin-top=24dp. Action: ConfirmRevoke → the confirm
dialog. Offered here — this is the one the PSU most wants gone.

## Design constraints

- Do NOT show the earlier funds check as reassurance. "Available" was a false positive, and the banner says so.
- Do NOT offer a retry. The payload came verbatim from the bank's own authorised consent — the same request produces the same refusal.
- Error role on both chip and banner — both signal "the bank cannot make the payment", not "the PSU made a mistake".
- Consent status is AUTH and the chip says "Cannot make payments". These coexist. Never derive the chip from consent status.
- NEVER present a consumed or remaining figure as the bank's arithmetic. The API exposes no consumed or remaining amount and no period boundary.
- errorContainer fill · onErrorContainer text and icons. Contrast 7.24:1 (W-03/W-06), WCAG AA.
