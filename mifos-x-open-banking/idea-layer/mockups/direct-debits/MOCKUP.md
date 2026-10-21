# Direct Debits — Visual Specification

| Field | Value |
|---|---|
| Feature | direct-debits |
| Flavor | consumer |
| Archetype | index_list |
| Status | designed |

---

## Screen Layout

### State: populated

```
┌──────────────────────────────────────────┐
│ ←  Direct Debits                      ⋮  │  ← TopAppBar: arrow_back | more_vert
├──────────────────────────────────────────┤
│                                          │
│  Direct Debits          [3 active]       │  ← headlineLarge `primary` | chip
│                                          │    `primary_container`
│ ┌────────────────────────────────────┐   │
│ │  Netflix                 [Active]  │   │  ← card `surface`, elevation 2, radius.lg
│ │  £15.99 / month    Next: 3 Jun 2026│   │  ← `primary` semibold | bodySmall
│ │  Ref: DD-NF-20240301               │   │  ← labelSmall `on_surface_variant`
│ └────────────────────────────────────┘   │  ← margin spacing.md h, spacing.md bottom
│                                          │
│ ┌────────────────────────────────────┐   │
│ │  Spotify                 [Active]  │   │  ← card `surface`, elevation 2, radius.lg
│ │  £10.99 / month   Next: 12 Jun 2026│   │
│ │  Ref: DD-SP-20231115               │   │
│ └────────────────────────────────────┘   │
│                                          │
│ ┌────────────────────────────────────┐   │
│ │  PureGym             [Cancelled]   │   │  ← muted card `surface_container`,
│ │  £29.99 / month                    │   │    no elevation, radius.lg
│ │  Ref: DD-GYM-20220601              │   │  ← `on_surface_variant` (no next date)
│ └────────────────────────────────────┘   │
│                                          │
│                    [+ Set Up Direct Debit]│  ← FAB bottom-right, `primary`, elev 6
└──────────────────────────────────────────┘
```

---

### State: loading

```
┌──────────────────────────────────────────┐
│ ←  Direct Debits                      ⋮  │
├──────────────────────────────────────────┤
│                                          │
│  Direct Debits                           │  ← Title visible; no count chip yet
│                                          │
│ ┌────────────────────────────────────┐   │
│ │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │   │  ← Skeleton card 1, h=110dp, shimmer
│ └────────────────────────────────────┘   │
│ ┌────────────────────────────────────┐   │
│ │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │   │  ← Skeleton card 2, h=110dp, shimmer
│ └────────────────────────────────────┘   │
│ ┌────────────────────────────────────┐   │
│ │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │   │  ← Skeleton card 3, h=110dp, shimmer
│ └────────────────────────────────────┘   │
└──────────────────────────────────────────┘
```

Skeleton fills use `surface_container`.

---

### State: empty

```
┌──────────────────────────────────────────┐
│ ←  Direct Debits                      ⋮  │
├──────────────────────────────────────────┤
│                                          │
│  Direct Debits                           │
│                                          │
│                                          │
│                                          │
│              [account_balance_wallet]    │  ← icon, large, `outline`
│                                          │
│          No direct debits set up         │  ← titleMedium, `on_surface`, centered
│                                          │
│  Authorise merchants like Netflix or     │  ← bodyMedium, `on_surface_variant`,
│  your utility providers to collect       │    centered
│  payments automatically on agreed dates  │
│                                          │
│                                          │
│                    [+ Set Up Direct Debit]│  ← FAB always visible
└──────────────────────────────────────────┘
```

---

### State: cancel_confirm (dialog overlay)

```
┌──────────────────────────────────────────┐
│ ←  Direct Debits                      ⋮  │
├──────────────────────────────────────────┤  ← full list visible behind dim overlay
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  ← `scrim` alpha 0.5
│░░░░                                 ░░░░│
│░░░░  ┌──────────────────────────┐  ░░░░│
│░░░░  │   Cancel Direct Debit?   │  ░░░░│  ← dialog radius.xl, elev 8, `surface` bg
│░░░░  │                          │  ░░░░│  ← headlineSmall `on_surface` bold
│░░░░  │  Netflix (DD-NF-20240301)│  ░░░░│
│░░░░  │  will stop collecting    │  ░░░░│  ← bodyMedium `on_surface_variant`
│░░░░  │  payments. This cannot   │  ░░░░│
│░░░░  │  be undone.              │  ░░░░│
│░░░░  │                          │  ░░░░│
│░░░░  │  [Yes, Cancel Mandate ]  │  ░░░░│  ← filled `error`/`on_error`, radius.md
│░░░░  │  [   Keep Mandate     ]  │  ░░░░│  ← outlined `primary`, radius.md
│░░░░  └──────────────────────────┘  ░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└──────────────────────────────────────────┘
```

---

### State: error

```
┌──────────────────────────────────────────┐
│ ←  Direct Debits                      ⋮  │
├──────────────────────────────────────────┤
│                                          │
│  Direct Debits                           │
│                                          │
│                                          │
│                 [cloud_off]              │  ← icon, large, `outline`
│                                          │
│       Unable to load direct debits       │  ← titleMedium, `on_surface`, centered
│                                          │
│   Check your connection and try again    │  ← bodyMedium, `on_surface_variant`
│                                          │
│              [    Try Again    ]         │  ← outlined button, `primary`
│                                          │
│                    [+ Set Up Direct Debit]│  ← FAB always visible
└──────────────────────────────────────────┘
```

---

## Component Detail

### Mandate Card — Active (Netflix, Spotify)

```
┌──────────────────────────────────────────┐
│  {MerchantName}              [Active]    │  ← titleMedium `on_surface` semibold
│                                          │    badge `primary_container` + check_circle
│  £{amount} / month     Next: {date}      │  ← bodyLarge `primary` semibold, Roboto Mono
│                                          │    | bodySmall `on_surface_variant`
│  Ref: {mandateReference}                 │  ← labelSmall `on_surface_variant`
└──────────────────────────────────────────┘
  Background: `surface` | corner_radius: radius.lg | elevation: 2
  Border: `outline` border.thin | margin: spacing.md h, spacing.md bottom
  Padding: spacing.md
  on_click: view_direct_debit → direct-debit-detail
```

### Mandate Card — Cancelled (PureGym)

```
┌──────────────────────────────────────────┐
│  {MerchantName}          [Cancelled]     │  ← titleMedium `on_surface_variant`
│                                          │    badge `surface_container` + cancel icon
│  £{amount} / month                       │  ← bodyLarge `on_surface_variant` normal
│                                          │    (no next date row)
│  Ref: {mandateReference}                 │  ← labelSmall `on_surface_variant`
└──────────────────────────────────────────┘
  Background: `surface_container` | corner_radius: radius.lg | elevation: 0
  Border: `outline` border.thin | margin: spacing.md h, spacing.md bottom
  Padding: spacing.md
  on_click: view_direct_debit → direct-debit-detail
```

### Active Count Chip

```
 [3 active]
  Background: `primary_container` | corner_radius: radius.md
  Padding: spacing.sm h, spacing.xs v
  Typography: labelMedium | Color: `on_primary_container` | font_weight: semibold
  Updates when a mandate is cancelled (3 → 2)
```

### Cancel Confirmation Dialog

```
┌──────────────────────────────────────────┐
│        Cancel Direct Debit?              │  ← headlineSmall `on_surface` bold
│                                          │
│  {merchantName} ({mandateRef}) will      │  ← bodyMedium `on_surface_variant`
│  stop collecting payments. This          │
│  cannot be undone.                       │
│                                          │
│  ┌──────────────────────────────────┐    │  ← filled `error`/`on_error`, radius.md
│  │       Yes, Cancel Mandate        │    │
│  └──────────────────────────────────┘    │
│                                          │
│  ┌──────────────────────────────────┐    │  ← outlined `primary`, radius.md
│  │          Keep Mandate            │    │
│  └──────────────────────────────────┘    │
└──────────────────────────────────────────┘
  corner_radius: radius.xl | background: `surface` | elevation: 8
  padding: spacing.lg h+v | Overlay scrim: `scrim` alpha 0.5
```

---

## Interaction Patterns

| Interaction | Component | Result |
|---|---|---|
| Tap Netflix card | direct_debit_netflix | view_direct_debit → direct-debit-detail sheet |
| Tap Spotify card | direct_debit_spotify | view_direct_debit → direct-debit-detail sheet |
| Tap PureGym card | direct_debit_gym | view_direct_debit → direct-debit-detail sheet (read-only) |
| Tap "Yes, Cancel Mandate" | cancel_confirm_cta | confirm_cancel_direct_debit → DELETE API → reload list |
| Tap "Keep Mandate" | cancel_dismiss_cta | dismiss_cancel_dialog → close dialog, no side effects |
| Tap FAB | setup_direct_debit_fab | setup_direct_debit → new mandate setup sheet |
| Tap back arrow | top bar navigation_icon | navigate_back → accounts screen |
| Tap overflow (⋮) | more_vert | open_direct_debit_options → options menu |
| Pull to refresh | scroll area | RefreshTriggered event → reload mandate list |
| Tap retry (error) | retry_button | RetryLoad event → loading state → API call |

---

## Design Notes

**Mandate reference on every card:** `mandate_reference` (e.g., "DD-NF-20240301") is surfaced in `labelSmall` muted text on every card — active and cancelled. This supports user support queries and is injected into the cancel confirm dialog body for explicit confirmation.

**Active status is `primary`, cancelled is neutral:** the count chip and Active badge use `primary_container` / `on_primary_container` with a `check_circle` icon — this palette maps the healthy/success semantic onto the trust-blue and ships no green. A cancelled mandate takes the neutral `surface_container` with a `cancel` icon rather than `error`: the customer chose to cancel it, so nothing has gone wrong. `error` on this screen is reserved for the one genuinely destructive action, the confirm CTA.

**Cancelled card visual language:** the PureGym card recedes by tone rather than by a second colour — `surface_container` background (vs `surface` for active), zero elevation, and `on_surface_variant` for the merchant name, amount, and reference. No next-date row, which is irrelevant for a cancelled mandate. Both badges pair tone with an icon and a text label, so status is never colour-only (WCAG 1.4.1).

**Active count chip accuracy:** the "3 active" chip reflects active Netflix + Spotify only — PureGym is cancelled and excluded from the active count. If the user cancels Netflix, the chip updates to "2 active" without a screen reload (optimistic update from ViewModel).

**Destructive action guard:** the cancel flow is a two-step interaction: (1) the user must explicitly choose to cancel from the detail view, (2) the `cancel_confirm` dialog then requires a second explicit confirmation with the `error` "Yes, Cancel Mandate" CTA. This friction is intentional — direct debit cancellation cannot be undone within the app.

**No quick-delete row icons:** direct debits differ from standing orders (which are user-controlled). Cancellation requires navigating to detail first. No swipe-to-delete or row-level delete icons — this asymmetry is by design.

**FAB always visible:** the "Set Up Direct Debit" FAB is visible in all states (populated, empty, error). Even when viewing cancelled mandates, users should always have a path to set up new ones. The FAB is hidden only during the loading skeleton state.

**Cancelled mandates in list:** OBP returns both active and cancelled mandates. Cancelled mandates are shown at the bottom of the list in a muted style — they provide an audit trail (the user can see what was cancelled and when).

*Generated by /idea export | 2026-08-03*
