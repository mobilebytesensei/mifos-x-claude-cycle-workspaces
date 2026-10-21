# Standing Orders — Visual Specification

| Field | Value |
|---|---|
| Feature | standing-orders |
| Flavor | consumer |
| Archetype | index_list |

---

## Screen Layout

Top-to-bottom layout on a vertically scrolling list screen with FAB:

```
[ Top App Bar: "Standing Orders"  ← ⚙️ ]  ← filter_list action
────────────────────────────────────────
[ Standing Orders     [3 active]        ]  ← headlineLarge `primary` + `primaryContainer` chip
────────────────────────────────────────
┌──────────────────────────────────────┐
│  Rent Payment            [Active ✓]  │  ← surfaceContainerLowest card, elevation 2
│  To: Landlord Holdings Ltd           │  ← bodyMedium, `onSurfaceVariant`
│  £1,200 / month        Next: 1 Jun   │  ← `primary` bold | bodySmall `onSurfaceVariant`
│                      [✏️]  [🗑️]      │  ← edit `primary` | delete `error`
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│  Netflix Subscription    [Active ✓]  │  ← surfaceContainerLowest card, elevation 2
│  (no beneficiary label shown)        │
│  £15.99 / month       Next: 7 Jun   │
│                      [✏️]  [🗑️]      │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐  ← dimmed: surfaceContainerLow bg, outlineVariant border
│  Gym Membership         [Paused ⏸]   │  ← muted text | neutral badge
│  £45.00 / month  Next: 15 Jun (Paused)│ ← `onSurfaceVariant` amount + date
│                      [✏️]  [🗑️]      │
└──────────────────────────────────────┘

                              [+ Create ]  ← FAB bottom-right, `primary`
────────────────────────────────────────
```

---

## Components

### title_count_row
- Horizontal stack, alignment center, spacing `spacing.md`
- Padding bottom: `spacing.md`, separates header from first card

### standing_orders_title
- Content: "Standing Orders"
- Typography: `headlineLarge`, color `primary`
- Flex-grows to fill space left of chip

### active_count_chip
- Content: "3 active"
- Background: `primaryContainer`, corner radius: `radius.md`
- Padding: `spacing.sm` horizontal, `spacing.xs` vertical
- Text: `labelMedium`, color `onPrimaryContainer`, semibold
- Communicates health at a glance — an active count, not a warning

### Standing order cards (Active: standing_order_rent, standing_order_netflix)
- Background: `surfaceContainerLowest`, corner radius: `radius.lg`, elevation: 2
- Border: `outlineVariant`, `border.thin`, margin bottom: `spacing.md`
- Padding: `spacing.md` horizontal and vertical
- Header row: `space_between` — title left, status badge right
- Beneficiary text: `bodyMedium`, `onSurfaceVariant`, prefix "To: "
- Amount row: `space_between` — amount left (`primary` semibold, Roboto Mono) | next date right (`bodySmall`, `onSurfaceVariant`)
- Actions row: `flex_end` — edit icon then delete icon, `spacing.sm` spacing

### Paused card (standing_order_gym)
- Background: `surfaceContainerLow` (one step up the tonal ladder from active), corner radius: `radius.lg`, elevation: 1
- Border: `outlineVariant`, `border.thin`
- Title text: `onSurfaceVariant` (dimmed vs active `onSurface`)
- Badge: "Paused" — background `surfaceContainerHigh`, text `onSurfaceVariant`, leading `pause_circle` icon
- Amount: `onSurfaceVariant` at `opacity.disabled`-adjacent weight (dimmed, not primary)
- Date: `onSurfaceVariant` — "Next: 15 Jun 2026 (Paused)" with literal "(Paused)" suffix

### Active badge
- Background `primaryContainer`, corner radius `radius.sm`, padding `spacing.sm` × `spacing.xs`
- Text: `labelSmall`, color `onPrimaryContainer`, leading `check_circle` icon (`icon.xs`)

### Paused badge
- Background `surfaceContainerHigh`, corner radius `radius.sm`
- Text: `labelSmall`, color `onSurfaceVariant`, leading `pause_circle` icon (`icon.xs`)

### Action icons (edit, delete)
- Edit: `edit_outlined`, size `icon.md`, color `primary`, `spacing.sm` padding
- Delete: `delete_outlined`, size `icon.md`, color `error`, `spacing.sm` padding
- Actions row: `justify: flex_end`, padding top `spacing.md`

### create_standing_order_fab
- Position: floating_action_button (bottom-right)
- Background: `primary`, text: `onPrimary`
- Leading icon: `add` (`icon.md`), corner radius `radius.lg`, elevation 6

---

## Interaction Patterns

| Interaction | Component | Result |
|---|---|---|
| Tap order card | standing_order_* | Opens standing order detail bottom sheet |
| Tap edit icon | *_edit_icon | Opens edit standing order sheet |
| Tap delete icon | *_delete_icon | Confirmation dialog: "Delete this standing order?" [Delete] [Cancel] |
| Confirm delete | — | DELETE_FAILED if error; success removes from list |
| Tap FAB | create_standing_order_fab | Opens create standing order form bottom sheet |
| Tap filter icon | filter_list (top bar) | Filter bottom sheet: All / Active / Paused |
| Pull to refresh | scroll area | RefreshTriggered event → reload list |

---

## Content Data

| Order | Beneficiary | Amount | Frequency | Next Date | Status |
|---|---|---|---|---|---|
| Rent Payment | Landlord Holdings Ltd | £1,200 | Monthly | 1 Jun 2026 | Active |
| Netflix Subscription | (Netflix) | £15.99 | Monthly | 7 Jun 2026 | Active |
| Gym Membership | (Gym) | £45.00 | Monthly | 15 Jun 2026 | Paused |
| Active count chip | — | — | — | — | "3 active" |

---

## Design Notes

**Active vs Paused visual differentiation:** active cards sit on `surfaceContainerLowest`; paused cards step up the tonal ladder to `surfaceContainerLow`. Active text uses full-contrast `onSurface`; paused uses `onSurfaceVariant`. This passive dimming communicates "paused" without requiring users to read the badge — the card *looks* inactive. Both badges also carry an icon (`check_circle` / `pause_circle`), so state is never conveyed by tone alone (WCAG 1.4.1).

**Active is `primary`, not green:** the active-count chip and the Active badge use `primaryContainer` / `onPrimaryContainer`. This palette ships no green family — DESIGN.md maps the success/healthy semantic onto the primary blue, and the same pair is used for a settled payment elsewhere in the app, so "active" and "settled" read as one visual language.

**Amount in primary colour:** £ amounts use `primary` for active orders and `onSurfaceVariant` for paused. The brand colour acts as a "this is moving money" signal. Every amount is set in Roboto Mono per the `amount` component contract so figures align down the column.

**Delete in `error`, edit in `primary`:** icon colour assignment at the row level ensures accidental taps result in an edit (reversible) not a delete (irreversible). Edit is on the left, delete on the right — matching the standard swipe-to-delete direction. `error` here is correct rather than over-applied: deleting a standing order is genuinely irreversible.

**FAB placement:** bottom-right per MD3 FAB spec, elevation 6, always visible in content, empty, and error states — creation is always available.

**Empty state copy:** "Set up recurring payments to automate your regular bills" — benefit-oriented language, not feature-describing. Pairs with `repeat_off` icon for context.

*Generated by /idea export | 2026-08-03*
