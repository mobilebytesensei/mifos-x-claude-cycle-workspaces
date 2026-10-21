# Visual Specification — ATM & Branch Locator

| Field | Value |
|---|---|
| Feature | atm-locator |
| Flavor | consumer |
| Archetype | index_list |

---

## Screen Layout

Top-to-bottom hierarchy on a scrollable column (background `surface`):

1. **Page title** — "ATM & Branches" `headlineLarge`, `primary`, padding top `spacing.lg`, horizontal `spacing.md`
2. **Location search input** — Pill-shaped search field (radius `radius.xl`, background `surfaceContainerLow`), leading search icon, placeholder "Enter city, postcode or address...", margin horizontal `spacing.md`, top `spacing.md`
3. **Location permission banner** *(location_denied state only)* — Bordered box (`primary` border, `primaryContainer` background), "Use my location for nearby ATMs" text with "Enable" text button
4. **Map area** — 240 dp tall rounded map (radius `radius.md`) displaying ATM/branch pins, margin horizontal `spacing.md`, top `spacing.md`
5. **Filter chips row** — Horizontal scrollable row of radio chips: "All" (selected, filled `primary`), "ATMs", "Branches", "24/7", padding horizontal `spacing.md`, vertical `spacing.md`
6. **Results header** — "3 ATMs found within 500m" `titleMedium`, `onSurface`
7. **Result cards** — Three elevated cards (elevation 2, radius `radius.md`, padding `spacing.md`, margin horizontal `spacing.md`, bottom `spacing.sm`):
   - Mifos ATM Oxford Street (0.2km, Open 24/7, £300 max withdrawal)
   - Mifos ATM Bond Street Station (0.5km, Open 24/7)
   - Mifos Branch Mayfair (0.8km, Mon–Fri 9am–5pm, Services: Cashier · FX · Safe Deposit)
8. **Divider** — `outlineVariant`, margin horizontal `spacing.md`

---

## Components

### Location Search Input
- **Position:** Directly below page title
- **Style:** Radius `radius.xl`, background `surfaceContainerLow`, leading "search" icon, padding horizontal `spacing.md` vertical `spacing.md`
- **Interaction:** Tap opens text entry; triggers location search on text change

### Filter Chips Row
- **Position:** Below map area, horizontal scrollable
- **Style:** Chips with radius `radius.lg`, padding horizontal `spacing.md` vertical `spacing.sm`; selected chip fills `primary` with `onPrimary` text; unselected chips use border-only style with `outline` stroke
- **Default selected:** "All" chip

### ATM Result Card — Oxford Street
- **Background:** `surfaceContainerLowest`, radius `radius.md`, elevation 2, padding `spacing.md`
- **Name:** "Mifos ATM — Oxford Street" `titleSmall`, weight 600, `onSurface`
- **Distance:** "0.2km away" `bodySmall`, `onSurfaceVariant`
- **Hours:** "Open 24/7" `bodySmall`, `primary`, weight 500, with check_circle icon
- **Limit:** "£300 max withdrawal" `bodySmall`, `onSurfaceVariant`
- **Directions link:** "Get Directions" `labelMedium`, `primary`, trailing directions icon

### ATM Result Card — Bond Street Station
- **Background:** `surfaceContainerLowest`, radius `radius.md`, elevation 2, padding `spacing.md`
- **Name:** "Mifos ATM — Bond Street Station" `titleSmall`, weight 600, `onSurface`
- **Distance:** "0.5km away" `bodySmall`, `onSurfaceVariant`
- **Hours:** "Open 24/7" `bodySmall`, `primary`, with check_circle icon
- **Directions link:** "Get Directions" `labelMedium`, `primary`

### Branch Result Card — Mayfair
- **Background:** `surfaceContainerLowest`, radius `radius.md`, elevation 2, padding `spacing.md`
- **Name:** "Mifos Branch — Mayfair" `titleSmall`, weight 600, `onSurface`
- **Distance:** "0.8km away" `bodySmall`, `onSurfaceVariant`
- **Hours:** "Mon–Fri 9am–5pm" `bodySmall`, `tertiary`, weight 500, with schedule icon
- **Services:** "Services: Cashier · FX · Safe Deposit" `bodySmall`, `onSurfaceVariant`
- **Directions link:** "Get Directions" `labelMedium`, `primary`

---

## Interaction Patterns

| Target | Gesture | Result |
|---|---|---|
| location_search_input | Tap | Keyboard opens, user types city/postcode; live search triggers |
| enable_location_button | Tap | OS location permission dialog appears |
| filter_all / filter_atms / filter_branches / filter_24_7 | Tap | Filter applied; result count header and visible cards update |
| atm_result_oxford_street / bond_street / mayfair_branch | Tap | ATM detail view pushed (view_atm_detail action) |
| atm_oxford_directions / bond_directions / branch_directions | Tap | Native maps app opens with destination pre-filled |

---

## Content Data

| Element | Sample Value |
|---|---|
| Result count header | 3 ATMs found within 500m |
| ATM 1 name | Mifos ATM — Oxford Street |
| ATM 1 distance | 0.2km away |
| ATM 1 hours | Open 24/7 |
| ATM 1 limit | £300 max withdrawal |
| ATM 2 name | Mifos ATM — Bond Street Station |
| ATM 2 distance | 0.5km away |
| ATM 2 hours | Open 24/7 |
| Branch 1 name | Mifos Branch — Mayfair |
| Branch 1 distance | 0.8km away |
| Branch 1 hours | Mon–Fri 9am–5pm |
| Branch 1 services | Cashier · FX · Safe Deposit |

---

## Design Notes

**Color Usage:**
- `primary` used for title, selected filter chip, "Enable" banner button, and all "Get Directions" links.
- **Always-open availability uses `primary`, not green** — this palette ships no green family, and DESIGN.md maps the success/available semantic onto the primary blue.
- **Limited-hours branches use `tertiary`, not amber** — DESIGN.md 1.3.0 assigns the warning / attention-needed semantic to the soft-violet tertiary. It distinguishes a restricted-hours branch from an always-open ATM without reaching for error red, which stays reserved for states where access is actually gone.
- Both hours treatments carry an icon (check_circle / schedule) alongside the text, so availability is never conveyed by colour alone (WCAG 1.4.1).

**Typography:**
- Page title: `headlineLarge` — consistent with the app's screen identity pattern.
- Result card names: `titleSmall` weight 600 — prominent but contained within the card hierarchy.
- Distance and hours: `bodySmall` — secondary metadata that doesn't compete with the name.

**Map Area:**
- 240 dp fixed height prevents the map from dominating the screen; the scrollable result list gives access to more results below.
- Radius `radius.md` matches the result card radius, creating a cohesive visual family.

**Accessibility:**
- Result cards are full-width tappable targets with aria listitem role.
- "Get Directions" links have explicit role="link" and describe the full destination in the a11y label.
- Location permission banner reads out the full request context for screen readers.
- Filter chips use role="radio" with clear group label "Filter ATMs and branches by type".

*Generated by /idea export | 2026-08-03*
