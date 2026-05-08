# Group-Linked Savings — Mockup Specification
**Feature**: group-linked-savings | **Screen**: savings-dashboard

---

## Design Language

**System**: Material Design 3, comfortable density
**Font**: Noto Sans
**Primary**: #2E7D32 — Group savings chart bars, cycle progress bar, tab indicator
**Secondary**: #FF8F00 — Individual savings line chart, balance amounts in amber
**Tertiary**: #1565C0 — Individual member avatars
**Min touch target**: 48dp for all member rows

---

## Screen: Savings Dashboard — Group Tab

### Layout — Group Savings Content State
```
┌─────────────────────────────────────────┐
│  Savings                        [search]│  TopAppBar — surface, elevation 2dp
│  Mwangaza Women's Group                 │  subtitle: bodySmall, onSurfaceVariant
├─────────────────────────────────────────┤
│ Last synced: Today 8:30 AM              │  SyncBand — surfaceVariant bg, labelSmall
├─────────────────────────────────────────┤
│ [Group Savings ▼] [Individual]          │  TabRow — primary indicator, 48dp height
├─────────────────────────────────────────┤
│  ┌── Weekly Contributions ────────────┐ │
│  │  ▌ ▌ ▌ ▌ ▌ ▌ ▌                  │ │  Bar chart — 180dp height
│  │  ██  ██  ██  ██  ██  ██           │ │  Primary green bars
│  │  W48 W49 W50 W51 W52  W3          │ │  X-axis: week labels
│  │  KES ────────────────────────      │ │  Y-axis: KES labels
│  └────────────────────────────────────┘ │  16dp horizontal margin
├─────────────────────────────────────────┤
│ ┌─ Cycle Progress ──────────────────  ┐ │  primaryContainer #A6F1A6 bg
│ │ Cycle Progress                       │ │  labelLarge, onPrimaryContainer
│ │ ████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     │ │  LinearProgressIndicator 17.7%
│ │ KES 4,600 collected  Target: KES 26K │ │  bodyMedium, onPrimaryContainer
│ │ 17.7% of cycle target reached        │ │  labelSmall, onPrimaryContainer opacity 0.8
│ └─────────────────────────────────────┘ │  16dp margin, 12dp corner
├─────────────────────────────────────────┤
│  Per-Member Contributions               │  titleSmall, onSurfaceVariant, 16dp pad
│  [Group total: KES 4,600]               │  Chip — primaryContainer bg, onPrimaryContainer
├─────────────────────────────────────────┤
│ [AD] Amara Diallo          KES 800      │  GroupMemberSavingsRow — 72dp min
│      4 meetings · Last: KES 200    total│  avatar: secondaryContainer #FFDDB3
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │  Divider
│ [PO] Peter Otieno        KES 1,200      │
│      4 meetings · Last: KES 300    total│
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │
│ [GM] Grace Mwangi          KES 800      │
│      4 meetings · Last: KES 200    total│
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │
│ [JM] John Mwangi         KES 1,200      │
│      4 meetings · Last: KES 300    total│
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │
│ [MA] Mary Akinyi           KES 600      │
│      3 meetings · Last: KES 200    total│
└─────────────────────────────────────────┘
```

---

## Screen: Savings Dashboard — Individual Tab

### Layout — Individual Savings Content State
```
┌─────────────────────────────────────────┐
│  Savings                        [search]│
│  Mwangaza Women's Group                 │
├─────────────────────────────────────────┤
│ Last synced: Today 8:30 AM              │
├─────────────────────────────────────────┤
│ [Group Savings] [Individual ▼]          │  Individual tab selected
├─────────────────────────────────────────┤
│  ┌── Weekly Activity ──────────────── ┐ │
│  │  /\/\/\/\                          │ │  Line chart — 180dp height
│  │  /        \/\/\                    │ │  Amber #FF8F00 line, 2dp width
│  │  W48 W49 W50 W51 W52  W3          │ │  Fill below alpha 0.12
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ ┌─ Total Individual Balances ─────── ┐ │  secondaryContainer #FFDDB3 bg
│ │ Total Individual Balances           │ │  labelLarge, onSecondaryContainer
│ │           KES 4,850                 │ │  headlineMedium, onSecondaryContainer bold
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Member Balances                        │  titleSmall, onSurfaceVariant
├─────────────────────────────────────────┤
│ [AD] Amara Diallo        KES 1,500      │  IndividualMemberRow — 72dp min
│      [↑ Deposit]  KES 500 on 04 May  balance  avatar: tertiaryContainer #D2E4FF
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │  balance text: secondary #FF8F00
│ [PO] Peter Otieno          KES 750      │
│      [↑ Deposit]  KES 200 on 01 May  balance  Deposit chip: primaryContainer bg
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │
│ [GM] Grace Mwangi        KES 2,200      │
│      [↓ Withdrawal] KES 500 on 28 Apr balance  Withdrawal chip: errorContainer bg
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │
│ [JM] John Mwangi           KES 400      │
│      [↑ Deposit]  KES 100 on 25 Apr  balance
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    │
│ [MA] Mary Akinyi             KES 0      │
│      No transactions yet             balance  no chip shown
└─────────────────────────────────────────┘
```

---

## Screen: Savings Dashboard — Loading State
```
┌─────────────────────────────────────────┐
│  Savings                                │
│  Mwangaza Women's Group                 │
├─────────────────────────────────────────┤
│ [Group Savings] [Individual]            │
├─────────────────────────────────────────┤
│ ████████████████████████████████████  │  Shimmer — 180dp (chart placeholder)
│                                         │
│ ████████████████████████████████████  │  Shimmer — 80dp (cycle card)
│                                         │
│ ████████████████████████████████████  │  Shimmer — 72dp (row 1)
│ ████████████████████████████████████  │  Shimmer — 72dp (row 2)
│ ████████████████████████████████████  │  Shimmer — 72dp (row 3)
│ ████████████████████████████████████  │  Shimmer — 72dp (row 4)
│ ████████████████████████████████████  │  Shimmer — 72dp (row 5)
└─────────────────────────────────────────┘
```

---

## Component Specifications

### TopAppBar
| Property | Value |
|----------|-------|
| Title | "Savings" — titleLarge, onSurface |
| Subtitle | "Mwangaza Women's Group" — bodySmall, onSurfaceVariant |
| Actions | search icon (48×48dp) |
| Background | surface #FAFAFA |
| Elevation | 2dp (scrolled state) |

### SyncBand
| Property | Value |
|----------|-------|
| Background | surfaceVariant #DEE5DA |
| Text | "Last synced: Today 8:30 AM" — labelSmall, onSurfaceVariant |
| Padding | 4dp vertical, 16dp horizontal |
| Visibility | visible when lastSyncAt != null |

### TabRow
| Property | Value |
|----------|-------|
| Indicator color | primary #2E7D32 |
| Selected label | primary, labelLarge |
| Unselected label | onSurfaceVariant, labelMedium |
| Divider | bottom 1dp, outline color |
| Height | 48dp |

### Bar Chart (Group Savings)
| Property | Value |
|----------|-------|
| Type | Vertical bar chart |
| Bar color | primary #2E7D32 |
| Bar width | (chart_width - margins) / 7, 4dp gap between bars |
| Height | 180dp |
| X-axis labels | bodySmall, onSurfaceVariant |
| Y-axis labels | labelSmall, onSurfaceVariant |
| Grid lines | surfaceVariant, 1dp, horizontal only |
| Data | weeklyTrend.groupAmount for last 6 weeks |

### Line Chart (Individual Savings)
| Property | Value |
|----------|-------|
| Type | Line chart with area fill |
| Line color | secondary #FF8F00 |
| Line width | 2dp |
| Dot color | secondary #FF8F00, size 6dp |
| Fill color | secondary #FF8F00, alpha 0.12 |
| Height | 180dp |
| Margin horizontal | 16dp |
| Data | weeklyTrend.individualAmount for last 6 weeks |

### CycleProgressCard
| Property | Value |
|----------|-------|
| Background | primaryContainer #A6F1A6 |
| Corner radius | 12dp |
| Padding | 16dp |
| Progress bar color | primary #2E7D32 |
| Progress bar track | primary + alpha 0.3 |
| Progress bar height | 8dp, corner radius 4dp |
| Progress value | cycleCollected / cycleTarget |
| Amounts text | bodyMedium, onPrimaryContainer |
| Percent label | labelSmall, onPrimaryContainer, opacity 0.8 |

### GroupMemberSavingsRow
| Element | Spec |
|---------|------|
| Min height | 72dp |
| Padding | 12dp vertical, 16dp horizontal |
| Avatar | 40dp circle, secondaryContainer #FFDDB3 bg, initials text labelMedium onSecondaryContainer |
| Name | bodyLarge, onSurface |
| Subtitle | bodySmall, onSurfaceVariant — "{N} meetings · Last: KES {amount}" |
| Trailing amount | labelLarge, primary #2E7D32 |
| Trailing label | labelSmall, onSurfaceVariant — "total" |
| Divider | 1dp, outline color |
| Tap target | full row 72dp |

### IndividualMemberSavingsRow
| Element | Spec |
|---------|------|
| Min height | 72dp |
| Avatar | 40dp circle, tertiaryContainer #D2E4FF bg, initials text labelMedium onTertiaryContainer |
| Name | bodyLarge, onSurface |
| Transaction chip | Deposit: primaryContainer #A6F1A6 bg, onPrimaryContainer text / Withdrawal: errorContainer #FFDAD6 bg, onErrorContainer text |
| Transaction text | bodySmall, onSurfaceVariant — "KES {amount} on {date}" |
| Balance | labelLarge, secondary #FF8F00 |
| Balance label | labelSmall, onSurfaceVariant — "balance" |

### IndividualTotalCard
| Property | Value |
|----------|-------|
| Background | secondaryContainer #FFDDB3 |
| Corner radius | 12dp |
| Padding | 16dp |
| Label | labelLarge, onSecondaryContainer |
| Amount | headlineMedium, onSecondaryContainer, bold |

---

## Interaction Patterns

1. **Tab switch**: SelectTab action → 200ms crossfade between chart types and member lists; progress card visible in GROUP tab only
2. **Pull to refresh**: isRefreshing=true → PullRefreshIndicator (primary green spinner) → re-fetch API → update cached data + lastSyncAt
3. **Member row tap**: OnOpenMemberDetail → navigate to member-savings-detail with memberId + savingsType
4. **Offline pull-to-refresh**: Shows Snackbar "Cannot refresh — you're offline" — does not start spinner
5. **Background refresh on open**: Screen loads cached data immediately, starts background API fetch; when fresh data arrives, content updates in-place via Flow

---

## Accessibility

- Chart descriptions: "Weekly group savings trend — highest week W3 at KES 1,850" (contentDescription)
- Member rows: "Amara Diallo group savings KES 800 across 4 meetings — tap to view detail"
- Cycle progress: "Cycle progress 17.7% — KES 4,600 of KES 26,000 target collected"
- Deposit chip: "Deposit" (not icon alone); Withdrawal chip: "Withdrawal"
- Tab row: "Group Savings tab — currently selected" / "Individual tab — not selected"
- Balance amounts: "Amara Diallo individual savings balance KES 1,500"
