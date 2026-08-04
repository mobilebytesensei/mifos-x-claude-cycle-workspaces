# Field Officer View — Stitch Prompt Specification
**Feature**: field-officer-view | **Screen**: field-officer-dashboard
**Requirement**: FR-009
**Stitch project**: MifosSave / mifos-x-group-banking
**Total sections**: 6

---

# SECTION 1: DESIGN SYSTEM CONTEXT

## Application Identity
MifosSave is a VSLA group banking app. The field officer dashboard is the portfolio supervision view — a field officer at a Fineract-powered microfinance institution monitors 5–20 VSLA groups across a region. The design must communicate portfolio health at a glance: green for healthy groups, amber for groups needing attention, red for groups in crisis. The four KPI cards use the full MD3 tonal palette — one color per KPI — to create a clear visual hierarchy without using the same color for everything.

## Material Design 3 Token System

### Color Palette (all hex values exact)

#### Primary — VSLA Green (GREEN health, groups KPI, active filter chip)
- primary: #2E7D32
- onPrimary: #FFFFFF
- primaryContainer: #A6F1A6
- onPrimaryContainer: #002106

#### Secondary — Amber (AMBER health, members KPI)
- secondary: #FF8F00
- onSecondary: #FFFFFF
- secondaryContainer: #FFDDB3
- onSecondaryContainer: #2A1700

#### Tertiary — Trust Blue (savings KPI, trusted financial data)
- tertiary: #1565C0
- onTertiary: #FFFFFF
- tertiaryContainer: #D2E4FF
- onTertiaryContainer: #001C39

#### Error — Alert Red (RED health, loans outstanding KPI)
- error: #D32F2F
- onError: #FFFFFF
- errorContainer: #FFDAD6
- onErrorContainer: #410002

#### Neutral
- surface: #FAFAFA
- onSurface: #1C1C1C
- surfaceVariant: #DEE5DA
- onSurfaceVariant: #424942
- outline: #727971
- outlineVariant: #C2C9BD

### Typography Scale (Noto Sans, scale_style: large)

| Style | Size (sp) | Weight | Usage |
|-------|-----------|--------|-------|
| titleLarge | 22 | 500 | TopAppBar title |
| headlineSmall | 24 | 400 | KPI values (8, 94, KES 142K) |
| titleSmall | 14 | 500 | Section headers ("Groups (8)") |
| labelLarge | 14 | 500 | KPI card labels, button label |
| labelMedium | 12 | 500 | Filter chip labels |
| labelSmall | 11 | 500 | Health indicator text |
| bodyLarge | 16 | 400 | Group name in health card |
| bodyMedium | 14 | 400 | — |
| bodySmall | 12 | 400 | Group card stats, subtitles |

### Spacing Scale
| Token | dp | Usage |
|-------|----|-------|
| xs | 4 | Health dot internal |
| sm | 8 | Card grid gap, chip spacing |
| md | 12 | Card padding, row padding |
| lg | 16 | Page margin, chip row padding |
| xl | 24 | Section gap |

### Shape Scale
| Token | Corner Radius | Usage |
|-------|--------------|-------|
| small | 8dp | Filter chip |
| medium | 12dp | KPI cards, group health cards |
| full | 9999dp | Health indicator dot (circle) |

### Elevation
| Level | dp | Usage |
|-------|----|-------|
| level_0 | 0dp | KPI cards (colored bg, no shadow needed) |
| level_2 | 3dp | Group health cards, TopAppBar (scrolled) |

### Motion Timing
| Token | Duration | Easing | Usage |
|-------|----------|--------|-------|
| short_4 | 200ms | Standard | Filter chip select/deselect |
| medium_1 | 250ms | Emphasized | Group card list filter transition |
| medium_2 | 300ms | Emphasized | KPI value number count-up animation |
| long_1 | 450ms | Decelerated | RED health dot pulse (attention) |
| shimmer_cycle | 1200ms | Linear | Loading skeleton |

### Accessibility
- Min touch target: 48dp (group cards, filter chips, action buttons)
- KPI cards: contentDescription with full value
- Health indicators: text label + color (not color alone)
- Filter chips: selected state announced by screen reader
- Export button: announces purpose and current state (exporting or idle)

### Breakpoints
| Name | Range | Behavior |
|------|-------|----------|
| compact | 0–599dp | KPI 2-column grid, group cards full width |
| medium | 600–839dp | KPI 4-column grid (1 row), group cards full width |
| expanded | 840dp+ | KPI 4-col, group cards 2-column grid |

---

# SECTION 2: SCREEN COMPONENT TREES

## Field Officer Dashboard — Full Component Tree (5 groups shown)

```
FieldOfficerDashboardScreen(
  isLoading=false, kpiTotalGroups=8, kpiTotalMembers=94,
  kpiTotalSavings=142000L, kpiLoansOutstanding=87500L,
  groups=5 GroupHealthCards, filteredGroups=5 (no active filter)
)
├── Scaffold
│   ├── TopAppBar
│   │   ├── title: Column
│   │   │   ├── Text("Field Dashboard", titleLarge, onSurface)
│   │   │   └── Text("James Otieno · Nairobi Branch", bodySmall, onSurfaceVariant)
│   │   ├── actions:
│   │   │   ├── IconButton(notifications, onClick=navigateToNotifications, 48×48dp)
│   │   │   └── IconButton(share, onClick=OnExportReport, 48×48dp)
│   │   └── elevation: 2dp (scrolled)
│   │
│   └── content: LazyColumn(fillMaxSize, contentPadding=PaddingValues(bottom=16dp))
│       │
│       ├── item: KpiCardGrid
│       │   └── LazyVerticalGrid(
│       │       columns=GridCells.Fixed(2),
│       │       contentPadding=PaddingValues(horizontal=16dp, vertical=12dp),
│       │       horizontalArrangement=spacedBy(8dp),
│       │       verticalArrangement=spacedBy(8dp),
│       │       userScrollEnabled=false
│       │       )
│       │       ├── KpiCard(label="Total Groups", value="8", bg=primaryContainer, icon=group)
│       │       ├── KpiCard(label="Total Members", value="94", bg=secondaryContainer, icon=people)
│       │       ├── KpiCard(label="Total Savings", value="KES 142K", bg=tertiaryContainer, icon=savings)
│       │       └── KpiCard(label="Loans Outstanding", value="KES 87.5K", bg=errorContainer, icon=account_balance)
│       │
│       ├── item: FilterChipRow
│       │   └── Row(
│       │       modifier=Modifier.fillMaxWidth().padding(horizontal=16dp),
│       │       horizontalArrangement=Arrangement.spacedBy(8dp)
│       │       )
│       │       ├── FilterChip("Region", selectedRegion, onFilterRegion, trailing=DropdownIcon)
│       │       ├── FilterChip("Status", selectedStatus, onFilterStatus, trailing=DropdownIcon)
│       │       └── FilterChip("Overdue", selectedOverdueFilter, onFilterOverdue, trailing=DropdownIcon)
│       │
│       ├── item: ExportReportRow
│       │   └── Row(modifier=Modifier.fillMaxWidth().padding(horizontal=16dp), horizontalArrangement=End)
│       │       └── OutlinedButton(
│       │           text=if(isExporting) "Exporting..." else "Export Report",
│       │           icon=if(isExporting) CircularProgressIndicator else Icon(upload),
│       │           onClick=OnExportReport,
│       │           enabled=!isExporting,
│       │           border=BorderStroke(1.dp, primary),
│       │           contentColor=primary,
│       │           height=48dp
│       │           )
│       │
│       ├── item: GroupsSectionHeader
│       │   └── Text(
│       │       "Groups (${filteredGroups.size})",
│       │       titleSmall,
│       │       onSurfaceVariant,
│       │       modifier=Modifier.padding(start=16dp, top=8dp, end=16dp, bottom=4dp)
│       │       )
│       │
│       └── items: GroupHealthCardRow × filteredGroups.size
│           └── GroupHealthCard (per group — see component spec below)
│               ├── Card(cornerRadius=12dp, elevation=2dp, margin=horizontal 16dp vertical 4dp)
│               │   └── [See GroupHealthCard spec in Section 3]
│               └── [Spacer between cards: 8dp from LazyColumn spacedBy]
│
└── [RegionFilterDropdown — if selectedRegion chip tapped]
    └── DropdownMenu(...)
        ├── DropdownMenuItem("Nairobi")
        ├── DropdownMenuItem("Mombasa")
        ├── DropdownMenuItem("Kisumu")
        └── DropdownMenuItem("Nakuru")
```

---

# SECTION 3: COMPONENT SPECIFICATIONS

## KpiCard

```kotlin
@Composable
fun KpiCard(
  label: String,
  value: String,
  containerColor: Color,
  contentColor: Color,
  icon: ImageVector
) {
  Card(
    shape = RoundedCornerShape(12.dp),
    colors = CardDefaults.cardColors(containerColor = containerColor),
    elevation = CardDefaults.cardElevation(0.dp),
    modifier = Modifier.fillMaxWidth().heightIn(min = 80.dp)
  ) {
    Column(modifier = Modifier.padding(12.dp)) {
      Row(verticalAlignment = Alignment.CenterVertically) {
        Icon(icon, contentDescription = null, tint = contentColor, modifier = Modifier.size(20.dp))
        Spacer(4.dp)
        Text(label, style = labelLarge, color = contentColor)
      }
      Spacer(4.dp)
      // Animated count-up effect on load (300ms)
      AnimatedContent(
        targetState = value,
        transitionSpec = { slideInVertically { it } + fadeIn() togetherWith slideOutVertically { -it } + fadeOut() }
      ) { displayValue ->
        Text(displayValue, style = headlineSmall, color = contentColor, fontWeight = FontWeight.Bold)
      }
    }
  }
}
```

### KPI Cards Demo Values

| Card | label | value | containerColor | contentColor | icon |
|------|-------|-------|---------------|-------------|------|
| Groups | "Total Groups" | "8" | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | group |
| Members | "Total Members" | "94" | secondaryContainer #FFDDB3 | onSecondaryContainer #2A1700 | people |
| Savings | "Total Savings" | "KES 142K" | tertiaryContainer #D2E4FF | onTertiaryContainer #001C39 | savings |
| Loans | "Loans Outstanding" | "KES 87.5K" | errorContainer #FFDAD6 | onErrorContainer #410002 | account_balance |

**Value formatting**:
- KES amounts ≥ 1,000: format as "KES {n}K" (e.g. 142000 → "KES 142K")
- KES amounts ≥ 1,000,000: format as "KES {n}M"
- Counts: plain integer ("8", "94")

## GroupHealthCard

```kotlin
@Composable
fun GroupHealthCard(
  group: GroupHealthCard,
  onClick: () -> Unit
) {
  val (healthColor, cardBgTint) = when (group.healthLevel) {
    HealthLevel.GREEN -> Pair(primary, surface)  // surface background — no tint for healthy
    HealthLevel.AMBER -> Pair(secondary, surface)
    HealthLevel.RED -> Pair(error, errorContainer.copy(alpha = 0.3f))  // subtle red tint
  }

  Card(
    shape = RoundedCornerShape(12.dp),
    colors = CardDefaults.cardColors(containerColor = cardBgTint),
    elevation = CardDefaults.cardElevation(2.dp),
    modifier = Modifier
      .fillMaxWidth()
      .padding(horizontal = 16.dp, vertical = 4.dp)
      .clickable(onClick = onClick)
  ) {
    Row(
      modifier = Modifier.fillMaxWidth().padding(12.dp),
      verticalAlignment = Alignment.CenterVertically
    ) {
      // Health indicator dot (pulsing for RED on first render)
      Box(
        modifier = Modifier
          .size(8.dp)
          .background(healthColor, CircleShape)
          .let {
            if (group.healthLevel == HealthLevel.RED) {
              it.pulseAnimation()  // scale 1.0→1.3→1.0, 600ms, once on load
            } else it
          }
      )

      Spacer(8.dp)

      Column(modifier = Modifier.weight(1f)) {
        Text(group.groupName, bodyLarge, onSurface)
        Text(
          "${group.region} · ${group.memberCount} members",
          bodySmall,
          onSurfaceVariant
        )
        Text(
          "KES ${group.totalSavings.formatShort()} savings · ${(group.overdueRate * 100).roundToInt()}% overdue",
          bodySmall,
          onSurfaceVariant
        )
      }

      Icon(
        Icons.AutoMirrored.Filled.ChevronRight,
        contentDescription = "Open ${group.groupName}",
        tint = onSurfaceVariant,
        modifier = Modifier.size(20.dp)
      )
    }
  }
}
```

### GroupHealthCard Visual States

**GREEN (Mwangaza Women's Group — 0% overdue)**:
```
Card bg: surface #FAFAFA
Health dot: #2E7D32 filled circle
Group name: onSurface
Stats: onSurfaceVariant
```

**AMBER (Tumaini Savings Circle — 12% overdue)**:
```
Card bg: surface #FAFAFA
Health dot: #FF8F00 filled circle
Group name: onSurface
Stats: onSurfaceVariant
```

**RED (Umoja Welfare Group — 25% overdue)**:
```
Card bg: errorContainer #FFDAD6 at 30% alpha = very subtle pink
Health dot: #D32F2F filled circle (pulses once on screen load — attention signal)
Group name: onSurface
Stats: onSurfaceVariant (NOT error red — red used only for health dot and bg tint)
```

## FilterChip (3 chips)

```kotlin
@Composable
fun DashboardFilterChip(
  label: String,
  selectedValue: String?,
  onClick: () -> Unit,
  onClear: () -> Unit
) {
  val isSelected = selectedValue != null

  FilterChip(
    selected = isSelected,
    onClick = onClick,
    label = {
      Text(
        text = if (isSelected) "$label: $selectedValue" else label,
        style = MaterialTheme.typography.labelMedium
      )
    },
    leadingIcon = if (isSelected) {
      { Icon(Icons.Default.Check, contentDescription = null, modifier = Modifier.size(16.dp)) }
    } else null,
    trailingIcon = if (isSelected) {
      { IconButton(onClick = onClear, modifier = Modifier.size(20.dp)) {
        Icon(Icons.Default.Close, contentDescription = "Clear $label filter", modifier = Modifier.size(12.dp))
      }}
    } else {
      { Icon(Icons.Default.ArrowDropDown, contentDescription = null, modifier = Modifier.size(16.dp)) }
    },
    colors = FilterChipDefaults.filterChipColors(
      containerColor = surfaceVariant,
      labelColor = onSurfaceVariant,
      selectedContainerColor = primaryContainer,
      selectedLabelColor = onPrimaryContainer,
      selectedLeadingIconColor = onPrimaryContainer
    ),
    border = if (isSelected) null else FilterChipDefaults.filterChipBorder(
      borderColor = outline,
      selectedBorderColor = Color.Transparent
    ),
    shape = RoundedCornerShape(8.dp)
  )
}
```

## Export Report Button

```kotlin
OutlinedButton(
  onClick = onExportReport,
  enabled = !isExporting,
  modifier = Modifier.height(48.dp),
  border = BorderStroke(1.dp, if (isExporting) outline else primary),
  colors = ButtonDefaults.outlinedButtonColors(
    contentColor = if (isExporting) onSurfaceVariant else primary
  ),
  shape = RoundedCornerShape(8.dp)
) {
  if (isExporting) {
    CircularProgressIndicator(
      modifier = Modifier.size(16.dp),
      strokeWidth = 2.dp,
      color = onSurfaceVariant
    )
  } else {
    Icon(Icons.Default.Upload, contentDescription = null, modifier = Modifier.size(16.dp))
  }
  Spacer(6.dp)
  Text(
    text = if (isExporting) "Exporting..." else "Export Report",
    style = MaterialTheme.typography.labelLarge
  )
}
```

---

# SECTION 4: INTERACTION FLOWS

## Flow 1: Dashboard Load

```
FieldOfficerDashboardScreen enters composition
  ↓
LaunchedEffect(Unit): viewModel.loadDashboard()
  ↓
isLoading = true → ShimmerSkeleton (KPI grid + 5 shimmer cards)
  ↓
Parallel API calls (Dispatchers.IO):
  GET /centers?staffId=3&limit=100
  → 8 centers returned
  ↓
For each center (parallel):
  GET /loans?groupId={id}&loanStatus=active
  GET /datatables/dt_group_corpus/{centerId}
  ↓
Compute per group:
  overdueRate = overdueLoans / totalActiveLoans
  healthLevel = if(overdueRate < 0.05) GREEN else if(< 0.20) AMBER else RED
  ↓
Compute KPIs:
  kpiTotalGroups = 8
  kpiTotalMembers = sum of member counts
  kpiTotalSavings = sum of corpus balances
  kpiLoansOutstanding = sum of outstanding loan principals
  ↓
isLoading = false
Groups sorted: RED first, AMBER second, GREEN last (critical groups surface to top)
KPI values animate (count-up 300ms)
RED group health dots pulse once (600ms scale animation)
```

## Flow 2: Region Filter Applied

```
User taps "Region ▾" chip
  ↓
DropdownMenu appears:
  Nairobi / Mombasa / Kisumu / Nakuru
  ↓
User taps "Nairobi"
DropdownMenu dismisses
  ↓
FilterByRegion("Nairobi") action
  ↓
selectedRegion = "Nairobi"
filteredGroups = groups.filter { it.region == "Nairobi" } = [Mwangaza, Tumaini]
  ↓
FilterChip updates:
  Label: "Region" → "Region: Nairobi"
  Background: surfaceVariant → primaryContainer (200ms)
  Trailing: ▾ → ×
  ↓
Section header: "Groups (8)" → "Groups (2)" (animated number change 200ms)
Group list: 8 cards → 2 cards (AnimatedVisibility exit for removed, 250ms)
  ↓
KPI cards: unchanged (always show ALL groups totals)
```

## Flow 3: Clear Filter

```
User taps × on "Region: Nairobi" chip
  ↓
ClearFilters (or FilterByRegion(null)) action
  ↓
selectedRegion = null
filteredGroups = groups (all 8)
  ↓
Chip: "Region: Nairobi" → "Region ▾" (200ms)
Group list restores: missing groups animate in (250ms)
Section header: "Groups (2)" → "Groups (8)"
```

## Flow 4: Export Report

```
User taps "Export Report" button
  ↓
OnExportReport action
  ↓
isExporting = true
Button → "Exporting..." with spinner
  ↓
ExportRepository.generateCsv(groups) on Dispatchers.IO:
  Build CSV string with header + one row per group
  Write to context.cacheDir/portfolio_report.csv
  Create FileProvider URI
  ↓
isExporting = false
  ↓
ShareCsvFile(uri) event
  ↓
Activity starts share intent:
  Intent.ACTION_SEND, mimeType="text/csv"
  User selects: email / WhatsApp / Google Drive / etc.
```

## Flow 5: Open Group Detail (Read-Only)

```
User taps Mwangaza Women's Group card
  ↓
Card ripple effect
  ↓
OnOpenGroupDetail(groupId=7)
  ↓
NavigateToGroupDetail(groupId=7, readOnlyMode=true)
  ↓
group-detail screen opens
  Field officer: read-only mode
    - Corpus card visible (no edit)
    - Member list visible (no add/remove)
    - Loan list visible (no approve)
    - No Quick Actions FAB
    - TopAppBar shows "← Back" to return to field-officer-dashboard
```

## Flow 6: Multi-Filter (Region + Overdue)

```
User selects Region: Nairobi (2 groups: Mwangaza GREEN, Tumaini AMBER)
User selects Overdue: HIGH (>10%)
  ↓
filteredGroups = groups.filter {
  it.region == "Nairobi" && it.overdueRate > 0.10
} = [Tumaini Savings Circle]  // 12% overdue, Nairobi
  ↓
Section header: "Groups (1)"
2 filter chips both show selected state
  ↓
Only Tumaini shown with AMBER indicator
```

---

# SECTION 5: REAL DATA SPECIFICATION

## Field Officer Context
**staffId**: 3
**staffName**: James Otieno
**officeName**: Nairobi Branch (primary office — supervises Nairobi + other regions)

## 5 Groups (Rendered Demo — all GREEN/AMBER/RED represented)

| groupId | Group Name | Region | Members | Savings | Active Loans | Overdue | Rate | Health |
|---------|-----------|--------|---------|---------|-------------|---------|------|--------|
| 7 | Mwangaza Women's Group | Nairobi | 12 | KES 47,500 | 3 | 0 | 0% | GREEN |
| 12 | Tumaini Savings Circle | Nairobi | 10 | KES 28,000 | 5 | 1 | 12% | AMBER |
| 15 | Umoja Welfare Group | Mombasa | 18 | KES 35,000 | 8 | 2 | 25% | RED |
| 18 | Pamoja | Mombasa | 8 | KES 18,500 | 2 | 0 | 3% | GREEN |
| 21 | Maisha Bora Circle | Kisumu | 11 | KES 13,000 | 4 | 1 | 8% | AMBER |

**Groups sorted in display order**: RED first (Umoja), AMBER (Tumaini, Maisha Bora), GREEN (Mwangaza, Pamoja).

## Full ViewModel State (demo)

```kotlin
FieldOfficerDashboardState(
  isLoading = false,
  isRefreshing = false,
  kpiTotalGroups = 8,  // all 8 supervised groups
  kpiTotalMembers = 94,
  kpiTotalSavings = 142_000L,
  kpiLoansOutstanding = 87_500L,
  groups = listOf(
    GroupHealthCard(15, "Umoja Welfare Group", "Mombasa", GroupStatus.ACTIVE, 18, 35_000L, 0.25f, 2, 8, HealthLevel.RED),
    GroupHealthCard(12, "Tumaini Savings Circle", "Nairobi", GroupStatus.ACTIVE, 10, 28_000L, 0.12f, 1, 5, HealthLevel.AMBER),
    GroupHealthCard(21, "Maisha Bora Circle", "Kisumu", GroupStatus.ACTIVE, 11, 13_000L, 0.08f, 1, 4, HealthLevel.AMBER),
    GroupHealthCard(7, "Mwangaza Women's Group", "Nairobi", GroupStatus.ACTIVE, 12, 47_500L, 0.0f, 0, 3, HealthLevel.GREEN),
    GroupHealthCard(18, "Pamoja", "Mombasa", GroupStatus.ACTIVE, 8, 18_500L, 0.03f, 0, 2, HealthLevel.GREEN)
    // + 3 more groups in full 8-group list
  ),
  filteredGroups = groups,  // no active filters
  selectedRegion = null,
  selectedStatus = null,
  selectedOverdueFilter = null,
  isExporting = false,
  error = null
)
```

## Export CSV Content (demo)

```csv
Group Name,Region,Status,Members,Total Savings (KES),Active Loans,Overdue Count,Overdue Rate,Health
Umoja Welfare Group,Mombasa,ACTIVE,18,35000,8,2,25%,RED
Tumaini Savings Circle,Nairobi,ACTIVE,10,28000,5,1,12%,AMBER
Maisha Bora Circle,Kisumu,ACTIVE,11,13000,4,1,8%,AMBER
Mwangaza Women's Group,Nairobi,ACTIVE,12,47500,3,0,0%,GREEN
Pamoja,Mombasa,ACTIVE,8,18500,2,0,3%,GREEN
...
```

File name: `portfolio_report_2026-05-06.csv`

---

# SECTION 6: RESPONSIVE LAYOUT + ADAPTIVE BEHAVIOR

## Compact Layout (0–599dp) — Primary target (360dp)

```
Screen: 360dp

TopAppBar: fullWidth, 64dp (two-line)

KPI Grid: LazyVerticalGrid(columns=Fixed(2), padding=horizontal 16dp, spacedBy=8dp)
  KPI Card width: (360 - 32 - 8) / 2 = 160dp
  KPI Card height: 80dp min (wrap content)
  Total grid height: 2 rows × (80dp + 8dp gap) = ~176dp

FilterChipRow: Row(padding=horizontal 16dp, spacedBy=8dp)
  3 chips × ~80dp each = needs horizontal scroll if content overflow
  → LazyRow recommended for chip overflow on small screens

GroupHealthCards: LazyColumn items, 80dp min each
  Width: 360 - 32dp margin = 328dp per card
```

### Compact KPI Value Formatting
```
kpiTotalSavings = 142000L → "KES 142K"  (K suffix for thousands)
kpiLoansOutstanding = 87500L → "KES 87.5K"
kpiTotalMembers = 94 → "94" (no suffix for counts)
```

## Medium Layout (600–839dp) — Tablet

```
KPI Grid: 4 columns in a single row
  KPI Card width: (600 - 32 - 24) / 4 = ~136dp each
  Total grid height: 80dp (1 row only)

FilterChips: Row, no scroll needed (more space)

GroupHealthCards: fullWidth, 360dp–580dp cards (padding 40dp horizontal)
```

## Expanded Layout (840dp+) — Field Officer Work Tablet

```
Row(fillMaxSize, padding=24dp, spacedBy=24dp)
  ├── Column(weight=0.35f) — LEFT: KPI + Filters
  │   ├── KPI Grid (2×2 or 1×4 depending on available width)
  │   ├── Spacer(16dp)
  │   ├── FilterChipRow (vertical stack in narrow panel)
  │   └── ExportButton
  │
  └── Column(weight=0.65f) — RIGHT: Group List
      ├── SectionHeader (with live count)
      └── LazyColumn: GroupHealthCards
          (scrollable independently of left panel)
```

## Dark Theme Mappings

| Light | Dark | Element |
|-------|------|---------|
| primaryContainer #A6F1A6 | #003910 | Groups KPI bg |
| onPrimaryContainer #002106 | #A6F1A6 | Groups KPI text |
| secondaryContainer #FFDDB3 | #422B00 | Members KPI bg |
| onSecondaryContainer #2A1700 | #FFDDB3 | Members KPI text |
| tertiaryContainer #D2E4FF | #003A8C | Savings KPI bg |
| onTertiaryContainer #001C39 | #D2E4FF | Savings KPI text |
| errorContainer #FFDAD6 | #410002 | Loans KPI bg |
| onErrorContainer #410002 | #FFDAD6 | Loans KPI text |
| surface #FAFAFA | #1C1C1E | Group card bg |
| Health dot colors (primary/secondary/error) | same hex values | health dots |

## Empty State (No Groups Assigned)

```kotlin
FieldOfficerEmptyState:
  Column(fillMaxSize, CenterHorizontally, Center)
    Icon(group_off, size=64dp, tint=onSurfaceVariant)
    Spacer(16dp)
    Text("No Groups Assigned", titleMedium, onSurface)
    Spacer(8dp)
    Text("Contact your administrator to be assigned VSLA groups.", bodySmall, onSurfaceVariant, textAlign=Center)
```

## Snackbar Messages

| Trigger | Message | Duration |
|---------|---------|---------|
| Export started | "Generating portfolio report..." | short |
| Export complete | "Report exported — check your share apps" | long |
| Export failed | "Export failed. Check storage permissions." | long |
| Refresh failed | "Cannot refresh — showing cached data" | long |
| Network restored | "Connected — refreshing data" | short |

## Loading Skeleton

```kotlin
FieldOfficerSkeleton:
  Column(padding=16dp, spacedBy=12dp)
    // KPI skeleton
    Row(spacedBy=8dp)
      ShimmerBox(weight=0.5f, height=80dp, cornerRadius=12dp)
      ShimmerBox(weight=0.5f, height=80dp, cornerRadius=12dp)
    Row(spacedBy=8dp)
      ShimmerBox(weight=0.5f, height=80dp, cornerRadius=12dp)
      ShimmerBox(weight=0.5f, height=80dp, cornerRadius=12dp)
    // Filter chip skeleton
    Row(spacedBy=8dp)
      ShimmerBox(width=80dp, height=32dp, cornerRadius=8dp)
      ShimmerBox(width=80dp, height=32dp, cornerRadius=8dp)
      ShimmerBox(width=80dp, height=32dp, cornerRadius=8dp)
    // Group card skeletons
    repeat(4) { ShimmerBox(fillMaxWidth, height=80dp, cornerRadius=12dp) }

// ShimmerBox: alpha 0.3→1.0→0.3 over 1200ms, color=surfaceVariant #DEE5DA
```

---

## Component State Matrix

Full state definitions for every interactive component in the field-officer-view feature. MifosSave tokens: primary #2E7D32, secondary #FF8F00, tertiary #1565C0, error #D32F2F.

### KpiCard (field-officer-dashboard — 4 KPI cards in 2×2 grid)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| KpiCard (groups) | default | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | none | 2dp | false | true |
| KpiCard (members) | default | secondaryContainer #FFDDB3 | onSecondaryContainer #2A1700 | none | 2dp | false | true |
| KpiCard (savings) | default | tertiaryContainer #D2E4FF | onTertiaryContainer #001C39 | none | 2dp | false | true |
| KpiCard (loans) | default | errorContainer #FFDAD6 | onErrorContainer #410002 | none | 2dp | false | true |
| KpiCard (any) | loading skeleton | surfaceVariant shimmer | n/a | none | 0dp | false | true |
| KpiCard (any) | error (load failed) | surfaceVariant #DEE5DA | onSurfaceVariant #424942 | 1dp outline #727971 | 0dp | false | true |
| KpiCard (any) | pressed (tappable future) | same bg, 8dp elevation | same text | none | 8dp | true | true |
| KpiCard (any) | focused (d-pad) | same bg | same text | 2dp primary #2E7D32 | 2dp | true | true |

### HealthBadge / HealthChip on GroupCard

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| HealthBadge GREEN | healthy | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | none | 0dp | false | true |
| HealthBadge AMBER | attention needed | secondaryContainer #FFDDB3 | onSecondaryContainer #2A1700 | none | 0dp | false | true |
| HealthBadge RED | critical | errorContainer #FFDAD6 | onErrorContainer #410002 | 1dp error #D32F2F | 0dp | false | true |
| HealthBadge (loading) | shimmer placeholder | surfaceVariant shimmer | n/a | none | 0dp | false | true |

### FilterChip (field-officer-dashboard — All / Green / Amber / Red)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| FilterChip "All" unselected | default | surface #FAFAFA | onSurfaceVariant #424942 | 1dp outline #727971 | 0dp | true | true |
| FilterChip "All" selected | active | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | none | 0dp | true | true |
| FilterChip "Green" selected | active | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | none | 0dp | true | true |
| FilterChip "Amber" selected | active | secondaryContainer #FFDDB3 | onSecondaryContainer #2A1700 | none | 0dp | true | true |
| FilterChip "Red" selected | active | errorContainer #FFDAD6 | onErrorContainer #410002 | none | 0dp | true | true |
| FilterChip (any) | pressed | surfaceVariant #DEE5DA | onSurface #1A1C19 | 1dp #2E7D32 | 0dp | true | true |
| FilterChip (any) | focused | surface #FAFAFA | onSurface #1A1C19 | 2dp primary #2E7D32 | 0dp | true | true |
| FilterChip (any) | disabled | surface at 38% | onSurface at 38% | 1dp at 38% | 0dp | false | true |

### GroupCard (field-officer-dashboard — main list item)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| GroupCard | default | surface #FAFAFA | onSurface #1A1C19 | none | 2dp | true | true |
| GroupCard | pressed | surfaceVariant #DEE5DA | onSurface #1A1C19 | none | 8dp | true | true |
| GroupCard | focused (d-pad) | surface #FAFAFA | onSurface #1A1C19 | 2dp primary #2E7D32 | 2dp | true | true |
| GroupCard — RED health | default | surface #FAFAFA | onSurface #1A1C19 | 1dp error #D32F2F (left-side accent) | 2dp | true | true |
| GroupCard — AMBER health | default | surface #FAFAFA | onSurface #1A1C19 | 1dp secondary #FF8F00 (left-side accent) | 2dp | true | true |
| GroupCard (loading skeleton) | shimmer | surfaceVariant | n/a | none | 0dp | false | true |

### ExportButton (field-officer-dashboard)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| ExportButton | default | primary #2E7D32 | onPrimary #FFFFFF | none | 4dp | true | true |
| ExportButton | pressed | primary #1B5E20 | onPrimary #FFFFFF | none | 8dp | true | true |
| ExportButton | focused | primary #2E7D32 | onPrimary #FFFFFF | 2dp onPrimary ring | 4dp | true | true |
| ExportButton | loading | primary #2E7D32 | CircularProgress white | none | 4dp | false | true |
| ExportButton | disabled | surface #FAFAFA | onSurface at 38% | none | 0dp | false | true |

---

## API Failure & Recovery Playbook

### GET /field-officer/portfolio (load dashboard KPIs and group list)

| Failure Type | Detection | User-Facing Response | Recovery |
|---|---|---|---|
| Network timeout | IOException after 10s | Snackbar: "Cannot refresh — showing cached data" | Show cached Room DB snapshot; retry 1s → 2s → 4s back-off |
| 401 Unauthorized | HTTP 401 | Navigate to login screen | Return to dashboard after re-auth; restore filter state |
| 403 Forbidden | HTTP 403 | "Access denied — contact your administrator" | No retry; log to Crashlytics |
| 404 Officer Not Found | HTTP 404 | "Officer profile not found — contact Mwangaza support" | No auto-retry; show contact info |
| 500 Server Error | HTTP 5xx | Snackbar: "Server error — showing cached data" with Retry | Manual retry; auto-retry once after 5s |
| Offline | No network | "Offline — showing last synced data" (warningContainer banner) | Auto-refresh when connectivity restored; show last-sync timestamp in TopAppBar subtitle |

### GET /field-officer/groups/{groupId}/detail (group detail expand — future v2)

| Failure Type | Detection | User-Facing Response | Recovery |
|---|---|---|---|
| Network timeout | IOException | "Loading from cache" chip | Show cached group detail |
| 401 Unauthorized | HTTP 401 | Re-auth then return to group | Preserve groupId in navigation backstack |
| 404 Not Found | HTTP 404 | "Group not found — may have been deleted" | Remove from local group list; re-sync portfolio |
| 500 Server Error | HTTP 5xx | Error snackbar with Retry | Manual retry |

### POST /field-officer/export (generate portfolio report)

| Failure Type | Detection | User-Facing Response | Recovery |
|---|---|---|---|
| Network timeout | IOException | "Export timed out — check your connection" Snackbar | Manual retry; do NOT queue to SyncQueue (export is read-only) |
| 401 Unauthorized | HTTP 401 | Re-auth then auto-retry export | Re-auth preserves export parameters |
| 500 Server Error | HTTP 5xx | "Export failed — try again later" Snackbar | Manual retry; Retry action in Snackbar |
| Offline | No network | "Must be online to export report" tooltip | Disable export button when offline; auto-enable on reconnect |
| Storage permission denied | SecurityException | "Storage permission required to save export" | Open app settings deep-link |

### Real-time Health Score Degradation (polling)

Field officer dashboard polls health scores every 5 minutes when app is in foreground:
- If poll fails: keep last health score; show "Last updated {timestamp}" in subtitle
- If 3 consecutive polls fail: show "Data may be outdated" warning chip on each GroupCard
- If poll recovers: silently update health scores; animate badge color transitions 300ms

---

## Screen Reader & Accessibility Deep Dive

### field-officer-dashboard — Focus Order (TalkBack / D-pad traversal)

1. TopAppBar — "Field Officer Dashboard, Mwangaza Women's Group region" (heading)
2. TopAppBar subtitle — "Last synced: {timestamp}" (status)
3. TopAppBar action — "Export portfolio report, button"
4. KPI card: Groups — "Groups: 8 groups in portfolio" (read as group)
5. KPI card: Members — "Members: 94 total members across all groups"
6. KPI card: Savings — "Total savings: KES 142,000"
7. KPI card: Loans outstanding — "Loans outstanding: KES 67,500"
8. FilterChip "All" (selected) — "Show all groups, selected"
9. FilterChip "Green" — "Show healthy groups only, not selected"
10. FilterChip "Amber" — "Show groups needing attention, not selected"
11. FilterChip "Red" — "Show critical groups, not selected"
12. GroupCard 1 — "Mwangaza Women's Group, health: Green, 12 members, savings KES 24,000, meeting on 15 Jun 2026, button"
13. GroupCard 2 — "Jua Kali Savings Group, health: Amber, 8 members, savings KES 11,200, 1 overdue loan, button"
14. GroupCard 3 — "Umoja Bora Group, health: Red, 6 members, 3 overdue loans, button"
15. ... (remaining GroupCards in portfolio order)

### TalkBack Announcement Strings

| Element | Announcement |
|---|---|
| KPI card (groups) | "Groups: {count} groups in your portfolio" |
| KPI card (members) | "Members: {count} total members across all groups" |
| KPI card (savings) | "Total savings: KES {amount} across all groups" |
| KPI card (loans) | "Loans outstanding: KES {amount} across {loanCount} active loans" |
| FilterChip unselected | "Filter by {health} health groups, not selected" |
| FilterChip selected | "Showing {health} groups, {count} groups found, selected" |
| GroupCard (GREEN) | "{groupName}, healthy group, {memberCount} members, savings KES {amount}, next meeting {date}" |
| GroupCard (AMBER) | "{groupName}, needs attention, {memberCount} members, {overdueCount} overdue loan(s)" |
| GroupCard (RED) | "{groupName}, critical — {memberCount} members, {overdueCount} overdue loans, immediate action required" |
| Export button | "Export portfolio report as PDF or CSV, button" |
| Loading state | "Loading field officer portfolio, please wait" (live region: polite) |
| Refresh complete | "Portfolio data refreshed, {count} groups updated" (polite) |
| Offline banner | "No internet connection — showing data from {timestamp}" (assertive) |

### Content Descriptions — Icons

| Icon | Content Description |
|---|---|
| groups (KPI) | "Total groups" |
| people (KPI) | "Total members" |
| savings (KPI) | "Total savings" |
| account_balance (KPI) | "Total loans outstanding" |
| download / export | "Export portfolio report" |
| circle (GREEN health) | "Group health: good" |
| warning_amber (AMBER health) | "Group health: needs attention" |
| error (RED health) | "Group health: critical" |
| sync | "Sync portfolio data" |
| arrow_back | "Go back" |

### Live Region Announcements

- Filter chip selected: "Showing {count} {health} groups" (polite)
- Export starts: "Generating portfolio report, please wait" (polite)
- Export complete: "Report exported successfully, saved to {filename}" (assertive)
| Export failed | "Export failed — {reason}" (assertive) |
- Health score update: "Portfolio health updated: {n} green, {n} amber, {n} red groups" (polite)
- Network restored: "Connected — refreshing portfolio data" (polite)

### Keyboard Navigation

- `Tab` / `Shift+Tab`: move focus KPI cards → FilterChips → GroupCards → Export button
- `Arrow keys` within FilterChip row: left/right to navigate chips
- `Enter` / `Space`: activate focused GroupCard (navigate to group detail) or FilterChip (toggle)
- `Escape`: dismiss any open bottom sheet or export options dialog
- All health states use both color AND icon — GREEN=check_circle, AMBER=warning, RED=error

### WCAG AA Contrast Ratios

| Text / Background | Contrast Ratio | Pass |
|---|---|---|
| onPrimaryContainer #002106 / primaryContainer #A6F1A6 | 11.2:1 | AAA |
| onSecondaryContainer #2A1700 / secondaryContainer #FFDDB3 | 9.1:1 | AAA |
| onTertiaryContainer #001C39 / tertiaryContainer #D2E4FF | 10.4:1 | AAA |
| onErrorContainer #410002 / errorContainer #FFDAD6 | 9.8:1 | AAA |
| onSurface #1C1C1C / surface #FAFAFA | 17.4:1 | AAA |
| onSurfaceVariant #424942 / surfaceVariant #DEE5DA | 5.9:1 | AA |
| primary #2E7D32 / surface #FAFAFA (large text) | 5.8:1 | AA |

---

## Animation & Motion Spec

### Screen Transitions

| Transition | Type | Duration | Easing |
|---|---|---|---|
| Login → field-officer-dashboard | fade through | 300ms | Standard |
| field-officer-dashboard → group-detail | containerTransform (card expands) | 400ms | EmphasizedDecelerate |
| group-detail → field-officer-dashboard (back) | containerTransform reverse | 350ms | EmphasizedAccelerate |
| Tab switch (if bottom nav present) | fade through | 200ms | Standard |

### Component Micro-Animations

| Component | Animation | Duration | Easing |
|---|---|---|---|
| KPI card value load | count-up number animation (0 → final value) | 600ms | DecelerateInterpolator |
| Health badge color change (poll update) | background color interpolation (e.g. AMBER→RED) | 300ms | Standard |
| FilterChip selection | background color + border interpolation | 150ms | Standard |
| GroupCard press ripple | radial ripple from touch point | 200ms | Standard |
| Export button loading | label fade out, CircularProgress fade in | 100ms | — |
| Pull-to-refresh | CircularProgressIndicator (primaryContainer tonal); rotate 360° at 900ms/rev |
| Offline banner slide in | slide down from top | 200ms | StandardDecelerate |
| Offline banner dismiss | slide up to hide | 200ms | StandardAccelerate |
| BottomSheet (export options) | slide up 350ms (EmphasizedDecelerate); dismiss 300ms |

### KPI Card Entrance Stagger

When dashboard first loads (after skeleton shimmer disappears):
1. KPI card 1 (Groups): scale 0.9→1.0 + fade 0→1, delay 0ms
2. KPI card 2 (Members): same, delay 50ms
3. KPI card 3 (Savings): same, delay 100ms
4. KPI card 4 (Loans): same, delay 150ms
5. GroupCards: stagger 30ms per card, start after KPIs complete
Total entrance duration: ~800ms for full dashboard (including 4 KPIs + first 6 GroupCards)

---

## Test & QA Annotations

### UI Test Tags

| Component | testTag |
|---|---|
| Dashboard root | `FieldOfficer_Dashboard_Root` |
| KPI card groups | `KpiCard_Groups` |
| KPI card members | `KpiCard_Members` |
| KPI card savings | `KpiCard_Savings` |
| KPI card loans | `KpiCard_Loans` |
| Filter chip "All" | `FilterChip_All` |
| Filter chip "Green" | `FilterChip_Green` |
| Filter chip "Amber" | `FilterChip_Amber` |
| Filter chip "Red" | `FilterChip_Red` |
| Group card | `GroupCard_{groupId}` |
| Health badge on card | `GroupCard_{groupId}_HealthBadge` |
| Export button | `FieldOfficer_ExportButton` |
| Offline banner | `FieldOfficer_OfflineBanner` |
| Error snackbar | `Snackbar_Error` |
| Last sync timestamp | `FieldOfficer_LastSyncTimestamp` |

### Required Test Scenarios — field-officer-dashboard

```
Given: field officer has 8 groups (5 green, 2 amber, 1 red)
When: dashboard loads
Then: KpiCard_Groups shows "8"; 5 green cards; 2 amber cards; 1 red card with error border

Given: user selects filter "Red"
When: FilterChip_Red is tapped
Then: only the 1 red GroupCard is shown; FilterChip_Red shows errorContainer background; TalkBack announces "Showing 1 critical group"

Given: user selects filter "Amber"
When: FilterChip_Amber is tapped
Then: 2 amber GroupCards shown; filter chip shows secondaryContainer background

Given: network is offline
When: dashboard opens
Then: offline banner visible (warningContainer); all data shows from cache; last-sync timestamp in subtitle; export button disabled

Given: user taps Export
When: network available and export succeeds
Then: loading state on button; success Snackbar "Report exported — Mwangaza_Portfolio_2026-06-15.pdf saved"
```

### Required Test Scenarios — GroupCard health states

```
Given: Mwangaza Women's Group has no overdue loans
When: card renders
Then: HealthBadge shows GREEN (primaryContainer); left border accent = none; TalkBack reads "healthy group"

Given: Jua Kali Savings Group has 1 overdue loan
When: card renders
Then: HealthBadge shows AMBER (secondaryContainer); overdue count chip visible; left border = secondary amber 1dp

Given: Umoja Bora Group has 3+ overdue loans
When: card renders
Then: HealthBadge shows RED (errorContainer); error 1dp left border; TalkBack reads "critical — immediate action required"

Given: health score updates during 5-minute poll (AMBER → RED)
When: poll response received
Then: badge color transitions 300ms (AMBER secondaryContainer → RED errorContainer); no layout jump

Given: all groups healthy (all green)
When: user taps filter "Red"
Then: empty state shown "No critical groups — all groups are healthy"; confirmation icon (check_circle green)
```

### Edge Cases

| Scenario | Expected Behavior |
|---|---|
| 0 groups in portfolio (new officer) | Empty state: "No groups assigned — contact your administrator" |
| 1 group in portfolio | Single GroupCard; KPI cards show values for that 1 group |
| 20 groups (max portfolio) | VirtualList LazyColumn; 60fps scroll; no dropped frames |
| Group name 50+ chars (e.g. "Kisumu Central Women's Cooperative Savings and Loan Association") | Truncate at 2 lines; full name in TalkBack; tooltip on long-press |
| RTL layout | KPI grid mirrors; GroupCard health badge stays on end side; FilterChip row scrolls RTL |
| Very large KPI value (KES 999,999) | Formatted "KES 1M" in compact form on KPI card; full value in TalkBack |
| Portfolio load takes > 3s | Shimmer skeleton shows for all KPIs and first 4 GroupCard placeholders |

### Performance Baselines

- Dashboard first meaningful paint: < 300ms on mid-range Android (2GB RAM, Snapdragon 450)
- KPI card value count-up: smooth 60fps for 600ms animation
- GroupCard list scroll: 60fps for up to 20 cards
- Filter chip selection → filtered list render: < 150ms
- Export button tap → loading state: < 100ms
- Poll update → health badge color change: < 50ms (no layout recomposition)

---

## i18n / Localization Spec

### String Keys and Translations

| Key | English (en) | Swahili (sw) | French (fr) |
|-----|-------------|--------------|-------------|
| `fo_dashboard_title` | "Field Officer Dashboard" | "Dashibodi ya Afisa Uwanjani" | "Tableau de bord de l'agent de terrain" |
| `fo_kpi_groups` | "Groups" | "Makundi" | "Groupes" |
| `fo_kpi_members` | "Members" | "Wanachama" | "Membres" |
| `fo_kpi_savings` | "Total Savings" | "Akiba Jumla" | "Épargne totale" |
| `fo_kpi_loans` | "Loans Outstanding" | "Mikopo Inayoendelea" | "Prêts en cours" |
| `fo_filter_all` | "All Groups" | "Makundi Yote" | "Tous les groupes" |
| `fo_filter_green` | "Healthy" | "Yenye Afya" | "En bonne santé" |
| `fo_filter_amber` | "Needs Attention" | "Inahitaji Tahadhari" | "Nécessite attention" |
| `fo_filter_red` | "Critical" | "Muhimu / Hatari" | "Critique" |
| `fo_health_green` | "Healthy" | "Afya Nzuri" | "Sain" |
| `fo_health_amber` | "Attention Needed" | "Tahadhari Inahitajika" | "Attention requise" |
| `fo_health_red` | "Critical" | "Hali ya Hatari" | "Critique" |
| `fo_export_button` | "Export Report" | "Hamisha Ripoti" | "Exporter le rapport" |
| `fo_export_success` | "Report saved to {filename}" | "Ripoti imehifadhiwa: {filename}" | "Rapport enregistré: {filename}" |
| `fo_offline_banner` | "Offline — showing cached data from {timestamp}" | "Nje ya mtandao — inaonyesha data ya {timestamp}" | "Hors ligne — données du {timestamp}" |
| `fo_last_sync` | "Last synced: {timestamp}" | "Ilisasishwa mara ya mwisho: {timestamp}" | "Dernière sync: {timestamp}" |
| `fo_no_groups` | "No groups assigned" | "Hakuna makundi yaliyopewa" | "Aucun groupe assigné" |
| `fo_empty_filter` | "No {health} groups" | "Hakuna makundi ya {health}" | "Aucun groupe {health}" |
| `fo_all_healthy` | "All groups are healthy" | "Makundi yote yana afya nzuri" | "Tous les groupes sont sains" |

### Pluralization Rules

| Key | Singular (en) | Plural (en) | Swahili |
|---|---|---|---|
| `group_count` | "1 group" | "{n} groups" | "kundi 1" → "makundi {n}" |
| `member_count` | "1 member" | "{n} members" | "mwanachama 1" → "wanachama {n}" |
| `overdue_count` | "1 overdue loan" | "{n} overdue loans" | "mkopo 1 umechelewa" → "mikopo {n} imechelewa" |

### Number Formatting (portfolio context)

| Value Type | en-KE | sw-KE | fr-FR |
|---|---|---|---|
| KPI savings (large) | KES 142,000 or compact "KES 142K" | same | KES 142 000 |
| KPI loans outstanding | KES 67,500 | same | KES 67 500 |
| Group savings (card) | KES 24,000 | same | KES 24 000 |
| Compact form threshold | ≥ 100,000 → use "K" suffix | same | same |

### Date Formatting

Portfolio last-sync timestamp:
| Locale | Format | Example |
|---|---|---|
| en-KE | "15 Jun 2026, 14:30" | DD MMM YYYY, HH:mm |
| sw-KE | "15 Jun 2026, 14:30" | same |
| fr-FR | "15/06/2026 à 14:30" | DD/MM/YYYY à HH:mm |

Next meeting date on GroupCard:
| Locale | Format | Example |
|---|---|---|
| en-KE | "Next meeting: 15 Jun" | "Next meeting: DD MMM" |
| sw-KE | "Mkutano ujao: 15 Jun" | same date format |
| fr-FR | "Prochaine réunion: 15 jun" | "DD MMM" lowercase month |

### RTL Considerations

- KPI 2×2 grid: grid items mirror in RTL (first item top-right in RTL)
- GroupCard: group name on start, health badge on end (reverses in RTL)
- FilterChip row: horizontally scrollable, RTL scroll direction
- Export button: full-width, text centered — no directional change
- All icons: auto-mirrored where directional (arrow_back, chevron_right)

---

## Offline-First Architecture Notes

### Field Officer Data Model (Room Entities)

```
FieldOfficerPortfolioEntity {
  officerId: String (PK)
  totalGroups: Int
  totalMembers: Int
  totalSavingsKes: Long
  totalLoansOutstandingKes: Long
  lastSyncedAt: Instant
  healthSummary: HealthSummary // GREEN:5, AMBER:2, RED:1
}

GroupHealthEntity {
  groupId: String (PK)
  groupName: String
  officerId: String (FK)
  memberCount: Int
  savingsBalance: Long
  activeLoansCount: Int
  overdueLoansCount: Int
  healthStatus: HealthStatus (GREEN | AMBER | RED)
  nextMeetingDate: LocalDate?
  lastMeetingDate: LocalDate?
  lastSyncedAt: Instant
}
```

### Health Score Calculation (Client-Side)

Health status is derived client-side from GroupHealthEntity data. No separate API call for health:
- GREEN: overdueLoansCount == 0 AND attendance rate (last 3 meetings) >= 80%
- AMBER: overdueLoansCount == 1–2 OR attendance rate 60–79%
- RED: overdueLoansCount >= 3 OR attendance rate < 60% OR no meetings in 30+ days

This calculation runs in a ViewModel using pure Kotlin — no network needed. Health status updates automatically when GroupHealthEntity is refreshed from server.

### Portfolio Export Format

The export button generates a portfolio summary report with two format options (bottom sheet):
1. PDF — formatted table with MifosSave branding; suitable for printing or sharing with MFI supervisor
2. CSV — raw data for import into Excel/Google Sheets; includes all GroupHealthEntity fields

Export file naming convention:
- `{officerName}_Portfolio_{YYYY-MM-DD}.pdf`
- `{officerName}_Portfolio_{YYYY-MM-DD}.csv`

Example: `JohnOdhiambo_Portfolio_2026-06-15.pdf`

### Background Sync Strategy

Field officer dashboard uses WorkManager for background data refresh:
- Frequency: every 4 hours while app is not in foreground
- Constraint: requires network connectivity
- On sync complete: send local notification "Portfolio data updated — {n} groups refreshed"
- Notification only shown if data changed (health status changed for any group)
- Foreground poll (while dashboard visible): every 5 minutes via coroutine delay (not WorkManager)

### Deep Link Support

Field officer can receive push notifications that deep-link to specific group detail:
- Notification format: "Umoja Bora Group — 3 loans now overdue. Tap to view."
- Deep link: `mifossave://field-officer/group/{groupId}`
- On tap: dashboard opens with RED filter pre-selected, scrolled to the relevant GroupCard
- Deep link works even from cold start (app not running)

### Dashboard Personalization (v2.0.0)

Planned for v2.0.0: field officer can pin their most critical groups to the top of the dashboard:
- Pinned groups always appear first regardless of filter
- Pin icon on each GroupCard (star outline → star filled when pinned)
- Max 3 pinned groups
- Pin state stored in DataStore (device-local, not server-synced)
- Pinned groups: pin icon uses primary #2E7D32 filled star

---

## Field Officer Reference Data

### Sample Portfolio — John Odhiambo, Kisumu Region

Reference data for all design mockups, test scenarios, and TalkBack announcements in the field-officer-view feature:

| Group Name | Members | Health | Savings (KES) | Overdue Loans | Next Meeting |
|---|---|---|---|---|---|
| Mwangaza Women's Group | 12 | GREEN | 24,000 | 0 | 15 Jun 2026 |
| Jua Kali Savings Group | 8 | AMBER | 11,200 | 1 | 20 Jun 2026 |
| Umoja Bora Group | 6 | RED | 8,400 | 3 | 18 Jun 2026 |
| Pwani Wanawake Circle | 10 | GREEN | 18,600 | 0 | 22 Jun 2026 |
| Kisumu Central VSLA | 15 | GREEN | 32,100 | 0 | 17 Jun 2026 |
| Mama Pima Cooperative | 9 | AMBER | 14,400 | 2 | 19 Jun 2026 |
| Siaya Youth Fund | 11 | GREEN | 21,000 | 0 | 23 Jun 2026 |
| Hekima Women's Group | 7 | GREEN | 9,800 | 0 | 25 Jun 2026 |

KPI totals: 8 groups · 78 members · KES 139,500 savings · KES 67,500 loans outstanding.

### Health Score Thresholds — Design Guidance

The three health states are visually distinct in every context they appear. Designers must never use green for a group with any overdue loans, regardless of savings balance:

| Condition | Health | Color | Icon |
|---|---|---|---|
| 0 overdue loans, attendance ≥ 80% | GREEN | primaryContainer | check_circle |
| 1–2 overdue loans OR attendance 60–79% | AMBER | secondaryContainer | warning_amber |
| 3+ overdue loans OR attendance < 60% | RED | errorContainer | error |
| No meetings in 30+ days (stale) | RED | errorContainer | error |
| Data insufficient to calculate | GREY | surfaceVariant | help_outline |

### GroupCard Layout Spec (compact breakpoint — 360dp)

At minimum supported screen width (360dp), GroupCard must fit all key information:

```
GroupCard (fillMaxWidth, padding 12dp, cornerRadius 12dp, elevation 2dp):
  Row(verticalAlignment=CenterVertically, horizontalArrangement=SpaceBetween):
    Column(weight=1f, spacedBy=4dp):
      Text(groupName, titleMedium, maxLines=1, overflow=Ellipsis)
      Row(spacedBy=8dp):
        Text("{memberCount} members", labelSmall, onSurfaceVariant)
        Text("KES {savings}", labelSmall, onSurfaceVariant)
    Column(horizontalAlignment=End, spacedBy=4dp):
      HealthBadge(status)    // chip with color + icon
      Text("Next: {date}", labelSmall, onSurfaceVariant)

Left border accent (RED/AMBER health only):
  Box(width=4dp, fillMaxHeight, color=health.accentColor) // outside card padding
```

At 360dp: groupName truncates to ~22 chars; amounts use compact "KES 24K" form for values ≥ 10,000.

### Push Notification Spec — Field Officer Events

| Event | Title | Body | Deep Link |
|---|---|---|---|
| Group health degrades (GREEN→AMBER) | "Jua Kali Savings — needs attention" | "1 loan is now overdue in your portfolio" | `mifossave://field-officer/group/{groupId}` |
| Group health degrades (AMBER→RED) | "Umoja Bora — critical alert" | "3 loans now overdue. Immediate action required." | `mifossave://field-officer/group/{groupId}` |
| No meeting in 30 days | "Mwangaza Women's Group — no recent meeting" | "Last meeting was 35 days ago. Please follow up." | `mifossave://field-officer/group/{groupId}` |
| Portfolio sync complete | "Portfolio updated" | "8 groups refreshed — all data current" | `mifossave://field-officer/dashboard` |
| Export ready | "Report ready" | "Your portfolio report is ready to download" | `mifossave://field-officer/export/{exportId}` |

Notification channel: `field_officer_alerts` — priority HIGH for health degradation events, NORMAL for sync complete and export ready.
