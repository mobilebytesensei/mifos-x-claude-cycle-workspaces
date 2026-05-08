# Fines Tracking — Mockup Specification
**Feature**: fines-tracking | **Screens**: meeting-conduct (Step 1: Attendance, Step 4: Loan Review)
**Requirements**: FR-012, FR-020

---

## Design Language

**System**: Material Design 3, comfortable density
**Font**: Noto Sans
**Primary**: #2E7D32 — PRESENT toggle active state, attendance progress chip complete
**Error**: #D32F2F — ABSENT icon, fine chip border
**Warning**: warningContainer #FFF9C4 — fine policy info chip, LATE toggle
**Error container**: errorContainer #FFDAD6 — fine amount chip per member, penalty fine input border when overdue
**Min touch target**: 48dp for all segmented button segments

---

## Step 1: Attendance (FR-012)

### Layout — Step 1 Content (all 5 members, meeting #4)
```
┌─────────────────────────────────────────┐
│ ← Meeting #4        [Step 2 of 7]  [⚡] │  TopAppBar — offline badge if offline
│  [○──●─────────────────────────────]    │  MeetingWizardStepper — Attendance active
├─────────────────────────────────────────┤
│ Record Attendance                        │  titleMedium, onSurface
│ [⚠] Late: KES 50 fine · Absent: KES 100 │  Info chip — warningContainer bg, 12dp corner
├─────────────────────────────────────────┤
│ [AD] Amara Diallo    Chairperson         │  AttendanceMemberRow — 64dp min
│      [✓ Present] [🕐 Late] [✗ Absent]   │  Segmented button — PRESENT selected
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─     │  Divider
│ [PO] Peter Otieno   Treasurer            │
│      [✓ Present] [🕐 Late] [✗ Absent]   │  PRESENT selected
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─     │
│ [GM] Grace Mwangi   Secretary            │
│      [✓ Present] [🕐 Late] [✗ Absent]   │  LATE selected (amber highlight)
│      [⚠ Fine: KES 50]                   │  Fine chip — errorContainer bg
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─     │
│ [JM] John Mwangi    Member               │
│      [✓ Present] [🕐 Late] [✗ Absent]   │  PRESENT selected
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─     │
│ [MA] Mary Akinyi    Member               │
│      [✓ Present] [🕐 Late] [✗ Absent]   │  ABSENT selected (red highlight)
│      [✕ Fine: KES 100]                  │  Fine chip — errorContainer bg, error border
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─     │
│ [5/5 recorded ✓]                        │  Attendance progress chip — primaryContainer
├─────────────────────────────────────────┤
│           [← Back]   [Next →]           │  Navigation footer — 56dp buttons
└─────────────────────────────────────────┘
```

### Attendance Step States

**State A — Partially recorded (3/5 done)**
```
[AD] Amara Diallo     [✓ Present]       → green
[PO] Peter Otieno     [✓ Present]       → green
[GM] Grace Mwangi     (no selection)    → neutral outline
[JM] John Mwangi      (no selection)    → neutral outline
[MA] Mary Akinyi      (no selection)    → neutral outline
[3/5 recorded] chip — surfaceVariant bg
```

**State B — Validation error (user tries to advance without all recorded)**
```
Step validation error snackbar:
  "Please record attendance for all 5 members before proceeding."
  surfaceVariant background, onSurface text
  
Members with no selection highlighted:
  Row border: outline color, 1dp
```

**State C — All recorded (5/5), Next enabled**
```
[5/5 recorded ✓] chip — primaryContainer #A6F1A6 bg, onPrimaryContainer text
Next button: enabled, primary green
```

---

## Step 4: Loan Review (FR-020)

### Layout — Step 4 Content (2 active loans, 1 overdue)
```
┌─────────────────────────────────────────┐
│ ← Meeting #4       [Step 5 of 7]  [⚡]  │
│  [○──○──○──●───────────────────────]    │  Stepper — Loan Review active
│  Corpus: KES 13,250  Cash: KES 2,000    │  Corpus band — tertiaryContainer
├─────────────────────────────────────────┤
│ Loan Review                              │  titleMedium
│ Record repayments for active loans       │  bodySmall, onSurfaceVariant
├─────────────────────────────────────────┤
│ ┌─ Peter Otieno — Loan #L-1002 ───────┐ │  LoanReviewCard — surface, elevation 2dp
│ │ Outstanding: KES 1,500              │ │  bodyMedium, onSurface
│ │ Expected repayment: KES 375/week    │ │  bodySmall, onSurfaceVariant
│ │ Status: [✓ Current]                 │ │  Current badge — primaryContainer bg
│ │                                     │ │
│ │ Repayment Amount (KES):             │ │  TextField label
│ │ ┌───────────────────────────────┐   │ │  OutlinedTextField — 48dp height
│ │ │  375                          │   │ │  primary border when focused
│ │ └───────────────────────────────┘   │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─ Grace Mwangi — Loan #L-1003 ──────┐ │  OVERDUE loan card
│ │ Outstanding: KES 3,000              │ │
│ │ Expected repayment: KES 750/week    │ │
│ │ Status: [✕ OVERDUE — 2 weeks]       │ │  OVERDUE badge — errorContainer bg
│ │                                     │ │
│ │ Repayment Amount (KES):             │ │
│ │ ┌───────────────────────────────┐   │ │  OutlinedTextField — error border (#D32F2F)
│ │ │  750                          │   │ │
│ │ └───────────────────────────────┘   │ │
│ │                                     │ │
│ │ Penalty Fine (KES):  [FR-020]       │ │  Fine label — error red, labelSmall
│ │ ┌───────────────────────────────┐   │ │  OutlinedTextField — errorContainer bg
│ │ │  100                          │   │ │  error border always on overdue loans
│ │ └───────────────────────────────┘   │ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Total Repayments: KES 1,125            │  Summary chip — secondaryContainer
│  Total Fines (today): KES 250           │  Summary chip — errorContainer
├─────────────────────────────────────────┤
│           [← Back]   [Next →]           │
└─────────────────────────────────────────┘
```

*Total fines = attendance fines (KES 150 from step 1) + loan penalty fines (KES 100 from step 4) = KES 250*

### Step 4 — No Active Loans Empty State
```
┌─────────────────────────────────────────┐
│ Loan Review                              │
├─────────────────────────────────────────┤
│          📋                             │  Icon 48dp, onSurfaceVariant
│    No Active Loans                      │  titleMedium
│  No members have active loans this      │  bodySmall, onSurfaceVariant
│  meeting. Tap Next to continue.         │
│  [No repayments — KES 0]                │  chip
└─────────────────────────────────────────┘
```

---

## Component Specifications

### FineInfoChip (Step 1)
| Property | Value |
|----------|-------|
| Background | warningContainer #FFF9C4 |
| Text color | onWarningContainer #E65100 |
| Icon | warning_amber, 16dp |
| Text | "Late: KES 50 fine · Absent: KES 100 fine (FR-012)" |
| Corner radius | 16dp (pill) |
| Padding | 8dp vertical, 12dp horizontal |

### AttendanceMemberRow — Segmented Button States

| Segment | Selected State | Unselected State |
|---------|---------------|-----------------|
| Present | bg: primary #2E7D32, text: onPrimary #FFFFFF, icon: checkmark filled green | bg: surface, text: onSurfaceVariant, outline: outline |
| Late | bg: warningContainer #FFF9C4, text: #E65100, icon: clock amber | bg: surface, text: onSurfaceVariant |
| Absent | bg: errorContainer #FFDAD6, text: onErrorContainer #410002, icon: dismiss red | bg: surface, text: onSurfaceVariant |

Each segment: min width 72dp, height 36dp (within 48dp row)

### FineChip (per member — appears below toggle when LATE or ABSENT)
| Variant | Property | Value |
|---------|----------|-------|
| LATE fine | Background | errorContainer #FFDAD6 |
| | Text | "Fine: KES 50" |
| | Text color | onErrorContainer #410002 |
| | Icon | clock, 14dp, #E65100 |
| ABSENT fine | Background | errorContainer #FFDAD6 |
| | Text | "Fine: KES 100" |
| | Text color | onErrorContainer #410002 |
| | Icon | error_outline, 14dp, #D32F2F |
| Both | Corner radius | 8dp |
| | Padding | 4dp vertical, 8dp horizontal |
| | Margin | 4dp top (below toggle) |

### AttendanceProgressChip
| State | Background | Text | Text Color |
|-------|-----------|------|-----------|
| Incomplete (n < total) | surfaceVariant #DEE5DA | "{n}/{total} recorded" | onSurfaceVariant |
| Complete (n == total) | primaryContainer #A6F1A6 | "{total}/{total} recorded ✓" | onPrimaryContainer #002106 |

### LoanReviewCard — Current Loan
| Property | Value |
|----------|-------|
| Background | surface #FAFAFA |
| Corner radius | 12dp |
| Elevation | 2dp |
| Status badge | primaryContainer #A6F1A6 bg, "✓ Current", onPrimaryContainer text |
| Repayment field | OutlinedTextField, primary border (#2E7D32) on focus |
| Fine field | Hidden (loan is not overdue) |

### LoanReviewCard — Overdue Loan
| Property | Value |
|----------|-------|
| Status badge | errorContainer #FFDAD6 bg, "✕ OVERDUE — N weeks", onErrorContainer text |
| Repayment field | OutlinedTextField, error border (#D32F2F) always on |
| Fine label | "Penalty Fine (KES) [FR-020]" — error color label, labelSmall |
| Fine field | OutlinedTextField, errorContainer #FFDAD6 bg, error border, always visible |
| Fine field hint | "Enter penalty amount" |

### Summary Chips (Step 4 bottom)
```
Row(horizontalArrangement=spacedBy(8dp), padding=horizontal 16dp)
  SuggestionChip
    label: "Total Repayments: KES {totalRepayments}"
    containerColor: secondaryContainer #FFDDB3
    labelColor: onSecondaryContainer
  SuggestionChip
    label: "Total Fines (today): KES {totalFines}"
    containerColor: errorContainer #FFDAD6
    labelColor: onErrorContainer
```

---

## Interaction Patterns

1. **Mark LATE**: Segmented button LATE tap → SetAttendance(memberId, LATE) → lateFines[memberId]=50 → FineChip appears (AnimatedVisibility 200ms) below toggle → totalFinesCollected += 50 → corpusBand updates
2. **Mark ABSENT**: Same as LATE but KES 100, red chip variant
3. **Revert to PRESENT**: Tap PRESENT segment → SetAttendance(memberId, PRESENT) → FineChip disappears (200ms) → totalFinesCollected -= previous fine
4. **Penalty fine entry**: TextField focus on penalty fine field → user types amount → SetLoanFine(loanId, amount) on each keystroke → totalFinesCollected updates → summary chip updates
5. **Try to advance step 1 without all recorded**: NextStep action → validation fails → ShowStepError snackbar → unset members' rows show outline highlight
6. **Corpus band update on fine entry**: Each SetLoanFine triggers recompute → corpusBand text animates to new value (150ms, standard easing)

---

## Accessibility

- Segmented button segments: each has contentDescription "Mark {memberName} as {status}"
- Fine chips: contentDescription "{memberName} fine: KES {amount}"
- Attendance progress: "3 of 5 members attendance recorded — 2 remaining"
- Overdue badge: contentDescription "Loan for {memberName} is overdue by {N} weeks"
- Penalty fine field: labelText "Penalty fine amount in Kenya Shillings" + contentDescription "Enter penalty fine for {memberName}'s overdue loan"
- Error snackbar: announced as alert role
