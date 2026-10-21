# Visual Specification — Beneficiaries
**Feature:** beneficiaries | **Flavor:** consumer

---

## Screen Layout

Vertical scroll with top app bar ("Beneficiaries" + back + filter_list sort action); no bottom navigation:

```
┌────────────────────────────────────┐
│ ← Beneficiaries              [≡]  │  ← top app bar
├────────────────────────────────────┤
│ 🔍 Search beneficiaries by name... │  ← beneficiary_search_bar
├────────────────────────────────────┤
│  Recently Used                     │  ← recently_used_header
│ ┌──────────────────────────────┐   │
│ │ [JS] John Smith              │   │  ← recent_beneficiary_john
│ │       Barclays UK            │   │
│ │       £500 · 2 days ago      │   │
│ └──────────────────────────────┘   │
│ ┌──────────────────────────────┐   │
│ │ [SW] Sarah Williams          │   │  ← recent_beneficiary_sarah
│ │       HSBC UK                │   │
│ │       £1,200 · 5 days ago    │   │
│ └──────────────────────────────┘   │
│ ┌──────────────────────────────┐   │
│ │ [MC] Michael Chen            │   │  ← recent_beneficiary_michael
│ │       Lloyds Bank            │   │
│ │       £250 · 1 week ago      │   │
│ └──────────────────────────────┘   │
├────────────────────────────────────┤
│  All Beneficiaries            [↕]  │  ← all_beneficiaries_header_row
│ ┌──────────────────────────────┐   │
│ │ [NatWest] James Anderson     │   │  ← beneficiary_item_anderson
│ │            GB29 NWBK ··· 8819│   │
│ │            Last: 12 May 2026  │   │
│ └──────────────────────────────┘   │
│ ┌──────────────────────────────┐   │
│ │ [Santander] Priya Patel      │   │  ← beneficiary_item_patel
│ │            GB72 ABBY ··· 4421│   │
│ └──────────────────────────────┘   │
│                                    │
│                     [+ Add Beneficiary]  ← FAB (floating bottom-right)
└────────────────────────────────────┘
```

---

## Components

### beneficiary_search_bar
- **Style:** variant=outlined, input_type=search, corner_radius `radius.xl`, background `surfaceContainerLow`
- **Padding:** horizontal `spacing.md`
- **Leading icon:** search (`icon.md`, `onSurfaceVariant`)
- **Trailing icon:** clear (`icon.md`, `onSurfaceVariant`) — appears when field is non-empty
- **Placeholder:** "Search beneficiaries by name or IBAN..." — a11y role: search_field

### recently_used_header
- **Content:** "Recently Used"
- **Style:** `titleMedium`, color `onSurface`, font_weight semibold, padding_top `spacing.md`, padding_bottom `spacing.sm`

### Recent Beneficiary Cards (john / sarah / michael)

Each card follows the same composition:

| Property | Value |
|---|---|
| Background | `surfaceContainerLowest` |
| Corner radius | `radius.md` |
| Elevation | 1 |
| Padding | horizontal `spacing.md`, vertical `spacing.md` |
| Border | `border.thin` `outlineVariant` |
| On tap | Navigate → send-money (pre-fill counterparty) |

**Internal layout (horizontal row):**
- **Avatar circle (44 dp diameter):** all three share `secondaryContainer` fill with initials in `onSecondaryContainer` at `titleMedium` bold ("JS" / "SW" / "MC"). The initials are the identifier; the circle is a neutral holder.
- **Info column (vertical, flex 1):**
  - Name: `titleMedium` or `bodyMedium` weight 500, `onSurface`
  - Bank name: `bodySmall`, `onSurfaceVariant`
  - Last payment: `bodySmall`, `onSurfaceVariant`, amount in Roboto Mono — e.g. "£500 · 2 days ago"

### section_divider
- **Color:** `outlineVariant`, thickness `border.thin`, padding_vertical `spacing.sm`

### all_beneficiaries_header_row
- **Layout:** horizontal, space-between, align center, padding_vertical `spacing.xs`
- **Left:** "All Beneficiaries" — `titleMedium`, `onSurface`, weight semibold
- **Right:** sort icon (sort, `icon.md`, `primary`) — tappable, triggers sort bottom sheet

### beneficiary_item_anderson — James Anderson (NatWest)
- **Same card style as recent beneficiary cards**
- **Left element:** NatWest logo image (32×32, corner_radius `radius.xs`, content_scale=fit)
- **Info column:**
  - "James Anderson" — `bodyMedium`, weight 500, `onSurface`
  - "GB29 NWBK ··· 8819" — `bodySmall`, `onSurfaceVariant`, Roboto Mono
  - "Last: 12 May 2026" — `bodySmall`, `onSurfaceVariant`

### beneficiary_item_patel — Priya Patel (Santander)
- **Left element:** Santander logo image (32×32)
- **IBAN:** "GB72 ABBY ··· 4421" — `bodySmall`, `onSurfaceVariant`, Roboto Mono

### add_beneficiary_fab
- **Style:** filled, container `primary`, label `onPrimary`, corner_radius `radius.lg`, elevation 6
- **Position:** floating_action_button (fixed bottom-right)
- **Label:** "Add Beneficiary"
- **Leading icon:** person_add (`icon.md`)

---

## Interaction Patterns

| Target | Gesture | Outcome |
|---|---|---|
| beneficiary_search_bar | Type | SearchQueryChanged event; filteredBeneficiaries updated live; state=searching |
| beneficiary_search_bar trailing clear | Tap | Clear search; reset to content state |
| recent_beneficiary_john | Tap | Navigate → send-money pre-filled with John Smith / Barclays UK |
| recent_beneficiary_sarah | Tap | Navigate → send-money pre-filled with Sarah Williams / HSBC UK |
| recent_beneficiary_michael | Tap | Navigate → send-money pre-filled with Michael Chen / Lloyds Bank |
| beneficiary_item_anderson | Tap | Navigate → send-money pre-filled with James Anderson / NatWest |
| beneficiary_item_patel | Tap | Navigate → send-money pre-filled with Priya Patel / Santander |
| sort_button | Tap | SortChanged event; sort bottom sheet opens (Alpha A-Z / Alpha Z-A / Recent) |
| Top app bar filter_list | Tap | sort_beneficiaries action (same as sort_button) |
| add_beneficiary_fab | Tap | AddBeneficiaryClicked event → open_add_beneficiary_sheet bottom sheet |

---

## Content Data

| Beneficiary | Bank | IBAN / Routing | Last Payment |
|---|---|---|---|
| John Smith | Barclays UK | (full IBAN in API) | £500 · 2 days ago |
| Sarah Williams | HSBC UK | (full IBAN in API) | £1,200 · 5 days ago |
| Michael Chen | Lloyds Bank | (full IBAN in API) | £250 · 1 week ago |
| James Anderson | NatWest | GB29 NWBK ··· 8819 | 12 May 2026 |
| Priya Patel | Santander UK | GB72 ABBY ··· 4421 | (from API) |

---

## Design Notes

- **Avatars are one neutral treatment, not three hues:** every recent-beneficiary avatar uses `secondaryContainer` with `onSecondaryContainer` initials. The previous spec assigned each payee its own colour (brand purple / teal / secondary purple) to "prevent visual monotony" — but two of those hues are outside this palette entirely, and the initials already do the identifying work the colour was claiming to do. Restraint is the point in a regulated-industry system: colour here would carry no meaning.
- **Recency metadata is neutral:** last-payment text uses `onSurfaceVariant` rather than an accent. Recency is context, not status, and this palette reserves its coloured roles for money direction and payment disposition.
- **Masked IBANs:** only the last 4 digits are shown (GB29 NWBK ··· 8819) for privacy. Roboto Mono makes partial IBANs easy to verify at a glance and matches every other account identifier in the app.
- **Two-section layout:** "Recently Used" (frequency-based, max 3) above "All Beneficiaries" (alphabetical, sortable) mirrors UX patterns from WhatsApp contacts and Apple Pay recents, reducing friction for repeat payments.
- **No bottom nav:** Beneficiaries is reached from within the payment flow or the More menu; removing the bottom nav keeps the user focused on counterparty selection.
- **Search corner radius:** the pill-shaped `radius.xl` search field (vs the `radius.md` cards) visually differentiates the input from list items, a common Material You pattern.
- **Empty state:** uses the `person_off` illustration icon with the action-oriented message "Add a beneficiary to start sending money quickly" — the FAB remains visible so the user has an immediate path forward.
- **FAB label visible:** the extended "Add Beneficiary" FAB (not icon-only) is used because users may not recognise the `person_add` icon, especially new users in the empty state.

---

_Generated by /idea export | 2026-08-03_
