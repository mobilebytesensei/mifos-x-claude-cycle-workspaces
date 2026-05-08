# Field Officer View — Mockup Specification
**Feature**: field-officer-view | **Screen**: field-officer-dashboard
**Requirement**: FR-009

---

## Design Language

**System**: Material Design 3, comfortable density
**Font**: Noto Sans
**Primary**: #2E7D32 — GREEN health, groups KPI, filter chip active
**Secondary**: #FF8F00 — AMBER health
**Tertiary**: #1565C0 — savings KPI
**Error**: #D32F2F — RED health, loans KPI
**Min touch target**: 48dp (56dp for Export Report button)

---

## Screen: Field Officer Dashboard — Content State
```
┌─────────────────────────────────────────┐
│  Field Dashboard                [🔔][↗] │  TopAppBar — surface, 2dp elevation
│  James Otieno · Nairobi Branch          │  subtitle: bodySmall, onSurfaceVariant
├─────────────────────────────────────────┤
│  ┌────────────┐ ┌────────────┐          │  KPI Cards — 2-column grid
│  │ Total      │ │ Total      │          │  Each card: 48% width, 80dp height
│  │ Groups     │ │ Members    │          │
│  │    8       │ │   94       │          │  Groups: primaryContainer #A6F1A6 bg
│  └────────────┘ └────────────┘          │  Members: secondaryContainer #FFDDB3 bg
│  ┌────────────┐ ┌────────────┐          │
│  │ Total      │ │ Loans      │          │
│  │ Savings    │ │ Outstanding│          │
│  │ KES 142K   │ │ KES 87.5K  │          │  Savings: tertiaryContainer #D2E4FF bg
│  └────────────┘ └────────────┘          │  Loans: errorContainer #FFDAD6 bg
├─────────────────────────────────────────┤
│ [Region ▾] [Status ▾] [Overdue ▾]       │  Filter chips — FilterChip MD3
│                                         │  16dp margin horizontal
├─────────────────────────────────────────┤
│  [Export Report ↗]                      │  OutlinedButton — primary border, 48dp
│                                         │  right-aligned
├─────────────────────────────────────────┤
│  Groups (8)                             │  Section header — titleSmall, onSurfaceVariant
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │  GroupHealthCard
│ │ ● Mwangaza Women's Group       [›] │ │  health indicator: primary green ● 8dp dot
│ │   Nairobi · 12 members              │ │  subtitle: bodySmall, onSurfaceVariant
│ │   KES 47,500 savings · 0% overdue   │ │  stats: bodySmall
│ └─────────────────────────────────────┘ │  bg: surface, corner 12dp, elevation 2dp
│ ┌─────────────────────────────────────┐ │
│ │ ◑ Tumaini Savings Circle       [›] │ │  AMBER indicator #FF8F00
│ │   Nairobi · 10 members              │ │
│ │   KES 28,000 savings · 12% overdue  │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ ✕ Umoja Welfare Group          [›] │ │  RED indicator #D32F2F
│ │   Mombasa · 18 members              │ │
│ │   KES 35,000 savings · 25% overdue  │ │  errorContainer #FFDAD6 bg tint (subtle)
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ ● Pamoja                       [›] │ │  GREEN
│ │   Mombasa · 8 members               │ │
│ │   KES 18,500 savings · 3% overdue   │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ ◑ Maisha Bora Circle            [›]│ │  AMBER
│ │   Kisumu · 11 members               │ │
│ │   KES 13,000 savings · 8% overdue   │ │
│ └─────────────────────────────────────┘ │
│   [3 more groups...]                    │  Pagination / "Load more" text
└─────────────────────────────────────────┘
```

---

## Screen: Field Officer Dashboard — Filtered (Region: Nairobi)
```
┌─────────────────────────────────────────┐
│  Field Dashboard                [🔔][↗] │
│  James Otieno · Nairobi Branch          │
├─────────────────────────────────────────┤
│  [KPI Cards — same as above]            │  KPIs show totals for ALL groups (unfiltered)
├─────────────────────────────────────────┤
│ [Nairobi ✓ ×] [Status ▾] [Overdue ▾]   │  Region chip: selected state — primary bg, × to clear
├─────────────────────────────────────────┤
│  Groups (2)                             │  Count updates to filtered result count
│ ┌─────────────────────────────────────┐ │
│ │ ● Mwangaza Women's Group       [›] │ │
│ │   Nairobi · 12 members · KES 47.5K  │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ ◑ Tumaini Savings Circle       [›] │ │
│ │   Nairobi · 10 members · KES 28K    │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## Screen: Field Officer Dashboard — Loading State
```
┌─────────────────────────────────────────┐
│  Field Dashboard                        │
├─────────────────────────────────────────┤
│  ┌────────────┐ ┌────────────┐          │  Shimmer KPI cards
│  │████████████│ │████████████│          │
│  └────────────┘ └────────────┘          │
│  ┌────────────┐ ┌────────────┐          │
│  │████████████│ │████████████│          │
│  └────────────┘ └────────────┘          │
│  ████████████████████████████████████  │  Shimmer group cards
│  ████████████████████████████████████  │
│  ████████████████████████████████████  │
└─────────────────────────────────────────┘
```

---

## Component Specifications

### TopAppBar
| Property | Value |
|----------|-------|
| Title | "Field Dashboard" — titleLarge, onSurface |
| Subtitle | "{staffName} · {officeName}" — bodySmall, onSurfaceVariant |
| Actions | notifications IconButton (48×48dp), export/share IconButton |
| Background | surface #FAFAFA |
| Elevation | 2dp (scrolled) |

### KPI Card Grid
| Property | Value |
|----------|-------|
| Layout | 2-column LazyVerticalGrid, spacedBy(8dp) |
| Card width | (screenWidth - 32dp margin - 8dp gap) / 2 |
| Card height | 80dp min, wrap content |
| Corner radius | 12dp |
| Elevation | 0dp (colored bg) |
| Padding | 12dp all sides |

### KPI Card Content
| Property | Value |
|----------|-------|
| Label | labelLarge, container's onContainer color |
| Value | headlineSmall, bold, onContainer color |
| Icon | 20dp, onContainer color (groups/people/savings/loan icon) |

### KPI Colors
| KPI | Background | Text |
|-----|-----------|------|
| Total Groups | primaryContainer #A6F1A6 | onPrimaryContainer #002106 |
| Total Members | secondaryContainer #FFDDB3 | onSecondaryContainer #2A1700 |
| Total Savings | tertiaryContainer #D2E4FF | onTertiaryContainer #001C39 |
| Loans Outstanding | errorContainer #FFDAD6 | onErrorContainer #410002 |

### Filter Chips
| Property | Value |
|----------|-------|
| Type | FilterChip (MD3) — shows dropdown on tap |
| Default state | surfaceVariant bg, onSurfaceVariant text, outline border |
| Selected state | primaryContainer bg, onPrimaryContainer text, no border + × clear icon |
| Height | 32dp |
| Spacing | 8dp between chips |
| Padding | horizontal 16dp |

### GroupHealthCard
| Property | Value |
|----------|-------|
| Corner radius | 12dp |
| Elevation | 2dp |
| Min height | 80dp |
| Padding | 12dp all |
| Health dot | 8dp filled circle (icon=circle) — GREEN/AMBER/RED colored |
| Card bg | WHITE surface for GREEN/AMBER; subtle errorContainer tint for RED |
| Chevron | chevron_right 20dp, onSurfaceVariant |
| Group name | bodyLarge, onSurface |
| Subtitle | bodySmall, onSurfaceVariant — "{Region} · {memberCount} members" |
| Stats | bodySmall, onSurfaceVariant — "KES {savings} savings · {overdueRate}% overdue" |
| Tap target | full card 80dp |

### Health Indicator Dot
| Level | Color | Icon | Size |
|-------|-------|------|------|
| GREEN (< 5%) | primary #2E7D32 | circle_filled | 8dp |
| AMBER (5–20%) | secondary #FF8F00 | circle_half (adjust) | 8dp |
| RED (≥ 20%) | error #D32F2F | cancel_small | 8dp |

### Export Report Button
| Property | Value |
|----------|-------|
| Type | OutlinedButton |
| Text | "Export Report" |
| Icon | upload / share, 18dp |
| Border | 1dp, primary #2E7D32 |
| Content color | primary #2E7D32 |
| Height | 48dp |
| Width | wrap content |
| Alignment | end (right-aligned) |
| Loading state | CircularProgressIndicator 18dp when isExporting=true |

---

## Interaction Patterns

1. **Filter chip tap**: Dropdown appears with region/status/overdue options → user selects → chip shows selected value with × → filteredGroups updates → groups section header count updates
2. **Clear filter**: Tap × on selected chip → filter cleared → all groups show again
3. **Group card tap**: Row ripple → OnOpenGroupDetail(groupId) → navigate to group-detail (read-only mode for field officer role)
4. **Export Report**: OnExportReport → isExporting=true → button shows spinner → CSV generated in background (Dispatchers.IO) → Android share intent with CSV file → isExporting=false
5. **Pull to refresh**: RefreshDashboard → spinner → re-fetch all groups + loans + corpora → update KPIs and cards
6. **GREEN/AMBER/RED visual**: Health dot pulses once on screen load for RED groups (AnimatedVisibility scale 1.0 → 1.3 → 1.0, 600ms, to draw attention)

---

## Accessibility

- KPI cards: contentDescription "Total groups: 8", "Total members: 94", etc.
- Health dot: contentDescription "Health: GREEN — 0% overdue" / "Health: AMBER — 12% overdue" / "Health: CRITICAL — 25% overdue"
- Filter chips: contentDescription "Filter by Region — currently: {selected or not set}"
- Group cards: contentDescription "{groupName}, {region}, {memberCount} members, {overdueRate}% overdue, health {level}"
- Export button: "Export portfolio report as CSV"
- Chevron: "Open {groupName} group detail"
