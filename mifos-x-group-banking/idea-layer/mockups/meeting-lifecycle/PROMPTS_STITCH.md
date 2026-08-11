# PROMPTS_STITCH — meeting-lifecycle
# MifosSave (mifos-x-group-banking) | Feature FR-003 / FR-019
# Generated: 2026-05-06
# Sections: 6 | Total lines: ≥1,200

---

## SECTION 1 — Design System Context

### 1.1 Brand Identity
MifosSave is a VSLA (Village Savings and Loan Association) group banking app designed for rural East African women's savings groups. The Mwangaza Women's Group (mwangaza = "light" in Swahili) conducts weekly meetings to collect savings, review loans, and track their shared corpus fund. The UI must project trust, growth, and communal ownership. Every color choice is deliberate and culturally resonant.

### 1.2 Color System — Light Theme

Primary colors (VSLA-green — growth, agricultural prosperity, trust):
- primary: #2E7D32
- on_primary: #FFFFFF
- primary_container: #A6F1A6
- on_primary_container: #002106

Secondary colors (amber — shared coin, harvest wealth, transactions):
- secondary: #FF8F00
- on_secondary: #FFFFFF
- secondary_container: #FFDDB3
- on_secondary_container: #2A1700

Tertiary colors (trust-blue — informational, corpus balance, financial data):
- tertiary: #1565C0
- on_tertiary: #FFFFFF
- tertiary_container: #D2E4FF
- on_tertiary_container: #001C39

Error and warning:
- error: #D32F2F
- on_error: #FFFFFF
- error_container: #FFDAD6
- on_error_container: #410002
- warning = secondary (#FF8F00) — used for late fines, unresolved items
- warning_container = secondary_container (#FFDDB3)
- on_warning_container = on_secondary_container (#2A1700)

Surface and background:
- background: #FFFFFF
- on_background: #1A1C19
- surface: #FAFAFA
- on_surface: #1A1C19
- surface_variant: #DEE5DA
- on_surface_variant: #424942
- outline: #727971
- outline_variant: #C2C9BD
- scrim: #000000

Inverse (for dark snackbars, tooltips):
- inverse_surface: #2F312D
- inverse_on_surface: #F0F1EB
- inverse_primary: #8BD68F

### 1.3 Color System — Dark Theme

- primary: #8BD68F
- on_primary: #003910
- primary_container: #00531A
- on_primary_container: #A6F1A6
- secondary: #FFB95C
- on_secondary: #472A00
- secondary_container: #653E00
- on_secondary_container: #FFDDB3
- tertiary: #9FCAFF
- on_tertiary: #00325B
- tertiary_container: #004A82
- on_tertiary_container: #D2E4FF
- error: #FFB4AB
- on_error: #690005
- error_container: #93000A
- on_error_container: #FFDAD6
- background: #1A1C19
- on_background: #E2E3DD
- surface: #121412
- on_surface: #E2E3DD
- surface_variant: #424942
- on_surface_variant: #C2C9BD

### 1.4 Typography — Noto Sans

All text uses Noto Sans for multilingual East African language support (Swahili, English). Scale configured as "large" for rural/low-vision users.

| Role | Size (sp) | Line Height (sp) | Letter Spacing (sp) | Weight |
|------|-----------|-----------------|---------------------|--------|
| displayLarge | 57 | 64 | -0.25 | 400 |
| displayMedium | 45 | 52 | 0 | 400 |
| displaySmall | 36 | 44 | 0 | 400 |
| headlineLarge | 32 | 40 | 0 | 400 |
| headlineMedium | 28 | 36 | 0 | 400 |
| headlineSmall | 24 | 32 | 0 | 400 |
| titleLarge | 22 | 28 | 0 | 500 |
| titleMedium | 16 | 24 | 0.15 | 500 |
| titleSmall | 14 | 20 | 0.1 | 500 |
| bodyLarge | 16 | 24 | 0.5 | 400 |
| bodyMedium | 14 | 20 | 0.25 | 400 |
| bodySmall | 12 | 16 | 0.4 | 400 |
| labelLarge | 14 | 20 | 0.1 | 500 |
| labelMedium | 12 | 16 | 0.5 | 500 |
| labelSmall | 11 | 16 | 0.5 | 500 |

KES amounts displayed in large cards use Noto Sans bold weight (700) for emphasis.

### 1.5 Spacing Scale (dp)

- xxs: 2dp — icon internal padding
- xs: 4dp — tight inline spacing
- sm: 8dp — small gaps between chips
- md: 12dp — between card sections
- lg: 16dp — standard horizontal padding
- xl: 24dp — card internal top padding
- xxl: 32dp — between major screen sections
- 3xl: 48dp — empty state vertical padding
- 4xl: 64dp — empty state icon size

Comfortable density: 8dp base grid. All vertical spacing is a multiple of 4dp.

### 1.6 Shape (Corner Radius)

| Name | dp | Usage |
|------|----|-------|
| none | 0dp | flat dividers |
| extra_small | 4dp | snackbars, progress bars |
| small | 8dp | chips, small cards |
| medium | 12dp | standard cards, text fields |
| large | 16dp | upcoming meeting card, corpus card |
| extra_large | 28dp | dialogs, hero cards |
| full | 9999dp | circular chips, FABs, avatars |

### 1.7 Elevation Levels

| Level | dp | Tonal Alpha | Usage |
|-------|-----|------------|-------|
| level_0 | 0dp | 0.00 | Flat surface backgrounds |
| level_1 | 1dp | 0.05 | Subtle raised cards |
| level_2 | 3dp | 0.08 | Standard cards (savings rows) |
| level_3 | 6dp | 0.11 | Upcoming meeting card |
| level_4 | 8dp | 0.12 | Wizard navigation footer |
| level_5 | 12dp | 0.14 | Dialogs, bottom sheets |

Tonal elevation: primary color tinted surface at the alpha above, mixed with surface color. Used for Material You tonal surface variants.

### 1.8 Motion System

Durations:
- short_1: 50ms — micro interactions (button press state)
- short_2: 100ms — instant feedback (running total update)
- short_3: 150ms — fade-ins for fine chips
- short_4: 200ms — snackbar appear, chip transitions
- medium_1: 250ms — step content crossfade
- medium_2: 300ms — snackbar slide-up, stepper fill
- medium_3: 350ms — complex state transitions
- medium_4: 400ms — screen entry animations
- long_1: 450ms — scroll-to-step navigation
- long_2: 500ms — full-page transitions

Easing curves:
- standard: cubic-bezier(0.2, 0.0, 0, 1.0) — most UI movements
- emphasized: cubic-bezier(0.2, 0.0, 0, 1.0) — hero element entries
- decelerated: cubic-bezier(0.0, 0.0, 0, 1.0) — elements entering screen
- accelerated: cubic-bezier(0.3, 0.0, 1.0, 1.0) — elements leaving screen

### 1.9 Accessibility Standards

- Minimum touch target: 48dp × 48dp for all interactive elements
- Normal text contrast: 4.5:1 (WCAG AA)
- Large text / icons contrast: 3.0:1 (WCAG AA large)
- Focus ring: 3dp, primary color outline
- TalkBack: All elements have content_description specified
- Role declarations: button, progressbar, group — per component spec
- Error states: never use color alone; always include text label or icon
- Offline mode: "Offline" chip on TopAppBar (warningContainer background) + text note on submit step

---

## SECTION 2 — Screen Layouts

### 2.1 MeetingCalendarScreen — Full Component Tree

```
MeetingCalendarScreen
├── TopAppBar (height: 56dp, background: surface #FAFAFA)
│   ├── NavigationIcon: none (root screen in bottom nav flow)
│   ├── Title: "Meetings" (titleLarge 22sp, on_surface #1A1C19)
│   ├── Subtitle: "Mwangaza Women's Group" (bodyMedium 14sp, on_surface_variant #424942)
│   └── Actions
│       └── IconButton: FluentIcons.calendar_list_24_regular (toggle view mode)
│           ├── size: 24dp
│           ├── tint: on_surface_variant #424942
│           └── min_touch_target: 48dp
├── [Optional] NetworkErrorBanner
│   ├── visible_when: error != null AND meetings.isNotEmpty()
│   ├── background: error_container #FFDAD6
│   ├── padding: 12dp
│   ├── Text: "Showing cached meetings — tap Retry to refresh" (bodySmall, on_error_container)
│   └── TextButton "Retry" → RefreshMeetings
├── LazyColumn
│   ├── Item: UpcomingMeetingCard (visible_when: upcoming meeting exists)
│   │   ├── position: pinned at top, scrolls away
│   │   ├── background: primary_container #A6F1A6
│   │   ├── corner_radius: 16dp
│   │   ├── padding: 16dp
│   │   ├── margin: 16dp horizontal, 8dp top
│   │   ├── elevation: 4dp
│   │   ├── Text "SCHEDULED MEETING" (labelMedium 12sp, on_primary_container #002106)
│   │   ├── Text "Meeting #4" (headlineSmall 24sp, on_primary_container, bold)
│   │   ├── Text "Wednesday, 7 May 2026" (bodyLarge 16sp, on_primary_container)
│   │   ├── AssistChip "Upcoming" (background: primary #2E7D32, text: on_primary #FFFFFF, corner: full)
│   │   └── FilledButton "Start Meeting"
│   │       ├── background: primary #2E7D32
│   │       ├── text_color: on_primary #FFFFFF
│   │       ├── min_height: 48dp
│   │       ├── full_width: true
│   │       ├── margin_top: 12dp
│   │       └── onClick → StartMeeting(meetingId, meetingNumber) → NavigateToConduct
│   ├── Item: SectionHeader "PAST MEETINGS" (titleSmall 14sp, on_surface_variant, ph: 16dp, pt: 8dp, pb: 4dp)
│   └── Items: MeetingListItem (repeats for past meetings)
│       ├── min_height: 72dp
│       ├── padding_horizontal: 16dp
│       ├── padding_vertical: 12dp
│       ├── divider: 1dp outline_variant
│       ├── Leading: CircleAvatar(text="#N", size: 40dp)
│       │   ├── background completed: primary_container #A6F1A6
│       │   └── background missed: error_container #FFDAD6
│       ├── Content column:
│       │   ├── Text "Meeting #3" (bodyLarge 16sp, on_surface #1A1C19)
│       │   └── Text "28 Apr 2026 · 5/5 present" (bodySmall 12sp, on_surface_variant #424942)
│       ├── Trailing column (alignment: end):
│       │   ├── Text "KES 1,850" (labelLarge 14sp, primary #2E7D32)
│       │   └── AssistChip
│       │       ├── completed: background successContainer (approximated: primary_container), text "Completed"
│       │       └── missed: background error_container #FFDAD6, text "Missed"
│       └── onClick → OpenPastMeeting → NavigateToReview
└── [Conditional overlays]
    ├── LoadingSkeleton (visible_when: isLoading)
    │   ├── 4 shimmer items
    │   ├── item_height: 72dp
    │   └── corner_radius: 12dp, margin: 16dp
    └── EmptyState (visible_when: meetings.isEmpty() AND !isLoading)
        ├── Icon: FluentIcons.calendar_empty_24_regular (64dp, on_surface_variant)
        ├── Title: "No Meetings Yet" (headlineSmall, centered)
        └── Subtitle: "Meetings will appear here once scheduled" (bodyMedium, centered)
```

### 2.2 MeetingConductScreen — Full Component Tree

```
MeetingConductScreen
├── TopAppBar (background: surface #FAFAFA, 64dp with subtitle)
│   ├── NavigationIcon: FluentIcons.dismiss_24_regular → NavigateBack
│   ├── Title: "Meeting #4" (titleLarge 22sp)
│   ├── Subtitle: "Step 2 of 7 — Attendance" (bodyMedium 14sp, on_surface_variant)
│   └── Actions:
│       └── [Offline] chip (visible_when: isOffline; background: secondary_container; text: on_secondary_container; corner: full; labelSmall)
├── HorizontalStepper (margin: 16dp, height: 48dp)
│   ├── 7 steps: Review(0), Attendance(1), Balance(2), Savings(3), Loans(4), Apply(5), Close(6)
│   ├── Active: filled primary #2E7D32 circle, labelSmall white inside
│   ├── Completed: filled primary_container #A6F1A6 circle with checkmark icon
│   ├── Inactive: outline #C2C9BD circle with outline text
│   ├── Connector: 1dp outline #727971 horizontal line between steps
│   └── Step labels below each circle (labelSmall 11sp)
├── CorpusBand (visible_when: currentStep >= 2, background: tertiary_container #D2E4FF, pv: 8dp, ph: 16dp)
│   ├── Text "Corpus: KES X" (labelLarge 14sp, on_tertiary_container #001C39)
│   └── Text "Cash on Hand: KES Y" (labelMedium 12sp, on_tertiary_container #001C39)
├── StepContent (fills remaining height, scrollable)
│   ├── Step0: PreviousMeetingReview (visible_when: currentStep == 0)
│   │   ├── Title "Previous Meeting Summary" (titleMedium, mb: 12dp)
│   │   ├── SummaryCard (background: surface_variant #DEE5DA, corner: 12dp, padding: 16dp)
│   │   │   ├── InfoRow "Meeting" / "#3"
│   │   │   ├── InfoRow "Date" / "28 Apr 2026"
│   │   │   ├── InfoRow "Total Collected" / "KES 1,850"
│   │   │   ├── InfoRow "Closing Corpus" / "KES 12,400"
│   │   │   └── InfoRow "Attendance" / "5/5"
│   │   └── OutlinedButton "View Full Report" (mt: 12dp, min-h: 48dp) → ViewFullPreviousMeeting
│   ├── Step1: Attendance (visible_when: currentStep == 1)
│   │   ├── Header "Record Attendance" (titleMedium)
│   │   ├── Chip "Late: KES 50 fine · Absent: KES 100 fine (FR-012)" (secondary_container #FFDDB3, mb: 12dp)
│   │   ├── LazyColumn of AttendanceMemberRow × 5
│   │   │   ├── min_height: 64dp; pv: 8dp; divider: true
│   │   │   ├── Leading: CircleAvatar(initials, 40dp, secondary_container #FFDDB3)
│   │   │   ├── Content: name (bodyLarge) + role (labelSmall, primary)
│   │   │   ├── Trailing: SegmentedButton(PRESENT | LATE | ABSENT)
│   │   │   │   ├── PRESENT: checkmark icon, selected: primary
│   │   │   │   ├── LATE: clock icon, selected: secondary
│   │   │   │   └── ABSENT: dismiss icon, selected: error
│   │   │   └── FineChip (below row, visible_when: LATE or ABSENT)
│   │   │       ├── LATE → "Fine: KES 50" (error_container #FFDAD6)
│   │   │       └── ABSENT → "Fine: KES 100" (error_container #FFDAD6)
│   │   └── ProgressChip "X/5 recorded" (mt: 12dp)
│   │       ├── incomplete: background surface_variant
│   │       └── complete (5/5): background primary_container #A6F1A6
│   ├── Step2: OpeningBalance (visible_when: currentStep == 2)
│   │   ├── Header "Opening Balance" (titleMedium, mb: 12dp)
│   │   ├── CorpusCard (background: primary_container #A6F1A6, corner: 16dp, padding: 24dp, mb: 12dp)
│   │   │   ├── "Group Corpus Fund" (labelLarge, on_primary_container)
│   │   │   ├── "KES 12,400" (displaySmall 36sp bold, on_primary_container)
│   │   │   └── "At start of Meeting #4" (bodySmall, on_primary_container)
│   │   ├── CashCard (background: surface_variant, corner: 12dp, padding: 16dp)
│   │   │   ├── "Cash on Hand" (labelLarge, on_surface_variant)
│   │   │   └── "KES 2,000" (headlineMedium 28sp, on_surface)
│   │   └── ConfirmText "Confirm these balances are correct before proceeding." (bodySmall, centered, mt: 12dp)
│   ├── Step3: SavingsCollection (visible_when: currentStep == 3)
│   │   ├── Header "Savings Collection" (titleMedium, mb: 4dp)
│   │   ├── MinContribChip "Min. group savings: KES 200/member (FR-020)" (secondary_container, mb: 12dp)
│   │   ├── LazyColumn of SavingsMemberRow × 5
│   │   │   ├── pv: 12dp; divider: true
│   │   │   ├── Leading: CircleAvatar(initials, 40dp, secondary_container)
│   │   │   ├── Name (bodyLarge)
│   │   │   ├── TextField "Group Savings (KES)" (hint: "Min. 200", prefix: KES, keyboard: number, min-h: 48dp)
│   │   │   │   └── error_text shown when amount > 0 AND amount < 200: "Below minimum KES 200 required"
│   │   │   └── TextField "Individual Savings (KES)" (hint: "Optional", mt: 8dp, min-h: 48dp)
│   │   └── RunningTotalBand (background: primary_container #A6F1A6, padding: 16dp, mt: 8dp)
│   │       ├── "Total Savings This Step:" (labelMedium, on_primary_container)
│   │       └── "KES 1,000" (headlineSmall 24sp bold, on_primary_container)
│   ├── Step4: LoanReview (visible_when: currentStep == 4)
│   │   ├── Header "Loan Review & Repayments" (titleMedium, mb: 12dp)
│   │   ├── LazyColumn of LoanReviewRow (repeats for activeLoans)
│   │   │   ├── pv: 12dp; divider: true
│   │   │   ├── Leading: CircleAvatar(initials, 40dp) — error_container if overdue, secondary_container otherwise
│   │   │   ├── Name (bodyLarge)
│   │   │   ├── Details "KES 1,500 loan · KES 875 outstanding · Week 4/12" (bodySmall, on_surface_variant)
│   │   │   ├── [OVERDUE] chip (error_container, visible_when: loan.isOverdue)
│   │   │   ├── TextField "Repayment (KES)" (hint: "Expected: KES 500", mt: 8dp, min-h: 48dp)
│   │   │   │   └── error_text: "Cannot exceed outstanding balance" (when repayment > outstanding)
│   │   │   └── TextField "Penalty Fine (KES)" (visible_when: isOverdue, mt: 8dp, min-h: 48dp)
│   │   └── EmptyState (visible_when: activeLoans.isEmpty())
│   │       ├── icon: checkmark_circle, tint: primary
│   │       └── "No Active Loans — Tap Next to proceed."
│   ├── Step5: LoanApplications (visible_when: currentStep == 5)
│   │   ├── Header "Loan Applications" (titleMedium, mb: 4dp)
│   │   ├── CorpusGateChip "Available to disburse: KES 14,025" (tertiary_container, visible when loans pending)
│   │   ├── LazyColumn of LoanApplicationCard (repeats for pendingLoanApplications)
│   │   │   ├── background: surface_variant; corner: 12dp; padding: 16dp; mb: 12dp
│   │   │   ├── MemberName (titleSmall)
│   │   │   ├── "Requests KES 1,500" (bodyLarge)
│   │   │   ├── "Purpose: School fees" (bodySmall, on_surface_variant)
│   │   │   ├── "3 For · 1 Against" (labelMedium, outline)
│   │   │   ├── Row:
│   │   │   │   ├── OutlinedButton "For ↑" (selected: primary_container bg; min-h: 48dp) → CastLoanVote(FOR)
│   │   │   │   └── OutlinedButton "Against ↓" (selected: error_container bg; ml: 8dp; min-h: 48dp) → CastLoanVote(AGAINST)
│   │   │   └── FilledButton "Chairperson Approve" (bg: primary; full-width; mt: 8dp; enabled: role=CHAIRPERSON AND majority FOR)
│   │   └── EmptyState (visible_when: pendingLoanApplications.isEmpty())
│   └── Step6: ClosingBalance (visible_when: currentStep == 6)
│       ├── Header "Closing Balance & Reconciliation" (titleMedium, mb: 12dp)
│       ├── ReconciliationCard (surface_variant, corner: 12dp, padding: 16dp, mb: 16dp)
│       │   ├── InfoRow "Opening Corpus" / "KES 12,400"
│       │   ├── Divider 1dp
│       │   ├── InfoRow "+ Group Savings" / "KES 1,000" (value_color: primary)
│       │   ├── InfoRow "+ Loan Repayments" / "KES 500" (value_color: primary)
│       │   ├── InfoRow "+ Fines Collected" / "KES 50" (value_color: primary)
│       │   ├── InfoRow "— Loans Disbursed" / "KES 1,500" (value_color: error #D32F2F)
│       │   ├── Divider 2dp
│       │   └── InfoRow "Closing Corpus" / "KES 12,450" (label: titleSmall, value: titleLarge, primary)
│       ├── Row of summary chips:
│       │   ├── "4/5 Present" chip (primary_container)
│       │   └── "Fines: KES 50" chip (secondary_container/warningContainer)
│       ├── FilledButton "Submit Meeting" (bg: primary, min-h: 56dp, full-width, loading when isSubmitting)
│       └── Text "You're offline — data saved locally and will sync when connected." (bodySmall, visible_when: isOffline)
├── WizardNavigationFooter (sticky bottom, elevation: 8dp, background: surface, padding: 16dp)
│   ├── OutlinedButton "Back" (flex: 1, min-h: 48dp, visible_when: currentStep > 0)
│   └── FilledButton "Next" / "Submit Meeting" (flex: 1, ml: 8dp, min-h: 48dp, primary)
├── StepValidationErrorSnackbar (visible_when: stepValidationError != null, error_container, 4000ms)
└── SubmitErrorSnackbar (visible_when: submitError != null, error_container, 6000ms, action: "Retry")
```

### 2.3 MeetingSummaryScreen — Full Component Tree

```
MeetingSummaryScreen
├── TopAppBar (background: surface)
│   ├── NavigationIcon: FluentIcons.arrow_left_24_regular → NavigateDone
│   ├── Title: "Meeting #4 Summary" (titleLarge)
│   ├── Subtitle: "7 May 2026" (bodyMedium, on_surface_variant)
│   └── Actions: IconButton FluentIcons.share_24_regular → ShareMeetingReport (loading_when: isSharing)
├── LazyColumn
│   ├── HeroCard (background: primary #2E7D32, corner: 28dp, padding: 24dp, margin: 16dp, elevation: 4dp)
│   │   ├── "Total Collected" (labelLarge, on_primary #FFFFFF)
│   │   ├── "KES 1,750" (displaySmall 36sp bold, on_primary)
│   │   ├── "Meeting #4 · 7 May 2026" (bodyMedium, on_primary 80% opacity)
│   │   └── AssistChip "Corpus: KES 12,450" (primary_container bg, on_primary_container text, mt: 12dp)
│   ├── MetricGrid (2 columns, gap: 12dp, margin_horizontal: 16dp, mb: 16dp)
│   │   ├── MetricCard "Attendance" / "5/5" (icon: people_checkmark, primary_container bg)
│   │   ├── MetricCard "Group Savings" / "KES 1,000" (icon: people_money, primary_container bg)
│   │   ├── MetricCard "Individual Savings" / "KES 750" (icon: person_money, secondary_container #FFDDB3 bg)
│   │   ├── MetricCard "Loan Repayments" / "KES 500" (icon: arrow_circle_down, tertiary_container #D2E4FF bg)
│   │   ├── MetricCard "Fines Collected" / "KES 50" (icon: warning, secondary_container warning bg)
│   │   └── MetricCard "Loans Disbursed" / "KES 1,500" (icon: arrow_circle_up, error_container #FFDAD6 bg)
│   ├── SavingsBreakdownSection (margin: 16dp, mb: 16dp)
│   │   ├── SectionHeader "Savings Breakdown" (titleSmall, on_surface_variant, mb: 8dp)
│   │   └── SavingsBreakdownRow × 5 (min_height: 56dp, divider: true)
│   │       ├── Leading: CircleAvatar(initials, 36dp, secondary_container)
│   │       ├── Content: name (bodyLarge) + "Group: KES X · Individual: KES Y" (bodySmall, on_surface_variant)
│   │       └── Trailing: "KES Z" (labelLarge, primary)
│   ├── CorpusReconciliationSection (background: tertiary_container #D2E4FF, corner: 12dp, padding: 16dp, margin: 16dp, mb: 16dp)
│   │   ├── "Corpus Reconciliation" (titleSmall, on_tertiary_container #001C39)
│   │   ├── InfoRow "Opening" / "KES 12,400" (on_tertiary_container)
│   │   ├── InfoRow "Closing" / "KES 12,450" (on_tertiary_container, value: titleMedium)
│   │   └── InfoRow "Net Change" / "KES +50" (value_color: primary #2E7D32)
│   └── FilledButton "Done" (bg: primary, text: on_primary, min-h: 56dp, full-width, margin: 16dp, mb: 24dp)
└── LoadingSkeleton (visible_when: isLoading, 5 shimmer items, height: 80dp, corner: 16dp)
```

### 2.4 PreviousMeetingReviewScreen — Full Component Tree

```
PreviousMeetingReviewScreen
├── TopAppBar (background: surface)
│   ├── NavigationIcon: FluentIcons.arrow_left_24_regular → NavigateBack
│   ├── Title: "Meeting #3" (titleLarge)
│   └── Subtitle: "28 Apr 2026" (bodyMedium, on_surface_variant)
├── ContextBanner (background: primary_container #A6F1A6, ph: 16dp, pv: 10dp)
│   ├── If launchedFrom=conduct: "Reviewing before Meeting #4 — Wed, 7 May 2026" + history icon
│   └── If launchedFrom=calendar: "Completed Meeting — 28 Apr 2026" + checkmark icon
├── LazyColumn
│   ├── UnresolvedAlertCard (visible_when: unresolvedItems.isNotEmpty())
│   │   ├── background: secondary_container #FFDDB3 (warningContainer)
│   │   ├── corner: 12dp; padding: 16dp; margin: 16dp
│   │   ├── Header row: ⚠ icon (20dp, secondary) + "Unresolved Items" (titleSmall)
│   │   └── UnresolvedItemRow × N
│   │       ├── icon per type (money_dismiss / vote / person_alert, 16dp, secondary)
│   │       └── description (bodySmall, on_secondary_container)
│   ├── SummaryMetricsCard (background: primary_container #A6F1A6, corner: 16dp, padding: 20dp, margin: 16dp)
│   │   ├── "Total Collected" (labelLarge)
│   │   ├── "KES 1,850" (headlineLarge 32sp bold)
│   │   ├── Divider
│   │   ├── InfoRow "Closing Corpus" / "KES 12,400"
│   │   ├── InfoRow "Fines Collected" / "KES 150"
│   │   └── InfoRow "Loans Disbursed" / "KES 0"
│   ├── AttendanceSectionHeader "Attendance" (titleSmall, ph: 16dp, pt: 8dp)
│   ├── AttendanceSummaryChips row (ph: 16dp, mb: 8dp)
│   │   └── Chip "5/5 Present" (primary_container)
│   ├── AttendanceDetailRow × 5 (min_height: 56dp, ph: 16dp, pv: 8dp, divider: true)
│   │   ├── Leading: CircleAvatar(initials, 36dp) — primary_container(PRESENT) / secondary_container(LATE) / error_container(ABSENT)
│   │   ├── Content: name (bodyLarge) + optional "Fine: KES X" (bodySmall, error, visible_when: fineAmount > 0)
│   │   └── Trailing: status chip (PRESENT→primary_container; LATE→secondary_container; ABSENT→error_container)
│   ├── SavingsSectionHeader "Savings Per Member" (titleSmall, ph: 16dp, pt: 16dp)
│   ├── MemberSavingsRow × 5 (min_height: 56dp, ph: 16dp, divider: true)
│   │   ├── Leading: CircleAvatar(initials, 36dp, secondary_container)
│   │   ├── Content: name (bodyLarge) + "Group: KES X · Individual: KES Y" (bodySmall, on_surface_variant)
│   │   └── Trailing: "KES Z" (labelLarge, primary #2E7D32)
│   ├── LoansSectionHeader "Loan Activity" (titleSmall, ph: 16dp, pt: 16dp)
│   └── LoanActivityRow × N (min_height: 56dp, ph: 16dp, divider: true)
│       ├── Leading: money icon (24dp, tertiary #1565C0)
│       ├── Content: name (bodyLarge) + "Repaid: KES X · Outstanding: KES Y" (bodySmall, on_surface_variant)
│       └── Trailing: chip "Disbursed KES Z" (primary_container, visible_when: amountDisbursed > 0)
└── StartMeetingCTA (visible_when: launchedFrom == conduct)
    └── FilledButton "Start Meeting #4" (bg: primary, full-width, min-h: 56dp, margin: 16dp)
```

---

## SECTION 3 — Component Specifications

### 3.1 UpcomingMeetingCard

**Component name:** UpcomingMeetingCard
**Usage:** Pinned at top of MeetingCalendarScreen when an upcoming meeting exists.

**Props:**
| Prop | Type | Required |
|------|------|----------|
| meetingNumber | Int | yes |
| meetingDate | String | yes |
| meetingId | String | yes |
| onStartMeeting | (String, Int) -> Unit | yes |

**Visual spec:**
- background: primary_container #A6F1A6
- corner_radius: 16dp
- padding: 16dp (all sides)
- margin: 16dp horizontal, 8dp vertical
- elevation: level_3 (6dp) with tonal tint
- min_height: 140dp
- max_width: screen_width - 32dp

**Content layout:**
```
Column(padding=16dp):
  Text("SCHEDULED MEETING", labelMedium 12sp, on_primary_container #002106, letterSpacing 1.5sp)
  Text("Meeting #4", headlineSmall 24sp, on_primary_container, bold, mt: 4dp)
  Text("Wednesday, 7 May 2026", bodyLarge 16sp, on_primary_container, mt: 2dp)
  Row(mt: 8dp):
    AssistChip("Upcoming", bg: primary #2E7D32, text: on_primary, corner: full)
  FilledButton("Start Meeting", bg: primary, on_primary, full-width, min-h: 48dp, mt: 12dp)
    ← Loading state: CircularProgressIndicator 16dp inside button
```

**Variants:**
- Default: standard green card as above
- Loading: button shows inline CircularProgressIndicator during navigation
- Disabled: button grayed out if insufficient permissions (non-treasurer/non-chairperson)

**Animation:** Card enters with slideInVertically(from=-60dp, duration: 300ms, easing: decelerated)

---

### 3.2 MeetingListItem

**Component name:** MeetingListItem
**Usage:** Each row in the past meetings LazyColumn.

**Props:**
| Prop | Type | Required |
|------|------|----------|
| meetingNumber | Int | yes |
| meetingDate | String | yes |
| meetingId | String | yes |
| attendanceCount | Int | yes |
| totalMemberCount | Int | yes |
| totalCollectedKES | Long | yes |
| status | MeetingStatus | yes |
| onTap | (String, Int) -> Unit | yes |

**Visual spec:**
- min_height: 72dp
- padding_horizontal: 16dp
- padding_vertical: 12dp
- divider: 1dp, outline_variant #C2C9BD, start indent: 72dp (past avatar)
- ripple: on tap, bounded

**Leading badge:**
- Circle avatar, size: 40dp
- Text: "#N" (labelLarge 14sp)
- completed: background primary_container #A6F1A6, text on_primary_container #002106
- missed: background error_container #FFDAD6, text on_error_container #410002

**Content:**
- "Meeting #3" (bodyLarge 16sp, on_surface #1A1C19)
- "28 Apr 2026 · 5/5 present" (bodySmall 12sp, on_surface_variant #424942, mt: 2dp)

**Trailing:**
- "KES 1,850" (labelLarge 14sp, primary #2E7D32)
- Status chip (corner: full, labelSmall 11sp)
  - COMPLETED: background primary_container #A6F1A6, text on_primary_container, text "Completed"
  - MISSED: background error_container #FFDAD6, text on_error_container, text "Missed"

**Variants:**
- Default: as above
- Pressed: ripple_color surface_variant #DEE5DA, scale 0.98 for 100ms
- Focused (accessibility): focus ring 3dp, primary #2E7D32

---

### 3.3 HorizontalStepper (MeetingWizardStepper)

**Component name:** MeetingWizardStepper
**Usage:** Top of MeetingConductScreen. Shows progress through 7 wizard steps.

**Props:**
| Prop | Type | Required |
|------|------|----------|
| currentStep | Int | yes |
| totalSteps | Int (7) | yes |
| stepLabels | List\<String\> | yes |

**Visual spec per step node:**
- step circle size: 28dp
- Active: filled primary #2E7D32, white step number, labelSmall
- Completed: filled primary_container #A6F1A6, checkmark icon 16dp primary
- Inactive: circle with outline_variant #C2C9BD border 1.5dp, outline_variant text
- Label below: labelSmall 11sp
  - Active: primary #2E7D32
  - Completed: on_primary_container
  - Inactive: on_surface_variant #424942

**Connector:**
- Height: 2dp
- Active segment (before current step): primary #2E7D32
- Inactive segment: outline_variant #C2C9BD

**Animation when step advances:**
- Completed circle fills with primary_container (150ms, standard easing)
- Checkmark icon fades in (100ms)
- Next step indicator activates with primary fill (200ms)
- Connector fills left-to-right (250ms, standard easing)

**Interactions:** Non-interactive — tapping past steps does NOT navigate back (wizard state is linear with save-on-advance).

---

### 3.4 CorpusBand

**Component name:** CorpusBand
**Usage:** Persistent horizontal band below stepper, visible on wizard steps 2-6.

**Props:**
| Prop | Type | Required |
|------|------|----------|
| corpusBalance | Long | yes |
| cashOnHand | Long | yes |
| isWarning | Boolean | no (default: false) |

**Visual spec:**
- background: tertiary_container #D2E4FF (normal) / error_container #FFDAD6 (when isWarning=true for step 5 negative corpus)
- height: 40dp
- padding_horizontal: 16dp
- padding_vertical: 8dp
- No corner radius (spans full width between stepper and step content)

**Content (Row, space_between):**
- Left: "Corpus: KES 12,400" (labelLarge 14sp, on_tertiary_container #001C39)
- Right: "Cash on Hand: KES 2,000" (labelMedium 12sp, on_tertiary_container #001C39)

**Warning state (step 5 corpus would go negative):**
- background transitions to error_container #FFDAD6 (200ms crossfade)
- text: "Corpus: KES 0 ⚠ INSUFFICIENT" (on_error_container #410002)

**Animation:** Enters with slideInVertically(from=-32dp, 200ms) when currentStep transitions from 1→2.

---

### 3.5 AttendanceMemberRow

**Component name:** AttendanceMemberRow
**Usage:** Step 1 of wizard — one row per group member for recording attendance.

**Props:**
| Prop | Type | Required |
|------|------|----------|
| member | GroupMember | yes |
| selectedStatus | AttendanceStatus? | yes |
| onStatusChange | (AttendanceStatus) -> Unit | yes |
| fineAmount | Long | no |

**Visual spec:**
- min_height: 64dp
- padding_vertical: 8dp
- divider: 1dp outline_variant, start indent 56dp

**Leading:** CircleAvatar(initials, 40dp, background: secondary_container #FFDDB3, text: on_secondary_container #2A1700)

**Content:**
- member.name (bodyLarge 16sp, on_surface #1A1C19)
- member.role (labelSmall 11sp, primary #2E7D32)

**Trailing:** SegmentedButton, 3 segments
- PRESENT: icon checkmark_16_filled, label "Present"
- LATE: icon clock_16_regular, label "Late"
- ABSENT: icon dismiss_16_regular, label "Absent"

**SegmentedButton visual:**
- min_height: 40dp, 3 segments equal width
- unselected: bg surface, outline 1dp outline_variant, labelSmall on_surface_variant
- selected PRESENT: bg primary_container #A6F1A6, text on_primary_container, border primary
- selected LATE: bg secondary_container #FFDDB3, text on_secondary_container, border secondary
- selected ABSENT: bg error_container #FFDAD6, text on_error_container, border error

**Fine Chip (below row, animated):**
- visible_when: selectedStatus == LATE or ABSENT
- enter: fadeIn + slideInVertically(from=8dp, 150ms)
- exit: fadeOut + slideOutVertically(to=8dp, 100ms)
- LATE: background error_container #FFDAD6, "Fine: KES 50" labelSmall on_error_container
- ABSENT: background error_container #FFDAD6, "Fine: KES 100" labelSmall on_error_container

---

### 3.6 SavingsMemberRow

**Component name:** SavingsMemberRow
**Usage:** Step 3 of wizard — one row per member for entering savings amounts.

**Props:**
| Prop | Type | Required |
|------|------|----------|
| member | GroupMember | yes |
| groupSavingsAmount | Long | yes |
| individualSavingsAmount | Long | yes |
| onGroupSavingsChange | (Long) -> Unit | yes |
| onIndividualSavingsChange | (Long) -> Unit | yes |
| groupSavingsError | String? | no |

**Visual spec:**
- padding_vertical: 12dp
- divider: true, outline_variant

**Layout:**
```
Row:
  CircleAvatar(initials, 40dp, secondary_container)
  Column(flex=1, ml: 12dp):
    Text(member.name, bodyLarge)
    OutlinedTextField("Group Savings (KES)"):
      label: "Group Savings (KES)"
      hint: "Min. 200"
      keyboardType: Number
      prefix: KES
      min_height: 48dp
      error: groupSavingsError
    OutlinedTextField("Individual Savings (KES)"):
      label: "Individual Savings (KES)"
      hint: "Optional"
      keyboardType: Number
      prefix: KES
      min_height: 48dp
      mt: 8dp
```

**Validation feedback:**
- Real-time: error text appears when amount > 0 AND amount < 200 after 300ms debounce
- Error text style: labelSmall, error #D32F2F
- TextField outline color changes to error #D32F2F when error present
- Cursor position preserved on error state

---

### 3.7 LoanApplicationCard

**Component name:** LoanApplicationCard
**Usage:** Step 5 of wizard — one card per pending loan application.

**Props:**
| Prop | Type | Required |
|------|------|----------|
| application | LoanApplication | yes |
| voteRecord | LoanVoteRecord | yes |
| isChairperson | Boolean | yes |
| onVoteFor | () -> Unit | yes |
| onVoteAgainst | () -> Unit | yes |
| onApprove | () -> Unit | yes |
| isCorpusSufficient | Boolean | yes |

**Visual spec:**
- background: surface_variant #DEE5DA
- corner_radius: 12dp
- padding: 16dp
- margin_bottom: 12dp
- Tonal elevation: level_2 (3dp)

**Content:**
```
Column:
  Text(application.memberName, titleSmall 14sp, on_surface)
  Text("Requests KES 1,500", bodyLarge 16sp, on_surface, mt: 4dp)
  Text("Purpose: School fees", bodySmall 12sp, on_surface_variant, mt: 2dp)
  Text("3 For · 1 Against", labelMedium 12sp, outline, mt: 8dp)
  Row(mt: 8dp, gap: 8dp):
    OutlinedButton("For ↑", icon: thumbs_up_16_regular, min-h: 48dp, flex: 1)
      selected: bg primary_container #A6F1A6, border primary, icon primary
    OutlinedButton("Against ↓", icon: thumbs_down_16_regular, min-h: 48dp, ml: 8dp, flex: 1)
      selected: bg error_container #FFDAD6, border error, icon error
  FilledButton("Chairperson Approve", bg: primary, min-h: 48dp, full-width, mt: 8dp)
    enabled_when: isChairperson AND voteRecord.votesFor > voteRecord.votesAgainst AND isCorpusSufficient
    disabled: bg surface_variant, text on_surface_variant (38% opacity)
```

**Corpus gate enforcement:**
- When approve tapped and !isCorpusSufficient: error snackbar "Corpus insufficient for this disbursement — available KES X"
- CorpusGateChip updates in real-time as applications approved

---

### 3.8 ReconciliationCard

**Component name:** ReconciliationCard
**Usage:** Step 6 of wizard — shows full meeting financial reconciliation.

**Props:**
| Prop | Type | Required |
|------|------|----------|
| openingCorpus | Long | yes |
| runningSavingsTotal | Long | yes |
| totalRepayments | Long | yes |
| totalFinesCollected | Long | yes |
| totalLoansDisbursed | Long | yes |
| closingCorpus | Long | yes |

**Visual spec:**
- background: surface_variant #DEE5DA
- corner_radius: 12dp
- padding: 16dp
- margin_bottom: 16dp

**Content (each InfoRow = Row with label + trailing value):**
```
InfoRow("Opening Corpus", "KES 12,400", value_style: bodyLarge)
Divider(1dp, outline_variant, mv: 8dp)
InfoRow("+ Group Savings", "KES 1,000", value_color: primary #2E7D32)
InfoRow("+ Loan Repayments", "KES 500", value_color: primary)
InfoRow("+ Fines Collected", "KES 50", value_color: primary)
InfoRow("— Loans Disbursed", "KES 1,500", value_color: error #D32F2F)
Divider(2dp, on_surface, mv: 8dp)
InfoRow("Closing Corpus", "KES 12,450", label_style: titleSmall, value_style: titleLarge, value_color: primary)
```

**Animation:** closingCorpus value counts up from openingCorpus to final value over 600ms when step 6 first renders (CountingText animation using animateFloatAsState).

---

### 3.9 MetricCard (MeetingSummaryScreen)

**Component name:** MetricCard
**Usage:** 6 instances in 2x3 grid on MeetingSummaryScreen.

**Props:**
| Prop | Type | Required |
|------|------|----------|
| label | String | yes |
| value | String | yes |
| icon | ImageVector | yes |
| iconTint | Color | yes |
| backgroundColor | Color | yes |

**Visual spec:**
- corner_radius: 12dp
- padding: 16dp
- min_height: 80dp

**Layout:**
```
Column:
  Row:
    Icon(icon, 20dp, iconTint)
    Text(label, labelSmall 11sp, on_surface_variant, ml: 4dp, flex: 1)
  Text(value, titleMedium 16sp, on_surface, mt: 8dp, bold)
```

---

## SECTION 4 — Interaction Patterns

### 4.1 Meeting Calendar — State Transitions

**Screen enters composition:**
1. Check SQLDelight cache: if cached data exists → render Content immediately (0ms), kick off background API fetch
2. If no cache → show Loading (skeleton shimmer, 300ms fade-in)
3. API response arrives: if isRefreshing → swap data with 200ms crossfade; update lastSyncAt
4. Error path: if API fails AND cache exists → show content_with_error (orange banner slides down 200ms)
5. Error path: if API fails AND no cache → show Error state (banner fade-in 200ms)

**Upcoming card tap (Start Meeting):**
1. Tap → ripple (100ms) + button loading state (200ms)
2. Navigate to MeetingConductScreen (slide-in from right, 400ms emphasized easing)
3. Screen push adds to back stack

**Past meeting tap:**
1. Tap → ripple (100ms)
2. Navigate to PreviousMeetingReviewScreen with launchedFrom=calendar

**Pull-to-refresh:**
1. Pull down ≥64dp → RefreshIndicator appears (primary #2E7D32 circular spinner)
2. On release → isRefreshing=true → RefreshMeetings action dispatched
3. Online: re-fetch → data swaps in (200ms crossfade) → RefreshIndicator dismisses (150ms)
4. Offline: RefreshIndicator dismisses → snackbar "Cannot refresh — you're offline" (4000ms)

---

### 4.2 Wizard Navigation — Step Advance Flow

**Back button (PreviousStep):**
- Tap → ripple (100ms)
- currentStep decrements immediately
- Step content crossfades (200ms, standard easing)
- Stepper active indicator moves left (250ms)
- Corpus band text may update (100ms crossfade if step moves below 2)
- No validation on back

**Next button (NextStep) — General:**
- Tap → button loading state (50ms)
- Validation runs (synchronous for most steps)
- Validation PASS:
  - currentStep increments
  - Step content crossfades (200ms)
  - Completed step shows checkmark fill (150ms)
  - Active step highlights (200ms)
  - SaveProgressLocally called (async, does not block UI)
- Validation FAIL:
  - Button returns to normal state (100ms)
  - StepValidationErrorSnackbar slides up (300ms, error_container background)
  - Snackbar auto-dismisses after 4000ms or on swipe
  - Current step content shakes (shake animation: 3x translate ±4dp, total 300ms)

**Step 1 Attendance validation:**
- Validate: attendanceMap.size == groupMembers.size (5 == 5)
- Missing members highlighted: pulsing outline_variant ring on unset member rows (500ms pulse cycle)
- Error message: "Please record attendance for all 5 members before proceeding."

**Step 3 Savings validation:**
- Validate: all savingsMap[memberId].groupAmount >= 200
- Violating rows: text field error text appears, outline turns error red
- Error message: "Amina Hassan has not met the minimum contribution of KES 200."

**Step 5 Corpus gate:**
- When ApproveLoanApplication triggered:
  - prospectiveClosing = openingCorpus + runningSavingsTotal + totalRepayments + totalFinesCollected - totalLoansDisbursed - requestedAmount
  - If < 0: block approval, error snackbar "Corpus insufficient for this disbursement — available KES X"
  - CorpusGateChip text updates in real-time as vote totals change

---

### 4.3 Savings Input — Real-time Validation

**Debounce:** 300ms after last keypress before validation triggers
**Min validation (< 200):**
1. TextField outline changes to error #D32F2F (150ms transition)
2. Error text fades in below field: "Below minimum KES 200 required" (labelSmall, error)
3. RunningTotalBand continues updating but shows incomplete icon
4. NextStep button remains enabled — full validation only on tap

**Max validation (> 10000):**
1. Input clamped at 10000 — further digits rejected
2. Toast snackbar: "Maximum KES 10,000 per member per meeting" (2000ms auto-dismiss)

**Running total update:**
1. Any valid amount input → runningSavingsTotal recomputed immediately
2. RunningTotalBand text updates with 100ms crossfade
3. CorpusBand (visible on step 3, step >= 2) also updates to show projected corpus

---

### 4.4 Submit Meeting Flow

**Online submit:**
1. Submit Meeting tapped → isSubmitting=true
2. Footer buttons disabled (opacity 0.38)
3. CircularProgressIndicator (primary #2E7D32, 40dp) fades in centered over step 6 content (200ms)
4. Overlay label: "Submitting meeting..." (bodyMedium, on_surface, mt: 8dp below spinner)
5. Sequential API calls (6 calls):
   - Call 1: POST dt_meeting_record → if 2xx continue; if 5xx → fall to offline path
   - Call 2: POST dt_meeting_attendance × 5 members (batched via Fineract batch API or sequential)
   - Call 3: POST savingsaccounts transactions × 5 members × 1-2 savings types
   - Call 4: POST loans/{id}/transactions?command=repayment per repaid loan
   - Call 5: POST loans/{id}/transactions?command=disburse per approved loan
   - Call 6: PUT dt_group_corpus
6. All 2xx → isSubmitting=false; success toast slides in: "Meeting #4 submitted successfully!" (2000ms)
7. After toast: navigate to MeetingSummaryScreen (slide-in from right, 400ms)

**Offline submit (SyncQueue path):**
1. ConnectivityObserver reports isOffline=true
2. Submit tapped → all 6 payload groups enqueued to SyncQueueRepository with meeting_id key
3. Priority order: corpus update = priority 1; meeting record = priority 2; attendance × 5 = priority 3-7; savings = priority 8-17; repayments = priority 18-N; disbursals = priority N+1
4. Optimistic success: toast "Meeting saved offline — will sync when connected" (3000ms)
5. Navigate to MeetingSummaryScreen with in-memory cached data
6. SyncQueue auto-dequeues when ConnectivityObserver reports isOffline=false

---

### 4.5 Loading States

**Skeleton shimmer animation:**
- Color: gradient from surface_variant #DEE5DA to outline_variant #C2C9BD to surface_variant
- Direction: left-to-right
- Duration: 1200ms per cycle, repeat indefinitely
- Corner radius matches final component (72dp row → 12dp radius skeleton item)

**API error with cached data:**
- ErrorBanner slides down from TopAppBar (300ms, decelerated easing)
- Existing content remains visible and interactive
- "Retry" button triggers RefreshMeetings

**No cache + API error:**
- Full ErrorState rendered (fade-in 200ms)
- Retry button centered, FilledButton #2E7D32

---

### 4.6 PreviousMeetingReview — Context-Aware Banner

**launchedFrom=conduct:**
- Banner text: "Reviewing before Meeting #4 — Wed, 7 May 2026"
- Icon: FluentIcons.history_24_regular (tint: on_primary_container #002106)
- Start Meeting CTA visible at bottom

**launchedFrom=calendar:**
- Banner text: "Completed Meeting — 28 Apr 2026"
- Icon: FluentIcons.checkmark_circle_24_filled (tint: primary #2E7D32)
- No Start Meeting CTA
- Back navigation goes to meeting-calendar

**UnresolvedItemsAlertCard:**
- Slides down below context banner (300ms) when unresolvedItems.isNotEmpty()
- Orange/amber theme (secondary_container background)
- Each unresolved item has icon indicating type:
  - UNPAID_FINE: money_dismiss icon
  - PENDING_LOAN_VOTE: vote icon
  - MISSED_ATTENDANCE: person_alert icon

---

## SECTION 5 — Content Data

### 5.1 Group Identity

- Group name: Mwangaza Women's Group
- Group type: VSLA (Village Savings and Loan Association)
- Location: Nairobi, Kenya
- Currency: KES (Kenya Shilling)
- Cycle: Cycle 1 of 12 months
- Meeting frequency: Weekly (every Wednesday)
- Center ID: 7
- Current meeting number: Meeting #4

### 5.2 Group Members (5 members, Meeting #4)

| ID | Name | Initials | Role | Attendance M#4 | Group Savings | Individual Savings |
|----|------|----------|------|----------------|---------------|--------------------|
| m1 | Amina Hassan | AH | Chairperson | PRESENT | KES 200 | KES 500 |
| m2 | Peter Otieno | PO | Treasurer | PRESENT | KES 200 | KES 0 |
| m3 | Grace Wanjiku | GW | Secretary | LATE (fine KES 50) | KES 200 | KES 50 |
| m4 | John Mwangi | JM | Member | PRESENT | KES 200 | KES 100 |
| m5 | Mary Akinyi | MA | Member | PRESENT | KES 200 | KES 100 |

### 5.3 Meeting #3 (Previous Meeting — shown in step 0 and previous-meeting-review)

- Meeting date: 28 April 2026
- Total savings collected: KES 1,850
- Corpus at close: KES 12,400
- Attendance: 5/5
- Opening corpus (M#3): KES 11,250
- Closing corpus (M#3): KES 12,400
- Fines collected: KES 150 (Grace Wanjiku LATE KES 50, Mary Akinyi ABSENT KES 100)
- Loans disbursed: KES 0
- Loan repayments: KES 500 (Peter Otieno)

### 5.4 Meeting #4 — Computed Reconciliation

- Opening corpus: KES 12,400 (from dt_group_corpus)
- Cash on hand: KES 2,000 (physical cash held by treasurer)
- Group savings collected: KES 1,000 (5 members × KES 200)
- Individual savings collected: KES 750 (Amina KES 500, Grace KES 50, John KES 100, Mary KES 100)
- Total savings: KES 1,750
- Loan repayments: KES 500 (Peter Otieno week 4/12, principal KES 1,500)
- Fines collected: KES 50 (Grace Wanjiku LATE)
- Loans disbursed: KES 1,500 (Grace Wanjiku — school fees, approved 3 For, 1 Against, Amina approved)
- Closing corpus = 12,400 + 1,000 + 500 + 50 - 1,500 = KES 12,450

### 5.5 Active Loans (Step 4 Demo Data)

- Peter Otieno: KES 1,500 principal, KES 875 outstanding, week 4/12 repayments, not overdue, expected weekly KES 125
- (Other members: no active loans)

### 5.6 Pending Loan Applications (Step 5 Demo Data)

- Grace Wanjiku: Requests KES 1,500, purpose "School fees for daughter Zawadi"
  - Votes: 3 For, 1 Against, 0 Abstain
  - Approved by Amina Hassan (Chairperson) after vote majority confirmed
  - Corpus gate check: 12,400 + 1,000 + 500 + 50 - 1,500 = KES 12,450 > 0 — APPROVED

### 5.7 Calendar Meeting History

| # | Date | Status | KES Collected | Attendance |
|---|------|--------|---------------|-----------|
| 4 | 7 May 2026 | UPCOMING | — | — |
| 3 | 28 Apr 2026 | COMPLETED | KES 1,850 | 5/5 |
| 2 | 21 Apr 2026 | COMPLETED | KES 1,200 | 4/5 |
| 1 | 14 Apr 2026 | COMPLETED | KES 900 | 5/5 |

### 5.8 Weekly Trend Data (Group Savings)

| Week | Group KES |
|------|-----------|
| W48 (2025) | KES 1,000 |
| W49 | KES 1,200 |
| W50 | KES 850 |
| W51 | KES 1,500 |
| W52 | KES 1,200 |
| W3 (2026) | KES 1,850 |

### 5.9 Error Messages (from state_model.errors)

- CorpusInsufficient: "Corpus balance insufficient to disburse this loan. Current corpus: KES 14,025."
- AttendanceIncomplete: "Please record attendance for all 5 members before proceeding."
- SavingsValidation: "Savings amount cannot exceed KES 10,000 per member per meeting."
- SubmitFailed: "Meeting submission failed. Data saved offline and will sync when connected."
- MinContributionNotMet: "Grace Wanjiku has not met the minimum contribution of KES 200."
- RepaymentExceedsBalance: "Repayment amount exceeds outstanding balance for Peter Otieno."

### 5.10 i18n Keys Rendered

- step0_title → "Previous Meeting Review"
- step1_title → "Attendance"
- step2_title → "Opening Balance"
- step3_title → "Savings Collection"
- step4_title → "Loan Review"
- step5_title → "Loan Applications"
- step6_title → "Closing Balance"
- submit_meeting → "Submit Meeting"
- submit_success_toast → "Meeting #4 submitted successfully!"
- offline_submit_note → "Offline — data queued for sync"

---

## SECTION 6 — Responsive Rules

### 6.1 Breakpoints

| Name | Range | Typical device |
|------|-------|---------------|
| compact | 0–599dp | Standard Android phones (360dp, 390dp, 412dp) |
| medium | 600–839dp | Foldables (unfolded), small tablets (7") |
| expanded | 840dp+ | Tablets (10"+), large foldables |

### 6.2 Compact (0–599dp) — Primary Target

This is the primary design target for MifosSave. Rural East Africa predominantly uses mid-range Android phones (Samsung A-series, Tecno, Infinix) with 360–412dp width.

**MeetingCalendarScreen (compact):**
- UpcomingMeetingCard: full-width minus 32dp margins
- MeetingListItem: full-width, 72dp height, 16dp horizontal padding
- BottomNavigation: visible, 56dp height, 4 tabs
- ViewToggle icon: visible in TopAppBar actions
- No calendar grid view on compact — list view only (CALENDAR mode shows same list)

**MeetingConductScreen (compact):**
- StepperHeader: 7 steps squeezed to 28dp circles with abbreviated labels (3 chars max)
- Step labels hidden on compact if they overflow — show only active step label below stepper
- StepContent: full-width, 16dp padding
- NavigationFooter: full-width, back + next buttons side by side (50/50 split)
- Keyboard: step content scrolls up on keyboard appear to keep input visible (WindowInsetsCompat)
- SavingsMemberRow: two TextFields stacked vertically (not side by side)

**MeetingSummaryScreen (compact):**
- MetricGrid: 2 columns, gap 12dp — no change
- HeroCard: full-width minus 32dp
- SavingsBreakdown: full-width rows

**PreviousMeetingReviewScreen (compact):**
- ContextBanner: full-width
- All sections: full-width with 16dp horizontal padding
- UnresolvedAlertCard: full-width minus 32dp margin

### 6.3 Medium (600–839dp) — Foldable / Small Tablet

**MeetingCalendarScreen (medium):**
- BottomNavigation: replaces with NavigationRail (72dp left rail, icon + label vertical)
- UpcomingMeetingCard: constrained to max 560dp width, centered
- MeetingListItem: constrained max 560dp, centered
- ViewToggle: enables true calendar grid view (month view with meeting dots)

**MeetingConductScreen (medium):**
- StepperHeader: full labels visible (no abbreviation)
- StepContent: max width 560dp, centered horizontally with 20dp padding on each side
- NavigationFooter: max width 560dp, centered
- CorpusBand: full-width (extends edge to edge)
- SavingsMemberRow: two TextFields side by side (group savings left, individual right)

**MeetingSummaryScreen (medium):**
- MetricGrid: 3 columns (3x2 instead of 2x3)
- HeroCard: max width 560dp, centered
- SavingsBreakdown: full width still, list format

**PreviousMeetingReviewScreen (medium):**
- Summary card + attendance section: may show side-by-side in a 2-column layout
- Max content width: 560dp, centered

### 6.4 Expanded (840dp+) — Tablet / Large Foldable

**MeetingCalendarScreen (expanded):**
- NavigationRail → NavigationDrawer (permanent, 240dp, pinned left)
- Content area: screen_width - 240dp (navigation drawer)
- 2-column layout: left column shows calendar month view; right column shows meeting detail preview
- UpcomingMeetingCard: left column top, max 440dp
- MeetingListItem: left column scrollable list, max 440dp
- Right panel: detail preview auto-opens when a meeting is selected (replaces navigation to new screen)

**MeetingConductScreen (expanded):**
- 2-panel layout: left panel (step list/progress) 300dp + right panel (step content, remaining width)
- Left panel: vertical step list replaces horizontal stepper; each step shows full title + completion state
- CorpusBand: spans top of right panel only
- NavigationFooter: bottom of right panel only
- SavingsMemberRow: group savings + individual savings in a 2-column row layout side by side
- AttendanceMemberRow: avatar + name in 180dp left; segmented button in remaining right space
- LoanApplicationCard: 2 cards per row (max 460dp each card)

**MeetingSummaryScreen (expanded):**
- Left panel: HeroCard + Corpus Reconciliation (320dp)
- Right panel: MetricGrid (2x3) + SavingsBreakdown + Done button
- MetricGrid: 2 columns within right panel (unchanged from compact)
- Share button: always visible in right panel top

**PreviousMeetingReviewScreen (expanded):**
- 2-column layout: left = Summary + Corpus card; right = Attendance + Savings + Loans
- Start Meeting CTA (if launchedFrom=conduct): bottom of right panel
- UnresolvedAlert: spans top of right panel

### 6.5 Font Scaling

- System font scale respected: all sp units scale with system font size preference
- Min readable size enforced: bodySmall 12sp × 0.85 scale = 10.2sp (acceptable for secondary labels)
- Large text mode (Android accessibility): all labelSmall items scale to minimum 14sp effective
- No hardcoded dp for text; all text uses sp exclusively

### 6.6 Orientation

**Portrait (primary):**
- All designs above are for portrait orientation
- Wizard steps: NavigationFooter at bottom, full-width

**Landscape (compact width in landscape = medium breakpoint behavior):**
- MeetingConductScreen in landscape on a phone: max content width = min(screen_height, 560dp), horizontally centered
- StepContent gains extra vertical space from lack of bottom navigation
- TextFields in SavingsStep: 3-column layout in landscape (avatar + group savings + individual savings)
- NavigationFooter: remains at bottom, height 56dp in landscape

### 6.7 Safe Areas and System Insets

- Status bar: transparent, content drawn behind using edgeToEdge
- Navigation bar (gesture/button): NavigationFooter padding_bottom = max(16dp, WindowInsets.navigationBars.bottom)
- Keyboard: step content area uses imePadding() to scroll above keyboard when TextFields are active
- Notch / cutout: TopAppBar respects WindowInsets.statusBars.top

### 6.8 RTL Support

- All layouts use start/end instead of left/right
- Stepper: steps flow right-to-left in RTL locales (Arabic, future support)
- InfoRow label: start-aligned, value: end-aligned (same in both LTR and RTL)
- Icons: FluentIcons that are directional (arrow_left) are mirrored in RTL via autoMirrored
- Avatar initials: single character from start of name (locale-aware)
