# API — ATM & Branch Locator

Client contracts for `atm-locator`. This project owns no backend: these are Ktorfit contracts
against the OBP sandbox, not owned schema.

---

## obp_get_atms

| | |
|---|---|
| Endpoint | `GET /obp/v3.0.0/banks/{bankId}/atms` |

ATMs for one bank.

| Code | Cause                                      |
|------|--------------------------------------------|
| 401  | Unauthorized — missing or invalid token    |
| 404  | Bank not found                             |
| 500  | Internal server error                      |

---

## obp_get_branches

| | |
|---|---|
| Endpoint | `GET /obp/v3.0.0/banks/{bankId}/branches` |

Branches for one bank, merged into the same result list.

---

## Per-bank, not global

Both endpoints take a `bankId`. There is no "all ATMs near me" call — the screen fetches per bank
across the banks the customer holds accounts with, then merges.

That scoping is why the empty state reads *"None of your banks have…"* rather than "no results
nearby". An ATM belonging to a bank the customer has no relationship with is not in scope and its
absence is not a gap.

---

## Location is optional

`hasLocation` gates distance, not availability.

| With a device position | Without |
|------------------------|---------|
| `distanceMeters` computed, `distanceLabel` rendered | both degrade; no false zero shown |
| `center` = device location | `center` = **centroid of matched ATMs** |
| Summary reads "4 ATMs near you" | Summary reads "4 ATMs" |

The centroid fallback is what lets the screen work at all without location permission — the map
still has somewhere sensible to sit. A locator that refused to render without permission would be
needlessly brittle, and the summary wording keeps the claim honest either way.

`use_my_location_button` is the affordance that sets `hasLocation`; it is not a precondition for
using the screen.

---

## Filtering

`query` filters client-side over the fetched, merged list. There is no server-side location search —
both endpoints return a bank's full set, and narrowing happens in memory.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/atm-locator/api.yaml. -->
