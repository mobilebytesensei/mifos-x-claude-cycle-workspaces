# Mifos MCP — Requirements

## Functional Requirements

| ID | Requirement | Feature | Priority |
|----|-------------|---------|:--------:|
| FR-001 | Search and retrieve client profiles by ID, name, or account number with pagination | client-management | must |
| FR-002 | Create and activate client accounts with KYC fields | client-management | must |
| FR-003 | Create and manage client identifiers (passports, national IDs) | client-management | must |
| FR-004 | Apply charges/fees to client accounts with auto-discovery | client-management | should |
| FR-005 | Create and manage groups with hierarchical structure | group-management | must |
| FR-006 | Bulk add/remove group memberships | group-management | should |
| FR-007 | Full loan lifecycle: submit, approve, disburse, repay, reschedule | loan-management | must |
| FR-008 | Retrieve loan details, repayment schedule, transaction history | loan-management | must |
| FR-009 | Apply late fees (penalty charges) to loans | loan-management | should |
| FR-010 | Waive loan interest with exact amount validation | loan-management | should |
| FR-011 | Undo loan approval and disbursal (mission-critical reversals) | loan-management | must |
| FR-012 | Create, approve, activate savings accounts | savings-management | must |
| FR-013 | Deposit and withdraw funds from savings accounts | savings-management | must |
| FR-014 | Calculate and post interest to savings accounts | savings-management | should |
| FR-015 | Manage staff members and office branches | staff-organization | should |
| FR-016 | List GL accounts and manage journal entries | accounting | should |
| FR-017 | Upload, retrieve, delete documents with binary attachment support | document-management | should |
| FR-018 | Create, update, run reports with parameterized queries | reporting | could |
| FR-019 | Execute concurrent bulk operations (10+ workers) | bulk-operations | could |
| FR-020 | Holistic client views and cross-domain search | composite-operations | could |
| FR-021 | Fineract latency measurement and server runtime stats | diagnostics | could |
| FR-022 | List loan and savings products with configuration details | product-management | should |
| FR-023 | Manage charges (fees/penalties) with CRUD operations | charge-management | should |
| FR-024 | Access Fineract code tables and custom datatables | code-tables | could |
| FR-025 | Manage loan collateral with CRUD operations | collateral-management | could |

## Summary

- **Must-have**: 8 requirements (FR-001–003, FR-005, FR-007–008, FR-011–013)
- **Should-have**: 9 requirements
- **Could-have**: 8 requirements
- **Total**: 25 requirements across 15 feature domains
