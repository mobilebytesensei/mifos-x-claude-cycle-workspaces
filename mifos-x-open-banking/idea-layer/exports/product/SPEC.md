# SPEC — Product Terms

| Field         | Value              |
|---------------|--------------------|
| Feature       | product            |
| Flavor        | consumer           |
| Status        | approved           |
| Quality Score | 95                 |
| ViewModel     | ProductViewModel   |
| Archetype     | detail_screen      |

---

## Overview

The terms of the product behind one account — fees, credit-interest bands, overdraft tiers and
features — reached from account-detail's Product chip.

It is a **tiered-rate** screen, which is what shapes its structure: credit interest and overdraft
charges are not single numbers but bands, so both sections render nested lists (a list of tiers,
each containing its own rows) rather than flat key/value pairs. Flattening them would misrepresent
banded pricing as a single rate.

The domain object is `OBProduct2?` — nullable, because an account can exist whose product the bank
does not return, which is what `empty` represents.

---

## Screens

| ID      | Name          | ViewModel        | Archetype     | Entry point    |
|---------|---------------|------------------|---------------|----------------|
| product | Product Terms | ProductViewModel | detail_screen | account-detail |

**Shell:** top app bar, title `{strings.product_terms_title}`, `back` leading icon. Bottom
navigation visible.

---

## Components

| ID                       | Type           | Description                                        |
|--------------------------|----------------|-----------------------------------------------------|
| product_header_card      | card           | Product identity block                             |
| └ product_type_label     | text           | `{product.ProductType}` — PCA or BCA               |
| └ product_name           | text           | `{product.ProductName}`                            |
| └ product_id             | text           | Product identifier                                 |
| fees_header              | section_header | Fees section                                       |
| monthly_max_charge_row   | list_item      | Monthly maximum charge                             |
| credit_interest_header   | section_header | Credit interest section                            |
| credit_interest_list     | list           | Interest bands                                     |
| └ tier_band_list         | list           | One band's tiers                                   |
| &nbsp;&nbsp;└ tier_band_row | list_item   | One tier — threshold + rate                        |
| overdraft_header         | section_header | Overdraft section                                  |
| overdraft_list           | list           | Overdraft bands                                    |
| └ overdraft_tier_list    | list           | One band's tiers                                   |
| &nbsp;&nbsp;└ overdraft_tier_row | list_item | One tier — threshold + charge                    |
| features_header          | section_header | Features section                                   |
| features_list            | list           | Product features                                   |
| └ feature_row            | list_item      | One feature                                        |
| empty_product_state      | empty_state    | No product returned for this account               |
| error_state              | error_state    | Load failure — `role: alert`                       |
| └ retry_button           | button         | `{strings.product_retry_button}` → `RetryLoad`     |

The doubly-nested lists in the interest and overdraft sections are deliberate: a band contains
tiers, and each tier is a row.

---

## States

Initial state: `loading`. Four states, matching `ProductUiState` one-for-one.

| State   | Rendering                                                  |
|---------|-------------------------------------------------------------|
| loading | Fetching                                                   |
| content | Header, fees, credit interest, overdraft, features         |
| empty   | `empty_product_state` — no product resolved for the account |
| error   | `error_state` + retry                                      |

---

## State Model

**ViewModel:** `ProductViewModel`.

**State:** `ProductState` — `accountId: String`, `product: OBProduct2?`, `uiState: ProductUiState`.

The nullable `product` is why `empty` exists as a distinct state: a successful response can still
carry no product.

**Screen state:** sealed `ProductUiState` — `Loading`, `Content`, `Empty`, `Error`.

**Error types**

| Type                    | Cause                                        |
|-------------------------|----------------------------------------------|
| `TokenExpiredError`     | PSU token expired                            |
| `ConsentScopeError`     | Consent lacks `ReadProducts`                 |
| `ProductNotFoundError`  | No product associated with the account       |
| `NetworkError`          | Offline / transport                          |

**Actions:** `ProductLoad`, `RetryLoad`.

**Nav callbacks:** `onBack -> popBackStack()` returning to account-detail.

**DI:** `SavedStateHandle` (carries `accountId`), `ProductRepository`.

---

## Navigation

| From    | To             | Trigger  | Type |
|---------|----------------|----------|------|
| product | account-detail | `onBack` | pop  |

A leaf screen — no forward navigation.

---

## API Endpoints

| ID      | Endpoint                             | Permission     |
|---------|--------------------------------------|----------------|
| product | `GET /accounts/{AccountId}/product`  | `ReadProducts` |

Returns the product (PCA or BCA) associated with the account, including fee tiers, credit-interest
bands and overdraft terms. Full detail: `API.md`.

---

## Design Tokens

Material 3, seed `#266489` ("Open Banking — Trust Blue"), Roboto, with `Roboto Mono` for rates,
thresholds and charges so figures align down each tier list. Components reference semantic roles, so
both theme modes resolve from `design-system/design-tokens.yaml`; `DESIGN.md` is the canonical brand
spec.

---

<!-- Generated 2026-08-04 by /idea-feature-export --all --force from screens/product/{ui,api,flow,docs}.yaml. -->
