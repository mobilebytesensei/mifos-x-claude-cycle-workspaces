# PROMPTS_STITCH — corpus-tracking
# MifosSave (mifos-x-group-banking) | Feature FR-018
# Generated: 2026-05-06
# Sections: 6 | Total lines: ≥1,200

---

## SECTION 1 — Design System Context

### 1.1 Brand Purpose for Corpus Tracking

The corpus fund is the soul of MifosSave. For the Mwangaza Women's Group, the corpus (derived from Latin "body") represents the group's collective financial body — the total pooled capital that grows through savings, shrinks through loans, and is distributed at cycle end through share-out. FR-018 mandates that this critical number be visible, accurate, and actionable throughout the app.

Design principles for corpus-tracking:
- **Prominence:** The KES balance must be the single most visually prominent number on the GroupDashboard — using displaySmall (36sp) in primary green, impossible to miss.
- **Trust:** The balance is sourced from network-first (60s TTL) to ensure accuracy. Stale data is always disclosed.
- **Safety:** The corpus gate is a hard financial safeguard. Its visual design must be instantly comprehensible — error red, not just a warning.
- **Live feedback:** During meetings, the corpus updates with every tap. The CorpusBand is persistent, real-time, and positioned where the eye naturally tracks during data entry.

### 1.2 Color System — Complete Specification

**Primary — VSLA-green (Corpus Sufficient State):**
- primary: #2E7D32
- on_primary: #FFFFFF
- primary_container: #A6F1A6 (group dashboard header background)
- on_primary_container: #002106

Corpus balance display: primary #2E7D32 (displaySmall 36sp) — green = money growing = trust

**Secondary — Amber (Corpus Warning, Near-Threshold):**
- secondary: #FF8F00
- on_secondary: #FFFFFF
- secondary_container: #FFDDB3 (CorpusBand warning state when projected corpus drops low)
- on_secondary_container: #2A1700

**Tertiary — Trust-blue (Normal CorpusBand, Informational Stats):**
- tertiary: #1565C0
- on_tertiary: #FFFFFF
- tertiary_container: #D2E4FF (CorpusBand background on steps 2-6)
- on_tertiary_container: #001C39

Corpus band: tertiary_container #D2E4FF — blue conveys informational/monitoring role, not alarm

**Error — Corpus Blocked (Critical, Financial Stop):**
- error: #D32F2F (corpus amount text when isCorpusInsufficient=true)
- on_error: #FFFFFF
- error_container: #FFDAD6 (block banner inside corpus card; corpus gate snackbar)
- on_error_container: #410002 (text on block banner)

Corpus card border: 2dp solid error #D32F2F when isCorpusInsufficient=true; transparent when sufficient

**Surface:**
- background: #FFFFFF
- on_background: #1A1C19
- surface: #FAFAFA (card backgrounds)
- on_surface: #1A1C19
- surface_variant: #DEE5DA (sub-stat backgrounds, shimmer skeleton)
- on_surface_variant: #424942 (section labels, stat labels)
- outline: #727971
- outline_variant: #C2C9BD

**Dark theme equivalents:**
- primary dark: #8BD68F
- primary_container dark: #00531A
- tertiary dark: #9FCAFF
- tertiary_container dark: #004A82
- error dark: #FFB4AB
- error_container dark: #93000A
- surface dark: #121412

### 1.3 Typography — Complete Scale

Font: Noto Sans (all weights)
Scale: large (rural-optimized)

| Role | sp | Line Height | Weight | Corpus Usage |
|------|----|-------------|--------|-------------|
| displayLarge | 57 | 64 | 400 | Not used |
| displayMedium | 45 | 52 | 400 | Not used |
| displaySmall | 36 | 44 | 400 | **Corpus balance KES amount** — primary headline number |
| headlineLarge | 32 | 40 | 400 | Not used |
| headlineMedium | 28 | 36 | 400 | Not used |
| headlineSmall | 24 | 32 | 400 | Group name in header |
| titleLarge | 22 | 28 | 500 | TopBar group name |
| titleMedium | 16 | 24 | 500 | "Corpus Fund" card label; savings summary total |
| titleSmall | 14 | 20 | 500 | "Quick Actions" section label; activity header |
| bodyLarge | 16 | 24 | 400 | Activity item descriptions |
| bodyMedium | 14 | 20 | 400 | Cycle info text; block banner text |
| bodySmall | 12 | 16 | 400 | Activity dates; supporting text |
| labelLarge | 14 | 20 | 500 | CorpusBand "Corpus: KES X"; stat labels |
| labelMedium | 12 | 16 | 500 | CorpusBand "Cash on Hand: KES Y"; stat values |
| labelSmall | 11 | 16 | 500 | Quick action button labels; chip text |

Corpus balance: displaySmall 36sp + Noto Sans bold (weight 700) for emphasis. This is the only element on GroupDashboard at this scale.

### 1.4 Spacing Scale (dp)

- xxs: 2dp
- xs: 4dp — chip padding
- sm: 8dp — gap between stat items in corpus card
- md: 12dp — card internal section gaps
- lg: 16dp — standard horizontal padding; card padding-horizontal
- xl: 20dp — corpus card internal padding
- xxl: 24dp — not used
- 3xl: 48dp — empty state padding
- 4xl: 64dp — error state icon size

Cards vertical margin: 8dp between cards on dashboard.
Quick action grid: 2×2, gap 12dp between buttons.

### 1.5 Shape Tokens

| Name | dp | Usage |
|------|----|-------|
| none | 0dp | flat dividers, CorpusBand (edge-to-edge) |
| extra_small | 4dp | small chips |
| small | 8dp | CorpusGateChip corner |
| medium | 12dp | SavingsSummaryCard, ActivityCard |
| large | 16dp | CorpusCard, QuickActionsCard, GroupHeaderCard |
| extra_large | 28dp | modal dialogs |
| full | 9999dp | status chips, corpus gate chip |

### 1.6 Elevation Levels

| Level | dp | Tonal | Usage |
|-------|-----|-------|-------|
| level_0 | 0dp | 0.00 | Group header card (zero elevation, embedded look) |
| level_1 | 1dp | 0.05 | Not used in corpus-tracking |
| level_2 | 3dp | 0.08 | QuickActions, SavingsSummary, Activity cards |
| level_3 | 6dp | 0.11 | Not used |
| level_4 | 8dp | 0.12 | CorpusCard (most elevated — highest priority content) |
| level_5 | 12dp | 0.14 | Not used |

CorpusCard: elevation level_4 (8dp) intentional — the most physically prominent card on the screen. Tonal elevation adds primary-tinted surface for extra visual weight.

### 1.7 Motion System

- short_2: 100ms — CorpusBand text crossfade on each value update
- short_3: 150ms — chip state color transitions
- short_4: 200ms — CorpusBand entry slide-down; corpus card border color transition (sufficient→insufficient)
- medium_1: 250ms — shimmer overlay fade-out when content loads
- medium_2: 300ms — corpus gate snackbar slide-up; error banner slide-down
- medium_3: 350ms — screen entry from group-list (slide from right)
- medium_4: 400ms — counter animation for corpus balance count-up on screen entry
- long_1: 450ms — full parallel data load completion fade-in
- long_2: 500ms — total dashboard animation time

Easing:
- standard: cubic-bezier(0.2, 0.0, 0, 1.0) — CorpusBand updates, chip transitions
- emphasized: cubic-bezier(0.2, 0.0, 0, 1.0) — corpus card entry
- decelerated: cubic-bezier(0.0, 0.0, 0, 1.0) — snackbar slide-up, CorpusBand entry
- accelerated: cubic-bezier(0.3, 0.0, 1.0, 1.0) — CorpusBand exit on step 1←2

### 1.8 Corpus Card — State Design Tokens Summary

| State | Border | KES Amount Color | Banner |
|-------|--------|-----------------|--------|
| Sufficient | transparent (0dp) | primary #2E7D32 | hidden |
| Insufficient | 2dp error #D32F2F | error #D32F2F | error_container visible |
| Loading | outline_variant #C2C9BD | shimmer | none |
| Offline/stale | transparent | primary #2E7D32 | "Data as of Meeting #3" chip |

### 1.9 Accessibility Standards

- Corpus amount: announced by TalkBack when screen loads (role: none, but parent card has content_description)
- Corpus block state: additional announcement "Warning: Loan disbursement is blocked" via AccessibilityEvent
- CorpusBand: content_description updates on each value change → ANNOUNCEMENT for live region
- All card content_descriptions written in complete sentences for screen reader comprehensibility
- Min touch target: 48dp all quick action buttons; quick action buttons in grid are 56dp min for easy tap
- Focus ring: 3dp primary #2E7D32
- Color alone never used: block state includes "BLOCKED" text label + warning icon in addition to red

---

## SECTION 2 — Screen Layouts

### 2.1 GroupDashboardScreen — Full Component Tree

```
GroupDashboardScreen
├── TopBar (height: 56dp)
│   ├── background: primary #2E7D32
│   ├── text_color: on_primary #FFFFFF
│   ├── NavigationIcon: FluentIcons.arrow_left_24_regular → OnBack
│   │   ├── tint: on_primary
│   │   └── min_touch_target: 48dp
│   ├── Title: "Mwangaza Women's Group" (titleLarge 22sp, on_primary)
│   └── Actions:
│       └── IconButton (more_vert, 24dp, on_primary, min: 48dp) → OnMoreOptions
├── LazyColumn (fillMaxSize, top: TopBar, bottom: BottomNav)
│   ├── Item: GroupHeaderCard
│   │   ├── background: primary_container #A6F1A6
│   │   ├── elevation: level_0 (0dp) — embedded in scroll
│   │   ├── corner_radius: 0dp (edge-to-edge, no gaps at top)
│   │   ├── padding: 16dp
│   │   ├── Text "Mwangaza Women's Group" (headlineSmall 24sp, on_primary_container #002106)
│   │   ├── Text "Cycle 1 of 12 months • Weekly meetings" (bodyMedium 14sp, on_primary_container, mt: 4dp)
│   │   └── Row (mt: 8dp, gap: 8dp):
│   │       ├── AssistChip "5 members" (background: secondary_container #FFDDB3, on_secondary_container)
│   │       └── AssistChip "0 overdue" (background: surface_variant #DEE5DA, on_surface_variant)
│   │           └── if overdueLoansCount > 0: background error_container #FFDAD6, on_error_container
│   ├── Item: CorpusCard (margin: 16dp horizontal, 8dp vertical)
│   │   ├── background: surface #FAFAFA
│   │   ├── elevation: level_4 (8dp) — most prominent card
│   │   ├── corner_radius: 16dp (large)
│   │   ├── padding: 20dp
│   │   ├── border: (when isCorpusInsufficient) 2dp error #D32F2F / otherwise: none
│   │   ├── Text "Corpus Fund" (titleMedium 16sp, on_surface #1A1C19)
│   │   ├── Text "KES 47,500" (displaySmall 36sp bold, color: primary #2E7D32 when sufficient / error #D32F2F when insufficient)
│   │   ├── CorpusBlockBanner (visible_when: isCorpusInsufficient)
│   │   │   ├── background: error_container #FFDAD6
│   │   │   ├── corner_radius: 8dp; padding: 12dp; margin_top: 8dp
│   │   │   ├── Row:
│   │   │   │   ├── Icon(warning_24_regular, 20dp, error #D32F2F)
│   │   │   │   └── Text "Loan disbursement is blocked — corpus balance is below minimum threshold." (bodyMedium, on_error_container #410002, ml: 8dp)
│   │   │   └── content_description: "Warning: Loan disbursement is blocked. Corpus KES 800 is below minimum KES 5,000."
│   │   ├── Row (mt: 16dp, horizontalArrangement: SpaceEvenly)
│   │   │   ├── StatColumn:
│   │   │   │   ├── Text "Opening Balance" (labelSmall 11sp, on_surface_variant)
│   │   │   │   └── Text "KES 0" (labelMedium 12sp, on_surface #1A1C19)
│   │   │   ├── VerticalDivider (1dp, outline_variant, height: 36dp)
│   │   │   ├── StatColumn:
│   │   │   │   ├── Text "Contributions" (labelSmall, on_surface_variant)
│   │   │   │   └── Text "KES 52,500" (labelMedium, on_surface)
│   │   │   ├── VerticalDivider (1dp, outline_variant)
│   │   │   └── StatColumn:
│   │   │       ├── Text "Loans Out" (labelSmall, on_surface_variant)
│   │   │       └── Text "KES 5,000" (labelMedium, on_surface)
│   │   └── content_description: "Corpus Fund KES 47,500. Opening Balance KES 0; Contributions this cycle KES 52,500; Loans outstanding KES 5,000."
│   ├── Item: QuickActionsCard (margin: 16dp horizontal, 8dp vertical)
│   │   ├── background: surface #FAFAFA
│   │   ├── elevation: level_2 (3dp)
│   │   ├── corner_radius: 16dp; padding: 16dp
│   │   ├── Text "Quick Actions" (titleSmall 14sp, on_surface_variant #424942)
│   │   └── 2×2 Grid (columns: 2, gap: 12dp, mt: 12dp):
│   │       ├── FilledButton "Start Meeting"
│   │       │   ├── icon: meeting_room (24dp)
│   │       │   ├── background: primary #2E7D32; text: on_primary; min: 56dp × 56dp
│   │       │   ├── onClick → OnStartMeeting → NavigateToMeetingCalendar
│   │       │   └── content_description: "Start a new group meeting"
│   │       ├── OutlinedButton "Members"
│   │       │   ├── icon: group (24dp)
│   │       │   ├── border: 1dp primary; text: primary; min: 56dp × 56dp
│   │       │   ├── onClick → OnViewMembers → NavigateToMemberList
│   │       │   └── content_description: "View all group members"
│   │       ├── OutlinedButton "Loans"
│   │       │   ├── icon: account_balance (24dp)
│   │       │   ├── border: 1dp primary; text: primary; min: 56dp × 56dp
│   │       │   ├── onClick → OnViewLoans → NavigateToLoanList
│   │       │   └── content_description: "View all group loans"
│   │       └── OutlinedButton "Share-Out"
│   │           ├── icon: share (24dp)
│   │           ├── enabled: isCycleEnd (= false in demo)
│   │           ├── enabled state: border 1dp secondary #FF8F00; text secondary; min: 56dp × 56dp
│   │           ├── disabled state: border 1dp outline_variant; text on_surface_variant; opacity 38%
│   │           ├── onClick (when enabled) → OnShareOut → NavigateToShareOut
│   │           └── content_description: "Distribute share-out at end of cycle" (disabled: "Share-Out available only at end of cycle")
│   ├── Item: SavingsSummaryCard (margin: 16dp horizontal, 8dp vertical)
│   │   ├── background: surface #FAFAFA; elevation: level_2; corner: 16dp; padding: 16dp
│   │   ├── Text "Savings Summary" (titleMedium 16sp, on_surface)
│   │   ├── Text "Mandatory contribution: KES 100 – KES 500 per meeting" (bodyMedium 14sp, on_surface_variant, mt: 4dp)
│   │   └── Text "KES 52,500 total" (titleLarge 22sp, tertiary #1565C0, mt: 8dp)
│   └── Item: ActivityFeedCard (margin: 16dp horizontal, 8dp vertical, mb: 16dp)
│       ├── background: surface; elevation: level_2; corner: 16dp; padding: 16dp
│       ├── Text "Recent Activity" (titleMedium, on_surface)
│       └── LazyColumn of ActivityListItem (max 5 items, min_touch_target: 56dp)
│           ├── Leading: activity type icon (24dp)
│           │   ├── MEETING: calendar icon, tint primary
│           │   ├── DEPOSIT: arrow_up_circle, tint primary
│           │   ├── LOAN: money, tint tertiary
│           │   ├── PENALTY: warning, tint secondary
│           │   └── SHARE_OUT: share, tint tertiary
│           ├── Content:
│           │   ├── Headline: activity.description (bodyLarge, on_surface)
│           │   └── Supporting: "${activity.date} • ${activity.memberName}" (bodySmall, on_surface_variant)
│           └── Trailing: Text "${activity.amount | KES}" (labelLarge, primary) if amount != null
├── ShimmerDashboard (visible_when: isLoading)
│   ├── 4 shimmer blocks; height: 120dp each; corner: 16dp; bg: surface_variant
│   └── shimmer gradient: surface_variant → outline_variant → surface_variant, 1200ms
└── ErrorState (visible_when: error != null)
    ├── Icon cloud_off (64dp, on_surface_variant, centered)
    ├── Text "Could not load group" (headlineSmall, centered)
    ├── Text error.message (bodyMedium, on_surface_variant, centered)
    └── FilledButton "Retry" (primary, mt: 16dp) → Retry
```

### 2.2 CorpusBand — Full Component Tree (in MeetingConductScreen)

```
CorpusBand
├── visible_when: currentStep >= 2
├── Row(
│     modifier: fillMaxWidth,
│     horizontalArrangement: SpaceBetween,
│     verticalAlignment: CenterVertically
│   )
│   ├── Text (start-aligned):
│   │   ├── content: "Corpus: KES ${displayCorpus}"
│   │   ├── style: labelLarge 14sp, weight 500
│   │   └── color: on_tertiary_container #001C39 (normal) / on_secondary_container #2A1700 (warning)
│   └── Text (end-aligned):
│       ├── content: "Cash on Hand: KES ${cashOnHand}"
│       ├── style: labelMedium 12sp, weight 500
│       └── color: on_tertiary_container (normal) / on_secondary_container (warning)
├── background: tertiary_container #D2E4FF (normal) / secondary_container #FFDDB3 (when isCorpusWarning)
├── height: 40dp
├── padding_horizontal: 16dp
├── padding_vertical: 8dp
└── content_description: "Group corpus fund KES ${displayCorpus}, cash on hand KES ${cashOnHand}"
```

**CorpusBand entry animation:**
- On step advance 1→2: slideInVertically from -40dp (band height), 200ms, decelerated easing
- On step advance 2→1 (back): slideOutVertically to -40dp, 150ms, accelerated easing

**CorpusBand value update:**
- displayCorpus value changes: text crossfades 100ms (old text fades out, new text fades in)
- The crossfade is visible because the KES amounts can change dramatically (thousands of KES)

### 2.3 CorpusGateChip — Full Component Tree (Step 5)

```
CorpusGateChip (visible_when: totalLoansDisbursed > 0 OR pendingLoanApplications.isNotEmpty())
├── AssistChip
│   ├── text: "Available to disburse: KES ${availableForDisbursal}"
│   ├── background: tertiary_container #D2E4FF
│   ├── text_color: on_tertiary_container #001C39
│   ├── corner: full (9999dp)
│   ├── padding: labelSmall 11sp
│   ├── margin_bottom: 12dp
│   └── content_description: "Available corpus for loan disbursement: KES ${availableForDisbursal}"
└── animation: text crossfades 100ms on value change (same as CorpusBand)
```

---

## SECTION 3 — Component Specifications

### 3.1 CorpusCard

**Component name:** CorpusCard
**Props:**
| Prop | Type | Required |
|------|------|----------|
| currentBalance | Double | yes |
| openingBalance | Double | yes |
| totalContributionsThisCycle | Double | yes |
| totalLoansOutstanding | Double | yes |
| isCorpusInsufficient | Boolean | yes |
| minimumDisbursementThreshold | Double | yes |

**Visual spec:**
- Card: surface #FAFAFA, elevation level_4 (8dp), corner 16dp, padding 20dp
- Border: Modifier.border(2.dp, MaterialTheme.colorScheme.error, RoundedCornerShape(16.dp)) — applied ONLY when isCorpusInsufficient=true

**Corpus amount display:**
- Text: "KES ${currentBalance.toLong() | formattedNumber}" e.g. "KES 47,500"
- Style: displaySmall 36sp, weight 700 (bold)
- Color: primary #2E7D32 when sufficient; error #D32F2F when insufficient
- Color animation: animateColorAsState with 200ms tween when isCorpusInsufficient changes

**Entry animation:**
- On screen enter: CountingNumber animation for balance
  - animateFloatAsState from 0f to currentBalance.toFloat(), 400ms, FastOutSlowInEasing
  - displayed as "KES ${animatedValue.roundToLong() | formattedNumber}"

**CorpusBlockBanner (inside card, visible_when: isCorpusInsufficient):**
- AnimatedVisibility with expandVertically + fadeIn on appear (200ms)
- AnimatedVisibility with shrinkVertically + fadeOut on dismiss (150ms)
- Layout:
```
Row(verticalAlignment: CenterVertically, padding: 12dp):
  Icon(warning_24_regular, 20dp, MaterialTheme.colorScheme.error)
  Text(
    "Loan disbursement is blocked — corpus balance is below minimum threshold.",
    bodyMedium 14sp,
    on_error_container #410002,
    ml: 8dp
  )
```

**Sub-stats row:**
- 3 StatColumn items separated by VerticalDividers
- StatColumn layout: Text(label, labelSmall, on_surface_variant) + Text(value, labelMedium, on_surface)
- Values formatted with thousand separators: 52500 → "52,500"

**Variants:**
- Sufficient (default): standard green amount, no border, no banner
- Insufficient: red border + red amount + error banner
- Loading: entire card is a shimmer block (120dp height, 16dp corner)
- Offline: stale corpus + subtle "As of Meeting #3" labelSmall chip below amount

---

### 3.2 QuickActionsGrid

**Component name:** QuickActionsGrid
**Props:**
| Prop | Type | Required |
|------|------|----------|
| isCorpusInsufficient | Boolean | yes |
| isCycleEnd | Boolean | yes |
| onStartMeeting | () -> Unit | yes |
| onViewMembers | () -> Unit | yes |
| onViewLoans | () -> Unit | yes |
| onShareOut | () -> Unit | yes |

**Visual spec:**
- 2×2 grid with uniformGap: 12dp
- All buttons: min height 56dp, min width = (screen_width - 32dp padding - 12dp gap) / 2

**Start Meeting button:**
- Variant: FilledButton
- background: primary #2E7D32
- text: on_primary #FFFFFF
- icon: meeting_room (24dp, on_primary)
- Always enabled (meeting can start even when corpus insufficient — FR-018 blocks disbursement, not meeting start)

**Members button:**
- Variant: OutlinedButton
- border: 1dp primary #2E7D32
- text: primary #2E7D32
- icon: group (24dp, primary)
- Always enabled

**Loans button:**
- Variant: OutlinedButton
- border: 1dp primary #2E7D32
- text: primary #2E7D32
- icon: account_balance (24dp, primary)
- Always enabled

**Share-Out button:**
- Variant: OutlinedButton
- When isCycleEnd=true: border 1dp secondary #FF8F00, text secondary, icon secondary — enabled
- When isCycleEnd=false: border 1dp outline_variant #C2C9BD, text on_surface_variant, icon on_surface_variant — disabled (38% opacity)
- Long-press when disabled: tooltip "Share-Out available at end of 12-month cycle" (2000ms, surface_variant bubble)

---

### 3.3 ActivityListItem

**Component name:** ActivityListItem
**Props:**
| Prop | Type | Required |
|------|------|----------|
| activity | ActivityItem | yes |

**Visual spec:**
- min_height: 56dp (non-interactive — no ripple)
- divider: 1dp outline_variant, start indent: 56dp

**Layout:**
```
ListItem(
  leadingContent: {
    Icon(
      imageVector = activityTypeIcon(activity.type),
      contentDescription = null,
      tint = activityTypeTint(activity.type),
      size = 24dp
    )
  },
  headlineContent: { Text(activity.description, bodyLarge) },
  supportingContent: { Text("${activity.date} • ${activity.memberName ?: ''}", bodySmall, on_surface_variant) },
  trailingContent: {
    if (activity.amount != null) Text("KES ${activity.amount.toLong() | formattedNumber}", labelLarge, primary)
  }
)
```

**Icon mapping:**
- MEETING: calendar_month_24_regular, primary #2E7D32
- DEPOSIT: arrow_circle_up_24_regular, primary #2E7D32
- LOAN: account_balance_24_regular, tertiary #1565C0
- PENALTY: warning_24_regular, secondary #FF8F00
- SHARE_OUT: share_24_regular, tertiary #1565C0

---

### 3.4 CorpusBand Component

**Component name:** CorpusBand (composable within MeetingConductScreen)
**Props:**
| Prop | Type | Required |
|------|------|----------|
| openingCorpus | Long | yes |
| runningSavingsTotal | Long | yes |
| totalRepayments | Long | yes |
| totalFinesCollected | Long | yes |
| totalLoansDisbursed | Long | yes |
| cashOnHand | Long | yes |

**Computed:**
```kotlin
val displayCorpus = openingCorpus + runningSavingsTotal + totalRepayments + totalFinesCollected - totalLoansDisbursed
val isWarning = displayCorpus < 0 // should never happen due to corpus gate, but defensive
```

**State animation:**
```kotlin
val backgroundColor by animateColorAsState(
    targetValue = if (isWarning) MaterialTheme.colorScheme.secondaryContainer
                  else MaterialTheme.colorScheme.tertiaryContainer,
    animationSpec = tween(200)
)
val textColor by animateColorAsState(
    targetValue = if (isWarning) MaterialTheme.colorScheme.onSecondaryContainer
                  else MaterialTheme.colorScheme.onTertiaryContainer,
    animationSpec = tween(200)
)
```

**Corpus value animation:**
- When displayCorpus changes: CrossfadeText composable
  - Fade old value out 100ms; fade new value in 100ms simultaneously (50ms overlap)

---

### 3.5 GroupHeaderCard

**Component name:** GroupHeaderCard
**Props:**
| Prop | Type | Required |
|------|------|----------|
| group | Group | yes |

**Visual spec:**
- background: primary_container #A6F1A6
- corner_radius: 0dp (edge-to-edge, appears flush with TopBar)
- padding: 16dp
- No elevation (embedded seamlessly below top bar)

**Layout:**
```
Column(padding: 16dp):
  Text(group.name, headlineSmall 24sp, on_primary_container #002106, fontWeight: SemiBold)
  Text("Cycle ${group.cycleNumber} of ${group.cycleLengthMonths} months • ${group.meetingFrequency} meetings",
       bodyMedium, on_primary_container, mt: 4dp)
  Row(mt: 8dp, gap: 8dp):
    AssistChip("${group.memberCount} members", secondary_container, on_secondary_container, corner: full)
    AssistChip(
      "${group.overdueLoansCount} overdue",
      if (overdueLoansCount > 0) error_container else surface_variant,
      if (overdueLoansCount > 0) on_error_container else on_surface_variant,
      corner: full
    )
```

---

## SECTION 4 — Interaction Patterns

### 4.1 GroupDashboard — Parallel Load

**Screen enters composition:**
1. GroupDashboardViewModel.OnLoad dispatches fetch_all_parallel
2. 4 API calls fire simultaneously:
   - get_center → group data
   - get_center_accounts → accounts data
   - get_group_corpus → corpus data (network-first, 60s TTL)
   - get_group_config → config data (stale-while-revalidate, 600s TTL)
3. ScreenState = Loading → 4 shimmer blocks render
4. As each API returns → state updates partially (not waiting for all 4)
5. After all 4 resolve → compute derived state:
   - isCorpusInsufficient = corpus.currentBalance < config.minimumDisbursementThreshold
   - isCorpusInsufficient: 47,500 < 5,000 → false (demo shows sufficient)
   - isCycleEnd = group.cycleNumber == group.cycleLengthMonths → false (month 1 of 12)
6. ScreenState = Content → shimmer fades out (200ms), cards fade in (250ms stagger)
7. CorpusCard entry: balance counts up from 0 to 47,500 (400ms counting animation)

**Refresh:**
- Pull-to-refresh → invalidate_cache=true → re-fetch all 4 APIs
- Only get_group_corpus is network-first (the others are stale-while-revalidate so already go to network eventually)
- RefreshIndicator: CircularProgressIndicator, primary #2E7D32, 24dp

---

### 4.2 Corpus Insufficient State Transition

**When corpus drops below minimumDisbursementThreshold:**

Scenario: loans grow during a meeting cycle; after meeting submission, corpus falls below KES 5,000.

1. PUT /dt_group_corpus called with new closingCorpus (e.g. KES 3,200)
2. Next GET /dt_group_corpus (TTL 60s or forced refresh on next dashboard visit)
3. corpus.currentBalance = 3,200 < config.minimumDisbursementThreshold = 5,000
4. isCorpusInsufficient = true

Visual transition (200ms each, can overlap):
5. CorpusCard border: none → 2dp error #D32F2F (animateColorAsState, 200ms)
6. Corpus amount color: primary #2E7D32 → error #D32F2F (animateColorAsState, 200ms)
7. CorpusBlockBanner: hidden → visible (AnimatedVisibility expandVertically, 200ms)
8. Content_description updated: "Warning: Loan disbursement is blocked."

In wizard (step 5 corpus gate):
- prospectiveClosing checked before ApproveLoanApplication dispatched
- If would go below 0: BLOCK (snackbar error, no state change)
- If would stay >= 0 but below minimumDisbursementThreshold: ALLOW with warning chip
- Warning chip: "⚠ Below minimum threshold" secondary_container chip below CorpusGateChip

---

### 4.3 Start Meeting — Corpus State Context

Per FR-018: loan disbursement is blocked when corpus insufficient, but meeting START is not blocked.

- isCorpusInsufficient=true + user taps "Start Meeting":
  1. Navigate normally to meeting-calendar (no dialog, no block)
  2. In meeting-calendar: upcoming card is shown normally
  3. Meeting conduct wizard: corpus band shows KES 3,200 (insufficient value)
  4. Step 5 loan applications: CorpusGateChip shows "Available to disburse: KES 3,200"
  5. Any loan approval attempt triggers gate: "Corpus insufficient..."
  6. Savings and attendance steps proceed normally (not corpus-gated)

---

### 4.4 Share-Out Button Behavior

**Disabled (isCycleEnd=false, Month 1 of 12):**
- Button visually disabled (outline_variant border, on_surface_variant text, 38% opacity on icon)
- Tap: no navigation; Snackbar: "Share-Out is only available at the end of the cycle." (error_container, 3000ms)
- Long-press: tooltip above button: "Available after Month 12" (surface_variant, 2000ms, labelSmall)

**Enabled (isCycleEnd=true, Month 12):**
- Button: secondary #FF8F00 border and text (amber = prosperity, harvest time)
- Tap → OnShareOut → NavigateToShareOut(groupId)
- Navigate to share-out-preview (slide-in from right, 400ms)

---

### 4.5 CorpusBand Real-time Update (Wizard Steps 2-6)

**Step 2 entry:**
- CorpusBand shows: openingCorpus = KES 12,400 (static, no updates yet)
- No user input on step 2 — display only

**Step 3 savings entry (updates):**
- Each SetSavingsAmount → displayCorpus recomputes:
  - displayCorpus = openingCorpus + runningSavingsTotal + 0 + 0 - 0
  - After Amina saves KES 200: displayCorpus = 12,400 + 200 = 12,600 (corpus grows)
  - After all 5 members (total group savings KES 1,000): displayCorpus = 13,400
- CorpusBand text: "Corpus: KES 12,600" → 100ms crossfade → "Corpus: KES 12,800" → etc.

**Step 4 repayments entry (updates):**
- SetLoanRepayment(Peter, KES 500) → displayCorpus = 13,400 + 500 = 13,900
- CorpusBand text crossfades: "Corpus: KES 13,900"

**Step 5 loan approval:**
- ApproveLoanApplication(Grace, KES 1,500):
  - Pre-check: prospectiveClosing = 13,900 - 1,500 = KES 12,400 > 0 → APPROVED
  - totalLoansDisbursed += 1,500
  - displayCorpus = 13,900 - 1,500 = 12,400
  - CorpusBand crossfades: "Corpus: KES 12,400"
  - CorpusGateChip updates: "Available to disburse: KES 12,400"

**Step 6 (closing):**
- CorpusBand shows final displayCorpus = 12,400 + 50 (fines) = 12,450
- Wait — fines added at step 1 (attendance), reflected in totalFinesCollected:
  - displayCorpus = 12,400 + 1,000 (savings) + 500 (repayments) + 50 (fines) - 1,500 (loans) = 12,450
  - CorpusBand: "Corpus: KES 12,450"

---

### 4.6 Corpus Gate Enforcement Detail

**Pre-approval corpus check algorithm:**
```
fun canApprove(loanAmount: Long, currentState: MeetingConductState): Boolean {
    val prospective = currentState.openingCorpus +
                      currentState.runningSavingsTotal +
                      currentState.totalRepayments +
                      currentState.totalFinesCollected -
                      currentState.totalLoansDisbursed -
                      loanAmount
    return prospective >= 0
}
```

**Gate trigger flow:**
1. Chairperson taps "Chairperson Approve" for Grace's KES 1,500 loan
2. canApprove(1500, state) called: 12,400 + 1,000 + 500 + 50 - 0 - 1,500 = 12,450 >= 0 → APPROVED
3. ApproveLoanApplication(graceId) dispatched

**Gate block example (hypothetical):**
1. John requests KES 15,000 (beyond corpus)
2. canApprove(15000, state): 12,450 - 15,000 = -2,550 < 0 → BLOCKED
3. ApproveLoanApplication NOT dispatched
4. ShowStepError emitted: "Corpus insufficient for this disbursement — available KES 12,450"
5. CorpusGateChip remains at "Available to disburse: KES 12,450"
6. analytics event: corpus_gate_triggered {loan_id: johnLoanId, requested: 15000, available: 12450}

---

### 4.7 Offline Corpus Display

**GroupDashboard offline:**
- get_group_corpus: TTL 60s network-first → if offline, use cache
- If cache exists: show corpus from cache with chip below amount: "As of Meeting #3 · 28 Apr 2026" (labelSmall, outline, corner: full)
- If no cache: corpus card shows "KES —" with placeholder text "Corpus unavailable offline"
- isCorpusInsufficient check: uses cached values if available; otherwise defaults to false (safe default — don't block unnecessarily)

**Meeting wizard offline:**
- openingCorpus loaded at wizard start (before offline potentially occurs)
- CorpusBand continues to show computed displayCorpus in-memory — no API dependency during entry
- On submit: SyncQueue path used; corpus PUT queued as priority 1
- Offline chip in TopAppBar remains visible throughout

---

## SECTION 5 — Content Data

### 5.1 Demo Group Data (GroupDashboard state)

**Group identity:**
- name: "Mwangaza Women's Group"
- cycleNumber: 1
- cycleLengthMonths: 12
- meetingFrequency: "Weekly"
- memberCount: 5
- overdueLoansCount: 0
- status: "ACTIVE"

**Corpus (from dt_group_corpus, as of Meeting #4):**
- currentBalance: KES 47,500 (corpus after 4 meetings plus initial fund)
- openingBalance: KES 0 (new cycle started from zero)
- totalContributionsThisCycle: KES 52,500 (all savings ever deposited into corpus)
- totalLoansOutstanding: KES 5,000 (Grace's loan of KES 1,500 + others from previous cycle)
- lastUpdated: "07 May 2026"

**Config (from dt_group_config):**
- contributionMin: 100 (note: GroupDashboard shows 100-500 range; meeting wizard enforces 200 min)
- contributionMax: 500 (max per meeting per member for group savings)
- loanMultiplier: 3.0 (max loan = savings balance × 3)
- interestRate: 10.0 (10% annual)
- cycleLengthMonths: 12
- fineAmount: 50.0 (KES 50 per late occurrence; 100 for absent via FR-012)
- minimumDisbursementThreshold: 5,000 (corpus must be >= KES 5,000 to disburse)

**Accounts summary:**
- savingsBalance: KES 52,500
- loansOutstanding: KES 5,000
- activeLoanCount: 1

**Derived state:**
- isCorpusInsufficient: 47,500 < 5,000 → false (sufficient)
- isCycleEnd: cycleNumber (1) == cycleLengthMonths (12) → false (not at cycle end)

### 5.2 Corpus in Meeting Wizard (#4, Step-by-Step)

| Step | Event | displayCorpus |
|------|-------|--------------|
| Step 2 entry | openingCorpus loaded | KES 12,400 |
| Step 3 — Amina KES 200 | savings += 200 | KES 12,600 |
| Step 3 — Peter KES 200 | savings += 200 | KES 12,800 |
| Step 3 — Grace KES 200 | savings += 200 | KES 13,000 |
| Step 3 — John KES 200 | savings += 200 | KES 13,200 |
| Step 3 — Mary KES 200 | savings += 200 | KES 13,400 |
| Step 4 — Peter repays KES 500 | repayments += 500 | KES 13,900 |
| Step 1 (calculated) — Grace fine KES 50 | fines total = 50 | (applied at step 1; reflected from step 2) |
| CorpusBand (with fines) from step 2 | all inflows | KES 13,950 |
| Step 5 — Grace KES 1,500 approved | disbursed += 1500 | KES 12,450 |
| Step 6 — closing balance | final reconciliation | KES 12,450 |

Note: displayCorpus formula includes fines immediately from step 2:
displayCorpus = 12,400 + runningSavingsTotal + totalRepayments + totalFinesCollected - totalLoansDisbursed

After all step 1 fines are computed (Grace KES 50 LATE):
- totalFinesCollected = 50
- So from step 2 onward: displayCorpus = 12,400 + 0 + 0 + 50 = 12,450 initially
- Then savings add: + 1,000 → 13,450
- Then repayments add: + 500 → 13,950
- Then loan disburse: - 1,500 → 12,450 (final closing)

### 5.3 Recent Activity Feed (demo data)

| # | Type | Description | Date | Member | Amount |
|---|------|-------------|------|--------|--------|
| 1 | MEETING | Meeting #4 conducted | 7 May 2026 | Amina Hassan | KES 1,750 |
| 2 | DEPOSIT | Individual savings deposit | 7 May 2026 | Amina Hassan | KES 500 |
| 3 | LOAN | Loan disbursed | 7 May 2026 | Grace Wanjiku | KES 1,500 |
| 4 | DEPOSIT | Group savings deposit | 28 Apr 2026 | All members | KES 1,850 |
| 5 | LOAN | Loan repayment received | 28 Apr 2026 | Peter Otieno | KES 500 |

### 5.4 Corpus Insufficient Scenario (hypothetical demo for testing)

To trigger isCorpusInsufficient=true in testing:
- Simulate dt_group_config.minimumDisbursementThreshold = 50,000 (test-only)
- With corpus.currentBalance = 47,500 < 50,000 → isCorpusInsufficient = true
- OR: set corpus.currentBalance = 800 via datatable update (realistic scenario: many loans disbursed)

Expected UI when insufficient:
- corpus card border: 2dp #D32F2F appears (200ms transition)
- corpus amount: color transitions to error #D32F2F (200ms)
- block banner: expands into view (200ms expandVertically)
- Quick actions: "Start Meeting" remains enabled; "Loans" remains enabled; all 4 buttons unchanged

### 5.5 Corpus Gate Test Scenarios (Step 5 wizard)

| Scenario | Requested | Available | Gate Result |
|----------|-----------|-----------|-------------|
| Grace KES 1,500 (approved) | 1,500 | 13,950 | APPROVED — 13,950 - 1,500 = 12,450 >= 0 |
| John KES 3,000 after Grace approved | 3,000 | 12,450 | APPROVED — 12,450 - 3,000 = 9,450 >= 0 |
| Amina KES 13,000 after above two | 13,000 | 9,450 | BLOCKED — 9,450 - 13,000 = -3,550 < 0 |
| Peter KES 9,000 after above two | 9,000 | 9,450 | APPROVED — 9,450 - 9,000 = 450 >= 0 |

---

## SECTION 6 — Responsive Rules

### 6.1 Breakpoints

| Name | Range | Primary Device |
|------|-------|---------------|
| compact | 0–599dp | Standard Android phones |
| medium | 600–839dp | Foldables, 7" tablets |
| expanded | 840dp+ | 10"+ tablets |

### 6.2 Compact (0–599dp) — Primary Target

**GroupDashboard (compact):**
- LazyColumn: single column; all cards full-width minus 32dp (16dp margins each side)
- CorpusCard: full-width card; displaySmall 36sp fits in ~300dp (5 characters "47,500" × 36sp = ~180dp — fine)
- QuickActionsGrid: 2×2 grid; button width = (360dp - 32dp - 12dp) / 2 = 158dp
- Button height: 56dp (comfortable, rural-friendly large targets)
- ActivityFeed: up to 5 items; each 56dp; total ~280dp (fits without pagination on compact)
- GroupHeaderCard: full-width, 0dp corner (flush with topbar)
- BottomNavigation: visible, 56dp, 4 tabs

**CorpusBand (compact, inside wizard):**
- height: 40dp; spans full screen width (edge-to-edge)
- Both text items on one row, space_between: "Corpus: KES 12,400" (left) + "Cash on Hand: KES 2,000" (right)
- At 360dp: "Corpus: KES 12,400" = ~120dp + "Cash on Hand: KES 2,000" = ~140dp → total 260dp + 16dp each side padding = OK (fits)
- If balance exceeds 99,999 (KES 100,000+): consider truncating to "KES 100K" format at compact

### 6.3 Medium (600–839dp) — Foldable / Small Tablet

**GroupDashboard (medium):**
- NavigationRail (72dp left) + content area (screen_width - 72dp)
- Content: max width 560dp, centered horizontally within content area
- CorpusCard: max 560dp; sub-stats row gains more horizontal space (stats can be wider)
- QuickActionsGrid: buttons width = (560dp - 12dp) / 2 = 274dp per button (comfortably wide)
- GroupHeaderCard: max 560dp (or edge-to-edge on medium for visual impact)
- ActivityFeed: may show 7 items before scroll (more vertical space available)

**CorpusBand (medium):**
- Same layout as compact (edge-to-edge); text has more horizontal space so never truncates

### 6.4 Expanded (840dp+) — Tablet / Large Foldable

**GroupDashboard (expanded):**
- NavigationDrawer: permanent, 240dp left panel
- Content area: screen_width - 240dp
- 2-column layout within content area:
  - Left column: CorpusCard (full-width of left column) + QuickActionsGrid (4 buttons in 2×2, larger)
  - Right column: GroupHeaderCard (strip) + SavingsSummaryCard + ActivityFeed (expanded, up to 10 items)
- CorpusCard in 2-column layout: constrained to ~420dp; displaySmall 36sp has ample room
- QuickActionsGrid: can expand to 4 columns (1×4) on expanded (all 4 buttons in one row)

**GroupDashboard 2-column split (expanded):**
```
[240dp NavigationDrawer] | [Left col ~380dp] | [Right col remaining ~440dp]
                           GroupHeaderCard       (above both cols, full width)
                           CorpusCard            SavingsSummaryCard
                           QuickActionsGrid      ActivityFeedCard (2× items)
```

**CorpusBand (expanded, inside wizard 2-panel layout):**
- Spans top of right panel only (step content panel)
- Left panel: vertical step list; does not need CorpusBand (corpus is step content context)
- Right panel top: CorpusBand horizontal strip, full right-panel width

### 6.5 Font Scaling Considerations

- displaySmall 36sp for corpus balance: at system scale 2.0× → 72sp effective
  - May require layout adjustment at 2.0×: "KES 47,500" at 72sp ≈ 280dp wide → still fits in 320dp card
  - Defensive: apply AutoSizeText with min 24sp / max 36sp if balance exceeds 7 digits
- labelSmall 11sp (stat labels): at 1.5× = 16.5sp — comfortable
- bodyMedium 14sp (block banner): at 1.5× = 21sp — remains readable within card

### 6.6 Orientation

**Landscape on compact (width ≈ 700dp → treated as medium):**
- GroupDashboard: NavigationRail appears
- CorpusCard: same layout; displaySmall 36sp with ample landscape width
- QuickActionsGrid: expand to 4 columns (1×4 row in landscape)
- ActivityFeed: more items visible without scroll

**Landscape wizard CorpusBand:**
- Same 40dp band; landscape gives more horizontal space — no text truncation issues

### 6.7 Dynamic Color / Material You

If system supports Material You (Android 12+):
- Tonal surface uses primary color tint at tonal_alpha for each elevation level
- CorpusCard at elevation level_4 (12% alpha): surface gets slight green tint → reinforces "corpus is healthy"
- When isCorpusInsufficient: tonal surface switches to error color → entire card surface faintly red — pre-attentive visual warning

### 6.8 RTL Support

- GroupHeaderCard: group name start-aligned; all content start-aligned
- CorpusCard: sub-stats remain in SpaceEvenly row (symmetric, RTL-safe)
- CorpusCard block banner: icon start, text end → RTL reverses to icon end, text start (automatic with Row layout)
- QuickActionsGrid: grid cells mirror in RTL (Members top-right → top-left in RTL)
- ActivityListItem: leading icon on start; trailing amount on end — RTL mirrors correctly
- CorpusBand: "Corpus: KES X" on start, "Cash on Hand: KES Y" on end → both align to respective edges in RTL
- CorpusGateChip: chip text is always LTR (KES amounts don't change reading direction)

### 6.9 Dark Theme

**Key color changes (dark theme):**
- CorpusCard background: surface dark #121412 (slightly darker than surface)
- Corpus balance (sufficient): primary dark #8BD68F (lighter green, high contrast on dark bg)
- Corpus balance (insufficient): error dark #FFB4AB (lighter red on dark)
- CorpusCard border (insufficient): error dark #FFB4AB (2dp)
- CorpusBlockBanner: error_container dark #93000A, on_error_container dark #FFDAD6
- GroupHeaderCard: primary_container dark #00531A, on_primary_container dark #A6F1A6
- CorpusBand: tertiary_container dark #004A82, on_tertiary_container dark #D2E4FF
- QuickActions: Start Meeting button: primary dark #8BD68F, on_primary dark #003910
- Activity icons: all tints shift to dark equivalents automatically via MaterialTheme.colorScheme

**Shimmer dark theme:**
- shimmer gradient: surface_variant dark #424942 → outline_variant dark #424942 (lighter) → surface_variant dark
- Luminance delta: ~15 points for visibility in dark theme

---

## Appendix A — i18n Keys (corpus-tracking)

All user-visible strings for corpus-tracking displayed components:

| Key | English |
|-----|---------|
| corpus_label | "Corpus Fund" |
| corpus_blocked | "Loan disbursement is blocked — corpus balance is below minimum threshold." |
| quick_actions_label | "Quick Actions" |
| start_meeting | "Start Meeting" |
| view_members | "Members" |
| view_loans | "Loans" |
| share_out | "Share-Out" |
| savings_label | "Savings Summary" |
| contribution_range | "Mandatory contribution: KES {{min}} – KES {{max}} per meeting" |
| activity_label | "Recent Activity" |
| error_network | "No internet. Showing cached data." |
| error_server | "Server error. Please retry." |
| error_not_found | "Group not found." |
| error_auth | "Session expired." |
| share_out_not_available | "Share-Out is only available at the end of the cycle." |
| corpus_insufficient_snackbar | "Corpus insufficient for this disbursement — available KES {{amount}}" |
| corpus_offline_note | "Data as of Meeting #{{number}}" |
| corpus_unavailable_offline | "Corpus unavailable offline" |
| opening_balance | "Opening Balance" |
| contributions_this_cycle | "Contributions" |
| loans_outstanding | "Loans Out" |

---

## Appendix B — Composable Dependency Map (corpus-tracking)

```
GroupDashboardScreen
  ├── GroupDashboardViewModel (Hilt ViewModel)
  │   ├── GroupRepository
  │   │   ├── FineractCenterDataSource (Retrofit: /centers/{id} + /centers/{id}/accounts)
  │   │   └── LocalGroupDao (SQLDelight)
  │   ├── CorpusRepository
  │   │   ├── FineractCorpusDataSource (Retrofit: /datatables/dt_group_corpus/{id})
  │   │   └── LocalCorpusDao (SQLDelight, 60s TTL)
  │   ├── NetworkMonitor (ConnectivityManager)
  │   └── SessionManager (DataStore)
  ├── TopBar (group name, back nav, more options)
  ├── GroupHeaderCard (group identity, cycle info, member/overdue chips)
  ├── CorpusCard
  │   ├── CorpusAmountText (animated counting display)
  │   ├── CorpusBlockBanner (AnimatedVisibility, error_container)
  │   └── CorpusSubStatsRow (3 stats: opening, contributions, loans out)
  ├── QuickActionsCard
  │   └── QuickActionsGrid (2×2: Start Meeting, Members, Loans, Share-Out)
  ├── SavingsSummaryCard
  ├── ActivityFeedCard
  │   └── ActivityListItem × N (max 5 items)
  └── ShimmerDashboard (visible when isLoading)

CorpusBand (inside MeetingConductScreen)
  ├── MeetingConductViewModel (shared, provides computed displayCorpus)
  ├── CorpusBandContent (Row with corpus amount + cash on hand)
  └── AnimatedColor (background transitions tertiary↔secondary when isWarning)

CorpusGateChip (inside Step5LoanApplications)
  ├── MeetingConductViewModel (availableForDisbursal computed)
  ├── AssistChip (tertiary_container, live updating text)
  └── ConnectedTo: ApproveLoanApplicationButton (enabled gate check)
```

---

## Appendix C — Corpus Update API Sequence (Meeting Submit)

The corpus update is the final step in the 6-call submission sequence. This ordering is critical — corpus must reflect all other transactions.

**Call 1:** POST dt_meeting_record → creates the meeting record row
- Body: CreateMeetingRecordRequest with closingCorpus embedded
- Response: DataTableEntryResponse {resourceId, resourceIdentifier}

**Call 2:** POST dt_meeting_attendance × 5 members → records per-member attendance
- One call per member; 5 total
- Body: CreateAttendanceRequest {meetingId, memberId, status, fineAmount}

**Call 3:** POST savingsaccounts/{id}/transactions × 9 calls → records all savings
- 5 group savings + 4 individual savings (Peter = 0, excluded)
- Each call: SavingsTransactionRequest {date, amount, paymentTypeId=1, locale, dateFormat}

**Call 4:** POST loans/{id}/transactions?command=repayment × 1 → Peter's repayment
- Body: LoanRepaymentRequest {date, amount, paymentTypeId}

**Call 5:** POST loans/{id}/transactions?command=disburse × 1 → Grace's approved loan
- Body: LoanDisbursalRequest {actualDisbursementDate, note, locale, dateFormat}

**Call 6 (corpus):** PUT dt_group_corpus/{centerId} → updates corpus to closingCorpus
- Body: UpdateCorpusRequest {corpusBalance: 12450, lastUpdatedMeeting: 4, lastUpdatedDate: "07 May 2026"}
- This is priority 1 in SyncQueue if offline — corpus integrity is the most critical invariant

**Error recovery (any call fails):**
- Calls 1-5 failures → SyncQueue with ordered priorities
- Call 6 (corpus) failure → SyncQueue priority 1 (highest)
- Next app launch: SyncQueue auto-processes in priority order
- Corpus displayed from local state until next GET /dt_group_corpus confirms

---

## Appendix D — Test Scenarios Matrix (corpus-tracking)

| Scenario | Screen | Condition | Expected Behavior |
|----------|--------|-----------|------------------|
| Dashboard load, corpus sufficient | GroupDashboard | corpus 47,500 >= threshold 5,000 | Green corpus amount; no border; no block banner |
| Dashboard load, corpus insufficient | GroupDashboard | corpus 800 < threshold 5,000 | Red corpus amount; 2dp error border; block banner visible |
| Start Meeting when insufficient | GroupDashboard | isCorpusInsufficient=true | Navigate to meeting-calendar normally (meeting start not blocked) |
| Loans button when insufficient | GroupDashboard | isCorpusInsufficient=true | Navigate to loan-list normally |
| Share-Out disabled | GroupDashboard | isCycleEnd=false | Button disabled (38% opacity); tap shows snackbar |
| Share-Out enabled | GroupDashboard | isCycleEnd=true | Button enabled (amber); tap navigates to share-out-preview |
| API timeout (all 4 calls) | GroupDashboard | No cache | Error screen with "Could not load group" and Retry |
| API timeout (corpus only) | GroupDashboard | Other APIs succeed | Partial content with "Corpus unavailable" chip |
| CorpusBand step 1→2 | MeetingConduct | currentStep advances 1→2 | CorpusBand slides in from top (200ms) |
| CorpusBand step 2→1 (back) | MeetingConduct | currentStep decrements 2→1 | CorpusBand slides out to top (150ms) |
| Corpus gate — sufficient | MeetingConduct step 5 | 12,450 - 1,500 = 10,950 >= 0 | Approval proceeds; displayCorpus decrements |
| Corpus gate — blocked | MeetingConduct step 5 | 12,450 - 15,000 = -2,550 < 0 | Approval blocked; error snackbar; corpus unchanged |
| CorpusBand savings update | MeetingConduct step 3 | Amina enters KES 200 | Band crossfades to KES 12,650 (12,400 + 200 + 50 fines) within 100ms |
| CorpusBand repayment update | MeetingConduct step 4 | Peter repays KES 500 | Band crossfades to KES 13,150 |
| Offline corpus display | GroupDashboard | isOffline=true, cache exists | Cached corpus shown; "Data as of Meeting #3" chip below amount |
| Corpus card entry animation | GroupDashboard | Screen enters | Balance counts up 0→47,500 over 400ms |

---

## Appendix E — Animation Choreography Timeline (corpus-tracking)

**GroupDashboard initial load (parallel APIs):**

| Time | Event |
|------|-------|
| T=0ms | Screen enters; 4 API calls fire simultaneously |
| T=0ms | Shimmer blocks appear (4x, fade-in 200ms) |
| T=~300ms | get_group_config returns (600s TTL — may be cache hit) |
| T=~800ms | All 4 APIs complete (typical network latency) |
| T=800ms | isCorpusInsufficient computed; isCycleEnd computed |
| T=800ms | Shimmer fades out (250ms) |
| T=850ms | GroupHeaderCard fades in (first, 200ms) |
| T=900ms | CorpusCard fades in (200ms) |
| T=900ms | Corpus amount counting animation starts (400ms, 0→47,500) |
| T=950ms | QuickActionsCard fades in (200ms) |
| T=1000ms | SavingsSummaryCard fades in (200ms) |
| T=1050ms | ActivityFeedCard fades in (200ms) |
| T=1300ms | Corpus amount reaches KES 47,500 (counting completes) |
| T=1300ms | Screen fully rendered and interactive |

**CorpusBand appear (step 1→2 in wizard):**

| Time | Event |
|------|-------|
| T=0ms | NextStep dispatched from step 1 |
| T=0ms | Attendance validation passes |
| T=50ms | currentStep = 2 |
| T=50ms | CorpusBand slideInVertically starts (from -40dp, 200ms) |
| T=50ms | StepContent crossfades to step 2 (200ms) |
| T=250ms | CorpusBand fully visible at top of step content area |
| T=250ms | Step 2 content rendered (OpeningBalance) |

**Corpus gate trigger animation:**

| Time | Event |
|------|-------|
| T=0ms | Chairperson taps "Chairperson Approve" for John KES 15,000 |
| T=0ms | canApprove() check runs synchronously (< 1ms) |
| T=0ms | canApprove returns false |
| T=0ms | ShowStepError event emitted |
| T=100ms | Error snackbar starts sliding up (300ms slide, decelerated) |
| T=100ms | corpus_gate_triggered analytics event sent |
| T=400ms | Snackbar fully visible at bottom |
| T=4400ms | Snackbar auto-dismisses (4000ms display) |
| T=4550ms | Snackbar fully gone (150ms fade) |

---

## Appendix F: Error State Specifications

### GroupDashboard — Loading States Detail

**Shimmer skeleton (isLoading=true):**
```
┌──────────────────────────────────────┐
│  ←  [shimmer 120dp wide]      [⋮]  │  TopBar still renders
├──────────────────────────────────────┤
│  ┌──────────────────────────────┐   │
│  │  [shimmer rect 120dp height] │   │  GroupHeaderCard placeholder
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │  [shimmer rect 120dp height] │   │  CorpusCard placeholder
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │  [shimmer rect 120dp height] │   │  QuickActionsSection placeholder
│  └──────────────────────────────┘   │
│  ┌──────────────────────────────┐   │
│  │  [shimmer rect 120dp height] │   │  ActivityFeed placeholder
│  └──────────────────────────────┘   │
└──────────────────────────────────────┘
```

Shimmer spec:
- Background: surface_variant #DEE5DA
- Gradient: linear, 0° → 180°, from #DEE5DA to #F5F7F3 to #DEE5DA
- Animation: translateX sweep 1,200ms, repeat indefinitely
- Corner: 16dp matching actual cards
- Height: 120dp per block (4 blocks)

### Corpus Data Unavailable States

| Trigger | CorpusCard Display | User Action |
|---------|-------------------|-------------|
| 404 on dt_group_corpus | KES —, chip "Corpus data missing" | Tap chip → support info |
| 500 (server error) | KES — (cached if available), amber chip | Retry button inside card |
| Auth 401 | Redirect to login (global handler) | Re-authenticate |
| Timeout >30s | Cached balance shown + warning chip | Auto-retry in 60s |
| Offline (no cache) | KES — with cloud_off icon | Prompt for connection |

### Corpus Card — Offline with Cache

```
┌──────────────────────────────────────┐
│ Corpus Fund         [sync_problem⚠] │  chip: secondary_container #FFDDB3
│ KES 47,500                           │  displaySmall 36sp #2E7D32
│ As of Meeting #3 (05 May 2026)       │  bodySmall #424942, italic
│                                      │
│  Opening  Contributions  Loans Out   │
│  KES 0    KES 52,500   KES 5,000    │
└──────────────────────────────────────┘
```

The "As of Meeting #X" suffix is derived from corpus.lastUpdated field stored in SQLDelight offline cache.

---

## Appendix G: CorpusCard Component Deep Dive

### animateColorAsState Usage

```
// Conceptual Kotlin (for Stitch rendering reference)
val cardBorderColor by animateColorAsState(
    targetValue = if (isCorpusInsufficient) MaterialTheme.colorScheme.error else Color.Transparent,
    animationSpec = tween(durationMillis = 200, easing = FastOutSlowInEasing),
    label = "corpusCardBorder"
)
val corpusTextColor by animateColorAsState(
    targetValue = if (isCorpusInsufficient) MaterialTheme.colorScheme.error
                  else MaterialTheme.colorScheme.primary,
    animationSpec = tween(durationMillis = 200),
    label = "corpusTextColor"
)
```

### CorpusCard Sub-stat Row Layout

Three equal-width sub-stats in a Row with weight(1f) each:

| Stat | Label | Value | Alignment |
|------|-------|-------|-----------|
| 1 | Opening | KES 0 | Center |
| 2 | Contributions | KES 52,500 | Center |
| 3 | Loans Out | KES 5,000 | Center |

- Label: labelSmall 11sp, #424942 (on_surface_variant)
- Value: titleSmall 14sp bold, #1A1C19 (on_surface)
- Dividers: 1dp vertical dividers between stats (color: outline_variant #C1C9BE)
- Background: surface_variant #DEE5DA, corner 8dp, padding 8dp each stat

### Block Banner Specification

Appears inside CorpusCard when isCorpusInsufficient=true:
- Background: errorContainer #FFDAD6
- Corner: 8dp
- Padding: 12dp horizontal, 8dp vertical
- Left icon: warning 20dp, on_error_container #410002
- Text: "Loan disbursement is blocked" titleSmall #410002
- Sub-text: "corpus balance is below minimum threshold." bodySmall #410002
- Invisible label: "INSUFFICIENT" added for screen reader (alpha=0f visually, visible to TalkBack)
- Appears with: fadeIn(150ms) + expandVertically(200ms)
- Disappears with: fadeOut(150ms) + shrinkVertically(200ms)

### CorpusCard — Quick Demo Values Cross-Check

| Metric | Value | Source |
|--------|-------|--------|
| currentBalance | KES 47,500 | dt_group_corpus demo |
| openingBalance | KES 0 | Cycle just started |
| totalContributionsThisCycle | KES 52,500 | All savings deposited |
| totalLoansOutstanding | KES 5,000 | Active loan principal |
| minimumDisbursementThreshold | KES 5,000 | dt_group_config |
| isCorpusInsufficient | false | 47,500 ≥ 5,000 |
| corpus formula check | 0 + 52,500 - 5,000 = 47,500 | Verified correct |

---

## Appendix H: QuickActionsGrid State Logic

### Four Action States

| Action | Icon | Condition | State |
|--------|------|-----------|-------|
| Start Meeting | calendar_today | Always enabled | FilledButton (primary) |
| Members | group | Always enabled | OutlinedButton |
| Loans | monetization_on | Always enabled | OutlinedButton |
| Share-Out | currency_exchange | isCycleEnd == true | OutlinedButton (enabled) |
| Share-Out | currency_exchange | isCycleEnd == false | OutlinedButton (disabled, 38% alpha) |

### Share-Out Tooltip (disabled state)

On tap of disabled Share-Out button:
1. Event: ShowCorpusBlockedDialog (reused for context)
2. Instead, custom: Snackbar appears: "Share-Out is only available at the end of the cycle (Week 52)"
3. Duration: 3000ms auto-dismiss
4. No action button in snackbar

### Meeting Start When Corpus Insufficient

**Critical UX decision:** Corpus insufficient state does NOT block meeting start.

- Start Meeting button remains FilledButton (primary) regardless of isCorpusInsufficient
- Navigation proceeds to meeting-calendar screen
- The corpus gate only blocks loan disbursement approval in step 5 of the wizard
- Rationale: group must still conduct meeting to collect savings/repayments which may restore corpus

---

## Appendix I: ActivityFeed Deep Dive

### Activity Types and Icons

| Type | Icon | Icon Tint | Description Pattern |
|------|------|-----------|---------------------|
| MEETING | calendar_month | primary #2E7D32 | "Meeting #N conducted" |
| DEPOSIT | arrow_upward | secondary_green | "Grace Wanjiku deposit" |
| LOAN | payments | tertiary #1565C0 | "Peter Otieno loan repaid" |
| PENALTY | warning | error #D32F2F | "Mary Akinyi fine — absent" |
| SHARE_OUT | account_balance | gold #FF8F00 | "Share-out distributed" |

### Demo Activity Items (5 items, Meeting #4)

| # | Type | Description | Amount | Date | Member |
|---|------|-------------|--------|------|--------|
| 1 | MEETING | Meeting #4 conducted | KES 1,750 | 7 May | Amina Hassan |
| 2 | DEPOSIT | Individual savings | KES 200 | 5 May | Grace Wanjiku |
| 3 | LOAN | Repayment | KES 500 | 28 Apr | Peter Otieno |
| 4 | PENALTY | Fine — absent | KES 50 | 21 Apr | Mary Akinyi |
| 5 | MEETING | Meeting #3 conducted | KES 1,600 | 14 Apr | Amina Hassan |

### ActivityListItem Layout

```
┌──────────────────────────────────────┐  height: 72dp
│  [icon 24dp]  Meeting #4 conducted  │  icon + titleSmall
│               Amina Hassan    7 May  │  member + date bodySmall
│                         KES 1,750   │  amount titleSmall (right-aligned)
└──────────────────────────────────────┘  divider bottom 1dp
```

- Max 5 items visible before "See all activity" link
- Tap any item: NavigateToActivityDetail (passes activityId)
- Long-press: no action (not required in v1)
- Empty state: centered text "No activity yet — conduct your first meeting"

---

## Appendix J: Responsive Design Supplement

### Compact (0–599dp) — Primary Form Factor

GroupDashboard scrolls as single column:
1. TopBar (56dp)
2. GroupHeaderCard (88dp)
3. CorpusCard (variable: 120dp normal, 168dp with block banner)
4. QuickActionsGrid (2×2 grid, 148dp total)
5. SavingsSummaryCard (88dp)
6. ActivityFeedCard (variable: 72dp per item × 5 = 360dp + header 48dp)

Total scroll height: ~830dp on a 800dp viewport → 30dp scroll

### Medium (600–839dp) — Foldable / Small Tablet

GroupDashboard adapts to 2-column layout for cards:
- Column 1: GroupHeaderCard + CorpusCard
- Column 2: QuickActionsGrid (2×2 grid, now 1×4 vertical) + SavingsSummaryCard
- ActivityFeed: full-width below, 3 items visible

CorpusCard: displaySmall stays 36sp (no scaling up — too large at this breakpoint already)
TopBar: extended width with more horizontal padding (24dp each side vs 16dp)

### Expanded (840dp+) — Large Tablet / Desktop

Two-panel layout:
- Left panel (40% width): GroupHeaderCard + CorpusCard + SavingsSummaryCard
- Right panel (60% width): QuickActionsGrid (full 2×2) + ActivityFeedCard (shows all 5 items)
- No scrolling needed — all content visible at once on most tablets

CorpusBand in wizard (expanded):
- Horizontal band still 40dp height
- KES amounts show commas formatted without truncation (KES 47,500 not KES 47.5K)
- CorpusGateChip widens to fill row (maxWidth constraint removed at expanded breakpoint)

### Dynamic Type Scaling

| System font scale | CorpusCard KES display | CorpusBand | Member rows |
|-------------------|----------------------|------------|-------------|
| 1.0 (default) | 36sp displaySmall | 14sp labelLarge | 14sp bodyMedium |
| 1.15 | 36sp (no scale — critical number) | 14sp | 14sp |
| 1.3 | 36sp (capped) | 14sp | 14sp |
| 1.5 | 30sp (scaled down to prevent overflow) | 13sp | 13sp |
| 2.0 | 24sp titleLarge fallback | 12sp | 12sp |

Critical rule: Corpus KES balance must NEVER truncate or ellipsize. Use sp values that scale down gracefully before allowing wrapping.

---

## Appendix K: Corpus Feature Integration Checklist

### Before Merging corpus-tracking Feature

**CorpusCard (GroupDashboard):**
- [ ] Network-first strategy implemented with 60s TTL in CorpusRepository
- [ ] animateColorAsState used for border and text color transitions (200ms tween)
- [ ] isCorpusInsufficient computed as: corpus.currentBalance < config.minimumDisbursementThreshold
- [ ] Block banner appears/disappears with fade+expand animation
- [ ] Content description updated dynamically when insufficient state changes
- [ ] Shimmer shows 4 blocks (not 3) matching final card count
- [ ] All 4 API calls dispatched in parallel (not sequential)

**CorpusBand (MeetingConductScreen):**
- [ ] CorpusBand only visible on steps 2–6 (not step 1 or step 7)
- [ ] slideInVertically animation on step 1→2 transition (200ms decelerated)
- [ ] displayCorpus computed via derivedStateOf (not recomputed on unrelated state)
- [ ] Text crossfades (100ms) on every displayCorpus change
- [ ] Background transitions to secondary_container when warning state

**Corpus Gate (Step 5):**
- [ ] canApprove() runs synchronously before dispatching ApproveLoanApplication
- [ ] Gate checks: projectedCorpus = displayCorpus - requestedAmount; canApprove = projectedCorpus >= 0
- [ ] Error snackbar uses errorContainer bg (NOT default snackbar bg)
- [ ] analytics: corpus_gate_triggered emitted with available_corpus + requested_amount
- [ ] CorpusGateChip updates in real-time as loans approved

**Corpus Update (Meeting Submission):**
- [ ] PUT /datatables/dt_group_corpus/{centerId} called with closingCorpus from wizard computation
- [ ] On 5xx: queued to SyncQueue priority 1 (highest priority)
- [ ] On success: SQLDelight corpus cache updated immediately
- [ ] locale="en" and dateFormat="dd MMMM yyyy" always included in PUT body
- [ ] lastUpdatedMeeting = current meetingNumber (from MeetingConductState)
