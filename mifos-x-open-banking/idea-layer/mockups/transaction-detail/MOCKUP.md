# Visual Specification — Transaction Detail
**Feature:** transaction-detail | **Flavor:** consumer

---

## Screen Layout

Vertical scroll with top app bar ("Transaction Details" + back + share); no bottom navigation:

```
┌────────────────────────────────────┐
│ ← Transaction Details        [↗]  │  ← top app bar
├────────────────────────────────────┤
│                                    │
│           -£42.50                  │  ← amount_hero_section (bg `primary`)
│        ✓ Settled                   │  ← status_badge (`primaryContainer` pill)
│                                    │
├────────────────────────────────────┤
│ ┌──────────────────────────────┐   │
│ │ [Tesco Logo] Tesco Supermarket│  │  ← merchant_card (elevation 4,
│ │             [Groceries]       │  │    negative top margin overlap)
│ └──────────────────────────────┘   │
│                                    │
│ ┌──────────────────────────────┐   │
│ │ Date & Time    25 May 2026, 14:32│ ← details_card
│ │──────────────────────────────│   │
│ │ Reference      SEPA-202605.. [⎘]│
│ │──────────────────────────────│   │
│ │ Transaction Type  SEPA Credit Transfer │
│ │──────────────────────────────│   │
│ │ From Account   Primary Checking │ │
│ │                ...0130          │ │
│ │──────────────────────────────│   │
│ │ To Beneficiary    Tesco PLC     │ │
│ │                DE89 3704...0044 │ │
│ └──────────────────────────────┘   │
│                                    │
│ [Download Receipt]                 │  ← outlined button `primary`
│      🚩 Report an Issue            │  ← `error` link
└────────────────────────────────────┘
```

---

## Components

### amount_hero_section — Hero
- **Background:** `primary`, full width, padding horizontal `spacing.lg`, top `spacing.lg`, bottom `spacing.xl`, align: center
- **amount_hero_value:** "-£42.50" — typography: `displayLarge`, color: `onPrimary`, Roboto Mono, font_weight: 700, text_align: center
- **status_badge_row:** centered horizontally below amount
  - Pill: background `primaryContainer`, border_radius `radius.lg`, padding horizontal `spacing.md` vertical `spacing.xs`
  - Inner row: check_circle icon (`icon.xs`, `onPrimaryContainer`) + "Settled" text (`labelMedium`, `onPrimaryContainer`)

### merchant_card
- **Position:** margin_horizontal `spacing.md`, negative top margin of `spacing.md` (overlaps hero), margin_bottom `spacing.md`
- **Style:** background `surfaceContainerLowest`, border_radius `radius.lg`, padding `spacing.md`, elevation 4
- **merchant_row (horizontal, spacing `spacing.md`):**
  - **merchant_logo:** 56×56 circle, background `primaryContainer`, border_radius `radius.full` — Tesco logo image
  - **merchant_info (vertical, flex 1):**
    - "Tesco Supermarket" — `titleLarge`, `onSurface`, weight 600
    - category_badge: "Groceries" chip — background `secondaryContainer`, border_radius `radius.xs`, padding horizontal `spacing.sm` vertical `spacing.xs`, text `labelSmall`, color `onSecondaryContainer`, align_self flex_start, margin_top `spacing.xs`

### details_card
- **Style:** background `surfaceContainerLowest`, border_radius `radius.lg`, padding `spacing.md`, margin_horizontal `spacing.md`, elevation 1
- **Each field row:** horizontal layout, space-between, padding_bottom `spacing.md` (except last row)
- **Between each row:** `outlineVariant` divider (`border.thin`), margin_bottom `spacing.md`
- **Label style:** `labelSmall`, `onSurfaceVariant`, letter_spacing 0.4
- **Value style:** `bodyMedium`, `onSurface`, weight 500

| Row | Label | Value |
|---|---|---|
| detail_date_row | "Date & Time" | "25 May 2026, 14:32" |
| detail_reference_row | "Reference" | "SEPA-2026051500123" (Roboto Mono, `bodySmall`) + copy icon |
| detail_type_row | "Transaction Type" | "SEPA Credit Transfer" |
| detail_from_row | "From Account" | "Primary Checking" (weight 500) + "...0130" (`bodySmall`, `onSurfaceVariant`, Roboto Mono) |
| detail_to_row | "To Beneficiary" | "Tesco PLC" (weight 500) + "DE89 3704...0044" (`bodySmall`, `onSurfaceVariant`, Roboto Mono) |

### download_receipt_button
- **Style:** variant=outlined, border_color `outline` (`border.thin`), text_color `primary`, border_radius `radius.md`
- **Padding:** vertical `spacing.md`, margin_horizontal `spacing.md`, margin_bottom `spacing.md`
- **Label:** "Download Receipt", typography `labelLarge`
- **Leading icon:** download (`icon.sm`)

### report_issue_row
- **Layout:** horizontal, centered, padding_bottom `spacing.lg`
- **flag icon:** `icon.xs`, `error`, padding_right `spacing.xs`
- **"Report an Issue" link:** `labelMedium`, `error` — taps open dispute form

---

## Interaction Patterns

| Target | Gesture | Outcome |
|---|---|---|
| Top app bar back | Tap | NavigateBack event → pop to transactions |
| Top app bar share icon | Tap | ShareTransaction event → system share sheet |
| copy_reference_icon | Tap | CopyReference event; referenceCopied=true (brief snackbar "Copied") |
| download_receipt_button | Tap | DownloadReceipt event; isDownloadingReceipt=true → PDF download progress |
| report_issue_link | Tap | OpenDisputeForm event → dispute form screen / bottom sheet |

---

## Content Data

| Element | Value |
|---|---|
| Transaction amount | -£42.50 |
| Status | Settled |
| Merchant | Tesco Supermarket |
| Category | Groceries |
| Date & Time | 25 May 2026, 14:32 |
| Reference | SEPA-2026051500123 |
| Transaction type | SEPA Credit Transfer |
| From account | Primary Checking (IBAN: ...0130) |
| To beneficiary | Tesco PLC (IBAN: DE89 3704...0044) |

---

## Design Notes

- **Amount colour on hero:** the hero fills with `primary`, so the amount is set in `onPrimary` — the role the palette guarantees meets AA against it. The debit direction is carried by the leading minus sign and the screen's "money out" framing, not by hue. Painting a red amount onto the blue hero was the previous approach; `error` red on `primary` blue cannot reach AA, and DESIGN.md is explicit that this palette never signals money direction with a red/green pair.
- **Status vocabulary:** the badge reads **Settled**, not "Completed". Per DESIGN.md's payment-disposition table a settled payment is `primary` with `primaryContainer` / `onPrimaryContainer` and a `check_circle` icon (7.27:1). An `AcceptedSettlementInProcess` result would instead render as **In progress** in `secondary` with a `schedule` icon — never as success.
- **Hero overlap pattern:** merchant_card uses a negative top margin of `spacing.md` to float above the hero bottom edge — the elevation 4 shadow makes it feel physically lifted off the hero. Same technique as account-detail, for visual continuity across the banking flow.
- **Reference monospace:** SEPA-2026051500123 is set in Roboto Mono at `bodySmall` so digit grouping reads as a code, distinct from prose text — the same `typography.mono` contract the `amount` component uses.
- **Masked IBANs:** source shows "...0130" (last 4 chars), destination shows "DE89 3704...0044" — partial disclosure protects counterparty privacy while giving enough context for recognition.
- **No bottom nav:** this is a leaf screen — removing the nav bar maximises vertical space for the structured details and signals there is no lateral navigation from this context.
- **Loading skeleton:** hero keeps its `primary` fill (background persists); merchant card and details card are replaced by `surfaceVariant` blocks to prevent layout jump on data arrival.

---

_Generated by /idea export | 2026-08-03_
