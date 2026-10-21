# State: content — pay-vrp-mandate

> COPY SOURCE — every user-facing string below is the verbatim `_strings/strings.yaml` value for
> the key `screens/pay-vrp-mandate/ui.yaml` binds. Resolved: `vrp.title` · `vrp.create_action` ·
> `vrp.list_label` · `vrp.health.active` ("Active") · `vrp.health.revoked` ("Cancelled" — the
> authored value for the state `ui.yaml` names `revoked`; the word is now cited, not guessed).
> `limitsSummary` is a formatted data value, not a string key — correctly keyless.
> No unsourced copy remains in this state.

Compose a mobile screen showing a list of variable payments with two examples: one active, one cancelled.

## Shell

TopAppBar:
- title: "Variable payments" · titleLarge · onSurface   `{strings.vrp.title}`
- navigationIcon: arrow_back
- actions: IconButton(add · onSurface tint · contentDescription="Set up a variable payment"
  `{strings.vrp.create_action}`)
- container: surface

BottomNavigationBar: active tab = Pay · active indicator = primary

## Mandate rows

The list itself carries contentDescription="Your variable payments" `{strings.vrp.list_label}`.

Each row is an ElevatedCard: corner radius 12dp · fill=surfaceContainer · elevation=1dp · full width.  
Interior Auto Layout: horizontal, spacing=12dp, padding=16dp.

### Row 1 — Active (consent 45223)

Leading: Icon(autorenew · size=40dp · tint=primary) inside a 48×48dp Box.

Body (vertical Auto Layout, spacing=4dp, flex-grow):
- Text: "test user" · titleMedium · onSurface
- Text: "Up to £10.00 per payment · £50.00 / week" · bodySmall · onSurfaceVariant

Trailing: MandateHealthChip — state=active
- Fill: primaryContainer (#C9E6FF)
- Icon: autorenew · size=16dp · colour=onPrimaryContainer (#004B6F)
- Label: "Active" · labelSmall · onPrimaryContainer   `{strings.vrp.health.active}`
- Corner radius: full (pill) · padding 8dp H, 4dp V

### Row 2 — Cancelled (consent 45205)

Leading: Icon(autorenew · size=40dp · tint=onSurfaceVariant) inside a 48×48dp Box.

Body (vertical Auto Layout, spacing=4dp, flex-grow):
- Text: "savings account" · titleMedium · onSurface
- Text: "Up to £5.00 per payment · £25.00 / week" · bodySmall · onSurfaceVariant

Trailing: MandateHealthChip — state=revoked
- Fill: surfaceVariant (#DDE3EA)
- Icon: block · size=16dp · colour=onSurfaceVariant (#41474D)
- Label: "Cancelled" · labelSmall · onSurfaceVariant   `{strings.vrp.health.revoked}`
- Corner radius: full (pill) · padding 8dp H, 4dp V

## Layout

ContentArea: background=surface · padding=16dp. Rows stacked vertically with 12dp gap.

## Design constraints

- autorenew icon for the category — never a payment/send icon
- Health chip fills taken exactly from design-tokens.yaml (primaryContainer / surfaceVariant)
- active chip icon and revoked chip icon must differ (autorenew vs block)
- `revoked` is a NORMAL terminal state, not a fault — muted neutral, never error-coloured
- Colour is never the only signal: icon + label always present together
- Minimum touch target per row: 48dp height minimum (card enforces this)
- Tap action: navigate to the variable payment detail (ripple = primary at 8% opacity on press)
