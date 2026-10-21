# Visual Specification — Transaction History
**Feature:** transactions | **Flavor:** consumer

---

## Screen Layout

Vertical scroll with top app bar ("Transactions" + back + filter_list action icon):

```
┌────────────────────────────────────┐
│ ← Transactions               [≡]  │  ← top app bar
├────────────────────────────────────┤
│ 🔍 Search by merchant, amount, date│  ← search_bar (bg `surfaceContainerLow`)
├────────────────────────────────────┤
│ 📅 Last 30 Days              ▼     │  ← date_range_picker
├────────────────────────────────────┤
│ [All] [Debit] [Credit] [Pending]   │  ← filter_chips_row
├────────────────────────────────────┤
│ ┌──────────────────────────────┐   │
│ │  Spent this month │ Received │   │  ← monthly_summary_card
│ │  £1,240.30        │ £3,200.00│   │    (`surfaceContainer`)
│ └──────────────────────────────┘   │
├────────────────────────────────────┤
│  25 May 2026                       │  ← transactions_date_group_header
│ ┌──────────────────────────────┐   │
│ │ [T] Tesco Supermarket        │   │
│ │     25 May 2026 · [Groceries]│  -£42.50 │  ← txn_list_row_1
│ └──────────────────────────────┘   │
│  24 May 2026                       │
│ ┌──────────────────────────────┐   │
│ │ [💰] Salary Payment          │   │
│ │     24 May 2026 · [Income]   │ +£3,200.00 │  ← txn_list_row_2
│ └──────────────────────────────┘   │
│  23 May 2026                       │
│ ┌──────────────────────────────┐   │
│ │ [E] EDF Energy               │   │
│ │     23 May 2026 · [Utilities]│  -£94.20 │  ← txn_list_row_3
│ └──────────────────────────────┘   │
│        Load More Transactions      │  ← load_more_button
├────────────────────────────────────┤
│  [Home] [Accounts*] [Pay] [Cards] [More] │
└────────────────────────────────────┘
```

---

## Components

### search_bar
- **Style:** variant=search, background `surfaceContainerLow`, border_radius `radius.md`
- **Padding:** horizontal `spacing.md`, vertical `spacing.md`; margin_horizontal `spacing.md`, margin_top `spacing.md`
- **Leading icon:** search (`icon.md`, `onSurfaceVariant`)
- **Trailing icon:** mic (`icon.md`, `onSurfaceVariant`)
- **Placeholder:** "Search by merchant, amount, date..." — `onSurfaceVariant`

### date_range_picker
- **Style:** background `surfaceContainerLow`, border_radius `radius.md`, padding horizontal `spacing.md` vertical `spacing.md`, margin_horizontal `spacing.md`
- **Row layout:** horizontal, space-between
- **Left:** date_range icon (`icon.sm`, `primary`) + "Last 30 Days" text (`bodyMedium`, `onSurface`)
- **Right:** expand_more icon (`icon.sm`, `onSurfaceVariant`)
- Entire component is tappable (opens date range dialog)

### filter_chips_row
- **Horizontal scroll, spacing `spacing.sm`, padding_horizontal `spacing.md`**
- **Active chip (All):** filled, container `primary`, text `onPrimary`, border_radius `radius.lg`, padding horizontal `spacing.md` vertical `spacing.sm`
- **Inactive chips (Debit, Credit, Pending):** outlined, border `outline` (`border.thin`), text `onSurfaceVariant`, same radius/padding
- Role: radio group (a11y)

### monthly_summary_card
- **Background:** `surfaceContainer`, border_radius `radius.lg`, padding `spacing.md`, margin_horizontal `spacing.md`
- **Two columns separated by a `border.thin` × 40 dp vertical divider (`outlineVariant`):**
  - **Left (spent_col):** "Spent this month" label (`labelSmall`, `onSurfaceVariant`, letter_spacing 0.4) above "£1,240.30" (`titleLarge`, `error`, Roboto Mono, weight 700)
  - **Right (received_col):** "Received" label above "£3,200.00" (`titleLarge`, `primary`, Roboto Mono, weight 700)

### transactions_date_group_header
- **"25 May 2026"** — `labelMedium`, `onSurfaceVariant`, letter_spacing 0.5, padding_horizontal `spacing.md`

### Transaction Row (txn_list_row_1 — Tesco Supermarket)
- **Background:** `surfaceContainerLowest`, border_radius `radius.md`, padding `spacing.md`, margin_horizontal `spacing.md`, elevation 1
- **Layout:** horizontal, align center, spacing `spacing.md`
- **Merchant logo:** 40×40 circle, background `surfaceContainerHigh`, glyph `onSurfaceVariant`
- **Info stack (flex 1):**
  - "Tesco Supermarket" — `bodyMedium`, `onSurface`, weight 500
  - Meta row: "25 May 2026" (`bodySmall`, `onSurfaceVariant`) + "·" separator + "Groceries" badge (`secondaryContainer` bg, `onSecondaryContainer` text, `labelSmall`)
- **Amount:** "-£42.50" — `bodyLarge`, `error`, Roboto Mono, weight 600

### Transaction Row (txn_list_row_2 — Salary Payment)
- **Merchant logo:** 40×40 circle, background `surfaceContainerHigh`, glyph `onSurfaceVariant`
- **Name:** "Salary Payment", **Date:** "24 May 2026"
- **Category badge:** "Income" — `secondaryContainer` bg, `onSecondaryContainer` text
- **Amount:** "+£3,200.00" — `bodyLarge`, `primary`, Roboto Mono, weight 600

### Transaction Row (txn_list_row_3 — EDF Energy)
- **Merchant logo:** 40×40 circle, background `surfaceContainerHigh`, glyph `onSurfaceVariant`
- **Name:** "EDF Energy", **Date:** "23 May 2026"
- **Category badge:** "Utilities" — `secondaryContainer` bg, `onSecondaryContainer` text
- **Amount:** "-£94.20" — `bodyLarge`, `error`, Roboto Mono, weight 600

### load_more_button
- **Variant:** text, text_color `primary`, typography `labelMedium`
- **Alignment:** center (align_self: center), padding_vertical `spacing.md`

---

## Interaction Patterns

| Target | Gesture | Outcome |
|---|---|---|
| search_bar | Tap / type | isSearching=true; skeleton rows during search; results replace list |
| date_range_picker | Tap | Opens date range dialog; DateRangeChanged event on confirm |
| filter_all | Tap | activeFilter=ALL; all transactions shown |
| filter_debit | Tap | activeFilter=DEBIT; re-fetches with type=DEBIT |
| filter_credit | Tap | activeFilter=CREDIT; re-fetches with type=CREDIT |
| filter_pending | Tap | activeFilter=PENDING; re-fetches with type=PENDING |
| txn_list_row_1 | Tap | Navigate → /transactions/txn_20260525_001 |
| txn_list_row_2 | Tap | Navigate → /transactions/txn_20260524_001 |
| txn_list_row_3 | Tap | Navigate → /transactions/txn_20260523_001 |
| load_more_button | Tap | LoadMore event; currentPage++ ; appends next 20 transactions |
| Top app bar filter icon | Tap | open_advanced_filter (date + type sheet) |

---

## Content Data

| Element | Value |
|---|---|
| Date range | Last 30 Days |
| Spent this month | £1,240.30 |
| Received this month | £3,200.00 |
| Txn 1 | Tesco Supermarket / Groceries / -£42.50 / 25 May 2026 |
| Txn 2 | Salary Payment / Income / +£3,200.00 / 24 May 2026 |
| Txn 3 | EDF Energy / Utilities / -£94.20 / 23 May 2026 |
| Transaction IDs | txn_20260525_001, txn_20260524_001, txn_20260523_001 |
| Page size | 20 per load |

---

## Design Notes

- **Summary card surface:** `surfaceContainer` sits one step up the tonal ladder from the row cards, so the summary reads as grouped without introducing a tinted brand wash behind financial figures. The previous 3% purple tint belonged to a palette this system no longer uses.
- **Money direction:** spent is `error`, received is `primary` — the palette's declared money pair. No green appears anywhere in this list, and the +/- sign carries direction independently of hue so the column survives colour-blind reading.
- **Category badges are one neutral family, not per-category hues:** every badge uses `secondaryContainer`/`onSecondaryContainer`. Groceries, Utilities, and Income previously each carried an invented tint (green, orange, green). Category is text, and text is what makes it scannable; giving each category its own colour family would mean maintaining new accessible pairs across two themes and two contrast variants to restate a label already on screen.
- **Merchant avatars:** all use `surfaceContainerHigh` with an `onSurfaceVariant` glyph, matching account-detail so a merchant looks the same wherever it appears.
- **Date group headers:** `labelMedium` with letter_spacing 0.5 in `onSurfaceVariant` — clearly separated from card content without a background divider, keeping the list light.
- **Search + filter combo:** the search bar, date picker, and filter chips are all persistent across states (visible in loading, content, and searching), so users can refine immediately without waiting for results.
- **Load more vs infinite scroll:** an explicit "Load More" button gives users control over data loading — important on metered mobile connections.
- **a11y:** each transaction row has a full-sentence label read by TalkBack: "Tesco Supermarket, debit forty-two pounds fifty, Groceries, 25 May 2026. Tap for details." Filter chips use role=radio with selected state.

---

_Generated by /idea export | 2026-08-03_
