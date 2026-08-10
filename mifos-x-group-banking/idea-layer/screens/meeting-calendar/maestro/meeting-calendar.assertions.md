# Behavior-assertion map — meeting-calendar Maestro flow

Flow: `idea-layer/screens/meeting-calendar/maestro/meeting-calendar.yaml`
appId: `org.mifos.groupbanking` · TestTags: `MeetingCalendarTestTags.kt` (CU-5)

## Reachability
login(ORGANIZER) → organizer-dashboard → `organizer_dashboard_nav_group_list_card` → group-list → `group_list_card_*` (first group) → group-dashboard → `group_dashboard_view_meetings_button` → meeting-calendar (NavHost §9c ← §7).

## State → success_signal → tag mapping
| State | success_signal | Selector | Encoded? |
|---|---|---|---|
| Loading | skeleton shimmer | `id: meeting_calendar_loading_indicator` | waited-through via `extendedWaitUntil` |
| Content | past-meeting list + pinned upcoming card | `id: meeting_calendar_lazy_column` (+ `meeting_calendar_upcoming_card`) | yes — asserted |
| Empty | no meetings illustration | `id: meeting_calendar_empty_section` | NOT asserted — mutually exclusive with Content/seeded meetings; induced-only |
| Error | inline error + retry | `id: meeting_calendar_error_section` / `error_retry_button` | NOT asserted — induced API failure only |

## on_click exercised
- `meeting_calendar_start_meeting_button` (StartMeeting) → assert `id: meeting_conduct_screen` (NavHost §9c `onNavigateToConduct`).

## Backend seed prerequisites
- ORGANIZER account + ≥1 group + a **seeded UPCOMING meeting** for that group. Without an upcoming meeting the pinned card + Start-Meeting CTA do not render, so `meeting_calendar_upcoming_card` / `start_meeting_button` asserts halt — a truthful data-gap signal, not a fake.

## Notes / gaps
- `group_list_card_` / substring id match taps the first seeded group without hardcoding a seed groupId (Maestro matches `id:` by regex substring).
- No tag ids invented.
