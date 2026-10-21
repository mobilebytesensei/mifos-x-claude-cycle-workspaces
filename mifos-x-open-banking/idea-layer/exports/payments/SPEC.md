# SPEC — Payments Hub

| Field         | Value              |
|---------------|--------------------|
| Feature       | payments           |
| Flavor        | consumer           |
| Status        | enriched           |
| Quality Score | 86/100             |
| ViewModel     | PaymentsViewModel  |
| Archetype     | dashboard          |
| Schema        | 4.0                |
| Contract      | 2.0.0              |
| Cluster       | payment-initiation |

---

## Overview

The Payments hub is the landing destination of the Pay bottom-navigation tab (order 2). It presents
seven square tiles — one per HSBC UK OBIE Personal payment rail — and routes each tap to that rail's
own screen. The hub makes no network call and holds no state beyond the static tile list, which is
known at compile time.

The seven rails diverge in endpoint family, mandatory fields, amount field name, charge model, status
ladder, and encoding. Two of those shapes are proven mutually exclusive: `InstructedAmount` on a
domestic standing order returns U005 "Field is not expected", and `FirstPaymentAmount` on an
international standing order likewise (both directions tested in PISP-tests R15). A single
parameterised form would hold seven contradictory contracts; a hub of seven tiles is the shape the
evidence dictates.

This is also the only surface in the app where a PSU sees all seven rails as distinct things. The
one-line description under each tile is not decoration — it is the only moment where a user can
tell "scheduled" (one future date) from "standing order" (a recurring mandate) before committing to
a form they cannot back out of cheaply. Those two are the pair users genuinely confuse.

---

## Screens

| ID       | Name     | ViewModel         | State(s) | Archetype |
|----------|----------|-------------------|----------|-----------|
| payments | Payments | PaymentsViewModel | content  | dashboard |

**Shell:** Pay tab is bottom-nav order 2; the bottom bar stays visible at all scroll positions. No
top app bar navigation icon (landing tab, not a pushed route). No FAB.

---

## Components

| ID                             | Type      | Description                                        |
|--------------------------------|-----------|----------------------------------------------------|
| hub_heading                    | text      | "How do you want to pay?" — `titleMedium`, `onSurface` |
| payment_type_grid              | grid      | 3-column, gap 12dp, square items (aspect 1:1)       |
| tile_domestic_single           | grid_item | "Pay someone" — icon `payments`, routes to pay-domestic-single |
| tile_domestic_scheduled        | grid_item | "Pay on a date" — icon `event`, routes to pay-domestic-scheduled |
| tile_domestic_standing_order   | grid_item | "Standing order" — icon `repeat`, routes to pay-domestic-standing-order |
| tile_international_single      | grid_item | "Pay abroad" — icon `public`, routes to pay-international-single |
| tile_international_scheduled   | grid_item | "Pay abroad on a date" — icon `public_off`, routes to pay-international-scheduled |
| tile_international_standing_order | grid_item | "Overseas standing order" — icon `currency_exchange`, routes to pay-international-standing-order |
| tile_vrp_mandate               | grid_item | "Variable payments" — icon `all_inclusive`, routes to pay-vrp-mandate |
| amend_notice                   | text      | OBL Customer Experience Guidelines notice — `bodySmall`, `onSurfaceVariant` |

Seven tiles, three per row; the seventh (VRP) sits alone on row 3, left-aligned. Tablet and desktop
widen the grid to 4 columns at 600dp+.

---

## States

Initial state: `content`. This is the **only** state. No loading, empty, error, or
unauthenticated variant exists, and none must be added:

| State   | Rendering                                      |
|---------|------------------------------------------------|
| content | Static seven-tile grid with `amend_notice` below |

The tile list is compile-time static; nothing here can fail. Tiles are never hidden on eligibility
grounds — the hub does not know which account the PSU will choose, and eligibility depends on that
choice. A hidden tile would leave a PSU unable to discover why a type is unavailable; the constraint
surfaces inside the type screen, at the debtor-account picker (FR-018).

States that must not be added: `loading` (nothing to load), `empty` (seven tiles, always, for every
PSU), `error` (no call is made), `unauthenticated` (no call returns 401 here).

---

## State Model

**ViewModel:** `PaymentsViewModel` — injects nothing. The hub makes no network call and reads no
repository. A ViewModel is declared only to keep navigation events off the composable, matching the
app's MVI pattern.

**UI state type:** `PaymentsUiState`

| State   | Fields | Notes                                         |
|---------|--------|-----------------------------------------------|
| Content | (none) | The tile list is a compile-time constant; no field is needed |

```kotlin
sealed interface PaymentsUiState {
    data object Content : PaymentsUiState
}
```

**Actions:**

| Action          | Signature                              | Effect                                      |
|-----------------|----------------------------------------|---------------------------------------------|
| OpenPaymentType | `fun openPaymentType(type: PaymentType)` | Emits `NavigateToPaymentType` event        |

`PaymentType` is a seven-value enum:
`DOMESTIC_SINGLE`, `DOMESTIC_SCHEDULED`, `DOMESTIC_STANDING_ORDER`,
`INTERNATIONAL_SINGLE`, `INTERNATIONAL_SCHEDULED`, `INTERNATIONAL_STANDING_ORDER`, `VRP_MANDATE`.

**Events:**

| Event                  | Params               | Consumer             |
|------------------------|----------------------|----------------------|
| NavigateToPaymentType  | `type: PaymentType`  | NavHost edge handler |

**DI:** (none) — PaymentsViewModel injects nothing.

---

## Navigation

### Entry Points

| Source                     | Trigger                               | Params |
|----------------------------|---------------------------------------|--------|
| app_shell_bottom_nav (Pay) | PSU taps the Pay tab (bottom-nav #2) | (none) |

### Routing Table — All Seven Tiles

| Tile Component                    | PaymentType                | Target Route                  | Downstream Screen         |
|-----------------------------------|----------------------------|-------------------------------|---------------------------|
| tile_domestic_single              | DOMESTIC_SINGLE            | pay-domestic-single           | Single payment form        |
| tile_domestic_scheduled           | DOMESTIC_SCHEDULED         | pay-domestic-scheduled        | Scheduled payment form     |
| tile_domestic_standing_order      | DOMESTIC_STANDING_ORDER    | pay-domestic-standing-order   | Standing order form        |
| tile_international_single         | INTERNATIONAL_SINGLE       | pay-international-single      | International payment form |
| tile_international_scheduled      | INTERNATIONAL_SCHEDULED    | pay-international-scheduled   | Int'l scheduled form       |
| tile_international_standing_order | INTERNATIONAL_STANDING_ORDER | pay-international-standing-order | Int'l standing order form |
| tile_vrp_mandate                  | VRP_MANDATE                | pay-vrp-mandate               | Mandate roster (a LIST, not a form) |

All seven targets resolve to real feature screens; navigation_verification confirmed 7 of 7 on
2026-08-07. The superseded send-money, send-money-amount, send-money-confirm and payment-result
screens were deleted in the same pass that introduced this hub.

### Shared Downstream Screens

Two additional screens are shared across all seven rails, but the hub does not route to them
directly — the type screens do after the PSU has completed a form:

| Shared Screen    | Role                                              |
|------------------|---------------------------------------------------|
| payment-consent  | Authorise return leg — PSU returns from HSBC after OAuth |
| payment-status   | Settlement tracker — reads per-rail resource-status GET |

### Nav Params

No params are passed from the hub to any type screen. The hub routes are parameterless; each type
screen resolves its own debtor account from the account store.

### Nav Invariant

`RULE-IMPL-NAVIGATION-CONNECTED-001` and `RULE-IMPL-DEAD-CLICKABLE-001` are enforced by
`TC-PAY-HUB-002`: every tile must resolve to an implemented route at the time the module ships.

---

## API Endpoints

**This screen makes no backend calls. The `operations` block is empty by design, and `has_api` is
deliberately absent from this feature's capability list.**

See `API.md` for the full rationale and the downstream endpoint map.

| # | Endpoint | Method | Auth | Notes |
|---|----------|--------|------|-------|
| — | (none)   | —      | —    | Pure navigation surface; all endpoints belong to the seven type features |

---

## Design Tokens Used

| Token               | Value (light)  | Used By                          |
|---------------------|----------------|----------------------------------|
| `surface`           | `#F7F9FF`      | Screen background                |
| `onSurface`         | `#181C20`      | `hub_heading` text               |
| `onSurfaceVariant`  | `#41474D`      | `amend_notice` text, tile description text |
| `surfaceContainerLow` | `#F1F4F9`    | Tile card background             |
| `outline`           | `#72787E`      | Tile card border (default state) |
| `primary`           | `#266489`      | Tile icon colour (active / pressed state) |
| `titleMedium`       | 16sp / 500     | `hub_heading`                    |
| `bodySmall`         | 12sp / 400     | `amend_notice`, tile descriptions |
| `labelMedium`       | 12sp / 500     | Tile labels                      |
| `radius.md`         | 12dp           | Tile card corner radius          |
| `spacing.md`        | 16dp           | Screen horizontal padding        |
| `spacing.sm`        | 8dp            | Grid gap (12dp literal; nearest named step) |
| `icon.md`           | 24dp           | Tile icons                       |
| `touch_targets.comfortable` | 48dp | Tile minimum tap target         |

---

## Testing

| ID              | Scenario                                                     | Priority |
|-----------------|--------------------------------------------------------------|:--------:|
| TC-PAY-HUB-001  | All seven tiles visible with correct labels and descriptions | P0       |
| TC-PAY-HUB-002  | Each tile taps successfully and navigates to the correct route | P0     |
| TC-PAY-HUB-003  | Grid renders correctly at 390dp baseline (7 tiles, 3-column) | P0      |
| TC-PAY-HUB-004  | Amend notice is visible below the grid                       | P0       |
| TC-PAY-HUB-005  | Grid widens to 4 columns at ≥600dp (tablet breakpoint)       | P1       |
| TC-PAY-HUB-006  | No tile is hidden regardless of account eligibility          | P1       |

**Coverage target:** P0 scenarios (4) must ship with the module; P1 scenarios are follow-on.

**Test file convention:** `feature/payments/src/commonTest/kotlin/.../PaymentsViewModelTest.kt`

---

## Referenced Journeys

Resolved against `idea-layer/journeys/*.yaml` — a journey is listed here only when the `payments`
screen appears in that journey's `screen_sequence`.

| Journey | Name | Persona | Tier | Where the hub appears |
|---|---|---|---|---|
| `consumer-accounts-payments` | Consumer Accounts & Payments | returning consumer | maximum | Step 6 — "choose how to pay"; success signal is *seven type tiles render*, then taps Domestic single |
| `consumer-cards-financing` | Consumer Recurring Payments Review | returning consumer | maximum | Final step — PSU arrives from `standing-order-detail` to set up a NEW standing order, because a PISP may not amend the existing one |
| `consumer-insights-utilities` | Consumer Insights & Utilities | returning consumer | medium | Step 2 — "pay someone abroad"; taps the International single tile |

The hub is the most journey-covered screen in the payment cluster: three of the five journeys pass
through it. Only two of the seven tiles are followed downstream by any journey, though —
`pay-domestic-single` and `pay-international-single`. The other five tiles route to features no
journey exercises (see `journeys/INDEX.md` § "Coverage gaps owed"), so TC-PAY-HUB-002 is the only
coverage those routes have.

Read `consumer-cards-financing` by its `name`, not its `id` — it stopped being about cards on
2026-08-07 when the `cards` and `card-detail` screens were deleted. The `id` was kept because
`screens/standing-order-detail/flow.yaml` and `screens/direct-debit-detail/flow.yaml` reference it.

---

## Dependencies

**Tier:** feature

| Dependency                    | Type    | Relation |
|-------------------------------|---------|----------|
| pay-domestic-single           | feature | child (route target) |
| pay-domestic-scheduled        | feature | child (route target) |
| pay-domestic-standing-order   | feature | child (route target) |
| pay-international-single      | feature | child (route target) |
| pay-international-scheduled   | feature | child (route target) |
| pay-international-standing-order | feature | child (route target) |
| pay-vrp-mandate               | feature | child (route target) |
| payment-consent               | feature | shared (downstream) |
| payment-status                | feature | shared (downstream) |

No shared entities. No libraries. No DI bindings on this feature's own module.

---

## Source State (spec ahead of source)

No `feature/payments` module exists yet. The Pay tab still points at
`SendMoneyRoute → PlaceholderScreen("Pay")` (BankingDestinations.kt:82). Drift and source-test
checks are unassertable for this feature — score them N/A, not failing.

The `feature/payments` module is owed by `/kmp-implement`. `PaymentsRoute` must be wired into the
bottom-nav composable (`AuthenticatedNavBarTabItem.kt`) in place of `SendMoneyRoute`.
