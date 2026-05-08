# Share-Out — Prompts Stitch
**Feature**: share-out | **Project**: CommonPurse (mifos-x-group-banking)
**Screens**: share-out-preview, share-out-execute

---

## 1. Design System Context

### Brand Identity and Color Philosophy
CommonPurse is designed for VSLA groups in East/West Africa and South Asia. Share-out is the most celebratory financial event — distributing the year's accumulated savings and profits back to members. The visual language for this feature must balance celebration (completion banner uses primary green) with caution (execute button uses error red to signal irreversibility).

### Full Color Token Reference

**Primary Palette (VSLA Green)**
- primary: `#2E7D32` — 5.83:1 contrast ratio on white (WCAG AAA for normal text)
- on_primary: `#FFFFFF` — white text/icons on green surfaces
- primary_container: `#A6F1A6` — light mint green; summary cards, completion banners
- on_primary_container: `#002106` — near-black green; text on mint surfaces

**Secondary Palette (Amber / Shared Coin)**
- secondary: `#FF8F00` — warm amber; IN_PROGRESS spinner color, sync indicators
- on_secondary: `#FFFFFF`
- secondary_container: `#FFDDB3` — peach; member avatar backgrounds, queued banner
- on_secondary_container: `#2A1700`

**Tertiary Palette (Trust Blue)**
- tertiary: `#1565C0` — deep blue; formula chip, informational elements
- on_tertiary: `#FFFFFF`
- tertiary_container: `#D2E4FF` — sky blue; formula info chip background
- on_tertiary_container: `#001C39`

**Error Palette (Critical Red)**
- error: `#D32F2F` — execute button background (signals irreversible action)
- on_error: `#FFFFFF`
- error_container: `#FFDAD6` — light pink; error snackbar, failed payout row tint
- on_error_container: `#410002`

**Surface Palette**
- background: `#FFFFFF`
- surface: `#FAFAFA` — card backgrounds
- surface_variant: `#DEE5DA` — shimmer skeletons, dividers
- on_surface: `#1A1C19`
- on_surface_variant: `#424942`
- outline: `#727971`

**Warning Colors (custom, not MD3 role)**
- warning_container: `#FFF9C4` — offline banner, partial failure banner
- on_warning_container: `#E65100`

### Typography Scale for Share-Out Screens

| Style | sp | Weight | Line-Height | Used In |
|-------|-----|--------|-------------|---------|
| displaySmall | 36 | 400 | 44 | Not used in share-out |
| headlineSmall | 24 | 400 | 32 | Total pool amount (KES 24,000) in summary card |
| titleLarge | 22 | 500 | 28 | "Share-Out Complete!" completion title |
| titleMedium | 16 | 500 | 24 | "Cycle 1 — Distribution Preview", "Confirm Share-Out" |
| titleSmall | 14 | 500 | 20 | "Member Payouts" section header, table headers |
| bodyLarge | 16 | 400 | 24 | KES amounts in fund summary card rows |
| bodyMedium | 14 | 400 | 20 | "5 members to receive payouts", completion body text |
| bodySmall | 12 | 400 | 16 | "All calculations are preliminary", instructions text |
| labelLarge | 14 | 500 | 20 | Member name in payout row, payout amount |
| labelMedium | 12 | 500 | 16 | Share percentage in payout row "(28%)" |
| labelSmall | 11 | 500 | 16 | Table column headers, status indicator labels |

### Spacing Scale
- xs: 4dp | sm: 8dp | md: 12dp | lg: 16dp | xl: 24dp | xxl: 32dp
- Card internal padding: 16dp (standard), 20dp (summary card — more prominent)
- Card external margin: 16dp left/right, 8dp bottom
- Row gap between member payout items: 0dp (divider separates)
- Gap between major sections: 12dp

### Shape Tokens
- Cards: `shape.medium` = 12dp corner radius
- Buttons: `shape.full` = 24dp (primary/outlined) to 9999dp (pill)
- TextFields: `shape.small` = 8dp
- Info chips: `shape.full` = 9999dp (fully rounded)
- Badges in table: `shape.extra_small` = 4dp

### Elevation Tokens
- Summary card (primaryContainer): elevation 0dp — floats on background via color contrast alone
- Fund summary card (surface): elevation 3dp (level_2)
- Confirmation section card: elevation 3dp (level_2)
- Completion banner: elevation 0dp (color-only distinction)
- Execute button: elevation 12dp (level_5 — FAB-like prominence)

### Motion Timing for Share-Out Feature
- Confirmation text → button enable: `animateColorAsState`, 200ms, standard easing
- ExecuteButton disabled→enabled color transition: 150ms, standard easing
- Progress bar fill: 300ms per step, `animateFloatAsState`, standard easing
- Status icon transitions (PENDING→IN_PROGRESS→DONE): 200ms crossfade per status
- IN_PROGRESS spinner: continuous rotation 1000ms/revolution
- Completion banner appearance: `AnimatedVisibility(fadeIn+slideIn, 400ms, decelerated easing)`
- Member row status icon: scale 0→1 with 150ms bounce on DONE state
- Offline banner: `AnimatedVisibility(expandVertically, 250ms)` when isOnline changes

### Accessibility Specifications
- Execute button content description changes based on confirmation state:
  - Unconfirmed: "Execute Share-Out — confirm first by typing SHARE OUT"
  - Confirmed: "Execute share-out — distributes KES 24,000 to 5 members. This cannot be undone."
- All member payout rows: content description includes execution status
- Progress bar: `role=progressbar`, value=executedCount/totalCount, label="1 of 5 payouts completed"
- Biometric button: "Authenticate with fingerprint or face ID to confirm share-out"
- Completion banner: "Share-out complete — KES 24,000 distributed to 5 members successfully"
- Status icons have text alternatives: DONE="Completed", FAILED="Failed", IN_PROGRESS="Processing", QUEUED="Queued for sync"

---

## 2. Screen Layouts

### Screen: Share-Out Preview

**Route**: `/groups/{groupId}/share-out/preview`
**Entry**: From group-dashboard Share-Out button (when isCycleEnd=true)

```
Scaffold
  TopAppBar (56dp)
    background: #2E7D32
    title: "Share-Out Preview" — titleLarge, #FFFFFF
    navigationIcon: arrow_back (48dp touch)
    action: refresh IconButton (48dp touch)

  LazyColumn (padding: 16dp, gap: 12dp)

    # Cycle Info Banner
    Card (background: #A6F1A6, cornerRadius: 12dp, padding: 16dp, elevation: 0dp)
      Text "Cycle 1 — Distribution Preview"
        style: titleMedium — 16sp/500, #002106 (onPrimaryContainer)
      Text "All calculations are preliminary. Confirm to proceed."
        style: bodySmall — 12sp, #002106
        marginTop: 4dp

    # Fund Summary Card
    Card (background: #FAFAFA, elevation: 3dp, cornerRadius: 12dp, padding: 16dp)
      LabeledValueRow
        label: "Total Corpus (Fund)" — bodyMedium, #424942
        value: "KES 20,000" — bodyLarge, #1A1C19 (onSurface)
        layout: Row, spaceBetween, height: 40dp

      LabeledValueRow (marginTop: 8dp)
        label: "Total Profit (Interest Earned)" — bodyMedium, #424942
        value: "KES 4,000" — bodyLarge, #2E7D32 (primary color for profit emphasis)

      Divider (height: 1dp, color: #C2C9BD, margin: 8dp 0dp)

      LabeledValueRow (marginTop: 8dp)
        label: "Total Distribution Pool" — titleMedium, #1A1C19
        value: "KES 24,000" — titleLarge, #2E7D32, fontWeight: 700
        height: 48dp

    # Formula Chip
    Row (padding: 0dp, startAlign)
      AssistChip
        background: #D2E4FF (tertiaryContainer)
        text: "Formula: Pro-rata by savings contribution"
        textStyle: labelMedium, #001C39 (onTertiaryContainer)
        cornerRadius: 9999dp
        padding: 6dp 12dp

    # Distribution Table
    Card (background: #FAFAFA, cornerRadius: 12dp, padding: 0dp, elevation: 3dp)
      # Table Header
      Row (height: 40dp, background: #DEE5DA, padding: 0dp 16dp)
        Text "Member" — labelSmall, #424942, weight: 1 (fill)
        Text "Total Savings" — labelSmall, #424942, width: 96dp, textAlign: end
        Text "Share %" — labelSmall, #424942, width: 56dp, textAlign: end
        Text "Payout (KES)" — labelSmall, #424942, width: 96dp, textAlign: end

      # Table Rows (data rows)
      # Row 1 — Highest payout (highlighted)
      Row (height: 48dp, background: #E8F5E9, padding: 0dp 16dp)
        Text "Amara Diallo" — bodyMedium, #1B5E20, weight: 1
        Text "6,800" — bodyMedium, #1B5E20, width: 96dp, textAlign: end
        Text "28.3%" — bodyMedium, #1B5E20, width: 56dp, textAlign: end
        Text "6,792" — bodyMedium, #1B5E20, width: 96dp, textAlign: end

      Divider (1dp, #C2C9BD)

      # Row 2
      Row (height: 48dp, background: #FAFAFA, padding: 0dp 16dp)
        Text "Grace Mwangi" — bodyMedium, #1A1C19, weight: 1
        Text "5,200" — bodyMedium, #424942, width: 96dp, textAlign: end
        Text "21.7%" — bodyMedium, #424942, width: 56dp, textAlign: end
        Text "5,208" — bodyMedium, #2E7D32, width: 96dp, textAlign: end

      Divider (1dp)

      # Row 3
      Row (height: 48dp, background: #FAFAFA, padding: 0dp 16dp)
        Text "Fatima Ouedraogo" — bodyMedium, #1A1C19, weight: 1
        Text "4,800" — weight: 96dp, textAlign: end
        Text "20.0%" — width: 56dp
        Text "4,800" — width: 96dp, #2E7D32

      Divider (1dp)

      # Row 4
      Row (height: 48dp)
        Text "Peter Otieno"
        Text "4,400" | Text "18.3%" | Text "4,392" — same style

      Divider (1dp)

      # Row 5
      Row (height: 48dp)
        Text "Mary Akinyi"
        Text "2,800" | Text "11.7%" | Text "2,808" — same style

    # Confirm Button
    FilledButton (minHeight: 56dp, fillMaxWidth: true, cornerRadius: 24dp)
      background: #2E7D32
      text: "Confirm & Proceed to Execute" — labelLarge, #FFFFFF
      enabled_when: memberPayouts.isNotEmpty()
      marginTop: 4dp
```

### Screen: Share-Out Execute

**Route**: `/groups/{groupId}/share-out/execute`
**Entry**: From share-out-preview via Confirm button

```
Scaffold
  TopAppBar (56dp)
    background: #2E7D32
    title: "Execute Share-Out" — titleLarge, #FFFFFF
    navigationIcon: arrow_back (enabled only when !isExecuting && !isCompleted)

  LazyColumn (padding: 0dp)

    # Summary Card
    Card (background: #A6F1A6, cornerRadius: 12dp, padding: 20dp,
          elevation: 0dp, margin: 16dp 16dp 0dp 16dp)
      Text "Total Distribution Pool" — labelMedium, #002106 (onPrimaryContainer)
      Text "KES 24,000" — headlineSmall, #002106, fontWeight: 700
        marginTop: 4dp
      Text "5 members to receive payouts" — bodyMedium, #002106
        marginTop: 4dp

    # Section Header
    Text "Member Payouts" — titleSmall, #424942 (onSurfaceVariant)
      padding: 16dp 16dp 4dp 16dp

    # Member Payout Rows (5 rows)
    LazyColumn
      Each row:
        ListItem (minHeight: 56dp, padding_horizontal: 16dp, padding_vertical: 12dp)
          leading:
            CircleAvatar (40dp × 40dp)
              background: #FFDDB3 (secondaryContainer)
              text: initials (2 chars) — titleSmall, #2A1700 (onSecondaryContainer)
          headline:
            Text memberName — bodyLarge, #1A1C19
          supporting:
            Text "KES [amount] ([percent]%)" — bodyMedium, #2E7D32 (primary)
          trailing:
            StatusIcon (24dp × 24dp) — visible when isExecuting || isCompleted || queuedOffline
              PENDING: circle_regular, #424942 (onSurfaceVariant)
              IN_PROGRESS: spinner animated, #FF8F00 (secondary/amber)
              DONE: checkmark_circle_filled, #2E7D32 (primary)
              FAILED: error_circle_filled, #D32F2F (error)
              QUEUED: cloud_arrow_up_regular, #FF8F00 (secondary)
          Divider below each row

    # Offline Info Banner (visible_when: !isOnline)
    Card (background: #FFF9C4, cornerRadius: 8dp, padding: 12dp, margin: 12dp 16dp 0dp)
      Row
        Icon wifi_off_24 — 20dp, #E65100
        marginEnd: 8dp
        Text "You are offline. Share-out will be queued and executed automatically when you reconnect."
          bodySmall, #E65100

    # Confirmation Section Card (visible_when: !isExecuting && !isCompleted && !queuedOffline)
    Card (background: #FAFAFA, elevation: 3dp, cornerRadius: 12dp,
          padding: 16dp, margin: 12dp 16dp 0dp)
      Text "Confirm Share-Out" — titleSmall, #1A1C19
        marginBottom: 4dp
      Text 'This action is irreversible. Type "SHARE OUT" below or use biometric authentication to confirm.'
        bodySmall, #424942 (onSurfaceVariant), marginBottom: 12dp

      OutlinedTextField (minHeight: 48dp, cornerRadius: 8dp)
        label: "Confirmation"
        placeholder: 'Type "SHARE OUT"'
        keyboardType: text
        value: confirmationText
        errorText: 'Must type exactly "SHARE OUT"'
          (visible when confirmationText.isNotBlank() && !isConfirmed)
        borderColor_active: #2E7D32 (when isConfirmed)
        borderColor_error: #D32F2F (when error)
        borderColor_normal: #727971

      Row (margin: 12dp 0dp, alignment: center)
        HorizontalDivider (flex: 1)
        Text "or" — labelSmall, #424942, padding: 0dp 8dp
        HorizontalDivider (flex: 1)

      OutlinedButton (minHeight: 48dp, fillMaxWidth: true, cornerRadius: 24dp)
        icon: fingerprint_24 — 20dp, leading
        text: "Use Biometric Instead" — labelLarge, primary color
        border: 1dp, #2E7D32

    # Execute Button (visible_when: !isCompleted && !queuedOffline)
    FilledButton (minHeight: 56dp, fillMaxWidth: true, cornerRadius: 24dp,
                  margin: 12dp 16dp 0dp)
      background: #D32F2F (error) when enabled
      background: #DEE5DA (surfaceVariant) when disabled
      text: "Execute Share-Out" — labelLarge
      text_color: #FFFFFF when enabled | #424942 when disabled
      enabled_when: isConfirmed && !isExecuting
      loading: CircularProgressIndicator (24dp, #FFFFFF) when isExecuting

    # Progress Indicator (visible_when: isExecuting)
    LinearProgressIndicator (height: 8dp, cornerRadius: 4dp, margin: 12dp 16dp 0dp)
      progress: executedCount / totalCount
      color: #2E7D32 (primary)
      trackColor: #A6F1A6 (primaryContainer)

    # Completion Banner (visible_when: isCompleted && failedPayouts.isEmpty())
    Card (background: #A6F1A6, cornerRadius: 12dp, padding: 20dp, margin: 16dp 16dp 0dp)
      Column (alignment: center, horizontalAlignment: center)
        Icon checkmark_circle_filled — 48dp, #2E7D32
        Text "Share-Out Complete!" — titleLarge, #002106, marginTop: 8dp
        Text "KES 24,000 distributed to 5 members successfully."
          bodyMedium, #002106, marginTop: 4dp

    # Partial Failure Banner (visible_when: isCompleted && failedPayouts.isNotEmpty())
    Card (background: #FFF9C4, cornerRadius: 12dp, padding: 16dp, margin: 16dp 16dp 0dp)
      Icon warning_filled — 32dp, #E65100
      Text "Partial Completion" — titleMedium, #E65100, marginTop: 4dp
      Text "4 of 5 payouts succeeded. 1 failed. Tap Retry to re-attempt failed payouts."
        bodySmall, #E65100

    # Retry Failed Button (visible_when: isCompleted && failedPayouts.isNotEmpty())
    FilledButton (margin: 12dp 16dp 0dp)
      background: #FF8F00 (secondary)
      text: "Retry Failed Payouts" — labelLarge, #FFFFFF

    # Done Button (visible_when: (isCompleted && failedPayouts.isEmpty()) || queuedOffline)
    FilledButton (minHeight: 56dp, fillMaxWidth: true, cornerRadius: 24dp, margin: 12dp 16dp 16dp)
      background: #2E7D32
      text: "Done" — labelLarge, #FFFFFF

    # Queued Offline Banner (visible_when: queuedOffline)
    Card (background: #FFDDB3, cornerRadius: 12dp, padding: 16dp, margin: 16dp 16dp 0dp)
      Icon cloud_arrow_up — 24dp, #2A1700 (onSecondaryContainer)
      Text "Queued for Sync" — titleSmall, #2A1700, marginTop: 4dp
      Text "5 payouts queued. They will be processed automatically when you reconnect."
        bodySmall, #2A1700
```

---

## 3. Component Specifications

### MemberPayoutRow Component
**Purpose**: Shows a single member's payout amount and real-time execution status during share-out.

**Props**:
- `payout: MemberPayout` — member data with amount and share percent
- `executionStatus: MemberExecutionStatus` — current status for this member
- `showStatus: Boolean` — visible during/after execution only

**Visual States by Status**:

| Status | Trailing Icon | Icon Color | Description for a11y |
|--------|--------------|-----------|----------------------|
| PENDING | circle_24_regular | #424942 | "Pending" |
| IN_PROGRESS | spinner_ios_20_filled (animated) | #FF8F00 | "Processing" |
| DONE | checkmark_circle_24_filled | #2E7D32 | "Completed" |
| FAILED | error_circle_24_filled | #D32F2F | "Failed" |
| QUEUED | cloud_arrow_up_24_regular | #FF8F00 | "Queued for sync" |

**Layout** (ListItem, min 56dp):
- Leading: CircleAvatar 40dp — background #FFDDB3, initials titleSmall
- Content: memberName (bodyLarge, #1A1C19) + "KES 6,792 (28%)" (bodyMedium, #2E7D32)
- Trailing: StatusIcon 24dp (visible only when showStatus=true)

**Animation on DONE**: Status icon scales 0→1.2→1.0 with 300ms spring animation

### ConfirmationTextField Component
**Props**:
- `value: String` — current text
- `isConfirmed: Boolean` — whether value matches "SHARE OUT"
- `onValueChange: (String) -> Unit`

**Border colors**:
- Default (empty): #727971 (outline)
- Typing (not confirmed): #727971
- Confirmed ("SHARE OUT"): #2E7D32 (primary) — 2dp width
- Error (typed but wrong): #D32F2F (error)

**Error text**: 'Must type exactly "SHARE OUT"' — labelSmall, #D32F2F
**Visibility rule**: error only shown when `confirmationText.isNotBlank() && !isConfirmed`

**Animation**: Border color transition 150ms, standard easing via `animateColorAsState`

### ExecuteButton Component
**State transitions**:

| State | Background | Text Color | Content |
|-------|-----------|-----------|---------|
| Disabled | #DEE5DA | #424942 | "Execute Share-Out" |
| Enabled | #D32F2F (error red) | #FFFFFF | "Execute Share-Out" |
| Loading | #D32F2F | hidden | CircularProgressIndicator 24dp white |

**Transition**: Disabled→Enabled background animates with `animateColorAsState(150ms)`
**Purpose of red**: Signals this action is irreversible — distinct from normal primary green CTAs

### ProgressIndicator Component
**Props**:
- `executedCount: Int`
- `totalCount: Int`
- `isExecuting: Boolean`

**Layout**: LinearProgressIndicator, height 8dp, cornerRadius 4dp
**Progress value**: `executedCount.toFloat() / totalCount.toFloat()`
**Color**: #2E7D32 (primary), track: #A6F1A6 (primaryContainer)
**Label below**: "1 of 5 payouts completed" — bodySmall, #424942

**Animation**: `animateFloatAsState(targetValue=progress, animationSpec=tween(300ms, standard easing))`

### CompletionBanner Component
**Props**:
- `totalPool: Double`
- `succeededCount: Int`
- `visible: Boolean`

**Layout**: Card, primaryContainer background, padding 20dp, cornerRadius 12dp
- Center-aligned column: icon → title → body
- Icon: checkmark_circle_filled, 48dp, #2E7D32
- Title: "Share-Out Complete!" — titleLarge, #002106
- Body: "KES 24,000 distributed to 5 members successfully." — bodyMedium, #002106

**Entrance animation**: `AnimatedVisibility(enter=fadeIn+slideInVertically, 400ms, decelerated easing)`

### FundSummaryCard Component (share-out-preview)
**Props**:
- `totalCorpus: Double`
- `totalProfit: Double`
- `totalPool: Double`

**Layout**: Card, surface bg, elevation 3dp
- Row 1: label "Total Corpus (Fund)" | value "KES 20,000" (bodyLarge)
- Row 2: label "Total Profit (Interest Earned)" | value "KES 4,000" (bodyLarge, #2E7D32)
- Divider
- Row 3: label "Total Distribution Pool" | value "KES 24,000" (titleLarge, #2E7D32, bold)

---

## 4. Interaction Patterns

### Confirmation Gate Flow (share-out-execute)
1. **Default state**: Execute button is grey/disabled, confirmation text field is empty
2. **User types**: Each keystroke calls `OnConfirmationTextChanged(text)`
3. **After 3+ chars typed wrongly**: Error text "Must type exactly SHARE OUT" appears below field (labelSmall, red)
4. **When "SHARE OUT" matched** (case-insensitive trim):
   - `isConfirmed = true`
   - Execute button transitions from grey (#DEE5DA) → red (#D32F2F) over 150ms
   - Content description of execute button updates to full irreversibility warning
5. **Biometric alternative**:
   - User taps "Use Biometric Instead"
   - System BiometricPrompt shown (Android platform API)
   - On success: `isConfirmed = true`, button activates as above
   - On failure: Snackbar "Biometric authentication failed. Please type SHARE OUT instead."

### Sequential Execution Flow (online path)
1. **User taps Execute** (with isConfirmed=true)
2. **Immediate state change**:
   - ScreenState → Executing
   - Back navigation disabled (arrow_back grayed out or hidden)
   - Confirmation section hides (AnimatedVisibility collapse, 250ms)
   - Progress indicator appears (AnimatedVisibility expand, 250ms)
3. **Step 1 — Create share-out record**:
   - POST /datatables/dt_share_out/{centerId}
   - On success: proceed to per-member payouts
   - On 403: navigate back, show "Chairperson role required" snackbar
   - On 500: queue everything to SyncQueue (fall through to offline path)
4. **Step 2 — Per-member payouts** (sequential, one at a time):
   - Member 1 (Amara Diallo, savingsAccountId: 1001):
     - `memberExecutionStatus[101] = IN_PROGRESS` — spinner icon animates
     - POST /savingsaccounts/1001/transactions (amount: 6,792)
     - On 2xx: `memberExecutionStatus[101] = DONE` — green checkmark appears with scale animation
     - `executedCount++`, progress bar fills to 1/5
   - Member 2 (Grace Mwangi): same flow, progress fills to 2/5
   - Member 3 (Fatima Ouedraogo): → 3/5
   - Member 4 (Peter Otieno): → 4/5
   - Member 5 (Mary Akinyi): → 5/5
5. **Completion**:
   - If all DONE: ScreenState → Success, completion banner slides in
   - If any FAILED: ScreenState → PartialFailure, partial banner shows

### Offline Queue Flow
1. **User taps Execute** while offline (isOnline=false)
2. Enqueue to SyncQueueRepository:
   - Priority=HIGH item: POST dt_share_out record
   - 5 items (one per member): POST /savingsaccounts/{id}/transactions
3. All `memberExecutionStatus` → QUEUED (cloud icon, amber)
4. `queuedOffline = true`
5. ScreenState → Success (optimistic display)
6. Queued banner appears: "5 payouts queued. They will process automatically when you reconnect."
7. Done button appears — taps OnDone → navigate to group-dashboard

### Partial Failure Retry Flow
1. **State**: Some DONE, some FAILED in memberExecutionStatus
2. Partial failure banner visible with counts "4 of 5 succeeded, 1 failed"
3. "Retry Failed Payouts" button tapped → `OnRetryFailed`
4. Failed members reset to PENDING → re-run withdrawal POST
5. On success: removed from failedPayouts; if failedPayouts.isEmpty → ScreenState.Success

---

## 5. Content Data

### Group: Mwangaza Women's Group
- Center ID: 7 (Fineract centerId)
- Cycle: 1
- Cycle length: 12 months
- Meetings conducted: 12 (cycle complete)

### Fund Figures — Cycle 1 Final
- Total corpus balance (accumulated savings fund): KES 20,000
- Total interest earned (from all loan repayments): KES 4,000
- **Total Distribution Pool**: KES 24,000

### Member Savings Contributions — Cycle 1
| Member | Member ID | Savings Account ID | Total Contributed | Share % | Payout (KES) |
|--------|-----------|-------------------|-------------------|---------|--------------|
| Amara Diallo | 101 | 1001 | KES 6,800 | 28.3% | KES 6,792 |
| Grace Mwangi | 102 | 1002 | KES 5,200 | 21.7% | KES 5,208 |
| Fatima Ouedraogo | 103 | 1003 | KES 4,800 | 20.0% | KES 4,800 |
| Peter Otieno | 104 | 1004 | KES 4,400 | 18.3% | KES 4,392 |
| Mary Akinyi | 105 | 1005 | KES 2,800 | 11.7% | KES 2,808 |
| **Total** | — | — | **KES 24,000** | **100%** | **KES 24,000** |

### Distribution Formula Verification
- Amara: 6,800 / 24,000 = 0.2833 → 0.2833 × 24,000 = KES 6,800 base + profit share = KES 6,792
- Grace: 5,200 / 24,000 = 0.2167 → KES 5,208
- Total: 6,792 + 5,208 + 4,800 + 4,392 + 2,808 = 24,000 ✓

### Execution Timeline (Meeting #12 — Cycle Close)
- Execution date: 07 May 2026 (Wednesday, final meeting)
- Field officer: Josephine Kamau (Staff ID: 12)
- Confirming chairperson: Amara Diallo
- dt_share_out record: cycle_number=1, total_pool=24000, executed_at="07 May 2026", status="completed"

### Partial Failure Demo Scenario
- Amara Diallo: DONE (KES 6,792 withdrawn successfully)
- Grace Mwangi: FAILED (insufficient balance in account — account closed early)
- Fatima Ouedraogo: DONE
- Peter Otieno: DONE
- Mary Akinyi: DONE
- Result: 4 succeeded, 1 failed — partial failure state shown
- Retry: Grace Mwangi withdrawal retried — if savings account restored, DONE; else stays FAILED

---

## 6. Responsive Rules

### Compact Layout (0–599dp — phones)
- **share-out-preview**: All sections stack vertically. Distribution table uses horizontal scroll (columns min 420dp total).
- **share-out-execute**: Summary card + member list + confirmation + execute button all stacked, full width.
- Member payout rows: 56dp height, leading avatar + content + trailing icon all in one row.
- Execute button: full width (fillMaxWidth), 56dp height, bottom of screen with 16dp margin.
- Progress indicator: full width.

### Medium Layout (600–839dp)
- **share-out-preview**: Table fits without horizontal scroll (all 4 columns visible).
- **share-out-execute**: Confirmation section card occupies 80% width, centered.
- Member payout rows same as compact but with more padding.

### Expanded Layout (840dp+)
- **share-out-preview**: Two-column layout — left: fund summary + formula chip; right: distribution table. 50/50 split.
- **share-out-execute**: Two-column — left: summary + payout list (scrollable); right: confirmation section + execute button (sticky).
- Both columns scrollable independently.
- Execute button stays visible in right column without scrolling.

### Bottom Navigation
- share-out-preview: bottom_nav visible=false (focused flow)
- share-out-execute: bottom_nav visible=false (critical irreversible action — no accidental nav)

### Typography at Large Text Size (1.3× OS multiplier)
- Table payout amounts (labelSmall) may wrap at 1.3× on compact — table uses horizontal scroll as fallback
- Completion banner text wraps naturally — no clipping

### Dark Theme Token Mapping
- primary: `#8BD68F` (light green on dark) — all primary green elements
- on_primary: `#003910`
- primary_container: `#00531A` — completion banner bg in dark mode
- on_primary_container: `#A6F1A6`
- error: `#FFB4AB` (light red on dark) — execute button still signals irreversibility
- surface: `#121412` — card backgrounds
- surface_variant: `#424942`
- secondary: `#FFB95C` (darker amber)

### Accessibility at Compact (360dp minimum supported width)
- Distribution table: switches to scrollable view at 360dp (min screen width of target devices)
- Execute button text "Execute Share-Out" truncates gracefully, never clips below button
- Member payout row: initials avatar and trailing icon both maintained at 360dp
- Confirmation field: minimum 280dp width, keyboard pushes up with `WindowInsetsCompat`

---

## Component State Matrix

Full state definitions for every interactive component in the share-out feature. CommonPurse design tokens: primary #2E7D32, error #D32F2F, Noto Sans.

### SummaryCard (share-out-preview screen — fund summary)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| SummaryCard | default | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | none | 2dp | false | true |
| SummaryCard | loading skeleton | surfaceVariant shimmer | n/a | none | 0dp | false | true |
| SummaryCard | error (data load failed) | errorContainer #FFDAD6 | onErrorContainer #410002 | 1dp error #D32F2F | 0dp | false | true |
| SummaryCard | dark mode | primaryContainer #00531A | onPrimaryContainer #A6F1A6 | none | 2dp | false | true |

### MemberPayoutRow (share-out-preview distribution table)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| PayoutRow | default | surface #FAFAFA | onSurface #1A1C19 | bottom 1dp outlineVariant #C2C9BD | 0dp | false | true |
| PayoutRow — avatar | default | secondaryContainer #FFDDB3 | onSecondaryContainer #2A1700 | none | 0dp | false | true |
| PayoutRow — amount chip | default | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | none | 0dp | false | true |
| PayoutRow — payout pending | secondaryContainer #FFDDB3 background | onSecondaryContainer #2A1700 | 1dp outline #FF8F00 | 0dp | false | true |
| PayoutRow — payout failed | errorContainer #FFDAD6 | onErrorContainer #410002 | 1dp error #D32F2F | 0dp | false | true |
| PayoutRow — payout success | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | none | 0dp | false | true |
| PayoutRow — highlighted | surface #FAFAFA | onSurface #1A1C19 | 2dp primary #2E7D32 | 2dp (focused for accessibility) | false | true |

### FormulaChip (share-out-preview screen)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| FormulaChip | default | tertiaryContainer #D2E4FF | onTertiaryContainer #001C39 | none | 0dp | true | true |
| FormulaChip | pressed | tertiary #1565C0 | onTertiary #FFFFFF | none | 0dp | true | true |
| FormulaChip | focused | tertiaryContainer #D2E4FF | onTertiaryContainer #001C39 | 2dp tertiary #1565C0 | 0dp | true | true |

### ExecuteButton (share-out-execute screen — critical irreversible action)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| ExecuteButton | default (locked) | surfaceVariant #DEE5DA | onSurfaceVariant #424942 | none | 0dp | false | true |
| ExecuteButton | unlocked (confirmation entered) | error #D32F2F | onError #FFFFFF | none | 6dp | true | true |
| ExecuteButton | pressed | error #B71C1C (darkened) | onError #FFFFFF | none | 12dp | true | true |
| ExecuteButton | focused | error #D32F2F | onError #FFFFFF | 2dp onError ring | 6dp | true | true |
| ExecuteButton | loading (in-progress) | error #D32F2F | CircularProgress white | none | 6dp | false | true |
| ExecuteButton | success | primary #2E7D32 | onPrimary #FFFFFF | none | 6dp | false | true |
| ExecuteButton | dark mode (locked) | surfaceVariant #424942 | onSurfaceVariant #DEE5DA | none | 0dp | false | true |

### ConfirmationTextField (share-out-execute screen)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| ConfirmField | empty (idle) | surfaceVariant #DEE5DA | onSurfaceVariant #424942 | 1dp outlineVariant #C2C9BD | 0dp | true | true |
| ConfirmField | typing (partial) | surfaceVariant #DEE5DA | onSurface #1A1C19 | 2dp primary #2E7D32 | 0dp | true | true |
| ConfirmField | correct ("CONFIRM") | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | 2dp primary #2E7D32 | 0dp | true | true |
| ConfirmField | incorrect (mismatch) | errorContainer #FFDAD6 | onErrorContainer #410002 | 2dp error #D32F2F | 0dp | true | true |
| ConfirmField | disabled (processing) | surface at 38% opacity | onSurface at 38% | none | 0dp | false | true |

### CompletionBanner (share-out-execute screen — post-execution)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------------------|---------|---------|
| CompletionBanner | hidden | — | — | — | — | false | false |
| CompletionBanner | animating in | primaryContainer #A6F1A6 (scale 0.8→1.0) | onPrimaryContainer #002106 | none | 0dp | false | true |
| CompletionBanner | visible | primaryContainer #A6F1A6 | onPrimaryContainer #002106 | none | 2dp | false | true |
| CompletionBanner — dark mode | visible | primary_container #00531A | on_primary_container #A6F1A6 | none | 2dp | false | true |

---

## API Failure & Recovery Playbook

### GET /shareout/preview (load distribution preview)

| Failure Type | Detection | User-Facing Response | Recovery |
|---|---|---|---|
| Network timeout | IOException after 10s | Snackbar: "Cannot load preview — check your connection" | Retry 1s → 2s → 4s; show cached preview if available |
| 401 Unauthorized | HTTP 401 | Navigate to login; return to share-out-preview after re-auth | Restore scroll position on return |
| 404 Group Not Found | HTTP 404 | "Group not found — please re-sync your group data" | Trigger group re-sync then retry |
| 500 Server Error | HTTP 5xx | Snackbar: "Server error — try again" with Retry action | Manual retry; log to Crashlytics |
| Offline | No network | "Offline — preview based on last synced data" warning banner (warningContainer) | Auto-refresh on reconnect; timestamp shows staleness |

Preview data freshness rule: if last sync > 24 hours ago, show stale-data chip "Data as of {timestamp} — refresh recommended".

### POST /shareout/execute (irreversible execution)

This is the highest-stakes API call in the app — triggers real money distribution. Special handling:

| Failure Type | Detection | User-Facing Response | Recovery |
|---|---|---|---|
| Network timeout (pre-commit) | IOException before server processes | "Connection lost — share-out NOT executed. Please check with server before retrying." | Do NOT auto-retry — risk of double execution; show manual check prompt |
| Network timeout (post-commit) | IOException after server may have processed | "Unknown status — contact your field officer immediately. Check server before retrying." | Show "Check Status" button that polls GET /shareout/status |
| 401 Unauthorized | HTTP 401 | Re-auth flow; re-present execute confirmation (do not auto-execute) | User must re-enter "CONFIRM" and tap Execute again |
| 409 Conflict (already executed) | HTTP 409 | "Share-out already executed for this cycle — no changes made" | Navigate to completion banner showing existing results |
| 422 Validation Error | HTTP 422 (e.g. unequal totals) | "Validation failed: {serverMessage}" — show specific error | Return to preview; force re-preview before re-execution |
| 500 Server Error | HTTP 5xx | "Share-out failed — contact your field officer" | Show error state; log to Crashlytics with full request context |
| Offline at execute time | No network | Disable Execute button; show "Must be online to execute share-out" tooltip | Auto-enable when reconnected; do not queue to SyncQueue (too high-stakes) |

### GET /shareout/status (poll after ambiguous timeout)

| Failure Type | Detection | User-Facing Response | Recovery |
|---|---|---|---|
| Completed | HTTP 200 status=COMPLETED | Show CompletionBanner; navigate to completion view | Normal flow |
| Not started | HTTP 200 status=NOT_STARTED | "Not executed — safe to retry" | Re-enable Execute button |
| In progress | HTTP 200 status=IN_PROGRESS | "Still processing — please wait" with spinner | Poll again after 5s (max 3 polls) |
| Timeout on status check | IOException | "Cannot determine status — contact field officer" | Manual intervention required |

### Offline Payout Recording (per-member payout status)

Individual payout status updates (per member) are queued to SyncQueue if the execute succeeded but individual status updates fail:
- SyncQueue entry: `{ type: "PAYOUT_STATUS", memberId, amount, cycleId }`
- Pending badge: shown on share-out nav entry
- Auto-sync: on next app open with network connectivity
- Max queue age: 7 days; after that, show "Payout status needs review" alert to field officer

---

## Screen Reader & Accessibility Deep Dive

### share-out-preview Screen — Focus Order (TalkBack / D-pad)

1. TopAppBar back arrow — "Go back, button"
2. TopAppBar title — "Cycle 1 — Distribution Preview, heading"
3. Fund Summary Card — "Total savings pool KES 24,000, heading" (role: group)
4. Summary row — "Total savings contributions: KES 18,000"
5. Summary row — "Total interest earned: KES 4,800"
6. Summary row — "Social fund deduction: KES 1,200"
7. Summary row — "Net distributable pool: KES 21,600"
8. Formula chip — "View distribution formula, button"
9. "Member Payouts" section header — "Member payouts, 5 members, heading"
10. Payout row — Amara Diallo — "Amara Diallo, payout KES 4,320, shares: 1.0, contributions: KES 3,600"
11. Payout row — Grace Mwangi — "Grace Mwangi, payout KES 5,184, shares: 1.2, contributions: KES 4,320"
12. Payout row — Peter Otieno — "Peter Otieno, payout KES 4,752, shares: 1.1, contributions: KES 3,960"
13. Payout row — Mary Akinyi — "Mary Akinyi, payout KES 3,888, shares: 0.9, contributions: KES 3,240"
14. Payout row — Fatima Ouedraogo — "Fatima Ouedraogo, payout KES 3,456, shares: 0.8, contributions: KES 2,880"
15. "Proceed to Execute" button — "Proceed to execute share-out, button"

### share-out-execute Screen — Focus Order

1. TopAppBar back arrow — "Go back to preview, button"
2. TopAppBar title — "Confirm Share-Out, heading"
3. Warning banner — "This action cannot be undone. KES 21,600 will be distributed to 5 members." (role: alert)
4. Summary recap card — read as group: "Total to distribute: KES 21,600, 5 members"
5. Confirmation field — "Type CONFIRM to enable the execute button, required, text field"
6. Execute button — "Execute share-out, button" (disabled until field correct)
7. Back / Cancel link — "Cancel and go back to preview, button"

### TalkBack Announcement Strings

| Element | Announcement |
|---|---|
| Summary card | "Fund summary for Mwangaza Women's Group Cycle 1: total pool KES 24,000, net distributable KES 21,600" |
| Payout row | "{memberName}, receives KES {amount}, based on {shares} shares and KES {contributions} contributions" |
| Formula chip | "Distribution formula: proportional to savings contributions, double-tap to see full formula" |
| Execute button (locked) | "Execute share-out button, disabled — type CONFIRM to enable" |
| Execute button (enabled) | "Execute share-out, double-tap to distribute KES 21,600 to 5 members. This cannot be undone." |
| Confirmation field (correct) | "CONFIRM entered — execute button is now enabled" |
| Confirmation field (incorrect) | "Incorrect — type the word CONFIRM in capital letters" |
| Completion banner | "Share-out complete! KES 21,600 distributed to 5 members of Mwangaza Women's Group. Cycle 1 closed." |
| Loading state | "Executing share-out, please wait" (live region: assertive) |
| Error state | "Share-out failed — {errorMessage}" (live region: assertive) |

### Content Descriptions — Icons

| Icon | Content Description |
|---|---|
| check_circle (payout success) | "Payout recorded" |
| pending (payout queued) | "Payout pending sync" |
| error (payout failed) | "Payout failed — needs attention" |
| info (formula chip icon) | "Distribution formula information" |
| warning (irreversibility banner) | "Warning: irreversible action" |
| celebration (completion banner) | "Share-out complete" |
| arrow_back | "Go back" |

### Live Region Announcements

- Execute starts: "Executing share-out for KES 21,600 — please wait" (assertive)
- Execute succeeds: "Share-out complete! KES 21,600 distributed to 5 members" (assertive)
- Execute fails: "Share-out failed — {reason}. No money was distributed." (assertive)
- Per-member payout recorded: "Payout of KES {amount} recorded for {memberName}" (polite, one per member)
- Offline detection: "No internet connection — share-out cannot be executed offline" (assertive)
- Preview load complete: "Distribution preview loaded for Cycle 1, Mwangaza Women's Group" (polite)

### WCAG AA Contrast Ratios

| Text / Background | Contrast Ratio | Pass Level |
|---|---|---|
| onPrimaryContainer #002106 / primaryContainer #A6F1A6 | 11.2:1 | AAA |
| onError #FFFFFF / error #D32F2F | 5.3:1 | AA (large text) |
| onTertiaryContainer #001C39 / tertiaryContainer #D2E4FF | 10.4:1 | AAA |
| onSurface #1A1C19 / surface #FAFAFA | 17.8:1 | AAA |
| onSecondaryContainer #2A1700 / secondaryContainer #FFDDB3 | 9.1:1 | AAA |
| onSurfaceVariant #424942 / surfaceVariant #DEE5DA | 5.9:1 | AA |
| onWarningContainer #E65100 / warningContainer #FFF9C4 | 4.8:1 | AA |

---

## Animation & Motion Spec

### Screen Transitions

| Transition | Type | Duration | Easing |
|---|---|---|---|
| Previous screen → share-out-preview | shared axis Z (forward) | 300ms | EmphasizedDecelerate |
| share-out-preview → share-out-execute | shared axis Z (forward, strong) | 350ms | EmphasizedDecelerate |
| share-out-execute → share-out-preview (back) | shared axis Z (backward) | 300ms | EmphasizedAccelerate |
| share-out-execute → completion | fade through | 400ms | Standard |

### Component Micro-Animations

| Component | Animation | Duration | Easing |
|---|---|---|---|
| CompletionBanner appear | scale 0.8→1.0 + opacity 0→1 | 400ms | EmphasizedDecelerate |
| PayoutRow check_circle appear | scale 0→1 staggered 50ms per row | 200ms each | EmphasizedDecelerate |
| ExecuteButton unlock | background color interpolation (grey→red) | 200ms | Standard |
| ExecuteButton loading | replace label with CircularProgress | 100ms | — |
| ConfirmationField correct | border color green + faint pulse | 300ms | Standard |
| ConfirmationField incorrect | horizontal shake 4dp left-right | 300ms (3 oscillations) | — |
| Warning banner entrance | slide down from top 200ms | 200ms | StandardDecelerate |
| Error snackbar | slide up from bottom | 250ms | StandardDecelerate |
| Error snackbar dismiss | fade out | 200ms | Standard |

### Loading Skeleton (share-out-preview)

```
ShimmerSpec:
  direction: left → right
  duration: 1200ms
  easing: LinearEasing (continuous loop)
  gradient: [ surfaceVariant #DEE5DA at 0%, surface #FAFAFA at 50%, surfaceVariant #DEE5DA at 100% ]
  angle: 20° diagonal
  Components shimmed:
    - SummaryCard placeholder: fillMaxWidth, height 120dp, cornerRadius 12dp
    - FormulaChip placeholder: width 140dp, height 32dp, cornerRadius 16dp
    - 5× PayoutRow placeholders: fillMaxWidth, height 56dp, cornerRadius 8dp
  Fade-out: shimmer fades 200ms as content fades in simultaneously
```

### Execute Progress Animation

When "Execute Share-Out" is tapped and processing begins:
1. Button label fades out, CircularProgressIndicator (white) fades in — 100ms
2. Progress indicator rotates continuously until API responds (no determinate progress)
3. On success: button transitions to primary green (200ms color interpolation); CompletionBanner animates in (400ms scale+fade)
4. On failure: button reverts to error red; shake animation 300ms; error Snackbar slides up

---

## Test & QA Annotations

### UI Test Tags

| Component | testTag |
|---|---|
| Preview screen root | `ShareOutPreview_Root` |
| Summary card | `ShareOut_SummaryCard` |
| Summary total pool | `ShareOut_TotalPool` |
| Formula chip | `ShareOut_FormulaChip` |
| Payout row (per member) | `PayoutRow_{memberId}` |
| Payout row amount | `PayoutRow_{memberId}_Amount` |
| Proceed button | `ShareOutPreview_ProceedButton` |
| Execute screen root | `ShareOutExecute_Root` |
| Warning banner | `ShareOutExecute_WarningBanner` |
| Confirmation field | `ShareOutExecute_ConfirmField` |
| Execute button | `ShareOutExecute_ExecuteButton` |
| Completion banner | `ShareOut_CompletionBanner` |
| Error snackbar | `Snackbar_Error` |
| Back / cancel | `ShareOutExecute_CancelButton` |

### Required Test Scenarios — share-out-preview

```
Given: group has 5 members with varied contributions (Amara: 3600, Grace: 4320, Peter: 3960, Mary: 3240, Fatima: 2880)
When: preview screen loads
Then: total pool shown as KES 24,000; net distributable KES 21,600; each member row shows proportional payout

Given: network is offline and cached preview exists
When: screen opens
Then: stale-data chip visible; cached data shown; "Refresh" button available

Given: network is offline and no cached preview
When: screen opens
Then: error state shown; "Cannot load — connect to internet to generate preview" message

Given: user taps formula chip
When: formula bottom sheet opens
Then: formula explained "Payout = (member savings / total savings) × distributable pool"; example with Amara's numbers shown

Given: all member payout rows render
When: screen renders completely
Then: sum of all 5 payout amounts equals KES 21,600 (within KES 1 rounding tolerance)
```

### Required Test Scenarios — share-out-execute

```
Given: confirmation field is empty
When: screen renders
Then: Execute button has disabled state (surfaceVariant background); TalkBack reads "disabled — type CONFIRM to enable"

Given: user types "confirm" (lowercase)
When: field value changes
Then: field shows error border; Execute button remains disabled; error text "Please type CONFIRM in capital letters"

Given: user types "CONFIRM" exactly
When: field value matches
Then: Execute button transitions to error red (enabled); TalkBack announces "CONFIRM entered — execute button now enabled"

Given: Execute button enabled and user taps
When: API call in progress
Then: button shows loading state; back button disabled; ConfirmationField disabled; no double-submit possible

Given: API returns success
When: execution completes
Then: CompletionBanner appears with scale animation; all 5 payout rows show check_circle; Snackbar "Share-out complete"

Given: API returns 409 (already executed)
When: error response received
Then: user sees "Share-out already executed for this cycle"; CompletionBanner shown with previous results
```

### Edge Cases

| Scenario | Expected Behavior |
|---|---|
| 1-member group share-out | Single payout row; total pool = single member payout (100%) |
| Member with zero contributions (e.g. joined mid-cycle) | Row shows KES 0 payout with note "Joined mid-cycle — no payout this cycle" |
| Very large pool (KES 999,999) | Amount formatted "KES 999,999"; no overflow in summary card |
| Member name 50+ chars (e.g. "Adaeze Nwachukwuemeka Obiechina") | Name truncated at 2 lines; full name in TalkBack; tooltip on long-press |
| RTL layout | Summary card rows mirror; avatar stays on start side; trailing icons flip |
| Execute tapped twice rapidly | Second tap ignored (button disabled during processing; state = loading) |
| App backgrounded during execution | WorkManager job continues in background; completion notification sent |

### Performance Baselines

- share-out-preview first paint: < 400ms (more complex calculation than list screens)
- Formula bottom sheet open: < 150ms
- Execute button feedback (tap to loading state): < 100ms
- CompletionBanner animation: smooth 60fps; no jank on mid-range devices
- PayoutRow status update (staggered): all 5 rows complete within 500ms of success response

---

## i18n / Localization Spec

### String Keys and Translations

| Key | English (en) | Swahili (sw) | French (fr) |
|-----|-------------|--------------|-------------|
| `shareout_preview_title` | "Cycle {n} — Distribution Preview" | "Mzunguko {n} — Muhtasari wa Mgawanyo" | "Cycle {n} — Aperçu de distribution" |
| `shareout_execute_title` | "Confirm Share-Out" | "Thibitisha Mgawanyo" | "Confirmer le partage" |
| `shareout_total_pool` | "Total Savings Pool" | "Jumla ya Akiba" | "Pool total d'épargne" |
| `shareout_net_distributable` | "Net Distributable" | "Kiasi cha Kugawanywa" | "Montant net distribuable" |
| `shareout_member_payouts` | "Member Payouts" | "Malipo ya Wanachama" | "Paiements des membres" |
| `shareout_formula_chip` | "View Formula" | "Angalia Mfumo" | "Voir la formule" |
| `shareout_proceed_button` | "Proceed to Execute" | "Endelea na Utekelezaji" | "Procéder à l'exécution" |
| `shareout_confirm_label` | "Type CONFIRM to enable" | "Andika THIBITISHA kuwezesha" | "Tapez CONFIRMER pour activer" |
| `shareout_execute_button` | "Execute Share-Out" | "Tekeleza Mgawanyo" | "Exécuter le partage" |
| `shareout_warning_irreversible` | "This action cannot be undone" | "Hatua hii haiwezi kutenduliwa" | "Cette action est irréversible" |
| `shareout_complete_title` | "Share-Out Complete!" | "Mgawanyo Umekamilika!" | "Partage terminé !" |
| `shareout_complete_body` | "KES {amount} distributed to {count} members" | "KES {amount} imegawanywa kwa wanachama {count}" | "KES {amount} distribués à {count} membres" |
| `shareout_offline_warning` | "Must be online to execute share-out" | "Lazima uwe na mtandao kutekeleza mgawanyo" | "Vous devez être en ligne pour exécuter le partage" |
| `shareout_already_executed` | "Share-out already executed for this cycle" | "Mgawanyo umetekelezwa tayari kwa mzunguko huu" | "Le partage a déjà été exécuté pour ce cycle" |
| `shareout_payout_row` | "{memberName} — KES {amount}" | "{memberName} — KES {amount}" | "{memberName} — KES {amount}" |
| `shareout_stale_data` | "Data as of {timestamp} — refresh recommended" | "Data ya {timestamp} — inashauriwa usasishaji" | "Données du {timestamp} — actualisation recommandée" |

### Pluralization Rules

| Key | Singular | Plural | Notes |
|---|---|---|---|
| `member_count` | "1 member" | "{n} members" | sw: "mwanachama 1" → "wanachama {n}" |
| `cycle_count` | "Cycle 1" | "Cycles {n}" | sw: "Mzunguko 1" → "Mizunguko {n}" |
| `payout_count` | "1 payout" | "{n} payouts" | sw: "malipo 1" → "malipo {n}" (same form) |

### Number Formatting (KES amounts in share-out context)

| Locale | Format | Example (KES 21,600) |
|---|---|---|
| en-KE | KES 21,600 | KES 21,600 |
| sw-KE | KES 21,600 | KES 21,600 (same) |
| fr-FR | KES 21 600 | thin-space thousands separator |

Individual payout amounts: always show 2 decimal places if there is a remainder from proportional division (e.g. KES 4,320.00 or KES 4,319.99 when rounding occurs). Rounding remainder distributed to group treasurer row automatically.

### RTL Considerations

- Summary card rows: amount always on end (right in LTR → left in RTL)
- Payout table: member name on start, amount on end; mirrors in RTL
- Warning banner icon: stays at start of banner (leading icon)
- Execute button: full-width, text centered — no directional change needed
- All string arguments ({memberName}, {amount}) positioned with XML placeholder — word order adapts to locale grammar

---

## Offline-First Architecture Notes

### Share-Out Is NOT Offline-Capable for Execution

Unlike most other features, share-out execution requires network connectivity. This is a deliberate product decision:
- Financial distribution of real money cannot be queued and auto-executed later without explicit re-confirmation
- The execute flow enforces online-only: Execute button is fully disabled when offline
- Preview generation CAN use cached data, but clearly marks staleness

### Share-Out Data Model (Room Entities)

```
ShareOutPreviewEntity {
  cycleId: String (PK)
  groupId: String
  totalSavings: Long          // KES paise-equivalent
  totalInterest: Long
  socialFundDeduction: Long
  netDistributable: Long
  generatedAt: Instant
  isCached: Boolean           // true = loaded from cache, not live server
  serverVersion: Int          // for conflict detection
}

MemberPayoutEntity {
  payoutId: String (PK)
  cycleId: String (FK → ShareOutPreviewEntity)
  memberId: String
  memberName: String          // denormalized for display when member table unavailable
  contributionAmount: Long
  shareRatio: Double          // e.g. 1.2 for Grace Mwangi
  payoutAmount: Long
  payoutStatus: PayoutStatus (PENDING | COMPLETED | FAILED)
  processedAt: Instant?
}

ShareOutExecutionEntity {
  executionId: String (PK)
  cycleId: String (FK)
  executedAt: Instant
  executedByUserId: String
  totalDistributed: Long
  memberCount: Int
  status: ExecutionStatus (COMPLETED | PARTIAL | FAILED)
}
```

### Preview Cache Invalidation Rules

The preview cache is invalidated when any of the following occurs:
- A new savings contribution is recorded in the current cycle
- A loan repayment is recorded (changes interest earned)
- Group configuration (social fund %) is changed
- Cache age exceeds 24 hours
- Field officer manually pulls to refresh

When cache is invalid: show "Refresh required — data changed since last preview" banner. Proceed button disabled until refresh completes.

### Idempotency Key for Execute

Each share-out execute POST includes a client-generated idempotency key:
```
X-Idempotency-Key: {cycleId}-{deviceId}-{timestampMs}
```
Server enforces: same key → same response (no double-execution). Client stores key in ShareOutExecutionEntity until server confirms completion. This handles the ambiguous-timeout scenario safely.

### Member Payout Ordering

Members in the payout table are sorted by:
1. Primary: contribution amount (descending) — highest contributor first
2. Secondary: alphabetical name (for tie-breaking)

Display order is fixed — not user-sortable. Grace Mwangi (KES 4,320 contributions) always appears before Fatima Ouedraogo (KES 2,880 contributions) in Mwangaza Women's Group Cycle 1.

### Post-Execution Audit Trail

After a successful share-out:
- A read-only audit record is stored locally and on server
- Audit record includes: executedBy, executedAt, total distributed, per-member amounts, idempotency key
- Field officer can view audit from previous cycles in Share-Out History screen (v2.0.0)
- Audit data is never deleted from server; local audit retained for 2 years

### Error Recovery Flow — Partial Failure

If execution partially succeeds (some member payouts recorded, others fail):
- Status = PARTIAL in ShareOutExecutionEntity
- Failed payout rows show error (errorContainer) in completion view
- "Retry Failed Payouts" button appears — retries only the failed individual payout records
- Partial state is surfaced to field officer immediately; not hidden
- Field officer notified via push notification if partial failure detected while app is backgrounded

---

## Share-Out Cycle State Machine

The share-out feature follows a strict state machine tied to the group's active cycle. Understanding the states is essential for correct screen rendering and button enablement.

### Cycle States

| State | Description | share-out-preview visible | Execute enabled |
|---|---|---|---|
| ACTIVE | Cycle in progress; savings being collected | No | No |
| PREVIEW_READY | Cycle end date reached; preview available | Yes | No (preview only) |
| EXECUTING | Execute tapped; processing in progress | Yes (read-only) | No (in-progress) |
| COMPLETED | Share-out executed successfully | Yes (completion view) | No (done) |
| PARTIAL | Some payouts failed | Yes (partial view) | Retry failed only |
| VOIDED | Execution rolled back by admin | No | No |

Transitions: ACTIVE → PREVIEW_READY (auto, on cycle end date) → EXECUTING (user action) → COMPLETED or PARTIAL.

### Cycle 1 Example — Mwangaza Women's Group

Reference data used across all share-out screens and test scenarios:

| Member | Contributions (KES) | Share Ratio | Payout (KES) |
|---|---|---|---|
| Amara Diallo | 3,600 | 1.0 | 4,320 |
| Grace Mwangi | 4,320 | 1.2 | 5,184 |
| Peter Otieno | 3,960 | 1.1 | 4,752 |
| Mary Akinyi | 3,240 | 0.9 | 3,888 |
| Fatima Ouedraogo | 2,880 | 0.8 | 3,456 |
| **Total** | **18,000** | — | **21,600** |

Social fund deduction: KES 1,200 (applied before distribution).
Interest earned: KES 4,800 (10% on average outstanding loans).
Net distributable = KES 18,000 + KES 4,800 − KES 1,200 = KES 21,600.

Distribution formula: `payout = (memberContributions / totalContributions) × shareRatio × netDistributable / sumOfShareRatios`

All amounts round to the nearest KES. Rounding remainder (if any) added to highest-contributor payout (Grace Mwangi).

### Member Avatar Colors (consistent across all screens)

Each member has a deterministic avatar background color derived from their memberId hash, mapped to secondaryContainer palette variants:

| Member | Avatar Background | Initials |
|---|---|---|
| Amara Diallo | secondaryContainer #FFDDB3 | AD |
| Grace Mwangi | primaryContainer #A6F1A6 | GM |
| Peter Otieno | tertiaryContainer #D2E4FF | PO |
| Mary Akinyi | secondaryContainer #FFDDB3 (shade 2) | MA |
| Fatima Ouedraogo | errorContainer #FFDAD6 (light, non-error context) | FO |

All avatar text: onSurface #1A1C19 for sufficient contrast on all background variants.

### Share-Out History Screen (v2.0.0 planned)

Not in current scope but referenced in this spec for completeness:
- Lists all completed share-outs with date, total distributed, cycle number
- Each row tappable → opens read-only completion view
- Data sourced from ShareOutExecutionEntity (retained permanently)
- FilterChip: by year (2025, 2026, All)
- Export available per historical cycle

### Push Notification Spec — Share-Out Events

| Event | Title | Body | Deep Link |
|---|---|---|---|
| Cycle enters PREVIEW_READY | "Share-out ready for Mwangaza Women's Group" | "Cycle 1 is complete — KES 21,600 ready to distribute" | `commonpurse://share-out/preview/{cycleId}` |
| Execute succeeds | "Share-out complete!" | "KES 21,600 distributed to 5 members of Mwangaza Women's Group" | `commonpurse://share-out/complete/{cycleId}` |
| Partial failure | "Share-out partially failed" | "2 payouts need attention for Mwangaza Women's Group" | `commonpurse://share-out/partial/{cycleId}` |
| Payout sync retry succeeds | "Pending payouts synced" | "All member payouts now recorded successfully" | `commonpurse://share-out/complete/{cycleId}` |

Notification channel: `share_out_events` — priority HIGH, vibration on, lockscreen visibility PRIVATE (financial data).

---

## Stitch Designer Checklist

Before submitting share-out screens for review, verify each item:

### share-out-preview Checklist

- [ ] Fund summary card uses primaryContainer #A6F1A6 background (not white, not green primary)
- [ ] Summary rows: label on start (onSurfaceVariant), amount on end (onSurface bold)
- [ ] Net distributable row visually distinct (titleLarge weight, onPrimary or on-primaryContainer)
- [ ] FormulaChip uses tertiaryContainer #D2E4FF — not primary green (reserved for actions)
- [ ] All 5 member payout rows present with avatar, name, payout amount chip
- [ ] Payout amount chips use primaryContainer #A6F1A6 background
- [ ] Member avatars: consistent initials style, secondaryContainer background
- [ ] "Proceed to Execute" button: primary green, full-width or prominent CTA placement
- [ ] Bottom nav hidden (focused flow — no accidental navigation away)
- [ ] Dark mode tokens applied to all components (see Dark Theme Token Mapping section)

### share-out-execute Checklist

- [ ] Warning banner (irreversibility) immediately visible without scrolling on compact screen
- [ ] Warning banner uses warningContainer #FFF9C4 / onWarningContainer #E65100
- [ ] Confirmation TextField placeholder text: "Type CONFIRM to enable"
- [ ] Execute button: error #D32F2F when unlocked — never primary green (must signal danger)
- [ ] Execute button disabled state: surfaceVariant background (clearly locked)
- [ ] CompletionBanner hidden in default state (only appears post-execution)
- [ ] Back/Cancel option present and accessible (no user traps)
- [ ] Online-only note visible when offline (Execute button disabled + tooltip)
- [ ] TalkBack: Execute button reads "cannot be undone" warning in announcement
- [ ] Loading state on Execute button during processing (no double-tap possible)

### Visual QA — Both Screens

- [ ] Noto Sans font loaded correctly (not system default)
- [ ] All text at scale_style: large sp values (not px or dp)
- [ ] Contrast ratios verified for all text/background combos (see WCAG table)
- [ ] Touch targets: minimum 48dp × 48dp for all interactive elements
- [ ] No hard-coded KES amounts — all sourced from ShareOutPreviewEntity data
- [ ] Member names used: Amara Diallo, Grace Mwangi, Peter Otieno, Mary Akinyi, Fatima Ouedraogo
- [ ] Group name: "Mwangaza Women's Group" in all headers
- [ ] Amounts in KES (Kenyan Shillings), comma-formatted for thousands
