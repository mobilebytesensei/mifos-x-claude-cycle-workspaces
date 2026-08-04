# MOCKUP — corpus-tracking
# MifosSave (mifos-x-group-banking) | Feature FR-018
# Generated: 2026-05-06

---

## Design Language

**Brand:** MifosSave by Mwangaza Women's Group
**System:** Material Design 3
**Primary:** #2E7D32 (VSLA-green) — corpus balance display, sufficient-corpus state
**Error:** #D32F2F — corpus block state, insufficient balance warning
**Tertiary:** #1565C0 (trust-blue) — informational corpus band in wizard, sub-stats
**Font:** Noto Sans; displaySmall 36sp bold for corpus KES amount
**Density:** Comfortable — 48dp minimum touch target; quick action buttons 56dp

The corpus is the most financially critical number in MifosSave. Its visual design must:
- Make the balance unmissable (displaySmall 36sp, primary green, prominently centered)
- Communicate sufficiency vs insufficiency instantly (border color: transparent when OK; error #D32F2F when blocked)
- Persist during meetings (CorpusBand always visible during financial entry steps)

---

## Screen-by-Screen

### Screen 1: GroupDashboardScreen

**Layout:** Column, scrollable (LazyColumn), full-screen

```
┌──────────────────────────────────────┐  TopBar
│  ←  Mwangaza Women's Group     [⋮]  │  bg: primary #2E7D32; text: onPrimary; 56dp
├──────────────────────────────────────┤
│                                      │  GroupHeaderCard
│  Mwangaza Women's Group              │  headlineSmall #002106
│  Cycle 1 of 12 months • Weekly       │  bodyMedium #002106
│  [5 members]  [0 overdue]            │  secondaryContainer chip + surfaceVariant chip
│                                      │
├──────────────────────────────────────┤  CorpusCard
│  ┌──────────────────────────────┐    │  surface #FAFAFA, elevation 4dp, corner 16dp
│  │ Corpus Fund                  │    │  titleMedium #1A1C19
│  │ KES 47,500                   │    │  displaySmall 36sp bold PRIMARY #2E7D32
│  │                              │    │  (no block banner — corpus sufficient)
│  │  Opening  Contributions  Loans Out │  3-stat row
│  │  KES 0   KES 52,500   KES 5,000  │  stat labels/values
│  └──────────────────────────────┘    │  padding: 20dp; mh: 16dp; mv: 8dp
│                                      │
├──────────────────────────────────────┤  QuickActionsSection
│  ┌──────────────────────────────┐    │  surface, elevation 2dp, corner 16dp
│  │ Quick Actions                │    │  titleSmall #424942
│  │  [📅 Start Meeting]  [👥 Members] │  2×2 grid; FilledButton + OutlinedButtons
│  │  [💰 Loans]  [💱 Share-Out↓] │    │  Share-Out disabled (not cycle end)
│  └──────────────────────────────┘    │
│                                      │
├──────────────────────────────────────┤  SavingsSummaryCard
│  ┌──────────────────────────────┐    │  surface, elevation 2dp, corner 16dp
│  │ Savings Summary              │    │  titleMedium
│  │ Mandatory: KES 100 – KES 500 │    │  bodyMedium #424942
│  │ KES 52,500 total             │    │  titleLarge TERTIARY #1565C0
│  └──────────────────────────────┘    │
│                                      │
└──────────────────────────────────────┤  ActivityFeedSection
  │  ┌──────────────────────────────┐  │  surface, elevation 2dp, corner 16dp
  │  │ Recent Activity              │  │
  │  │ 📅 Meeting #4 conducted   7 May │  MEETING type icon
  │  │    Amina Hassan       KES 1,750  │
  │  │ ↑  Grace Wanjiku deposit  5 May  │  DEPOSIT type icon
  │  │    Individual savings   KES 200  │
  │  │ 💰  Peter Otieno loan repaid 28 Apr │  LOAN type icon
  │  │    Repayment          KES 500    │
  │  └──────────────────────────────┘  │
```

**Corpus card — INSUFFICIENT state:**
```
│  ┌──────────────────────────────┐    │  border: 2dp ERROR #D32F2F
│  │ Corpus Fund                  │    │  titleMedium
│  │ KES 800                      │    │  displaySmall 36sp ERROR #D32F2F (not primary)
│  │                              │    │
│  │ ⚠ Loan disbursement is blocked │  │  errorContainer #FFDAD6 banner inside card
│  │   corpus balance is below    │    │  on_error_container #410002 text
│  │   minimum threshold.         │    │  icon: warning 20dp
│  │                              │    │
│  │  Opening  Contributions  Loans Out │
│  │  KES 0   KES 52,500   KES 51,700 │  (loans out > contributions = insufficient)
│  └──────────────────────────────┘    │
```

**Loading state:** 4 shimmer blocks (120dp height each, corner 16dp, surface_variant bg, shimmer animation).

**Error state:** centered cloud_off icon + "Could not load group" title + error.message body + FilledButton "Retry" (primary bg).

---

### Screen 2: CorpusBand (inside MeetingConductScreen, steps 2-6)

Shown as a persistent horizontal strip below the step stepper.

```
STEP 2 (Opening Balance) — CorpusBand appears:
┌──────────────────────────────────────┐  height: 40dp
│  Corpus: KES 12,400  Cash on Hand: KES 2,000  │  bg: tertiaryContainer #D2E4FF
└──────────────────────────────────────┘  ph: 16dp, pv: 8dp

STEP 3 (Savings entered — corpus updates live):
┌──────────────────────────────────────┐  live update
│  Corpus: KES 13,400  Cash on Hand: KES 2,000  │  text crossfades on change
└──────────────────────────────────────┘

STEP 5 (Loan approved — corpus decreases):
┌──────────────────────────────────────┐  warningContainer bg (amber)
│  Corpus: KES 11,900  Cash on Hand: KES 2,000  │  on_secondary_container text
└──────────────────────────────────────┘  (corpus dropped but still positive)

STEP 5 — Corpus would go negative (gate triggered BEFORE approval):
  [error snackbar slides up from bottom]
  "Corpus insufficient for this disbursement — available KES 900"
  [CorpusBand stays at current positive value; loan blocked]
```

**CorpusBand normal state:**
- background: tertiary_container #D2E4FF
- "Corpus: KES X" (labelLarge 14sp, on_tertiary_container #001C39)
- "Cash on Hand: KES Y" (labelMedium 12sp, on_tertiary_container #001C39)

**CorpusBand warning state (projected corpus drops below min, not yet approved):**
- background transitions to secondary_container #FFDDB3 (200ms crossfade)
- "Corpus: KES X ⚠" (labelLarge, on_secondary_container #2A1700)
- Visual signal only — approval still blocked by corpus gate

---

### Screen 3: Step 5 Corpus Gate (inside MeetingConductScreen)

**CorpusGateChip (above loan application cards):**
```
[Available to disburse: KES 13,400]  tertiaryContainer #D2E4FF chip; corner: full; mb: 12dp
```

**Updates when loans approved:**
```
Grace Wanjiku — KES 1,500 approved:
[Available to disburse: KES 11,900]  ← updates in real-time
```

**Corpus gate enforcement (pre-approval check):**
```
John Mwangi — requests KES 12,000 (would make corpus = -100):
[Available to disburse: KES 11,900]

Amina (Chairperson) taps "Chairperson Approve":
  → pre-check fires: 11,900 - 12,000 = -100 < 0 → BLOCKED
  → ApproveLoanApplication action NOT dispatched
  → SnackBar slides up:
    "Corpus insufficient for this disbursement — available KES 11,900"
    errorContainer bg #FFDAD6; on_error_container text; 4000ms auto-dismiss
```

---

## Interaction Patterns

**GroupDashboard — parallel API load:**
1. Screen enters: all 4 API calls fired simultaneously (get_center, get_center_accounts, get_group_corpus, get_group_config)
2. While loading: 4 shimmer blocks, 120dp each, surface_variant with shimmer gradient
3. As each call resolves: state partially updates (corpus card may appear before activity feed)
4. isCorpusInsufficient computed: corpus.currentBalance < config.minimumDisbursementThreshold
5. If isCorpusInsufficient=true: corpus card border transitions to error 2dp (200ms)
6. Full Content rendered once all 4 calls return

**CorpusBand update (live, steps 2-6):**
1. Step advance from 1→2: CorpusBand slides down from stepper (200ms, decelerated easing); initial value = openingCorpus
2. Each SetSavingsAmount action: displayCorpus recomputed (synchronous); CorpusBand text crossfades (100ms)
3. Each SetLoanRepayment action: same pattern
4. Each ApproveLoanApplication: displayCorpus decrements; CorpusBand warns if < minimumDisbursementThreshold

**Corpus gate snackbar:**
- Appears: slides up from bottom 300ms
- Duration: 4000ms auto-dismiss
- No action button (user must reduce requested amount or choose smaller loan)
- analytics: corpus_gate_triggered emitted with available_corpus and requested_amount

**Share-Out button state:**
- isCycleEnd=false: button disabled (50% opacity), tint outline, tooltip "Share-Out is only available at the end of the cycle"
- isCycleEnd=true: button enabled, secondary #FF8F00 border and text

---

## Accessibility

- CorpusCard: content_description "Group corpus fund KES 47,500. Three sub-stats: Opening Balance KES 0; Contributions this cycle KES 52,500; Loans outstanding KES 5,000."
- When insufficient: additional content_description "Warning: Loan disbursement is blocked — corpus below minimum threshold of KES 5,000."
- CorpusBand: content_description updated on each change: "Group corpus fund KES 12,400. Cash on hand KES 2,000." Announced via AccessibilityEvent.TYPE_ANNOUNCEMENT
- CorpusGateChip: content_description "Available to disburse: KES 11,900. Corpus gate active."
- Error snackbar: content_description prefixed "Error: Corpus insufficient for this disbursement — available KES 11,900"
- Quick action buttons: each has explicit content_description ("Start a new meeting" / "View all members" / "View all loans" / "Distribute share-out at end of cycle")
- Color alone never conveys corpus state: text label "INSUFFICIENT" added when block banner visible
