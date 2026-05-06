---
_blueprint:
  version: "2.88.0"
  date: "2026-05-05"
  layer: "server-layer"
  project: "mifos-x-group-banking"
  scaffolded_at: "2026-05-05"
---

# API Index — mifos-x-group-banking

> O(1) lookup: feature → Fineract endpoint group → MCP tools
> Source: API_CONTRACT.yaml + BRIDGE_AUDIT_LOG.yaml

| Feature | Endpoint Group | MCP Tools | Fineract Resource |
|---------|---------------|-----------|------------------|
| authentication | /authentication, /self/userdetails | authenticate, self_authenticate | POST /authentication |
| group-management | /groups, /centers | create_lending_group, get_group, list_all_groups | POST/GET /groups |
| member-onboarding | /clients | create_new_client, get_client, search_clients | POST/GET /clients |
| meeting-lifecycle | /meetings | record_meeting, list_meetings, record_attendance | POST/GET /meetings |
| savings-collection | /savingsaccounts | approve_activate_savings, deposit, withdraw | POST /savingsaccounts |
| group-linked-savings | /savingsaccounts | approve_activate_savings, calc_post_interest | POST /savingsaccounts |
| corpus-tracking | /datatables/dt_group_corpus | get_group_corpus, update_group_corpus | GET/PUT datatables |
| loan-management | /loans | create_new_loan, approve_disburse_loan, make_repayment | POST/GET /loans |
| share-out | /datatables/dt_share_out | record_share_out, list_share_outs | GET/POST datatables |
| offline-sync | /batches | send_batch, get_sync_state, update_sync_state | POST /batches |
| fines-tracking | /datatables/dt_meeting_attendance | record_attendance, list_attendance | GET/POST datatables |
| end-user-dashboard | /self/loans, /self/savingsaccounts | list_self_loans, list_self_savings, get_self_client | GET /self/* |
| field-officer-view | /staff, /clients | get_staff, list_all_groups, get_overdue_loans_for_client | GET /staff |
| social-fund | /datatables/dt_social_fund | get_social_fund, update_social_fund | GET/PUT datatables |
| multi-language | — | — | client-side only |

**Source of truth**: `API_CONTRACT.yaml` · **MCP server**: mifos (65 tools)
