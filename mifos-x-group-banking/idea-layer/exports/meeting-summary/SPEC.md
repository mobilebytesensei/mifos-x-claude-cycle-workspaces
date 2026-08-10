<!--
  generated_from_feature: meeting-summary
  generated_from_feature_version: "1.0.0"
  contract_version: "2.0.0"
  source_siblings: [ui.yaml, api.yaml, docs.yaml, flow.yaml, tests.yaml]
  generated_by: /idea-feature-export-spec
  status: approved (quality_score 88)
-->

# Meeting Summary — Feature Spec

## Overview

Read-only post-meeting summary shown immediately after a meeting is successfully submitted (or
opened from a completed meeting deep-link). Displays the date, attendance rate, total savings
collected (group + individual breakdown), loans disbursed, repayments received, fines collected,
and closing corpus balance, plus a share/export button. On entry it renders `MeetingRecordDetail`
from in-memory meeting-conduct wizard state if available, else fetches `dt_meeting_record` over
REST gated by `cmp-network-monitor` with a Store5 stale-while-revalidate SQLDelight cache keyed by
group/meeting. Totals and opening/closing corpus are reconciled at close by the collection-sheet
companion; no money movement occurs here. Admin only. Covers FR-003 / FR-019.

**Route:** `/meetings/{meetingId}/summary` · **Entry:** `meeting-conduct` (submit success), `meeting-calendar` (completed-meeting deep link)
**Nav params:** `meeting_id: String`, `meeting_number: Int`, `group_id: Int`

**Acceptance Criteria:**

- AC1: On entry, render from in-memory wizard state immediately if passed, then verify with API;
       deep-link entry shows Loading then fetches `dt_meeting_record`.
- AC2: Hero card shows total collected + closing-corpus chip; metric grid shows attendance,
       group savings, individual savings, repayments, fines, loans disbursed.
- AC3: Savings breakdown lists per-member group + individual amounts with a computed total.
- AC4: Corpus reconciliation card shows opening, closing, and net change.
- AC5: Share icon generates a text/PDF report and opens the OS share sheet (isSharing toggles).
- AC6: Done / back navigates to `meeting-calendar` (read-only — no save on exit).

## Screens

| Screen | Composable | Layout | Description |
|---|---|---|---|
| meeting_summary_screen | `MeetingSummaryScreen` | Column (TopAppBar + LazyColumn[HeroCard + MetricGrid + SavingsBreakdown + CorpusReconciliation + Done]) | Full-screen read-only summary with share |

## State Model

### MeetingSummaryViewModel

**State — `MeetingSummaryState`**

| Field | Type | Default | Description |
|---|---|---|---|
| meetingSummary | MeetingSummaryData? | `null` | Loaded record detail |
| isLoading | Boolean | `true` | Load in flight |
| error | String? | `null` | Error message |
| isSharing | Boolean | `false` | Share report composing |
| meetingId | String | `""` | From nav_params |
| meetingNumber | Int | `0` | From nav_params |
| groupId | Int | `0` | From nav_params |

**Screen States — `MeetingSummaryScreenState`**: `Loading`, `Content`, `Error`

| State | Components |
|---|---|
| `Loading` | top_app_bar, loading_skeleton |
| `Content` | top_app_bar, hero_card, metric_grid, savings_breakdown_section, corpus_reconciliation_section, done_button |
| `Error` | top_app_bar, error_banner |

**Errors**

| Error | Message |
|---|---|
| LoadFailed | "Could not load meeting summary. Showing cached data." |

**Actions — `MeetingSummaryAction`**

| Action | Trigger | Effect |
|---|---|---|
| `LoadSummary` | Screen enters composition | crud — render from wizard state or fetch dt_meeting_record |
| `ShareMeetingReport` | Tap share icon | share_external — generate text/PDF report, open OS share sheet (kmpToolkit/FileKit) |
| `NavigateDone` | Tap Done / back | navigate — to meeting-calendar |

**Events — `MeetingSummaryEvent`**

| Event | Trigger |
|---|---|
| `NavigateToCalendar` | Done / back |
| `ShareSummary` | Share icon |

**DI Dependencies**

- `MeetingRepository` — getMeetingRecord
- `ShareManager` — OS share sheet
- `NavigationManager`
- (LocalMeetingDao for cache)

## Navigation

| Condition | Destination | Params |
|---|---|---|
| Done / back | `meeting-calendar` | — |

**navigates_to:** `meeting-calendar` (user_taps_done_or_back)

## API Endpoints (1)

| ID | Method | Endpoint | Writable |
|---|---|---|---|
| `get_meeting_record` | GET | `/fineract-provider/api/v1/datatables/dt_meeting_record/{groupId}` | no |

See `exports/meeting-summary/API.md`.

## Flow Logic

| Decision | Branches |
|---|---|
| `screen_init` | data_passed_from_conduct_wizard → render from in-memory state, verify with API · deep_link_entry → show Loading, fetch dt_meeting_record |
| `share_tapped` | always → generate text/PDF report with all fields, open OS share sheet |

## Dependencies

- **Features:** `meeting-conduct` (entry), `meeting-calendar` (exit)
- **Libraries:** `cmp-network-monitor`; external: Store5, SQLDelight, kmpToolkit/FileKit (share)
- **Shared entities:** MeetingSummaryData, SavingsBreakdownItem, LoanSummaryItem

## DTOs

See `exports/meeting-summary/API.md`. Key types: `MeetingRecordDetail`, `SavingsBreakdownItem`,
`LoanSummaryItem`.

## Testing (7 scenarios)

| ID | Priority | Scenario |
|---|---|---|
| TC-MS-001 | P0 | On mount, meeting summary loads from MeetingRepository |
| TC-MS-002 | P0 | Summary displays attendance, total savings, loans disbursed |
| TC-MS-003 | P1 | Resolutions list renders pass/fail outcomes |
| TC-MS-004 | P1 | Share triggers ShareSheet with summary PDF/text |
| TC-MS-005 | P0 | Done emits NavigateDone back to meeting-calendar |
| TC-MS-006 | P1 | Error state shows retry on load failure |
| TC-MS-007 | P2 | Absent members list rendered below attendance count |

Coverage targets: ViewModel 90%+, Screen 80%+, Repository 85%+.

## Designed UX Reference

- **Stitch prompts:** `idea-layer/screens/meeting-summary/prompts/`
- **Preview HTML:** `idea-layer/screens/meeting-summary/preview/`
- **Design conformance:** `hero_card` (primary, xl radius, 4dp elevation) shows the total collected
  in displaySmall plus a closing-corpus chip. A 2-column `metric_grid` renders six color-coded
  metric cards (attendance/primaryContainer, group savings, individual savings/secondaryContainer,
  repayments/tertiaryContainer, fines/warningContainer, loans disbursed/errorContainer).
  `savings_breakdown_section` lists per-member rows with avatar, group·individual line, and a
  primary-colored total. `corpus_reconciliation_section` (tertiaryContainer) shows opening/closing/
  net-change info rows. `top_app_bar` share icon (loading while sharing) and a full-width Done button.
