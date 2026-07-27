# Behavior-assertion map — organizer-dashboard Maestro flow

Flow: `idea-layer/screens/organizer-dashboard/maestro/organizer-dashboard.yaml`
appId: `org.mifos.groupbanking` · TestTags: `OrganizerDashboardTestTags.kt` (CU-5 append-only)

## Reachability
- NavHost start = `login-signup`. Login success with an **ORGANIZER** membership auto-routes to organizer-dashboard (`LoginSignupViewModel` line ~532 `memberships.any { it.role == ORGANIZER } -> NavigateToOrganizerDashboard`). This is the only in-app entry — no deep-link launch arg exists.

## State → success_signal → tag mapping
| State | success_signal | Selector | Encoded? |
|---|---|---|---|
| Loading | spinner while companion API in flight | `id: organizer_dashboard_loading_indicator` | waited-through via `extendedWaitUntil` on screen |
| Content | KPI + schedule + quick-nav loaded | `id: organizer_dashboard_content` (+ `welcome_header`, `kpi_row`, `quick_nav_section`, `schedule_section`) | yes — asserted |
| Empty | zero-groups CTA | `id: organizer_dashboard_empty_section` / `empty_cta_button` | NOT asserted — only reachable when the account holds 0 groups (contradicts the ORGANIZER-with-groups prereq); induced-only |
| Error | inline error + retry | `id: organizer_dashboard_error_section` / `error_retry_button` | NOT asserted — requires induced API failure |

## on_click exercised
- `organizer_dashboard_kpi_groups_card` (OnViewAllGroups) → assert `id: group_list_screen`. Real nav edge (`GroupBankingNavHost` §6b `onNavigateToGroupList`).

## Backend seed prerequisites
- Demo account credentials (override `ORGANIZER_USER` / `ORGANIZER_PASS` env) that authenticate against the seeded companion/Fineract backend AND hold the ORGANIZER role in ≥1 group.

## Notes / gaps
- No tag ids invented — every selector is a real `OrganizerDashboardTestTags` / `LoginSignupTestTags` / `GroupListTestTags` constant.
- Empty + Error states are induced-only and deliberately NOT faked.
