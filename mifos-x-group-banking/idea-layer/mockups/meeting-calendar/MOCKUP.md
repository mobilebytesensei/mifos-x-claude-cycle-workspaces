# Meeting Calendar — Mockup Specification

**Feature**: meeting-calendar | **Route**: `/meetings` | **Type**: list + pinned-hero
**Feature group**: meeting-management | **Flow**: meeting-management-flow
**Generated from**: `screens/meeting-calendar/ui.yaml` (schema 4.0), `screens/meeting-calendar/demo-data.yaml` (schema 2.1.0), `design-system/DESIGN.md` (CommonPurse-v3, 2026-06-04)
**Generated at**: 2026-07-18; **regenerated 2026-08-01** (evolve R4 — re-synthesized from enriched ui.yaml: added the upcoming-card **Reschedule** link, the **no-upcoming schedule card** with a **Set / Adjust Schedule** CTA replacing the former dead "Next meeting not scheduled" placeholder, and the **schedule-editor bottom sheet**; Stitch external, MD-only fallback per RULE-STITCH-OPTIN-CONSISTENCY-001)

---

## Design Language

**System**: CommonPurse-v3 (Material Design 3 · MD3) — dense financial dashboard (density 7/10)
**Aesthetic**: `minimalist-ui` · variance 3/10 · motion 3/10 · density 7/10 · accessibility-first · regulated-industry
**Font**: Roboto (Android) / SF Pro (iOS) — system stack · Roboto Mono / SF Mono for KES amounts
**Primary**: `#2E7D32` (`--primary-700`, VSLA green) — TopAppBar fill, Start Meeting CTA, "Collected" amounts, retry action
**Primary container**: `#C8E6C9` (`--primary-100`) — Upcoming meeting hero card fill (`primaryContainer`)
**Accent**: `#FF8F00` (`--accent-700`, amber) — reserved for pooled fund emphasis (not used on this screen)
**Success**: `#2E7D32` on `#C8E6C9` — COMPLETED status chips
**Warning**: `#F57C00` — reserved (no OVERDUE state on this screen)
**Danger**: `#C62828` on `#FFCDD2` — MISSED status chips + error banner text
**Muted**: `#616161` (`--text-secondary`) on `#F5F5F5` — section header ("Past Meetings")
**Background**: `#FFFFFF` (`--bg-canvas`) canvas · `#FAFAFA` (`--bg-subtle`) app · `#F5F5F5` (`--bg-muted`) surfaceVariant (shimmer)
**Corner radius**: 24dp (`lg`) hero card · 12dp (`md`) skeleton items · full-round chips
**Elevation**: 4dp (`md`) upcoming meeting hero card · 0dp past meeting list rows (borders over shadows per DS conventions)
**Min touch target**: 72dp meeting list row · 48dp Start Meeting CTA (`min_height: 48dp`) · 44dp toggle icon
**Motion preset**: `gentle` — fast:150ms / base:200ms / slow:300ms · `cubic-bezier(0.4, 0, 0.2, 1)` · reduced-motion honored

---

## Screen: Meeting Calendar

### Entry
- From **home-dashboard** ("Meetings" nav link); nav-param `center_id: Int`
- From **bottom_nav** "Meetings" tab (`condition: meetings_tab_selected`)
- Back navigation pops the route and returns to `home-dashboard`

### Layout (state: `content`)

```
┌─────────────────────────────────────────┐
│ 9:41                     ●●● 5G ▮       │  Status bar
├─────────────────────────────────────────┤
│  Meetings                        [⇋]    │  top_app_bar · title Meetings (headlineSmall)
│  Mwangaza Women's Group                 │  subtitle bodyMedium onSurfaceVariant
│                                          │  toggle_view_btn — calendar_list icon, 44dp
├─────────────────────────────────────────┤   background: surface, elevation 0
│                                          │
│  ┌────────────────────────────────────┐ │  upcoming_meeting_card (visible_when hasUpcoming)
│  │  Meeting #5           [Upcoming]   │ │  primaryContainer #C8E6C9 fill
│  │  Tuesday, 21 Jul 2026              │ │  corner 24dp (lg), elevation 4dp
│  │                        Reschedule  │ │  reschedule_link — text btn, onPrimaryContainer, 44dp
│  │  ┌──────────────────────────────┐ │ │  → OpenScheduleEditor (opens editor sheet prefilled)
│  │  │       Start Meeting          │ │ │  Meeting #N — headlineSmall onPrimaryContainer
│  │  └──────────────────────────────┘ │ │  Date — bodyLarge onPrimaryContainer
│  └────────────────────────────────────┘ │  Upcoming chip — primary fill #2E7D32
│                                          │  Start Meeting — primary CTA full-width 48dp
│                                          │  → StartMeeting → meeting-conduct(mtg-005)
├─────────────────────────────────────────┤
│  Past Meetings                           │  section_header_past · titleSmall
│                                          │  color onSurfaceVariant, 16dp padding
├─────────────────────────────────────────┤
│  ┌──┐  Meeting #4                  KES  │  meeting_list_item — 72dp min-height
│  │ 4│  Tue, 14 Jul 2026 · 5/5      2500 │  40dp circular avatar w/ meeting #
│  └──┘  present            [Completed]   │  title bodyLarge · sub bodySmall
├─────────────────────────────────────────┤  trailing: KES bold labelLarge (primary)
│  ┌──┐  Meeting #3                        │  status chip: successContainer / errorContainer
│  │ 3│  Tue, 7 Jul 2026 · 0/5      —      │  MISSED → errorContainer #FFCDD2
│  └──┘  present            [Missed]      │  no KES trailing (nullable field)
├─────────────────────────────────────────┤
│  ┌──┐  Meeting #2                  KES  │
│  │ 2│  Tue, 30 Jun 2026 · 4/5     1900 │
│  └──┘  present            [Completed]   │  → OpenPastMeeting → previous-meeting-review
├─────────────────────────────────────────┤
│  ┌──┐  Meeting #1                  KES  │
│  │ 1│  Tue, 23 Jun 2026 · 5/5     2350 │
│  └──┘  present            [Completed]   │
│                          ↕ scroll        │  LazyColumn — past meetings scrollable
└─────────────────────────────────────────┘
```

### Layout (state: `content`, no upcoming meeting — `!hasUpcoming`)

When the group has no scheduled next meeting, the pinned hero card is replaced by the **`no_upcoming_schedule_card`** — this is the NEW element that replaces the former dead "Next meeting not scheduled" placeholder with a live CTA:

```
┌─────────────────────────────────────────┐
│  Meetings                        [⇋]    │  top_app_bar
│  Mwangaza Women's Group                 │
├─────────────────────────────────────────┤
│  ┌────────────────────────────────────┐ │  no_upcoming_schedule_card
│  │  📅+                                │ │  surfaceVariant fill, corner 24dp (lg), 20dp pad
│  │  No Upcoming Meeting                │ │  calendar_add icon 32dp onSurfaceVariant
│  │  Meetings auto-generate from your   │ │  title titleMedium onSurface
│  │  group's recurring schedule. Set or │ │  body bodyMedium onSurfaceVariant
│  │  adjust the schedule to see the     │ │
│  │  next meeting.                      │ │
│  │  ┌──────────────────────────────┐  │ │  set_schedule_cta — filled primary, 48dp full-width
│  │  │     Set / Adjust Schedule    │  │ │  → OpenScheduleEditor (opens editor sheet)
│  │  └──────────────────────────────┘  │ │
│  └────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│  Past Meetings                           │  section_header_past + list unchanged below
│  ...                                     │
└─────────────────────────────────────────┘
```

### Layout (`schedule_editor_sheet` bottom sheet — overlays any state when `showScheduleEditor == true`)

Opened by the upcoming card's **Reschedule** link, the **Set / Adjust Schedule** CTA (no-upcoming card), or the empty-state CTA. NEW modal bottom sheet:

```
                                             schedule_editor_sheet — bottom-sheet
├═════════════ drag handle ═══════════════┤  16dp top radius, 24dp inset, scrim behind
│  Meeting Schedule                        │  title titleLarge onSurface
│                                          │
│  Meeting Day                        ▾    │  schedule_day_field — dropdown (Mon…Sun), 56dp
│  ┌────────────────────────────────────┐ │  value ← scheduleDay · OnScheduleFieldChange(day)
│  │  Wednesday                         │ │
│  └────────────────────────────────────┘ │
│  Meeting Time                       🕐   │  schedule_time_field — time-picker (HH:mm), 56dp
│  ┌────────────────────────────────────┐ │  value ← scheduleTime · OnScheduleFieldChange(time)
│  │  14:00                             │ │
│  └────────────────────────────────────┘ │
│  Repeats                                 │  schedule_frequency_field — segmented button
│  [ Weekly ][ Fortnightly ][ Monthly ]   │  value ← scheduleFrequency · OnScheduleFieldChange(frequency)
│                                          │
│  ┌──────────────────────────────────┐   │  schedule_confirm_btn — "Save Schedule" filled primary 56dp
│  │          Save Schedule           │   │  enabled_when !isRescheduling && day!='' && time!=''
│  └──────────────────────────────────┘   │  loading ← isRescheduling · → RescheduleMeeting (call_api)
│               Cancel                     │  schedule_cancel_btn — text 44dp · → DismissScheduleEditor
└─────────────────────────────────────────┘
```

- `schedule_confirm_btn` "Save Schedule" is disabled until both day and time are chosen, and shows a spinner while `isRescheduling`; on success it emits `ShowScheduleUpdated` ("Meeting schedule updated"), re-runs `LoadMeetings`, and dismisses the sheet.
- `schedule_cancel_btn` "Cancel" (or scrim tap) → `DismissScheduleEditor` — closes the sheet and discards the unsaved draft (pure transform_state).

### Demo Data (state: `content`, from `demo-data.yaml`)

Five weekly-Tuesday meetings for Mwangaza Women's Group (centerId=1) — 1 UPCOMING pinned + 4 past rows:

| # | Meeting ID          | Date         | Status    | Attendance | Collected (KES) |
|---|---------------------|--------------|-----------|------------|-----------------|
| 5 | MTG-2026-07-21      | 2026-07-21   | UPCOMING  | —          | —               |
| 4 | MTG-2026-07-14      | 2026-07-14   | COMPLETED | 5 / 5      | 2,500           |
| 3 | MTG-2026-07-07      | 2026-07-07   | MISSED    | —          | —               |
| 2 | MTG-2026-06-30      | 2026-06-30   | COMPLETED | 4 / 5      | 1,900           |
| 1 | MTG-2026-06-23      | 2026-06-23   | COMPLETED | 5 / 5      | 2,350           |

Companion `MeetingRecordItem` (3 records, one per COMPLETED meeting — MISSED #3 skipped) read via `get_meeting_records_datatable` on_mount from `dt_meeting_record`:

| # | Actual Date | Total Savings | Total Repayments | Attendance | Closing Corpus (KES) |
|---|-------------|---------------|------------------|------------|----------------------|
| 1 | 2026-06-23  | 1,500         | 850              | 5          | 47,350               |
| 2 | 2026-06-30  | 1,250         | 650              | 4          | 49,250               |
| 4 | 2026-07-14  | 1,500         | 1,000            | 5          | 51,750               |

- **UPCOMING row drives the hero card + Start Meeting CTA** (`meeting-conduct` navigation target).
- **MISSED rows are visually distinct** (errorContainer chip + no KES trailing) but still tappable → `OpenPastMeeting` opens a read-only review record.
- **Closing corpus grows monotonically** (47,350 → 49,250 → 51,750 KES) — audit-consistent for the 2026-07-18 render date.
- **Weekly Tuesday cadence** preserved from the previous cycle (MISSED #3 = holiday/absent-quorum simulation).

---

## States

The ui.yaml declares 4 `screen_state` members (`Loading`, `Content`, `Empty`, `Error`) plus a hybrid `content_with_error` composite. Each renders as a distinct HTML preview surface under `preview/`.

### `loading`
Skeleton shimmer while `MeetingRepository.getMeetings(centerId)` Store5 stream is in flight — cold-start with no cache.

```
┌ Meetings                        [⇋]    ┐  top_app_bar remains rendered
├─────────────────────────────────────────┤   (title + subtitle inert)
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  loading_skeleton · count 4
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  item_height 72dp · corner md (12dp)
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  16dp margin · surfaceVariant #F5F5F5
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  shimmer 1.4s ease-in-out infinite
└─────────────────────────────────────────┘  respects prefers-reduced-motion
```

- Toggle-view icon inert (no ripple, `pointer-events: none`) during load.
- Motion preset `gentle` → shimmer collapses to static grey blocks under reduced-motion.
- No hero card rendered until first row arrives (avoids layout jump).

### `content` (see layout above)
Meetings loaded from Store5 stream. When `hasUpcoming`, the pinned hero = first item with `status == UPCOMING` and now carries a **Reschedule** text link (→ `OpenScheduleEditor`). When `!hasUpcoming`, the hero is replaced by the **`no_upcoming_schedule_card`** with a **Set / Adjust Schedule** CTA (→ `OpenScheduleEditor`) — this replaces the former dead "Next meeting not scheduled" placeholder. Past meetings scroll below in reverse-chronological order (LazyColumn). The **`schedule_editor_sheet`** bottom sheet overlays when `showScheduleEditor == true`. ViewMode default = `LIST`; toggling to `CALENDAR` swaps the LazyColumn for a month-grid (calendar view is out of scope for this MD — LIST is the reference).

### `content_with_error`
Content visible but a persistent error banner shown for stale-data warning — SQLDelight cache HAD rows, Fineract refresh FAILED. Common on flaky connectivity.

```
┌ Meetings                        [⇋]    ┐
├─────────────────────────────────────────┤
│  ⚠ Showing cached meetings —            │  error_banner
│     tap Retry to refresh    [Retry]     │  background: errorContainer #FFCDD2
├─────────────────────────────────────────┤  text_color: onErrorContainer #B71C1C
│  [Meeting #5  Upcoming     Start ▶]     │  padding 12dp
│  Past Meetings                           │  Retry → RefreshMeetings (call_api)
│  [Meeting #4  Completed   KES 2,500]    │  cmp-network-monitor gates the retry
│  ...                                     │
└─────────────────────────────────────────┘
```

- Banner is non-blocking — hero card + past list remain tappable.
- Retry re-hits `centers/{centerId}/meetings` network-first, gated by `cmp-network-monitor`.
- Offline → banner persists, list keeps cached rows visible (stale-while-revalidate).

### `empty`
Center has never held a meeting yet (e.g. a fresh group in its bootstrap window).

```
┌ Meetings                        [⇋]    ┐
├─────────────────────────────────────────┤
│                                          │
│                                          │
│               📅                          │  empty_state · calendar_empty icon
│         No Meetings Yet                  │  title titleLarge onSurface
│                                          │
│    Meetings will appear here             │  body bodyMedium --text-secondary #616161
│    once scheduled                        │
│  ┌──────────────────────────────────┐   │  empty_set_schedule_cta — filled primary 48dp
│  │       Set / Adjust Schedule       │   │  → OpenScheduleEditor (opens editor sheet)
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

- **NEW CTA** `empty_set_schedule_cta` "Set / Adjust Schedule" → `OpenScheduleEditor` opens the schedule-editor sheet so the organizer sets the group's recurring schedule; future meetings then auto-generate. (Replaces the prior no-CTA dead end.)
- Illustration uses `calendar_empty` outlined icon at 64dp, `onSurfaceVariant` tint.

### `error`
Full-screen error — Fineract API failed AND cache is empty. First-time-offline / auth expiry / server outage.

```
┌ Meetings                        [⇋]    ┐
├─────────────────────────────────────────┤
│  ⚠ Showing cached meetings —            │  error_banner surface visible
│     tap Retry to refresh    [Retry]     │
├─────────────────────────────────────────┤
│                                          │
│               ☁                          │  (composed with error_banner state,
│       Could not load meetings            │   full-screen fallback illustrating
│                                          │   the Fineract-down + no-cache path)
│    Check your connection                 │
│                                          │
│  ┌─────────── Retry ────────────────┐   │  Retry → RefreshMeetings
│  └──────────────────────────────────┘   │  effect: call_api
│                                          │  fresh=true, re-triggers Store5
└─────────────────────────────────────────┘
```

Error message vocabulary (from `state_model.errors`):
- `NetworkError` — "Could not load meetings. Showing cached data."
- `EmptyState` — "No meetings scheduled yet." (routes to `empty`, not `error`)

---

## Interaction Patterns

1. **Toggle view tap (top bar action)** → `ToggleViewMode` (effect: `transform_state`) → flips `viewMode` between `LIST` and `CALENDAR`; pure ViewModel state transition, no network, no persistence. The same cached meetings re-render in the chosen layout.
2. **Start Meeting tap (hero CTA)** → `StartMeeting(meetingId, meetingNumber, centerId)` (effect: `navigate`) → NavController push `meeting-conduct` with route args. No Fineract mutation at tap time (collection sheet screen owns the writes).
3. **Past meeting row tap** → `OpenPastMeeting(meetingId, meetingNumber, centerId)` (effect: `navigate`) → NavController push `previous-meeting-review` — read-only drill-down into the past meeting record.
4. **Pull to refresh** → `RefreshMeetings` (effect: `call_api`) → Store5 network-first, `cmp-network-monitor`-gated; success replaces SQLDelight cache, offline preserves cached rows behind the error banner.
5. **Retry tap (banner / full-screen error)** → `RefreshMeetings` (same as PTR) → identical Store5 fresh=true re-fetch. Banner dismisses on success.
6. **Screen enters composition** → `LoadMeetings` fires (default action, `on_mount`) — Store5 emits cached rows immediately then background-refreshes.
7. **Toggle icon focus** → 2dp solid `--primary-700` focus ring, 2dp offset (per DS §Accessibility) — screen-reader label "Toggle calendar/list view".
8. **Reschedule / Set-Adjust-Schedule tap** → `OpenScheduleEditor` (effect: `transform_state`) → sets `showScheduleEditor = true` and opens the `schedule_editor_sheet` prefilled with the group's current recurring `meetingDay` / `meetingTime` / `frequency`. Fired from three surfaces: the upcoming card's **Reschedule** link, the no-upcoming card's **Set / Adjust Schedule** CTA, and the empty-state CTA. Pure VM flip — no write until Confirm.
9. **Edit schedule fields (day / time / frequency)** → `OnScheduleFieldChange(day|time|frequency)` (effect: `transform_state`) → updates the corresponding draft field (`scheduleDay` / `scheduleTime` / `scheduleFrequency`); pure in-VM, no side effects.
10. **Save Schedule tap** → `RescheduleMeeting(day, time, frequency)` (effect: `call_api`) → PUTs `updateCalendar` to the Fineract collection-meeting Calendar (`PUT /centers/{centerId}/calendars/{calendarId}?command=updateCalendar` — the recurrence source of truth) and mirrors `meetingDay`/`meetingTime`/`frequency` into the `dt_group_config` datatable. On success re-runs `LoadMeetings` so the shifted recurrence renders, emits `ShowScheduleUpdated`, and dismisses the sheet. `cmp-network-monitor` gates connectivity; offline the PUT is queued to the SQLDelight `sync_queue`. Meetings are never created ad-hoc here — only the recurring schedule is adjusted.
11. **Cancel / scrim tap (editor sheet)** → `DismissScheduleEditor` (effect: `transform_state`) → sets `showScheduleEditor = false` and discards the unsaved draft; no write.

---

## Accessibility

- Meeting list row exposes a single semantic action ("Open meeting {meetingNumber} from {meetingDate}, {status}, KES {totalCollected} collected"). Missed meetings omit the amount clause.
- Status is text + colored chip — never color-only (chip label always readable: "Completed" / "Missed" / "Upcoming").
- Upcoming hero card announces "Next meeting {meetingNumber}, {meetingDate}. Double-tap Start Meeting to begin."
- Toggle-view icon carries explicit `content_description: "Toggle calendar/list view"` (ui.yaml).
- Retry action inside the error banner focusable, labeled, and reachable via TalkBack/VoiceOver swipe order.
- Min touch target 72dp on past meeting rows, 48dp on Start Meeting CTA, 44dp on toggle icon (matches DS §Component conventions).
- Locales covered (from ui.yaml `i18n.en` — Swahili / French / Hindi expansion planned): English canonical.
- WCAG AA contrast maintained: primary #2E7D32 on onPrimary white = 5.9:1; error #C62828 on errorContainer #FFCDD2 = 4.7:1.
- Text scaling honored up to 200% without layout breakage — meeting list row title/subtitle stack vertically at large text sizes; trailing KES amount wraps below chip.
- Font stack respects system settings — Roboto (Android) / SF Pro (iOS); Roboto Mono / SF Mono for KES amounts (aids OCR-style scanning in the trailing column).

---

## Motion & Feedback

- Shimmer skeleton: 1.4s ease-in-out infinite (loading state) — disabled under `prefers-reduced-motion`.
- Card ripple: MD3 standard 200ms (`base` motion token) ease-out on tap of past meeting rows.
- Toggle view: rotate icon 180°, 150ms (`fast`) — reduces to instant swap under reduced-motion.
- Start Meeting press: MD3 elevation change 4dp → 8dp + ripple, 200ms.
- Banner enter (error → content_with_error): slide-down 200ms + auto-persist (no auto-dismiss — user must Retry or connectivity restore).
- Full-screen error illustration: static (no idle animation) per DS §Motion (motion 3/10 dial).
- Retry press: MD3 button ripple only; no full-screen loader — loading state re-renders in place while Store5 re-hits Fineract.

---

## Data Flow (ui.yaml `business_logic.kind: crud`)

**External libs**: `SQLDelight`, `Store5`
**Internal libs**: `cmp-network-monitor`
**Required modules**: `core/network`, `core/database`

Read paths (offline-first, stale-while-revalidate):
- `meetings[]` ← `MeetingRepository.getMeetings(centerId)` via Store5 stream
  - Source of truth: SQLDelight `meetings` cache
  - Fetcher: Fineract `GET /centers/{centerId}/meetings` (gated by `cmp-network-monitor`)
  - `RefreshMeetings` triggers Store5 `fresh=true` (network-first)
- `meetingRecords[]` ← `get_meeting_records_datatable(centerId)` from `dt_meeting_record` (server-side datatable; populates the past-meeting rows' trailing KES + attendance)
- `viewMode` — pure in-memory ViewModel state (LIST | CALENDAR), no persistence
- `isLoading` / `isRefreshing` — derived from Store5 stream state
- `error` — nullable, populated on `NetworkError` (transient) or fatal Fineract failure

Write path: **one — the recurring schedule only** (`RescheduleMeeting`). The schedule-editor sheet PUTs `updateCalendar` to the Fineract collection-meeting Calendar (`PUT /centers/{centerId}/calendars/{calendarId}?command=updateCalendar`) and mirrors `meetingDay`/`meetingTime`/`frequency` into the `dt_group_config` datatable; `cmp-network-monitor` gates it, offline it queues to the SQLDelight `sync_queue`. No individual meeting is created or mutated here — only the recurrence the list reads from. Meeting-conduct still owns the per-meeting collection-sheet money writes.

Offline behavior: when `NetworkMonitor.isOffline == true`, cache rows still render and the error banner surfaces "Showing cached meetings — tap Retry to refresh." The list itself stays in `content` state; the banner overlays as `content_with_error`.

Idempotency & sync-conflict: no client-side writes → no rollback path. Fresh Store5 pulls silently reconcile any server-side edits (a MISSED meeting flipped to COMPLETED downstream, for example).

---

## Related Artifacts

| Type | Path |
|------|------|
| Screen YAML | `idea-layer/screens/meeting-calendar/ui.yaml` |
| API contract | `idea-layer/screens/meeting-calendar/api.yaml` |
| Data flow | `idea-layer/screens/meeting-calendar/data-flow.yaml` |
| Demo data | `idea-layer/screens/meeting-calendar/demo-data.yaml` |
| Flow | `idea-layer/screens/meeting-calendar/flow.yaml` |
| Tests | `idea-layer/screens/meeting-calendar/tests.yaml` |
| Preview HTML (loading) | `idea-layer/screens/meeting-calendar/preview/loading.html` |
| Preview HTML (content) | `idea-layer/screens/meeting-calendar/preview/content.html` |
| Preview HTML (content_with_error) | `idea-layer/screens/meeting-calendar/preview/content_with_error.html` |
| Preview HTML (empty) | `idea-layer/screens/meeting-calendar/preview/empty.html` |
| Preview HTML (error) | `idea-layer/screens/meeting-calendar/preview/error.html` |
| Stitch prompts (per state) | `idea-layer/screens/meeting-calendar/prompts/{loading,content,content_with_error,empty,error}.md` |
| Stitch mockup dir (probe deferred) | `idea-layer/mockups/meeting-calendar/stitch/` |
| Feature-group mockup | `idea-layer/mockups/meeting-management/MOCKUP.md` (planned) |

---

## Notes

- Stitch generation was NOT run in this pass (external dep — probe deferred per RULE-STITCH-OPTIN-CONSISTENCY-001; `requires_stitch: true` opt-in backfilled in ui.yaml). This MOCKUP.md is the LLM-driven analog synthesized from ui.yaml (schema 4.0) + demo-data.yaml (schema 2.1.0) + DESIGN.md tokens per RULE-CI-001 (Claude-Intelligence only on idea-layer).
- Any legacy stitch artifact under `stitch/` is stale relative to the current 5-row demo dataset (meetings rolled forward 2026-04-14..2026-05-12 → 2026-06-23..2026-07-21 in the 2026-07-18 heal) and will regenerate on the next Stitch-enabled `/idea-feature-stitch --features meeting-calendar` pass.
- Calendar view mode (`ViewMode.CALENDAR`) is declared in `state_model` but visualized here only in LIST form — the calendar month-grid layout will be authored when Stitch runs and its own preview state lands.
- Re-run with Stitch (once vault key + connectivity available):
  ```bash
  STITCH_API_KEY=<key> deno run --allow-env --allow-net --allow-read --allow-write \
    .claude-runtime/scripts/stitch-generate.ts \
    --workspace mifos-x/mifos-x-group-banking --features meeting-calendar
  ```
- Design conformance verifier: preview HTML mirrors the layout above; any hand-edit to ui.yaml components/states triggers `needs_generate_mockup` on the next `/idea-sync` cascade.
