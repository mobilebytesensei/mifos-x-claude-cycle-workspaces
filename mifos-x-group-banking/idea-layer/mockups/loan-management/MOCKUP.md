# Loan Management — Mockup Specification
**Feature**: loan-management | **Screens**: loan-list, loan-apply, loan-detail, meeting-conduct (steps 4–5)

---

## Design Language

**System**: Material Design 3 (MD3) — comfortable density
**Font**: Noto Sans (optimised for multilingual rural users)
**Primary**: #2E7D32 (VSLA green) — all CTAs, active states, TopBar backgrounds
**Secondary**: #FF8F00 (amber) — highlights, secondary actions
**Error**: #D32F2F (red) — overdue indicators, Mark Defaulted button
**Min touch target**: 48dp (48dp for non-primary, 56dp for primary CTAs)
**Corner radius**: 12dp (cards), 24dp (buttons), 8dp (text fields)

---

## Screen 1: Loan List (`/groups/{groupId}/loans`)

### Layout
```
┌─────────────────────────────────────────┐
│ [←] Group Loans               [#2E7D32] │  TopAppBar — primary bg, white text
├─────────────────────────────────────────┤
│ [All][Active][Overdue][Closed]           │  FilterChipRow — horizontal scroll, 8dp gap
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │ [PO] Peter Otieno         [Active]  │ │  LoanCard — surface bg, elevation 2dp
│ │      KES 15,000                     │ │  Member avatar 40dp, fallback person icon
│ │      Outstanding: KES 11,250        │ │  Status badge: #C8E6C9 bg / #1B5E20 text
│ │      Next: 2026-05-12               │ │  bodySmall for outstanding + next date
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ [GW] Grace Wanjiku        [Overdue] │ │  Overdue card — errorContainer badge
│ │      KES 3,000                      │ │
│ │      Outstanding: KES 2,625         │ │
│ │      OVERDUE — KES 375              │ │  Red label labelSmall bold
│ └─────────────────────────────────────┘ │
│                                    [+]  │  FAB — primary #2E7D32, "Apply for Loan"
└─────────────────────────────────────────┘
```

### States
- **Loading**: 5× shimmer cards, height 96dp, corner 12dp, surfaceVariant bg
- **Content**: Filter chips row + loan cards + FAB (chairperson/treasurer only)
- **Empty**: account_balance_wallet icon, "No loans yet", chip-filtered empty body
- **Error**: cloud_off icon, error message, "Retry" CTA

### Filter Chip Styles
| Chip | Selected BG | Active text |
|------|------------|-------------|
| All | primaryContainer | onPrimaryContainer |
| Active | primaryContainer | onPrimaryContainer |
| Overdue | errorContainer | onErrorContainer |
| Closed | surfaceVariant | onSurfaceVariant |

---

## Screen 2: Loan Apply (`/groups/{groupId}/loans/apply`)

### Layout
```
┌─────────────────────────────────────────┐
│ [←] Apply for Loan            [#2E7D32] │  TopAppBar
├─────────────────────────────────────────┤
│ [Select Member ▼]                        │  Dropdown, 48dp min, person icon leading
├─────────────────────────────────────────┤
│ ┌ Savings balance: KES 5,000 ─────────┐ │  Eligibility banner — primaryContainer
│ │ Max eligible: KES 15,000 (3× savings)│ │  Visible when member selected
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ [KES] Requested Amount (KES)            │  TextField — decimal keyboard, currency_exchange icon
├─────────────────────────────────────────┤
│ ┌ Warning: corpus below 10% buffer ──┐  │  Warning banner — #FFF9C4 bg, visible when flag
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ [Loan Duration ▼] [12 weeks]            │  Dropdown — 4/8/12/24/52 weeks options
├─────────────────────────────────────────┤
│ [Loan Purpose ▼] [Business]             │  Dropdown — Medical/Education/Business/Emergency/Other
├─────────────────────────────────────────┤
│ [Loan Product ▼]                        │  Dropdown — loads from /loanproducts
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │       Submit Application            │ │  FilledButton — primary, 56dp, full width
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Validation Rules
- Amount field shows error text when `requestedAmount > eligibleAmount` (labelSmall, error color)
- Corpus warning banner visible when `corpusBalance - requestedAmount < corpusBalance * 0.10`
- Submit button disabled until `selectedMember != null && requestedAmount.isNotBlank() && amountError == null && selectedProduct != null`
- Submit button shows CircularProgressIndicator during `isSubmitting`

---

## Screen 3: Loan Detail (`/loans/{loanId}`)

### Layout
```
┌─────────────────────────────────────────┐
│ [←] Loan Detail              [refresh]  │  TopAppBar + refresh action icon
├─────────────────────────────────────────┤
│ ┌ Peter Otieno ─────────────[Active] ─┐ │  Member header card — primaryContainer bg
│ │ Standard Group Loan                  │ │
│ │ Principal: KES 15,000                │ │
│ │ Disbursed: 2026-04-14  5% per week   │ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ [Outstanding: KES 11,250] [Overdue: —]  │  Info chips row — secondaryContainer
├─────────────────────────────────────────┤
│ [Schedule]  [Repayment History]          │  TabBar — primary indicator
├─────────────────────────────────────────┤
│  Wk │ Due Date  │ Due    │ Paid   │ Bal  │  Data table — Schedule tab
│   1 │ 2026-04-21│ 2,000  │ 2,000  │   0  │  PAID row: #F1F8E9 bg, #33691E text
│   2 │ 2026-04-28│ 1,937  │ 1,937  │   0  │  UPCOMING row: surface bg
│   3 │ 2026-05-05│ 1,875  │ 1,875  │   0  │
│   4 │ 2026-05-12│ 1,812  │   0    │1,812 │  UPCOMING — default surface color
├─────────────────────────────────────────┤
│ [Record Repayment]  [Mark Defaulted]     │  Action row — Record: primary, Defaulted: error
└─────────────────────────────────────────┘
```

### Tab: Repayment History
- List of RepaymentTransaction rows: type text + date (bodySmall, onSurfaceVariant) + amount (bodyMedium, primary)
- Empty text: "No repayments recorded yet."

### Role-gated Actions
- "Record Repayment" button: visible only when `canRecordRepayment && loan.status == ACTIVE`
- "Mark Defaulted" button: visible only when `canMarkDefaulted && loan.status == OVERDUE`

---

## Meeting Conduct — Step 4 (Loan Review)

Per-member loan review row with:
- Avatar (40dp, secondaryContainer BG, red errorContainer BG when overdue)
- Member name (bodyLarge) + loan summary text (bodySmall, onSurfaceVariant)
- OVERDUE chip (errorContainer bg) when `loan.isOverdue`
- Repayment TextField (48dp min, hint: "Expected: KES 1,250")
- Penalty fine TextField (48dp min, only visible for overdue loans)

## Meeting Conduct — Step 5 (Loan Applications)

Per-application card:
- Member name (titleSmall) + requested amount (bodyLarge) + purpose (bodySmall, onSurfaceVariant)
- Vote tally: "3 For · 1 Against" (labelMedium, outline color)
- [For] OutlinedButton (selectedBG: primaryContainer) + [Against] OutlinedButton (selectedBG: errorContainer)
- [Chairperson Approve] FilledButton — primary bg, enabled only when majority For + current user is Chairperson
- Corpus gate chip showing available disbursement balance (tertiaryContainer)

---

## Interaction Patterns

1. **Filter selection**: Tap chip → client-side filter, no API call, instant result
2. **Loan card tap**: Ripple animation (standard easing, 200ms) → navigate to loan-detail
3. **FAB tap**: Scale animation 0.85→1.0 (emphasized easing, 300ms) → navigate to loan-apply
4. **Submit button**: Disabled state shows outline style → enabled when valid → loading shows spinner
5. **Pull to refresh**: Standard Material refresh indicator, invalidates cache, re-fetches
6. **Pagination**: Scroll to end triggers `OnLoadNextPage`, appends 20 more items

---

## Accessibility

- All cards have `contentDescription` with full loan info for screen readers
- Overdue indicator has explicit "OVERDUE" text (not color-only)
- Status badges use both color AND text label
- Minimum touch targets: 48dp (cards 72dp min height)
- Focus ring: 3dp, follows MD3 focus indicator spec
- Noto Sans supports English, Swahili, French, Hindi character sets
