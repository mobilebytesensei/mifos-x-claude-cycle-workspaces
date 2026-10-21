# State: revoking — pay-vrp-mandate-detail

> COPY SOURCE — every string is the verbatim `_strings/strings.yaml` value for the key cited
> inline.
> ⚠ STILL UNSOURCED — the dialog's dismiss label. `ui.yaml#revoke_confirm_dialog` declares title,
> body and confirm ONLY, so no key exists. Do NOT borrow `consent_detail.revoke_dialog.cancel`
> ("Keep access") — that dialog revokes an AIS consent. NOTE the collision the authored copy
> introduces: the confirm CTA is now "Yes, cancel it", so a dismiss reading "Cancel" sits beside
> it meaning the opposite. Declare the dismiss in `ui.yaml` and author a key for it.

Compose the variable payment detail screen with the cancellation confirmation dialog open.
Consent 45223 (creditor: test user), health=active.

## Shell

TopAppBar:
- title: "Variable payment" `{vrp.detail_title}` · titleLarge · onSurface
- navigationIcon: back (arrow_back)
- container: surface

No bottom nav.

## Background (scrimmed)

The detail screen content is visible behind a scrim (scrim=#000000 at 32% opacity):

MandateDetailCard (ElevatedCard: radius=12dp · surfaceContainer · elevation=1dp · padding=16dp):
- Row: "To" `{vrp.review.to}` / "test user · 401800 00133787"
- Row: "Most per payment" `{vrp.review.max_per_payment}` / "£10.00"
- Row: "Status" `{vrp.detail.status}` / MandateHealthChip(active · primaryContainer · autorenew ·
  "Active" `{vrp.health.active}`)

HeadroomSection: label "Limits and spending" `{vrp.detail.headroom}` + one HeadroomCard for the
weekly limit ("£50.00 limit · £10.00 counted from payments made in this app" · progress=0.20),
with `{vrp.pro_rating_notice}` below it as an info note.

PayNowButton (FilledButton · "Pay now" `{vrp.pay_now}` · primary · muted by scrim, not interactive).  
RevokeButton (TextButton · "Cancel this variable payment" `{vrp.revoke}` · error colour · muted by scrim).

## Dialog

AlertDialog: container=surfaceContainerHigh (#E5E8ED) · corner radius=28dp (extra_large) ·
elevation=3dp · padding=24dp · max width=312dp · Auto Layout vertical, spacing=16dp.

### Title

Text: "Cancel this variable payment?" `{vrp.revoke_confirm_title}`  
Style: titleLarge · onSurface

### Body

Text: "The limits you set will be removed and no more payments can be made under this variable payment. This cannot be undone — you would need to set up a new one and approve it with HSBC again."  
`{vrp.revoke_confirm_body}` · Style: bodyMedium · onSurfaceVariant

### Actions row

Horizontal · spacing=8dp · alignment=end.

1. TextButton: label="Cancel" · onSurface · labelLarge — UNSOURCED, see the note above.  
   Action: dismiss dialog, return to detail screen.

2. FilledButton: label="Yes, cancel it" `{vrp.revoke_confirm_cta}` · fill=error (#BA1A1A) ·
   label=onError (#FFFFFF) · radius=full · labelLarge.  
   Action: DELETE /domestic-vrp-consents/45223 → write local revoked record → navigate to list.

## Design constraints

- The confirm fill is error (#BA1A1A) — the one place on this screen where an action CTA takes the error role. The body makes clear this is permanent.
- Do NOT show a loading indicator inside the confirm on tap. The dialog stays open with the confirm disabled until the DELETE 204 returns, then dismisses.
- Write the local revoked record immediately after the 204, before any subsequent GET can fire. After DELETE the consent GET returns 400 U011 forever, and that is a NORMAL terminal state — never rendered as an error.
- The dismiss is a same-weight escape: TextButton, not an outlined or subtle secondary. The PSU must be able to back out without feeling discouraged.
- The body is the authored catalogue value and is deliberately generic — it names neither creditor nor per-payment maximum. Do not re-specialise it; both are on the card behind the dialog.
- Consumer wording throughout: "variable payment", never "VRP" and never "mandate".
