# Meeting Conduct — Mockup Specification

**Feature**: meeting-conduct | **Route**: `/meetings/{meetingId}/conduct` | **Type**: wizard (7 steps)
**Feature group**: meeting-management | **Flow**: meeting-management-flow
**Generated from**: `screens/meeting-conduct/ui.yaml`, `screens/meeting-conduct/demo-data.yaml`, `design-system/DESIGN.md`
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature meeting-conduct`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: MifosSave-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for KES amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — stepper active dot, filled CTAs (Next / Submit), footer button, chairperson approve
**Primary container**: `#C8E6C9` on `#1B5E20` — running-savings band, corpus balance card (Step 2), attendance-complete progress chip
**Tertiary container**: on `--accent-100 / #FFE082` — Corpus band (persistent header on steps 2-6), pooled-fund emphasis
**Secondary container**: — min-contribution info chip (Step 3), non-overdue loan avatar background
**Warning container**: `#FFF9C4` on `#E65100` — offline badge, late/absent fine policy chip
**Error container**: `#FFCDD2` on `#B71C1C` — OVERDUE chip, late/absent per-member fine chip, submit error snackbar, Against vote selection
**Surface variant**: `#F5F5F5` — reconciliation card (Step 6), previous-meeting review card, loan-application card fill
**Background**: `#FFFFFF` canvas · `#FAFAFA` app
**Corner radius**: 12dp cards · 16dp corpus/reconciliation cards (lg) · full-round chips + stepper dots
**Elevation**: 2dp cards · 8dp navigation footer
**Min touch target**: 64dp attendance/savings rows · 56dp submit button · 48dp segmented buttons · 28dp stepper step
**Reduced motion**: `prefers-reduced-motion: reduce` disables step slide-in + shimmer + spinner rotation

---

## Screen: Meeting #{meetingNumber} Wizard

### Entry
- From **meeting-calendar** ("Start Meeting" on an upcoming meeting card); nav-params `meetingId: String`, `meetingNumber: Int`, `groupId: Int`
- Back navigation via close button in top app bar pops the wizard and returns to `meeting-calendar` (discarding in-progress state; SQLDelight `meeting_wizard_state` retains progress for resumption on next entry)
- Successful submit navigates to `meeting-summary` with the same three params

### Persistent chrome (all steps)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│ [✕] Meeting #4                  [Offline]│  top_app_bar — surface bg, primary [✕] icon
│     Attendance — Step 2 of 7             │  subtitle (bodySmall, onSurfaceVariant)
├─────────────────────────────────────────┤
│  ●───●───○───○───○───○───○              │  step_stepper — 7 dots + connectors,
│  Rev  Att  Bal  Sav  Lon  App  Cls       │  active #2E7D32 · completed #C8E6C9 ·
│                                          │  inactive outlineVariant · 28dp step size
├─────────────────────────────────────────┤
│  Corpus: KES 14,850                      │  corpus_band — tertiaryContainer bg,
│  Cash on Hand: KES 3,500                 │  visible_when currentStep >= 2 only,
│                                          │  labelLarge + labelMedium
├─────────────────────────────────────────┤
│                                          │
│         { STEP CONTENT — see below }     │  scrollable body per currentStep (0..6)
│                                          │
├─────────────────────────────────────────┤
│  [ ‹ Back ]            [ Next › ]  or   │  wizard_footer — surface bg, elevation 8dp,
│                        [ Submit Meeting]│  padding 16dp · Back visible_when step>0 ·
└─────────────────────────────────────────┘  Next label swaps to "Submit Meeting" on step 6
```

- **Offline badge** (top-right chip) — warningContainer pill, visible only when `isOffline == true`; signals that submit will enqueue to SQLDelight `sync_queue`.
- **Corpus band** — labelLarge live-computed: `openingCorpus + runningSavingsTotal + totalRepayments − totalLoansDisbursed`; hidden on steps 0-1 (review + attendance).
- **Stepper labels** — Review · Attendance · Balance · Savings · Loans · Apply · Close (7 total).

---

### Step 0 · Previous Meeting Review

```
┌ Previous Meeting Review ────────────────┐
│  ┌────────────────────────────────────┐ │
│  │ Meeting              #4            │ │  prev_meeting_summary_card
│  │ Date                05 May 2026    │ │  surfaceVariant bg, md corner, 16dp pad
│  │ Total Collected     KES 2,500      │ │  info_row × 5, key labelMedium onSurfaceVariant
│  │ Closing Corpus      KES 51,750     │ │       value bodyMedium onSurface right-aligned
│  │ Attendance          5/5            │ │  Roboto Mono for amounts
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────── View Full Report ─────────────┐│  view_full_previous_btn — outlined variant,
│  └─────────────────────────────────────┘│  visible when previousMeetingSummary != null
│                                          │  → ViewFullPreviousMeeting → previous-meeting-review
└──────────────────────────────────────────┘
```

**First-meeting variant** — when `previousMeetingSummary == null`:

```
┌ Previous Meeting Review ────────────────┐
│                                          │
│                 🕘                       │  no_prev_meeting_placeholder
│         First Meeting                    │  empty-state, history_24_regular icon
│  No previous meeting data — this is      │  title titleLarge, body bodyMedium
│  the group's first meeting.              │
│                                          │
└──────────────────────────────────────────┘
```

- Read-only step; Back button hidden (step 0), Next advances to Attendance.
- View Full Report → NavController push `previous-meeting-review(meetingNumber=4, groupId=7)`.

### Step 1 · Attendance

```
┌ Attendance ─────────────────────────────┐
│  [ Late: KES 50 fine · Absent: KES 100 ]│  fine_info_chip — warningContainer,
│  fine (FR-012)                           │  onWarningContainer text
│                                          │
│  ┌──────────────────────────────────┐   │
│  │[AW] Amina Wanjiru       [P|L|A ] │   │  attendance_member_row — repeats_for
│  │     TREASURER                     │   │  groupMembers, 64dp min-height,
│  └──────────────────────────────────┘   │  divider bottom
│  ┌──────────────────────────────────┐   │  leading avatar 40dp initials (AW/PO/…)
│  │[PO] Peter Otieno        [P|L|A ] │   │  content: name bodyLarge, role labelSmall primary
│  │     MEMBER                        │   │  trailing segmented-button Present/Late/Absent
│  └──────────────────────────────────┘   │  → SetAttendance(memberId, status)
│  ┌──────────────────────────────────┐   │
│  │[GA] Grace Achieng       [P|L|A ] │   │
│  │     SECRETARY                     │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │[JK] John Kamau          [P|L|A ] │   │
│  │     CHAIRPERSON                   │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │[MN] Mary Njeri          [P|L|A ] │   │
│  │     MEMBER                        │   │
│  │     [ Fine: KES 50 ]              │   │  fine_chip — errorContainer pill,
│  └──────────────────────────────────┘   │  visible_when LATE || ABSENT
│                                          │
│  [ 4/5 recorded ]                        │  attendance_progress_chip — surfaceVariant
│                                          │  → primaryContainer when count == total
└──────────────────────────────────────────┘
```

- **Segmented button** selection posts `SetAttendance(memberId, status)` → `attendanceMap` update + auto-derived fine (KES 50 late / 100 absent) folded into `totalFinesCollected` client-side.
- **Fine chip** appears inline under the member row when status = LATE or ABSENT.
- **Progress chip** turns primary-container-green at 5/5; `AttendanceIncomplete` error blocks Next if any member unrecorded.
- **Step validation** — Next tap runs `RecordAttendance validation`, surfaces `stepValidationError` in snackbar (errorContainer, 4s auto-dismiss) if incomplete.

### Step 2 · Opening Balance (read-only)

```
┌ Opening Balance ────────────────────────┐
│  ┌────────────────────────────────────┐ │
│  │                                    │ │  corpus_balance_card — primaryContainer bg,
│  │  Group Corpus Fund                 │ │  lg corner 24dp, 24dp pad
│  │                                    │ │  labelLarge onPrimaryContainer
│  │  KES 51,750                        │ │  displaySmall onPrimaryContainer bold
│  │                                    │ │  Roboto Mono
│  │  At start of Meeting #5            │ │  bodySmall onPrimaryContainer
│  └────────────────────────────────────┘ │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │  Cash on Hand                      │ │  cash_on_hand_card — surfaceVariant bg,
│  │  KES 3,500                         │ │  md corner 12dp, 16dp pad
│  └────────────────────────────────────┘ │  labelLarge onSurfaceVariant +
│                                          │  headlineMedium onSurface bold
└──────────────────────────────────────────┘
```

- Read-only display of `openingCorpus` and `cashOnHand` from `CorpusRepository.getOpeningCorpus(groupId)`.
- Corpus band above becomes visible starting this step and stays live for steps 3-6.

### Step 3 · Savings Collection

```
┌ Savings Collection ─────────────────────┐
│  [ Min. group savings: KES 200/member ] │  min_contribution_chip —
│  (FR-020)                                │  secondaryContainer + onSecondaryContainer
│                                          │
│  ┌──────────────────────────────────┐   │
│  │[AW] Amina Wanjiru                 │   │  savings_member_row — repeats_for
│  │     [Group Savings (KES)      300]│   │  groupMembers, divider between rows
│  │     [Individual Savings (KES) 200]│   │  content: name bodyLarge, 2 text-fields:
│  └──────────────────────────────────┘   │  group_savings_input (KES prefix, min 200,
│  ┌──────────────────────────────────┐   │  keyboard_type number) + individual_savings_input
│  │[PO] Peter Otieno                  │   │  (optional)
│  │     [Group Savings          200 ] │   │  → SetSavingsAmount(memberId, type, amount)
│  │     [Individual Savings     0   ] │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │[GA] Grace Achieng                 │   │
│  │     [Group Savings          250 ] │   │
│  │     [Individual Savings     100 ] │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │[JK] John Kamau                    │   │
│  │     [Group Savings          400 ] │   │
│  │     [Individual Savings     500 ] │   │
│  └──────────────────────────────────┘   │
│  ┌──────────────────────────────────┐   │
│  │[MN] Mary Njeri                    │   │
│  │     [Group Savings          200 ] │   │
│  │     [Individual Savings     0   ] │   │
│  └──────────────────────────────────┘   │
├──────────────────────────────────────────┤
│  Total Savings This Step:                │  running_total_band — primaryContainer bg,
│  KES 1,350                               │  16dp pad · labelMedium key +
│                                          │  headlineSmall bold value (Roboto Mono)
└──────────────────────────────────────────┘
```

- Two inputs per member — `GROUP_LINKED` (min 200) + `INDIVIDUAL` (optional voluntary). Both update `savingsMap` and recompute `runningSavingsTotal` on every keystroke.
- **Validation** — Next tap validates each `groupAmount >= 200`; `SavingsValidation` error caps any input above KES 10,000; `MinContributionNotMet` snackbar names the failing member.
- Corpus band above reflects savings folded into corpus in real time.

### Step 4 · Loan Review

```
┌ Loan Review ────────────────────────────┐
│  ┌──────────────────────────────────┐   │
│  │[AW] Amina Wangari                 │   │  loan_review_row — repeats_for activeLoans
│  │     KES 8,000 loan · KES 5,600    │   │  leading avatar 40dp initials,
│  │     outstanding · Week 4/16       │   │  secondaryContainer bg when !overdue
│  │     [Repayment (KES)         700]│   │  content: memberName bodyLarge +
│  └──────────────────────────────────┘   │  meta bodySmall onSurfaceVariant +
│                                          │  repayment_input text-field
│  ┌──────────────────────────────────┐   │
│  │[JO] Joseph Otieno       [OVERDUE]│   │  errorContainer avatar bg + OVERDUE chip
│  │     KES 12,000 loan · KES 9,600  │   │  visible_when loan.isOverdue == true
│  │     outstanding · Week 4/20      │   │
│  │     [Repayment (KES)         600]│   │
│  │     [Penalty Fine (KES)      100]│   │  fine_input visible_when isOverdue only
│  └──────────────────────────────────┘   │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │[GW] Grace Wanjiku                 │   │
│  │     KES 5,000 loan · KES 3,000   │   │
│  │     outstanding · Week 4/10      │   │
│  │     [Repayment (KES)         500]│   │
│  └──────────────────────────────────┘   │
└──────────────────────────────────────────┘
```

**Empty variant** — when `activeLoans.isEmpty()`:

```
┌ Loan Review ────────────────────────────┐
│                                          │
│                 ✓                        │  no_active_loans_placeholder
│         No Active Loans                  │  checkmark_circle_24_regular icon
│  No members currently have active        │  title titleLarge, body bodyMedium
│  loans. Tap Next to proceed.             │
│                                          │
└──────────────────────────────────────────┘
```

- **Repayment input** → `SetLoanRepayment(loanId, amount)` (transform_state); validated ≤ `loan.outstandingBalance` → `RepaymentExceedsBalance` error if exceeded.
- **Penalty fine input** → `SetLoanFine(loanId, fineAmount)` (transform_state); appears only for overdue loans; folded into `totalFinesCollected`.
- Expected weekly repayment shown as input hint (e.g. "Expected: KES 700").

### Step 5 · Loan Applications

```
┌ Loan Applications ──────────────────────┐
│  [ Available to disburse: KES 12,850 ]  │  corpus_gate_chip — tertiaryContainer,
│                                          │  visible_when totalLoansDisbursed > 0
│                                          │
│  ┌──────────────────────────────────┐   │
│  │ Peter Kamau                       │   │  loan_application_card —
│  │ Requests KES 8,000                │   │  surfaceVariant bg, md corner, 16dp pad,
│  │ Purpose: School fees for two      │   │  12dp bottom margin
│  │ children — Term 3                 │   │  titleSmall + bodyLarge + bodySmall
│  │                                    │   │
│  │ 4 For · 0 Against                 │   │  vote_tally — labelMedium outline
│  │                                    │   │
│  │  [ For ]     [ Against ]           │   │  vote_for_btn / vote_against_btn — outlined
│  │  (selected primaryContainer)      │   │  selected_when loanVotes[app.id]==FOR/AGAINST
│  │                                    │   │  → CastLoanVote(loanId, FOR|AGAINST)
│  │                                    │   │
│  │  [ Chairperson Approve ]           │   │  approve_btn — filled variant, full-width,
│  │  (enabled: role & votesFor>Against)│   │  #2E7D32 bg, onPrimary text, min 56dp
│  └──────────────────────────────────┘   │  → ApproveLoanApplication(loanId)
│                                          │
│  ┌──────────────────────────────────┐   │
│  │ Mary Njeri                        │   │
│  │ Requests KES 4,500                │   │
│  │ Purpose: Restock produce stall    │   │
│  │ ahead of harvest week             │   │
│  │                                    │   │
│  │ 3 For · 1 Against                 │   │
│  │  [ For ]     [ Against ]           │   │
│  │  [ Chairperson Approve ]           │   │
│  └──────────────────────────────────┘   │
└──────────────────────────────────────────┘
```

**Empty variant** — when `pendingLoanApplications.isEmpty()`:

```
┌ Loan Applications ──────────────────────┐
│                                          │
│                 📄                       │  no_pending_loans_placeholder
│    No Pending Applications               │  document_checkmark_24_regular icon
│  No loan applications to review          │  title titleLarge, body bodyMedium
│  this meeting. Tap Next to proceed.      │
│                                          │
└──────────────────────────────────────────┘
```

- **Vote buttons** — mutually exclusive (For fills primaryContainer, Against fills errorContainer). Every member votes on every application; tally updates the local `LoanVoteRecord` state.
- **Approve gate** — enabled only when `currentUserRole == CHAIRPERSON && votesFor > votesAgainst`; disabled state uses `--text-disabled #9E9E9E` on 40% alpha primary.
- **Corpus insufficiency** — `CorpusInsufficient` snackbar surfaces if approved disbursement would drive corpus < 0; approve tap blocked until corpus gate chip goes non-negative.

### Step 6 · Closing Balance & Submit

```
┌ Closing Balance ────────────────────────┐
│  ┌────────────────────────────────────┐ │
│  │ Opening Corpus       KES 51,750    │ │  reconciliation_card —
│  ├────────────────────────────────────┤ │  surfaceVariant bg, md corner, 16dp pad
│  │ + Group Savings      KES 1,350     │ │  info_row × 5 (label labelMedium
│  │ + Loan Repayments    KES 1,800     │ │  onSurfaceVariant / value bodyMedium)
│  │ + Fines Collected    KES 150       │ │  positive rows: value_color primary
│  │ — Loans Disbursed    KES 8,000     │ │  disbursed row: value_color error
│  ├────────────────────────────────────┤ │  divider weight 2dp
│  │ Closing Corpus       KES 47,050    │ │  label titleSmall bold,
│  │                                    │ │  value titleLarge primary bold
│  └────────────────────────────────────┘ │  Roboto Mono for all amounts
│                                          │
│  ┌────────────────────────────────────┐ │
│  │       Submit Meeting               │ │  submit_meeting_btn — filled variant,
│  └────────────────────────────────────┘ │  #2E7D32 bg, onPrimary text, 56dp min,
│                                          │  full-width · loading spinner overlay when
│                                          │  isSubmitting == true
│  You're offline. Meeting data will be    │  offline_submit_note — visible_when isOffline,
│  saved locally and synced when connected │  bodySmall onSurfaceVariant, center-aligned
└──────────────────────────────────────────┘
```

- **Reconciliation math** (visible to user): `openingCorpus + runningSavingsTotal + totalRepayments + totalFinesCollected − totalLoansDisbursed = closingCorpus`.
- **Submit** — runs ordered API sequence `record meeting → attendance → savings → repayments → disbursals → PATCH corpus` against Fineract; on 5xx or offline enqueues to SQLDelight `sync_queue` for Store5 drain on reconnect.
- Footer Next button label swaps to **"Submit Meeting"** on step 6 (mirrors this in-body button).

---

## States (screen_state)

The ui.yaml declares 4 `screen_state` members driving the wizard shell (independent of the 7 step-content bodies above).

### `loading`
Initial parallel fetch of 5 payloads: `previousMeetingSummary`, `groupMembers` (GroupDetail), `openingCorpus + cashOnHand` (CorpusRecord), `activeLoans` (LoanSummary projection over LoanDetail), `pendingLoanApplications`.

```
[ ✕ ]  Meeting #4  (subtitle deferred)     ← top_app_bar visible
●───○───○───○───○───○───○                   ← step_stepper skeleton (all inactive)
[ shimmer band 24dp — corpus_band skeleton ]
────────────────────────────────────────
[ shimmer card ]   ← 96dp × full, corner 12dp, surfaceVariant, 1.4s ease-in-out
[ shimmer card ]
[ shimmer card ]
[ shimmer card ]
[ shimmer card ]
[ shimmer inputs row ]
────────────────────────────────────────
[ shimmer footer 72dp ]
```

- Top bar retains "Meeting #{meetingNumber}"; subtitle hidden.
- Footer buttons inert (`pointer-events: none`) during load.
- Respects `prefers-reduced-motion: reduce`.

### `content` (see per-step layouts above)
Wizard active. `currentStep ∈ [0..6]` selects the body. Footer Back visible when step > 0; Next label swaps to "Submit Meeting" on step 6.

### `submitting`
Post-Submit overlay while Fineract sequence is in flight.

```
┌ Closing Balance ────────────────────────┐
│   [reconciliation card, dimmed 60%]      │
│   [submit button, disabled]              │
│                                          │
│                 ⟳                        │  CircularProgressIndicator centered,
│         Submitting meeting…              │  primary tint (#2E7D32), 48dp
│                                          │
│  [ Back ]                     [ ⟳ ]      │  Footer disabled, next shows spinner
└──────────────────────────────────────────┘
```

- Backdrop scrim `rgba(0,0,0,0.32)` over reconciliation card.
- Footer Back button disabled to prevent race.
- Spinner respects reduced-motion (renders as static primary indicator).

### `submit_success`
Brief toast then navigate to `meeting-summary`.

```
        ┌──────────────────────────────┐
        │ Meeting #4 submitted         │  Snackbar — primaryContainer bg,
        │ successfully!                │  onPrimaryContainer text
        └──────────────────────────────┘  duration 2000ms, slide-up
                                          → NavigateToMeetingSummary(meetingId, meetingNumber, groupId)
```

### `submit_error`
API failed AND offline enqueue also failed — retry from snackbar.

```
┌ Closing Balance ────────────────────────┐
│  [reconciliation card, submit btn re-enabled]│
│                                          │
│  ┌────────────────────────────────────┐ │
│  │ Meeting submission failed. Data    │ │  submit_error_snackbar — errorContainer bg,
│  │ saved offline and will sync when   │ │  onErrorContainer text · duration 6000ms
│  │ connected.        [ Retry ]        │ │  action_text "Retry" → SubmitMeeting (call_api)
│  └────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

Error taxonomy (typed):
- `CorpusInsufficient` — Step 5 approve blocked
- `AttendanceIncomplete` — Step 1 → Step 2 advance blocked
- `SavingsValidation` — Step 3 amount > KES 10,000
- `MinContributionNotMet` — Step 3 groupAmount < KES 200
- `RepaymentExceedsBalance` — Step 4 repayment > outstanding
- `SubmitFailed` — Step 6 API + offline queue both failed

---

## Demo Data (state: `content`, from `demo-data.yaml`)

Meeting #5 in progress for Mwangaza Women's Group (groupId 1, Kisumu West). Opening corpus KES 51,750, cash on hand KES 3,500. Five members recorded on the previous roster.

### Group members (5 rows for attendance + savings)

| memberId | Name          | Initials | Role        |
|----------|---------------|----------|-------------|
| m-101    | Amina Wanjiru | AW       | TREASURER   |
| m-102    | Peter Otieno  | PO       | MEMBER      |
| m-103    | Grace Achieng | GA       | SECRETARY   |
| m-104    | John Kamau    | JK       | CHAIRPERSON |
| m-105    | Mary Njeri    | MN       | MEMBER      |

### Active loans (Step 4)

| loanId | Member         | Principal | Outstanding | Overdue | Week | Expected Weekly |
|--------|----------------|-----------|-------------|---------|------|-----------------|
| 5001   | Amina Wangari  | KES 8,000 | KES 5,600   | no      | 4/16 | KES 700         |
| 5002   | Joseph Otieno  | KES 12,000| KES 9,600   | **yes** | 4/20 | KES 600         |
| 5003   | Grace Wanjiku  | KES 5,000 | KES 3,000   | no      | 4/10 | KES 500         |

### Pending applications (Step 5)

| id                | Member       | Requested | Purpose                                  | Votes For | Against |
|-------------------|--------------|-----------|------------------------------------------|-----------|---------|
| PENDING-5004-NEW  | Peter Kamau  | KES 8,000 | School fees for two children — Term 3    | 4         | 0       |
| PENDING-5005-NEW  | Mary Njeri   | KES 4,500 | Restock produce stall ahead of harvest   | 3         | 1       |

### Sample savings entries (Step 3, mixed contribution levels)

| memberId | Group KES | Individual KES |
|----------|-----------|----------------|
| m-101    | 300       | 200            |
| m-102    | 200       | 0              |
| m-103    | 250       | 100            |
| m-104    | 400       | 500            |
| m-105    | 200       | 0              |

Running total after step: **KES 1,950** (group KES 1,350 + individual KES 600). Reconciliation on step 6 uses group-linked KES 1,350 as `runningSavingsTotal` (individual savings post separately to per-member savings accounts on submit).

### Previous meeting summary (Step 0)

Meeting #4 · 05 May 2026 · Total collected KES 2,500 · Closing corpus KES 51,750 · Attendance 5/5 → becomes `openingCorpus` of the current meeting.

---

## Interaction Patterns

1. **Step advance** (`NextStep`, footer Next) → validates the current step (attendance completeness, savings ≥ 200 & ≤ 10,000, repayment ≤ outstanding, corpus non-negative post-disbursal) then `currentStep++`; also fires `SaveProgressLocally` to persist wizard state into SQLDelight `meeting_wizard_state`. On step 6, `Next` label swaps to "Submit Meeting" and delegates to `SubmitMeeting`.
2. **Step retreat** (`PreviousStep`, footer Back) → `currentStep--`, all entered data preserved in memory + local persistence (no re-fetch, no clear).
3. **Set attendance** (segmented button `PRESENT|LATE|ABSENT`) → `SetAttendance(memberId, status)` (transform_state); auto-derives `lateFines[memberId] = 50` or `absentFines[memberId] = 100` per FR-012; folded into `totalFinesCollected`.
4. **Set savings** (both group + individual inputs) → `SetSavingsAmount(memberId, amount, type)` (transform_state) on each keystroke; `runningSavingsTotal` recomputed live; corpus band above updates instantly.
5. **Set loan repayment / fine** (Step 4 inputs) → `SetLoanRepayment` / `SetLoanFine` (transform_state); validated ≤ outstanding balance; fine input surfaces only when `loan.isOverdue == true`.
6. **Cast loan vote** (Step 5 For/Against buttons) → `CastLoanVote(loanId, FOR|AGAINST)` (transform_state); local tally updates; final aggregate posts to `dt_loan_vote` datatable on submit.
7. **Chairperson approve** (Step 5 approve button, gated) → `ApproveLoanApplication(loanId)` (transform_state); queues the disbursal for the submit sequence; corpus insufficiency blocks the tap with an error snackbar.
8. **Submit** (Step 6 button OR footer Next on step 6) → `SubmitMeeting` (call_api, external `fineract-rest + sqldelight`); ordered sequence: `POST /meetings → POST /attendance → POST /savings/{n}/deposits → POST /loans/{n}/repayments → POST /loans/{n}/disbursals → PATCH /groups/{id}/corpus`; on any 5xx or offline the full payload is enqueued to the `sync_queue` SQLDelight table for Store5 drain on reconnect.
9. **Back / close** (top app bar ✕) → `NavigateBack` (navigate) → pops to `meeting-calendar`; wizard progress remains persisted in local `meeting_wizard_state` for resumption.
10. **View full previous report** (Step 0 button) → `ViewFullPreviousMeeting` (navigate) → pushes `previous-meeting-review(meetingNumber, groupId)`.
11. **Dismiss error snackbar** (auto or swipe) → `DismissError` (emit_event) → clears `stepValidationError`.
12. **Auto save on background** → `SaveProgressLocally` fires on app background AND every successful step advance.

---

## Accessibility

- Every segmented-button reads as a labeled tab ("Attendance for {member.name}, currently {status}").
- Fine chips are text + colored fill (never color-only): "Fine: KES 50" always readable.
- Roles announced next to member names (`TREASURER` / `CHAIRPERSON` / etc.) so screen reader users hear governance roles.
- Currency amounts labelled with "KES {amount} Kenyan Shillings" for TalkBack/VoiceOver.
- Min touch targets: 64dp member rows, 48dp segmented buttons, 56dp submit CTA, 28dp stepper dots (grouped touch region ≥ 48dp).
- Corpus math on Step 6 announced as continuous prose: "Opening corpus fifty-one thousand seven hundred fifty. Plus group savings one thousand three hundred fifty. Plus loan repayments one thousand eight hundred. Plus fines one hundred fifty. Minus loans disbursed eight thousand. Closing corpus forty-seven thousand fifty."
- Focus ring: 2dp `#2E7D32` primary outline, 2dp offset (buttons, inputs, chips).
- Reduced motion: shimmer + stepper transition + submit spinner all collapse to static frames.
- Locales covered: English, Swahili (`step6_title: "Salio la Kufunga"`), French (`step6_title: "Solde de Clôture"`), Hindi (`step6_title: "समापन शेष"`) — full i18n table for step titles + validation errors + submit toasts (see ui.yaml `i18n.en`).

---

## Motion & Feedback

- Step advance/retreat: 200ms slide-in horizontal (ease-out) — disabled under `prefers-reduced-motion`.
- Corpus band recompute: 150ms crossfade on value change (running savings totals as they type).
- Segmented button select: MD3 ripple + 150ms fill transition.
- Fine chip appearance: 150ms fade-in when attendance flips to LATE/ABSENT.
- Submit spinner: MD3 CircularProgressIndicator, primary tint, 800ms rotation (disabled under reduced motion).
- Success toast: 300ms slide-up, 2000ms visible, 300ms slide-down.
- Error snackbar: 300ms slide-up, 4000ms (validation) or 6000ms (submit) visible with Retry action.
- Stepper progression: completed dot fills primaryContainer with 150ms crossfade.

---

## Data Flow (ui.yaml `business_logic.kind: composite`)

**Internal lib**: `cmp-network-monitor`
**External libs**: `fineract-rest`, `sqldelight`, `store5`

Read paths (Step 0/1 parallel prefetch during `loading` state):
- `previousMeetingSummary` ← `MeetingRepository.getRecentMeeting(groupId)` (Store5 stream over SQLDelight cache + Fineract `GET /groups/{id}/meetings/recent`)
- `groupMembers[]` ← `GroupDetail.activeClientMembers` (from `GET /groups/{id}?fields=activeClientMembers`)
- `openingCorpus`, `cashOnHand` ← `CorpusRepository.getOpeningCorpus(groupId)` (from `GET /groups/{id}/corpus`)
- `activeLoans[]` ← `LoanRepository.getActiveGroupLoans(groupId)` (Fineract m_loan projected into `LoanSummary` view-model DTO)
- `pendingLoanApplications[]` ← `LoanRepository.getPending(groupId)` + local vote tally overlay

Write path (Step 6 submit, ordered):
1. `POST /collectionsheet` (record meeting) — establishes `meetingId`
2. `POST /collectionsheet/{meetingId}/attendance` — attendanceMap entries
3. `POST /savingsaccounts/{n}/transactions` — per-member deposits
4. `POST /loans/{n}/transactions` (type: repayment) — repayments
5. `POST /loans/{n}/transactions` (type: chargeoff for overdue fines) — loan penalty fines
6. `POST /loans/{n}/transactions` (type: disburse) — approved disbursals
7. `PATCH /groups/{id}/corpus` — closing balance write-through

Offline behavior — when `NetworkMonitor.isOffline == true` OR any POST returns 5xx: the full submit payload is serialized into SQLDelight `sync_queue` with a monotonic `sync_ordinal`, the `submit_success` toast still fires ("Meeting saved offline — will sync when connected"), and NavigateToMeetingSummary proceeds. Store5 drains the queue on next connectivity change via `NetworkMonitor` events, retrying in-order with exponential backoff.

Local state persistence — every step advance auto-saves the full wizard state (attendance + savings + repayments + votes + approvals) to SQLDelight `meeting_wizard_state` keyed by `meetingId`, so mid-wizard close (or app background) can resume from the same step on re-entry.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/meeting-conduct/ui.yaml` |
| API contract | `idea-layer/screens/meeting-conduct/api.yaml` |
| Data flow | `idea-layer/screens/meeting-conduct/data-flow.yaml` |
| Demo data | `idea-layer/screens/meeting-conduct/demo-data.yaml` |
| Flow | `idea-layer/screens/meeting-conduct/flow.yaml` |
| Tests | `idea-layer/screens/meeting-conduct/tests.yaml` |
| Preview HTML (per step + shell states) | `idea-layer/screens/meeting-conduct/preview/{loading,content,submitting,submit_success,submit_error}.html` |
| Stitch prompts (per state) | `idea-layer/screens/meeting-conduct/prompts/{loading,content,submitting,submit_success,submit_error}.md` |
| Feature-group mockup | `idea-layer/mockups/meeting-management/MOCKUP.md` |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from `ui.yaml` + `demo-data.yaml` + `design-system/DESIGN.md` per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- This is a `wizard` screen with 7 step-content blocks — the "content" state renders one step at a time via `visible_when: currentStep == N`. All 7 step layouts are documented above; the wizard shell (top bar + stepper + corpus band + footer) is persistent across steps.
- The `composite` business_logic kind indicates this screen is NOT template-generated — every action either transforms local state (`transform_state`) or triggers the ordered submit sequence (`call_api`) on step 6.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features meeting-conduct
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to ui.yaml components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
