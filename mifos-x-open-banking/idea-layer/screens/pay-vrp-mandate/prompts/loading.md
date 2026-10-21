# State: loading — pay-vrp-mandate

> COPY SOURCE — every user-facing string below is the verbatim `_strings/strings.yaml` value for
> the key `screens/pay-vrp-mandate/ui.yaml` binds. Resolved: `vrp.title` (top bar) ·
> `vrp.create_action` (the add action's label, used as its contentDescription).
> No unsourced copy remains in this state.

Compose a mobile screen for the "Variable payments" list in its loading state.

## Shell

TopAppBar:
- title: "Variable payments" · titleLarge · onSurface   `{strings.vrp.title}`
- navigationIcon: arrow_back
- actions: IconButton(add · onSurface tint · contentDescription="Set up a variable payment"
  `{strings.vrp.create_action}`)
- container: surface

BottomNavigationBar:
- active tab: Pay · indicator = primary

## Layout

ContentArea: background=surface · padding=16dp vertical, 16dp horizontal.

Show three MandateSkeleton cards stacked vertically with 12dp spacing between them. Each card:
- ElevatedCard: corner radius 12dp · fill=surfaceContainer · elevation 1dp
- Interior padding 16dp
- Three ShimmerBox elements inside (vertical, 8dp gap):
  1. ShimmerBox width=160dp height=14dp corner-radius=4dp fill=surfaceContainerHigh
  2. ShimmerBox width=120dp height=12dp corner-radius=4dp fill=surfaceContainerHighest
  3. ShimmerBox width=80dp height=24dp corner-radius=full fill=surfaceContainerHigh
- Apply a left-to-right shimmer animation: fill sweeps from surfaceContainerHigh to surfaceContainerHighest over 1200ms, easing=Linear, repeating. No bounce.

The rest of the screen shows no text, no buttons, no icons. Empty space uses surface (#F7F9FF).

## Design constraints

- Auto Layout vertical, spacing=12dp, padding=16dp
- No animation beyond the shimmer sweep
- Colours from design-tokens.yaml only — no inline hex
- All skeleton shapes pill or rectangular — no illustrative graphics
