# Offline Sync — Stitch Prompt Specification
**Feature**: offline-sync | **Screen**: sync-status
**Stitch project**: MifosSave / mifos-x-group-banking
**Total sections**: 6

---

# SECTION 1: DESIGN SYSTEM CONTEXT

## Application Identity
MifosSave is a VSLA (Village Savings and Loan Association) group banking app for rural financial communities in Sub-Saharan Africa. The sync-status screen is the offline resilience hub — it shows members and field officers the real-time state of all locally queued data waiting to be committed to the Fineract backend. The design must communicate trust (data is safe), status clarity (green/amber/red), and actionability (retry failed, sync now).

## Material Design 3 Token System

### Color Palette (all hex values exact)

#### Primary — VSLA Green (SYNCED state, Sync Now button)
- primary: #2E7D32
- onPrimary: #FFFFFF
- primaryContainer: #A6F1A6
- onPrimaryContainer: #002106

#### Secondary — Amber (pending indicators, entity badges)
- secondary: #FF8F00
- onSecondary: #FFFFFF
- secondaryContainer: #FFDDB3
- onSecondaryContainer: #2A1700

#### Tertiary — Trust Blue (conflict chip)
- tertiary: #1565C0
- onTertiary: #FFFFFF
- tertiaryContainer: #D2E4FF
- onTertiaryContainer: #001C39

#### Error — Alert Red (FAILED state, failed item badges, retry borders)
- error: #D32F2F
- onError: #FFFFFF
- errorContainer: #FFDAD6
- onErrorContainer: #410002

#### Neutral (backgrounds and surfaces)
- surface: #FAFAFA
- onSurface: #1C1C1C
- surfaceVariant: #DEE5DA
- onSurfaceVariant: #424942
- outline: #727971
- background: #FAFAFA
- onBackground: #1C1C1C

#### Custom semantic status backgrounds (not MD3 roles — custom tokens)
- custom_synced_card_bg: #C8E6C9 (light green — SYNCED status card)
- custom_pending_card_bg: #FFF9C4 (light amber — PENDING status card)
- custom_failed_card_bg: #FFCDD2 (light red — FAILED status card)
- custom_synced_text: #1B5E20 (dark green — SYNCED text)
- custom_pending_text: #E65100 (dark amber — PENDING text)
- custom_failed_text: #D32F2F (error red — FAILED text)
- custom_offline_bg: #FFF9C4 (warning container — offline banner)
- custom_offline_text: #E65100 (warning content text)
- custom_sync_button_disabled: #DEE5DA (surfaceVariant — disabled Sync Now)

### Typography Scale (Noto Sans, scale_style: large — rural accessibility)

| Style | Size (sp) | Weight | Line Height (sp) | Usage |
|-------|-----------|--------|-----------------|-------|
| displayLarge | 57 | 400 | 64 | — |
| displayMedium | 45 | 400 | 52 | — |
| displaySmall | 36 | 400 | 44 | — |
| headlineLarge | 32 | 400 | 40 | — |
| headlineMedium | 28 | 400 | 36 | — |
| headlineSmall | 24 | 400 | 32 | — |
| titleLarge | 22 | 500 | 28 | Screen title in TopAppBar |
| titleMedium | 16 | 500 | 24 | Status card title, section headers |
| titleSmall | 14 | 500 | 20 | Failed section header |
| bodyLarge | 16 | 400 | 24 | — |
| bodyMedium | 14 | 400 | 20 | Entity type labels, last sync text |
| bodySmall | 12 | 400 | 16 | Error messages, subtitle text |
| labelLarge | 14 | 500 | 20 | Sync Now button label |
| labelMedium | 12 | 500 | 16 | Entity type + operation label |
| labelSmall | 11 | 500 | 16 | Conflict chip text, badge text |

### Spacing Scale
| Token | Value (dp) | Usage |
|-------|-----------|-------|
| xxs | 2 | Micro gaps |
| xs | 4 | Chip internal padding |
| sm | 8 | Card internal padding (compact) |
| md | 12 | Row padding vertical |
| lg | 16 | Standard page margin, card padding |
| xl | 24 | Section spacing |
| xxl | 32 | Large gaps |
| 3xl | 48 | — |
| 4xl | 64 | — |

### Shape Scale
| Token | Corner Radius | Usage |
|-------|--------------|-------|
| none | 0dp | Dividers |
| extra_small | 4dp | Small chips |
| small | 8dp | Status cards, failed rows |
| medium | 12dp | Surface cards |
| large | 16dp | Conflict chip (pill) |
| extra_large | 28dp | — |
| full | 9999dp | Badge pills |

### Elevation Scale
| Level | dp | Tonal Overlay Alpha | Usage |
|-------|----|--------------------|-------|
| level_0 | 0dp | 0% | Flat surfaces |
| level_1 | 1dp | 5% | Offline banner |
| level_2 | 3dp | 8% | Pending by type card, TopAppBar |
| level_3 | 6dp | 11% | — |
| level_4 | 8dp | 12% | — |
| level_5 | 12dp | 14% | — |

### Motion Timing
| Token | Duration | Easing | Usage |
|-------|----------|--------|-------|
| short_1 | 50ms | Standard | Immediate feedback |
| short_2 | 100ms | Standard | Badge updates |
| short_3 | 150ms | Standard | — |
| short_4 | 200ms | Standard | Button state transition (online→offline) |
| medium_1 | 250ms | Emphasized | Status card color change |
| medium_2 | 300ms | Emphasized | AnimatedVisibility (syncing progress bar) |
| medium_3 | 350ms | Emphasized | Shimmer cycle |
| medium_4 | 400ms | Decelerated | Screen enter |
| long_1 | 450ms | Decelerated | — |
| long_2 | 500ms | Accelerated | Screen exit |
| shimmer_cycle | 1200ms | Linear | Shimmer pulse alpha 0.3→1.0→0.3 |

### Accessibility Standards
- Minimum touch target: 48dp (Retry button, chips); 56dp (Sync Now button)
- Color contrast ratio: 4.5:1 minimum (WCAG AA)
- All icons paired with text labels (not color alone for status)
- Role annotations for progress indicators and badges
- Content descriptions for all interactive elements

### Breakpoints
| Name | Range | Behavior |
|------|-------|----------|
| compact | 0–599dp | Single column, full-width cards |
| medium | 600–839dp | Single column, 80% width cards centered |
| expanded | 840dp+ | Two-column: status sidebar + details panel |

---

# SECTION 2: SCREEN COMPONENT TREES

## Screen: sync-status

### Full Component Tree (PENDING demo state)

```
SyncStatusScreen (isOnline=true, overallStatus=PENDING, pendingCount=3, failedCount=0)
├── Scaffold
│   ├── TopAppBar
│   │   ├── title: "Sync Status" — titleLarge, onSurface
│   │   ├── actions:
│   │   │   └── IconButton(icon=refresh, onClick=OnRefresh)
│   │   │       ├── size: 48×48dp
│   │   │       └── contentDescription: "Refresh sync status"
│   │   ├── colors: TopAppBarDefaults.topAppBarColors(containerColor=surface)
│   │   └── elevation: 2dp (scrolled)
│   │
│   └── content: LazyColumn(verticalArrangement=spacedBy(16dp), contentPadding=16dp all)
│       │
│       ├── item: OfflineBanner [shown when isOnline=false]
│       │   ├── Row(bg=custom_offline_bg, padding=8dp, cornerRadius=4dp)
│       │   ├── Icon(wifi_off, tint=custom_offline_text, size=16dp)
│       │   ├── Spacer(4dp)
│       │   └── Text("You are offline", bodySmall, custom_offline_text)
│       │
│       ├── item: StatusCard
│       │   ├── Card(bg=custom_pending_card_bg, cornerRadius=8dp, elevation=0dp)
│       │   └── Row(padding=16dp, verticalAlignment=CenterVertically)
│       │       ├── Column(weight=1f)
│       │       │   ├── Row(verticalAlignment=CenterVertically)
│       │       │   │   ├── Icon(circle, size=12dp, tint=custom_pending_text)
│       │       │   │   ├── Spacer(8dp)
│       │       │   │   └── Text("PENDING", titleMedium, custom_pending_text, fontWeight=Bold)
│       │       │   ├── Spacer(4dp)
│       │       │   └── Text("3 items pending sync", bodyMedium, onSurfaceVariant)
│       │       │
│       │       └── Column(horizontalAlignment=End)
│       │           ├── Text("Last sync", labelSmall, onSurfaceVariant)
│       │           └── Text("Yesterday 8:30 AM", bodySmall, onSurfaceVariant)
│       │
│       ├── item: PendingByTypeSection [shown when pendingCount > 0]
│       │   ├── Card(bg=surface, cornerRadius=12dp, elevation=2dp)
│       │   ├── Column(padding=0dp)
│       │   ├── SectionHeader: Text("Pending by Type", titleSmall, onSurfaceVariant, padding=16dp top+horizontal)
│       │   ├── Divider(thickness=1dp, color=outline alpha 0.12)
│       │   ├── PendingTypeRow(entityType=MEETING, count=1)
│       │   │   ├── Row(minHeight=48dp, padding=horizontal 16dp vertical 12dp)
│       │   │   ├── Icon(event_note, size=24dp, tint=onSurfaceVariant)
│       │   │   ├── Spacer(12dp)
│       │   │   ├── Text("Meeting Records", bodyMedium, onSurface, weight=1f)
│       │   │   └── Badge(text="1 pending", bg=secondaryContainer, textColor=onSecondaryContainer, cornerRadius=full)
│       │   ├── Divider(1dp)
│       │   └── PendingTypeRow(entityType=SAVINGS, count=2)
│       │       ├── Row(minHeight=48dp, padding=horizontal 16dp vertical 12dp)
│       │       ├── Icon(savings, size=24dp, tint=onSurfaceVariant)
│       │       ├── Spacer(12dp)
│       │       ├── Text("Savings", bodyMedium, onSurface, weight=1f)
│       │       └── Badge(text="2 pending", bg=secondaryContainer, textColor=onSecondaryContainer)
│       │
│       ├── item: ConflictChip
│       │   └── AssistChip(
│       │       label="0 conflicts",
│       │       containerColor=tertiaryContainer,
│       │       labelColor=tertiary,
│       │       cornerRadius=16dp,
│       │       icon=warning_amber size=16dp
│       │   )
│       │
│       ├── item: FailedOperationsSection [shown when failedCount > 0]
│       │   ├── Card(bg=errorContainer, cornerRadius=8dp)
│       │   ├── SectionHeader: Text("Failed Operations", titleSmall, onErrorContainer)
│       │   └── LazyColumn: FailedOperationRow per item
│       │       ├── Column(padding=12dp vertical, 16dp horizontal)
│       │       ├── Row
│       │       │   ├── Icon(error_outline, 20dp, error)
│       │       │   ├── Spacer(8dp)
│       │       │   └── Text("SAVINGS / CREATE", labelMedium, onErrorContainer, weight=1f)
│       │       ├── Spacer(4dp)
│       │       ├── Text(errorMessage, bodySmall, onSurfaceVariant, maxLines=2)
│       │       ├── Spacer(8dp)
│       │       └── OutlinedButton("Retry", onClick=OnRetryOperation(id), borderColor=onErrorContainer, height=40dp)
│       │
│       └── item: SyncNowButton
│           └── Button(
│               text="Sync Now",
│               icon=upload,
│               enabled=isOnline && !isSyncing,
│               containerColor=if(enabled) primary else #DEE5DA,
│               contentColor=if(enabled) onPrimary else onSurfaceVariant,
│               height=56dp,
│               fillMaxWidth=true,
│               onClick=OnSyncNow
│           )
│           [when isSyncing=true]: CircularProgressIndicator(size=18dp, strokeWidth=2dp, color=onPrimary) replaces icon
│
└── [SyncingProgressBar — AnimatedVisibility when isSyncing=true]
    └── LinearProgressIndicator(
        modifier=fillMaxWidth,
        color=primary,
        trackColor=primaryContainer,
        height=4dp
    )
    [anchored below TopAppBar, above LazyColumn content]
```

---

# SECTION 3: COMPONENT SPECIFICATIONS

## StatusCard

### SYNCED Variant
```
Card
  containerColor: #C8E6C9
  contentColor: #1B5E20
  shape: RoundedCornerShape(8.dp)
  elevation: CardDefaults.cardElevation(0.dp)
  modifier: fillMaxWidth, padding horizontal 0dp (margin handled by LazyColumn)

  Row (padding 16dp, verticalAlignment=CenterVertically)
    Column (weight=1f)
      Row (verticalAlignment=CenterVertically)
        Icon(check_circle_filled, size=20dp, tint=#1B5E20)
        Spacer(8dp)
        Text("SYNCED", titleMedium, #1B5E20, fontWeight=Bold)
      Spacer(4dp)
      Text("All data synced", bodyMedium, onSurfaceVariant)
    
    Column (horizontalAlignment=End)
      Text("Last sync", labelSmall, onSurfaceVariant)
      Text("Today 8:30 AM", bodySmall, onSurfaceVariant)
```

### PENDING Variant
```
  containerColor: #FFF9C4
  Icon: circle (outline), tint=#E65100
  Title: "PENDING", #E65100
  Subtitle: "{count} items pending sync"
```

### FAILED Variant
```
  containerColor: #FFCDD2
  Icon: cancel (filled), tint=#D32F2F
  Title: "FAILED", #D32F2F
  Subtitle: "{count} item(s) failed"
```

## PendingTypeRow

```
Row
  modifier: fillMaxWidth, heightIn(min=48dp), padding(horizontal=16dp, vertical=12dp)
  verticalAlignment: CenterVertically

  Icon
    imageVector: entity-specific (event_note/savings/account_balance_wallet/how_to_vote/pie_chart/person)
    size: 24dp
    tint: onSurfaceVariant #424942

  Spacer(12dp)

  Text
    text: entityType.displayName (Meeting Records / Savings / Attendance / Loan / Share-Out / Member)
    style: bodyMedium
    color: onSurface
    modifier: weight(1f)

  SuggestionChip (or custom Badge)
    label: "{count} pending"
    containerColor: secondaryContainer #FFDDB3
    labelColor: onSecondaryContainer #2A1700
    shape: RoundedCornerShape(full)
    height: 24dp
```

### Entity type display names and icons
| EntityType | Display Name | MD3 Icon |
|------------|-------------|---------|
| MEETING | Meeting Records | event_note |
| SAVINGS | Savings | savings |
| ATTENDANCE | Attendance | how_to_reg |
| LOAN | Loans | account_balance |
| SHARE_OUT | Share-Out | pie_chart |
| MEMBER | Members | person_add |

## FailedOperationRow

```
Column
  modifier: fillMaxWidth, padding(horizontal=16dp, vertical=12dp)
  background: errorContainer #FFDAD6

  Row (verticalAlignment=CenterVertically)
    Icon(error_outline, size=20dp, tint=error #D32F2F)
    Spacer(8dp)
    Text("{entityType} / {operation}", labelMedium, onErrorContainer #410002, weight=1f)

  Spacer(4dp)

  Text
    text: item.errorMessage ?: "Unknown error"
    style: bodySmall
    color: onSurfaceVariant
    maxLines: 2
    overflow: TextOverflow.Ellipsis

  Spacer(8dp)

  OutlinedButton
    text: "Retry"
    onClick: OnRetryOperation(item.id)
    border: BorderStroke(1dp, onErrorContainer #410002)
    contentColor: onErrorContainer
    height: 40dp
    shape: RoundedCornerShape(8dp)
```

## SyncNowButton

```
Button
  modifier: fillMaxWidth, height(56dp)
  shape: RoundedCornerShape(12dp)
  colors: ButtonDefaults.buttonColors(
    containerColor = primary #2E7D32,
    contentColor = onPrimary #FFFFFF,
    disabledContainerColor = #DEE5DA,
    disabledContentColor = onSurfaceVariant #424942
  )
  enabled: isOnline && !isSyncing

  Row (verticalAlignment=CenterVertically, horizontalArrangement=Center)
    if isSyncing:
      CircularProgressIndicator(size=18dp, strokeWidth=2dp, color=onPrimary)
    else:
      Icon(upload, size=18dp)
    Spacer(8dp)
    Text(
      text: if(isSyncing) "Syncing..." else "Sync Now",
      style: labelLarge
    )
```

## SyncingProgressBar

```
AnimatedVisibility(
  visible = isSyncing,
  enter = slideInVertically(initialOffsetY = { -it }) + fadeIn(animationSpec=tween(200)),
  exit = slideOutVertically(targetOffsetY = { -it }) + fadeOut(animationSpec=tween(200))
)
  LinearProgressIndicator
    modifier: fillMaxWidth, height(4dp)
    color: primary #2E7D32
    trackColor: primaryContainer #A6F1A6
    // indeterminate — no progress value since batch size unknown at runtime
```

## ConflictChip

```
SuggestionChip (or FilterChip non-interactive)
  onClick: null (display only)
  label: Text(
    text: if(conflictCount == 0) "0 conflicts" else "$conflictCount conflict(s) detected",
    style: labelSmall,
    color: if(conflictCount > 0) tertiary #1565C0 else onSurfaceVariant
  )
  icon: Icon(warning_amber, size=16dp, tint: same as label)
  shape: RoundedCornerShape(16dp)
  colors: ChipDefaults.suggestionChipColors(
    containerColor = tertiaryContainer #D2E4FF,
    labelColor = tertiary #1565C0
  )
  border: none when conflictCount == 0; 1dp tertiary border when > 0
```

## OfflineBanner

```
AnimatedVisibility(visible = !isOnline)
  Row
    modifier: fillMaxWidth, padding(8dp), background(#FFF9C4), cornerRadius(4dp)
    verticalAlignment: CenterVertically

    Icon(wifi_off, size=16dp, tint=#E65100)
    Spacer(4dp)
    Text(
      text = "You are offline. Data is saved locally.",
      style = bodySmall,
      color = #E65100
    )
```

---

# SECTION 4: INTERACTION FLOWS

## Flow 1: Screen Load (SQLDelight Read)

```
SyncStatusScreen launched (composable enters composition)
  ↓
LaunchedEffect(Unit)
  ↓
viewModel.loadSyncStatus() called on Dispatchers.IO
  ↓
isLoading = true → ShimmerLayout shown (3 shimmer blocks)
  ↓
Parallel reads on SQLDelight:
  ├── sync_queue: COUNT(*) WHERE status='pending' → pendingCount
  ├── sync_queue: COUNT(*) WHERE status='failed' → failedCount
  ├── sync_queue: GROUP BY entity_type WHERE status='pending' → pendingByType
  ├── sync_queue: WHERE status='failed' → failedOperations list
  ├── sync_queue: conflict count query → conflictCount
  └── app_settings: WHERE key='last_synced_at' → lastSyncAt
  ↓
overallStatus computed:
  if failedCount > 0 → FAILED
  else if pendingCount > 0 → PENDING
  else → SYNCED
  ↓
isLoading = false → real UI shown
  ↓
NetworkMonitor.isOnline collected → isOnline updates
```

**Timing**: SQLDelight reads complete in <50ms on modern devices. Total perceived load: <100ms — no shimmer needed in practice but shown for robustness.

## Flow 2: Sync Now

```
User taps "Sync Now" button (isOnline=true, !isSyncing)
  ↓
OnSyncNow action dispatched
  ↓
isSyncing = true
SyncNowButton → "Syncing..." state (spinner)
SyncingProgressBar → AnimatedVisibility enters (200ms slideIn)
  ↓
SyncManager.syncNow() called on Dispatchers.IO
  ↓
Step 1: Read all pending SyncQueueItems from SQLDelight
Step 2: Mark all as in_progress (UPDATE sync_queue SET status='in_progress')
Step 3: Build BatchRequest with one sub-request per item
Step 4: POST /fineract-provider/api/v1/batches
  ↓
Response received:
  for each BatchSubResponse:
    if statusCode in 200..299 → UPDATE SET status='synced' WHERE id=requestId
    if statusCode in 400..499 → UPDATE SET status='failed', error_message=body.defaultUserMessage
    if statusCode >= 500 → UPDATE SET status='pending', retried_at=now
  ↓
app_settings.last_synced_at = now (UTC ISO)
  ↓
isSyncing = false
SyncingProgressBar → AnimatedVisibility exits (200ms slideOut)
  ↓
Re-read SQLDelight → update all counts
  ↓
if all synced → emit SyncCompleted → ShowSnackbar("All items synced successfully")
if partial failure → ShowSnackbar("3 synced, 1 failed — tap to retry")
```

## Flow 3: Retry Failed Item

```
User taps "Retry" on a FailedOperationRow (item.id = 2)
  ↓
OnRetryOperation(itemId=2) action dispatched
  ↓
SQLDelight: UPDATE sync_queue SET status='pending', error_message=NULL WHERE id=2
  ↓
Re-read counts:
  failedCount decrements by 1
  pendingCount increments by 1
  failedOperations list removes item 2
  pendingByType updates entity count
  ↓
overallStatus recomputed:
  if failedCount is now 0 and pendingCount > 0 → PENDING
  ↓
UI animates status card color change: #FFCDD2 → #FFF9C4 (250ms emphasized)
FailedOperationRow animates out (200ms fadeOut)
PendingTypeRow updates badge count (100ms)
  ↓
Retry item now queued — will be included in next Sync Now or auto-sync
```

## Flow 4: Auto-Sync on Connectivity Restore

```
Device transitions from airplane mode to WiFi/mobile
  ↓
NetworkMonitor.isOnline emits true
  ↓
isOnline = true in ViewModel
SyncNowButton transitions: #DEE5DA → primary #2E7D32 (200ms color animation)
OfflineBanner animates out (200ms fadeOut)
  ↓
if pendingCount > 0:
  SyncManager.scheduleImmediateSync() called (WorkManager one-shot)
    ↓
    WorkManager dispatches SyncWorker
    SyncWorker calls SyncManager.syncNow()
    Same flow as Flow 2 above
  ↓
  On completion: Screen observes StateFlow — counts update automatically
```

## Flow 5: Offline Arrival (isOnline changes to false)

```
NetworkMonitor.isOnline emits false
  ↓
isOnline = false
SyncNowButton: enabled=false → color transitions to #DEE5DA (200ms standard)
OfflineBanner: AnimatedVisibility enters (200ms slideIn from top)
  ↓
User taps disabled Sync Now button → no action (button absorbs tap, no ripple)
  ↓
User may still:
  - View pending/failed counts (reads from SQLDelight — no network needed)
  - Tap Retry (marks item as pending in SQLDelight — queued for next auto-sync)
  - Tap Refresh (re-reads SQLDelight — no network needed)
```

## Flow 6: Background Sync Completion (screen is visible)

```
SyncManager background job completes while sync-status screen is active
  ↓
SyncQueueRepository emits updated queue state via Flow
  ↓
ViewModel collects updated counts via collectAsState
  ↓
StatusCard animates to new status color:
  PENDING → SYNCED: card bg #FFF9C4 → #C8E6C9 (250ms emphasized)
  Icon: circle → check_circle_filled (crossfade 200ms)
  Title: "PENDING" → "SYNCED", text color #E65100 → #1B5E20
  ↓
PendingByTypeSection: AnimatedVisibility exit if pendingCount == 0 (200ms)
  ↓
last sync timestamp updates: "Yesterday 8:30 AM" → "Just now"
  ↓
ShowSnackbar("Sync complete — all data saved")
```

---

# SECTION 5: REAL DATA SPECIFICATION

## Demo Sync Queue State

**Scenario**: Mwangaza Women's Group meeting #4 conducted offline (no connectivity). Meeting records, attendance, and savings collections written to SQLDelight SyncQueue. Connectivity now restored — ready to sync.

### sync_queue table contents

| id | entity_type | operation | status | created_at | error_message |
|----|------------|-----------|--------|-----------|---------------|
| 1 | MEETING | CREATE | pending | 2026-05-06T10:15:00Z | null |
| 2 | SAVINGS | CREATE | pending | 2026-05-06T10:15:01Z | null |
| 3 | SAVINGS | CREATE | pending | 2026-05-06T10:15:02Z | null |

### SyncQueueItem details

**Item 1 — Meeting Record (groupId=7, meeting #4)**
```json
{
  "id": 1,
  "entityType": "MEETING",
  "operation": "CREATE",
  "payloadJson": "{\"meeting_number\":4,\"meeting_date\":\"06 May 2026\",\"opening_corpus\":12400.0,\"closing_corpus\":12950.0,\"total_savings_collected\":1050.0,\"total_fines_collected\":50.0,\"total_repayments_collected\":0.0,\"status\":\"completed\",\"locale\":\"en\",\"dateFormat\":\"dd MMMM yyyy\"}",
  "status": "pending",
  "createdAt": "2026-05-06T10:15:00Z",
  "retriedAt": null,
  "errorMessage": null
}
```

**Item 2 — Mary Akinyi savings (savings account id=501)**
```json
{
  "id": 2,
  "entityType": "SAVINGS",
  "operation": "CREATE",
  "payloadJson": "{\"transactionDate\":\"06 May 2026\",\"transactionAmount\":200.0,\"paymentTypeId\":1,\"note\":\"Meeting #4 savings — Mary Akinyi\",\"locale\":\"en\",\"dateFormat\":\"dd MMMM yyyy\"}",
  "status": "pending",
  "createdAt": "2026-05-06T10:15:01Z",
  "retriedAt": null,
  "errorMessage": null
}
```

**Item 3 — John Mwangi savings (savings account id=502)**
```json
{
  "id": 3,
  "entityType": "SAVINGS",
  "operation": "CREATE",
  "payloadJson": "{\"transactionDate\":\"06 May 2026\",\"transactionAmount\":300.0,\"paymentTypeId\":1,\"note\":\"Meeting #4 savings — John Mwangi\",\"locale\":\"en\",\"dateFormat\":\"dd MMMM yyyy\"}",
  "status": "pending",
  "createdAt": "2026-05-06T10:15:02Z",
  "retriedAt": null,
  "errorMessage": null
}
```

### app_settings table
```
key: "last_synced_at"
value: "2026-05-05T08:30:00Z"
last_synced_at: "2026-05-05T08:30:00Z"
```
Displayed as: "Yesterday 8:30 AM" (relative, formatted by DateFormatter using device locale)

### ViewModel state (demo)
```kotlin
SyncStatusUiState(
  isLoading = false,
  isOnline = true,
  isSyncing = false,
  pendingCount = 3,
  failedCount = 0,
  conflictCount = 0,
  overallStatus = SyncOverallStatus.PENDING,
  pendingByType = mapOf(
    EntityType.MEETING to 1,
    EntityType.SAVINGS to 2
  ),
  failedOperations = emptyList(),
  lastSyncAt = Instant.parse("2026-05-05T08:30:00Z")
)
```

### Post-Sync Success State
After successful batch POST, all 3 items updated to synced:
```kotlin
SyncStatusUiState(
  isLoading = false,
  isOnline = true,
  isSyncing = false,
  pendingCount = 0,
  failedCount = 0,
  conflictCount = 0,
  overallStatus = SyncOverallStatus.SYNCED,
  pendingByType = emptyMap(),
  failedOperations = emptyList(),
  lastSyncAt = Instant.parse("2026-05-06T10:15:45Z")  // now
)
```

### Partial Failure Scenario
Item 2 (Mary Akinyi savings) fails with 400 — savings account below minimum balance:
```kotlin
SyncStatusUiState(
  pendingCount = 2,  // items 1 and 3 succeeded and were re-queued? No — only item 2 failed
  // Actually: item 1 synced, item 2 failed, item 3 synced
  pendingCount = 0,
  failedCount = 1,
  conflictCount = 0,
  overallStatus = SyncOverallStatus.FAILED,
  pendingByType = emptyMap(),
  failedOperations = listOf(
    SyncQueueItem(
      id = 2,
      entityType = EntityType.SAVINGS,
      operation = SyncOperation.CREATE,
      status = SyncStatus.failed,
      errorMessage = "The savings account balance cannot go below the minimum balance requirement.",
      retriedAt = Instant.parse("2026-05-06T10:15:45Z")
    )
  ),
  lastSyncAt = Instant.parse("2026-05-06T10:15:45Z")
)
```

### Conflict Detection Example
If both a SAVINGS CREATE (pending) and a SAVINGS CREATE (failed) exist for the same account:
```
conflictCount = 1
ConflictChip displays: "1 conflict detected"
chip border: 1dp tertiary #1565C0
```

---

# SECTION 6: RESPONSIVE LAYOUT + ADAPTIVE BEHAVIOR

## Compact Layout (0–599dp width) — Primary Target

This is the primary device class for rural VSLA members using entry-level Android devices (5–6" screens, 360–393dp width).

```
Screen width: 360dp

TopAppBar: fullWidth, height=56dp
  title: "Sync Status" — left-aligned
  refresh icon: right 12dp margin

LazyColumn
  contentPadding: PaddingValues(horizontal=16dp, vertical=16dp)
  verticalArrangement: spacedBy(16dp)

StatusCard: fillMaxWidth, height=min 80dp
PendingByTypeSection: fillMaxWidth
ConflictChip: wrapContent (left-aligned)
FailedOperationsSection: fillMaxWidth
SyncNowButton: fillMaxWidth, height=56dp
```

### Compact Typography Adjustments
No font size changes — scale_style=large already optimized for rural readability.

### Compact Touch Targets
- All rows: minHeight=48dp enforced
- Retry button: height=40dp (meets minimum in context with row padding)
- Sync Now: 56dp (primary CTA, exceeds minimum)

## Medium Layout (600–839dp width) — Tablet / Large Phone

```
Screen width: 720dp

LazyColumn
  contentPadding: PaddingValues(horizontal=80dp, vertical=24dp)
  // Cards centered with 80dp margins on each side = 560dp card width

StatusCard: maxWidth=560dp, centered
PendingByTypeSection: maxWidth=560dp
ConflictChip: wrapContent, centered
SyncNowButton: maxWidth=560dp, height=56dp
```

## Expanded Layout (840dp+) — Field Officer Tablet, Desktop

```
Screen width: 1024dp

Row (fillMaxWidth)
  ├── Column (weight=0.4f, padding=24dp) — LEFT: Status Summary Panel
  │   ├── StatusCard (fillMaxWidth)
  │   ├── Spacer(16dp)
  │   ├── ConflictChip
  │   ├── Spacer(24dp)
  │   └── SyncNowButton (fillMaxWidth)
  │
  └── Column (weight=0.6f, padding=24dp) — RIGHT: Details Panel
      ├── PendingByTypeSection (fillMaxWidth)
      ├── Spacer(16dp)
      └── FailedOperationsSection (fillMaxWidth, scrollable)
```

## Dark Theme Mappings

All custom status card backgrounds shift to darker tonal equivalents:

| Light Token | Dark Equivalent | Value |
|------------|----------------|-------|
| #C8E6C9 (SYNCED bg) | primaryContainer | #A6F1A6 (already dark-safe) |
| #FFF9C4 (PENDING bg) | tertiaryContainer dark | #3A3000 (deep amber dark) |
| #FFCDD2 (FAILED bg) | errorContainer | #410002 (deep red dark) |
| surface #FAFAFA | surface dark | #1C1C1E |
| onSurface #1C1C1C | onSurface dark | #E6E1E5 |
| outline #727971 | outline dark | #8C9388 |

Dark theme Sync Now button: primary #2E7D32 remains (sufficient contrast on #1C1C1E surface).

## RTL Support (Arabic, Urdu — future)

All Row children use `Arrangement.Start` / `Alignment.Start` so RTL mirrors correctly:
- Status icon: leading (becomes trailing in RTL)
- Last sync timestamp: trailing (becomes leading in RTL)
- Retry button: trailing (becomes leading in RTL)
- Offline icon + text: leading + text follows (correct in both directions)

## Bottom Navigation Integration

sync-status appears in the bottom navigation bar with:
```kotlin
NavigationBarItem(
  icon = { BadgedBox(
    badge = {
      if (failedCount > 0) Badge() // red dot, no number
    }
  ) { Icon(Icons.Outlined.Sync, "Sync") } },
  label = { Text("Sync") },
  selected = currentRoute == "sync-status"
)
```

Badge: shown when failedCount > 0 (data failure requires attention). Not shown for pending-only state (normal offline operation).

## Loading State Shimmer Detail

```kotlin
@Composable
fun SyncStatusShimmer() {
  Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
    // Status card shimmer
    ShimmerBox(modifier = Modifier.fillMaxWidth().height(80.dp).clip(RoundedCornerShape(8.dp)))

    // Pending by type card shimmer
    ShimmerBox(modifier = Modifier.fillMaxWidth().height(120.dp).clip(RoundedCornerShape(12.dp)))

    // Sync now button shimmer
    ShimmerBox(modifier = Modifier.fillMaxWidth().height(56.dp).clip(RoundedCornerShape(12.dp)))
  }
}

// ShimmerBox: animates alpha 0.3 → 1.0 → 0.3 over 1200ms using infiniteTransition
// color: surfaceVariant #DEE5DA
```

## Snackbar Messages

| Event | Message | Duration |
|-------|---------|----------|
| SyncCompleted (all synced) | "All items synced successfully" | short (4s) |
| SyncCompleted (partial) | "{n} synced, {m} failed — tap Retry to fix" | long (8s) |
| SyncCompleted (all failed) | "Sync failed — check connection and retry" | long (8s) |
| RetryOperation queued | "Item queued for retry" | short (4s) |
| OnRefresh completed | "Status refreshed" | short (4s) |

Snackbar position: above bottom navigation bar (using Scaffold's snackbarHost).

## Performance Notes

- SQLDelight reads always on `Dispatchers.IO` — never on main thread
- NetworkMonitor: `callbackFlow` wrapping `ConnectivityManager.NetworkCallback`
- SyncManager: `WorkManager` `CoroutineWorker` with exponential backoff (delay: 30s, 2m, 10m, max 1h)
- StateFlow: `stateIn(scope, SharingStarted.WhileSubscribed(5000), initialState)` — auto-cancels when screen leaves composition
- No pagination needed: SyncQueue is bounded (cleared when synced; failed operations expected <100 items)

---

# SECTION 7: COMPONENT STATE MATRIX

## SyncStatusCard (top-level sync state indicator)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| SyncStatusCard | ALL_SYNCED | primaryContainer (#A6F1A6) | onPrimaryContainer (#002106) | primary 1dp (#2E7D32) | elevation 1dp | true | true |
| SyncStatusCard | SYNCING | secondaryContainer (#FFDDB3) | onSecondaryContainer (#2A1700) | secondary 1dp (#FF8F00) | elevation 1dp | false | true |
| SyncStatusCard | PENDING | secondaryContainer (#FFDDB3) | onSecondaryContainer (#2A1700) | secondary 2dp (#FF8F00) | elevation 1dp | true | true |
| SyncStatusCard | FAILED | errorContainer (#FFDAD6) | onErrorContainer (#410002) | error 2dp (#D32F2F) | elevation 1dp | true | true |
| SyncStatusCard | OFFLINE | surfaceVariant (#DEE5DA) | onSurfaceVariant (#424942) | outline 1dp (#727971) | elevation 0dp | true | true |
| SyncStatusCard | loading | surfaceVariant (#DEE5DA) shimmer | onSurfaceVariant (#424942) | none | elevation 0dp | false | true |

## SyncQueueItem Row

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| SyncQueueItemRow | PENDING | surface (#FAFAFA) | onSurface (#1C1C1C) | left accent 4dp secondary (#FF8F00) | none | true | true |
| SyncQueueItemRow | SYNCING | primaryContainer (#A6F1A6) 20% alpha | onSurface (#1C1C1C) | left accent 4dp primary (#2E7D32) | none | false | true |
| SyncQueueItemRow | SYNCED | surface (#FAFAFA) | onSurfaceVariant (#424942) | none | none | false | true |
| SyncQueueItemRow | FAILED | errorContainer (#FFDAD6) 30% alpha | onErrorContainer (#410002) | left accent 4dp error (#D32F2F) | none | true | true |
| SyncQueueItemRow | CONFLICT | tertiaryContainer (#D2E4FF) 30% alpha | onTertiaryContainer (#001C39) | left accent 4dp tertiary (#1565C0) | none | true | true |
| SyncQueueItemRow | pressed | surfaceVariant (#DEE5DA) | onSurface (#1C1C1C) | none | none | true | true |
| SyncQueueItemRow | focused | surface (#FAFAFA) | onSurface (#1C1C1C) | primary 2dp focus ring | none | true | true |
| SyncQueueItemRow | disabled | surfaceVariant (#DEE5DA) | onSurfaceVariant 38% alpha | none | none | false | true |

## Retry Button (per failed item)

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| RetryButton | default | error (#D32F2F) | onError (#FFFFFF) | none | elevation 1dp | true | true |
| RetryButton | pressed | errorContainer (#FFDAD6) | onErrorContainer (#410002) | error 2dp | elevation 0dp | true | true |
| RetryButton | focused | error (#D32F2F) | onError (#FFFFFF) | white 3dp focus ring | elevation 1dp | true | true |
| RetryButton | loading | errorContainer (#FFDAD6) | onErrorContainer 60% | none | none | false | true |
| RetryButton | disabled | surfaceVariant (#DEE5DA) | onSurfaceVariant 38% alpha | none | none | false | true |
| RetryButton | success | primaryContainer (#A6F1A6) | onPrimaryContainer (#002106) | none | none | false | true |

## Sync Now FAB

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| SyncNowFAB | default (online) | primary (#2E7D32) | onPrimary (#FFFFFF) | none | elevation 6dp | true | true |
| SyncNowFAB | pressed | primaryContainer (#A6F1A6) | onPrimaryContainer (#002106) | none | elevation 2dp | true | true |
| SyncNowFAB | focused | primary (#2E7D32) | onPrimary (#FFFFFF) | white 3dp focus ring | elevation 6dp | true | true |
| SyncNowFAB | syncing | primaryContainer (#A6F1A6) | onPrimaryContainer (#002106) | none | elevation 4dp | false | true |
| SyncNowFAB | offline | surfaceVariant (#DEE5DA) | onSurfaceVariant 38% alpha | none | elevation 0dp | false | true |
| SyncNowFAB | disabled | surfaceVariant (#DEE5DA) | onSurfaceVariant 38% alpha | none | elevation 0dp | false | true |

## Connectivity Banner

| Component | State | Background | Text/Icon Color | Border | Shadow | Enabled | Visible |
|-----------|-------|------------|-----------------|--------|--------|---------|---------|
| ConnectivityBanner | offline | secondaryContainer (#FFDDB3) | onSecondaryContainer (#2A1700) | none | elevation 2dp | N/A | true |
| ConnectivityBanner | back_online | primaryContainer (#A6F1A6) | onPrimaryContainer (#002106) | none | elevation 2dp | N/A | true |
| ConnectivityBanner | hidden | — | — | — | — | — | false |

---

# SECTION 8: API FAILURE & RECOVERY PLAYBOOK

## SQLDelight Local Queue Operations

The offline-sync feature is primarily local — the SyncQueue lives in SQLDelight. Remote API failures trigger queue state updates.

## Endpoint: POST /savingsaccounts/{accountId}/transactions (queued contribution)

| Failure | UX Response | Recovery |
|---------|-------------|----------|
| Network timeout | Mark item PENDING in SyncQueue; SyncStatusCard stays PENDING | Exponential backoff: 30s → 2m → 10m via WorkManager; max 3 auto-retries |
| 401 Unauthorized | Navigate to LoginScreen; preserve SyncQueue (do not clear) | Post-login, auto-resume SyncQueue drain |
| 404 Not Found | Mark item FAILED; error badge on SyncQueueItemRow | Manual retry button; shows dialog "Account not found — contact administrator" |
| 500 Server Error | Mark item FAILED after 3 attempts; snackbar "Sync failed — tap Retry to fix" | Manual retry via per-item RetryButton or global "Retry All" action |
| Offline | Item stays PENDING; ConnectivityBanner shows; SyncNowFAB disabled | Auto-retry when NetworkMonitor emits Connected; no user action required |
| Conflict (409) | Mark item CONFLICT; chip with Icons.Outlined.Warning + tertiary blue | Dialog: "Conflict detected — data was changed on server. View server version or keep local?" |

## Endpoint: GET /syncstatus (global sync state)

| Failure | UX Response | Recovery |
|---------|-------------|----------|
| Network timeout | Use local SQLDelight counts (PENDING/FAILED items) as proxy | Retry silently: 1s → 2s → 4s; SyncStatusCard shows local state |
| 401 Unauthorized | Navigate to LoginScreen | Standard auth recovery |
| 404 Not Found | Assume clean slate; log `sync_status_404` | No user-visible impact |
| 500 Server Error | SyncStatusCard shows local-computed state only; no error shown | Background retry every 60s |
| Offline | SyncStatusCard switches to OFFLINE state; local queue counts shown | Auto-refresh on reconnect |

## Endpoint: POST /loans/{loanId}/repayments (queued loan repayment)

| Failure | UX Response | Recovery |
|---------|-------------|----------|
| Network timeout | Queue to SyncQueue type=LOAN_REPAYMENT | Backoff retry; show "Peter Otieno — loan repayment KES 2,500 queued" in SyncQueue |
| 422 Validation | Mark FAILED; inline detail "Amount exceeds due installment KES 1,800" | User must edit amount; surfaced via SyncQueueItemRow expand → Edit Amount action |
| 500 Server Error | Mark FAILED; snackbar "Loan repayment failed. Will retry automatically." | WorkManager retry with REPLACE |
| Offline | Immediate queue with optimistic "Payment recorded offline" confirmation | Auto-sync on reconnect |

## SyncQueue Drain Protocol (detailed)

```
NetworkMonitor emits CONNECTED →
  1. SyncManager.drainQueue() called on Dispatchers.IO
  2. Query: SELECT * FROM sync_queue WHERE status = 'PENDING' OR status = 'FAILED' AND retry_count < 3 ORDER BY created_at ASC
  3. For each item in result:
     a. Mark status = 'SYNCING' → emit to StateFlow<SyncState>
     b. Execute remote API call
     c. Success: mark status = 'SYNCED', update entity in local DB, emit SyncItemResult.Success
     d. Failure (4xx non-401): mark status = 'FAILED', increment retry_count, emit SyncItemResult.Failure
     e. Failure (401): pause drain, navigate to login, resume post-login
     f. Failure (5xx): mark status = 'FAILED' if retry_count >= 3, else re-queue with backoff
  4. After full drain: emit SyncResult.Complete(synced=n, failed=m)
  5. Trigger NotificationManager if failed > 0: "Sync incomplete — {m} items need attention"
```

---

# SECTION 9: SCREEN READER & ACCESSIBILITY DEEP DIVE

## SyncStatus Screen — Focus Order

1. TopAppBar title "Sync Status" — role = Heading
2. ConnectivityBanner (if visible) — liveRegion = Assertive; "You are offline. {n} items pending sync."
3. SyncStatusCard — role = Status; contentDescription = "All synced" / "Syncing {n} items" / "{n} items pending" / "{n} items failed" / "Offline — {n} items queued"
4. "Sync Now" FAB (if online and pending items exist) — role = Button; "Sync {n} pending items now"
5. SyncQueue section header — role = Heading level 2; "Pending Sync Items, {n} total"
6. SyncQueueItemRow 1 (e.g. Mary Akinyi — contribution) — contentDescription = "Mary Akinyi — KES 500 group contribution, status: pending, created 5 minutes ago"
7. SyncQueueItemRow 2 (e.g. Peter Otieno — loan repayment) — contentDescription = "Peter Otieno — KES 2,500 loan repayment, status: failed, tap to retry"
8. RetryButton (per failed item) — "Retry sync for {entity_type} — {member_name}"
9. "Failed Items" section header (if any failed) — role = Heading level 2
10. "Retry All Failed" button — role = Button; "Retry all {n} failed sync items"
11. Bottom Navigation Bar items

## TalkBack Announcement Strings

| Element | TalkBack String |
|---------|----------------|
| SyncStatusCard (ALL_SYNCED) | "All items are synced. No pending operations." |
| SyncStatusCard (PENDING) | "{n} items are waiting to sync. Tap Sync Now to upload." |
| SyncStatusCard (SYNCING) | "Syncing {n} items. Please wait." (liveRegion = Polite) |
| SyncStatusCard (FAILED) | "{n} sync items failed. Double-tap Retry All to try again." (liveRegion = Assertive) |
| SyncStatusCard (OFFLINE) | "You are offline. {n} items are saved and will sync when you reconnect." |
| ConnectivityBanner (offline) | "Connection lost. Changes will sync automatically when reconnected." |
| ConnectivityBanner (back online) | "Connection restored. Syncing your saved changes now." |
| SyncQueueItemRow (PENDING) | "{member_name} — {operation_type} KES {amount}, pending, created {relative_time}" |
| SyncQueueItemRow (FAILED) | "{member_name} — {operation_type} KES {amount}, sync failed, double-tap to retry" |
| SyncQueueItemRow (CONFLICT) | "{member_name} — {operation_type}, conflict detected, double-tap to resolve" |
| SyncQueueItemRow (SYNCED) | "{member_name} — {operation_type}, synced successfully" |
| RetryButton | "Retry sync for {member_name}'s {operation_type}" |
| SyncNowFAB | "Sync {n} pending items now" |

## Content Descriptions — All Icons

| Icon | Composable | contentDescription |
|------|-----------|-------------------|
| Icons.Outlined.Sync | SyncNowFAB | "Sync pending items" |
| Icons.Outlined.CheckCircle | SyncStatusCard (ALL_SYNCED) | "All synced" |
| Icons.Outlined.Schedule | SyncQueueItemRow (PENDING) | "Pending sync" |
| Icons.Outlined.ErrorOutline | SyncQueueItemRow (FAILED) | "Sync failed" |
| Icons.Outlined.Warning | SyncQueueItemRow (CONFLICT) | "Conflict detected" |
| Icons.Outlined.CloudOff | ConnectivityBanner / SyncStatusCard (OFFLINE) | "Offline" |
| Icons.Outlined.CloudDone | SyncStatusCard (ALL_SYNCED) | "Cloud synced" |
| Icons.Outlined.Replay | RetryButton | "Retry" |
| Icons.Outlined.SyncProblem | SyncStatusCard (FAILED) | "Sync problem" |
| Icons.Outlined.WifiOff | ConnectivityBanner | "No internet connection" |

## Live Region Announcements

```kotlin
// SyncStatusCard — announces on state changes
SyncStatusCard(
    modifier = Modifier.semantics {
        liveRegion = LiveRegionMode.Polite
        contentDescription = syncStateDescription(syncState)
    }
)

// ConnectivityBanner — immediate announcement on connectivity change
ConnectivityBanner(
    modifier = Modifier.semantics {
        liveRegion = LiveRegionMode.Assertive  // Interrupts current announcement
    }
)

// Snackbar on sync complete
LaunchedEffect(syncResult) {
    if (syncResult is SyncResult.Complete) {
        snackbarHostState.showSnackbar(
            message = if (syncResult.failed == 0)
                "All items synced successfully"
            else
                "${syncResult.synced} synced, ${syncResult.failed} failed — tap Retry to fix"
        )
    }
}
```

## WCAG AA Contrast Ratios

| Foreground | Background | Ratio | Pass AA |
|------------|------------|-------|---------|
| onPrimary #FFFFFF | primary #2E7D32 | 7.1:1 | Pass (AA + AAA) |
| onPrimaryContainer #002106 | primaryContainer #A6F1A6 | 8.2:1 | Pass (AA + AAA) |
| onSecondaryContainer #2A1700 | secondaryContainer #FFDDB3 | 9.4:1 | Pass (AA + AAA) |
| onErrorContainer #410002 | errorContainer #FFDAD6 | 12.4:1 | Pass (AA + AAA) |
| onError #FFFFFF | error #D32F2F | 4.5:1 | Pass (AA) |
| onTertiaryContainer #001C39 | tertiaryContainer #D2E4FF | 10.2:1 | Pass (AA + AAA) |
| onSurface #1C1C1C | surface #FAFAFA | 16.1:1 | Pass (AA + AAA) |
| onSurfaceVariant #424942 | surfaceVariant #DEE5DA | 5.9:1 | Pass (AA) |

## Color-Blind Safe Status States

All SyncQueue states use BOTH color AND icon/shape (never color alone):
- ALL_SYNCED: green (#2E7D32) + Icons.Outlined.CheckCircle (circle with checkmark)
- PENDING: amber (#FF8F00) + Icons.Outlined.Schedule (clock face)
- SYNCING: green animated + Icons.Outlined.Sync (rotating arrows)
- FAILED: red (#D32F2F) + Icons.Outlined.ErrorOutline (circle with !)
- CONFLICT: blue (#1565C0) + Icons.Outlined.Warning (triangle with !)
- OFFLINE: grey (#727971) + Icons.Outlined.CloudOff (cloud with slash)

---

# SECTION 10: ANIMATION & MOTION SPEC

## Screen Enter / Exit Animations

| Screen | Enter | Exit |
|--------|-------|------|
| SyncStatusScreen | fadeIn(tween(250)) + slideInVertically(+60px → 0, tween(300, EaseOutCubic)) | fadeOut(tween(200)) |
| ConflictResolutionDialog | scaleIn(0.88 → 1.0, tween(300, EmphasizedDecelerate)) + fadeIn(300ms) | scaleOut(1.0 → 0.88, 200ms) + fadeOut(200ms) |
| SyncQueueItemRow expansion | animateContentSize(tween(250, EaseInOutCubic)) | same |

## SyncStatusCard State Transition Animations

| Transition | Duration | Easing |
|------------|----------|--------|
| PENDING → SYNCING | background color fade 300ms | FastOutSlowIn |
| SYNCING → ALL_SYNCED | background color fade 400ms + checkmark path draw 500ms | EaseOutCubic |
| SYNCING → FAILED | background color fade 300ms + shake animation 400ms (±4dp, 3 cycles) | LinearEasing |
| ANY → OFFLINE | fade 200ms to grey state | LinearEasing |
| OFFLINE → PENDING | fade 200ms from grey + slide banner down 200ms | EaseOutCubic |

## Loading Skeleton Shimmer (SyncQueue list)

```kotlin
val shimmerColors = listOf(
    surfaceVariant.copy(alpha = 0.9f),
    surfaceVariant.copy(alpha = 0.3f),
    surfaceVariant.copy(alpha = 0.9f),
)
// Gradient angle: 270° (left → right)
// Duration: 1200ms per cycle
// Applied to: 3 placeholder SyncQueueItemRow skeletons during initial load
// Shimmer width: 80% of row width
```

## SyncNowFAB Progress Animation

```kotlin
// While syncing: rotate icon 360° continuously
val rotation by animateFloatAsState(
    targetValue = if (isSyncing) 360f else 0f,
    animationSpec = if (isSyncing)
        infiniteRepeatable(tween(800, easing = LinearEasing))
    else
        tween(0)
)
Icon(
    imageVector = Icons.Outlined.Sync,
    modifier = Modifier.rotate(rotation)
)
```

## ConnectivityBanner Enter / Exit

- Enter: `slideInVertically(initialOffsetY = { -it }, tween(200, EaseOutCubic))`
- Exit: `slideOutVertically(targetOffsetY = { -it }, tween(150, EaseInCubic))`
- Back-online banner: auto-dismisses after 3s with `fadeOut(tween(300))`

## Pull-to-Refresh Spec (SyncQueue list)

```kotlin
PullRefreshIndicator(
    refreshing = isRefreshingStatus,
    state = pullRefreshState,
    // Color: primary #2E7D32
    // Background: surface #FAFAFA
    // Threshold: 64dp
    // Scale in: animateFloatAsState 0f → 1f, 200ms EaseOutBack
)
// Refresh action: re-query SyncQueue from SQLDelight + attempt GET /syncstatus
```

---

# SECTION 11: TEST & QA ANNOTATIONS

## UI Test Tags

| Composable | testTag |
|-----------|---------|
| SyncStatusScreen root | `"SyncStatusScreen"` |
| SyncStatusCard | `"SyncStatusCard"` |
| SyncStatusCard (ALL_SYNCED) | `"SyncStatusCard_AllSynced"` |
| SyncStatusCard (PENDING) | `"SyncStatusCard_Pending"` |
| SyncStatusCard (SYNCING) | `"SyncStatusCard_Syncing"` |
| SyncStatusCard (FAILED) | `"SyncStatusCard_Failed"` |
| SyncStatusCard (OFFLINE) | `"SyncStatusCard_Offline"` |
| ConnectivityBanner (offline) | `"ConnectivityBanner_Offline"` |
| ConnectivityBanner (online) | `"ConnectivityBanner_BackOnline"` |
| SyncNowFAB | `"SyncNowFAB"` |
| SyncQueueList | `"SyncQueueList"` |
| SyncQueueItemRow (by id) | `"SyncQueueItemRow_{operationId}"` |
| RetryButton (per item) | `"RetryButton_{operationId}"` |
| RetryAllButton | `"RetryAllButton"` |
| ConflictResolutionDialog | `"ConflictResolutionDialog"` |
| ConflictKeepLocal | `"ConflictResolution_KeepLocal"` |
| ConflictUseServer | `"ConflictResolution_UseServer"` |
| EmptyState (all synced) | `"SyncQueue_EmptyState"` |

## Required Test Scenarios

### Screen: SyncStatusScreen — Online / Synced

**Given** the user has no pending items in SyncQueue  
**When** the SyncStatus screen loads  
**Then** SyncStatusCard shows ALL_SYNCED state with green background, checkmark icon, and text "All items synced successfully"

---

**Given** the user has 3 PENDING items (Grace Mwangi — contribution, Mary Akinyi — savings, Peter Otieno — repayment)  
**When** the SyncStatus screen loads online  
**Then** SyncStatusCard shows PENDING state; SyncQueueList shows 3 rows in amber left-border style; SyncNowFAB is enabled

---

**Given** the user taps SyncNowFAB  
**When** the sync operation completes successfully  
**Then** SyncStatusCard transitions to ALL_SYNCED; SyncQueueList shows SYNCED rows with muted styling; snackbar "All items synced successfully" appears

---

**Given** one item in SyncQueue returns HTTP 500 during sync  
**When** the sync operation completes  
**Then** that item shows FAILED state with red left-border and RetryButton visible; snackbar shows "1 synced, 1 failed — tap Retry to fix"

---

**Given** a CONFLICT item is in the queue (item was modified on server since last sync)  
**When** the user taps the conflict row  
**Then** ConflictResolutionDialog appears with two options: "Keep my changes" and "Use server version"

### Screen: SyncStatusScreen — Offline

**Given** the device has no network connection  
**When** the SyncStatus screen is opened  
**Then** ConnectivityBanner shows "Offline — {n} items queued"; SyncNowFAB is disabled (grey); SyncStatusCard shows OFFLINE state

---

**Given** the device is offline with 5 items in queue  
**When** network is restored  
**Then** ConnectivityBanner changes to "Connection restored. Syncing now."; SyncNowFAB becomes enabled; auto-drain begins within 2s

---

**Given** there are 50+ items in the SyncQueue  
**When** the SyncQueue list renders  
**Then** list is scrollable (LazyColumn); all items are reachable; no frame drops during fast scroll (target: <3 dropped frames on Pixel 4a equivalent)

## Edge Cases

- Empty queue (0 items): EmptyState shows "Nothing to sync — you're all up to date" with checkmark illustration
- Single item that keeps failing (retry_count = 3): item permanently marked FAILED; no more auto-retries; manual retry still works
- 50+ character operation descriptions: truncated at 2 lines with ellipsis; full text in expanded view
- Item created while offline, then device back online before user opens sync screen: auto-drain starts, item never shows PENDING in UI (transitions straight to SYNCED)
- Amara Diallo contribution of KES 0 (edge): validation prevents KES 0 from entering queue — not an offline-sync edge case

---

# SECTION 12: i18n / LOCALIZATION SPEC

## String Keys with Translations

| Key | EN | SW (Swahili) | FR (French) |
|-----|----|--------------|-------------|
| `sync_screen_title` | "Sync Status" | "Hali ya Usawazishaji" | "État de Synchronisation" |
| `sync_status_all_synced` | "All items synced" | "Vitu vyote vinachanganywa" | "Tous les éléments synchronisés" |
| `sync_status_pending` | "{n} items pending sync" | "Vitu {n} vinasubiri usawazishaji" | "{n} éléments en attente de sync" |
| `sync_status_syncing` | "Syncing {n} items…" | "Inasawazisha vitu {n}…" | "Synchronisation de {n} éléments…" |
| `sync_status_failed` | "{n} items failed to sync" | "Vitu {n} havikuweza kusawazishwa" | "{n} éléments n'ont pas pu se synchroniser" |
| `sync_status_offline` | "Offline — {n} items queued" | "Nje ya mtandao — vitu {n} vimepakuliwa" | "Hors ligne — {n} éléments en file" |
| `sync_connectivity_offline` | "No internet connection. Changes saved locally." | "Hakuna mtandao. Mabadiliko yamehifadhiwa." | "Pas de connexion. Modifications sauvegardées." |
| `sync_connectivity_restored` | "Connection restored. Syncing now." | "Mtandao umepatikana. Inasawazisha sasa." | "Connexion rétablie. Synchronisation en cours." |
| `sync_now_button` | "Sync Now" | "Sawazisha Sasa" | "Synchroniser Maintenant" |
| `sync_retry_button` | "Retry" | "Jaribu Tena" | "Réessayer" |
| `sync_retry_all_button` | "Retry All Failed" | "Jaribu Tena Zote Zilizoshindwa" | "Réessayer Tout ce qui a Échoué" |
| `sync_queue_empty` | "Nothing to sync — you're all up to date" | "Hakuna cha kusawazisha — umesasishwa" | "Rien à synchroniser — tout est à jour" |
| `sync_item_contribution` | "Group contribution — {name}" | "Mchango wa kikundi — {name}" | "Contribution groupe — {name}" |
| `sync_item_savings` | "Individual savings — {name}" | "Akiba ya kibinafsi — {name}" | "Épargne individuelle — {name}" |
| `sync_item_repayment` | "Loan repayment — {name}" | "Malipo ya mkopo — {name}" | "Remboursement prêt — {name}" |
| `sync_item_attendance` | "Attendance record — {date}" | "Rekodi ya mahudhurio — {date}" | "Relevé de présence — {date}" |
| `sync_conflict_title` | "Sync Conflict" | "Mgongano wa Usawazishaji" | "Conflit de Synchronisation" |
| `sync_conflict_body` | "This item was changed on the server. Keep your local changes or use the server version?" | "Kipengele hiki kimebadilishwa kwenye seva. Hifadhi mabadiliko yako au tumia toleo la seva?" | "Cet élément a été modifié sur le serveur. Garder vos modifications locales ou utiliser la version du serveur ?" |
| `sync_conflict_keep_local` | "Keep my changes" | "Hifadhi mabadiliko yangu" | "Garder mes modifications" |
| `sync_conflict_use_server` | "Use server version" | "Tumia toleo la seva" | "Utiliser la version serveur" |
| `sync_snackbar_complete_success` | "All items synced successfully" | "Vitu vyote vinachanganywa" | "Tous les éléments synchronisés" |
| `sync_snackbar_partial` | "{n} synced, {m} failed — tap Retry to fix" | "{n} imesawazishwa, {m} imeshindwa — gusa Jaribu Tena" | "{n} synchronisés, {m} échoués — appuyez sur Réessayer" |
| `sync_snackbar_all_failed` | "Sync failed — check connection and retry" | "Usawazishaji umeshindwa — angalia mtandao na ujaribu tena" | "Synchronisation échouée — vérifiez la connexion et réessayez" |

## Number Formatting — KES

All amounts in SyncQueueItemRows use en-KE locale:

| Amount | Formatted |
|--------|-----------|
| 500 | KES 500.00 |
| 2500 | KES 2,500.00 |
| 48500 | KES 48,500.00 |
| 1234.5 | KES 1,234.50 |

```kotlin
val numberFormat = NumberFormat.getCurrencyInstance(Locale("en", "KE"))
fun formatKES(amount: Double): String = numberFormat.format(amount)
// Result: "KES 2,500.00"
```

## Date Formatting — en-KE Locale

| Format | Pattern | Example |
|--------|---------|---------|
| Sync item created | relative | "5 minutes ago" / "dakika 5 zilizopita" |
| Sync item created (>24h) | dd/MM/yyyy | 05/05/2026 |
| Last synced timestamp | "d MMM yyyy, HH:mm" | "5 May 2026, 14:30" |
| Last synced (today) | "Today at HH:mm" | "Today at 14:30" |

```kotlin
fun formatRelativeTime(createdAt: Instant, now: Instant, locale: Locale): String {
    val diffMinutes = Duration.between(createdAt, now).toMinutes()
    return when {
        diffMinutes < 1 -> stringResource(R.string.sync_time_just_now)
        diffMinutes < 60 -> stringResource(R.string.sync_time_minutes_ago, diffMinutes)
        diffMinutes < 1440 -> stringResource(R.string.sync_time_hours_ago, diffMinutes / 60)
        else -> DateTimeFormatter.ofPattern("dd/MM/yyyy", locale).format(createdAt.atZone(ZoneId.systemDefault()))
    }
}
```

## Plural Rules (Swahili)

Swahili has no grammatical plural distinction for most nouns — use same form for 1 and many:
- "Vitu 1 vinasubiri" (1 item pending) — same structure as "Vitu 3 vinasubiri"
- Use `{n}` placeholder and do not apply English-style s/es suffix logic
- Android plurals resource: use `other` quantity for all Swahili counts
