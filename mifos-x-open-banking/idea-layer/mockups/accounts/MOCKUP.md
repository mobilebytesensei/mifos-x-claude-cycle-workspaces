# Visual Specification — My Accounts
**Feature:** accounts | **Flavor:** consumer

---

## Screen Layout

Top-to-bottom composition on a vertical scroll canvas bounded by a 5-tab bottom navigation bar:

```
┌────────────────────────────────────────┐
│  My Accounts                      [?]  │  ← accounts_header (h: 56dp)
├────────────────────────────────────────┤
│  🔍 Search by name, number or label [×]│  ← accounts_search (h: 56dp)
├────────────────────────────────────────┤
│  🏦 Mifos Bank UK           £10,430.50 │  ← bank_group_1_header
│     2 accounts                         │
├────────────────────────────────────────┤
│ ┌──────────────────────────────────┐   │
│ │▌ Primary Checking    [CHECKING]  │   │  ← account_card_1
│ │  £4,250.00                       │   │
│ │  ⊞ DE89 3704 0044 0532 0130 00   │   │
│ └──────────────────────────────────┘   │
│ ┌──────────────────────────────────┐   │
│ │▌ Holiday Savings      [SAVINGS]  │   │  ← account_card_2
│ │  £6,180.50                       │   │
│ │  ⊞ DE89 3704 0044 0532 0131 00   │   │
│ └──────────────────────────────────┘   │
├────────────────────────────────────────┤
│  🏦 Mifos Business UK        £2,050.00 │  ← bank_group_2_header
│     1 account                          │
├────────────────────────────────────────┤
│ ┌──────────────────────────────────┐   │
│ │▌ Business Current   [BUSINESS]   │   │  ← account_card_3
│ │  £2,050.00                       │   │
│ │  ⊞ DE89 3704 0044 0532 0132 00   │   │
│ └──────────────────────────────────┘   │
├────────────────────────────────────────┤
│  Total across 3 accounts   £12,480.50  │  ← total_balance_footer
├────────────────────────────────────────┤
│  [Home] [Accounts★] [Pay] [Cards] [⋯] │  ← bottom nav
└────────────────────────────────────────┘
                              [+] FAB     ← add_account_fab (fixed, bottom-right)
```

---

## Components

### accounts_header
- **Position:** Top of scroll content; padding_horizontal `spacing.md`, padding_top `spacing.lg`, padding_bottom `spacing.sm`
- **Layout:** Horizontal row, space-between, vertically centred
- **Left:** Text "My Accounts" — `headlineLarge` (32 sp, Roboto), color `onSurface`; a11y heading level 1
- **Right:** `help_outline` icon, `icon.md`, color `onSurfaceVariant`; tappable, focusable; on_click: `open_account_help`

### accounts_search
- **Position:** Below header; margin_horizontal `spacing.md`, padding_vertical `spacing.md`
- **Variant:** Outlined text field, border_radius `radius.xl` (pill)
- **Leading icon:** `search` (Material), color `onSurfaceVariant`
- **Trailing icon:** `close`, visible when field has input; clears query
- **Placeholder:** "Search by name, number or label" — color `onSurfaceVariant`
- **Background:** `surfaceContainer`; border `outline` idle (`border.thin`), `primary` focused (`border.focus`)
- **Interaction:** on_click triggers `search_accounts(query)`; a11y role: searchbox
- **States:** idle, hover, focus, focus_visible, disabled, error

### bank_group_1_header — Mifos Bank UK
- **Position:** Below search bar; padding_horizontal `spacing.md`, padding_top `spacing.lg`, padding_bottom `spacing.sm`
- **Layout:** Horizontal row, space-between
- **Left cluster:** `account_balance` icon `icon.sm` `primary` + vertical stack of "Mifos Bank UK" (`titleSmall`, `onSurface`) and "2 accounts" (`labelSmall`, `onSurfaceVariant`), `spacing.sm` gap between icon and text stack
- **Right:** Subtotal "£10,430.50" — `titleMedium`, Roboto Mono, color `primary`
- **A11Y:** heading level 2; full label covers name, count, and subtotal value

### account_card_1 — Primary Checking
- **Background:** `surfaceContainerLowest`, border_radius `radius.lg`, elevation 2, `border.thick` left-border `primary`
- **Padding:** `spacing.lg` all sides; margin_horizontal `spacing.md`, margin_bottom `spacing.md`
- **Header row (space-between):**
  - Left: "Primary Checking" — `titleMedium` (16 sp/600), color `onSurface`
  - Right: badge box — `secondaryContainer` bg, `radius.xs`; "CHECKING" — `labelSmall` (11 sp/500), color `onSecondaryContainer`
- **Balance row:** "£4,250.00" — `displaySmall` (36 sp/600), Roboto Mono, color `primary`; padding_bottom `spacing.sm`
- **IBAN row:** `account_box` icon `icon.xs` `onSurfaceVariant` + "DE89 3704 0044 0532 0130 00" — `bodySmall` (12 sp), `onSurfaceVariant`, Roboto Mono; `spacing.sm` gap
- **A11Y:** role button, label: "Primary Checking account, balance four thousand two hundred fifty pounds, tap to view details"
- **On tap:** navigate → account-detail (account_id: acc_checking_primary)
- **States:** idle, hover, focus_visible, pressed

### account_card_2 — Holiday Savings
- **Left-border accent:** `border.thick` `primary`
- **Balance:** "£6,180.50" — `displaySmall`, Roboto Mono, color `primary`
- **Badge:** "SAVINGS" — `secondaryContainer` bg, `labelSmall`, color `onSecondaryContainer`
- **IBAN:** "DE89 3704 0044 0532 0131 00" Roboto Mono `onSurfaceVariant`
- **On tap:** navigate → account-detail (account_id: acc_savings_goal)
- **A11Y:** "Holiday Savings account, balance six thousand one hundred eighty pounds fifty, tap to view details"

### bank_group_2_header — Mifos Business UK
- **Layout:** Mirrors bank_group_1_header pattern
- **Left cluster:** `account_balance` icon `icon.sm` `primary` + "Mifos Business UK" `titleSmall` `onSurface` + "1 account" `labelSmall` `onSurfaceVariant`
- **Right:** Subtotal "£2,050.00" — `titleMedium`, Roboto Mono, color `primary`
- **A11Y:** heading level 2

### account_card_3 — Business Current
- **Left-border accent:** `border.thick` `primary`
- **Balance:** "£2,050.00" — `displaySmall`, Roboto Mono, color `primary`
- **Badge:** "BUSINESS" — `secondaryContainer` bg, `labelSmall`, color `onSecondaryContainer`
- **IBAN:** "DE89 3704 0044 0532 0132 00" Roboto Mono `onSurfaceVariant`
- **On tap:** navigate → account-detail (account_id: acc_business_main)
- **A11Y:** "Business Current account, balance two thousand fifty pounds, tap to view details"

### footer_divider
- **Color:** `outlineVariant` (`border.thin`); margin_horizontal `spacing.md`, margin_vertical `spacing.xs`
- **A11Y:** role separator

### total_balance_footer
- **Background:** `surfaceContainer`, border_radius `radius.md`, padding `spacing.md`
- **Margin:** horizontal `spacing.md`, top `spacing.xs`, bottom `spacing.xxl` + `spacing.xl` (clears FAB + nav)
- **Row (space-between):**
  - Left: "Total across 3 accounts" — `bodyMedium` (14 sp), color `onSurfaceVariant`
  - Right: "£12,480.50" — `titleLarge` (22 sp/700), Roboto Mono, color `primary`
- **A11Y:** role text, "Total: twelve thousand four hundred eighty pounds fifty pence across three accounts"

### add_account_fab
- **Fixed position:** above the bottom nav bar, right `spacing.md`
- **Size:** 56×56 dp, border_radius `radius.lg`
- **Style:** container `primary`, `add` icon `icon.md` color `onPrimary`, elevation 6
- **On tap:** `request_new_account`
- **A11Y:** role button, label: "Request a new account", hint: "Opens the account request form"
- **States:** idle, hover, focus_visible, pressed, disabled

---

## Interaction Patterns

| Target                | Gesture | Outcome                                              |
|-----------------------|---------|------------------------------------------------------|
| accounts_search       | Tap / type | Filter `filteredAccounts` + regroup `groupedByBank`; trailing `close` clears query |
| account_card_1        | Tap     | Navigate → account-detail / acc_checking_primary     |
| account_card_2        | Tap     | Navigate → account-detail / acc_savings_goal         |
| account_card_3        | Tap     | Navigate → account-detail / acc_business_main        |
| add_account_fab       | Tap     | Opens account request form                           |
| accounts_help_icon    | Tap     | Opens account help overlay                           |
| Bottom nav            | Tap     | Replace top-level destination                        |

---

## Loading State (skeleton)

- accounts_header and accounts_search remain visible and interactive
- 3 skeleton boxes (120 dp tall, `surfaceVariant` bg, `radius.lg`, `spacing.md` horizontal margin, `spacing.md` between) replace all account cards and bank group headers
- 1 shorter skeleton box (48 dp, `surfaceVariant` bg, `radius.md`, `spacing.md` margin) replaces total_balance_footer
- Shimmer animation: `shimmer_duration: short4`; reduced motion fallback: static placeholder

---

## Empty State

- accounts_header visible, search bar hidden
- Centred card: illustration `no_accounts`, title "No accounts found" (`titleMedium`), message "You don't have any accounts yet. Request a new account to get started." (`bodyMedium`), CTA "Request Account" → `request_new_account`

---

## Error State

- accounts_header visible, search bar hidden
- Centred card: icon `error_outline` (`error`), title "Could not load accounts", message "We were unable to fetch your account list. Please check your connection and try again.", CTA "Retry" → `retry_load`

---

## Content Data

| Element                   | Value                           |
|---------------------------|---------------------------------|
| Bank group 1 name         | Mifos Bank UK                   |
| Bank group 1 account count| 2 accounts                      |
| Bank group 1 subtotal     | £10,430.50                      |
| Account 1 name            | Primary Checking                |
| Account 1 type            | CHECKING                        |
| Account 1 balance         | £4,250.00                       |
| Account 1 IBAN            | DE89 3704 0044 0532 0130 00     |
| Account 2 name            | Holiday Savings                 |
| Account 2 type            | SAVINGS                         |
| Account 2 balance         | £6,180.50                       |
| Account 2 IBAN            | DE89 3704 0044 0532 0131 00     |
| Bank group 2 name         | Mifos Business UK               |
| Bank group 2 account count| 1 account                       |
| Bank group 2 subtotal     | £2,050.00                       |
| Account 3 name            | Business Current                |
| Account 3 type            | BUSINESS                        |
| Account 3 balance         | £2,050.00                       |
| Account 3 IBAN            | DE89 3704 0044 0532 0132 00     |
| Total balance             | £12,480.50                      |
| Total account count       | 3                               |

---

## Design Notes

- **No filter tabs:** the previous account-type filter chip row has been removed. Discovery and narrowing is handled by the `accounts_search` free-text field, which searches across name, number, and label in real time.
- **Bank-grouped layout:** accounts are grouped into hierarchical sections by institution. Each section header shows bank icon, name, account count, and subtotal, giving instant portfolio-level context before reading individual cards.
- **Account type is a label, not a colour:** the previous spec gave each type its own left-border hue (green / teal / amber) and had already needed an A11Y-002 fix because the amber failed contrast when it reached text. All three cards now share a `primary` left accent, and the type is carried by the `CHECKING` / `SAVINGS` / `BUSINESS` badge. That removes two colours the palette never shipped, removes the contrast exception, and matches DESIGN.md's rule that `tertiary` means warning — a business account is not a warning.
- **Balances in `primary`:** every displayed balance is a positive figure, and `primary` is this system's credit colour. Amounts and IBANs are set in Roboto Mono per the `amount` component contract so figures and account numbers align down the column.
- **Typography hierarchy:** `headlineLarge` (screen title) > `displaySmall` (balance amounts) > `titleMedium` (account names) > `titleSmall` (bank institution names) > `bodySmall` (IBAN text) — five clear levels, all Roboto.
- **Spacing rhythm:** `spacing.md` horizontal gutters on all cards and section headers; `spacing.md` margin below each card; `spacing.lg` top padding on section headers.
- **Accessibility:** every account card has a full-sentence a11y label covering name, balance, and action hint. Bank group headers expose heading level 2. The search field exposes role searchbox. IBAN text is monospace for digit-grouping legibility.
- **Bottom nav:** Accounts tab active (icon: account_balance); the FAB is positioned to clear the nav bar.

---

_Generated by /idea export | 2026-08-03_
