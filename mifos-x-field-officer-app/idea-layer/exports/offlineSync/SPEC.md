<!--
generated_by: /idea-feature-export
generated_at: 2026-10-27
feature_id: offlineSync
generated_from_feature_version: "1.3"
sources:
  - screens/offlineSync/docs.yaml
  - screens/offlineSync/ui.yaml
  - screens/offlineSync/api.yaml
  - screens/offlineSync/flow.yaml
  - screens/offlineSync/data-flow.yaml
  - screens/offlineSync/tests.yaml
  - flows/offline-sync.yaml
  - journeys/field-officer-syncs-before-field.yaml
  - design-system/design-tokens.yaml
  - REQUIREMENTS.md (FR-OFF-01..08, NFR-OFF-01)
design_tier_consumed: stitch          # RULE-UI-SOURCE-001 US9: all 6 states — mockups/offlineSync/stitch/0{1..6}-offlineSync-*; picker sheet from preview/picker.html (not a screen state)
-->

# SPEC — Offline sync

Settings → Offline sync. Before going into the field, the officer chooses existing centres, groups or
clients and syncs them to the device; a durable background job downloads each one's full downstream tree so
every screen of those records opens with no network. **Download-only** — work done offline is saved as a
draft and uploaded by Settings → Sync & Drafts. The screen is a live dashboard of everything stored locally
at three levels (Centre / Group / Client) with each record's sync status.

| | |
|---|---|
| Feature id | `offlineSync` |
| Module | `feature/offlinesync` (new, flat) |
| Route | `OfflineSyncRoute` (no params) — from the Settings row "Offline sync" |
| Bottom nav | **no** — Settings sub-screen (`ui.yaml#shell`), back arrow + title |
| Business logic | `composite` — local MutableStores (`MUTABLE`), background worker in `sync/` |
| Version | 1.3 |

## Decisions (docs.yaml)

| id | decision |
|---|---|
| download-only | no upload section, no server writes; offline work → drafts → Sync & Drafts |
| separate-from-drafts | its own Settings row; Sync & Drafts unchanged |
| three-level-inventory | Centres / Groups / Clients tabs over the local inventory; via-parent rows; centre → groups → clients expand |
| sync-status-dashboard | per record: Waiting · Syncing… · Synced <t> · Out of date · N failed; needs-sync first |
| full-downstream-tree | centre → groups → clients → every loan + savings account (closed included), documents with file contents, datatables, templates |
| same-stores-as-screens | every read goes through the record screen's own store + key — "synced" = the screen opens offline |
| background-job | worker-kmp unique work `offline-sync`, survives process death; loans + datatables batched |
| refresh-mode | Manual (default) or Automatic 1/6/12/24 h, Wi-Fi only, charging only — ONE periodic job; only chosen records |

## Screens

| Screen | ViewModel | States (ui.yaml) |
|---|---|---|
| `OfflineSyncScreen` | `OfflineSyncViewModel` | loading · content · syncing · partial_failure · empty · offline |
| `RecordPickerSheet` (bottom sheet over the screen) | same ViewModel (`picker` sub-state) | loading · content · empty · error |

## Components (ui.yaml → testTag)

| Component | testTag | States | Contents |
|---|---|---|---|
| summary_header | `offline_sync_header` | all | connection chip · "N to sync" · 3 level tiles (centres/groups/clients) · last/next sync line · Sync now `offline_sync_sync_now` |
| offline_banner | `offline_sync_offline_banner` | offline | "You're offline…" |
| active_job_card | `offline_sync_active_job` | syncing | title · progress bar (done/total) · current label · Cancel `offline_sync_cancel_job` |
| job_result_card | `offline_sync_job_result` | partial_failure | "Done · N synced · M failed" · each failure with the server message · Retry failed `offline_sync_retry_failed` |
| offline_records_section | `offline_sync_records` / row `offline_sync_record_row` | content-like | level chips `offline_sync_records_level` · rows with status · Refresh `offline_sync_record_refresh` / Remove `offline_sync_record_remove` on chosen rows · expand |
| refresh_mode_card | `offline_sync_refresh_mode` | not offline | Manual/Automatic `offline_sync_refresh_mode_toggle` · interval `offline_sync_refresh_interval` · Wi-Fi `offline_sync_wifi_only` · charging `offline_sync_charging_only` |
| drafts_link | `offline_sync_drafts_link` | offline | "Work you do offline is saved as drafts." → Sync & Drafts |
| empty_offline | `offline_sync_empty` | empty | three-tile motif · copy · Add records |
| add_records_fab | `offline_sync_add_records` | content, syncing, partial_failure | opens the picker |
| record_picker | `offline_sync_picker` (+ `_tabs`, `_search`, `_list`, `_row`, `_download`) | sheet | Centres/Groups/Clients · search · multi-select · On device chip · "Download N for offline" |

## State Model

```
OfflineSyncUiState(
  online: Boolean,
  levels: LevelTotals(centres, groups, clients),
  toSync: Int,
  lastSyncedAt: Instant?, nextSyncAt: Instant?,
  activeJob: SyncJob?,            // RUNNING → syncing state
  lastResult: SyncJob?,           // FINISHED with failures → partial_failure
  level: RecordLevel,             // CENTRES | GROUPS | CLIENTS
  records: List<OfflineRecordRow>,// rows of the selected level, needs-sync first
  expanded: Set<RecordKey>,
  refresh: RefreshSettings(mode, intervalHours, wifiOnly, chargingOnly),
  picker: PickerState?,           // null = closed
  confirmRemove: OfflineRecord?,
)
```

All of it is LOCAL (`sync_job`, `offline_record`, prefs, `NetworkMonitor`) and observed, so progress
written by the worker re-renders the screen live and survives a restart. Only the picker lists are remote
(the existing centre/group/client list stores).

## Data + background (layers)

| Layer | Adds |
|---|---|
| `core/model` | `SyncTarget(kind, id, name)`, `RecordKind`, `OfflineRecord`, `RecordSyncStatus`, `SyncJob`, `SyncFailure`, `RefreshSettings` |
| `core/database` | Room `offline_record` + `sync_job` tables, DAOs, DB v20 + migration-ledger row |
| `core/datastore` | `OfflineSyncPreferences` (mode, interval, wifiOnly, chargingOnly) |
| `core/data` | `OfflineSyncRepository` (observe inventory/jobs/prefs, choose, remove, enqueue, cancel, retry) + `OfflineSyncEngine` (discover → fetch through the screen stores → record), reusing `OfflineDownloadRepositoryImpl`'s walk, extended to closed accounts + documents + datatables |
| `sync/` | `OfflineSyncWorker` (unique `offline-sync`, KEEP) + periodic `offline-refresh` (`ExistingPeriodicWorkPolicy.UPDATE`, constraints from prefs); `WorkScheduler` gains `enqueueOfflineSync` / `schedulePeriodic` / `cancelPeriodic` |
| `feature/offlinesync` | screen, picker, ViewModel, route, DI, strings ×20 |
| `feature/settings` | "Offline sync" row → `navigateToOfflineSync()` |
| `feature/center`, `feature/groups` | long-press Download → `OfflineSyncRepository.choose + enqueue` (replaces the screen-bound collector) |

## Navigation (flow.yaml)

| Trigger | Target |
|---|---|
| back | Settings |
| centre / group / client row | `centerDetail` / `groupsDetail` / `clientProfile` (open from the device when offline) |
| Sync & Drafts link (offline) | `syncAndDrafts` |

## Design (Stitch, consumed per state)

White bordered 16dp cards on `#FAFAFB`; indigo `primary` only on Sync now and the selected chip. Header:
connection + "N to sync" chips, then three equal level tiles. Rows: 40dp rounded-square initials avatar
(centre indigo, group purple, client green), name, counts, a small status line with icon coloured by
status (waiting primary, synced secondary, out of date tertiary, failed error). Syncing: one indigo-outlined
job card with progress bar + steps. Partial failure: rose result card with the server messages verbatim +
"Retry failed". Offline: amber banner, disabled Sync now, Clients tab + local search, drafts link.

## Testing

`tests.yaml` — 15 scenarios (7 high · 5 medium · 3 low). Journey `field-officer-syncs-before-field` (8
steps). Implemented as `OfflineSyncViewModelTest`, `OfflineSyncEngineTest` (tree walk, de-dup, failures per
read), `OfflineSyncScreenUiTest`, previews + Roborazzi goldens.

## Known Gaps

| Gap | Why | Rendered as |
|---|---|---|
| Offline repayment queue has no uploader | out of scope (download-only); belongs to Sync & Drafts | recorded in `docs.yaml#handoff_to_drafts` |
| Most GETs cannot be batched | the gateway's batch API routes only `loans/*` + `datatables/*` (501 otherwise) | single calls, 5 in flight |
| Exact periodic timing on iOS | the OS schedules BGTasks | "at most every N h" |
| Status bar in two Stitch renders, swapped Manual/Automatic order, an invented "Selective sync" label | Stitch output | not reproduced — code follows the ui.yaml order |
