# MOCKUP — savings-collection
# MifosSave (mifos-x-group-banking) | Feature FR-004 / FR-017
# Generated: 2026-05-06

---

## Design Language

**Brand:** MifosSave by Mwangaza Women's Group
**System:** Material Design 3
**Primary:** #2E7D32 (VSLA-green) — mandatory group savings, growth, collective wealth
**Secondary:** #FF8F00 (amber) — individual voluntary savings, personal growth
**Tertiary:** #1565C0 (trust-blue) — informational metrics, balance figures
**Font:** Noto Sans — 12sp minimum for labels; 28sp+ for key KES amounts
**Chart colors:** Primary green for group savings bars; Amber for individual savings line
**Density:** Comfortable — 48dp minimum touch targets on all rows and inputs

---

## Screen-by-Screen

### Screen 1: SavingsDashboardScreen

**Overall layout:** Column, full-screen

```
┌──────────────────────────────────────┐
│  Savings                             │  titleLarge 22sp surface #FAFAFA
│  Mwangaza Women's Group              │  bodyMedium #424942
├──────────────────────────────────────┤
│  Last synced: 7 May 2026, 10:34      │  lastSyncBand: surfaceVariant #DEE5DA
│                                      │  labelSmall #424942, ph: 16dp, pv: 4dp
├──────────────────────────────────────┤
│  [Group Savings ↑]  [Individual 👤]  │  TabRow; indicator: primary #2E7D32
│                                      │
│  --- GROUP SAVINGS TAB ---           │
│                                      │
│  ████████████████████                │  Bar chart 180dp tall
│  ████  ████  ██  ████  ████  ████   │  primary #2E7D32 bars
│  W48   W49   W50  W51  W52   W3     │  labelSmall x-axis
│  KES                                 │  y-axis labelSmall
│                                      │
│  ┌─────────────────────────────┐     │  CycleProgressCard
│  │ Cycle Progress              │     │  primaryContainer #A6F1A6
│  │ ████████████░░░░░░░░░░░░░   │     │  LinearProgress; primary; h: 8dp
│  │ KES 7,600 collected  Target: KES 10,400 │  bodyMedium
│  │ 73% of cycle target reached │     │  labelSmall 80% opacity
│  └─────────────────────────────┘     │  corner: 12dp; padding: 16dp; mh: 16dp
│                                      │
│  Per-Member Contributions            │  titleSmall #424942 ph: 16dp
│  Group total: KES 7,600              │  primaryContainer chip mh: 16dp mb: 8dp
│  ─────────────────────────────────   │
│  [AH]  Amina Hassan            KES 1,800  │  72dp row
│        3 meetings · Last: KES 600    │  bodySmall #424942
│                              total   │  labelSmall #424942
│  ─────────────────────────────────   │
│  [PO]  Peter Otieno            KES 1,800  │
│        3 meetings · Last: KES 600    │
│  ─────────────────────────────────   │
│  [GW]  Grace Wanjiku           KES 1,400  │
│        3 meetings · Last: KES 200    │
│  ─────────────────────────────────   │
│  [JM]  John Mwangi             KES 1,800  │
│        3 meetings · Last: KES 600    │
│  ─────────────────────────────────   │
│  [MA]  Mary Akinyi             KES 800   │
│        3 meetings · Last: KES 200    │
│                                      │
└──────────────────────────────────────┘
```

**Individual Savings Tab:**
```
│  ∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿∿              │  Line chart 180dp tall
│  amber line chart #FF8F00             │  fill below with 12% opacity
│  W48  W49  W50  W51  W52  W3          │
│                                       │
│  ┌───────────────────────────────┐    │  IndividualTotalCard
│  │ Total Individual Balances     │    │  secondaryContainer #FFDDB3
│  │ KES 3,750                     │    │  headlineMedium 28sp bold
│  └───────────────────────────────┘    │  corner: 12dp; padding: 16dp; mh: 16dp
│                                       │
│  Member Balances                      │  titleSmall #424942
│  ──────────────────────────────────   │
│  [AH]  Amina Hassan           KES 1,500  │  72dp row
│        [↑ Deposit] KES 500 on 7 May   │  chip + bodySmall
│                              balance  │  labelSmall #FF8F00 (secondary)
│  ──────────────────────────────────   │
│  [PO]  Peter Otieno           KES 500   │
│        [no last transaction]          │
│  ──────────────────────────────────   │
│  [GW]  Grace Wanjiku          KES 850   │
│        [↑ Deposit] KES 200 on 5 May   │
│  ──────────────────────────────────   │
│  [JM]  John Mwangi            KES 500   │
│        [↑ Deposit] KES 100 on 7 May   │
│  ──────────────────────────────────   │
│  [MA]  Mary Akinyi            KES 400   │
│        [↑ Deposit] KES 100 on 7 May   │
```

**Loading state:** 6 shimmer skeleton items, 72dp height each, 12dp corner radius, 16dp margin.
**Error state with cached data:** error_container banner at top with "Showing cached savings — pull down to retry" + Retry TextButton.
**Empty state:** icon + "No Savings Data" + "Savings will appear after the first meeting is conducted".

---

### Screen 2: Step3SavingsCollection (inside MeetingConductScreen)

Appears as the body content when currentStep == 3 in the wizard.

```
"Savings Collection"  titleMedium #1A1C19; mb: 4dp

[Min. group savings: KES 200/member (FR-020)]  secondaryContainer #FFDDB3 chip; corner: full; mb: 12dp; labelSmall

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[AH]  Amina Hassan
      ┌────────────────────────────────┐  OutlinedTextField; min-h: 48dp
      │ Group Savings (KES)  KES 200   │  label + prefix; keyboard: number
      └────────────────────────────────┘
      ┌────────────────────────────────┐
      │ Individual Savings (KES) 500   │  hint: "Optional"; mt: 8dp
      └────────────────────────────────┘
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[PO]  Peter Otieno
      ┌────────────────────────────────┐
      │ Group Savings (KES)  KES 200   │
      └────────────────────────────────┘
      ┌────────────────────────────────┐
      │ Individual Savings (KES)   0   │  (0 shown as empty or 0)
      └────────────────────────────────┘
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[GW]  Grace Wanjiku   [⚠ Below minimum — enter at least KES 200]
      ┌────────────────────────────────┐  ← error outline; label turns error red
      │ Group Savings (KES)  KES 100   │  ← error state shown
      │ Below minimum KES 200 required │  ← error text labelSmall error #D32F2F
      └────────────────────────────────┘
      ┌────────────────────────────────┐
      │ Individual Savings (KES)  50   │
      └────────────────────────────────┘
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[JM]  John Mwangi
      [Group Savings  KES 200]  [Individual  KES 100]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[MA]  Mary Akinyi
      [Group Savings  KES 200]  [Individual  KES 100]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌──────────────────────────────────────┐  RunningTotalBand
│ Total Savings This Step:             │  primaryContainer #A6F1A6
│ KES 1,350                            │  headlineSmall 24sp bold
└──────────────────────────────────────┘  padding: 16dp; mt: 8dp
```

**Error state (below KES 200):**
- TextField outline: error #D32F2F (2dp)
- Label: error #D32F2F (animates from on_surface_variant #424942 in 150ms)
- Error text below field: "Below minimum KES 200 required" (labelSmall, error #D32F2F)
- Field background: error_container #FFDAD6 at 8% opacity tint

**Valid state (>= KES 200):**
- TextField outline: primary #2E7D32 when focused, outline #727971 when unfocused

---

## Interaction Patterns

**Tab switching:**
1. Tap tab → tab indicator slides from old to new (200ms, standard easing)
2. Tab content fades in (150ms) — no explicit slide (content differs significantly)
3. Chart renders with a brief draw-in animation (bars grow up 300ms; line draws left-to-right 400ms)

**Member row tap (savings-dashboard):**
1. Tap → ripple (100ms) bounded to row
2. Navigate to member-savings-detail (slide-in 400ms)

**Cycle progress bar:**
1. On screen enter: progress bar animates from 0 to current value (400ms, decelerated easing)
2. Percentage text counts up simultaneously with progress bar

**Group savings bar chart:**
1. Each bar grows from 0 to its value sequentially left-to-right (50ms delay between bars)
2. Total animation: 300ms

**Individual savings line chart:**
1. Line draws from left to right over 400ms with fill fading in simultaneously (200ms)
2. Data points appear with scale animation (scale 0→1, 100ms each, 50ms delay from previous)

**Running total band (step 3):**
1. Any input change → runningSavingsTotal recomputed (synchronous)
2. Band text crossfades from old to new value (100ms)
3. If savings total increases → brief "bump" scale animation on band (scale 1.0→1.05→1.0, 200ms)

---

## Accessibility

- TabRow: each tab has role=tab; content_description includes "Group Savings tab" / "Individual Savings tab"
- Bar chart: content_description "Weekly group savings trend chart — 6 weeks; highest: KES 1,850 in week W3"
- Cycle progress: content_description "73% of cycle target reached — KES 7,600 of KES 10,400"
- Member rows in list: role=button, content_description "Amina Hassan group savings KES 1,800 across 3 meetings"
- TextField error: content_description includes error text when error is present
- Running total band: announces on change for TalkBack: "Total savings updated: KES 1,350"
- All color differences are accompanied by text or icon (deposit chip shows "↑ Deposit" text, not just green color)
