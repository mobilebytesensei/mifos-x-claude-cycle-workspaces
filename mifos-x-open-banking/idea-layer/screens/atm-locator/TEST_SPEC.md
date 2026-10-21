# TEST SPEC — ATM Locator

| Field      | Value                                     |
|------------|-------------------------------------------|
| Feature    | atm-locator                               |
| Source     | `screens/atm-locator/tests.yaml`          |
| Screen id  | `atm_locator_main`                        |
| Scenarios  | 16                                        |
| Priorities | high 12 · medium 4                        |
| States     | content 12 · loading 1 · empty 1 · error 2 |
| Module     | _none yet — spec-only feature_            |

> No source module exists. These are **forward specs** derived from the feature's idea-layer
> siblings, not reverse-synced from a shipped suite.

---

## Coverage

| State   | Scenarios | Covered |
|---------|-----------|---------|
| loading | 1  | TC-ATM-001 |
| content | 12 | TC-ATM-002 … -011, -015, -016 |
| empty   | 1  | TC-ATM-012 |
| error   | 2  | TC-ATM-013, -014 |

All four declared states are covered. The weight sits on content because this screen's behaviour
*is* its content state — a map, an in-memory filter, a selection model and a distance sort, none
of which are reachable from any other state.

Two scenarios pin deliberate absences that the screen's own title invites someone to add:
TC-ATM-015 records that **branches are never fetched** despite "ATM & Branches" in the top bar,
and TC-ATM-006 records that there is **no permission-denied state**. Both are recorded rather than
defaulted.

---

## TC-ATM-001 — Loading state shows only the title and a progress indicator

**Priority:** medium · **State:** loading

- **Given** The bank list and per-bank ATM fetches are in flight (`initial_state: loading`)
- **When** Screen mounts
- **Then**
  - `atm_locator_title` visible with a centred progress indicator
  - Map, search row, result header and all rows are hidden
  - No skeleton is used — a `CircularProgressIndicator` covers the load

The negative assertion is the point: a skeleton map is not a meaningful placeholder, and this
screen chose a spinner instead. A later "consistency" pass that swaps in shimmer would break this.

---

## TC-ATM-002 — Content state renders the map above the searchable list

**Priority:** high · **State:** content

- **Given** ATMs resolve across the user's banks
- **When** Screen renders
- **Then**
  - Top app bar shows "ATM & Branches" with an `arrow_back` icon; no bottom nav
  - `atm_map_area` renders the MapLibre map
  - `atm_search_row` with `location_search_input` and `use_my_location_button` visible
  - `nearby_results_header` and the ATM rows visible

---

## TC-ATM-003 — ATMs come from one unauthenticated Open Data call, with no per-bank fan-out

**Priority:** high · **State:** content

- **Given** The screen is opened, whether or not the user has connected any account
- **When** The screen loads
- **Then**
  - A single `GET https://api.hsbc.com/x-open-banking/v2.2/atms/geo-location/lat/{latitude}/long/{longitude}?radius={1-10}` is issued (`get_atms_by_geolocation`)
  - There is no `bankId` path segment and no per-bank fan-out — `api.hsbc.com` serves one ASPSP
  - The request carries no token, client certificate, consent or `x-fapi-*` header
  - `data.Brand[].ATM[]` is flattened client-side into the row list

The absence of a fan-out is the assertion that matters. Open Data is a single-ASPSP,
unauthenticated surface, so how many accounts the customer holds — or whether they hold any —
has no bearing on what this screen requests. `radius` is required despite its documented default
and is in MILES with a hard ceiling of 10, so proximity ordering beyond that window is entirely a
client concern, which is why TC-ATM-006's sort and TC-ATM-007's badges exist at all. The
postcode, town and country variants are the same shape: path-only, unauthenticated, no `bankId`.

---

## TC-ATM-004 — Search filters the resident list in memory

**Priority:** high · **State:** content

- **Given** The ATM set is already loaded
- **When** User types a city, postcode or address into `location_search_input`
- **Then**
  - `onQueryChanged` records the keystroke and re-filters in memory
  - No network call is issued per keystroke
  - There are no filter chips — free-text search is the only filter

---

## TC-ATM-005 — Result summary tracks both query and location

**Priority:** high · **State:** content

- **Given** Content state
- **When** The query or the known location changes
- **Then**
  - `nearby_results_header` reflects `resultSummary`
  - With no matches it reads "No matching ATMs"
  - Without location it reads e.g. "4 ATMs"; with location it reads "4 ATMs near you"

"Near you" is an accuracy claim, not copy. Rendering it before coordinates are known would tell
the customer the list is sorted by distance when it is not.

---

## TC-ATM-006 — Use-my-location resolves coordinates and re-sorts the list

**Priority:** high · **State:** content

- **Given** `hasLocation` is false
- **When** User taps `use_my_location_button` (`request_user_location`)
- **Then**
  - The platform coarse-location permission is requested via `rememberDeviceLocationRequester`
  - On grant, `onUserLocation` writes the coordinates to state and `hasLocation` becomes true
  - Rows re-sort nearest-first by great-circle distance
  - There is no permission banner and no location-denied state

The final assertion is a real design decision, not an omission: a denied permission leaves the
screen fully usable via free-text search, so it has nothing to report. A future permission-denied
state would need this scenario updated, not silently bypassed.

---

## TC-ATM-007 — Distance badges appear only once location is known

**Priority:** medium · **State:** content

- **Given** `hasLocation` is false
- **When** The rows render
- **Then**
  - Distance badges are not shown
  - Once location is known each row shows its `distanceLabel`, e.g. "320 m"

---

## TC-ATM-008 — Only one row is expanded at a time

**Priority:** high · **State:** content

- **Given** No row is currently expanded
- **When** User taps a row (`select_atm`), then taps a different row
- **Then**
  - `selectedAtmId` is set to the tapped row and only that row expands
  - Selecting another row collapses the first
  - Tapping the already-open row clears `selectedAtmId` and collapses it

All three transitions are asserted together because `selectedAtmId` is a single nullable slot —
the accordion behaviour and the toggle-to-close behaviour are the same field read two ways.

---

## TC-ATM-009 — Expanded detail shows address, capability chips and directions

**Priority:** high · **State:** content

- **Given** A row is expanded
- **When** The detail renders
- **Then**
  - The address line is visible
  - The Accessible chip appears only when the ATM is accessible
  - The Deposits chip appears only when the ATM accepts deposits
  - A Directions button is visible
  - None of these render for collapsed rows

"Only when" is the operative phrase for the two chips. An Accessible chip shown unconditionally
sends a wheelchair user to a machine they cannot reach.

---

## TC-ATM-010 — Directions delegates routing to the platform

**Priority:** high · **State:** content

- **Given** A row is expanded
- **When** User taps the Directions button (`open_directions`)
- **Then**
  - A `geo:` URI for that ATM is handed to `LocalUriHandler`
  - The app never draws a route itself
  - No `DirectionsRequested` event and no `NavigationService` are involved

---

## TC-ATM-011 — Map centres on the device when known, else on the matched set

**Priority:** medium · **State:** content

- **Given** Content state
- **When** `center` is computed
- **Then**
  - With location known, `center` is the device location
  - Without location, `center` is the centroid of the matched ATMs

---

## TC-ATM-012 — Banks with no ATMs render the empty state

**Priority:** high · **State:** empty

- **Given** The load succeeds but returns an empty ATM list
- **When** Screen renders
- **Then**
  - `atm_empty_state` with its icon, title and message is shown
  - Map, search row and result header are hidden
  - This is distinct from a failed load

---

## TC-ATM-013 — Error and no-network share the AtmErrorState branch

**Priority:** high · **State:** error

- **Given** Every bank fetch failed, the accounts lookup failed, or the device is offline
- **When** Screen renders
- **Then**
  - `atm_error_state` with icon, title, message and `atm_retry_button` is shown
  - Both `ScreenState` variants render identically
  - Map, search row and result header are hidden
  - No sign-in prompt, session-expired message or login navigation is reachable from this screen

Recorded as a collapse, deliberately. Two distinct `ScreenState` variants converge on one
rendering here, where a session-scoped screen would keep `Unauthenticated` and `NoNetwork`
separately asserted. Whether that collapse is right is a product question; this scenario at
least makes it visible rather than incidental.

**Amended 2026-08-07.** This was "Error, no-network and unauthenticated", asserting that *three*
variants render identically. The `unauthenticated` state has been removed from this screen: the
Open Data API declares `auth: none`, the swagger declares no security scheme, and api.yaml is
explicit that "there is no 401 and no 403 in the spec, on any path". The state was unreachable
code shipping a false message — "Sign in again to find ATMs near you" — on one of only three
screens a prospective customer can reach before connecting any account. The point stands: on a
session-scoped screen `Unauthenticated` is genuinely reachable, which is exactly why this screen
borrowing that shape was wrong. The final assertion is now inverted so it fails if a sign-in path
returns.

> **Amended again 2026-08-07.** The two paragraphs above originally cited `cards` (TC-CARDS-012,
> -013) as the session-scoped contrast. That screen was deleted the same day — OBIE has no card
> resource — so the citation is replaced with the general statement. Nothing about this screen's
> verdict changes; `cards` was an illustration, not the evidence.

---

## TC-ATM-014 — Retry re-runs the aggregate fetch

**Priority:** high · **State:** error

- **Given** Error state is displayed
- **When** User taps `atm_retry_button` (`retry_load`)
- **Then**
  - `onRetry` re-issues the Open Data ATM fetch for the current search area
  - The call reads from `atms` and `branches` sources as declared
  - State transitions error → loading → content on success

---

## TC-ATM-015 — Branches are not fetched or rendered

**Priority:** medium · **State:** content

- **Given** Branch lookup is deferred — it moved to the separate `branch-locator` feature on 2026-08-07
- **When** The screen loads
- **Then**
  - No branches endpoint is called — no `BranchesApi` or `BranchRepository` exists
  - The list contains ATMs only, despite the screen title naming branches
  - `AtmRepository` and `AccountsRepository` are the only injected dependencies

Note the tension with TC-ATM-014, which says the retry reads from "`atms` and `branches` sources
as declared". The declaration and the implementation disagree, and this scenario is the one
telling the truth. Worth resolving in `api.yaml` rather than leaving two scenarios to contradict
each other.

---

## TC-ATM-016 — A failed refresh does not blank an already-populated list

**Priority:** high · **State:** content

- **Given** ATMs are already rendered and a subsequent Open Data fetch fails
- **When** The failure is handled
- **Then**
  - The previously fetched ATMs still render
  - The screen stays in Content — Error is reserved for having nothing to show

TC-ATM-003 establishes that there is exactly one request and no fan-out, so there is no partial
result to reconcile: a fetch either returns an area's ATMs or it does not. That makes the resident
list the only thing standing between a transient network failure and a blank screen, and it is why
the memory cache in `data-flow.yaml` is not merely an optimisation.

---

## Traceability

| Action | Scenario |
|--------|----------|
| `request_user_location` | TC-ATM-006 |
| `select_atm` | TC-ATM-008 |
| `open_directions` | TC-ATM-010 |
| `retry_load` | TC-ATM-014 |
| free-text query change | TC-ATM-004, -005 |

Every declared action has exactly one covering scenario.

---

_Generated by /idea-feature-test-export | 2026-08-04_
