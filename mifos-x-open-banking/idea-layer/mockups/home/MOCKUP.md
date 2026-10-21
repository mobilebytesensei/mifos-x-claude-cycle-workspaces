# MOCKUP — Home Dashboard

| Field   | Value    |
|---------|----------|
| Feature | home     |
| Flavor  | consumer |

---

## Screen Layout

The Home Dashboard is a vertically scrollable column on `surface` background. It is anchored by a bottom navigation bar (5 tabs) that persists across all scroll positions. The scroll content hierarchy from top to bottom:

1. Greeting text + date (padding-top `spacing.lg`, horizontal `spacing.md`)
2. Primary account hero card (horizontal margin `spacing.md`)
3. Total balance chip (horizontal margin `spacing.md`, margin-top `spacing.md`)
4. Recent Transactions section header (horizontal `spacing.md`, top `spacing.md`, bottom `spacing.md`)
5. Three transaction rows (horizontal margin `spacing.md`, gap `spacing.sm`)
6. Services section title (horizontal `spacing.md`, top `spacing.md`, bottom `spacing.md`)
7. Services grid — 3 tiles in a horizontal row (horizontal `spacing.md`)
8. Bottom spacer (`spacing.lg`) above the bottom nav bar

---

## Components

### Greeting Block

**greeting_text**
- Content: "Good morning, Alex"
- Style: `headlineMedium` typography, color `primary`, padding-top `spacing.lg`, padding-horizontal `spacing.md`
- Data-driven: personalized via `HomeScreenState.greetingName` ("Alex")
- Accessibility: role=heading level=1

**greeting_date**
- Content: "Monday, 25 May 2026"
- Style: `bodyMedium` typography, color `onSurfaceVariant`, padding-horizontal `spacing.md`, padding-bottom `spacing.md`

---

### Primary Account Hero Card

**primary_account_card**
- Container: background `primary`, border-radius `radius.lg`, padding `spacing.lg`, horizontal margin `spacing.md`, elevation 4
- Accessibility: role=region, label="Primary Checking account card"

Contents from top to bottom:

**account_card_label**
- Content: "Primary Checking"
- Style: `labelLarge` typography, color `onPrimary` at reduced emphasis (`opacity.loading`)

**account_card_balance**
- Content: "£4,250.00"
- Style: `displaySmall` typography, Roboto Mono, color `onPrimary`, padding-top `spacing.sm`, padding-bottom `spacing.xs`
- Accessibility: label="Account balance: four thousand two hundred fifty pounds"

**account_card_iban**
- Content: "•••• •••• •••• 0130"
- Style: `bodyMedium` typography, Roboto Mono, color `onPrimary` at reduced emphasis, padding-bottom `spacing.md`
- Accessibility: label="Account number ending 0130"

**quick_actions_row** — Horizontal row of three equal-flex buttons:

| Button               | ID                   | Style                                                              | Target       |
|----------------------|----------------------|--------------------------------------------------------------------|--------------|
| "Send Money"         | btn_send_money       | Filled `onPrimary` container, text `primary`, radius `radius.md`   | send-money   |
| "Beneficiaries"      | btn_add_beneficiary  | Outlined `onPrimary` border, text `onPrimary`, radius `radius.md`  | beneficiaries|
| "View Cards"         | btn_view_cards       | Outlined `onPrimary` border, text `onPrimary`, radius `radius.md`  | cards        |

All three: `labelMedium` typography, padding-horizontal `spacing.md`, padding-vertical `spacing.sm`, flex=1.

---

### Total Balance Chip

**total_balance_chip**
- Container: background `primaryContainer`, border-radius `radius.md`, padding-horizontal `spacing.md`, padding-vertical `spacing.sm`, margin-horizontal `spacing.md`, margin-top `spacing.md`
- Row contents: account_balance_wallet icon (`icon.xs`, `onPrimaryContainer`) + "Total across 3 accounts: £12,480.50" text (`labelMedium`, `onPrimaryContainer`, figure in Roboto Mono)
- Accessibility: label="Total across 3 accounts: twelve thousand four hundred eighty pounds fifty pence"

---

### Recent Transactions Section

**recent_transactions_header**
- Horizontal row: "Recent Transactions" heading (left) + "View All" link (right)
- Heading: `titleLarge` typography, color `onSurface`, role=heading level=2
- Link: "View All", `labelMedium`, color `primary`; navigates to transactions

**transaction_row_1 — Tesco Supermarket**
- Card: background `surfaceContainerLowest`, border-radius `radius.md`, padding `spacing.md`, margin-horizontal `spacing.md`, margin-bottom `spacing.sm`, elevation 1
- Left icon container: 44×44 dp circle, background `surfaceContainerHigh`, contains shopping_cart icon (`icon.md`, `onSurfaceVariant`)
- Center column: "Tesco Supermarket" (`bodyLarge`, `onSurface`) + "23 May 2026 · Groceries" (`bodySmall`, `onSurfaceVariant`)
- Right column: "-£42.50" (`bodyLarge`, `error`, Roboto Mono, weight 600) + "DEBIT" badge (`labelSmall`, `onErrorContainer`, background `errorContainer`, border-radius `radius.xs`)

**transaction_row_2 — Salary Payment**
- Card: same card style as row_1
- Left icon container: 44×44 dp circle, background `surfaceContainerHigh`, contains payments icon (`icon.md`, `onSurfaceVariant`)
- Center column: "Salary Payment" (`bodyLarge`, `onSurface`) + "22 May 2026 · Income" (`bodySmall`, `onSurfaceVariant`)
- Right column: "+£3,200.00" (`bodyLarge`, `primary`, Roboto Mono, weight 600) + "CREDIT" badge (`labelSmall`, `onPrimaryContainer`, background `primaryContainer`, border-radius `radius.xs`)

**transaction_row_3 — EDF Energy**
- Card: same card style as row_1
- Left icon container: 44×44 dp circle, background `surfaceContainerHigh`, contains bolt icon (`icon.md`, `onSurfaceVariant`)
- Center column: "EDF Energy" (`bodyLarge`, `onSurface`) + "20 May 2026 · Utilities" (`bodySmall`, `onSurfaceVariant`)
- Right column: "-£94.20" (`bodyLarge`, `error`, Roboto Mono, weight 600) + "DEBIT" badge (`labelSmall`, `onErrorContainer`, background `errorContainer`)

---

### Services Grid

**services_section_title**
- Content: "Services"
- Style: `titleLarge` typography, color `onSurface`, padding-horizontal `spacing.md`, padding-top `spacing.md`, padding-bottom `spacing.md`

**services_grid** — Horizontal row, spacing `spacing.md`, padding-horizontal `spacing.md`, padding-bottom `spacing.md`:

| Tile                  | ID                      | Background            | Icon (size/color)                              | Label                          |
|-----------------------|-------------------------|-----------------------|------------------------------------------------|--------------------------------|
| Standing Orders       | service_standing_orders | `secondaryContainer`  | repeat, `icon.md`, `onSecondaryContainer`      | "Standing Orders"              |
| ATM & Branches        | service_atm_locator     | `secondaryContainer`  | location_on, `icon.md`, `onSecondaryContainer` | "ATM & Branches"               |
| FX Rates              | service_fx_rates        | `secondaryContainer`  | currency_exchange, `icon.md`, `onSecondaryContainer` | "FX Rates"               |

All tiles: border-radius `radius.lg`, padding `spacing.md`, flex=1; icon above label with padding-top `spacing.sm`; `labelMedium` typography, label colour `onSecondaryContainer`.

---

### Bottom Navigation Bar

5 tabs, always visible, positioned at screen bottom. Container `surfaceContainer`, active item `primary` per the `bottom_nav` component contract:
- **Home** (home icon, active=true) — `primary` indicator
- **Accounts** (account_balance icon) — target: accounts
- **Pay** (send icon) — target: send-money
- **Cards** (credit_card icon) — target: cards
- **More** (more_horiz icon) — target: more

---

## Interaction Patterns

| Element                 | Gesture | Outcome                                                         |
|-------------------------|---------|-----------------------------------------------------------------|
| btn_send_money          | Tap     | Navigate to `send-money` screen                                 |
| btn_add_beneficiary     | Tap     | Navigate to `beneficiaries` screen                              |
| btn_view_cards          | Tap     | Navigate to `cards` screen                                      |
| view_all_link           | Tap     | Navigate to `transactions` screen                               |
| service_standing_orders | Tap     | Navigate to `standing-orders` screen                            |
| service_atm_locator     | Tap     | Navigate to `atm-locator` screen                                |
| service_fx_rates        | Tap     | Navigate to `fx-rates` screen                                   |
| nav bottom bar tabs     | Tap     | Tab switch to respective screen                                 |
| Error card Retry button | Tap     | Fires `RetryLoad` event → `loadDashboardData()`                 |
| Empty card "Set Up Account" | Tap | Navigate to `accounts` screen                                  |

**Loading state:**
- Greeting text and date remain visible.
- Account card region is replaced by a `surfaceVariant` skeleton box (height 180 dp, border-radius `radius.lg`, margin-horizontal `spacing.md`).
- Two transaction placeholder boxes shown below (height 72 dp each, border-radius `radius.md`, `surfaceVariant`, margin-top `spacing.sm`).
- Skeleton boxes do not animate — static fills for the initial load pass.

**Error state:**
- Greeting block visible.
- Error card appears: icon `error_outline` (`error`) + title "Could not load your account" + message "We were unable to fetch your account data. Check your connection and try again." + "Retry" button.

**Empty state:**
- Greeting block visible.
- Empty card appears: illustration `account_empty` + title "No accounts yet" + message "Your accounts will appear here once your profile is set up." + "Set Up Account" button.

---

## Content Data

| Component              | Content Value                              |
|------------------------|--------------------------------------------|
| greeting_text          | "Good morning, Alex"                       |
| greeting_date          | "Monday, 25 May 2026"                      |
| account_card_label     | "Primary Checking"                         |
| account_card_balance   | "£4,250.00"                               |
| account_card_iban      | "•••• •••• •••• 0130"                      |
| total_balance_text     | "Total across 3 accounts: £12,480.50"     |
| txn1_merchant          | "Tesco Supermarket"                        |
| txn1_date              | "23 May 2026 · Groceries"                  |
| txn1_amount            | "-£42.50"                                  |
| txn2_merchant          | "Salary Payment"                           |
| txn2_date              | "22 May 2026 · Income"                     |
| txn2_amount            | "+£3,200.00"                              |
| txn3_merchant          | "EDF Energy"                               |
| txn3_date              | "20 May 2026 · Utilities"                  |
| txn3_amount            | "-£94.20"                                  |
| service_standing_orders| "Standing Orders"                          |
| service_atm_label      | "ATM & Branches"                           |
| service_fx_label       | "FX Rates"                                 |

---

## Design Notes

**Color usage:**
- The `primary` hero card is the visual anchor of the screen — it carries the most important data (balance) and the primary user actions. Reverse-colour text (`onPrimary` at full and reduced emphasis) preserves hierarchy inside the card.
- Transaction amounts use the palette's money pair: `error` for debits, `primary` for credits — **not** a red/green pair. DESIGN.md is explicit that credit uses the primary blue "never green-on-red, to stay calm and colour-blind-safe". The coloured amount is supported by a DEBIT / CREDIT badge drawn from the matching container role, so the distinction survives without colour entirely.
- **Service tiles share one container role.** They previously carried three invented tints (purple / teal / amber) to give "category identity"; each tile already has an icon and a text label doing that job, and none of those three hues exist in this palette. All three now use `secondaryContainer` / `onSecondaryContainer`.
- The total balance chip uses `primaryContainer`, so it reads as part of the account-card family without competing with the hero.

**Typography:**
- `displaySmall` (account balance in the hero card) is the typographic climax of the screen — the largest text, in `onPrimary` on `primary`, establishes immediate visual priority. It is set in Roboto Mono, as is every other figure on the screen, per the `amount` component contract.
- `headlineMedium` (greeting) anchors the screen's personal register; the `primary` colour reinforces session identity.
- `titleLarge` for section headers ("Recent Transactions", "Services") uses neutral `onSurface` to avoid competing with the greeting and hero card.
- `labelSmall` for DEBIT/CREDIT badges provides dense information at minimal size without visual noise.
- Roboto throughout — one family, hierarchy carried by the type scale.

**Spacing:**
- Consistent `spacing.md` horizontal margins create a unified canvas width for all major elements.
- `spacing.sm` gap between transaction cards provides clear item separation without excessive whitespace.
- `spacing.md` tile gap in the services grid creates a tight-but-breathable 3-column layout.
- `spacing.lg` bottom spacer ensures last-scrolled content is not clipped by the bottom nav bar.

**Accessibility:**
- Greeting is role=heading level=1 — establishes the page title for screen readers.
- Section headers (Recent Transactions, Services) are role=heading level=2 — proper document outline.
- Account card is role=region with a descriptive label — allows VoiceOver/TalkBack users to navigate to the account block directly.
- Transaction rows are role=listitem with full aria labels reading the merchant, amount, and date (e.g. "Tesco Supermarket, debit forty-two pounds fifty, 23 May 2026").
- The DEBIT/CREDIT badge supplements the colour coding — the badge text ensures colour-blind users get an explicit categorical signal (WCAG 1.4.1).
- All navigation buttons carry explicit `hint` attributes describing the destination (e.g. "Opens the send money screen").

---

_Generated by /idea export | 2026-08-03_
