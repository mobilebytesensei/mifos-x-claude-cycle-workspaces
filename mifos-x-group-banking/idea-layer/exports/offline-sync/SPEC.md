# Offline Sync — Feature Specification
**Project**: CommonPurse (mifos-x-group-banking)
**Feature ID**: offline-sync
**Requirement**: FR-008
**Version**: 1.0.0
**Status**: enriched

---

## Overview

CommonPurse operates fully offline using SQLDelight as a local database. Every write operation (meeting records, savings transactions, loan repayments, attendance, share-out) is first written to a local SyncQueue table and then synced to Fineract when connectivity is restored. The sync-status screen provides a real-time view of pending, failed, and conflicting queue items sourced exclusively from the local SQLDelight database — no network call on load.

---

## Acceptance Criteria

- **FR-008**: All group banking operations (meetings, savings, loans, attendance, share-out) work with no internet connection. Data is stored in SQLDelight and queued for sync. When connectivity is restored, a SyncManager background job processes the SyncQueue using the Fineract batch API (`POST /batches`). The sync-status screen shows overall status (SYNCED/PENDING/FAILED), pending count by entity type, failed operations with per-item retry, last sync timestamp, and a manual "Sync Now" button (disabled when offline). Conflict detection is supported with a conflict counter.

---

## Screens Table

| Screen ID | Route | Type | Role |
|-----------|-------|------|------|
| sync-status | /sync-status | dashboard | Both (admin + end user) |

---

## State Model

### SyncStatusViewModel
| Field | Type | Default |
|-------|------|---------|
| isOnline | Boolean | false |
| pendingCount | Int | 0 |
| failedCount | Int | 0 |
| lastSyncAt | Instant? | null |
| isSyncing | Boolean | false |
| pendingByType | Map<EntityType, Int> | emptyMap() |
| failedOperations | List<SyncQueueItem> | emptyList() |
| conflictCount | Int | 0 |
| overallStatus | SyncOverallStatus | SYNCED |
| isLoading | Boolean | true |

**Overall status logic**:
- SYNCED: `pendingCount == 0 && failedCount == 0`
- PENDING: `pendingCount > 0`
- FAILED: `failedCount > 0`

**Actions**: OnSyncNow, OnRetryOperation(itemId), OnRefresh
**Events**: ShowSnackbar(message), SyncCompleted
**DI**: SyncQueueRepository, SyncManager, NetworkMonitor

---

## Navigation Table

| From | Action | To |
|------|--------|----|
| bottom_nav | Tap Sync tab | sync-status |
| offline_indicator_tap | Any screen's offline badge tap | sync-status |

sync-status is a terminal screen — it does not navigate anywhere else.

---

## API Endpoints Table

| Method | Path | Description |
|--------|------|-------------|
| POST | /fineract-provider/api/v1/batches | Batch sync all pending SyncQueue items to Fineract |

All other data is read from the local SQLDelight database (`sync_queue` and `app_settings` tables).

---

## SQLDelight Schema

### sync_queue table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment |
| entity_type | TEXT | MEETING, LOAN, SAVINGS, ATTENDANCE, SHARE_OUT, MEMBER |
| operation | TEXT | CREATE, UPDATE, DELETE |
| payload_json | TEXT | Full request body as JSON string |
| status | TEXT | pending, in_progress, synced, failed |
| created_at | TEXT | ISO timestamp |
| retried_at | TEXT? | Last retry timestamp |
| error_message | TEXT? | Last error if failed |

### app_settings table
| Column | Type | Description |
|--------|------|-------------|
| key | TEXT PRIMARY KEY | Setting key |
| value | TEXT | Setting value |
| last_synced_at | TEXT | ISO timestamp of last successful sync |

---

## Design Tokens Used

| Token | Value | Usage |
|-------|-------|-------|
| primary / #2E7D32 | — | SYNCED status card bg tint, Sync Now button |
| error / #D32F2F | — | FAILED status card bg tint, failed item badges |
| errorContainer / #FFDAD6 | — | Failed operations section background |
| onErrorContainer / #410002 | — | Failed section text, retry button border |
| tertiaryContainer / #D2E4FF | — | Conflict chip background |
| secondaryContainer / #FFDDB3 | — | Entity count badges |
| Custom green #C8E6C9 | — | SYNCED status card background |
| Custom amber #FFF9C4 | — | PENDING status card background |
| Custom red #FFCDD2 | — | FAILED status card background |
