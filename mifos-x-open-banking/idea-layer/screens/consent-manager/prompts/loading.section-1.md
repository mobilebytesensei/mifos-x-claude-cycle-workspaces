# consent-manager — loading state — section 1/1

> Composition fragment. Compose into the parent (loading.md). DESIGN.md is the contract.

## Composition (top → bottom, continued)
1. **text** (#consent_title) — label: "Connected Apps", content: "Connected Apps"
2. **text** (#consent_subtitle) — label: "Manage third-party apps that have access to your account data", content: "Manage third-party apps that have access to your account data"
3. **box** (#consent_moneymanager) — label: "MoneyManager Pro consent card", content: "MoneyManager Pro consent card", on_click: { action: view_consent_detail }
4. **stack** (#moneymanager_header_row) — label: "MoneyManager Pro header row", on_click: { action: dismiss }
5. **image** (#moneymanager_logo) — label: "MoneyManager Pro logo", content: "app_logo_moneymanager"
6. **stack** (#moneymanager_info) — label: "MoneyManager Pro app info", on_click: { action: dismiss }
7. **text** (#moneymanager_name) — label: "MoneyManager Pro", content: "MoneyManager Pro"
8. **text** (#moneymanager_dates) — label: "Granted 1 Mar 2026 · Expires 1 Mar 2027", content: "Granted 1 Mar 2026 · Expires 1 Mar 2027"
9. **box** (#moneymanager_active_badge) — label: "ACTIVE", content: "ACTIVE", on_click: { action: dismiss }
10. **stack** (#moneymanager_scopes_row) — label: "MoneyManager Pro consent scopes", on_click: { action: dismiss }
11. **box** (#moneymanager_scope_read_accounts) — label: "Read Accounts", content: "Read Accounts", on_click: { action: dismiss }
12. **box** (#moneymanager_scope_view_transactions) — label: "View Transactions", content: "View Transactions", on_click: { action: dismiss }
13. **box** (#moneymanager_scope_check_balances) — label: "Check Balances", content: "Check Balances", on_click: { action: dismiss }
14. **button** (#moneymanager_revoke_button) — label: "Revoke Access", on_click: { action: revoke_consent }
15. **box** (#consent_taxhelper) — label: "TaxHelper consent card", content: "TaxHelper consent card", on_click: { action: view_consent_detail }
16. **stack** (#taxhelper_header_row) — label: "TaxHelper header row", on_click: { action: dismiss }
17. **image** (#taxhelper_logo) — label: "TaxHelper logo", content: "app_logo_taxhelper"
18. **stack** (#taxhelper_info) — label: "TaxHelper app info", on_click: { action: dismiss }
19. **text** (#taxhelper_name) — label: "TaxHelper", content: "TaxHelper"
20. **text** (#taxhelper_dates) — label: "Granted 15 Jan 2026 · Expires 15 Jan 2027", content: "Granted 15 Jan 2026 · Expires 15 Jan 2027"
21. **box** (#taxhelper_active_badge) — label: "ACTIVE", content: "ACTIVE", on_click: { action: dismiss }
22. **stack** (#taxhelper_scopes_row) — label: "TaxHelper consent scopes", on_click: { action: dismiss }
23. **box** (#taxhelper_scope_view_transactions) — label: "View Transactions", content: "View Transactions", on_click: { action: dismiss }
24. **box** (#taxhelper_scope_read_accounts) — label: "Read Accounts", content: "Read Accounts", on_click: { action: dismiss }
25. **button** (#taxhelper_revoke_button) — label: "Revoke Access", on_click: { action: revoke_consent }
26. **box** (#consent_budgetwise) — label: "BudgetWise consent card", content: "BudgetWise consent card", on_click: { action: state_change, target: view_consent_detail }
27. **stack** (#budgetwise_header_row) — label: "BudgetWise header row", on_click: { action: dismiss }
28. **image** (#budgetwise_logo) — label: "BudgetWise logo", content: "app_logo_budgetwise"
29. **stack** (#budgetwise_info) — label: "BudgetWise app info", on_click: { action: dismiss }
30. **text** (#budgetwise_name) — label: "BudgetWise", content: "BudgetWise"
31. **text** (#budgetwise_dates) — label: "Granted 10 Oct 2025 · Expired 10 Apr 2026", content: "Granted 10 Oct 2025 · Expired 10 Apr 2026"
32. **box** (#budgetwise_expired_badge) — label: "EXPIRED", content: "EXPIRED", on_click: { action: dismiss }
33. **stack** (#budgetwise_scopes_row) — label: "BudgetWise consent scopes", on_click: { action: dismiss }
34. **box** (#budgetwise_scope_check_balances) — label: "Check Balances", content: "Check Balances", on_click: { action: dismiss }
35. **button** (#budgetwise_remove_button) — label: "Remove", on_click: { action: revoke_consent }
36. **box** (#revoke_confirm_dialog) — label: "Revoke access confirmation dialog", content: "Revoke access confirmation dialog", on_click: { action: dismiss }
37. **text** (#revoke_dialog_title) — label: "Revoke access?", content: "Revoke access?"
38. **text** (#revoke_dialog_body) — label: "This will immediately remove this app's access to your account data. You can rec", content: "This will immediately remove this app's access to your account data. You can rec"
39. **stack** (#revoke_dialog_actions) — label: "Revoke dialog action buttons", on_click: { action: dismiss }
40. **button** (#revoke_dialog_cancel_button) — label: "Cancel", on_click: { action: dismiss_revoke_dialog }
41. **button** (#revoke_dialog_confirm_button) — label: "Revoke", on_click: { action: confirm_revoke_consent }
42. **image** (#empty_state_icon) — label: "No connected apps illustration", content: "ic_link_off"
43. **text** (#empty_state_title) — label: "No apps connected", content: "No apps connected"
44. **text** (#empty_state_body) — label: "Third-party apps you authorise will appear here. Visit your bank's app marketpla", content: "Third-party apps you authorise will appear here. Visit your bank's app marketpla"
