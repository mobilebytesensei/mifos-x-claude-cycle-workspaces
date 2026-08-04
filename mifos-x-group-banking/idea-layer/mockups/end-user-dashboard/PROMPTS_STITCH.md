# End-User Dashboard — Stitch Prompts

---

## 1. Design System Context

### Overview

MifosSave is a Kotlin Multiplatform group-banking app serving Village Savings and Loan Associations (VSLAs) in rural East Africa. The end-user dashboard is the self-service face of the app — designed specifically for group members who want to check their savings, understand their loans, and request new credit. The visual language is warm, green (VSLA-green for growth), and emphasises positive financial progress.

The design system is Material Design 3 (M3) with a custom brand palette and a large typography scale optimised for outdoor daylight reading. The primary target device is a mid-range Android phone (Samsung Galaxy A32, 6.4" screen, 360dp width).

### Brand Identity

**App name**: MifosSave
**Tagline**: "Your community savings group"
**Logo**: Leaf-and-coin SVG mark (leaf = growth, coin = shared savings)
**Tone of voice**: Warm, encouraging, community-focused. "Your savings", not "Account balance". "Need a loan?" not "Apply for credit."

### Full Color Palette — Light Mode

| Token | Hex | RGB | Usage |
|-------|-----|-----|-------|
| primary | #2E7D32 | 46, 125, 50 | Brand green — buttons, active states, top bars, savings icons, progress |
| on_primary | #FFFFFF | 255, 255, 255 | Text/icons on primary backgrounds |
| primary_container | #A6F1A6 | 166, 241, 166 | Soft green — tab unselected, group banner chip, savings detail header |
| on_primary_container | #002106 | 0, 33, 6 | Dark green — text on primary_container |
| secondary | #FF8F00 | 255, 143, 0 | Amber — FAB, extended FAB, harvest colour |
| on_secondary | #FFFFFF | 255, 255, 255 | Text/icons on secondary |
| secondary_container | #FFDDB3 | 255, 221, 179 | Light amber — offline banner, share-out card, individual promo |
| on_secondary_container | #2A1700 | 42, 23, 0 | Dark brown — text on secondary_container |
| tertiary | #1565C0 | 21, 101, 192 | Trust-blue — loan info, repayment estimate colour |
| on_tertiary | #FFFFFF | 255, 255, 255 | Text on tertiary |
| tertiary_container | #D2E4FF | 210, 228, 255 | Light blue — loan request CTA card, savings limit card |
| on_tertiary_container | #001C39 | 0, 28, 57 | Deep navy — text on tertiary_container |
| error | #D32F2F | 211, 47, 47 | Alert red — overdue badges, withdrawal amounts, error banners |
| on_error | #FFFFFF | 255, 255, 255 | Text on error |
| error_container | #FFDAD6 | 255, 218, 214 | Soft red — inline error backgrounds |
| on_error_container | #410002 | 65, 0, 2 | Deep red — text on error_container |
| background | #FFFFFF | 255, 255, 255 | Page background |
| on_background | #1A1C19 | 26, 28, 25 | Primary text on background |
| surface | #FAFAFA | 250, 250, 250 | Card surfaces |
| on_surface | #1A1C19 | 26, 28, 25 | Primary text on cards |
| surface_variant | #DEE5DA | 222, 229, 218 | Chip backgrounds, icon containers, shimmer base |
| on_surface_variant | #424942 | 66, 73, 66 | Secondary text, icons, captions |
| outline | #727971 | 114, 121, 113 | Input borders, dividers, date labels |
| outline_variant | #C2C9BD | 194, 201, 189 | Inactive borders, light dividers |
| scrim | #000000 | 0, 0, 0 | Modal overlays (dialog backdrop at 40%) |
| inverse_surface | #2F312D | 47, 49, 45 | Snackbar background |
| inverse_on_surface | #F0F1EB | 240, 241, 235 | Snackbar text |
| inverse_primary | #8BD68F | 139, 214, 143 | Primary accent on dark |

### Full Color Palette — Dark Mode

| Token | Hex | Usage |
|-------|-----|-------|
| primary | #8BD68F | Lighter VSLA-green for dark backgrounds |
| on_primary | #003910 | Dark green on primary |
| primary_container | #00531A | Dark green container |
| on_primary_container | #A6F1A6 | Soft green text |
| secondary | #FFB95C | Bright amber for dark mode |
| on_secondary | #472A00 | Dark text |
| secondary_container | #653E00 | Dark amber |
| on_secondary_container | #FFDDB3 | Light text on dark amber |
| tertiary | #9FCAFF | Lighter blue |
| on_tertiary | #00325B | Dark blue |
| tertiary_container | #004A82 | Deep blue |
| on_tertiary_container | #D2E4FF | Light blue text |
| error | #FFB4AB | Soft red for dark |
| on_error | #690005 | Dark red |
| error_container | #93000A | Dark red container |
| on_error_container | #FFDAD6 | Soft pink text |
| background | #1A1C19 | Dark background |
| on_background | #E2E3DD | Off-white text |
| surface | #121412 | Very dark card surface |
| on_surface | #E2E3DD | Light text |
| surface_variant | #424942 | Medium grey |
| on_surface_variant | #C2C9BD | Light grey secondary text |
| outline | #8C9388 | Medium grey borders |

### Typography Scale

Font: **Noto Sans** (excellent Unicode support for Swahili, French, English, Kiswahili, Hindi).
Scale: Large (+1 above standard M3) for outdoor/low-light readability.

| Style | Size (sp) | Line-Height (sp) | Tracking (sp) | Weight | Dashboard Usage |
|-------|-----------|-----------------|---------------|--------|----------------|
| displayLarge | 57 | 64 | -0.25 | 400 | Not used in this feature |
| displayMedium | 45 | 52 | 0 | 400 | Large balance in future hero |
| displaySmall | 36 | 44 | 0 | 400 | Primary balance figure on SavingsSummaryCard |
| headlineLarge | 32 | 40 | 0 | 400 | Not used in this feature |
| headlineMedium | 28 | 36 | 0 | 400 | Screen section headings (rare) |
| headlineSmall | 24 | 32 | 0 | 400 | Loan outstanding amount, savings balance on hero |
| titleLarge | 22 | 28 | 0 | 500 | Top bar titles |
| titleMedium | 16 | 24 | 0.15 | 500 | Section headers, selected duration |
| titleSmall | 14 | 20 | 0.1 | 500 | Small section subtitles |
| bodyLarge | 16 | 24 | 0.5 | 400 | Card body text, transaction amounts, input text |
| bodyMedium | 14 | 20 | 0.25 | 400 | Card descriptions, error text, supporting text |
| bodySmall | 12 | 16 | 0.4 | 400 | Contribution row min/max labels |
| labelLarge | 14 | 20 | 0.1 | 500 | Button labels, card sub-headers, chip text |
| labelMedium | 12 | 16 | 0.5 | 500 | Date labels, account numbers, status chips |
| labelSmall | 11 | 16 | 0.5 | 500 | Running balance, fine print |

### Spacing Scale

| Token | dp | Typical Usage |
|-------|-----|--------------|
| spacing_xxs | 2 | Fine-grain adjustments |
| spacing_xs | 4 | Icon-to-text gap |
| spacing_sm | 8 | Card inner spacing, chip padding |
| spacing_md | 12 | Card padding secondary, form spacing |
| spacing_lg | 16 | Standard horizontal screen margin |
| spacing_xl | 24 | Card padding primary, section gap |
| spacing_xxl | 32 | Large section gaps |
| spacing_3xl | 48 | Generous whitespace on large screens |
| spacing_4xl | 64 | Hero section top padding |

### Shape Tokens

| Token | Radius | Dashboard Usage |
|-------|--------|----------------|
| shape_none | 0dp | Dividers |
| shape_extra_small | 4dp | Dense chips |
| shape_small | 8dp | Offline banner, snackbar |
| shape_medium | 12dp | Duration selector card, filter chips text field |
| shape_large | 16dp | Main cards (savings, loan, share-out, CTA) |
| shape_extra_large | 28dp | Bottom sheet corners |
| shape_full | 9999dp | Filter chips, FAB, submit button, tab chips |

### Elevation

| Level | dp | Tonal Alpha | Dashboard Usage |
|-------|-----|------------|----------------|
| level_0 | 0 | 0.00 | Group banner, share-out card, CTA card (intentionally flat) |
| level_1 | 1 | 0.05 | Duration selector card |
| level_2 | 3 | 0.08 | Savings card, loan card, contribution progress card |
| level_3 | 6 | 0.11 | Dialog background |
| level_4 | 8 | 0.12 | Bottom sheet |
| level_5 | 12 | 0.14 | FAB, extended FAB |

### Motion Tokens

| Token | Duration (ms) | Easing | Dashboard Usage |
|-------|--------------|--------|----------------|
| short_1 | 50 | standard | Micro state changes |
| short_2 | 100 | standard | Icon state, chip selection |
| short_3 | 150 | standard | Shimmer item fade-in |
| short_4 | 200 | standard | Card press ripple |
| medium_1 | 250 | emphasized | Filter chip transition |
| medium_2 | 300 | emphasized | Loan card expand, screen navigation |
| medium_3 | 350 | emphasized | Shimmer → content transition |
| medium_4 | 400 | emphasized | Full-page content load |
| long_1 | 450 | decelerated | Complex card animations |
| long_2 | 500 | decelerated | Dashboard initial load |

Easing:
- standard: cubic-bezier(0.2, 0.0, 0, 1.0)
- emphasized: cubic-bezier(0.2, 0.0, 0, 1.0)
- decelerated: cubic-bezier(0.0, 0.0, 0, 1.0)
- accelerated: cubic-bezier(0.3, 0.0, 1.0, 1.0)

### Accessibility Baseline

- Min touch target: 48dp (all interactive elements)
- Contrast normal text (≥12sp): 4.5:1 minimum
- Contrast large text (≥18sp bold): 3.0:1 minimum
- Focus ring: 3dp, primary colour
- All icons with semantic meaning: contentDescription required
- Error states: live_region="polite" or "assertive" depending on urgency
- Offline banner: live_region="polite"
- Error snackbar: live_region="assertive"
- Shimmer loading: contentDescription "Loading your dashboard" / "Loading savings" / "Loading loans"

---

## 2. Screen Layouts

### PersonalDashboardScreen — Full Component Tree

Screen: 360dp × 800dp compact baseline.
Status bar: 24dp. Navigation bar: 48dp.
Background: #FFFFFF.

```
Screen (360dp × 800dp)
└── Scaffold(
      topBar = DashboardTopBar,
      bottomBar = BottomNavigationBar,
      containerColor = background (#FFFFFF)
    )
    ├── DashboardTopBar (height 64dp)
    │     background = primary (#2E7D32), elevation = 0dp
    │     ├── Column (title composable, start-aligned, paddingStart 16dp)
    │     │     ├── Text(greeting + memberName)
    │     │     │     text = "Good morning, Grace"
    │     │     │     style = titleMedium (16sp, weight 500)
    │     │     │     color = on_primary (#FFFFFF)
    │     │     └── Text(groupName)
    │     │           text = "Mwangaza Women's Group"
    │     │           style = bodyMedium (14sp)
    │     │           color = on_primary (#FFFFFF) opacity 0.8
    │     └── IconButton (notifications, end-aligned)
    │           icon = FluentIcons.alert_24_regular
    │           tint = on_primary (#FFFFFF)
    │           size = 48dp touch target
    │           Badge: count label labelSmall, background error (#D32F2F)
    │
    ├── LazyColumn (fillMaxSize)
    │     verticalArrangement = Arrangement.Top
    │     paddingBottom = 80dp (bottom nav height)
    │     │
    │     ├── GroupBanner (full width)
    │     │     background = primary (#2E7D32)
    │     │     padding = top 16dp, horizontal 24dp, bottom 24dp
    │     │     elevation = 0dp
    │     │     Row(verticalAlignment = CenterVertically)
    │     │       ├── Text("Mwangaza Women's Group")
    │     │       │     style = bodyLarge (16sp), weight semibold
    │     │       │     color = on_primary (#FFFFFF)
    │     │       │     modifier = weight(1f)
    │     │       └── Chip("KES")
    │     │             background = primary_container (#A6F1A6)
    │     │             textColor = on_primary_container (#002106)
    │     │             cornerRadius = full (9999dp)
    │     │             padding = top/bottom 4dp, horizontal 12dp
    │     │             style = labelMedium (12sp, weight 500)
    │     │
    │     ├── SavingsSummaryCard
    │     │     width = 328dp (360 - 32dp margins)
    │     │     marginHorizontal = 16dp
    │     │     marginTop = -20dp  ← overlaps GroupBanner bottom by 20dp
    │     │     background = surface (#FAFAFA)
    │     │     cornerRadius = 16dp [shape_large]
    │     │     elevation = 3dp [level_2]
    │     │     padding = 20dp
    │     │     ├── Row(header)
    │     │     │     icon = FluentIcons.savings_24_filled 20dp primary (#2E7D32)
    │     │     │     Text "Total Savings" labelLarge (14sp, weight 500) on_surface_variant
    │     │     │     Spacer(weight=1f)
    │     │     │     icon = FluentIcons.chevron_right_24_regular on_surface_variant
    │     │     ├── Text "KES 12,450"
    │     │     │     style = displaySmall (36sp), weight bold, Noto Sans
    │     │     │     color = on_surface (#1A1C19)
    │     │     │     marginTop = 4dp
    │     │     └── Row(breakdown)
    │     │           marginTop = 8dp
    │     │           ├── Column(group-linked, weight 1f)
    │     │           │     Text "Group-linked" labelMedium on_surface_variant
    │     │           │     Text "KES 9,600" bodyLarge weight semibold primary (#2E7D32)
    │     │           └── Column(individual, weight 1f)
    │     │                 Text "Individual" labelMedium on_surface_variant
    │     │                 Text "KES 2,850" bodyLarge weight semibold secondary (#FF8F00)
    │     │
    │     ├── [when activeLoan != null] LoanSummaryCard
    │     │     width = 328dp, marginHorizontal = 16dp, marginTop = 12dp
    │     │     background = surface, cornerRadius = 16dp, elevation = 3dp, padding = 20dp
    │     │     ├── Row(header)
    │     │     │     icon = FluentIcons.money_24_filled 20dp tertiary (#1565C0)
    │     │     │     Text "Active Loan" labelLarge on_surface_variant
    │     │     │     Spacer(weight=1f)
    │     │     │     icon = FluentIcons.chevron_right_24_regular on_surface_variant
    │     │     ├── Text "KES 15,000"
    │     │     │     style = headlineSmall (24sp) on_surface, weight bold
    │     │     │     marginTop = 4dp
    │     │     └── Row(next repayment)
    │     │           marginTop = 8dp
    │     │           [if isOverdue] icon warning_24_filled 16dp error
    │     │           Text "Next repayment" labelMedium on_surface_variant
    │     │           Text " KES 1,500 · 15 May 2026" bodyMedium
    │     │             color = [isOverdue: error (#D32F2F)] [normal: on_surface]
    │     │
    │     ├── [when activeLoan == null] RequestLoanCta
    │     │     width = 328dp, marginHorizontal = 16dp, marginTop = 12dp
    │     │     background = tertiary_container (#D2E4FF)
    │     │     cornerRadius = 16dp, elevation = 0dp, padding = 20dp
    │     │     Row(verticalAlignment = CenterVertically, gap = 16dp)
    │     │       ├── icon add_circle_24_filled 40dp on_tertiary_container (#001C39)
    │     │       └── Column
    │     │             Text "Need a loan?" titleMedium on_tertiary_container
    │     │             Text "Apply for up to KES 37,350 (3× your savings)"
    │     │               bodyMedium on_tertiary_container opacity 0.8
    │     │
    │     ├── ShareOutProjectionCard
    │     │     width = 328dp, marginHorizontal = 16dp, marginTop = 12dp
    │     │     background = secondary_container (#FFDDB3)
    │     │     cornerRadius = 16dp, elevation = 0dp, padding = 16dp
    │     │     Row(verticalAlignment = CenterVertically)
    │     │       ├── icon trophy_24_filled 24dp on_secondary_container (#2A1700)
    │     │       ├── Spacer(8dp)
    │     │       └── Column
    │     │             Text "Projected share-out" labelLarge on_secondary_container
    │     │             Text "KES 38,250" headlineSmall bold on_secondary_container
    │     │
    │     ├── Text "Recent Activity"
    │     │     style = titleMedium (16sp, weight 500)
    │     │     color = on_surface (#1A1C19)
    │     │     marginHorizontal = 16dp, marginTop = 24dp, marginBottom = 8dp
    │     │
    │     └── [repeated] RecentActivityListItem
    │           height = 56dp min, minTouchTarget = 48dp
    │           padding = horizontal 16dp, vertical 8dp
    │           Divider below each item (1dp, outline_variant)
    │           Row(verticalAlignment = CenterVertically, gap = 12dp)
    │             ├── Icon(deposit: arrow_download_24_filled primary OR withdrawal: arrow_upload_24_filled error)
    │             │     size = 24dp
    │             ├── Column(weight=1f)
    │             │     Text(type) bodyLarge on_surface
    │             │     Text(date) labelMedium outline
    │             └── Text(amount)
    │                   deposit: "+KES 500" bodyLarge semibold primary (#2E7D32)
    │                   withdrawal: "-KES 200" bodyLarge semibold error (#D32F2F)
    │
    └── BottomNavigationBar (height 80dp)
          background = surface (#FAFAFA), elevation = 3dp
          Items: Dashboard (home icon, selected=primary), Savings (savings icon), Loans (money icon)
          Selected indicator: primary_container pill behind icon
```

Z-ordering note: SavingsSummaryCard has marginTop = -20dp, creating an overlap with the GroupBanner. The card uses elevation (3dp) to render above the banner's flat surface. This creates the "card emerges from green header" effect common in financial apps.

---

### PersonalSavingsScreen — Full Component Tree

Screen: 360dp × 800dp.

```
Screen (360dp × 800dp)
└── Scaffold(topBar = SavingsTopBar, bottomBar = BottomNav, containerColor = surface)
    ├── SavingsTopBar (height 64dp)
    │     background = primary (#2E7D32), elevation = 0dp
    │     NavigationIcon: arrow_left_24_regular 24dp on_primary
    │     Title: "My Savings" titleLarge (22sp) on_primary
    │
    └── Content Column (scrollable)
          ├── SavingsTabRow (full width)
          │     background = primary_container (#A6F1A6)
          │     padding = horizontal 16dp, vertical 12dp
          │     Row(gap = 8dp)
          │       ├── Tab 1 "Group-linked"
          │       │     [selected] background = primary (#2E7D32), text = on_primary (#FFFFFF)
          │       │     [unselected] background = primary_container, text = on_primary_container
          │       │     icon = people_community_24_filled 18dp
          │       │     text = "Group-linked" labelLarge (14sp, weight 500)
          │       │     cornerRadius = full (9999dp)
          │       │     padding = vertical 8dp, horizontal 16dp
          │       └── Tab 2 "Individual" (hidden when individualSavingsId == null)
          │             [selected] background = primary, text = on_primary
          │             icon = person_circle_24_filled 18dp
          │             text = "Individual" labelLarge
          │             cornerRadius = full
          │
          ├── BalanceHeroCard
          │     width = 328dp, marginHorizontal = 16dp, marginBottom = 16dp
          │     background = primary (#2E7D32)
          │     cornerRadius = 16dp, elevation = 0dp, padding = 24dp
          │     ├── Text(label)
          │     │     [GROUP_LINKED] "Group-Linked Savings"
          │     │     [INDIVIDUAL] "Individual Savings"
          │     │     style = labelLarge (14sp, weight 500)
          │     │     color = on_primary (#FFFFFF) opacity 0.8
          │     ├── Text(amount)
          │     │     [GROUP_LINKED] "KES 9,600"
          │     │     [INDIVIDUAL] "KES 2,850"
          │     │     style = displaySmall (36sp), weight bold, Noto Sans
          │     │     color = on_primary (#FFFFFF)
          │     │     marginTop = 4dp
          │     └── Text(account number)
          │           text = "Acc: 000100012345"
          │           style = labelMedium (12sp, weight 500)
          │           color = on_primary (#FFFFFF) opacity 0.7
          │           marginTop = 8dp
          │
          ├── [GROUP_LINKED tab only] ContributionProgressCard
          │     width = 328dp, marginHorizontal = 16dp, marginBottom = 12dp
          │     background = surface (#FAFAFA)
          │     cornerRadius = 16dp, elevation = 3dp, padding = 16dp
          │     ├── Row(header, gap 8dp)
          │     │     icon = calendar_checkmark_24_filled 20dp primary (#2E7D32)
          │     │     Text "Contribution Progress" labelLarge on_surface_variant
          │     ├── Text "18 / 24 meetings"
          │     │     style = bodyMedium on_surface marginTop 8dp
          │     ├── LinearProgressIndicator
          │     │     progress = 0.75 (18/24)
          │     │     height = 8dp
          │     │     trackColor = primary_container (#A6F1A6)
          │     │     progressColor = primary (#2E7D32)
          │     │     cornerRadius = full
          │     │     marginTop = 8dp
          │     └── Row (contribution summary)
          │           marginTop = 8dp
          │           Text "KES 100 min" bodySmall on_surface_variant
          │           Spacer(weight=1f)
          │           Text "This cycle: KES 9,600" bodySmall on_surface_variant semibold
          │           Spacer(weight=1f)
          │           Text "KES 500 max" bodySmall on_surface_variant
          │
          ├── Text "Transaction History"
          │     style = titleMedium (16sp, weight 500) on_surface semibold
          │     marginHorizontal = 16dp, marginTop = 8dp, marginBottom = 4dp
          │
          └── [repeated] SavingsTransactionListItem
                height = 72dp min
                padding = horizontal 16dp, vertical 12dp
                Divider below each
                Row(verticalAlignment = CenterVertically, gap = 12dp)
                  ├── Box(size=40dp, shape=circle, background=surface_variant)
                  │     Icon(deposit: trending_up_24_filled primary OR withdrawal: trending_down_24_filled error)
                  │     icon size = 24dp, centred
                  ├── Column(weight=1f)
                  │     Text(transaction type)
                  │       "Deposit" / "Withdrawal" / "Meeting contribution"
                  │       style = bodyLarge (16sp) on_surface
                  │     Text(date) "15 Apr 2026" bodySmall on_surface_variant
                  └── Column(end-aligned)
                        Text(amount) "+KES 500" bodyLarge semibold
                          deposit: color = primary (#2E7D32)
                          withdrawal: color = error (#D32F2F)
                        Text("Balance: KES 9,600") labelSmall outline
```

---

### PersonalLoansScreen — Full Component Tree

Screen: 360dp × 800dp.

```
Screen (360dp × 800dp)
└── Scaffold(topBar = LoansTopBar, bottomBar = BottomNav, floatingActionButton = RequestLoanFab)
    ├── LoansTopBar (height 64dp)
    │     background = primary (#2E7D32), elevation = 0dp
    │     NavigationIcon: arrow_left_24_regular on_primary
    │     Title: "My Loans" titleLarge on_primary
    │
    ├── LazyColumn (fillMaxSize, paddingBottom = 80dp + 88dp FAB clearance)
    │     ├── LoanStatusFilterChips (full width)
    │     │     horizontalScroll = true
    │     │     paddingHorizontal = 16dp, paddingVertical = 8dp, chipSpacing = 8dp
    │     │     Chips: "All", "Active", "Closed"
    │     │     [selected] background = primary, text = on_primary
    │     │     [unselected] background = surface, border = outline 1dp, text = on_surface
    │     │     cornerRadius = full, padding = 6dp × 14dp
    │     │
    │     └── [repeated] LoanCard
    │           width = 328dp, marginHorizontal = 16dp, marginBottom = 12dp
    │           background = surface (#FAFAFA)
    │           cornerRadius = 16dp, elevation = 3dp, padding = 16dp
    │           │
    │           ├── [COLLAPSED VIEW]
    │           │     Row(header, verticalAlignment = CenterVertically)
    │           │       ├── Column(weight=1f)
    │           │       │     Text(productName) titleMedium (16sp, weight 500) on_surface
    │           │       │     Text(accountNo) labelSmall on_surface_variant
    │           │       ├── StatusChip
    │           │       │     [Active] background=primary_container, text=on_primary_container, text="Active"
    │           │       │     [Pending] background=secondary_container, text=on_secondary_container, text="Pending"
    │           │       │     [Closed] background=surface_variant, text=on_surface_variant, text="Closed"
    │           │       │     [Overdue] background=error_container, text=on_error_container, text="Overdue"
    │           │       │     cornerRadius=full, padding=4dp × 10dp, style=labelMedium
    │           │       └── Icon(chevron_down OR chevron_up) 24dp on_surface_variant
    │           │     Divider(marginTop=12dp, marginBottom=12dp, color=outline_variant)
    │           │     Row(balance)
    │           │       Text "Outstanding" labelMedium on_surface_variant
    │           │       Spacer(weight=1f)
    │           │       Text "KES 15,000" headlineSmall bold on_surface
    │           │     [if active loan] Row(next repayment, marginTop=8dp)
    │           │       [if isOverdue] icon warning_24_filled 16dp error
    │           │       Text "Next repayment:" bodyMedium on_surface_variant
    │           │       Spacer(4dp)
    │           │       Text "KES 1,500 · 15 May 2026" bodyMedium
    │           │         color = [isOverdue: error] [normal: on_surface]
    │           │
    │           └── [EXPANDED VIEW — AnimatedVisibility]
    │                 Divider(marginTop=12dp, marginBottom=8dp)
    │                 Text "Repayment Schedule" labelLarge on_surface_variant marginBottom=8dp
    │                 [repeated] RepaymentPeriodRow
    │                   height = 40dp min
    │                   Row(verticalAlignment = CenterVertically, gap = 8dp)
    │                     icon:
    │                       [complete] checkmark_circle_24_filled primary (#2E7D32)
    │                       [pending] circle_24_regular on_surface_variant
    │                       [overdue] dismiss_circle_24_filled error (#D32F2F)
    │                       icon size = 20dp
    │                     Text "#1" labelMedium on_surface_variant width=24dp
    │                     Text(dueDate) bodyMedium on_surface weight=1f
    │                     Text(amount) bodyLarge
    │                       [complete] on_surface_variant
    │                       [pending] on_surface
    │                       [overdue] error (#D32F2F)
    │
    └── RequestLoanFab (ExtendedFloatingActionButton)
          background = secondary (#FF8F00)
          icon = add_24_filled 24dp on_secondary (#FFFFFF)
          text = "Request Loan" labelLarge on_secondary
          cornerRadius = full
          elevation = 12dp [level_5]
          minTouchTarget = 56dp
          visible when loans.isNotEmpty()
          position: end-bottom (Scaffold FAB anchor)
          marginEnd = 16dp, marginBottom = 24dp
```

---

### LoanRequestScreen — Full Component Tree

Screen: 360dp × 800dp.
Keyboard avoidance: imePadding() on Column.

```
Screen (360dp × 800dp)
└── Scaffold(topBar = LoanRequestTopBar, containerColor = surface)
    ├── LoanRequestTopBar (height 64dp)
    │     background = primary (#2E7D32), elevation = 0dp
    │     NavigationIcon: arrow_left_24_regular on_primary
    │     Title: "Request a Loan" titleLarge on_primary
    │
    └── Column (fillMaxSize, verticalScroll, imePadding)
          ├── [visible when isOfflineMode=true] OfflineModeBanner
          │     width = 328dp, marginHorizontal = 16dp, marginTop = 8dp
          │     background = secondary_container (#FFDDB3)
          │     cornerRadius = 8dp [shape_small]
          │     padding = vertical 8dp, horizontal 16dp
          │     Row(gap = 8dp, verticalAlignment = CenterVertically)
          │       icon = wifi_off_24_filled 20dp on_secondary_container
          │       Text "You are offline. Your request will be saved and sent when you reconnect."
          │         bodySmall (12sp) on_secondary_container
          │
          ├── SavingsLimitCard
          │     width = 328dp, marginHorizontal = 16dp, marginTop = 12dp
          │     background = tertiary_container (#D2E4FF)
          │     cornerRadius = 16dp, elevation = 0dp, padding = 16dp
          │     ├── Row(row 1, gap 8dp, marginBottom 8dp)
          │     │     icon = savings_24_filled 20dp on_tertiary_container
          │     │     Text "Your savings balance" labelMedium on_tertiary_container
          │     │     Spacer(weight=1f)
          │     │     Text "KES 12,450" bodyLarge on_tertiary_container
          │     └── Row(row 2, gap 8dp)
          │           icon = money_24_filled 20dp on_tertiary_container
          │           Column(weight=1f)
          │             Text "Maximum you can borrow" labelMedium on_tertiary_container
          │             Text "(3× your savings)" bodySmall on_tertiary_container opacity 0.7
          │           Text "KES 37,350" titleMedium bold on_tertiary_container
          │
          ├── OutlinedTextField (LoanAmountField)
          │     width = 328dp, marginHorizontal = 16dp, marginTop = 16dp
          │     label = "Loan Amount (KES)"
          │     prefix = "KES " (textStyle = bodyLarge primary)
          │     placeholder = "0"
          │     leadingIcon = money_24_regular 24dp on_surface_variant
          │     keyboardType = Number, imeAction = Next
          │     supportingText = "Enter amount between KES 500 and your maximum" bodySmall
          │     errorText = requestedAmountError (bodySmall error colour)
          │     activeColour = primary (#2E7D32)
          │
          ├── ExposedDropdownMenuBox (LoanPurposeDropdown)
          │     width = 328dp, marginHorizontal = 16dp, marginTop = 12dp
          │     label = "Loan Purpose"
          │     leadingIcon = notepad_24_regular 24dp on_surface_variant
          │     trailingIcon = chevron_down_24_regular (rotates on expand)
          │     Options (each 48dp height):
          │       "School Fees"
          │       "Medical Emergency"
          │       "Business"
          │       "Farming / Agriculture"
          │       "Home Improvement"
          │       "Emergency"
          │       "Other"
          │     errorText = purposeError
          │
          ├── DurationSelector (Card)
          │     width = 328dp, marginHorizontal = 16dp, marginTop = 12dp
          │     background = surface (#FAFAFA)
          │     cornerRadius = 12dp [shape_medium], elevation = 1dp, padding = 16dp
          │     ├── Text "Repayment Duration" labelLarge on_surface_variant
          │     ├── Text "12 weeks" titleLarge (22sp) bold on_surface marginTop=4dp
          │     ├── Slider
          │     │     value = 12, range = 4..52, steps = 12 (4-week increments)
          │     │     activeTrackColor = primary (#2E7D32)
          │     │     inactiveTrackColor = primary_container (#A6F1A6)
          │     │     thumbColor = primary (#2E7D32)
          │     │     thumbRadius = 10dp, touchTarget = 48dp
          │     │     marginTop = 8dp
          │     └── Row(repayment estimate, marginTop=8dp)
          │           Text "Weekly repayment estimate:" bodyMedium on_surface_variant
          │           Spacer(weight=1f)
          │           Text "KES 3,223" bodyLarge tertiary (#1565C0) semibold
          │
          ├── [visible when amount valid] RepaymentSummaryCard
          │     width = 328dp, marginHorizontal = 16dp, marginTop = 12dp
          │     background = surface_variant (#DEE5DA)
          │     cornerRadius = 12dp, elevation = 0dp, padding = 16dp
          │     ├── Row "Principal" + Spacer + "KES 37,350" bodyLarge on_surface_variant
          │     ├── Row "Interest (group rate)" + Spacer + "KES 1,300" bodyLarge on_surface_variant
          │     ├── Divider (outline_variant, marginVertical 8dp)
          │     └── Row "Total to repay" + Spacer + "KES 38,650" titleMedium bold on_surface
          │
          ├── [visible when !isSubmitting] SubmitButton (FilledButton)
          │     width = 328dp, marginHorizontal = 16dp
          │     marginTop = 24dp, marginBottom = 24dp
          │     background = [enabled] primary (#2E7D32) / [disabled] surface_variant
          │     text = "Submit Application" labelLarge
          │     textColor = [enabled] on_primary (#FFFFFF) / [disabled] on_surface_variant
          │     cornerRadius = full (9999dp), minHeight = 56dp
          │
          └── [visible when isSubmitting] CircularProgressIndicator
                size = 32dp, stroke = 3dp
                color = primary (#2E7D32)
                alignment = Center
                marginTop = 24dp
```

---

## 3. Component Specifications

### SavingsSummaryCard — Complete Spec

**Purpose**: The first thing a member sees below the green header. Immediately answers "how much have I saved?" with a single large number, then provides context below.

**Key UX decisions**:
- displaySmall (36sp) for the balance — readable at arm's length in outdoor daylight
- The -20dp margin overlapping the GroupBanner creates visual depth: card "rises from" the green band
- Two-line breakdown (group-linked + individual) avoids hiding important sub-totals

**Variants by state**:
- Loading: shimmer placeholder (height 130dp, cornerRadius lg)
- Content: full balance with breakdown
- Stale data (offline): subtle "Cached" badge in top-right (outlineVariant background, labelSmall)
- Error: hidden (error_state shown instead)

**Balance formatting**:
- Format: "KES {amount}" where amount is formatted with comma-thousands: 12,450
- Currency symbol always precedes number with space: "KES 12,450" not "12,450 KES"
- Negative balance (theoretical): shown in error colour with minus sign

**Breakdown row**:
- Two equal-width columns via Row(horizontalArrangement = SpaceEvenly)
- Group-linked: primary (#2E7D32) — emphasises this is the community savings
- Individual: secondary (#FF8F00) — warm amber, voluntary contribution

**Tap area**: entire card is one tap target (no internal tappable sub-regions)

---

### LoanSummaryCard — Complete Spec

**Purpose**: Visible when member has an active loan. Answers: "what do I owe and when is it due?" Overdue state adds urgency via red colour + warning icon.

**Content states**:
1. Active, not overdue: outstanding amount in on_surface, next repayment in on_surface, next repayment date
2. Active, overdue: outstanding amount in on_surface, next repayment amount in error (#D32F2F), warning_24_filled icon, "Overdue" badge in errorContainer
3. Pending approval: outstanding shows "-" (not disbursed); chip shows "Pending" secondaryContainer
4. Closed: card not shown (RequestLoanCta shown instead)

**Overdue indicator layout**:
```
Row(gap=4dp, verticalAlignment=CenterVertically)
  icon warning_24_filled 16dp error
  Text "Overdue" labelSmall bold error
  Spacer(weight=1f)
  Text "Was due 5 May 2026" bodySmall error
```

---

### RequestLoanCta — Complete Spec

**Purpose**: Prompt for members with no active loan. Shown when activeLoan == null. The amount "KES 37,350 (3× your savings)" is personalised — updates based on current savings balance.

**Copy logic**:
- maxLoanAmount = savingsBalance × loanMultiplier (3.0 by default, configurable in dt_group_config)
- If savingsBalance = 12,450 and multiplier = 3.0: maxLoanAmount = KES 37,350
- Subtitle: "Apply for up to KES {maxLoanAmount} (3× your savings)"

**Visual weight**: Uses tertiaryContainer (blue) to differentiate from savings (green) and share-out (amber). The blue signals informational/action rather than status.

---

### ShareOutProjectionCard — Complete Spec

**Purpose**: Shows how much this member will receive at cycle end. Motivational — encourages continued savings.

**Projection calculation** (displayed value only, calculated server-side or via formula):
- If total group corpus = KES 450,000
- Member's savings ratio = 12,450 / total_group_savings
- Projected share-out = member_ratio × (corpus + cycle profit)
- Display: "KES 38,250" (example for Grace Mwangi)

**Trophy icon**: FluentIcons.trophy_24_filled — celebrates financial achievement. Warm amber background (secondaryContainer) creates positive association.

---

### ContributionProgressCard — Complete Spec

**Purpose**: On the PersonalSavingsScreen GROUP_LINKED tab. Shows meeting attendance as a fraction and current cycle contribution total.

**Progress bar spec**:
- LinearProgressIndicator, Compose Material3 implementation
- height = 8dp (thicker than default for visibility)
- trackColor = primary_container (#A6F1A6)
- progressColor = primary (#2E7D32)
- cornerRadius = full (pill shape via Modifier.clip)
- progress value: meetingsAttended.toFloat() / totalMeetings.toFloat() = 18/24 = 0.75

**Meeting labels**:
- Above bar: "18 / 24 meetings" bodyMedium on_surface
- Below bar row: three columns
  - Start: "KES 100 min" — minimum per meeting
  - Centre: "This cycle: KES 9,600" — current total (bold)
  - End: "KES 500 max" — maximum per meeting

---

### LoanCard (Expandable) — Complete Spec

**Collapsed height**: approximately 120dp (varies with content)
**Expanded height**: collapsed + (repayment periods × 40dp) + divider (1dp) + header (24dp)

**Status chip styling**:
- All chips: cornerRadius full, padding 4dp × 10dp, labelMedium (12sp, weight 500)
- Active: background primary_container (#A6F1A6), text on_primary_container (#002106)
- Pending: background secondary_container (#FFDDB3), text on_secondary_container (#2A1700)
- Closed: background surface_variant (#DEE5DA), text on_surface_variant (#424942)
- Overdue: background error_container (#FFDAD6), text on_error_container (#410002)

**Expand animation**:
- AnimatedVisibility with expandVertically(animationSpec = tween(durationMillis=300))
- Chevron rotation: Animatable from 0f to 180f degrees, duration 200ms (short_4)
- Both animate simultaneously

**Repayment period row (expanded)**:
- Per period: Row(height=40dp, verticalAlignment=CenterVertically, padding horizontal 0dp)
- Period number "#1" width 24dp, labelMedium on_surface_variant
- Due date text weight=1f, bodyMedium on_surface
- Amount right-aligned, bodyLarge
  - Complete + paid: on_surface_variant (de-emphasised)
  - Pending: on_surface
  - Overdue: error (#D32F2F)
- Status icon (20dp) between date and amount:
  - checkmark_circle_24_filled primary — paid
  - circle_24_regular on_surface_variant — pending/upcoming
  - dismiss_circle_24_filled error — overdue/missed

---

### DurationSelector (Slider) — Complete Spec

**Slider behaviour**:
- M3 Slider composable with discrete steps
- Range: 4 to 52 (weeks), steps parameter = 12 (creates stops at: 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52 — 13 possible values)
- Default: 12 weeks
- Each step represents 4 weeks
- Value snaps to nearest step on drag release

**Repayment estimate recalculation**:
- Triggered on every slider value change (OnDurationChanged)
- Formula: repaymentEstimate = (principal + totalInterest) / durationWeeks
- Where totalInterest = principal × (interestRatePerPeriod / 100) × (termFrequency / 52)
- Example: principal=37,350, rate=2% per month, 12 weeks → repaymentEstimate = KES 3,223/week
- Displayed immediately (no loading state)

**Touch target**: Standard M3 Slider thumb = 20dp visual + 44dp touch area (meets 48dp with Track hitbox contribution)

---

### SubmitButton — Complete Spec

**Enabled condition**:
```kotlin
isFormValid = requestedAmount.isNotBlank()
    && requestedAmountError == null
    && requestedAmount.toDoubleOrNull() != null
    && requestedAmount.toDouble() > 0
    && requestedAmount.toDouble() <= maxLoanAmount
    && purpose != null
    && durationWeeks > 0
```

**Button states**:
1. Disabled: background = on_surface at 12% opacity, text = on_surface at 38% opacity
2. Enabled: background = primary (#2E7D32), text = on_primary (#FFFFFF)
3. Pressed: ripple on_primary at 20%, scale 0.97 over 50ms
4. Loading (isSubmitting=true): button hidden, spinner shown at same vertical position

**Submission flow**:
1. Tap → isSubmitting=true
2. All form fields: enabled=false (readOnly visual)
3. POST /datatables/dt_loan_request
4. On 200: successDialogVisible=true, isSubmitting=false
5. On network/503: if offline → SyncQueue → ShowOfflineQueuedConfirmation
6. On other error: submitError set, isSubmitting=false → snackbar appears

---

### SubmitSuccessDialog — Complete Spec

**Online mode dialog**:
- Icon: checkmark_circle_24_filled 48dp primary (#2E7D32)
- Title: "Request Submitted!" titleLarge on_surface
- Body: "Your loan request has been submitted. It will be reviewed by the group at the next meeting." bodyMedium on_surface_variant
- Button: "OK" — background primary, text on_primary, cornerRadius full, minHeight 48dp

**Offline mode dialog**:
- Icon: checkmark_circle_24_filled 48dp primary (#2E7D32)
- Title: "Request Saved!" titleLarge on_surface
- Body: "You are offline. Your loan request has been saved and will be submitted automatically when you reconnect." bodyMedium on_surface_variant
- Button: "OK" — same styling

**Dialog container**:
- Background: surface (#FAFAFA)
- Corner radius: 16dp
- Padding: 24dp
- Scrim: #000000 at 40%
- Elevation: 6dp (level_3)

---

## 4. Interaction Patterns

### Dashboard Data Loading — Full Flow

**Initial load sequence**:
1. PersonalDashboardViewModel initialised with clientId from nav_params
2. isLoading = true → DashboardShimmer visible (4 cards, each 100dp, animating shimmer gradient)
3. Shimmer gradient: sweeps left-to-right, base colour surface_variant, highlight colour surface
4. Parallel API calls launched (Kotlin coroutines):
   - GET /self/clients/{clientId}/accounts
   - GET /self/savingsaccounts/{groupLinkedSavingsId}
5. On all responses received:
   - isLoading = false
   - Shimmer fades out (200ms)
   - Cards fade in, staggered 50ms each:
     - GroupBanner (immediate — group name from session)
     - SavingsSummaryCard (from accounts response)
     - LoanSummaryCard or RequestLoanCta (based on activeLoan)
     - ShareOutProjectionCard
     - RecentActivityListItem × N (from last 5 transactions)
6. Analytics: `screen_viewed` event fired after content visible

**Offline load sequence**:
1. ConnectivityManager.isOnline() = false
2. isLoading = true
3. Load from SQLDelight:
   - SELECT * FROM savings_accounts WHERE client_id = ? LIMIT 1
   - SELECT * FROM loan_accounts WHERE client_id = ? AND status = 'ACTIVE' LIMIT 1
   - SELECT * FROM savings_transactions WHERE client_id = ? ORDER BY date DESC LIMIT 5
4. On cache hit: same display as online, plus offline badge "Cached" (surface_variant chip, top-right of SavingsSummaryCard)
5. On cache miss: error_state shown immediately (no data at all)

---

### Pull-to-Refresh — Full Flow

**Trigger**: User swipes down from top of LazyColumn.

**Step-by-step**:
1. User begins dragging down from y ≤ 10dp from top of list
2. SwipeRefresh threshold: 64dp drag → shows indicator
3. On release past threshold:
   - isRefreshing = true
   - CircularProgressIndicator (primary) animates into view at top
4. Parallel re-fetch: get_client_accounts + get_savings_account + recent transactions
5. On completion:
   - isRefreshing = false
   - Indicator fades out (150ms)
   - Updated data renders smoothly (DiffUtil-based list animation for transactions)
   - If data changed: cards update with crossfade animation (200ms)
   - If data unchanged: silent (no visual change)
6. Haptic: medium impact on refresh trigger

---

### Tab Switching (PersonalSavingsScreen) — Full Flow

**Trigger**: Tap Group-linked or Individual tab chip.

**Step-by-step**:
1. `OnTabSelected(SavingsTab.INDIVIDUAL)` dispatched
2. `selectedTab` updates to INDIVIDUAL
3. Tab chip animation:
   - Previously selected (GROUP_LINKED): background crossfade primary → primary_container (150ms)
   - Newly selected (INDIVIDUAL): background crossfade primary_container → primary (150ms)
4. Content below tabs:
   - BalanceHeroCard: balance text crossfades (amount changes: 9,600 → 2,850), duration 200ms
   - ContributionProgressCard: AnimatedVisibility(exit), duration 300ms
   - TransactionListItem list: new items fade in (staggered 50ms each, from alpha 0 → 1)
5. Analytics: `savings_tab_switched` event with tab=individual

**Individual tab absent scenario**:
- When individualSavingsId == null: Individual tab chip is not rendered
- Tab row shows only "Group-linked" chip with single-chip styling (no selected/unselected toggle)

---

### Loan Request Submission — Full Flow (Online)

**Pre-conditions**: isFormValid=true, isOfflineMode=false, isSubmitting=false

**Step-by-step**:
1. Tap SubmitButton
2. isSubmitting=true
3. SubmitButton fades out (150ms), SubmittingIndicator fades in (150ms)
4. All form fields: readOnly=true, alpha=0.6
5. POST /datatables/dt_loan_request called

**HTTP 200 response**:
6. isSubmitting=false
7. successDialogVisible=true (online copy)
8. Success dialog slides in from bottom (300ms, decelerated)
9. Analytics: `loan_request_success` event with mode=online, amount
10. User taps "OK"
11. OnSuccessDialogDismiss dispatched
12. Navigate to personal-dashboard
13. Dashboard auto-refreshes on return (OnRefresh dispatched on resume)

**HTTP 409 (duplicate request) response**:
6. isSubmitting=false
7. submitError = SubmitError.Validation
8. SubmitErrorSnackbar visible: "You already have a pending loan request."
9. SubmitButton returns (fade in 150ms)
10. Fields re-enabled

---

### Loan Request Submission — Full Flow (Offline)

**Pre-conditions**: isFormValid=true, isOfflineMode=true (ConnectivityManager.isOnline()=false)

**Step-by-step**:
1. OfflineModeBanner visible from start (user arrived on screen while offline)
2. User fills form normally (all fields function same as online)
3. Tap SubmitButton
4. isSubmitting=true → spinner shows
5. ConnectivityManager.isOnline() checked → false → offline branch
6. SyncQueueRepository.enqueue({
     entityType: "dt_loan_request",
     payload: LoanRequestPayload.toJson(),
     status: "PENDING",
     createdAt: ISO-8601 timestamp
   })
7. SyncQueueEntry saved to SQLDelight locally
8. isSubmitting=false
9. successDialogVisible=true (offline copy)
10. Dialog: "Request Saved! Your loan request has been saved and will be submitted automatically when you reconnect."
11. Analytics: `loan_request_success` event with mode=offline_queued
12. User taps "OK" → navigate to personal-dashboard
13. When device reconnects: SyncQueueWorker processes queue → POST /datatables/dt_loan_request
14. On sync success: SyncQueueEntry status → "SYNCED"
15. On sync failure: retryCount++ (max 5 retries, exponential backoff)

---

### Filter Chip Selection (PersonalLoansScreen)

**Trigger**: Tap "All", "Active", or "Closed" chip.

**Step-by-step**:
1. `OnFilterChange(LoanStatusFilter.ACTIVE)` dispatched
2. filterStatus = ACTIVE
3. Previously selected chip (ALL): background crossfades primary → surface (150ms)
4. Newly selected (ACTIVE): border hidden, background crossfades surface → primary (150ms)
5. Loan list filters immediately (no loading state):
   - loans.filter { it.status.active } displayed
   - Closed/pending loans removed with itemAnimator fadeOut (150ms)
   - Active loans remain/animate to new positions
6. If no loans match filter: empty state variant shows "No active loans" (adapts title based on filter)

---

### Overdue Loan Highlight Behaviour

When `loan.isOverdue == true`:

1. LoanCard header: StatusChip shows "Overdue" (errorContainer background)
2. Next repayment amount: text colour changes to error (#D32F2F)
3. Next repayment row prefix: warning_24_filled 16dp error icon prepended
4. RepaymentPeriodRow (expanded): overdue periods show dismiss_circle_24_filled error icon + amount in error colour
5. Dashboard LoanSummaryCard: same overdue treatment in the card preview

---

## 5. Content Data

### Real Member Data — Grace Mwangi (Primary Test User)

**Member profile**:
- Name: Grace Mwangi
- Client ID: 2081
- Username: grace.mwangi
- Group: Mwangaza Women's Group
- Group ID (Fineract Center): 401
- Member since: 4 January 2026 (Cycle 3 start)
- Role: General Member
- Meeting attendance: 18 of 24 (this cycle up to May 2026)

**Savings accounts**:
- Group-linked savings account:
  - Account ID: 30042
  - Account No: 000100030042
  - Product: Mwangaza Group Savings
  - Balance: KES 9,600 (18 meetings × KES 500 min / some meetings = variable)
  - Total deposits this cycle: KES 9,600
  - Total withdrawals: KES 0

- Individual savings account:
  - Account ID: 30043
  - Account No: 000100030043
  - Product: Personal Voluntary Savings
  - Balance: KES 2,850
  - Total deposits: KES 3,100
  - Total withdrawals: KES 250

**Combined savings**: KES 12,450 (displayed on dashboard)

**Recent transactions** (last 5):
| Date | Type | Amount | Running Balance | Account |
|------|------|--------|----------------|---------|
| 30 Apr 2026 | Meeting contribution | +KES 500 | KES 9,600 | Group-linked |
| 25 Apr 2026 | Deposit | +KES 200 | KES 2,850 | Individual |
| 16 Apr 2026 | Meeting contribution | +KES 500 | KES 9,100 | Group-linked |
| 10 Apr 2026 | Withdrawal | -KES 250 | KES 2,650 | Individual |
| 3 Apr 2026 | Meeting contribution | +KES 500 | KES 8,600 | Group-linked |

**Active loan** (none — Grace has no current active loan):
- activeLoan = null → RequestLoanCta shown on dashboard

**Share-out projection**:
- Total group corpus: KES 450,000 (18 members' savings + cycle profit)
- Grace's savings ratio: 12,450 / 225,000 (total group savings) = 5.53%
- Projected share-out: 5.53% × 450,000 = KES 24,900 (conservative)
- With profit: KES 38,250 (includes interest from group loans)

**Loan multiplier**: 3.0 (from dt_group_config)
**Max eligible loan**: 12,450 × 3 = KES 37,350

---

### Real Member Data — Amara Diallo (Secondary Test User — Has Active Loan)

**Member profile**:
- Name: Amara Diallo
- Client ID: 2082
- Group: Mwangaza Women's Group
- Savings balance: KES 10,200
- Active loan: KES 15,000 at 2% per month

**Active loan details**:
- Loan ID: 5001
- Account No: 000100005001
- Product: Group Loan Facility
- Principal: KES 15,000
- Disbursed: 5 March 2026
- Term: 12 weeks
- Interest rate: 2% per month
- Total outstanding: KES 15,300
- Status: Active (on-track)
- Next repayment: KES 1,500, due 5 June 2026
- isOverdue: false

**Repayment schedule** (12 weekly periods):
| # | Due Date | Total Due | Paid | Complete |
|---|---------|----------|------|---------|
| 1 | 12 Mar 2026 | KES 1,275 | KES 1,275 | true |
| 2 | 19 Mar 2026 | KES 1,275 | KES 1,275 | true |
| 3 | 26 Mar 2026 | KES 1,275 | KES 1,275 | true |
| 4 | 2 Apr 2026 | KES 1,275 | KES 1,275 | true |
| 5 | 9 Apr 2026 | KES 1,275 | KES 1,275 | true |
| 6 | 16 Apr 2026 | KES 1,275 | KES 1,275 | true |
| 7 | 23 Apr 2026 | KES 1,275 | KES 1,275 | true |
| 8 | 30 Apr 2026 | KES 1,275 | KES 1,275 | true |
| 9 | 7 May 2026 | KES 1,275 | KES 1,275 | true |
| 10 | 14 May 2026 | KES 1,275 | KES 1,275 | true |
| 11 | 21 May 2026 | KES 1,275 | KES 0 | false (upcoming) |
| 12 | 28 May 2026 | KES 1,275 | KES 0 | false (upcoming) |

**Overdue scenario** (for testing overdue state):
- Modify period 11 dueDate to 1 May 2026 (past today)
- isOverdue = true
- LoanCard: "Overdue" chip, red next repayment text, warning icon

---

### Loan Request Form — Sample Data Entry

**User**: Grace Mwangi (clientId=2081, savingsBalance=12,450)

**Filled form**:
- Loan Amount: "15000" → displays "KES 15,000"
- Max validation: 15,000 ≤ 37,350 → valid, no error
- Purpose: "School Fees" (SCHOOL_FEES)
- Duration: 12 weeks (slider default)
- Repayment estimate: KES 15,000 / 12 = KES 1,250/week base + 2% monthly interest ≈ KES 1,300/week

**Repayment summary card**:
- Principal: KES 15,000
- Interest (group rate): KES 300 (2% × 1 month × 15,000 / approximate 12-week term)
- Total to repay: KES 15,300

**Over-limit scenario**:
- Amount entered: "40000"
- requestedAmountError: "Maximum loan is KES 37,350"
- Field border turns error (#D32F2F), supporting text shows error
- SubmitButton remains disabled

**Purpose dropdown open state**:
- Dropdown height: up to 280dp (5 options visible, scroll for rest)
- Each option row: height 48dp, bodyLarge on_surface
- Hover/focus: surface_variant (#DEE5DA) background
- Selected: primary_container (#A6F1A6) background, checkmark_24_filled primary at end

---

### Analytics Events — Sample Payloads

**savings_card_tapped**:
```json
{
  "event": "savings_card_tapped",
  "savings_balance": 12450.0,
  "client_id": 2081,
  "screen_id": "personal-dashboard",
  "timestamp": "2026-05-06T10:22:11Z"
}
```

**loan_expanded** (Amara Diallo):
```json
{
  "event": "loan_expanded",
  "loan_id": 5001,
  "status": "Active",
  "client_id": 2082,
  "timestamp": "2026-05-06T10:25:33Z"
}
```

**loan_request_submitted** (Grace Mwangi):
```json
{
  "event": "loan_request_submitted",
  "amount": 15000.0,
  "purpose": "SCHOOL_FEES",
  "duration_weeks": 12,
  "is_offline": false,
  "client_id": 2081,
  "timestamp": "2026-05-06T10:28:07Z"
}
```

**loan_request_success** (offline queued scenario):
```json
{
  "event": "loan_request_success",
  "mode": "offline_queued",
  "amount": 15000.0,
  "client_id": 2081,
  "timestamp": "2026-05-06T10:28:08Z"
}
```

---

## 6. Responsive Rules

### Compact (0–599dp width) — Primary Target

**PersonalDashboardScreen**:
- All cards: full-width minus 16dp margin each side → width = screenWidth - 32dp
- SavingsSummaryCard overlap: -20dp (fixed, regardless of screen width)
- LazyColumn with standard item spacing
- Bottom nav: 80dp height, 3 items
- FAB (on loans screen): end-bottom, 16dp margins

**PersonalSavingsScreen**:
- Tab row: fills full width; tab chips expand to fill (SpaceEvenly arrangement)
- BalanceHeroCard: full width minus 32dp
- ContributionProgressCard: full width minus 32dp
- Transaction list: full width with 16dp horizontal padding

**PersonalLoansScreen**:
- Filter chips: horizontal scroll (no wrap) — keeps chips in single row
- Loan cards: full width minus 32dp
- FAB: extended (icon + text), anchored bottom-end

**LoanRequestScreen**:
- All form elements: full width minus 32dp
- Duration slider: full width (fills content area)
- Submit button: full width minus 32dp, pill shape

---

### Medium (600–839dp width) — Foldables, Small Tablets

**PersonalDashboardScreen**:
- Cards: max-width 560dp, centred with auto horizontal margins
- Top bar: wider; group name can show fully without truncation
- GroupBanner chip moves to end of group name row without wrapping
- Bottom nav: same structure, wider items

**PersonalSavingsScreen**:
- BalanceHeroCard: max-width 560dp, centred
- ContributionProgressCard: max-width 560dp, centred
- Transaction list rows: max-width 560dp, centred

**PersonalLoansScreen**:
- Loan cards: max-width 560dp, centred
- Filter chips no longer need horizontal scroll (all 3 fit comfortably)

**LoanRequestScreen**:
- Form elements: max-width 560dp, centred
- Duration selector: max-width 560dp, centred (slider wider = easier adjustment)

---

### Expanded (≥840dp width) — Tablets and Landscape

**PersonalDashboardScreen**:
- Two-column layout: sidebar (left, 280dp) + content (right, remaining)
- Sidebar (NavigationRail):
  - background: surface_variant (#DEE5DA)
  - Items: Dashboard (home), Savings, Loans
  - Selected indicator: primary_container pill
  - Width: 80dp (icons only) or 280dp (with labels)
- Content column:
  - Max-width: 640dp, centred within right pane
  - No bottom navigation bar (replaced by NavigationRail)
  - Full content cards with wider layouts

**PersonalSavingsScreen (expanded)**:
- Two-column content area:
  - Left column (50%): BalanceHeroCard + ContributionProgressCard
  - Right column (50%): Transaction history (LazyColumn)
- Tab row spans full width above both columns

**PersonalLoansScreen (expanded)**:
- Main content max-width: 640dp
- Loan cards: expanded to 560dp wide (more comfortable repayment schedule view)
- FAB: optional — can be NavigationRail action item instead

**LoanRequestScreen (expanded)**:
- Two-column form layout:
  - Left (50%): Amount field + Purpose dropdown
  - Right (50%): Duration selector + Repayment summary
- SavingsLimitCard: full width spanning both columns
- Submit button: centred, max-width 400dp

---

### Orientation — Portrait vs Landscape

**Portrait (standard)**:
- All layouts as described in component trees above

**Landscape compact** (phone rotated):
- PersonalDashboardScreen: GroupBanner collapses to minimal height (no padding expansion)
- SavingsSummaryCard: -20dp overlap maintained; card height unchanged
- LazyColumn scrolls horizontally-compressed content
- Bottom nav: hidden in compact landscape (use gesture navigation instead)

**Landscape expanded** (tablet landscape):
- Same as expanded portrait (two-column layout already handles landscape)
- NavigationRail visible on left

---

### Bottom Navigation Bar Spec

Applies to PersonalDashboardScreen, PersonalSavingsScreen, PersonalLoansScreen (bottom_nav: true).
NOT shown on LoanRequestScreen (bottom_nav: false).

**Spec**:
- Height: 80dp (including safe area padding)
- Background: surface (#FAFAFA)
- Elevation: 3dp (level_2)
- Items: 3 items (Dashboard, Savings, Loans)
- Item width: equal thirds of screen width
- Selected indicator: primary_container (#A6F1A6) pill behind icon, cornerRadius full
- Selected icon colour: on_secondary_container (#2A1700)... actually on primary: on_primary_container (#002106)
- Unselected icon colour: on_surface_variant (#424942)
- Item labels: labelMedium (12sp, weight 500), colour matching icon
- Icon size: 24dp
- Transition: icon cross-fades, indicator expands from centre (duration 200ms, short_4)

**Navigation items**:
| Item | Icon | Selected Route |
|------|------|---------------|
| Dashboard | home_24_regular / home_24_filled | /dashboard |
| Savings | savings_24_regular / savings_24_filled | /savings |
| Loans | money_24_regular / money_24_filled | /loans |
