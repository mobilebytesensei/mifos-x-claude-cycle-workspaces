# Group-Linked Savings — Stitch Prompt Specification
**Feature**: group-linked-savings | **Screen**: savings-dashboard
**Stitch project**: MifosSave / mifos-x-group-banking
**Total sections**: 6

---

# SECTION 1: DESIGN SYSTEM CONTEXT

## Application Identity
MifosSave is a VSLA (Village Savings and Loan Association) group banking app for rural communities. The savings dashboard is the financial health hub for group treasurers and chairpersons — it visualizes the dual savings model: mandatory group contributions (built collectively, meeting by meeting) and voluntary individual savings (personal balances each member controls). The design must be warm and encouraging: green for group progress, amber for personal balances.

## Material Design 3 Token System

### Color Palette (all hex values exact)

#### Primary — VSLA Green (group savings, progress, tab indicator)
- primary: #2E7D32
- onPrimary: #FFFFFF
- primaryContainer: #A6F1A6
- onPrimaryContainer: #002106

#### Secondary — Amber (individual savings, personal balances)
- secondary: #FF8F00
- onSecondary: #FFFFFF
- secondaryContainer: #FFDDB3
- onSecondaryContainer: #2A1700

#### Tertiary — Trust Blue (individual member avatars)
- tertiary: #1565C0
- onTertiary: #FFFFFF
- tertiaryContainer: #D2E4FF
- onTertiaryContainer: #001C39

#### Error (withdrawal chip)
- error: #D32F2F
- errorContainer: #FFDAD6
- onErrorContainer: #410002

#### Neutral
- surface: #FAFAFA
- onSurface: #1C1C1C
- surfaceVariant: #DEE5DA
- onSurfaceVariant: #424942
- outline: #727971

### Typography Scale (Noto Sans, scale_style: large)

| Style | Size (sp) | Weight | Usage |
|-------|-----------|--------|-------|
| titleLarge | 22 | 500 | TopAppBar title |
| titleSmall | 14 | 500 | Section headers (Per-Member Contributions) |
| headlineMedium | 28 | 400 | Individual total balance |
| labelLarge | 14 | 500 | Cycle progress label, tab labels, group total chip, trailing amounts |
| labelMedium | 12 | 500 | Avatar initials, deposit/withdrawal chip labels |
| labelSmall | 11 | 500 | Sync band, cycle percent, trailing "total"/"balance" labels |
| bodyLarge | 16 | 400 | Member names |
| bodyMedium | 14 | 400 | Cycle collected/target amounts |
| bodySmall | 12 | 400 | Member subtitles (meetings contributed, last transaction) |

### Spacing Scale
| Token | Value (dp) |
|-------|-----------|
| xxs | 2 |
| xs | 4 |
| sm | 8 |
| md | 12 |
| lg | 16 |
| xl | 24 |

### Shape Scale
| Token | Corner Radius | Usage |
|-------|--------------|-------|
| extra_small | 4dp | Chips |
| small | 8dp | — |
| medium | 12dp | Cycle card, individual total card |
| large | 16dp | — |
| full | 9999dp | Avatar circles, badges |

### Elevation
| Level | dp | Usage |
|-------|----|-------|
| level_0 | 0dp | Flat rows |
| level_2 | 3dp | TopAppBar (scrolled), cards |

### Motion
| Token | Duration | Usage |
|-------|----------|-------|
| short_4 | 200ms | Tab crossfade |
| medium_1 | 250ms | Pull-to-refresh indicator |
| shimmer_cycle | 1200ms | Skeleton pulse |

### Accessibility
- Min touch target: 48dp (member rows: 72dp, exceeds minimum)
- Color contrast: 4.5:1 WCAG AA
- Charts must have contentDescription summaries (not color-alone)
- Deposit/withdrawal identified by label text + color (not color alone)

### Breakpoints
| Name | Range | Behavior |
|------|-------|----------|
| compact | 0–599dp | Single column, full-width |
| medium | 600–839dp | Centered, 80% width |
| expanded | 840dp+ | Two-column: chart left, member list right |

---

# SECTION 2: SCREEN COMPONENT TREES

## Screen: savings-dashboard (GROUP tab selected)

```
SavingsDashboardScreen(selectedTab=GROUP, isLoading=false, isRefreshing=false)
├── Scaffold
│   ├── TopAppBar
│   │   ├── title: Column
│   │   │   ├── Text("Savings", titleLarge, onSurface)
│   │   │   └── Text("Mwangaza Women's Group", bodySmall, onSurfaceVariant)
│   │   ├── actions:
│   │   │   └── IconButton(search, onClick=navigateToSearch, 48×48dp)
│   │   └── elevation: 2dp (scrolled)
│   │
│   └── content: Column (fillMaxSize)
│       │
│       ├── SyncBand (visible when lastSyncAt != null)
│       │   └── Box(bg=surfaceVariant, padding=horizontal 16dp vertical 4dp, fillMaxWidth)
│       │       └── Text("Last synced: Today 8:30 AM", labelSmall, onSurfaceVariant)
│       │
│       ├── TabRow(selectedTabIndex=0)
│       │   ├── Tab(text="Group Savings", icon=people_money)
│       │   ├── Tab(text="Individual", icon=person_money)
│       │   ├── indicatorColor: primary #2E7D32
│       │   └── divider: 1dp, outline
│       │
│       └── LazyColumn (fillMaxSize, pull-to-refresh enabled)
│           ├── item: PullRefreshIndicator (animates when isRefreshing)
│           │
│           ├── item: WeeklyTrendChartGroup
│           │   ├── Surface(bg=surface, elevation=0dp, padding=16dp)
│           │   └── BarChart
│           │       ├── height: 180dp
│           │       ├── bars: 6 (W48–W3)
│           │       ├── barColor: primary #2E7D32
│           │       ├── gridLines: surfaceVariant horizontal
│           │       ├── xAxisLabels: bodySmall, onSurfaceVariant
│           │       ├── yAxisLabels: labelSmall, onSurfaceVariant
│           │       └── contentDescription: "Weekly group savings trend, 6 weeks"
│           │
│           ├── item: CycleProgressCard
│           │   ├── Card(bg=primaryContainer #A6F1A6, cornerRadius=12dp, margin=horizontal 16dp)
│           │   └── Column(padding=16dp)
│           │       ├── Text("Cycle Progress", labelLarge, onPrimaryContainer)
│           │       ├── Spacer(8dp)
│           │       ├── LinearProgressIndicator(
│           │       │   progress=0.177f,
│           │       │   color=primary,
│           │       │   trackColor=primary alpha 0.3,
│           │       │   modifier=fillMaxWidth height 8dp clip RoundedCornerShape(4dp)
│           │       │   )
│           │       ├── Spacer(8dp)
│           │       ├── Row(horizontalArrangement=SpaceBetween)
│           │       │   ├── Text("KES 4,600 collected", bodyMedium, onPrimaryContainer, weight=1f)
│           │       │   └── Text("Target: KES 26,000", bodyMedium, onPrimaryContainer)
│           │       └── Text("17.7% of cycle target reached", labelSmall, onPrimaryContainer alpha 0.8)
│           │
│           ├── item: SectionHeader + TotalChip
│           │   ├── Text("Per-Member Contributions", titleSmall, onSurfaceVariant, padding=horizontal 16dp)
│           │   └── SuggestionChip(
│           │       label="Group total: KES 4,600",
│           │       containerColor=primaryContainer,
│           │       labelColor=onPrimaryContainer,
│           │       modifier=padding horizontal 16dp
│           │       )
│           │
│           └── items: GroupMemberSavingsRow × 5
│               ├── Row(minHeight=72dp, padding=horizontal 16dp vertical 12dp, clickable)
│               ├── Avatar(initials, size=40dp, bg=secondaryContainer)
│               ├── Column(weight=1f, padding=horizontal 12dp)
│               │   ├── Text(member.name, bodyLarge, onSurface)
│               │   └── Text("{N} meetings · Last: KES {amount}", bodySmall, onSurfaceVariant)
│               ├── Column(horizontalAlignment=End)
│               │   ├── Text("KES {total}", labelLarge, primary)
│               │   └── Text("total", labelSmall, onSurfaceVariant)
│               └── Divider(1dp, outline)
```

## Screen: savings-dashboard (INDIVIDUAL tab selected)

```
SavingsDashboardScreen(selectedTab=INDIVIDUAL)
│
└── LazyColumn
    ├── item: WeeklyTrendChartIndividual
    │   └── LineChart
    │       ├── height: 180dp
    │       ├── lineColor: secondary #FF8F00
    │       ├── lineWidth: 2dp
    │       ├── dotColor: secondary #FF8F00, size 6dp
    │       ├── fillColor: secondary alpha 0.12
    │       ├── data: weeklyTrend.individualAmount
    │       └── contentDescription: "Weekly individual savings trend"
    │
    ├── item: IndividualTotalCard
    │   ├── Card(bg=secondaryContainer #FFDDB3, cornerRadius=12dp, margin=horizontal 16dp)
    │   └── Column(padding=16dp)
    │       ├── Text("Total Individual Balances", labelLarge, onSecondaryContainer)
    │       └── Text("KES 4,850", headlineMedium, onSecondaryContainer, fontWeight=Bold)
    │
    ├── item: SectionHeader
    │   └── Text("Member Balances", titleSmall, onSurfaceVariant, padding=horizontal 16dp)
    │
    └── items: IndividualMemberSavingsRow × 5
        ├── Row(minHeight=72dp, padding=horizontal 16dp vertical 12dp, clickable)
        ├── Avatar(initials, size=40dp, bg=tertiaryContainer #D2E4FF)
        ├── Column(weight=1f, padding=horizontal 12dp)
        │   ├── Text(member.name, bodyLarge, onSurface)
        │   └── Row (verticalAlignment=CenterVertically)
        │       ├── TransactionChip [if lastTransaction != null]
        │       │   ├── DEPOSIT: bg=#A6F1A6, text="↑ Deposit", color=onPrimaryContainer
        │       │   └── WITHDRAWAL: bg=#FFDAD6, text="↓ Withdrawal", color=onErrorContainer
        │       └── Text("KES {amount} on {date}", bodySmall, onSurfaceVariant)
        ├── Column(horizontalAlignment=End)
        │   ├── Text("KES {balance}", labelLarge, secondary #FF8F00)
        │   └── Text("balance", labelSmall, onSurfaceVariant)
        └── Divider(1dp, outline)
```

---

# SECTION 3: COMPONENT SPECIFICATIONS

## TopAppBar with Subtitle

```kotlin
TopAppBar(
  title = {
    Column {
      Text(
        text = "Savings",
        style = MaterialTheme.typography.titleLarge,
        color = MaterialTheme.colorScheme.onSurface
      )
      Text(
        text = groupName,  // "Mwangaza Women's Group"
        style = MaterialTheme.typography.bodySmall,
        color = MaterialTheme.colorScheme.onSurfaceVariant
      )
    }
  },
  actions = {
    IconButton(onClick = onSearch) {
      Icon(Icons.Default.Search, contentDescription = "Search members")
    }
  },
  colors = TopAppBarDefaults.topAppBarColors(
    containerColor = MaterialTheme.colorScheme.surface
  )
)
```

## BarChart Component (Group Savings)

```
BarChart specification:
  Container: Surface, bg=surface, elevation=0
  Chart area: Canvas composable, fillMaxWidth, height=180dp
  
  Data binding: weeklyTrend.mapIndexed { index, point -> BarEntry(index.toFloat(), point.groupAmount.toFloat()) }
  
  Bar rendering:
    barColor: primary #2E7D32
    cornerTopRadius: 4dp
    barWidth: (chartWidth - margins - gaps) / barCount
    gap: 8dp between bars
  
  Axes:
    X-axis: weekLabel per bar, bodySmall Noto Sans, onSurfaceVariant
    Y-axis: auto-range 0 to maxAmount × 1.2, labelSmall, onSurfaceVariant
    
  Grid:
    Horizontal lines: 3 lines at 25%, 50%, 75% of max; surfaceVariant color, 1dp
    No vertical grid lines
    
  Animation: bars grow from 0 to full height over 400ms on first composition, decelerated easing
  
  Accessibility: Canvas semanticsRole=image, contentDescription
```

## LineChart Component (Individual Savings)

```
LineChart specification:
  Line color: secondary #FF8F00
  Line width: 2dp stroke
  Dots: filled circles, 6dp diameter, secondary color
  Fill area: below line to x-axis, secondary color alpha 0.12
  Smooth curve: use cubic bezier interpolation (Hermite spline)
  
  Axes: same as BarChart
  
  Animation: line draws from left to right over 600ms on first composition
```

## CycleProgressCard

```
CycleProgressCard specification:
  Background: primaryContainer #A6F1A6
  Corner radius: 12dp (shape.medium)
  Elevation: 0dp (colored bg)
  Margin: horizontal 16dp, vertical 0dp (LazyColumn handles spacing)
  
  Content column padding: 16dp
  
  Title row:
    Icon(savings, 20dp, onPrimaryContainer) + Spacer(8dp) + Text("Cycle Progress", labelLarge, onPrimaryContainer)
  
  Progress bar:
    LinearProgressIndicator
    progress: (cycleCollected / cycleTarget).toFloat()
    color: primary #2E7D32
    trackColor: primary alpha 0.3
    height: 8dp (custom via modifier height)
    corner radius: 4dp
    margin top: 8dp, margin bottom: 8dp
  
  Amounts row:
    Text("KES {cycleCollected} collected", bodyMedium, onPrimaryContainer, weight=1f)
    Text("Target: KES {cycleTarget}", bodyMedium, onPrimaryContainer)
  
  Percent label:
    Text("{percent}% of cycle target reached", labelSmall, onPrimaryContainer, alpha=0.8f)
    
  Demo values:
    cycleCollected = 4,600
    cycleTarget = 26,000
    progress = 0.177f
    label = "17.7% of cycle target reached"
```

## GroupMemberSavingsRow

```
GroupMemberSavingsRow(member: MemberGroupSavingsRow) specification:
  
  Container: Row, clickable(onClick=OnOpenMemberDetail(member.memberId, GROUP_LINKED))
  MinHeight: 72dp
  Padding: horizontal 16dp, vertical 12dp
  VerticalAlignment: CenterVertically
  
  Leading: Avatar circle
    size: 40dp
    background: secondaryContainer #FFDDB3
    text: member initials (first letter of first + first letter of last name)
    text style: labelLarge, onSecondaryContainer #2A1700
    shape: CircleShape
  
  Spacer: 12dp
  
  Center column (weight=1f):
    Text(member.name, bodyLarge, onSurface)
    Text("{member.meetingsContributed} meetings · Last: KES {member.lastContribution}", bodySmall, onSurfaceVariant)
  
  Trailing column (horizontalAlignment=End):
    Text("KES {member.totalContributed}", labelLarge, primary #2E7D32)
    Text("total", labelSmall, onSurfaceVariant)
  
  Divider: 1dp, outline #727971, below row
```

**Demo data for 5 rows**:
| Member | Initials | Meetings | Last | Total |
|--------|---------|---------|------|-------|
| Amara Diallo | AD | 4 | KES 200 | KES 800 |
| Peter Otieno | PO | 4 | KES 300 | KES 1,200 |
| Grace Mwangi | GM | 4 | KES 200 | KES 800 |
| John Mwangi | JM | 4 | KES 300 | KES 1,200 |
| Mary Akinyi | MA | 3 | KES 200 | KES 600 |

## IndividualMemberSavingsRow

```
IndividualMemberSavingsRow(member: MemberIndividualSavingsRow) specification:
  
  Container: Row, clickable(onClick=OnOpenMemberDetail(member.memberId, INDIVIDUAL))
  MinHeight: 72dp
  Padding: horizontal 16dp, vertical 12dp
  VerticalAlignment: CenterVertically
  
  Avatar circle:
    background: tertiaryContainer #D2E4FF
    text color: onTertiaryContainer #001C39
    (blue avatars distinguish individual from group)
  
  Center column (weight=1f):
    Text(member.name, bodyLarge, onSurface)
    Row (verticalAlignment=CenterVertically):
      if member.lastTransaction != null:
        TransactionChip (see below)
        Spacer(4dp)
        Text("KES {|member.lastTransaction|} on {member.lastTransactionDate}", bodySmall, onSurfaceVariant)
      else:
        Text("No transactions yet", bodySmall, onSurfaceVariant)
  
  Trailing column (horizontalAlignment=End):
    Text("KES {member.currentBalance}", labelLarge, secondary #FF8F00)
    Text("balance", labelSmall, onSurfaceVariant)
```

## TransactionChip

```
TransactionChip(type: String, amount: Long) — inline chip, not full-width

DEPOSIT:
  text: "↑ Deposit"
  containerColor: primaryContainer #A6F1A6
  labelColor: onPrimaryContainer #002106
  shape: RoundedCornerShape(4dp)
  padding: horizontal 6dp, vertical 2dp
  style: labelSmall

WITHDRAWAL:
  text: "↓ Withdrawal"
  containerColor: errorContainer #FFDAD6
  labelColor: onErrorContainer #410002
  shape: RoundedCornerShape(4dp)
  padding: horizontal 6dp, vertical 2dp
  style: labelSmall
```

## IndividualTotalCard

```
IndividualTotalCard specification:
  Background: secondaryContainer #FFDDB3
  Corner radius: 12dp
  Margin: horizontal 16dp
  Elevation: 0dp
  
  Column(padding=16dp):
    Text("Total Individual Balances", labelLarge, onSecondaryContainer #2A1700)
    Spacer(8dp)
    Text("KES 4,850", headlineMedium, onSecondaryContainer, fontWeight=Bold)
```

---

# SECTION 4: INTERACTION FLOWS

## Flow 1: Screen Load (cached-then-fresh)

```
SavingsDashboardScreen enters composition
  ↓
LaunchedEffect(Unit): viewModel.loadDashboard(centerId)
  ↓
isLoading = true → ShimmerSkeleton (6 items × 72dp)
  ↓
Parallel reads:
  ├── LocalSavingsDao: getCachedGroupSummary(centerId)
  ├── LocalSavingsDao: getCachedIndividualSummary(centerId)
  └── LocalSavingsDao: getLastSyncAt(centerId)
  ↓
if cachedData != null:
  isLoading = false
  groupSavingsSummary = cachedGroupSummary
  individualSavingsSummary = cachedIndividualSummary
  lastSyncAt = "Today 8:30 AM" (formatted)
  → Content shown immediately
  ↓
  Background fetch (Dispatchers.IO):
    GET /savingsaccounts/{groupSavingsId}/transactions (limit=50)
    GET /clients/{clientId}/accounts × 5 members
    GET /savingsaccounts/{individualSavingsId}/transactions × 5 members
      ↓
    Compute GroupSavingsSummary from transactions
    Compute IndividualSavingsSummary from account balances + transactions
    Compute WeeklyContributionPoints
      ↓
    Update SQLDelight cache
    Emit fresh data to StateFlow
    lastSyncAt = "Just now"
    → Content updates in-place (chart animates to new values)

else (no cache):
  isLoading = true → wait for API
  On success: isLoading = false → Content
  On failure: isLoading = false → Error state (full-screen cloud_off)
```

## Flow 2: Tab Switch

```
User taps "Individual" tab
  ↓
SelectTab(SavingsTab.INDIVIDUAL) action
  ↓
selectedTab = INDIVIDUAL
  ↓
Crossfade composable animates:
  GroupSavingsTabContent fades out (200ms standard easing)
  IndividualSavingsTabContent fades in (200ms)
  ↓
LineChart draws from left to right (600ms, decelerated easing — first time)
IndividualTotalCard slides in from below (300ms, decelerated)
MemberBalances list items stagger in: delay × index × 50ms
```

## Flow 3: Pull to Refresh

```
User pulls down on LazyColumn (drag offset > threshold)
  ↓
isRefreshing = true → PullRefreshIndicator appears (primary green spinner)
  ↓
RefreshDashboard action dispatched
  ↓
if isOnline:
  Re-fetch all API endpoints (same as background fetch in Flow 1)
    ↓
  Success: update content, lastSyncAt = "Just now", isRefreshing = false
  Failure: isRefreshing = false, ShowSnackbar("Failed to refresh — showing cached data")

if !isOnline:
  isRefreshing = false immediately
  ShowSnackbar("Cannot refresh — you're offline")
```

## Flow 4: Member Row Tap (Group Tab)

```
User taps "Amara Diallo" row in Group Savings tab
  ↓
Row ripple effect (standard touch feedback)
  ↓
OnOpenMemberDetail(memberId="101", savingsType=GROUP_LINKED)
  ↓
Event: NavigateToMemberDetail(memberId="101", savingsType=GROUP_LINKED)
  ↓
Navigation to member-savings-detail screen
  (shows Amara Diallo's meeting-by-meeting contribution history)
```

## Flow 5: Member Row Tap (Individual Tab)

```
User taps "Grace Mwangi" row in Individual tab
  ↓
OnOpenMemberDetail(memberId="103", savingsType=INDIVIDUAL)
  ↓
Event: NavigateToMemberDetail(memberId="103", savingsType=INDIVIDUAL)
  ↓
Navigation to member-savings-detail screen
  (shows Grace Mwangi's deposit/withdrawal history, KES 2,200 current balance)
```

## Flow 6: Background Sync Updates Screen

```
SyncManager completes sync (savings transactions synced)
  ↓
LocalSavingsDao emits updated Flow
  ↓
ViewModel collects update via distinctUntilChanged()
  ↓
groupSavingsSummary updates (e.g. new meeting #5 contributions added)
weeklyTrend updates (W4 bar appears in chart)
  ↓
Chart: animated update — W4 bar grows from 0 (300ms)
CycleProgressCard: progress bar animates to new value (400ms)
Member rows: amounts update in-place (150ms)
SyncBand: lastSyncAt = "Just now"
```

---

# SECTION 5: REAL DATA SPECIFICATION

## Group Context
**Group Name**: Mwangaza Women's Group
**centerId**: 7 (Fineract center ID)
**groupSavingsAccountId**: 200 (mandatory savings product: "Group Mandatory Savings")
**Cycle**: Cycle 1 (first 26-week cycle)
**Meetings completed**: 4 (of 26 planned)
**Meeting day**: Wednesday
**Minimum contribution**: KES 200 per meeting per member

## Member Roster

| Member | memberId | Initials | individualSavingsAcctId | Group Savings Product |
|--------|----------|---------|------------------------|----------------------|
| Amara Diallo | 101 | AD | 601 | Individual Voluntary Savings |
| Peter Otieno | 102 | PO | 602 | Individual Voluntary Savings |
| Grace Mwangi | 103 | GM | 603 | Individual Voluntary Savings |
| John Mwangi | 104 | JM | 604 | Individual Voluntary Savings |
| Mary Akinyi | 105 | MA | 605 | Individual Voluntary Savings |

## Group Savings — Per Member Breakdown

Meetings #1–4 contributions:

| Member | Mtg 1 | Mtg 2 | Mtg 3 | Mtg 4 | Total | Meetings |
|--------|-------|-------|-------|-------|-------|---------|
| Amara Diallo | 200 | 200 | 200 | 200 | 800 | 4 |
| Peter Otieno | 300 | 300 | 300 | 300 | 1,200 | 4 |
| Grace Mwangi | 200 | 200 | 200 | 200 | 800 | 4 |
| John Mwangi | 300 | 300 | 300 | 300 | 1,200 | 4 |
| Mary Akinyi | 200 | 200 | 200 | — | 600 | 3 (absent mtg 4) |
| **Total** | **1,200** | **1,200** | **1,200** | **1,000** | **4,600** | |

**Cycle target computation**:
- Min contribution: KES 200 (Amara, Grace, Mary), KES 300 (Peter, John — contribute more)
- Average: (800+1200+800+1200+600)/5 / 4 meetings = KES 920/member average
- CycleTarget set at KES 26,000 (= KES 1,000/meeting × 26 meetings, treasurer-configured)
- cycleCollected: KES 4,600
- cycleProgress: 4,600 / 26,000 = 17.7%

## Individual Savings — Current Balances

| Member | Current Balance | Last Transaction | Last Date | Type |
|--------|----------------|-----------------|-----------|------|
| Amara Diallo | KES 1,500 | KES 500 | 04 May 2026 | DEPOSIT |
| Peter Otieno | KES 750 | KES 200 | 01 May 2026 | DEPOSIT |
| Grace Mwangi | KES 2,200 | KES 500 | 28 Apr 2026 | WITHDRAWAL |
| John Mwangi | KES 400 | KES 100 | 25 Apr 2026 | DEPOSIT |
| Mary Akinyi | KES 0 | — | — | — |

**Total individual balance**: KES 4,850

## Weekly Trend Data (last 6 weeks — W48 2025 through W3 2026)

| Week | Date Range | Group KES | Individual KES |
|------|-----------|-----------|---------------|
| W48 | 24–30 Nov 2025 | 1,000 | 300 |
| W49 | 01–07 Dec 2025 | 1,200 | 500 |
| W50 | 08–14 Dec 2025 | 850 | 200 |
| W51 | 15–21 Dec 2025 | 1,500 | 700 |
| W52 | 22–28 Dec 2025 | 1,200 | 400 |
| W3 | 12–18 Jan 2026 | 1,850 | 650 |

**Note**: W1 and W2 data gaps are expected (school holiday period, group paused meetings).

## Last Sync Timestamp
- lastSyncAt: "2026-05-06T08:30:00Z"
- Displayed: "Today 8:30 AM"

## Full ViewModel State (demo)

```kotlin
SavingsDashboardState(
  selectedTab = SavingsTab.GROUP,
  isLoading = false,
  isRefreshing = false,
  error = null,
  lastSyncAt = "Today 8:30 AM",
  centerId = 7,
  cycleTarget = 26_000L,
  cycleCollected = 4_600L,
  groupSavingsSummary = GroupSavingsSummary(
    totalCollected = 4_600L,
    cycleTarget = 26_000L,
    cycleProgress = 0.177f,
    memberRows = listOf(
      MemberGroupSavingsRow("101", "Amara Diallo", 800L, 200L, 4),
      MemberGroupSavingsRow("102", "Peter Otieno", 1_200L, 300L, 4),
      MemberGroupSavingsRow("103", "Grace Mwangi", 800L, 200L, 4),
      MemberGroupSavingsRow("104", "John Mwangi", 1_200L, 300L, 4),
      MemberGroupSavingsRow("105", "Mary Akinyi", 600L, 200L, 3)
    )
  ),
  individualSavingsSummary = IndividualSavingsSummary(
    totalBalance = 4_850L,
    memberRows = listOf(
      MemberIndividualSavingsRow("101", "Amara Diallo", 1_500L, 500L, "04 May 2026", "DEPOSIT"),
      MemberIndividualSavingsRow("102", "Peter Otieno", 750L, 200L, "01 May 2026", "DEPOSIT"),
      MemberIndividualSavingsRow("103", "Grace Mwangi", 2_200L, -500L, "28 Apr 2026", "WITHDRAWAL"),
      MemberIndividualSavingsRow("104", "John Mwangi", 400L, 100L, "25 Apr 2026", "DEPOSIT"),
      MemberIndividualSavingsRow("105", "Mary Akinyi", 0L, null, null, null)
    )
  ),
  weeklyTrend = listOf(
    WeeklyContributionPoint("W48", 1_000L, 300L),
    WeeklyContributionPoint("W49", 1_200L, 500L),
    WeeklyContributionPoint("W50", 850L, 200L),
    WeeklyContributionPoint("W51", 1_500L, 700L),
    WeeklyContributionPoint("W52", 1_200L, 400L),
    WeeklyContributionPoint("W3", 1_850L, 650L)
  )
)
```

---

# SECTION 6: RESPONSIVE LAYOUT + ADAPTIVE BEHAVIOR

## Compact Layout (0–599dp) — Primary target

```
Screen width: 360dp

TopAppBar: fillMaxWidth, height=64dp (two-line title)
SyncBand: fillMaxWidth, height=24dp
TabRow: fillMaxWidth, height=48dp

LazyColumn: fillMaxWidth, contentPadding=16dp, verticalArrangement=spacedBy(12dp)
  Chart: fillMaxWidth (margin 16dp sides = 328dp chart), height=180dp
  CycleProgressCard: fillMaxWidth (margin 16dp sides = 328dp), cornerRadius=12dp
  GroupTotalChip: wrapContent, left-aligned with 16dp margin
  MemberRows: fillMaxWidth, min 72dp each
```

### Chart bar widths at 360dp
- Available width: 360dp - 32dp margins = 328dp
- 6 bars with 8dp gaps: (328dp - 5×8dp) / 6 = ~47dp per bar

## Medium Layout (600–839dp) — Larger phones, small tablets

```
LazyColumn: maxWidth=520dp, horizontalAlignment=Center
  All cards: maxWidth=520dp
  Member rows: maxWidth=520dp
```

## Expanded Layout (840dp+) — Field officer tablets, desktop Chrome

```
Row(fillMaxSize)
  ├── Column(weight=0.5f, padding=24dp) — Charts + Summary
  │   ├── WeeklyTrendChart (fillMaxWidth within column)
  │   ├── Spacer(16dp)
  │   └── CycleProgressCard or IndividualTotalCard
  │
  └── Column(weight=0.5f, padding=24dp) — Member List
      ├── SectionHeader + TotalChip
      └── LazyColumn: MemberRows (scrollable independently)
```

## Dark Theme Token Mappings

| Light value | Dark equivalent |
|------------|----------------|
| surface #FAFAFA | #1C1C1E |
| primaryContainer #A6F1A6 | #003910 (darkened) |
| onPrimaryContainer #002106 | #A6F1A6 |
| secondaryContainer #FFDDB3 | #422B00 |
| onSecondaryContainer #2A1700 | #FFDDB3 |
| tertiaryContainer #D2E4FF | #004A9C |
| primary #2E7D32 | #48C454 (lightened for dark bg contrast) |
| secondary #FF8F00 | #FFB74D |

## Snackbar Messages

| Trigger | Message | Duration |
|---------|---------|----------|
| Pull-to-refresh offline | "Cannot refresh — you're offline" | short (4s) |
| Pull-to-refresh failed | "Failed to refresh — showing cached data" | long (8s) |
| Background sync complete | "Savings data updated" | short (4s) |
| No member savings accounts | "No savings accounts found for this group" | long (8s) |

## Shimmer Skeleton Specification

```kotlin
SavingsDashboardSkeleton:
  Column(padding=16dp, spacedBy=12dp)
    ShimmerBox(fillMaxWidth, height=180dp, cornerRadius=8dp)  // Chart placeholder
    ShimmerBox(fillMaxWidth, height=80dp, cornerRadius=12dp)  // Cycle card / total card
    ShimmerBox(fillMaxWidth, height=72dp, cornerRadius=0dp)   // Row 1
    ShimmerBox(fillMaxWidth, height=72dp, cornerRadius=0dp)   // Row 2
    ShimmerBox(fillMaxWidth, height=72dp, cornerRadius=0dp)   // Row 3
    ShimmerBox(fillMaxWidth, height=72dp, cornerRadius=0dp)   // Row 4
    ShimmerBox(fillMaxWidth, height=72dp, cornerRadius=0dp)   // Row 5

// ShimmerEffect: infiniteTransition alpha 0.3→1.0→0.3 over 1200ms
// ShimmerBox color: surfaceVariant #DEE5DA
```

## Bottom Navigation Integration

```kotlin
NavigationBarItem(
  icon = { Icon(Icons.Outlined.Savings, "Savings") },
  label = { Text("Savings") },
  selected = currentRoute == "savings"
)
```

No badge — savings dashboard is informational, no alert state. New meeting data shown when screen is opened.

## Analytics Events (Stitch instrumentation hooks)

| User Action | Event Name | Params |
|-------------|-----------|--------|
| Screen opened | screen_viewed | screen_id=savings-dashboard |
| Tab switched to Individual | savings_tab_switched | new_tab=INDIVIDUAL |
| Tab switched to Group | savings_tab_switched | new_tab=GROUP |
| Member row tapped (group) | member_savings_opened | member_id, savings_type=GROUP_LINKED |
| Member row tapped (individual) | member_savings_opened | member_id, savings_type=INDIVIDUAL |
| Pull to refresh | savings_dashboard_refreshed | online=Boolean |

---

# SECTION 7: COMPONENT STATE MATRIX

## Group Savings Progress Card

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| GroupSavingsCard | default | surface (#FAFAFA) | onSurface (#1C1C1C) | outline 1dp (#727971) | elevation 1dp | true | true |
| GroupSavingsCard | pressed | primaryContainer (#A6F1A6) | onPrimaryContainer (#002106) | primary 2dp (#2E7D32) | elevation 0dp | true | true |
| GroupSavingsCard | focused | surface (#FAFAFA) | onSurface (#1C1C1C) | primary 3dp (#2E7D32) | elevation 2dp | true | true |
| GroupSavingsCard | loading | surfaceVariant (#DEE5DA) | onSurfaceVariant (#424942) | none | elevation 0dp | false | true |
| GroupSavingsCard | error | errorContainer (#FFDAD6) | onErrorContainer (#410002) | error 2dp (#D32F2F) | elevation 0dp | true | true |
| GroupSavingsCard | success | primaryContainer (#A6F1A6) | onPrimaryContainer (#002106) | primary 1dp (#2E7D32) | elevation 1dp | true | true |

## Individual Savings Member Row

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| MemberSavingsRow | default | surface (#FAFAFA) | onSurface (#1C1C1C) | none | none | true | true |
| MemberSavingsRow | pressed | secondaryContainer (#FFDDB3) | onSecondaryContainer (#2A1700) | secondary 1dp (#FF8F00) | none | true | true |
| MemberSavingsRow | focused | surface (#FAFAFA) | onSurface (#1C1C1C) | primary 2dp (#2E7D32) | none | true | true |
| MemberSavingsRow | disabled | surfaceVariant (#DEE5DA) | onSurfaceVariant 38% alpha | none | none | false | true |
| MemberSavingsRow | loading | surfaceVariant (#DEE5DA) | onSurfaceVariant (#424942) | none | none | false | true |
| MemberSavingsRow | error | errorContainer (#FFDAD6) | onErrorContainer (#410002) | error 1dp (#D32F2F) | none | true | true |
| MemberSavingsRow | success | primaryContainer (#A6F1A6) | onPrimaryContainer (#002106) | none | none | true | true |

## Tab Row (Group | Individual)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| SavingsTabRow | default (unselected) | surface (#FAFAFA) | onSurfaceVariant (#424942) | outline bottom 1dp | none | true | true |
| SavingsTabRow | selected | surface (#FAFAFA) | primary (#2E7D32) | primary bottom 3dp | none | true | true |
| SavingsTabRow | pressed | primaryContainer (#A6F1A6) | primary (#2E7D32) | primary bottom 3dp | none | true | true |
| SavingsTabRow | focused | surface (#FAFAFA) | primary (#2E7D32) | primary bottom 3dp + focus ring | none | true | true |
| SavingsTabRow | disabled | surfaceVariant (#DEE5DA) | onSurfaceVariant 38% alpha | none | none | false | true |

## Sync / Refresh FAB

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| RefreshFAB | default | primaryContainer (#A6F1A6) | onPrimaryContainer (#002106) | none | elevation 6dp | true | true |
| RefreshFAB | pressed | primary (#2E7D32) | onPrimary (#FFFFFF) | none | elevation 2dp | true | true |
| RefreshFAB | focused | primaryContainer (#A6F1A6) | onPrimaryContainer (#002106) | primary 3dp ring | elevation 6dp | true | true |
| RefreshFAB | loading | primaryContainer (#A6F1A6) | onPrimaryContainer 60% alpha | none | elevation 4dp | false | true |
| RefreshFAB | disabled | surfaceVariant (#DEE5DA) | onSurfaceVariant 38% alpha | none | elevation 0dp | false | true |

## Balance Amount Chip (group total / individual balance)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| BalanceChip (group) | default | primaryContainer (#A6F1A6) | onPrimaryContainer (#002106) | none | none | true | true |
| BalanceChip (individual) | default | secondaryContainer (#FFDDB3) | onSecondaryContainer (#2A1700) | none | none | true | true |
| BalanceChip | loading | surfaceVariant (#DEE5DA) | onSurfaceVariant (#424942) shimmer | none | none | false | true |
| BalanceChip | error | errorContainer (#FFDAD6) | onErrorContainer (#410002) | error 1dp (#D32F2F) | none | true | true |

---

# SECTION 8: API FAILURE & RECOVERY PLAYBOOK

## Endpoint: GET /savingsaccounts/group/{groupId}

| Failure | UX Response | Recovery |
|---------|-------------|----------|
| Network timeout | Show cached data with amber banner "Last updated {time}" | Exponential backoff retry: 1s → 2s → 4s, max 3 attempts |
| 401 Unauthorized | Navigate to LoginScreen; preserve local SyncQueue; show snackbar "Session expired — please log in" | Post-login, auto-retry the request; restore scroll position |
| 404 Not Found | Show stale-data warning card "Group savings data unavailable"; show re-sync prompt | Offer "Contact Support" deep link; log event `savings_group_404` |
| 500 Server Error | Snackbar "Unable to load group savings. Try again." (long, 8s) | Retry button in snackbar; after 2 manual retries, show "Still having trouble? Check your connection." |
| Offline | Show last-known balance from local Room cache; display "Offline — showing cached data" banner (amber) | Auto-retry on reconnect via NetworkMonitor callback |

## Endpoint: GET /savingsaccounts/individual/{memberId}

| Failure | UX Response | Recovery |
|---------|-------------|----------|
| Network timeout | Skeleton loader persists for ≤3s, then shows stale value from local DB | Retry: 1s → 2s → 4s; show "Slow connection" text after attempt 2 |
| 401 Unauthorized | Navigate to LoginScreen; preserve member list state in SavedStateHandle | Auto-restore after login via NavBackStackEntry args |
| 404 Not Found | MemberSavingsRow shows dashes for balance, warning icon (Icons.Outlined.Warning, amber) | Row tap opens snackbar "Balance unavailable for {member_name}" |
| 500 Server Error | Snackbar "Could not fetch balance for {member_name}. Try again." | Member row retry on next pull-to-refresh |
| Offline | Display last known individual balance from local cache; amber offline badge on member avatar | Queue refresh request in SyncQueue type=FETCH; auto-execute on reconnect |

## Endpoint: POST /savingsaccounts/group/{groupId}/transactions (contribution)

| Failure | UX Response | Recovery |
|---------|-------------|----------|
| Network timeout | Queue to SyncQueue with type=CONTRIBUTION; show "Saved offline — will sync when online" | Auto-retry on reconnect (exponential: 30s → 2m → 10m) |
| 401 Unauthorized | Navigate to LoginScreen; preserve contribution form data in StateFlow | Resume contribution flow post-login with pre-filled amount |
| 404 Not Found | Error dialog: "Account not found. Contact your administrator." | Cannot recover — show helpdesk contact action |
| 500 Server Error | Snackbar "Contribution failed. Saved locally — retrying automatically." | WorkManager retry with REPLACE policy |
| Offline | Immediately queue to SyncQueue; show confirmation "KES {amount} saved for {member_name} — will sync when online" | Optimistic UI update: add row locally, mark with pending badge |
| Validation error (422) | Inline error on amount field: "Minimum contribution is KES 50.00" | Highlight field with error border; request focus |

## SyncQueue Auto-Retry Protocol

```
Connectivity restored →
  1. Drain SyncQueue ordered by created_at ASC
  2. For each item: attempt POST/PUT
  3. On success: mark SYNCED, update local cache
  4. On failure: increment retry_count
     - retry_count < 3: re-queue with backoff
     - retry_count >= 3: mark FAILED, notify user via NotificationManager channel "sync_failures"
  5. Emit SyncResult to StateFlow<SyncState>
```

---

# SECTION 9: SCREEN READER & ACCESSIBILITY DEEP DIVE

## Savings Dashboard Screen — Focus Order

1. TopAppBar back/up button (if nested) — contentDescription = "Navigate back"
2. TopAppBar title "Savings Dashboard" — role = Heading
3. "Mwangaza Women's Group" group name chip — contentDescription = "Group: Mwangaza Women's Group"
4. GroupSavingsCard progress section — contentDescription = "Group savings: KES 48,500 of KES 60,000 target. 80% complete."
5. Tab row — role = Tab; "Group Savings tab, 1 of 2, selected" / "Individual Savings tab, 2 of 2"
6. Tab content area — first interactive row receives focus on tab switch
7. MemberSavingsRow (Amara Diallo) — contentDescription = "Amara Diallo, individual savings KES 3,200. Tap to view details."
8. MemberSavingsRow (Grace Mwangi) — contentDescription = "Grace Mwangi, individual savings KES 4,750. Tap to view details."
9. MemberSavingsRow (Peter Otieno) — contentDescription = "Peter Otieno, individual savings KES 2,100. Tap to view details."
10. MemberSavingsRow (Mary Akinyi) — contentDescription = "Mary Akinyi, individual savings KES 5,600. Tap to view details."
11. Pull-to-refresh handle — contentDescription = "Pull down to refresh savings data"
12. Bottom Navigation Bar items — each with localized label and role = Tab

## TalkBack Announcement Strings

| Element | TalkBack String |
|---------|----------------|
| GroupSavingsCard (loading) | "Loading group savings data" |
| GroupSavingsCard (loaded) | "Mwangaza Women's Group has saved KES 48,500 of their KES 60,000 target" |
| GroupSavingsCard (error) | "Unable to load group savings. Double-tap to retry." |
| MemberSavingsRow | "{name}, balance KES {amount}, double-tap to open savings details" |
| Progress bar (LinearProgressIndicator) | "Savings progress: 80 percent" |
| Tab switch | "Individual Savings tab selected, showing {count} members" |
| BalanceChip (group) | "Group total: KES {amount}" |
| BalanceChip (individual) | "Personal balance: KES {amount}" |
| OfflineBanner | "You are offline. Showing data last updated {relative_time}" |
| RefreshFAB | "Refresh savings data" |

## Content Descriptions — All Icons

| Icon | Composable | contentDescription |
|------|-----------|-------------------|
| Icons.Outlined.Savings | BottomNavItem | "Savings" |
| Icons.Outlined.Group | GroupSavingsCard header | "Group" |
| Icons.Outlined.Person | MemberSavingsRow avatar placeholder | "{member_name}'s avatar" |
| Icons.Outlined.TrendingUp | Progress indicator chip | "Progress trending up" |
| Icons.Outlined.Warning | Stale data / error badge | "Warning: data may be outdated" |
| Icons.Outlined.Sync | RefreshFAB | "Sync savings data" |
| Icons.Outlined.CheckCircle | Synced state indicator | "Data is up to date" |
| Icons.Outlined.CloudOff | Offline indicator | "No internet connection" |
| Icons.Outlined.ArrowForward | MemberSavingsRow trailing | "View details for {member_name}" |

## Live Region Announcements

```kotlin
// Loading state
Box(modifier = Modifier.semantics {
    liveRegion = LiveRegionMode.Polite
    contentDescription = if (isLoading) "Loading savings data" else "Savings data loaded"
})

// Error state
Text(
    text = errorMessage,
    modifier = Modifier.semantics {
        liveRegion = LiveRegionMode.Assertive
    }
)
```

## WCAG AA Contrast Ratios

| Foreground | Background | Ratio | Pass AA (4.5:1 normal / 3:1 large) |
|------------|------------|-------|-------------------------------------|
| onPrimary #FFFFFF | primary #2E7D32 | 7.1:1 | Pass (AA + AAA) |
| onPrimaryContainer #002106 | primaryContainer #A6F1A6 | 8.2:1 | Pass (AA + AAA) |
| onSecondary #FFFFFF | secondary #FF8F00 | 3.3:1 | Pass (large text / UI only) |
| onSecondaryContainer #2A1700 | secondaryContainer #FFDDB3 | 9.4:1 | Pass (AA + AAA) |
| onSurface #1C1C1C | surface #FAFAFA | 16.1:1 | Pass (AA + AAA) |
| onSurfaceVariant #424942 | surfaceVariant #DEE5DA | 5.9:1 | Pass (AA) |
| error #D32F2F | surface #FAFAFA | 5.4:1 | Pass (AA) |
| onErrorContainer #410002 | errorContainer #FFDAD6 | 12.4:1 | Pass (AA + AAA) |

## Color-Blind Safe Status States

All status states (synced / pending / failed / offline) use BOTH color AND icon/shape:
- Synced: green (#2E7D32) + Icons.Outlined.CheckCircle
- Pending: amber (#FF8F00) + Icons.Outlined.Schedule (clock icon)
- Failed: red (#D32F2F) + Icons.Outlined.ErrorOutline (triangle with !)
- Offline: grey (#727971) + Icons.Outlined.CloudOff

---

# SECTION 10: ANIMATION & MOTION SPEC

## Screen Enter / Exit Animations

| Screen | Enter | Exit |
|--------|-------|------|
| SavingsDashboard | fadeIn(tween(300)) + slideInVertically(+80px → 0, tween(300, easing=EaseOutCubic)) | fadeOut(tween(200)) |
| MemberSavingsDetail | slideInHorizontally(+full → 0, tween(350, easing=EmphasizedDecelerate)) | slideOutHorizontally(0 → -full, tween(300, easing=EmphasizedAccelerate)) |
| ContributionBottomSheet | slideInVertically(+full → 0, tween(350, easing=EmphasizedDecelerate)) | slideOutVertically(0 → +full, tween(300)) |

## Loading Skeleton Shimmer

```kotlin
// Shimmer gradient spec
val shimmerColors = listOf(
    surfaceVariant.copy(alpha = 0.9f),  // #DEE5DA
    surfaceVariant.copy(alpha = 0.3f),  // #DEE5DA 30%
    surfaceVariant.copy(alpha = 0.9f),
)
// Direction: left → right (270° angle)
// Duration: 1200ms per cycle
// Loop: infiniteRepeatable(RepeatMode.Restart)
// Applied to: GroupSavingsCard skeleton, MemberSavingsRow skeletons (3 rows shown)
```

## State Transition Animations

| Transition | Duration | Easing |
|------------|----------|--------|
| Loading → Loaded (card appears) | 200ms | FastOutSlowIn (standard) |
| Error → Retry loading | fade 150ms out + 150ms in | LinearEasing |
| Tab switch content swap | crossfade 150ms | LinearEasing |
| MemberSavingsRow expand/collapse | 250ms height + 200ms fade | EaseInOutCubic |
| BalanceChip number update (amount change) | 300ms countUp animation | EaseOutCubic |
| OfflineBanner enter | slideInVertically 200ms from top | EaseOutCubic |
| OfflineBanner exit | slideOutVertically 150ms to top | EaseInCubic |

## Pull-to-Refresh Spec

```kotlin
PullRefreshIndicator(
    refreshing = isRefreshing,
    state = pullRefreshState,
    // Color: primary #2E7D32
    // Background: surface #FAFAFA
    // Scale: animateFloatAsState 0f → 1f, 200ms EaseOutBack
    // Threshold: 64dp
)
```

## BottomSheet: Contribution Entry

- Trigger: FAB tap or "Record Contribution" action
- Enter: `slideInVertically(fullHeight → 0, tween(350, easing=EmphasizedDecelerateEasing))`
- Drag handle: visible, 32dp wide, 4dp tall, outline color
- Scrim: black 32% alpha, fadeIn 250ms
- Exit on swipe-down: `slideOutVertically(0 → fullHeight, tween(300))`
- Scrim fadeOut: 200ms

---

# SECTION 11: TEST & QA ANNOTATIONS

## UI Test Tags

| Composable | testTag |
|-----------|---------|
| GroupSavingsCard (loaded) | `"GroupSavingsCard_Loaded"` |
| GroupSavingsCard (loading) | `"GroupSavingsCard_Loading"` |
| GroupSavingsCard (error) | `"GroupSavingsCard_Error"` |
| SavingsTabRow | `"SavingsTabRow"` |
| Tab — Group | `"SavingsTab_Group"` |
| Tab — Individual | `"SavingsTab_Individual"` |
| MemberSavingsRow (by member id) | `"MemberSavingsRow_{memberId}"` |
| BalanceChip — group | `"BalanceChip_Group"` |
| BalanceChip — individual | `"BalanceChip_Individual_{memberId}"` |
| OfflineBanner | `"OfflineBanner"` |
| RefreshFAB | `"RefreshFAB"` |
| ErrorSnackbar | `"ErrorSnackbar"` |
| PullRefreshIndicator | `"PullRefreshIndicator"` |

## Required Test Scenarios

### Screen: SavingsDashboard — Group Tab

**Given** the user is a group treasurer for Mwangaza Women's Group  
**When** the screen loads with a valid network connection  
**Then** GroupSavingsCard shows group total KES 48,500 and individual members list loads within 3s

---

**Given** the user is on the Group tab  
**When** they pull down to refresh  
**Then** PullRefreshIndicator appears in primary green, network call is made, and data updates within 3s

---

**Given** the device is offline  
**When** the user navigates to SavingsDashboard  
**Then** OfflineBanner is visible, cached data displays correctly, and RefreshFAB is disabled

---

**Given** the group savings API returns HTTP 500  
**When** the user is viewing the GroupSavingsCard  
**Then** ErrorSnackbar with message "Unable to load group savings. Try again." appears and retry button is visible

---

**Given** the user taps a member row (e.g. Amara Diallo)  
**When** the navigation transition completes  
**Then** MemberSavingsDetail screen shows Amara Diallo's individual balance and transaction history

### Screen: SavingsDashboard — Individual Tab

**Given** there are 0 members with savings accounts  
**When** the Individual tab is selected  
**Then** empty state illustration with text "No individual savings accounts yet" is displayed (testTag="EmptyState_Individual")

---

**Given** there is exactly 1 member (Grace Mwangi, KES 4,750)  
**When** the Individual tab is selected  
**Then** exactly one MemberSavingsRow renders with correct name and amount

---

**Given** there are 50+ members in the group  
**When** the Individual tab renders  
**Then** list is scrollable, all items are reachable via scroll, and no performance jank (frame drops <5) on Pixel 4a equivalent

---

**Given** a member name is 50+ characters (e.g. "Amara Bintou Diallo Kouyaté Traoré Dembélé-Sissoko")  
**When** their MemberSavingsRow renders  
**Then** name truncates with ellipsis at 1 line, full name accessible via contentDescription

## Edge Cases

- Empty group (0 members): GroupSavingsCard shows KES 0.00, "No contributions yet" subtitle
- Single member group: Individual tab shows 1 row, group card shows that member's contribution only
- All members on zero balance: BalanceChips show "KES 0.00" — no crash, no missing UI
- Amount exceeds KES 9,999,999.99: format as "KES 10,000,000.00" — no overflow in chip
- Expired auth mid-session: login redirect preserves full nav stack, restores on return

---

# SECTION 12: i18n / LOCALIZATION SPEC

## String Keys with Translations

| Key | EN | SW (Swahili) | FR (French) |
|-----|----|--------------|-------------|
| `savings_screen_title` | "Savings Dashboard" | "Dashibodi ya Akiba" | "Tableau des Économies" |
| `savings_tab_group` | "Group" | "Kikundi" | "Groupe" |
| `savings_tab_individual` | "Individual" | "Binafsi" | "Individuel" |
| `savings_group_total_label` | "Group Savings Total" | "Jumla ya Akiba ya Kikundi" | "Total des Économies du Groupe" |
| `savings_individual_balance_label` | "Individual Balance" | "Salio la Kibinafsi" | "Solde Individuel" |
| `savings_target_label` | "Target" | "Lengo" | "Objectif" |
| `savings_progress_label` | "{percent}% of target" | "{percent}% ya lengo" | "{percent}% de l'objectif" |
| `savings_member_count_label` | "{count} members" | "wanachama {count}" | "{count} membres" |
| `savings_offline_banner` | "Offline — showing cached data" | "Nje ya mtandao — inaonyesha data iliyohifadhiwa" | "Hors ligne — données en cache" |
| `savings_error_group` | "Unable to load group savings. Try again." | "Imeshindwa kupakia akiba ya kikundi. Jaribu tena." | "Impossible de charger les économies du groupe. Réessayez." |
| `savings_error_individual` | "Could not fetch balance for {name}. Try again." | "Imeshindwa kupata salio la {name}. Jaribu tena." | "Impossible de récupérer le solde de {name}. Réessayez." |
| `savings_last_updated` | "Last updated {time}" | "Ilisasishwa mara ya mwisho {time}" | "Dernière mise à jour {time}" |
| `savings_contribution_success` | "KES {amount} contribution recorded for {name}" | "Mchango wa KES {amount} umerekodiwa kwa {name}" | "Contribution de KES {amount} enregistrée pour {name}" |
| `savings_empty_individual` | "No individual savings accounts yet" | "Hakuna akaunti za akiba za kibinafsi bado" | "Aucun compte d'épargne individuel pour l'instant" |
| `savings_refresh_label` | "Refresh savings data" | "Onyesha upya data ya akiba" | "Actualiser les données d'épargne" |
| `savings_group_name` | "Mwangaza Women's Group" | "Kikundi cha Wanawake Mwangaza" | "Groupe des Femmes Mwangaza" |

## Number Formatting — KES

| Amount | Formatted (en-KE) |
|--------|-------------------|
| 1000 | KES 1,000.00 |
| 48500 | KES 48,500.00 |
| 1234.5 | KES 1,234.50 |
| 9999999.99 | KES 9,999,999.99 |
| 0 | KES 0.00 |

```kotlin
val numberFormat = NumberFormat.getCurrencyInstance(Locale("en", "KE"))
// Produces: KES 48,500.00
// Ensure currency symbol is always "KES " (with trailing space)
```

## Date Formatting — en-KE Locale

| Format | Pattern | Example |
|--------|---------|---------|
| Short date | dd/MM/yyyy | 06/05/2026 |
| Long date | d MMMM yyyy | 6 May 2026 |
| Relative time (recent) | "X minutes ago" / "dakika X zilizopita" | "5 minutes ago" |
| Relative time (today) | "Today at HH:mm" / "Leo saa HH:mm" | "Today at 14:30" |
| Relative time (yesterday) | "Yesterday" / "Jana" / "Hier" | "Yesterday" |

```kotlin
val dateFormat = SimpleDateFormat("dd/MM/yyyy", Locale("en", "KE"))
// For TalkBack: "sixth of May twenty twenty-six" via AccessibilityDateFormatter
```

## RTL Support Note

Swahili and French are LTR — no RTL layout changes required for these locales. If Hindi is added in a future sprint, enable `layoutDirection = LayoutDirection.Ltr` override for currency chips (currency symbol always left-anchored per KES convention).

## Plural Rules (English / Swahili)

For member count labels: English uses standard s/es plurals (`1 member`, `3 members`). Swahili uses consistent form: `mwanachama 1`, `wanachama 3` — use Android quantity strings with `one` and `other` quantities for EN; use `other` for all SW counts. French: `1 membre`, `3 membres` — standard French singular/plural rules apply.
