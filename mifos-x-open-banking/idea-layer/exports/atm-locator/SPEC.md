# SPEC — ATM & Branch Locator

| Field         | Value                    |
|---------------|--------------------------|
| Feature       | atm-locator              |
| Flavor        | consumer                 |
| Status        | approved                 |
| Quality Score | 93                       |
| ViewModel     | AtmLocatorViewModel      |
| Archetype     | index_list               |

---

## Overview

Nearby ATMs and branches for the banks the customer holds accounts with, as a map area above an
expandable result list. Each row carries distance, opening hours, accessibility and deposit-taking
flags, and a Directions action.

Location is **optional, not required**. `hasLocation` gates the experience: with a device position,
rows show distances and `center` is that position; without one, `center` falls back to the
**centroid of the matched ATMs** and the screen still works. A locator that refuses to function
without location permission would be needlessly brittle.

Expansion is single-open: `selectedAtmId` holds one id, and **tapping the open row clears it**, so
the list never accumulates expanded rows.

The result summary is written to be honest about scope — "4 ATMs" when no position is known, "4 ATMs
near you" when one is.

---

## Screens

| ID          | Name                 | ViewModel           | Archetype  |
|-------------|----------------------|---------------------|------------|
| atm-locator | ATM & Branch Locator | AtmLocatorViewModel | index_list |

---

## Components

| ID                       | Type        | Description                                        |
|--------------------------|-------------|-----------------------------------------------------|
| atm_locator_title        | text        | "ATM & Branches"                                   |
| atm_map_area             | image       | Map region                                         |
| atm_search_row           | stack       | Search row                                         |
| └ location_search_input  | input       | `query` — filters by location text                 |
| └ use_my_location_button | icon_button | `my_location` — sets `hasLocation`                 |
| nearby_results_header    | text        | `resultSummary`                                    |
| atm_result_kcb_westlands | box         | One ATM row — tap expands; tapping again collapses |
| └ atm_kcb_name           | text        | ATM name                                           |
| └ atm_kcb_hours          | text        | `hoursLabel`                                       |
| └ atm_kcb_distance       | badge       | `distanceLabel`                                    |
| └ atm_kcb_address        | text        | `addressLine`                                      |
| └ atm_kcb_accessible_chip| chip        | Shown when `accessible`                            |
| └ atm_kcb_deposits_chip  | chip        | Shown when `acceptsDeposits`                       |
| └ atm_kcb_directions     | button      | Opens directions                                   |
| atm_result_equity_cbd    | box         | Second ATM row (same structure)                    |
| atm_result_coop_karen    | box         | Third ATM row (same structure)                     |
| atm_empty_state          | stack       | No results container                               |
| └ atm_empty_icon         | icon        | `location_off`                                     |
| └ atm_empty_title        | text        | "No ATMs nearby"                                   |
| └ atm_empty_message      | text        | "None of your banks have…"                         |
| atm_error_state          | stack       | Error container                                    |
| └ atm_error_icon         | icon        | `cloud_off`                                        |
| └ atm_error_title        | text        | "Couldn't load ATMs"                               |
| └ atm_error_message      | text        | "Check your connection…"                           |
| └ atm_retry_button       | button      | Retry                                              |

The three result rows are demo instances of one repeating pattern — a real implementation renders
one per `AtmRow`.

---

## States

Initial state: `loading`. Six states — the canonical four plus two connectivity states.

| State           | Rendering                                       |
|-----------------|--------------------------------------------------|
| loading         | Fetching                                        |
| content         | Map, search, summary, expandable rows           |
| empty           | `location_off` — no ATMs for the customer's banks |
| error           | `cloud_off` + retry                             |
| no_network      | Error treatment                                 |
| unauthenticated | Error treatment                                 |

The empty message names the reason precisely — *none of your banks* have ATMs nearby, rather than
"no results", because the search is scoped to the banks the customer holds accounts with.

---

## State Model

**ViewModel:** `AtmLocatorViewModel` — `ScreenState<AtmLocatorContent>`.

**Content fields**

| Field           | Type             | Note                                                          |
|-----------------|------------------|----------------------------------------------------------------|
| `atms`          | `List<AtmRow>`   | Each row: id, name, addressLine, distanceLabel, distanceMeters?, lat, lng, hoursLabel, accessible, acceptsDeposits, moreInfo |
| `query`         | `String`         | Default `""`                                                   |
| `hasLocation`   | `Boolean`        | Default `false` — location is optional                         |
| `resultSummary` | `String`         | "No matching ATMs" / "4 ATMs" / "4 ATMs near you"              |
| `selectedAtmId` | `String`         | Default `""`; the single expanded row — tapping the open one clears it |
| `center`        | `MapCoordinate?` | Device location when known, **else the centroid of matched ATMs** |

`distanceMeters` is nullable alongside the formatted `distanceLabel`: without a device position
there is no distance to compute, and the label degrades rather than showing a false zero.

---

## Navigation

`navigates_to: []` — a leaf screen. Directions hand off to the platform maps application rather than
navigating in-app. Journey: `consumer-insights-utilities`.

**Known deferral:** reached from account-detail's ATM chip, whose `AtmLocatorRoute` currently
resolves to `PlaceholderScreen("ATM locator")` in cmp-navigation — the chip renders and navigates,
but no feature module implements the destination yet. Recorded in
`idea-plan.yaml#deferred_routes` with `target_milestone: unscheduled`. The idea-layer screen
specified here does exist; the module does not.

---

## API Endpoints

| ID               | Endpoint                                     |
|------------------|----------------------------------------------|
| obp_get_atms     | `GET /obp/v3.0.0/banks/{bankId}/atms`        |
| obp_get_branches | `GET /obp/v3.0.0/banks/{bankId}/branches`    |

Both are per-bank. Full detail: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto. Accessibility and deposit chips
use `secondaryContainer` — they are facilities, not statuses. Components reference semantic roles, so
both theme modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand
spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/atm-locator/{ui,api,flow,docs}.yaml. -->
