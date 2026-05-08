# Share-Out — Mockup Specification
**Feature**: share-out | **Screens**: share-out-preview, share-out-execute

---

## Design Language

**System**: Material Design 3, comfortable density
**Font**: Noto Sans
**Primary**: #2E7D32 — TopBar, confirm button, completion state
**Error**: #D32F2F — Execute button (signals irreversibility)
**Secondary**: #FF8F00 — queued/sync indicators
**Min touch target**: 48dp (56dp for execute button)

---

## Screen 1: Share-Out Preview

### Layout
```
┌─────────────────────────────────────────┐
│ [←] Share-Out Preview       [refresh]   │  TopAppBar — primary green
├─────────────────────────────────────────┤
│ ┌ Cycle 1 — Distribution Preview ─────┐ │  Info banner — primaryContainer
│ │ All calculations are preliminary.    │ │  titleMedium + bodySmall
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ ┌─ Fund Summary ──────────────────────┐ │  Surface card — elevation 2dp
│ │ Total Corpus (Fund)                  │ │  LabeledValue row
│ │                     KES 20,000       │ │  bodyLarge
│ │ Total Profit (Interest Earned)       │ │
│ │                      KES 4,000       │ │  bodyLarge, primary color
│ │ ──────────────────────────────────── │ │  divider
│ │ Total Distribution Pool              │ │
│ │                     KES 24,000       │ │  titleLarge, primary, bold
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ [Formula: Pro-rata by savings contrib.]  │  Info chip — tertiaryContainer
├─────────────────────────────────────────┤
│ Member          │ Savings │ Share% │Payout│  Data table
│ Amara Diallo    │ 6,800   │ 28.3%  │6,792 │  Highest payout: #E8F5E9 bg
│ Grace Mwangi    │ 5,200   │ 21.7%  │5,208 │
│ Fatima Ouedraogo│ 4,800   │ 20.0%  │4,800 │
│ Peter Otieno    │ 4,400   │ 18.3%  │4,392 │
│ Mary Akinyi     │ 2,800   │ 11.7%  │2,808 │
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │      Confirm & Proceed to Execute   │ │  FilledButton — primary, 56dp
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### States
- **Loading**: 4× shimmer blocks (80dp height each)
- **Content**: All sections visible
- **Error**: cloud_off icon + error message + Retry CTA

### Distribution Table Styling
- Header row: surfaceVariant background, labelSmall, onSurfaceVariant text
- Member column: fill width
- Savings, Share%, Payout columns: 104dp, 64dp, 104dp respectively
- Highest payout row: background #E8F5E9, text #1B5E20 (Amara Diallo at 28.3%)
- Default rows: surface background

---

## Screen 2: Share-Out Execute

### Layout — Content State (awaiting confirmation)
```
┌─────────────────────────────────────────┐
│ [←] Execute Share-Out                   │  TopAppBar — primary; back enabled pre-execution
├─────────────────────────────────────────┤
│ ┌ Total Distribution Pool ────────────┐ │  Summary card — primaryContainer
│ │           KES 24,000                │ │  headlineSmall, bold
│ │ 5 members to receive payouts        │ │  bodyMedium
│ └─────────────────────────────────────┘ │
│ Member Payouts                           │  Section header — titleSmall, onSurfaceVariant
│ ─────────────────────────────────────── │
│ [AD] Amara Diallo    KES 6,792 (28%)  ○ │  MemberPayoutRow — 56dp min height
│ [PO] Peter Otieno   KES 5,208 (22%)  ○ │  Trailing: status icon (○=pending)
│ [GW] Grace Mwangi   KES 4,800 (20%)  ○ │
│ [JM] John Mwangi    KES 4,392 (18%)  ○ │
│ [MA] Mary Akinyi    KES 2,808 (12%)  ○ │
├─────────────────────────────────────────┤
│ ┌─ Confirm Share-Out ─────────────────┐ │  Confirmation card — surface, elevation 2dp
│ │ This action is irreversible. Type   │ │  bodySmall, onSurfaceVariant
│ │ "SHARE OUT" or use biometric.       │ │
│ │ ┌─ Confirmation ──────────────────┐ │ │  TextField — 48dp min
│ │ │ Type "SHARE OUT"                │ │ │
│ │ └─────────────────────────────────┘ │ │
│ │ ─────────── or ─────────────────── │ │  Divider with "or" text
│ │ [🖐 Use Biometric Instead]          │ │  OutlinedButton — full width, 48dp
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │         Execute Share-Out           │ │  FilledButton — ERROR red (#D32F2F), 56dp
│ └─────────────────────────────────────┘ │  Greyed when !isConfirmed
└─────────────────────────────────────────┘
```

### Layout — Executing State
```
[Summary card — same as above]
[Member Payouts list with animated status icons]
  Amara Diallo  KES 6,792  ⟳ (spinner, amber, animated)  ← IN_PROGRESS
  Peter Otieno  KES 5,208  ○ (pending circle)            ← PENDING
  Grace Mwangi  KES 4,800  ○                              ← PENDING
  ...

[Progress bar — 8dp height, #2E7D32, fills left to right]
  "1 of 5 payouts completed"
```

### Layout — Success State
```
[Summary card]
[Payout list — all ✓ green checkmarks]
  Amara Diallo  KES 6,792  ✓ (green checkmark_circle_filled)
  Peter Otieno  KES 5,208  ✓
  ...

[Completion Banner — primaryContainer]
  ✓ (48dp icon, primary green)
  "Share-Out Complete!"  (titleLarge)
  "KES 24,000 distributed to 5 members successfully." (bodyMedium)

[Done button — primary, 56dp, full width]
```

### Layout — Offline State (additional banner)
```
[Wifi-off icon] [You are offline. Share-out will be queued and executed automatically when you reconnect.]
Background: warningContainer (#FFF9C4), text: onWarningContainer (#E65100)
```

---

## Interaction Patterns

1. **Confirmation text typing**: Each keystroke updates `isConfirmed`; "SHARE OUT" (any case) enables execute button with 150ms color transition
2. **Execute button activation**: Transitions from greyed (`#DEE5DA` bg) to red (`#D32F2F`) with 200ms animate
3. **Biometric tap**: Shows system biometric prompt; on success `isConfirmed = true`
4. **Execution start**: Back navigation disabled, execute button shows spinner, progress bar appears with AnimatedVisibility
5. **Per-member status animation**: Status icon cycles PENDING → IN_PROGRESS (spinning amber) → DONE (green check) or FAILED (red circle)
6. **Progress bar fill**: Animates width from 0 to full as executedCount/totalCount increases (300ms per step, standard easing)

---

## Accessibility

- Execute button labeled "Execute share-out — distributes KES 24,000 to 5 members. This cannot be undone." when enabled
- Confirmation field has hint text and explicit content description with current confirmation state
- All member payout rows have content descriptions including execution status
- Error indicators use both icon and text, not color alone
- Progress bar uses `role=progressbar` with semantic value and label
