# Visual Specification — Products

| Field | Value |
|---|---|
| Feature | products |
| Flavor | consumer |
| Archetype | index_list |
| States | loading, populated, empty, error |

---

## Screen Layout (populated state)

Top app bar: title "Products", back arrow (left), search icon (right).
Bottom navigation: 5 items — Home | Accounts | **Products (active)** | Send | More.
Main content: vertically scrollable column, background `surface`.

```
┌─────────────────────────────────┐
│ ← Products                   🔍 │  ← top app bar
├─────────────────────────────────┤
│                                 │
│  Products                       │  ← headlineLarge `primary` bold
│  Explore accounts, savings,     │
│  loans and cards tailored       │
│  for you.                       │  ← bodyMedium `on_surface_variant`
│                                 │
│  [All] [Savings] [Loans]        │
│        [Cards] [Mortgages]  →   │  ← horizontal scroll chip row
│                                 │
│ ┌─────────────────────────────┐ │
│ │ Instant Access Savings  Savings│ ← product card 1
│ │ 4.5% AER                    │ │  ← displaySmall `primary` bold
│ │ Earn 4.5% AER on every...   │ │
│ │ [4.5% AER][Instant access]  │ │  ← feature badge chips
│ │ [No minimum deposit]        │ │
│ │               [Details][Apply Now]│
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ Fixed Rate Bond 1yr   Savings│  ← product card 2
│ │ 5.1% AER                    │ │
│ │ Lock in a market-leading... │ │
│ │ [5.1% AER][12-month term]   │ │
│ │ [FSCS protected]            │ │
│ │               [Details][Apply Now]│
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ Personal Loan           Loans│  ← product card 3
│ │ From 6.9% APR               │ │
│ │ Borrow from £1,000 to...    │ │
│ │ [From 6.9% APR][Up to £25k] │ │
│ │ [1–7 year terms]            │ │
│ │               [Details][Apply Now]│
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ Platinum Credit Card    Cards│  ← product card 4
│ │ 0% for 20 months            │ │
│ │ 0% interest on purchases... │ │
│ │ [0% for 20 months]          │ │
│ │ [No annual fee][Contactless]│ │
│ │               [Details][Apply Now]│
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ 🎁 Refer a friend — earn £50 │  ← promo banner `primary` bg
│ │ When your friend opens any  │ │
│ │ account before 30 June 2026 │ │
│ └─────────────────────────────┘ │
│                                 │
├─────────────────────────────────┤
│  🏠  💳  🏪  ↗  ⋯              │  ← bottom nav
└─────────────────────────────────┘
```

---

## Category Filter Chip Row

- **Layout:** Horizontally scrollable row, padding_horizontal `spacing.md`, spacing `spacing.sm` between chips
- **Chip style:** corner_radius `radius.lg`, padding_horizontal `spacing.md`, padding_vertical `spacing.sm`, `labelMedium`
- **Active chip (All):** Filled `primary`, `on_primary` text
- **Inactive chips:** Outlined, border `outline` (`border.thin`), text `on_surface_variant`
- **Chips (L→R):** All | Savings | Loans | Cards | Mortgages

---

## Product Cards — Common Structure

All four cards share the same container style:

| Property | Value |
|---|---|
| background | `surface` |
| corner_radius | `radius.lg` |
| elevation | 2 |
| padding_horizontal | `spacing.md` |
| padding_vertical | `spacing.md` |
| border | `outline`, `border.thin` |
| margin_horizontal | `spacing.md` |
| margin_bottom | `spacing.md` |

**Internal layout (top to bottom):**

1. **Header row** (horizontal, space_between): product name (`titleMedium`, `on_surface`, semi-bold) + category badge chip (`labelSmall`, `secondary_container`)
2. **Rate badge** (`displaySmall`, `primary`, bold, Roboto Mono) — the prominent rate or offer
3. **Description** (`bodyMedium`, `on_surface_variant`) — 1–2 line sentence
4. **Feature badges row** (horizontal scroll, spacing `spacing.sm`) — 2–3 chips
5. **Actions row** (right-aligned): "Details" (outlined `primary`) + "Apply Now" (filled `primary` / `on_primary`), both corner_radius `radius.sm`

**Badge role vocabulary** — two roles, assigned by meaning rather than by category:

| Role | Used for | Tokens |
|---|---|---|
| **Headline benefit** | the return or offer that is the reason to choose the product | `primary_container` / `on_primary_container` |
| **Product fact** | access terms, duration, limits, protections, payment features | `secondary_container` / `on_secondary_container` |

---

## Product Card Detail — Instant Access Savings

| Element | Content | Style |
|---|---|---|
| Name | Instant Access Savings | `titleMedium`, `on_surface`, semi-bold |
| Category badge | Savings | `secondary_container` bg, `on_secondary_container` text |
| Rate | 4.5% AER | `displaySmall`, `primary`, bold, Roboto Mono |
| Description | "Earn 4.5% AER on every pound you save. Withdraw at any time with no notice period or penalties." | `bodyMedium`, `on_surface_variant` |
| Badge 1 (benefit) | 4.5% AER | `primary_container` bg, `on_primary_container` text |
| Badge 2 (fact) | Instant access | `secondary_container` bg, `on_secondary_container` text |
| Badge 3 (fact) | No minimum deposit | `secondary_container` bg, `on_secondary_container` text |
| Button 1 | Details | outlined `primary` |
| Button 2 | Apply Now | filled `primary`, `on_primary` text |

---

## Product Card Detail — Fixed Rate Bond 1yr

| Element | Content | Style |
|---|---|---|
| Name | Fixed Rate Bond 1yr | `titleMedium`, `on_surface`, semi-bold |
| Category badge | Savings | `secondary_container` bg, `on_secondary_container` text |
| Rate | 5.1% AER | `displaySmall`, `primary`, bold, Roboto Mono |
| Description | "Lock in a market-leading 5.1% AER for 12 months. Minimum deposit £1,000. Interest paid at maturity." | `bodyMedium`, `on_surface_variant` |
| Badge 1 (benefit) | 5.1% AER | `primary_container` bg, `on_primary_container` text |
| Badge 2 (fact) | 12-month term | `secondary_container` bg, `on_secondary_container` text |
| Badge 3 (fact) | FSCS protected | `secondary_container` bg, `on_secondary_container` text |
| Button 1 | Details | outlined `primary` |
| Button 2 | Apply Now | filled `primary`, `on_primary` text |

---

## Product Card Detail — Personal Loan

| Element | Content | Style |
|---|---|---|
| Name | Personal Loan | `titleMedium`, `on_surface`, semi-bold |
| Category badge | Loans | `secondary_container` bg, `on_secondary_container` text |
| Rate | From 6.9% APR | `displaySmall`, `primary`, bold, Roboto Mono |
| Description | "Borrow from £1,000 to £25,000 at a representative 6.9% APR. Flexible repayment terms from 1 to 7 years." | `bodyMedium`, `on_surface_variant` |
| Badge 1 (benefit) | From 6.9% APR | `primary_container` bg, `on_primary_container` text |
| Badge 2 (fact) | Up to £25,000 | `secondary_container` bg, `on_secondary_container` text |
| Badge 3 (fact) | 1–7 year terms | `secondary_container` bg, `on_secondary_container` text |
| Button 1 | Details | outlined `primary` |
| Button 2 | Apply Now | filled `primary`, `on_primary` text |

---

## Product Card Detail — Platinum Credit Card

| Element | Content | Style |
|---|---|---|
| Name | Platinum Credit Card | `titleMedium`, `on_surface`, semi-bold |
| Category badge | Cards | `secondary_container` bg, `on_secondary_container` text |
| Rate | 0% for 20 months | `displaySmall`, `primary`, bold, Roboto Mono |
| Description | "0% interest on purchases for 20 months. No annual fee. Contactless and Apple Pay / Google Pay enabled." | `bodyMedium`, `on_surface_variant` |
| Badge 1 (benefit) | 0% for 20 months | `primary_container` bg, `on_primary_container` text |
| Badge 2 (fact) | No annual fee | `secondary_container` bg, `on_secondary_container` text |
| Badge 3 (fact) | Contactless & Apple/Google Pay | `secondary_container` bg, `on_secondary_container` text |
| Button 1 | Details | outlined `primary` |
| Button 2 | Apply Now | filled `primary`, `on_primary` text |

---

## Promotional Banner

```
┌─────────────────────────────────────┐
│  🎁  Refer a friend — earn £50      │  ← titleSmall, `on_primary`, semi-bold
│     When your friend opens any      │  ← bodySmall, `primary_container`
│     account before 30 June 2026     │
└─────────────────────────────────────┘
```

| Property | Value |
|---|---|
| Background | `primary` |
| corner_radius | `radius.md` |
| padding_horizontal | `spacing.md` |
| padding_vertical | `spacing.md` |
| margin_horizontal | `spacing.md` |
| margin_bottom | `spacing.md` |
| on_click | navigates to home (referral flow) |

---

## State — Loading

```
┌─────────────────────────────────┐
│  Products                       │
│  Explore accounts, savings...   │
│  [All] [Savings] [Loans] [Cards][Mortgages]→
│                                 │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │  ← skeleton card 1
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │  ← skeleton card 2
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │  ← skeleton card 3
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │  ← skeleton card 4
└─────────────────────────────────┘
```

- Title, subtitle, and all 5 category tabs visible
- 4 skeleton placeholders in `surface_container` matching the card shape (shimmer animation)
- Promotional banner not shown

---

## State — Empty

```
┌─────────────────────────────────┐
│  Products                       │
│  Explore accounts, savings...   │
│  [All] [Savings] [Loans] [Cards][Mortgages]→
│                                 │
│           🏪                    │  ← store_outlined icon, `outline`
│    No products available        │  ← titleMedium, `on_surface`
│  No products match the selected │
│  category. Try a different      │
│  filter or check back later.    │  ← bodyMedium `on_surface_variant`
└─────────────────────────────────┘
```

- Triggered when the category filter returns zero matching products
- Empty-state icon: `store_outlined`
- Title: "No products available"
- Message: "No products match the selected category. Try a different filter or check back later."

---

## State — Error

```
┌─────────────────────────────────┐
│  Products                       │
│  Explore accounts, savings...   │
│  [All] [Savings] [Loans] [Cards][Mortgages]→
│                                 │
│           ☁️✗                   │  ← cloud_off icon, `outline`
│  Unable to load products        │  ← titleMedium, `on_surface`
│  Check your connection and try  │
│  again. Your saved favourites   │
│  are still available offline.   │  ← bodyMedium `on_surface_variant`
│                                 │
│            [ Try Again ]        │  ← filled `primary` retry button
└─────────────────────────────────┘
```

- Error icon: `cloud_off`
- Title: "Unable to load products"
- Message: "Check your connection and try again. Your saved favourites are still available offline."
- Retry button: filled `primary` / `on_primary`, dispatches `RetryLoad` event

---

## Interaction Patterns

| Component | Gesture | Result |
|---|---|---|
| tab_all / tab_savings / tab_loans / tab_cards / tab_mortgages | Tap | `filter_products` action — active chip updates; product list filters client-side |
| Product card body (any) | Tap | `navigate` → application-detail with product code |
| ias_learn_more / frb_learn_more / personal_loan_learn_more / pcc_learn_more | Tap | `navigate` → application-detail (Details view) |
| ias_apply / frb_apply / personal_loan_apply / pcc_apply | Tap | `navigate` → application-detail (Apply Now entry) |
| promotions_banner | Tap | `navigate` → home (referral flow) |
| top app bar search icon | Tap | `search_products` — search overlay activates |
| top app bar back arrow | Tap | `navigate_back` → home |
| bottom nav — Home | Tap | replace → home |
| bottom nav — Accounts | Tap | replace → accounts |
| bottom nav — Send | Tap | replace → send-money |
| Retry button (error state) | Tap | `RetryLoad` event → re-fetches OBP products endpoint |

---

## Design Notes

**Rate badge hierarchy:**
The `displaySmall` rate figure is the primary visual anchor on each card. Its `primary` colour ties every product back to the brand, and the large size creates an instant value-scanning affordance for a user comparing rates. It is set in Roboto Mono so percentages align down the list.

**Badges carry meaning, not taxonomy:**
The previous spec ran a four-hue semantic system — green for gain, blue for access, orange for borrowing, purple for protection — and none of those families exist in this palette. Worse, the scheme asked colour to encode a distinction the badge text already states. Badges now use exactly two roles: **`primary_container` for the headline benefit** (the rate or offer that is the reason to pick the product) and **`secondary_container` for every product fact** (term, limit, protection, payment features). One glance finds the number that matters; everything else reads as equal-weight detail.

**Category badges are neutral:**
Savings / Loans / Cards / Mortgages all take `secondary_container`. Category is a taxonomy label, not a status, and the previous colour-per-category scheme would have forced a loan product into the `tertiary` warning role — which DESIGN.md 1.3.0 reserves for attention-needed states. A loan on offer is not a warning.

**Promotional banner placement:**
Placed below all product cards so it does not interrupt the primary browsing flow but is still encountered before the user reaches the bottom of the list. The subtitle uses `primary_container` on the `primary` background — enough contrast to read comfortably while sitting softer than full `on_primary`.

**Accessibility:**
- Each product card has a full accessibility label: name + rate + primary benefit + action hint.
- Category tabs declare `role: tab` and `selected` state for screen readers.
- Apply Now and Details buttons have distinct `content_description` per product.
- Error and empty states are announced as live regions.

---

*Generated by /idea export | 2026-08-03*
