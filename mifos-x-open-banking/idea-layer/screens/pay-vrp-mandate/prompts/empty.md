# State: empty — pay-vrp-mandate

> COPY SOURCE — every user-facing string below is the verbatim `_strings/strings.yaml` value for
> the key `screens/pay-vrp-mandate/ui.yaml` binds. Resolved: `vrp.title` · `vrp.empty_title` ·
> `vrp.empty_body` · `vrp.create_action`.
> The former "Redirection note" section is GONE as a separate block: `ui.yaml#no_mandates` folds
> that content into `body`, and the authored `vrp.empty_body` carries it. It must not be split
> back out into a second string.
> No unsourced copy remains in this state.

Compose a mobile screen showing the first-run empty state for the variable payments list.
The PSU has no variable payments yet, or has never used this app to set one up.

## Shell

TopAppBar:
- title: "Variable payments" · titleLarge · onSurface   `{strings.vrp.title}`
- navigationIcon: arrow_back
- actions: IconButton(add · onSurface tint · contentDescription="Set up a variable payment"
  `{strings.vrp.create_action}`)
- container: surface

BottomNavigationBar: active tab = Pay · indicator = primary

## Empty state content

Vertically centred in the available screen area between the top bar and bottom nav.
Auto Layout: vertical · alignment=center · spacing=24dp · horizontal padding=32dp.

### Illustration

Icon: account_balance · size=64dp · tint=onSurfaceVariant · no background circle.

### Headline

Text: "No variable payments"   `{strings.vrp.empty_title}`  
Style: headlineSmall · onSurface · textAlign=center

### Body copy

Text (ONE paragraph, rendered in full — no truncation, no ellipsis):
"A variable payment lets you set spending limits once, then pay any amount within them without approving each payment. You have not set one up yet. Only the ones you set up in this app appear here, so one set up on another device will not show. If you want a payment on a set date, or one that repeats on a schedule, use Pay on a date or Standing order instead."

`{strings.vrp.empty_body}` · Style: bodyMedium · onSurfaceVariant · textAlign=center

### CTA

FilledButton: label="Set up a variable payment" `{strings.vrp.create_action}` · corner radius=full (pill) · fill=primary (#266489) · label=onPrimary (#FFFFFF) · labelLarge.  
Action: StartCreate — opens the 4-step create form.

## Design constraints

- The body paragraph must render complete. It carries two facts the PSU cannot infer and that no other surface states: this list only ever shows ones set up in THIS app, and a dated or repeating instruction belongs to Pay on a date / Standing order instead.
- No sign-in prompt, no "connect your bank", no session-related messaging. This empty state is reached with a valid session.
- Do not imply the PSU's bank account is empty — this is about records held on this device.
- account_balance icon is informational, not a status icon. No status chip present.
- Background: surface (#F7F9FF). No card wrapper around the empty state content.
