# SPEC — Products

| Field         | Value             |
|---------------|-------------------|
| Feature       | products          |
| Flavor        | consumer          |
| Status        | approved          |
| Quality Score | 95                |
| ViewModel     | ProductsViewModel |

---

## Overview

A read-only catalogue of the products an ASPSP has published. The PSU picks a bank from the
selector, switches between the Personal and Business audience tabs, and reads the resulting product
cards. Cards are data-driven — one `product_card` template rendered per catalogue entry, not a
hardcoded product set — and each carries a category badge and a "More info" affordance.

There is **no in-app apply or details journey**. The only outbound affordance is the product's
`more_info_url`, handed to the platform browser via `compose.ui.platform.LocalUriHandler`; full
terms live on the bank's own site and are never inlined here. The screen is a pushed leaf owning a
back arrow only — `flow.yaml#navigates_to` is intentionally empty.

Bank selection and audience filtering both operate on the already-fetched catalogue, so neither
re-queries. A bank whose catalogue fails to load and an audience tab with no matching products both
render inline rows within Content rather than taking over the screen.

---

## Screens

| ID       | Name     | Layout | Scroll   | Responsive  |
|----------|----------|--------|----------|-------------|
| products | Products | Column | Vertical | mobile_only (baseline 390) |

---

## Components

| ID                       | Type           | Description                                                                                          |
|--------------------------|----------------|------------------------------------------------------------------------------------------------------|
| products_title           | text           | Screen title; the one component visible in every state                                                |
| products_bank_selector   | card           | surfaceContainer, radius 12, `account_balance` leading + `keyboard_arrow_down` trailing — opens the ASPSP picker; `onBankSelected` re-filters the resident list to that bank |
| products_scope_tabs      | tab_bar        | Audience tab strip; `onScopeSelected` re-filters the loaded catalogue                                 |
| products_tab_personal    | text           | Personal audience tab — narrows the catalogue to retail products                                      |
| products_tab_business    | text           | Business audience tab — narrows the catalogue to commercial products                                  |
| product_card             | card           | Data-driven card template, one per catalogue entry: surfaceContainer, radius 16, outlineVariant 1dp border, 16dp padding. Tapping opens `more_info_url` in the platform browser |
| product_category_badge   | badge          | Category label on the card                                                                            |
| product_more_info        | text           | "More info" — link-styled affordance opening `more_info_url` in the platform browser                  |
| products_bank_load_failed| text           | Inline row shown within Content when the selected bank's catalogue fails to load                       |
| products_scope_empty     | text           | Inline row shown within Content when the selected audience tab matches no products                     |

---

## States

Shipped state set is `ScreenState<ProductsContent>`:

| State           | Rendering                                                                              |
|-----------------|----------------------------------------------------------------------------------------|
| loading         | Shimmer (short4; `static_placeholder` under reduced-motion), loading icon               |
| content         | Title, bank selector, audience tabs, product cards + badges, More info, and the two inline rows |
| empty           | `inventory_2` — "No products published" / "The bank has not published a product catalogue yet" |
| error           | `cloud_off` — "Unable to load products" / "Check your connection and try again", retry   |
| no_network      | Same treatment as error                                                                 |
| unauthenticated | Title only                                                                              |

Initial state: `loading`.

Per-bank load failure (`bankLoadFailed`) and in-scope emptiness render as inline rows **within**
Content — they are deliberately not separate ScreenStates.

---

## Navigation

| From     | To                    | Trigger                          | Type            |
|----------|-----------------------|----------------------------------|-----------------|
| products | (platform browser)    | `open_url` → `more_info_url` on a product card or "More info" | external |
| products | (previous screen)     | `navigate_back` top-bar arrow    | pop             |

`navigates_to: []` — Products is a pushed leaf with no in-app forward navigation. There is no
`application-detail` screen and no apply journey.

---

## API Endpoints

| ID                 | Endpoint                                   | Purpose                                      |
|--------------------|--------------------------------------------|----------------------------------------------|
| obp_products       | `GET /obp/v3.0.0/banks/{bankId}/products`  | The selected bank's published product catalogue |
| obp_get_my_accounts| `GET /obp/v3.0.0/my/accounts`              | Resolves the banks available to this PSU      |
| search_products    | —                                          | Catalogue search                              |

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto. Components reference semantic
roles (`surfaceContainer`, `outlineVariant`, `primary`) rather than literal hex values, so both
theme modes resolve from `design-system/design-tokens.yaml`.

---

<!--
Regenerated 2026-08-04 by /idea-sync from screens/products/{ui,api,flow}.yaml.

The previous revision described a hardcoded four-product catalogue — Instant Access Savings, Fixed
Rate Bond, Personal Loan, Platinum Credit Card — each with its own "Details" (outlined) and "Apply
Now" (filled) buttons navigating to an `application-detail` screen, plus a refer-a-friend promo
banner offering £50 cashback and tab-bar navigation to home/accounts/send-money. None of those
components exist in the source of truth: the catalogue is data-driven from a single `product_card`
template, `application-detail` resolves to no screen directory, and flow.yaml states explicitly
that Products has NO in-app forward nav and no apply journey. Literal hex values from the
pre-migration palette were also carried in that revision; components now reference semantic roles.

Provenance: regenerated 2026-08-04 during the export-drift repair and re-verified against an
unchanged source hash (7e0576e5201f) by /idea-feature-export --all --force in the same session.
-->
