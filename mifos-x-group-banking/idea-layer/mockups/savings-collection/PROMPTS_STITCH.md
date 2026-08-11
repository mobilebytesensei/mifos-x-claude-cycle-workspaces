# PROMPTS_STITCH — savings-collection
# MifosSave (mifos-x-group-banking) | Feature FR-004 / FR-017
# Generated: 2026-05-06
# Sections: 6 | Total lines: ≥1,200

---

## SECTION 1 — Design System Context

### 1.1 Brand Purpose for Savings Collection

The savings-collection feature is the financial heart of MifosSave. For VSLA groups like the Mwangaza Women's Group, weekly savings are the engine of shared prosperity. The UI communicates:
- Group solidarity: mandatory savings viewed collectively (group savings = shared wealth in green)
- Individual autonomy: optional personal savings in amber (personal money, personal choice)
- Progress and growth: cycle progress bars animate on entry, visually celebrating collective advancement toward the year-end share-out

The dual-savings model (FR-017) reflects the VSLA structure:
- GROUP_LINKED savings: mandatory, linked to group account, minimum KES 200/meeting, pooled for loans
- INDIVIDUAL savings: voluntary, linked to personal account, no minimum, accessible by member

### 1.2 Color System — Full Specification

**Primary — VSLA-green #2E7D32 (Group Savings Identity):**
- primary: #2E7D32
- on_primary: #FFFFFF
- primary_container: #A6F1A6 (cycle progress card, group total chips, running total band)
- on_primary_container: #002106

**Secondary — Amber #FF8F00 (Individual Savings Identity):**
- secondary: #FF8F00
- on_secondary: #FFFFFF
- secondary_container: #FFDDB3 (minimum contribution chip, individual total card)
- on_secondary_container: #2A1700

**Tertiary — Trust-blue #1565C0 (Informational, Balances):**
- tertiary: #1565C0
- on_tertiary: #FFFFFF
- tertiary_container: #D2E4FF
- on_tertiary_container: #001C39

**Error (Validation):**
- error: #D32F2F (below-minimum group savings, amount > 10,000)
- on_error: #FFFFFF
- error_container: #FFDAD6 (error state textfield background tint)
- on_error_container: #410002

**Surface:**
- background: #FFFFFF
- on_background: #1A1C19
- surface: #FAFAFA (app background)
- on_surface: #1A1C19
- surface_variant: #DEE5DA (last-sync band, dividers, skeleton shimmer base)
- on_surface_variant: #424942 (secondary labels, section headers)
- outline: #727971 (textfield unfocused border)
- outline_variant: #C2C9BD (list item dividers, stepper inactive connectors)

**Chart-specific colors:**
- Group savings bars: #2E7D32 (primary) with 100% opacity
- Group savings bars (hover/pressed): #1B5E20 (darker green)
- Individual savings line: #FF8F00 (secondary)
- Individual savings fill-below: rgba(255, 143, 0, 0.12) — 12% opacity amber fill
- Individual savings data point dots: #FF8F00 (secondary, 8dp diameter)
- Chart axis text: #424942 (on_surface_variant, labelSmall 11sp)
- Chart grid lines: #C2C9BD (outline_variant, 0.5dp, dashed)

### 1.3 Typography — Full Scale

Font family: Noto Sans (all weights)
Scale configured: large (optimized for rural users, low-DPI displays, outdoor use)

| Role | Size (sp) | Line Height | Weight | Usage in Savings |
|------|-----------|-------------|--------|-----------------|
| displayLarge | 57 | 64 | 400 | Not used |
| displayMedium | 45 | 52 | 400 | Not used |
| displaySmall | 36 | 44 | 400 | Not used |
| headlineLarge | 32 | 40 | 400 | Not used |
| headlineMedium | 28 | 36 | 400 | Individual total balance KES amount |
| headlineSmall | 24 | 32 | 400 | Running total band KES amount |
| titleLarge | 22 | 28 | 500 | TopAppBar "Savings" title |
| titleMedium | 16 | 24 | 500 | "Savings Collection" step header |
| titleSmall | 14 | 20 | 500 | Section headers ("Per-Member Contributions") |
| bodyLarge | 16 | 24 | 400 | Member name in list rows |
| bodyMedium | 14 | 20 | 400 | Cycle amounts text ("KES 7,600 collected") |
| bodySmall | 12 | 16 | 400 | "3 meetings · Last: KES 600" sub-labels |
| labelLarge | 14 | 20 | 500 | Member savings totals in trailing (group tab) |
| labelMedium | 12 | 16 | 500 | "Total Savings This Step:" label in running total |
| labelSmall | 11 | 16 | 500 | Tab labels, chip text, week labels in chart, percent text |

KES amounts in cards and banners: Noto Sans bold (weight 700) for numbers.

### 1.4 Spacing Scale (dp)

- xxs: 2dp — minimal padding
- xs: 4dp — chip internal horizontal padding
- sm: 8dp — gap between chips in a row; textfield bottom margin
- md: 12dp — card internal section gaps; chart margin
- lg: 16dp — standard screen horizontal padding; card padding
- xl: 24dp — card top padding for large cards
- xxl: 32dp — section separation
- 3xl: 48dp — empty state padding
- 4xl: 64dp — empty state illustration size

Vertical rhythm: 8dp base grid throughout. Row heights: 72dp (member list), 48dp (text fields), 40dp (chips and progress bar sections).

### 1.5 Shape Tokens

- none: 0dp — flat progress track
- extra_small: 4dp — progress bar cap
- small: 8dp — shimmer skeleton corner; textfield corner
- medium: 12dp — standard card corner radius (cycle progress card, individual total card)
- large: 16dp — hero cards (not used in savings-collection primary)
- extra_large: 28dp — bottom sheet dialogs
- full: 9999dp — chips, avatars, FABs, tab indicator

### 1.6 Elevation

| Level | dp | Tonal Alpha | Usage |
|-------|-----|------------|-------|
| level_0 | 0dp | 0.00 | SavingsDashboard background |
| level_1 | 1dp | 0.05 | Sync band subtle separation |
| level_2 | 3dp | 0.08 | Cycle progress card, per-member cards |
| level_3 | 6dp | 0.11 | RunningTotalBand slight lift |
| level_4 | 8dp | 0.12 | Not used in savings-collection |
| level_5 | 12dp | 0.14 | Not used in savings-collection |

### 1.7 Motion System

Durations and their savings-specific usage:
- short_2: 100ms — running total band text crossfade on each input change
- short_3: 150ms — textfield label color transition (normal → error → focused)
- short_4: 200ms — fade-in for deposit/withdrawal chip; tab content fade; scale bump on total update
- medium_1: 250ms — step content crossfade when advancing from step 2→3
- medium_2: 300ms — bar chart bar grow animation per bar; validation error snackbar slide-up
- medium_3: 350ms — savings validation debounce wait before error shows
- medium_4: 400ms — full bar chart render completion; line chart draw animation
- long_1: 450ms — cycle progress bar fill animation on screen entry
- long_2: 500ms — line chart fill-below fade animation

Easing curves:
- standard: cubic-bezier(0.2, 0.0, 0, 1.0) — most UI motion
- emphasized: cubic-bezier(0.2, 0.0, 0, 1.0) — hero element entries
- decelerated: cubic-bezier(0.0, 0.0, 0, 1.0) — progress bar fill, cycle card
- accelerated: cubic-bezier(0.3, 0.0, 1.0, 1.0) — elements leaving

### 1.8 Chart Design Tokens

**Group Savings Bar Chart:**
- chart_type: bar (vertical)
- bar_color: primary #2E7D32
- bar_width: 28dp per bar
- bar_gap: 8dp between bars
- x_axis_label_style: labelSmall 11sp, on_surface_variant #424942
- y_axis_label_style: labelSmall 11sp, on_surface_variant #424942
- grid_line_color: outline_variant #C2C9BD, opacity 0.5, dashed
- chart_height: 180dp
- chart_margin_horizontal: 16dp
- chart_margin_top: 12dp
- chart_margin_bottom: 8dp
- selected_bar_color: on_primary_container #002106 (darker green on tap)
- tooltip_background: surface_variant #DEE5DA
- tooltip_text_style: labelMedium 12sp, on_surface #1A1C19

**Individual Savings Line Chart:**
- chart_type: line (with area fill)
- line_color: secondary #FF8F00
- line_width: 2dp
- dot_color: secondary #FF8F00
- dot_size: 8dp diameter
- dot_selected_size: 12dp
- fill_below_color: rgba(255, 143, 0, 0.12)
- x_axis_label_style: labelSmall 11sp, on_surface_variant
- y_axis_label_style: labelSmall 11sp, on_surface_variant
- chart_height: 180dp
- chart_margin_horizontal: 16dp
- chart_margin_top: 12dp
- chart_margin_bottom: 8dp

### 1.9 Accessibility Standards

- Minimum touch target: 48dp × 48dp
- Member list rows: min_height 72dp, min_touch_target enforced via LocalMinimumInteractiveComponentEnforcement
- Tab items: min_touch_target 48dp, both width and height
- Text fields: min_height 48dp
- Color alone never communicates state: group savings bars labeled with week labels; individual chart has line labels; error states always include text
- Focus ring: 3dp, primary #2E7D32 for light theme
- TalkBack: all interactive components have content_description
- Charts: provide alternative text description for screen readers (total and trend summary)
- Contrast: primary on white 5.83:1 (AAA); secondary on white 3.21:1 (AA large only — used only for icons and large text)

---

## SECTION 2 — Screen Layouts

### 2.1 SavingsDashboardScreen — Full Component Tree (compact, portrait)

```
SavingsDashboardScreen
├── TopAppBar (height: 56dp, background: surface #FAFAFA)
│   ├── Title: "Savings" (titleLarge 22sp, on_surface #1A1C19)
│   └── Subtitle: "Mwangaza Women's Group" (bodyMedium 14sp, on_surface_variant #424942)
├── LastSyncBand (visible_when: lastSyncAt != null)
│   ├── background: surface_variant #DEE5DA
│   ├── padding_horizontal: 16dp, padding_vertical: 4dp
│   ├── height: 24dp
│   └── Text "Last synced: 7 May 2026, 10:34 AM" (labelSmall 11sp, on_surface_variant #424942)
├── TabRow (indicator: primary #2E7D32, 3dp indicator height)
│   ├── Tab GROUP: icon FluentIcons.people_money_24_regular + label "Group Savings"
│   │   ├── selected_label_color: primary #2E7D32 (labelSmall)
│   │   └── unselected_label_color: on_surface_variant #424942
│   └── Tab INDIVIDUAL: icon FluentIcons.person_money_24_regular + label "Individual"
│       ├── selected_label_color: primary #2E7D32
│       └── unselected_label_color: on_surface_variant
├── TabContent (fills remaining height, LazyColumn per tab)
│   ├── GroupSavingsTabContent (visible_when: selectedTab == GROUP)
│   │   ├── WeeklyBarChart
│   │   │   ├── type: bar; height: 180dp; mh: 16dp; mt: 12dp; mb: 8dp
│   │   │   ├── data: 6 bars — W48(1000), W49(1200), W50(850), W51(1500), W52(1200), W3(1850)
│   │   │   ├── bar_color: primary #2E7D32
│   │   │   ├── animation: bars grow bottom-to-top, 300ms total, 50ms delay between each
│   │   │   └── content_description: "Weekly group savings bar chart. Highest: KES 1,850 in week W3 2026"
│   │   ├── CycleProgressCard
│   │   │   ├── background: primary_container #A6F1A6
│   │   │   ├── corner_radius: 12dp; padding: 16dp; mh: 16dp; mb: 12dp
│   │   │   ├── Text "Cycle Progress" (labelLarge 14sp, on_primary_container #002106)
│   │   │   ├── LinearProgressIndicator
│   │   │   │   ├── progress: cycleCollected / cycleTarget (= 7600 / 10400 ≈ 0.731)
│   │   │   │   ├── color: primary #2E7D32
│   │   │   │   ├── track_color: rgba(46, 125, 50, 0.3)
│   │   │   │   ├── height: 8dp; corner_radius: 4dp; mt: 8dp; mb: 8dp
│   │   │   │   └── animation: 0→0.731 over 450ms decelerated on screen entry
│   │   │   ├── Row (space_between):
│   │   │   │   ├── "KES 7,600 collected" (bodyMedium, on_primary_container)
│   │   │   │   └── "Target: KES 10,400" (bodyMedium, on_primary_container)
│   │   │   └── Text "73% of cycle target reached" (labelSmall 11sp, on_primary_container 80% opacity)
│   │   ├── SectionHeader "Per-Member Contributions" (titleSmall 14sp, on_surface_variant, ph: 16dp, pt: 8dp, pb: 4dp)
│   │   ├── GroupTotalChip "Group total: KES 7,600" (primary_container bg, mh: 16dp, mb: 8dp, corner: full)
│   │   └── LazyColumn of GroupMemberSavingsRow × 5
│   │       ├── min_height: 72dp; ph: 16dp; pv: 12dp; divider: 1dp outline_variant
│   │       ├── Leading: CircleAvatar(initials, 40dp, secondary_container #FFDDB3, on_secondary_container)
│   │       ├── Content:
│   │       │   ├── member.name (bodyLarge 16sp, on_surface #1A1C19)
│   │       │   └── "3 meetings · Last: KES 600" (bodySmall 12sp, on_surface_variant #424942)
│   │       ├── Trailing Column (alignment: end):
│   │       │   ├── "KES 1,800" (labelLarge 14sp, primary #2E7D32)
│   │       │   └── "total" (labelSmall 11sp, on_surface_variant)
│   │       └── onClick → OpenMemberDetail(memberId, GROUP_LINKED)
│   └── IndividualSavingsTabContent (visible_when: selectedTab == INDIVIDUAL)
│       ├── WeeklyLineChart
│       │   ├── type: line; height: 180dp; mh: 16dp; mt: 12dp; mb: 8dp
│       │   ├── data: 6 points — W48(300), W49(500), W50(200), W51(700), W52(400), W3(650)
│       │   ├── line_color: secondary #FF8F00; line_width: 2dp
│       │   ├── dot_color: secondary #FF8F00; dot_size: 8dp
│       │   ├── fill_below: rgba(255, 143, 0, 0.12)
│       │   ├── animation: line draws L→R 400ms; fill fades in 200ms after line completes
│       │   └── content_description: "Weekly individual savings line chart. Highest: KES 700 in week W51 2025"
│       ├── IndividualTotalCard
│       │   ├── background: secondary_container #FFDDB3
│       │   ├── corner_radius: 12dp; padding: 16dp; mh: 16dp; mb: 12dp
│       │   ├── Text "Total Individual Balances" (labelLarge, on_secondary_container #2A1700)
│       │   └── Text "KES 3,750" (headlineMedium 28sp bold, on_secondary_container)
│       ├── SectionHeader "Member Balances" (titleSmall, on_surface_variant, ph: 16dp, pt: 8dp, pb: 4dp)
│       └── LazyColumn of IndividualMemberSavingsRow × 5
│           ├── min_height: 72dp; ph: 16dp; pv: 12dp; divider: 1dp outline_variant
│           ├── Leading: CircleAvatar(initials, 40dp, tertiary_container #D2E4FF, on_tertiary_container)
│           ├── Content:
│           │   ├── member.name (bodyLarge, on_surface)
│           │   └── TransactionChipRow:
│           │       ├── [↑ Deposit] chip: background primary_container, on_primary_container, labelSmall, corner full
│           │       ├── [↓ Withdrawal] chip: background error_container, on_error_container, labelSmall, corner full
│           │       └── Text "KES 500 on 7 May" (bodySmall, on_surface_variant, ml: 4dp)
│           ├── Trailing Column (alignment: end):
│           │   ├── "KES 1,500" (labelLarge 14sp, secondary #FF8F00)
│           │   └── "balance" (labelSmall, on_surface_variant)
│           └── onClick → OpenMemberDetail(memberId, INDIVIDUAL)
├── LoadingSkeleton (visible_when: isLoading)
│   ├── 6 shimmer items; height: 72dp; corner_radius: 12dp; margin: 16dp
│   └── shimmer gradient: surface_variant #DEE5DA → outline_variant #C2C9BD → surface_variant; 1200ms cycle
└── ErrorBanner (visible_when: error != null)
    ├── background: error_container #FFDAD6
    ├── padding: 12dp
    ├── Text "Showing cached savings — pull down to retry" (bodySmall, on_error_container)
    └── TextButton "Retry" → RefreshDashboard
```

### 2.2 Step3SavingsCollection (In-Wizard) — Full Component Tree

```
Step3SavingsCollection (visible_when: currentStep == 3)
├── Header "Savings Collection" (titleMedium 16sp, on_surface, mb: 4dp)
├── MinContributionChip
│   ├── text: "Min. group savings: KES 200/member (FR-020)"
│   ├── background: secondary_container #FFDDB3
│   ├── text_color: on_secondary_container #2A1700
│   ├── corner: full; padding: sm(8dp)/xs(4dp); mb: 12dp
│   └── content_description: "Minimum group savings is KES 200 per member per meeting"
├── LazyColumn of SavingsMemberRow × 5 (Amina, Peter, Grace, John, Mary)
│   ├── padding_vertical: 12dp
│   ├── divider: 1dp outline_variant
│   ├── Row:
│   │   ├── Leading: CircleAvatar(initials, 40dp, secondary_container #FFDDB3, on_secondary_container)
│   │   └── Column(flex=1, ml: 12dp):
│   │       ├── Text(member.name, bodyLarge, on_surface)
│   │       ├── OutlinedTextField "Group Savings (KES)"
│   │       │   ├── value: savingsMap[memberId]?.groupAmount or ""
│   │       │   ├── label: "Group Savings (KES)"
│   │       │   ├── hint: "Min. 200"
│   │       │   ├── prefix: "KES"
│   │       │   ├── keyboardType: Number
│   │       │   ├── min_height: 48dp
│   │       │   ├── isError: groupAmount > 0 AND groupAmount < 200
│   │       │   ├── supportingText (when error):
│   │       │   │   └── "Below minimum KES 200 required" (labelSmall, error #D32F2F)
│   │       │   └── onValueChange → SetSavingsAmount(memberId, amount, GROUP_LINKED)
│   │       └── OutlinedTextField "Individual Savings (KES)"
│   │           ├── value: savingsMap[memberId]?.individualAmount or ""
│   │           ├── label: "Individual Savings (KES)"
│   │           ├── hint: "Optional"
│   │           ├── prefix: "KES"
│   │           ├── keyboardType: Number
│   │           ├── min_height: 48dp
│   │           ├── margin_top: 8dp
│   │           └── onValueChange → SetSavingsAmount(memberId, amount, INDIVIDUAL)
│   └── content_description: "Savings entry for {member.name}: group KES {amount}, individual KES {amount}"
└── RunningTotalBand
    ├── background: primary_container #A6F1A6
    ├── padding: 16dp; margin_top: 8dp; corner_radius: 8dp
    ├── Row:
    │   ├── Text "Total Savings This Step:" (labelMedium 12sp, on_primary_container)
    │   └── Text "KES 1,350" (headlineSmall 24sp bold, on_primary_container, ml: auto)
    └── content_description: "Running savings total for this meeting: KES 1,350"
```

---

## SECTION 3 — Component Specifications

### 3.1 WeeklyBarChart

**Component name:** WeeklyBarChart
**Props:** data (List\<WeeklyContributionPoint\>), yField (String: "groupAmount"), barColor (Color = primary), height (Dp = 180dp)

**Visual spec:**
- Overall size: 180dp height, full available width minus 32dp (16dp margin each side)
- Bar width: floor((availableWidth - totalGaps) / dataPoints.size)
- For 6 data points and ~328dp available: (328 - 5×8) / 6 ≈ 47dp per bar
- Bar gap: 8dp between bars
- Y-axis: 5 tick marks; max = ceil(maxValue / 500) × 500; e.g. max 2000, ticks at 0, 500, 1000, 1500, 2000
- Y-axis labels: "0", "500", "1K", "1.5K", "2K" (abbreviated above 1000)
- X-axis labels: week strings; labelSmall 11sp; centered below each bar
- Grid lines: horizontal dashed lines at each y-tick; outline_variant 0.5dp
- Bar corner: top corners rounded with small (8dp) radius; bottom flat

**Entry animation:**
- Each bar: animateFloatAsState from 0f to 1f (fractional height) with delay(i × 50ms), duration 300ms, decelerated easing
- Total animation time: 6 bars × 50ms delay + 300ms = 550ms

**Touch interaction:**
- On bar tap: bar darkens to on_primary_container #002106 (100ms)
- Tooltip appears above tapped bar: "W3: KES 1,850" (surface_variant bg, bodyMedium, 4dp padding, 8dp corner radius, 150ms fade-in)
- Tooltip auto-dismisses after 2000ms

**Accessibility:**
- content_description: "Weekly group savings bar chart. 6 weeks shown. W48: KES 1,000; W49: KES 1,200; W50: KES 850; W51: KES 1,500; W52: KES 1,200; W3: KES 1,850."
- role: Image (charts are non-interactive in accessibility tree; data also available in list below)

---

### 3.2 WeeklyLineChart

**Component name:** WeeklyLineChart
**Props:** data (List\<WeeklyContributionPoint\>), yField (String: "individualAmount"), lineColor (Color = secondary), height (Dp = 180dp)

**Visual spec:**
- Same overall dimensions as WeeklyBarChart (180dp × full-width-minus-32dp)
- Line: 2dp width, secondary #FF8F00
- Data point dots: 8dp diameter, secondary #FF8F00, filled; on tap: 12dp (scale animation 150ms)
- Fill-below: area from line to x-axis; fill color rgba(255, 143, 0, 0.12); gradient may fade to transparent at bottom
- Y-axis: same tick calculation as bar chart but for individual amounts (max ~800 KES → ticks at 0, 200, 400, 600, 800)
- X-axis: same week labels

**Entry animation:**
- Path draws from left to right: PathEffect animated using animateFloatAsState on path fraction, 400ms decelerated
- Fill-below fades in: alpha animates 0→0.12 over 200ms, starting at 300ms (after line mostly drawn)
- Dots appear: scale 0→1 per dot, 100ms each, 40ms delay between dots

**Touch interaction:**
- Tap/drag on chart → nearest data point highlights (scale 1→1.5, 100ms)
- Tooltip: week label + KES amount; amber tinted background (secondary_container #FFDDB3)

**Accessibility:**
- content_description: "Weekly individual savings line chart. 6 weeks shown. W48: KES 300; W49: KES 500; W50: KES 200; W51: KES 700; W52: KES 400; W3: KES 650."

---

### 3.3 CycleProgressCard

**Component name:** CycleProgressCard
**Props:** cycleCollected (Long), cycleTarget (Long)

**Computed:**
- progress: Float = cycleCollected.toFloat() / cycleTarget.toFloat() — clamped 0f–1f
- percentage: Int = (progress × 100).roundToInt()

**Visual spec:**
- background: primary_container #A6F1A6
- corner_radius: 12dp
- padding: 16dp
- margin_horizontal: 16dp
- margin_bottom: 12dp
- elevation: level_2 (3dp)

**Content:**
```
Text "Cycle Progress" (labelLarge 14sp, on_primary_container #002106)
LinearProgressIndicator:
  progress: animated 0f→currentProgress on screen entry (450ms, decelerated)
  color: primary #2E7D32
  track_color: rgba(46, 125, 50, 0.3) (30% alpha primary on primary_container)
  height: 8dp
  corner_radius: 4dp (ClipShape)
  margin_top: 8dp
  margin_bottom: 8dp
Row(horizontalArrangement: SpaceBetween):
  Text "KES 7,600 collected" (bodyMedium 14sp, on_primary_container)
  Text "Target: KES 10,400" (bodyMedium 14sp, on_primary_container)
Text "73% of cycle target reached" (labelSmall 11sp, on_primary_container, opacity 0.8)
```

**Progress animation:** animateFloatAsState(targetValue = progress, animationSpec = tween(450ms, easing = FastOutSlowInEasing))
**Percentage text animation:** CountingTextTransition — countUp from 0 to percentage over 400ms

---

### 3.4 GroupMemberSavingsRow

**Component name:** GroupMemberSavingsRow
**Props:** member (MemberGroupSavingsRow), onTap (String, SavingsType) -> Unit

**Visual spec:**
- min_height: 72dp
- padding_horizontal: 16dp
- padding_vertical: 12dp
- divider: 1dp, outline_variant #C2C9BD, start indent 72dp

**Layout:**
```
Row(verticalAlignment: CenterVertically):
  CircleAvatar:
    text: member.name initials (first 2 chars)
    size: 40dp
    background: secondary_container #FFDDB3
    text_color: on_secondary_container #2A1700
    text_style: labelLarge 14sp
  Column(flex=1, ml: 12dp):
    Text(member.name, bodyLarge 16sp, on_surface #1A1C19)
    Text("${member.meetingsContributed} meetings · Last: KES ${member.lastContribution}",
         bodySmall 12sp, on_surface_variant #424942, mt: 2dp)
  Column(horizontalAlignment: End):
    Text("KES ${member.totalContributed}", labelLarge 14sp, primary #2E7D32)
    Text("total", labelSmall 11sp, on_surface_variant #424942, mt: 2dp)
```

**Variants:**
- Default: standard row above
- Pressed: ripple bounded, scale 0.99 for 100ms
- Focused: 3dp primary focus ring

**Demo data:**
- Amina Hassan (AH): KES 1,800 total, 3 meetings, last KES 600
- Peter Otieno (PO): KES 1,800 total, 3 meetings, last KES 600
- Grace Wanjiku (GW): KES 1,400 total, 3 meetings, last KES 200
- John Mwangi (JM): KES 1,800 total, 3 meetings, last KES 600
- Mary Akinyi (MA): KES 800 total, 3 meetings, last KES 200

---

### 3.5 IndividualMemberSavingsRow

**Component name:** IndividualMemberSavingsRow
**Props:** member (MemberIndividualSavingsRow), onTap (String, SavingsType) -> Unit

**Visual spec:**
- Same dimensions as GroupMemberSavingsRow

**Leading:** CircleAvatar(initials, 40dp, tertiary_container #D2E4FF, on_tertiary_container #001C39)

**Content:**
```
Column:
  Text(member.name, bodyLarge, on_surface)
  Row (visible_when: lastTransaction != null):
    AssistChip:
      if DEPOSIT: text "↑ Deposit", bg primary_container #A6F1A6, text on_primary_container, corner full
      if WITHDRAWAL: text "↓ Withdrawal", bg error_container #FFDAD6, text on_error_container, corner full
      labelSmall 11sp
    Text("KES ${lastTransaction} on ${lastTransactionDate}", bodySmall, on_surface_variant, ml: 4dp)
```

**Trailing:**
```
Column(horizontalAlignment: End):
  Text("KES ${member.currentBalance}", labelLarge 14sp, secondary #FF8F00)
  Text("balance", labelSmall 11sp, on_surface_variant)
```

**Demo data:**
- Amina Hassan: KES 1,500 balance, last deposit KES 500 on 7 May
- Peter Otieno: KES 500 balance, no last transaction (opened but no activity this cycle)
- Grace Wanjiku: KES 850 balance, last deposit KES 200 on 5 May
- John Mwangi: KES 500 balance, last deposit KES 100 on 7 May
- Mary Akinyi: KES 400 balance, last deposit KES 100 on 7 May

---

### 3.6 SavingsMemberRow (In-Wizard)

**Component name:** SavingsMemberRow (used in Step3SavingsCollection)
**Props:**
- member (GroupMember): memberId, name, initials, role
- groupSavingsAmount (Long): current value in savingsMap
- individualSavingsAmount (Long): current value in savingsMap
- onGroupAmountChange ((Long) -> Unit)
- onIndividualAmountChange ((Long) -> Unit)

**Visual spec:**
- padding_vertical: 12dp
- divider: 1dp outline_variant

**TextField specification:**
- Component: OutlinedTextField (Material3)
- Container shape: small (8dp corner radius)
- min_height: 48dp
- prefix: {Text "KES" (labelLarge, on_surface_variant)}
- keyboard_type: KeyboardType.Number
- keyboard_options: ImeAction.Next (group field) / ImeAction.Done (individual field)
- cursor_color: primary #2E7D32
- focused_indicator_color: primary #2E7D32
- unfocused_indicator_color: outline #727971
- error_indicator_color: error #D32F2F

**Group savings validation:**
- Triggers: 300ms after last input change (debounce)
- Error condition: amount.toLong() in range 1..199
- Error text: "Below minimum KES 200 required"
- Max amount: 10,000 KES — input clamped, excess digits dropped
- Valid range: 200–10,000

**Individual savings validation:**
- No minimum — all amounts >= 0 valid
- Max: no maximum enforced in UI (backend may enforce limits)

---

### 3.7 RunningTotalBand

**Component name:** RunningTotalBand
**Props:** totalKES (Long)

**Visual spec:**
- background: primary_container #A6F1A6
- padding: 16dp all sides
- margin_top: 8dp
- corner_radius: 8dp (small)

**Layout:**
```
Row(verticalAlignment: CenterVertically):
  Text("Total Savings This Step:", labelMedium 12sp, on_primary_container #002106, flex: 1)
  Spacer
  Text("KES ${totalKES}", headlineSmall 24sp, on_primary_container, fontWeight: Bold)
```

**Animation:**
- On totalKES change: text crossfades (100ms, standard easing)
- On increase: brief scale pulse (1.0 → 1.05 → 1.0, 200ms, standard easing)
- On decrease: no pulse

---

## SECTION 4 — Interaction Patterns

### 4.1 SavingsDashboard Load Flow

**Screen enters composition:**
1. Dispatch LoadDashboard action
2. Check LocalSavingsDao cache: if data exists → render Content immediately; show LastSyncBand; kick off background refresh
3. If no cache → set isLoading=true → show 6-item shimmer skeleton (fade-in 200ms)
4. API calls run in parallel: get_group_savings_transactions + get_client_savings_accounts (×5) + get_individual_savings_transactions (×5)
5. As data arrives: progressively update state → Content renders (300ms crossfade from skeleton)
6. lastSyncAt = current timestamp → LastSyncBand fades in (200ms)
7. Charts render with entry animations (bar chart 550ms total; line chart 600ms total)

**Error handling:**
- Partial API failure: show available data + error_container banner for failed portions
- Full API failure + cache: Content with ErrorBanner (slides down 300ms)
- Full API failure + no cache: Error screen (fade-in 200ms) with centered Retry button

---

### 4.2 Tab Switching

**Tab indicator animation:**
- Horizontal slide from old to new tab position (200ms, standard easing)
- Tab label and icon color transitions: old tab fades to on_surface_variant (150ms); new tab activates to primary (150ms)

**Tab content transition:**
- Old content fades out (150ms)
- New content fades in (150ms) after old completes
- No slide — content areas differ significantly, crossfade is cleaner

**Chart re-renders:**
- Switching to GROUP: bar chart animates in fresh (all bars grow simultaneously, 300ms)
- Switching to INDIVIDUAL: line chart animates in (draw 400ms)
- Subsequent switches: charts animate on each tab switch (not just first visit)

---

### 4.3 Pull-to-Refresh

**Online:**
1. Pull ≥64dp → RefreshIndicator (CircularProgressIndicator, primary #2E7D32, 24dp) fades in (100ms)
2. Release → isRefreshing=true → API calls triggered
3. Data returns → content swaps in (200ms crossfade)
4. RefreshIndicator slides up and fades out (300ms)
5. LastSyncBand timestamp updates

**Offline:**
1. Pull → RefreshIndicator appears (100ms)
2. Release → ConnectivityObserver reports offline
3. RefreshIndicator dismisses immediately (200ms)
4. Snackbar: "Cannot refresh — you're offline" (error_container bg, 4000ms, no action button)
5. Content unchanged (showing last cached data)

---

### 4.4 Savings Input Flow (Step 3)

**Focus management:**
- Screen enters step 3 → focus auto-set to first member's group savings field (Amina Hassan)
- ImeAction.Next on group savings field → moves focus to individual savings field for same member
- ImeAction.Next on individual savings field → moves focus to next member's group savings field
- ImeAction.Done on last member's individual savings field → closes keyboard; user taps Next in footer

**Validation flow per field (group savings):**
1. Character entered → debounce timer resets
2. 300ms after last keypress → validation check:
   - amount in range 1..199 → isError=true; supportingText animates in (150ms fade)
   - amount == 0 or empty → isError=false; no error message (0 is handled at step advance validation)
   - amount in range 200..10000 → isError=false; field shows success state (focused: primary border)
3. SetSavingsAmount action dispatched on every change (validation is non-blocking)

**Amount clamping:**
- User types "12000" → field shows "12000" momentarily
- 300ms debounce → clamp fires → field snaps to "10000"
- Toast: "Maximum KES 10,000 per member per meeting" (2000ms, no action)

**Running total update:**
- Every SetSavingsAmount action → runningSavingsTotal recomputed in ViewModel
- State emission → RunningTotalBand recomposes (100ms text crossfade)
- CorpusBand (visible because step >= 2) also recomputes projected corpus

---

### 4.5 Member Row Tap → Detail Navigation

**GroupMemberSavingsRow tap:**
1. ripple bounded to row (100ms)
2. OpenMemberDetail(memberId, SavingsType.GROUP_LINKED) dispatched
3. NavigateToMemberDetail event emitted
4. NavController.navigate("/savings/member/{memberId}?type=GROUP_LINKED")
5. Slide-in from right (400ms, emphasized easing)
6. Back stack: dashboard → detail

**IndividualMemberSavingsRow tap:**
- Same flow with SavingsType.INDIVIDUAL

---

### 4.6 LastSyncBand — Display Logic

**Show conditions:**
- lastSyncAt != null (always true after first load completes)
- isLoading == false AND isRefreshing == false

**Animation:**
- On first appear: slideInVertically from -24dp (band height), 200ms
- On disappear (if sync completes < 30s ago): no hide — always shown once data is loaded

**Timestamp format:**
- Same day: "Last synced: 10:34 AM"
- Yesterday: "Last synced: Yesterday, 3:22 PM"
- Older: "Last synced: 5 May 2026, 2:15 PM"

---

## SECTION 5 — Content Data

### 5.1 Group Identity

- Group: Mwangaza Women's Group
- Center ID: 7
- Currency: KES (Kenya Shilling)
- Cycle: Cycle 1 (of 12 months total)
- Cycle start: January 2026
- Current meeting: Week 4 (Meeting #4, 7 May 2026)
- Cycle target savings: KES 10,400 (= 5 members × KES 200 min × 52 weeks × some fraction for 4-month partial)
- Group savings product name: "Group Linked Savings"
- Individual savings product name: "Individual Savings"

### 5.2 Savings Summary Data (Dashboard State at Meeting #4)

**Group Savings — Per Member (cycle to date):**
| Member | Meetings | Total Contributed | Last Contribution |
|--------|----------|------------------|------------------|
| Amina Hassan | 3 | KES 1,800 | KES 600 |
| Peter Otieno | 3 | KES 1,800 | KES 600 |
| Grace Wanjiku | 3 | KES 1,400 | KES 200 |
| John Mwangi | 3 | KES 1,800 | KES 600 |
| Mary Akinyi | 3 | KES 800 | KES 200 |
| **Group Total** | | **KES 7,600** | |

Note: Grace's lower total reflects she often contributes the minimum KES 200 when late.
Note: Mary's lowest total reflects she missed Meeting #3 (was absent) so contributed KES 0.

**Individual Savings — Per Member (current balances):**
| Member | Current Balance | Last Transaction | Date |
|--------|----------------|-----------------|------|
| Amina Hassan | KES 1,500 | Deposit KES 500 | 7 May 2026 |
| Peter Otieno | KES 500 | (no activity this cycle besides opening) | — |
| Grace Wanjiku | KES 850 | Deposit KES 200 | 5 May 2026 |
| John Mwangi | KES 500 | Deposit KES 100 | 7 May 2026 |
| Mary Akinyi | KES 400 | Deposit KES 100 | 7 May 2026 |
| **Total Balance** | **KES 3,750** | | |

### 5.3 Weekly Trend Data (last 6 meetings)

| Week | Meeting # | Date | Group KES | Individual KES |
|------|-----------|------|-----------|----------------|
| W48 (2025) | M#-2 (pre-cycle) | 24 Nov 2025 | 1,000 | 300 |
| W49 | M#-1 | 1 Dec 2025 | 1,200 | 500 |
| W50 | M#1 | 14 Apr 2026 | 850 | 200 |
| W51 | M#2 | 21 Apr 2026 | 1,500 | 700 |
| W52 | M#3 | 28 Apr 2026 | 1,200 | 400 |
| W3 (2026) | M#3 again | 28 Apr 2026 | 1,850 | 650 |

(Note: weeks W48-W49 represent pre-Cycle 1 seed savings; W50+ are Cycle 1)

### 5.4 Cycle Progress Computation

- cycleTarget: KES 10,400 (admin-configured in dt_group_config: contributionMin=200 × 52 weeks × 5 members / partial adjustment)
- cycleCollected: KES 7,600 (sum of mandatory group deposits in Cycle 1)
- cycleProgress: 7,600 / 10,400 = 0.731 = 73%
- Remaining to target: KES 2,800

### 5.5 Step 3 Wizard Data (Meeting #4 real-time entry)

At the time step 3 is displayed:
- openingCorpus: KES 12,400 (from corpus band)
- Group savings minimum: KES 200 per member
- Group savings maximum: KES 10,000 per member

Expected demo entry:
| Member | Group Savings | Individual Savings | Notes |
|--------|--------------|-------------------|-------|
| Amina Hassan | KES 200 | KES 500 | Has cash from her side business |
| Peter Otieno | KES 200 | KES 0 | Only group contribution this week |
| Grace Wanjiku | KES 200 | KES 50 | Small individual deposit |
| John Mwangi | KES 200 | KES 100 | |
| Mary Akinyi | KES 200 | KES 100 | |
| **Totals** | **KES 1,000** | **KES 750** | **KES 1,750 total** |

**Running total progression:**
- After Amina (first entry): KES 700
- After Peter: KES 900
- After Grace: KES 1,150
- After John: KES 1,450
- After Mary: KES 1,750 (final)

### 5.6 Validation Scenarios

**Scenario A — Grace enters KES 100 group savings:**
- isError=true on group field
- Error text: "Below minimum KES 200 required"
- Running total still includes KES 100 (partial sum)
- NextStep is blocked with message: "Grace Wanjiku has not met the minimum contribution of KES 200."

**Scenario B — Amina enters KES 15,000:**
- Input clamped to KES 10,000 after 300ms
- Toast: "Maximum KES 10,000 per member per meeting"

**Scenario C — Individual savings left empty:**
- Treated as KES 0 (valid — individual is optional)
- No error displayed

### 5.7 API Call Sequence on Meeting Submission (Savings Portion)

After all 5 members have valid entries, on SubmitMeeting:

Call 3a: POST /savingsaccounts/{groupSavingsAccountId}/transactions
  body: { transactionDate: "07 May 2026", transactionAmount: 200, paymentTypeId: 1, locale: "en", dateFormat: "dd MMMM yyyy" }
  → one call per member; total: 5 calls for group savings (only non-zero amounts)

Call 3b: POST /savingsaccounts/{amimaIndividualSavingsId}/transactions
  body: { transactionDate: "07 May 2026", transactionAmount: 500, paymentTypeId: 1, locale: "en", dateFormat: "dd MMMM yyyy" }
  → called for each member where individualAmount > 0; total: 4 calls (Peter = 0 excluded)

Total savings API calls: 9 (5 group + 4 individual)

---

## SECTION 6 — Responsive Rules

### 6.1 Breakpoints

| Name | Range | Primary Device |
|------|-------|---------------|
| compact | 0–599dp | Android phones (360–412dp width) |
| medium | 600–839dp | Foldables, 7" tablets |
| expanded | 840dp+ | 10"+ tablets, large foldables |

### 6.2 Compact (0–599dp) — Primary Target

**SavingsDashboardScreen (compact):**
- BottomNavigation: visible, 56dp height, 4 tabs
- TopAppBar: standard 56dp, single-line title + subtitle
- TabRow: full-width; tabs fill available space equally (50% each)
- Charts: height 180dp, full width minus 32dp margins
- CycleProgressCard: full width minus 32dp (16dp margins each side)
- GroupMemberSavingsRow: full-width; avatar (40dp) + content column + trailing
- IndividualMemberSavingsRow: same layout; secondary #FF8F00 trailing balance
- LastSyncBand: visible, 24dp height, full-width

**Step3SavingsCollection (compact, inside wizard):**
- SavingsMemberRow: single-column TextField layout — group savings field first (full width), individual savings field below (full width)
- RunningTotalBand: full-width, 16dp padding
- LazyColumn: must handle keyboard insets — imePadding() applied; screen scrolls to keep active TextField visible
- Member row height: dynamic based on TextField heights; minimum effective ~140dp (avatar + 2 TextFields)

### 6.3 Medium (600–839dp) — Foldable / Small Tablet

**SavingsDashboardScreen (medium):**
- BottomNavigation → NavigationRail (72dp left, icon + short label vertical)
- Content area: screen_width - 72dp
- Charts: max width 560dp, centered horizontally
- CycleProgressCard: max width 560dp, centered
- TabRow: max width 560dp, centered; larger touch targets
- Member rows: max width 560dp; consistent row height
- LastSyncBand: full-width (edge-to-edge)

**Step3SavingsCollection (medium):**
- SavingsMemberRow: switch to 2-column layout — group savings field left (48%), individual savings field right (48%), with 4dp gap
- Row height: ~80dp (avatar row + one row of two TextFields)
- This halves the scroll distance needed to complete step 3
- RunningTotalBand: max width 560dp, centered

### 6.4 Expanded (840dp+) — Tablet / Large Foldable

**SavingsDashboardScreen (expanded):**
- NavigationDrawer: permanent 240dp left panel
- 2-panel layout within content area:
  - Left panel (360dp): TabRow + charts stacked vertically
  - Right panel (remaining): per-member list with larger rows (80dp height)
- Charts fill left panel width (360dp - 32dp = 328dp)
- Right panel shows detail pane: tapping a member row → inline detail appears in right panel without navigation push
- Member rows in right panel: additional detail visible (sparkline mini-chart for last 4 contributions)

**Step3SavingsCollection (expanded):**
- 2-panel wizard layout (from expanded meeting-conduct):
  - SavingsMemberRow: 3-column layout — avatar + name (180dp) | group savings field (240dp) | individual savings field (240dp)
  - All 5 member rows visible simultaneously without scrolling (total ~400dp)
  - RunningTotalBand: spans full width of right panel

### 6.5 Font Scaling

- sp units used throughout; respects system font size
- bodySmall 12sp × 0.85 min = 10.2sp (acceptable for "3 meetings · Last: KES 600" secondary labels)
- Cycle progress percentage text: labelSmall 11sp; at 1.5× scale = 16.5sp — remains readable
- KES amounts: headlineSmall 24sp (running total) — at 1.5× = 36sp; still fits in banner
- Tab labels: labelSmall 11sp — at 2× might truncate; consider hiding individual tab label (icon-only) at 2× scale

### 6.6 Orientation — Landscape Compact

**Landscape on phone (landscape width ≈ 700–900dp → treated as medium breakpoint):**
- TabRow: moves to NavigationRail left side
- Charts: height constrained to min(180dp, available_height × 0.35)
- Member list: 2-column grid on landscape (side by side)
- Step3 savings: 2-column TextField layout (identical to medium breakpoint)
- Running total band: fixed to bottom of content area (not scrollable); positioned above NavigationFooter

### 6.7 Keyboard Insets (Step 3)

When TextFields in SavingsMemberRow gain focus:
1. IME (keyboard) appears → WindowInsets.ime provides keyboard height
2. LazyColumn content padding bottom = keyboard height + 16dp
3. LazyColumn.scrollToItem(focusedMemberIndex) called to bring active member into view
4. On keyboard dismiss: content padding resets (150ms animation)
5. RunningTotalBand stays visible above keyboard (it's part of LazyColumn as last item, not fixed)

### 6.8 RTL Support

- CircleAvatar initials: locale-aware character selection
- Row layouts: start/end instead of left/right
- Charts: RTL mirrors x-axis (weeks go right-to-left; most recent week on left)
- Tab indicator: slides right-to-left when tabs are in RTL order
- TextFields: text is LTR (numbers always LTR regardless of locale)
- Deposit/Withdrawal chip arrows: ↑ and ↓ remain vertical; no directional mirroring needed

### 6.9 Dark Theme Adaptation

All colors automatically adapt via CompositionLocalProvider(LocalContentColor):
- Bar chart: primary dark #8BD68F (instead of #2E7D32)
- Line chart: secondary dark #FFB95C (instead of #FF8F00)
- Card backgrounds: primary_container dark #00531A, secondary_container dark #653E00
- Surface: #121412; surface_variant dark: #424942
- Error states: error #FFB4AB on dark

### 6.10 Performance Considerations

**Chart rendering:**
- Bar chart: drawn on Canvas composable using DrawScope; no third-party library required
- Line chart: PathEffect + animatePathFraction; all computation in remember{} blocks to avoid recomposition
- Both charts: data passed as stable List; keys derived from weekLabel strings

**LazyColumn (per-member rows):**
- keys: member.memberId (stable, avoids full re-render on partial updates)
- itemContent: SavingsMemberRow is a @Composable fun with stable props; recomposes only when its specific member's data changes
- rememberUpdatedState for callbacks (onGroupAmountChange, onIndividualAmountChange) to avoid stale closure issues

**RunningTotalBand:**
- Derived state: val runningSavingsTotal by remember { derivedStateOf { savingsMap.values.sumOf { it.groupAmount + it.individualAmount } } }
- Only recomposes when savingsMap changes (not on other unrelated state changes)

**Offline cache:**
- SQLDelight schema: savings_transactions (id, savings_id, member_id, type, amount, date, synced)
- LRU-style eviction: max 200 rows per account; older rows purged on insert
- lastSyncAt stored in DataStore Preferences (not SQLDelight) for fast read without SQL overhead

---

## Appendix A — i18n Keys (savings-collection)

All user-visible strings referenced by key in the YAML screen definitions:

| Key | English |
|-----|---------|
| screen_title | "Savings" |
| group_tab_label | "Group Savings" |
| individual_tab_label | "Individual" |
| cycle_progress_label | "Cycle Progress" |
| per_member_header | "Per-Member Contributions" |
| member_balances_header | "Member Balances" |
| total_group_label | "Group total" |
| total_individual_label | "Total Individual Balances" |
| network_error | "Showing cached savings — pull down to retry" |
| last_synced_prefix | "Last synced:" |
| chart_x_label | "Week" |
| chart_y_label | "KES" |
| meetings_suffix | "meetings" |
| last_contribution_prefix | "Last:" |
| empty_title | "No Savings Data" |
| empty_subtitle | "Savings will appear after the first meeting is conducted" |
| min_contribution_chip | "Min. group savings: KES 200/member (FR-020)" |
| savings_collection_header | "Savings Collection" |
| group_savings_field_label | "Group Savings (KES)" |
| group_savings_hint | "Min. 200" |
| individual_savings_field_label | "Individual Savings (KES)" |
| individual_savings_hint | "Optional" |
| running_total_label | "Total Savings This Step:" |
| below_minimum_error | "Below minimum KES 200 required" |
| max_exceeded_toast | "Maximum KES 10,000 per member per meeting" |
| deposit_chip | "↑ Deposit" |
| withdrawal_chip | "↓ Withdrawal" |
| balance_label | "balance" |
| total_label | "total" |
| cant_refresh_offline | "Cannot refresh — you're offline" |

---

## Appendix B — Composable Dependency Map (savings-collection)

```
SavingsDashboardScreen
  ├── SavingsDashboardViewModel (Hilt ViewModel)
  │   ├── SavingsRepository (interface)
  │   │   ├── FineractSavingsDataSource (Retrofit)
  │   │   └── LocalSavingsDao (SQLDelight)
  │   ├── ConnectivityObserver (NetworkMonitor)
  │   └── NavigationManager
  ├── SavingsDashboardTopBar
  ├── LastSyncBand
  ├── SavingsTabRow
  ├── GroupSavingsTabContent
  │   ├── WeeklyBarChart (Canvas composable)
  │   ├── CycleProgressCard
  │   ├── GroupSavingsTotalChip
  │   └── GroupMemberSavingsRow × N (LazyColumn items)
  ├── IndividualSavingsTabContent
  │   ├── WeeklyLineChart (Canvas composable)
  │   ├── IndividualTotalCard
  │   └── IndividualMemberSavingsRow × N (LazyColumn items)
  └── SavingsDashboardSkeleton (visible when loading)

Step3SavingsCollection (inside MeetingConductScreen)
  ├── MeetingConductViewModel (shared ViewModel)
  ├── SavingsStepHeader
  ├── MinContributionChip
  ├── SavingsMemberRow × N
  │   ├── MemberAvatar
  │   ├── GroupSavingsTextField (validates on debounce)
  │   └── IndividualSavingsTextField
  └── RunningTotalBand (derives from MeetingConductState.runningSavingsTotal)
```

---

## Appendix C — Test Scenarios Matrix (savings-collection)

| Scenario | Screen | State | Expected Behavior |
|----------|--------|-------|------------------|
| First visit, online | SavingsDashboard | isLoading=true | 6-item shimmer skeleton; both tabs disabled during load |
| Load complete, GROUP tab | SavingsDashboard | Content GROUP | Bar chart with 6 bars; cycle progress 73%; 5 member rows |
| Switch to INDIVIDUAL tab | SavingsDashboard | Content INDIVIDUAL | Line chart draws; individual total card; 5 member rows with amber balance |
| Network error + cached data | SavingsDashboard | Content + error | Error banner (orange); cached content visible; last-sync band shows stale timestamp |
| Network error + no cache | SavingsDashboard | Error | Full-screen error state; Retry button |
| Offline pull-to-refresh | SavingsDashboard | Content | Snackbar "Cannot refresh — you're offline"; content unchanged |
| Step 3 empty entry | MeetingConduct | currentStep==3 | All fields empty; running total KES 0; Next tap blocked by validation |
| Step 3 valid minimum | MeetingConduct | currentStep==3 | All members enter KES 200; running total KES 1,000; no errors |
| Step 3 below minimum (Grace KES 100) | MeetingConduct | currentStep==3 | Grace's group field shows error text; running total shows KES 100 as partial; Next blocked |
| Step 3 above maximum (KES 12,000) | MeetingConduct | currentStep==3 | Input clamped to KES 10,000; toast shown; running total uses KES 10,000 |
| Step 3 individual only (group empty) | MeetingConduct | currentStep==3 | Individual entries accepted; group still required; Next blocked by group validation |
| Member row tap (GROUP tab) | SavingsDashboard | Content GROUP | Navigate to member-savings-detail with savingsType=GROUP_LINKED |
| Member row tap (INDIVIDUAL tab) | SavingsDashboard | Content INDIVIDUAL | Navigate to member-savings-detail with savingsType=INDIVIDUAL |

---

## Appendix D — Animation Choreography Timeline

Full animation sequence on SavingsDashboardScreen initial load (GROUP tab):

| T=0ms | Screen enters; shimmer skeleton fades in (200ms) |
| T=0ms | 4 API calls dispatched in parallel |
| T=~800ms | API responses arrive (typical latency) |
| T=800ms | Content fades in, skeleton fades out (250ms crossfade) |
| T=800ms | LastSyncBand slides down (200ms) |
| T=850ms | TabRow activates (150ms) |
| T=950ms | CycleProgressCard appears (fade 200ms) |
| T=1000ms | LinearProgress animates 0→73% (450ms) |
| T=1050ms | Bar chart starts rendering: bar 1 grows (W48) |
| T=1100ms | Bar 2 grows (W49, +50ms delay) |
| T=1150ms | Bar 3 grows (W50, +50ms delay) |
| T=1200ms | Bar 4 grows (W51, +50ms delay) |
| T=1250ms | Bar 5 grows (W52, +50ms delay) |
| T=1300ms | Bar 6 grows (W3, +50ms delay) |
| T=1350ms | All 6 bars at full height (300ms grow duration each) |
| T=1400ms | Member rows LazyColumn renders (stagger 50ms per row) |
| T=1650ms | All 5 member rows fully visible |
| T=1650ms | Screen fully interactive |

Total time to interactive: ~1,650ms (800ms network + 850ms animation)

Step 3 savings input animation on first character:
| T=0ms | Key pressed; SetSavingsAmount dispatched |
| T=0ms | runningSavingsTotal recomputed |
| T=0ms | RunningTotalBand crossfade starts (100ms) |
| T=50ms | CorpusBand crossfade starts (100ms) |
| T=100ms | RunningTotalBand shows new value |
| T=150ms | CorpusBand shows new corpus projection |
| T=300ms | Validation debounce fires (if amount 1-199: error shows in 150ms) |

---

## Appendix E: Error State Specifications

### SavingsDashboard — Network Error State

**Full-screen error (no cached data):**
```
┌──────────────────────────────────────┐
│  ←  Savings                    [⋮]  │  TopBar: primary #2E7D32
├──────────────────────────────────────┤
│                                      │
│                                      │
│            cloud_off icon            │  icon: 64dp, outline style
│             #B0B8B0 tint             │
│                                      │
│      Could not load savings data     │  titleLarge #1A1C19
│                                      │
│   Check your network connection and  │  bodyMedium #424942
│            try again.                │
│                                      │
│          ┌───────────────┐           │
│          │     Retry     │           │  FilledButton: primary bg
│          └───────────────┘           │
│                                      │
└──────────────────────────────────────┘
```

**Partial error (cached GROUP data, INDIVIDUAL unavailable):**
- GROUP tab: shows cached bar chart with LastSyncBand warning chip: "Showing cached data from 05 May 2026"
- INDIVIDUAL tab: shows error banner: "Individual savings unavailable — pull to refresh"
- LastSyncBand: surface bg #FAFAFA with sync_problem 16dp icon, amber #FF8F00 text

**Offline with stale data (>2 meetings old):**
- GROUP tab renders normally from SQLDelight cache
- Amber banner below TopBar: "Offline — data may be outdated" (12dp chip, secondary_container bg #FFDDB3)
- isFromCache=true in CycleProgressCard: sub-label appended: " (as of Meeting #3)"
- Pull-to-refresh shows CircularProgressIndicator → returns NetworkUnavailableError → snackbar: "No network — showing cached data"

### Step 3 (MeetingConductScreen) — Savings Input Error States

| Error Scenario | UI Response | Duration |
|----------------|-------------|----------|
| Amount < 200 (mandatory min) | Red outline + supporting text "Min KES 200" + errorContainer tint row | Until corrected |
| Amount > 500 (voluntary cap) | Amber outline + supporting text "Max KES 500 mandatory; extra goes voluntary" | Until corrected |
| Amount = 0 (empty field) | No error while empty; error shows on NextStep attempt | Transient |
| Non-numeric input | TextField rejects non-digits silently (keyboardType = KeyboardType.Number) | Instant |
| Total exceeds group cap | Snackbar: "Total mandatory savings KES X exceeds cycle cap" | 4000ms |

**Row-level error visual (Grace Wanjiku enters KES 100):**
```
┌──────────────────────────────────────┐  errorContainer tint #FFDAD6
│ Grace Wanjiku (Secretary)            │  bodyMedium error #B3261E
│ Mandatory  ┌────────────┐           │
│            │  KES 100  │  ✗        │  error border, X icon
│            └────────────┘           │
│            Min KES 200              │  supporting text bodySmall error
│ Voluntary  ┌────────────┐           │
│            │  KES 0    │            │  no error on voluntary
│            └────────────┘           │
│ Running total: KES 2,700            │  RunningTotalBand still updates
└──────────────────────────────────────┘
```

---

## Appendix F: Component State Matrix

### SavingsMemberRow — State Combinations

| State | Mandatory Field | Voluntary Field | Row Bg | Action |
|-------|----------------|-----------------|--------|--------|
| Empty | Neutral border | Neutral border | surface | Awaiting input |
| Valid | Primary border | Neutral border | surface | Amount accepted |
| Below min | Error border | Neutral border | errorContainer tint | Block NextStep |
| At max | Primary border | Amber border | surface | Warning on voluntary |
| Submitted | Read-only display | Read-only display | surface_variant | Not editable |
| Absent member | Grayed out | Grayed out | surface_variant at 38% | Row disabled |

**Absent member row:**
```
┌──────────────────────────────────────┐  opacity: 38%
│ Peter Otieno (Treasurer)             │  ABSENT chip: errorContainer #FFDAD6
│ [ABSENT]   mandatory: —  vol: —      │  fields disabled (grey)
└──────────────────────────────────────┘
```
Note: Absent members do not contribute to savings; RunningTotalBand excludes them automatically.

### WeeklyBarChart — Rendering States

| State | Visual | Notes |
|-------|--------|-------|
| Loading | Shimmer rectangles (6 bars, grey) | shimmer animation 1.5s repeat |
| Normal | Green bars (#2E7D32), 6 weeks | staggered grow animation |
| Single data point | 1 bar (current week) | No trend line shown |
| Zero contributions | Bar at 0dp, label "KES 0" below | floor line indicator |
| Highlighted bar | Scale 1.0→1.05, outline primary | On tap, tooltip shows |
| Bar tap tooltip | "Week 3: KES 13,200" (labelSmall) | popup above bar, 2000ms auto-dismiss |

### CycleProgressCard — Progress Values

| Progress | Color | Label |
|----------|-------|-------|
| 0-24% | secondary #FF8F00 | Early cycle |
| 25-49% | tertiary #1565C0 | Building momentum |
| 50-74% | primary #2E7D32 | On track |
| 75-99% | primary #2E7D32 | Near completion |
| 100% | primary #2E7D32 + star icon | Cycle complete |

Demo: 6/52 weeks = 11.5% → secondary #FF8F00 linear progress indicator.

---

## Appendix G: API Failure Recovery Playbook

### Scenario 1: GET savings transactions fails (Step 3 wizard)

**Trigger:** Network timeout after 30s in savingsTransactionsRepository.fetchForMember()
**Behaviour:**
1. ViewModel catches NetworkException
2. Checks SQLDelight cache: if cached data exists → fallback to cache, show amber chip "Showing cached savings"
3. If no cache: SavingsMemberRow shows skeleton with retry button per member
4. Log event: `savings_fetch_failed` with groupId + memberId + error_code

### Scenario 2: POST savings transaction fails (step 3 submit)

**Trigger:** 5xx from /clients/{clientId}/savingsaccounts/{savingsId}/transactions
**Behaviour:**
1. FailedSavingsEntry pushed to SyncQueue with priority 2
2. SyncStatus indicator turns amber in wizard header
3. Snackbar: "Savings for Grace Wanjiku queued — will sync when online"
4. Meeting submission does NOT block; proceeds without the failed transaction
5. On reconnect: SyncQueueRepository retries with exponential backoff (1s, 2s, 4s, max 30s)
6. On success: `savings_sync_recovered` analytics event

### Scenario 3: dt_group_corpus fetch fails (GroupDashboard load)

**Trigger:** 404 from /datatables/dt_group_corpus/{groupId}
**Behaviour:**
1. corpus field stays null in ViewModel
2. CorpusCard renders with KES — (em-dash) and chip: "Corpus data unavailable"
3. isCorpusInsufficient defaults to false (safe: no false block)
4. Retry button inside CorpusCard (16dp padding, outlined button)
5. Log: `corpus_fetch_404` with groupId (investigate missing datatable row)

### Scenario 4: PUT corpus update fails (meeting submission)

**Trigger:** 500 from /datatables/dt_group_corpus/{groupId}
**Behaviour:**
1. UpdateCorpusRequest queued in SyncQueue at priority 1 (highest)
2. Meeting record still saved locally via SQLDelight
3. Snackbar: "Corpus sync failed — will retry automatically"
4. SyncStatusIndicator (amber) shown on GroupDashboard until resolved
5. Retry fires within 30s; if repeated failure: push Firebase notification to Chairperson

---

## Appendix H: Accessibility Deep Dive

### Focus Order — SavingsDashboard GROUP Tab

1. TopBar back button (contentDescription: "Navigate back")
2. TopBar title: "Savings" (heading role)
3. TopBar overflow menu button
4. GROUP tab (selected, role=Tab)
5. INDIVIDUAL tab (unselected, role=Tab)
6. CycleProgressCard (contentDescription: "Cycle progress 11.5 percent — Week 6 of 52 — KES 52,500 of KES 91,000 target")
7. WeeklyBarChart (contentDescription: "Weekly group savings bar chart — 6 weeks shown — highest week KES 13,200 in Week 50")
8. Member rows 1–5 (each: "Name Role — mandatory KES X — voluntary KES Y — total KES Z")
9. LastSyncBand (contentDescription: "Data last synced at Meeting number 4 on 07 May 2026")

### Focus Order — Step 3 Savings (MeetingConductScreen)

1. Back/close button
2. Step indicator: "Step 3 of 7 — Savings Collection"
3. CorpusBand: "Group corpus fund KES 12,400. Cash on hand KES 2,000." (announces on change)
4. RunningTotalBand: "Running savings total KES 0" (announces on each change via TYPE_ANNOUNCEMENT)
5. Member 1 (Amina Hassan) mandatory field → voluntary field
6. Member 2 (Peter Otieno) — skipped if ABSENT (contentDescription: "Peter Otieno marked absent — savings not collected")
7. Member 3 (Grace Wanjiku) mandatory field → voluntary field
8. Member 4 (John Mwangi) mandatory field → voluntary field
9. Member 5 (Mary Akinyi) mandatory field → voluntary field
10. Next button: "Proceed to Step 4 Loan Repayments"

### Screen Reader Announcements for Real-Time Updates

| Event | Announcement Text | AccessibilityEvent Type |
|-------|-------------------|------------------------|
| Savings entered for Amina | "Running total KES 300" | TYPE_ANNOUNCEMENT |
| Corpus updates | "Corpus KES 12,700" | TYPE_ANNOUNCEMENT |
| Validation error appears | "Error: Grace Wanjiku minimum KES 200 required" | TYPE_WINDOW_CONTENT_CHANGED |
| Validation error clears | "Grace Wanjiku savings KES 250 accepted" | TYPE_ANNOUNCEMENT |
| All entries valid | "All savings complete — KES 1,000 total" | TYPE_ANNOUNCEMENT |

### Color Contrast Ratios

| Element | Foreground | Background | Ratio | WCAG Level |
|---------|-----------|-----------|-------|------------|
| Corpus balance large text | #2E7D32 | #FAFAFA | 4.6:1 | AA ✓ |
| Error corpus balance | #D32F2F | #FAFAFA | 4.5:1 | AA ✓ |
| CorpusBand text | #001C39 | #D2E4FF | 8.2:1 | AAA ✓ |
| RunningTotalBand | #001C39 | #D2E4FF | 8.2:1 | AAA ✓ |
| Member row primary text | #1A1C19 | #FAFAFA | 16.1:1 | AAA ✓ |
| Supporting error text | #B3261E | #FAFAFA | 5.1:1 | AA ✓ |
| Tab label (selected) | #2E7D32 | #FAFAFA | 4.6:1 | AA ✓ |
| Tab label (unselected) | #424942 | #FAFAFA | 8.7:1 | AAA ✓ |
| Amber warning text | #2A1700 | #FFDDB3 | 9.4:1 | AAA ✓ |

All interactive elements: minimum 48×48dp touch target. Error states use BOTH color AND icon/text (never color alone).

---

## Appendix I: Integration Checklist

### Before Merging Savings Collection Feature

**UI Integration:**
- [ ] SavingsDashboard navigates from GroupDashboard "View Savings" menu item
- [ ] Step 3 in MeetingConductScreen uses SavingsMemberRow composable
- [ ] Tab state preserved on screen rotation (rememberSaveable)
- [ ] Dark theme applied: all custom colors have dark-mode equivalents in design-tokens.yaml
- [ ] WeeklyBarChart renders correctly in large fonts (accessibility scale 1.3× and 1.5×)

**API Integration:**
- [ ] GET /clients/{clientId}/savingsaccounts/{savingsId}/transactions uses stale-while-revalidate TTL 180s
- [ ] GET /groups/{groupId}/accounts uses stale-while-revalidate TTL 180s
- [ ] POST savings transaction body includes locale + dateFormat fields
- [ ] SyncQueue entries for failed POSTs use priority 2 (not default 5)
- [ ] Offline writes to SQLDelight savings_transaction table use correct schema

**State Management:**
- [ ] derivedStateOf used for runningSavingsTotal (not recomputed on unrelated state changes)
- [ ] SavingsUiState.Content carries both group and individual tabs' data
- [ ] isFromCache flag propagated to LastSyncBand composable
- [ ] MeetingConductViewModel.step3Savings persists across step navigation (back/forward)

**Accessibility:**
- [ ] TalkBack announces RunningTotalBand changes (TYPE_ANNOUNCEMENT)
- [ ] All member rows have contentDescription with role + amounts
- [ ] WeeklyBarChart has contentDescription covering all 6 data points
- [ ] Error states announced without relying on color change alone

**Performance:**
- [ ] WeeklyBarChart uses Canvas (not Composable per bar) for 60fps animation
- [ ] LazyColumn for member list (not Column) — important at >10 members
- [ ] SQLDelight queries run on IO dispatcher (not Main)
- [ ] Image loading (member avatars, if added) uses Coil with memory cache
