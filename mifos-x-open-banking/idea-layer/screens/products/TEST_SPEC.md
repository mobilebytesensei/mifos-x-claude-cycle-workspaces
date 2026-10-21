# TEST SPEC — Products

> ## ⚠ STALE GENERATED OUTPUT — DO NOT TREAT AS THE TEST SUITE
>
> **This document has been superseded in full and is awaiting regeneration from
> `screens/products/tests.yaml`.**
>
> `tests.yaml` was rewritten on 2026-08-07 against the HSBC UK **Open Data Product Finder**
> (`api.hsbc.com`, OBIE Open Data v2.2 — four families, two brands, no auth) and now carries
> **37** scenarios. This file still renders the **17** scenarios of the superseded model and
> its `TC-PRODS-*` numbers **do not correspond** to the same-numbered scenarios in `tests.yaml`.
> `TC-PRODS-005` here is a per-bank fan-out; in `tests.yaml` it is first direct brand labelling.
>
> Every scenario below describes one of two dead models: the 2026-05/06 per-bank catalogue
> keyed on `bankId`, or the 2026-08-06 per-account AIS reading. Neither exists. There is no
> `bankId` path segment, no per-bank fan-out, no client-side audience split, and — because the
> Product Finder is unauthenticated — no `401`, no `403`, and no session-expired state.
>
> The four assertions that named non-existent endpoints or error codes have been struck through
> below so they cannot be actioned, but **striking them does not make the rest correct**. Read
> `screens/products/tests.yaml` instead, and regenerate this file rather than hand-patching it.

| Field      | Value                                                                |
|------------|----------------------------------------------------------------------|
| Feature    | products                                                             |
| Source     | `screens/products/tests.yaml`                                        |
| Scenarios  | 17 — **STALE**, `tests.yaml` now declares 37                          |
| Priorities | high 9 · medium 7 · low 1 — **STALE**                                 |
| States     | content 12 · loading 2 · empty 1 · error 1 · unauthenticated 1 — **STALE**, `unauthenticated` was deleted as unreachable |
| Module     | _none yet — spec-only feature_                                       |

> No source module exists. These are **forward specs** derived from the feature's idea-layer
> siblings. The singular `product` feature **does** ship (`feature/product`) — this is the
> catalogue browser, not the detail screen.

---

## Coverage

| State           | Scenarios | Covered |
|-----------------|-----------|---------|
| loading         | 2  | TC-PRODS-001, -005 |
| content         | 12 | TC-PRODS-002, -003, -004, -006 … -012, -016, -017 |
| empty           | 1  | TC-PRODS-013 |
| error           | 1  | TC-PRODS-014 |
| unauthenticated | 1  | TC-PRODS-015 |

Five states covered.

---

## Everything the user sees is derived client-side

The sandbox returns products with `null` category and `null` family, so the screen invents its own
taxonomy:

| Surface | Derivation | Scenario |
|---------|-----------|----------|
| Personal / Business tabs | `scopeOf` over code and name against `BUSINESS_MARKERS` | TC-PRODS-006 |
| Category badge | `categoryOf` into EVERYDAY / SAVINGS / CARDS / LOANS | TC-PRODS-008 |

Substring matching on product names is a heuristic, and it is presented to the customer as a fact.
A personal product whose name happens to contain "BUSINESS", or a business product that names none
of the five markers, lands in the wrong tab with no indication that the sorting was guessed. The
category badge has the same exposure and, per TC-PRODS-008, no filter depends on it — so a wrong
badge misinforms without breaking anything, which is the harder failure to catch.

Worth stating in `api.yaml` as a known limitation rather than leaving it implicit in `scopeOf`.

---

## Failure is layered, not global

Three different scopes of failure land in three different places:

| Scope | Scenario | Result |
|-------|----------|--------|
| One bank's catalogue fails | TC-PRODS-011 | inline row; screen stays in Content |
| One audience tab has no matches | TC-PRODS-012 | inline row; screen stays in Content |
| No bank returns any products | TC-PRODS-013 | Empty state |
| Every bank 404s / 401 / offline | TC-PRODS-014, -015 | Error shell with retry |

That gradient is the strongest part of this spec. Compare `fx-rates`, which folds `Empty` into the
error branch — here empty and error stay distinct, and partial failure never takes the screen down.

---

## TC-PRODS-001 — Loading state shows the shimmer placeholder only

**Priority:** medium · **State:** loading

- **Given** Per-bank catalogue fetches are in flight
- **When** Screen mounts
- **Then**
  - Loading affordance is shown with no product rows rendered
  - Reduced-motion preference substitutes `static_placeholder` for the shimmer

---

## TC-PRODS-002 — Content state renders the per-bank catalogue shell

**Priority:** high · **State:** content

- **Given** The user holds accounts at three banks; all catalogues resolve
- **When** Screen renders
- **Then**
  - Top app bar shows "Products" with an `arrow_back` icon, no actions and no bottom nav
  - `products_bank_selector` visible as a Surface pill with `account_balance` leading icon and `keyboard_arrow_down` trailing icon
  - `products_scope_tabs` visible with `products_tab_personal` and `products_tab_business`
  - `product_card` rows render for the selected bank and audience
  - Personal is the default selected tab (`ProductScope.PERSONAL`)

---

## TC-PRODS-003 — Bank selector is always shown, even with a single bank

**Priority:** medium · **State:** content

- **Given** The user holds an account at exactly one bank
- **When** Screen renders
- **Then**
  - `products_bank_selector` is still visible
  - It shows that bank's resolved display name from `BanksRepository`

Keeping a one-option control visible is the right call here: it tells the customer *whose*
catalogue they are reading, which matters more than saving a row.

---

## TC-PRODS-004 — Choosing a different bank re-filters the list

**Priority:** high · **State:** content

- **Given** Content state with three banks loaded
- **When** User taps `products_bank_selector` and picks another bank from the `PickerBottomSheet`
- **Then**
  - `onBankSelected` sets `selectedBankId` on state
  - The product list re-filters to that bank's offerings without a new round of fetches
  - The audience tab selection is preserved

Preserving the tab is the assertion that makes bank-switching a comparison tool — a customer
looking at business products at one bank wants to see business products at the next.

---

## TC-PRODS-005 — Catalogues are fetched per bank in parallel, once per session

**Priority:** high · **State:** loading

> **SUPERSEDED — do not action.** There is no per-bank fan-out and no `bankId`. The Product
> Finder is a single-ASPSP public catalogue on `api.hsbc.com`; the audience split is which
> endpoint you call, not how you filter a merged list. This screen reads nothing belonging to
> the PSU, so `AccountsRepository` is not a dependency and the screen is reachable before login.
> Current loading behaviour: `tests.yaml#TC-PRODS-001..004` (per-family fetch —
> `personal-current-accounts` on open, the other three families lazily on first tab selection).

- ~~**Given** The user holds accounts at three distinct `bankId`s~~
- ~~**When** The screen loads~~
- ~~**Then**~~
  - ~~`GET /obp/v3.0.0/banks/{bankId}/products` is issued once per bank via `awaitAll`~~
  - ~~The bank set comes from the distinct `bank_id` values in `AccountsRepository.myAccounts()`~~
  - ~~Bank display names are resolved through `BanksRepository`~~

---

## TC-PRODS-006 — Audience split is derived client-side because the API category is null

**Priority:** high · **State:** content

- **Given** Sandbox products return null `category` and `family`
- **When** `scopeOf` runs over code and name
- **Then**
  - Products matching `BUSINESS_MARKERS` (BUSINESS, CORPORATE, WORKING-CAPITAL, FREELANCER, FX-SPOT) resolve to `ProductScope.BUSINESS`
  - All others resolve to `ProductScope.PERSONAL`
  - The split does not depend on the API `category` field

Note the default: anything unmatched is Personal. So a mis-sorted business product surfaces to
retail customers rather than hiding — the safer direction of the two, though still wrong.

---

## TC-PRODS-007 — Switching to Business shows only business products

**Priority:** high · **State:** content

- **Given** The selected bank has both personal and business products
- **When** User taps `products_tab_business` (`onScopeSelected BUSINESS`)
- **Then**
  - `scope` becomes `ProductScope.BUSINESS`
  - Only rows whose derived scope is BUSINESS are listed
  - `products_tab_business` reports selected to assistive tech and `products_tab_personal` does not

---

## TC-PRODS-008 — Category badge is derived client-side across four buckets

**Priority:** medium · **State:** content

- **Given** Products load with null `category` from the API
- **When** `product_category_badge` renders per card
- **Then**
  - `categoryOf` resolves each row to EVERYDAY, SAVINGS, CARDS or LOANS
  - No MORTGAGES bucket exists — mortgage-like products fall under LOANS
  - The badge is the only surviving use of category; there are no category filter chips

A mortgage badged as a loan is a plausible mis-labelling to a customer and an implausible one to a
bank. Recorded as a deliberate simplification, not an oversight.

---

## TC-PRODS-009 — More info opens the product URL in the platform browser

**Priority:** high · **State:** content

- **Given** A product row with a non-blank `moreInfoUrl`
- **When** User taps `product_card` or `product_more_info`
- **Then**
  - `LocalUriHandler.openUri` is invoked with the product's `more_info_url`
  - No in-app web view is used and no terms text is inlined on the screen
  - No Apply or Details journey is triggered — none exists

Refusing to inline product terms is right. Rendering a bank's own terms inside this app would make
the app appear to be the source of a claim it has no authority over.

---

## TC-PRODS-010 — A product with no URL renders as a non-clickable card

**Priority:** high · **State:** content

- **Given** A product row whose `moreInfoUrl` is blank
- **When** `product_card` renders
- **Then**
  - The card is disabled and does not respond to taps
  - No browser is opened
  - The name, description and category badge still render

The card stays informative while ceasing to be interactive. Both halves are needed — a card that
disappears loses a real product from the catalogue, and one that stays tappable dead-ends.

---

## TC-PRODS-011 — A single bank failing degrades inline, not globally

**Priority:** high · **State:** content

- **Given** Two of three bank catalogues resolve and the selected bank's fetch fails
- **When** The failure is handled
- **Then**
  - `bankLoadFailed` is true for that bank
  - `products_bank_load_failed` row "Could not load this bank's products" renders inline
  - The screen stays in Content — it does **NOT** fall to the full-screen error state
  - Retry re-fetches via `onRetry`

The inline notice is what `fx-rates` TC-FX-011 lacks: there, a failing pair simply vanishes from
the list. Here the customer is told which bank did not answer.

---

## TC-PRODS-012 — An audience tab with no matching products shows the in-scope empty row

**Priority:** medium · **State:** content

- **Given** The selected bank publishes no business products
- **When** User switches to the Business tab
- **Then**
  - `products_scope_empty` "No products at this bank yet" renders inline
  - The screen stays in Content rather than switching to the Empty state
  - The bank selector and tabs remain usable

Correct: switching to the full Empty state would strip the selector and tabs (TC-PRODS-013) and
strand the customer on a screen with no way back to the tab that had results.

---

## TC-PRODS-013 — Empty state covers a bank with no published catalogue at all

**Priority:** medium · **State:** empty

- **Given** No products are returned for any bank
- **When** Screen renders
- **Then**
  - `inventory_2` empty icon visible
  - Title "No products published" and message "The bank has not published a product catalogue yet" visible
  - No product rows, selector or tabs rendered

The message says "the bank" while the condition is "no bank returned anything". Minor, but with
several banks loaded the singular is misleading.

---

## TC-PRODS-014 — Error state offers retry on a 404 bank lookup

**Priority:** medium · **State:** error

> **SUPERSEDED — do not action.** `BANK_NOT_FOUND` is an Open Bank Project error code and does
> not exist on this host; neither does the per-bank lookup that could raise it. `api.yaml#errors`
> declares `400 · 408 · 429 · 500 · 503` and nothing else. The `429` case is the one worth
> designing for — an unauthenticated public API rate-limits by origin, so a retry loop is
> throttled against every user behind the same egress.

- ~~**Given** `obp_products` returns 404 `BANK_NOT_FOUND` for every bank~~
- ~~**When** Screen renders~~
- ~~**Then**~~
  - ~~`cloud_off` icon with "Unable to load products" and "Check your connection and try again" visible~~
  - ~~Retry button visible and wired to `onRetry`~~

---

## TC-PRODS-015 — Unauthenticated and no-network render the same recoverable failure shell

**Priority:** medium · **State:** unauthenticated

> **SUPERSEDED — do not action.** `USER_NOT_LOGGED_IN` is an Open Bank Project error code. The
> Product Finder takes no token, no consent, no session and no API key, and the spec declares no
> `401` and no `403` on any path — so the `unauthenticated` state is **unreachable** and was
> deleted (`ui.yaml#removed_state_2026_08_07`). Shipping it would put a sign-in promise on a
> screen where signing in changes nothing about what can be seen. The no-network half of this
> scenario survives on its own merits.
>
> The surviving insight — never leave the user silently on an empty list, because an empty
> catalogue reads as "this bank has nothing to offer" — is carried by
> `tests.yaml#TC-PRODS-017` (inline segment-empty row) and the `empty_family_rule`.

- ~~**Given** `obp_products` returns 401 `USER_NOT_LOGGED_IN`, or the device is offline~~
- ~~**When** Screen renders~~
- ~~**Then**~~
  - ~~`ScreenState` resolves to `Unauthenticated` or `NoNetwork` respectively~~
  - ~~Both render the `cloud_off` error shell with a retry button~~
  - ~~The user is not silently left on an empty list~~

---

## TC-PRODS-016 — Product name binds to the API name field, not a label field

**Priority:** high · **State:** content

> **SUPERSEDED — do not action.** `code` / `name` / `description` are Open Bank Project
> snake_case fields. This wire is OBIE PascalCase throughout, and the field is `Name`; there is
> no `label` field for this guard to rule out. `tests.yaml` records it as retired
> (`TC-PRODS-016#was`) and replaces it with the defect that IS present — `TC-PRODS-018`,
> trailing whitespace on live `Name` values such as `"Small Business Loan "`.

- ~~**Given** `obp_products` returns products with `code`, `name` and `description`~~
- ~~**When** `ProductRow` is mapped~~
- ~~**Then**~~
  - ~~`name` is populated from the response `name` field~~
  - ~~No row renders a blank display name~~

---

## TC-PRODS-017 — Product search is not reachable from this screen

**Priority:** low · **State:** content

- **Given** `search_products` is marked deferred
- **When** The top app bar renders
- **Then**
  - `actions` is empty — no search affordance exists
  - No search endpoint is called by this screen

---

## Traceability

| Action | Scenario |
|--------|----------|
| `onBankSelected` | TC-PRODS-004 |
| `onScopeSelected` | TC-PRODS-007 |
| open product URL | TC-PRODS-009, -010 |
| `onRetry` | TC-PRODS-011, -014 |

Every declared action has a covering scenario, and both the eligible and ineligible cases of the
product tap are covered.

---

_Generated by /idea-feature-test-export | 2026-08-04_
