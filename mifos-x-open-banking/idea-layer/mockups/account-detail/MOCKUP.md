# Visual Specification — Account Detail
**Feature:** account-detail | **Flavor:** consumer

---

## Screen Layout

Full-screen vertical scroll with a top app bar ("Account Details" + back arrow) and persistent bottom navigation:

```
┌────────────────────────────────────┐
│ ← Account Details                  │  ← top app bar (`primary` bg)
├────────────────────────────────────┤
│  Primary Checking                  │
│  £4,250.00                         │  ← account_header_card (bg `primary`)
│  [GBP] [CHECKING]                  │
├────────────────────────────────────┤
│ ┌──────────────────────────────┐   │
│ │ IBAN                    [⎘] │   │  ← account_info_card (elevation 3,
│ │ DE89 3704 0044 0532 0130 00  │   │    negative top margin overlapping hero)
│ │──────────────────────────────│   │
│ │ BIC / SWIFT             [⎘] │   │
│ │ COBADEFFXXX                  │   │
│ └──────────────────────────────┘   │
├────────────────────────────────────┤
│ [Send Money] [Request] [Statement] │  ← action_row
├────────────────────────────────────┤
│  Recent Transactions      View All │  ← transactions_header_row
│ ┌──────────────────────────────┐   │
│ │ 🛒 Tesco Supermarket          │   │
│ │    23 May 2026         -£42.50│   │  ← detail_txn_row_1
│ └──────────────────────────────┘   │
│ ┌──────────────────────────────┐   │
│ │ 💰 Salary Payment             │   │
│ │    22 May 2026      +£3,200.00│   │  ← detail_txn_row_2
│ └──────────────────────────────┘   │
│ ┌──────────────────────────────┐   │
│ │ ⚡ EDF Energy                 │   │
│ │    20 May 2026         -£94.20│   │  ← detail_txn_row_3
│ └──────────────────────────────┘   │
│ ┌──────────────────────────────┐   │
│ │ 📦 Amazon Prime               │   │
│ │    18 May 2026          -£8.99│   │  ← detail_txn_row_4
│ └──────────────────────────────┘   │
│ ┌──────────────────────────────┐   │
│ │ ☕ Costa Coffee               │   │
│ │    17 May 2026          -£3.75│   │  ← detail_txn_row_5
│ └──────────────────────────────┘   │
├────────────────────────────────────┤
│  [Home] [Accounts*] [Pay] [Cards] [More] │
└────────────────────────────────────┘
```

---

## Components

### account_header_card — Hero Section
- **Background:** `primary`, full width, no border radius
- **Padding:** horizontal `spacing.lg`, top `spacing.md`, bottom `spacing.xl`
- **account_header_label:** "Primary Checking" — `labelLarge`, color `onPrimary` at reduced emphasis (`opacity.loading`), padding_bottom `spacing.xs`
- **account_header_balance:** "£4,250.00" — `displayLarge`, `onPrimary`, Roboto Mono, font_weight 700, padding_bottom `spacing.xs`
- **Badges (horizontal stack, spacing `spacing.sm`):**
  - GBP badge: background `onPrimary` at `opacity.hover`, border_radius `radius.xs`, padding horizontal `spacing.sm` vertical `spacing.xs`, text `labelSmall` `onPrimary`
  - CHECKING badge: same pill style

### account_info_card — Routing Information
- **Position:** negative top margin of `spacing.md` (overlaps hero for visual continuity), margin_horizontal `spacing.md`
- **Background:** `surfaceContainerLowest`, border_radius `radius.lg`, elevation 3, padding `spacing.md`
- **IBAN row (space-between):**
  - Left col: "IBAN" label (`labelSmall`, `onSurfaceVariant`, letter_spacing 0.5) above "DE89 3704 0044 0532 0130 00" (`bodyMedium`, `onSurface`, Roboto Mono)
  - Right: content_copy icon `icon.md`, `primary` (tappable)
- **Divider:** `outlineVariant` horizontal rule (`border.thin`), margin_bottom `spacing.md`
- **BIC row:** same layout — "BIC / SWIFT" / "COBADEFFXXX" / copy icon

### action_row
- **Layout:** horizontal, spacing `spacing.sm`, padding_horizontal `spacing.md`, padding_bottom `spacing.lg`
- **btn_send_money:** variant=tonal, container `primaryContainer`, label `onPrimaryContainer`, icon send, border_radius `radius.md`, flex 1
- **btn_request_payment:** variant=outlined, border `outline` (`border.thin`), text `primary`, icon request_quote, flex 1
- **btn_download_statement:** variant=outlined, border `outline` (`border.thin`), text `primary`, icon download, flex 1

### Transaction Rows (detail_txn_row_1..5)
- **Background:** `surfaceContainerLowest`, border_radius `radius.md`, padding `spacing.md`, margin_horizontal `spacing.md`, elevation 1
- **Layout:** horizontal, align center, spacing `spacing.md`
- **Icon avatars (44×44 circles):** all five use the same neutral treatment — `surfaceContainerHigh` fill with the merchant glyph in `onSurfaceVariant` at `icon.md`. The glyph alone carries the category (shopping_basket / payments / bolt / subscriptions / local_cafe); it is not colour-coded.
- **Center stack:** merchant name (`bodyMedium`, `onSurface`) / date (`bodySmall`, `onSurfaceVariant`)
- **Right:** signed amount in Roboto Mono, `bodyLarge`, weight 600 — debits `error`; credits `primary`

---

## Interaction Patterns

| Target | Gesture | Outcome |
|---|---|---|
| Top app bar back arrow | Tap | Pop to accounts |
| copy_iban_button | Tap | Copies IBAN to clipboard; ibanCopied=true (brief toast) |
| copy_bic_button | Tap | Copies BIC to clipboard; bicCopied=true |
| btn_send_money | Tap | Navigate → send-money |
| btn_request_payment | Tap | Trigger payment request flow |
| btn_download_statement | Tap | Initiate PDF statement download; isDownloadingStatement=true |
| view_all_transactions_link | Tap | Navigate → transactions |
| Transaction rows | None (not tappable in this view) | — |

---

## Content Data

| Element | Value |
|---|---|
| Account name | Primary Checking |
| Balance | £4,250.00 |
| Currency | GBP |
| Account type | CHECKING |
| IBAN | DE89 3704 0044 0532 0130 00 |
| BIC/SWIFT | COBADEFFXXX |
| Txn 1 | Tesco Supermarket / 23 May 2026 / -£42.50 |
| Txn 2 | Salary Payment / 22 May 2026 / +£3,200.00 |
| Txn 3 | EDF Energy / 20 May 2026 / -£94.20 |
| Txn 4 | Amazon Prime / 18 May 2026 / -£8.99 |
| Txn 5 | Costa Coffee / 17 May 2026 / -£3.75 |

---

## Design Notes

- **Hero overlap:** the info card uses a negative top margin of `spacing.md` to visually bridge the hero to the scrollable content — a floating-card effect that is a Material Design 3 elevation pattern.
- **Colour contrast:** `onPrimary` text on the `primary` hero is the pair the palette guarantees at AA. Badge backgrounds use `onPrimary` at `opacity.hover` (8%) for subtle grouping without disrupting legibility.
- **Merchant avatars are neutral, not category-coloured:** the previous spec gave each merchant its own hue (red/green/orange/violet/deep-orange). This palette ships M3's five families and no more, and DESIGN.md retired the category-accent role when the PFM screens were removed. All avatars therefore share `surfaceContainerHigh` with an `onSurfaceVariant` glyph — the icon carries the category, and no invented tonal family has to be kept accessible across two themes and two contrast variants.
- **Copy affordance:** content_copy icons in `primary` are sized `icon.md` with `spacing.sm` padding to clear the 44 dp `touch_targets.minimum` floor.
- **Transaction direction coding:** debits use `error`, credits use `primary` — the palette's money pair. There is no green here by design ("never green-on-red, to stay calm and colour-blind-safe"), and the +/- sign carries the direction independently of hue.
- **Skeleton loading:** the hero keeps its `primary` fill during load; info card and actions skeleton with `surfaceVariant` blocks, maintaining spatial layout.
- **Typography ladder:** `displayLarge` (balance) → `titleLarge` (section heading) → `bodyMedium` (routing values) → `bodySmall` (dates/secondary) — four distinct steps ensuring clear hierarchy. Balance and routing numbers are set in Roboto Mono per the `amount` component contract.

---

_Generated by /idea export | 2026-08-03_
