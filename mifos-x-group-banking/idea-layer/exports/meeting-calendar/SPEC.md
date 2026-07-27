<!--
  generated_from_feature: meeting-calendar
  generated_from_feature_version: "1.0.0"
  contract_version: "2.0.0"
  source_siblings: [ui.yaml, api.yaml, docs.yaml, flow.yaml, tests.yaml]
  generated_by: /idea-feature-export-spec
  status: approved (quality_score 87)
-->

# Meeting Calendar — Feature Spec

## Overview

Calendar and list view of all meetings for the group center. Each meeting card shows meeting
number, scheduled date, status (upcoming/completed/missed), attendance count, and total KES
collected. The upcoming meeting is pinned at the top with a prominent "Start Meeting" CTA;
past meetings scroll below. Reads scheduled meetings from the Fineract
`centers/{centerId}/meetings` API and the `dt_meeting_record` datatable, then lists upcoming and
past meetings. Offline-first: results are cached via SQLDelight and served stale-while-revalidate,
with `cmp-network-monitor` gating live refresh. No money moves occur here — the app only reads
Fineract as the system of record. Admin (treasurer/chairperson) can conduct a new meeting or
review a past one.

**Route:** `/meetings` · **Entry:** `home-dashboard` (Meetings nav), bottom_nav (meetings tab)
**Nav params:** `center_id: Int`

**Acceptance Criteria:**

- AC1: On mount, load meetings for the center; cached data renders immediately then refreshes.
- AC2: The upcoming meeting is pinned at top with an enabled "Start Meeting" CTA; if none, show
       a "Next meeting not scheduled" placeholder.
- AC3: `ToggleViewMode` is a pure transform flipping LIST/CALENDAR (no network, no persistence).
- AC4: Tapping the upcoming card → `NavigateToConduct(meetingId, meetingNumber)`; tapping a
       completed/missed row → `NavigateToReview(...)`.
- AC5: Error → error banner over cached data with Retry (network-first refresh).
- AC6: Empty → empty state when no meetings exist.

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| meeting_calendar_screen | `MeetingCalendarScreen` | Column (TopAppBar + ViewToggle + PinnedUpcoming + LazyColumn) | Toggle calendar/list; upcoming card pinned; scrollable past list |

## State Model

### MeetingCalendarViewModel

**State — `MeetingCalendarState`**

| Field | Type | Default | Description |
|---|---|---|---|
| meetings | List<MeetingListItem> | `emptyList()` | Upcoming + past meetings |
| isLoading | Boolean | `true` | Initial load in flight |
| isRefreshing | Boolean | `false` | Pull-to-refresh in flight |
| viewMode | ViewMode | `ViewMode.LIST` | LIST or CALENDAR |
| error | String? | `null` | Error message |
| centerId | Int | `0` | Group center id |

**Screen States — `MeetingCalendarScreenState`**: `Loading`, `Content`, `Empty`, `Error`

| State | Components |
|---|---|
| `Loading` | top_app_bar, loading_skeleton |
| `Content` | top_app_bar, upcoming_meeting_card, section_header_past, meeting_list_item |
| `content_with_error` | top_app_bar, error_banner, upcoming_meeting_card, section_header_past, meeting_list_item |
| `Empty` | top_app_bar, empty_state |
| `Error` | top_app_bar, error_banner |

**Errors**

| Error | Message |
|---|---|
| NetworkError | "Could not load meetings. Showing cached data." |
| EmptyState | "No meetings scheduled yet." |

**Actions — `MeetingCalendarAction`**

| Action | Params | Trigger | Effect |
|---|---|---|---|
| `LoadMeetings` | — | Screen enters composition | call_api — get_center_meetings + records |
| `RefreshMeetings` | — | Pull-to-refresh / error retry | call_api — network-first refresh |
| `ToggleViewMode` | — | Tap calendar/list toggle | transform_state — flip viewMode |
| `StartMeeting` | meetingId, meetingNumber | Tap Start Meeting on upcoming card | navigate — to meeting-conduct |
| `OpenPastMeeting` | meetingId, meetingNumber | Tap completed meeting card | navigate — to previous-meeting-review |

**Events — `MeetingCalendarEvent`**

| Event | Payload | Trigger |
|---|---|---|
| `NavigateToConduct` | meetingId: String, meetingNumber: Int | Start upcoming meeting |
| `NavigateToReview` | meetingId: String, meetingNumber: Int | Open past meeting |
| `ShowError` | message: String | Load failure |

**DI Dependencies**

- `MeetingRepository` — getMeetings, records
- `NavigationManager`
- `ConnectivityObserver` (cmp-network-monitor)
- `LocalMeetingDao`

## Navigation

| Condition | Destination | Params |
|---|---|---|
| Tap Start Meeting (upcoming) | `meeting-conduct` | meeting_id, meeting_number, center_id |
| Tap completed/missed row | `previous-meeting-review` | meeting_id, meeting_number, center_id |

**navigates_to:** `meeting-conduct` (user_taps_start_meeting), `previous-meeting-review` (user_taps_completed_meeting)

## API Endpoints (2)

| ID | Method | Endpoint | Cache | Writable |
|---|---|---|---|---|
| `get_center_meetings` | GET | `/fineract-provider/api/v1/centers/{centerId}/meetings` | stale-while-revalidate, offline show_cached | no |
| `get_meeting_records_datatable` | GET | `/fineract-provider/api/v1/datatables/dt_meeting_record/{centerId}` | stale-while-revalidate | no |

See `exports/meeting-calendar/API.md`.

## Flow Logic

| Decision | Branches |
|---|---|
| `screen_loads` | cached_data_available → render Content stale, then fetch fresh · no_cache → show Loading skeleton, fetch API |
| `upcoming_meeting_exists` | true → pin upcoming card with Start Meeting CTA · false → "Next meeting not scheduled" placeholder |
| `user_taps_meeting_card` | status == upcoming → NavigateToConduct · status == completed/missed → NavigateToReview |

## Dependencies

- **Features:** `home-dashboard` (entry), `meeting-conduct`, `previous-meeting-review`
- **Libraries:** `cmp-network-monitor`; external: SQLDelight, Store5
- **Required modules:** core/network, core/database

## DTOs

See `exports/meeting-calendar/API.md`. Key types: `MeetingListItem`, `MeetingListResponse`,
`MeetingRecordList`, `MeetingRecordItem`, `MeetingStatus` (UPCOMING, COMPLETED, MISSED),
`ViewMode` (LIST, CALENDAR).

## Testing (9 scenarios)

| ID | Priority | Scenario |
|---|---|---|
| TC-MC-001 | P0 | On mount, meetings load for the center and populate the calendar |
| TC-MC-002 | P0 | Calendar view shows meeting dots on scheduled dates |
| TC-MC-003 | P1 | Toggle to LIST shows chronological meetings list |
| TC-MC-004 | P0 | Tapping a calendar date shows that date's meetings |
| TC-MC-005 | P0 | Start Meeting visible on today's meeting for ORGANIZER role |
| TC-MC-006 | P0 | OnStartMeeting navigates to meeting-conduct with ids |
| TC-MC-007 | P1 | OnViewPastMeeting navigates to previous-meeting-review |
| TC-MC-008 | P1 | Error state shows retry on load failure |
| TC-MC-009 | P1 | Pull-to-refresh reloads meetings |

Coverage targets: ViewModel 90%+, Screen 80%+, Repository 85%+.

## Designed UX Reference

- **Stitch prompts:** `idea-layer/screens/meeting-calendar/prompts/`
- **Preview HTML:** `idea-layer/screens/meeting-calendar/preview/`
- **Design conformance:** `top_app_bar` shows the app title + dynamic group-name subtitle plus a
  calendar/list toggle. `upcoming_meeting_card` (primaryContainer, 4dp elevation) pins the next
  meeting with number, date, an "Upcoming" chip, and a full-width primary "Start Meeting" button.
  Past `meeting_list_item` rows carry a numbered avatar, date · attendance line, KES collected
  trailing value, and a status chip (completed → successContainer, missed → errorContainer).
  `loading_skeleton` (4 items), `error_banner` (errorContainer + Retry), and `empty_state` cover
  the remaining states.
