# Behavior-assertion map — meeting-conduct Maestro flow

Flow: `idea-layer/screens/meeting-conduct/maestro/meeting-conduct.yaml`
appId: `org.mifos.groupbanking` · TestTags: `MeetingConductTestTags.kt` (CU-5)

## Reachability
login(ORGANIZER) → organizer-dashboard → group-list → group card → group-dashboard → `group_dashboard_view_meetings_button` → meeting-calendar → `meeting_calendar_start_meeting_button` → meeting-conduct (NavHost §9d).

## State → success_signal → tag mapping
| State | success_signal | Selector | Encoded? |
|---|---|---|---|
| Loading | 5 parallel loads in flight | `id: meeting_conduct_loading_indicator` | waited-through via `extendedWaitUntil` |
| Content | wizard active — stepper + step-0 body | `id: meeting_conduct_stepper` (+ `step0_previous_review`, then `step1_attendance` after Next) | yes — asserted |
| Submitting | overlay after Submit tapped | (no dedicated tag; overlay only) | NOT asserted — post-submit only |
| SubmitSuccess | brief toast → meeting-summary | n/a → `meeting_summary_screen` | NOT asserted — see gap |
| SubmitError | error snackbar | `id: meeting_conduct_validation_error` (step-validation) | NOT asserted — induced only |

## on_click exercised
- `meeting_conduct_next_footer_button` (NextStep) → step 0→1, assert `id: meeting_conduct_step1_attendance`. Step 0 has no validation gate so this always advances.

## Backend seed prerequisites
- ORGANIZER account + group + a seeded UPCOMING meeting (for the calendar Start-Meeting CTA).

## Notes / gaps
- **Reachable prefix = step 0 → step 1.** Advancing past step 1 requires recording PRESENT/LATE/ABSENT for **every** `meeting_conduct_attendance_row_<memberId>` (validation `all_members_attendance_set`); step 3 needs savings ≥ KES 200 per member; the final Submit sequences POSTs to the Fineract collection-sheet backend. Member ids are seed-specific, so the full submit → `meeting-summary` transition is NOT deterministically scriptable in static authoring and is deliberately NOT faked here.
- No tag ids invented.
