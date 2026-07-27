# Behavior-assertion map — previous-meeting-review Maestro flow

Flow: `idea-layer/screens/previous-meeting-review/maestro/previous-meeting-review.yaml`
appId: `org.mifos.groupbanking` · TestTags: `PreviousMeetingReviewTestTags.kt` (CU-5)

## Reachability
login(ORGANIZER) → organizer-dashboard → group-list → group card → group-dashboard → `group_dashboard_view_meetings_button` → meeting-calendar → tap `meeting_calendar_row_<id>` (a completed/missed past meeting) → previous-meeting-review with `launchedFrom="calendar"` (NavHost §9e).

## State → success_signal → tag mapping
| State | success_signal | Selector | Encoded? |
|---|---|---|---|
| Loading | shimmer skeleton | `id: previous_meeting_review_loading_section` | waited-through via `extendedWaitUntil` |
| Content | recap: context banner + metrics + sections | `id: previous_meeting_review_content_list` (+ `context_banner`, `summary_metrics_card`) | yes — asserted |
| Error | full-screen error | `id: previous_meeting_review_error_section` / `error_retry_button` | NOT asserted — induced load failure only |

## on_click / interaction exercised
- top-bar back (`NavigateBack`) → assert `id: meeting_calendar_screen`. The forward `start_meeting_cta` (`previous_meeting_review_start_meeting_cta`, StartNewMeeting) is `visible_when launchedFrom=="conduct"` — hidden on this calendar-launched path — so back is the reachable primary interaction here.

## Backend seed prerequisites
- ORGANIZER account + group + a seeded COMPLETED/MISSED past meeting so `meeting_calendar_row_*` exists.

## Notes / gaps
- The `conduct`-launched variant (which shows `start_meeting_cta`) is reached from meeting-conduct step-0 "View Full Report" and is covered by the meeting-conduct wizard prereqs; not re-driven here.
- Unresolved-alert card (`previous_meeting_review_unresolved_alert_card`) is `visible_when unresolvedItems.isNotEmpty()` — data-dependent, not asserted.
- No tag ids invented.
