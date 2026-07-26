# Behavior-assertion map — meeting-summary Maestro flow

Flow: `idea-layer/screens/meeting-summary/maestro/meeting-summary.yaml`
appId: `org.mifos.groupbanking` · TestTags: `MeetingSummaryTestTags.kt` (CU-5)

## Reachability — post-submit-only (documented gap)
meeting-summary is reached **only** via a successful full meeting-conduct submit (`NavigateToMeetingSummary`, NavHost §9b ← §9d). NavHost routes meeting-calendar past-meeting rows to `previous-meeting-review`, **not** summary, so there is no tap-only path. The executable flow drives the reachable **prefix** (login → … → meeting-conduct wizard, asserting `meeting_conduct_stepper`); the summary target assertions are documented below but not executed, because completing the 7-step submit requires per-member attendance/savings/loan data with seed-specific member ids that cannot be deterministically scripted in static authoring.

## State → success_signal → tag mapping (target, for when reached post-submit)
| State | success_signal | Selector | Encoded? |
|---|---|---|---|
| Loading | skeleton while record loads / from wizard memory | `id: meeting_summary_loading_section` | documented (target) |
| Content | hero KES card + metric grid + breakdown + Done | `id: meeting_summary_content_list` (+ `hero_card`, `metric_grid`, `corpus_reconciliation_section`, `done_button`) | documented (target) — see flow trailing comment |
| Error | full-screen error | `id: meeting_summary_error_section` / `error_retry_button` | NOT asserted — induced only |

## on_click (target)
- `meeting_summary_done_button` (NavigateDone) → `meeting_calendar_screen`.
- `meeting_summary_share_button` (ShareMeetingReport) → OS share sheet (external; not device-assertable).

## Backend seed prerequisites (to actually reach summary)
- ORGANIZER account + group + UPCOMING meeting, then a completed submit: attendance for all members, savings ≥ KES 200/member, valid corpus close — the full collection-sheet POST sequence against the Fineract companion backend.

## Notes / gaps
- Reachable prefix asserted live = up to `meeting_conduct_stepper`. Summary assertions are captured as documentation, NOT faked live assertions (truthful reachable-prefix + note-the-gap).
- No tag ids invented — every `meeting_summary_*` selector is a real `MeetingSummaryTestTags` constant.
