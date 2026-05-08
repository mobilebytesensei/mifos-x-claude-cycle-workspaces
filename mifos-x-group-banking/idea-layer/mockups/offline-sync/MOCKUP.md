# Offline Sync — Mockup Specification
**Feature**: offline-sync | **Screen**: sync-status

---

## Design Language

**System**: Material Design 3, comfortable density
**Font**: Noto Sans
**Primary**: #2E7D32 — Sync Now button, SYNCED status, success icons
**Secondary**: #FF8F00 — pending/queued indicators, amber progress chips
**Error**: #D32F2F — FAILED status card, failed item badges, retry borders
**Min touch target**: 48dp (Sync Now button: 56dp)

---

## Screen: Sync Status

### Layout — PENDING State (demo data: 3 pending, 0 failed)
```
┌─────────────────────────────────────────┐
│  Sync Status                   [refresh]│  TopAppBar — surface, elevation 2dp
│                                         │  No back button (bottom nav terminal)
├─────────────────────────────────────────┤
│ ┌─ ● PENDING ──────────────────────── ┐ │  Status card — #FFF9C4 bg, 8dp corners
│ │   3 items pending sync              │ │  titleMedium, #E65100 text
│ │   Last sync: Yesterday 8:30 AM      │ │  bodySmall, onSurfaceVariant
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ ┌─ Pending by Type ─────────────────  ┐ │  Surface card — elevation 2dp
│ │ 📋 Meeting Records    [1 pending]   │ │  LabelWithBadge row, 48dp height
│ │ 💰 Savings            [2 pending]   │ │  badge: secondaryContainer #FFDDB3
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  [0 conflicts]                          │  Conflict chip — tertiaryContainer #D2E4FF
│                                         │  labelSmall, #1565C0 text, borderRadius 16dp
├─────────────────────────────────────────┤
│ ┌─ Failed Operations ───────────────  ┐ │  Section — hidden when failedCount == 0
│ │  (empty — no failures)              │ │  errorContainer #FFDAD6 bg (shown when > 0)
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │       ↑  Sync Now                   │ │  FilledButton — primary green, 56dp height
│ └─────────────────────────────────────┘ │  full width, 16dp side margin
└─────────────────────────────────────────┘
```

### Layout — SYNCED State
```
┌─────────────────────────────────────────┐
│  Sync Status                   [refresh]│
├─────────────────────────────────────────┤
│ ┌─ ✓ SYNCED ──────────────────────── ┐ │  Status card — #C8E6C9 bg, 8dp corners
│ │   All data synced                   │ │  titleMedium, #1B5E20 text
│ │   Last sync: Today 8:30 AM          │ │  bodySmall, onSurfaceVariant
│ └─────────────────────────────────────┘ │
│ ┌─ Pending by Type ─────────────────  ┐ │
│ │  (all zeroes — no rows displayed)   │ │  Section hidden or "Everything is up to date"
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │       ✓  Sync Now                   │ │  Enabled — user may force sync manually
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Layout — FAILED State (e.g. savings item 400 error)
```
┌─────────────────────────────────────────┐
│  Sync Status                   [refresh]│
├─────────────────────────────────────────┤
│ ┌─ ✕ FAILED ─────────────────────── ┐ │  Status card — #FFCDD2 bg, 8dp corners
│ │   1 item failed                     │ │  titleMedium, #D32F2F text
│ │   Last sync: Today 8:30 AM          │ │  bodySmall
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ ┌─ Failed Operations ─────────────────┐ │  Surface — errorContainer #FFDAD6 bg
│ │ ✕  SAVINGS / CREATE               │ │  LabelMedium — entity type + operation
│ │    The savings account balance...  │ │  bodySmall, onSurfaceVariant, max 2 lines
│ │    [Retry]                         │ │  OutlinedButton — onErrorContainer border
│ │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │ │  Divider between items
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │       ↑  Sync Now                   │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Layout — OFFLINE State (isOnline = false)
```
┌─────────────────────────────────────────┐
│  Sync Status                   [refresh]│
│ [wifi_off] You are offline              │  Offline banner — warningContainer #FFF9C4
│                                         │  bodySmall, icon 16dp, 8dp padding
├─────────────────────────────────────────┤
│ [Status card — same content as above]   │
│ [Pending by Type — same]                │
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │       ↑  Sync Now (disabled)        │ │  FilledButton — greyed (#DEE5DA bg)
│ └─────────────────────────────────────┘ │  Not clickable when isOnline=false
└─────────────────────────────────────────┘
```

### Layout — Syncing State (isSyncing = true)
```
┌─────────────────────────────────────────┐
│  Sync Status                   [refresh]│
├─────────────────────────────────────────┤
│ [Status card — PENDING with spinner]    │  CircularProgressIndicator 24dp inside card
│ ┌─ Syncing... ─────────────────────── ┐ │  AnimatedVisibility — appears when isSyncing
│ │  ⟳  Syncing 3 items...             │ │  LinearProgressIndicator — primary green
│ └─────────────────────────────────────┘ │  indeterminate mode, 4dp height
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │       ⟳  Syncing... (disabled)      │ │  Button shows spinner, disabled during sync
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Layout — Loading State (initial load from SQLDelight)
```
┌─────────────────────────────────────────┐
│  Sync Status                            │
├─────────────────────────────────────────┤
│ ████████████████████████████████████  │  Shimmer block — 80dp height, rounded 8dp
│                                         │  ShimmerEffect: alpha 0.3→1.0, 1200ms
│ ████████████████████████████████████  │  Shimmer block — 120dp height
│                                         │
│ ████████████████████████████████████  │  Shimmer block — 56dp height (button)
└─────────────────────────────────────────┘
```

---

## Component Specifications

### StatusCard
| Property | Value |
|----------|-------|
| Width | fill-maxWidth, 16dp horizontal margin |
| Height | wrap_content, min 72dp |
| Corner radius | 8dp (shape.small) |
| Padding | 16dp all sides |
| Background | SYNCED: #C8E6C9 / PENDING: #FFF9C4 / FAILED: #FFCDD2 |
| Status icon | ✓ (24dp, #1B5E20) / ● (24dp, #E65100) / ✕ (24dp, #D32F2F) |
| Title | titleMedium, status-specific color, bold |
| Subtitle | bodySmall, onSurfaceVariant |

### PendingByTypeSection
| Row Element | Spec |
|-------------|------|
| Row height | 48dp min |
| Entity icon | 24dp, from MD3 icon set |
| Label | bodyMedium, onSurface |
| Badge | secondaryContainer #FFDDB3 bg, labelSmall, 16dp corner radius |
| Divider | 1dp, outline color |

### FailedOperationRow
| Element | Spec |
|---------|------|
| Background | errorContainer #FFDAD6 |
| Entity + operation label | labelMedium, onErrorContainer #410002 |
| Error message | bodySmall, onSurfaceVariant, max 2 lines, ellipsize end |
| Retry button | OutlinedButton — border onErrorContainer color, 48dp height |
| Row padding | 12dp vertical, 16dp horizontal |

### ConflictChip
| Property | Value |
|----------|-------|
| Background | tertiaryContainer #D2E4FF |
| Text color | tertiary #1565C0 |
| Corner radius | 16dp (pill shape) |
| Text | labelSmall — "N conflicts detected" or "0 conflicts" |
| Visibility | Always shown (even when 0) |

### SyncNowButton
| State | Background | Text | Icon |
|-------|-----------|------|------|
| Enabled (online) | primary #2E7D32 | "Sync Now" | upload icon |
| Disabled (offline) | #DEE5DA | "Sync Now" | upload icon |
| Syncing | primary #2E7D32 | "Syncing..." | CircularProgressIndicator 18dp |
| Height | 56dp all states | | |
| Width | fill-maxWidth, 16dp margin | | |

---

## Navigation

sync-status is a **terminal screen** — it appears in the bottom navigation bar and does not navigate anywhere. All actions (Sync Now, Retry) execute in-place and update the screen state.

### Bottom Navigation Entry
| Property | Value |
|----------|-------|
| Icon | sync (outlined) |
| Label | Sync |
| Badge | Red dot when failedCount > 0 |

### Entry Points
- Bottom navigation Sync tab tap
- Any screen's offline indicator badge tap (leads to sync-status)

---

## Interaction Patterns

1. **Screen load**: Read SQLDelight synchronously on background dispatcher → emit to StateFlow → isLoading=false (no network call)
2. **Sync Now tap**: OnSyncNow action → isSyncing=true → disable button + show progress → SyncManager.syncNow() → collect result → update queue items → isSyncing=false → emit ShowSnackbar or SyncCompleted
3. **Retry tap**: OnRetryOperation(itemId) → UPDATE sync_queue SET status='pending' WHERE id=itemId → re-read counts → update UI
4. **Refresh tap**: OnRefresh action → re-read SQLDelight → update all ViewModel fields
5. **Connectivity restore**: NetworkMonitor emits isOnline=true → SyncManager auto-trigger if pendingCount > 0 → same flow as Sync Now
6. **Conflict chip tap**: No action — display only (future: conflict resolution screen in v2.0.0)

---

## Accessibility

- Status card icon uses contentDescription: "Sync status: PENDING — 3 items waiting"
- Sync Now button: "Sync now — sends 3 pending items to server" when enabled; "Sync unavailable — you are offline" when disabled
- Failed operation retry button: "Retry syncing savings transaction — previously failed with balance error"
- Conflict chip: role=chip with contentDescription "0 conflicts detected"
- Progress indicator: role=progressbar with label "Syncing in progress"
- All badges use contentDescription: "2 pending savings transactions"
