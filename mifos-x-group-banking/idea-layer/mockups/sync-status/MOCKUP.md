# Sync Status — Mockup Specification

**Feature**: sync-status | **Route**: `/sync-status` | **Type**: detail (dashboard)
**Feature group**: offline-sync | **Flow**: offline-sync-flow
**Generated from**: `screens/sync-status/ui.yaml`, `screens/sync-status/demo-data.yaml`, `design-system/DESIGN.md`
**Generated at**: 2026-07-18 (by `/idea-render-mockup --feature sync-status`, headless LLM driver — Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: MifosSave-v3 (Material Design 3 · MD3) — comfortable density
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first · regulated-industry
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for timestamps + counts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar, Sync Now filled button
**Accent**: `#FF8F00` (`--accent-700`, amber) — reserved for pooled fund emphasis (not used on this screen)
**Success**: `#1B5E20` on `#C8E6C9` — SYNCED overall_status_card background + label
**Warning**: `#E65100` on `#FFF9C4` — PENDING overall_status_card background + label
**Danger**: `#B71C1C` on `#FFCDD2` — FAILED overall_status_card + `errorContainer` failed_operations_section
**Info**: `#1565C0` — system notices (unused on this screen)
**Muted**: `#616161` on `#F5F5F5` — Offline disabled button, secondary metadata
**Background**: `#FFFFFF` canvas · `#FAFAFA` app · `#F5F5F5` surfaceVariant (shimmer)
**Corner radius**: 16dp overall_status_card + conflict_chip · 12dp pending_breakdown_card / failed_operations_section / shimmer_status · 24dp sync_now_button (pill) · 16dp retry_button (small pill)
**Elevation**: 2dp overall_status_card / pending_breakdown_card
**Min touch target**: 56dp sync_now_button · 48dp top_bar back · 40dp retry_button
**Density**: 7/10 (dense financial dashboard — three stacked info cards fit above the fold at 1× scale)

---

## Screen: Sync Status

### Entry
- From the **personal-dashboard profile overflow menu** → Sync Status (`trigger: profile_overflow_menu_sync_status_selected`)
- From **sync_indicator_tap** on any screen when `pending_or_failed_ops_exist == true`
- Back navigation pops the route to whichever screen was previously topmost (typically personal-dashboard) — this is a **terminal** dashboard (no outbound navigation)

### Layout (state: `content`, `overallStatus = PENDING`, isOnline = true)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│      Sync Status              [#2E7D32] │  top_bar — primary green, onPrimary text
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │            ⟳ (48dp)                 │ │  overall_status_card — background #FFF9C4
│  │                                    │ │  corner 16dp, padding 20dp, elevation 2dp
│  │        Sync Pending                │ │  status_label · titleLarge, bold, #E65100
│  │                                    │ │
│  │   Last synced: 2 days ago          │ │  last_sync_text · bodySmall, onSurfaceVariant
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │  Pending Operations (3)            │ │  pending_breakdown_card — visible_when pendingCount>0
│  │                                    │ │  background surface, elevation 2dp, corner 12dp
│  │  Meeting Records            [ 1 ]  │ │  list-item · bodyMedium onSurface + badge
│  │  Savings Transactions       [ 2 ]  │ │  badge · secondaryContainer / onSecondaryContainer
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │  ⟳  Sync Now                       │ │  sync_now_button — filled, #2E7D32
│  │                                    │ │  corner 24dp, 56dp min touch, full width
│  └────────────────────────────────────┘ │  enabled_when isOnline && !isSyncing
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │
│  │  Failed Operations (1)             │ │  failed_operations_section — visible_when failedCount>0
│  │                                    │ │  background errorContainer #FFCDD2, corner 12dp
│  │  Attendance Records — CREATE       │ │  bodyMedium, onErrorContainer
│  │  HTTP 503 — server unavailable     │ │  bodySmall, onErrorContainer
│  │                        [ Retry ]   │ │  retry_button · outlined, 40dp, onErrorContainer
│  └────────────────────────────────────┘ │  → OnRetryOperation(itemId: 4)
└─────────────────────────────────────────┘
```

### Demo Data (state: `content`, from `demo-data.yaml`)

Seed state from `SyncQueueSummary` + `SyncStatusState` — a Mwangaza Women's Group field officer opens the app after a Sunday meeting; three offline writes queued, one prior attendance batch failed on Saturday:

| Field | Value |
|---|---|
| `isOnline` | `true` |
| `overallStatus` | `PENDING` |
| `pendingCount` | 3 |
| `failedCount` | 1 |
| `conflictCount` | 0 |
| `lastSyncAt` | `2026-05-09T08:30:00Z` (renders as "Last synced: 2 days ago" via `timeAgo` filter) |
| `isSyncing` | `false` |
| `pendingByType` | `{MEETING: 1, SAVINGS: 2}` |
| `isLoading` | `false` |

**Pending queue (`SyncQueueItem[]`):**

| id | entityType  | operation | payload (excerpt)                            | status  | createdAt            |
|----|-------------|-----------|----------------------------------------------|---------|----------------------|
| 1  | MEETING     | CREATE    | `centerId=1, meetingDate=2026-05-05`         | PENDING | 2026-05-09T07:00:00Z |
| 2  | SAVINGS     | CREATE    | `savingsAccountId=1001, amount=500`          | PENDING | 2026-05-09T07:05:00Z |
| 3  | SAVINGS     | CREATE    | `savingsAccountId=1002, amount=400`          | PENDING | 2026-05-09T07:05:30Z |
| 4  | ATTENDANCE  | CREATE    | `centerId=1, clientIds=[101,102,103,104,105]`| FAILED  | 2026-05-08T15:00:00Z (retried 06:45) |

- **`item` binding** — the singular row over `failedOperations` renders id 4 (the attendance batch): `entityType=ATTENDANCE`, `operation=CREATE`, `errorMessage="HTTP 503 — server unavailable"`.
- **Batch drain preview** — on `Sync Now`, the 3 pending rows compose into a `BatchSyncRequest` targeting Fineract `/batches` with `relativeUrl` `centers/1/meetings` + two `savingsaccounts/{id}/transactions?command=deposit` POSTs.
- **Batch response** — happy-path `SyncResult { successCount: 3, failedCount: 0, conflictCount: 0 }` returns `resourceId` 9001/9002/9003 for the three queue items → Store5 Bookkeeper advances rows to `synced`, `lastSyncAt` refreshes.
- **`conflict_chip` hidden** on the seed (`conflictCount == 0`); would render `tertiaryContainer` pill above `pending_breakdown_card` when set.
- **`all_synced_empty` hidden** on the seed (`pendingCount + failedCount > 0`); replaces the middle stack when both counters drop to zero.

---

## States

The ui.yaml declares 3 `screen_state` members (`Loading`, `Content`, `Error`) — each renders as a distinct HTML preview surface under `preview/`.

### `loading`
Shimmer skeleton mirroring the three stacked info cards while the local SQLDelight `SyncQueue` read + Store5 warm-start is in flight (no network call — this screen never fetches on load).

```
[ Sync Status ]                             ← top_bar visible with title
────────────────────────────────────────
[shimmer card ] ← 80dp × full width, corner 12dp, surfaceVariant
[shimmer card ]   ← shimmer_status count: 3
[shimmer card ]
```

- Cards: 80dp × full width, corner 12dp, `surfaceVariant` background shimmering 1.4s ease-in-out infinite.
- Respects `prefers-reduced-motion: reduce` (animation disabled).
- Top bar retains title "Sync Status".
- Sync Now button not rendered while `isLoading == true`.

### `content` (see layout above)
Steady-state dashboard. Composition adapts to `overallStatus`:

- **`SYNCED`** — `overall_status_card` uses `cloud_done` icon (#2E7D32) on `#C8E6C9` background, label "All Synced" (#1B5E20). `pending_breakdown_card` and `failed_operations_section` collapse (both `visible_when` counters == 0). `all_synced_empty` renders in their place with `cloud_done` icon and body "No pending or failed operations."
- **`PENDING`** — the demo layout shown above. `overall_status_card` uses `cloud_sync` icon (#E65100) on `#FFF9C4`, label "Sync Pending". Pending breakdown lists each `EntityType` humanized (`MEETING → Meeting Records`, `SAVINGS → Savings Transactions`, `ATTENDANCE → Attendance Records`, `SHARE_OUT → Share-Out Records`, `MEMBER → Member Updates`, `LOAN → Loan Operations`).
- **`FAILED`** — `overall_status_card` uses `cloud_off` icon (#B71C1C) on `#FFCDD2`, label "Sync Failed". `failed_operations_section` is the dominant surface; each row renders `entityType — operation`, its `errorMessage`, and an outlined **Retry** button.

**Offline variant** (`isOnline == false`, any status): the `sync_now_button` disables and swaps label to `"Offline — Connect to sync"`; retry buttons on failed rows disable identically. The overall status card is unchanged (queue state is the truth; connectivity is orthogonal).

**In-flight variant** (`isSyncing == true`): `sync_now_button` swaps to a loading spinner + inert state (`loading_when: isSyncing`); the top bar title remains stable; per-row Retry buttons stay tappable (they enqueue rather than block).

**Conflict variant** (`conflictCount > 0`): `conflict_chip` renders between `overall_status_card` and `pending_breakdown_card` as a tertiary-container pill (`{{conflictCount}} conflict(s) detected — review before syncing`); user must resolve conflicts elsewhere before Sync Now sends.

### `error`
Local DB read failed (SQLDelight `DbRead` error). The overall status card renders in a degraded shell with `cloud_off` iconography and the `SyncStatusError.DbRead` message ("Could not read sync queue from local database."). No retry surface is authored on the ui.yaml — recovery is via `OnRefresh` (pull to refresh) which re-reads the DB. The `SyncFailed` error variant surfaces the same card with copy "Sync failed. Check your connection and try again." after a batch attempt returned non-2xx and the queue could not advance.

```
┌ Sync Status ───────────────────────────┐
│  ┌────────────────────────────────────┐ │
│  │             ☁ (48dp)               │ │  overall_status_card degraded — #FFCDD2 background
│  │                                    │ │
│  │        Sync Failed                 │ │  status_label · #B71C1C
│  │                                    │ │
│  │  Could not read sync queue         │ │  last_sync_text replaced with error copy
│  │  from local database.              │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## Interaction Patterns

1. **Sync Now tap** → `OnSyncNow` (effect: `call_api`; libs: `cmp-network-monitor` + `Fineract batch API` + `Store5`) — collects every pending `SyncQueueItem`, composes a `BatchSyncRequest`, POSTs to Fineract `/batches`. On per-request 2xx, the Store5 `Bookkeeper` advances that row `pending → in_progress → synced` and stamps `lastSyncAt`; on non-2xx, the row transitions to `failed` with the response body captured as `errorMessage`. Conflicts surface via `conflictCount` for review before another drain.
2. **Retry tap on failed row** → `OnRetryOperation(itemId)` (effect: `call_api`; same lib set) — re-submits one previously failed row through the same Bookkeeper drain. Requires online; disabled otherwise.
3. **Pull to refresh** → `OnRefresh` — re-reads the local `SyncQueue` table via `SyncQueueRepository`. Does NOT trigger a network call (this is a local-state refresh — the drain is user-initiated only).
4. **Re-selecting Sync Status from the overflow menu** — no-op (already at destination).
5. **Conflict chip tap** (when visible) — no interaction contract declared; chip is informational only. Conflicts are resolved on entity-specific screens (loan-detail, member-profile, etc.).
6. **Terminal screen** — no outbound navigation. `SessionManager` back stack pops directly to the previous destination (typically personal-dashboard).

---

## Accessibility

- Overall status is text + colored icon + colored background — never color-only. Every state ships an English label ("All Synced" / "Sync Pending" / "Sync Failed") plus Swahili / French / Hindi translations.
- Pending breakdown badges expose `{{count}}` as their accessible name; entity labels ship humanized (`MEETING → Meeting Records`) with the same i18n set.
- Sync Now button announces its offline state via `disabled_label` — screen readers hear "Offline — Connect to sync" instead of the disabled Sync Now.
- Retry buttons on failed rows have a 40dp min touch target and expose the entity + operation in the accessible name ("Retry Attendance Records — CREATE").
- The overflow-menu Sync Status item + the global sync indicator surface `overallStatus` (cloud_done / cloud_sync / cloud_off) so the state is visible without opening the screen.
- Locales covered: English, Swahili (`Hali ya Usawazishaji` / `Sawazisha Sasa`), French (`État de Synchronisation` / `Synchroniser Maintenant`), Hindi (`सिंक स्थिति` / `अभी सिंक करें`).
- Font stack respects system settings (Roboto / SF Pro system) — dynamic type honored on iOS; density stays legible at 200% scale (three cards spill into scroll rather than truncate).

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- Status icon transition: cross-fade 200ms when `overallStatus` changes (SYNCED ↔ PENDING ↔ FAILED).
- Sync Now button: filled MD3 ripple 300ms ease-out; spinner replaces icon in-place during `isSyncing`.
- Retry button: outlined MD3 ripple 200ms; row remains in the list after a successful retry (moves to synced then vanishes on next refresh).
- Conflict chip: fade-in 150ms when `conflictCount` transitions 0 → n.
- Snackbar (`ShowSnackbar` event): standard MD3 slide-up + auto-dismiss 4s (used for "Sync complete" / "Retry succeeded" affirmations).
- Sync completion (`SyncCompleted` event): triggers a snackbar and a subtle 200ms status card background transition PENDING → SYNCED.
- Motion budget honors design_read `motion: 3/10` — no parallax, no hero, no page-load spinner beyond the shimmer.

---

## Data Flow (ui.yaml `business_logic.kind: processor`)

**Internal libs**: `cmp-network-monitor`
**External libs**: `SQLDelight`, `Store5`, `Fineract batch API`

Read paths (offline-first, always-local):
- `pendingCount` / `failedCount` / `conflictCount` / `pendingByType` / `failedOperations[]` / `overallStatus` ← `SyncQueueRepository` streamed from the SQLDelight `sync_queue` table (no network on load).
- `isOnline` ← `NetworkMonitor.isOnline` (`cmp-network-monitor`).
- `lastSyncAt` ← `SyncQueueRepository.getLastSyncTimestamp()` from the local DB.
- `isSyncing` ← `SyncManager.currentDrainState` StateFlow.

Write path (`OnSyncNow` / `OnRetryOperation`, external: Store5 MutableStore + Bookkeeper):
1. `SyncManager.drain()` reads every row where `status == PENDING` (or the single `itemId` for retry).
2. Rows are batched into a single `BatchSyncRequest` — `{ requests: [{ requestId, relativeUrl, method, body }, ...] }`.
3. Store5 `MutableStore<SyncKey, SyncBatch>` sends the batch to Fineract `/batches` via the network fetcher; `Bookkeeper` records the pre-drain snapshot.
4. Per-response: `statusCode 2xx` → Bookkeeper advances the corresponding queue row to `synced` and stamps `resourceId`; `statusCode ≥ 400` → row moves to `failed` with response body captured as `errorMessage`; the batch as a whole finalises `lastSyncAt`.
5. Conflict detection (server 409 or Fineract conflict shape) increments `conflictCount` and holds the row in `failed` for manual review — the drain does NOT auto-resolve.

Offline behavior: when `NetworkMonitor.isOffline == true`, all rows remain in the local queue; `sync_now_button` and every `retry_button` disable; no snackbar is shown (the disabled label is the message). The screen itself never renders the `error` state solely because of connectivity — that surface is reserved for local DB failures.

Terminal-screen invariant: the ViewModel emits `SyncStatusEvent.SyncCompleted` on a clean drain but never navigates — the caller (personal-dashboard overflow menu / sync indicator) decides where the user returns to.

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/sync-status/ui.yaml` |
| API contract | `idea-layer/screens/sync-status/api.yaml` |
| Data flow | `idea-layer/screens/sync-status/data-flow.yaml` |
| Demo data | `idea-layer/screens/sync-status/demo-data.yaml` |
| Flow | `idea-layer/screens/sync-status/flow.yaml` |
| Tests | `idea-layer/screens/sync-status/tests.yaml` |
| Docs | `idea-layer/screens/sync-status/docs.yaml` |
| Preview HTML (loading) | `idea-layer/screens/sync-status/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/sync-status/preview/content.html` |
| Preview HTML (error) | `idea-layer/screens/sync-status/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/sync-status/prompts/{loading,content,error}.md` |
| Stitch mockup dir | `idea-layer/mockups/sync-status/stitch/` (probe deferred) |
| Feature-group mockup | `idea-layer/mockups/offline-sync/MOCKUP.md` (Screen 1 section) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001). This MOCKUP.md is the LLM-driven analog synthesized from `ui.yaml` (v4.0), `demo-data.yaml` (v2.1.0), and `design-system/DESIGN.md` per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- Terminal-screen contract: no outbound `on_click.target`. The personal-dashboard overflow menu (and the global sync indicator) own re-entry. Any future extension (conflict resolution flow, drain history detail) must add explicit action contracts to ui.yaml — this MOCKUP.md is not a nav authority.
- The `overall_status_card` uses `style_by_status` + `value_by_status` maps in ui.yaml (single component, three visual variants) rather than three separate cards; this MOCKUP.md renders the PENDING variant as canonical and enumerates SYNCED / FAILED in the States section.
- The `pending_breakdown_card` iterates `pendingByType` as a map (`EntityType → Int`) — the six `entity_*` i18n keys cover the closed enum (`MEETING`, `LOAN`, `SAVINGS`, `ATTENDANCE`, `SHARE_OUT`, `MEMBER`).
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features sync-status
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to ui.yaml components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
