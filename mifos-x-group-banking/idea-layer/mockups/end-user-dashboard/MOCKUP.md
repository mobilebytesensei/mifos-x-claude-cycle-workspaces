# End-User Dashboard — Mockup Spec

## Design Language

CommonPurse uses Material Design 3 with VSLA-specific brand tokens. The end-user surface is warm and encouraging — members see their savings grow and have clear pathways to request loans. All text is large for readability in outdoor rural settings. Touch targets meet 48dp minimum across all interactive elements.

**Primary brand colours**:
- Primary: #2E7D32 (VSLA-green — growth, community)
- Secondary: #FF8F00 (amber — harvest, shared wealth)
- Tertiary: #1565C0 (trust-blue — loan information)
- Error: #D32F2F (overdue, warnings)

**Typography**: Noto Sans, large scale. displaySmall 36sp for balance figures.

**Shapes**: sm=8dp, md=12dp, lg=16dp, full=9999dp.

**Elevation**: Cards at level_2 (3dp), FAB at level_5 (12dp).

---

## Screen-by-Screen

### PersonalDashboardScreen

**Layout**: Scaffold — green top bar (primary) + LazyColumn body + bottom navigation bar.

**States**:
- `loading` — shimmer shown for all 4 card slots; group banner visible
- `content` — all cards rendered; pull-to-refresh available
- `refreshing` — content visible + pull indicator at top
- `error` — error state with Retry button
- `empty` — no accounts (new member); only Request Loan CTA visible

**Components**:

| Component | Type | Style Summary | Interaction |
|-----------|------|--------------|-------------|
| DashboardTopBar | TopBar | Background primary (#2E7D32), elevation 0dp. Custom title: time-of-day greeting + "Grace". Trailing: FluentIcons.alert_24_regular notification bell, badge for unread. | Tap notification bell → notifications screen |
| GroupBanner | Card | Background primary (#2E7D32), padding 16dp top/24dp horizontal/24dp bottom, elevation 0dp. Group name "Mwangaza Women's Group" bodyLarge semibold onPrimary. Currency chip "KES" primaryContainer fill, onPrimaryContainer text, cornerRadius full. | Non-interactive |
| SavingsSummaryCard | Card | Background surface, cornerRadius lg (16dp), elevation 3dp, padding 20dp, margin 16dp horizontal, margin_top -20dp (overlaps group banner). Icon savings_24_filled primary. Balance "KES 12,450" displaySmall bold. Breakdown row: group-linked "KES 9,600" primary, individual "KES 2,850" secondary. Trailing chevron-right. | Tap → OnSavingsCardClick → personal-savings |
| LoanSummaryCard | Card | Visible when activeLoan != null. Background surface, cornerRadius lg (16dp), elevation 3dp, padding 20dp, margin 16dp horizontal, margin_top 12dp. Icon money_24_filled tertiary. Outstanding "KES 15,000" headlineSmall. Next repayment row: "KES 1,500 · 15 May 2026". Overdue indicator: warning_24_filled error when isOverdue. | Tap → OnLoanCardClick → personal-loans |
| RequestLoanCta | Card | Visible when activeLoan == null. Background tertiaryContainer (#D2E4FF), cornerRadius lg (16dp), elevation 0dp, padding 20dp, margin 16dp horizontal, margin_top 12dp. Icon add_circle_24_filled 40dp onTertiaryContainer. Title "Need a loan?" titleMedium. Subtitle "Apply for up to KES 37,350 (3× your savings)" bodyMedium. | Tap → OnRequestLoanClick → loan-request |
| ShareOutProjectionCard | Card | Background secondaryContainer (#FFDDB3), cornerRadius lg (16dp), elevation 0dp, padding 16dp, margin 16dp horizontal, margin_top 12dp. Icon trophy_24_filled onSecondaryContainer. Label "Projected share-out" labelLarge. Amount "KES 38,250" headlineSmall bold onSecondaryContainer. | Non-interactive |
| RecentActivityHeader | Text | "Recent Activity" titleMedium semibold onSurface, margin 16dp horizontal, margin_top 24dp, margin_bottom 8dp | Non-interactive |
| RecentActivityListItem | ListItem (repeating) | Leading icon: arrow_download (deposit) primary or arrow_upload (withdrawal) error, 24dp. Amount bodyLarge semibold (primary for deposit, error for withdrawal). Type label bodyMedium onSurfaceVariant. Date labelMedium outline. Divider between items. minTouchTarget 48dp. | Non-interactive |
| DashboardShimmer | Shimmer | Visible when isLoading=true. 4 shimmer cards, each height 100dp, cornerRadius lg, margin 16dp, spacing 8dp | Non-interactive |
| DashboardErrorState | EmptyState | Visible when error != null && !isLoading. Icon wifi_off_24_filled 64dp onSurfaceVariant. Title "Could not load dashboard". Subtitle "Check your internet connection and try again." Button "Try Again" primary. | Tap → OnRetry |
| PullToRefresh | SwipeRefresh | Color primary (#2E7D32). Shown when isRefreshing=true. | Swipe down → OnRefresh |

---

### PersonalSavingsScreen

**Layout**: Scaffold — green top bar + TabRow + LazyColumn per tab.

**States**:
- `loading` — shimmer for 6 items
- `content` — balance hero + contribution progress + transaction list
- `error` — error state with retry

**Components**:

| Component | Type | Style Summary | Interaction |
|-----------|------|--------------|-------------|
| SavingsTopBar | TopBar | Background primary (#2E7D32), elevation 0dp. Back arrow onPrimary. Title "My Savings" titleLarge onPrimary. | Tap back → personal-dashboard |
| SavingsTabRow | Chip row | Background primaryContainer (#A6F1A6), horizontal padding 16dp, vertical 12dp. Selected: primary fill, onPrimary text, cornerRadius full. Unselected: primaryContainer fill, onPrimaryContainer text. Tab 1: people_community icon + "Group-linked". Tab 2: person_circle icon + "Individual" (hidden when no individual account). | Tap → OnTabSelected |
| BalanceHeroCard | Card | Background primary (#2E7D32), cornerRadius lg (16dp), padding 24dp, margin 16dp horizontal, elevation 0dp. Label "Group-Linked Savings" / "Individual Savings" labelLarge onPrimary 0.8 opacity. Amount "KES 9,600" displaySmall bold Noto Sans onPrimary. Account number "Acc: 000100012345" labelMedium onPrimary 0.7 opacity. | Non-interactive |
| ContributionProgressCard | Card | Visible on GROUP_LINKED tab. Background surface, cornerRadius lg (16dp), elevation 3dp, padding 16dp, margin 16dp horizontal. Icon calendar_checkmark_24_filled primary. Label "Contribution Progress" labelLarge onSurfaceVariant. Progress bar: "18 / 24 meetings" label, LinearProgressIndicator fraction 0.75, height 8dp, color primary, track primaryContainer, cornerRadius full. Contribution row: "KES 100 min · KES 500 max · This cycle: KES 9,600" bodySmall onSurfaceVariant. | Non-interactive |
| TransactionsHeader | Text | "Transaction History" titleMedium semibold onSurface, margin 16dp horizontal. | Non-interactive |
| SavingsTransactionListItem | ListItem (repeating) | Leading: circular icon container 40dp surfaceVariant, trending_up (deposit) primary or trending_down (withdrawal) error. Title "Deposit" / "Withdrawal" / "Meeting contribution" bodyLarge onSurface. Subtitle date "15 Apr 2026" bodySmall onSurfaceVariant. Trailing: amount "+KES 500" bodyLarge semibold (primary/error). Running balance "Balance: KES 9,600" labelSmall outline. Divider between items. | Non-interactive |
| EmptyIndividualPromo | EmptyState | Visible when selectedTab==INDIVIDUAL && individualSavingsId==null. Icon piggy_bank_24_filled 64dp secondary. Background secondaryContainer. Title "No individual savings yet". Subtitle "Speak to your group treasurer to open an individual savings account." | Non-interactive |
| SavingsShimmer | Shimmer | 6 items, height 56dp each, cornerRadius md, margin 16dp. | Non-interactive |
| SavingsErrorState | EmptyState | Icon wifi_off_24_filled 64dp. Title "Could not load savings". Button "Try Again" primary. | Tap → OnRetry |

---

### PersonalLoansScreen

**Layout**: Scaffold — green top bar + LazyColumn + FAB (amber).

**States**:
- `loading` — 3 shimmer cards
- `content` — loan list + FAB
- `empty` — empty state + CTA button
- `error` — error state + retry

**Components**:

| Component | Type | Style Summary | Interaction |
|-----------|------|--------------|-------------|
| LoansTopBar | TopBar | Background primary (#2E7D32), elevation 0dp. Back arrow onPrimary. Title "My Loans" titleLarge onPrimary. | Tap back → personal-dashboard |
| LoanStatusFilterChips | Chip row | Horizontal scroll. Selected: primary fill, onPrimary text, cornerRadius full. Unselected: surface fill, onSurface text, outline border 1dp. Chips: "All", "Active", "Closed". Padding 6dp × 14dp, spacing 8dp, margin 16dp horizontal. | Tap chip → OnFilterChange |
| LoanCard (collapsed) | Card | Background surface, cornerRadius lg (16dp), elevation 3dp, padding 16dp, margin 16dp horizontal, margin_bottom 12dp. Header row: product name titleMedium semibold onSurface + account number labelSmall onSurfaceVariant + status chip (Active: primaryContainer; Pending: secondaryContainer; Closed: surfaceVariant; Overdue: errorContainer). Balance row: "Outstanding" labelMedium onSurfaceVariant + amount headlineSmall bold. Next repayment row (active only): amount + due date; warning_24_filled error when overdue. Trailing chevron_down. | Tap → OnLoanExpand(loanId) |
| LoanCard (expanded) | Card | Same as collapsed + repayment schedule section below divider. "Repayment Schedule" labelLarge onSurfaceVariant. Per-period rows: period "#1", due date "15 Apr 2026", amount "KES 1,500", status icon (checkmark_circle paid primary / circle_regular pending / dismiss_circle_filled overdue error). | Tap → OnLoanExpand (collapses) |
| RequestLoanFab | FAB (extended) | Background secondary (#FF8F00), icon add_24_filled onSecondary, text "Request Loan" onSecondary, cornerRadius full, min_touch_target 56dp, elevation 12dp. Visible when loans.isNotEmpty(). | Tap → OnRequestLoanClick → loan-request |
| LoansEmptyState | EmptyState | Icon money_24_regular 64dp onSurfaceVariant. Title "No loans yet". Subtitle "Apply for a loan of up to 3× your savings balance." Button "Request a Loan" primary fill, onPrimary text. | Tap → OnRequestLoanClick |
| LoansShimmer | Shimmer | 3 cards, height 120dp each, cornerRadius lg, margin 16dp, spacing 12dp. | Non-interactive |
| LoansErrorState | EmptyState | Icon wifi_off_24_filled 64dp onSurfaceVariant. Title "Could not load loans". Button "Try Again" primary. | Tap → OnRetry |

---

### LoanRequestScreen

**Layout**: Scaffold — green top bar + scrollable Column + bottom submit bar area.

**States**:
- `content` — form ready; submit disabled until valid
- `submitting` — fields disabled; spinner shown
- `submit_success` — success dialog overlay
- `submit_error` — error snackbar at bottom
- `offline_queued` — offline banner + success dialog with offline copy

**Components**:

| Component | Type | Style Summary | Interaction |
|-----------|------|--------------|-------------|
| LoanRequestTopBar | TopBar | Background primary (#2E7D32), elevation 0dp. Back arrow onPrimary. Title "Request a Loan" titleLarge onPrimary. | Tap back → personal-loans |
| OfflineModeBanner | Card | Visible when isOfflineMode=true. Background secondaryContainer (#FFDDB3), cornerRadius sm (8dp), padding 8dp × 16dp, margin 16dp horizontal, margin_top 8dp. Icon wifi_off_24_filled 20dp onSecondaryContainer. Text "You are offline. Your request will be saved and sent when you reconnect." bodySmall onSecondaryContainer. live_region polite. | Non-interactive |
| SavingsLimitCard | Card | Background tertiaryContainer (#D2E4FF), cornerRadius lg (16dp), padding 16dp, margin 16dp horizontal, margin_top 12dp, elevation 0dp. Row 1: savings_24_filled onTertiaryContainer + "Your savings balance" labelMedium + "KES 12,450" bodyLarge onTertiaryContainer. Row 2: money_24_filled + "Maximum you can borrow" labelMedium + "KES 37,350" titleMedium bold + "(3× your savings)" bodySmall. | Non-interactive |
| LoanAmountField | OutlinedTextField | Label "Loan Amount (KES)", prefix "KES", placeholder "0", leading icon money_24_regular, keyboard number, IME next, margin 16dp horizontal, margin_top 16dp. Error text from requestedAmountError. Supporting text "Enter amount between KES 500 and your maximum". | Type → OnAmountChange |
| LoanPurposeDropdown | ExposedDropdown | Label "Loan Purpose", leading icon notepad_24_regular, trailing chevron_down, margin 16dp horizontal, margin_top 12dp. Options: School Fees, Medical Emergency, Business, Farming / Agriculture, Home Improvement, Emergency, Other. Error text from purposeError. | Select → OnPurposeSelected |
| DurationSelector | Card | Background surface, cornerRadius md (12dp), padding 16dp, margin 16dp horizontal, margin_top 12dp, elevation 1dp. Header "Repayment Duration" labelLarge onSurfaceVariant. Selected duration "12 weeks" titleLarge bold onSurface. Slider: range 4–52 weeks, 12 steps, active primary, inactive primaryContainer, thumb primary. Weekly repayment row: "Weekly repayment estimate" + "KES 3,223" bodyLarge tertiary semibold. | Slide → OnDurationChanged |
| RepaymentSummaryCard | Card | Visible when requestedAmount non-blank + no amount error. Background surfaceVariant (#DEE5DA), cornerRadius md (12dp), padding 16dp, margin 16dp horizontal, margin_top 12dp. Rows: "Principal" KES X, "Interest (group rate)" KES Y, divider, "Total to repay" KES Z titleMedium bold. | Non-interactive |
| SubmitButton | FilledButton | Text "Submit Application", background primary (#2E7D32), text onPrimary, cornerRadius full, min_height 56dp, margin 16dp horizontal, margin_top 24dp, margin_bottom 24dp. Disabled when !isFormValid or isSubmitting. | Tap → OnSubmitClick |
| SubmittingIndicator | CircularProgressIndicator | Visible when isSubmitting=true. Size 32dp, primary colour, centred, margin_top 24dp. | Non-interactive |
| SubmitSuccessDialog | AlertDialog | Icon checkmark_circle_24_filled 48dp primary. Title "Request Submitted!" (online) or "Request Saved!" (offline). Body text describing next steps. Button "OK" primary fill cornerRadius full. cornerRadius lg. | Tap OK → OnSuccessDialogDismiss → personal-dashboard |
| SubmitErrorSnackbar | Snackbar | Background errorContainer (#FFDAD6), text onErrorContainer. Action "Retry" tertiary (#1565C0). Duration 5000ms. Visible when submitError != null && !isSubmitting. | Tap Retry → OnRetry |

---

## Interaction Patterns

**Pull-to-refresh (PersonalDashboardScreen)**:
1. User swipes down from top of LazyColumn
2. SwipeRefresh indicator appears (colour primary, 36dp spinner)
3. `OnRefresh` dispatched; `isRefreshing = true`
4. Parallel API calls: get_client_accounts + get_savings_account
5. On completion: `isRefreshing = false`; cards update with fresh data
6. Indicator animates out (fade 150ms)

**Savings card tap**:
1. Tap on SavingsSummaryCard
2. Card pressed ripple (on_surface at 12%, 200ms)
3. `OnSavingsCardClick` dispatched
4. `NavigateToSavings` event emitted
5. Horizontal shared-axis navigation to PersonalSavingsScreen (300ms medium_2)
6. Nav params: clientId, groupLinkedSavingsId, individualSavingsId?

**Loan card expand/collapse**:
1. User taps LoanCard
2. `OnLoanExpand(loanId)` dispatched
3. If selectedLoanId == loanId: collapse (set selectedLoanId = null)
4. If selectedLoanId != loanId: expand (set selectedLoanId = loanId; collapse previous if any)
5. Expand animation: AnimatedVisibility with expandVertically (duration 300ms medium_2, decelerated easing)
6. Chevron rotates: 0° → 180° (expand), 180° → 0° (collapse) over 200ms

**Loan request form validation**:
- Amount field: validates on each character change
  - empty: no error shown
  - non-numeric: requestedAmountError = "Please enter a valid amount"
  - ≤ 0: requestedAmountError = "Amount must be greater than KES 0"
  - > maxLoanAmount: requestedAmountError = "Maximum loan is KES {maxLoanAmount}"
  - valid: error cleared; repaymentEstimate recalculates
- Purpose dropdown: purposeError shown only if user taps Submit without selecting
- Duration slider: always valid (starts at default 12 weeks)
- isFormValid: requestedAmount valid + purpose selected + durationWeeks > 0

**Offline loan request submission**:
1. `isOfflineMode = true` on form entry (ConnectivityManager check)
2. OfflineModeBanner shown (slide-in from top, 200ms)
3. User fills form and taps Submit
4. `OnSubmitClick` dispatched
5. ConnectivityManager.isOnline() = false → offline branch
6. SyncQueueRepository.enqueue(LoanRequestPayload) called
7. `successDialogVisible = true` with offline copy
8. Dialog: "Request Saved! Your loan request has been saved and will be submitted automatically when you reconnect."
9. User taps OK → navigate to personal-dashboard

---

## Accessibility

**WCAG AA compliance (key checks)**:
- primary (#2E7D32) on surface (#FAFAFA): 5.54:1 — AA passes
- onPrimary (#FFFFFF) on primary (#2E7D32): 13.5:1 — AAA
- onSecondaryContainer (#2A1700) on secondaryContainer (#FFDDB3): 8.4:1 — AAA
- onTertiaryContainer (#001C39) on tertiaryContainer (#D2E4FF): 9.1:1 — AAA
- error (#D32F2F) on surface (#FAFAFA): 5.91:1 — AAA

**Touch targets**:
- All list items: minTouchTarget 48dp height
- FAB: 56dp minimum (extended FAB is naturally tall)
- Filter chips: 36dp touch target with 6dp outer padding = 48dp total
- Slider thumb: 48dp touch target

**Screen reader support**:
- SavingsSummaryCard contentDescription: "Total savings KES 12,450. Group-linked KES 9,600, Individual KES 2,850. Tap to see details."
- LoanSummaryCard contentDescription: "Active loan — KES 15,000 outstanding. Next repayment KES 1,500 on 15 May 2026. Tap to see schedule."
- RequestLoanCta contentDescription: "Request a loan — tap to apply"
- RecentActivityListItem: "Deposit KES 500 on 15 Apr 2026"
- LoanCard contentDescription: "Loan {productName} — outstanding KES {amount}. Status: {Active/Closed/Overdue}. Tap to expand repayment schedule."

**Focus order (PersonalDashboardScreen)**:
TopBar greeting → notification bell → SavingsSummaryCard → LoanSummaryCard or RequestLoanCta → ShareOutProjectionCard → RecentActivityListItem (repeated)

**OfflineModeBanner**: live_region = "polite" — announces "You are offline" to screen reader when banner appears.

**SuccessDialog**: focus trapped within dialog when visible. First focus: title. Confirm button is last focusable element.
