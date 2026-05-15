# Component Inventory — mifos-x-group-banking

## Core Domain Components (10)

| Component | Type | Used In |
|-----------|------|---------|
| corpus_balance_card | card | group-dashboard, savings-dashboard |
| group_member_tile | list_item | member-list, member-add, meeting-conduct |
| loan_status_chip | chip | loan-list, loan-detail, member-profile |
| meeting_attendance_row | list_item | meeting-conduct, meeting-summary, previous-meeting-review |
| savings_collection_input | form_field | meeting-conduct |
| share_out_preview_card | card | share-out-preview, share-out-execute |
| sync_status_indicator | status_badge | sync-status, app-bar (global) |
| client_type_tile | selection_card | client-type-selector |
| loan_repayment_schedule_row | list_item | loan-detail, personal-loans |
| group_cycle_header | section_header | group-dashboard, savings-dashboard |

## Framework Primitives Used

- app_bar_with_offline_badge (extends top_app_bar)
- bottom_nav_bar (5 items: Dashboard, Members, Meetings, Loans, Settings)
- confirmation_dialog (share-out, loan approval, logout)
- offline_sync_snackbar (global, fires on connectivity change)
- progress_bar_card (corpus progress, loan repayment progress)
- amount_display_large (KES amounts, 20sp+)
- attendance_chip (Present/Absent/Excused)
- loan_status_chip (Active/Overdue/Closed/Defaulted/Pending)
