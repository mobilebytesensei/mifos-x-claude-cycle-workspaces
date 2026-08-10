# Fines Tracking — Stitch Prompt Specification
**Feature**: fines-tracking | **Screens**: meeting-conduct Step 1 (Attendance) + Step 4 (Loan Review)
**Requirements**: FR-012, FR-020
**Stitch project**: MifosSave / mifos-x-group-banking
**Total sections**: 6

---

# SECTION 1: DESIGN SYSTEM CONTEXT

## Application Identity
MifosSave is a VSLA group banking app for rural communities. Fines tracking is embedded in the meeting wizard — the treasurer and chairperson record attendance (with automatic fine calculation) and loan repayments with optional penalty fines. The design must be firm but not punitive: fines are community-agreed policies that strengthen group discipline. Use warning amber for soft signals (late) and error red for hard signals (absent, overdue).

## Material Design 3 Token System

### Color Palette (all hex values exact)

#### Primary — VSLA Green (PRESENT state, progress indicators)
- primary: #2E7D32
- onPrimary: #FFFFFF
- primaryContainer: #A6F1A6
- onPrimaryContainer: #002106

#### Secondary — Amber (LATE attendance, secondary labels)
- secondary: #FF8F00
- onSecondary: #FFFFFF
- secondaryContainer: #FFDDB3
- onSecondaryContainer: #2A1700

#### Tertiary — Trust Blue (Corpus band background)
- tertiary: #1565C0
- onTertiary: #FFFFFF
- tertiaryContainer: #D2E4FF
- onTertiaryContainer: #001C39

#### Error — Alert Red (ABSENT state, overdue loans, fine chips)
- error: #D32F2F
- onError: #FFFFFF
- errorContainer: #FFDAD6
- onErrorContainer: #410002

#### Warning (policy chip, LATE state visual)
- warningContainer: #FFF9C4
- onWarningContainer: #E65100

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
| titleMedium | 16 | 500 | Step section headers ("Record Attendance", "Loan Review") |
| labelLarge | 14 | 500 | Button labels, repayment field labels, corpus band |
| labelMedium | 12 | 500 | Corpus band secondary text, loan card amounts |
| labelSmall | 11 | 500 | Fine chip text, penalty fine label, role pill |
| bodyLarge | 16 | 400 | Member names in rows |
| bodyMedium | 14 | 400 | Loan outstanding balance |
| bodySmall | 12 | 400 | Step subheadings, loan expected repayment |

### Spacing Scale
| Token | dp | Usage |
|-------|----|-------|
| xs | 4 | Fine chip internal padding vertical |
| sm | 8 | Fine chip padding horizontal, row gap |
| md | 12 | Card padding vertical |
| lg | 16 | Page margin, row padding horizontal |
| xl | 24 | Card padding full |

### Shape Scale
| Token | Corner Radius | Usage |
|-------|--------------|-------|
| small | 8dp | Fine chips |
| medium | 12dp | Loan review cards |
| large | 16dp | Fine policy info chip |
| full | 9999dp | Role pills, attendance progress chip |

### Motion
| Token | Duration | Easing | Usage |
|-------|----------|--------|-------|
| short_4 | 200ms | Standard | Fine chip AnimatedVisibility enter/exit |
| short_3 | 150ms | Standard | Corpus band value update |
| short_2 | 100ms | Standard | Segmented button segment select |
| medium_2 | 300ms | Emphasized | Loan card overdue border fade-in |

### Accessibility
- Min touch target: 48dp (each segment in segmented button: 48dp height minimum)
- Fine chips: paired icon + text, not color alone
- Role pills: semantic color (primary for Chairperson/Treasurer, neutral for Member)
- Error fields: labeled with error text below field, not color alone
- All alerts announced as role=alert

### Breakpoints
| Name | Range | Behavior |
|------|-------|----------|
| compact | 0–599dp | Single column, full-width |
| medium | 600–839dp | Cards max 560dp, centered |
| expanded | 840dp+ | Two-column: members left, summary right |

---

# SECTION 2: SCREEN COMPONENT TREES

## Step 1: Attendance — Full Component Tree (meeting #4, demo data)

```
MeetingConductScreen(currentStep=1)
├── Scaffold
│   ├── TopAppBar
│   │   ├── title: "Meeting #4"
│   │   ├── subtitle: "Attendance — Step 2 of 7"
│   │   ├── navigationIcon: IconButton(dismiss, onClick=NavigateBack)
│   │   └── actions: [OfflineBadge if isOffline]
│   │
│   ├── content: Column(fillMaxSize)
│   │   ├── MeetingWizardStepper(currentStep=1, totalSteps=7)
│   │   │   └── 7 steps: step 1 (Attendance) active (primary), steps 0 completed (primaryContainer)
│   │   │
│   │   └── LazyColumn(fillMaxSize, contentPadding=16dp)
│   │       ├── item: AttendanceStepHeader
│   │       │   └── Text("Record Attendance", titleMedium, onSurface)
│   │       │
│   │       ├── item: FineInfoChip
│   │       │   └── AssistChip(
│   │       │       label="Late: KES 50 fine · Absent: KES 100 fine (FR-012)",
│   │       │       containerColor=warningContainer,
│   │       │       labelColor=onWarningContainer,
│   │       │       leadingIcon=warning_amber size 16dp,
│   │       │       cornerRadius=16dp
│   │       │       )
│   │       │
│   │       ├── items: AttendanceMemberRow × 5
│   │       │   ├── Column (per member)
│   │       │   │   ├── Row(minHeight=64dp, padding=horizontal 0dp vertical 8dp)
│   │       │   │   │   ├── Avatar(initials, 40dp, secondaryContainer bg)
│   │       │   │   │   ├── Spacer(12dp)
│   │       │   │   │   ├── Column(weight=1f)
│   │       │   │   │   │   ├── Text(member.name, bodyLarge, onSurface)
│   │       │   │   │   │   └── RolePill(member.role)
│   │       │   │   │   └── SegmentedButton(
│   │       │   │   │       segments=[PRESENT, LATE, ABSENT],
│   │       │   │   │       selectedSegment=attendanceMap[member.memberId],
│   │       │   │   │       onSegmentSelected=SetAttendance
│   │       │   │   │       )
│   │       │   │   │
│   │       │   │   └── AnimatedVisibility(
│   │       │   │       visible = attendanceMap[memberId] in [LATE, ABSENT],
│   │       │   │       enter = expandVertically(200ms) + fadeIn(200ms),
│   │       │   │       exit = shrinkVertically(200ms) + fadeOut(200ms)
│   │       │   │       )
│   │       │   │       └── FineChip(status=attendanceMap[memberId], amount=lateFine/absentFine)
│   │       │   │
│   │       │   └── Divider(1dp, outline)
│   │       │
│   │       └── item: AttendanceProgressChip
│   │           └── SuggestionChip(
│   │               label="{attendanceMap.size}/{groupMembers.size} recorded{if complete: ' ✓'}",
│   │               containerColor=if(complete) primaryContainer else surfaceVariant,
│   │               labelColor=if(complete) onPrimaryContainer else onSurfaceVariant
│   │               )
│   │
│   └── NavigationFooter (sticky bottom)
│       └── Row(fillMaxWidth, padding=16dp)
│           ├── OutlinedButton("← Back", onClick=PreviousStep, width=0.45f, height=56dp)
│           └── FilledButton("Next →", onClick=NextStep, width=0.45f, height=56dp, enabled=canAdvance)
│
└── StepValidationErrorSnackbar (when ShowStepError emitted)
    └── Snackbar("Please record attendance for all 5 members before proceeding.")
```

## Step 4: Loan Review — Full Component Tree (2 loans: 1 current, 1 overdue)

```
MeetingConductScreen(currentStep=4)
├── Scaffold
│   ├── TopAppBar (same structure, subtitle="Loan Review — Step 5 of 7")
│   │
│   ├── content: Column(fillMaxSize)
│   │   ├── MeetingWizardStepper(currentStep=4)
│   │   │
│   │   ├── CorpusBand (visible when currentStep >= 2)
│   │   │   └── Row(bg=tertiaryContainer, padding=horizontal 16dp vertical 8dp)
│   │   │       ├── Text("Corpus: KES 13,250", labelLarge, onTertiaryContainer, weight=1f)
│   │   │       └── Text("Cash: KES 2,000", labelMedium, onTertiaryContainer)
│   │   │
│   │   └── LazyColumn(fillMaxSize, contentPadding=16dp, spacedBy=12dp)
│   │       ├── item: LoanReviewHeader
│   │       │   ├── Text("Loan Review", titleMedium, onSurface)
│   │       │   └── Text("Record repayments for active loans", bodySmall, onSurfaceVariant)
│   │       │
│   │       ├── item: LoanReviewCard — Peter Otieno (current)
│   │       │   └── Card(bg=surface, cornerRadius=12dp, elevation=2dp)
│   │       │       └── Column(padding=16dp)
│   │       │           ├── Row(verticalAlignment=CenterVertically)
│   │       │           │   ├── Column(weight=1f)
│   │       │           │   │   ├── Text("Peter Otieno — Loan #L-1002", labelMedium, onSurface)
│   │       │           │   │   └── Text("Outstanding: KES 1,500", bodyMedium)
│   │       │           │   └── StatusBadge("✓ Current", bg=primaryContainer, text=onPrimaryContainer)
│   │       │           ├── Text("Expected: KES 375/week", bodySmall, onSurfaceVariant)
│   │       │           ├── Spacer(12dp)
│   │       │           ├── Text("Repayment Amount (KES):", labelSmall, onSurfaceVariant)
│   │       │           └── OutlinedTextField(
│   │       │               value=loanRepayments["L-1002"],
│   │       │               onValueChange=SetLoanRepayment("L-1002", it),
│   │       │               label="Repayment",
│   │       │               keyboardType=Number,
│   │       │               height=48dp,
│   │       │               focusedBorderColor=primary
│   │       │               )
│   │       │
│   │       ├── item: LoanReviewCard — Grace Mwangi (OVERDUE)
│   │       │   └── Card(bg=surface, borderColor=error 1dp, cornerRadius=12dp, elevation=2dp)
│   │       │       └── Column(padding=16dp)
│   │       │           ├── Row
│   │       │           │   ├── Column(weight=1f)
│   │       │           │   │   ├── Text("Grace Mwangi — Loan #L-1003")
│   │       │           │   │   └── Text("Outstanding: KES 3,000")
│   │       │           │   └── StatusBadge("✕ OVERDUE — 2 weeks", bg=errorContainer, text=onErrorContainer)
│   │       │           ├── Text("Expected: KES 750/week", bodySmall, onSurfaceVariant)
│   │       │           ├── Spacer(12dp)
│   │       │           ├── Text("Repayment Amount (KES):", labelSmall, onSurfaceVariant)
│   │       │           ├── OutlinedTextField(
│   │       │           │   value=loanRepayments["L-1003"],
│   │       │           │   borderColor=error always,
│   │       │           │   )
│   │       │           ├── Spacer(8dp)
│   │       │           ├── Text("Penalty Fine (KES):  [FR-020]", labelSmall, error, fontWeight=Medium)
│   │       │           └── OutlinedTextField(
│   │       │               value=loanFines["L-1003"],
│   │       │               onValueChange=SetLoanFine("L-1003", it),
│   │       │               containerColor=errorContainer,
│   │       │               borderColor=error always,
│   │       │               keyboardType=Number,
│   │       │               height=48dp
│   │       │               )
│   │       │
│   │       └── item: LoanReviewSummaryRow
│   │           └── Row(padding=horizontal 0dp, spacedBy=8dp)
│   │               ├── SuggestionChip("Total Repayments: KES 1,125", secondaryContainer bg)
│   │               └── SuggestionChip("Total Fines (today): KES 250", errorContainer bg)
│   │
│   └── NavigationFooter (same structure)
```

---

# SECTION 3: COMPONENT SPECIFICATIONS

## MeetingWizardStepper

```kotlin
HorizontalStepper(
  steps = 7,
  currentStep = currentStep,  // 0-indexed
  completedColor = primaryContainer,   // #A6F1A6
  activeColor = primary,               // #2E7D32
  inactiveColor = outlineVariant,      // #C2C9BD
  connectorColor = outline,            // #727971
  stepSize = 28dp,
  stepLabels = ["Review", "Attendance", "Balance", "Savings", "Loans", "Apply", "Close"],
  labelStyle = MaterialTheme.typography.labelSmall,
  labelColor = onSurfaceVariant,
  modifier = Modifier.fillMaxWidth().padding(horizontal=16dp, vertical=8dp)
)

// Step 0 (Review): completed → primaryContainer bg, check icon
// Step 1 (Attendance): active → primary bg, filled circle
// Steps 2–6: inactive → outlineVariant bg
```

## CorpusBand

```kotlin
AnimatedVisibility(visible = currentStep >= 2) {
  Row(
    modifier = Modifier.fillMaxWidth().background(tertiaryContainer).padding(horizontal=16dp, vertical=8dp),
    horizontalArrangement = Arrangement.SpaceBetween,
    verticalAlignment = Alignment.CenterVertically
  ) {
    Text(
      text = "Corpus: KES ${liveCorpus.formatKES()}",
      style = MaterialTheme.typography.labelLarge,
      color = onTertiaryContainer
    )
    Text(
      text = "Cash: KES ${cashOnHand.formatKES()}",
      style = MaterialTheme.typography.labelMedium,
      color = onTertiaryContainer
    )
  }
}
// liveCorpus = openingCorpus + runningSavingsTotal + totalRepayments + totalFinesCollected - totalLoansDisbursed
// Updates with 150ms animation on each fine/repayment change
```

## SegmentedButton (Attendance Toggle)

```kotlin
SingleChoiceSegmentedButtonRow(modifier = Modifier.height(36.dp)) {
  AttendanceStatus.entries.forEachIndexed { index, status ->
    SegmentedButton(
      selected = attendanceMap[memberId] == status,
      onClick = { onSetAttendance(memberId, status) },
      shape = SegmentedButtonDefaults.itemShape(index, AttendanceStatus.entries.size),
      colors = SegmentedButtonDefaults.colors(
        activeContainerColor = when(status) {
          PRESENT -> primary
          LATE -> warningContainer
          ABSENT -> errorContainer
        },
        activeContentColor = when(status) {
          PRESENT -> onPrimary
          LATE -> onWarningContainer
          ABSENT -> onErrorContainer
        }
      )
    ) {
      Row(verticalAlignment = CenterVertically) {
        Icon(statusIcon(status), size = 14dp)
        Spacer(4.dp)
        Text(status.label, labelSmall)
      }
    }
  }
}
```

## FineChip

```kotlin
AnimatedVisibility(
  visible = attendanceMap[memberId] in listOf(LATE, ABSENT),
  enter = expandVertically(animationSpec = tween(200)) + fadeIn(tween(200)),
  exit = shrinkVertically(animationSpec = tween(200)) + fadeOut(tween(200))
) {
  AssistChip(
    onClick = {},  // non-interactive
    label = {
      Text(
        text = "Fine: KES ${if(status==LATE) 50 else 100}",
        style = MaterialTheme.typography.labelSmall,
        color = onErrorContainer
      )
    },
    leadingIcon = {
      Icon(
        imageVector = if(status == LATE) Icons.Default.Schedule else Icons.Default.ErrorOutline,
        contentDescription = null,
        tint = if(status == LATE) secondary else error,
        modifier = Modifier.size(14.dp)
      )
    },
    colors = AssistChipDefaults.assistChipColors(
      containerColor = errorContainer,
      labelColor = onErrorContainer
    ),
    border = AssistChipDefaults.assistChipBorder(
      borderColor = if(status == ABSENT) error else secondary,
      borderWidth = 1.dp
    ),
    shape = RoundedCornerShape(8.dp),
    modifier = Modifier.padding(top = 4.dp)
  )
}
```

## PenaltyFineTextField (Overdue loan, Step 4)

```kotlin
Column {
  Text(
    text = "Penalty Fine (KES):  [FR-020]",
    style = MaterialTheme.typography.labelSmall,
    color = MaterialTheme.colorScheme.error
  )
  Spacer(4.dp)
  OutlinedTextField(
    value = loanFines[loanId]?.toString() ?: "",
    onValueChange = { value -> onSetLoanFine(loanId, value.toLongOrNull() ?: 0L) },
    modifier = Modifier.fillMaxWidth().height(56.dp),
    label = { Text("Penalty amount") },
    placeholder = { Text("0") },
    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
    colors = OutlinedTextFieldDefaults.colors(
      focusedContainerColor = errorContainer,
      unfocusedContainerColor = errorContainer,
      focusedBorderColor = error,
      unfocusedBorderColor = error,    // always red on overdue loans
      focusedLabelColor = error,
      unfocusedLabelColor = onErrorContainer
    ),
    shape = RoundedCornerShape(8.dp)
  )
}
```

## StatusBadge (Loan status)

```kotlin
@Composable
fun LoanStatusBadge(isOverdue: Boolean, overdueWeeks: Int = 0) {
  val (bg, textColor, text, icon) = if (isOverdue) {
    Quad(errorContainer, onErrorContainer, "✕ OVERDUE — $overdueWeeks week${if(overdueWeeks>1) "s" else ""}", Icons.Default.Cancel)
  } else {
    Quad(primaryContainer, onPrimaryContainer, "✓ Current", Icons.Default.CheckCircle)
  }
  SuggestionChip(
    onClick = {},
    label = { Text(text, labelSmall, textColor) },
    icon = { Icon(icon, null, tint = textColor, modifier = Modifier.size(14.dp)) },
    colors = SuggestionChipDefaults.suggestionChipColors(containerColor = bg),
    shape = RoundedCornerShape(full)
  )
}
```

## RolePill

```kotlin
SuggestionChip(
  label = { Text(member.role, labelSmall) },
  colors = SuggestionChipDefaults.suggestionChipColors(
    containerColor = when(member.role) {
      "Chairperson" -> primary
      "Treasurer" -> tertiaryContainer
      "Secretary" -> secondaryContainer
      else -> surfaceVariant
    },
    labelColor = when(member.role) {
      "Chairperson" -> onPrimary
      "Treasurer" -> onTertiaryContainer
      "Secretary" -> onSecondaryContainer
      else -> onSurfaceVariant
    }
  ),
  shape = RoundedCornerShape(full),
  modifier = Modifier.height(20.dp)
)
```

---

# SECTION 4: INTERACTION FLOWS

## Flow 1: Mark Member as LATE (FR-012)

```
Treasurer taps "Late" segment for Grace Mwangi (memberId="103")
  ↓
SegmentedButton animates: onPrimary → warningContainer bg (100ms)
  ↓
SetAttendance("103", AttendanceStatus.LATE) action dispatched
  ↓
ViewModel:
  attendanceMap["103"] = LATE
  lateFines["103"] = 50L
  totalFinesCollected = lateFines.values.sum() + absentFines.values.sum() + loanFines.values.sum()
  (prev: 0L) + 50L = 50L
  ↓
FineChip for Grace Mwangi:
  AnimatedVisibility enters (expandVertically + fadeIn, 200ms)
  Text: "Fine: KES 50"
  ↓
CorpusBand:
  liveCorpus = 12,400 + 0 + 0 + 50 - 0 = 12,450
  Text animates: "Corpus: KES 12,450" (150ms standard)
  ↓
AttendanceProgressChip updates: count increments
```

## Flow 2: Mark Member as ABSENT (FR-012)

```
Treasurer taps "Absent" segment for Mary Akinyi (memberId="105")
  ↓
SegmentedButton animates: → errorContainer bg (100ms)
  ↓
SetAttendance("105", AttendanceStatus.ABSENT) action
  ↓
absentFines["105"] = 100L
totalFinesCollected = 50L + 100L = 150L
  ↓
FineChip appears (200ms):
  Icon: error_outline, 14dp, error color
  Text: "Fine: KES 100"
  Border: 1dp error #D32F2F
  ↓
CorpusBand: "Corpus: KES 12,550" (150ms)
```

## Flow 3: Revert ABSENT to PRESENT

```
Treasurer taps "Present" segment for Mary Akinyi
  ↓
SetAttendance("105", PRESENT)
  ↓
absentFines.remove("105")
totalFinesCollected = 50L - 100L = 50L (only Grace Mwangi's late fine remains)
  ↓
FineChip: AnimatedVisibility exits (shrinkVertically + fadeOut, 200ms)
CorpusBand updates back: "Corpus: KES 12,450"
```

## Flow 4: Attendance Step Advance Validation

```
Treasurer taps "Next →" with 4/5 members recorded (Grace Mwangi unset)
  ↓
NextStep action
  ↓
Validation: attendanceMap.size (4) < groupMembers.size (5) → FAIL
  ↓
ShowStepError("Please record attendance for all 5 members before proceeding.")
  ↓
Snackbar appears at bottom (above navigation footer)
Unset member row (Grace Mwangi): Row border highlight — outline 1dp
  ↓
Treasurer sets Grace Mwangi as PRESENT
attendanceMap.size == 5 → canAdvance = true
  ↓
Next button: enabled with full primary green color
```

## Flow 5: Enter Loan Penalty Fine (FR-020) — Step 4

```
[Step 4 loaded — Grace Mwangi's loan #L-1003 shows OVERDUE badge]
  ↓
Treasurer taps penalty fine TextField
Keyboard opens (NumberKeyboard)
  ↓
Treasurer types "100"
  ↓
onValueChange: SetLoanFine("L-1003", 100L)
  ↓
ViewModel:
  loanFines["L-1003"] = 100L
  totalFinesCollected = 50L (from step 1 attendance) + 0 (no other loan fines) + 100L = 150L
  closingCorpus recalculated
  ↓
CorpusBand: "Corpus: KES 13,550" (includes all fines now)
  ↓
Summary chip updates: "Total Fines (today): KES 250" (150 attendance + 100 loan penalty)
```

## Flow 6: Meeting Submit — Fines Included in API Calls

```
[Step 6 — SubmitMeeting action triggered]
  ↓
ScreenState → Submitting (overlay)
  ↓
Sequential API calls:

1. POST /datatables/dt_meeting_record
   Body includes:
   { "totalFinesCollected": 250, "closingCorpus": 13550, ... }

2. POST /datatables/dt_meeting_attendance per member
   Grace Mwangi: { "status": "LATE", "fineAmount": 50 }
   Mary Akinyi: { "status": "ABSENT", "fineAmount": 100 }
   Others: { "status": "PRESENT", "fineAmount": 0 }

3. Corpus update: PUT /datatables/dt_group_corpus/7
   { "corpusBalance": 13550, ... }
  ↓
All 2xx → NavigateToMeetingSummary
```

---

# SECTION 5: REAL DATA SPECIFICATION

## Meeting Context
**Group**: Mwangaza Women's Group
**groupId**: 7
**meetingId**: "meeting-7-4"
**meetingNumber**: 4
**meetingDate**: 06 May 2026
**openingCorpus**: KES 12,400
**cashOnHand**: KES 2,000

## Attendance Data (Step 1 demo)

| Member | memberId | Role | Status | Fine |
|--------|----------|------|--------|------|
| Amara Diallo | 101 | Chairperson | PRESENT | KES 0 |
| Peter Otieno | 102 | Treasurer | PRESENT | KES 0 |
| Grace Mwangi | 103 | Secretary | LATE | KES 50 |
| John Mwangi | 104 | Member | PRESENT | KES 0 |
| Mary Akinyi | 105 | Member | ABSENT | KES 100 |

**attendanceFinesTotal**: KES 150
**attendanceCount (PRESENT)**: 3

**Step 1 ViewModel state**:
```kotlin
attendanceMap = mapOf(
  "101" to PRESENT,
  "102" to PRESENT,
  "103" to LATE,
  "104" to PRESENT,
  "105" to ABSENT
)
lateFines = mapOf("103" to 50L)
absentFines = mapOf("105" to 100L)
totalFinesCollected = 150L  // only attendance fines at end of step 1
```

## Active Loans Data (Step 4 demo)

| loanId | Member | Principal | Outstanding | Expected Weekly | Status | Overdue Weeks |
|--------|--------|-----------|-------------|----------------|--------|--------------|
| L-1002 | Peter Otieno | KES 1,500 | KES 1,500 | KES 375/week | CURRENT | 0 |
| L-1003 | Grace Mwangi | KES 3,000 | KES 3,000 | KES 750/week | OVERDUE | 2 |

## Step 4 Fine Entry (demo)

**Loan penalty fines entered by treasurer**:
```kotlin
loanFines = mapOf("L-1003" to 100L)  // Grace Mwangi overdue penalty
loanRepayments = mapOf(
  "L-1002" to 375L,  // Peter Otieno standard repayment
  "L-1003" to 750L   // Grace Mwangi repayment + separate fine
)
totalRepayments = 1_125L
```

## Final Totals (all steps complete)

```kotlin
// After all steps, before submit:
totalFinesCollected = 150L (attendance) + 100L (loan penalty) = 250L
totalSavingsCollected = 1_000L  // 4 members × ~KES 250 avg
totalRepaymentsReceived = 1_125L
totalLoansDisbursed = 0L  // no new loans approved
openingCorpus = 12_400L
closingCorpus = 12_400 + 1_000 + 1_125 + 250 - 0 = 14_775L
```

## CreateMeetingRecordRequest (final)

```json
{
  "groupId": 7,
  "meetingNumber": 4,
  "actualDate": "06 May 2026",
  "openingCorpus": 12400,
  "closingCorpus": 14775,
  "totalSavingsCollected": 1000,
  "totalRepaymentsReceived": 1125,
  "totalLoansDisbursed": 0,
  "totalFinesCollected": 250,
  "attendanceCount": 3,
  "locale": "en",
  "dateFormat": "dd MMMM yyyy"
}
```

## AttendanceRequest (LATE — Grace Mwangi)

```json
{
  "meetingId": "meeting-7-4",
  "memberId": "103",
  "status": "LATE",
  "fineAmount": 50,
  "locale": "en"
}
```

## AttendanceRequest (ABSENT — Mary Akinyi)

```json
{
  "meetingId": "meeting-7-4",
  "memberId": "105",
  "status": "ABSENT",
  "fineAmount": 100,
  "locale": "en"
}
```

---

# SECTION 6: RESPONSIVE LAYOUT + ADAPTIVE BEHAVIOR

## Compact Layout (0–599dp) — Primary target (360dp phone)

### Step 1 Attendance Layout
```
Screen width: 360dp

TopAppBar: fullWidth, 64dp (two-line)
Stepper: fullWidth, 44dp, 7 circles with connector lines
LazyColumn: contentPadding=16dp

AttendanceMemberRow:
  minHeight: 64dp
  Avatar: 40dp circle
  Content column: weight=1f, about 160dp
  SegmentedButton: 3 segments × 60dp = 180dp (fills remaining width)
  FineChip: full width, appears below toggle

FineInfoChip: wrapContent, left-aligned
AttendanceProgressChip: wrapContent

NavigationFooter: sticky bottom, height=72dp, buttons side by side
  Back: 48% width, OutlinedButton
  Next: 48% width, FilledButton
```

### Segmented Button at 360dp
```
Available width: 360dp - 32dp margin - 40dp avatar - 12dp spacer - 12dp content = ~264dp for SegmentedButton
3 segments: 264dp / 3 = 88dp per segment
Min touch: 88dp width × 36dp height → fits (width exceeds minimum 48dp)
```

## Medium Layout (600–839dp) — Tablet

```
Step 1 Attendance:
  Card: maxWidth=560dp, centered
  SegmentedButton: 3 segments, more comfortable 100dp+ each

Step 4 Loan Review:
  Loan cards: maxWidth=560dp
  Two-column possible: member info left, repayment inputs right
```

## Expanded Layout (840dp+)

```
Step 1:
  Row(fillMaxSize)
  ├── Column(weight=0.5f) — Member list
  │   LazyColumn: AttendanceMemberRows
  └── Column(weight=0.5f) — Live summary
      AttendanceProgressCard:
        "3/5 recorded"
        Fine breakdown: LATE: KES 50 × 1, ABSENT: KES 100 × 1
        Total fines: KES 150
      CorpusProjection card

Step 4:
  Row(fillMaxSize)
  ├── Column(weight=0.6f) — Loan cards
  └── Column(weight=0.4f) — Summary
      Total Repayments: KES X
      Total Fines: KES Y
      Corpus impact preview
```

## Dark Theme

| Light | Dark |
|-------|------|
| warningContainer #FFF9C4 | #3A2600 (dark amber) |
| onWarningContainer #E65100 | #FFB74D |
| errorContainer #FFDAD6 | #410002 |
| onErrorContainer #410002 | #FFDAD6 |
| tertiaryContainer #D2E4FF | #004A9C |
| onTertiaryContainer #001C39 | #D2E4FF |
| surface #FAFAFA | #1C1C1E |
| primary #2E7D32 | #48C454 |

## Validation Error UX

```
Snackbar positioning:
  Bottom of screen, above NavigationFooter
  Padding bottom = NavigationFooter height + 8dp

Unset member row highlight:
  Row: border 1dp outline color appears (AnimatedBorderStroke 200ms)
  Label below row: Text("Tap to set attendance", labelSmall, onSurfaceVariant italic)
  Duration: 2 seconds, then auto-dismiss highlight
```

## Fine Policy Customization (v2.0.0 note)

In v1.0.0, fine amounts are constants: LATE=50, ABSENT=100. In v2.0.0, amounts will be configurable via group settings (dt_group_config). The FineInfoChip text will update dynamically:
```
"Late: KES {groupConfig.lateFineAmount} · Absent: KES {groupConfig.absentFineAmount} (FR-012)"
```
Stitch designers: keep the chip text dynamic (no hardcoded KES values in chip labels).

---

## Component State Matrix

Full state definitions for every interactive component in fines-tracking. MifosSave tokens: primary #2E7D32 (PRESENT), secondary #FF8F00 (LATE), error #D32F2F (ABSENT/overdue).

### AttendanceToggle — per-member row in Step 1 (PRESENT / LATE / ABSENT)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| AttendanceButton PRESENT | selected | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | none | 0dp | true | true |
| AttendanceButton PRESENT | unselected | surface #FAFAFA | onSurfaceVariant #424942 | 1dp outlineVariant #C2C9BD | 0dp | true | true |
| AttendanceButton PRESENT | pressed | primaryContainer #A6F1A6 (80% opacity) | onPrimaryContainer #002106 | none | 0dp | true | true |
| AttendanceButton PRESENT | focused | surface #FAFAFA | onSurface #1A1C19 | 2dp primary #2E7D32 | 0dp | true | true |
| AttendanceButton LATE | selected | secondaryContainer #FFDDB3 | onSecondaryContainer #2A1700 | none | 0dp | true | true |
| AttendanceButton LATE | unselected | surface #FAFAFA | onSurfaceVariant #424942 | 1dp outlineVariant #C2C9BD | 0dp | true | true |
| AttendanceButton LATE | pressed | secondaryContainer #FFDDB3 (80% opacity) | onSecondaryContainer #2A1700 | none | 0dp | true | true |
| AttendanceButton ABSENT | selected | errorContainer #FFDAD6 | onErrorContainer #410002 | 1dp error #D32F2F | 0dp | true | true |
| AttendanceButton ABSENT | unselected | surface #FAFAFA | onSurfaceVariant #424942 | 1dp outlineVariant #C2C9BD | 0dp | true | true |
| AttendanceButton ABSENT | pressed | errorContainer #FFDAD6 (80% opacity) | onErrorContainer #410002 | none | 0dp | true | true |
| AttendanceButton (any) | disabled (meeting locked) | surface at 38% | onSurface at 38% | 1dp at 38% | 0dp | false | true |

### FineChip — automatic fine display per attendance row

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| FineChip LATE | visible | secondaryContainer #FFDDB3 | onSecondaryContainer #2A1700 | none | 0dp | false | true |
| FineChip ABSENT | visible | errorContainer #FFDAD6 | onErrorContainer #410002 | none | 0dp | false | true |
| FineChip PRESENT | hidden | — | — | — | — | false | false |
| FineChip LATE | animating in | secondaryContainer (scale 0.8→1.0) | same | none | 0dp | false | true |
| FineChip ABSENT | animating in | errorContainer (scale 0.8→1.0) | same | none | 0dp | false | true |

### MemberAttendanceRow (Step 1 full row)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| AttendanceRow | PRESENT | surface #FAFAFA | onSurface #1A1C19 | none | 0dp | true | true |
| AttendanceRow | LATE | warningContainer #FFF9C4 tint | onWarningContainer #E65100 | none | 0dp | true | true |
| AttendanceRow | ABSENT | errorContainer #FFDAD6 light tint | onErrorContainer #410002 | 1dp error #D32F2F left accent | 0dp | true | true |
| AttendanceRow | unset (validation error) | surface #FAFAFA | onSurface #1A1C19 | 1dp error #D32F2F animated | 0dp | true | true |
| AttendanceRow | focused (d-pad) | surface #FAFAFA | onSurface #1A1C19 | 2dp primary #2E7D32 | 0dp | true | true |
| AttendanceRow (loading skeleton) | shimmer | surfaceVariant | n/a | none | 0dp | false | true |

### RepaymentField (Step 4 — per-member loan repayment amount)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| RepaymentField | empty (idle) | surfaceVariant #DEE5DA | onSurfaceVariant #424942 | 1dp outlineVariant #C2C9BD | 0dp | true | true |
| RepaymentField | focused | surfaceVariant #DEE5DA | onSurface #1A1C19 | 2dp primary #2E7D32 | 0dp | true | true |
| RepaymentField | filled (valid) | surfaceVariant #DEE5DA | onSurface #1A1C19 | 1dp outlineVariant | 0dp | true | true |
| RepaymentField | overpayment error | errorContainer #FFDAD6 | onErrorContainer #410002 | 2dp error #D32F2F | 0dp | true | true |
| RepaymentField | disabled (no active loan) | surface at 38% opacity | onSurface at 38% | none | 0dp | false | true |
| RepaymentField | read-only (locked) | surfaceVariant at 60% | onSurfaceVariant #424942 | none | 0dp | false | false (hidden if no loan) |

### PenaltyFineChip (Step 4 — overdue loan penalty toggle)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| PenaltyChip | unselected (waive) | surface #FAFAFA | onSurfaceVariant #424942 | 1dp outlineVariant | 0dp | true | true |
| PenaltyChip | selected (apply fine) | errorContainer #FFDAD6 | onErrorContainer #410002 | none | 0dp | true | true |
| PenaltyChip | focused | surface #FAFAFA | onSurface #1A1C19 | 2dp primary #2E7D32 | 0dp | true | true |
| PenaltyChip | disabled | surface at 38% | onSurface at 38% | none | 0dp | false | false (hidden if no overdue penalty) |

### FineInfoChip (policy reminder at top of Step 1)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| FineInfoChip | default | tertiaryContainer #D2E4FF | onTertiaryContainer #001C39 | none | 0dp | true | true |
| FineInfoChip | expanded (tapped to see detail) | tertiaryContainer #D2E4FF | onTertiaryContainer #001C39 | 1dp tertiary #1565C0 | 0dp | true | true |
| FineInfoChip | focused | tertiaryContainer #D2E4FF | onTertiaryContainer #001C39 | 2dp tertiary #1565C0 | 0dp | true | true |

### StepNavigationButton (Next Step / Previous Step)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| NextStepButton | default | primary #2E7D32 | onPrimary #FFFFFF | none | 4dp | true | true |
| NextStepButton | pressed | primary #1B5E20 | onPrimary #FFFFFF | none | 8dp | true | true |
| NextStepButton | focused | primary #2E7D32 | onPrimary #FFFFFF | 2dp onPrimary ring | 4dp | true | true |
| NextStepButton | loading | primary #2E7D32 | CircularProgress white | none | 4dp | false | true |
| NextStepButton | disabled (validation incomplete) | surface #FAFAFA | onSurface at 38% | none | 0dp | false | true |
| BackStepButton | default | surface #FAFAFA | primary #2E7D32 | 1dp primary | 0dp | true | true |
| BackStepButton | pressed | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | none | 0dp | true | true |

---

## API Failure & Recovery Playbook

### POST /meetings/{meetingId}/attendance (record attendance with fines)

| Failure Type | Detection | User-Facing Response | Recovery |
|---|---|---|---|
| Network timeout | IOException after 10s | "Attendance not saved — queued for retry" | Add to SyncQueue; show pending badge on meetings nav tab |
| 401 Unauthorized | HTTP 401 | Navigate to login; return to Step 1 after re-auth | Preserve all attendance selections in SavedStateHandle |
| 409 Conflict | HTTP 409 (attendance already recorded) | "Attendance already recorded for this meeting — view recorded data?" | Navigate to view-only attendance summary |
| 422 Validation | HTTP 422 (unset member) | "All members must have attendance set before saving" | Scroll to first unset row; highlight with error border |
| 500 Server Error | HTTP 5xx | Snackbar: "Server error — attendance queued" | Queue to SyncQueue; retry 1s → 2s → 4s |
| Offline | No network | "Offline — attendance saved locally, will sync when connected" | SyncQueue entry; pending badge; auto-sync on reconnect |

SyncQueue entry format: `{ type: "ATTENDANCE", meetingId, records: [{memberId, status, fineAmount}] }`

### POST /meetings/{meetingId}/repayments (record loan repayments + penalties)

| Failure Type | Detection | User-Facing Response | Recovery |
|---|---|---|---|
| Network timeout | IOException | "Repayment not saved — queued" | SyncQueue; pending badge; do NOT allow double-entry |
| 401 Unauthorized | HTTP 401 | Re-auth flow; preserve all repayment amounts | Re-submit after re-auth |
| 409 Conflict | HTTP 409 (duplicate repayment) | "Repayment already recorded for {memberName} this period" | Skip duplicate; continue with remaining members |
| 422 Overpayment | HTTP 422 | "{memberName} repayment KES {amount} exceeds outstanding KES {outstanding}" | Highlight field in error; auto-suggest outstanding balance |
| 500 Server Error | HTTP 5xx | Snackbar: "Server error — repayment queued" | SyncQueue; retry strategy |
| Offline | No network | "Offline — repayments saved locally" | SyncQueue; auto-retry on reconnect |

### GET /meetings/{meetingId}/template (load meeting template with member list)

| Failure Type | Detection | User-Facing Response | Recovery |
|---|---|---|---|
| Network timeout | IOException | Show cached template from Room DB | Proceed with cached data; mark as "unverified" |
| 401 Unauthorized | HTTP 401 | Re-auth | Return to same meeting step |
| 404 Not Found | HTTP 404 | "Meeting not found — it may have been cancelled" | Navigate back to meetings list |
| 500 Server Error | HTTP 5xx | Error snackbar; offer retry | Manual retry; fallback to cached |
| Offline | No network | Show cached member list with last known attendance | Allow recording against cache; sync later |

### Fine Auto-Calculation — Local (no API)

Fine calculation happens entirely client-side — no API call:
- LATE attendance: fine = `groupConfig.lateFineAmount` (default KES 50) — instant, no network
- ABSENT attendance: fine = `groupConfig.absentFineAmount` (default KES 100) — instant, no network
- Penalty fine (overdue loan): fine = `loanProduct.penaltyRate × outstandingAmount` — instant calculation
- Calculation failure (e.g. null groupConfig): fallback to hardcoded KES 50/KES 100; show "Using default fine amounts" info chip

---

## Screen Reader & Accessibility Deep Dive

### Step 1 — Attendance Recording Focus Order (TalkBack / D-pad)

1. TopAppBar back arrow — "Go back to meeting list, button"
2. TopAppBar title — "Record Attendance, Step 1 of 4" (heading)
3. Step progress indicator — "Step 1 of 4 — Attendance" (status)
4. FineInfoChip — "Fine policy: Late KES 50 · Absent KES 100 (FR-012), tap for details, button"
5. "Record Attendance" section header — "Record attendance for 5 members, heading"
6. MemberRow — Amara Diallo: "Amara Diallo, attendance not set — select Present, Late, or Absent" (role: group)
7.   AttendanceButton PRESENT — "Present — no fine, not selected, button"
8.   AttendanceButton LATE — "Late — fine KES 50, not selected, button"
9.   AttendanceButton ABSENT — "Absent — fine KES 100, not selected, button"
10. MemberRow — Grace Mwangi: same pattern
11. MemberRow — Peter Otieno: same pattern
12. MemberRow — Mary Akinyi: same pattern
13. MemberRow — Fatima Ouedraogo: same pattern
14. Fine summary chip — "Total fines this meeting: KES 150 — 1 late, 1 absent" (status)
15. "Next: Step 2" button — "Go to step 2, button" (disabled if any member unset)

### Step 4 — Loan Review Focus Order

1. TopAppBar back arrow — "Go back to step 3, button"
2. TopAppBar title — "Loan Review, Step 4 of 4" (heading)
3. Step progress — "Step 4 of 4 — Loan Review" (status)
4. Corpus band — "Group corpus: KES 36,400, includes today's contributions" (status)
5. "Loan Review" section header — "Review loan repayments for active borrowers, heading"
6. LoanRepaymentRow — Amara Diallo: "Amara Diallo, active loan, outstanding KES 5,000, enter repayment amount"
7.   RepaymentField — "Repayment amount in KES for Amara Diallo, required, text field"
8.   PenaltyChip — "Apply overdue penalty fine, not selected, button" (visible only if overdue)
9. LoanRepaymentRow — Grace Mwangi (no active loan): "Grace Mwangi — no active loan" (status, skip)
10. LoanRepaymentRow — Peter Otieno: "Peter Otieno, overdue loan 12 days, outstanding KES 8,000"
11.   RepaymentField — "Repayment amount for Peter Otieno"
12.   PenaltyChip — "Apply overdue penalty fine KES 240, not selected, button"
13. Fine totals summary — "Total attendance fines: KES 150 · Total penalty fines: KES 240 · Grand total: KES 390"
14. "Save & Complete" button — "Save meeting record and complete, button"
15. "Back to Step 3" button — "Go back to step 3, button"

### TalkBack Announcement Strings

| Element | Announcement |
|---|---|
| FineInfoChip | "Fine policy: KES {lateFine} for late, KES {absentFine} for absent, double-tap to see full policy" |
| AttendanceButton PRESENT (selected) | "Present selected for {memberName} — no fine" |
| AttendanceButton LATE (selected) | "Late selected for {memberName} — KES {lateFine} fine applied" |
| AttendanceButton ABSENT (selected) | "Absent selected for {memberName} — KES {absentFine} fine applied" |
| FineChip LATE (appears) | "Fine KES {amount} added for {memberName}" |
| FineChip ABSENT (appears) | "Fine KES {amount} added for {memberName}" |
| RepaymentField | "{memberName}, outstanding KES {outstanding}, enter repayment amount" |
| PenaltyChip (unselected) | "Overdue penalty not applied — double-tap to add KES {penaltyAmount} fine" |
| PenaltyChip (selected) | "Overdue penalty KES {penaltyAmount} applied for {memberName}" |
| Fine summary | "Total fines: KES {total} — {lateCount} late, {absentCount} absent, {penaltyCount} penalty" |
| Validation error (unset member) | "Attendance not set for {memberName} — must be set before proceeding" (assertive) |
| Next step button (disabled) | "Next step unavailable — all members must have attendance recorded" |
| Save success | "Meeting record saved — KES {totalFines} in fines recorded for Mwangaza Women's Group" (assertive) |

### Content Descriptions — Icons and Indicators

| Icon | Content Description |
|---|---|
| check (PRESENT button icon) | "Present" |
| schedule (LATE button icon) | "Late" |
| close / cancel (ABSENT button icon) | "Absent" |
| info (FineInfoChip icon) | "Fine policy information" |
| warning_amber (LATE row indicator) | "Late — fine applies" |
| error_outline (ABSENT row indicator) | "Absent — fine applies" |
| trending_down (overdue loan) | "Loan is overdue" |
| account_balance (corpus band) | "Group corpus balance" |

### Live Region Announcements

- Attendance set: "{memberName} marked as {status}. {fineMessage}" (polite)
- Fine total updates: "Total fines updated: KES {total}" (polite, on each change)
- Validation error (attempt to advance): "Cannot proceed — {count} member(s) have no attendance set" (assertive)
- Meeting save complete: "Meeting attendance and loan review saved successfully" (assertive)
- Offline queued: "Data saved locally — will sync when you reconnect" (polite)
- Sync complete: "Meeting data synced to server" (polite)

### WCAG AA Contrast Ratios

| Text / Background | Contrast Ratio | Pass |
|---|---|---|
| onPrimaryContainer #002106 / primaryContainer #A6F1A6 | 11.2:1 | AAA |
| onSecondaryContainer #2A1700 / secondaryContainer #FFDDB3 | 9.1:1 | AAA |
| onErrorContainer #410002 / errorContainer #FFDAD6 | 9.8:1 | AAA |
| onTertiaryContainer #001C39 / tertiaryContainer #D2E4FF | 10.4:1 | AAA |
| onSurface #1C1C1C / surface #FAFAFA | 17.4:1 | AAA |
| onWarningContainer #E65100 / warningContainer #FFF9C4 | 4.8:1 | AA |
| onSurfaceVariant #424942 / surfaceVariant #DEE5DA | 5.9:1 | AA |

### Keyboard Navigation

- `Tab` / `Shift+Tab`: move focus forward/backward through all interactive elements in step
- `Arrow keys` within AttendanceToggle: left/right selects PRESENT / LATE / ABSENT
- `Enter` / `Space`: activate focused button, toggle chip, advance step
- `Escape`: go back one step (Step 2→1, Step 4→3); from Step 1, confirm before leaving meeting
- All attendance states use both color AND icon — never color alone (WCAG 1.4.1)
- Error states highlight with both border AND icon AND error message text

---

## Animation & Motion Spec

### Step Transitions

| Transition | Type | Duration | Easing |
|---|---|---|---|
| Step 1 → Step 2 | shared axis X (forward) | 300ms | EmphasizedDecelerate |
| Step 2 → Step 1 (back) | shared axis X (backward) | 300ms | EmphasizedAccelerate |
| Step 3 → Step 4 | shared axis X (forward) | 300ms | EmphasizedDecelerate |
| Step 4 → Step 3 (back) | shared axis X (backward) | 300ms | EmphasizedAccelerate |
| Step 4 → completion | fade through | 400ms | Standard |

### Component Micro-Animations

| Component | Animation | Duration | Easing |
|---|---|---|---|
| FineChip appear (LATE/ABSENT selected) | scale 0.8→1.0 + fade 0→1 | 200ms | EmphasizedDecelerate |
| FineChip dismiss (PRESENT selected) | scale 1.0→0.8 + fade 1→0 | 150ms | EmphasizedAccelerate |
| AttendanceRow ABSENT tint | background color interpolation (surface→errorContainer tint) | 200ms | Standard |
| AttendanceRow LATE tint | background color interpolation (surface→warningContainer) | 200ms | Standard |
| AttendanceRow PRESENT restore | background color interpolation back to surface | 200ms | Standard |
| Fine total chip update | text cross-fade (old amount → new amount) | 150ms | Standard |
| Validation error border | animated border stroke appear 200ms + pulsate 2× | 600ms total | Standard |
| Next step button enable | background color (surfaceVariant → primary #2E7D32) | 200ms | Standard |
| BottomSheet (FineInfoChip detail) | slide up 350ms (EmphasizedDecelerate) |
| Confirm dialog (save meeting) | scale 0.8→1.0 with 250ms fade | 250ms | EmphasizedDecelerate |
| Step progress indicator advance | fill animation for completed step dot | 300ms | Standard |

### Loading Skeleton — Step 1 Attendance

```
Step1Skeleton:
  Column(padding=16dp, spacedBy=12dp)
    // FineInfoChip skeleton
    ShimmerBox(width=240dp, height=32dp, cornerRadius=16dp)
    // Section header skeleton
    ShimmerBox(width=160dp, height=20dp, cornerRadius=4dp)
    // 5× member row skeletons
    repeat(5) {
      Row(fillMaxWidth, spacedBy=8dp, verticalAlignment=Center)
        ShimmerBox(width=40dp, height=40dp, cornerRadius=20dp) // avatar
        ShimmerBox(weight=1f, height=20dp, cornerRadius=4dp)   // name
        Row(spacedBy=4dp)
          ShimmerBox(width=72dp, height=36dp, cornerRadius=8dp) // P button
          ShimmerBox(width=72dp, height=36dp, cornerRadius=8dp) // L button
          ShimmerBox(width=72dp, height=36dp, cornerRadius=8dp) // A button
    }
// ShimmerBox: alpha 0.3→1.0→0.3 over 1200ms, surfaceVariant #DEE5DA
```

---

## Test & QA Annotations

### UI Test Tags

| Component | testTag |
|---|---|
| Step 1 root | `MeetingStep1_Root` |
| Step 4 root | `MeetingStep4_Root` |
| Fine info chip | `FinesTracking_FineInfoChip` |
| Member attendance row | `AttendanceRow_{memberId}` |
| Present button (per member) | `AttendanceBtn_{memberId}_Present` |
| Late button (per member) | `AttendanceBtn_{memberId}_Late` |
| Absent button (per member) | `AttendanceBtn_{memberId}_Absent` |
| Fine chip on row | `FineChip_{memberId}` |
| Fine total summary chip | `FinesTracking_FineTotalChip` |
| Repayment field | `RepaymentField_{memberId}` |
| Penalty fine chip | `PenaltyChip_{memberId}` |
| Next step button | `MeetingStep_NextButton` |
| Back step button | `MeetingStep_BackButton` |
| Save & complete button | `MeetingStep4_SaveButton` |
| Corpus band | `MeetingStep4_CorpusBand` |
| Error snackbar | `Snackbar_Error` |
| Validation error highlight | `AttendanceRow_{memberId}_Error` |

### Required Test Scenarios — Step 1 (Attendance)

```
Given: 5 members in Mwangaza Women's Group (Amara Diallo, Grace Mwangi, Peter Otieno, Mary Akinyi, Fatima Ouedraogo)
When: Step 1 loads
Then: 5 AttendanceRows shown; all buttons unselected; FineInfoChip visible; NextButton disabled

Given: Amara Diallo marked PRESENT, Grace Mwangi marked PRESENT, others not set
When: user taps NextButton
Then: button remains disabled; unset rows (Peter, Mary, Fatima) highlight with error border; TalkBack announces "Cannot proceed — 3 members have no attendance set"

Given: Amara Diallo marked LATE
When: LATE button tapped
Then: FineChip appears (secondaryContainer, "KES 50") with scale animation; row tints to warningContainer; fine total chip updates to "KES 50"

Given: Grace Mwangi marked ABSENT
When: ABSENT button tapped
Then: FineChip appears (errorContainer, "KES 100") with scale animation; row tints to errorContainer; error left-border accent appears; fine total updates to "KES 150"

Given: all 5 members have attendance set (2 PRESENT, 1 LATE, 2 ABSENT)
When: NextButton checked
Then: NextButton enabled (primary green); tapping advances to Step 2; fine totals preserved
```

### Required Test Scenarios — Step 4 (Loan Review)

```
Given: Peter Otieno has active loan outstanding KES 8,000, overdue by 12 days
When: Step 4 loads
Then: Peter's RepaymentField enabled; PenaltyChip visible (unselected); overdue indicator shown

Given: treasurer enters KES 8,500 for Peter Otieno (exceeds outstanding KES 8,000)
When: amount entered
Then: RepaymentField shows error border; error text "Amount KES 8,500 exceeds outstanding KES 8,000"; SaveButton remains disabled

Given: treasurer enters KES 8,000 (exact outstanding amount)
When: amount entered
Then: RepaymentField shows valid state (no error); PenaltyChip still available

Given: PenaltyChip tapped for Peter Otieno (overdue 12 days)
When: chip selected
Then: chip shows errorContainer; penalty fine amount added to total; fine summary updates; TalkBack "Overdue penalty KES {amount} applied for Peter Otieno"

Given: all repayments valid, save tapped
When: API responds success
Then: Step 4 transitions to completion screen; Snackbar "Meeting record saved — KES {totalFines} in fines recorded"

Given: API fails (network timeout) during save
When: IOException thrown
Then: data queued to SyncQueue; Snackbar "Data saved locally — will sync when connected"; completion screen still shown
```

### Edge Cases

| Scenario | Expected Behavior |
|---|---|
| All 5 members PRESENT | FineChips all hidden; fine total = KES 0; NextButton immediately enabled after last selection |
| All 5 members ABSENT | Total fines = KES 500; error borders on all rows until saved |
| Member with no active loan in Step 4 | RepaymentField hidden; row shows "No active loan — KES 0" non-interactive |
| Multiple overdue members | Each shows independent PenaltyChip; each chip independently toggleable |
| Member name 50+ chars | Truncated at 1 line in attendance row; full name in TalkBack |
| Fine amounts updated (v2.0.0 groupConfig) | FineInfoChip text dynamically updates; FineChip amounts update to match config |
| Meeting already recorded (409 conflict) | "Already recorded" info state shown; read-only view of existing attendance |
| RTL layout | Attendance buttons right-to-left order (Absent, Late, Present); avatars on start; fine chips on end |

### Performance Baselines

- Step 1 first meaningful paint: < 200ms (simpler UI, no network needed for fine calculation)
- Attendance toggle response (tap to state update): < 50ms
- FineChip appear animation: smooth 60fps for 200ms
- Fine total recalculation (local): < 10ms (pure arithmetic, no network)
- Step transition animation: smooth 60fps for 300ms
- Step 4 load (from cached member list): < 200ms
- Meeting save (tap to queued): < 100ms before queued acknowledgment shown

---

## i18n / Localization Spec

### String Keys and Translations

| Key | English (en) | Swahili (sw) | French (fr) |
|-----|-------------|--------------|-------------|
| `attendance_step_title` | "Record Attendance" | "Rekodi Mahudhurio" | "Enregistrer la présence" |
| `loan_review_step_title` | "Loan Review" | "Ukaguzi wa Mikopo" | "Revue des prêts" |
| `step_indicator` | "Step {n} of {total}" | "Hatua {n} ya {total}" | "Étape {n} sur {total}" |
| `attendance_present` | "Present" | "Yupo" | "Présent" |
| `attendance_late` | "Late" | "Amechelewa" | "En retard" |
| `attendance_absent` | "Absent" | "Hayupo" | "Absent" |
| `fine_info_chip` | "Late: KES {late} · Absent: KES {absent} (FR-012)" | "Chelewa: KES {late} · Hayupo: KES {absent}" | "Retard: KES {late} · Absent: KES {absent}" |
| `fine_chip_late` | "Fine: KES {amount}" | "Faini: KES {amount}" | "Amende: KES {amount}" |
| `fine_chip_absent` | "Fine: KES {amount}" | "Faini: KES {amount}" | "Amende: KES {amount}" |
| `fine_total_chip` | "Total fines: KES {total}" | "Jumla ya faini: KES {total}" | "Amende totale: KES {total}" |
| `attendance_validation_error` | "All members must have attendance recorded" | "Wanachama wote lazima wawe na rekodi ya mahudhurio" | "Tous les membres doivent avoir leur présence enregistrée" |
| `repayment_label` | "Repayment Amount (KES)" | "Kiasi cha Kulipa (KES)" | "Montant du remboursement (KES)" |
| `penalty_chip_label` | "Apply penalty fine: KES {amount}" | "Weka faini ya adhabu: KES {amount}" | "Appliquer l'amende: KES {amount}" |
| `overpayment_error` | "Amount exceeds outstanding KES {outstanding}" | "Kiasi kinazidi salio la KES {outstanding}" | "Le montant dépasse le solde de KES {outstanding}" |
| `corpus_band_label` | "Group Corpus: KES {amount}" | "Akiba Kuu ya Kikundi: KES {amount}" | "Corpus du groupe: KES {amount}" |
| `meeting_save_success` | "Meeting record saved" | "Rekodi ya mkutano imehifadhiwa" | "Compte-rendu de réunion enregistré" |
| `meeting_save_offline` | "Saved locally — will sync when connected" | "Imehifadhiwa ndani — itasawazishwa ukiwa na mtandao" | "Enregistré localement — synchronisation à la connexion" |
| `next_step` | "Next: Step {n}" | "Ifuatayo: Hatua {n}" | "Suivant: Étape {n}" |
| `back_step` | "Back to Step {n}" | "Rudi Hatua {n}" | "Retour à l'étape {n}" |
| `save_complete` | "Save & Complete" | "Hifadhi na Kamilisha" | "Enregistrer et terminer" |

### Pluralization Rules

Attendance and fines involve counts that require correct plural forms:

| Key | Singular (en) | Plural (en) | Swahili |
|---|---|---|---|
| `absent_count` | "1 absent" | "{n} absent" | "hayupo 1" → "hawajupo {n}" |
| `late_count` | "1 late" | "{n} late" | "amechelewa 1" → "wamechelewa {n}" |
| `unset_count` | "1 member unset" | "{n} members unset" | "mwanachama 1 bila rekodi" → "wanachama {n} bila rekodi" |
| `overdue_days` | "1 day overdue" | "{n} days overdue" | "siku 1 imechelewa" → "siku {n} zimechelewa" |

French pluralization: "1 absent" → "2 absents" (add "s"); "1 retard" → "2 retards".

### Number Formatting (fines context)

| Value | en-KE | sw-KE | fr-FR |
|---|---|---|---|
| Fine KES 50 | KES 50 | KES 50 | KES 50 |
| Fine KES 100 | KES 100 | KES 100 | KES 100 |
| Total fines KES 1,250 | KES 1,250 | KES 1,250 | KES 1 250 |
| Corpus KES 36,400 | KES 36,400 | KES 36,400 | KES 36 400 |
| Penalty fine (e.g. 3% of KES 8,000 = KES 240) | KES 240 | KES 240 | KES 240 |

Penalty fine amounts: whole KES only — round down to nearest KES (no cents in fine amounts).

### Date Formatting (meeting context)

Meeting date in step header and completion screen:

| Locale | Format | Example |
|---|---|---|
| en-KE | "Wednesday, 15 Jun 2026" | EEEE, DD MMM YYYY |
| sw-KE | "Jumatano, 15 Jun 2026" | day name in Swahili |
| fr-FR | "mercredi 15 juin 2026" | lowercase day and month |

Overdue loan dates (next payment was due):

| Locale | Format | Example |
|---|---|---|
| en-KE | "Due 3 Jun 2026 (12 days overdue)" | |
| sw-KE | "Ilitakiwa 3 Jun 2026 (siku 12 zimechelewa)" | |
| fr-FR | "Dû le 3 juin 2026 (12 jours de retard)" | |

### RTL Considerations

- Attendance toggle buttons row: order reverses in RTL — Absent first (leftmost in RTL), Present last
- FineChip: aligns to end of member name in LTR → start in RTL (always near member identity)
- Corpus band: full-width, amount centered — no directional change
- Step navigation: Back button on start, Next button on end — mirrors correctly in RTL
- All fine amounts: end-aligned in RTL tables; start-aligned in LTR
- Step progress dots: render RTL (step 4 on left, step 1 on right in RTL layout)
