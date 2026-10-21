# MOCKUP — Payments Hub

| Field   | Value    |
|---------|----------|
| Feature | payments |
| Flavor  | consumer |
| State   | content (only state) |

---

## Screen Layout

The Payments hub is the landing surface of the Pay bottom-nav tab. It is a vertically scrollable
column on the `surface` background (`#F7F9FF`). A `surfaceContainer` bottom navigation bar (80dp)
persists at the bottom across all scroll positions; the Pay tab is the active item.

No top app bar is rendered — the tab selection itself is the navigation entry; there is no Back
affordance and no title bar.

Scroll content hierarchy, top to bottom:

1. Screen heading (`hub_heading`) — horizontal padding `spacing.md` (16dp), top `spacing.md`
2. Seven-tile payment-type grid (`payment_type_grid`) — horizontal padding `spacing.md`, gap 12dp
3. Amend notice (`amend_notice`) — horizontal padding `spacing.md`, top `spacing.md`, bottom `spacing.md`

---

## Component Hierarchy

### Hub Heading

**hub_heading**
- Content: "How do you want to pay?"
- Typography: `titleMedium` (16sp, weight 500)
- Color: `onSurface` (`#181C20`)
- Padding: top `spacing.md`, horizontal `spacing.md`, bottom `spacing.sm`
- Accessibility: `role=header`, semantic label matches content

---

### Payment Type Grid

**payment_type_grid**
- Type: `LazyVerticalGrid` — 3 columns (Fixed), gap 12dp both axes
- Item aspect ratio: 1:1 (square tiles)
- Horizontal padding: `spacing.md` (16dp) on both sides
- Accessibility: `role=list`, label "Payment types. Seven options."
- Row count: 3 rows (items 1–3, 4–6, 7 alone left-aligned)
- Tablet/desktop: widens to 4 columns at ≥600dp; tiles stay square

Seven tiles, each implemented as a **rail_tile** component:

#### Tile anatomy (all seven, shared structure)

Each tile is an M3-style `ElevatedCard` or `OutlinedCard`:
- Background: `surfaceContainerLow` (`#F1F4F9`)
- Border: 1dp `outlineVariant` (`#C1C7CE`) at rest — decorative, does not carry a glyph
- Corner radius: `radius.md` (12dp)
- Elevation: level 1 (tonal, no shadow)
- Minimum tap target: 48dp × 48dp (`touch_targets.comfortable`)
- Internal padding: `spacing.md` (16dp)
- Internal layout: `Auto Layout Vertical`, gap `spacing.sm` (8dp)

Tile contents (top to bottom):
1. **Icon** — Material Symbols outlined, 24dp (`icon.md`), color `primary` (`#266489`)
2. **Label** — `labelMedium` (12sp, weight 500), color `onSurface` (`#181C20`)
3. **Description** — `bodySmall` (12sp, weight 400), color `onSurfaceVariant` (`#41474D`), max 2 lines

Interactive states (applied to the Card surface):
| State    | Background              | Overlay opacity | Border                  |
|----------|-------------------------|-----------------|-------------------------|
| Default  | `surfaceContainerLow`   | 0%              | 1dp `outlineVariant`    |
| Pressed  | `surfaceContainerLow`   | 12% `primary` ripple | 1dp `outlineVariant` |
| Focused  | `surfaceContainerLow`   | 12% `primary`   | 2dp `primary`           |
| Disabled | (tiles are never disabled — eligibility is enforced inside the type screen) |

#### The seven tiles

| # | Component ID                       | Icon              | Label                   | Description                        | Route                         |
|---|-------------------------------------|-------------------|-------------------------|------------------------------------|-------------------------------|
| 1 | tile_domestic_single               | `payments`        | Pay someone             | One payment, sent now              | pay-domestic-single           |
| 2 | tile_domestic_scheduled            | `event`           | Pay on a date           | One payment, on a future date      | pay-domestic-scheduled        |
| 3 | tile_domestic_standing_order       | `repeat`          | Standing order          | Same payment, repeating            | pay-domestic-standing-order   |
| 4 | tile_international_single          | `public`          | Pay abroad              | One overseas payment, sent now     | pay-international-single      |
| 5 | tile_international_scheduled       | `public_off`      | Pay abroad on a date    | One overseas payment, on a future date | pay-international-scheduled |
| 6 | tile_international_standing_order  | `currency_exchange` | Overseas standing order | Same overseas payment, repeating  | pay-international-standing-order |
| 7 | tile_vrp_mandate                   | `all_inclusive`   | Variable payments       | Set limits once, pay any amount within them | pay-vrp-mandate    |

**Visual differentiation between the seven tiles:**

Tiles are differentiated by their icon, label, and one-line description only — not by colour or
size. All seven tiles are equal weight: no rail is presented as the default or promoted above the
others, because "the usual one" is a domestic assumption the international rails do not share.

The icon set provides semantic grouping without colour-coding:
- `payments` → immediate, real-time domestic
- `event` → calendar, a single future moment
- `repeat` → loop, a recurring domestic mandate
- `public` → globe, overseas
- `public_off` → globe-off, a single future overseas moment
- `currency_exchange` → exchange arrows, recurring overseas
- `all_inclusive` → infinite, VRP mandate

The description text does the heaviest disambiguation work. The pair users confuse is tiles 2 and 3:
"on a future date" (one-off, scheduled) versus "repeating" (recurring, standing order). These must
never be swapped or paraphrased.

---

### Amend Notice

**amend_notice**
- Content: "To change or cancel a standing order or a scheduled payment you have already set up,
  use the HSBC app or online banking. Open Banking does not let this app change them."
- Typography: `bodySmall` (12sp, weight 400)
- Color: `onSurfaceVariant` (`#41474D`)
- Padding: horizontal `spacing.md`, top `spacing.md`, bottom `spacing.lg`
- Accessibility: `role=text`
- Purpose: OBL Customer Experience Guidelines requirement, surfaced at the Pay landing point so
  PSUs understand the limitation before they create a recurring payment, not after.

---

## Interaction Patterns

### Primary interaction — tap a tile

1. PSU taps any tile card. Ripple effect at `opacity.pressed` (12%) using `primary` overlay.
2. `PaymentsViewModel.openPaymentType(type)` is called with the corresponding `PaymentType` enum.
3. `NavigateToPaymentType` event emitted; NavHost pushes the destination route.
4. The hub stays in the back stack — Back on any type screen returns here.

### No state transitions on the hub itself

The hub has exactly one state (`content`). There is no loading state (nothing to load), no empty
state (seven tiles, always), no error state (no call made), and no eligibility filtering (enforced
downstream). The screen does not change between the moment it first renders and the moment the PSU
leaves it.

---

## Partial-Failure Taxonomy

The hub is specifically designed to have no failure surface of its own. The following failure
scenarios may affect downstream screens but do not affect the hub's rendering:

| Scenario                              | Hub behaviour                           | Who handles it |
|---------------------------------------|----------------------------------------|----------------|
| PSU has no eligible accounts          | Hub renders all seven tiles normally   | Debtor-account picker inside type screen (FR-018) |
| A type screen is not yet implemented  | Not possible at ship — RULE-IMPL-NAVIGATION-CONNECTED-001 enforced by TC-PAY-HUB-002 | feature/payments cannot ship until all seven routes exist |
| VRP endpoint unavailable              | Hub renders the VRP tile normally      | `pay-vrp-mandate` shows its own error state |
| Network offline                       | Hub renders all seven tiles normally (static content, no fetch) | — |
| Auth token expired                    | Hub renders normally; type screen triggers re-auth on first API call | `payment-consent` handles the auth callback |
| HSBC sandbox in maintenance           | Hub renders normally                   | Type screens show error states with retry |

The hub's inability to fail is the whole point. Every other Pay-layer surface in the app has
loading, error and empty states. This one does not — and that is a feature, not an omission.

---

## Responsive Layout Notes

| Width   | Grid columns | Margin    | Gap  |
|---------|:-----------:|-----------|------|
| < 600dp | 3           | 16dp      | 12dp |
| ≥ 600dp | 4           | 24dp      | 12dp |

At 3 columns: row 1 = tiles 1–3, row 2 = tiles 4–6, row 3 = tile 7 alone (left-aligned, not centred).
At 4 columns: row 1 = tiles 1–4, row 2 = tiles 5–7 plus blank cell.

---

## Bottom Navigation (app shell)

| Tab     | Icon              | Label    | Active on this screen? |
|---------|-------------------|----------|:----------------------:|
| Home    | `home`            | Home     | No                     |
| Accounts| `account_balance` | Accounts | No                     |
| Pay     | `payment`         | Pay      | Yes — filled/tinted `primary` |
| More    | `more_horiz`      | More     | No                     |

Bottom nav container: `surfaceContainer` (`#EBEEF3`), 80dp, active item `primary` (`#266489`),
inactive `onSurfaceVariant`.
