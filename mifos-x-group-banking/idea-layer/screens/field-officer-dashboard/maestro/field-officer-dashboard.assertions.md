# Behavior-assertion map — field-officer-dashboard Maestro flow

Flow: `idea-layer/screens/field-officer-dashboard/maestro/field-officer-dashboard.yaml`
appId: `org.mifos.groupbanking` · TestTags: `FieldOfficerDashboardTestTags.kt` (CU-5)

## Reachability
- Registered in NavHost (§6a) but **no login-landing branch** calls it. Sole in-app affordance = organizer-dashboard's `organizer_dashboard_nav_field_officer_card`, which is `visible_when fieldOfficerEnabled` (default **false**). So the flow reaches it via: login (ORGANIZER) → organizer-dashboard → Field-Officers tile.

## State → success_signal → tag mapping
| State | success_signal | Selector | Encoded? |
|---|---|---|---|
| Loading | shimmer while parallel centers+groups fetch | `id: field_officer_dashboard_loading_indicator` | waited-through via `extendedWaitUntil` |
| Content | KPI row + filter chips + group-health list | `id: field_officer_dashboard_kpi_row` (+ `filter_row`, `group_list`) | yes — asserted |
| Empty | no groups assigned | `id: field_officer_dashboard_empty_section` | NOT asserted — contradicts seeded-groups prereq; induced-only |
| Error | inline error + retry | `id: field_officer_dashboard_error_section` / `error_retry_button` | NOT asserted — induced API failure only |

## on_click exercised
- `field_officer_dashboard_card_<groupId>` (OnGroupTapped, substring-matched first card) → assert `id: group_dashboard_screen` (read-only supervisory view; NavHost §6a `onNavigateToGroupDashboard`).

## Backend seed prerequisites
- ORGANIZER demo account AND companion `fieldOfficerEnabled: true` so the quick-nav tile renders.
- ≥1 group assigned to the staffId so `field_officer_dashboard_card_*` exists.

## Notes / gaps
- **Hard gap:** if `fieldOfficerEnabled=false` (default demo), the tile is hidden and the flow halts at the `nav_field_officer_card` tap — a truthful surfacing of the reachability gap, not a faked pass.
- Filter chips open picker dialogs that carry no per-screen TestTag hook (dialog is a system overlay) — chip on_click not exercised to avoid asserting an untagged surface.
- No tag ids invented.
