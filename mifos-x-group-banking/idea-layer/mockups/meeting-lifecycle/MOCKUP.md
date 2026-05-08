# MOCKUP — meeting-lifecycle
# CommonPurse (mifos-x-group-banking) | Feature FR-003 / FR-019
# Generated: 2026-05-06

---

## Design Language

**Brand:** CommonPurse by Mwangaza Women's Group
**System:** Material Design 3
**Primary:** #2E7D32 (VSLA-green) — growth, trust, agricultural roots
**Secondary:** #FF8F00 (amber) — shared coin, harvest wealth
**Tertiary:** #1565C0 (trust-blue) — informational elements, corpus tracking
**Font:** Noto Sans — chosen for multilingual Swahili/English support and legibility on low-DPI screens
**Density:** Comfortable — 48dp minimum touch targets; rural-friendly large tap zones
**Radius:** Cards 16dp (large), dialogs 28dp (extra-large), chips full-round (9999dp)
**Elevation:** Navigation footer level_4 (8dp), cards level_2 (3dp), upcoming pinned card level_3 (6dp)

---

## Screen-by-Screen

### Screen 1: MeetingCalendarScreen

**Layout:** Column, full-screen, status bar #2E7D32

```
┌──────────────────────────────────────┐  height: 56dp
│  [←]  Meetings                 [☰]  │  background: surface #FAFAFA
│       Mwangaza Women's Group         │  subtitle: bodyMedium #424942
├──────────────────────────────────────┤  divider: 1dp outlineVariant
│                                      │
│  ┌──────────────────────────────┐    │  UpcomingMeetingCard
│  │ SCHEDULED MEETING            │    │  background: primaryContainer #A6F1A6
│  │ Meeting #4         [Upcoming]│    │  corner: 16dp; padding: 16dp
│  │ Wednesday, 7 May 2026        │    │  margin: 16dp; elevation: 4dp
│  │                              │    │
│  │  [  Start Meeting  ]         │    │  FilledButton; bg: #2E7D32
│  └──────────────────────────────┘    │  min-h: 48dp; full-width; mt: 12dp
│                                      │
│  PAST MEETINGS                       │  titleSmall #424942; ph: 16dp
│  ─────────────────────────────────   │
│  [#3]  Meeting #3              KES 1,850  │  72dp row
│        28 Apr 2026 · 5/5 present  [Completed]  │  primaryContainer badge
│  ─────────────────────────────────   │
│  [#2]  Meeting #2              KES 1,200  │
│        21 Apr 2026 · 4/5 present  [Completed]  │
│  ─────────────────────────────────   │
│  [#1]  Meeting #1              KES 900   │
│        14 Apr 2026 · 5/5 present  [Completed]  │
│                                      │
└──────────────────────────────────────┘
     [Home]  [Meetings]  [Savings]  [Loans]  ← BottomNav
```

**States:**
- Loading: 4x shimmer cards, height 72dp each, cornerRadius 12dp
- Content: upcoming card pinned + past meetings LazyColumn
- Content_with_error: orange banner "Showing cached meetings — tap Retry" above upcoming card
- Empty: centered icon + "No Meetings Yet" + "Meetings will appear once scheduled"
- Error: full-screen error banner with Retry button

---

### Screen 2: MeetingConductScreen (7-step Wizard)

**Overall layout:** full-screen, no bottom nav, all 7 steps share the same chrome

```
TopAppBar (surface #FAFAFA, 64dp with subtitle):
  Title:    "Meeting #4"             titleLarge 22sp
  Subtitle: "Step 2 of 7 — Attendance"  bodyMedium 14sp #424942
  Close:    [✕] FluentIcons.dismiss_24_regular → back to calendar
  Offline:  [Offline] chip (warningContainer #FF8F00 tint; only visible when isOffline)

StepperHeader (horizontal, margin: 16dp, mt: 8dp):
  Step 0: [◑] Review      — completed, primaryContainer fill
  Step 1: [●] Attendance  — active, primary #2E7D32 fill
  Step 2: [ ] Balance     — inactive, outlineVariant
  Step 3: [ ] Savings     — inactive
  Step 4: [ ] Loans       — inactive
  Step 5: [ ] Apply       — inactive
  Step 6: [ ] Close       — inactive
  Connector line: outline #727971, 1dp

CorpusBand (visible steps 2-6, tertiaryContainer #D2E4FF, pv: 8dp, ph: 16dp):
  "Corpus: KES 12,400"    labelLarge #001C39
  "Cash on Hand: KES 2,000"  labelMedium #001C39
```

**Step 0 — Previous Meeting Review:**
```
  ┌─────────────────────────────────┐  surfaceVariant #DEE5DA card
  │ Meeting #3                      │  corner: 12dp; padding: 16dp
  │ 28 Apr 2026                     │  bodyLarge #1A1C19
  │ Total Collected  KES 1,850      │  info_row
  │ Closing Corpus   KES 12,400     │  info_row
  │ Attendance       5/5            │  info_row
  └─────────────────────────────────┘
  [ View Full Report ]  OutlinedButton; mt: 12dp; min-h: 48dp
```

**Step 1 — Attendance:**
```
  "Record Attendance"  titleMedium #1A1C19
  [Late: KES 50 fine · Absent: KES 100 fine (FR-012)]  warningContainer chip

  [AH]  Amina Hassan   Chairperson   [ Present | Late | Absent ]  → 64dp row
  [PO]  Peter Otieno   Treasurer     [ Present | Late | Absent ]
  [GW]  Grace Wanjiku  Secretary     [ Present | Late | Absent ]
  [JM]  John Mwangi    Member        [ Present | Late | Absent ]
  [MA]  Mary Akinyi    Member        [ Present | Late | Absent ]

  [Fine: KES 50]  errorContainer chip (appears below row when LATE selected)
  [Fine: KES 100] errorContainer chip (appears below row when ABSENT selected)

  [3/5 recorded]  surfaceVariant chip → [5/5 recorded] primaryContainer chip (all done)
```

**Step 2 — Opening Balance:**
```
  ┌─────────────────────────────────┐  primaryContainer #A6F1A6
  │ Group Corpus Fund               │  labelLarge #002106
  │ KES 12,400                      │  displaySmall 36sp bold #002106
  │ At start of Meeting #4          │  bodySmall #002106
  └─────────────────────────────────┘  corner: 16dp; padding: 24dp

  ┌─────────────────────────────────┐  surfaceVariant #DEE5DA
  │ Cash on Hand   KES 2,000        │  headlineMedium 28sp
  └─────────────────────────────────┘  corner: 12dp; padding: 16dp

  "Confirm these balances are correct before proceeding."  bodySmall #424942 centered
```

**Step 3 — Savings Collection:**
```
  "Savings Collection"  titleMedium
  [Min. group savings: KES 200/member (FR-020)]  secondaryContainer #FFDDB3 chip

  [AH]  Amina Hassan
        Group Savings (KES)  [____200____]  min-h: 48dp; prefix: KES
        Individual Savings   [____500____]  optional; min-h: 48dp; mt: 8dp
  divider
  [PO]  Peter Otieno
        Group Savings (KES)  [____200____]
        Individual Savings   [___________]
  ... (5 members)

  ┌─────────────────────────────────┐  primaryContainer running total
  │ Total Savings This Step:        │
  │ KES 1,000                       │  headlineSmall 24sp bold
  └─────────────────────────────────┘  bg: #A6F1A6; padding: 16dp; mt: 8dp
```

**Step 4 — Loan Review:**
```
  "Loan Review & Repayments"  titleMedium

  [PO]  Peter Otieno                          errorContainer background (overdue)
        KES 1,500 loan · KES 875 outstanding · Week 4/12
        [OVERDUE]  errorContainer chip
        Repayment (KES)  [____500____]  hint: "Expected: KES 500"; min-h: 48dp
        Penalty Fine     [____50_____]  visible only when overdue; mt: 8dp
```

**Step 5 — Loan Applications:**
```
  "Loan Applications"  titleMedium
  [Available to disburse: KES 14,025]  tertiaryContainer chip

  ┌─────────────────────────────────┐  surfaceVariant card
  │ Grace Wanjiku                   │  titleSmall
  │ Requests KES 1,500              │  bodyLarge
  │ Purpose: School fees            │  bodySmall #424942
  │ 3 For · 1 Against               │  labelMedium #727971
  │ [ For ↑ ]  [ Against ↓ ]        │  OutlinedButtons; min-h: 48dp
  │ [ Chairperson Approve ]         │  FilledButton #2E7D32; enabled when majority For + chairperson
  └─────────────────────────────────┘  padding: 16dp; corner: 12dp
```

**Step 6 — Closing Balance:**
```
  "Closing Balance & Reconciliation"  titleMedium

  ┌─────────────────────────────────┐  surfaceVariant card
  │ Opening Corpus    KES 12,400    │
  │ ─────────────────────────────── │  divider 1dp
  │ + Group Savings   KES 1,000     │  primary #2E7D32
  │ + Loan Repayments KES 500       │  primary
  │ + Fines Collected KES 50        │  primary
  │ — Loans Disbursed KES 1,500     │  error #D32F2F
  │ ══════════════════════════════  │  divider 2dp
  │ Closing Corpus    KES 12,450    │  titleLarge #2E7D32
  └─────────────────────────────────┘

  [4/5 Present]  primaryContainer chip    [Fines: KES 50]  warningContainer chip

  [ Submit Meeting ]  FilledButton; bg: #2E7D32; min-h: 56dp; full-width
  "You're offline — data saved locally and will sync when connected."  bodySmall (conditional)
```

**NavigationFooter (sticky, elevation 8dp, surface, padding 16dp):**
```
  [ Back ]   OutlinedButton flex:1    [ Next → ]  FilledButton flex:1 ml: 8dp
  (hidden on step 0)                  (shows "Submit Meeting" on step 6)
```

**Step Validation Snackbar:** errorContainer bg, 4000ms, bottom of screen
**Submit Progress Overlay:** CircularProgressIndicator centered, label "Submitting meeting..."

---

### Screen 3: MeetingSummaryScreen

```
TopAppBar: "Meeting #4 Summary" / "7 May 2026"  [← back]  [share ↑]

┌──────────────────────────────────────┐  primary #2E7D32 hero card
│ Total Collected                      │  labelLarge white
│ KES 1,750                            │  displaySmall 36sp bold white
│ Meeting #4 · 7 May 2026              │  bodyMedium white 80% opacity
│ [Corpus: KES 12,450]                 │  primaryContainer chip mt: 12dp
└──────────────────────────────────────┘  corner: 28dp; padding: 24dp; margin: 16dp

2x3 Metric Grid (gap 12dp, margin: 16dp):
  [👥] Attendance        5/5          primaryContainer
  [💰] Group Savings     KES 1,000    primaryContainer
  [👤] Individual Savings KES 750     secondaryContainer
  [↙] Loan Repayments   KES 500      tertiaryContainer
  [⚠] Fines Collected   KES 50       warningContainer
  [↗] Loans Disbursed   KES 1,500    errorContainer

Savings Breakdown (titleSmall "Savings Breakdown"):
  [AH] Amina Hassan    Group: KES 200 · Ind: KES 500   KES 700  primary
  [PO] Peter Otieno    Group: KES 200 · Ind: KES 0     KES 200  primary
  [GW] Grace Wanjiku   Group: KES 200 · Ind: KES 50    KES 250  primary
  [JM] John Mwangi     Group: KES 200 · Ind: KES 100   KES 300  primary
  [MA] Mary Akinyi     Group: KES 200 · Ind: KES 100   KES 300  primary

Corpus Reconciliation (tertiaryContainer #D2E4FF card):
  Corpus Reconciliation  titleSmall #001C39
  Opening    KES 12,400
  Closing    KES 12,450   titleMedium
  Net Change +KES 50      primary #2E7D32

[ Done ]  FilledButton #2E7D32; min-h: 56dp; full-width; margin: 16dp bottom: 24dp
```

---

### Screen 4: PreviousMeetingReviewScreen

```
TopAppBar: "Meeting #3" / "28 Apr 2026"  [← back]

ContextBanner (primaryContainer #A6F1A6):
  If launchedFrom=conduct:  "Reviewing before Meeting #4 — Wed, 7 May 2026"  [📋]
  If launchedFrom=calendar: "Completed Meeting — 28 Apr 2026"  [✓]

UnresolvedItemsAlertCard (warningContainer; visible only when items exist):
  [⚠] Unresolved Items  titleSmall
    · [💰] Mary Akinyi — KES 100 fine unpaid from Meeting #3
    · [🗳] Grace Wanjiku loan vote unresolved

SummaryMetricsCard (primaryContainer #A6F1A6, corner 16dp, padding 20dp):
  Total Collected  KES 1,850  headlineLarge bold
  ─────────────────────────────
  Closing Corpus   KES 12,400
  Fines Collected  KES 150
  Loans Disbursed  KES 0

Attendance section:
  [5/5 Present]  primaryContainer chip
  [AH] Amina Hassan   [Present]  primaryContainer chip
  [PO] Peter Otieno   [Present]  primaryContainer chip
  [GW] Grace Wanjiku  [Late]     warningContainer chip  Fine: KES 50
  [JM] John Mwangi    [Present]  primaryContainer chip
  [MA] Mary Akinyi    [Absent]   errorContainer chip     Fine: KES 100

Savings Per Member section:
  [AH] Amina Hassan    Group: KES 400 · Ind: KES 0    KES 400  primary
  [PO] Peter Otieno    Group: KES 400 · Ind: KES 0    KES 400  primary
  [GW] Grace Wanjiku   Group: KES 250 · Ind: KES 200  KES 450  primary
  [JM] John Mwangi     Group: KES 300 · Ind: KES 100  KES 400  primary
  [MA] Mary Akinyi     Group: KES 200 · Ind: KES 0    KES 200  primary

Loan Activity section:
  [💲] Peter Otieno   Repaid: KES 500 · Outstanding: KES 875  Week 3/12

[ Start Meeting #4 ]  FilledButton #2E7D32; min-h: 56dp; visible only when launchedFrom=conduct; margin: 16dp
```

---

## Interaction Patterns

**Attendance segmented button:** Tap segment → instant visual update (150ms); fine chip fades in (200ms) for LATE/ABSENT; fade out (150ms) when PRESENT selected. Progress chip color transitions from surfaceVariant to primaryContainer at 5/5.

**Savings input:** Real-time validation on each character typed; error text appears 150ms after input stops if below KES 200; running total banner updates in 100ms after each valid input change.

**Step advance:** NextStep button triggers validation; on failure — snackbar slides up from bottom (300ms); on success — step content cross-fades (200ms); stepper indicator fills with primary color (250ms).

**Corpus band update:** When savings or repayments change, corpus band text updates with a 100ms crossfade to indicate recalculation.

**Submit overlay:** When Submit tapped, all footer buttons disable; CircularProgressIndicator fades in (200ms) centered over step 6 content; on success, brief 2s toast slides in from bottom, then screens transitions to meeting-summary.

---

## Accessibility

- All interactive elements: min 48dp touch target (FR-accessibility)
- CorpusBand content description: "Group corpus fund KES X, cash on hand KES Y" — read by TalkBack on each step change
- Stepper role: progressbar — "Meeting wizard step 2 of 7: Attendance"
- AttendanceMemberRow: role=group; each segmented button announces selection change
- Error snackbar: content_description prefixed with "Validation error:" for screen readers
- Submit button during loading: content_description changes to "Submitting meeting, please wait"
- Color is never the sole differentiator — status chips always include text label (PRESENT / LATE / ABSENT)
