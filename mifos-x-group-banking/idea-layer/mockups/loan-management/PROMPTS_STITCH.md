# Loan Management — Prompts Stitch
**Feature**: loan-management | **Project**: MifosSave (mifos-x-group-banking)
**Screens**: loan-list, loan-apply, loan-detail, meeting-conduct steps 4–5

---

## 1. Design System Context

### Brand Identity
MifosSave is a VSLA (Village Savings and Loan Association) group banking app designed for rural communities in Sub-Saharan Africa and South Asia. The visual language communicates financial trust, growth, and community — anchored in Material Design 3 with a carefully crafted tonal palette.

### Primary Color System
- **Primary**: `#2E7D32` — deep VSLA green. Represents growth, stability, nature, and financial health. Used on: TopAppBar backgrounds, FAB fill, primary buttons, active filter chips, loan status badges (active), tab indicators, progress bars.
- **On Primary**: `#FFFFFF` — white text/icons on primary surfaces. Contrast ratio 13.5:1 (AAA).
- **Primary Container**: `#A6F1A6` — light green. Used on: selected filter chips, eligibility banner background, active loan badge background, cycle progress cards, member savings total chips.
- **On Primary Container**: `#002106` — very dark green. Text on primaryContainer surfaces. Contrast excellent.

### Secondary Color System
- **Secondary**: `#FF8F00` — warm amber. Represents shared coin, harvest, and communal wealth. Used on: individual savings charts (amber line), secondary outlined buttons, info chips for savings balances, sync status icons.
- **On Secondary**: `#FFFFFF` — white on amber surfaces.
- **Secondary Container**: `#FFDDB3` — light amber. Used on: member avatars background, savings-related chip backgrounds, info chips.
- **On Secondary Container**: `#2A1700` — very dark amber-brown.

### Tertiary Color System
- **Tertiary**: `#1565C0` — trust blue. Used on: corpus fund balance displays, informational chips, link text.
- **On Tertiary**: `#FFFFFF` — white on blue.
- **Tertiary Container**: `#D2E4FF` — light blue. Used on: corpus band background, fund summary cards.
- **On Tertiary Container**: `#001C39` — very dark navy.

### Error / Warning Color System
- **Error**: `#D32F2F` — deep red. Used on: overdue loan indicators, Mark Defaulted button, repayment exceed validation text.
- **On Error**: `#FFFFFF` — white on error.
- **Error Container**: `#FFDAD6` — light pink/red. Used on: overdue status badge backgrounds, overdue filter chip selected, failed sync item rows.
- **On Error Container**: `#410002` — very dark red. Text on error container surfaces.
- **Warning (custom)**: `#FFF9C4` background / `#E65100` text — corpus depletion warning banner. Not a MD3 standard role but used for corpus warning.

### Surface Colors
- **Background**: `#FFFFFF` — pure white page background.
- **Surface**: `#FAFAFA` — off-white card and container backgrounds.
- **Surface Variant**: `#DEE5DA` — slightly green-tinted grey. Used on: shimmer skeletons, dividers, unselected filter chips, closed loan badge.
- **On Surface**: `#1A1C19` — near-black. Primary body text.
- **On Surface Variant**: `#424942` — medium grey with green hint. Secondary text, subtitles, supporting text.
- **Outline**: `#727971` — medium border/divider color.
- **Outline Variant**: `#C2C9BD` — lighter divider.

### Typography Scale (Noto Sans)
All sizes are in `sp` (scale-independent pixels, scale_style: large for rural accessibility).

| Style | Size sp | Line Height sp | Tracking | Weight | Used For |
|-------|---------|----------------|----------|--------|----------|
| displaySmall | 36 | 44 | 0 | 400 | Corpus balance large display |
| headlineLarge | 32 | 40 | 0 | 400 | Screen section titles |
| headlineMedium | 28 | 36 | 0 | 400 | KPI card values |
| headlineSmall | 24 | 32 | 0 | 400 | Member name on detail header, loan product title |
| titleLarge | 22 | 28 | 0 | 500 | Total distribution pool value |
| titleMedium | 16 | 24 | 0.15 | 500 | Loan card member name, step titles, section headers |
| titleSmall | 14 | 20 | 0.1 | 500 | Chip labels, table headers, secondary titles |
| bodyLarge | 16 | 24 | 0.5 | 400 | Principal amounts, form field values |
| bodyMedium | 14 | 20 | 0.25 | 400 | Loan amounts, outstanding balance, description text |
| bodySmall | 12 | 16 | 0.4 | 400 | Next repayment date, interest rate, supporting info |
| labelLarge | 14 | 20 | 0.1 | 500 | Button labels, chip text, table column values |
| labelMedium | 12 | 16 | 0.5 | 500 | Status labels, vote tally text |
| labelSmall | 11 | 16 | 0.5 | 500 | Overdue amount label (bold), tiny status indicators |

### Spacing Scale (dp)
- xxs: 2dp | xs: 4dp | sm: 8dp | md: 12dp | lg: 16dp | xl: 24dp | xxl: 32dp | 3xl: 48dp | 4xl: 64dp
- Density: comfortable (generous padding for rural/low-vision users)

### Shape Tokens (corner radius dp)
- none: 0dp | extra_small: 4dp | small: 8dp | medium: 12dp | large: 16dp | extra_large: 28dp | full: 9999dp
- Cards use `shape.medium` (12dp)
- Buttons use `shape.full` (24dp or 9999dp for rounded pill)
- TextFields use `shape.small` (8dp)

### Elevation Tokens
- Level 0: 0dp — flat surfaces, header bands
- Level 1: 1dp, tonal alpha 5% — subtle separation
- Level 2: 3dp, tonal alpha 8% — cards (loan cards, standard)
- Level 3: 6dp, tonal alpha 11% — elevated cards, modals
- Level 4: 8dp, tonal alpha 12% — corpus card (critical info)
- Level 5: 12dp, tonal alpha 14% — dialogs, FAB

### Motion Timing
- short_1: 50ms | short_2: 100ms | short_3: 150ms | short_4: 200ms
- medium_1: 250ms | medium_2: 300ms | medium_3: 350ms | medium_4: 400ms
- long_1: 450ms | long_2: 500ms
- Standard easing: `cubic-bezier(0.2, 0.0, 0, 1.0)` — default for most transitions
- Emphasized easing: `cubic-bezier(0.2, 0.0, 0, 1.0)` — for FAB scale, hero transitions
- Decelerated: `cubic-bezier(0.0, 0.0, 0, 1.0)` — elements entering screen
- Accelerated: `cubic-bezier(0.3, 0.0, 1.0, 1.0)` — elements leaving screen

### Accessibility Specifications
- Minimum touch target: 48dp × 48dp (WCAG 2.5.5)
- Primary CTA minimum: 56dp height
- Focus ring: 3dp outline, follows system focus color
- Color contrast: Primary #2E7D32 on white = 5.83:1 (AAA normal text)
- All status indicators use both color and text label (never color-only)
- Screen reader content descriptions on all interactive and data-driven components
- Noto Sans font supports full Latin Extended, Cyrillic (for French diacritics), Devanagari (Hindi), and Latin Extended-A (Swahili special chars)

---

## 2. Screen Layouts

### Screen: Loan List (`loan-list`)

**Route**: `/groups/{groupId}/loans`
**Entry**: From group-dashboard via "Loans" button, or bottom navigation

**Full Component Tree with Dimensions**:
```
Scaffold
  TopAppBar (height: 56dp)
    background: #2E7D32 (primary)
    title: "Group Loans" — titleLarge, #FFFFFF, 22sp/500
    navigationIcon: arrow_back (24dp icon, 48dp touch target)
    padding_horizontal: 4dp (around icons)

  LazyColumn (fills remaining height)
    padding: 0dp (content cards have own padding)

    # Filter Chips Row
    Row (height: 48dp, padding: 8dp 16dp)
      horizontalScroll: true
      gap: 8dp
      FilterChip "All"    — min_height 32dp, horizontal padding 12dp
      FilterChip "Active" — same dimensions
      FilterChip "Overdue" — same dimensions
      FilterChip "Closed" — same dimensions

    # Loan Cards (repeating)
    LoanCard (each card)
      Card
        background: #FAFAFA (surface)
        elevation: 3dp (level_2)
        cornerRadius: 12dp
        padding: 16dp
        margin: 0dp 16dp 8dp 16dp
        minHeight: 72dp

        Row (horizontal)
          Avatar (40dp × 40dp, corner: full)
            background: secondaryContainer (#FFDDB3)
            initials text: titleSmall, onSecondaryContainer
            marginEnd: 12dp

          Column (weight: 1, fills remaining width)
            Text member_name_text
              value: "Peter Otieno"
              style: titleMedium — 16sp/500, #1A1C19 (onSurface)
              marginBottom: 2dp

            Text loan_amount_text
              value: "KES 15,000"
              style: bodyMedium — 14sp/400, #424942 (onSurfaceVariant)
              marginBottom: 2dp

            Text outstanding_text
              value: "Outstanding: KES 11,250"
              style: bodySmall — 12sp/400, #424942 (onSurfaceVariant)
              marginBottom: 4dp

            Row (wrap: true, gap: 8dp)
              StatusBadge
                ACTIVE: background #C8E6C9, text #1B5E20, text: "Active"
                OVERDUE: background #FFCDD2, text #B71C1C, text: "Overdue"
                CLOSED: background #F5F5F5, text #757575, text: "Closed"
                PENDING: background #FFF9C4, text #E65100, text: "Pending"
                labelSmall — 11sp/500
                cornerRadius: 4dp
                padding: 2dp 8dp

            Text next_repayment_text
              value: "Next: 2026-05-12"
              style: bodySmall — 12sp/400, #424942
              visible_when: status == ACTIVE

          # Right column: overdue indicator
          Column (alignment: end)
            Text overdue_indicator (visible_when: isOverdue)
              value: "OVERDUE — KES 375"
              style: labelSmall — 11sp/500 bold, #D32F2F (error)
              marginTop: 4dp

    # FAB (positioned at bottom end)
    FloatingActionButton
      background: #2E7D32 (primary)
      icon: add (24dp, #FFFFFF)
      label: "Apply for Loan"
      size: extended (height 56dp)
      elevation: 12dp (level_5)
      margin: 16dp
      visible_when: canApplyLoan == true
      contentPadding: 16dp 20dp

    # Loading State (replaces cards)
    repeat 5 times:
      ShimmerCard
        height: 96dp
        cornerRadius: 12dp
        background: #DEE5DA (surfaceVariant)
        margin: 0dp 16dp 8dp
        animated: shimmer left-to-right, duration 1200ms, loop

    # Empty State (replaces cards)
    EmptyStateColumn (padding: 48dp, alignment: center)
      Icon account_balance_wallet — 56dp, #424942 (onSurfaceVariant)
      Text "No loans yet" — titleMedium, #1A1C19, marginTop: 16dp
      Text "No loans match the selected filter." — bodyMedium, #424942, marginTop: 8dp

    # Error State (replaces cards)
    ErrorStateColumn (padding: 48dp)
      Icon cloud_off — 56dp, #424942
      Text "Could not load loans" — titleMedium, #1A1C19
      Text "{{error.message}}" — bodyMedium, #424942
      Button "Retry" — outlinedButton, primary border, min_height 48dp, marginTop: 16dp
```

### Screen: Loan Apply (`loan-apply`)

**Route**: `/groups/{groupId}/loans/apply`
**Entry**: From loan-list FAB

```
Scaffold
  TopAppBar (56dp)
    background: #2E7D32
    title: "Apply for Loan" — titleLarge, #FFFFFF
    navigationIcon: arrow_back

  LazyColumn (padding: 16dp)
    gap between items: 12dp

    # Member Selector
    ExposedDropdownMenuBox
      OutlinedTextField (minHeight: 56dp)
        label: "Select Member"
        placeholder: "Choose group member"
        leadingIcon: person (24dp, #424942)
        trailingIcon: arrow_drop_down
        cornerRadius: 8dp
        borderColor: #727971 (outline)
        focusBorderColor: #2E7D32 (primary)

    # Eligibility Banner (visible_when: selectedMember != null)
    Card (background: #A6F1A6, cornerRadius: 8dp, padding: 12dp)
      Text "Savings balance: KES 5,000"
        style: bodyMedium — 14sp, #002106 (onPrimaryContainer)
      Text "Max eligible: KES 15,000 (3× savings)"
        style: titleSmall — 14sp/500, #2E7D32 (primary)
        marginTop: 4dp

    # Amount Input
    OutlinedTextField (minHeight: 56dp)
      label: "Requested Amount (KES)"
      placeholder: "e.g. 1500"
      inputType: number
      keyboardType: decimal
      leadingIcon: currency_exchange (24dp)
      cornerRadius: 8dp
      errorText: "Amount exceeds eligible limit of KES 15,000" (visible when amountError != null)
      errorColor: #D32F2F

    # Corpus Warning Banner (visible_when: corpusWarning)
    Card (background: #FFF9C4, cornerRadius: 8dp, padding: 12dp)
      Row (alignment: centerVertical)
        Icon warning — 20dp, #E65100
        marginEnd: 8dp
      Text "Warning: Disbursing this amount will reduce the group corpus below 10% buffer. Current balance: KES 24,000."
        style: bodySmall — 12sp, #E65100
        marginStart: 4dp

    # Duration Dropdown
    ExposedDropdownMenuBox
      OutlinedTextField (minHeight: 56dp)
        label: "Loan Duration"
        options: 4 weeks / 8 weeks / 12 weeks / 24 weeks / 52 weeks (1 year)
        cornerRadius: 8dp

    # Purpose Dropdown
    ExposedDropdownMenuBox
      OutlinedTextField (minHeight: 56dp)
        label: "Loan Purpose"
        options: Medical / Education / Business / Emergency / Other
        cornerRadius: 8dp

    # Product Dropdown
    ExposedDropdownMenuBox
      OutlinedTextField (minHeight: 56dp)
        label: "Loan Product"
        placeholder: "Select product"
        options: [from /loanproducts API]
        cornerRadius: 8dp

    # Submit Button
    FilledButton (minHeight: 56dp, width: fillMaxWidth)
      background: #2E7D32
      text: "Submit Application" — labelLarge, #FFFFFF
      cornerRadius: 24dp
      enabled_when: selectedMember != null && requestedAmount.isNotBlank() && amountError == null && selectedProduct != null
      loading: CircularProgressIndicator (24dp, #FFFFFF) when isSubmitting
      marginTop: 8dp
```

### Screen: Loan Detail (`loan-detail`)

**Route**: `/loans/{loanId}`

```
Scaffold
  TopAppBar (56dp)
    background: #2E7D32
    title: "Loan Detail"
    navigationIcon: arrow_back
    actions: refresh IconButton (24dp icon, 48dp touch)

  LazyColumn (padding: 0dp, gap: 0dp)

    # Member Header Card
    Card (background: #A6F1A6, cornerRadius: 12dp, padding: 16dp, elevation: 0dp, margin: 16dp 16dp 0dp)
      Row (alignment: spaceBetween)
        Column
          Text "Peter Otieno" — headlineSmall, 24sp/400, #002106
          Text "Standard Group Loan" — bodyMedium, 14sp, #002106
          Text "Principal: KES 15,000" — bodyLarge, 16sp, #002106, marginTop: 4dp
          Text "Disbursed: 2026-04-14" — bodySmall, 12sp, #002106
          Text "Interest: 5% per week" — bodySmall, 12sp, #002106
        StatusBadge "Active" — #C8E6C9 bg / #1B5E20 text, alignment: topEnd

    # Outstanding Summary Row
    Row (padding: 8dp 16dp, gap: 8dp)
      InfoChip "Outstanding: KES 11,250"
        background: #FFDDB3 (secondaryContainer)
        text: labelMedium, #2A1700 (onSecondaryContainer)
        cornerRadius: 8dp
        padding: 6dp 12dp
      InfoChip "Overdue: KES 375" (visible_when: totalOverdue > 0)
        background: #FFDAD6 (errorContainer)
        text: labelMedium, #410002 (onErrorContainer)

    # Tab Bar
    TabRow (height: 48dp)
      indicator: 2dp line, #2E7D32
      Tab "Schedule" — titleSmall, primary when selected, onSurfaceVariant when unselected
      Tab "Repayment History" — same styling

    # Schedule Table (visible_when: selectedTab == SCHEDULE)
    Table (horizontalScroll: true when compact)
      Header row (height: 40dp, background: surfaceVariant)
        | Wk (40dp) | Due Date (96dp) | Due (88dp) | Paid (88dp) | Balance (88dp) | Status (72dp) |
        all headers: labelSmall, #424942, center aligned
      Data rows (height: 48dp each)
        PAID row: background #F1F8E9, text #33691E
        PARTIAL row: background #FFF9C4, text #E65100
        OVERDUE row: background #FFCDD2, text #B71C1C
        UPCOMING row: background #FAFAFA, text #1A1C19
        Week 1: 1 | 2026-04-21 | 2,000 | 2,000 | 0 | Paid
        Week 2: 2 | 2026-04-28 | 1,937 | 1,937 | 0 | Paid
        Week 3: 3 | 2026-05-05 | 1,875 | 1,875 | 0 | Paid
        Week 4: 4 | 2026-05-12 | 1,812 | 0 | 1,812 | Upcoming

    # History List (visible_when: selectedTab == HISTORY)
    LazyColumn
      each RepaymentTransaction row:
        ListItem (height: 56dp)
          headline: txn.type — bodyMedium, #1A1C19
          supporting: txn.date — bodySmall, #424942
          trailing: "KES 2,000" — bodyMedium, #2E7D32 (primary)
      empty: "No repayments recorded yet." — bodyMedium center, onSurfaceVariant

    # Action Buttons Row
    Row (padding: 16dp, gap: 12dp)
      FilledButton "Record Repayment" (weight: 1, minHeight: 48dp)
        background: #2E7D32, text: onPrimary
        visible_when: canRecordRepayment && loan.status == ACTIVE
        cornerRadius: 24dp
      FilledButton "Mark Defaulted" (weight: 1, minHeight: 48dp)
        background: #D32F2F (error), text: #FFFFFF
        visible_when: canMarkDefaulted && loan.status == OVERDUE
        cornerRadius: 24dp
```

---

## 3. Component Specifications

### LoanCard Component
**Purpose**: Displays a single loan summary in the loan-list screen.

**Props**:
- `loan: LoanSummary` — full loan data object
- `onClick: (loanId: Long) -> Unit` — tap handler

**Visual States**:

| State | Background | Border | Elevation |
|-------|-----------|--------|-----------|
| Default | #FAFAFA (surface) | none | 3dp |
| Pressed | #DEE5DA (surfaceVariant) — ripple | none | 1dp (reduces during press) |
| Focused | #FAFAFA + 3dp focus ring #2E7D32 | 3dp outline | 3dp |

**Overdue Variant**:
- StatusBadge color scheme changes to errorContainer/onErrorContainer
- Red overdue indicator text appended below standard info
- Avatar background stays secondaryContainer (overdueRate is on loan, not member)

**Animations**:
- Tap: `ripple` effect from touch point, 200ms, standard easing
- Load: `fadeIn(duration=150ms, easing=decelerated)` staggered 30ms per card

### FilterChip Component
**Props**:
- `label: String` — chip text
- `selected: Boolean` — current state
- `onSelected: () -> Unit` — tap handler
- `selectedColor: ColorToken` — background when selected

**Visual States**:

| State | Background | Text Color | Border |
|-------|-----------|-----------|--------|
| Default | surfaceVariant (#DEE5DA) | onSurfaceVariant (#424942) | outline 1dp |
| Selected (All/Active) | primaryContainer (#A6F1A6) | onPrimaryContainer (#002106) | none |
| Selected (Overdue) | errorContainer (#FFDAD6) | onErrorContainer (#410002) | none |
| Selected (Closed) | surfaceVariant (#DEE5DA) | onSurfaceVariant (#424942) | outline 1dp |
| Pressed | Scale 0.96, ripple overlay | — | — |

**Dimensions**: height 32dp, horizontal padding 12dp, corner radius full (9999dp), labelSmall text

**Animation**: toggle 150ms, standard easing, background color animates via `animateColorAsState`

### EligibilityBanner Component
**Purpose**: Shows computed max loan amount once member selected in loan-apply.

**Props**:
- `savingsBalance: Double` — member's current savings
- `loanMultiplier: Double` — from group config (e.g. 3.0)
- `eligibleAmount: Double` — computed: savingsBalance × loanMultiplier
- `visible: Boolean` — shows only when selectedMember != null

**Layout**: Card, primaryContainer background (#A6F1A6), cornerRadius 8dp, padding 12dp
- Row 1: "Savings balance: KES 5,000" — bodyMedium, onPrimaryContainer
- Row 2: "Max eligible: KES 15,000 (3× savings)" — titleSmall/500, primary green

**Animation**: `AnimatedVisibility(enter=fadeIn+expandVertically, exit=fadeOut+shrinkVertically, duration=250ms)`

### CorpusWarningBanner Component
**Purpose**: Warns treasurer when requested amount would deplete corpus below 10% safety buffer.

**Props**:
- `visible: Boolean` — shown when `corpusBalance - requestedAmount < corpusBalance * 0.10`
- `corpusBalance: Double` — current corpus balance

**Layout**: Card, background #FFF9C4, cornerRadius 8dp, padding 12dp
- Icon: warning, 20dp, #E65100
- Text: "Warning: Disbursing this amount will reduce the group corpus below 10% buffer. Current balance: KES 24,000." — bodySmall, #E65100

**Animation**: Same as EligibilityBanner — fade+expand/collapse 250ms

### StatusBadge Component
**Props**:
- `status: LoanStatus` — ACTIVE, OVERDUE, CLOSED, PENDING, REJECTED

**Style map**:

| Status | Background | Text Color | Text |
|--------|-----------|-----------|------|
| ACTIVE | #C8E6C9 | #1B5E20 | "Active" |
| OVERDUE | #FFCDD2 | #B71C1C | "Overdue" |
| CLOSED | #F5F5F5 | #757575 | "Closed" |
| PENDING | #FFF9C4 | #E65100 | "Pending" |
| REJECTED | #FFDAD6 | #410002 | "Rejected" |

**Dimensions**: cornerRadius 4dp, padding 2dp 8dp, text labelSmall

### RepaymentScheduleTable Component
**Props**:
- `rows: List<RepaymentScheduleRow>` — schedule data

**Column widths** (dp): Wk=40, Due Date=96, Due=88, Paid=88, Balance=88, Status=72

**Row color rules**:
- PAID: background #F1F8E9, text #33691E (dark green)
- PARTIAL: background #FFF9C4, text #E65100 (orange)
- OVERDUE: background #FFCDD2, text #B71C1C (red)
- UPCOMING: background #FAFAFA, text #1A1C19 (default surface)

**Header row**: background surfaceVariant (#DEE5DA), labelSmall text, onSurfaceVariant

### ActionButtonsRow Component
**Purpose**: Record Repayment and/or Mark Defaulted at bottom of loan-detail screen.

**Visibility rules**:
- "Record Repayment": visible when `canRecordRepayment == true && loan.status == ACTIVE`
- "Mark Defaulted": visible when `canMarkDefaulted == true && loan.status == OVERDUE`

**Styles**:
- Record Repayment: FilledButton, background #2E7D32, text #FFFFFF, cornerRadius 24dp, weight 1
- Mark Defaulted: FilledButton, background #D32F2F, text #FFFFFF, cornerRadius 24dp, weight 1

### MemberSelector Dropdown (loan-apply)
**Props**:
- `members: List<GroupMember>` — loaded from API
- `selectedMember: GroupMember?` — current selection
- `onMemberSelected: (GroupMember) -> Unit`

**Loading state**: Shows "Loading members..." with CircularProgressIndicator (16dp) inside field
**Empty state**: Dropdown shows "No members found" if API returns empty

### Submit Button States
| State | Background | Text | Icon |
|-------|-----------|------|------|
| Disabled | #DEE5DA (surfaceVariant) | #424942 (onSurfaceVariant) | none |
| Enabled | #2E7D32 (primary) | #FFFFFF (onPrimary) | none |
| Loading | #2E7D32 | hidden | CircularProgressIndicator 24dp white |
| Success | brief #A6F1A6 flash, then navigate | — | — |

---

## 4. Interaction Patterns

### Filter Chip Selection Flow (loan-list)
1. **Trigger**: User taps a filter chip (e.g. "Overdue")
2. **Animation start**: Chip scales to 0.94 (press feedback, 100ms, accelerated easing)
3. **State update**: `selectedFilter` → OVERDUE, `filteredLoans` = client-side filter result (no API call)
4. **Animation end**: Chip background animates from surfaceVariant → errorContainer (150ms, standard easing via `animateColorAsState`)
5. **List update**: LazyColumn items update with `AnimatedVisibility` — items leaving: `fadeOut+shrinkVertically(150ms)`, items entering: `fadeIn+expandVertically(150ms)` staggered 20ms per item
6. **Result display**: If 0 results, empty state fades in (200ms)

### Loan Card Tap Flow (loan-list → loan-detail)
1. **Trigger**: User taps any area of LoanCard
2. **Ripple**: Ripple effect from touch point expands to card bounds, color: primary 12% alpha, duration 200ms
3. **Navigation**: `LoanListEvent.NavigateToLoanDetail(loanId)` emitted
4. **Transition**: Shared element container transform — card expands to fill screen over 400ms (emphasized easing)
5. **Detail screen**: Member header card enters from top (slide in 300ms, decelerated easing)

### FAB Tap Flow (loan-list → loan-apply)
1. **Trigger**: User taps "Apply for Loan" FAB
2. **Press**: FAB scale 1.0 → 0.85 (100ms, accelerated)
3. **Release**: FAB scale 0.85 → 1.0 (300ms, emphasized decelerated)
4. **Navigation**: `LoanListEvent.NavigateToLoanApply(groupId)` emitted
5. **Transition**: FAB expands into full screen (container transform, 400ms, emphasized)

### Eligibility Computation (loan-apply)
1. **Trigger**: User selects a member from dropdown
2. **API calls** (parallel): `GET /clients/{clientId}/accounts` + `GET /datatables/dt_group_config/{groupId}`
3. **Loading state**: TextField shows shimmer loading indicator (1000ms)
4. **Computation**: `eligibleAmount = memberSavingsBalance × loanMultiplier` (client-side, instant)
5. **Banner reveal**: EligibilityBanner `AnimatedVisibility(enter=fadeIn+expandVertically, 250ms)`
6. **Amount field unlock**: Amount field becomes editable/focused automatically

### Amount Validation Flow
1. **Trigger**: User types in amount field (each keystroke)
2. **Validation** (debounced 200ms): `requestedAmount.toDoubleOrNull() > eligibleAmount`
3. **Error state**: `amountError` set → field shows red border + error text "Amount exceeds eligible limit of KES 15,000"
4. **Corpus check**: `corpusBalance - requestedAmount < corpusBalance * 0.10` → warning banner shown
5. **Submit button**: re-evaluates enabled state after each change

### Loan Application Submission Flow
1. **Trigger**: User taps "Submit Application"
2. **Optimistic**: Button shows loading spinner immediately, form inputs disabled
3. **API call**: POST /loans — up to 10s timeout
4. **Success**: Brief success toast "Loan application submitted", navigate to meeting-conduct for voting
5. **Error**: Error state shows with "Try Again" CTA, form re-enables

### Repayment Schedule Tab Switch
1. **Trigger**: User taps "Repayment History" tab
2. **Indicator**: Tab indicator slides from "Schedule" to "Repayment History" (300ms, standard easing)
3. **Content**: Cross-fade between schedule table and history list (200ms)
4. **No loading**: Both datasets loaded on screen entry, just toggling visibility

### Record Repayment Dialog Flow
1. **Trigger**: Treasurer taps "Record Repayment"
2. **Dialog** slides up from bottom (300ms, decelerated): Amount field, Date picker, Confirm
3. **Submit**: POST /loans/{loanId}/transactions?command=repayment
4. **Success**: Dialog dismisses, schedule table refreshes with new PAID row, outstanding amount updates
5. **Error**: Error text inside dialog, form stays open

### Pull-to-Refresh Flow
1. **Trigger**: User drags list down beyond threshold (56dp)
2. **Indicator**: Material refresh spinner appears below TopAppBar
3. **API call**: `GET /groups/{groupId}/loans` with cache invalidation
4. **Complete**: Spinner dismisses (200ms fade out), new data replaces old with `crossfade(300ms)`

---

## 5. Content Data

### Demo Group
- **Group**: Mwangaza Women's Group
- **Group ID**: 7 (Fineract centerId)
- **Cycle**: 1 of 12 months
- **Meeting schedule**: Weekly (Monday 9:00 AM)
- **Corpus balance**: KES 24,000
- **Loan multiplier**: 3.0×

### Group Members
| Member ID | Name | Role | Savings Balance | Eligible Amount |
|-----------|------|------|-----------------|-----------------|
| m1 (clientId: 101) | Amara Diallo | Chairperson | KES 6,800 | KES 20,400 |
| m2 (clientId: 102) | Grace Mwangi | Treasurer | KES 5,200 | KES 15,600 |
| m3 (clientId: 103) | Fatima Ouedraogo | Secretary | KES 4,800 | KES 14,400 |
| m4 (clientId: 104) | Peter Otieno | Member | KES 5,000 | KES 15,000 |
| m5 (clientId: 105) | Mary Akinyi | Member | KES 2,800 | KES 8,400 |

### Active Loans
**Loan 1 — Peter Otieno**:
- Loan ID: 1001, Fineract Loan ID: 1001
- Principal: KES 15,000
- Interest rate: 5% per week (declining balance)
- Duration: 12 weeks
- Disbursed: 2026-04-14
- Status: ACTIVE
- Outstanding: KES 11,250 (3 payments of KES 1,250 principal made)
- Next repayment: 2026-05-12 (week 4)
- isOverdue: false
- Repayment schedule:
  - Week 1 (2026-04-21): Due KES 2,000 | Paid KES 2,000 | Status: PAID
  - Week 2 (2026-04-28): Due KES 1,937.50 | Paid KES 1,937.50 | Status: PAID
  - Week 3 (2026-05-05): Due KES 1,875 | Paid KES 1,875 | Status: PAID
  - Week 4 (2026-05-12): Due KES 1,812.50 | Paid KES 0 | Status: UPCOMING
  - Weeks 5–12: UPCOMING

**Loan 2 — Grace Mwangi**:
- Loan ID: 1002, Fineract Loan ID: 1002
- Principal: KES 3,000
- Interest rate: 5% per week
- Duration: 8 weeks
- Disbursed: 2026-04-07
- Status: OVERDUE
- Outstanding: KES 2,625
- Overdue amount: KES 375
- isOverdue: true

### Loan Products Available
| Product ID | Name | Min Principal | Max Principal | Interest Rate |
|-----------|------|--------------|--------------|---------------|
| 1 | Standard Group Loan | KES 500 | KES 50,000 | 5% per week |
| 2 | Emergency Loan | KES 200 | KES 10,000 | 3% per week |
| 3 | Business Growth Loan | KES 2,000 | KES 100,000 | 6% per week |

### Meeting Data (Meeting #7)
- Meeting ID: "mtg-007"
- Meeting number: 7
- Center ID: 7
- Date: 2026-05-07
- Opening corpus: KES 24,000
- Pending loan applications:
  - Amara Diallo: requests KES 12,000 for Business (savings KES 6,800, eligible KES 20,400)
  - Mary Akinyi: requests KES 5,000 for Medical (savings KES 2,800, eligible KES 8,400)

### Corpus Check Demo
- corpusBalance: KES 24,000
- If Peter applies for KES 15,000: `24,000 - 15,000 = 9,000` (37.5% buffer — no warning)
- If Amara applies for KES 22,000: `24,000 - 22,000 = 2,000` (8.3% buffer — WARNING triggered)
- Corpus warning threshold: `corpusBalance * 0.10 = 2,400`

---

## 6. Responsive Rules

### Compact Layout (0–599dp width — phones, typical target device)
- **loan-list**: Single-column layout. Filter chips in horizontal scrolling row. Loan cards full width with 16dp horizontal margins.
- **loan-apply**: Single-column form, all fields full width, dropdowns fill width.
- **loan-detail**: Tabs take full width. Table uses horizontal scroll (min 520dp needed for 6 columns). Action buttons are 2-column row (weight:1 each).
- **meeting-conduct step 4**: Member rows full width. Repayment and fine inputs stack vertically below member info.
- **meeting-conduct step 5**: Application cards full width. Vote buttons in a row (2 columns). Approve button full width below vote row.

### Medium Layout (600–839dp width — foldables, small tablets)
- **loan-list**: Filter chips may show without scroll. Cards maintain 16dp margins but content area wider.
- **loan-apply**: Form still single column but fields wider. Eligibility banner is more prominent.
- **loan-detail**: Table can show all 6 columns without scroll. Action buttons appear as row naturally.
- **meeting-conduct**: Attendance/savings/loan rows have more horizontal space; input fields align to right side.

### Expanded Layout (840dp+ — tablets, desktop)
- **loan-list**: Two-column card grid. Left: loan cards (narrower). Right: could show selected loan detail panel (future split-panel).
- **loan-apply**: Two-column form layout. Left column: member selector + eligibility + amount + corpus warning. Right column: duration + purpose + product + submit.
- **loan-detail**: Three-column table visible without scroll. Schedule and history tabs side by side (future two-pane).
- **meeting-conduct**: Wizard steps shown in side-by-side layout when step content is narrow enough. Stepper vertical on left, content on right.

### Bottom Navigation Visibility
- **loan-list**: bottom_nav visible=true, selected_tab=loans
- **loan-apply**: bottom_nav visible=false (focused form flow)
- **loan-detail**: bottom_nav visible=false (focused detail view)
- **meeting-conduct**: bottom_nav visible=false (full-screen wizard)

### Typography Scaling for Low-Vision Users
- Base: `scale_style: large` — all sp values are already scaled up from MD3 defaults
- OS text size multiplier: app supports 1.0× to 1.3× without layout breaking
- At 1.3× multiplier: label texts still fit in filter chips (tested at 14dp virtual screen)
- Tables: switch to horizontal scroll below 360dp width when text size > 1.1×

### RTL Support Note
- Swahili, French, English: LTR — no layout change needed
- Hindi (Devanagari): LTR — no layout change needed
- Noto Sans handles all required Unicode ranges
- All padding/margin/start/end use logical layout directions (marginStart, paddingEnd) not Left/Right

### FAB Positioning
- **Compact**: FAB fixed at `Alignment.BottomEnd`, margin 16dp from window edges
- **Medium/Expanded**: FAB shifts to `Alignment.BottomEnd` of content area; no overlap with two-pane layout
- FAB hidden when scrolling down fast (>300dp/s), reappears when scrolling up or stops

### Card Elevation Responsive Behavior
- Cards maintain elevation at all breakpoints
- On medium+: add subtle drop shadow (elevation 4dp) to distinguish from wider backgrounds
- On compact: elevation 2dp standard (closer to content edges, less depth needed)

---

## Component State Matrix

Full state definitions for every interactive component in the loan-management feature. Colors reference the MifosSave MD3 token system (primary #2E7D32).

### LoanListCard (loan-list screen)

| Component | State | Background | Text/Icon Color | Border | Shadow (elevation) | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| LoanListCard | default | surface #FAFAFA | onSurface #1A1C19 | none | 2dp | true | true |
| LoanListCard | pressed | surfaceVariant #DEE5DA | onSurface #1A1C19 | none | 8dp (lifted) | true | true |
| LoanListCard | focused (d-pad) | surface #FAFAFA | onSurface #1A1C19 | 2dp outline #2E7D32 | 2dp | true | true |
| LoanListCard | disabled | surface #FAFAFA (50% opacity) | onSurface at 38% | none | 0dp | false | true |
| LoanListCard | loading skeleton | surfaceVariant shimmer | n/a | none | 0dp | false | true |
| LoanListCard — active badge | default | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | none | 0dp | true | true |
| LoanListCard — overdue badge | default | errorContainer #FFDAD6 | onErrorContainer #410002 | none | 0dp | true | true |
| LoanListCard — closed badge | default | surfaceVariant #DEE5DA | onSurfaceVariant #424942 | none | 0dp | true | true |
| LoanListCard — pending badge | default | secondaryContainer #FFDDB3 | onSecondaryContainer #2A1700 | none | 0dp | true | true |

### FilterChip (loan-list screen — All / Active / Overdue / Closed)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| FilterChip | unselected default | surface #FAFAFA | onSurfaceVariant #424942 | 1dp outline #727971 | 0dp | true | true |
| FilterChip | unselected hovered | surfaceVariant #DEE5DA | onSurfaceVariant #424942 | 1dp outline #727971 | 0dp | true | true |
| FilterChip | selected (active) | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | none | 0dp | true | true |
| FilterChip | selected (overdue) | errorContainer #FFDAD6 | onErrorContainer #410002 | none | 0dp | true | true |
| FilterChip | pressed | surfaceVariant #DEE5DA | onSurface #1A1C19 | 1dp #2E7D32 | 0dp | true | true |
| FilterChip | focused | surface #FAFAFA | onSurface #1A1C19 | 2dp #2E7D32 | 0dp | true | true |
| FilterChip | disabled | surface at 38% opacity | onSurface at 38% | 1dp outline at 38% | 0dp | false | true |

### PrimaryButton — "Apply for Loan" FAB / form submit

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| FAB (Apply) | default | primary #2E7D32 | onPrimary #FFFFFF | none | 6dp | true | true |
| FAB (Apply) | pressed | primary #1B5E20 (darker) | onPrimary #FFFFFF | none | 12dp | true | true |
| FAB (Apply) | focused | primary #2E7D32 | onPrimary #FFFFFF | 2dp onPrimary ring | 6dp | true | true |
| FAB (Apply) | loading | primary #2E7D32 | CircularProgressIndicator white | none | 6dp | false | true |
| FAB (Apply) | disabled | surface #FAFAFA | onSurface at 38% | none | 0dp | false | true |
| FAB (Apply) | hidden (scroll down) | — | — | — | — | false | false |

### LoanApplyForm — text fields (loan-apply screen)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| TextField | default | surfaceVariant #DEE5DA | onSurface #1A1C19 | 1dp outlineVariant #C2C9BD | 0dp | true | true |
| TextField | focused | surfaceVariant #DEE5DA | onSurface #1A1C19 | 2dp primary #2E7D32 | 0dp | true | true |
| TextField | filled (has value) | surfaceVariant #DEE5DA | onSurface #1A1C19 | 1dp outlineVariant | 0dp | true | true |
| TextField | error | errorContainer #FFDAD6 | onErrorContainer #410002 | 2dp error #D32F2F | 0dp | true | true |
| TextField | disabled | surface at 38% opacity | onSurface at 38% | 1dp at 38% opacity | 0dp | false | true |
| TextField | read-only | surfaceVariant #DEE5DA at 60% | onSurfaceVariant #424942 | 1dp outlineVariant | 0dp | false | true |

### RepaymentStatusRow (loan-detail screen)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| RepaymentRow | paid | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | none | 0dp | false | true |
| RepaymentRow | due today | warningContainer #FFF9C4 | onWarningContainer #E65100 | none | 0dp | true | true |
| RepaymentRow | overdue | errorContainer #FFDAD6 | onErrorContainer #410002 | 1dp error #D32F2F | 0dp | true | true |
| RepaymentRow | upcoming | surface #FAFAFA | onSurfaceVariant #424942 | none | 0dp | false | true |
| RepaymentRow | waived | surfaceVariant #DEE5DA | onSurfaceVariant at 60% | none | 0dp | false | true |

---

## API Failure & Recovery Playbook

Each API call in the loan-management feature has a defined failure handling contract. All retries use exponential back-off. SyncQueue entries persist across app restarts in local Room DB.

### GET /loans (loan-list load)

| Failure Type | Detection | User-Facing Response | Recovery |
|---|---|---|---|
| Network timeout | IOException after 10s | Snackbar: "Connection timed out — showing cached loans" | Auto-retry: 1s, 2s, 4s back-off; show cached data from Room DB |
| 401 Unauthorized | HTTP 401 | Navigate to LoginScreen, preserve pending SyncQueue entries | Session re-auth; restore last scroll position on return |
| 404 Not Found | HTTP 404 | Snackbar: "Loan data not found — contact your field officer" | Offer manual refresh button |
| 500 Server Error | HTTP 5xx | Snackbar: "Server error — try again" with Retry action | Manual retry; log to Crashlytics |
| Offline (no network) | NetworkCapabilities=false | Show "Offline" banner (warningContainer); list from cached Room snapshot | Auto-refresh when connectivity restored; show last-sync timestamp |

Retry schedule: attempt 1 immediate → attempt 2 after 1s → attempt 3 after 2s → attempt 4 after 4s → fail with user notification.

### POST /loans (loan application submit)

| Failure Type | Detection | User-Facing Response | Recovery |
|---|---|---|---|
| Network timeout | IOException | "Application not submitted — queued for retry" | Add to SyncQueue with PENDING status; show pending badge on loan card |
| 401 Unauthorized | HTTP 401 | Navigate to login, re-hydrate form data from SavedStateHandle | Re-submit after auth |
| 422 Validation Error | HTTP 422 + body.errors[] | Inline field errors: highlight field, show error text below | User corrects inputs; no retry needed |
| 404 Group Not Found | HTTP 404 | "Group account not found — re-sync your group data" | Trigger group re-sync; re-enable submit after sync |
| 500 Server Error | HTTP 5xx | "Application failed to submit" Snackbar with Retry | Allow user-triggered retry up to 3×; offer save-as-draft fallback |
| Offline | No network at submit time | Queue to SyncQueue; disable submit button after first queue; show "Will submit when online" | Auto-submit when reconnected; badge count on nav item |

### GET /loans/{loanId} (loan detail load)

| Failure Type | Detection | User-Facing Response | Recovery |
|---|---|---|---|
| Network timeout | IOException after 10s | "Loading from cache — may not be current" | Show cached detail from Room; offer manual refresh |
| 401 Unauthorized | HTTP 401 | Navigate to login | Return to same detail on successful re-auth |
| 404 Not Found | HTTP 404 | "This loan record no longer exists" + Back button | Navigate back to loan-list; remove from local cache |
| 500 Server Error | HTTP 5xx | Error Snackbar with Retry | Retry up to 3× auto; then manual |
| Offline | No network | Show cached loan with "Offline — showing last saved data" chip | Reconnect auto-refresh |

### POST /loans/{loanId}/repayments (make repayment)

| Failure Type | Detection | User-Facing Response | Recovery |
|---|---|---|---|
| Network timeout | IOException | Queue to SyncQueue; show "Payment pending" badge | Auto-submit on reconnect |
| 401 Unauthorized | HTTP 401 | Preserve repayment amount in SavedStateHandle; re-auth flow | Auto-resubmit after re-auth |
| 409 Conflict | HTTP 409 (duplicate repayment) | "Payment already recorded for this period" Snackbar | Refresh repayment schedule; no duplicate entry |
| 500 Server Error | HTTP 5xx | "Payment failed — try again" with Retry | Manual retry; SyncQueue fallback after 3 failures |
| Offline | No network | Queue to SyncQueue; show pending badge; disable "Pay Now" button | Auto-retry on reconnect |

### SyncQueue — Pending Badge Rules
- Pending badge on BottomNav loans tab: shown when SyncQueue has ≥1 loan-related entry
- Badge count: exact number of pending items (max "9+")
- Badge color: secondaryContainer #FFDDB3 / onSecondaryContainer #2A1700
- Auto-dismiss when SyncQueue drains to 0 (all entries processed)

---

## Screen Reader & Accessibility Deep Dive

### loan-list Screen — Focus Order (TalkBack / D-pad traversal)

1. TopAppBar — "Mwangaza Women's Group, Loans" (role: heading)
2. TopAppBar trailing icon — "Sync data" (button)
3. FilterChip "All" (selected)
4. FilterChip "Active"
5. FilterChip "Overdue"
6. FilterChip "Closed"
7. First LoanListCard — e.g. "Amara Diallo, Active loan, KES 5,000 outstanding, due 15 Jun 2026" (role: button, activates loan-detail)
8. Second LoanListCard — "Grace Mwangi, Overdue loan, KES 3,200 outstanding, overdue by 12 days"
9. Third LoanListCard — "Peter Otieno, Active loan, KES 8,000 outstanding, due 22 Jun 2026"
10. Fourth LoanListCard — "Mary Akinyi, Pending approval, KES 10,000 applied"
11. Fifth LoanListCard — "Fatima Ouedraogo, Closed loan, fully repaid"
12. FAB — "Apply for new loan" (role: button)

### TalkBack Announcement Strings

| Element | Announcement |
|---|---|
| LoanListCard (active) | "{memberName}, active loan, KES {outstanding} outstanding, next due {date}" |
| LoanListCard (overdue) | "{memberName}, overdue loan, KES {outstanding} outstanding, overdue by {days} days, double-tap to view details" |
| LoanListCard (pending) | "{memberName}, loan application pending approval, KES {amount} applied" |
| LoanListCard (closed) | "{memberName}, loan fully repaid and closed" |
| FilterChip (unselected) | "Show {filter} loans, not selected" |
| FilterChip (selected) | "Showing {filter} loans, selected" |
| FAB | "Apply for new group loan, button" |
| Sync icon | "Sync loan data with server, button" |
| Loading state | "Loading loans, please wait" (live region: polite) |
| Empty state | "No {filter} loans found for Mwangaza Women's Group" |

### loan-apply Screen — Focus Order

1. TopAppBar back arrow — "Go back to loan list" (button)
2. TopAppBar title — "New Loan Application, Mwangaza Women's Group" (heading)
3. Member selector dropdown — "Select member, required" (combobox)
4. Loan product dropdown — "Select loan product, required" (combobox)
5. Principal amount field — "Principal amount in Kenyan Shillings, required, enter a number" (text input)
6. Repayment period field — "Repayment period in months, required" (text input)
7. Guarantor 1 selector — "Select first guarantor member" (combobox)
8. Guarantor 2 selector — "Select second guarantor member, optional" (combobox)
9. Eligibility indicator chip — "Eligible: savings balance KES 2,400, sufficient for this loan" or error equivalent
10. Loan summary card — "Loan summary: principal KES 10,000, interest 10%, total repayable KES 11,000 over 6 months"
11. Submit button — "Submit loan application" (button)

### loan-detail Screen — Focus Order

1. TopAppBar back arrow — "Go back to loans list" (button)
2. TopAppBar title — "Loan Details, {memberName}" (heading)
3. TopAppBar overflow menu — "More actions" (button)
4. Loan status chip — "Status: Active" or "Overdue" (status)
5. Principal display — "Principal: KES 10,000"
6. Outstanding balance — "Outstanding balance: KES 7,200"
7. Interest rate — "Interest rate: 10 percent per cycle"
8. Disbursed date — "Disbursed on 1 January 2026"
9. Due date — "Final due date: 30 June 2026"
10. "Make Repayment" button (button, primary action)
11. Repayment schedule header — "Repayment schedule, heading"
12. Schedule rows (each): "{month} installment: KES {amount}, status: {paid/due/overdue}"
13. "Mark as Defaulted" button — "Mark loan as defaulted, destructive action, button"

### Content Descriptions — Icons

| Icon | Content Description |
|---|---|
| check_circle (paid repayment) | "Installment paid" |
| error (overdue) | "Overdue — immediate action required" |
| schedule (upcoming) | "Upcoming installment" |
| remove_circle (waived) | "Interest waived by field officer" |
| sync (TopAppBar) | "Sync with server" |
| arrow_back | "Go back" |
| add (FAB) | "Apply for new loan" |
| more_vert | "More actions" |

### Live Region Announcements

- When loan list finishes loading: "Loaded {count} loans for Mwangaza Women's Group" (assertive)
- When sync completes: "Loan data updated" (polite)
- When filter chip selected: "Showing {count} {filter} loans" (polite)
- When form field has validation error: "{fieldName} error: {errorMessage}" (assertive)
- When repayment submitted successfully: "Repayment of KES {amount} recorded for {memberName}" (assertive)

### Keyboard Navigation

- `Tab` / `Shift+Tab`: move focus forward / backward through interactive elements
- `Enter` / `Space`: activate focused button, chip, or card
- `Arrow keys`: navigate within FilterChip row (left/right), dropdown options (up/down)
- `Escape`: dismiss bottom sheet, dropdown, or dialog; navigate back from detail screen
- `Backspace` (text field focused): clear one character
- All status states (Active / Overdue / Closed / Pending) use both color AND icon — never color alone

### WCAG AA Contrast Ratios

| Text / Background | Contrast Ratio | Pass Level |
|---|---|---|
| onSurface #1A1C19 / surface #FAFAFA | 17.8:1 | AAA |
| onPrimary #FFFFFF / primary #2E7D32 | 13.5:1 | AAA |
| onPrimaryContainer #002106 / primaryContainer #A6F1A6 | 11.2:1 | AAA |
| onErrorContainer #410002 / errorContainer #FFDAD6 | 9.8:1 | AAA |
| onSecondaryContainer #2A1700 / secondaryContainer #FFDDB3 | 9.1:1 | AAA |
| onSurfaceVariant #424942 / surface #FAFAFA | 7.3:1 | AAA |
| primary #2E7D32 / background #FFFFFF (large text) | 5.8:1 | AA |
| onWarningContainer #E65100 / warningContainer #FFF9C4 | 4.8:1 | AA |

---

## Animation & Motion Spec

### Screen Transitions

| Transition | Type | Duration | Easing |
|---|---|---|---|
| loan-list → loan-detail | containerTransform (card expands to full screen) | 400ms | EmphasizedDecelerate |
| loan-detail → loan-list (back) | containerTransform (reverse) | 350ms | EmphasizedAccelerate |
| loan-list → loan-apply | shared axis Z (forward) | 300ms | StandardDecelerate |
| loan-apply → loan-list (cancel) | shared axis Z (backward) | 300ms | StandardAccelerate |
| Tab switch (bottom nav) | fade through | 200ms | Standard |

### Enter / Exit Animations per Screen

**loan-list**:
- Enter: fade in 200ms (StandardEasing); list items stagger 30ms each from top
- Exit: fade out 150ms

**loan-apply**:
- Enter: slide up from bottom 300ms (EmphasizedDecelerate); elevation 0→2dp
- Exit: slide down 250ms (EmphasizedAccelerate)

**loan-detail**:
- Enter: containerTransform from tapped card 400ms
- Exit: containerTransform reverse 350ms

### Loading Skeleton Shimmer

```
ShimmerSpec:
  direction: left → right
  duration: 1200ms
  easing: LinearEasing (continuous loop)
  gradient: [ surfaceVariant #DEE5DA at 0%, surface #FAFAFA at 50%, surfaceVariant #DEE5DA at 100% ]
  angle: 20° diagonal
  repeat: indefinitely until content loads
  fade-out: shimmer fades out 200ms (standard easing) as real content fades in 200ms
```

### Component Micro-Animations

| Component | Animation | Duration | Easing |
|---|---|---|---|
| FilterChip selection | background color interpolation | 150ms | Standard |
| FAB scroll hide | translate Y +80dp + fade | 200ms | StandardAccelerate |
| FAB scroll show | translate Y 0 + fade in | 300ms | EmphasizedDecelerate |
| Repayment status badge | scale 0.8→1.0 on first appear | 200ms | EmphasizedDecelerate |
| Error snackbar | slide up from bottom | 250ms | StandardDecelerate |
| Error snackbar dismiss | fade out | 200ms | Standard |
| BottomSheet (loan actions) | slide up 350ms (EmphasizedDecelerate); dismiss slide down 300ms |
| Confirm dialog | scale 0.8→1.0 with opacity 0→1 | 250ms | EmphasizedDecelerate |
| Pull-to-refresh indicator | CircularProgressIndicator, primaryContainer tonal; rotate 360° at 900ms/rev |

---

## Test & QA Annotations

### UI Test Tags

| Component | testTag |
|---|---|
| Loan list root | `LoanList_Root` |
| Filter chip "All" | `FilterChip_All` |
| Filter chip "Active" | `FilterChip_Active` |
| Filter chip "Overdue" | `FilterChip_Overdue` |
| Filter chip "Closed" | `FilterChip_Closed` |
| Individual loan card | `LoanCard_{loanId}` |
| Loan card status badge | `LoanCard_{loanId}_StatusBadge` |
| Apply loan FAB | `LoanList_FAB_Apply` |
| Apply form root | `LoanApply_Form` |
| Member selector | `LoanApply_MemberSelector` |
| Product selector | `LoanApply_ProductSelector` |
| Principal field | `LoanApply_PrincipalField` |
| Submit button | `LoanApply_SubmitButton` |
| Eligibility chip | `LoanApply_EligibilityChip` |
| Loan detail root | `LoanDetail_Root` |
| Make repayment button | `LoanDetail_RepaymentButton` |
| Repayment row | `RepaymentRow_{installmentNumber}` |
| Mark defaulted button | `LoanDetail_MarkDefaultedButton` |
| Sync icon button | `TopAppBar_SyncButton` |
| Error snackbar | `Snackbar_Error` |

### Required Test Scenarios — loan-list

```
Given: group has 3 active, 1 overdue, 1 closed loan
When: screen opens
Then: list shows 5 cards; filter "All" is selected; counts in chips match

Given: user taps filter "Overdue"
When: chip selection changes
Then: only the 1 overdue card is shown; chip background changes to errorContainer; TalkBack announces "Showing 1 overdue loan"

Given: network is offline
When: screen opens
Then: cached list is shown; offline banner is visible (warningContainer); sync icon shows disconnected state

Given: user taps "Apply for Loan" FAB
When: navigation occurs
Then: LoanApply_Form is shown; member selector is empty; submit button is disabled

Given: list has 0 loans for the selected filter
When: filter chip is selected
Then: empty state illustration shown; TalkBack announces "No overdue loans found"
```

### Required Test Scenarios — loan-apply

```
Given: user selects a member (Amara Diallo) with insufficient savings
When: eligibility chip renders
Then: chip shows error color; text reads "Not eligible — savings balance KES 400 below minimum"

Given: user enters principal amount "0" or negative value
When: submit is attempted
Then: field border turns error red; error text appears below field; submit button remains disabled

Given: form is completely filled with valid data
When: user taps Submit
Then: loading indicator on button; on success navigate to loan-list; success Snackbar "Loan application submitted for Grace Mwangi"

Given: network fails during submit
When: API call throws IOException
Then: Snackbar "Application queued — will submit when online"; SyncQueue badge appears on bottom nav

Given: server returns 422 with field errors
When: API responds with validation errors
Then: each errored field highlighted; error text below each field; focus moves to first errored field
```

### Required Test Scenarios — loan-detail

```
Given: overdue loan with 2 missed installments
When: loan-detail opens
Then: overdue badge visible; both missed rows show error background; "Make Repayment" button enabled

Given: user taps "Make Repayment" with amount KES 2,000 for Peter Otieno
When: API succeeds
Then: installment row updates to paid (primaryContainer); Snackbar "KES 2,000 recorded for Peter Otieno"

Given: all installments paid
When: detail renders
Then: outstanding balance shows "KES 0"; status chip changes to closed; "Mark Defaulted" button hidden

Given: user taps "Mark as Defaulted" and confirms
When: confirmation dialog dismissed with Confirm
Then: loan status changes to DEFAULTED; error badge appears; Snackbar "Loan marked as defaulted"

Given: loan-detail opened while offline
When: no cached data available
Then: error state shown with message "Unable to load — no cached data available. Reconnect to view details"
```

### Edge Cases

| Scenario | Expected Behavior |
|---|---|
| Empty loan list (new group) | Empty state: "No loans yet — tap + to apply for the first group loan" |
| Single loan | List shows 1 card, no dividers, FAB remains visible |
| 50+ loans | VirtualList (LazyColumn) ensures 60fps scroll; first meaningful paint < 300ms |
| Member name 50+ chars | Text truncated with ellipsis at 2 lines; full name in TalkBack announcement |
| RTL layout | All start/end margins flip; icons mirror correctly; LoanCard status badge remains right-aligned |
| Very large principal (KES 999,999) | Amount formatted with comma separator: "KES 999,999"; no overflow |
| Simultaneous sync + filter | Shimmer overlay only on newly-loading items; existing filtered cards remain visible |

### Performance Baselines

- First meaningful paint (loan-list): < 300ms on mid-range Android (2GB RAM)
- List scroll: 60fps (no dropped frames) for up to 50 loan cards
- Loan-detail open (from tap): < 250ms to start containerTransform animation
- Sync operation: UI remains interactive during background sync (WorkManager job)
- Form submit button feedback: < 100ms to show loading state after tap

---

## i18n / Localization Spec

### String Keys and Translations

| Key | English (en) | Swahili (sw) | French (fr) |
|-----|-------------|--------------|-------------|
| `loan_list_title` | "Loans" | "Mikopo" | "Prêts" |
| `loan_filter_all` | "All" | "Zote" | "Tous" |
| `loan_filter_active` | "Active" | "Zinazoendelea" | "Actifs" |
| `loan_filter_overdue` | "Overdue" | "Zilizochelewa" | "En retard" |
| `loan_filter_closed` | "Closed" | "Zilizofungwa" | "Clôturés" |
| `loan_apply_title` | "New Loan Application" | "Ombi Jipya la Mkopo" | "Nouvelle demande de prêt" |
| `loan_apply_member_label` | "Member" | "Mwanachama" | "Membre" |
| `loan_apply_principal_label` | "Principal Amount (KES)" | "Kiasi cha Mkopo (KES)" | "Montant principal (KES)" |
| `loan_apply_submit` | "Submit Application" | "Wasilisha Ombi" | "Soumettre la demande" |
| `loan_detail_outstanding` | "Outstanding Balance" | "Salio Linalobaki" | "Solde restant dû" |
| `loan_detail_make_repayment` | "Make Repayment" | "Lipa Mkopo" | "Effectuer un remboursement" |
| `loan_detail_mark_defaulted` | "Mark as Defaulted" | "Weka Kama Kushindwa" | "Marquer comme en défaut" |
| `loan_status_active` | "Active" | "Inayoendelea" | "Actif" |
| `loan_status_overdue` | "Overdue" | "Imechelewa" | "En retard" |
| `loan_status_closed` | "Closed" | "Imefungwa" | "Clôturé" |
| `loan_status_pending` | "Pending Approval" | "Inasubiri Idhini" | "En attente d'approbation" |
| `loan_status_defaulted` | "Defaulted" | "Imeshindwa" | "En défaut" |
| `loan_sync_complete` | "Loan data updated" | "Data ya mikopo imesasishwa" | "Données de prêts mises à jour" |
| `loan_offline_banner` | "Offline — showing cached loans" | "Nje ya mtandao — inaonyesha mikopo iliyohifadhiwa" | "Hors ligne — affichage des prêts en cache" |
| `loan_empty_state` | "No {filter} loans found" | "Hakuna mikopo ya {filter} iliyopatikana" | "Aucun prêt {filter} trouvé" |
| `loan_repayment_success` | "KES {amount} recorded for {memberName}" | "KES {amount} imerekodiwa kwa {memberName}" | "KES {amount} enregistré pour {memberName}" |
| `loan_apply_eligible` | "Eligible — savings KES {balance}" | "Anastahili — akiba KES {balance}" | "Éligible — épargne KES {balance}" |
| `loan_apply_ineligible` | "Not eligible — savings KES {balance} below minimum" | "Hastahili — akiba KES {balance} chini ya kiwango" | "Non éligible — épargne KES {balance} en dessous du minimum" |

### Pluralization Rules

Swahili uses a class-based pluralization system. Key plural forms for this feature:

| Key | Singular (sw) | Plural (sw) | English equivalent |
|---|---|---|---|
| `loan_count` | "mkopo 1" | "mikopo {n}" | "{n} loan(s)" |
| `installment_count` | "awamu 1" | "awamu {n}" | "{n} installment(s)" |
| `day_overdue` | "siku 1 imechelewa" | "siku {n} zimechelewa" | "{n} day(s) overdue" |

French pluralization: standard — add "s" for n>1; "un prêt" vs "2 prêts".

### Number Formatting

| Locale | Amount Display | Example |
|---|---|---|
| en-KE (default) | KES 1,234.50 | KES 10,000 / KES 1,234.50 |
| sw-KE | KES 1,234.50 | same format as en-KE |
| fr-FR | KES 1 234,50 | thin-space thousands separator, comma decimal |
| ar (future) | ١٠٬٠٠٠ KES | Eastern Arabic numerals, RTL amount placement |

All KES amounts: no decimal places for whole numbers (KES 10,000 not KES 10,000.00). Decimal shown only for cents-level precision in interest calculations.

### Date Formatting

| Locale | Format | Example |
|---|---|---|
| en-KE | DD MMM YYYY | 15 Jun 2026 |
| sw-KE | DD MMM YYYY | 15 Jun 2026 (same) |
| fr-FR | DD/MM/YYYY | 15/06/2026 |
| en-US | MMM DD, YYYY | Jun 15, 2026 |
| ar (future) | YYYY/MM/DD | 2026/06/15 |

Repayment schedule dates always use the device locale (resolved at runtime via `DateTimeFormatter.ofLocalizedDate(FormatStyle.MEDIUM)`).

### RTL Considerations

- All layout uses `Arrangement.Start`/`End` (logical) — never `Left`/`Right`
- LoanListCard: member name on start, status badge on end; mirrors correctly in RTL
- FAB stays at `Alignment.BottomEnd` (maps to bottom-left in RTL)
- Back arrow icon: auto-mirrored in RTL (`autoMirrored = true`)
- Progress bars: fill from start in LTR, from end in RTL
- Arabic support planned for v3.0 — all string resources structured with placeholder args for word-order flexibility

---

## Offline-First Architecture Notes

### Room DB Schema for Loan Management

The loan-management feature relies on three local Room entities for offline operation:

```
LoanEntity {
  loanId: String (PK)
  memberId: String (FK → MemberEntity)
  groupId: String
  principalAmount: Long (KES, stored as Long in paise-equivalent to avoid Float)
  outstandingBalance: Long
  status: LoanStatus (ACTIVE | OVERDUE | CLOSED | PENDING | DEFAULTED)
  disbursedDate: LocalDate?
  dueDate: LocalDate?
  interestRatePct: Double
  productId: String
  lastSyncedAt: Instant
  isSyncPending: Boolean
}

RepaymentScheduleEntity {
  installmentId: String (PK)
  loanId: String (FK → LoanEntity)
  dueDate: LocalDate
  principalDue: Long
  interestDue: Long
  totalDue: Long
  status: InstallmentStatus (UPCOMING | DUE_TODAY | OVERDUE | PAID | WAIVED)
  paidDate: LocalDate?
  lastSyncedAt: Instant
}

LoanApplicationDraft {
  draftId: String (PK)
  memberId: String
  productId: String
  principalAmount: Long
  repaymentPeriodMonths: Int
  guarantor1Id: String?
  guarantor2Id: String?
  createdAt: Instant
  syncStatus: SyncStatus (PENDING | SYNCING | FAILED | DONE)
}
```

### SyncQueue Processing Order

Loan-related SyncQueue entries are processed in this priority order:
1. `REPAYMENT` entries (highest priority — money movement)
2. `LOAN_APPLICATION` entries (member waiting for approval)
3. `LOAN_STATUS_UPDATE` entries (defaulted, closed)
4. `LOAN_LIST_REFRESH` entries (lowest priority — read-only refresh)

Conflict resolution: if server state differs from local state (e.g. loan marked CLOSED on server but ACTIVE locally), server state wins. Local state is updated and UI refreshes automatically.

### Pessimistic UI for Repayments

Repayments are NOT optimistically updated in the UI — too high-stakes. Flow:
1. User taps "Make Repayment"
2. Loading state on button
3. API call completes (or fails → SyncQueue)
4. Only on success: update RepaymentScheduleEntity; refresh UI
5. On failure: show error state; do NOT show paid state speculatively

Rationale: falsely showing a repayment as "paid" when it is still pending could cause member disputes and data integrity issues in group lending contexts.

### Data Freshness Indicators

| Staleness | Indicator | Color |
|---|---|---|
| < 1 hour | No indicator (fresh) | — |
| 1–24 hours | Subtitle: "Synced {n} hours ago" | onSurfaceVariant |
| > 24 hours | Warning chip: "Data may be outdated — tap to refresh" | warningContainer #FFF9C4 |
| Never synced (offline since install) | Banner: "No server data — offline mode only" | warningContainer |
